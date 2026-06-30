"""
orchestrator.py
==================================================================
Module 3 of 3  -  Approval, BOT submission, notifications, audit & main()

Ties Modules 1 and 2 together into a fully unattended run:

    extract_and_transform()  ->  produce_bot_file()  ->  approve  ->
    submit_to_bot()  ->  audit + notify

Designed to run on a schedule (Task Scheduler / cron / Airflow). One process
invocation handles one or many workflow profiles.

Key safety properties
----------------------
* Idempotency: every submission carries a deterministic idempotency key
  (workflow + content hash). Re-running after a crash will NOT double-submit.
* Auto-approval guardrails: a batch is auto-submitted only if it is within
  row-count and exception-rate limits; otherwise it is parked for review.
* Dead-letter: anything that fails after retries is written to a dead-letter
  store and alerted, never silently lost.
* Every run (success or failure) is recorded in the audit log.
* PHI never leaves in alerts/logs in the clear (claim numbers are summarised
  as counts; failures reference hashed ids only).

Worst cases handled
-------------------
* BOT API 5xx / timeouts        -> retry w/ backoff, then dead-letter + alert
* Duplicate run / replay         -> idempotency key short-circuits
* Notification channel down      -> alert failure is logged, run still recorded
* Audit store unavailable        -> local append-only fallback (never lose audit)
* One profile fails              -> others still run; non-zero exit at the end
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd

from claims_pipeline import (
    EmptyResultError,
    WorkflowProfile,
    available_profiles,
    extract_and_transform,
    get_profile,
    get_secret,
    log,
    retry,
)
from macro_engine import MacroEngineError, produce_bot_file

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover
    requests = None


# ======================================================================
# Approval guardrails
# ======================================================================
@dataclass
class ApprovalDecision:
    approved: bool
    reason: str


def evaluate_approval(profile: WorkflowProfile, clean: pd.DataFrame,
                      exceptions: pd.DataFrame) -> ApprovalDecision:
    total = len(clean) + len(exceptions)
    if total == 0:
        return ApprovalDecision(False, "no rows")
    if len(clean) == 0:
        return ApprovalDecision(False, "all rows are exceptions")
    if len(clean) > profile.max_rows_auto:
        return ApprovalDecision(
            False, f"row count {len(clean)} exceeds auto limit {profile.max_rows_auto}"
        )
    exc_pct = len(exceptions) / total
    if exc_pct > profile.max_exception_pct:
        return ApprovalDecision(
            False, f"exception rate {exc_pct:.1%} exceeds {profile.max_exception_pct:.0%}"
        )
    return ApprovalDecision(True, f"auto-approved ({len(clean)} rows, {exc_pct:.1%} exceptions)")


# ======================================================================
# Idempotency
# ======================================================================
def idempotency_key(profile_name: str, df: pd.DataFrame) -> str:
    keys = [c for c in ("claim_nbr", "serv_nbr") if c in df.columns]
    basis = df[keys].astype(str).agg("|".join, axis=1).sort_values() if keys else df.astype(str).agg("|".join, axis=1)
    digest = hashlib.sha256(("".join(basis.tolist())).encode()).hexdigest()
    return f"{profile_name}:{digest[:16]}"


# ======================================================================
# Audit store (SQLite by default; pluggable for SharePoint/Dataverse/SQL)
# ======================================================================
class AuditStore:
    def __init__(self, db_path: str = "audit/claims_audit.db") -> None:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self._init()

    def _init(self) -> None:
        with sqlite3.connect(self.db_path) as cx:
            cx.execute(
                """CREATE TABLE IF NOT EXISTS runs(
                    idempotency_key TEXT PRIMARY KEY,
                    workflow TEXT, record_count INTEGER, exception_count INTEGER,
                    status TEXT, submitter TEXT, bot_ref TEXT, ts_utc TEXT)"""
            )

    def already_submitted(self, key: str) -> bool:
        with sqlite3.connect(self.db_path) as cx:
            row = cx.execute(
                "SELECT status FROM runs WHERE idempotency_key=? AND status='SUBMITTED'",
                (key,),
            ).fetchone()
        return row is not None

    def record(self, key: str, workflow: str, records: int, exceptions: int,
               status: str, bot_ref: str = "") -> None:
        entry = (
            key, workflow, records, exceptions, status,
            os.getenv("AUTOMATION_USER", "svc-claims-bot"), bot_ref,
            datetime.now(timezone.utc).isoformat(),
        )
        try:
            with sqlite3.connect(self.db_path) as cx:
                cx.execute(
                    "INSERT OR REPLACE INTO runs VALUES(?,?,?,?,?,?,?,?)", entry
                )
        except Exception as exc:  # never lose an audit record
            log.error("Audit DB write failed (%s); appending to fallback file", exc)
            with open("audit/audit_fallback.jsonl", "a", encoding="utf-8") as fh:
                fh.write(json.dumps(dict(zip(
                    ["key", "workflow", "records", "exceptions", "status",
                     "submitter", "bot_ref", "ts_utc"], entry))) + "\n")


# ======================================================================
# Notifications (Teams webhook + email via Graph; both best-effort)
# ======================================================================
class Notifier:
    def __init__(self) -> None:
        self.teams_webhook = os.getenv("TEAMS_WEBHOOK_URL")

    def alert(self, title: str, lines: list[str], level: str = "info") -> None:
        """Send a Teams card. Failure to notify never breaks the run."""
        if not (self.teams_webhook and requests):
            log.info("NOTIFY[%s] %s | %s", level, title, " / ".join(lines))
            return
        color = {"info": "0078D4", "warning": "E08E0B", "error": "C0392B"}.get(level, "0078D4")
        card = {
            "@type": "MessageCard", "@context": "http://schema.org/extensions",
            "themeColor": color, "summary": title,
            "sections": [{"activityTitle": title, "text": "  \n".join(lines)}],
        }
        try:
            resp = requests.post(self.teams_webhook, json=card, timeout=15)
            resp.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            log.error("Teams notification failed: %s", exc)


# ======================================================================
# BOT submission
# ======================================================================
class DeadLetterError(RuntimeError):
    """Submission exhausted retries; parked in dead-letter."""


@retry(times=4, base_delay=3.0)
def _post_to_bot(api_url: str, token: str, file_path: str, key: str) -> str:
    if requests is None:
        raise RuntimeError("'requests' is not installed")
    with open(file_path, "rb") as fh:
        resp = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {token}", "Idempotency-Key": key},
            files={"file": (os.path.basename(file_path), fh)},
            timeout=120,
        )
    if resp.status_code >= 500:
        raise RuntimeError(f"BOT server error {resp.status_code}")  # retryable
    if resp.status_code >= 400:
        # client error: not retryable, surface immediately
        raise DeadLetterError(f"BOT rejected file ({resp.status_code}): {resp.text[:200]}")
    return resp.json().get("job_id", "")


def submit_to_bot(file_path: str, key: str) -> str:
    api_url = get_secret("BOT_API_URL")
    token = get_secret("BOT_API_TOKEN")
    try:
        job_id = _post_to_bot(api_url, token, file_path, key)
        log.info("BOT accepted submission, job_id=%s", job_id)
        return job_id
    except DeadLetterError:
        raise
    except Exception as exc:  # retries exhausted
        raise DeadLetterError(f"BOT submission failed after retries: {exc}") from exc


def _dead_letter(file_path: str, key: str, reason: str) -> None:
    dl = Path("DeadLetter")
    dl.mkdir(parents=True, exist_ok=True)
    try:
        if os.path.exists(file_path):
            import shutil

            shutil.copy2(file_path, dl / os.path.basename(file_path))
    except Exception:  # noqa: BLE001
        pass
    with open(dl / "deadletter.log", "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.now(timezone.utc).isoformat()} | {key} | {reason}\n")


# ======================================================================
# Per-workflow run
# ======================================================================
def run_workflow(profile_name: str, audit: AuditStore, notifier: Notifier) -> bool:
    """Run a single workflow end to end. Returns True on success."""
    log.info("=== Starting workflow %s ===", profile_name)
    try:
        clean, exceptions, profile = extract_and_transform(profile_name)
    except EmptyResultError:
        log.info("[%s] nothing to process this run", profile_name)
        return True
    except Exception as exc:  # extraction/transform failure
        notifier.alert(f"{profile_name}: extraction failed", [str(exc)], "error")
        audit.record(f"{profile_name}:NA", profile_name, 0, 0, "EXTRACT_FAILED")
        return False

    key = idempotency_key(profile_name, clean)
    if audit.already_submitted(key):
        log.info("[%s] identical batch already submitted (idempotent skip)", profile_name)
        return True

    # exceptions are always surfaced, but do not block the clean batch
    if not exceptions.empty:
        notifier.alert(
            f"{profile_name}: {len(exceptions)} exception claim(s) need review",
            [f"Reasons: {exceptions['exception_reason'].value_counts().to_dict()}"],
            "warning",
        )

    decision = evaluate_approval(profile, clean, exceptions)
    if not decision.approved:
        log.warning("[%s] not auto-approved: %s", profile_name, decision.reason)
        audit.record(key, profile_name, len(clean), len(exceptions), "PARKED_FOR_REVIEW")
        notifier.alert(f"{profile_name}: held for manual review", [decision.reason], "warning")
        return True  # parking is a valid, non-error outcome

    # build the macro-enabled BOT file (Module 2)
    try:
        bot_file = produce_bot_file(profile, clean)
    except MacroEngineError as exc:
        notifier.alert(f"{profile_name}: macro/template stage failed", [str(exc)], "error")
        audit.record(key, profile_name, len(clean), len(exceptions), "MACRO_FAILED")
        return False

    # submit
    try:
        job_id = submit_to_bot(bot_file, key)
        audit.record(key, profile_name, len(clean), len(exceptions), "SUBMITTED", job_id)
        notifier.alert(
            f"{profile_name}: submitted to BOT",
            [f"{len(clean)} claims", f"job_id={job_id}", decision.reason],
            "info",
        )
        return True
    except DeadLetterError as exc:
        _dead_letter(bot_file, key, str(exc))
        audit.record(key, profile_name, len(clean), len(exceptions), "DEAD_LETTER")
        notifier.alert(f"{profile_name}: submission DEAD-LETTERED", [str(exc)], "error")
        return False


# ======================================================================
# Entry point
# ======================================================================
def main(argv: Optional[list[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    known = available_profiles()
    targets = argv if argv else known

    audit = AuditStore()
    notifier = Notifier()
    failures: list[str] = []

    for name in targets:
        try:
            get_profile(name)  # validates existence (YAML or in-code)
        except KeyError:
            log.error("Unknown workflow '%s' (known: %s)", name, known)
            failures.append(name)
            continue
        try:
            ok = run_workflow(name, audit, notifier)
        except Exception as exc:  # last-resort guard so one bad run can't abort the rest
            log.exception("[%s] unhandled error: %s", name, exc)
            ok = False
        if not ok:
            failures.append(name)

    if failures:
        log.error("Completed with failures: %s", failures)
        return 1
    log.info("All workflows completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

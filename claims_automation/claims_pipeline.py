"""
claims_pipeline.py
==================================================================
Module 1 of 3  -  Extract + Transform + Validate

Pulls pend claims from Oracle, applies the per-workflow transformation
rules (6P / ARHOMES / M2 / ...), validates them, and returns a clean
dataframe plus an exceptions dataframe ready for the macro template.

Also hosts shared infrastructure used by the other two modules:
    - HIPAA-safe logging (PHI redaction)
    - secrets retrieval (env / Azure Key Vault)
    - workflow profiles (config-driven)
    - retry helper

Healthcare notes
----------------
* PHI (claim_nbr, member/subscriber ids) is NEVER written to logs in the
  clear. The logging filter hashes any token that looks like an id.
* Monetary columns are coerced to Decimal-safe floats and zero-filled so
  the BOT never receives NULL amounts (a common pend-claim rejection cause).

Worst cases handled here
------------------------
* DB unreachable / transient ORA errors      -> retry w/ backoff, then fail loud
* Query returns zero rows                     -> short-circuit, no empty file
* Result missing an expected column           -> explicit, actionable error
* Dirty data (NaN, whitespace, mixed types)   -> coerced/trimmed safely
* Duplicate claims                            -> de-duplicated deterministically
* Missing CI (M2)                             -> routed to exceptions, not dropped
"""
from __future__ import annotations

import functools
import hashlib
import logging
import os
import re
import time
from dataclasses import dataclass, field
from typing import Callable, Optional

import pandas as pd

try:  # oracledb is optional at import time so the module loads anywhere
    import oracledb  # type: ignore
except Exception:  # pragma: no cover
    oracledb = None

try:  # PyYAML is optional; without it the engine uses the in-code registry
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


# ======================================================================
# HIPAA-safe logging
# ======================================================================
_ID_PATTERN = re.compile(r"\b([A-Z]{0,3}\d{6,})\b")  # claim/member-id-like tokens


class PHIRedactingFilter(logging.Filter):
    """Replaces id-like tokens in log records with a stable short hash."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = _ID_PATTERN.sub(self._mask, record.msg)
        if record.args:
            record.args = tuple(
                _ID_PATTERN.sub(self._mask, a) if isinstance(a, str) else a
                for a in record.args
            )
        return True

    @staticmethod
    def _mask(m: re.Match) -> str:
        digest = hashlib.sha256(m.group(1).encode()).hexdigest()[:8]
        return f"<id:{digest}>"


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger("claims")
    if logger.handlers:
        return logger
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s")
    )
    handler.addFilter(PHIRedactingFilter())
    logger.addHandler(handler)
    logger.propagate = False
    return logger


log = setup_logging()


# ======================================================================
# Secrets
# ======================================================================
def get_secret(name: str, default: Optional[str] = None) -> str:
    """Resolve a secret from Azure Key Vault if configured, else env var.

    Never hard-code credentials. Set KEYVAULT_URL to use the vault.
    """
    vault_url = os.getenv("KEYVAULT_URL")
    if vault_url:
        try:
            from azure.identity import DefaultAzureCredential  # type: ignore
            from azure.keyvault.secrets import SecretClient  # type: ignore

            client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
            return client.get_secret(name).value
        except Exception as exc:  # fall back to env on any vault failure
            log.warning("Key Vault lookup for %s failed (%s); using env fallback", name, exc)
    val = os.getenv(name, default)
    if val is None:
        raise RuntimeError(f"Required secret '{name}' not found in vault or environment")
    return val


# ======================================================================
# Retry helper
# ======================================================================
def retry(times: int = 3, base_delay: float = 2.0, exceptions: tuple = (Exception,)):
    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last = None
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:  # noqa: BLE001
                    last = exc
                    if attempt == times:
                        break
                    delay = base_delay * (2 ** (attempt - 1))
                    log.warning("%s failed (attempt %d/%d): %s; retrying in %.1fs",
                                fn.__name__, attempt, times, exc, delay)
                    time.sleep(delay)
            raise RuntimeError(f"{fn.__name__} failed after {times} attempts") from last
        return wrapper
    return decorator


# ======================================================================
# Workflow profiles  (config-driven; add a new claim type = add a profile)
# ======================================================================
@dataclass(frozen=True)
class WorkflowProfile:
    name: str
    query: str
    template_path: str
    macro_name: Optional[str] = None          # None => data-only load (no VBA run)
    # transform toggles
    zero_fill_amounts: bool = False
    trim_ex_array: bool = False
    m2_filter: bool = False
    required_columns: tuple = field(default_factory=tuple)
    amount_columns: tuple = ("AmtCoins", "AmtCopay", "AmtDeduct")
    dedupe_keys: tuple = ("claim_nbr", "serv_nbr")
    # mapping of source column -> template tab/range (used by macro_engine)
    template_map: dict = field(default_factory=dict)
    # auto-approval guardrails (used by orchestrator)
    max_rows_auto: int = 5000
    max_exception_pct: float = 0.05


_BASE_REQUIRED = ("claim_nbr", "serv_nbr", "PROF_CI_TO_APPLY")

PROFILES: dict[str, WorkflowProfile] = {
    "6P": WorkflowProfile(
        name="6P",
        query="SELECT * FROM pend_claims_vw WHERE workflow_type = '6P'",
        template_path=r"templates/6P_BOT_Template.xlsm",
        macro_name="Module1.FormatClaims",
        zero_fill_amounts=True,
        trim_ex_array=True,
        required_columns=_BASE_REQUIRED + ("ex_array",),
        template_map={"Claims": ["claim_nbr", "serv_nbr", "PROF_CI_TO_APPLY"]},
    ),
    "ARHOMES": WorkflowProfile(
        name="ARHOMES",
        query="SELECT * FROM pend_claims_vw WHERE workflow_type = 'ARHOMES'",
        template_path=r"templates/ARHOMES_BOT_Template.xlsm",
        macro_name="Module1.FormatClaims",
        zero_fill_amounts=True,
        trim_ex_array=True,
        required_columns=_BASE_REQUIRED + ("ex_array",),
        template_map={"Claims": ["claim_nbr", "serv_nbr", "PROF_CI_TO_APPLY"]},
    ),
    "M2": WorkflowProfile(
        name="M2",
        query="SELECT * FROM pend_claims_vw WHERE workflow_type = 'M2'",
        template_path=r"templates/M2_BOT_Template.xlsm",
        macro_name="Module1.FormatClaims",
        m2_filter=True,
        required_columns=_BASE_REQUIRED + ("NSA_FAC_IND",),
        template_map={"Claims": ["claim_nbr", "serv_nbr", "CI"]},
    ),
}

# Directory holding externalized YAML profiles (override via env).
PROFILES_DIR = os.getenv("CLAIMS_PROFILES_DIR", os.path.join(os.path.dirname(__file__), "profiles"))

# tuple-typed fields on WorkflowProfile: YAML lists must be coerced to tuples
_TUPLE_FIELDS = ("required_columns", "amount_columns", "dedupe_keys")
# every field the dataclass accepts (guards against typos in YAML)
_PROFILE_FIELDS = {
    "name", "query", "template_path", "macro_name", "zero_fill_amounts",
    "trim_ex_array", "m2_filter", "required_columns", "amount_columns",
    "dedupe_keys", "template_map", "max_rows_auto", "max_exception_pct",
}


def profile_from_dict(data: dict) -> WorkflowProfile:
    """Build a WorkflowProfile from a plain dict (e.g. parsed YAML).

    Coerces list fields to tuples and rejects unknown keys so a typo in a
    YAML file fails loudly instead of being silently ignored.
    """
    unknown = set(data) - _PROFILE_FIELDS
    if unknown:
        raise ProfileError(f"Profile has unknown keys: {sorted(unknown)}")
    if not data.get("name") or not data.get("query") or not data.get("template_path"):
        raise ProfileError("Profile must define at least 'name', 'query' and 'template_path'")
    kwargs = dict(data)
    for f in _TUPLE_FIELDS:
        if f in kwargs and kwargs[f] is not None:
            kwargs[f] = tuple(kwargs[f])
    return WorkflowProfile(**kwargs)


def load_yaml_profile(name: str) -> Optional[WorkflowProfile]:
    """Load profiles/<name>.yaml if PyYAML is present and the file exists."""
    if yaml is None:
        return None
    path = os.path.join(PROFILES_DIR, f"{name}.yaml")
    if not os.path.exists(path):
        path = os.path.join(PROFILES_DIR, f"{name}.yml")
        if not os.path.exists(path):
            return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except Exception as exc:
        raise ProfileError(f"Failed to parse profile '{path}': {exc}") from exc
    profile = profile_from_dict(data)
    log.info("Loaded profile '%s' from %s", name, path)
    return profile


def get_profile(name: str) -> WorkflowProfile:
    """Resolve a profile: prefer externalized YAML, fall back to the in-code registry."""
    profile = load_yaml_profile(name)
    if profile is not None:
        return profile
    if name in PROFILES:
        log.info("Loaded profile '%s' from in-code registry", name)
        return PROFILES[name]
    raise KeyError(
        f"Unknown workflow profile '{name}'. Looked in {PROFILES_DIR} and "
        f"in-code registry {list(PROFILES)}"
    )


def available_profiles() -> list[str]:
    """Names available from YAML files plus the in-code registry (deduplicated)."""
    names = set(PROFILES)
    if yaml is not None and os.path.isdir(PROFILES_DIR):
        for fn in os.listdir(PROFILES_DIR):
            if fn.endswith((".yaml", ".yml")):
                names.add(os.path.splitext(fn)[0])
    return sorted(names)


class ProfileError(RuntimeError):
    """Raised when a YAML profile is malformed or has invalid keys."""


# ======================================================================
# Extraction
# ======================================================================
class OracleExtractor:
    """Read-only Oracle access with pooling, timeouts and retries."""

    def __init__(self) -> None:
        if oracledb is None:
            raise RuntimeError("python-oracledb is not installed in this environment")
        self.user = get_secret("ORACLE_USER")
        self.password = get_secret("ORACLE_PASSWORD")
        self.dsn = get_secret("ORACLE_DSN")  # e.g. host:1521/service

    @retry(times=4, base_delay=2.0)
    def fetch(self, query: str) -> pd.DataFrame:
        log.info("Connecting to Oracle and executing query")
        conn = oracledb.connect(
            user=self.user, password=self.password, dsn=self.dsn,
            tcp_connect_timeout=15,
        )
        try:
            conn.call_timeout = 120_000  # 2-minute statement guard (ms)
            df = pd.read_sql(query, conn)
        finally:
            try:
                conn.close()
            except Exception:  # noqa: BLE001
                pass
        # normalise column names (Oracle often upper-cases)
        df.columns = [str(c) for c in df.columns]
        log.info("Query returned %d rows, %d columns", len(df), df.shape[1])
        return df


# ======================================================================
# Transformation + validation
# ======================================================================
class ClaimsTransformer:
    def __init__(self, profile: WorkflowProfile) -> None:
        self.p = profile

    # -- public ---------------------------------------------------------
    def run(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Returns (clean_df, exceptions_df)."""
        if df is None or df.empty:
            raise EmptyResultError(f"[{self.p.name}] query returned no rows; nothing to process")

        self._assert_columns(df)
        df = self._normalise(df)
        df = self._dedupe(df)

        if self.p.m2_filter:
            df = self._m2_filter(df)
        if self.p.zero_fill_amounts:
            df = self._zero_fill(df)
        if self.p.trim_ex_array:
            df = self._trim_ex_array(df)

        clean, exceptions = self._validate(df)
        log.info("[%s] %d clean rows, %d exception rows", self.p.name, len(clean), len(exceptions))
        return clean, exceptions

    # -- steps ----------------------------------------------------------
    def _assert_columns(self, df: pd.DataFrame) -> None:
        missing = [c for c in self.p.required_columns if c not in df.columns]
        if missing:
            raise SchemaError(
                f"[{self.p.name}] query result missing required columns: {missing}. "
                f"Got: {list(df.columns)}"
            )

    def _normalise(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        # trim whitespace on object cols; turn empty strings into NA
        for col in df.select_dtypes(include="object").columns:
            df[col] = (df[col].astype("string").str.strip().replace({"": pd.NA, "nan": pd.NA}))
        return df

    def _dedupe(self, df: pd.DataFrame) -> pd.DataFrame:
        keys = [k for k in self.p.dedupe_keys if k in df.columns]
        if not keys:
            return df
        before = len(df)
        df = df.drop_duplicates(subset=keys, keep="first").reset_index(drop=True)
        if before != len(df):
            log.info("[%s] removed %d duplicate rows on %s", self.p.name, before - len(df), keys)
        return df

    def _m2_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        # keep only facility NSA rows, then map PROF_CI_TO_APPLY -> CI
        mask = df["NSA_FAC_IND"].astype("string").str.upper().eq("Y")
        df = df[mask].copy()
        df["CI"] = df["PROF_CI_TO_APPLY"]
        log.info("[%s] NSA_FAC_IND='Y' filter kept %d rows", self.p.name, len(df))
        return df

    def _zero_fill(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self.p.amount_columns:
            if col not in df.columns:
                df[col] = 0.0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0).round(2)
        return df

    def _trim_ex_array(self, df: pd.DataFrame) -> pd.DataFrame:
        # business rule: drop first 2 chars of ex_array -> EX1toApply1
        s = df["ex_array"].astype("string").fillna("")
        df["EX1toApply1"] = s.str.slice(2)
        return df

    def _validate(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        reasons = pd.Series([""] * len(df), index=df.index, dtype="string")

        # CI must be present for the BOT to apply the claim
        ci_col = "CI" if "CI" in df.columns else "PROF_CI_TO_APPLY"
        ci_missing = df[ci_col].isna()
        reasons = reasons.mask(ci_missing, reasons.str.cat(["missing_CI"] * len(df), na_rep="") + ";")

        # core keys must be present
        for key in ("claim_nbr", "serv_nbr"):
            if key in df.columns:
                bad = df[key].isna()
                reasons = reasons.mask(bad, reasons + f"missing_{key};")

        is_exception = reasons.str.len() > 0
        exceptions = df[is_exception].copy()
        if not exceptions.empty:
            exceptions["exception_reason"] = reasons[is_exception].str.rstrip(";")
        clean = df[~is_exception].reset_index(drop=True)
        return clean, exceptions


# ======================================================================
# Errors
# ======================================================================
class EmptyResultError(RuntimeError):
    """Raised when the query returns no rows."""


class SchemaError(RuntimeError):
    """Raised when expected columns are absent (schema drift)."""


# ======================================================================
# Convenience entry point
# ======================================================================
def extract_and_transform(profile_name: str) -> tuple[pd.DataFrame, pd.DataFrame, WorkflowProfile]:
    profile = get_profile(profile_name)
    extractor = OracleExtractor()
    raw = extractor.fetch(profile.query)
    clean, exceptions = ClaimsTransformer(profile).run(raw)
    return clean, exceptions, profile


if __name__ == "__main__":
    import sys

    name = sys.argv[1] if len(sys.argv) > 1 else "6P"
    try:
        clean_df, exc_df, prof = extract_and_transform(name)
        log.info("Done. clean=%d exceptions=%d for %s", len(clean_df), len(exc_df), prof.name)
    except EmptyResultError as e:
        log.info("No work: %s", e)
    except (SchemaError, RuntimeError) as e:
        log.error("Pipeline failed: %s", e)
        sys.exit(1)

# Pend Claims Automation (Python)

Fully automated, unattended replacement for the manual pend-claims process:
pull from Oracle, transform (replacing the Excel macros), load the claims into
the macro-enabled BOT template, run its macro if required, submit to the BOT,
and log/alert — all on a schedule.

This replaces Power Automate Desktop (premium) with a license-free Python
solution and keeps the existing `.xlsm` BOT template in the loop.

## Modules

| File | Stage | Responsibility |
|------|-------|----------------|
| `claims_pipeline.py` | 1 | Oracle extract + pandas transform + validation. Also hosts shared infra: HIPAA-safe logging, secrets, retry, workflow profiles. |
| `macro_engine.py` | 2 | Load claims into the macro-enabled `.xlsm` and (optionally) run its VBA. Handles encryption, sheet/VBA protection, Excel crashes, atomic save, row-count verification. |
| `orchestrator.py` | 3 | Approval guardrails, idempotent BOT submission, dead-letter, Teams/email notifications, audit logging, `main()` entry point. |

## Flow

```
schedule -> extract_and_transform -> produce_bot_file -> approve -> submit_to_bot -> audit + notify
                  (Module 1)            (Module 2)                    (Module 3)
                                    M2 branch: NSA_FAC_IND filter + CI mapping
```

## Quick start

```bash
pip install -r requirements.txt

# run all workflows, or name specific ones
python orchestrator.py
python orchestrator.py M2 6P
```

## Configuration

All credentials come from **environment variables** (or Azure Key Vault if
`KEYVAULT_URL` is set). Nothing is hard-coded.

| Variable | Purpose |
|----------|---------|
| `ORACLE_USER` / `ORACLE_PASSWORD` / `ORACLE_DSN` | Read-only Oracle access (`host:1521/service`) |
| `TEMPLATE_OPEN_PASSWORD` | Only if the `.xlsm` is **encrypted** (password to open) |
| `TEMPLATE_SHEET_PASSWORD` | Only if sheets are protected and the macro does not self-unprotect |
| `BOT_API_URL` / `BOT_API_TOKEN` | BOT submission endpoint |
| `TEAMS_WEBHOOK_URL` | Teams alerts (optional) |
| `AUTOMATION_USER` | Submitter recorded in the audit log |
| `KEYVAULT_URL` | Optional: pull the above from Azure Key Vault |

### Workflow profiles

Each claim type is a profile (query + transform rules + template mapping +
guardrails). They live in code (`PROFILES` in `claims_pipeline.py`) and can be
externalized to `profiles/*.yaml` (see `profiles/6P.yaml`). Add a new claim
type by adding a profile — no engine changes.

## Macro-enabled template handling

Two strategies, chosen automatically:

* **Data-only (preferred):** `openpyxl` with `keep_vba=True` writes claims into
  the template tabs without Excel installed. Sheet protection is bypassed on
  write; a VBA-project password does **not** block this.
* **Macro-run:** if a profile sets `macro_name`, a real Excel is driven via
  `xlwings` to execute the VBA. Requires Windows + licensed Excel. Stale Excel
  processes are killed, alerts/events disabled, and Excel is always closed.

**Encrypted templates** (password required to open) are decrypted to a temp
copy via `msoffcrypto`, processed, then re-encrypted.

## Safety properties

- **HIPAA:** claim/member ids are hashed in logs; alerts carry counts, not PHI.
- **Idempotent:** a content-hash key prevents double-submission on replay.
- **Auto-approval guardrails:** oversized or high-exception batches are parked
  for manual review instead of being submitted.
- **Atomic + verified:** output written atomically and row-count checked before
  submission; half-written files are removed on error.
- **Never silently fails:** failures are dead-lettered, audited, and alerted.

## Before go-live

1. Confirm the real template **tab/range names** in each profile's `template_map`.
2. Confirm the actual **macro name** (`Module1.FormatClaims` is a placeholder).
3. Confirm which **password protection** the template uses (see the table above).
4. Run against a **test Oracle view** and a **copy** of the template first.

> Generated against the documented 5-workflow scope (6P, ARHOMES, M2, + others).
> Tune profiles and template mappings to match production before scheduling.

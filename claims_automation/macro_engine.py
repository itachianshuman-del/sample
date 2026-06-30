"""
macro_engine.py
==================================================================
Module 2 of 3  -  Load claims into the macro-enabled template and run its macro

This is the highest-risk step. It deals with a real-world .xlsm BOT
template that may carry ANY combination of:
    1. VBA project password   (locks code editor)   -> harmless to us
    2. Worksheet protection   (locked cells)         -> openpyxl bypasses; xlwings unprotects
    3. Workbook structure lock                        -> only blocks structural edits
    4. File-open ENCRYPTION   (password to open)      -> must decrypt first

Two strategies, chosen automatically:
    * DATA-ONLY  (preferred): openpyxl with keep_vba=True writes claims into
      the template's tabs WITHOUT needing Excel installed. Sheet protection is
      ignored by openpyxl on write. No password required for cases 1-3.
    * MACRO-RUN  : if the profile names a macro that must execute, drive a real
      Excel via xlwings, run the macro, then save. Used only when needed.

Worst cases handled
-------------------
* Encrypted template            -> msoffcrypto decrypt to temp, re-encrypt on save
* Template / tab / range missing -> explicit error before any write
* File locked by another process -> retry with backoff
* Excel not installed (macro-run requested) -> fail clearly OR fall back
* Excel hangs / leaves zombie processes -> pre-kill stale, guaranteed cleanup
* Macro raises at runtime        -> captured, Excel force-closed, error surfaced
* Row-count mismatch after load  -> hard fail (never ship a short file)
* Partial write / crash mid-save -> atomic write (temp file -> os.replace)
"""
from __future__ import annotations

import os
import shutil
import tempfile
import time
from pathlib import Path
from typing import Optional

import pandas as pd

from claims_pipeline import WorkflowProfile, get_secret, log, retry

try:
    import openpyxl  # type: ignore
except Exception:  # pragma: no cover
    openpyxl = None


# ======================================================================
# Protection detection + decryption
# ======================================================================
def is_encrypted(path: str) -> bool:
    """Encrypted OOXML files are OLE/CFB containers, not zips.

    A normal .xlsm starts with 'PK' (zip). An encrypted one starts with the
    OLE magic bytes D0 CF 11 E0.
    """
    try:
        with open(path, "rb") as fh:
            head = fh.read(8)
        return head[:4] == b"\xd0\xcf\x11\xe0"
    except OSError as exc:
        raise MacroEngineError(f"Cannot read template '{path}': {exc}") from exc


def decrypt_to_temp(path: str, password: str) -> str:
    """Decrypt an encrypted workbook to a temp .xlsm and return its path."""
    try:
        import msoffcrypto  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise MacroEngineError(
            "Template is encrypted but 'msoffcrypto-tool' is not installed"
        ) from exc

    fd, tmp = tempfile.mkstemp(suffix=".xlsm")
    os.close(fd)
    try:
        with open(path, "rb") as enc:
            office = msoffcrypto.OfficeFile(enc)
            office.load_key(password=password)
            with open(tmp, "wb") as out:
                office.decrypt(out)
        log.info("Template decrypted to working copy")
        return tmp
    except Exception as exc:
        _safe_unlink(tmp)
        raise MacroEngineError(f"Failed to decrypt template (wrong password?): {exc}") from exc


def encrypt_in_place(path: str, password: str) -> None:
    """Re-encrypt the output workbook with a password (msoffcrypto write)."""
    try:
        import msoffcrypto  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise MacroEngineError("Cannot re-encrypt: 'msoffcrypto-tool' missing") from exc
    fd, tmp = tempfile.mkstemp(suffix=".xlsm")
    os.close(fd)
    try:
        with open(path, "rb") as plain:
            office = msoffcrypto.OfficeFile(plain)
            with open(tmp, "wb") as out:
                office.encrypt(password, out)
        os.replace(tmp, path)
        log.info("Output workbook re-encrypted")
    except Exception as exc:
        _safe_unlink(tmp)
        raise MacroEngineError(f"Failed to re-encrypt output: {exc}") from exc


# ======================================================================
# Strategy A: data-only load with openpyxl (no Excel needed)
# ======================================================================
def populate_with_openpyxl(template_path: str, out_path: str,
                           df: pd.DataFrame, profile: WorkflowProfile) -> int:
    """Write claims into the template tabs, preserving VBA. Returns rows written."""
    if openpyxl is None:
        raise MacroEngineError("openpyxl is not installed")

    # load WITH vba so the macro project survives the save
    try:
        wb = openpyxl.load_workbook(template_path, keep_vba=True)
    except Exception as exc:
        raise MacroEngineError(f"Could not open template (corrupt or not .xlsm?): {exc}") from exc

    rows_written = 0
    try:
        for sheet_name, columns in profile.template_map.items():
            if sheet_name not in wb.sheetnames:
                raise MacroEngineError(
                    f"Template missing required tab '{sheet_name}'. Tabs: {wb.sheetnames}"
                )
            ws = wb[sheet_name]
            missing = [c for c in columns if c not in df.columns]
            if missing:
                raise MacroEngineError(f"Data missing columns for tab '{sheet_name}': {missing}")

            # NOTE: openpyxl writes regardless of sheet protection (UI-only guard)
            _clear_data_rows(ws, n_cols=len(columns))
            for r, (_, row) in enumerate(df[columns].iterrows(), start=2):  # row 1 = headers
                for c, col in enumerate(columns, start=1):
                    ws.cell(row=r, column=c, value=_clean(row[col]))
            rows_written = len(df)

        # ProcessInfo tab (best effort; created if absent)
        _write_process_info(wb, profile)

        _atomic_save(wb, out_path)
    finally:
        wb.close()

    log.info("[%s] openpyxl wrote %d rows into template", profile.name, rows_written)
    return rows_written


def _clear_data_rows(ws, n_cols: int) -> None:
    if ws.max_row and ws.max_row > 1:
        ws.delete_rows(2, ws.max_row - 1)


def _write_process_info(wb, profile: WorkflowProfile) -> None:
    name = "ProcessInfo"
    ws = wb[name] if name in wb.sheetnames else wb.create_sheet(name)
    from datetime import datetime, timezone

    ws["A1"], ws["B1"] = "process_name", profile.name
    ws["A2"], ws["B2"] = "generated_utc", datetime.now(timezone.utc).isoformat()


def _clean(value):
    if pd.isna(value):
        return None
    return value


def _atomic_save(wb, out_path: str) -> None:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(suffix=".xlsm", dir=str(out.parent))
    os.close(fd)
    try:
        wb.save(tmp)
        os.replace(tmp, out_path)  # atomic on same filesystem
    except Exception:
        _safe_unlink(tmp)
        raise


# ======================================================================
# Strategy B: run the actual VBA macro via xlwings (Windows + Excel)
# ======================================================================
def run_macro_with_xlwings(workbook_path: str, macro_name: str,
                           sheet_password: Optional[str] = None,
                           timeout_s: int = 300) -> None:
    """Open the workbook in Excel, run the named macro, save and close.

    Guarantees Excel is terminated even on failure, and pre-kills any stale
    Excel processes that could lock the file or pop a dialog.
    """
    try:
        import xlwings as xw  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise ExcelUnavailableError("xlwings/Excel not available for macro execution") from exc

    _kill_stale_excel()

    app = None
    book = None
    deadline = time.time() + timeout_s
    try:
        app = xw.App(visible=False, add_book=False)
        app.display_alerts = False
        app.screen_updating = False
        try:
            app.api.EnableEvents = False
            app.api.AskToUpdateLinks = False
        except Exception:  # noqa: BLE001 - COM property quirks across versions
            pass

        book = app.books.open(workbook_path, update_links=False)

        # if sheets are protected and the macro doesn't self-unprotect, do it
        if sheet_password:
            for sht in book.sheets:
                try:
                    sht.api.Unprotect(Password=sheet_password)
                except Exception:  # noqa: BLE001
                    pass

        log.info("Running macro %s", macro_name)
        macro = book.macro(macro_name)
        macro()  # synchronous

        if time.time() > deadline:
            raise MacroTimeoutError(f"Macro {macro_name} exceeded {timeout_s}s")

        book.save()
        log.info("Macro completed and workbook saved")
    except Exception as exc:
        raise MacroEngineError(f"Macro execution failed: {exc}") from exc
    finally:
        # guaranteed cleanup, in order, swallowing secondary errors
        if book is not None:
            try:
                book.close()
            except Exception:  # noqa: BLE001
                pass
        if app is not None:
            try:
                app.kill()
            except Exception:  # noqa: BLE001
                pass
        _kill_stale_excel()


def _kill_stale_excel() -> None:
    """Best-effort termination of orphaned Excel processes (Windows)."""
    if os.name != "nt":
        return
    try:
        import psutil  # type: ignore

        for proc in psutil.process_iter(["name"]):
            if (proc.info.get("name") or "").lower() == "excel.exe":
                try:
                    proc.kill()
                except Exception:  # noqa: BLE001
                    pass
    except Exception:
        os.system('taskkill /f /im excel.exe >nul 2>&1')  # noqa: S605 fallback


# ======================================================================
# High-level orchestration of this stage
# ======================================================================
@retry(times=3, base_delay=3.0)
def produce_bot_file(profile: WorkflowProfile, df: pd.DataFrame,
                     ready_dir: str = "ReadyForBOT") -> str:
    """Produce the populated, BOT-ready .xlsm and return its path.

    Steps: resolve protection -> populate (openpyxl) -> optional macro run
    (xlwings) -> verify row count -> re-encrypt if needed -> place in ready dir.
    """
    template = profile.template_path
    if not os.path.exists(template):
        raise MacroEngineError(f"Template not found: {template}")
    if df is None or df.empty:
        raise MacroEngineError(f"[{profile.name}] refusing to build an empty BOT file")

    working_template = template
    cleanup_tmp = None
    encrypted = is_encrypted(template)
    if encrypted:
        pw = get_secret("TEMPLATE_OPEN_PASSWORD")
        working_template = decrypt_to_temp(template, pw)
        cleanup_tmp = working_template

    out_name = f"{profile.name}_{int(time.time())}.xlsm"
    out_path = str(Path(ready_dir) / out_name)

    try:
        # Strategy A: always populate via openpyxl (works headless, ignores sheet locks)
        rows = populate_with_openpyxl(working_template, out_path, df, profile)

        # Strategy B: only if the profile requires the VBA to actually run
        if profile.macro_name:
            try:
                sheet_pw = _maybe_sheet_password()
                run_macro_with_xlwings(out_path, profile.macro_name, sheet_password=sheet_pw)
            except ExcelUnavailableError:
                # No Excel on this host. If the macro is mandatory this is fatal.
                log.error("[%s] macro run requested but Excel is unavailable", profile.name)
                raise

        _verify_row_count(out_path, expected=rows, profile=profile)

        if encrypted:
            encrypt_in_place(out_path, get_secret("TEMPLATE_OPEN_PASSWORD"))

        log.info("[%s] BOT file ready: %s", profile.name, out_path)
        return out_path
    except Exception:
        _safe_unlink(out_path)  # never leave a half-written file in the ready dir
        raise
    finally:
        if cleanup_tmp:
            _safe_unlink(cleanup_tmp)


def _maybe_sheet_password() -> Optional[str]:
    try:
        return get_secret("TEMPLATE_SHEET_PASSWORD")
    except RuntimeError:
        return None  # not configured -> assume macro self-unprotects


def _verify_row_count(path: str, expected: int, profile: WorkflowProfile) -> None:
    """Re-open the produced file and confirm the Claims tab row count matches."""
    if openpyxl is None or expected == 0:
        return
    decrypt_tmp = None
    check_path = path
    if is_encrypted(path):
        decrypt_tmp = decrypt_to_temp(path, get_secret("TEMPLATE_OPEN_PASSWORD"))
        check_path = decrypt_tmp
    try:
        wb = openpyxl.load_workbook(check_path, read_only=True, keep_vba=True)
        try:
            claims_tab = next(iter(profile.template_map.keys()))
            ws = wb[claims_tab]
            actual = max(ws.max_row - 1, 0)  # minus header
        finally:
            wb.close()
        if actual != expected:
            raise RowCountMismatchError(
                f"[{profile.name}] expected {expected} claim rows but file has {actual}"
            )
        log.info("[%s] row-count verification passed (%d)", profile.name, actual)
    finally:
        if decrypt_tmp:
            _safe_unlink(decrypt_tmp)


# ======================================================================
# Utilities + errors
# ======================================================================
def _safe_unlink(path: Optional[str]) -> None:
    if not path:
        return
    for _ in range(3):
        try:
            if os.path.exists(path):
                os.remove(path)
            return
        except PermissionError:
            time.sleep(1)  # file may be transiently locked
        except OSError:
            return


class MacroEngineError(RuntimeError):
    """Generic, actionable error from the macro stage."""


class ExcelUnavailableError(MacroEngineError):
    """Excel/xlwings not present when a macro run was required."""


class MacroTimeoutError(MacroEngineError):
    """Macro ran longer than the allowed budget."""


class RowCountMismatchError(MacroEngineError):
    """Produced file does not contain the expected number of claims."""

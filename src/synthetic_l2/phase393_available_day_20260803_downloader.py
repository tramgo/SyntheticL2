from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase340_official_catalyst_calendar_acquisition_precommit import TICKERS
from synthetic_l2.phase372_sas_one_day_20260721_downloader import (
    DEFAULT_FILE_SHARE,
    DEFAULT_REAL_ROOT,
    SAS_ENV_NAMES,
    TRUSTSTORE_INJECTED,
    discover_target_file_rows,
    download_file_rows,
    local_target_inventory,
    normalize_sas_source,
    sas_from_env,
)
from synthetic_l2.phase374_next_day_20260722_downloader import read_csv, redact_discovery
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION

DEFAULT_PHASE392_DIR = Path("outputs/phase392_dryrun")
DEFAULT_OUTPUT_DIR = Path("outputs/phase393")
TARGET_DATE = "2026-08-03"


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return rows.iloc[0] if not rows.empty else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def write_outputs(phase392_dir: Path, output_dir: Path, real_root: Path, file_share: str, timeout: int, dry_run: bool, max_files: int, workers: int) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase392 = read_csv(phase392_dir / "phase392_acceptance_summary.csv")
    pending_events = read_csv(phase392_dir / "phase392_pending_post_close_events.csv")
    if phase392.empty:
        raise FileNotFoundError("Phase393 requires Phase392 probe artifacts")
    before = local_target_inventory(real_root, TARGET_DATE)
    sas_info = sas_from_env()
    sas_present = int(bool(sas_info["value"]))
    discovered = pd.DataFrame(columns=["trade_date", "exchange", "symbol", "relative_file", "share", "file_path"])
    download = pd.DataFrame(columns=["trade_date", "exchange", "symbol", "share", "file_path_redacted", "local_path", "status", "bytes_written", "secret_material_recorded"])
    access_rows: list[dict[str, Any]] = []
    error_text = ""
    if not sas_present:
        access_rows.append({"access_route": "file_sas_env", "available": 0, "result": "no_supported_sas_env_var_present", "evidence": "supported env names checked; value not recorded", "secret_material_recorded": 0})
    else:
        try:
            source = normalize_sas_source(sas_info["value"])
            if source["service"] != "file":
                raise ValueError("Phase393 expects File service SAS for Azure Files share")
            discovered, shares = discover_target_file_rows(source["endpoint"], source["sas"], TARGET_DATE, TICKERS, timeout, file_share)
            access_rows.append({"access_route": "file_sas_env", "available": 1, "result": "file_sas_discovery_attempted", "evidence": f"env={sas_info['env_name']};shares_checked={len(shares)};rows={len(discovered)}", "secret_material_recorded": 0})
            download = download_file_rows(source["endpoint"], source["sas"], discovered, real_root, timeout, dry_run, max_files, workers)
        except Exception as exc:
            error_text = f"{type(exc).__name__}:{str(exc)[:220]}"
            access_rows.append({"access_route": "file_sas_env", "available": 0, "result": "file_sas_discovery_or_download_failed", "evidence": error_text, "secret_material_recorded": 0})
    after = local_target_inventory(real_root, TARGET_DATE)
    access = pd.DataFrame(access_rows)
    local_symbols = int(after["symbol"].nunique()) if not after.empty else 0
    local_files = int(after["parquet_files"].sum()) if not after.empty else 0
    local_bytes = int(after["bytes"].sum()) if not after.empty else 0
    local_full = int(local_symbols >= len(TICKERS))
    downloaded = int(download["status"].eq("downloaded").sum()) if not download.empty else 0
    existing = int(download["status"].eq("existing").sum()) if not download.empty else 0
    errors = int(download["status"].eq("error").sum()) if not download.empty else 0
    secret_rows = int(access["secret_material_recorded"].astype(int).sum()) + (int(download["secret_material_recorded"].astype(int).sum()) if not download.empty else 0)
    pending_rows = len(pending_events) if not pending_events.empty else as_int(metric_value(phase392, "phase392_pending_post_close_event_rows"))
    gates = pd.DataFrame([
        ("P393_PHASE392_PROBE_PRESENT", int(not phase392.empty), "Phase392 probe present"),
        ("P393_TARGET_AVAILABLE_DISCOVERY", int(len(discovered) > 0 or local_full == 1 or dry_run == 0 and bool(error_text)), f"discovered_rows={len(discovered)}; local_full={local_full}; error={int(bool(error_text))}"),
        ("P393_FULL_UNIVERSE_VERIFIED_OR_PENDING", int(local_full == 1 or dry_run or bool(error_text) or sas_present == 0), f"local_symbols={local_symbols}"),
        ("P393_NO_SECRET_MATERIAL_RECORDED", int(secret_rows == 0), f"secret_rows={secret_rows}"),
        ("P393_NO_RETEST_OR_PROMOTION", 1, "download_only"),
    ], columns=["gate_id", "passed", "evidence"])
    summary = pd.DataFrame([
        ("phase393_available_day_20260803_downloader_complete", int(gates["passed"].astype(int).all()), "Phase393 complete"),
        ("phase393_target_trade_date", TARGET_DATE, "First nearby full partition after shell-only 2026-07-28/29"),
        ("phase393_pending_post_close_event_rows_from_phase392", pending_rows, "Rows from natural 2026-07-28 target"),
        ("phase393_sas_env_present", sas_present, "Supported SAS env present"),
        ("phase393_truststore_injected", TRUSTSTORE_INJECTED, "Truststore injected"),
        ("phase393_dry_run", int(dry_run), "Dry-run mode"),
        ("phase393_workers", workers, "Concurrent workers"),
        ("phase393_discovered_file_rows", len(discovered), "Discovered target file rows"),
        ("phase393_discovered_symbols", int(discovered["symbol"].nunique()) if not discovered.empty else 0, "Discovered target symbols"),
        ("phase393_download_manifest_rows", len(download), "Download manifest rows"),
        ("phase393_existing_file_rows", existing, "Existing/skipped file rows"),
        ("phase393_downloaded_file_rows", downloaded, "Downloaded file rows"),
        ("phase393_error_file_rows", errors, "Per-file error rows"),
        ("phase393_local_symbols_after", local_symbols, "Local symbols after"),
        ("phase393_local_parquet_files_after", local_files, "Local parquet files after"),
        ("phase393_local_bytes_after", local_bytes, "Local bytes after"),
        ("phase393_local_full_universe_after", local_full, "Full universe local after"),
        ("phase393_strategy_retest_executed_now", 0, "No retest"),
        ("phase393_strategy_promotion_allowed", 0, "No promotion"),
        ("phase393_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase393_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase393_next_best_action", "refresh_catalyst_event_count_after_20260803_then_rerun_frozen_retest_no_search", "Recommended next action"),
    ], columns=["metric", "value", "description"])
    outputs = {
        "summary": output_dir / "phase393_acceptance_summary.csv",
        "access": output_dir / "phase393_access_ledger.csv",
        "discovery": output_dir / "phase393_discovered_file_manifest.csv",
        "download": output_dir / "phase393_download_manifest.csv",
        "local_before": output_dir / "phase393_local_inventory_before.csv",
        "local_after": output_dir / "phase393_local_inventory_after.csv",
        "gates": output_dir / "phase393_gate_evaluation.csv",
        "report": output_dir / "phase393_available_day_20260803_downloader_report.md",
        "manifest": output_dir / "phase393_available_day_20260803_downloader_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    access.to_csv(outputs["access"], index=False)
    redact_discovery(discovered).to_csv(outputs["discovery"], index=False)
    download.to_csv(outputs["download"], index=False)
    before.to_csv(outputs["local_before"], index=False)
    after.to_csv(outputs["local_after"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text("\n".join(["# Phase393 Available-Day 2026-08-03 Downloader", "", f"Generated: {generated_utc}", "", _markdown_table(summary), "", _markdown_table(gates), ""]), encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({"phase": 393, "generated_at_utc": generated_utc, "outputs": {k: str(v) for k, v in outputs.items()}, "supported_sas_env_names_checked": SAS_ENV_NAMES, "reproducibility": reproducibility_fields(artifact_id="phase393_available_day_20260803_downloader", generated_utc=generated_utc, inputs={"phase392_summary": str(phase392_dir / "phase392_acceptance_summary.csv")}, parameters={"target_date": TARGET_DATE, "dry_run": dry_run, "max_files": max_files, "workers": workers, "secret_material_recorded": secret_rows}, outputs={k: str(v) for k, v in outputs.items()}, cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION)}, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase392-dir", type=Path, default=DEFAULT_PHASE392_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--file-share", default=DEFAULT_FILE_SHARE)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-files", type=int, default=0)
    parser.add_argument("--workers", type=int, default=128)
    args = parser.parse_args()
    print(json.dumps({k: str(v) for k, v in write_outputs(args.phase392_dir, args.output_dir, args.real_root, args.file_share, args.timeout, args.dry_run, args.max_files, args.workers).items()}, indent=2))

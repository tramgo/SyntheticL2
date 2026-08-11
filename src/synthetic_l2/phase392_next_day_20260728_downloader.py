from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta, timezone
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

DEFAULT_PHASE385_DIR = Path("outputs/phase385")
DEFAULT_PHASE391_DIR = Path("outputs/phase391")
DEFAULT_OUTPUT_DIR = Path("outputs/phase392")


def next_weekday(text: str) -> str:
    dt = date.fromisoformat(text) + timedelta(days=1)
    while dt.weekday() >= 5:
        dt += timedelta(days=1)
    return dt.isoformat()


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


def pick_target(eligibility: pd.DataFrame) -> tuple[str, pd.DataFrame]:
    pending = eligibility[
        eligibility["market_session"].astype(str).eq("post_close")
        & eligibility["diagnostic_trade_date"].fillna("").astype(str).eq("")
    ].copy()
    if pending.empty:
        return "", pending
    source_date = sorted(pending["announcement_date"].dropna().astype(str).unique().tolist())[-1]
    return next_weekday(source_date), pending[pending["announcement_date"].astype(str).eq(source_date)].copy()


def write_outputs(phase385_dir: Path, phase391_dir: Path, output_dir: Path, real_root: Path, file_share: str, timeout: int, dry_run: bool, max_files: int, workers: int) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    eligibility = read_csv(phase385_dir / "phase373_no_lookahead_official_catalyst_eligibility.csv")
    phase391 = read_csv(phase391_dir / "phase391_acceptance_summary.csv")
    if eligibility.empty or phase391.empty:
        raise FileNotFoundError("Phase392 requires Phase385 eligibility and Phase391 interpretation")
    target_date, pending_events = pick_target(eligibility)
    before = local_target_inventory(real_root, target_date)
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
                raise ValueError("Phase392 expects File service SAS for Azure Files share")
            discovered, shares = discover_target_file_rows(source["endpoint"], source["sas"], target_date, TICKERS, timeout, file_share)
            access_rows.append({"access_route": "file_sas_env", "available": 1, "result": "file_sas_discovery_attempted", "evidence": f"env={sas_info['env_name']};shares_checked={len(shares)};rows={len(discovered)}", "secret_material_recorded": 0})
            download = download_file_rows(source["endpoint"], source["sas"], discovered, real_root, timeout, dry_run, max_files, workers)
        except Exception as exc:
            error_text = f"{type(exc).__name__}:{str(exc)[:220]}"
            access_rows.append({"access_route": "file_sas_env", "available": 0, "result": "file_sas_discovery_or_download_failed", "evidence": error_text, "secret_material_recorded": 0})
    after = local_target_inventory(real_root, target_date)
    access = pd.DataFrame(access_rows)
    local_symbols = int(after["symbol"].nunique()) if not after.empty else 0
    local_files = int(after["parquet_files"].sum()) if not after.empty else 0
    local_bytes = int(after["bytes"].sum()) if not after.empty else 0
    local_full = int(local_symbols >= len(TICKERS))
    downloaded = int(download["status"].eq("downloaded").sum()) if not download.empty else 0
    existing = int(download["status"].eq("existing").sum()) if not download.empty else 0
    errors = int(download["status"].eq("error").sum()) if not download.empty else 0
    secret_rows = int(access["secret_material_recorded"].astype(int).sum()) + (int(download["secret_material_recorded"].astype(int).sum()) if not download.empty else 0)
    gates = pd.DataFrame([
        ("P392_PHASE391_PRESENT", as_int(metric_value(phase391, "phase391_interpret_phase390_capacity_sensitivity_complete")), "Phase391 complete"),
        ("P392_TARGET_SELECTED", int(bool(target_date)), target_date),
        ("P392_DISCOVERY_OR_WAIT_RECORDED", int(sas_present == 0 or len(discovered) > 0 or bool(error_text)), f"discovered_rows={len(discovered)}; error={int(bool(error_text))}"),
        ("P392_FULL_UNIVERSE_VERIFIED_OR_PENDING", int(local_full == 1 or dry_run or sas_present == 0 or bool(error_text)), f"local_symbols={local_symbols}"),
        ("P392_NO_SECRET_MATERIAL_RECORDED", int(secret_rows == 0), f"secret_rows={secret_rows}"),
        ("P392_NO_RETEST_OR_PROMOTION", 1, "download_only"),
    ], columns=["gate_id", "passed", "evidence"])
    summary = pd.DataFrame([
        ("phase392_next_day_20260728_downloader_complete", int(gates["passed"].astype(int).all()), "Phase392 complete"),
        ("phase392_target_trade_date", target_date, "Next no-lookahead target"),
        ("phase392_pending_post_close_event_rows", len(pending_events), "Known pending rows unlocked by target"),
        ("phase392_sas_env_present", sas_present, "Supported SAS env present"),
        ("phase392_truststore_injected", TRUSTSTORE_INJECTED, "Truststore injected"),
        ("phase392_dry_run", int(dry_run), "Dry-run mode"),
        ("phase392_workers", workers, "Concurrent workers"),
        ("phase392_discovered_file_rows", len(discovered), "Discovered target file rows"),
        ("phase392_discovered_symbols", int(discovered["symbol"].nunique()) if not discovered.empty else 0, "Discovered target symbols"),
        ("phase392_download_manifest_rows", len(download), "Download manifest rows"),
        ("phase392_existing_file_rows", existing, "Existing/skipped file rows"),
        ("phase392_downloaded_file_rows", downloaded, "Downloaded file rows"),
        ("phase392_error_file_rows", errors, "Per-file error rows"),
        ("phase392_local_symbols_after", local_symbols, "Local symbols after"),
        ("phase392_local_parquet_files_after", local_files, "Local parquet files after"),
        ("phase392_local_bytes_after", local_bytes, "Local bytes after"),
        ("phase392_local_full_universe_after", local_full, "Full universe local after"),
        ("phase392_strategy_retest_executed_now", 0, "No retest"),
        ("phase392_strategy_promotion_allowed", 0, "No promotion"),
        ("phase392_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase392_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase392_next_best_action", "refresh_catalyst_event_count_after_20260728_then_rerun_frozen_retest_no_search", "Recommended next action"),
    ], columns=["metric", "value", "description"])
    outputs = {
        "summary": output_dir / "phase392_acceptance_summary.csv",
        "pending_events": output_dir / "phase392_pending_post_close_events.csv",
        "access": output_dir / "phase392_access_ledger.csv",
        "discovery": output_dir / "phase392_discovered_file_manifest.csv",
        "download": output_dir / "phase392_download_manifest.csv",
        "local_before": output_dir / "phase392_local_inventory_before.csv",
        "local_after": output_dir / "phase392_local_inventory_after.csv",
        "gates": output_dir / "phase392_gate_evaluation.csv",
        "report": output_dir / "phase392_next_day_20260728_downloader_report.md",
        "manifest": output_dir / "phase392_next_day_20260728_downloader_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    pending_events.to_csv(outputs["pending_events"], index=False)
    access.to_csv(outputs["access"], index=False)
    redact_discovery(discovered).to_csv(outputs["discovery"], index=False)
    download.to_csv(outputs["download"], index=False)
    before.to_csv(outputs["local_before"], index=False)
    after.to_csv(outputs["local_after"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text("\n".join(["# Phase392 Next-Day 2026-07-28 Downloader", "", f"Generated: {generated_utc}", "", _markdown_table(summary), "", _markdown_table(gates), ""]), encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({"phase": 392, "generated_at_utc": generated_utc, "outputs": {k: str(v) for k, v in outputs.items()}, "supported_sas_env_names_checked": SAS_ENV_NAMES, "reproducibility": reproducibility_fields(artifact_id="phase392_next_day_20260728_downloader", generated_utc=generated_utc, inputs={"phase385_eligibility": str(phase385_dir / "phase373_no_lookahead_official_catalyst_eligibility.csv")}, parameters={"target_date": target_date, "dry_run": dry_run, "max_files": max_files, "workers": workers, "secret_material_recorded": secret_rows}, outputs={k: str(v) for k, v in outputs.items()}, cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION)}, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase385-dir", type=Path, default=DEFAULT_PHASE385_DIR)
    parser.add_argument("--phase391-dir", type=Path, default=DEFAULT_PHASE391_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--file-share", default=DEFAULT_FILE_SHARE)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-files", type=int, default=0)
    parser.add_argument("--workers", type=int, default=128)
    args = parser.parse_args()
    print(json.dumps({k: str(v) for k, v in write_outputs(args.phase385_dir, args.phase391_dir, args.output_dir, args.real_root, args.file_share, args.timeout, args.dry_run, args.max_files, args.workers).items()}, indent=2))

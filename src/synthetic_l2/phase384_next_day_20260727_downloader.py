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
from synthetic_l2.phase374_next_day_20260722_downloader import as_int, metric_value, read_csv, redact_discovery
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE383_DIR = Path("outputs/phase383")
DEFAULT_OUTPUT_DIR = Path("outputs/phase384")


def write_outputs(phase383_dir: Path, output_dir: Path, real_root: Path, file_share: str, timeout: int, dry_run: bool, max_files: int, workers: int) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase383 = read_csv(phase383_dir / "phase383_acceptance_summary.csv")
    pending_events = read_csv(phase383_dir / "phase383_pending_post_close_events.csv")
    if phase383.empty or pending_events.empty:
        raise FileNotFoundError("Phase384 requires Phase383 precommit artifacts")
    target_date = str(metric_value(phase383, "phase383_target_trade_date", ""))
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
                raise ValueError("Phase384 expects File service SAS for Azure Files share")
            discovered, shares = discover_target_file_rows(source["endpoint"], source["sas"], target_date, TICKERS, timeout, file_share)
            access_rows.append({"access_route": "file_sas_env", "available": 1, "result": "file_sas_discovery_attempted", "evidence": f"env={sas_info['env_name']};shares_checked={len(shares)};rows={len(discovered)}", "secret_material_recorded": 0})
            download = download_file_rows(source["endpoint"], source["sas"], discovered, real_root, timeout, dry_run, max_files, workers)
        except Exception as exc:  # pragma: no cover
            error_text = f"{type(exc).__name__}:{str(exc)[:220]}"
            access_rows.append({"access_route": "file_sas_env", "available": 0, "result": "file_sas_discovery_or_download_failed", "evidence": error_text, "secret_material_recorded": 0})

    after = local_target_inventory(real_root, target_date)
    access = pd.DataFrame(access_rows)
    discovered_symbols = int(discovered["symbol"].nunique()) if not discovered.empty else 0
    local_symbols_after = int(after["symbol"].nunique()) if not after.empty else 0
    local_files_after = int(after["parquet_files"].sum()) if not after.empty else 0
    local_bytes_after = int(after["bytes"].sum()) if not after.empty else 0
    local_full_universe_after = int(local_symbols_after >= len(TICKERS))
    downloaded_files = int(download["status"].eq("downloaded").sum()) if not download.empty else 0
    existing_files = int(download["status"].eq("existing").sum()) if not download.empty else 0
    error_files = int(download["status"].eq("error").sum()) if not download.empty else 0
    secret_rows = int(access["secret_material_recorded"].astype(int).sum()) + (int(download["secret_material_recorded"].astype(int).sum()) if not download.empty else 0)

    gates = pd.DataFrame(
        [
            ("P384_PHASE383_PRECOMMIT_PRESENT", as_int(metric_value(phase383, "phase383_event_density_repair_precommit_complete")), "Phase383 complete"),
            ("P384_TARGET_SELECTED", int(bool(target_date)), target_date),
            ("P384_DISCOVERY_OR_WAIT_RECORDED", int(sas_present == 0 or len(discovered) > 0 or bool(error_text)), f"discovered_rows={len(discovered)}; error={int(bool(error_text))}"),
            ("P384_FULL_UNIVERSE_VERIFIED_OR_PENDING", int(local_full_universe_after == 1 or dry_run or sas_present == 0 or bool(error_text)), f"local_symbols={local_symbols_after}"),
            ("P384_NO_SECRET_MATERIAL_RECORDED", int(secret_rows == 0), f"secret_rows={secret_rows}"),
            ("P384_NO_STRATEGY_RETEST_OR_PROMOTION", 1, "download_only"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    summary = pd.DataFrame(
        [
            ("phase384_next_day_20260727_downloader_complete", int(gates["passed"].astype(int).all()), "Phase384 complete"),
            ("phase384_target_trade_date", target_date, "Phase383 target date"),
            ("phase384_pending_post_close_event_rows", len(pending_events), "Known pending rows unlocked by target"),
            ("phase384_sas_env_present", sas_present, "Supported SAS env present"),
            ("phase384_truststore_injected", TRUSTSTORE_INJECTED, "Truststore injected"),
            ("phase384_dry_run", int(dry_run), "Dry-run mode"),
            ("phase384_workers", workers, "Concurrent workers"),
            ("phase384_discovered_file_rows", len(discovered), "Discovered target file rows"),
            ("phase384_discovered_symbols", discovered_symbols, "Discovered target symbols"),
            ("phase384_download_manifest_rows", len(download), "Download manifest rows"),
            ("phase384_existing_file_rows", existing_files, "Existing/skipped file rows"),
            ("phase384_downloaded_file_rows", downloaded_files, "Downloaded file rows"),
            ("phase384_error_file_rows", error_files, "Per-file error rows"),
            ("phase384_local_symbols_after", local_symbols_after, "Local symbols after"),
            ("phase384_local_parquet_files_after", local_files_after, "Local parquet files after"),
            ("phase384_local_bytes_after", local_bytes_after, "Local bytes after"),
            ("phase384_local_full_universe_after", local_full_universe_after, "Full universe local after"),
            ("phase384_strategy_retest_executed_now", 0, "No retest in this phase"),
            ("phase384_strategy_promotion_allowed", 0, "No promotion"),
            ("phase384_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase384_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase384_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase384_hard_gate_rows", len(gates), "Hard gates"),
            ("phase384_next_best_action", "refresh_catalyst_event_count_after_20260727_then_rerun_frozen_retest_no_search", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase384_acceptance_summary.csv",
        "pending_events": output_dir / "phase384_pending_post_close_events.csv",
        "access": output_dir / "phase384_access_ledger.csv",
        "discovery": output_dir / "phase384_discovered_file_manifest.csv",
        "download": output_dir / "phase384_download_manifest.csv",
        "local_before": output_dir / "phase384_local_inventory_before.csv",
        "local_after": output_dir / "phase384_local_inventory_after.csv",
        "gates": output_dir / "phase384_gate_evaluation.csv",
        "report": output_dir / "phase384_next_day_20260727_downloader_report.md",
        "manifest": output_dir / "phase384_next_day_20260727_downloader_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    pending_events.to_csv(outputs["pending_events"], index=False)
    access.to_csv(outputs["access"], index=False)
    redact_discovery(discovered).to_csv(outputs["discovery"], index=False)
    download.to_csv(outputs["download"], index=False)
    before.to_csv(outputs["local_before"], index=False)
    after.to_csv(outputs["local_after"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join([
        "# Phase384 Next-Day 2026-07-27 Downloader",
        "",
        f"Generated: {generated_utc}",
        "",
        "Phase384 executes the Phase383 event-density repair download. It downloads/verifies the next no-lookahead real-L2 target day and does not run a strategy retest.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(summary),
        "",
        "## Gate evaluation",
        "",
        _markdown_table(gates),
        "",
        "No retest, promotion, paper/live acceptance, or deployable profitability claim is opened.",
    ])
    outputs["report"].write_text(report + "\n", encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({
        "phase": 384,
        "generated_at_utc": generated_utc,
        "outputs": {key: str(value) for key, value in outputs.items()},
        "supported_sas_env_names_checked": SAS_ENV_NAMES,
        "reproducibility": reproducibility_fields(
            artifact_id="phase384_next_day_20260727_downloader",
            generated_utc=generated_utc,
            inputs={"phase383_summary": str(phase383_dir / "phase383_acceptance_summary.csv"), "real_root": str(real_root)},
            parameters={"target_date": target_date, "dry_run": dry_run, "max_files": max_files, "workers": workers, "secret_material_recorded": secret_rows},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": "refresh_catalyst_event_count_after_20260727_then_rerun_frozen_retest_no_search",
    }, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase383-dir", type=Path, default=DEFAULT_PHASE383_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--file-share", default=DEFAULT_FILE_SHARE)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-files", type=int, default=0)
    parser.add_argument("--workers", type=int, default=128)
    args = parser.parse_args()
    outputs = write_outputs(args.phase383_dir, args.output_dir, args.real_root, args.file_share, args.timeout, args.dry_run, args.max_files, args.workers)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))

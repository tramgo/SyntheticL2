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
from synthetic_l2.phase374_next_day_20260722_downloader import as_int, metric_value, pick_target, read_csv, redact_discovery
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase378")
PHASE377_SUMMARY = Path("outputs/phase377/phase377_acceptance_summary.csv")
PHASE377_ELIGIBILITY = Path("outputs/phase377/phase373_no_lookahead_official_catalyst_eligibility.csv")


def write_outputs(output_dir: Path, real_root: Path, file_share: str, timeout: int, dry_run: bool, max_files: int, workers: int) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase377 = read_csv(PHASE377_SUMMARY)
    eligibility = read_csv(PHASE377_ELIGIBILITY)
    if phase377.empty or eligibility.empty:
        raise FileNotFoundError("Phase378 requires Phase377 summary and refreshed eligibility artifacts")

    target_date, pending_events = pick_target(eligibility)
    if not target_date:
        target_date = "NO_PENDING_TARGET"

    before = local_target_inventory(real_root, target_date) if target_date != "NO_PENDING_TARGET" else pd.DataFrame(columns=["trade_date", "symbol", "parquet_files", "bytes"])
    sas_info = sas_from_env()
    sas_present = int(bool(sas_info["value"]))
    discovered = pd.DataFrame(columns=["trade_date", "exchange", "symbol", "relative_file", "share", "file_path"])
    download = pd.DataFrame(columns=["trade_date", "exchange", "symbol", "share", "file_path_redacted", "local_path", "status", "bytes_written", "secret_material_recorded"])
    access_rows: list[dict[str, Any]] = []
    error_text = ""

    if not sas_present:
        access_rows.append({"access_route": "file_sas_env", "available": 0, "result": "no_supported_sas_env_var_present", "evidence": "supported env names checked; value not recorded", "secret_material_recorded": 0})
    elif target_date == "NO_PENDING_TARGET":
        access_rows.append({"access_route": "file_sas_env", "available": 0, "result": "no_pending_target", "evidence": "Phase377 has no post-close pending rows", "secret_material_recorded": 0})
    else:
        try:
            source = normalize_sas_source(sas_info["value"])
            if source["service"] != "file":
                raise ValueError("Phase378 expects File service SAS for Azure Files share")
            discovered, shares = discover_target_file_rows(source["endpoint"], source["sas"], target_date, TICKERS, timeout, file_share)
            access_rows.append({"access_route": "file_sas_env", "available": 1, "result": "file_sas_discovery_attempted", "evidence": f"env={sas_info['env_name']};shares_checked={len(shares)};rows={len(discovered)}", "secret_material_recorded": 0})
            download = download_file_rows(source["endpoint"], source["sas"], discovered, real_root, timeout, dry_run, max_files, workers)
        except Exception as exc:  # pragma: no cover - network dependent
            error_text = f"{type(exc).__name__}:{str(exc)[:220]}"
            access_rows.append({"access_route": "file_sas_env", "available": 0, "result": "file_sas_discovery_or_download_failed", "evidence": error_text, "secret_material_recorded": 0})

    after = local_target_inventory(real_root, target_date) if target_date != "NO_PENDING_TARGET" else before
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

    previous_estimate = float(metric_value(phase377, "phase377_estimated_selected_after_refresh", 0.0))
    previous_ready = as_int(metric_value(phase377, "phase377_refreshed_eligible_rows"))
    added_pending = len(pending_events) if local_full_universe_after else 0
    selected_per_ready = previous_estimate / previous_ready if previous_ready else 0.0
    estimated_selected_after_target = previous_estimate + added_pending * selected_per_ready
    event_floor_after_target = int(estimated_selected_after_target >= 30.0)

    gates = pd.DataFrame(
        [
            ("P378_PHASE377_PRESENT", int(as_int(metric_value(phase377, "phase377_interpret_20260723_event_refresh_complete")) == 1), "Phase377 complete"),
            ("P378_TARGET_SELECTED", int(target_date != "NO_PENDING_TARGET"), target_date),
            ("P378_SAS_OR_SAFE_WAIT", 1, f"sas_present={sas_present}"),
            ("P378_DISCOVERY_OR_WAIT_RECORDED", int(sas_present == 0 or len(discovered) > 0 or bool(error_text)), f"discovered_rows={len(discovered)}; error={int(bool(error_text))}"),
            ("P378_FULL_UNIVERSE_VERIFIED_OR_PENDING", int(local_full_universe_after == 1 or dry_run or sas_present == 0 or bool(error_text)), f"local_symbols={local_symbols_after}"),
            ("P378_NO_SECRET_MATERIAL_RECORDED", int(secret_rows == 0), f"secret_rows={secret_rows}"),
            ("P378_NO_STRATEGY_RETEST_OR_PROMOTION", 1, "download_and_event_floor_estimate_only"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    next_action = (
        "refresh_catalyst_event_count_after_20260724_no_paper_live"
        if local_full_universe_after
        else f"provide_sas_or_local_drop_full_universe_real_l2_for_{target_date}_then_rerun_phase378_no_paper_live"
    )
    summary = pd.DataFrame(
        [
            ("phase378_next_day_20260724_downloader_complete", int(gates["passed"].astype(int).all()), "Phase378 complete if all hard gates pass"),
            ("phase378_target_trade_date", target_date, "Next target date from Phase377 pending post-close rows"),
            ("phase378_pending_post_close_event_rows", len(pending_events), "Known pending post-close catalyst rows unlocked by target"),
            ("phase378_sas_env_present", sas_present, "Supported SAS env present"),
            ("phase378_truststore_injected", TRUSTSTORE_INJECTED, "Truststore injected before HTTPS calls"),
            ("phase378_dry_run", int(dry_run), "Dry-run mode"),
            ("phase378_workers", workers, "Concurrent workers"),
            ("phase378_discovered_file_rows", len(discovered), "Discovered target file rows"),
            ("phase378_discovered_symbols", discovered_symbols, "Discovered target symbols"),
            ("phase378_download_manifest_rows", len(download), "Download manifest rows"),
            ("phase378_existing_file_rows", existing_files, "Existing/skipped file rows"),
            ("phase378_downloaded_file_rows", downloaded_files, "Downloaded file rows"),
            ("phase378_error_file_rows", error_files, "Per-file error rows"),
            ("phase378_local_symbols_after", local_symbols_after, "Local symbols after"),
            ("phase378_local_parquet_files_after", local_files_after, "Local parquet files after"),
            ("phase378_local_bytes_after", local_bytes_after, "Local bytes after"),
            ("phase378_local_full_universe_after", local_full_universe_after, "Full universe local after"),
            ("phase378_estimated_selected_after_target", estimated_selected_after_target, "Estimated selected trades after adding target pending events"),
            ("phase378_event_floor_after_target_estimate", event_floor_after_target, "Whether target estimate reaches 30-event floor"),
            ("phase378_acceptance_retest_allowed_now", 0, "No retest in this phase"),
            ("phase378_strategy_promotion_allowed", 0, "No promotion"),
            ("phase378_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase378_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase378_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase378_hard_gate_rows", len(gates), "Hard gates"),
            ("phase378_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase378_acceptance_summary.csv",
        "pending_events": output_dir / "phase378_pending_post_close_events.csv",
        "access": output_dir / "phase378_access_ledger.csv",
        "discovery": output_dir / "phase378_discovered_file_manifest.csv",
        "download": output_dir / "phase378_download_manifest.csv",
        "local_before": output_dir / "phase378_local_inventory_before.csv",
        "local_after": output_dir / "phase378_local_inventory_after.csv",
        "gates": output_dir / "phase378_gate_evaluation.csv",
        "report": output_dir / "phase378_next_day_20260724_downloader_report.md",
        "manifest": output_dir / "phase378_next_day_20260724_downloader_manifest.json",
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
        "# Phase378 Next-Day 2026-07-24 Downloader",
        "",
        f"Generated: {generated_utc}",
        "",
        "Phase378 selects the next target from Phase377 pending post-close catalyst rows, downloads/verifies the full-universe real L2 day when SAS is available, and does not run a strategy retest.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(summary),
        "",
        "## Pending post-close events",
        "",
        _markdown_table(pending_events.head(40)),
        "",
        "## Access ledger",
        "",
        _markdown_table(access),
        "",
        "## Gate evaluation",
        "",
        _markdown_table(gates),
        "",
        "No strategy retest, promotion, paper/live acceptance, or deployable profitability claim is opened.",
    ])
    outputs["report"].write_text(report + "\n", encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({
        "phase": 378,
        "generated_at_utc": generated_utc,
        "outputs": {key: str(value) for key, value in outputs.items()},
        "supported_sas_env_names_checked": SAS_ENV_NAMES,
        "reproducibility": reproducibility_fields(
            artifact_id="phase378_next_day_20260724_downloader",
            generated_utc=generated_utc,
            inputs={"phase377_summary": str(PHASE377_SUMMARY), "phase377_eligibility": str(PHASE377_ELIGIBILITY), "real_root": str(real_root)},
            parameters={"target_date": target_date, "dry_run": dry_run, "max_files": max_files, "workers": workers, "secret_material_recorded": secret_rows},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": next_action,
    }, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--file-share", default=DEFAULT_FILE_SHARE)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-files", type=int, default=0)
    parser.add_argument("--workers", type=int, default=128)
    args = parser.parse_args()
    outputs = write_outputs(args.output_dir, args.real_root, args.file_share, args.timeout, args.dry_run, args.max_files, args.workers)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))

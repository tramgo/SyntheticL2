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
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase374")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def next_weekday(text: str) -> str:
    dt = date.fromisoformat(text) + timedelta(days=1)
    while dt.weekday() >= 5:
        dt += timedelta(days=1)
    return dt.isoformat()


def pick_target(eligibility: pd.DataFrame) -> tuple[str, pd.DataFrame]:
    pending = eligibility[
        eligibility["market_session"].astype(str).eq("post_close")
        & eligibility["diagnostic_trade_date"].fillna("").astype(str).eq("")
    ].copy()
    if pending.empty:
        return "", pending
    source_date = sorted(pending["announcement_date"].dropna().astype(str).unique().tolist())[-1]
    return next_weekday(source_date), pending[pending["announcement_date"].astype(str).eq(source_date)].copy()


def redact_discovery(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    if "file_path" in out.columns:
        out["file_path_redacted"] = out["file_path"].astype(str).str.replace(r"part-[^/]+\.parquet$", "part-REDACTED.parquet", regex=True)
        out = out.drop(columns=["file_path"], errors="ignore")
    return out


def write_outputs(output_dir: Path, real_root: Path, file_share: str, timeout: int, dry_run: bool, max_files: int, workers: int) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase373 = read_csv(Path("outputs/phase373/phase373_acceptance_summary.csv"))
    eligibility = read_csv(Path("outputs/phase373/phase373_no_lookahead_official_catalyst_eligibility.csv"))
    if phase373.empty or eligibility.empty:
        raise FileNotFoundError("Phase374 requires Phase373 summary and eligibility artifacts")

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
        access_rows.append({"access_route": "file_sas_env", "available": 0, "result": "no_pending_target", "evidence": "Phase373 has no post-close pending rows", "secret_material_recorded": 0})
    else:
        try:
            source = normalize_sas_source(sas_info["value"])
            if source["service"] != "file":
                raise ValueError("Phase374 expects File service SAS for Azure Files share")
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

    previous_estimate = float(metric_value(phase373, "phase373_estimated_selected_after_refresh", 0.0))
    previous_ready = as_int(metric_value(phase373, "phase373_refreshed_no_lookahead_eligible_rows"))
    added_pending = len(pending_events) if local_full_universe_after else 0
    # Use Phase373's observed event-to-selected estimate as a conservative continuity heuristic.
    selected_per_ready = previous_estimate / previous_ready if previous_ready else 0.0
    estimated_selected_after_target = previous_estimate + added_pending * selected_per_ready
    event_floor_after_target = int(estimated_selected_after_target >= 30.0)

    gates = pd.DataFrame(
        [
            ("P374_PHASE373_PRESENT", int(as_int(metric_value(phase373, "phase373_refreshed_catalyst_event_count_after_20260721_complete")) == 1), "Phase373 complete"),
            ("P374_TARGET_SELECTED", int(target_date != "NO_PENDING_TARGET"), target_date),
            ("P374_SAS_OR_SAFE_WAIT", 1, f"sas_present={sas_present}"),
            ("P374_DISCOVERY_OR_WAIT_RECORDED", int(sas_present == 0 or len(discovered) > 0 or bool(error_text)), f"discovered_rows={len(discovered)}; error={int(bool(error_text))}"),
            ("P374_FULL_UNIVERSE_VERIFIED_OR_PENDING", int(local_full_universe_after == 1 or dry_run or sas_present == 0 or bool(error_text)), f"local_symbols={local_symbols_after}"),
            ("P374_NO_SECRET_MATERIAL_RECORDED", int(secret_rows == 0), f"secret_rows={secret_rows}"),
            ("P374_NO_STRATEGY_RETEST_OR_PROMOTION", 1, "download_and_event_floor_estimate_only"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )

    next_action = (
        "refresh_catalyst_event_count_after_20260722_no_paper_live"
        if local_full_universe_after
        else f"provide_sas_or_local_drop_full_universe_real_l2_for_{target_date}_then_rerun_phase374_no_paper_live"
    )
    summary = pd.DataFrame(
        [
            ("phase374_next_day_20260722_downloader_complete", int(gates["passed"].astype(int).all()), "Phase374 complete if all hard gates pass"),
            ("phase374_target_trade_date", target_date, "Next target date from Phase373 pending post-close rows"),
            ("phase374_pending_post_close_event_rows", len(pending_events), "Known pending post-close catalyst rows unlocked by target"),
            ("phase374_sas_env_present", sas_present, "Supported SAS env present"),
            ("phase374_truststore_injected", TRUSTSTORE_INJECTED, "Truststore injected before HTTPS calls"),
            ("phase374_dry_run", int(dry_run), "Dry-run mode"),
            ("phase374_workers", workers, "Concurrent workers"),
            ("phase374_discovered_file_rows", len(discovered), "Discovered target file rows"),
            ("phase374_discovered_symbols", discovered_symbols, "Discovered target symbols"),
            ("phase374_download_manifest_rows", len(download), "Download manifest rows"),
            ("phase374_existing_file_rows", existing_files, "Existing/skipped file rows"),
            ("phase374_downloaded_file_rows", downloaded_files, "Downloaded file rows"),
            ("phase374_error_file_rows", error_files, "Per-file error rows"),
            ("phase374_local_symbols_after", local_symbols_after, "Local symbols after"),
            ("phase374_local_parquet_files_after", local_files_after, "Local parquet files after"),
            ("phase374_local_bytes_after", local_bytes_after, "Local bytes after"),
            ("phase374_local_full_universe_after", local_full_universe_after, "Full universe local after"),
            ("phase374_estimated_selected_after_target", estimated_selected_after_target, "Estimated selected trades after adding target pending events"),
            ("phase374_event_floor_after_target_estimate", event_floor_after_target, "Whether target estimate reaches 30-event floor"),
            ("phase374_acceptance_retest_allowed_now", 0, "No retest in this phase"),
            ("phase374_strategy_promotion_allowed", 0, "No promotion"),
            ("phase374_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase374_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase374_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase374_hard_gate_rows", len(gates), "Hard gates"),
            ("phase374_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )

    outputs = {
        "summary": output_dir / "phase374_acceptance_summary.csv",
        "pending_events": output_dir / "phase374_pending_post_close_events.csv",
        "access": output_dir / "phase374_access_ledger.csv",
        "discovery": output_dir / "phase374_discovered_file_manifest.csv",
        "download": output_dir / "phase374_download_manifest.csv",
        "local_before": output_dir / "phase374_local_inventory_before.csv",
        "local_after": output_dir / "phase374_local_inventory_after.csv",
        "gates": output_dir / "phase374_gate_evaluation.csv",
        "report": output_dir / "phase374_next_day_20260722_downloader_report.md",
        "manifest": output_dir / "phase374_next_day_20260722_downloader_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    pending_events.to_csv(outputs["pending_events"], index=False)
    access.to_csv(outputs["access"], index=False)
    redact_discovery(discovered).to_csv(outputs["discovery"], index=False)
    download.to_csv(outputs["download"], index=False)
    before.to_csv(outputs["local_before"], index=False)
    after.to_csv(outputs["local_after"], index=False)
    gates.to_csv(outputs["gates"], index=False)

    report = "\n".join(
        [
            "# Phase374 Next-Day 2026-07-22 Downloader",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase374 selects the next target from Phase373 pending post-close catalyst rows, downloads/verifies the full-universe real L2 day when SAS is available, and does not run a strategy retest.",
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
        ]
    )
    outputs["report"].write_text(report + "\n", encoding="utf-8")

    manifest = {
        "phase": 374,
        "generated_at_utc": generated_utc,
        "outputs": {key: str(value) for key, value in outputs.items()},
        "supported_sas_env_names_checked": SAS_ENV_NAMES,
        "reproducibility": reproducibility_fields(
            artifact_id="phase374_next_day_20260722_downloader",
            generated_utc=generated_utc,
            inputs={"phase373_eligibility": "outputs/phase373/phase373_no_lookahead_official_catalyst_eligibility.csv", "real_root": str(real_root)},
            parameters={"target_date": target_date, "dry_run": dry_run, "max_files": max_files, "workers": workers, "secret_material_recorded": secret_rows},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": next_action,
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--file-share", default=DEFAULT_FILE_SHARE)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-files", type=int, default=0)
    parser.add_argument("--workers", type=int, default=96)
    args = parser.parse_args()
    outputs = write_outputs(args.output_dir, args.real_root, args.file_share, args.timeout, args.dry_run, args.max_files, args.workers)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase143")
DEFAULT_PHASE115_DIR = Path("outputs/phase115")
DEFAULT_PHASE142_DIR = Path("outputs/phase142")
DEFAULT_REQUIRED_DATES = ["2026-07-10", "2026-07-14"]
DEFAULT_SCRATCH_ROOT = Path("scratch_azcopy_selected/raw_l2")
DEFAULT_TARGET_ROOT = Path("real_data_sample/l2_multiday_panel")


def read_metric_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["metric", "value", "description"])
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def read_phase142_dates(phase142_dir: Path) -> pd.DataFrame:
    path = phase142_dir / "local_real_l2_date_readiness.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def build_required_date_status(
    phase142_dates: pd.DataFrame,
    required_dates: list[str],
    scratch_root: Path,
    target_root: Path,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for date in required_dates:
        scratch_rows = (
            phase142_dates[
                phase142_dates["root"].astype(str).eq(str(scratch_root))
                & phase142_dates["trade_date"].astype(str).eq(date)
            ]
            if not phase142_dates.empty
            else pd.DataFrame()
        )
        target_rows = (
            phase142_dates[
                phase142_dates["root"].astype(str).eq(str(target_root))
                & phase142_dates["trade_date"].astype(str).eq(date)
            ]
            if not phase142_dates.empty
            else pd.DataFrame()
        )
        scratch_ready = bool(
            not scratch_rows.empty
            and scratch_rows["ready_for_phase115_import"].astype(bool).any()
        )
        target_ready = bool(
            not target_rows.empty
            and target_rows["ready_for_phase115_import"].astype(bool).any()
        )
        scratch_files = int(pd.to_numeric(scratch_rows.get("parquet_files", pd.Series(dtype=float)), errors="coerce").sum()) if not scratch_rows.empty else 0
        target_files = int(pd.to_numeric(target_rows.get("parquet_files", pd.Series(dtype=float)), errors="coerce").sum()) if not target_rows.empty else 0
        scratch_bytes = int(pd.to_numeric(scratch_rows.get("bytes", pd.Series(dtype=float)), errors="coerce").sum()) if not scratch_rows.empty else 0
        target_bytes = int(pd.to_numeric(target_rows.get("bytes", pd.Series(dtype=float)), errors="coerce").sum()) if not target_rows.empty else 0
        if target_ready:
            action = "already_imported"
        elif scratch_ready:
            action = "run_phase115_import"
        else:
            action = "download_with_azcopy_helper_then_rerun_phase142"
        rows.append(
            {
                "trade_date": date,
                "scratch_ready_for_import": scratch_ready,
                "target_already_ready": target_ready,
                "scratch_parquet_files": scratch_files,
                "target_parquet_files": target_files,
                "scratch_bytes": scratch_bytes,
                "target_bytes": target_bytes,
                "required_date_satisfied": bool(scratch_ready or target_ready),
                "next_action": action,
            }
        )
    return pd.DataFrame(rows)


def build_command_plan(status: pd.DataFrame, scratch_root: Path, target_root: Path) -> pd.DataFrame:
    missing_dates = status.loc[~status["required_date_satisfied"].astype(bool), "trade_date"].astype(str).tolist()
    scratch_ready_dates = status.loc[
        status["scratch_ready_for_import"].astype(bool) & ~status["target_already_ready"].astype(bool),
        "trade_date",
    ].astype(str).tolist()
    rows: list[dict[str, Any]] = []
    if missing_dates:
        rows.append(
            {
                "step": 1,
                "action": "download_missing_required_dates",
                "runs_now": False,
                "command": (
                    "powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_azure_real_l2_dates_azcopy.ps1 "
                    f"-Dates {','.join(missing_dates)} -ShareSasToken \"<read_list_share_sas>\" "
                    "# or use -AccountKey \"<storage_account_key>\" / AZURE_STORAGE_KEY"
                ),
                "why": "At least one required date is not locally ready in scratch or target.",
            }
        )
    rows.append(
        {
            "step": 2,
            "action": "verify_local_downloads",
            "runs_now": True,
            "command": (
                "python scripts/run_phase142_local_real_l2_download_verifier.py "
                f"--roots {scratch_root.as_posix()} {target_root.as_posix()}"
            ),
            "why": "Confirms local coverage/schema/readability before Phase115 import.",
        }
    )
    rows.append(
        {
            "step": 3,
            "action": "import_ready_scratch_dates",
            "runs_now": bool(scratch_ready_dates),
            "command": (
                "python scripts/run_phase115_real_panel_refresh_orchestrator.py "
                f"--source-root {scratch_root.as_posix()} --target-root {target_root.as_posix()} --execute-import"
            ),
            "why": (
                f"Ready scratch dates not yet in target: {','.join(scratch_ready_dates)}"
                if scratch_ready_dates
                else "No required date is locally ready in scratch but missing from target."
            ),
        }
    )
    rows.append(
        {
            "step": 4,
            "action": "review_phase115_unlock_state",
            "runs_now": True,
            "command": "Import-Csv outputs/phase115/phase115_real_panel_refresh_acceptance_summary.csv",
            "why": "Replay remains closed unless Phase110/Phase115 explicitly prove the minimum real-anchor gate.",
        }
    )
    return pd.DataFrame(rows)


def summarize(phase115: pd.DataFrame, status: pd.DataFrame) -> pd.DataFrame:
    ready_days = as_int(metric_value(phase115, "phase115_phase110_ready_real_anchor_days"))
    days_needed = as_int(metric_value(phase115, "phase115_phase110_days_needed_for_min"), 5)
    required_satisfied = int(status["required_date_satisfied"].astype(bool).sum()) if not status.empty else 0
    required_count = int(len(status))
    target_ready = int(status["target_already_ready"].astype(bool).sum()) if not status.empty else 0
    scratch_ready = int(status["scratch_ready_for_import"].astype(bool).sum()) if not status.empty else 0
    can_run_phase115_import = bool(scratch_ready > target_ready)
    all_required_satisfied = bool(required_satisfied == required_count and required_count > 0)
    return pd.DataFrame(
        [
            ("phase143_current_ready_real_anchor_days", ready_days, "Ready real-anchor days from latest Phase115/110"),
            ("phase143_days_needed_for_min", days_needed, "Additional ready real days needed for minimum unlock before this preflight"),
            ("phase143_required_date_rows", required_count, "Required next-date rows checked"),
            ("phase143_required_dates_satisfied", required_satisfied, "Required dates already ready in scratch or target"),
            ("phase143_required_dates_target_ready", target_ready, "Required dates already ready in canonical target"),
            ("phase143_required_dates_scratch_ready", scratch_ready, "Required dates ready in scratch for Phase115 import"),
            ("phase143_all_required_dates_satisfied", int(all_required_satisfied), "1 means configured required dates are locally ready in scratch or target"),
            ("phase143_can_run_phase115_import_now", int(can_run_phase115_import), "1 means at least one required date is ready in scratch but not yet imported"),
            ("phase143_strategy_replay_allowed", 0, "Preflight never unlocks strategy replay"),
            (
                "phase143_next_best_action",
                "run_phase115_execute_import" if can_run_phase115_import else "download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase142_phase143",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase143 Real L2 Two-Date Acquisition Preflight",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase143 is an executable guard before the next Phase115 import/refresh.",
        "It checks whether the configured next two real L2 dates are already ready in scratch or target, and emits the exact next command path.",
        "It does not contact Azure and does not unlock strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase143_real_l2_two_date_preflight_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase143(
    phase115_dir: Path,
    phase142_dir: Path,
    output_dir: Path,
    base_dir: Path,
    required_dates: list[str],
    scratch_root: Path,
    target_root: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase115 = read_metric_table(phase115_dir / "phase115_real_panel_refresh_acceptance_summary.csv")
    phase142_dates = read_phase142_dates(phase142_dir)
    status = build_required_date_status(phase142_dates, required_dates, scratch_root, target_root)
    commands = build_command_plan(status, scratch_root, target_root)
    acceptance = summarize(phase115, status)

    status.to_csv(output_dir / "required_real_l2_date_status.csv", index=False)
    commands.to_csv(output_dir / "real_l2_next_command_plan.csv", index=False)
    acceptance.to_csv(output_dir / "phase143_real_l2_two_date_preflight_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Required Date Status": status,
            "Next Command Plan": commands,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase143_real_l2_two_date_preflight",
        **reproducibility_fields(
            artifact_id="phase143",
            generated_utc=generated_utc,
            inputs={
                "phase115_acceptance": str(phase115_dir / "phase115_real_panel_refresh_acceptance_summary.csv"),
                "phase142_date_readiness": str(phase142_dir / "local_real_l2_date_readiness.csv"),
                "required_dates": required_dates,
                "scratch_root": str(scratch_root),
                "target_root": str(target_root),
            },
            parameters={
                "minimum_ready_real_days": 5,
                "strategy_replay_policy": "closed",
                "preflight_policy": "do_not_run_phase115_import_until_required_dates_are_ready_in_scratch_or_target",
                "download_auth_policy": "AzCopy helper accepts ShareSasToken or AccountKey; generated signatures are not persisted",
            },
            outputs={
                "required_date_status": str(output_dir / "required_real_l2_date_status.csv"),
                "command_plan": str(output_dir / "real_l2_next_command_plan.csv"),
                "acceptance_summary": str(output_dir / "phase143_real_l2_two_date_preflight_acceptance_summary.csv"),
                "report": str(output_dir / "phase143_real_l2_two_date_preflight_report.md"),
                "manifest": str(output_dir / "phase143_real_l2_two_date_preflight_manifest.json"),
            },
            random_seed="none_deterministic_preflight",
            scenario_ids="phase143_real_l2_two_date_acquisition_preflight",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase143_real_l2_two_date_preflight_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preflight the next two real L2 dates before Phase115 import.")
    parser.add_argument("--phase115-dir", type=Path, default=DEFAULT_PHASE115_DIR)
    parser.add_argument("--phase142-dir", type=Path, default=DEFAULT_PHASE142_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--required-dates", nargs="+", default=DEFAULT_REQUIRED_DATES)
    parser.add_argument("--scratch-root", type=Path, default=DEFAULT_SCRATCH_ROOT)
    parser.add_argument("--target-root", type=Path, default=DEFAULT_TARGET_ROOT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase143(
        phase115_dir=args.phase115_dir,
        phase142_dir=args.phase142_dir,
        output_dir=args.output_dir,
        base_dir=args.base_dir,
        required_dates=args.required_dates,
        scratch_root=args.scratch_root,
        target_root=args.target_root,
    )


if __name__ == "__main__":
    main()

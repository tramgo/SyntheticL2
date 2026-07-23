from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase115_real_panel_refresh_orchestrator import (
    DEFAULT_EXCHANGE,
    DEFAULT_MAX_FILES_PER_SYMBOL,
    DEFAULT_REAL_ROOT,
    run_phase115,
)
from synthetic_l2.phase117_real_anchor_acquisition_work_order import run_phase117
from synthetic_l2.phase137_post_phase132_real_anchor_restart import run_phase137
from synthetic_l2.phase142_local_real_l2_download_verifier import run_phase142
from synthetic_l2.phase143_real_l2_two_date_preflight import run_phase143
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase145")
DEFAULT_SCRATCH_ROOT = Path("scratch_azcopy_selected/raw_l2")
DEFAULT_TARGET_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_PHASE142_DIR = Path("outputs/phase142")
DEFAULT_PHASE143_DIR = Path("outputs/phase143")
DEFAULT_PHASE115_DIR = Path("outputs/phase115")
DEFAULT_PHASE117_DIR = Path("outputs/phase117")
DEFAULT_PHASE137_DIR = Path("outputs/phase137")
DEFAULT_PHASE116_DIR = Path("outputs/phase116")
DEFAULT_PHASE132_DIR = Path("outputs/phase132")
DEFAULT_REQUIRED_DATES = ["2026-07-10", "2026-07-14"]


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    if not path.exists():
        return default
    frame = pd.read_csv(path)
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


def run_step(step_rows: list[dict[str, Any]], step_id: str, description: str, fn: Any, *args: Any, **kwargs: Any) -> None:
    started = datetime.now(timezone.utc)
    try:
        fn(*args, **kwargs)
        status = "completed"
        error = ""
    except Exception as exc:
        status = "failed"
        error = repr(exc)
    ended = datetime.now(timezone.utc)
    step_rows.append(
        {
            "step_id": step_id,
            "description": description,
            "status": status,
            "started_utc": started.isoformat(),
            "ended_utc": ended.isoformat(),
            "elapsed_seconds": (ended - started).total_seconds(),
            "error": error,
        }
    )
    if status == "failed":
        raise RuntimeError(f"{step_id} failed: {error}")


def phase143_can_import(phase143_dir: Path) -> bool:
    return bool(
        as_int(
            metric_value(
                phase143_dir / "phase143_real_l2_two_date_preflight_acceptance_summary.csv",
                "phase143_can_run_phase115_import_now",
                0,
            )
        )
    )


def summarize(
    output_dir: Path,
    step_ledger: pd.DataFrame,
    phase115_dir: Path,
    phase142_dir: Path,
    phase143_dir: Path,
    phase137_dir: Path,
    import_executed: bool,
) -> pd.DataFrame:
    ready_days = as_int(metric_value(phase115_dir / "phase115_real_panel_refresh_acceptance_summary.csv", "phase115_phase110_ready_real_anchor_days", 0))
    days_needed = as_int(metric_value(phase115_dir / "phase115_real_panel_refresh_acceptance_summary.csv", "phase115_phase110_days_needed_for_min", 5))
    replay_allowed = as_int(metric_value(phase115_dir / "phase115_real_panel_refresh_acceptance_summary.csv", "phase115_replay_unlock_allowed", 0))
    phase142_ready_rows = as_int(metric_value(phase142_dir / "phase142_local_real_l2_download_verifier_acceptance_summary.csv", "phase142_ready_date_rows", 0))
    required_satisfied = as_int(metric_value(phase143_dir / "phase143_real_l2_two_date_preflight_acceptance_summary.csv", "phase143_required_dates_satisfied", 0))
    required_rows = as_int(metric_value(phase143_dir / "phase143_real_l2_two_date_preflight_acceptance_summary.csv", "phase143_required_date_rows", 0))
    phase137_days_needed = as_int(metric_value(phase137_dir / "phase137_post_phase132_real_anchor_restart_acceptance_summary.csv", "phase137_additional_days_needed_for_min", days_needed))
    return pd.DataFrame(
        [
            ("phase145_steps", int(len(step_ledger)), "Post-download refresh steps attempted"),
            ("phase145_failed_steps", int((step_ledger["status"].astype(str) != "completed").sum()) if not step_ledger.empty else 0, "Post-download refresh steps failed"),
            ("phase145_phase115_import_executed", int(import_executed), "1 means Phase115 import/refresh was run because Phase143 allowed it"),
            ("phase145_phase142_ready_date_rows", phase142_ready_rows, "Root/date rows ready in Phase142 local verifier"),
            ("phase145_phase143_required_date_rows", required_rows, "Configured required dates checked by Phase143"),
            ("phase145_phase143_required_dates_satisfied", required_satisfied, "Configured required dates ready in scratch or target"),
            ("phase145_ready_real_anchor_days", ready_days, "Ready real-anchor days after this orchestrator"),
            ("phase145_days_needed_for_min", days_needed, "Additional ready real-anchor days needed for minimum unlock"),
            ("phase145_phase137_days_needed_for_min", phase137_days_needed, "Phase137 refreshed additional-days-needed metric"),
            ("phase145_replay_unlock_allowed", replay_allowed, "Replay unlock flag remains inherited from Phase115"),
            (
                "phase145_next_best_action",
                "run_phase115_execute_import" if phase143_can_import(phase143_dir) else "download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase145",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase145 Real L2 Post-download Refresh Orchestrator",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase145 stitches the post-download real-anchor workflow together.",
        "It always refreshes Phase142 and Phase143, runs Phase115 only when Phase143 says a required date is locally ready for import, and then refreshes Phase117/137 handoff evidence.",
        "It does not contact Azure and does not unlock strategy replay by itself.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase145_real_l2_post_download_refresh_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase145(
    output_dir: Path,
    base_dir: Path,
    scratch_root: Path,
    target_root: Path,
    required_dates: list[str],
    phase142_dir: Path,
    phase143_dir: Path,
    phase115_dir: Path,
    phase117_dir: Path,
    phase137_dir: Path,
    phase116_dir: Path,
    phase132_dir: Path,
    max_files_per_symbol: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    step_rows: list[dict[str, Any]] = []

    run_step(
        step_rows,
        "P145_PHASE142_VERIFY_LOCAL_DOWNLOADS_INITIAL",
        "Verify scratch and canonical real L2 date partitions.",
        run_phase142,
        [scratch_root, target_root],
        phase142_dir,
        base_dir,
        DEFAULT_EXCHANGE,
    )
    run_step(
        step_rows,
        "P145_PHASE143_PREFLIGHT_REQUIRED_DATES_INITIAL",
        "Check whether configured required dates are locally ready.",
        run_phase143,
        phase115_dir,
        phase142_dir,
        phase143_dir,
        base_dir,
        required_dates,
        scratch_root,
        target_root,
    )

    import_executed = phase143_can_import(phase143_dir)
    if import_executed:
        run_step(
            step_rows,
            "P145_PHASE115_IMPORT_AND_REFRESH",
            "Import ready scratch dates into canonical panel and refresh Phase96/110 gates.",
            run_phase115,
            scratch_root,
            target_root,
            DEFAULT_REAL_ROOT,
            [Path("raw_l2"), Path("scratch_l2_sample_20260710_HDFCBANK")],
            phase115_dir,
            base_dir,
            True,
            False,
            DEFAULT_EXCHANGE,
            max_files_per_symbol,
        )
        run_step(
            step_rows,
            "P145_PHASE142_VERIFY_LOCAL_DOWNLOADS_AFTER_IMPORT",
            "Refresh local verifier after Phase115 import.",
            run_phase142,
            [scratch_root, target_root],
            phase142_dir,
            base_dir,
            DEFAULT_EXCHANGE,
        )
        run_step(
            step_rows,
            "P145_PHASE143_PREFLIGHT_REQUIRED_DATES_AFTER_IMPORT",
            "Refresh required-date preflight after import.",
            run_phase143,
            phase115_dir,
            phase142_dir,
            phase143_dir,
            base_dir,
            required_dates,
            scratch_root,
            target_root,
        )

    run_step(
        step_rows,
        "P145_PHASE117_REFRESH_WORK_ORDER",
        "Refresh real-anchor acquisition work order.",
        run_phase117,
        base_dir,
        phase117_dir,
        Path("real_data_sample"),
        phase115_dir,
        phase116_dir,
        [Path("raw_l2"), Path("scratch_l2_sample_20260710_HDFCBANK"), scratch_root],
    )
    run_step(
        step_rows,
        "P145_PHASE137_REFRESH_RESTART_HANDOFF",
        "Refresh post-Phase132 real-anchor restart handoff.",
        run_phase137,
        base_dir,
        phase137_dir,
        phase132_dir,
        phase117_dir,
        phase116_dir,
        phase115_dir,
    )

    steps = pd.DataFrame(step_rows)
    acceptance = summarize(output_dir, steps, phase115_dir, phase142_dir, phase143_dir, phase137_dir, import_executed)
    steps.to_csv(output_dir / "phase145_refresh_step_ledger.csv", index=False)
    acceptance.to_csv(output_dir / "phase145_real_l2_post_download_refresh_acceptance_summary.csv", index=False)
    write_report(output_dir, {"Acceptance Summary": acceptance, "Step Ledger": steps})

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase145_real_l2_post_download_refresh",
        **reproducibility_fields(
            artifact_id="phase145",
            generated_utc=generated_utc,
            inputs={
                "scratch_root": str(scratch_root),
                "target_root": str(target_root),
                "required_dates": required_dates,
                "phase142_dir": str(phase142_dir),
                "phase143_dir": str(phase143_dir),
                "phase115_dir": str(phase115_dir),
                "phase117_dir": str(phase117_dir),
                "phase137_dir": str(phase137_dir),
            },
            parameters={
                "conditional_import": "run_phase115_only_when_phase143_can_run_phase115_import_now_equals_1",
                "max_files_per_symbol": max_files_per_symbol,
                "strategy_replay_policy": "closed_until_phase115_phase110_unlock",
            },
            outputs={
                "step_ledger": str(output_dir / "phase145_refresh_step_ledger.csv"),
                "acceptance_summary": str(output_dir / "phase145_real_l2_post_download_refresh_acceptance_summary.csv"),
                "report": str(output_dir / "phase145_real_l2_post_download_refresh_report.md"),
                "manifest": str(output_dir / "phase145_real_l2_post_download_refresh_manifest.json"),
            },
            random_seed="none_deterministic_post_download_refresh",
            scenario_ids="phase145_real_l2_post_download_refresh",
            cost_model_version="not_applicable",
            latency_model_version="phase115_phase110_real_anchor_gate",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase145_real_l2_post_download_refresh_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run post-download real L2 verification/import/handoff refresh.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--scratch-root", type=Path, default=DEFAULT_SCRATCH_ROOT)
    parser.add_argument("--target-root", type=Path, default=DEFAULT_TARGET_ROOT)
    parser.add_argument("--required-dates", nargs="+", default=DEFAULT_REQUIRED_DATES)
    parser.add_argument("--phase142-dir", type=Path, default=DEFAULT_PHASE142_DIR)
    parser.add_argument("--phase143-dir", type=Path, default=DEFAULT_PHASE143_DIR)
    parser.add_argument("--phase115-dir", type=Path, default=DEFAULT_PHASE115_DIR)
    parser.add_argument("--phase117-dir", type=Path, default=DEFAULT_PHASE117_DIR)
    parser.add_argument("--phase137-dir", type=Path, default=DEFAULT_PHASE137_DIR)
    parser.add_argument("--phase116-dir", type=Path, default=DEFAULT_PHASE116_DIR)
    parser.add_argument("--phase132-dir", type=Path, default=DEFAULT_PHASE132_DIR)
    parser.add_argument("--max-files-per-symbol", type=int, default=DEFAULT_MAX_FILES_PER_SYMBOL)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase145(
        output_dir=args.output_dir,
        base_dir=args.base_dir,
        scratch_root=args.scratch_root,
        target_root=args.target_root,
        required_dates=args.required_dates,
        phase142_dir=args.phase142_dir,
        phase143_dir=args.phase143_dir,
        phase115_dir=args.phase115_dir,
        phase117_dir=args.phase117_dir,
        phase137_dir=args.phase137_dir,
        phase116_dir=args.phase116_dir,
        phase132_dir=args.phase132_dir,
        max_files_per_symbol=args.max_files_per_symbol,
    )


if __name__ == "__main__":
    main()

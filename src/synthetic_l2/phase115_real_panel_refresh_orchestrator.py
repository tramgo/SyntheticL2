from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase96_real_anchor_panel_builder import DEFAULT_MAX_FILES_PER_SYMBOL, DEFAULT_PHASE95_DIR, run_phase96
from synthetic_l2.phase110_multiday_replay_unlock_gate import DEFAULT_PHASE109_DIR, run_phase110
from synthetic_l2.phase111_real_anchor_ingest_discovery import DEFAULT_CANDIDATE_ROOTS, run_phase111
from synthetic_l2.phase113_real_l2_dropzone_importer import DEFAULT_EXCHANGE, DEFAULT_SOURCE_ROOT, DEFAULT_TARGET_ROOT, run_phase113
from synthetic_l2.phase114_dropzone_import_integrity_verifier import run_phase114
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase115")
DEFAULT_REAL_ROOT = Path("real_data_sample")


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


def summarize(output_dir: Path, steps: pd.DataFrame, execute_import: bool) -> pd.DataFrame:
    sub = output_dir / "subruns"
    phase111_final = sub / "phase111_final" / "phase111_real_anchor_ingest_acceptance_summary.csv"
    phase113 = sub / "phase113" / "phase113_dropzone_import_acceptance_summary.csv"
    phase114 = sub / "phase114" / "phase114_dropzone_import_integrity_acceptance_summary.csv"
    phase96 = sub / "phase96" / "real_anchor_panel_builder_acceptance_summary.csv"
    phase110 = sub / "phase110" / "phase110_multiday_replay_unlock_acceptance_summary.csv"
    replay_allowed = int(float(metric_value(phase110, "phase110_replay_unlock_allowed", 0)))
    ready_days = int(float(metric_value(phase110, "phase110_ready_real_anchor_days", 0)))
    days_needed = int(float(metric_value(phase110, "phase110_days_needed_for_min", 5)))
    return pd.DataFrame(
        [
            ("phase115_steps", int(len(steps)), "Refresh orchestration steps executed"),
            ("phase115_failed_steps", int((steps["status"].astype(str) != "completed").sum()), "Refresh orchestration steps failed"),
            ("phase115_execute_import", int(execute_import), "1 means Phase113 copied files into the drop-zone"),
            ("phase115_phase111_additional_real_dates_found", metric_value(phase111_final, "phase111_additional_real_dates_found", "missing"), "Final Phase111 additional-date discovery flag"),
            ("phase115_phase113_copied_files", metric_value(phase113, "phase113_copied_files", "missing"), "Files copied by Phase113"),
            ("phase115_phase114_dry_run_integrity_ready", metric_value(phase114, "phase114_dry_run_integrity_ready", "missing"), "Dry-run integrity-ready flag"),
            ("phase115_phase114_executed_import_integrity_pass", metric_value(phase114, "phase114_executed_import_integrity_pass", "missing"), "Executed import integrity pass flag"),
            ("phase115_phase96_ready_anchor_days", metric_value(phase96, "phase96_ready_anchor_days", "missing"), "Ready real anchor days after refresh"),
            ("phase115_phase110_ready_real_anchor_days", ready_days, "Ready real anchor days in replay unlock gate"),
            ("phase115_phase110_days_needed_for_min", days_needed, "Additional ready days needed for minimum unlock"),
            ("phase115_replay_unlock_allowed", replay_allowed, "1 means strategy replay may reopen"),
            ("phase115_strategy_replay_allowed", replay_allowed, "Compatibility alias for replay unlock decision"),
            ("phase115_recommend_next_action", "collect_or_import_more_real_l2_days_then_run_phase115_with_execute_import", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase115 Real Panel Refresh Orchestrator",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase115 runs the real-panel refresh chain in one command: discovery, import planning/copy, integrity, Phase96 readiness, Phase110 replay unlock, and final discovery.",
        "By default it is dry-run safe and writes subrun outputs under outputs/phase115/subruns.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase115_real_panel_refresh_orchestrator_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase115(
    source_root: Path,
    target_root: Path,
    real_root: Path,
    candidate_roots: list[Path],
    output_dir: Path,
    base_dir: Path,
    execute_import: bool,
    overwrite: bool,
    default_exchange: str,
    max_files_per_symbol: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    sub = output_dir / "subruns"
    sub.mkdir(parents=True, exist_ok=True)
    step_rows: list[dict[str, Any]] = []

    run_step(
        step_rows,
        "P115_PHASE111_INITIAL_DISCOVERY",
        "Discover candidate real panels before import.",
        run_phase111,
        candidate_roots,
        Path("outputs/phase96"),
        Path("outputs/phase110"),
        sub / "phase111_initial",
        base_dir,
    )
    run_step(
        step_rows,
        "P115_PHASE113_IMPORT_PLAN_OR_EXECUTE",
        "Create or execute drop-zone import plan.",
        run_phase113,
        source_root,
        target_root,
        sub / "phase113",
        base_dir,
        default_exchange,
        execute_import,
        overwrite,
    )
    run_step(
        step_rows,
        "P115_PHASE114_IMPORT_INTEGRITY",
        "Verify drop-zone import integrity or dry-run readiness.",
        run_phase114,
        sub / "phase113",
        sub / "phase114",
        base_dir,
    )
    run_step(
        step_rows,
        "P115_PHASE96_PANEL_READINESS",
        "Rebuild real anchor panel readiness after import step.",
        run_phase96,
        real_root,
        DEFAULT_PHASE95_DIR,
        sub / "phase96",
        base_dir,
        max_files_per_symbol,
    )
    run_step(
        step_rows,
        "P115_PHASE110_REPLAY_UNLOCK_GATE",
        "Re-evaluate replay unlock gate after readiness refresh.",
        run_phase110,
        sub / "phase96",
        DEFAULT_PHASE109_DIR,
        sub / "phase110",
        base_dir,
    )
    run_step(
        step_rows,
        "P115_PHASE111_FINAL_DISCOVERY",
        "Refresh candidate discovery after import/readiness/gate run.",
        run_phase111,
        candidate_roots,
        sub / "phase96",
        sub / "phase110",
        sub / "phase111_final",
        base_dir,
    )

    steps = pd.DataFrame(step_rows)
    acceptance = summarize(output_dir, steps, execute_import)
    steps.to_csv(output_dir / "phase115_refresh_step_ledger.csv", index=False)
    acceptance.to_csv(output_dir / "phase115_real_panel_refresh_acceptance_summary.csv", index=False)
    write_report(output_dir, {"Acceptance Summary": acceptance, "Step Ledger": steps})

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase115_real_panel_refresh_orchestrator",
        **reproducibility_fields(
            artifact_id="phase115",
            generated_utc=generated_utc,
            inputs={
                "source_root": str(source_root),
                "target_root": str(target_root),
                "real_root": str(real_root),
                "candidate_roots": [str(path) for path in candidate_roots],
            },
            parameters={
                "execute_import": execute_import,
                "overwrite": overwrite,
                "default_exchange": default_exchange,
                "max_files_per_symbol": max_files_per_symbol,
                "strategy_replay_policy": "closed_until_phase110_unlock",
            },
            outputs={
                "step_ledger": str(output_dir / "phase115_refresh_step_ledger.csv"),
                "acceptance_summary": str(output_dir / "phase115_real_panel_refresh_acceptance_summary.csv"),
                "report": str(output_dir / "phase115_real_panel_refresh_orchestrator_report.md"),
                "manifest": str(output_dir / "phase115_real_panel_refresh_orchestrator_manifest.json"),
            },
            random_seed="none_deterministic_phase115_refresh",
            scenario_ids="phase115_real_panel_refresh_orchestrator",
            cost_model_version="not_applicable",
            latency_model_version="phase110_multiday_gate",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase115_real_panel_refresh_orchestrator_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run real-panel refresh chain from discovery through replay unlock gate.")
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--target-root", type=Path, default=DEFAULT_TARGET_ROOT)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--candidate-roots", nargs="+", type=Path, default=DEFAULT_CANDIDATE_ROOTS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--execute-import", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--default-exchange", default=DEFAULT_EXCHANGE)
    parser.add_argument("--max-files-per-symbol", type=int, default=DEFAULT_MAX_FILES_PER_SYMBOL)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase115(
        args.source_root,
        args.target_root,
        args.real_root,
        args.candidate_roots,
        args.output_dir,
        args.base_dir,
        args.execute_import,
        args.overwrite,
        args.default_exchange,
        args.max_files_per_symbol,
    )


if __name__ == "__main__":
    main()

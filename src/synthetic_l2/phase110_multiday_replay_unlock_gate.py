from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE96_DIR = Path("outputs/phase96")
DEFAULT_PHASE109_DIR = Path("outputs/phase109")
DEFAULT_OUTPUT_DIR = Path("outputs/phase110")
MIN_READY_REAL_DAYS = 5
TARGET_READY_REAL_DAYS = 10


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


def build_gate_rows(phase96_dir: Path, phase109_dir: Path) -> pd.DataFrame:
    phase109_pass = int(float(metric_value(phase109_dir / "phase109_residual_imbalance_floor_acceptance_summary.csv", "phase109_full_symbol_calibrated_realism_pass", 0)))
    phase109_gaps = int(float(metric_value(phase109_dir / "phase109_residual_imbalance_floor_acceptance_summary.csv", "phase109_calibration_gap_rows", 999999)))
    phase109_replay = int(float(metric_value(phase109_dir / "phase109_residual_imbalance_floor_acceptance_summary.csv", "phase109_strategy_replay_allowed", 1)))
    ready_days = int(float(metric_value(phase96_dir / "real_anchor_panel_builder_acceptance_summary.csv", "phase96_ready_anchor_days", 0)))
    panels_ready = int(float(metric_value(phase96_dir / "real_anchor_panel_builder_acceptance_summary.csv", "phase96_panels_ready_for_phase94_rerun", 0)))
    phase96_unlocked = int(float(metric_value(phase96_dir / "real_anchor_panel_builder_acceptance_summary.csv", "phase96_strategy_replay_unlocked", 0)))
    return pd.DataFrame(
        [
            {
                "gate_id": "P110_ONE_DAY_FULL_SYMBOL_REALISM_PASS",
                "gate_pass": bool(phase109_pass == 1 and phase109_gaps == 0),
                "evidence": f"phase109_full_symbol_calibrated_realism_pass={phase109_pass}; phase109_calibration_gap_rows={phase109_gaps}",
                "next_action_if_fail": "rerun_symbol_aware_generator_calibration",
            },
            {
                "gate_id": "P110_PHASE109_REPLAY_LOCK_PRESERVED",
                "gate_pass": bool(phase109_replay == 0),
                "evidence": f"phase109_strategy_replay_allowed={phase109_replay}",
                "next_action_if_fail": "restore_strategy_replay_lock",
            },
            {
                "gate_id": "P110_MIN_MULTIDAY_REAL_PANEL_AVAILABLE",
                "gate_pass": bool(ready_days >= MIN_READY_REAL_DAYS),
                "evidence": f"phase96_ready_anchor_days={ready_days}; required_min={MIN_READY_REAL_DAYS}",
                "next_action_if_fail": "collect_more_real_websocket_l2_days",
            },
            {
                "gate_id": "P110_PHASE96_PANEL_READY_FOR_RERUN",
                "gate_pass": bool(panels_ready >= 1),
                "evidence": f"phase96_panels_ready_for_phase94_rerun={panels_ready}",
                "next_action_if_fail": "rerun_phase96_after_multiday_real_panel_ingest",
            },
            {
                "gate_id": "P110_PHASE96_STRATEGY_UNLOCK",
                "gate_pass": bool(phase96_unlocked == 1),
                "evidence": f"phase96_strategy_replay_unlocked={phase96_unlocked}",
                "next_action_if_fail": "keep_strategy_replay_closed_until_multiday_realism_passes",
            },
        ]
    )


def build_acquisition_queue(phase96_dir: Path) -> pd.DataFrame:
    readiness = pd.read_csv(phase96_dir / "real_day_readiness.csv")
    ready_days = int(readiness["day_ready_for_anchor_panel"].astype(bool).sum()) if not readiness.empty else 0
    days_needed_min = max(0, MIN_READY_REAL_DAYS - ready_days)
    days_needed_target = max(0, TARGET_READY_REAL_DAYS - ready_days)
    observed_dates = ";".join(readiness.loc[readiness["day_ready_for_anchor_panel"].astype(bool), "trade_date"].astype(str).tolist())
    return pd.DataFrame(
        [
            {
                "priority": 1,
                "work_item": "collect_minimum_multiday_real_anchor_panel",
                "current_ready_days": ready_days,
                "required_ready_days": MIN_READY_REAL_DAYS,
                "target_ready_days": TARGET_READY_REAL_DAYS,
                "days_needed_for_min": days_needed_min,
                "days_needed_for_target": days_needed_target,
                "observed_ready_dates": observed_dates,
                "acceptance_gate": "Phase96 ready_anchor_days >= 5 and panels_ready_for_phase94_rerun >= 1.",
            },
            {
                "priority": 2,
                "work_item": "rerun_phase109_style_calibrated_realism_on_multiday_panel",
                "current_ready_days": ready_days,
                "required_ready_days": MIN_READY_REAL_DAYS,
                "target_ready_days": TARGET_READY_REAL_DAYS,
                "days_needed_for_min": days_needed_min,
                "days_needed_for_target": days_needed_target,
                "observed_ready_dates": observed_dates,
                "acceptance_gate": "0 severe metric gaps and acceptable total gap fraction on the multiday panel.",
            },
            {
                "priority": 3,
                "work_item": "only_then_consider_strategy_replay",
                "current_ready_days": ready_days,
                "required_ready_days": MIN_READY_REAL_DAYS,
                "target_ready_days": TARGET_READY_REAL_DAYS,
                "days_needed_for_min": days_needed_min,
                "days_needed_for_target": days_needed_target,
                "observed_ready_dates": observed_dates,
                "acceptance_gate": "Phase110 replay_unlock_allowed=1.",
            },
        ]
    )


def summarize(gates: pd.DataFrame, acquisition: pd.DataFrame) -> pd.DataFrame:
    pass_count = int(gates["gate_pass"].astype(bool).sum())
    ready_days = int(acquisition["current_ready_days"].iloc[0]) if not acquisition.empty else 0
    days_needed_min = int(acquisition["days_needed_for_min"].iloc[0]) if not acquisition.empty else MIN_READY_REAL_DAYS
    replay_unlock_allowed = bool(gates["gate_pass"].astype(bool).all())
    return pd.DataFrame(
        [
            ("phase110_gate_rows", int(len(gates)), "Replay unlock gates evaluated"),
            ("phase110_gate_pass_rows", pass_count, "Replay unlock gates passing"),
            ("phase110_one_day_realism_gate_pass", int(gates.loc[gates["gate_id"].eq("P110_ONE_DAY_FULL_SYMBOL_REALISM_PASS"), "gate_pass"].iloc[0]), "1 means Phase109 one-day full-symbol realism passed"),
            ("phase110_ready_real_anchor_days", ready_days, "Ready real anchor days currently available"),
            ("phase110_required_ready_real_days_min", MIN_READY_REAL_DAYS, "Minimum ready real days required"),
            ("phase110_target_ready_real_days", TARGET_READY_REAL_DAYS, "Preferred ready real days target"),
            ("phase110_days_needed_for_min", days_needed_min, "Additional ready days required for minimum multiday unlock"),
            ("phase110_replay_unlock_allowed", int(replay_unlock_allowed), "1 means strategy replay may reopen"),
            ("phase110_strategy_replay_allowed", int(replay_unlock_allowed), "Compatibility alias for replay unlock decision"),
            ("phase110_recommend_next_action", "collect_4_more_ready_real_websocket_l2_days_then_rerun_phase96_and_multiday_realism", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase110 Multiday Replay Unlock Gate",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase110 consolidates the clean one-day Phase109 realism result with the real multiday panel requirement.",
        "It deliberately keeps strategy replay closed unless all unlock gates pass.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase110_multiday_replay_unlock_gate_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase110(phase96_dir: Path, phase109_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    gates = build_gate_rows(phase96_dir, phase109_dir)
    acquisition = build_acquisition_queue(phase96_dir)
    acceptance = summarize(gates, acquisition)

    gates.to_csv(output_dir / "phase110_replay_unlock_gates.csv", index=False)
    acquisition.to_csv(output_dir / "phase110_real_anchor_acquisition_queue.csv", index=False)
    acceptance.to_csv(output_dir / "phase110_multiday_replay_unlock_acceptance_summary.csv", index=False)
    write_report(output_dir, {"Acceptance Summary": acceptance, "Replay Unlock Gates": gates, "Acquisition Queue": acquisition})

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase110_multiday_replay_unlock_gate",
        **reproducibility_fields(
            artifact_id="phase110",
            generated_utc=generated_utc,
            inputs={
                "phase96_acceptance": str(phase96_dir / "real_anchor_panel_builder_acceptance_summary.csv"),
                "phase96_replay_gate": str(phase96_dir / "real_anchor_replay_gate.csv"),
                "phase109_acceptance": str(phase109_dir / "phase109_residual_imbalance_floor_acceptance_summary.csv"),
            },
            parameters={
                "minimum_ready_real_days": MIN_READY_REAL_DAYS,
                "target_ready_real_days": TARGET_READY_REAL_DAYS,
                "strategy_replay_policy": "closed_until_phase110_replay_unlock_allowed_equals_1",
            },
            outputs={
                "gates": str(output_dir / "phase110_replay_unlock_gates.csv"),
                "acquisition_queue": str(output_dir / "phase110_real_anchor_acquisition_queue.csv"),
                "acceptance_summary": str(output_dir / "phase110_multiday_replay_unlock_acceptance_summary.csv"),
                "report": str(output_dir / "phase110_multiday_replay_unlock_gate_report.md"),
                "manifest": str(output_dir / "phase110_multiday_replay_unlock_gate_manifest.json"),
            },
            random_seed="none_deterministic_phase110_gate",
            scenario_ids="phase110_post_phase109_multiday_replay_unlock_gate",
            cost_model_version="not_applicable",
            latency_model_version="phase109_symbol_aware_realism_gate",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase110_multiday_replay_unlock_gate_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate multiday replay unlock gate after Phase109 realism pass.")
    parser.add_argument("--phase96-dir", type=Path, default=DEFAULT_PHASE96_DIR)
    parser.add_argument("--phase109-dir", type=Path, default=DEFAULT_PHASE109_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase110(args.phase96_dir, args.phase109_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

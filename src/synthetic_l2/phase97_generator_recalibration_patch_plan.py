from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE94_DIR = Path("outputs/phase94")
DEFAULT_PHASE96_DIR = Path("outputs/phase96")
DEFAULT_OUTPUT_DIR = Path("outputs/phase97")


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


def load_inputs(phase94_dir: Path, phase96_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    gaps = pd.read_csv(phase94_dir / "calibration_gap_summary.csv")
    comparison = pd.read_csv(phase94_dir / "real_vs_synthetic_calibration_comparison.csv")
    remediation = pd.read_csv(phase94_dir / "calibration_remediation_queue.csv")
    replay_gate = pd.read_csv(phase96_dir / "real_anchor_replay_gate.csv")
    return gaps, comparison, remediation, replay_gate


def severity(gap_fraction: float) -> str:
    if gap_fraction >= 0.50:
        return "severe"
    if gap_fraction >= 0.25:
        return "material"
    if gap_fraction > 0:
        return "watch"
    return "pass"


def build_patch_plan(gaps: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "p90_gap_ms": {
            "generator_layer": "event_timing_point_process",
            "patch_intent": "increase tail inter-arrival gaps or reduce over-dense burst persistence where synthetic/real ratio is too low",
            "primary_knobs": "hawkes_baseline_intensity|self_excitation_decay|retail_feed_throttle|disconnect_gap_injection",
            "validation_metric": "p90_gap_ms gap_fraction <= 0.25 and median synthetic_to_real_ratio within [0.20, 5.00]",
        },
        "one_tick_return_std": {
            "generator_layer": "efficient_price_and_microprice_noise",
            "patch_intent": "reduce synthetic one-tick volatility scale when synthetic/real ratio is too high",
            "primary_knobs": "per_tick_volatility_multiplier|jump_size_scale|microprice_noise_scale|shock_decay",
            "validation_metric": "one_tick_return_std gap_fraction <= 0.25 and median synthetic_to_real_ratio within [0.10, 10.00]",
        },
        "median_abs_l1_imbalance": {
            "generator_layer": "l1_queue_size_and_imbalance_model",
            "patch_intent": "increase or reshape displayed L1 imbalance dispersion when synthetic imbalance is too muted",
            "primary_knobs": "l1_quantity_skew_scale|bid_ask_copula_strength|queue_replenishment_asymmetry",
            "validation_metric": "median_abs_l1_imbalance gap_fraction <= 0.25 and median synthetic_to_real_ratio within [0.25, 4.00]",
        },
        "median_l5_depth": {
            "generator_layer": "l2_depth_shape_model",
            "patch_intent": "rebalance L2 depth ladder scale and cross-symbol heterogeneity",
            "primary_knobs": "depth_ladder_multiplier|level_decay_curve|symbol_liquidity_scale|etf_equity_depth_split",
            "validation_metric": "median_l5_depth gap_fraction <= 0.25 and median synthetic_to_real_ratio within [0.10, 10.00]",
        },
        "median_l1_depth": {
            "generator_layer": "l1_depth_scale_model",
            "patch_intent": "rebalance top-of-book displayed depth scale after L5 shape adjustment",
            "primary_knobs": "l1_base_depth_multiplier|l1_l5_share_ratio|symbol_depth_shrinkage",
            "validation_metric": "median_l1_depth gap_fraction <= 0.25 and median synthetic_to_real_ratio within [0.10, 10.00]",
        },
        "median_spread_bps": {
            "generator_layer": "spread_model",
            "patch_intent": "preserve current spread calibration unless future multi-day anchors contradict it",
            "primary_knobs": "spread_tick_distribution|symbol_spread_scale|regime_spread_multiplier",
            "validation_metric": "median_spread_bps remains gap_fraction <= 0.25",
        },
        "p90_spread_bps": {
            "generator_layer": "spread_tail_model",
            "patch_intent": "preserve current tail spread calibration unless future multi-day anchors contradict it",
            "primary_knobs": "spread_tail_multiplier|shock_spread_widening|feed_profile_spread_noise",
            "validation_metric": "p90_spread_bps remains gap_fraction <= 0.25",
        },
        "median_gap_ms": {
            "generator_layer": "event_timing_point_process",
            "patch_intent": "monitor median cadence while fixing p90 cadence; avoid making the full stream too sparse",
            "primary_knobs": "baseline_intensity_floor|symbol_activity_scale",
            "validation_metric": "median_gap_ms gap_fraction <= 0.25",
        },
    }
    ranked = gaps.copy()
    ranked["severity"] = ranked["gap_fraction"].astype(float).map(severity)
    ranked = ranked.sort_values(["gap_fraction", "symbol_metrics"], ascending=[False, False], kind="mergesort")
    rows: list[dict[str, Any]] = []
    for priority, row in enumerate(ranked.to_dict("records"), start=1):
        metric = str(row["metric"])
        spec = mapping.get(
            metric,
            {
                "generator_layer": "unmapped_generator_layer",
                "patch_intent": "triage manually",
                "primary_knobs": "manual_review",
                "validation_metric": f"{metric} gap_fraction <= 0.25",
            },
        )
        rows.append(
            {
                "priority": priority,
                "metric": metric,
                "category": row["category"],
                "severity": row["severity"],
                "gap_fraction": float(row["gap_fraction"]),
                "median_synthetic_to_real_ratio": float(row["median_synthetic_to_real_ratio"]),
                "generator_layer": spec["generator_layer"],
                "patch_intent": spec["patch_intent"],
                "primary_knobs": spec["primary_knobs"],
                "validation_metric": spec["validation_metric"],
                "requires_multiday_confirmation": True,
            }
        )
    return pd.DataFrame(rows)


def build_patch_sequence(patch_plan: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "sequence": 1,
                "stage": "real_anchor_extension",
                "action": "Collect or ingest at least 5 ready real L2 days, 10 preferred, then rerun Phase96 and Phase94.",
                "exit_gate": "phase96_panels_ready_for_phase94_rerun=1",
            },
            {
                "sequence": 2,
                "stage": "timing_patch",
                "action": "Patch p90_gap_ms first because event cadence affects all replay horizons and forward-fill/staleness assumptions.",
                "exit_gate": "p90_gap_ms gap_fraction <= 0.25 without breaking median_gap_ms",
            },
            {
                "sequence": 3,
                "stage": "volatility_patch",
                "action": "Patch one_tick_return_std after timing because current synthetic one-tick volatility is too high relative to the real anchor.",
                "exit_gate": "one_tick_return_std gap_fraction <= 0.25",
            },
            {
                "sequence": 4,
                "stage": "book_shape_patch",
                "action": "Patch L1 imbalance and L1/L5 depth scales together so the book ladder remains internally consistent.",
                "exit_gate": "median_abs_l1_imbalance, median_l1_depth, and median_l5_depth gap_fraction <= 0.25",
            },
            {
                "sequence": 5,
                "stage": "preserve_passing_spread_anchor",
                "action": "Keep median and p90 spread calibration within current passing gates while other patches are applied.",
                "exit_gate": "median_spread_bps and p90_spread_bps gap_fraction remain <= 0.25",
            },
            {
                "sequence": 6,
                "stage": "replay_gate_review",
                "action": "Only after Phase94 passes on multi-day anchors may a new strategy-family precommit be created.",
                "exit_gate": "phase94_strategy_replay_resume_allowed=1",
            },
        ]
    )


def build_strategy_lock(replay_gate: pd.DataFrame, phase94_dir: Path, phase96_dir: Path) -> pd.DataFrame:
    phase94_resume = metric_value(phase94_dir / "generator_realism_calibration_acceptance_summary.csv", "phase94_strategy_replay_resume_allowed", 0)
    phase96_unlocked = metric_value(phase96_dir / "real_anchor_panel_builder_acceptance_summary.csv", "phase96_strategy_replay_unlocked", 0)
    p96_lock = False
    if not replay_gate.empty and "gate_id" in replay_gate.columns:
        row = replay_gate[replay_gate["gate_id"].eq("P96_STRATEGY_REPLAY_LOCK")]
        if not row.empty:
            p96_lock = str(row.iloc[0]["gate_pass"]).lower() == "true"
    unlocked = bool(int(float(phase94_resume)) == 1 and int(float(phase96_unlocked)) == 1 and p96_lock)
    return pd.DataFrame(
        [
            {
                "lock_id": "P97_STRATEGY_REPLAY_LOCK",
                "strategy_replay_allowed": unlocked,
                "phase94_strategy_resume_allowed": int(float(phase94_resume)),
                "phase96_strategy_replay_unlocked": int(float(phase96_unlocked)),
                "decision": "replay_closed" if not unlocked else "replay_may_resume_with_precommit",
                "allowed_next_action": "generator_recalibration_and_real_panel_collection"
                if not unlocked
                else "new_strategy_precommit_only_no_direct_replay",
            }
        ]
    )


def summarize(patch_plan: pd.DataFrame, strategy_lock: pd.DataFrame) -> pd.DataFrame:
    severe = int(patch_plan["severity"].eq("severe").sum()) if not patch_plan.empty else 0
    material_or_worse = int(patch_plan["severity"].isin(["severe", "material"]).sum()) if not patch_plan.empty else 0
    replay_allowed = bool(strategy_lock["strategy_replay_allowed"].iloc[0]) if not strategy_lock.empty else False
    return pd.DataFrame(
        [
            ("phase97_patch_metric_rows", int(len(patch_plan)), "Calibration metrics mapped into generator patch plan"),
            ("phase97_severe_patch_rows", severe, "Metrics with >=50% symbol-anchor gap fraction"),
            ("phase97_material_or_severe_patch_rows", material_or_worse, "Metrics with >=25% symbol-anchor gap fraction"),
            ("phase97_strategy_replay_allowed", int(replay_allowed), "1 means strategy replay may resume"),
            ("phase97_generator_recalibration_required", int(not replay_allowed), "1 means generator/data calibration work remains required"),
            ("phase97_recommend_next_action", "extend_real_anchor_panel_then_patch_timing_volatility_book_shape", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase97 Generator Recalibration Patch Plan",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase97 converts Phase94 calibration gaps and Phase96 real-panel readiness into an ordered generator recalibration plan.",
        "It does not reopen strategy replay; it preserves the lock until real-anchor coverage and calibration gates pass.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase97_generator_recalibration_patch_plan_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase97(phase94_dir: Path, phase96_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    gaps, comparison, remediation, replay_gate = load_inputs(phase94_dir, phase96_dir)
    patch_plan = build_patch_plan(gaps)
    sequence = build_patch_sequence(patch_plan)
    strategy_lock = build_strategy_lock(replay_gate, phase94_dir, phase96_dir)
    acceptance = summarize(patch_plan, strategy_lock)

    patch_plan.to_csv(output_dir / "generator_recalibration_patch_plan.csv", index=False)
    sequence.to_csv(output_dir / "generator_recalibration_patch_sequence.csv", index=False)
    strategy_lock.to_csv(output_dir / "strategy_replay_lock.csv", index=False)
    acceptance.to_csv(output_dir / "generator_recalibration_patch_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Patch Plan": patch_plan,
            "Patch Sequence": sequence,
            "Strategy Replay Lock": strategy_lock,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase97_generator_recalibration_patch_plan"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase97",
            generated_utc=generated_utc,
            inputs={
                "phase94_gap_summary": str(phase94_dir / "calibration_gap_summary.csv"),
                "phase94_comparison": str(phase94_dir / "real_vs_synthetic_calibration_comparison.csv"),
                "phase94_remediation": str(phase94_dir / "calibration_remediation_queue.csv"),
                "phase96_replay_gate": str(phase96_dir / "real_anchor_replay_gate.csv"),
            },
            parameters={
                "strategy_replay_policy": "closed_until_phase94_and_phase96_pass",
                "patch_order": "real_anchor_extension_then_timing_then_volatility_then_book_shape_then_spread_preservation",
                "gap_fraction_material_threshold": 0.25,
                "gap_fraction_severe_threshold": 0.50,
            },
            outputs={
                "patch_plan": str(output_dir / "generator_recalibration_patch_plan.csv"),
                "patch_sequence": str(output_dir / "generator_recalibration_patch_sequence.csv"),
                "strategy_replay_lock": str(output_dir / "strategy_replay_lock.csv"),
                "acceptance_summary": str(output_dir / "generator_recalibration_patch_acceptance_summary.csv"),
                "report": str(output_dir / "phase97_generator_recalibration_patch_plan_report.md"),
                "manifest": str(output_dir / "phase97_generator_recalibration_patch_plan_manifest.json"),
            },
            random_seed="none_deterministic_patch_plan",
            scenario_ids="phase97_post_phase94_phase96_recalibration_plan",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_patch_plan",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase97_generator_recalibration_patch_plan_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build generator recalibration patch plan from Phase94/96 evidence.")
    parser.add_argument("--phase94-dir", type=Path, default=DEFAULT_PHASE94_DIR)
    parser.add_argument("--phase96-dir", type=Path, default=DEFAULT_PHASE96_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase97(args.phase94_dir, args.phase96_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

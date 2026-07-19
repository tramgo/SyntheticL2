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


DEFAULT_PHASE97_DIR = Path("outputs/phase97")
DEFAULT_OUTPUT_DIR = Path("outputs/phase98")


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


def load_patch_plan(phase97_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    return (
        pd.read_csv(phase97_dir / "generator_recalibration_patch_plan.csv"),
        pd.read_csv(phase97_dir / "strategy_replay_lock.csv"),
    )


def build_generator_knob_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "knob_id": "event_timing.tail_gap_multiplier",
                "generator_phase": "phase49_phase51_dense_timing",
                "current_observed_pattern": "dense_subtick_id adds millisecond offsets, creating over-dense tail cadence in Phase94",
                "default_value": 1.0,
                "candidate_values": "2.0|4.0|6.0|8.0",
                "target_metric": "p90_gap_ms",
                "expected_effect": "increase synthetic tail inter-arrival gaps while preserving enough median event density",
                "risk": "too high may make active symbols artificially sparse",
            },
            {
                "knob_id": "event_timing.burst_throttle_fraction",
                "generator_phase": "phase49_phase51_dense_timing",
                "current_observed_pattern": "dense repeats preserve source-event bursts too aggressively",
                "default_value": 0.0,
                "candidate_values": "0.10|0.20|0.35",
                "target_metric": "p90_gap_ms",
                "expected_effect": "thin or stagger dense burst repetitions to reduce unrealistic burst persistence",
                "risk": "may reduce rows and change storage-size assumptions",
            },
            {
                "knob_id": "price.micro_step_spread_fraction",
                "generator_phase": "phase49_phase51_dense_price",
                "current_observed_pattern": "dense micro-step uses spread * 0.08 and Phase94 shows high one-tick volatility",
                "default_value": 0.08,
                "candidate_values": "0.02|0.03|0.04|0.05",
                "target_metric": "one_tick_return_std",
                "expected_effect": "reduce synthetic one-tick volatility without changing spread anchors",
                "risk": "too low may suppress legitimate short-horizon movement",
            },
            {
                "knob_id": "price.jump_size_scale",
                "generator_phase": "phase45_phase51_price_state",
                "current_observed_pattern": "Phase94 median synthetic/real one_tick_return_std ratio slightly exceeds upper gate",
                "default_value": 1.0,
                "candidate_values": "0.45|0.60|0.75|0.90",
                "target_metric": "one_tick_return_std",
                "expected_effect": "reduce generator jump contribution while preserving regime ranking",
                "risk": "may flatten shock days if applied globally instead of regime-conditionally",
            },
            {
                "knob_id": "book.l1_quantity_skew_scale",
                "generator_phase": "phase45_add_depth_levels",
                "current_observed_pattern": "l1_imbalance is clipped and converted directly into bid/ask quantity skew; Phase94 shows muted median_abs_l1_imbalance",
                "default_value": 1.0,
                "candidate_values": "1.25|1.50|1.75|2.00",
                "target_metric": "median_abs_l1_imbalance",
                "expected_effect": "increase displayed L1 imbalance dispersion",
                "risk": "can create unrealistic one-sided displayed quantity if not clipped",
            },
            {
                "knob_id": "book.depth_ladder_multiplier",
                "generator_phase": "phase45_add_depth_levels",
                "current_observed_pattern": "base_qty = 100 + event_intensity * 250 with level_weight = 1 + 0.35*(level-1)",
                "default_value": 1.0,
                "candidate_values": "0.50|0.65|0.80|1.20",
                "target_metric": "median_l5_depth",
                "expected_effect": "rebalance L5 displayed depth scale and cross-symbol heterogeneity",
                "risk": "must be coordinated with L1 depth so ladder shape remains plausible",
            },
            {
                "knob_id": "book.l1_l5_share_ratio",
                "generator_phase": "phase45_add_depth_levels",
                "current_observed_pattern": "level weights create deterministic ladder shape from the same base quantity",
                "default_value": 1.0,
                "candidate_values": "0.70|0.85|1.15|1.30",
                "target_metric": "median_l1_depth|median_l5_depth",
                "expected_effect": "adjust top-of-book share relative to deeper displayed book",
                "risk": "may pass L1 but fail L5 unless jointly validated",
            },
            {
                "knob_id": "spread.preserve_current_scale",
                "generator_phase": "phase45_phase51_spread",
                "current_observed_pattern": "Phase94 median and p90 spread anchors pass",
                "default_value": 1.0,
                "candidate_values": "1.0",
                "target_metric": "median_spread_bps|p90_spread_bps",
                "expected_effect": "hold spread distribution stable during timing/volatility/book patches",
                "risk": "do not accidentally fix failing metrics by breaking passing spread anchors",
            },
        ]
    )


def build_candidate_profiles() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "profile_id": "P98_TIMING_ONLY_CONSERVATIVE",
                "scope": "timing",
                "description": "Smallest timing patch; tests whether tail cadence can improve without reducing median event support too far.",
                "event_timing.tail_gap_multiplier": 2.0,
                "event_timing.burst_throttle_fraction": 0.10,
                "price.micro_step_spread_fraction": 0.08,
                "price.jump_size_scale": 1.0,
                "book.l1_quantity_skew_scale": 1.0,
                "book.depth_ladder_multiplier": 1.0,
                "book.l1_l5_share_ratio": 1.0,
                "spread.preserve_current_scale": 1.0,
            },
            {
                "profile_id": "P98_TIMING_VOL_MODERATE",
                "scope": "timing_volatility",
                "description": "Moderate timing and volatility patch matching the two severe Phase97 gaps.",
                "event_timing.tail_gap_multiplier": 4.0,
                "event_timing.burst_throttle_fraction": 0.20,
                "price.micro_step_spread_fraction": 0.04,
                "price.jump_size_scale": 0.75,
                "book.l1_quantity_skew_scale": 1.0,
                "book.depth_ladder_multiplier": 1.0,
                "book.l1_l5_share_ratio": 1.0,
                "spread.preserve_current_scale": 1.0,
            },
            {
                "profile_id": "P98_FULL_BOOK_REBALANCE_BASE",
                "scope": "timing_volatility_book",
                "description": "Base full patch: timing and volatility plus L1 imbalance/depth rebalance.",
                "event_timing.tail_gap_multiplier": 4.0,
                "event_timing.burst_throttle_fraction": 0.20,
                "price.micro_step_spread_fraction": 0.04,
                "price.jump_size_scale": 0.75,
                "book.l1_quantity_skew_scale": 1.50,
                "book.depth_ladder_multiplier": 0.80,
                "book.l1_l5_share_ratio": 0.85,
                "spread.preserve_current_scale": 1.0,
            },
            {
                "profile_id": "P98_FULL_BOOK_REBALANCE_STRONG",
                "scope": "timing_volatility_book",
                "description": "Stronger full patch for sensitivity testing if base patch under-corrects cadence/volatility.",
                "event_timing.tail_gap_multiplier": 6.0,
                "event_timing.burst_throttle_fraction": 0.35,
                "price.micro_step_spread_fraction": 0.03,
                "price.jump_size_scale": 0.60,
                "book.l1_quantity_skew_scale": 1.75,
                "book.depth_ladder_multiplier": 0.65,
                "book.l1_l5_share_ratio": 0.85,
                "spread.preserve_current_scale": 1.0,
            },
        ]
    )


def build_validation_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "gate_id": "P98_NO_STRATEGY_REPLAY",
                "requirement": "Calibration profiles may only produce generator quality and Phase94-style anchor evidence.",
                "pass_threshold": "No P&L replay or strategy promotion artifacts generated by calibration runs.",
            },
            {
                "gate_id": "P98_REAL_PANEL_FIRST",
                "requirement": "Preferred path is to extend the real panel before finalizing any generator patch.",
                "pass_threshold": "Phase96 panels_ready_for_phase94_rerun=1 before declaring calibration fixed.",
            },
            {
                "gate_id": "P98_TIMING",
                "requirement": "Tail cadence severe gap must clear without breaking median cadence.",
                "pass_threshold": "p90_gap_ms gap_fraction<=0.25 and median_gap_ms gap_fraction<=0.25",
            },
            {
                "gate_id": "P98_VOLATILITY",
                "requirement": "One-tick volatility severe gap must clear.",
                "pass_threshold": "one_tick_return_std gap_fraction<=0.25",
            },
            {
                "gate_id": "P98_BOOK_SHAPE",
                "requirement": "L1 imbalance and L1/L5 depth must jointly clear material gap gates.",
                "pass_threshold": "median_abs_l1_imbalance, median_l1_depth and median_l5_depth gap_fraction<=0.25",
            },
            {
                "gate_id": "P98_SPREAD_PRESERVATION",
                "requirement": "Passing spread anchors must remain passing.",
                "pass_threshold": "median_spread_bps and p90_spread_bps gap_fraction<=0.25",
            },
            {
                "gate_id": "P98_REOPEN_STRATEGY_REPLAY",
                "requirement": "Strategy replay can reopen only after Phase94 passes on an adequate real anchor panel.",
                "pass_threshold": "phase94_strategy_replay_resume_allowed=1 and phase96_strategy_replay_unlocked=1",
            },
        ]
    )


def build_wiring_targets(knobs: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "target_file": "src/synthetic_l2/phase45_raw_tick_lake_materializer.py",
                "target_function": "add_depth_levels",
                "knobs_to_wire": "book.l1_quantity_skew_scale|book.depth_ladder_multiplier|book.l1_l5_share_ratio|spread.preserve_current_scale",
                "current_code_anchor": "base_qty = 100 + intensity * 250; level_weight = 1.0 + 0.35 * (level - 1)",
                "patch_requirement": "Accept a calibration profile object and apply depth/imbalance multipliers without changing default output when profile is absent.",
            },
            {
                "target_file": "src/synthetic_l2/phase49_dense_tick_rate_expansion.py",
                "target_function": "densify_frame",
                "knobs_to_wire": "event_timing.tail_gap_multiplier|event_timing.burst_throttle_fraction|price.micro_step_spread_fraction|price.jump_size_scale",
                "current_code_anchor": "callback_received_utc_ms += dense_subtick_id; micro_step = spread * 0.08",
                "patch_requirement": "Support calibrated subtick spacing/throttle and micro-step scaling while preserving deterministic dense ids.",
            },
            {
                "target_file": "src/synthetic_l2/phase51_full_dense_lake_materializer.py",
                "target_function": "_densify_chunk",
                "knobs_to_wire": "event_timing.tail_gap_multiplier|event_timing.burst_throttle_fraction|price.micro_step_spread_fraction|price.jump_size_scale",
                "current_code_anchor": "callback_received_utc_ms += dense_subtick_id; micro_step = spread * 0.08",
                "patch_requirement": "Apply the same calibrated dense timing/price behavior used by Phase49 so shard and full-lake generation remain consistent.",
            },
            {
                "target_file": "src/synthetic_l2/phase94_generator_realism_calibration_audit.py",
                "target_function": "run_phase94",
                "knobs_to_wire": "profile_id|calibration_profile_manifest",
                "current_code_anchor": "compares real anchor profile vs synthetic compact profile",
                "patch_requirement": "Record active generator calibration profile in the audit manifest and compare against the same gates.",
            },
        ]
    )


def build_acceptance_summary(
    patch_plan: pd.DataFrame,
    strategy_lock: pd.DataFrame,
    knobs: pd.DataFrame,
    profiles: pd.DataFrame,
    gates: pd.DataFrame,
) -> pd.DataFrame:
    replay_allowed = bool(strategy_lock["strategy_replay_allowed"].astype(str).str.lower().eq("true").any())
    severe_rows = int(patch_plan["severity"].astype(str).eq("severe").sum())
    return pd.DataFrame(
        [
            ("phase98_patch_metric_rows", int(len(patch_plan)), "Phase97 patch metrics consumed"),
            ("phase98_severe_metric_rows", severe_rows, "Severe Phase97 metrics requiring calibration"),
            ("phase98_generator_knob_rows", int(len(knobs)), "Generator knobs cataloged for calibration wiring"),
            ("phase98_candidate_profile_rows", int(len(profiles)), "Candidate calibration profiles defined"),
            ("phase98_validation_gate_rows", int(len(gates)), "Validation gates locked before generator patch execution"),
            ("phase98_strategy_replay_allowed", int(replay_allowed), "1 means strategy replay may resume now"),
            ("phase98_ready_for_generator_patch_wiring", int(len(knobs) >= 8 and len(profiles) >= 4 and not replay_allowed), "1 means Phase99 may wire calibration profiles into generator code"),
            ("phase98_recommend_next_action", "wire_calibration_profiles_into_generator_then_rerun_phase94_quality_only", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase98 Generator Calibration Config Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase98 turns the Phase97 patch plan into explicit generator calibration knobs, candidate profiles, wiring targets and validation gates.",
        "It does not change generated data yet and does not reopen strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase98_generator_calibration_config_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase98(phase97_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    patch_plan, strategy_lock = load_patch_plan(phase97_dir)
    knobs = build_generator_knob_catalog()
    profiles = build_candidate_profiles()
    gates = build_validation_contract()
    wiring = build_wiring_targets(knobs)
    acceptance = build_acceptance_summary(patch_plan, strategy_lock, knobs, profiles, gates)

    knobs.to_csv(output_dir / "generator_calibration_knob_catalog.csv", index=False)
    profiles.to_csv(output_dir / "generator_calibration_candidate_profiles.csv", index=False)
    gates.to_csv(output_dir / "generator_calibration_validation_contract.csv", index=False)
    wiring.to_csv(output_dir / "generator_calibration_wiring_targets.csv", index=False)
    strategy_lock.to_csv(output_dir / "strategy_replay_lock_passthrough.csv", index=False)
    acceptance.to_csv(output_dir / "generator_calibration_config_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Generator Knob Catalog": knobs,
            "Candidate Calibration Profiles": profiles,
            "Validation Contract": gates,
            "Wiring Targets": wiring,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase98_generator_calibration_config_contract"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase98",
            generated_utc=generated_utc,
            inputs={
                "phase97_patch_plan": str(phase97_dir / "generator_recalibration_patch_plan.csv"),
                "phase97_strategy_lock": str(phase97_dir / "strategy_replay_lock.csv"),
            },
            parameters={
                "strategy_replay_policy": "closed",
                "profile_policy": "candidate_generator_quality_profiles_only",
                "next_phase": "wire_profiles_without_strategy_replay",
            },
            outputs={
                "knob_catalog": str(output_dir / "generator_calibration_knob_catalog.csv"),
                "candidate_profiles": str(output_dir / "generator_calibration_candidate_profiles.csv"),
                "validation_contract": str(output_dir / "generator_calibration_validation_contract.csv"),
                "wiring_targets": str(output_dir / "generator_calibration_wiring_targets.csv"),
                "acceptance_summary": str(output_dir / "generator_calibration_config_acceptance_summary.csv"),
                "report": str(output_dir / "phase98_generator_calibration_config_contract_report.md"),
                "manifest": str(output_dir / "phase98_generator_calibration_config_contract_manifest.json"),
            },
            random_seed="none_deterministic_config_contract",
            scenario_ids="phase98_post_phase97_generator_config_contract",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_config_contract",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase98_generator_calibration_config_contract_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create generator calibration config contract from Phase97 patch plan.")
    parser.add_argument("--phase97-dir", type=Path, default=DEFAULT_PHASE97_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase98(args.phase97_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

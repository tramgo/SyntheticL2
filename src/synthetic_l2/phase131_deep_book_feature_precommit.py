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


DEFAULT_OUTPUT_DIR = Path("outputs/phase131")
DEFAULT_PHASE129_DIR = Path("outputs/phase129")
DEFAULT_PHASE130_DIR = Path("outputs/phase130")
PINNED_COST_MODEL_VERSION = "zerodha_equity_intraday_nse_order_formula_v2_2026_07_14"
ALLOWED_DATASET = "outputs/phase129/allowed_context_label_matrix.csv"
FORBIDDEN_OUTPUTS = "strategy_code;buy_sell_signal;order_arrival_stream;live_tagged_fill_model;pnl_replay;profitability_claim"
BASELINE_BRIER_MARGIN = 0.005


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def build_feature_catalog() -> pd.DataFrame:
    rows = [
        {
            "feature_id": "p131_l2_l5_depth_ratio_bid",
            "definition": "bid_level_2_quantity / max(sum(bid_level_2_quantity..bid_level_5_quantity), 1)",
            "required_depth_levels": "L2,L3,L4,L5",
            "minimum_depth_level": 2,
            "maximum_depth_level": 5,
            "directional_use": "bid_resilience_context",
            "candidate_label_targets": "p129_regime_stability_label;p129_liquidity_opportunity_label",
            "forbidden_use": "entry_side_or_order_signal",
            "phase132_model_family": "single_feature_threshold;two_feature_threshold_combo",
            "strategy_replay_allowed": 0,
        },
        {
            "feature_id": "p131_l2_l5_depth_ratio_ask",
            "definition": "ask_level_2_quantity / max(sum(ask_level_2_quantity..ask_level_5_quantity), 1)",
            "required_depth_levels": "L2,L3,L4,L5",
            "minimum_depth_level": 2,
            "maximum_depth_level": 5,
            "directional_use": "ask_resilience_context",
            "candidate_label_targets": "p129_regime_stability_label;p129_liquidity_opportunity_label",
            "forbidden_use": "entry_side_or_order_signal",
            "phase132_model_family": "single_feature_threshold;two_feature_threshold_combo",
            "strategy_replay_allowed": 0,
        },
        {
            "feature_id": "p131_cumulative_notional_imbalance_top5",
            "definition": "(sum(bid_level_1_notional..bid_level_5_notional) - sum(ask_level_1_notional..ask_level_5_notional)) / max(total_top5_notional, 1)",
            "required_depth_levels": "L1,L2,L3,L4,L5",
            "minimum_depth_level": 2,
            "maximum_depth_level": 5,
            "directional_use": "deep_book_pressure_context",
            "candidate_label_targets": "p129_liquidity_opportunity_label;p129_cost_toxicity_refinement_label",
            "forbidden_use": "entry_side_or_order_signal",
            "phase132_model_family": "single_feature_threshold;two_feature_threshold_combo",
            "strategy_replay_allowed": 0,
        },
        {
            "feature_id": "p131_book_thinning_event_rate_1s",
            "definition": "rolling_1s_count(sum_top5_depth_t < 0.75 * rolling_5s_median_sum_top5_depth)",
            "required_depth_levels": "L1,L2,L3,L4,L5",
            "minimum_depth_level": 2,
            "maximum_depth_level": 5,
            "directional_use": "liquidity_withdrawal_context",
            "candidate_label_targets": "p129_regime_stability_label;p129_cost_toxicity_refinement_label",
            "forbidden_use": "entry_side_or_order_signal",
            "phase132_model_family": "single_feature_threshold;two_feature_threshold_combo",
            "strategy_replay_allowed": 0,
        },
        {
            "feature_id": "p131_level_crossing_hazard_bid",
            "definition": "rolling_1s_rate(best_bid_price moves through prior bid_level_2_price or deeper bid levels)",
            "required_depth_levels": "L2,L3,L4,L5",
            "minimum_depth_level": 2,
            "maximum_depth_level": 5,
            "directional_use": "bid_queue_depletion_context",
            "candidate_label_targets": "p129_cost_toxicity_refinement_label",
            "forbidden_use": "entry_side_or_order_signal",
            "phase132_model_family": "single_feature_threshold;two_feature_threshold_combo",
            "strategy_replay_allowed": 0,
        },
        {
            "feature_id": "p131_level_crossing_hazard_ask",
            "definition": "rolling_1s_rate(best_ask_price moves through prior ask_level_2_price or deeper ask levels)",
            "required_depth_levels": "L2,L3,L4,L5",
            "minimum_depth_level": 2,
            "maximum_depth_level": 5,
            "directional_use": "ask_queue_depletion_context",
            "candidate_label_targets": "p129_cost_toxicity_refinement_label",
            "forbidden_use": "entry_side_or_order_signal",
            "phase132_model_family": "single_feature_threshold;two_feature_threshold_combo",
            "strategy_replay_allowed": 0,
        },
        {
            "feature_id": "p131_depth_slope_top5_bid",
            "definition": "linear_slope(level_index, bid_level_1_quantity..bid_level_5_quantity)",
            "required_depth_levels": "L1,L2,L3,L4,L5",
            "minimum_depth_level": 2,
            "maximum_depth_level": 5,
            "directional_use": "bid_depth_shape_context",
            "candidate_label_targets": "p129_regime_stability_label;p129_liquidity_opportunity_label",
            "forbidden_use": "entry_side_or_order_signal",
            "phase132_model_family": "single_feature_threshold;two_feature_threshold_combo",
            "strategy_replay_allowed": 0,
        },
        {
            "feature_id": "p131_depth_slope_top5_ask",
            "definition": "linear_slope(level_index, ask_level_1_quantity..ask_level_5_quantity)",
            "required_depth_levels": "L1,L2,L3,L4,L5",
            "minimum_depth_level": 2,
            "maximum_depth_level": 5,
            "directional_use": "ask_depth_shape_context",
            "candidate_label_targets": "p129_regime_stability_label;p129_liquidity_opportunity_label",
            "forbidden_use": "entry_side_or_order_signal",
            "phase132_model_family": "single_feature_threshold;two_feature_threshold_combo",
            "strategy_replay_allowed": 0,
        },
        {
            "feature_id": "p131_mean_cancel_intensity_l2_l5",
            "definition": "rolling_mean(abs(delta_depth_l2..delta_depth_l5) where price level persists and depth decreases)",
            "required_depth_levels": "L2,L3,L4,L5",
            "minimum_depth_level": 2,
            "maximum_depth_level": 5,
            "directional_use": "passive_fill_realism_context",
            "candidate_label_targets": "p129_cost_toxicity_refinement_label",
            "forbidden_use": "entry_side_or_order_signal",
            "phase132_model_family": "single_feature_threshold;two_feature_threshold_combo",
            "strategy_replay_allowed": 0,
        },
        {
            "feature_id": "p131_deep_book_pressure_signed",
            "definition": "signed combination of top5 notional imbalance, bid/ask depth slopes, and l2_l5 cancel-intensity asymmetry",
            "required_depth_levels": "L2,L3,L4,L5",
            "minimum_depth_level": 2,
            "maximum_depth_level": 5,
            "directional_use": "deep_book_context_only",
            "candidate_label_targets": "p129_regime_stability_label;p129_liquidity_opportunity_label;p129_cost_toxicity_refinement_label",
            "forbidden_use": "entry_side_or_order_signal",
            "phase132_model_family": "single_feature_threshold;two_feature_threshold_combo",
            "strategy_replay_allowed": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_cost_regimes() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "cost_regime_id": "base",
                "cost_model_version": PINNED_COST_MODEL_VERSION,
                "zerodha_formula_edit_allowed": 0,
                "spread_cross_cost_multiplier": 1.0,
                "brokerage_multiplier": 1.0,
                "stt_multiplier": 1.0,
                "transaction_charge_multiplier": 1.0,
                "sebi_charge_multiplier": 1.0,
                "stamp_duty_multiplier": 1.0,
                "gst_multiplier": 1.0,
                "description": "Pinned Zerodha equity intraday NSE retail cash cost model unchanged.",
                "immutable_after_phase131": 1,
            },
            {
                "cost_regime_id": "harsh",
                "cost_model_version": PINNED_COST_MODEL_VERSION,
                "zerodha_formula_edit_allowed": 0,
                "spread_cross_cost_multiplier": 1.25,
                "brokerage_multiplier": 1.25,
                "stt_multiplier": 1.25,
                "transaction_charge_multiplier": 1.25,
                "sebi_charge_multiplier": 1.25,
                "stamp_duty_multiplier": 1.25,
                "gst_multiplier": 1.25,
                "description": "Pinned Zerodha formula plus 25 percent uplift to spread-cross cost and every per-leg fee component.",
                "immutable_after_phase131": 1,
            },
        ]
    )


def build_baseline_reference(phase130_selection: pd.DataFrame) -> pd.DataFrame:
    if phase130_selection.empty:
        return pd.DataFrame()
    frame = phase130_selection.copy()
    frame["reference_family"] = "phase130_l1_context_diagnostic_baseline"
    frame["minimum_brier_lift_required_for_phase132"] = BASELINE_BRIER_MARGIN
    frame["strategy_replay_allowed"] = 0
    return frame[
        [
            "label",
            "reference_family",
            "selected_model_id",
            "best_brier",
            "holdout_auc",
            "minimum_brier_lift_required_for_phase132",
            "strategy_replay_allowed",
        ]
    ]


def build_guardrails() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "guardrail_id": "P131_RETAIL_CASH_EQUITY_ONLY",
                "requirement": "Instrument scope remains NSE cash equity in the 32-symbol Phase96/Phase129 panel.",
                "enforcement": "Allowed dataset is locked to Phase129 allowed_context_label_matrix.csv.",
            },
            {
                "guardrail_id": "P131_DEPTH_REQUIRES_L2_L5",
                "requirement": "No precommitted feature may depend only on L1.",
                "enforcement": "Feature catalog must set minimum_depth_level >= 2 for every feature.",
            },
            {
                "guardrail_id": "P131_COST_MODEL_PINNED",
                "requirement": "Base regime must preserve the pinned Zerodha equity intraday NSE model exactly.",
                "enforcement": f"cost_model_version must equal {PINNED_COST_MODEL_VERSION}.",
            },
            {
                "guardrail_id": "P131_HARSH_REGIME_IMMUTABLE",
                "requirement": "Harsh stress factors are declared once and cannot be edited by later phases in this plan.",
                "enforcement": "phase131_cost_regimes.csv records immutable_after_phase131=1 for base and harsh.",
            },
            {
                "guardrail_id": "P131_NO_REPLAY_OR_PROFIT_CLAIMS",
                "requirement": "Phase131 ships specifications only.",
                "enforcement": f"Forbidden outputs: {FORBIDDEN_OUTPUTS}.",
            },
        ]
    )


def build_gate_evaluation(features: pd.DataFrame, costs: pd.DataFrame, baseline: pd.DataFrame, allowed_matrix: pd.DataFrame) -> pd.DataFrame:
    base_rows = costs[costs["cost_regime_id"].eq("base")] if not costs.empty else pd.DataFrame()
    harsh_rows = costs[costs["cost_regime_id"].eq("harsh")] if not costs.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            {
                "gate_id": "P131_FEATURE_CATALOG_SIZE",
                "gate_pass": int(8 <= len(features) <= 10),
                "evidence": f"feature_rows={len(features)}",
            },
            {
                "gate_id": "P131_NO_L1_ONLY_FEATURES",
                "gate_pass": int(not features.empty and pd.to_numeric(features["minimum_depth_level"], errors="coerce").ge(2).all()),
                "evidence": "minimum_depth_level>=2 for every feature",
            },
            {
                "gate_id": "P131_COST_REGIMES_LOCKED",
                "gate_pass": int(
                    len(costs) == 2
                    and set(costs["cost_regime_id"]) == {"base", "harsh"}
                    and costs["immutable_after_phase131"].astype(int).all()
                ),
                "evidence": f"cost_regimes={';'.join(costs['cost_regime_id'].astype(str).tolist()) if not costs.empty else ''}",
            },
            {
                "gate_id": "P131_PINNED_COST_MODEL_MATCH",
                "gate_pass": int(
                    ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION == PINNED_COST_MODEL_VERSION
                    and not base_rows.empty
                    and base_rows["cost_model_version"].astype(str).eq(PINNED_COST_MODEL_VERSION).all()
                    and not harsh_rows.empty
                    and harsh_rows["cost_model_version"].astype(str).eq(PINNED_COST_MODEL_VERSION).all()
                ),
                "evidence": f"repo_cost_model={ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION}",
            },
            {
                "gate_id": "P131_ALLOWED_DATASET_EXISTS",
                "gate_pass": int(not allowed_matrix.empty and len(allowed_matrix) == 228),
                "evidence": f"allowed_context_rows={len(allowed_matrix)}",
            },
            {
                "gate_id": "P131_PHASE130_BASELINE_REFERENCE_EXISTS",
                "gate_pass": int(not baseline.empty and len(baseline) == 3),
                "evidence": f"baseline_reference_rows={len(baseline)}",
            },
            {
                "gate_id": "P131_NO_REPLAY",
                "gate_pass": int(
                    (features.empty or features["strategy_replay_allowed"].astype(int).sum() == 0)
                    and (costs.empty or "strategy_replay_allowed" not in costs.columns)
                    and (baseline.empty or baseline["strategy_replay_allowed"].astype(int).sum() == 0)
                ),
                "evidence": "feature and baseline artifacts keep strategy_replay_allowed=0",
            },
        ]
    )


def build_acceptance_summary(features: pd.DataFrame, costs: pd.DataFrame, baseline: pd.DataFrame, gates: pd.DataFrame, allowed_matrix: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("phase131_feature_catalog_rows", int(len(features)), "Precommitted L2-L5 feature definitions"),
            ("phase131_l1_only_feature_rows", int(pd.to_numeric(features["minimum_depth_level"], errors="coerce").lt(2).sum()) if not features.empty else 0, "Feature definitions incorrectly depending only on L1"),
            ("phase131_cost_regime_rows", int(len(costs)), "Immutable cost regimes declared"),
            ("phase131_phase130_baseline_reference_rows", int(len(baseline)), "Phase130 baseline references for Phase132 ordering/lift checks"),
            ("phase131_allowed_context_rows", int(len(allowed_matrix)), "Allowed Phase129 contexts locked as Phase132 dataset"),
            ("phase131_brier_lift_margin", BASELINE_BRIER_MARGIN, "Minimum Brier lift over Phase130 baseline required in Phase132"),
            ("phase131_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase131_all_gates_pass", int(gates["gate_pass"].astype(bool).all()) if not gates.empty else 0, "1 means Phase131 precommit is self-consistent"),
            ("phase131_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase131_next_best_action", "run_phase132_deep_book_feature_diagnostics_or_stop_if_precommit_fails", "Recommended next milestone"),
            ("phase131_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha model retained unchanged"),
        ],
        columns=["metric", "value", "description"],
    )


def evaluation_rules_markdown() -> str:
    return "\n".join(
        [
            "# Phase131 Evaluation Rules",
            "",
            "These rules are immutable for Phases 132-136 of the deep-book passive branch.",
            "",
            "1. A feature or strategy clears only if it clears both cost regimes: `base` and `harsh`.",
            "2. No cost-stress ordering reversal is allowed. A candidate that ranks above the Phase130 L1/context baselines under `base` but falls below them under `harsh` is rejected as brittle.",
            "3. Positive-pockets exception is disallowed. Full-sample verdict under `harsh` decides the outcome.",
            "4. `strategy_replay_allowed` remains `0` throughout this plan unless separate real-anchor gates outside this plan unlock replay.",
            "5. Phase131 and Phase132 may emit feature diagnostics only. They may not emit strategy code, buy/sell signals, order-arrival streams, live-tagged fill models, P&L replay, or profitability claims.",
            "",
            f"Baseline comparison margin for Phase132: Brier improvement must be greater than `{BASELINE_BRIER_MARGIN}` versus the matching Phase130 selected diagnostic baseline.",
            f"Pinned cost model: `{PINNED_COST_MODEL_VERSION}`.",
            f"Allowed dataset: `{ALLOWED_DATASET}`.",
            "",
        ]
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase131 Deep-Book Feature and Cost-Stress Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase131 locks the deep-book feature catalog, base/harsh cost regimes, and evaluation rules before Phase132 diagnostics touch data.",
        "It emits specifications only and explicitly forbids strategy code, order simulation, P&L replay, and profitability claims.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase131_deep_book_feature_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase131(base_dir: Path, output_dir: Path, phase129_dir: Path, phase130_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    allowed_matrix = read_csv(base_dir / phase129_dir / "allowed_context_label_matrix.csv")
    phase130_selection = read_csv(base_dir / phase130_dir / "diagnostic_model_selection.csv")
    features = build_feature_catalog()
    costs = build_cost_regimes()
    baseline = build_baseline_reference(phase130_selection)
    guardrails = build_guardrails()
    gates = build_gate_evaluation(features, costs, baseline, allowed_matrix)
    acceptance = build_acceptance_summary(features, costs, baseline, gates, allowed_matrix)

    features.to_csv(output_dir / "phase131_feature_catalog.csv", index=False)
    costs.to_csv(output_dir / "phase131_cost_regimes.csv", index=False)
    baseline.to_csv(output_dir / "phase131_phase130_baseline_reference.csv", index=False)
    guardrails.to_csv(output_dir / "phase131_guardrails.csv", index=False)
    gates.to_csv(output_dir / "phase131_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase131_deep_book_feature_precommit_acceptance_summary.csv", index=False)
    (output_dir / "phase131_evaluation_rules.md").write_text(evaluation_rules_markdown(), encoding="utf-8")
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Feature Catalog": features,
            "Cost Regimes": costs,
            "Phase130 Baseline Reference": baseline,
            "Guardrails": guardrails,
            "Gate Evaluation": gates,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase131_deep_book_feature_and_cost_stress_precommit",
        "allowed_dataset": ALLOWED_DATASET,
        "feature_count": int(len(features)),
        "cost_regimes": costs["cost_regime_id"].astype(str).tolist(),
        "phase132_brier_lift_margin": BASELINE_BRIER_MARGIN,
        "strategy_replay_allowed": 0,
        "forbidden_outputs": FORBIDDEN_OUTPUTS,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase131",
            generated_utc=generated_utc,
            inputs={
                "phase129_label_matrix": str(phase129_dir / "allowed_context_label_matrix.csv"),
                "phase130_model_selection": str(phase130_dir / "diagnostic_model_selection.csv"),
                "continuation_plan": "Plan/Plan continuation2.txt",
            },
            parameters={
                "feature_scope": "requires_l2_l5_top5_depth",
                "cost_regimes": "base_and_harsh_immutable",
                "harsh_uplift": "1.25x_spread_cross_and_all_per_leg_fee_components",
                "phase132_model_family": "single_feature_threshold_and_two_feature_threshold_combos",
                "replay_policy": "closed",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "feature_catalog": str(output_dir / "phase131_feature_catalog.csv"),
                "cost_regimes": str(output_dir / "phase131_cost_regimes.csv"),
                "evaluation_rules": str(output_dir / "phase131_evaluation_rules.md"),
                "baseline_reference": str(output_dir / "phase131_phase130_baseline_reference.csv"),
                "guardrails": str(output_dir / "phase131_guardrails.csv"),
                "gates": str(output_dir / "phase131_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase131_deep_book_feature_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase131_deep_book_feature_precommit_report.md"),
                "manifest": str(output_dir / "phase131_precommit_manifest.json"),
            },
            random_seed="none_precommit_specification",
            scenario_ids="phase131_deep_book_passive_surface_precommit",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_precommit",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase131_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Precommit Phase131 deep-book L2-L5 feature catalog and cost-stress regimes.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--phase129-dir", type=Path, default=DEFAULT_PHASE129_DIR)
    parser.add_argument("--phase130-dir", type=Path, default=DEFAULT_PHASE130_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase131(base_dir=args.base_dir, output_dir=args.output_dir, phase129_dir=args.phase129_dir, phase130_dir=args.phase130_dir)


if __name__ == "__main__":
    main()

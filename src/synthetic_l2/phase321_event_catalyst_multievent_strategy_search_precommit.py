from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, charge_component_catalog


DEFAULT_PHASE320_DIR = Path("outputs/phase320")
DEFAULT_OUTPUT_DIR = Path("outputs/phase321")

NEXT_ACTION = "run_phase322_event_catalyst_multievent_strategy_search_training_only_no_replay"
REPAIR_ACTION = "repair_phase321_event_catalyst_multievent_strategy_search_precommit"


def build_strategy_family_catalog() -> pd.DataFrame:
    rows = [
        ("P321_DEPTH_PRESSURE_CONTINUATION", "sign(event_depth_l2_l5_pressure)", "event_depth_l2_l5_pressure", "target_post_300s_mid_return_bps;target_post_900s_mid_return_bps", 1, "Follow depth-beyond-L1 pressure after catalyst events."),
        ("P321_DEPTH_PRESSURE_REVERSAL", "-sign(event_depth_l2_l5_pressure)", "event_depth_l2_l5_pressure", "target_post_300s_mid_return_bps;target_post_900s_mid_return_bps", 1, "Fade depth-beyond-L1 pressure after catalyst events."),
        ("P321_DEPTH_ACCEL_CONTINUATION", "sign(event_depth_l2_l5_pressure - pre300_depth_l2_l5_pressure_avg)", "event_depth_l2_l5_pressure;pre300_depth_l2_l5_pressure_avg", "target_post_300s_mid_return_bps;target_post_900s_mid_return_bps", 1, "Follow event-time acceleration versus pre-event depth-beyond-L1 pressure."),
        ("P321_DEPTH_ACCEL_REVERSAL", "-sign(event_depth_l2_l5_pressure - pre300_depth_l2_l5_pressure_avg)", "event_depth_l2_l5_pressure;pre300_depth_l2_l5_pressure_avg", "target_post_300s_mid_return_bps;target_post_900s_mid_return_bps", 1, "Fade event-time acceleration versus pre-event depth-beyond-L1 pressure."),
        ("P321_QTY_IMBALANCE_CONTINUATION", "sign(event_depth_l2_l5_qty_imbalance)", "event_depth_l2_l5_qty_imbalance", "target_post_60s_mid_return_bps;target_post_300s_mid_return_bps", 1, "Follow depth levels 2-5 quantity imbalance."),
        ("P321_QTY_IMBALANCE_REVERSAL", "-sign(event_depth_l2_l5_qty_imbalance)", "event_depth_l2_l5_qty_imbalance", "target_post_60s_mid_return_bps;target_post_300s_mid_return_bps", 1, "Fade depth levels 2-5 quantity imbalance."),
        ("P321_ORDER_IMBALANCE_CONTINUATION", "sign(event_depth_l2_l5_order_imbalance)", "event_depth_l2_l5_order_imbalance", "target_post_60s_mid_return_bps;target_post_300s_mid_return_bps", 1, "Follow order-count imbalance across depth levels 2-5."),
        ("P321_ORDER_IMBALANCE_REVERSAL", "-sign(event_depth_l2_l5_order_imbalance)", "event_depth_l2_l5_order_imbalance", "target_post_60s_mid_return_bps;target_post_300s_mid_return_bps", 1, "Fade order-count imbalance across depth levels 2-5."),
        ("P321_MICROPRICE_DEPTH_CONFIRM", "sign(pre300_microprice_minus_mid_avg) when same sign as event_depth_l2_l5_qty_imbalance", "pre300_microprice_minus_mid_avg;event_depth_l2_l5_qty_imbalance", "target_post_60s_mid_return_bps;target_post_300s_mid_return_bps", 1, "Require top-of-book microprice and depth-beyond-L1 quantity imbalance to agree."),
        ("P321_DEPTH_PRESSURE_TARGET_SHIFT", "sign(pre300_depth_l2_l5_pressure_avg)", "pre300_depth_l2_l5_pressure_avg", "target_post_300s_depth_pressure_shift", 1, "Use pre-event depth pressure to predict subsequent liquidity-pressure shift."),
    ]
    return pd.DataFrame(rows, columns=["family_id", "signal_formula", "required_live_feature_columns", "target_columns", "uses_depth_beyond_l1", "description"])


def build_search_grid() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    horizons = [60, 300, 900, 1800]
    threshold_policies = ["top_10pct_abs_signal", "top_25pct_abs_signal", "top_50pct_abs_signal", "all_nonzero_signal"]
    cost_profiles = ["zerodha_base", "zerodha_plus_1bp_slippage", "zerodha_plus_2bp_slippage", "zerodha_2x_all_in_cost_proxy"]
    initial_capitals = [100_000, 250_000, 500_000]
    notionals = [25_000, 50_000, 75_000, 100_000]
    max_concurrency = [1, 2, 4]
    side_policies = ["long_short", "long_only", "short_only"]
    execution_policies = ["taker_entry_taker_exit", "passive_aware_directional_with_penalties"]
    for horizon in horizons:
        for threshold in threshold_policies:
            for cost_profile in cost_profiles:
                for capital in initial_capitals:
                    for notional in notionals:
                        for concurrency in max_concurrency:
                            for side_policy in side_policies:
                                for execution_policy in execution_policies:
                                    rows.append(
                                        {
                                            "horizon_seconds": horizon,
                                            "threshold_policy": threshold,
                                            "cost_profile": cost_profile,
                                            "initial_capital_inr": capital,
                                            "fixed_notional_inr": notional,
                                            "max_concurrent_positions": concurrency,
                                            "side_policy": side_policy,
                                            "execution_policy": execution_policy,
                                        }
                                    )
    return pd.DataFrame(rows)


def build_acceptance_contract() -> pd.DataFrame:
    rows = [
        ("fixed_capital_denominator", "required", "Annualized return must be net P&L divided by fixed initial capital; no unlimited-capital return."),
        ("annualized_research_lead_threshold_pct", "12.0", "Sparse >12% annualized is a research lead only, not acceptance."),
        ("cost200_profile_required", "zerodha_2x_all_in_cost_proxy", "Every candidate family must be scored under a 2x cost stress profile."),
        ("zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Use documented Zerodha equity intraday NSE charges."),
        ("minimum_scheduled_event_rows_for_acceptance", "30", "Below 30 scheduled events is sparse clue only."),
        ("minimum_symbol_date_breadth_for_acceptance", "2_symbols_x_2_dates_positive", "Avoid single-symbol/single-date pockets."),
        ("full_depth_required", "depth_levels_1_to_5", "Use top-five market-by-price depth."),
        ("depth_beyond_l1_required", "depth_levels_2_to_5_material", "No L1-only strategy candidates."),
        ("target_separation", "target_columns_prefixed_and_not_live_features", "No target column may be used as a live signal input."),
        ("net_edge_live_mask", "forbidden", "No lookahead net-edge live mask."),
        ("passive_fill_policy_if_used", "pessimistic_back_of_queue_fill_probability", "Passive-aware variants must include fill probability, not assumed fills."),
        ("adverse_selection_if_passive", "required", "Passive-aware variants must penalize filled passive orders for toxicity/adverse selection."),
        ("forced_flatten_if_passive", "required", "Any unfilled/unexited passive-aware inventory must pay taker flatten cost."),
        ("maker_rebate_assumption", "forbidden", "Retail maker rebate is not assumed."),
        ("phase321_execution_now", "forbidden", "Phase321 is precommit only; Phase322 may run training-only search."),
        ("paper_live_or_profitability_claim", "forbidden", "No paper/live/deployable claim from precommit or training search."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_phase322_work_order() -> pd.DataFrame:
    rows = [
        ("load_phase320_matrix", "outputs/phase320/phase320_event_catalyst_multievent_feature_matrix.csv", "Use the accepted compact matrix."),
        ("expand_family_grid", "family_catalog x search_grid", "Evaluate directional full-depth families only."),
        ("compute_signed_signals", "family-specific live feature formulas", "Use no target_ columns in signal construction."),
        ("score_targets", "target_post_{60,300,900,1800}s_mid_return_bps and target_post_300s_depth_pressure_shift", "Targets are outcomes only."),
        ("apply_zerodha_costs", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Apply brokerage, STT, transaction, GST, SEBI, stamp duty, and slippage/cost stress."),
        ("apply_fixed_capital_scheduler", "initial_capital, fixed_notional, max_concurrent_positions", "Reject unlimited-capital annual-return math."),
        ("apply_passive_aware_penalties", "fill_probability + adverse_selection + forced_flatten", "Only for passive-aware execution-policy rows."),
        ("write_training_search_outputs", "outputs/phase322", "Training-only search outputs; no replay/promotion."),
    ]
    return pd.DataFrame(rows, columns=["work_order_id", "scope", "description"])


def build_gate_evaluation(phase320: pd.DataFrame, families: pd.DataFrame, grid: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame) -> pd.DataFrame:
    phase320_complete = as_int(metric_value(phase320, "phase320_multievent_feature_materialization_complete", 0))
    depth_family_rows = int(families["uses_depth_beyond_l1"].astype(int).sum()) if not families.empty else 0
    cost200_rows = int(grid["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy").sum()) if not grid.empty else 0
    passive_rows = int(grid["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties").sum()) if not grid.empty else 0
    rows: list[tuple[str, bool, Any, Any]] = [
        ("P321_PHASE320_COMPLETE", phase320_complete == 1, phase320_complete, 1),
        ("P321_PHASE320_MATRIX_BREADTH", as_int(metric_value(phase320, "phase320_feature_matrix_rows", 0)) == 320, metric_value(phase320, "phase320_feature_matrix_rows", ""), 320),
        ("P321_PHASE320_TARGET_SEPARATION", as_int(metric_value(phase320, "phase320_target_columns_used_as_live_features", 1)) == 0, metric_value(phase320, "phase320_target_columns_used_as_live_features", ""), 0),
        ("P321_FAMILY_CATALOG_PRESENT", len(families) >= 10, len(families), ">=10"),
        ("P321_ALL_FAMILIES_USE_DEPTH_BEYOND_L1", depth_family_rows == len(families) and len(families) > 0, f"{depth_family_rows}/{len(families)}", "all"),
        ("P321_SEARCH_GRID_PRESENT", len(grid) > 0, len(grid), ">0"),
        ("P321_COST200_PRESENT", cost200_rows > 0, cost200_rows, ">0"),
        ("P321_PASSIVE_AWARE_ROWS_PRESENT", passive_rows > 0, passive_rows, ">0"),
        ("P321_FIXED_CAPITAL_PRESENT", contract["contract_id"].astype(str).eq("fixed_capital_denominator").any(), "present", "present"),
        ("P321_PASSIVE_REALISM_PENALTIES_PRESENT", {"passive_fill_policy_if_used", "adverse_selection_if_passive", "forced_flatten_if_passive"}.issubset(set(contract["contract_id"].astype(str))), "fill+adverse+flatten", "present"),
        ("P321_WORK_ORDER_PRESENT", len(work_order) >= 8, len(work_order), ">=8"),
        ("P321_NO_STRATEGY_SEARCH_EXECUTED_NOW", True, "phase321_execution_now=0", 0),
        ("P321_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(families: pd.DataFrame, grid: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    return pd.DataFrame(
        [
            ("phase321_multievent_strategy_search_precommit_complete", complete, "Phase321 multi-event strategy search precommit completed"),
            ("phase321_strategy_family_rows", int(len(families)), "Strategy family rows"),
            ("phase321_depth_beyond_l1_family_rows", int(families["uses_depth_beyond_l1"].astype(int).sum()) if not families.empty else 0, "Families using depth levels 2-5"),
            ("phase321_search_grid_rows", int(len(grid)), "Search grid rows before family expansion"),
            ("phase321_expanded_variant_upper_bound_rows", int(len(families) * len(grid)), "Family x grid upper bound"),
            ("phase321_cost200_grid_rows", int(grid["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy").sum()) if not grid.empty else 0, "2x cost-stress grid rows"),
            ("phase321_passive_aware_grid_rows", int(grid["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties").sum()) if not grid.empty else 0, "Passive-aware execution grid rows"),
            ("phase321_acceptance_contract_rows", int(len(contract)), "Acceptance contract rows"),
            ("phase321_work_order_rows", int(len(work_order)), "Phase322 work-order rows"),
            ("phase321_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha cost model version"),
            ("phase321_full_depth_required", 1, "Depth levels 1-5 required"),
            ("phase321_depth_beyond_l1_required", 1, "Depth levels 2-5 materiality required"),
            ("phase321_l1_only_candidate_allowed", 0, "L1-only candidate path closed"),
            ("phase321_net_edge_live_mask_rows_allowed", 0, "No net-edge live lookahead mask allowed"),
            ("phase321_fixed_capital_required", 1, "Fixed initial capital denominator required"),
            ("phase321_cost200_required", 1, "2x cost stress required"),
            ("phase321_passive_realism_penalties_required", 1, "Fill probability, adverse selection and forced flatten required for passive-aware rows"),
            ("phase321_strategy_search_execution_allowed_next", 1 if complete else 0, "Phase322 training-only search may run if gates pass"),
            ("phase321_strategy_replay_allowed", 0, "No replay"),
            ("phase321_strategy_promotion_allowed", 0, "No promotion"),
            ("phase321_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase321_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase321_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase321_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase321_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase321 Event-Catalyst Multi-Event Strategy Search Precommit",
        "",
        "Phase321 precommits the training-only strategy search over the Phase320 multi-event top-five-depth feature matrix.",
        "It includes the attached passive-aware execution realism constraints as execution-policy boundaries, but does not reopen the older Phase300 route.",
        "It does not execute strategy search, replay, promote, open paper/live acceptance, or claim profitability.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase321_event_catalyst_multievent_strategy_search_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase320_dir: Path = DEFAULT_PHASE320_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase320 = read_csv(phase320_dir / "phase320_acceptance_summary.csv")
    families = build_strategy_family_catalog()
    grid = build_search_grid()
    contract = build_acceptance_contract()
    work_order = build_phase322_work_order()
    costs = charge_component_catalog()
    gates = build_gate_evaluation(phase320, families, grid, contract, work_order)
    acceptance = build_acceptance(families, grid, contract, work_order, gates)

    families.to_csv(output_dir / "phase321_strategy_family_catalog.csv", index=False)
    grid.to_csv(output_dir / "phase321_strategy_search_grid.csv", index=False)
    contract.to_csv(output_dir / "phase321_acceptance_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase321_phase322_work_order.csv", index=False)
    costs.to_csv(output_dir / "phase321_zerodha_cost_component_catalog.csv", index=False)
    gates.to_csv(output_dir / "phase321_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase321_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        acceptance,
        {
            "Strategy family catalog": families,
            "Search grid preview": grid.head(80),
            "Acceptance contract": contract,
            "Phase322 work order": work_order,
            "Zerodha cost component catalog": costs,
            "Gates": gates,
        },
    )

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase321_event_catalyst_multievent_strategy_search_precommit",
        **reproducibility_fields(
            artifact_id="phase321",
            generated_utc=generated_utc,
            inputs={"phase320_acceptance": str(phase320_dir / "phase320_acceptance_summary.csv")},
            parameters={"zerodha_cost_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "no_strategy_search_now": 1},
            outputs={"acceptance_summary": str(output_dir / "phase321_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_precommit_only",
        ),
    }
    (output_dir / "phase321_event_catalyst_multievent_strategy_search_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase321 multi-event strategy search.")
    parser.add_argument("--phase320-dir", type=Path, default=DEFAULT_PHASE320_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase320_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

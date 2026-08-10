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


DEFAULT_PHASE330_DIR = Path("outputs/phase330")
DEFAULT_OUTPUT_DIR = Path("outputs/phase331")

NEXT_ACTION = "run_phase332_event_catalyst_expanded_strategy_search_training_only_no_replay"
REPAIR_ACTION = "repair_phase331_event_catalyst_expanded_strategy_search_precommit"


def build_strategy_family_catalog() -> pd.DataFrame:
    rows = [
        ("P331_DEPTH_PRESSURE_CONTINUATION", "sign(event_depth_l2_l5_pressure)", "event_depth_l2_l5_pressure", "target_post_300s_mid_return_bps;target_post_900s_mid_return_bps", 1, "Follow depth-beyond-L1 pressure after catalyst events."),
        ("P331_DEPTH_PRESSURE_REVERSAL", "-sign(event_depth_l2_l5_pressure)", "event_depth_l2_l5_pressure", "target_post_300s_mid_return_bps;target_post_900s_mid_return_bps", 1, "Fade depth-beyond-L1 pressure after catalyst events."),
        ("P331_DEPTH_ACCEL_CONTINUATION", "sign(event_depth_l2_l5_pressure - pre300_depth_l2_l5_pressure_avg)", "event_depth_l2_l5_pressure;pre300_depth_l2_l5_pressure_avg", "target_post_300s_mid_return_bps;target_post_900s_mid_return_bps", 1, "Follow event-time acceleration versus pre-event depth-beyond-L1 pressure."),
        ("P331_DEPTH_ACCEL_REVERSAL", "-sign(event_depth_l2_l5_pressure - pre300_depth_l2_l5_pressure_avg)", "event_depth_l2_l5_pressure;pre300_depth_l2_l5_pressure_avg", "target_post_300s_mid_return_bps;target_post_900s_mid_return_bps", 1, "Fade event-time acceleration versus pre-event depth-beyond-L1 pressure."),
        ("P331_QTY_IMBALANCE_CONTINUATION", "sign(event_depth_l2_l5_qty_imbalance)", "event_depth_l2_l5_qty_imbalance", "target_post_60s_mid_return_bps;target_post_300s_mid_return_bps", 1, "Follow levels 2-5 quantity imbalance."),
        ("P331_QTY_IMBALANCE_REVERSAL", "-sign(event_depth_l2_l5_qty_imbalance)", "event_depth_l2_l5_qty_imbalance", "target_post_60s_mid_return_bps;target_post_300s_mid_return_bps", 1, "Fade levels 2-5 quantity imbalance."),
        ("P331_ORDER_IMBALANCE_CONTINUATION", "sign(event_depth_l2_l5_order_imbalance)", "event_depth_l2_l5_order_imbalance", "target_post_60s_mid_return_bps;target_post_300s_mid_return_bps", 1, "Follow order-count imbalance across levels 2-5."),
        ("P331_ORDER_IMBALANCE_REVERSAL", "-sign(event_depth_l2_l5_order_imbalance)", "event_depth_l2_l5_order_imbalance", "target_post_60s_mid_return_bps;target_post_300s_mid_return_bps", 1, "Fade order-count imbalance across levels 2-5."),
        ("P331_MICROPRICE_DEPTH_CONFIRM", "sign(pre300_microprice_minus_mid_avg) when same sign as event_depth_l2_l5_qty_imbalance", "pre300_microprice_minus_mid_avg;event_depth_l2_l5_qty_imbalance", "target_post_60s_mid_return_bps;target_post_300s_mid_return_bps", 1, "Require top-of-book microprice and depth-beyond-L1 quantity imbalance to agree."),
        ("P331_PRE900_TO_EVENT_PRESSURE_SHIFT", "sign(event_depth_l2_l5_pressure - pre900_depth_l2_l5_pressure_avg)", "event_depth_l2_l5_pressure;pre900_depth_l2_l5_pressure_avg", "target_post_300s_mid_return_bps;target_post_1800s_mid_return_bps", 1, "Trade pressure shifts from long pre-event context into event time."),
        ("P331_DEPTH_SHARE_COMPRESSION_REVERSAL", "-sign(event_l2_l5_depth_share - pre300_l2_l5_depth_share_avg)", "event_l2_l5_depth_share;pre300_l2_l5_depth_share_avg", "target_post_300s_mid_return_bps;target_post_900s_mid_return_bps", 1, "Fade sudden displayed-depth compression beyond L1."),
        ("P331_DEPTH_SHARE_EXPANSION_CONTINUATION", "sign(event_l2_l5_depth_share - pre300_l2_l5_depth_share_avg)", "event_l2_l5_depth_share;pre300_l2_l5_depth_share_avg", "target_post_300s_mid_return_bps;target_post_900s_mid_return_bps", 1, "Follow sudden displayed-depth expansion beyond L1."),
        ("P331_SPREAD_ADJUSTED_PRESSURE_CONTINUATION", "sign(event_depth_pressure)", "event_depth_pressure;event_l1_spread", "target_post_60s_mid_return_bps;target_post_300s_mid_return_bps", 1, "Follow spread-adjusted full visible-depth pressure."),
        ("P331_SPREAD_ADJUSTED_PRESSURE_REVERSAL", "-sign(event_depth_pressure)", "event_depth_pressure;event_l1_spread", "target_post_60s_mid_return_bps;target_post_300s_mid_return_bps", 1, "Fade spread-adjusted full visible-depth pressure."),
        ("P331_DEPTH_PRESSURE_TARGET_SHIFT", "sign(pre300_depth_l2_l5_pressure_avg)", "pre300_depth_l2_l5_pressure_avg", "target_post_300s_depth_pressure_shift", 1, "Use pre-event L2-L5 pressure to predict subsequent liquidity-pressure shift."),
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
    event_buckets = ["all_events", "preopen_gap_events", "earnings_like_events", "macro_or_index_context", "liquidity_shock_context"]
    for horizon in horizons:
        for threshold in threshold_policies:
            for cost_profile in cost_profiles:
                for capital in initial_capitals:
                    for notional in notionals:
                        for concurrency in max_concurrency:
                            for side_policy in side_policies:
                                for execution_policy in execution_policies:
                                    for event_bucket in event_buckets:
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
                                                "event_bucket_policy": event_bucket,
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
        ("full_depth_required", "zerodha_visible_depth_levels_1_to_5", "Use top-five market-by-price depth."),
        ("depth_beyond_l1_required", "depth_levels_2_to_5_material", "No L1-only strategy candidates."),
        ("target_separation", "target_columns_prefixed_and_not_live_features", "No target column may be used as a live signal input."),
        ("net_edge_live_mask", "forbidden", "No lookahead net-edge live mask."),
        ("passive_fill_policy_if_used", "pessimistic_back_of_queue_fill_probability", "Passive-aware variants must include fill probability, not assumed fills."),
        ("adverse_selection_if_passive", "required", "Passive-aware variants must penalize filled passive orders for toxicity/adverse selection."),
        ("forced_flatten_if_passive", "required", "Any unfilled/unexited passive-aware inventory must pay taker flatten cost."),
        ("maker_rebate_assumption", "forbidden", "Retail maker rebate is not assumed."),
        ("phase331_execution_now", "forbidden", "Phase331 is precommit only; Phase332 may run training-only search."),
        ("strategy_replay_allowed", "forbidden", "No replay opens from Phase331."),
        ("paper_live_or_profitability_claim", "forbidden", "No paper/live/deployable claim from precommit or training search."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_phase332_work_order() -> pd.DataFrame:
    rows = [
        ("load_phase330_matrix", "outputs/phase330/phase330_event_catalyst_expanded_feature_matrix.parquet", "Use the accepted compact expanded matrix."),
        ("expand_family_grid", "family_catalog x search_grid", "Evaluate directional full-depth families only."),
        ("compute_signed_signals", "family-specific live feature formulas", "Use no target_ columns in signal construction."),
        ("score_targets", "target_post_{60,300,900,1800}s_mid_return_bps and target_post_300s_depth_pressure_shift", "Targets are outcomes only."),
        ("apply_event_bucket_policy", "event_bucket_policy", "Bucket policies must be observable context labels, not target/net-edge filters."),
        ("apply_zerodha_costs", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Apply brokerage, STT, transaction, GST, SEBI, stamp duty, and slippage/cost stress."),
        ("apply_fixed_capital_scheduler", "initial_capital, fixed_notional, max_concurrent_positions", "Reject unlimited-capital annual-return math."),
        ("apply_passive_aware_penalties", "fill_probability + adverse_selection + forced_flatten", "Only for passive-aware execution-policy rows."),
        ("apply_controls", "side_flip + random_side + shuffled_label + no_l1_only + no_net_edge_mask", "Controls decide whether a clue is meaningful."),
        ("write_training_search_outputs", "outputs/phase332", "Training-only search outputs; no replay/promotion/paper-live."),
    ]
    return pd.DataFrame(rows, columns=["work_order_id", "scope", "description"])


def build_gate_evaluation(phase330: pd.DataFrame, families: pd.DataFrame, grid: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame) -> pd.DataFrame:
    phase330_complete = as_int(metric_value(phase330, "phase330_expanded_feature_materialization_complete", 0))
    depth_family_rows = int(families["uses_depth_beyond_l1"].astype(int).sum()) if not families.empty else 0
    cost200_rows = int(grid["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy").sum()) if not grid.empty else 0
    passive_rows = int(grid["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties").sum()) if not grid.empty else 0
    rows: list[tuple[str, bool, Any, Any]] = [
        ("P331_PHASE330_COMPLETE", phase330_complete == 1, phase330_complete, 1),
        ("P331_PHASE330_MATRIX_BREADTH", as_int(metric_value(phase330, "phase330_feature_matrix_rows", 0)) == 1600, metric_value(phase330, "phase330_feature_matrix_rows", ""), 1600),
        ("P331_PHASE330_TARGET_SEPARATION", as_int(metric_value(phase330, "phase330_target_columns_used_as_live_features", 1)) == 0, metric_value(phase330, "phase330_target_columns_used_as_live_features", ""), 0),
        ("P331_PHASE330_DEPTH_COLUMNS_PRESENT", as_int(metric_value(phase330, "phase330_depth_feature_columns", 0)) >= 20, metric_value(phase330, "phase330_depth_feature_columns", ""), ">=20"),
        ("P331_FAMILY_CATALOG_PRESENT", len(families) >= 15, len(families), ">=15"),
        ("P331_ALL_FAMILIES_USE_DEPTH_BEYOND_L1", depth_family_rows == len(families) and len(families) > 0, f"{depth_family_rows}/{len(families)}", "all"),
        ("P331_SEARCH_GRID_PRESENT", len(grid) > 0, len(grid), ">0"),
        ("P331_COST200_PRESENT", cost200_rows > 0, cost200_rows, ">0"),
        ("P331_PASSIVE_AWARE_ROWS_PRESENT", passive_rows > 0, passive_rows, ">0"),
        ("P331_FIXED_CAPITAL_PRESENT", contract["contract_id"].astype(str).eq("fixed_capital_denominator").any(), "present", "present"),
        ("P331_PASSIVE_REALISM_PENALTIES_PRESENT", {"passive_fill_policy_if_used", "adverse_selection_if_passive", "forced_flatten_if_passive"}.issubset(set(contract["contract_id"].astype(str))), "fill+adverse+flatten", "present"),
        ("P331_WORK_ORDER_PRESENT", len(work_order) >= 10, len(work_order), ">=10"),
        ("P331_NO_STRATEGY_SEARCH_EXECUTED_NOW", True, "phase331_execution_now=0", 0),
        ("P331_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(families: pd.DataFrame, grid: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    return pd.DataFrame(
        [
            ("phase331_expanded_strategy_search_precommit_complete", complete, "Phase331 expanded strategy search precommit completed"),
            ("phase331_strategy_family_rows", int(len(families)), "Strategy family rows"),
            ("phase331_depth_beyond_l1_family_rows", int(families["uses_depth_beyond_l1"].astype(int).sum()) if not families.empty else 0, "Families using depth levels 2-5"),
            ("phase331_search_grid_rows", int(len(grid)), "Search grid rows before family expansion"),
            ("phase331_expanded_variant_upper_bound_rows", int(len(families) * len(grid)), "Family x grid upper bound"),
            ("phase331_cost200_grid_rows", int(grid["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy").sum()) if not grid.empty else 0, "2x cost-stress grid rows"),
            ("phase331_passive_aware_grid_rows", int(grid["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties").sum()) if not grid.empty else 0, "Passive-aware execution grid rows"),
            ("phase331_event_bucket_policy_rows", int(grid["event_bucket_policy"].nunique()) if not grid.empty else 0, "Observable event-bucket policies"),
            ("phase331_acceptance_contract_rows", int(len(contract)), "Acceptance contract rows"),
            ("phase331_work_order_rows", int(len(work_order)), "Phase332 work-order rows"),
            ("phase331_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha cost model version"),
            ("phase331_full_depth_required", 1, "Depth levels 1-5 required"),
            ("phase331_depth_beyond_l1_required", 1, "Depth levels 2-5 materiality required"),
            ("phase331_l1_only_candidate_allowed", 0, "L1-only candidate path closed"),
            ("phase331_net_edge_live_mask_rows_allowed", 0, "No net-edge live lookahead mask allowed"),
            ("phase331_fixed_capital_required", 1, "Fixed initial capital denominator required"),
            ("phase331_cost200_required", 1, "2x cost stress required"),
            ("phase331_passive_realism_penalties_required", 1, "Fill probability, adverse selection and forced flatten required for passive-aware rows"),
            ("phase331_strategy_search_execution_allowed_next", 1 if complete else 0, "Phase332 training-only search may run if gates pass"),
            ("phase331_strategy_replay_allowed", 0, "No replay"),
            ("phase331_strategy_promotion_allowed", 0, "No promotion"),
            ("phase331_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase331_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase331_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase331_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase331_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase331 Event-Catalyst Expanded Strategy Search Precommit",
        "",
        "Phase331 precommits the training-only strategy search over the Phase330 expanded top-five-depth feature matrix.",
        "It carries the attached passive-aware execution realism constraints as execution-policy boundaries without reopening the already-falsified Phase300 passive-aware route.",
        "It does not execute strategy search, replay, promote, open paper/live acceptance, or claim profitability.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase331_event_catalyst_expanded_strategy_search_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase330_dir: Path = DEFAULT_PHASE330_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase330 = read_csv(phase330_dir / "phase330_acceptance_summary.csv")
    families = build_strategy_family_catalog()
    grid = build_search_grid()
    contract = build_acceptance_contract()
    work_order = build_phase332_work_order()
    costs = charge_component_catalog()
    gates = build_gate_evaluation(phase330, families, grid, contract, work_order)
    acceptance = build_acceptance(families, grid, contract, work_order, gates)

    families.to_csv(output_dir / "phase331_strategy_family_catalog.csv", index=False)
    grid.to_csv(output_dir / "phase331_strategy_search_grid.csv", index=False)
    contract.to_csv(output_dir / "phase331_acceptance_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase331_phase332_work_order.csv", index=False)
    costs.to_csv(output_dir / "phase331_zerodha_cost_component_catalog.csv", index=False)
    gates.to_csv(output_dir / "phase331_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase331_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        acceptance,
        {
            "Strategy family catalog": families,
            "Search grid preview": grid.head(80),
            "Acceptance contract": contract,
            "Phase332 work order": work_order,
            "Zerodha cost component catalog": costs,
            "Gates": gates,
        },
    )

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase331_event_catalyst_expanded_strategy_search_precommit",
        **reproducibility_fields(
            artifact_id="phase331",
            generated_utc=generated_utc,
            inputs={"phase330_acceptance": str(phase330_dir / "phase330_acceptance_summary.csv")},
            parameters={"zerodha_cost_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "no_strategy_search_now": 1, "expanded_feature_rows": 1600},
            outputs={"acceptance_summary": str(output_dir / "phase331_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_precommit_only",
        ),
    }
    (output_dir / "phase331_event_catalyst_expanded_strategy_search_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase331 expanded strategy search.")
    parser.add_argument("--phase330-dir", type=Path, default=DEFAULT_PHASE330_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase330_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

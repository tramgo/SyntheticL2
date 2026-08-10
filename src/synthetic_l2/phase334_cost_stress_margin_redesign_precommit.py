from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE332_DIR = Path("outputs/phase332")
DEFAULT_PHASE333_DIR = Path("outputs/phase333")
DEFAULT_OUTPUT_DIR = Path("outputs/phase334")

NEXT_ACTION = "run_phase335_cost_stress_margin_redesign_training_only_no_replay"
REPAIR_ACTION = "repair_phase334_cost_stress_margin_redesign_precommit"

ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30


def build_design_lanes() -> pd.DataFrame:
    rows = [
        {
            "lane_id": "P334_LANE_A_STRICTER_DEPTH_ACCEL_EDGE",
            "preserved_family": "P331_DEPTH_ACCEL_REVERSAL",
            "hypothesis": "The 2x-cost miss is small enough that stricter live depth-acceleration reversal entries may lift average edge per trade above the cost-stress hurdle.",
            "allowed_live_filters": "abs_depth_accel_quantile>=0.95; spread_bps<=recent_median; depth_l1_l5_qty_share_bidask_material",
            "forbidden_filters": "future_return; net_edge; target; realized_pnl; post_entry_outcome",
            "cost_stress_required": 1,
            "full_depth_required": 1,
            "levels_2_to_5_required": 1,
            "passive_diagnostic_required": 1,
            "primary_execution_policy": "taker_entry_taker_exit",
        },
        {
            "lane_id": "P334_LANE_B_TURNOVER_COMPRESSION",
            "preserved_family": "P331_DEPTH_ACCEL_REVERSAL",
            "hypothesis": "Reduce cost drag by allowing only the strongest one or two symbols per event while preserving at least 30 scheduled events.",
            "allowed_live_filters": "rank_abs_signal_within_event<=1_or_2; event_bucket=all_or_macro; max_trade_rows_per_event_cap",
            "forbidden_filters": "sort_by_future_pnl; sort_by_target_return; realized_winner_selection",
            "cost_stress_required": 1,
            "full_depth_required": 1,
            "levels_2_to_5_required": 1,
            "passive_diagnostic_required": 1,
            "primary_execution_policy": "taker_entry_taker_exit",
        },
        {
            "lane_id": "P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN",
            "preserved_family": "P331_DEPTH_ACCEL_REVERSAL",
            "hypothesis": "The 0.482445937 percentage-point gap may close if trades avoid wide-spread/weak-book states using only live top-five depth quality.",
            "allowed_live_filters": "spread_bps_quantile<=0.50; top5_notional_depth_quantile>=0.50; order_count_imbalance_l1_l5_material",
            "forbidden_filters": "post_trade_slippage; fill_success_after_entry; realized_exit_quality",
            "cost_stress_required": 1,
            "full_depth_required": 1,
            "levels_2_to_5_required": 1,
            "passive_diagnostic_required": 1,
            "primary_execution_policy": "taker_entry_taker_exit",
        },
        {
            "lane_id": "P334_LANE_D_HORIZON_AND_EXIT_MARGIN",
            "preserved_family": "P331_DEPTH_ACCEL_REVERSAL",
            "hypothesis": "Cost-stress margin may improve by testing nearby exit horizons and forced-flat timing around the 900-second near miss without looking at future labels during signal formation.",
            "allowed_live_filters": "horizon_seconds in 600,900,1200,1500; no_new_target_columns_as_features; fixed_event_scheduler",
            "forbidden_filters": "choose_horizon_per_event_from_realized_pnl; use_future_return_as_mask",
            "cost_stress_required": 1,
            "full_depth_required": 1,
            "levels_2_to_5_required": 1,
            "passive_diagnostic_required": 1,
            "primary_execution_policy": "taker_entry_taker_exit",
        },
    ]
    return pd.DataFrame(rows)


def build_search_contract() -> pd.DataFrame:
    rows = [
        ("input_matrix", "outputs/phase330/phase330_feature_matrix.parquet", "Use the existing expanded full-depth event feature matrix."),
        ("scenario_source", "outputs/phase332/phase332_scenario_summary.parquet", "Use Phase332 only for precommitted clue selection and diagnostic comparison."),
        ("preserved_family", "P331_DEPTH_ACCEL_REVERSAL", "Only redesign around the Phase333-preserved family."),
        ("annualized_threshold_pct", ANNUALIZED_THRESHOLD_PCT, "Do not lower the user profitability threshold."),
        ("cost_profile_required", "zerodha_2x_all_in_cost_proxy", "Acceptance diagnostics require 2x Zerodha all-in cost stress."),
        ("robust_event_floor", ROBUST_EVENT_FLOOR, "Acceptance-grade diagnostics require at least 30 scheduled events."),
        ("fixed_capital_denominator", "required", "Annualized return must use fixed initial capital."),
        ("full_depth_top5_required", 1, "Use top-five market-by-price depth and features using levels beyond L1."),
        ("l1_only_allowed", 0, "No L1-only strategy variant is allowed."),
        ("net_edge_live_mask_allowed", 0, "No future outcome or net-edge live masks are allowed."),
        ("passive_aware_policy", "diagnostic_required_not_primary_rescue", "Passive-aware fill/adverse-selection/forced-flatten penalties remain in diagnostics."),
        ("strategy_replay_allowed", 0, "Phase334 is precommit only."),
        ("paper_or_live_allowed", 0, "No paper/live acceptance opens here."),
        ("profitability_claim_allowed", 0, "No deployable profitability claim opens here."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_phase335_work_order(design_lanes: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, lane in design_lanes.iterrows():
        rows.extend(
            [
                {
                    "work_order_id": f"{lane['lane_id']}_GRID",
                    "lane_id": lane["lane_id"],
                    "action": "build_training_only_redesign_grid",
                    "requirements": "cost200 required; fixed capital; full top-five depth; no future masks",
                },
                {
                    "work_order_id": f"{lane['lane_id']}_CONTROLS",
                    "lane_id": lane["lane_id"],
                    "action": "attach_controls",
                    "requirements": "side flip; random side; family-neutral broadness; passive-aware diagnostic",
                },
            ]
        )
    rows.append(
        {
            "work_order_id": "P334_ACCEPTANCE_AND_REPORTING",
            "lane_id": "all",
            "action": "write_phase335_outputs",
            "requirements": "scenario surface; top candidates; cost200 above12 count; acceptance-grade count; no replay claim",
        }
    )
    return pd.DataFrame(rows)


def build_gate_evaluation(phase332: pd.DataFrame, phase333: pd.DataFrame, design_lanes: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame) -> pd.DataFrame:
    phase333_complete = as_int(metric_value(phase333, "phase333_event_catalyst_expanded_strategy_search_interpretation_complete", 0))
    near_miss = as_int(metric_value(phase333, "phase333_best_cost200_near_miss_preserved", 0))
    cost200_passed = as_int(metric_value(phase333, "phase333_cost200_profitability_bar_passed", 1))
    replay = as_int(metric_value(phase333, "phase333_replay_allowed", 1))
    claim = as_int(metric_value(phase333, "phase333_deployable_profitability_claim_allowed", 1))
    best_cost200 = float(metric_value(phase332, "phase332_best_cost200_annualized_return_pct", 0) or 0)
    rows = [
        ("P334_PHASE333_COMPLETE", phase333_complete == 1, phase333_complete, 1),
        ("P334_NEAR_MISS_PRESERVED", near_miss == 1, near_miss, 1),
        ("P334_COST200_NOT_ALREADY_ACCEPTED", cost200_passed == 0, cost200_passed, 0),
        ("P334_BEST_COST200_WITHIN_REDESIGN_RANGE", 10.0 <= best_cost200 < ANNUALIZED_THRESHOLD_PCT, best_cost200, ">=10 and <12"),
        ("P334_DESIGN_LANES_PRESENT", len(design_lanes) >= 4, len(design_lanes), ">=4"),
        ("P334_CONTRACT_ROWS_PRESENT", len(contract) >= 12, len(contract), ">=12"),
        ("P334_WORK_ORDER_PRESENT", len(work_order) >= 9, len(work_order), ">=9"),
        ("P334_FULL_DEPTH_REQUIRED", int(design_lanes["full_depth_required"].astype(int).min()) == 1, "all", "all=1"),
        ("P334_LEVELS_2_TO_5_REQUIRED", int(design_lanes["levels_2_to_5_required"].astype(int).min()) == 1, "all", "all=1"),
        ("P334_NO_REPLAY_OR_CLAIM", replay == 0 and claim == 0, f"replay={replay};claim={claim}", "both_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(design_lanes: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame, phase332: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase334_cost_stress_margin_redesign_precommit_complete", int(hard_pass == hard_rows), "Phase334 precommit completed"),
            ("phase334_preserved_family", "P331_DEPTH_ACCEL_REVERSAL", "Family preserved from Phase333"),
            ("phase334_design_lane_rows", len(design_lanes), "Design lanes"),
            ("phase334_search_contract_rows", len(contract), "Search contract rows"),
            ("phase334_phase335_work_order_rows", len(work_order), "Phase335 work-order rows"),
            ("phase334_best_cost200_prior_annualized_return_pct", metric_value(phase332, "phase332_best_cost200_annualized_return_pct", ""), "Prior best 2x-cost annualized return"),
            ("phase334_required_annualized_threshold_pct", ANNUALIZED_THRESHOLD_PCT, "Required annualized threshold"),
            ("phase334_required_cost_profile", "zerodha_2x_all_in_cost_proxy", "Required cost profile"),
            ("phase334_full_depth_required", 1, "Full top-five depth required"),
            ("phase334_levels_2_to_5_required", 1, "Levels 2-5 materiality required"),
            ("phase334_l1_only_allowed", 0, "No L1-only variants"),
            ("phase334_net_edge_live_mask_allowed", 0, "No net-edge/future-outcome live masks"),
            ("phase334_strategy_replay_allowed", 0, "No replay"),
            ("phase334_strategy_promotion_allowed", 0, "No promotion"),
            ("phase334_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase334_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase334_strategy_search_execution_allowed_next", int(hard_pass == hard_rows), "Phase335 training-only execution allowed next"),
            ("phase334_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase334_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase334_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase334 Cost-Stress Margin Redesign Precommit",
        "",
        "Phase334 precommits a narrow redesign around the Phase333-preserved depth-acceleration reversal near miss.",
        "It is not a replay, promotion, paper/live gate, or profitability claim.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase334_cost_stress_margin_redesign_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase332_dir: Path = DEFAULT_PHASE332_DIR, phase333_dir: Path = DEFAULT_PHASE333_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase332 = read_csv(phase332_dir / "phase332_acceptance_summary.csv")
    phase333 = read_csv(phase333_dir / "phase333_acceptance_summary.csv")
    design_lanes = build_design_lanes()
    contract = build_search_contract()
    work_order = build_phase335_work_order(design_lanes)
    gates = build_gate_evaluation(phase332, phase333, design_lanes, contract, work_order)
    acceptance = build_acceptance(design_lanes, contract, work_order, gates, phase332)

    design_lanes.to_csv(output_dir / "phase334_design_lanes.csv", index=False)
    contract.to_csv(output_dir / "phase334_search_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase334_phase335_work_order.csv", index=False)
    gates.to_csv(output_dir / "phase334_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase334_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        acceptance,
        {
            "Design lanes": design_lanes,
            "Search contract": contract,
            "Phase335 work order": work_order,
            "Gates": gates,
        },
    )

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase334_cost_stress_margin_redesign_precommit",
        **reproducibility_fields(
            artifact_id="phase334",
            generated_utc=generated_utc,
            inputs={
                "phase332_acceptance": str(phase332_dir / "phase332_acceptance_summary.csv"),
                "phase333_acceptance": str(phase333_dir / "phase333_acceptance_summary.csv"),
            },
            parameters={"annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT, "robust_event_floor": ROBUST_EVENT_FLOOR},
            outputs={"acceptance_summary": str(output_dir / "phase334_acceptance_summary.csv")},
            cost_model_version="inherits_phase332_zerodha_cost_profiles",
            latency_model_version="not_applicable_precommit_only",
        ),
    }
    (output_dir / "phase334_cost_stress_margin_redesign_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Precommit Phase334 cost-stress margin redesign.")
    parser.add_argument("--phase332-dir", type=Path, default=DEFAULT_PHASE332_DIR)
    parser.add_argument("--phase333-dir", type=Path, default=DEFAULT_PHASE333_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase332_dir, args.phase333_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

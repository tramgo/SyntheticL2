from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase424_queue_depletion_continuation_precommit import SYMBOLS
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE298_DIR = Path("outputs/phase298")
DEFAULT_PHASE426_DIR = Path("outputs/phase426")
DEFAULT_OUTPUT_DIR = Path("outputs/phase427")

THESIS_ID = "P427_BROADER_FULL_DEPTH_FEATURE_FAMILY_SWEEP"
NEXT_ACTION = "run_phase428_broader_full_depth_feature_family_sweep_no_paper_live"
REPAIR_ACTION = "repair_phase427_broader_full_depth_feature_family_precommit"

FEATURE_FAMILIES = [
    ("depth_pressure_continuation", "top5_and_l2_l5_imbalance_align_with_last_price_microtrend"),
    ("depth_pressure_reversal", "top5_and_l2_l5_imbalance_opposes_last_price_microtrend"),
    ("spread_compression_breakout", "spread_contracts_while_l2_l5_same_side_replenishes"),
    ("spread_expansion_fade", "spread_expands_while_opposite_l2_l5_absorbs"),
    ("queue_churn_followthrough", "order_count_churn_and_depth_replacement_align_with_direction"),
    ("book_slope_migration", "weighted_depth_slope_migrates_from_far_levels_to_l1"),
]
LOOKBACK_TICKS = [60, 180, 360]
FORWARD_TICKS = [3, 6, 12]
MIN_FORWARD_HOLD_MS = 250.0
MAX_HOLD_TICKS = 60
SPREAD_BPS_BUCKETS = [4.0, 8.0, 12.0]
IMBALANCE_THRESHOLDS = [0.25, 0.40, 0.55]
DEPTH_CHANGE_THRESHOLDS = [0.10, 0.25, 0.40]
INITIAL_CAPITAL_INR = 1_000_000.0
ORDER_NOTIONAL_INR = 100_000.0
COST_MULTIPLIER = 2.0
MIN_COMPLETED_ROUND_TRIPS = 30
MIN_TRADE_DATES = 5
MIN_SYMBOLS = 5
MIN_POSITIVE_DATE_FRACTION = 0.60
ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT = 5.0
MAX_SURVIVORS_TO_REPORT = 25

EXPECTED_GRID_ROWS = len(FEATURE_FAMILIES) * len(LOOKBACK_TICKS) * len(FORWARD_TICKS) * len(SPREAD_BPS_BUCKETS) * len(IMBALANCE_THRESHOLDS) * len(DEPTH_CHANGE_THRESHOLDS)


def sha256_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_csv(index=False, lineterminator="\n").encode("utf-8")).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_family_catalog() -> pd.DataFrame:
    rows = []
    for family_id, description in FEATURE_FAMILIES:
        rows.append(
            {
                "family_id": family_id,
                "description": description,
                "requires_l2_l5": 1,
                "has_l1_only_control": 1,
                "has_side_flip_control": 1,
            }
        )
    return pd.DataFrame(rows)


def build_parameter_grid() -> pd.DataFrame:
    rows = []
    for family_id, _ in FEATURE_FAMILIES:
        for lookback in LOOKBACK_TICKS:
            for forward in FORWARD_TICKS:
                for spread in SPREAD_BPS_BUCKETS:
                    for imb in IMBALANCE_THRESHOLDS:
                        for depth in DEPTH_CHANGE_THRESHOLDS:
                            rows.append(
                                {
                                    "scenario_id": f"P428_{family_id}_L{lookback}_F{forward}_S{str(spread).replace('.', 'p')}_I{str(imb).replace('.', 'p')}_D{str(depth).replace('.', 'p')}",
                                    "family_id": family_id,
                                    "lookback_ticks": lookback,
                                    "forward_ticks": forward,
                                    "min_forward_hold_ms": MIN_FORWARD_HOLD_MS,
                                    "max_hold_ticks": MAX_HOLD_TICKS,
                                    "max_spread_bps": spread,
                                    "imbalance_threshold": imb,
                                    "depth_change_threshold": depth,
                                    "cost_multiplier": COST_MULTIPLIER,
                                    "order_notional_inr": ORDER_NOTIONAL_INR,
                                }
                            )
    return pd.DataFrame(rows)


def build_contract(grid: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("thesis_id", THESIS_ID, "Material-new broader full-depth L2 feature-family sweep after repeated narrow-route failures."),
            ("material_difference", "precommitted_multi_family_sweep_not_single_threshold_rescue", "Tests several distinct full-depth archetypes without post-result threshold edits."),
            ("families", ";".join(f for f, _ in FEATURE_FAMILIES), "Frozen feature families."),
            ("scenario_rows", len(grid), "Frozen scenario grid size."),
            ("execution_profile", "single_name_taker_entry_taker_exit_exact_forward_ticks_cost200", "No passive fills or maker rebate."),
            ("full_depth_required", "L1_to_L5_price_quantity_orders_levels_2_to_5_materiality", "Primary scenarios require top-five book state."),
            ("controls", "l1_only_removed_depth;side_flip;family_rank_stability;real_anchor_cross_check", "Controls must be reported."),
            ("capital", f"initial={INITIAL_CAPITAL_INR};order_notional={ORDER_NOTIONAL_INR}", "Fixed capital denominator."),
            ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha equity intraday NSE formula."),
            ("cost_multiplier", COST_MULTIPLIER, "Cost200 acceptance scoring."),
            ("acceptance", f"round_trips>={MIN_COMPLETED_ROUND_TRIPS};dates>={MIN_TRADE_DATES};symbols>={MIN_SYMBOLS};positive_date_fraction>={MIN_POSITIVE_DATE_FRACTION};annualized>={ANNUALIZED_THRESHOLD_PCT};l2_l5_edge_delta>={MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT}", "Broad search still needs profitability, breadth and full-depth uniqueness."),
            ("reporting_limit", f"top_survivors<={MAX_SURVIVORS_TO_REPORT}", "Report bounded candidates, not unlimited curve-fit tables."),
            ("forbidden", "pair_spread_rescue;queue_depletion_threshold_rescue;market_maker_rescue;passive_fill_rescue;bar_return_reversal_alone;post_result_threshold_tuning;promotion;paper_live;deployable_claim", "Closed routes and boundaries."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_input_registry(phase298: pd.DataFrame, schema: pd.DataFrame, phase426: pd.DataFrame, grid: pd.DataFrame) -> pd.DataFrame:
    schema_present = 0
    if not schema.empty and "book_level_present_columns" in schema.columns:
        schema_present = int(pd.to_numeric(schema["book_level_present_columns"], errors="coerce").fillna(0).min())
    return pd.DataFrame(
        [
            ("phase298_dense_root", scalar(phase298, "phase298_dense_root", ""), "Raw dense source root."),
            ("phase298_full_depth_required", scalar(phase298, "phase298_raw_book_state_l1_l5_required", ""), "Must be one."),
            ("phase298_levels_2_to_5_required", scalar(phase298, "phase298_levels_2_to_5_required", ""), "Must be one."),
            ("phase298_l1_only_variant_rows", scalar(phase298, "phase298_l1_only_variant_rows", ""), "Must be zero."),
            ("phase298_schema_present_columns_min", schema_present, "Minimum L1-L5 schema columns."),
            ("phase426_selected_verdict", scalar(phase426, "phase426_selected_verdict", ""), "Queue-depletion closure context."),
            ("phase426_same_family_tuning_allowed", scalar(phase426, "phase426_same_family_tuning_allowed", ""), "Must be zero."),
            ("scenario_grid_rows", len(grid), "Precommitted scenario count."),
            ("family_rows", len(FEATURE_FAMILIES), "Precommitted family count."),
            ("symbol_rows", len(SYMBOLS), "Precommitted symbol universe."),
            ("execution_results_generated_now", 0, "Precommit only."),
        ],
        columns=["input_id", "value", "description"],
    )


def build_execution_hard_gates() -> pd.DataFrame:
    gates = [
        ("P428_PHASE427_PRECOMMIT_USED", "Execution must read Phase427 frozen grid."),
        ("P428_TICK_ORDERED_REPLAY", "Ticks consumed in exchange-time order."),
        ("P428_EXACT_FORWARD_TICK_INDEXING", "Every trade exit must use exact post-entry tick offsets."),
        ("P428_FULL_DEPTH_PRIMARY_FEATURES", "Primary scenarios require L2-L5 features."),
        ("P428_L1_ONLY_CONTROL", "Run removed-depth control for every surviving family."),
        ("P428_SIDE_FLIP_CONTROL", "Run side-flip control for every surviving family."),
        ("P428_COST200_FIXED_CAPITAL", "Use Zerodha cost200 and fixed INR 1,000,000 capital."),
        ("P428_BREADTH_AND_RETURN_GATES", "Apply event/date/symbol/positive-date/annualized gates."),
        ("P428_REAL_ANCHOR_CROSS_CHECK", "Replay top bounded survivors on available real anchors."),
        ("P428_NO_POST_RESULT_TUNING", "Do not add thresholds after seeing results."),
        ("P428_BOUNDARIES_CLOSED", "No promotion, paper/live or deployable claim."),
    ]
    return pd.DataFrame([{"gate_id": g, "requirement": r, "severity": "hard", "phase427_precommitted": 1} for g, r in gates])


def build_gates(inputs: pd.DataFrame, contract: pd.DataFrame, grid: pd.DataFrame, exec_gates: pd.DataFrame) -> pd.DataFrame:
    values = dict(zip(inputs["input_id"], inputs["value"]))
    forbidden = ";".join(contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str))
    gates = [
        ("P427_PHASE298_RAW_DENSE_PRESENT", str(values.get("phase298_dense_root", "")) == "raw_synthetic_l2_dense_full_year", values.get("phase298_dense_root", ""), "raw_synthetic_l2_dense_full_year"),
        ("P427_FULL_DEPTH_SCHEMA_PRESENT", as_int(values.get("phase298_schema_present_columns_min", 0)) >= 30, values.get("phase298_schema_present_columns_min", ""), ">=30"),
        ("P427_LEVELS_2_TO_5_REQUIRED", str(values.get("phase298_levels_2_to_5_required", "")) == "1", values.get("phase298_levels_2_to_5_required", ""), 1),
        ("P427_PHASE426_ROUTE_CLOSED", str(values.get("phase426_selected_verdict", "")) == "P426_QUEUE_DEPLETION_CONTINUATION_REJECTED_ZERO_SYNTHETIC_EVENTS", values.get("phase426_selected_verdict", ""), "P426_QUEUE_DEPLETION_CONTINUATION_REJECTED_ZERO_SYNTHETIC_EVENTS"),
        ("P427_NO_SAME_FAMILY_TUNING", str(values.get("phase426_same_family_tuning_allowed", "")) == "0", values.get("phase426_same_family_tuning_allowed", ""), 0),
        ("P427_MULTI_FAMILY_GRID_FROZEN", len(grid) == EXPECTED_GRID_ROWS, len(grid), EXPECTED_GRID_ROWS),
        ("P427_FAMILY_BREADTH_FROZEN", len(FEATURE_FAMILIES) == 6, len(FEATURE_FAMILIES), 6),
        ("P427_EXACT_FORWARD_TICK_GRID_FROZEN", sorted(grid["forward_ticks"].unique().tolist()) == FORWARD_TICKS, ";".join(map(str, sorted(grid["forward_ticks"].unique().tolist()))), ";".join(map(str, FORWARD_TICKS))),
        ("P427_COST200_FIXED_CAPITAL_PINNED", COST_MULTIPLIER == 2.0 and INITIAL_CAPITAL_INR == 1_000_000.0 and ORDER_NOTIONAL_INR <= 100_000.0, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={ORDER_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P427_EXECUTION_HARD_GATES_PRECOMMITTED", len(exec_gates) == 11, len(exec_gates), 11),
        ("P427_RESULTS_NOT_GENERATED", as_int(values.get("execution_results_generated_now", 1)) == 0, values.get("execution_results_generated_now", ""), 0),
        ("P427_FORBIDDEN_ROUTES_CLOSED", all(x in forbidden for x in ["pair_spread_rescue", "queue_depletion_threshold_rescue", "market_maker_rescue", "post_result_threshold_tuning"]), forbidden, "closed_routes_listed"),
        ("P427_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(contract: pd.DataFrame, families: pd.DataFrame, grid: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase427_broader_full_depth_feature_family_precommit_complete", 1, "Phase427 precommit completed"),
            ("phase427_thesis_id", THESIS_ID, "Frozen thesis"),
            ("phase427_family_rows", len(families), "Frozen family rows"),
            ("phase427_scenario_grid_rows", len(grid), "Frozen scenario rows"),
            ("phase427_parameter_grid_hash", sha256_frame(grid), "Hash of frozen grid"),
            ("phase427_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha cost model"),
            ("phase427_cost_multiplier", COST_MULTIPLIER, "Cost200"),
            ("phase427_initial_capital_inr", INITIAL_CAPITAL_INR, "Fixed capital"),
            ("phase427_order_notional_inr", ORDER_NOTIONAL_INR, "Order notional"),
            ("phase427_execution_results_generated", 0, "Precommit only"),
            ("phase427_strategy_promotion_allowed", 0, "No promotion"),
            ("phase427_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase427_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase427_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase428 may run"),
            ("phase427_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase427_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase427_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, contract: pd.DataFrame, families: pd.DataFrame, grid: pd.DataFrame, inputs: pd.DataFrame, exec_gates: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase427 Broader Full-Depth Feature-Family Sweep Precommit",
        "",
        "Phase427 freezes a broader full-depth L2 feature-family sweep after the narrow Phase424 queue-depletion route failed with zero synthetic events.",
        "",
        "This is still not paper/live: it is a precommitted research sweep with exact-tick exits, cost200, fixed capital, L1-only controls and closed boundaries.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Frozen Contract",
        "",
        _markdown_table(contract),
        "",
        "## Feature Families",
        "",
        _markdown_table(families),
        "",
        "## Frozen Scenario Grid Sample",
        "",
        _markdown_table(grid.head(30)),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Phase428 Hard-Gate Contract",
        "",
        _markdown_table(exec_gates),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "No Phase427 strategy result, promotion, paper/live acceptance or deployable claim is generated.",
    ]
    (output_dir / "phase427_broader_full_depth_feature_family_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase298_dir: Path = DEFAULT_PHASE298_DIR, phase426_dir: Path = DEFAULT_PHASE426_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase298 = read_csv(phase298_dir / "phase298_acceptance_summary.csv")
    schema = read_csv(phase298_dir / "phase298_raw_book_schema_audit.csv")
    phase426 = read_csv(phase426_dir / "phase426_acceptance_summary.csv")
    if phase298.empty or schema.empty or phase426.empty:
        raise FileNotFoundError("Phase427 requires Phase298 raw dense outputs and Phase426 interpretation outputs.")
    families = build_family_catalog()
    grid = build_parameter_grid()
    contract = build_contract(grid)
    inputs = build_input_registry(phase298, schema, phase426, grid)
    exec_gates = build_execution_hard_gates()
    gates = build_gates(inputs, contract, grid, exec_gates)
    acceptance = build_acceptance(contract, families, grid, gates)
    contract.to_csv(output_dir / "phase427_frozen_contract.csv", index=False)
    families.to_csv(output_dir / "phase427_feature_family_catalog.csv", index=False)
    grid.to_csv(output_dir / "phase427_parameter_grid.csv", index=False)
    inputs.to_csv(output_dir / "phase427_input_registry.csv", index=False)
    exec_gates.to_csv(output_dir / "phase427_execution_hard_gate_contract.csv", index=False)
    gates.to_csv(output_dir / "phase427_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase427_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, contract, families, grid, inputs, exec_gates, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase427_broader_full_depth_feature_family_precommit",
        **reproducibility_fields(
            artifact_id="phase427_broader_full_depth_feature_family_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase298_acceptance_summary": str(phase298_dir / "phase298_acceptance_summary.csv"),
                "phase298_raw_book_schema_audit": str(phase298_dir / "phase298_raw_book_schema_audit.csv"),
                "phase426_acceptance_summary": str(phase426_dir / "phase426_acceptance_summary.csv"),
            },
            parameters={"thesis_id": THESIS_ID, "parameter_grid_hash": sha256_frame(grid), "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase427_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase427_precommit_exact_tick_feature_family_sweep",
        ),
    }
    (output_dir / "phase427_broader_full_depth_feature_family_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase427 broader full-depth feature-family sweep precommit.")
    parser.add_argument("--phase298-dir", type=Path, default=DEFAULT_PHASE298_DIR)
    parser.add_argument("--phase426-dir", type=Path, default=DEFAULT_PHASE426_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase298_dir, args.phase426_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

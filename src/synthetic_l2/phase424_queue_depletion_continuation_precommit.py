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
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE298_DIR = Path("outputs/phase298")
DEFAULT_PHASE423_DIR = Path("outputs/phase423")
DEFAULT_OUTPUT_DIR = Path("outputs/phase424")

THESIS_ID = "P424_FULL_DEPTH_QUEUE_DEPLETION_CONTINUATION"
NEXT_ACTION = "run_phase425_queue_depletion_continuation_execution_no_paper_live"
REPAIR_ACTION = "repair_phase424_queue_depletion_continuation_precommit"

SYMBOLS = [
    "ADANIPORTS",
    "AXISBANK",
    "BAJAJ-AUTO",
    "BANKBEES",
    "BHARTIARTL",
    "BPCL",
    "BRITANNIA",
    "CIPLA",
    "DRREDDY",
    "GOLDBEES",
    "HCLTECH",
    "HDFCBANK",
    "HINDUNILVR",
    "ICICIBANK",
    "INFY",
    "ITBEES",
    "ITC",
    "JUNIORBEES",
    "KOTAKBANK",
    "LT",
    "M&M",
    "MARUTI",
    "NESTLEIND",
    "NIFTYBEES",
    "ONGC",
    "RELIANCE",
    "SBIN",
    "SUNPHARMA",
    "TCS",
    "TECHM",
    "ULTRACEMCO",
    "WIPRO",
]

LOOKBACK_TICKS = 180
ENTRY_FORWARD_TICKS = 3
MIN_FORWARD_HOLD_MS = 250.0
MAX_HOLD_TICKS = 30
MIN_L2_L5_OPPOSITE_DEPLETION = 0.35
MIN_L2_L5_SAME_SIDE_REPLENISHMENT = 0.10
MIN_L1_IMBALANCE_CONFIRMATION = 0.55
MAX_SPREAD_BPS = 8.0
MAX_OPPOSITE_L1_NOTIONAL_INR = 1_500_000.0
MIN_L2_L5_DEPTH_NOTIONAL_INR = 2_000_000.0
INITIAL_CAPITAL_INR = 1_000_000.0
ORDER_NOTIONAL_INR = 100_000.0
COST_MULTIPLIER = 2.0
MIN_COMPLETED_ROUND_TRIPS = 30
MIN_TRADE_DATES = 5
MIN_SYMBOLS = 5
MIN_POSITIVE_DATE_FRACTION = 0.60
ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT = 5.0


def sha256_frame(frame: pd.DataFrame) -> str:
    payload = frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_symbol_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "symbol": symbol,
                "exchange": "NSE",
                "universe_role": "liquid_cash_equity_or_etf",
                "phase424_included": 1,
            }
            for symbol in SYMBOLS
        ]
    )


def build_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("thesis_id", THESIS_ID, "Material-new single-name full-depth L2 source after Phase423."),
            ("material_difference", "queue_depletion_continuation_not_pair_spread_not_market_making_not_bar_reversal", "Continuation after visible opposite-side depth evaporation, not a rescue of closed routes."),
            ("market_hypothesis", "when_l2_l5_opposite_queue_evaporates_and_l1_pressure_confirms_direction_short_horizon_continuation_may_pay_after_cost200", "A liquidity-consumption continuation thesis using the full top-five book."),
            ("entry_signal", "opposite_l2_l5_depth_depletion_plus_order_count_thinning_plus_l1_imbalance_confirmation", "Requires levels 2-5 depth and order-count features."),
            ("long_rule", "ask_l2_l5_depletes_ask_order_count_thins_bid_l2_l5_replenishes_l1_imbalance_bid_dominant", "Buy when ask-side queues thin and bid pressure confirms."),
            ("short_rule", "bid_l2_l5_depletes_bid_order_count_thins_ask_l2_l5_replenishes_l1_imbalance_ask_dominant", "Sell/short-side simulation mirror for research scoring only."),
            ("exit_rule", "exit_after_entry_forward_ticks_stop_or_max_hold_ticks", "Uses exact forward tick indexing in Phase425, not elapsed-time proxy-only."),
            ("execution_profile", "taker_entry_then_taker_exit_cost200_no_passive_fill_no_maker_rebate", "Directional taker execution with Zerodha costs."),
            ("full_depth_required", "L1_to_L5_price_quantity_orders_with_levels_2_to_5_materiality", "Top-five market-by-price book state is mandatory."),
            ("l1_only_control", "remove_l2_l5_depletion_replenishment_and_order_count_terms", "Primary must beat L1-only control by the frozen edge margin."),
            ("side_flip_control", "invert_direction_for_same_events", "Side-flip must not dominate primary."),
            ("real_anchor_cross_check", "replay_same_frozen_rules_on_available_local_real_l2_dates", "Check sign and cost survival on real anchors if enough rows exist."),
            ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha equity intraday NSE formula."),
            ("cost_multiplier", COST_MULTIPLIER, "Cost200 acceptance scoring."),
            ("capital", f"initial={INITIAL_CAPITAL_INR};order_notional={ORDER_NOTIONAL_INR}", "Fixed capital denominator, no unlimited capital."),
            ("acceptance", f"round_trips>={MIN_COMPLETED_ROUND_TRIPS};dates>={MIN_TRADE_DATES};symbols>={MIN_SYMBOLS};positive_date_fraction>={MIN_POSITIVE_DATE_FRACTION};annualized>={ANNUALIZED_THRESHOLD_PCT};l2_l5_edge_delta>={MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT}", "Must be profitable with breadth and full-depth uniqueness."),
            ("forbidden", "pair_spread_rescue;market_maker_rescue;passive_fill_rescue;bar_return_reversal_alone;post_result_threshold_tuning;promotion;paper_live;deployable_claim", "Closed routes and boundaries."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_parameter_freeze(symbol_catalog: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("P424_LOOKBACK_TICKS", LOOKBACK_TICKS, "fixed"),
        ("P424_ENTRY_FORWARD_TICKS", ENTRY_FORWARD_TICKS, "fixed"),
        ("P424_MIN_FORWARD_HOLD_MS", MIN_FORWARD_HOLD_MS, "fixed"),
        ("P424_MAX_HOLD_TICKS", MAX_HOLD_TICKS, "fixed"),
        ("P424_MIN_L2_L5_OPPOSITE_DEPLETION", MIN_L2_L5_OPPOSITE_DEPLETION, "fixed"),
        ("P424_MIN_L2_L5_SAME_SIDE_REPLENISHMENT", MIN_L2_L5_SAME_SIDE_REPLENISHMENT, "fixed"),
        ("P424_MIN_L1_IMBALANCE_CONFIRMATION", MIN_L1_IMBALANCE_CONFIRMATION, "fixed"),
        ("P424_MAX_SPREAD_BPS", MAX_SPREAD_BPS, "fixed"),
        ("P424_MAX_OPPOSITE_L1_NOTIONAL_INR", MAX_OPPOSITE_L1_NOTIONAL_INR, "fixed"),
        ("P424_MIN_L2_L5_DEPTH_NOTIONAL_INR", MIN_L2_L5_DEPTH_NOTIONAL_INR, "fixed"),
        ("P424_INITIAL_CAPITAL_INR", INITIAL_CAPITAL_INR, "fixed"),
        ("P424_ORDER_NOTIONAL_INR", ORDER_NOTIONAL_INR, "fixed"),
        ("P424_COST_MULTIPLIER", COST_MULTIPLIER, "fixed"),
        ("P424_MIN_COMPLETED_ROUND_TRIPS", MIN_COMPLETED_ROUND_TRIPS, "fixed"),
        ("P424_MIN_TRADE_DATES", MIN_TRADE_DATES, "fixed"),
        ("P424_MIN_SYMBOLS", MIN_SYMBOLS, "fixed"),
        ("P424_MIN_POSITIVE_DATE_FRACTION", MIN_POSITIVE_DATE_FRACTION, "fixed"),
        ("P424_ANNUALIZED_THRESHOLD_PCT", ANNUALIZED_THRESHOLD_PCT, "fixed"),
        ("P424_MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT", MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT, "fixed"),
    ]
    rows.append(("P424_SYMBOL_COUNT", len(symbol_catalog), "fixed"))
    return pd.DataFrame(rows, columns=["parameter_id", "value", "status"])


def build_input_registry(phase298: pd.DataFrame, schema: pd.DataFrame, phase423: pd.DataFrame, symbol_catalog: pd.DataFrame) -> pd.DataFrame:
    schema_present = 0
    if not schema.empty and "book_level_present_columns" in schema.columns:
        schema_present = int(pd.to_numeric(schema["book_level_present_columns"], errors="coerce").fillna(0).min())
    return pd.DataFrame(
        [
            ("phase298_dense_root", scalar(phase298, "phase298_dense_root", ""), "Raw dense source root."),
            ("phase298_full_depth_required", scalar(phase298, "phase298_raw_book_state_l1_l5_required", ""), "Must be one."),
            ("phase298_levels_2_to_5_required", scalar(phase298, "phase298_levels_2_to_5_required", ""), "Must be one."),
            ("phase298_l1_only_variant_rows", scalar(phase298, "phase298_l1_only_variant_rows", ""), "Must be zero."),
            ("phase298_net_edge_live_mask_rows", scalar(phase298, "phase298_net_edge_live_mask_rows", ""), "Must be zero."),
            ("phase298_schema_present_columns_min", schema_present, "Minimum L1-L5 schema columns."),
            ("phase423_selected_verdict", scalar(phase423, "phase423_selected_verdict", ""), "Pair-spread route closure context."),
            ("phase423_same_family_tuning_allowed", scalar(phase423, "phase423_same_family_tuning_allowed", ""), "Must be zero."),
            ("symbol_catalog_rows", len(symbol_catalog), "Precommitted symbol count."),
            ("execution_results_generated_now", 0, "Precommit only."),
        ],
        columns=["input_id", "value", "description"],
    )


def build_execution_hard_gates() -> pd.DataFrame:
    gates = [
        ("P425_PHASE424_PRECOMMIT_USED", "Execution must read Phase424 frozen contract and parameter freeze."),
        ("P425_TICK_ORDERED_SINGLE_NAME_REPLAY", "Ticks must be consumed in exchange-time order with no lookahead."),
        ("P425_EXACT_FORWARD_TICK_INDEXING", f"Exit evaluation must use at least {ENTRY_FORWARD_TICKS} exact post-entry ticks, not proxy-only elapsed time."),
        ("P425_FORWARD_TIME_ENFORCED", f"Exit must also be at least {MIN_FORWARD_HOLD_MS} ms after entry."),
        ("P425_FULL_DEPTH_L1_L5_REQUIRED", "Feature rows must include L1-L5 price, quantity and order count fields."),
        ("P425_LEVELS_2_TO_5_MATERIAL", "Primary entry must require L2-L5 depletion/replenishment/order-count thinning."),
        ("P425_L1_ONLY_CONTROL", "L1-only control must be run and primary must beat it by the frozen edge margin."),
        ("P425_SIDE_FLIP_CONTROL", "Side-flip control must be run and must not dominate primary."),
        ("P425_TAKER_ONLY_EXECUTION", "No passive fill, queue priority advantage or maker rebate."),
        ("P425_NO_LOOKAHEAD", "All rolling queue-depletion features must be computed before entry tick."),
        ("P425_COST200_FIXED_CAPITAL", "Use Zerodha cost200 with fixed INR 1,000,000 denominator."),
        ("P425_EVENT_FLOOR", f"Completed round trips >= {MIN_COMPLETED_ROUND_TRIPS}."),
        ("P425_DATE_BREADTH", f"Distinct trade dates >= {MIN_TRADE_DATES}."),
        ("P425_SYMBOL_BREADTH", f"Distinct symbols >= {MIN_SYMBOLS}."),
        ("P425_POSITIVE_DATE_FRACTION", f"Positive date fraction >= {MIN_POSITIVE_DATE_FRACTION}."),
        ("P425_ANNUALIZED_FLOOR", f"Annualized fixed-capital return >= {ANNUALIZED_THRESHOLD_PCT} percent."),
        ("P425_REAL_ANCHOR_CROSS_CHECK", "Replay on available local real L2 dates and report sign/cost survival."),
        ("P425_BOUNDARIES_CLOSED", "No promotion, paper/live acceptance or deployable claim in Phase425."),
    ]
    return pd.DataFrame([{"gate_id": gate, "requirement": requirement, "severity": "hard", "phase424_precommitted": 1} for gate, requirement in gates])


def build_gates(inputs: pd.DataFrame, contract: pd.DataFrame, freeze: pd.DataFrame, exec_gates: pd.DataFrame) -> pd.DataFrame:
    values = dict(zip(inputs["input_id"], inputs["value"]))
    schema_cols = as_int(values.get("phase298_schema_present_columns_min", 0))
    material = ";".join(contract.loc[contract["contract_id"].eq("material_difference"), "contract_value"].astype(str).tolist())
    forbidden = ";".join(contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).tolist())
    gates = [
        ("P424_PHASE298_RAW_DENSE_PRESENT", str(values.get("phase298_dense_root", "")) == "raw_synthetic_l2_dense_full_year", values.get("phase298_dense_root", ""), "raw_synthetic_l2_dense_full_year"),
        ("P424_FULL_DEPTH_SCHEMA_PRESENT", schema_cols >= 30, schema_cols, ">=30"),
        ("P424_LEVELS_2_TO_5_REQUIRED", str(values.get("phase298_levels_2_to_5_required", "")) == "1", values.get("phase298_levels_2_to_5_required", ""), 1),
        ("P424_L1_ONLY_FORBIDDEN_AS_PRIMARY", as_int(values.get("phase298_l1_only_variant_rows", 1)) == 0, values.get("phase298_l1_only_variant_rows", ""), 0),
        ("P424_NO_NET_EDGE_LIVE_MASK", as_int(values.get("phase298_net_edge_live_mask_rows", 1)) == 0, values.get("phase298_net_edge_live_mask_rows", ""), 0),
        ("P424_PHASE423_PAIR_ROUTE_CLOSED", str(values.get("phase423_selected_verdict", "")) == "P423_PAIR_SPREAD_POSITIVE_LEAD_FALSIFIED_BY_REALISM_RETEST", values.get("phase423_selected_verdict", ""), "P423_PAIR_SPREAD_POSITIVE_LEAD_FALSIFIED_BY_REALISM_RETEST"),
        ("P424_NO_SAME_FAMILY_TUNING", str(values.get("phase423_same_family_tuning_allowed", "")) == "0", values.get("phase423_same_family_tuning_allowed", ""), 0),
        ("P424_MATERIAL_NEW_QUEUE_DEPLETION", "queue_depletion_continuation" in material and "not_pair_spread" in material, material, "queue_depletion_not_pair"),
        ("P424_SYMBOL_CATALOG_FROZEN", as_int(values.get("symbol_catalog_rows", 0)) >= MIN_SYMBOLS, values.get("symbol_catalog_rows", ""), f">={MIN_SYMBOLS}"),
        ("P424_FIXED_PARAMETERS_FROZEN", len(freeze) >= 20, len(freeze), ">=20"),
        ("P424_EXACT_FORWARD_TICK_REQUIREMENT_FROZEN", ENTRY_FORWARD_TICKS >= 3 and MIN_FORWARD_HOLD_MS >= 250.0, f"ticks={ENTRY_FORWARD_TICKS};ms={MIN_FORWARD_HOLD_MS}", "ticks>=3;ms>=250"),
        ("P424_FULL_DEPTH_UNIQUE_GATE_FROZEN", MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT > 0, MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT, ">0"),
        ("P424_COST200_FIXED_CAPITAL_PINNED", COST_MULTIPLIER == 2.0 and INITIAL_CAPITAL_INR >= 1_000_000 and ORDER_NOTIONAL_INR <= 100_000, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};order_notional={ORDER_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P424_EXECUTION_HARD_GATES_PRECOMMITTED", len(exec_gates) == 18, len(exec_gates), 18),
        ("P424_RESULTS_NOT_GENERATED", as_int(values.get("execution_results_generated_now", 1)) == 0, values.get("execution_results_generated_now", ""), 0),
        ("P424_FORBIDDEN_ROUTES_CLOSED", all(x in forbidden for x in ["pair_spread_rescue", "market_maker_rescue", "passive_fill_rescue", "bar_return_reversal_alone"]), forbidden, "closed_routes_listed"),
        ("P424_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(contract: pd.DataFrame, symbols: pd.DataFrame, freeze: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase424_queue_depletion_continuation_precommit_complete", 1, "Phase424 precommit completed"),
            ("phase424_thesis_id", THESIS_ID, "Frozen thesis"),
            ("phase424_material_new_full_depth", 1, "Queue-depletion continuation"),
            ("phase424_contract_rows", len(contract), "Contract rows"),
            ("phase424_symbol_catalog_rows", len(symbols), "Frozen symbols"),
            ("phase424_parameter_freeze_rows", len(freeze), "Frozen parameter rows"),
            ("phase424_parameter_freeze_hash", sha256_frame(freeze), "Hash of frozen parameter table"),
            ("phase424_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha cost model"),
            ("phase424_cost_multiplier", COST_MULTIPLIER, "Cost200"),
            ("phase424_initial_capital_inr", INITIAL_CAPITAL_INR, "Fixed capital"),
            ("phase424_order_notional_inr", ORDER_NOTIONAL_INR, "Order notional"),
            ("phase424_exact_forward_ticks_required", ENTRY_FORWARD_TICKS, "No proxy-only tick gate"),
            ("phase424_execution_results_generated", 0, "Precommit only"),
            ("phase424_strategy_promotion_allowed", 0, "No promotion"),
            ("phase424_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase424_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase424_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase425 may run"),
            ("phase424_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase424_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase424_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, contract: pd.DataFrame, symbols: pd.DataFrame, freeze: pd.DataFrame, inputs: pd.DataFrame, exec_gates: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase424 Queue-Depletion Continuation Precommit",
        "",
        "Phase424 freezes a materially new full-depth L2 thesis after Phase423 falsified the pair-spread positive lead.",
        "",
        "The thesis is queue-depletion continuation: when levels 2-5 on the opposite side visibly evaporate, order counts thin, same-side deeper liquidity replenishes, and L1 pressure confirms the direction, the next few exact ticks may continue before costs overwhelm the move.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Frozen Contract",
        "",
        _markdown_table(contract),
        "",
        "## Symbol Catalog",
        "",
        _markdown_table(symbols),
        "",
        "## Frozen Parameters",
        "",
        _markdown_table(freeze),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Phase425 Hard-Gate Contract",
        "",
        _markdown_table(exec_gates),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "No Phase424 strategy result, promotion, paper/live acceptance or deployable claim is generated.",
    ]
    (output_dir / "phase424_queue_depletion_continuation_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase298_dir: Path = DEFAULT_PHASE298_DIR, phase423_dir: Path = DEFAULT_PHASE423_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase298 = read_csv(phase298_dir / "phase298_acceptance_summary.csv")
    schema = read_csv(phase298_dir / "phase298_raw_book_schema_audit.csv")
    phase423 = read_csv(phase423_dir / "phase423_acceptance_summary.csv")
    if phase298.empty or schema.empty or phase423.empty:
        raise FileNotFoundError("Phase424 requires Phase298 raw dense acceptance/schema outputs and Phase423 acceptance summary.")
    symbol_catalog = build_symbol_catalog()
    contract = build_contract()
    freeze = build_parameter_freeze(symbol_catalog)
    inputs = build_input_registry(phase298, schema, phase423, symbol_catalog)
    exec_gates = build_execution_hard_gates()
    gates = build_gates(inputs, contract, freeze, exec_gates)
    acceptance = build_acceptance(contract, symbol_catalog, freeze, gates)
    contract.to_csv(output_dir / "phase424_frozen_contract.csv", index=False)
    symbol_catalog.to_csv(output_dir / "phase424_symbol_catalog.csv", index=False)
    freeze.to_csv(output_dir / "phase424_parameter_freeze.csv", index=False)
    inputs.to_csv(output_dir / "phase424_input_registry.csv", index=False)
    exec_gates.to_csv(output_dir / "phase424_execution_hard_gate_contract.csv", index=False)
    gates.to_csv(output_dir / "phase424_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase424_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, contract, symbol_catalog, freeze, inputs, exec_gates, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase424_queue_depletion_continuation_precommit",
        **reproducibility_fields(
            artifact_id="phase424_queue_depletion_continuation_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase298_acceptance_summary": str(phase298_dir / "phase298_acceptance_summary.csv"),
                "phase298_raw_book_schema_audit": str(phase298_dir / "phase298_raw_book_schema_audit.csv"),
                "phase423_acceptance_summary": str(phase423_dir / "phase423_acceptance_summary.csv"),
            },
            parameters={"thesis_id": THESIS_ID, "parameter_freeze_hash": sha256_frame(freeze), "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase424_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase424_precommit_exact_forward_tick_indexing",
        ),
    }
    (output_dir / "phase424_queue_depletion_continuation_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase424 queue-depletion continuation precommit.")
    parser.add_argument("--phase298-dir", type=Path, default=DEFAULT_PHASE298_DIR)
    parser.add_argument("--phase423-dir", type=Path, default=DEFAULT_PHASE423_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase298_dir, args.phase423_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

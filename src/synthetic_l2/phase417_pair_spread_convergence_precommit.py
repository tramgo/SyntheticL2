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
DEFAULT_PHASE416_DIR = Path("outputs/phase416")
DEFAULT_OUTPUT_DIR = Path("outputs/phase417")

THESIS_ID = "P417_FULL_DEPTH_PAIR_SPREAD_CONVERGENCE_MARKET_NEUTRAL"
NEXT_ACTION = "run_phase418_pair_spread_convergence_execution_no_paper_live"
REPAIR_ACTION = "repair_phase417_pair_spread_convergence_precommit"

PAIRS = [
    ("HDFCBANK", "ICICIBANK"),
    ("HDFCBANK", "AXISBANK"),
    ("INFY", "TCS"),
    ("RELIANCE", "ONGC"),
]
LOOKBACK_TICKS = 240
ENTRY_ZSCORE = 1.75
EXIT_ZSCORE = 0.35
STOP_ZSCORE = 3.25
MAX_HOLD_TICKS = 360
MAX_SPREAD_BPS_PER_LEG = 8.0
MIN_L2_L5_LIQUIDITY_PER_LEG_INR = 2_000_000.0
MAX_ABS_L2_L5_IMBALANCE_CONFLICT = 0.65
INITIAL_CAPITAL_INR = 1_000_000.0
PAIR_NOTIONAL_INR = 100_000.0
LEG_NOTIONAL_INR = 50_000.0
COST_MULTIPLIER = 2.0
MIN_COMPLETED_ROUND_TRIPS = 30
MIN_TRADE_DATES = 5
MIN_PAIRS = 2
MIN_POSITIVE_DATE_FRACTION = 0.60
ANNUALIZED_THRESHOLD_PCT = 12.0


def sha256_frame(frame: pd.DataFrame) -> str:
    payload = frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_pair_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "pair_id": f"{a}_{b}",
                "leg_a": a,
                "leg_b": b,
                "gross_pair_notional_inr": PAIR_NOTIONAL_INR,
                "leg_notional_inr": LEG_NOTIONAL_INR,
                "relationship": "sector_or_macro_linked_large_liquid_names",
            }
            for a, b in PAIRS
        ]
    )


def build_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("thesis_id", THESIS_ID, "Material-new non-directional full-depth L2 source after Phase416."),
            ("material_difference", "market_neutral_pair_spread_convergence_not_single_name_directional_not_market_making", "Long/short pair exposure, not one-name direction or passive quoting."),
            ("market_hypothesis", "temporary_pair_spread_dislocation_with_adequate_l2_l5_liquidity_and_no_deep_book_conflict_may_converge", "Non-directional relative-value thesis."),
            ("entry_signal", "rolling_log_mid_spread_zscore_abs_ge_entry_threshold", "Pair spread z-score, not bar-return reversal alone."),
            ("side_rule", "if spread high short leg_a_long_leg_b; if spread low long_leg_a_short_leg_b", "Market-neutral pair direction."),
            ("exit_rule", "exit_on_zscore_reversion_stop_or_max_hold_ticks", "Fixed exit, stop and max hold."),
            ("execution_profile", "taker_entry_both_legs_taker_exit_both_legs_cost200", "No passive fills and no maker rebate."),
            ("lookback_ticks", LOOKBACK_TICKS, "Fixed rolling pair spread lookback."),
            ("entry_zscore", ENTRY_ZSCORE, "Fixed entry z-score."),
            ("exit_zscore", EXIT_ZSCORE, "Fixed convergence exit."),
            ("stop_zscore", STOP_ZSCORE, "Fixed divergence stop."),
            ("max_hold_ticks", MAX_HOLD_TICKS, "Fixed max hold."),
            ("max_spread_bps_per_leg", MAX_SPREAD_BPS_PER_LEG, "Avoid wide-spread execution per leg."),
            ("min_l2_l5_liquidity_per_leg_inr", MIN_L2_L5_LIQUIDITY_PER_LEG_INR, "Full-depth liquidity gate beyond L1."),
            ("max_abs_l2_l5_imbalance_conflict", MAX_ABS_L2_L5_IMBALANCE_CONFLICT, "Avoid severe deep-book pressure against required leg direction."),
            ("full_depth_required", "L1_to_L5_both_legs_with_levels_2_to_5_liquidity_and_imbalance", "L1-only variants forbidden."),
            ("pair_catalog_rows", len(PAIRS), "Precommitted pairs."),
            ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha equity intraday NSE formula."),
            ("cost_multiplier", COST_MULTIPLIER, "Cost200 acceptance scoring."),
            ("capital", f"initial={INITIAL_CAPITAL_INR};pair_notional={PAIR_NOTIONAL_INR};leg_notional={LEG_NOTIONAL_INR}", "Fixed capital denominator, no unlimited capital."),
            ("acceptance", f"round_trips>={MIN_COMPLETED_ROUND_TRIPS};dates>={MIN_TRADE_DATES};pairs>={MIN_PAIRS};positive_date_fraction>={MIN_POSITIVE_DATE_FRACTION};annualized>={ANNUALIZED_THRESHOLD_PCT}", "Must be profitable with breadth."),
            ("controls", "side_flip;levels_2_to_5_removed;single_leg_proxy;cost100_rank_stability;real_anchor_sign", "Controls must be reported."),
            ("forbidden", "directional_snapback_rescue;market_maker_rescue;passive_fill_rescue;bar_return_reversal_alone;promotion;paper_live;deployable_claim", "Closed routes and boundaries."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_parameter_freeze(pair_catalog: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("P417_LOOKBACK_TICKS", LOOKBACK_TICKS, "fixed"),
        ("P417_ENTRY_ZSCORE", ENTRY_ZSCORE, "fixed"),
        ("P417_EXIT_ZSCORE", EXIT_ZSCORE, "fixed"),
        ("P417_STOP_ZSCORE", STOP_ZSCORE, "fixed"),
        ("P417_MAX_HOLD_TICKS", MAX_HOLD_TICKS, "fixed"),
        ("P417_MAX_SPREAD_BPS_PER_LEG", MAX_SPREAD_BPS_PER_LEG, "fixed"),
        ("P417_MIN_L2_L5_LIQUIDITY_PER_LEG_INR", MIN_L2_L5_LIQUIDITY_PER_LEG_INR, "fixed"),
        ("P417_MAX_ABS_L2_L5_IMBALANCE_CONFLICT", MAX_ABS_L2_L5_IMBALANCE_CONFLICT, "fixed"),
        ("P417_INITIAL_CAPITAL_INR", INITIAL_CAPITAL_INR, "fixed"),
        ("P417_PAIR_NOTIONAL_INR", PAIR_NOTIONAL_INR, "fixed"),
        ("P417_COST_MULTIPLIER", COST_MULTIPLIER, "fixed"),
    ]
    for row in pair_catalog.itertuples(index=False):
        rows.append((f"P417_PAIR_{row.pair_id}", f"{row.leg_a}/{row.leg_b}", "fixed"))
    return pd.DataFrame(rows, columns=["parameter_id", "value", "status"])


def build_input_registry(phase298: pd.DataFrame, schema: pd.DataFrame, phase416: pd.DataFrame, pair_catalog: pd.DataFrame) -> pd.DataFrame:
    schema_present = 0
    if not schema.empty and "book_level_present_columns" in schema.columns:
        schema_present = int(pd.to_numeric(schema["book_level_present_columns"], errors="coerce").fillna(0).min())
    symbols_needed = sorted(set(pair_catalog["leg_a"]).union(set(pair_catalog["leg_b"])))
    return pd.DataFrame(
        [
            ("phase298_dense_root", scalar(phase298, "phase298_dense_root", ""), "Raw dense source root."),
            ("phase298_full_depth_required", scalar(phase298, "phase298_raw_book_state_l1_l5_required", ""), "Must be one."),
            ("phase298_levels_2_to_5_required", scalar(phase298, "phase298_levels_2_to_5_required", ""), "Must be one."),
            ("phase298_l1_only_variant_rows", scalar(phase298, "phase298_l1_only_variant_rows", ""), "Must be zero."),
            ("phase298_net_edge_live_mask_rows", scalar(phase298, "phase298_net_edge_live_mask_rows", ""), "Must be zero."),
            ("phase298_schema_present_columns_min", schema_present, "Minimum L1-L5 schema columns."),
            ("phase416_selected_verdict", scalar(phase416, "phase416_selected_verdict", ""), "Directional snapback closure context."),
            ("phase416_same_family_tuning_allowed", scalar(phase416, "phase416_same_family_tuning_allowed", ""), "Must be zero."),
            ("pair_catalog_rows", len(pair_catalog), "Precommitted pair count."),
            ("symbols_needed", ";".join(symbols_needed), "Symbols required by Phase418."),
            ("execution_results_generated_now", 0, "Precommit only."),
        ],
        columns=["input_id", "value", "description"],
    )


def build_execution_hard_gates() -> pd.DataFrame:
    gates = [
        ("P418_TICK_ORDERED_PAIR_ALIGNMENT", "Pair ticks must be aligned by timestamp without lookahead."),
        ("P418_MARKET_NEUTRAL_PAIR_EXPOSURE", "Both legs must be entered and exited with equal fixed notional."),
        ("P418_TAKER_ONLY_EXECUTION", "No passive fills, no maker rebate."),
        ("P418_FULL_DEPTH_L1_L5_BOTH_LEGS", "Both legs must use L1-L5 book state."),
        ("P418_LEVELS_2_TO_5_MATERIAL", "Levels 2-5 liquidity and imbalance gates required."),
        ("P418_NO_LOOKAHEAD", "Rolling z-score and depth features must be known before entry."),
        ("P418_COST200_FIXED_CAPITAL", "Use Zerodha cost200 and fixed INR 1,000,000 capital."),
        ("P418_FIXED_PARAMETERS", "No post-result tuning."),
        ("P418_EVENT_FLOOR", f"Completed pair round trips >= {MIN_COMPLETED_ROUND_TRIPS}."),
        ("P418_DATE_BREADTH", f"Distinct trade dates >= {MIN_TRADE_DATES}."),
        ("P418_PAIR_BREADTH", f"Distinct pairs >= {MIN_PAIRS}."),
        ("P418_POSITIVE_DATE_FRACTION", f"Positive date fraction >= {MIN_POSITIVE_DATE_FRACTION}."),
        ("P418_ANNUALIZED_FLOOR", f"Annualized fixed-capital return >= {ANNUALIZED_THRESHOLD_PCT} percent."),
        ("P418_SIDE_FLIP_CONTROL", "Side-flip pair direction must not dominate primary."),
        ("P418_L2_L5_REMOVED_CONTROL", "Removing levels 2-5 must degrade or invalidate primary."),
        ("P418_SINGLE_LEG_PROXY_CONTROL", "Pair result must not be explainable by one leg only."),
        ("P418_COST100_RANK_STABILITY", "Cost100 rank must not reverse acceptance ordering."),
        ("P418_REAL_ANCHOR_CROSS_CHECK", "Synthetic result sign must be checked on real anchors if available."),
        ("P418_BOUNDARIES_CLOSED", "No promotion, paper/live acceptance or deployable claim."),
    ]
    return pd.DataFrame(
        [{"gate_id": gate, "requirement": requirement, "severity": "hard", "phase417_precommitted": 1} for gate, requirement in gates]
    )


def build_gate_evaluation(inputs: pd.DataFrame, contract: pd.DataFrame, freeze: pd.DataFrame, exec_gates: pd.DataFrame) -> pd.DataFrame:
    values = dict(zip(inputs["input_id"], inputs["value"]))
    schema_cols = as_int(values.get("phase298_schema_present_columns_min", 0))
    material = ";".join(contract.loc[contract["contract_id"].eq("material_difference"), "contract_value"].astype(str).tolist())
    forbidden = ";".join(contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str).tolist())
    gates = [
        ("P417_PHASE298_RAW_DENSE_PRESENT", str(values.get("phase298_dense_root", "")) == "raw_synthetic_l2_dense_full_year", values.get("phase298_dense_root", ""), "raw_synthetic_l2_dense_full_year"),
        ("P417_FULL_DEPTH_SCHEMA_PRESENT", schema_cols >= 30, schema_cols, ">=30"),
        ("P417_LEVELS_2_TO_5_REQUIRED", str(values.get("phase298_levels_2_to_5_required", "")) == "1", values.get("phase298_levels_2_to_5_required", ""), 1),
        ("P417_L1_ONLY_FORBIDDEN", as_int(values.get("phase298_l1_only_variant_rows", 1)) == 0, values.get("phase298_l1_only_variant_rows", ""), 0),
        ("P417_NO_LOOKAHEAD_SOURCE", as_int(values.get("phase298_net_edge_live_mask_rows", 1)) == 0, values.get("phase298_net_edge_live_mask_rows", ""), 0),
        ("P417_PHASE416_DIRECTIONAL_ROUTE_CLOSED", str(values.get("phase416_selected_verdict", "")) == "P416_DEEP_BOOK_DIVERGENCE_SNAPBACK_REJECTED_NON_SPARSE_NEGATIVE", values.get("phase416_selected_verdict", ""), "P416_DEEP_BOOK_DIVERGENCE_SNAPBACK_REJECTED_NON_SPARSE_NEGATIVE"),
        ("P417_NO_SAME_FAMILY_TUNING", str(values.get("phase416_same_family_tuning_allowed", "")) == "0", values.get("phase416_same_family_tuning_allowed", ""), 0),
        ("P417_MARKET_NEUTRAL_MATERIAL_NEW", "market_neutral_pair_spread_convergence" in material and "not_single_name_directional" in material, material, "market_neutral_not_directional"),
        ("P417_PAIR_CATALOG_FROZEN", as_int(values.get("pair_catalog_rows", 0)) >= 4, values.get("pair_catalog_rows", ""), ">=4"),
        ("P417_FIXED_PARAMETERS_FROZEN", len(freeze) >= 15, len(freeze), ">=15"),
        ("P417_TAKER_ONLY_PINNED", "taker_entry_both_legs_taker_exit_both_legs_cost200" in ";".join(contract["contract_value"].astype(str)), "taker_only_pair", "present"),
        ("P417_COST200_FIXED_CAPITAL_PINNED", COST_MULTIPLIER == 2.0 and INITIAL_CAPITAL_INR >= 1_000_000 and PAIR_NOTIONAL_INR <= 100_000, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};pair_notional={PAIR_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P417_EXECUTION_HARD_GATES_PRECOMMITTED", len(exec_gates) == 19, len(exec_gates), 19),
        ("P417_RESULTS_NOT_GENERATED", as_int(values.get("execution_results_generated_now", 1)) == 0, values.get("execution_results_generated_now", ""), 0),
        ("P417_FORBIDDEN_ROUTES_CLOSED", all(x in forbidden for x in ["directional_snapback_rescue", "market_maker_rescue", "passive_fill_rescue", "bar_return_reversal_alone"]), forbidden, "closed_routes_listed"),
        ("P417_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(contract: pd.DataFrame, pairs: pd.DataFrame, freeze: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase417_pair_spread_convergence_precommit_complete", 1, "Phase417 precommit completed"),
            ("phase417_thesis_id", THESIS_ID, "Frozen thesis"),
            ("phase417_material_new_non_directional", 1, "Market-neutral pair-spread convergence"),
            ("phase417_contract_rows", len(contract), "Contract rows"),
            ("phase417_pair_catalog_rows", len(pairs), "Frozen pairs"),
            ("phase417_parameter_freeze_rows", len(freeze), "Frozen parameter rows"),
            ("phase417_parameter_freeze_hash", sha256_frame(freeze), "Hash of frozen parameter table"),
            ("phase417_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha cost model"),
            ("phase417_cost_multiplier", COST_MULTIPLIER, "Cost200"),
            ("phase417_initial_capital_inr", INITIAL_CAPITAL_INR, "Fixed capital"),
            ("phase417_pair_notional_inr", PAIR_NOTIONAL_INR, "Gross pair notional"),
            ("phase417_execution_results_generated", 0, "Precommit only"),
            ("phase417_strategy_promotion_allowed", 0, "No promotion"),
            ("phase417_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase417_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase417_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase418 may run"),
            ("phase417_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase417_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase417_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, contract: pd.DataFrame, pairs: pd.DataFrame, freeze: pd.DataFrame, inputs: pd.DataFrame, exec_gates: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase417 Pair-Spread Convergence Precommit",
        "",
        "Phase417 freezes a materially new non-directional full-depth L2 source after Phase416 closed the directional snapback route.",
        "",
        "The thesis is market-neutral pair-spread convergence with taker-only equal-notional long/short legs and L1-L5 depth checks on both legs.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Frozen Thesis Contract",
        "",
        _markdown_table(contract),
        "",
        "## Pair Catalog",
        "",
        _markdown_table(pairs),
        "",
        "## Frozen Parameters",
        "",
        _markdown_table(freeze),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Phase418 Hard-Gate Contract",
        "",
        _markdown_table(exec_gates),
        "",
        "## Phase417 Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "No strategy result, promotion, paper/live acceptance or deployable profitability claim is generated by Phase417.",
    ]
    (output_dir / "phase417_pair_spread_convergence_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase298_dir: Path = DEFAULT_PHASE298_DIR, phase416_dir: Path = DEFAULT_PHASE416_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase298 = read_csv(phase298_dir / "phase298_acceptance_summary.csv")
    schema = read_csv(phase298_dir / "phase298_raw_book_schema_audit.csv")
    phase416 = read_csv(phase416_dir / "phase416_acceptance_summary.csv")
    if phase298.empty or schema.empty or phase416.empty:
        raise FileNotFoundError("Phase417 requires Phase298 and Phase416 evidence.")
    pairs = build_pair_catalog()
    contract = build_contract()
    freeze = build_parameter_freeze(pairs)
    inputs = build_input_registry(phase298, schema, phase416, pairs)
    exec_gates = build_execution_hard_gates()
    gates = build_gate_evaluation(inputs, contract, freeze, exec_gates)
    acceptance = build_acceptance(contract, pairs, freeze, gates)
    contract.to_csv(output_dir / "phase417_frozen_thesis_contract.csv", index=False)
    pairs.to_csv(output_dir / "phase417_pair_catalog.csv", index=False)
    freeze.to_csv(output_dir / "phase417_parameter_freeze.csv", index=False)
    inputs.to_csv(output_dir / "phase417_input_registry.csv", index=False)
    exec_gates.to_csv(output_dir / "phase417_execution_hard_gate_contract.csv", index=False)
    gates.to_csv(output_dir / "phase417_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase417_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, contract, pairs, freeze, inputs, exec_gates, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase417_pair_spread_convergence_precommit",
        **reproducibility_fields(
            artifact_id="phase417_pair_spread_convergence_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase298_acceptance_summary": str(phase298_dir / "phase298_acceptance_summary.csv"),
                "phase416_acceptance_summary": str(phase416_dir / "phase416_acceptance_summary.csv"),
            },
            parameters={"thesis_id": THESIS_ID, "parameter_freeze_hash": sha256_frame(freeze), "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase417_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase417_taker_pair_next_tick_precommit",
        ),
    }
    (output_dir / "phase417_pair_spread_convergence_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase417 pair-spread convergence precommit.")
    parser.add_argument("--phase298-dir", type=Path, default=DEFAULT_PHASE298_DIR)
    parser.add_argument("--phase416-dir", type=Path, default=DEFAULT_PHASE416_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase298_dir, args.phase416_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

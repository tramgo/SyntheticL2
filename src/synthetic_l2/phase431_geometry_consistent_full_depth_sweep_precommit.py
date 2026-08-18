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
from synthetic_l2.phase427_broader_full_depth_feature_family_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    COST_MULTIPLIER,
    FEATURE_FAMILIES,
    IMBALANCE_THRESHOLDS,
    INITIAL_CAPITAL_INR,
    LOOKBACK_TICKS,
    MIN_COMPLETED_ROUND_TRIPS,
    MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT,
    MIN_POSITIVE_DATE_FRACTION,
    MIN_SYMBOLS,
    MIN_TRADE_DATES,
    ORDER_NOTIONAL_INR,
    SPREAD_BPS_BUCKETS,
    DEPTH_CHANGE_THRESHOLDS,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE427_DIR = Path("outputs/phase427")
DEFAULT_PHASE430_DIR = Path("outputs/phase430")
DEFAULT_OUTPUT_DIR = Path("outputs/phase431")

THESIS_ID = "P431_GEOMETRY_CONSISTENT_FULL_DEPTH_FEATURE_SWEEP"
NEXT_ACTION = "run_phase432_geometry_consistent_full_depth_feature_sweep_no_paper_live"
REPAIR_ACTION = "repair_phase431_geometry_consistent_precommit"

FORWARD_TICKS = [3]
MIN_FORWARD_HOLD_MS = 250.0
SYNTHETIC_MAX_HOLD_TICKS = 2500
REAL_ANCHOR_MAX_HOLD_TICKS = 500
EXPECTED_GRID_ROWS = 2 * len(FEATURE_FAMILIES) * len(LOOKBACK_TICKS) * len(FORWARD_TICKS) * len(SPREAD_BPS_BUCKETS) * len(IMBALANCE_THRESHOLDS) * len(DEPTH_CHANGE_THRESHOLDS)


def sha256_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_csv(index=False, lineterminator="\n").encode("utf-8")).hexdigest()


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def build_geometry_grid() -> pd.DataFrame:
    rows = []
    for panel, max_hold in [("synthetic", SYNTHETIC_MAX_HOLD_TICKS), ("real_anchor", REAL_ANCHOR_MAX_HOLD_TICKS)]:
        for family_id, _ in FEATURE_FAMILIES:
            for lookback in LOOKBACK_TICKS:
                for forward in FORWARD_TICKS:
                    for spread in SPREAD_BPS_BUCKETS:
                        for imb in IMBALANCE_THRESHOLDS:
                            for depth in DEPTH_CHANGE_THRESHOLDS:
                                rows.append(
                                    {
                                        "scenario_id": f"P432_{panel}_{family_id}_L{lookback}_F{forward}_M{max_hold}_S{str(spread).replace('.', 'p')}_I{str(imb).replace('.', 'p')}_D{str(depth).replace('.', 'p')}",
                                        "panel": panel,
                                        "family_id": family_id,
                                        "lookback_ticks": lookback,
                                        "forward_ticks": forward,
                                        "min_forward_hold_ms": MIN_FORWARD_HOLD_MS,
                                        "max_hold_ticks": max_hold,
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
            ("thesis_id", THESIS_ID, "Geometry-consistent repair precommit after Phase430."),
            ("relationship_to_phase427", "same_feature_threshold_grid_with_timing_geometry_repair_only", "Feature thresholds are preserved; only max-hold geometry is repaired."),
            ("synthetic_geometry", f"forward_ticks=3;min_hold_ms={MIN_FORWARD_HOLD_MS};max_hold_ticks={SYNTHETIC_MAX_HOLD_TICKS}", "From Phase430 synthetic feasibility recommendation."),
            ("real_anchor_geometry", f"forward_ticks=3;min_hold_ms={MIN_FORWARD_HOLD_MS};max_hold_ticks={REAL_ANCHOR_MAX_HOLD_TICKS}", "From Phase430 real-anchor feasibility recommendation."),
            ("scenario_rows", len(grid), "Frozen repaired grid rows."),
            ("families", ";".join(f for f, _ in FEATURE_FAMILIES), "Same Phase427 feature families."),
            ("execution_profile", "single_name_taker_entry_taker_exit_exact_forward_ticks_cost200", "No passive fills or maker rebate."),
            ("full_depth_required", "L1_to_L5_price_quantity_orders_levels_2_to_5_materiality", "Primary scenarios require top-five book state."),
            ("controls", "l1_only_removed_depth;side_flip;real_anchor_cross_check", "Controls must be reported."),
            ("cost_model", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha equity intraday NSE formula."),
            ("capital", f"initial={INITIAL_CAPITAL_INR};order_notional={ORDER_NOTIONAL_INR}", "Fixed capital denominator."),
            ("acceptance", f"round_trips>={MIN_COMPLETED_ROUND_TRIPS};dates>={MIN_TRADE_DATES};symbols>={MIN_SYMBOLS};positive_date_fraction>={MIN_POSITIVE_DATE_FRACTION};annualized>={ANNUALIZED_THRESHOLD_PCT};l2_l5_edge_delta>={MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT}", "Strict acceptance remains unchanged."),
            ("forbidden", "feature_threshold_tuning;pair_spread_rescue;queue_depletion_threshold_rescue;market_maker_rescue;promotion;paper_live;deployable_claim", "Closed routes and boundaries."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_input_registry(phase427: pd.DataFrame, phase430: pd.DataFrame, rec: pd.DataFrame, grid: pd.DataFrame) -> pd.DataFrame:
    syn = rec[rec["panel"].eq("synthetic")].iloc[0] if not rec[rec["panel"].eq("synthetic")].empty else pd.Series(dtype=object)
    real = rec[rec["panel"].eq("real_anchor")].iloc[0] if not rec[rec["panel"].eq("real_anchor")].empty else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            ("phase427_grid_rows", scalar(phase427, "phase427_scenario_grid_rows", ""), "Original broad sweep grid."),
            ("phase430_audit_complete", scalar(phase430, "phase430_timing_geometry_audit_complete", ""), "Timing audit complete."),
            ("phase430_timing_repair_precommit_allowed", scalar(phase430, "phase430_timing_repair_precommit_allowed", ""), "Must be one."),
            ("phase430_synthetic_recommended_forward_ticks", syn.get("recommended_forward_ticks", ""), "Phase430 synthetic recommendation."),
            ("phase430_synthetic_recommended_max_hold_ticks", syn.get("recommended_max_hold_ticks", ""), "Phase430 synthetic recommendation."),
            ("phase430_synthetic_feasible_fraction", syn.get("feasible_fraction", ""), "Phase430 synthetic recommendation."),
            ("phase430_real_recommended_forward_ticks", real.get("recommended_forward_ticks", ""), "Phase430 real-anchor recommendation."),
            ("phase430_real_recommended_max_hold_ticks", real.get("recommended_max_hold_ticks", ""), "Phase430 real-anchor recommendation."),
            ("phase430_real_feasible_fraction", real.get("feasible_fraction", ""), "Phase430 real-anchor recommendation."),
            ("phase431_grid_rows", len(grid), "Repaired grid rows."),
            ("execution_results_generated_now", 0, "Precommit only."),
        ],
        columns=["input_id", "value", "description"],
    )


def build_execution_hard_gates() -> pd.DataFrame:
    gates = [
        ("P432_PHASE431_PRECOMMIT_USED", "Execution must read Phase431 geometry grid."),
        ("P432_PANEL_SPECIFIC_GEOMETRY", "Synthetic uses max_hold=2500; real-anchor uses max_hold=500."),
        ("P432_NO_FEATURE_THRESHOLD_TUNING", "Feature thresholds must match Phase427 grid dimensions."),
        ("P432_EXACT_FORWARD_TICK_INDEXING", "Every trade exit uses exact post-entry tick indexing."),
        ("P432_FULL_DEPTH_PRIMARY_FEATURES", "Primary scenarios require L2-L5 features."),
        ("P432_L1_ONLY_CONTROL", "Run removed-depth control for top/surviving scenarios."),
        ("P432_SIDE_FLIP_CONTROL", "Run side-flip control for top/surviving scenarios."),
        ("P432_COST200_FIXED_CAPITAL", "Use Zerodha cost200 and fixed INR 1,000,000 capital."),
        ("P432_BREADTH_AND_RETURN_GATES", "Apply event/date/symbol/positive-date/annualized gates."),
        ("P432_REAL_ANCHOR_CROSS_CHECK", "Replay top synthetic candidates using real-anchor geometry."),
        ("P432_BOUNDARIES_CLOSED", "No promotion, paper/live or deployable claim."),
    ]
    return pd.DataFrame([{"gate_id": gate, "requirement": requirement, "severity": "hard", "phase431_precommitted": 1} for gate, requirement in gates])


def build_gates(inputs: pd.DataFrame, contract: pd.DataFrame, grid: pd.DataFrame, exec_gates: pd.DataFrame) -> pd.DataFrame:
    values = dict(zip(inputs["input_id"], inputs["value"]))
    forbidden = ";".join(contract.loc[contract["contract_id"].eq("forbidden"), "contract_value"].astype(str))
    gates = [
        ("P431_PHASE430_COMPLETE", str(values.get("phase430_audit_complete", "")) == "1", values.get("phase430_audit_complete", ""), 1),
        ("P431_TIMING_REPAIR_ALLOWED", str(values.get("phase430_timing_repair_precommit_allowed", "")) == "1", values.get("phase430_timing_repair_precommit_allowed", ""), 1),
        ("P431_SYNTHETIC_GEOMETRY_MATCHES_AUDIT", as_int(values.get("phase430_synthetic_recommended_max_hold_ticks", 0)) == SYNTHETIC_MAX_HOLD_TICKS, values.get("phase430_synthetic_recommended_max_hold_ticks", ""), SYNTHETIC_MAX_HOLD_TICKS),
        ("P431_REAL_GEOMETRY_MATCHES_AUDIT", as_int(values.get("phase430_real_recommended_max_hold_ticks", 0)) == REAL_ANCHOR_MAX_HOLD_TICKS, values.get("phase430_real_recommended_max_hold_ticks", ""), REAL_ANCHOR_MAX_HOLD_TICKS),
        ("P431_FEATURE_THRESHOLDS_NOT_TUNED", set(grid["forward_ticks"].unique()) == {3} and sorted(grid["lookback_ticks"].unique().tolist()) == LOOKBACK_TICKS and sorted(grid["imbalance_threshold"].unique().tolist()) == IMBALANCE_THRESHOLDS, "phase427_threshold_dimensions_preserved_except_forward_bucket_repair", "preserved"),
        ("P431_PANEL_GEOMETRY_GRID_FROZEN", len(grid) == EXPECTED_GRID_ROWS, len(grid), EXPECTED_GRID_ROWS),
        ("P431_COST200_FIXED_CAPITAL_PINNED", COST_MULTIPLIER == 2.0 and INITIAL_CAPITAL_INR == 1_000_000.0, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR}", "cost200_fixed_capital"),
        ("P431_EXECUTION_HARD_GATES_PRECOMMITTED", len(exec_gates) == 11, len(exec_gates), 11),
        ("P431_RESULTS_NOT_GENERATED", as_int(values.get("execution_results_generated_now", 1)) == 0, values.get("execution_results_generated_now", ""), 0),
        ("P431_FORBIDDEN_ROUTES_CLOSED", all(x in forbidden for x in ["feature_threshold_tuning", "pair_spread_rescue", "queue_depletion_threshold_rescue", "promotion"]), forbidden, "closed_routes_listed"),
        ("P431_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(grid: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase431_geometry_consistent_precommit_complete", 1, "Phase431 precommit completed"),
            ("phase431_thesis_id", THESIS_ID, "Frozen thesis"),
            ("phase431_grid_rows", len(grid), "Frozen geometry-consistent rows"),
            ("phase431_parameter_grid_hash", sha256_frame(grid), "Hash of frozen grid"),
            ("phase431_synthetic_max_hold_ticks", SYNTHETIC_MAX_HOLD_TICKS, "Synthetic repaired max hold"),
            ("phase431_real_anchor_max_hold_ticks", REAL_ANCHOR_MAX_HOLD_TICKS, "Real-anchor repaired max hold"),
            ("phase431_forward_ticks", ";".join(map(str, FORWARD_TICKS)), "Forward tick bucket"),
            ("phase431_execution_results_generated", 0, "Precommit only"),
            ("phase431_strategy_promotion_allowed", 0, "No promotion"),
            ("phase431_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase431_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase431_execution_allowed_next", int(hard_pass == hard_rows), "Whether Phase432 may run"),
            ("phase431_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase431_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase431_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, contract: pd.DataFrame, inputs: pd.DataFrame, exec_gates: pd.DataFrame, gates: pd.DataFrame, grid: pd.DataFrame) -> None:
    lines = [
        "# Phase431 Geometry-Consistent Full-Depth Sweep Precommit",
        "",
        "Phase431 freezes a timing-geometry repair before rerunning the broader full-depth feature-family sweep.",
        "",
        "Only execution geometry is repaired. Feature thresholds remain inherited from Phase427; no signal tuning is performed.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Frozen Contract",
        "",
        _markdown_table(contract),
        "",
        "## Input Registry",
        "",
        _markdown_table(inputs),
        "",
        "## Phase432 Hard-Gate Contract",
        "",
        _markdown_table(exec_gates),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "## Repaired Grid Sample",
        "",
        _markdown_table(grid.head(30)),
        "",
        "No Phase431 strategy result, promotion, paper/live acceptance or deployable claim is generated.",
    ]
    (output_dir / "phase431_geometry_consistent_full_depth_sweep_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase427_dir: Path = DEFAULT_PHASE427_DIR, phase430_dir: Path = DEFAULT_PHASE430_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase427 = read_csv(phase427_dir / "phase427_acceptance_summary.csv")
    phase430 = read_csv(phase430_dir / "phase430_acceptance_summary.csv")
    rec = read_csv(phase430_dir / "phase430_recommended_timing_geometry.csv")
    if phase427.empty or phase430.empty or rec.empty:
        raise FileNotFoundError("Phase431 requires Phase427 and Phase430 outputs.")
    grid = build_geometry_grid()
    contract = build_contract(grid)
    inputs = build_input_registry(phase427, phase430, rec, grid)
    exec_gates = build_execution_hard_gates()
    gates = build_gates(inputs, contract, grid, exec_gates)
    acceptance = build_acceptance(grid, gates)
    contract.to_csv(output_dir / "phase431_frozen_contract.csv", index=False)
    grid.to_csv(output_dir / "phase431_geometry_consistent_parameter_grid.csv", index=False)
    inputs.to_csv(output_dir / "phase431_input_registry.csv", index=False)
    exec_gates.to_csv(output_dir / "phase431_execution_hard_gate_contract.csv", index=False)
    gates.to_csv(output_dir / "phase431_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase431_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, contract, inputs, exec_gates, gates, grid)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase431_geometry_consistent_full_depth_sweep_precommit",
        **reproducibility_fields(
            artifact_id="phase431_geometry_consistent_full_depth_sweep_precommit",
            generated_utc=generated_utc,
            inputs={"phase427_acceptance_summary": str(phase427_dir / "phase427_acceptance_summary.csv"), "phase430_recommended_timing_geometry": str(phase430_dir / "phase430_recommended_timing_geometry.csv")},
            parameters={"thesis_id": THESIS_ID, "parameter_grid_hash": sha256_frame(grid), "next_action": NEXT_ACTION},
            outputs={"acceptance_summary": str(output_dir / "phase431_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase431_geometry_consistent_precommit",
        ),
    }
    (output_dir / "phase431_geometry_consistent_full_depth_sweep_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase431 geometry-consistent full-depth sweep precommit.")
    parser.add_argument("--phase427-dir", type=Path, default=DEFAULT_PHASE427_DIR)
    parser.add_argument("--phase430-dir", type=Path, default=DEFAULT_PHASE430_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase427_dir, args.phase430_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

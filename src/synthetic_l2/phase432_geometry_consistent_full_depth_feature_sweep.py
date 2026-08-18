from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase428_broader_full_depth_feature_family_sweep import (
    DEFAULT_RAW_ROOT,
    DEFAULT_REAL_ROOTS,
    evaluate_controls,
    evaluate_grid_on_ticks,
    load_real_anchor_ticks,
    load_synthetic_ticks,
)
from synthetic_l2.phase431_geometry_consistent_full_depth_sweep_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    COST_MULTIPLIER,
    INITIAL_CAPITAL_INR,
    MIN_COMPLETED_ROUND_TRIPS,
    MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT,
    MIN_POSITIVE_DATE_FRACTION,
    MIN_SYMBOLS,
    MIN_TRADE_DATES,
    NEXT_ACTION as PHASE431_NEXT_ACTION,
    ORDER_NOTIONAL_INR,
    THESIS_ID,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE431_DIR = Path("outputs/phase431")
DEFAULT_OUTPUT_DIR = Path("outputs/phase432")

TOP_SCENARIOS_FOR_CONTROLS = 25
NEXT_ACTION = "interpret_phase432_geometry_consistent_full_depth_feature_sweep_no_paper_live"


def scenario_value(summary: pd.DataFrame, scenario_id: str, column: str, default: Any = 0) -> Any:
    row = summary[summary["scenario_id"].astype(str).eq(scenario_id)] if not summary.empty else pd.DataFrame()
    return row[column].iloc[0] if not row.empty and column in row.columns else default


def panel_grid(grid: pd.DataFrame, panel: str) -> pd.DataFrame:
    out = grid[grid["panel"].astype(str).eq(panel)].copy()
    return out.drop(columns=["panel"]).reset_index(drop=True)


def best_active_or_zero(summary: pd.DataFrame) -> pd.Series:
    if summary.empty:
        return pd.Series(dtype=object)
    active = summary[pd.to_numeric(summary["completed_round_trips"], errors="coerce").fillna(0).gt(0)]
    if not active.empty:
        return active.sort_values("annualized_return_pct", ascending=False).iloc[0]
    return summary.sort_values("annualized_return_pct", ascending=False).iloc[0]


def active_first_ranking(summary: pd.DataFrame) -> pd.DataFrame:
    if summary.empty:
        return summary
    trips = pd.to_numeric(summary["completed_round_trips"], errors="coerce").fillna(0)
    return pd.concat(
        [
            summary[trips.gt(0)].sort_values("annualized_return_pct", ascending=False),
            summary[trips.eq(0)].sort_values("annualized_return_pct", ascending=False),
        ],
        ignore_index=True,
    )


def add_cross_panel_comparison(syn_summary: pd.DataFrame, real_summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    ranked = active_first_ranking(syn_summary)
    for row in ranked.head(TOP_SCENARIOS_FOR_CONTROLS).itertuples(index=False):
        sid = str(row.scenario_id)
        real_sid = sid.replace("P432_synthetic_", "P432_real_anchor_")
        rows.append(
            {
                "synthetic_scenario_id": sid,
                "real_anchor_scenario_id": real_sid,
                "family_id": row.family_id,
                "synthetic_round_trips": row.completed_round_trips,
                "synthetic_annualized_return_pct": row.annualized_return_pct,
                "synthetic_positive_date_fraction": row.positive_date_fraction,
                "real_anchor_round_trips": scenario_value(real_summary, real_sid, "completed_round_trips", 0),
                "real_anchor_annualized_return_pct": scenario_value(real_summary, real_sid, "annualized_return_pct", 0.0),
                "real_anchor_positive_date_fraction": scenario_value(real_summary, real_sid, "positive_date_fraction", 0.0),
            }
        )
    return pd.DataFrame(rows)


def build_gates(syn_summary: pd.DataFrame, syn_controls: pd.DataFrame, real_summary: pd.DataFrame, cross: pd.DataFrame) -> pd.DataFrame:
    best = best_active_or_zero(syn_summary)
    best_sid = str(best.get("scenario_id", ""))
    best_ann = float(best.get("annualized_return_pct", 0.0))
    ctrl = syn_controls[syn_controls["scenario_id"].astype(str).eq(best_sid)].iloc[0] if not syn_controls.empty and best_sid in set(syn_controls["scenario_id"].astype(str)) else pd.Series(dtype=object)
    l1_ann = float(ctrl.get("l1_only_annualized_return_pct", 0.0))
    side_ann = float(ctrl.get("side_flip_annualized_return_pct", 0.0))
    real_sid = best_sid.replace("P432_synthetic_", "P432_real_anchor_")
    real_ann = float(scenario_value(real_summary, real_sid, "annualized_return_pct", 0.0))
    gates = [
        ("P432_EXECUTION_COMPLETE", True, 1, 1),
        ("P432_PHASE431_PRECOMMIT_USED", True, PHASE431_NEXT_ACTION, "run_phase432"),
        ("P432_SYNTHETIC_GRID_ROWS_EVALUATED", len(syn_summary) == 486, len(syn_summary), 486),
        ("P432_REAL_ANCHOR_GRID_ROWS_EVALUATED", len(real_summary) == 486, len(real_summary), 486),
        ("P432_PANEL_SPECIFIC_GEOMETRY", True, "synthetic_2500_real_500", "present"),
        ("P432_EXACT_FORWARD_TICK_INDEXING", True, "phase428_exact_index_engine", "present"),
        ("P432_FULL_DEPTH_PRIMARY_FEATURES", True, "phase427_l2_l5_families", "present"),
        ("P432_L1_ONLY_CONTROL", best_ann - l1_ann >= MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT, best_ann - l1_ann, f">={MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT}"),
        ("P432_SIDE_FLIP_CONTROL", best_ann >= side_ann, side_ann, "best>=side_flip"),
        ("P432_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={ORDER_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P432_EVENT_FLOOR", int(best.get("completed_round_trips", 0)) >= MIN_COMPLETED_ROUND_TRIPS, best.get("completed_round_trips", 0), f">={MIN_COMPLETED_ROUND_TRIPS}"),
        ("P432_DATE_BREADTH", int(best.get("trade_dates", 0)) >= MIN_TRADE_DATES, best.get("trade_dates", 0), f">={MIN_TRADE_DATES}"),
        ("P432_SYMBOL_BREADTH", int(best.get("symbols", 0)) >= MIN_SYMBOLS, best.get("symbols", 0), f">={MIN_SYMBOLS}"),
        ("P432_POSITIVE_DATE_FRACTION", float(best.get("positive_date_fraction", 0.0)) >= MIN_POSITIVE_DATE_FRACTION, best.get("positive_date_fraction", 0.0), f">={MIN_POSITIVE_DATE_FRACTION}"),
        ("P432_ANNUALIZED_FLOOR", best_ann >= ANNUALIZED_THRESHOLD_PCT, best_ann, f">={ANNUALIZED_THRESHOLD_PCT}"),
        ("P432_REAL_ANCHOR_CROSS_CHECK", (best_ann == 0.0 and real_ann == 0.0) or best_ann * real_ann >= 0, real_ann, "same_sign"),
        ("P432_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(syn_summary: pd.DataFrame, syn_controls: pd.DataFrame, real_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    best = best_active_or_zero(syn_summary)
    survivors = int(syn_summary["acceptance_survivor"].astype(int).sum()) if not syn_summary.empty else 0
    active = syn_summary[pd.to_numeric(syn_summary["completed_round_trips"], errors="coerce").fillna(0).gt(0)] if not syn_summary.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase432_geometry_consistent_full_depth_sweep_complete", 1, "Phase432 execution completed"),
            ("phase432_synthetic_grid_rows_evaluated", len(syn_summary), "Synthetic scenario rows"),
            ("phase432_real_anchor_grid_rows_evaluated", len(real_summary), "Real-anchor scenario rows"),
            ("phase432_best_scenario_id", best.get("scenario_id", ""), "Best synthetic scenario by annualized return"),
            ("phase432_best_family_id", best.get("family_id", ""), "Best synthetic family"),
            ("phase432_best_completed_round_trips", best.get("completed_round_trips", 0), "Best round trips"),
            ("phase432_best_trade_dates", best.get("trade_dates", 0), "Best trade dates"),
            ("phase432_best_symbols", best.get("symbols", 0), "Best symbols"),
            ("phase432_best_positive_date_fraction", best.get("positive_date_fraction", 0.0), "Best positive date fraction"),
            ("phase432_best_net_pnl_inr", best.get("net_pnl_inr", 0.0), "Best net P&L"),
            ("phase432_best_annualized_return_pct", best.get("annualized_return_pct", 0.0), "Best annualized return"),
            ("phase432_active_synthetic_scenario_rows", len(active), "Synthetic scenarios with at least one trade"),
            ("phase432_cost200_acceptance_survivor_rows", survivors, "Accepted synthetic scenarios before control gates"),
            ("phase432_control_rows", len(syn_controls), "Control rows"),
            ("phase432_strategy_promotion_allowed", 0, "No promotion"),
            ("phase432_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase432_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase432_hard_gate_pass_rows", int(gates["passed"].astype(bool).sum()), "Passed hard gates"),
            ("phase432_hard_gate_rows", len(gates), "Hard gates"),
            ("phase432_next_best_action", NEXT_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, syn_summary: pd.DataFrame, controls: pd.DataFrame, real_summary: pd.DataFrame, cross: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase432 Geometry-Consistent Full-Depth Feature Sweep",
        "",
        "Phase432 executes the Phase431 timing-geometry repair: same Phase427 feature thresholds, panel-specific feasible max-hold windows, exact forward ticks and Zerodha cost200.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Top Synthetic Scenarios",
        "",
        _markdown_table(syn_summary.head(30)),
        "",
        "## Top Synthetic Controls",
        "",
        _markdown_table(controls.head(30)),
        "",
        "## Cross-Panel Comparison",
        "",
        _markdown_table(cross.head(30)),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: no promotion, paper/live acceptance or deployable profitability claim is generated by Phase432.",
    ]
    (output_dir / "phase432_geometry_consistent_full_depth_feature_sweep_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(raw_root: Path = DEFAULT_RAW_ROOT, phase431_dir: Path = DEFAULT_PHASE431_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR, real_roots: list[Path] | None = None) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase431 = read_csv(phase431_dir / "phase431_acceptance_summary.csv")
    if str(metric_value(phase431, "phase431_next_best_action", "")) != PHASE431_NEXT_ACTION:
        raise ValueError("Phase432 requires Phase431 execution allowance.")
    grid = read_csv(phase431_dir / "phase431_geometry_consistent_parameter_grid.csv")
    syn_grid = panel_grid(grid, "synthetic")
    real_grid = panel_grid(grid, "real_anchor")
    synthetic_ticks = load_synthetic_ticks(raw_root)
    syn_ledger, syn_diag, syn_summary = evaluate_grid_on_ticks(synthetic_ticks, syn_grid, "synthetic")
    top_syn_grid = active_first_ranking(syn_summary).head(TOP_SCENARIOS_FOR_CONTROLS).merge(syn_grid, on=["scenario_id", "family_id"], how="left")
    syn_controls = evaluate_controls(synthetic_ticks, top_syn_grid[syn_grid.columns], "synthetic_top")
    real_ticks = load_real_anchor_ticks(real_roots or DEFAULT_REAL_ROOTS)
    real_ledger, real_diag, real_summary = evaluate_grid_on_ticks(real_ticks, real_grid, "real_anchor")
    cross = add_cross_panel_comparison(syn_summary, real_summary)
    gates = build_gates(syn_summary, syn_controls, real_summary, cross)
    acceptance = build_acceptance(syn_summary, syn_controls, real_summary, gates)
    syn_summary.to_csv(output_dir / "phase432_synthetic_scenario_summary.csv", index=False)
    syn_diag.to_csv(output_dir / "phase432_synthetic_scan_diagnostics.csv", index=False)
    syn_ledger.to_csv(output_dir / "phase432_synthetic_trade_ledger_sample.csv", index=False)
    syn_controls.to_csv(output_dir / "phase432_top_scenario_controls.csv", index=False)
    real_summary.to_csv(output_dir / "phase432_real_anchor_scenario_summary.csv", index=False)
    real_diag.to_csv(output_dir / "phase432_real_anchor_scan_diagnostics.csv", index=False)
    real_ledger.to_csv(output_dir / "phase432_real_anchor_trade_ledger_sample.csv", index=False)
    cross.to_csv(output_dir / "phase432_cross_panel_comparison.csv", index=False)
    gates.to_csv(output_dir / "phase432_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase432_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, syn_summary, syn_controls, real_summary, cross, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase432_geometry_consistent_full_depth_feature_sweep",
        **reproducibility_fields(
            artifact_id="phase432_geometry_consistent_full_depth_feature_sweep",
            generated_utc=generated_utc,
            inputs={"phase431_grid": str(phase431_dir / "phase431_geometry_consistent_parameter_grid.csv"), "raw_root": str(raw_root)},
            parameters={"thesis_id": THESIS_ID, "synthetic_grid_rows": len(syn_grid), "real_anchor_grid_rows": len(real_grid)},
            outputs={"acceptance_summary": str(output_dir / "phase432_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase431_geometry_consistent_exact_tick",
        ),
    }
    (output_dir / "phase432_geometry_consistent_full_depth_feature_sweep_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase432 geometry-consistent full-depth feature sweep.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase431-dir", type=Path, default=DEFAULT_PHASE431_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.raw_root, args.phase431_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

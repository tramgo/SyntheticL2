from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase255_richer_raw_depth_feature_quality_interpretation import safe_float
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE288_DIR = Path("outputs/phase288")
DEFAULT_OUTPUT_DIR = Path("outputs/phase289")

SELECTED_NEXT_ROUTE = "P289_ADAPTIVE_FULL_DEPTH_LIQUIDITY_PRESSURE_EXPANSION_SEARCH"
NEXT_ACTION = "run_phase290_adaptive_full_depth_liquidity_pressure_expansion_search_no_paper_live"
REPAIR_ACTION = "repair_phase289_full_depth_liquidity_pressure_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
SPARSE_DIAGNOSTIC_EVENT_FLOOR = 8
ROBUST_PORTFOLIO_EVENT_FLOOR = 30


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    return out


def build_ranked_pressure_interpretation(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    frame = numeric(
        scenarios,
        [
            "mechanical_one_date_annualized_portfolio_return_pct",
            "realized_net_pnl_inr",
            "scheduled_event_rows",
            "selected_event_rows",
            "sparse_diagnostic_event_floor_met",
            "robust_portfolio_event_floor_met",
            "cost200_above12_sparse_diagnostic",
            "robust_portfolio_floor_above12",
            "uses_top5",
            "uses_levels_2_to_5",
            "l1_only_variant",
            "uses_net_edge_as_live_mask",
            "initial_capital_inr",
            "fixed_notional_inr",
            "max_concurrent_positions",
            "notional_turnover_x_initial_capital",
            "avg_open_notional_utilization",
            "rejected_same_symbol_overlap_rows",
            "rejected_max_concurrent_rows",
        ],
    )
    rows: list[dict[str, Any]] = []
    for variant_id, group in frame.groupby("phase288_variant_id", dropna=False):
        ranked = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False)
        best = ranked.iloc[0]
        max_ann = safe_float(best.get("mechanical_one_date_annualized_portfolio_return_pct", 0.0), 0.0)
        max_events = int(group["scheduled_event_rows"].max())
        rows.append(
            {
                "phase288_variant_id": str(variant_id),
                "liquidity_family": best.get("liquidity_family", ""),
                "pressure_column": best.get("pressure_column", ""),
                "side_mode": best.get("side_mode", ""),
                "exit_horizon_ticks": best.get("exit_horizon_ticks", ""),
                "scenario_rows": int(len(group)),
                "selected_event_rows": int(group["selected_event_rows"].max()),
                "max_scheduled_event_rows": max_events,
                "cost200_above12_sparse_diagnostic_rows": int(group["cost200_above12_sparse_diagnostic"].sum()),
                "robust_portfolio_floor_above12_rows": int(group["robust_portfolio_floor_above12"].sum()),
                "sparse_floor_met_rows": int(group["sparse_diagnostic_event_floor_met"].sum()),
                "robust_portfolio_floor_met_rows": int(group["robust_portfolio_event_floor_met"].sum()),
                "min_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].min()),
                "median_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].median()),
                "max_annualized_pct": max_ann,
                "max_net_pnl_inr": float(group["realized_net_pnl_inr"].max()),
                "best_scenario_id": best.get("scenario_id", ""),
                "best_initial_capital_inr": best.get("initial_capital_inr", ""),
                "best_fixed_notional_inr": best.get("fixed_notional_inr", ""),
                "best_max_concurrent_positions": best.get("max_concurrent_positions", ""),
                "best_notional_turnover_x_initial_capital": best.get("notional_turnover_x_initial_capital", ""),
                "best_avg_open_notional_utilization": best.get("avg_open_notional_utilization", ""),
                "rejected_same_symbol_overlap_rows": int(group["rejected_same_symbol_overlap_rows"].max()),
                "rejected_max_concurrent_rows": int(group["rejected_max_concurrent_rows"].max()),
                "uses_top5": as_int(best.get("uses_top5", 0)),
                "uses_levels_2_to_5": as_int(best.get("uses_levels_2_to_5", 0)),
                "l1_only_variant": as_int(best.get("l1_only_variant", 0)),
                "uses_net_edge_as_live_mask": as_int(best.get("uses_net_edge_as_live_mask", 0)),
                "positive_but_below12": int(0.0 < max_ann < ANNUALIZED_THRESHOLD_PCT),
                "too_sparse_for_sparse_diagnostic": int(max_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR),
                "too_sparse_for_portfolio_claim": int(max_events < ROBUST_PORTFOLIO_EVENT_FLOOR),
                "full_depth_positive_clue": int(max_ann > 0.0 and as_int(best.get("uses_levels_2_to_5", 0)) == 1 and as_int(best.get("l1_only_variant", 0)) == 0),
                "same_pressure_route_exhausted_for_acceptance": int(max_ann < ANNUALIZED_THRESHOLD_PCT or max_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR),
            }
        )
    return pd.DataFrame(rows).sort_values(
        [
            "cost200_above12_sparse_diagnostic_rows",
            "robust_portfolio_floor_above12_rows",
            "full_depth_positive_clue",
            "max_annualized_pct",
            "max_scheduled_event_rows",
        ],
        ascending=[False, False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_family_interpretation(ranked: pd.DataFrame) -> pd.DataFrame:
    if ranked.empty:
        return pd.DataFrame()
    frame = numeric(
        ranked,
        [
            "scenario_rows",
            "selected_event_rows",
            "max_scheduled_event_rows",
            "cost200_above12_sparse_diagnostic_rows",
            "robust_portfolio_floor_above12_rows",
            "sparse_floor_met_rows",
            "robust_portfolio_floor_met_rows",
            "min_annualized_pct",
            "median_annualized_pct",
            "max_annualized_pct",
            "max_net_pnl_inr",
            "positive_but_below12",
            "full_depth_positive_clue",
        ],
    )
    rows: list[dict[str, Any]] = []
    for family, group in frame.groupby("liquidity_family", dropna=False):
        best = group.sort_values("max_annualized_pct", ascending=False).iloc[0]
        rows.append(
            {
                "liquidity_family": str(family),
                "variant_rows": int(group["phase288_variant_id"].astype(str).nunique()),
                "scenario_rows": int(group["scenario_rows"].sum()),
                "selected_event_rows_max": int(group["selected_event_rows"].max()),
                "max_scheduled_event_rows": int(group["max_scheduled_event_rows"].max()),
                "cost200_above12_sparse_diagnostic_rows": int(group["cost200_above12_sparse_diagnostic_rows"].sum()),
                "robust_portfolio_floor_above12_rows": int(group["robust_portfolio_floor_above12_rows"].sum()),
                "sparse_floor_met_rows": int(group["sparse_floor_met_rows"].sum()),
                "robust_portfolio_floor_met_rows": int(group["robust_portfolio_floor_met_rows"].sum()),
                "min_annualized_pct": float(group["min_annualized_pct"].min()),
                "median_annualized_pct": float(group["median_annualized_pct"].median()),
                "max_annualized_pct": float(group["max_annualized_pct"].max()),
                "max_net_pnl_inr": float(group["max_net_pnl_inr"].max()),
                "best_variant_id": best.get("phase288_variant_id", ""),
                "positive_but_below12_variants": int(group["positive_but_below12"].sum()),
                "full_depth_positive_clue_variants": int(group["full_depth_positive_clue"].sum()),
                "preserve_adaptive_expansion_clue": int(float(group["max_annualized_pct"].max()) > 0.0),
                "close_family_for_acceptance": int(int(group["cost200_above12_sparse_diagnostic_rows"].sum()) == 0),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["preserve_adaptive_expansion_clue", "max_annualized_pct", "max_scheduled_event_rows"],
        ascending=[False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_interpretation_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    scenarios = as_int(metric_value(summary, "phase288_scenario_rows", 0))
    above12 = as_int(metric_value(summary, "phase288_sparse_above12_scenario_rows", 0))
    robust_above12 = as_int(metric_value(summary, "phase288_robust_portfolio_above12_scenario_rows", 0))
    robust_floor = as_int(metric_value(summary, "phase288_robust_portfolio_floor_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase288_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase288_best_scheduled_event_rows", 0))
    l1_only = as_int(metric_value(summary, "phase288_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase288_net_edge_live_mask_rows", 0))
    positive_clues = int(ranked["full_depth_positive_clue"].astype(int).sum()) if not ranked.empty else 0
    return pd.DataFrame(
        [
            ("phase288_executed", f"scenario_rows={scenarios}", "evidence", int(scenarios > 0), "Phase288 executed the direct full-depth liquidity-pressure strategy search."),
            ("no_sparse_above12_survivor", f"sparse_above12_rows={above12};best_ann={best_ann}", "hard_negative", int(above12 == 0 and best_ann < ANNUALIZED_THRESHOLD_PCT), "No Phase288 scenario crossed the fixed-capital >12% sparse diagnostic threshold."),
            ("no_robust_portfolio_survivor", f"robust_floor_rows={robust_floor};robust_above12_rows={robust_above12};best_events={best_events}", "hard_negative", int(robust_floor == 0 and robust_above12 == 0), "No Phase288 scenario met robust breadth or robust above-12 evidence."),
            ("best_case_too_sparse", f"best_ann={best_ann};best_scheduled_events={best_events}", "risk", int(best_ann < ANNUALIZED_THRESHOLD_PCT and best_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR), "The best Phase288 result is below threshold and too sparse."),
            ("full_depth_boundary_preserved", f"l1_only={l1_only};live_label_leakage={leakage};positive_full_depth_clues={positive_clues}", "constraint", int(l1_only == 0 and leakage == 0), "Full top-five depth and no-live-leakage boundaries held."),
            ("same_pressure_route_should_close_for_acceptance", "cost200_above12=0;robust_above12=0", "decision", 1, "Do not accept the fixed-grid Phase288 pressure route."),
            ("next_route_should_expand_pressure_family_adaptively", SELECTED_NEXT_ROUTE, "next_action", 1, "Move to adaptive thresholds and family-specific pressure interactions instead of repeating the fixed grid."),
        ],
        columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"],
    )


def build_decision_ledger(summary: pd.DataFrame, ranked: pd.DataFrame, families: pd.DataFrame) -> pd.DataFrame:
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    above12 = as_int(metric_value(summary, "phase288_sparse_above12_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase288_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase288_best_scheduled_event_rows", 0))
    preserved = ";".join(families.loc[families["preserve_adaptive_expansion_clue"].astype(int).eq(1), "liquidity_family"].astype(str).tolist()) if not families.empty else ""
    return pd.DataFrame(
        [
            ("close_phase288_pressure_route_for_acceptance", int(above12 == 0), f"sparse_above12={above12};best_ann={best_ann};best_events={best_events}", "Do not accept, replay, or promote Phase288 pressure variants."),
            ("preserve_best_full_depth_pressure_clue", top.get("phase288_variant_id", ""), f"family={top.get('liquidity_family', '')};pressure={top.get('pressure_column', '')};scheduled_events={best_events}", "Carry forward only as a clue for adaptive expansion."),
            ("preserved_pressure_families_for_expansion", preserved, "positive full-depth but below-12 diagnostics", "Preserve families as search context, not as accepted strategies."),
            ("do_not_relax_annualized_denominator", 1, "fixed_initial_capital_required", "Annualized return remains fixed-capital based, never unlimited-capital based."),
            ("do_not_claim_portfolio_return", 1, f"best_scheduled_events={best_events};sparse_floor={SPARSE_DIAGNOSTIC_EVENT_FLOOR};robust_floor={ROBUST_PORTFOLIO_EVENT_FLOOR}", "Evidence is too sparse for a portfolio-return claim."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "fixed pressure grid exhausted; adaptive feature interactions required", "Run an adaptive full-depth pressure expansion search."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def decision_value(decisions: pd.DataFrame, decision_id: str) -> str:
    rows = decisions.loc[decisions["decision_id"].astype(str).eq(decision_id), "decision_value"] if not decisions.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_next_route_contract(families: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    top_clues = ranked[ranked["full_depth_positive_clue"].astype(int).eq(1)].head(12) if not ranked.empty else pd.DataFrame()
    clue_ids = ";".join(top_clues["phase288_variant_id"].astype(str).tolist()) if not top_clues.empty else ""
    family_ids = ";".join(families.loc[families["preserve_adaptive_expansion_clue"].astype(int).eq(1), "liquidity_family"].astype(str).tolist()) if not families.empty else ""
    return pd.DataFrame(
        [
            ("P290_INPUTS", "outputs/phase277/phase277_cost200_redesign_event_universe.csv;outputs/phase288/phase288_liquidity_pressure_scenario_results.csv;outputs/phase288/phase288_liquidity_pressure_variant_summary.csv", "Use event universe plus Phase288 failure evidence."),
            ("P290_PRESERVED_PHASE288_CLUES", clue_ids, "Carry forward positive full-depth pressure clues only as diagnostic context."),
            ("P290_PRESERVED_PRESSURE_FAMILIES", family_ids, "Keep positive but below-threshold families for adaptive expansion."),
            ("P290_SEARCH_TYPE", "adaptive_full_depth_liquidity_pressure_expansion_search", "Expand thresholds and feature interactions while preserving observable full-depth L2 masks."),
            ("P290_REQUIRED_DIRECTIONS", "family_specific_thresholds;pressure_feature_interactions;side_by_pressure_sign;horizon_by_spread_state;open_vs_nonopen_buckets;cost200_fixed_capital_scheduler", "Search more flexibly without using future labels as live masks."),
            ("P290_CAPITAL_AND_COST", "initial_capital_100000;cost200_required;fixed_notional_grid;max_concurrent_grid;annualized_denominator_fixed_capital", "No unlimited-capital annualized return."),
            ("P290_ACCEPTANCE_DIAGNOSTICS", f"cost200_annualized_pct_gt_{ANNUALIZED_THRESHOLD_PCT};scheduled_event_rows_ge_{SPARSE_DIAGNOSTIC_EVENT_FLOOR}_for_sparse_discovery;scheduled_event_rows_ge_{ROBUST_PORTFOLIO_EVENT_FLOOR}_for_portfolio_claim", "Sparse >12% remains discovery only; robust portfolio claim needs a larger event floor."),
            ("P290_BOUNDARY", "no_paper_live;no_strategy_replay;no_deployable_profitability_claim;l1_only_forbidden;net_edge_live_mask_forbidden", "Boundaries remain closed until evidence earns them."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_gate_evaluation(summary: pd.DataFrame, ranked: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase288_liquidity_pressure_search_complete", 0))
    next_action = str(metric_value(summary, "phase288_next_best_action", ""))
    hard_pass = as_int(metric_value(summary, "phase288_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(summary, "phase288_hard_gate_rows", 0))
    l1_only = as_int(metric_value(summary, "phase288_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase288_net_edge_live_mask_rows", 0))
    replay = as_int(metric_value(summary, "phase288_strategy_replay_allowed", 0))
    paper = as_int(metric_value(summary, "phase288_paper_or_live_acceptance_allowed", 0))
    claim = as_int(metric_value(summary, "phase288_deployable_profitability_claim_allowed", 0))
    gates = [
        ("P289_PHASE288_SEARCH_COMPLETE", complete == 1, complete, "Phase288 search complete"),
        ("P289_PHASE288_NEXT_ACTION_PRESENT", "phase289" in next_action, next_action, "Phase288 routes to Phase289 interpretation"),
        ("P289_PHASE288_GATES_PASS", hard_rows > 0 and hard_pass == hard_rows, f"{hard_pass}/{hard_rows}", "Phase288 gates pass"),
        ("P289_RANKED_INTERPRETATION_PRESENT", len(ranked) > 0, len(ranked), ">0 ranked variants"),
        ("P289_CLOSES_PHASE288_FOR_ACCEPTANCE", str(decision_value(decisions, "close_phase288_pressure_route_for_acceptance")) == "1", decision_value(decisions, "close_phase288_pressure_route_for_acceptance"), "Phase288 closed for acceptance"),
        ("P289_NEXT_ROUTE_SELECTED", str(decision_value(decisions, "selected_next_route")) == SELECTED_NEXT_ROUTE, decision_value(decisions, "selected_next_route"), SELECTED_NEXT_ROUTE),
        ("P289_FULL_DEPTH_BOUNDARY_PRESERVED", l1_only == 0 and leakage == 0, f"l1_only={l1_only};live_mask={leakage}", "full-depth, no leakage"),
        ("P289_BOUNDARIES_CLOSED", replay == 0 and paper == 0 and claim == 0, f"replay={replay};paper={paper};claim={claim}", "no replay/paper/live/claim"),
        ("P289_ROUTE_CONTRACT_PRESENT", len(route) >= 8, len(route), "Phase290 route contract rows"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def write_report(output_dir: Path, summary: pd.DataFrame, ranked: pd.DataFrame, families: pd.DataFrame, interpretation: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase289 Full-Depth Liquidity-Pressure Interpretation",
        "",
        "Phase289 interprets Phase288 as a no-survivor fixed-grid pressure search and selects adaptive full-depth liquidity-pressure expansion as the next route.",
        "",
        "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened.",
        "",
        "## Phase288 Summary",
        "",
        _markdown_table(summary),
        "",
        "## Ranked Pressure Interpretation",
        "",
        _markdown_table(ranked.head(20)),
        "",
        "## Family Interpretation",
        "",
        _markdown_table(families),
        "",
        "## Interpretation Ledger",
        "",
        _markdown_table(interpretation),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decisions),
        "",
        "## Phase290 Route Contract",
        "",
        _markdown_table(route),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase289_full_depth_liquidity_pressure_interpretation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(phase288_dir: Path = DEFAULT_PHASE288_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase288_dir / "phase288_acceptance_summary.csv")
    scenarios = read_csv(phase288_dir / "phase288_liquidity_pressure_scenario_results.csv")
    ranked = build_ranked_pressure_interpretation(scenarios)
    families = build_family_interpretation(ranked)
    interpretation = build_interpretation_ledger(summary, ranked)
    decisions = build_decision_ledger(summary, ranked, families)
    route = build_next_route_contract(families, ranked)
    gates = build_gate_evaluation(summary, ranked, decisions, route)

    ranked.to_csv(output_dir / "phase289_ranked_pressure_interpretation.csv", index=False)
    families.to_csv(output_dir / "phase289_pressure_family_interpretation.csv", index=False)
    interpretation.to_csv(output_dir / "phase289_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase289_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase289_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase289_gate_evaluation.csv", index=False)

    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    best = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    acceptance = pd.DataFrame(
        [
            ("phase289_interpretation_complete", 1, "Phase289 interpretation completed"),
            ("phase289_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
            ("phase289_phase288_variant_rows", as_int(metric_value(summary, "phase288_variant_rows", 0)), "Phase288 variants interpreted"),
            ("phase289_phase288_scenario_rows", as_int(metric_value(summary, "phase288_scenario_rows", 0)), "Phase288 scenarios interpreted"),
            ("phase289_phase288_sparse_above12_scenario_rows", as_int(metric_value(summary, "phase288_sparse_above12_scenario_rows", 0)), "Phase288 sparse above-12 rows"),
            ("phase289_phase288_robust_portfolio_floor_scenario_rows", as_int(metric_value(summary, "phase288_robust_portfolio_floor_scenario_rows", 0)), "Phase288 robust floor rows"),
            ("phase289_phase288_robust_portfolio_above12_scenario_rows", as_int(metric_value(summary, "phase288_robust_portfolio_above12_scenario_rows", 0)), "Phase288 robust above-12 rows"),
            ("phase289_best_phase288_variant_id", best.get("phase288_variant_id", ""), "Best interpreted Phase288 variant"),
            ("phase289_best_liquidity_family", best.get("liquidity_family", ""), "Best interpreted liquidity family"),
            ("phase289_best_pressure_column", best.get("pressure_column", ""), "Best interpreted pressure feature"),
            ("phase289_best_side_mode", best.get("side_mode", ""), "Best interpreted side mode"),
            ("phase289_best_cost200_annualized_pct", best.get("max_annualized_pct", ""), "Best fixed-capital annualized diagnostic"),
            ("phase289_best_scheduled_event_rows", best.get("max_scheduled_event_rows", ""), "Best scheduled events"),
            ("phase289_positive_full_depth_clue_variant_rows", int(ranked["full_depth_positive_clue"].astype(int).sum()) if not ranked.empty else 0, "Positive full-depth clue variants"),
            ("phase289_close_phase288_for_acceptance", decision_value(decisions, "close_phase288_pressure_route_for_acceptance"), "Close Phase288 route for acceptance"),
            ("phase289_do_not_relax_annualized_denominator", decision_value(decisions, "do_not_relax_annualized_denominator"), "Keep fixed-capital annualized denominator"),
            ("phase289_do_not_claim_portfolio_return", decision_value(decisions, "do_not_claim_portfolio_return"), "Do not claim portfolio return"),
            ("phase289_strategy_replay_allowed", 0, "No strategy replay unlocked"),
            ("phase289_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
            ("phase289_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
            ("phase289_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase289_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase289_hard_gate_rows", hard_rows, "Hard gates evaluated"),
            ("phase289_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    acceptance.to_csv(output_dir / "phase289_acceptance_summary.csv", index=False)
    write_report(output_dir, summary, ranked, families, interpretation, decisions, route, gates)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = reproducibility_fields(
        artifact_id="phase289",
        generated_utc=generated_utc,
        inputs={
            "phase288_acceptance_summary": str(phase288_dir / "phase288_acceptance_summary.csv"),
            "phase288_scenario_results": str(phase288_dir / "phase288_liquidity_pressure_scenario_results.csv"),
        },
        parameters={
            "selected_next_route": SELECTED_NEXT_ROUTE,
            "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
            "sparse_diagnostic_event_floor": SPARSE_DIAGNOSTIC_EVENT_FLOOR,
            "robust_portfolio_event_floor": ROBUST_PORTFOLIO_EVENT_FLOOR,
            "strategy_replay_allowed": 0,
            "paper_or_live_acceptance_allowed": 0,
            "deployable_profitability_claim_allowed": 0,
        },
        outputs={
            "acceptance_summary": str(output_dir / "phase289_acceptance_summary.csv"),
            "next_route_contract": str(output_dir / "phase289_next_route_contract.csv"),
            "gate_evaluation": str(output_dir / "phase289_gate_evaluation.csv"),
        },
        cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        latency_model_version="phase289_interpretation_no_new_latency_model",
    )
    manifest.update(
        {
            "generated_utc": generated_utc,
            "phase288_dir": str(phase288_dir),
            "output_dir": str(output_dir),
            "selected_next_route": SELECTED_NEXT_ROUTE,
            "next_action": NEXT_ACTION,
            "hard_gate_pass_rows": hard_pass,
            "hard_gate_rows": hard_rows,
        }
    )
    (output_dir / "phase289_full_depth_liquidity_pressure_interpretation_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase288-dir", type=Path, default=DEFAULT_PHASE288_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    print(json.dumps(run(args.phase288_dir, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

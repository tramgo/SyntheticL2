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


DEFAULT_PHASE292_DIR = Path("outputs/phase292")
DEFAULT_OUTPUT_DIR = Path("outputs/phase293")

SELECTED_NEXT_ROUTE = "P294_FULL_DEPTH_PRESSURE_ABSORPTION_CONTINUATION_SEARCH"
NEXT_ACTION = "run_phase294_full_depth_pressure_absorption_continuation_search_no_paper_live"
REPAIR_ACTION = "repair_phase293_adaptive_pressure_breadth_repair_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
SPARSE_DIAGNOSTIC_EVENT_FLOOR = 8
ROBUST_PORTFOLIO_EVENT_FLOOR = 30


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    return out


def build_ranked_breadth_repair_interpretation(scenarios: pd.DataFrame) -> pd.DataFrame:
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
    for variant_id, group in frame.groupby("phase292_variant_id", dropna=False):
        ranked = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False)
        best = ranked.iloc[0]
        max_ann = safe_float(best.get("mechanical_one_date_annualized_portfolio_return_pct", 0.0), 0.0)
        max_events = int(group["scheduled_event_rows"].max())
        rows.append(
            {
                "phase292_variant_id": str(variant_id),
                "repair_family": best.get("repair_family", ""),
                "primary_pressure_column": best.get("primary_pressure_column", ""),
                "interaction_column": best.get("interaction_column", ""),
                "spread_state": best.get("spread_state", ""),
                "market_bucket": best.get("market_bucket", ""),
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
                "above12_sparse_survivor": int(int(group["cost200_above12_sparse_diagnostic"].sum()) > 0),
                "robust_portfolio_survivor": int(int(group["robust_portfolio_floor_above12"].sum()) > 0),
                "positive_but_below12": int(0.0 < max_ann < ANNUALIZED_THRESHOLD_PCT),
                "too_sparse_for_sparse_diagnostic": int(max_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR),
                "too_sparse_for_portfolio_claim": int(max_events < ROBUST_PORTFOLIO_EVENT_FLOOR),
                "full_depth_positive_clue": int(max_ann > 0.0 and as_int(best.get("uses_levels_2_to_5", 0)) == 1 and as_int(best.get("l1_only_variant", 0)) == 0),
                "breadth_repair_exhausted_for_acceptance": int(max_ann <= ANNUALIZED_THRESHOLD_PCT or int(group["cost200_above12_sparse_diagnostic"].sum()) == 0),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["above12_sparse_survivor", "robust_portfolio_survivor", "full_depth_positive_clue", "max_annualized_pct", "max_scheduled_event_rows"],
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
    for family, group in frame.groupby("repair_family", dropna=False):
        best = group.sort_values("max_annualized_pct", ascending=False).iloc[0]
        rows.append(
            {
                "repair_family": str(family),
                "variant_rows": int(group["phase292_variant_id"].astype(str).nunique()),
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
                "best_variant_id": best.get("phase292_variant_id", ""),
                "full_depth_positive_clue_variants": int(group["full_depth_positive_clue"].sum()),
                "close_family_for_acceptance": int(int(group["cost200_above12_sparse_diagnostic_rows"].sum()) == 0),
                "preserve_as_contrarian_failure_evidence": int(float(group["max_annualized_pct"].max()) < ANNUALIZED_THRESHOLD_PCT),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["close_family_for_acceptance", "max_annualized_pct"],
        ascending=[True, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_interpretation_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    scenarios = as_int(metric_value(summary, "phase292_scenario_rows", 0))
    sparse_above12 = as_int(metric_value(summary, "phase292_sparse_above12_scenario_rows", 0))
    robust_above12 = as_int(metric_value(summary, "phase292_robust_portfolio_above12_scenario_rows", 0))
    robust_floor = as_int(metric_value(summary, "phase292_robust_portfolio_floor_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase292_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase292_best_scheduled_event_rows", 0))
    l1_only = as_int(metric_value(summary, "phase292_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase292_net_edge_live_mask_rows", 0))
    positive_clues = int(ranked["full_depth_positive_clue"].astype(int).sum()) if not ranked.empty else 0
    return pd.DataFrame(
        [
            ("phase292_executed", f"scenario_rows={scenarios}", "evidence", int(scenarios > 0), "Phase292 executed the breadth-repair search."),
            ("breadth_repair_failed_above12", f"sparse_above12={sparse_above12};best_ann={best_ann}", "hard_negative", int(sparse_above12 == 0 and best_ann < ANNUALIZED_THRESHOLD_PCT), "No fixed-capital cost200 breadth-repair scenario exceeded 12%."),
            ("no_robust_portfolio_evidence", f"robust_floor={robust_floor};robust_above12={robust_above12};best_events={best_events}", "hard_negative", int(robust_floor == 0 and robust_above12 == 0), "No robust portfolio event-floor evidence exists."),
            ("full_depth_boundary_preserved", f"l1_only={l1_only};live_label_leakage={leakage}", "constraint", int(l1_only == 0 and leakage == 0), "Full-depth and no-live-leakage boundaries held."),
            ("positive_clues_below_threshold", f"positive_full_depth_clues={positive_clues}", "research_clue", int(positive_clues > 0), "Positive-but-below-threshold rows may inform what not to repeat."),
            ("contrarian_reversal_route_exhausted", "phase290_spark_not_broadened_by_phase292", "decision", 1, "Do not keep searching minor threshold variants of the same contrarian repair route."),
            ("next_route_should_test_continuation", SELECTED_NEXT_ROUTE, "next_action", 1, "A strong pressure event may continue rather than reverse; test full-depth absorption/continuation next."),
        ],
        columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"],
    )


def build_decision_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    best_ann = safe_float(metric_value(summary, "phase292_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase292_best_scheduled_event_rows", 0))
    sparse_above12 = as_int(metric_value(summary, "phase292_sparse_above12_scenario_rows", 0))
    return pd.DataFrame(
        [
            ("close_phase292_breadth_repair_for_acceptance", 1, f"sparse_above12={sparse_above12};best_ann={best_ann};best_events={best_events}", "Do not accept, replay, or promote Phase292."),
            ("close_same_contrarian_breadth_repair_family", 1, "phase292_breadth_repair_failed", "Avoid another near-duplicate threshold relaxation pass."),
            ("preserve_best_phase292_failure_clue", top.get("phase292_variant_id", ""), f"family={top.get('repair_family', '')};side={top.get('side_mode', '')};bucket={top.get('market_bucket', '')}", "Keep only as negative evidence and implementation context."),
            ("do_not_relax_annualized_denominator", 1, "fixed_initial_capital_required", "Annualized return remains fixed-capital based."),
            ("do_not_lower_cost_or_event_floor", 1, f"cost200_required;event_floor={SPARSE_DIAGNOSTIC_EVENT_FLOOR};portfolio_floor={ROBUST_PORTFOLIO_EVENT_FLOOR}", "Do not manufacture profitability by weakening the denominator or floor."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "contrarian/reversal breadth repair failed", "Test full-depth pressure absorption/continuation as a materially different thesis."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def decision_value(decisions: pd.DataFrame, decision_id: str) -> str:
    rows = decisions.loc[decisions["decision_id"].astype(str).eq(decision_id), "decision_value"] if not decisions.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_next_route_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P294_INPUTS", "outputs/phase277/phase277_cost200_redesign_event_universe.csv;outputs/phase292/phase292_breadth_repair_scenario_results.csv;outputs/phase292/phase292_breadth_repair_variant_summary.csv", "Use the same full-depth event universe plus Phase292 failure evidence."),
            ("P294_SEARCH_TYPE", "full_depth_pressure_absorption_continuation_search", "Test continuation after pressure/absorption instead of contrarian reversal."),
            ("P294_REQUIRED_L2_FEATURES", "top5_imbalance;depth_withdrawal_pressure;visible_absorption_or_replenishment;spread_state;depth_beyond_l1_materiality", "Use Zerodha top-five market-by-price depth, not L1-only signals."),
            ("P294_SIGNAL_DIRECTION", "continuation_after_absorption;no_bar_return_reversal_alone;no_minor_phase292_threshold_repair", "Materially different from the failed contrarian route."),
            ("P294_CAPITAL_AND_COST", "fixed_initial_capital;cost200_required;Zerodha_intraday_equity_formula;max_concurrent_scheduler", "No unlimited capital or bps-only cost shortcut."),
            ("P294_DISCOVERY_GATE", f"annualized_pct_gt_{ANNUALIZED_THRESHOLD_PCT};scheduled_event_rows_ge_{SPARSE_DIAGNOSTIC_EVENT_FLOOR}", "Above-12 is discovery only unless event breadth is present."),
            ("P294_PORTFOLIO_GATE", f"scheduled_event_rows_ge_{ROBUST_PORTFOLIO_EVENT_FLOOR};multi_symbol_and_multi_date_breadth_required", "Portfolio claims require materially more breadth."),
            ("P294_BOUNDARY", "no_paper_live;no_strategy_replay;no_deployable_profitability_claim;l1_only_forbidden;net_edge_live_mask_forbidden", "Only a synthetic-only search route is opened."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_gate_evaluation(summary: pd.DataFrame, ranked: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase292_breadth_repair_search_complete", 0))
    next_action = str(metric_value(summary, "phase292_next_best_action", ""))
    hard_pass = as_int(metric_value(summary, "phase292_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(summary, "phase292_hard_gate_rows", 0))
    sparse_above12 = as_int(metric_value(summary, "phase292_sparse_above12_scenario_rows", 0))
    robust_above12 = as_int(metric_value(summary, "phase292_robust_portfolio_above12_scenario_rows", 0))
    l1_only = as_int(metric_value(summary, "phase292_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase292_net_edge_live_mask_rows", 0))
    replay = as_int(metric_value(summary, "phase292_strategy_replay_allowed", 0))
    paper = as_int(metric_value(summary, "phase292_paper_or_live_acceptance_allowed", 0))
    claim = as_int(metric_value(summary, "phase292_deployable_profitability_claim_allowed", 0))
    gates = [
        ("P293_PHASE292_SEARCH_COMPLETE", complete == 1, complete, "Phase292 search complete"),
        ("P293_PHASE292_NEXT_ACTION_PRESENT", "phase293" in next_action, next_action, "Phase292 routes to Phase293 interpretation"),
        ("P293_PHASE292_GATES_PASS", hard_rows > 0 and hard_pass == hard_rows, f"{hard_pass}/{hard_rows}", "Phase292 gates pass"),
        ("P293_RANKED_INTERPRETATION_PRESENT", len(ranked) > 0, len(ranked), ">0 ranked variants"),
        ("P293_CLOSES_PHASE292_FOR_ACCEPTANCE", str(decision_value(decisions, "close_phase292_breadth_repair_for_acceptance")) == "1", decision_value(decisions, "close_phase292_breadth_repair_for_acceptance"), "Phase292 closed for acceptance"),
        ("P293_NO_SURVIVOR_TO_PROMOTE", sparse_above12 == 0 and robust_above12 == 0, f"sparse_above12={sparse_above12};robust_above12={robust_above12}", "no Phase292 survivor"),
        ("P293_NEXT_ROUTE_SELECTED", str(decision_value(decisions, "selected_next_route")) == SELECTED_NEXT_ROUTE, decision_value(decisions, "selected_next_route"), SELECTED_NEXT_ROUTE),
        ("P293_FULL_DEPTH_BOUNDARY_PRESERVED", l1_only == 0 and leakage == 0, f"l1_only={l1_only};live_mask={leakage}", "full-depth, no leakage"),
        ("P293_BOUNDARIES_CLOSED", replay == 0 and paper == 0 and claim == 0, f"replay={replay};paper={paper};claim={claim}", "no replay/paper/live/claim"),
        ("P293_ROUTE_CONTRACT_PRESENT", len(route) >= 8, len(route), "Phase294 route contract rows"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def write_report(output_dir: Path, summary: pd.DataFrame, ranked: pd.DataFrame, families: pd.DataFrame, interpretation: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase293 Adaptive Pressure Breadth-Repair Interpretation",
        "",
        "Phase293 interprets Phase292 as a failed breadth repair of the Phase290 one-event adaptive-pressure spark.",
        "",
        "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened.",
        "",
        "The next route pivots to a materially different full-depth L2 thesis: pressure absorption / continuation rather than contrarian reversal.",
        "",
        "## Phase292 Summary",
        "",
        _markdown_table(summary),
        "",
        "## Ranked Breadth-Repair Interpretation",
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
        "## Phase294 Route Contract",
        "",
        _markdown_table(route),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase293_adaptive_pressure_breadth_repair_interpretation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(phase292_dir: Path = DEFAULT_PHASE292_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase292_dir / "phase292_acceptance_summary.csv")
    scenarios = read_csv(phase292_dir / "phase292_breadth_repair_scenario_results.csv")
    ranked = build_ranked_breadth_repair_interpretation(scenarios)
    families = build_family_interpretation(ranked)
    interpretation = build_interpretation_ledger(summary, ranked)
    decisions = build_decision_ledger(summary, ranked)
    route = build_next_route_contract()
    gates = build_gate_evaluation(summary, ranked, decisions, route)

    ranked.to_csv(output_dir / "phase293_ranked_breadth_repair_interpretation.csv", index=False)
    families.to_csv(output_dir / "phase293_breadth_repair_family_interpretation.csv", index=False)
    interpretation.to_csv(output_dir / "phase293_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase293_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase293_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase293_gate_evaluation.csv", index=False)

    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    best = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    acceptance = pd.DataFrame(
        [
            ("phase293_interpretation_complete", 1, "Phase293 interpretation completed"),
            ("phase293_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
            ("phase293_phase292_variant_rows", as_int(metric_value(summary, "phase292_variant_rows", 0)), "Phase292 variants interpreted"),
            ("phase293_phase292_scenario_rows", as_int(metric_value(summary, "phase292_scenario_rows", 0)), "Phase292 scenarios interpreted"),
            ("phase293_phase292_sparse_above12_scenario_rows", as_int(metric_value(summary, "phase292_sparse_above12_scenario_rows", 0)), "Phase292 sparse above-12 rows"),
            ("phase293_phase292_robust_portfolio_floor_scenario_rows", as_int(metric_value(summary, "phase292_robust_portfolio_floor_scenario_rows", 0)), "Phase292 robust floor rows"),
            ("phase293_phase292_robust_portfolio_above12_scenario_rows", as_int(metric_value(summary, "phase292_robust_portfolio_above12_scenario_rows", 0)), "Phase292 robust above-12 rows"),
            ("phase293_best_phase292_variant_id", best.get("phase292_variant_id", ""), "Best interpreted Phase292 variant"),
            ("phase293_best_repair_family", best.get("repair_family", ""), "Best interpreted repair family"),
            ("phase293_best_side_mode", best.get("side_mode", ""), "Best interpreted side mode"),
            ("phase293_best_market_bucket", best.get("market_bucket", ""), "Best interpreted market bucket"),
            ("phase293_best_cost200_annualized_pct", best.get("max_annualized_pct", ""), "Best fixed-capital annualized diagnostic"),
            ("phase293_best_scheduled_event_rows", best.get("max_scheduled_event_rows", ""), "Best scheduled events"),
            ("phase293_positive_but_below12_variant_rows", int(ranked["positive_but_below12"].astype(int).sum()) if not ranked.empty else 0, "Positive but below-12 variants"),
            ("phase293_close_phase292_for_acceptance", decision_value(decisions, "close_phase292_breadth_repair_for_acceptance"), "Close Phase292 route for acceptance"),
            ("phase293_close_same_contrarian_repair_family", decision_value(decisions, "close_same_contrarian_breadth_repair_family"), "Close same contrarian repair family"),
            ("phase293_do_not_relax_annualized_denominator", decision_value(decisions, "do_not_relax_annualized_denominator"), "Keep fixed-capital annualized denominator"),
            ("phase293_do_not_lower_cost_or_event_floor", decision_value(decisions, "do_not_lower_cost_or_event_floor"), "Keep cost/event floors"),
            ("phase293_strategy_replay_allowed", 0, "No strategy replay unlocked"),
            ("phase293_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
            ("phase293_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
            ("phase293_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase293_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase293_hard_gate_rows", hard_rows, "Hard gates evaluated"),
            ("phase293_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    acceptance.to_csv(output_dir / "phase293_acceptance_summary.csv", index=False)
    write_report(output_dir, summary, ranked, families, interpretation, decisions, route, gates)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = reproducibility_fields(
        artifact_id="phase293",
        generated_utc=generated_utc,
        inputs={
            "phase292_acceptance_summary": str(phase292_dir / "phase292_acceptance_summary.csv"),
            "phase292_scenario_results": str(phase292_dir / "phase292_breadth_repair_scenario_results.csv"),
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
            "acceptance_summary": str(output_dir / "phase293_acceptance_summary.csv"),
            "next_route_contract": str(output_dir / "phase293_next_route_contract.csv"),
            "gate_evaluation": str(output_dir / "phase293_gate_evaluation.csv"),
        },
        cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        latency_model_version="phase293_interpretation_no_new_latency_model",
    )
    manifest.update(
        {
            "generated_utc": generated_utc,
            "phase292_dir": str(phase292_dir),
            "output_dir": str(output_dir),
            "selected_next_route": SELECTED_NEXT_ROUTE,
            "next_action": NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION,
            "hard_gate_pass_rows": hard_pass,
            "hard_gate_rows": hard_rows,
        }
    )
    (output_dir / "phase293_adaptive_pressure_breadth_repair_interpretation_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase292-dir", type=Path, default=DEFAULT_PHASE292_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    print(json.dumps(run(args.phase292_dir, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

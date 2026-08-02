from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, metric_value, read_csv
from synthetic_l2.phase255_richer_raw_depth_feature_quality_interpretation import safe_float
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE271_DIR = Path("outputs/phase271")
DEFAULT_OUTPUT_DIR = Path("outputs/phase272")

SELECTED_NEXT_ROUTE = "P272_FOCUSED_CAPITAL_AWARE_CANDIDATE_FOLLOWTHROUGH_SEARCH"
NEXT_ACTION = "run_phase273_focused_capital_aware_candidate_followthrough_search_no_paper_live"
REPAIR_ACTION = "repair_phase272_fixed_capital_capacity_return_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_DATES_FOR_PORTFOLIO_CLAIM = 5


def metric_value_from_frame(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return default if rows.empty else rows.iloc[0]


def build_ranked_capital_leads(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    frame = scenarios.copy()
    numeric = [
        "mechanical_one_date_annualized_portfolio_return_pct",
        "portfolio_return_pct",
        "realized_net_pnl_inr",
        "scheduled_event_rows",
        "rejected_event_rows",
        "notional_turnover_x_initial_capital",
        "max_drawdown_inr",
        "initial_capital_inr",
        "fixed_notional_inr",
        "max_concurrent_positions",
        "annualized_above_12pct_research_diagnostic",
        "portfolio_claim_allowed",
    ]
    for col in numeric:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    frame["scope_candidate_id"] = frame["scope_candidate_id"].astype(str)
    frame["cost_profile"] = frame["cost_profile"].astype(str)
    candidate_frame = frame[~frame["scope_candidate_id"].eq("ALL_RANKED_LEADS")].copy()
    rows: list[dict[str, Any]] = []
    for candidate_id, group in candidate_frame.groupby("scope_candidate_id", dropna=False):
        best = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
        cost100_positive = int(group[group["cost_profile"].eq("cost100")]["annualized_above_12pct_research_diagnostic"].sum())
        cost150_positive = int(group[group["cost_profile"].eq("cost150")]["annualized_above_12pct_research_diagnostic"].sum())
        cost200_positive = int(group[group["cost_profile"].eq("cost200")]["annualized_above_12pct_research_diagnostic"].sum())
        plus_1bp_positive = int(group[group["cost_profile"].eq("cost100_plus_1bp")]["annualized_above_12pct_research_diagnostic"].sum())
        plus_2bp_positive = int(group[group["cost_profile"].eq("cost100_plus_2bp")]["annualized_above_12pct_research_diagnostic"].sum())
        robust_cost_profile_count = int(sum(positive > 0 for positive in [cost100_positive, cost150_positive, cost200_positive, plus_1bp_positive, plus_2bp_positive]))
        rows.append(
            {
                "scope_candidate_id": candidate_id,
                "best_scenario_id": best["scenario_id"],
                "best_scope_id": best["scope_id"],
                "best_cost_profile": best["cost_profile"],
                "best_initial_capital_inr": best["initial_capital_inr"],
                "best_fixed_notional_inr": best["fixed_notional_inr"],
                "best_max_concurrent_positions": best["max_concurrent_positions"],
                "best_scheduled_event_rows": int(best["scheduled_event_rows"]),
                "best_rejected_event_rows": int(best["rejected_event_rows"]),
                "best_realized_net_pnl_inr": best["realized_net_pnl_inr"],
                "best_portfolio_return_pct": best["portfolio_return_pct"],
                "best_mechanical_one_date_annualized_portfolio_return_pct": best["mechanical_one_date_annualized_portfolio_return_pct"],
                "best_notional_turnover_x_initial_capital": best["notional_turnover_x_initial_capital"],
                "best_max_drawdown_inr": best["max_drawdown_inr"],
                "cost100_above12_scenario_rows": cost100_positive,
                "cost150_above12_scenario_rows": cost150_positive,
                "cost200_above12_scenario_rows": cost200_positive,
                "cost100_plus_1bp_above12_scenario_rows": plus_1bp_positive,
                "cost100_plus_2bp_above12_scenario_rows": plus_2bp_positive,
                "robust_cost_profile_count": robust_cost_profile_count,
                "followthrough_priority": int(cost200_positive > 0 and robust_cost_profile_count >= 3),
                "portfolio_claim_allowed": int(group["portfolio_claim_allowed"].max()),
            }
        )
    ranked = pd.DataFrame(rows)
    if ranked.empty:
        return ranked
    return ranked.sort_values(
        [
            "followthrough_priority",
            "cost200_above12_scenario_rows",
            "robust_cost_profile_count",
            "best_mechanical_one_date_annualized_portfolio_return_pct",
            "best_realized_net_pnl_inr",
        ],
        ascending=[False, False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_scope_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    frame = scenarios.copy()
    for col in ["mechanical_one_date_annualized_portfolio_return_pct", "realized_net_pnl_inr", "scheduled_event_rows", "annualized_above_12pct_research_diagnostic"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    grouped = (
        frame.groupby(["scope_id", "scope_candidate_id"], dropna=False)
        .agg(
            scenario_rows=("scenario_id", "nunique"),
            cost_profile_rows=("cost_profile", "nunique"),
            above12_scenario_rows=("annualized_above_12pct_research_diagnostic", "sum"),
            best_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "max"),
            best_realized_net_pnl_inr=("realized_net_pnl_inr", "max"),
            max_scheduled_event_rows=("scheduled_event_rows", "max"),
        )
        .reset_index()
    )
    return grouped.sort_values(["above12_scenario_rows", "best_annualized_pct"], ascending=[False, False]).reset_index(drop=True)


def build_interpretation_ledger(summary: pd.DataFrame, scenarios: pd.DataFrame, ranked: pd.DataFrame, scope_summary: pd.DataFrame) -> pd.DataFrame:
    observed_dates = as_int(metric_value_from_frame(summary, "phase271_observed_trade_dates", 0))
    scenario_rows = as_int(metric_value_from_frame(summary, "phase271_scenario_rows", 0))
    cost100_above = as_int(metric_value_from_frame(summary, "phase271_cost100_annualized_above_12pct_scenario_rows", 0))
    cost200_above = as_int(metric_value_from_frame(summary, "phase271_cost200_annualized_above_12pct_scenario_rows", 0))
    portfolio_claim = as_int(metric_value_from_frame(summary, "phase271_portfolio_claim_allowed", 1))
    deployable_claim = as_int(metric_value_from_frame(summary, "phase271_deployable_profitability_claim_allowed", 1))
    pooled = scope_summary[scope_summary["scope_candidate_id"].astype(str).eq("ALL_RANKED_LEADS")] if not scope_summary.empty else pd.DataFrame()
    pooled_above = int(pooled["above12_scenario_rows"].iloc[0]) if not pooled.empty else 0
    followthrough = int(ranked["followthrough_priority"].sum()) if not ranked.empty else 0
    best_candidate = str(ranked["scope_candidate_id"].iloc[0]) if not ranked.empty else ""
    best_ann = safe_float(ranked["best_mechanical_one_date_annualized_portfolio_return_pct"].iloc[0], 0.0) if not ranked.empty else 0.0
    rows = [
        ("fixed_capital_scheduler_materialized", f"scenario_rows={scenario_rows};observed_dates={observed_dates}", "positive_mechanics", int(scenario_rows > 0), "Capital-aware denominator and scheduler are now materialized."),
        ("per_candidate_profitable_pockets_found", f"cost100_above12={cost100_above};cost200_above12={cost200_above};best_candidate={best_candidate};best_ann={best_ann}", "research_positive", int(cost100_above > 0), "Small one-date capital-aware pockets exist and should be chased with focused follow-through."),
        ("pooled_allocator_not_yet_working", f"pooled_above12_scenarios={pooled_above}", "important_context", int(pooled_above == 0), "Pooling all ranked leads diluted the edge; follow-through should isolate candidates first."),
        ("cost200_survival_is_sparse_but_nonzero", f"cost200_above12={cost200_above};followthrough_priority_candidates={followthrough}", "research_positive", int(cost200_above > 0), "Some pockets survive 2x modeled Zerodha costs on the one-date diagnostic."),
        ("one_date_only_blocks_portfolio_claim", f"observed_dates={observed_dates};min_required={MIN_DATES_FOR_PORTFOLIO_CLAIM};portfolio_claim_allowed={portfolio_claim}", "hard_boundary", int(observed_dates < MIN_DATES_FOR_PORTFOLIO_CLAIM and portfolio_claim == 0), "Do not call the annualized diagnostic a robust annual portfolio return."),
        ("deployable_profitability_claim_closed", f"deployable_profitability_claim_allowed={deployable_claim}", "hard_boundary", int(deployable_claim == 0), "No paper/live or deployable profitability claim is opened by this result."),
        ("focused_followthrough_required", f"priority_candidates={followthrough}", "next_action", int(followthrough > 0), "Next step should test focused candidate subsets and parameter neighborhoods, not broad pooled averaging."),
    ]
    return pd.DataFrame(rows, columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"])


def build_decision_ledger(ranked: pd.DataFrame, summary: pd.DataFrame) -> pd.DataFrame:
    priority_rows = int(ranked["followthrough_priority"].sum()) if not ranked.empty else 0
    best_candidate = str(ranked["scope_candidate_id"].iloc[0]) if not ranked.empty else ""
    observed_dates = as_int(metric_value_from_frame(summary, "phase271_observed_trade_dates", 0))
    return pd.DataFrame(
        [
            ("preserve_phase271_capital_aware_pockets", int(priority_rows > 0), f"priority_candidates={priority_rows};best_candidate={best_candidate}", "Keep the profitable diagnostic pockets for immediate focused strategy follow-through."),
            ("do_not_claim_robust_annual_portfolio_return", 1, f"observed_dates={observed_dates};min_required={MIN_DATES_FOR_PORTFOLIO_CLAIM}", "One-date annualization is a diagnostic only."),
            ("do_not_promote_or_paper_live", 1, "acceptance_grade_scenario_rows=0", "No replay promotion, paper/live, or deployable claim is allowed."),
            ("avoid_broad_pooled_allocator_for_next_step", 1, "ALL_RANKED_LEADS produced no above-12 diagnostic scenarios", "Do not average away small candidate-specific edges."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "focused candidate follow-through search", "Test the specific profitable pockets and near-neighbor parameterizations next."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def build_next_route_contract(ranked: pd.DataFrame) -> pd.DataFrame:
    top_candidates = ";".join(ranked.head(5)["scope_candidate_id"].astype(str).tolist()) if not ranked.empty else ""
    rows = [
        ("P273_INPUT", "outputs/phase271/phase271_capital_scenario_results.csv;outputs/phase271/phase271_scheduled_event_ledger.csv", "Use capital-aware scenario and event evidence from Phase271."),
        ("P273_CANDIDATE_SCOPE", top_candidates, "Focus on top per-candidate pockets rather than the all-ranked pooled allocator."),
        ("P273_SEARCH_TYPE", "focused_capital_aware_candidate_followthrough_search", "Evaluate top-candidate subsets, cost profiles, notional/concurrency neighborhoods and event-order sensitivity."),
        ("P273_DEPTH_REQUIREMENT", "full_top_five_rows_1_to_5_and_levels_2_to_5_required", "Preserve the full-depth Zerodha L2 objective."),
        ("P273_ACCEPTANCE_BOUNDARY", "one_date_diagnostic_only;no_paper_live;no_deployable_profitability_claim", "Do not relabel diagnostics as robust portfolio results."),
        ("P273_OUTPUT", "focused_candidate_followthrough_results_and_interpretation", "Produce a concrete next search, not just a plan."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def decision_value(frame: pd.DataFrame, decision_id: str) -> str:
    rows = frame.loc[frame["decision_id"].astype(str).eq(decision_id), "decision_value"] if not frame.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_gate_evaluation(summary: pd.DataFrame, scenarios: pd.DataFrame, ranked: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    phase271_complete = as_int(metric_value_from_frame(summary, "phase271_fixed_capital_analysis_complete", 0))
    phase271_next = str(metric_value_from_frame(summary, "phase271_next_best_action", ""))
    observed_dates = as_int(metric_value_from_frame(summary, "phase271_observed_trade_dates", 0))
    hard_pass = as_int(metric_value_from_frame(summary, "phase271_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value_from_frame(summary, "phase271_hard_gate_rows", 0))
    full_depth = as_int(metric_value_from_frame(summary, "phase271_full_top_five_depth_required", 0))
    l2_l5 = as_int(metric_value_from_frame(summary, "phase271_levels_2_to_5_materiality_required", 0))
    l1_only = as_int(metric_value_from_frame(summary, "phase271_l1_only_candidate_allowed", 1))
    portfolio_claim = as_int(metric_value_from_frame(summary, "phase271_portfolio_claim_allowed", 1))
    deployable_claim = as_int(metric_value_from_frame(summary, "phase271_deployable_profitability_claim_allowed", 1))
    priority_rows = int(ranked["followthrough_priority"].sum()) if not ranked.empty else 0
    rows = [
        ("P272_PHASE271_WORK_ORDER_PRESENT", "run_phase272_fixed_capital_capacity_return_interpretation" in phase271_next, phase271_next, "Phase271 next action targets Phase272", "hard"),
        ("P272_PHASE271_ANALYSIS_COMPLETE", phase271_complete == 1, phase271_complete, "Phase271 complete", "hard"),
        ("P272_PHASE271_HARD_GATES_PASS", hard_pass == hard_rows and hard_rows > 0, f"{hard_pass}/{hard_rows}", "Phase271 hard gates pass", "hard"),
        ("P272_SCENARIOS_PRESENT", len(scenarios) > 0, len(scenarios), ">0 Phase271 scenarios", "hard"),
        ("P272_PRIORITY_POCKETS_FOUND", priority_rows > 0, priority_rows, ">0 follow-through priority candidates", "hard"),
        ("P272_FULL_DEPTH_PRESERVED", full_depth == 1 and l2_l5 == 1 and l1_only == 0, f"full={full_depth};l2_l5={l2_l5};l1_only={l1_only}", "full-depth and no L1-only", "hard"),
        ("P272_ONE_DATE_BOUNDARY_RECOGNIZED", observed_dates < MIN_DATES_FOR_PORTFOLIO_CLAIM and portfolio_claim == 0, f"dates={observed_dates};portfolio_claim={portfolio_claim}", "one-date diagnostic only", "hard"),
        ("P272_NO_PROMOTION_OR_DEPLOYABLE_CLAIM", deployable_claim == 0, deployable_claim, "deployable claim closed", "hard"),
        ("P272_NEXT_ROUTE_SELECTED", decision_value(decisions, "selected_next_route") == SELECTED_NEXT_ROUTE and int(route["contract_id"].astype(str).eq("P273_SEARCH_TYPE").sum()) == 1, SELECTED_NEXT_ROUTE, "Phase273 focused follow-through selected", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(summary: pd.DataFrame, ranked: pd.DataFrame, scope_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    best = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    priority_rows = int(ranked["followthrough_priority"].sum()) if not ranked.empty else 0
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase272_interpretation_complete", 1, "Phase272 fixed-capital capacity-return interpretation completed"),
        ("phase272_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
        ("phase272_phase271_scenario_rows", as_int(metric_value_from_frame(summary, "phase271_scenario_rows", 0)), "Phase271 scenario rows interpreted"),
        ("phase272_phase271_scope_rows", as_int(metric_value_from_frame(summary, "phase271_scope_rows", 0)), "Phase271 scheduling scopes interpreted"),
        ("phase272_phase271_observed_trade_dates", as_int(metric_value_from_frame(summary, "phase271_observed_trade_dates", 0)), "Observed dates remain one-date diagnostic"),
        ("phase272_ranked_capital_candidate_rows", len(ranked), "Per-candidate capital-aware rows ranked"),
        ("phase272_followthrough_priority_candidate_rows", priority_rows, "Candidates with 2x and multi-profile one-date diagnostic support"),
        ("phase272_pooled_above12_scenario_rows", int(scope_summary[scope_summary["scope_candidate_id"].astype(str).eq("ALL_RANKED_LEADS")]["above12_scenario_rows"].iloc[0]) if not scope_summary.empty and not scope_summary[scope_summary["scope_candidate_id"].astype(str).eq("ALL_RANKED_LEADS")].empty else 0, "Pooled all-ranked lead above-12 diagnostic rows"),
        ("phase272_best_candidate_id", best.get("scope_candidate_id", ""), "Best follow-through candidate"),
        ("phase272_best_scenario_id", best.get("best_scenario_id", ""), "Best scenario for best candidate"),
        ("phase272_best_cost_profile", best.get("best_cost_profile", ""), "Best cost profile"),
        ("phase272_best_realized_net_pnl_inr", best.get("best_realized_net_pnl_inr", ""), "Best realized net P&L"),
        ("phase272_best_mechanical_one_date_annualized_portfolio_return_pct", best.get("best_mechanical_one_date_annualized_portfolio_return_pct", ""), "Best one-date annualized diagnostic"),
        ("phase272_best_cost200_above12_scenario_rows", best.get("cost200_above12_scenario_rows", ""), "Best candidate 2x-cost above-12 rows"),
        ("phase272_portfolio_claim_allowed", 0, "Robust portfolio claim remains closed"),
        ("phase272_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase272_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase272_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase272_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase272_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase272_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase272_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase272 Fixed-capital Capacity-return Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase272 interprets Phase271's fixed-capital scheduled diagnostics.",
        "The key finding is candidate-specific profitable one-date pockets, while the pooled all-ranked allocator is not yet profitable.",
        "The next step is focused candidate follow-through, not replay promotion or paper/live acceptance.",
        "Annualized values remain one-date mechanical diagnostics until enough dates exist for a robust portfolio claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase271_dir: Path = DEFAULT_PHASE271_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase271_dir / "phase271_acceptance_summary.csv")
    scenarios = read_csv(phase271_dir / "phase271_capital_scenario_results.csv")
    if summary.empty:
        raise FileNotFoundError("Missing Phase271 acceptance summary.")
    if scenarios.empty:
        raise FileNotFoundError("Missing Phase271 capital scenario results.")
    ranked = build_ranked_capital_leads(scenarios)
    scope_summary = build_scope_summary(scenarios)
    interpretations = build_interpretation_ledger(summary, scenarios, ranked, scope_summary)
    decisions = build_decision_ledger(ranked, summary)
    route = build_next_route_contract(ranked)
    gates = build_gate_evaluation(summary, scenarios, ranked, decisions, route)
    acceptance = build_acceptance_summary(summary, ranked, scope_summary, gates)

    ranked.to_csv(output_dir / "phase272_ranked_capital_aware_research_pockets.csv", index=False)
    scope_summary.to_csv(output_dir / "phase272_scope_summary.csv", index=False)
    interpretations.to_csv(output_dir / "phase272_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase272_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase272_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase272_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase272_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase272_fixed_capital_capacity_return_interpretation_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Ranked Capital-aware Research Pockets": ranked.head(20),
            "Scope Summary": scope_summary,
            "Interpretation Ledger": interpretations,
            "Decision Ledger": decisions,
            "Next Route Contract": route,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase272_fixed_capital_capacity_return_interpretation",
        **reproducibility_fields(
            artifact_id="phase272",
            generated_utc=generated_utc,
            inputs={
                "phase271_acceptance_summary": str(phase271_dir / "phase271_acceptance_summary.csv"),
                "phase271_capital_scenario_results": str(phase271_dir / "phase271_capital_scenario_results.csv"),
            },
            parameters={
                "selected_next_route": SELECTED_NEXT_ROUTE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "min_dates_for_portfolio_claim": MIN_DATES_FOR_PORTFOLIO_CLAIM,
                "full_top_five_depth_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "l1_only_candidate_allowed": 0,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "ranked_capital_aware_research_pockets": str(output_dir / "phase272_ranked_capital_aware_research_pockets.csv"),
                "scope_summary": str(output_dir / "phase272_scope_summary.csv"),
                "interpretation_ledger": str(output_dir / "phase272_interpretation_ledger.csv"),
                "decision_ledger": str(output_dir / "phase272_decision_ledger.csv"),
                "next_route_contract": str(output_dir / "phase272_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase272_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase272_acceptance_summary.csv"),
                "report": str(output_dir / "phase272_fixed_capital_capacity_return_interpretation_report.md"),
                "manifest": str(output_dir / "phase272_fixed_capital_capacity_return_interpretation_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase272_interpretation_only_no_new_replay",
        ),
    }
    (output_dir / "phase272_fixed_capital_capacity_return_interpretation_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase272 fixed-capital capacity-return interpretation.")
    parser.add_argument("--phase271-dir", type=Path, default=DEFAULT_PHASE271_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase271_dir=args.phase271_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

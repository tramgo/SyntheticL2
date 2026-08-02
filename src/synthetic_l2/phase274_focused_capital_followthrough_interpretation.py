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
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE273_DIR = Path("outputs/phase273")
DEFAULT_OUTPUT_DIR = Path("outputs/phase274")

SELECTED_NEXT_ROUTE = "P274_FOCUSED_CAPITAL_MULTIDAY_SYNTHETIC_FOLLOWTHROUGH_SEARCH"
NEXT_ACTION = "run_phase275_focused_capital_multiday_synthetic_followthrough_search_no_paper_live"
REPAIR_ACTION = "repair_phase274_focused_capital_followthrough_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_DATES_FOR_PORTFOLIO_CLAIM = 5


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return default if rows.empty else rows.iloc[0]


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    return out


def build_ranked_followthrough(results: pd.DataFrame, stability: pd.DataFrame) -> pd.DataFrame:
    if results.empty:
        return pd.DataFrame()
    frame = numeric(
        results,
        [
            "mechanical_one_date_annualized_portfolio_return_pct",
            "realized_net_pnl_inr",
            "scheduled_event_rows",
            "notional_turnover_x_initial_capital",
            "max_drawdown_inr",
            "annualized_above_12pct_research_diagnostic",
        ],
    )
    rows: list[dict[str, Any]] = []
    for keys, group in frame.groupby(["phase273_scope_id", "phase273_scope_candidate_id", "cost_profile"], dropna=False):
        scope_id, candidate_id, cost_profile = keys
        best = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
        stability_rows = stability[
            stability["phase273_scope_id"].astype(str).eq(str(scope_id))
            & stability["phase273_scope_candidate_id"].astype(str).eq(str(candidate_id))
            & stability["cost_profile"].astype(str).eq(str(cost_profile))
        ]
        stable = stability_rows.iloc[0] if not stability_rows.empty else pd.Series(dtype=object)
        above12 = int(group["annualized_above_12pct_research_diagnostic"].sum())
        scenario_rows = int(len(group))
        median_ann = safe_float(stable.get("median_annualized_pct", group["mechanical_one_date_annualized_portfolio_return_pct"].median()), 0.0)
        min_ann = safe_float(stable.get("min_annualized_pct", group["mechanical_one_date_annualized_portfolio_return_pct"].min()), 0.0)
        rows.append(
            {
                "phase273_scope_id": scope_id,
                "phase273_scope_candidate_id": candidate_id,
                "cost_profile": cost_profile,
                "scenario_rows": scenario_rows,
                "above12_scenario_rows": above12,
                "above12_fraction": above12 / scenario_rows if scenario_rows else 0.0,
                "median_annualized_pct": median_ann,
                "min_annualized_pct": min_ann,
                "max_annualized_pct": safe_float(stable.get("max_annualized_pct", group["mechanical_one_date_annualized_portfolio_return_pct"].max()), 0.0),
                "max_realized_net_pnl_inr": safe_float(stable.get("max_realized_net_pnl_inr", group["realized_net_pnl_inr"].max()), 0.0),
                "best_scenario_id": best["scenario_id"],
                "best_order_policy": best["order_policy"],
                "best_initial_capital_inr": best["initial_capital_inr"],
                "best_fixed_notional_inr": best["fixed_notional_inr"],
                "best_max_concurrent_positions": best["max_concurrent_positions"],
                "best_scheduled_event_rows": int(best["scheduled_event_rows"]),
                "best_notional_turnover_x_initial_capital": best["notional_turnover_x_initial_capital"],
                "worst_drawdown_inr": safe_float(stable.get("worst_drawdown_inr", group["max_drawdown_inr"].min()), 0.0),
                "followthrough_preserve": int(above12 > 0 and str(cost_profile) in {"cost100", "cost100_plus_1bp", "cost100_plus_2bp", "cost150", "cost200"}),
                "cost200_survivor": int(str(cost_profile) == "cost200" and above12 > 0),
                "median_positive": int(median_ann > ANNUALIZED_THRESHOLD_PCT),
                "worst_case_positive": int(min_ann > ANNUALIZED_THRESHOLD_PCT),
            }
        )
    ranked = pd.DataFrame(rows)
    return ranked.sort_values(
        ["cost200_survivor", "median_positive", "above12_fraction", "max_annualized_pct", "above12_scenario_rows"],
        ascending=[False, False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_interpretation_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    cost100_above = as_int(metric_value(summary, "phase273_cost100_above12_scenario_rows", 0))
    cost200_above = as_int(metric_value(summary, "phase273_cost200_above12_scenario_rows", 0))
    scenario_rows = as_int(metric_value(summary, "phase273_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase273_best_mechanical_one_date_annualized_portfolio_return_pct", 0.0), 0.0)
    cost200_rows = ranked[ranked["cost200_survivor"].astype(int).eq(1)] if not ranked.empty else pd.DataFrame()
    median_positive_rows = int(ranked["median_positive"].astype(int).sum()) if not ranked.empty else 0
    worst_positive_rows = int(ranked["worst_case_positive"].astype(int).sum()) if not ranked.empty else 0
    rows = [
        ("focused_followthrough_strengthened_signal", f"cost100_above12={cost100_above};cost200_above12={cost200_above};best_ann={best_ann}", "research_positive", int(cost100_above > 0 and cost200_above > 0), "Phase273 strengthened the candidate-specific one-date diagnostic."),
        ("top2_subset_is_best_scope", str(metric_value(summary, "phase273_best_scope_id", "")), "research_positive", int(str(metric_value(summary, "phase273_best_scope_id", "")) == "TOP2_PRIORITY_SUBSET"), "The two priority candidates combine better than either broad pooling or single-candidate-only best case."),
        ("order_policy_fragility_remains", f"median_positive_rows={median_positive_rows};worst_case_positive_rows={worst_positive_rows}", "risk", int(worst_positive_rows == 0), "Some order policies and scenario settings remain negative, so this is not ready for promotion."),
        ("cost200_survivor_profiles_exist", f"cost200_scope_profile_rows={len(cost200_rows)}", "research_positive", int(len(cost200_rows) > 0), "2x-cost diagnostic survival exists but remains one-date evidence."),
        ("one_date_blocks_portfolio_claim", "observed_trade_dates=1;required>=5", "hard_boundary", 1, "Annualized values remain one-date mechanical diagnostics."),
        ("next_step_must_execute_multiday_synthetic_followthrough", f"scenario_rows={scenario_rows}", "next_action", 1, "Move from one-date diagnostic to synthetic-only multi-date follow-through search."),
    ]
    return pd.DataFrame(rows, columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"])


def build_decision_ledger(ranked: pd.DataFrame) -> pd.DataFrame:
    preserved = ranked[ranked["followthrough_preserve"].astype(int).eq(1)] if not ranked.empty else pd.DataFrame()
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            ("preserve_phase273_followthrough_pockets", int(len(preserved) > 0), f"preserved_scope_profile_rows={len(preserved)};top_scope={top.get('phase273_scope_id', '')}", "Keep Phase273 pockets for multi-date synthetic follow-through."),
            ("do_not_promote_or_claim_portfolio_return", 1, "one_date_diagnostic_only", "No replay, paper/live, or deployable annual return claim."),
            ("do_not_continue_broad_pooled_allocator", 1, "Phase272 pooled_above12=0", "Continue focused top-two/candidate route instead of all-ranked pooling."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "execute synthetic-only multi-date follow-through search", "Next step should execute a broader synthetic follow-through search."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def build_next_route_contract(ranked: pd.DataFrame) -> pd.DataFrame:
    top_rows = ranked.head(5)
    top_scope_profiles = ";".join((top_rows["phase273_scope_id"].astype(str) + ":" + top_rows["cost_profile"].astype(str)).tolist()) if not top_rows.empty else ""
    return pd.DataFrame(
        [
            ("P275_INPUT", "outputs/phase273/phase273_followthrough_scenario_results.csv;outputs/phase273/phase273_order_policy_stability_summary.csv", "Use Phase273 focused follow-through evidence."),
            ("P275_SCOPE_PROFILES", top_scope_profiles, "Focus on strongest top-two and priority scope/cost profiles."),
            ("P275_SEARCH_TYPE", "focused_capital_multiday_synthetic_followthrough_search", "Execute synthetic-only multi-date or multi-seed follow-through, not a precommit-only step."),
            ("P275_DEPTH_REQUIREMENT", "full_top_five_rows_1_to_5_and_levels_2_to_5_required", "Keep full-depth L2 requirement."),
            ("P275_BOUNDARY", "no_paper_live;no_deployable_profitability_claim_until_multiday_acceptance", "No claim until multi-date gates pass."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def decision_value(decisions: pd.DataFrame, decision_id: str) -> str:
    rows = decisions.loc[decisions["decision_id"].astype(str).eq(decision_id), "decision_value"] if not decisions.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_gate_evaluation(summary: pd.DataFrame, results: pd.DataFrame, ranked: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    phase273_complete = as_int(metric_value(summary, "phase273_followthrough_search_complete", 0))
    phase273_next = str(metric_value(summary, "phase273_next_best_action", ""))
    hard_pass = as_int(metric_value(summary, "phase273_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(summary, "phase273_hard_gate_rows", 0))
    cost200_above = as_int(metric_value(summary, "phase273_cost200_above12_scenario_rows", 0))
    replay_allowed = as_int(metric_value(summary, "phase273_strategy_replay_allowed", 1))
    paper_allowed = as_int(metric_value(summary, "phase273_paper_or_live_acceptance_allowed", 1))
    claim_allowed = as_int(metric_value(summary, "phase273_deployable_profitability_claim_allowed", 1))
    rows = [
        ("P274_PHASE273_WORK_ORDER_PRESENT", "run_phase274_focused_capital_followthrough_interpretation" in phase273_next, phase273_next, "Phase273 next action targets Phase274", "hard"),
        ("P274_PHASE273_SEARCH_COMPLETE", phase273_complete == 1, phase273_complete, "Phase273 complete", "hard"),
        ("P274_PHASE273_HARD_GATES_PASS", hard_pass == hard_rows and hard_rows > 0, f"{hard_pass}/{hard_rows}", "Phase273 hard gates pass", "hard"),
        ("P274_RESULTS_PRESENT", len(results) > 0 and len(ranked) > 0, f"results={len(results)};ranked={len(ranked)}", "Phase273 results ranked", "hard"),
        ("P274_COST200_SURVIVAL_RECOGNIZED", cost200_above > 0 and int(ranked["cost200_survivor"].astype(int).sum()) > 0, cost200_above, ">0 cost200 diagnostic survivors", "hard"),
        ("P274_BOUNDARIES_CLOSED", replay_allowed == 0 and paper_allowed == 0 and claim_allowed == 0, f"replay={replay_allowed};paper={paper_allowed};claim={claim_allowed}", "no replay/paper/live/claim", "hard"),
        ("P274_NEXT_ROUTE_SELECTED", decision_value(decisions, "selected_next_route") == SELECTED_NEXT_ROUTE and int(route["contract_id"].astype(str).eq("P275_SEARCH_TYPE").sum()) == 1, SELECTED_NEXT_ROUTE, "Phase275 multi-date follow-through selected", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(summary: pd.DataFrame, ranked: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase274_interpretation_complete", 1, "Phase274 focused capital follow-through interpretation completed"),
        ("phase274_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
        ("phase274_phase273_scenario_rows", as_int(metric_value(summary, "phase273_scenario_rows", 0)), "Phase273 scenarios interpreted"),
        ("phase274_phase273_cost100_above12_scenario_rows", as_int(metric_value(summary, "phase273_cost100_above12_scenario_rows", 0)), "Phase273 cost100 above-12 rows"),
        ("phase274_phase273_cost200_above12_scenario_rows", as_int(metric_value(summary, "phase273_cost200_above12_scenario_rows", 0)), "Phase273 cost200 above-12 rows"),
        ("phase274_ranked_scope_profile_rows", len(ranked), "Ranked scope/profile rows"),
        ("phase274_cost200_survivor_scope_profile_rows", int(ranked["cost200_survivor"].astype(int).sum()) if not ranked.empty else 0, "Scope/profile rows with 2x-cost above-12 diagnostics"),
        ("phase274_median_positive_scope_profile_rows", int(ranked["median_positive"].astype(int).sum()) if not ranked.empty else 0, "Scope/profile rows with median above 12%"),
        ("phase274_worst_case_positive_scope_profile_rows", int(ranked["worst_case_positive"].astype(int).sum()) if not ranked.empty else 0, "Scope/profile rows with worst case above 12%"),
        ("phase274_best_scope_profile", f"{top.get('phase273_scope_id', '')}:{top.get('cost_profile', '')}", "Best ranked scope/profile"),
        ("phase274_best_scenario_id", top.get("best_scenario_id", ""), "Best scenario ID"),
        ("phase274_best_order_policy", top.get("best_order_policy", ""), "Best order policy"),
        ("phase274_best_max_annualized_pct", top.get("max_annualized_pct", ""), "Best max one-date annualized diagnostic"),
        ("phase274_best_median_annualized_pct", top.get("median_annualized_pct", ""), "Best median one-date annualized diagnostic"),
        ("phase274_portfolio_claim_allowed", 0, "Robust portfolio claim remains closed"),
        ("phase274_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase274_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase274_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase274_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase274_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase274_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase274_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase274 Focused Capital Follow-through Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase274 interprets the Phase273 focused follow-through search.",
        "The result is strong enough to continue into synthetic-only multi-date follow-through, but not strong enough for replay promotion or portfolio-return claims.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase273_dir: Path = DEFAULT_PHASE273_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase273_dir / "phase273_acceptance_summary.csv")
    results = read_csv(phase273_dir / "phase273_followthrough_scenario_results.csv")
    stability = read_csv(phase273_dir / "phase273_order_policy_stability_summary.csv")
    if summary.empty:
        raise FileNotFoundError("Missing Phase273 acceptance summary.")
    if results.empty:
        raise FileNotFoundError("Missing Phase273 follow-through scenario results.")
    ranked = build_ranked_followthrough(results, stability)
    interpretations = build_interpretation_ledger(summary, ranked)
    decisions = build_decision_ledger(ranked)
    route = build_next_route_contract(ranked)
    gates = build_gate_evaluation(summary, results, ranked, decisions, route)
    acceptance = build_acceptance_summary(summary, ranked, gates)

    ranked.to_csv(output_dir / "phase274_ranked_followthrough_scope_profiles.csv", index=False)
    interpretations.to_csv(output_dir / "phase274_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase274_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase274_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase274_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase274_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase274_focused_capital_followthrough_interpretation_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Ranked Follow-through Scope Profiles": ranked.head(20),
            "Interpretation Ledger": interpretations,
            "Decision Ledger": decisions,
            "Next Route Contract": route,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase274_focused_capital_followthrough_interpretation",
        **reproducibility_fields(
            artifact_id="phase274",
            generated_utc=generated_utc,
            inputs={
                "phase273_acceptance_summary": str(phase273_dir / "phase273_acceptance_summary.csv"),
                "phase273_followthrough_scenario_results": str(phase273_dir / "phase273_followthrough_scenario_results.csv"),
                "phase273_order_policy_stability_summary": str(phase273_dir / "phase273_order_policy_stability_summary.csv"),
            },
            parameters={
                "selected_next_route": SELECTED_NEXT_ROUTE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "min_dates_for_portfolio_claim": MIN_DATES_FOR_PORTFOLIO_CLAIM,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "ranked_followthrough_scope_profiles": str(output_dir / "phase274_ranked_followthrough_scope_profiles.csv"),
                "interpretation_ledger": str(output_dir / "phase274_interpretation_ledger.csv"),
                "decision_ledger": str(output_dir / "phase274_decision_ledger.csv"),
                "next_route_contract": str(output_dir / "phase274_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase274_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase274_acceptance_summary.csv"),
                "report": str(output_dir / "phase274_focused_capital_followthrough_interpretation_report.md"),
                "manifest": str(output_dir / "phase274_focused_capital_followthrough_interpretation_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase274_interpretation_only_no_new_replay",
        ),
    }
    (output_dir / "phase274_focused_capital_followthrough_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase274 focused capital follow-through interpretation.")
    parser.add_argument("--phase273-dir", type=Path, default=DEFAULT_PHASE273_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase273_dir=args.phase273_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

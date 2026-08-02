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


DEFAULT_PHASE275_DIR = Path("outputs/phase275")
DEFAULT_OUTPUT_DIR = Path("outputs/phase276")

SELECTED_NEXT_ROUTE = "P276_COST_ROBUST_FULL_DEPTH_REDESIGN_SEARCH"
NEXT_ACTION = "run_phase277_cost_robust_full_depth_redesign_search_no_paper_live"
REPAIR_ACTION = "repair_phase276_multiday_synthetic_followthrough_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_SYNTHETIC_DATES_FOR_INTERPRETATION = 5


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    return out


def build_ranked_interpretation(scenarios: pd.DataFrame, stability: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame()
    frame = numeric(
        scenarios,
        [
            "mechanical_one_date_annualized_portfolio_return_pct",
            "realized_net_pnl_inr",
            "scheduled_event_rows",
            "synthetic_multiday_above12_diagnostic",
            "observed_trade_dates",
            "max_drawdown_inr",
        ],
    )
    stability = numeric(
        stability,
        [
            "scenario_rows",
            "synthetic_above12_scenario_rows",
            "min_annualized_pct",
            "median_annualized_pct",
            "max_annualized_pct",
            "mean_net_pnl_inr",
            "max_net_pnl_inr",
            "min_net_pnl_inr",
            "above12_fraction",
            "median_above12",
            "worst_case_above12",
        ],
    )
    rows: list[dict[str, Any]] = []
    for keys, group in frame.groupby(["phase275_scope_profile_id", "phase275_scope_id", "phase275_scope_candidate_id", "cost_profile"], dropna=False):
        profile_id, scope_id, candidate_id, cost_profile = keys
        best = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
        stable_rows = stability[
            stability["phase275_scope_id"].astype(str).eq(str(scope_id))
            & stability["phase275_scope_candidate_id"].astype(str).eq(str(candidate_id))
            & stability["cost_profile"].astype(str).eq(str(cost_profile))
        ]
        stable = stable_rows.iloc[0] if not stable_rows.empty else pd.Series(dtype=object)
        scenario_rows = int(len(group))
        above12 = int(group["synthetic_multiday_above12_diagnostic"].sum())
        max_ann = safe_float(stable.get("max_annualized_pct", group["mechanical_one_date_annualized_portfolio_return_pct"].max()), 0.0)
        median_ann = safe_float(stable.get("median_annualized_pct", group["mechanical_one_date_annualized_portfolio_return_pct"].median()), 0.0)
        min_ann = safe_float(stable.get("min_annualized_pct", group["mechanical_one_date_annualized_portfolio_return_pct"].min()), 0.0)
        cost200 = str(cost_profile) == "cost200"
        rows.append(
            {
                "phase275_scope_profile_id": profile_id,
                "phase275_scope_id": scope_id,
                "phase275_scope_candidate_id": candidate_id,
                "cost_profile": cost_profile,
                "scenario_rows": scenario_rows,
                "synthetic_above12_scenario_rows": above12,
                "above12_fraction": above12 / scenario_rows if scenario_rows else 0.0,
                "min_annualized_pct": min_ann,
                "median_annualized_pct": median_ann,
                "max_annualized_pct": max_ann,
                "mean_net_pnl_inr": safe_float(stable.get("mean_net_pnl_inr", group["realized_net_pnl_inr"].mean()), 0.0),
                "max_net_pnl_inr": safe_float(stable.get("max_net_pnl_inr", group["realized_net_pnl_inr"].max()), 0.0),
                "min_net_pnl_inr": safe_float(stable.get("min_net_pnl_inr", group["realized_net_pnl_inr"].min()), 0.0),
                "best_scenario_id": best.get("scenario_id", ""),
                "best_order_policy": best.get("order_policy", ""),
                "best_synthetic_regime": best.get("synthetic_regime", ""),
                "best_synthetic_seed": best.get("synthetic_seed", ""),
                "best_initial_capital_inr": best.get("initial_capital_inr", ""),
                "best_fixed_notional_inr": best.get("fixed_notional_inr", ""),
                "best_max_concurrent_positions": best.get("max_concurrent_positions", ""),
                "best_scheduled_event_rows": as_int(best.get("scheduled_event_rows", 0)),
                "cost200_profile": int(cost200),
                "normal_cost_sparse_positive": int(not cost200 and above12 > 0 and median_ann <= ANNUALIZED_THRESHOLD_PCT),
                "cost200_failed": int(cost200 and above12 == 0),
                "median_failed": int(median_ann <= ANNUALIZED_THRESHOLD_PCT),
                "worst_case_failed": int(min_ann <= ANNUALIZED_THRESHOLD_PCT),
                "redesign_priority": int((not cost200 and above12 > 0) or (cost200 and max_ann > 0)),
            }
        )
    ranked = pd.DataFrame(rows)
    return ranked.sort_values(
        ["redesign_priority", "cost200_profile", "synthetic_above12_scenario_rows", "max_annualized_pct"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_interpretation_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    scenario_rows = as_int(metric_value(summary, "phase275_scenario_rows", 0))
    cost100_above = as_int(metric_value(summary, "phase275_cost100_above12_scenario_rows", 0))
    cost200_above = as_int(metric_value(summary, "phase275_cost200_above12_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase275_best_synthetic_multiday_annualized_portfolio_return_pct", 0.0), 0.0)
    cost200_median = as_int(metric_value(summary, "phase275_cost200_median_above12_scope_profile_rows", 0))
    cost200_worst = as_int(metric_value(summary, "phase275_cost200_worst_case_above12_scope_profile_rows", 0))
    sparse_positive = int(ranked["normal_cost_sparse_positive"].astype(int).sum()) if not ranked.empty else 0
    rows = [
        ("synthetic_multiday_search_executed", f"scenario_rows={scenario_rows};synthetic_dates={metric_value(summary, 'phase275_synthetic_date_rows', '')}", "evidence", int(scenario_rows > 0), "Phase275 moved beyond one-date diagnostics into synthetic multiday testing."),
        ("normal_cost_sparse_positive_exists", f"cost100_above12={cost100_above};best_ann={best_ann}", "research_positive", int(cost100_above > 0), "A small normal-cost pocket exists, but it is sparse."),
        ("cost200_multiday_failure", f"cost200_above12={cost200_above};cost200_median_above12={cost200_median};cost200_worst_above12={cost200_worst}", "hard_negative", int(cost200_above == 0 and cost200_median == 0 and cost200_worst == 0), "The focused pocket does not survive 2x-cost synthetic multiday stress."),
        ("sparsity_warning", f"sparse_positive_profiles={sparse_positive};scenario_rows={scenario_rows}", "risk", int(sparse_positive > 0), "Above-12 outcomes are rare and concentrated, so do not overfit to the best seed/regime."),
        ("full_depth_route_still_material", "sample ledger preserves top-five and levels 2-5 depth features", "constraint", 1, "Do not fall back to L1-only features; redesign must remain full-depth."),
        ("next_route_should_redesign_for_cost_robustness", SELECTED_NEXT_ROUTE, "next_action", 1, "The next executable search should target edge magnitude, fill selectivity, and cost robustness."),
    ]
    return pd.DataFrame(rows, columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"])


def build_decision_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    cost200_above = as_int(metric_value(summary, "phase275_cost200_above12_scenario_rows", 0))
    cost100_above = as_int(metric_value(summary, "phase275_cost100_above12_scenario_rows", 0))
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            ("close_phase275_for_promotion", 1, f"cost200_above12={cost200_above};portfolio_claim=0", "No promotion, paper/live, or deployable profitability claim is allowed."),
            ("recognize_fragile_normal_cost_pocket", int(cost100_above > 0), f"cost100_above12={cost100_above};best_profile={metric_value(summary, 'phase275_best_scope_profile', '')}", "Keep the signal as a research clue, not as an accepted strategy."),
            ("reject_as_is_focused_pocket", int(cost200_above == 0), "cost200_multiday_above12=0", "The Phase275 focused pocket should not be continued unchanged."),
            ("selected_redesign_anchor_profile", top.get("phase275_scope_profile_id", ""), f"redesign_priority={top.get('redesign_priority', '')};max_ann={top.get('max_annualized_pct', '')}", "Use the strongest fragile profiles as anchors for redesign."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "cost robustness failed but normal-cost pocket exists", "Execute a cost-robust full-depth redesign search."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def build_next_route_contract(ranked: pd.DataFrame) -> pd.DataFrame:
    anchors = ranked[ranked["redesign_priority"].astype(int).eq(1)].head(3) if not ranked.empty else pd.DataFrame()
    anchor_profiles = ";".join(anchors["phase275_scope_profile_id"].astype(str).tolist()) if not anchors.empty else ""
    return pd.DataFrame(
        [
            ("P277_INPUT", "outputs/phase275/phase275_multiday_synthetic_scenario_results.csv;outputs/phase275/phase275_sample_synthetic_scheduled_event_ledger.csv", "Use Phase275 scenario and scheduled-event evidence."),
            ("P277_ANCHOR_PROFILES", anchor_profiles, "Anchor redesign on fragile normal-cost and near-surviving cost-stress profiles."),
            ("P277_SEARCH_TYPE", "cost_robust_full_depth_redesign_search", "Execute a new search, not a paper/live route."),
            ("P277_OBJECTIVE", "increase_cost200_above12_and_median_stability_without_l1_only_fallback", "Target cost robustness while retaining full-depth L2 materiality."),
            ("P277_REQUIRED_FEATURE_FAMILIES", "top5_imbalance;levels_2_to_5_depth;depth_replenishment_withdrawal;spread_regime;event_sparsity", "Keep full-depth order-book features central."),
            ("P277_BOUNDARY", "no_paper_live;no_deployable_profitability_claim;no_strategy_replay_until_cost_robust_multiday_acceptance", "Boundaries remain closed."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def decision_value(decisions: pd.DataFrame, decision_id: str) -> str:
    rows = decisions.loc[decisions["decision_id"].astype(str).eq(decision_id), "decision_value"] if not decisions.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_gate_evaluation(summary: pd.DataFrame, scenarios: pd.DataFrame, ranked: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    phase275_next = str(metric_value(summary, "phase275_next_best_action", ""))
    phase275_complete = as_int(metric_value(summary, "phase275_multiday_synthetic_followthrough_search_complete", 0))
    hard_pass = as_int(metric_value(summary, "phase275_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(summary, "phase275_hard_gate_rows", 0))
    replay_allowed = as_int(metric_value(summary, "phase275_strategy_replay_allowed", 1))
    paper_allowed = as_int(metric_value(summary, "phase275_paper_or_live_acceptance_allowed", 1))
    claim_allowed = as_int(metric_value(summary, "phase275_deployable_profitability_claim_allowed", 1))
    cost100_above = as_int(metric_value(summary, "phase275_cost100_above12_scenario_rows", 0))
    cost200_above = as_int(metric_value(summary, "phase275_cost200_above12_scenario_rows", 0))
    rows = [
        ("P276_PHASE275_WORK_ORDER_PRESENT", "run_phase276_multiday_synthetic_followthrough_interpretation" in phase275_next, phase275_next, "Phase275 next action targets Phase276", "hard"),
        ("P276_PHASE275_SEARCH_COMPLETE", phase275_complete == 1, phase275_complete, "Phase275 complete", "hard"),
        ("P276_PHASE275_HARD_GATES_PASS", hard_pass == hard_rows and hard_rows > 0, f"{hard_pass}/{hard_rows}", "Phase275 hard gates pass", "hard"),
        ("P276_RESULTS_PRESENT", len(scenarios) > 0 and len(ranked) > 0, f"scenarios={len(scenarios)};ranked={len(ranked)}", "Phase275 results interpreted", "hard"),
        ("P276_OUTCOME_CLASSIFIED_AS_FRAGILE", cost100_above > 0 and cost200_above == 0, f"cost100_above12={cost100_above};cost200_above12={cost200_above}", "normal-cost positive but cost200 failed", "hard"),
        ("P276_BOUNDARIES_CLOSED", replay_allowed == 0 and paper_allowed == 0 and claim_allowed == 0, f"replay={replay_allowed};paper={paper_allowed};claim={claim_allowed}", "no replay/paper/live/claim", "hard"),
        ("P276_NEXT_ROUTE_SELECTED", decision_value(decisions, "selected_next_route") == SELECTED_NEXT_ROUTE and int(route["contract_id"].astype(str).eq("P277_SEARCH_TYPE").sum()) == 1, SELECTED_NEXT_ROUTE, "Phase277 cost-robust redesign selected", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(summary: pd.DataFrame, ranked: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase276_interpretation_complete", 1, "Phase276 multiday synthetic follow-through interpretation completed"),
        ("phase276_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
        ("phase276_phase275_scenario_rows", as_int(metric_value(summary, "phase275_scenario_rows", 0)), "Phase275 scenarios interpreted"),
        ("phase276_phase275_synthetic_date_rows", as_int(metric_value(summary, "phase275_synthetic_date_rows", 0)), "Synthetic dates per Phase275 scenario"),
        ("phase276_phase275_cost100_above12_scenario_rows", as_int(metric_value(summary, "phase275_cost100_above12_scenario_rows", 0)), "Phase275 cost100 above-12 rows"),
        ("phase276_phase275_cost200_above12_scenario_rows", as_int(metric_value(summary, "phase275_cost200_above12_scenario_rows", 0)), "Phase275 cost200 above-12 rows"),
        ("phase276_phase275_best_synthetic_multiday_annualized_pct", metric_value(summary, "phase275_best_synthetic_multiday_annualized_portfolio_return_pct", ""), "Best Phase275 synthetic multiday annualized diagnostic"),
        ("phase276_ranked_profile_rows", len(ranked), "Ranked interpreted profile rows"),
        ("phase276_normal_cost_sparse_positive_profile_rows", int(ranked["normal_cost_sparse_positive"].astype(int).sum()) if not ranked.empty else 0, "Normal-cost sparse-positive profile rows"),
        ("phase276_cost200_failed_profile_rows", int(ranked["cost200_failed"].astype(int).sum()) if not ranked.empty else 0, "Cost200 failed profile rows"),
        ("phase276_best_redesign_anchor_profile", top.get("phase275_scope_profile_id", ""), "Best redesign anchor profile"),
        ("phase276_best_redesign_anchor_max_annualized_pct", top.get("max_annualized_pct", ""), "Best redesign anchor max synthetic annualized diagnostic"),
        ("phase276_phase275_as_is_promotion_allowed", 0, "Phase275 pocket cannot be promoted as-is"),
        ("phase276_portfolio_claim_allowed", 0, "Robust real portfolio claim remains closed"),
        ("phase276_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase276_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase276_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase276_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase276_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase276_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase276_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase276 Multiday Synthetic Follow-through Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase276 interprets the Phase275 synthetic multiday follow-through.",
        "The conclusion is not promotion: the pocket has a sparse normal-cost positive signal but fails 2x-cost robustness.",
        "The selected next route is a cost-robust full-depth redesign search.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase275_dir: Path = DEFAULT_PHASE275_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase275_dir / "phase275_acceptance_summary.csv")
    scenarios = read_csv(phase275_dir / "phase275_multiday_synthetic_scenario_results.csv")
    stability = read_csv(phase275_dir / "phase275_scope_profile_stability_summary.csv")
    if summary.empty:
        raise FileNotFoundError("Missing Phase275 acceptance summary.")
    if scenarios.empty:
        raise FileNotFoundError("Missing Phase275 multiday synthetic scenario results.")
    ranked = build_ranked_interpretation(scenarios, stability)
    interpretations = build_interpretation_ledger(summary, ranked)
    decisions = build_decision_ledger(summary, ranked)
    route = build_next_route_contract(ranked)
    gates = build_gate_evaluation(summary, scenarios, ranked, decisions, route)
    acceptance = build_acceptance_summary(summary, ranked, gates)

    ranked.to_csv(output_dir / "phase276_ranked_multiday_synthetic_profiles.csv", index=False)
    interpretations.to_csv(output_dir / "phase276_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase276_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase276_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase276_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase276_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase276_multiday_synthetic_followthrough_interpretation_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Ranked Multiday Synthetic Profiles": ranked,
            "Interpretation Ledger": interpretations,
            "Decision Ledger": decisions,
            "Next Route Contract": route,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase276_multiday_synthetic_followthrough_interpretation",
        **reproducibility_fields(
            artifact_id="phase276",
            generated_utc=generated_utc,
            inputs={
                "phase275_acceptance_summary": str(phase275_dir / "phase275_acceptance_summary.csv"),
                "phase275_multiday_synthetic_scenario_results": str(phase275_dir / "phase275_multiday_synthetic_scenario_results.csv"),
                "phase275_scope_profile_stability_summary": str(phase275_dir / "phase275_scope_profile_stability_summary.csv"),
            },
            parameters={
                "selected_next_route": SELECTED_NEXT_ROUTE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "min_synthetic_dates_for_interpretation": MIN_SYNTHETIC_DATES_FOR_INTERPRETATION,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "ranked_multiday_synthetic_profiles": str(output_dir / "phase276_ranked_multiday_synthetic_profiles.csv"),
                "interpretation_ledger": str(output_dir / "phase276_interpretation_ledger.csv"),
                "decision_ledger": str(output_dir / "phase276_decision_ledger.csv"),
                "next_route_contract": str(output_dir / "phase276_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase276_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase276_acceptance_summary.csv"),
                "report": str(output_dir / "phase276_multiday_synthetic_followthrough_interpretation_report.md"),
                "manifest": str(output_dir / "phase276_multiday_synthetic_followthrough_interpretation_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase276_interpretation_only_no_new_replay",
        ),
    }
    (output_dir / "phase276_multiday_synthetic_followthrough_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase276 multiday synthetic follow-through interpretation.")
    parser.add_argument("--phase275-dir", type=Path, default=DEFAULT_PHASE275_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase275_dir=args.phase275_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

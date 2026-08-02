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


DEFAULT_PHASE283_DIR = Path("outputs/phase283")
DEFAULT_OUTPUT_DIR = Path("outputs/phase284")

SELECTED_NEXT_ROUTE = "P284_EVENT_LIFECYCLE_EXIT_SIDE_REDESIGN_PRECOMMIT"
NEXT_ACTION = "run_phase285_event_lifecycle_exit_side_redesign_precommit_no_paper_live"
REPAIR_ACTION = "repair_phase284_regime_conditioned_full_depth_ensemble_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
SPARSE_DIAGNOSTIC_EVENT_FLOOR = 8
ROBUST_PORTFOLIO_EVENT_FLOOR = 30


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    return out


def build_ranked_ensemble_interpretation(scenarios: pd.DataFrame) -> pd.DataFrame:
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
            "l1_only_variant",
            "uses_net_edge_as_live_mask",
            "uses_top5",
            "uses_levels_2_to_5",
            "initial_capital_inr",
            "fixed_notional_inr",
            "max_concurrent_positions",
            "notional_turnover_x_initial_capital",
            "avg_open_notional_utilization",
        ],
    )
    rows: list[dict[str, Any]] = []
    for variant_id, group in frame.groupby("phase283_variant_id", dropna=False):
        ranked = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False)
        best = ranked.iloc[0]
        max_ann = safe_float(best.get("mechanical_one_date_annualized_portfolio_return_pct", 0.0), 0.0)
        max_events = int(group["scheduled_event_rows"].max())
        rows.append(
            {
                "phase283_variant_id": str(variant_id),
                "ensemble_family_id": best.get("ensemble_family_id", ""),
                "ensemble_family": best.get("ensemble_family", ""),
                "bucket_id": best.get("bucket_id", ""),
                "bucket_rule": best.get("bucket_rule", ""),
                "vote_threshold": as_int(best.get("vote_threshold", 0)),
                "seed_ids": best.get("seed_ids", ""),
                "included_target_families": best.get("included_target_families", ""),
                "scenario_rows": int(len(group)),
                "selected_event_rows": int(group["selected_event_rows"].max()),
                "max_scheduled_event_rows": max_events,
                "cost200_above12_sparse_diagnostic_rows": int(group["cost200_above12_sparse_diagnostic"].sum()),
                "sparse_floor_met_rows": int(group["sparse_diagnostic_event_floor_met"].sum()),
                "robust_portfolio_floor_met_rows": int(group["robust_portfolio_event_floor_met"].sum()),
                "max_annualized_pct": max_ann,
                "median_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].median()),
                "min_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].min()),
                "max_net_pnl_inr": float(group["realized_net_pnl_inr"].max()),
                "best_scenario_id": best.get("scenario_id", ""),
                "best_initial_capital_inr": best.get("initial_capital_inr", ""),
                "best_fixed_notional_inr": best.get("fixed_notional_inr", ""),
                "best_max_concurrent_positions": best.get("max_concurrent_positions", ""),
                "best_notional_turnover_x_initial_capital": best.get("notional_turnover_x_initial_capital", ""),
                "best_avg_open_notional_utilization": best.get("avg_open_notional_utilization", ""),
                "uses_top5": as_int(best.get("uses_top5", 0)),
                "uses_levels_2_to_5": as_int(best.get("uses_levels_2_to_5", 0)),
                "l1_only_variant": as_int(best.get("l1_only_variant", 0)),
                "uses_net_edge_as_live_mask": as_int(best.get("uses_net_edge_as_live_mask", 0)),
                "near_miss_under_12": int(0.0 < max_ann < ANNUALIZED_THRESHOLD_PCT),
                "too_sparse_for_portfolio_claim": int(max_events < ROBUST_PORTFOLIO_EVENT_FLOOR),
                "full_depth_positive_clue": int(max_ann > 0.0 and as_int(best.get("l1_only_variant", 0)) == 0 and as_int(best.get("uses_levels_2_to_5", 0)) == 1),
                "same_route_exhausted_for_acceptance": int(max_ann < ANNUALIZED_THRESHOLD_PCT or max_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR),
            }
        )
    ranked = pd.DataFrame(rows)
    return ranked.sort_values(
        [
            "full_depth_positive_clue",
            "cost200_above12_sparse_diagnostic_rows",
            "robust_portfolio_floor_met_rows",
            "max_annualized_pct",
            "max_scheduled_event_rows",
        ],
        ascending=[False, False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_family_interpretation(variant_summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    if variant_summary.empty:
        return pd.DataFrame()
    frame = numeric(
        variant_summary,
        [
            "scenario_rows",
            "selected_event_rows",
            "max_scheduled_event_rows",
            "cost200_above12_sparse_diagnostic_rows",
            "sparse_floor_met_rows",
            "robust_portfolio_floor_met_rows",
            "min_annualized_pct",
            "median_annualized_pct",
            "max_annualized_pct",
            "max_net_pnl_inr",
            "median_above12",
        ],
    )
    rows: list[dict[str, Any]] = []
    for family, group in frame.groupby("ensemble_family", dropna=False):
        family_ranked = ranked[ranked["ensemble_family"].astype(str).eq(str(family))] if not ranked.empty else pd.DataFrame()
        best = group.sort_values("max_annualized_pct", ascending=False).iloc[0]
        rows.append(
            {
                "ensemble_family": str(family),
                "variant_rows": int(group["phase283_variant_id"].astype(str).nunique()) if "phase283_variant_id" in group.columns else int(len(group)),
                "scenario_rows": int(group["scenario_rows"].sum()),
                "selected_event_rows_max": int(group["selected_event_rows"].max()),
                "max_scheduled_event_rows": int(group["max_scheduled_event_rows"].max()),
                "cost200_above12_sparse_diagnostic_rows": int(group["cost200_above12_sparse_diagnostic_rows"].sum()),
                "sparse_floor_met_rows": int(group["sparse_floor_met_rows"].sum()),
                "robust_portfolio_floor_met_rows": int(group["robust_portfolio_floor_met_rows"].sum()),
                "min_annualized_pct": float(group["min_annualized_pct"].min()),
                "median_annualized_pct": float(group["median_annualized_pct"].median()),
                "max_annualized_pct": float(group["max_annualized_pct"].max()),
                "max_net_pnl_inr": float(group["max_net_pnl_inr"].max()),
                "best_variant_id": best.get("phase283_variant_id", ""),
                "positive_full_depth_clue_variants": int(family_ranked["full_depth_positive_clue"].astype(int).sum()) if not family_ranked.empty else 0,
                "near_miss_variants": int(family_ranked["near_miss_under_12"].astype(int).sum()) if not family_ranked.empty else 0,
                "close_family_for_acceptance": int(int(group["cost200_above12_sparse_diagnostic_rows"].sum()) == 0),
                "preserve_as_lifecycle_redesign_seed": int(float(group["max_annualized_pct"].max()) > 0.0),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["preserve_as_lifecycle_redesign_seed", "max_annualized_pct", "max_scheduled_event_rows"],
        ascending=[False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_interpretation_ledger(summary: pd.DataFrame, ranked: pd.DataFrame, seeds: pd.DataFrame) -> pd.DataFrame:
    scenario_rows = as_int(metric_value(summary, "phase283_scenario_rows", 0))
    above12 = as_int(metric_value(summary, "phase283_sparse_above12_scenario_rows", 0))
    robust = as_int(metric_value(summary, "phase283_robust_portfolio_floor_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase283_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase283_best_scheduled_event_rows", 0))
    l1_only = as_int(metric_value(summary, "phase283_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase283_net_edge_live_mask_rows", 0))
    material_clues = int(ranked["full_depth_positive_clue"].astype(int).sum()) if not ranked.empty else 0
    repaired_seeds = int(pd.to_numeric(seeds.get("net_edge_live_mask_removed", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not seeds.empty else 0
    return pd.DataFrame(
        [
            ("phase283_executed", f"scenario_rows={scenario_rows}", "evidence", int(scenario_rows > 0), "Phase283 executed the regime-conditioned full-depth ensemble search."),
            ("no_sparse_above12_survivor", f"sparse_above12_rows={above12};best_ann={best_ann}", "hard_negative", int(above12 == 0 and best_ann < ANNUALIZED_THRESHOLD_PCT), "No Phase283 scenario crossed the >12% cost200 sparse diagnostic threshold."),
            ("no_robust_portfolio_floor_survivor", f"robust_floor_rows={robust};best_events={best_events}", "hard_negative", int(robust == 0), "No Phase283 scenario met the robust portfolio event floor."),
            ("near_miss_remains_too_sparse", f"best_ann={best_ann};best_scheduled_events={best_events}", "risk", int(0.0 < best_ann < ANNUALIZED_THRESHOLD_PCT and best_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR), "The best clue remains a sparse near-miss, not a profitable strategy."),
            ("full_depth_boundary_preserved", f"l1_only={l1_only};live_label_leakage={leakage};repaired_seeds={repaired_seeds}", "constraint", int(l1_only == 0 and leakage == 0), "Full top-five depth and no-live-leakage boundaries held."),
            ("same_ensemble_route_should_close_for_acceptance", "cost200_above12=0;robust_floor=0", "decision", 1, "Do not keep iterating the same Phase283 ensemble/filter stack for acceptance."),
            ("next_route_changes_edge_source", SELECTED_NEXT_ROUTE, "next_action", 1, "Move to event lifecycle, side, and exit redesign rather than relaxing thresholds or adding more filters."),
        ],
        columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"],
    )


def build_decision_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    above12 = as_int(metric_value(summary, "phase283_sparse_above12_scenario_rows", 0))
    robust = as_int(metric_value(summary, "phase283_robust_portfolio_floor_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase283_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase283_best_scheduled_event_rows", 0))
    return pd.DataFrame(
        [
            ("close_phase283_ensemble_route_for_acceptance", int(above12 == 0 and robust == 0), f"sparse_above12={above12};robust_floor={robust};best_ann={best_ann}", "Do not accept or promote Phase283 ensemble search."),
            ("preserve_best_full_depth_near_miss_clue", top.get("phase283_variant_id", ""), f"family={top.get('ensemble_family', '')};bucket={top.get('bucket_id', '')};scheduled_events={best_events}", "Preserve best clue only as evidence for lifecycle redesign."),
            ("do_not_relax_cost_threshold", 1, "cost200_required;threshold=12", "Do not convert the below-12 near-miss into an acceptance rule."),
            ("do_not_claim_portfolio_return", 1, f"best_scheduled_events={best_events};sparse_floor={SPARSE_DIAGNOSTIC_EVENT_FLOOR};robust_floor={ROBUST_PORTFOLIO_EVENT_FLOOR}", "Sparse near-miss is not a robust annual portfolio-return claim."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "ensemble route exhausted; edge source must change", "Precommit event lifecycle/side/exit redesign."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def build_next_route_contract(ranked: pd.DataFrame, families: pd.DataFrame) -> pd.DataFrame:
    top_clues = ranked[ranked["full_depth_positive_clue"].astype(int).eq(1)].head(10) if not ranked.empty else pd.DataFrame()
    clue_ids = ";".join(top_clues["phase283_variant_id"].astype(str).tolist()) if not top_clues.empty else ""
    family_ids = ";".join(families[families["preserve_as_lifecycle_redesign_seed"].astype(int).eq(1)]["ensemble_family"].astype(str).tolist()) if not families.empty else ""
    return pd.DataFrame(
        [
            ("P285_INPUTS", "outputs/phase277/phase277_cost200_redesign_event_universe.csv;outputs/phase283/phase283_regime_conditioned_ensemble_scenario_results.csv;outputs/phase283/phase283_sample_regime_conditioned_scheduled_event_ledger.csv", "Use the full-depth event universe and Phase283 scheduled near-miss evidence."),
            ("P285_PRESERVED_PHASE283_CLUES", clue_ids, "Carry forward positive full-depth near-miss ensemble variants only as clues."),
            ("P285_PRESERVED_FAMILIES", family_ids, "Carry forward ensemble families with positive diagnostics as seed context."),
            ("P285_SEARCH_TYPE", "event_lifecycle_exit_side_redesign", "Search side, entry timing, exit horizon, stop/timeout/take-profit lifecycle, and order timing instead of only more filters."),
            ("P285_REQUIRED_DIRECTIONS", "follow_vs_reversal_side;latency_bucket;entry_delay_ticks;exit_horizon_ticks;take_profit_bps;stop_loss_bps;timeout_exit;queue_adversity;fixed_capital_cost200", "Change the source of edge while keeping cost and capacity realism."),
            ("P285_FULL_DEPTH_REQUIREMENT", "top_five_rows_1_to_5_required;levels_2_to_5_materiality_required;beyond_l1_features_required;l1_only_forbidden", "The next search must continue using full Zerodha top-five depth."),
            ("P285_ACCEPTANCE_DIAGNOSTICS", f"cost200_annualized_pct_gt_{ANNUALIZED_THRESHOLD_PCT};scheduled_event_rows_ge_{SPARSE_DIAGNOSTIC_EVENT_FLOOR}_for_sparse_diagnostic;scheduled_event_rows_ge_{ROBUST_PORTFOLIO_EVENT_FLOOR}_for_portfolio_claim", "Sparse >12% is a discovery clue; robust portfolio claim needs many more trades."),
            ("P285_BOUNDARY", "no_paper_live;no_strategy_replay;no_deployable_profitability_claim;net_edge_live_mask_forbidden", "Boundaries remain closed until evidence earns them."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def decision_value(decisions: pd.DataFrame, decision_id: str) -> str:
    rows = decisions.loc[decisions["decision_id"].astype(str).eq(decision_id), "decision_value"] if not decisions.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_gate_evaluation(summary: pd.DataFrame, ranked: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase283_regime_conditioned_ensemble_search_complete", 0))
    next_action = str(metric_value(summary, "phase283_next_best_action", ""))
    hard_pass = as_int(metric_value(summary, "phase283_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(summary, "phase283_hard_gate_rows", 0))
    replay_allowed = as_int(metric_value(summary, "phase283_strategy_replay_allowed", 1))
    paper_allowed = as_int(metric_value(summary, "phase283_paper_or_live_acceptance_allowed", 1))
    claim_allowed = as_int(metric_value(summary, "phase283_deployable_profitability_claim_allowed", 1))
    above12 = as_int(metric_value(summary, "phase283_sparse_above12_scenario_rows", 0))
    robust = as_int(metric_value(summary, "phase283_robust_portfolio_floor_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase283_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase283_best_scheduled_event_rows", 0))
    l1_only = as_int(metric_value(summary, "phase283_l1_only_variant_rows", 0))
    live_leakage = as_int(metric_value(summary, "phase283_net_edge_live_mask_rows", 0))
    rows = [
        ("P284_PHASE283_WORK_ORDER_PRESENT", "run_phase284_regime_conditioned_full_depth_ensemble_interpretation" in next_action, next_action, "Phase283 next action targets Phase284", "hard"),
        ("P284_PHASE283_SEARCH_COMPLETE", complete == 1, complete, "Phase283 complete", "hard"),
        ("P284_PHASE283_HARD_GATES_PASS", hard_pass == hard_rows and hard_rows > 0, f"{hard_pass}/{hard_rows}", "Phase283 hard gates pass", "hard"),
        ("P284_RESULTS_PRESENT", len(ranked) > 0, len(ranked), "Phase283 variants interpreted", "hard"),
        ("P284_OUTCOME_CLASSIFIED_AS_NO_SURVIVOR", above12 == 0 and robust == 0 and best_ann < ANNUALIZED_THRESHOLD_PCT, f"sparse_above12={above12};robust={robust};best_ann={best_ann}", "no accepted cost200 survivor", "hard"),
        ("P284_EVENT_COUNT_REMAINS_TOO_SPARSE", best_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR, best_events, f"<{SPARSE_DIAGNOSTIC_EVENT_FLOOR} scheduled events for sparse diagnostic survivor", "hard"),
        ("P284_FULL_DEPTH_BOUNDARY_PRESERVED", l1_only == 0 and live_leakage == 0, f"l1_only={l1_only};live_leakage={live_leakage}", "full-depth/no-leakage preserved", "hard"),
        ("P284_BOUNDARIES_CLOSED", replay_allowed == 0 and paper_allowed == 0 and claim_allowed == 0, f"replay={replay_allowed};paper={paper_allowed};claim={claim_allowed}", "no replay/paper/live/claim", "hard"),
        ("P284_NEXT_ROUTE_SELECTED", decision_value(decisions, "selected_next_route") == SELECTED_NEXT_ROUTE and int(route["contract_id"].astype(str).eq("P285_SEARCH_TYPE").sum()) == 1, SELECTED_NEXT_ROUTE, "Phase285 lifecycle redesign precommit selected", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(summary: pd.DataFrame, ranked: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase284_interpretation_complete", 1, "Phase284 regime-conditioned full-depth ensemble interpretation completed"),
        ("phase284_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
        ("phase284_phase283_seed_rows", as_int(metric_value(summary, "phase283_seed_rows", 0)), "Phase283 seeds interpreted"),
        ("phase284_phase283_variant_rows", as_int(metric_value(summary, "phase283_variant_rows", 0)), "Phase283 variants interpreted"),
        ("phase284_phase283_scenario_rows", as_int(metric_value(summary, "phase283_scenario_rows", 0)), "Phase283 scenarios interpreted"),
        ("phase284_phase283_sparse_above12_scenario_rows", as_int(metric_value(summary, "phase283_sparse_above12_scenario_rows", 0)), "Phase283 cost200 sparse above-12 rows"),
        ("phase284_phase283_robust_portfolio_floor_scenario_rows", as_int(metric_value(summary, "phase283_robust_portfolio_floor_scenario_rows", 0)), "Phase283 robust floor rows"),
        ("phase284_phase283_best_cost200_annualized_pct", metric_value(summary, "phase283_best_cost200_annualized_pct", ""), "Best Phase283 cost200 annualized diagnostic"),
        ("phase284_phase283_best_realized_net_pnl_inr", metric_value(summary, "phase283_best_realized_net_pnl_inr", ""), "Best Phase283 realized net P&L"),
        ("phase284_phase283_best_scheduled_event_rows", metric_value(summary, "phase283_best_scheduled_event_rows", ""), "Best Phase283 scheduled events"),
        ("phase284_positive_full_depth_clue_variant_rows", int(ranked["full_depth_positive_clue"].astype(int).sum()) if not ranked.empty else 0, "Positive full-depth clue rows"),
        ("phase284_near_miss_variant_rows", int(ranked["near_miss_under_12"].astype(int).sum()) if not ranked.empty else 0, "Near-miss variants below 12%"),
        ("phase284_close_phase283_for_acceptance", 1, "Close Phase283 ensemble route for acceptance"),
        ("phase284_best_preserved_clue_variant", top.get("phase283_variant_id", ""), "Best preserved Phase283 clue variant"),
        ("phase284_best_preserved_clue_family", top.get("ensemble_family", ""), "Best preserved Phase283 clue family"),
        ("phase284_best_preserved_clue_bucket", top.get("bucket_id", ""), "Best preserved Phase283 clue bucket"),
        ("phase284_do_not_relax_cost_threshold", 1, "Keep cost200 threshold"),
        ("phase284_do_not_claim_portfolio_return", 1, "Sparse near-miss is not a robust annual portfolio claim"),
        ("phase284_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase284_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase284_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase284_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase284_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase284_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase284_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase284 Regime-conditioned Full-depth Ensemble Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase284 interprets the Phase283 regime-conditioned full-depth ensemble search.",
        "The route is closed for acceptance because it produced no cost200 >12% sparse diagnostic survivor and no robust event-floor survivor.",
        "The next route changes the source of edge: event lifecycle, side, and exit redesign while keeping full Zerodha top-five depth and cost200 fixed-capital scoring.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase283_dir: Path = DEFAULT_PHASE283_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase283_dir / "phase283_acceptance_summary.csv")
    variant_summary = read_csv(phase283_dir / "phase283_regime_conditioned_ensemble_variant_summary.csv")
    scenarios = read_csv(phase283_dir / "phase283_regime_conditioned_ensemble_scenario_results.csv")
    seeds = read_csv(phase283_dir / "phase283_observable_seed_catalog.csv")
    if summary.empty:
        raise FileNotFoundError("Missing Phase283 acceptance summary.")
    if variant_summary.empty:
        raise FileNotFoundError("Missing Phase283 variant summary.")
    if scenarios.empty:
        raise FileNotFoundError("Missing Phase283 scenario results.")
    if seeds.empty:
        raise FileNotFoundError("Missing Phase283 observable seed catalog.")

    ranked = build_ranked_ensemble_interpretation(scenarios)
    families = build_family_interpretation(variant_summary, ranked)
    interpretations = build_interpretation_ledger(summary, ranked, seeds)
    decisions = build_decision_ledger(summary, ranked)
    route = build_next_route_contract(ranked, families)
    gates = build_gate_evaluation(summary, ranked, decisions, route)
    acceptance = build_acceptance_summary(summary, ranked, gates)

    ranked.to_csv(output_dir / "phase284_ranked_ensemble_interpretation.csv", index=False)
    families.to_csv(output_dir / "phase284_family_interpretation.csv", index=False)
    interpretations.to_csv(output_dir / "phase284_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase284_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase284_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase284_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase284_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase284_regime_conditioned_full_depth_ensemble_interpretation_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Ranked Ensemble Interpretation": ranked.head(20),
            "Family Interpretation": families,
            "Interpretation Ledger": interpretations,
            "Decision Ledger": decisions,
            "Next Route Contract": route,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase284_regime_conditioned_full_depth_ensemble_interpretation",
        **reproducibility_fields(
            artifact_id="phase284",
            generated_utc=generated_utc,
            inputs={
                "phase283_acceptance_summary": str(phase283_dir / "phase283_acceptance_summary.csv"),
                "phase283_variant_summary": str(phase283_dir / "phase283_regime_conditioned_ensemble_variant_summary.csv"),
                "phase283_scenario_results": str(phase283_dir / "phase283_regime_conditioned_ensemble_scenario_results.csv"),
                "phase283_observable_seed_catalog": str(phase283_dir / "phase283_observable_seed_catalog.csv"),
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
                "ranked_ensemble_interpretation": str(output_dir / "phase284_ranked_ensemble_interpretation.csv"),
                "family_interpretation": str(output_dir / "phase284_family_interpretation.csv"),
                "interpretation_ledger": str(output_dir / "phase284_interpretation_ledger.csv"),
                "decision_ledger": str(output_dir / "phase284_decision_ledger.csv"),
                "next_route_contract": str(output_dir / "phase284_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase284_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase284_acceptance_summary.csv"),
                "report": str(output_dir / "phase284_regime_conditioned_full_depth_ensemble_interpretation_report.md"),
                "manifest": str(output_dir / "phase284_regime_conditioned_full_depth_ensemble_interpretation_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase284_interpretation_only_no_new_replay",
        ),
    }
    (output_dir / "phase284_regime_conditioned_full_depth_ensemble_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase284 regime-conditioned full-depth ensemble interpretation.")
    parser.add_argument("--phase283-dir", type=Path, default=DEFAULT_PHASE283_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase283_dir=args.phase283_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

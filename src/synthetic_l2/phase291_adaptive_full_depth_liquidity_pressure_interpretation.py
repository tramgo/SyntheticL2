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


DEFAULT_PHASE290_DIR = Path("outputs/phase290")
DEFAULT_OUTPUT_DIR = Path("outputs/phase291")

SELECTED_NEXT_ROUTE = "P291_ADAPTIVE_PRESSURE_BREADTH_REPAIR_SEARCH"
NEXT_ACTION = "run_phase292_adaptive_pressure_breadth_repair_search_no_paper_live"
REPAIR_ACTION = "repair_phase291_adaptive_full_depth_liquidity_pressure_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
SPARSE_DIAGNOSTIC_EVENT_FLOOR = 8
ROBUST_PORTFOLIO_EVENT_FLOOR = 30


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    return out


def build_ranked_adaptive_interpretation(scenarios: pd.DataFrame) -> pd.DataFrame:
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
    for variant_id, group in frame.groupby("phase290_variant_id", dropna=False):
        ranked = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False)
        best = ranked.iloc[0]
        max_ann = safe_float(best.get("mechanical_one_date_annualized_portfolio_return_pct", 0.0), 0.0)
        max_events = int(group["scheduled_event_rows"].max())
        rows.append(
            {
                "phase290_variant_id": str(variant_id),
                "adaptive_family": best.get("adaptive_family", ""),
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
                "annualized_above12_but_too_sparse": int(max_ann > ANNUALIZED_THRESHOLD_PCT and max_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR),
                "positive_but_below12": int(0.0 < max_ann < ANNUALIZED_THRESHOLD_PCT),
                "too_sparse_for_sparse_diagnostic": int(max_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR),
                "too_sparse_for_portfolio_claim": int(max_events < ROBUST_PORTFOLIO_EVENT_FLOOR),
                "full_depth_positive_clue": int(max_ann > 0.0 and as_int(best.get("uses_levels_2_to_5", 0)) == 1 and as_int(best.get("l1_only_variant", 0)) == 0),
                "same_adaptive_route_exhausted_for_acceptance": int(max_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR or int(group["cost200_above12_sparse_diagnostic"].sum()) == 0),
            }
        )
    return pd.DataFrame(rows).sort_values(
        [
            "annualized_above12_but_too_sparse",
            "cost200_above12_sparse_diagnostic_rows",
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
            "annualized_above12_but_too_sparse",
            "full_depth_positive_clue",
        ],
    )
    rows: list[dict[str, Any]] = []
    for family, group in frame.groupby("adaptive_family", dropna=False):
        best = group.sort_values("max_annualized_pct", ascending=False).iloc[0]
        rows.append(
            {
                "adaptive_family": str(family),
                "variant_rows": int(group["phase290_variant_id"].astype(str).nunique()),
                "scenario_rows": int(group["scenario_rows"].sum()),
                "selected_event_rows_max": int(group["selected_event_rows"].max()),
                "max_scheduled_event_rows": int(group["max_scheduled_event_rows"].max()),
                "above12_but_too_sparse_variants": int(group["annualized_above12_but_too_sparse"].sum()),
                "cost200_above12_sparse_diagnostic_rows": int(group["cost200_above12_sparse_diagnostic_rows"].sum()),
                "robust_portfolio_floor_above12_rows": int(group["robust_portfolio_floor_above12_rows"].sum()),
                "sparse_floor_met_rows": int(group["sparse_floor_met_rows"].sum()),
                "robust_portfolio_floor_met_rows": int(group["robust_portfolio_floor_met_rows"].sum()),
                "min_annualized_pct": float(group["min_annualized_pct"].min()),
                "median_annualized_pct": float(group["median_annualized_pct"].median()),
                "max_annualized_pct": float(group["max_annualized_pct"].max()),
                "max_net_pnl_inr": float(group["max_net_pnl_inr"].max()),
                "best_variant_id": best.get("phase290_variant_id", ""),
                "full_depth_positive_clue_variants": int(group["full_depth_positive_clue"].sum()),
                "preserve_breadth_repair_clue": int(float(group["max_annualized_pct"].max()) > ANNUALIZED_THRESHOLD_PCT),
                "close_family_for_acceptance": int(int(group["cost200_above12_sparse_diagnostic_rows"].sum()) == 0),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["preserve_breadth_repair_clue", "max_annualized_pct", "max_scheduled_event_rows"],
        ascending=[False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_interpretation_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    scenarios = as_int(metric_value(summary, "phase290_scenario_rows", 0))
    above12 = as_int(metric_value(summary, "phase290_sparse_above12_scenario_rows", 0))
    robust_above12 = as_int(metric_value(summary, "phase290_robust_portfolio_above12_scenario_rows", 0))
    robust_floor = as_int(metric_value(summary, "phase290_robust_portfolio_floor_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase290_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase290_best_scheduled_event_rows", 0))
    l1_only = as_int(metric_value(summary, "phase290_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase290_net_edge_live_mask_rows", 0))
    sparks = int(ranked["annualized_above12_but_too_sparse"].astype(int).sum()) if not ranked.empty else 0
    return pd.DataFrame(
        [
            ("phase290_executed", f"scenario_rows={scenarios}", "evidence", int(scenarios > 0), "Phase290 executed adaptive full-depth pressure expansion."),
            ("above12_spark_exists_but_too_sparse", f"best_ann={best_ann};best_events={best_events};spark_variants={sparks}", "research_clue", int(best_ann > ANNUALIZED_THRESHOLD_PCT and best_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR), "The high annualized result is a spark, not an accepted strategy."),
            ("no_sparse_above12_survivor", f"sparse_above12_rows={above12}", "hard_negative", int(above12 == 0), "No Phase290 scenario met both >12% and the sparse event floor."),
            ("no_robust_portfolio_survivor", f"robust_floor_rows={robust_floor};robust_above12_rows={robust_above12}", "hard_negative", int(robust_floor == 0 and robust_above12 == 0), "No robust portfolio evidence exists."),
            ("full_depth_boundary_preserved", f"l1_only={l1_only};live_label_leakage={leakage}", "constraint", int(l1_only == 0 and leakage == 0), "Full-depth and no-live-leakage boundaries held."),
            ("same_adaptive_route_should_close_for_acceptance", "event_floor_failed", "decision", 1, "Do not accept the one-event adaptive spark."),
            ("next_route_should_repair_breadth", SELECTED_NEXT_ROUTE, "next_action", 1, "Search whether adaptive pressure clues can be broadened without relaxing cost/capital rules."),
        ],
        columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"],
    )


def build_decision_ledger(summary: pd.DataFrame, ranked: pd.DataFrame, families: pd.DataFrame) -> pd.DataFrame:
    top = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    best_ann = safe_float(metric_value(summary, "phase290_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase290_best_scheduled_event_rows", 0))
    preserved = ";".join(families.loc[families["preserve_breadth_repair_clue"].astype(int).eq(1), "adaptive_family"].astype(str).tolist()) if not families.empty else ""
    return pd.DataFrame(
        [
            ("close_phase290_adaptive_route_for_acceptance", 1, f"best_ann={best_ann};best_events={best_events};event_floor={SPARSE_DIAGNOSTIC_EVENT_FLOOR}", "Do not accept, replay, or promote Phase290."),
            ("preserve_best_adaptive_pressure_spark", top.get("phase290_variant_id", ""), f"family={top.get('adaptive_family', '')};interaction={top.get('interaction_column', '')};scheduled_events={best_events}", "Carry forward only as a breadth-repair clue."),
            ("preserved_families_for_breadth_repair", preserved, "above-12 but too sparse or positive diagnostics", "Preserve families as search context, not as accepted strategies."),
            ("do_not_relax_annualized_denominator", 1, "fixed_initial_capital_required", "Annualized return remains fixed-capital based."),
            ("do_not_claim_portfolio_return", 1, f"best_scheduled_events={best_events};robust_floor={ROBUST_PORTFOLIO_EVENT_FLOOR}", "Evidence is too sparse for a portfolio-return claim."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "adaptive route found spark but failed breadth", "Run adaptive pressure breadth repair."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def decision_value(decisions: pd.DataFrame, decision_id: str) -> str:
    rows = decisions.loc[decisions["decision_id"].astype(str).eq(decision_id), "decision_value"] if not decisions.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_next_route_contract(families: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    top_clues = ranked[ranked["annualized_above12_but_too_sparse"].astype(int).eq(1)].head(12) if not ranked.empty else pd.DataFrame()
    clue_ids = ";".join(top_clues["phase290_variant_id"].astype(str).tolist()) if not top_clues.empty else ""
    family_ids = ";".join(families.loc[families["preserve_breadth_repair_clue"].astype(int).eq(1), "adaptive_family"].astype(str).tolist()) if not families.empty else ""
    return pd.DataFrame(
        [
            ("P292_INPUTS", "outputs/phase277/phase277_cost200_redesign_event_universe.csv;outputs/phase290/phase290_adaptive_pressure_scenario_results.csv;outputs/phase290/phase290_adaptive_pressure_variant_summary.csv", "Use event universe plus Phase290 spark evidence."),
            ("P292_PRESERVED_PHASE290_SPARKS", clue_ids, "Carry forward above-12 but too-sparse adaptive variants only as breadth-repair clues."),
            ("P292_PRESERVED_ADAPTIVE_FAMILIES", family_ids, "Keep adaptive families with sparks for breadth repair."),
            ("P292_SEARCH_TYPE", "adaptive_pressure_breadth_repair_search", "Broaden event counts while preserving observable full-depth L2 masks."),
            ("P292_REQUIRED_DIRECTIONS", "looser_but_feature_only_thresholds;family_context_transfer;open_to_all_bucket_transfer;horizon_and_concurrency_breadth;cost200_fixed_capital_scheduler", "Repair breadth without using future labels as live masks."),
            ("P292_CAPITAL_AND_COST", "initial_capital_100000;cost200_required;fixed_notional_grid;max_concurrent_grid;annualized_denominator_fixed_capital", "No unlimited-capital annualized return."),
            ("P292_ACCEPTANCE_DIAGNOSTICS", f"cost200_annualized_pct_gt_{ANNUALIZED_THRESHOLD_PCT};scheduled_event_rows_ge_{SPARSE_DIAGNOSTIC_EVENT_FLOOR}_for_sparse_discovery;scheduled_event_rows_ge_{ROBUST_PORTFOLIO_EVENT_FLOOR}_for_portfolio_claim", "Sparse >12% remains discovery only; robust portfolio claim needs a larger event floor."),
            ("P292_BOUNDARY", "no_paper_live;no_strategy_replay;no_deployable_profitability_claim;l1_only_forbidden;net_edge_live_mask_forbidden", "Boundaries remain closed until evidence earns them."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_gate_evaluation(summary: pd.DataFrame, ranked: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase290_adaptive_liquidity_pressure_search_complete", 0))
    next_action = str(metric_value(summary, "phase290_next_best_action", ""))
    hard_pass = as_int(metric_value(summary, "phase290_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(summary, "phase290_hard_gate_rows", 0))
    l1_only = as_int(metric_value(summary, "phase290_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase290_net_edge_live_mask_rows", 0))
    replay = as_int(metric_value(summary, "phase290_strategy_replay_allowed", 0))
    paper = as_int(metric_value(summary, "phase290_paper_or_live_acceptance_allowed", 0))
    claim = as_int(metric_value(summary, "phase290_deployable_profitability_claim_allowed", 0))
    gates = [
        ("P291_PHASE290_SEARCH_COMPLETE", complete == 1, complete, "Phase290 search complete"),
        ("P291_PHASE290_NEXT_ACTION_PRESENT", "phase291" in next_action, next_action, "Phase290 routes to Phase291 interpretation"),
        ("P291_PHASE290_GATES_PASS", hard_rows > 0 and hard_pass == hard_rows, f"{hard_pass}/{hard_rows}", "Phase290 gates pass"),
        ("P291_RANKED_INTERPRETATION_PRESENT", len(ranked) > 0, len(ranked), ">0 ranked variants"),
        ("P291_CLOSES_PHASE290_FOR_ACCEPTANCE", str(decision_value(decisions, "close_phase290_adaptive_route_for_acceptance")) == "1", decision_value(decisions, "close_phase290_adaptive_route_for_acceptance"), "Phase290 closed for acceptance"),
        ("P291_NEXT_ROUTE_SELECTED", str(decision_value(decisions, "selected_next_route")) == SELECTED_NEXT_ROUTE, decision_value(decisions, "selected_next_route"), SELECTED_NEXT_ROUTE),
        ("P291_FULL_DEPTH_BOUNDARY_PRESERVED", l1_only == 0 and leakage == 0, f"l1_only={l1_only};live_mask={leakage}", "full-depth, no leakage"),
        ("P291_BOUNDARIES_CLOSED", replay == 0 and paper == 0 and claim == 0, f"replay={replay};paper={paper};claim={claim}", "no replay/paper/live/claim"),
        ("P291_ROUTE_CONTRACT_PRESENT", len(route) >= 8, len(route), "Phase292 route contract rows"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def write_report(output_dir: Path, summary: pd.DataFrame, ranked: pd.DataFrame, families: pd.DataFrame, interpretation: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase291 Adaptive Full-Depth Liquidity-Pressure Interpretation",
        "",
        "Phase291 interprets Phase290 as a high-annualized but too-sparse adaptive pressure spark and selects breadth repair as the next route.",
        "",
        "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened.",
        "",
        "## Phase290 Summary",
        "",
        _markdown_table(summary),
        "",
        "## Ranked Adaptive Interpretation",
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
        "## Phase292 Route Contract",
        "",
        _markdown_table(route),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase291_adaptive_full_depth_liquidity_pressure_interpretation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(phase290_dir: Path = DEFAULT_PHASE290_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase290_dir / "phase290_acceptance_summary.csv")
    scenarios = read_csv(phase290_dir / "phase290_adaptive_pressure_scenario_results.csv")
    ranked = build_ranked_adaptive_interpretation(scenarios)
    families = build_family_interpretation(ranked)
    interpretation = build_interpretation_ledger(summary, ranked)
    decisions = build_decision_ledger(summary, ranked, families)
    route = build_next_route_contract(families, ranked)
    gates = build_gate_evaluation(summary, ranked, decisions, route)

    ranked.to_csv(output_dir / "phase291_ranked_adaptive_pressure_interpretation.csv", index=False)
    families.to_csv(output_dir / "phase291_adaptive_pressure_family_interpretation.csv", index=False)
    interpretation.to_csv(output_dir / "phase291_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase291_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase291_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase291_gate_evaluation.csv", index=False)

    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    best = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    acceptance = pd.DataFrame(
        [
            ("phase291_interpretation_complete", 1, "Phase291 interpretation completed"),
            ("phase291_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
            ("phase291_phase290_variant_rows", as_int(metric_value(summary, "phase290_variant_rows", 0)), "Phase290 variants interpreted"),
            ("phase291_phase290_scenario_rows", as_int(metric_value(summary, "phase290_scenario_rows", 0)), "Phase290 scenarios interpreted"),
            ("phase291_phase290_sparse_above12_scenario_rows", as_int(metric_value(summary, "phase290_sparse_above12_scenario_rows", 0)), "Phase290 sparse above-12 rows"),
            ("phase291_phase290_robust_portfolio_floor_scenario_rows", as_int(metric_value(summary, "phase290_robust_portfolio_floor_scenario_rows", 0)), "Phase290 robust floor rows"),
            ("phase291_phase290_robust_portfolio_above12_scenario_rows", as_int(metric_value(summary, "phase290_robust_portfolio_above12_scenario_rows", 0)), "Phase290 robust above-12 rows"),
            ("phase291_best_phase290_variant_id", best.get("phase290_variant_id", ""), "Best interpreted Phase290 variant"),
            ("phase291_best_adaptive_family", best.get("adaptive_family", ""), "Best interpreted adaptive family"),
            ("phase291_best_primary_pressure_column", best.get("primary_pressure_column", ""), "Best interpreted primary pressure feature"),
            ("phase291_best_interaction_column", best.get("interaction_column", ""), "Best interpreted interaction feature"),
            ("phase291_best_side_mode", best.get("side_mode", ""), "Best interpreted side mode"),
            ("phase291_best_market_bucket", best.get("market_bucket", ""), "Best interpreted market bucket"),
            ("phase291_best_cost200_annualized_pct", best.get("max_annualized_pct", ""), "Best fixed-capital annualized diagnostic"),
            ("phase291_best_scheduled_event_rows", best.get("max_scheduled_event_rows", ""), "Best scheduled events"),
            ("phase291_above12_but_too_sparse_variant_rows", int(ranked["annualized_above12_but_too_sparse"].astype(int).sum()) if not ranked.empty else 0, "Above-12 but too-sparse variants"),
            ("phase291_close_phase290_for_acceptance", decision_value(decisions, "close_phase290_adaptive_route_for_acceptance"), "Close Phase290 route for acceptance"),
            ("phase291_do_not_relax_annualized_denominator", decision_value(decisions, "do_not_relax_annualized_denominator"), "Keep fixed-capital annualized denominator"),
            ("phase291_do_not_claim_portfolio_return", decision_value(decisions, "do_not_claim_portfolio_return"), "Do not claim portfolio return"),
            ("phase291_strategy_replay_allowed", 0, "No strategy replay unlocked"),
            ("phase291_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
            ("phase291_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
            ("phase291_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase291_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase291_hard_gate_rows", hard_rows, "Hard gates evaluated"),
            ("phase291_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    acceptance.to_csv(output_dir / "phase291_acceptance_summary.csv", index=False)
    write_report(output_dir, summary, ranked, families, interpretation, decisions, route, gates)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = reproducibility_fields(
        artifact_id="phase291",
        generated_utc=generated_utc,
        inputs={
            "phase290_acceptance_summary": str(phase290_dir / "phase290_acceptance_summary.csv"),
            "phase290_scenario_results": str(phase290_dir / "phase290_adaptive_pressure_scenario_results.csv"),
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
            "acceptance_summary": str(output_dir / "phase291_acceptance_summary.csv"),
            "next_route_contract": str(output_dir / "phase291_next_route_contract.csv"),
            "gate_evaluation": str(output_dir / "phase291_gate_evaluation.csv"),
        },
        cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        latency_model_version="phase291_interpretation_no_new_latency_model",
    )
    manifest.update(
        {
            "generated_utc": generated_utc,
            "phase290_dir": str(phase290_dir),
            "output_dir": str(output_dir),
            "selected_next_route": SELECTED_NEXT_ROUTE,
            "next_action": NEXT_ACTION,
            "hard_gate_pass_rows": hard_pass,
            "hard_gate_rows": hard_rows,
        }
    )
    (output_dir / "phase291_adaptive_full_depth_liquidity_pressure_interpretation_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase290-dir", type=Path, default=DEFAULT_PHASE290_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    print(json.dumps(run(args.phase290_dir, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

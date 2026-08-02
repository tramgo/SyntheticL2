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


DEFAULT_PHASE294_DIR = Path("outputs/phase294")
DEFAULT_OUTPUT_DIR = Path("outputs/phase295")

SELECTED_NEXT_ROUTE = "P296_FULL_YEAR_TOP5_DEPTH_STRATEGY_FAMILY_SWEEP"
NEXT_ACTION = "run_phase296_full_year_top5_depth_strategy_family_sweep_no_paper_live"
REPAIR_ACTION = "repair_phase295_full_depth_pressure_absorption_continuation_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
SPARSE_DIAGNOSTIC_EVENT_FLOOR = 8
ROBUST_PORTFOLIO_EVENT_FLOOR = 30


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    return out


def build_ranked_continuation_interpretation(scenarios: pd.DataFrame) -> pd.DataFrame:
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
            "notional_turnover_x_initial_capital",
            "avg_open_notional_utilization",
            "rejected_same_symbol_overlap_rows",
            "rejected_max_concurrent_rows",
        ],
    )
    rows: list[dict[str, Any]] = []
    for variant_id, group in frame.groupby("phase294_variant_id", dropna=False):
        best = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
        max_ann = safe_float(best.get("mechanical_one_date_annualized_portfolio_return_pct", 0.0), 0.0)
        max_events = int(group["scheduled_event_rows"].max())
        rows.append(
            {
                "phase294_variant_id": str(variant_id),
                "continuation_family": best.get("continuation_family", ""),
                "primary_pressure_column": best.get("primary_pressure_column", ""),
                "secondary_pressure_column": best.get("secondary_pressure_column", ""),
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
                "best_notional_turnover_x_initial_capital": best.get("notional_turnover_x_initial_capital", ""),
                "best_avg_open_notional_utilization": best.get("avg_open_notional_utilization", ""),
                "rejected_same_symbol_overlap_rows": int(group["rejected_same_symbol_overlap_rows"].max()),
                "rejected_max_concurrent_rows": int(group["rejected_max_concurrent_rows"].max()),
                "uses_top5": as_int(best.get("uses_top5", 0)),
                "uses_levels_2_to_5": as_int(best.get("uses_levels_2_to_5", 0)),
                "l1_only_variant": as_int(best.get("l1_only_variant", 0)),
                "uses_net_edge_as_live_mask": as_int(best.get("uses_net_edge_as_live_mask", 0)),
                "positive_but_below12": int(0.0 < max_ann < ANNUALIZED_THRESHOLD_PCT),
                "continuation_survivor": int(int(group["cost200_above12_sparse_diagnostic"].sum()) > 0),
                "robust_continuation_survivor": int(int(group["robust_portfolio_floor_above12"].sum()) > 0),
                "too_sparse_for_sparse_diagnostic": int(max_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR),
                "too_sparse_for_portfolio_claim": int(max_events < ROBUST_PORTFOLIO_EVENT_FLOOR),
                "current_event_universe_exhausted_for_acceptance": int(int(group["cost200_above12_sparse_diagnostic"].sum()) == 0),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["continuation_survivor", "robust_continuation_survivor", "max_annualized_pct", "max_scheduled_event_rows"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_family_interpretation(family_summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    if family_summary.empty:
        return pd.DataFrame()
    frame = numeric(
        family_summary,
        [
            "variant_rows",
            "scenario_rows",
            "max_scheduled_event_rows",
            "cost200_above12_sparse_diagnostic_rows",
            "robust_portfolio_floor_above12_rows",
            "sparse_floor_met_rows",
            "robust_portfolio_floor_met_rows",
            "median_annualized_pct",
            "max_annualized_pct",
            "max_net_pnl_inr",
        ],
    )
    frame["close_family_for_acceptance"] = (frame["cost200_above12_sparse_diagnostic_rows"].astype(int).eq(0)).astype(int)
    frame["preserve_for_full_year_sweep"] = (
        frame["continuation_family"].astype(str).isin(
            ranked.loc[ranked["positive_but_below12"].astype(int).eq(1), "continuation_family"].astype(str).unique().tolist()
        )
    ).astype(int) if not ranked.empty else 0
    return frame.sort_values(["close_family_for_acceptance", "max_annualized_pct"], ascending=[True, False], kind="mergesort").reset_index(drop=True)


def build_interpretation_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    scenarios = as_int(metric_value(summary, "phase294_scenario_rows", 0))
    sparse_above12 = as_int(metric_value(summary, "phase294_sparse_above12_scenario_rows", 0))
    robust_above12 = as_int(metric_value(summary, "phase294_robust_portfolio_above12_scenario_rows", 0))
    robust_floor = as_int(metric_value(summary, "phase294_robust_portfolio_floor_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase294_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase294_best_scheduled_event_rows", 0))
    l1_only = as_int(metric_value(summary, "phase294_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase294_net_edge_live_mask_rows", 0))
    positive_below12 = int(ranked["positive_but_below12"].astype(int).sum()) if not ranked.empty else 0
    return pd.DataFrame(
        [
            ("phase294_executed", f"scenario_rows={scenarios}", "evidence", int(scenarios > 0), "Phase294 executed the continuation/absorption search."),
            ("continuation_failed_above12", f"sparse_above12={sparse_above12};best_ann={best_ann}", "hard_negative", int(sparse_above12 == 0 and best_ann < ANNUALIZED_THRESHOLD_PCT), "No fixed-capital cost200 continuation scenario exceeded the sparse-discovery gate."),
            ("no_robust_portfolio_evidence", f"robust_floor={robust_floor};robust_above12={robust_above12};best_events={best_events}", "hard_negative", int(robust_floor == 0 and robust_above12 == 0), "No robust portfolio evidence exists."),
            ("full_depth_boundary_preserved", f"l1_only={l1_only};live_label_leakage={leakage}", "constraint", int(l1_only == 0 and leakage == 0), "Full-depth and no-live-leakage boundaries held."),
            ("positive_below12_not_enough", f"positive_below12_variants={positive_below12}", "research_clue", int(positive_below12 > 0), "Some variants are positive but below the required threshold and event floor."),
            ("phase277_event_universe_exhausted", "phase290_to_phase294_no_survivor", "decision", 1, "The curated Phase277 event universe should not be mined with more minor variants."),
            ("next_route_should_expand_universe", SELECTED_NEXT_ROUTE, "next_action", 1, "Move to full-year top-five depth family sweep rather than more Phase277 repairs."),
        ],
        columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"],
    )


def build_decision_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    best = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            ("close_phase294_for_acceptance", 1, f"best_ann={metric_value(summary, 'phase294_best_cost200_annualized_pct', '')};best_events={metric_value(summary, 'phase294_best_scheduled_event_rows', '')}", "Do not accept, replay, or promote Phase294."),
            ("close_phase277_event_universe_for_minor_repairs", 1, "Phase290-Phase294 no survivor", "Avoid additional minor threshold searches on the same curated event universe."),
            ("preserve_best_phase294_clue_for_full_year", best.get("phase294_variant_id", ""), f"family={best.get('continuation_family', '')};bucket={best.get('market_bucket', '')};side={best.get('side_mode', '')}", "Carry only as a full-year sweep clue, not as a strategy."),
            ("do_not_relax_annualized_denominator", 1, "fixed_initial_capital_required", "Annualized return remains fixed-capital based."),
            ("do_not_lower_cost_or_event_floor", 1, f"cost200_required;event_floor={SPARSE_DIAGNOSTIC_EVENT_FLOOR};portfolio_floor={ROBUST_PORTFOLIO_EVENT_FLOOR}", "Do not manufacture profitability by weakening rules."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "current event universe exhausted", "Move to full-year top-five depth family sweep."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def decision_value(decisions: pd.DataFrame, decision_id: str) -> str:
    rows = decisions.loc[decisions["decision_id"].astype(str).eq(decision_id), "decision_value"] if not decisions.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_next_route_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P296_INPUTS", "full_year_raw_or_compact_top5_l2_lake;outputs/phase294/phase294_continuation_family_summary.csv;outputs/phase149/phase149_branch_status_summary.csv", "Leave the small Phase277 event universe and use full-year top-five L2 evidence."),
            ("P296_SEARCH_TYPE", "full_year_top5_depth_strategy_family_sweep", "Run a broader family sweep on full-year L2-derived events/features."),
            ("P296_REQUIRED_L2_SCOPE", "top5_market_by_price_rows_1_to_5;levels_2_to_5_materiality_required;l1_only_forbidden", "Maintain the core project objective."),
            ("P296_STRATEGY_FAMILIES", "absorption_continuation;pressure_reversal;liquidity_vacuum;spread_compression;depth_replenishment;cross_symbol_pressure_if_available", "Broaden families on full-year data rather than tweaking Phase277 thresholds."),
            ("P296_COST_CAPITAL", "fixed_initial_capital;cost200_required;Zerodha_intraday_equity_formula;max_concurrent_scheduler", "No unlimited capital or simplified bps-only costs."),
            ("P296_DISCOVERY_GATE", f"annualized_pct_gt_{ANNUALIZED_THRESHOLD_PCT};scheduled_event_rows_ge_{SPARSE_DIAGNOSTIC_EVENT_FLOOR};multi_date_required", "Sparse discovery requires more than one-event sparks."),
            ("P296_PORTFOLIO_GATE", f"scheduled_event_rows_ge_{ROBUST_PORTFOLIO_EVENT_FLOOR};multi_symbol_and_multi_regime_required", "Portfolio/profitability claims require robust breadth."),
            ("P296_BOUNDARY", "no_paper_live;no_strategy_replay;no_deployable_profitability_claim;net_edge_live_mask_forbidden", "Synthetic-only search; acceptance remains closed until earned."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_gate_evaluation(summary: pd.DataFrame, ranked: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase294_continuation_search_complete", 0))
    next_action = str(metric_value(summary, "phase294_next_best_action", ""))
    hard_pass = as_int(metric_value(summary, "phase294_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(summary, "phase294_hard_gate_rows", 0))
    sparse_above12 = as_int(metric_value(summary, "phase294_sparse_above12_scenario_rows", 0))
    robust_above12 = as_int(metric_value(summary, "phase294_robust_portfolio_above12_scenario_rows", 0))
    l1_only = as_int(metric_value(summary, "phase294_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase294_net_edge_live_mask_rows", 0))
    replay = as_int(metric_value(summary, "phase294_strategy_replay_allowed", 0))
    paper = as_int(metric_value(summary, "phase294_paper_or_live_acceptance_allowed", 0))
    claim = as_int(metric_value(summary, "phase294_deployable_profitability_claim_allowed", 0))
    gates = [
        ("P295_PHASE294_SEARCH_COMPLETE", complete == 1, complete, "Phase294 search complete"),
        ("P295_PHASE294_NEXT_ACTION_PRESENT", "phase295" in next_action, next_action, "Phase294 routes to Phase295 interpretation"),
        ("P295_PHASE294_GATES_PASS", hard_rows > 0 and hard_pass == hard_rows, f"{hard_pass}/{hard_rows}", "Phase294 gates pass"),
        ("P295_RANKED_INTERPRETATION_PRESENT", len(ranked) > 0, len(ranked), ">0 ranked variants"),
        ("P295_CLOSES_PHASE294_FOR_ACCEPTANCE", str(decision_value(decisions, "close_phase294_for_acceptance")) == "1", decision_value(decisions, "close_phase294_for_acceptance"), "Phase294 closed for acceptance"),
        ("P295_NO_SURVIVOR_TO_PROMOTE", sparse_above12 == 0 and robust_above12 == 0, f"sparse_above12={sparse_above12};robust_above12={robust_above12}", "no Phase294 survivor"),
        ("P295_NEXT_ROUTE_SELECTED", str(decision_value(decisions, "selected_next_route")) == SELECTED_NEXT_ROUTE, decision_value(decisions, "selected_next_route"), SELECTED_NEXT_ROUTE),
        ("P295_FULL_DEPTH_BOUNDARY_PRESERVED", l1_only == 0 and leakage == 0, f"l1_only={l1_only};live_mask={leakage}", "full-depth, no leakage"),
        ("P295_BOUNDARIES_CLOSED", replay == 0 and paper == 0 and claim == 0, f"replay={replay};paper={paper};claim={claim}", "no replay/paper/live/claim"),
        ("P295_ROUTE_CONTRACT_PRESENT", len(route) >= 8, len(route), "Phase296 route contract rows"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def write_report(output_dir: Path, summary: pd.DataFrame, ranked: pd.DataFrame, families: pd.DataFrame, interpretation: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase295 Full-Depth Pressure Absorption / Continuation Interpretation",
        "",
        "Phase295 interprets Phase294 as a clean negative continuation result on the current Phase277 event universe.",
        "",
        "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened.",
        "",
        "The selected next route leaves the small curated event universe and moves to a full-year top-five depth family sweep.",
        "",
        "## Phase294 Summary",
        "",
        _markdown_table(summary),
        "",
        "## Ranked Continuation Interpretation",
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
        "## Phase296 Route Contract",
        "",
        _markdown_table(route),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase295_full_depth_pressure_absorption_continuation_interpretation_report.md").write_text("\n".join(lines), encoding="utf-8")


def run(phase294_dir: Path = DEFAULT_PHASE294_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase294_dir / "phase294_acceptance_summary.csv")
    scenarios = read_csv(phase294_dir / "phase294_continuation_scenario_results.csv")
    family_summary = read_csv(phase294_dir / "phase294_continuation_family_summary.csv")
    ranked = build_ranked_continuation_interpretation(scenarios)
    families = build_family_interpretation(family_summary, ranked)
    interpretation = build_interpretation_ledger(summary, ranked)
    decisions = build_decision_ledger(summary, ranked)
    route = build_next_route_contract()
    gates = build_gate_evaluation(summary, ranked, decisions, route)

    ranked.to_csv(output_dir / "phase295_ranked_continuation_interpretation.csv", index=False)
    families.to_csv(output_dir / "phase295_continuation_family_interpretation.csv", index=False)
    interpretation.to_csv(output_dir / "phase295_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase295_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase295_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase295_gate_evaluation.csv", index=False)

    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    best = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    acceptance = pd.DataFrame(
        [
            ("phase295_interpretation_complete", 1, "Phase295 interpretation completed"),
            ("phase295_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
            ("phase295_phase294_variant_rows", as_int(metric_value(summary, "phase294_variant_rows", 0)), "Phase294 variants interpreted"),
            ("phase295_phase294_scenario_rows", as_int(metric_value(summary, "phase294_scenario_rows", 0)), "Phase294 scenarios interpreted"),
            ("phase295_phase294_family_rows", as_int(metric_value(summary, "phase294_family_rows", 0)), "Phase294 families interpreted"),
            ("phase295_phase294_sparse_above12_scenario_rows", as_int(metric_value(summary, "phase294_sparse_above12_scenario_rows", 0)), "Phase294 sparse above-12 rows"),
            ("phase295_phase294_robust_portfolio_floor_scenario_rows", as_int(metric_value(summary, "phase294_robust_portfolio_floor_scenario_rows", 0)), "Phase294 robust floor rows"),
            ("phase295_phase294_robust_portfolio_above12_scenario_rows", as_int(metric_value(summary, "phase294_robust_portfolio_above12_scenario_rows", 0)), "Phase294 robust above-12 rows"),
            ("phase295_best_phase294_variant_id", best.get("phase294_variant_id", ""), "Best interpreted Phase294 variant"),
            ("phase295_best_continuation_family", best.get("continuation_family", ""), "Best interpreted continuation family"),
            ("phase295_best_side_mode", best.get("side_mode", ""), "Best interpreted side mode"),
            ("phase295_best_market_bucket", best.get("market_bucket", ""), "Best interpreted market bucket"),
            ("phase295_best_cost200_annualized_pct", best.get("max_annualized_pct", ""), "Best fixed-capital annualized diagnostic"),
            ("phase295_best_scheduled_event_rows", best.get("max_scheduled_event_rows", ""), "Best scheduled events"),
            ("phase295_positive_but_below12_variant_rows", int(ranked["positive_but_below12"].astype(int).sum()) if not ranked.empty else 0, "Positive but below-12 variants"),
            ("phase295_close_phase294_for_acceptance", decision_value(decisions, "close_phase294_for_acceptance"), "Close Phase294 route for acceptance"),
            ("phase295_close_phase277_event_universe_for_minor_repairs", decision_value(decisions, "close_phase277_event_universe_for_minor_repairs"), "Close current event universe for minor repairs"),
            ("phase295_do_not_relax_annualized_denominator", decision_value(decisions, "do_not_relax_annualized_denominator"), "Keep fixed-capital annualized denominator"),
            ("phase295_do_not_lower_cost_or_event_floor", decision_value(decisions, "do_not_lower_cost_or_event_floor"), "Keep cost/event floors"),
            ("phase295_strategy_replay_allowed", 0, "No strategy replay unlocked"),
            ("phase295_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
            ("phase295_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
            ("phase295_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase295_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase295_hard_gate_rows", hard_rows, "Hard gates evaluated"),
            ("phase295_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    acceptance.to_csv(output_dir / "phase295_acceptance_summary.csv", index=False)
    write_report(output_dir, summary, ranked, families, interpretation, decisions, route, gates)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = reproducibility_fields(
        artifact_id="phase295",
        generated_utc=generated_utc,
        inputs={
            "phase294_acceptance_summary": str(phase294_dir / "phase294_acceptance_summary.csv"),
            "phase294_scenario_results": str(phase294_dir / "phase294_continuation_scenario_results.csv"),
            "phase294_family_summary": str(phase294_dir / "phase294_continuation_family_summary.csv"),
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
            "acceptance_summary": str(output_dir / "phase295_acceptance_summary.csv"),
            "next_route_contract": str(output_dir / "phase295_next_route_contract.csv"),
            "gate_evaluation": str(output_dir / "phase295_gate_evaluation.csv"),
        },
        cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        latency_model_version="phase295_interpretation_no_new_latency_model",
    )
    manifest.update(
        {
            "generated_utc": generated_utc,
            "phase294_dir": str(phase294_dir),
            "output_dir": str(output_dir),
            "selected_next_route": SELECTED_NEXT_ROUTE,
            "next_action": NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION,
            "hard_gate_pass_rows": hard_pass,
            "hard_gate_rows": hard_rows,
        }
    )
    (output_dir / "phase295_full_depth_pressure_absorption_continuation_interpretation_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase294-dir", type=Path, default=DEFAULT_PHASE294_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    print(json.dumps(run(args.phase294_dir, args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

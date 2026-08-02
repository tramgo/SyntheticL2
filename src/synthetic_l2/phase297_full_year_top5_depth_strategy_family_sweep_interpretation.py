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


DEFAULT_PHASE296_DIR = Path("outputs/phase296")
DEFAULT_OUTPUT_DIR = Path("outputs/phase297")

SELECTED_NEXT_ROUTE = "P298_RAW_DENSE_TOP5_BOOK_STATE_STRATEGY_SWEEP"
NEXT_ACTION = "run_phase298_raw_dense_top5_book_state_strategy_sweep_no_paper_live"
REPAIR_ACTION = "repair_phase297_full_year_top5_depth_strategy_family_sweep_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
SPARSE_DIAGNOSTIC_EVENT_FLOOR = 8
ROBUST_PORTFOLIO_EVENT_FLOOR = 30


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    return out


def build_ranked_variant_interpretation(variants: pd.DataFrame) -> pd.DataFrame:
    if variants.empty:
        return pd.DataFrame()
    frame = numeric(
        variants,
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
            "best_scheduled_event_rows",
        ],
    )
    frame["above12_sparse_survivor"] = frame["cost200_above12_sparse_diagnostic_rows"].astype(int).gt(0).astype(int)
    frame["robust_portfolio_survivor"] = frame["robust_portfolio_floor_above12_rows"].astype(int).gt(0).astype(int)
    frame["positive_but_below12"] = frame["max_annualized_pct"].between(0.0, ANNUALIZED_THRESHOLD_PCT, inclusive="neither").astype(int)
    frame["too_sparse_for_sparse_diagnostic"] = frame["max_scheduled_event_rows"].lt(SPARSE_DIAGNOSTIC_EVENT_FLOOR).astype(int)
    frame["too_sparse_for_portfolio_claim"] = frame["max_scheduled_event_rows"].lt(ROBUST_PORTFOLIO_EVENT_FLOOR).astype(int)
    frame["preserve_as_raw_book_state_clue"] = (
        frame["positive_but_below12"].astype(int).eq(1)
        & frame["max_annualized_pct"].ge(0.25)
    ).astype(int)
    frame["current_proxy_sweep_acceptance_closed"] = (
        frame["above12_sparse_survivor"].astype(int).eq(0)
        & frame["robust_portfolio_survivor"].astype(int).eq(0)
    ).astype(int)
    return frame.sort_values(
        ["above12_sparse_survivor", "robust_portfolio_survivor", "preserve_as_raw_book_state_clue", "max_annualized_pct", "max_scheduled_event_rows"],
        ascending=[False, False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_family_interpretation(families: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    if families.empty:
        return pd.DataFrame()
    frame = numeric(
        families,
        [
            "scenario_rows",
            "variant_rows",
            "max_scheduled_event_rows",
            "cost200_above12_sparse_diagnostic_rows",
            "robust_portfolio_floor_above12_rows",
            "sparse_floor_met_rows",
            "robust_portfolio_floor_met_rows",
            "min_annualized_pct",
            "median_annualized_pct",
            "max_annualized_pct",
            "max_net_pnl_inr",
        ],
    )
    clue_families = set(ranked.loc[ranked["preserve_as_raw_book_state_clue"].astype(int).eq(1), "strategy_family"].astype(str)) if not ranked.empty else set()
    frame["close_proxy_family_for_acceptance"] = frame["cost200_above12_sparse_diagnostic_rows"].astype(int).eq(0).astype(int)
    frame["preserve_family_for_raw_book_state_sweep"] = frame["strategy_family"].astype(str).isin(clue_families).astype(int)
    return frame.sort_values(
        ["preserve_family_for_raw_book_state_sweep", "max_annualized_pct"],
        ascending=[False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_interpretation_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    scenarios = as_int(metric_value(summary, "phase296_scenario_rows", 0))
    sparse_above12 = as_int(metric_value(summary, "phase296_sparse_above12_scenario_rows", 0))
    robust_above12 = as_int(metric_value(summary, "phase296_robust_portfolio_above12_scenario_rows", 0))
    robust_floor = as_int(metric_value(summary, "phase296_robust_portfolio_floor_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase296_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase296_best_scheduled_event_rows", 0))
    l1_only = as_int(metric_value(summary, "phase296_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase296_net_edge_live_mask_rows", 0))
    preserved_clues = int(ranked["preserve_as_raw_book_state_clue"].astype(int).sum()) if not ranked.empty else 0
    return pd.DataFrame(
        [
            ("phase296_executed", f"scenario_rows={scenarios}", "evidence", int(scenarios > 0), "Phase296 executed the full-year top-five-depth proxy sweep."),
            ("phase296_failed_above12", f"sparse_above12={sparse_above12};best_ann={best_ann}", "hard_negative", int(sparse_above12 == 0 and best_ann < ANNUALIZED_THRESHOLD_PCT), "No fixed-capital cost200 scenario exceeded the 12% sparse-discovery threshold."),
            ("phase296_no_robust_portfolio_evidence", f"robust_floor={robust_floor};robust_above12={robust_above12};best_events={best_events}", "hard_negative", int(robust_floor == 0 and robust_above12 == 0), "No robust portfolio evidence exists."),
            ("phase296_too_sparse_best_case", f"best_scheduled_events={best_events}", "constraint", int(best_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR), "The best result is also too sparse for the sparse diagnostic event floor."),
            ("fixed_capital_boundary_preserved", str(metric_value(summary, "phase296_annualized_denominator", "")), "constraint", int(str(metric_value(summary, "phase296_annualized_denominator", "")) == "fixed_initial_capital"), "No unlimited-capital annualization."),
            ("full_depth_proxy_boundary_preserved", f"l1_only={l1_only};live_label_leakage={leakage}", "constraint", int(l1_only == 0 and leakage == 0), "Top-five/depth-beyond-L1 proxy and no live leakage boundaries held."),
            ("proxy_input_limit_identified", "Phase42 lacks raw L1-L5 persisted book state columns", "design_gap", 1, "The next search should use raw dense top-five book-state artifacts, not more Phase42 proxy variants."),
            ("raw_book_state_clues_preserved", f"clue_variants={preserved_clues}", "research_clue", int(preserved_clues > 0), "Positive-but-below-threshold pockets can seed raw-book-state work without opening acceptance."),
            ("next_route_should_use_raw_book_state", SELECTED_NEXT_ROUTE, "next_action", 1, "Move from proxy features to raw dense top-five book-state strategy sweep."),
        ],
        columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"],
    )


def build_decision_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    best = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            ("close_phase296_for_acceptance", 1, f"best_ann={metric_value(summary, 'phase296_best_cost200_annualized_pct', '')};sparse_above12={metric_value(summary, 'phase296_sparse_above12_scenario_rows', '')}", "Do not accept, replay, or promote Phase296."),
            ("close_phase42_proxy_sweep_for_direct_acceptance", 1, "full_year_proxy_sweep_no_survivor", "Avoid more minor proxy-only grid tweaks as the next action."),
            ("preserve_best_phase296_clue_for_raw_book_state", best.get("phase296_variant_id", ""), f"family={best.get('strategy_family', '')};feed={best.get('feed_profile', '')};max_ann={best.get('max_annualized_pct', '')}", "Carry only as a raw-book-state clue, not as a strategy."),
            ("do_not_claim_portfolio_return", 1, "no_above12;no_robust_floor;best_events_below_floor", "No deployable or robust annual return claim."),
            ("do_not_relax_annualized_denominator", 1, "fixed_initial_capital_required", "Annualized return remains fixed-capital based."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "Phase42 proxy input limit plus no survivor", "Move to raw dense top-five book-state strategy sweep."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def decision_value(decisions: pd.DataFrame, decision_id: str) -> str:
    rows = decisions.loc[decisions["decision_id"].astype(str).eq(decision_id), "decision_value"] if not decisions.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_next_route_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P298_INPUTS", "raw_synthetic_l2_dense_full_year;raw_l2_like_partitions;date_exchange_symbol_top5_book_state", "Use the raw dense top-five book-state lake or raw-lake partitions, not only Phase42 proxy features."),
            ("P298_REQUIRED_BOOK_SCOPE", "bid_price_1_to_5;ask_price_1_to_5;bid_qty_1_to_5;ask_qty_1_to_5;order_count_1_to_5_if_available", "Persisted market-by-price levels 1-5 are required."),
            ("P298_TERMINOLOGY", "Zerodha_top_five_market_by_price_depth_levels_1_to_5_not_universal_market_data_L1_to_L5", "Use correct terminology for book levels."),
            ("P298_STRATEGY_SEEDS", "top5_pressure_continuation;microprice_depth_reversal;beyond_l1_absorption;spread_compressed_mlofi", "Seed from Phase296 clues but recompute from raw levels."),
            ("P298_FEATURES", "level_weighted_imbalance;depth_beyond_l1;queue_size_slope;spread_ticks;microprice_l1_to_l5;book_churn;level_replenishment", "Exploit raw book levels rather than proxy-only l5 imbalance."),
            ("P298_COST_CAPITAL", "fixed_initial_capital;cost200_required;Zerodha_intraday_equity_formula;max_concurrent_scheduler", "No unlimited capital or simplified bps-only costs."),
            ("P298_DISCOVERY_GATE", f"annualized_pct_gt_{ANNUALIZED_THRESHOLD_PCT};scheduled_event_rows_ge_{SPARSE_DIAGNOSTIC_EVENT_FLOOR};multi_date_required", "Sparse discovery remains a clue only."),
            ("P298_PORTFOLIO_GATE", f"scheduled_event_rows_ge_{ROBUST_PORTFOLIO_EVENT_FLOOR};multi_symbol_and_multi_regime_required", "Portfolio/profitability claims require robust breadth."),
            ("P298_BOUNDARY", "no_paper_live;no_strategy_replay;no_deployable_profitability_claim;net_edge_live_mask_forbidden", "Synthetic-only search; no acceptance until earned."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def build_gate_evaluation(summary: pd.DataFrame, ranked: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase296_full_year_sweep_complete", 0))
    next_action = str(metric_value(summary, "phase296_next_best_action", ""))
    hard_pass = as_int(metric_value(summary, "phase296_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(summary, "phase296_hard_gate_rows", 0))
    sparse_above12 = as_int(metric_value(summary, "phase296_sparse_above12_scenario_rows", 0))
    robust_above12 = as_int(metric_value(summary, "phase296_robust_portfolio_above12_scenario_rows", 0))
    best_events = as_int(metric_value(summary, "phase296_best_scheduled_event_rows", 0))
    l1_only = as_int(metric_value(summary, "phase296_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase296_net_edge_live_mask_rows", 0))
    replay = as_int(metric_value(summary, "phase296_strategy_replay_allowed", 0))
    paper = as_int(metric_value(summary, "phase296_paper_or_live_acceptance_allowed", 0))
    claim = as_int(metric_value(summary, "phase296_deployable_profitability_claim_allowed", 0))
    gates = [
        ("P297_PHASE296_SWEEP_COMPLETE", complete == 1, complete, "Phase296 sweep complete"),
        ("P297_PHASE296_NEXT_ACTION_PRESENT", "phase297" in next_action, next_action, "Phase296 routes to Phase297 interpretation"),
        ("P297_PHASE296_GATES_PASS", hard_rows > 0 and hard_pass == hard_rows, f"{hard_pass}/{hard_rows}", "Phase296 hard gates pass"),
        ("P297_RANKED_INTERPRETATION_PRESENT", len(ranked) > 0, len(ranked), ">0 ranked variants"),
        ("P297_CLOSES_PHASE296_FOR_ACCEPTANCE", str(decision_value(decisions, "close_phase296_for_acceptance")) == "1", decision_value(decisions, "close_phase296_for_acceptance"), "Phase296 closed for acceptance"),
        ("P297_NO_SURVIVOR_TO_PROMOTE", sparse_above12 == 0 and robust_above12 == 0, f"sparse_above12={sparse_above12};robust_above12={robust_above12}", "no Phase296 survivor"),
        ("P297_BEST_TOO_SPARSE", best_events < SPARSE_DIAGNOSTIC_EVENT_FLOOR, best_events, f"<{SPARSE_DIAGNOSTIC_EVENT_FLOOR}"),
        ("P297_FIXED_CAPITAL_DENOMINATOR", str(metric_value(summary, "phase296_annualized_denominator", "")) == "fixed_initial_capital", metric_value(summary, "phase296_annualized_denominator", ""), "fixed_initial_capital"),
        ("P297_FULL_DEPTH_PROXY_BOUNDARY", l1_only == 0 and leakage == 0, f"l1_only={l1_only};live_mask={leakage}", "top-five proxy, no leakage"),
        ("P297_NEXT_ROUTE_SELECTED", str(decision_value(decisions, "selected_next_route")) == SELECTED_NEXT_ROUTE, decision_value(decisions, "selected_next_route"), SELECTED_NEXT_ROUTE),
        ("P297_BOUNDARIES_CLOSED", replay == 0 and paper == 0 and claim == 0, f"replay={replay};paper={paper};claim={claim}", "no replay/paper/live/claim"),
        ("P297_ROUTE_CONTRACT_PRESENT", len(route) >= 9, len(route), "Phase298 route contract rows"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(summary: pd.DataFrame, ranked: pd.DataFrame, families: pd.DataFrame, decisions: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    best = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase297_interpretation_complete", 1, "Phase297 interpretation completed"),
            ("phase297_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
            ("phase297_phase296_input_rows", metric_value(summary, "phase296_input_rows", 0), "Phase296 input rows interpreted"),
            ("phase297_phase296_variant_rows", metric_value(summary, "phase296_variant_rows", 0), "Phase296 variants interpreted"),
            ("phase297_phase296_scenario_rows", metric_value(summary, "phase296_scenario_rows", 0), "Phase296 scenarios interpreted"),
            ("phase297_phase296_sparse_above12_scenario_rows", metric_value(summary, "phase296_sparse_above12_scenario_rows", 0), "Phase296 sparse above-12 rows"),
            ("phase297_phase296_robust_portfolio_floor_scenario_rows", metric_value(summary, "phase296_robust_portfolio_floor_scenario_rows", 0), "Phase296 robust floor rows"),
            ("phase297_phase296_robust_portfolio_above12_scenario_rows", metric_value(summary, "phase296_robust_portfolio_above12_scenario_rows", 0), "Phase296 robust above-12 rows"),
            ("phase297_best_phase296_variant_id", best.get("phase296_variant_id", ""), "Best interpreted Phase296 variant"),
            ("phase297_best_strategy_family", best.get("strategy_family", ""), "Best interpreted family"),
            ("phase297_best_feed_profile", best.get("feed_profile", ""), "Best interpreted feed profile"),
            ("phase297_best_cost200_annualized_pct", best.get("max_annualized_pct", ""), "Best fixed-capital annualized diagnostic"),
            ("phase297_best_scheduled_event_rows", best.get("max_scheduled_event_rows", ""), "Best scheduled events"),
            ("phase297_positive_but_below12_variant_rows", int(ranked["positive_but_below12"].astype(int).sum()) if not ranked.empty else 0, "Positive but below-12 variants"),
            ("phase297_raw_book_state_clue_variant_rows", int(ranked["preserve_as_raw_book_state_clue"].astype(int).sum()) if not ranked.empty else 0, "Variants preserved as raw-book-state clues"),
            ("phase297_family_rows", len(families), "Families interpreted"),
            ("phase297_close_phase296_for_acceptance", decision_value(decisions, "close_phase296_for_acceptance"), "Close Phase296 for acceptance"),
            ("phase297_close_phase42_proxy_sweep_for_direct_acceptance", decision_value(decisions, "close_phase42_proxy_sweep_for_direct_acceptance"), "Close proxy-only sweep for direct acceptance"),
            ("phase297_do_not_claim_portfolio_return", decision_value(decisions, "do_not_claim_portfolio_return"), "Do not claim portfolio return"),
            ("phase297_do_not_relax_annualized_denominator", decision_value(decisions, "do_not_relax_annualized_denominator"), "Keep fixed initial-capital denominator"),
            ("phase297_strategy_replay_allowed", 0, "No replay"),
            ("phase297_strategy_promotion_allowed", 0, "No promotion"),
            ("phase297_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase297_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase297_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase297_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase297_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, summary: pd.DataFrame, ranked: pd.DataFrame, families: pd.DataFrame, interpretation: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase297 Full-Year Top-Five-Depth Strategy-Family Sweep Interpretation",
        "",
        "Phase297 interprets Phase296 as a clean negative result for the Phase42 full-year top-five-depth proxy sweep.",
        "",
        "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened.",
        "",
        "The selected next route moves from proxy features to raw dense top-five market-by-price book-state strategy work.",
        "",
        "## Phase296 Summary",
        "",
        _markdown_table(summary),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "## Interpretation Ledger",
        "",
        _markdown_table(interpretation),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decisions),
        "",
        "## Next Route Contract",
        "",
        _markdown_table(route),
        "",
        "## Family Interpretation",
        "",
        _markdown_table(families),
        "",
        "## Top Ranked Variants",
        "",
        _markdown_table(ranked.head(20)),
    ]
    (output_dir / "phase297_full_year_top5_depth_strategy_family_sweep_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase296_dir: Path = DEFAULT_PHASE296_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary = read_csv(phase296_dir / "phase296_acceptance_summary.csv")
    variants = read_csv(phase296_dir / "phase296_variant_summary.csv")
    family_summary = read_csv(phase296_dir / "phase296_family_summary.csv")
    if summary.empty or variants.empty or family_summary.empty:
        raise FileNotFoundError(f"Phase296 outputs are incomplete under {phase296_dir}")
    ranked = build_ranked_variant_interpretation(variants)
    families = build_family_interpretation(family_summary, ranked)
    interpretation = build_interpretation_ledger(summary, ranked)
    decisions = build_decision_ledger(summary, ranked)
    route = build_next_route_contract()
    gates = build_gate_evaluation(summary, ranked, decisions, route)
    acceptance = build_acceptance(summary, ranked, families, decisions, gates)

    ranked.to_csv(output_dir / "phase297_ranked_variant_interpretation.csv", index=False)
    families.to_csv(output_dir / "phase297_family_interpretation.csv", index=False)
    interpretation.to_csv(output_dir / "phase297_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase297_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase297_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase297_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase297_acceptance_summary.csv", index=False)
    write_report(output_dir, summary, ranked, families, interpretation, decisions, route, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase297_full_year_top5_depth_strategy_family_sweep_interpretation",
        **reproducibility_fields(
            artifact_id="phase297",
            generated_utc=generated_utc,
            inputs={
                "phase296_acceptance_summary": str(phase296_dir / "phase296_acceptance_summary.csv"),
                "phase296_variant_summary": str(phase296_dir / "phase296_variant_summary.csv"),
                "phase296_family_summary": str(phase296_dir / "phase296_family_summary.csv"),
            },
            parameters={
                "selected_next_route": SELECTED_NEXT_ROUTE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "sparse_diagnostic_event_floor": SPARSE_DIAGNOSTIC_EVENT_FLOOR,
                "robust_portfolio_event_floor": ROBUST_PORTFOLIO_EVENT_FLOOR,
                "next_route_input_scope": "raw_dense_top5_book_state",
            },
            outputs={"acceptance_summary": str(output_dir / "phase297_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase297_interpretation_only",
        ),
    }
    (output_dir / "phase297_full_year_top5_depth_strategy_family_sweep_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase297 full-year top-five-depth sweep interpretation.")
    parser.add_argument("--phase296-dir", type=Path, default=DEFAULT_PHASE296_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(phase296_dir=args.phase296_dir, output_dir=args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

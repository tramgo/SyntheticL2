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


DEFAULT_PHASE298_DIR = Path("outputs/phase298")
DEFAULT_OUTPUT_DIR = Path("outputs/phase299")

SELECTED_NEXT_ROUTE = "P300_PASSIVE_AWARE_DIRECTIONAL_L2_EXECUTION_PRECOMMIT"
NEXT_ACTION = "run_phase300_passive_aware_execution_hybrid_precommit_no_paper_live"
REPAIR_ACTION = "repair_phase299_raw_dense_top5_book_state_strategy_sweep_interpretation"

ANNUALIZED_THRESHOLD_PCT = 12.0
SPARSE_CLUE_EVENT_FLOOR = 30
ROBUST_PORTFOLIO_EVENT_FLOOR = 30


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)
    return out


def build_ranked_interpretation(variants: pd.DataFrame) -> pd.DataFrame:
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
        ],
    )
    frame["above12_but_below_phase300_floor"] = (
        frame["max_annualized_pct"].gt(ANNUALIZED_THRESHOLD_PCT)
        & frame["max_scheduled_event_rows"].lt(SPARSE_CLUE_EVENT_FLOOR)
    ).astype(int)
    frame["phase298_acceptance_survivor"] = (
        frame["cost200_above12_sparse_diagnostic_rows"].astype(int).gt(0)
        | frame["robust_portfolio_floor_above12_rows"].astype(int).gt(0)
    ).astype(int)
    frame["preserve_as_directional_signal_seed"] = (
        frame["above12_but_below_phase300_floor"].astype(int).eq(1)
        | (
            frame["max_annualized_pct"].gt(0.0)
            & frame["max_scheduled_event_rows"].ge(3)
            & frame["strategy_family"].astype(str).str.contains("MICROPRICE|ABSORPTION|PRESSURE", regex=True)
        )
    ).astype(int)
    frame["close_for_direct_acceptance"] = frame["phase298_acceptance_survivor"].astype(int).eq(0).astype(int)
    return frame.sort_values(
        [
            "phase298_acceptance_survivor",
            "preserve_as_directional_signal_seed",
            "max_annualized_pct",
            "max_scheduled_event_rows",
        ],
        ascending=[False, False, False, False],
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
            "min_annualized_pct",
            "median_annualized_pct",
            "max_annualized_pct",
            "max_net_pnl_inr",
        ],
    )
    seed_families = set(ranked.loc[ranked["preserve_as_directional_signal_seed"].astype(int).eq(1), "strategy_family"].astype(str)) if not ranked.empty else set()
    frame["close_for_direct_acceptance"] = (
        frame["cost200_above12_sparse_diagnostic_rows"].astype(int).eq(0)
        & frame["robust_portfolio_floor_above12_rows"].astype(int).eq(0)
    ).astype(int)
    frame["preserve_for_passive_aware_execution"] = frame["strategy_family"].astype(str).isin(seed_families).astype(int)
    return frame.sort_values(
        ["preserve_for_passive_aware_execution", "max_annualized_pct"],
        ascending=[False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_interpretation_ledger(summary: pd.DataFrame, ranked: pd.DataFrame) -> pd.DataFrame:
    scenarios = as_int(metric_value(summary, "phase298_scenario_rows", 0))
    sparse_above12 = as_int(metric_value(summary, "phase298_sparse_above12_scenario_rows", 0))
    robust_above12 = as_int(metric_value(summary, "phase298_robust_portfolio_above12_scenario_rows", 0))
    best_ann = safe_float(metric_value(summary, "phase298_best_cost200_annualized_pct", 0.0), 0.0)
    best_events = as_int(metric_value(summary, "phase298_best_scheduled_event_rows", 0))
    best_dates = as_int(metric_value(summary, "phase298_best_observed_trade_dates", 0))
    seed_rows = int(ranked["preserve_as_directional_signal_seed"].astype(int).sum()) if not ranked.empty else 0
    above12_below_floor = int(ranked["above12_but_below_phase300_floor"].astype(int).sum()) if not ranked.empty else 0
    return pd.DataFrame(
        [
            ("phase298_executed", f"scenario_rows={scenarios}", "evidence", int(scenarios > 0), "Phase298 executed on raw dense top-five book-state artifacts."),
            ("phase298_no_direct_acceptance_survivor", f"sparse_above12={sparse_above12};robust_above12={robust_above12}", "hard_negative", int(sparse_above12 == 0 and robust_above12 == 0), "No direct Phase298 survivor is accepted or promoted."),
            ("phase298_best_is_sparse_spark", f"best_ann={best_ann};best_events={best_events};best_dates={best_dates}", "research_clue", int(best_ann > ANNUALIZED_THRESHOLD_PCT and best_events < SPARSE_CLUE_EVENT_FLOOR), "The best result is a sparse fixed-capital annualized spark, not a strategy."),
            ("above12_below_floor_variants_preserved", f"rows={above12_below_floor}", "research_clue", int(above12_below_floor > 0), "High annualized pockets below the 30-event floor are preserved only as directional-signal seeds."),
            ("directional_signal_seeds_preserved", f"rows={seed_rows}", "next_input", int(seed_rows > 0), "Reuse existing directional signals; do not run a fresh alpha search in Phase300."),
            ("raw_depth_scope_preserved", "bid/ask price, quantity, order-count depth levels 1-5", "constraint", 1, "Phase300 must continue using top-five market-by-price depth levels, including levels 2-5."),
            ("taker_cost_problem_identified", "prior candidates crossed spread on entry/exit", "design_gap", 1, "The next lever is passive-aware execution, not more taker-only threshold mining."),
            ("next_route_selected", SELECTED_NEXT_ROUTE, "next_action", 1, "Route to Phase300 passive-aware execution precommit before generating results."),
        ],
        columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"],
    )


def build_decision_ledger(ranked: pd.DataFrame) -> pd.DataFrame:
    best = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            ("close_phase298_for_direct_acceptance", 1, "no_sparse_or_robust_acceptance_rows", "No replay, promotion, paper/live, or profitability claim is opened."),
            ("preserve_best_sparse_spark_as_seed", best.get("phase298_variant_id", ""), f"family={best.get('strategy_family', '')};ann={best.get('max_annualized_pct', '')};events={best.get('max_scheduled_event_rows', '')}", "Use only as a directional signal seed."),
            ("do_not_add_new_alpha_search_in_phase300", 1, "charter_requires_reuse_validated_directional_signals", "Phase300 tests execution realism, not a new signal grid."),
            ("require_passive_fill_model", 1, "passive_fill_probability_from_queue_depth_required", "No assumed passive fills."),
            ("require_adverse_selection_penalty", 1, "fill_conditioned_toxicity_penalty_required", "Filled passive orders must pay adverse-selection penalty."),
            ("require_forced_flatten_cost", 1, "inventory_leftover_pays_taker_flatten", "No free spread saving by refusing to exit."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "only remaining retail cost-side lever", "Freeze Phase300 passive-aware execution charter before results."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def decision_value(decisions: pd.DataFrame, decision_id: str) -> str:
    rows = decisions.loc[decisions["decision_id"].astype(str).eq(decision_id), "decision_value"] if not decisions.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_phase300_route_contract() -> pd.DataFrame:
    rows = [
        ("P300_THESIS", "passive_aware_execution_of_directional_top5_depth_signals", "Test the retail-available cost-side lever after taker-only edges failed."),
        ("P300_INPUT_DIRECTIONAL_SIGNALS", "P235;P268;P280;P281;P282;P298_sparse_directional_seeds", "Reuse existing directional L2 signals; no new alpha search."),
        ("P300_INPUT_FILL_MODEL", "P260_to_P269_passive_queue_depth_features", "Estimate P(fill | queue depth, side, horizon) from raw depth state."),
        ("P300_INPUT_TOXICITY", "P130_and_P280_to_P282_adverse_selection_toxicity_estimates", "Apply fill-conditioned toxicity/adverse-selection penalty."),
        ("P300_INPUT_FEED_FILTER", "P130_feed_imperfection_regime_filter", "Skip toxic or degraded feed windows where applicable."),
        ("P300_INPUT_COST_MODEL", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned Zerodha NSE equity intraday model with cost200 stress."),
        ("P300_INPUT_RAW_BOOK", "P51_raw_dense_lake;P298_schema_audit", "Use raw top-five market-by-price depth levels 1-5 price/qty/order-count."),
        ("P300_FORBID_L1_ONLY", "l1_only_variant_rows_must_equal_0", "Levels 2-5 materiality remains required."),
        ("P300_FORBID_LOOKAHEAD", "net_edge_live_mask_rows_must_equal_0", "No net-edge labels may be used as live masks."),
        ("P300_REQUIRED_EXECUTION_POLICY", "passive_entry_wait_cancel_or_cross;passive_exit_when_calm;aggressive_exit_when_risk_or_expiry", "Hybrid execution policy, not two-sided market-making."),
        ("P300_REQUIRED_PENALTIES", "fill_probability;adverse_selection;forced_flatten", "All three realism penalties are mandatory."),
        ("P300_ACCEPTANCE_BAR", "events_ge_30;annualized_gt_12pct_cost200;multi_symbol_date_breadth;rank_stable_1x_to_2x", "Sparse >12% pockets below 30 events are discovery-only."),
        ("P300_BOUNDARY", "replay_0;promotion_0;paper_live_0;profitability_claim_0", "Synthetic-only precommit; no acceptance flip."),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gate_evaluation(summary: pd.DataFrame, ranked: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    complete = as_int(metric_value(summary, "phase298_raw_dense_sweep_complete", 0))
    next_action = str(metric_value(summary, "phase298_next_best_action", ""))
    hard_pass = as_int(metric_value(summary, "phase298_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(summary, "phase298_hard_gate_rows", 0))
    sparse_above12 = as_int(metric_value(summary, "phase298_sparse_above12_scenario_rows", 0))
    robust_above12 = as_int(metric_value(summary, "phase298_robust_portfolio_above12_scenario_rows", 0))
    best_events = as_int(metric_value(summary, "phase298_best_scheduled_event_rows", 0))
    l1_only = as_int(metric_value(summary, "phase298_l1_only_variant_rows", 0))
    leakage = as_int(metric_value(summary, "phase298_net_edge_live_mask_rows", 0))
    replay = as_int(metric_value(summary, "phase298_strategy_replay_allowed", 0))
    paper = as_int(metric_value(summary, "phase298_paper_or_live_acceptance_allowed", 0))
    claim = as_int(metric_value(summary, "phase298_deployable_profitability_claim_allowed", 0))
    seed_rows = int(ranked["preserve_as_directional_signal_seed"].astype(int).sum()) if not ranked.empty else 0
    gates = [
        ("P299_PHASE298_SWEEP_COMPLETE", complete == 1, complete, "Phase298 sweep complete"),
        ("P299_PHASE298_NEXT_ACTION_PRESENT", "phase299" in next_action, next_action, "Phase298 routes to Phase299 interpretation"),
        ("P299_PHASE298_GATES_PASS", hard_rows > 0 and hard_pass == hard_rows, f"{hard_pass}/{hard_rows}", "Phase298 hard gates pass"),
        ("P299_RANKED_INTERPRETATION_PRESENT", len(ranked) > 0, len(ranked), ">0 ranked variants"),
        ("P299_CLOSES_PHASE298_FOR_DIRECT_ACCEPTANCE", str(decision_value(decisions, "close_phase298_for_direct_acceptance")) == "1", decision_value(decisions, "close_phase298_for_direct_acceptance"), "Phase298 closed for direct acceptance"),
        ("P299_NO_ACCEPTANCE_SURVIVOR", sparse_above12 == 0 and robust_above12 == 0, f"sparse_above12={sparse_above12};robust_above12={robust_above12}", "no Phase298 survivor"),
        ("P299_BEST_BELOW_PHASE300_EVENT_FLOOR", best_events < SPARSE_CLUE_EVENT_FLOOR, best_events, f"<{SPARSE_CLUE_EVENT_FLOOR}"),
        ("P299_DIRECTIONAL_SEEDS_PRESERVED", seed_rows > 0, seed_rows, ">0"),
        ("P299_RAW_TOP5_BOOK_SCOPE", l1_only == 0 and leakage == 0, f"l1_only={l1_only};live_mask={leakage}", "levels 1-5 and no leakage"),
        ("P299_FIXED_CAPITAL_DENOMINATOR", str(metric_value(summary, "phase298_annualized_denominator", "")) == "fixed_initial_capital", metric_value(summary, "phase298_annualized_denominator", ""), "fixed_initial_capital"),
        ("P299_NEXT_ROUTE_SELECTED", str(decision_value(decisions, "selected_next_route")) == SELECTED_NEXT_ROUTE, decision_value(decisions, "selected_next_route"), SELECTED_NEXT_ROUTE),
        ("P299_BOUNDARIES_CLOSED", replay == 0 and paper == 0 and claim == 0, f"replay={replay};paper={paper};claim={claim}", "no replay/paper/live/claim"),
        ("P299_PHASE300_CONTRACT_PRESENT", len(route) >= 13, len(route), "Phase300 route contract rows"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(summary: pd.DataFrame, ranked: pd.DataFrame, families: pd.DataFrame, decisions: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    best = ranked.iloc[0] if not ranked.empty else pd.Series(dtype=object)
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase299_interpretation_complete", 1, "Phase299 interpretation completed"),
            ("phase299_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
            ("phase299_phase298_variant_rows", metric_value(summary, "phase298_variant_rows", 0), "Phase298 variants interpreted"),
            ("phase299_phase298_scenario_rows", metric_value(summary, "phase298_scenario_rows", 0), "Phase298 scenarios interpreted"),
            ("phase299_phase298_sparse_above12_scenario_rows", metric_value(summary, "phase298_sparse_above12_scenario_rows", 0), "Phase298 sparse above-12 rows"),
            ("phase299_phase298_robust_portfolio_above12_scenario_rows", metric_value(summary, "phase298_robust_portfolio_above12_scenario_rows", 0), "Phase298 robust above-12 rows"),
            ("phase299_best_phase298_variant_id", best.get("phase298_variant_id", ""), "Best interpreted Phase298 variant"),
            ("phase299_best_strategy_family", best.get("strategy_family", ""), "Best interpreted family"),
            ("phase299_best_cost200_annualized_pct", best.get("max_annualized_pct", ""), "Best fixed-capital annualized diagnostic"),
            ("phase299_best_scheduled_event_rows", best.get("max_scheduled_event_rows", ""), "Best scheduled events"),
            ("phase299_above12_below_30_event_variant_rows", int(ranked["above12_but_below_phase300_floor"].astype(int).sum()) if not ranked.empty else 0, "Above-12 but below 30-event clue rows"),
            ("phase299_directional_signal_seed_rows", int(ranked["preserve_as_directional_signal_seed"].astype(int).sum()) if not ranked.empty else 0, "Directional signal seeds preserved"),
            ("phase299_family_rows", len(families), "Families interpreted"),
            ("phase299_close_phase298_for_direct_acceptance", decision_value(decisions, "close_phase298_for_direct_acceptance"), "Close Phase298 for direct acceptance"),
            ("phase299_do_not_add_new_alpha_search_in_phase300", decision_value(decisions, "do_not_add_new_alpha_search_in_phase300"), "Phase300 is execution realism, not new alpha search"),
            ("phase299_require_passive_fill_model", decision_value(decisions, "require_passive_fill_model"), "Passive fill model required"),
            ("phase299_require_adverse_selection_penalty", decision_value(decisions, "require_adverse_selection_penalty"), "Adverse selection penalty required"),
            ("phase299_require_forced_flatten_cost", decision_value(decisions, "require_forced_flatten_cost"), "Forced flatten cost required"),
            ("phase299_strategy_replay_allowed", 0, "No replay"),
            ("phase299_strategy_promotion_allowed", 0, "No promotion"),
            ("phase299_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase299_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase299_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase299_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase299_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, summary: pd.DataFrame, ranked: pd.DataFrame, families: pd.DataFrame, interpretation: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase299 Raw Dense Top-Five Book-State Strategy Sweep Interpretation",
        "",
        "Phase299 closes Phase298 for direct acceptance and preserves its high-annualized sparse pockets only as directional-signal seeds.",
        "",
        "The selected next route is a Phase300 passive-aware execution precommit. Phase300 must freeze fill probability, adverse-selection, and forced-flatten rules before producing results.",
        "",
        "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened.",
        "",
        "## Phase298 Summary",
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
        "## Phase300 Route Contract",
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
    (output_dir / "phase299_raw_dense_top5_book_state_strategy_sweep_interpretation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase298_dir: Path = DEFAULT_PHASE298_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    summary = read_csv(phase298_dir / "phase298_acceptance_summary.csv")
    variants = read_csv(phase298_dir / "phase298_variant_summary.csv")
    family_summary = read_csv(phase298_dir / "phase298_family_summary.csv")
    if summary.empty or variants.empty or family_summary.empty:
        raise FileNotFoundError(f"Phase298 outputs are incomplete under {phase298_dir}")
    ranked = build_ranked_interpretation(variants)
    families = build_family_interpretation(family_summary, ranked)
    interpretation = build_interpretation_ledger(summary, ranked)
    decisions = build_decision_ledger(ranked)
    route = build_phase300_route_contract()
    gates = build_gate_evaluation(summary, ranked, decisions, route)
    acceptance = build_acceptance(summary, ranked, families, decisions, gates)

    ranked.to_csv(output_dir / "phase299_ranked_variant_interpretation.csv", index=False)
    families.to_csv(output_dir / "phase299_family_interpretation.csv", index=False)
    interpretation.to_csv(output_dir / "phase299_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase299_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase299_phase300_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase299_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase299_acceptance_summary.csv", index=False)
    write_report(output_dir, summary, ranked, families, interpretation, decisions, route, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase299_raw_dense_top5_book_state_strategy_sweep_interpretation",
        **reproducibility_fields(
            artifact_id="phase299",
            generated_utc=generated_utc,
            inputs={
                "phase298_acceptance_summary": str(phase298_dir / "phase298_acceptance_summary.csv"),
                "phase298_variant_summary": str(phase298_dir / "phase298_variant_summary.csv"),
                "phase298_family_summary": str(phase298_dir / "phase298_family_summary.csv"),
            },
            parameters={
                "selected_next_route": SELECTED_NEXT_ROUTE,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "sparse_clue_event_floor": SPARSE_CLUE_EVENT_FLOOR,
                "robust_portfolio_event_floor": ROBUST_PORTFOLIO_EVENT_FLOOR,
                "phase300_policy": "precommit_before_results",
            },
            outputs={"acceptance_summary": str(output_dir / "phase299_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase299_interpretation_only",
        ),
    }
    (output_dir / "phase299_raw_dense_top5_book_state_strategy_sweep_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase299 raw dense top-five book-state sweep interpretation.")
    parser.add_argument("--phase298-dir", type=Path, default=DEFAULT_PHASE298_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(phase298_dir=args.phase298_dir, output_dir=args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

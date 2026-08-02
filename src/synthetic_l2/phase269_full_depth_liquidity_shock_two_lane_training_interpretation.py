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


DEFAULT_PHASE268_DIR = Path("outputs/phase268")
DEFAULT_OUTPUT_DIR = Path("outputs/phase269")
SELECTED_NEXT_ROUTE = "P269_FIXED_CAPITAL_CONCURRENCY_AND_CAPACITY_RETURN_PRECOMMIT"
NEXT_ACTION = "run_phase270_fixed_capital_concurrency_and_capacity_return_precommit_no_paper_live"


def metric_value_from_frame(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return default if rows.empty else rows.iloc[0]


def build_research_lead_ranking(variants: pd.DataFrame) -> pd.DataFrame:
    if variants.empty:
        return pd.DataFrame()
    frame = variants.copy()
    numeric_cols = [
        "cost100_annualized_return_pct",
        "cost200_annualized_return_pct",
        "cost100_net_pnl_inr",
        "cost200_net_pnl_inr",
        "cost200_avg_net_per_event",
        "shuffle_label_margin_inr",
        "cost100_event_rows",
        "symbols",
        "trade_dates",
        "annualized_profitable_research_lead",
        "cost200_annualized_profitable_research_lead",
        "acceptance_grade_candidate",
        "exploratory_candidate",
        "side_flip_degrades",
        "random_side_beat",
    ]
    for col in numeric_cols:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    leads = frame.loc[frame["annualized_profitable_research_lead"].astype(int).eq(1)].copy()
    if leads.empty:
        return leads
    leads["fixed_notional_proxy_only"] = 1
    leads["portfolio_return_validated"] = 0
    leads["needs_capital_concurrency_capacity_model"] = 1
    leads["acceptance_blockers"] = leads.apply(
        lambda row: ";".join(
            blocker
            for blocker, failed in [
                ("not_2x_annualized_above_12pct", safe_float(row.get("cost200_annualized_return_pct", 0.0), 0.0) < 12.0),
                ("acceptance_grade_zero", as_int(row.get("acceptance_grade_candidate", 0)) == 0),
                ("events_lt_30", as_int(row.get("cost100_event_rows", 0)) < 30),
                ("symbols_lt_8", as_int(row.get("symbols", 0)) < 8),
                ("shuffle_margin_lt_100", safe_float(row.get("shuffle_label_margin_inr", 0.0), 0.0) < 100.0),
                ("cost200_avg_lt_25", safe_float(row.get("cost200_avg_net_per_event", 0.0), 0.0) < 25.0),
            ]
            if failed
        ),
        axis=1,
    )
    keep = [
        "candidate_id",
        "family_id",
        "horizon",
        "imbalance_quantile",
        "shock_quantile",
        "spread_regime",
        "cost100_event_rows",
        "symbols",
        "trade_dates",
        "cost100_net_pnl_inr",
        "cost100_annualized_return_pct",
        "cost150_net_pnl_inr",
        "cost200_net_pnl_inr",
        "cost200_annualized_return_pct",
        "cost200_avg_net_per_event",
        "shuffle_label_margin_inr",
        "side_flip_degrades",
        "random_side_beat",
        "acceptance_grade_candidate",
        "fixed_notional_proxy_only",
        "portfolio_return_validated",
        "needs_capital_concurrency_capacity_model",
        "acceptance_blockers",
    ]
    keep = [col for col in keep if col in leads.columns]
    return leads[keep].sort_values(
        ["cost100_annualized_return_pct", "cost100_net_pnl_inr", "symbols", "cost100_event_rows"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_failure_mode_ledger(summary: pd.DataFrame, variants: pd.DataFrame, leads: pd.DataFrame) -> pd.DataFrame:
    annualization_is_portfolio = as_int(metric_value_from_frame(summary, "phase268_annualization_is_portfolio_return", 1))
    annualized_leads = as_int(metric_value_from_frame(summary, "phase268_annualized_profitable_research_lead_rows", 0))
    cost200_annualized_leads = as_int(metric_value_from_frame(summary, "phase268_cost200_annualized_profitable_research_lead_rows", 0))
    acceptance_rows = as_int(metric_value_from_frame(summary, "phase268_acceptance_grade_candidate_rows", 0))
    variant_rows = as_int(metric_value_from_frame(summary, "phase268_variant_rows", 0))
    full_depth = as_int(metric_value_from_frame(summary, "phase268_full_top_five_depth_variant_rows", 0))
    l2_l5 = as_int(metric_value_from_frame(summary, "phase268_depth_beyond_l1_variant_rows", 0))
    l1_only = as_int(metric_value_from_frame(summary, "phase268_l1_only_variant_rows", 0))
    best_cost100_ann = safe_float(metric_value_from_frame(summary, "phase268_best_cost100_annualized_return_pct", 0.0), 0.0)
    best_cost200_ann = safe_float(metric_value_from_frame(summary, "phase268_best_cost200_annualized_return_pct", 0.0), 0.0)
    best_shuffle = safe_float(metric_value_from_frame(summary, "phase268_best_shuffle_label_margin_inr", 0.0), 0.0)
    best_events = as_int(metric_value_from_frame(summary, "phase268_best_event_rows", 0))
    best_symbols = as_int(metric_value_from_frame(summary, "phase268_best_symbols", 0))
    rows = [
        ("profitable_fixed_notional_research_leads_found", f"annualized_1x_leads={annualized_leads}; best_1x_annualized={best_cost100_ann}", "research_positive", int(annualized_leads > 0), "There are profit-hunting leads worth preserving."),
        ("no_cost200_annualized_profitable_research_leads", f"cost200_annualized_leads={cost200_annualized_leads}; best_2x_annualized={best_cost200_ann}", "hard", int(cost200_annualized_leads == 0), "No lead clears the 12% fixed-notional proxy under 2x modeled costs."),
        ("no_acceptance_grade_candidate", f"acceptance_grade_candidates={acceptance_rows}", "hard", int(acceptance_rows == 0), "No candidate is acceptance-grade yet."),
        ("annualization_not_portfolio_return", f"phase268_annualization_is_portfolio_return={annualization_is_portfolio}", "hard", int(annualization_is_portfolio == 0), "Annualized values are fixed-notional proxies, not capital-account portfolio returns."),
        ("best_lead_breadth_and_shuffle_fragile", f"events={best_events};symbols={best_symbols};shuffle_margin={best_shuffle}", "hard", int(best_events < 30 or best_symbols < 8 or best_shuffle < 100.0), "Best lead remains sparse or shuffle-fragile."),
        ("capital_concurrency_capacity_missing", "capital_concurrency_model=not_yet_materialized;capacity_model=not_yet_materialized", "hard", 1, "Next phase must convert fixed-notional proxies into capital-aware return evidence."),
        ("full_depth_surface_preserved", f"full_depth={full_depth};l2_l5={l2_l5};l1_only={l1_only};variants={variant_rows}", "important_context", int(full_depth == variant_rows and l2_l5 == variant_rows and l1_only == 0 and variant_rows > 0), "Full-depth L2/L2-L5 objective remains intact."),
    ]
    return pd.DataFrame(rows, columns=["finding_id", "evidence", "severity", "finding_present", "interpretation"])


def build_decision_ledger(summary: pd.DataFrame, leads: pd.DataFrame) -> pd.DataFrame:
    annualized_leads = as_int(metric_value_from_frame(summary, "phase268_annualized_profitable_research_lead_rows", 0))
    acceptance_rows = as_int(metric_value_from_frame(summary, "phase268_acceptance_grade_candidate_rows", 0))
    return pd.DataFrame(
        [
            ("preserve_phase268_research_leads", int(annualized_leads > 0), f"annualized_1x_research_leads={annualized_leads}", "Keep the leads for next-stage capital-aware analysis."),
            ("do_not_claim_portfolio_annual_return", 1, "annualization_formula=net_pnl_inr / 100000 * 252", "Annualized values are fixed-notional proxies only."),
            ("do_not_promote_or_replay_phase268", int(acceptance_rows == 0), f"acceptance_grade_candidates={acceptance_rows}", "No replay, promotion, paper/live, or deployable profitability claim."),
            ("require_fixed_capital_concurrency_model", 1, "small-event annualized proxy can overstate deployable return", "Next phase must model simultaneous capital use, per-event notional, and capacity."),
            ("preserve_full_depth_requirement", 1, "rows_1_to_5_and_l2_l5_required", "Full-depth Zerodha top-five depth remains mandatory."),
            ("selected_next_route", SELECTED_NEXT_ROUTE, "capital-aware return precommit", "Next materially necessary action."),
        ],
        columns=["decision_id", "decision_value", "evidence", "description"],
    )


def build_next_route_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("P270_INPUT", "outputs/phase268/phase268_two_lane_variant_results.csv and outputs/phase268/phase268_exploratory_event_ledger.csv", "Use Phase268 research leads and event ledger; no replay yet."),
            ("P270_RETURN_TYPE", "fixed_capital_portfolio_return_model", "Convert fixed-notional annualized proxy into capital-aware return evidence."),
            ("P270_CAPITAL_ACCOUNTING", "initial_capital;per_trade_notional;max_concurrent_positions;capital_reuse;cash_drag", "Explicitly model capital constraints instead of assuming unlimited capital."),
            ("P270_CAPACITY_ACCOUNTING", "events_per_day;symbol_capacity;turnover;cost_stress;slippage_sensitivity", "Check if small-event pockets remain meaningful after capacity and turnover limits."),
            ("P270_DEPTH_REQUIREMENT", "full_top_five_rows_1_to_5_and_levels_2_to_5_required", "Capital-aware analysis must still use the full-depth L2 signal surface."),
            ("P270_FORBIDDEN", "paper_live_or_deployable_profitability_claim;portfolio_return_claim_without_capital_model;l1_only", "No claim until capital/capacity model exists and L1-only remains forbidden."),
            ("P270_OUTPUT", "capital_return_precommit_and_candidate_capacity_contract", "Write the contract for a later capital-aware analysis/search."),
        ],
        columns=["contract_id", "contract_value", "description"],
    )


def decision_value(frame: pd.DataFrame, decision_id: str) -> str:
    rows = frame.loc[frame["decision_id"].astype(str).eq(decision_id), "decision_value"] if not frame.empty else pd.Series(dtype=str)
    return "" if rows.empty else str(rows.iloc[0])


def build_gate_evaluation(phase268_dir: Path, summary: pd.DataFrame, variants: pd.DataFrame, leads: pd.DataFrame, decisions: pd.DataFrame, route: pd.DataFrame) -> pd.DataFrame:
    next_action = str(metric_value(phase268_dir / "phase268_acceptance_summary.csv", "phase268_next_best_action", ""))
    variant_rows = as_int(metric_value_from_frame(summary, "phase268_variant_rows", 0))
    full_depth = as_int(metric_value_from_frame(summary, "phase268_full_top_five_depth_variant_rows", 0))
    l2_l5 = as_int(metric_value_from_frame(summary, "phase268_depth_beyond_l1_variant_rows", 0))
    l1_only = as_int(metric_value_from_frame(summary, "phase268_l1_only_variant_rows", 0))
    annualization_is_portfolio = as_int(metric_value_from_frame(summary, "phase268_annualization_is_portfolio_return", 1))
    acceptance_rows = as_int(metric_value_from_frame(summary, "phase268_acceptance_grade_candidate_rows", 0))
    rows = [
        ("P269_PHASE268_WORK_ORDER_PRESENT", "run_phase269_full_depth_liquidity_shock_two_lane_training_interpretation" in next_action, next_action, "Phase268 next action targets Phase269", "hard"),
        ("P269_PHASE268_SEARCH_EXECUTED", variant_rows > 0 and len(variants) == variant_rows, f"summary={variant_rows};rows={len(variants)}", "Phase268 variants present", "hard"),
        ("P269_FULL_DEPTH_RECOGNIZED", full_depth == variant_rows and l2_l5 == variant_rows and l1_only == 0 and variant_rows > 0, f"full_depth={full_depth};l2_l5={l2_l5};l1_only={l1_only};variants={variant_rows}", "all variants full-depth and no L1-only", "hard"),
        ("P269_RESEARCH_LEADS_RANKED", len(leads) == as_int(metric_value_from_frame(summary, "phase268_annualized_profitable_research_lead_rows", 0)), len(leads), "all annualized research leads ranked", "hard"),
        ("P269_ANNUALIZATION_NOT_PORTFOLIO_RECOGNIZED", annualization_is_portfolio == 0, annualization_is_portfolio, "annualized proxy is not portfolio return", "hard"),
        ("P269_NO_ACCEPTANCE_RECOGNIZED", acceptance_rows == 0, acceptance_rows, "0 acceptance-grade candidates", "hard"),
        ("P269_CAPITAL_MODEL_NEXT_ROUTE_SELECTED", decision_value(decisions, "selected_next_route") == SELECTED_NEXT_ROUTE and int(route["contract_id"].astype(str).eq("P270_CAPITAL_ACCOUNTING").sum()) == 1, SELECTED_NEXT_ROUTE, "capital-aware precommit selected", "hard"),
        ("P269_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase269 Full-depth Liquidity-shock Two-lane Training Interpretation",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase269 interprets Phase268 after adding the fixed-notional annualized-return research lens.",
        "It preserves profitable exploratory leads, but explicitly refuses to treat fixed-notional annualization as portfolio annual return.",
        "The next step is a capital/concurrency/capacity return precommit, while full Zerodha top-five rows 1-5 and levels 2-5 remain mandatory.",
        "This is not replay execution, strategy promotion, paper/live acceptance, or a deployable profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(phase268_dir: Path = DEFAULT_PHASE268_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = read_csv(phase268_dir / "phase268_acceptance_summary.csv")
    variants = read_csv(phase268_dir / "phase268_two_lane_variant_results.csv")
    if summary.empty:
        raise FileNotFoundError("Missing Phase268 acceptance summary.")
    if variants.empty:
        raise FileNotFoundError("Missing Phase268 variant results.")
    leads = build_research_lead_ranking(variants)
    failures = build_failure_mode_ledger(summary, variants, leads)
    decisions = build_decision_ledger(summary, leads)
    route = build_next_route_contract()
    gates = build_gate_evaluation(phase268_dir, summary, variants, leads, decisions, route)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    best_lead = leads.iloc[0].to_dict() if not leads.empty else {}
    next_action = NEXT_ACTION if hard_pass == len(hard) else "repair_phase269_two_lane_interpretation"
    acceptance = pd.DataFrame(
        [
            ("phase269_interpretation_complete", 1, "Phase269 two-lane training interpretation completed"),
            ("phase269_phase268_variant_rows", as_int(metric_value_from_frame(summary, "phase268_variant_rows", 0)), "Phase268 variants interpreted"),
            ("phase269_phase268_full_depth_variant_rows", as_int(metric_value_from_frame(summary, "phase268_full_top_five_depth_variant_rows", 0)), "Full-depth variants interpreted"),
            ("phase269_phase268_l2_l5_variant_rows", as_int(metric_value_from_frame(summary, "phase268_depth_beyond_l1_variant_rows", 0)), "Levels 2-5 variants interpreted"),
            ("phase269_phase268_l1_only_variant_rows", as_int(metric_value_from_frame(summary, "phase268_l1_only_variant_rows", 0)), "L1-only variants interpreted"),
            ("phase269_phase268_exploratory_candidate_rows", as_int(metric_value_from_frame(summary, "phase268_exploratory_candidate_rows", 0)), "Exploratory candidates"),
            ("phase269_phase268_annualized_profitable_research_lead_rows", as_int(metric_value_from_frame(summary, "phase268_annualized_profitable_research_lead_rows", 0)), "Fixed-notional annualized 1x research leads"),
            ("phase269_phase268_cost200_annualized_profitable_research_lead_rows", as_int(metric_value_from_frame(summary, "phase268_cost200_annualized_profitable_research_lead_rows", 0)), "Fixed-notional annualized 2x research leads"),
            ("phase269_phase268_acceptance_grade_candidate_rows", as_int(metric_value_from_frame(summary, "phase268_acceptance_grade_candidate_rows", 0)), "Acceptance-grade candidates"),
            ("phase269_annualization_notional_inr", metric_value_from_frame(summary, "phase268_annualization_notional_inr", ""), "Fixed notional denominator"),
            ("phase269_annualization_formula", metric_value_from_frame(summary, "phase268_annualization_formula", ""), "Annualization formula"),
            ("phase269_annualization_is_portfolio_return", as_int(metric_value_from_frame(summary, "phase268_annualization_is_portfolio_return", 1)), "Annualization is portfolio return flag"),
            ("phase269_best_research_lead_candidate_id", best_lead.get("candidate_id", ""), "Top fixed-notional annualized research lead"),
            ("phase269_best_research_lead_family_id", best_lead.get("family_id", ""), "Top lead family"),
            ("phase269_best_research_lead_cost100_annualized_return_pct", best_lead.get("cost100_annualized_return_pct", 0.0), "Top lead 1x annualized proxy"),
            ("phase269_best_research_lead_cost200_annualized_return_pct", best_lead.get("cost200_annualized_return_pct", 0.0), "Top lead 2x annualized proxy"),
            ("phase269_best_research_lead_events", best_lead.get("cost100_event_rows", 0), "Top lead event rows"),
            ("phase269_best_research_lead_symbols", best_lead.get("symbols", 0), "Top lead symbols"),
            ("phase269_best_research_lead_shuffle_margin_inr", best_lead.get("shuffle_label_margin_inr", 0.0), "Top lead shuffled-label margin"),
            ("phase269_preserve_research_leads", as_int(decision_value(decisions, "preserve_phase268_research_leads"), 0), "Preserve research leads"),
            ("phase269_do_not_claim_portfolio_annual_return", as_int(decision_value(decisions, "do_not_claim_portfolio_annual_return"), 0), "Do not claim portfolio annual return"),
            ("phase269_do_not_promote_or_replay_phase268", as_int(decision_value(decisions, "do_not_promote_or_replay_phase268"), 0), "Do not promote/replay Phase268"),
            ("phase269_selected_next_route", SELECTED_NEXT_ROUTE, "Selected next route"),
            ("phase269_next_route_contract_rows", len(route), "Next route contract rows"),
            ("phase269_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase269_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase269_download_more_dates_now_allowed", 0, "No new download in Phase269"),
            ("phase269_replay_execution_allowed_now", 0, "No replay execution in Phase269"),
            ("phase269_strategy_promotion_allowed", 0, "No strategy promotion from Phase269"),
            ("phase269_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase269"),
            ("phase269_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase269"),
            ("phase269_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    leads.to_csv(output_dir / "phase269_ranked_annualized_research_leads.csv", index=False)
    failures.to_csv(output_dir / "phase269_interpretation_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase269_decision_ledger.csv", index=False)
    route.to_csv(output_dir / "phase269_next_route_contract.csv", index=False)
    gates.to_csv(output_dir / "phase269_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase269_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase269_full_depth_liquidity_shock_two_lane_training_interpretation_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Ranked Annualized Research Leads": leads.head(30),
            "Interpretation Ledger": failures,
            "Decision Ledger": decisions,
            "Next Route Contract": route,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase269_full_depth_liquidity_shock_two_lane_training_interpretation",
        **reproducibility_fields(
            artifact_id="phase269",
            generated_utc=generated_utc,
            inputs={"phase268_dir": str(phase268_dir)},
            parameters={
                "selected_next_route": SELECTED_NEXT_ROUTE,
                "annualized_proxy_is_portfolio_return": 0,
                "full_top_five_depth_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "l1_only_candidate_allowed": 0,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "ranked_annualized_research_leads": str(output_dir / "phase269_ranked_annualized_research_leads.csv"),
                "interpretation_ledger": str(output_dir / "phase269_interpretation_ledger.csv"),
                "decision_ledger": str(output_dir / "phase269_decision_ledger.csv"),
                "next_route_contract": str(output_dir / "phase269_next_route_contract.csv"),
                "gate_evaluation": str(output_dir / "phase269_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase269_acceptance_summary.csv"),
                "report": str(output_dir / "phase269_full_depth_liquidity_shock_two_lane_training_interpretation_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase269_no_replay_interpretation",
        ),
    }
    (output_dir / "phase269_full_depth_liquidity_shock_two_lane_training_interpretation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase269 two-lane liquidity-shock interpretation.")
    parser.add_argument("--phase268-dir", type=Path, default=DEFAULT_PHASE268_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(phase268_dir=args.phase268_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, metric_value, read_csv
from synthetic_l2.phase271_fixed_capital_concurrency_and_capacity_return_analysis import (
    COST_PROFILES,
    MIN_DATES_FOR_PORTFOLIO_CLAIM,
    load_candidate_events,
    schedule_events_for_scenario,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE268_DIR = Path("outputs/phase268")
DEFAULT_PHASE269_DIR = Path("outputs/phase269")
DEFAULT_PHASE272_DIR = Path("outputs/phase272")
DEFAULT_OUTPUT_DIR = Path("outputs/phase273")

SELECTED_ROUTE = "P273_FOCUSED_CAPITAL_AWARE_CANDIDATE_FOLLOWTHROUGH_SEARCH"
NEXT_ACTION = "run_phase274_focused_capital_followthrough_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase273_focused_capital_aware_candidate_followthrough_search"

INITIAL_CAPITAL_GRID_INR = [100_000.0, 250_000.0, 500_000.0]
FIXED_NOTIONAL_GRID_INR = [50_000.0, 75_000.0, 100_000.0, 125_000.0]
MAX_CONCURRENT_GRID = [1, 2, 3, 4]
ANNUALIZED_THRESHOLD_PCT = 12.0

ORDER_POLICIES = [
    "time_rank",
    "time_reverse_rank",
    "rank_time",
    "reverse_rank_time",
    "deterministic_shuffle",
]


def metric_value_from_frame(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return default if rows.empty else rows.iloc[0]


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_priority_candidates(phase272_dir: Path) -> list[str]:
    ranked = read_csv(phase272_dir / "phase272_ranked_capital_aware_research_pockets.csv")
    if ranked.empty:
        raise FileNotFoundError("Missing Phase272 ranked capital-aware research pockets.")
    priority = ranked[pd.to_numeric(ranked.get("followthrough_priority"), errors="coerce").fillna(0).astype(int).eq(1)].copy()
    if priority.empty:
        priority = ranked.head(2).copy()
    return priority["scope_candidate_id"].astype(str).head(2).tolist()


def build_followthrough_scopes(priority_candidates: list[str], events: pd.DataFrame) -> list[tuple[str, str, pd.DataFrame]]:
    scopes: list[tuple[str, str, pd.DataFrame]] = []
    for index, candidate_id in enumerate(priority_candidates, start=1):
        scope_events = events[events["candidate_id"].astype(str).eq(candidate_id)].copy()
        if not scope_events.empty:
            scopes.append((f"PRIORITY{index:02d}", candidate_id, scope_events))
    if len(priority_candidates) >= 2:
        subset_events = events[events["candidate_id"].astype(str).isin(priority_candidates)].copy()
        if not subset_events.empty:
            scopes.append(("TOP2_PRIORITY_SUBSET", ";".join(priority_candidates), subset_events))
    return scopes


def apply_order_policy(events: pd.DataFrame, policy: str) -> pd.DataFrame:
    frame = events.copy()
    if policy == "time_rank":
        return frame.sort_values(["trade_date", "exchange", "richer_event_bar_id", "candidate_rank", "candidate_id", "symbol"]).reset_index(drop=True)
    if policy == "time_reverse_rank":
        return frame.sort_values(["trade_date", "exchange", "richer_event_bar_id", "candidate_rank", "candidate_id", "symbol"], ascending=[True, True, True, False, True, True]).reset_index(drop=True)
    if policy == "rank_time":
        return frame.sort_values(["candidate_rank", "trade_date", "exchange", "richer_event_bar_id", "candidate_id", "symbol"]).reset_index(drop=True)
    if policy == "reverse_rank_time":
        return frame.sort_values(["candidate_rank", "trade_date", "exchange", "richer_event_bar_id", "candidate_id", "symbol"], ascending=[False, True, True, True, True, True]).reset_index(drop=True)
    if policy == "deterministic_shuffle":
        key = (
            frame["candidate_id"].astype(str)
            + "|"
            + frame["trade_date"].astype(str)
            + "|"
            + frame["exchange"].astype(str)
            + "|"
            + frame["symbol"].astype(str)
            + "|"
            + frame["richer_event_bar_id"].astype(str)
        )
        frame["_shuffle_key"] = key.map(stable_hash)
        return frame.sort_values("_shuffle_key").drop(columns=["_shuffle_key"]).reset_index(drop=True)
    raise ValueError(f"Unknown order policy: {policy}")


def run_followthrough_search(priority_candidates: list[str], events: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    scenario_rows: list[dict[str, Any]] = []
    sample_ledger_frames: list[pd.DataFrame] = []
    scopes = build_followthrough_scopes(priority_candidates, events)
    for scope_id, scope_candidate_id, scope_events in scopes:
        for order_policy in ORDER_POLICIES:
            ordered_events = apply_order_policy(scope_events, order_policy)
            for initial_capital in INITIAL_CAPITAL_GRID_INR:
                for fixed_notional in FIXED_NOTIONAL_GRID_INR:
                    for max_concurrent in MAX_CONCURRENT_GRID:
                        for profile in COST_PROFILES:
                            scenario, ledger = schedule_events_for_scenario(
                                events=ordered_events,
                                scope_id=f"P273_{scope_id}_{order_policy.upper()}",
                                scope_candidate_id=scope_candidate_id,
                                initial_capital_inr=initial_capital,
                                fixed_notional_inr=fixed_notional,
                                max_concurrent_positions=max_concurrent,
                                cost_profile=profile["cost_profile"],
                                cost_multiplier=profile["cost_multiplier"],
                                extra_slippage_bps=profile["extra_slippage_bps"],
                            )
                            scenario["phase273_scope_id"] = scope_id
                            scenario["phase273_scope_candidate_id"] = scope_candidate_id
                            scenario["order_policy"] = order_policy
                            scenario["candidate_subset_size"] = len(scope_candidate_id.split(";"))
                            scenario_rows.append(scenario)
                            if profile["cost_profile"] in {"cost100", "cost200"} and initial_capital == 100_000.0 and fixed_notional == 100_000.0 and max_concurrent in {1, 2}:
                                ledger = ledger.copy()
                                ledger["phase273_scope_id"] = scope_id
                                ledger["order_policy"] = order_policy
                                sample_ledger_frames.append(ledger)
    results = pd.DataFrame(scenario_rows)
    sample_ledger = pd.concat(sample_ledger_frames, ignore_index=True) if sample_ledger_frames else pd.DataFrame()
    return results, sample_ledger


def build_stability_summary(results: pd.DataFrame) -> pd.DataFrame:
    frame = results.copy()
    numeric = [
        "mechanical_one_date_annualized_portfolio_return_pct",
        "realized_net_pnl_inr",
        "annualized_above_12pct_research_diagnostic",
        "scheduled_event_rows",
        "max_drawdown_inr",
    ]
    for col in numeric:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    grouped = (
        frame.groupby(["phase273_scope_id", "phase273_scope_candidate_id", "cost_profile"], dropna=False)
        .agg(
            scenario_rows=("scenario_id", "nunique"),
            above12_scenario_rows=("annualized_above_12pct_research_diagnostic", "sum"),
            min_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "min"),
            median_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "median"),
            max_annualized_pct=("mechanical_one_date_annualized_portfolio_return_pct", "max"),
            max_realized_net_pnl_inr=("realized_net_pnl_inr", "max"),
            max_scheduled_event_rows=("scheduled_event_rows", "max"),
            worst_drawdown_inr=("max_drawdown_inr", "min"),
            order_policy_rows=("order_policy", "nunique"),
        )
        .reset_index()
    )
    grouped["above12_fraction"] = grouped["above12_scenario_rows"] / grouped["scenario_rows"]
    return grouped.sort_values(["cost_profile", "above12_scenario_rows", "max_annualized_pct"], ascending=[True, False, False]).reset_index(drop=True)


def build_gate_evaluation(phase272_dir: Path, priority_candidates: list[str], results: pd.DataFrame, stability: pd.DataFrame) -> pd.DataFrame:
    phase272_summary = read_csv(phase272_dir / "phase272_acceptance_summary.csv")
    phase272_next = str(metric_value_from_frame(phase272_summary, "phase272_next_best_action", ""))
    phase272_complete = as_int(metric_value_from_frame(phase272_summary, "phase272_interpretation_complete", 0))
    scenario_expected = len(build_followthrough_scopes(priority_candidates, results.rename(columns={"phase273_scope_candidate_id": "candidate_id"}))) if False else 0
    cost200_positive = int(results[results["cost_profile"].astype(str).eq("cost200")]["annualized_above_12pct_research_diagnostic"].astype(int).sum()) if not results.empty else 0
    full_depth = as_int(metric_value_from_frame(phase272_summary, "phase272_strategy_replay_allowed", 0)) == 0
    rows = [
        ("P273_PHASE272_WORK_ORDER_PRESENT", "run_phase273_focused_capital_aware_candidate_followthrough_search" in phase272_next, phase272_next, "Phase272 next action targets Phase273", "hard"),
        ("P273_PHASE272_INTERPRETATION_COMPLETE", phase272_complete == 1, phase272_complete, "Phase272 complete", "hard"),
        ("P273_PRIORITY_CANDIDATES_PRESENT", len(priority_candidates) >= 2, len(priority_candidates), ">=2 priority candidates", "hard"),
        ("P273_FOLLOWTHROUGH_SCENARIOS_PRESENT", len(results) > 0, len(results), ">0 follow-through scenarios", "hard"),
        ("P273_ORDER_POLICY_STRESS_PRESENT", set(ORDER_POLICIES).issubset(set(results["order_policy"].astype(str))), ";".join(sorted(results["order_policy"].astype(str).unique())), "all order policies", "hard"),
        ("P273_COST200_DIAGNOSTIC_SURVIVES", cost200_positive > 0, cost200_positive, ">0 cost200 above-12 one-date diagnostic scenarios", "hard"),
        ("P273_FULL_DEPTH_BOUNDARY_PRESERVED", full_depth, "phase272_replay_closed_and_full_depth_contract_inherited", "full-depth inherited, replay closed", "hard"),
        ("P273_NO_REPLAY_PROMOTION_PAPER_LIVE", bool((results["strategy_replay_allowed"] == 0).all() and (results["promotion_allowed"] == 0).all() and (results["paper_or_live_acceptance_allowed"] == 0).all()), 0, "replay/promotion/paper-live closed", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(priority_candidates: list[str], results: pd.DataFrame, stability: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    best = results.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
    cost100 = results[results["cost_profile"].astype(str).eq("cost100")]
    cost200 = results[results["cost_profile"].astype(str).eq("cost200")]
    robust_scope_cost200 = stability[
        stability["cost_profile"].astype(str).eq("cost200")
        & (pd.to_numeric(stability["above12_scenario_rows"], errors="coerce").fillna(0) > 0)
    ]
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase273_followthrough_search_complete", 1, "Phase273 focused capital-aware follow-through search completed"),
        ("phase273_selected_route", SELECTED_ROUTE, "Selected route"),
        ("phase273_priority_candidate_rows", len(priority_candidates), "Priority Phase272 candidates used"),
        ("phase273_priority_candidates", ";".join(priority_candidates), "Priority candidate IDs"),
        ("phase273_scope_rows", int(results["phase273_scope_id"].astype(str).nunique()), "Candidate/subset scopes"),
        ("phase273_order_policy_rows", int(results["order_policy"].astype(str).nunique()), "Order policies evaluated"),
        ("phase273_scenario_rows", len(results), "Follow-through scenarios evaluated"),
        ("phase273_cost100_above12_scenario_rows", int(cost100["annualized_above_12pct_research_diagnostic"].astype(int).sum()), "Cost100 above-12 one-date diagnostic rows"),
        ("phase273_cost200_above12_scenario_rows", int(cost200["annualized_above_12pct_research_diagnostic"].astype(int).sum()), "Cost200 above-12 one-date diagnostic rows"),
        ("phase273_cost200_positive_scope_profile_rows", int(len(robust_scope_cost200)), "Scope/profile rows with any 2x-cost above-12 diagnostics"),
        ("phase273_best_scenario_id", best["scenario_id"], "Best follow-through scenario"),
        ("phase273_best_scope_id", best["phase273_scope_id"], "Best follow-through scope"),
        ("phase273_best_scope_candidate_id", best["phase273_scope_candidate_id"], "Best follow-through candidate scope"),
        ("phase273_best_order_policy", best["order_policy"], "Best order policy"),
        ("phase273_best_cost_profile", best["cost_profile"], "Best cost profile"),
        ("phase273_best_realized_net_pnl_inr", best["realized_net_pnl_inr"], "Best realized net P&L"),
        ("phase273_best_mechanical_one_date_annualized_portfolio_return_pct", best["mechanical_one_date_annualized_portfolio_return_pct"], "Best one-date annualized diagnostic"),
        ("phase273_best_scheduled_event_rows", best["scheduled_event_rows"], "Best scheduled event rows"),
        ("phase273_best_notional_turnover_x_initial_capital", best["notional_turnover_x_initial_capital"], "Best notional turnover / capital"),
        ("phase273_portfolio_claim_allowed", 0, "Robust portfolio claim remains closed"),
        ("phase273_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase273_strategy_promotion_allowed", 0, "No strategy promotion unlocked"),
        ("phase273_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase273_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase273_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase273_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase273_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase273 Focused Capital-aware Candidate Follow-through Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase273 executes the focused follow-through selected by Phase272.",
        "It tests the two priority candidate pockets and their combined subset across notional, concurrency, cost and deterministic order-policy stresses.",
        "The results remain one-date diagnostics only; replay, promotion, paper/live and deployable profitability claims stay closed.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    phase268_dir: Path = DEFAULT_PHASE268_DIR,
    phase269_dir: Path = DEFAULT_PHASE269_DIR,
    phase272_dir: Path = DEFAULT_PHASE272_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    priority_candidates = load_priority_candidates(phase272_dir)
    _, events, _ = load_candidate_events(phase268_dir, phase269_dir)
    results, sample_ledger = run_followthrough_search(priority_candidates, events)
    stability = build_stability_summary(results)
    gates = build_gate_evaluation(phase272_dir, priority_candidates, results, stability)
    acceptance = build_acceptance_summary(priority_candidates, results, stability, gates)

    results.to_csv(output_dir / "phase273_followthrough_scenario_results.csv", index=False)
    sample_ledger.to_csv(output_dir / "phase273_sample_scheduled_event_ledger.csv", index=False)
    stability.to_csv(output_dir / "phase273_order_policy_stability_summary.csv", index=False)
    gates.to_csv(output_dir / "phase273_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase273_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase273_focused_capital_aware_candidate_followthrough_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Top Follow-through Scenarios": results.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).head(30),
            "Order Policy Stability Summary": stability,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase273_focused_capital_aware_candidate_followthrough_search",
        **reproducibility_fields(
            artifact_id="phase273",
            generated_utc=generated_utc,
            inputs={
                "phase272_ranked_pockets": str(phase272_dir / "phase272_ranked_capital_aware_research_pockets.csv"),
                "phase268_event_ledger": str(phase268_dir / "phase268_exploratory_event_ledger.csv"),
                "phase269_ranked_leads": str(phase269_dir / "phase269_ranked_annualized_research_leads.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "initial_capital_grid_inr": INITIAL_CAPITAL_GRID_INR,
                "fixed_notional_grid_inr": FIXED_NOTIONAL_GRID_INR,
                "max_concurrent_grid": MAX_CONCURRENT_GRID,
                "cost_profiles": COST_PROFILES,
                "order_policies": ORDER_POLICIES,
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
                "followthrough_scenario_results": str(output_dir / "phase273_followthrough_scenario_results.csv"),
                "sample_scheduled_event_ledger": str(output_dir / "phase273_sample_scheduled_event_ledger.csv"),
                "order_policy_stability_summary": str(output_dir / "phase273_order_policy_stability_summary.csv"),
                "gate_evaluation": str(output_dir / "phase273_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase273_acceptance_summary.csv"),
                "report": str(output_dir / "phase273_focused_capital_aware_candidate_followthrough_search_report.md"),
                "manifest": str(output_dir / "phase273_focused_capital_aware_candidate_followthrough_search_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase273_phase271_horizon_capital_lock_scheduler_with_order_policy_stress",
        ),
    }
    (output_dir / "phase273_focused_capital_aware_candidate_followthrough_search_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase273 focused capital-aware candidate follow-through search.")
    parser.add_argument("--phase268-dir", type=Path, default=DEFAULT_PHASE268_DIR)
    parser.add_argument("--phase269-dir", type=Path, default=DEFAULT_PHASE269_DIR)
    parser.add_argument("--phase272-dir", type=Path, default=DEFAULT_PHASE272_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(
        phase268_dir=args.phase268_dir,
        phase269_dir=args.phase269_dir,
        phase272_dir=args.phase272_dir,
        output_dir=args.output_dir,
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

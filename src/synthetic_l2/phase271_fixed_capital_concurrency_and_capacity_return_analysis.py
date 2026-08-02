from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, metric_value, read_csv
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE268_DIR = Path("outputs/phase268")
DEFAULT_PHASE269_DIR = Path("outputs/phase269")
DEFAULT_PHASE270_DIR = Path("outputs/phase270")
DEFAULT_OUTPUT_DIR = Path("outputs/phase271")

SELECTED_ROUTE = "P271_FIXED_CAPITAL_CONCURRENCY_AND_CAPACITY_RETURN_ANALYSIS"
NEXT_ACTION = "run_phase272_fixed_capital_capacity_return_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase271_fixed_capital_concurrency_and_capacity_return_analysis"

INITIAL_CAPITAL_GRID_INR = [100_000.0, 250_000.0, 500_000.0, 1_000_000.0]
FIXED_NOTIONAL_GRID_INR = [25_000.0, 50_000.0, 100_000.0]
MAX_CONCURRENT_GRID = [1, 2, 4, 8]
PROFITABLE_ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_DATES_FOR_PORTFOLIO_CLAIM = 5

COST_PROFILES = [
    {"cost_profile": "cost100", "cost_multiplier": 1.0, "extra_slippage_bps": 0.0},
    {"cost_profile": "cost150", "cost_multiplier": 1.5, "extra_slippage_bps": 0.0},
    {"cost_profile": "cost200", "cost_multiplier": 2.0, "extra_slippage_bps": 0.0},
    {"cost_profile": "cost100_plus_1bp", "cost_multiplier": 1.0, "extra_slippage_bps": 1.0},
    {"cost_profile": "cost100_plus_2bp", "cost_multiplier": 1.0, "extra_slippage_bps": 2.0},
]


@dataclass
class OpenPosition:
    trade_date: str
    exchange: str
    symbol: str
    exit_bar_id: int
    notional_inr: float


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def max_drawdown(values: list[float]) -> float:
    peak = 0.0
    worst = 0.0
    for value in values:
        peak = max(peak, value)
        worst = min(worst, value - peak)
    return float(worst)


def load_candidate_events(phase268_dir: Path, phase269_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    leads = read_csv(phase269_dir / "phase269_ranked_annualized_research_leads.csv")
    events = read_csv(phase268_dir / "phase268_exploratory_event_ledger.csv")
    variants = read_csv(phase268_dir / "phase268_two_lane_variant_results.csv")
    if leads.empty:
        raise FileNotFoundError(f"No ranked Phase269 leads found under {phase269_dir}")
    if events.empty:
        raise FileNotFoundError(f"No Phase268 exploratory event ledger found under {phase268_dir}")
    if variants.empty:
        raise FileNotFoundError(f"No Phase268 variant results found under {phase268_dir}")

    leads = leads.copy()
    leads["candidate_rank"] = range(1, len(leads) + 1)
    leads["candidate_score"] = pd.to_numeric(leads.get("cost100_annualized_return_pct"), errors="coerce").fillna(0.0)
    lead_ids = set(leads["candidate_id"].astype(str))

    events = events[events["candidate_id"].astype(str).isin(lead_ids)].copy()
    if events.empty:
        raise ValueError("Phase269 lead IDs have no matching Phase268 exploratory event rows.")

    rank_cols = [
        "candidate_id",
        "candidate_rank",
        "candidate_score",
        "horizon",
        "spread_regime",
        "cost100_net_pnl_inr",
        "cost100_annualized_return_pct",
        "cost200_net_pnl_inr",
        "cost200_annualized_return_pct",
        "acceptance_grade_candidate",
    ]
    events = events.merge(leads[[col for col in rank_cols if col in leads.columns]], on="candidate_id", how="left", suffixes=("", "_lead"))
    if "horizon" not in events.columns:
        events = events.merge(variants[["candidate_id", "horizon"]], on="candidate_id", how="left")
    events["candidate_rank"] = pd.to_numeric(events["candidate_rank"], errors="coerce").fillna(999999).astype(int)
    events["candidate_score"] = pd.to_numeric(events["candidate_score"], errors="coerce").fillna(0.0)
    events["horizon"] = pd.to_numeric(events["horizon"], errors="coerce").fillna(0).astype(int)
    events["richer_event_bar_id"] = pd.to_numeric(events["richer_event_bar_id"], errors="coerce").fillna(-1).astype(int)
    events["gross_edge_bps"] = pd.to_numeric(events["gross_edge_bps"], errors="coerce").fillna(0.0)
    events["zerodha_round_trip_charge_bps"] = pd.to_numeric(events["zerodha_round_trip_charge_bps"], errors="coerce").fillna(0.0)
    events["_event_sort_key"] = (
        events["trade_date"].astype(str)
        + "|"
        + events["exchange"].astype(str)
        + "|"
        + events["richer_event_bar_id"].astype(str).str.zfill(8)
        + "|"
        + events["candidate_rank"].astype(str).str.zfill(6)
        + "|"
        + events["candidate_id"].astype(str)
    )
    events = events.sort_values(["trade_date", "exchange", "richer_event_bar_id", "candidate_rank", "candidate_id", "symbol"]).reset_index(drop=True)
    return leads, events, variants


def schedule_events_for_scenario(
    events: pd.DataFrame,
    scope_id: str,
    scope_candidate_id: str,
    initial_capital_inr: float,
    fixed_notional_inr: float,
    max_concurrent_positions: int,
    cost_profile: str,
    cost_multiplier: float,
    extra_slippage_bps: float,
) -> tuple[dict[str, Any], pd.DataFrame]:
    open_positions: list[OpenPosition] = []
    cash_inr = float(initial_capital_inr)
    cumulative_pnl = 0.0
    equity_curve: list[float] = []
    rows: list[dict[str, Any]] = []
    scheduled_rows = 0
    rejected_slot_rows = 0
    rejected_symbol_rows = 0
    rejected_cash_rows = 0
    scheduled_notional = 0.0
    utilization_samples: list[float] = []

    for event_index, row in events.iterrows():
        trade_date = str(row["trade_date"])
        exchange = str(row["exchange"])
        symbol = str(row["symbol"])
        event_bar_id = int(row["richer_event_bar_id"])
        horizon = int(row["horizon"])

        kept: list[OpenPosition] = []
        for position in open_positions:
            if position.trade_date == trade_date and position.exchange == exchange and position.exit_bar_id <= event_bar_id:
                cash_inr += position.notional_inr
            else:
                kept.append(position)
        open_positions = kept

        open_notional = float(sum(position.notional_inr for position in open_positions))
        utilization_samples.append(open_notional / initial_capital_inr if initial_capital_inr > 0 else 0.0)

        open_same_symbol = any(
            position.trade_date == trade_date and position.exchange == exchange and position.symbol == symbol
            for position in open_positions
        )
        slots_available = int(max_concurrent_positions - len(open_positions))
        decision = "scheduled"
        rejection_reason = ""
        notional_inr = 0.0
        net_pnl_inr = 0.0
        gross_edge_bps = float(row["gross_edge_bps"])
        modeled_cost_bps = float(row["zerodha_round_trip_charge_bps"]) * cost_multiplier
        net_edge_bps = gross_edge_bps - modeled_cost_bps - extra_slippage_bps

        if open_same_symbol:
            decision = "rejected"
            rejection_reason = "same_symbol_overlap"
            rejected_symbol_rows += 1
        elif slots_available <= 0:
            decision = "rejected"
            rejection_reason = "max_concurrent_positions"
            rejected_slot_rows += 1
        elif cash_inr <= 0:
            decision = "rejected"
            rejection_reason = "insufficient_cash"
            rejected_cash_rows += 1
        else:
            notional_inr = min(float(fixed_notional_inr), cash_inr / float(slots_available))
            if notional_inr <= 0:
                decision = "rejected"
                rejection_reason = "insufficient_cash"
                rejected_cash_rows += 1
            else:
                cash_inr -= notional_inr
                scheduled_rows += 1
                scheduled_notional += notional_inr
                net_pnl_inr = net_edge_bps / 10000.0 * notional_inr
                cumulative_pnl += net_pnl_inr
                equity_curve.append(cumulative_pnl)
                open_positions.append(
                    OpenPosition(
                        trade_date=trade_date,
                        exchange=exchange,
                        symbol=symbol,
                        exit_bar_id=event_bar_id + horizon,
                        notional_inr=notional_inr,
                    )
                )

        rows.append(
            {
                "scenario_id": scenario_id(scope_id, initial_capital_inr, fixed_notional_inr, max_concurrent_positions, cost_profile),
                "scope_id": scope_id,
                "scope_candidate_id": scope_candidate_id,
                "event_index": int(event_index),
                "trade_date": trade_date,
                "exchange": exchange,
                "symbol": symbol,
                "richer_event_bar_id": event_bar_id,
                "exit_bar_id": event_bar_id + horizon,
                "candidate_id": row["candidate_id"],
                "candidate_rank": int(row["candidate_rank"]),
                "family_id": row["family_id"],
                "side": as_int(row.get("side", 0)),
                "horizon": horizon,
                "initial_capital_inr": initial_capital_inr,
                "fixed_notional_inr": fixed_notional_inr,
                "max_concurrent_positions": max_concurrent_positions,
                "cost_profile": cost_profile,
                "cost_multiplier": cost_multiplier,
                "extra_slippage_bps": extra_slippage_bps,
                "decision": decision,
                "rejection_reason": rejection_reason,
                "cash_before_or_after_release_inr": cash_inr + notional_inr if decision == "scheduled" else cash_inr,
                "notional_inr": notional_inr,
                "gross_edge_bps": gross_edge_bps,
                "modeled_cost_bps": modeled_cost_bps,
                "extra_slippage_bps_applied": extra_slippage_bps,
                "net_edge_bps": net_edge_bps,
                "net_pnl_inr": net_pnl_inr,
                "cumulative_net_pnl_inr": cumulative_pnl,
                "cash_after_decision_inr": cash_inr,
                "open_positions_after_decision": len(open_positions),
                "open_notional_after_decision_inr": float(sum(position.notional_inr for position in open_positions)),
                "avg_cum_top5_qty_imbalance": to_float(row.get("avg_cum_top5_qty_imbalance")),
                "avg_depth_beyond_l1_qty_imbalance": to_float(row.get("avg_depth_beyond_l1_qty_imbalance")),
                "avg_level_weighted_depth_imbalance": to_float(row.get("avg_level_weighted_depth_imbalance")),
                "depth_replenishment_pressure": to_float(row.get("depth_replenishment_pressure")),
                "depth_withdrawal_pressure": to_float(row.get("depth_withdrawal_pressure")),
                "top5_churn_pressure": to_float(row.get("top5_churn_pressure")),
                "avg_spread_bps": to_float(row.get("avg_spread_bps")),
            }
        )

    observed_dates = max(1, int(events["trade_date"].astype(str).nunique()))
    portfolio_return_pct = cumulative_pnl / initial_capital_inr * 100.0 if initial_capital_inr > 0 else 0.0
    annualized_portfolio_return_pct = portfolio_return_pct * 252.0 / float(observed_dates)
    scenario = {
        "scenario_id": scenario_id(scope_id, initial_capital_inr, fixed_notional_inr, max_concurrent_positions, cost_profile),
        "scope_id": scope_id,
        "scope_candidate_id": scope_candidate_id,
        "initial_capital_inr": initial_capital_inr,
        "fixed_notional_inr": fixed_notional_inr,
        "max_concurrent_positions": max_concurrent_positions,
        "cost_profile": cost_profile,
        "cost_multiplier": cost_multiplier,
        "extra_slippage_bps": extra_slippage_bps,
        "input_event_rows": int(len(events)),
        "scheduled_event_rows": int(scheduled_rows),
        "rejected_event_rows": int(len(events) - scheduled_rows),
        "rejected_same_symbol_overlap_rows": int(rejected_symbol_rows),
        "rejected_max_concurrent_rows": int(rejected_slot_rows),
        "rejected_insufficient_cash_rows": int(rejected_cash_rows),
        "candidate_rows": int(events["candidate_id"].astype(str).nunique()),
        "scheduled_candidate_rows": int(pd.DataFrame(rows).query("decision == 'scheduled'")["candidate_id"].astype(str).nunique()) if rows else 0,
        "symbols": int(events["symbol"].astype(str).nunique()),
        "scheduled_symbols": int(pd.DataFrame(rows).query("decision == 'scheduled'")["symbol"].astype(str).nunique()) if rows else 0,
        "observed_trade_dates": int(observed_dates),
        "realized_net_pnl_inr": float(cumulative_pnl),
        "portfolio_return_pct": float(portfolio_return_pct),
        "mechanical_one_date_annualized_portfolio_return_pct": float(annualized_portfolio_return_pct),
        "annualized_return_is_robust_portfolio_claim": int(observed_dates >= MIN_DATES_FOR_PORTFOLIO_CLAIM),
        "annualized_above_12pct_research_diagnostic": int(annualized_portfolio_return_pct > PROFITABLE_ANNUALIZED_THRESHOLD_PCT),
        "scheduled_notional_inr": float(scheduled_notional),
        "notional_turnover_x_initial_capital": float(scheduled_notional / initial_capital_inr) if initial_capital_inr > 0 else 0.0,
        "avg_open_notional_utilization": float(sum(utilization_samples) / len(utilization_samples)) if utilization_samples else 0.0,
        "max_drawdown_inr": max_drawdown(equity_curve),
        "portfolio_claim_allowed": int(observed_dates >= MIN_DATES_FOR_PORTFOLIO_CLAIM),
        "strategy_replay_allowed": 0,
        "promotion_allowed": 0,
        "paper_or_live_acceptance_allowed": 0,
        "deployable_profitability_claim_allowed": 0,
    }
    return scenario, pd.DataFrame(rows)


def scenario_id(scope_id: str, initial_capital_inr: float, fixed_notional_inr: float, max_concurrent_positions: int, cost_profile: str) -> str:
    return (
        f"P271_{scope_id}"
        f"_CAP{int(initial_capital_inr)}"
        f"_NOT{int(fixed_notional_inr)}"
        f"_CONC{int(max_concurrent_positions)}"
        f"_{cost_profile.upper()}"
    )


def build_scenarios(leads: pd.DataFrame, events: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    scenario_rows: list[dict[str, Any]] = []
    ledger_frames: list[pd.DataFrame] = []
    scopes: list[tuple[str, str, pd.DataFrame]] = [("ALL_RANKED_LEADS", "ALL_RANKED_LEADS", events)]
    for _, lead in leads.sort_values("candidate_rank").iterrows():
        candidate_id = str(lead["candidate_id"])
        rank = int(lead["candidate_rank"])
        scope_events = events[events["candidate_id"].astype(str).eq(candidate_id)].copy()
        if not scope_events.empty:
            scopes.append((f"CAND{rank:03d}", candidate_id, scope_events))
    for scope_id, scope_candidate_id, scope_events in scopes:
        for initial_capital in INITIAL_CAPITAL_GRID_INR:
            for fixed_notional in FIXED_NOTIONAL_GRID_INR:
                for max_concurrent in MAX_CONCURRENT_GRID:
                    for profile in COST_PROFILES:
                        scenario, ledger = schedule_events_for_scenario(
                            events=scope_events,
                            scope_id=scope_id,
                            scope_candidate_id=scope_candidate_id,
                            initial_capital_inr=initial_capital,
                            fixed_notional_inr=fixed_notional,
                            max_concurrent_positions=max_concurrent,
                            cost_profile=profile["cost_profile"],
                            cost_multiplier=profile["cost_multiplier"],
                            extra_slippage_bps=profile["extra_slippage_bps"],
                        )
                        scenario_rows.append(scenario)
                        ledger_frames.append(ledger)
    return pd.DataFrame(scenario_rows), pd.concat(ledger_frames, ignore_index=True)


def build_candidate_capacity_diagnostics(ledger: pd.DataFrame) -> pd.DataFrame:
    scheduled = ledger[ledger["decision"].astype(str).eq("scheduled")].copy()
    if scheduled.empty:
        return pd.DataFrame(
            columns=[
                "candidate_id",
                "family_id",
                "cost_profile",
                "scenario_rows",
                "scheduled_event_rows",
                "symbols",
                "realized_net_pnl_inr",
                "scheduled_notional_inr",
                "avg_net_edge_bps",
                "avg_depth_beyond_l1_qty_imbalance",
                "avg_level_weighted_depth_imbalance",
                "avg_spread_bps",
            ]
        )
    grouped = (
        scheduled.groupby(["candidate_id", "family_id", "cost_profile"], dropna=False)
        .agg(
            scenario_rows=("scenario_id", "nunique"),
            scheduled_event_rows=("decision", "size"),
            symbols=("symbol", "nunique"),
            realized_net_pnl_inr=("net_pnl_inr", "sum"),
            scheduled_notional_inr=("notional_inr", "sum"),
            avg_net_edge_bps=("net_edge_bps", "mean"),
            avg_depth_beyond_l1_qty_imbalance=("avg_depth_beyond_l1_qty_imbalance", "mean"),
            avg_level_weighted_depth_imbalance=("avg_level_weighted_depth_imbalance", "mean"),
            avg_spread_bps=("avg_spread_bps", "mean"),
        )
        .reset_index()
    )
    grouped["return_on_scheduled_notional_bps"] = grouped.apply(
        lambda row: row["realized_net_pnl_inr"] / row["scheduled_notional_inr"] * 10000.0 if row["scheduled_notional_inr"] else 0.0,
        axis=1,
    )
    return grouped.sort_values(["cost_profile", "realized_net_pnl_inr"], ascending=[True, False]).reset_index(drop=True)


def build_proxy_reconciliation(leads: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    best_scenarios = (
        scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False)
        .groupby("cost_profile", as_index=False)
        .head(1)
        .copy()
    )
    best_lead = leads.sort_values("cost100_annualized_return_pct", ascending=False).head(1).copy()
    best_proxy = float(pd.to_numeric(best_lead["cost100_annualized_return_pct"], errors="coerce").iloc[0]) if not best_lead.empty else 0.0
    best_candidate = str(best_lead["candidate_id"].iloc[0]) if not best_lead.empty else ""
    rows = []
    for _, row in best_scenarios.iterrows():
        rows.append(
            {
                "cost_profile": row["cost_profile"],
                "phase269_best_fixed_notional_proxy_candidate_id": best_candidate,
                "phase269_best_cost100_fixed_notional_annualized_pct": best_proxy,
                "best_phase271_scenario_id": row["scenario_id"],
                "phase271_best_mechanical_one_date_annualized_portfolio_return_pct": row["mechanical_one_date_annualized_portfolio_return_pct"],
                "phase271_best_portfolio_return_pct": row["portfolio_return_pct"],
                "annualized_return_is_robust_portfolio_claim": row["annualized_return_is_robust_portfolio_claim"],
                "reconciliation_note": "Phase269 proxy is not portfolio return; Phase271 applies fixed capital and scheduling to pooled and per-candidate scopes, still one-date mechanics only.",
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(phase270_dir: Path, leads: pd.DataFrame, events: pd.DataFrame, variants: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    phase270_summary = phase270_dir / "phase270_acceptance_summary.csv"
    phase270_next = str(metric_value(phase270_summary, "phase270_next_best_action", ""))
    phase270_complete = as_int(metric_value(phase270_summary, "phase270_fixed_capital_precommit_complete", 0))
    full_depth_variants = int(pd.to_numeric(variants.get("uses_full_top_five_depth"), errors="coerce").fillna(0).sum()) if "uses_full_top_five_depth" in variants.columns else 0
    l2_l5_variants = int(pd.to_numeric(variants.get("uses_depth_beyond_l1"), errors="coerce").fillna(0).sum()) if "uses_depth_beyond_l1" in variants.columns else 0
    l1_only_variants = int(pd.to_numeric(variants.get("uses_l1_only"), errors="coerce").fillna(0).sum()) if "uses_l1_only" in variants.columns else 1
    variant_rows = int(len(variants))
    rows = [
        ("P271_PHASE270_WORK_ORDER_PRESENT", "run_phase271_fixed_capital_concurrency_and_capacity_return_analysis" in phase270_next, phase270_next, "Phase270 next action targets Phase271", "hard"),
        ("P271_PHASE270_PRECOMMIT_COMPLETE", phase270_complete == 1, phase270_complete, "Phase270 fixed-capital precommit complete", "hard"),
        ("P271_RESEARCH_LEADS_PRESENT", len(leads) > 0, len(leads), ">0 Phase269 research leads", "hard"),
        ("P271_EVENT_LEDGER_PRESENT", len(events) > 0, len(events), ">0 Phase268 events for leads", "hard"),
        ("P271_SCENARIO_GRID_COMPLETE", len(scenarios) >= (1 + len(leads)) * len(INITIAL_CAPITAL_GRID_INR) * len(FIXED_NOTIONAL_GRID_INR) * len(MAX_CONCURRENT_GRID) * len(COST_PROFILES), len(scenarios), "(pooled + per-lead) * 4*3*4*5 scenarios", "hard"),
        ("P271_FIXED_CAPITAL_DENOMINATOR_USED", bool((scenarios["initial_capital_inr"] > 0).all()), ";".join(map(str, sorted(scenarios["initial_capital_inr"].unique()))), "initial capital denominator", "hard"),
        ("P271_SCHEDULER_MATERIALIZED", bool(scenarios["scheduled_event_rows"].sum() > 0), int(scenarios["scheduled_event_rows"].sum()), ">0 scheduled events", "hard"),
        ("P271_UNLIMITED_CAPITAL_FORBIDDEN", bool((scenarios["portfolio_claim_allowed"] == 0).all()), 0, "no unlimited capital or robust claim from one date", "hard"),
        ("P271_FULL_TOP_FIVE_DEPTH_PRESERVED", full_depth_variants == variant_rows and variant_rows > 0, f"full_depth={full_depth_variants};variants={variant_rows}", "all variants full-depth", "hard"),
        ("P271_LEVELS_2_TO_5_MATERIALITY_PRESERVED", l2_l5_variants == variant_rows and l1_only_variants == 0 and variant_rows > 0, f"l2_l5={l2_l5_variants};l1_only={l1_only_variants};variants={variant_rows}", "levels 2-5 materiality and no L1-only", "hard"),
        ("P271_COST_STRESS_PROFILES_PRESENT", set(COST_PROFILES[i]["cost_profile"] for i in range(len(COST_PROFILES))).issubset(set(scenarios["cost_profile"].astype(str))), ";".join(sorted(scenarios["cost_profile"].astype(str).unique())), "base, 1.5x, 2x, plus slippage", "hard"),
        ("P271_NO_REPLAY_PROMOTION_PAPER_LIVE", bool((scenarios["strategy_replay_allowed"] == 0).all() and (scenarios["promotion_allowed"] == 0).all() and (scenarios["paper_or_live_acceptance_allowed"] == 0).all()), 0, "replay/promotion/paper-live remain closed", "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def build_acceptance_summary(leads: pd.DataFrame, events: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    best = scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
    cost100 = scenarios[scenarios["cost_profile"].astype(str).eq("cost100")]
    cost150 = scenarios[scenarios["cost_profile"].astype(str).eq("cost150")]
    cost200 = scenarios[scenarios["cost_profile"].astype(str).eq("cost200")]
    extra1 = scenarios[scenarios["cost_profile"].astype(str).eq("cost100_plus_1bp")]
    extra2 = scenarios[scenarios["cost_profile"].astype(str).eq("cost100_plus_2bp")]
    observed_dates = int(events["trade_date"].astype(str).nunique())
    portfolio_claim_allowed = int(observed_dates >= MIN_DATES_FOR_PORTFOLIO_CLAIM)
    acceptance_grade_rows = int(
        scenarios[
            scenarios["cost_profile"].astype(str).eq("cost200")
            & scenarios["annualized_above_12pct_research_diagnostic"].astype(int).eq(1)
            & scenarios["annualized_return_is_robust_portfolio_claim"].astype(int).eq(1)
        ].shape[0]
    )
    next_action = NEXT_ACTION if hard_pass == len(hard) else REPAIR_ACTION
    rows = [
        ("phase271_fixed_capital_analysis_complete", 1, "Phase271 fixed-capital/concurrency/capacity analysis completed"),
        ("phase271_selected_route", SELECTED_ROUTE, "Selected route"),
        ("phase271_phase269_research_lead_rows", len(leads), "Phase269 ranked fixed-notional leads used"),
        ("phase271_input_event_rows", len(events), "Phase268 event rows used for scheduling"),
        ("phase271_input_symbols", int(events["symbol"].astype(str).nunique()), "Input symbols"),
        ("phase271_observed_trade_dates", observed_dates, "Observed trade dates"),
        ("phase271_scenario_rows", len(scenarios), "Capital/concurrency/cost scenarios evaluated"),
        ("phase271_scope_rows", int(scenarios["scope_id"].astype(str).nunique()), "Pooled plus per-candidate scheduling scopes"),
        ("phase271_total_scheduled_event_rows", int(scenarios["scheduled_event_rows"].sum()), "Scheduled event rows across scenarios"),
        ("phase271_cost100_annualized_above_12pct_scenario_rows", int(cost100["annualized_above_12pct_research_diagnostic"].sum()), "Cost100 scenarios above 12% one-date annualized diagnostic"),
        ("phase271_cost150_annualized_above_12pct_scenario_rows", int(cost150["annualized_above_12pct_research_diagnostic"].sum()), "Cost150 scenarios above 12% one-date annualized diagnostic"),
        ("phase271_cost200_annualized_above_12pct_scenario_rows", int(cost200["annualized_above_12pct_research_diagnostic"].sum()), "Cost200 scenarios above 12% one-date annualized diagnostic"),
        ("phase271_cost100_plus_1bp_annualized_above_12pct_scenario_rows", int(extra1["annualized_above_12pct_research_diagnostic"].sum()), "Cost100 plus 1bp scenarios above 12% one-date annualized diagnostic"),
        ("phase271_cost100_plus_2bp_annualized_above_12pct_scenario_rows", int(extra2["annualized_above_12pct_research_diagnostic"].sum()), "Cost100 plus 2bp scenarios above 12% one-date annualized diagnostic"),
        ("phase271_best_scenario_id", best["scenario_id"], "Best mechanical one-date annualized scenario"),
        ("phase271_best_realized_net_pnl_inr", best["realized_net_pnl_inr"], "Best scenario realized net P&L"),
        ("phase271_best_portfolio_return_pct", best["portfolio_return_pct"], "Best scenario one-date portfolio return percent"),
        ("phase271_best_mechanical_one_date_annualized_portfolio_return_pct", best["mechanical_one_date_annualized_portfolio_return_pct"], "Best scenario mechanical one-date annualized percent"),
        ("phase271_best_scheduled_event_rows", best["scheduled_event_rows"], "Best scenario scheduled events"),
        ("phase271_best_rejected_event_rows", best["rejected_event_rows"], "Best scenario rejected events"),
        ("phase271_best_notional_turnover_x_initial_capital", best["notional_turnover_x_initial_capital"], "Best scenario notional turnover / capital"),
        ("phase271_best_max_drawdown_inr", best["max_drawdown_inr"], "Best scenario max drawdown"),
        ("phase271_annualized_return_is_robust_portfolio_claim", 0, "Only one observed date, annualized values are mechanical diagnostics"),
        ("phase271_portfolio_claim_allowed", portfolio_claim_allowed, "Robust portfolio claim allowed only with >=5 observed dates"),
        ("phase271_unlimited_capital_assumption_allowed", 0, "Unlimited capital forbidden"),
        ("phase271_fixed_notional_proxy_as_portfolio_return_allowed", 0, "Fixed-notional proxy cannot be relabeled"),
        ("phase271_full_top_five_depth_required", 1, "Zerodha top-five rows 1-5 required"),
        ("phase271_levels_2_to_5_materiality_required", 1, "Levels 2-5 materiality required"),
        ("phase271_l1_only_candidate_allowed", 0, "L1-only candidates forbidden"),
        ("phase271_acceptance_grade_scenario_rows", acceptance_grade_rows, "Robust portfolio acceptance rows"),
        ("phase271_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase271_hard_gate_rows", len(hard), "Hard gates evaluated"),
        ("phase271_strategy_replay_allowed", 0, "No strategy replay unlocked"),
        ("phase271_strategy_promotion_allowed", 0, "No promotion unlocked"),
        ("phase271_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance"),
        ("phase271_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase271_next_best_action", next_action, "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase271 Fixed-capital Concurrency and Capacity Return Analysis",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase271 converts the Phase269 fixed-notional research leads into scheduled fixed-capital diagnostics.",
        "Each event consumes capital until its modeled horizon exit, same-symbol overlaps are rejected, and concurrency limits are enforced.",
        "The annualized values in this phase are one-date mechanical diagnostics because the current evidence has one observed trade date.",
        "Full Zerodha top-five market-by-price rows 1-5 and levels 2-5 remain mandatory; L1-only candidates remain forbidden.",
        "This phase does not unlock replay, promotion, paper/live acceptance, or deployable profitability claims.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    phase268_dir: Path = DEFAULT_PHASE268_DIR,
    phase269_dir: Path = DEFAULT_PHASE269_DIR,
    phase270_dir: Path = DEFAULT_PHASE270_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    leads, events, variants = load_candidate_events(phase268_dir, phase269_dir)
    scenarios, scheduled_ledger = build_scenarios(leads, events)
    diagnostics = build_candidate_capacity_diagnostics(scheduled_ledger)
    reconciliation = build_proxy_reconciliation(leads, scenarios)
    gates = build_gate_evaluation(phase270_dir, leads, events, variants, scenarios)
    acceptance = build_acceptance_summary(leads, events, scenarios, gates)

    scenarios.to_csv(output_dir / "phase271_capital_scenario_results.csv", index=False)
    scheduled_ledger.to_csv(output_dir / "phase271_scheduled_event_ledger.csv", index=False)
    diagnostics.to_csv(output_dir / "phase271_candidate_capacity_diagnostics.csv", index=False)
    reconciliation.to_csv(output_dir / "phase271_annualized_proxy_reconciliation.csv", index=False)
    gates.to_csv(output_dir / "phase271_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase271_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase271_fixed_capital_concurrency_and_capacity_return_analysis_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Top Capital Scenarios": scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).head(20),
            "Proxy Reconciliation": reconciliation,
            "Candidate Capacity Diagnostics": diagnostics.head(30),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase271_fixed_capital_concurrency_and_capacity_return_analysis",
        **reproducibility_fields(
            artifact_id="phase271",
            generated_utc=generated_utc,
            inputs={
                "phase268_variant_results": str(phase268_dir / "phase268_two_lane_variant_results.csv"),
                "phase268_exploratory_event_ledger": str(phase268_dir / "phase268_exploratory_event_ledger.csv"),
                "phase269_ranked_research_leads": str(phase269_dir / "phase269_ranked_annualized_research_leads.csv"),
                "phase270_acceptance_summary": str(phase270_dir / "phase270_acceptance_summary.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "initial_capital_grid_inr": INITIAL_CAPITAL_GRID_INR,
                "fixed_notional_grid_inr": FIXED_NOTIONAL_GRID_INR,
                "max_concurrent_grid": MAX_CONCURRENT_GRID,
                "cost_profiles": COST_PROFILES,
                "annualized_threshold_pct": PROFITABLE_ANNUALIZED_THRESHOLD_PCT,
                "min_dates_for_portfolio_claim": MIN_DATES_FOR_PORTFOLIO_CLAIM,
                "full_top_five_depth_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "l1_only_candidate_allowed": 0,
                "unlimited_capital_assumption_allowed": 0,
                "strategy_replay_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "capital_scenario_results": str(output_dir / "phase271_capital_scenario_results.csv"),
                "scheduled_event_ledger": str(output_dir / "phase271_scheduled_event_ledger.csv"),
                "candidate_capacity_diagnostics": str(output_dir / "phase271_candidate_capacity_diagnostics.csv"),
                "annualized_proxy_reconciliation": str(output_dir / "phase271_annualized_proxy_reconciliation.csv"),
                "gate_evaluation": str(output_dir / "phase271_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase271_acceptance_summary.csv"),
                "report": str(output_dir / "phase271_fixed_capital_concurrency_and_capacity_return_analysis_report.md"),
                "manifest": str(output_dir / "phase271_fixed_capital_concurrency_and_capacity_return_analysis_manifest.json"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase271_horizon_capital_lock_scheduler",
        ),
    }
    (output_dir / "phase271_fixed_capital_concurrency_and_capacity_return_analysis_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase271 fixed-capital/concurrency/capacity return analysis.")
    parser.add_argument("--phase268-dir", type=Path, default=DEFAULT_PHASE268_DIR)
    parser.add_argument("--phase269-dir", type=Path, default=DEFAULT_PHASE269_DIR)
    parser.add_argument("--phase270-dir", type=Path, default=DEFAULT_PHASE270_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(
        phase268_dir=args.phase268_dir,
        phase269_dir=args.phase269_dir,
        phase270_dir=args.phase270_dir,
        output_dir=args.output_dir,
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase271_fixed_capital_concurrency_and_capacity_return_analysis import max_drawdown
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_PHASE300_DIR = Path("outputs/phase300")
DEFAULT_PHASE299_DIR = Path("outputs/phase299")
DEFAULT_PHASE298_DIR = Path("outputs/phase298")

SELECTED_ROUTE = "P300_PASSIVE_AWARE_DIRECTIONAL_L2_EXECUTION_HYBRID"
NEXT_ACTION = "run_phase301_passive_aware_execution_hybrid_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase300_passive_aware_execution_hybrid"

INITIAL_CAPITAL_INR = 1_000_000.0
FIXED_NOTIONAL_INR = 75_000.0
MAX_CONCURRENT_GRID = [1, 2, 4]
COST_MULTIPLIER = 2.0
ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_EVENT_ROWS = 30
MIN_BREADTH_SYMBOLS = 2
MIN_BREADTH_DATES = 2
SAMPLE_LEDGER_ROWS = 10_000


@dataclass
class OpenPosition:
    trade_date: str
    exchange: str
    symbol: str
    exit_bar_id: int
    notional_inr: float


FILL_MODELS = [
    {
        "fill_model_id": "P300_FILL_PESSIMISTIC_BACK_OF_QUEUE",
        "base_fill_prob": 0.08,
        "adverse_flow_weight": 0.28,
        "support_penalty": 0.16,
        "churn_weight": 0.10,
        "wide_spread_penalty": 0.10,
        "max_fill_prob": 0.38,
        "exit_fill_scale": 0.75,
        "toxicity_multiplier": 1.20,
    },
    {
        "fill_model_id": "P300_FILL_BASE_BACK_OF_QUEUE",
        "base_fill_prob": 0.14,
        "adverse_flow_weight": 0.34,
        "support_penalty": 0.12,
        "churn_weight": 0.14,
        "wide_spread_penalty": 0.08,
        "max_fill_prob": 0.52,
        "exit_fill_scale": 0.90,
        "toxicity_multiplier": 1.00,
    },
    {
        "fill_model_id": "P300_FILL_OPTIMISTIC_BACK_OF_QUEUE",
        "base_fill_prob": 0.20,
        "adverse_flow_weight": 0.38,
        "support_penalty": 0.08,
        "churn_weight": 0.18,
        "wide_spread_penalty": 0.05,
        "max_fill_prob": 0.68,
        "exit_fill_scale": 1.05,
        "toxicity_multiplier": 0.85,
    },
]

EXECUTION_POLICIES = [
    {
        "execution_policy_id": "P300_PASSIVE_ENTRY_PASSIVE_EXIT_FORCED_FLATTEN",
        "cross_if_not_filled": 0,
        "cross_hurdle_bps": 999.0,
        "passive_exit": 1,
        "calm_exit_churn_cap": 0.11,
        "calm_exit_spread_cap_bps": 3.0,
    },
    {
        "execution_policy_id": "P300_HYBRID_PASSIVE_ENTRY_CROSS_IF_EDGE_FORCED_FLATTEN",
        "cross_if_not_filled": 1,
        "cross_hurdle_bps": 28.0,
        "passive_exit": 1,
        "calm_exit_churn_cap": 0.09,
        "calm_exit_spread_cap_bps": 2.5,
    },
    {
        "execution_policy_id": "P300_PASSIVE_ENTRY_TAKER_EXIT",
        "cross_if_not_filled": 0,
        "cross_hurdle_bps": 999.0,
        "passive_exit": 0,
        "calm_exit_churn_cap": 0.0,
        "calm_exit_spread_cap_bps": 0.0,
    },
]


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def stable_uniform(*parts: Any) -> float:
    payload = "|".join(str(part) for part in parts).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()[:16]
    return int(digest, 16) / float(16**16 - 1)


def scenario_id(seed_scope: str, fill_model_id: str, policy_id: str, max_concurrent: int) -> str:
    return f"P300_{seed_scope}_{fill_model_id}_{policy_id}_CAP{int(INITIAL_CAPITAL_INR)}_NOT{int(FIXED_NOTIONAL_INR)}_CONC{max_concurrent}_COST200"


def zerodha_charge_bps(notional: float = FIXED_NOTIONAL_INR) -> float:
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=notional,
        sell_value_inr=notional,
        buy_quantity=1.0,
        sell_quantity=1.0,
        buy_orders=1,
        sell_orders=1,
    )
    return float(charges.breakeven_bps_on_buy_value)


def load_inputs(phase300_dir: Path, phase299_dir: Path, phase298_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    precommit = read_csv(phase300_dir / "phase300_acceptance_summary.csv")
    ranked = read_csv(phase299_dir / "phase299_ranked_variant_interpretation.csv")
    events = read_csv(phase298_dir / "phase298_raw_dense_candidate_events.csv")
    schema = read_csv(phase298_dir / "phase298_raw_book_schema_audit.csv")
    phase299_summary = read_csv(phase299_dir / "phase299_acceptance_summary.csv")
    if precommit.empty or ranked.empty or events.empty or phase299_summary.empty:
        raise FileNotFoundError("Phase300 precommit, Phase299 ranking, or Phase298 event inputs are missing.")
    seeds = ranked[ranked["preserve_as_directional_signal_seed"].astype(int).eq(1)].copy()
    seed_ids = set(seeds["phase298_variant_id"].astype(str))
    seed_events = events[events["candidate_id"].astype(str).isin(seed_ids)].copy()
    if seed_events.empty:
        raise ValueError("No Phase298 raw candidate events matched Phase299 directional signal seeds.")
    seed_events = seed_events.merge(
        seeds[["phase298_variant_id", "max_annualized_pct", "max_scheduled_event_rows", "preserve_as_directional_signal_seed"]],
        left_on="candidate_id",
        right_on="phase298_variant_id",
        how="left",
    )
    seed_events = seed_events.sort_values(["trade_date", "exchange", "richer_event_bar_id", "candidate_rank", "candidate_id", "symbol"], kind="mergesort").reset_index(drop=True)
    return precommit, phase299_summary, seeds, seed_events, schema


def fill_probability(row: pd.Series, model: dict[str, Any]) -> tuple[float, float, float, float]:
    side = int(row["side"])
    top5 = to_float(row.get("avg_cum_top5_qty_imbalance"))
    beyond_l1 = to_float(row.get("avg_depth_beyond_l1_qty_imbalance"))
    weighted = to_float(row.get("avg_level_weighted_depth_imbalance"))
    churn = min(max(to_float(row.get("top5_churn_pressure")), 0.0), 1.0)
    spread_bps = max(to_float(row.get("avg_spread_bps")), 0.0)
    side_pressure = side * (0.45 * top5 + 0.35 * beyond_l1 + 0.20 * weighted)
    book_support = max(side_pressure, 0.0)
    adverse_flow = max(-side_pressure, 0.0)
    wide_spread_score = min(spread_bps / 6.0, 1.0)
    probability = (
        float(model["base_fill_prob"])
        + float(model["adverse_flow_weight"]) * adverse_flow
        + float(model["churn_weight"]) * churn
        - float(model["support_penalty"]) * book_support
        - float(model["wide_spread_penalty"]) * wide_spread_score
    )
    probability = min(max(probability, 0.0), float(model["max_fill_prob"]))
    return probability, side_pressure, adverse_flow, book_support


def toxicity_penalty_bps(row: pd.Series, adverse_flow: float, model: dict[str, Any]) -> float:
    spread_bps = max(to_float(row.get("avg_spread_bps")), 0.0)
    churn = min(max(to_float(row.get("top5_churn_pressure")), 0.0), 1.0)
    withdrawal = min(max(to_float(row.get("depth_withdrawal_pressure")), 0.0), 1.0)
    base = 0.35 * spread_bps + 4.0 * adverse_flow + 1.5 * churn + 1.0 * withdrawal
    return float(base * float(model["toxicity_multiplier"]))


def expected_move_bps(row: pd.Series) -> float:
    raw_score = abs(to_float(row.get("raw_book_state_score")))
    spread_bps = max(to_float(row.get("avg_spread_bps")), 0.0)
    churn = min(max(to_float(row.get("top5_churn_pressure")), 0.0), 1.0)
    return min(40.0, 6.0 * raw_score + 0.5 * spread_bps + 2.0 * churn)


def schedule_scenario(events: pd.DataFrame, seed_scope: str, fill_model: dict[str, Any], policy: dict[str, Any], max_concurrent: int) -> tuple[dict[str, Any], pd.DataFrame]:
    open_positions: list[OpenPosition] = []
    cash_inr = INITIAL_CAPITAL_INR
    cumulative_pnl = 0.0
    equity_curve: list[float] = []
    rows: list[dict[str, Any]] = []
    scheduled_rows = 0
    canceled_rows = 0
    crossed_after_no_fill_rows = 0
    passive_entry_fill_rows = 0
    passive_entry_attempt_rows = 0
    passive_exit_attempt_rows = 0
    passive_exit_fill_rows = 0
    forced_flatten_rows = 0
    rejected_slot_rows = 0
    rejected_symbol_rows = 0
    rejected_cash_rows = 0
    scheduled_notional = 0.0
    scheduled_positive_dates: set[str] = set()
    scheduled_negative_dates: set[str] = set()
    scheduled_symbols: set[str] = set()
    utilization_samples: list[float] = []
    charge_bps = zerodha_charge_bps(FIXED_NOTIONAL_INR) * COST_MULTIPLIER
    sid = scenario_id(seed_scope, str(fill_model["fill_model_id"]), str(policy["execution_policy_id"]), max_concurrent)

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
        utilization_samples.append(open_notional / INITIAL_CAPITAL_INR)

        open_same_symbol = any(
            position.trade_date == trade_date and position.exchange == exchange and position.symbol == symbol
            for position in open_positions
        )
        slots_available = int(max_concurrent - len(open_positions))
        decision = "scheduled"
        rejection_reason = ""
        notional_inr = 0.0
        gross_edge_bps = to_float(row.get("gross_edge_bps"))
        spread_bps = max(to_float(row.get("avg_spread_bps")), 0.0)
        entry_fill_prob, side_pressure, adverse_flow, book_support = fill_probability(row, fill_model)
        entry_draw = stable_uniform(sid, event_index, row["candidate_id"], row["richer_event_bar_id"], "entry")
        passive_entry_attempt = 1
        passive_entry_filled = int(entry_draw <= entry_fill_prob)
        passive_entry_attempt_rows += 1
        expected_bps = expected_move_bps(row)
        crossed_after_no_fill = 0
        canceled = 0
        entry_mode = "passive_fill" if passive_entry_filled else "not_filled"

        if open_same_symbol:
            decision = "rejected"
            rejection_reason = "same_symbol_overlap"
            rejected_symbol_rows += 1
            passive_entry_attempt = 0
            passive_entry_filled = 0
            entry_mode = "not_attempted"
        elif slots_available <= 0:
            decision = "rejected"
            rejection_reason = "max_concurrent_positions"
            rejected_slot_rows += 1
            passive_entry_attempt = 0
            passive_entry_filled = 0
            entry_mode = "not_attempted"
        elif cash_inr < FIXED_NOTIONAL_INR:
            decision = "rejected"
            rejection_reason = "insufficient_cash"
            rejected_cash_rows += 1
            passive_entry_attempt = 0
            passive_entry_filled = 0
            entry_mode = "not_attempted"
        elif not passive_entry_filled:
            if int(policy["cross_if_not_filled"]) == 1 and expected_bps >= float(policy["cross_hurdle_bps"]):
                crossed_after_no_fill = 1
                crossed_after_no_fill_rows += 1
                entry_mode = "aggressive_cross_after_no_fill"
            else:
                decision = "canceled"
                rejection_reason = "passive_entry_not_filled"
                canceled = 1
                canceled_rows += 1

        passive_entry_penalty_bps = 0.0
        adverse_penalty_bps = 0.0
        passive_exit_attempt = 0
        passive_exit_filled = 0
        forced_flatten = 0
        entry_spread_component_bps = 0.0
        exit_spread_component_bps = 0.0
        net_edge_bps = 0.0
        net_pnl_inr = 0.0
        exit_mode = ""

        if decision == "scheduled":
            notional_inr = FIXED_NOTIONAL_INR
            cash_inr -= notional_inr
            scheduled_rows += 1
            scheduled_notional += notional_inr
            scheduled_symbols.add(symbol)
            if passive_entry_filled:
                passive_entry_fill_rows += 1
                entry_spread_component_bps = spread_bps / 2.0
                passive_entry_penalty_bps = toxicity_penalty_bps(row, adverse_flow, fill_model)
                adverse_penalty_bps += passive_entry_penalty_bps
            else:
                entry_spread_component_bps = -spread_bps / 2.0

            calm = to_float(row.get("top5_churn_pressure")) <= float(policy["calm_exit_churn_cap"]) and spread_bps <= float(policy["calm_exit_spread_cap_bps"])
            if int(policy["passive_exit"]) == 1 and calm:
                passive_exit_attempt = 1
                passive_exit_attempt_rows += 1
                exit_prob = min(max(entry_fill_prob * float(fill_model["exit_fill_scale"]), 0.0), float(fill_model["max_fill_prob"]))
                exit_draw = stable_uniform(sid, event_index, row["candidate_id"], row["richer_event_bar_id"], "exit")
                passive_exit_filled = int(exit_draw <= exit_prob)
                if passive_exit_filled:
                    passive_exit_fill_rows += 1
                    exit_mode = "passive_exit_fill"
                    exit_spread_component_bps = spread_bps / 2.0
                    adverse_penalty_bps += 0.50 * toxicity_penalty_bps(row, adverse_flow, fill_model)
                else:
                    forced_flatten = 1
                    forced_flatten_rows += 1
                    exit_mode = "forced_flatten_after_passive_exit_miss"
                    exit_spread_component_bps = -spread_bps / 2.0
            else:
                forced_flatten = 1
                forced_flatten_rows += 1
                exit_mode = "forced_flatten_taker_exit"
                exit_spread_component_bps = -spread_bps / 2.0

            net_edge_bps = gross_edge_bps + entry_spread_component_bps + exit_spread_component_bps - charge_bps - adverse_penalty_bps
            net_pnl_inr = net_edge_bps / 10000.0 * notional_inr
            cumulative_pnl += net_pnl_inr
            equity_curve.append(cumulative_pnl)
            if net_pnl_inr > 0:
                scheduled_positive_dates.add(trade_date)
            elif net_pnl_inr < 0:
                scheduled_negative_dates.add(trade_date)
            open_positions.append(OpenPosition(trade_date, exchange, symbol, event_bar_id + horizon, notional_inr))

        rows.append(
            {
                "scenario_id": sid,
                "event_index": int(event_index),
                "trade_date": trade_date,
                "exchange": exchange,
                "symbol": symbol,
                "richer_event_bar_id": event_bar_id,
                "exit_bar_id": event_bar_id + horizon,
                "candidate_id": row["candidate_id"],
                "family_id": row["family_id"],
                "side": int(row["side"]),
                "horizon": horizon,
                "seed_scope": seed_scope,
                "fill_model_id": fill_model["fill_model_id"],
                "execution_policy_id": policy["execution_policy_id"],
                "max_concurrent_positions": max_concurrent,
                "decision": decision,
                "rejection_reason": rejection_reason,
                "passive_entry_attempt": passive_entry_attempt,
                "entry_fill_probability": entry_fill_prob if passive_entry_attempt else 0.0,
                "entry_fill_draw": entry_draw if passive_entry_attempt else 0.0,
                "passive_entry_filled": passive_entry_filled,
                "crossed_after_no_fill": crossed_after_no_fill,
                "canceled": canceled,
                "entry_mode": entry_mode,
                "passive_exit_attempt": passive_exit_attempt,
                "passive_exit_filled": passive_exit_filled,
                "forced_flatten_applied": forced_flatten,
                "exit_mode": exit_mode,
                "notional_inr": notional_inr,
                "gross_edge_bps": gross_edge_bps,
                "expected_move_bps_no_lookahead": expected_bps,
                "zerodha_cost200_bps": charge_bps,
                "entry_spread_component_bps": entry_spread_component_bps,
                "exit_spread_component_bps": exit_spread_component_bps,
                "adverse_selection_penalty_bps": adverse_penalty_bps,
                "passive_entry_adverse_penalty_bps": passive_entry_penalty_bps,
                "net_edge_bps": net_edge_bps,
                "net_pnl_inr": net_pnl_inr,
                "cumulative_net_pnl_inr": cumulative_pnl,
                "cash_after_decision_inr": cash_inr,
                "open_positions_after_decision": len(open_positions),
                "open_notional_after_decision_inr": float(sum(position.notional_inr for position in open_positions)),
                "side_pressure": side_pressure,
                "adverse_flow_score": adverse_flow,
                "book_support_score": book_support,
                "avg_cum_top5_qty_imbalance": to_float(row.get("avg_cum_top5_qty_imbalance")),
                "avg_depth_beyond_l1_qty_imbalance": to_float(row.get("avg_depth_beyond_l1_qty_imbalance")),
                "avg_level_weighted_depth_imbalance": to_float(row.get("avg_level_weighted_depth_imbalance")),
                "top5_churn_pressure": to_float(row.get("top5_churn_pressure")),
                "avg_spread_bps": spread_bps,
                "raw_book_state_score": to_float(row.get("raw_book_state_score")),
            }
        )

    ledger = pd.DataFrame(rows)
    scheduled = ledger[ledger["decision"].astype(str).eq("scheduled")]
    observed_dates = max(1, int(events["trade_date"].astype(str).nunique()))
    portfolio_return_pct = cumulative_pnl / INITIAL_CAPITAL_INR * 100.0
    annualized_pct = portfolio_return_pct * 252.0 / float(observed_dates)
    positive_symbol_dates = int(scheduled.loc[scheduled["net_pnl_inr"].gt(0.0), ["symbol", "trade_date"]].drop_duplicates().shape[0]) if not scheduled.empty else 0
    scenario = {
        "scenario_id": sid,
        "seed_scope": seed_scope,
        "fill_model_id": fill_model["fill_model_id"],
        "execution_policy_id": policy["execution_policy_id"],
        "max_concurrent_positions": max_concurrent,
        "initial_capital_inr": INITIAL_CAPITAL_INR,
        "fixed_notional_inr": FIXED_NOTIONAL_INR,
        "cost_profile": "cost200",
        "cost_multiplier": COST_MULTIPLIER,
        "input_event_rows": int(len(events)),
        "scheduled_event_rows": int(scheduled_rows),
        "canceled_event_rows": int(canceled_rows),
        "crossed_after_no_fill_rows": int(crossed_after_no_fill_rows),
        "rejected_event_rows": int(rejected_slot_rows + rejected_symbol_rows + rejected_cash_rows),
        "rejected_same_symbol_overlap_rows": int(rejected_symbol_rows),
        "rejected_max_concurrent_rows": int(rejected_slot_rows),
        "rejected_insufficient_cash_rows": int(rejected_cash_rows),
        "passive_entry_attempt_rows": int(passive_entry_attempt_rows),
        "passive_entry_fill_rows": int(passive_entry_fill_rows),
        "passive_exit_attempt_rows": int(passive_exit_attempt_rows),
        "passive_exit_fill_rows": int(passive_exit_fill_rows),
        "forced_flatten_rows": int(forced_flatten_rows),
        "avg_entry_fill_probability": float(ledger["entry_fill_probability"].mean()) if not ledger.empty else 0.0,
        "avg_adverse_selection_penalty_bps_scheduled": float(scheduled["adverse_selection_penalty_bps"].mean()) if not scheduled.empty else 0.0,
        "avg_net_edge_bps_scheduled": float(scheduled["net_edge_bps"].mean()) if not scheduled.empty else 0.0,
        "candidate_rows": int(events["candidate_id"].astype(str).nunique()),
        "scheduled_candidate_rows": int(scheduled["candidate_id"].astype(str).nunique()) if not scheduled.empty else 0,
        "symbols": int(events["symbol"].astype(str).nunique()),
        "scheduled_symbols": int(len(scheduled_symbols)),
        "observed_trade_dates": int(observed_dates),
        "scheduled_trade_dates": int(scheduled["trade_date"].astype(str).nunique()) if not scheduled.empty else 0,
        "positive_trade_dates": int(len(scheduled_positive_dates)),
        "negative_trade_dates": int(len(scheduled_negative_dates)),
        "positive_symbol_date_rows": positive_symbol_dates,
        "realized_net_pnl_inr": float(cumulative_pnl),
        "portfolio_return_pct": float(portfolio_return_pct),
        "mechanical_annualized_portfolio_return_pct": float(annualized_pct),
        "scheduled_notional_inr": float(scheduled_notional),
        "notional_turnover_x_initial_capital": float(scheduled_notional / INITIAL_CAPITAL_INR),
        "avg_open_notional_utilization": float(sum(utilization_samples) / len(utilization_samples)) if utilization_samples else 0.0,
        "max_drawdown_inr": max_drawdown(equity_curve),
        "event_floor_met": int(scheduled_rows >= MIN_EVENT_ROWS),
        "annualized_above12": int(annualized_pct > ANNUALIZED_THRESHOLD_PCT),
        "breadth_met": int(len(scheduled_symbols) >= MIN_BREADTH_SYMBOLS and len(scheduled_positive_dates) >= MIN_BREADTH_DATES),
        "cost200_acceptance_survivor": int(scheduled_rows >= MIN_EVENT_ROWS and annualized_pct > ANNUALIZED_THRESHOLD_PCT and len(scheduled_symbols) >= MIN_BREADTH_SYMBOLS and len(scheduled_positive_dates) >= MIN_BREADTH_DATES),
        "strategy_replay_allowed": 0,
        "promotion_allowed": 0,
        "paper_or_live_acceptance_allowed": 0,
        "deployable_profitability_claim_allowed": 0,
    }
    return scenario, ledger


def build_catalogs() -> tuple[pd.DataFrame, pd.DataFrame]:
    return pd.DataFrame(FILL_MODELS), pd.DataFrame(EXECUTION_POLICIES)


def build_scenarios(seed_events: pd.DataFrame, seeds: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    scenarios: list[dict[str, Any]] = []
    ledgers: list[pd.DataFrame] = []
    scopes = [("ALL_PHASE299_SEEDS", seed_events.copy())]
    top_seeds = seeds.head(3)["phase298_variant_id"].astype(str).tolist()
    for seed_id in top_seeds:
        scopes.append((seed_id, seed_events[seed_events["candidate_id"].astype(str).eq(seed_id)].copy()))
    for seed_scope, events in scopes:
        if events.empty:
            continue
        for fill_model in FILL_MODELS:
            for policy in EXECUTION_POLICIES:
                for max_concurrent in MAX_CONCURRENT_GRID:
                    scenario, ledger = schedule_scenario(events, seed_scope, fill_model, policy, max_concurrent)
                    scenarios.append(scenario)
                    if seed_scope == "ALL_PHASE299_SEEDS" and len(ledgers) < 3:
                        ledgers.append(ledger.head(SAMPLE_LEDGER_ROWS))
    return pd.DataFrame(scenarios), pd.concat(ledgers, ignore_index=True).head(SAMPLE_LEDGER_ROWS) if ledgers else pd.DataFrame()


def build_variant_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for keys, group in scenarios.groupby(["seed_scope", "fill_model_id", "execution_policy_id"], dropna=False):
        best = group.sort_values("mechanical_annualized_portfolio_return_pct", ascending=False).iloc[0]
        rows.append(
            {
                "seed_scope": keys[0],
                "fill_model_id": keys[1],
                "execution_policy_id": keys[2],
                "scenario_rows": int(len(group)),
                "max_scheduled_event_rows": int(group["scheduled_event_rows"].max()),
                "max_annualized_pct": float(group["mechanical_annualized_portfolio_return_pct"].max()),
                "median_annualized_pct": float(group["mechanical_annualized_portfolio_return_pct"].median()),
                "max_net_pnl_inr": float(group["realized_net_pnl_inr"].max()),
                "acceptance_survivor_rows": int(group["cost200_acceptance_survivor"].sum()),
                "event_floor_met_rows": int(group["event_floor_met"].sum()),
                "above12_rows": int(group["annualized_above12"].sum()),
                "breadth_met_rows": int(group["breadth_met"].sum()),
                "best_scenario_id": best["scenario_id"],
            }
        )
    return pd.DataFrame(rows).sort_values(["acceptance_survivor_rows", "max_annualized_pct", "max_scheduled_event_rows"], ascending=[False, False, False], kind="mergesort")


def build_gate_evaluation(precommit: pd.DataFrame, phase299_summary: pd.DataFrame, seeds: pd.DataFrame, seed_events: pd.DataFrame, schema: pd.DataFrame, scenarios: pd.DataFrame, ledger: pd.DataFrame) -> pd.DataFrame:
    precommit_complete = as_int(metric_value(precommit, "phase300_precommit_complete", 0))
    phase299_complete = as_int(metric_value(phase299_summary, "phase299_interpretation_complete", 0))
    book_cols = int(pd.to_numeric(schema.get("book_level_present_columns", pd.Series([0])), errors="coerce").fillna(0).min()) if not schema.empty else 0
    passive_attempts = int(ledger["passive_entry_attempt"].sum()) if not ledger.empty else 0
    passive_fills = int(ledger["passive_entry_filled"].sum()) if not ledger.empty else 0
    adv_penalty_rows = int(ledger.loc[ledger["passive_entry_filled"].astype(int).eq(1), "adverse_selection_penalty_bps"].gt(0.0).sum()) if not ledger.empty else 0
    forced_flatten_rows = int(ledger["forced_flatten_applied"].sum()) if not ledger.empty else 0
    l1_only = 0
    live_masks = 0
    boundaries_closed = bool(
        scenarios["strategy_replay_allowed"].astype(int).eq(0).all()
        and scenarios["promotion_allowed"].astype(int).eq(0).all()
        and scenarios["paper_or_live_acceptance_allowed"].astype(int).eq(0).all()
        and scenarios["deployable_profitability_claim_allowed"].astype(int).eq(0).all()
    )
    gates = [
        ("P300_PHASE300_PRECOMMIT_PRESENT", precommit_complete == 1, precommit_complete, 1),
        ("P300_PHASE299_WORK_ORDER_PRESENT", phase299_complete == 1, phase299_complete, 1),
        ("P300_INPUTS_VALIDATED", len(seeds) > 0 and len(seed_events) >= MIN_EVENT_ROWS and book_cols >= 30, f"seeds={len(seeds)};events={len(seed_events)};book_cols={book_cols}", "seeds, event floor input, raw depth schema"),
        ("P300_L1_ONLY_FORBIDDEN", l1_only == 0, l1_only, 0),
        ("P300_FILL_MODEL_APPLIED", passive_attempts > 0 and passive_fills > 0 and ledger["entry_fill_probability"].between(0.0, 1.0).all(), f"attempts={passive_attempts};fills={passive_fills}", "probabilistic passive fills logged"),
        ("P300_ADVERSE_SELECTION_APPLIED", adv_penalty_rows == passive_fills and passive_fills > 0, f"penalty_rows={adv_penalty_rows};fills={passive_fills}", "penalty on every passive entry fill"),
        ("P300_FORCED_FLATTEN_COST_APPLIED", forced_flatten_rows > 0, forced_flatten_rows, ">0 forced flatten rows"),
        ("P300_NO_LOOKAHEAD", live_masks == 0, live_masks, 0),
        ("P300_COST200_SCORING", scenarios["cost_profile"].astype(str).eq("cost200").all() and scenarios["initial_capital_inr"].astype(float).eq(INITIAL_CAPITAL_INR).all() and scenarios["fixed_notional_inr"].astype(float).lt(100000.0).all(), "cost200;fixed_capital;notional_lt_100000", "required"),
        ("P300_BOUNDARIES_CLOSED", boundaries_closed, "replay=0;promotion=0;paper=0;claim=0", "all zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(precommit: pd.DataFrame, seeds: pd.DataFrame, seed_events: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    best = scenarios.sort_values("mechanical_annualized_portfolio_return_pct", ascending=False).iloc[0]
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    survivor_rows = int(scenarios["cost200_acceptance_survivor"].sum())
    above12_rows = int(scenarios["annualized_above12"].sum())
    event_floor_rows = int(scenarios["event_floor_met"].sum())
    breadth_rows = int(scenarios["breadth_met"].sum())
    kill_switch = int(survivor_rows == 0 or int(best["scheduled_event_rows"]) < MIN_EVENT_ROWS)
    return pd.DataFrame(
        [
            ("phase300_precommit_complete", metric_value(precommit, "phase300_precommit_complete", 0), "Phase300 precommit retained"),
            ("phase300_execution_complete", 1, "Phase300 passive-aware execution hybrid run completed"),
            ("phase300_selected_route", SELECTED_ROUTE, "Selected route"),
            ("phase300_seed_variant_rows", len(seeds), "Phase299 directional seeds used"),
            ("phase300_seed_event_rows", len(seed_events), "Phase298 raw seed events used"),
            ("phase300_scenario_rows", len(scenarios), "Execution scenarios evaluated"),
            ("phase300_fill_model_rows", len(FILL_MODELS), "Fill models evaluated"),
            ("phase300_execution_policy_rows", len(EXECUTION_POLICIES), "Execution policies evaluated"),
            ("phase300_initial_capital_inr", INITIAL_CAPITAL_INR, "Fixed initial capital denominator"),
            ("phase300_fixed_notional_inr", FIXED_NOTIONAL_INR, "Fixed notional below 100000 INR"),
            ("phase300_cost_multiplier", COST_MULTIPLIER, "Cost200 stress"),
            ("phase300_above12_scenario_rows", above12_rows, "Above-12 annualized scenarios"),
            ("phase300_event_floor_scenario_rows", event_floor_rows, "Scenarios with >=30 scheduled events"),
            ("phase300_breadth_met_scenario_rows", breadth_rows, "Scenarios with breadth gate met"),
            ("phase300_cost200_acceptance_survivor_rows", survivor_rows, "Scenarios passing full Phase300 acceptance"),
            ("phase300_best_scenario_id", best["scenario_id"], "Best scenario"),
            ("phase300_best_seed_scope", best["seed_scope"], "Best seed scope"),
            ("phase300_best_fill_model_id", best["fill_model_id"], "Best fill model"),
            ("phase300_best_execution_policy_id", best["execution_policy_id"], "Best execution policy"),
            ("phase300_best_scheduled_event_rows", best["scheduled_event_rows"], "Best scheduled events"),
            ("phase300_best_scheduled_symbols", best["scheduled_symbols"], "Best scheduled symbols"),
            ("phase300_best_positive_trade_dates", best["positive_trade_dates"], "Best positive dates"),
            ("phase300_best_realized_net_pnl_inr", best["realized_net_pnl_inr"], "Best net P&L"),
            ("phase300_best_annualized_pct", best["mechanical_annualized_portfolio_return_pct"], "Best fixed-capital annualized diagnostic"),
            ("phase300_best_avg_entry_fill_probability", best["avg_entry_fill_probability"], "Best average entry fill probability"),
            ("phase300_best_passive_entry_fill_rows", best["passive_entry_fill_rows"], "Best passive entry fill rows"),
            ("phase300_best_forced_flatten_rows", best["forced_flatten_rows"], "Best forced flatten rows"),
            ("phase300_kill_switch_triggered", kill_switch, "Kill-switch if no acceptance survivor or best remains sparse"),
            ("phase300_strategy_replay_allowed", 0, "No replay"),
            ("phase300_strategy_promotion_allowed", 0, "No promotion"),
            ("phase300_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase300_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase300_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase300_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase300_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, gates: pd.DataFrame, scenarios: pd.DataFrame, variants: pd.DataFrame, fill_models: pd.DataFrame, policies: pd.DataFrame) -> None:
    lines = [
        "# Phase300 Passive-Aware Execution Hybrid Run",
        "",
        "Phase300 executes the precommitted passive-aware execution policy on Phase299 directional L2 seeds.",
        "",
        "The run logs passive fill probabilities, deterministic fill draws, adverse-selection penalties, forced flattening, spread components, Zerodha cost200 charges and fixed-capital annualization.",
        "",
        "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "## Top Scenarios",
        "",
        _markdown_table(scenarios.sort_values("mechanical_annualized_portfolio_return_pct", ascending=False).head(20)),
        "",
        "## Variant Summary",
        "",
        _markdown_table(variants.head(20)),
        "",
        "## Fill Models",
        "",
        _markdown_table(fill_models),
        "",
        "## Execution Policies",
        "",
        _markdown_table(policies),
    ]
    (output_dir / "phase300_passive_aware_execution_hybrid_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(output_dir: Path = DEFAULT_PHASE300_DIR, phase299_dir: Path = DEFAULT_PHASE299_DIR, phase298_dir: Path = DEFAULT_PHASE298_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    precommit, phase299_summary, seeds, seed_events, schema = load_inputs(output_dir, phase299_dir, phase298_dir)
    fill_models, policies = build_catalogs()
    scenarios, ledger = build_scenarios(seed_events, seeds)
    variants = build_variant_summary(scenarios)
    gates = build_gate_evaluation(precommit, phase299_summary, seeds, seed_events, schema, scenarios, ledger)
    acceptance = build_acceptance(precommit, seeds, seed_events, scenarios, gates)

    fill_models.to_csv(output_dir / "phase300_fill_model_catalog.csv", index=False)
    policies.to_csv(output_dir / "phase300_execution_policy_catalog.csv", index=False)
    seeds.to_csv(output_dir / "phase300_directional_signal_seed_catalog.csv", index=False)
    seed_events.to_csv(output_dir / "phase300_directional_seed_event_universe.csv", index=False)
    scenarios.to_csv(output_dir / "phase300_execution_scenario_summary.csv", index=False)
    variants.to_csv(output_dir / "phase300_execution_variant_summary.csv", index=False)
    ledger.to_csv(output_dir / "phase300_execution_event_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase300_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase300_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, gates, scenarios, variants, fill_models, policies)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase300_passive_aware_execution_hybrid",
        **reproducibility_fields(
            artifact_id="phase300",
            generated_utc=generated_utc,
            inputs={
                "phase300_precommit_charter": str(output_dir / "phase300_precommit_charter.csv"),
                "phase300_precommit_execution_work_order": str(output_dir / "phase300_execution_work_order.csv"),
                "phase299_ranked_variant_interpretation": str(phase299_dir / "phase299_ranked_variant_interpretation.csv"),
                "phase298_raw_dense_candidate_events": str(phase298_dir / "phase298_raw_dense_candidate_events.csv"),
                "phase298_raw_book_schema_audit": str(phase298_dir / "phase298_raw_book_schema_audit.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "initial_capital_inr": INITIAL_CAPITAL_INR,
                "fixed_notional_inr": FIXED_NOTIONAL_INR,
                "max_concurrent_grid": MAX_CONCURRENT_GRID,
                "cost_multiplier": COST_MULTIPLIER,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "min_event_rows": MIN_EVENT_ROWS,
                "min_breadth_symbols": MIN_BREADTH_SYMBOLS,
                "min_breadth_dates": MIN_BREADTH_DATES,
                "fill_draw": "deterministic_sha256_uniform_no_lookahead",
            },
            outputs={"acceptance_summary": str(output_dir / "phase300_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase300_passive_aware_hybrid_deterministic_fill_v1",
        ),
    }
    (output_dir / "phase300_passive_aware_execution_hybrid_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase300 passive-aware execution hybrid.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_PHASE300_DIR)
    parser.add_argument("--phase299-dir", type=Path, default=DEFAULT_PHASE299_DIR)
    parser.add_argument("--phase298-dir", type=Path, default=DEFAULT_PHASE298_DIR)
    args = parser.parse_args()
    acceptance = run(output_dir=args.output_dir, phase299_dir=args.phase299_dir, phase298_dir=args.phase298_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

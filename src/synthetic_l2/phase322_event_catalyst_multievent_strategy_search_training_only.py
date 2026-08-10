from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import (
    BROKERAGE_CAP_PER_EXECUTED_ORDER_INR,
    BROKERAGE_RATE,
    GST_RATE,
    NSE_TRANSACTION_CHARGE_RATE,
    SEBI_CHARGE_RATE,
    STAMP_DUTY_BUY_SIDE_RATE,
    STT_INTRADAY_SELL_SIDE_RATE,
    ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
)


DEFAULT_PHASE320_DIR = Path("outputs/phase320")
DEFAULT_PHASE321_DIR = Path("outputs/phase321")
DEFAULT_OUTPUT_DIR = Path("outputs/phase322")

NEXT_ACTION = "run_phase323_event_catalyst_multievent_strategy_search_interpretation_no_replay"
REPAIR_ACTION = "repair_phase322_event_catalyst_multievent_strategy_search_training_only"

ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30


def threshold_mask(abs_signal: pd.Series, policy: str) -> pd.Series:
    if policy == "all_nonzero_signal":
        return abs_signal > 0
    if policy == "top_50pct_abs_signal":
        return abs_signal >= abs_signal.quantile(0.50)
    if policy == "top_25pct_abs_signal":
        return abs_signal >= abs_signal.quantile(0.75)
    if policy == "top_10pct_abs_signal":
        return abs_signal >= abs_signal.quantile(0.90)
    return pd.Series(False, index=abs_signal.index)


def signed_signal(frame: pd.DataFrame, family_id: str) -> pd.Series:
    if family_id == "P321_DEPTH_PRESSURE_CONTINUATION":
        return pd.to_numeric(frame["event_depth_l2_l5_pressure"], errors="coerce")
    if family_id == "P321_DEPTH_PRESSURE_REVERSAL":
        return -pd.to_numeric(frame["event_depth_l2_l5_pressure"], errors="coerce")
    if family_id == "P321_DEPTH_ACCEL_CONTINUATION":
        return pd.to_numeric(frame["event_depth_l2_l5_pressure"], errors="coerce") - pd.to_numeric(frame["pre300_depth_l2_l5_pressure_avg"], errors="coerce")
    if family_id == "P321_DEPTH_ACCEL_REVERSAL":
        return -(pd.to_numeric(frame["event_depth_l2_l5_pressure"], errors="coerce") - pd.to_numeric(frame["pre300_depth_l2_l5_pressure_avg"], errors="coerce"))
    if family_id == "P321_QTY_IMBALANCE_CONTINUATION":
        return pd.to_numeric(frame["event_depth_l2_l5_qty_imbalance"], errors="coerce")
    if family_id == "P321_QTY_IMBALANCE_REVERSAL":
        return -pd.to_numeric(frame["event_depth_l2_l5_qty_imbalance"], errors="coerce")
    if family_id == "P321_ORDER_IMBALANCE_CONTINUATION":
        return pd.to_numeric(frame["event_depth_l2_l5_order_imbalance"], errors="coerce")
    if family_id == "P321_ORDER_IMBALANCE_REVERSAL":
        return -pd.to_numeric(frame["event_depth_l2_l5_order_imbalance"], errors="coerce")
    if family_id == "P321_MICROPRICE_DEPTH_CONFIRM":
        micro = pd.to_numeric(frame["pre300_microprice_minus_mid_avg"], errors="coerce")
        depth = pd.to_numeric(frame["event_depth_l2_l5_qty_imbalance"], errors="coerce")
        return micro.where(np.sign(micro).eq(np.sign(depth)), 0.0)
    if family_id == "P321_DEPTH_PRESSURE_TARGET_SHIFT":
        return pd.to_numeric(frame["pre300_depth_l2_l5_pressure_avg"], errors="coerce")
    return pd.Series(0.0, index=frame.index)


def vector_cost_inr(notional: float, gross_return_bps: pd.Series, cost_profile: str) -> pd.Series:
    buy_value = float(notional)
    sell_value = (buy_value * (1.0 + gross_return_bps.abs() / 10_000.0)).clip(lower=0.0)
    turnover = buy_value + sell_value
    buy_brokerage = min(buy_value * BROKERAGE_RATE, BROKERAGE_CAP_PER_EXECUTED_ORDER_INR)
    sell_brokerage = np.minimum(sell_value * BROKERAGE_RATE, BROKERAGE_CAP_PER_EXECUTED_ORDER_INR)
    brokerage = buy_brokerage + sell_brokerage
    average_intraday_price = turnover / 2.0
    stt = np.floor(average_intraday_price * STT_INTRADAY_SELL_SIDE_RATE + 0.5)
    transaction_charge = turnover * NSE_TRANSACTION_CHARGE_RATE
    sebi_charge = turnover * SEBI_CHARGE_RATE
    stamp_duty = buy_value * STAMP_DUTY_BUY_SIDE_RATE
    gst = GST_RATE * (brokerage + transaction_charge + sebi_charge)
    base_cost = brokerage + stt + transaction_charge + sebi_charge + stamp_duty + gst
    if cost_profile == "zerodha_2x_all_in_cost_proxy":
        return base_cost * 2.0
    extra_slip_bps = 2.0 if cost_profile == "zerodha_plus_2bp_slippage" else (1.0 if cost_profile == "zerodha_plus_1bp_slippage" else 0.0)
    slippage = turnover * extra_slip_bps / 10_000.0
    return base_cost + slippage


def passive_adjustments(frame: pd.DataFrame, execution_policy: str, notional: float) -> tuple[pd.Series, pd.Series, pd.Series]:
    zeros = pd.Series(0.0, index=frame.index)
    if execution_policy != "passive_aware_directional_with_penalties":
        return pd.Series(1.0, index=frame.index), zeros, zeros
    spread_bps = (pd.to_numeric(frame["event_l1_spread"], errors="coerce") / pd.to_numeric(frame["event_l1_mid"], errors="coerce").replace(0, np.nan) * 10_000.0).fillna(0.0).clip(lower=0.0)
    depth_share = pd.to_numeric(frame["event_l2_l5_depth_share"], errors="coerce").fillna(0.0).clip(lower=0.0, upper=1.5)
    toxicity = pd.to_numeric(frame["event_depth_l2_l5_pressure"], errors="coerce").abs().fillna(0.0).clip(lower=0.0, upper=25.0)
    fill_probability = (0.45 + 0.25 * depth_share - 0.015 * spread_bps - 0.010 * toxicity).clip(lower=0.10, upper=0.80)
    adverse_selection_bps = (0.50 + 0.20 * toxicity + 0.10 * spread_bps).clip(lower=0.50, upper=8.0)
    forced_flatten_bps = (1.0 - fill_probability) * (spread_bps + 2.0)
    penalty_inr = notional * (adverse_selection_bps + forced_flatten_bps) / 10_000.0
    return fill_probability, adverse_selection_bps, penalty_inr


def evaluate_scenario(features: pd.DataFrame, family_id: str, grid_row: pd.Series) -> dict[str, Any]:
    horizon = as_int(grid_row["horizon_seconds"])
    target_col = f"target_post_{horizon}s_mid_return_bps"
    if target_col not in features.columns:
        return {}
    frame = features.copy()
    frame["signal"] = signed_signal(frame, family_id).fillna(0.0)
    frame["abs_signal"] = frame["signal"].abs()
    frame = frame[threshold_mask(frame["abs_signal"], str(grid_row["threshold_policy"]))].copy()
    frame = frame[frame["signal"].ne(0)].copy()
    if frame.empty:
        return {}
    frame["side"] = np.where(frame["signal"] > 0, 1, -1)
    side_policy = str(grid_row["side_policy"])
    if side_policy == "long_only":
        frame = frame[frame["side"].eq(1)].copy()
    elif side_policy == "short_only":
        frame = frame[frame["side"].eq(-1)].copy()
    if frame.empty:
        return {}
    frame["signed_return_bps"] = frame["side"] * pd.to_numeric(frame[target_col], errors="coerce")
    frame = frame.dropna(subset=["signed_return_bps"]).copy()
    if frame.empty:
        return {}
    frame = frame.sort_values(["event_id", "abs_signal", "symbol"], ascending=[True, False, True])
    max_concurrent = as_int(grid_row["max_concurrent_positions"])
    notional = float(grid_row["fixed_notional_inr"])
    capital = float(grid_row["initial_capital_inr"])
    affordable = max(0, int(capital // notional))
    slots = max(0, min(max_concurrent, affordable))
    if slots <= 0:
        return {}
    selected = frame.groupby("event_id", group_keys=False).head(slots).copy()
    if selected.empty:
        return {}
    fill_probability, adverse_selection_bps, passive_penalty = passive_adjustments(selected, str(grid_row["execution_policy"]), notional)
    selected["fill_probability"] = fill_probability
    selected["gross_pnl_inr"] = notional * selected["signed_return_bps"] / 10_000.0 * selected["fill_probability"]
    cost_values = vector_cost_inr(notional, selected["signed_return_bps"], str(grid_row["cost_profile"]))
    selected["cost_inr"] = cost_values * selected["fill_probability"]
    selected["passive_penalty_inr"] = passive_penalty
    selected["net_pnl_inr"] = selected["gross_pnl_inr"] - selected["cost_inr"] - selected["passive_penalty_inr"]
    net_pnl = float(selected["net_pnl_inr"].sum())
    gross_pnl = float(selected["gross_pnl_inr"].sum())
    cost_inr = float(selected["cost_inr"].sum())
    passive_penalty_inr = float(selected["passive_penalty_inr"].sum())
    event_rows = int(selected["event_id"].nunique())
    symbol_rows = int(selected["symbol"].nunique())
    observed_dates = int(selected["event_time_ist"].astype(str).str.slice(0, 10).nunique())
    portfolio_return_pct = net_pnl / capital * 100.0 if capital else 0.0
    annualized_pct = portfolio_return_pct * 252.0 / max(observed_dates, 1)
    return {
        "family_id": family_id,
        "horizon_seconds": horizon,
        "threshold_policy": str(grid_row["threshold_policy"]),
        "cost_profile": str(grid_row["cost_profile"]),
        "initial_capital_inr": capital,
        "fixed_notional_inr": notional,
        "max_concurrent_positions": max_concurrent,
        "side_policy": side_policy,
        "execution_policy": str(grid_row["execution_policy"]),
        "scheduled_event_rows": event_rows,
        "symbol_rows": symbol_rows,
        "observed_trade_dates": observed_dates,
        "trade_rows": int(len(selected)),
        "avg_fill_probability": float(selected["fill_probability"].mean()),
        "gross_pnl_inr": gross_pnl,
        "cost_inr": cost_inr,
        "passive_penalty_inr": passive_penalty_inr,
        "net_pnl_inr": net_pnl,
        "portfolio_return_pct": portfolio_return_pct,
        "annualized_return_pct": annualized_pct,
        "above12_annualized": int(annualized_pct > ANNUALIZED_THRESHOLD_PCT),
        "robust_event_floor_met": int(event_rows >= ROBUST_EVENT_FLOOR),
        "acceptance_grade_candidate": int(annualized_pct > ANNUALIZED_THRESHOLD_PCT and event_rows >= ROBUST_EVENT_FLOOR and symbol_rows >= 2 and observed_dates >= 2 and str(grid_row["cost_profile"]) == "zerodha_2x_all_in_cost_proxy"),
        "profitability_claim_allowed": 0,
    }


def run_search(features: pd.DataFrame, families: pd.DataFrame, grid: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if features.empty or families.empty or grid.empty:
        return pd.DataFrame()
    feature_base = features.copy()
    capitals = sorted(pd.to_numeric(grid["initial_capital_inr"], errors="coerce").dropna().unique().tolist())
    notionals = sorted(pd.to_numeric(grid["fixed_notional_inr"], errors="coerce").dropna().unique().tolist())
    concurrencies = sorted(pd.to_numeric(grid["max_concurrent_positions"], errors="coerce").dropna().astype(int).unique().tolist())
    horizons = sorted(pd.to_numeric(grid["horizon_seconds"], errors="coerce").dropna().astype(int).unique().tolist())
    threshold_policies = sorted(grid["threshold_policy"].astype(str).unique().tolist())
    cost_profiles = sorted(grid["cost_profile"].astype(str).unique().tolist())
    side_policies = sorted(grid["side_policy"].astype(str).unique().tolist())
    execution_policies = sorted(grid["execution_policy"].astype(str).unique().tolist())
    possible_slots = sorted({max(0, min(int(conc), int(float(capital) // float(notional)))) for capital in capitals for notional in notionals for conc in concurrencies})

    for family_id in families["family_id"].astype(str):
        frame = feature_base.copy()
        frame["signal"] = signed_signal(frame, family_id).fillna(0.0)
        frame["abs_signal"] = frame["signal"].abs()
        frame["side"] = np.where(frame["signal"] > 0, 1, -1)
        for horizon in horizons:
            target_col = f"target_post_{horizon}s_mid_return_bps"
            if target_col not in frame.columns:
                continue
            frame["signed_return_bps_base"] = frame["side"] * pd.to_numeric(frame[target_col], errors="coerce")
            for threshold_policy in threshold_policies:
                thresholded = frame[threshold_mask(frame["abs_signal"], threshold_policy) & frame["signal"].ne(0)].copy()
                if thresholded.empty:
                    continue
                for side_policy in side_policies:
                    if side_policy == "long_only":
                        sided = thresholded[thresholded["side"].eq(1)].copy()
                    elif side_policy == "short_only":
                        sided = thresholded[thresholded["side"].eq(-1)].copy()
                    else:
                        sided = thresholded.copy()
                    sided = sided.dropna(subset=["signed_return_bps_base"]).sort_values(["event_id", "abs_signal", "symbol"], ascending=[True, False, True])
                    selected_by_slots: dict[int, pd.DataFrame] = {}
                    for slots in possible_slots:
                        if slots <= 0 or sided.empty:
                            selected_by_slots[slots] = pd.DataFrame()
                        else:
                            selected = sided.groupby("event_id", group_keys=False).head(slots).copy()
                            selected_by_slots[slots] = selected
                    for capital in capitals:
                        capital_float = float(capital)
                        for notional in notionals:
                            notional_float = float(notional)
                            affordable = int(capital_float // notional_float)
                            for max_concurrent in concurrencies:
                                slots = max(0, min(int(max_concurrent), affordable))
                                selected = selected_by_slots.get(slots, pd.DataFrame())
                                for cost_profile in cost_profiles:
                                    for execution_policy in execution_policies:
                                        if selected.empty:
                                            rows.append(
                                                {
                                                    "family_id": family_id,
                                                    "horizon_seconds": horizon,
                                                    "threshold_policy": threshold_policy,
                                                    "cost_profile": cost_profile,
                                                    "initial_capital_inr": capital_float,
                                                    "fixed_notional_inr": notional_float,
                                                    "max_concurrent_positions": int(max_concurrent),
                                                    "side_policy": side_policy,
                                                    "execution_policy": execution_policy,
                                                    "scheduled_event_rows": 0,
                                                    "symbol_rows": 0,
                                                    "observed_trade_dates": 0,
                                                    "trade_rows": 0,
                                                    "avg_fill_probability": 0.0,
                                                    "gross_pnl_inr": 0.0,
                                                    "cost_inr": 0.0,
                                                    "passive_penalty_inr": 0.0,
                                                    "net_pnl_inr": 0.0,
                                                    "portfolio_return_pct": 0.0,
                                                    "annualized_return_pct": 0.0,
                                                    "above12_annualized": 0,
                                                    "robust_event_floor_met": 0,
                                                    "acceptance_grade_candidate": 0,
                                                    "profitability_claim_allowed": 0,
                                                }
                                            )
                                            continue
                                        fill_probability, _, passive_penalty = passive_adjustments(selected, execution_policy, notional_float)
                                        signed_returns = pd.to_numeric(selected["signed_return_bps_base"], errors="coerce").fillna(0.0)
                                        gross_pnl = notional_float * signed_returns / 10_000.0 * fill_probability
                                        costs = vector_cost_inr(notional_float, signed_returns, cost_profile) * fill_probability
                                        net = gross_pnl - costs - passive_penalty
                                        net_pnl = float(net.sum())
                                        event_rows = int(selected["event_id"].nunique())
                                        symbol_rows = int(selected["symbol"].nunique())
                                        observed_dates = int(selected["event_time_ist"].astype(str).str.slice(0, 10).nunique())
                                        portfolio_return_pct = net_pnl / capital_float * 100.0 if capital_float else 0.0
                                        annualized_pct = portfolio_return_pct * 252.0 / max(observed_dates, 1)
                                        rows.append(
                                            {
                                                "family_id": family_id,
                                                "horizon_seconds": horizon,
                                                "threshold_policy": threshold_policy,
                                                "cost_profile": cost_profile,
                                                "initial_capital_inr": capital_float,
                                                "fixed_notional_inr": notional_float,
                                                "max_concurrent_positions": int(max_concurrent),
                                                "side_policy": side_policy,
                                                "execution_policy": execution_policy,
                                                "scheduled_event_rows": event_rows,
                                                "symbol_rows": symbol_rows,
                                                "observed_trade_dates": observed_dates,
                                                "trade_rows": int(len(selected)),
                                                "avg_fill_probability": float(fill_probability.mean()),
                                                "gross_pnl_inr": float(gross_pnl.sum()),
                                                "cost_inr": float(costs.sum()),
                                                "passive_penalty_inr": float(passive_penalty.sum()),
                                                "net_pnl_inr": net_pnl,
                                                "portfolio_return_pct": portfolio_return_pct,
                                                "annualized_return_pct": annualized_pct,
                                                "above12_annualized": int(annualized_pct > ANNUALIZED_THRESHOLD_PCT),
                                                "robust_event_floor_met": int(event_rows >= ROBUST_EVENT_FLOOR),
                                                "acceptance_grade_candidate": int(annualized_pct > ANNUALIZED_THRESHOLD_PCT and event_rows >= ROBUST_EVENT_FLOOR and symbol_rows >= 2 and observed_dates >= 2 and cost_profile == "zerodha_2x_all_in_cost_proxy"),
                                                "profitability_claim_allowed": 0,
                                            }
                                        )
    return pd.DataFrame(rows)


def build_interpretation(scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios.empty:
        return pd.DataFrame([{"metric": "phase322_best_scenario_id", "value": "", "description": "No scenarios produced"}])
    ranked = scenarios.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=[False, False]).reset_index(drop=True)
    best = ranked.iloc[0]
    cost200 = scenarios[scenarios["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy")]
    best_cost200 = cost200.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=[False, False]).head(1)
    broadest = scenarios.sort_values(["scheduled_event_rows", "annualized_return_pct"], ascending=[False, False]).head(1).iloc[0]
    rows = [
        ("phase322_best_scenario_id", scenario_id(best), "Best scenario by annualized return"),
        ("phase322_best_family_id", best["family_id"], "Best scenario family"),
        ("phase322_best_execution_policy", best["execution_policy"], "Best scenario execution policy"),
        ("phase322_best_cost_profile", best["cost_profile"], "Best scenario cost profile"),
        ("phase322_best_annualized_return_pct", float(best["annualized_return_pct"]), "Best annualized fixed-capital research metric"),
        ("phase322_best_net_pnl_inr", float(best["net_pnl_inr"]), "Best net P&L"),
        ("phase322_best_scheduled_event_rows", int(best["scheduled_event_rows"]), "Best scheduled event rows"),
        ("phase322_cost200_above12_scenario_rows", int(((cost200["annualized_return_pct"] > ANNUALIZED_THRESHOLD_PCT)).sum()) if not cost200.empty else 0, "2x cost scenarios above 12% annualized"),
        ("phase322_cost200_acceptance_grade_candidate_rows", int(cost200["acceptance_grade_candidate"].sum()) if not cost200.empty else 0, "2x cost scenarios meeting acceptance-grade event/date/symbol floor"),
        ("phase322_best_cost200_annualized_return_pct", float(best_cost200.iloc[0]["annualized_return_pct"]) if not best_cost200.empty else "", "Best 2x-cost annualized return"),
        ("phase322_best_cost200_scheduled_event_rows", int(best_cost200.iloc[0]["scheduled_event_rows"]) if not best_cost200.empty else 0, "Best 2x-cost scheduled events"),
        ("phase322_broadest_scenario_id", scenario_id(broadest), "Scenario with broadest event support"),
        ("phase322_broadest_annualized_return_pct", float(broadest["annualized_return_pct"]), "Broadest scenario annualized return"),
        ("phase322_broadest_scheduled_event_rows", int(broadest["scheduled_event_rows"]), "Broadest scheduled event rows"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def scenario_id(row: pd.Series) -> str:
    return (
        f"{row['family_id']}_H{int(row['horizon_seconds'])}_{row['threshold_policy']}_"
        f"{row['side_policy']}_{row['execution_policy']}_CAP{int(row['initial_capital_inr'])}_"
        f"NOT{int(row['fixed_notional_inr'])}_CONC{int(row['max_concurrent_positions'])}_{row['cost_profile']}"
    )


def build_gate_evaluation(phase321: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    phase321_complete = as_int(metric_value(phase321, "phase321_multievent_strategy_search_precommit_complete", 0))
    execution_allowed = as_int(metric_value(phase321, "phase321_strategy_search_execution_allowed_next", 0))
    expected_upper = as_int(metric_value(phase321, "phase321_expanded_variant_upper_bound_rows", 0))
    scenario_rows = int(len(scenarios))
    rows = [
        ("P322_PHASE321_COMPLETE", phase321_complete == 1, phase321_complete, 1),
        ("P322_PHASE321_EXECUTION_ALLOWED", execution_allowed == 1, execution_allowed, 1),
        ("P322_SCENARIOS_PRODUCED", scenario_rows > 0, scenario_rows, ">0"),
        ("P322_VARIANT_COVERAGE_COMPLETE", scenario_rows == expected_upper, f"{scenario_rows}/{expected_upper}", "equal"),
        ("P322_COST200_SCENARIOS_PRESENT", int(scenarios["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy").sum()) > 0 if not scenarios.empty else False, int(scenarios["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy").sum()) if not scenarios.empty else 0, ">0"),
        ("P322_PASSIVE_AWARE_SCENARIOS_PRESENT", int(scenarios["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties").sum()) > 0 if not scenarios.empty else False, int(scenarios["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties").sum()) if not scenarios.empty else 0, ">0"),
        ("P322_FIXED_CAPITAL_DENOMINATOR", int((scenarios["initial_capital_inr"] > 0).all()) if not scenarios.empty else 0, "all_positive", "all_positive"),
        ("P322_NO_PROFITABILITY_CLAIM", int((scenarios["profitability_claim_allowed"].astype(int) == 0).all()) if not scenarios.empty else 0, "profitability_claim_allowed=0", 0),
        ("P322_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(scenarios: pd.DataFrame, interpretation: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    im = {str(row.metric): row.value for row in interpretation.itertuples(index=False)}
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    rows = [
        ("phase322_multievent_strategy_search_training_complete", complete, "Phase322 training-only strategy search completed"),
        ("phase322_scenario_rows", int(len(scenarios)), "Scenario rows evaluated"),
        ("phase322_family_rows", int(scenarios["family_id"].nunique()) if not scenarios.empty else 0, "Distinct families evaluated"),
        ("phase322_cost200_scenario_rows", int(scenarios["cost_profile"].astype(str).eq("zerodha_2x_all_in_cost_proxy").sum()) if not scenarios.empty else 0, "2x cost-stress scenarios"),
        ("phase322_passive_aware_scenario_rows", int(scenarios["execution_policy"].astype(str).eq("passive_aware_directional_with_penalties").sum()) if not scenarios.empty else 0, "Passive-aware scenarios"),
        ("phase322_above12_annualized_scenario_rows", int(scenarios["above12_annualized"].astype(int).sum()) if not scenarios.empty else 0, "Scenarios above 12% annualized research threshold"),
        ("phase322_cost200_above12_scenario_rows", as_int(im.get("phase322_cost200_above12_scenario_rows", 0)), "2x cost scenarios above 12% annualized"),
        ("phase322_cost200_acceptance_grade_candidate_rows", as_int(im.get("phase322_cost200_acceptance_grade_candidate_rows", 0)), "2x cost scenarios meeting acceptance-grade breadth"),
        ("phase322_best_scenario_id", im.get("phase322_best_scenario_id", ""), "Best scenario id"),
        ("phase322_best_family_id", im.get("phase322_best_family_id", ""), "Best scenario family"),
        ("phase322_best_execution_policy", im.get("phase322_best_execution_policy", ""), "Best execution policy"),
        ("phase322_best_cost_profile", im.get("phase322_best_cost_profile", ""), "Best cost profile"),
        ("phase322_best_annualized_return_pct", im.get("phase322_best_annualized_return_pct", ""), "Best annualized fixed-capital research metric"),
        ("phase322_best_scheduled_event_rows", im.get("phase322_best_scheduled_event_rows", ""), "Best scheduled event rows"),
        ("phase322_best_cost200_annualized_return_pct", im.get("phase322_best_cost200_annualized_return_pct", ""), "Best 2x-cost annualized return"),
        ("phase322_best_cost200_scheduled_event_rows", im.get("phase322_best_cost200_scheduled_event_rows", ""), "Best 2x-cost scheduled events"),
        ("phase322_annualized_denominator", "fixed_initial_capital", "No unlimited capital denominator"),
        ("phase322_strategy_replay_allowed", 0, "No replay"),
        ("phase322_strategy_promotion_allowed", 0, "No promotion"),
        ("phase322_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase322_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
        ("phase322_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase322_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase322_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, interpretation: pd.DataFrame, gates: pd.DataFrame, top: pd.DataFrame) -> None:
    lines = [
        "# Phase322 Event-Catalyst Multi-Event Strategy Search Training-Only",
        "",
        "Phase322 executes the precommitted training-only strategy search over the Phase320 feature matrix.",
        "It reports fixed-capital research diagnostics only. It does not replay, promote, open paper/live acceptance, or claim deployable profitability.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Interpretation metrics",
        "",
        _markdown_table(interpretation),
        "",
        "## Top scenarios",
        "",
        _markdown_table(top),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase322_event_catalyst_multievent_strategy_search_training_only_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase320_dir: Path = DEFAULT_PHASE320_DIR, phase321_dir: Path = DEFAULT_PHASE321_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    features = read_csv(phase320_dir / "phase320_event_catalyst_multievent_feature_matrix.csv")
    phase321 = read_csv(phase321_dir / "phase321_acceptance_summary.csv")
    families = read_csv(phase321_dir / "phase321_strategy_family_catalog.csv")
    grid = read_csv(phase321_dir / "phase321_strategy_search_grid.csv")
    scenarios = run_search(features, families, grid)
    if not scenarios.empty:
        scenarios["scenario_id"] = scenarios.apply(scenario_id, axis=1)
        scenarios = scenarios.sort_values(["annualized_return_pct", "net_pnl_inr"], ascending=[False, False]).reset_index(drop=True)
    interpretation = build_interpretation(scenarios)
    gates = build_gate_evaluation(phase321, scenarios)
    acceptance = build_acceptance(scenarios, interpretation, gates)
    top = scenarios.head(100) if not scenarios.empty else pd.DataFrame()

    scenarios.to_csv(output_dir / "phase322_scenario_summary.csv", index=False)
    top.to_csv(output_dir / "phase322_top_scenarios.csv", index=False)
    interpretation.to_csv(output_dir / "phase322_interpretation_metrics.csv", index=False)
    gates.to_csv(output_dir / "phase322_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase322_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, interpretation, gates, top.head(25) if not top.empty else top)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase322_event_catalyst_multievent_strategy_search_training_only",
        **reproducibility_fields(
            artifact_id="phase322",
            generated_utc=generated_utc,
            inputs={
                "phase320_feature_matrix": str(phase320_dir / "phase320_event_catalyst_multievent_feature_matrix.csv"),
                "phase321_acceptance": str(phase321_dir / "phase321_acceptance_summary.csv"),
                "phase321_grid": str(phase321_dir / "phase321_strategy_search_grid.csv"),
            },
            parameters={"annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT, "robust_event_floor": ROBUST_EVENT_FLOOR},
            outputs={"scenario_summary": str(output_dir / "phase322_scenario_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase321_passive_aware_directional_penalty_proxy",
        ),
    }
    (output_dir / "phase322_event_catalyst_multievent_strategy_search_training_only_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase322 multi-event strategy search training-only.")
    parser.add_argument("--phase320-dir", type=Path, default=DEFAULT_PHASE320_DIR)
    parser.add_argument("--phase321-dir", type=Path, default=DEFAULT_PHASE321_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase320_dir, args.phase321_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

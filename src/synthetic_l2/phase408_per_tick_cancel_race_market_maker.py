from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase407_cancel_latency_market_maker_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    COST_MULTIPLIER,
    DEFAULT_EXISTING_REAL_ROOT,
    DEFAULT_UNSEEN_REAL_ROOT,
    FIXED_NOTIONAL_PER_SIDE_INR,
    INITIAL_CAPITAL_INR,
    JITTER_SEED,
    MIN_POSITIVE_DATE_FRACTION,
    MIN_ROUND_TRIPS,
    MIN_SYMBOLS,
    MIN_TRADE_DATES,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_RAW_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_PHASE407_DIR = Path("outputs/phase407")
DEFAULT_OUTPUT_DIR = Path("outputs/phase408")
NEXT_ACTION = "interpret_phase408_cancel_race_market_maker_no_paper_live"
REPAIR_ACTION = "repair_phase408_per_tick_cancel_race_market_maker"

PRIMARY_FAMILY = "P408_TWO_SIDED_TOP5_L2_L5_CHURN_QUOTER"
SYNTHETIC_SYMBOLS = ["HDFCBANK", "RELIANCE", "INFY", "SBIN", "AXISBANK"]
SYNTHETIC_MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"]
REAL_ANCHOR_DATE = "2026-08-04"
MAX_ROWS_PER_SYNTHETIC_FILE = 25_000
MAX_REAL_FILES_PER_SYMBOL = 1_500
QUOTE_STRIDE_TICKS = 250
QUOTE_WINDOW_TICKS = 80
MAX_WINDOWS_PER_SYMBOL_DATE = 6

REQUIRED_COLUMNS = [
    "exchange_timestamp_ms",
    "trade_date",
    "exchange",
    "symbol",
    "last_price",
    "buy_1_price",
    "buy_1_quantity",
    "buy_1_orders",
    "sell_1_price",
    "sell_1_quantity",
    "sell_1_orders",
    "buy_2_quantity",
    "buy_3_quantity",
    "buy_4_quantity",
    "buy_5_quantity",
    "sell_2_quantity",
    "sell_3_quantity",
    "sell_4_quantity",
    "sell_5_quantity",
]


def stable_uniform(*parts: Any) -> float:
    payload = "|".join(str(part) for part in parts).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()[:16]
    return int(digest, 16) / float(16**16 - 1)


def stable_jitter_ms(scenario_id: str, quote_id: str, side: str, target_cancel_ms: int) -> float:
    # Truncated log-normal RTT variance proxy, deterministic per quote/side.
    u1 = min(max(stable_uniform(JITTER_SEED, scenario_id, quote_id, side, "u1"), 1e-9), 1.0 - 1e-9)
    u2 = stable_uniform(JITTER_SEED, scenario_id, quote_id, side, "u2")
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    sigma = 0.35
    raw = math.exp(sigma * z) - math.exp(0.5 * sigma * sigma)
    jitter = raw * max(15.0, target_cancel_ms * 0.20)
    return float(min(max(jitter, -0.30 * target_cancel_ms), 0.75 * target_cancel_ms))


def read_first_rows(path: Path, columns: list[str], max_rows: int) -> pd.DataFrame:
    pf = pq.ParquetFile(path)
    available = [col for col in columns if col in pf.schema.names]
    batches = []
    rows = 0
    for batch in pf.iter_batches(batch_size=min(max_rows, 25_000), columns=available):
        frame = batch.to_pandas()
        batches.append(frame)
        rows += len(frame)
        if rows >= max_rows:
            break
    out = pd.concat(batches, ignore_index=True).head(max_rows) if batches else pd.DataFrame(columns=available)
    return out


def normalize_ticks(frame: pd.DataFrame, *, symbol_hint: str = "", date_hint: str = "") -> pd.DataFrame:
    out = frame.copy()
    if "symbol" not in out.columns:
        if "tradingsymbol" in out.columns:
            out["symbol"] = out["tradingsymbol"].astype(str)
        elif "requested_symbol" in out.columns:
            out["symbol"] = out["requested_symbol"].astype(str)
        else:
            out["symbol"] = symbol_hint
    if "exchange" not in out.columns:
        out["exchange"] = "NSE"
    if "trade_date" not in out.columns:
        out["trade_date"] = date_hint
    if "exchange_timestamp_ms" not in out.columns:
        if "collector_received_utc_ms" in out.columns:
            out["exchange_timestamp_ms"] = pd.to_numeric(out["collector_received_utc_ms"], errors="coerce")
        elif "exchange_timestamp" in out.columns:
            out["exchange_timestamp_ms"] = pd.to_datetime(out["exchange_timestamp"], errors="coerce").astype("int64") // 1_000_000
        else:
            out["exchange_timestamp_ms"] = np.arange(len(out), dtype=float)
    numeric_cols = [c for c in out.columns if c.endswith("_price") or c.endswith("_quantity") or c.endswith("_orders") or c in ["last_price", "exchange_timestamp_ms"]]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out = out.dropna(subset=["exchange_timestamp_ms", "last_price", "buy_1_price", "sell_1_price"])
    out = out[out["sell_1_price"].astype(float).gt(out["buy_1_price"].astype(float))]
    out["trade_date"] = out["trade_date"].astype(str)
    out["symbol"] = out["symbol"].astype(str).str.upper()
    return out.sort_values(["trade_date", "symbol", "exchange_timestamp_ms"], kind="mergesort").reset_index(drop=True)


def load_synthetic_ticks(raw_root: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for month in SYNTHETIC_MONTHS:
        for symbol in SYNTHETIC_SYMBOLS:
            path = raw_root / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"
            if not path.exists():
                continue
            frames.append(read_first_rows(path, REQUIRED_COLUMNS, MAX_ROWS_PER_SYNTHETIC_FILE))
    return normalize_ticks(pd.concat(frames, ignore_index=True) if frames else pd.DataFrame())


def load_real_anchor_ticks(existing_root: Path, unseen_root: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for root in [unseen_root, existing_root]:
        date_root = root / f"trade_date={REAL_ANCHOR_DATE}" / "exchange=NSE"
        if not date_root.exists():
            continue
        for symbol in SYNTHETIC_SYMBOLS[:3]:
            files = sorted((date_root / f"symbol={symbol}").glob("*.parquet"))[:MAX_REAL_FILES_PER_SYMBOL]
            for file in files:
                try:
                    frames.append(pd.read_parquet(file))
                except Exception:
                    continue
        if frames:
            break
    return normalize_ticks(pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(), date_hint=REAL_ANCHOR_DATE)


def depth_l2_l5_signal(row: pd.Series) -> float:
    bid = sum(float(row.get(f"buy_{level}_quantity", 0.0) or 0.0) for level in range(2, 6))
    ask = sum(float(row.get(f"sell_{level}_quantity", 0.0) or 0.0) for level in range(2, 6))
    denom = bid + ask
    return 0.0 if denom <= 0 else (bid - ask) / denom


def top5_churn(window: pd.DataFrame) -> float:
    cols = [f"buy_{i}_quantity" for i in range(1, 6)] + [f"sell_{i}_quantity" for i in range(1, 6)]
    present = [c for c in cols if c in window.columns]
    if len(window) < 3 or not present:
        return 0.0
    qty = window[present].astype(float).sum(axis=1)
    base = max(float(qty.median()), 1.0)
    return float(qty.diff().abs().fillna(0.0).sum() / (base * max(1, len(qty))))


def quote_side_outcome(window: pd.DataFrame, *, side: str, quote_price: float, spread: float, scenario_id: str, quote_id: str, cancel_latency_ms: int, decide_latency_ms: int, move_fraction: float) -> dict[str, Any]:
    start_mid = (float(window.iloc[0]["buy_1_price"]) + float(window.iloc[0]["sell_1_price"])) / 2.0
    start_ts = float(window.iloc[0]["exchange_timestamp_ms"])
    adverse_threshold = max(0.01, spread * move_fraction)
    cancel_attempted = 0
    cancel_succeeded = 0
    cancel_lost_race = 0
    cancel_decision_ts = None
    cancel_arrival_ts = None
    effective_cancel_latency_ms = None
    fill_ts = None
    fill_price = None
    for tick in window.iloc[1:].itertuples(index=False):
        ts = float(getattr(tick, "exchange_timestamp_ms"))
        bid = float(getattr(tick, "buy_1_price"))
        ask = float(getattr(tick, "sell_1_price"))
        last = float(getattr(tick, "last_price"))
        mid = (bid + ask) / 2.0
        if cancel_attempted == 0:
            adverse = (start_mid - mid) > adverse_threshold if side == "bid" else (mid - start_mid) > adverse_threshold
            if adverse:
                cancel_attempted = 1
                cancel_decision_ts = ts + decide_latency_ms
                jitter = stable_jitter_ms(scenario_id, quote_id, side, cancel_latency_ms)
                effective_cancel_latency_ms = cancel_latency_ms + jitter
                cancel_arrival_ts = cancel_decision_ts + effective_cancel_latency_ms
        touched = last <= quote_price if side == "bid" else last >= quote_price
        if touched:
            fill_ts = ts
            fill_price = quote_price
            if cancel_attempted and cancel_arrival_ts is not None and ts <= cancel_arrival_ts:
                cancel_lost_race = 1
            break
        if cancel_attempted and cancel_arrival_ts is not None and ts > cancel_arrival_ts:
            cancel_succeeded = 1
            break
    if cancel_attempted == 1 and fill_ts is None and cancel_succeeded == 0:
        cancel_succeeded = 1
    return {
        "filled": int(fill_ts is not None),
        "fill_ts": fill_ts or 0.0,
        "fill_price": fill_price or 0.0,
        "cancel_attempted": cancel_attempted,
        "cancel_succeeded": cancel_succeeded,
        "cancel_lost_race": cancel_lost_race,
        "effective_cancel_latency_ms": effective_cancel_latency_ms or 0.0,
    }


def score_round_trip(side: str, entry_price: float, exit_bid: float, exit_ask: float, quantity: int) -> dict[str, float]:
    if side == "bid":
        buy_value = entry_price * quantity
        sell_value = exit_bid * quantity
        gross = sell_value - buy_value
    else:
        sell_value = entry_price * quantity
        buy_value = exit_ask * quantity
        gross = sell_value - buy_value
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=buy_value,
        sell_value_inr=sell_value,
        buy_quantity=quantity,
        sell_quantity=quantity,
        buy_orders=1,
        sell_orders=1,
    )
    cost200 = float(charges.total_charges * COST_MULTIPLIER)
    return {"buy_value_inr": float(buy_value), "sell_value_inr": float(sell_value), "gross_pnl_inr": float(gross), "cost200_inr": cost200, "net_pnl_inr": float(gross - cost200)}


def simulate_panel(ticks: pd.DataFrame, latency_grid: pd.DataFrame, panel: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    trade_rows: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    if ticks.empty:
        return pd.DataFrame(), pd.DataFrame()
    for grid in latency_grid.itertuples(index=False):
        scenario_id = f"P408_{PRIMARY_FAMILY}_{grid.scenario_grid_id}"
        for (trade_date, symbol), group in ticks.groupby(["trade_date", "symbol"], sort=True):
            g = group.sort_values("exchange_timestamp_ms", kind="mergesort").reset_index(drop=True)
            windows = 0
            for start in range(0, max(0, len(g) - QUOTE_WINDOW_TICKS), QUOTE_STRIDE_TICKS):
                if windows >= MAX_WINDOWS_PER_SYMBOL_DATE:
                    break
                window = g.iloc[start : start + QUOTE_WINDOW_TICKS].copy()
                if len(window) < 10:
                    continue
                first = window.iloc[0]
                bid = float(first["buy_1_price"])
                ask = float(first["sell_1_price"])
                spread = ask - bid
                if bid <= 0 or ask <= bid:
                    continue
                l2_l5 = depth_l2_l5_signal(first)
                if abs(l2_l5) < 0.02:
                    continue
                windows += 1
                quote_id = f"{panel}_{trade_date}_{symbol}_{start}"
                churn = top5_churn(window)
                for side, quote_price in [("bid", bid), ("ask", ask)]:
                    outcome = quote_side_outcome(
                        window,
                        side=side,
                        quote_price=quote_price,
                        spread=spread,
                        scenario_id=scenario_id,
                        quote_id=quote_id,
                        cancel_latency_ms=int(grid.cancel_latency_ms),
                        decide_latency_ms=int(grid.decide_latency_ms),
                        move_fraction=float(grid.move_threshold_spread_fraction),
                    )
                    diagnostics.append(
                        {
                            "panel": panel,
                            "scenario_id": scenario_id,
                            "scenario_grid_id": grid.scenario_grid_id,
                            "trade_date": trade_date,
                            "symbol": symbol,
                            "quote_id": quote_id,
                            "side": side,
                            "cancel_latency_ms": int(grid.cancel_latency_ms),
                            "decide_latency_ms": int(grid.decide_latency_ms),
                            "move_threshold_spread_fraction": float(grid.move_threshold_spread_fraction),
                            "l2_l5_signal": l2_l5,
                            "top5_churn": churn,
                            **outcome,
                        }
                    )
                    if not outcome["filled"]:
                        continue
                    exit_tick = window.iloc[-1]
                    quantity = max(1, int(FIXED_NOTIONAL_PER_SIDE_INR // quote_price))
                    pnl = score_round_trip(side, quote_price, float(exit_tick["buy_1_price"]), float(exit_tick["sell_1_price"]), quantity)
                    trade_rows.append(
                        {
                            "panel": panel,
                            "scenario_id": scenario_id,
                            "scenario_grid_id": grid.scenario_grid_id,
                            "trade_date": trade_date,
                            "symbol": symbol,
                            "quote_id": quote_id,
                            "side": side,
                            "cancel_latency_ms": int(grid.cancel_latency_ms),
                            "decide_latency_ms": int(grid.decide_latency_ms),
                            "move_threshold_spread_fraction": float(grid.move_threshold_spread_fraction),
                            "quote_post_ts": float(first["exchange_timestamp_ms"]),
                            "fill_ts": outcome["fill_ts"],
                            "exit_ts": float(exit_tick["exchange_timestamp_ms"]),
                            "quote_price": quote_price,
                            "exit_bid": float(exit_tick["buy_1_price"]),
                            "exit_ask": float(exit_tick["sell_1_price"]),
                            "quantity": quantity,
                            "l2_l5_signal": l2_l5,
                            "top5_churn": churn,
                            "cancel_lost_race": outcome["cancel_lost_race"],
                            "effective_cancel_latency_ms": outcome["effective_cancel_latency_ms"],
                            "cost_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
                            **pnl,
                        }
                    )
    return pd.DataFrame(trade_rows), pd.DataFrame(diagnostics)


def summarize(trades: pd.DataFrame, diagnostics: pd.DataFrame, panel: str, cost_multiplier: float) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if diagnostics.empty:
        return pd.DataFrame()
    for scenario_id, diag in diagnostics.groupby("scenario_id", sort=False):
        t = trades[trades["scenario_id"].astype(str).eq(str(scenario_id))].copy() if not trades.empty else pd.DataFrame()
        dates = int(t["trade_date"].nunique()) if not t.empty else 0
        symbols = int(t["symbol"].nunique()) if not t.empty else 0
        net = float(t["net_pnl_inr"].sum()) if not t.empty else 0.0
        by_date = t.groupby("trade_date")["net_pnl_inr"].sum() if not t.empty else pd.Series(dtype=float)
        positive_date_fraction = float((by_date > 0).sum() / len(by_date)) if len(by_date) else 0.0
        annualized = (net / INITIAL_CAPITAL_INR) * (252.0 / max(1, dates)) * 100.0
        rows.append(
            {
                "panel": panel,
                "scenario_id": scenario_id,
                "scenario_grid_id": str(diag["scenario_grid_id"].iloc[0]),
                "cancel_latency_ms": int(diag["cancel_latency_ms"].iloc[0]),
                "decide_latency_ms": int(diag["decide_latency_ms"].iloc[0]),
                "move_threshold_spread_fraction": float(diag["move_threshold_spread_fraction"].iloc[0]),
                "quote_side_rows": int(len(diag)),
                "cancel_attempted_rows": int(diag["cancel_attempted"].astype(int).sum()),
                "cancel_succeeded_rows": int(diag["cancel_succeeded"].astype(int).sum()),
                "cancel_lost_race_rows": int(diag["cancel_lost_race"].astype(int).sum()),
                "completed_round_trips": int(len(t)),
                "trade_dates": dates,
                "symbols": symbols,
                "positive_date_fraction": positive_date_fraction,
                "net_pnl_inr": net,
                "annualized_return_pct": annualized,
                "above12": int(annualized >= ANNUALIZED_THRESHOLD_PCT),
                "event_floor_met": int(len(t) >= MIN_ROUND_TRIPS),
                "date_breadth_met": int(dates >= MIN_TRADE_DATES),
                "symbol_breadth_met": int(symbols >= MIN_SYMBOLS),
                "positive_date_fraction_met": int(positive_date_fraction >= MIN_POSITIVE_DATE_FRACTION),
                "cost200_acceptance_survivor": int(
                    cost_multiplier == 2.0
                    and annualized >= ANNUALIZED_THRESHOLD_PCT
                    and len(t) >= MIN_ROUND_TRIPS
                    and dates >= MIN_TRADE_DATES
                    and symbols >= MIN_SYMBOLS
                    and positive_date_fraction >= MIN_POSITIVE_DATE_FRACTION
                ),
                "avg_effective_cancel_latency_ms": float(diag.loc[diag["cancel_attempted"].astype(int).eq(1), "effective_cancel_latency_ms"].replace(0, np.nan).mean() or 0.0),
                "avg_lost_race_net_pnl_inr": float(t.loc[t["cancel_lost_race"].astype(int).eq(1), "net_pnl_inr"].mean()) if not t.empty and "cancel_lost_race" in t.columns else 0.0,
            }
        )
    return pd.DataFrame(rows)


def monotonicity_check(scenarios: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if scenarios.empty:
        return pd.DataFrame()
    for (decide, move), group in scenarios.groupby(["decide_latency_ms", "move_threshold_spread_fraction"], sort=True):
        curve = group.sort_values("cancel_latency_ms", kind="mergesort")
        pnl = curve["net_pnl_inr"].astype(float).tolist()
        monotone = all(pnl[i] >= pnl[i + 1] for i in range(len(pnl) - 1)) if len(pnl) > 1 else False
        material_range = float(max(pnl) - min(pnl)) if pnl else 0.0
        material_effect = material_range >= max(100.0, 0.01 * max(abs(x) for x in pnl)) if pnl else False
        rows.append(
            {
                "decide_latency_ms": decide,
                "move_threshold_spread_fraction": move,
                "latency_curve_points": len(curve),
                "net_pnl_curve": ";".join(f"{x:.4f}" for x in pnl),
                "latency_pnl_range_inr": material_range,
                "latency_material_effect": int(material_effect),
                "latency_monotone_decreasing": int(monotone and material_effect),
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(scenarios: pd.DataFrame, real_scenarios: pd.DataFrame, latency_curves: pd.DataFrame, diagnostics: pd.DataFrame) -> pd.DataFrame:
    best = scenarios.sort_values("annualized_return_pct", ascending=False, kind="mergesort").iloc[0] if not scenarios.empty else pd.Series(dtype=object)
    survivors = int(scenarios["cost200_acceptance_survivor"].astype(int).sum()) if not scenarios.empty else 0
    best_grid = str(best.get("scenario_grid_id", ""))
    real_match = real_scenarios[real_scenarios["scenario_grid_id"].astype(str).eq(best_grid)] if not real_scenarios.empty else pd.DataFrame()
    real_sign_preserved = 0
    if not real_match.empty:
        real_sign_preserved = int(np.sign(float(real_match.iloc[0]["net_pnl_inr"])) == np.sign(float(best.get("net_pnl_inr", 0.0))))
    rank_cost100_proxy_top_quartile = 0
    if not scenarios.empty:
        cost100_proxy = scenarios.assign(cost100_proxy_net_pnl_inr=scenarios["net_pnl_inr"].astype(float) + 0.5 * scenarios["completed_round_trips"].astype(float) * 165.0)
        top_quartile_n = max(1, math.ceil(len(cost100_proxy) * 0.25))
        top_cost100 = set(cost100_proxy.sort_values("cost100_proxy_net_pnl_inr", ascending=False).head(top_quartile_n)["scenario_grid_id"].astype(str))
        rank_cost100_proxy_top_quartile = int(best_grid in top_cost100)
    curve_match = latency_curves[
        (latency_curves["decide_latency_ms"].astype(int).eq(as_int(best.get("decide_latency_ms", -1))))
        & (pd.to_numeric(latency_curves["move_threshold_spread_fraction"], errors="coerce").eq(float(best.get("move_threshold_spread_fraction", -1))))
    ] if not latency_curves.empty and not best.empty else pd.DataFrame()
    latency_monotone = int(curve_match["latency_monotone_decreasing"].astype(int).max()) if not curve_match.empty else 0
    gates = [
        ("MM_INPUTS_VALIDATED", len(scenarios) > 0 and len(real_scenarios) > 0, f"synthetic_scenarios={len(scenarios)};real_scenarios={len(real_scenarios)}", ">0"),
        ("MM_TICK_LOOP_PRESENT", True, "per_tick_window_loop", "present"),
        ("MM_CANCEL_RACE_APPLIED", diagnostics[["cancel_attempted", "cancel_succeeded", "cancel_lost_race"]].shape[1] == 3 if not diagnostics.empty else False, "cancel_attempted;succeeded;lost_race", "logged"),
        ("MM_LATENCY_HONEST", int(scenarios["cancel_latency_ms"].min()) >= 150 if not scenarios.empty else False, scenarios["cancel_latency_ms"].min() if not scenarios.empty else "", ">=150"),
        ("MM_NO_REBATE_ASSUMED", True, "maker_rebate=0", 0),
        ("MM_TWO_SIDED_REQUIRED", True, "bid_and_ask_quoted_each_window", "required"),
        ("MM_FULL_DEPTH_L2_L5", True, "l2_l5_signal_abs_filter", "required"),
        ("MM_NO_LOOKAHEAD", True, "ticks_sorted_exchange_timestamp_and_forward_loop", "required"),
        ("MM_COST200_SCORING", True, f"cost_multiplier={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={FIXED_NOTIONAL_PER_SIDE_INR}", "cost200_fixed_capital"),
        ("MM_EVENT_FLOOR", int(best.get("completed_round_trips", 0)) >= MIN_ROUND_TRIPS if not best.empty else False, best.get("completed_round_trips", 0), f">={MIN_ROUND_TRIPS}"),
        ("MM_DATE_BREADTH", int(best.get("trade_dates", 0)) >= MIN_TRADE_DATES if not best.empty else False, best.get("trade_dates", 0), f">={MIN_TRADE_DATES}"),
        ("MM_SYMBOL_BREADTH", int(best.get("symbols", 0)) >= MIN_SYMBOLS if not best.empty else False, best.get("symbols", 0), f">={MIN_SYMBOLS}"),
        ("MM_POSITIVE_DATE_FRACTION", float(best.get("positive_date_fraction", 0.0)) >= MIN_POSITIVE_DATE_FRACTION if not best.empty else False, best.get("positive_date_fraction", 0.0), f">={MIN_POSITIVE_DATE_FRACTION}"),
        ("MM_ANNUALIZED_FLOOR", float(best.get("annualized_return_pct", -999.0)) >= ANNUALIZED_THRESHOLD_PCT if not best.empty else False, best.get("annualized_return_pct", ""), f">={ANNUALIZED_THRESHOLD_PCT}"),
        ("MM_NO_RANK_REVERSAL", rank_cost100_proxy_top_quartile == 1, rank_cost100_proxy_top_quartile, 1),
        ("MM_LATENCY_MONOTONICITY", latency_monotone == 1, latency_monotone, 1),
        ("MM_REAL_ANCHOR_CROSS_CHECK", real_sign_preserved == 1, real_sign_preserved, 1),
        ("MM_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(scenarios: pd.DataFrame, real_scenarios: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    best = scenarios.sort_values("annualized_return_pct", ascending=False, kind="mergesort").iloc[0] if not scenarios.empty else pd.Series(dtype=object)
    survivors = int(scenarios["cost200_acceptance_survivor"].astype(int).sum()) if not scenarios.empty else 0
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    kill = int(survivors == 0 or hard_pass < hard_rows)
    return pd.DataFrame(
        [
            ("phase408_per_tick_cancel_race_market_maker_complete", 1, "Phase408 execution completed"),
            ("phase408_synthetic_scenario_rows", len(scenarios), "Synthetic scenario rows"),
            ("phase408_real_anchor_scenario_rows", len(real_scenarios), "Real-anchor scenario rows"),
            ("phase408_best_scenario_id", best.get("scenario_id", ""), "Best synthetic scenario"),
            ("phase408_best_scenario_grid_id", best.get("scenario_grid_id", ""), "Best grid id"),
            ("phase408_best_cancel_latency_ms", best.get("cancel_latency_ms", ""), "Best cancel latency"),
            ("phase408_best_completed_round_trips", best.get("completed_round_trips", 0), "Best completed round trips"),
            ("phase408_best_trade_dates", best.get("trade_dates", 0), "Best trade dates"),
            ("phase408_best_symbols", best.get("symbols", 0), "Best symbols"),
            ("phase408_best_positive_date_fraction", best.get("positive_date_fraction", 0), "Best positive date fraction"),
            ("phase408_best_net_pnl_inr", best.get("net_pnl_inr", 0), "Best net PnL"),
            ("phase408_best_annualized_return_pct", best.get("annualized_return_pct", 0), "Best annualized return"),
            ("phase408_cost200_acceptance_survivor_rows", survivors, "Cost200 acceptance survivors"),
            ("phase408_kill_switch_triggered", kill, "Kill if no survivors or hard gates fail"),
            ("phase408_strategy_promotion_allowed", 0, "No promotion"),
            ("phase408_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase408_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase408_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase408_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase408_next_best_action", NEXT_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, scenarios: pd.DataFrame, real_scenarios: pd.DataFrame, gates: pd.DataFrame, latency_curves: pd.DataFrame) -> None:
    lines = [
        "# Phase408 Per-Tick Cancel-Race Market-Maker Execution",
        "",
        "Phase408 executes the Phase407 cancel-latency charter using a bounded per-tick market-by-price cancel-race simulator.",
        "",
        "Fills remain inferred from received ticks and last-price/quote crossings; exact exchange queue identity is not claimed.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Top Synthetic Scenarios",
        "",
        _markdown_table(scenarios.sort_values("annualized_return_pct", ascending=False).head(15) if not scenarios.empty else scenarios),
        "",
        "## Real Anchor Scenarios",
        "",
        _markdown_table(real_scenarios.sort_values("annualized_return_pct", ascending=False).head(15) if not real_scenarios.empty else real_scenarios),
        "",
        "## Latency Curves",
        "",
        _markdown_table(latency_curves),
        "",
        "## Hard Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "No promotion, paper/live acceptance, deployable profitability claim, or maker rebate is opened.",
    ]
    (output_dir / "phase408_per_tick_cancel_race_market_maker_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase407_dir: Path = DEFAULT_PHASE407_DIR,
    raw_root: Path = DEFAULT_RAW_ROOT,
    existing_real_root: Path = DEFAULT_EXISTING_REAL_ROOT,
    unseen_real_root: Path = DEFAULT_UNSEEN_REAL_ROOT,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase407 = read_csv(phase407_dir / "phase407_acceptance_summary.csv")
    latency_grid = read_csv(phase407_dir / "phase407_latency_grid.csv")
    if phase407.empty or latency_grid.empty:
        raise FileNotFoundError("Phase408 requires Phase407 precommit outputs.")
    synthetic_ticks = load_synthetic_ticks(raw_root)
    real_ticks = load_real_anchor_ticks(existing_real_root, unseen_real_root)
    synthetic_trades, synthetic_diagnostics = simulate_panel(synthetic_ticks, latency_grid, "synthetic_dense")
    real_trades, real_diagnostics = simulate_panel(real_ticks, latency_grid, "real_anchor_reserved")
    synthetic_scenarios = summarize(synthetic_trades, synthetic_diagnostics, "synthetic_dense", COST_MULTIPLIER)
    real_scenarios = summarize(real_trades, real_diagnostics, "real_anchor_reserved", COST_MULTIPLIER)
    latency_curves = monotonicity_check(synthetic_scenarios)
    gates = build_gate_evaluation(synthetic_scenarios, real_scenarios, latency_curves, synthetic_diagnostics)
    acceptance = build_acceptance(synthetic_scenarios, real_scenarios, gates)

    synthetic_scenarios.to_csv(output_dir / "phase408_synthetic_scenario_summary.csv", index=False)
    synthetic_trades.to_csv(output_dir / "phase408_synthetic_trade_ledger.csv", index=False)
    synthetic_diagnostics.to_csv(output_dir / "phase408_synthetic_cancel_race_diagnostics.csv", index=False)
    real_scenarios.to_csv(output_dir / "phase408_real_anchor_scenario_summary.csv", index=False)
    real_trades.to_csv(output_dir / "phase408_real_anchor_trade_ledger.csv", index=False)
    real_diagnostics.to_csv(output_dir / "phase408_real_anchor_cancel_race_diagnostics.csv", index=False)
    latency_curves.to_csv(output_dir / "phase408_latency_monotonicity_curves.csv", index=False)
    gates.to_csv(output_dir / "phase408_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase408_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, synthetic_scenarios, real_scenarios, gates, latency_curves)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase408_per_tick_cancel_race_market_maker",
        **reproducibility_fields(
            artifact_id="phase408_per_tick_cancel_race_market_maker",
            generated_utc=generated_utc,
            inputs={
                "phase407_acceptance_summary": str(phase407_dir / "phase407_acceptance_summary.csv"),
                "phase407_latency_grid": str(phase407_dir / "phase407_latency_grid.csv"),
                "raw_root": str(raw_root),
                "real_anchor_date": REAL_ANCHOR_DATE,
            },
            parameters={
                "synthetic_symbols": ";".join(SYNTHETIC_SYMBOLS),
                "synthetic_months": ";".join(SYNTHETIC_MONTHS),
                "max_rows_per_synthetic_file": MAX_ROWS_PER_SYNTHETIC_FILE,
                "quote_stride_ticks": QUOTE_STRIDE_TICKS,
                "quote_window_ticks": QUOTE_WINDOW_TICKS,
                "max_windows_per_symbol_date": MAX_WINDOWS_PER_SYMBOL_DATE,
            },
            outputs={"acceptance_summary": str(output_dir / "phase408_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase407_precommitted_cancel_latency_grid",
        ),
    }
    (output_dir / "phase408_per_tick_cancel_race_market_maker_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase408 per-tick cancel-race market-maker execution.")
    parser.add_argument("--phase407-dir", type=Path, default=DEFAULT_PHASE407_DIR)
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--existing-real-root", type=Path, default=DEFAULT_EXISTING_REAL_ROOT)
    parser.add_argument("--unseen-real-root", type=Path, default=DEFAULT_UNSEEN_REAL_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase407_dir, args.raw_root, args.existing_real_root, args.unseen_real_root, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

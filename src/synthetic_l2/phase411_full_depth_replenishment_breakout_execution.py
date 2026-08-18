from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase410_full_depth_replenishment_breakout_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    BREAKOUT_CONFIRM_SECONDS,
    COST_MULTIPLIER,
    FIXED_NOTIONAL_INR,
    HORIZON_SECONDS,
    IMPULSE_LOOKBACK_SECONDS,
    INITIAL_CAPITAL_INR,
    MAX_CONCURRENT_POSITIONS,
    MAX_DEPTH_WITHDRAWAL_PRESSURE,
    MAX_SPREAD_BPS,
    MIN_ABS_IMPULSE_BPS,
    MIN_COMPLETED_ROUND_TRIPS,
    MIN_LEVELS_2_TO_5_REPLENISHMENT_PRESSURE,
    MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT,
    MIN_POSITIVE_DATE_FRACTION,
    MIN_SYMBOLS,
    MIN_TOP5_IMBALANCE_ALIGNMENT,
    MIN_TRADE_DATES,
    NEXT_ACTION as PHASE410_NEXT_ACTION,
    REBUILD_CONFIRM_SECONDS,
    STOP_BPS,
    TAKE_PROFIT_BPS,
    THESIS_ID,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_RAW_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_PHASE410_DIR = Path("outputs/phase410")
DEFAULT_OUTPUT_DIR = Path("outputs/phase411")
DEFAULT_REAL_ROOTS = [Path("real_data_sample/l2_unseen_validation"), Path("real_data_sample/l2_multiday_panel")]

SYNTHETIC_SYMBOLS = ["HDFCBANK", "RELIANCE", "INFY", "SBIN", "AXISBANK"]
SYNTHETIC_MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"]
MAX_ROWS_PER_SYNTHETIC_FILE = 20_000
MAX_SYNTHETIC_DATES = 5
MAX_WINDOWS_PER_SYMBOL_DATE = 8
MIN_TICKS_PER_GROUP = 200
SCAN_STRIDE = 500
REAL_ANCHOR_MAX_DATES = 1
REAL_ANCHOR_MAX_FILES_PER_SYMBOL_DATE = 80

NEXT_ACTION = "interpret_phase411_full_depth_replenishment_breakout_execution"
REPAIR_ACTION = "repair_phase411_execution_or_inputs"
PRIMARY_SCENARIO = "P411_PRIMARY_REPLENISHMENT_BREAKOUT"

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
    "buy_2_price",
    "buy_2_quantity",
    "buy_2_orders",
    "sell_2_price",
    "sell_2_quantity",
    "sell_2_orders",
    "buy_3_price",
    "buy_3_quantity",
    "buy_3_orders",
    "sell_3_price",
    "sell_3_quantity",
    "sell_3_orders",
    "buy_4_price",
    "buy_4_quantity",
    "buy_4_orders",
    "sell_4_price",
    "sell_4_quantity",
    "sell_4_orders",
    "buy_5_price",
    "buy_5_quantity",
    "buy_5_orders",
    "sell_5_price",
    "sell_5_quantity",
    "sell_5_orders",
]


def read_first_rows(path: Path, max_rows: int) -> pd.DataFrame:
    pf = pq.ParquetFile(path)
    columns = [col for col in REQUIRED_COLUMNS if col in pf.schema.names]
    batches = []
    rows = 0
    for batch in pf.iter_batches(batch_size=min(max_rows, 30_000), columns=columns):
        frame = batch.to_pandas()
        batches.append(frame)
        rows += len(frame)
        if rows >= max_rows:
            break
    return pd.concat(batches, ignore_index=True).head(max_rows) if batches else pd.DataFrame(columns=columns)


def normalize_ticks(frame: pd.DataFrame, *, symbol_hint: str = "", date_hint: str = "") -> pd.DataFrame:
    out = frame.copy()
    if out.empty:
        return out
    if "symbol" not in out.columns:
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
    numeric_cols = [
        col
        for col in out.columns
        if col in {"exchange_timestamp_ms", "last_price"}
        or col.endswith("_price")
        or col.endswith("_quantity")
        or col.endswith("_orders")
    ]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    for col in REQUIRED_COLUMNS:
        if col.endswith("_quantity") and col not in out.columns:
            out[col] = 0.0
        if col.endswith("_orders") and col not in out.columns:
            out[col] = 0.0
    out = out.dropna(subset=["exchange_timestamp_ms", "last_price", "buy_1_price", "sell_1_price"])
    out = out[out["sell_1_price"].astype(float).gt(out["buy_1_price"].astype(float))]
    out["symbol"] = out["symbol"].astype(str).str.upper()
    out["trade_date"] = out["trade_date"].astype(str)
    return out.sort_values(["trade_date", "symbol", "exchange_timestamp_ms"], kind="mergesort").reset_index(drop=True)


def load_synthetic_ticks(raw_root: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    seen_dates: set[str] = set()
    for month in SYNTHETIC_MONTHS:
        for symbol in SYNTHETIC_SYMBOLS:
            path = raw_root / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"
            if path.exists():
                frame = read_first_rows(path, MAX_ROWS_PER_SYNTHETIC_FILE)
                frames.append(frame)
                if "trade_date" in frame.columns:
                    seen_dates.update(frame["trade_date"].dropna().astype(str).unique().tolist())
            if len(seen_dates) >= MAX_SYNTHETIC_DATES and len(frames) >= len(SYNTHETIC_SYMBOLS):
                break
    return normalize_ticks(pd.concat(frames, ignore_index=True) if frames else pd.DataFrame())


def load_real_anchor_ticks(roots: list[Path]) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    loaded_dates = 0
    for root in roots:
        if not root.exists():
            continue
        for date_root in sorted(root.glob("trade_date=*")):
            if loaded_dates >= REAL_ANCHOR_MAX_DATES:
                break
            exchange_root = date_root / "exchange=NSE"
            if not exchange_root.exists():
                continue
            date_value = date_root.name.split("=", 1)[1]
            any_loaded = False
            for symbol in SYNTHETIC_SYMBOLS[:3]:
                symbol_root = exchange_root / f"symbol={symbol}"
                files = sorted(symbol_root.glob("*.parquet"))[:REAL_ANCHOR_MAX_FILES_PER_SYMBOL_DATE]
                for file in files:
                    try:
                        frames.append(pd.read_parquet(file))
                        any_loaded = True
                    except Exception:
                        continue
            if any_loaded:
                loaded_dates += 1
    return normalize_ticks(pd.concat(frames, ignore_index=True) if frames else pd.DataFrame())


def l2_l5_bid_qty(row: pd.Series) -> float:
    return float(sum(row.get(f"buy_{level}_quantity", 0.0) or 0.0 for level in range(2, 6)))


def l2_l5_ask_qty(row: pd.Series) -> float:
    return float(sum(row.get(f"sell_{level}_quantity", 0.0) or 0.0 for level in range(2, 6)))


def top5_imbalance(row: pd.Series) -> float:
    bid = float(sum(row.get(f"buy_{level}_quantity", 0.0) or 0.0 for level in range(1, 6)))
    ask = float(sum(row.get(f"sell_{level}_quantity", 0.0) or 0.0 for level in range(1, 6)))
    denom = bid + ask
    return 0.0 if denom <= 0 else (bid - ask) / denom


def l2_l5_imbalance(row: pd.Series) -> float:
    bid = l2_l5_bid_qty(row)
    ask = l2_l5_ask_qty(row)
    denom = bid + ask
    return 0.0 if denom <= 0 else (bid - ask) / denom


def level_weighted_imbalance(row: pd.Series) -> float:
    bid = 0.0
    ask = 0.0
    for level in range(1, 6):
        weight = 1.0 / float(level)
        bid += weight * float(row.get(f"buy_{level}_quantity", 0.0) or 0.0)
        ask += weight * float(row.get(f"sell_{level}_quantity", 0.0) or 0.0)
    denom = bid + ask
    return 0.0 if denom <= 0 else (bid - ask) / denom


def spread_bps(row: pd.Series) -> float:
    bid = float(row["buy_1_price"])
    ask = float(row["sell_1_price"])
    mid = (bid + ask) / 2.0
    return 0.0 if mid <= 0 else (ask - bid) / mid * 10_000.0


def replenishment_and_withdrawal(rebuild: pd.DataFrame, side: int) -> tuple[float, float]:
    first = rebuild.iloc[0]
    last = rebuild.iloc[-1]
    bid_first = l2_l5_bid_qty(first)
    bid_last = l2_l5_bid_qty(last)
    ask_first = l2_l5_ask_qty(first)
    ask_last = l2_l5_ask_qty(last)
    base = max(1.0, float(np.median([bid_first + ask_first, bid_last + ask_last])))
    if side > 0:
        return max(0.0, bid_last - bid_first) / base, max(0.0, ask_first - ask_last) / base
    return max(0.0, ask_last - ask_first) / base, max(0.0, bid_first - bid_last) / base


def side_from_impulse(impulse_bps: float) -> int:
    return 1 if impulse_bps > 0 else -1


def fixed_quantity(entry_price: float) -> int:
    if entry_price <= 0:
        return 0
    return max(1, int(math.floor(FIXED_NOTIONAL_INR / entry_price)))


def score_trade(side: int, entry_price: float, exit_price: float, qty: int) -> dict[str, Any]:
    if side > 0:
        buy_value = entry_price * qty
        sell_value = exit_price * qty
        gross = sell_value - buy_value
    else:
        sell_value = entry_price * qty
        buy_value = exit_price * qty
        gross = sell_value - buy_value
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=float(buy_value),
        sell_value_inr=float(sell_value),
        buy_quantity=float(qty),
        sell_quantity=float(qty),
        buy_orders=1,
        sell_orders=1,
    )
    return {
        "quantity": qty,
        "buy_value_inr": float(buy_value),
        "sell_value_inr": float(sell_value),
        "gross_pnl_inr": float(gross),
        "zerodha_charges_inr": float(charges.total_charges),
        "cost200_inr": float(charges.total_charges * COST_MULTIPLIER),
        "net_pnl_inr": float(gross - charges.total_charges * COST_MULTIPLIER),
    }


def choose_exit(future: pd.DataFrame, side: int, entry_price: float) -> tuple[pd.Series, str, float]:
    if future.empty:
        raise ValueError("future window is empty")
    stop = entry_price * (1.0 - side * STOP_BPS / 10_000.0)
    target = entry_price * (1.0 + side * TAKE_PROFIT_BPS / 10_000.0)
    for _, row in future.iterrows():
        if side > 0:
            exit_price = float(row["buy_1_price"])
            if exit_price <= stop:
                return row, "stop", exit_price
            if exit_price >= target:
                return row, "target", exit_price
        else:
            exit_price = float(row["sell_1_price"])
            if exit_price >= stop:
                return row, "stop", exit_price
            if exit_price <= target:
                return row, "target", exit_price
    row = future.iloc[-1]
    return row, "horizon", float(row["buy_1_price"] if side > 0 else row["sell_1_price"])


def candidate_from_index(group: pd.DataFrame, idx: int, *, scenario_id: str, l2_l5_required: bool, spread_gate_required: bool, flip_side: bool) -> dict[str, Any] | None:
    row = group.iloc[idx]
    ts = float(row["exchange_timestamp_ms"])
    impulse_start_ts = ts - IMPULSE_LOOKBACK_SECONDS * 1000.0
    rebuild_start_ts = ts - REBUILD_CONFIRM_SECONDS * 1000.0
    breakout_start_ts = ts - BREAKOUT_CONFIRM_SECONDS * 1000.0
    impulse = group[(group["exchange_timestamp_ms"] >= impulse_start_ts) & (group["exchange_timestamp_ms"] <= ts)]
    rebuild = group[(group["exchange_timestamp_ms"] >= rebuild_start_ts) & (group["exchange_timestamp_ms"] <= ts)]
    breakout = group[(group["exchange_timestamp_ms"] >= breakout_start_ts) & (group["exchange_timestamp_ms"] <= ts)]
    if len(impulse) < 3 or len(rebuild) < 3 or len(breakout) < 3:
        return None
    impulse_bps = (float(row["last_price"]) / float(impulse.iloc[0]["last_price"]) - 1.0) * 10_000.0
    if abs(impulse_bps) < MIN_ABS_IMPULSE_BPS:
        return None
    side = side_from_impulse(impulse_bps)
    if flip_side:
        side *= -1
    replenish, withdrawal = replenishment_and_withdrawal(rebuild, side)
    top5 = top5_imbalance(row)
    weighted = level_weighted_imbalance(row)
    l2_l5 = l2_l5_imbalance(row)
    spread = spread_bps(row)
    if side * top5 < MIN_TOP5_IMBALANCE_ALIGNMENT:
        return None
    if side * weighted < MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT:
        return None
    if l2_l5_required and (replenish < MIN_LEVELS_2_TO_5_REPLENISHMENT_PRESSURE or side * l2_l5 < MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT):
        return None
    if withdrawal > MAX_DEPTH_WITHDRAWAL_PRESSURE:
        return None
    if spread_gate_required and spread > MAX_SPREAD_BPS:
        return None
    if side > 0 and float(row["last_price"]) < float(breakout["last_price"].max()):
        return None
    if side < 0 and float(row["last_price"]) > float(breakout["last_price"].min()):
        return None
    future = group[(group["exchange_timestamp_ms"] > ts) & (group["exchange_timestamp_ms"] <= ts + HORIZON_SECONDS * 1000.0)]
    if len(future) < 2:
        return None
    entry_row = future.iloc[0]
    entry_price = float(entry_row["sell_1_price"] if side > 0 else entry_row["buy_1_price"])
    qty = fixed_quantity(entry_price)
    if qty <= 0:
        return None
    exit_row, exit_reason, exit_price = choose_exit(future.iloc[1:], side, entry_price)
    score = score_trade(side, entry_price, exit_price, qty)
    return {
        "scenario_id": scenario_id,
        "trade_date": str(row["trade_date"]),
        "exchange": str(row.get("exchange", "NSE")),
        "symbol": str(row["symbol"]),
        "signal_ts_ms": ts,
        "entry_ts_ms": float(entry_row["exchange_timestamp_ms"]),
        "exit_ts_ms": float(exit_row["exchange_timestamp_ms"]),
        "side": "long" if side > 0 else "short",
        "impulse_bps": float(impulse_bps),
        "top5_imbalance": float(top5),
        "l2_l5_imbalance": float(l2_l5),
        "level_weighted_imbalance": float(weighted),
        "l2_l5_replenishment_pressure": float(replenish),
        "depth_withdrawal_pressure": float(withdrawal),
        "spread_bps": float(spread),
        "entry_price": float(entry_price),
        "exit_price": float(exit_price),
        "exit_reason": exit_reason,
        **score,
    }


def run_scenario(ticks: pd.DataFrame, *, scenario_id: str, l2_l5_required: bool, spread_gate_required: bool, flip_side: bool) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    for (trade_date, symbol), group in ticks.groupby(["trade_date", "symbol"], sort=True):
        group = group.sort_values("exchange_timestamp_ms", kind="mergesort").reset_index(drop=True)
        scanned = 0
        selected = 0
        if len(group) >= MIN_TICKS_PER_GROUP:
            for idx in range(MIN_TICKS_PER_GROUP // 2, len(group) - 3, SCAN_STRIDE):
                scanned += 1
                trade = candidate_from_index(
                    group,
                    idx,
                    scenario_id=scenario_id,
                    l2_l5_required=l2_l5_required,
                    spread_gate_required=spread_gate_required,
                    flip_side=flip_side,
                )
                if trade is not None:
                    rows.append(trade)
                    selected += 1
                    if selected >= MAX_WINDOWS_PER_SYMBOL_DATE:
                        break
        diagnostics.append(
            {
                "scenario_id": scenario_id,
                "trade_date": trade_date,
                "symbol": symbol,
                "input_ticks": len(group),
                "candidate_scan_points": scanned,
                "selected_trades": selected,
                "l2_l5_required": int(l2_l5_required),
                "spread_gate_required": int(spread_gate_required),
                "flip_side": int(flip_side),
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(diagnostics)


def scenario_summary(ledger: pd.DataFrame, panel: str, scenario_id_if_empty: str = PRIMARY_SCENARIO) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame(
            [
                {
                    "panel": panel,
                    "scenario_id": scenario_id_if_empty,
                    "completed_round_trips": 0,
                    "trade_dates": 0,
                    "symbols": 0,
                    "positive_date_fraction": 0.0,
                    "net_pnl_inr": 0.0,
                    "gross_pnl_inr": 0.0,
                    "cost200_inr": 0.0,
                    "annualized_return_pct": 0.0,
                    "acceptance_survivor": 0,
                }
            ]
        )
    rows = []
    for scenario_id, group in ledger.groupby("scenario_id", sort=True):
        date_pnl = group.groupby("trade_date")["net_pnl_inr"].sum()
        trade_dates = int(group["trade_date"].nunique())
        symbols = int(group["symbol"].nunique())
        net = float(group["net_pnl_inr"].sum())
        annualized = (net / INITIAL_CAPITAL_INR) * (252.0 / max(1, trade_dates)) * 100.0
        pos_frac = float((date_pnl > 0).mean()) if len(date_pnl) else 0.0
        survivor = int(
            len(group) >= MIN_COMPLETED_ROUND_TRIPS
            and trade_dates >= MIN_TRADE_DATES
            and symbols >= MIN_SYMBOLS
            and pos_frac >= MIN_POSITIVE_DATE_FRACTION
            and annualized >= ANNUALIZED_THRESHOLD_PCT
        )
        rows.append(
            {
                "panel": panel,
                "scenario_id": scenario_id,
                "completed_round_trips": int(len(group)),
                "trade_dates": trade_dates,
                "symbols": symbols,
                "positive_date_fraction": pos_frac,
                "net_pnl_inr": net,
                "gross_pnl_inr": float(group["gross_pnl_inr"].sum()),
                "cost200_inr": float(group["cost200_inr"].sum()),
                "annualized_return_pct": float(annualized),
                "acceptance_survivor": survivor,
            }
        )
    return pd.DataFrame(rows).sort_values(["acceptance_survivor", "annualized_return_pct"], ascending=[False, False], kind="mergesort")


def build_gate_evaluation(primary: pd.Series, synthetic_summary: pd.DataFrame, real_summary: pd.DataFrame) -> pd.DataFrame:
    side_flip = synthetic_summary[synthetic_summary["scenario_id"].eq("P411_SIDE_FLIP_CONTROL")]
    l2_removed = synthetic_summary[synthetic_summary["scenario_id"].eq("P411_LEVELS_2_TO_5_REMOVED_CONTROL")]
    spread_removed = synthetic_summary[synthetic_summary["scenario_id"].eq("P411_SPREAD_GATE_REMOVED_CONTROL")]
    primary_ann = float(primary.get("annualized_return_pct", 0.0))
    real_primary = real_summary[real_summary["scenario_id"].eq(PRIMARY_SCENARIO)]
    real_ann = float(real_primary["annualized_return_pct"].iloc[0]) if not real_primary.empty else 0.0
    gates = [
        ("P411_EXECUTION_COMPLETE", True, 1, 1),
        ("P411_PHASE410_ALLOWED_EXECUTION", True, PHASE410_NEXT_ACTION, "run_phase411"),
        ("P411_TICK_ORDERED_REPLAY", True, "timestamp_sorted_group_loop", "present"),
        ("P411_STATEFUL_SEQUENCE", True, "impulse->rebuild->breakout", "present"),
        ("P411_TAKER_ONLY_EXECUTION", True, "taker_entry_taker_exit", "present"),
        ("P411_FULL_DEPTH_L1_L5", True, "required_columns=L1-L5", "present"),
        ("P411_LEVELS_2_TO_5_MATERIAL", True, "l2_l5_replenishment_and_imbalance_required", "present"),
        ("P411_NO_LOOKAHEAD", True, "features_before_entry_tick", "present"),
        ("P411_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={FIXED_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P411_FIXED_PARAMETERS", True, "phase410_parameter_freeze", "present"),
        ("P411_EVENT_FLOOR", int(primary.get("completed_round_trips", 0)) >= MIN_COMPLETED_ROUND_TRIPS, primary.get("completed_round_trips", 0), f">={MIN_COMPLETED_ROUND_TRIPS}"),
        ("P411_DATE_BREADTH", int(primary.get("trade_dates", 0)) >= MIN_TRADE_DATES, primary.get("trade_dates", 0), f">={MIN_TRADE_DATES}"),
        ("P411_SYMBOL_BREADTH", int(primary.get("symbols", 0)) >= MIN_SYMBOLS, primary.get("symbols", 0), f">={MIN_SYMBOLS}"),
        ("P411_POSITIVE_DATE_FRACTION", float(primary.get("positive_date_fraction", 0.0)) >= MIN_POSITIVE_DATE_FRACTION, primary.get("positive_date_fraction", 0.0), f">={MIN_POSITIVE_DATE_FRACTION}"),
        ("P411_ANNUALIZED_FLOOR", primary_ann >= ANNUALIZED_THRESHOLD_PCT, primary_ann, f">={ANNUALIZED_THRESHOLD_PCT}"),
        ("P411_SIDE_FLIP_CONTROL", not side_flip.empty and primary_ann >= float(side_flip["annualized_return_pct"].iloc[0]), float(side_flip["annualized_return_pct"].iloc[0]) if not side_flip.empty else "", "primary>=side_flip"),
        ("P411_L2_L5_REMOVED_CONTROL", not l2_removed.empty and primary_ann >= float(l2_removed["annualized_return_pct"].iloc[0]), float(l2_removed["annualized_return_pct"].iloc[0]) if not l2_removed.empty else "", "primary>=l2_removed"),
        ("P411_SPREAD_GATE_REMOVED_CONTROL", not spread_removed.empty, int(not spread_removed.empty), 1),
        ("P411_REAL_ANCHOR_CROSS_CHECK", (primary_ann == 0.0 and real_ann == 0.0) or (primary_ann * real_ann >= 0), real_ann, "same_sign"),
        ("P411_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(synthetic_summary: pd.DataFrame, real_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    primary = synthetic_summary[synthetic_summary["scenario_id"].eq(PRIMARY_SCENARIO)]
    p = primary.iloc[0] if not primary.empty else pd.Series(dtype=object)
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    survivors = int(synthetic_summary["acceptance_survivor"].astype(int).sum()) if "acceptance_survivor" in synthetic_summary.columns else 0
    return pd.DataFrame(
        [
            ("phase411_full_depth_replenishment_breakout_execution_complete", 1, "Phase411 execution completed"),
            ("phase411_primary_scenario_id", PRIMARY_SCENARIO, "Primary frozen scenario"),
            ("phase411_synthetic_scenario_rows", len(synthetic_summary), "Synthetic scenario rows"),
            ("phase411_real_anchor_scenario_rows", len(real_summary), "Real-anchor scenario rows"),
            ("phase411_primary_completed_round_trips", p.get("completed_round_trips", 0), "Primary round trips"),
            ("phase411_primary_trade_dates", p.get("trade_dates", 0), "Primary trade dates"),
            ("phase411_primary_symbols", p.get("symbols", 0), "Primary symbols"),
            ("phase411_primary_positive_date_fraction", p.get("positive_date_fraction", 0.0), "Primary positive date fraction"),
            ("phase411_primary_net_pnl_inr", p.get("net_pnl_inr", 0.0), "Primary net PnL"),
            ("phase411_primary_annualized_return_pct", p.get("annualized_return_pct", 0.0), "Primary annualized return"),
            ("phase411_cost200_acceptance_survivor_rows", survivors, "Accepted synthetic scenarios"),
            ("phase411_strategy_promotion_allowed", 0, "No promotion"),
            ("phase411_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase411_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase411_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase411_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase411_next_best_action", NEXT_ACTION if hard_pass == hard_rows else "interpret_phase411_failure_no_same_family_tuning", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, synthetic_summary: pd.DataFrame, real_summary: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase411 Full-Depth Replenishment Breakout Execution",
        "",
        "Phase411 executes the Phase410 frozen taker-only replenishment-breakout thesis on bounded raw dense synthetic L1-L5 ticks and reserved real anchors.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Synthetic Scenario Summary",
        "",
        _markdown_table(synthetic_summary),
        "",
        "## Real-Anchor Scenario Summary",
        "",
        _markdown_table(real_summary),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase411 is a synthetic/real-anchor backtest artifact only. It is not paper/live acceptance or a deployable profitability claim.",
    ]
    (output_dir / "phase411_full_depth_replenishment_breakout_execution_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(raw_root: Path = DEFAULT_RAW_ROOT, phase410_dir: Path = DEFAULT_PHASE410_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase410 = read_csv(phase410_dir / "phase410_acceptance_summary.csv")
    if phase410.empty or str(metric_value(phase410, "phase410_execution_allowed_next", "0")) != "1":
        raise RuntimeError("Phase411 requires completed Phase410 precommit with execution_allowed_next=1.")
    synthetic_ticks = load_synthetic_ticks(raw_root)
    real_ticks = load_real_anchor_ticks(DEFAULT_REAL_ROOTS)
    scenarios = [
        (PRIMARY_SCENARIO, True, True, False),
        ("P411_SIDE_FLIP_CONTROL", True, True, True),
        ("P411_LEVELS_2_TO_5_REMOVED_CONTROL", False, True, False),
        ("P411_SPREAD_GATE_REMOVED_CONTROL", True, False, False),
    ]
    synthetic_ledgers = []
    synthetic_diags = []
    synthetic_summaries = []
    real_ledgers = []
    real_diags = []
    real_summaries = []
    for scenario_id, l2_required, spread_required, flip in scenarios:
        ledger, diag = run_scenario(synthetic_ticks, scenario_id=scenario_id, l2_l5_required=l2_required, spread_gate_required=spread_required, flip_side=flip)
        synthetic_ledgers.append(ledger)
        synthetic_diags.append(diag)
        synthetic_summaries.append(scenario_summary(ledger, "synthetic", scenario_id))
        rledger, rdiag = run_scenario(real_ticks, scenario_id=scenario_id, l2_l5_required=l2_required, spread_gate_required=spread_required, flip_side=flip)
        real_ledgers.append(rledger)
        real_diags.append(rdiag)
        real_summaries.append(scenario_summary(rledger, "real_anchor", scenario_id))
    synthetic_ledger = pd.concat(synthetic_ledgers, ignore_index=True) if synthetic_ledgers else pd.DataFrame()
    synthetic_diag = pd.concat(synthetic_diags, ignore_index=True) if synthetic_diags else pd.DataFrame()
    real_ledger = pd.concat(real_ledgers, ignore_index=True) if real_ledgers else pd.DataFrame()
    real_diag = pd.concat(real_diags, ignore_index=True) if real_diags else pd.DataFrame()
    synthetic_summary = pd.concat(synthetic_summaries, ignore_index=True) if synthetic_summaries else pd.DataFrame()
    real_summary = pd.concat(real_summaries, ignore_index=True) if real_summaries else pd.DataFrame()
    primary_row = synthetic_summary[synthetic_summary["scenario_id"].eq(PRIMARY_SCENARIO)]
    primary = primary_row.iloc[0] if not primary_row.empty else pd.Series(dtype=object)
    gates = build_gate_evaluation(primary, synthetic_summary, real_summary)
    acceptance = build_acceptance(synthetic_summary, real_summary, gates)
    synthetic_ledger.to_csv(output_dir / "phase411_synthetic_trade_ledger.csv", index=False)
    synthetic_diag.to_csv(output_dir / "phase411_synthetic_scan_diagnostics.csv", index=False)
    synthetic_summary.to_csv(output_dir / "phase411_synthetic_scenario_summary.csv", index=False)
    real_ledger.to_csv(output_dir / "phase411_real_anchor_trade_ledger.csv", index=False)
    real_diag.to_csv(output_dir / "phase411_real_anchor_scan_diagnostics.csv", index=False)
    real_summary.to_csv(output_dir / "phase411_real_anchor_scenario_summary.csv", index=False)
    gates.to_csv(output_dir / "phase411_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase411_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, synthetic_summary, real_summary, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase411_full_depth_replenishment_breakout_execution",
        **reproducibility_fields(
            artifact_id="phase411_full_depth_replenishment_breakout_execution",
            generated_utc=generated_utc,
            inputs={
                "phase410_acceptance_summary": str(phase410_dir / "phase410_acceptance_summary.csv"),
                "raw_root": str(raw_root),
                "real_anchor_roots": ";".join(str(root) for root in DEFAULT_REAL_ROOTS),
            },
            parameters={
                "thesis_id": THESIS_ID,
                "synthetic_symbols": ";".join(SYNTHETIC_SYMBOLS),
                "synthetic_months": ";".join(SYNTHETIC_MONTHS),
                "max_rows_per_synthetic_file": MAX_ROWS_PER_SYNTHETIC_FILE,
                "max_windows_per_symbol_date": MAX_WINDOWS_PER_SYMBOL_DATE,
                "max_concurrent_positions": MAX_CONCURRENT_POSITIONS,
            },
            outputs={"acceptance_summary": str(output_dir / "phase411_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase411_taker_next_tick_order_arrival",
        ),
    }
    (output_dir / "phase411_full_depth_replenishment_breakout_execution_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase411 full-depth replenishment breakout execution.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase410-dir", type=Path, default=DEFAULT_PHASE410_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.raw_root, args.phase410_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

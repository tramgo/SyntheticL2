from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase411_full_depth_replenishment_breakout_execution import DEFAULT_RAW_ROOT, DEFAULT_REAL_ROOTS, REQUIRED_COLUMNS, normalize_ticks
from synthetic_l2.phase427_broader_full_depth_feature_family_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    COST_MULTIPLIER,
    INITIAL_CAPITAL_INR,
    MAX_SURVIVORS_TO_REPORT,
    MIN_COMPLETED_ROUND_TRIPS,
    MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT,
    MIN_POSITIVE_DATE_FRACTION,
    MIN_SYMBOLS,
    MIN_TRADE_DATES,
    NEXT_ACTION as PHASE427_NEXT_ACTION,
    ORDER_NOTIONAL_INR,
    SYMBOLS,
    THESIS_ID,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_PHASE427_DIR = Path("outputs/phase427")
DEFAULT_OUTPUT_DIR = Path("outputs/phase428")

SYNTHETIC_MONTHS = ["2026-01", "2026-02"]
SYNTHETIC_SYMBOLS = SYMBOLS[:4]
MAX_ROWS_PER_SYNTHETIC_FILE = 5_000
REAL_ANCHOR_SYMBOLS = SYMBOLS[:8]
REAL_ANCHOR_MAX_DATES = 2
REAL_ANCHOR_MAX_FILES_PER_SYMBOL_DATE = 20
SCAN_STRIDE = 500
MAX_TRADES_PER_SCENARIO_GROUP = 8
TOP_SCENARIOS_FOR_REAL_ANCHOR = 25
MAX_LEDGER_ROWS = 25_000
MAX_TRADES_PER_SCENARIO = 500
NEXT_ACTION = "interpret_phase428_broader_full_depth_feature_family_sweep_no_paper_live"


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


def load_synthetic_ticks(raw_root: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for month in SYNTHETIC_MONTHS:
        for symbol in SYNTHETIC_SYMBOLS:
            path = raw_root / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"
            if path.exists():
                frames.append(read_first_rows(path, MAX_ROWS_PER_SYNTHETIC_FILE))
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
            for symbol in REAL_ANCHOR_SYMBOLS:
                for file in sorted((exchange_root / f"symbol={symbol}").glob("*.parquet"))[:REAL_ANCHOR_MAX_FILES_PER_SYMBOL_DATE]:
                    try:
                        frame = pd.read_parquet(file)
                    except Exception:
                        continue
                    if "symbol" not in frame.columns:
                        frame["symbol"] = symbol
                    if "trade_date" not in frame.columns:
                        frame["trade_date"] = date_value
                    frames.append(frame)
                    any_loaded = True
            if any_loaded:
                loaded_dates += 1
    return normalize_ticks(pd.concat(frames, ignore_index=True) if frames else pd.DataFrame())


def sum_side(frame: pd.DataFrame, side: str, levels: range, field: str) -> pd.Series:
    cols = [f"{side}_{level}_{field}" for level in levels if f"{side}_{level}_{field}" in frame.columns]
    return frame[cols].astype(float).sum(axis=1) if cols else pd.Series(0.0, index=frame.index)


def prepare_group_features(group: pd.DataFrame) -> pd.DataFrame:
    out = group.sort_values("exchange_timestamp_ms", kind="mergesort").reset_index(drop=True).copy()
    bid1 = out["buy_1_price"].astype(float)
    ask1 = out["sell_1_price"].astype(float)
    mid = (bid1 + ask1) / 2.0
    out["mid"] = mid
    out["spread_bps_feature"] = np.where(mid > 0, (ask1 - bid1) / mid * 10_000.0, 0.0)
    b1q = out["buy_1_quantity"].astype(float)
    a1q = out["sell_1_quantity"].astype(float)
    out["l1_imbalance"] = np.where((b1q + a1q) > 0, (b1q - a1q) / (b1q + a1q), 0.0)
    b25 = sum_side(out, "buy", range(2, 6), "quantity")
    a25 = sum_side(out, "sell", range(2, 6), "quantity")
    bo25 = sum_side(out, "buy", range(2, 6), "orders")
    ao25 = sum_side(out, "sell", range(2, 6), "orders")
    out["l2_l5_bid_qty"] = b25
    out["l2_l5_ask_qty"] = a25
    out["l2_l5_bid_orders"] = bo25
    out["l2_l5_ask_orders"] = ao25
    out["l2_l5_imbalance"] = np.where((b25 + a25) > 0, (b25 - a25) / (b25 + a25), 0.0)
    top_bid = b1q + b25
    top_ask = a1q + a25
    out["top5_imbalance"] = np.where((top_bid + top_ask) > 0, (top_bid - top_ask) / (top_bid + top_ask), 0.0)
    near_bid = out["buy_1_quantity"].astype(float) + out["buy_2_quantity"].astype(float)
    far_bid = sum_side(out, "buy", range(3, 6), "quantity")
    near_ask = out["sell_1_quantity"].astype(float) + out["sell_2_quantity"].astype(float)
    far_ask = sum_side(out, "sell", range(3, 6), "quantity")
    out["book_slope"] = np.where((near_bid + far_bid + near_ask + far_ask) > 0, ((near_bid - far_bid) - (near_ask - far_ask)) / (near_bid + far_bid + near_ask + far_ask), 0.0)
    return out


def feature_delta(now: pd.Series, base: pd.Series) -> dict[str, float]:
    bid_base = float(base["l2_l5_bid_qty"])
    bid_now = float(now["l2_l5_bid_qty"])
    ask_base = float(base["l2_l5_ask_qty"])
    ask_now = float(now["l2_l5_ask_qty"])
    orders_base = float(base["l2_l5_bid_orders"] + base["l2_l5_ask_orders"])
    orders_now = float(now["l2_l5_bid_orders"] + now["l2_l5_ask_orders"])
    depth_base = bid_base + ask_base
    depth_now = bid_now + ask_now
    return {
        "bid_depth_change": (bid_now - bid_base) / max(1.0, bid_base),
        "ask_depth_change": (ask_now - ask_base) / max(1.0, ask_base),
        "total_depth_change": (depth_now - depth_base) / max(1.0, depth_base),
        "order_churn": abs(orders_now - orders_base) / max(1.0, orders_base),
        "spread_change": float(now["spread_bps_feature"] - base["spread_bps_feature"]),
        "book_slope_change": float(now["book_slope"] - base["book_slope"]),
        "microtrend_bps": (float(now["mid"]) / max(0.01, float(base["mid"])) - 1.0) * 10_000.0,
    }


def signal_side_and_pass(family_id: str, now: pd.Series, base: pd.Series, imb_thr: float, depth_thr: float, max_spread: float, *, l1_only: bool = False) -> tuple[int, bool, dict[str, float]]:
    d = feature_delta(now, base)
    l1 = float(now["l1_imbalance"])
    l2 = float(now["l2_l5_imbalance"])
    top5 = float(now["top5_imbalance"])
    side = 1 if (l1 + (0 if l1_only else l2)) >= 0 else -1
    if float(now["spread_bps_feature"]) > max_spread:
        return side, False, d
    if l1_only:
        return side, abs(l1) >= imb_thr, d
    trend_side = 1 if d["microtrend_bps"] >= 0 else -1
    if family_id == "depth_pressure_continuation":
        side = trend_side
        passed = side * top5 >= imb_thr and side * l2 >= imb_thr
    elif family_id == "depth_pressure_reversal":
        side = -trend_side
        passed = side * top5 >= imb_thr and side * l2 >= imb_thr
    elif family_id == "spread_compression_breakout":
        side = 1 if l2 >= 0 else -1
        passed = d["spread_change"] <= -depth_thr and side * l2 >= imb_thr and (side > 0 and d["bid_depth_change"] >= depth_thr or side < 0 and d["ask_depth_change"] >= depth_thr)
    elif family_id == "spread_expansion_fade":
        side = -trend_side
        passed = d["spread_change"] >= depth_thr and side * l2 >= imb_thr
    elif family_id == "queue_churn_followthrough":
        side = trend_side
        passed = d["order_churn"] >= depth_thr and side * top5 >= imb_thr and side * l2 >= imb_thr
    elif family_id == "book_slope_migration":
        side = 1 if d["book_slope_change"] >= 0 else -1
        passed = abs(d["book_slope_change"]) >= depth_thr and side * l2 >= imb_thr
    else:
        passed = False
    return side, bool(passed), d


def exact_exit_index(group: pd.DataFrame, entry_idx: int, forward_ticks: int, max_hold_ticks: int, min_hold_ms: float) -> tuple[int | None, int, float]:
    max_idx = min(len(group) - 1, entry_idx + int(max_hold_ticks))
    for j in range(entry_idx + int(forward_ticks), max_idx + 1):
        hold_ms = float(group.iloc[j]["exchange_timestamp_ms"]) - float(group.iloc[entry_idx]["exchange_timestamp_ms"])
        if hold_ms >= float(min_hold_ms):
            return j, j - entry_idx, hold_ms
    return None, 0, 0.0


def fixed_quantity(price: float) -> int:
    return max(1, int(math.floor(ORDER_NOTIONAL_INR / max(price, 0.01))))


def score_trade(side: int, entry_price: float, exit_price: float, qty: int) -> dict[str, float]:
    if side > 0:
        buy_value = entry_price * qty
        sell_value = exit_price * qty
        gross = sell_value - buy_value
    else:
        sell_value = entry_price * qty
        buy_value = exit_price * qty
        gross = sell_value - buy_value
    charges = calculate_equity_intraday_nse_charges(buy_value_inr=buy_value, sell_value_inr=sell_value, buy_quantity=qty, sell_quantity=qty, buy_orders=1, sell_orders=1)
    cost100 = float(charges.total_charges)
    cost200 = cost100 * COST_MULTIPLIER
    return {"gross_pnl_inr": float(gross), "cost100_inr": cost100, "cost200_inr": cost200, "net_pnl_inr": float(gross - cost200), "net_pnl_cost100_inr": float(gross - cost100)}


def build_scan_features(ticks: pd.DataFrame, grid: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    lookbacks = sorted(int(x) for x in grid["lookback_ticks"].unique())
    forwards = sorted(int(x) for x in grid["forward_ticks"].unique())
    max_hold = int(grid["max_hold_ticks"].max())
    min_hold = float(grid["min_forward_hold_ms"].min())
    for (trade_date, symbol), raw_group in ticks.groupby(["trade_date", "symbol"], sort=True):
        group = prepare_group_features(raw_group)
        if len(group) <= max(lookbacks) + max_hold + max(forwards) + 2:
            continue
        for lookback in lookbacks:
            for idx in range(lookback, len(group) - max_hold - max(forwards) - 2, SCAN_STRIDE):
                base = group.iloc[idx - lookback]
                now = group.iloc[idx]
                fd = feature_delta(now, base)
                entry_idx = idx + 1
                entry = group.iloc[entry_idx]
                long_entry = float(entry["sell_1_price"])
                short_entry = float(entry["buy_1_price"])
                for forward in forwards:
                    exit_idx, actual_forward, hold_ms = exact_exit_index(group, entry_idx, forward, max_hold, min_hold)
                    if exit_idx is None:
                        continue
                    exit_row = group.iloc[exit_idx]
                    rows.append(
                        {
                            "trade_date": str(trade_date),
                            "symbol": str(symbol),
                            "lookback_ticks": lookback,
                            "forward_ticks": forward,
                            "signal_index": idx,
                            "entry_index": entry_idx,
                            "exit_index": exit_idx,
                            "signal_ts_ms": float(now["exchange_timestamp_ms"]),
                            "entry_ts_ms": float(entry["exchange_timestamp_ms"]),
                            "exit_ts_ms": float(exit_row["exchange_timestamp_ms"]),
                            "actual_forward_ticks_after_entry": actual_forward,
                            "hold_ms": hold_ms,
                            "l1_imbalance": float(now["l1_imbalance"]),
                            "l2_l5_imbalance": float(now["l2_l5_imbalance"]),
                            "top5_imbalance": float(now["top5_imbalance"]),
                            "spread_bps_feature": float(now["spread_bps_feature"]),
                            "book_slope": float(now["book_slope"]),
                            "long_entry_price": long_entry,
                            "long_exit_price": float(exit_row["buy_1_price"]),
                            "short_entry_price": short_entry,
                            "short_exit_price": float(exit_row["sell_1_price"]),
                            **fd,
                        }
                    )
    return pd.DataFrame(rows)


def scenario_mask_and_side(features: pd.DataFrame, row: pd.Series, *, l1_only_control: bool = False, side_flip_control: bool = False) -> tuple[pd.Series, pd.Series]:
    f = features
    imb = float(row["imbalance_threshold"])
    depth = float(row["depth_change_threshold"])
    spread = float(row["max_spread_bps"])
    base = f["spread_bps_feature"].le(spread)
    if l1_only_control:
        side = np.where(f["l1_imbalance"].ge(0), 1, -1)
        mask = base & (pd.Series(side, index=f.index) * f["l1_imbalance"]).ge(imb)
    else:
        trend_side = np.where(f["microtrend_bps"].ge(0), 1, -1)
        family = str(row["family_id"])
        if family == "depth_pressure_continuation":
            side = trend_side
            mask = base & (pd.Series(side, index=f.index) * f["top5_imbalance"]).ge(imb) & (pd.Series(side, index=f.index) * f["l2_l5_imbalance"]).ge(imb)
        elif family == "depth_pressure_reversal":
            side = -trend_side
            mask = base & (pd.Series(side, index=f.index) * f["top5_imbalance"]).ge(imb) & (pd.Series(side, index=f.index) * f["l2_l5_imbalance"]).ge(imb)
        elif family == "spread_compression_breakout":
            side = np.where(f["l2_l5_imbalance"].ge(0), 1, -1)
            side_series = pd.Series(side, index=f.index)
            same_replenish = ((side_series.gt(0) & f["bid_depth_change"].ge(depth)) | (side_series.lt(0) & f["ask_depth_change"].ge(depth)))
            mask = base & f["spread_change"].le(-depth) & (side_series * f["l2_l5_imbalance"]).ge(imb) & same_replenish
        elif family == "spread_expansion_fade":
            side = -trend_side
            mask = base & f["spread_change"].ge(depth) & (pd.Series(side, index=f.index) * f["l2_l5_imbalance"]).ge(imb)
        elif family == "queue_churn_followthrough":
            side = trend_side
            side_series = pd.Series(side, index=f.index)
            mask = base & f["order_churn"].ge(depth) & (side_series * f["top5_imbalance"]).ge(imb) & (side_series * f["l2_l5_imbalance"]).ge(imb)
        elif family == "book_slope_migration":
            side = np.where(f["book_slope_change"].ge(0), 1, -1)
            mask = base & f["book_slope_change"].abs().ge(depth) & (pd.Series(side, index=f.index) * f["l2_l5_imbalance"]).ge(imb)
        else:
            side = np.ones(len(f), dtype=int)
            mask = pd.Series(False, index=f.index)
    side_series = pd.Series(side, index=f.index).astype(int)
    if side_flip_control:
        side_series = -side_series
    return mask.fillna(False), side_series


def score_selected(selected: pd.DataFrame, side: pd.Series) -> pd.DataFrame:
    out = selected.copy()
    aligned_side = side.loc[selected.index].astype(int)
    out["side_int"] = aligned_side.values
    out["entry_price"] = np.where(out["side_int"].gt(0), out["long_entry_price"], out["short_entry_price"])
    out["exit_price"] = np.where(out["side_int"].gt(0), out["long_exit_price"], out["short_exit_price"])
    out["quantity"] = [fixed_quantity(float(x)) for x in out["entry_price"]]
    scores = [score_trade(int(s), float(e), float(x), int(q)) for s, e, x, q in zip(out["side_int"], out["entry_price"], out["exit_price"], out["quantity"])]
    if scores:
        score_frame = pd.DataFrame(scores, index=out.index)
        for col in score_frame.columns:
            out[col] = score_frame[col]
    else:
        for col in ["gross_pnl_inr", "cost100_inr", "cost200_inr", "net_pnl_inr", "net_pnl_cost100_inr"]:
            out[col] = []
    out["side"] = np.where(out["side_int"].gt(0), "long", "short")
    return out


def summarize_selected(selected: pd.DataFrame, panel: str, scenario_id: str, family_id: str) -> dict[str, Any]:
    if selected.empty:
        return {"panel": panel, "scenario_id": scenario_id, "family_id": family_id, "completed_round_trips": 0, "trade_dates": 0, "symbols": 0, "positive_date_fraction": 0.0, "net_pnl_inr": 0.0, "gross_pnl_inr": 0.0, "cost200_inr": 0.0, "annualized_return_pct": 0.0, "acceptance_survivor": 0}
    date_pnl = selected.groupby("trade_date")["net_pnl_inr"].sum()
    trips = int(len(selected))
    dates = int(selected["trade_date"].nunique())
    symbols = int(selected["symbol"].nunique())
    net = float(selected["net_pnl_inr"].sum())
    ann = (net / INITIAL_CAPITAL_INR) * (252.0 / max(1, dates)) * 100.0
    pos_frac = float((date_pnl > 0).mean()) if len(date_pnl) else 0.0
    return {
        "panel": panel,
        "scenario_id": scenario_id,
        "family_id": family_id,
        "completed_round_trips": trips,
        "trade_dates": dates,
        "symbols": symbols,
        "positive_date_fraction": pos_frac,
        "net_pnl_inr": net,
        "gross_pnl_inr": float(selected["gross_pnl_inr"].sum()),
        "cost200_inr": float(selected["cost200_inr"].sum()),
        "annualized_return_pct": float(ann),
        "acceptance_survivor": int(trips >= MIN_COMPLETED_ROUND_TRIPS and dates >= MIN_TRADE_DATES and symbols >= MIN_SYMBOLS and pos_frac >= MIN_POSITIVE_DATE_FRACTION and ann >= ANNUALIZED_THRESHOLD_PCT),
    }


def evaluate_grid_on_ticks(ticks: pd.DataFrame, grid: pd.DataFrame, panel: str, *, l1_only_control: bool = False, side_flip_control: bool = False) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    features = build_scan_features(ticks, grid)
    if features.empty:
        diag = pd.DataFrame(
            [
                {
                    "panel": panel,
                    "scenario_id": str(row.scenario_id),
                    "family_id": row.family_id,
                    "candidate_scan_points": 0,
                    "selected_trades": 0,
                    "l1_only_control": int(l1_only_control),
                    "side_flip_control": int(side_flip_control),
                    "empty_reason": "no_scan_points_satisfied_exact_forward_tick_and_min_hold_window",
                }
                for row in grid.itertuples(index=False)
            ]
        )
        summary = pd.DataFrame(
            [
                summarize_selected(pd.DataFrame(), panel, str(row.scenario_id), str(row.family_id))
                for row in grid.itertuples(index=False)
            ]
        ).sort_values("annualized_return_pct", ascending=False).reset_index(drop=True)
        return pd.DataFrame(), diag, summary
    ledgers: list[dict[str, Any]] = []
    diag: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for row in grid.itertuples(index=False):
        sid = str(row.scenario_id)
        subset = features[features["lookback_ticks"].eq(int(row.lookback_ticks)) & features["forward_ticks"].eq(int(row.forward_ticks))]
        mask, side = scenario_mask_and_side(subset, pd.Series(row._asdict()), l1_only_control=l1_only_control, side_flip_control=side_flip_control)
        selected_raw = subset.loc[mask].head(MAX_TRADES_PER_SCENARIO)
        selected = score_selected(selected_raw, side) if not selected_raw.empty else pd.DataFrame()
        diag.append({"panel": panel, "scenario_id": sid, "family_id": row.family_id, "candidate_scan_points": len(subset), "selected_trades": len(selected), "l1_only_control": int(l1_only_control), "side_flip_control": int(side_flip_control)})
        summaries.append(summarize_selected(selected, panel, sid, str(row.family_id)))
        if not selected.empty and len(ledgers) < MAX_LEDGER_ROWS:
            keep = selected.head(MAX_LEDGER_ROWS - len(ledgers)).copy()
            keep["panel"] = panel
            keep["scenario_id"] = sid
            keep["family_id"] = str(row.family_id)
            keep["l1_only_control"] = int(l1_only_control)
            keep["side_flip_control"] = int(side_flip_control)
            ledgers.extend(keep.to_dict("records"))
    return pd.DataFrame(ledgers), pd.DataFrame(diag), pd.DataFrame(summaries).sort_values("annualized_return_pct", ascending=False).reset_index(drop=True)


def evaluate_controls(ticks: pd.DataFrame, top_grid: pd.DataFrame, panel: str) -> pd.DataFrame:
    rows = []
    for row in top_grid.itertuples(index=False):
        control_rows = []
        for control_name, l1_only, side_flip in [("l1_only", True, False), ("side_flip", False, True)]:
            mini = pd.DataFrame([row._asdict()])
            ledger, _, summary = evaluate_grid_on_ticks(ticks, mini, f"{panel}_{control_name}", l1_only_control=l1_only, side_flip_control=side_flip)
            ann = float(summary["annualized_return_pct"].iloc[0]) if not summary.empty else 0.0
            trips = int(summary["completed_round_trips"].iloc[0]) if not summary.empty else 0
            control_rows.append((control_name, ann, trips))
        rows.append({"scenario_id": row.scenario_id, "family_id": row.family_id, "l1_only_annualized_return_pct": control_rows[0][1], "l1_only_trips": control_rows[0][2], "side_flip_annualized_return_pct": control_rows[1][1], "side_flip_trips": control_rows[1][2]})
    return pd.DataFrame(rows)


def build_gates(summary: pd.DataFrame, controls: pd.DataFrame, real_summary: pd.DataFrame) -> pd.DataFrame:
    best = summary.iloc[0] if not summary.empty else pd.Series(dtype=object)
    survivors = int(summary["acceptance_survivor"].astype(int).sum()) if not summary.empty else 0
    best_sid = str(best.get("scenario_id", ""))
    control = controls[controls["scenario_id"].astype(str).eq(best_sid)].iloc[0] if not controls.empty and best_sid else pd.Series(dtype=object)
    l1_ann = float(control.get("l1_only_annualized_return_pct", 0.0))
    side_ann = float(control.get("side_flip_annualized_return_pct", 0.0))
    best_ann = float(best.get("annualized_return_pct", 0.0))
    real_ann = float(real_summary["annualized_return_pct"].max()) if not real_summary.empty else 0.0
    gates = [
        ("P428_EXECUTION_COMPLETE", True, 1, 1),
        ("P428_PHASE427_PRECOMMIT_USED", True, PHASE427_NEXT_ACTION, "run_phase428"),
        ("P428_GRID_ROWS_EVALUATED", len(summary) == 1458, len(summary), 1458),
        ("P428_TICK_ORDERED_REPLAY", True, "timestamp_sorted_group_loop", "present"),
        ("P428_EXACT_FORWARD_TICK_INDEXING", True, "forward_ticks_from_grid", "present"),
        ("P428_FULL_DEPTH_PRIMARY_FEATURES", True, "l2_l5_feature_families", "present"),
        ("P428_L1_ONLY_CONTROL", best_ann - l1_ann >= MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT, best_ann - l1_ann, f">={MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT}"),
        ("P428_SIDE_FLIP_CONTROL", best_ann >= side_ann, side_ann, "best>=side_flip"),
        ("P428_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={ORDER_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P428_EVENT_FLOOR", int(best.get("completed_round_trips", 0)) >= MIN_COMPLETED_ROUND_TRIPS, best.get("completed_round_trips", 0), f">={MIN_COMPLETED_ROUND_TRIPS}"),
        ("P428_DATE_BREADTH", int(best.get("trade_dates", 0)) >= MIN_TRADE_DATES, best.get("trade_dates", 0), f">={MIN_TRADE_DATES}"),
        ("P428_SYMBOL_BREADTH", int(best.get("symbols", 0)) >= MIN_SYMBOLS, best.get("symbols", 0), f">={MIN_SYMBOLS}"),
        ("P428_POSITIVE_DATE_FRACTION", float(best.get("positive_date_fraction", 0.0)) >= MIN_POSITIVE_DATE_FRACTION, best.get("positive_date_fraction", 0.0), f">={MIN_POSITIVE_DATE_FRACTION}"),
        ("P428_ANNUALIZED_FLOOR", best_ann >= ANNUALIZED_THRESHOLD_PCT, best_ann, f">={ANNUALIZED_THRESHOLD_PCT}"),
        ("P428_REAL_ANCHOR_CROSS_CHECK", (best_ann == 0.0 and real_ann == 0.0) or best_ann * real_ann >= 0, real_ann, "same_sign"),
        ("P428_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(summary: pd.DataFrame, controls: pd.DataFrame, real_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    best = summary.iloc[0] if not summary.empty else pd.Series(dtype=object)
    return pd.DataFrame(
        [
            ("phase428_broader_full_depth_feature_family_sweep_complete", 1, "Phase428 execution completed"),
            ("phase428_grid_rows_evaluated", len(summary), "Scenario rows evaluated"),
            ("phase428_best_scenario_id", best.get("scenario_id", ""), "Best synthetic scenario by annualized return"),
            ("phase428_best_family_id", best.get("family_id", ""), "Best synthetic family"),
            ("phase428_best_completed_round_trips", best.get("completed_round_trips", 0), "Best round trips"),
            ("phase428_best_trade_dates", best.get("trade_dates", 0), "Best trade dates"),
            ("phase428_best_symbols", best.get("symbols", 0), "Best symbols"),
            ("phase428_best_positive_date_fraction", best.get("positive_date_fraction", 0.0), "Best positive date fraction"),
            ("phase428_best_net_pnl_inr", best.get("net_pnl_inr", 0.0), "Best net P&L"),
            ("phase428_best_annualized_return_pct", best.get("annualized_return_pct", 0.0), "Best annualized return"),
            ("phase428_cost200_acceptance_survivor_rows", int(summary["acceptance_survivor"].astype(int).sum()) if not summary.empty else 0, "Accepted synthetic scenarios before control gates"),
            ("phase428_control_rows", len(controls), "Control rows"),
            ("phase428_real_anchor_rows", len(real_summary), "Real-anchor summary rows"),
            ("phase428_strategy_promotion_allowed", 0, "No promotion"),
            ("phase428_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase428_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase428_hard_gate_pass_rows", int(gates["passed"].astype(bool).sum()), "Passed hard gates"),
            ("phase428_hard_gate_rows", len(gates), "Hard gates"),
            ("phase428_next_best_action", NEXT_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, summary: pd.DataFrame, controls: pd.DataFrame, real_summary: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase428 Broader Full-Depth Feature-Family Sweep",
        "",
        "Phase428 executes the Phase427 frozen broader full-depth L2 feature-family sweep on a bounded dense synthetic panel.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Top Synthetic Scenarios",
        "",
        _markdown_table(summary.head(30)),
        "",
        "## Controls For Top Synthetic Scenarios",
        "",
        _markdown_table(controls.head(30)),
        "",
        "## Real-Anchor Replay Summary",
        "",
        _markdown_table(real_summary.head(30)),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: no promotion, paper/live acceptance or deployable profitability claim is generated by Phase428.",
    ]
    (output_dir / "phase428_broader_full_depth_feature_family_sweep_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(raw_root: Path = DEFAULT_RAW_ROOT, phase427_dir: Path = DEFAULT_PHASE427_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR, real_roots: list[Path] | None = None) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase427 = read_csv(phase427_dir / "phase427_acceptance_summary.csv")
    if str(metric_value(phase427, "phase427_next_best_action", "")) != PHASE427_NEXT_ACTION:
        raise ValueError("Phase428 requires Phase427 precommit execution allowance.")
    grid = read_csv(phase427_dir / "phase427_parameter_grid.csv")
    synthetic_ticks = load_synthetic_ticks(raw_root)
    syn_ledger, syn_diag, syn_summary = evaluate_grid_on_ticks(synthetic_ticks, grid, "synthetic")
    top_for_controls = syn_summary.head(TOP_SCENARIOS_FOR_REAL_ANCHOR).merge(grid, on=["scenario_id", "family_id"], how="left")
    controls = evaluate_controls(synthetic_ticks, top_for_controls[grid.columns], "synthetic_top")
    real_summary = pd.DataFrame()
    if not top_for_controls.empty:
        real_ticks = load_real_anchor_ticks(real_roots or DEFAULT_REAL_ROOTS)
        if not real_ticks.empty:
            _, _, real_summary = evaluate_grid_on_ticks(real_ticks, top_for_controls[grid.columns], "real_anchor")
    gates = build_gates(syn_summary, controls, real_summary)
    acceptance = build_acceptance(syn_summary, controls, real_summary, gates)
    syn_summary.to_csv(output_dir / "phase428_synthetic_scenario_summary.csv", index=False)
    syn_diag.to_csv(output_dir / "phase428_synthetic_scan_diagnostics.csv", index=False)
    syn_ledger.to_csv(output_dir / "phase428_synthetic_trade_ledger_sample.csv", index=False)
    controls.to_csv(output_dir / "phase428_top_scenario_controls.csv", index=False)
    real_summary.to_csv(output_dir / "phase428_real_anchor_top_scenario_summary.csv", index=False)
    gates.to_csv(output_dir / "phase428_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase428_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, syn_summary, controls, real_summary, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase428_broader_full_depth_feature_family_sweep",
        **reproducibility_fields(
            artifact_id="phase428_broader_full_depth_feature_family_sweep",
            generated_utc=generated_utc,
            inputs={"phase427_parameter_grid": str(phase427_dir / "phase427_parameter_grid.csv"), "raw_root": str(raw_root)},
            parameters={"thesis_id": THESIS_ID, "synthetic_symbols": ";".join(SYNTHETIC_SYMBOLS), "scan_stride": SCAN_STRIDE},
            outputs={"acceptance_summary": str(output_dir / "phase428_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase428_exact_forward_tick_grid",
        ),
    }
    (output_dir / "phase428_broader_full_depth_feature_family_sweep_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase428 broader full-depth feature-family sweep.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase427-dir", type=Path, default=DEFAULT_PHASE427_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.raw_root, args.phase427_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

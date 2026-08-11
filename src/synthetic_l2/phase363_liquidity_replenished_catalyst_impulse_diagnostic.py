from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow.dataset as ds

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase342_official_catalyst_real_day_survivor_diagnostic_execution import (
    IST_OFFSET_MS,
    MARKET_CLOSE,
    MARKET_OPEN,
    RAW_COLUMNS,
    first_tick_at_or_after,
    ist_timestamp_ms,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_PHASE341_DIR = Path("outputs/phase341")
DEFAULT_PHASE359_DIR = Path("outputs/phase359")
DEFAULT_PHASE362_DIR = Path("outputs/phase362")
DEFAULT_EXISTING_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_UNSEEN_ROOT = Path("real_data_sample/l2_unseen_validation")
DEFAULT_OUTPUT_DIR = Path("outputs/phase363")

INITIAL_CAPITAL_INR = 250_000.0
FIXED_NOTIONAL_INR = 100_000.0
MAX_CONCURRENT_POSITIONS = 2
TRADING_DAYS_PER_YEAR = 252.0
ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30


def utc_second_of_day(ms: int) -> int:
    return int((ms // 1000) % 86_400)


def file_second_of_day(path: Path) -> int | None:
    stem = path.name
    if not stem.startswith("part-") or len(stem) < 11:
        return None
    text = stem[5:11]
    if not text.isdigit():
        return None
    hour = int(text[0:2])
    minute = int(text[2:4])
    second = int(text[4:6])
    return hour * 3600 + minute * 60 + second


def select_window_files(files: list[Path], start_ms: int, end_ms: int) -> list[Path]:
    start_sec = max(0, utc_second_of_day(start_ms) - 180)
    end_sec = min(86_399, utc_second_of_day(end_ms) + 180)
    selected = []
    for path in files:
        sec = file_second_of_day(path)
        if sec is not None and start_sec <= sec <= end_sec:
            selected.append(path)
    return selected or files


def load_raw_window_day_symbol(real_root: Path, trade_date: str, symbol: str, start_ms: int, end_ms: int) -> pd.DataFrame:
    root = real_root / f"trade_date={trade_date}" / "exchange=NSE" / f"symbol={symbol}"
    files = sorted(root.glob("*.parquet"))
    if not files:
        return pd.DataFrame(columns=RAW_COLUMNS)
    files = select_window_files(files, start_ms, end_ms)
    df = ds.dataset([str(path) for path in files], format="parquet", partitioning=None).to_table(columns=RAW_COLUMNS, use_threads=False).to_pandas()
    df = df.dropna(subset=["collector_received_utc_ms", "buy_1_price", "sell_1_price"]).copy()
    if df.empty:
        return df
    df["collector_received_utc_ms"] = df["collector_received_utc_ms"].astype("int64")
    df = df.sort_values(["collector_received_utc_ms", "exchange_timestamp"]).reset_index(drop=True)
    ist_second = ((df["collector_received_utc_ms"].astype("int64") + int(IST_OFFSET_MS)) // 1000) % 86_400
    market_open_second = MARKET_OPEN.hour * 3600 + MARKET_OPEN.minute * 60
    market_close_second = MARKET_CLOSE.hour * 3600 + MARKET_CLOSE.minute * 60
    df = df[
        (ist_second >= market_open_second)
        & (ist_second <= market_close_second)
        & (df["buy_1_price"].astype(float) > 0)
        & (df["sell_1_price"].astype(float) > 0)
        & (df["sell_1_price"].astype(float) >= df["buy_1_price"].astype(float))
    ].copy()
    if df.empty:
        return df
    df["mid"] = (df["buy_1_price"].astype(float) + df["sell_1_price"].astype(float)) / 2.0
    bid_qty_cols = [f"buy_{level}_quantity" for level in range(1, 6)]
    ask_qty_cols = [f"sell_{level}_quantity" for level in range(1, 6)]
    bid_order_cols = [f"buy_{level}_orders" for level in range(1, 6)]
    ask_order_cols = [f"sell_{level}_orders" for level in range(1, 6)]
    df["top5_bid_qty"] = df[bid_qty_cols].astype(float).sum(axis=1)
    df["top5_ask_qty"] = df[ask_qty_cols].astype(float).sum(axis=1)
    df["top5_qty_imbalance"] = (df["top5_bid_qty"] - df["top5_ask_qty"]) / (df["top5_bid_qty"] + df["top5_ask_qty"]).replace(0, pd.NA)
    df["l2_l5_bid_qty"] = df[[f"buy_{level}_quantity" for level in range(2, 6)]].astype(float).sum(axis=1)
    df["l2_l5_ask_qty"] = df[[f"sell_{level}_quantity" for level in range(2, 6)]].astype(float).sum(axis=1)
    df["l2_l5_qty_imbalance"] = (df["l2_l5_bid_qty"] - df["l2_l5_ask_qty"]) / (df["l2_l5_bid_qty"] + df["l2_l5_ask_qty"]).replace(0, pd.NA)
    df["top5_bid_orders"] = df[bid_order_cols].astype(float).sum(axis=1)
    df["top5_ask_orders"] = df[ask_order_cols].astype(float).sum(axis=1)
    df["top5_order_imbalance"] = (df["top5_bid_orders"] - df["top5_ask_orders"]) / (df["top5_bid_orders"] + df["top5_ask_orders"]).replace(0, pd.NA)
    return df


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def normalize_work_orders(phase341_dir: Path, phase359_dir: Path) -> pd.DataFrame:
    old = read_csv(phase341_dir / "phase341_phase342_execution_work_order.csv")
    new = read_csv(phase359_dir / "phase359_phase360_execution_work_order.csv")
    frames: list[pd.DataFrame] = []
    if not old.empty:
        f = old.copy()
        f["canonical_work_order_id"] = f["work_order_id"].astype(str)
        f["panel"] = "existing_phase341"
        frames.append(
            f[
                [
                    "canonical_work_order_id",
                    "panel",
                    "symbol",
                    "announcement_time_ist",
                    "market_session",
                    "diagnostic_trade_date",
                    "diagnostic_start_rule",
                    "description",
                    "no_lookahead_rule_applied",
                ]
            ]
        )
    if not new.empty:
        f = new.copy()
        f["canonical_work_order_id"] = f["phase360_work_order_id"].astype(str)
        f["panel"] = "unseen_phase359"
        frames.append(
            f[
                [
                    "canonical_work_order_id",
                    "panel",
                    "symbol",
                    "announcement_time_ist",
                    "market_session",
                    "diagnostic_trade_date",
                    "diagnostic_start_rule",
                    "description",
                    "no_lookahead_rule_applied",
                ]
            ]
        )
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def root_for(panel: str, existing_root: Path, unseen_root: Path) -> Path:
    return unseen_root if panel == "unseen_phase359" else existing_root


def announcement_start_ms(row: pd.Series) -> int:
    rule = str(row.get("diagnostic_start_rule", ""))
    if rule in {"market_open_next_available_unseen_real_l2_day", "market_open_next_available_real_l2_day", "market_open_same_day"}:
        return ist_timestamp_ms(str(row["diagnostic_trade_date"]), "09:15:00")
    ts = pd.to_datetime(row["announcement_time_ist"], format="%d-%b-%Y %H:%M:%S", errors="coerce")
    if pd.isna(ts):
        return ist_timestamp_ms(str(row["diagnostic_trade_date"]), "09:15:00")
    return int(ts.tz_localize("Asia/Kolkata").tz_convert("UTC").timestamp() * 1000)


def top5_total(row: pd.Series) -> float:
    bid = float(row.get("top5_bid_qty", 0.0) or 0.0)
    ask = float(row.get("top5_ask_qty", 0.0) or 0.0)
    return bid + ask


def build_event_features(work: pd.DataFrame, existing_root: Path, unseen_root: Path, delays: list[int], horizon_seconds: int) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    max_delay = max(delays)
    for item in work.itertuples(index=False):
        item_s = pd.Series(item._asdict())
        start_ms = announcement_start_ms(item_s)
        end_ms = start_ms + (max_delay + horizon_seconds + 60) * 1000
        raw = load_raw_window_day_symbol(root_for(str(item.panel), existing_root, unseen_root), str(item.diagnostic_trade_date), str(item.symbol), start_ms, end_ms)
        start_tick = first_tick_at_or_after(raw, start_ms)
        if start_tick is None:
            for delay in delays:
                rows.append(
                    {
                        "canonical_work_order_id": item.canonical_work_order_id,
                        "panel": item.panel,
                        "symbol": item.symbol,
                        "diagnostic_trade_date": item.diagnostic_trade_date,
                        "decision_delay_seconds": delay,
                        "status": "no_start_tick",
                    }
                )
            continue
        for delay in delays:
            decision_tick = first_tick_at_or_after(raw, int(start_tick["collector_received_utc_ms"]) + delay * 1000)
            if decision_tick is None:
                rows.append(
                    {
                        "canonical_work_order_id": item.canonical_work_order_id,
                        "panel": item.panel,
                        "symbol": item.symbol,
                        "diagnostic_trade_date": item.diagnostic_trade_date,
                        "decision_delay_seconds": delay,
                        "status": "no_decision_tick",
                    }
                )
                continue
            exit_tick = first_tick_at_or_after(raw, int(decision_tick["collector_received_utc_ms"]) + horizon_seconds * 1000)
            forced_exit = 0
            if exit_tick is None:
                exit_tick = raw.iloc[-1]
                forced_exit = 1
            start_mid = float(start_tick["mid"])
            decision_mid = float(decision_tick["mid"])
            exit_mid = float(exit_tick["mid"])
            impulse_bps = ((decision_mid - start_mid) / start_mid * 10_000.0) if start_mid > 0 else 0.0
            side_sign = float(np.sign(impulse_bps))
            start_qty = top5_total(start_tick)
            decision_qty = top5_total(decision_tick)
            replenishment_ratio = ((decision_qty - start_qty) / start_qty) if start_qty > 0 else 0.0
            entry_long_price = float(decision_tick["sell_1_price"])
            exit_long_price = float(exit_tick["buy_1_price"])
            entry_short_price = float(decision_tick["buy_1_price"])
            exit_short_price = float(exit_tick["sell_1_price"])
            rows.append(
                {
                    "canonical_work_order_id": item.canonical_work_order_id,
                    "panel": item.panel,
                    "symbol": item.symbol,
                    "announcement_time_ist": item.announcement_time_ist,
                    "market_session": item.market_session,
                    "diagnostic_trade_date": item.diagnostic_trade_date,
                    "diagnostic_start_rule": item.diagnostic_start_rule,
                    "description": item.description,
                    "decision_delay_seconds": delay,
                    "horizon_seconds": horizon_seconds,
                    "status": "ready",
                    "start_ms": start_ms,
                    "start_tick_ms": int(start_tick["collector_received_utc_ms"]),
                    "decision_ms": int(decision_tick["collector_received_utc_ms"]),
                    "exit_ms": int(exit_tick["collector_received_utc_ms"]),
                    "forced_exit": forced_exit,
                    "start_mid": start_mid,
                    "decision_mid": decision_mid,
                    "exit_mid": exit_mid,
                    "impulse_bps": impulse_bps,
                    "impulse_side_sign": side_sign,
                    "start_top5_qty": start_qty,
                    "decision_top5_qty": decision_qty,
                    "replenishment_ratio": replenishment_ratio,
                    "decision_top5_qty_imbalance": float(decision_tick["top5_qty_imbalance"]) if pd.notna(decision_tick["top5_qty_imbalance"]) else 0.0,
                    "decision_l2_l5_qty_imbalance": float(decision_tick["l2_l5_qty_imbalance"]) if pd.notna(decision_tick["l2_l5_qty_imbalance"]) else 0.0,
                    "decision_top5_order_imbalance": float(decision_tick["top5_order_imbalance"]) if pd.notna(decision_tick["top5_order_imbalance"]) else 0.0,
                    "entry_long_price": entry_long_price,
                    "exit_long_price": exit_long_price,
                    "entry_short_price": entry_short_price,
                    "exit_short_price": exit_short_price,
                }
            )
    return pd.DataFrame(rows)


def costed_pnl(row: pd.Series, side_sign: float) -> tuple[int, float, float, float, float]:
    if side_sign > 0:
        entry = float(row["entry_long_price"])
        exit_price = float(row["exit_long_price"])
        qty = math.floor(FIXED_NOTIONAL_INR / entry) if entry > 0 else 0
        buy_value = qty * entry
        sell_value = qty * exit_price
        gross = sell_value - buy_value
    else:
        entry = float(row["entry_short_price"])
        exit_price = float(row["exit_short_price"])
        qty = math.floor(FIXED_NOTIONAL_INR / entry) if entry > 0 else 0
        sell_value = qty * entry
        buy_value = qty * exit_price
        gross = sell_value - buy_value
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=buy_value,
        sell_value_inr=sell_value,
        buy_quantity=qty,
        sell_quantity=qty,
        buy_orders=1,
        sell_orders=1,
    )
    cost200 = 2.0 * charges.total_charges
    return qty, buy_value, sell_value, gross, gross - cost200


def scenario_trades(events: pd.DataFrame, grid_row: pd.Series, *, control: bool) -> pd.DataFrame:
    ready = events[(events["status"].eq("ready")) & (events["decision_delay_seconds"].astype(int).eq(int(grid_row["decision_delay_seconds"])))].copy()
    if ready.empty:
        return pd.DataFrame()
    impulse_side = np.sign(pd.to_numeric(ready["impulse_bps"], errors="coerce").fillna(0.0))
    depth = pd.to_numeric(ready["decision_l2_l5_qty_imbalance"], errors="coerce").fillna(0.0)
    top5 = pd.to_numeric(ready["decision_top5_qty_imbalance"], errors="coerce").fillna(0.0)
    replenishment = pd.to_numeric(ready["replenishment_ratio"], errors="coerce").fillna(-999.0)
    mask = (
        impulse_side.ne(0)
        & pd.to_numeric(ready["impulse_bps"], errors="coerce").abs().ge(float(grid_row["min_abs_impulse_bps"]))
        & depth.abs().ge(float(grid_row["min_abs_l2_l5_imbalance"]))
        & np.sign(depth).eq(impulse_side)
        & (np.sign(top5).eq(impulse_side) | top5.abs().lt(0.05))
        & replenishment.ge(float(grid_row["min_replenishment_ratio"]))
    )
    selected = ready.loc[mask].copy()
    if selected.empty:
        return pd.DataFrame()
    side = -impulse_side.loc[selected.index] if control else impulse_side.loc[selected.index]
    rows: list[dict[str, Any]] = []
    for idx, row in selected.iterrows():
        side_sign = float(side.loc[idx])
        qty, buy_value, sell_value, gross, net = costed_pnl(row, side_sign)
        out = row.to_dict()
        out.update(
            {
                "scenario_id": str(grid_row["scenario_grid_id"]) + ("_REVERSAL_CONTROL" if control else "_CONTINUATION"),
                "scenario_role": "impulse_reversal_control" if control else "impulse_continuation",
                "side": "long" if side_sign > 0 else "short",
                "side_sign": side_sign,
                "quantity": qty,
                "buy_value_inr": buy_value,
                "sell_value_inr": sell_value,
                "gross_pnl_inr": gross,
                "cost200_inr": gross - net,
                "net_pnl_inr": net,
                "capacity_selected": 0,
                "cost_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            }
        )
        rows.append(out)
    return pd.DataFrame(rows)


def apply_capacity(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return trades
    out = trades.sort_values(["decision_ms", "canonical_work_order_id"]).copy()
    selected: set[str] = set()
    active_exits: list[int] = []
    for row in out.itertuples(index=False):
        active_exits = [x for x in active_exits if x > int(row.decision_ms)]
        if len(active_exits) < MAX_CONCURRENT_POSITIONS:
            selected.add(str(row.canonical_work_order_id))
            active_exits.append(int(row.exit_ms))
    out["capacity_selected"] = [int(str(r.canonical_work_order_id) in selected) for r in out.itertuples(index=False)]
    return out


def summarize(trades: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if trades.empty:
        return pd.DataFrame(columns=["scenario_id", "scenario_role", "scheduled_event_rows", "capacity_selected_trade_rows", "diagnostic_trade_dates", "symbols", "positive_trade_rows", "positive_symbols", "positive_symbol_date_cells", "net_pnl_inr", "annualized_return_pct", "above12", "event_floor_met", "breadth_met", "acceptance_candidate"])
    for scenario_id, frame in trades.groupby("scenario_id"):
        role = str(frame["scenario_role"].iloc[0])
        cap = frame[frame["capacity_selected"].astype(int).eq(1)].copy()
        days = int(cap["diagnostic_trade_date"].nunique()) if not cap.empty else 0
        net = float(cap["net_pnl_inr"].sum()) if not cap.empty else 0.0
        annualized = (net / INITIAL_CAPITAL_INR) * (TRADING_DAYS_PER_YEAR / max(1, days)) * 100.0
        by_symbol = cap.groupby("symbol")["net_pnl_inr"].sum() if not cap.empty else pd.Series(dtype=float)
        by_symbol_date = cap.groupby(["symbol", "diagnostic_trade_date"])["net_pnl_inr"].sum() if not cap.empty else pd.Series(dtype=float)
        rows.append(
            {
                "scenario_id": scenario_id,
                "scenario_role": role,
                "scheduled_event_rows": int(len(frame)),
                "capacity_selected_trade_rows": int(len(cap)),
                "diagnostic_trade_dates": days,
                "symbols": int(cap["symbol"].nunique()) if not cap.empty else 0,
                "positive_trade_rows": int((cap["net_pnl_inr"] > 0).sum()) if not cap.empty else 0,
                "positive_symbols": int((by_symbol > 0).sum()) if not cap.empty else 0,
                "positive_symbol_date_cells": int((by_symbol_date > 0).sum()) if not cap.empty else 0,
                "net_pnl_inr": net,
                "annualized_return_pct": annualized,
                "above12": int(annualized > ANNUALIZED_THRESHOLD_PCT),
                "event_floor_met": int(len(cap) >= ROBUST_EVENT_FLOOR),
                "breadth_met": int((by_symbol > 0).sum() >= 2 and (by_symbol_date > 0).sum() >= 2),
                "acceptance_candidate": int(annualized > ANNUALIZED_THRESHOLD_PCT and len(cap) >= ROBUST_EVENT_FLOOR and (by_symbol > 0).sum() >= 2 and (by_symbol_date > 0).sum() >= 2),
            }
        )
    return pd.DataFrame(rows).sort_values(["annualized_return_pct", "capacity_selected_trade_rows"], ascending=[False, False])


def write_outputs(phase341_dir: Path, phase359_dir: Path, phase362_dir: Path, existing_root: Path, unseen_root: Path, output_dir: Path, max_work_rows: int) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    grid = read_csv(phase362_dir / "phase362_scenario_grid.csv")
    phase362_summary = read_csv(phase362_dir / "phase362_acceptance_summary.csv")
    work = normalize_work_orders(phase341_dir, phase359_dir)
    if work.empty or grid.empty:
        raise FileNotFoundError("Phase363 requires Phase341/Phase359 work orders and Phase362 grid")
    if max_work_rows > 0:
        work = work.head(max_work_rows).copy()
    delays = sorted(grid["decision_delay_seconds"].astype(int).unique().tolist())
    horizon_seconds = int(grid["horizon_seconds"].astype(int).max())
    events = build_event_features(work, existing_root, unseen_root, delays, horizon_seconds)
    trade_frames: list[pd.DataFrame] = []
    for _, row in grid.iterrows():
        trade_frames.append(scenario_trades(events, row, control=False))
        trade_frames.append(scenario_trades(events, row, control=True))
    trades = pd.concat([frame for frame in trade_frames if not frame.empty], ignore_index=True) if trade_frames else pd.DataFrame()
    if not trades.empty:
        trades = pd.concat([apply_capacity(frame) for _, frame in trades.groupby("scenario_id")], ignore_index=True)
    scenarios = summarize(trades)
    best = scenarios.iloc[0].to_dict() if not scenarios.empty else {}
    gates = pd.DataFrame(
        [
            ("P363_PHASE362_PRECOMMIT_PRESENT", int(str(phase362_summary.loc[phase362_summary["metric"].eq("phase362_liquidity_replenished_catalyst_impulse_precommit_complete"), "value"].iloc[0]) == "1") if not phase362_summary.empty else 0, "Phase362 precommit complete"),
            ("P363_WORK_ORDERS_PRESENT", int(len(work) > 0), f"work_rows={len(work)}"),
            ("P363_EVENT_FEATURES_READY", int(events["status"].eq("ready").sum() > 0), f"ready_rows={int(events['status'].eq('ready').sum()) if not events.empty else 0}"),
            ("P363_FULL_DEPTH_FILTER_APPLIED", 1, "uses top5 and levels 2-5 quantity/order features"),
            ("P363_CONTROLS_EXECUTED", int((scenarios["scenario_role"].eq("impulse_reversal_control")).any()) if not scenarios.empty else 0, "reversal controls"),
            ("P363_COST200_FIXED_CAPITAL", int(not trades.empty and trades["cost_model_version"].astype(str).eq(ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION).all()), ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION),
            ("P363_NO_SAME_FAMILY_FADE_RESCUE", 1, "new impulse-continuation family only"),
            ("P363_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    passed = int(gates["passed"].astype(int).sum())
    summary = pd.DataFrame(
        [
            ("phase363_liquidity_replenished_catalyst_impulse_diagnostic_complete", 1, "Phase363 execution completed"),
            ("phase363_work_order_rows", len(work), "Combined Phase341 + Phase359 work orders"),
            ("phase363_max_work_rows", max_work_rows, "Optional smoke limit; 0 means full work order"),
            ("phase363_event_feature_rows", len(events), "Event feature rows"),
            ("phase363_ready_event_feature_rows", int(events["status"].eq("ready").sum()) if not events.empty else 0, "Ready event feature rows"),
            ("phase363_scenario_rows", len(scenarios), "Scenario summary rows"),
            ("phase363_trade_rows", len(trades), "Trade ledger rows"),
            ("phase363_above12_rows", int(scenarios["above12"].sum()) if not scenarios.empty else 0, "Above-12 rows"),
            ("phase363_acceptance_candidate_rows", int(scenarios["acceptance_candidate"].sum()) if not scenarios.empty else 0, "Acceptance candidates"),
            ("phase363_best_scenario_id", best.get("scenario_id", ""), "Best scenario"),
            ("phase363_best_annualized_return_pct", best.get("annualized_return_pct", 0.0), "Best annualized return"),
            ("phase363_best_net_pnl_inr", best.get("net_pnl_inr", 0.0), "Best net PnL"),
            ("phase363_best_capacity_selected_trade_rows", best.get("capacity_selected_trade_rows", 0), "Best selected trades"),
            ("phase363_strategy_promotion_allowed", 0, "No promotion"),
            ("phase363_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase363_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase363_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase363_hard_gate_rows", len(gates), "Hard gates"),
            ("phase363_next_best_action", "interpret_phase363_or_precommit_next_material_real_l2_thesis_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase363_acceptance_summary.csv",
        "events": output_dir / "phase363_event_feature_ledger.csv",
        "trades": output_dir / "phase363_trade_ledger.csv",
        "scenarios": output_dir / "phase363_scenario_summary.csv",
        "gates": output_dir / "phase363_gate_evaluation.csv",
        "report": output_dir / "phase363_liquidity_replenished_catalyst_impulse_diagnostic_report.md",
        "manifest": output_dir / "phase363_liquidity_replenished_catalyst_impulse_diagnostic_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    events.to_csv(outputs["events"], index=False)
    trades.to_csv(outputs["trades"], index=False)
    scenarios.to_csv(outputs["scenarios"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase363 Liquidity-Replenished Catalyst Impulse Diagnostic",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase363 executes the Phase362 materially new impulse-continuation thesis on the current local official-catalyst real-L2 work orders. It uses full top-five depth, levels 2-5 materiality, liquidity replenishment, impulse-reversal controls, Zerodha cost200 fixed-capital scoring, and no paper/live or profitability claim.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Scenario summary",
            "",
            _markdown_table(scenarios.head(20)),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened.",
        ]
    )
    outputs["report"].write_text(report + "\n", encoding="utf-8")
    manifest = {
        "phase": 363,
        "generated_at_utc": generated_utc,
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase363_liquidity_replenished_catalyst_impulse_diagnostic",
            generated_utc=generated_utc,
            inputs={
                "phase341_work_order": str(phase341_dir / "phase341_phase342_execution_work_order.csv"),
                "phase359_work_order": str(phase359_dir / "phase359_phase360_execution_work_order.csv"),
                "phase362_grid": str(phase362_dir / "phase362_scenario_grid.csv"),
            },
            parameters={"initial_capital_inr": INITIAL_CAPITAL_INR, "fixed_notional_inr": FIXED_NOTIONAL_INR, "max_concurrent_positions": MAX_CONCURRENT_POSITIONS, "max_work_rows": max_work_rows},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase362_decision_delay_after_official_catalyst_start",
        ),
        "next_action": str(summary[summary["metric"].eq("phase363_next_best_action")]["value"].iloc[0]),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase341-dir", type=Path, default=DEFAULT_PHASE341_DIR)
    parser.add_argument("--phase359-dir", type=Path, default=DEFAULT_PHASE359_DIR)
    parser.add_argument("--phase362-dir", type=Path, default=DEFAULT_PHASE362_DIR)
    parser.add_argument("--existing-root", type=Path, default=DEFAULT_EXISTING_ROOT)
    parser.add_argument("--unseen-root", type=Path, default=DEFAULT_UNSEEN_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-work-rows", type=int, default=0)
    args = parser.parse_args()
    outputs = write_outputs(args.phase341_dir, args.phase359_dir, args.phase362_dir, args.existing_root, args.unseen_root, args.output_dir, args.max_work_rows)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()

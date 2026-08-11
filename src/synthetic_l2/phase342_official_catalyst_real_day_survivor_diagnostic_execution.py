from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, time, timezone
from pathlib import Path

import duckdb
import pandas as pd
import pyarrow.dataset as ds

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_PHASE341_DIR = Path("outputs/phase341")
DEFAULT_REAL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_OUTPUT_DIR = Path("outputs/phase342")

NEXT_ACTION = "run_phase343_official_catalyst_real_day_diagnostic_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase342_official_catalyst_real_day_survivor_diagnostic_execution"

IST_OFFSET_MS = 5.5 * 60 * 60 * 1000
MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 30)
TRADING_DAYS_PER_YEAR = 252.0

RAW_COLUMNS = [
    "collector_received_utc_ms",
    "exchange_timestamp",
    "last_price",
    "buy_1_price",
    "buy_1_quantity",
    "buy_1_orders",
    "buy_2_price",
    "buy_2_quantity",
    "buy_2_orders",
    "buy_3_price",
    "buy_3_quantity",
    "buy_3_orders",
    "buy_4_price",
    "buy_4_quantity",
    "buy_4_orders",
    "buy_5_price",
    "buy_5_quantity",
    "buy_5_orders",
    "sell_1_price",
    "sell_1_quantity",
    "sell_1_orders",
    "sell_2_price",
    "sell_2_quantity",
    "sell_2_orders",
    "sell_3_price",
    "sell_3_quantity",
    "sell_3_orders",
    "sell_4_price",
    "sell_4_quantity",
    "sell_4_orders",
    "sell_5_price",
    "sell_5_quantity",
    "sell_5_orders",
]


def ist_timestamp_ms(date_text: str, time_text: str) -> int:
    dt = pd.Timestamp(f"{date_text} {time_text}", tz="Asia/Kolkata")
    return int(dt.tz_convert("UTC").timestamp() * 1000)


def announcement_start_ms(row: pd.Series) -> int:
    if row["diagnostic_start_rule"] == "market_open_next_available_real_l2_day":
        return ist_timestamp_ms(str(row["diagnostic_trade_date"]), "09:15:00")
    if row["diagnostic_start_rule"] == "market_open_same_day":
        return ist_timestamp_ms(str(row["diagnostic_trade_date"]), "09:15:00")
    ts = pd.to_datetime(row["announcement_time_ist"], format="%d-%b-%Y %H:%M:%S", errors="coerce")
    if pd.isna(ts):
        return ist_timestamp_ms(str(row["diagnostic_trade_date"]), "09:15:00")
    ts = ts.tz_localize("Asia/Kolkata")
    return int(ts.tz_convert("UTC").timestamp() * 1000)


def load_raw_day_symbol(real_root: Path, trade_date: str, symbol: str) -> pd.DataFrame:
    root = real_root / f"trade_date={trade_date}" / "exchange=NSE" / f"symbol={symbol}"
    files = sorted(root.glob("*.parquet"))
    if not files:
        return pd.DataFrame(columns=RAW_COLUMNS)
    file_list = [str(path) for path in files]
    try:
        df = ds.dataset(file_list, format="parquet", partitioning=None).to_table(columns=RAW_COLUMNS, use_threads=False).to_pandas()
    except Exception:
        try:
            select_cols = ", ".join(RAW_COLUMNS)
            duck_files = [str(path).replace("\\", "/") for path in files]
            df = duckdb.sql(f"select {select_cols} from read_parquet({duck_files}, union_by_name=true)").df()
        except Exception:
            parts = []
            for offset in range(0, len(files), 100):
                batch = files[offset : offset + 100]
                parts.append(pd.concat([pd.read_parquet(path, columns=RAW_COLUMNS) for path in batch], ignore_index=True))
            df = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=RAW_COLUMNS)
    df = df.dropna(subset=["collector_received_utc_ms", "buy_1_price", "sell_1_price"]).copy()
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
    df["mid"] = (df["buy_1_price"].astype(float) + df["sell_1_price"].astype(float)) / 2.0
    df["spread"] = df["sell_1_price"].astype(float) - df["buy_1_price"].astype(float)
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


def first_tick_at_or_after(df: pd.DataFrame, target_ms: int) -> pd.Series | None:
    if df.empty:
        return None
    pos = df["collector_received_utc_ms"].searchsorted(target_ms, side="left")
    if pos >= len(df):
        return None
    return df.iloc[int(pos)]


def diagnostic_row(work: pd.Series, raw: pd.DataFrame) -> dict[str, object]:
    start_ms = announcement_start_ms(work)
    horizon_ms = int(float(work["horizon_seconds"]) * 1000.0)
    entry = first_tick_at_or_after(raw, start_ms)
    if entry is None:
        return {
            "work_order_id": work["work_order_id"],
            "symbol": work["symbol"],
            "diagnostic_trade_date": work["diagnostic_trade_date"],
            "status": "no_entry_tick_after_start",
            "capacity_selected": 0,
        }
    exit_target_ms = int(entry["collector_received_utc_ms"]) + horizon_ms
    exit_tick = first_tick_at_or_after(raw, exit_target_ms)
    forced_exit = 0
    if exit_tick is None:
        exit_tick = raw.iloc[-1]
        forced_exit = 1
    entry_ask = float(entry["sell_1_price"])
    exit_bid = float(exit_tick["buy_1_price"])
    entry_mid = float(entry["mid"])
    exit_mid = float(exit_tick["mid"])
    fixed_notional = float(work["fixed_notional_inr"])
    quantity = math.floor(fixed_notional / entry_ask) if entry_ask > 0 else 0
    buy_value = quantity * entry_ask
    sell_value = quantity * exit_bid
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=buy_value,
        sell_value_inr=sell_value,
        buy_quantity=quantity,
        sell_quantity=quantity,
        buy_orders=1,
        sell_orders=1,
    )
    gross_pnl = sell_value - buy_value
    net_pnl = gross_pnl - (2.0 * charges.total_charges)
    side_flip_gross = buy_value - sell_value
    side_flip_net = side_flip_gross - (2.0 * charges.total_charges)
    return {
        "work_order_id": work["work_order_id"],
        "source_scenario_id": work["source_scenario_id"],
        "symbol": work["symbol"],
        "announcement_time_ist": work["announcement_time_ist"],
        "market_session": work["market_session"],
        "diagnostic_trade_date": work["diagnostic_trade_date"],
        "diagnostic_start_rule": work["diagnostic_start_rule"],
        "description": work["description"],
        "status": "filled",
        "horizon_seconds": int(float(work["horizon_seconds"])),
        "start_ms": start_ms,
        "entry_ms": int(entry["collector_received_utc_ms"]),
        "exit_ms": int(exit_tick["collector_received_utc_ms"]),
        "entry_delay_ms": int(entry["collector_received_utc_ms"]) - start_ms,
        "holding_ms": int(exit_tick["collector_received_utc_ms"]) - int(entry["collector_received_utc_ms"]),
        "forced_exit": forced_exit,
        "entry_mid": entry_mid,
        "exit_mid": exit_mid,
        "mid_return_bps": ((exit_mid - entry_mid) / entry_mid * 10_000.0) if entry_mid else 0.0,
        "entry_bid": float(entry["buy_1_price"]),
        "entry_ask": entry_ask,
        "exit_bid": exit_bid,
        "exit_ask": float(exit_tick["sell_1_price"]),
        "entry_spread": float(entry["spread"]),
        "exit_spread": float(exit_tick["spread"]),
        "entry_top5_qty_imbalance": float(entry["top5_qty_imbalance"]) if pd.notna(entry["top5_qty_imbalance"]) else 0.0,
        "exit_top5_qty_imbalance": float(exit_tick["top5_qty_imbalance"]) if pd.notna(exit_tick["top5_qty_imbalance"]) else 0.0,
        "entry_l2_l5_qty_imbalance": float(entry["l2_l5_qty_imbalance"]) if pd.notna(entry["l2_l5_qty_imbalance"]) else 0.0,
        "exit_l2_l5_qty_imbalance": float(exit_tick["l2_l5_qty_imbalance"]) if pd.notna(exit_tick["l2_l5_qty_imbalance"]) else 0.0,
        "entry_top5_order_imbalance": float(entry["top5_order_imbalance"]) if pd.notna(entry["top5_order_imbalance"]) else 0.0,
        "exit_top5_order_imbalance": float(exit_tick["top5_order_imbalance"]) if pd.notna(exit_tick["top5_order_imbalance"]) else 0.0,
        "quantity": quantity,
        "buy_value_inr": buy_value,
        "sell_value_inr": sell_value,
        "gross_pnl_inr": gross_pnl,
        "zerodha_charges_1x_inr": charges.total_charges,
        "zerodha_charges_2x_inr": 2.0 * charges.total_charges,
        "net_pnl_inr": net_pnl,
        "side_flip_net_pnl_inr": side_flip_net,
        "initial_capital_inr": float(work["initial_capital_inr"]),
        "fixed_notional_inr": fixed_notional,
        "max_concurrent_positions": int(float(work["max_concurrent_positions"])),
        "cost_model_version": charges.model_version,
        "cost_profile": work["cost_profile"],
        "capacity_selected": 0,
    }


def apply_capacity_selection(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return trades
    trades = trades.copy()
    filled = trades[trades["status"].eq("filled")].sort_values(["entry_ms", "work_order_id"]).copy()
    active_exits: list[int] = []
    selected_ids: set[str] = set()
    max_concurrent = int(filled["max_concurrent_positions"].dropna().astype(int).max()) if not filled.empty else 0
    for row in filled.itertuples(index=False):
        active_exits = [exit_ms for exit_ms in active_exits if exit_ms > int(row.entry_ms)]
        if len(active_exits) < max_concurrent:
            selected_ids.add(str(row.work_order_id))
            active_exits.append(int(row.exit_ms))
    trades["capacity_selected"] = trades["work_order_id"].astype(str).isin(selected_ids).astype(int)
    return trades


def portfolio_summary(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    filled = trades[trades["status"].eq("filled")].copy()
    selected = filled[filled["capacity_selected"].astype(int).eq(1)].copy()
    if selected.empty:
        selected = filled.iloc[0:0].copy()
    capital = float(filled["initial_capital_inr"].dropna().max()) if not filled.empty else 0.0
    unique_days = max(1, int(filled["diagnostic_trade_date"].nunique())) if not filled.empty else 1
    rows = []
    for scope_name, frame in [("isolated_all_events_diagnostic", filled), ("capacity_capped_portfolio_diagnostic", selected)]:
        net = float(frame["net_pnl_inr"].sum()) if not frame.empty else 0.0
        side_flip = float(frame["side_flip_net_pnl_inr"].sum()) if not frame.empty else 0.0
        rows.append(
            {
                "scope": scope_name,
                "trade_rows": int(len(frame)),
                "diagnostic_trade_dates": int(frame["diagnostic_trade_date"].nunique()) if not frame.empty else 0,
                "symbols": int(frame["symbol"].nunique()) if not frame.empty else 0,
                "positive_trade_rows": int((frame["net_pnl_inr"] > 0).sum()) if not frame.empty else 0,
                "positive_symbol_date_cells": int(frame[frame["net_pnl_inr"] > 0][["diagnostic_trade_date", "symbol"]].drop_duplicates().shape[0]) if not frame.empty else 0,
                "net_pnl_inr": net,
                "side_flip_net_pnl_inr": side_flip,
                "annualized_return_pct": (net / capital * 100.0 * TRADING_DAYS_PER_YEAR / unique_days) if capital else 0.0,
                "side_flip_annualized_return_pct": (side_flip / capital * 100.0 * TRADING_DAYS_PER_YEAR / unique_days) if capital else 0.0,
                "initial_capital_inr": capital,
                "annualization_diagnostic_days": unique_days,
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(phase341: pd.DataFrame, trades: pd.DataFrame, summary: pd.DataFrame) -> pd.DataFrame:
    phase341_complete = as_int(metric_value(phase341, "phase341_official_catalyst_real_day_survivor_diagnostic_precommit_complete", 0))
    execution_allowed = as_int(metric_value(phase341, "phase341_phase342_execution_allowed_next", 0))
    expected_work = as_int(metric_value(phase341, "phase341_work_order_rows", 0))
    filled_rows = int(trades["status"].eq("filled").sum()) if not trades.empty else 0
    capacity_rows = int(trades["capacity_selected"].astype(int).sum()) if not trades.empty and "capacity_selected" in trades.columns else 0
    rows = [
        ("P342_PHASE341_COMPLETE", phase341_complete == 1, phase341_complete, 1),
        ("P342_EXECUTION_ALLOWED_BY_PRECOMMIT", execution_allowed == 1, execution_allowed, 1),
        ("P342_WORK_ORDER_ROWS_RECONCILED", len(trades) == expected_work, f"{len(trades)}/{expected_work}", "all"),
        ("P342_FILLED_DIAGNOSTIC_ROWS_PRESENT", filled_rows > 0, filled_rows, ">0"),
        ("P342_CAPACITY_CAPPED_ROWS_PRESENT", capacity_rows > 0, capacity_rows, ">0"),
        ("P342_FIXED_CAPITAL_SUMMARY_PRESENT", not summary.empty and "capacity_capped_portfolio_diagnostic" in summary["scope"].astype(str).tolist(), "present", "present"),
        ("P342_COST_MODEL_PINNED", bool(not trades.empty and trades["cost_model_version"].astype(str).eq(ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION).all()), ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "pinned"),
        ("P342_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", True, "closed", "closed"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed", "required"])


def write_outputs(phase341_dir: Path, real_root: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase341 = read_csv(phase341_dir / "phase341_acceptance_summary.csv")
    work = pd.read_csv(phase341_dir / "phase341_phase342_execution_work_order.csv")
    cache: dict[tuple[str, str], pd.DataFrame] = {}
    rows = []
    for item in work.itertuples(index=False):
        row = pd.Series(item._asdict())
        key = (str(row["diagnostic_trade_date"]), str(row["symbol"]))
        if key not in cache:
            cache[key] = load_raw_day_symbol(real_root, key[0], key[1])
        rows.append(diagnostic_row(row, cache[key]))
    trades = apply_capacity_selection(pd.DataFrame(rows))
    portfolio = portfolio_summary(trades)
    gates = build_gate_evaluation(phase341, trades, portfolio)
    passed = int(gates["passed"].astype(bool).sum())
    total = int(len(gates))
    capacity = portfolio[portfolio["scope"].eq("capacity_capped_portfolio_diagnostic")]
    isolated = portfolio[portfolio["scope"].eq("isolated_all_events_diagnostic")]
    cap_row = capacity.iloc[0].to_dict() if not capacity.empty else {}
    iso_row = isolated.iloc[0].to_dict() if not isolated.empty else {}
    summary = pd.DataFrame(
        [
            ("phase342_official_catalyst_real_day_survivor_diagnostic_execution_complete", 1, "Phase342 execution completed"),
            ("phase342_phase341_complete", as_int(metric_value(phase341, "phase341_official_catalyst_real_day_survivor_diagnostic_precommit_complete", 0)), "Phase341 complete"),
            ("phase342_work_order_rows", len(work), "Work-order rows"),
            ("phase342_filled_trade_rows", int(trades["status"].eq("filled").sum()) if not trades.empty else 0, "Rows with entry/exit ticks"),
            ("phase342_capacity_selected_trade_rows", int(trades["capacity_selected"].astype(int).sum()) if not trades.empty else 0, "Capacity-capped selected rows"),
            ("phase342_capacity_capped_net_pnl_inr", cap_row.get("net_pnl_inr", 0.0), "Capacity-capped net PnL"),
            ("phase342_capacity_capped_annualized_return_pct", cap_row.get("annualized_return_pct", 0.0), "Capacity-capped fixed-capital annualized return"),
            ("phase342_capacity_capped_positive_symbol_date_cells", cap_row.get("positive_symbol_date_cells", 0), "Capacity-capped positive symbol-date cells"),
            ("phase342_isolated_all_events_net_pnl_inr", iso_row.get("net_pnl_inr", 0.0), "All isolated-event diagnostic net PnL"),
            ("phase342_isolated_all_events_annualized_return_pct", iso_row.get("annualized_return_pct", 0.0), "All isolated-event diagnostic fixed-capital annualized return"),
            ("phase342_sbin_filled_rows", int(len(trades[(trades["symbol"].eq("SBIN")) & (trades["status"].eq("filled"))])) if not trades.empty else 0, "SBIN filled diagnostic rows"),
            ("phase342_sbin_capacity_selected_rows", int(len(trades[(trades["symbol"].eq("SBIN")) & (trades["capacity_selected"].astype(int).eq(1))])) if not trades.empty else 0, "SBIN capacity-selected rows"),
            ("phase342_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Pinned cost model"),
            ("phase342_cost_profile", "zerodha_2x_all_in_cost_proxy", "2x cost profile"),
            ("phase342_strategy_promotion_allowed", 0, "No promotion"),
            ("phase342_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase342_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase342_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase342_hard_gate_rows", total, "Hard gates"),
            ("phase342_next_best_action", NEXT_ACTION if passed == total else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    report = "\n".join(
        [
            "# Phase342 Official-Catalyst Real-Day Survivor Diagnostic Execution",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "Phase342 executes the no-lookahead official-catalyst diagnostic on local raw Zerodha WebSocket top-five L2 ticks. It is still diagnostic-only.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Portfolio summary",
            "",
            _markdown_table(portfolio),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened by Phase342.",
        ]
    )
    outputs = {
        "summary": output_dir / "phase342_acceptance_summary.csv",
        "trade_ledger": output_dir / "phase342_real_day_trade_diagnostic_ledger.csv",
        "portfolio_summary": output_dir / "phase342_real_day_portfolio_summary.csv",
        "gates": output_dir / "phase342_gate_evaluation.csv",
        "report": output_dir / "phase342_official_catalyst_real_day_survivor_diagnostic_execution_report.md",
        "manifest": output_dir / "phase342_official_catalyst_real_day_survivor_diagnostic_execution_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    trades.to_csv(outputs["trade_ledger"], index=False)
    portfolio.to_csv(outputs["portfolio_summary"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text(report, encoding="utf-8")
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "phase": 342,
        "generated_at_utc": generated_utc,
        "phase341_dir": str(phase341_dir),
        "real_root": str(real_root),
        "output_dir": str(output_dir),
        "date_symbol_cache_rows": len(cache),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase342",
            generated_utc=generated_utc,
            inputs={"phase341_work_order": str(phase341_dir / "phase341_phase342_execution_work_order.csv"), "real_root": str(real_root)},
            parameters={"trading_days_per_year": TRADING_DAYS_PER_YEAR, "cost_profile": "zerodha_2x_all_in_cost_proxy"},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase341-dir", type=Path, default=DEFAULT_PHASE341_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase341_dir, args.real_root, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()

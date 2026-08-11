from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase342_official_catalyst_real_day_survivor_diagnostic_execution import (
    first_tick_at_or_after,
    ist_timestamp_ms,
    load_raw_day_symbol,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_PHASE359_DIR = Path("outputs/phase359")
DEFAULT_UNSEEN_ROOT = Path("real_data_sample/l2_unseen_validation")
DEFAULT_OUTPUT_DIR = Path("outputs/phase360")

PRIMARY_SCENARIO_ID = "P360_UNSEEN_P357_FULL_DEPTH_MARKET_NEUTRAL_DEPTH_2_5_FADE"
TOP5_REFERENCE_ID = "P360_UNSEEN_TOP5_REFERENCE_MARKET_NEUTRAL_FADE"
SIDE_FLIP_ID = "P360_UNSEEN_SIDE_FLIP_CONTROL"
ALT_SIDE_ID = "P360_UNSEEN_DETERMINISTIC_ALTERNATE_SIDE_CONTROL"
INITIAL_CAPITAL_INR = 250_000.0
FIXED_NOTIONAL_INR = 100_000.0
MAX_CONCURRENT_POSITIONS = 2
LOOKBACK_SECONDS = 900
HORIZON_SECONDS = 900
MARKET_NEUTRAL_ABS_BPS = 1.0
TOP5_ABS_THRESHOLD = 0.25
DEEP_ABS_THRESHOLD = 0.25
ROBUST_EVENT_FLOOR = 30
ANNUALIZED_THRESHOLD_PCT = 12.0


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def announcement_start_ms(row: pd.Series) -> int:
    rule = str(row.get("diagnostic_start_rule", ""))
    if rule in {"market_open_next_available_unseen_real_l2_day", "market_open_next_available_real_l2_day", "market_open_same_day"}:
        return ist_timestamp_ms(str(row["diagnostic_trade_date"]), "09:15:00")
    ts = pd.to_datetime(row["announcement_time_ist"], format="%d-%b-%Y %H:%M:%S", errors="coerce")
    if pd.isna(ts):
        return ist_timestamp_ms(str(row["diagnostic_trade_date"]), "09:15:00")
    ts = ts.tz_localize("Asia/Kolkata")
    return int(ts.tz_convert("UTC").timestamp() * 1000)


def raw_cache_loader(real_root: Path):
    cache: dict[tuple[str, str], pd.DataFrame] = {}

    def load(trade_date: str, symbol: str) -> pd.DataFrame:
        key = (str(trade_date), str(symbol).upper())
        if key not in cache:
            cache[key] = load_raw_day_symbol(real_root, key[0], key[1])
        return cache[key]

    return load


def proxy_pre_return_bps(proxy_raw: pd.DataFrame, entry_ms: int) -> float | None:
    if proxy_raw.empty:
        return None
    pre = first_tick_at_or_after(proxy_raw, entry_ms - LOOKBACK_SECONDS * 1000)
    at_entry = first_tick_at_or_after(proxy_raw, entry_ms)
    if pre is None or at_entry is None:
        return None
    pre_mid = float(pre["mid"])
    entry_mid = float(at_entry["mid"])
    if pre_mid <= 0:
        return None
    return (entry_mid - pre_mid) / pre_mid * 10_000.0


def build_event_ledger(work_order: pd.DataFrame, real_root: Path) -> pd.DataFrame:
    load = raw_cache_loader(real_root)
    rows: list[dict[str, Any]] = []
    for work in work_order.itertuples(index=False):
        trade_date = str(work.diagnostic_trade_date)
        symbol = str(work.symbol).upper()
        raw = load(trade_date, symbol)
        start_ms = announcement_start_ms(pd.Series(work._asdict()))
        entry = first_tick_at_or_after(raw, start_ms)
        if entry is None:
            rows.append(
                {
                    "phase360_work_order_id": work.phase360_work_order_id,
                    "symbol": symbol,
                    "diagnostic_trade_date": trade_date,
                    "status": "no_entry_tick_after_start",
                    "eligible_for_primary": 0,
                }
            )
            continue
        exit_tick = first_tick_at_or_after(raw, int(entry["collector_received_utc_ms"]) + HORIZON_SECONDS * 1000)
        forced_exit = 0
        if exit_tick is None:
            exit_tick = raw.iloc[-1]
            forced_exit = 1
        proxy_raw = load(trade_date, "NIFTYBEES")
        proxy_ret = proxy_pre_return_bps(proxy_raw, int(entry["collector_received_utc_ms"]))
        entry_top5 = float(entry["top5_qty_imbalance"]) if pd.notna(entry["top5_qty_imbalance"]) else 0.0
        entry_deep = float(entry["l2_l5_qty_imbalance"]) if pd.notna(entry["l2_l5_qty_imbalance"]) else 0.0
        market_neutral = int(proxy_ret is not None and abs(proxy_ret) <= MARKET_NEUTRAL_ABS_BPS)
        top5_gate = int(abs(entry_top5) >= TOP5_ABS_THRESHOLD)
        deep_gate = int(abs(entry_deep) >= DEEP_ABS_THRESHOLD)
        eligible = int(market_neutral and top5_gate and deep_gate and np.sign(entry_deep) != 0)
        entry_mid = float(entry["mid"])
        quantity = math.floor(FIXED_NOTIONAL_INR / entry_mid) if entry_mid > 0 else 0
        buy_value = quantity * entry_mid
        sell_value = quantity * float(exit_tick["mid"])
        charges = calculate_equity_intraday_nse_charges(
            buy_value_inr=min(buy_value, sell_value),
            sell_value_inr=max(buy_value, sell_value),
            buy_quantity=quantity,
            sell_quantity=quantity,
            buy_orders=1,
            sell_orders=1,
        )
        rows.append(
            {
                "phase360_work_order_id": work.phase360_work_order_id,
                "family_id": work.family_id,
                "source_id": work.source_id,
                "symbol": symbol,
                "announcement_time_ist": work.announcement_time_ist,
                "announcement_date": work.announcement_date,
                "market_session": work.market_session,
                "diagnostic_trade_date": trade_date,
                "diagnostic_start_rule": work.diagnostic_start_rule,
                "description": work.description,
                "status": "filled",
                "start_ms": start_ms,
                "entry_ms": int(entry["collector_received_utc_ms"]),
                "exit_ms": int(exit_tick["collector_received_utc_ms"]),
                "entry_delay_ms": int(entry["collector_received_utc_ms"]) - start_ms,
                "holding_ms": int(exit_tick["collector_received_utc_ms"]) - int(entry["collector_received_utc_ms"]),
                "forced_exit": forced_exit,
                "entry_mid": entry_mid,
                "exit_mid": float(exit_tick["mid"]),
                "quantity": quantity,
                "proxy_symbol": "NIFTYBEES",
                "lookback_seconds": LOOKBACK_SECONDS,
                "proxy_pre_return_bps": proxy_ret if proxy_ret is not None else np.nan,
                "market_neutral_gate": market_neutral,
                "entry_top5_qty_imbalance": entry_top5,
                "entry_l2_l5_qty_imbalance": entry_deep,
                "top5_gate": top5_gate,
                "deep_gate": deep_gate,
                "eligible_for_primary": eligible,
                "zerodha_charges_2x_inr": 2.0 * charges.total_charges,
                "cost_model_version": charges.model_version,
                "initial_capital_inr": INITIAL_CAPITAL_INR,
                "fixed_notional_inr": FIXED_NOTIONAL_INR,
                "max_concurrent_positions": MAX_CONCURRENT_POSITIONS,
            }
        )
    return pd.DataFrame(rows)


def apply_capacity(frame: pd.DataFrame, scenario_id: str) -> pd.DataFrame:
    if frame.empty:
        return frame
    out = frame.sort_values(["entry_ms", "phase360_work_order_id"]).copy()
    active_exits: list[int] = []
    selected: set[str] = set()
    for row in out.itertuples(index=False):
        active_exits = [exit_ms for exit_ms in active_exits if exit_ms > int(row.entry_ms)]
        if len(active_exits) < MAX_CONCURRENT_POSITIONS:
            selected.add(str(row.phase360_work_order_id))
            active_exits.append(int(row.exit_ms))
    out["scenario_id"] = scenario_id
    out["capacity_selected"] = out["phase360_work_order_id"].astype(str).isin(selected).astype(int)
    return out


def score_scenario(base: pd.DataFrame, side: pd.Series, scenario_id: str, scenario_role: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    if base.empty:
        selected = base.copy()
    else:
        selected = base.loc[side.ne(0)].copy()
    if selected.empty:
        row = {
            "scenario_id": scenario_id,
            "scenario_role": scenario_role,
            "scheduled_event_rows": 0,
            "capacity_selected_trade_rows": 0,
            "diagnostic_trade_dates": 0,
            "symbols": 0,
            "positive_symbols": 0,
            "positive_symbol_date_cells": 0,
            "net_pnl_inr": 0.0,
            "annualized_return_pct": 0.0,
            "above12": 0,
            "event_floor_met": 0,
            "breadth_met": 0,
            "acceptance_candidate": 0,
        }
        return selected, row
    selected_side = side.loc[selected.index].astype(float)
    selected["side_sign"] = selected_side
    selected["side"] = np.where(selected_side > 0, "long", "short")
    gross = selected_side * (selected["exit_mid"].astype(float) - selected["entry_mid"].astype(float)) * selected["quantity"].astype(float)
    selected["gross_pnl_inr"] = gross.values
    selected["cost200_inr"] = selected["zerodha_charges_2x_inr"].astype(float).values
    selected["net_pnl_inr"] = selected["gross_pnl_inr"].astype(float) - selected["cost200_inr"].astype(float)
    selected = apply_capacity(selected, scenario_id)
    cap = selected[selected["capacity_selected"].astype(int).eq(1)].copy()
    days = int(cap["diagnostic_trade_date"].nunique()) if not cap.empty else 0
    net_sum = float(cap["net_pnl_inr"].sum()) if not cap.empty else 0.0
    annualized = (net_sum / INITIAL_CAPITAL_INR) * (252.0 / max(1, days)) * 100.0
    by_symbol = cap.groupby("symbol")["net_pnl_inr"].sum() if not cap.empty else pd.Series(dtype=float)
    by_symbol_date = cap.groupby(["symbol", "diagnostic_trade_date"])["net_pnl_inr"].sum() if not cap.empty else pd.Series(dtype=float)
    row = {
        "scenario_id": scenario_id,
        "scenario_role": scenario_role,
        "scheduled_event_rows": int(len(selected)),
        "capacity_selected_trade_rows": int(len(cap)),
        "diagnostic_trade_dates": days,
        "symbols": int(cap["symbol"].nunique()) if not cap.empty else 0,
        "positive_trade_rows": int((cap["net_pnl_inr"] > 0).sum()) if not cap.empty else 0,
        "positive_symbols": int((by_symbol > 0).sum()) if not cap.empty else 0,
        "positive_symbol_date_cells": int((by_symbol_date > 0).sum()) if not cap.empty else 0,
        "net_pnl_inr": net_sum,
        "annualized_return_pct": annualized,
        "above12": int(annualized > ANNUALIZED_THRESHOLD_PCT),
        "event_floor_met": int(len(cap) >= ROBUST_EVENT_FLOOR),
        "breadth_met": int((by_symbol > 0).sum() >= 2 and (by_symbol_date > 0).sum() >= 2),
        "acceptance_candidate": int(annualized > ANNUALIZED_THRESHOLD_PCT and len(cap) >= ROBUST_EVENT_FLOOR and (by_symbol > 0).sum() >= 2 and (by_symbol_date > 0).sum() >= 2),
    }
    return selected, row


def evaluate(phase359_dir: Path, real_root: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    work = read_csv(phase359_dir / "phase359_phase360_execution_work_order.csv")
    phase359_summary = read_csv(phase359_dir / "phase359_acceptance_summary.csv")
    if work.empty:
        raise FileNotFoundError("Phase359 work order is missing or empty")
    events = build_event_ledger(work, real_root)
    filled = events[events["status"].eq("filled")].copy()
    primary_base = filled[filled["eligible_for_primary"].astype(int).eq(1)].copy()
    deep_side = -np.sign(pd.to_numeric(primary_base["entry_l2_l5_qty_imbalance"], errors="coerce").fillna(0.0))
    top5_side = -np.sign(pd.to_numeric(primary_base["entry_top5_qty_imbalance"], errors="coerce").fillna(0.0))
    primary_trades, primary_row = score_scenario(primary_base, deep_side, PRIMARY_SCENARIO_ID, "primary_full_depth_depth_2_5_fade")
    top5_trades, top5_row = score_scenario(primary_base, top5_side, TOP5_REFERENCE_ID, "top5_reference")
    flip_trades, flip_row = score_scenario(primary_base, -deep_side, SIDE_FLIP_ID, "side_flip_control")
    alt_side = pd.Series([1 if i % 2 == 0 else -1 for i in range(len(primary_base))], index=primary_base.index, dtype=float)
    alt_trades, alt_row = score_scenario(primary_base, alt_side, ALT_SIDE_ID, "deterministic_alternate_side_control")
    scenarios = pd.DataFrame([primary_row, top5_row, flip_row, alt_row])
    trades = pd.concat([primary_trades, top5_trades, flip_trades, alt_trades], ignore_index=True) if not primary_base.empty else pd.DataFrame()
    primary = scenarios[scenarios["scenario_id"].eq(PRIMARY_SCENARIO_ID)].iloc[0]
    gates = pd.DataFrame(
        [
            ("P360_PHASE359_COMPLETE", int(str(phase359_summary.loc[phase359_summary["metric"].eq("phase359_local_unseen_real_l2_catalyst_expansion_complete"), "value"].iloc[0]) == "1") if not phase359_summary.empty else 0, "Phase359 complete"),
            ("P360_WORK_ORDER_PRESENT", int(len(work) > 0), f"work_rows={len(work)}"),
            ("P360_FILLED_EVENTS_PRESENT", int(len(filled) > 0), f"filled={len(filled)}"),
            ("P360_FULL_DEPTH_FILTER_APPLIED", 1, f"eligible_primary={len(primary_base)}"),
            ("P360_COST200_FIXED_CAPITAL", int(not trades.empty and trades["cost_model_version"].astype(str).eq(ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION).all()), ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION),
            ("P360_EVENT_FLOOR_CHECKED", 1, f"event_floor_met={primary['event_floor_met']}"),
            ("P360_CONTROLS_EXECUTED", int(len(scenarios) >= 4), f"scenario_rows={len(scenarios)}"),
            ("P360_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    passed = int(gates["passed"].astype(int).sum())
    summary = pd.DataFrame(
        [
            ("phase360_full_depth_market_neutral_fade_unseen_execution_complete", 1, "Phase360 execution completed"),
            ("phase360_phase359_work_order_rows", len(work), "Phase359 work-order rows"),
            ("phase360_filled_event_rows", len(filled), "Filled raw L2 event rows"),
            ("phase360_primary_eligible_event_rows", len(primary_base), "Rows passing market-neutral, top-five and depth 2-5 filters"),
            ("phase360_primary_capacity_selected_trade_rows", primary["capacity_selected_trade_rows"], "Primary capacity-selected rows"),
            ("phase360_primary_diagnostic_trade_dates", primary["diagnostic_trade_dates"], "Primary dates"),
            ("phase360_primary_symbols", primary["symbols"], "Primary symbols"),
            ("phase360_primary_positive_symbols", primary["positive_symbols"], "Primary positive symbols"),
            ("phase360_primary_positive_symbol_date_cells", primary["positive_symbol_date_cells"], "Primary positive symbol/date cells"),
            ("phase360_primary_net_pnl_inr", primary["net_pnl_inr"], "Primary net PnL"),
            ("phase360_primary_annualized_return_pct", primary["annualized_return_pct"], "Primary annualized return"),
            ("phase360_primary_above12", primary["above12"], "Primary above 12%"),
            ("phase360_primary_event_floor_met", primary["event_floor_met"], "Primary >=30 event floor"),
            ("phase360_acceptance_candidate_rows", int(scenarios["acceptance_candidate"].sum()), "Acceptance candidates"),
            ("phase360_strategy_promotion_allowed", 0, "No promotion"),
            ("phase360_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase360_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase360_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase360_hard_gate_rows", len(gates), "Hard gates"),
            ("phase360_next_best_action", "interpret_phase360_and_decide_expand_or_close_no_paper_live", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    return events, trades, scenarios, summary, gates


def write_outputs(phase359_dir: Path, real_root: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    events, trades, scenarios, summary, gates = evaluate(phase359_dir, real_root)
    outputs = {
        "summary": output_dir / "phase360_acceptance_summary.csv",
        "events": output_dir / "phase360_event_ledger.csv",
        "trades": output_dir / "phase360_trade_ledger.csv",
        "scenarios": output_dir / "phase360_scenario_summary.csv",
        "gates": output_dir / "phase360_gate_evaluation.csv",
        "report": output_dir / "phase360_full_depth_market_neutral_fade_on_unseen_real_l2_report.md",
        "manifest": output_dir / "phase360_full_depth_market_neutral_fade_on_unseen_real_l2_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    events.to_csv(outputs["events"], index=False)
    trades.to_csv(outputs["trades"], index=False)
    scenarios.to_csv(outputs["scenarios"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase360 Full-Depth Market-Neutral Fade on Unseen Real L2",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase360 executes the Phase357/358 full-depth market-neutral fade family on the Phase359 unseen official-catalyst real L2 work order. It uses NIFTYBEES 900-second market-neutral context, top-five and depth-levels-2-5 filters, depth-levels-2-5 fade side selection, Zerodha cost200 fixed-capital scoring, and deterministic controls. It opens no promotion, paper/live acceptance, or deployable profitability claim.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Scenario summary",
            "",
            _markdown_table(scenarios),
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
        "phase": 360,
        "generated_at_utc": generated_utc,
        "phase359_dir": str(phase359_dir),
        "real_root": str(real_root),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase360_full_depth_market_neutral_fade_on_unseen_real_l2",
            generated_utc=generated_utc,
            inputs={"phase359_work_order": str(phase359_dir / "phase359_phase360_execution_work_order.csv"), "real_root": str(real_root)},
            parameters={
                "primary_scenario_id": PRIMARY_SCENARIO_ID,
                "lookback_seconds": LOOKBACK_SECONDS,
                "horizon_seconds": HORIZON_SECONDS,
                "market_neutral_abs_bps": MARKET_NEUTRAL_ABS_BPS,
                "top5_abs_threshold": TOP5_ABS_THRESHOLD,
                "deep_abs_threshold": DEEP_ABS_THRESHOLD,
                "event_floor": ROBUST_EVENT_FLOOR,
            },
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase359_unseen_real_l2_first_tick_after_official_catalyst",
        ),
        "next_action": str(summary[summary["metric"].eq("phase360_next_best_action")]["value"].iloc[0]),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase359-dir", type=Path, default=DEFAULT_PHASE359_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_UNSEEN_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase359_dir, args.real_root, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()

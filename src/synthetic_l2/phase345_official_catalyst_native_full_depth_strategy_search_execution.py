from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase342_official_catalyst_real_day_survivor_diagnostic_execution import (
    TRADING_DAYS_PER_YEAR,
    announcement_start_ms,
    first_tick_at_or_after,
    load_raw_day_symbol,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_PHASE344_DIR = Path("outputs/phase344")
DEFAULT_PHASE341_DIR = Path("outputs/phase341")
DEFAULT_PHASE342_DIR = Path("outputs/phase342")
DEFAULT_REAL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_OUTPUT_DIR = Path("outputs/phase345")

NEXT_ACTION = "run_phase346_official_catalyst_native_search_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase345_official_catalyst_native_full_depth_strategy_search_execution"

ANNUALIZED_THRESHOLD_PCT = 12.0
ROBUST_EVENT_FLOOR = 30
INITIAL_CAPITAL_INR = 250_000.0
FIXED_NOTIONAL_INR = 100_000.0
MAX_CONCURRENT_POSITIONS = 2


def stable_unit_hash(text: str) -> float:
    raw = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return int(raw, 16) / float(16**12 - 1)


def trade_pnl(entry: pd.Series, exit_tick: pd.Series, side: str) -> dict[str, float]:
    if side == "short":
        entry_price = float(entry["buy_1_price"])
        exit_price = float(exit_tick["sell_1_price"])
        quantity = math.floor(FIXED_NOTIONAL_INR / entry_price) if entry_price > 0 else 0
        sell_value = quantity * entry_price
        buy_value = quantity * exit_price
        gross = sell_value - buy_value
    else:
        entry_price = float(entry["sell_1_price"])
        exit_price = float(exit_tick["buy_1_price"])
        quantity = math.floor(FIXED_NOTIONAL_INR / entry_price) if entry_price > 0 else 0
        buy_value = quantity * entry_price
        sell_value = quantity * exit_price
        gross = sell_value - buy_value
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=buy_value,
        sell_value_inr=sell_value,
        buy_quantity=quantity,
        sell_quantity=quantity,
        buy_orders=1,
        sell_orders=1,
    )
    return {
        "quantity": float(quantity),
        "buy_value_inr": float(buy_value),
        "sell_value_inr": float(sell_value),
        "gross_pnl_inr": float(gross),
        "zerodha_charges_2x_inr": float(2.0 * charges.total_charges),
        "net_pnl_inr": float(gross - 2.0 * charges.total_charges),
    }


def side_from_policy(family_id: str, entry: pd.Series, row_id: str) -> str:
    if family_id == "P344_CATALYST_CATEGORY_CONTINUATION":
        return "long"
    if family_id == "P344_FULL_DEPTH_CATALYST_REACTION_FILTER":
        return "long" if float(entry["l2_l5_qty_imbalance"]) >= 0.0 else "short"
    if family_id == "P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC":
        pressure = float(entry["top5_qty_imbalance"]) + float(entry["l2_l5_qty_imbalance"])
        return "long" if pressure >= 0.0 else "short"
    return "long"


def eligible_for_family(family_id: str, event: pd.Series) -> bool:
    desc = str(event["description"])
    symbol = str(event["symbol"])
    if family_id == "P344_CATALYST_CATEGORY_CONTINUATION":
        return desc in {"General Updates", "Updates"}
    if family_id == "P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC":
        return symbol in {"SBIN", "AXISBANK", "HDFCBANK", "ICICIBANK", "KOTAKBANK"}
    if family_id == "P344_NEGATIVE_CONTROL_FAILED_SURVIVOR_REPLAY":
        return True
    return True


def threshold_pass(family_id: str, entry: pd.Series, quantile: float, thresholds: dict[str, dict[float, float]]) -> bool:
    if quantile <= 0.0 or family_id == "P344_NEGATIVE_CONTROL_FAILED_SURVIVOR_REPLAY":
        return True
    metric = "l2_l5_abs" if family_id == "P344_FULL_DEPTH_CATALYST_REACTION_FILTER" else "top5_abs"
    value = abs(float(entry["l2_l5_qty_imbalance"])) if metric == "l2_l5_abs" else abs(float(entry["top5_qty_imbalance"]))
    return value >= thresholds.get(metric, {}).get(float(quantile), 0.0)


def scenario_trade(row: pd.Series, event: pd.Series, raw: pd.DataFrame, thresholds: dict[str, dict[float, float]]) -> dict[str, object]:
    family_id = str(row["family_id"])
    if not eligible_for_family(family_id, event):
        return {"status": "family_event_filter_skip"}
    start_ms = announcement_start_ms(event)
    timing = str(row["entry_timing_policy"])
    if timing == "delay_60s":
        start_ms += 60_000
    elif timing == "delay_300s":
        start_ms += 300_000
    elif timing == "phase342_exact":
        start_ms = announcement_start_ms(event)
    entry = first_tick_at_or_after(raw, start_ms)
    if entry is None:
        return {"status": "no_entry_tick"}
    if not threshold_pass(family_id, entry, float(row["depth_threshold_quantile"]), thresholds):
        return {"status": "depth_threshold_skip"}
    exit_tick = first_tick_at_or_after(raw, int(entry["collector_received_utc_ms"]) + int(row["horizon_seconds"]) * 1000)
    forced_exit = 0
    if exit_tick is None:
        exit_tick = raw.iloc[-1]
        forced_exit = 1
    side = side_from_policy(family_id, entry, str(event["seq_id"]))
    pnl = trade_pnl(entry, exit_tick, side)
    flip_pnl = trade_pnl(entry, exit_tick, "short" if side == "long" else "long")
    random_side = "long" if stable_unit_hash(str(row["scenario_id"]) + str(event["seq_id"])) >= 0.5 else "short"
    random_pnl = trade_pnl(entry, exit_tick, random_side)
    return {
        "status": "filled",
        "symbol": event["symbol"],
        "description": event["description"],
        "diagnostic_trade_date": event["diagnostic_trade_date"],
        "announcement_time_ist": event["announcement_time_ist"],
        "seq_id": event["seq_id"],
        "side": side,
        "entry_ms": int(entry["collector_received_utc_ms"]),
        "exit_ms": int(exit_tick["collector_received_utc_ms"]),
        "holding_ms": int(exit_tick["collector_received_utc_ms"]) - int(entry["collector_received_utc_ms"]),
        "forced_exit": forced_exit,
        "entry_mid": float(entry["mid"]),
        "exit_mid": float(exit_tick["mid"]),
        "mid_return_bps": ((float(exit_tick["mid"]) - float(entry["mid"])) / float(entry["mid"]) * 10_000.0) if float(entry["mid"]) else 0.0,
        "entry_top5_qty_imbalance": float(entry["top5_qty_imbalance"]),
        "entry_l2_l5_qty_imbalance": float(entry["l2_l5_qty_imbalance"]),
        "entry_top5_order_imbalance": float(entry["top5_order_imbalance"]),
        **pnl,
        "side_flip_net_pnl_inr": float(flip_pnl["net_pnl_inr"]),
        "random_side": random_side,
        "random_side_net_pnl_inr": float(random_pnl["net_pnl_inr"]),
    }


def apply_capacity(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame["capacity_selected"] = 0
    filled = frame[frame["status"].eq("filled")].sort_values(["entry_ms", "scenario_id", "seq_id"])
    active: list[int] = []
    selected: set[int] = set()
    for idx, row in filled.iterrows():
        active = [exit_ms for exit_ms in active if exit_ms > int(row["entry_ms"])]
        if len(active) < MAX_CONCURRENT_POSITIONS:
            selected.add(int(idx))
            active.append(int(row["exit_ms"]))
    frame.loc[list(selected), "capacity_selected"] = 1
    return frame


def summarize_scenarios(trades: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if trades.empty:
        return pd.DataFrame()
    for scenario_id, frame in trades.groupby("scenario_id", dropna=False):
        filled = frame[frame["status"].eq("filled")].copy()
        selected = filled[filled["capacity_selected"].astype(int).eq(1)].copy()
        for scope, scoped in [("isolated_all_events", filled), ("capacity_capped", selected)]:
            days = max(1, int(scoped["diagnostic_trade_date"].nunique())) if not scoped.empty else 1
            net = float(scoped["net_pnl_inr"].sum()) if not scoped.empty else 0.0
            side_flip = float(scoped["side_flip_net_pnl_inr"].sum()) if not scoped.empty else 0.0
            random_net = float(scoped["random_side_net_pnl_inr"].sum()) if not scoped.empty else 0.0
            base = frame.iloc[0]
            rows.append(
                {
                    "scenario_id": scenario_id,
                    "scope": scope,
                    "family_id": base["family_id"],
                    "entry_timing_policy": base["entry_timing_policy"],
                    "horizon_seconds": base["horizon_seconds"],
                    "depth_threshold_quantile": base["depth_threshold_quantile"],
                    "trade_rows": int(len(scoped)),
                    "diagnostic_trade_dates": int(scoped["diagnostic_trade_date"].nunique()) if not scoped.empty else 0,
                    "symbols": int(scoped["symbol"].nunique()) if not scoped.empty else 0,
                    "positive_symbol_date_cells": int(scoped[scoped["net_pnl_inr"] > 0][["diagnostic_trade_date", "symbol"]].drop_duplicates().shape[0]) if not scoped.empty else 0,
                    "net_pnl_inr": net,
                    "side_flip_net_pnl_inr": side_flip,
                    "random_side_net_pnl_inr": random_net,
                    "annualized_return_pct": net / INITIAL_CAPITAL_INR * 100.0 * TRADING_DAYS_PER_YEAR / days,
                    "side_flip_annualized_return_pct": side_flip / INITIAL_CAPITAL_INR * 100.0 * TRADING_DAYS_PER_YEAR / days,
                    "random_side_annualized_return_pct": random_net / INITIAL_CAPITAL_INR * 100.0 * TRADING_DAYS_PER_YEAR / days,
                    "control_pass": int(net > side_flip and net > random_net),
                    "above12": int(net / INITIAL_CAPITAL_INR * 100.0 * TRADING_DAYS_PER_YEAR / days > ANNUALIZED_THRESHOLD_PCT),
                    "acceptance_candidate": int(scope == "capacity_capped" and len(scoped) >= ROBUST_EVENT_FLOOR and net / INITIAL_CAPITAL_INR * 100.0 * TRADING_DAYS_PER_YEAR / days > ANNUALIZED_THRESHOLD_PCT and net > side_flip and net > random_net and base["family_id"] != "P344_NEGATIVE_CONTROL_FAILED_SURVIVOR_REPLAY"),
                }
            )
    return pd.DataFrame(rows).sort_values(["scope", "annualized_return_pct"], ascending=[True, False]).reset_index(drop=True)


def build_thresholds(events: pd.DataFrame, real_root: Path) -> dict[str, dict[float, float]]:
    values_top5 = []
    values_l2l5 = []
    cache: dict[tuple[str, str], pd.DataFrame] = {}
    eligible = events[events["diagnostic_real_l2_available"].astype(int).eq(1)].copy()
    for event in eligible.itertuples(index=False):
        key = (str(event.diagnostic_trade_date), str(event.symbol))
        if key not in cache:
            cache[key] = load_raw_day_symbol(real_root, key[0], key[1])
        raw = cache[key]
        tick = first_tick_at_or_after(raw, announcement_start_ms(pd.Series(event._asdict())))
        if tick is not None:
            values_top5.append(abs(float(tick["top5_qty_imbalance"])))
            values_l2l5.append(abs(float(tick["l2_l5_qty_imbalance"])))
    return {
        "top5_abs": {q: float(pd.Series(values_top5).quantile(q)) if values_top5 else 0.0 for q in [0.5, 0.75]},
        "l2_l5_abs": {q: float(pd.Series(values_l2l5).quantile(q)) if values_l2l5 else 0.0 for q in [0.5, 0.75]},
    }


def execute_search(grid: pd.DataFrame, events: pd.DataFrame, real_root: Path, phase342_trades: pd.DataFrame) -> pd.DataFrame:
    grid = grid.copy().reset_index(drop=True)
    grid["scenario_id"] = grid.apply(lambda r: f"P345_{r.name:04d}_{r['family_id']}_{r['entry_timing_policy']}_H{r['horizon_seconds']}_Q{str(r['depth_threshold_quantile']).replace('.', 'p')}", axis=1)
    eligible = events[events["diagnostic_real_l2_available"].astype(int).eq(1)].copy()
    thresholds = build_thresholds(eligible, real_root)
    cache: dict[tuple[str, str], pd.DataFrame] = {}
    rows: list[dict[str, object]] = []
    for scenario in grid.to_dict("records"):
        if scenario["family_id"] == "P344_NEGATIVE_CONTROL_FAILED_SURVIVOR_REPLAY":
            for trade in phase342_trades.to_dict("records"):
                rows.append({**scenario, **trade, "scenario_id": scenario["scenario_id"], "status": trade.get("status", "filled")})
            continue
        for event in eligible.to_dict("records"):
            key = (str(event["diagnostic_trade_date"]), str(event["symbol"]))
            if key not in cache:
                cache[key] = load_raw_day_symbol(real_root, key[0], key[1])
            result = scenario_trade(pd.Series(scenario), pd.Series(event), cache[key], thresholds)
            rows.append({**scenario, **result})
    trades = pd.DataFrame(rows)
    return pd.concat([apply_capacity(frame) for _, frame in trades.groupby("scenario_id", dropna=False)], ignore_index=True)


def build_gate_evaluation(phase344: pd.DataFrame, grid: pd.DataFrame, trades: pd.DataFrame, summary: pd.DataFrame) -> pd.DataFrame:
    phase344_complete = as_int(metric_value(phase344, "phase344_official_catalyst_native_full_depth_strategy_search_precommit_complete", 0))
    execution_allowed = as_int(metric_value(phase344, "phase344_phase345_execution_allowed_next", 0))
    expected_grid = as_int(metric_value(phase344, "phase344_grid_rows", 0))
    acceptance_rows = int(summary["acceptance_candidate"].sum()) if not summary.empty and "acceptance_candidate" in summary else 0
    rows = [
        ("P345_PHASE344_COMPLETE", phase344_complete == 1, phase344_complete, 1),
        ("P345_EXECUTION_ALLOWED_BY_PRECOMMIT", execution_allowed == 1, execution_allowed, 1),
        ("P345_GRID_RECONCILED", len(grid) == expected_grid, f"{len(grid)}/{expected_grid}", "all"),
        ("P345_TRADE_ROWS_PRESENT", len(trades) > 0, len(trades), ">0"),
        ("P345_CAPACITY_SUMMARIES_PRESENT", "capacity_capped" in summary["scope"].astype(str).unique().tolist(), "present", "present"),
        ("P345_ACCEPTANCE_STATUS_RECORDED", True, acceptance_rows, "recorded"),
        ("P345_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM", True, "closed", "closed"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed", "required"])


def write_outputs(phase344_dir: Path, phase341_dir: Path, phase342_dir: Path, real_root: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase344 = read_csv(phase344_dir / "phase344_acceptance_summary.csv")
    grid = pd.read_csv(phase344_dir / "phase344_phase345_search_grid.csv")
    events = pd.read_csv(phase341_dir / "phase341_no_lookahead_official_catalyst_eligibility_ledger.csv")
    phase342_trades = pd.read_csv(phase342_dir / "phase342_real_day_trade_diagnostic_ledger.csv")
    trades = execute_search(grid, events, real_root, phase342_trades)
    summary = summarize_scenarios(trades)
    gates = build_gate_evaluation(phase344, grid, trades, summary)
    passed = int(gates["passed"].astype(bool).sum())
    total = int(len(gates))
    capacity = summary[summary["scope"].eq("capacity_capped")].copy()
    acceptance = capacity[capacity["acceptance_candidate"].astype(int).eq(1)].copy() if not capacity.empty else pd.DataFrame()
    best = capacity.sort_values("annualized_return_pct", ascending=False).head(1).iloc[0].to_dict() if not capacity.empty else {}
    acceptance_summary = pd.DataFrame(
        [
            ("phase345_official_catalyst_native_full_depth_strategy_search_execution_complete", 1, "Phase345 execution completed"),
            ("phase345_phase344_complete", as_int(metric_value(phase344, "phase344_official_catalyst_native_full_depth_strategy_search_precommit_complete", 0)), "Phase344 complete"),
            ("phase345_grid_rows", len(grid), "Search grid rows"),
            ("phase345_trade_rows", len(trades), "Scenario trade rows"),
            ("phase345_capacity_summary_rows", len(capacity), "Capacity-capped scenario summaries"),
            ("phase345_capacity_above12_rows", int(capacity["above12"].sum()) if not capacity.empty else 0, "Capacity scenarios above 12%"),
            ("phase345_acceptance_candidate_rows", len(acceptance), "Acceptance candidate rows"),
            ("phase345_best_capacity_scenario_id", best.get("scenario_id", ""), "Best capacity scenario"),
            ("phase345_best_capacity_family_id", best.get("family_id", ""), "Best capacity family"),
            ("phase345_best_capacity_annualized_return_pct", best.get("annualized_return_pct", 0.0), "Best capacity annualized return"),
            ("phase345_best_capacity_net_pnl_inr", best.get("net_pnl_inr", 0.0), "Best capacity net PnL"),
            ("phase345_best_capacity_trade_rows", best.get("trade_rows", 0), "Best capacity trade rows"),
            ("phase345_best_capacity_control_pass", best.get("control_pass", 0), "Best capacity control pass"),
            ("phase345_strategy_promotion_allowed", 0, "No promotion"),
            ("phase345_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase345_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase345_hard_gate_pass_rows", passed, "Passed hard gates"),
            ("phase345_hard_gate_rows", total, "Hard gates"),
            ("phase345_next_best_action", NEXT_ACTION if passed == total else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    report = "\n".join(
        [
            "# Phase345 Official-Catalyst-Native Full-Depth Strategy Search Execution",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "Phase345 executes the Phase344 material-new official-catalyst-native full-depth grid. Results remain diagnostic until interpreted.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(acceptance_summary),
            "",
            "## Top capacity scenarios",
            "",
            _markdown_table(capacity.sort_values("annualized_return_pct", ascending=False).head(20) if not capacity.empty else pd.DataFrame()),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened by Phase345.",
        ]
    )
    outputs = {
        "summary": output_dir / "phase345_acceptance_summary.csv",
        "trade_ledger": output_dir / "phase345_strategy_trade_ledger.csv",
        "scenario_summary": output_dir / "phase345_strategy_scenario_summary.csv",
        "gates": output_dir / "phase345_gate_evaluation.csv",
        "report": output_dir / "phase345_official_catalyst_native_full_depth_strategy_search_execution_report.md",
        "manifest": output_dir / "phase345_official_catalyst_native_full_depth_strategy_search_execution_manifest.json",
    }
    acceptance_summary.to_csv(outputs["summary"], index=False)
    trades.to_csv(outputs["trade_ledger"], index=False)
    summary.to_csv(outputs["scenario_summary"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text(report, encoding="utf-8")
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "phase": 345,
        "generated_at_utc": generated_utc,
        "phase344_dir": str(phase344_dir),
        "phase341_dir": str(phase341_dir),
        "phase342_dir": str(phase342_dir),
        "real_root": str(real_root),
        "output_dir": str(output_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase345",
            generated_utc=generated_utc,
            inputs={
                "phase344_grid": str(phase344_dir / "phase344_phase345_search_grid.csv"),
                "phase341_events": str(phase341_dir / "phase341_no_lookahead_official_catalyst_eligibility_ledger.csv"),
                "real_root": str(real_root),
            },
            parameters={"annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT, "robust_event_floor": ROBUST_EVENT_FLOOR},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase344-dir", type=Path, default=DEFAULT_PHASE344_DIR)
    parser.add_argument("--phase341-dir", type=Path, default=DEFAULT_PHASE341_DIR)
    parser.add_argument("--phase342-dir", type=Path, default=DEFAULT_PHASE342_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase344_dir, args.phase341_dir, args.phase342_dir, args.real_root, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()

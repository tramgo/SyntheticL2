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
from synthetic_l2.phase428_broader_full_depth_feature_family_sweep import load_real_anchor_ticks, prepare_group_features, score_trade
from synthetic_l2.phase437_low_turnover_depth_regime_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    COST_MULTIPLIER,
    INITIAL_CAPITAL_INR,
    MAX_TRADES_PER_SYMBOL_DATE,
    MIN_COMPLETED_ROUND_TRIPS,
    MIN_POSITIVE_DATE_FRACTION,
    MIN_SYMBOLS,
    MIN_TRADE_DATES,
    NEXT_ACTION as PHASE437_NEXT_ACTION,
    ORDER_NOTIONAL_INR,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE437_DIR = Path("outputs/phase437")
DEFAULT_OUTPUT_DIR = Path("outputs/phase438")

THESIS_ID = "P438_LOW_TURNOVER_FULL_DEPTH_REGIME_CARRY_EXECUTION"
NEXT_ACTION = "interpret_phase438_low_turnover_depth_regime_carry_no_paper_live"

MAX_ROWS_PER_SYNTHETIC_FILE = 5_000
MAX_SYNTHETIC_MONTHS = 12
MAX_SYNTHETIC_SYMBOLS = 32


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


def load_broad_synthetic_ticks(raw_root: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    month_roots = sorted(raw_root.glob("trade_month=*"))[:MAX_SYNTHETIC_MONTHS]
    for month_root in month_roots:
        symbol_roots = sorted(month_root.glob("symbol=*"))[:MAX_SYNTHETIC_SYMBOLS]
        for symbol_root in symbol_roots:
            file = symbol_root / "part-00000.parquet"
            if file.exists():
                frames.append(read_first_rows(file, MAX_ROWS_PER_SYNTHETIC_FILE))
    return normalize_ticks(pd.concat(frames, ignore_index=True) if frames else pd.DataFrame())


def fixed_quantity(price: float) -> int:
    return max(1, int(math.floor(ORDER_NOTIONAL_INR / max(float(price), 0.01))))


def direction_from_pressure(row: pd.Series, family_id: str, *, l1_only: bool = False) -> int:
    if l1_only:
        pressure = float(row["l1_imbalance"])
    else:
        pressure = float(row["top5_imbalance"]) + float(row["l2_l5_imbalance"]) + float(row["book_slope"])
    side = 1 if pressure >= 0 else -1
    if str(family_id) == "depth_regime_snapback":
        side = -side
    return int(side)


def score_group_trade(group: pd.DataFrame, scenario: pd.Series, *, l1_only: bool = False, side_flip: bool = False) -> dict[str, Any] | None:
    early = int(scenario["early_window_ticks"])
    delay = int(scenario["entry_delay_ticks"])
    hold = int(scenario["hold_ticks"])
    if len(group) <= early + delay + 2:
        return None
    signal_idx = early - 1
    entry_idx = min(len(group) - 2, signal_idx + delay)
    exit_idx = min(len(group) - 1, entry_idx + hold)
    if exit_idx <= entry_idx:
        return None
    signal = group.iloc[signal_idx]
    entry = group.iloc[entry_idx]
    exit_row = group.iloc[exit_idx]
    side = direction_from_pressure(signal, str(scenario["family_id"]), l1_only=l1_only)
    if side_flip:
        side = -side
    entry_price = float(entry["sell_1_price"] if side > 0 else entry["buy_1_price"])
    exit_price = float(exit_row["buy_1_price"] if side > 0 else exit_row["sell_1_price"])
    qty = fixed_quantity(entry_price)
    scores = score_trade(side, entry_price, exit_price, qty)
    return {
        "scenario_id": str(scenario["scenario_id"]),
        "family_id": str(scenario["family_id"]),
        "trade_date": str(group.iloc[0]["trade_date"]),
        "symbol": str(group.iloc[0]["symbol"]),
        "signal_index": signal_idx,
        "entry_index": entry_idx,
        "exit_index": exit_idx,
        "hold_ticks_observed": exit_idx - entry_idx,
        "hold_ms": float(exit_row["exchange_timestamp_ms"]) - float(entry["exchange_timestamp_ms"]),
        "side": "long" if side > 0 else "short",
        "side_int": side,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "quantity": qty,
        "l1_imbalance": float(signal["l1_imbalance"]),
        "l2_l5_imbalance": float(signal["l2_l5_imbalance"]),
        "top5_imbalance": float(signal["top5_imbalance"]),
        "book_slope": float(signal["book_slope"]),
        **scores,
    }


def evaluate_scenarios(ticks: pd.DataFrame, grid: pd.DataFrame, panel: str, *, l1_only: bool = False, side_flip: bool = False, time_shuffle: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    groups = []
    for _, raw in ticks.groupby(["trade_date", "symbol"], sort=True):
        groups.append(prepare_group_features(raw))
    trades: list[dict[str, Any]] = []
    for scenario in grid.itertuples(index=False):
        row = pd.Series(scenario._asdict())
        scenario_trades = []
        for group in groups:
            trade = score_group_trade(group, row, l1_only=l1_only, side_flip=side_flip)
            if trade is not None:
                scenario_trades.append(trade)
        if time_shuffle and scenario_trades:
            sides = [t["side_int"] for t in scenario_trades]
            shuffled = pd.Series(sides).sample(frac=1.0, random_state=438).tolist()
            reshuffled = []
            for trade, side in zip(scenario_trades, shuffled):
                g = next(g for g in groups if str(g.iloc[0]["trade_date"]) == trade["trade_date"] and str(g.iloc[0]["symbol"]) == trade["symbol"])
                entry = g.iloc[int(trade["entry_index"])]
                exit_row = g.iloc[int(trade["exit_index"])]
                entry_price = float(entry["sell_1_price"] if side > 0 else entry["buy_1_price"])
                exit_price = float(exit_row["buy_1_price"] if side > 0 else exit_row["sell_1_price"])
                qty = fixed_quantity(entry_price)
                scores = score_trade(int(side), entry_price, exit_price, qty)
                trade = {**trade, "side": "long" if side > 0 else "short", "side_int": int(side), "entry_price": entry_price, "exit_price": exit_price, "quantity": qty, **scores}
                reshuffled.append(trade)
            scenario_trades = reshuffled
        trades.extend(scenario_trades)
    ledger = pd.DataFrame(trades)
    summary = summarize_by_scenario(ledger, grid, panel)
    return ledger, summary


def summarize_by_scenario(ledger: pd.DataFrame, grid: pd.DataFrame, panel: str) -> pd.DataFrame:
    rows = []
    for scenario in grid.itertuples(index=False):
        sid = str(scenario.scenario_id)
        trades = ledger[ledger["scenario_id"].astype(str).eq(sid)] if not ledger.empty else pd.DataFrame()
        if trades.empty:
            rows.append(
                {
                    "panel": panel,
                    "scenario_id": sid,
                    "family_id": scenario.family_id,
                    "completed_round_trips": 0,
                    "trade_dates": 0,
                    "symbols": 0,
                    "positive_date_fraction": 0.0,
                    "gross_pnl_inr": 0.0,
                    "cost200_inr": 0.0,
                    "net_pnl_inr": 0.0,
                    "annualized_return_pct": 0.0,
                    "acceptance_survivor": 0,
                }
            )
            continue
        date_pnl = trades.groupby("trade_date")["net_pnl_inr"].sum()
        dates = int(trades["trade_date"].nunique())
        net = float(trades["net_pnl_inr"].sum())
        ann = (net / INITIAL_CAPITAL_INR) * (252.0 / max(1, dates)) * 100.0
        pos_frac = float((date_pnl > 0).mean()) if len(date_pnl) else 0.0
        trips = int(len(trades))
        symbols = int(trades["symbol"].nunique())
        rows.append(
            {
                "panel": panel,
                "scenario_id": sid,
                "family_id": scenario.family_id,
                "completed_round_trips": trips,
                "trade_dates": dates,
                "symbols": symbols,
                "positive_date_fraction": pos_frac,
                "gross_pnl_inr": float(trades["gross_pnl_inr"].sum()),
                "cost200_inr": float(trades["cost200_inr"].sum()),
                "net_pnl_inr": net,
                "annualized_return_pct": float(ann),
                "acceptance_survivor": int(
                    trips >= MIN_COMPLETED_ROUND_TRIPS
                    and dates >= MIN_TRADE_DATES
                    and symbols >= MIN_SYMBOLS
                    and pos_frac >= MIN_POSITIVE_DATE_FRACTION
                    and ann >= ANNUALIZED_THRESHOLD_PCT
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("annualized_return_pct", ascending=False).reset_index(drop=True)


def best(summary: pd.DataFrame) -> pd.Series:
    active = summary[pd.to_numeric(summary["completed_round_trips"], errors="coerce").fillna(0).gt(0)]
    return active.sort_values("annualized_return_pct", ascending=False).iloc[0] if not active.empty else summary.iloc[0]


def build_gates(summary: pd.DataFrame, l1_summary: pd.DataFrame, side_summary: pd.DataFrame, shuffle_summary: pd.DataFrame, real_summary: pd.DataFrame) -> pd.DataFrame:
    b = best(summary)
    sid = str(b["scenario_id"])
    l1 = l1_summary[l1_summary["scenario_id"].astype(str).eq(sid)].iloc[0]
    side = side_summary[side_summary["scenario_id"].astype(str).eq(sid)].iloc[0]
    shuffle = shuffle_summary[shuffle_summary["scenario_id"].astype(str).eq(sid)].iloc[0]
    real = real_summary[real_summary["scenario_id"].astype(str).eq(sid)].iloc[0] if not real_summary.empty and sid in set(real_summary["scenario_id"].astype(str)) else pd.Series(dtype=object)
    primary_ann = float(b["annualized_return_pct"])
    gates = [
        ("P438_PHASE437_PRECOMMIT_USED", True, PHASE437_NEXT_ACTION, "phase437_next_action"),
        ("P438_LOW_TURNOVER_ONE_TRADE_PER_SYMBOL_DATE", int(b["completed_round_trips"]) <= int(b["trade_dates"]) * int(b["symbols"]) * MAX_TRADES_PER_SYMBOL_DATE, b["completed_round_trips"], "one_per_symbol_date"),
        ("P438_FULL_DEPTH_PRIMARY_PRESENT", True, sid, "full_depth_pressure"),
        ("P438_L1_ONLY_CONTROL", primary_ann - float(l1["annualized_return_pct"]) >= 5.0, primary_ann - float(l1["annualized_return_pct"]), ">=5 pct pts"),
        ("P438_SIDE_FLIP_CONTROL_NOT_DOMINANT", primary_ann >= float(side["annualized_return_pct"]), side["annualized_return_pct"], "primary>=side_flip"),
        ("P438_TIME_SHUFFLE_CONTROL_NOT_DOMINANT", primary_ann >= float(shuffle["annualized_return_pct"]), shuffle["annualized_return_pct"], "primary>=time_shuffle"),
        ("P438_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={ORDER_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P438_EVENT_FLOOR", int(b["completed_round_trips"]) >= MIN_COMPLETED_ROUND_TRIPS, b["completed_round_trips"], f">={MIN_COMPLETED_ROUND_TRIPS}"),
        ("P438_DATE_BREADTH", int(b["trade_dates"]) >= MIN_TRADE_DATES, b["trade_dates"], f">={MIN_TRADE_DATES}"),
        ("P438_SYMBOL_BREADTH", int(b["symbols"]) >= MIN_SYMBOLS, b["symbols"], f">={MIN_SYMBOLS}"),
        ("P438_POSITIVE_DATE_FRACTION", float(b["positive_date_fraction"]) >= MIN_POSITIVE_DATE_FRACTION, b["positive_date_fraction"], f">={MIN_POSITIVE_DATE_FRACTION}"),
        ("P438_ANNUALIZED_FLOOR", primary_ann >= ANNUALIZED_THRESHOLD_PCT, primary_ann, f">={ANNUALIZED_THRESHOLD_PCT}"),
        ("P438_REAL_ANCHOR_CROSS_CHECK", (primary_ann == 0 and float(real.get("annualized_return_pct", 0)) == 0) or primary_ann * float(real.get("annualized_return_pct", 0)) >= 0, real.get("annualized_return_pct", 0), "same_sign"),
        ("P438_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(ticks: pd.DataFrame, summary: pd.DataFrame, gates: pd.DataFrame, real_summary: pd.DataFrame) -> pd.DataFrame:
    b = best(summary)
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase438_low_turnover_depth_regime_complete", 1, "Phase438 execution completed"),
            ("phase438_thesis_id", THESIS_ID, "Execution thesis"),
            ("phase438_synthetic_tick_rows_loaded", len(ticks), "Synthetic tick rows loaded"),
            ("phase438_synthetic_trade_dates_loaded", ticks["trade_date"].nunique() if not ticks.empty else 0, "Synthetic dates loaded"),
            ("phase438_synthetic_symbols_loaded", ticks["symbol"].nunique() if not ticks.empty else 0, "Synthetic symbols loaded"),
            ("phase438_best_scenario_id", b["scenario_id"], "Best active synthetic scenario"),
            ("phase438_best_family_id", b["family_id"], "Best family"),
            ("phase438_best_completed_round_trips", b["completed_round_trips"], "Best round trips"),
            ("phase438_best_trade_dates", b["trade_dates"], "Best trade dates"),
            ("phase438_best_symbols", b["symbols"], "Best symbols"),
            ("phase438_best_positive_date_fraction", b["positive_date_fraction"], "Best positive date fraction"),
            ("phase438_best_gross_pnl_inr", b["gross_pnl_inr"], "Best gross P&L"),
            ("phase438_best_cost200_inr", b["cost200_inr"], "Best cost200 charges"),
            ("phase438_best_net_pnl_inr", b["net_pnl_inr"], "Best net P&L"),
            ("phase438_best_annualized_return_pct", b["annualized_return_pct"], "Best annualized return"),
            ("phase438_real_anchor_best_annualized_return_pct", best(real_summary)["annualized_return_pct"] if not real_summary.empty else 0, "Real-anchor best annualized return"),
            ("phase438_cost200_acceptance_survivor_rows", int(summary["acceptance_survivor"].astype(int).sum()), "Synthetic acceptance survivors before controls"),
            ("phase438_strategy_promotion_allowed", 0, "No promotion"),
            ("phase438_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase438_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase438_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase438_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase438_next_best_action", NEXT_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, summary: pd.DataFrame, controls: pd.DataFrame, real_summary: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase438 Low-Turnover Full-Depth Regime Carry Execution",
        "",
        "Phase438 executes the Phase437 lower-turnover source: one early-session full-depth regime trade per symbol/date with longer hold horizons.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Synthetic Scenario Summary",
        "",
        _markdown_table(summary),
        "",
        "## Control Summary For Best Scenario",
        "",
        _markdown_table(controls),
        "",
        "## Real-Anchor Summary",
        "",
        _markdown_table(real_summary),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: no strategy promotion, paper/live acceptance or deployable profitability claim is generated by Phase438.",
    ]
    (output_dir / "phase438_low_turnover_depth_regime_carry_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(raw_root: Path = DEFAULT_RAW_ROOT, phase437_dir: Path = DEFAULT_PHASE437_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR, real_roots: list[Path] | None = None) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase437 = read_csv(phase437_dir / "phase437_acceptance_summary.csv")
    if str(metric_value(phase437, "phase437_next_best_action", "")) != PHASE437_NEXT_ACTION:
        raise ValueError("Phase438 requires Phase437 execution allowance.")
    grid = read_csv(phase437_dir / "phase437_low_turnover_scenario_grid.csv")
    ticks = load_broad_synthetic_ticks(raw_root)
    ledger, summary = evaluate_scenarios(ticks, grid, "synthetic")
    l1_ledger, l1_summary = evaluate_scenarios(ticks, grid, "synthetic_l1_only", l1_only=True)
    side_ledger, side_summary = evaluate_scenarios(ticks, grid, "synthetic_side_flip", side_flip=True)
    shuffle_ledger, shuffle_summary = evaluate_scenarios(ticks, grid, "synthetic_time_shuffle", time_shuffle=True)
    best_sid = str(best(summary)["scenario_id"])
    controls = pd.DataFrame(
        [
            {"control": "l1_only", **l1_summary[l1_summary["scenario_id"].astype(str).eq(best_sid)].iloc[0].to_dict()},
            {"control": "side_flip", **side_summary[side_summary["scenario_id"].astype(str).eq(best_sid)].iloc[0].to_dict()},
            {"control": "time_shuffle", **shuffle_summary[shuffle_summary["scenario_id"].astype(str).eq(best_sid)].iloc[0].to_dict()},
        ]
    )
    real_ticks = load_real_anchor_ticks(real_roots or DEFAULT_REAL_ROOTS)
    real_ledger, real_summary = evaluate_scenarios(real_ticks, grid, "real_anchor") if not real_ticks.empty else (pd.DataFrame(), pd.DataFrame())
    gates = build_gates(summary, l1_summary, side_summary, shuffle_summary, real_summary)
    acceptance = build_acceptance(ticks, summary, gates, real_summary)
    summary.to_csv(output_dir / "phase438_synthetic_scenario_summary.csv", index=False)
    ledger.head(25_000).to_csv(output_dir / "phase438_synthetic_trade_ledger_sample.csv", index=False)
    controls.to_csv(output_dir / "phase438_best_scenario_controls.csv", index=False)
    real_summary.to_csv(output_dir / "phase438_real_anchor_scenario_summary.csv", index=False)
    real_ledger.head(25_000).to_csv(output_dir / "phase438_real_anchor_trade_ledger_sample.csv", index=False)
    gates.to_csv(output_dir / "phase438_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase438_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, summary, controls, real_summary, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase438_low_turnover_depth_regime_carry",
        **reproducibility_fields(
            artifact_id="phase438_low_turnover_depth_regime_carry",
            generated_utc=generated_utc,
            inputs={"phase437_grid": str(phase437_dir / "phase437_low_turnover_scenario_grid.csv"), "raw_root": str(raw_root)},
            parameters={"thesis_id": THESIS_ID, "max_rows_per_synthetic_file": MAX_ROWS_PER_SYNTHETIC_FILE, "max_months": MAX_SYNTHETIC_MONTHS, "max_symbols": MAX_SYNTHETIC_SYMBOLS},
            outputs={"acceptance_summary": str(output_dir / "phase438_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase438_fixed_tick_longer_horizon",
        ),
    }
    (output_dir / "phase438_low_turnover_depth_regime_carry_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase438 low-turnover full-depth regime carry execution.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase437-dir", type=Path, default=DEFAULT_PHASE437_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.raw_root, args.phase437_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

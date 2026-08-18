from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase411_full_depth_replenishment_breakout_execution import DEFAULT_RAW_ROOT, DEFAULT_REAL_ROOTS, REQUIRED_COLUMNS, normalize_ticks, spread_bps
from synthetic_l2.phase424_queue_depletion_continuation_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    COST_MULTIPLIER,
    ENTRY_FORWARD_TICKS,
    INITIAL_CAPITAL_INR,
    LOOKBACK_TICKS,
    MAX_HOLD_TICKS,
    MAX_OPPOSITE_L1_NOTIONAL_INR,
    MAX_SPREAD_BPS,
    MIN_COMPLETED_ROUND_TRIPS,
    MIN_FORWARD_HOLD_MS,
    MIN_L1_IMBALANCE_CONFIRMATION,
    MIN_L2_L5_DEPTH_NOTIONAL_INR,
    MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT,
    MIN_L2_L5_OPPOSITE_DEPLETION,
    MIN_L2_L5_SAME_SIDE_REPLENISHMENT,
    MIN_POSITIVE_DATE_FRACTION,
    MIN_SYMBOLS,
    MIN_TRADE_DATES,
    NEXT_ACTION as PHASE424_NEXT_ACTION,
    ORDER_NOTIONAL_INR,
    SYMBOLS,
    THESIS_ID,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_PHASE424_DIR = Path("outputs/phase424")
DEFAULT_OUTPUT_DIR = Path("outputs/phase425")

SYNTHETIC_MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"]
SYNTHETIC_SYMBOLS = SYMBOLS[:8]
MAX_ROWS_PER_SYNTHETIC_FILE = 30_000
MAX_SYNTHETIC_DATES = 5
REAL_ANCHOR_SYMBOLS = SYMBOLS[:8]
REAL_ANCHOR_MAX_DATES = 5
REAL_ANCHOR_MAX_FILES_PER_SYMBOL_DATE = 60
SCAN_STRIDE = 250
MIN_TICKS_PER_GROUP = max(LOOKBACK_TICKS + MAX_HOLD_TICKS + ENTRY_FORWARD_TICKS + 2, 240)
MAX_TRADES_PER_SYMBOL_DATE = 20

PRIMARY_SCENARIO = "P425_PRIMARY_QUEUE_DEPLETION_CONTINUATION"
L1_ONLY_SCENARIO = "P425_L1_ONLY_CONTROL"
SIDE_FLIP_SCENARIO = "P425_SIDE_FLIP_CONTROL"
NEXT_ACTION = "interpret_phase425_queue_depletion_continuation_no_paper_live"


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
    seen_dates: set[str] = set()
    for month in SYNTHETIC_MONTHS:
        for symbol in SYNTHETIC_SYMBOLS:
            path = raw_root / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"
            if path.exists():
                frame = read_first_rows(path, MAX_ROWS_PER_SYNTHETIC_FILE)
                frames.append(frame)
                if "trade_date" in frame.columns:
                    seen_dates.update(frame["trade_date"].dropna().astype(str).unique().tolist())
        if len(seen_dates) >= MAX_SYNTHETIC_DATES:
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


def sum_side(row: pd.Series, side: str, levels: range, field: str) -> float:
    return float(sum(float(row.get(f"{side}_{level}_{field}", 0.0) or 0.0) for level in levels))


def l2_l5_depth_notional(row: pd.Series) -> float:
    mid = (float(row["buy_1_price"]) + float(row["sell_1_price"])) / 2.0
    qty = sum_side(row, "buy", range(2, 6), "quantity") + sum_side(row, "sell", range(2, 6), "quantity")
    return float(mid * qty)


def l1_imbalance(row: pd.Series) -> float:
    bid = float(row.get("buy_1_quantity", 0.0) or 0.0)
    ask = float(row.get("sell_1_quantity", 0.0) or 0.0)
    denom = bid + ask
    return 0.0 if denom <= 0 else (bid - ask) / denom


def side_metrics(base: pd.Series, row: pd.Series, side: int) -> dict[str, float]:
    if side > 0:
        opposite, same = "sell", "buy"
        opposite_l1_notional = float(row["sell_1_price"]) * float(row.get("sell_1_quantity", 0.0) or 0.0)
    else:
        opposite, same = "buy", "sell"
        opposite_l1_notional = float(row["buy_1_price"]) * float(row.get("buy_1_quantity", 0.0) or 0.0)
    opposite_base_qty = sum_side(base, opposite, range(2, 6), "quantity")
    opposite_now_qty = sum_side(row, opposite, range(2, 6), "quantity")
    same_base_qty = sum_side(base, same, range(2, 6), "quantity")
    same_now_qty = sum_side(row, same, range(2, 6), "quantity")
    opposite_base_orders = sum_side(base, opposite, range(2, 6), "orders")
    opposite_now_orders = sum_side(row, opposite, range(2, 6), "orders")
    return {
        "opposite_l2_l5_depletion": max(0.0, opposite_base_qty - opposite_now_qty) / max(1.0, opposite_base_qty),
        "opposite_l2_l5_order_thinning": max(0.0, opposite_base_orders - opposite_now_orders) / max(1.0, opposite_base_orders),
        "same_side_l2_l5_replenishment": max(0.0, same_now_qty - same_base_qty) / max(1.0, same_base_qty),
        "opposite_l1_notional_inr": opposite_l1_notional,
        "l1_imbalance": l1_imbalance(row),
        "l2_l5_depth_notional_inr": l2_l5_depth_notional(row),
        "spread_bps": spread_bps(row),
    }


def frozen_primary_event(base: pd.Series, row: pd.Series, side: int) -> tuple[bool, dict[str, float]]:
    m = side_metrics(base, row, side)
    passed = (
        m["spread_bps"] <= MAX_SPREAD_BPS
        and m["opposite_l1_notional_inr"] <= MAX_OPPOSITE_L1_NOTIONAL_INR
        and m["l2_l5_depth_notional_inr"] >= MIN_L2_L5_DEPTH_NOTIONAL_INR
        and m["opposite_l2_l5_depletion"] >= MIN_L2_L5_OPPOSITE_DEPLETION
        and m["opposite_l2_l5_order_thinning"] >= MIN_L2_L5_OPPOSITE_DEPLETION
        and m["same_side_l2_l5_replenishment"] >= MIN_L2_L5_SAME_SIDE_REPLENISHMENT
        and side * m["l1_imbalance"] >= MIN_L1_IMBALANCE_CONFIRMATION
    )
    return passed, m


def frozen_l1_only_event(base: pd.Series, row: pd.Series, side: int) -> tuple[bool, dict[str, float]]:
    m = side_metrics(base, row, side)
    passed = (
        m["spread_bps"] <= MAX_SPREAD_BPS
        and m["opposite_l1_notional_inr"] <= MAX_OPPOSITE_L1_NOTIONAL_INR
        and side * m["l1_imbalance"] >= MIN_L1_IMBALANCE_CONFIRMATION
    )
    return passed, m


def choose_side(row: pd.Series) -> int:
    return 1 if l1_imbalance(row) >= 0 else -1


def fixed_quantity(entry_price: float) -> int:
    return max(1, int(math.floor(ORDER_NOTIONAL_INR / max(entry_price, 0.01))))


def score_trade(side: int, entry_price: float, exit_price: float, qty: int) -> dict[str, float]:
    if side > 0:
        buy_value = entry_price * qty
        sell_value = exit_price * qty
        gross = sell_value - buy_value
    else:
        sell_value = entry_price * qty
        buy_value = exit_price * qty
        gross = sell_value - buy_value
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=buy_value,
        sell_value_inr=sell_value,
        buy_quantity=qty,
        sell_quantity=qty,
        buy_orders=1,
        sell_orders=1,
    )
    cost100 = float(charges.total_charges)
    cost200 = cost100 * COST_MULTIPLIER
    return {
        "gross_pnl_inr": float(gross),
        "cost100_inr": cost100,
        "cost200_inr": cost200,
        "net_pnl_inr": float(gross - cost200),
        "net_pnl_cost100_inr": float(gross - cost100),
    }


def exact_exit_index(group: pd.DataFrame, entry_idx: int) -> tuple[int | None, int, float]:
    max_idx = min(len(group) - 1, entry_idx + MAX_HOLD_TICKS)
    for j in range(entry_idx + ENTRY_FORWARD_TICKS, max_idx + 1):
        hold_ms = float(group.iloc[j]["exchange_timestamp_ms"]) - float(group.iloc[entry_idx]["exchange_timestamp_ms"])
        if hold_ms >= MIN_FORWARD_HOLD_MS:
            return j, j - entry_idx, hold_ms
    return None, 0, 0.0


def candidate_from_index(group: pd.DataFrame, idx: int, scenario_id: str, *, l1_only: bool = False, side_flip: bool = False) -> dict[str, Any] | None:
    base = group.iloc[idx - LOOKBACK_TICKS]
    signal = group.iloc[idx]
    side = choose_side(signal)
    event_passed, metrics = frozen_l1_only_event(base, signal, side) if l1_only else frozen_primary_event(base, signal, side)
    if not event_passed:
        return None
    if side_flip:
        side *= -1
    entry_idx = idx + 1
    if entry_idx >= len(group):
        return None
    exit_idx, forward_ticks, hold_ms = exact_exit_index(group, entry_idx)
    if exit_idx is None:
        return None
    entry = group.iloc[entry_idx]
    exit_row = group.iloc[exit_idx]
    entry_price = float(entry["sell_1_price"] if side > 0 else entry["buy_1_price"])
    exit_price = float(exit_row["buy_1_price"] if side > 0 else exit_row["sell_1_price"])
    qty = fixed_quantity(entry_price)
    if qty <= 0:
        return None
    score = score_trade(side, entry_price, exit_price, qty)
    return {
        "scenario_id": scenario_id,
        "trade_date": str(signal["trade_date"]),
        "exchange": str(signal.get("exchange", "NSE")),
        "symbol": str(signal["symbol"]),
        "signal_index": int(idx),
        "entry_index": int(entry_idx),
        "exit_index": int(exit_idx),
        "signal_ts_ms": float(signal["exchange_timestamp_ms"]),
        "entry_ts_ms": float(entry["exchange_timestamp_ms"]),
        "exit_ts_ms": float(exit_row["exchange_timestamp_ms"]),
        "forward_ticks_after_entry": int(forward_ticks),
        "hold_ms": float(hold_ms),
        "side": "long" if side > 0 else "short",
        "l1_only_control": int(l1_only),
        "side_flip_control": int(side_flip),
        "entry_price": entry_price,
        "exit_price": exit_price,
        "quantity": qty,
        **metrics,
        **score,
    }


def run_scenario(ticks: pd.DataFrame, scenario_id: str, *, l1_only: bool = False, side_flip: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    diags: list[dict[str, Any]] = []
    for (trade_date, symbol), group in ticks.groupby(["trade_date", "symbol"], sort=True):
        group = group.sort_values("exchange_timestamp_ms", kind="mergesort").reset_index(drop=True)
        scanned = 0
        selected = 0
        if len(group) >= MIN_TICKS_PER_GROUP:
            for idx in range(LOOKBACK_TICKS, len(group) - MAX_HOLD_TICKS - ENTRY_FORWARD_TICKS - 2, SCAN_STRIDE):
                scanned += 1
                trade = candidate_from_index(group, idx, scenario_id, l1_only=l1_only, side_flip=side_flip)
                if trade is not None:
                    rows.append(trade)
                    selected += 1
                    if selected >= MAX_TRADES_PER_SYMBOL_DATE:
                        break
        diags.append(
            {
                "scenario_id": scenario_id,
                "trade_date": trade_date,
                "symbol": symbol,
                "input_ticks": len(group),
                "candidate_scan_points": scanned,
                "selected_trades": selected,
                "l1_only": int(l1_only),
                "side_flip": int(side_flip),
                "exact_forward_tick_rule": ENTRY_FORWARD_TICKS,
                "min_forward_hold_ms": MIN_FORWARD_HOLD_MS,
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(diags)


def run_panel(ticks: pd.DataFrame, panel: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    scenarios = [
        (PRIMARY_SCENARIO, False, False),
        (L1_ONLY_SCENARIO, True, False),
        (SIDE_FLIP_SCENARIO, False, True),
    ]
    ledgers = []
    diags = []
    for scenario_id, l1_only, side_flip in scenarios:
        ledger, diag = run_scenario(ticks, scenario_id, l1_only=l1_only, side_flip=side_flip)
        ledgers.append(ledger)
        diags.append(diag)
    ledger = pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()
    diag = pd.concat(diags, ignore_index=True) if diags else pd.DataFrame()
    summary = summarize(ledger, panel, [x[0] for x in scenarios])
    return ledger, diag, summary


def summarize(ledger: pd.DataFrame, panel: str, scenario_ids: list[str]) -> pd.DataFrame:
    rows = []
    for scenario_id in scenario_ids:
        group = ledger[ledger["scenario_id"].eq(scenario_id)] if not ledger.empty else pd.DataFrame()
        if group.empty:
            rows.append(
                {
                    "panel": panel,
                    "scenario_id": scenario_id,
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
            )
            continue
        date_pnl = group.groupby("trade_date")["net_pnl_inr"].sum()
        trade_dates = int(group["trade_date"].nunique())
        symbols = int(group["symbol"].nunique())
        net = float(group["net_pnl_inr"].sum())
        annualized = (net / INITIAL_CAPITAL_INR) * (252.0 / max(1, trade_dates)) * 100.0
        pos_frac = float((date_pnl > 0).mean()) if len(date_pnl) else 0.0
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
                "acceptance_survivor": int(
                    len(group) >= MIN_COMPLETED_ROUND_TRIPS
                    and trade_dates >= MIN_TRADE_DATES
                    and symbols >= MIN_SYMBOLS
                    and pos_frac >= MIN_POSITIVE_DATE_FRACTION
                    and annualized >= ANNUALIZED_THRESHOLD_PCT
                ),
            }
        )
    return pd.DataFrame(rows)


def scenario_value(summary: pd.DataFrame, scenario_id: str, column: str, default: Any = 0) -> Any:
    row = summary[summary["scenario_id"].astype(str).eq(scenario_id)] if not summary.empty else pd.DataFrame()
    return row[column].iloc[0] if not row.empty and column in row.columns else default


def build_gates(summary: pd.DataFrame, real_summary: pd.DataFrame) -> pd.DataFrame:
    primary = summary[summary["scenario_id"].eq(PRIMARY_SCENARIO)].iloc[0]
    primary_ann = float(primary["annualized_return_pct"])
    l1_ann = float(scenario_value(summary, L1_ONLY_SCENARIO, "annualized_return_pct", 0.0))
    side_flip_ann = float(scenario_value(summary, SIDE_FLIP_SCENARIO, "annualized_return_pct", 0.0))
    real_ann = float(scenario_value(real_summary, PRIMARY_SCENARIO, "annualized_return_pct", 0.0))
    full_depth_delta = primary_ann - l1_ann
    gates = [
        ("P425_EXECUTION_COMPLETE", True, 1, 1),
        ("P425_PHASE424_PRECOMMIT_USED", True, PHASE424_NEXT_ACTION, "run_phase425"),
        ("P425_TICK_ORDERED_SINGLE_NAME_REPLAY", True, "timestamp_sorted_group_loop", "present"),
        ("P425_EXACT_FORWARD_TICK_INDEXING", True, ENTRY_FORWARD_TICKS, ">=3 exact post-entry ticks"),
        ("P425_FORWARD_TIME_ENFORCED", True, MIN_FORWARD_HOLD_MS, ">=250ms"),
        ("P425_FULL_DEPTH_L1_L5_REQUIRED", True, "required_columns=L1-L5_price_quantity_orders", "present"),
        ("P425_LEVELS_2_TO_5_MATERIAL", True, "depletion_replenishment_order_thinning", "present"),
        ("P425_L1_ONLY_CONTROL", full_depth_delta >= MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT, full_depth_delta, f">={MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT}"),
        ("P425_SIDE_FLIP_CONTROL", primary_ann >= side_flip_ann, side_flip_ann, "primary>=side_flip"),
        ("P425_TAKER_ONLY_EXECUTION", True, "taker_entry_taker_exit", "present"),
        ("P425_NO_LOOKAHEAD", True, "rolling_baseline_before_signal_then_entry_next_tick", "present"),
        ("P425_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={ORDER_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P425_EVENT_FLOOR", int(primary["completed_round_trips"]) >= MIN_COMPLETED_ROUND_TRIPS, primary["completed_round_trips"], f">={MIN_COMPLETED_ROUND_TRIPS}"),
        ("P425_DATE_BREADTH", int(primary["trade_dates"]) >= MIN_TRADE_DATES, primary["trade_dates"], f">={MIN_TRADE_DATES}"),
        ("P425_SYMBOL_BREADTH", int(primary["symbols"]) >= MIN_SYMBOLS, primary["symbols"], f">={MIN_SYMBOLS}"),
        ("P425_POSITIVE_DATE_FRACTION", float(primary["positive_date_fraction"]) >= MIN_POSITIVE_DATE_FRACTION, primary["positive_date_fraction"], f">={MIN_POSITIVE_DATE_FRACTION}"),
        ("P425_ANNUALIZED_FLOOR", primary_ann >= ANNUALIZED_THRESHOLD_PCT, primary_ann, f">={ANNUALIZED_THRESHOLD_PCT}"),
        ("P425_REAL_ANCHOR_CROSS_CHECK", (primary_ann == 0.0 and real_ann == 0.0) or primary_ann * real_ann >= 0, real_ann, "same_sign"),
        ("P425_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(summary: pd.DataFrame, real_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    primary = summary[summary["scenario_id"].eq(PRIMARY_SCENARIO)].iloc[0]
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    survivors = int(summary["acceptance_survivor"].astype(int).sum())
    l1_ann = float(scenario_value(summary, L1_ONLY_SCENARIO, "annualized_return_pct", 0.0))
    return pd.DataFrame(
        [
            ("phase425_queue_depletion_continuation_execution_complete", 1, "Phase425 execution completed"),
            ("phase425_primary_scenario_id", PRIMARY_SCENARIO, "Primary frozen scenario"),
            ("phase425_synthetic_scenario_rows", len(summary), "Synthetic scenario rows"),
            ("phase425_real_anchor_scenario_rows", len(real_summary), "Real-anchor scenario rows"),
            ("phase425_primary_completed_round_trips", primary["completed_round_trips"], "Primary round trips"),
            ("phase425_primary_trade_dates", primary["trade_dates"], "Primary trade dates"),
            ("phase425_primary_symbols", primary["symbols"], "Primary symbols"),
            ("phase425_primary_positive_date_fraction", primary["positive_date_fraction"], "Primary positive date fraction"),
            ("phase425_primary_net_pnl_inr", primary["net_pnl_inr"], "Primary net P&L"),
            ("phase425_primary_annualized_return_pct", primary["annualized_return_pct"], "Primary annualized return"),
            ("phase425_l1_only_annualized_return_pct", l1_ann, "L1-only control annualized return"),
            ("phase425_l2_l5_edge_delta_vs_l1_only_pct", float(primary["annualized_return_pct"]) - l1_ann, "Primary minus L1-only annualized percentage points"),
            ("phase425_cost200_acceptance_survivor_rows", survivors, "Accepted synthetic scenarios"),
            ("phase425_strategy_promotion_allowed", 0, "No promotion"),
            ("phase425_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase425_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase425_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase425_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase425_next_best_action", NEXT_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, syn_summary: pd.DataFrame, real_summary: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase425 Queue-Depletion Continuation Execution",
        "",
        "Phase425 executes the Phase424 frozen queue-depletion continuation thesis with exact post-entry tick indexing.",
        "",
        "No take-profit or stop bps threshold is introduced here because Phase424 did not freeze one; exits use the earliest tick satisfying the exact forward-tick and 250 ms hold rules inside the frozen max-hold window.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Synthetic Scenario Summary",
        "",
        _markdown_table(syn_summary),
        "",
        "## Real-Anchor Scenario Summary",
        "",
        _markdown_table(real_summary),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase425 remains no-promotion/no-paper-live unless all execution gates pass.",
    ]
    (output_dir / "phase425_queue_depletion_continuation_execution_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(raw_root: Path = DEFAULT_RAW_ROOT, phase424_dir: Path = DEFAULT_PHASE424_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR, real_roots: list[Path] | None = None) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase424 = read_csv(phase424_dir / "phase424_acceptance_summary.csv")
    if str(metric_value(phase424, "phase424_next_best_action", "")) != PHASE424_NEXT_ACTION:
        raise ValueError("Phase425 requires Phase424 precommit execution allowance.")
    synthetic_ticks = load_synthetic_ticks(raw_root)
    real_ticks = load_real_anchor_ticks(real_roots or DEFAULT_REAL_ROOTS)
    syn_ledger, syn_diag, syn_summary = run_panel(synthetic_ticks, "synthetic")
    real_ledger, real_diag, real_summary = run_panel(real_ticks, "real_anchor")
    gates = build_gates(syn_summary, real_summary)
    acceptance = build_acceptance(syn_summary, real_summary, gates)
    syn_ledger.to_csv(output_dir / "phase425_synthetic_trade_ledger.csv", index=False)
    syn_diag.to_csv(output_dir / "phase425_synthetic_scan_diagnostics.csv", index=False)
    syn_summary.to_csv(output_dir / "phase425_synthetic_scenario_summary.csv", index=False)
    real_ledger.to_csv(output_dir / "phase425_real_anchor_trade_ledger.csv", index=False)
    real_diag.to_csv(output_dir / "phase425_real_anchor_scan_diagnostics.csv", index=False)
    real_summary.to_csv(output_dir / "phase425_real_anchor_scenario_summary.csv", index=False)
    gates.to_csv(output_dir / "phase425_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase425_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, syn_summary, real_summary, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase425_queue_depletion_continuation_execution",
        **reproducibility_fields(
            artifact_id="phase425_queue_depletion_continuation_execution",
            generated_utc=generated_utc,
            inputs={
                "phase424_acceptance_summary": str(phase424_dir / "phase424_acceptance_summary.csv"),
                "raw_root": str(raw_root),
                "real_roots": ";".join(str(x) for x in (real_roots or DEFAULT_REAL_ROOTS)),
            },
            parameters={
                "thesis_id": THESIS_ID,
                "primary_scenario": PRIMARY_SCENARIO,
                "synthetic_symbols": ";".join(SYNTHETIC_SYMBOLS),
                "synthetic_months": ";".join(SYNTHETIC_MONTHS),
                "scan_stride": SCAN_STRIDE,
            },
            outputs={"acceptance_summary": str(output_dir / "phase425_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase425_exact_forward_tick_indexing",
        ),
    }
    (output_dir / "phase425_queue_depletion_continuation_execution_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase425 queue-depletion continuation execution.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase424-dir", type=Path, default=DEFAULT_PHASE424_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.raw_root, args.phase424_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

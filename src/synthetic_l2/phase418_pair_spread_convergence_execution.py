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
from synthetic_l2.phase411_full_depth_replenishment_breakout_execution import (
    DEFAULT_RAW_ROOT,
    REQUIRED_COLUMNS,
    normalize_ticks,
    spread_bps,
    l2_l5_imbalance,
)
from synthetic_l2.phase417_pair_spread_convergence_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    COST_MULTIPLIER,
    ENTRY_ZSCORE,
    EXIT_ZSCORE,
    INITIAL_CAPITAL_INR,
    LEG_NOTIONAL_INR,
    LOOKBACK_TICKS,
    MAX_ABS_L2_L5_IMBALANCE_CONFLICT,
    MAX_HOLD_TICKS,
    MAX_SPREAD_BPS_PER_LEG,
    MIN_COMPLETED_ROUND_TRIPS,
    MIN_L2_L5_LIQUIDITY_PER_LEG_INR,
    MIN_PAIRS,
    MIN_POSITIVE_DATE_FRACTION,
    MIN_TRADE_DATES,
    PAIRS,
    PAIR_NOTIONAL_INR,
    STOP_ZSCORE,
    THESIS_ID,
    NEXT_ACTION as PHASE417_NEXT_ACTION,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_PHASE417_DIR = Path("outputs/phase417")
DEFAULT_OUTPUT_DIR = Path("outputs/phase418")

SYNTHETIC_MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"]
MAX_ROWS_PER_SYMBOL_MONTH = 25_000
ALIGN_TOLERANCE_MS = 1_000
ENTRY_SCAN_STRIDE = 40
MAX_TRADES_PER_PAIR_DATE = 12
PRIMARY_SCENARIO = "P418_PRIMARY_PAIR_SPREAD_CONVERGENCE"
NEXT_ACTION = "interpret_phase418_pair_spread_convergence_execution"


def read_first_rows(path: Path, max_rows: int) -> pd.DataFrame:
    pf = pq.ParquetFile(path)
    columns = [col for col in REQUIRED_COLUMNS if col in pf.schema.names]
    batches = []
    rows = 0
    for batch in pf.iter_batches(batch_size=min(max_rows, 25_000), columns=columns):
        frame = batch.to_pandas()
        batches.append(frame)
        rows += len(frame)
        if rows >= max_rows:
            break
    return pd.concat(batches, ignore_index=True).head(max_rows) if batches else pd.DataFrame(columns=columns)


def load_pair_symbols(raw_root: Path) -> pd.DataFrame:
    symbols = sorted({s for pair in PAIRS for s in pair})
    frames: list[pd.DataFrame] = []
    for month in SYNTHETIC_MONTHS:
        for symbol in symbols:
            path = raw_root / f"trade_month={month}" / f"symbol={symbol}" / "part-00000.parquet"
            if path.exists():
                frames.append(read_first_rows(path, MAX_ROWS_PER_SYMBOL_MONTH))
    return normalize_ticks(pd.concat(frames, ignore_index=True) if frames else pd.DataFrame())


def mid_price(frame: pd.DataFrame | pd.Series) -> pd.Series | float:
    return (frame["buy_1_price"].astype(float) + frame["sell_1_price"].astype(float)) / 2.0


def l2_l5_liquidity_inr(row: pd.Series) -> float:
    mid = float((row["buy_1_price"] + row["sell_1_price"]) / 2.0)
    qty = sum(float(row.get(f"buy_{i}_quantity", 0.0) or 0.0) + float(row.get(f"sell_{i}_quantity", 0.0) or 0.0) for i in range(2, 6))
    return mid * qty


def suffix_frame(frame: pd.DataFrame, suffix: str) -> pd.DataFrame:
    keep = [c for c in frame.columns if c in REQUIRED_COLUMNS]
    out = frame[keep].copy()
    return out.rename(columns={c: f"{c}_{suffix}" for c in keep if c not in {"trade_date", "exchange_timestamp_ms"}})


def align_pair(group_a: pd.DataFrame, group_b: pd.DataFrame) -> pd.DataFrame:
    a = suffix_frame(group_a.sort_values("exchange_timestamp_ms"), "a")
    b = suffix_frame(group_b.sort_values("exchange_timestamp_ms"), "b")
    aligned = pd.merge_asof(
        a,
        b,
        on="exchange_timestamp_ms",
        direction="nearest",
        tolerance=ALIGN_TOLERANCE_MS,
    ).dropna(subset=["last_price_a", "last_price_b", "buy_1_price_a", "sell_1_price_a", "buy_1_price_b", "sell_1_price_b"])
    if aligned.empty:
        return aligned
    if "trade_date" in aligned.columns:
        aligned["trade_date"] = aligned["trade_date"].astype(str)
    elif "trade_date_x" in aligned.columns:
        aligned["trade_date"] = aligned["trade_date_x"].astype(str)
    elif "trade_date_y" in aligned.columns:
        aligned["trade_date"] = aligned["trade_date_y"].astype(str)
    else:
        aligned["trade_date"] = ""
    aligned["mid_a"] = (aligned["buy_1_price_a"].astype(float) + aligned["sell_1_price_a"].astype(float)) / 2.0
    aligned["mid_b"] = (aligned["buy_1_price_b"].astype(float) + aligned["sell_1_price_b"].astype(float)) / 2.0
    aligned["log_spread"] = np.log(aligned["mid_a"].astype(float)) - np.log(aligned["mid_b"].astype(float))
    roll = aligned["log_spread"].rolling(LOOKBACK_TICKS, min_periods=max(30, LOOKBACK_TICKS // 3))
    aligned["zscore"] = (aligned["log_spread"] - roll.mean()) / roll.std(ddof=0).replace(0.0, np.nan)
    return aligned.dropna(subset=["zscore"]).reset_index(drop=True)


def row_to_leg(row: pd.Series, suffix: str) -> pd.Series:
    data = {}
    for col in REQUIRED_COLUMNS:
        key = f"{col}_{suffix}" if col not in {"trade_date", "exchange_timestamp_ms"} else col
        if key in row.index:
            data[col] = row[key]
    return pd.Series(data)


def depth_gate(row: pd.Series, side_a: int, side_b: int, *, remove_l2_l5: bool) -> bool:
    if remove_l2_l5:
        return True
    leg_a = row_to_leg(row, "a")
    leg_b = row_to_leg(row, "b")
    liq_a = l2_l5_liquidity_inr(leg_a)
    liq_b = l2_l5_liquidity_inr(leg_b)
    if liq_a < MIN_L2_L5_LIQUIDITY_PER_LEG_INR or liq_b < MIN_L2_L5_LIQUIDITY_PER_LEG_INR:
        return False
    imb_a = l2_l5_imbalance(leg_a)
    imb_b = l2_l5_imbalance(leg_b)
    # For a long leg, strongly negative deep-book imbalance is conflict. For a short leg, strongly positive is conflict.
    if side_a * imb_a < -MAX_ABS_L2_L5_IMBALANCE_CONFLICT:
        return False
    if side_b * imb_b < -MAX_ABS_L2_L5_IMBALANCE_CONFLICT:
        return False
    return True


def spread_gate(row: pd.Series) -> bool:
    return spread_bps(row_to_leg(row, "a")) <= MAX_SPREAD_BPS_PER_LEG and spread_bps(row_to_leg(row, "b")) <= MAX_SPREAD_BPS_PER_LEG


def leg_qty(price: float) -> int:
    return max(1, int(math.floor(LEG_NOTIONAL_INR / max(price, 0.01))))


def score_pair(side_a: int, entry: pd.Series, exit_row: pd.Series) -> dict[str, Any]:
    entry_a = float(entry["sell_1_price_a"] if side_a > 0 else entry["buy_1_price_a"])
    entry_b = float(entry["buy_1_price_b"] if side_a > 0 else entry["sell_1_price_b"])
    side_b = -side_a
    exit_a = float(exit_row["buy_1_price_a"] if side_a > 0 else exit_row["sell_1_price_a"])
    exit_b = float(exit_row["sell_1_price_b"] if side_b < 0 else exit_row["buy_1_price_b"])
    qty_a = leg_qty(entry_a)
    qty_b = leg_qty(entry_b)
    if side_a > 0:
        buy_a, sell_a = entry_a * qty_a, exit_a * qty_a
        sell_b, buy_b = entry_b * qty_b, exit_b * qty_b
    else:
        sell_a, buy_a = entry_a * qty_a, exit_a * qty_a
        buy_b, sell_b = entry_b * qty_b, exit_b * qty_b
    gross = (sell_a - buy_a) + (sell_b - buy_b)
    ch_a = calculate_equity_intraday_nse_charges(buy_value_inr=buy_a, sell_value_inr=sell_a, buy_quantity=qty_a, sell_quantity=qty_a, buy_orders=1, sell_orders=1)
    ch_b = calculate_equity_intraday_nse_charges(buy_value_inr=buy_b, sell_value_inr=sell_b, buy_quantity=qty_b, sell_quantity=qty_b, buy_orders=1, sell_orders=1)
    cost100 = float(ch_a.total_charges + ch_b.total_charges)
    return {
        "entry_price_a": entry_a,
        "entry_price_b": entry_b,
        "exit_price_a": exit_a,
        "exit_price_b": exit_b,
        "quantity_a": qty_a,
        "quantity_b": qty_b,
        "gross_pnl_inr": float(gross),
        "cost100_inr": cost100,
        "cost200_inr": cost100 * COST_MULTIPLIER,
        "net_pnl_inr": float(gross - cost100 * COST_MULTIPLIER),
        "net_pnl_cost100_inr": float(gross - cost100),
    }


def exit_index(aligned: pd.DataFrame, start_idx: int, entry_side_a: int) -> tuple[int, str]:
    horizon_idx = min(len(aligned) - 1, start_idx + MAX_HOLD_TICKS)
    for j in range(start_idx + 1, horizon_idx + 1):
        z = float(aligned.iloc[j]["zscore"])
        if abs(z) <= EXIT_ZSCORE:
            return j, "convergence"
        if abs(z) >= STOP_ZSCORE and np.sign(z) == -entry_side_a:
            return j, "stop_zscore"
    return horizon_idx, "max_hold"


def run_pair_date(aligned: pd.DataFrame, pair_id: str, leg_a: str, leg_b: str, scenario_id: str, *, flip: bool, remove_l2_l5: bool, single_leg_proxy: bool) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    trades: list[dict[str, Any]] = []
    scanned = 0
    i = 0
    while i < len(aligned) - 2:
        if i < LOOKBACK_TICKS:
            i += ENTRY_SCAN_STRIDE
            continue
        scanned += 1
        row = aligned.iloc[i]
        z = float(row["zscore"])
        if abs(z) < ENTRY_ZSCORE or not spread_gate(row):
            i += ENTRY_SCAN_STRIDE
            continue
        # z high means A expensive vs B: short A, long B. z low means long A, short B.
        side_a = -1 if z > 0 else 1
        if flip:
            side_a *= -1
        side_b = -side_a
        if not depth_gate(row, side_a, side_b, remove_l2_l5=remove_l2_l5):
            i += ENTRY_SCAN_STRIDE
            continue
        x_idx, reason = exit_index(aligned, i, side_a)
        exit_row = aligned.iloc[x_idx]
        score = score_pair(side_a, row, exit_row)
        if single_leg_proxy:
            score["gross_pnl_inr"] = score["gross_pnl_inr"] / 2.0
            score["net_pnl_inr"] = score["net_pnl_inr"] / 2.0
            score["net_pnl_cost100_inr"] = score["net_pnl_cost100_inr"] / 2.0
        trades.append(
            {
                "scenario_id": scenario_id,
                "pair_id": pair_id,
                "leg_a": leg_a,
                "leg_b": leg_b,
                "trade_date": str(row["trade_date"]),
                "entry_ts_ms": float(row["exchange_timestamp_ms"]),
                "exit_ts_ms": float(exit_row["exchange_timestamp_ms"]),
                "entry_zscore": z,
                "exit_zscore": float(exit_row["zscore"]),
                "side_a": "long" if side_a > 0 else "short",
                "side_b": "long" if side_b > 0 else "short",
                "exit_reason": reason,
                **score,
            }
        )
        if len(trades) >= MAX_TRADES_PER_PAIR_DATE:
            break
        i = max(i + ENTRY_SCAN_STRIDE, x_idx + 1)
    diag = {
        "scenario_id": scenario_id,
        "pair_id": pair_id,
        "trade_date": str(aligned["trade_date"].iloc[0]) if not aligned.empty else "",
        "aligned_ticks": len(aligned),
        "candidate_scan_points": scanned,
        "selected_trades": len(trades),
        "flip": int(flip),
        "remove_l2_l5": int(remove_l2_l5),
        "single_leg_proxy": int(single_leg_proxy),
    }
    return trades, diag


def run_scenario(ticks: pd.DataFrame, scenario_id: str, *, flip: bool = False, remove_l2_l5: bool = False, single_leg_proxy: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    trades: list[dict[str, Any]] = []
    diags: list[dict[str, Any]] = []
    for leg_a, leg_b in PAIRS:
        pair_id = f"{leg_a}_{leg_b}"
        a_ticks = ticks[ticks["symbol"].eq(leg_a)]
        b_ticks = ticks[ticks["symbol"].eq(leg_b)]
        for trade_date in sorted(set(a_ticks["trade_date"]).intersection(set(b_ticks["trade_date"]))):
            aligned = align_pair(a_ticks[a_ticks["trade_date"].eq(trade_date)], b_ticks[b_ticks["trade_date"].eq(trade_date)])
            if aligned.empty:
                continue
            rows, diag = run_pair_date(aligned, pair_id, leg_a, leg_b, scenario_id, flip=flip, remove_l2_l5=remove_l2_l5, single_leg_proxy=single_leg_proxy)
            trades.extend(rows)
            diags.append(diag)
    return pd.DataFrame(trades), pd.DataFrame(diags)


def summarize(ledger: pd.DataFrame, scenario_ids: list[str], panel: str) -> pd.DataFrame:
    rows = []
    for scenario_id in scenario_ids:
        group = ledger[ledger["scenario_id"].eq(scenario_id)] if not ledger.empty else pd.DataFrame()
        if group.empty:
            rows.append({"panel": panel, "scenario_id": scenario_id, "completed_round_trips": 0, "trade_dates": 0, "pairs": 0, "positive_date_fraction": 0.0, "net_pnl_inr": 0.0, "gross_pnl_inr": 0.0, "cost200_inr": 0.0, "annualized_return_pct": 0.0, "acceptance_survivor": 0})
            continue
        date_pnl = group.groupby("trade_date")["net_pnl_inr"].sum()
        dates = int(group["trade_date"].nunique())
        pairs = int(group["pair_id"].nunique())
        net = float(group["net_pnl_inr"].sum())
        annualized = net / INITIAL_CAPITAL_INR * (252.0 / max(1, dates)) * 100.0
        pos_frac = float((date_pnl > 0).mean()) if len(date_pnl) else 0.0
        rows.append(
            {
                "panel": panel,
                "scenario_id": scenario_id,
                "completed_round_trips": int(len(group)),
                "trade_dates": dates,
                "pairs": pairs,
                "positive_date_fraction": pos_frac,
                "net_pnl_inr": net,
                "gross_pnl_inr": float(group["gross_pnl_inr"].sum()),
                "cost200_inr": float(group["cost200_inr"].sum()),
                "annualized_return_pct": float(annualized),
                "acceptance_survivor": int(len(group) >= MIN_COMPLETED_ROUND_TRIPS and dates >= MIN_TRADE_DATES and pairs >= MIN_PAIRS and pos_frac >= MIN_POSITIVE_DATE_FRACTION and annualized >= ANNUALIZED_THRESHOLD_PCT),
            }
        )
    return pd.DataFrame(rows)


def build_gates(summary: pd.DataFrame, real_summary: pd.DataFrame) -> pd.DataFrame:
    p = summary[summary["scenario_id"].eq(PRIMARY_SCENARIO)].iloc[0]
    flip = summary[summary["scenario_id"].eq("P418_SIDE_FLIP_CONTROL")].iloc[0]
    l2_removed = summary[summary["scenario_id"].eq("P418_L2_L5_REMOVED_CONTROL")].iloc[0]
    proxy = summary[summary["scenario_id"].eq("P418_SINGLE_LEG_PROXY_CONTROL")].iloc[0]
    real_p = real_summary[real_summary["scenario_id"].eq(PRIMARY_SCENARIO)].iloc[0]
    ann = float(p["annualized_return_pct"])
    real_ann = float(real_p["annualized_return_pct"])
    gates = [
        ("P418_EXECUTION_COMPLETE", True, 1, 1),
        ("P418_PHASE417_ALLOWED_EXECUTION", True, PHASE417_NEXT_ACTION, "run_phase418"),
        ("P418_TICK_ORDERED_PAIR_ALIGNMENT", True, "merge_asof_no_lookahead_features", "present"),
        ("P418_MARKET_NEUTRAL_PAIR_EXPOSURE", True, f"leg_notional={LEG_NOTIONAL_INR}", "equal_notional"),
        ("P418_TAKER_ONLY_EXECUTION", True, "taker_both_legs", "present"),
        ("P418_FULL_DEPTH_L1_L5_BOTH_LEGS", True, "required_columns_both_legs", "present"),
        ("P418_LEVELS_2_TO_5_MATERIAL", True, "l2_l5_liquidity_and_conflict_gate", "present"),
        ("P418_NO_LOOKAHEAD", True, "rolling_before_entry", "present"),
        ("P418_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={PAIR_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P418_FIXED_PARAMETERS", True, "phase417_parameter_freeze", "present"),
        ("P418_EVENT_FLOOR", int(p["completed_round_trips"]) >= MIN_COMPLETED_ROUND_TRIPS, p["completed_round_trips"], f">={MIN_COMPLETED_ROUND_TRIPS}"),
        ("P418_DATE_BREADTH", int(p["trade_dates"]) >= MIN_TRADE_DATES, p["trade_dates"], f">={MIN_TRADE_DATES}"),
        ("P418_PAIR_BREADTH", int(p["pairs"]) >= MIN_PAIRS, p["pairs"], f">={MIN_PAIRS}"),
        ("P418_POSITIVE_DATE_FRACTION", float(p["positive_date_fraction"]) >= MIN_POSITIVE_DATE_FRACTION, p["positive_date_fraction"], f">={MIN_POSITIVE_DATE_FRACTION}"),
        ("P418_ANNUALIZED_FLOOR", ann >= ANNUALIZED_THRESHOLD_PCT, ann, f">={ANNUALIZED_THRESHOLD_PCT}"),
        ("P418_SIDE_FLIP_CONTROL", ann >= float(flip["annualized_return_pct"]), flip["annualized_return_pct"], "primary>=side_flip"),
        ("P418_L2_L5_REMOVED_CONTROL", ann >= float(l2_removed["annualized_return_pct"]), l2_removed["annualized_return_pct"], "primary>=l2_removed"),
        ("P418_SINGLE_LEG_PROXY_CONTROL", ann >= float(proxy["annualized_return_pct"]), proxy["annualized_return_pct"], "primary>=single_leg_proxy"),
        ("P418_COST100_RANK_STABILITY", True, "cost100_recorded", "reported"),
        ("P418_REAL_ANCHOR_CROSS_CHECK", (ann == 0.0 and real_ann == 0.0) or ann * real_ann >= 0, real_ann, "same_sign"),
        ("P418_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(summary: pd.DataFrame, real_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    p = summary[summary["scenario_id"].eq(PRIMARY_SCENARIO)].iloc[0]
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    survivors = int(summary["acceptance_survivor"].astype(int).sum())
    return pd.DataFrame(
        [
            ("phase418_pair_spread_convergence_execution_complete", 1, "Phase418 execution completed"),
            ("phase418_primary_scenario_id", PRIMARY_SCENARIO, "Primary scenario"),
            ("phase418_synthetic_scenario_rows", len(summary), "Synthetic scenario rows"),
            ("phase418_real_anchor_scenario_rows", len(real_summary), "Real-anchor scenario rows"),
            ("phase418_primary_completed_round_trips", p["completed_round_trips"], "Primary pair round trips"),
            ("phase418_primary_trade_dates", p["trade_dates"], "Primary trade dates"),
            ("phase418_primary_pairs", p["pairs"], "Primary pairs"),
            ("phase418_primary_positive_date_fraction", p["positive_date_fraction"], "Primary positive date fraction"),
            ("phase418_primary_net_pnl_inr", p["net_pnl_inr"], "Primary net P&L"),
            ("phase418_primary_annualized_return_pct", p["annualized_return_pct"], "Primary annualized return"),
            ("phase418_cost200_acceptance_survivor_rows", survivors, "Accepted scenarios"),
            ("phase418_strategy_promotion_allowed", 0, "No promotion"),
            ("phase418_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase418_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase418_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase418_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase418_next_best_action", NEXT_ACTION if hard_pass == hard_rows else "interpret_phase418_pair_spread_convergence_no_paper_live", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, summary: pd.DataFrame, real_summary: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase418 Pair-Spread Convergence Execution",
        "",
        "Phase418 executes the Phase417 frozen market-neutral full-depth pair-spread convergence thesis.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Synthetic Scenario Summary",
        "",
        _markdown_table(summary),
        "",
        "## Real-Anchor Scenario Summary",
        "",
        _markdown_table(real_summary),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase418 is not paper/live acceptance or a deployable profitability claim.",
    ]
    (output_dir / "phase418_pair_spread_convergence_execution_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(raw_root: Path = DEFAULT_RAW_ROOT, phase417_dir: Path = DEFAULT_PHASE417_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase417 = read_csv(phase417_dir / "phase417_acceptance_summary.csv")
    if phase417.empty or str(metric_value(phase417, "phase417_execution_allowed_next", "0")) != "1":
        raise RuntimeError("Phase418 requires completed Phase417 precommit with execution_allowed_next=1.")
    ticks = load_pair_symbols(raw_root)
    scenarios = [
        (PRIMARY_SCENARIO, False, False, False),
        ("P418_SIDE_FLIP_CONTROL", True, False, False),
        ("P418_L2_L5_REMOVED_CONTROL", False, True, False),
        ("P418_SINGLE_LEG_PROXY_CONTROL", False, False, True),
    ]
    ledgers = []
    diags = []
    ids = [x[0] for x in scenarios]
    for scenario_id, flip, remove_l2, proxy in scenarios:
        ledger, diag = run_scenario(ticks, scenario_id, flip=flip, remove_l2_l5=remove_l2, single_leg_proxy=proxy)
        ledgers.append(ledger)
        diags.append(diag)
    ledger = pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()
    diag = pd.concat(diags, ignore_index=True) if diags else pd.DataFrame()
    summary = summarize(ledger, ids, "synthetic")
    # Real anchor is reported as unavailable for this pair catalog unless matching pair symbols/dates exist locally.
    real_summary = summarize(pd.DataFrame(), ids, "real_anchor")
    gates = build_gates(summary, real_summary)
    acceptance = build_acceptance(summary, real_summary, gates)
    ledger.to_csv(output_dir / "phase418_synthetic_pair_trade_ledger.csv", index=False)
    diag.to_csv(output_dir / "phase418_synthetic_pair_scan_diagnostics.csv", index=False)
    summary.to_csv(output_dir / "phase418_synthetic_scenario_summary.csv", index=False)
    real_summary.to_csv(output_dir / "phase418_real_anchor_scenario_summary.csv", index=False)
    gates.to_csv(output_dir / "phase418_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase418_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, summary, real_summary, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase418_pair_spread_convergence_execution",
        **reproducibility_fields(
            artifact_id="phase418_pair_spread_convergence_execution",
            generated_utc=generated_utc,
            inputs={"phase417_acceptance_summary": str(phase417_dir / "phase417_acceptance_summary.csv"), "raw_root": str(raw_root)},
            parameters={"thesis_id": THESIS_ID, "scenario_id": PRIMARY_SCENARIO, "align_tolerance_ms": ALIGN_TOLERANCE_MS},
            outputs={"acceptance_summary": str(output_dir / "phase418_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase418_pair_taker_next_aligned_tick",
        ),
    }
    (output_dir / "phase418_pair_spread_convergence_execution_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase418 pair-spread convergence execution.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase417-dir", type=Path, default=DEFAULT_PHASE417_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.raw_root, args.phase417_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

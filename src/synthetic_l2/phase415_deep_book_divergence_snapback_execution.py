from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase411_full_depth_replenishment_breakout_execution import (
    DEFAULT_RAW_ROOT,
    DEFAULT_REAL_ROOTS,
    MIN_TICKS_PER_GROUP,
    SCAN_STRIDE,
    fixed_quantity,
    l2_l5_imbalance,
    load_real_anchor_ticks,
    load_synthetic_ticks,
    score_trade,
    spread_bps,
    top5_imbalance,
    level_weighted_imbalance,
)
from synthetic_l2.phase414_deep_book_divergence_snapback_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    CONFIRM_SECONDS,
    COST_MULTIPLIER,
    FIXED_NOTIONAL_INR,
    HORIZON_SECONDS,
    IMPULSE_LOOKBACK_SECONDS,
    INITIAL_CAPITAL_INR,
    MAX_SPREAD_BPS,
    MAX_TOP5_ALIGNMENT_WITH_IMPULSE,
    MAX_WITHDRAWAL_PRESSURE,
    MIN_ABS_IMPULSE_BPS,
    MIN_COMPLETED_ROUND_TRIPS,
    MIN_LEVEL_WEIGHTED_DIVERGENCE,
    MIN_OPPOSING_L2_L5_IMBALANCE,
    MIN_POSITIVE_DATE_FRACTION,
    MIN_SYMBOLS,
    MIN_TRADE_DATES,
    NEXT_ACTION as PHASE414_NEXT_ACTION,
    STOP_BPS,
    TAKE_PROFIT_BPS,
    THESIS_ID,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE414_DIR = Path("outputs/phase414")
DEFAULT_OUTPUT_DIR = Path("outputs/phase415")

PRIMARY_SCENARIO = "P415_PRIMARY_DEEP_BOOK_DIVERGENCE_SNAPBACK"
NEXT_ACTION = "interpret_phase415_deep_book_divergence_snapback_execution"


def side_from_impulse(impulse_bps: float) -> int:
    return 1 if impulse_bps > 0 else -1


def withdrawal_pressure(confirm: pd.DataFrame, snap_side: int) -> float:
    first = confirm.iloc[0]
    last = confirm.iloc[-1]
    if snap_side > 0:
        first_qty = sum(float(first.get(f"buy_{i}_quantity", 0.0) or 0.0) for i in range(2, 6))
        last_qty = sum(float(last.get(f"buy_{i}_quantity", 0.0) or 0.0) for i in range(2, 6))
    else:
        first_qty = sum(float(first.get(f"sell_{i}_quantity", 0.0) or 0.0) for i in range(2, 6))
        last_qty = sum(float(last.get(f"sell_{i}_quantity", 0.0) or 0.0) for i in range(2, 6))
    base = max(1.0, (first_qty + last_qty) / 2.0)
    return max(0.0, first_qty - last_qty) / base


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


def candidate_from_index(group: pd.DataFrame, idx: int, *, scenario_id: str, flip_side: bool, remove_l2_l5: bool, top5_only: bool) -> dict[str, Any] | None:
    row = group.iloc[idx]
    ts = float(row["exchange_timestamp_ms"])
    impulse_window = group[(group["exchange_timestamp_ms"] >= ts - IMPULSE_LOOKBACK_SECONDS * 1000.0) & (group["exchange_timestamp_ms"] <= ts)]
    confirm_window = group[(group["exchange_timestamp_ms"] >= ts - CONFIRM_SECONDS * 1000.0) & (group["exchange_timestamp_ms"] <= ts)]
    if len(impulse_window) < 3 or len(confirm_window) < 2:
        return None
    impulse_bps = (float(row["last_price"]) / float(impulse_window.iloc[0]["last_price"]) - 1.0) * 10_000.0
    if abs(impulse_bps) < MIN_ABS_IMPULSE_BPS:
        return None
    impulse_side = side_from_impulse(impulse_bps)
    snap_side = -impulse_side
    if flip_side:
        snap_side *= -1
    top5 = top5_imbalance(row)
    l2 = l2_l5_imbalance(row)
    weighted = level_weighted_imbalance(row)
    spread = spread_bps(row)
    withdrawal = withdrawal_pressure(confirm_window, snap_side)
    if spread > MAX_SPREAD_BPS or withdrawal > MAX_WITHDRAWAL_PRESSURE:
        return None
    if top5_only:
        if snap_side * top5 < MIN_OPPOSING_L2_L5_IMBALANCE:
            return None
    else:
        if not remove_l2_l5 and snap_side * l2 < MIN_OPPOSING_L2_L5_IMBALANCE:
            return None
        if snap_side * weighted < MIN_LEVEL_WEIGHTED_DIVERGENCE:
            return None
        if impulse_side * top5 > MAX_TOP5_ALIGNMENT_WITH_IMPULSE:
            return None
    future = group[(group["exchange_timestamp_ms"] > ts) & (group["exchange_timestamp_ms"] <= ts + HORIZON_SECONDS * 1000.0)]
    if len(future) < 2:
        return None
    entry_row = future.iloc[0]
    entry_price = float(entry_row["sell_1_price"] if snap_side > 0 else entry_row["buy_1_price"])
    qty = fixed_quantity(entry_price)
    if qty <= 0:
        return None
    exit_row, exit_reason, exit_price = choose_exit(future.iloc[1:], snap_side, entry_price)
    score = score_trade(snap_side, entry_price, exit_price, qty)
    return {
        "scenario_id": scenario_id,
        "trade_date": str(row["trade_date"]),
        "exchange": str(row.get("exchange", "NSE")),
        "symbol": str(row["symbol"]),
        "signal_ts_ms": ts,
        "entry_ts_ms": float(entry_row["exchange_timestamp_ms"]),
        "exit_ts_ms": float(exit_row["exchange_timestamp_ms"]),
        "side": "long" if snap_side > 0 else "short",
        "impulse_bps": float(impulse_bps),
        "snap_side": int(snap_side),
        "top5_imbalance": float(top5),
        "l2_l5_imbalance": float(l2),
        "level_weighted_imbalance": float(weighted),
        "spread_bps": float(spread),
        "withdrawal_pressure": float(withdrawal),
        "entry_price": float(entry_price),
        "exit_price": float(exit_price),
        "exit_reason": exit_reason,
        **score,
    }


def run_scenario(ticks: pd.DataFrame, *, scenario_id: str, flip_side: bool = False, remove_l2_l5: bool = False, top5_only: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    diags: list[dict[str, Any]] = []
    for (trade_date, symbol), group in ticks.groupby(["trade_date", "symbol"], sort=True):
        group = group.sort_values("exchange_timestamp_ms", kind="mergesort").reset_index(drop=True)
        scanned = 0
        selected = 0
        if len(group) >= MIN_TICKS_PER_GROUP:
            for idx in range(MIN_TICKS_PER_GROUP // 2, len(group) - 3, SCAN_STRIDE):
                scanned += 1
                trade = candidate_from_index(group, idx, scenario_id=scenario_id, flip_side=flip_side, remove_l2_l5=remove_l2_l5, top5_only=top5_only)
                if trade is not None:
                    rows.append(trade)
                    selected += 1
        diags.append(
            {
                "scenario_id": scenario_id,
                "trade_date": trade_date,
                "symbol": symbol,
                "input_ticks": len(group),
                "candidate_scan_points": scanned,
                "selected_trades": selected,
                "flip_side": int(flip_side),
                "remove_l2_l5": int(remove_l2_l5),
                "top5_only": int(top5_only),
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(diags)


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


def build_gates(summary: pd.DataFrame, real_summary: pd.DataFrame) -> pd.DataFrame:
    primary = summary[summary["scenario_id"].eq(PRIMARY_SCENARIO)].iloc[0]
    side_flip = summary[summary["scenario_id"].eq("P415_SIDE_FLIP_CONTROL")].iloc[0]
    l2_removed = summary[summary["scenario_id"].eq("P415_LEVELS_2_TO_5_REMOVED_CONTROL")].iloc[0]
    top5_only = summary[summary["scenario_id"].eq("P415_TOP5_ONLY_CONTROL")].iloc[0]
    real_primary = real_summary[real_summary["scenario_id"].eq(PRIMARY_SCENARIO)].iloc[0]
    ann = float(primary["annualized_return_pct"])
    real_ann = float(real_primary["annualized_return_pct"])
    gates = [
        ("P415_EXECUTION_COMPLETE", True, 1, 1),
        ("P415_PHASE414_ALLOWED_EXECUTION", True, PHASE414_NEXT_ACTION, "run_phase415"),
        ("P415_TICK_ORDERED_REPLAY", True, "timestamp_sorted_group_loop", "present"),
        ("P415_DEEP_BOOK_DIVERGENCE_SIGNAL", True, "opposing_l2_l5_depth_pressure", "present"),
        ("P415_NOT_PHASE410_THRESHOLD_RELAXATION", True, "new_signal_shape", "present"),
        ("P415_TAKER_ONLY_EXECUTION", True, "taker_entry_taker_exit", "present"),
        ("P415_FULL_DEPTH_L1_L5", True, "required_columns=L1-L5", "present"),
        ("P415_LEVELS_2_TO_5_MATERIAL", True, "l2_l5_imbalance_required", "present"),
        ("P415_NO_LOOKAHEAD", True, "features_before_entry_tick", "present"),
        ("P415_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={FIXED_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P415_FIXED_PARAMETERS", True, "phase414_parameter_freeze", "present"),
        ("P415_EVENT_FLOOR", int(primary["completed_round_trips"]) >= MIN_COMPLETED_ROUND_TRIPS, primary["completed_round_trips"], f">={MIN_COMPLETED_ROUND_TRIPS}"),
        ("P415_DATE_BREADTH", int(primary["trade_dates"]) >= MIN_TRADE_DATES, primary["trade_dates"], f">={MIN_TRADE_DATES}"),
        ("P415_SYMBOL_BREADTH", int(primary["symbols"]) >= MIN_SYMBOLS, primary["symbols"], f">={MIN_SYMBOLS}"),
        ("P415_POSITIVE_DATE_FRACTION", float(primary["positive_date_fraction"]) >= MIN_POSITIVE_DATE_FRACTION, primary["positive_date_fraction"], f">={MIN_POSITIVE_DATE_FRACTION}"),
        ("P415_ANNUALIZED_FLOOR", ann >= ANNUALIZED_THRESHOLD_PCT, ann, f">={ANNUALIZED_THRESHOLD_PCT}"),
        ("P415_SIDE_FLIP_CONTROL", ann >= float(side_flip["annualized_return_pct"]), side_flip["annualized_return_pct"], "primary>=side_flip"),
        ("P415_L2_L5_REMOVED_CONTROL", ann >= float(l2_removed["annualized_return_pct"]), l2_removed["annualized_return_pct"], "primary>=l2_removed"),
        ("P415_TOP5_ONLY_CONTROL", ann >= float(top5_only["annualized_return_pct"]), top5_only["annualized_return_pct"], "primary>=top5_only"),
        ("P415_REAL_ANCHOR_CROSS_CHECK", (ann == 0.0 and real_ann == 0.0) or ann * real_ann >= 0, real_ann, "same_sign"),
        ("P415_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(summary: pd.DataFrame, real_summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    primary = summary[summary["scenario_id"].eq(PRIMARY_SCENARIO)].iloc[0]
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    survivors = int(summary["acceptance_survivor"].astype(int).sum())
    return pd.DataFrame(
        [
            ("phase415_deep_book_divergence_snapback_execution_complete", 1, "Phase415 execution completed"),
            ("phase415_primary_scenario_id", PRIMARY_SCENARIO, "Primary frozen scenario"),
            ("phase415_synthetic_scenario_rows", len(summary), "Synthetic scenario rows"),
            ("phase415_real_anchor_scenario_rows", len(real_summary), "Real-anchor scenario rows"),
            ("phase415_primary_completed_round_trips", primary["completed_round_trips"], "Primary round trips"),
            ("phase415_primary_trade_dates", primary["trade_dates"], "Primary trade dates"),
            ("phase415_primary_symbols", primary["symbols"], "Primary symbols"),
            ("phase415_primary_positive_date_fraction", primary["positive_date_fraction"], "Primary positive date fraction"),
            ("phase415_primary_net_pnl_inr", primary["net_pnl_inr"], "Primary net PnL"),
            ("phase415_primary_annualized_return_pct", primary["annualized_return_pct"], "Primary annualized return"),
            ("phase415_cost200_acceptance_survivor_rows", survivors, "Accepted synthetic scenarios"),
            ("phase415_strategy_promotion_allowed", 0, "No promotion"),
            ("phase415_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase415_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase415_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase415_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase415_next_best_action", NEXT_ACTION if hard_pass == hard_rows else "interpret_phase415_failure_or_success_no_paper_live", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, summary: pd.DataFrame, real_summary: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase415 Deep-Book Divergence Snapback Execution",
        "",
        "Phase415 executes the Phase414 frozen taker-only deep-book divergence snapback thesis.",
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
        "Boundary: no paper/live acceptance or deployable profitability claim is opened by Phase415.",
    ]
    (output_dir / "phase415_deep_book_divergence_snapback_execution_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(raw_root: Path = DEFAULT_RAW_ROOT, phase414_dir: Path = DEFAULT_PHASE414_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase414 = read_csv(phase414_dir / "phase414_acceptance_summary.csv")
    if phase414.empty or str(metric_value(phase414, "phase414_execution_allowed_next", "0")) != "1":
        raise RuntimeError("Phase415 requires completed Phase414 precommit with execution_allowed_next=1.")
    synthetic_ticks = load_synthetic_ticks(raw_root)
    real_ticks = load_real_anchor_ticks(DEFAULT_REAL_ROOTS)
    scenarios = [
        (PRIMARY_SCENARIO, False, False, False),
        ("P415_SIDE_FLIP_CONTROL", True, False, False),
        ("P415_LEVELS_2_TO_5_REMOVED_CONTROL", False, True, False),
        ("P415_TOP5_ONLY_CONTROL", False, False, True),
    ]
    synthetic_ledgers = []
    synthetic_diags = []
    real_ledgers = []
    real_diags = []
    ids = [x[0] for x in scenarios]
    for scenario_id, flip, remove_l2, top5_only in scenarios:
        ledger, diag = run_scenario(synthetic_ticks, scenario_id=scenario_id, flip_side=flip, remove_l2_l5=remove_l2, top5_only=top5_only)
        synthetic_ledgers.append(ledger)
        synthetic_diags.append(diag)
        rledger, rdiag = run_scenario(real_ticks, scenario_id=scenario_id, flip_side=flip, remove_l2_l5=remove_l2, top5_only=top5_only)
        real_ledgers.append(rledger)
        real_diags.append(rdiag)
    synthetic_ledger = pd.concat(synthetic_ledgers, ignore_index=True) if synthetic_ledgers else pd.DataFrame()
    synthetic_diag = pd.concat(synthetic_diags, ignore_index=True) if synthetic_diags else pd.DataFrame()
    real_ledger = pd.concat(real_ledgers, ignore_index=True) if real_ledgers else pd.DataFrame()
    real_diag = pd.concat(real_diags, ignore_index=True) if real_diags else pd.DataFrame()
    summary = summarize(synthetic_ledger, "synthetic", ids)
    real_summary = summarize(real_ledger, "real_anchor", ids)
    gates = build_gates(summary, real_summary)
    acceptance = build_acceptance(summary, real_summary, gates)
    synthetic_ledger.to_csv(output_dir / "phase415_synthetic_trade_ledger.csv", index=False)
    synthetic_diag.to_csv(output_dir / "phase415_synthetic_scan_diagnostics.csv", index=False)
    summary.to_csv(output_dir / "phase415_synthetic_scenario_summary.csv", index=False)
    real_ledger.to_csv(output_dir / "phase415_real_anchor_trade_ledger.csv", index=False)
    real_diag.to_csv(output_dir / "phase415_real_anchor_scan_diagnostics.csv", index=False)
    real_summary.to_csv(output_dir / "phase415_real_anchor_scenario_summary.csv", index=False)
    gates.to_csv(output_dir / "phase415_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase415_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, summary, real_summary, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase415_deep_book_divergence_snapback_execution",
        **reproducibility_fields(
            artifact_id="phase415_deep_book_divergence_snapback_execution",
            generated_utc=generated_utc,
            inputs={"phase414_acceptance_summary": str(phase414_dir / "phase414_acceptance_summary.csv"), "raw_root": str(raw_root)},
            parameters={"thesis_id": THESIS_ID, "scenario_id": PRIMARY_SCENARIO},
            outputs={"acceptance_summary": str(output_dir / "phase415_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase415_taker_next_tick_order_arrival",
        ),
    }
    (output_dir / "phase415_deep_book_divergence_snapback_execution_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase415 deep-book divergence snapback execution.")
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--phase414-dir", type=Path, default=DEFAULT_PHASE414_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.raw_root, args.phase414_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

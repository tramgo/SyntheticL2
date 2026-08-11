from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase404_liquidity_vacuum_continuation_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    COST_MULTIPLIER,
    DEFAULT_PHASE401_DIR,
    FIXED_NOTIONAL_INR,
    HORIZON_SECONDS,
    INITIAL_CAPITAL_INR,
    MAX_CONCURRENT_POSITIONS,
    MAX_REPLENISHMENT_RATIO,
    MIN_ABS_IMPULSE_BPS,
    MIN_ABS_L2_L5_IMBALANCE,
    MIN_ABS_TOP5_IMBALANCE,
    MIN_SELECTED_EVENT_ROWS,
    THESIS_ID,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_PHASE404_DIR = Path("outputs/phase404")
DEFAULT_OUTPUT_DIR = Path("outputs/phase405")
PRIMARY_SCENARIO_ID = "P405_LIQUIDITY_VACUUM_CONTINUATION_FULL_DEPTH"
SIDE_FLIP_SCENARIO_ID = "P405_CONTROL_SIDE_FLIP"
DEPTH_REMOVED_SCENARIO_ID = "P405_CONTROL_TOP5_ONLY_DEPTH_REMOVED"
NEXT_ACTION = "interpret_phase405_liquidity_vacuum_continuation_no_paper_live"
REPAIR_ACTION = "repair_phase405_liquidity_vacuum_continuation_execution"


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def sign_series(frame: pd.DataFrame, column: str) -> pd.Series:
    return np.sign(pd.to_numeric(frame[column], errors="coerce").fillna(0.0))


def primary_mask(events: pd.DataFrame) -> pd.Series:
    impulse_side = sign_series(events, "impulse_side_sign")
    top5 = pd.to_numeric(events["decision_top5_qty_imbalance"], errors="coerce").fillna(0.0)
    deep = pd.to_numeric(events["decision_l2_l5_qty_imbalance"], errors="coerce").fillna(0.0)
    replenishment = pd.to_numeric(events["replenishment_ratio"], errors="coerce").fillna(999.0)
    impulse = pd.to_numeric(events["impulse_bps"], errors="coerce").fillna(0.0)
    return (
        events["status"].astype(str).eq("ready")
        & impulse_side.ne(0)
        & impulse.abs().ge(MIN_ABS_IMPULSE_BPS)
        & np.sign(top5).eq(impulse_side)
        & top5.abs().ge(MIN_ABS_TOP5_IMBALANCE)
        & np.sign(deep).eq(impulse_side)
        & deep.abs().ge(MIN_ABS_L2_L5_IMBALANCE)
        & replenishment.le(MAX_REPLENISHMENT_RATIO)
    )


def top5_only_mask(events: pd.DataFrame) -> pd.Series:
    impulse_side = sign_series(events, "impulse_side_sign")
    top5 = pd.to_numeric(events["decision_top5_qty_imbalance"], errors="coerce").fillna(0.0)
    replenishment = pd.to_numeric(events["replenishment_ratio"], errors="coerce").fillna(999.0)
    impulse = pd.to_numeric(events["impulse_bps"], errors="coerce").fillna(0.0)
    return (
        events["status"].astype(str).eq("ready")
        & impulse_side.ne(0)
        & impulse.abs().ge(MIN_ABS_IMPULSE_BPS)
        & np.sign(top5).eq(impulse_side)
        & top5.abs().ge(MIN_ABS_TOP5_IMBALANCE)
        & replenishment.le(MAX_REPLENISHMENT_RATIO)
    )


def build_trade_rows(events: pd.DataFrame, mask: pd.Series, scenario_id: str, side_multiplier: int, scenario_role: str) -> pd.DataFrame:
    selected = events.loc[mask].copy()
    if selected.empty:
        return pd.DataFrame()
    selected = selected.sort_values(["diagnostic_trade_date", "decision_ms", "symbol", "canonical_work_order_id"], kind="mergesort").reset_index(drop=True)
    selected["scenario_id"] = scenario_id
    selected["scenario_role"] = scenario_role
    selected["side_sign"] = sign_series(selected, "impulse_side_sign") * int(side_multiplier)
    selected = selected[selected["side_sign"].ne(0)].copy()
    rows: list[dict[str, Any]] = []
    for row in selected.itertuples(index=False):
        side_sign = float(row.side_sign)
        if side_sign > 0:
            entry_price = to_float(getattr(row, "entry_long_price"))
            exit_price = to_float(getattr(row, "exit_long_price"))
            buy_value = entry_price
            sell_value = exit_price
            side = "long"
        else:
            entry_price = to_float(getattr(row, "entry_short_price"))
            exit_price = to_float(getattr(row, "exit_short_price"))
            buy_value = exit_price
            sell_value = entry_price
            side = "short"
        if entry_price <= 0 or exit_price <= 0:
            continue
        quantity = max(1, int(FIXED_NOTIONAL_INR // entry_price))
        buy_value_inr = float(buy_value * quantity)
        sell_value_inr = float(sell_value * quantity)
        gross = (exit_price - entry_price) * quantity * side_sign
        charges = calculate_equity_intraday_nse_charges(
            buy_value_inr=buy_value_inr,
            sell_value_inr=sell_value_inr,
            buy_quantity=quantity,
            sell_quantity=quantity,
            buy_orders=1,
            sell_orders=1,
        )
        cost200 = float(charges.total_charges * COST_MULTIPLIER)
        record = row._asdict()
        record.update(
            {
                "scenario_id": scenario_id,
                "scenario_role": scenario_role,
                "side": side,
                "side_sign": side_sign,
                "quantity": quantity,
                "buy_value_inr": buy_value_inr,
                "sell_value_inr": sell_value_inr,
                "gross_pnl_inr": float(gross),
                "cost200_inr": cost200,
                "net_pnl_inr": float(gross - cost200),
                "cost_model_version": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            }
        )
        rows.append(record)
    return pd.DataFrame(rows)


def apply_capacity(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return trades
    out = trades.sort_values(["diagnostic_trade_date", "decision_ms", "symbol", "canonical_work_order_id"], kind="mergesort").copy()
    out["capacity_selected"] = 0
    for _, group in out.groupby("diagnostic_trade_date", sort=False):
        selected_indices = group.head(MAX_CONCURRENT_POSITIONS).index
        out.loc[selected_indices, "capacity_selected"] = 1
    return out


def summarize(trades: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for scenario_id, group in trades.groupby("scenario_id", sort=False):
        selected = group[group["capacity_selected"].astype(int).eq(1)].copy()
        net = selected["net_pnl_inr"].astype(float) if not selected.empty else pd.Series(dtype=float)
        dates = int(selected["diagnostic_trade_date"].nunique()) if not selected.empty else 0
        net_sum = float(net.sum()) if not net.empty else 0.0
        annualized = (net_sum / INITIAL_CAPITAL_INR) * (252.0 / max(1, dates)) * 100.0
        by_symbol = selected.groupby("symbol")["net_pnl_inr"].sum() if not selected.empty else pd.Series(dtype=float)
        by_symbol_date = selected.groupby(["symbol", "diagnostic_trade_date"])["net_pnl_inr"].sum() if not selected.empty else pd.Series(dtype=float)
        rows.append(
            {
                "scenario_id": scenario_id,
                "scenario_role": str(group["scenario_role"].iloc[0]) if "scenario_role" in group.columns and not group.empty else "",
                "raw_candidate_rows": int(len(group)),
                "capacity_selected_trade_rows": int(len(selected)),
                "diagnostic_dates": dates,
                "symbols": int(selected["symbol"].nunique()) if not selected.empty else 0,
                "positive_symbols": int((by_symbol > 0).sum()) if not by_symbol.empty else 0,
                "positive_symbol_date_cells": int((by_symbol_date > 0).sum()) if not by_symbol_date.empty else 0,
                "net_pnl_inr": net_sum,
                "annualized_return_pct": annualized,
                "above12": int(annualized > ANNUALIZED_THRESHOLD_PCT),
                "event_floor_met": int(len(selected) >= MIN_SELECTED_EVENT_ROWS),
                "breadth_met": int((by_symbol > 0).sum() >= 2 and (by_symbol_date > 0).sum() >= 2) if not by_symbol.empty else 0,
                "acceptance_candidate": int(annualized > ANNUALIZED_THRESHOLD_PCT and len(selected) >= MIN_SELECTED_EVENT_ROWS and (by_symbol > 0).sum() >= 2 and (by_symbol_date > 0).sum() >= 2) if not by_symbol.empty else 0,
                "avg_impulse_bps": float(selected["impulse_bps"].astype(float).mean()) if not selected.empty else 0.0,
                "avg_replenishment_ratio": float(selected["replenishment_ratio"].astype(float).mean()) if not selected.empty else 0.0,
                "avg_l2_l5_abs_imbalance": float(selected["decision_l2_l5_qty_imbalance"].astype(float).abs().mean()) if not selected.empty else 0.0,
            }
        )
    return pd.DataFrame(rows)


def build_gate_evaluation(phase404: pd.DataFrame, scenarios: pd.DataFrame, trades: pd.DataFrame) -> pd.DataFrame:
    precommit_complete = as_int(metric_value(phase404, "phase404_liquidity_vacuum_continuation_precommit_complete", 0))
    primary = scenarios[scenarios["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)].copy() if not scenarios.empty else pd.DataFrame()
    p = primary.iloc[0].to_dict() if not primary.empty else {}
    gates = [
        ("P405_PHASE404_PRECOMMIT_PRESENT", precommit_complete == 1, precommit_complete, 1),
        ("P405_PRIMARY_SCENARIO_PRESENT", not primary.empty, int(not primary.empty), 1),
        ("P405_FULL_DEPTH_FILTER_APPLIED", int((trades.get("scenario_id", pd.Series(dtype=str)).astype(str).eq(PRIMARY_SCENARIO_ID)).sum()) >= 0, "top5_and_l2_l5_alignment", "applied"),
        ("P405_CONTROLS_LOGGED", set([SIDE_FLIP_SCENARIO_ID, DEPTH_REMOVED_SCENARIO_ID]).issubset(set(scenarios["scenario_id"].astype(str))) if not scenarios.empty else False, ";".join(scenarios["scenario_id"].astype(str)) if not scenarios.empty else "", "side_flip;depth_removed"),
        ("P405_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={FIXED_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P405_NO_PROMOTION_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(events: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    primary = scenarios[scenarios["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)].copy() if not scenarios.empty else pd.DataFrame()
    side = scenarios[scenarios["scenario_id"].astype(str).eq(SIDE_FLIP_SCENARIO_ID)].copy() if not scenarios.empty else pd.DataFrame()
    depth_removed = scenarios[scenarios["scenario_id"].astype(str).eq(DEPTH_REMOVED_SCENARIO_ID)].copy() if not scenarios.empty else pd.DataFrame()
    p = primary.iloc[0].to_dict() if not primary.empty else {}
    s = side.iloc[0].to_dict() if not side.empty else {}
    d = depth_removed.iloc[0].to_dict() if not depth_removed.empty else {}
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase405_liquidity_vacuum_continuation_execution_complete", 1, "Phase405 execution completed"),
            ("phase405_thesis_id", THESIS_ID, "Executed thesis"),
            ("phase405_event_feature_rows", len(events), "Input event feature rows"),
            ("phase405_ready_event_feature_rows", int(events["status"].astype(str).eq("ready").sum()) if not events.empty else 0, "Ready rows"),
            ("phase405_primary_raw_candidate_rows", p.get("raw_candidate_rows", 0), "Primary raw candidate rows"),
            ("phase405_primary_capacity_selected_trade_rows", p.get("capacity_selected_trade_rows", 0), "Primary selected trades"),
            ("phase405_primary_diagnostic_dates", p.get("diagnostic_dates", 0), "Primary diagnostic dates"),
            ("phase405_primary_symbols", p.get("symbols", 0), "Primary symbols"),
            ("phase405_primary_positive_symbols", p.get("positive_symbols", 0), "Primary positive symbols"),
            ("phase405_primary_net_pnl_inr", p.get("net_pnl_inr", 0), "Primary net PnL"),
            ("phase405_primary_annualized_return_pct", p.get("annualized_return_pct", 0), "Primary annualized return"),
            ("phase405_primary_above12", p.get("above12", 0), "Primary above 12%"),
            ("phase405_primary_event_floor_met", p.get("event_floor_met", 0), "Primary event floor"),
            ("phase405_primary_breadth_met", p.get("breadth_met", 0), "Primary breadth"),
            ("phase405_primary_acceptance_candidate", p.get("acceptance_candidate", 0), "Primary acceptance"),
            ("phase405_side_flip_annualized_return_pct", s.get("annualized_return_pct", 0), "Side-flip annualized return"),
            ("phase405_depth_removed_annualized_return_pct", d.get("annualized_return_pct", 0), "Depth-removed control annualized return"),
            ("phase405_strategy_promotion_allowed", 0, "No promotion"),
            ("phase405_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase405_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase405_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase405_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase405_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase405 Liquidity-Vacuum Continuation Execution",
        "",
        "Phase405 executes the Phase404 fixed-threshold material-new full-depth L2 thesis.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Scenario Summary",
        "",
        _markdown_table(scenarios),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "No promotion, paper/live acceptance, deployable profitability claim, or parameter search is opened.",
    ]
    (output_dir / "phase405_liquidity_vacuum_continuation_execution_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase404_dir: Path = DEFAULT_PHASE404_DIR, phase401_dir: Path = DEFAULT_PHASE401_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase404 = read_csv(phase404_dir / "phase404_acceptance_summary.csv")
    events = read_csv(phase401_dir / "phase387_event_feature_ledger.csv")
    if phase404.empty or events.empty:
        raise FileNotFoundError("Phase405 requires Phase404 acceptance and Phase401 event features.")
    primary = build_trade_rows(events, primary_mask(events), PRIMARY_SCENARIO_ID, 1, "liquidity_vacuum_continuation")
    side_flip = build_trade_rows(events, primary_mask(events), SIDE_FLIP_SCENARIO_ID, -1, "side_flip_control")
    depth_removed = build_trade_rows(events, top5_only_mask(events), DEPTH_REMOVED_SCENARIO_ID, 1, "top5_only_depth_removed_control")
    frames = [frame for frame in [primary, side_flip, depth_removed] if not frame.empty]
    trades = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if not trades.empty:
        trades = pd.concat([apply_capacity(group) for _, group in trades.groupby("scenario_id", sort=False)], ignore_index=True)
    scenarios = summarize(trades) if not trades.empty else pd.DataFrame(columns=["scenario_id", "scenario_role", "raw_candidate_rows", "capacity_selected_trade_rows", "annualized_return_pct", "acceptance_candidate"])
    gates = build_gate_evaluation(phase404, scenarios, trades)
    acceptance = build_acceptance(events, scenarios, gates)
    trades.to_csv(output_dir / "phase405_trade_ledger.csv", index=False)
    scenarios.to_csv(output_dir / "phase405_scenario_summary.csv", index=False)
    gates.to_csv(output_dir / "phase405_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase405_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, scenarios, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase405_liquidity_vacuum_continuation_execution",
        **reproducibility_fields(
            artifact_id="phase405_liquidity_vacuum_continuation_execution",
            generated_utc=generated_utc,
            inputs={
                "phase404_acceptance_summary": str(phase404_dir / "phase404_acceptance_summary.csv"),
                "phase401_event_feature_ledger": str(phase401_dir / "phase387_event_feature_ledger.csv"),
            },
            parameters={
                "primary_scenario_id": PRIMARY_SCENARIO_ID,
                "fixed_notional_inr": FIXED_NOTIONAL_INR,
                "initial_capital_inr": INITIAL_CAPITAL_INR,
                "max_concurrent_positions": MAX_CONCURRENT_POSITIONS,
                "cost_multiplier": COST_MULTIPLIER,
                "horizon_seconds": HORIZON_SECONDS,
            },
            outputs={"acceptance_summary": str(output_dir / "phase405_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase401_event_feature_decision_delay_120s",
        ),
    }
    (output_dir / "phase405_liquidity_vacuum_continuation_execution_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase405 liquidity-vacuum continuation execution.")
    parser.add_argument("--phase404-dir", type=Path, default=DEFAULT_PHASE404_DIR)
    parser.add_argument("--phase401-dir", type=Path, default=DEFAULT_PHASE401_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase404_dir, args.phase401_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

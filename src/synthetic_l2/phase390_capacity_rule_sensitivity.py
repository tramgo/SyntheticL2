from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION

DEFAULT_PHASE389_DIR = Path("outputs/phase389")
DEFAULT_PHASE387_DIR = Path("outputs/phase387")
DEFAULT_OUTPUT_DIR = Path("outputs/phase390")
INITIAL_CAPITAL_INR = 250_000.0
FIXED_NOTIONAL_INR = 100_000.0
TRADING_DAYS_PER_YEAR = 252.0
EVENT_FLOOR = 30
ANNUALIZED_THRESHOLD_PCT = 12.0


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return rows.iloc[0] if not rows.empty else default


def parse_ladder(text: str) -> list[int]:
    return [int(x) for x in str(text).replace(",", ";").split(";") if x.strip()]


def apply_capacity(trades: pd.DataFrame, capacity: int) -> pd.DataFrame:
    out = trades.sort_values(["decision_ms", "canonical_work_order_id"]).copy()
    selected: set[str] = set()
    active_exits: list[int] = []
    for row in out.itertuples(index=False):
        active_exits = [x for x in active_exits if x > int(float(row.decision_ms))]
        if len(active_exits) < capacity:
            selected.add(str(row.canonical_work_order_id))
            active_exits.append(int(float(row.exit_ms)))
    out["sensitivity_capacity"] = capacity
    out["sensitivity_capacity_selected"] = [int(str(r.canonical_work_order_id) in selected) for r in out.itertuples(index=False)]
    return out


def summarize_capacity(trades: pd.DataFrame, capacity: int) -> dict[str, Any]:
    cap = trades[trades["sensitivity_capacity_selected"].astype(int).eq(1)].copy()
    days = int(cap["diagnostic_trade_date"].nunique()) if not cap.empty else 0
    net = float(pd.to_numeric(cap["net_pnl_inr"], errors="coerce").fillna(0.0).sum()) if not cap.empty else 0.0
    capital_base = max(INITIAL_CAPITAL_INR, capacity * FIXED_NOTIONAL_INR)
    annualized = (net / capital_base) * (TRADING_DAYS_PER_YEAR / max(1, days)) * 100.0
    by_symbol = cap.groupby("symbol")["net_pnl_inr"].sum() if not cap.empty else pd.Series(dtype=float)
    by_symbol_date = cap.groupby(["symbol", "diagnostic_trade_date"])["net_pnl_inr"].sum() if not cap.empty else pd.Series(dtype=float)
    return {
        "capacity": capacity,
        "capital_base_inr": capital_base,
        "scheduled_event_rows": int(len(trades)),
        "capacity_selected_trade_rows": int(len(cap)),
        "diagnostic_trade_dates": days,
        "symbols": int(cap["symbol"].nunique()) if not cap.empty else 0,
        "positive_symbols": int((by_symbol > 0).sum()) if not cap.empty else 0,
        "positive_symbol_date_cells": int((by_symbol_date > 0).sum()) if not cap.empty else 0,
        "net_pnl_inr": net,
        "annualized_return_pct_capital_adjusted": annualized,
        "above12": int(annualized > ANNUALIZED_THRESHOLD_PCT),
        "event_floor_met": int(len(cap) >= EVENT_FLOOR),
        "breadth_met": int((by_symbol > 0).sum() >= 2 and (by_symbol_date > 0).sum() >= 2),
        "sensitivity_acceptance_shape": int(annualized > ANNUALIZED_THRESHOLD_PCT and len(cap) >= EVENT_FLOOR and (by_symbol > 0).sum() >= 2 and (by_symbol_date > 0).sum() >= 2),
        "promotion_allowed": 0,
    }


def write_outputs(phase389_dir: Path, phase387_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    precommit = read_csv(phase389_dir / "phase389_acceptance_summary.csv")
    contract = read_csv(phase389_dir / "phase389_capacity_sensitivity_contract.csv")
    trades = read_csv(phase387_dir / "phase387_trade_ledger.csv")
    if precommit.empty or contract.empty or trades.empty:
        raise FileNotFoundError("Phase390 requires Phase389 precommit and Phase387 trade ledger")
    ladder = parse_ladder(str(contract["capacity_ladder"].iloc[0]))
    primary_id = str(contract["frozen_primary_scenario_id"].iloc[0])
    primary_raw = trades[trades["scenario_id"].astype(str).eq(primary_id)].copy()
    side_raw = trades[~trades["scenario_id"].astype(str).eq(primary_id)].copy()
    selected_frames = []
    summary_rows = []
    for capacity in ladder:
        primary_cap = apply_capacity(primary_raw, capacity)
        side_cap = apply_capacity(side_raw, capacity) if not side_raw.empty else pd.DataFrame()
        selected_frames.append(primary_cap)
        if not side_cap.empty:
            selected_frames.append(side_cap)
        row = summarize_capacity(primary_cap, capacity)
        row["scenario_id"] = primary_id
        row["scenario_role"] = "impulse_reversal_control"
        if not side_cap.empty:
            side = summarize_capacity(side_cap, capacity)
            row["side_flip_annualized_return_pct_capital_adjusted"] = side["annualized_return_pct_capital_adjusted"]
            row["side_flip_selected_trade_rows"] = side["capacity_selected_trade_rows"]
        summary_rows.append(row)
    sensitivity_trades = pd.concat(selected_frames, ignore_index=True) if selected_frames else pd.DataFrame()
    scenario_summary = pd.DataFrame(summary_rows)
    best = scenario_summary.sort_values(["sensitivity_acceptance_shape", "annualized_return_pct_capital_adjusted"], ascending=[False, False]).iloc[0].to_dict()
    gates = pd.DataFrame([
        ("P390_PHASE389_PRECOMMIT_PRESENT", int(str(metric_value(precommit, "phase389_capacity_sensitivity_precommit_complete")) == "1"), "Phase389 complete"),
        ("P390_LADDER_EXECUTED", int(set(ladder).issubset(set(scenario_summary["capacity"].astype(int)))), f"ladder={ladder}"),
        ("P390_CAPITAL_ADJUSTED_RETURNS", 1, "capital_base=max(250k, capacity*100k)"),
        ("P390_ALPHA_COST_DEPTH_UNCHANGED", 1, "reused Phase387 raw trades"),
        ("P390_NO_PROMOTION_PAPER_LIVE", 1, "sensitivity_only"),
    ], columns=["gate_id", "passed", "evidence"])
    summary = pd.DataFrame([
        ("phase390_capacity_rule_sensitivity_complete", int(gates["passed"].astype(int).all()), "Phase390 complete"),
        ("phase390_capacity_ladder", ";".join(map(str, ladder)), "Capacities tested"),
        ("phase390_best_capacity", best.get("capacity", 0), "Best sensitivity capacity"),
        ("phase390_best_selected_trade_rows", best.get("capacity_selected_trade_rows", 0), "Best selected trades"),
        ("phase390_best_annualized_return_pct_capital_adjusted", best.get("annualized_return_pct_capital_adjusted", 0.0), "Best capital-adjusted annualized return"),
        ("phase390_best_sensitivity_acceptance_shape", best.get("sensitivity_acceptance_shape", 0), "Would pass shape gates as sensitivity"),
        ("phase390_promotion_allowed", 0, "No promotion from sensitivity"),
        ("phase390_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase390_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase390_next_best_action", "interpret_phase390_capacity_sensitivity_no_paper_live", "Recommended next action"),
    ], columns=["metric", "value", "description"])
    outputs = {
        "summary": output_dir / "phase390_acceptance_summary.csv",
        "scenarios": output_dir / "phase390_capacity_scenario_summary.csv",
        "trades": output_dir / "phase390_capacity_trade_ledger.csv",
        "gates": output_dir / "phase390_gate_evaluation.csv",
        "report": output_dir / "phase390_capacity_rule_sensitivity_report.md",
        "manifest": output_dir / "phase390_capacity_rule_sensitivity_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    scenario_summary.to_csv(outputs["scenarios"], index=False)
    sensitivity_trades.to_csv(outputs["trades"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text("\n".join(["# Phase390 Capacity Rule Sensitivity", "", f"Generated: {generated_utc}", "", _markdown_table(summary), "", _markdown_table(scenario_summary), "", _markdown_table(gates), ""]), encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({"phase": 390, "generated_at_utc": generated_utc, "outputs": {k: str(v) for k, v in outputs.items()}, "reproducibility": reproducibility_fields(artifact_id="phase390_capacity_rule_sensitivity", generated_utc=generated_utc, inputs={"phase387_trades": str(phase387_dir / "phase387_trade_ledger.csv"), "phase389_contract": str(phase389_dir / "phase389_capacity_sensitivity_contract.csv")}, parameters={"capacity_ladder": ladder, "promotion_allowed": False}, outputs={k: str(v) for k, v in outputs.items()}, cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION)}, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase389-dir", type=Path, default=DEFAULT_PHASE389_DIR)
    parser.add_argument("--phase387-dir", type=Path, default=DEFAULT_PHASE387_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    print(json.dumps({k: str(v) for k, v in write_outputs(args.phase389_dir, args.phase387_dir, args.output_dir).items()}, indent=2))

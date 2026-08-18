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
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase440_external_catalyst_full_depth_precommit import (
    ANNUALIZED_THRESHOLD_PCT,
    COST_MULTIPLIER,
    INITIAL_CAPITAL_INR,
    MIN_COMPLETED_ROUND_TRIPS,
    MIN_POSITIVE_DATE_FRACTION,
    MIN_SYMBOLS,
    MIN_TRADE_DATES,
    NEXT_ACTION as PHASE440_NEXT_ACTION,
    ORDER_NOTIONAL_INR,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_PHASE440_DIR = Path("outputs/phase440")
DEFAULT_PHASE387_DIR = Path("outputs/phase387")
DEFAULT_OUTPUT_DIR = Path("outputs/phase441")

THESIS_ID = "P441_EXTERNAL_CATALYST_FULL_DEPTH_CONFIRMATION_EXECUTION"
NEXT_ACTION = "interpret_phase441_external_catalyst_full_depth_confirmation_no_paper_live"


def fixed_quantity(price: float) -> int:
    return max(1, int(math.floor(ORDER_NOTIONAL_INR / max(float(price), 0.01))))


def score_side(row: pd.Series, side_sign: int) -> dict[str, float]:
    if side_sign > 0:
        entry = float(row["entry_long_price"])
        exit_price = float(row["exit_long_price"])
        buy = entry
        sell = exit_price
        gross = (sell - buy) * fixed_quantity(entry)
    else:
        entry = float(row["entry_short_price"])
        exit_price = float(row["exit_short_price"])
        sell = entry
        buy = exit_price
        gross = (sell - buy) * fixed_quantity(entry)
    qty = fixed_quantity(entry)
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=buy * qty,
        sell_value_inr=sell * qty,
        buy_quantity=qty,
        sell_quantity=qty,
        buy_orders=1,
        sell_orders=1,
    )
    cost100 = float(charges.total_charges)
    cost200 = cost100 * COST_MULTIPLIER
    return {
        "side": "long" if side_sign > 0 else "short",
        "side_sign": int(side_sign),
        "entry_price": entry,
        "exit_price": exit_price,
        "quantity": qty,
        "gross_pnl_inr": float(gross),
        "cost200_inr": float(cost200),
        "net_pnl_inr": float(gross - cost200),
    }


def confirmation_mask(events: pd.DataFrame, mode: str, *, l1_only: bool = False) -> pd.Series:
    impulse_side = events["impulse_side_sign"].astype(float).replace(0, np.nan).fillna(1.0)
    if l1_only:
        imb = events["decision_top5_qty_imbalance"].astype(float)
    else:
        imb = events["decision_l2_l5_qty_imbalance"].astype(float)
    repl = events["replenishment_ratio"].astype(float)
    exhaustion = (-impulse_side * imb).ge(0.20)
    if mode == "exhaustion":
        return exhaustion
    return exhaustion & repl.ge(0.0)


def evaluate(events: pd.DataFrame, grid: pd.DataFrame, panel: str, *, side_flip: bool = False, l1_only: bool = False, time_shift: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    trades: list[dict[str, Any]] = []
    ready = events[events["status"].astype(str).eq("ready")].copy()
    if time_shift and not ready.empty:
        ready["impulse_side_sign"] = ready["impulse_side_sign"].sample(frac=1.0, random_state=441).to_numpy()
    for scenario in grid.itertuples(index=False):
        row = pd.Series(scenario._asdict())
        mask = confirmation_mask(ready, str(row["depth_confirmation"]), l1_only=l1_only)
        candidates = ready[mask].copy()
        if candidates.empty:
            continue
        candidates["rank_score"] = candidates["impulse_bps"].abs() * (1.0 + candidates["decision_l2_l5_qty_imbalance"].abs())
        selected = (
            candidates.sort_values(["diagnostic_trade_date", "rank_score"], ascending=[True, False])
            .groupby("diagnostic_trade_date", sort=False)
            .head(int(row["capacity_events_per_date"]))
        )
        for _, ev in selected.iterrows():
            side = -1 * int(float(ev["impulse_side_sign"]) or 1)
            if side_flip:
                side = -side
            scored = score_side(ev, side)
            trades.append(
                {
                    "panel": panel,
                    "scenario_id": str(row["scenario_id"]),
                    "family_id": str(row["family_id"]),
                    "canonical_work_order_id": ev["canonical_work_order_id"],
                    "diagnostic_trade_date": ev["diagnostic_trade_date"],
                    "symbol": ev["symbol"],
                    "description": ev.get("description", ""),
                    "depth_confirmation": row["depth_confirmation"],
                    "capacity_events_per_date": int(row["capacity_events_per_date"]),
                    "precommitted_horizon_ticks": int(row["horizon_ticks"]),
                    "source_horizon_seconds": float(ev.get("horizon_seconds", 0.0)),
                    "impulse_bps": float(ev["impulse_bps"]),
                    "decision_l2_l5_qty_imbalance": float(ev["decision_l2_l5_qty_imbalance"]),
                    "decision_top5_qty_imbalance": float(ev["decision_top5_qty_imbalance"]),
                    "replenishment_ratio": float(ev["replenishment_ratio"]),
                    **scored,
                }
            )
    ledger = pd.DataFrame(trades)
    return ledger, summarize(ledger, grid, panel)


def summarize(ledger: pd.DataFrame, grid: pd.DataFrame, panel: str) -> pd.DataFrame:
    rows = []
    for scenario in grid.itertuples(index=False):
        sid = str(scenario.scenario_id)
        subset = ledger[ledger["scenario_id"].astype(str).eq(sid)] if not ledger.empty else pd.DataFrame()
        if subset.empty:
            rows.append({"panel": panel, "scenario_id": sid, "family_id": scenario.family_id, "completed_round_trips": 0, "trade_dates": 0, "symbols": 0, "positive_date_fraction": 0.0, "gross_pnl_inr": 0.0, "cost200_inr": 0.0, "net_pnl_inr": 0.0, "annualized_return_pct": 0.0, "acceptance_survivor": 0})
            continue
        date_pnl = subset.groupby("diagnostic_trade_date")["net_pnl_inr"].sum()
        dates = int(subset["diagnostic_trade_date"].nunique())
        trips = int(len(subset))
        symbols = int(subset["symbol"].nunique())
        net = float(subset["net_pnl_inr"].sum())
        ann = (net / INITIAL_CAPITAL_INR) * (252.0 / max(1, dates)) * 100.0
        pos_frac = float((date_pnl > 0).mean()) if len(date_pnl) else 0.0
        rows.append(
            {
                "panel": panel,
                "scenario_id": sid,
                "family_id": scenario.family_id,
                "completed_round_trips": trips,
                "trade_dates": dates,
                "symbols": symbols,
                "positive_date_fraction": pos_frac,
                "gross_pnl_inr": float(subset["gross_pnl_inr"].sum()),
                "cost200_inr": float(subset["cost200_inr"].sum()),
                "net_pnl_inr": net,
                "annualized_return_pct": float(ann),
                "acceptance_survivor": int(trips >= MIN_COMPLETED_ROUND_TRIPS and dates >= MIN_TRADE_DATES and symbols >= MIN_SYMBOLS and pos_frac >= MIN_POSITIVE_DATE_FRACTION and ann >= ANNUALIZED_THRESHOLD_PCT),
            }
        )
    return pd.DataFrame(rows).sort_values("annualized_return_pct", ascending=False).reset_index(drop=True)


def best(summary: pd.DataFrame) -> pd.Series:
    active = summary[pd.to_numeric(summary["completed_round_trips"], errors="coerce").fillna(0).gt(0)]
    return active.sort_values("annualized_return_pct", ascending=False).iloc[0] if not active.empty else summary.iloc[0]


def build_gates(summary: pd.DataFrame, l1_summary: pd.DataFrame, side_summary: pd.DataFrame, shift_summary: pd.DataFrame, source_events: pd.DataFrame) -> pd.DataFrame:
    b = best(summary)
    sid = str(b["scenario_id"])
    l1 = l1_summary[l1_summary["scenario_id"].astype(str).eq(sid)].iloc[0]
    side = side_summary[side_summary["scenario_id"].astype(str).eq(sid)].iloc[0]
    shift = shift_summary[shift_summary["scenario_id"].astype(str).eq(sid)].iloc[0]
    ann = float(b["annualized_return_pct"])
    gates = [
        ("P441_PHASE440_PRECOMMIT_USED", True, PHASE440_NEXT_ACTION, "phase440_next_action"),
        ("P441_SOURCE_EVENT_FLOOR_AVAILABLE", len(source_events) >= MIN_COMPLETED_ROUND_TRIPS, len(source_events), f">={MIN_COMPLETED_ROUND_TRIPS}"),
        ("P441_FULL_DEPTH_CONFIRMATION_USED", True, sid, "l2_l5_confirmation"),
        ("P441_HORIZON_RECOMPUTE_LIMITATION_RECORDED", True, "phase387_feature_ledger_fixed_horizon_seconds", "recorded"),
        ("P441_L1_ONLY_CONTROL", ann - float(l1["annualized_return_pct"]) >= 5.0, ann - float(l1["annualized_return_pct"]), ">=5 pct pts"),
        ("P441_SIDE_FLIP_CONTROL_NOT_DOMINANT", ann >= float(side["annualized_return_pct"]), side["annualized_return_pct"], "primary>=side_flip"),
        ("P441_TIME_SHIFT_CONTROL_NOT_DOMINANT", ann >= float(shift["annualized_return_pct"]), shift["annualized_return_pct"], "primary>=time_shift"),
        ("P441_COST200_FIXED_CAPITAL", True, f"cost={COST_MULTIPLIER};capital={INITIAL_CAPITAL_INR};notional={ORDER_NOTIONAL_INR}", "cost200_fixed_capital"),
        ("P441_EVENT_FLOOR", int(b["completed_round_trips"]) >= MIN_COMPLETED_ROUND_TRIPS, b["completed_round_trips"], f">={MIN_COMPLETED_ROUND_TRIPS}"),
        ("P441_DATE_BREADTH", int(b["trade_dates"]) >= MIN_TRADE_DATES, b["trade_dates"], f">={MIN_TRADE_DATES}"),
        ("P441_SYMBOL_BREADTH", int(b["symbols"]) >= MIN_SYMBOLS, b["symbols"], f">={MIN_SYMBOLS}"),
        ("P441_POSITIVE_DATE_FRACTION", float(b["positive_date_fraction"]) >= MIN_POSITIVE_DATE_FRACTION, b["positive_date_fraction"], f">={MIN_POSITIVE_DATE_FRACTION}"),
        ("P441_ANNUALIZED_FLOOR", ann >= ANNUALIZED_THRESHOLD_PCT, ann, f">={ANNUALIZED_THRESHOLD_PCT}"),
        ("P441_BOUNDARIES_CLOSED", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_acceptance(events: pd.DataFrame, summary: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    b = best(summary)
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase441_external_catalyst_full_depth_complete", 1, "Phase441 execution completed"),
            ("phase441_thesis_id", THESIS_ID, "Execution thesis"),
            ("phase441_source_event_rows", len(events), "Phase387 ready event rows available"),
            ("phase441_best_scenario_id", b["scenario_id"], "Best active scenario"),
            ("phase441_best_completed_round_trips", b["completed_round_trips"], "Best round trips"),
            ("phase441_best_trade_dates", b["trade_dates"], "Best dates"),
            ("phase441_best_symbols", b["symbols"], "Best symbols"),
            ("phase441_best_positive_date_fraction", b["positive_date_fraction"], "Best positive-date fraction"),
            ("phase441_best_gross_pnl_inr", b["gross_pnl_inr"], "Best gross P&L"),
            ("phase441_best_cost200_inr", b["cost200_inr"], "Best cost200 charges"),
            ("phase441_best_net_pnl_inr", b["net_pnl_inr"], "Best net P&L"),
            ("phase441_best_annualized_return_pct", b["annualized_return_pct"], "Best annualized return"),
            ("phase441_cost200_acceptance_survivor_rows", int(summary["acceptance_survivor"].astype(int).sum()), "Accepted scenario rows before controls"),
            ("phase441_strategy_promotion_allowed", 0, "No promotion"),
            ("phase441_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase441_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase441_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase441_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase441_next_best_action", NEXT_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, summary: pd.DataFrame, controls: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase441 External Catalyst Full-Depth Confirmation Execution",
        "",
        "Phase441 executes the Phase440 external-catalyst plus full-depth confirmation source using local Phase387 event-feature evidence.",
        "",
        "The execution is bounded by the Phase387 feature ledger's fixed event horizon; it does not claim fresh raw-horizon recomputation.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Scenario Summary",
        "",
        _markdown_table(summary),
        "",
        "## Controls For Best Scenario",
        "",
        _markdown_table(controls),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: no strategy promotion, paper/live acceptance or deployable profitability claim is generated by Phase441.",
    ]
    (output_dir / "phase441_external_catalyst_full_depth_confirmation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase440_dir: Path = DEFAULT_PHASE440_DIR, phase387_dir: Path = DEFAULT_PHASE387_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase440 = read_csv(phase440_dir / "phase440_acceptance_summary.csv")
    if str(metric_value(phase440, "phase440_next_best_action", "")) != PHASE440_NEXT_ACTION:
        raise ValueError("Phase441 requires Phase440 execution allowance.")
    grid = read_csv(phase440_dir / "phase440_external_catalyst_scenario_grid.csv")
    events = read_csv(phase387_dir / "phase387_event_feature_ledger.csv")
    ready = events[events["status"].astype(str).eq("ready")].copy()
    ledger, summary = evaluate(ready, grid, "external_catalyst_full_depth")
    l1_ledger, l1_summary = evaluate(ready, grid, "l1_only_ablation", l1_only=True)
    side_ledger, side_summary = evaluate(ready, grid, "side_flip", side_flip=True)
    shift_ledger, shift_summary = evaluate(ready, grid, "time_shifted_catalyst", time_shift=True)
    best_sid = str(best(summary)["scenario_id"])
    controls = pd.DataFrame(
        [
            {"control": "l1_only", **l1_summary[l1_summary["scenario_id"].astype(str).eq(best_sid)].iloc[0].to_dict()},
            {"control": "side_flip", **side_summary[side_summary["scenario_id"].astype(str).eq(best_sid)].iloc[0].to_dict()},
            {"control": "time_shifted_catalyst", **shift_summary[shift_summary["scenario_id"].astype(str).eq(best_sid)].iloc[0].to_dict()},
        ]
    )
    gates = build_gates(summary, l1_summary, side_summary, shift_summary, ready)
    acceptance = build_acceptance(ready, summary, gates)
    summary.to_csv(output_dir / "phase441_scenario_summary.csv", index=False)
    ledger.to_csv(output_dir / "phase441_trade_ledger.csv", index=False)
    controls.to_csv(output_dir / "phase441_best_scenario_controls.csv", index=False)
    gates.to_csv(output_dir / "phase441_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase441_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, summary, controls, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase441_external_catalyst_full_depth_confirmation",
        **reproducibility_fields(
            artifact_id="phase441_external_catalyst_full_depth_confirmation",
            generated_utc=generated_utc,
            inputs={"phase440_grid": str(phase440_dir / "phase440_external_catalyst_scenario_grid.csv"), "phase387_events": str(phase387_dir / "phase387_event_feature_ledger.csv")},
            parameters={"thesis_id": THESIS_ID, "source_horizon": "phase387_feature_ledger_fixed_horizon_seconds"},
            outputs={"acceptance_summary": str(output_dir / "phase441_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase387_event_feature_fixed_horizon",
        ),
    }
    (output_dir / "phase441_external_catalyst_full_depth_confirmation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase441 external catalyst full-depth confirmation execution.")
    parser.add_argument("--phase440-dir", type=Path, default=DEFAULT_PHASE440_DIR)
    parser.add_argument("--phase387-dir", type=Path, default=DEFAULT_PHASE387_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase440_dir, args.phase387_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

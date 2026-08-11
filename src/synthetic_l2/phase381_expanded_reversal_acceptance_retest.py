from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase363_liquidity_replenished_catalyst_impulse_diagnostic import (
    ANNUALIZED_THRESHOLD_PCT,
    DEFAULT_EXISTING_ROOT,
    DEFAULT_UNSEEN_ROOT,
    ROBUST_EVENT_FLOOR,
    apply_capacity,
    build_event_features,
    read_csv,
    scenario_trades,
    summarize,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE380_DIR = Path("outputs/phase380")
DEFAULT_PHASE362_DIR = Path("outputs/phase362")
DEFAULT_OUTPUT_DIR = Path("outputs/phase381")
PRIMARY_SCENARIO_ID = "P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL"
PRIMARY_GRID_ID = "P362_D120_I2p5_D0p25_R0p0"
SIDE_FLIP_SCENARIO_ID = "P362_D120_I2p5_D0p25_R0p0_CONTINUATION"


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return rows.iloc[0] if not rows.empty else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def root_has_date(root: Path, trade_date: str) -> bool:
    return (root / f"trade_date={trade_date}" / "exchange=NSE").exists()


def load_phase380_work(phase380_dir: Path, existing_root: Path, unseen_root: Path) -> pd.DataFrame:
    work = read_csv(phase380_dir / "phase380_phase360_execution_work_order.csv")
    if work.empty:
        raise FileNotFoundError("Phase381 requires Phase380 adapted work order")
    out = work.copy()
    panels: list[str] = []
    roots: list[str] = []
    for trade_date in out["diagnostic_trade_date"].astype(str):
        if root_has_date(unseen_root, trade_date):
            panels.append("unseen_phase359")
            roots.append(str(unseen_root))
        elif root_has_date(existing_root, trade_date):
            panels.append("existing_phase341")
            roots.append(str(existing_root))
        else:
            panels.append("missing_local_l2")
            roots.append("")
    out["canonical_work_order_id"] = out["phase360_work_order_id"].astype(str)
    out["panel"] = panels
    out["resolved_real_root"] = roots
    return out[
        [
            "canonical_work_order_id",
            "panel",
            "symbol",
            "announcement_time_ist",
            "market_session",
            "diagnostic_trade_date",
            "diagnostic_start_rule",
            "description",
            "no_lookahead_rule_applied",
            "resolved_real_root",
        ]
    ].copy()


def write_outputs(phase380_dir: Path, phase362_dir: Path, existing_root: Path, unseen_root: Path, output_dir: Path, max_work_rows: int) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase380_summary = read_csv(phase380_dir / "phase380_acceptance_summary.csv")
    phase380_contract = read_csv(phase380_dir / "phase380_retest_contract.csv")
    grid = read_csv(phase362_dir / "phase362_scenario_grid.csv")
    if phase380_summary.empty or phase380_contract.empty or grid.empty:
        raise FileNotFoundError("Phase381 requires Phase380 summary/contract and Phase362 grid")
    work = load_phase380_work(phase380_dir, existing_root, unseen_root)
    missing = work[work["panel"].eq("missing_local_l2")].copy()
    if max_work_rows > 0:
        work = work.head(max_work_rows).copy()
    primary_grid = grid[grid["scenario_grid_id"].astype(str).eq(PRIMARY_GRID_ID)].copy()
    if primary_grid.empty:
        raise FileNotFoundError(f"Phase381 requires frozen grid row {PRIMARY_GRID_ID}")
    primary_grid_row = primary_grid.iloc[0]
    delays = [int(primary_grid_row["decision_delay_seconds"])]
    horizon_seconds = int(primary_grid_row["horizon_seconds"])
    events = build_event_features(work.drop(columns=["resolved_real_root"], errors="ignore"), existing_root, unseen_root, delays, horizon_seconds)
    primary_trades = scenario_trades(events, primary_grid_row, control=True)
    side_flip_trades = scenario_trades(events, primary_grid_row, control=False)
    trade_frames = [frame for frame in [primary_trades, side_flip_trades] if not frame.empty]
    trades = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    if not trades.empty:
        trades = pd.concat([apply_capacity(frame) for _, frame in trades.groupby("scenario_id")], ignore_index=True)
    scenarios = summarize(trades)
    primary = scenarios[scenarios["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)].copy() if not scenarios.empty else pd.DataFrame()
    side_flip = scenarios[scenarios["scenario_id"].astype(str).eq(SIDE_FLIP_SCENARIO_ID)].copy() if not scenarios.empty else pd.DataFrame()
    primary_row = primary.iloc[0].to_dict() if not primary.empty else {}
    side_row = side_flip.iloc[0].to_dict() if not side_flip.empty else {}
    primary_acceptance = int(primary_row.get("acceptance_candidate", 0) or 0)
    primary_ann = float(primary_row.get("annualized_return_pct", 0.0) or 0.0)
    primary_trades_n = int(primary_row.get("capacity_selected_trade_rows", 0) or 0)
    primary_breadth = int(primary_row.get("breadth_met", 0) or 0)
    side_ann = float(side_row.get("annualized_return_pct", 0.0) or 0.0)
    ready_events = int(events["status"].eq("ready").sum()) if not events.empty else 0

    interpretation = pd.DataFrame(
        [
            {
                "interpretation_id": "expanded_retest_executed",
                "value": int(len(events) > 0 and len(scenarios) > 0),
                "evidence": f"event_rows={len(events)}; scenario_rows={len(scenarios)}",
                "decision": "Frozen expanded real-L2 retest executed.",
            },
            {
                "interpretation_id": "primary_acceptance_candidate",
                "value": primary_acceptance,
                "evidence": f"ann={primary_ann}; selected_trades={primary_trades_n}; breadth={primary_breadth}",
                "decision": "Primary passes acceptance gates only if annualized return, event floor and breadth all pass.",
            },
            {
                "interpretation_id": "side_flip_control_not_better",
                "value": int(primary_ann > side_ann),
                "evidence": f"primary_ann={primary_ann}; side_flip_ann={side_ann}",
                "decision": "Primary reversal should dominate same-filter continuation control.",
            },
        ]
    )
    gates = pd.DataFrame(
        [
            ("P381_PHASE380_PRECOMMIT_PRESENT", as_int(metric_value(phase380_summary, "phase380_expanded_reversal_acceptance_retest_precommit_complete")), "Phase380 precommit complete"),
            ("P381_NO_MISSING_LOCAL_L2_DATES", int(missing.empty), f"missing_rows={len(missing)}"),
            ("P381_FROZEN_GRID_ONLY", int(len(primary_grid) == 1), PRIMARY_GRID_ID),
            ("P381_EVENT_FEATURES_READY", int(ready_events > 0), f"ready_rows={ready_events}"),
            ("P381_FULL_DEPTH_COST200_RETAINED", int(not trades.empty and trades["cost_model_version"].astype(str).eq(ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION).all()), ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION),
            ("P381_ACCEPTANCE_GATE_EVALUATED", 1, f"ann>{ANNUALIZED_THRESHOLD_PCT}; events>={ROBUST_EVENT_FLOOR}; breadth"),
            ("P381_NO_PARAMETER_SEARCH", 1, "single frozen grid row plus side-flip control"),
            ("P381_NO_PAPER_LIVE_OR_DEPLOYABLE_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    summary = pd.DataFrame(
        [
            ("phase381_expanded_reversal_acceptance_retest_complete", int(gates["passed"].astype(int).all()), "Phase381 complete"),
            ("phase381_work_order_rows", len(work), "Expanded work-order rows replayed"),
            ("phase381_missing_local_l2_rows", len(missing), "Rows whose diagnostic date has no local L2 root"),
            ("phase381_event_feature_rows", len(events), "Event feature rows"),
            ("phase381_ready_event_feature_rows", ready_events, "Ready event feature rows"),
            ("phase381_trade_rows", len(trades), "Trade ledger rows"),
            ("phase381_scenario_rows", len(scenarios), "Scenario rows"),
            ("phase381_primary_scenario_id", PRIMARY_SCENARIO_ID, "Frozen primary scenario"),
            ("phase381_primary_selected_trade_rows", primary_trades_n, "Primary capacity-selected trades"),
            ("phase381_primary_diagnostic_dates", primary_row.get("diagnostic_trade_dates", 0), "Primary diagnostic dates"),
            ("phase381_primary_symbols", primary_row.get("symbols", 0), "Primary symbols"),
            ("phase381_primary_positive_symbols", primary_row.get("positive_symbols", 0), "Primary positive symbols"),
            ("phase381_primary_positive_symbol_date_cells", primary_row.get("positive_symbol_date_cells", 0), "Primary positive symbol-date cells"),
            ("phase381_primary_net_pnl_inr", primary_row.get("net_pnl_inr", 0.0), "Primary net PnL"),
            ("phase381_primary_annualized_return_pct", primary_ann, "Primary annualized return"),
            ("phase381_primary_above12", primary_row.get("above12", 0), "Primary above 12%"),
            ("phase381_primary_event_floor_met", primary_row.get("event_floor_met", 0), "Primary event floor"),
            ("phase381_primary_breadth_met", primary_breadth, "Primary breadth gate"),
            ("phase381_primary_acceptance_candidate", primary_acceptance, "Primary acceptance candidate"),
            ("phase381_side_flip_annualized_return_pct", side_ann, "Side-flip control annualized return"),
            ("phase381_strategy_promotion_allowed", primary_acceptance, "Promotion allowed only if primary acceptance candidate"),
            ("phase381_paper_or_live_acceptance_allowed", 0, "No paper/live action in this phase"),
            ("phase381_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase381_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase381_hard_gate_rows", len(gates), "Hard gates"),
            ("phase381_next_best_action", "interpret_phase381_acceptance_result_no_paper_live", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase381_acceptance_summary.csv",
        "resolved_work": output_dir / "phase381_resolved_work_order.csv",
        "events": output_dir / "phase381_event_feature_ledger.csv",
        "trades": output_dir / "phase381_trade_ledger.csv",
        "scenarios": output_dir / "phase381_scenario_summary.csv",
        "interpretation": output_dir / "phase381_interpretation_ledger.csv",
        "gates": output_dir / "phase381_gate_evaluation.csv",
        "report": output_dir / "phase381_expanded_reversal_acceptance_retest_report.md",
        "manifest": output_dir / "phase381_expanded_reversal_acceptance_retest_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    work.to_csv(outputs["resolved_work"], index=False)
    events.to_csv(outputs["events"], index=False)
    trades.to_csv(outputs["trades"], index=False)
    scenarios.to_csv(outputs["scenarios"], index=False)
    interpretation.to_csv(outputs["interpretation"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join([
        "# Phase381 Expanded Reversal Acceptance Retest",
        "",
        f"Generated: {generated_utc}",
        "",
        "Phase381 executes the Phase380 precommitted expanded real-L2 frozen reversal retest. It uses one frozen grid row plus the registered same-filter continuation side-flip control. It performs no parameter search and opens no paper/live action.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(summary),
        "",
        "## Scenario summary",
        "",
        _markdown_table(scenarios),
        "",
        "## Interpretation",
        "",
        _markdown_table(interpretation),
        "",
        "## Gate evaluation",
        "",
        _markdown_table(gates),
        "",
        "No paper/live acceptance or deployable profitability claim is opened.",
    ])
    outputs["report"].write_text(report + "\n", encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({
        "phase": 381,
        "generated_at_utc": generated_utc,
        "outputs": {k: str(v) for k, v in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase381_expanded_reversal_acceptance_retest",
            generated_utc=generated_utc,
            inputs={"phase380_contract": str(phase380_dir / "phase380_retest_contract.csv"), "phase380_work_order": str(phase380_dir / "phase380_phase360_execution_work_order.csv"), "phase362_grid": str(phase362_dir / "phase362_scenario_grid.csv")},
            parameters={"primary_grid_id": PRIMARY_GRID_ID, "primary_scenario_id": PRIMARY_SCENARIO_ID, "parameter_search_allowed": False, "max_work_rows": max_work_rows},
            outputs={k: str(v) for k, v in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase365_frozen_120_second_decision_delay",
        ),
        "next_action": "interpret_phase381_acceptance_result_no_paper_live",
    }, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase380-dir", type=Path, default=DEFAULT_PHASE380_DIR)
    parser.add_argument("--phase362-dir", type=Path, default=DEFAULT_PHASE362_DIR)
    parser.add_argument("--existing-root", type=Path, default=DEFAULT_EXISTING_ROOT)
    parser.add_argument("--unseen-root", type=Path, default=DEFAULT_UNSEEN_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-work-rows", type=int, default=0)
    args = parser.parse_args()
    outputs = write_outputs(args.phase380_dir, args.phase362_dir, args.existing_root, args.unseen_root, args.output_dir, args.max_work_rows)
    print(json.dumps({k: str(v) for k, v in outputs.items()}, indent=2))

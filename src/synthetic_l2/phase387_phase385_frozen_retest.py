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
from synthetic_l2.phase381_expanded_reversal_acceptance_retest import root_has_date
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION

DEFAULT_PHASE386_DIR = Path("outputs/phase386")
DEFAULT_PHASE362_DIR = Path("outputs/phase362")
DEFAULT_OUTPUT_DIR = Path("outputs/phase387")
PRIMARY_GRID_ID = "P362_D120_I2p5_D0p25_R0p0"
PRIMARY_SCENARIO_ID = "P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL"
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


def load_work(phase386_dir: Path, existing_root: Path, unseen_root: Path) -> pd.DataFrame:
    work = read_csv(phase386_dir / "phase386_phase360_execution_work_order.csv")
    if work.empty:
        raise FileNotFoundError("Phase387 requires Phase386 adapted work order")
    out = work.copy()
    panels, roots = [], []
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
    return out[["canonical_work_order_id", "panel", "symbol", "announcement_time_ist", "market_session", "diagnostic_trade_date", "diagnostic_start_rule", "description", "no_lookahead_rule_applied", "resolved_real_root"]].copy()


def write_outputs(phase386_dir: Path, phase362_dir: Path, existing_root: Path, unseen_root: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase386_summary = read_csv(phase386_dir / "phase386_acceptance_summary.csv")
    grid = read_csv(phase362_dir / "phase362_scenario_grid.csv")
    if phase386_summary.empty or grid.empty:
        raise FileNotFoundError("Phase387 requires Phase386 summary and Phase362 grid")
    work = load_work(phase386_dir, existing_root, unseen_root)
    missing = work[work["panel"].eq("missing_local_l2")].copy()
    grid_row_df = grid[grid["scenario_grid_id"].astype(str).eq(PRIMARY_GRID_ID)].copy()
    if grid_row_df.empty:
        raise FileNotFoundError(f"Missing frozen grid {PRIMARY_GRID_ID}")
    grid_row = grid_row_df.iloc[0]
    events = build_event_features(work.drop(columns=["resolved_real_root"], errors="ignore"), existing_root, unseen_root, [int(grid_row["decision_delay_seconds"])], int(grid_row["horizon_seconds"]))
    primary_trades = scenario_trades(events, grid_row, control=True)
    side_flip_trades = scenario_trades(events, grid_row, control=False)
    frames = [f for f in [primary_trades, side_flip_trades] if not f.empty]
    trades = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if not trades.empty:
        trades = pd.concat([apply_capacity(frame) for _, frame in trades.groupby("scenario_id")], ignore_index=True)
    scenarios = summarize(trades)
    primary = scenarios[scenarios["scenario_id"].astype(str).eq(PRIMARY_SCENARIO_ID)].copy() if not scenarios.empty else pd.DataFrame()
    side = scenarios[scenarios["scenario_id"].astype(str).eq(SIDE_FLIP_SCENARIO_ID)].copy() if not scenarios.empty else pd.DataFrame()
    p = primary.iloc[0].to_dict() if not primary.empty else {}
    s = side.iloc[0].to_dict() if not side.empty else {}
    primary_ann = float(p.get("annualized_return_pct", 0.0) or 0.0)
    side_ann = float(s.get("annualized_return_pct", 0.0) or 0.0)
    selected = int(p.get("capacity_selected_trade_rows", 0) or 0)
    acceptance = int(p.get("acceptance_candidate", 0) or 0)
    ready = int(events["status"].eq("ready").sum()) if not events.empty else 0
    gates = pd.DataFrame(
        [
            ("P387_PHASE386_PRECOMMIT_PRESENT", as_int(metric_value(phase386_summary, "phase386_phase385_retest_precommit_complete")), "Phase386 complete"),
            ("P387_NO_MISSING_LOCAL_L2_DATES", int(missing.empty), f"missing_rows={len(missing)}"),
            ("P387_FROZEN_GRID_ONLY", 1, PRIMARY_GRID_ID),
            ("P387_EVENT_FEATURES_READY", int(ready > 0), f"ready_rows={ready}"),
            ("P387_FULL_DEPTH_COST200_RETAINED", int(not trades.empty and trades["cost_model_version"].astype(str).eq(ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION).all()), ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION),
            ("P387_ACCEPTANCE_GATE_EVALUATED", 1, f"ann>{ANNUALIZED_THRESHOLD_PCT}; events>={ROBUST_EVENT_FLOOR}; breadth"),
            ("P387_NO_PARAMETER_SEARCH", 1, "single frozen grid row plus side-flip control"),
            ("P387_NO_PAPER_LIVE_OR_DEPLOYABLE_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    interpretation = pd.DataFrame([
        {"interpretation_id": "primary_acceptance_candidate", "value": acceptance, "evidence": f"ann={primary_ann}; selected_trades={selected}; event_floor={p.get('event_floor_met', 0)}; breadth={p.get('breadth_met', 0)}", "decision": "Primary is accepted only if profitability, event floor and breadth all pass."},
        {"interpretation_id": "side_flip_control_not_better", "value": int(primary_ann > side_ann), "evidence": f"primary_ann={primary_ann}; side_flip_ann={side_ann}", "decision": "Primary reversal should dominate continuation control."},
    ])
    summary = pd.DataFrame(
        [
            ("phase387_phase385_frozen_retest_complete", int(gates["passed"].astype(int).all()), "Phase387 complete"),
            ("phase387_work_order_rows", len(work), "Expanded work-order rows replayed"),
            ("phase387_missing_local_l2_rows", len(missing), "Rows whose diagnostic date has no local L2 root"),
            ("phase387_event_feature_rows", len(events), "Event feature rows"),
            ("phase387_ready_event_feature_rows", ready, "Ready event feature rows"),
            ("phase387_trade_rows", len(trades), "Trade ledger rows"),
            ("phase387_scenario_rows", len(scenarios), "Scenario rows"),
            ("phase387_primary_scenario_id", PRIMARY_SCENARIO_ID, "Frozen primary scenario"),
            ("phase387_primary_selected_trade_rows", selected, "Primary capacity-selected trades"),
            ("phase387_primary_diagnostic_dates", p.get("diagnostic_trade_dates", 0), "Primary diagnostic dates"),
            ("phase387_primary_symbols", p.get("symbols", 0), "Primary symbols"),
            ("phase387_primary_positive_symbols", p.get("positive_symbols", 0), "Primary positive symbols"),
            ("phase387_primary_positive_symbol_date_cells", p.get("positive_symbol_date_cells", 0), "Primary positive symbol-date cells"),
            ("phase387_primary_net_pnl_inr", p.get("net_pnl_inr", 0.0), "Primary net PnL"),
            ("phase387_primary_annualized_return_pct", primary_ann, "Primary annualized return"),
            ("phase387_primary_above12", p.get("above12", 0), "Primary above 12%"),
            ("phase387_primary_event_floor_met", p.get("event_floor_met", 0), "Primary event floor"),
            ("phase387_primary_breadth_met", p.get("breadth_met", 0), "Primary breadth gate"),
            ("phase387_primary_acceptance_candidate", acceptance, "Primary acceptance candidate"),
            ("phase387_side_flip_annualized_return_pct", side_ann, "Side-flip control annualized return"),
            ("phase387_strategy_promotion_allowed", acceptance, "Promotion allowed only if primary acceptance candidate"),
            ("phase387_paper_or_live_acceptance_allowed", 0, "No paper/live action in this phase"),
            ("phase387_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase387_next_best_action", "interpret_phase387_acceptance_result_no_paper_live", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase387_acceptance_summary.csv",
        "resolved_work": output_dir / "phase387_resolved_work_order.csv",
        "events": output_dir / "phase387_event_feature_ledger.csv",
        "trades": output_dir / "phase387_trade_ledger.csv",
        "scenarios": output_dir / "phase387_scenario_summary.csv",
        "interpretation": output_dir / "phase387_interpretation_ledger.csv",
        "gates": output_dir / "phase387_gate_evaluation.csv",
        "report": output_dir / "phase387_phase385_frozen_retest_report.md",
        "manifest": output_dir / "phase387_phase385_frozen_retest_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    work.to_csv(outputs["resolved_work"], index=False)
    events.to_csv(outputs["events"], index=False)
    trades.to_csv(outputs["trades"], index=False)
    scenarios.to_csv(outputs["scenarios"], index=False)
    interpretation.to_csv(outputs["interpretation"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    outputs["report"].write_text("\n".join(["# Phase387 Phase385 Frozen Retest", "", f"Generated: {generated_utc}", "", _markdown_table(summary), "", _markdown_table(scenarios), ""]) , encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({"phase": 387, "generated_at_utc": generated_utc, "outputs": {k: str(v) for k, v in outputs.items()}, "reproducibility": reproducibility_fields(artifact_id="phase387_phase385_frozen_retest", generated_utc=generated_utc, inputs={"phase386_work_order": str(phase386_dir / "phase386_phase360_execution_work_order.csv")}, parameters={"primary_grid_id": PRIMARY_GRID_ID, "parameter_search_allowed": False}, outputs={k: str(v) for k, v in outputs.items()}, cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, latency_model_version="phase365_frozen_120_second_decision_delay")}, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase386-dir", type=Path, default=DEFAULT_PHASE386_DIR)
    parser.add_argument("--phase362-dir", type=Path, default=DEFAULT_PHASE362_DIR)
    parser.add_argument("--existing-root", type=Path, default=DEFAULT_EXISTING_ROOT)
    parser.add_argument("--unseen-root", type=Path, default=DEFAULT_UNSEEN_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    print(json.dumps({k: str(v) for k, v in write_outputs(args.phase386_dir, args.phase362_dir, args.existing_root, args.unseen_root, args.output_dir).items()}, indent=2))

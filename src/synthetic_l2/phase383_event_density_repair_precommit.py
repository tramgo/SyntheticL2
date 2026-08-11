from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE382_DIR = Path("outputs/phase382")
DEFAULT_PHASE379_DIR = Path("outputs/phase379")
DEFAULT_OUTPUT_DIR = Path("outputs/phase383")
EVENT_FLOOR = 30
PRIMARY_SCENARIO_ID = "P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL"


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


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


def next_weekday(text: str) -> str:
    dt = date.fromisoformat(text) + timedelta(days=1)
    while dt.weekday() >= 5:
        dt += timedelta(days=1)
    return dt.isoformat()


def write_outputs(phase382_dir: Path, phase379_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase382_summary = read_csv(phase382_dir / "phase382_acceptance_summary.csv")
    eligibility = read_csv(phase379_dir / "phase373_no_lookahead_official_catalyst_eligibility.csv")
    if phase382_summary.empty or eligibility.empty:
        raise FileNotFoundError("Phase383 requires Phase382 interpretation and Phase379 refreshed eligibility")

    pending = eligibility[
        eligibility["market_session"].astype(str).eq("post_close")
        & eligibility["diagnostic_trade_date"].fillna("").astype(str).eq("")
    ].copy()
    source_date = sorted(pending["announcement_date"].dropna().astype(str).unique().tolist())[-1] if not pending.empty else ""
    target_date = next_weekday(source_date) if source_date else ""
    selected_gap = as_int(metric_value(phase382_summary, "phase382_event_floor_gap"))
    selected_trades = as_int(metric_value(phase382_summary, "phase382_primary_selected_trade_rows"))
    acceptance_candidate = as_int(metric_value(phase382_summary, "phase382_acceptance_candidate"))

    contract = pd.DataFrame(
        [
            {
                "contract_id": "P383_EVENT_DENSITY_REPAIR_BY_NEXT_REAL_L2_DAY",
                "source_phase": "Phase382",
                "frozen_primary_scenario_id": PRIMARY_SCENARIO_ID,
                "repair_type": "expand_no_lookahead_real_l2_event_pool",
                "target_trade_date": target_date,
                "source_post_close_announcement_date": source_date,
                "pending_post_close_rows": len(pending[pending["announcement_date"].astype(str).eq(source_date)]) if source_date else 0,
                "current_selected_trades": selected_trades,
                "selected_trade_gap_to_floor": selected_gap,
                "parameter_relaxation_allowed": 0,
                "capital_or_capacity_change_allowed": 0,
                "same_run_rescue_allowed": 0,
                "strategy_retest_executed_now": 0,
                "paper_live_or_profit_claim_allowed": 0,
            }
        ]
    )
    gates = pd.DataFrame(
        [
            ("P383_PHASE382_PRESENT", as_int(metric_value(phase382_summary, "phase382_interpret_phase381_retest_complete")), "Phase382 complete"),
            ("P383_ACCEPTANCE_STILL_CLOSED", int(acceptance_candidate == 0), f"acceptance_candidate={acceptance_candidate}"),
            ("P383_EVENT_DENSITY_GAP_PRESENT", int(selected_gap > 0), f"gap={selected_gap}"),
            ("P383_NEXT_NO_LOOKAHEAD_TARGET_SELECTED", int(bool(target_date)), target_date),
            ("P383_PENDING_POST_CLOSE_EVENTS_PRESENT", int(len(pending) > 0), f"pending_rows={len(pending)}"),
            ("P383_NO_PARAMETER_OR_CAPACITY_RESCUE", 1, "expand evidence only"),
            ("P383_NO_RETEST_OR_PAPER_LIVE_NOW", 1, "precommit_only"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    summary = pd.DataFrame(
        [
            ("phase383_event_density_repair_precommit_complete", int(gates["passed"].astype(int).all()), "Phase383 complete"),
            ("phase383_frozen_primary_scenario_id", PRIMARY_SCENARIO_ID, "Frozen primary"),
            ("phase383_current_selected_trades", selected_trades, "Phase382 selected trades"),
            ("phase383_event_floor_required", EVENT_FLOOR, "Required selected trades"),
            ("phase383_selected_trade_gap", selected_gap, "Gap to event floor"),
            ("phase383_pending_post_close_rows", len(pending[pending["announcement_date"].astype(str).eq(source_date)]) if source_date else 0, "Rows unlocked by target"),
            ("phase383_source_post_close_announcement_date", source_date, "Pending announcement date"),
            ("phase383_target_trade_date", target_date, "Next no-lookahead L2 date"),
            ("phase383_parameter_relaxation_allowed", 0, "No parameter rescue"),
            ("phase383_capital_or_capacity_change_allowed", 0, "No capacity rescue"),
            ("phase383_strategy_retest_executed_now", 0, "No retest"),
            ("phase383_strategy_promotion_allowed", 0, "No promotion"),
            ("phase383_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase383_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase383_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed gates"),
            ("phase383_hard_gate_rows", len(gates), "Gates"),
            ("phase383_next_best_action", "download_phase384_target_20260727_then_refresh_and_rerun_frozen_retest_no_search", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase383_acceptance_summary.csv",
        "contract": output_dir / "phase383_event_density_repair_contract.csv",
        "pending": output_dir / "phase383_pending_post_close_events.csv",
        "gates": output_dir / "phase383_gate_evaluation.csv",
        "report": output_dir / "phase383_event_density_repair_precommit_report.md",
        "manifest": output_dir / "phase383_event_density_repair_precommit_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    contract.to_csv(outputs["contract"], index=False)
    pending.to_csv(outputs["pending"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join([
        "# Phase383 Event-Density Repair Precommit",
        "",
        f"Generated: {generated_utc}",
        "",
        "Phase383 precommits the next repair after Phase382: expand the no-lookahead real-L2 event pool by adding the next catalyst day. It explicitly forbids parameter relaxation, capital/capacity rescue, same-run rescue, paper/live action, and profitability claims.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(summary),
        "",
        "## Repair contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate evaluation",
        "",
        _markdown_table(gates),
        "",
        "No retest, promotion, paper/live acceptance, or deployable profitability claim is opened in this precommit.",
    ])
    outputs["report"].write_text(report + "\n", encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({
        "phase": 383,
        "generated_at_utc": generated_utc,
        "outputs": {k: str(v) for k, v in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase383_event_density_repair_precommit",
            generated_utc=generated_utc,
            inputs={"phase382_summary": str(phase382_dir / "phase382_acceptance_summary.csv"), "phase379_eligibility": str(phase379_dir / "phase373_no_lookahead_official_catalyst_eligibility.csv")},
            parameters={"event_floor": EVENT_FLOOR, "target_trade_date": target_date, "parameter_relaxation_allowed": False, "capital_or_capacity_change_allowed": False},
            outputs={k: str(v) for k, v in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": "download_phase384_target_20260727_then_refresh_and_rerun_frozen_retest_no_search",
    }, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase382-dir", type=Path, default=DEFAULT_PHASE382_DIR)
    parser.add_argument("--phase379-dir", type=Path, default=DEFAULT_PHASE379_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase382_dir, args.phase379_dir, args.output_dir)
    print(json.dumps({k: str(v) for k, v in outputs.items()}, indent=2))

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


DEFAULT_PHASE379_DIR = Path("outputs/phase379")
DEFAULT_PHASE365_DIR = Path("outputs/phase365")
DEFAULT_OUTPUT_DIR = Path("outputs/phase380")
EVENT_FLOOR = 30
PRIMARY_SCENARIO_ID = "P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL"
PRIMARY_GRID_ID = "P362_D120_I2p5_D0p25_R0p0"


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


def adapt_work_order(work: pd.DataFrame) -> pd.DataFrame:
    out = work.copy()
    if "phase373_work_order_id" not in out.columns:
        raise ValueError("Phase380 requires phase373_work_order_id in refreshed work order")
    out["phase360_work_order_id"] = out["phase373_work_order_id"].astype(str)
    out["family_id"] = "phase380_expanded_real_l2_catalyst_retest"
    out["primary_scenario_id"] = PRIMARY_SCENARIO_ID
    columns = [
        "phase360_work_order_id",
        "family_id",
        "primary_scenario_id",
        "source_id",
        "symbol",
        "announcement_time_ist",
        "announcement_date",
        "market_session",
        "diagnostic_trade_date",
        "diagnostic_start_rule",
        "description",
        "no_lookahead_rule_applied",
        "full_depth_levels_1_to_5_required",
        "levels_2_to_5_materiality_required",
        "cost_profile",
        "paper_live_or_profit_claim_allowed",
    ]
    return out[columns].copy()


def write_outputs(phase379_dir: Path, phase365_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase379_summary = read_csv(phase379_dir / "phase379_acceptance_summary.csv")
    phase365_thesis = read_csv(phase365_dir / "phase365_thesis_contract.csv")
    refresh_work = read_csv(phase379_dir / "phase373_refreshed_execution_work_order.csv")
    if phase379_summary.empty or phase365_thesis.empty or refresh_work.empty:
        raise FileNotFoundError("Phase380 requires Phase379 interpretation, Phase365 thesis and refreshed work order")

    adapted_work = adapt_work_order(refresh_work)
    target_dates = sorted(adapted_work["diagnostic_trade_date"].dropna().astype(str).unique().tolist())
    symbols = sorted(adapted_work["symbol"].dropna().astype(str).unique().tolist())
    event_floor_met = as_int(metric_value(phase379_summary, "phase379_event_floor_met"))
    estimated_selected = metric_value(phase379_summary, "phase379_estimated_selected_after_refresh")

    contract = pd.DataFrame(
        [
            {
                "contract_id": "P380_EXPANDED_REAL_L2_RETEST_PRECOMMIT",
                "source_thesis_id": str(phase365_thesis["thesis_id"].iloc[0]),
                "frozen_primary_scenario_id": PRIMARY_SCENARIO_ID,
                "frozen_grid_id": PRIMARY_GRID_ID,
                "work_order_source": str(phase379_dir / "phase373_refreshed_execution_work_order.csv"),
                "adapted_work_order": "phase380_phase360_execution_work_order.csv",
                "parameter_search_allowed": 0,
                "strategy_retest_executed_now": 0,
                "full_depth_levels_1_to_5_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "cost_model": ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
                "acceptance_event_floor": EVENT_FLOOR,
                "paper_live_or_profit_claim_allowed": 0,
            }
        ]
    )
    gates = pd.DataFrame(
        [
            ("P380_PHASE379_EVENT_FLOOR_OPEN", event_floor_met, f"estimated_selected={estimated_selected}; floor={EVENT_FLOOR}"),
            ("P380_PHASE365_FROZEN_THESIS_PRESENT", int(str(phase365_thesis["thesis_id"].iloc[0]) == "P365_POST_CATALYST_IMPULSE_REVERSAL_AFTER_REPLENISHMENT"), str(phase365_thesis["thesis_id"].iloc[0])),
            ("P380_EXPANDED_WORK_ORDER_PRESENT", int(len(adapted_work) > 0), f"rows={len(adapted_work)}"),
            ("P380_FULL_DEPTH_AND_COST_RULE_RETAINED", int(adapted_work["full_depth_levels_1_to_5_required"].astype(int).eq(1).all() and adapted_work["levels_2_to_5_materiality_required"].astype(int).eq(1).all()), ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION),
            ("P380_NO_SEARCH_NO_RETEST_YET", 1, "precommit_only"),
            ("P380_NO_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    summary = pd.DataFrame(
        [
            ("phase380_expanded_reversal_acceptance_retest_precommit_complete", int(gates["passed"].astype(int).all()), "Phase380 complete"),
            ("phase380_frozen_primary_scenario_id", PRIMARY_SCENARIO_ID, "Frozen primary scenario"),
            ("phase380_adapted_work_order_rows", len(adapted_work), "Expanded work-order rows"),
            ("phase380_adapted_work_order_dates", len(target_dates), "Diagnostic dates"),
            ("phase380_adapted_work_order_symbols", len(symbols), "Symbols"),
            ("phase380_phase379_estimated_selected_after_refresh", estimated_selected, "Phase379 selected-event estimate"),
            ("phase380_event_floor_open", event_floor_met, "Event floor open"),
            ("phase380_parameter_search_allowed", 0, "No search"),
            ("phase380_strategy_retest_executed_now", 0, "No retest in precommit"),
            ("phase380_strategy_promotion_allowed", 0, "No promotion"),
            ("phase380_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase380_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase380_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed gates"),
            ("phase380_hard_gate_rows", len(gates), "Gates"),
            ("phase380_next_best_action", "execute_phase381_expanded_real_l2_frozen_reversal_acceptance_retest_no_search_no_paper_live", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase380_acceptance_summary.csv",
        "contract": output_dir / "phase380_retest_contract.csv",
        "work_order": output_dir / "phase380_phase360_execution_work_order.csv",
        "gates": output_dir / "phase380_gate_evaluation.csv",
        "report": output_dir / "phase380_expanded_reversal_acceptance_retest_precommit_report.md",
        "manifest": output_dir / "phase380_expanded_reversal_acceptance_retest_precommit_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    contract.to_csv(outputs["contract"], index=False)
    adapted_work.to_csv(outputs["work_order"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join([
        "# Phase380 Expanded Reversal Acceptance Retest Precommit",
        "",
        f"Generated: {generated_utc}",
        "",
        "Phase380 precommits the expanded real-L2 acceptance retest after Phase379 opened the event-count gate. It adapts the refreshed Phase379 work order into the Phase363/Phase381 execution schema without changing the frozen strategy parameters.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(summary),
        "",
        "## Retest contract",
        "",
        _markdown_table(contract),
        "",
        "## Gate evaluation",
        "",
        _markdown_table(gates),
        "",
        "No strategy retest, search, promotion, paper/live acceptance, or deployable profitability claim is opened in this precommit.",
    ])
    outputs["report"].write_text(report + "\n", encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({
        "phase": 380,
        "generated_at_utc": generated_utc,
        "outputs": {k: str(v) for k, v in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase380_expanded_reversal_acceptance_retest_precommit",
            generated_utc=generated_utc,
            inputs={"phase379_summary": str(phase379_dir / "phase379_acceptance_summary.csv"), "phase379_work_order": str(phase379_dir / "phase373_refreshed_execution_work_order.csv"), "phase365_thesis": str(phase365_dir / "phase365_thesis_contract.csv")},
            parameters={"primary_scenario_id": PRIMARY_SCENARIO_ID, "event_floor": EVENT_FLOOR, "parameter_search_allowed": False, "strategy_retest_executed_now": False},
            outputs={k: str(v) for k, v in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": "execute_phase381_expanded_real_l2_frozen_reversal_acceptance_retest_no_search_no_paper_live",
    }, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase379-dir", type=Path, default=DEFAULT_PHASE379_DIR)
    parser.add_argument("--phase365-dir", type=Path, default=DEFAULT_PHASE365_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.phase379_dir, args.phase365_dir, args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase380_expanded_reversal_acceptance_retest_precommit import adapt_work_order
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION

DEFAULT_PHASE385_DIR = Path("outputs/phase385")
DEFAULT_PHASE382_DIR = Path("outputs/phase382")
DEFAULT_OUTPUT_DIR = Path("outputs/phase386")
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


def write_outputs(phase385_dir: Path, phase382_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase385_summary = read_csv(phase385_dir / "phase373_acceptance_summary.csv")
    phase382_summary = read_csv(phase382_dir / "phase382_acceptance_summary.csv")
    work = read_csv(phase385_dir / "phase373_refreshed_execution_work_order.csv")
    if phase385_summary.empty or phase382_summary.empty or work.empty:
        raise FileNotFoundError("Phase386 requires Phase385 refresh and Phase382 interpretation")
    adapted = adapt_work_order(work)
    dates = sorted(adapted["diagnostic_trade_date"].dropna().astype(str).unique().tolist())
    symbols = sorted(adapted["symbol"].dropna().astype(str).unique().tolist())
    estimate = metric_value(phase385_summary, "phase373_estimated_selected_after_refresh")
    prior_selected = as_int(metric_value(phase382_summary, "phase382_primary_selected_trade_rows"))
    summary = pd.DataFrame(
        [
            ("phase386_phase385_retest_precommit_complete", 1, "Phase386 complete"),
            ("phase386_frozen_primary_scenario_id", PRIMARY_SCENARIO_ID, "Frozen primary scenario"),
            ("phase386_adapted_work_order_rows", len(adapted), "Expanded work-order rows"),
            ("phase386_adapted_work_order_dates", len(dates), "Diagnostic dates"),
            ("phase386_adapted_work_order_symbols", len(symbols), "Symbols"),
            ("phase386_phase385_estimated_selected_after_refresh", estimate, "Phase385 selected-event estimate"),
            ("phase386_previous_actual_selected_trades", prior_selected, "Phase381/382 actual selected trades"),
            ("phase386_parameter_search_allowed", 0, "No search"),
            ("phase386_strategy_retest_executed_now", 0, "No retest in precommit"),
            ("phase386_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase386_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase386_next_best_action", "execute_phase387_phase385_frozen_retest_no_search", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    contract = pd.DataFrame([{
        "contract_id": "P386_PHASE385_FROZEN_RETEST_PRECOMMIT",
        "frozen_primary_scenario_id": PRIMARY_SCENARIO_ID,
        "work_order_source": str(phase385_dir / "phase373_refreshed_execution_work_order.csv"),
        "adapted_work_order": "phase386_phase360_execution_work_order.csv",
        "parameter_search_allowed": 0,
        "strategy_retest_executed_now": 0,
        "paper_live_or_profit_claim_allowed": 0,
    }])
    gates = pd.DataFrame(
        [
            ("P386_PHASE385_REFRESH_PRESENT", as_int(metric_value(phase385_summary, "phase373_refreshed_catalyst_event_count_after_20260721_complete")), "Phase385 refresh complete"),
            ("P386_WORK_ORDER_PRESENT", int(len(adapted) > 0), f"rows={len(adapted)}"),
            ("P386_NO_SEARCH_OR_RETEST_YET", 1, "precommit_only"),
            ("P386_NO_PAPER_LIVE_OR_PROFIT_CLAIM", 1, "closed"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    outputs = {
        "summary": output_dir / "phase386_acceptance_summary.csv",
        "contract": output_dir / "phase386_retest_contract.csv",
        "work_order": output_dir / "phase386_phase360_execution_work_order.csv",
        "gates": output_dir / "phase386_gate_evaluation.csv",
        "report": output_dir / "phase386_phase385_retest_precommit_report.md",
        "manifest": output_dir / "phase386_phase385_retest_precommit_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    contract.to_csv(outputs["contract"], index=False)
    adapted.to_csv(outputs["work_order"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join([
        "# Phase386 Phase385 Frozen Retest Precommit",
        "",
        f"Generated: {generated_utc}",
        "",
        "Phase386 adapts the Phase385 refreshed work order into the frozen retest schema. It performs no retest, no search, and no paper/live action.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(summary),
        "",
        "## Gate evaluation",
        "",
        _markdown_table(gates),
    ])
    outputs["report"].write_text(report + "\n", encoding="utf-8")
    outputs["manifest"].write_text(json.dumps({
        "phase": 386,
        "generated_at_utc": generated_utc,
        "outputs": {k: str(v) for k, v in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase386_phase385_retest_precommit",
            generated_utc=generated_utc,
            inputs={"phase385_work_order": str(phase385_dir / "phase373_refreshed_execution_work_order.csv")},
            parameters={"primary_scenario_id": PRIMARY_SCENARIO_ID, "parameter_search_allowed": False},
            outputs={k: str(v) for k, v in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
    }, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase385-dir", type=Path, default=DEFAULT_PHASE385_DIR)
    parser.add_argument("--phase382-dir", type=Path, default=DEFAULT_PHASE382_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    print(json.dumps({k: str(v) for k, v in write_outputs(args.phase385_dir, args.phase382_dir, args.output_dir).items()}, indent=2))

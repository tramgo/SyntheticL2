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


DEFAULT_REFRESH_DIR = Path("outputs/phase375")
DEFAULT_OUTPUT_DIR = Path("outputs/phase375")
TARGET_DATE = "2026-07-22"
EVENT_FLOOR = 30


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    return rows.iloc[0] if not rows.empty else default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def write_outputs(refresh_dir: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase373_summary = read_csv(Path("outputs/phase373/phase373_acceptance_summary.csv"))
    phase374_summary = read_csv(Path("outputs/phase374/phase374_acceptance_summary.csv"))
    refresh_summary = read_csv(refresh_dir / "phase373_acceptance_summary.csv")
    eligibility = read_csv(refresh_dir / "phase373_no_lookahead_official_catalyst_eligibility.csv")
    if phase373_summary.empty or phase374_summary.empty or refresh_summary.empty or eligibility.empty:
        raise FileNotFoundError("Phase375 requires Phase373, Phase374 and refreshed eligibility artifacts")

    ready = eligibility[eligibility["diagnostic_real_l2_available"].astype(int).eq(1)].copy()
    target_ready = ready[ready["diagnostic_trade_date"].astype(str).eq(TARGET_DATE)].copy()
    target_carry = target_ready[target_ready["announcement_date"].astype(str).lt(TARGET_DATE)].copy()
    previous_ready = as_int(metric_value(phase373_summary, "phase373_refreshed_no_lookahead_eligible_rows"))
    refreshed_ready = int(len(ready))
    new_vs_phase373 = refreshed_ready - previous_ready
    estimated_selected = as_float(metric_value(refresh_summary, "phase373_estimated_selected_after_refresh"))
    floor_met = int(estimated_selected >= EVENT_FLOOR)

    decision = pd.DataFrame(
        [
            {
                "decision_id": "phase374_download_verified",
                "value": as_int(metric_value(phase374_summary, "phase374_local_full_universe_after")),
                "evidence": f"symbols={metric_value(phase374_summary, 'phase374_local_symbols_after')}; files={metric_value(phase374_summary, 'phase374_local_parquet_files_after')}",
                "decision": "2026-07-22 full-universe L2 is locally available.",
            },
            {
                "decision_id": "event_pool_improved",
                "value": int(new_vs_phase373 > 0),
                "evidence": f"new_vs_phase373={new_vs_phase373}; target_ready={len(target_ready)}",
                "decision": "The target day added useful catalyst events.",
            },
            {
                "decision_id": "event_floor_still_not_met",
                "value": int(floor_met == 0),
                "evidence": f"estimated_selected={estimated_selected}; floor={EVENT_FLOOR}",
                "decision": "Do not run acceptance retest yet.",
            },
        ]
    )
    gates = pd.DataFrame(
        [
            ("P375_PHASE374_FULL_UNIVERSE_PRESENT", as_int(metric_value(phase374_summary, "phase374_local_full_universe_after")), "Phase374 local full universe"),
            ("P375_REFRESH_PRESENT", int(refreshed_ready > 0), f"ready={refreshed_ready}"),
            ("P375_TARGET_EVENTS_PRESENT", int(len(target_ready) > 0), f"target_ready={len(target_ready)}"),
            ("P375_EVENT_FLOOR_CHECKED", 1, f"estimated_selected={estimated_selected:.3f}; floor={EVENT_FLOOR}"),
            ("P375_NO_RETEST_OR_PROMOTION", 1, "interpretation_only"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )
    summary = pd.DataFrame(
        [
            ("phase375_interpret_20260722_event_refresh_complete", int(gates["passed"].astype(int).all()), "Phase375 complete"),
            ("phase375_target_trade_date", TARGET_DATE, "Target date"),
            ("phase375_target_ready_rows", len(target_ready), "Eligible rows on target diagnostic date"),
            ("phase375_target_carry_forward_rows", len(target_carry), "Prior-date post-close rows carried into target"),
            ("phase375_refreshed_eligible_rows", refreshed_ready, "Refreshed eligible rows"),
            ("phase375_previous_phase373_eligible_rows", previous_ready, "Previous Phase373 eligible rows"),
            ("phase375_new_eligible_rows_vs_phase373", new_vs_phase373, "New eligible rows after adding target"),
            ("phase375_estimated_selected_after_refresh", estimated_selected, "Estimated selected trades"),
            ("phase375_event_floor_met", floor_met, "Estimated event floor met"),
            ("phase375_acceptance_retest_allowed_now", 0, "No retest in this phase"),
            ("phase375_strategy_promotion_allowed", 0, "No promotion"),
            ("phase375_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase375_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase375_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed gates"),
            ("phase375_hard_gate_rows", len(gates), "Gates"),
            ("phase375_next_best_action", "download_next_official_catalyst_real_l2_day_or_precommit_retest_only_after_floor_no_paper_live", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )
    outputs = {
        "summary": output_dir / "phase375_acceptance_summary.csv",
        "target_events": output_dir / "phase375_target_date_eligible_events.csv",
        "decision": output_dir / "phase375_decision_ledger.csv",
        "gates": output_dir / "phase375_gate_evaluation.csv",
        "report": output_dir / "phase375_interpret_20260722_event_refresh_report.md",
        "manifest": output_dir / "phase375_interpret_20260722_event_refresh_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    target_ready.to_csv(outputs["target_events"], index=False)
    decision.to_csv(outputs["decision"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase375 Interpret 2026-07-22 Event Refresh",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase375 interprets the refreshed event count after Phase374 downloaded `2026-07-22`. It does not run a strategy retest.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Decision ledger",
            "",
            _markdown_table(decision),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "No strategy retest, promotion, paper/live acceptance, or deployable profitability claim is opened.",
        ]
    )
    outputs["report"].write_text(report + "\n", encoding="utf-8")
    manifest = {
        "phase": 375,
        "generated_at_utc": generated_utc,
        "outputs": {k: str(v) for k, v in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase375_interpret_20260722_event_refresh",
            generated_utc=generated_utc,
            inputs={"refresh_dir": str(refresh_dir), "phase374_summary": "outputs/phase374/phase374_acceptance_summary.csv"},
            parameters={"target_date": TARGET_DATE, "event_floor": EVENT_FLOOR, "strategy_retest_executed": False},
            outputs={k: str(v) for k, v in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": str(summary[summary["metric"].eq("phase375_next_best_action")]["value"].iloc[0]),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-dir", type=Path, default=DEFAULT_REFRESH_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(args.refresh_dir, args.output_dir)
    print(json.dumps({k: str(v) for k, v in outputs.items()}, indent=2))

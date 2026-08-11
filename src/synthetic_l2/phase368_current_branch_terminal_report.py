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


DEFAULT_OUTPUT_DIR = Path("outputs/phase368")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def require_inputs(inputs: dict[str, pd.DataFrame]) -> None:
    missing = [name for name, frame in inputs.items() if frame.empty]
    if missing:
        raise FileNotFoundError("Phase368 requires non-empty input artifacts: " + "; ".join(missing))


def write_outputs(output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()

    p302 = read_csv(Path("outputs/phase302/phase302_acceptance_summary.csv"))
    p359 = read_csv(Path("outputs/phase359/phase359_acceptance_summary.csv"))
    p360 = read_csv(Path("outputs/phase360/phase360_acceptance_summary.csv"))
    p363 = read_csv(Path("outputs/phase363/phase363_acceptance_summary.csv"))
    p366 = read_csv(Path("outputs/phase366/phase366_acceptance_summary.csv"))
    p367 = read_csv(Path("outputs/phase367/phase367_acceptance_summary.csv"))
    p367_recon = read_csv(Path("outputs/phase367/phase367_reconciliation_ledger.csv"))

    require_inputs(
        {
            "phase302_summary": p302,
            "phase359_summary": p359,
            "phase360_summary": p360,
            "phase363_summary": p363,
            "phase366_summary": p366,
            "phase367_summary": p367,
            "phase367_reconciliation": p367_recon,
        }
    )

    p302_verdict = str(metric_value(p302, "phase302_selected_verdict", ""))
    p359_unseen_dates = str(metric_value(p359, "phase359_unseen_date_list", ""))
    p359_events = as_int(metric_value(p359, "phase359_no_lookahead_eligible_event_rows"))
    p360_ann = as_float(metric_value(p360, "phase360_primary_annualized_return_pct"))
    p360_acceptance = as_int(metric_value(p360, "phase360_acceptance_candidate_rows"))
    p363_best = str(metric_value(p363, "phase363_best_scenario_id", ""))
    p363_best_ann = as_float(metric_value(p363, "phase363_best_annualized_return_pct"))
    p363_acceptance = as_int(metric_value(p363, "phase363_acceptance_candidate_rows"))
    p366_trades = as_int(metric_value(p366, "phase366_primary_trade_rows"))
    p366_event_floor = as_int(metric_value(p366, "phase366_primary_event_floor_met"))
    p366_acceptance = as_int(metric_value(p366, "phase366_acceptance_candidate_rows"))
    p367_reopened = as_int(metric_value(p367, "phase367_passive_acceptance_reopened"))

    branch_verdict = "P368_CURRENT_PASSIVE_AWARE_AND_CATALYST_REVERSAL_BRANCH_CLOSED_FOR_ACCEPTANCE"
    evidence_chain = pd.DataFrame(
        [
            {
                "phase": 302,
                "evidence_role": "old_passive_aware_terminal_report",
                "key_observation": f"verdict={p302_verdict}",
                "acceptance_read": "Old Phase298-301 passive-aware route closed for acceptance.",
            },
            {
                "phase": 359,
                "evidence_role": "local_unseen_real_l2_official_catalyst_join",
                "key_observation": f"unseen_dates={p359_unseen_dates}; eligible_events={p359_events}",
                "acceptance_read": "Real L2/catalyst holdout evidence exists, but event count is still small.",
            },
            {
                "phase": 360,
                "evidence_role": "full_depth_market_neutral_fade_real_holdout",
                "key_observation": f"ann={p360_ann}; acceptance={p360_acceptance}",
                "acceptance_read": "Full-depth fade failed on unseen real L2 catalyst holdout.",
            },
            {
                "phase": 363,
                "evidence_role": "liquidity_replenished_catalyst_impulse_diagnostic",
                "key_observation": f"best={p363_best}; ann={p363_best_ann}; acceptance={p363_acceptance}",
                "acceptance_read": "Found a positive reversal-control clue, but no acceptance candidate.",
            },
            {
                "phase": 366,
                "evidence_role": "frozen_reversal_clue_audit",
                "key_observation": f"trades={p366_trades}; event_floor_met={p366_event_floor}; acceptance={p366_acceptance}",
                "acceptance_read": "Clue remains sparse and below event-floor acceptance.",
            },
            {
                "phase": 367,
                "evidence_role": "passive_aware_charter_reconciliation",
                "key_observation": f"passive_acceptance_reopened={p367_reopened}",
                "acceptance_read": "Passive-aware route is not reopened by the sparse clue.",
            },
        ]
    )

    closure_decisions = pd.DataFrame(
        [
            {
                "decision_id": "selected_current_branch_verdict",
                "decision_value": branch_verdict,
                "evidence": "Phase302 closure plus Phase367 reconciliation",
                "decision_status": "close_current_branch_for_acceptance",
            },
            {
                "decision_id": "do_not_run_passive_acceptance_on_12_trade_clue",
                "decision_value": 1,
                "evidence": f"Phase366 selected trades={p366_trades}; event_floor_met={p366_event_floor}",
                "decision_status": "blocked_until_more_real_events",
            },
            {
                "decision_id": "preserve_catalyst_reversal_clue",
                "decision_value": p363_best,
                "evidence": f"ann={p363_best_ann}; acceptance={p363_acceptance}",
                "decision_status": "diagnostic_only",
            },
            {
                "decision_id": "next_data_action_if_continuing",
                "decision_value": "add_or_verify_more_official_catalyst_real_l2_events",
                "evidence": "Phase367 next-action contract",
                "decision_status": "data_expansion_before_retest",
            },
            {
                "decision_id": "boundaries_closed",
                "decision_value": "promotion=0;paper_live=0;deployable_claim=0",
                "evidence": "Phase367 and upstream summaries",
                "decision_status": "closed",
            },
        ]
    )

    byproducts = pd.DataFrame(
        [
            {
                "byproduct_id": "P368_OFFICIAL_CATALYST_EVENT_JOIN",
                "kept_for": "future event-count expansion and no-lookahead real L2 diagnostics",
                "not_kept_for": "acceptance on current sparse event count",
            },
            {
                "byproduct_id": "P368_FULL_DEPTH_REAL_L2_SCHEMA_AUDIT",
                "kept_for": "ensuring levels 1-5 and levels 2-5 materiality in later tests",
                "not_kept_for": "L1-only strategy variants",
            },
            {
                "byproduct_id": "P368_PASSIVE_AWARE_REALISM_CHARTER",
                "kept_for": "future passive execution tests after event-floor evidence exists",
                "not_kept_for": "weakening fill, adverse-selection, or forced-flatten penalties",
            },
            {
                "byproduct_id": "P368_CATALYST_REVERSAL_CLUE",
                "kept_for": "falsification on additional official-catalyst real L2 days",
                "not_kept_for": "paper/live or profitability claims",
            },
        ]
    )

    gates = pd.DataFrame(
        [
            ("P368_PHASE302_TERMINAL_PRESENT", int(bool(p302_verdict)), p302_verdict),
            ("P368_PHASE359_REAL_HOLDOUT_PRESENT", int(p359_events > 0), f"eligible_events={p359_events}"),
            ("P368_PHASE360_REAL_HOLDOUT_EXECUTED", int(p360_acceptance == 0), f"ann={p360_ann}; acceptance={p360_acceptance}"),
            ("P368_PHASE366_CLUE_BELOW_ACCEPTANCE", int(p366_event_floor == 0 and p366_acceptance == 0), f"trades={p366_trades}; event_floor={p366_event_floor}; acceptance={p366_acceptance}"),
            ("P368_PHASE367_RECONCILIATION_COMPLETE", int(as_int(metric_value(p367, "phase367_passive_aware_charter_reconciliation_complete")) == 1), "Phase367 complete"),
            ("P368_EVIDENCE_CHAIN_PRESENT", int(len(evidence_chain) == 6), f"rows={len(evidence_chain)}"),
            ("P368_BOUNDARIES_CLOSED", 1, "promotion=0;paper_live=0;claim=0"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )

    summary = pd.DataFrame(
        [
            ("phase368_current_branch_terminal_report_complete", int(gates["passed"].astype(int).all()), "Phase368 complete if all hard gates pass"),
            ("phase368_selected_verdict", branch_verdict, "Current branch verdict"),
            ("phase368_phase359_no_lookahead_events", p359_events, "Phase359 eligible catalyst events"),
            ("phase368_phase360_primary_annualized_return_pct", p360_ann, "Phase360 real holdout annualized"),
            ("phase368_phase360_acceptance_candidate_rows", p360_acceptance, "Phase360 acceptance candidates"),
            ("phase368_phase363_best_scenario_id", p363_best, "Phase363 best clue"),
            ("phase368_phase363_best_annualized_return_pct", p363_best_ann, "Phase363 best annualized"),
            ("phase368_phase366_primary_trade_rows", p366_trades, "Phase366 selected trades"),
            ("phase368_phase366_event_floor_met", p366_event_floor, "Phase366 event floor"),
            ("phase368_phase367_passive_acceptance_reopened", p367_reopened, "Phase367 passive acceptance reopened"),
            ("phase368_strategy_promotion_allowed", 0, "No promotion"),
            ("phase368_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase368_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase368_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase368_hard_gate_rows", len(gates), "Hard gates"),
            ("phase368_next_best_action", "add_or_verify_more_official_catalyst_real_l2_events_before_any_retest_no_paper_live", "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )

    outputs = {
        "summary": output_dir / "phase368_acceptance_summary.csv",
        "evidence": output_dir / "phase368_evidence_chain.csv",
        "closure": output_dir / "phase368_closure_decision.csv",
        "byproducts": output_dir / "phase368_byproduct_catalog.csv",
        "gates": output_dir / "phase368_gate_evaluation.csv",
        "report": output_dir / "phase368_current_branch_terminal_report.md",
        "manifest": output_dir / "phase368_current_branch_terminal_report_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    evidence_chain.to_csv(outputs["evidence"], index=False)
    closure_decisions.to_csv(outputs["closure"], index=False)
    byproducts.to_csv(outputs["byproducts"], index=False)
    gates.to_csv(outputs["gates"], index=False)

    report = "\n".join(
        [
            "# Phase368 Current Branch Terminal Report",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase368 closes the current passive-aware/catalyst-reversal evidence branch for acceptance. This is not a claim that all top-five depth research is useless; it says the current evidence does not justify replay promotion, paper/live acceptance, or deployable profitability claims.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Evidence chain",
            "",
            _markdown_table(evidence_chain),
            "",
            "## Closure decisions",
            "",
            _markdown_table(closure_decisions),
            "",
            "## Durable by-products",
            "",
            _markdown_table(byproducts),
            "",
            "## Gates",
            "",
            _markdown_table(gates),
            "",
            "## Boundary",
            "",
            "No replay promotion, paper/live acceptance, or deployable profitability claim is opened. The next productive path is data expansion: add or verify more official-catalyst real L2 events before any retest.",
        ]
    )
    outputs["report"].write_text(report + "\n", encoding="utf-8")

    manifest = {
        "phase": 368,
        "generated_at_utc": generated_utc,
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase368_current_branch_terminal_report",
            generated_utc=generated_utc,
            inputs={
                "phase302_summary": "outputs/phase302/phase302_acceptance_summary.csv",
                "phase359_summary": "outputs/phase359/phase359_acceptance_summary.csv",
                "phase360_summary": "outputs/phase360/phase360_acceptance_summary.csv",
                "phase363_summary": "outputs/phase363/phase363_acceptance_summary.csv",
                "phase366_summary": "outputs/phase366/phase366_acceptance_summary.csv",
                "phase367_summary": "outputs/phase367/phase367_acceptance_summary.csv",
            },
            parameters={"current_branch_verdict": branch_verdict},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": str(summary[summary["metric"].eq("phase368_next_best_action")]["value"].iloc[0]),
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(output_dir=args.output_dir)
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))

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


DEFAULT_PHASE300_DIR = Path("outputs/phase300")
DEFAULT_PHASE301_DIR = Path("outputs/phase301")
DEFAULT_PHASE363_DIR = Path("outputs/phase363")
DEFAULT_PHASE366_DIR = Path("outputs/phase366")
DEFAULT_CHARTER_PATH = Path("Plan/phase300_passive_aware_execution_charter.md")
DEFAULT_OUTPUT_DIR = Path("outputs/phase367")


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


def contains_all(text: str, needles: list[str]) -> int:
    lowered = text.lower()
    return int(all(needle.lower() in lowered for needle in needles))


def contains_any(text: str, needles: list[str]) -> int:
    lowered = text.lower()
    return int(any(needle.lower() in lowered for needle in needles))


def write_outputs(
    phase300_dir: Path,
    phase301_dir: Path,
    phase363_dir: Path,
    phase366_dir: Path,
    charter_path: Path,
    output_dir: Path,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()

    phase300_summary = read_csv(phase300_dir / "phase300_acceptance_summary.csv")
    phase300_gates = read_csv(phase300_dir / "phase300_gate_evaluation.csv")
    phase301_summary = read_csv(phase301_dir / "phase301_acceptance_summary.csv")
    phase301_kill = read_csv(phase301_dir / "phase301_kill_switch_audit.csv")
    phase363_summary = read_csv(phase363_dir / "phase363_acceptance_summary.csv")
    phase366_summary = read_csv(phase366_dir / "phase366_acceptance_summary.csv")
    phase366_interp = read_csv(phase366_dir / "phase366_interpretation_ledger.csv")

    missing = [
        str(path)
        for path, frame in [
            (phase300_dir / "phase300_acceptance_summary.csv", phase300_summary),
            (phase300_dir / "phase300_gate_evaluation.csv", phase300_gates),
            (phase301_dir / "phase301_acceptance_summary.csv", phase301_summary),
            (phase301_dir / "phase301_kill_switch_audit.csv", phase301_kill),
            (phase363_dir / "phase363_acceptance_summary.csv", phase363_summary),
            (phase366_dir / "phase366_acceptance_summary.csv", phase366_summary),
        ]
        if frame.empty
    ]
    if missing:
        raise FileNotFoundError("Phase367 requires existing Phase300/301/363/366 artifacts: " + "; ".join(missing))

    charter_text = charter_path.read_text(encoding="utf-8") if charter_path.exists() else ""
    charter_checks = pd.DataFrame(
        [
            {
                "charter_check_id": "P367_CHARTER_PRESENT",
                "passed": int(charter_path.exists()),
                "evidence": str(charter_path),
                "interpretation": "Attached passive-aware charter is present in the plan folder.",
            },
            {
                "charter_check_id": "P367_REALISM_PENALTIES_PRESENT",
                "passed": int(
                    contains_all(charter_text, ["fill", "adverse"])
                    and contains_any(charter_text, ["forced flatten", "forced-flatten", "forced flattening"])
                ),
                "evidence": "fill/adverse/forced-flatten text scan",
                "interpretation": "Charter requires fill probability, adverse selection, and forced flatten cost.",
            },
            {
                "charter_check_id": "P367_FULL_DEPTH_REQUIRED",
                "passed": contains_all(charter_text, ["levels 1-5", "levels 2-5"]),
                "evidence": "full-depth text scan",
                "interpretation": "Charter forbids L1-only variants and requires full top-five depth materiality.",
            },
            {
                "charter_check_id": "P367_COST200_REQUIRED",
                "passed": contains_all(charter_text, ["cost200", "2x"]),
                "evidence": "cost stress text scan",
                "interpretation": "Charter pins 2x cost stress and fixed-capital scoring.",
            },
            {
                "charter_check_id": "P367_NO_RESCUE_REQUIRED",
                "passed": contains_all(charter_text, ["do not", "more filters"]),
                "evidence": "kill-switch text scan",
                "interpretation": "Charter forbids after-the-fact rescue tuning of the same stack.",
            },
        ]
    )

    phase300_survivors = as_int(metric_value(phase300_summary, "phase300_cost200_acceptance_survivor_rows"))
    phase300_event_floor = as_int(metric_value(phase300_summary, "phase300_event_floor_scenario_rows"))
    phase300_breadth = as_int(metric_value(phase300_summary, "phase300_breadth_met_scenario_rows"))
    phase300_kill = as_int(metric_value(phase300_summary, "phase300_kill_switch_triggered"))
    phase300_gate_pass = as_int(metric_value(phase300_summary, "phase300_hard_gate_pass_rows"))
    phase300_gate_rows = as_int(metric_value(phase300_summary, "phase300_hard_gate_rows"))

    phase301_terminal = as_int(metric_value(phase301_summary, "phase301_terminal_report_required"))
    phase301_no_rescue = as_int(metric_value(phase301_summary, "phase301_do_not_rescue_with_more_filters"))
    phase301_outcome = str(metric_value(phase301_summary, "phase301_selected_outcome", ""))

    phase363_best = str(metric_value(phase363_summary, "phase363_best_scenario_id", ""))
    phase363_best_ann = as_float(metric_value(phase363_summary, "phase363_best_annualized_return_pct"))
    phase363_acceptance = as_int(metric_value(phase363_summary, "phase363_acceptance_candidate_rows"))

    phase366_primary_ann = as_float(metric_value(phase366_summary, "phase366_primary_annualized_return_pct"))
    phase366_primary_trades = as_int(metric_value(phase366_summary, "phase366_primary_trade_rows"))
    phase366_event_floor = as_int(metric_value(phase366_summary, "phase366_primary_event_floor_met"))
    phase366_acceptance = as_int(metric_value(phase366_summary, "phase366_acceptance_candidate_rows"))
    phase366_strict_ann = as_float(metric_value(phase366_summary, "phase366_strict_replenishment_annualized_return_pct"))
    phase366_above12 = as_int(metric_value(phase366_summary, "phase366_primary_above12"))

    reconciliation = pd.DataFrame(
        [
            {
                "reconciliation_id": "phase300_charter_executed",
                "status": "proved",
                "evidence": f"gates={phase300_gate_pass}/{phase300_gate_rows}; survivors={phase300_survivors}",
                "decision": "Attached passive-aware charter already has an executed Phase300 artifact chain.",
            },
            {
                "reconciliation_id": "phase300_acceptance_closed",
                "status": "proved" if phase300_survivors == 0 and phase300_kill == 1 else "not_proved",
                "evidence": f"survivors={phase300_survivors}; kill_switch={phase300_kill}",
                "decision": "Passive-aware execution route remains closed for the Phase299/300 evidence chain.",
            },
            {
                "reconciliation_id": "phase301_no_rescue_binding",
                "status": "proved" if phase301_terminal == 1 and phase301_no_rescue == 1 else "not_proved",
                "evidence": f"outcome={phase301_outcome}; terminal={phase301_terminal}; no_rescue={phase301_no_rescue}",
                "decision": "Do not tune extra filters into the old Phase300 stack.",
            },
            {
                "reconciliation_id": "phase366_new_clue_present",
                "status": "proved" if phase366_above12 == 1 and phase366_primary_trades > 0 else "not_proved",
                "evidence": f"scenario={phase363_best}; ann={phase366_primary_ann}; trades={phase366_primary_trades}",
                "decision": "The later catalyst-reversal branch is a new sparse clue, not a Phase300 rescue.",
            },
            {
                "reconciliation_id": "phase366_not_enough_to_reopen_passive_acceptance",
                "status": "proved" if phase366_event_floor == 0 and phase366_acceptance == 0 else "not_proved",
                "evidence": f"event_floor_met={phase366_event_floor}; acceptance={phase366_acceptance}; strict_replenishment_ann={phase366_strict_ann}",
                "decision": "The clue is too sparse and too fragile under stricter replenishment to justify passive-aware acceptance testing as a promotion path now.",
            },
        ]
    )

    next_action_contract = pd.DataFrame(
        [
            {
                "contract_id": "P367_ALLOW_ONLY_FROZEN_FALSIFICATION_OR_MORE_REAL_EVENTS",
                "allowed": 1,
                "requirement": "Either write a terminal/branch report or acquire/verify additional official-catalyst real L2 events before any passive-aware rerun.",
            },
            {
                "contract_id": "P367_PASSIVE_RERUN_BLOCKED_UNTIL_EVENT_FLOOR",
                "allowed": 0,
                "requirement": "Do not run passive-aware execution on the 12-trade Phase366 clue as acceptance evidence; >=30 scheduled events are required first.",
            },
            {
                "contract_id": "P367_NO_FILTER_RESCUE",
                "allowed": 0,
                "requirement": "Do not add more filters to rescue the old passive-aware stack.",
            },
            {
                "contract_id": "P367_IF_REOPENED_USE_CHARTER_REALISM",
                "allowed": 1,
                "requirement": "Any future passive-aware run must include probabilistic fills, adverse-selection penalty, forced flatten, full top-five depth, no lookahead and cost200.",
            },
            {
                "contract_id": "P367_BOUNDARIES_CLOSED",
                "allowed": 0,
                "requirement": "No replay promotion, paper/live acceptance or deployable profitability claim.",
            },
        ]
    )

    gates = pd.DataFrame(
        [
            ("P367_CHARTER_PRESENT", int(charter_checks["passed"].astype(int).all()), f"checks={int(charter_checks['passed'].astype(int).sum())}/{len(charter_checks)}"),
            ("P367_PHASE300_EXECUTED", int(phase300_gate_pass == phase300_gate_rows and phase300_gate_rows > 0), f"phase300_gates={phase300_gate_pass}/{phase300_gate_rows}"),
            ("P367_PHASE301_INTERPRETED", int(phase301_outcome == "P301_PASSIVE_AWARE_EXECUTION_FALSIFIED"), phase301_outcome),
            ("P367_PHASE366_CLUE_AUDITED", int(phase366_primary_trades > 0 and phase366_acceptance == 0), f"trades={phase366_primary_trades}; acceptance={phase366_acceptance}"),
            ("P367_NO_REOPEN_WITH_SPARSE_CLUE", int(phase366_event_floor == 0), f"event_floor_met={phase366_event_floor}"),
            ("P367_BOUNDARIES_CLOSED", 1, "replay=0;promotion=0;paper=0;claim=0"),
        ],
        columns=["gate_id", "passed", "evidence"],
    )

    passive_acceptance_reopened = 0
    next_action = "expand_official_catalyst_real_l2_events_or_write_terminal_branch_report_no_paper_live"
    summary = pd.DataFrame(
        [
            ("phase367_passive_aware_charter_reconciliation_complete", int(gates["passed"].astype(int).all()), "Phase367 completed if all hard gates pass"),
            ("phase367_phase300_charter_survivor_rows", phase300_survivors, "Phase300 cost200 acceptance survivors"),
            ("phase367_phase300_event_floor_rows", phase300_event_floor, "Phase300 event-floor scenarios"),
            ("phase367_phase300_breadth_rows", phase300_breadth, "Phase300 breadth-met scenarios"),
            ("phase367_phase301_terminal_report_required", phase301_terminal, "Phase301 terminal report requirement"),
            ("phase367_phase366_primary_annualized_return_pct", phase366_primary_ann, "Phase366 clue annualized diagnostic"),
            ("phase367_phase366_primary_trade_rows", phase366_primary_trades, "Phase366 selected trades"),
            ("phase367_phase366_event_floor_met", phase366_event_floor, "Phase366 event floor"),
            ("phase367_phase366_acceptance_candidate_rows", phase366_acceptance, "Phase366 acceptance candidates"),
            ("phase367_passive_acceptance_reopened", passive_acceptance_reopened, "Whether passive-aware acceptance path is reopened now"),
            ("phase367_strategy_promotion_allowed", 0, "No promotion"),
            ("phase367_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase367_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase367_hard_gate_pass_rows", int(gates["passed"].astype(int).sum()), "Passed hard gates"),
            ("phase367_hard_gate_rows", len(gates), "Hard gates"),
            ("phase367_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )

    outputs = {
        "summary": output_dir / "phase367_acceptance_summary.csv",
        "charter": output_dir / "phase367_charter_requirement_audit.csv",
        "reconciliation": output_dir / "phase367_reconciliation_ledger.csv",
        "contract": output_dir / "phase367_next_action_contract.csv",
        "gates": output_dir / "phase367_gate_evaluation.csv",
        "report": output_dir / "phase367_passive_aware_charter_reconciliation_report.md",
        "manifest": output_dir / "phase367_passive_aware_charter_reconciliation_manifest.json",
    }
    summary.to_csv(outputs["summary"], index=False)
    charter_checks.to_csv(outputs["charter"], index=False)
    reconciliation.to_csv(outputs["reconciliation"], index=False)
    next_action_contract.to_csv(outputs["contract"], index=False)
    gates.to_csv(outputs["gates"], index=False)
    report = "\n".join(
        [
            "# Phase367 Passive-Aware Charter Reconciliation",
            "",
            f"Generated: {generated_utc}",
            "",
            "Phase367 reconciles the attached Phase300 passive-aware execution charter with the later Phase363/366 catalyst-reversal clue. It creates no new trades, performs no search, and opens no promotion, paper/live acceptance, or deployable profitability claim.",
            "",
            "## Acceptance summary",
            "",
            _markdown_table(summary),
            "",
            "## Charter requirement audit",
            "",
            _markdown_table(charter_checks),
            "",
            "## Reconciliation ledger",
            "",
            _markdown_table(reconciliation),
            "",
            "## Next-action contract",
            "",
            _markdown_table(next_action_contract),
            "",
            "## Gate evaluation",
            "",
            _markdown_table(gates),
            "",
            "Phase367 decision: the Phase300 passive-aware route remains falsified for its evidence chain. The Phase366 catalyst-reversal branch is a positive sparse clue, but it does not reopen passive-aware acceptance testing until additional official-catalyst real L2 events satisfy the event floor and robustness controls.",
            "",
            "No promotion, paper/live acceptance, or deployable profitability claim is opened.",
        ]
    )
    outputs["report"].write_text(report + "\n", encoding="utf-8")
    manifest = {
        "phase": 367,
        "generated_at_utc": generated_utc,
        "charter_path": str(charter_path),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "reproducibility": reproducibility_fields(
            artifact_id="phase367_passive_aware_charter_reconciliation",
            generated_utc=generated_utc,
            inputs={
                "phase300_summary": str(phase300_dir / "phase300_acceptance_summary.csv"),
                "phase301_summary": str(phase301_dir / "phase301_acceptance_summary.csv"),
                "phase363_summary": str(phase363_dir / "phase363_acceptance_summary.csv"),
                "phase366_summary": str(phase366_dir / "phase366_acceptance_summary.csv"),
                "charter": str(charter_path),
            },
            parameters={"no_new_trades": True, "passive_acceptance_reopened": passive_acceptance_reopened},
            outputs={key: str(value) for key, value in outputs.items()},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
        ),
        "next_action": next_action,
    }
    outputs["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase300-dir", type=Path, default=DEFAULT_PHASE300_DIR)
    parser.add_argument("--phase301-dir", type=Path, default=DEFAULT_PHASE301_DIR)
    parser.add_argument("--phase363-dir", type=Path, default=DEFAULT_PHASE363_DIR)
    parser.add_argument("--phase366-dir", type=Path, default=DEFAULT_PHASE366_DIR)
    parser.add_argument("--charter-path", type=Path, default=DEFAULT_CHARTER_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    outputs = write_outputs(
        phase300_dir=args.phase300_dir,
        phase301_dir=args.phase301_dir,
        phase363_dir=args.phase363_dir,
        phase366_dir=args.phase366_dir,
        charter_path=args.charter_path,
        output_dir=args.output_dir,
    )
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))

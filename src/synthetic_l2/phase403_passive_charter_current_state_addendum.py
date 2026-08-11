from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_ATTACHMENT = Path(r"C:\Users\Ramic\.codex\attachments\10cf61a2-bfc1-4e3b-9099-09a01ef9583e\pasted-text.txt")
DEFAULT_PHASE300_DIR = Path("outputs/phase300")
DEFAULT_PHASE301_DIR = Path("outputs/phase301")
DEFAULT_PHASE302_DIR = Path("outputs/phase302")
DEFAULT_PHASE402_DIR = Path("outputs/phase402")
DEFAULT_OUTPUT_DIR = Path("outputs/phase403")

SELECTED_DECISION = "P403_PASSIVE_AWARE_CHARTER_EXECUTED_AND_REMAINS_FALSIFIED"
NEXT_ACTION = "precommit_material_new_full_depth_l2_thesis_or_stop_same_route_no_paper_live"
REPAIR_ACTION = "repair_phase403_passive_charter_current_state_addendum"
ANNUALIZED_THRESHOLD_PCT = 12.0
MIN_SELECTED_EVENT_ROWS = 30


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def attachment_digest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"present": 0, "bytes": 0, "contains_passive_aware": 0, "contains_forced_flatten": 0}
    text = path.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    return {
        "present": 1,
        "bytes": path.stat().st_size,
        "contains_passive_aware": int("passive" in lowered and "aware" in lowered),
        "contains_forced_flatten": int("forced" in lowered and "flatten" in lowered),
    }


def build_evidence_ledger(
    attachment_info: dict[str, Any],
    phase300: pd.DataFrame,
    phase301: pd.DataFrame,
    phase302: pd.DataFrame,
    phase402: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "evidence_id": "P403_ATTACHMENT_CHARTER_PRESENT",
                "source": str(DEFAULT_ATTACHMENT),
                "observed_value": f"present={attachment_info['present']};bytes={attachment_info['bytes']}",
                "interpretation": "Attached passive-aware execution charter was read for this addendum.",
            },
            {
                "evidence_id": "P403_PHASE300_EXECUTED",
                "source": "outputs/phase300/phase300_acceptance_summary.csv",
                "observed_value": (
                    f"execution_complete={metric_value(phase300, 'phase300_execution_complete', '')};"
                    f"scenarios={metric_value(phase300, 'phase300_scenario_rows', '')};"
                    f"survivors={metric_value(phase300, 'phase300_cost200_acceptance_survivor_rows', '')};"
                    f"kill={metric_value(phase300, 'phase300_kill_switch_triggered', '')}"
                ),
                "interpretation": "The attached charter's passive-aware hybrid was already executed under Phase300.",
            },
            {
                "evidence_id": "P403_PHASE301_FALSIFIED",
                "source": "outputs/phase301/phase301_acceptance_summary.csv",
                "observed_value": (
                    f"outcome={metric_value(phase301, 'phase301_selected_outcome', '')};"
                    f"terminal_required={metric_value(phase301, 'phase301_terminal_report_required', '')};"
                    f"do_not_rescue={metric_value(phase301, 'phase301_do_not_rescue_with_more_filters', '')}"
                ),
                "interpretation": "The passive-aware route was interpreted as falsified; same-stack rescue tuning is forbidden.",
            },
            {
                "evidence_id": "P403_PHASE302_TERMINAL_REPORT",
                "source": "outputs/phase302/phase302_acceptance_summary.csv",
                "observed_value": (
                    f"verdict={metric_value(phase302, 'phase302_selected_verdict', '')};"
                    f"material_new_required={metric_value(phase302, 'phase302_material_new_source_or_thesis_required', '')};"
                    f"do_not_continue_same_route={metric_value(phase302, 'phase302_do_not_continue_same_route', '')}"
                ),
                "interpretation": "The older Phase300 charter route already required a material-new source or thesis before continuing.",
            },
            {
                "evidence_id": "P403_PHASE402_NEW_REAL_L2_RETEST",
                "source": "outputs/phase402/phase388_acceptance_summary.csv",
                "observed_value": (
                    f"annualized={metric_value(phase402, 'phase388_primary_annualized_return_pct', '')};"
                    f"selected_trades={metric_value(phase402, 'phase388_primary_capacity_selected_trades', '')};"
                    f"acceptance={metric_value(phase402, 'phase388_acceptance_candidate', '')};"
                    f"promotion={metric_value(phase402, 'phase388_strategy_promotion_allowed', '')}"
                ),
                "interpretation": "The newer real-L2 catalyst reversal retest also failed acceptance and fell below the >12% annualized threshold.",
            },
        ]
    )


def build_gate_evaluation(
    attachment_info: dict[str, Any],
    phase300: pd.DataFrame,
    phase301: pd.DataFrame,
    phase302: pd.DataFrame,
    phase402: pd.DataFrame,
) -> pd.DataFrame:
    phase300_survivors = as_int(metric_value(phase300, "phase300_cost200_acceptance_survivor_rows", 0))
    phase402_ann = to_float(metric_value(phase402, "phase388_primary_annualized_return_pct", 0.0))
    phase402_trades = as_int(metric_value(phase402, "phase388_primary_capacity_selected_trades", 0))
    phase402_acceptance = as_int(metric_value(phase402, "phase388_acceptance_candidate", 0))
    gates = [
        ("P403_ATTACHMENT_PRESENT", attachment_info["present"] == 1, attachment_info["present"], 1),
        ("P403_ATTACHMENT_MATCHES_PASSIVE_CHARTER", attachment_info["contains_passive_aware"] == 1 and attachment_info["contains_forced_flatten"] == 1, f"passive={attachment_info['contains_passive_aware']};flatten={attachment_info['contains_forced_flatten']}", "passive_aware_and_forced_flatten"),
        ("P403_PHASE300_EXECUTION_COMPLETE", as_int(metric_value(phase300, "phase300_execution_complete", 0)) == 1, metric_value(phase300, "phase300_execution_complete", ""), 1),
        ("P403_PHASE300_NO_ACCEPTANCE_SURVIVOR", phase300_survivors == 0, phase300_survivors, 0),
        ("P403_PHASE301_FALSIFIED", str(metric_value(phase301, "phase301_selected_outcome", "")) == "P301_PASSIVE_AWARE_EXECUTION_FALSIFIED", metric_value(phase301, "phase301_selected_outcome", ""), "P301_PASSIVE_AWARE_EXECUTION_FALSIFIED"),
        ("P403_PHASE302_MATERIAL_NEW_REQUIRED", as_int(metric_value(phase302, "phase302_material_new_source_or_thesis_required", 0)) == 1, metric_value(phase302, "phase302_material_new_source_or_thesis_required", ""), 1),
        ("P403_PHASE402_NOT_PROFITABLE_BY_USER_RULE", phase402_ann <= ANNUALIZED_THRESHOLD_PCT, phase402_ann, f">{ANNUALIZED_THRESHOLD_PCT}"),
        ("P403_PHASE402_SELECTED_FLOOR_NOT_MET", phase402_trades < MIN_SELECTED_EVENT_ROWS, phase402_trades, f">={MIN_SELECTED_EVENT_ROWS}"),
        ("P403_PHASE402_NO_ACCEPTANCE", phase402_acceptance == 0, phase402_acceptance, 0),
        ("P403_BOUNDARIES_CLOSED", as_int(metric_value(phase402, "phase388_strategy_promotion_allowed", 0)) == 0 and as_int(metric_value(phase402, "phase388_paper_or_live_acceptance_allowed", 0)) == 0 and as_int(metric_value(phase402, "phase388_deployable_profitability_claim_allowed", 0)) == 0, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in gates])


def build_decision_ledger(phase300: pd.DataFrame, phase302: pd.DataFrame, phase402: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("selected_decision", SELECTED_DECISION, "Phase300/301/302 and Phase402 all reject acceptance.", "closed_for_same_route"),
            ("attached_charter_action_status", "already_executed_as_phase300_and_interpreted_as_phase301", "Phase300 execution and Phase301 falsification are present.", "done"),
            ("same_passive_aware_rescue_allowed", 0, f"phase302_do_not_continue_same_route={metric_value(phase302, 'phase302_do_not_continue_same_route', '')}", "forbidden"),
            ("new_real_l2_reversal_status", "failed_current_profitability_rule", f"phase402_ann={metric_value(phase402, 'phase388_primary_annualized_return_pct', '')};selected={metric_value(phase402, 'phase388_primary_capacity_selected_trades', '')}", "not_accepted"),
            ("best_phase300_sparse_pocket_status", "diagnostic_only", f"phase300_best_events={metric_value(phase300, 'phase300_best_scheduled_event_rows', '')};survivors={metric_value(phase300, 'phase300_cost200_acceptance_survivor_rows', '')}", "not_acceptance"),
            ("recommended_next_route", NEXT_ACTION, "Needs material-new full-depth L2 thesis/source; do not rescue same stack.", "next"),
            ("paper_live_or_profit_claim", 0, "promotion=0;paper=0;claim=0", "closed"),
        ],
        columns=["decision_id", "decision_value", "evidence", "decision_status"],
    )


def build_acceptance(gates: pd.DataFrame, decisions: pd.DataFrame, phase300: pd.DataFrame, phase402: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    next_action = NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION
    return pd.DataFrame(
        [
            ("phase403_passive_charter_current_state_addendum_complete", 1, "Phase403 addendum completed"),
            ("phase403_selected_decision", SELECTED_DECISION, "Current decision"),
            ("phase403_attachment_performed_status", "already_executed_phase300_phase301_phase302", "Attached passive-aware charter route has already been performed and closed"),
            ("phase403_phase300_cost200_acceptance_survivor_rows", metric_value(phase300, "phase300_cost200_acceptance_survivor_rows", 0), "Phase300 acceptance survivors"),
            ("phase403_phase300_best_scheduled_event_rows", metric_value(phase300, "phase300_best_scheduled_event_rows", 0), "Phase300 best sparse events"),
            ("phase403_phase402_primary_annualized_return_pct", metric_value(phase402, "phase388_primary_annualized_return_pct", 0), "Newest real-L2 retest annualized return"),
            ("phase403_phase402_primary_capacity_selected_trades", metric_value(phase402, "phase388_primary_capacity_selected_trades", 0), "Newest real-L2 selected trades"),
            ("phase403_phase402_acceptance_candidate", metric_value(phase402, "phase388_acceptance_candidate", 0), "Newest real-L2 acceptance"),
            ("phase403_same_route_rescue_allowed", 0, "Do not rescue the passive-aware Phase300 stack"),
            ("phase403_material_new_thesis_required", 1, "Required before next strategy search"),
            ("phase403_strategy_replay_allowed", 0, "No replay opened by this addendum"),
            ("phase403_strategy_promotion_allowed", 0, "No promotion"),
            ("phase403_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase403_deployable_profitability_claim_allowed", 0, "No deployable claim"),
            ("phase403_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase403_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase403_next_best_action", next_action, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, evidence: pd.DataFrame, decisions: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase403 Passive-Aware Charter Current-State Addendum",
        "",
        "Phase403 reconciles the attached passive-aware execution charter with the current repository evidence.",
        "",
        "Result: the attached charter was already executed as Phase300, interpreted as falsified in Phase301, closed in Phase302, and the newer Phase402 real-L2 retest does not reopen the same route.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Evidence Ledger",
        "",
        _markdown_table(evidence),
        "",
        "## Decision Ledger",
        "",
        _markdown_table(decisions),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: this addendum opens no promotion, paper/live acceptance, deployable profitability claim, or same-route rescue.",
    ]
    (output_dir / "phase403_passive_charter_current_state_addendum_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    attachment: Path = DEFAULT_ATTACHMENT,
    phase300_dir: Path = DEFAULT_PHASE300_DIR,
    phase301_dir: Path = DEFAULT_PHASE301_DIR,
    phase302_dir: Path = DEFAULT_PHASE302_DIR,
    phase402_dir: Path = DEFAULT_PHASE402_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    attachment_info = attachment_digest(attachment)
    phase300 = read_csv(phase300_dir / "phase300_acceptance_summary.csv")
    phase301 = read_csv(phase301_dir / "phase301_acceptance_summary.csv")
    phase302 = read_csv(phase302_dir / "phase302_acceptance_summary.csv")
    phase402 = read_csv(phase402_dir / "phase388_acceptance_summary.csv")
    if phase300.empty or phase301.empty or phase302.empty or phase402.empty:
        raise FileNotFoundError("Phase300/301/302 or Phase402 summary evidence is missing.")
    evidence = build_evidence_ledger(attachment_info, phase300, phase301, phase302, phase402)
    gates = build_gate_evaluation(attachment_info, phase300, phase301, phase302, phase402)
    decisions = build_decision_ledger(phase300, phase302, phase402)
    acceptance = build_acceptance(gates, decisions, phase300, phase402)

    evidence.to_csv(output_dir / "phase403_evidence_ledger.csv", index=False)
    decisions.to_csv(output_dir / "phase403_decision_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase403_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase403_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, evidence, decisions, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase403_passive_charter_current_state_addendum",
        **reproducibility_fields(
            artifact_id="phase403_passive_charter_current_state_addendum",
            generated_utc=generated_utc,
            inputs={
                "attachment": str(attachment),
                "phase300_acceptance_summary": str(phase300_dir / "phase300_acceptance_summary.csv"),
                "phase301_acceptance_summary": str(phase301_dir / "phase301_acceptance_summary.csv"),
                "phase302_acceptance_summary": str(phase302_dir / "phase302_acceptance_summary.csv"),
                "phase402_acceptance_summary": str(phase402_dir / "phase388_acceptance_summary.csv"),
            },
            parameters={
                "selected_decision": SELECTED_DECISION,
                "annualized_threshold_pct": ANNUALIZED_THRESHOLD_PCT,
                "min_selected_event_rows": MIN_SELECTED_EVENT_ROWS,
                "next_action": NEXT_ACTION,
            },
            outputs={"acceptance_summary": str(output_dir / "phase403_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_addendum_only",
        ),
    }
    (output_dir / "phase403_passive_charter_current_state_addendum_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Phase403 passive-aware charter current-state addendum.")
    parser.add_argument("--attachment", type=Path, default=DEFAULT_ATTACHMENT)
    parser.add_argument("--phase300-dir", type=Path, default=DEFAULT_PHASE300_DIR)
    parser.add_argument("--phase301-dir", type=Path, default=DEFAULT_PHASE301_DIR)
    parser.add_argument("--phase302-dir", type=Path, default=DEFAULT_PHASE302_DIR)
    parser.add_argument("--phase402-dir", type=Path, default=DEFAULT_PHASE402_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.attachment, args.phase300_dir, args.phase301_dir, args.phase302_dir, args.phase402_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

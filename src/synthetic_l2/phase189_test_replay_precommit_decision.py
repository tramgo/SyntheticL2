from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE187_DIR = Path("outputs/phase187")
DEFAULT_PHASE188_DIR = Path("outputs/phase188")
DEFAULT_OUTPUT_DIR = Path("outputs/phase189")
FORBIDDEN_OUTPUTS = "test_replay;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = "") -> Any:
    if frame.empty or "metric" not in frame.columns or "value" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def build_phase189_decision(phase188: pd.DataFrame, interpretation: pd.DataFrame) -> pd.DataFrame:
    candidate_id = str(metric_value(phase188, "phase188_candidate_id", ""))
    min_profile_net = as_float(metric_value(phase188, "phase188_min_profile_net_bps_proxy_mean", 0.0))
    control_edge = as_float(metric_value(phase188, "phase188_min_profile_edge_over_shuffled_bps", 0.0))
    breadth_warning = as_int(metric_value(phase188, "phase188_breadth_warning", 1))
    date_warning = as_int(metric_value(phase188, "phase188_date_count_warning", 1))
    concentration_warning = as_int(metric_value(phase188, "phase188_concentration_warning", 1))
    symbol_positive_fraction = as_float(metric_value(phase188, "phase188_symbol_positive_fraction", 0.0))
    validation_decision_events = as_int(metric_value(phase188, "phase188_validation_decision_events", 0))
    interpreted_row = interpretation.iloc[0].to_dict() if not interpretation.empty else {}
    hard_promising = int(min_profile_net > 0 and control_edge > 0 and concentration_warning == 0)
    caution_flags = int(breadth_warning + date_warning)
    test_precommit_allowed = int(hard_promising == 1 and caution_flags == 0)
    decision = (
        "precommit_single_candidate_untouched_test_replay"
        if test_precommit_allowed
        else "defer_test_replay_collect_more_validation_breadth_or_redesign"
    )
    return pd.DataFrame(
        [
            {
                "candidate_id": candidate_id,
                "phase188_robustness_interpretation": interpreted_row.get("robustness_interpretation", ""),
                "min_profile_net_bps_proxy_mean": min_profile_net,
                "min_profile_edge_over_shuffled_bps": control_edge,
                "validation_decision_events": validation_decision_events,
                "symbol_positive_fraction": symbol_positive_fraction,
                "concentration_warning": concentration_warning,
                "breadth_warning": breadth_warning,
                "date_count_warning": date_warning,
                "hard_promising_evidence": hard_promising,
                "caution_flag_count": caution_flags,
                "phase189_decision": decision,
                "untouched_test_replay_precommit_allowed": test_precommit_allowed,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
            }
        ]
    )


def build_future_test_contract(decision: pd.DataFrame) -> pd.DataFrame:
    row = decision.iloc[0] if not decision.empty else {}
    candidate_id = row.get("candidate_id", "")
    return pd.DataFrame(
        [
            {
                "contract_id": "P189_SINGLE_CANDIDATE_FREEZE",
                "requirement": f"Only the frozen candidate may be used in any later untouched-test replay: {candidate_id}. No threshold, profile or symbol selection may use test rows.",
                "required_before_test_replay": 1,
                "status_after_phase189": "precommitted_but_not_opened",
            },
            {
                "contract_id": "P189_NO_VALIDATION_RESELECTION",
                "requirement": "If additional validation breadth is collected, candidate choice must be either frozen or the phase must return to train-only selection; test rows remain untouched.",
                "required_before_test_replay": 1,
                "status_after_phase189": "precommitted_but_not_opened",
            },
            {
                "contract_id": "P189_BREADTH_REPAIR_REQUIRED",
                "requirement": "Before untouched-test replay, either symbol breadth warning and date-count warning must be repaired, or explicitly accepted as a diagnostic-only test limitation.",
                "required_before_test_replay": 1,
                "status_after_phase189": "blocking_current_test_unlock",
            },
            {
                "contract_id": "P189_COST_LATENCY_BINDING",
                "requirement": "Any later test replay must bind Phase180 retail/default and stressed-retail cost/latency profiles before any net metric.",
                "required_before_test_replay": 1,
                "status_after_phase189": "precommitted_but_not_opened",
            },
            {
                "contract_id": "P189_NEGATIVE_CONTROLS_REQUIRED",
                "requirement": "Any later untouched-test replay must include shuffled-time and shuffled-symbol controls before interpretation.",
                "required_before_test_replay": 1,
                "status_after_phase189": "precommitted_but_not_opened",
            },
            {
                "contract_id": "P189_NO_PROMOTION_FROM_TEST_ALONE",
                "requirement": "A positive untouched-test replay may only trigger a later promotion-readiness audit; it cannot directly open paper/live acceptance.",
                "required_before_test_replay": 1,
                "status_after_phase189": "precommitted_but_not_opened",
            },
        ]
    )


def build_redesign_or_data_action(decision: pd.DataFrame) -> pd.DataFrame:
    row = decision.iloc[0] if not decision.empty else {}
    breadth_warning = as_int(row.get("breadth_warning", 1))
    date_warning = as_int(row.get("date_count_warning", 1))
    actions = []
    if date_warning:
        actions.append(
            {
                "action_id": "P189_ADD_VALIDATION_DATES",
                "priority": 1,
                "action": "Add or designate additional validation dates before untouched-test replay.",
                "evidence_target": "validation_dates_with_events >= 2 without using test_untouched rows",
            }
        )
    if breadth_warning:
        actions.append(
            {
                "action_id": "P189_REPAIR_SYMBOL_BREADTH_OR_DECLARE_SCOPE",
                "priority": 2,
                "action": "Repair weak symbol breadth or explicitly restrict the candidate scope before test replay.",
                "evidence_target": "symbol_positive_fraction >= 0.25 or candidate_scope_declared_symbol_specific",
            }
        )
    actions.append(
        {
            "action_id": "P189_PREPARE_DIAGNOSTIC_TEST_REPLAY_SPEC",
            "priority": 3,
            "action": "Draft a diagnostic-only untouched-test replay spec for the frozen candidate, but do not execute it in Phase189.",
            "evidence_target": "test_replay_allowed_next remains 0 in Phase189",
        }
    )
    return pd.DataFrame(actions)


def build_gate_evaluation(phase188: pd.DataFrame, decision: pd.DataFrame, contract: pd.DataFrame, actions: pd.DataFrame) -> pd.DataFrame:
    interpretation_complete = as_int(metric_value(phase188, "phase188_interpretation_complete", 0))
    row = decision.iloc[0] if not decision.empty else {}
    return pd.DataFrame(
        [
            {"gate_id": "P189_PHASE188_INTERPRETATION_COMPLETE", "gate_pass": int(interpretation_complete == 1), "evidence": f"phase188_interpretation_complete={interpretation_complete}", "severity": "hard"},
            {"gate_id": "P189_DECISION_RECORDED", "gate_pass": int(not decision.empty and str(row.get("phase189_decision", "")) != ""), "evidence": f"decision_rows={len(decision)}", "severity": "hard"},
            {"gate_id": "P189_BREADTH_DATE_WARNINGS_ACKNOWLEDGED", "gate_pass": int(as_int(row.get("breadth_warning", 1)) == 1 or as_int(row.get("date_count_warning", 1)) == 1), "evidence": f"breadth_warning={row.get('breadth_warning', '')}; date_count_warning={row.get('date_count_warning', '')}", "severity": "hard"},
            {"gate_id": "P189_TEST_REPLAY_NOT_OPENED", "gate_pass": int(as_int(row.get("test_replay_allowed_next", 1)) == 0), "evidence": f"test_replay_allowed_next={row.get('test_replay_allowed_next', '')}", "severity": "hard"},
            {"gate_id": "P189_PROMOTION_AND_PAPER_LIVE_CLOSED", "gate_pass": int(as_int(row.get("promotion_allowed", 1)) == 0 and as_int(row.get("paper_or_live_acceptance_allowed", 1)) == 0), "evidence": f"promotion_allowed={row.get('promotion_allowed', '')}; paper_live={row.get('paper_or_live_acceptance_allowed', '')}", "severity": "hard"},
            {"gate_id": "P189_FUTURE_TEST_CONTRACT_DECLARED", "gate_pass": int(len(contract) >= 6 and contract["required_before_test_replay"].astype(int).eq(1).all()), "evidence": f"contract_rows={len(contract)}", "severity": "hard"},
            {"gate_id": "P189_REPAIR_ACTIONS_DECLARED", "gate_pass": int(len(actions) >= 2), "evidence": f"action_rows={len(actions)}", "severity": "hard"},
        ]
    )


def build_acceptance_summary(decision: pd.DataFrame, contract: pd.DataFrame, actions: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    row = decision.iloc[0] if not decision.empty else {}
    rows = [
        ("phase189_decision_rows", int(len(decision)), "Decision rows"),
        ("phase189_future_test_contract_rows", int(len(contract)), "Future test contract rows"),
        ("phase189_repair_action_rows", int(len(actions)), "Repair/action rows"),
        ("phase189_candidate_id", row.get("candidate_id", ""), "Candidate under decision"),
        ("phase189_decision", row.get("phase189_decision", ""), "Decision"),
        ("phase189_min_profile_net_bps_proxy_mean", row.get("min_profile_net_bps_proxy_mean", ""), "Minimum profile validation net bps from Phase188"),
        ("phase189_symbol_positive_fraction", row.get("symbol_positive_fraction", ""), "Phase188 symbol-positive fraction"),
        ("phase189_breadth_warning", row.get("breadth_warning", ""), "1 means breadth warning acknowledged"),
        ("phase189_date_count_warning", row.get("date_count_warning", ""), "1 means date-count warning acknowledged"),
        ("phase189_untouched_test_replay_precommit_allowed", row.get("untouched_test_replay_precommit_allowed", ""), "1 means current evidence allows a test precommit"),
        ("phase189_test_replay_allowed_next", 0, "No test replay opened by Phase189"),
        ("phase189_promotion_allowed", 0, "No promotion opened"),
        ("phase189_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
        ("phase189_gate_rows", int(len(gates)), "Gates evaluated"),
        ("phase189_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
        ("phase189_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase189_decision_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase189 decision completed"),
        ("phase189_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
        ("phase189_next_best_action", "build_phase190_additional_validation_breadth_or_diagnostic_test_spec_no_execution", "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, decision: pd.DataFrame, contract: pd.DataFrame, actions: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase189 Untouched-test Replay Precommit or Redesign Decision",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase189 decides whether the Phase187/188 sparse candidate may proceed toward untouched-test replay.",
        "Because Phase188 recorded breadth and date-count warnings, Phase189 defers test replay and records repair/precommit conditions.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Decision",
        "",
        _markdown_table(decision),
        "",
        "## Future Test Contract",
        "",
        _markdown_table(contract),
        "",
        "## Repair or Data Actions",
        "",
        _markdown_table(actions),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase189_test_replay_precommit_decision_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase189(phase187_dir: Path, phase188_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase188 = read_csv(phase188_dir / "phase188_sparse_candidate_interpretation_acceptance_summary.csv")
    interpretation = read_csv(phase188_dir / "phase188_sparse_candidate_interpretation.csv")
    decision = build_phase189_decision(phase188, interpretation)
    contract = build_future_test_contract(decision)
    actions = build_redesign_or_data_action(decision)
    gates = build_gate_evaluation(phase188, decision, contract, actions)
    acceptance = build_acceptance_summary(decision, contract, actions, gates)

    decision.to_csv(output_dir / "phase189_test_replay_or_redesign_decision.csv", index=False)
    contract.to_csv(output_dir / "phase189_future_test_replay_contract.csv", index=False)
    actions.to_csv(output_dir / "phase189_repair_or_data_actions.csv", index=False)
    gates.to_csv(output_dir / "phase189_test_replay_precommit_decision_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase189_test_replay_precommit_decision_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, decision, contract, actions, gates)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase189_untouched_test_replay_precommit_or_redesign_decision",
        **reproducibility_fields(
            artifact_id="phase189_test_replay_precommit_decision",
            generated_utc=generated_utc,
            inputs={
                "phase187_acceptance": str(phase187_dir / "phase187_cost_aware_sparse_candidate_acceptance_summary.csv"),
                "phase188_acceptance": str(phase188_dir / "phase188_sparse_candidate_interpretation_acceptance_summary.csv"),
                "phase188_interpretation": str(phase188_dir / "phase188_sparse_candidate_interpretation.csv"),
            },
            parameters={
                "test_replay_executed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_live_acceptance_allowed": 0,
            },
            outputs={
                "decision": str(output_dir / "phase189_test_replay_or_redesign_decision.csv"),
                "future_test_contract": str(output_dir / "phase189_future_test_replay_contract.csv"),
                "repair_actions": str(output_dir / "phase189_repair_or_data_actions.csv"),
                "gate_evaluation": str(output_dir / "phase189_test_replay_precommit_decision_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase189_test_replay_precommit_decision_acceptance_summary.csv"),
                "report": str(output_dir / "phase189_test_replay_precommit_decision_report.md"),
            },
            scenario_ids="phase189_untouched_test_replay_precommit_or_redesign_decision",
            cost_model_version="phase180_zerodha_equity_intraday_cost_bound_proxy",
            latency_model_version="phase180_retail_marketable_default_and_stressed_retail",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase189_test_replay_precommit_decision_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase187-dir", type=Path, default=DEFAULT_PHASE187_DIR)
    parser.add_argument("--phase188-dir", type=Path, default=DEFAULT_PHASE188_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase189(args.phase187_dir, args.phase188_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

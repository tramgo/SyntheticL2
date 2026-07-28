from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE187_DIR = Path("outputs/phase187")
DEFAULT_PHASE189_DIR = Path("outputs/phase189")
DEFAULT_PHASE190_DIR = Path("outputs/phase190")
DEFAULT_OUTPUT_DIR = Path("outputs/phase191")
FORBIDDEN_OUTPUTS = "test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim"


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


def stable_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def build_frozen_candidate_contract(selected: pd.DataFrame, phase189_decision: pd.DataFrame) -> pd.DataFrame:
    candidate_id = str(phase189_decision["candidate_id"].iloc[0]) if not phase189_decision.empty else "P187_TOP5_I85_S2p5_Z1_R100"
    rows = selected.loc[selected["candidate_id"].astype(str).eq(candidate_id)].copy()
    if rows.empty:
        raise ValueError(f"Frozen candidate {candidate_id} not found in Phase187 selected candidates")
    row = rows.iloc[0]
    payload = {
        "candidate_id": candidate_id,
        "imbalance_source": row["imbalance_source"],
        "min_abs_imbalance": float(row["min_abs_imbalance"]),
        "max_spread_bps": float(row["max_spread_bps"]),
        "min_abs_event_zscore": float(row["min_abs_event_zscore"]),
        "max_decision_rate": float(row["max_decision_rate"]),
        "allowed_latency_profiles": "P180_RETAIL_MARKETABLE_DEFAULT;P180_STRESSED_RETAIL",
    }
    return pd.DataFrame(
        [
            {
                **payload,
                "candidate_contract_hash": stable_hash(payload),
                "selection_source_phase": "phase187_train_only",
                "validation_interpretation_phase": "phase188",
                "test_precommit_decision_phase": "phase189",
                "diagnostic_spec_phase": "phase190",
                "may_change_before_test_replay": 0,
                "test_replay_execution_allowed_by_phase191": 0,
            }
        ]
    )


def build_future_command_contract(candidate_contract: pd.DataFrame) -> pd.DataFrame:
    row = candidate_contract.iloc[0]
    return pd.DataFrame(
        [
            {
                "command_contract_id": "P191_FUTURE_RUNNER",
                "future_runner": "scripts/run_phase192_diagnostic_test_replay.py",
                "allowed_phase": "phase192_or_later_only",
                "required_candidate_contract_hash": row["candidate_contract_hash"],
                "required_split_role": "test_untouched",
                "allowed_latency_profiles": "P180_RETAIL_MARKETABLE_DEFAULT;P180_STRESSED_RETAIL",
                "negative_controls_required": "shuffled_time;shuffled_symbol",
                "may_emit_test_result_in_phase191": 0,
                "may_emit_orders_or_fills": 0,
                "may_open_promotion": 0,
            }
        ]
    )


def build_abort_rules() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "abort_rule_id": "P191_HASH_MISMATCH",
                "condition": "candidate_contract_hash_at_execution != phase191_required_candidate_contract_hash",
                "action": "abort_before_reading_test_rows",
            },
            {
                "abort_rule_id": "P191_SPLIT_MISMATCH",
                "condition": "any_input_row_split_role != test_untouched",
                "action": "abort_and_mark_test_contaminated",
            },
            {
                "abort_rule_id": "P191_COST_LATENCY_MISSING",
                "condition": "any_net_metric_without_phase180_retail_or_stressed_profile",
                "action": "invalidate_result",
            },
            {
                "abort_rule_id": "P191_NEGATIVE_CONTROLS_MISSING",
                "condition": "missing_shuffled_time_or_shuffled_symbol_control",
                "action": "block_interpretation",
            },
            {
                "abort_rule_id": "P191_PROMOTION_ATTEMPT",
                "condition": "paper_live_acceptance_or_promotion_opened_from_diagnostic_test",
                "action": "invalidate_and_return_to_precommit",
            },
        ]
    )


def build_precommit_matrix(phase189: pd.DataFrame, phase190: pd.DataFrame, candidate_contract: pd.DataFrame, command_contract: pd.DataFrame, abort_rules: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "precommit_item": "phase189_decision_complete",
                "observed": as_int(metric_value(phase189, "phase189_decision_complete", 0)),
                "required": 1,
                "pass": int(as_int(metric_value(phase189, "phase189_decision_complete", 0)) == 1),
            },
            {
                "precommit_item": "phase190_diagnostic_spec_written",
                "observed": as_int(metric_value(phase190, "phase190_decision_complete", 0)),
                "required": 1,
                "pass": int(as_int(metric_value(phase190, "phase190_decision_complete", 0)) == 1),
            },
            {
                "precommit_item": "candidate_frozen",
                "observed": int(not candidate_contract.empty and candidate_contract["may_change_before_test_replay"].astype(int).eq(0).all()),
                "required": 1,
                "pass": int(not candidate_contract.empty and candidate_contract["may_change_before_test_replay"].astype(int).eq(0).all()),
            },
            {
                "precommit_item": "future_command_declared",
                "observed": len(command_contract),
                "required": 1,
                "pass": int(len(command_contract) == 1),
            },
            {
                "precommit_item": "abort_rules_declared",
                "observed": len(abort_rules),
                "required": 5,
                "pass": int(len(abort_rules) >= 5),
            },
            {
                "precommit_item": "phase191_test_execution_closed",
                "observed": 0,
                "required": 0,
                "pass": 1,
            },
        ]
    )


def build_gate_evaluation(matrix: pd.DataFrame, candidate_contract: pd.DataFrame, command_contract: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"gate_id": "P191_PREVIOUS_PRECOMMIT_CHAIN_PASS", "gate_pass": int(matrix["pass"].astype(int).all()), "evidence": f"matrix_pass_rows={int(matrix['pass'].astype(int).sum())}/{len(matrix)}", "severity": "hard"},
            {"gate_id": "P191_CANDIDATE_HASH_DECLARED", "gate_pass": int(not candidate_contract.empty and str(candidate_contract['candidate_contract_hash'].iloc[0]) != ""), "evidence": f"candidate_rows={len(candidate_contract)}", "severity": "hard"},
            {"gate_id": "P191_FUTURE_COMMAND_CONTRACT_DECLARED", "gate_pass": int(not command_contract.empty and command_contract["may_emit_test_result_in_phase191"].astype(int).eq(0).all()), "evidence": f"command_rows={len(command_contract)}", "severity": "hard"},
            {"gate_id": "P191_TEST_REPLAY_EXECUTION_CLOSED", "gate_pass": 1, "evidence": "test_replay_execution=0", "severity": "hard"},
            {"gate_id": "P191_PROMOTION_AND_PAPER_LIVE_CLOSED", "gate_pass": 1, "evidence": "promotion_allowed=0; paper_live_acceptance_allowed=0", "severity": "hard"},
        ]
    )


def build_acceptance_summary(candidate_contract: pd.DataFrame, command_contract: pd.DataFrame, abort_rules: pd.DataFrame, matrix: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    row = candidate_contract.iloc[0] if not candidate_contract.empty else {}
    rows = [
        ("phase191_candidate_contract_rows", int(len(candidate_contract)), "Frozen candidate contract rows"),
        ("phase191_future_command_contract_rows", int(len(command_contract)), "Future command contract rows"),
        ("phase191_abort_rule_rows", int(len(abort_rules)), "Abort rule rows"),
        ("phase191_precommit_matrix_rows", int(len(matrix)), "Precommit matrix rows"),
        ("phase191_candidate_id", row.get("candidate_id", ""), "Frozen candidate"),
        ("phase191_candidate_contract_hash", row.get("candidate_contract_hash", ""), "Frozen candidate hash"),
        ("phase191_gate_rows", int(len(gates)), "Gates evaluated"),
        ("phase191_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
        ("phase191_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase191_diagnostic_test_precommit_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means diagnostic precommit completed"),
        ("phase191_test_replay_execution", 0, "No test replay executed"),
        ("phase191_test_result_allowed", 0, "No test result emitted"),
        ("phase191_test_replay_allowed_next", 0, "No test replay opened by Phase191"),
        ("phase191_promotion_allowed", 0, "No promotion opened"),
        ("phase191_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
        ("phase191_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
        ("phase191_next_best_action", "either_add_real_validation_date_or_explicitly_authorize_phase192_diagnostic_test_replay", "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, candidate_contract: pd.DataFrame, command_contract: pd.DataFrame, abort_rules: pd.DataFrame, matrix: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase191 Diagnostic Test Replay Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase191 freezes the diagnostic-test replay contract but does not execute test replay.",
        "The candidate, command contract and abort rules are explicit so any later diagnostic test run cannot silently reselect or promote.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Frozen Candidate Contract",
        "",
        _markdown_table(candidate_contract),
        "",
        "## Future Command Contract",
        "",
        _markdown_table(command_contract),
        "",
        "## Abort Rules",
        "",
        _markdown_table(abort_rules),
        "",
        "## Precommit Matrix",
        "",
        _markdown_table(matrix),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase191_diagnostic_test_replay_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase191(phase187_dir: Path, phase189_dir: Path, phase190_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    selected = read_csv(phase187_dir / "phase187_train_selected_candidates.csv")
    phase189 = read_csv(phase189_dir / "phase189_test_replay_precommit_decision_acceptance_summary.csv")
    phase189_decision = read_csv(phase189_dir / "phase189_test_replay_or_redesign_decision.csv")
    phase190 = read_csv(phase190_dir / "phase190_validation_breadth_or_diagnostic_test_spec_acceptance_summary.csv")

    candidate_contract = build_frozen_candidate_contract(selected, phase189_decision)
    command_contract = build_future_command_contract(candidate_contract)
    abort_rules = build_abort_rules()
    matrix = build_precommit_matrix(phase189, phase190, candidate_contract, command_contract, abort_rules)
    gates = build_gate_evaluation(matrix, candidate_contract, command_contract)
    acceptance = build_acceptance_summary(candidate_contract, command_contract, abort_rules, matrix, gates)

    candidate_contract.to_csv(output_dir / "phase191_frozen_candidate_contract.csv", index=False)
    command_contract.to_csv(output_dir / "phase191_future_command_contract.csv", index=False)
    abort_rules.to_csv(output_dir / "phase191_abort_rules.csv", index=False)
    matrix.to_csv(output_dir / "phase191_precommit_matrix.csv", index=False)
    gates.to_csv(output_dir / "phase191_diagnostic_test_replay_precommit_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase191_diagnostic_test_replay_precommit_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, candidate_contract, command_contract, abort_rules, matrix, gates)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase191_diagnostic_test_replay_precommit_no_execution",
        **reproducibility_fields(
            artifact_id="phase191_diagnostic_test_replay_precommit",
            generated_utc=generated_utc,
            inputs={
                "phase187_selected": str(phase187_dir / "phase187_train_selected_candidates.csv"),
                "phase189_acceptance": str(phase189_dir / "phase189_test_replay_precommit_decision_acceptance_summary.csv"),
                "phase189_decision": str(phase189_dir / "phase189_test_replay_or_redesign_decision.csv"),
                "phase190_acceptance": str(phase190_dir / "phase190_validation_breadth_or_diagnostic_test_spec_acceptance_summary.csv"),
            },
            parameters={"test_replay_execution": 0, "promotion_allowed": 0},
            outputs={
                "candidate_contract": str(output_dir / "phase191_frozen_candidate_contract.csv"),
                "command_contract": str(output_dir / "phase191_future_command_contract.csv"),
                "abort_rules": str(output_dir / "phase191_abort_rules.csv"),
                "precommit_matrix": str(output_dir / "phase191_precommit_matrix.csv"),
                "gate_evaluation": str(output_dir / "phase191_diagnostic_test_replay_precommit_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase191_diagnostic_test_replay_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase191_diagnostic_test_replay_precommit_report.md"),
            },
            scenario_ids="phase191_diagnostic_test_replay_precommit_no_execution",
            cost_model_version="phase180_zerodha_equity_intraday_cost_bound_proxy",
            latency_model_version="phase180_retail_marketable_default_and_stressed_retail",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase191_diagnostic_test_replay_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase187-dir", type=Path, default=DEFAULT_PHASE187_DIR)
    parser.add_argument("--phase189-dir", type=Path, default=DEFAULT_PHASE189_DIR)
    parser.add_argument("--phase190-dir", type=Path, default=DEFAULT_PHASE190_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase191(args.phase187_dir, args.phase189_dir, args.phase190_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

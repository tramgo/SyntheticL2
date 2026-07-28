from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE189_DIR = Path("outputs/phase189")
DEFAULT_OUTPUT_DIR = Path("outputs/phase190")
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


def build_split_feasibility(label_inventory: pd.DataFrame) -> pd.DataFrame:
    if label_inventory.empty:
        return pd.DataFrame()
    grouped = (
        label_inventory.groupby(["split_role", "trade_date"], as_index=False)
        .agg(partitions=("symbol", "count"), rows=("rows", "sum"), symbols=("symbol", "nunique"))
        .sort_values(["split_role", "trade_date"])
    )
    grouped["usable_for_phase190_additional_validation"] = (
        grouped["split_role"].astype(str).eq("validation")
        | grouped["split_role"].astype(str).eq("train")
    ).astype(int)
    grouped["must_not_relabel_as_validation_in_phase190"] = grouped["split_role"].astype(str).eq("test_untouched").astype(int)
    return grouped


def build_validation_breadth_decision(split_feasibility: pd.DataFrame, phase189: pd.DataFrame) -> pd.DataFrame:
    validation_dates = sorted(split_feasibility.loc[split_feasibility["split_role"].astype(str).eq("validation"), "trade_date"].astype(str).unique().tolist())
    test_dates = sorted(split_feasibility.loc[split_feasibility["split_role"].astype(str).eq("test_untouched"), "trade_date"].astype(str).unique().tolist())
    train_dates = sorted(split_feasibility.loc[split_feasibility["split_role"].astype(str).eq("train"), "trade_date"].astype(str).unique().tolist())
    has_extra_validation = int(len(validation_dates) >= 2)
    test_replay_deferred = int(as_int(metric_value(phase189, "phase189_test_replay_allowed_next", 0)) == 0)
    return pd.DataFrame(
        [
            {
                "decision_id": "P190_VALIDATION_BREADTH_FEASIBILITY",
                "train_dates": ";".join(train_dates),
                "validation_dates": ";".join(validation_dates),
                "test_untouched_dates": ";".join(test_dates),
                "validation_date_count": len(validation_dates),
                "test_untouched_date_count": len(test_dates),
                "additional_validation_breadth_available_now": has_extra_validation,
                "may_relabel_test_as_validation": 0,
                "phase189_test_replay_deferred": test_replay_deferred,
                "phase190_decision": "diagnostic_test_spec_only_no_execution" if not has_extra_validation else "additional_validation_available_rerun_phase187_188_before_test",
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
            }
        ]
    )


def build_diagnostic_test_spec(phase189_decision: pd.DataFrame) -> pd.DataFrame:
    candidate_id = str(phase189_decision["candidate_id"].iloc[0]) if not phase189_decision.empty and "candidate_id" in phase189_decision.columns else "P187_TOP5_I85_S2p5_Z1_R100"
    return pd.DataFrame(
        [
            {
                "spec_id": "P190_FREEZE_CANDIDATE",
                "spec": f"Freeze candidate {candidate_id}; no threshold, profile, symbol, or date reselection may occur during diagnostic test replay.",
                "required_for_future_execution": 1,
            },
            {
                "spec_id": "P190_USE_ONLY_TEST_UNTOUCHED_SPLIT",
                "spec": "A later diagnostic test replay may read only rows whose existing split_role is test_untouched; it may not relabel test rows in Phase190.",
                "required_for_future_execution": 1,
            },
            {
                "spec_id": "P190_BIND_COST_LATENCY",
                "spec": "Bind Phase180 P180_RETAIL_MARKETABLE_DEFAULT and P180_STRESSED_RETAIL profiles before any net metric.",
                "required_for_future_execution": 1,
            },
            {
                "spec_id": "P190_NEGATIVE_CONTROLS",
                "spec": "Include shuffled-time and shuffled-symbol controls in the future diagnostic test replay interpretation.",
                "required_for_future_execution": 1,
            },
            {
                "spec_id": "P190_NO_PROMOTION_FROM_TEST",
                "spec": "A positive diagnostic test result may only open a later promotion-readiness audit, not paper/live acceptance.",
                "required_for_future_execution": 1,
            },
            {
                "spec_id": "P190_BREADTH_LIMITATION_REPORT",
                "spec": "Report that validation breadth was limited to one date and weak symbol-positive breadth before interpreting any future test result.",
                "required_for_future_execution": 1,
            },
        ]
    )


def build_data_actions(decision: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "action_id": "P190_DOWNLOAD_OR_DESIGNATE_MORE_VALIDATION_DATES",
                "priority": 1,
                "action": "Add at least one more non-test validation date from real receive-flow data, then rerun Phase187 and Phase188 before revisiting test replay.",
                "success_metric": "validation_date_count >= 2 with test_untouched_dates unchanged",
            },
            {
                "action_id": "P190_KEEP_TEST_UNTOUCHED",
                "priority": 2,
                "action": "Do not relabel the current test_untouched date as validation in this branch.",
                "success_metric": "may_relabel_test_as_validation=0 and test_replay_allowed_next=0",
            },
            {
                "action_id": "P190_OPTIONAL_DIAGNOSTIC_SPEC_REVIEW",
                "priority": 3,
                "action": "Review the diagnostic test replay spec, but do not execute it until a later explicit precommit phase allows it.",
                "success_metric": "test_replay_execution=0 in Phase190",
            },
        ]
    )


def build_gate_evaluation(phase189: pd.DataFrame, decision: pd.DataFrame, spec: pd.DataFrame, split_feasibility: pd.DataFrame) -> pd.DataFrame:
    phase189_complete = as_int(metric_value(phase189, "phase189_decision_complete", 0))
    row = decision.iloc[0] if not decision.empty else {}
    test_not_relabelled = int(not split_feasibility.empty and split_feasibility["must_not_relabel_as_validation_in_phase190"].astype(int).sum() >= 1)
    return pd.DataFrame(
        [
            {"gate_id": "P190_PHASE189_DECISION_COMPLETE", "gate_pass": int(phase189_complete == 1), "evidence": f"phase189_decision_complete={phase189_complete}", "severity": "hard"},
            {"gate_id": "P190_SPLIT_FEASIBILITY_RECORDED", "gate_pass": int(not split_feasibility.empty), "evidence": f"split_rows={len(split_feasibility)}", "severity": "hard"},
            {"gate_id": "P190_TEST_NOT_RELABELLED", "gate_pass": int(as_int(row.get("may_relabel_test_as_validation", 1)) == 0 and test_not_relabelled == 1), "evidence": f"may_relabel_test_as_validation={row.get('may_relabel_test_as_validation', '')}", "severity": "hard"},
            {"gate_id": "P190_DIAGNOSTIC_SPEC_DECLARED", "gate_pass": int(len(spec) >= 6 and spec["required_for_future_execution"].astype(int).eq(1).all()), "evidence": f"spec_rows={len(spec)}", "severity": "hard"},
            {"gate_id": "P190_TEST_REPLAY_NOT_EXECUTED", "gate_pass": int(as_int(row.get("test_replay_allowed_next", 1)) == 0), "evidence": f"test_replay_allowed_next={row.get('test_replay_allowed_next', '')}", "severity": "hard"},
            {"gate_id": "P190_PROMOTION_AND_PAPER_LIVE_CLOSED", "gate_pass": int(as_int(row.get("promotion_allowed", 1)) == 0 and as_int(row.get("paper_or_live_acceptance_allowed", 1)) == 0), "evidence": f"promotion_allowed={row.get('promotion_allowed', '')}; paper_live={row.get('paper_or_live_acceptance_allowed', '')}", "severity": "hard"},
        ]
    )


def build_acceptance_summary(decision: pd.DataFrame, split_feasibility: pd.DataFrame, spec: pd.DataFrame, actions: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates.loc[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["gate_pass"].astype(int).sum()) if not hard.empty else 0
    row = decision.iloc[0] if not decision.empty else {}
    rows = [
        ("phase190_split_feasibility_rows", int(len(split_feasibility)), "Split feasibility rows"),
        ("phase190_decision_rows", int(len(decision)), "Decision rows"),
        ("phase190_diagnostic_test_spec_rows", int(len(spec)), "Diagnostic test spec rows"),
        ("phase190_data_action_rows", int(len(actions)), "Data/action rows"),
        ("phase190_validation_date_count", row.get("validation_date_count", ""), "Current validation date count"),
        ("phase190_test_untouched_date_count", row.get("test_untouched_date_count", ""), "Current test_untouched date count"),
        ("phase190_additional_validation_breadth_available_now", row.get("additional_validation_breadth_available_now", ""), "1 means current artifacts have enough validation dates"),
        ("phase190_may_relabel_test_as_validation", 0, "Test rows cannot be relabelled as validation"),
        ("phase190_decision", row.get("phase190_decision", ""), "Decision"),
        ("phase190_gate_rows", int(len(gates)), "Gates evaluated"),
        ("phase190_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
        ("phase190_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
        ("phase190_test_replay_execution", 0, "No test replay executed"),
        ("phase190_test_replay_allowed_next", 0, "No test replay opened by Phase190"),
        ("phase190_promotion_allowed", 0, "No promotion opened"),
        ("phase190_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
        ("phase190_decision_complete", int(len(hard) > 0 and hard_pass == len(hard)), "1 means Phase190 completed"),
        ("phase190_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
        ("phase190_next_best_action", "add_real_validation_date_or_build_phase191_diagnostic_test_replay_precommit_no_execution", "Recommended next milestone"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, split_feasibility: pd.DataFrame, decision: pd.DataFrame, spec: pd.DataFrame, actions: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase190 Additional Validation Breadth or Diagnostic Test Spec",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase190 checks whether additional validation breadth exists without touching the test set.",
        "Current artifacts have one validation date and one test_untouched date, so Phase190 writes a diagnostic-only test replay spec and does not execute it.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Split Feasibility",
        "",
        _markdown_table(split_feasibility),
        "",
        "## Decision",
        "",
        _markdown_table(decision),
        "",
        "## Diagnostic Test Spec",
        "",
        _markdown_table(spec),
        "",
        "## Data Actions",
        "",
        _markdown_table(actions),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
    ]
    (output_dir / "phase190_validation_breadth_or_diagnostic_test_spec_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase190(phase181_dir: Path, phase189_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    phase189 = read_csv(phase189_dir / "phase189_test_replay_precommit_decision_acceptance_summary.csv")
    phase189_decision = read_csv(phase189_dir / "phase189_test_replay_or_redesign_decision.csv")
    split_feasibility = build_split_feasibility(label_inventory)
    decision = build_validation_breadth_decision(split_feasibility, phase189)
    spec = build_diagnostic_test_spec(phase189_decision)
    actions = build_data_actions(decision)
    gates = build_gate_evaluation(phase189, decision, spec, split_feasibility)
    acceptance = build_acceptance_summary(decision, split_feasibility, spec, actions, gates)

    split_feasibility.to_csv(output_dir / "phase190_split_feasibility.csv", index=False)
    decision.to_csv(output_dir / "phase190_validation_breadth_decision.csv", index=False)
    spec.to_csv(output_dir / "phase190_diagnostic_test_replay_spec.csv", index=False)
    actions.to_csv(output_dir / "phase190_data_actions.csv", index=False)
    gates.to_csv(output_dir / "phase190_validation_breadth_or_diagnostic_test_spec_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase190_validation_breadth_or_diagnostic_test_spec_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, split_feasibility, decision, spec, actions, gates)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase190_additional_validation_breadth_or_diagnostic_test_spec_no_execution",
        **reproducibility_fields(
            artifact_id="phase190_validation_breadth_or_diagnostic_test_spec",
            generated_utc=generated_utc,
            inputs={
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase189_acceptance": str(phase189_dir / "phase189_test_replay_precommit_decision_acceptance_summary.csv"),
                "phase189_decision": str(phase189_dir / "phase189_test_replay_or_redesign_decision.csv"),
            },
            parameters={"test_replay_execution": 0, "test_replay_allowed_next": 0, "may_relabel_test_as_validation": 0},
            outputs={
                "split_feasibility": str(output_dir / "phase190_split_feasibility.csv"),
                "decision": str(output_dir / "phase190_validation_breadth_decision.csv"),
                "diagnostic_test_spec": str(output_dir / "phase190_diagnostic_test_replay_spec.csv"),
                "data_actions": str(output_dir / "phase190_data_actions.csv"),
                "gate_evaluation": str(output_dir / "phase190_validation_breadth_or_diagnostic_test_spec_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase190_validation_breadth_or_diagnostic_test_spec_acceptance_summary.csv"),
                "report": str(output_dir / "phase190_validation_breadth_or_diagnostic_test_spec_report.md"),
            },
            scenario_ids="phase190_additional_validation_breadth_or_diagnostic_test_spec_no_execution",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase190_validation_breadth_or_diagnostic_test_spec_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase189-dir", type=Path, default=DEFAULT_PHASE189_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase190(args.phase181_dir, args.phase189_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

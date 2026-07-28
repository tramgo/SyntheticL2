from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE217_DIR = Path("outputs/phase217")
DEFAULT_OUTPUT_DIR = Path("outputs/phase218")
FORBIDDEN_OUTPUTS = "model_fit_execution;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_design_matrix_export;row_level_prediction_export"
NEXT_ACTION = "run_phase219_event_only_train_validation_model_fit_dry_run_no_replay_no_test"


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


def semicolon_join(values: pd.Series) -> str:
    return ";".join(sorted({str(v) for v in values.dropna().astype(str) if str(v)}))


def build_decision_ledger(phase217: pd.DataFrame, target_scope: pd.DataFrame, bindings: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    phase217_complete = as_int(metric_value(phase217, "phase217_event_only_design_matrix_precommit_complete", 0))
    target_rows = len(target_scope)
    binding_rows = len(bindings)
    control_rows = len(controls)
    event_rows = int(pd.to_numeric(target_scope["total_event_only_rows"], errors="coerce").fillna(0).sum()) if not target_scope.empty else 0
    min_target_rows = 3
    min_binding_rows = 18
    min_event_rows = 10000
    precommit_ok = int(phase217_complete == 1 and target_rows >= min_target_rows and binding_rows >= min_binding_rows and control_rows >= 3 and event_rows >= min_event_rows)
    return pd.DataFrame(
        [
            {
                "phase218_decision_id": "P218_PRECOMMIT_EVENT_ONLY_MODEL_FIT_DRY_RUN",
                "decision": "precommit_phase219_event_only_train_validation_model_fit_dry_run" if precommit_ok else "stop_or_redesign_event_only_model_fit",
                "phase217_complete": phase217_complete,
                "target_scope_rows": target_rows,
                "feature_binding_rows": binding_rows,
                "control_plan_rows": control_rows,
                "target_row_observation_scope": event_rows,
                "minimum_target_scope_rows": min_target_rows,
                "minimum_feature_binding_rows": min_binding_rows,
                "minimum_event_only_observations": min_event_rows,
                "model_fit_dry_run_precommitted_for_phase219": precommit_ok,
                "model_fit_execution_allowed_phase218": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_model_family_spec(target_scope: pd.DataFrame) -> pd.DataFrame:
    horizons = semicolon_join(target_scope["horizon_sec"]) if not target_scope.empty and "horizon_sec" in target_scope.columns else ""
    labels = semicolon_join(target_scope["label_name"]) if not target_scope.empty and "label_name" in target_scope.columns else ""
    return pd.DataFrame(
        [
            {
                "phase218_model_spec_id": "P218_EVENT_ONLY_BALANCED_LOGIT",
                "model_family": "class_weighted_regularized_logistic_classification",
                "target_labels": labels,
                "primary_horizons_sec": horizons,
                "feature_policy": "phase217_same_horizon_receive_flow_features_only",
                "sample_policy": "event_surprise_bucket_equals_1_train_fit_validation_score_only",
                "control_policy": "base_rate_and_event_time_shuffle_controls_required",
                "selection_policy": "validation_screening_only_test_sealed_no_replay",
                "allowed_next_phase_scope": "phase219_train_validation_fit_dry_run_only",
                "model_fit_execution_allowed_phase218": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
            },
            {
                "phase218_model_spec_id": "P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC",
                "model_family": "event_only_sparse_classification_diagnostic",
                "target_labels": labels,
                "primary_horizons_sec": horizons,
                "feature_policy": "phase217_same_horizon_receive_flow_features_only_nonnegative_transforms_where_required",
                "sample_policy": "event_surprise_bucket_equals_1_train_fit_validation_score_only",
                "control_policy": "base_rate_and_event_time_shuffle_controls_required",
                "selection_policy": "diagnostic_validation_only_test_sealed_no_replay",
                "allowed_next_phase_scope": "phase219_train_validation_fit_dry_run_only",
                "model_fit_execution_allowed_phase218": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
            },
            {
                "phase218_model_spec_id": "P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC",
                "model_family": "low_depth_tree_or_stump_diagnostic",
                "target_labels": labels,
                "primary_horizons_sec": horizons,
                "feature_policy": "phase217_same_horizon_receive_flow_features_only_depth_limited",
                "sample_policy": "event_surprise_bucket_equals_1_train_fit_validation_score_only",
                "control_policy": "base_rate_and_event_time_shuffle_controls_required",
                "selection_policy": "interpretability_only_no_threshold_selection_for_test",
                "allowed_next_phase_scope": "phase219_train_validation_fit_dry_run_only",
                "model_fit_execution_allowed_phase218": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
            },
        ]
    )


def build_target_contract(target_scope: pd.DataFrame) -> pd.DataFrame:
    if target_scope.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for row in target_scope.to_dict("records"):
        rows.append(
            {
                "phase218_target_contract_id": str(row.get("phase217_target_scope_id", "")).replace("P217_SCOPE_", "P218_TARGET_"),
                "phase217_target_scope_id": row.get("phase217_target_scope_id", ""),
                "label_name": row.get("label_name", ""),
                "horizon_sec": as_int(row.get("horizon_sec", 0)),
                "train_event_only_rows": as_int(row.get("train_event_only_rows", 0)),
                "validation_event_only_rows": as_int(row.get("validation_event_only_rows", 0)),
                "total_event_only_rows": as_int(row.get("total_event_only_rows", 0)),
                "positive_rate_min": row.get("positive_rate_min", ""),
                "positive_rate_max": row.get("positive_rate_max", ""),
                "eligible_for_phase219_fit_dry_run": as_int(row.get("allowed_for_design_matrix_contract", 0)),
                "sealed_test_rows_used": 0,
                "model_fit_execution_allowed_phase218": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_feature_contract(bindings: pd.DataFrame) -> pd.DataFrame:
    if bindings.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    group_cols = ["phase206_feature_id", "feature_family", "horizon_sec", "required_columns", "present_columns"]
    for keys, part in bindings.groupby(group_cols, dropna=False, sort=True):
        feature_id, family, horizon, required, present = keys
        rows.append(
            {
                "phase218_feature_contract_id": f"P218_{feature_id}_H{as_int(horizon)}s",
                "phase206_feature_id": feature_id,
                "feature_family": family,
                "horizon_sec": as_int(horizon),
                "required_columns": required,
                "present_columns": present,
                "target_bindings": len(part),
                "same_horizon_binding": int(pd.to_numeric(part["same_horizon_binding"], errors="coerce").fillna(0).min()),
                "feature_available": int(pd.to_numeric(part["feature_available"], errors="coerce").fillna(0).min()),
                "eligible_for_phase219_fit_dry_run": 1,
                "model_fit_execution_allowed_phase218": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_control_contract(controls: pd.DataFrame) -> pd.DataFrame:
    if controls.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for row in controls.to_dict("records"):
        rows.append(
            {
                "phase218_control_id": str(row.get("phase217_control_id", "")).replace("P217_", "P218_"),
                "control_type": row.get("control_type", ""),
                "contract": row.get("phase216_requirement", ""),
                "required_for_phase219_fit_dry_run": 1,
                "target_scope_rows_covered": as_int(row.get("target_scope_rows_covered", 0)),
                "event_only_rows_covered": as_int(row.get("event_only_rows_covered", 0)),
                "sealed_test_rows_used": 0,
                "model_fit_execution_allowed_phase218": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_phase219_work_order(decision: pd.DataFrame, model_specs: pd.DataFrame, target_contract: pd.DataFrame, feature_contract: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    dry_run_precommitted = as_int(decision["model_fit_dry_run_precommitted_for_phase219"].iloc[0]) if not decision.empty else 0
    return pd.DataFrame(
        [
            {
                "phase219_work_order_id": "P219_EVENT_ONLY_TRAIN_VALIDATION_MODEL_FIT_DRY_RUN",
                "work_order": "Execute only a train/validation event-only model-fit dry run using Phase218 specs and controls; emit validation diagnostics, no strategy replay, no sealed test, no promotion.",
                "model_fit_dry_run_precommitted": dry_run_precommitted,
                "model_spec_rows": len(model_specs),
                "target_contract_rows": len(target_contract),
                "feature_contract_rows": len(feature_contract),
                "control_contract_rows": len(controls),
                "allowed_next_scope": "train_validation_model_fit_dry_run_no_replay_no_test",
                "model_fit_execution_allowed_phase219": dry_run_precommitted,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase218": 0,
                "allowed_in_phase218": 0,
                "rationale": "Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(
    phase217: pd.DataFrame,
    decision: pd.DataFrame,
    model_specs: pd.DataFrame,
    target_contract: pd.DataFrame,
    feature_contract: pd.DataFrame,
    controls: pd.DataFrame,
    work_order: pd.DataFrame,
    forbidden: pd.DataFrame,
) -> pd.DataFrame:
    phase217_complete = as_int(metric_value(phase217, "phase217_event_only_design_matrix_precommit_complete", 0))
    dry_run_precommitted = as_int(decision["model_fit_dry_run_precommitted_for_phase219"].iloc[0]) if not decision.empty else 0
    eligible_targets = int(pd.to_numeric(target_contract["eligible_for_phase219_fit_dry_run"], errors="coerce").fillna(0).sum()) if not target_contract.empty else 0
    eligible_features = int(pd.to_numeric(feature_contract["eligible_for_phase219_fit_dry_run"], errors="coerce").fillna(0).sum()) if not feature_contract.empty else 0
    required_controls = int(pd.to_numeric(controls["required_for_phase219_fit_dry_run"], errors="coerce").fillna(0).sum()) if not controls.empty else 0
    forbidden_emitted = int(pd.to_numeric(forbidden["emitted_in_phase218"], errors="coerce").fillna(0).sum()) if not forbidden.empty else 1
    phase218_execution_flags = 0
    for frame in [decision, model_specs, target_contract, feature_contract, controls]:
        for col in ["model_fit_execution_allowed_phase218", "strategy_replay_allowed", "test_replay_allowed_next", "promotion_allowed", "paper_or_live_acceptance_allowed", "profitability_claim_allowed"]:
            if not frame.empty and col in frame.columns:
                phase218_execution_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P218_PHASE217_COMPLETE", phase217_complete == 1, f"phase217_complete={phase217_complete}", "hard"),
            ("P218_DECISION_RECORDED", len(decision) == 1 and dry_run_precommitted == 1, f"decision_rows={len(decision)}; dry_run_precommitted={dry_run_precommitted}", "hard"),
            ("P218_MODEL_SPECS_RECORDED", len(model_specs) >= 3, f"model_specs={len(model_specs)}", "hard"),
            ("P218_TARGET_AND_FEATURE_CONTRACTS_RECORDED", len(target_contract) >= 3 and eligible_targets == len(target_contract) and len(feature_contract) >= 6 and eligible_features == len(feature_contract), f"targets={len(target_contract)}; eligible_targets={eligible_targets}; features={len(feature_contract)}; eligible_features={eligible_features}", "hard"),
            ("P218_CONTROLS_RECORDED", len(controls) == 3 and required_controls == 3, f"controls={len(controls)}; required={required_controls}", "hard"),
            ("P218_PHASE219_WORK_ORDER_RECORDED", len(work_order) == 1 and as_int(work_order["model_fit_execution_allowed_phase219"].iloc[0]) == 1, f"work_order={len(work_order)}; phase219_fit_allowed={as_int(work_order['model_fit_execution_allowed_phase219'].iloc[0]) if not work_order.empty else 0}", "hard"),
            ("P218_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and phase218_execution_flags == 0, f"forbidden_emitted={forbidden_emitted}; phase218_execution_flags={phase218_execution_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(decision: pd.DataFrame, model_specs: pd.DataFrame, target_contract: pd.DataFrame, feature_contract: pd.DataFrame, controls: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    dry_run_precommitted = as_int(decision["model_fit_dry_run_precommitted_for_phase219"].iloc[0]) if not decision.empty else 0
    return pd.DataFrame(
        [
            ("phase218_decision_rows", len(decision), "Decision ledger rows"),
            ("phase218_model_spec_rows", len(model_specs), "Model-family specification rows"),
            ("phase218_target_contract_rows", len(target_contract), "Event-only target contract rows"),
            ("phase218_feature_contract_rows", len(feature_contract), "Event-only feature contract rows"),
            ("phase218_control_contract_rows", len(controls), "Control contract rows"),
            ("phase218_phase219_work_order_rows", len(work_order), "Phase219 work-order rows"),
            ("phase218_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase218_gate_rows", len(gates), "Gates evaluated"),
            ("phase218_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase218_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase218_event_only_model_fit_precommit_or_stop_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase218 completed"),
            ("phase218_model_fit_dry_run_precommitted_for_phase219", dry_run_precommitted, "1 means Phase219 may execute train/validation fit dry run"),
            ("phase218_model_fit_execution_allowed", 0, "No model fit execution in Phase218"),
            ("phase218_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase218_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase218_promotion_allowed", 0, "No promotion opened"),
            ("phase218_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase218_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase218_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase218_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase218 Event-only Model-fit Precommit-or-stop",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase218 decides whether the Phase217 event-only design-matrix contract is strong enough to precommit a train/validation model-fit dry run.",
        "It precommits a Phase219 dry run but does not execute model fitting, emit predictions, run replay, use sealed test, promote anything, or make profitability claims.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase218_event_only_model_fit_precommit_or_stop_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase218(phase217_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase217 = read_csv(phase217_dir / "phase217_design_matrix_acceptance_summary.csv")
    target_scope = read_csv(phase217_dir / "phase217_event_only_target_scope.csv")
    bindings = read_csv(phase217_dir / "phase217_same_horizon_feature_bindings.csv")
    controls217 = read_csv(phase217_dir / "phase217_control_plan.csv")

    decision = build_decision_ledger(phase217, target_scope, bindings, controls217)
    model_specs = build_model_family_spec(target_scope)
    target_contract = build_target_contract(target_scope)
    feature_contract = build_feature_contract(bindings)
    controls = build_control_contract(controls217)
    work_order = build_phase219_work_order(decision, model_specs, target_contract, feature_contract, controls)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase217, decision, model_specs, target_contract, feature_contract, controls, work_order, forbidden)
    acceptance = build_acceptance(decision, model_specs, target_contract, feature_contract, controls, work_order, forbidden, gates)

    decision.to_csv(output_dir / "phase218_model_fit_precommit_decision.csv", index=False)
    model_specs.to_csv(output_dir / "phase218_model_family_spec.csv", index=False)
    target_contract.to_csv(output_dir / "phase218_event_only_target_contract.csv", index=False)
    feature_contract.to_csv(output_dir / "phase218_event_only_feature_contract.csv", index=False)
    controls.to_csv(output_dir / "phase218_control_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase218_phase219_work_order.csv", index=False)
    forbidden.to_csv(output_dir / "phase218_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase218_model_fit_precommit_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase218_model_fit_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Decision Ledger": decision,
            "Model Family Spec": model_specs,
            "Event-only Target Contract": target_contract,
            "Event-only Feature Contract": feature_contract,
            "Control Contract": controls,
            "Phase219 Work Order": work_order,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase218_event_only_model_fit_precommit_or_stop_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase218_event_only_model_fit_precommit_or_stop",
            generated_utc=generated,
            inputs={
                "phase217_acceptance": str(phase217_dir / "phase217_design_matrix_acceptance_summary.csv"),
                "phase217_target_scope": str(phase217_dir / "phase217_event_only_target_scope.csv"),
                "phase217_feature_bindings": str(phase217_dir / "phase217_same_horizon_feature_bindings.csv"),
                "phase217_controls": str(phase217_dir / "phase217_control_plan.csv"),
            },
            parameters={
                "minimum_target_scope_rows": "3",
                "minimum_feature_binding_rows": "18",
                "minimum_event_only_observations": "10000",
                "model_fit_execution_allowed_phase218": "0",
                "phase219_model_fit_dry_run_precommit_allowed": "1",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "decision": str(output_dir / "phase218_model_fit_precommit_decision.csv"),
                "model_specs": str(output_dir / "phase218_model_family_spec.csv"),
                "target_contract": str(output_dir / "phase218_event_only_target_contract.csv"),
                "feature_contract": str(output_dir / "phase218_event_only_feature_contract.csv"),
                "controls": str(output_dir / "phase218_control_contract.csv"),
                "work_order": str(output_dir / "phase218_phase219_work_order.csv"),
                "forbidden": str(output_dir / "phase218_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase218_model_fit_precommit_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase218_model_fit_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase218_event_only_model_fit_precommit_or_stop_report.md"),
            },
            scenario_ids="phase218_event_only_model_fit_precommit_or_stop_no_replay_no_test",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase218_model_fit_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase218 event-only model-fit precommit-or-stop without execution/replay/test.")
    parser.add_argument("--phase217-dir", type=Path, default=DEFAULT_PHASE217_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase218(args.phase217_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

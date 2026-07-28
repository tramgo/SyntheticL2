from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE207_DIR = Path("outputs/phase207")
DEFAULT_PHASE214_DIR = Path("outputs/phase214")
DEFAULT_PHASE216_DIR = Path("outputs/phase216")
DEFAULT_OUTPUT_DIR = Path("outputs/phase217")
FORBIDDEN_OUTPUTS = "model_fit;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_design_matrix_export;row_level_prediction_export"
NEXT_ACTION = "run_phase218_event_only_model_fit_precommit_or_stop_no_replay_no_test"


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


def build_target_scope(allowlist: pd.DataFrame, split_balance: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for target in allowlist.to_dict("records"):
        horizon = as_int(target.get("horizon_sec", 0))
        split_rows = split_balance[pd.to_numeric(split_balance["horizon_sec"], errors="coerce").fillna(-1).astype(int).eq(horizon)] if not split_balance.empty else pd.DataFrame()
        train_event_rows = int(pd.to_numeric(split_rows.loc[split_rows["split_role"].astype(str).eq("train"), "event_surprise_rows"], errors="coerce").fillna(0).sum()) if not split_rows.empty else 0
        validation_event_rows = int(pd.to_numeric(split_rows.loc[split_rows["split_role"].astype(str).eq("validation"), "event_surprise_rows"], errors="coerce").fillna(0).sum()) if not split_rows.empty else 0
        rows.append(
            {
                "phase217_target_scope_id": str(target.get("phase216_target_id", "")).replace("P216_", "P217_SCOPE_"),
                "phase216_target_id": target.get("phase216_target_id", ""),
                "label_name": target.get("label_name", ""),
                "horizon_sec": horizon,
                "event_only_filter": target.get("event_only_filter", "event_surprise_bucket == 1"),
                "train_event_only_rows": train_event_rows,
                "validation_event_only_rows": validation_event_rows,
                "total_event_only_rows": train_event_rows + validation_event_rows,
                "positive_rate_min": target.get("positive_rate_min", ""),
                "positive_rate_max": target.get("positive_rate_max", ""),
                "split_roles_required": "train;validation",
                "sealed_test_rows_used": 0,
                "allowed_for_design_matrix_contract": int(train_event_rows > 0 and validation_event_rows > 0),
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_feature_binding(allowlist: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for target in allowlist.to_dict("records"):
        horizon = as_int(target.get("horizon_sec", 0))
        same_horizon = features[pd.to_numeric(features["horizon_sec"], errors="coerce").fillna(-1).astype(int).eq(horizon)] if not features.empty else pd.DataFrame()
        same_horizon = same_horizon[pd.to_numeric(same_horizon["feature_available"], errors="coerce").fillna(0).astype(int).eq(1)] if not same_horizon.empty else same_horizon
        for feature in same_horizon.to_dict("records"):
            rows.append(
                {
                    "phase217_binding_id": f"P217_BIND_{target.get('phase216_target_id', '')}_{feature.get('phase206_feature_id', '')}_H{horizon}s",
                    "phase216_target_id": target.get("phase216_target_id", ""),
                    "label_name": target.get("label_name", ""),
                    "horizon_sec": horizon,
                    "phase206_feature_id": feature.get("phase206_feature_id", ""),
                    "feature_family": feature.get("feature_family", ""),
                    "required_columns": feature.get("required_columns", ""),
                    "present_columns": feature.get("present_columns", ""),
                    "present_column_count": as_int(feature.get("present_column_count", 0)),
                    "same_horizon_binding": 1,
                    "target_columns_excluded_from_features": 1,
                    "feature_available": as_int(feature.get("feature_available", 0)),
                    "model_fit_allowed_now": 0,
                    "strategy_replay_allowed": 0,
                    "test_replay_allowed_next": 0,
                }
            )
    return pd.DataFrame(rows)


def build_design_matrix_contract(target_scope: pd.DataFrame, bindings: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    target_rows = len(target_scope)
    binding_rows = len(bindings)
    event_rows = int(pd.to_numeric(target_scope["total_event_only_rows"], errors="coerce").fillna(0).sum()) if not target_scope.empty else 0
    return pd.DataFrame(
        [
            {
                "phase217_contract_id": "P217_EVENT_ONLY_DESIGN_MATRIX_CONTRACT",
                "contract": "Build only an event-only train/validation design-matrix contract using Phase216 allowed targets, same-horizon Phase207 features, and event_surprise_bucket == 1 rows; do not export row-level matrices or fit models in Phase217.",
                "target_scope_rows": target_rows,
                "feature_binding_rows": binding_rows,
                "required_control_rows": len(controls),
                "target_row_observation_scope": event_rows,
                "row_level_design_matrix_export_allowed": 0,
                "sealed_test_policy": "inventory_only_zero_rows_used",
                "threshold_widening_allowed": 0,
                "model_fit_allowed_now": 0,
                "model_fit_allowed_next": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_control_plan(phase216_controls: pd.DataFrame, target_scope: pd.DataFrame) -> pd.DataFrame:
    total_targets = len(target_scope)
    event_rows = int(pd.to_numeric(target_scope["total_event_only_rows"], errors="coerce").fillna(0).sum()) if not target_scope.empty else 0
    rows: list[dict[str, Any]] = []
    for control in phase216_controls.to_dict("records"):
        control_type = str(control.get("control_type", ""))
        rows.append(
            {
                "phase217_control_id": str(control.get("phase216_control_id", "")).replace("P216_", "P217_"),
                "control_type": control_type,
                "phase216_requirement": control.get("requirement", ""),
                "target_scope_rows_covered": total_targets,
                "event_only_rows_covered": event_rows if control_type != "sealed_test" else 0,
                "required_for_future_model_fit_precommit": 1,
                "implemented_as_contract_only": 1,
                "sealed_test_rows_used": 0,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_phase218_work_order(contract: pd.DataFrame, target_scope: pd.DataFrame, bindings: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    contract_ok = int(not contract.empty and as_int(contract["row_level_design_matrix_export_allowed"].iloc[0]) == 0)
    return pd.DataFrame(
        [
            {
                "phase218_work_order_id": "P218_EVENT_ONLY_MODEL_FIT_PRECOMMIT_OR_STOP",
                "work_order": "Decide whether the Phase217 event-only design-matrix contract is strong enough to precommit a train/validation model fit, or stop/redesign without replay.",
                "phase217_contract_rows": len(contract),
                "target_scope_rows": len(target_scope),
                "feature_binding_rows": len(bindings),
                "control_plan_rows": len(controls),
                "phase217_contract_ok": contract_ok,
                "allowed_next_scope": "model_fit_precommit_decision_only_no_strategy_replay_no_test",
                "model_fit_execution_allowed_next": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        ]
    )


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase217": 0,
                "allowed_in_phase217": 0,
                "rationale": "Phase217 is a design-matrix precommit and emits no row-level matrix, model, prediction, replay, order/fill/P&L, promotion, paper/live, or profitability artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(
    phase216: pd.DataFrame,
    allowlist: pd.DataFrame,
    target_scope: pd.DataFrame,
    bindings: pd.DataFrame,
    controls: pd.DataFrame,
    contract: pd.DataFrame,
    work_order: pd.DataFrame,
    forbidden: pd.DataFrame,
) -> pd.DataFrame:
    phase216_complete = as_int(metric_value(phase216, "phase216_event_surprise_event_only_target_precommit_complete", 0))
    allowed_targets = as_int(metric_value(phase216, "phase216_full_train_validation_target_rows", 0))
    target_scope_pass = int(pd.to_numeric(target_scope["allowed_for_design_matrix_contract"], errors="coerce").fillna(0).sum()) if not target_scope.empty else 0
    same_horizon = int(pd.to_numeric(bindings["same_horizon_binding"], errors="coerce").fillna(0).sum()) if not bindings.empty else 0
    available_bindings = int(pd.to_numeric(bindings["feature_available"], errors="coerce").fillna(0).sum()) if not bindings.empty else 0
    forbidden_emitted = int(pd.to_numeric(forbidden["emitted_in_phase217"], errors="coerce").fillna(0).sum()) if not forbidden.empty else 1
    replay_flags = 0
    for frame in [target_scope, bindings, controls, contract, work_order]:
        for col in ["model_fit_allowed_now", "model_fit_allowed_next", "model_fit_execution_allowed_next", "strategy_replay_allowed", "test_replay_allowed_next", "profitability_claim_allowed", "threshold_widening_allowed", "row_level_design_matrix_export_allowed"]:
            if not frame.empty and col in frame.columns:
                replay_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P217_PHASE216_COMPLETE", phase216_complete == 1, f"phase216_complete={phase216_complete}", "hard"),
            ("P217_ALLOWED_TARGETS_MATCH_PHASE216", len(target_scope) == len(allowlist) == allowed_targets and target_scope_pass == allowed_targets, f"allowlist={len(allowlist)}; target_scope={len(target_scope)}; phase216_allowed={allowed_targets}; target_scope_pass={target_scope_pass}", "hard"),
            ("P217_SAME_HORIZON_FEATURE_BINDINGS_RECORDED", len(bindings) > 0 and same_horizon == len(bindings) and available_bindings == len(bindings), f"bindings={len(bindings)}; same_horizon={same_horizon}; available={available_bindings}", "hard"),
            ("P217_REQUIRED_CONTROLS_RECORDED", len(controls) == 3, f"controls={len(controls)}", "hard"),
            ("P217_DESIGN_MATRIX_CONTRACT_RECORDED", len(contract) == 1 and as_int(contract['target_scope_rows'].iloc[0]) == len(target_scope) and as_int(contract['feature_binding_rows'].iloc[0]) == len(bindings), f"contract={len(contract)}; target_scope={len(target_scope)}; bindings={len(bindings)}", "hard"),
            ("P217_PHASE218_WORK_ORDER_RECORDED", len(work_order) == 1, f"work_order={len(work_order)}", "hard"),
            ("P217_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and replay_flags == 0, f"forbidden_emitted={forbidden_emitted}; replay_flags={replay_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(target_scope: pd.DataFrame, bindings: pd.DataFrame, controls: pd.DataFrame, contract: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase217_target_scope_rows", len(target_scope), "Event-only target scope rows"),
            ("phase217_feature_binding_rows", len(bindings), "Same-horizon target-feature binding rows"),
            ("phase217_control_plan_rows", len(controls), "Required control plan rows"),
            ("phase217_design_matrix_contract_rows", len(contract), "Design-matrix contract rows"),
            ("phase217_phase218_work_order_rows", len(work_order), "Phase218 work-order rows"),
            ("phase217_target_row_observation_scope", int(pd.to_numeric(target_scope["total_event_only_rows"], errors="coerce").fillna(0).sum()) if not target_scope.empty else 0, "Target-row event-only observations across allowed targets"),
            ("phase217_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase217_gate_rows", len(gates), "Gates evaluated"),
            ("phase217_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase217_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase217_event_only_design_matrix_precommit_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase217 completed"),
            ("phase217_row_level_design_matrix_export_allowed", 0, "No row-level design matrix export opened"),
            ("phase217_model_fit_allowed_next", 0, "No model fit opened"),
            ("phase217_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase217_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase217_promotion_allowed", 0, "No promotion opened"),
            ("phase217_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase217_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase217_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase217_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase217 Event-only Design-matrix Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase217 binds the Phase216 event-only target allowlist to same-horizon Phase207 receive-flow features.",
        "It records design-matrix scope and controls only; row-level matrix export, model fitting, replay, sealed test use, promotion, paper/live acceptance, and profitability claims remain closed.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase217_event_only_design_matrix_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase217(phase207_dir: Path, phase214_dir: Path, phase216_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase216 = read_csv(phase216_dir / "phase216_event_only_target_acceptance_summary.csv")
    allowlist = read_csv(phase216_dir / "phase216_event_only_target_allowlist.csv")
    phase216_controls = read_csv(phase216_dir / "phase216_control_contract.csv")
    features = read_csv(phase207_dir / "phase207_allowed_feature_matrix.csv")
    split_balance = read_csv(phase214_dir / "phase214_split_balance_summary.csv")

    target_scope = build_target_scope(allowlist, split_balance)
    bindings = build_feature_binding(allowlist, features)
    controls = build_control_plan(phase216_controls, target_scope)
    contract = build_design_matrix_contract(target_scope, bindings, controls)
    work_order = build_phase218_work_order(contract, target_scope, bindings, controls)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase216, allowlist, target_scope, bindings, controls, contract, work_order, forbidden)
    acceptance = build_acceptance(target_scope, bindings, controls, contract, work_order, forbidden, gates)

    target_scope.to_csv(output_dir / "phase217_event_only_target_scope.csv", index=False)
    bindings.to_csv(output_dir / "phase217_same_horizon_feature_bindings.csv", index=False)
    controls.to_csv(output_dir / "phase217_control_plan.csv", index=False)
    contract.to_csv(output_dir / "phase217_design_matrix_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase217_phase218_work_order.csv", index=False)
    forbidden.to_csv(output_dir / "phase217_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase217_design_matrix_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase217_design_matrix_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Event-only Target Scope": target_scope,
            "Same-horizon Feature Bindings": bindings,
            "Control Plan": controls,
            "Design-matrix Contract": contract,
            "Phase218 Work Order": work_order,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase217_event_only_design_matrix_precommit_no_model_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase217_event_only_design_matrix_precommit",
            generated_utc=generated,
            inputs={
                "phase207_features": str(phase207_dir / "phase207_allowed_feature_matrix.csv"),
                "phase214_split_balance": str(phase214_dir / "phase214_split_balance_summary.csv"),
                "phase216_acceptance": str(phase216_dir / "phase216_event_only_target_acceptance_summary.csv"),
                "phase216_allowlist": str(phase216_dir / "phase216_event_only_target_allowlist.csv"),
                "phase216_controls": str(phase216_dir / "phase216_control_contract.csv"),
            },
            parameters={
                "event_only_filter": "event_surprise_bucket == 1",
                "same_horizon_feature_binding": "1",
                "row_level_design_matrix_export_allowed": "0",
                "model_fit_allowed": "0",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "target_scope": str(output_dir / "phase217_event_only_target_scope.csv"),
                "feature_bindings": str(output_dir / "phase217_same_horizon_feature_bindings.csv"),
                "controls": str(output_dir / "phase217_control_plan.csv"),
                "contract": str(output_dir / "phase217_design_matrix_contract.csv"),
                "work_order": str(output_dir / "phase217_phase218_work_order.csv"),
                "forbidden": str(output_dir / "phase217_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase217_design_matrix_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase217_design_matrix_acceptance_summary.csv"),
                "report": str(output_dir / "phase217_event_only_design_matrix_precommit_report.md"),
            },
            scenario_ids="phase217_event_only_design_matrix_precommit_no_model_no_replay_no_test",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase217_design_matrix_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase217 event-only design-matrix precommit without model/replay/test.")
    parser.add_argument("--phase207-dir", type=Path, default=DEFAULT_PHASE207_DIR)
    parser.add_argument("--phase214-dir", type=Path, default=DEFAULT_PHASE214_DIR)
    parser.add_argument("--phase216-dir", type=Path, default=DEFAULT_PHASE216_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase217(args.phase207_dir, args.phase214_dir, args.phase216_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

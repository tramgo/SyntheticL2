from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE212_DIR = Path("outputs/phase212")
DEFAULT_OUTPUT_DIR = Path("outputs/phase213")
SELECTED_SOURCE_ID = "P213_EVENT_SURPRISE_CONDITIONAL_LABEL_SOURCE"
FORBIDDEN_OUTPUTS = "model_fit;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase214_event_surprise_label_contract_materialization_no_model_no_replay_no_test"


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


def build_source_selection(redesign: pd.DataFrame, action: pd.DataFrame) -> pd.DataFrame:
    ranked = action.sort_values("phase212_action_rank") if not action.empty and "phase212_action_rank" in action.columns else action
    selected_redesign_id = str(ranked.iloc[0]["phase212_redesign_id"]) if not ranked.empty else "P212_EVENT_SURPRISE_CONDITIONAL_LABEL_SOURCE"
    selected = redesign[redesign["phase212_redesign_id"].astype(str).eq(selected_redesign_id)] if not redesign.empty else pd.DataFrame()
    record = selected.iloc[0].to_dict() if not selected.empty else {}
    return pd.DataFrame(
        [
            {
                "phase213_source_id": SELECTED_SOURCE_ID,
                "phase212_redesign_id": selected_redesign_id,
                "selection_rank": 1,
                "selected_for_phase214": 1,
                "source_type": "material_new_conditional_label_source",
                "source_theme": record.get("redesign_theme", "material_new_label_source"),
                "source_description": record.get("precommit_action", "Define conditional event-surprise labels."),
                "why_materially_different": record.get("why_materially_different", "Targets control-like/base-rate failures with conditional labels."),
                "phase211_failure_addressed": "control_like_mse;weak_global_correlation;base_rate_accuracy",
                "non_selected_alternatives_preserved": ";".join(redesign.loc[~redesign["phase212_redesign_id"].astype(str).eq(selected_redesign_id), "phase212_redesign_id"].astype(str).tolist()) if not redesign.empty else "",
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "profitability_claim_allowed": 0,
            }
        ]
    )


def build_conditional_label_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase213_label_contract_id": "P213_EVENT_SURPRISE_UP_LABEL",
                "label_name": "event_surprise_up_conditional_label",
                "label_definition": "Future mid-return exceeds same-symbol/date liquidity-regime conditional baseline after a receive-event surprise bucket.",
                "conditioning_fields": "symbol;trade_date;horizon_sec;spread_regime;liquidity_regime;receive_event_rate_zscore_bucket",
                "balance_requirement": "validation_positive_rate_between_0p35_and_0p65_or_abstain",
                "control_requirement": "shuffled_target_control;shuffled_event_time_control;base_rate_accuracy_control",
                "materialization_allowed_next": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
            },
            {
                "phase213_label_contract_id": "P213_EVENT_SURPRISE_DOWN_LABEL",
                "label_name": "event_surprise_down_conditional_label",
                "label_definition": "Future mid-return underperforms same-symbol/date liquidity-regime conditional baseline after a receive-event surprise bucket.",
                "conditioning_fields": "symbol;trade_date;horizon_sec;spread_regime;liquidity_regime;receive_event_rate_zscore_bucket",
                "balance_requirement": "validation_positive_rate_between_0p35_and_0p65_or_abstain",
                "control_requirement": "shuffled_target_control;shuffled_event_time_control;base_rate_accuracy_control",
                "materialization_allowed_next": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
            },
            {
                "phase213_label_contract_id": "P213_EVENT_SURPRISE_VOL_EXPANSION_LABEL",
                "label_name": "event_surprise_vol_expansion_conditional_label",
                "label_definition": "Future absolute return or spread expansion exceeds conditional baseline after receive-event surprise.",
                "conditioning_fields": "symbol;trade_date;horizon_sec;spread_regime;liquidity_regime;receive_event_rate_zscore_bucket",
                "balance_requirement": "validation_positive_rate_between_0p35_and_0p65_or_abstain",
                "control_requirement": "shuffled_target_control;shuffled_event_time_control;base_rate_accuracy_control",
                "materialization_allowed_next": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
            },
        ]
    )


def build_feature_requirement_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase213_feature_requirement_id": "P213_RECEIVE_EVENT_SURPRISE_BUCKETS",
                "required_feature_source": "phase176_receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days",
                "requirement": "Create causal receive-event surprise buckets from prior-date baselines only.",
                "leakage_control": "bucket assignment must use only current/past receive timestamps and prior-date baseline state",
                "required_for_phase214": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
            },
            {
                "phase213_feature_requirement_id": "P213_LIQUIDITY_REGIME_BUCKETS",
                "required_feature_source": "spread;top5_qty_imbalance;stale_quote_duration_ms;quote_churn_count",
                "requirement": "Create causal spread/liquidity/churn regimes for conditional baselines.",
                "leakage_control": "regime state must be computed at or before feature bucket timestamp",
                "required_for_phase214": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
            },
            {
                "phase213_feature_requirement_id": "P213_CONDITIONAL_BASELINE_STATE",
                "required_feature_source": "train_only_symbol_date_horizon_regime_baselines",
                "requirement": "Estimate label baselines on train split only; validation uses frozen train baselines; sealed test unused.",
                "leakage_control": "no validation/test target values in baseline estimation",
                "required_for_phase214": 1,
                "model_fit_allowed_now": 0,
                "strategy_replay_allowed": 0,
            },
        ]
    )


def build_control_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase213_control_id": "P213_BALANCED_BASE_RATE_CONTROL",
                "control_type": "base_rate",
                "requirement": "Report class balance by split/horizon/regime and reject labels where validation base-rate dominates.",
                "required_before_model_fit": 1,
                "test_replay_allowed_next": 0,
            },
            {
                "phase213_control_id": "P213_SHUFFLED_EVENT_TIME_CONTROL",
                "control_type": "time_shuffle",
                "requirement": "Shuffle receive-event surprise bucket times within symbol/date before interpretation.",
                "required_before_model_fit": 1,
                "test_replay_allowed_next": 0,
            },
            {
                "phase213_control_id": "P213_TRAIN_BASELINE_ONLY_CONTROL",
                "control_type": "leakage_control",
                "requirement": "Prove conditional baselines are estimated from train split only and sealed test remains unused.",
                "required_before_model_fit": 1,
                "test_replay_allowed_next": 0,
            },
        ]
    )


def build_phase214_work_order(selection: pd.DataFrame, labels: pd.DataFrame, features: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "phase214_work_order_id": "P214_EVENT_SURPRISE_CONDITIONAL_LABEL_MATERIALIZATION",
                "phase213_source_id": selection["phase213_source_id"].iloc[0] if not selection.empty else SELECTED_SOURCE_ID,
                "work_order": "Materialize event-surprise conditional label contract over train/validation partitions only, with sealed test inventory recorded but unused.",
                "label_contract_rows": len(labels),
                "feature_requirement_rows": len(features),
                "control_rows": len(controls),
                "allowed_next_scope": "label_contract_materialization_and_quality_no_model_no_replay_no_test",
                "model_fit_allowed_next": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
                "promotion_allowed": 0,
            }
        ]
    )


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase213": 0,
                "allowed_in_phase213": 0,
                "rationale": "Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase212: pd.DataFrame, selection: pd.DataFrame, labels: pd.DataFrame, features: pd.DataFrame, controls: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase212_complete = as_int(metric_value(phase212, "phase212_model_family_closure_or_redesign_precommit_complete", 0))
    families_closed = as_int(metric_value(phase212, "phase212_families_closed_for_replay", 0))
    replay_flags = 0
    for frame in [selection, labels, features, controls, work_order]:
        for col in ["model_fit_allowed_now", "model_fit_allowed_next", "strategy_replay_allowed", "test_replay_allowed_next", "promotion_allowed", "paper_or_live_acceptance_allowed", "profitability_claim_allowed"]:
            if not frame.empty and col in frame.columns:
                replay_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    forbidden_emitted = int(forbidden["emitted_in_phase213"].astype(int).sum()) if not forbidden.empty else 1
    return pd.DataFrame(
        [
            ("P213_PHASE212_COMPLETE", phase212_complete == 1, f"phase212_complete={phase212_complete}", "hard"),
            ("P213_CURRENT_FAMILIES_CLOSED", families_closed == 3, f"families_closed={families_closed}", "hard"),
            ("P213_MATERIAL_SOURCE_SELECTED", len(selection) == 1 and int(selection["selected_for_phase214"].iloc[0]) == 1, f"selection_rows={len(selection)}", "hard"),
            ("P213_LABEL_CONTRACT_RECORDED", len(labels) == 3 and labels["materialization_allowed_next"].astype(int).eq(1).all(), f"label_contract_rows={len(labels)}", "hard"),
            ("P213_FEATURE_REQUIREMENTS_RECORDED", len(features) == 3 and features["required_for_phase214"].astype(int).eq(1).all(), f"feature_requirement_rows={len(features)}", "hard"),
            ("P213_CONTROL_CONTRACT_RECORDED", len(controls) == 3 and controls["required_before_model_fit"].astype(int).eq(1).all(), f"control_rows={len(controls)}", "hard"),
            ("P213_PHASE214_WORK_ORDER_RECORDED", len(work_order) == 1, f"work_order_rows={len(work_order)}", "hard"),
            ("P213_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and replay_flags == 0, f"forbidden_emitted={forbidden_emitted}; replay_flags={replay_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(selection: pd.DataFrame, labels: pd.DataFrame, features: pd.DataFrame, controls: pd.DataFrame, work_order: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase213_source_selection_rows", len(selection), "Material-new-source selection rows"),
            ("phase213_selected_source_id", selection["phase213_source_id"].iloc[0] if not selection.empty else "", "Selected material source"),
            ("phase213_label_contract_rows", len(labels), "Conditional label contract rows"),
            ("phase213_feature_requirement_rows", len(features), "Feature requirement rows"),
            ("phase213_control_contract_rows", len(controls), "Control contract rows"),
            ("phase213_phase214_work_order_rows", len(work_order), "Phase214 work-order rows"),
            ("phase213_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase213_gate_rows", len(gates), "Gates evaluated"),
            ("phase213_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase213_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase213_material_new_model_source_precommit_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase213 completed"),
            ("phase213_model_fit_allowed_next", 0, "No model fit opened"),
            ("phase213_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase213_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase213_promotion_allowed", 0, "No promotion opened"),
            ("phase213_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase213_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase213_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase213_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase213 Material New Model Source Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase213 selects a materially new source after Phase212 closed the current model families for replay.",
        "It precommits an event-surprise conditional label source and a Phase214 materialization work order without fitting models, running replay, using sealed test, or making profitability claims.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase213_material_new_model_source_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase213(phase212_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase212 = read_csv(phase212_dir / "phase212_model_family_closure_acceptance_summary.csv")
    redesign = read_csv(phase212_dir / "phase212_material_redesign_precommit_catalog.csv")
    action = read_csv(phase212_dir / "phase212_phase213_action_queue.csv")
    selection = build_source_selection(redesign, action)
    labels = build_conditional_label_contract()
    features = build_feature_requirement_contract()
    controls = build_control_contract()
    work_order = build_phase214_work_order(selection, labels, features, controls)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase212, selection, labels, features, controls, work_order, forbidden)
    acceptance = build_acceptance(selection, labels, features, controls, work_order, forbidden, gates)

    selection.to_csv(output_dir / "phase213_material_source_selection.csv", index=False)
    labels.to_csv(output_dir / "phase213_conditional_label_contract.csv", index=False)
    features.to_csv(output_dir / "phase213_feature_requirement_contract.csv", index=False)
    controls.to_csv(output_dir / "phase213_control_contract.csv", index=False)
    work_order.to_csv(output_dir / "phase213_phase214_work_order.csv", index=False)
    forbidden.to_csv(output_dir / "phase213_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase213_material_new_source_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase213_material_new_source_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Material Source Selection": selection,
            "Conditional Label Contract": labels,
            "Feature Requirement Contract": features,
            "Control Contract": controls,
            "Phase214 Work Order": work_order,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase213_material_new_model_source_precommit_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase213_material_new_model_source_precommit",
            generated_utc=generated,
            inputs={
                "phase212_acceptance": str(phase212_dir / "phase212_model_family_closure_acceptance_summary.csv"),
                "phase212_redesign_catalog": str(phase212_dir / "phase212_material_redesign_precommit_catalog.csv"),
                "phase212_action_queue": str(phase212_dir / "phase212_phase213_action_queue.csv"),
            },
            parameters={
                "selected_source_id": SELECTED_SOURCE_ID,
                "selected_route": "event_surprise_conditional_label_source",
                "model_fit_allowed": "0",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "selection": str(output_dir / "phase213_material_source_selection.csv"),
                "label_contract": str(output_dir / "phase213_conditional_label_contract.csv"),
                "feature_contract": str(output_dir / "phase213_feature_requirement_contract.csv"),
                "control_contract": str(output_dir / "phase213_control_contract.csv"),
                "work_order": str(output_dir / "phase213_phase214_work_order.csv"),
                "forbidden": str(output_dir / "phase213_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase213_material_new_source_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase213_material_new_source_acceptance_summary.csv"),
                "report": str(output_dir / "phase213_material_new_model_source_precommit_report.md"),
            },
            scenario_ids="phase213_material_new_model_source_precommit_no_replay_no_test",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase213_material_new_source_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase213 material new model source precommit without replay/test.")
    parser.add_argument("--phase212-dir", type=Path, default=DEFAULT_PHASE212_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase213(args.phase212_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE180_DIR = Path("outputs/phase180")
DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE207_DIR = Path("outputs/phase207")
DEFAULT_PHASE208_DIR = Path("outputs/phase208")
DEFAULT_OUTPUT_DIR = Path("outputs/phase209")
FORBIDDEN_OUTPUTS = "model_fit;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening"
NEXT_ACTION = "run_phase210_train_validation_model_fit_dry_run_no_replay_no_test"


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


def build_model_fit_spec() -> pd.DataFrame:
    rows = [
        {
            "phase209_model_spec_id": "P209_LINEAR_LOGIT_DIRECTION_BASELINE",
            "model_family": "regularized_logistic_classification",
            "target_label": "short_horizon_direction_label",
            "primary_horizons_sec": "1;5;15;60",
            "feature_policy": "phase206_nonoverlap_allowed_features_only",
            "calibration_policy": "train_fit_validation_calibration_only",
            "selection_policy": "validation_screening_only_test_sealed",
            "negative_controls_required": "shuffled_time_date;target_symbol_excluded_cross_symbol;blocked_form_overlap",
            "allowed_next_phase_scope": "train_validation_fit_dry_run_only",
            "model_fit_execution_allowed_phase209": 0,
            "strategy_replay_allowed": 0,
            "test_replay_allowed_next": 0,
            "promotion_allowed": 0,
            "paper_or_live_acceptance_allowed": 0,
        },
        {
            "phase209_model_spec_id": "P209_RIDGE_RETURN_SIGN_BASELINE",
            "model_family": "regularized_linear_return_sign_proxy",
            "target_label": "future_mid_return_bps_next_bucket",
            "primary_horizons_sec": "1;5;15;60",
            "feature_policy": "phase206_nonoverlap_allowed_features_only",
            "calibration_policy": "train_only_standardization_validation_score_no_test",
            "selection_policy": "validation_screening_only_test_sealed",
            "negative_controls_required": "shuffled_time_date;target_symbol_excluded_cross_symbol;blocked_form_overlap",
            "allowed_next_phase_scope": "train_validation_fit_dry_run_only",
            "model_fit_execution_allowed_phase209": 0,
            "strategy_replay_allowed": 0,
            "test_replay_allowed_next": 0,
            "promotion_allowed": 0,
            "paper_or_live_acceptance_allowed": 0,
        },
        {
            "phase209_model_spec_id": "P209_MONOTONIC_TREE_DIAGNOSTIC",
            "model_family": "monotonic_tree_or_gradient_boosting_diagnostic",
            "target_label": "execution_risk_spread_widen_next_bucket",
            "primary_horizons_sec": "1;5;15;60",
            "feature_policy": "phase206_nonoverlap_allowed_features_only_with_depth_direction_constraints",
            "calibration_policy": "validation_diagnostic_only_no_threshold_selection_for_test",
            "selection_policy": "diagnostic_interpretability_only_test_sealed",
            "negative_controls_required": "shuffled_time_date;target_symbol_excluded_cross_symbol;blocked_form_overlap",
            "allowed_next_phase_scope": "train_validation_fit_dry_run_only",
            "model_fit_execution_allowed_phase209": 0,
            "strategy_replay_allowed": 0,
            "test_replay_allowed_next": 0,
            "promotion_allowed": 0,
            "paper_or_live_acceptance_allowed": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_feature_set_contract(matrix: pd.DataFrame, quality: pd.DataFrame) -> pd.DataFrame:
    if matrix.empty:
        return pd.DataFrame()
    quality_keys = set()
    if not quality.empty:
        for row in quality.to_dict("records"):
            quality_keys.add((str(row.get("phase206_feature_id", "")), as_int(row.get("horizon_sec", 0))))
    rows: list[dict[str, Any]] = []
    for (feature_id, horizon), part in matrix.groupby(["phase206_feature_id", "horizon_sec"], sort=True):
        feature_available = int(pd.to_numeric(part["feature_available"], errors="coerce").fillna(0).min())
        quality_pass = int((str(feature_id), as_int(horizon)) in quality_keys)
        rows.append(
            {
                "phase209_feature_set_id": f"P209_{feature_id}_H{as_int(horizon)}s",
                "phase206_feature_id": feature_id,
                "feature_family": semicolon_join(part["feature_family"]) if "feature_family" in part.columns else "",
                "horizon_sec": as_int(horizon),
                "required_columns": semicolon_join(part["required_columns"]) if "required_columns" in part.columns else "",
                "feature_available": feature_available,
                "quality_gate_pass": quality_pass,
                "trade_dates": as_int(part["trade_dates"].max(), 0),
                "symbols": as_int(part["symbols"].max(), 0),
                "total_feature_rows": as_int(part["total_feature_rows"].max(), 0),
                "allowed_for_phase210_design_matrix": int(feature_available == 1 and quality_pass == 1),
                "model_fit_execution_allowed_phase209": 0,
                "strategy_replay_allowed": 0,
                "test_replay_allowed_next": 0,
            }
        )
    return pd.DataFrame(rows)


def build_label_target_contract(label_families: pd.DataFrame, label_inventory: pd.DataFrame) -> pd.DataFrame:
    available_columns = ""
    if not label_inventory.empty and "label_file" in label_inventory.columns:
        first_file = next((Path(str(p)) for p in label_inventory["label_file"].dropna().astype(str) if Path(str(p)).exists()), None)
        if first_file is not None:
            try:
                available_columns = ";".join(pd.read_parquet(first_file).columns.astype(str).tolist())
            except Exception:
                available_columns = ""
    split_counts = label_inventory.groupby("split_role")["label_available_rows"].sum().to_dict() if not label_inventory.empty and "split_role" in label_inventory.columns else {}
    rows: list[dict[str, Any]] = []
    target_specs = [
        ("P209_PRIMARY_DIRECTION_TARGET", "short_horizon_direction_label", "classification_direction", "future receive-flow direction label; no P&L label"),
        ("P209_RETURN_PROXY_TARGET", "future_mid_return_bps_next_bucket", "regression_or_sign_proxy", "future mid-return label for model diagnostics only"),
        ("P209_EXECUTION_RISK_TARGET", "execution_risk_spread_widen_next_bucket", "classification_execution_risk", "future spread-widening risk label; not a fill model"),
    ]
    for target_id, label_name, target_type, description in target_specs:
        rows.append(
            {
                "phase209_label_target_id": target_id,
                "label_column": label_name,
                "target_type": target_type,
                "description": description,
                "label_family_rows": len(label_families),
                "label_partition_rows": len(label_inventory),
                "label_available_rows": as_int(label_inventory["label_available_rows"].sum(), 0) if not label_inventory.empty and "label_available_rows" in label_inventory.columns else 0,
                "train_label_available_rows": as_int(split_counts.get("train", 0), 0),
                "validation_label_available_rows": as_int(split_counts.get("validation", 0), 0),
                "test_label_available_rows_sealed": as_int(split_counts.get("test", 0), 0),
                "column_seen_in_sample": int(label_name in available_columns.split(";")),
                "cost_latency_binding": semicolon_join(label_families["cost_latency_binding_required"]) if not label_families.empty and "cost_latency_binding_required" in label_families.columns else "",
                "test_selection_allowed": 0,
                "model_fit_execution_allowed_phase209": 0,
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_split_and_control_contract(label_inventory: pd.DataFrame, ablations: pd.DataFrame) -> pd.DataFrame:
    split_dates = {}
    if not label_inventory.empty and {"split_role", "trade_date"}.issubset(label_inventory.columns):
        split_dates = label_inventory.groupby("split_role")["trade_date"].apply(lambda s: semicolon_join(s)).to_dict()
        sealed_test_dates = semicolon_join(label_inventory.loc[label_inventory["split_role"].astype(str).str.contains("test", case=False, na=False), "trade_date"])
    else:
        sealed_test_dates = ""
    ablation_ids = semicolon_join(ablations["ablation_id"]) if not ablations.empty and "ablation_id" in ablations.columns else ""
    rows = [
        {
            "phase209_control_id": "P209_TRAIN_VALIDATION_TEST_SPLIT_CONTRACT",
            "control_type": "split",
            "required_before_phase210": 1,
            "contract": "Fit on train only; screen/calibrate on validation only; keep test dates sealed and unused.",
            "train_dates": split_dates.get("train", ""),
            "validation_dates": split_dates.get("validation", ""),
            "test_dates_sealed": sealed_test_dates,
            "source_ablation_ids": ablation_ids,
            "model_fit_execution_allowed_phase209": 0,
            "strategy_replay_allowed": 0,
            "test_replay_allowed_next": 0,
        },
        {
            "phase209_control_id": "P209_SHUFFLED_TIME_DATE_NEGATIVE_CONTROL",
            "control_type": "negative_control",
            "required_before_phase210": 1,
            "contract": "Every model-family dry run must include a shuffled time/date control before edge interpretation.",
            "train_dates": split_dates.get("train", ""),
            "validation_dates": split_dates.get("validation", ""),
            "test_dates_sealed": sealed_test_dates,
            "source_ablation_ids": ablation_ids,
            "model_fit_execution_allowed_phase209": 0,
            "strategy_replay_allowed": 0,
            "test_replay_allowed_next": 0,
        },
        {
            "phase209_control_id": "P209_TARGET_SYMBOL_EXCLUDED_CROSS_SYMBOL_CONTROL",
            "control_type": "leakage_control",
            "required_before_phase210": 1,
            "contract": "Cross-symbol arrival synchrony must exclude the target symbol in any future design matrix.",
            "train_dates": split_dates.get("train", ""),
            "validation_dates": split_dates.get("validation", ""),
            "test_dates_sealed": sealed_test_dates,
            "source_ablation_ids": ablation_ids,
            "model_fit_execution_allowed_phase209": 0,
            "strategy_replay_allowed": 0,
            "test_replay_allowed_next": 0,
        },
        {
            "phase209_control_id": "P209_BLOCKED_FORM_OVERLAP_CONTROL",
            "control_type": "reuse_control",
            "required_before_phase210": 1,
            "contract": "No Phase164 form reuse, no fixed Phase167 S08 score, no passive queue replay form overlap.",
            "train_dates": split_dates.get("train", ""),
            "validation_dates": split_dates.get("validation", ""),
            "test_dates_sealed": sealed_test_dates,
            "source_ablation_ids": ablation_ids,
            "model_fit_execution_allowed_phase209": 0,
            "strategy_replay_allowed": 0,
            "test_replay_allowed_next": 0,
        },
    ]
    return pd.DataFrame(rows)


def build_forbidden_execution_ledger() -> pd.DataFrame:
    forbidden = [
        "model_fit",
        "model_prediction",
        "strategy_replay",
        "test_replay_execution",
        "test_result",
        "promotion",
        "paper_live_acceptance",
        "order_arrival",
        "fill_model",
        "pnl_replay",
        "profitability_claim",
        "threshold_widening",
    ]
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase209": 0,
                "allowed_in_phase209": 0,
                "rationale": "Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase.",
            }
            for item in forbidden
        ]
    )


def build_gates(
    phase208: pd.DataFrame,
    feature_contract: pd.DataFrame,
    label_contract: pd.DataFrame,
    split_contract: pd.DataFrame,
    model_specs: pd.DataFrame,
    forbidden: pd.DataFrame,
) -> pd.DataFrame:
    phase208_complete = as_int(metric_value(phase208, "phase208_feature_matrix_quality_gate_complete", 0))
    available_feature_rows = int(feature_contract["allowed_for_phase210_design_matrix"].astype(int).sum()) if not feature_contract.empty else 0
    label_columns_seen = int(label_contract["column_seen_in_sample"].astype(int).sum()) if not label_contract.empty else 0
    required_controls = int(split_contract["required_before_phase210"].astype(int).sum()) if not split_contract.empty else 0
    forbidden_emitted = int(forbidden["emitted_in_phase209"].astype(int).sum()) if not forbidden.empty else 1
    forbidden_flags = 0
    for frame in [feature_contract, label_contract, split_contract, model_specs]:
        for col in ["model_fit_execution_allowed_phase209", "strategy_replay_allowed", "test_replay_allowed_next", "promotion_allowed", "paper_or_live_acceptance_allowed"]:
            if not frame.empty and col in frame.columns:
                forbidden_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P209_PHASE208_COMPLETE", phase208_complete == 1, f"phase208_complete={phase208_complete}", "hard"),
            ("P209_MODEL_SPECS_RECORDED", len(model_specs) >= 3, f"model_spec_rows={len(model_specs)}", "hard"),
            ("P209_FEATURE_SET_CONTRACT_RECORDED", available_feature_rows >= 24, f"allowed_feature_rows={available_feature_rows}", "hard"),
            ("P209_LABEL_TARGET_CONTRACT_RECORDED", len(label_contract) == 3 and label_columns_seen == 3, f"label_rows={len(label_contract)}; columns_seen={label_columns_seen}", "hard"),
            ("P209_SPLIT_AND_CONTROL_CONTRACT_RECORDED", len(split_contract) >= 4 and required_controls == len(split_contract), f"split_control_rows={len(split_contract)}; required_controls={required_controls}", "hard"),
            ("P209_FORBIDDEN_EXECUTION_LEDGER_CLEAN", forbidden_emitted == 0 and forbidden_flags == 0, f"forbidden_emitted={forbidden_emitted}; forbidden_flags={forbidden_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(model_specs: pd.DataFrame, feature_contract: pd.DataFrame, label_contract: pd.DataFrame, split_contract: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase209_model_spec_rows", len(model_specs), "Model-family specification rows"),
            ("phase209_feature_set_rows", len(feature_contract), "Feature-set contract rows"),
            ("phase209_allowed_feature_set_rows", int(feature_contract["allowed_for_phase210_design_matrix"].astype(int).sum()) if not feature_contract.empty else 0, "Feature-set rows allowed for future Phase210 design matrix"),
            ("phase209_label_target_rows", len(label_contract), "Label-target contract rows"),
            ("phase209_split_control_rows", len(split_contract), "Split/control contract rows"),
            ("phase209_forbidden_execution_rows", len(forbidden), "Forbidden execution ledger rows"),
            ("phase209_gate_rows", len(gates), "Gates evaluated"),
            ("phase209_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase209_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase209_model_fit_precommit_spec_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase209 completed"),
            ("phase209_model_fit_execution_allowed", 0, "No model fitting executed/opened in Phase209"),
            ("phase209_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase209_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase209_promotion_allowed", 0, "No promotion opened"),
            ("phase209_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase209_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase209_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase209 Model-fit Precommit Spec",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase209 freezes the next model-fit design without executing the fit.",
        "It records model families, feature sets, label targets, train/validation/test sealing rules, negative controls, and forbidden outputs.",
        "It emits no model predictions, no strategy replay, no order/fill/P&L artifacts, no promotion, and no paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase209_model_fit_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase209(phase180_dir: Path, phase181_dir: Path, phase207_dir: Path, phase208_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase208 = read_csv(phase208_dir / "phase208_feature_matrix_quality_acceptance_summary.csv")
    matrix = read_csv(phase207_dir / "phase207_allowed_feature_matrix.csv")
    quality = read_csv(phase208_dir / "phase208_feature_matrix_quality_summary.csv")
    ablations = read_csv(phase207_dir / "phase207_target_exclusion_ablation_spec.csv")
    label_families = read_csv(phase180_dir / "phase180_label_family_precommit.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    model_specs = build_model_fit_spec()
    feature_contract = build_feature_set_contract(matrix, quality)
    label_contract = build_label_target_contract(label_families, label_inventory)
    split_contract = build_split_and_control_contract(label_inventory, ablations)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase208, feature_contract, label_contract, split_contract, model_specs, forbidden)
    acceptance = build_acceptance(model_specs, feature_contract, label_contract, split_contract, forbidden, gates)

    model_specs.to_csv(output_dir / "phase209_model_fit_spec.csv", index=False)
    feature_contract.to_csv(output_dir / "phase209_feature_set_contract.csv", index=False)
    label_contract.to_csv(output_dir / "phase209_label_target_contract.csv", index=False)
    split_contract.to_csv(output_dir / "phase209_split_and_control_contract.csv", index=False)
    forbidden.to_csv(output_dir / "phase209_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase209_model_fit_precommit_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase209_model_fit_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Model Fit Spec": model_specs,
            "Feature Set Contract": feature_contract,
            "Label Target Contract": label_contract,
            "Split and Control Contract": split_contract,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase209_model_fit_precommit_spec_no_execution_no_replay",
        **reproducibility_fields(
            artifact_id="phase209_model_fit_precommit_spec",
            generated_utc=generated,
            inputs={
                "phase180_label_family_precommit": str(phase180_dir / "phase180_label_family_precommit.csv"),
                "phase181_label_partition_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase207_allowed_feature_matrix": str(phase207_dir / "phase207_allowed_feature_matrix.csv"),
                "phase207_target_exclusion_ablation_spec": str(phase207_dir / "phase207_target_exclusion_ablation_spec.csv"),
                "phase208_quality_acceptance": str(phase208_dir / "phase208_feature_matrix_quality_acceptance_summary.csv"),
                "phase208_quality_summary": str(phase208_dir / "phase208_feature_matrix_quality_summary.csv"),
            },
            parameters={
                "minimum_model_specs": "3",
                "minimum_allowed_feature_set_rows": "24",
                "target_columns": "short_horizon_direction_label;future_mid_return_bps_next_bucket;execution_risk_spread_widen_next_bucket",
                "model_fit_execution_allowed_phase209": "0",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "model_fit_spec": str(output_dir / "phase209_model_fit_spec.csv"),
                "feature_set_contract": str(output_dir / "phase209_feature_set_contract.csv"),
                "label_target_contract": str(output_dir / "phase209_label_target_contract.csv"),
                "split_and_control_contract": str(output_dir / "phase209_split_and_control_contract.csv"),
                "forbidden_execution_ledger": str(output_dir / "phase209_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase209_model_fit_precommit_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase209_model_fit_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase209_model_fit_precommit_report.md"),
            },
            scenario_ids="phase209_model_fit_precommit_spec_no_execution_no_replay",
            cost_model_version="zerodha_equity_cost_catalog_phase180_bound_no_replay",
            latency_model_version="phase180_latency_slippage_catalog_bound_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase209_model_fit_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase209 model-fit precommit spec without fitting/replay.")
    parser.add_argument("--phase180-dir", type=Path, default=DEFAULT_PHASE180_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase207-dir", type=Path, default=DEFAULT_PHASE207_DIR)
    parser.add_argument("--phase208-dir", type=Path, default=DEFAULT_PHASE208_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase209(args.phase180_dir, args.phase181_dir, args.phase207_dir, args.phase208_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE181_DIR = Path("outputs/phase181")
DEFAULT_PHASE209_DIR = Path("outputs/phase209")
DEFAULT_OUTPUT_DIR = Path("outputs/phase210")
JOIN_KEYS = ["bucket_ms", "trade_date", "exchange", "symbol", "horizon_sec"]
RNG_SEED = 210
RIDGE_LAMBDA = 1.0
FORBIDDEN_OUTPUTS = "strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase211_model_fit_validation_interpretation_no_replay_no_test"


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


def parse_feature_columns(feature_contract: pd.DataFrame) -> list[str]:
    columns: set[str] = set()
    if feature_contract.empty or "required_columns" not in feature_contract.columns:
        return []
    allowed = feature_contract
    if "allowed_for_phase210_design_matrix" in allowed.columns:
        allowed = allowed[pd.to_numeric(allowed["allowed_for_phase210_design_matrix"], errors="coerce").fillna(0).astype(int).eq(1)]
    for value in allowed["required_columns"].dropna().astype(str):
        for col in value.split(";"):
            col = col.strip()
            if col:
                columns.add(col)
    return sorted(columns)


def partition_key(row: dict[str, Any]) -> tuple[int, str, str, str]:
    return (as_int(row.get("horizon_sec", 0)), str(row.get("trade_date", "")), str(row.get("exchange", "")), str(row.get("symbol", "")))


def load_design_matrices(feature_inventory: pd.DataFrame, label_inventory: pd.DataFrame, feature_columns: list[str], target_columns: list[str]) -> tuple[dict[int, dict[str, pd.DataFrame]], pd.DataFrame]:
    feature_paths = {partition_key(row): Path(str(row.get("parquet_file", ""))) for row in feature_inventory.to_dict("records")}
    matrices: dict[int, dict[str, list[pd.DataFrame]]] = {}
    inventory_rows: list[dict[str, Any]] = []
    usable = label_inventory[label_inventory["split_role"].astype(str).isin(["train", "validation"])] if not label_inventory.empty and "split_role" in label_inventory.columns else pd.DataFrame()
    for row in usable.to_dict("records"):
        key = partition_key(row)
        feature_path = feature_paths.get(key)
        label_path = Path(str(row.get("label_file", "")))
        split_role = str(row.get("split_role", ""))
        horizon = key[0]
        if feature_path is None or not feature_path.exists() or not label_path.exists():
            inventory_rows.append(
                {
                    "horizon_sec": horizon,
                    "trade_date": key[1],
                    "exchange": key[2],
                    "symbol": key[3],
                    "split_role": split_role,
                    "feature_file_exists": int(feature_path is not None and feature_path.exists()),
                    "label_file_exists": int(label_path.exists()),
                    "joined_rows": 0,
                    "test_rows_used": 0,
                }
            )
            continue
        feature_cols = JOIN_KEYS + feature_columns
        label_cols = JOIN_KEYS + ["split_role", "label_available"] + target_columns
        features = pd.read_parquet(feature_path, columns=[c for c in feature_cols if c in pd.read_parquet(feature_path).columns])
        labels = pd.read_parquet(label_path, columns=[c for c in label_cols if c in pd.read_parquet(label_path).columns])
        joined = features.merge(labels, on=JOIN_KEYS, how="inner")
        if "label_available" in joined.columns:
            joined = joined[pd.to_numeric(joined["label_available"], errors="coerce").fillna(0).astype(int).eq(1)]
        for col in feature_columns:
            if col not in joined.columns:
                joined[col] = 0.0
        joined[feature_columns] = joined[feature_columns].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)
        for col in target_columns:
            if col in joined.columns:
                joined[col] = pd.to_numeric(joined[col], errors="coerce")
        keep_cols = JOIN_KEYS + ["split_role"] + feature_columns + [c for c in target_columns if c in joined.columns]
        joined = joined[keep_cols]
        matrices.setdefault(horizon, {}).setdefault(split_role, []).append(joined)
        inventory_rows.append(
            {
                "horizon_sec": horizon,
                "trade_date": key[1],
                "exchange": key[2],
                "symbol": key[3],
                "split_role": split_role,
                "feature_file_exists": 1,
                "label_file_exists": 1,
                "joined_rows": len(joined),
                "test_rows_used": 0,
            }
        )
    matrix_frames: dict[int, dict[str, pd.DataFrame]] = {}
    for horizon, split_map in matrices.items():
        matrix_frames[horizon] = {}
        for split_role, frames in split_map.items():
            matrix_frames[horizon][split_role] = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    return matrix_frames, pd.DataFrame(inventory_rows)


def transform_target(frame: pd.DataFrame, target: str) -> pd.Series:
    y = pd.to_numeric(frame[target], errors="coerce")
    if target == "short_horizon_direction_label":
        return (y > 0).astype(float)
    return y.astype(float)


def fit_ridge(train: pd.DataFrame, feature_columns: list[str], target: str, shuffle: bool = False) -> dict[str, Any]:
    clean = train.dropna(subset=[target]).copy()
    x_raw = clean[feature_columns].to_numpy(dtype=float)
    y = transform_target(clean, target).to_numpy(dtype=float)
    if shuffle:
        rng = np.random.default_rng(RNG_SEED)
        y = rng.permutation(y)
    means = x_raw.mean(axis=0)
    stds = x_raw.std(axis=0)
    stds = np.where(stds <= 1e-12, 1.0, stds)
    x = (x_raw - means) / stds
    design = np.column_stack([np.ones(len(x)), x])
    penalty = np.eye(design.shape[1]) * RIDGE_LAMBDA
    penalty[0, 0] = 0.0
    beta = np.linalg.pinv(design.T @ design + penalty) @ design.T @ y
    return {
        "target": target,
        "feature_columns": feature_columns,
        "means": means,
        "stds": stds,
        "beta": beta,
        "train_rows": len(clean),
        "shuffle_control": int(shuffle),
    }


def score_model(model: dict[str, Any], frame: pd.DataFrame, split_role: str) -> dict[str, Any]:
    target = str(model["target"])
    clean = frame.dropna(subset=[target]).copy()
    x_raw = clean[model["feature_columns"]].to_numpy(dtype=float)
    x = (x_raw - model["means"]) / model["stds"]
    design = np.column_stack([np.ones(len(x)), x])
    y = transform_target(clean, target).to_numpy(dtype=float)
    pred = design @ model["beta"]
    err = pred - y
    y_std = float(np.std(y)) if len(y) else 0.0
    pred_std = float(np.std(pred)) if len(pred) else 0.0
    corr = float(np.corrcoef(y, pred)[0, 1]) if len(y) > 2 and y_std > 1e-12 and pred_std > 1e-12 else 0.0
    is_binary = target in {"short_horizon_direction_label", "execution_risk_spread_widen_next_bucket"}
    accuracy = float(((pred >= 0.5).astype(int) == (y >= 0.5).astype(int)).mean()) if is_binary and len(y) else np.nan
    return {
        "split_role": split_role,
        "rows": len(clean),
        "target_mean": float(np.mean(y)) if len(y) else np.nan,
        "prediction_mean": float(np.mean(pred)) if len(pred) else np.nan,
        "mse": float(np.mean(err * err)) if len(err) else np.nan,
        "mae": float(np.mean(np.abs(err))) if len(err) else np.nan,
        "correlation": corr,
        "binary_accuracy": accuracy,
    }


def build_fits(matrix_frames: dict[int, dict[str, pd.DataFrame]], model_specs: pd.DataFrame, feature_columns: list[str]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    metrics: list[dict[str, Any]] = []
    coefs: list[dict[str, Any]] = []
    controls: list[dict[str, Any]] = []
    for spec in model_specs.to_dict("records"):
        spec_id = str(spec.get("phase209_model_spec_id", ""))
        target = str(spec.get("target_label", ""))
        for horizon in sorted(matrix_frames):
            train = matrix_frames[horizon].get("train", pd.DataFrame())
            validation = matrix_frames[horizon].get("validation", pd.DataFrame())
            if train.empty or validation.empty or target not in train.columns or target not in validation.columns:
                continue
            main_model = fit_ridge(train, feature_columns, target, shuffle=False)
            shuffled_model = fit_ridge(train, feature_columns, target, shuffle=True)
            for model, control_name in [(main_model, "main_fit"), (shuffled_model, "shuffled_target_negative_control")]:
                for split_role, frame in [("train", train), ("validation", validation)]:
                    scored = score_model(model, frame, split_role)
                    if control_name == "main_fit":
                        metrics.append(
                            {
                                "phase210_model_fit_id": f"P210_{spec_id}_H{horizon}s",
                                "phase209_model_spec_id": spec_id,
                                "model_family": spec.get("model_family", ""),
                                "target_label": target,
                                "horizon_sec": horizon,
                                "split_role": split_role,
                                "train_rows_used_for_fit": main_model["train_rows"],
                                "test_rows_used": 0,
                                "strategy_replay_allowed": 0,
                                "promotion_allowed": 0,
                                **scored,
                            }
                        )
                    elif split_role == "validation":
                        controls.append(
                            {
                                "phase210_control_id": f"P210_SHUFFLED_{spec_id}_H{horizon}s",
                                "phase209_model_spec_id": spec_id,
                                "target_label": target,
                                "horizon_sec": horizon,
                                "control_type": control_name,
                                "validation_rows": scored["rows"],
                                "validation_mse": scored["mse"],
                                "validation_binary_accuracy": scored["binary_accuracy"],
                                "test_rows_used": 0,
                                "strategy_replay_allowed": 0,
                            }
                        )
            for name, value in zip(["intercept"] + feature_columns, main_model["beta"].tolist()):
                coefs.append(
                    {
                        "phase210_model_fit_id": f"P210_{spec_id}_H{horizon}s",
                        "phase209_model_spec_id": spec_id,
                        "target_label": target,
                        "horizon_sec": horizon,
                        "coefficient_name": name,
                        "coefficient_value": float(value),
                        "model_fit_execution": 1,
                        "strategy_replay_allowed": 0,
                        "test_replay_allowed_next": 0,
                    }
                )
    return pd.DataFrame(metrics), pd.DataFrame(coefs), pd.DataFrame(controls)


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase210": 0,
                "allowed_in_phase210": 0,
                "rationale": "Phase210 fits train/validation dry-run models only and does not run replay, test replay, fills, P&L, promotion, or paper/live acceptance.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase209: pd.DataFrame, inventory: pd.DataFrame, metrics: pd.DataFrame, coefs: pd.DataFrame, controls: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase209_complete = as_int(metric_value(phase209, "phase209_model_fit_precommit_spec_complete", 0))
    model_fit_rows = int(metrics["phase210_model_fit_id"].nunique()) if not metrics.empty else 0
    validation_metric_rows = int(metrics["split_role"].astype(str).eq("validation").sum()) if not metrics.empty else 0
    test_rows_used = 0
    for frame in [inventory, metrics, controls]:
        if not frame.empty and "test_rows_used" in frame.columns:
            test_rows_used += int(pd.to_numeric(frame["test_rows_used"], errors="coerce").fillna(0).sum())
    forbidden_emitted = int(forbidden["emitted_in_phase210"].astype(int).sum()) if not forbidden.empty else 1
    replay_flags = 0
    for frame in [metrics, coefs, controls]:
        for col in ["strategy_replay_allowed", "test_replay_allowed_next", "promotion_allowed"]:
            if not frame.empty and col in frame.columns:
                replay_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P210_PHASE209_COMPLETE", phase209_complete == 1, f"phase209_complete={phase209_complete}", "hard"),
            ("P210_DESIGN_MATRIX_JOINED", int(inventory["joined_rows"].sum()) > 0 if not inventory.empty else False, f"joined_rows={int(inventory['joined_rows'].sum()) if not inventory.empty else 0}", "hard"),
            ("P210_MODEL_FITS_RECORDED", model_fit_rows == 12, f"model_fit_rows={model_fit_rows}", "hard"),
            ("P210_VALIDATION_METRICS_RECORDED", validation_metric_rows == 12, f"validation_metric_rows={validation_metric_rows}", "hard"),
            ("P210_NEGATIVE_CONTROLS_RECORDED", len(controls) == 12, f"negative_control_rows={len(controls)}", "hard"),
            ("P210_TEST_REPLAY_AND_TEST_ROWS_CLOSED", test_rows_used == 0, f"test_rows_used={test_rows_used}", "hard"),
            ("P210_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and replay_flags == 0, f"forbidden_emitted={forbidden_emitted}; replay_flags={replay_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(inventory: pd.DataFrame, metrics: pd.DataFrame, coefs: pd.DataFrame, controls: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase210_design_matrix_partition_rows", len(inventory), "Train/validation joined partition rows"),
            ("phase210_design_matrix_joined_rows", int(inventory["joined_rows"].sum()) if not inventory.empty else 0, "Joined train/validation design-matrix rows"),
            ("phase210_model_fit_rows", int(metrics["phase210_model_fit_id"].nunique()) if not metrics.empty else 0, "Unique model/horizon fits"),
            ("phase210_metric_rows", len(metrics), "Train/validation metric rows"),
            ("phase210_validation_metric_rows", int(metrics["split_role"].astype(str).eq("validation").sum()) if not metrics.empty else 0, "Validation metric rows"),
            ("phase210_coefficient_rows", len(coefs), "Coefficient rows"),
            ("phase210_negative_control_rows", len(controls), "Negative-control rows"),
            ("phase210_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase210_gate_rows", len(gates), "Gates evaluated"),
            ("phase210_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase210_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase210_train_validation_model_fit_dry_run_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase210 completed"),
            ("phase210_model_fit_execution", 1, "Train/validation model fitting executed"),
            ("phase210_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase210_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase210_test_rows_used", 0, "No sealed test rows used"),
            ("phase210_promotion_allowed", 0, "No promotion opened"),
            ("phase210_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase210_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase210_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase210_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase210 Train/Validation Model-fit Dry Run",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase210 joins Phase176 receive-flow feature partitions to Phase181 receive-flow labels and fits train-only ridge dry-run models.",
        "It scores train and validation aggregates, records shuffled-target controls, and exports only aggregate metrics/coefficient ledgers.",
        "It does not use sealed test rows, run strategy replay, emit orders/fills/P&L, promote anything, or open paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase210_train_validation_model_fit_dry_run_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase210(phase176_dir: Path, phase181_dir: Path, phase209_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase209 = read_csv(phase209_dir / "phase209_model_fit_precommit_acceptance_summary.csv")
    model_specs = read_csv(phase209_dir / "phase209_model_fit_spec.csv")
    feature_contract = read_csv(phase209_dir / "phase209_feature_set_contract.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    feature_columns = parse_feature_columns(feature_contract)
    target_columns = sorted(model_specs["target_label"].dropna().astype(str).unique().tolist()) if not model_specs.empty and "target_label" in model_specs.columns else []
    matrix_frames, design_inventory = load_design_matrices(feature_inventory, label_inventory, feature_columns, target_columns)
    metrics, coefs, controls = build_fits(matrix_frames, model_specs, feature_columns)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase209, design_inventory, metrics, coefs, controls, forbidden)
    acceptance = build_acceptance(design_inventory, metrics, coefs, controls, forbidden, gates)

    design_inventory.to_csv(output_dir / "phase210_design_matrix_partition_inventory.csv", index=False)
    metrics.to_csv(output_dir / "phase210_train_validation_model_metrics.csv", index=False)
    coefs.to_csv(output_dir / "phase210_model_coefficient_ledger.csv", index=False)
    controls.to_csv(output_dir / "phase210_negative_control_metrics.csv", index=False)
    forbidden.to_csv(output_dir / "phase210_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase210_train_validation_model_fit_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase210_train_validation_model_fit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Design Matrix Partition Inventory": design_inventory,
            "Train/Validation Model Metrics": metrics,
            "Model Coefficient Ledger": coefs,
            "Negative Control Metrics": controls,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase210_train_validation_model_fit_dry_run_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase210_train_validation_model_fit_dry_run",
            generated_utc=generated,
            inputs={
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase209_model_spec": str(phase209_dir / "phase209_model_fit_spec.csv"),
                "phase209_feature_contract": str(phase209_dir / "phase209_feature_set_contract.csv"),
                "phase209_acceptance": str(phase209_dir / "phase209_model_fit_precommit_acceptance_summary.csv"),
            },
            parameters={
                "ridge_lambda": str(RIDGE_LAMBDA),
                "rng_seed": str(RNG_SEED),
                "feature_columns": ";".join(feature_columns),
                "target_columns": ";".join(target_columns),
                "allowed_splits": "train;validation",
                "sealed_test_rows_used": "0",
                "strategy_replay_allowed": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "design_inventory": str(output_dir / "phase210_design_matrix_partition_inventory.csv"),
                "metrics": str(output_dir / "phase210_train_validation_model_metrics.csv"),
                "coefficients": str(output_dir / "phase210_model_coefficient_ledger.csv"),
                "negative_controls": str(output_dir / "phase210_negative_control_metrics.csv"),
                "forbidden": str(output_dir / "phase210_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase210_train_validation_model_fit_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase210_train_validation_model_fit_acceptance_summary.csv"),
                "report": str(output_dir / "phase210_train_validation_model_fit_dry_run_report.md"),
            },
            scenario_ids="phase210_train_validation_model_fit_dry_run_no_replay_no_test",
            cost_model_version="zerodha_equity_cost_catalog_phase180_bound_no_replay",
            latency_model_version="phase180_latency_slippage_catalog_bound_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase210_train_validation_model_fit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase210 train/validation model-fit dry run without replay/test.")
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase209-dir", type=Path, default=DEFAULT_PHASE209_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase210(args.phase176_dir, args.phase181_dir, args.phase209_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

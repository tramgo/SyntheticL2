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
DEFAULT_PHASE214_DIR = Path("outputs/phase214")
DEFAULT_PHASE218_DIR = Path("outputs/phase218")
DEFAULT_OUTPUT_DIR = Path("outputs/phase219")
JOIN_KEYS = ["bucket_ms", "trade_date", "exchange", "symbol", "horizon_sec"]
RIDGE_LAMBDA = 1.0
RNG_SEED = 219
FORBIDDEN_OUTPUTS = "strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_design_matrix_export;row_level_prediction_export"
NEXT_ACTION = "run_phase220_event_only_model_fit_validation_interpretation_no_replay_no_test"


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


def split_columns(value: Any) -> list[str]:
    return [c.strip() for c in str(value).split(";") if c.strip()]


def partition_key(row: dict[str, Any]) -> tuple[int, str, str, str]:
    return (as_int(row.get("horizon_sec", 0)), str(row.get("trade_date", "")), str(row.get("exchange", "")), str(row.get("symbol", "")))


def feature_columns_by_horizon(feature_contract: pd.DataFrame) -> dict[int, list[str]]:
    mapping: dict[int, set[str]] = {}
    if feature_contract.empty:
        return {}
    allowed = feature_contract[pd.to_numeric(feature_contract["eligible_for_phase219_fit_dry_run"], errors="coerce").fillna(0).astype(int).eq(1)] if "eligible_for_phase219_fit_dry_run" in feature_contract.columns else feature_contract
    for row in allowed.to_dict("records"):
        horizon = as_int(row.get("horizon_sec", 0))
        mapping.setdefault(horizon, set()).update(split_columns(row.get("required_columns", "")))
    return {horizon: sorted(cols) for horizon, cols in mapping.items()}


def load_event_only_matrices(feature_inventory: pd.DataFrame, label_inventory: pd.DataFrame, targets: pd.DataFrame, feature_map: dict[int, list[str]]) -> tuple[dict[int, dict[str, pd.DataFrame]], pd.DataFrame]:
    target_horizons = sorted({as_int(v) for v in targets["horizon_sec"].dropna().tolist()}) if not targets.empty else []
    target_columns = sorted(set(targets["label_name"].dropna().astype(str).tolist())) if not targets.empty else []
    feature_paths = {partition_key(row): Path(str(row.get("parquet_file", ""))) for row in feature_inventory.to_dict("records")}
    usable_labels = label_inventory[
        label_inventory["split_role"].astype(str).isin(["train", "validation"])
        & pd.to_numeric(label_inventory["horizon_sec"], errors="coerce").fillna(-1).astype(int).isin(target_horizons)
    ] if not label_inventory.empty else pd.DataFrame()
    matrix_parts: dict[int, dict[str, list[pd.DataFrame]]] = {}
    inventory_rows: list[dict[str, Any]] = []
    parquet_columns_cache: dict[Path, list[str]] = {}
    for row in usable_labels.to_dict("records"):
        key = partition_key(row)
        horizon = key[0]
        split_role = str(row.get("split_role", ""))
        feature_path = feature_paths.get(key)
        label_path = Path(str(row.get("label_file", "")))
        feature_cols = feature_map.get(horizon, [])
        if feature_path is None or not feature_path.exists() or not label_path.exists() or not feature_cols:
            inventory_rows.append(
                {
                    "horizon_sec": horizon,
                    "trade_date": key[1],
                    "exchange": key[2],
                    "symbol": key[3],
                    "split_role": split_role,
                    "feature_file_exists": int(feature_path is not None and feature_path.exists()),
                    "label_file_exists": int(label_path.exists()),
                    "event_only_joined_rows": 0,
                    "test_rows_used": 0,
                }
            )
            continue
        if feature_path not in parquet_columns_cache:
            parquet_columns_cache[feature_path] = pd.read_parquet(feature_path).columns.astype(str).tolist()
        if label_path not in parquet_columns_cache:
            parquet_columns_cache[label_path] = pd.read_parquet(label_path).columns.astype(str).tolist()
        available_feature_cols = [c for c in JOIN_KEYS + feature_cols if c in parquet_columns_cache[feature_path]]
        available_label_cols = [c for c in JOIN_KEYS + ["split_role", "event_surprise_bucket"] + target_columns if c in parquet_columns_cache[label_path]]
        features = pd.read_parquet(feature_path, columns=available_feature_cols)
        labels = pd.read_parquet(label_path, columns=available_label_cols)
        if "event_surprise_bucket" in labels.columns:
            labels = labels[pd.to_numeric(labels["event_surprise_bucket"], errors="coerce").fillna(0).astype(int).eq(1)]
        joined = features.merge(labels, on=JOIN_KEYS, how="inner")
        for col in feature_cols:
            if col not in joined.columns:
                joined[col] = 0.0
        joined[feature_cols] = joined[feature_cols].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)
        for col in target_columns:
            if col in joined.columns:
                joined[col] = pd.to_numeric(joined[col], errors="coerce").fillna(0).astype(int)
        keep = JOIN_KEYS + ["split_role"] + feature_cols + [c for c in target_columns if c in joined.columns]
        joined = joined[keep]
        matrix_parts.setdefault(horizon, {}).setdefault(split_role, []).append(joined)
        inventory_rows.append(
            {
                "horizon_sec": horizon,
                "trade_date": key[1],
                "exchange": key[2],
                "symbol": key[3],
                "split_role": split_role,
                "feature_file_exists": 1,
                "label_file_exists": 1,
                "event_only_joined_rows": len(joined),
                "test_rows_used": 0,
            }
        )
    matrices: dict[int, dict[str, pd.DataFrame]] = {}
    for horizon, split_map in matrix_parts.items():
        matrices[horizon] = {}
        for split_role, frames in split_map.items():
            matrices[horizon][split_role] = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    return matrices, pd.DataFrame(inventory_rows)


def transform_features(frame: pd.DataFrame, columns: list[str], model_family: str) -> pd.DataFrame:
    data = frame[columns].copy()
    if "sparse_classification" in model_family:
        data = data.abs()
    elif "tree_or_stump" in model_family:
        data = data.rank(pct=True)
    return data.replace([np.inf, -np.inf], np.nan).fillna(0.0)


def fit_ridge(train: pd.DataFrame, feature_columns: list[str], target: str, model_family: str, shuffle: bool = False) -> dict[str, Any]:
    clean = train.dropna(subset=[target]).copy()
    x_raw = transform_features(clean, feature_columns, model_family).to_numpy(dtype=float)
    y = pd.to_numeric(clean[target], errors="coerce").fillna(0).to_numpy(dtype=float)
    if shuffle:
        rng = np.random.default_rng(RNG_SEED)
        y = rng.permutation(y)
    means = x_raw.mean(axis=0) if len(x_raw) else np.zeros(len(feature_columns))
    stds = x_raw.std(axis=0) if len(x_raw) else np.ones(len(feature_columns))
    stds = np.where(stds <= 1e-12, 1.0, stds)
    x = (x_raw - means) / stds
    design = np.column_stack([np.ones(len(x)), x]) if len(x) else np.zeros((0, len(feature_columns) + 1))
    penalty = np.eye(design.shape[1]) * RIDGE_LAMBDA
    penalty[0, 0] = 0.0
    beta = np.linalg.pinv(design.T @ design + penalty) @ design.T @ y if len(design) else np.zeros(len(feature_columns) + 1)
    return {"target": target, "feature_columns": feature_columns, "model_family": model_family, "means": means, "stds": stds, "beta": beta, "train_rows": len(clean), "shuffle_control": int(shuffle)}


def score_model(model: dict[str, Any], frame: pd.DataFrame, split_role: str) -> dict[str, Any]:
    target = str(model["target"])
    clean = frame.dropna(subset=[target]).copy()
    y = pd.to_numeric(clean[target], errors="coerce").fillna(0).to_numpy(dtype=float)
    x_raw = transform_features(clean, model["feature_columns"], str(model["model_family"])).to_numpy(dtype=float)
    x = (x_raw - model["means"]) / model["stds"] if len(x_raw) else np.zeros((0, len(model["feature_columns"])))
    design = np.column_stack([np.ones(len(x)), x]) if len(x) else np.zeros((0, len(model["feature_columns"]) + 1))
    pred = np.clip(design @ model["beta"], 0.0, 1.0) if len(design) else np.array([])
    base = np.repeat(np.mean(y), len(y)) if len(y) else np.array([])
    err = pred - y
    base_err = base - y
    y_std = float(np.std(y)) if len(y) else 0.0
    pred_std = float(np.std(pred)) if len(pred) else 0.0
    corr = float(np.corrcoef(y, pred)[0, 1]) if len(y) > 2 and y_std > 1e-12 and pred_std > 1e-12 else 0.0
    return {
        "split_role": split_role,
        "rows": len(clean),
        "positive_rate": float(np.mean(y)) if len(y) else np.nan,
        "prediction_mean": float(np.mean(pred)) if len(pred) else np.nan,
        "mse": float(np.mean(err * err)) if len(err) else np.nan,
        "base_rate_mse": float(np.mean(base_err * base_err)) if len(base_err) else np.nan,
        "mse_improvement_vs_base": float(np.mean(base_err * base_err) - np.mean(err * err)) if len(err) else np.nan,
        "binary_accuracy": float(((pred >= 0.5).astype(int) == (y >= 0.5).astype(int)).mean()) if len(y) else np.nan,
        "correlation": corr,
    }


def build_fits(matrices: dict[int, dict[str, pd.DataFrame]], model_specs: pd.DataFrame, targets: pd.DataFrame, feature_map: dict[int, list[str]]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    metrics: list[dict[str, Any]] = []
    coefs: list[dict[str, Any]] = []
    controls: list[dict[str, Any]] = []
    for target_row in targets.to_dict("records"):
        target = str(target_row.get("label_name", ""))
        horizon = as_int(target_row.get("horizon_sec", 0))
        train = matrices.get(horizon, {}).get("train", pd.DataFrame())
        validation = matrices.get(horizon, {}).get("validation", pd.DataFrame())
        feature_columns = feature_map.get(horizon, [])
        if train.empty or validation.empty or target not in train.columns or target not in validation.columns or not feature_columns:
            continue
        for spec in model_specs.to_dict("records"):
            spec_id = str(spec.get("phase218_model_spec_id", ""))
            family = str(spec.get("model_family", ""))
            model_id = f"P219_{spec_id}_{target}_H{horizon}s"
            model = fit_ridge(train, feature_columns, target, family, shuffle=False)
            shuffled = fit_ridge(train, feature_columns, target, family, shuffle=True)
            for split_role, frame in [("train", train), ("validation", validation)]:
                scored = score_model(model, frame, split_role)
                metrics.append(
                    {
                        "phase219_model_fit_id": model_id,
                        "phase218_model_spec_id": spec_id,
                        "model_family": family,
                        "target_label": target,
                        "horizon_sec": horizon,
                        "train_rows_used_for_fit": model["train_rows"],
                        "test_rows_used": 0,
                        "strategy_replay_allowed": 0,
                        "promotion_allowed": 0,
                        **scored,
                    }
                )
            validation_main = score_model(model, validation, "validation")
            validation_shuffle = score_model(shuffled, validation, "validation")
            controls.append(
                {
                    "phase219_control_id": f"P219_BASE_RATE_{model_id}",
                    "phase219_model_fit_id": model_id,
                    "control_type": "event_only_base_rate",
                    "validation_rows": validation_main["rows"],
                    "validation_mse": validation_main["base_rate_mse"],
                    "validation_binary_accuracy": np.nan,
                    "test_rows_used": 0,
                    "strategy_replay_allowed": 0,
                }
            )
            controls.append(
                {
                    "phase219_control_id": f"P219_SHUFFLED_{model_id}",
                    "phase219_model_fit_id": model_id,
                    "control_type": "event_time_shuffle",
                    "validation_rows": validation_shuffle["rows"],
                    "validation_mse": validation_shuffle["mse"],
                    "validation_binary_accuracy": validation_shuffle["binary_accuracy"],
                    "test_rows_used": 0,
                    "strategy_replay_allowed": 0,
                }
            )
            for name, value in zip(["intercept"] + feature_columns, model["beta"].tolist()):
                coefs.append(
                    {
                        "phase219_model_fit_id": model_id,
                        "phase218_model_spec_id": spec_id,
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
                "emitted_in_phase219": 0,
                "allowed_in_phase219": 0,
                "rationale": "Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase218: pd.DataFrame, inventory: pd.DataFrame, metrics: pd.DataFrame, coefs: pd.DataFrame, controls: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase218_complete = as_int(metric_value(phase218, "phase218_event_only_model_fit_precommit_or_stop_complete", 0))
    dry_run_precommitted = as_int(metric_value(phase218, "phase218_model_fit_dry_run_precommitted_for_phase219", 0))
    model_fit_rows = int(metrics["phase219_model_fit_id"].nunique()) if not metrics.empty else 0
    validation_rows = int(metrics["split_role"].astype(str).eq("validation").sum()) if not metrics.empty else 0
    test_rows_used = 0
    for frame in [inventory, metrics, controls]:
        if not frame.empty and "test_rows_used" in frame.columns:
            test_rows_used += int(pd.to_numeric(frame["test_rows_used"], errors="coerce").fillna(0).sum())
    forbidden_emitted = int(pd.to_numeric(forbidden["emitted_in_phase219"], errors="coerce").fillna(0).sum()) if not forbidden.empty else 1
    replay_flags = 0
    for frame in [metrics, coefs, controls]:
        for col in ["strategy_replay_allowed", "test_replay_allowed_next", "promotion_allowed"]:
            if not frame.empty and col in frame.columns:
                replay_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P219_PHASE218_COMPLETE_AND_PRECOMMITTED", phase218_complete == 1 and dry_run_precommitted == 1, f"phase218_complete={phase218_complete}; dry_run_precommitted={dry_run_precommitted}", "hard"),
            ("P219_EVENT_ONLY_DESIGN_MATRIX_JOINED", int(inventory["event_only_joined_rows"].sum()) > 0 if not inventory.empty else False, f"event_only_joined_rows={int(inventory['event_only_joined_rows'].sum()) if not inventory.empty else 0}", "hard"),
            ("P219_MODEL_FITS_RECORDED", model_fit_rows == 21, f"model_fit_rows={model_fit_rows}", "hard"),
            ("P219_VALIDATION_METRICS_RECORDED", validation_rows == 21, f"validation_metric_rows={validation_rows}", "hard"),
            ("P219_CONTROLS_RECORDED", len(controls) == 42, f"control_rows={len(controls)}", "hard"),
            ("P219_TEST_REPLAY_AND_TEST_ROWS_CLOSED", test_rows_used == 0, f"test_rows_used={test_rows_used}", "hard"),
            ("P219_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and replay_flags == 0, f"forbidden_emitted={forbidden_emitted}; replay_flags={replay_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(inventory: pd.DataFrame, metrics: pd.DataFrame, coefs: pd.DataFrame, controls: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase219_event_only_partition_rows", len(inventory), "Train/validation event-only joined partition rows"),
            ("phase219_event_only_joined_rows", int(inventory["event_only_joined_rows"].sum()) if not inventory.empty else 0, "Joined event-only design-matrix rows across partition inventory"),
            ("phase219_model_fit_rows", int(metrics["phase219_model_fit_id"].nunique()) if not metrics.empty else 0, "Unique model/target/horizon fits"),
            ("phase219_metric_rows", len(metrics), "Train/validation metric rows"),
            ("phase219_validation_metric_rows", int(metrics["split_role"].astype(str).eq("validation").sum()) if not metrics.empty else 0, "Validation metric rows"),
            ("phase219_coefficient_rows", len(coefs), "Coefficient rows"),
            ("phase219_control_rows", len(controls), "Base-rate and shuffled-control rows"),
            ("phase219_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase219_gate_rows", len(gates), "Gates evaluated"),
            ("phase219_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase219_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase219_event_only_train_validation_model_fit_dry_run_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase219 completed"),
            ("phase219_model_fit_execution", 1, "Train/validation event-only model fitting executed"),
            ("phase219_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase219_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase219_test_rows_used", 0, "No sealed test rows used"),
            ("phase219_promotion_allowed", 0, "No promotion opened"),
            ("phase219_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase219_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase219_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase219_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase219 Event-only Train/Validation Model-fit Dry Run",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase219 executes the Phase218-precommitted train/validation event-only model-fit dry run.",
        "It joins Phase176 receive-flow features with Phase214 event-surprise labels, filters to event_surprise_bucket == 1, fits aggregate diagnostic models, and writes only aggregate metrics/coefficient/control ledgers.",
        "It does not export row-level design matrices or predictions, use sealed test rows, run strategy replay, emit orders/fills/P&L, promote anything, open paper/live acceptance, or make profitability claims.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase219_event_only_train_validation_model_fit_dry_run_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase219(phase176_dir: Path, phase214_dir: Path, phase218_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase218 = read_csv(phase218_dir / "phase218_model_fit_precommit_acceptance_summary.csv")
    model_specs = read_csv(phase218_dir / "phase218_model_family_spec.csv")
    targets = read_csv(phase218_dir / "phase218_event_only_target_contract.csv")
    feature_contract = read_csv(phase218_dir / "phase218_event_only_feature_contract.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = read_csv(phase214_dir / "phase214_label_partition_inventory.csv")
    feature_map = feature_columns_by_horizon(feature_contract)
    matrices, inventory = load_event_only_matrices(feature_inventory, label_inventory, targets, feature_map)
    metrics, coefs, controls = build_fits(matrices, model_specs, targets, feature_map)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase218, inventory, metrics, coefs, controls, forbidden)
    acceptance = build_acceptance(inventory, metrics, coefs, controls, forbidden, gates)

    inventory.to_csv(output_dir / "phase219_event_only_design_matrix_partition_inventory.csv", index=False)
    metrics.to_csv(output_dir / "phase219_train_validation_model_metrics.csv", index=False)
    coefs.to_csv(output_dir / "phase219_model_coefficient_ledger.csv", index=False)
    controls.to_csv(output_dir / "phase219_control_metrics.csv", index=False)
    forbidden.to_csv(output_dir / "phase219_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase219_model_fit_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase219_model_fit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Event-only Design Matrix Partition Inventory": inventory,
            "Train/Validation Model Metrics": metrics,
            "Model Coefficient Ledger": coefs,
            "Control Metrics": controls,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase219_event_only_train_validation_model_fit_dry_run_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase219_event_only_train_validation_model_fit_dry_run",
            generated_utc=generated,
            inputs={
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase214_label_inventory": str(phase214_dir / "phase214_label_partition_inventory.csv"),
                "phase218_acceptance": str(phase218_dir / "phase218_model_fit_precommit_acceptance_summary.csv"),
                "phase218_model_specs": str(phase218_dir / "phase218_model_family_spec.csv"),
                "phase218_targets": str(phase218_dir / "phase218_event_only_target_contract.csv"),
                "phase218_features": str(phase218_dir / "phase218_event_only_feature_contract.csv"),
            },
            parameters={
                "ridge_lambda": str(RIDGE_LAMBDA),
                "rng_seed": str(RNG_SEED),
                "event_only_filter": "event_surprise_bucket == 1",
                "allowed_splits": "train;validation",
                "model_fit_execution": "1",
                "sealed_test_rows_used": "0",
                "strategy_replay_allowed": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "inventory": str(output_dir / "phase219_event_only_design_matrix_partition_inventory.csv"),
                "metrics": str(output_dir / "phase219_train_validation_model_metrics.csv"),
                "coefficients": str(output_dir / "phase219_model_coefficient_ledger.csv"),
                "controls": str(output_dir / "phase219_control_metrics.csv"),
                "forbidden": str(output_dir / "phase219_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase219_model_fit_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase219_model_fit_acceptance_summary.csv"),
                "report": str(output_dir / "phase219_event_only_train_validation_model_fit_dry_run_report.md"),
            },
            scenario_ids="phase219_event_only_train_validation_model_fit_dry_run_no_replay_no_test",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase219_model_fit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase219 event-only train/validation model-fit dry run without replay/test.")
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase214-dir", type=Path, default=DEFAULT_PHASE214_DIR)
    parser.add_argument("--phase218-dir", type=Path, default=DEFAULT_PHASE218_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase219(args.phase176_dir, args.phase214_dir, args.phase218_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

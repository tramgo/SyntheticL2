from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE176_DIR = Path("outputs/phase176")
DEFAULT_PHASE206_DIR = Path("outputs/phase206")
DEFAULT_OUTPUT_DIR = Path("outputs/phase207")
FORBIDDEN_OUTPUTS = "model_fit;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening"


FEATURE_COLUMN_MAP = {
    "P206_RECEIVE_EVENT_RATE_ZSCORE": "receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days",
    "P206_QUOTE_CHURN_RATE": "quote_churn_count",
    "P206_DEPTH_REFRESH_INTENSITY": "depth_refresh_count;top5_qty_imbalance",
    "P206_STALE_QUOTE_DURATION": "stale_quote_duration_ms",
    "P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY": "cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols",
    "P206_RECEIVE_FLOW_REGIME_STATE": "receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share",
}


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


def sample_schema_columns(inventory: pd.DataFrame, max_files: int = 8) -> set[str]:
    columns: set[str] = set()
    if inventory.empty or "parquet_file" not in inventory.columns:
        return columns
    for rel in inventory["parquet_file"].dropna().astype(str).head(max_files):
        path = Path(rel)
        if not path.exists():
            continue
        try:
            frame = pd.read_parquet(path)
        except Exception:
            continue
        columns.update(frame.columns.astype(str).tolist())
    return columns


def build_feature_matrix(feature_catalog: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    schema_cols = sample_schema_columns(inventory)
    horizons = sorted(pd.to_numeric(inventory.get("horizon_sec", pd.Series(dtype=int)), errors="coerce").dropna().astype(int).unique().tolist())
    rows: list[dict[str, Any]] = []
    for feature in feature_catalog.to_dict("records"):
        feature_id = str(feature.get("phase206_feature_id", ""))
        required_cols = [c for c in FEATURE_COLUMN_MAP.get(feature_id, "").split(";") if c]
        for horizon in horizons:
            part = inventory.loc[pd.to_numeric(inventory["horizon_sec"], errors="coerce").astype("Int64").eq(horizon)]
            present_cols = [c for c in required_cols if c in schema_cols]
            rows.append(
                {
                    "phase207_matrix_id": f"{feature_id}_H{horizon}s",
                    "phase206_feature_id": feature_id,
                    "feature_family": feature.get("feature_family", ""),
                    "horizon_sec": horizon,
                    "required_columns": ";".join(required_cols),
                    "present_columns": ";".join(present_cols),
                    "required_column_count": len(required_cols),
                    "present_column_count": len(present_cols),
                    "feature_available": int(len(required_cols) > 0 and len(present_cols) == len(required_cols)),
                    "partition_rows": int(len(part)),
                    "trade_dates": int(part["trade_date"].nunique()) if "trade_date" in part.columns else 0,
                    "symbols": int(part["symbol"].nunique()) if "symbol" in part.columns else 0,
                    "total_feature_rows": int(pd.to_numeric(part.get("rows", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()),
                    "model_fit_allowed": 0,
                    "strategy_replay_allowed": 0,
                    "test_replay_allowed_next": 0,
                }
            )
    return pd.DataFrame(rows)


def build_target_exclusion_ablation_spec(feature_matrix: pd.DataFrame) -> pd.DataFrame:
    synchrony = feature_matrix[feature_matrix["phase206_feature_id"].astype(str).eq("P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY")]
    return pd.DataFrame(
        [
            {
                "ablation_id": "P207_TARGET_SYMBOL_EXCLUDED_SYNCHRONY",
                "feature_id": "P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY",
                "required_before_model_fit": 1,
                "spec": "Future synchrony features must recompute cross_symbol_arrival_count/share excluding the target symbol before any model fitting.",
                "matrix_rows_available": int(len(synchrony)),
                "model_fit_allowed": 0,
                "strategy_replay_allowed": 0,
            },
            {
                "ablation_id": "P207_SHUFFLED_TIME_NEGATIVE_CONTROL",
                "feature_id": "all_phase206_features",
                "required_before_model_fit": 1,
                "spec": "Any future model phase must include shuffled-time/date negative controls before edge interpretation.",
                "matrix_rows_available": int(len(feature_matrix)),
                "model_fit_allowed": 0,
                "strategy_replay_allowed": 0,
            },
            {
                "ablation_id": "P207_BLOCKED_FORM_OVERLAP_CONTROL",
                "feature_id": "all_phase206_features",
                "required_before_model_fit": 1,
                "spec": "Any future model phase must prove no reuse of Phase164 forms, fixed Phase167 S08 score, or passive queue replay.",
                "matrix_rows_available": int(len(feature_matrix)),
                "model_fit_allowed": 0,
                "strategy_replay_allowed": 0,
            },
        ]
    )


def build_leakage_terminology_audit(feature_catalog: pd.DataFrame, feature_matrix: pd.DataFrame) -> pd.DataFrame:
    depth_rows = feature_catalog[feature_catalog["feature_family"].astype(str).eq("top_five_depth_churn")]
    leakage_rows = int(feature_catalog["leakage_control"].astype(str).ne("").sum()) if "leakage_control" in feature_catalog.columns else 0
    return pd.DataFrame(
        [
            {
                "audit_id": "P207_LEAKAGE_CONTROLS_PRESENT",
                "audit_pass": int(leakage_rows == len(feature_catalog) and len(feature_catalog) > 0),
                "evidence": f"leakage_rows={leakage_rows}; feature_rows={len(feature_catalog)}",
                "model_fit_allowed": 0,
            },
            {
                "audit_id": "P207_TOP_FIVE_TERMINOLOGY_CORRECT",
                "audit_pass": int(not depth_rows.empty and depth_rows["phase206_allowed_role"].astype(str).str.contains("top_five_market_by_price", regex=False).all()),
                "evidence": "depth features are top-five market-by-price, not L3/L4 order-by-order",
                "model_fit_allowed": 0,
            },
            {
                "audit_id": "P207_MATRIX_NO_MODEL_OR_REPLAY_FLAGS",
                "audit_pass": int(
                    feature_matrix["model_fit_allowed"].astype(int).sum() == 0
                    and feature_matrix["strategy_replay_allowed"].astype(int).sum() == 0
                    and feature_matrix["test_replay_allowed_next"].astype(int).sum() == 0
                ) if not feature_matrix.empty else 0,
                "evidence": "all matrix model/replay flags are 0",
                "model_fit_allowed": 0,
            },
        ]
    )


def build_gates(phase206: pd.DataFrame, feature_matrix: pd.DataFrame, ablations: pd.DataFrame, audit: pd.DataFrame) -> pd.DataFrame:
    phase206_complete = as_int(metric_value(phase206, "phase206_nonoverlap_feature_contract_complete", 0))
    available_rows = int(feature_matrix["feature_available"].astype(int).sum()) if not feature_matrix.empty else 0
    forbidden_sum = 0
    for frame in [feature_matrix, ablations, audit]:
        for col in ["model_fit_allowed", "strategy_replay_allowed", "test_replay_allowed_next"]:
            if not frame.empty and col in frame.columns:
                forbidden_sum += int(frame[col].astype(int).sum())
    return pd.DataFrame(
        [
            ("P207_PHASE206_COMPLETE", phase206_complete == 1, f"phase206_complete={phase206_complete}", "hard"),
            ("P207_FEATURE_MATRIX_RECORDED", len(feature_matrix) >= 6, f"matrix_rows={len(feature_matrix)}", "hard"),
            ("P207_FEATURE_AVAILABILITY_POSITIVE", available_rows >= 6, f"available_rows={available_rows}", "hard"),
            ("P207_TARGET_EXCLUSION_ABLATION_SPEC_RECORDED", len(ablations) == 3 and ablations["required_before_model_fit"].astype(int).eq(1).all(), f"ablation_rows={len(ablations)}", "hard"),
            ("P207_LEAKAGE_TERMINOLOGY_AUDIT_PASSED", not audit.empty and audit["audit_pass"].astype(int).all(), f"audit_pass_rows={int(audit['audit_pass'].astype(int).sum()) if not audit.empty else 0}", "hard"),
            ("P207_NO_MODEL_FIT_REPLAY_OR_PROMOTION", forbidden_sum == 0, f"forbidden_flag_sum={forbidden_sum}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(feature_matrix: pd.DataFrame, ablations: pd.DataFrame, audit: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase207_feature_matrix_rows", len(feature_matrix), "Feature/horizon matrix rows"),
            ("phase207_feature_available_rows", int(feature_matrix["feature_available"].astype(int).sum()) if not feature_matrix.empty else 0, "Available feature/horizon rows"),
            ("phase207_trade_dates_max", int(feature_matrix["trade_dates"].max()) if not feature_matrix.empty else 0, "Maximum trade-date coverage"),
            ("phase207_symbols_max", int(feature_matrix["symbols"].max()) if not feature_matrix.empty else 0, "Maximum symbol coverage"),
            ("phase207_target_exclusion_ablation_rows", len(ablations), "Ablation spec rows"),
            ("phase207_leakage_terminology_audit_rows", len(audit), "Leakage/terminology audit rows"),
            ("phase207_gate_rows", len(gates), "Gates evaluated"),
            ("phase207_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase207_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase207_feature_matrix_precommit_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase207 completed"),
            ("phase207_model_fit_allowed", 0, "No model fitting opened"),
            ("phase207_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase207_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase207_promotion_allowed", 0, "No promotion opened"),
            ("phase207_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase207_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase207_next_best_action", "run_phase208_feature_matrix_quality_gate_no_model_no_replay", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase207 Allowed Feature Matrix Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase207 builds an allowed feature/horizon availability matrix from the Phase206 catalog and Phase176 materialized features.",
        "It emits no model fit, no replay, no orders/fills/P&L, no promotion and no paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase207_allowed_feature_matrix_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase207(phase176_dir: Path, phase206_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    phase206 = read_csv(phase206_dir / "phase206_nonoverlap_feature_acceptance_summary.csv")
    feature_catalog = read_csv(phase206_dir / "phase206_selected_source_feature_catalog.csv")
    feature_matrix = build_feature_matrix(feature_catalog, inventory)
    ablations = build_target_exclusion_ablation_spec(feature_matrix)
    audit = build_leakage_terminology_audit(feature_catalog, feature_matrix)
    gates = build_gates(phase206, feature_matrix, ablations, audit)
    acceptance = build_acceptance(feature_matrix, ablations, audit, gates)

    feature_matrix.to_csv(output_dir / "phase207_allowed_feature_matrix.csv", index=False)
    ablations.to_csv(output_dir / "phase207_target_exclusion_ablation_spec.csv", index=False)
    audit.to_csv(output_dir / "phase207_leakage_terminology_audit.csv", index=False)
    gates.to_csv(output_dir / "phase207_feature_matrix_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase207_feature_matrix_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Allowed Feature Matrix": feature_matrix,
            "Target Exclusion and Negative-control Ablation Spec": ablations,
            "Leakage and Terminology Audit": audit,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase207_allowed_feature_matrix_precommit_no_model_no_replay",
        **reproducibility_fields(
            artifact_id="phase207_allowed_feature_matrix_precommit",
            generated_utc=generated,
            inputs={
                "phase176_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase206_acceptance": str(phase206_dir / "phase206_nonoverlap_feature_acceptance_summary.csv"),
                "phase206_feature_catalog": str(phase206_dir / "phase206_selected_source_feature_catalog.csv"),
            },
            parameters={
                "precommit_scope": "allowed_feature_matrix_no_model_no_replay",
                "model_fit_allowed": "0",
                "strategy_replay_allowed": "0",
                "test_replay_allowed_next": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "feature_matrix": str(output_dir / "phase207_allowed_feature_matrix.csv"),
                "ablations": str(output_dir / "phase207_target_exclusion_ablation_spec.csv"),
                "audit": str(output_dir / "phase207_leakage_terminology_audit.csv"),
                "gates": str(output_dir / "phase207_feature_matrix_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase207_feature_matrix_acceptance_summary.csv"),
                "report": str(output_dir / "phase207_allowed_feature_matrix_precommit_report.md"),
            },
            scenario_ids="phase207_allowed_feature_matrix_precommit_no_model_no_replay",
            cost_model_version="not_applicable_no_strategy_replay",
            latency_model_version="not_applicable_no_strategy_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase207_feature_matrix_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Phase207 allowed feature matrix precommit without model/replay.")
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase206-dir", type=Path, default=DEFAULT_PHASE206_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase207(args.phase176_dir, args.phase206_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

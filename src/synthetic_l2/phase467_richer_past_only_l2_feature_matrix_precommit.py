from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE466_DIR = Path("outputs/phase466")
DEFAULT_PHASE462_DIR = Path("outputs/phase462")
DEFAULT_OUTPUT_DIR = Path("outputs/phase467")

THESIS_ID = "P467_RICHER_PAST_ONLY_L1_L5_FEATURE_MATRIX_PRECOMMIT"
NEXT_ACTION = "run_phase468_materialize_richer_past_only_l1_l5_feature_matrix_no_model_no_pnl"

LOOKBACK_TICKS = 20
ENTRY_INDEX = 20
HORIZON_TICKS = 240
MIN_ABS_FORWARD_MOVE_BPS = 2.0

BASE_SCHEMA_COLUMNS = [
    "exchange_timestamp_ms",
    "trade_date",
    "exchange",
    "symbol",
    "last_price",
    "last_traded_quantity",
    "volume_traded",
    "total_buy_quantity",
    "total_sell_quantity",
]
L1_L5_SCHEMA_COLUMNS = []
for _level in range(1, 6):
    L1_L5_SCHEMA_COLUMNS.extend(
        [
            f"buy_{_level}_price",
            f"buy_{_level}_quantity",
            f"buy_{_level}_orders",
            f"sell_{_level}_price",
            f"sell_{_level}_quantity",
            f"sell_{_level}_orders",
        ]
    )
REQUIRED_SCHEMA_COLUMNS = BASE_SCHEMA_COLUMNS + L1_L5_SCHEMA_COLUMNS

FEATURES = [
    ("recent_mid_return_bps", "base", "mid return from lookback start to entry", 0),
    ("spread_bps", "base", "entry best ask minus best bid in bps", 0),
    ("l1_imbalance", "base", "entry level-1 quantity imbalance", 0),
    ("l25_imbalance", "base", "entry levels 2-5 quantity imbalance", 1),
    ("volume_delta_lookback", "base", "entry volume minus lookback-start volume", 0),
    ("l1_l5_bid_depth_slope", "depth_curve_shape", "entry bid quantity slope over levels 1-5", 1),
    ("l1_l5_ask_depth_slope", "depth_curve_shape", "entry ask quantity slope over levels 1-5", 1),
    ("l1_l5_depth_concentration", "depth_curve_shape", "entry L1 depth share of total L1-L5 depth", 1),
    ("l25_order_imbalance", "depth_curve_shape", "entry levels 2-5 order-count imbalance", 1),
    ("ofi_l1_lookback", "ofi_and_depth_churn", "signed L1 quantity change over lookback", 0),
    ("ofi_l25_lookback", "ofi_and_depth_churn", "signed levels 2-5 quantity change over lookback", 1),
    ("l25_replenishment_events", "ofi_and_depth_churn", "count of positive levels 2-5 depth changes before entry", 1),
    ("l25_withdrawal_events", "ofi_and_depth_churn", "count of negative levels 2-5 depth changes before entry", 1),
    ("microprice_l1_minus_mid_bps", "microprice_pressure", "L1 microprice displacement from mid at entry", 0),
    ("microprice_l25_minus_mid_bps", "microprice_pressure", "levels 2-5 microprice displacement from mid at entry", 1),
    ("spread_change_lookback_bps", "spread_regime_context", "entry spread minus lookback-start spread", 0),
    ("spread_mean_lookback_bps", "spread_regime_context", "mean spread over past-only lookback", 0),
    ("trade_qty_sum_lookback", "volume_acceleration", "sum last_traded_quantity over lookback", 0),
    ("trade_qty_accel_lookback", "volume_acceleration", "second-half minus first-half traded quantity over lookback", 0),
    ("minute_of_day", "time_of_day_context", "known exchange timestamp minute bucket", 0),
]
FORBIDDEN_AS_FEATURES = [
    "forward_return_bps",
    "abs_forward_return_bps",
    "label_side",
    "move_candidate",
    "exit_price",
    "exit_row",
]


def scalar(summary: pd.DataFrame, metric: str, default: Any = "") -> Any:
    return metric_value(summary, metric, default) if not summary.empty else default


def cval(contract: pd.DataFrame, key: str, default: str = "") -> str:
    rows = contract.loc[contract["contract_id"].astype(str).eq(key), "contract_value"].astype(str).tolist()
    return rows[0] if rows else default


def hash_frame(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_json(orient="records", date_format="iso").encode("utf-8")).hexdigest()


def feature_contract() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "feature_name": name,
                "feature_family": family,
                "timestamp_rule": "computed only from rows <= entry row inside each candidate window",
                "description": description,
                "uses_l2_l5_depth": uses_l2_l5,
                "allowed_as_model_input": 1,
            }
            for name, family, description, uses_l2_l5 in FEATURES
        ]
    )


def schema_evidence(selected_files: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for item in selected_files.to_dict("records"):
        path = Path(item["path"])
        if not path.exists():
            rows.append({"path": str(path), "exists": 0, "schema_columns": 0, "missing_required_columns": ";".join(REQUIRED_SCHEMA_COLUMNS)})
            continue
        names = set(pq.ParquetFile(path).schema.names)
        missing = [col for col in REQUIRED_SCHEMA_COLUMNS if col not in names]
        rows.append({"path": str(path), "exists": 1, "schema_columns": len(names), "missing_required_columns": ";".join(missing)})
    return pd.DataFrame(rows)


def build_contract(features: pd.DataFrame, selected_files: pd.DataFrame, schema: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("phase467_thesis_id", THESIS_ID, "Precommit thesis"),
        ("source_phase", "phase462_phase463_distributional_label_source", "Use same selected replacement source"),
        ("input_dense_root", cval(read_csv(DEFAULT_PHASE462_DIR / "phase462_frozen_phase463_contract.csv"), "replacement_dense_root"), "Dense root"),
        ("input_profile_id", cval(read_csv(DEFAULT_PHASE462_DIR / "phase462_frozen_phase463_contract.csv"), "replacement_profile_id"), "Profile id"),
        ("selected_file_count", int(len(selected_files)), "Selected files"),
        ("selected_file_hash", hash_frame(selected_files), "Selected files hash"),
        ("required_schema_column_count", len(REQUIRED_SCHEMA_COLUMNS), "Required raw columns"),
        ("lookback_ticks", LOOKBACK_TICKS, "Past-only lookback"),
        ("entry_index", ENTRY_INDEX, "Entry row"),
        ("horizon_ticks", HORIZON_TICKS, "Forward label horizon retained for labels only"),
        ("min_abs_forward_move_bps", MIN_ABS_FORWARD_MOVE_BPS, "Move label floor"),
        ("allowed_features", ";".join(features["feature_name"].astype(str)), "Allowed richer features"),
        ("l2_l5_feature_count", int(features["uses_l2_l5_depth"].sum()), "Features using levels 2-5"),
        ("forbidden_feature_columns", ";".join(FORBIDDEN_AS_FEATURES), "Future/label columns forbidden as predictors"),
        ("feature_contract_hash", hash_frame(features), "Feature contract hash"),
        ("schema_evidence_hash", hash_frame(schema), "Schema evidence hash"),
        ("phase468_allowed_next", 1, "Allows matrix materialization only"),
        ("model_fit_allowed", 0, "No model fit in Phase467/468"),
        ("strategy_pnl_allowed", 0, "No strategy P&L"),
        ("strategy_promotion_allowed", 0, "No promotion"),
        ("paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("deployable_profitability_claim_allowed", 0, "No deployable claim"),
    ]
    return pd.DataFrame(rows, columns=["contract_id", "contract_value", "description"])


def build_gates(phase466: pd.DataFrame, selected_files: pd.DataFrame, features: pd.DataFrame, schema: pd.DataFrame) -> pd.DataFrame:
    feature_names = set(features["feature_name"].astype(str))
    gates = [
        ("P467_PHASE466_RICHER_FEATURE_PRECOMMIT_ALLOWED", as_int(scalar(phase466, "phase466_richer_past_only_feature_precommit_allowed", 0)) == 1, scalar(phase466, "phase466_richer_past_only_feature_precommit_allowed", 0), 1),
        ("P467_SELECTED_FILES_PRESENT", int(selected_files["exists"].sum()) == len(selected_files), int(selected_files["exists"].sum()), len(selected_files)),
        ("P467_REQUIRED_SCHEMA_PRESENT", schema["missing_required_columns"].astype(str).eq("").all(), int(schema["missing_required_columns"].astype(str).eq("").sum()), len(schema)),
        ("P467_FEATURE_COUNT_GE_20", len(features) >= 20, len(features), ">=20"),
        ("P467_L2_L5_FEATURE_COUNT_GE_8", int(features["uses_l2_l5_depth"].sum()) >= 8, int(features["uses_l2_l5_depth"].sum()), ">=8"),
        ("P467_BASE_PHASE465_FEATURES_RETAINED", {"recent_mid_return_bps", "spread_bps", "l1_imbalance", "l25_imbalance", "volume_delta_lookback"}.issubset(feature_names), ";".join(sorted(feature_names)), "base features included"),
        ("P467_FORBIDDEN_LABELS_NOT_FEATURES", set(FORBIDDEN_AS_FEATURES).isdisjoint(feature_names), ";".join(sorted(set(FORBIDDEN_AS_FEATURES) & feature_names)), "empty"),
        ("P467_MODEL_FIT_NOT_ALLOWED", True, "precommit_only", "no_model_fit"),
        ("P467_NO_STRATEGY_PNL", True, "precommit_only", "no_pnl"),
        ("P467_NO_PAPER_LIVE_OR_CLAIM", True, "promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(gates: pd.DataFrame, features: pd.DataFrame, selected_files: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    all_pass = int(hard_pass == hard_rows)
    rows = [
        ("phase467_richer_past_only_l1_l5_feature_matrix_precommit_complete", 1, "Phase467 precommit completed"),
        ("phase467_thesis_id", THESIS_ID, "Precommit thesis"),
        ("phase467_feature_count", int(len(features)), "Allowed feature count"),
        ("phase467_l2_l5_feature_count", int(features["uses_l2_l5_depth"].sum()), "Features using levels 2-5"),
        ("phase467_selected_file_count", int(len(selected_files)), "Selected files"),
        ("phase467_selected_files_present", int(selected_files["exists"].sum()), "Present selected files"),
        ("phase467_model_fit_generated", 0, "No model fit"),
        ("phase467_strategy_pnl_generated", 0, "No strategy P&L"),
        ("phase467_strategy_promotion_allowed", 0, "No promotion"),
        ("phase467_paper_or_live_acceptance_allowed", 0, "No paper/live"),
        ("phase467_deployable_profitability_claim_allowed", 0, "No deployable claim"),
        ("phase467_phase468_allowed_next", all_pass, "Allows richer matrix materialization only if all gates pass"),
        ("phase467_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
        ("phase467_hard_gate_rows", hard_rows, "Hard gates"),
        ("phase467_next_best_action", NEXT_ACTION if all_pass else "repair_phase467_feature_contract_before_materialization", "Recommended next action"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, acceptance: pd.DataFrame, contract: pd.DataFrame, features: pd.DataFrame, schema: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase467 Richer Past-Only L1-L5 Feature Matrix Precommit",
        "",
        "Phase467 freezes a richer past-only L1-L5 feature matrix before any additional model fit or P&L replay.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Frozen Phase468 Contract",
        "",
        _markdown_table(contract),
        "",
        "## Feature Contract",
        "",
        _markdown_table(features),
        "",
        "## Schema Evidence",
        "",
        _markdown_table(schema.head(25)),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "Boundary: Phase468 may materialize the richer matrix only. Model fitting and strategy P&L remain closed.",
    ]
    (output_dir / "phase467_richer_past_only_l1_l5_feature_matrix_precommit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase466_dir: Path = DEFAULT_PHASE466_DIR, phase462_dir: Path = DEFAULT_PHASE462_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase466 = read_csv(phase466_dir / "phase466_acceptance_summary.csv")
    selected = read_csv(phase462_dir / "phase462_selected_replacement_files.csv")
    features = feature_contract()
    schema = schema_evidence(selected)
    contract = build_contract(features, selected, schema)
    gates = build_gates(phase466, selected, features, schema)
    acceptance = build_acceptance(gates, features, selected)
    selected.to_csv(output_dir / "phase467_selected_files.csv", index=False)
    features.to_csv(output_dir / "phase467_feature_contract.csv", index=False)
    schema.to_csv(output_dir / "phase467_schema_evidence.csv", index=False)
    contract.to_csv(output_dir / "phase467_frozen_phase468_contract.csv", index=False)
    gates.to_csv(output_dir / "phase467_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase467_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, contract, features, schema, gates)
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase467_richer_past_only_l1_l5_feature_matrix_precommit",
        "contract_hash": hash_frame(contract),
        **reproducibility_fields(
            artifact_id="phase467_richer_past_only_l1_l5_feature_matrix_precommit",
            generated_utc=generated_utc,
            inputs={"phase466_acceptance_summary": str(phase466_dir / "phase466_acceptance_summary.csv")},
            parameters={"thesis_id": THESIS_ID, "lookback_ticks": LOOKBACK_TICKS, "feature_count": len(features)},
            outputs={"acceptance_summary": str(output_dir / "phase467_acceptance_summary.csv")},
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase467_precommit_no_execution",
        ),
    }
    (output_dir / "phase467_richer_past_only_l1_l5_feature_matrix_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase467 richer past-only L1-L5 feature matrix precommit.")
    parser.add_argument("--phase466-dir", type=Path, default=DEFAULT_PHASE466_DIR)
    parser.add_argument("--phase462-dir", type=Path, default=DEFAULT_PHASE462_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    out = run(args.phase466_dir, args.phase462_dir, args.output_dir)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()

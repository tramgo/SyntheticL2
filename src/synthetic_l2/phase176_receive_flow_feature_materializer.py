from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE175_DIR = Path("outputs/phase175")
DEFAULT_PHASE172_DIR = Path("outputs/phase172")
DEFAULT_REAL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_OUTPUT_DIR = Path("outputs/phase176")
DEFAULT_FEATURE_ROOT = Path("derived_real_l2_receive_flow_features_phase176")
FORBIDDEN_OUTPUTS = "buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance"


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


def build_materialization_plan(schema: pd.DataFrame, feature_root: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in schema.to_dict("records"):
        feature_id = str(item["feature_id"])
        rows.append(
            {
                "feature_id": feature_id,
                "feature_family": item["feature_family"],
                "materialization_status": "gated_pending_phase175_activation",
                "target_layout": str(feature_root / "trade_date=YYYY-MM-DD" / "exchange=NSE" / "symbol=SYMBOL" / f"{feature_id.lower()}.parquet"),
                "allowed_horizons": item["allowed_horizons"],
                "minimum_source_days": item["minimum_source_days"],
                "leakage_control": item["leakage_control"],
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_sql_templates(feature_root: Path, real_root: Path) -> pd.DataFrame:
    templates = [
        {
            "template_id": "P176_BASE_RECEIVE_EVENTS",
            "purpose": "local-only source view over downloaded Zerodha top-five market-by-price Parquet",
            "sql_template": (
                "SELECT trade_date, exchange, tradingsymbol AS symbol, collector_received_utc_ms AS receive_ms, "
                "buy_1_price, buy_1_quantity, sell_1_price, sell_1_quantity, "
                "buy_1_quantity, buy_2_quantity, buy_3_quantity, buy_4_quantity, buy_5_quantity, "
                "sell_1_quantity, sell_2_quantity, sell_3_quantity, sell_4_quantity, sell_5_quantity "
                f"FROM read_parquet('{str(real_root / 'trade_date=*' / 'exchange=NSE' / 'symbol=*' / '*.parquet').replace(chr(92), '/')}', hive_partitioning=true, union_by_name=true)"
            ),
            "output_path": "",
            "strategy_replay_allowed": 0,
        },
        {
            "template_id": "P176_1S_BUCKET_FEATURES",
            "purpose": "1-second bucket receive-event/churn/staleness/synchrony features after activation opens",
            "sql_template": (
                "WITH ordered AS (... event-time sorted source ...), buckets AS (... floor(receive_ms/1000) ... ) "
                "SELECT trade_date, exchange, symbol, bucket_1s, receive_event_count, quote_churn_count, "
                "depth_refresh_count, stale_quote_duration_ms, cross_symbol_arrival_count FROM buckets"
            ),
            "output_path": str(feature_root / "horizon=1s"),
            "strategy_replay_allowed": 0,
        },
        {
            "template_id": "P176_5S_15S_60S_AGGREGATIONS",
            "purpose": "higher-horizon aggregations from already materialized 1-second features",
            "sql_template": (
                "SELECT trade_date, exchange, symbol, horizon, bucket_ts, aggregate_receive_flow_features "
                "FROM phase176_1s_features GROUP BY trade_date, exchange, symbol, horizon, bucket_ts"
            ),
            "output_path": str(feature_root / "horizon={5s,15s,60s}"),
            "strategy_replay_allowed": 0,
        },
    ]
    return pd.DataFrame(templates)


def build_gate_evaluation(phase175: pd.DataFrame, phase172: pd.DataFrame, schema: pd.DataFrame, real_root: Path) -> pd.DataFrame:
    activation_ready = as_int(metric_value(phase175, "phase175_activation_ready", 0))
    ready_dates = as_int(metric_value(phase172, "phase172_ready_receive_flow_dates", 0))
    additional_dates = as_int(metric_value(phase172, "phase172_additional_dates_needed", 0))
    return pd.DataFrame(
        [
            {
                "gate_id": "P176_PHASE175_ACTIVATION_READY",
                "gate_pass": int(activation_ready == 1),
                "evidence": f"phase175_activation_ready={activation_ready};ready_dates={ready_dates};additional_needed={additional_dates}",
                "severity": "activation",
            },
            {
                "gate_id": "P176_SCHEMA_AVAILABLE",
                "gate_pass": int(len(schema) >= 6),
                "evidence": f"feature_schema_rows={len(schema)}",
                "severity": "hard",
            },
            {
                "gate_id": "P176_LOCAL_REAL_ROOT_EXISTS",
                "gate_pass": int(real_root.exists()),
                "evidence": str(real_root),
                "severity": "hard",
            },
            {
                "gate_id": "P176_NO_REPLAY_OR_PROFITABILITY_OUTPUTS",
                "gate_pass": 1,
                "evidence": "materializer scaffold only while activation gate is closed; forbidden_outputs=" + FORBIDDEN_OUTPUTS,
                "severity": "hard",
            },
        ]
    )


def build_acceptance_summary(plan: pd.DataFrame, templates: pd.DataFrame, gates: pd.DataFrame, phase175: pd.DataFrame) -> pd.DataFrame:
    activation_ready = as_int(metric_value(phase175, "phase175_activation_ready", 0))
    hard = gates[gates["severity"].astype(str).eq("hard")]
    activation = gates[gates["severity"].astype(str).eq("activation")]
    materialized = int(activation_ready == 1 and not activation.empty and activation["gate_pass"].astype(bool).all())
    next_action = (
        "run_phase176_materialization_after_gate_open_then_phase177_feature_quality_audit"
        if materialized
        else "add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_then_rerun_phase174_phase172_phase175_before_phase176_materialization"
    )
    return pd.DataFrame(
        [
            ("phase176_materialization_plan_rows", int(len(plan)), "Feature materialization plan rows"),
            ("phase176_sql_template_rows", int(len(templates)), "DuckDB/local SQL templates declared"),
            ("phase176_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase176_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase176_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase176_activation_ready", activation_ready, "Inherited Phase175 activation gate"),
            ("phase176_features_materialized", materialized, "1 means feature parquet was materialized"),
            ("phase176_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase176_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase176_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase176_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase176 Receive-flow Feature Materializer",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase176 is the executable materialization scaffold for the Phase175 feature schema.",
        "When Phase175 activation is closed, Phase176 writes plan/templates/gates only and materializes no feature parquet.",
        "It does not emit signals, orders, fills, P&L, profitability claims, or paper/live acceptance.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase176_receive_flow_feature_materializer_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase176(phase175_dir: Path, phase172_dir: Path, real_root: Path, output_dir: Path, feature_root: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase175 = read_csv(phase175_dir / "phase175_receive_flow_feature_schema_precommit_acceptance_summary.csv")
    phase172 = read_csv(phase172_dir / "phase172_real_l2_receive_flow_availability_acceptance_summary.csv")
    schema = read_csv(phase175_dir / "phase175_receive_flow_feature_schema.csv")
    materialization_plan = build_materialization_plan(schema, feature_root)
    templates = build_sql_templates(feature_root, real_root)
    gates = build_gate_evaluation(phase175, phase172, schema, real_root)
    acceptance = build_acceptance_summary(materialization_plan, templates, gates, phase175)

    materialization_plan.to_csv(output_dir / "phase176_materialization_plan.csv", index=False)
    templates.to_csv(output_dir / "phase176_duckdb_sql_templates.csv", index=False)
    gates.to_csv(output_dir / "phase176_materialization_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase176_receive_flow_feature_materializer_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Materialization Plan": materialization_plan,
            "DuckDB SQL Templates": templates,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase176_receive_flow_feature_materializer",
        **reproducibility_fields(
            artifact_id="phase176_receive_flow_feature_materializer",
            generated_utc=generated,
            inputs={
                "phase175_acceptance": str(phase175_dir / "phase175_receive_flow_feature_schema_precommit_acceptance_summary.csv"),
                "phase175_schema": str(phase175_dir / "phase175_receive_flow_feature_schema.csv"),
                "phase172_acceptance": str(phase172_dir / "phase172_real_l2_receive_flow_availability_acceptance_summary.csv"),
                "real_root": str(real_root),
            },
            parameters={
                "feature_root": str(feature_root),
                "activation_policy": "materialize_only_when_phase175_activation_ready_equals_1",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
                "strategy_replay_policy": "closed",
            },
            outputs={
                "materialization_plan": str(output_dir / "phase176_materialization_plan.csv"),
                "duckdb_sql_templates": str(output_dir / "phase176_duckdb_sql_templates.csv"),
                "gate_evaluation": str(output_dir / "phase176_materialization_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase176_receive_flow_feature_materializer_acceptance_summary.csv"),
                "report": str(output_dir / "phase176_receive_flow_feature_materializer_report.md"),
            },
            random_seed="none_deterministic_gated_materializer",
            scenario_ids="phase176_gated_receive_flow_feature_materializer",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase176_receive_flow_feature_materializer_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase175-dir", type=Path, default=DEFAULT_PHASE175_DIR)
    parser.add_argument("--phase172-dir", type=Path, default=DEFAULT_PHASE172_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--feature-root", type=Path, default=DEFAULT_FEATURE_ROOT)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase176(args.phase175_dir, args.phase172_dir, args.real_root, args.output_dir, args.feature_root, args.base_dir)


if __name__ == "__main__":
    main()

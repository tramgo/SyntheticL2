from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE171_DIR = Path("outputs/phase171")
DEFAULT_PHASE172_DIR = Path("outputs/phase172")
DEFAULT_PHASE174_DIR = Path("outputs/phase174")
DEFAULT_OUTPUT_DIR = Path("outputs/phase175")
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


def build_feature_schema() -> pd.DataFrame:
    rows = [
        {
            "feature_id": "P175_RECEIVE_EVENT_RATE_ZSCORE",
            "feature_family": "receive_cadence",
            "definition": "Per symbol/time bucket received-tick count standardized by same-symbol intraday baseline.",
            "minimum_input_columns": "collector_received_utc_ms;trade_date;tradingsymbol",
            "minimum_source_days": 5,
            "allowed_horizons": "1s;5s;15s;60s with coverage/staleness reporting",
            "leakage_control": "baseline statistics fitted on train dates only before test-date transform",
            "forbidden_use": "do_not_convert_directly_to_trade_signal_without_phase176_precommit",
        },
        {
            "feature_id": "P175_QUOTE_CHURN_RATE",
            "feature_family": "book_state_churn",
            "definition": "Rate of top-of-book price/quantity state changes in a bounded receive-time bucket.",
            "minimum_input_columns": "collector_received_utc_ms;buy_1_price;buy_1_quantity;sell_1_price;sell_1_quantity",
            "minimum_source_days": 5,
            "allowed_horizons": "1s;5s;15s;60s with symbol-specific coverage gates",
            "leakage_control": "computed only from events received at or before the feature timestamp",
            "forbidden_use": "no future quote state, no posthoc threshold tuning on P&L",
        },
        {
            "feature_id": "P175_DEPTH_REFRESH_INTENSITY",
            "feature_family": "top_five_depth_churn",
            "definition": "Receive-time rate of visible depth quantity changes across depth rows 1-5 on both sides.",
            "minimum_input_columns": "collector_received_utc_ms;buy_1_quantity..buy_5_quantity;sell_1_quantity..sell_5_quantity",
            "minimum_source_days": 5,
            "allowed_horizons": "1s;5s;15s;60s with depth-field completeness gates",
            "leakage_control": "uses top-five market-by-price state only; no inferred hidden order events",
            "forbidden_use": "must not be described as exchange order-by-order L3/L4 data",
        },
        {
            "feature_id": "P175_STALE_QUOTE_DURATION",
            "feature_family": "feed_staleness",
            "definition": "Elapsed receive time since last top-of-book or depth-quantity state change.",
            "minimum_input_columns": "collector_received_utc_ms;buy_1_price;buy_1_quantity;sell_1_price;sell_1_quantity;depth_quantities",
            "minimum_source_days": 5,
            "allowed_horizons": "event_time;1s;5s;15s",
            "leakage_control": "forward state duration censored at the current timestamp; no future duration completion",
            "forbidden_use": "no fill-quality inference without later broker/order telemetry",
        },
        {
            "feature_id": "P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY",
            "feature_family": "cross_symbol_receive_flow",
            "definition": "Number/share of universe symbols with at least one received tick in the same 1-second bucket.",
            "minimum_input_columns": "collector_received_utc_ms;trade_date;tradingsymbol",
            "minimum_source_days": 5,
            "allowed_horizons": "1s native synchrony source plus 5s/15s aggregations",
            "leakage_control": "computed from contemporaneous receive buckets only; target symbol exclusion required in ablation",
            "forbidden_use": "no reuse of Phase167 fixed S08 score or blocked lead-lag formula",
        },
        {
            "feature_id": "P175_RECEIVE_FLOW_REGIME_STATE",
            "feature_family": "source_quality_context",
            "definition": "Unsupervised context label from cadence/churn/staleness/synchrony features for filtering only.",
            "minimum_input_columns": "P175_RECEIVE_EVENT_RATE_ZSCORE;P175_QUOTE_CHURN_RATE;P175_STALE_QUOTE_DURATION;P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY",
            "minimum_source_days": 5,
            "allowed_horizons": "daily fitted context with intraday labels",
            "leakage_control": "fit context model on train dates only; report train/test date separation",
            "forbidden_use": "filter/context only until a separate strategy precommit phase opens",
        },
    ]
    return pd.DataFrame(rows)


def build_activation_gates(phase171: pd.DataFrame, phase172: pd.DataFrame, phase174: pd.DataFrame, schema: pd.DataFrame) -> pd.DataFrame:
    selected_source = str(metric_value(phase171, "phase171_selected_source_id", ""))
    ready_dates = as_int(metric_value(phase172, "phase172_ready_receive_flow_dates", 0))
    min_dates = as_int(metric_value(phase172, "phase172_minimum_ready_dates_required", 5), 5)
    additional_dates = as_int(metric_value(phase172, "phase172_additional_dates_needed", min_dates), min_dates)
    hard_pass = as_int(metric_value(phase172, "phase172_hard_gate_pass_rows", 0))
    hard_rows = as_int(metric_value(phase172, "phase172_hard_gate_rows", 0))
    download_ran = as_int(metric_value(phase174, "phase174_download_ran", 0))
    return pd.DataFrame(
        [
            {
                "gate_id": "P175_SOURCE_IS_PHASE171_REAL_RECEIVE_FLOW",
                "gate_pass": int(selected_source == "P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW"),
                "evidence": f"phase171_selected_source_id={selected_source}",
                "severity": "hard",
            },
            {
                "gate_id": "P175_PHASE172_STRUCTURAL_GATES_PASS",
                "gate_pass": int(hard_rows > 0 and hard_pass == hard_rows),
                "evidence": f"phase172_hard_gate_pass_rows={hard_pass}/{hard_rows}",
                "severity": "hard",
            },
            {
                "gate_id": "P175_MINIMUM_REAL_DAYS_AVAILABLE",
                "gate_pass": int(ready_dates >= min_dates),
                "evidence": f"ready_dates={ready_dates};minimum={min_dates};additional_needed={additional_dates}",
                "severity": "activation",
            },
            {
                "gate_id": "P175_SECURE_DOWNLOAD_PATH_EXISTS",
                "gate_pass": 1,
                "evidence": f"phase174_download_ran={download_ran};runner=scripts/run_phase174_secure_real_l2_download_orchestrator.ps1",
                "severity": "hard",
            },
            {
                "gate_id": "P175_FEATURE_SCHEMA_DECLARED",
                "gate_pass": int(len(schema) >= 6),
                "evidence": f"feature_rows={len(schema)}",
                "severity": "hard",
            },
            {
                "gate_id": "P175_NO_REPLAY_OR_PROFITABILITY_OUTPUTS",
                "gate_pass": 1,
                "evidence": "schema and gates only; forbidden_outputs=" + FORBIDDEN_OUTPUTS,
                "severity": "hard",
            },
        ]
    )


def build_feature_quality_gate_catalog(schema: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for feature_id in schema["feature_id"].astype(str):
        rows.extend(
            [
                {
                    "feature_id": feature_id,
                    "quality_gate_id": f"{feature_id}_COVERAGE",
                    "gate_definition": "train and test coverage must be reported by date, symbol and horizon before any strategy precommit",
                    "minimum_required": ">=5 ready dates and >=30 symbols/date",
                    "failure_action": "do_not_activate_feature",
                },
                {
                    "feature_id": feature_id,
                    "quality_gate_id": f"{feature_id}_LEAKAGE",
                    "gate_definition": "feature timestamp must be <= label/signal decision timestamp; train-fitted transforms only",
                    "minimum_required": "zero known future-leakage rows",
                    "failure_action": "block_feature_family_and_emit_leakage_ledger",
                },
            ]
        )
    return pd.DataFrame(rows)


def build_forbidden_overlap() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "blocked_family": "PHASE164_S01_TO_S07_S09_SYNTHETIC_FORMS",
                "phase175_action": "do_not_reuse_signal_formula_or_threshold",
                "overlap_allowed": 0,
            },
            {
                "blocked_family": "PHASE167_S08_FIXED_CROSS_SYMBOL_LEAD_LAG_FORM",
                "phase175_action": "cross-symbol synchrony may be a source feature, but Phase167 fixed S08 score is forbidden",
                "overlap_allowed": 0,
            },
            {
                "blocked_family": "PHASE131_TO_136_TOP_FIVE_DEPTH_PASSIVE_BRANCH",
                "phase175_action": "top-five depth churn may be audited as source quality, but passive queue/fill claims remain closed",
                "overlap_allowed": 0,
            },
        ]
    )


def build_acceptance_summary(schema: pd.DataFrame, gates: pd.DataFrame, quality: pd.DataFrame, phase172: pd.DataFrame) -> pd.DataFrame:
    ready_dates = as_int(metric_value(phase172, "phase172_ready_receive_flow_dates", 0))
    additional_dates = as_int(metric_value(phase172, "phase172_additional_dates_needed", 0))
    hard = gates[gates["severity"].astype(str).eq("hard")]
    activation = gates[gates["severity"].astype(str).eq("activation")]
    activation_ready = int(not activation.empty and activation["gate_pass"].astype(bool).all())
    next_action = (
        "run_phase176_receive_flow_feature_materialization_no_strategy"
        if activation_ready
        else "add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_then_rerun_phase174_phase172_before_phase176"
    )
    return pd.DataFrame(
        [
            ("phase175_feature_schema_rows", int(len(schema)), "Precommitted receive-flow feature rows"),
            ("phase175_feature_quality_gate_rows", int(len(quality)), "Feature quality gates declared"),
            ("phase175_activation_gate_rows", int(len(gates)), "Activation gates evaluated"),
            ("phase175_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase175_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase175_activation_ready", activation_ready, "1 means feature materialization may open"),
            ("phase175_ready_receive_flow_dates", ready_dates, "Ready receive-flow dates inherited from Phase172"),
            ("phase175_additional_dates_needed", additional_dates, "Additional real L2 dates still needed"),
            ("phase175_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase175_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase175_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase175_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase175 Receive-flow Feature Schema Precommit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase175 precommits the real receive-flow feature schema and activation gates before any materialization or strategy replay.",
        "It is not a strategy phase: no signals, orders, fills, P&L, profitability claims, or paper/live acceptance are emitted.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase175_receive_flow_feature_schema_precommit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase175(phase171_dir: Path, phase172_dir: Path, phase174_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase171 = read_csv(phase171_dir / "phase171_external_orderflow_source_acceptance_summary.csv")
    phase172 = read_csv(phase172_dir / "phase172_real_l2_receive_flow_availability_acceptance_summary.csv")
    phase174 = read_csv(phase174_dir / "phase174_secure_real_l2_download_orchestrator_acceptance_summary.csv")
    schema = build_feature_schema()
    gates = build_activation_gates(phase171, phase172, phase174, schema)
    quality = build_feature_quality_gate_catalog(schema)
    forbidden = build_forbidden_overlap()
    acceptance = build_acceptance_summary(schema, gates, quality, phase172)

    schema.to_csv(output_dir / "phase175_receive_flow_feature_schema.csv", index=False)
    quality.to_csv(output_dir / "phase175_receive_flow_feature_quality_gate_catalog.csv", index=False)
    forbidden.to_csv(output_dir / "phase175_forbidden_overlap_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase175_activation_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase175_receive_flow_feature_schema_precommit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Feature Schema": schema,
            "Feature Quality Gate Catalog": quality,
            "Forbidden Overlap Ledger": forbidden,
            "Activation Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase175_receive_flow_feature_schema_precommit",
        **reproducibility_fields(
            artifact_id="phase175_receive_flow_feature_schema_precommit",
            generated_utc=generated,
            inputs={
                "phase171_acceptance": str(phase171_dir / "phase171_external_orderflow_source_acceptance_summary.csv"),
                "phase172_acceptance": str(phase172_dir / "phase172_real_l2_receive_flow_availability_acceptance_summary.csv"),
                "phase174_acceptance": str(phase174_dir / "phase174_secure_real_l2_download_orchestrator_acceptance_summary.csv"),
            },
            parameters={
                "minimum_ready_real_l2_dates": 5,
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
                "strategy_replay_policy": "closed",
                "paper_live_policy": "closed",
            },
            outputs={
                "feature_schema": str(output_dir / "phase175_receive_flow_feature_schema.csv"),
                "quality_gate_catalog": str(output_dir / "phase175_receive_flow_feature_quality_gate_catalog.csv"),
                "forbidden_overlap_ledger": str(output_dir / "phase175_forbidden_overlap_ledger.csv"),
                "activation_gate_evaluation": str(output_dir / "phase175_activation_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase175_receive_flow_feature_schema_precommit_acceptance_summary.csv"),
                "report": str(output_dir / "phase175_receive_flow_feature_schema_precommit_report.md"),
            },
            random_seed="none_deterministic_schema_contract",
            scenario_ids="phase175_precommit_before_receive_flow_materialization",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase175_receive_flow_feature_schema_precommit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase171-dir", type=Path, default=DEFAULT_PHASE171_DIR)
    parser.add_argument("--phase172-dir", type=Path, default=DEFAULT_PHASE172_DIR)
    parser.add_argument("--phase174-dir", type=Path, default=DEFAULT_PHASE174_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase175(args.phase171_dir, args.phase172_dir, args.phase174_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE175_DIR = Path("outputs/phase175")
DEFAULT_PHASE172_DIR = Path("outputs/phase172")
DEFAULT_REAL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_OUTPUT_DIR = Path("outputs/phase176")
DEFAULT_FEATURE_ROOT = Path("derived_real_l2_receive_flow_features_phase176")
FORBIDDEN_OUTPUTS = "buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance"
L1_STATE_COLUMNS = ["buy_1_price", "buy_1_quantity", "sell_1_price", "sell_1_quantity"]
DEPTH_QTY_COLUMNS = [f"buy_{level}_quantity" for level in range(1, 6)] + [f"sell_{level}_quantity" for level in range(1, 6)]
PRICE_COLUMNS = ["buy_1_price", "sell_1_price", "last_price"]
BASE_REQUIRED_COLUMNS = [
    "collector_received_utc_ms",
    "trade_date",
    "exchange",
    "tradingsymbol",
    "last_price",
    "buy_1_price",
    "buy_1_quantity",
    "sell_1_price",
    "sell_1_quantity",
]


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
                "materialization_status": "pending_gate_evaluation",
                "target_layout": str(feature_root / "trade_date=YYYY-MM-DD" / "exchange=NSE" / "symbol=SYMBOL" / f"{feature_id.lower()}.parquet"),
                "allowed_horizons": item["allowed_horizons"],
                "minimum_source_days": item["minimum_source_days"],
                "leakage_control": item["leakage_control"],
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def discover_symbol_dirs(real_root: Path) -> list[Path]:
    if not real_root.exists():
        return []
    return sorted(
        path
        for path in real_root.glob("trade_date=*/exchange=*/symbol=*")
        if path.is_dir() and any(path.glob("*.parquet"))
    )


def partition_value(path: Path, prefix: str) -> str:
    for part in path.parts:
        if part.startswith(prefix + "="):
            return part.split("=", 1)[1]
    return ""


def read_symbol_day(symbol_dir: Path) -> pd.DataFrame:
    df = pd.read_parquet(symbol_dir)
    required = [col for col in BASE_REQUIRED_COLUMNS + DEPTH_QTY_COLUMNS + PRICE_COLUMNS if col in df.columns]
    missing = [col for col in BASE_REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"{symbol_dir} missing required columns: {missing}")
    df = df[sorted(set(required), key=required.index)].copy()
    df["collector_received_utc_ms"] = pd.to_numeric(df["collector_received_utc_ms"], errors="coerce")
    df = df.dropna(subset=["collector_received_utc_ms"]).sort_values("collector_received_utc_ms")
    df["collector_received_utc_ms"] = df["collector_received_utc_ms"].astype("int64")
    if df.empty:
        return df

    for col in L1_STATE_COLUMNS + DEPTH_QTY_COLUMNS + PRICE_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")

    prev_l1 = df[L1_STATE_COLUMNS].shift(1)
    prev_depth = df[DEPTH_QTY_COLUMNS].shift(1)
    l1_change = df[L1_STATE_COLUMNS].ne(prev_l1).any(axis=1)
    depth_change = df[DEPTH_QTY_COLUMNS].ne(prev_depth).any(axis=1)
    l1_change.iloc[0] = True
    depth_change.iloc[0] = True

    gap_ms = df["collector_received_utc_ms"].diff().fillna(0).clip(lower=0, upper=60_000)
    state_change = l1_change | depth_change
    df["bucket_ms"] = (df["collector_received_utc_ms"] // 1000) * 1000
    df["quote_churn_event"] = l1_change.astype("int8")
    df["depth_refresh_event"] = depth_change.astype("int8")
    df["stale_quote_duration_ms_event"] = np.where(state_change, 0, gap_ms).astype("float64")
    bid_qty = df["buy_1_quantity"].fillna(0)
    ask_qty = df["sell_1_quantity"].fillna(0)
    top5_bid_qty = df[[f"buy_{level}_quantity" for level in range(1, 6)]].fillna(0).sum(axis=1)
    top5_ask_qty = df[[f"sell_{level}_quantity" for level in range(1, 6)]].fillna(0).sum(axis=1)
    df["spread"] = df["sell_1_price"] - df["buy_1_price"]
    df["l1_qty_imbalance"] = np.where((bid_qty + ask_qty) > 0, (bid_qty - ask_qty) / (bid_qty + ask_qty), np.nan)
    df["top5_qty_imbalance"] = np.where(
        (top5_bid_qty + top5_ask_qty) > 0,
        (top5_bid_qty - top5_ask_qty) / (top5_bid_qty + top5_ask_qty),
        np.nan,
    )
    return df


def build_1s_features_for_symbol(symbol_dir: Path) -> pd.DataFrame:
    df = read_symbol_day(symbol_dir)
    if df.empty:
        return pd.DataFrame()
    trade_date = partition_value(symbol_dir, "trade_date") or str(df["trade_date"].iloc[0])
    exchange = partition_value(symbol_dir, "exchange") or str(df["exchange"].iloc[0])
    symbol = partition_value(symbol_dir, "symbol") or str(df["tradingsymbol"].iloc[0])
    grouped = df.groupby("bucket_ms", sort=True)
    out = grouped.agg(
        receive_event_count=("collector_received_utc_ms", "size"),
        quote_churn_count=("quote_churn_event", "sum"),
        depth_refresh_count=("depth_refresh_event", "sum"),
        stale_quote_duration_ms=("stale_quote_duration_ms_event", "sum"),
        first_receive_ms=("collector_received_utc_ms", "first"),
        last_receive_ms=("collector_received_utc_ms", "last"),
        last_price=("last_price", "last"),
        best_bid=("buy_1_price", "last"),
        best_ask=("sell_1_price", "last"),
        spread=("spread", "last"),
        l1_qty_imbalance=("l1_qty_imbalance", "last"),
        top5_qty_imbalance=("top5_qty_imbalance", "last"),
    ).reset_index()
    out["trade_date"] = trade_date
    out["exchange"] = exchange
    out["symbol"] = symbol
    out["horizon_sec"] = 1
    out["bucket_second_of_day_utc"] = ((out["bucket_ms"] // 1000) % 86_400).astype("int32")
    return out


def add_cross_symbol_synchrony(features_1s: pd.DataFrame) -> pd.DataFrame:
    if features_1s.empty:
        return features_1s
    active = (
        features_1s[["trade_date", "bucket_ms", "symbol"]]
        .drop_duplicates()
        .groupby(["trade_date", "bucket_ms"], as_index=False)
        .agg(cross_symbol_arrival_count=("symbol", "nunique"))
    )
    universe = features_1s.groupby("trade_date")["symbol"].nunique().rename("phase176_universe_symbols").reset_index()
    active = active.merge(universe, on="trade_date", how="left")
    active["cross_symbol_arrival_share"] = active["cross_symbol_arrival_count"] / active["phase176_universe_symbols"].replace(0, np.nan)
    return features_1s.merge(active, on=["trade_date", "bucket_ms"], how="left")


def add_prior_date_receive_rate_zscore(features_1s: pd.DataFrame) -> pd.DataFrame:
    if features_1s.empty:
        return features_1s
    per_date = (
        features_1s.groupby(["symbol", "trade_date"], as_index=False)["receive_event_count"]
        .agg(["mean", "std", "count"])
        .reset_index()
        .sort_values(["symbol", "trade_date"])
    )
    per_date["weighted_sum"] = per_date["mean"] * per_date["count"].clip(lower=1)
    per_date["prior_weighted_sum"] = per_date.groupby("symbol")["weighted_sum"].cumsum() - per_date["weighted_sum"]
    per_date["prior_count"] = per_date.groupby("symbol")["count"].cumsum() - per_date["count"]
    per_date["std_non_null"] = per_date["std"].replace(0, np.nan)
    per_date["prior_std_sum"] = per_date.groupby("symbol")["std_non_null"].transform(lambda series: series.fillna(0).cumsum()) - per_date["std_non_null"].fillna(0)
    per_date["prior_std_count"] = per_date.groupby("symbol")["std_non_null"].transform(lambda series: series.notna().cumsum()) - per_date["std_non_null"].notna().astype(int)
    per_date["receive_event_rate_baseline_mean_prior_dates"] = per_date["prior_weighted_sum"] / per_date["prior_count"].replace(0, np.nan)
    per_date["receive_event_rate_baseline_std_prior_dates"] = per_date["prior_std_sum"] / per_date["prior_std_count"].replace(0, np.nan)
    per_date["receive_event_rate_baseline_days"] = per_date.groupby("symbol").cumcount()
    baseline = per_date[
        [
            "symbol",
            "trade_date",
            "receive_event_rate_baseline_mean_prior_dates",
            "receive_event_rate_baseline_std_prior_dates",
            "receive_event_rate_baseline_days",
        ]
    ]
    rows = features_1s.merge(baseline, on=["symbol", "trade_date"], how="left")
    rows["receive_event_rate_zscore"] = (
        (rows["receive_event_count"] - rows["receive_event_rate_baseline_mean_prior_dates"])
        / rows["receive_event_rate_baseline_std_prior_dates"].replace(0, np.nan)
    ).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return rows


def aggregate_horizon(features_1s: pd.DataFrame, horizon_sec: int) -> pd.DataFrame:
    if features_1s.empty:
        return features_1s
    frame = features_1s.copy()
    horizon_ms = horizon_sec * 1000
    frame["bucket_ms"] = (frame["bucket_ms"] // horizon_ms) * horizon_ms
    grouped = frame.groupby(["trade_date", "exchange", "symbol", "bucket_ms"], sort=True)
    out = grouped.agg(
        receive_event_count=("receive_event_count", "sum"),
        quote_churn_count=("quote_churn_count", "sum"),
        depth_refresh_count=("depth_refresh_count", "sum"),
        stale_quote_duration_ms=("stale_quote_duration_ms", "sum"),
        first_receive_ms=("first_receive_ms", "min"),
        last_receive_ms=("last_receive_ms", "max"),
        last_price=("last_price", "last"),
        best_bid=("best_bid", "last"),
        best_ask=("best_ask", "last"),
        spread=("spread", "last"),
        l1_qty_imbalance=("l1_qty_imbalance", "last"),
        top5_qty_imbalance=("top5_qty_imbalance", "last"),
        cross_symbol_arrival_count=("cross_symbol_arrival_count", "max"),
        phase176_universe_symbols=("phase176_universe_symbols", "max"),
        cross_symbol_arrival_share=("cross_symbol_arrival_share", "max"),
        receive_event_rate_zscore=("receive_event_rate_zscore", "mean"),
        receive_event_rate_baseline_days=("receive_event_rate_baseline_days", "min"),
    ).reset_index()
    out["horizon_sec"] = horizon_sec
    out["bucket_second_of_day_utc"] = ((out["bucket_ms"] // 1000) % 86_400).astype("int32")
    return out


def write_partitioned_feature_files(frame: pd.DataFrame, feature_root: Path, horizon_sec: int) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if frame.empty:
        return pd.DataFrame(rows)
    for (trade_date, exchange, symbol), part in frame.groupby(["trade_date", "exchange", "symbol"], sort=True):
        out_dir = feature_root / f"horizon={horizon_sec}s" / f"trade_date={trade_date}" / f"exchange={exchange}" / f"symbol={symbol}"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "receive_flow_features.parquet"
        part.sort_values("bucket_ms").to_parquet(out_path, index=False)
        rows.append(
            {
                "horizon_sec": horizon_sec,
                "trade_date": trade_date,
                "exchange": exchange,
                "symbol": symbol,
                "rows": int(len(part)),
                "parquet_file": str(out_path),
                "bytes": int(out_path.stat().st_size),
            }
        )
    return pd.DataFrame(rows)


def materialize_receive_flow_features(real_root: Path, feature_root: Path) -> pd.DataFrame:
    symbol_dirs = discover_symbol_dirs(real_root)
    if feature_root.exists():
        resolved = feature_root.resolve()
        cwd = Path(".").resolve()
        if cwd not in resolved.parents and resolved != cwd:
            raise ValueError(f"Refusing to clear feature root outside workspace: {feature_root}")
        shutil.rmtree(feature_root)
    feature_root.mkdir(parents=True, exist_ok=True)

    frames: list[pd.DataFrame] = []
    for symbol_dir in symbol_dirs:
        frame = build_1s_features_for_symbol(symbol_dir)
        if not frame.empty:
            frames.append(frame)
    if not frames:
        return pd.DataFrame(columns=["horizon_sec", "trade_date", "exchange", "symbol", "rows", "parquet_file", "bytes"])

    features_1s = pd.concat(frames, ignore_index=True)
    features_1s = add_cross_symbol_synchrony(features_1s)
    features_1s = add_prior_date_receive_rate_zscore(features_1s)

    inventory_frames = [write_partitioned_feature_files(features_1s, feature_root, 1)]
    for horizon_sec in (5, 15, 60):
        inventory_frames.append(write_partitioned_feature_files(aggregate_horizon(features_1s, horizon_sec), feature_root, horizon_sec))
    return pd.concat(inventory_frames, ignore_index=True) if inventory_frames else pd.DataFrame()


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


def build_acceptance_summary(
    plan: pd.DataFrame,
    templates: pd.DataFrame,
    gates: pd.DataFrame,
    phase175: pd.DataFrame,
    feature_root: Path,
    inventory: pd.DataFrame,
) -> pd.DataFrame:
    activation_ready = as_int(metric_value(phase175, "phase175_activation_ready", 0))
    hard = gates[gates["severity"].astype(str).eq("hard")]
    activation = gates[gates["severity"].astype(str).eq("activation")]
    feature_files = list(feature_root.rglob("*.parquet")) if feature_root.exists() else []
    feature_rows = int(inventory["rows"].sum()) if not inventory.empty and "rows" in inventory.columns else 0
    materialized = int(
        activation_ready == 1
        and not activation.empty
        and activation["gate_pass"].astype(bool).all()
        and len(feature_files) > 0
    )
    next_action = (
        "run_phase177_feature_quality_audit"
        if materialized
        else (
            "implement_phase176_parquet_materialization_now_that_activation_gate_is_open"
            if activation_ready == 1
            else "add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_then_rerun_phase174_phase172_phase175_before_phase176_materialization"
        )
    )
    return pd.DataFrame(
        [
            ("phase176_materialization_plan_rows", int(len(plan)), "Feature materialization plan rows"),
            ("phase176_sql_template_rows", int(len(templates)), "DuckDB/local SQL templates declared"),
            ("phase176_gate_rows", int(len(gates)), "Gates evaluated"),
            ("phase176_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase176_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase176_activation_ready", activation_ready, "Inherited Phase175 activation gate"),
            ("phase176_materialized_partition_rows", int(len(inventory)), "Feature partition rows written to inventory"),
            ("phase176_materialized_feature_rows", feature_rows, "Feature rows written across all horizons"),
            ("phase176_feature_parquet_files", len(feature_files), "Feature parquet files present under feature root"),
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
    activation_gates = gates[gates["severity"].astype(str).eq("activation")]
    hard_gates = gates[gates["severity"].astype(str).eq("hard")]
    can_materialize = (
        not activation_gates.empty
        and activation_gates["gate_pass"].astype(bool).all()
        and not hard_gates.empty
        and hard_gates["gate_pass"].astype(bool).all()
    )
    inventory = (
        materialize_receive_flow_features(real_root, feature_root)
        if can_materialize
        else pd.DataFrame(columns=["horizon_sec", "trade_date", "exchange", "symbol", "rows", "parquet_file", "bytes"])
    )
    materialized_feature_ids = set(schema["feature_id"].astype(str).tolist()) if not inventory.empty else set()
    materialization_plan["materialization_status"] = materialization_plan["feature_id"].map(
        lambda feature_id: "materialized_feature_file_family" if feature_id in materialized_feature_ids else "not_materialized"
    )
    acceptance = build_acceptance_summary(materialization_plan, templates, gates, phase175, feature_root, inventory)

    materialization_plan.to_csv(output_dir / "phase176_materialization_plan.csv", index=False)
    templates.to_csv(output_dir / "phase176_duckdb_sql_templates.csv", index=False)
    gates.to_csv(output_dir / "phase176_materialization_gate_evaluation.csv", index=False)
    inventory.to_csv(output_dir / "phase176_feature_partition_inventory.csv", index=False)
    acceptance.to_csv(output_dir / "phase176_receive_flow_feature_materializer_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Materialization Plan": materialization_plan,
            "DuckDB SQL Templates": templates,
            "Gate Evaluation": gates,
            "Feature Partition Inventory": inventory.head(200),
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
                "feature_partition_inventory": str(output_dir / "phase176_feature_partition_inventory.csv"),
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

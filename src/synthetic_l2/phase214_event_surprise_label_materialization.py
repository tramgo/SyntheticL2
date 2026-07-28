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
DEFAULT_PHASE213_DIR = Path("outputs/phase213")
DEFAULT_OUTPUT_DIR = Path("outputs/phase214")
DEFAULT_LABEL_ROOT = Path("derived_phase214_event_surprise_conditional_labels")
JOIN_KEYS = ["bucket_ms", "trade_date", "exchange", "symbol", "horizon_sec"]
ALLOWED_SPLITS = {"train", "validation"}
SEALED_TEST_SPLITS = {"test_untouched", "test"}
FORBIDDEN_OUTPUTS = "model_fit;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export"
NEXT_ACTION = "run_phase215_event_surprise_label_quality_interpretation_no_model_no_replay_no_test"


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


def partition_key(row: dict[str, Any]) -> tuple[int, str, str, str]:
    return (as_int(row.get("horizon_sec", 0)), str(row.get("trade_date", "")), str(row.get("exchange", "")), str(row.get("symbol", "")))


def regime_bucket(series: pd.Series, low_q: float = 0.33, high_q: float = 0.67) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)
    low = numeric.quantile(low_q)
    high = numeric.quantile(high_q)
    if pd.isna(low) or pd.isna(high) or low >= high:
        return pd.Series(["mid"] * len(series), index=series.index, dtype=str)
    return pd.cut(numeric.fillna(numeric.median()), bins=[-np.inf, low, high, np.inf], labels=["low", "mid", "high"]).astype(str)


def zscore_bucket(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return pd.cut(numeric, bins=[-np.inf, -1.0, 1.0, np.inf], labels=["negative", "normal", "positive"]).astype(str)


def read_selected_columns(path: Path, columns: list[str]) -> pd.DataFrame:
    schema_cols = pd.read_parquet(path).columns.astype(str).tolist()
    return pd.read_parquet(path, columns=[col for col in columns if col in schema_cols])


def collect_train_baselines(feature_inventory: pd.DataFrame, label_inventory: pd.DataFrame) -> pd.DataFrame:
    feature_paths = {partition_key(row): Path(str(row.get("parquet_file", ""))) for row in feature_inventory.to_dict("records")}
    rows: list[pd.DataFrame] = []
    train_labels = label_inventory[label_inventory["split_role"].astype(str).eq("train")] if not label_inventory.empty else pd.DataFrame()
    for row in train_labels.to_dict("records"):
        key = partition_key(row)
        feature_path = feature_paths.get(key)
        label_path = Path(str(row.get("label_file", "")))
        if feature_path is None or not feature_path.exists() or not label_path.exists():
            continue
        features = read_selected_columns(feature_path, JOIN_KEYS + ["spread", "top5_qty_imbalance", "quote_churn_count", "receive_event_rate_zscore"])
        labels = read_selected_columns(label_path, JOIN_KEYS + ["split_role", "label_available", "future_mid_return_bps_next_bucket", "future_abs_return_bps_next_bucket", "future_spread_change_bps_next_bucket"])
        joined = features.merge(labels, on=JOIN_KEYS, how="inner")
        joined = joined[pd.to_numeric(joined.get("label_available", 0), errors="coerce").fillna(0).astype(int).eq(1)]
        joined["spread_regime"] = regime_bucket(joined.get("spread", pd.Series(dtype=float)))
        joined["liquidity_regime"] = regime_bucket(joined.get("top5_qty_imbalance", pd.Series(dtype=float)).abs())
        joined["receive_event_rate_zscore_bucket"] = zscore_bucket(joined.get("receive_event_rate_zscore", pd.Series(dtype=float)))
        rows.append(
            joined[
                [
                    "symbol",
                    "horizon_sec",
                    "spread_regime",
                    "liquidity_regime",
                    "receive_event_rate_zscore_bucket",
                    "future_mid_return_bps_next_bucket",
                    "future_abs_return_bps_next_bucket",
                    "future_spread_change_bps_next_bucket",
                ]
            ]
        )
    if not rows:
        return pd.DataFrame()
    all_train = pd.concat(rows, ignore_index=True)
    grouped = all_train.groupby(["symbol", "horizon_sec", "spread_regime", "liquidity_regime", "receive_event_rate_zscore_bucket"], dropna=False)
    baseline = grouped.agg(
        baseline_mid_return_bps=("future_mid_return_bps_next_bucket", "median"),
        baseline_abs_return_bps=("future_abs_return_bps_next_bucket", "median"),
        baseline_spread_change_bps=("future_spread_change_bps_next_bucket", "median"),
        baseline_rows=("future_mid_return_bps_next_bucket", "size"),
    ).reset_index()
    return baseline


def materialize_labels(feature_inventory: pd.DataFrame, label_inventory: pd.DataFrame, baselines: pd.DataFrame, output_root: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    feature_paths = {partition_key(row): Path(str(row.get("parquet_file", ""))) for row in feature_inventory.to_dict("records")}
    fallback = (
        baselines.groupby(["symbol", "horizon_sec"], dropna=False)
        .agg(
            fallback_mid_return_bps=("baseline_mid_return_bps", "median"),
            fallback_abs_return_bps=("baseline_abs_return_bps", "median"),
            fallback_spread_change_bps=("baseline_spread_change_bps", "median"),
            fallback_rows=("baseline_rows", "sum"),
        )
        .reset_index()
        if not baselines.empty
        else pd.DataFrame()
    )
    inventory_rows: list[dict[str, Any]] = []
    quality_rows: list[dict[str, Any]] = []
    sealed_rows: list[dict[str, Any]] = []
    output_root.mkdir(parents=True, exist_ok=True)
    for row in label_inventory.to_dict("records"):
        split_role = str(row.get("split_role", ""))
        key = partition_key(row)
        if split_role in SEALED_TEST_SPLITS:
            sealed_rows.append(
                {
                    "horizon_sec": key[0],
                    "trade_date": key[1],
                    "exchange": key[2],
                    "symbol": key[3],
                    "split_role": split_role,
                    "sealed_test_rows_available": as_int(row.get("label_available_rows", row.get("rows", 0))),
                    "sealed_test_rows_used": 0,
                    "materialized_in_phase214": 0,
                }
            )
            continue
        if split_role not in ALLOWED_SPLITS:
            continue
        feature_path = feature_paths.get(key)
        label_path = Path(str(row.get("label_file", "")))
        if feature_path is None or not feature_path.exists() or not label_path.exists():
            continue
        features = read_selected_columns(feature_path, JOIN_KEYS + ["spread", "top5_qty_imbalance", "quote_churn_count", "receive_event_rate_zscore"])
        labels = read_selected_columns(label_path, JOIN_KEYS + ["split_role", "label_available", "future_mid_return_bps_next_bucket", "future_abs_return_bps_next_bucket", "future_spread_change_bps_next_bucket"])
        joined = features.merge(labels, on=JOIN_KEYS, how="inner")
        joined = joined[pd.to_numeric(joined.get("label_available", 0), errors="coerce").fillna(0).astype(int).eq(1)].copy()
        joined["spread_regime"] = regime_bucket(joined.get("spread", pd.Series(dtype=float)))
        joined["liquidity_regime"] = regime_bucket(joined.get("top5_qty_imbalance", pd.Series(dtype=float)).abs())
        joined["receive_event_rate_zscore_bucket"] = zscore_bucket(joined.get("receive_event_rate_zscore", pd.Series(dtype=float)))
        joined = joined.merge(
            baselines,
            on=["symbol", "horizon_sec", "spread_regime", "liquidity_regime", "receive_event_rate_zscore_bucket"],
            how="left",
        )
        joined = joined.merge(fallback, on=["symbol", "horizon_sec"], how="left") if not fallback.empty else joined
        joined["fallback_baseline_used"] = pd.to_numeric(joined["baseline_rows"], errors="coerce").fillna(0).eq(0).astype(int)
        joined["baseline_mid_return_bps"] = pd.to_numeric(joined["baseline_mid_return_bps"], errors="coerce").fillna(pd.to_numeric(joined.get("fallback_mid_return_bps", 0.0), errors="coerce")).fillna(0.0)
        joined["baseline_abs_return_bps"] = pd.to_numeric(joined["baseline_abs_return_bps"], errors="coerce").fillna(pd.to_numeric(joined.get("fallback_abs_return_bps", 0.0), errors="coerce")).fillna(0.0)
        joined["baseline_spread_change_bps"] = pd.to_numeric(joined["baseline_spread_change_bps"], errors="coerce").fillna(pd.to_numeric(joined.get("fallback_spread_change_bps", 0.0), errors="coerce")).fillna(0.0)
        joined["baseline_rows"] = pd.to_numeric(joined["baseline_rows"], errors="coerce").fillna(pd.to_numeric(joined.get("fallback_rows", 0), errors="coerce")).fillna(0).astype(int)
        surprise = pd.to_numeric(joined.get("receive_event_rate_zscore", 0), errors="coerce").fillna(0.0).abs() >= 1.0
        mid = pd.to_numeric(joined["future_mid_return_bps_next_bucket"], errors="coerce").fillna(0.0)
        absret = pd.to_numeric(joined["future_abs_return_bps_next_bucket"], errors="coerce").fillna(0.0)
        spread_chg = pd.to_numeric(joined["future_spread_change_bps_next_bucket"], errors="coerce").fillna(0.0)
        joined["event_surprise_bucket"] = surprise.astype(int)
        joined["event_surprise_up_conditional_label"] = ((surprise) & (mid > joined["baseline_mid_return_bps"])).astype(int)
        joined["event_surprise_down_conditional_label"] = ((surprise) & (mid < joined["baseline_mid_return_bps"])).astype(int)
        joined["event_surprise_vol_expansion_conditional_label"] = ((surprise) & ((absret > joined["baseline_abs_return_bps"]) | (spread_chg > joined["baseline_spread_change_bps"]))).astype(int)
        out_cols = JOIN_KEYS + [
            "split_role",
            "spread_regime",
            "liquidity_regime",
            "receive_event_rate_zscore_bucket",
            "event_surprise_bucket",
            "baseline_rows",
            "fallback_baseline_used",
            "event_surprise_up_conditional_label",
            "event_surprise_down_conditional_label",
            "event_surprise_vol_expansion_conditional_label",
        ]
        rel = Path(f"horizon={key[0]}s") / f"trade_date={key[1]}" / f"exchange={key[2]}" / f"symbol={key[3]}" / "event_surprise_conditional_labels.parquet"
        out_path = output_root / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        joined[out_cols].to_parquet(out_path, index=False)
        rows = len(joined)
        available = int(joined["event_surprise_bucket"].sum())
        up_rate = float(joined["event_surprise_up_conditional_label"].mean()) if rows else 0.0
        down_rate = float(joined["event_surprise_down_conditional_label"].mean()) if rows else 0.0
        vol_rate = float(joined["event_surprise_vol_expansion_conditional_label"].mean()) if rows else 0.0
        inventory_rows.append(
            {
                "horizon_sec": key[0],
                "trade_date": key[1],
                "exchange": key[2],
                "symbol": key[3],
                "split_role": split_role,
                "rows": rows,
                "event_surprise_rows": available,
                "label_file": str(out_path),
                "bytes": out_path.stat().st_size,
                "test_rows_used": 0,
            }
        )
        quality_rows.append(
            {
                "horizon_sec": key[0],
                "trade_date": key[1],
                "exchange": key[2],
                "symbol": key[3],
                "split_role": split_role,
                "rows": rows,
                "event_surprise_rows": available,
                "up_positive_rate": up_rate,
                "down_positive_rate": down_rate,
                "vol_expansion_positive_rate": vol_rate,
                "min_baseline_rows": int(joined["baseline_rows"].min()) if rows else 0,
                "fallback_baseline_rows": int(joined["fallback_baseline_used"].sum()) if rows else 0,
                "sparse_event_surprise_partition": int(available == 0),
                "quality_pass": int(rows > 0 and joined["baseline_rows"].min() >= 1),
                "model_fit_allowed": 0,
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(inventory_rows), pd.DataFrame(quality_rows), pd.DataFrame(sealed_rows)


def build_split_balance_summary(quality: pd.DataFrame) -> pd.DataFrame:
    if quality.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for (split_role, horizon), part in quality.groupby(["split_role", "horizon_sec"], sort=True):
        rows.append(
            {
                "split_role": split_role,
                "horizon_sec": horizon,
                "partition_rows": len(part),
                "total_rows": int(part["rows"].sum()),
                "event_surprise_rows": int(part["event_surprise_rows"].sum()),
                "mean_up_positive_rate": float(part["up_positive_rate"].mean()),
                "mean_down_positive_rate": float(part["down_positive_rate"].mean()),
                "mean_vol_expansion_positive_rate": float(part["vol_expansion_positive_rate"].mean()),
                "quality_pass_rows": int(part["quality_pass"].astype(int).sum()),
                "model_fit_allowed": 0,
                "strategy_replay_allowed": 0,
            }
        )
    return pd.DataFrame(rows)


def build_forbidden_execution_ledger() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "forbidden_output": item,
                "emitted_in_phase214": 0,
                "allowed_in_phase214": 0,
                "rationale": "Phase214 materializes conditional labels only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact.",
            }
            for item in FORBIDDEN_OUTPUTS.split(";")
        ]
    )


def build_gates(phase213: pd.DataFrame, inventory: pd.DataFrame, quality: pd.DataFrame, balance: pd.DataFrame, sealed: pd.DataFrame, forbidden: pd.DataFrame) -> pd.DataFrame:
    phase213_complete = as_int(metric_value(phase213, "phase213_material_new_model_source_precommit_complete", 0))
    materialized_rows = int(inventory["rows"].sum()) if not inventory.empty else 0
    quality_pass = int(quality["quality_pass"].astype(int).sum()) if not quality.empty else 0
    event_surprise_rows = int(inventory["event_surprise_rows"].sum()) if not inventory.empty else 0
    sealed_used = int(sealed["sealed_test_rows_used"].astype(int).sum()) if not sealed.empty else 0
    forbidden_emitted = int(forbidden["emitted_in_phase214"].astype(int).sum()) if not forbidden.empty else 1
    replay_flags = 0
    for frame in [inventory, quality, balance]:
        for col in ["model_fit_allowed", "strategy_replay_allowed", "test_replay_allowed_next", "promotion_allowed"]:
            if not frame.empty and col in frame.columns:
                replay_flags += int(pd.to_numeric(frame[col], errors="coerce").fillna(0).sum())
    return pd.DataFrame(
        [
            ("P214_PHASE213_COMPLETE", phase213_complete == 1, f"phase213_complete={phase213_complete}", "hard"),
            ("P214_LABEL_PARTITIONS_MATERIALIZED", len(inventory) == 512, f"partition_rows={len(inventory)}", "hard"),
            ("P214_LABEL_ROWS_POSITIVE", materialized_rows > 0, f"materialized_rows={materialized_rows}", "hard"),
            ("P214_EVENT_SURPRISE_ROWS_POSITIVE", event_surprise_rows > 0, f"event_surprise_rows={event_surprise_rows}", "hard"),
            ("P214_QUALITY_ROWS_PASS", not quality.empty and quality_pass == len(quality), f"quality_pass_rows={quality_pass}; quality_rows={len(quality)}", "hard"),
            ("P214_SPLIT_BALANCE_RECORDED", len(balance) == 8, f"balance_rows={len(balance)}", "hard"),
            ("P214_SEALED_TEST_INVENTORY_UNUSED", not sealed.empty and sealed_used == 0, f"sealed_rows={len(sealed)}; sealed_used={sealed_used}", "hard"),
            ("P214_FORBIDDEN_OUTPUTS_CLEAN", forbidden_emitted == 0 and replay_flags == 0, f"forbidden_emitted={forbidden_emitted}; replay_flags={replay_flags}", "hard"),
        ],
        columns=["gate_id", "gate_pass", "evidence", "severity"],
    )


def build_acceptance(inventory: pd.DataFrame, quality: pd.DataFrame, balance: pd.DataFrame, sealed: pd.DataFrame, forbidden: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard = gates[gates["severity"].astype(str).eq("hard")] if not gates.empty else pd.DataFrame()
    return pd.DataFrame(
        [
            ("phase214_label_partition_rows", len(inventory), "Materialized train/validation label partition rows"),
            ("phase214_label_rows", int(inventory["rows"].sum()) if not inventory.empty else 0, "Materialized conditional label rows"),
            ("phase214_event_surprise_rows", int(inventory["event_surprise_rows"].sum()) if not inventory.empty else 0, "Rows with event-surprise bucket active"),
            ("phase214_quality_rows", len(quality), "Partition quality rows"),
            ("phase214_quality_pass_rows", int(quality["quality_pass"].astype(int).sum()) if not quality.empty else 0, "Partition quality rows passed"),
            ("phase214_split_balance_rows", len(balance), "Split/horizon balance rows"),
            ("phase214_sealed_test_inventory_rows", len(sealed), "Sealed test inventory rows recorded"),
            ("phase214_sealed_test_rows_used", int(sealed["sealed_test_rows_used"].astype(int).sum()) if not sealed.empty else 0, "Sealed test rows used"),
            ("phase214_forbidden_execution_rows", len(forbidden), "Forbidden execution rows"),
            ("phase214_gate_rows", len(gates), "Gates evaluated"),
            ("phase214_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase214_hard_gate_pass_rows", int(hard["gate_pass"].astype(bool).sum()) if not hard.empty else 0, "Hard gates passed"),
            ("phase214_event_surprise_label_materialization_complete", int(not hard.empty and hard["gate_pass"].astype(bool).all()), "1 means Phase214 completed"),
            ("phase214_model_fit_allowed_next", 0, "No model fit opened"),
            ("phase214_strategy_replay_allowed", 0, "No strategy replay opened"),
            ("phase214_test_replay_allowed_next", 0, "No test replay opened"),
            ("phase214_promotion_allowed", 0, "No promotion opened"),
            ("phase214_paper_or_live_acceptance_allowed", 0, "Paper/live remains closed"),
            ("phase214_profitability_claim_allowed", 0, "No profitability claim is allowed"),
            ("phase214_forbidden_outputs", FORBIDDEN_OUTPUTS, "Outputs forbidden in this phase"),
            ("phase214_next_best_action", NEXT_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase214 Event-surprise Conditional Label Materialization",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase214 materializes event-surprise conditional labels over train and validation partitions only.",
        "It records sealed test inventory but uses zero sealed test rows and emits no model, replay, P&L, promotion, or profitability claim.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase214_event_surprise_label_materialization_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase214(phase176_dir: Path, phase181_dir: Path, phase213_dir: Path, output_dir: Path, label_root: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase213 = read_csv(phase213_dir / "phase213_material_new_source_acceptance_summary.csv")
    feature_inventory = read_csv(phase176_dir / "phase176_feature_partition_inventory.csv")
    label_inventory = read_csv(phase181_dir / "phase181_label_partition_inventory.csv")
    baselines = collect_train_baselines(feature_inventory, label_inventory)
    inventory, quality, sealed = materialize_labels(feature_inventory, label_inventory, baselines, label_root)
    balance = build_split_balance_summary(quality)
    forbidden = build_forbidden_execution_ledger()
    gates = build_gates(phase213, inventory, quality, balance, sealed, forbidden)
    acceptance = build_acceptance(inventory, quality, balance, sealed, forbidden, gates)

    baselines.to_csv(output_dir / "phase214_train_conditional_baselines.csv", index=False)
    inventory.to_csv(output_dir / "phase214_label_partition_inventory.csv", index=False)
    quality.to_csv(output_dir / "phase214_label_partition_quality.csv", index=False)
    balance.to_csv(output_dir / "phase214_split_balance_summary.csv", index=False)
    sealed.to_csv(output_dir / "phase214_sealed_test_inventory.csv", index=False)
    forbidden.to_csv(output_dir / "phase214_execution_forbidden_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase214_event_surprise_label_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase214_event_surprise_label_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Train Conditional Baselines": baselines,
            "Label Partition Inventory": inventory,
            "Label Partition Quality": quality,
            "Split Balance Summary": balance,
            "Sealed Test Inventory": sealed,
            "Forbidden Execution Ledger": forbidden,
            "Gate Evaluation": gates,
        },
    )
    generated = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated,
        "scope": "phase214_event_surprise_label_contract_materialization_no_model_no_replay_no_test",
        **reproducibility_fields(
            artifact_id="phase214_event_surprise_label_materialization",
            generated_utc=generated,
            inputs={
                "phase176_feature_inventory": str(phase176_dir / "phase176_feature_partition_inventory.csv"),
                "phase181_label_inventory": str(phase181_dir / "phase181_label_partition_inventory.csv"),
                "phase213_acceptance": str(phase213_dir / "phase213_material_new_source_acceptance_summary.csv"),
            },
            parameters={
                "allowed_splits": "train;validation",
                "sealed_test_splits": "test_untouched;test",
                "sealed_test_rows_used": "0",
                "event_surprise_abs_zscore_threshold": "1.0",
                "model_fit_allowed": "0",
                "strategy_replay_allowed": "0",
                "forbidden_outputs": FORBIDDEN_OUTPUTS,
            },
            outputs={
                "baselines": str(output_dir / "phase214_train_conditional_baselines.csv"),
                "inventory": str(output_dir / "phase214_label_partition_inventory.csv"),
                "quality": str(output_dir / "phase214_label_partition_quality.csv"),
                "balance": str(output_dir / "phase214_split_balance_summary.csv"),
                "sealed": str(output_dir / "phase214_sealed_test_inventory.csv"),
                "forbidden": str(output_dir / "phase214_execution_forbidden_ledger.csv"),
                "gates": str(output_dir / "phase214_event_surprise_label_gate_evaluation.csv"),
                "acceptance": str(output_dir / "phase214_event_surprise_label_acceptance_summary.csv"),
                "report": str(output_dir / "phase214_event_surprise_label_materialization_report.md"),
            },
            scenario_ids="phase214_event_surprise_label_materialization_no_model_no_replay_no_test",
            cost_model_version="not_applicable_no_replay",
            latency_model_version="not_applicable_no_replay",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase214_event_surprise_label_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase214 event-surprise label materialization without model/replay/test.")
    parser.add_argument("--phase176-dir", type=Path, default=DEFAULT_PHASE176_DIR)
    parser.add_argument("--phase181-dir", type=Path, default=DEFAULT_PHASE181_DIR)
    parser.add_argument("--phase213-dir", type=Path, default=DEFAULT_PHASE213_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--label-root", type=Path, default=DEFAULT_LABEL_ROOT)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    run_phase214(args.phase176_dir, args.phase181_dir, args.phase213_dir, args.output_dir, args.label_root, args.base_dir)


if __name__ == "__main__":
    main()

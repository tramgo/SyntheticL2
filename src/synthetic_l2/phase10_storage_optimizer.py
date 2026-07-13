from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.reproducibility import reproducibility_fields


PRODUCTS = [
    ("stage_a1_compact_real_ticks", "outputs/stage_a1/compact_ticks_by_symbol/symbol=*/ticks.parquet", "real_received_ticks"),
    ("phase5_price_paths_5m", "outputs/phase5/price_paths_5m.parquet", "synthetic_price_bars"),
    ("phase6_l2_book_states_5m", "outputs/phase6/l2_book_states_5m.parquet", "synthetic_l2_book"),
    ("phase8_retail_feed_observations", "outputs/phase8/retail_feed_observations.parquet", "synthetic_retail_feed"),
    ("phase9_tier_a_raw_synthetic_events", "outputs/phase9/tier_a/raw_synthetic_events.parquet", "synthetic_event_product"),
    ("phase9_tier_b_compact_l2_state", "outputs/phase9/tier_b/compact_l2_state.parquet", "synthetic_l2_product"),
    ("phase9_tier_c_features_5m", "outputs/phase9/tier_c/features_5m.parquet", "synthetic_feature_product"),
    ("phase9_tier_d_resampled_features_15m", "outputs/phase9/tier_d/resampled_features_15m.parquet", "synthetic_resampled_feature_product"),
]


PROFILE_SPECS = [
    {
        "profile": "Small",
        "purpose": "unit/integration tests",
        "tickers": 5,
        "trading_days": 10,
        "feed_profiles": 1,
        "event_multiplier": 1.0,
        "include_raw_replay": True,
        "include_features": True,
    },
    {
        "profile": "Medium",
        "purpose": "initial strategy screening",
        "tickers": 32,
        "trading_days": 63,
        "feed_profiles": 5,
        "event_multiplier": 1.0,
        "include_raw_replay": True,
        "include_features": True,
    },
    {
        "profile": "Full",
        "purpose": "annual stress study",
        "tickers": 32,
        "trading_days": 252,
        "feed_profiles": 5,
        "event_multiplier": 1.0,
        "include_raw_replay": True,
        "include_features": True,
    },
    {
        "profile": "Dense",
        "purpose": "microstructure stress",
        "tickers": 10,
        "trading_days": 63,
        "feed_profiles": 5,
        "event_multiplier": 4.0,
        "include_raw_replay": True,
        "include_features": True,
    },
    {
        "profile": "Feature-only",
        "purpose": "rapid ML experiments",
        "tickers": 32,
        "trading_days": 63,
        "feed_profiles": 5,
        "event_multiplier": 1.0,
        "include_raw_replay": False,
        "include_features": True,
    },
]


def parquet_files(pattern: str) -> list[Path]:
    root = Path(".")
    if "*" not in pattern:
        path = Path(pattern)
        return [path] if path.exists() else []
    return sorted(root.glob(pattern))


def parquet_rows(path: Path) -> int:
    meta = pq.ParquetFile(path).metadata
    return int(meta.num_rows)


def collect_inventory() -> pd.DataFrame:
    rows: list[dict] = []
    for dataset, pattern, layer in PRODUCTS:
        files = parquet_files(pattern)
        total_bytes = sum(path.stat().st_size for path in files)
        total_rows = sum(parquet_rows(path) for path in files)
        rows.append(
            {
                "dataset": dataset,
                "layer": layer,
                "path_pattern": pattern,
                "file_count": len(files),
                "total_rows": total_rows,
                "total_bytes": total_bytes,
                "bytes_per_row": total_bytes / total_rows if total_rows else None,
                "mb": total_bytes / (1024 * 1024),
                "target_file_size_mb": "128-512",
                "tiny_file_warning": bool(files and total_bytes / len(files) < 8 * 1024 * 1024 and len(files) > 16),
            }
        )
    return pd.DataFrame(rows)


def collect_schema_audit() -> pd.DataFrame:
    rows: list[dict] = []
    for dataset, pattern, layer in PRODUCTS:
        files = parquet_files(pattern)
        if not files:
            continue
        schema = pq.ParquetFile(files[0]).schema_arrow
        for field in schema:
            rows.append(
                {
                    "dataset": dataset,
                    "layer": layer,
                    "column": field.name,
                    "arrow_type": str(field.type),
                    "nullable": field.nullable,
                    "recommended_type_note": recommended_type_note(field.name, str(field.type)),
                }
            )
    return pd.DataFrame(rows)


def recommended_type_note(column: str, arrow_type: str) -> str:
    name = column.lower()
    if name.endswith("_utc_ms") or name in {"event_id", "receive_sequence", "source_sequence", "bar_index", "scenario_day"}:
        return "integer sequence/timestamp type is appropriate"
    if "price" in name or name.endswith("_px_1") or "_px_" in name or "spread" in name or "return" in name:
        if "double" in arrow_type or "float" in arrow_type:
            return "candidate for fixed-point integer ticks where exact tick-grid replay is required"
    if "qty" in name or "orders" in name or "volume" in name:
        return "integer quantity/order type preferred"
    if name.startswith("is_"):
        return "boolean flag is appropriate"
    if name in {"symbol", "feed_profile", "quarter_profile", "regime_code", "book_event_label", "event_kind"}:
        return "dictionary encoding recommended"
    return ""


def build_size_estimates(inventory: pd.DataFrame, data_quality_path: Path) -> pd.DataFrame:
    quality = pd.read_csv(data_quality_path)
    real_rows_per_symbol_day = float(quality["row_count"].mean())
    raw_input_bytes_per_real_event = float(quality["file_bytes"].sum() / quality["row_count"].sum())

    inv = inventory.set_index("dataset")
    compact_real_bpr = float(inv.loc["stage_a1_compact_real_ticks", "bytes_per_row"])
    tier_b_bpr = float(inv.loc["phase9_tier_b_compact_l2_state", "bytes_per_row"])
    tier_c_bpr = float(inv.loc["phase9_tier_c_features_5m", "bytes_per_row"])
    tier_d_bpr = float(inv.loc["phase9_tier_d_resampled_features_15m", "bytes_per_row"])
    tier_a_bpr = float(inv.loc["phase9_tier_a_raw_synthetic_events", "bytes_per_row"])
    tier_c_rows = float(inv.loc["phase9_tier_c_features_5m", "total_rows"])
    tier_d_rows = float(inv.loc["phase9_tier_d_resampled_features_15m", "total_rows"])
    tier_d_rows_per_source_row = tier_d_rows / tier_c_rows if tier_c_rows else 0.0

    rows: list[dict] = []
    for spec in PROFILE_SPECS:
        symbol_days = spec["tickers"] * spec["trading_days"]
        profile_symbol_days = symbol_days * spec["feed_profiles"]
        estimated_real_event_rows = real_rows_per_symbol_day * symbol_days * spec["event_multiplier"]
        estimated_feed_rows = estimated_real_event_rows * spec["feed_profiles"]
        raw_replay_bytes = estimated_feed_rows * tier_a_bpr if spec["include_raw_replay"] else 0.0
        compact_l2_bytes = estimated_feed_rows * max(compact_real_bpr, tier_b_bpr)
        feature_bytes = estimated_feed_rows * tier_c_bpr if spec["include_features"] else 0.0
        resampled_feature_bytes = estimated_feed_rows * tier_d_rows_per_source_row * tier_d_bpr if spec["include_features"] else 0.0
        total_bytes = raw_replay_bytes + compact_l2_bytes + feature_bytes + resampled_feature_bytes
        rows.append(
            {
                "profile": spec["profile"],
                "purpose": spec["purpose"],
                "tickers": spec["tickers"],
                "trading_days": spec["trading_days"],
                "feed_profiles": spec["feed_profiles"],
                "event_multiplier": spec["event_multiplier"],
                "symbol_days": symbol_days,
                "profile_symbol_days": profile_symbol_days,
                "mean_real_events_per_symbol_day": real_rows_per_symbol_day,
                "raw_input_bytes_per_real_event": raw_input_bytes_per_real_event,
                "compact_real_bytes_per_event": compact_real_bpr,
                "estimated_feed_rows": estimated_feed_rows,
                "raw_replay_gb": raw_replay_bytes / (1024**3),
                "compact_l2_gb": compact_l2_bytes / (1024**3),
                "feature_gb": feature_bytes / (1024**3),
                "resampled_feature_gb": resampled_feature_bytes / (1024**3),
                "total_gb": total_bytes / (1024**3),
                "conservative_total_gb": total_bytes * 0.70 / (1024**3),
                "aggressive_total_gb": total_bytes * 2.50 / (1024**3),
            }
        )
    return pd.DataFrame(rows)


def build_partition_recommendations(inventory: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for record in inventory.to_dict("records"):
        dataset = record["dataset"]
        if "tier_a" in dataset:
            partition = "layer=raw_events/trade_date=YYYY-MM-DD/symbol=ABC/part-*.parquet"
        elif "tier_b" in dataset or "l2" in dataset or "feed" in dataset:
            partition = "layer=l2_state/trade_date=YYYY-MM-DD/symbol=ABC/part-*.parquet"
        elif "tier_d" in dataset or "resampled" in dataset:
            partition = "layer=features_15m/trading_month=YYYY-MM/symbol=ABC/part-*.parquet"
        elif "tier_c" in dataset or "feature" in dataset:
            partition = "layer=features_5m/trading_month=YYYY-MM/symbol=ABC/part-*.parquet"
        else:
            partition = "layer=audit_or_calibration/trade_date=YYYY-MM-DD/symbol=ABC/part-*.parquet"
        rows.append(
            {
                "dataset": dataset,
                "recommended_partitioning": partition,
                "current_file_count": record["file_count"],
                "current_mb": record["mb"],
                "tiny_file_warning": record["tiny_file_warning"],
                "action": "keep current single-file product until it exceeds practical rewrite threshold"
                if record["file_count"] == 1
                else "consider compaction into 128-512 MB files before large multi-day expansion",
            }
        )
    return pd.DataFrame(rows)


def _markdown_table(frame: pd.DataFrame, float_format: str = ".4f") -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        def fmt(value):
            if pd.isna(value):
                return ""
            if isinstance(value, float):
                return format(value, float_format)
            return str(value)

        text[column] = text[column].map(fmt)
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def write_report(output_dir: Path, inventory: pd.DataFrame, estimates: pd.DataFrame, partitions: pd.DataFrame, schema: pd.DataFrame) -> None:
    compact_cols = ["dataset", "file_count", "total_rows", "mb", "bytes_per_row", "tiny_file_warning"]
    estimate_cols = ["profile", "tickers", "trading_days", "feed_profiles", "event_multiplier", "estimated_feed_rows", "total_gb", "conservative_total_gb", "aggressive_total_gb"]
    schema_issues = schema[schema["recommended_type_note"].str.contains("candidate|dictionary", case=False, na=False)].head(25)
    lines = [
        "# Phase 10 Storage and Size Optimization Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase measures current Parquet product sizes, audits physical column types, and estimates storage for the plan profiles.",
        "Parquet/Zstandard remains the durable format. DuckDB remains the analytic query layer. SQLite is not used for high-volume tick/L2 storage.",
        "",
        "## Current Product Inventory",
        "",
        _markdown_table(inventory[compact_cols]),
        "",
        "## Size Estimates",
        "",
        _markdown_table(estimates[estimate_cols]),
        "",
        "## Partition Recommendations",
        "",
        _markdown_table(partitions[["dataset", "recommended_partitioning", "action"]].head(20)),
        "",
        "## Type Optimization Candidates",
        "",
        _markdown_table(schema_issues[["dataset", "column", "arrow_type", "recommended_type_note"]]),
        "",
        "## Caveats",
        "",
        "- Estimates use the current one-day real received-tick row rate and current synthetic product bytes-per-row.",
        "- The current Phase 6-9 synthetic stream is 5-minute state based; event-driven expansion will change row counts and should rerun this phase.",
        "- Conservative/aggressive totals are storage-planning bands, not statistical confidence intervals.",
        "",
    ]
    (output_dir / "phase10_storage_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase10(output_dir: Path, data_quality_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory = collect_inventory()
    schema = collect_schema_audit()
    estimates = build_size_estimates(inventory, data_quality_path)
    partitions = build_partition_recommendations(inventory)

    inventory.to_csv(output_dir / "storage_inventory.csv", index=False)
    schema.to_csv(output_dir / "schema_physical_types.csv", index=False)
    estimates.to_csv(output_dir / "size_estimates.csv", index=False)
    partitions.to_csv(output_dir / "partition_recommendations.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "data_quality_path": str(data_quality_path),
        "outputs": [
            "storage_inventory.csv",
            "schema_physical_types.csv",
            "size_estimates.csv",
            "partition_recommendations.csv",
            "phase10_storage_report.md",
        ],
        "storage_decision": "Parquet/Zstandard durable storage with DuckDB query layer; SQLite only for small metadata if needed later.",
        "evidence_scope": "current Stage A1 and Phase 5-9 artifacts",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase10",
            generated_utc=generated_utc,
            inputs={"data_quality_path": str(data_quality_path), "products": PRODUCTS},
            parameters={"storage_decision": manifest["storage_decision"], "evidence_scope": manifest["evidence_scope"]},
            outputs={
                "storage_inventory": str(output_dir / "storage_inventory.csv"),
                "schema_physical_types": str(output_dir / "schema_physical_types.csv"),
                "size_estimates": str(output_dir / "size_estimates.csv"),
                "partition_recommendations": str(output_dir / "partition_recommendations.csv"),
                "report": str(output_dir / "phase10_storage_report.md"),
                "manifest": str(output_dir / "storage_manifest.json"),
            },
            random_seed="not_applicable_deterministic_storage_inventory",
            scenario_ids="current_workspace_stage_a1_phase5_phase6_phase8_phase9_products",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="phase8_feed_profiles_v1_or_not_applicable",
        )
    )
    (output_dir / "storage_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, inventory, estimates, partitions, schema)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 10 storage inventory, schema audit and size estimates.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase10"))
    parser.add_argument("--data-quality-path", type=Path, default=Path("outputs/stage_a1/data_quality_report.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase10(args.output_dir, args.data_quality_path)


if __name__ == "__main__":
    main()

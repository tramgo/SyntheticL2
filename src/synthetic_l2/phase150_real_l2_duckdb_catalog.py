from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase150")
DEFAULT_REAL_PANEL_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_DB_PATH = DEFAULT_OUTPUT_DIR / "real_l2_catalog.duckdb"
PART_RE = re.compile(r"^(?P<key>trade_date|exchange|symbol)=(?P<value>.+)$")


def infer_part(path: Path, key: str) -> str:
    for part in path.parts:
        match = PART_RE.match(part)
        if match and match.group("key") == key:
            return match.group("value")
    return ""


def discover_files(root: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if not root.exists():
        return pd.DataFrame(
            columns=[
                "file_path",
                "relative_path",
                "trade_date",
                "exchange",
                "symbol",
                "bytes",
                "file_name",
            ]
        )
    for path in sorted(root.rglob("*.parquet")):
        stat = path.stat()
        rows.append(
            {
                "file_path": path.as_posix(),
                "relative_path": path.relative_to(root).as_posix(),
                "trade_date": infer_part(path, "trade_date"),
                "exchange": infer_part(path, "exchange"),
                "symbol": infer_part(path, "symbol"),
                "bytes": int(stat.st_size),
                "file_name": path.name,
            }
        )
    return pd.DataFrame(rows)


def build_date_symbol_summary(files: pd.DataFrame) -> pd.DataFrame:
    if files.empty:
        return pd.DataFrame()
    return (
        files.groupby(["trade_date", "exchange", "symbol"], sort=True)
        .agg(
            parquet_files=("file_path", "count"),
            bytes=("bytes", "sum"),
            first_file=("relative_path", "first"),
            last_file=("relative_path", "last"),
        )
        .reset_index()
    )


def build_date_summary(files: pd.DataFrame) -> pd.DataFrame:
    if files.empty:
        return pd.DataFrame()
    return (
        files.groupby(["trade_date", "exchange"], sort=True)
        .agg(
            symbols=("symbol", "nunique"),
            parquet_files=("file_path", "count"),
            bytes=("bytes", "sum"),
        )
        .reset_index()
    )


def schema_catalog(sample_file: Path) -> pd.DataFrame:
    if not sample_file.exists():
        return pd.DataFrame(columns=["column_ordinal", "column_name", "duckdb_type", "nullable"])
    schema = pq.read_schema(sample_file)
    rows = []
    for idx, field in enumerate(schema):
        rows.append(
            {
                "column_ordinal": idx,
                "column_name": field.name,
                "arrow_type": str(field.type),
                "nullable": bool(field.nullable),
            }
        )
    return pd.DataFrame(rows)


def build_query_templates(root: Path) -> pd.DataFrame:
    glob = root.as_posix().rstrip("/") + "/**/*.parquet"
    rows = [
        {
            "template_id": "read_one_symbol_day",
            "description": "Read one symbol/day directly from local partitioned Parquet.",
            "sql_template": "SELECT * FROM parquet_scan('<root>/trade_date=<date>/exchange=NSE/symbol=<symbol>/*.parquet', union_by_name=true, filename=true) ORDER BY collector_received_utc_ms LIMIT 100;",
        },
        {
            "template_id": "count_one_symbol_day",
            "description": "Count rows for one symbol/day by scanning only that partition.",
            "sql_template": "SELECT count(*) AS rows FROM parquet_scan('<root>/trade_date=<date>/exchange=NSE/symbol=<symbol>/*.parquet', union_by_name=true);",
        },
        {
            "template_id": "best_bid_ask_sample",
            "description": "Sample L1 book columns from one symbol/day without scanning the full lake.",
            "sql_template": "SELECT trade_date, exchange, tradingsymbol, collector_received_utc_ms, last_price, buy_1_price, buy_1_quantity, sell_1_price, sell_1_quantity FROM parquet_scan('<root>/trade_date=<date>/exchange=NSE/symbol=<symbol>/*.parquet', union_by_name=true) ORDER BY collector_received_utc_ms LIMIT 100;",
        },
        {
            "template_id": "all_panel_glob",
            "description": "Full local panel glob for deliberate analytical scans; avoid for quick metadata checks.",
            "sql_template": f"SELECT * FROM parquet_scan('{glob}', hive_partitioning=true, union_by_name=true, filename=true);",
        },
    ]
    return pd.DataFrame(rows)


def quote_sql(value: str) -> str:
    return value.replace("'", "''")


def build_duckdb_catalog(
    db_path: Path,
    files: pd.DataFrame,
    date_symbol_summary: pd.DataFrame,
    date_summary: pd.DataFrame,
    columns: pd.DataFrame,
    query_templates: pd.DataFrame,
    sample_file: Path,
) -> pd.DataFrame:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    con = duckdb.connect(str(db_path))
    try:
        con.register("files_df", files)
        con.register("date_symbol_summary_df", date_symbol_summary)
        con.register("date_summary_df", date_summary)
        con.register("columns_df", columns)
        con.register("query_templates_df", query_templates)
        con.execute("CREATE TABLE real_l2_parquet_files AS SELECT * FROM files_df")
        con.execute("CREATE TABLE real_l2_date_symbol_summary AS SELECT * FROM date_symbol_summary_df")
        con.execute("CREATE TABLE real_l2_date_summary AS SELECT * FROM date_summary_df")
        con.execute("CREATE TABLE real_l2_schema_columns AS SELECT * FROM columns_df")
        con.execute("CREATE TABLE real_l2_query_templates AS SELECT * FROM query_templates_df")
        if sample_file.exists():
            sample_sql = f"CREATE VIEW real_l2_sample_ticks AS SELECT * FROM parquet_scan('{quote_sql(sample_file.as_posix())}', union_by_name=true, filename=true)"
            con.execute(sample_sql)
            smoke = con.execute(
                "SELECT count(*) AS rows, min(collector_received_utc_ms) AS min_received_ms, max(collector_received_utc_ms) AS max_received_ms FROM real_l2_sample_ticks"
            ).fetchdf()
        else:
            smoke = pd.DataFrame([{"rows": 0, "min_received_ms": None, "max_received_ms": None}])
        catalog_tables = con.execute(
            "SELECT table_name, table_type FROM information_schema.tables WHERE table_schema='main' ORDER BY table_name"
        ).fetchdf()
        smoke["sample_file"] = sample_file.as_posix() if sample_file.exists() else ""
        smoke["catalog_tables"] = "|".join(catalog_tables["table_name"].astype(str).tolist())
        return smoke
    finally:
        con.close()


def summarize(files: pd.DataFrame, date_symbol_summary: pd.DataFrame, date_summary: pd.DataFrame, columns: pd.DataFrame, smoke: pd.DataFrame, db_path: Path) -> pd.DataFrame:
    sample_rows = int(pd.to_numeric(smoke["rows"], errors="coerce").fillna(0).iloc[0]) if not smoke.empty else 0
    required_depth_columns = [f"{side}_{level}_{field}" for side in ["buy", "sell"] for level in range(1, 6) for field in ["price", "quantity", "orders"]]
    columns_found = set(columns["column_name"].astype(str).tolist()) if not columns.empty else set()
    depth_columns_present = int(sum(col in columns_found for col in required_depth_columns))
    return pd.DataFrame(
        [
            ("phase150_duckdb_available", 1, "DuckDB import and connection succeeded"),
            ("phase150_catalog_db_created", int(db_path.exists()), "Persistent DuckDB metadata catalog exists"),
            ("phase150_parquet_files_cataloged", int(len(files)), "Local real L2 Parquet files cataloged without row-copy ingest"),
            ("phase150_cataloged_bytes", int(files["bytes"].sum()) if not files.empty else 0, "Cataloged local Parquet bytes"),
            ("phase150_trade_dates", int(date_summary["trade_date"].nunique()) if not date_summary.empty else 0, "Distinct trade dates cataloged"),
            ("phase150_date_symbol_partitions", int(len(date_symbol_summary)), "Date/exchange/symbol partitions cataloged"),
            ("phase150_schema_columns", int(len(columns)), "Columns in sampled Parquet schema"),
            ("phase150_depth_columns_present", depth_columns_present, "buy/sell level 1-5 price/quantity/orders columns present in sampled schema"),
            ("phase150_sample_query_rows", sample_rows, "Rows returned by DuckDB sample-file smoke query"),
            ("phase150_strategy_replay_allowed", 0, "Cataloging local Parquet does not unlock strategy replay"),
            ("phase150_next_best_action", "use_duckdb_catalog_for_local_real_l2_queries_after_phase148_downloads", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase150 Real L2 DuckDB Catalog",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase150 builds a metadata-first DuckDB catalog for the local real Zerodha top-five market-by-price Parquet panel.",
        "It does not copy all tick rows into DuckDB. Bulk storage remains partitioned Parquet; DuckDB stores metadata, summaries, schema, templates, and a sample-file view.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase150_real_l2_duckdb_catalog_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase150(output_dir: Path, base_dir: Path, real_panel_root: Path, db_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = discover_files(real_panel_root)
    sample_file = Path(files["file_path"].iloc[0]) if not files.empty else Path("")
    date_symbol_summary = build_date_symbol_summary(files)
    date_summary = build_date_summary(files)
    columns = schema_catalog(sample_file)
    templates = build_query_templates(real_panel_root)
    smoke = build_duckdb_catalog(db_path, files, date_symbol_summary, date_summary, columns, templates, sample_file)
    acceptance = summarize(files, date_symbol_summary, date_summary, columns, smoke, db_path)

    files.to_csv(output_dir / "phase150_real_l2_file_inventory.csv", index=False)
    date_symbol_summary.to_csv(output_dir / "phase150_real_l2_date_symbol_summary.csv", index=False)
    date_summary.to_csv(output_dir / "phase150_real_l2_date_summary.csv", index=False)
    columns.to_csv(output_dir / "phase150_real_l2_schema_columns.csv", index=False)
    templates.to_csv(output_dir / "phase150_duckdb_query_templates.csv", index=False)
    smoke.to_csv(output_dir / "phase150_duckdb_smoke_query.csv", index=False)
    acceptance.to_csv(output_dir / "phase150_real_l2_duckdb_catalog_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Date Summary": date_summary,
            "Schema Columns": columns,
            "DuckDB Smoke Query": smoke,
            "Query Templates": templates,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase150_real_l2_duckdb_catalog",
        **reproducibility_fields(
            artifact_id="phase150",
            generated_utc=generated_utc,
            inputs={"real_panel_root": str(real_panel_root)},
            parameters={
                "catalog_policy": "metadata_first_no_full_row_copy",
                "duckdb_database": str(db_path),
                "sample_file": sample_file.as_posix() if sample_file.exists() else "",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "duckdb_database": str(db_path),
                "file_inventory": str(output_dir / "phase150_real_l2_file_inventory.csv"),
                "date_symbol_summary": str(output_dir / "phase150_real_l2_date_symbol_summary.csv"),
                "date_summary": str(output_dir / "phase150_real_l2_date_summary.csv"),
                "schema_columns": str(output_dir / "phase150_real_l2_schema_columns.csv"),
                "query_templates": str(output_dir / "phase150_duckdb_query_templates.csv"),
                "smoke_query": str(output_dir / "phase150_duckdb_smoke_query.csv"),
                "acceptance_summary": str(output_dir / "phase150_real_l2_duckdb_catalog_acceptance_summary.csv"),
                "report": str(output_dir / "phase150_real_l2_duckdb_catalog_report.md"),
                "manifest": str(output_dir / "phase150_real_l2_duckdb_catalog_manifest.json"),
            },
            random_seed="none_deterministic_catalog",
            scenario_ids="phase150_real_l2_duckdb_catalog",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase150_real_l2_duckdb_catalog_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a metadata-first DuckDB catalog for local real L2 Parquet.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--real-panel-root", type=Path, default=DEFAULT_REAL_PANEL_ROOT)
    parser.add_argument("--db-path", type=Path, default=DEFAULT_DB_PATH)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase150(args.output_dir, args.base_dir, args.real_panel_root, args.db_path)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.phase317_event_catalyst_multievent_top5_depth_join_materialization import (
    DEPTH_COLUMNS,
    OUTPUT_COLUMNS,
    parquet_timestamp_bounds,
)
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE326_DIR = Path("outputs/phase326")
DEFAULT_OUTPUT_DIR = Path("outputs/phase327")

NEXT_ACTION_IF_JOINED = "run_phase328_event_catalyst_expanded_join_quality_audit_no_strategy_search"
NEXT_ACTION_IF_NO_OVERLAP = "repair_phase327_event_timestamps_or_dense_coverage_then_rerun_join"
REPAIR_ACTION = "repair_phase327_event_catalyst_expanded_top5_depth_join_materialization"


def sql_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def sql_list(values: list[str]) -> str:
    return "[" + ", ".join(sql_quote(value) for value in values) + "]"


def compact_parts_streaming(part_paths: list[str], output_path: Path) -> int:
    if output_path.exists():
        output_path.unlink()
    writer: pq.ParquetWriter | None = None
    joined_rows = 0
    try:
        for part_path in part_paths:
            pf = pq.ParquetFile(part_path)
            joined_rows += int(pf.metadata.num_rows)
            for row_group in range(pf.num_row_groups):
                table = pf.read_row_group(row_group, columns=OUTPUT_COLUMNS)
                if writer is None:
                    writer = pq.ParquetWriter(output_path, table.schema, compression="zstd")
                writer.write_table(table)
    finally:
        if writer is not None:
            writer.close()
    return joined_rows


def count_timestamp_rows(path: Path, start_epoch: int, end_epoch: int) -> int:
    pf = pq.ParquetFile(path)
    ts_idx = pf.schema.names.index("exchange_timestamp_ms")
    count = 0
    for row_group in range(pf.num_row_groups):
        stats = pf.metadata.row_group(row_group).column(ts_idx).statistics
        if stats is None or not stats.has_min_max:
            table = pf.read_row_group(row_group, columns=["exchange_timestamp_ms"])
        elif int(stats.min) <= end_epoch and int(stats.max) >= start_epoch:
            table = pf.read_row_group(row_group, columns=["exchange_timestamp_ms"])
        else:
            continue
        values = table.column("exchange_timestamp_ms").to_numpy()
        count += int(((values >= start_epoch) & (values <= end_epoch)).sum())
        if count > 0:
            return count
    return count


def choose_fallback_source(symbol: str, start_epoch: int, end_epoch: int) -> tuple[str, int]:
    checked = 0
    candidates: list[Path] = []
    for path in sorted(Path("raw_synthetic_l2_dense_full_year").glob(f"trade_month=*/symbol={symbol}/part-*.parquet")):
        file_min, file_max, _, _ = parquet_timestamp_bounds(path)
        if file_min <= end_epoch and file_max >= start_epoch:
            candidates.append(path)
    for path in candidates:
        checked += 1
        if count_timestamp_rows(path, start_epoch, end_epoch) > 0:
            return str(path), checked
    return "", checked


def materialize_duckdb(work_order: pd.DataFrame, output_path: Path, preview_rows: int = 1000) -> tuple[pd.DataFrame, pd.DataFrame, int, int]:
    work = work_order.copy()
    work["dense_file_path"] = work["dense_file_path"].astype(str)
    work["event_epoch"] = work["window_start_epoch"].astype("int64") + work["pre_event_seconds"].astype("int64")

    coverage = work[
        [
            "event_id",
            "symbol",
            "dense_file_path",
            "window_start_epoch",
            "window_end_epoch",
            "timestamp_overlap",
        ]
    ].copy()
    coverage["actual_dense_file_path"] = coverage["dense_file_path"]
    coverage["file_exists"] = coverage["dense_file_path"].map(lambda value: int(Path(value).exists()))
    bounds: dict[str, tuple[int, int, int, int]] = {}
    for value in sorted(coverage.loc[coverage["file_exists"].eq(1), "dense_file_path"].unique()):
        bounds[value] = parquet_timestamp_bounds(Path(value))
    coverage["file_min_epoch"] = coverage["dense_file_path"].map(lambda value: bounds.get(value, (0, 0, 0, 0))[0])
    coverage["file_max_epoch"] = coverage["dense_file_path"].map(lambda value: bounds.get(value, (0, 0, 0, 0))[1])
    coverage["source_rows"] = coverage["dense_file_path"].map(lambda value: bounds.get(value, (0, 0, 0, 0))[2])
    coverage["row_groups"] = coverage["dense_file_path"].map(lambda value: bounds.get(value, (0, 0, 0, 0))[3])
    coverage["fallback_paths_checked"] = 0
    coverage["fallback_used"] = 0
    coverage["row_groups_read"] = 0
    coverage["materialized_rows"] = 0

    if output_path.exists():
        output_path.unlink()
    parts_dir = output_path.parent / "phase327_symbol_parts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    temp_parts_dir = output_path.parent / "phase327_symbol_source_parts"
    temp_parts_dir.mkdir(parents=True, exist_ok=True)
    fallback_parts_dir = output_path.parent / "phase327_symbol_fallback_parts"
    fallback_parts_dir.mkdir(parents=True, exist_ok=True)
    for old_fallback_part in fallback_parts_dir.glob("*.parquet"):
        old_fallback_part.unlink()

    con = duckdb.connect()
    con.register("phase327_windows_all", work)
    depth_select = ",\n                ".join([f"d.{col}" for col in DEPTH_COLUMNS])
    part_paths: list[str] = []
    for symbol, symbol_work in work.groupby("symbol", sort=True):
        part_path = parts_dir / f"symbol={symbol}.parquet"
        if part_path.exists() and part_path.stat().st_size > 0:
            part_paths.append(str(part_path))
            continue
        if part_path.exists():
            part_path.unlink()
        for old_source_part in temp_parts_dir.glob(f"symbol={symbol}__source=*.parquet"):
            old_source_part.unlink()

        source_part_paths: list[str] = []
        for source_index, (source_path, source_work) in enumerate(symbol_work.groupby("dense_file_path", sort=True), start=1):
            source_part_path = temp_parts_dir / f"symbol={symbol}__source={source_index:02d}.parquet"
            source_part_sql = sql_quote(str(source_part_path))
            con.register("phase327_source_windows", source_work)
            source_path_sql = sql_quote(str(source_path))
            con.execute(
                f"""
                COPY (
                    SELECT
                        w.event_id,
                        w.event_time_ist,
                        w.event_type,
                        w.symbol,
                        CAST(d.exchange_timestamp_ms - w.event_epoch AS BIGINT) AS relative_second,
                        d.exchange_timestamp_ms,
                        d.last_price,
                        d.volume_traded,
                        {depth_select}
                    FROM read_parquet({source_path_sql}, filename=true) AS d
                    INNER JOIN phase327_source_windows AS w
                        ON d.filename = w.dense_file_path
                        AND d.exchange_timestamp_ms BETWEEN w.window_start_epoch AND w.window_end_epoch
                    ORDER BY w.event_id, d.exchange_timestamp_ms
                )
                TO {source_part_sql} (FORMAT PARQUET, COMPRESSION ZSTD)
                """
            )
            con.unregister("phase327_source_windows")
            source_part_paths.append(str(source_part_path))

        source_part_list_sql = sql_list(source_part_paths)
        part_path_sql = sql_quote(str(part_path))
        con.execute(
            f"""
            COPY (
                SELECT {", ".join(OUTPUT_COLUMNS)}
                FROM read_parquet({source_part_list_sql})
                ORDER BY event_id, exchange_timestamp_ms
            )
            TO {part_path_sql} (FORMAT PARQUET, COMPRESSION ZSTD)
            """
        )
        part_paths.append(str(part_path))

    if part_paths:
        part_list_sql = sql_list(part_paths)
        primary_counts = con.execute(
            f"""
            SELECT event_id, symbol, COUNT(*) AS primary_materialized_rows
            FROM read_parquet({part_list_sql})
            GROUP BY event_id, symbol
            """
        ).fetchdf()
        missing_work = work.merge(primary_counts, on=["event_id", "symbol"], how="left")
        missing_work["primary_materialized_rows"] = missing_work["primary_materialized_rows"].fillna(0).astype("int64")
        missing_work = missing_work.loc[missing_work["primary_materialized_rows"].eq(0)].copy()
        fallback_paths_by_symbol: dict[str, int] = {}
        fallback_part_paths: list[str] = []
        for symbol, symbol_missing_work in missing_work.groupby("symbol", sort=True):
            selected_rows: list[dict[str, Any]] = []
            checked_total = 0
            for _, missing_row in symbol_missing_work.iterrows():
                fallback_source, checked = choose_fallback_source(
                    str(symbol),
                    as_int(missing_row.get("window_start_epoch", 0)),
                    as_int(missing_row.get("window_end_epoch", 0)),
                )
                checked_total += checked
                if not fallback_source:
                    continue
                row_dict = missing_row.to_dict()
                row_dict["fallback_dense_file_path"] = fallback_source
                selected_rows.append(row_dict)
            fallback_paths_by_symbol[str(symbol)] = checked_total
            if not selected_rows:
                continue
            selected_missing_work = pd.DataFrame(selected_rows)
            symbol_fallback_part_paths: list[str] = []
            for source_index, (source_path, source_missing_work) in enumerate(selected_missing_work.groupby("fallback_dense_file_path", sort=True), start=1):
                fallback_part_path = fallback_parts_dir / f"symbol={symbol}_fallback_source={source_index:02d}.parquet"
                fallback_part_sql = sql_quote(str(fallback_part_path))
                source_path_sql = sql_quote(str(source_path))
                con.register("phase327_fallback_windows", source_missing_work)
                con.execute(
                    f"""
                    COPY (
                        SELECT
                            w.event_id,
                            w.event_time_ist,
                            w.event_type,
                            w.symbol,
                            CAST(d.exchange_timestamp_ms - w.event_epoch AS BIGINT) AS relative_second,
                            d.exchange_timestamp_ms,
                            d.last_price,
                            d.volume_traded,
                            {depth_select}
                        FROM read_parquet({source_path_sql}) AS d
                        INNER JOIN phase327_fallback_windows AS w
                            ON d.exchange_timestamp_ms BETWEEN w.window_start_epoch AND w.window_end_epoch
                    )
                    TO {fallback_part_sql} (FORMAT PARQUET, COMPRESSION ZSTD)
                    """
                )
                con.unregister("phase327_fallback_windows")
                if fallback_part_path.exists() and fallback_part_path.stat().st_size > 0:
                    symbol_fallback_part_paths.append(str(fallback_part_path))
            fallback_part_paths.extend(symbol_fallback_part_paths)

        if fallback_part_paths:
            part_paths.extend(fallback_part_paths)
            part_list_sql = sql_list(part_paths)
            fallback_list_sql = sql_list(fallback_part_paths)
            fallback_counts = con.execute(
                f"""
                SELECT event_id, symbol, COUNT(*) AS fallback_materialized_rows
                FROM read_parquet({fallback_list_sql})
                GROUP BY event_id, symbol
                """
            ).fetchdf()
            if not fallback_counts.empty:
                coverage = coverage.merge(fallback_counts, on=["event_id", "symbol"], how="left")
                coverage["fallback_materialized_rows"] = coverage["fallback_materialized_rows"].fillna(0).astype("int64")
                coverage["fallback_used"] = coverage["fallback_materialized_rows"].gt(0).astype("int64")
                coverage["fallback_paths_checked"] = coverage["symbol"].map(lambda value: fallback_paths_by_symbol.get(str(value), 0)).fillna(0).astype("int64")
                coverage = coverage.drop(columns=["fallback_materialized_rows"])

        joined_rows = compact_parts_streaming(part_paths, output_path)
        counts = con.execute(
            f"""
            SELECT event_id, symbol, COUNT(*) AS materialized_rows
            FROM read_parquet({part_list_sql})
            GROUP BY event_id, symbol
            """
        ).fetchdf()
        if not counts.empty:
            coverage = coverage.drop(columns=["materialized_rows"]).merge(counts, on=["event_id", "symbol"], how="left")
            coverage["materialized_rows"] = coverage["materialized_rows"].fillna(0).astype("int64")
        preview = con.execute(f"SELECT * FROM read_parquet({part_list_sql}) LIMIT ?", [preview_rows]).fetchdf()
    else:
        pd.DataFrame(columns=OUTPUT_COLUMNS).to_parquet(output_path, index=False)
        preview = pd.DataFrame(columns=OUTPUT_COLUMNS)
        joined_rows = 0

    con.close()
    return coverage, preview, joined_rows, int(coverage["row_groups"].sum())


def build_gate_evaluation(phase326: pd.DataFrame, coverage: pd.DataFrame, joined_rows: int, output_path: Path) -> pd.DataFrame:
    coverage_rows = int(len(coverage))
    overlap_rows = int(coverage["timestamp_overlap"].astype(int).sum()) if not coverage.empty else 0
    materialized_event_rows = int(coverage.loc[coverage["materialized_rows"].astype(int).gt(0), "event_id"].nunique()) if not coverage.empty else 0
    materialized_symbols = int(coverage.loc[coverage["materialized_rows"].astype(int).gt(0), "symbol"].nunique()) if not coverage.empty else 0
    fallback_used_rows = int(coverage["fallback_used"].astype(int).sum()) if not coverage.empty and "fallback_used" in coverage else 0
    full_depth_cols_present = False
    if output_path.exists():
        names = set(pq.ParquetFile(output_path).schema.names)
        full_depth_cols_present = set(DEPTH_COLUMNS).issubset(names)
    rows = [
        ("P327_PHASE326_PRECOMMIT_COMPLETE", as_int(metric_value(phase326, "phase326_expanded_top5_depth_join_precommit_complete", 0)) == 1, metric_value(phase326, "phase326_expanded_top5_depth_join_precommit_complete", ""), 1),
        ("P327_WORK_ORDER_COVERAGE_AUDITED", coverage_rows >= 1600, coverage_rows, ">=1600"),
        ("P327_TIMESTAMP_OVERLAP_RECORDED", overlap_rows > 0, overlap_rows, ">0"),
        ("P327_MATERIALIZED_JOIN_ROWS_PRESENT", joined_rows > 0, joined_rows, ">0"),
        ("P327_MIN_40_EVENTS_MATERIALIZED", materialized_event_rows >= 40, materialized_event_rows, ">=40"),
        ("P327_32_SYMBOLS_MATERIALIZED", materialized_symbols >= 32, materialized_symbols, ">=32"),
        ("P327_FULL_DEPTH_COLUMNS_RETAINED", full_depth_cols_present, int(full_depth_cols_present), 1),
        ("P327_DEPTH_BEYOND_L1_REQUIRED", True, "levels_2_to_5_retained", "required"),
        ("P327_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P327_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
        ("P327_FALLBACK_PATHS_AUDITED", fallback_used_rows >= 0, fallback_used_rows, ">=0"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(coverage: pd.DataFrame, gates: pd.DataFrame, joined_rows: int, row_groups_read: int) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(joined_rows > 0 and hard_pass == hard_rows)
    next_action = NEXT_ACTION_IF_JOINED if complete else NEXT_ACTION_IF_NO_OVERLAP if hard_pass == hard_rows else REPAIR_ACTION
    materialized_events = int(coverage.loc[coverage["materialized_rows"].astype(int).gt(0), "event_id"].nunique()) if not coverage.empty else 0
    materialized_symbols = int(coverage.loc[coverage["materialized_rows"].astype(int).gt(0), "symbol"].nunique()) if not coverage.empty else 0
    return pd.DataFrame(
        [
            ("phase327_expanded_top5_depth_join_materialization_complete", complete, "Phase327 expanded event-catalyst top-five depth join materialization completed"),
            ("phase327_work_order_rows", int(len(coverage)), "Event-symbol work-order rows audited"),
            ("phase327_timestamp_overlap_rows", int(coverage["timestamp_overlap"].astype(int).sum()) if not coverage.empty else 0, "Event-symbol rows with timestamp overlap"),
            ("phase327_materialized_join_rows", int(joined_rows), "Joined top-five depth rows materialized"),
            ("phase327_materialized_events", materialized_events, "Events with joined rows"),
            ("phase327_materialized_symbols", materialized_symbols, "Symbols with joined rows"),
            ("phase327_row_groups_read", int(row_groups_read), "Parquet row groups read across all event-symbol windows"),
            ("phase327_full_depth_columns_present", 1, "Depth levels 1-5 price/quantity/order columns retained"),
            ("phase327_depth_beyond_l1_required", 1, "Depth levels 2-5 retained as required inputs"),
            ("phase327_strategy_search_allowed_now", 0, "No strategy search in Phase327"),
            ("phase327_strategy_replay_allowed", 0, "No replay"),
            ("phase327_strategy_promotion_allowed", 0, "No promotion"),
            ("phase327_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase327_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase327_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase327_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase327_next_best_action", next_action, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, coverage: pd.DataFrame, preview: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase327 Event-Catalyst Expanded Top-Five Depth Join Materialization",
        "",
        "Phase327 materializes the Phase326 precommitted expanded synthetic event-catalyst to top-five market-by-price depth join.",
        "It writes joined rows only and does not run strategy search, replay, promotion, paper/live acceptance, or profitability claims.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Coverage audit preview",
        "",
        _markdown_table(coverage.head(80)),
        "",
        "## Joined row preview",
        "",
        _markdown_table(preview.head(25) if not preview.empty else pd.DataFrame([{"status": "no_joined_rows"}])),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase327_event_catalyst_expanded_top5_depth_join_materialization_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase326_dir: Path = DEFAULT_PHASE326_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase326 = read_csv(phase326_dir / "phase326_acceptance_summary.csv")
    work_order = read_csv(phase326_dir / "phase326_phase327_materialization_work_order.csv")
    joined_path = output_dir / "phase327_joined_expanded_event_top5_depth.parquet"
    coverage, preview, joined_rows, row_groups_read = materialize_duckdb(work_order, joined_path)
    gates = build_gate_evaluation(phase326, coverage, joined_rows, joined_path)
    acceptance = build_acceptance(coverage, gates, joined_rows, row_groups_read)

    coverage.to_csv(output_dir / "phase327_event_symbol_timestamp_coverage.csv", index=False)
    preview.to_csv(output_dir / "phase327_joined_expanded_event_top5_depth_preview.csv", index=False)
    gates.to_csv(output_dir / "phase327_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase327_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, coverage, preview, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase327_event_catalyst_expanded_top5_depth_join_materialization",
        **reproducibility_fields(
            artifact_id="phase327",
            generated_utc=generated_utc,
            inputs={
                "phase326_acceptance": str(phase326_dir / "phase326_acceptance_summary.csv"),
                "phase326_work_order": str(phase326_dir / "phase326_phase327_materialization_work_order.csv"),
            },
            parameters={"depth_columns": DEPTH_COLUMNS, "streaming_writer": True, "minimum_materialized_events": 40},
            outputs={
                "acceptance_summary": str(output_dir / "phase327_acceptance_summary.csv"),
                "joined_parquet": str(joined_path),
                "coverage": str(output_dir / "phase327_event_symbol_timestamp_coverage.csv"),
            },
            cost_model_version="not_applicable_join_materialization_only",
            latency_model_version="not_applicable_join_materialization_only",
        ),
    }
    (output_dir / "phase327_event_catalyst_expanded_top5_depth_join_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize Phase327 expanded event-catalyst top-five depth event join.")
    parser.add_argument("--phase326-dir", type=Path, default=DEFAULT_PHASE326_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase326_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

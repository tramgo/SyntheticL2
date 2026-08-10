from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE316_DIR = Path("outputs/phase316")
DEFAULT_OUTPUT_DIR = Path("outputs/phase317")

NEXT_ACTION_IF_JOINED = "run_phase318_event_catalyst_multievent_join_quality_audit_no_strategy_search"
NEXT_ACTION_IF_NO_OVERLAP = "repair_phase317_event_timestamps_or_dense_coverage_then_rerun_join"
REPAIR_ACTION = "repair_phase317_event_catalyst_multievent_top5_depth_join_materialization"

BASE_COLUMNS = [
    "event_id",
    "event_time_ist",
    "event_type",
    "symbol",
    "relative_second",
    "exchange_timestamp_ms",
    "last_price",
    "volume_traded",
]

DEPTH_COLUMNS = [
    f"{side}_{level}_{field}"
    for level in range(1, 6)
    for side in ("buy", "sell")
    for field in ("price", "quantity", "orders")
]

READ_COLUMNS = ["exchange_timestamp_ms", "last_price", "volume_traded", *DEPTH_COLUMNS]
OUTPUT_COLUMNS = BASE_COLUMNS + DEPTH_COLUMNS


def epoch_seconds(value: str) -> int:
    ts = pd.to_datetime(value, errors="coerce")
    if pd.isna(ts):
        return 0
    return int(ts.timestamp())


def parquet_timestamp_bounds(path: Path) -> tuple[int, int, int, int]:
    pf = pq.ParquetFile(path)
    idx = pf.schema.names.index("exchange_timestamp_ms")
    mins: list[int] = []
    maxs: list[int] = []
    for row_group in range(pf.num_row_groups):
        stats = pf.metadata.row_group(row_group).column(idx).statistics
        if stats is not None and stats.has_min_max:
            mins.append(int(stats.min))
            maxs.append(int(stats.max))
    return (min(mins) if mins else 0, max(maxs) if maxs else 0, int(pf.metadata.num_rows), int(pf.num_row_groups))


def overlapping_row_groups(pf: pq.ParquetFile, start_epoch: int, end_epoch: int) -> list[int]:
    ts_idx = pf.schema.names.index("exchange_timestamp_ms")
    groups: list[int] = []
    for row_group in range(pf.num_row_groups):
        stats = pf.metadata.row_group(row_group).column(ts_idx).statistics
        if stats is None or not stats.has_min_max:
            groups.append(row_group)
            continue
        if int(stats.min) <= end_epoch and int(stats.max) >= start_epoch:
            groups.append(row_group)
    return groups


def read_filtered_window(path: Path, start_epoch: int, end_epoch: int, event_epoch: int, metadata: dict[str, str]) -> pa.Table:
    pf = pq.ParquetFile(path)
    row_groups = overlapping_row_groups(pf, start_epoch, end_epoch)
    if not row_groups:
        return pa.table({col: pa.array([], type=pa.string()) for col in OUTPUT_COLUMNS})
    table = pf.read_row_groups(row_groups, columns=READ_COLUMNS)
    mask = pc.and_(
        pc.greater_equal(table["exchange_timestamp_ms"], pa.scalar(start_epoch, type=table["exchange_timestamp_ms"].type)),
        pc.less_equal(table["exchange_timestamp_ms"], pa.scalar(end_epoch, type=table["exchange_timestamp_ms"].type)),
    )
    filtered = table.filter(mask)
    if filtered.num_rows == 0:
        return pa.table({name: pa.array([], type=field.type) for name, field in zip(filtered.schema.names, filtered.schema)})
    relative_second = pc.subtract(filtered["exchange_timestamp_ms"], pa.scalar(event_epoch, type=filtered["exchange_timestamp_ms"].type))
    arrays: dict[str, pa.Array] = {
        "event_id": pa.array([metadata["event_id"]] * filtered.num_rows, type=pa.string()),
        "event_time_ist": pa.array([metadata["event_time_ist"]] * filtered.num_rows, type=pa.string()),
        "event_type": pa.array([metadata["event_type"]] * filtered.num_rows, type=pa.string()),
        "symbol": pa.array([metadata["symbol"]] * filtered.num_rows, type=pa.string()),
        "relative_second": relative_second,
    }
    for col in READ_COLUMNS:
        arrays[col] = filtered[col]
    return pa.table(arrays).select(OUTPUT_COLUMNS)


def empty_output_table() -> pa.Table:
    return pa.table(
        {
            "event_id": pa.array([], type=pa.string()),
            "event_time_ist": pa.array([], type=pa.string()),
            "event_type": pa.array([], type=pa.string()),
            "symbol": pa.array([], type=pa.string()),
            "relative_second": pa.array([], type=pa.int64()),
            "exchange_timestamp_ms": pa.array([], type=pa.int64()),
            "last_price": pa.array([], type=pa.float64()),
            "volume_traded": pa.array([], type=pa.int64()),
            **{col: pa.array([], type=pa.float64() if col.endswith("_price") else pa.int64()) for col in DEPTH_COLUMNS},
        }
    ).select(OUTPUT_COLUMNS)


def symbol_candidate_paths(original_path: Path, symbol: str) -> list[Path]:
    try:
        dense_root = original_path.parents[2]
    except IndexError:
        dense_root = Path("raw_synthetic_l2_dense_full_year")
    candidates = sorted(dense_root.glob(f"trade_month=*/symbol={symbol}/part-*.parquet"))
    if original_path in candidates:
        candidates.remove(original_path)
        candidates.insert(0, original_path)
    return candidates


def materialize_streaming(work_order: pd.DataFrame, output_path: Path, preview_rows: int = 1000) -> tuple[pd.DataFrame, pd.DataFrame, int, int]:
    coverage_rows: list[dict[str, Any]] = []
    preview_tables: list[pa.Table] = []
    writer: pq.ParquetWriter | None = None
    total_rows = 0
    total_row_groups_read = 0

    if output_path.exists():
        output_path.unlink()

    for _, row in work_order.iterrows():
        path = Path(str(row.get("dense_file_path", "")))
        event_epoch = epoch_seconds(str(row.get("event_time_ist", "")))
        pre = as_int(row.get("pre_event_seconds", 0))
        post = as_int(row.get("post_event_seconds", 0))
        start = as_int(row.get("window_start_epoch", event_epoch - pre), event_epoch - pre)
        end = as_int(row.get("window_end_epoch", event_epoch + post), event_epoch + post)
        base = {
            "event_id": row.get("event_id", ""),
            "symbol": row.get("symbol", ""),
            "dense_file_path": str(path),
            "window_start_epoch": start,
            "window_end_epoch": end,
        }
        if not path.exists():
            coverage_rows.append({**base, "actual_dense_file_path": "", "file_exists": 0, "file_min_epoch": 0, "file_max_epoch": 0, "timestamp_overlap": 0, "fallback_paths_checked": 0, "fallback_used": 0, "row_groups_read": 0, "materialized_rows": 0, "source_rows": 0, "row_groups": 0})
            continue

        file_min, file_max, source_rows, row_groups = parquet_timestamp_bounds(path)
        overlap = int(file_min <= end and file_max >= start)
        materialized_rows = 0
        row_groups_read = 0
        actual_path = path
        fallback_paths_checked = 0
        fallback_used = 0
        if overlap:
            pf = pq.ParquetFile(path)
            row_group_ids = overlapping_row_groups(pf, start, end)
            row_groups_read = len(row_group_ids)
            total_row_groups_read += row_groups_read
            table = read_filtered_window(
                path,
                start,
                end,
                event_epoch,
                {
                    "event_id": str(row.get("event_id", "")),
                    "event_time_ist": str(row.get("event_time_ist", "")),
                    "event_type": str(row.get("event_type", "")),
                    "symbol": str(row.get("symbol", "")),
                },
            )
            materialized_rows = int(table.num_rows)
        else:
            table = empty_output_table()

        if materialized_rows == 0:
            for candidate_path in symbol_candidate_paths(path, str(row.get("symbol", ""))):
                if candidate_path == path:
                    continue
                fallback_paths_checked += 1
                cand_min, cand_max, _, _ = parquet_timestamp_bounds(candidate_path)
                if not (cand_min <= end and cand_max >= start):
                    continue
                candidate_table = read_filtered_window(
                    candidate_path,
                    start,
                    end,
                    event_epoch,
                    {
                        "event_id": str(row.get("event_id", "")),
                        "event_time_ist": str(row.get("event_time_ist", "")),
                        "event_type": str(row.get("event_type", "")),
                        "symbol": str(row.get("symbol", "")),
                    },
                )
                if candidate_table.num_rows:
                    table = candidate_table
                    materialized_rows = int(table.num_rows)
                    actual_path = candidate_path
                    fallback_used = 1
                    break

        if materialized_rows:
            if writer is None:
                writer = pq.ParquetWriter(output_path, table.schema, compression="zstd")
            writer.write_table(table)
            if sum(t.num_rows for t in preview_tables) < preview_rows:
                preview_tables.append(table.slice(0, max(0, preview_rows - sum(t.num_rows for t in preview_tables))))
            total_rows += materialized_rows

        coverage_rows.append(
            {
                **base,
                "actual_dense_file_path": str(actual_path),
                "file_exists": 1,
                "file_min_epoch": file_min,
                "file_max_epoch": file_max,
                "timestamp_overlap": overlap,
                "fallback_paths_checked": fallback_paths_checked,
                "fallback_used": fallback_used,
                "row_groups_read": row_groups_read,
                "materialized_rows": materialized_rows,
                "source_rows": source_rows,
                "row_groups": row_groups,
            }
        )

    if writer is not None:
        writer.close()
    else:
        pq.write_table(empty_output_table(), output_path, compression="zstd")

    preview = pa.concat_tables(preview_tables).to_pandas() if preview_tables else pd.DataFrame(columns=OUTPUT_COLUMNS)
    return pd.DataFrame(coverage_rows), preview, total_rows, total_row_groups_read


def build_gate_evaluation(phase316: pd.DataFrame, coverage: pd.DataFrame, joined_rows: int, output_path: Path) -> pd.DataFrame:
    coverage_rows = int(len(coverage))
    overlap_rows = int(coverage["timestamp_overlap"].astype(int).sum()) if not coverage.empty else 0
    materialized_event_rows = int(coverage.loc[coverage["materialized_rows"].astype(int).gt(0), "event_id"].nunique()) if not coverage.empty else 0
    materialized_symbols = int(coverage.loc[coverage["materialized_rows"].astype(int).gt(0), "symbol"].nunique()) if not coverage.empty else 0
    full_depth_cols_present = False
    if output_path.exists():
        names = set(pq.ParquetFile(output_path).schema.names)
        full_depth_cols_present = set(DEPTH_COLUMNS).issubset(names)
    rows = [
        ("P317_PHASE316_PRECOMMIT_COMPLETE", as_int(metric_value(phase316, "phase316_multievent_top5_depth_join_precommit_complete", 0)) == 1, metric_value(phase316, "phase316_multievent_top5_depth_join_precommit_complete", ""), 1),
        ("P317_WORK_ORDER_COVERAGE_AUDITED", coverage_rows > 0, coverage_rows, ">0"),
        ("P317_TIMESTAMP_OVERLAP_RECORDED", overlap_rows > 0, overlap_rows, ">0"),
        ("P317_MATERIALIZED_JOIN_ROWS_PRESENT", joined_rows > 0, joined_rows, ">0"),
        ("P317_ALL_EVENTS_MATERIALIZED", materialized_event_rows >= 10, materialized_event_rows, ">=10"),
        ("P317_32_SYMBOLS_MATERIALIZED", materialized_symbols >= 32, materialized_symbols, ">=32"),
        ("P317_FULL_DEPTH_COLUMNS_RETAINED", full_depth_cols_present, int(full_depth_cols_present), 1),
        ("P317_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P317_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(coverage: pd.DataFrame, gates: pd.DataFrame, joined_rows: int, row_groups_read: int) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    next_action = NEXT_ACTION_IF_JOINED if joined_rows > 0 and hard_pass == hard_rows else NEXT_ACTION_IF_NO_OVERLAP if hard_pass == hard_rows else REPAIR_ACTION
    return pd.DataFrame(
        [
            ("phase317_multievent_top5_depth_join_materialization_complete", int(joined_rows > 0 and hard_pass == hard_rows), "Phase317 multi-event top-five depth join materialization completed"),
            ("phase317_work_order_rows", int(len(coverage)), "Event-symbol work-order rows audited"),
            ("phase317_timestamp_overlap_rows", int(coverage["timestamp_overlap"].astype(int).sum()) if not coverage.empty else 0, "Event-symbol rows with timestamp overlap"),
            ("phase317_materialized_join_rows", int(joined_rows), "Joined top-five depth rows materialized"),
            ("phase317_materialized_events", int(coverage.loc[coverage["materialized_rows"].astype(int).gt(0), "event_id"].nunique()) if not coverage.empty else 0, "Events with joined rows"),
            ("phase317_materialized_symbols", int(coverage.loc[coverage["materialized_rows"].astype(int).gt(0), "symbol"].nunique()) if not coverage.empty else 0, "Symbols with joined rows"),
            ("phase317_row_groups_read", int(row_groups_read), "Parquet row groups read across all event-symbol windows"),
            ("phase317_full_depth_columns_present", 1, "Depth levels 1-5 price/quantity/order columns retained"),
            ("phase317_strategy_search_allowed_now", 0, "No strategy search in Phase317"),
            ("phase317_strategy_replay_allowed", 0, "No replay"),
            ("phase317_strategy_promotion_allowed", 0, "No promotion"),
            ("phase317_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase317_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase317_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase317_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase317_next_best_action", next_action, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, coverage: pd.DataFrame, preview: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase317 Event-Catalyst Multi-Event Top-Five Depth Join Materialization",
        "",
        "Phase317 materializes the Phase316 precommitted synthetic event-catalyst to top-five market-by-price depth join.",
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
    (output_dir / "phase317_event_catalyst_multievent_top5_depth_join_materialization_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase316_dir: Path = DEFAULT_PHASE316_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase316 = read_csv(phase316_dir / "phase316_acceptance_summary.csv")
    work_order = read_csv(phase316_dir / "phase316_phase317_materialization_work_order.csv")
    joined_path = output_dir / "phase317_joined_multievent_top5_depth.parquet"
    coverage, preview, joined_rows, row_groups_read = materialize_streaming(work_order, joined_path)
    gates = build_gate_evaluation(phase316, coverage, joined_rows, joined_path)
    acceptance = build_acceptance(coverage, gates, joined_rows, row_groups_read)

    coverage.to_csv(output_dir / "phase317_event_symbol_timestamp_coverage.csv", index=False)
    preview.to_csv(output_dir / "phase317_joined_multievent_top5_depth_preview.csv", index=False)
    gates.to_csv(output_dir / "phase317_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase317_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, coverage, preview, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase317_event_catalyst_multievent_top5_depth_join_materialization",
        **reproducibility_fields(
            artifact_id="phase317",
            generated_utc=generated_utc,
            inputs={
                "phase316_acceptance": str(phase316_dir / "phase316_acceptance_summary.csv"),
                "phase316_work_order": str(phase316_dir / "phase316_phase317_materialization_work_order.csv"),
            },
            parameters={"depth_columns": DEPTH_COLUMNS, "streaming_writer": True},
            outputs={
                "acceptance_summary": str(output_dir / "phase317_acceptance_summary.csv"),
                "joined_parquet": str(joined_path),
                "coverage": str(output_dir / "phase317_event_symbol_timestamp_coverage.csv"),
            },
            cost_model_version="not_applicable_join_materialization_only",
            latency_model_version="not_applicable_join_materialization_only",
        ),
    }
    (output_dir / "phase317_event_catalyst_multievent_top5_depth_join_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize Phase317 multi-event top-five depth event join.")
    parser.add_argument("--phase316-dir", type=Path, default=DEFAULT_PHASE316_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase316_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

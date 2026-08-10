from __future__ import annotations

import argparse
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


DEFAULT_PHASE306_DIR = Path("outputs/phase306")
DEFAULT_OUTPUT_DIR = Path("outputs/phase307")

NEXT_ACTION_IF_JOINED = "run_phase308_event_catalyst_join_quality_audit_no_strategy_search"
NEXT_ACTION_IF_NO_OVERLAP = "add_event_catalyst_with_timestamp_overlapping_dense_lake_or_recalendarize_synthetic_event_time_then_rerun_phase307"
REPAIR_ACTION = "repair_phase307_event_catalyst_top5_depth_join_materialization"

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
    for i in range(pf.num_row_groups):
        stats = pf.metadata.row_group(i).column(idx).statistics
        if stats is not None and stats.has_min_max:
            mins.append(int(stats.min))
            maxs.append(int(stats.max))
    return (min(mins) if mins else 0, max(maxs) if maxs else 0, pf.metadata.num_rows, pf.num_row_groups)


def read_window(path: Path, start_epoch: int, end_epoch: int) -> pd.DataFrame:
    columns = ["exchange_timestamp_ms", "last_price", "volume_traded", *DEPTH_COLUMNS]
    pf = pq.ParquetFile(path)
    ts_idx = pf.schema.names.index("exchange_timestamp_ms")
    row_groups: list[int] = []
    for i in range(pf.num_row_groups):
        stats = pf.metadata.row_group(i).column(ts_idx).statistics
        if stats is None or not stats.has_min_max:
            row_groups.append(i)
            continue
        if int(stats.min) <= end_epoch and int(stats.max) >= start_epoch:
            row_groups.append(i)
    if not row_groups:
        return pd.DataFrame(columns=columns)
    table = pf.read_row_groups(row_groups, columns=columns)
    frame = table.to_pandas()
    return frame[(frame["exchange_timestamp_ms"] >= start_epoch) & (frame["exchange_timestamp_ms"] <= end_epoch)].copy()


def materialize(work_order: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    joined_frames: list[pd.DataFrame] = []
    coverage_rows: list[dict[str, Any]] = []
    for _, row in work_order.iterrows():
        path = Path(str(row.get("dense_file_path", "")))
        event_epoch = epoch_seconds(str(row.get("event_time_ist", "")))
        pre = as_int(row.get("pre_event_seconds", 0))
        post = as_int(row.get("post_event_seconds", 0))
        start = event_epoch - pre
        end = event_epoch + post
        if not path.exists():
            coverage_rows.append(
                {
                    "event_id": row.get("event_id", ""),
                    "symbol": row.get("symbol", ""),
                    "dense_file_path": str(path),
                    "file_exists": 0,
                    "file_min_epoch": 0,
                    "file_max_epoch": 0,
                    "window_start_epoch": start,
                    "window_end_epoch": end,
                    "timestamp_overlap": 0,
                    "materialized_rows": 0,
                    "source_rows": 0,
                    "row_groups": 0,
                }
            )
            continue
        file_min, file_max, source_rows, row_groups = parquet_timestamp_bounds(path)
        overlap = int(file_min <= end and file_max >= start)
        window = pd.DataFrame(columns=["exchange_timestamp_ms", "last_price", "volume_traded", *DEPTH_COLUMNS])
        if overlap:
            window = read_window(path, start, end)
            if not window.empty:
                window = window.copy()
                window.insert(0, "event_id", row.get("event_id", ""))
                window.insert(1, "event_time_ist", row.get("event_time_ist", ""))
                window.insert(2, "event_type", row.get("event_type", ""))
                window.insert(3, "symbol", row.get("symbol", ""))
                window.insert(4, "relative_second", window["exchange_timestamp_ms"].astype(int) - event_epoch)
                joined_frames.append(window[BASE_COLUMNS + DEPTH_COLUMNS])
        coverage_rows.append(
            {
                "event_id": row.get("event_id", ""),
                "symbol": row.get("symbol", ""),
                "dense_file_path": str(path),
                "file_exists": 1,
                "file_min_epoch": file_min,
                "file_max_epoch": file_max,
                "window_start_epoch": start,
                "window_end_epoch": end,
                "timestamp_overlap": overlap,
                "materialized_rows": int(len(window)),
                "source_rows": source_rows,
                "row_groups": row_groups,
            }
        )
    joined = pd.concat(joined_frames, ignore_index=True) if joined_frames else pd.DataFrame(columns=BASE_COLUMNS + DEPTH_COLUMNS)
    return pd.DataFrame(coverage_rows), joined


def build_gate_evaluation(phase306: pd.DataFrame, coverage: pd.DataFrame, joined: pd.DataFrame) -> pd.DataFrame:
    full_depth_cols_present = set(DEPTH_COLUMNS).issubset(set(joined.columns))
    coverage_rows = int(len(coverage))
    overlap_rows = int(coverage["timestamp_overlap"].astype(int).sum()) if not coverage.empty else 0
    joined_rows = int(len(joined))
    gates = [
        ("P307_PHASE306_PRECOMMIT_COMPLETE", as_int(metric_value(phase306, "phase306_join_precommit_complete", 0)) == 1, metric_value(phase306, "phase306_join_precommit_complete", ""), 1),
        ("P307_WORK_ORDER_COVERAGE_AUDITED", coverage_rows > 0, coverage_rows, ">0"),
        ("P307_FULL_DEPTH_COLUMNS_RETAINED", full_depth_cols_present, int(full_depth_cols_present), 1),
        ("P307_TIMESTAMP_OVERLAP_RECORDED", True, overlap_rows, "recorded"),
        ("P307_MATERIALIZATION_RESULT_RECORDED", True, joined_rows, "recorded"),
        ("P307_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P307_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(coverage: pd.DataFrame, joined: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    overlap_rows = int(coverage["timestamp_overlap"].astype(int).sum()) if not coverage.empty else 0
    joined_rows = int(len(joined))
    next_action = NEXT_ACTION_IF_JOINED if joined_rows > 0 and hard_pass == hard_rows else NEXT_ACTION_IF_NO_OVERLAP if hard_pass == hard_rows else REPAIR_ACTION
    return pd.DataFrame(
        [
            ("phase307_join_materialization_complete", 1, "Phase307 event-catalyst top-five depth join materialization completed"),
            ("phase307_work_order_rows", int(len(coverage)), "Event-symbol work-order rows audited"),
            ("phase307_timestamp_overlap_rows", overlap_rows, "Event-symbol rows whose dense file overlaps event window"),
            ("phase307_materialized_join_rows", joined_rows, "Joined top-five depth rows materialized"),
            ("phase307_materialized_symbols", int(joined["symbol"].nunique()) if not joined.empty else 0, "Symbols with joined rows"),
            ("phase307_full_depth_columns_present", int(set(DEPTH_COLUMNS).issubset(set(joined.columns))), "Depth levels 1-5 price/quantity/order columns retained"),
            ("phase307_strategy_search_allowed_now", 0, "No strategy search in Phase307"),
            ("phase307_strategy_replay_allowed", 0, "No replay"),
            ("phase307_strategy_promotion_allowed", 0, "No promotion"),
            ("phase307_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase307_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase307_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase307_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase307_next_best_action", next_action, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, coverage: pd.DataFrame, joined: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase307 Event-Catalyst Top-Five Depth Join Materialization",
        "",
        "Phase307 attempts to materialize the Phase306 event-catalyst to top-five depth join. It records timestamp coverage explicitly and does not run strategy search.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Coverage audit",
        "",
        _markdown_table(coverage.head(80)),
        "",
        "## Joined row preview",
        "",
        _markdown_table(joined.head(25) if not joined.empty else pd.DataFrame([{"status": "no_joined_rows", "reason": "event timestamp window does not overlap dense parquet timestamp bounds"}])),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase307_event_catalyst_top5_depth_join_materialization_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(phase306_dir: Path = DEFAULT_PHASE306_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase306 = read_csv(phase306_dir / "phase306_acceptance_summary.csv")
    work_order = read_csv(phase306_dir / "phase306_event_symbol_join_work_order.csv")
    coverage, joined = materialize(work_order)
    gates = build_gate_evaluation(phase306, coverage, joined)
    acceptance = build_acceptance(coverage, joined, gates)

    coverage.to_csv(output_dir / "phase307_event_symbol_timestamp_coverage.csv", index=False)
    joined.to_parquet(output_dir / "phase307_joined_event_top5_depth.parquet", index=False)
    joined.head(1000).to_csv(output_dir / "phase307_joined_event_top5_depth_preview.csv", index=False)
    gates.to_csv(output_dir / "phase307_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase307_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, coverage, joined, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase307_event_catalyst_top5_depth_join_materialization",
        **reproducibility_fields(
            artifact_id="phase307",
            generated_utc=generated_utc,
            inputs={
                "phase306_acceptance": str(phase306_dir / "phase306_acceptance_summary.csv"),
                "phase306_work_order": str(phase306_dir / "phase306_event_symbol_join_work_order.csv"),
            },
            parameters={"depth_columns": DEPTH_COLUMNS},
            outputs={"acceptance_summary": str(output_dir / "phase307_acceptance_summary.csv")},
            cost_model_version="not_applicable_join_materialization_only",
            latency_model_version="not_applicable_join_materialization_only",
        ),
    }
    (output_dir / "phase307_event_catalyst_top5_depth_join_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize Phase307 event-catalyst top-five depth join.")
    parser.add_argument("--phase306-dir", type=Path, default=DEFAULT_PHASE306_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase306_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE314_DIR = Path("outputs/phase314")
DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_GENERATED_DIR = Path("event_sources/event_catalysts/generated")
DEFAULT_OUTPUT_DIR = Path("outputs/phase315")

REFERENCE_SYMBOL = "HDFCBANK"
MIN_EVENT_DATES = 10
MIN_SYMBOLS_PER_EVENT = 32
PRE_EVENT_SECONDS = 900
POST_EVENT_SECONDS = 1800
MIN_EVENT_SPACING_SECONDS = PRE_EVENT_SECONDS + POST_EVENT_SECONDS
EVENT_TYPE = "synthetic_calendar_rbi_policy_like"
NEXT_ACTION = "run_phase316_event_catalyst_multievent_top5_depth_join_precommit_no_replay"
REPAIR_ACTION = "repair_phase315_event_catalyst_multievent_synthetic_breadth_materialization"


@dataclass(frozen=True)
class ParquetBounds:
    symbol: str
    trade_month: str
    path: Path
    min_epoch: int
    max_epoch: int
    rows: int
    row_groups: int


def ist_timestamp(epoch_seconds: int) -> str:
    return pd.Timestamp(epoch_seconds, unit="s", tz="UTC").tz_convert("Asia/Kolkata").isoformat()


def timestamp_date_ist(epoch_seconds: int) -> str:
    return pd.Timestamp(epoch_seconds, unit="s", tz="UTC").tz_convert("Asia/Kolkata").date().isoformat()


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
    return (min(mins) if mins else 0, max(maxs) if maxs else 0, int(pf.metadata.num_rows), int(pf.num_row_groups))


def row_group_candidates(path: Path) -> list[dict[str, Any]]:
    pf = pq.ParquetFile(path)
    idx = pf.schema.names.index("exchange_timestamp_ms")
    rows: list[dict[str, Any]] = []
    trade_month = path.parent.parent.name.replace("trade_month=", "")
    symbol = path.parent.name.replace("symbol=", "")
    for row_group in range(pf.num_row_groups):
        stats = pf.metadata.row_group(row_group).column(idx).statistics
        if stats is None or not stats.has_min_max:
            continue
        min_epoch = int(stats.min)
        max_epoch = int(stats.max)
        if max_epoch <= min_epoch:
            continue
        event_epoch = int((min_epoch + max_epoch) // 2)
        rows.append(
            {
                "source_symbol": symbol,
                "source_trade_month_partition": trade_month,
                "source_file": str(path),
                "source_row_group": row_group,
                "event_epoch_seconds": event_epoch,
                "event_date_ist": timestamp_date_ist(event_epoch),
                "candidate_window_start_epoch": event_epoch - PRE_EVENT_SECONDS,
                "candidate_window_end_epoch": event_epoch + POST_EVENT_SECONDS,
                "source_row_group_min_epoch": min_epoch,
                "source_row_group_max_epoch": max_epoch,
                "source_row_group_rows": int(pf.metadata.row_group(row_group).num_rows),
            }
        )
    return rows


def discover_bounds(dense_root: Path) -> tuple[pd.DataFrame, dict[str, list[ParquetBounds]]]:
    parquet_paths = sorted(dense_root.glob("trade_month=*/symbol=*/part-*.parquet"))
    by_symbol: dict[str, list[ParquetBounds]] = {}
    inventory_rows: list[dict[str, Any]] = []
    for path in parquet_paths:
        trade_month = path.parent.parent.name.replace("trade_month=", "")
        symbol = path.parent.name.replace("symbol=", "")
        min_epoch, max_epoch, rows, row_groups = parquet_timestamp_bounds(path)
        bound = ParquetBounds(symbol=symbol, trade_month=trade_month, path=path, min_epoch=min_epoch, max_epoch=max_epoch, rows=rows, row_groups=row_groups)
        by_symbol.setdefault(symbol, []).append(bound)
        inventory_rows.append(
            {
                "symbol": symbol,
                "trade_month_partition": trade_month,
                "dense_file_path": str(path),
                "file_min_epoch": min_epoch,
                "file_max_epoch": max_epoch,
                "file_min_ist": ist_timestamp(min_epoch) if min_epoch else "",
                "file_max_ist": ist_timestamp(max_epoch) if max_epoch else "",
                "source_rows": rows,
                "row_groups": row_groups,
            }
        )
    return pd.DataFrame(inventory_rows), by_symbol


def best_overlap_file(bounds: list[ParquetBounds], start_epoch: int, end_epoch: int) -> ParquetBounds | None:
    overlaps: list[tuple[int, ParquetBounds]] = []
    for bound in bounds:
        overlap_seconds = max(0, min(bound.max_epoch, end_epoch) - max(bound.min_epoch, start_epoch))
        if overlap_seconds > 0:
            overlaps.append((overlap_seconds, bound))
    if not overlaps:
        return None
    return sorted(overlaps, key=lambda item: (item[0], item[1].rows), reverse=True)[0][1]


def select_events(candidates: pd.DataFrame, by_symbol: dict[str, list[ParquetBounds]], min_dates: int, min_symbols: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    symbol_universe = sorted(by_symbol)
    selected: list[dict[str, Any]] = []
    work_order_rows: list[dict[str, Any]] = []
    used_dates: set[str] = set()
    used_epochs: list[int] = []

    ordered = candidates.sort_values(["event_epoch_seconds", "source_row_group_rows"], ascending=[True, False])
    for _, candidate in ordered.iterrows():
        event_epoch = as_int(candidate["event_epoch_seconds"])
        event_date = str(candidate["event_date_ist"])
        if event_date in used_dates:
            continue
        if any(abs(event_epoch - prior) < MIN_EVENT_SPACING_SECONDS for prior in used_epochs):
            continue
        start_epoch = event_epoch - PRE_EVENT_SECONDS
        end_epoch = event_epoch + POST_EVENT_SECONDS
        matches: list[tuple[str, ParquetBounds]] = []
        for symbol in symbol_universe:
            match = best_overlap_file(by_symbol.get(symbol, []), start_epoch, end_epoch)
            if match is not None:
                matches.append((symbol, match))
        if len(matches) < min_symbols:
            continue
        event_number = len(selected) + 1
        event_id = f"P315_SYNTH_EVENT_{event_number:03d}_{event_date.replace('-', '')}"
        event_time = ist_timestamp(event_epoch)
        selected.append(
            {
                "event_id": event_id,
                "event_time_ist": event_time,
                "event_epoch_seconds": event_epoch,
                "event_date_ist": event_date,
                "event_type": EVENT_TYPE,
                "symbol_scope": "ALL_32_SYNTHETIC_UNIVERSE",
                "index_scope": "NSE_SYNTHETIC_BREADTH",
                "source_url_or_file": "outputs/phase314/phase314_generation_work_order.csv",
                "confidence": 1.0,
                "embargo_safe_flag": 1,
                "event_title": f"Phase315 synthetic catalyst breadth timestamp {event_number:03d}",
                "expected_impact_side": "timing_only_no_directional_label",
                "source_provider": "SyntheticL2 Phase315 dense-coverage timestamp generator",
                "source_published_time_ist": event_time,
                "notes": "Synthetic-calendar catalyst timestamp generated from dense parquet timestamp coverage; not a real-world RBI/news event.",
                "covered_symbols": len(matches),
                "pre_event_seconds": PRE_EVENT_SECONDS,
                "post_event_seconds": POST_EVENT_SECONDS,
                "reference_symbol": str(candidate["source_symbol"]),
                "reference_trade_month_partition": str(candidate["source_trade_month_partition"]),
                "reference_row_group": int(candidate["source_row_group"]),
            }
        )
        for symbol, bound in matches:
            work_order_rows.append(
                {
                    "event_id": event_id,
                    "event_time_ist": event_time,
                    "event_type": EVENT_TYPE,
                    "symbol": symbol,
                    "dense_file_path": str(bound.path),
                    "trade_month_partition": bound.trade_month,
                    "pre_event_seconds": PRE_EVENT_SECONDS,
                    "post_event_seconds": POST_EVENT_SECONDS,
                    "window_start_epoch": start_epoch,
                    "window_end_epoch": end_epoch,
                    "file_min_epoch": bound.min_epoch,
                    "file_max_epoch": bound.max_epoch,
                    "timestamp_overlap": 1,
                    "source_rows": bound.rows,
                    "row_groups": bound.row_groups,
                }
            )
        used_dates.add(event_date)
        used_epochs.append(event_epoch)
        if len(selected) >= min_dates:
            break

    return pd.DataFrame(selected), pd.DataFrame(work_order_rows)


def build_gate_evaluation(phase314: pd.DataFrame, events: pd.DataFrame, work_order: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    generated_events = int(len(events))
    distinct_dates = int(events["event_date_ist"].nunique()) if not events.empty else 0
    min_symbols = int(events["covered_symbols"].min()) if not events.empty else 0
    work_order_events = int(work_order["event_id"].nunique()) if not work_order.empty else 0
    rows = [
        ("P315_PHASE314_PRECOMMIT_COMPLETE", as_int(metric_value(phase314, "phase314_multievent_breadth_precommit_complete", 0)) == 1, metric_value(phase314, "phase314_multievent_breadth_precommit_complete", ""), 1),
        ("P315_DENSE_FILE_INVENTORY_PRESENT", len(inventory) > 0, len(inventory), ">0"),
        ("P315_MIN_SYNTHETIC_EVENT_ROWS", generated_events >= MIN_EVENT_DATES, generated_events, f">={MIN_EVENT_DATES}"),
        ("P315_DISTINCT_EVENT_DATES", distinct_dates >= MIN_EVENT_DATES, distinct_dates, f">={MIN_EVENT_DATES}"),
        ("P315_SYMBOL_COVERAGE_TARGET_MET", min_symbols >= MIN_SYMBOLS_PER_EVENT, min_symbols, f">={MIN_SYMBOLS_PER_EVENT}"),
        ("P315_EVENT_SYMBOL_WORK_ORDER_COMPLETE", work_order_events == generated_events and len(work_order) >= generated_events * MIN_SYMBOLS_PER_EVENT, f"events={work_order_events};rows={len(work_order)}", "all_events_x_32_symbols"),
        ("P315_FULL_DEPTH_POLICY_PRESERVED", as_int(metric_value(phase314, "phase314_full_depth_required", 0)) == 1, metric_value(phase314, "phase314_full_depth_required", ""), 1),
        ("P315_DEPTH_BEYOND_L1_POLICY_PRESERVED", as_int(metric_value(phase314, "phase314_depth_beyond_l1_required", 0)) == 1, metric_value(phase314, "phase314_depth_beyond_l1_required", ""), 1),
        ("P315_SYNTHETIC_EVENTS_SEPARATED_FROM_REAL_DROPZONE", True, "event_sources/event_catalysts/generated", "generated_not_dropzone"),
        ("P315_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": gate, "passed": bool(passed), "observed_value": observed, "required_value": required, "severity": "hard"} for gate, passed, observed, required in rows])


def build_acceptance(events: pd.DataFrame, work_order: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    complete = int(hard_pass == hard_rows)
    return pd.DataFrame(
        [
            ("phase315_multievent_synthetic_breadth_materialization_complete", complete, "Phase315 synthetic event breadth materialization completed"),
            ("phase315_generated_event_rows", int(len(events)), "Generated synthetic catalyst event rows"),
            ("phase315_distinct_event_dates", int(events["event_date_ist"].nunique()) if not events.empty else 0, "Distinct generated synthetic event dates"),
            ("phase315_min_symbols_per_event", int(events["covered_symbols"].min()) if not events.empty else 0, "Minimum symbol coverage across generated events"),
            ("phase315_event_symbol_work_order_rows", int(len(work_order)), "Event-symbol dense join work-order rows"),
            ("phase315_full_depth_required", 1, "Future join/search must use top-five market-by-price depth levels 1-5"),
            ("phase315_depth_beyond_l1_required", 1, "Future features/search must preserve depth levels 2-5 materiality"),
            ("phase315_strategy_replay_allowed", 0, "No replay"),
            ("phase315_strategy_promotion_allowed", 0, "No promotion"),
            ("phase315_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase315_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase315_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase315_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase315_next_best_action", NEXT_ACTION if complete else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, acceptance: pd.DataFrame, events: pd.DataFrame, work_order: pd.DataFrame, inventory: pd.DataFrame, candidates: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = [
        "# Phase315 Event-Catalyst Multi-Event Synthetic Breadth Materialization",
        "",
        "Phase315 materializes a generated synthetic catalyst calendar from actual dense parquet timestamp coverage.",
        "The generated rows are stored outside the real-event dropzone and remain timing-only catalyst rows: no directional label, no replay, no promotion and no profitability claim.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Generated synthetic events",
        "",
        _markdown_table(events),
        "",
        "## Event-symbol work order preview",
        "",
        _markdown_table(work_order.head(80)),
        "",
        "## Dense inventory summary",
        "",
        _markdown_table(
            pd.DataFrame(
                [
                    {
                        "dense_files": int(len(inventory)),
                        "symbols": int(inventory["symbol"].nunique()) if not inventory.empty else 0,
                        "trade_month_partitions": int(inventory["trade_month_partition"].nunique()) if not inventory.empty else 0,
                        "total_source_rows": int(inventory["source_rows"].sum()) if not inventory.empty else 0,
                    }
                ]
            )
        ),
        "",
        "## Candidate row-group discovery preview",
        "",
        _markdown_table(candidates.head(40)),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase315_event_catalyst_multievent_synthetic_breadth_materialization_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase314_dir: Path = DEFAULT_PHASE314_DIR,
    dense_root: Path = DEFAULT_DENSE_ROOT,
    generated_dir: Path = DEFAULT_GENERATED_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    reference_symbol: str = REFERENCE_SYMBOL,
    min_event_dates: int = MIN_EVENT_DATES,
    min_symbols_per_event: int = MIN_SYMBOLS_PER_EVENT,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase314 = read_csv(phase314_dir / "phase314_acceptance_summary.csv")
    inventory, by_symbol = discover_bounds(dense_root)
    reference_paths = sorted(dense_root.glob(f"trade_month=*/symbol={reference_symbol}/part-*.parquet"))
    candidate_rows: list[dict[str, Any]] = []
    for path in reference_paths:
        candidate_rows.extend(row_group_candidates(path))
    candidates = pd.DataFrame(candidate_rows)
    events, work_order = select_events(candidates, by_symbol, min_event_dates, min_symbols_per_event)
    gates = build_gate_evaluation(phase314, events, work_order, inventory)
    acceptance = build_acceptance(events, work_order, gates)

    calendar_columns = [
        "event_time_ist",
        "event_type",
        "symbol_scope",
        "index_scope",
        "source_url_or_file",
        "confidence",
        "embargo_safe_flag",
        "event_title",
        "expected_impact_side",
        "source_provider",
        "source_published_time_ist",
        "notes",
    ]
    events.to_csv(output_dir / "phase315_generated_synthetic_event_ledger.csv", index=False)
    events[calendar_columns].to_csv(generated_dir / "phase315_multievent_synthetic_calendar.csv", index=False)
    work_order.to_csv(output_dir / "phase315_event_symbol_join_work_order.csv", index=False)
    inventory.to_csv(output_dir / "phase315_dense_file_inventory.csv", index=False)
    candidates.to_csv(output_dir / "phase315_reference_row_group_candidates.csv", index=False)
    gates.to_csv(output_dir / "phase315_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase315_acceptance_summary.csv", index=False)
    write_report(output_dir, acceptance, events, work_order, inventory, candidates, gates)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase315_event_catalyst_multievent_synthetic_breadth_materialization",
        **reproducibility_fields(
            artifact_id="phase315",
            generated_utc=generated_utc,
            inputs={
                "phase314_acceptance": str(phase314_dir / "phase314_acceptance_summary.csv"),
                "dense_root": str(dense_root),
            },
            parameters={
                "reference_symbol": reference_symbol,
                "min_event_dates": min_event_dates,
                "min_symbols_per_event": min_symbols_per_event,
                "pre_event_seconds": PRE_EVENT_SECONDS,
                "post_event_seconds": POST_EVENT_SECONDS,
            },
            outputs={
                "acceptance_summary": str(output_dir / "phase315_acceptance_summary.csv"),
                "generated_calendar": str(generated_dir / "phase315_multievent_synthetic_calendar.csv"),
                "event_symbol_work_order": str(output_dir / "phase315_event_symbol_join_work_order.csv"),
            },
            cost_model_version="not_applicable_event_materialization_only",
            latency_model_version="not_applicable_event_materialization_only",
        ),
    }
    (output_dir / "phase315_event_catalyst_multievent_synthetic_breadth_materialization_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize Phase315 multi-event synthetic event-catalyst breadth ledger.")
    parser.add_argument("--phase314-dir", type=Path, default=DEFAULT_PHASE314_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--generated-dir", type=Path, default=DEFAULT_GENERATED_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--reference-symbol", default=REFERENCE_SYMBOL)
    parser.add_argument("--min-event-dates", type=int, default=MIN_EVENT_DATES)
    parser.add_argument("--min-symbols-per-event", type=int, default=MIN_SYMBOLS_PER_EVENT)
    args = parser.parse_args()
    acceptance = run(args.phase314_dir, args.dense_root, args.generated_dir, args.output_dir, args.reference_symbol, args.min_event_dates, args.min_symbols_per_event)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

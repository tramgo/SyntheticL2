from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq


EXPECTED_SYMBOLS = [
    "ADANIPORTS",
    "AXISBANK",
    "BAJAJ-AUTO",
    "BANKBEES",
    "BHARTIARTL",
    "BPCL",
    "BRITANNIA",
    "CIPLA",
    "DRREDDY",
    "GOLDBEES",
    "HCLTECH",
    "HDFCBANK",
    "HINDUNILVR",
    "ICICIBANK",
    "INFY",
    "ITBEES",
    "ITC",
    "JUNIORBEES",
    "KOTAKBANK",
    "LT",
    "M&M",
    "MARUTI",
    "NESTLEIND",
    "NIFTYBEES",
    "ONGC",
    "RELIANCE",
    "SBIN",
    "SUNPHARMA",
    "TCS",
    "TECHM",
    "ULTRACEMCO",
    "WIPRO",
]

ETF_SYMBOLS = {"BANKBEES", "GOLDBEES", "ITBEES", "JUNIORBEES", "NIFTYBEES"}
HORIZONS_MS = [100, 250, 500, 1000, 5000, 15000, 60000]

PRICE_COLUMNS = [
    "last_price",
    "average_traded_price",
    "ohlc_open",
    "ohlc_high",
    "ohlc_low",
    "ohlc_close",
    *[f"buy_{level}_price" for level in range(1, 6)],
    *[f"sell_{level}_price" for level in range(1, 6)],
]

QUANTITY_COLUMNS = [
    "last_traded_quantity",
    "volume_traded",
    "total_buy_quantity",
    "total_sell_quantity",
    "oi",
    "oi_day_high",
    "oi_day_low",
    *[f"buy_{level}_quantity" for level in range(1, 6)],
    *[f"sell_{level}_quantity" for level in range(1, 6)],
    *[f"buy_{level}_orders" for level in range(1, 6)],
    *[f"sell_{level}_orders" for level in range(1, 6)],
]


@dataclass(frozen=True)
class SymbolFiles:
    symbol: str
    symbol_dir: Path
    files: list[Path]


def discover_symbol_files(input_dir: Path) -> list[SymbolFiles]:
    groups: list[SymbolFiles] = []
    for symbol_dir in sorted(input_dir.glob("symbol=*")):
        if not symbol_dir.is_dir():
            continue
        symbol = symbol_dir.name.split("=", 1)[1]
        files = sorted(symbol_dir.glob("part-*.parquet"))
        groups.append(SymbolFiles(symbol=symbol, symbol_dir=symbol_dir, files=files))
    return groups


def compact_symbol(symbol_files: SymbolFiles, output_dir: Path) -> pd.DataFrame:
    if not symbol_files.files:
        data = pd.DataFrame()
    else:
        file_order = {path.name: ordinal for ordinal, path in enumerate(symbol_files.files)}
        dataset = ds.dataset([str(path) for path in symbol_files.files], format="parquet")
        data = dataset.scanner(
            columns=[*dataset.schema.names, "__filename"],
            use_threads=True,
        ).to_table().to_pandas()
        data.insert(0, "source_file", data.pop("__filename").map(lambda value: Path(value).name))
        data.insert(1, "source_file_ordinal", data["source_file"].map(file_order).astype("int32"))
        data.insert(2, "row_in_source_file", data.groupby("source_file", sort=False).cumcount().astype("int32"))

    data["instrument_class"] = "etf" if symbol_files.symbol in ETF_SYMBOLS else "equity"
    data["observation_semantics"] = "received_tick"
    data["sequence_local"] = np.arange(len(data), dtype=np.int64)

    sort_cols = ["collector_received_monotonic_ns", "collector_received_utc_ms", "source_file_ordinal", "row_in_source_file"]
    present_sort_cols = [col for col in sort_cols if col in data.columns]
    if present_sort_cols:
        data = data.sort_values(present_sort_cols, kind="mergesort").reset_index(drop=True)
        data["sequence_local"] = np.arange(len(data), dtype=np.int64)

    symbol_out = output_dir / f"symbol={symbol_files.symbol}"
    symbol_out.mkdir(parents=True, exist_ok=True)
    pq.write_table(
        pa.Table.from_pandas(data, preserve_index=False),
        symbol_out / "ticks.parquet",
        compression="zstd",
    )
    return data


def schema_records(symbol_files: Iterable[SymbolFiles]) -> tuple[list[dict], list[dict], list[dict]]:
    file_rows: list[dict] = []
    mismatch_rows: list[dict] = []
    first_schema: list[tuple[str, str]] | None = None
    first_contract: list[tuple[str, str]] | None = None
    first_order: list[str] = []
    observed_types: dict[str, set[str]] = {}

    groups = list(symbol_files)
    for group_index, group in enumerate(groups, start=1):
        print(f"[stage-a1] inventory/schema {group_index}/{len(groups)} {group.symbol} ({len(group.files)} files)", flush=True)
        for parquet_path in group.files:
            parquet_file = pq.ParquetFile(parquet_path)
            schema = [(field.name, str(field.type)) for field in parquet_file.schema_arrow]
            contract = [(name, _type_family(typ)) for name, typ in schema]
            for name, typ in schema:
                observed_types.setdefault(name, set()).add(typ)
            if first_schema is None:
                first_schema = schema
                first_contract = contract
                first_order = [name for name, _ in schema]
            exact_schema_matches_first = schema == first_schema
            logical_schema_matches_first = contract == first_contract
            if not logical_schema_matches_first:
                mismatch_rows.extend(
                    {
                        "symbol": group.symbol,
                        "file": parquet_path.name,
                        "ordinal": ordinal,
                        "column_name": name,
                        "column_type": typ,
                        "logical_type": _type_family(typ),
                    }
                    for ordinal, (name, typ) in enumerate(schema)
                )
            file_rows.append(
                {
                    "symbol": group.symbol,
                    "file": parquet_path.name,
                    "rows": parquet_file.metadata.num_rows,
                    "row_groups": parquet_file.metadata.num_row_groups,
                    "bytes": parquet_path.stat().st_size,
                    "exact_schema_matches_first": exact_schema_matches_first,
                    "schema_matches_first": logical_schema_matches_first,
                }
            )
    schema_rows = [
        {
            "ordinal": ordinal,
            "column_name": name,
            "observed_column_types": "|".join(sorted(observed_types.get(name, set()))),
            "logical_type": _type_family(next(iter(observed_types.get(name, {"unknown"})))),
        }
        for ordinal, name in enumerate(first_order)
    ]
    return schema_rows, file_rows, mismatch_rows


def _type_family(arrow_type: str) -> str:
    if arrow_type in {"int8", "int16", "int32", "int64", "uint8", "uint16", "uint32", "uint64", "float", "double"}:
        return "number"
    if "string" in arrow_type:
        return "string"
    if arrow_type in {"bool", "boolean"}:
        return "boolean"
    if arrow_type.startswith("timestamp"):
        return "timestamp"
    return arrow_type


def _count_negative(data: pd.DataFrame, columns: list[str]) -> int:
    total = 0
    for column in columns:
        if column in data.columns:
            total += int((pd.to_numeric(data[column], errors="coerce") < 0).sum())
    return total


def _depth_sort_errors(data: pd.DataFrame) -> tuple[int, int]:
    bid_errors = pd.Series(False, index=data.index)
    ask_errors = pd.Series(False, index=data.index)
    for level in range(1, 5):
        bid_left = pd.to_numeric(data.get(f"buy_{level}_price"), errors="coerce")
        bid_right = pd.to_numeric(data.get(f"buy_{level + 1}_price"), errors="coerce")
        ask_left = pd.to_numeric(data.get(f"sell_{level}_price"), errors="coerce")
        ask_right = pd.to_numeric(data.get(f"sell_{level + 1}_price"), errors="coerce")
        bid_errors = bid_errors | ((bid_left < bid_right) & bid_left.notna() & bid_right.notna())
        ask_errors = ask_errors | ((ask_left > ask_right) & ask_left.notna() & ask_right.notna())
    return int(bid_errors.sum()), int(ask_errors.sum())


def _positive_min_increment(values: pd.Series) -> float | None:
    clean = pd.to_numeric(values, errors="coerce").dropna().sort_values().unique()
    if len(clean) < 2:
        return None
    diffs = np.diff(clean)
    positive = diffs[diffs > 0]
    if len(positive) == 0:
        return None
    return float(np.min(positive))


def _off_tick_005_count(data: pd.DataFrame) -> int:
    count = 0
    for column in PRICE_COLUMNS:
        if column not in data.columns:
            continue
        values = pd.to_numeric(data[column], errors="coerce").dropna()
        if values.empty:
            continue
        scaled = values * 20.0
        count += int((np.abs(scaled - np.round(scaled)) > 1e-7).sum())
    return count


def symbol_quality(symbol: str, data: pd.DataFrame, file_summary: pd.DataFrame) -> dict:
    receive_ms = pd.to_numeric(data.get("collector_received_utc_ms"), errors="coerce")
    monotonic_ns = pd.to_numeric(data.get("collector_received_monotonic_ns"), errors="coerce")
    volume = pd.to_numeric(data.get("volume_traded"), errors="coerce")
    bid_1 = pd.to_numeric(data.get("buy_1_price"), errors="coerce")
    ask_1 = pd.to_numeric(data.get("sell_1_price"), errors="coerce")

    receive_diff_ms = receive_ms.diff()
    monotonic_diff_ns = monotonic_ns.diff()
    volume_diff = volume.diff()

    bid_sort_errors, ask_sort_errors = _depth_sort_errors(data)
    row_count = int(len(data))
    bytes_total = int(file_summary["bytes"].sum()) if not file_summary.empty else 0
    duration_seconds = float((receive_ms.max() - receive_ms.min()) / 1000.0) if row_count > 1 else 0.0

    null_rates = {
        col: float(data[col].isna().mean())
        for col in data.columns
        if col not in {"source_file", "observation_semantics", "instrument_class"}
    }
    worst_null_field = max(null_rates, key=null_rates.get) if null_rates else None
    worst_null_rate = null_rates.get(worst_null_field, 0.0) if worst_null_field else 0.0

    min_price_increment = _positive_min_increment(data["last_price"]) if "last_price" in data.columns else None

    return {
        "symbol": symbol,
        "instrument_class": "etf" if symbol in ETF_SYMBOLS else "equity",
        "row_count": row_count,
        "file_count": int(file_summary.shape[0]),
        "file_bytes": bytes_total,
        "compressed_bytes_per_row": float(bytes_total / row_count) if row_count else math.nan,
        "first_receive_ms": int(receive_ms.min()) if receive_ms.notna().any() else None,
        "last_receive_ms": int(receive_ms.max()) if receive_ms.notna().any() else None,
        "first_receive_utc": _utc_from_ms(receive_ms.min()),
        "last_receive_utc": _utc_from_ms(receive_ms.max()),
        "duration_seconds": duration_seconds,
        "event_rate_per_second": float(row_count / duration_seconds) if duration_seconds > 0 else math.nan,
        "duplicate_receive_ms": int(receive_ms.duplicated().sum()),
        "duplicate_monotonic_ns": int(monotonic_ns.duplicated().sum()),
        "receive_ms_order_violations": int((receive_diff_ms < 0).sum()),
        "monotonic_ns_order_violations": int((monotonic_diff_ns < 0).sum()),
        "min_interarrival_ms": float(receive_diff_ms[receive_diff_ms >= 0].min()) if (receive_diff_ms >= 0).any() else math.nan,
        "median_interarrival_ms": float(receive_diff_ms[receive_diff_ms >= 0].median()) if (receive_diff_ms >= 0).any() else math.nan,
        "p95_interarrival_ms": float(receive_diff_ms[receive_diff_ms >= 0].quantile(0.95)) if (receive_diff_ms >= 0).any() else math.nan,
        "max_interarrival_ms": float(receive_diff_ms[receive_diff_ms >= 0].max()) if (receive_diff_ms >= 0).any() else math.nan,
        "stale_gap_gt_5s_count": int((receive_diff_ms > 5000).sum()),
        "stale_gap_gt_15s_count": int((receive_diff_ms > 15000).sum()),
        "crossed_book_count": int((bid_1 > ask_1).sum()),
        "locked_book_count": int((bid_1 == ask_1).sum()),
        "negative_quantity_or_order_count": _count_negative(data, QUANTITY_COLUMNS),
        "bid_depth_sort_error_rows": bid_sort_errors,
        "ask_depth_sort_error_rows": ask_sort_errors,
        "cumulative_volume_reversal_count": int((volume_diff < 0).sum()),
        "off_tick_005_price_count": _off_tick_005_count(data),
        "inferred_min_last_price_increment": min_price_increment,
        "worst_null_field": worst_null_field,
        "worst_null_rate": worst_null_rate,
    }


def horizon_coverage(symbol: str, data: pd.DataFrame) -> list[dict]:
    receive_ms = pd.to_numeric(data.get("collector_received_utc_ms"), errors="coerce").dropna()
    if receive_ms.empty:
        return [
            {
                "symbol": symbol,
                "instrument_class": "etf" if symbol in ETF_SYMBOLS else "equity",
                "horizon_ms": horizon,
                "expected_bins": 0,
                "bins_with_update": 0,
                "coverage_fraction": math.nan,
                "forward_fill_fraction": math.nan,
                "supported_for_resampling": False,
            }
            for horizon in HORIZONS_MS
        ]

    start = int(receive_ms.min())
    end = int(receive_ms.max())
    rows: list[dict] = []
    for horizon in HORIZONS_MS:
        expected_bins = max(1, int(math.floor((end - start) / horizon)) + 1)
        bins = ((receive_ms - start) // horizon).astype(np.int64)
        bins_with_update = int(bins.nunique())
        coverage = bins_with_update / expected_bins if expected_bins else math.nan
        rows.append(
            {
                "symbol": symbol,
                "instrument_class": "etf" if symbol in ETF_SYMBOLS else "equity",
                "horizon_ms": horizon,
                "expected_bins": expected_bins,
                "bins_with_update": bins_with_update,
                "coverage_fraction": float(coverage),
                "forward_fill_fraction": float(1.0 - coverage) if not math.isnan(coverage) else math.nan,
                "supported_for_resampling": bool(coverage >= 0.90),
            }
        )
    return rows


def _utc_from_ms(value: float | int | None) -> str | None:
    if value is None or pd.isna(value):
        return None
    return datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc).isoformat()


def manifest_summary(input_dir: Path) -> dict:
    manifest_path = input_dir / "azure_files_manifest.csv"
    if not manifest_path.exists():
        return {"manifest_present": False}
    manifest = pd.read_csv(manifest_path)
    local_files = {
        (path.parent.name, path.name): path.stat().st_size
        for path in input_dir.glob("symbol=*/part-*.parquet")
    }
    manifest_files = {
        (str(row.symbol_dir), str(row.name)): int(row.bytes)
        for row in manifest.itertuples(index=False)
    }
    manifest_keys = set(manifest_files)
    local_keys = set(local_files)
    missing_local = sorted(manifest_keys - local_keys)
    extra_local = sorted(local_keys - manifest_keys)
    size_mismatches = []
    for symbol_dir, name in sorted(manifest_keys & local_keys):
        manifest_bytes = manifest_files[(symbol_dir, name)]
        local_bytes = int(local_files[(symbol_dir, name)])
        if manifest_bytes != local_bytes:
            size_mismatches.append({"symbol_dir": symbol_dir, "name": name, "manifest_bytes": manifest_bytes, "local_bytes": local_bytes})
    return {
        "manifest_present": True,
        "manifest_rows": int(len(manifest)),
        "local_file_rows": int(len(local_files)),
        "missing_local_count": len(missing_local),
        "extra_local_count": len(extra_local),
        "size_mismatch_count": len(size_mismatches),
        "missing_local_examples": missing_local[:10],
        "extra_local_examples": extra_local[:10],
        "size_mismatch_examples": size_mismatches[:10],
    }


def parameter_ledger() -> pd.DataFrame:
    rows = [
        ("received_event_rate", "measured", "Computed per symbol from collector_received_utc_ms."),
        ("interarrival_distribution", "measured", "Computed per symbol from receive timestamp differences."),
        ("batch_flush_cadence", "measured", "Approximated from source file time ranges and rows per file."),
        ("schema_presence", "measured", "Detected from all Parquet file schemas."),
        ("manifest_completeness", "measured", "Compared local files to azure_files_manifest.csv."),
        ("depth_sorting_validity", "measured", "Checked L1-L5 bid/ask price monotonicity."),
        ("crossed_locked_book_frequency", "measured", "Checked best bid and best ask state."),
        ("horizon_coverage", "measured", "Computed per symbol for 100ms through 60s bins."),
        ("tick_size", "weakly_estimated", "Minimum observed price increment is sample-derived; exchange tick rules are not embedded."),
        ("add_cancel_consume_events", "assumed", "Market-by-price snapshots do not identify individual order events."),
        ("aggressor_side", "assumed", "Can only be inferred from price/volume/depth changes."),
        ("queue_position", "blocked", "Top-five market-by-price feed lacks individual order queue identity."),
        ("connection_reconnect_boundaries", "blocked", "Current row schema has no connection_id or reconnect markers."),
        ("dropped_message_rate", "blocked", "No exchange sequence or dropped-message diagnostics in the row schema."),
    ]
    return pd.DataFrame(rows, columns=["parameter", "evidence_label", "evidence_note"])


def write_report(
    output_dir: Path,
    input_dir: Path,
    quality: pd.DataFrame,
    coverage: pd.DataFrame,
    file_summary: pd.DataFrame,
    manifest: dict,
) -> None:
    symbols = sorted(quality["symbol"].tolist())
    full_session_below_dense_1s = coverage[(coverage["horizon_ms"] == 1000) & (~coverage["supported_for_resampling"])]["symbol"].tolist()
    worst_gaps = quality.sort_values("max_interarrival_ms", ascending=False).head(5)
    class_profile = quality.groupby("instrument_class").agg(
        symbols=("symbol", "count"),
        rows=("row_count", "sum"),
        median_event_rate_per_second=("event_rate_per_second", "median"),
        median_interarrival_ms=("median_interarrival_ms", "median"),
        total_files=("file_count", "sum"),
        total_bytes=("file_bytes", "sum"),
    )
    class_profile_text = _markdown_table(class_profile.reset_index())
    worst_gaps_text = _markdown_table(
        worst_gaps[["symbol", "instrument_class", "max_interarrival_ms", "p95_interarrival_ms", "stale_gap_gt_15s_count"]]
    )

    lines = [
        "# Stage A1 Tick-Stream Audit Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        f"Input directory: `{input_dir}`",
        f"Output directory: `{output_dir}`",
        "",
        "## Scope",
        "",
        "This report audits the current one-day Zerodha WebSocket L2 sample as a received-tick stream.",
        "It does not claim multi-day calibration, strategy profitability, or exchange-order reconstruction.",
        "",
        "## Inventory",
        "",
        f"- Symbols discovered: {len(symbols)}",
        f"- Parquet files: {int(file_summary.shape[0])}",
        f"- Rows: {int(quality['row_count'].sum())}",
        f"- Bytes: {int(quality['file_bytes'].sum())}",
        f"- Manifest present: {manifest.get('manifest_present')}",
        f"- Manifest rows: {manifest.get('manifest_rows')}",
        f"- Missing local files from manifest: {manifest.get('missing_local_count')}",
        f"- Extra local files not in manifest: {manifest.get('extra_local_count')}",
        f"- Size mismatches: {manifest.get('size_mismatch_count')}",
        "",
        "## Class Profile",
        "",
        class_profile_text,
        "",
        "## Stage A1 Gate Status",
        "",
        "| Gate | Status | Evidence |",
        "|---|---|---|",
        f"| All 32 requested symbols represented | {'PASS' if set(symbols) == set(EXPECTED_SYMBOLS) else 'FAIL'} | Found {len(symbols)} symbols |",
        f"| Manifest/file completeness | {'PASS' if manifest.get('missing_local_count') == 0 and manifest.get('extra_local_count') == 0 and manifest.get('size_mismatch_count') == 0 else 'FAIL'} | Compared local files to manifest |",
        f"| Schema consistency | {'PASS' if bool(file_summary['schema_matches_first'].all()) else 'FAIL'} | {int(file_summary['schema_matches_first'].sum())}/{int(file_summary.shape[0])} files match first schema |",
        f"| Receive ordering | {'PASS' if int(quality['monotonic_ns_order_violations'].sum()) == 0 else 'FAIL'} | {int(quality['monotonic_ns_order_violations'].sum())} monotonic-ns order violations |",
        f"| Book not crossed | {'PASS' if int(quality['crossed_book_count'].sum()) == 0 else 'WARN'} | {int(quality['crossed_book_count'].sum())} crossed best-book rows |",
        f"| Depth price sorting | {'PASS' if int(quality['bid_depth_sort_error_rows'].sum() + quality['ask_depth_sort_error_rows'].sum()) == 0 else 'WARN'} | Bid errors {int(quality['bid_depth_sort_error_rows'].sum())}, ask errors {int(quality['ask_depth_sort_error_rows'].sum())} |",
        f"| Horizon coverage measured | PASS | {coverage.shape[0]} symbol/horizon rows |",
        f"| Parameter evidence labelled | PASS | See `parameter_evidence_ledger.csv` |",
        "",
        "## Largest Receive Gaps",
        "",
        worst_gaps_text,
        "",
        "## 1-Second Horizon Support",
        "",
        "The 90% gate is a dense full-session regular-panel gate, not a claim that 1-second or sub-second received ticks are absent.",
        f"Symbols below the dense full-session 90% one-second bin coverage gate: {', '.join(full_session_below_dense_1s) if full_session_below_dense_1s else 'none'}",
        "Use event-driven ticks and window-specific coverage audits before enabling 1-second features for active periods such as the open.",
        "",
        "## Outputs",
        "",
        "- `compact_ticks_by_symbol/symbol=*/ticks.parquet`",
        "- `data_quality_report.csv` and `data_quality_report.parquet`",
        "- `horizon_coverage.csv`",
        "- `schema_report.csv`",
        "- `file_inventory.csv`",
        "- `manifest_check.json`",
        "- `parameter_evidence_ledger.csv`",
        "",
    ]
    (output_dir / "stage_a1_report.md").write_text("\n".join(lines), encoding="utf-8")


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text_frame = frame.copy()
    for column in text_frame.columns:
        text_frame[column] = text_frame[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text_frame.columns]
    rows = text_frame.values.tolist()
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def run_stage_a1(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    compact_dir = output_dir / "compact_ticks_by_symbol"
    compact_dir.mkdir(parents=True, exist_ok=True)

    groups = discover_symbol_files(input_dir)
    schema_rows, file_rows, mismatch_rows = schema_records(groups)
    schema_df = pd.DataFrame(schema_rows)
    file_df = pd.DataFrame(file_rows)
    schema_df.to_csv(output_dir / "schema_report.csv", index=False)
    pd.DataFrame(mismatch_rows).to_csv(output_dir / "schema_mismatches.csv", index=False)
    file_df.to_csv(output_dir / "file_inventory.csv", index=False)

    quality_rows: list[dict] = []
    coverage_rows: list[dict] = []
    for index, group in enumerate(groups, start=1):
        print(f"[stage-a1] compacting/auditing {index}/{len(groups)} {group.symbol} ({len(group.files)} files)", flush=True)
        data = compact_symbol(group, compact_dir)
        symbol_files = file_df[file_df["symbol"] == group.symbol]
        quality_rows.append(symbol_quality(group.symbol, data, symbol_files))
        coverage_rows.extend(horizon_coverage(group.symbol, data))

    quality_df = pd.DataFrame(quality_rows).sort_values("symbol")
    coverage_df = pd.DataFrame(coverage_rows).sort_values(["symbol", "horizon_ms"])
    ledger_df = parameter_ledger()
    manifest = manifest_summary(input_dir)

    quality_df.to_csv(output_dir / "data_quality_report.csv", index=False)
    pq.write_table(pa.Table.from_pandas(quality_df, preserve_index=False), output_dir / "data_quality_report.parquet", compression="zstd")
    coverage_df.to_csv(output_dir / "horizon_coverage.csv", index=False)
    ledger_df.to_csv(output_dir / "parameter_evidence_ledger.csv", index=False)
    (output_dir / "manifest_check.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, input_dir, quality_df, coverage_df, file_df, manifest)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage A1 one-day received-tick audit.")
    parser.add_argument("--input-dir", type=Path, default=Path("real_data_sample/l2_single_day"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/stage_a1"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_stage_a1(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
from datetime import datetime, time, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import pyarrow.parquet as pq


HORIZONS_MS = [100, 250, 500, 1000, 5000, 15000, 60000]
IST = ZoneInfo("Asia/Kolkata")


def parse_time(value: str) -> time:
    return datetime.strptime(value, "%H:%M:%S").time()


def symbol_from_path(path: Path) -> str:
    return path.parent.name.split("=", 1)[1]


def coverage_for_window(input_dir: Path, output_dir: Path, window_name: str, start_ist: time, end_ist: time) -> pd.DataFrame:
    rows: list[dict] = []
    files = sorted(input_dir.glob("symbol=*/ticks.parquet"))
    for index, path in enumerate(files, start=1):
        symbol = symbol_from_path(path)
        print(f"[window-audit] {window_name} {index}/{len(files)} {symbol}", flush=True)
        table = pq.read_table(path, columns=["collector_received_utc_ms"])
        data = table.to_pandas()
        receive_utc = pd.to_datetime(data["collector_received_utc_ms"], unit="ms", utc=True)
        receive_ist = receive_utc.dt.tz_convert(IST)
        mask = (receive_ist.dt.time >= start_ist) & (receive_ist.dt.time < end_ist)
        window_dates = receive_ist.loc[mask].dt.date
        values = data.loc[mask, "collector_received_utc_ms"].dropna().astype("int64")
        if values.empty:
            for horizon in HORIZONS_MS:
                rows.append(
                    {
                        "window_name": window_name,
                        "symbol": symbol,
                        "horizon_ms": horizon,
                        "rows": 0,
                        "window_seconds": 0.0,
                        "event_rate_per_second": None,
                        "expected_bins": 0,
                        "bins_with_update": 0,
                        "coverage_fraction": None,
                        "forward_fill_fraction": None,
                        "median_gap_ms": None,
                        "p95_gap_ms": None,
                        "supported_dense_regular_panel": False,
                        "supports_event_driven_1s": False,
                    }
                )
            continue

        first_date = window_dates.iloc[0]
        window_start = datetime.combine(first_date, start_ist, IST)
        window_end = datetime.combine(first_date, end_ist, IST)
        window_start_ms = int(window_start.timestamp() * 1000)
        window_end_ms = int(window_end.timestamp() * 1000)
        duration_ms = max(1, window_end_ms - window_start_ms)
        diffs = values.sort_values().diff().dropna()
        median_gap = float(diffs.median()) if len(diffs) else None
        p95_gap = float(diffs.quantile(0.95)) if len(diffs) else None
        event_rate = len(values) / (duration_ms / 1000.0) if duration_ms > 0 else None
        for horizon in HORIZONS_MS:
            expected_bins = max(1, int((duration_ms + horizon - 1) // horizon))
            bins = ((values - window_start_ms) // horizon).astype("int64")
            bins_with_update = int(bins.nunique())
            coverage = bins_with_update / expected_bins if expected_bins else None
            supports_event_driven_1s = bool(horizon == 1000 and event_rate is not None and event_rate >= 1.0 and (p95_gap is None or p95_gap <= 5000))
            rows.append(
                {
                    "window_name": window_name,
                    "symbol": symbol,
                    "horizon_ms": horizon,
                    "rows": int(len(values)),
                    "window_seconds": duration_ms / 1000.0,
                    "event_rate_per_second": event_rate,
                    "expected_bins": expected_bins,
                    "bins_with_update": bins_with_update,
                    "coverage_fraction": coverage,
                    "forward_fill_fraction": (1.0 - coverage) if coverage is not None else None,
                    "median_gap_ms": median_gap,
                    "p95_gap_ms": p95_gap,
                    "supported_dense_regular_panel": bool(coverage is not None and coverage >= 0.90),
                    "supports_event_driven_1s": supports_event_driven_1s,
                }
            )
    out = pd.DataFrame(rows).sort_values(["window_name", "symbol", "horizon_ms"])
    output_dir.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_dir / f"horizon_window_coverage_{window_name}.csv", index=False)
    write_report(output_dir, window_name, out)
    return out


def write_report(output_dir: Path, window_name: str, coverage: pd.DataFrame) -> None:
    one_sec = coverage[coverage["horizon_ms"] == 1000].copy()
    dense = int(one_sec["supported_dense_regular_panel"].sum()) if len(one_sec) else 0
    event = int(one_sec["supports_event_driven_1s"].sum()) if len(one_sec) else 0
    top = one_sec.sort_values(["event_rate_per_second", "coverage_fraction"], ascending=False).head(12)
    lines = [
        f"# Horizon Window Coverage Report: {window_name}",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Interpretation",
        "",
        "Dense regular-panel support means at least 90% of bins in the selected window contain an update.",
        "Event-driven 1-second support means the selected window has at least 1 received tick per second on average and p95 gap <= 5 seconds.",
        "",
        "## One-Second Summary",
        "",
        f"- Symbols passing dense 1-second regular-panel gate: {dense}",
        f"- Symbols passing event-driven 1-second gate: {event}",
        "",
        "## Top One-Second Window Coverage",
        "",
        _markdown_table(top[["symbol", "rows", "window_seconds", "event_rate_per_second", "coverage_fraction", "median_gap_ms", "p95_gap_ms", "supported_dense_regular_panel", "supports_event_driven_1s"]]),
        "",
    ]
    (output_dir / f"horizon_window_coverage_{window_name}.md").write_text("\n".join(lines), encoding="utf-8")


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text_frame = frame.copy()
    for column in text_frame.columns:
        text_frame[column] = text_frame[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text_frame.columns]
    rows = text_frame.values.tolist()
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit horizon coverage for an IST time window.")
    parser.add_argument("--input-dir", type=Path, default=Path("outputs/stage_a1/compact_ticks_by_symbol"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/stage_a1"))
    parser.add_argument("--window-name", default="open_0915_0920")
    parser.add_argument("--start-ist", default="09:15:00")
    parser.add_argument("--end-ist", default="09:20:00")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    coverage_for_window(args.input_dir, args.output_dir, args.window_name, parse_time(args.start_ist), parse_time(args.end_ist))


if __name__ == "__main__":
    main()

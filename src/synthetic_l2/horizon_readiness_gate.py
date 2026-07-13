from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


DENSE_COVERAGE_THRESHOLD = 0.90
EVENT_DRIVEN_1S_MIN_RATE = 1.0
EVENT_DRIVEN_1S_MAX_P95_GAP_MS = 5000.0


def load_inputs(full_session_path: Path, open_window_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    full = pd.read_csv(full_session_path)
    window = pd.read_csv(open_window_path)
    return full, window


def full_session_decisions(full: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for horizon, group in full.groupby("horizon_ms", sort=True):
        dense_symbols = group[group["coverage_fraction"] >= DENSE_COVERAGE_THRESHOLD]["symbol"].tolist()
        rows.append(
            {
                "scope": "full_session",
                "window_name": "full_session",
                "horizon_ms": int(horizon),
                "symbols_evaluated": int(group["symbol"].nunique()),
                "dense_regular_panel_symbols": int(len(dense_symbols)),
                "event_driven_symbols": None,
                "median_coverage_fraction": float(group["coverage_fraction"].median()),
                "min_coverage_fraction": float(group["coverage_fraction"].min()),
                "median_forward_fill_fraction": float(group["forward_fill_fraction"].median()),
                "max_forward_fill_fraction": float(group["forward_fill_fraction"].max()),
                "readiness_status": "dense_regular_panel_supported" if len(dense_symbols) == group["symbol"].nunique() else "event_driven_or_sparse_only",
                "usable_for_dense_regular_panel": bool(len(dense_symbols) == group["symbol"].nunique()),
                "usable_for_event_driven_features": bool(horizon >= 1000),
                "caveat": (
                    "All symbols pass the 90% dense regular-panel gate."
                    if len(dense_symbols) == group["symbol"].nunique()
                    else "Do not treat this horizon as a complete dense panel across all symbols; use event-time logic or explicit forward-fill/staleness controls."
                ),
            }
        )
    return pd.DataFrame(rows)


def open_window_decisions(window: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for horizon, group in window.groupby("horizon_ms", sort=True):
        dense_symbols = group[group["coverage_fraction"] >= DENSE_COVERAGE_THRESHOLD]["symbol"].tolist()
        event_symbols = []
        if horizon == 1000:
            event_symbols = group[
                (group["event_rate_per_second"] >= EVENT_DRIVEN_1S_MIN_RATE)
                & (group["p95_gap_ms"] <= EVENT_DRIVEN_1S_MAX_P95_GAP_MS)
            ]["symbol"].tolist()
        rows.append(
            {
                "scope": "open_window",
                "window_name": str(group["window_name"].iloc[0]) if len(group) else "open_window",
                "horizon_ms": int(horizon),
                "symbols_evaluated": int(group["symbol"].nunique()),
                "dense_regular_panel_symbols": int(len(dense_symbols)),
                "event_driven_symbols": int(len(event_symbols)) if horizon == 1000 else None,
                "median_coverage_fraction": float(group["coverage_fraction"].median()),
                "min_coverage_fraction": float(group["coverage_fraction"].min()),
                "median_forward_fill_fraction": float(group["forward_fill_fraction"].median()),
                "max_forward_fill_fraction": float(group["forward_fill_fraction"].max()),
                "median_event_rate_per_second": float(group["event_rate_per_second"].median()),
                "median_p95_gap_ms": float(group["p95_gap_ms"].median()),
                "readiness_status": _open_window_status(horizon, len(dense_symbols), len(event_symbols), int(group["symbol"].nunique())),
                "usable_for_dense_regular_panel": bool(len(dense_symbols) == group["symbol"].nunique()),
                "usable_for_event_driven_features": bool(horizon == 1000 and len(event_symbols) > 0),
                "caveat": _open_window_caveat(horizon, len(dense_symbols), len(event_symbols), int(group["symbol"].nunique())),
            }
        )
    return pd.DataFrame(rows)


def _open_window_status(horizon: int, dense_count: int, event_count: int, symbols: int) -> str:
    if dense_count == symbols:
        return "dense_regular_panel_supported"
    if horizon == 1000 and event_count > 0:
        return "event_driven_1s_supported_for_active_symbols"
    if horizon < 1000:
        return "unsupported_sparse_subsecond"
    return "sparse_or_forward_fill_only"


def _open_window_caveat(horizon: int, dense_count: int, event_count: int, symbols: int) -> str:
    if dense_count == symbols:
        return "All symbols pass the 90% dense regular-panel gate in this window."
    if horizon == 1000 and event_count > 0:
        return f"{event_count}/{symbols} symbols pass the event-driven 1-second gate; dense 1-second panels still require explicit forward-fill/staleness controls."
    if horizon < 1000:
        return "Sub-second horizons are sparse in the current retail received-feed sample; do not use as dense panels."
    return "Use only with explicit coverage, staleness and forward-fill labels."


def symbol_decisions(window: pd.DataFrame) -> pd.DataFrame:
    one_second = window[window["horizon_ms"] == 1000].copy()
    one_second["event_driven_1s_ready"] = (
        (one_second["event_rate_per_second"] >= EVENT_DRIVEN_1S_MIN_RATE)
        & (one_second["p95_gap_ms"] <= EVENT_DRIVEN_1S_MAX_P95_GAP_MS)
    )
    one_second["dense_1s_ready"] = one_second["coverage_fraction"] >= DENSE_COVERAGE_THRESHOLD
    one_second["readiness_status"] = one_second.apply(
        lambda row: "dense_1s_ready"
        if row["dense_1s_ready"]
        else ("event_driven_1s_ready" if row["event_driven_1s_ready"] else "not_1s_ready"),
        axis=1,
    )
    return one_second[
        [
            "window_name",
            "symbol",
            "rows",
            "window_seconds",
            "event_rate_per_second",
            "coverage_fraction",
            "forward_fill_fraction",
            "median_gap_ms",
            "p95_gap_ms",
            "dense_1s_ready",
            "event_driven_1s_ready",
            "readiness_status",
        ]
    ].sort_values(["readiness_status", "event_rate_per_second", "coverage_fraction"], ascending=[True, False, False])


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else (f"{value:.6g}" if isinstance(value, float) else str(value)))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def write_report(output_dir: Path, horizon_decisions: pd.DataFrame, one_second_symbols: pd.DataFrame, manifest: dict) -> None:
    lines = [
        "# Horizon Readiness Gate Report",
        "",
        f"Generated UTC: {manifest['generated_utc']}",
        "",
        "## Interpretation",
        "",
        "This gate converts observed Zerodha received-feed coverage into explicit horizon-readiness decisions.",
        "It separates dense regular-panel support from event-driven feature support so sparse 100 ms, 250 ms, 500 ms and 1-second panels are not accidentally treated as complete data.",
        "",
        "## Horizon Decisions",
        "",
        _markdown_table(horizon_decisions),
        "",
        "## Open-Window One-Second Symbol Decisions",
        "",
        _markdown_table(one_second_symbols),
        "",
        "## Key Caveat",
        "",
        "The current one-day retail WebSocket sample can support event-driven 1-second work for active symbols/windows, but not dense full-session 1-second panels across the full universe.",
        "",
    ]
    (output_dir / "horizon_readiness_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_gate(full_session_path: Path, open_window_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    full, window = load_inputs(full_session_path, open_window_path)
    full_decisions = full_session_decisions(full)
    open_decisions = open_window_decisions(window)
    horizon_decisions = pd.concat([full_decisions, open_decisions], ignore_index=True, sort=False)
    one_second_symbols = symbol_decisions(window)
    horizon_decisions.to_csv(output_dir / "horizon_readiness_summary.csv", index=False)
    one_second_symbols.to_csv(output_dir / "one_second_symbol_readiness.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "full_session_path": str(full_session_path),
        "open_window_path": str(open_window_path),
        "dense_coverage_threshold": DENSE_COVERAGE_THRESHOLD,
        "event_driven_1s_min_rate": EVENT_DRIVEN_1S_MIN_RATE,
        "event_driven_1s_max_p95_gap_ms": EVENT_DRIVEN_1S_MAX_P95_GAP_MS,
        "horizon_rows": int(len(horizon_decisions)),
        "one_second_symbol_rows": int(len(one_second_symbols)),
        "event_driven_1s_symbols_open_window": int(one_second_symbols["event_driven_1s_ready"].sum()),
        "dense_1s_symbols_open_window": int(one_second_symbols["dense_1s_ready"].sum()),
        "scope": "received_feed_horizon_readiness_gate",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="horizon_readiness",
            generated_utc=generated_utc,
            inputs={"full_session_path": str(full_session_path), "open_window_path": str(open_window_path)},
            parameters={
                "dense_coverage_threshold": DENSE_COVERAGE_THRESHOLD,
                "event_driven_1s_min_rate": EVENT_DRIVEN_1S_MIN_RATE,
                "event_driven_1s_max_p95_gap_ms": EVENT_DRIVEN_1S_MAX_P95_GAP_MS,
            },
            outputs={
                "horizon_readiness_summary": str(output_dir / "horizon_readiness_summary.csv"),
                "one_second_symbol_readiness": str(output_dir / "one_second_symbol_readiness.csv"),
                "report": str(output_dir / "horizon_readiness_report.md"),
                "manifest": str(output_dir / "horizon_readiness_manifest.json"),
            },
            random_seed="not_applicable_deterministic_coverage_gate",
            scenario_ids="not_applicable_received_real_sample",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="not_applicable_no_latency_model",
        )
    )
    (output_dir / "horizon_readiness_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, horizon_decisions, one_second_symbols, manifest)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create horizon-readiness decisions from received-feed coverage evidence.")
    parser.add_argument("--full-session", type=Path, default=Path("outputs/stage_a1/horizon_coverage.csv"))
    parser.add_argument("--open-window", type=Path, default=Path("outputs/stage_a1/horizon_window_coverage_open_0915_0920.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/horizon_readiness"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_gate(args.full_session, args.open_window, args.output_dir)


if __name__ == "__main__":
    main()

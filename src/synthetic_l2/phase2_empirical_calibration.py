from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields
import pyarrow.parquet as pq


ETF_SYMBOLS = {"BANKBEES", "GOLDBEES", "ITBEES", "JUNIORBEES", "NIFTYBEES"}
QUANTILES = [0.05, 0.25, 0.50, 0.75, 0.95]


def _q(series: pd.Series, quantile: float) -> float:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    return float(clean.quantile(quantile)) if len(clean) else np.nan


def _mean(series: pd.Series) -> float:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    return float(clean.mean()) if len(clean) else np.nan


def _std(series: pd.Series) -> float:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    return float(clean.std()) if len(clean) else np.nan


def _sum(series: pd.Series) -> float:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    return float(clean.sum()) if len(clean) else 0.0


def _symbol_from_path(path: Path) -> str:
    return path.parent.name.split("=", 1)[1]


def _instrument_class(symbol: str) -> str:
    return "etf" if symbol in ETF_SYMBOLS else "equity"


def _read_symbol_tables(normalized_dir: Path, delta_dir: Path) -> list[tuple[str, pd.DataFrame, pd.DataFrame]]:
    pairs: list[tuple[str, pd.DataFrame, pd.DataFrame]] = []
    normalized_files = sorted(normalized_dir.glob("symbol=*/normalized_ticks.parquet"))
    for normalized_path in normalized_files:
        symbol = _symbol_from_path(normalized_path)
        delta_path = delta_dir / f"symbol={symbol}" / "received_tick_deltas.parquet"
        if not delta_path.exists():
            raise FileNotFoundError(f"Missing delta file for {symbol}: {delta_path}")
        normalized = pq.ParquetFile(normalized_path).read().to_pandas()
        deltas = pq.ParquetFile(delta_path).read().to_pandas()
        pairs.append((symbol, normalized, deltas))
    return pairs


def calibrate_symbol(symbol: str, normalized: pd.DataFrame, deltas: pd.DataFrame) -> tuple[dict, dict, dict, dict]:
    positive_volume = deltas.loc[pd.to_numeric(deltas["cum_volume_increment"], errors="coerce") > 0, "cum_volume_increment"]
    duration_seconds = (
        (pd.to_numeric(normalized["event_ts_receive_ms"], errors="coerce").max() - pd.to_numeric(normalized["event_ts_receive_ms"], errors="coerce").min())
        / 1000.0
        if len(normalized) > 1
        else np.nan
    )
    row_count = int(len(normalized))

    price = {
        "symbol": symbol,
        "instrument_class": _instrument_class(symbol),
        "rows": row_count,
        "reference_ltp_median": _q(normalized["ltp"], 0.50),
        "ltp_q05": _q(normalized["ltp"], 0.05),
        "ltp_q95": _q(normalized["ltp"], 0.95),
        "inferred_tick_size_median": _q(normalized["inferred_tick_size"], 0.50),
        "spread_median": _q(normalized["spread"], 0.50),
        "spread_q95": _q(normalized["spread"], 0.95),
        "spread_ticks_median": _q(normalized["spread_ticks"], 0.50),
        "spread_ticks_q95": _q(normalized["spread_ticks"], 0.95),
        "mid_change_std": _std(deltas["mid_change"]),
        "microprice_change_std": _std(deltas["microprice_change"]),
        "nonzero_price_change_fraction": float((pd.to_numeric(deltas["price_change"], errors="coerce").fillna(0) != 0).mean()) if row_count else np.nan,
        "evidence_label": "measured_one_day",
    }

    activity = {
        "symbol": symbol,
        "instrument_class": _instrument_class(symbol),
        "rows": row_count,
        "duration_seconds": float(duration_seconds) if not pd.isna(duration_seconds) else np.nan,
        "event_rate_per_second": float(row_count / duration_seconds) if duration_seconds and duration_seconds > 0 else np.nan,
        "elapsed_ms_q05": _q(deltas["elapsed_ms"], 0.05),
        "elapsed_ms_q25": _q(deltas["elapsed_ms"], 0.25),
        "elapsed_ms_median": _q(deltas["elapsed_ms"], 0.50),
        "elapsed_ms_q75": _q(deltas["elapsed_ms"], 0.75),
        "elapsed_ms_q95": _q(deltas["elapsed_ms"], 0.95),
        "stale_gap_gt_5s_count": int(deltas["stale_gap_gt_5s"].sum()),
        "stale_gap_gt_15s_count": int(deltas["stale_gap_gt_15s"].sum()),
        "volume_increment_rows": int((pd.to_numeric(deltas["cum_volume_increment"], errors="coerce") > 0).sum()),
        "evidence_label": "measured_one_day",
    }

    bid_l5 = sum(pd.to_numeric(normalized[f"bid_qty_{level}"], errors="coerce") for level in range(1, 6))
    ask_l5 = sum(pd.to_numeric(normalized[f"ask_qty_{level}"], errors="coerce") for level in range(1, 6))
    depth = {
        "symbol": symbol,
        "instrument_class": _instrument_class(symbol),
        "book_valid_fraction": float(normalized["book_valid"].mean()) if row_count else np.nan,
        "bid_l5_qty_median": _q(bid_l5, 0.50),
        "ask_l5_qty_median": _q(ask_l5, 0.50),
        "bid_l5_qty_q95": _q(bid_l5, 0.95),
        "ask_l5_qty_q95": _q(ask_l5, 0.95),
        "l1_imbalance_median": _q(deltas["l1_imbalance"], 0.50),
        "l1_imbalance_q05": _q(deltas["l1_imbalance"], 0.05),
        "l1_imbalance_q95": _q(deltas["l1_imbalance"], 0.95),
        "l5_imbalance_median": _q(deltas["l5_imbalance"], 0.50),
        "l5_imbalance_q05": _q(deltas["l5_imbalance"], 0.05),
        "l5_imbalance_q95": _q(deltas["l5_imbalance"], 0.95),
        "book_slope_l5_median": _q(deltas["book_slope_l5"], 0.50),
        "book_convexity_l5_median": _q(deltas["book_convexity_l5"], 0.50),
        "mlofi_qty_q05": _q(deltas["mlofi_qty"], 0.05),
        "mlofi_qty_median": _q(deltas["mlofi_qty"], 0.50),
        "mlofi_qty_q95": _q(deltas["mlofi_qty"], 0.95),
        "evidence_label": "measured_one_day",
    }

    trade_flow = {
        "symbol": symbol,
        "instrument_class": _instrument_class(symbol),
        "cum_volume_increment_total": _sum(deltas["cum_volume_increment"]),
        "positive_volume_increment_rows": int(len(positive_volume)),
        "positive_volume_increment_median": _q(positive_volume, 0.50),
        "positive_volume_increment_q95": _q(positive_volume, 0.95),
        "buy_pressure_weak_rows": int((deltas["aggressor_side_inference"] == "buy_pressure_weak").sum()),
        "sell_pressure_weak_rows": int((deltas["aggressor_side_inference"] == "sell_pressure_weak").sum()),
        "unknown_aggressor_rows": int((deltas["aggressor_side_inference"] == "unknown").sum()),
        "inferred_withdrawal_rows": int(deltas["inferred_depth_withdrawal"].sum()),
        "inferred_replenishment_rows": int(deltas["inferred_depth_replenishment"].sum()),
        "volume_reversal_rows": int(deltas["volume_reversal_flag"].sum()),
        "evidence_label": "weakly_inferred_one_day",
    }
    return price, activity, depth, trade_flow


def build_five_second_panel(symbol_tables: list[tuple[str, pd.DataFrame, pd.DataFrame]]) -> pd.DataFrame:
    series: list[pd.Series] = []
    for symbol, normalized, _ in symbol_tables:
        frame = normalized[["event_ts_receive_ms", "mid_price"]].copy()
        frame["bin_5s"] = (pd.to_numeric(frame["event_ts_receive_ms"], errors="coerce") // 5000).astype("int64")
        binned = frame.groupby("bin_5s", sort=True)["mid_price"].last().rename(symbol)
        series.append(binned)
    if not series:
        return pd.DataFrame()
    panel = pd.concat(series, axis=1).sort_index().ffill(limit=3)
    return panel.pct_change(fill_method=None).replace([np.inf, -np.inf], np.nan)


def cross_section_outputs(price: pd.DataFrame, activity: pd.DataFrame, depth: pd.DataFrame, trade_flow: pd.DataFrame, returns_5s: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    merged = price.merge(activity, on=["symbol", "instrument_class"], suffixes=("", "_activity"))
    merged = merged.merge(depth, on=["symbol", "instrument_class"], suffixes=("", "_depth"))
    merged = merged.merge(trade_flow, on=["symbol", "instrument_class"], suffixes=("", "_trade"))
    class_summary = merged.groupby("instrument_class").agg(
        symbols=("symbol", "count"),
        rows=("rows", "sum"),
        median_event_rate_per_second=("event_rate_per_second", "median"),
        median_spread_ticks=("spread_ticks_median", "median"),
        median_book_valid_fraction=("book_valid_fraction", "median"),
        median_l5_imbalance=("l5_imbalance_median", "median"),
        total_volume_increment=("cum_volume_increment_total", "sum"),
    ).reset_index()

    if returns_5s.empty:
        corr_summary = pd.DataFrame(columns=["metric", "value", "evidence_label"])
    else:
        corr = returns_5s.corr(min_periods=50)
        values = corr.where(~np.eye(corr.shape[0], dtype=bool)).stack().dropna()
        corr_summary = pd.DataFrame(
            [
                {"metric": "five_second_pairwise_corr_count", "value": float(len(values)), "evidence_label": "weak_one_day"},
                {"metric": "five_second_pairwise_corr_median", "value": float(values.median()) if len(values) else np.nan, "evidence_label": "weak_one_day"},
                {"metric": "five_second_pairwise_corr_q05", "value": float(values.quantile(0.05)) if len(values) else np.nan, "evidence_label": "weak_one_day"},
                {"metric": "five_second_pairwise_corr_q95", "value": float(values.quantile(0.95)) if len(values) else np.nan, "evidence_label": "weak_one_day"},
            ]
        )
    return class_summary, corr_summary


def parameter_evidence_ledger() -> pd.DataFrame:
    rows = [
        ("reference_price", "measured_one_day", "Median LTP from normalized received ticks."),
        ("spread_distribution", "measured_one_day", "Distribution of best ask minus best bid."),
        ("inferred_tick_size", "weakly_estimated_one_day", "Minimum observed LTP increment; not an exchange rule lookup."),
        ("event_rate", "measured_one_day", "Rows per receive-duration by symbol."),
        ("interarrival_distribution", "measured_one_day", "Elapsed receive milliseconds from consecutive received ticks."),
        ("stale_gap_profile", "measured_one_day", "Counts of receive gaps above 5s and 15s."),
        ("depth_quantity_distribution", "measured_one_day", "L1-L5 visible market-by-price quantities."),
        ("l1_l5_imbalance", "measured_one_day", "Computed from visible bid/ask depth."),
        ("mlofi_quantity", "weakly_inferred_one_day", "Consecutive market-by-price state deltas, not direct order events."),
        ("trade_flow_pressure", "weakly_inferred_one_day", "Volume increments plus price-change sign; aggressor side is not directly observed."),
        ("cross_symbol_correlation", "weak_one_day", "Five-second forward-filled mid returns; needs multi-day holdout before calibration use."),
        ("regime_transition_probabilities", "blocked", "One day cannot identify robust regime transitions."),
        ("shock_frequency", "blocked", "One day cannot calibrate shock arrival frequencies."),
        ("queue_position_or_fill_priority", "blocked", "Top-five market-by-price feed has no individual order queue identity."),
    ]
    return pd.DataFrame(rows, columns=["parameter", "evidence_label", "evidence_note"])


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


def write_report(output_dir: Path, price: pd.DataFrame, activity: pd.DataFrame, depth: pd.DataFrame, trade_flow: pd.DataFrame, class_summary: pd.DataFrame, corr_summary: pd.DataFrame) -> None:
    largest_gaps = activity.sort_values("stale_gap_gt_15s_count", ascending=False).head(8)
    tightest_spreads = price.sort_values("spread_ticks_median", ascending=True).head(8)
    lines = [
        "# Phase 2 Empirical Calibration Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This report calibrates one-day received-tick distributions from Phase 1 outputs.",
        "It does not certify regime stability, strategy profitability, queue fills or shock frequencies.",
        "",
        "## Inventory",
        "",
        f"- Symbols calibrated: {len(price)}",
        f"- Rows represented: {int(price['rows'].sum()) if len(price) else 0}",
        f"- Symbols with >15s stale gaps: {int((activity['stale_gap_gt_15s_count'] > 0).sum()) if len(activity) else 0}",
        f"- Symbols with book-valid fraction below 99.9%: {int((depth['book_valid_fraction'] < 0.999).sum()) if len(depth) else 0}",
        "",
        "## Instrument-Class Summary",
        "",
        _markdown_table(class_summary),
        "",
        "## Five-Second Cross-Symbol Correlation Summary",
        "",
        _markdown_table(corr_summary),
        "",
        "## Largest Stale-Gap Counts",
        "",
        _markdown_table(largest_gaps[["symbol", "instrument_class", "stale_gap_gt_15s_count", "elapsed_ms_median", "elapsed_ms_q95"]]),
        "",
        "## Tightest Median Spreads",
        "",
        _markdown_table(tightest_spreads[["symbol", "instrument_class", "spread_ticks_median", "spread_ticks_q95", "reference_ltp_median"]]),
        "",
        "## Outputs",
        "",
        "- `price_tick_calibration.csv`",
        "- `activity_calibration.csv`",
        "- `depth_calibration.csv`",
        "- `trade_flow_calibration.csv`",
        "- `cross_section_class_summary.csv`",
        "- `cross_section_correlation_summary.csv`",
        "- `parameter_evidence_ledger.csv`",
        "- `calibration_manifest.json`",
        "",
    ]
    (output_dir / "phase2_calibration_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase2(phase1_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir = phase1_dir / "normalized_ticks_by_symbol"
    delta_dir = phase1_dir / "received_tick_deltas_by_symbol"
    symbol_tables = _read_symbol_tables(normalized_dir, delta_dir)

    price_rows: list[dict] = []
    activity_rows: list[dict] = []
    depth_rows: list[dict] = []
    trade_flow_rows: list[dict] = []
    for index, (symbol, normalized, deltas) in enumerate(symbol_tables, start=1):
        print(f"[phase2] calibrating {index}/{len(symbol_tables)} {symbol}", flush=True)
        price, activity, depth, trade_flow = calibrate_symbol(symbol, normalized, deltas)
        price_rows.append(price)
        activity_rows.append(activity)
        depth_rows.append(depth)
        trade_flow_rows.append(trade_flow)

    price_df = pd.DataFrame(price_rows).sort_values("symbol")
    activity_df = pd.DataFrame(activity_rows).sort_values("symbol")
    depth_df = pd.DataFrame(depth_rows).sort_values("symbol")
    trade_flow_df = pd.DataFrame(trade_flow_rows).sort_values("symbol")
    returns_5s = build_five_second_panel(symbol_tables)
    class_summary, corr_summary = cross_section_outputs(price_df, activity_df, depth_df, trade_flow_df, returns_5s)
    ledger = parameter_evidence_ledger()

    price_df.to_csv(output_dir / "price_tick_calibration.csv", index=False)
    activity_df.to_csv(output_dir / "activity_calibration.csv", index=False)
    depth_df.to_csv(output_dir / "depth_calibration.csv", index=False)
    trade_flow_df.to_csv(output_dir / "trade_flow_calibration.csv", index=False)
    class_summary.to_csv(output_dir / "cross_section_class_summary.csv", index=False)
    corr_summary.to_csv(output_dir / "cross_section_correlation_summary.csv", index=False)
    ledger.to_csv(output_dir / "parameter_evidence_ledger.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "phase1_dir": str(phase1_dir),
        "symbols": int(len(price_df)),
        "rows": int(price_df["rows"].sum()) if len(price_df) else 0,
        "five_second_return_bins": int(len(returns_5s)),
        "evidence_scope": "one_day_received_tick_sample",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase2",
            generated_utc=generated_utc,
            inputs={"phase1_dir": str(phase1_dir)},
            parameters={"calibration_scope": manifest["evidence_scope"]},
            outputs={
                "price_tick_calibration": str(output_dir / "price_tick_calibration.csv"),
                "activity_calibration": str(output_dir / "activity_calibration.csv"),
                "depth_calibration": str(output_dir / "depth_calibration.csv"),
                "trade_flow_calibration": str(output_dir / "trade_flow_calibration.csv"),
                "parameter_evidence_ledger": str(output_dir / "parameter_evidence_ledger.csv"),
                "report": str(output_dir / "phase2_calibration_report.md"),
            },
            random_seed="not_applicable_deterministic_empirical_calibration",
            scenario_ids="not_applicable_received_real_sample",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="not_applicable_no_latency_model",
        )
    )
    (output_dir / "calibration_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, price_df, activity_df, depth_df, trade_flow_df, class_summary, corr_summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 2 empirical calibration from Phase 1 received-tick features.")
    parser.add_argument("--phase1-dir", type=Path, default=Path("outputs/phase1"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase2"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase2(args.phase1_dir, args.output_dir)


if __name__ == "__main__":
    main()

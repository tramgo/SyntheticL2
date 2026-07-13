from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.reproducibility import reproducibility_fields


LEVELS = range(1, 6)


def _safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    denominator = denominator.replace(0, np.nan)
    return numerator / denominator


def _min_positive_increment(values: pd.Series) -> float:
    clean = pd.to_numeric(values, errors="coerce").dropna().sort_values().unique()
    if len(clean) < 2:
        return np.nan
    diffs = np.diff(clean)
    positive = diffs[diffs > 0]
    return float(np.min(positive)) if len(positive) else np.nan


def _book_valid(data: pd.DataFrame) -> pd.Series:
    bid_1 = pd.to_numeric(data["buy_1_price"], errors="coerce")
    ask_1 = pd.to_numeric(data["sell_1_price"], errors="coerce")
    valid = bid_1.notna() & ask_1.notna() & (bid_1 > 0) & (ask_1 > 0) & (bid_1 <= ask_1)
    for level in range(1, 5):
        bid_left = pd.to_numeric(data[f"buy_{level}_price"], errors="coerce")
        bid_right = pd.to_numeric(data[f"buy_{level + 1}_price"], errors="coerce")
        ask_left = pd.to_numeric(data[f"sell_{level}_price"], errors="coerce")
        ask_right = pd.to_numeric(data[f"sell_{level + 1}_price"], errors="coerce")
        valid = valid & ((bid_left >= bid_right) | bid_right.isna())
        valid = valid & ((ask_left <= ask_right) | ask_right.isna())
    return valid


def normalize_ticks(data: pd.DataFrame) -> pd.DataFrame:
    normalized = pd.DataFrame(
        {
            "trading_date": data.get("trade_date"),
            "event_ts_exchange": data.get("exchange_timestamp"),
            "event_ts_receive": data.get("collector_received_utc"),
            "event_ts_receive_ms": pd.to_numeric(data.get("collector_received_utc_ms"), errors="coerce"),
            "event_receive_monotonic_ns": pd.to_numeric(data.get("collector_received_monotonic_ns"), errors="coerce"),
            "instrument_token": data.get("instrument_token"),
            "symbol": data.get("tradingsymbol", data.get("requested_symbol")),
            "requested_symbol": data.get("requested_symbol"),
            "sequence_local": data.get("sequence_local"),
            "source_file": data.get("source_file"),
            "source_file_ordinal": data.get("source_file_ordinal"),
            "row_in_source_file": data.get("row_in_source_file"),
            "observation_semantics": "received_tick",
            "ltp": pd.to_numeric(data.get("last_price"), errors="coerce"),
            "last_trade_qty": pd.to_numeric(data.get("last_traded_quantity"), errors="coerce"),
            "cum_volume": pd.to_numeric(data.get("volume_traded"), errors="coerce"),
            "avg_trade_price": pd.to_numeric(data.get("average_traded_price"), errors="coerce"),
            "open": pd.to_numeric(data.get("ohlc_open"), errors="coerce"),
            "high": pd.to_numeric(data.get("ohlc_high"), errors="coerce"),
            "low": pd.to_numeric(data.get("ohlc_low"), errors="coerce"),
            "close": pd.to_numeric(data.get("ohlc_close"), errors="coerce"),
            "total_buy_qty": pd.to_numeric(data.get("total_buy_quantity"), errors="coerce"),
            "total_sell_qty": pd.to_numeric(data.get("total_sell_quantity"), errors="coerce"),
            "connection_id": pd.NA,
            "is_reconnect_boundary": pd.NA,
        }
    )
    for level in LEVELS:
        normalized[f"bid_px_{level}"] = pd.to_numeric(data.get(f"buy_{level}_price"), errors="coerce")
        normalized[f"bid_qty_{level}"] = pd.to_numeric(data.get(f"buy_{level}_quantity"), errors="coerce")
        normalized[f"bid_orders_{level}"] = pd.to_numeric(data.get(f"buy_{level}_orders"), errors="coerce")
        normalized[f"ask_px_{level}"] = pd.to_numeric(data.get(f"sell_{level}_price"), errors="coerce")
        normalized[f"ask_qty_{level}"] = pd.to_numeric(data.get(f"sell_{level}_quantity"), errors="coerce")
        normalized[f"ask_orders_{level}"] = pd.to_numeric(data.get(f"sell_{level}_orders"), errors="coerce")

    tick_size = _min_positive_increment(normalized["ltp"])
    spread = normalized["ask_px_1"] - normalized["bid_px_1"]
    normalized["spread"] = spread
    normalized["spread_ticks"] = spread / tick_size if tick_size and not np.isnan(tick_size) else np.nan
    normalized["mid_price"] = (normalized["bid_px_1"] + normalized["ask_px_1"]) / 2.0
    normalized["microprice_l1"] = _safe_divide(
        normalized["ask_px_1"] * normalized["bid_qty_1"] + normalized["bid_px_1"] * normalized["ask_qty_1"],
        normalized["bid_qty_1"] + normalized["ask_qty_1"],
    )
    normalized["book_valid"] = _book_valid(data)
    normalized["inferred_tick_size"] = tick_size
    normalized = normalized.sort_values(
        ["event_receive_monotonic_ns", "event_ts_receive_ms", "source_file_ordinal", "row_in_source_file"],
        kind="mergesort",
    ).reset_index(drop=True)
    normalized["sequence_local"] = np.arange(len(normalized), dtype=np.int64)
    return normalized


def derive_deltas(normalized: pd.DataFrame) -> pd.DataFrame:
    deltas = normalized[
        [
            "trading_date",
            "event_ts_receive",
            "event_ts_receive_ms",
            "event_receive_monotonic_ns",
            "instrument_token",
            "symbol",
            "sequence_local",
            "observation_semantics",
            "ltp",
            "cum_volume",
            "spread",
            "spread_ticks",
            "mid_price",
            "microprice_l1",
            "book_valid",
            "inferred_tick_size",
        ]
    ].copy()
    deltas["elapsed_ms"] = deltas["event_ts_receive_ms"].diff()
    deltas["price_change"] = deltas["ltp"].diff()
    deltas["mid_change"] = deltas["mid_price"].diff()
    deltas["microprice_change"] = deltas["microprice_l1"].diff()
    deltas["spread_change"] = deltas["spread"].diff()
    deltas["cum_volume_increment"] = deltas["cum_volume"].diff().clip(lower=0)
    deltas["volume_reversal_flag"] = deltas["cum_volume"].diff() < 0
    deltas["stale_gap_gt_5s"] = deltas["elapsed_ms"] > 5000
    deltas["stale_gap_gt_15s"] = deltas["elapsed_ms"] > 15000

    bid_qty_total = sum(normalized[f"bid_qty_{level}"] for level in LEVELS)
    ask_qty_total = sum(normalized[f"ask_qty_{level}"] for level in LEVELS)
    deltas["l1_imbalance"] = _safe_divide(
        normalized["bid_qty_1"] - normalized["ask_qty_1"],
        normalized["bid_qty_1"] + normalized["ask_qty_1"],
    )
    deltas["l5_imbalance"] = _safe_divide(bid_qty_total - ask_qty_total, bid_qty_total + ask_qty_total)

    mlofi = pd.Series(0.0, index=normalized.index)
    withdrawal = pd.Series(False, index=normalized.index)
    replenishment = pd.Series(False, index=normalized.index)
    for level in LEVELS:
        bid_delta = normalized[f"bid_qty_{level}"].diff()
        ask_delta = normalized[f"ask_qty_{level}"].diff()
        deltas[f"bid_qty_delta_{level}"] = bid_delta
        deltas[f"ask_qty_delta_{level}"] = ask_delta
        deltas[f"bid_px_shift_{level}"] = normalized[f"bid_px_{level}"].diff()
        deltas[f"ask_px_shift_{level}"] = normalized[f"ask_px_{level}"].diff()
        mlofi = mlofi + bid_delta.fillna(0) - ask_delta.fillna(0)
        withdrawal = withdrawal | (bid_delta < 0) | (ask_delta < 0)
        replenishment = replenishment | (bid_delta > 0) | (ask_delta > 0)

    deltas["mlofi_qty"] = mlofi
    deltas["inferred_depth_withdrawal"] = withdrawal
    deltas["inferred_depth_replenishment"] = replenishment
    deltas["inference_confidence"] = "market_by_price_state_delta"
    deltas["aggressor_side_inference"] = np.select(
        [
            (deltas["cum_volume_increment"] > 0) & (deltas["price_change"] > 0),
            (deltas["cum_volume_increment"] > 0) & (deltas["price_change"] < 0),
        ],
        ["buy_pressure_weak", "sell_pressure_weak"],
        default="unknown",
    )

    bid_slope = normalized["bid_px_1"] - normalized["bid_px_5"]
    ask_slope = normalized["ask_px_5"] - normalized["ask_px_1"]
    deltas["book_slope_l5"] = (bid_slope + ask_slope) / 2.0
    bid_near = normalized["bid_qty_1"] + normalized["bid_qty_2"]
    ask_near = normalized["ask_qty_1"] + normalized["ask_qty_2"]
    bid_far = normalized["bid_qty_4"] + normalized["bid_qty_5"]
    ask_far = normalized["ask_qty_4"] + normalized["ask_qty_5"]
    deltas["book_convexity_l5"] = _safe_divide(bid_near + ask_near, bid_far + ask_far)
    deltas["local_volatility_20_ticks"] = deltas["mid_change"].rolling(20, min_periods=5).std()
    return deltas


def summarize_symbol(symbol: str, normalized: pd.DataFrame, deltas: pd.DataFrame) -> dict:
    return {
        "symbol": symbol,
        "rows": int(len(normalized)),
        "first_receive_utc": normalized["event_ts_receive"].iloc[0] if len(normalized) else None,
        "last_receive_utc": normalized["event_ts_receive"].iloc[-1] if len(normalized) else None,
        "book_valid_fraction": float(normalized["book_valid"].mean()) if len(normalized) else np.nan,
        "median_elapsed_ms": float(deltas["elapsed_ms"].median()) if len(deltas) else np.nan,
        "p95_elapsed_ms": float(deltas["elapsed_ms"].quantile(0.95)) if len(deltas) else np.nan,
        "stale_gap_gt_15s_count": int(deltas["stale_gap_gt_15s"].sum()),
        "volume_increment_rows": int((deltas["cum_volume_increment"] > 0).sum()),
        "volume_reversal_rows": int(deltas["volume_reversal_flag"].sum()),
        "inferred_withdrawal_rows": int(deltas["inferred_depth_withdrawal"].sum()),
        "inferred_replenishment_rows": int(deltas["inferred_depth_replenishment"].sum()),
        "median_spread": float(normalized["spread"].median()) if len(normalized) else np.nan,
        "median_spread_ticks": float(normalized["spread_ticks"].median()) if len(normalized) else np.nan,
    }


def run_phase1(input_dir: Path, output_dir: Path) -> None:
    normalized_dir = output_dir / "normalized_ticks_by_symbol"
    delta_dir = output_dir / "received_tick_deltas_by_symbol"
    normalized_dir.mkdir(parents=True, exist_ok=True)
    delta_dir.mkdir(parents=True, exist_ok=True)

    summaries: list[dict] = []
    files = sorted(input_dir.glob("symbol=*/ticks.parquet"))
    for index, path in enumerate(files, start=1):
        symbol = path.parent.name.split("=", 1)[1]
        print(f"[phase1] deriving {index}/{len(files)} {symbol}", flush=True)
        raw = pq.read_table(path).to_pandas()
        normalized = normalize_ticks(raw)
        deltas = derive_deltas(normalized)

        symbol_norm_dir = normalized_dir / f"symbol={symbol}"
        symbol_delta_dir = delta_dir / f"symbol={symbol}"
        symbol_norm_dir.mkdir(parents=True, exist_ok=True)
        symbol_delta_dir.mkdir(parents=True, exist_ok=True)
        pq.write_table(pa.Table.from_pandas(normalized, preserve_index=False), symbol_norm_dir / "normalized_ticks.parquet", compression="zstd")
        pq.write_table(pa.Table.from_pandas(deltas, preserve_index=False), symbol_delta_dir / "received_tick_deltas.parquet", compression="zstd")
        summaries.append(summarize_symbol(symbol, normalized, deltas))

    summary = pd.DataFrame(summaries).sort_values("symbol")
    summary.to_csv(output_dir / "phase1_feature_summary.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "input_dir": str(input_dir),
        "symbols_processed": int(len(summary)),
        "rows_processed": int(summary["rows"].sum()) if len(summary) else 0,
        "outputs": {
            "normalized_ticks_by_symbol": str(normalized_dir),
            "received_tick_deltas_by_symbol": str(delta_dir),
            "phase1_feature_summary": str(output_dir / "phase1_feature_summary.csv"),
            "report": str(output_dir / "phase1_report.md"),
            "manifest": str(output_dir / "phase1_manifest.json"),
        },
        "scope": "phase1_received_tick_normalization_and_delta_features",
        "inference_caveat": "market_by_price_deltas_are_received_tick_inferences_not_exchange_order_events",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase1",
            generated_utc=generated_utc,
            inputs={"input_dir": str(input_dir)},
            parameters={"levels": list(LEVELS), "scope": manifest["scope"]},
            outputs=manifest["outputs"],
            random_seed="not_applicable_deterministic_received_tick_feature_derivation",
            scenario_ids="not_applicable_received_real_sample",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="not_applicable_no_latency_model",
        )
    )
    (output_dir / "phase1_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    report = [
        "# Phase 1 Received-Tick Feature Report",
        "",
        f"Generated UTC: {generated_utc}",
        f"Input directory: `{input_dir}`",
        f"Output directory: `{output_dir}`",
        "",
        "## Scope",
        "",
        "This phase normalizes the Stage A1 compact received-tick stream and derives consecutive received-tick deltas.",
        "Derived add/cancel/aggressor fields remain inference labels, not direct exchange-order observations.",
        "",
        "## Inventory",
        "",
        f"- Symbols processed: {len(summary)}",
        f"- Rows processed: {int(summary['rows'].sum()) if len(summary) else 0}",
        f"- Symbols with volume reversals: {int((summary['volume_reversal_rows'] > 0).sum()) if len(summary) else 0}",
        f"- Symbols with 15s stale gaps: {int((summary['stale_gap_gt_15s_count'] > 0).sum()) if len(summary) else 0}",
        "",
        "## Outputs",
        "",
        "- `normalized_ticks_by_symbol/symbol=*/normalized_ticks.parquet`",
        "- `received_tick_deltas_by_symbol/symbol=*/received_tick_deltas.parquet`",
        "- `phase1_feature_summary.csv`",
        "",
    ]
    (output_dir / "phase1_report.md").write_text("\n".join(report), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Derive Phase 1 normalized ticks and received-tick deltas.")
    parser.add_argument("--input-dir", type=Path, default=Path("outputs/stage_a1/compact_ticks_by_symbol"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase1"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase1(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


LEVELS = range(1, 6)


def load_inputs(phase2_dir: Path, phase5_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    price_cal = pd.read_csv(phase2_dir / "price_tick_calibration.csv")
    depth_cal = pd.read_csv(phase2_dir / "depth_calibration.csv")
    paths = pq.read_table(phase5_dir / "price_paths_5m.parquet").to_pandas()
    return price_cal, depth_cal, paths


def tick_round(value: float, tick_size: float) -> float:
    if not math.isfinite(value):
        value = tick_size
    return max(tick_size, round(value / tick_size) * tick_size)


def quantity_profile(total_qty: float, convexity: float, side_bias: float) -> list[int]:
    convexity = float(np.clip(convexity if math.isfinite(convexity) else 1.0, 0.35, 2.5))
    weights = np.array([(level + 0.5) ** convexity for level in range(5)], dtype=float)
    weights = weights / weights.sum()
    scale = max(total_qty, 5.0) * side_bias
    quantities = np.maximum(1, np.round(scale * weights)).astype(int)
    return quantities.tolist()


def event_label(row: pd.Series, spread_ticks: int, intensity: float) -> str:
    if bool(row["is_market_shock_day"]) and bool(row["is_symbol_shock"]) and abs(float(row["jump_component"])) > 0:
        return "multi_level_sweep"
    if spread_ticks >= max(4, int(float(row["spread_multiplier"]) * 8)):
        return "spread_widening"
    if abs(float(row["bar_return"])) > 0.006:
        return "best_price_shift"
    if intensity > 1.8:
        return "replenishment"
    if intensity < 0.7:
        return "quiet_book_refresh"
    return "book_state_update"


def generate_states(price_cal: pd.DataFrame, depth_cal: pd.DataFrame, paths: pd.DataFrame) -> pd.DataFrame:
    cal = price_cal.merge(depth_cal, on=["symbol", "instrument_class"], how="inner", suffixes=("_price", "_depth"))
    cal_map = {row.symbol: row for row in cal.itertuples(index=False)}
    rows: list[dict] = []

    for index, row in paths.iterrows():
        if index % 75000 == 0:
            print(f"[phase6] generating book state {index + 1}/{len(paths)}", flush=True)
        symbol = row["symbol"]
        params = cal_map[symbol]
        tick_size = float(max(params.inferred_tick_size_median, 0.01))
        mid = float(row["close"])
        spread_base = float(params.spread_ticks_median)
        spread_q95 = float(params.spread_ticks_q95)
        shock_spread = 1.35 if bool(row["is_symbol_shock"]) else 1.0
        spread_ticks = int(max(1, round(spread_base * float(row["spread_multiplier"]) * shock_spread)))
        if bool(row["is_market_shock_day"]):
            spread_ticks = min(max(spread_ticks, int(round(spread_q95))), int(max(spread_q95 * 2, spread_ticks)))
        if spread_ticks % 2 == 1:
            half_down = spread_ticks // 2
            half_up = spread_ticks - half_down
        else:
            half_down = half_up = spread_ticks // 2

        bid_1 = tick_round(mid - half_down * tick_size, tick_size)
        ask_1 = tick_round(mid + half_up * tick_size, tick_size)
        if bid_1 >= ask_1:
            bid_1 = tick_round(mid - tick_size, tick_size)
            ask_1 = tick_round(mid + tick_size, tick_size)

        depth_multiplier = float(row["depth_multiplier"])
        if bool(row["is_symbol_shock"]):
            depth_multiplier *= 0.65
        volatility_thin = max(0.35, 1.0 - min(abs(float(row["bar_return"])) * 20.0, 0.45))
        bid_total = float(params.bid_l5_qty_median) * depth_multiplier * volatility_thin
        ask_total = float(params.ask_l5_qty_median) * depth_multiplier * volatility_thin
        imbalance = float(params.l5_imbalance_median)
        if float(row["bar_return"]) > 0:
            ask_total *= max(0.55, 1.0 - abs(float(row["bar_return"])) * 8.0)
        elif float(row["bar_return"]) < 0:
            bid_total *= max(0.55, 1.0 - abs(float(row["bar_return"])) * 8.0)
        bid_qty = quantity_profile(bid_total, float(params.book_convexity_l5_median), 1.0 + max(imbalance, 0))
        ask_qty = quantity_profile(ask_total, float(params.book_convexity_l5_median), 1.0 + max(-imbalance, 0))
        bid_orders = [max(1, int(round(q / max(1, np.sqrt(q) * 2.5)))) for q in bid_qty]
        ask_orders = [max(1, int(round(q / max(1, np.sqrt(q) * 2.5)))) for q in ask_qty]

        intensity = float(row["event_rate_multiplier"]) * (1.0 + min(abs(float(row["bar_return"])) * 50.0, 2.0))
        state = {
            "quarter_profile": row["quarter_profile"],
            "scenario_day": int(row["scenario_day"]),
            "trade_date": row["trade_date"],
            "bar_index": int(row["bar_index"]),
            "bar_start": row["bar_start"],
            "symbol": symbol,
            "regime_code": row["regime_code"],
            "regime_family": row["regime_family"],
            "mid_price": mid,
            "tick_size": tick_size,
            "spread_ticks": spread_ticks,
            "spread": spread_ticks * tick_size,
            "book_event_label": event_label(row, spread_ticks, intensity),
            "event_intensity_proxy": intensity,
            "is_market_shock_day": bool(row["is_market_shock_day"]),
            "is_symbol_shock": bool(row["is_symbol_shock"]),
            "bar_return": float(row["bar_return"]),
            "depth_multiplier": depth_multiplier,
            "evidence_label": "synthetic_l2_state_v1",
        }
        for level in LEVELS:
            state[f"bid_px_{level}"] = tick_round(bid_1 - (level - 1) * tick_size, tick_size)
            state[f"ask_px_{level}"] = tick_round(ask_1 + (level - 1) * tick_size, tick_size)
            state[f"bid_qty_{level}"] = bid_qty[level - 1]
            state[f"ask_qty_{level}"] = ask_qty[level - 1]
            state[f"bid_orders_{level}"] = bid_orders[level - 1]
            state[f"ask_orders_{level}"] = ask_orders[level - 1]
        rows.append(state)
    return pd.DataFrame(rows)


def validate_books(states: pd.DataFrame) -> dict:
    bid_order_errors = pd.Series(False, index=states.index)
    ask_order_errors = pd.Series(False, index=states.index)
    for level in range(1, 5):
        bid_order_errors = bid_order_errors | (states[f"bid_px_{level}"] < states[f"bid_px_{level + 1}"])
        ask_order_errors = ask_order_errors | (states[f"ask_px_{level}"] > states[f"ask_px_{level + 1}"])
    crossed = states["bid_px_1"] >= states["ask_px_1"]
    nonpositive_qty = pd.Series(False, index=states.index)
    nonpositive_orders = pd.Series(False, index=states.index)
    tick_errors = pd.Series(False, index=states.index)
    for level in LEVELS:
        nonpositive_qty = nonpositive_qty | (states[f"bid_qty_{level}"] <= 0) | (states[f"ask_qty_{level}"] <= 0)
        nonpositive_orders = nonpositive_orders | (states[f"bid_orders_{level}"] <= 0) | (states[f"ask_orders_{level}"] <= 0)
        tick_errors = tick_errors | (((states[f"bid_px_{level}"] / states["tick_size"]).round() - states[f"bid_px_{level}"] / states["tick_size"]).abs() > 1e-7)
        tick_errors = tick_errors | (((states[f"ask_px_{level}"] / states["tick_size"]).round() - states[f"ask_px_{level}"] / states["tick_size"]).abs() > 1e-7)
    return {
        "book_rows": int(len(states)),
        "profiles": int(states["quarter_profile"].nunique()),
        "scenario_days": int(states[["quarter_profile", "scenario_day"]].drop_duplicates().shape[0]),
        "symbols": int(states["symbol"].nunique()),
        "crossed_or_locked_l1_rows": int(crossed.sum()),
        "bid_depth_sort_error_rows": int(bid_order_errors.sum()),
        "ask_depth_sort_error_rows": int(ask_order_errors.sum()),
        "nonpositive_quantity_rows": int(nonpositive_qty.sum()),
        "nonpositive_order_rows": int(nonpositive_orders.sum()),
        "tick_grid_error_rows": int(tick_errors.sum()),
        "median_spread_ticks": float(states["spread_ticks"].median()),
        "q95_spread_ticks": float(states["spread_ticks"].quantile(0.95)),
    }


def build_summary(states: pd.DataFrame) -> pd.DataFrame:
    return states.groupby(["quarter_profile", "regime_code", "book_event_label"], sort=True).agg(
        rows=("symbol", "count"),
        median_spread_ticks=("spread_ticks", "median"),
        median_event_intensity_proxy=("event_intensity_proxy", "median"),
        median_bid_l5_qty=("bid_qty_5", "median"),
        median_ask_l5_qty=("ask_qty_5", "median"),
    ).reset_index()


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


def write_report(output_dir: Path, validation: dict, summary: pd.DataFrame) -> None:
    event_counts = summary.groupby("book_event_label", sort=True)["rows"].sum().reset_index().sort_values("rows", ascending=False)
    lines = [
        "# Phase 6 L2 Book Generator Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase generates one synthetic top-five market-by-price book state per Phase 5 price bar.",
        "It does not yet produce individual exchange order events or deterministic queue/fill priority.",
        "",
        "## Validation",
        "",
        *(f"- {key}: {value}" for key, value in validation.items()),
        "",
        "## Event Label Counts",
        "",
        _markdown_table(event_counts),
        "",
        "## Outputs",
        "",
        "- `l2_book_states_5m.parquet`",
        "- `l2_book_summary.csv`",
        "- `l2_book_manifest.json`",
        "",
    ]
    (output_dir / "phase6_l2_book_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase6(phase2_dir: Path, phase5_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    price_cal, depth_cal, paths = load_inputs(phase2_dir, phase5_dir)
    states = generate_states(price_cal, depth_cal, paths)
    summary = build_summary(states)
    validation = validate_books(states)
    pq.write_table(pa.Table.from_pandas(states, preserve_index=False), output_dir / "l2_book_states_5m.parquet", compression="zstd")
    summary.to_csv(output_dir / "l2_book_summary.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "phase2_dir": str(phase2_dir),
        "phase5_dir": str(phase5_dir),
        "validation": validation,
        "evidence_scope": "synthetic_l2_state_v1_market_by_price",
    }
    (output_dir / "l2_book_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, validation, summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Phase 6 synthetic top-five L2 book states.")
    parser.add_argument("--phase2-dir", type=Path, default=Path("outputs/phase2"))
    parser.add_argument("--phase5-dir", type=Path, default=Path("outputs/phase5"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase6"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase6(args.phase2_dir, args.phase5_dir, args.output_dir)


if __name__ == "__main__":
    main()


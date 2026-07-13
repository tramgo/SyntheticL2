from __future__ import annotations

import argparse
import json
import math
import random
from datetime import datetime, time, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.reproducibility import reproducibility_fields


SYMBOL_SECTORS = {
    "ADANIPORTS": "industrials",
    "AXISBANK": "financials",
    "BAJAJ-AUTO": "autos",
    "BANKBEES": "etf",
    "BHARTIARTL": "telecom",
    "BPCL": "energy",
    "BRITANNIA": "consumer",
    "CIPLA": "pharma",
    "DRREDDY": "pharma",
    "GOLDBEES": "commodity_etf",
    "HCLTECH": "it",
    "HDFCBANK": "financials",
    "HINDUNILVR": "consumer",
    "ICICIBANK": "financials",
    "INFY": "it",
    "ITBEES": "it_etf",
    "ITC": "consumer",
    "JUNIORBEES": "index_etf",
    "KOTAKBANK": "financials",
    "LT": "industrials",
    "M&M": "autos",
    "MARUTI": "autos",
    "NESTLEIND": "consumer",
    "NIFTYBEES": "index_etf",
    "ONGC": "energy",
    "RELIANCE": "energy",
    "SBIN": "financials",
    "SUNPHARMA": "pharma",
    "TCS": "it",
    "TECHM": "it",
    "ULTRACEMCO": "materials",
    "WIPRO": "it",
}

DRIFT_BY_REGIME = {
    "D01": 0.0000,
    "D02": 0.0000,
    "D03": 0.0000,
    "D04": 0.0040,
    "D05": 0.0100,
    "D06": -0.0040,
    "D07": -0.0180,
    "D08": 0.0060,
    "D09": -0.0020,
    "D10": -0.0080,
    "D11": 0.0020,
    "D12": 0.0000,
    "D13": -0.0010,
    "D14": 0.0000,
    "D15": 0.0000,
    "D16": 0.0020,
    "D17": 0.0000,
    "D18": 0.0000,
    "D19": 0.0000,
    "D20": -0.0040,
}

SESSION_START = time(9, 15)
SESSION_END = time(15, 30)
BAR_MINUTES = 5


def load_inputs(phase2_dir: Path, phase4_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    price = pd.read_csv(phase2_dir / "price_tick_calibration.csv")
    activity = pd.read_csv(phase2_dir / "activity_calibration.csv")
    calendar = pd.read_csv(phase4_dir / "scenario_calendar.csv")
    return price, activity, calendar


def tick_round(price: float, tick_size: float) -> float:
    if not math.isfinite(price) or price <= 0:
        return max(tick_size, tick_size)
    if not tick_size or tick_size <= 0 or not math.isfinite(tick_size):
        tick_size = 0.05
    return max(tick_size, round(price / tick_size) * tick_size)


def intraday_times(trade_date: str) -> list[pd.Timestamp]:
    start = pd.Timestamp.combine(pd.Timestamp(trade_date).date(), SESSION_START)
    end = pd.Timestamp.combine(pd.Timestamp(trade_date).date(), SESSION_END)
    return list(pd.date_range(start=start, end=end, freq=f"{BAR_MINUTES}min", inclusive="left"))


def tod_weight(index: int, total: int) -> float:
    x = index / max(total - 1, 1)
    return 0.85 + 0.45 * (abs(x - 0.5) * 2.0) ** 1.5


def symbol_seed(base_seed: int, scenario_day: int, symbol: str) -> int:
    return base_seed * 1000003 + scenario_day * 9176 + sum(ord(ch) for ch in symbol)


def prepare_symbol_parameters(price: pd.DataFrame, activity: pd.DataFrame) -> pd.DataFrame:
    params = price.merge(activity[["symbol", "event_rate_per_second", "elapsed_ms_median"]], on="symbol", how="left")
    params["sector"] = params["symbol"].map(SYMBOL_SECTORS).fillna("other")
    params["tick_size"] = params["inferred_tick_size_median"].fillna(0.05).clip(lower=0.01)
    params["reference_price"] = params["reference_ltp_median"].clip(lower=params["tick_size"])
    # Convert observed mid-change rupee scale to a cautious 5-minute return-vol proxy.
    params["base_bar_vol"] = (
        (params["microprice_change_std"].abs() / params["reference_price"]).replace([np.inf, -np.inf], np.nan).fillna(0.0005)
        * 2.5
    ).clip(lower=0.0002, upper=0.012)
    params["beta"] = np.where(params["instrument_class"] == "etf", 0.75, 1.0)
    params.loc[params["sector"].isin(["financials", "it", "energy"]), "beta"] = 1.10
    params.loc[params["sector"].isin(["consumer", "pharma"]), "beta"] = 0.80
    return params


def regime_return_shape(regime_code: str, n: int) -> np.ndarray:
    x = np.linspace(0, 1, n)
    if regime_code in {"D04", "D05", "D06", "D07"}:
        return 0.7 + 0.6 * x
    if regime_code in {"D08", "D10"}:
        return np.exp(-3 * x)
    if regime_code in {"D09", "D11", "D19"}:
        return np.where(x < 0.45, 1.0, -0.8)
    if regime_code in {"D12", "D20"}:
        return 0.6 + 1.4 * np.exp(-((x - 0.45) ** 2) / 0.018)
    return np.ones(n)


def simulate_day(day: pd.Series, params: pd.DataFrame) -> pd.DataFrame:
    times = intraday_times(day["trade_date"])
    n = len(times)
    base_seed = int(day["seed"])
    day_seed = base_seed * 1009 + int(day["scenario_day"])
    market_rng = np.random.default_rng(day_seed)
    regime_code = str(day["regime_code"])
    vol_multiplier = float(day["vol_multiplier"])
    corr_multiplier = float(day["correlation_multiplier"])
    drift = DRIFT_BY_REGIME.get(regime_code, 0.0)
    shape = regime_return_shape(regime_code, n)
    shape = shape / max(np.abs(shape).sum(), 1.0)
    market_vol = 0.0012 * vol_multiplier * corr_multiplier
    market_noise = market_rng.normal(0.0, market_vol, n) * np.array([tod_weight(i, n) for i in range(n)])
    market_drift = drift * shape
    market_returns = market_noise + market_drift

    sector_returns: dict[str, np.ndarray] = {}
    for sector in sorted(params["sector"].unique()):
        sector_seed = day_seed + sum(ord(ch) for ch in sector)
        rng = np.random.default_rng(sector_seed)
        sector_returns[sector] = 0.45 * market_returns + rng.normal(0.0, market_vol * 0.65, n)

    shock_symbols = set(str(day.get("shock_symbols", "")).split("|")) if pd.notna(day.get("shock_symbols", "")) else set()
    shock_symbols.discard("")
    rows: list[dict] = []
    for param in params.itertuples(index=False):
        symbol = param.symbol
        rng = np.random.default_rng(symbol_seed(base_seed, int(day["scenario_day"]), symbol))
        py_rng = random.Random(symbol_seed(base_seed, int(day["scenario_day"]), symbol) + 13)
        tick_size = float(param.tick_size)
        reference_price = float(param.reference_price)
        previous_close = reference_price

        if bool(day["is_gap_day"]):
            gap_direction = -1 if regime_code in {"D10", "D11"} else 1
            if regime_code == "D09":
                gap_direction = 1
            gap_return = gap_direction * py_rng.uniform(0.002, 0.018) * vol_multiplier
        else:
            gap_return = py_rng.uniform(-0.002, 0.002)

        open_price = tick_round(previous_close * (1.0 + gap_return), tick_size)
        last_close = open_price
        cumulative_return = 0.0
        sector_path = sector_returns.get(param.sector, np.zeros(n))
        idio_vol = float(param.base_bar_vol) * vol_multiplier
        for bar_index, ts in enumerate(times):
            idio = rng.normal(0.0, idio_vol * tod_weight(bar_index, n))
            jump = 0.0
            if symbol in shock_symbols and bool(day["is_market_shock_day"]) and bar_index in {max(1, n // 3), max(2, n // 2)}:
                jump_sign = -1 if regime_code in {"D07", "D10", "D20"} else rng.choice([-1, 1])
                jump = jump_sign * rng.uniform(0.002, 0.012) * vol_multiplier
            ret = float(param.beta) * market_returns[bar_index] + 0.35 * sector_path[bar_index] + idio + jump
            cumulative_return += ret

            open_bar = last_close
            close_bar = tick_round(open_bar * math.exp(ret), tick_size)
            wiggle = abs(rng.normal(0.0, idio_vol * open_bar * 0.45))
            high_bar = tick_round(max(open_bar, close_bar) + wiggle, tick_size)
            low_bar = tick_round(max(tick_size, min(open_bar, close_bar) - wiggle), tick_size)
            close_bar = min(max(close_bar, low_bar), high_bar)
            rows.append(
                {
                    "quarter_profile": day["quarter_profile"],
                    "scenario_day": int(day["scenario_day"]),
                    "trade_date": day["trade_date"],
                    "bar_index": bar_index,
                    "bar_start": ts.isoformat(),
                    "symbol": symbol,
                    "sector": param.sector,
                    "regime_code": regime_code,
                    "regime_family": day["regime_family"],
                    "intraday_template": day["intraday_template"],
                    "open": open_bar,
                    "high": high_bar,
                    "low": low_bar,
                    "close": close_bar,
                    "bar_return": math.log(close_bar / open_bar) if open_bar > 0 and close_bar > 0 else 0.0,
                    "cumulative_return": cumulative_return,
                    "tick_size": tick_size,
                    "vol_multiplier": vol_multiplier,
                    "event_rate_multiplier": float(day["event_rate_multiplier"]),
                    "spread_multiplier": float(day["spread_multiplier"]),
                    "depth_multiplier": float(day["depth_multiplier"]),
                    "correlation_multiplier": corr_multiplier,
                    "is_gap_day": bool(day["is_gap_day"]),
                    "is_market_shock_day": bool(day["is_market_shock_day"]),
                    "is_symbol_shock": symbol in shock_symbols,
                    "market_component": float(market_returns[bar_index]),
                    "sector_component": float(sector_path[bar_index]),
                    "idiosyncratic_component": float(idio),
                    "jump_component": float(jump),
                    "evidence_label": "synthetic_price_process_v1",
                }
            )
            last_close = close_bar
    return pd.DataFrame(rows)


def build_daily_summary(paths: pd.DataFrame) -> pd.DataFrame:
    summary = paths.groupby(["quarter_profile", "scenario_day", "trade_date", "regime_code", "symbol"], sort=True).agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
        bars=("bar_index", "count"),
        shock_bars=("is_symbol_shock", "sum"),
        mean_spread_multiplier=("spread_multiplier", "mean"),
        mean_depth_multiplier=("depth_multiplier", "mean"),
    ).reset_index()
    summary["daily_return"] = (summary["close"] / summary["open"]) - 1.0
    summary["high_low_range"] = (summary["high"] / summary["low"]) - 1.0
    return summary


def validate_paths(paths: pd.DataFrame, daily: pd.DataFrame) -> dict:
    tick_grid_error = ((paths["close"] / paths["tick_size"]).round() - (paths["close"] / paths["tick_size"])).abs().max()
    return {
        "bar_rows": int(len(paths)),
        "daily_rows": int(len(daily)),
        "profiles": int(paths["quarter_profile"].nunique()),
        "scenario_days": int(paths[["quarter_profile", "scenario_day"]].drop_duplicates().shape[0]),
        "symbols": int(paths["symbol"].nunique()),
        "bars_per_symbol_day_min": int(daily["bars"].min()) if len(daily) else 0,
        "bars_per_symbol_day_max": int(daily["bars"].max()) if len(daily) else 0,
        "min_price": float(paths[["open", "high", "low", "close"]].min().min()),
        "max_tick_grid_error": float(tick_grid_error),
        "high_low_violations": int(((paths["high"] < paths[["open", "close"]].max(axis=1)) | (paths["low"] > paths[["open", "close"]].min(axis=1))).sum()),
    }


def write_report(output_dir: Path, validation: dict, daily: pd.DataFrame) -> None:
    profile_summary = daily.groupby("quarter_profile", sort=True).agg(
        symbol_days=("symbol", "count"),
        median_daily_return=("daily_return", "median"),
        q05_daily_return=("daily_return", lambda x: x.quantile(0.05)),
        q95_daily_return=("daily_return", lambda x: x.quantile(0.95)),
        median_high_low_range=("high_low_range", "median"),
    ).reset_index()
    lines = [
        "# Phase 5 Price Process Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase generates deterministic 5-minute synthetic OHLC price paths from the Phase 4 scenario calendar.",
        "It does not yet generate L2 depth states, order-book events, retail feed effects or strategy fills.",
        "",
        "## Validation",
        "",
        *(f"- {key}: {value}" for key, value in validation.items()),
        "",
        "## Profile Summary",
        "",
        _markdown_table(profile_summary),
        "",
        "## Outputs",
        "",
        "- `price_paths_5m.parquet`",
        "- `daily_price_summary.csv`",
        "- `price_process_manifest.json`",
        "",
    ]
    (output_dir / "phase5_price_process_report.md").write_text("\n".join(lines), encoding="utf-8")


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


def run_phase5(phase2_dir: Path, phase4_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    price, activity, calendar = load_inputs(phase2_dir, phase4_dir)
    params = prepare_symbol_parameters(price, activity)
    day_frames: list[pd.DataFrame] = []
    total_days = len(calendar)
    for index, day in calendar.iterrows():
        if (index + 1) % 20 == 0 or index == 0:
            print(f"[phase5] simulating day {index + 1}/{total_days}", flush=True)
        day_frames.append(simulate_day(day, params))
    paths = pd.concat(day_frames, ignore_index=True)
    daily = build_daily_summary(paths)
    validation = validate_paths(paths, daily)

    pq.write_table(pa.Table.from_pandas(paths, preserve_index=False), output_dir / "price_paths_5m.parquet", compression="zstd")
    daily.to_csv(output_dir / "daily_price_summary.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "phase2_dir": str(phase2_dir),
        "phase4_dir": str(phase4_dir),
        "bar_minutes": BAR_MINUTES,
        "session_start": SESSION_START.isoformat(),
        "session_end": SESSION_END.isoformat(),
        "validation": validation,
        "evidence_scope": "synthetic_price_process_v1",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase5",
            generated_utc=generated_utc,
            inputs={"phase2_dir": str(phase2_dir), "phase4_dir": str(phase4_dir)},
            parameters={
                "bar_minutes": BAR_MINUTES,
                "session_start": SESSION_START.isoformat(),
                "session_end": SESSION_END.isoformat(),
            },
            outputs={
                "price_paths_5m": str(output_dir / "price_paths_5m.parquet"),
                "daily_price_summary": str(output_dir / "daily_price_summary.csv"),
                "report": str(output_dir / "phase5_price_process_report.md"),
            },
            random_seed="phase4_scenario_calendar.seed plus deterministic symbol_seed",
            scenario_ids="outputs/phase4/scenario_calendar.csv",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="not_applicable_no_latency_model",
        )
    )
    (output_dir / "price_process_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, validation, daily)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Phase 5 synthetic 5-minute price paths.")
    parser.add_argument("--phase2-dir", type=Path, default=Path("outputs/phase2"))
    parser.add_argument("--phase4-dir", type=Path, default=Path("outputs/phase4"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase5"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase5(args.phase2_dir, args.phase4_dir, args.output_dir)


if __name__ == "__main__":
    main()

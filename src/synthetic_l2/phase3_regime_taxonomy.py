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


INTRADAY_STATE_DESCRIPTIONS = {
    "I01": "Pre-open/opening discovery",
    "I02": "Opening momentum",
    "I03": "Opening reversal",
    "I04": "Normal continuous trading",
    "I05": "Midday liquidity lull",
    "I06": "Momentum burst",
    "I07": "Volatility burst",
    "I08": "Liquidity withdrawal",
    "I11": "Range compression",
    "I18": "Feed degradation/reconnect episode",
}

DAILY_REGIME_DESCRIPTIONS = {
    "D01": "Normal balanced",
    "D03": "High-volatility sideways",
    "D04": "Gradual bullish trend",
    "D06": "Gradual bearish trend",
    "D13": "Liquidity-stressed",
    "D16": "Index-dominated day",
    "D17": "Stock-specific dispersion",
}


def _symbol_from_path(path: Path) -> str:
    return path.parent.name.split("=", 1)[1]


def _instrument_class(symbol: str) -> str:
    return "etf" if symbol in ETF_SYMBOLS else "equity"


def _zscore(series: pd.Series) -> pd.Series:
    clean = pd.to_numeric(series, errors="coerce")
    std = clean.std()
    if pd.isna(std) or std == 0:
        return pd.Series(0.0, index=series.index)
    return (clean - clean.mean()) / std


def load_symbol_tables(phase1_dir: Path) -> list[tuple[str, pd.DataFrame, pd.DataFrame]]:
    normalized_dir = phase1_dir / "normalized_ticks_by_symbol"
    delta_dir = phase1_dir / "received_tick_deltas_by_symbol"
    tables: list[tuple[str, pd.DataFrame, pd.DataFrame]] = []
    for normalized_path in sorted(normalized_dir.glob("symbol=*/normalized_ticks.parquet")):
        symbol = _symbol_from_path(normalized_path)
        delta_path = delta_dir / f"symbol={symbol}" / "received_tick_deltas.parquet"
        normalized = pq.ParquetFile(normalized_path).read().to_pandas()
        deltas = pq.ParquetFile(delta_path).read().to_pandas()
        tables.append((symbol, normalized, deltas))
    return tables


def symbol_bin_features(symbol: str, normalized: pd.DataFrame, deltas: pd.DataFrame, bin_ms: int) -> pd.DataFrame:
    frame = normalized[
        [
            "event_ts_receive_ms",
            "mid_price",
            "spread_ticks",
            "book_valid",
        ]
    ].copy()
    frame["symbol"] = symbol
    frame["instrument_class"] = _instrument_class(symbol)
    frame["bin_id"] = (pd.to_numeric(frame["event_ts_receive_ms"], errors="coerce") // bin_ms).astype("int64")
    delta_frame = deltas[
        [
            "event_ts_receive_ms",
            "cum_volume_increment",
            "mid_change",
            "l5_imbalance",
            "inferred_depth_withdrawal",
            "stale_gap_gt_15s",
        ]
    ].copy()
    delta_frame["bin_id"] = (pd.to_numeric(delta_frame["event_ts_receive_ms"], errors="coerce") // bin_ms).astype("int64")

    grouped = frame.groupby("bin_id", sort=True).agg(
        symbol=("symbol", "first"),
        instrument_class=("instrument_class", "first"),
        first_receive_ms=("event_ts_receive_ms", "min"),
        last_receive_ms=("event_ts_receive_ms", "max"),
        event_count=("event_ts_receive_ms", "count"),
        first_mid=("mid_price", "first"),
        last_mid=("mid_price", "last"),
        median_spread_ticks=("spread_ticks", "median"),
        book_valid_fraction=("book_valid", "mean"),
    )
    delta_grouped = delta_frame.groupby("bin_id", sort=True).agg(
        volume_increment=("cum_volume_increment", "sum"),
        abs_mid_change_sum=("mid_change", lambda value: pd.to_numeric(value, errors="coerce").abs().sum()),
        median_l5_imbalance=("l5_imbalance", "median"),
        withdrawal_rows=("inferred_depth_withdrawal", "sum"),
        stale_gap_gt_15s_count=("stale_gap_gt_15s", "sum"),
    )
    out = grouped.join(delta_grouped, how="left").reset_index()
    valid_mid = (out["first_mid"] > 0) & (out["last_mid"] > 0)
    out["bin_return"] = np.where(valid_mid, (out["last_mid"] / out["first_mid"]) - 1.0, np.nan)
    out["receive_utc"] = pd.to_datetime(out["first_receive_ms"], unit="ms", utc=True)
    return out


def build_intraday_states(symbol_bins: pd.DataFrame) -> pd.DataFrame:
    market = symbol_bins.groupby("bin_id", sort=True).agg(
        first_receive_ms=("first_receive_ms", "min"),
        last_receive_ms=("last_receive_ms", "max"),
        symbols_seen=("symbol", "nunique"),
        event_count=("event_count", "sum"),
        median_symbol_return=("bin_return", "median"),
        median_abs_mid_change_sum=("abs_mid_change_sum", "median"),
        median_spread_ticks=("median_spread_ticks", "median"),
        median_l5_imbalance=("median_l5_imbalance", "median"),
        total_volume_increment=("volume_increment", "sum"),
        withdrawal_rows=("withdrawal_rows", "sum"),
        stale_gap_gt_15s_count=("stale_gap_gt_15s_count", "sum"),
    ).reset_index()
    market["receive_utc"] = pd.to_datetime(market["first_receive_ms"], unit="ms", utc=True)
    market["event_z"] = _zscore(market["event_count"])
    market["vol_z"] = _zscore(market["median_abs_mid_change_sum"])
    market["spread_z"] = _zscore(market["median_spread_ticks"])
    market["withdrawal_z"] = _zscore(market["withdrawal_rows"])

    states: list[str] = []
    reasons: list[str] = []
    for ordinal, row in market.reset_index(drop=True).iterrows():
        if row["stale_gap_gt_15s_count"] > 0:
            state, reason = "I18", "stale receive gap observed"
        elif ordinal < 3:
            if row["median_symbol_return"] > 0.001:
                state, reason = "I02", "opening positive momentum"
            elif row["median_symbol_return"] < -0.001:
                state, reason = "I03", "opening negative reversal pressure"
            else:
                state, reason = "I01", "opening discovery"
        elif row["spread_z"] > 1.0 and row["withdrawal_z"] > 0.5:
            state, reason = "I08", "spread and withdrawal elevated"
        elif row["vol_z"] > 1.25 and abs(row["median_symbol_return"]) > 0.0005:
            state, reason = "I06", "directional volatility burst"
        elif row["vol_z"] > 1.25:
            state, reason = "I07", "non-directional volatility burst"
        elif row["event_z"] < -0.75 and row["vol_z"] < -0.5:
            state, reason = "I05", "low activity and low movement"
        elif row["vol_z"] < -0.75 and row["spread_z"] < 0:
            state, reason = "I11", "range compression"
        else:
            state, reason = "I04", "baseline continuous trading"
        states.append(state)
        reasons.append(reason)
    market["intraday_state"] = states
    market["state_description"] = market["intraday_state"].map(INTRADAY_STATE_DESCRIPTIONS)
    market["classification_reason"] = reasons
    market["evidence_label"] = "one_day_candidate"
    return market


def classify_ticker_states(symbol_bins: pd.DataFrame, intraday: pd.DataFrame) -> pd.DataFrame:
    market_returns = intraday.set_index("bin_id")["median_symbol_return"]
    symbol_total_returns = symbol_bins.groupby("symbol").apply(_total_return_from_bins, include_groups=False)
    symbol_gross_returns = symbol_bins.groupby("symbol")["bin_return"].apply(lambda x: pd.to_numeric(x, errors="coerce").abs().sum())
    symbol_volume_totals = symbol_bins.groupby("symbol")["volume_increment"].sum()
    spread_tail = symbol_bins["median_spread_ticks"].quantile(0.85)
    total_return_median_abs = symbol_total_returns.abs().median()
    total_return_q85 = symbol_total_returns.quantile(0.85)
    total_return_q15 = symbol_total_returns.quantile(0.15)
    volume_q85 = symbol_volume_totals.quantile(0.85)
    gross_return_q85 = symbol_gross_returns.quantile(0.85)
    rows: list[dict] = []
    for symbol, group in symbol_bins.groupby("symbol", sort=True):
        aligned = group.set_index("bin_id")["bin_return"].replace([np.inf, -np.inf], np.nan).reindex(market_returns.index)
        corr = aligned.corr(market_returns)
        event_rate = group["event_count"].sum() / max((group["last_receive_ms"].max() - group["first_receive_ms"].min()) / 1000.0, 1.0)
        total_return = _total_return_from_bins(group)
        spread_median = group["median_spread_ticks"].median()
        stale_bins = int((group["stale_gap_gt_15s_count"] > 0).sum())
        volume_total = group["volume_increment"].sum()
        abs_return = pd.to_numeric(group["bin_return"], errors="coerce").abs().sum()

        if stale_bins > 0 and event_rate < 0.8:
            state, reason = "illiquid/stale", "stale gaps plus low event rate"
        elif spread_median >= spread_tail:
            state, reason = "spread stress", "median spread in top cross-sectional tail"
        elif pd.notna(corr) and corr > 0.45 and pd.notna(total_return) and abs(total_return) > total_return_median_abs:
            state, reason = "high-beta follower", "positive market correlation with larger move"
        elif pd.notna(corr) and corr > 0.20:
            state, reason = "market follower", "positive market correlation"
        elif volume_total >= volume_q85:
            state, reason = "abnormal volume", "volume increment in top cross-sectional tail"
        elif pd.notna(total_return) and total_return >= total_return_q85:
            state, reason = "leader", "total return in top cross-sectional tail"
        elif pd.notna(total_return) and total_return <= total_return_q15:
            state, reason = "laggard", "total return in bottom cross-sectional tail"
        elif abs_return >= gross_return_q85:
            state, reason = "mean-reverting outlier", "large gross movement without strong market-following label"
        else:
            state, reason = "defensive/low-beta", "low or unclear market correlation"

        rows.append(
            {
                "symbol": symbol,
                "instrument_class": _instrument_class(symbol),
                "ticker_state": state,
                "classification_reason": reason,
                "market_return_corr_5m": float(corr) if pd.notna(corr) else np.nan,
                "event_rate_per_second": float(event_rate),
                "total_return": float(total_return) if pd.notna(total_return) else np.nan,
                "median_spread_ticks": float(spread_median) if pd.notna(spread_median) else np.nan,
                "stale_bins": stale_bins,
                "volume_increment_total": float(volume_total),
                "gross_abs_return": float(abs_return),
                "evidence_label": "one_day_candidate",
            }
        )
    return pd.DataFrame(rows).sort_values("symbol")


def classify_daily_regime(symbol_bins: pd.DataFrame, intraday: pd.DataFrame, phase2_dir: Path) -> pd.DataFrame:
    symbol_returns = symbol_bins.groupby("symbol").apply(_total_return_from_bins, include_groups=False).replace([np.inf, -np.inf], np.nan).dropna()
    median_return = float(symbol_returns.median())
    dispersion = float(symbol_returns.quantile(0.75) - symbol_returns.quantile(0.25))
    stale_state_fraction = float((intraday["intraday_state"] == "I18").mean()) if len(intraday) else np.nan
    stressed_fraction = float((intraday["intraday_state"] == "I08").mean()) if len(intraday) else np.nan
    corr_path = phase2_dir / "cross_section_correlation_summary.csv"
    corr_median = np.nan
    if corr_path.exists():
        corr = pd.read_csv(corr_path)
        match = corr.loc[corr["metric"] == "five_second_pairwise_corr_median", "value"]
        if len(match):
            corr_median = float(match.iloc[0])

    if stale_state_fraction > 0.15 or stressed_fraction > 0.20:
        code, reason = "D13", "liquidity or feed stress dominates observed state mix"
    elif corr_median > 0.25 and abs(median_return) > 0.002:
        code, reason = "D16", "common cross-symbol move with positive return correlation"
    elif dispersion > 0.01 and abs(median_return) < 0.003:
        code, reason = "D17", "high dispersion with muted median move"
    elif median_return > 0.004:
        code, reason = "D04", "positive median cross-symbol drift"
    elif median_return < -0.004:
        code, reason = "D06", "negative median cross-symbol drift"
    elif intraday["vol_z"].quantile(0.90) > 1.5:
        code, reason = "D03", "large intraday volatility bursts without strong trend"
    else:
        code, reason = "D01", "balanced one-day candidate"

    return pd.DataFrame(
        [
            {
                "trade_date": "2026-07-13",
                "daily_regime_code": code,
                "daily_regime": DAILY_REGIME_DESCRIPTIONS[code],
                "classification_reason": reason,
                "median_symbol_return": median_return,
                "return_iqr": dispersion,
                "five_second_pairwise_corr_median": corr_median,
                "intraday_bins": int(len(intraday)),
                "stale_or_feed_state_fraction": stale_state_fraction,
                "liquidity_withdrawal_state_fraction": stressed_fraction,
                "evidence_label": "one_day_candidate_not_promotable",
            }
        ]
    )


def _total_return_from_bins(group: pd.DataFrame) -> float:
    mids = pd.concat([group["first_mid"], group["last_mid"]], ignore_index=True)
    mids = pd.to_numeric(mids, errors="coerce")
    mids = mids[(mids > 0) & mids.notna()]
    if len(mids) < 2:
        return np.nan
    return float((mids.iloc[-1] / mids.iloc[0]) - 1.0)


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


def write_report(output_dir: Path, daily: pd.DataFrame, intraday: pd.DataFrame, ticker_states: pd.DataFrame) -> None:
    state_counts = intraday["intraday_state"].value_counts().rename_axis("intraday_state").reset_index(name="bins")
    ticker_counts = ticker_states["ticker_state"].value_counts().rename_axis("ticker_state").reset_index(name="symbols")
    lines = [
        "# Phase 3 Regime Taxonomy Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase assigns one-day candidate daily, intraday and ticker-specific regime labels.",
        "Labels are engineering inputs for scenario design, not statistically validated regime claims.",
        "",
        "## Daily Candidate",
        "",
        _markdown_table(daily),
        "",
        "## Intraday State Counts",
        "",
        _markdown_table(state_counts),
        "",
        "## Ticker-State Counts",
        "",
        _markdown_table(ticker_counts),
        "",
        "## Outputs",
        "",
        "- `daily_regime_observation.csv`",
        "- `intraday_market_states.csv`",
        "- `ticker_state_profile.csv`",
        "- `symbol_intraday_features.csv`",
        "- `regime_manifest.json`",
        "",
    ]
    (output_dir / "phase3_regime_taxonomy_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase3(phase1_dir: Path, phase2_dir: Path, output_dir: Path, bin_ms: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = load_symbol_tables(phase1_dir)
    features: list[pd.DataFrame] = []
    for index, (symbol, normalized, deltas) in enumerate(tables, start=1):
        print(f"[phase3] binning {index}/{len(tables)} {symbol}", flush=True)
        features.append(symbol_bin_features(symbol, normalized, deltas, bin_ms))
    symbol_bins = pd.concat(features, ignore_index=True).sort_values(["bin_id", "symbol"])
    intraday = build_intraday_states(symbol_bins)
    ticker_states = classify_ticker_states(symbol_bins, intraday)
    daily = classify_daily_regime(symbol_bins, intraday, phase2_dir)

    daily.to_csv(output_dir / "daily_regime_observation.csv", index=False)
    intraday.to_csv(output_dir / "intraday_market_states.csv", index=False)
    ticker_states.to_csv(output_dir / "ticker_state_profile.csv", index=False)
    symbol_bins.to_csv(output_dir / "symbol_intraday_features.csv", index=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "phase1_dir": str(phase1_dir),
        "phase2_dir": str(phase2_dir),
        "symbols": int(symbol_bins["symbol"].nunique()),
        "bin_ms": int(bin_ms),
        "intraday_bins": int(intraday.shape[0]),
        "symbol_bin_rows": int(symbol_bins.shape[0]),
        "evidence_scope": "one_day_candidate_taxonomy",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase3",
            generated_utc=generated_utc,
            inputs={"phase1_dir": str(phase1_dir), "phase2_dir": str(phase2_dir)},
            parameters={"bin_ms": int(bin_ms), "taxonomy_scope": manifest["evidence_scope"]},
            outputs={
                "daily_regime_observation": str(output_dir / "daily_regime_observation.csv"),
                "intraday_market_states": str(output_dir / "intraday_market_states.csv"),
                "ticker_state_profile": str(output_dir / "ticker_state_profile.csv"),
                "symbol_intraday_features": str(output_dir / "symbol_intraday_features.csv"),
                "report": str(output_dir / "phase3_regime_report.md"),
            },
            random_seed="not_applicable_deterministic_regime_taxonomy",
            scenario_ids="one_day_candidate_taxonomy_bins",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="not_applicable_no_latency_model",
        )
    )
    (output_dir / "regime_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, daily, intraday, ticker_states)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 3 one-day regime taxonomy.")
    parser.add_argument("--phase1-dir", type=Path, default=Path("outputs/phase1"))
    parser.add_argument("--phase2-dir", type=Path, default=Path("outputs/phase2"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase3"))
    parser.add_argument("--bin-ms", type=int, default=300000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase3(args.phase1_dir, args.phase2_dir, args.output_dir, args.bin_ms)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


LEVELS = range(1, 6)


def load_inputs(phase7_dir: Path, phase8_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    shocks = pd.read_csv(phase7_dir / "shock_library.csv")
    feed = pq.read_table(phase8_dir / "retail_feed_observations.parquet").to_pandas()
    dropped = pd.read_csv(phase8_dir / "retail_feed_dropped_events.csv")
    return shocks, feed, dropped


def build_tier_a(shocks: pd.DataFrame, feed: pd.DataFrame, dropped: pd.DataFrame) -> pd.DataFrame:
    shock_events = shocks.copy()
    shock_events["event_source"] = "phase7_shock_library"
    shock_events["event_kind"] = "shock_definition"
    shock_events["event_ts"] = shock_events["trade_date"].astype(str) + "T" + shock_events["start_time"].astype(str)
    shock_events["symbol"] = shock_events["target"]
    shock_events["feed_profile"] = "scenario_definition"
    shock_events["source_sequence"] = np.arange(len(shock_events), dtype=np.int64)

    feed_events = feed[
        [
            "feed_profile",
            "quarter_profile",
            "scenario_day",
            "trade_date",
            "symbol",
            "bar_index",
            "collector_received_utc",
            "collector_received_utc_ms",
            "source_sequence",
            "receive_sequence",
            "book_event_label",
            "regime_code",
            "is_duplicate",
            "is_disconnect_gap",
            "is_out_of_order_injected",
        ]
    ].copy()
    feed_events["event_source"] = "phase8_retail_feed"
    feed_events["event_kind"] = np.where(feed_events["is_duplicate"], "duplicate_l2_state", "received_l2_state")
    feed_events["event_ts"] = feed_events["collector_received_utc"]
    feed_events["scope"] = "ticker"
    feed_events["target"] = feed_events["symbol"]
    feed_events["variant"] = "observed_feed_profile"
    feed_events["shock_type"] = feed_events["book_event_label"]
    feed_events["required_l2_effects"] = ""

    dropped_events = dropped.copy()
    if len(dropped_events):
        dropped_events["event_source"] = "phase8_retail_feed"
        dropped_events["event_kind"] = "dropped_l2_state"
        dropped_events["event_ts"] = dropped_events["trade_date"].astype(str)
        dropped_events["scope"] = "ticker"
        dropped_events["target"] = dropped_events["symbol"]
        dropped_events["variant"] = "dropped_by_profile"
        dropped_events["shock_type"] = dropped_events["drop_reason"]
        dropped_events["required_l2_effects"] = ""
        dropped_events["receive_sequence"] = pd.NA
        dropped_events["collector_received_utc"] = pd.NA
        dropped_events["collector_received_utc_ms"] = pd.NA
        dropped_events["book_event_label"] = pd.NA
        dropped_events["regime_code"] = pd.NA
        dropped_events["is_duplicate"] = False
        dropped_events["is_disconnect_gap"] = False
        dropped_events["is_out_of_order_injected"] = False

    common = [
        "event_source",
        "event_kind",
        "event_ts",
        "feed_profile",
        "quarter_profile",
        "scenario_day",
        "trade_date",
        "symbol",
        "scope",
        "target",
        "variant",
        "shock_type",
        "required_l2_effects",
        "regime_code",
        "source_sequence",
        "receive_sequence",
        "collector_received_utc_ms",
        "book_event_label",
        "is_duplicate",
        "is_disconnect_gap",
        "is_out_of_order_injected",
    ]
    frames = [shock_events.reindex(columns=common), feed_events.reindex(columns=common)]
    if len(dropped_events):
        frames.append(dropped_events.reindex(columns=common))
    out = pd.concat(frames, ignore_index=True)
    out["event_id"] = np.arange(len(out), dtype=np.int64)
    return out[["event_id", *common]]


def build_tier_b(feed: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "feed_profile",
        "quarter_profile",
        "scenario_day",
        "trade_date",
        "bar_index",
        "bar_start",
        "symbol",
        "regime_code",
        "regime_family",
        "collector_received_utc",
        "collector_received_utc_ms",
        "receive_sequence",
        "source_sequence",
        "mid_price",
        "tick_size",
        "spread_ticks",
        "spread",
        "book_event_label",
        "event_intensity_proxy",
        "is_market_shock_day",
        "is_symbol_shock",
        "is_shock_day_from_library",
        "is_duplicate",
        "is_disconnect_gap",
        "is_out_of_order_injected",
    ]
    for level in LEVELS:
        cols.extend(
            [
                f"bid_px_{level}",
                f"ask_px_{level}",
                f"bid_qty_{level}",
                f"ask_qty_{level}",
                f"bid_orders_{level}",
                f"ask_orders_{level}",
            ]
        )
    tier_b = feed[cols].copy()
    tier_b["l1_imbalance"] = (tier_b["bid_qty_1"] - tier_b["ask_qty_1"]) / (tier_b["bid_qty_1"] + tier_b["ask_qty_1"]).replace(0, np.nan)
    bid_l5 = sum(tier_b[f"bid_qty_{level}"] for level in LEVELS)
    ask_l5 = sum(tier_b[f"ask_qty_{level}"] for level in LEVELS)
    tier_b["l5_imbalance"] = (bid_l5 - ask_l5) / (bid_l5 + ask_l5).replace(0, np.nan)
    tier_b["microprice_l1"] = (
        tier_b["ask_px_1"] * tier_b["bid_qty_1"] + tier_b["bid_px_1"] * tier_b["ask_qty_1"]
    ) / (tier_b["bid_qty_1"] + tier_b["ask_qty_1"]).replace(0, np.nan)
    return tier_b


def build_tier_c(tier_b: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["feed_profile", "quarter_profile", "scenario_day", "trade_date", "symbol"]
    ordered = tier_b.sort_values([*group_cols, "collector_received_utc_ms", "receive_sequence"], kind="mergesort")
    grouped = ordered.groupby(group_cols, sort=False)
    ordered["mid_return_1"] = grouped["mid_price"].pct_change()
    ordered["future_mid_return_1"] = grouped["mid_price"].shift(-1) / ordered["mid_price"] - 1.0
    bid_delta = sum(grouped[f"bid_qty_{level}"].diff().fillna(0) for level in LEVELS)
    ask_delta = sum(grouped[f"ask_qty_{level}"].diff().fillna(0) for level in LEVELS)
    ordered["mlofi_qty"] = bid_delta - ask_delta
    ordered["momentum_3"] = ordered["mid_price"] / grouped["mid_price"].shift(3) - 1.0
    ordered["local_volatility_6"] = grouped["mid_return_1"].rolling(6, min_periods=2).std().reset_index(level=list(range(len(group_cols))), drop=True)
    ordered["book_slope_l5"] = ((ordered["bid_px_1"] - ordered["bid_px_5"]) + (ordered["ask_px_5"] - ordered["ask_px_1"])) / 2.0
    ordered["book_convexity_l5"] = (
        ordered["bid_qty_1"] + ordered["bid_qty_2"] + ordered["ask_qty_1"] + ordered["ask_qty_2"]
    ) / (ordered["bid_qty_4"] + ordered["bid_qty_5"] + ordered["ask_qty_4"] + ordered["ask_qty_5"]).replace(0, np.nan)
    return ordered[
        [
            "feed_profile",
            "quarter_profile",
            "scenario_day",
            "trade_date",
            "bar_index",
            "symbol",
            "collector_received_utc_ms",
            "regime_code",
            "mid_price",
            "spread_ticks",
            "spread",
            "l1_imbalance",
            "l5_imbalance",
            "microprice_l1",
            "mlofi_qty",
            "momentum_3",
            "local_volatility_6",
            "book_slope_l5",
            "book_convexity_l5",
            "event_intensity_proxy",
            "is_market_shock_day",
            "is_symbol_shock",
            "is_duplicate",
            "is_disconnect_gap",
            "is_out_of_order_injected",
            "mid_return_1",
            "future_mid_return_1",
        ]
    ].reset_index(drop=True)


def build_tier_d_resampled(tier_c: pd.DataFrame, source_interval_minutes: int = 5, target_interval_minutes: int = 15) -> pd.DataFrame:
    if target_interval_minutes % source_interval_minutes != 0:
        raise ValueError("target_interval_minutes must be a multiple of source_interval_minutes")
    bars_per_panel = target_interval_minutes // source_interval_minutes
    group_cols = ["feed_profile", "quarter_profile", "scenario_day", "trade_date", "symbol"]
    ordered = tier_c.sort_values([*group_cols, "bar_index", "collector_received_utc_ms"], kind="mergesort").copy()
    ordered["resample_bar_index"] = (ordered["bar_index"] // bars_per_panel).astype("int64")
    ordered["source_interval_minutes"] = source_interval_minutes
    ordered["target_interval_minutes"] = target_interval_minutes
    resample_cols = [*group_cols, "resample_bar_index"]
    out = (
        ordered.groupby(resample_cols, sort=False)
        .agg(
            source_rows=("bar_index", "count"),
            source_bar_start=("bar_index", "min"),
            source_bar_end=("bar_index", "max"),
            collector_received_utc_ms_start=("collector_received_utc_ms", "min"),
            collector_received_utc_ms_end=("collector_received_utc_ms", "max"),
            mid_price_open=("mid_price", "first"),
            mid_price_high=("mid_price", "max"),
            mid_price_low=("mid_price", "min"),
            mid_price_close=("mid_price", "last"),
            spread_ticks_mean=("spread_ticks", "mean"),
            spread_ticks_max=("spread_ticks", "max"),
            spread_mean=("spread", "mean"),
            l1_imbalance_mean=("l1_imbalance", "mean"),
            l5_imbalance_mean=("l5_imbalance", "mean"),
            microprice_l1_close=("microprice_l1", "last"),
            mlofi_qty_sum=("mlofi_qty", "sum"),
            momentum_3_close=("momentum_3", "last"),
            local_volatility_6_mean=("local_volatility_6", "mean"),
            book_slope_l5_mean=("book_slope_l5", "mean"),
            book_convexity_l5_mean=("book_convexity_l5", "mean"),
            event_intensity_proxy_mean=("event_intensity_proxy", "mean"),
            duplicate_rows=("is_duplicate", "sum"),
            disconnect_gap_rows=("is_disconnect_gap", "sum"),
            out_of_order_rows=("is_out_of_order_injected", "sum"),
            is_market_shock_day=("is_market_shock_day", "max"),
            is_symbol_shock=("is_symbol_shock", "max"),
        )
        .reset_index()
    )
    out["source_interval_minutes"] = source_interval_minutes
    out["target_interval_minutes"] = target_interval_minutes
    out["mid_return_panel"] = out["mid_price_close"] / out["mid_price_open"].replace(0, np.nan) - 1.0
    out["panel_complete"] = out["source_rows"] == bars_per_panel
    grouped = out.sort_values([*group_cols, "resample_bar_index"], kind="mergesort").groupby(group_cols, sort=False)
    out["future_mid_return_panel_1"] = grouped["mid_price_close"].shift(-1) / out["mid_price_close"].replace(0, np.nan) - 1.0
    return out.reset_index(drop=True)


def summarize_resampled(tier_d: pd.DataFrame) -> pd.DataFrame:
    return (
        tier_d.groupby(["feed_profile", "target_interval_minutes"], sort=True)
        .agg(
            rows=("symbol", "count"),
            symbols=("symbol", "nunique"),
            trade_dates=("trade_date", "nunique"),
            scenario_days=("scenario_day", "nunique"),
            complete_panels=("panel_complete", "sum"),
            incomplete_panels=("panel_complete", lambda values: int((~values.astype(bool)).sum())),
            mean_source_rows=("source_rows", "mean"),
            median_spread_ticks=("spread_ticks_mean", "median"),
            mean_event_intensity=("event_intensity_proxy_mean", "mean"),
        )
        .reset_index()
    )


def validate_products(tier_a: pd.DataFrame, tier_b: pd.DataFrame, tier_c: pd.DataFrame, tier_d: pd.DataFrame) -> dict:
    return {
        "tier_a_events": int(len(tier_a)),
        "tier_a_event_kinds": int(tier_a["event_kind"].nunique()),
        "tier_b_rows": int(len(tier_b)),
        "tier_b_profiles": int(tier_b["feed_profile"].nunique()),
        "tier_b_symbols": int(tier_b["symbol"].nunique()),
        "tier_c_rows": int(len(tier_c)),
        "tier_c_profiles": int(tier_c["feed_profile"].nunique()),
        "tier_c_symbols": int(tier_c["symbol"].nunique()),
        "tier_c_future_label_nulls": int(tier_c["future_mid_return_1"].isna().sum()),
        "tier_b_crossed_l1_rows": int((tier_b["bid_px_1"] >= tier_b["ask_px_1"]).sum()),
        "tier_d_resampled_rows": int(len(tier_d)),
        "tier_d_resampled_profiles": int(tier_d["feed_profile"].nunique()),
        "tier_d_resampled_symbols": int(tier_d["symbol"].nunique()),
        "tier_d_target_interval_minutes": int(tier_d["target_interval_minutes"].max()) if len(tier_d) else 0,
        "tier_d_incomplete_panels": int((~tier_d["panel_complete"]).sum()) if len(tier_d) else 0,
    }


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


def write_report(output_dir: Path, validation: dict, tier_a: pd.DataFrame, tier_b: pd.DataFrame, resampled_summary: pd.DataFrame) -> None:
    event_kinds = tier_a["event_kind"].value_counts().rename_axis("event_kind").reset_index(name="rows")
    profiles = tier_b.groupby("feed_profile", sort=True).agg(rows=("symbol", "count"), symbols=("symbol", "nunique")).reset_index()
    lines = [
        "# Phase 9 Data Products Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase assembles formal Tier A/B/C/D synthetic data products from Phase 7 and Phase 8 outputs.",
        "Tier D is a deterministic 15-minute resampled feature panel derived from the current Tier C 5-minute feature product.",
        "",
        "## Validation",
        "",
        *(f"- {key}: {value}" for key, value in validation.items()),
        "",
        "## Tier A Event Kinds",
        "",
        _markdown_table(event_kinds),
        "",
        "## Tier B Profiles",
        "",
        _markdown_table(profiles),
        "",
        "## Tier D Resampled 15-Minute Summary",
        "",
        _markdown_table(resampled_summary),
        "",
        "## Outputs",
        "",
        "- `tier_a/raw_synthetic_events.parquet`",
        "- `tier_b/compact_l2_state.parquet`",
        "- `tier_c/features_5m.parquet`",
        "- `tier_d/resampled_features_15m.parquet`",
        "- `tier_d/resampled_panel_summary.csv`",
        "- `data_product_manifest.json`",
        "",
    ]
    (output_dir / "phase9_data_products_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase9(phase7_dir: Path, phase8_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    tier_a_dir = output_dir / "tier_a"
    tier_b_dir = output_dir / "tier_b"
    tier_c_dir = output_dir / "tier_c"
    tier_d_dir = output_dir / "tier_d"
    tier_a_dir.mkdir(exist_ok=True)
    tier_b_dir.mkdir(exist_ok=True)
    tier_c_dir.mkdir(exist_ok=True)
    tier_d_dir.mkdir(exist_ok=True)

    shocks, feed, dropped = load_inputs(phase7_dir, phase8_dir)
    print("[phase9] building Tier A", flush=True)
    tier_a = build_tier_a(shocks, feed, dropped)
    print("[phase9] building Tier B", flush=True)
    tier_b = build_tier_b(feed)
    print("[phase9] building Tier C", flush=True)
    tier_c = build_tier_c(tier_b)
    print("[phase9] building Tier D resampled panel", flush=True)
    tier_d = build_tier_d_resampled(tier_c)
    resampled_summary = summarize_resampled(tier_d)
    validation = validate_products(tier_a, tier_b, tier_c, tier_d)

    pq.write_table(pa.Table.from_pandas(tier_a, preserve_index=False), tier_a_dir / "raw_synthetic_events.parquet", compression="zstd")
    pq.write_table(pa.Table.from_pandas(tier_b, preserve_index=False), tier_b_dir / "compact_l2_state.parquet", compression="zstd")
    pq.write_table(pa.Table.from_pandas(tier_c, preserve_index=False), tier_c_dir / "features_5m.parquet", compression="zstd")
    pq.write_table(pa.Table.from_pandas(tier_d, preserve_index=False), tier_d_dir / "resampled_features_15m.parquet", compression="zstd")
    resampled_summary.to_csv(tier_d_dir / "resampled_panel_summary.csv", index=False)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "phase7_dir": str(phase7_dir),
        "phase8_dir": str(phase8_dir),
        "products": {
            "tier_a": "raw synthetic events and feed lifecycle events",
            "tier_b": "compact received L2 state stream",
            "tier_c": "5-minute feature and future-return label dataset",
            "tier_d": "15-minute resampled feature panel derived from Tier C",
        },
        "validation": validation,
        "resampled_product": {
            "source_tier": "tier_c",
            "source_interval_minutes": 5,
            "target_interval_minutes": 15,
            "path": str(tier_d_dir / "resampled_features_15m.parquet"),
            "summary_path": str(tier_d_dir / "resampled_panel_summary.csv"),
        },
        "evidence_scope": "synthetic_data_products_v1",
    }
    (output_dir / "data_product_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, validation, tier_a, tier_b, resampled_summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 9 synthetic data product tiers.")
    parser.add_argument("--phase7-dir", type=Path, default=Path("outputs/phase7"))
    parser.add_argument("--phase8-dir", type=Path, default=Path("outputs/phase8"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase9"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase9(args.phase7_dir, args.phase8_dir, args.output_dir)


if __name__ == "__main__":
    main()

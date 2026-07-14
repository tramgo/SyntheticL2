from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


PARTIAL_STRATEGIES = ["S03", "S04", "S06", "S08"]
ACTIVE_WINDOW_START = "09:15:00"
ACTIVE_WINDOW_END = "15:30:00"


def load_received_deltas(input_root: Path) -> pd.DataFrame:
    paths = sorted(input_root.glob("symbol=*/received_tick_deltas.parquet"))
    if not paths:
        raise FileNotFoundError(f"No received_tick_deltas parquet files under {input_root}")
    frames = []
    columns = [
        "trading_date",
        "event_ts_receive",
        "event_ts_receive_ms",
        "symbol",
        "sequence_local",
        "ltp",
        "cum_volume",
        "spread",
        "spread_ticks",
        "mid_price",
        "microprice_l1",
        "book_valid",
        "elapsed_ms",
        "mid_change",
        "microprice_change",
        "spread_change",
        "cum_volume_increment",
        "stale_gap_gt_5s",
        "stale_gap_gt_15s",
        "l1_imbalance",
        "l5_imbalance",
        "mlofi_qty",
        "inferred_depth_withdrawal",
        "inferred_depth_replenishment",
        "inference_confidence",
        "aggressor_side_inference",
        "book_slope_l5",
        "book_convexity_l5",
        "local_volatility_20_ticks",
    ]
    for path in paths:
        table = pq.ParquetFile(path).read(columns=columns)
        frames.append(table.to_pandas())
    frame = pd.concat(frames, ignore_index=True)
    frame["event_ts_receive"] = pd.to_datetime(frame["event_ts_receive"], utc=True, errors="coerce")
    frame = frame.sort_values(["symbol", "event_ts_receive_ms", "sequence_local"], kind="mergesort").reset_index(drop=True)
    return frame


def enrich_labels(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy()
    grouped = data.groupby("symbol", sort=False)
    data["next_mid_1"] = grouped["mid_price"].shift(-1)
    data["next_mid_3"] = grouped["mid_price"].shift(-3)
    data["future_return_1"] = data["next_mid_1"] / data["mid_price"] - 1.0
    data["future_return_3"] = data["next_mid_3"] / data["mid_price"] - 1.0
    data["active_market_window"] = data["event_ts_receive"].dt.tz_convert("Asia/Kolkata").dt.strftime("%H:%M:%S").between(ACTIVE_WINDOW_START, ACTIVE_WINDOW_END)
    data["usable_short_horizon"] = (
        data["book_valid"].astype(bool)
        & data["active_market_window"].astype(bool)
        & ~data["stale_gap_gt_5s"].astype(bool)
        & ~data["stale_gap_gt_15s"].astype(bool)
        & data["mid_price"].gt(0)
        & data["next_mid_1"].notna()
    )
    data["trade_side_sign"] = (
        data["aggressor_side_inference"]
        .map({"buy": 1, "sell": -1, "buy_pressure_weak": 1, "sell_pressure_weak": -1})
        .fillna(0)
        .astype("int8")
    )
    data["mlofi_sign"] = np.sign(data["mlofi_qty"].fillna(0)).astype("int8")
    data["l1_sign"] = np.sign(data["l1_imbalance"].fillna(0)).astype("int8")
    data["l5_sign"] = np.sign(data["l5_imbalance"].fillna(0)).astype("int8")

    spread_widening = data["spread_change"].fillna(0).gt(0)
    spread_normalizing = data["spread_change"].fillna(0).lt(0)
    low_realized_move = data["mid_change"].abs().fillna(0).le(data["inferred_tick_size"] if "inferred_tick_size" in data.columns else 0.05)
    volume_event = data["cum_volume_increment"].fillna(0).gt(0)

    data["s03_liquidity_vacuum_proxy"] = (
        data["usable_short_horizon"]
        & data["inferred_depth_withdrawal"].astype(bool)
        & spread_widening
        & data["local_volatility_20_ticks"].fillna(0).gt(data["local_volatility_20_ticks"].median())
    )
    data["s03_reversal_candidate_proxy"] = data["s03_liquidity_vacuum_proxy"] & spread_normalizing.shift(-1).fillna(False)
    data["s04_trade_flow_depth_confirm_proxy"] = (
        data["usable_short_horizon"]
        & volume_event
        & data["trade_side_sign"].ne(0)
        & (data["trade_side_sign"] == data["mlofi_sign"])
        & (data["trade_side_sign"] == data["l5_sign"])
    )
    data["s06_absorption_like_proxy"] = (
        data["usable_short_horizon"]
        & volume_event
        & data["trade_side_sign"].ne(0)
        & data["inferred_depth_replenishment"].astype(bool)
        & low_realized_move
    )
    data["s06_absorption_side"] = np.where(data["s06_absorption_like_proxy"], data["trade_side_sign"], 0).astype("int8")
    return data


def lead_lag_panel(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    usable = data[data["usable_short_horizon"]].copy()
    usable["bucket_5s"] = (usable["event_ts_receive_ms"].astype("int64") // 5000) * 5000
    symbol_bucket = (
        usable.groupby(["bucket_5s", "symbol"], sort=True)
        .agg(
            symbol_mlofi=("mlofi_qty", "sum"),
            symbol_return=("mid_change", "sum"),
            symbol_events=("symbol", "size"),
        )
        .reset_index()
    )
    market_bucket = symbol_bucket.groupby("bucket_5s", sort=True).agg(market_mlofi=("symbol_mlofi", "sum"), market_events=("symbol_events", "sum")).reset_index()
    merged = symbol_bucket.merge(market_bucket, on="bucket_5s", how="left")
    merged["ex_self_market_mlofi"] = merged["market_mlofi"] - merged["symbol_mlofi"]
    merged = merged.sort_values(["symbol", "bucket_5s"], kind="mergesort")
    grouped = merged.groupby("symbol", sort=False)
    merged["future_symbol_return_1_bucket"] = grouped["symbol_return"].shift(-1)
    merged["s08_lead_lag_proxy"] = merged["ex_self_market_mlofi"].ne(0) & merged["future_symbol_return_1_bucket"].notna()

    rows = []
    for symbol, group in merged.groupby("symbol", sort=True):
        eligible = group[group["s08_lead_lag_proxy"]].copy()
        if len(eligible) >= 10 and eligible["ex_self_market_mlofi"].std() > 0 and eligible["future_symbol_return_1_bucket"].std() > 0:
            corr = float(eligible["ex_self_market_mlofi"].corr(eligible["future_symbol_return_1_bucket"]))
        else:
            corr = np.nan
        rows.append(
            {
                "symbol": symbol,
                "lead_lag_bucket_rows": int(len(eligible)),
                "lead_lag_abs_corr_proxy": abs(corr) if pd.notna(corr) else np.nan,
                "lead_lag_corr_proxy": corr,
                "s08_proxy_available": bool(len(eligible) >= 10 and pd.notna(corr)),
                "acceptance_grade": False,
                "limitation": "One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized.",
            }
        )
    return merged, pd.DataFrame(rows)


def event_label_summary(data: pd.DataFrame, lead_lag_summary: pd.DataFrame) -> pd.DataFrame:
    grouped = data.groupby("symbol", sort=True)
    rows = []
    for symbol, group in grouped:
        ll = lead_lag_summary[lead_lag_summary["symbol"].eq(symbol)]
        rows.append(
            {
                "symbol": symbol,
                "rows": int(len(group)),
                "usable_short_horizon_rows": int(group["usable_short_horizon"].sum()),
                "s03_liquidity_vacuum_proxy_rows": int(group["s03_liquidity_vacuum_proxy"].sum()),
                "s03_reversal_candidate_proxy_rows": int(group["s03_reversal_candidate_proxy"].sum()),
                "s04_trade_flow_depth_confirm_rows": int(group["s04_trade_flow_depth_confirm_proxy"].sum()),
                "s06_absorption_like_proxy_rows": int(group["s06_absorption_like_proxy"].sum()),
                "s08_lead_lag_bucket_rows": int(ll["lead_lag_bucket_rows"].iloc[0]) if len(ll) else 0,
                "medium_confidence_rows": int(group["inference_confidence"].astype(str).eq("medium").sum()),
                "low_confidence_rows": int(group["inference_confidence"].astype(str).eq("low").sum()),
                "stale_gap_gt_5s_rows": int(group["stale_gap_gt_5s"].sum()),
                "acceptance_grade": False,
            }
        )
    return pd.DataFrame(rows)


def feature_label_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "strategy_id": "S03",
                "feature_label": "liquidity_vacuum_reversal_proxy",
                "required_inputs": "depth withdrawal, spread widening/normalization, local volatility, future mid move",
                "current_support": "proxy_feature_available",
                "acceptance_blocker": "market-by-price feed cannot prove hidden liquidity, exact queue state or true cause of withdrawal/reversal",
            },
            {
                "strategy_id": "S04",
                "feature_label": "trade_flow_depth_confirmation_proxy",
                "required_inputs": "volume increment, weak aggressor side, MLOFI sign, L5 imbalance sign",
                "current_support": "proxy_feature_available",
                "acceptance_blocker": "aggressor side is weakly inferred and not exchange-confirmed",
            },
            {
                "strategy_id": "S06",
                "feature_label": "absorption_like_replenishment_proxy",
                "required_inputs": "volume increment, weak aggressor side, visible replenishment, low realized mid move",
                "current_support": "proxy_feature_available",
                "acceptance_blocker": "cannot distinguish iceberg/absorption from ordinary market-by-price aggregation and replenishment",
            },
            {
                "strategy_id": "S08",
                "feature_label": "cross_symbol_lead_lag_mlofi_proxy",
                "required_inputs": "5s receive bucket, symbol MLOFI, ex-self market MLOFI, next-bucket return",
                "current_support": "proxy_feature_available",
                "acceptance_blocker": "one-day receive-time correlation is not causal lead-lag and needs multi-day timestamp-skew/common-shock controls",
            },
        ]
    )


def strategy_support_summary(label_summary: pd.DataFrame, lead_lag_summary: pd.DataFrame) -> pd.DataFrame:
    total_symbols = int(label_summary["symbol"].nunique())
    rows = []
    specs = [
        ("S03", "s03_liquidity_vacuum_proxy_rows", "liquidity vacuum/reversal"),
        ("S04", "s04_trade_flow_depth_confirm_rows", "trade-flow plus depth confirmation"),
        ("S06", "s06_absorption_like_proxy_rows", "absorption-like replenishment"),
    ]
    for strategy_id, column, label in specs:
        symbols_with_proxy = int((label_summary[column] > 0).sum())
        proxy_rows = int(label_summary[column].sum())
        rows.append(
            {
                "strategy_id": strategy_id,
                "feature_label_family": label,
                "proxy_rows": proxy_rows,
                "symbols_with_proxy": symbols_with_proxy,
                "symbols_evaluated": total_symbols,
                "support_upgrade_status": "partial_proxy_feature_engineered" if proxy_rows > 0 else "still_missing_proxy_feature",
                "acceptance_ready": False,
                "required_next_evidence": "multi-day Class B labels, common-shock controls, broker/exchange fill/cost reconciliation and acceptance replay",
            }
        )
    s08_symbols = int(lead_lag_summary["s08_proxy_available"].sum()) if len(lead_lag_summary) else 0
    s08_rows = int(lead_lag_summary["lead_lag_bucket_rows"].sum()) if len(lead_lag_summary) else 0
    rows.append(
        {
            "strategy_id": "S08",
            "feature_label_family": "cross-symbol/index lead-lag OFI",
            "proxy_rows": s08_rows,
            "symbols_with_proxy": s08_symbols,
            "symbols_evaluated": total_symbols,
            "support_upgrade_status": "partial_proxy_feature_engineered" if s08_rows > 0 else "still_missing_proxy_feature",
            "acceptance_ready": False,
            "required_next_evidence": "multi-day lead-lag stability, timestamp-skew tests, simultaneous-shock controls and out-of-sample acceptance replay",
        }
    )
    return pd.DataFrame(rows)


def overall_summary(data: pd.DataFrame, support: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"metric": "phase28_received_delta_rows", "value": int(len(data)), "description": "Received tick-delta rows scanned"},
            {"metric": "phase28_symbols_evaluated", "value": int(data["symbol"].nunique()), "description": "Symbols evaluated"},
            {"metric": "phase28_partial_strategy_families", "value": int(len(support)), "description": "Partial strategy families evaluated"},
            {"metric": "phase28_proxy_feature_engineered_families", "value": int(support["support_upgrade_status"].eq("partial_proxy_feature_engineered").sum()), "description": "Partial families with proxy feature labels now engineered"},
            {"metric": "phase28_total_proxy_label_rows", "value": int(support["proxy_rows"].sum()), "description": "Total proxy label rows or buckets across S03/S04/S06/S08"},
            {"metric": "phase28_acceptance_ready", "value": 0, "description": "Richer labels are weak market-by-price proxies, not acceptance evidence"},
        ]
    )


def write_report(output_dir: Path, overall: pd.DataFrame, catalog: pd.DataFrame, labels: pd.DataFrame, lead_lag: pd.DataFrame, support: pd.DataFrame) -> None:
    lines = [
        "# Phase 28 Richer Event Label Support",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This milestone engineers explicit proxy labels for the partial strategy families S03/S04/S06/S08 from the current received-tick delta product.",
        "All labels remain weak market-by-price inferences and are not exchange-observed order events.",
        "",
        "## Overall Summary",
        "",
        _markdown_table(overall),
        "",
        "## Strategy Support Summary",
        "",
        _markdown_table(support),
        "",
        "## Feature Label Catalog",
        "",
        _markdown_table(catalog),
        "",
        "## Event Label Summary",
        "",
        _markdown_table(labels),
        "",
        "## Lead-Lag Proxy Summary",
        "",
        _markdown_table(lead_lag),
        "",
    ]
    (output_dir / "phase28_richer_event_label_support_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase28(input_root: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw = load_received_deltas(input_root)
    enriched = enrich_labels(raw)
    lead_lag_rows, lead_lag_summary = lead_lag_panel(enriched)
    labels = event_label_summary(enriched, lead_lag_summary)
    catalog = feature_label_catalog()
    support = strategy_support_summary(labels, lead_lag_summary)
    overall = overall_summary(enriched, support)

    pq.write_table(pa.Table.from_pandas(enriched, preserve_index=False), output_dir / "richer_event_label_panel.parquet", compression="zstd")
    pq.write_table(pa.Table.from_pandas(lead_lag_rows, preserve_index=False), output_dir / "lead_lag_bucket_panel.parquet", compression="zstd")
    catalog.to_csv(output_dir / "feature_label_catalog.csv", index=False)
    labels.to_csv(output_dir / "event_label_summary.csv", index=False)
    lead_lag_summary.to_csv(output_dir / "lead_lag_proxy_summary.csv", index=False)
    support.to_csv(output_dir / "strategy_support_upgrade_summary.csv", index=False)
    overall.to_csv(output_dir / "richer_event_label_overall_summary.csv", index=False)
    write_report(output_dir, overall, catalog, labels, lead_lag_summary, support)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "received_delta_rows": int(len(enriched)),
        "symbols_evaluated": int(enriched["symbol"].nunique()),
        "partial_strategy_families": PARTIAL_STRATEGIES,
        "proxy_feature_engineered_families": int(support["support_upgrade_status"].eq("partial_proxy_feature_engineered").sum()),
        "scope": "phase28_richer_event_label_support_not_acceptance_evidence",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase28",
            generated_utc=generated_utc,
            inputs={"received_tick_deltas": str(input_root)},
            parameters={
                "partial_strategies": PARTIAL_STRATEGIES,
                "active_window_start_ist": ACTIVE_WINDOW_START,
                "active_window_end_ist": ACTIVE_WINDOW_END,
                "lead_lag_bucket_ms": 5000,
            },
            outputs={
                "richer_event_label_panel": str(output_dir / "richer_event_label_panel.parquet"),
                "lead_lag_bucket_panel": str(output_dir / "lead_lag_bucket_panel.parquet"),
                "feature_label_catalog": str(output_dir / "feature_label_catalog.csv"),
                "event_label_summary": str(output_dir / "event_label_summary.csv"),
                "lead_lag_proxy_summary": str(output_dir / "lead_lag_proxy_summary.csv"),
                "strategy_support_upgrade_summary": str(output_dir / "strategy_support_upgrade_summary.csv"),
                "overall_summary": str(output_dir / "richer_event_label_overall_summary.csv"),
                "report": str(output_dir / "phase28_richer_event_label_support_report.md"),
                "manifest": str(output_dir / "phase28_richer_event_label_support_manifest.json"),
            },
            random_seed="none_deterministic_label_rules",
            scenario_ids="current_one_day_class_b_received_tick_delta_sample",
            cost_model_version="not_applicable_feature_label_support",
            latency_model_version="receive_timestamp_bucket_5s_for_lead_lag_proxy",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase28_richer_event_label_support_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build richer event-label proxy support for partial strategy families.")
    parser.add_argument("--input-root", type=Path, default=Path("outputs/phase1/received_tick_deltas_by_symbol"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase28"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase28(args.input_root, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

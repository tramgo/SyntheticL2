from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from synthetic_l2.phase12_execution_simulator import EXECUTION_PROFILES, _zerodha_order_formula_charges
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


FORWARD_HORIZON_EVENTS = [1, 3, 6]
FEATURES = [
    ("raw_momentum_follow", "momentum_3_event", 1),
    ("raw_momentum_fade", "momentum_3_event", -1),
    ("raw_l1_imbalance_follow", "l1_imbalance", 1),
    ("raw_l1_imbalance_fade", "l1_imbalance", -1),
    ("raw_l5_imbalance_follow", "l5_imbalance", 1),
    ("raw_l5_imbalance_fade", "l5_imbalance", -1),
    ("raw_microprice_follow", "microprice_dev", 1),
    ("raw_microprice_fade", "microprice_dev", -1),
]
ABS_THRESHOLD_QUANTILES = [0.90, 0.95, 0.98]
MIN_RAW_SIGNALS_FOR_CANDIDATE = 5_000
MIN_RAW_PRECISION_LIFT_FOR_CANDIDATE = 1.20


def load_inventory(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    inventory = pd.read_csv(path)
    inventory["file_path"] = inventory["file_path"].astype(str)
    return inventory


def load_raw_ticks(inventory: pd.DataFrame) -> pd.DataFrame:
    paths = [Path(path) for path in inventory["file_path"].tolist()]
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing raw partitions: {missing[:5]}")
    columns = [
        "trade_date",
        "exchange",
        "symbol",
        "feed_profile",
        "annual_event_id",
        "callback_received_utc_ms",
        "exchange_timestamp_ms",
        "last_price",
        "last_traded_quantity",
        "volume_traded",
        "is_duplicate",
        "is_disconnect_gap",
        "is_out_of_order_injected",
    ]
    for level in range(1, 6):
        columns.extend(
            [
                f"buy_{level}_price",
                f"buy_{level}_quantity",
                f"buy_{level}_orders",
                f"sell_{level}_price",
                f"sell_{level}_quantity",
                f"sell_{level}_orders",
            ]
        )
    tables = [pq.ParquetFile(path).read(columns=columns) for path in paths]
    table = pa.concat_tables(tables, promote_options="default")
    ticks = table.to_pandas()
    return ticks.sort_values(["feed_profile", "trade_date", "symbol", "annual_event_id"], kind="mergesort").reset_index(drop=True)


def reconstruct_features(raw: pd.DataFrame) -> pd.DataFrame:
    out = raw.copy()
    out["best_bid"] = out["buy_1_price"].astype(float)
    out["best_ask"] = out["sell_1_price"].astype(float)
    out["mid_price"] = (out["best_bid"] + out["best_ask"]) / 2.0
    out["spread"] = out["best_ask"] - out["best_bid"]
    out["l1_imbalance"] = (out["buy_1_quantity"].astype(float) - out["sell_1_quantity"].astype(float)) / (
        out["buy_1_quantity"].astype(float) + out["sell_1_quantity"].astype(float)
    ).replace(0.0, np.nan)
    bid_qty_cols = [f"buy_{level}_quantity" for level in range(1, 6)]
    ask_qty_cols = [f"sell_{level}_quantity" for level in range(1, 6)]
    bid_sum = out[bid_qty_cols].astype(float).sum(axis=1)
    ask_sum = out[ask_qty_cols].astype(float).sum(axis=1)
    out["l5_imbalance"] = (bid_sum - ask_sum) / (bid_sum + ask_sum).replace(0.0, np.nan)
    out["microprice_l1"] = (
        out["best_ask"] * out["buy_1_quantity"].astype(float)
        + out["best_bid"] * out["sell_1_quantity"].astype(float)
    ) / (out["buy_1_quantity"].astype(float) + out["sell_1_quantity"].astype(float)).replace(0.0, np.nan)
    out["microprice_dev"] = (out["microprice_l1"] - out["mid_price"]) / out["mid_price"].replace(0.0, np.nan)
    group_cols = ["feed_profile", "trade_date", "symbol"]
    grouped = out.groupby(group_cols, sort=False)
    out["next_mid_price"] = grouped["mid_price"].shift(-1)
    out["mid_return_event"] = out["mid_price"] / grouped["mid_price"].shift(1) - 1.0
    out["momentum_3_event"] = grouped["mid_return_event"].transform(lambda values: values.rolling(3, min_periods=1).sum()).fillna(0.0)
    out["next_is_bad_feed"] = (
        grouped["is_duplicate"].shift(-1).fillna(False).astype(bool)
        | grouped["is_disconnect_gap"].shift(-1).fillna(False).astype(bool)
        | grouped["is_out_of_order_injected"].shift(-1).fillna(False).astype(bool)
    )
    return out


def retail_cost_hurdle(raw_features: pd.DataFrame) -> pd.Series:
    retail = next(profile for profile in EXECUTION_PROFILES if profile["execution_profile"] == "retail_marketable_default")
    ticks = raw_features.copy()
    ticks["side"] = 1
    ticks["next_mid_price"] = ticks["next_mid_price"].fillna(ticks["mid_price"])
    charges = _zerodha_order_formula_charges(
        ticks[["symbol", "mid_price", "next_mid_price", "side"]],
        order_notional_inr=float(retail.get("order_notional_inr", 100_000.0)),
        apply_charges=True,
    )
    half_spread_return = (ticks["spread"].astype(float).clip(lower=0.0) / 2.0) / ticks["mid_price"].astype(float)
    internal = float(retail["impact_bps"]) / 10_000.0
    return half_spread_return + internal + charges["zerodha_charge_return"].astype(float)


def build_integrity_summary(inventory: pd.DataFrame, raw: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    level_checks = []
    for level in range(1, 6):
        level_checks.append(bool(raw[f"buy_{level}_price"].notna().all()))
        level_checks.append(bool(raw[f"sell_{level}_price"].notna().all()))
        level_checks.append(bool((raw[f"buy_{level}_quantity"].astype(float) > 0).all()))
        level_checks.append(bool((raw[f"sell_{level}_quantity"].astype(float) > 0).all()))
    rows = [
        ("phase46_partition_rows", int(len(inventory)), "Raw date/exchange/symbol partitions scanned"),
        ("phase46_inventory_rows", int(inventory["rows"].sum()), "Rows declared by Phase45 inventory"),
        ("phase46_raw_rows_loaded", int(len(raw)), "Raw rows loaded from partitioned parquet lake"),
        ("phase46_symbols", int(raw["symbol"].nunique()), "Symbols loaded from raw lake"),
        ("phase46_trade_dates", int(raw["trade_date"].nunique()), "Trade dates loaded from raw lake"),
        ("phase46_feed_profiles", int(raw["feed_profile"].nunique()), "Feed profiles loaded from raw lake"),
        ("phase46_l1_l5_depth_complete", int(all(level_checks)), "All L1-L5 price and quantity fields present/nonzero"),
        ("phase46_inventory_row_match", int(int(inventory["rows"].sum()) == len(raw)), "Loaded row count matches inventory"),
        ("phase46_feature_rows_reconstructed", int(len(features)), "Rows with raw-derived feature reconstruction"),
        ("phase46_mid_price_null_rows", int(features["mid_price"].isna().sum()), "Rows with missing reconstructed mid price"),
        ("phase46_synthetic_full_year_acceptance_ready", 0, "Raw-lake replay diagnostic is experiment plumbing, not acceptance"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def evaluate_raw_forward_edges(features: pd.DataFrame) -> pd.DataFrame:
    data = features.copy()
    data["retail_cost_hurdle_return"] = retail_cost_hurdle(data)
    grouped = data.groupby(["feed_profile", "trade_date", "symbol"], sort=False)["mid_price"]
    for horizon in FORWARD_HORIZON_EVENTS:
        data[f"forward_mid_return_{horizon}e"] = grouped.shift(-horizon) / data["mid_price"] - 1.0
        data[f"any_cost_clear_edge_{horizon}e"] = data[f"forward_mid_return_{horizon}e"].abs() > data["retail_cost_hurdle_return"]
    clean = ~(
        data["is_duplicate"].astype(bool)
        | data["is_disconnect_gap"].astype(bool)
        | data["is_out_of_order_injected"].astype(bool)
        | data["next_is_bad_feed"].astype(bool)
    )
    rows = []
    for thesis_id, feature_col, direction_mult in FEATURES:
        values = data[feature_col].astype(float)
        thresholds = {q: float(values.abs().replace([np.inf, -np.inf], np.nan).dropna().quantile(q)) for q in ABS_THRESHOLD_QUANTILES}
        for threshold_q, threshold in thresholds.items():
            signal = (np.sign(values) * direction_mult).where(clean & values.notna() & (values.abs() >= threshold), 0).fillna(0).astype("int8")
            for horizon in FORWARD_HORIZON_EVENTS:
                forward = data[f"forward_mid_return_{horizon}e"].astype(float)
                valid = signal.ne(0) & forward.notna()
                baseline_valid = clean & forward.notna()
                baseline_rate = float(data.loc[baseline_valid, f"any_cost_clear_edge_{horizon}e"].mean()) if bool(baseline_valid.any()) else 0.0
                if bool(valid.any()):
                    signed_forward = signal.loc[valid].astype(float) * forward.loc[valid]
                    hurdle = data.loc[valid, "retail_cost_hurdle_return"].astype(float)
                    net_edge = signed_forward - hurdle
                    precision = float((net_edge > 0).mean())
                    lift = float(precision / baseline_rate) if baseline_rate > 0 else 0.0
                    mean_net = float(net_edge.mean())
                    signals = int(valid.sum())
                else:
                    precision = 0.0
                    lift = 0.0
                    mean_net = 0.0
                    signals = 0
                rows.append(
                    {
                        "raw_label_candidate_id": f"{thesis_id}_q{int(threshold_q * 100)}_{horizon}e",
                        "thesis_id": thesis_id,
                        "feature_column": feature_col,
                        "direction_multiplier": int(direction_mult),
                        "threshold_quantile": float(threshold_q),
                        "threshold_value": threshold,
                        "forward_horizon_events": int(horizon),
                        "signals": signals,
                        "baseline_any_edge_rate": baseline_rate,
                        "directional_precision": precision,
                        "precision_lift_vs_baseline": lift,
                        "mean_net_edge_return": mean_net,
                        "candidate_for_raw_replay": bool(
                            signals >= MIN_RAW_SIGNALS_FOR_CANDIDATE
                            and mean_net > 0.0
                            and lift >= MIN_RAW_PRECISION_LIFT_FOR_CANDIDATE
                        ),
                    }
                )
    return pd.DataFrame(rows).sort_values(
        ["candidate_for_raw_replay", "mean_net_edge_return", "precision_lift_vs_baseline", "signals"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def build_replay_summary(raw_edges: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("phase46_raw_edge_candidate_rows", int(len(raw_edges)), "Raw-derived forward-edge candidates evaluated"),
        ("phase46_total_raw_edge_signals", int(raw_edges["signals"].sum()), "Total raw-derived feature-threshold signals evaluated"),
        ("phase46_raw_replay_candidate_rows", int(raw_edges["candidate_for_raw_replay"].sum()), "Raw-derived rows passing pre-replay screen"),
        ("phase46_best_raw_mean_net_edge_return", float(raw_edges["mean_net_edge_return"].max()) if len(raw_edges) else 0.0, "Best raw-derived mean net edge return"),
        ("phase46_best_raw_precision_lift_vs_baseline", float(raw_edges["precision_lift_vs_baseline"].max()) if len(raw_edges) else 0.0, "Best raw-derived precision lift"),
        ("phase46_best_raw_directional_precision", float(raw_edges["directional_precision"].max()) if len(raw_edges) else 0.0, "Best raw-derived directional precision"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 46 Raw Tick-Lake Replay Diagnostics",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase reads the Phase 45 partitioned raw websocket-like L2 lake, reconstructs event features from L1-L5 depth fields, and runs a raw-source forward-edge diagnostic.",
        "It proves the raw lake can be used as the experiment source instead of the compact Phase 42 parquet. It is not strategy acceptance evidence.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase46_raw_tick_lake_replay_diagnostics_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase46(inventory_path: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory = load_inventory(inventory_path)
    raw = load_raw_ticks(inventory)
    features = reconstruct_features(raw)
    integrity = build_integrity_summary(inventory, raw, features)
    raw_edges = evaluate_raw_forward_edges(features)
    replay_summary = build_replay_summary(raw_edges)
    feature_sample = features[
        [
            "trade_date",
            "exchange",
            "symbol",
            "feed_profile",
            "annual_event_id",
            "mid_price",
            "spread",
            "l1_imbalance",
            "l5_imbalance",
            "microprice_dev",
            "momentum_3_event",
        ]
    ].head(5_000)
    integrity.to_csv(output_dir / "raw_tick_lake_integrity_summary.csv", index=False)
    raw_edges.to_csv(output_dir / "raw_tick_lake_forward_edge_results.csv", index=False)
    replay_summary.to_csv(output_dir / "raw_tick_lake_replay_summary.csv", index=False)
    feature_sample.to_csv(output_dir / "raw_tick_lake_feature_sample.csv", index=False)
    write_report(
        output_dir,
        {
            "Integrity Summary": integrity,
            "Replay Summary": replay_summary,
            "Top Raw Forward-Edge Results": raw_edges.head(80),
            "Feature Sample": feature_sample.head(40),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase46_raw_tick_lake_replay_diagnostics_not_acceptance",
        "raw_rows_loaded": int(len(raw)),
        "raw_partitions_scanned": int(len(inventory)),
        "raw_edge_candidate_rows": int(len(raw_edges)),
        "raw_replay_candidate_rows": int(raw_edges["candidate_for_raw_replay"].sum()),
        "synthetic_full_year_acceptance_ready": 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase46",
            generated_utc=generated_utc,
            inputs={"raw_tick_lake_partition_inventory": str(inventory_path)},
            parameters={
                "source": "phase45_partitioned_raw_l2_tick_lake",
                "forward_horizon_events": FORWARD_HORIZON_EVENTS,
                "features": [row[0] for row in FEATURES],
                "threshold_quantiles": ABS_THRESHOLD_QUANTILES,
                "minimum_raw_signals_for_candidate": MIN_RAW_SIGNALS_FOR_CANDIDATE,
                "minimum_raw_precision_lift_for_candidate": MIN_RAW_PRECISION_LIFT_FOR_CANDIDATE,
                "acceptance_boundary": "raw_lake_experiment_plumbing_not_acceptance",
            },
            outputs={
                "integrity_summary": str(output_dir / "raw_tick_lake_integrity_summary.csv"),
                "forward_edge_results": str(output_dir / "raw_tick_lake_forward_edge_results.csv"),
                "replay_summary": str(output_dir / "raw_tick_lake_replay_summary.csv"),
                "feature_sample": str(output_dir / "raw_tick_lake_feature_sample.csv"),
                "report": str(output_dir / "phase46_raw_tick_lake_replay_diagnostics_report.md"),
                "manifest": str(output_dir / "phase46_raw_tick_lake_replay_diagnostics_manifest.json"),
            },
            random_seed="none_deterministic_raw_lake_replay_diagnostics",
            scenario_ids="phase45_raw_full_year_l2_tick_lake",
            cost_model_version="phase12_zerodha_equity_intraday_cost_model_retail_hurdle",
            latency_model_version="phase45_raw_callback_sequence_and_l1_l5_depth_schema",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase46_raw_tick_lake_replay_diagnostics_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run diagnostics/replay screen from the raw L2 tick lake.")
    parser.add_argument("--inventory", type=Path, default=Path("outputs/phase45/raw_tick_lake_partition_inventory.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase46"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase46(args.inventory, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

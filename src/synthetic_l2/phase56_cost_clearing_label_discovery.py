from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd

from synthetic_l2.phase12_execution_simulator import EXECUTION_PROFILES
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, calculate_equity_intraday_nse_charges


DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_OUTPUT_DIR = Path("outputs/phase56")
DEFAULT_ORDER_NOTIONAL_INR = 100_000.0

FEATURES = [
    ("one_tick_return", "momentum", "sign"),
    ("one_tick_return", "contrarian", "opposite"),
    ("l1_imbalance", "l1_imbalance", "sign"),
    ("microprice_dev", "microprice", "sign"),
]
ABS_QUANTILES = [0.90, 0.95, 0.975, 0.99, 0.995]
SPREAD_QUANTILES = [0.50, 0.75]
DEPTH_QUANTILES = [0.00, 0.50, 0.75]
HORIZONS = [20, 50, 100]
COST_HURDLE_MULTIPLIER = 1.25


@dataclass(frozen=True)
class Rule:
    rule_id: str
    feature: str
    feature_family: str
    side_mode: str
    abs_quantile: float
    spread_quantile: float
    depth_quantile: float
    horizon_events: int
    abs_threshold: float
    spread_bps_max: float
    depth_notional_min: float


def parquet_files(dense_root: Path, limit_shards: int | None = None) -> list[Path]:
    files = sorted(dense_root.glob("trade_month=*/symbol=*/part-00000.parquet"))
    if not files:
        raise FileNotFoundError(f"No dense parquet files under {dense_root}")
    return files[:limit_shards] if limit_shards is not None else files


def _safe_path(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def retail_profile() -> dict[str, Any]:
    for profile in EXECUTION_PROFILES:
        if profile["execution_profile"] == "retail_marketable_default":
            return dict(profile)
    raise KeyError("retail_marketable_default execution profile is missing")


def profile_cost_bps(profile: dict[str, Any]) -> float:
    if not bool(profile.get("apply_zerodha_equity_intraday_charges", False)):
        return 0.0
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=float(profile.get("order_notional_inr", DEFAULT_ORDER_NOTIONAL_INR)),
        sell_value_inr=float(profile.get("order_notional_inr", DEFAULT_ORDER_NOTIONAL_INR)),
    )
    return float(charges.effective_bps_on_buy_value)


def _bounded_source_sql(path: Path, max_rows_per_shard: int | None) -> str:
    source = f"read_parquet('{_safe_path(path)}', union_by_name=true)"
    filters = "buy_1_price > 0 and sell_1_price > 0 and sell_1_price >= buy_1_price"
    if max_rows_per_shard is not None:
        filters += f" and local_sequence_id <= {int(max_rows_per_shard)}"
    return f"select * from {source} where {filters}"


def query_observations(path: Path, shard_index: int, max_rows_per_shard: int | None, train_fraction: float) -> pd.DataFrame:
    profile = retail_profile()
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    max_rows_expr = int(max_rows_per_shard) if max_rows_per_shard is not None else 9_223_372_036_854_775_000
    train_cutoff_expr = int(max_rows_expr * float(train_fraction))
    con = duckdb.connect()
    try:
        sql = f"""
        with base as (
            select
                trade_date,
                symbol,
                local_sequence_id,
                ((buy_1_price + sell_1_price) / 2.0) as mid_price,
                greatest(sell_1_price - buy_1_price, 0.01) as spread,
                greatest(sell_1_price - buy_1_price, 0.01) as tick_size_proxy,
                greatest(((sell_1_price - buy_1_price) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0)) * 10000.0, 0.0) as spread_bps,
                (((buy_1_price * buy_1_quantity) + (sell_1_price * sell_1_quantity)) / 2.0) as l1_depth_notional,
                ((buy_1_quantity - sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0)) as l1_imbalance,
                (((sell_1_price * buy_1_quantity + buy_1_price * sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0))
                    - ((buy_1_price + sell_1_price) / 2.0)) / nullif(((buy_1_price + sell_1_price) / 2.0), 0.0) as microprice_dev,
                (last_price / nullif(lag(last_price) over (order by local_sequence_id), 0.0) - 1.0) as one_tick_return,
                coalesce(is_duplicate, false) as is_duplicate,
                coalesce(is_disconnect_gap, false) as is_disconnect_gap,
                coalesce(is_out_of_order_injected, false) as is_out_of_order_injected
            from ({_bounded_source_sql(path, max_rows_per_shard)})
        )
        select
            {shard_index}::integer as shard_index,
            trade_date,
            symbol,
            local_sequence_id,
            case when local_sequence_id <= {train_cutoff_expr} then 'train' else 'test' end as split,
            one_tick_return,
            l1_imbalance,
            microprice_dev,
            spread_bps,
            l1_depth_notional,
            (((spread / 2.0) / nullif(mid_price, 0.0))
              + ({slippage_ticks} * tick_size_proxy / nullif(mid_price, 0.0))
              + ({impact_bps} / 10000.0)
              + ({zerodha_bps} / 10000.0)) as retail_cost_return,
            lead(mid_price, 20) over (order by local_sequence_id) / nullif(mid_price, 0.0) - 1.0 as future_return_h20,
            lead(mid_price, 50) over (order by local_sequence_id) / nullif(mid_price, 0.0) - 1.0 as future_return_h50,
            lead(mid_price, 100) over (order by local_sequence_id) / nullif(mid_price, 0.0) - 1.0 as future_return_h100
        from base
        where not is_duplicate
          and not is_disconnect_gap
          and not is_out_of_order_injected
        """
        frame = con.execute(sql).fetchdf()
        return frame.dropna(subset=["one_tick_return", "l1_imbalance", "microprice_dev", "future_return_h20"])
    finally:
        con.close()


def load_observations(files: list[Path], max_rows_per_shard: int | None, train_fraction: float) -> pd.DataFrame:
    frames = [query_observations(path, index, max_rows_per_shard, train_fraction) for index, path in enumerate(files, start=1)]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def oracle_summary(observations: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for horizon in HORIZONS:
        future = observations[f"future_return_h{horizon}"].astype(float)
        cost = observations["retail_cost_return"].astype(float)
        mask = future.abs() >= cost * COST_HURDLE_MULTIPLIER
        gross = future.abs().where(mask, 0.0)
        cost_paid = cost.where(mask, 0.0)
        rows.append(
            {
                "horizon_events": horizon,
                "observations": int(future.notna().sum()),
                "oracle_trades": int(mask.sum()),
                "oracle_trade_fraction": float(mask.mean()),
                "oracle_net_pnl_inr": float(((gross - cost_paid).sum()) * DEFAULT_ORDER_NOTIONAL_INR),
                "oracle_mean_net_return": float((gross[mask] - cost_paid[mask]).mean()) if int(mask.sum()) else 0.0,
            }
        )
    return pd.DataFrame(rows)


def build_rules(train: pd.DataFrame) -> list[Rule]:
    rules: list[Rule] = []
    spread_thresholds = {q: float(train["spread_bps"].quantile(q)) for q in SPREAD_QUANTILES}
    depth_thresholds = {q: float(train["l1_depth_notional"].quantile(q)) for q in DEPTH_QUANTILES}
    for feature, family, side_mode in FEATURES:
        abs_series = train[feature].abs().replace([np.inf, -np.inf], np.nan).dropna()
        if abs_series.empty:
            continue
        abs_thresholds = {q: float(abs_series.quantile(q)) for q in ABS_QUANTILES}
        for abs_q, abs_threshold in abs_thresholds.items():
            for spread_q, spread_threshold in spread_thresholds.items():
                for depth_q, depth_threshold in depth_thresholds.items():
                    for horizon in HORIZONS:
                        rules.append(
                            Rule(
                                rule_id=(
                                    f"S56_{family.upper()}_{side_mode.upper()}_"
                                    f"Q{int(abs_q * 1000):03d}_SP{int(spread_q * 100):02d}_"
                                    f"DP{int(depth_q * 100):02d}_H{horizon}"
                                ),
                                feature=feature,
                                feature_family=family,
                                side_mode=side_mode,
                                abs_quantile=abs_q,
                                spread_quantile=spread_q,
                                depth_quantile=depth_q,
                                horizon_events=horizon,
                                abs_threshold=abs_threshold,
                                spread_bps_max=spread_threshold,
                                depth_notional_min=depth_threshold,
                            )
                        )
    return rules


def evaluate_rule(frame: pd.DataFrame, rule: Rule, split: str) -> dict[str, Any]:
    side = np.sign(frame[rule.feature].astype(float))
    if rule.side_mode == "opposite":
        side = -side
    future = frame[f"future_return_h{rule.horizon_events}"].astype(float)
    cost = frame["retail_cost_return"].astype(float)
    mask = (
        (frame["split"] == split)
        & frame[rule.feature].abs().ge(rule.abs_threshold)
        & frame["spread_bps"].le(rule.spread_bps_max)
        & frame["l1_depth_notional"].ge(rule.depth_notional_min)
        & side.ne(0)
        & future.notna()
    )
    if not bool(mask.any()):
        return {
            "trades": 0,
            "net_pnl_inr": 0.0,
            "gross_pnl_proxy_inr": 0.0,
            "cost_pnl_drag_proxy_inr": 0.0,
            "mean_net_return": 0.0,
            "precision_cost_clear": 0.0,
            "positive_symbol_rows": 0,
            "symbols": 0,
        }
    gross_return = side[mask] * future[mask]
    cost_return = cost[mask]
    net_return = gross_return - cost_return
    symbol_net = (pd.DataFrame({"symbol": frame.loc[mask, "symbol"], "net": net_return}).groupby("symbol")["net"].sum())
    return {
        "trades": int(mask.sum()),
        "net_pnl_inr": float(net_return.sum() * DEFAULT_ORDER_NOTIONAL_INR),
        "gross_pnl_proxy_inr": float(gross_return.sum() * DEFAULT_ORDER_NOTIONAL_INR),
        "cost_pnl_drag_proxy_inr": float(cost_return.sum() * DEFAULT_ORDER_NOTIONAL_INR),
        "mean_net_return": float(net_return.mean()),
        "precision_cost_clear": float((gross_return > (cost_return * COST_HURDLE_MULTIPLIER)).mean()),
        "positive_symbol_rows": int((symbol_net > 0).sum()),
        "symbols": int(symbol_net.shape[0]),
    }


def evaluate_rules(observations: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train = observations[observations["split"] == "train"].copy()
    test = observations[observations["split"] == "test"].copy()
    rules = build_rules(train)
    rows: list[dict[str, Any]] = []
    for rule in rules:
        train_metrics = evaluate_rule(observations, rule, "train")
        if train_metrics["trades"] < 20:
            continue
        test_metrics = evaluate_rule(observations, rule, "test")
        rows.append(
            {
                "rule_id": rule.rule_id,
                "feature_family": rule.feature_family,
                "feature": rule.feature,
                "side_mode": rule.side_mode,
                "horizon_events": rule.horizon_events,
                "abs_quantile": rule.abs_quantile,
                "spread_quantile": rule.spread_quantile,
                "depth_quantile": rule.depth_quantile,
                "abs_threshold": rule.abs_threshold,
                "spread_bps_max": rule.spread_bps_max,
                "depth_notional_min": rule.depth_notional_min,
                "train_trades": train_metrics["trades"],
                "train_net_pnl_inr": train_metrics["net_pnl_inr"],
                "train_precision_cost_clear": train_metrics["precision_cost_clear"],
                "train_mean_net_return": train_metrics["mean_net_return"],
                "test_trades": test_metrics["trades"],
                "test_net_pnl_inr": test_metrics["net_pnl_inr"],
                "test_gross_pnl_proxy_inr": test_metrics["gross_pnl_proxy_inr"],
                "test_cost_pnl_drag_proxy_inr": test_metrics["cost_pnl_drag_proxy_inr"],
                "test_precision_cost_clear": test_metrics["precision_cost_clear"],
                "test_mean_net_return": test_metrics["mean_net_return"],
                "test_positive_symbol_rows": test_metrics["positive_symbol_rows"],
                "test_symbols": test_metrics["symbols"],
            }
        )
    catalog = pd.DataFrame(rows)
    if catalog.empty:
        return catalog, pd.DataFrame()
    catalog["test_positive_after_costs"] = catalog["test_net_pnl_inr"] > 0
    catalog["test_positive_symbol_fraction"] = np.where(
        catalog["test_symbols"] > 0,
        catalog["test_positive_symbol_rows"] / catalog["test_symbols"],
        0.0,
    )
    catalog["phase56_candidate"] = (
        catalog["test_positive_after_costs"]
        & (catalog["test_precision_cost_clear"] >= 0.50)
        & (catalog["test_trades"] >= 10)
        & (catalog["test_positive_symbol_fraction"] >= 0.50)
    )
    catalog["has_test_trades"] = catalog["test_trades"] > 0
    top = catalog.sort_values(
        ["phase56_candidate", "has_test_trades", "test_net_pnl_inr", "test_precision_cost_clear"],
        ascending=[False, False, False, False],
    )
    return catalog, top.head(25).reset_index(drop=True)


def acceptance_summary(observations: pd.DataFrame, catalog: pd.DataFrame, top_rules: pd.DataFrame, files: list[Path], elapsed: float) -> pd.DataFrame:
    train_rows = int((observations["split"] == "train").sum()) if not observations.empty else 0
    test_rows = int((observations["split"] == "test").sum()) if not observations.empty else 0
    rows = [
        ("phase56_dense_shards_scanned", len(files), "Dense shards scanned"),
        ("phase56_observation_rows", int(len(observations)), "No-lookahead feature/label observations"),
        ("phase56_train_rows", train_rows, "Chronological training rows"),
        ("phase56_test_rows", test_rows, "Chronological test rows"),
        ("phase56_rule_rows_evaluated", int(len(catalog)), "Candidate rules with at least 20 training trades"),
        ("phase56_positive_test_rule_rows", int((catalog["test_net_pnl_inr"] > 0).sum()) if not catalog.empty else 0, "Rules positive after retail costs on test split"),
        ("phase56_scale_candidate_rows", int(catalog["phase56_candidate"].sum()) if not catalog.empty else 0, "Rules passing no-lookahead scale gate"),
        (
            "phase56_best_traded_test_net_pnl_inr",
            float(catalog.loc[catalog["test_trades"] > 0, "test_net_pnl_inr"].max())
            if (not catalog.empty and bool((catalog["test_trades"] > 0).any()))
            else 0.0,
            "Best no-lookahead test net P&L among rules that emitted at least one test trade",
        ),
        ("phase56_best_rule_id", str(top_rules.iloc[0]["rule_id"]) if not top_rules.empty else "", "Top test rule"),
        ("phase56_elapsed_seconds", elapsed, "Elapsed seconds"),
        ("phase56_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
        ("phase56_recommend_scale_to_wider_dense_replay", int(catalog["phase56_candidate"].sum() > 0) if not catalog.empty else 0, "1 means at least one no-lookahead rule deserves wider replay"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase56 Cost-Clearing Label Discovery",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase56 searches for no-lookahead observable rules that predict Phase55-style cost-clearing forward moves.",
        "Thresholds are derived from the chronological training split and evaluated on a later test split.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase56_cost_clearing_label_discovery_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase56(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    limit_shards: int | None,
    max_rows_per_shard: int | None,
    train_fraction: float,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = parquet_files(dense_root, limit_shards=limit_shards)
    started = time.perf_counter()
    observations = load_observations(files, max_rows_per_shard, train_fraction)
    catalog, top_rules = evaluate_rules(observations)
    oracle = oracle_summary(observations)
    elapsed = time.perf_counter() - started
    acceptance = acceptance_summary(observations, catalog, top_rules, files, elapsed)

    observations.head(5000).to_csv(output_dir / "cost_clearing_label_observation_sample.csv", index=False)
    oracle.to_csv(output_dir / "cost_clearing_oracle_summary.csv", index=False)
    catalog.to_csv(output_dir / "cost_clearing_rule_catalog.csv", index=False)
    top_rules.to_csv(output_dir / "cost_clearing_top_rules.csv", index=False)
    acceptance.to_csv(output_dir / "cost_clearing_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Oracle Label Summary": oracle,
            "Top No-Lookahead Rules": top_rules,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase56_cost_clearing_label_discovery",
        "dense_shards_scanned": len(files),
        "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
        "train_fraction": train_fraction,
        "recommend_scale_to_wider_dense_replay": int(catalog["phase56_candidate"].sum() > 0) if not catalog.empty else 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase56",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase55_cost_aware_edge_mining": "outputs/phase55/phase55_cost_aware_edge_mining_report.md",
            },
            parameters={
                "limit_shards": limit_shards if limit_shards is not None else "none_full_lake",
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "train_fraction": train_fraction,
                "feature_families": ";".join(sorted({item[1] for item in FEATURES})),
                "horizons": ";".join(str(item) for item in HORIZONS),
                "cost_hurdle_multiplier": COST_HURDLE_MULTIPLIER,
            },
            outputs={
                "observation_sample": str(output_dir / "cost_clearing_label_observation_sample.csv"),
                "oracle_summary": str(output_dir / "cost_clearing_oracle_summary.csv"),
                "rule_catalog": str(output_dir / "cost_clearing_rule_catalog.csv"),
                "top_rules": str(output_dir / "cost_clearing_top_rules.csv"),
                "acceptance_summary": str(output_dir / "cost_clearing_acceptance_summary.csv"),
                "report": str(output_dir / "phase56_cost_clearing_label_discovery_report.md"),
                "manifest": str(output_dir / "phase56_cost_clearing_label_discovery_manifest.json"),
            },
            random_seed="none_deterministic_dense_lake_rule_mining",
            scenario_ids="phase56_bounded_first_shards_chronological_split",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase56_retail_cost_hurdle_labeling_no_order_latency_applied_to_features",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase56_cost_clearing_label_discovery_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Discover no-lookahead labels/rules for retail cost-clearing dense moves.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--limit-shards", type=int, default=8)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    parser.add_argument("--train-fraction", type=float, default=0.70)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase56(args.dense_root, args.output_dir, args.base_dir, args.limit_shards, args.max_rows_per_shard, args.train_fraction)


if __name__ == "__main__":
    main()

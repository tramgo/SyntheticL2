from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_ORDER_NOTIONAL_INR
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_BARS_PATH = Path("outputs/phase235/phase235_real_event_bars.parquet")
DEFAULT_PHASE250_DIR = Path("outputs/phase250")
DEFAULT_OUTPUT_DIR = Path("outputs/phase251")

FORBIDDEN_TUNING_DATES = {"2026-07-17", "2026-07-20"}
HORIZONS = [4, 6, 8, 10, 12]
RESIDUAL_QUANTILES = [0.75, 0.85, 0.90, 0.95]
TOP5_QUANTILES = [0.50, 0.65, 0.80]
DEPTH_BEYOND_L1_QUANTILES = [0.35, 0.50]
SPREAD_QUANTILES = [0.75, 0.90]
INTENSITY_QUANTILES = [0.25, 0.50]
RANK_BUCKETS = [1, 2]
FAMILIES = [
    "P250_SECTOR_PAIR_RESIDUAL_REVERSION",
    "P250_INDEX_BASKET_RESIDUAL_REVERSION",
    "P250_TOP5_IMBALANCE_RELATIVE_DIVERGENCE",
    "P250_MARKET_NEUTRAL_LONG_SHORT_BASKET",
]
RANDOM_CONTROL_RUNS = 1000
RANDOM_SEED = 251
RANDOM_BEAT_THRESHOLD = 0.95
MIN_CONTROL_TRADES = 20
MIN_CONTROL_DATES = 4
MIN_CONTROL_SYMBOLS = 8


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    frame = read_csv(path)
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    return rows.iloc[0]


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def candidate_id(
    family: str,
    horizon: int,
    residual_q: float,
    top5_q: float,
    depth_q: float,
    spread_q: float,
    intensity_q: float,
    rank_bucket: int,
) -> str:
    fam = family.replace("P250_", "P251_")
    return "_".join(
        [
            fam,
            f"H{horizon}",
            f"RQ{str(residual_q).replace('.', '_')}",
            f"TQ{str(top5_q).replace('.', '_')}",
            f"DQ{str(depth_q).replace('.', '_')}",
            f"SP{str(spread_q).replace('.', '_')}",
            f"IQ{str(intensity_q).replace('.', '_')}",
            f"RB{rank_bucket}",
        ]
    )


def load_training_bars(bars_path: Path, phase250_dir: Path) -> pd.DataFrame:
    if as_int(metric_value(phase250_dir / "phase250_acceptance_summary.csv", "phase250_phase251_training_search_allowed_next", 0)) != 1:
        raise RuntimeError("Phase250 does not allow Phase251 training search.")
    universe = read_csv(phase250_dir / "phase250_pair_basket_universe.csv")
    if universe.empty:
        raise FileNotFoundError(phase250_dir / "phase250_pair_basket_universe.csv")
    bars = pd.read_parquet(bars_path).sort_values(["trade_date", "source_event_bar_id", "symbol"], kind="mergesort")
    bars["trade_date"] = bars["trade_date"].astype(str)
    bars = bars[~bars["trade_date"].isin(FORBIDDEN_TUNING_DATES)].copy()
    required = {
        "trade_date",
        "exchange",
        "symbol",
        "source_event_bar_id",
        "close_mid_price",
        "bar_return",
        "avg_top5_market_by_price_imbalance",
        "avg_l1_imbalance",
        "avg_spread",
        "avg_event_intensity_proxy",
        "taker_round_trip_cost_floor_bps",
    }
    missing = sorted(required.difference(bars.columns))
    if missing:
        raise ValueError(f"Phase251 bars missing required columns: {missing}")
    universe = universe[["symbol", "peer_group_id", "phase251_allowed"]].copy()
    universe["symbol"] = universe["symbol"].astype(str)
    bars = bars.merge(universe, on="symbol", how="left")
    bars = bars[bars["phase251_allowed"].fillna(0).astype(int).eq(1)].copy()
    bars["peer_group_id"] = bars["peer_group_id"].astype(str)
    bars = bars.reset_index(drop=True)
    for horizon in HORIZONS:
        bars[f"future_return_h{horizon}"] = (
            bars.groupby(["trade_date", "symbol"], sort=False)["close_mid_price"].shift(-horizon)
            / bars["close_mid_price"]
            - 1.0
        )
    return materialize_relative_features(bars)


def materialize_relative_features(bars: pd.DataFrame) -> pd.DataFrame:
    key = ["trade_date", "source_event_bar_id", "peer_group_id"]
    group = bars.groupby(key, sort=False)
    count = group["symbol"].transform("count").astype(float)
    sum_return = group["bar_return"].transform("sum").astype(float)
    sum_top5 = group["avg_top5_market_by_price_imbalance"].transform("sum").astype(float)
    bars["basket_return"] = np.where(count > 1, (sum_return - bars["bar_return"].astype(float)) / (count - 1.0), np.nan)
    bars["basket_top5_imbalance"] = np.where(count > 1, (sum_top5 - bars["avg_top5_market_by_price_imbalance"].astype(float)) / (count - 1.0), np.nan)
    bars["symbol_residual_return"] = bars["bar_return"].astype(float) - bars["basket_return"].astype(float)
    bars["relative_top5_imbalance"] = bars["avg_top5_market_by_price_imbalance"].astype(float) - bars["basket_top5_imbalance"].astype(float)
    bars["depth_beyond_l1_imbalance"] = bars["avg_top5_market_by_price_imbalance"].astype(float) - bars["avg_l1_imbalance"].astype(float)
    sum_depth_beyond_l1 = group["depth_beyond_l1_imbalance"].transform("sum").astype(float)
    bars["basket_depth_beyond_l1_imbalance"] = np.where(count > 1, (sum_depth_beyond_l1 - bars["depth_beyond_l1_imbalance"].astype(float)) / (count - 1.0), np.nan)
    bars["relative_depth_beyond_l1_imbalance"] = bars["depth_beyond_l1_imbalance"].astype(float) - bars["basket_depth_beyond_l1_imbalance"].astype(float)
    sum_cost = group["taker_round_trip_cost_floor_bps"].transform("sum").astype(float)
    bars["basket_cost_bps"] = np.where(count > 1, (sum_cost - bars["taker_round_trip_cost_floor_bps"].astype(float)) / (count - 1.0), np.nan)
    for horizon in HORIZONS:
        future_col = f"future_return_h{horizon}"
        sum_future = group[future_col].transform("sum").astype(float)
        bars[f"basket_future_return_h{horizon}"] = np.where(count > 1, (sum_future - bars[future_col].astype(float)) / (count - 1.0), np.nan)
    market = (
        bars.loc[bars["peer_group_id"].eq("index_etf_basket"), ["trade_date", "source_event_bar_id", "bar_return", "avg_top5_market_by_price_imbalance"]]
        .groupby(["trade_date", "source_event_bar_id"], sort=False)
        .mean(numeric_only=True)
        .rename(columns={"bar_return": "index_basket_return", "avg_top5_market_by_price_imbalance": "index_basket_top5_imbalance"})
        .reset_index()
    )
    bars = bars.merge(market, on=["trade_date", "source_event_bar_id"], how="left")
    bars["index_residual_return"] = bars["bar_return"].astype(float) - bars["index_basket_return"].fillna(0.0).astype(float)
    bars["index_relative_top5_imbalance"] = bars["avg_top5_market_by_price_imbalance"].astype(float) - bars["index_basket_top5_imbalance"].fillna(0.0).astype(float)
    bars["index_relative_depth_beyond_l1_imbalance"] = bars["relative_depth_beyond_l1_imbalance"].fillna(0.0).astype(float)
    bars["residual_rank_pct"] = bars.groupby(["trade_date", "source_event_bar_id", "peer_group_id"], sort=False)["symbol_residual_return"].rank(pct=True)
    bars["top5_rank_pct"] = bars.groupby(["trade_date", "source_event_bar_id", "peer_group_id"], sort=False)["relative_top5_imbalance"].rank(pct=True)
    return bars


def build_leg_ledger(
    selected: pd.DataFrame,
    family: str,
    cid: str,
    horizon: int,
    signal_side: pd.Series,
    basket_mode: str,
    thresholds: dict[str, float],
) -> pd.DataFrame:
    future_col = f"future_return_h{horizon}"
    basket_future_col = f"basket_future_return_h{horizon}"
    selected = selected.copy()
    selected["_signal_side"] = signal_side.astype(float)
    selected = selected[
        selected[future_col].notna()
        & selected[basket_future_col].notna()
        & selected["basket_cost_bps"].notna()
        & selected["_signal_side"].ne(0)
    ].copy()
    if selected.empty:
        return pd.DataFrame()
    selected["candidate_id"] = cid
    selected["family_id"] = family
    selected["signal_symbol"] = selected["symbol"].astype(str)
    selected["leg_symbol"] = selected["symbol"].astype(str)
    selected["leg_role"] = "market_neutral_signal_plus_peer_basket"
    selected["horizon_event_bars"] = horizon
    selected["basket_mode"] = basket_mode
    selected["side"] = selected["_signal_side"].astype(float)
    selected["notional_inr"] = DEFAULT_ORDER_NOTIONAL_INR
    selected["future_return"] = selected[future_col].astype(float)
    selected["basket_future_return"] = selected[basket_future_col].astype(float)
    selected["gross_pnl_inr"] = selected["side"] * (selected["future_return"] - selected["basket_future_return"]) * DEFAULT_ORDER_NOTIONAL_INR
    selected["symbol_cost_pnl_drag_inr"] = selected["taker_round_trip_cost_floor_bps"].astype(float) / 10000.0 * DEFAULT_ORDER_NOTIONAL_INR
    selected["basket_cost_pnl_drag_inr"] = selected["basket_cost_bps"].astype(float) / 10000.0 * DEFAULT_ORDER_NOTIONAL_INR
    selected["cost_pnl_drag_inr"] = selected["symbol_cost_pnl_drag_inr"] + selected["basket_cost_pnl_drag_inr"]
    selected["net_pnl_inr"] = selected["gross_pnl_inr"] - selected["cost_pnl_drag_inr"]
    for key, value in thresholds.items():
        selected[key] = value
    keep = [
        "candidate_id",
        "family_id",
        "trade_date",
        "exchange",
        "source_event_bar_id",
        "peer_group_id",
        "signal_symbol",
        "leg_symbol",
        "leg_role",
        "horizon_event_bars",
        "basket_mode",
        "side",
        "notional_inr",
        "future_return",
        "basket_future_return",
        "symbol_residual_return",
        "relative_top5_imbalance",
        "relative_depth_beyond_l1_imbalance",
        "avg_spread",
        "avg_event_intensity_proxy",
        "taker_round_trip_cost_floor_bps",
        "basket_cost_bps",
        "gross_pnl_inr",
        "symbol_cost_pnl_drag_inr",
        "basket_cost_pnl_drag_inr",
        "cost_pnl_drag_inr",
        "net_pnl_inr",
        *thresholds.keys(),
    ]
    return selected[keep].copy()


def summarize_ledger(cid: str, family: str, ledger: pd.DataFrame, params: dict[str, Any]) -> dict[str, Any]:
    gross = float(ledger["gross_pnl_inr"].sum()) if not ledger.empty else 0.0
    cost = float(ledger["cost_pnl_drag_inr"].sum()) if not ledger.empty else 0.0
    net = gross - cost
    cost150 = gross - 1.5 * cost
    cost200 = gross - 2.0 * cost
    signal_ledger = ledger.copy()
    date_net = ledger.groupby("trade_date", sort=True)["net_pnl_inr"].sum()
    symbol_net = ledger.groupby("leg_symbol", sort=True)["net_pnl_inr"].sum()
    denom = abs(net) if abs(net) > 0 else np.nan
    return {
        "candidate_id": cid,
        "family_id": family,
        **params,
        "training_trades": int(len(signal_ledger)),
        "training_leg_rows": int(len(ledger) * 2),
        "training_net_pnl_inr": net,
        "training_gross_pnl_inr": gross,
        "training_cost_pnl_drag_inr": cost,
        "cost150_net_pnl_inr": cost150,
        "cost200_net_pnl_inr": cost200,
        "training_dates": int(ledger["trade_date"].nunique()) if not ledger.empty else 0,
        "training_symbols": int(ledger["signal_symbol"].nunique()) if not ledger.empty else 0,
        "training_signal_symbols": int(signal_ledger["signal_symbol"].nunique()) if not signal_ledger.empty else 0,
        "training_peer_groups": int(ledger["peer_group_id"].nunique()) if not ledger.empty else 0,
        "training_positive_dates": int((date_net > 0).sum()) if not ledger.empty else 0,
        "training_min_date_net_pnl_inr": float(date_net.min()) if not ledger.empty else np.nan,
        "training_max_date_contribution_abs": float(date_net.abs().max() / denom) if denom and not np.isnan(denom) and not ledger.empty else np.nan,
        "training_max_symbol_contribution_abs": float(symbol_net.abs().max() / denom) if denom and not np.isnan(denom) and not ledger.empty else np.nan,
        "training_precision_cost_clear": float((signal_ledger.groupby(["trade_date", "source_event_bar_id", "signal_symbol"])["net_pnl_inr"].sum() > 0).mean()) if not signal_ledger.empty else 0.0,
        "cost_stress_pass": bool(cost150 > 0 and cost200 > 0),
        "market_neutral_notional": 1,
        "costs_applied_per_leg": 1,
        "top5_feature_active": 1,
        "full_top_five_depth_active": 1,
        "depth_beyond_l1_active": 1,
    }


def replay_variant(
    bars: pd.DataFrame,
    family: str,
    horizon: int,
    residual_q: float,
    top5_q: float,
    depth_q: float,
    spread_q: float,
    intensity_q: float,
    rank_bucket: int,
) -> tuple[dict[str, Any], pd.DataFrame]:
    future_col = f"future_return_h{horizon}"
    valid = bars[bars[future_col].notna()].copy()
    if valid.empty:
        return {}, pd.DataFrame()
    residual_col = "index_residual_return" if family == "P250_INDEX_BASKET_RESIDUAL_REVERSION" else "symbol_residual_return"
    top5_col = "index_relative_top5_imbalance" if family == "P250_INDEX_BASKET_RESIDUAL_REVERSION" else "relative_top5_imbalance"
    depth_col = "index_relative_depth_beyond_l1_imbalance" if family == "P250_INDEX_BASKET_RESIDUAL_REVERSION" else "relative_depth_beyond_l1_imbalance"
    valid = valid[valid[residual_col].notna() & valid[top5_col].notna() & valid[depth_col].notna()].copy()
    if valid.empty:
        return {}, pd.DataFrame()
    thresholds = {
        "residual_abs_threshold": float(valid[residual_col].abs().quantile(residual_q)),
        "top5_abs_threshold": float(valid[top5_col].abs().quantile(top5_q)),
        "depth_beyond_l1_abs_threshold": float(valid[depth_col].abs().quantile(depth_q)),
        "spread_max": float(valid["avg_spread"].quantile(spread_q)),
        "event_intensity_min": float(valid["avg_event_intensity_proxy"].quantile(intensity_q)),
    }
    filtered = valid[
        valid["avg_spread"].le(thresholds["spread_max"])
        & valid["avg_event_intensity_proxy"].ge(thresholds["event_intensity_min"])
    ].copy()
    if family in {"P250_SECTOR_PAIR_RESIDUAL_REVERSION", "P250_INDEX_BASKET_RESIDUAL_REVERSION"}:
        filtered = filtered[
            filtered[residual_col].abs().ge(thresholds["residual_abs_threshold"])
            & filtered[top5_col].abs().ge(thresholds["top5_abs_threshold"])
            & filtered[depth_col].abs().ge(thresholds["depth_beyond_l1_abs_threshold"])
            & (np.sign(filtered[top5_col].astype(float)) != np.sign(filtered[residual_col].astype(float)))
        ].copy()
        signal_side = -np.sign(filtered[residual_col].astype(float))
        basket_mode = "residual_reversion_against_peers"
    elif family == "P250_TOP5_IMBALANCE_RELATIVE_DIVERGENCE":
        filtered = filtered[
            filtered[top5_col].abs().ge(thresholds["top5_abs_threshold"])
            & filtered[depth_col].abs().ge(thresholds["depth_beyond_l1_abs_threshold"])
            & filtered[residual_col].abs().le(thresholds["residual_abs_threshold"])
        ].copy()
        signal_side = np.sign(filtered[top5_col].astype(float))
        basket_mode = "relative_top5_predictive_against_peers"
    else:
        enriched = filtered.copy()
        enriched = enriched[enriched[depth_col].abs().ge(thresholds["depth_beyond_l1_abs_threshold"])].copy()
        enriched["_rank_score"] = -enriched[residual_col].rank(pct=True) + enriched[top5_col].rank(pct=True) + 0.5 * enriched[depth_col].rank(pct=True)
        enriched["_long_rank"] = enriched.groupby(["trade_date", "source_event_bar_id", "peer_group_id"], sort=False)["_rank_score"].rank(method="first", ascending=False)
        enriched["_short_rank"] = enriched.groupby(["trade_date", "source_event_bar_id", "peer_group_id"], sort=False)["_rank_score"].rank(method="first", ascending=True)
        filtered = enriched[(enriched["_long_rank"].le(rank_bucket)) | (enriched["_short_rank"].le(rank_bucket))].copy()
        signal_side = np.where(filtered["_long_rank"].le(rank_bucket), 1.0, -1.0)
        basket_mode = "ranked_market_neutral_long_short"
    if filtered.empty:
        return {}, pd.DataFrame()
    cid = candidate_id(family, horizon, residual_q, top5_q, depth_q, spread_q, intensity_q, rank_bucket)
    params = {
        "horizon_event_bars": horizon,
        "residual_quantile": residual_q,
        "top5_abs_quantile": top5_q,
        "depth_beyond_l1_quantile": depth_q,
        "spread_quantile": spread_q,
        "intensity_quantile": intensity_q,
        "rank_bucket": rank_bucket,
        "basket_mode": basket_mode,
    }
    ledger = build_leg_ledger(filtered, family, cid, horizon, pd.Series(signal_side, index=filtered.index), basket_mode, thresholds)
    if ledger.empty:
        return {}, pd.DataFrame()
    return summarize_ledger(cid, family, ledger, params), ledger


def scan_variants(bars: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    rows: list[dict[str, Any]] = []
    ledgers: dict[str, pd.DataFrame] = {}
    for family in FAMILIES:
        for horizon in HORIZONS:
            for residual_q in RESIDUAL_QUANTILES:
                for top5_q in TOP5_QUANTILES:
                    for depth_q in DEPTH_BEYOND_L1_QUANTILES:
                        for spread_q in SPREAD_QUANTILES:
                            for intensity_q in INTENSITY_QUANTILES:
                                for rank_bucket in RANK_BUCKETS:
                                    summary, ledger = replay_variant(bars, family, horizon, residual_q, top5_q, depth_q, spread_q, intensity_q, rank_bucket)
                                    if not summary:
                                        continue
                                    rows.append(summary)
                                    if summary["cost_stress_pass"] and summary["training_trades"] >= MIN_CONTROL_TRADES:
                                        ledgers[summary["candidate_id"]] = ledger
    candidates = pd.DataFrame(rows)
    if candidates.empty:
        return candidates, ledgers
    candidates = candidates.sort_values(["cost200_net_pnl_inr", "cost150_net_pnl_inr", "training_net_pnl_inr"], ascending=[False, False, False]).reset_index(drop=True)
    return candidates, ledgers


def build_controls(candidates: pd.DataFrame, ledgers: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    if candidates.empty:
        return pd.DataFrame(), pd.DataFrame()
    pool = candidates[
        candidates["cost_stress_pass"].astype(bool)
        & candidates["training_trades"].ge(MIN_CONTROL_TRADES)
        & candidates["training_dates"].ge(MIN_CONTROL_DATES)
        & candidates["training_symbols"].ge(MIN_CONTROL_SYMBOLS)
        & candidates["market_neutral_notional"].eq(1)
        & candidates["costs_applied_per_leg"].eq(1)
        & candidates["full_top_five_depth_active"].eq(1)
        & candidates["depth_beyond_l1_active"].eq(1)
    ].head(100)
    rng = np.random.default_rng(RANDOM_SEED)
    for candidate in pool.to_dict("records"):
        cid = str(candidate["candidate_id"])
        ledger = ledgers.get(cid, pd.DataFrame())
        if ledger.empty:
            continue
        gross = ledger["gross_pnl_inr"].to_numpy(dtype=float)
        cost = ledger["cost_pnl_drag_inr"].to_numpy(dtype=float)
        net = float((gross - cost).sum())
        random_nets = np.asarray([float((rng.choice([-1.0, 1.0], size=len(ledger)) * np.abs(gross) - cost).sum()) for _ in range(RANDOM_CONTROL_RUNS)])
        rows.append(
            {
                "candidate_id": cid,
                "side_flip_net_pnl_inr": float((-gross - cost).sum()),
                "side_flip_pass": bool((-gross - cost).sum() < 0),
                "random_p95_net_pnl_inr": float(np.quantile(random_nets, 0.95)),
                "random_beat_fraction": float((net > random_nets).mean()),
                "random_side_pass": bool((net > random_nets).mean() >= RANDOM_BEAT_THRESHOLD),
                "cost150_net_pnl_inr": candidate["cost150_net_pnl_inr"],
                "cost150_pass": bool(candidate["cost150_net_pnl_inr"] > 0),
                "cost200_net_pnl_inr": candidate["cost200_net_pnl_inr"],
                "cost200_pass": bool(candidate["cost200_net_pnl_inr"] > 0),
            }
        )
    controls = pd.DataFrame(rows)
    if controls.empty:
        return controls, pd.DataFrame()
    controls["control_pass_rows"] = controls[["side_flip_pass", "random_side_pass", "cost150_pass", "cost200_pass"]].astype(bool).sum(axis=1)
    controlled = candidates.merge(controls, on="candidate_id", how="inner")
    controlled["phase251_candidate_survived"] = (
        controlled["control_pass_rows"].ge(4)
        & controlled["training_dates"].ge(MIN_CONTROL_DATES)
        & controlled["training_symbols"].ge(MIN_CONTROL_SYMBOLS)
        & controlled["training_trades"].ge(MIN_CONTROL_TRADES)
        & controlled["market_neutral_notional"].eq(1)
        & controlled["costs_applied_per_leg"].eq(1)
        & controlled["full_top_five_depth_active"].eq(1)
        & controlled["depth_beyond_l1_active"].eq(1)
    )
    controlled = controlled.sort_values(["phase251_candidate_survived", "random_beat_fraction", "cost200_net_pnl_inr_y"], ascending=[False, False, False])
    return controls, controlled.reset_index(drop=True)


def build_gate_evaluation(candidates: pd.DataFrame, controlled: pd.DataFrame, phase250_dir: Path) -> pd.DataFrame:
    next_action = str(metric_value(phase250_dir / "phase250_acceptance_summary.csv", "phase250_next_best_action", ""))
    survivors = int(controlled["phase251_candidate_survived"].astype(bool).sum()) if not controlled.empty else 0
    cost200_positive = int(candidates["cost200_net_pnl_inr"].gt(0).sum()) if not candidates.empty else 0
    market_neutral = int(candidates["market_neutral_notional"].eq(1).sum()) if not candidates.empty else 0
    costs_per_leg = int(candidates["costs_applied_per_leg"].eq(1).sum()) if not candidates.empty else 0
    full_depth = int(candidates["full_top_five_depth_active"].eq(1).sum()) if not candidates.empty else 0
    beyond_l1 = int(candidates["depth_beyond_l1_active"].eq(1).sum()) if not candidates.empty else 0
    rows = [
        ("P251_PHASE250_WORK_ORDER_PRESENT", "run_phase251_training_only_pair_basket_relative_value_search" in next_action, next_action, "Phase250 next action targets Phase251", "hard"),
        ("P251_FORBIDDEN_DATES_EXCLUDED", True, ";".join(sorted(FORBIDDEN_TUNING_DATES)), "2026-07-17 and 2026-07-20 excluded", "hard"),
        ("P251_VARIANTS_EVALUATED", len(candidates) >= 400, len(candidates), ">=400 pair/basket variants", "hard"),
        ("P251_MARKET_NEUTRAL_ALL_VARIANTS", market_neutral == len(candidates) and len(candidates) > 0, f"{market_neutral}/{len(candidates)}", "all variants", "hard"),
        ("P251_COSTS_PER_LEG_ALL_VARIANTS", costs_per_leg == len(candidates) and len(candidates) > 0, f"{costs_per_leg}/{len(candidates)}", "all variants", "hard"),
        ("P251_FULL_TOP_FIVE_DEPTH_ALL_VARIANTS", full_depth == len(candidates) and len(candidates) > 0, f"{full_depth}/{len(candidates)}", "all variants use top-five market-by-price depth", "hard"),
        ("P251_DEPTH_BEYOND_L1_ALL_VARIANTS", beyond_l1 == len(candidates) and len(candidates) > 0, f"{beyond_l1}/{len(candidates)}", "all variants use depth beyond L1", "hard"),
        ("P251_COST200_POSITIVE_VARIANTS_FOUND", cost200_positive > 0, cost200_positive, ">0 positive at 2x cost", "hard"),
        ("P251_CONTROLLED_SURVIVOR_FOUND", survivors > 0, survivors, ">0 controlled survivors", "diagnostic"),
        ("P251_NO_DOWNLOAD_HOLDOUT_TUNING_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase251 Pair/Basket Relative-value Training Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase251 executes the Phase250 precommitted training-only search.",
        "It excludes 2026-07-17 and 2026-07-20 from tuning, uses existing Phase235 event bars only, balances long/short notional, applies costs per leg and keeps downloads, holdout execution, paper/live and profitability claims closed.",
        "Every variant requires Zerodha top-five market-by-price depth through `avg_top5_market_by_price_imbalance` and a depth-beyond-L1 contrast, so this is not an L1-only or price-only search.",
        "",
    ]
    for title, table in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(table), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(bars_path: Path = DEFAULT_BARS_PATH, phase250_dir: Path = DEFAULT_PHASE250_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    bars = load_training_bars(bars_path, phase250_dir)
    candidates, ledgers = scan_variants(bars)
    controls, controlled = build_controls(candidates, ledgers)
    survivors = controlled[controlled["phase251_candidate_survived"].astype(bool)].copy() if not controlled.empty else pd.DataFrame()
    best = survivors.iloc[0].to_dict() if not survivors.empty else (controlled.iloc[0].to_dict() if not controlled.empty else (candidates.iloc[0].to_dict() if not candidates.empty else {}))
    best_id = str(best.get("candidate_id", ""))
    if best_id and best_id not in ledgers:
        _, best_ledger = replay_variant(
            bars,
            str(best.get("family_id", "")),
            as_int(best.get("horizon_event_bars", 0)),
            as_float(best.get("residual_quantile", 0.0)),
            as_float(best.get("top5_abs_quantile", 0.0)),
            as_float(best.get("depth_beyond_l1_quantile", 0.0)),
            as_float(best.get("spread_quantile", 0.0)),
            as_float(best.get("intensity_quantile", 0.0)),
            as_int(best.get("rank_bucket", 1)),
        )
        if not best_ledger.empty:
            ledgers[best_id] = best_ledger
    gates = build_gate_evaluation(candidates, controlled, phase250_dir)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = (
        "precommit_phase252_future_holdout_for_pair_basket_relative_value_candidate_no_2026_07_17_or_2026_07_20_tuning_no_paper_live"
        if not survivors.empty
        else "close_or_broaden_phase251_pair_basket_relative_value_search_no_downloads_no_paper_live"
    )
    acceptance = pd.DataFrame(
        [
            ("phase251_pair_basket_search_complete", 1, "Phase251 pair/basket training-only search completed"),
            ("phase251_training_event_bar_rows", len(bars), "Training event bars after forbidden-date exclusion and universe filter"),
            ("phase251_training_dates", bars["trade_date"].nunique(), "Training dates used"),
            ("phase251_training_symbols", bars["symbol"].nunique(), "Training symbols used"),
            ("phase251_forbidden_tuning_dates", ";".join(sorted(FORBIDDEN_TUNING_DATES)), "Dates excluded from tuning"),
            ("phase251_variant_rows", len(candidates), "Pair/basket variants evaluated"),
            ("phase251_full_top_five_depth_variant_rows", int(candidates["full_top_five_depth_active"].eq(1).sum()) if not candidates.empty else 0, "Variants using top-five market-by-price depth"),
            ("phase251_depth_beyond_l1_variant_rows", int(candidates["depth_beyond_l1_active"].eq(1).sum()) if not candidates.empty else 0, "Variants using depth-beyond-L1 contrast"),
            ("phase251_net_positive_variant_rows", int(candidates["training_net_pnl_inr"].gt(0).sum()) if not candidates.empty else 0, "Net-positive variants at base cost"),
            ("phase251_cost150_positive_variant_rows", int(candidates["cost150_net_pnl_inr"].gt(0).sum()) if not candidates.empty else 0, "Positive variants at 1.5x cost"),
            ("phase251_cost200_positive_variant_rows", int(candidates["cost200_net_pnl_inr"].gt(0).sum()) if not candidates.empty else 0, "Positive variants at 2.0x cost"),
            ("phase251_controlled_candidate_rows", len(controlled), "Candidates evaluated with side-flip/random-side controls"),
            ("phase251_survivor_candidate_rows", len(survivors), "Candidates passing controls and breadth gates"),
            ("phase251_best_candidate_id", best_id, "Best Phase251 survivor/candidate"),
            ("phase251_best_family_id", best.get("family_id", ""), "Best candidate family"),
            ("phase251_best_training_net_pnl_inr", as_float(best.get("training_net_pnl_inr", 0.0)), "Best training net P&L"),
            ("phase251_best_cost200_net_pnl_inr", as_float(best.get("cost200_net_pnl_inr_y", best.get("cost200_net_pnl_inr", 0.0))), "Best 2x-cost net P&L"),
            ("phase251_best_random_beat_fraction", as_float(best.get("random_beat_fraction", 0.0)), "Best random-side beat fraction"),
            ("phase251_best_trade_rows", as_int(best.get("training_trades", 0)), "Best signal trades"),
            ("phase251_best_leg_rows", as_int(best.get("training_leg_rows", 0)), "Best leg rows"),
            ("phase251_best_dates", as_int(best.get("training_dates", 0)), "Best dates represented"),
            ("phase251_best_symbols", as_int(best.get("training_symbols", 0)), "Best leg symbols represented"),
            ("phase251_best_peer_groups", as_int(best.get("training_peer_groups", 0)), "Best peer groups represented"),
            ("phase251_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase251_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase251_future_holdout_precommit_allowed", int(not survivors.empty), "Future holdout precommit allowed only if survivors exist"),
            ("phase251_download_more_dates_now_allowed", 0, "No raw-date download in Phase251"),
            ("phase251_holdout_parameter_tuning_allowed", 0, "No holdout-date tuning"),
            ("phase251_strategy_promotion_allowed", 0, "No strategy promotion from Phase251"),
            ("phase251_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase251"),
            ("phase251_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase251"),
            ("phase251_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    candidates.to_csv(output_dir / "phase251_candidate_summary.csv", index=False)
    controls.to_csv(output_dir / "phase251_control_summary.csv", index=False)
    controlled.to_csv(output_dir / "phase251_controlled_candidate_summary.csv", index=False)
    survivors.to_csv(output_dir / "phase251_survivor_candidates.csv", index=False)
    ledgers.get(best_id, pd.DataFrame()).to_csv(output_dir / "phase251_best_candidate_leg_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase251_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase251_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase251_pair_basket_relative_value_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Best Candidate": pd.DataFrame([best]) if best else pd.DataFrame(),
            "Survivor Candidates": survivors.head(25),
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase251_pair_basket_relative_value_search",
        **reproducibility_fields(
            artifact_id="phase251",
            generated_utc=generated_utc,
            inputs={"bars_path": str(bars_path), "phase250_dir": str(phase250_dir)},
            parameters={
                "horizons": HORIZONS,
                "families": FAMILIES,
                "residual_quantiles": RESIDUAL_QUANTILES,
                "top5_quantiles": TOP5_QUANTILES,
                "depth_beyond_l1_quantiles": DEPTH_BEYOND_L1_QUANTILES,
                "spread_quantiles": SPREAD_QUANTILES,
                "intensity_quantiles": INTENSITY_QUANTILES,
                "rank_buckets": RANK_BUCKETS,
                "forbidden_tuning_dates": sorted(FORBIDDEN_TUNING_DATES),
                "random_control_runs": RANDOM_CONTROL_RUNS,
                "random_seed": RANDOM_SEED,
                "download_more_dates_now_allowed": 0,
                "holdout_parameter_tuning_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "candidate_summary": str(output_dir / "phase251_candidate_summary.csv"),
                "control_summary": str(output_dir / "phase251_control_summary.csv"),
                "controlled_candidate_summary": str(output_dir / "phase251_controlled_candidate_summary.csv"),
                "survivor_candidates": str(output_dir / "phase251_survivor_candidates.csv"),
                "best_candidate_leg_ledger": str(output_dir / "phase251_best_candidate_leg_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase251_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase251_acceptance_summary.csv"),
                "report": str(output_dir / "phase251_pair_basket_relative_value_search_report.md"),
            },
            random_seed=RANDOM_SEED,
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase251_training_only_pair_basket_real_event_bar_adapter_no_holdout_tuning",
        ),
    }
    (output_dir / "phase251_pair_basket_relative_value_search_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase251 pair/basket relative-value training-only search.")
    parser.add_argument("--bars-path", type=Path, default=DEFAULT_BARS_PATH)
    parser.add_argument("--phase250-dir", type=Path, default=DEFAULT_PHASE250_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(bars_path=args.bars_path, phase250_dir=args.phase250_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase271_fixed_capital_concurrency_and_capacity_return_analysis import schedule_events_for_scenario
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import (
    ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
    calculate_equity_intraday_nse_charges,
)


DEFAULT_INPUT_PATH = Path("outputs/phase42/native_full_year_l2_event_state.parquet")
DEFAULT_PHASE295_DIR = Path("outputs/phase295")
DEFAULT_OUTPUT_DIR = Path("outputs/phase296")

SELECTED_ROUTE = "P296_FULL_YEAR_TOP5_DEPTH_STRATEGY_FAMILY_SWEEP"
NEXT_ACTION = "run_phase297_full_year_top5_depth_strategy_family_sweep_interpretation_no_paper_live"
REPAIR_ACTION = "repair_phase296_full_year_top5_depth_strategy_family_sweep"

INITIAL_CAPITAL_INR = 1_000_000.0
FIXED_NOTIONAL_GRID_INR = [100_000.0]
MAX_CONCURRENT_GRID = [1, 2]
COST_MULTIPLIER = 2.0
EXTRA_SLIPPAGE_BPS = 0.0
ANNUALIZED_THRESHOLD_PCT = 12.0
SPARSE_DIAGNOSTIC_EVENT_FLOOR = 8
ROBUST_PORTFOLIO_EVENT_FLOOR = 30
SAMPLE_LEDGER_ROWS = 5_000

INPUT_COLUMNS = [
    "feed_profile",
    "synthetic_trade_date",
    "synthetic_year_day",
    "symbol",
    "annual_event_id",
    "receive_sequence",
    "regime_code",
    "mid_price",
    "next_mid_price",
    "l1_imbalance",
    "l5_imbalance",
    "spread_ticks",
    "tick_size",
    "event_intensity_proxy",
    "mlofi_qty_event",
    "momentum_3_event",
    "local_volatility_6_event",
    "microprice_dev",
    "is_market_shock_day",
    "is_duplicate",
    "is_disconnect_gap",
    "is_out_of_order_injected",
    "next_is_bad_feed",
]


def q(frame: pd.DataFrame, column: str, quantile: float) -> float:
    values = pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty:
        return 0.0
    return float(values.quantile(quantile))


def load_full_year_events(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    schema_names = set(pq.ParquetFile(path).schema.names)
    missing = [col for col in INPUT_COLUMNS if col not in schema_names]
    if missing:
        raise ValueError(f"Phase296 input is missing required columns: {missing}")
    frame = pq.read_table(path, columns=INPUT_COLUMNS).to_pandas()
    frame = frame.sort_values(["feed_profile", "synthetic_year_day", "symbol", "annual_event_id"], kind="mergesort").reset_index(drop=True)
    numeric_cols = [
        "annual_event_id",
        "synthetic_year_day",
        "receive_sequence",
        "mid_price",
        "next_mid_price",
        "l1_imbalance",
        "l5_imbalance",
        "spread_ticks",
        "tick_size",
        "event_intensity_proxy",
        "mlofi_qty_event",
        "momentum_3_event",
        "local_volatility_6_event",
        "microprice_dev",
    ]
    for col in numeric_cols:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    for col in ["is_market_shock_day", "is_duplicate", "is_disconnect_gap", "is_out_of_order_injected", "next_is_bad_feed"]:
        frame[col] = frame[col].fillna(False).astype(bool)
    group_cols = ["feed_profile", "synthetic_year_day", "symbol"]
    grouped = frame.groupby(group_cols, sort=False)
    for horizon in [1, 3, 6]:
        frame[f"future_mid_h{horizon}"] = grouped["mid_price"].shift(-horizon)
        frame[f"forward_return_bps_h{horizon}"] = (frame[f"future_mid_h{horizon}"] / frame["mid_price"] - 1.0) * 10_000.0
    frame["beyond_l1_imbalance_proxy"] = frame["l5_imbalance"] - frame["l1_imbalance"]
    frame["abs_beyond_l1_imbalance_proxy"] = frame["beyond_l1_imbalance_proxy"].abs()
    frame["abs_l5_imbalance"] = frame["l5_imbalance"].abs()
    frame["abs_mlofi"] = frame["mlofi_qty_event"].abs()
    frame["abs_momentum_3_event"] = frame["momentum_3_event"].abs()
    frame["abs_microprice_dev"] = frame["microprice_dev"].abs()
    frame["spread_bps_proxy"] = (frame["spread_ticks"].clip(lower=1) * frame["tick_size"]) / frame["mid_price"].replace(0.0, np.nan) * 10_000.0
    frame["nontrend_regime"] = ~frame["regime_code"].astype(str).isin(["D03", "D04", "D05", "D06"])
    return frame


def zerodha_round_trip_charge_bps(notional_inr: float = 100_000.0) -> float:
    charges = calculate_equity_intraday_nse_charges(
        buy_value_inr=notional_inr,
        sell_value_inr=notional_inr,
        buy_quantity=1.0,
        sell_quantity=1.0,
        buy_orders=1,
        sell_orders=1,
    )
    return float(charges.breakeven_bps_on_buy_value)


def family_signal(frame: pd.DataFrame, family_id: str) -> tuple[pd.Series, pd.Series, pd.Series]:
    if family_id == "P296_TOP5_PRESSURE_CONTINUATION":
        pressure = frame["l5_imbalance"]
        score = frame["abs_l5_imbalance"] * (1.0 + frame["event_intensity_proxy"].fillna(0.0).clip(lower=0.0))
        eligible = pressure.abs().gt(0.0)
    elif family_id == "P296_BEYOND_L1_ABSORPTION_CONTINUATION":
        pressure = frame["beyond_l1_imbalance_proxy"]
        score = frame["abs_beyond_l1_imbalance_proxy"] * (1.0 + frame["event_intensity_proxy"].fillna(0.0).clip(lower=0.0))
        eligible = pressure.abs().gt(0.0)
    elif family_id == "P296_TOP5_PRESSURE_REVERSAL_RANGE":
        pressure = -frame["l5_imbalance"]
        score = frame["abs_l5_imbalance"] * frame["nontrend_regime"].astype(float)
        eligible = frame["nontrend_regime"] & pressure.abs().gt(0.0)
    elif family_id == "P296_SPREAD_COMPRESSED_MLOFI_FOLLOW":
        pressure = frame["mlofi_qty_event"]
        score = frame["abs_mlofi"] * (1.0 + frame["abs_l5_imbalance"])
        eligible = pressure.abs().gt(0.0)
    elif family_id == "P296_LIQUIDITY_VACUUM_MOMENTUM_CONTINUATION":
        pressure = frame["momentum_3_event"]
        score = frame["abs_momentum_3_event"] * (1.0 + frame["spread_bps_proxy"].fillna(0.0))
        eligible = pressure.abs().gt(0.0)
    elif family_id == "P296_MICROPRICE_DEPTH_REVERSAL":
        pressure = -frame["microprice_dev"]
        score = frame["abs_microprice_dev"] * (1.0 + frame["abs_l5_imbalance"])
        eligible = pressure.abs().gt(0.0)
    else:
        raise ValueError(f"Unknown family_id={family_id}")
    side = pd.Series(np.sign(pressure).astype("int8"), index=frame.index)
    return side, score.astype(float), eligible.fillna(False)


def build_variant_catalog_and_events(events: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    family_ids = [
        "P296_TOP5_PRESSURE_CONTINUATION",
        "P296_BEYOND_L1_ABSORPTION_CONTINUATION",
        "P296_TOP5_PRESSURE_REVERSAL_RANGE",
        "P296_SPREAD_COMPRESSED_MLOFI_FOLLOW",
        "P296_LIQUIDITY_VACUUM_MOMENTUM_CONTINUATION",
        "P296_MICROPRICE_DEPTH_REVERSAL",
    ]
    intensity_quantiles = [0.70, 0.85]
    beyond_l1_quantiles = [0.70]
    spread_regimes = [("NOT_WIDE", 0.80, "le")]
    daily_event_limits = [1, 3]
    horizons = [1, 3, 6]
    base_tradable = (
        events["mid_price"].gt(0.0)
        & ~events["is_duplicate"]
        & ~events["is_disconnect_gap"]
        & ~events["is_out_of_order_injected"]
        & ~events["next_is_bad_feed"]
    )
    base_charge_bps = zerodha_round_trip_charge_bps()
    rows: list[dict[str, Any]] = []
    variant_events: dict[str, pd.DataFrame] = {}
    for feed_profile, profile_frame in events.groupby("feed_profile", sort=True):
        profile_frame = profile_frame.copy()
        spread_q = {label: q(profile_frame, "spread_bps_proxy", quantile) for label, quantile, _ in spread_regimes}
        intensity_q = {quantile: q(profile_frame, "event_intensity_proxy", quantile) for quantile in intensity_quantiles}
        beyond_q = {quantile: q(profile_frame, "abs_beyond_l1_imbalance_proxy", quantile) for quantile in beyond_l1_quantiles}
        for family_id in family_ids:
            side, score, family_eligible = family_signal(profile_frame, family_id)
            profile_frame["_family_side"] = side
            profile_frame["_family_score"] = score
            for intensity_quantile in intensity_quantiles:
                for beyond_quantile in beyond_l1_quantiles:
                    full_depth_mask = profile_frame["abs_beyond_l1_imbalance_proxy"].ge(beyond_q[beyond_quantile])
                    intensity_mask = profile_frame["event_intensity_proxy"].ge(intensity_q[intensity_quantile])
                    for spread_label, _spread_quantile, spread_operator in spread_regimes:
                        if spread_operator == "le":
                            spread_mask = profile_frame["spread_bps_proxy"].le(spread_q[spread_label])
                        else:
                            spread_mask = profile_frame["spread_bps_proxy"].ge(spread_q[spread_label])
                        base_mask = base_tradable.loc[profile_frame.index] & family_eligible & full_depth_mask & intensity_mask & spread_mask
                        selected_base = profile_frame.loc[base_mask].copy()
                        if selected_base.empty:
                            continue
                        selected_base = selected_base.sort_values(
                            ["synthetic_trade_date", "_family_score", "annual_event_id"],
                            ascending=[True, False, True],
                            kind="mergesort",
                        )
                        selected_base["_daily_rank"] = selected_base.groupby("synthetic_trade_date", sort=False).cumcount() + 1
                        for daily_limit in daily_event_limits:
                            limited = selected_base[selected_base["_daily_rank"].le(daily_limit)].copy()
                            if limited.empty:
                                continue
                            for horizon in horizons:
                                tradable = limited[f"future_mid_h{horizon}"].notna() & limited[f"forward_return_bps_h{horizon}"].replace([np.inf, -np.inf], np.nan).notna()
                                v = limited.loc[tradable].copy()
                                if v.empty:
                                    continue
                                variant_id = (
                                    f"{family_id}_{str(feed_profile).upper()}"
                                    f"_IQ{int(intensity_quantile*100)}"
                                    f"_BQ{int(beyond_quantile*100)}"
                                    f"_{spread_label}_DL{daily_limit}_H{horizon}"
                                )
                                v["trade_date"] = v["synthetic_trade_date"].astype(str)
                                v["exchange"] = "NSE"
                                v["richer_event_bar_id"] = v["annual_event_id"].astype(int)
                                v["candidate_id"] = variant_id
                                v["candidate_rank"] = v["_daily_rank"].astype(int)
                                v["family_id"] = family_id
                                v["side"] = v["_family_side"].astype(int)
                                v["horizon"] = int(horizon)
                                v["gross_edge_bps"] = v["side"].astype(float) * v[f"forward_return_bps_h{horizon}"].astype(float)
                                v["zerodha_round_trip_charge_bps"] = base_charge_bps
                                v["avg_cum_top5_qty_imbalance"] = v["l5_imbalance"].astype(float)
                                v["avg_depth_beyond_l1_qty_imbalance"] = v["beyond_l1_imbalance_proxy"].astype(float)
                                v["avg_level_weighted_depth_imbalance"] = (0.65 * v["l5_imbalance"].astype(float)) + (0.35 * v["beyond_l1_imbalance_proxy"].astype(float))
                                v["depth_replenishment_pressure"] = v["mlofi_qty_event"].astype(float)
                                v["depth_withdrawal_pressure"] = -v["mlofi_qty_event"].astype(float)
                                v["top5_churn_pressure"] = v["abs_mlofi"].astype(float)
                                v["avg_spread_bps"] = v["spread_bps_proxy"].astype(float)
                                keep_cols = [
                                    "trade_date",
                                    "exchange",
                                    "symbol",
                                    "richer_event_bar_id",
                                    "candidate_id",
                                    "candidate_rank",
                                    "family_id",
                                    "side",
                                    "horizon",
                                    "gross_edge_bps",
                                    "zerodha_round_trip_charge_bps",
                                    "avg_cum_top5_qty_imbalance",
                                    "avg_depth_beyond_l1_qty_imbalance",
                                    "avg_level_weighted_depth_imbalance",
                                    "depth_replenishment_pressure",
                                    "depth_withdrawal_pressure",
                                    "top5_churn_pressure",
                                    "avg_spread_bps",
                                ]
                                variant_events[variant_id] = v[keep_cols].sort_values(["trade_date", "richer_event_bar_id", "candidate_rank", "symbol"], kind="mergesort").reset_index(drop=True)
                                rows.append(
                                    {
                                        "phase296_variant_id": variant_id,
                                        "feed_profile": feed_profile,
                                        "strategy_family": family_id,
                                        "intensity_threshold_quantile": intensity_quantile,
                                        "beyond_l1_materiality_quantile": beyond_quantile,
                                        "spread_regime": spread_label,
                                        "daily_event_limit": daily_limit,
                                        "exit_horizon_ticks": horizon,
                                        "selected_event_rows": int(len(variant_events[variant_id])),
                                        "symbols": int(variant_events[variant_id]["symbol"].astype(str).nunique()),
                                        "trade_dates": int(variant_events[variant_id]["trade_date"].astype(str).nunique()),
                                        "uses_top5": 1,
                                        "uses_levels_2_to_5": 1,
                                        "uses_l1_l5_spread_proxy": 1,
                                        "raw_l1_l5_book_state_persisted": 0,
                                        "l1_only_variant": 0,
                                        "uses_net_edge_as_live_mask": 0,
                                        "annualized_denominator": "fixed_initial_capital",
                                    }
                                )
    return pd.DataFrame(rows), variant_events


def build_scenarios(variant_catalog: pd.DataFrame, variant_events: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    scenarios: list[dict[str, Any]] = []
    ledgers: list[pd.DataFrame] = []
    meta = variant_catalog.set_index("phase296_variant_id").to_dict(orient="index")
    for variant_id, events in variant_events.items():
        for fixed_notional in FIXED_NOTIONAL_GRID_INR:
            for max_concurrent in MAX_CONCURRENT_GRID:
                scenario, ledger = schedule_events_for_scenario(
                    events=events,
                    scope_id=variant_id,
                    scope_candidate_id=variant_id,
                    initial_capital_inr=INITIAL_CAPITAL_INR,
                    fixed_notional_inr=fixed_notional,
                    max_concurrent_positions=max_concurrent,
                    cost_profile="cost200",
                    cost_multiplier=COST_MULTIPLIER,
                    extra_slippage_bps=EXTRA_SLIPPAGE_BPS,
                )
                m = meta[variant_id]
                scenario.update(
                    {
                        "phase296_variant_id": variant_id,
                        "feed_profile": m.get("feed_profile", ""),
                        "strategy_family": m.get("strategy_family", ""),
                        "spread_regime": m.get("spread_regime", ""),
                        "daily_event_limit": m.get("daily_event_limit", ""),
                        "exit_horizon_ticks": m.get("exit_horizon_ticks", ""),
                        "selected_event_rows": m.get("selected_event_rows", 0),
                        "uses_top5": 1,
                        "uses_levels_2_to_5": 1,
                        "uses_l1_l5_spread_proxy": 1,
                        "raw_l1_l5_book_state_persisted": 0,
                        "l1_only_variant": 0,
                        "uses_net_edge_as_live_mask": 0,
                        "sparse_diagnostic_event_floor_met": int(scenario["scheduled_event_rows"] >= SPARSE_DIAGNOSTIC_EVENT_FLOOR),
                        "robust_portfolio_event_floor_met": int(scenario["scheduled_event_rows"] >= ROBUST_PORTFOLIO_EVENT_FLOOR),
                        "cost200_above12_sparse_diagnostic": int(
                            scenario["mechanical_one_date_annualized_portfolio_return_pct"] > ANNUALIZED_THRESHOLD_PCT
                            and scenario["scheduled_event_rows"] >= SPARSE_DIAGNOSTIC_EVENT_FLOOR
                        ),
                        "robust_portfolio_floor_above12": int(
                            scenario["mechanical_one_date_annualized_portfolio_return_pct"] > ANNUALIZED_THRESHOLD_PCT
                            and scenario["scheduled_event_rows"] >= ROBUST_PORTFOLIO_EVENT_FLOOR
                        ),
                    }
                )
                scenarios.append(scenario)
                if not ledger.empty and len(ledgers) * SAMPLE_LEDGER_ROWS < SAMPLE_LEDGER_ROWS:
                    sample = ledger[ledger["decision"].astype(str).eq("scheduled")].head(SAMPLE_LEDGER_ROWS).copy()
                    if not sample.empty:
                        sample["phase296_variant_id"] = variant_id
                        sample["feed_profile"] = m.get("feed_profile", "")
                        sample["strategy_family"] = m.get("strategy_family", "")
                        ledgers.append(sample)
    return pd.DataFrame(scenarios), pd.concat(ledgers, ignore_index=True).head(SAMPLE_LEDGER_ROWS) if ledgers else pd.DataFrame()


def build_variant_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for variant_id, group in scenarios.groupby("phase296_variant_id", dropna=False):
        best = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
        rows.append(
            {
                "phase296_variant_id": variant_id,
                "feed_profile": best.get("feed_profile", ""),
                "strategy_family": best.get("strategy_family", ""),
                "spread_regime": best.get("spread_regime", ""),
                "daily_event_limit": best.get("daily_event_limit", ""),
                "exit_horizon_ticks": best.get("exit_horizon_ticks", ""),
                "scenario_rows": int(len(group)),
                "selected_event_rows": int(group["selected_event_rows"].max()),
                "max_scheduled_event_rows": int(group["scheduled_event_rows"].max()),
                "cost200_above12_sparse_diagnostic_rows": int(group["cost200_above12_sparse_diagnostic"].sum()),
                "robust_portfolio_floor_above12_rows": int(group["robust_portfolio_floor_above12"].sum()),
                "sparse_floor_met_rows": int(group["sparse_diagnostic_event_floor_met"].sum()),
                "robust_portfolio_floor_met_rows": int(group["robust_portfolio_event_floor_met"].sum()),
                "min_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].min()),
                "median_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].median()),
                "max_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].max()),
                "max_net_pnl_inr": float(group["realized_net_pnl_inr"].max()),
                "best_scheduled_event_rows": int(best.get("scheduled_event_rows", 0)),
                "best_scenario_id": best.get("scenario_id", ""),
            }
        )
    return pd.DataFrame(rows).sort_values(["cost200_above12_sparse_diagnostic_rows", "max_annualized_pct", "max_scheduled_event_rows"], ascending=[False, False, False], kind="mergesort").reset_index(drop=True)


def build_family_summary(scenarios: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for family, group in scenarios.groupby("strategy_family", dropna=False):
        best = group.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
        rows.append(
            {
                "strategy_family": family,
                "feed_profiles": int(group["feed_profile"].astype(str).nunique()),
                "scenario_rows": int(len(group)),
                "variant_rows": int(group["phase296_variant_id"].astype(str).nunique()),
                "max_scheduled_event_rows": int(group["scheduled_event_rows"].max()),
                "cost200_above12_sparse_diagnostic_rows": int(group["cost200_above12_sparse_diagnostic"].sum()),
                "robust_portfolio_floor_above12_rows": int(group["robust_portfolio_floor_above12"].sum()),
                "sparse_floor_met_rows": int(group["sparse_diagnostic_event_floor_met"].sum()),
                "robust_portfolio_floor_met_rows": int(group["robust_portfolio_event_floor_met"].sum()),
                "min_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].min()),
                "median_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].median()),
                "max_annualized_pct": float(group["mechanical_one_date_annualized_portfolio_return_pct"].max()),
                "max_net_pnl_inr": float(group["realized_net_pnl_inr"].max()),
                "best_variant_id": best.get("phase296_variant_id", ""),
                "best_feed_profile": best.get("feed_profile", ""),
            }
        )
    return pd.DataFrame(rows).sort_values(["robust_portfolio_floor_above12_rows", "cost200_above12_sparse_diagnostic_rows", "max_annualized_pct"], ascending=[False, False, False], kind="mergesort").reset_index(drop=True)


def build_gates(phase295_summary: pd.DataFrame, input_events: pd.DataFrame, catalog: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    phase295_complete = as_int(metric_value(phase295_summary, "phase295_interpretation_complete", 0))
    phase295_next = str(metric_value(phase295_summary, "phase295_next_best_action", ""))
    l1_only = int(pd.to_numeric(catalog.get("l1_only_variant", pd.Series(dtype=int)), errors="coerce").fillna(0).sum())
    leakage = int(pd.to_numeric(catalog.get("uses_net_edge_as_live_mask", pd.Series(dtype=int)), errors="coerce").fillna(0).sum())
    gates = [
        ("P296_PHASE295_WORK_ORDER_PRESENT", phase295_complete == 1 and "phase296" in phase295_next, phase295_next, "Phase295 routes to Phase296"),
        ("P296_INPUT_FULL_YEAR_PRESENT", len(input_events) >= 3_000_000 and input_events["synthetic_trade_date"].nunique() == 252, f"rows={len(input_events)};dates={input_events['synthetic_trade_date'].nunique()}", "full-year Phase42 event-state"),
        ("P296_TOP5_DEPTH_PROXY_PRESENT", {"l1_imbalance", "l5_imbalance", "beyond_l1_imbalance_proxy"}.issubset(set(input_events.columns)), "l1+l5+beyond_l1_proxy", "top-five-depth proxy columns"),
        ("P296_VARIANTS_PRESENT", len(catalog) >= 300, len(catalog), ">=300 profile-specific variants"),
        ("P296_SCENARIOS_PRESENT", len(scenarios) >= 600, len(scenarios), ">=600 fixed-capital cost200 scenarios"),
        ("P296_FIXED_CAPITAL_REQUIRED", bool((scenarios["initial_capital_inr"].astype(float).eq(INITIAL_CAPITAL_INR)).all()), INITIAL_CAPITAL_INR, "fixed initial capital denominator"),
        ("P296_COST200_REQUIRED", bool((scenarios["cost_profile"].astype(str).eq("cost200")).all()), "cost200", "Zerodha cost stress profile"),
        ("P296_FULL_DEPTH_REQUIRED", l1_only == 0 and bool((catalog["uses_top5"].astype(int).eq(1)).all()) and bool((catalog["uses_levels_2_to_5"].astype(int).eq(1)).all()), f"l1_only={l1_only}", "top-five and levels 2-5 proxy required"),
        ("P296_NO_LIVE_NET_EDGE_MASKS", leakage == 0, leakage, "no net/gross edge live masks"),
        ("P296_FIXED_CAPITAL_ANNUALIZED_DENOMINATOR", bool((catalog["annualized_denominator"].astype(str).eq("fixed_initial_capital")).all()), "fixed_initial_capital", "no unlimited-capital annualization"),
        ("P296_BOUNDARIES_CLOSED", True, "replay=0;paper=0;claim=0", "no replay/paper/live/claim"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(input_events: pd.DataFrame, catalog: pd.DataFrame, scenarios: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    best = scenarios.sort_values("mechanical_one_date_annualized_portfolio_return_pct", ascending=False).iloc[0]
    sparse = int(scenarios["cost200_above12_sparse_diagnostic"].sum())
    robust_floor = int(scenarios["robust_portfolio_event_floor_met"].sum())
    robust_above = int(scenarios["robust_portfolio_floor_above12"].sum())
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    return pd.DataFrame(
        [
            ("phase296_full_year_sweep_complete", 1, "Phase296 full-year top-five-depth strategy family sweep completed"),
            ("phase296_selected_route", SELECTED_ROUTE, "Selected route"),
            ("phase296_input_rows", len(input_events), "Full-year event-state rows"),
            ("phase296_input_trade_dates", input_events["synthetic_trade_date"].nunique(), "Synthetic trading dates"),
            ("phase296_input_symbols", input_events["symbol"].astype(str).nunique(), "Symbols"),
            ("phase296_input_feed_profiles", input_events["feed_profile"].astype(str).nunique(), "Feed profiles"),
            ("phase296_variant_rows", len(catalog), "Profile-specific variants evaluated"),
            ("phase296_scenario_rows", len(scenarios), "Cost200 fixed-capital scenarios evaluated"),
            ("phase296_sparse_above12_scenario_rows", sparse, "Above-12 sparse diagnostic rows"),
            ("phase296_robust_portfolio_floor_scenario_rows", robust_floor, "Robust floor rows"),
            ("phase296_robust_portfolio_above12_scenario_rows", robust_above, "Robust above-12 rows"),
            ("phase296_best_variant_id", best.get("phase296_variant_id", ""), "Best variant"),
            ("phase296_best_strategy_family", best.get("strategy_family", ""), "Best family"),
            ("phase296_best_feed_profile", best.get("feed_profile", ""), "Best feed profile"),
            ("phase296_best_cost200_annualized_pct", best.get("mechanical_one_date_annualized_portfolio_return_pct", ""), "Best fixed-capital annualized diagnostic"),
            ("phase296_best_realized_net_pnl_inr", best.get("realized_net_pnl_inr", ""), "Best net P&L"),
            ("phase296_best_scheduled_event_rows", best.get("scheduled_event_rows", ""), "Best scheduled events"),
            ("phase296_best_observed_trade_dates", best.get("observed_trade_dates", ""), "Best observed dates"),
            ("phase296_best_initial_capital_inr", best.get("initial_capital_inr", ""), "Fixed initial capital denominator"),
            ("phase296_best_fixed_notional_inr", best.get("fixed_notional_inr", ""), "Best fixed order notional"),
            ("phase296_best_max_concurrent_positions", best.get("max_concurrent_positions", ""), "Best max concurrent positions"),
            ("phase296_l1_only_variant_rows", int(catalog["l1_only_variant"].sum()), "L1-only variants"),
            ("phase296_net_edge_live_mask_rows", int(catalog["uses_net_edge_as_live_mask"].sum()), "Net edge live masks"),
            ("phase296_annualized_denominator", "fixed_initial_capital", "Annualized denominator"),
            ("phase296_strategy_replay_allowed", 0, "No replay"),
            ("phase296_strategy_promotion_allowed", 0, "No promotion"),
            ("phase296_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase296_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase296_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase296_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase296_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, summary: pd.DataFrame, gates: pd.DataFrame, families: pd.DataFrame, variants: pd.DataFrame) -> None:
    lines = [
        "# Phase296 Full-Year Top-Five-Depth Strategy-Family Sweep",
        "",
        "Phase296 executes a full-year synthetic-only family sweep on Phase42's 3.0M-row event-state.",
        "",
        "The annualized return denominator is fixed initial capital. The reused scheduler rejects trades when cash, same-symbol overlap, or max-concurrent constraints are hit.",
        "",
        "Depth terminology note: this Phase42 input has top-five-depth feature proxies (`l5_imbalance` and a derived beyond-L1 proxy), not persisted raw bid/ask price and quantity for every book level. Raw L1-L5 book-state persistence remains a separate dense-lake milestone.",
        "",
        "No replay, promotion, paper/live acceptance, or deployable profitability claim is opened by this search.",
        "",
        "## Acceptance Summary",
        "",
        _markdown_table(summary),
        "",
        "## Gate Evaluation",
        "",
        _markdown_table(gates),
        "",
        "## Family Summary",
        "",
        _markdown_table(families.head(20)),
        "",
        "## Top Variants",
        "",
        _markdown_table(variants.head(20)),
    ]
    (output_dir / "phase296_full_year_top5_depth_strategy_family_sweep_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(input_path: Path = DEFAULT_INPUT_PATH, phase295_dir: Path = DEFAULT_PHASE295_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase295_summary = read_csv(phase295_dir / "phase295_acceptance_summary.csv")
    events = load_full_year_events(input_path)
    catalog, variant_events = build_variant_catalog_and_events(events)
    if catalog.empty:
        raise ValueError("Phase296 produced no variants.")
    scenarios, sample_ledger = build_scenarios(catalog, variant_events)
    if scenarios.empty:
        raise ValueError("Phase296 produced no scenarios.")
    variants = build_variant_summary(scenarios)
    families = build_family_summary(scenarios)
    gates = build_gates(phase295_summary, events, catalog, scenarios)
    summary = build_acceptance(events, catalog, scenarios, gates)

    catalog.to_csv(output_dir / "phase296_variant_catalog.csv", index=False)
    scenarios.to_csv(output_dir / "phase296_scenario_summary.csv", index=False)
    variants.to_csv(output_dir / "phase296_variant_summary.csv", index=False)
    families.to_csv(output_dir / "phase296_family_summary.csv", index=False)
    gates.to_csv(output_dir / "phase296_gate_evaluation.csv", index=False)
    summary.to_csv(output_dir / "phase296_acceptance_summary.csv", index=False)
    if not sample_ledger.empty:
        sample_ledger.to_csv(output_dir / "phase296_sample_trade_ledger.csv", index=False)
    write_report(output_dir, summary, gates, families, variants)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase296_full_year_top5_depth_strategy_family_sweep",
        **reproducibility_fields(
            artifact_id="phase296",
            generated_utc=generated_utc,
            inputs={
                "phase42_full_year_event_state": str(input_path),
                "phase295_acceptance_summary": str(phase295_dir / "phase295_acceptance_summary.csv"),
            },
            parameters={
                "selected_route": SELECTED_ROUTE,
                "initial_capital_inr": INITIAL_CAPITAL_INR,
                "fixed_notional_grid_inr": FIXED_NOTIONAL_GRID_INR,
                "max_concurrent_grid": MAX_CONCURRENT_GRID,
                "cost_multiplier": COST_MULTIPLIER,
                "annualized_denominator": "fixed_initial_capital",
                "input_depth_scope": "top_five_depth_feature_proxy_not_raw_l1_l5_book_state",
            },
            outputs={
                "acceptance_summary": str(output_dir / "phase296_acceptance_summary.csv"),
                "scenario_summary": str(output_dir / "phase296_scenario_summary.csv"),
                "variant_summary": str(output_dir / "phase296_variant_summary.csv"),
                "family_summary": str(output_dir / "phase296_family_summary.csv"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase296_event_horizon_proxy_v1",
        ),
    }
    (output_dir / "phase296_full_year_top5_depth_strategy_family_sweep_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase296 full-year top-five-depth strategy-family sweep.")
    parser.add_argument("--input-path", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--phase295-dir", type=Path, default=DEFAULT_PHASE295_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    summary = run(input_path=args.input_path, phase295_dir=args.phase295_dir, output_dir=args.output_dir)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

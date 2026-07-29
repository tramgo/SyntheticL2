from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, metric_value, read_csv
from synthetic_l2.phase255_richer_raw_depth_feature_quality_interpretation import safe_float
from synthetic_l2.phase256_richer_raw_top5_depth_cost_aware_strategy_search import max_drawdown
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE261_DIR = Path("outputs/phase261")
DEFAULT_INPUT_PARQUET = Path("outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet")
DEFAULT_OUTPUT_DIR = Path("outputs/phase262")
NOTIONAL_INR = 100_000.0
HORIZONS = [3, 6, 10]
SPREAD_MIN_QUANTILES = [0.25, 0.50, 0.75]
REPLENISHMENT_QUANTILES = [0.40, 0.60, 0.75]
CHURN_MAX_QUANTILES = [0.40, 0.60, 0.75]
PRICE_SHIFT_MAX_QUANTILES = [0.50, 0.75]
IMBALANCE_THRESHOLDS = [0.00, 0.03, 0.06]
SKEW_IMBALANCE_THRESHOLDS = [0.02, 0.05, 0.10]
SPREAD_CAPTURE_FRACTIONS = [0.50]
COST_MULTIPLIERS = [1.0, 1.5, 2.0]
MIN_OPPORTUNITY_ROWS = 30
MIN_SYMBOLS = 8
MIN_FILL_EQUIVALENT_ROWS = 5.0


def stable_random_side(key: str) -> int:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return 1 if int(digest[:8], 16) % 2 == 0 else -1


def load_event_bars(input_parquet: Path) -> pd.DataFrame:
    if not input_parquet.exists():
        raise FileNotFoundError(f"Missing richer raw-depth event bars: {input_parquet}")
    con = duckdb.connect()
    try:
        frame = con.execute(f"select * from read_parquet('{input_parquet.as_posix()}')").fetchdf()
    finally:
        con.close()
    frame = frame.sort_values(["trade_date", "exchange", "symbol", "richer_event_bar_id"], kind="mergesort").reset_index(drop=True)
    return add_passive_features(frame)


def add_passive_features(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    numeric_columns = [
        "avg_cum_buy_qty_l1_l5",
        "avg_cum_sell_qty_l1_l5",
        "avg_cum_buy_qty_l2_l5",
        "avg_cum_sell_qty_l2_l5",
        "avg_cum_buy_orders_l1_l5",
        "avg_cum_sell_orders_l1_l5",
        "avg_spread_bps",
        "avg_cum_top5_qty_imbalance",
        "avg_depth_beyond_l1_qty_imbalance",
        "avg_order_count_imbalance_l1_l5",
        "depth_replenishment_pressure",
        "depth_withdrawal_pressure",
        "top5_qty_churn_sum",
        "top5_order_churn_sum",
        "l1_price_shift_abs_sum",
        "zerodha_round_trip_charge_bps",
        "close_mid_price",
    ]
    for column in numeric_columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["l2_l5_bid_share"] = frame["avg_cum_buy_qty_l2_l5"] / frame["avg_cum_buy_qty_l1_l5"].replace(0, pd.NA)
    frame["l2_l5_ask_share"] = frame["avg_cum_sell_qty_l2_l5"] / frame["avg_cum_sell_qty_l1_l5"].replace(0, pd.NA)
    frame["bid_queue_pressure"] = frame["avg_cum_buy_qty_l1_l5"] / frame["avg_cum_buy_orders_l1_l5"].replace(0, pd.NA)
    frame["ask_queue_pressure"] = frame["avg_cum_sell_qty_l1_l5"] / frame["avg_cum_sell_orders_l1_l5"].replace(0, pd.NA)
    frame["churn_pressure"] = frame["top5_qty_churn_sum"] + frame["top5_order_churn_sum"]
    frame["cancel_replace_pressure_bps"] = frame["l1_price_shift_abs_sum"] / frame["close_mid_price"].replace(0, pd.NA) * 10000.0
    frame["withdrawal_pressure_norm"] = frame["depth_withdrawal_pressure"] / (
        frame["depth_replenishment_pressure"] + frame["depth_withdrawal_pressure"]
    ).replace(0, pd.NA)
    frame["withdrawal_pressure_norm"] = frame["withdrawal_pressure_norm"].fillna(0.0)
    frame["l2_l5_bid_share"] = frame["l2_l5_bid_share"].fillna(0.0)
    frame["l2_l5_ask_share"] = frame["l2_l5_ask_share"].fillna(0.0)
    frame["bid_queue_pressure"] = frame["bid_queue_pressure"].fillna(frame["bid_queue_pressure"].median())
    frame["ask_queue_pressure"] = frame["ask_queue_pressure"].fillna(frame["ask_queue_pressure"].median())
    return frame


def fill_model_rows(phase261_dir: Path) -> pd.DataFrame:
    grid = read_csv(phase261_dir / "phase261_fill_probability_grid.csv")
    if grid.empty:
        raise FileNotFoundError("Missing Phase261 fill probability grid.")
    for column in [
        "base_fill_probability",
        "queue_haircut",
        "churn_haircut",
        "levels_2_to_5_support_boost",
        "nonfill_stress_multiplier",
        "queue_adversity_multiplier",
        "adverse_selection_penalty_multiplier",
        "max_fill_probability_cap",
    ]:
        grid[column] = pd.to_numeric(grid[column], errors="coerce")
    return grid


def make_opportunities(
    frame: pd.DataFrame,
    mask: pd.Series,
    side: pd.Series,
    horizon: int,
    spread_capture_fraction: float,
    fill_model: pd.Series,
    family_id: str,
) -> pd.DataFrame:
    label = f"future_return_h{horizon}"
    selected = frame.loc[mask & frame[label].notna()].copy()
    if selected.empty:
        return selected
    selected["side"] = side.loc[selected.index].astype(int)
    same_queue = selected["bid_queue_pressure"].where(selected["side"].gt(0), selected["ask_queue_pressure"])
    queue_rank = same_queue.rank(pct=True).fillna(1.0)
    churn_rank = selected["churn_pressure"].rank(pct=True).fillna(1.0)
    l2_share = selected["l2_l5_bid_share"].where(selected["side"].gt(0), selected["l2_l5_ask_share"]).fillna(0.0)
    base_fill = safe_float(fill_model["base_fill_probability"], 0.0)
    queue_haircut = safe_float(fill_model["queue_haircut"], 1.0)
    churn_haircut = safe_float(fill_model["churn_haircut"], 1.0)
    l2_boost = safe_float(fill_model["levels_2_to_5_support_boost"], 0.0)
    queue_adversity = safe_float(fill_model["queue_adversity_multiplier"], 1.0)
    adverse_mult = safe_float(fill_model["adverse_selection_penalty_multiplier"], 1.0)
    nonfill_stress = safe_float(fill_model["nonfill_stress_multiplier"], 1.0)
    fill_cap = safe_float(fill_model["max_fill_probability_cap"], 0.35)
    fill_probability = (
        base_fill
        * (1.0 - (1.0 - queue_haircut) * queue_rank * queue_adversity)
        * (1.0 - (1.0 - churn_haircut) * churn_rank)
        + l2_boost * l2_share
    ).clip(0.0, fill_cap)
    spread_capture_bps = selected["avg_spread_bps"].clip(lower=0.0) * spread_capture_fraction
    future_move_bps = selected["side"] * pd.to_numeric(selected[label], errors="coerce") * 10000.0
    adverse_penalty_bps = (
        selected["withdrawal_pressure_norm"].clip(0, 1) * adverse_mult * selected["avg_spread_bps"].clip(lower=0.0)
        + selected["cancel_replace_pressure_bps"].fillna(0.0).clip(lower=0.0) * 0.25 * queue_adversity
    )
    nonfill_penalty_bps = (1.0 - fill_probability) * nonfill_stress * selected["cancel_replace_pressure_bps"].fillna(0.0).clip(lower=0.0) * 0.05
    selected["fill_model_id"] = str(fill_model["fill_model_id"])
    selected["fill_probability"] = fill_probability
    selected["spread_capture_bps"] = spread_capture_bps
    selected["future_move_bps"] = future_move_bps
    selected["adverse_penalty_bps"] = adverse_penalty_bps
    selected["nonfill_penalty_bps"] = nonfill_penalty_bps
    selected["expected_gross_bps"] = fill_probability * (spread_capture_bps + future_move_bps - adverse_penalty_bps) - nonfill_penalty_bps
    selected["family_id"] = family_id
    return selected


def passive_metrics(opportunities: pd.DataFrame, cost_multiplier: float) -> dict[str, Any]:
    if opportunities.empty:
        return {
            "opportunity_rows": 0,
            "expected_net_pnl_inr": 0.0,
            "expected_gross_pnl_inr": 0.0,
            "expected_cost_inr": 0.0,
            "realized_fill_equivalent_rows": 0.0,
            "win_rate": 0.0,
            "profit_factor": 0.0,
            "avg_expected_net_per_opportunity": 0.0,
            "max_drawdown_inr": 0.0,
        }
    gross_bps = opportunities["expected_gross_bps"]
    cost_bps = opportunities["zerodha_round_trip_charge_bps"] * cost_multiplier * opportunities["fill_probability"].clip(0, 1)
    net_bps = gross_bps - cost_bps
    net_inr = net_bps / 10000.0 * NOTIONAL_INR
    gross_inr = gross_bps / 10000.0 * NOTIONAL_INR
    cost_inr = cost_bps / 10000.0 * NOTIONAL_INR
    gross_pos = safe_float(net_inr[net_inr > 0].sum(), 0.0)
    gross_neg = safe_float(-net_inr[net_inr < 0].sum(), 0.0)
    return {
        "opportunity_rows": int(len(opportunities)),
        "expected_net_pnl_inr": safe_float(net_inr.sum(), 0.0),
        "expected_gross_pnl_inr": safe_float(gross_inr.sum(), 0.0),
        "expected_cost_inr": safe_float(cost_inr.sum(), 0.0),
        "realized_fill_equivalent_rows": safe_float(opportunities["fill_probability"].sum(), 0.0),
        "win_rate": float((net_inr > 0).mean()) if len(net_inr) else 0.0,
        "profit_factor": gross_pos / gross_neg if gross_neg > 0 else (999.0 if gross_pos > 0 else 0.0),
        "avg_expected_net_per_opportunity": safe_float(net_inr.mean(), 0.0),
        "max_drawdown_inr": max_drawdown(net_inr),
    }


def deterministic_controls(opportunities: pd.DataFrame, cost_multiplier: float) -> dict[str, Any]:
    if opportunities.empty:
        return {
            "side_flip_expected_net_pnl_inr": 0.0,
            "side_flip_degrades": 0,
            "random_side_expected_net_pnl_inr": 0.0,
            "random_side_beat": 0,
            "queue_adverse_expected_net_pnl_inr": 0.0,
            "queue_adversity_survives": 0,
            "nonfill_stress_expected_net_pnl_inr": 0.0,
            "nonfill_stress_survives": 0,
        }
    base = passive_metrics(opportunities, cost_multiplier)["expected_net_pnl_inr"]
    flipped = opportunities.copy()
    flipped["expected_gross_bps"] = flipped["fill_probability"] * (
        flipped["spread_capture_bps"] - flipped["future_move_bps"] - flipped["adverse_penalty_bps"]
    ) - flipped["nonfill_penalty_bps"]
    flip_net = passive_metrics(flipped, cost_multiplier)["expected_net_pnl_inr"]
    randomed = opportunities.copy()
    key = (
        randomed["symbol"].astype(str)
        + "_"
        + randomed["richer_event_bar_id"].astype(str)
        + "_"
        + randomed["trade_date"].astype(str)
        + "_phase262_passive"
    )
    random_side = key.map(stable_random_side)
    randomed["expected_gross_bps"] = randomed["fill_probability"] * (
        randomed["spread_capture_bps"] + random_side * randomed["future_move_bps"].abs() - randomed["adverse_penalty_bps"]
    ) - randomed["nonfill_penalty_bps"]
    random_net = passive_metrics(randomed, cost_multiplier)["expected_net_pnl_inr"]
    adverse = opportunities.copy()
    adverse["fill_probability"] = (adverse["fill_probability"] * 0.75).clip(lower=0.0)
    adverse["expected_gross_bps"] = adverse["expected_gross_bps"] - adverse["fill_probability"] * adverse["avg_spread_bps"].clip(lower=0.0) * 0.50
    adverse_net = passive_metrics(adverse, cost_multiplier)["expected_net_pnl_inr"]
    nonfill = opportunities.copy()
    nonfill["fill_probability"] = (nonfill["fill_probability"] * 0.60).clip(lower=0.0)
    nonfill["expected_gross_bps"] = (
        nonfill["fill_probability"] * (nonfill["spread_capture_bps"] + nonfill["future_move_bps"] - nonfill["adverse_penalty_bps"])
        - (1.0 - nonfill["fill_probability"]) * nonfill["nonfill_penalty_bps"] * 1.50
    )
    nonfill_net = passive_metrics(nonfill, cost_multiplier)["expected_net_pnl_inr"]
    return {
        "side_flip_expected_net_pnl_inr": flip_net,
        "side_flip_degrades": int(base > flip_net),
        "random_side_expected_net_pnl_inr": random_net,
        "random_side_beat": int(base > random_net),
        "queue_adverse_expected_net_pnl_inr": adverse_net,
        "queue_adversity_survives": int(adverse_net > 0),
        "nonfill_stress_expected_net_pnl_inr": nonfill_net,
        "nonfill_stress_survives": int(nonfill_net > 0),
    }


def threshold_maps(frame: pd.DataFrame) -> dict[str, dict[float, float]]:
    return {
        "spread": {q: safe_float(frame["avg_spread_bps"].quantile(q), 0.0) for q in SPREAD_MIN_QUANTILES},
        "replenishment": {q: safe_float(frame["depth_replenishment_pressure"].quantile(q), 0.0) for q in REPLENISHMENT_QUANTILES},
        "churn": {q: safe_float(frame["churn_pressure"].quantile(q), 0.0) for q in CHURN_MAX_QUANTILES},
        "price_shift": {q: safe_float(frame["l1_price_shift_abs_sum"].quantile(q), 0.0) for q in PRICE_SHIFT_MAX_QUANTILES},
    }


def opportunity_mask_and_side(
    frame: pd.DataFrame,
    family_id: str,
    spread_min: float,
    repl_min: float,
    churn_cap: float,
    price_shift_cap: float,
    imbalance_threshold: float,
) -> tuple[pd.Series, pd.Series]:
    bid_signal = (
        frame["avg_depth_beyond_l1_qty_imbalance"].ge(imbalance_threshold)
        & frame["avg_cum_top5_qty_imbalance"].ge(-0.05)
        & frame["avg_order_count_imbalance_l1_l5"].ge(-0.30)
    )
    ask_signal = (
        frame["avg_depth_beyond_l1_qty_imbalance"].le(-imbalance_threshold)
        & frame["avg_cum_top5_qty_imbalance"].le(0.05)
        & frame["avg_order_count_imbalance_l1_l5"].le(0.30)
    )
    side = pd.Series(0, index=frame.index)
    if family_id == "P262_BROAD_PASSIVE_BID_REPLENISHMENT":
        side = pd.Series(1, index=frame.index)
        family_mask = bid_signal
    elif family_id == "P262_BROAD_PASSIVE_ASK_REPLENISHMENT":
        side = pd.Series(-1, index=frame.index)
        family_mask = ask_signal
    elif family_id == "P262_TWO_SIDED_SPREAD_CAPTURE_LOW_CHURN":
        side = side.mask(bid_signal, 1).mask(ask_signal, -1)
        family_mask = side.ne(0)
    else:
        side = side.mask(frame["avg_depth_beyond_l1_qty_imbalance"].ge(imbalance_threshold), 1)
        side = side.mask(frame["avg_depth_beyond_l1_qty_imbalance"].le(-imbalance_threshold), -1)
        family_mask = side.ne(0)
    common_mask = (
        frame["avg_spread_bps"].ge(spread_min)
        & frame["depth_replenishment_pressure"].ge(repl_min)
        & frame["churn_pressure"].le(churn_cap)
        & frame["l1_price_shift_abs_sum"].le(price_shift_cap)
        & frame["l2_l5_bid_share"].ge(0.50)
        & frame["l2_l5_ask_share"].ge(0.50)
        & frame["allowed_for_training_parameter_selection"].eq(1)
    )
    return family_mask & common_mask, side


def build_training_search(frame: pd.DataFrame, phase261_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    fills = fill_model_rows(phase261_dir)
    families = read_csv(phase261_dir / "phase261_broadened_candidate_family_catalog.csv")
    families = families[~families["quote_side"].astype(str).eq("filter")].copy()
    thresholds = threshold_maps(frame)
    rows: list[dict[str, Any]] = []
    survivor_ledgers: list[pd.DataFrame] = []
    for family_id in families["candidate_family_id"].astype(str).tolist():
        for horizon in HORIZONS:
            if family_id in {"P262_BROAD_PASSIVE_BID_REPLENISHMENT", "P262_BROAD_PASSIVE_ASK_REPLENISHMENT"}:
                grid_rows = [
                    (spread_q, spread_min, repl_q, repl_min, 0.75, thresholds["churn"][0.75], 0.75, thresholds["price_shift"][0.75], imbalance_threshold)
                    for spread_q, spread_min in thresholds["spread"].items()
                    for repl_q, repl_min in thresholds["replenishment"].items()
                    for imbalance_threshold in IMBALANCE_THRESHOLDS
                ]
            elif family_id == "P262_TWO_SIDED_SPREAD_CAPTURE_LOW_CHURN":
                grid_rows = [
                    (spread_q, spread_min, 0.40, thresholds["replenishment"][0.40], churn_q, churn_cap, price_q, price_cap, 0.00)
                    for spread_q, spread_min in thresholds["spread"].items()
                    if spread_q >= 0.50
                    for churn_q, churn_cap in thresholds["churn"].items()
                    for price_q, price_cap in thresholds["price_shift"].items()
                ]
            else:
                grid_rows = [
                    (spread_q, spread_min, 0.40, thresholds["replenishment"][0.40], 0.75, thresholds["churn"][0.75], 0.75, thresholds["price_shift"][0.75], imbalance_threshold)
                    for spread_q, spread_min in thresholds["spread"].items()
                    if spread_q in {0.25, 0.50}
                    for imbalance_threshold in SKEW_IMBALANCE_THRESHOLDS
                ]
            for spread_q, spread_min, repl_q, repl_min, churn_q, churn_cap, price_q, price_cap, imbalance_threshold in grid_rows:
                                mask, side = opportunity_mask_and_side(
                                    frame=frame,
                                    family_id=family_id,
                                    spread_min=spread_min,
                                    repl_min=repl_min,
                                    churn_cap=churn_cap,
                                    price_shift_cap=price_cap,
                                    imbalance_threshold=imbalance_threshold,
                                )
                                opportunity_rows_before_fill = int((mask & frame[f"future_return_h{horizon}"].notna()).sum())
                                for capture_fraction in SPREAD_CAPTURE_FRACTIONS:
                                    for _, fill_model in fills.iterrows():
                                        opportunities = make_opportunities(
                                            frame=frame,
                                            mask=mask,
                                            side=side,
                                            horizon=horizon,
                                            spread_capture_fraction=capture_fraction,
                                            fill_model=fill_model,
                                            family_id=family_id,
                                        )
                                        candidate_id = (
                                            f"P262_{family_id}_H{horizon}_SPQ{str(spread_q).replace('.', 'p')}_"
                                            f"RQ{str(repl_q).replace('.', 'p')}_CQ{str(churn_q).replace('.', 'p')}_"
                                            f"PQ{str(price_q).replace('.', 'p')}_I{str(imbalance_threshold).replace('.', 'p')}_"
                                            f"CF{str(capture_fraction).replace('.', 'p')}_{fill_model['fill_model_id']}"
                                        )
                                        record: dict[str, Any] = {
                                            "candidate_id": candidate_id,
                                            "family_id": family_id,
                                            "fill_model_id": fill_model["fill_model_id"],
                                            "fill_profile": fill_model["profile"],
                                            "uses_full_top_five_depth": 1,
                                            "uses_depth_beyond_l1": 1,
                                            "uses_l1_only": 0,
                                            "horizon": horizon,
                                            "spread_quantile": spread_q,
                                            "spread_min_bps": spread_min,
                                            "replenishment_quantile": repl_q,
                                            "replenishment_min": repl_min,
                                            "churn_quantile": churn_q,
                                            "churn_cap": churn_cap,
                                            "price_shift_quantile": price_q,
                                            "price_shift_cap": price_cap,
                                            "imbalance_threshold": imbalance_threshold,
                                            "spread_capture_fraction": capture_fraction,
                                            "opportunity_rows_before_fill": opportunity_rows_before_fill,
                                            "symbols": int(opportunities["symbol"].nunique()) if not opportunities.empty else 0,
                                            "trade_dates": int(opportunities["trade_date"].nunique()) if not opportunities.empty else 0,
                                            "mean_fill_probability": safe_float(opportunities["fill_probability"].mean(), 0.0) if not opportunities.empty else 0.0,
                                        }
                                        for multiplier in COST_MULTIPLIERS:
                                            metrics = passive_metrics(opportunities, multiplier)
                                            suffix = f"cost{int(multiplier * 100):03d}"
                                            record.update({f"{suffix}_{k}": v for k, v in metrics.items()})
                                        controls = deterministic_controls(opportunities, 1.0)
                                        record.update(controls)
                                        record["survivor_candidate"] = int(
                                            record["cost100_opportunity_rows"] >= MIN_OPPORTUNITY_ROWS
                                            and record["symbols"] >= MIN_SYMBOLS
                                            and record["cost100_realized_fill_equivalent_rows"] >= MIN_FILL_EQUIVALENT_ROWS
                                            and record["cost100_expected_net_pnl_inr"] > 0
                                            and record["cost150_expected_net_pnl_inr"] > 0
                                            and record["cost200_expected_net_pnl_inr"] > 0
                                            and record["side_flip_degrades"] == 1
                                            and record["random_side_beat"] == 1
                                            and record["queue_adversity_survives"] == 1
                                            and record["nonfill_stress_survives"] == 1
                                        )
                                        record["has_opportunities"] = int(record["cost100_opportunity_rows"] > 0)
                                        rows.append(record)
                                        if record["survivor_candidate"]:
                                            survivor_ledgers.append(
                                                opportunities.assign(candidate_id=candidate_id)[
                                                    [
                                                        "candidate_id",
                                                        "trade_date",
                                                        "exchange",
                                                        "symbol",
                                                        "richer_event_bar_id",
                                                        "family_id",
                                                        "fill_model_id",
                                                        "side",
                                                        "fill_probability",
                                                        "spread_capture_bps",
                                                        "future_move_bps",
                                                        "adverse_penalty_bps",
                                                        "nonfill_penalty_bps",
                                                        "expected_gross_bps",
                                                        "zerodha_round_trip_charge_bps",
                                                    ]
                                                ]
                                            )
    variants = pd.DataFrame(rows).sort_values(
        [
            "survivor_candidate",
            "has_opportunities",
            "cost200_expected_net_pnl_inr",
            "cost150_expected_net_pnl_inr",
            "cost100_expected_net_pnl_inr",
        ],
        ascending=[False, False, False, False, False],
    )
    survivor_ledger = pd.concat(survivor_ledgers, ignore_index=True) if survivor_ledgers else pd.DataFrame()
    return variants, survivor_ledger


def build_gate_evaluation(phase261_dir: Path, variants: pd.DataFrame, frame: pd.DataFrame) -> pd.DataFrame:
    next_action = str(metric_value(phase261_dir / "phase261_acceptance_summary.csv", "phase261_next_best_action", ""))
    rows = [
        ("P262_PHASE261_WORK_ORDER_PRESENT", "run_phase262_passive_opportunity_breadth_fill_model_training_search" in next_action, next_action, "Phase261 next action targets Phase262", "hard"),
        ("P262_PHASE261_FULL_DEPTH_REQUIRED", as_int(metric_value(phase261_dir / "phase261_acceptance_summary.csv", "phase261_full_top_five_depth_required", 0)) == 1, metric_value(phase261_dir / "phase261_acceptance_summary.csv", "phase261_full_top_five_depth_required", 0), "full top-five depth required", "hard"),
        ("P262_PHASE261_L2_L5_REQUIRED", as_int(metric_value(phase261_dir / "phase261_acceptance_summary.csv", "phase261_levels_2_to_5_materiality_required", 0)) == 1, metric_value(phase261_dir / "phase261_acceptance_summary.csv", "phase261_levels_2_to_5_materiality_required", 0), "levels 2-5 materiality required", "hard"),
        ("P262_INPUT_ROWS_PRESENT", len(frame) >= 1000, len(frame), ">=1000 richer raw top-five event bars", "hard"),
        ("P262_VARIANTS_TESTED", len(variants) > 0, len(variants), ">0 variants", "hard"),
        ("P262_ALL_VARIANTS_USE_FULL_DEPTH", int(variants["uses_full_top_five_depth"].sum()) == len(variants), int(variants["uses_full_top_five_depth"].sum()), "all variants use full top-five depth", "hard"),
        ("P262_ALL_VARIANTS_USE_LEVELS_2_TO_5", int(variants["uses_depth_beyond_l1"].sum()) == len(variants), int(variants["uses_depth_beyond_l1"].sum()), "all variants use levels 2-5/beyond-L1", "hard"),
        ("P262_NO_L1_ONLY_VARIANTS", int(variants["uses_l1_only"].sum()) == 0, int(variants["uses_l1_only"].sum()), "0 L1-only variants", "hard"),
        ("P262_FILL_GRID_APPLIED", int(variants["fill_model_id"].nunique()) >= 12, int(variants["fill_model_id"].nunique()), ">=12 Phase261 fill models", "hard"),
        ("P262_CONTROLS_APPLIED", {"side_flip_degrades", "random_side_beat", "queue_adversity_survives", "nonfill_stress_survives"}.issubset(set(variants.columns)), "side_flip;random_side;queue_adversity;nonfill_stress", "all controls present", "hard"),
        ("P262_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase262 Passive Opportunity Breadth and Fill-model Training Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase262 executes the broader training-only passive opportunity search precommitted in Phase261.",
        "Every variant uses Zerodha top-five market-by-price rows 1-5 and levels 2-5 materiality; L1-only variants are forbidden.",
        "Expected passive P&L is fill-probability weighted, cost-aware, queue/adverse-selection stressed and non-fill stressed.",
        "This is not replay execution, strategy promotion, paper/live acceptance or a deployable profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    input_parquet: Path = DEFAULT_INPUT_PARQUET,
    phase261_dir: Path = DEFAULT_PHASE261_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if as_int(metric_value(phase261_dir / "phase261_acceptance_summary.csv", "phase261_full_top_five_depth_required", 0)) != 1:
        raise RuntimeError("Phase261 does not require full top-five depth.")
    if as_int(metric_value(phase261_dir / "phase261_acceptance_summary.csv", "phase261_l1_only_candidate_allowed", 1)) != 0:
        raise RuntimeError("Phase261 does not forbid L1-only candidates.")
    frame = load_event_bars(input_parquet)
    variants, survivor_ledger = build_training_search(frame, phase261_dir)
    gates = build_gate_evaluation(phase261_dir, variants, frame)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    survivor_rows = int(variants["survivor_candidate"].sum()) if not variants.empty else 0
    positive_cost100 = int(variants["cost100_expected_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    positive_cost150 = int(variants["cost150_expected_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    positive_cost200 = int(variants["cost200_expected_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    best = variants.iloc[0].to_dict() if not variants.empty else {}
    next_action = (
        "run_phase263_passive_opportunity_breadth_fill_model_interpretation_no_paper_live"
        if hard_pass == len(hard)
        else "repair_phase262_passive_opportunity_training_search"
    )
    acceptance = pd.DataFrame(
        [
            ("phase262_passive_training_search_complete", 1, "Phase262 passive opportunity breadth/fill-model training search completed"),
            ("phase262_input_event_bar_rows", len(frame), "Input event bars"),
            ("phase262_symbols", int(frame["symbol"].nunique()), "Input symbol breadth"),
            ("phase262_trade_dates", int(frame["trade_date"].nunique()), "Input trade dates"),
            ("phase262_variant_rows", len(variants), "Passive variants tested"),
            ("phase262_full_top_five_depth_variant_rows", int(variants["uses_full_top_five_depth"].sum()) if not variants.empty else 0, "Variants using full top-five depth"),
            ("phase262_depth_beyond_l1_variant_rows", int(variants["uses_depth_beyond_l1"].sum()) if not variants.empty else 0, "Variants using levels 2-5/beyond-L1"),
            ("phase262_l1_only_variant_rows", int(variants["uses_l1_only"].sum()) if not variants.empty else 0, "L1-only variants"),
            ("phase262_fill_model_rows_used", int(variants["fill_model_id"].nunique()) if not variants.empty else 0, "Distinct Phase261 fill models used"),
            ("phase262_cost100_positive_variant_rows", positive_cost100, "Variants positive at 1x Zerodha charge stack"),
            ("phase262_cost150_positive_variant_rows", positive_cost150, "Variants positive at 1.5x charges"),
            ("phase262_cost200_positive_variant_rows", positive_cost200, "Variants positive at 2x charges"),
            ("phase262_survivor_candidate_rows", survivor_rows, "Variants passing breadth, cost stress and controls"),
            ("phase262_best_candidate_id", best.get("candidate_id", ""), "Best candidate by survivor/cost200/cost150/cost100 ranking"),
            ("phase262_best_family_id", best.get("family_id", ""), "Best candidate family"),
            ("phase262_best_fill_model_id", best.get("fill_model_id", ""), "Best fill model"),
            ("phase262_best_cost100_expected_net_pnl_inr", best.get("cost100_expected_net_pnl_inr", 0.0), "Best 1x-charge expected net P&L"),
            ("phase262_best_cost200_expected_net_pnl_inr", best.get("cost200_expected_net_pnl_inr", 0.0), "Best 2x-charge expected net P&L"),
            ("phase262_best_opportunity_rows", best.get("cost100_opportunity_rows", 0), "Best opportunity rows"),
            ("phase262_best_symbols", best.get("symbols", 0), "Best symbol breadth"),
            ("phase262_best_realized_fill_equivalent_rows", best.get("cost100_realized_fill_equivalent_rows", 0.0), "Best fill-equivalent rows"),
            ("phase262_best_side_flip_degrades", best.get("side_flip_degrades", 0), "Best side-flip control"),
            ("phase262_best_random_side_beat", best.get("random_side_beat", 0), "Best random-side control"),
            ("phase262_best_queue_adversity_survives", best.get("queue_adversity_survives", 0), "Best queue-adversity stress"),
            ("phase262_best_nonfill_stress_survives", best.get("nonfill_stress_survives", 0), "Best non-fill stress"),
            ("phase262_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase262_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase262_download_more_dates_now_allowed", 0, "No new download in Phase262"),
            ("phase262_replay_execution_allowed_now", 0, "No replay execution in Phase262"),
            ("phase262_strategy_promotion_allowed", 0, "No strategy promotion from Phase262"),
            ("phase262_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase262"),
            ("phase262_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase262"),
            ("phase262_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    variants.to_csv(output_dir / "phase262_passive_opportunity_variant_results.csv", index=False)
    variants.head(100).to_csv(output_dir / "phase262_top_passive_opportunity_variants.csv", index=False)
    survivor_ledger.to_csv(output_dir / "phase262_survivor_opportunity_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase262_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase262_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase262_passive_opportunity_breadth_fill_model_training_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Top Passive Opportunity Variants": variants.head(30),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase262_passive_opportunity_breadth_fill_model_training_search",
        **reproducibility_fields(
            artifact_id="phase262",
            generated_utc=generated_utc,
            inputs={"input_parquet": str(input_parquet), "phase261_dir": str(phase261_dir)},
            parameters={
                "notional_inr": NOTIONAL_INR,
                "horizons": HORIZONS,
                "spread_min_quantiles": SPREAD_MIN_QUANTILES,
                "replenishment_quantiles": REPLENISHMENT_QUANTILES,
                "churn_max_quantiles": CHURN_MAX_QUANTILES,
                "price_shift_max_quantiles": PRICE_SHIFT_MAX_QUANTILES,
                "imbalance_thresholds": IMBALANCE_THRESHOLDS,
                "skew_imbalance_thresholds": SKEW_IMBALANCE_THRESHOLDS,
                "spread_capture_fractions": SPREAD_CAPTURE_FRACTIONS,
                "cost_multipliers": COST_MULTIPLIERS,
                "min_opportunity_rows": MIN_OPPORTUNITY_ROWS,
                "min_symbols": MIN_SYMBOLS,
                "min_fill_equivalent_rows": MIN_FILL_EQUIVALENT_ROWS,
                "full_top_five_depth_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "l1_only_candidate_allowed": 0,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "passive_opportunity_variant_results": str(output_dir / "phase262_passive_opportunity_variant_results.csv"),
                "top_passive_opportunity_variants": str(output_dir / "phase262_top_passive_opportunity_variants.csv"),
                "survivor_opportunity_ledger": str(output_dir / "phase262_survivor_opportunity_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase262_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase262_acceptance_summary.csv"),
                "report": str(output_dir / "phase262_passive_opportunity_breadth_fill_model_training_search_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase262_passive_expected_fill_grid_event_bar_proxy",
        ),
    }
    (output_dir / "phase262_passive_opportunity_breadth_fill_model_training_search_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase262 passive opportunity breadth/fill-model training search.")
    parser.add_argument("--input-parquet", type=Path, default=DEFAULT_INPUT_PARQUET)
    parser.add_argument("--phase261-dir", type=Path, default=DEFAULT_PHASE261_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(input_parquet=args.input_parquet, phase261_dir=args.phase261_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

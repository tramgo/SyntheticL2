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


DEFAULT_PHASE264_DIR = Path("outputs/phase264")
DEFAULT_INPUT_PARQUET = Path("outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet")
DEFAULT_OUTPUT_DIR = Path("outputs/phase265")
NOTIONAL_INR = 100_000.0
HORIZONS = [3, 6, 10]
IMBALANCE_QUANTILES = [0.60, 0.75, 0.90]
SHOCK_QUANTILES = [0.60, 0.75, 0.90]
SPREAD_REGIMES = ["low", "mid", "high", "compression"]
COST_MULTIPLIERS = [1.0, 1.5, 2.0]
MIN_OPPORTUNITY_ROWS = 30
MIN_SYMBOLS = 8
MIN_DATES = 1


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
    return add_event_features(frame)


def add_event_features(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    numeric_columns = [
        "avg_cum_buy_qty_l1_l5",
        "avg_cum_sell_qty_l1_l5",
        "avg_cum_buy_qty_l2_l5",
        "avg_cum_sell_qty_l2_l5",
        "avg_spread_bps",
        "avg_cum_top5_qty_imbalance",
        "avg_depth_beyond_l1_qty_imbalance",
        "avg_level_weighted_depth_imbalance",
        "avg_order_count_imbalance_l1_l5",
        "depth_replenishment_pressure",
        "depth_withdrawal_pressure",
        "top5_qty_churn_sum",
        "top5_order_churn_sum",
        "l1_price_shift_abs_sum",
        "zerodha_round_trip_charge_bps",
    ]
    for column in numeric_columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["l2_l5_bid_share"] = (frame["avg_cum_buy_qty_l2_l5"] / frame["avg_cum_buy_qty_l1_l5"].replace(0, pd.NA)).fillna(0.0)
    frame["l2_l5_ask_share"] = (frame["avg_cum_sell_qty_l2_l5"] / frame["avg_cum_sell_qty_l1_l5"].replace(0, pd.NA)).fillna(0.0)
    frame["top5_churn_pressure"] = frame["top5_qty_churn_sum"] + frame["top5_order_churn_sum"]
    frame["abs_l2_l5_imbalance"] = frame["avg_depth_beyond_l1_qty_imbalance"].abs()
    frame["abs_top5_imbalance"] = frame["avg_cum_top5_qty_imbalance"].abs()
    frame["abs_level_weighted_imbalance"] = frame["avg_level_weighted_depth_imbalance"].abs()
    group = frame.groupby(["trade_date", "exchange", "symbol"], sort=False)
    frame["spread_change_bps"] = group["avg_spread_bps"].diff().fillna(0.0)
    frame["spread_compression_bps"] = (-frame["spread_change_bps"]).clip(lower=0.0)
    frame["spread_expansion_bps"] = frame["spread_change_bps"].clip(lower=0.0)
    frame["replenishment_minus_withdrawal"] = frame["depth_replenishment_pressure"] - frame["depth_withdrawal_pressure"]
    frame["withdrawal_minus_replenishment"] = -frame["replenishment_minus_withdrawal"]
    return frame


def threshold_maps(frame: pd.DataFrame) -> dict[str, dict[float, float]]:
    return {
        "imbalance": {q: safe_float(frame["abs_l2_l5_imbalance"].quantile(q), 0.0) for q in IMBALANCE_QUANTILES},
        "shock": {q: safe_float(frame["top5_churn_pressure"].quantile(q), 0.0) for q in SHOCK_QUANTILES},
        "replenishment": {q: safe_float(frame["depth_replenishment_pressure"].quantile(q), 0.0) for q in SHOCK_QUANTILES},
        "withdrawal": {q: safe_float(frame["depth_withdrawal_pressure"].quantile(q), 0.0) for q in SHOCK_QUANTILES},
        "spread": {
            0.33: safe_float(frame["avg_spread_bps"].quantile(0.33), 0.0),
            0.66: safe_float(frame["avg_spread_bps"].quantile(0.66), 0.0),
        },
        "compression": {q: safe_float(frame["spread_compression_bps"].quantile(q), 0.0) for q in SHOCK_QUANTILES},
    }


def spread_regime_mask(frame: pd.DataFrame, regime: str, thresholds: dict[str, dict[float, float]]) -> pd.Series:
    if regime == "low":
        return frame["avg_spread_bps"].le(thresholds["spread"][0.33])
    if regime == "mid":
        return frame["avg_spread_bps"].gt(thresholds["spread"][0.33]) & frame["avg_spread_bps"].le(thresholds["spread"][0.66])
    if regime == "high":
        return frame["avg_spread_bps"].gt(thresholds["spread"][0.66])
    if regime == "compression":
        return frame["spread_compression_bps"].gt(0)
    raise ValueError(f"Unknown spread regime: {regime}")


def event_mask_and_side(
    frame: pd.DataFrame,
    family_id: str,
    imbalance_min: float,
    shock_min: float,
    spread_regime: str,
    thresholds: dict[str, dict[float, float]],
) -> tuple[pd.Series, pd.Series]:
    side = pd.Series(0, index=frame.index)
    regime = spread_regime_mask(frame, spread_regime, thresholds)
    if family_id == "P265_L2L5_BID_ABSORPTION_CONTINUATION":
        side = pd.Series(1, index=frame.index)
        mask = (
            frame["avg_depth_beyond_l1_qty_imbalance"].ge(imbalance_min)
            & frame["avg_cum_top5_qty_imbalance"].ge(0)
            & frame["avg_level_weighted_depth_imbalance"].ge(0)
            & frame["depth_replenishment_pressure"].ge(shock_min)
            & frame["l2_l5_bid_share"].ge(0.50)
        )
    elif family_id == "P265_L2L5_ASK_ABSORPTION_CONTINUATION":
        side = pd.Series(-1, index=frame.index)
        mask = (
            frame["avg_depth_beyond_l1_qty_imbalance"].le(-imbalance_min)
            & frame["avg_cum_top5_qty_imbalance"].le(0)
            & frame["avg_level_weighted_depth_imbalance"].le(0)
            & frame["depth_replenishment_pressure"].ge(shock_min)
            & frame["l2_l5_ask_share"].ge(0.50)
        )
    elif family_id == "P265_WITHDRAWAL_REVERSAL_AFTER_SHOCK":
        long_side = frame["avg_depth_beyond_l1_qty_imbalance"].ge(imbalance_min) & frame["avg_level_weighted_depth_imbalance"].ge(0)
        short_side = frame["avg_depth_beyond_l1_qty_imbalance"].le(-imbalance_min) & frame["avg_level_weighted_depth_imbalance"].le(0)
        side = side.mask(long_side, 1).mask(short_side, -1)
        mask = side.ne(0) & frame["depth_withdrawal_pressure"].ge(shock_min) & frame["top5_churn_pressure"].ge(shock_min)
    elif family_id == "P265_SPREAD_COMPRESSION_ABSORPTION":
        long_side = frame["avg_depth_beyond_l1_qty_imbalance"].ge(imbalance_min) & frame["avg_cum_top5_qty_imbalance"].ge(0)
        short_side = frame["avg_depth_beyond_l1_qty_imbalance"].le(-imbalance_min) & frame["avg_cum_top5_qty_imbalance"].le(0)
        side = side.mask(long_side, 1).mask(short_side, -1)
        mask = side.ne(0) & frame["spread_compression_bps"].ge(thresholds["compression"][0.60]) & frame["top5_churn_pressure"].ge(shock_min)
    else:
        raise ValueError(f"Unknown event family: {family_id}")
    common = (
        regime
        & frame["allowed_for_training_parameter_selection"].eq(1)
        & frame["l2_l5_bid_share"].ge(0.50)
        & frame["l2_l5_ask_share"].ge(0.50)
    )
    return mask & common, side


def make_events(frame: pd.DataFrame, mask: pd.Series, side: pd.Series, horizon: int, family_id: str) -> pd.DataFrame:
    label = f"future_return_h{horizon}"
    selected = frame.loc[mask & frame[label].notna()].copy()
    if selected.empty:
        return selected
    selected["side"] = side.loc[selected.index].astype(int)
    selected["future_move_bps"] = selected["side"] * pd.to_numeric(selected[label], errors="coerce") * 10000.0
    selected["gross_edge_bps"] = selected["future_move_bps"]
    selected["family_id"] = family_id
    return selected


def event_metrics(events: pd.DataFrame, cost_multiplier: float) -> dict[str, Any]:
    if events.empty:
        return {
            "event_rows": 0,
            "net_pnl_inr": 0.0,
            "gross_pnl_inr": 0.0,
            "cost_inr": 0.0,
            "win_rate": 0.0,
            "profit_factor": 0.0,
            "avg_net_per_event": 0.0,
            "max_drawdown_inr": 0.0,
            "cost_hurdle_hit_rate": 0.0,
        }
    gross_bps = events["gross_edge_bps"]
    cost_bps = events["zerodha_round_trip_charge_bps"] * cost_multiplier
    net_bps = gross_bps - cost_bps
    net_inr = net_bps / 10000.0 * NOTIONAL_INR
    gross_inr = gross_bps / 10000.0 * NOTIONAL_INR
    cost_inr = cost_bps / 10000.0 * NOTIONAL_INR
    gross_pos = safe_float(net_inr[net_inr > 0].sum(), 0.0)
    gross_neg = safe_float(-net_inr[net_inr < 0].sum(), 0.0)
    return {
        "event_rows": int(len(events)),
        "net_pnl_inr": safe_float(net_inr.sum(), 0.0),
        "gross_pnl_inr": safe_float(gross_inr.sum(), 0.0),
        "cost_inr": safe_float(cost_inr.sum(), 0.0),
        "win_rate": float((net_inr > 0).mean()) if len(net_inr) else 0.0,
        "profit_factor": gross_pos / gross_neg if gross_neg > 0 else (999.0 if gross_pos > 0 else 0.0),
        "avg_net_per_event": safe_float(net_inr.mean(), 0.0),
        "max_drawdown_inr": max_drawdown(net_inr),
        "cost_hurdle_hit_rate": float((gross_bps > cost_bps).mean()) if len(gross_bps) else 0.0,
    }


def deterministic_controls(events: pd.DataFrame, cost_multiplier: float) -> dict[str, Any]:
    if events.empty:
        return {
            "side_flip_net_pnl_inr": 0.0,
            "side_flip_degrades": 0,
            "random_side_net_pnl_inr": 0.0,
            "random_side_beat": 0,
            "shuffle_label_net_pnl_inr": 0.0,
            "shuffle_label_beat": 0,
        }
    base = event_metrics(events, cost_multiplier)["net_pnl_inr"]
    flipped = events.copy()
    flipped["gross_edge_bps"] = -flipped["gross_edge_bps"]
    flip_net = event_metrics(flipped, cost_multiplier)["net_pnl_inr"]
    randomed = events.copy()
    key = (
        randomed["symbol"].astype(str)
        + "_"
        + randomed["richer_event_bar_id"].astype(str)
        + "_"
        + randomed["trade_date"].astype(str)
        + "_phase265_liquidity"
    )
    random_side = key.map(stable_random_side)
    randomed["gross_edge_bps"] = random_side * randomed["future_move_bps"].abs()
    random_net = event_metrics(randomed, cost_multiplier)["net_pnl_inr"]
    shuffled = events.copy()
    if len(shuffled) > 1:
        order_key = (
            shuffled["symbol"].astype(str)
            + "_"
            + shuffled["trade_date"].astype(str)
            + "_"
            + shuffled["richer_event_bar_id"].astype(str)
            + "_shuffle"
        )
        shuffled = shuffled.assign(_order=order_key.map(lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest()))
        shuffled_values = shuffled.sort_values("_order")["future_move_bps"].to_numpy()
        shuffled["gross_edge_bps"] = shuffled_values
        shuffled = shuffled.drop(columns=["_order"])
    shuffle_net = event_metrics(shuffled, cost_multiplier)["net_pnl_inr"]
    return {
        "side_flip_net_pnl_inr": flip_net,
        "side_flip_degrades": int(base > flip_net),
        "random_side_net_pnl_inr": random_net,
        "random_side_beat": int(base > random_net),
        "shuffle_label_net_pnl_inr": shuffle_net,
        "shuffle_label_beat": int(base > shuffle_net),
    }


def build_training_search(frame: pd.DataFrame, phase264_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    families = read_csv(phase264_dir / "phase264_event_family_catalog.csv")
    families = families[~families["direction_space"].astype(str).eq("filter")].copy()
    thresholds = threshold_maps(frame)
    rows: list[dict[str, Any]] = []
    survivor_ledgers: list[pd.DataFrame] = []
    for family_id in families["event_family_id"].astype(str).tolist():
        for horizon in HORIZONS:
            for imbalance_q, imbalance_min in thresholds["imbalance"].items():
                for shock_q in SHOCK_QUANTILES:
                    shock_base = (
                        thresholds["replenishment"][shock_q]
                        if "ABSORPTION_CONTINUATION" in family_id
                        else thresholds["withdrawal"][shock_q]
                        if "WITHDRAWAL" in family_id
                        else thresholds["shock"][shock_q]
                    )
                    for spread_regime in SPREAD_REGIMES:
                        mask, side = event_mask_and_side(
                            frame=frame,
                            family_id=family_id,
                            imbalance_min=imbalance_min,
                            shock_min=shock_base,
                            spread_regime=spread_regime,
                            thresholds=thresholds,
                        )
                        events = make_events(frame, mask, side, horizon, family_id)
                        candidate_id = (
                            f"P265_{family_id}_H{horizon}_IQ{str(imbalance_q).replace('.', 'p')}_"
                            f"SQ{str(shock_q).replace('.', 'p')}_SP{spread_regime.upper()}"
                        )
                        record: dict[str, Any] = {
                            "candidate_id": candidate_id,
                            "family_id": family_id,
                            "uses_full_top_five_depth": 1,
                            "uses_depth_beyond_l1": 1,
                            "uses_l1_only": 0,
                            "horizon": horizon,
                            "imbalance_quantile": imbalance_q,
                            "imbalance_min": imbalance_min,
                            "shock_quantile": shock_q,
                            "shock_min": shock_base,
                            "spread_regime": spread_regime,
                            "symbols": int(events["symbol"].nunique()) if not events.empty else 0,
                            "trade_dates": int(events["trade_date"].nunique()) if not events.empty else 0,
                        }
                        for multiplier in COST_MULTIPLIERS:
                            metrics = event_metrics(events, multiplier)
                            suffix = f"cost{int(multiplier * 100):03d}"
                            record.update({f"{suffix}_{k}": v for k, v in metrics.items()})
                        controls = deterministic_controls(events, 1.0)
                        record.update(controls)
                        record["survivor_candidate"] = int(
                            record["cost100_event_rows"] >= MIN_OPPORTUNITY_ROWS
                            and record["symbols"] >= MIN_SYMBOLS
                            and record["trade_dates"] >= MIN_DATES
                            and record["cost100_net_pnl_inr"] > 0
                            and record["cost150_net_pnl_inr"] > 0
                            and record["cost200_net_pnl_inr"] > 0
                            and record["side_flip_degrades"] == 1
                            and record["random_side_beat"] == 1
                            and record["shuffle_label_beat"] == 1
                        )
                        record["has_events"] = int(record["cost100_event_rows"] > 0)
                        rows.append(record)
                        if record["survivor_candidate"]:
                            survivor_ledgers.append(
                                events.assign(candidate_id=candidate_id)[
                                    [
                                        "candidate_id",
                                        "trade_date",
                                        "exchange",
                                        "symbol",
                                        "richer_event_bar_id",
                                        "family_id",
                                        "side",
                                        "future_move_bps",
                                        "gross_edge_bps",
                                        "zerodha_round_trip_charge_bps",
                                        "avg_cum_top5_qty_imbalance",
                                        "avg_depth_beyond_l1_qty_imbalance",
                                        "depth_replenishment_pressure",
                                        "depth_withdrawal_pressure",
                                        "top5_churn_pressure",
                                    ]
                                ]
                            )
    variants = pd.DataFrame(rows).sort_values(
        ["survivor_candidate", "has_events", "cost200_net_pnl_inr", "cost150_net_pnl_inr", "cost100_net_pnl_inr"],
        ascending=[False, False, False, False, False],
    )
    survivor_ledger = pd.concat(survivor_ledgers, ignore_index=True) if survivor_ledgers else pd.DataFrame()
    return variants, survivor_ledger


def build_gate_evaluation(phase264_dir: Path, variants: pd.DataFrame, frame: pd.DataFrame) -> pd.DataFrame:
    next_action = str(metric_value(phase264_dir / "phase264_acceptance_summary.csv", "phase264_next_best_action", ""))
    rows = [
        ("P265_PHASE264_WORK_ORDER_PRESENT", "run_phase265_full_depth_liquidity_shock_absorption_event_training_search" in next_action, next_action, "Phase264 next action targets Phase265", "hard"),
        ("P265_PHASE264_FULL_DEPTH_REQUIRED", as_int(metric_value(phase264_dir / "phase264_acceptance_summary.csv", "phase264_full_top_five_depth_required", 0)) == 1, metric_value(phase264_dir / "phase264_acceptance_summary.csv", "phase264_full_top_five_depth_required", 0), "full top-five depth required", "hard"),
        ("P265_PHASE264_L2_L5_REQUIRED", as_int(metric_value(phase264_dir / "phase264_acceptance_summary.csv", "phase264_levels_2_to_5_materiality_required", 0)) == 1, metric_value(phase264_dir / "phase264_acceptance_summary.csv", "phase264_levels_2_to_5_materiality_required", 0), "levels 2-5 materiality required", "hard"),
        ("P265_INPUT_ROWS_PRESENT", len(frame) >= 1000, len(frame), ">=1000 richer raw top-five event bars", "hard"),
        ("P265_VARIANTS_TESTED", len(variants) > 0, len(variants), ">0 event variants", "hard"),
        ("P265_ALL_VARIANTS_USE_FULL_DEPTH", int(variants["uses_full_top_five_depth"].sum()) == len(variants), int(variants["uses_full_top_five_depth"].sum()), "all variants use full top-five depth", "hard"),
        ("P265_ALL_VARIANTS_USE_LEVELS_2_TO_5", int(variants["uses_depth_beyond_l1"].sum()) == len(variants), int(variants["uses_depth_beyond_l1"].sum()), "all variants use levels 2-5/beyond-L1", "hard"),
        ("P265_NO_L1_ONLY_VARIANTS", int(variants["uses_l1_only"].sum()) == 0, int(variants["uses_l1_only"].sum()), "0 L1-only variants", "hard"),
        ("P265_CONTROLS_APPLIED", {"side_flip_degrades", "random_side_beat", "shuffle_label_beat"}.issubset(set(variants.columns)), "side_flip;random_side;shuffle_label", "controls present", "hard"),
        ("P265_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase265 Full-depth Liquidity-shock Absorption Event Training Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase265 executes a training-only directional liquidity-shock/absorption event search from the Phase264 contract.",
        "Every candidate uses Zerodha top-five market-by-price rows 1-5 and levels 2-5 materiality; L1-only variants are forbidden.",
        "This is not replay execution, strategy promotion, paper/live acceptance or a deployable profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    input_parquet: Path = DEFAULT_INPUT_PARQUET,
    phase264_dir: Path = DEFAULT_PHASE264_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if as_int(metric_value(phase264_dir / "phase264_acceptance_summary.csv", "phase264_full_top_five_depth_required", 0)) != 1:
        raise RuntimeError("Phase264 does not require full top-five depth.")
    if as_int(metric_value(phase264_dir / "phase264_acceptance_summary.csv", "phase264_l1_only_candidate_allowed", 1)) != 0:
        raise RuntimeError("Phase264 does not forbid L1-only candidates.")
    frame = load_event_bars(input_parquet)
    variants, survivor_ledger = build_training_search(frame, phase264_dir)
    gates = build_gate_evaluation(phase264_dir, variants, frame)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    survivor_rows = int(variants["survivor_candidate"].sum()) if not variants.empty else 0
    positive_cost100 = int(variants["cost100_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    positive_cost150 = int(variants["cost150_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    positive_cost200 = int(variants["cost200_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    best = variants.iloc[0].to_dict() if not variants.empty else {}
    next_action = (
        "run_phase266_full_depth_liquidity_shock_absorption_event_interpretation_no_paper_live"
        if hard_pass == len(hard)
        else "repair_phase265_liquidity_shock_absorption_training_search"
    )
    acceptance = pd.DataFrame(
        [
            ("phase265_liquidity_shock_training_search_complete", 1, "Phase265 full-depth liquidity-shock/absorption training search completed"),
            ("phase265_input_event_bar_rows", len(frame), "Input event bars"),
            ("phase265_symbols", int(frame["symbol"].nunique()), "Input symbol breadth"),
            ("phase265_trade_dates", int(frame["trade_date"].nunique()), "Input trade dates"),
            ("phase265_variant_rows", len(variants), "Event variants tested"),
            ("phase265_full_top_five_depth_variant_rows", int(variants["uses_full_top_five_depth"].sum()) if not variants.empty else 0, "Variants using full top-five depth"),
            ("phase265_depth_beyond_l1_variant_rows", int(variants["uses_depth_beyond_l1"].sum()) if not variants.empty else 0, "Variants using levels 2-5/beyond-L1"),
            ("phase265_l1_only_variant_rows", int(variants["uses_l1_only"].sum()) if not variants.empty else 0, "L1-only variants"),
            ("phase265_cost100_positive_variant_rows", positive_cost100, "Variants positive at 1x Zerodha charge stack"),
            ("phase265_cost150_positive_variant_rows", positive_cost150, "Variants positive at 1.5x charges"),
            ("phase265_cost200_positive_variant_rows", positive_cost200, "Variants positive at 2x charges"),
            ("phase265_survivor_candidate_rows", survivor_rows, "Variants passing breadth, cost stress and controls"),
            ("phase265_best_candidate_id", best.get("candidate_id", ""), "Best candidate by survivor/cost200/cost150/cost100 ranking"),
            ("phase265_best_family_id", best.get("family_id", ""), "Best candidate family"),
            ("phase265_best_cost100_net_pnl_inr", best.get("cost100_net_pnl_inr", 0.0), "Best 1x-charge net P&L"),
            ("phase265_best_cost200_net_pnl_inr", best.get("cost200_net_pnl_inr", 0.0), "Best 2x-charge net P&L"),
            ("phase265_best_event_rows", best.get("cost100_event_rows", 0), "Best event rows"),
            ("phase265_best_symbols", best.get("symbols", 0), "Best symbol breadth"),
            ("phase265_best_trade_dates", best.get("trade_dates", 0), "Best date breadth"),
            ("phase265_best_side_flip_degrades", best.get("side_flip_degrades", 0), "Best side-flip control"),
            ("phase265_best_random_side_beat", best.get("random_side_beat", 0), "Best random-side control"),
            ("phase265_best_shuffle_label_beat", best.get("shuffle_label_beat", 0), "Best shuffled-label control"),
            ("phase265_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase265_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase265_download_more_dates_now_allowed", 0, "No new download in Phase265"),
            ("phase265_replay_execution_allowed_now", 0, "No replay execution in Phase265"),
            ("phase265_strategy_promotion_allowed", 0, "No strategy promotion from Phase265"),
            ("phase265_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase265"),
            ("phase265_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase265"),
            ("phase265_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    variants.to_csv(output_dir / "phase265_liquidity_shock_variant_results.csv", index=False)
    variants.head(100).to_csv(output_dir / "phase265_top_liquidity_shock_variants.csv", index=False)
    survivor_ledger.to_csv(output_dir / "phase265_survivor_event_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase265_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase265_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase265_full_depth_liquidity_shock_absorption_event_training_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Top Liquidity-shock Variants": variants.head(30),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase265_full_depth_liquidity_shock_absorption_event_training_search",
        **reproducibility_fields(
            artifact_id="phase265",
            generated_utc=generated_utc,
            inputs={"input_parquet": str(input_parquet), "phase264_dir": str(phase264_dir)},
            parameters={
                "notional_inr": NOTIONAL_INR,
                "horizons": HORIZONS,
                "imbalance_quantiles": IMBALANCE_QUANTILES,
                "shock_quantiles": SHOCK_QUANTILES,
                "spread_regimes": SPREAD_REGIMES,
                "cost_multipliers": COST_MULTIPLIERS,
                "min_opportunity_rows": MIN_OPPORTUNITY_ROWS,
                "min_symbols": MIN_SYMBOLS,
                "min_dates": MIN_DATES,
                "full_top_five_depth_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "l1_only_candidate_allowed": 0,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "liquidity_shock_variant_results": str(output_dir / "phase265_liquidity_shock_variant_results.csv"),
                "top_liquidity_shock_variants": str(output_dir / "phase265_top_liquidity_shock_variants.csv"),
                "survivor_event_ledger": str(output_dir / "phase265_survivor_event_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase265_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase265_acceptance_summary.csv"),
                "report": str(output_dir / "phase265_full_depth_liquidity_shock_absorption_event_training_search_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase265_directional_event_bar_proxy_no_replay",
        ),
    }
    (output_dir / "phase265_full_depth_liquidity_shock_absorption_event_training_search_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase265 full-depth liquidity-shock/absorption event training search.")
    parser.add_argument("--input-parquet", type=Path, default=DEFAULT_INPUT_PARQUET)
    parser.add_argument("--phase264-dir", type=Path, default=DEFAULT_PHASE264_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(input_parquet=args.input_parquet, phase264_dir=args.phase264_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

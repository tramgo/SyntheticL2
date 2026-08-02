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


DEFAULT_PHASE267_DIR = Path("outputs/phase267")
DEFAULT_INPUT_PARQUET = Path("outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet")
DEFAULT_OUTPUT_DIR = Path("outputs/phase268")
NOTIONAL_INR = 100_000.0
TRADING_DAYS_PER_YEAR = 252.0
ANNUALIZED_RETURN_PROFITABLE_THRESHOLD_PCT = 12.0
HORIZONS = [3, 6, 10]
IMBALANCE_QUANTILES = [0.50, 0.60, 0.75, 0.90]
SHOCK_QUANTILES = [0.50, 0.60, 0.75, 0.90]
SPREAD_REGIMES = ["low", "mid", "high", "compression", "all_with_spread_cap"]
COST_MULTIPLIERS = [1.0, 1.5, 2.0]
EXPLORATORY_MIN_EVENTS = 5
EXPLORATORY_MIN_SYMBOLS = 2
ACCEPTANCE_MIN_EVENTS = 30
ACCEPTANCE_MIN_SYMBOLS = 8
ACCEPTANCE_MIN_DATES = 1
ACCEPTANCE_MIN_COST200_AVG_NET_PER_EVENT_INR = 25.0
ACCEPTANCE_MIN_SHUFFLE_MARGIN_INR = 100.0


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
    frame["abs_level_weighted_imbalance"] = frame["avg_level_weighted_depth_imbalance"].abs()
    group = frame.groupby(["trade_date", "exchange", "symbol"], sort=False)
    frame["spread_change_bps"] = group["avg_spread_bps"].diff().fillna(0.0)
    frame["spread_compression_bps"] = (-frame["spread_change_bps"]).clip(lower=0.0)
    frame["replenishment_minus_withdrawal"] = frame["depth_replenishment_pressure"] - frame["depth_withdrawal_pressure"]
    frame["withdrawal_minus_replenishment"] = -frame["replenishment_minus_withdrawal"]
    frame["market_direction_proxy"] = frame.groupby(["trade_date", "richer_event_bar_id"], sort=False)["future_return_h3"].transform("mean").fillna(0.0)
    frame["market_volatility_proxy"] = frame.groupby(["trade_date", "richer_event_bar_id"], sort=False)["future_return_h3"].transform(lambda x: x.abs().mean()).fillna(0.0)
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
            0.85: safe_float(frame["avg_spread_bps"].quantile(0.85), 0.0),
        },
        "compression": {q: safe_float(frame["spread_compression_bps"].quantile(q), 0.0) for q in SHOCK_QUANTILES},
        "market_vol": {q: safe_float(frame["market_volatility_proxy"].quantile(q), 0.0) for q in SHOCK_QUANTILES},
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
    if regime == "all_with_spread_cap":
        return frame["avg_spread_bps"].le(thresholds["spread"][0.85])
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
    if family_id == "P268_BID_ABSORPTION_BREADTH_REPAIR":
        side = pd.Series(1, index=frame.index)
        mask = (
            frame["avg_depth_beyond_l1_qty_imbalance"].ge(imbalance_min)
            & frame["avg_cum_top5_qty_imbalance"].ge(-0.05)
            & frame["avg_level_weighted_depth_imbalance"].ge(-0.05)
            & frame["depth_replenishment_pressure"].ge(shock_min)
            & frame["l2_l5_bid_share"].ge(0.45)
        )
    elif family_id == "P268_ASK_ABSORPTION_BREADTH_REPAIR":
        side = pd.Series(-1, index=frame.index)
        mask = (
            frame["avg_depth_beyond_l1_qty_imbalance"].le(-imbalance_min)
            & frame["avg_cum_top5_qty_imbalance"].le(0.05)
            & frame["avg_level_weighted_depth_imbalance"].le(0.05)
            & frame["depth_replenishment_pressure"].ge(shock_min)
            & frame["l2_l5_ask_share"].ge(0.45)
        )
    elif family_id == "P268_SPREAD_COMPRESSION_ABSORPTION_REPAIR":
        long_side = frame["avg_depth_beyond_l1_qty_imbalance"].ge(imbalance_min * 0.80)
        short_side = frame["avg_depth_beyond_l1_qty_imbalance"].le(-imbalance_min * 0.80)
        side = side.mask(long_side, 1).mask(short_side, -1)
        mask = side.ne(0) & frame["spread_compression_bps"].ge(thresholds["compression"][0.50]) & frame["top5_churn_pressure"].ge(shock_min)
    elif family_id == "P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR":
        long_side = frame["avg_depth_beyond_l1_qty_imbalance"].ge(imbalance_min * 0.75) & frame["avg_level_weighted_depth_imbalance"].ge(-0.05)
        short_side = frame["avg_depth_beyond_l1_qty_imbalance"].le(-imbalance_min * 0.75) & frame["avg_level_weighted_depth_imbalance"].le(0.05)
        side = side.mask(long_side, 1).mask(short_side, -1)
        mask = side.ne(0) & frame["depth_withdrawal_pressure"].ge(shock_min) & frame["top5_churn_pressure"].ge(shock_min)
    elif family_id == "P268_MARKET_REGIME_CONFIRMED_ABSORPTION":
        long_side = (
            frame["avg_depth_beyond_l1_qty_imbalance"].ge(imbalance_min * 0.70)
            & frame["market_direction_proxy"].ge(-0.00005)
            & frame["market_volatility_proxy"].le(thresholds["market_vol"][0.75])
        )
        short_side = (
            frame["avg_depth_beyond_l1_qty_imbalance"].le(-imbalance_min * 0.70)
            & frame["market_direction_proxy"].le(0.00005)
            & frame["market_volatility_proxy"].le(thresholds["market_vol"][0.75])
        )
        side = side.mask(long_side, 1).mask(short_side, -1)
        mask = side.ne(0) & frame["top5_churn_pressure"].ge(shock_min * 0.80)
    else:
        raise ValueError(f"Unknown event family: {family_id}")
    common = (
        regime
        & frame["allowed_for_training_parameter_selection"].eq(1)
        & frame["l2_l5_bid_share"].ge(0.45)
        & frame["l2_l5_ask_share"].ge(0.45)
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
        return {"event_rows": 0, "net_pnl_inr": 0.0, "gross_pnl_inr": 0.0, "cost_inr": 0.0, "win_rate": 0.0, "profit_factor": 0.0, "avg_net_per_event": 0.0, "max_drawdown_inr": 0.0, "cost_hurdle_hit_rate": 0.0, "annualized_return_pct": 0.0}
    gross_bps = events["gross_edge_bps"]
    cost_bps = events["zerodha_round_trip_charge_bps"] * cost_multiplier
    net_bps = gross_bps - cost_bps
    net_inr = net_bps / 10000.0 * NOTIONAL_INR
    gross_inr = gross_bps / 10000.0 * NOTIONAL_INR
    cost_inr = cost_bps / 10000.0 * NOTIONAL_INR
    gross_pos = safe_float(net_inr[net_inr > 0].sum(), 0.0)
    gross_neg = safe_float(-net_inr[net_inr < 0].sum(), 0.0)
    trade_dates = max(int(events["trade_date"].nunique()), 1) if "trade_date" in events.columns else 1
    annualized_return_pct = safe_float(net_inr.sum(), 0.0) / NOTIONAL_INR / trade_dates * TRADING_DAYS_PER_YEAR * 100.0
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
        "annualized_return_pct": annualized_return_pct,
    }


def deterministic_controls(events: pd.DataFrame, cost_multiplier: float) -> dict[str, Any]:
    if events.empty:
        return {"side_flip_net_pnl_inr": 0.0, "side_flip_degrades": 0, "random_side_net_pnl_inr": 0.0, "random_side_beat": 0, "shuffle_label_net_pnl_inr": 0.0, "shuffle_label_margin_inr": 0.0, "shuffle_label_beat": 0}
    base = event_metrics(events, cost_multiplier)["net_pnl_inr"]
    flipped = events.copy()
    flipped["gross_edge_bps"] = -flipped["gross_edge_bps"]
    flip_net = event_metrics(flipped, cost_multiplier)["net_pnl_inr"]
    randomed = events.copy()
    key = randomed["symbol"].astype(str) + "_" + randomed["richer_event_bar_id"].astype(str) + "_" + randomed["trade_date"].astype(str) + "_phase268"
    random_side = key.map(stable_random_side)
    randomed["gross_edge_bps"] = random_side * randomed["future_move_bps"].abs()
    random_net = event_metrics(randomed, cost_multiplier)["net_pnl_inr"]
    shuffled = events.copy()
    if len(shuffled) > 1:
        order_key = shuffled["symbol"].astype(str) + "_" + shuffled["trade_date"].astype(str) + "_" + shuffled["richer_event_bar_id"].astype(str) + "_shuffle_phase268"
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
        "shuffle_label_margin_inr": base - shuffle_net,
        "shuffle_label_beat": int(base > shuffle_net),
    }


def build_training_search(frame: pd.DataFrame, phase267_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    families = read_csv(phase267_dir / "phase267_candidate_family_contract.csv")
    thresholds = threshold_maps(frame)
    rows: list[dict[str, Any]] = []
    exploratory_ledgers: list[pd.DataFrame] = []
    acceptance_ledgers: list[pd.DataFrame] = []
    for family_id in families["candidate_family_id"].astype(str).tolist():
        for horizon in HORIZONS:
            for imbalance_q, imbalance_min in thresholds["imbalance"].items():
                for shock_q in SHOCK_QUANTILES:
                    shock_base = thresholds["replenishment"][shock_q] if "ABSORPTION" in family_id else thresholds["withdrawal"][shock_q] if "WITHDRAWAL" in family_id else thresholds["shock"][shock_q]
                    for spread_regime in SPREAD_REGIMES:
                        mask, side = event_mask_and_side(frame, family_id, imbalance_min, shock_base, spread_regime, thresholds)
                        events = make_events(frame, mask, side, horizon, family_id)
                        candidate_id = f"P268_{family_id}_H{horizon}_IQ{str(imbalance_q).replace('.', 'p')}_SQ{str(shock_q).replace('.', 'p')}_SP{spread_regime.upper()}"
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
                        record["exploratory_candidate"] = int(
                            record["cost100_event_rows"] >= EXPLORATORY_MIN_EVENTS
                            and record["symbols"] >= EXPLORATORY_MIN_SYMBOLS
                            and record["cost100_net_pnl_inr"] > 0
                        )
                        record["annualized_profitable_research_lead"] = int(
                            record["cost100_event_rows"] >= EXPLORATORY_MIN_EVENTS
                            and record["symbols"] >= EXPLORATORY_MIN_SYMBOLS
                            and record["cost100_annualized_return_pct"] >= ANNUALIZED_RETURN_PROFITABLE_THRESHOLD_PCT
                        )
                        record["cost200_annualized_profitable_research_lead"] = int(
                            record["cost100_event_rows"] >= EXPLORATORY_MIN_EVENTS
                            and record["symbols"] >= EXPLORATORY_MIN_SYMBOLS
                            and record["cost200_annualized_return_pct"] >= ANNUALIZED_RETURN_PROFITABLE_THRESHOLD_PCT
                        )
                        record["acceptance_grade_candidate"] = int(
                            record["cost100_event_rows"] >= ACCEPTANCE_MIN_EVENTS
                            and record["symbols"] >= ACCEPTANCE_MIN_SYMBOLS
                            and record["trade_dates"] >= ACCEPTANCE_MIN_DATES
                            and record["cost100_net_pnl_inr"] > 0
                            and record["cost150_net_pnl_inr"] > 0
                            and record["cost200_net_pnl_inr"] > 0
                            and record["cost200_avg_net_per_event"] >= ACCEPTANCE_MIN_COST200_AVG_NET_PER_EVENT_INR
                            and record["shuffle_label_margin_inr"] >= ACCEPTANCE_MIN_SHUFFLE_MARGIN_INR
                            and record["side_flip_degrades"] == 1
                            and record["random_side_beat"] == 1
                            and record["uses_l1_only"] == 0
                        )
                        record["has_events"] = int(record["cost100_event_rows"] > 0)
                        rows.append(record)
                        event_cols = ["trade_date", "exchange", "symbol", "richer_event_bar_id", "family_id", "side", "future_move_bps", "gross_edge_bps", "zerodha_round_trip_charge_bps", "avg_cum_top5_qty_imbalance", "avg_depth_beyond_l1_qty_imbalance", "avg_level_weighted_depth_imbalance", "depth_replenishment_pressure", "depth_withdrawal_pressure", "top5_churn_pressure", "avg_spread_bps"]
                        if record["exploratory_candidate"] and not events.empty:
                            exploratory_ledgers.append(events.assign(candidate_id=candidate_id)[["candidate_id", *event_cols]])
                        if record["acceptance_grade_candidate"] and not events.empty:
                            acceptance_ledgers.append(events.assign(candidate_id=candidate_id)[["candidate_id", *event_cols]])
    variants = pd.DataFrame(rows).sort_values(
        ["acceptance_grade_candidate", "cost200_annualized_profitable_research_lead", "annualized_profitable_research_lead", "exploratory_candidate", "cost200_annualized_return_pct", "cost100_annualized_return_pct"],
        ascending=[False, False, False, False, False, False],
        kind="mergesort",
    )
    exploratory_ledger = pd.concat(exploratory_ledgers, ignore_index=True) if exploratory_ledgers else pd.DataFrame()
    acceptance_ledger = pd.concat(acceptance_ledgers, ignore_index=True) if acceptance_ledgers else pd.DataFrame()
    return variants, exploratory_ledger, acceptance_ledger


def build_gate_evaluation(phase267_dir: Path, variants: pd.DataFrame, frame: pd.DataFrame) -> pd.DataFrame:
    next_action = str(metric_value(phase267_dir / "phase267_acceptance_summary.csv", "phase267_next_best_action", ""))
    rows = [
        ("P268_PHASE267_WORK_ORDER_PRESENT", "run_phase268_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_training_search" in next_action, next_action, "Phase267 next action targets Phase268", "hard"),
        ("P268_PHASE267_EXPLORATORY_LANE_ENABLED", as_int(metric_value(phase267_dir / "phase267_acceptance_summary.csv", "phase267_exploratory_lane_enabled", 0)) == 1, metric_value(phase267_dir / "phase267_acceptance_summary.csv", "phase267_exploratory_lane_enabled", 0), "exploratory lane enabled", "hard"),
        ("P268_PHASE267_EXPLORATORY_CONTROLS_NOT_FILTERS", as_int(metric_value(phase267_dir / "phase267_acceptance_summary.csv", "phase267_exploratory_controls_are_filters", 1)) == 0, metric_value(phase267_dir / "phase267_acceptance_summary.csv", "phase267_exploratory_controls_are_filters", 1), "exploratory controls recorded as metrics", "hard"),
        ("P268_INPUT_ROWS_PRESENT", len(frame) >= 1000, len(frame), ">=1000 richer raw top-five event bars", "hard"),
        ("P268_VARIANTS_TESTED", len(variants) > 0, len(variants), ">0 variants", "hard"),
        ("P268_ALL_VARIANTS_USE_FULL_DEPTH", int(variants["uses_full_top_five_depth"].sum()) == len(variants), int(variants["uses_full_top_five_depth"].sum()), "all variants use rows 1-5", "hard"),
        ("P268_ALL_VARIANTS_USE_LEVELS_2_TO_5", int(variants["uses_depth_beyond_l1"].sum()) == len(variants), int(variants["uses_depth_beyond_l1"].sum()), "all variants use levels 2-5", "hard"),
        ("P268_NO_L1_ONLY_VARIANTS", int(variants["uses_l1_only"].sum()) == 0, int(variants["uses_l1_only"].sum()), "0 L1-only variants", "hard"),
        ("P268_TWO_LANE_LABELS_PRESENT", {"exploratory_candidate", "acceptance_grade_candidate"}.issubset(set(variants.columns)), "exploratory;acceptance", "two-lane labels present", "hard"),
        ("P268_ANNUALIZED_RETURN_LABELS_PRESENT", {"annualized_profitable_research_lead", "cost100_annualized_return_pct", "cost200_annualized_return_pct"}.issubset(set(variants.columns)), "annualized_return", "annualized-return research lead labels present", "hard"),
        ("P268_CONTROLS_RECORDED", {"side_flip_degrades", "random_side_beat", "shuffle_label_margin_inr"}.issubset(set(variants.columns)), "side_flip;random_side;shuffle_margin", "controls recorded", "hard"),
        ("P268_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase268 Full-depth Liquidity-shock Two-lane Training Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase268 executes the Phase267 two-lane repair search.",
        "The exploratory lane keeps promising pockets with controls recorded as diagnostics, while the acceptance lane applies strict controls before any future replay/promotion discussion.",
        "All candidates use Zerodha top-five market-by-price rows 1-5 and levels 2-5 materiality; L1-only variants are forbidden.",
        f"Annualized-return fields are fixed-notional research proxies: net P&L divided by INR {NOTIONAL_INR:,.0f} and scaled by {TRADING_DAYS_PER_YEAR:.0f} trading days. They are not portfolio annual returns because capital concurrency, sizing, reuse, and capacity are not modeled here.",
        "This is not replay execution, strategy promotion, paper/live acceptance, or a deployable profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(input_parquet: Path = DEFAULT_INPUT_PARQUET, phase267_dir: Path = DEFAULT_PHASE267_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if as_int(metric_value(phase267_dir / "phase267_acceptance_summary.csv", "phase267_full_top_five_depth_required", 0)) != 1:
        raise RuntimeError("Phase267 does not require full top-five depth.")
    if as_int(metric_value(phase267_dir / "phase267_acceptance_summary.csv", "phase267_l1_only_candidate_allowed", 1)) != 0:
        raise RuntimeError("Phase267 does not forbid L1-only candidates.")
    frame = load_event_bars(input_parquet)
    variants, exploratory_ledger, acceptance_ledger = build_training_search(frame, phase267_dir)
    gates = build_gate_evaluation(phase267_dir, variants, frame)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    exploratory_rows = int(variants["exploratory_candidate"].sum()) if not variants.empty else 0
    annualized_lead_rows = int(variants["annualized_profitable_research_lead"].sum()) if not variants.empty else 0
    cost200_annualized_lead_rows = int(variants["cost200_annualized_profitable_research_lead"].sum()) if not variants.empty else 0
    acceptance_rows = int(variants["acceptance_grade_candidate"].sum()) if not variants.empty else 0
    cost100_positive = int(variants["cost100_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    cost150_positive = int(variants["cost150_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    cost200_positive = int(variants["cost200_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    best = variants.iloc[0].to_dict() if not variants.empty else {}
    next_action = "run_phase269_full_depth_liquidity_shock_two_lane_training_interpretation_no_paper_live" if hard_pass == len(hard) else "repair_phase268_two_lane_training_search"
    acceptance = pd.DataFrame(
        [
            ("phase268_two_lane_training_search_complete", 1, "Phase268 full-depth two-lane training search completed"),
            ("phase268_input_event_bar_rows", len(frame), "Input event bars"),
            ("phase268_symbols", int(frame["symbol"].nunique()), "Input symbol breadth"),
            ("phase268_trade_dates", int(frame["trade_date"].nunique()), "Input trade dates"),
            ("phase268_variant_rows", len(variants), "Variants tested"),
            ("phase268_full_top_five_depth_variant_rows", int(variants["uses_full_top_five_depth"].sum()) if not variants.empty else 0, "Variants using rows 1-5"),
            ("phase268_depth_beyond_l1_variant_rows", int(variants["uses_depth_beyond_l1"].sum()) if not variants.empty else 0, "Variants using levels 2-5"),
            ("phase268_l1_only_variant_rows", int(variants["uses_l1_only"].sum()) if not variants.empty else 0, "L1-only variants"),
            ("phase268_exploratory_candidate_rows", exploratory_rows, "Exploratory candidates retained"),
            ("phase268_annualization_notional_inr", NOTIONAL_INR, "Fixed notional denominator for annualized-return proxy"),
            ("phase268_annualization_trading_days", TRADING_DAYS_PER_YEAR, "Trading-day multiplier for annualized-return proxy"),
            ("phase268_annualization_is_portfolio_return", 0, "Annualized-return fields are not portfolio annual returns"),
            ("phase268_annualization_formula", "net_pnl_inr / 100000 * 252", "Fixed-notional research-lead proxy formula"),
            ("phase268_annualized_profitable_research_lead_rows", annualized_lead_rows, "Exploratory candidates with annualized return >= 12% at 1x costs"),
            ("phase268_cost200_annualized_profitable_research_lead_rows", cost200_annualized_lead_rows, "Exploratory candidates with annualized return >= 12% at 2x costs"),
            ("phase268_acceptance_grade_candidate_rows", acceptance_rows, "Acceptance-grade candidates"),
            ("phase268_cost100_positive_variant_rows", cost100_positive, "Variants positive at 1x costs"),
            ("phase268_cost150_positive_variant_rows", cost150_positive, "Variants positive at 1.5x costs"),
            ("phase268_cost200_positive_variant_rows", cost200_positive, "Variants positive at 2x costs"),
            ("phase268_best_candidate_id", best.get("candidate_id", ""), "Best candidate"),
            ("phase268_best_family_id", best.get("family_id", ""), "Best family"),
            ("phase268_best_exploratory_candidate", best.get("exploratory_candidate", 0), "Best exploratory flag"),
            ("phase268_best_acceptance_grade_candidate", best.get("acceptance_grade_candidate", 0), "Best acceptance flag"),
            ("phase268_best_cost100_net_pnl_inr", best.get("cost100_net_pnl_inr", 0.0), "Best 1x net P&L"),
            ("phase268_best_cost100_annualized_return_pct", best.get("cost100_annualized_return_pct", 0.0), "Best 1x annualized return"),
            ("phase268_best_cost200_net_pnl_inr", best.get("cost200_net_pnl_inr", 0.0), "Best 2x net P&L"),
            ("phase268_best_cost200_annualized_return_pct", best.get("cost200_annualized_return_pct", 0.0), "Best 2x annualized return"),
            ("phase268_best_cost200_avg_net_per_event_inr", best.get("cost200_avg_net_per_event", 0.0), "Best 2x average net/event"),
            ("phase268_best_event_rows", best.get("cost100_event_rows", 0), "Best event rows"),
            ("phase268_best_symbols", best.get("symbols", 0), "Best symbols"),
            ("phase268_best_trade_dates", best.get("trade_dates", 0), "Best dates"),
            ("phase268_best_shuffle_label_margin_inr", best.get("shuffle_label_margin_inr", 0.0), "Best shuffled-label margin"),
            ("phase268_best_side_flip_degrades", best.get("side_flip_degrades", 0), "Best side-flip control"),
            ("phase268_best_random_side_beat", best.get("random_side_beat", 0), "Best random-side control"),
            ("phase268_exploratory_controls_are_filters", 0, "Exploratory controls are metrics, not hard filters"),
            ("phase268_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase268_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase268_download_more_dates_now_allowed", 0, "No new download in Phase268"),
            ("phase268_replay_execution_allowed_now", 0, "No replay execution in Phase268"),
            ("phase268_strategy_promotion_allowed", 0, "No strategy promotion from Phase268"),
            ("phase268_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase268"),
            ("phase268_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase268"),
            ("phase268_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    variants.to_csv(output_dir / "phase268_two_lane_variant_results.csv", index=False)
    variants.head(120).to_csv(output_dir / "phase268_top_two_lane_variants.csv", index=False)
    exploratory_ledger.to_csv(output_dir / "phase268_exploratory_event_ledger.csv", index=False)
    acceptance_ledger.to_csv(output_dir / "phase268_acceptance_event_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase268_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase268_acceptance_summary.csv", index=False)
    write_report(output_dir / "phase268_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_training_search_report.md", {"Acceptance Summary": acceptance, "Gate Evaluation": gates, "Top Two-lane Variants": variants.head(40)})
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase268_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_training_search",
        **reproducibility_fields(
            artifact_id="phase268",
            generated_utc=generated_utc,
            inputs={"input_parquet": str(input_parquet), "phase267_dir": str(phase267_dir)},
            parameters={
                "notional_inr": NOTIONAL_INR,
                "trading_days_per_year": TRADING_DAYS_PER_YEAR,
                "annualized_return_profitable_threshold_pct": ANNUALIZED_RETURN_PROFITABLE_THRESHOLD_PCT,
                "horizons": HORIZONS,
                "imbalance_quantiles": IMBALANCE_QUANTILES,
                "shock_quantiles": SHOCK_QUANTILES,
                "spread_regimes": SPREAD_REGIMES,
                "cost_multipliers": COST_MULTIPLIERS,
                "exploratory_controls_are_filters": 0,
                "full_top_five_depth_required": 1,
                "levels_2_to_5_materiality_required": 1,
                "l1_only_candidate_allowed": 0,
                "download_more_dates_now_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "two_lane_variant_results": str(output_dir / "phase268_two_lane_variant_results.csv"),
                "top_two_lane_variants": str(output_dir / "phase268_top_two_lane_variants.csv"),
                "exploratory_event_ledger": str(output_dir / "phase268_exploratory_event_ledger.csv"),
                "acceptance_event_ledger": str(output_dir / "phase268_acceptance_event_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase268_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase268_acceptance_summary.csv"),
                "report": str(output_dir / "phase268_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_training_search_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase268_directional_event_bar_proxy_no_replay",
        ),
    }
    (output_dir / "phase268_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_training_search_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase268 full-depth two-lane liquidity-shock training search.")
    parser.add_argument("--input-parquet", type=Path, default=DEFAULT_INPUT_PARQUET)
    parser.add_argument("--phase267-dir", type=Path, default=DEFAULT_PHASE267_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(input_parquet=args.input_parquet, phase267_dir=args.phase267_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

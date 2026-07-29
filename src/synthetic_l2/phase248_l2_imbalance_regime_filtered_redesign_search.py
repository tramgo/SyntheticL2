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
DEFAULT_PHASE247_DIR = Path("outputs/phase247")
DEFAULT_OUTPUT_DIR = Path("outputs/phase248")
FORBIDDEN_TUNING_DATES = {"2026-07-17", "2026-07-20"}
HORIZONS = [6, 8, 10, 12]
EVENT_QUANTILES = [0.95, 0.975, 0.99]
BAR_RETURN_QUANTILES = [0.85, 0.90, 0.95]
TOP5_ABS_QUANTILES = [0.50, 0.65, 0.80]
SPREAD_QUANTILES = [0.75, 0.90]
INTENSITY_QUANTILES = [0.25, 0.50]
RANGE_VOL_QUANTILES = [0.75]
FAMILIES = [
    "P247_REVERSAL_L2_CONFIRMATION",
    "P247_REVERSAL_L2_DIVERGENCE",
    "P247_RANGE_ONLY_REVERSAL",
    "P247_COMBINED_STRICT_REVERSAL",
]
RANDOM_CONTROL_RUNS = 1000
RANDOM_SEED = 248
RANDOM_BEAT_THRESHOLD = 0.95
MIN_CONTROL_TRADES = 8
MIN_CONTROL_DATES = 4
MIN_CONTROL_SYMBOLS = 6


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
    event_q: float,
    bar_q: float,
    top5_q: float,
    spread_q: float,
    intensity_q: float,
    range_q: float,
) -> str:
    fam = family.replace("P247_", "P248_")
    parts = [
        fam,
        f"H{horizon}",
        f"EQ{str(event_q).replace('.', '_')}",
        f"BQ{str(bar_q).replace('.', '_')}",
        f"TQ{str(top5_q).replace('.', '_')}",
        f"SP{str(spread_q).replace('.', '_')}",
        f"IQ{str(intensity_q).replace('.', '_')}",
        f"RQ{str(range_q).replace('.', '_')}",
    ]
    return "_".join(parts)


def load_training_bars(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    bars = pd.read_parquet(path).sort_values(["trade_date", "symbol", "source_event_bar_id"], kind="mergesort")
    bars["trade_date"] = bars["trade_date"].astype(str)
    bars = bars[~bars["trade_date"].isin(FORBIDDEN_TUNING_DATES)].copy()
    required = {
        "trade_date",
        "exchange",
        "symbol",
        "source_event_bar_id",
        "close_mid_price",
        "event_window_score",
        "bar_return",
        "avg_top5_market_by_price_imbalance",
        "avg_l1_imbalance",
        "avg_spread",
        "avg_event_intensity_proxy",
        "abs_bar_return_bps",
        "taker_round_trip_cost_floor_bps",
    }
    missing = sorted(required.difference(bars.columns))
    if missing:
        raise ValueError(f"Training bars missing required Phase248 columns: {missing}")
    bars = bars.reset_index(drop=True)
    bars["prior_range_vol_bps"] = (
        bars.groupby(["trade_date", "symbol"], sort=False)["abs_bar_return_bps"]
        .transform(lambda s: s.shift(1).rolling(20, min_periods=5).median())
        .astype(float)
    )
    fallback = float(bars["abs_bar_return_bps"].median()) if len(bars) else 0.0
    bars["prior_range_vol_bps"] = bars["prior_range_vol_bps"].fillna(fallback)
    market = (
        bars.loc[bars["symbol"].astype(str).eq("NIFTYBEES"), ["trade_date", "source_event_bar_id", "bar_return"]]
        .rename(columns={"bar_return": "market_direction_proxy"})
        .drop_duplicates(["trade_date", "source_event_bar_id"])
    )
    bars = bars.merge(market, on=["trade_date", "source_event_bar_id"], how="left")
    bars["market_direction_proxy"] = bars["market_direction_proxy"].fillna(0.0).astype(float)
    for horizon in HORIZONS:
        bars[f"future_return_h{horizon}"] = (
            bars.groupby(["trade_date", "symbol"], sort=False)["close_mid_price"].shift(-horizon)
            / bars["close_mid_price"]
            - 1.0
        )
    return bars


def replay_variant(
    base: pd.DataFrame,
    family: str,
    horizon: int,
    event_q: float,
    bar_q: float,
    top5_q: float,
    spread_q: float,
    intensity_q: float,
    range_q: float,
) -> tuple[dict[str, Any], pd.DataFrame]:
    future_col = f"future_return_h{horizon}"
    valid = base[base[future_col].notna()]
    if valid.empty:
        return {}, pd.DataFrame()
    thresholds = {
        "event_window_score_threshold": float(valid["event_window_score"].quantile(event_q)),
        "bar_abs_threshold": float(valid["bar_return"].abs().quantile(bar_q)),
        "top5_abs_threshold": float(valid["avg_top5_market_by_price_imbalance"].abs().quantile(top5_q)),
        "spread_max": float(valid["avg_spread"].quantile(spread_q)),
        "event_intensity_min": float(valid["avg_event_intensity_proxy"].quantile(intensity_q)),
        "range_vol_max": float(valid["prior_range_vol_bps"].quantile(range_q)),
        "market_abs_max": float(valid["market_direction_proxy"].abs().quantile(0.75)),
    }
    selected = valid.loc[
        valid["event_window_score"].ge(thresholds["event_window_score_threshold"])
        & valid["bar_return"].abs().ge(thresholds["bar_abs_threshold"])
        & valid["avg_top5_market_by_price_imbalance"].abs().ge(thresholds["top5_abs_threshold"])
        & valid["avg_spread"].le(thresholds["spread_max"])
        & valid["avg_event_intensity_proxy"].ge(thresholds["event_intensity_min"])
    ].copy()
    if selected.empty:
        return {}, pd.DataFrame()
    bar_sign = np.sign(selected["bar_return"].astype(float))
    top5_sign = np.sign(selected["avg_top5_market_by_price_imbalance"].astype(float))
    side = -bar_sign
    if family in {"P247_REVERSAL_L2_CONFIRMATION", "P247_COMBINED_STRICT_REVERSAL"}:
        selected = selected.loc[top5_sign.eq(side)].copy()
    if family in {"P247_REVERSAL_L2_DIVERGENCE", "P247_COMBINED_STRICT_REVERSAL"}:
        selected = selected.loc[top5_sign.ne(0) & bar_sign.ne(0) & top5_sign.ne(bar_sign)].copy()
    if family in {"P247_RANGE_ONLY_REVERSAL", "P247_COMBINED_STRICT_REVERSAL"}:
        selected = selected.loc[
            selected["prior_range_vol_bps"].le(thresholds["range_vol_max"])
            & selected["market_direction_proxy"].abs().le(thresholds["market_abs_max"])
        ].copy()
    if selected.empty:
        return {}, pd.DataFrame()
    selected["side"] = -np.sign(selected["bar_return"].astype(float))
    selected = selected[selected["side"].ne(0)].copy()
    if selected.empty:
        return {}, pd.DataFrame()
    cid = candidate_id(family, horizon, event_q, bar_q, top5_q, spread_q, intensity_q, range_q)
    selected["candidate_id"] = cid
    selected["family_id"] = family
    selected["horizon_event_bars"] = horizon
    selected["event_quantile"] = event_q
    selected["bar_return_quantile"] = bar_q
    selected["top5_abs_quantile"] = top5_q
    selected["spread_quantile"] = spread_q
    selected["intensity_quantile"] = intensity_q
    selected["range_vol_quantile"] = range_q
    for key, value in thresholds.items():
        selected[key] = value
    selected["gross_return"] = selected["side"] * selected[future_col].astype(float)
    selected["cost_return"] = selected["taker_round_trip_cost_floor_bps"].astype(float) / 10000.0
    selected["gross_pnl_inr"] = selected["gross_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["cost_pnl_drag_inr"] = selected["cost_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["net_pnl_inr"] = selected["gross_pnl_inr"] - selected["cost_pnl_drag_inr"]
    gross = float(selected["gross_pnl_inr"].sum())
    cost = float(selected["cost_pnl_drag_inr"].sum())
    net = gross - cost
    cost150 = gross - 1.5 * cost
    cost200 = gross - 2.0 * cost
    date_net = selected.groupby("trade_date", sort=True)["net_pnl_inr"].sum()
    symbol_net = selected.groupby("symbol", sort=True)["net_pnl_inr"].sum()
    denom = abs(net) if abs(net) > 0 else np.nan
    summary = {
        "candidate_id": cid,
        "family_id": family,
        "horizon_event_bars": horizon,
        "event_quantile": event_q,
        "bar_return_quantile": bar_q,
        "top5_abs_quantile": top5_q,
        "spread_quantile": spread_q,
        "intensity_quantile": intensity_q,
        "range_vol_quantile": range_q,
        **thresholds,
        "training_trades": int(len(selected)),
        "training_net_pnl_inr": net,
        "training_gross_pnl_inr": gross,
        "training_cost_pnl_drag_inr": cost,
        "cost150_net_pnl_inr": cost150,
        "cost200_net_pnl_inr": cost200,
        "training_dates": int(selected["trade_date"].nunique()),
        "training_symbols": int(selected["symbol"].nunique()),
        "training_positive_dates": int((date_net > 0).sum()),
        "training_min_date_net_pnl_inr": float(date_net.min()),
        "training_max_date_contribution_abs": float(date_net.abs().max() / denom) if denom and not np.isnan(denom) else np.nan,
        "training_max_symbol_contribution_abs": float(symbol_net.abs().max() / denom) if denom and not np.isnan(denom) else np.nan,
        "training_precision_cost_clear": float((selected["net_pnl_inr"] > 0).mean()),
        "cost_stress_pass": bool(cost150 > 0 and cost200 > 0),
        "top5_filter_active": 1,
        "spread_liquidity_guard_active": 1,
        "range_or_market_veto_active": int(family in {"P247_RANGE_ONLY_REVERSAL", "P247_COMBINED_STRICT_REVERSAL"}),
    }
    keep = [
        "candidate_id",
        "family_id",
        "trade_date",
        "exchange",
        "symbol",
        "source_event_bar_id",
        "horizon_event_bars",
        "side",
        "bar_return",
        "avg_top5_market_by_price_imbalance",
        "avg_l1_imbalance",
        "avg_spread",
        "avg_event_intensity_proxy",
        "prior_range_vol_bps",
        "market_direction_proxy",
        "event_window_score",
        "close_mid_price",
        future_col,
        "gross_pnl_inr",
        "cost_pnl_drag_inr",
        "net_pnl_inr",
    ]
    return summary, selected[keep]


def scan_variants(bars: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    rows: list[dict[str, Any]] = []
    ledgers: dict[str, pd.DataFrame] = {}
    for family in FAMILIES:
        for horizon in HORIZONS:
            for event_q in EVENT_QUANTILES:
                for bar_q in BAR_RETURN_QUANTILES:
                    for top5_q in TOP5_ABS_QUANTILES:
                        for spread_q in SPREAD_QUANTILES:
                            for intensity_q in INTENSITY_QUANTILES:
                                for range_q in RANGE_VOL_QUANTILES:
                                    summary, ledger = replay_variant(bars, family, horizon, event_q, bar_q, top5_q, spread_q, intensity_q, range_q)
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
        & candidates["top5_filter_active"].eq(1)
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
        future_abs = np.abs(gross + cost)
        random_nets = np.asarray(
            [float((rng.choice([-1.0, 1.0], size=len(ledger)) * future_abs - cost).sum()) for _ in range(RANDOM_CONTROL_RUNS)]
        )
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
    controlled["phase248_candidate_survived"] = (
        controlled["control_pass_rows"].ge(4)
        & controlled["training_dates"].ge(MIN_CONTROL_DATES)
        & controlled["training_symbols"].ge(MIN_CONTROL_SYMBOLS)
        & controlled["training_trades"].ge(MIN_CONTROL_TRADES)
        & controlled["top5_filter_active"].eq(1)
        & controlled["spread_liquidity_guard_active"].eq(1)
    )
    controlled = controlled.sort_values(["phase248_candidate_survived", "random_beat_fraction", "cost200_net_pnl_inr_y"], ascending=[False, False, False])
    return controls, controlled.reset_index(drop=True)


def build_gate_evaluation(candidates: pd.DataFrame, controlled: pd.DataFrame, phase247_dir: Path) -> pd.DataFrame:
    next_action = str(metric_value(phase247_dir / "phase247_acceptance_summary.csv", "phase247_next_best_action", ""))
    survivors = int(controlled["phase248_candidate_survived"].astype(bool).sum()) if not controlled.empty else 0
    cost200_positive = int(candidates["cost200_net_pnl_inr"].gt(0).sum()) if not candidates.empty else 0
    l2_filtered = int(candidates["top5_filter_active"].eq(1).sum()) if not candidates.empty else 0
    rows = [
        ("P248_PHASE247_WORK_ORDER_PRESENT", "run_phase248" in next_action, next_action, "Phase247 next action targets Phase248", "hard"),
        ("P248_FORBIDDEN_HOLDOUT_DATES_EXCLUDED", True, ";".join(sorted(FORBIDDEN_TUNING_DATES)), "2026-07-17 and 2026-07-20 excluded", "hard"),
        ("P248_L2_FILTER_ACTIVE_IN_ALL_VARIANTS", l2_filtered == len(candidates) and len(candidates) > 0, f"{l2_filtered}/{len(candidates)}", "all variants", "hard"),
        ("P248_VARIANTS_EVALUATED", len(candidates) >= 800, len(candidates), ">=800 combined-filter variants", "hard"),
        ("P248_COST200_POSITIVE_VARIANTS_FOUND", cost200_positive > 0, cost200_positive, ">0 positive at 2x cost", "hard"),
        ("P248_CONTROLLED_SURVIVOR_FOUND", survivors > 0, survivors, ">0 controlled survivors", "diagnostic"),
        ("P248_NO_DOWNLOAD_HOLDOUT_TUNING_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase248 L2 Imbalance / Regime-filtered Redesign Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase248 is a training-only search for the Phase247 redesign families.",
        "It excludes the 2026-07-17 and 2026-07-20 holdout/fresh diagnostic dates from tuning, requires top-five market-by-price imbalance in every variant, and keeps downloads/paper/live/profitability claims closed.",
        "",
    ]
    for title, table in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(table), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(bars_path: Path = DEFAULT_BARS_PATH, phase247_dir: Path = DEFAULT_PHASE247_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    bars = load_training_bars(bars_path)
    candidates, ledgers = scan_variants(bars)
    controls, controlled = build_controls(candidates, ledgers)
    survivors = controlled[controlled["phase248_candidate_survived"].astype(bool)].copy() if not controlled.empty else pd.DataFrame()
    best = survivors.iloc[0].to_dict() if not survivors.empty else (controlled.iloc[0].to_dict() if not controlled.empty else (candidates.iloc[0].to_dict() if not candidates.empty else {}))
    best_id = str(best.get("candidate_id", ""))
    gates = build_gate_evaluation(candidates, controlled, phase247_dir)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = (
        "precommit_phase249_future_holdout_for_l2_imbalance_regime_filtered_candidate_no_2026_07_17_or_2026_07_20_tuning_no_paper_live"
        if not survivors.empty
        else "close_or_broaden_phase248_l2_imbalance_regime_filtered_search_no_downloads_no_paper_live"
    )
    acceptance = pd.DataFrame(
        [
            ("phase248_l2_imbalance_regime_filtered_search_complete", 1, "Phase248 training-only redesign search completed"),
            ("phase248_training_event_bar_rows", len(bars), "Training event bars used"),
            ("phase248_training_dates", bars["trade_date"].nunique(), "Training dates used"),
            ("phase248_training_symbols", bars["symbol"].nunique(), "Training symbols used"),
            ("phase248_forbidden_tuning_dates", ";".join(sorted(FORBIDDEN_TUNING_DATES)), "Dates excluded from tuning"),
            ("phase248_variant_rows", len(candidates), "Combined-filter variants evaluated"),
            ("phase248_l2_filtered_variant_rows", int(candidates["top5_filter_active"].eq(1).sum()) if not candidates.empty else 0, "Variants with required top-five imbalance filter active"),
            ("phase248_net_positive_variant_rows", int(candidates["training_net_pnl_inr"].gt(0).sum()) if not candidates.empty else 0, "Net-positive variants at base cost"),
            ("phase248_cost150_positive_variant_rows", int(candidates["cost150_net_pnl_inr"].gt(0).sum()) if not candidates.empty else 0, "Positive variants at 1.5x cost"),
            ("phase248_cost200_positive_variant_rows", int(candidates["cost200_net_pnl_inr"].gt(0).sum()) if not candidates.empty else 0, "Positive variants at 2.0x cost"),
            ("phase248_controlled_candidate_rows", len(controlled), "Candidates evaluated with side-flip/random-side controls"),
            ("phase248_survivor_candidate_rows", len(survivors), "Candidates passing controls and breadth gates"),
            ("phase248_best_candidate_id", best_id, "Best Phase248 survivor/candidate"),
            ("phase248_best_family_id", best.get("family_id", ""), "Best candidate family"),
            ("phase248_best_training_net_pnl_inr", as_float(best.get("training_net_pnl_inr", 0.0)), "Best training net P&L"),
            ("phase248_best_cost200_net_pnl_inr", as_float(best.get("cost200_net_pnl_inr_y", best.get("cost200_net_pnl_inr", 0.0))), "Best 2x-cost net P&L"),
            ("phase248_best_random_beat_fraction", as_float(best.get("random_beat_fraction", 0.0)), "Best random-side beat fraction"),
            ("phase248_best_trade_rows", as_int(best.get("training_trades", 0)), "Best trade rows"),
            ("phase248_best_dates", as_int(best.get("training_dates", 0)), "Best dates represented"),
            ("phase248_best_symbols", as_int(best.get("training_symbols", 0)), "Best symbols represented"),
            ("phase248_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase248_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase248_future_holdout_precommit_allowed", int(not survivors.empty), "Future holdout precommit allowed only if survivors exist"),
            ("phase248_download_more_dates_now_allowed", 0, "No raw-date download in Phase248"),
            ("phase248_holdout_parameter_tuning_allowed", 0, "No holdout-date tuning"),
            ("phase248_strategy_promotion_allowed", 0, "No strategy promotion from Phase248"),
            ("phase248_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase248"),
            ("phase248_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase248"),
            ("phase248_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    candidates.to_csv(output_dir / "phase248_candidate_summary.csv", index=False)
    controls.to_csv(output_dir / "phase248_control_summary.csv", index=False)
    controlled.to_csv(output_dir / "phase248_controlled_candidate_summary.csv", index=False)
    survivors.to_csv(output_dir / "phase248_survivor_candidates.csv", index=False)
    ledgers.get(best_id, pd.DataFrame()).to_csv(output_dir / "phase248_best_candidate_trade_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase248_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase248_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase248_l2_imbalance_regime_filtered_redesign_search_report.md",
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
        "scope": "phase248_l2_imbalance_regime_filtered_redesign_search",
        **reproducibility_fields(
            artifact_id="phase248",
            generated_utc=generated_utc,
            inputs={"bars_path": str(bars_path), "phase247_dir": str(phase247_dir)},
            parameters={
                "horizons": HORIZONS,
                "families": FAMILIES,
                "event_quantiles": EVENT_QUANTILES,
                "bar_return_quantiles": BAR_RETURN_QUANTILES,
                "top5_abs_quantiles": TOP5_ABS_QUANTILES,
                "spread_quantiles": SPREAD_QUANTILES,
                "intensity_quantiles": INTENSITY_QUANTILES,
                "range_vol_quantiles": RANGE_VOL_QUANTILES,
                "forbidden_tuning_dates": sorted(FORBIDDEN_TUNING_DATES),
                "random_control_runs": RANDOM_CONTROL_RUNS,
                "random_seed": RANDOM_SEED,
                "download_more_dates_now_allowed": 0,
                "holdout_parameter_tuning_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "candidate_summary": str(output_dir / "phase248_candidate_summary.csv"),
                "control_summary": str(output_dir / "phase248_control_summary.csv"),
                "controlled_candidate_summary": str(output_dir / "phase248_controlled_candidate_summary.csv"),
                "survivor_candidates": str(output_dir / "phase248_survivor_candidates.csv"),
                "best_candidate_trade_ledger": str(output_dir / "phase248_best_candidate_trade_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase248_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase248_acceptance_summary.csv"),
                "report": str(output_dir / "phase248_l2_imbalance_regime_filtered_redesign_search_report.md"),
            },
            random_seed=RANDOM_SEED,
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase248_training_only_real_event_bar_adapter_no_holdout_tuning",
        ),
    }
    (output_dir / "phase248_l2_imbalance_regime_filtered_redesign_search_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase248 L2 imbalance / regime-filtered training-only redesign search.")
    parser.add_argument("--bars-path", type=Path, default=DEFAULT_BARS_PATH)
    parser.add_argument("--phase247-dir", type=Path, default=DEFAULT_PHASE247_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(bars_path=args.bars_path, phase247_dir=args.phase247_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

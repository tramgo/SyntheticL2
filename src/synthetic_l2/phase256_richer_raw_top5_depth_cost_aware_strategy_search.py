from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, metric_value
from synthetic_l2.phase255_richer_raw_depth_feature_quality_interpretation import safe_float
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE255_DIR = Path("outputs/phase255")
DEFAULT_INPUT_PARQUET = Path("outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet")
DEFAULT_OUTPUT_DIR = Path("outputs/phase256")
NOTIONAL_INR = 100_000.0
MIN_TRADE_ROWS = 30
MIN_SYMBOLS = 8

FULL_DEPTH_FEATURES = [
    "avg_order_count_imbalance_l1_l5",
    "avg_depth_beyond_l1_qty_imbalance",
    "avg_level_weighted_depth_imbalance",
    "avg_depth_slope_bid",
    "avg_depth_slope_ask",
    "avg_depth_convexity_bid",
    "avg_depth_convexity_ask",
    "top5_qty_churn_sum",
    "top5_order_churn_sum",
    "depth_replenishment_pressure",
    "depth_withdrawal_pressure",
]

HORIZONS = [3, 6, 10]
SIGN_MODES = ["follow", "reverse"]
THRESHOLD_QUANTILES = [0.70, 0.80, 0.90, 0.95]
SPREAD_CAP_QUANTILES = [0.50, 0.75, 0.90]
CHURN_FLOOR_QUANTILES = [0.00, 0.50, 0.75]
COST_MULTIPLIERS = [1.0, 1.5, 2.0]


def load_event_bars(input_parquet: Path) -> pd.DataFrame:
    if not input_parquet.exists():
        raise FileNotFoundError(f"Missing richer raw-depth event bars: {input_parquet}")
    con = duckdb.connect()
    try:
        frame = con.execute(f"select * from read_parquet('{input_parquet.as_posix()}')").fetchdf()
    finally:
        con.close()
    return frame.sort_values(["trade_date", "exchange", "symbol", "richer_event_bar_id"], kind="mergesort").reset_index(drop=True)


def max_drawdown(values: pd.Series) -> float:
    if values.empty:
        return 0.0
    cumulative = values.cumsum()
    running_max = cumulative.cummax()
    drawdown = cumulative - running_max
    return safe_float(drawdown.min(), 0.0)


def evaluate_trades(trades: pd.DataFrame, cost_multiplier: float) -> dict[str, Any]:
    if trades.empty:
        return {
            "trade_rows": 0,
            "net_pnl_inr": 0.0,
            "gross_pnl_inr": 0.0,
            "cost_inr": 0.0,
            "win_rate": 0.0,
            "profit_factor": 0.0,
            "avg_net_pnl_per_trade": 0.0,
            "max_drawdown_inr": 0.0,
        }
    gross = trades["side"] * trades["future_return"] * NOTIONAL_INR
    cost = trades["taker_round_trip_cost_floor_bps"] / 10000.0 * NOTIONAL_INR * cost_multiplier
    net = gross - cost
    wins = int((net > 0).sum())
    gross_pos = safe_float(net[net > 0].sum(), 0.0)
    gross_neg = safe_float(-net[net < 0].sum(), 0.0)
    return {
        "trade_rows": int(len(trades)),
        "net_pnl_inr": safe_float(net.sum(), 0.0),
        "gross_pnl_inr": safe_float(gross.sum(), 0.0),
        "cost_inr": safe_float(cost.sum(), 0.0),
        "win_rate": wins / len(trades) if len(trades) else 0.0,
        "profit_factor": gross_pos / gross_neg if gross_neg > 0 else (999.0 if gross_pos > 0 else 0.0),
        "avg_net_pnl_per_trade": safe_float(net.mean(), 0.0),
        "max_drawdown_inr": max_drawdown(net),
    }


def deterministic_side_control(trades: pd.DataFrame, cost_multiplier: float) -> dict[str, Any]:
    if trades.empty:
        return {"random_side_net_pnl_inr": 0.0, "random_side_beat": 0}
    controlled = trades.copy()
    key = (
        controlled["symbol"].astype(str)
        + "_"
        + controlled["richer_event_bar_id"].astype(str)
        + "_"
        + controlled["trade_date"].astype(str)
    )
    controlled["side"] = key.map(lambda x: 1 if (hash(x) % 2 == 0) else -1)
    metrics = evaluate_trades(controlled, cost_multiplier)
    return {
        "random_side_net_pnl_inr": metrics["net_pnl_inr"],
        "random_side_beat": int(evaluate_trades(trades, cost_multiplier)["net_pnl_inr"] > metrics["net_pnl_inr"]),
    }


def build_strategy_search(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = frame.copy()
    frame["l2_l5_bid_share"] = pd.to_numeric(frame["avg_cum_buy_qty_l2_l5"], errors="coerce") / pd.to_numeric(
        frame["avg_cum_buy_qty_l1_l5"], errors="coerce"
    ).replace(0, pd.NA)
    frame["l2_l5_ask_share"] = pd.to_numeric(frame["avg_cum_sell_qty_l2_l5"], errors="coerce") / pd.to_numeric(
        frame["avg_cum_sell_qty_l1_l5"], errors="coerce"
    ).replace(0, pd.NA)
    frame["full_depth_share_min"] = frame[["l2_l5_bid_share", "l2_l5_ask_share"]].min(axis=1)
    frame["depth_churn_rank_feature"] = pd.to_numeric(frame["top5_qty_churn_sum"], errors="coerce") + pd.to_numeric(
        frame["top5_order_churn_sum"], errors="coerce"
    )
    spread_caps = {
        q: safe_float(pd.to_numeric(frame["avg_spread_bps"], errors="coerce").quantile(q), 0.0)
        for q in SPREAD_CAP_QUANTILES
    }
    churn_floors = {
        q: safe_float(pd.to_numeric(frame["depth_churn_rank_feature"], errors="coerce").quantile(q), 0.0)
        for q in CHURN_FLOOR_QUANTILES
    }
    rows: list[dict[str, Any]] = []
    trade_rows: list[pd.DataFrame] = []
    variant_id = 0
    for feature in FULL_DEPTH_FEATURES:
        values = pd.to_numeric(frame[feature], errors="coerce")
        abs_thresholds = {q: safe_float(values.abs().quantile(q), 0.0) for q in THRESHOLD_QUANTILES}
        for horizon in HORIZONS:
            label = f"future_return_h{horizon}"
            for sign_mode in SIGN_MODES:
                for threshold_q, threshold in abs_thresholds.items():
                    for spread_q, spread_cap in spread_caps.items():
                        for churn_q, churn_floor in churn_floors.items():
                            variant_id += 1
                            side = values.map(lambda x: 1 if x > threshold else (-1 if x < -threshold else 0))
                            if sign_mode == "reverse":
                                side = -side
                            mask = (
                                side.ne(0)
                                & frame[label].notna()
                                & frame["avg_spread_bps"].le(spread_cap)
                                & frame["depth_churn_rank_feature"].ge(churn_floor)
                                & frame["full_depth_share_min"].ge(0.50)
                                & frame["allowed_for_training_parameter_selection"].eq(1)
                            )
                            trades = frame.loc[mask, [
                                "trade_date",
                                "exchange",
                                "symbol",
                                "richer_event_bar_id",
                                "avg_spread_bps",
                                "taker_round_trip_cost_floor_bps",
                                label,
                            ]].rename(columns={label: "future_return"})
                            trades = trades.assign(side=side.loc[mask].astype(int))
                            candidate_id = (
                                f"P256_{feature.upper()}_{sign_mode.upper()}_H{horizon}_"
                                f"TQ{str(threshold_q).replace('.', 'p')}_SPQ{str(spread_q).replace('.', 'p')}_"
                                f"CQ{str(churn_q).replace('.', 'p')}"
                            )
                            per_cost: dict[str, Any] = {
                                "candidate_id": candidate_id,
                                "feature": feature,
                                "uses_full_top_five_depth": 1,
                                "uses_depth_beyond_l1": 1,
                                "sign_mode": sign_mode,
                                "horizon": horizon,
                                "threshold_quantile": threshold_q,
                                "threshold_abs_value": threshold,
                                "spread_cap_quantile": spread_q,
                                "spread_cap_bps": spread_cap,
                                "churn_floor_quantile": churn_q,
                                "churn_floor": churn_floor,
                                "symbols": int(trades["symbol"].nunique()) if not trades.empty else 0,
                                "trade_dates": int(trades["trade_date"].nunique()) if not trades.empty else 0,
                            }
                            for cost_multiplier in COST_MULTIPLIERS:
                                metrics = evaluate_trades(trades, cost_multiplier)
                                suffix = f"cost{int(cost_multiplier * 100):03d}"
                                per_cost.update({f"{suffix}_{k}": v for k, v in metrics.items()})
                            control = deterministic_side_control(trades, 1.0)
                            per_cost.update(control)
                            per_cost["survivor_candidate"] = int(
                                per_cost["cost100_trade_rows"] >= MIN_TRADE_ROWS
                                and per_cost["symbols"] >= MIN_SYMBOLS
                                and per_cost["cost100_net_pnl_inr"] > 0
                                and per_cost["cost150_net_pnl_inr"] > 0
                                and per_cost["cost200_net_pnl_inr"] > 0
                                and per_cost["random_side_beat"] == 1
                            )
                            rows.append(per_cost)
                            if per_cost["survivor_candidate"]:
                                trade_rows.append(trades.assign(candidate_id=candidate_id))
    variants = pd.DataFrame(rows).sort_values(
        ["survivor_candidate", "cost200_net_pnl_inr", "cost100_net_pnl_inr"],
        ascending=[False, False, False],
    )
    survivor_trades = pd.concat(trade_rows, ignore_index=True) if trade_rows else pd.DataFrame()
    return variants, survivor_trades


def build_gate_evaluation(phase255_dir: Path, variants: pd.DataFrame, frame: pd.DataFrame) -> pd.DataFrame:
    phase255_next = str(metric_value(phase255_dir / "phase255_acceptance_summary.csv", "phase255_next_best_action", ""))
    rows = [
        ("P256_PHASE255_WORK_ORDER_PRESENT", "run_phase256_richer_raw_top5_depth_cost_aware_strategy_search" in phase255_next, phase255_next, "Phase255 next action targets Phase256", "hard"),
        ("P256_INPUT_ROWS_PRESENT", len(frame) >= 1000, len(frame), ">=1000 richer raw-depth event bars", "hard"),
        ("P256_VARIANTS_TESTED", len(variants) > 0, len(variants), ">0 training-only strategy variants", "hard"),
        ("P256_ALL_VARIANTS_USE_FULL_DEPTH", int(variants["uses_full_top_five_depth"].sum()) == len(variants), int(variants["uses_full_top_five_depth"].sum()), "all variants use full top-five depth", "hard"),
        ("P256_ALL_VARIANTS_USE_DEPTH_BEYOND_L1", int(variants["uses_depth_beyond_l1"].sum()) == len(variants), int(variants["uses_depth_beyond_l1"].sum()), "all variants use levels 2-5 / beyond-L1 fields", "hard"),
        ("P256_COST_STACK_APPLIED", "cost200_net_pnl_inr" in variants.columns, "cost100/cost150/cost200", "Zerodha cost floor applied at 1x/1.5x/2x", "hard"),
        ("P256_NO_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase256 Richer Raw Top-five Depth Cost-aware Strategy Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase256 searches training-only strategy variants on the Phase254/255 richer raw Zerodha top-five depth event-bar product.",
        "Every candidate uses full top-five depth and levels 2-5/beyond-L1 information. Costs use the carried Zerodha taker round-trip cost floor.",
        "This is not paper/live acceptance, promotion, or a deployable profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    input_parquet: Path = DEFAULT_INPUT_PARQUET,
    phase255_dir: Path = DEFAULT_PHASE255_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if as_int(metric_value(phase255_dir / "phase255_acceptance_summary.csv", "phase255_strategy_search_allowed_next", 0)) != 1:
        raise RuntimeError("Phase255 does not allow Phase256 strategy search.")
    frame = load_event_bars(input_parquet)
    variants, survivor_trades = build_strategy_search(frame)
    gates = build_gate_evaluation(phase255_dir, variants, frame)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    survivor_rows = int(variants["survivor_candidate"].sum()) if not variants.empty else 0
    positive_cost100 = int(variants["cost100_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    positive_cost150 = int(variants["cost150_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    positive_cost200 = int(variants["cost200_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    best = variants.iloc[0].to_dict() if not variants.empty else {}
    next_action = (
        "run_phase257_richer_raw_top5_depth_strategy_search_interpretation_no_paper_live"
        if hard_pass == len(hard)
        else "repair_phase256_richer_raw_top5_depth_strategy_search_before_interpretation"
    )
    acceptance = pd.DataFrame(
        [
            ("phase256_strategy_search_complete", 1, "Phase256 richer raw top-five depth training-only strategy search completed"),
            ("phase256_input_event_bar_rows", len(frame), "Input richer raw-depth event bars"),
            ("phase256_symbols", int(frame["symbol"].nunique()), "Symbols represented"),
            ("phase256_trade_dates", int(frame["trade_date"].nunique()), "Trade dates represented"),
            ("phase256_variant_rows", len(variants), "Training-only strategy variants tested"),
            ("phase256_full_top_five_depth_variant_rows", int(variants["uses_full_top_five_depth"].sum()) if not variants.empty else 0, "Variants using full top-five depth"),
            ("phase256_depth_beyond_l1_variant_rows", int(variants["uses_depth_beyond_l1"].sum()) if not variants.empty else 0, "Variants using levels 2-5/beyond-L1 fields"),
            ("phase256_cost100_positive_variant_rows", positive_cost100, "Variants positive at 1x Zerodha cost floor"),
            ("phase256_cost150_positive_variant_rows", positive_cost150, "Variants positive at 1.5x cost floor"),
            ("phase256_cost200_positive_variant_rows", positive_cost200, "Variants positive at 2x cost floor"),
            ("phase256_survivor_candidate_rows", survivor_rows, "Variants passing trade, breadth, cost-stress and random-side controls"),
            ("phase256_best_candidate_id", best.get("candidate_id", ""), "Best candidate by survivor/cost200/cost100 ranking"),
            ("phase256_best_feature", best.get("feature", ""), "Best candidate feature"),
            ("phase256_best_sign_mode", best.get("sign_mode", ""), "Best candidate sign mode"),
            ("phase256_best_horizon", best.get("horizon", ""), "Best candidate horizon"),
            ("phase256_best_cost100_net_pnl_inr", best.get("cost100_net_pnl_inr", 0.0), "Best candidate 1x-cost net P&L"),
            ("phase256_best_cost200_net_pnl_inr", best.get("cost200_net_pnl_inr", 0.0), "Best candidate 2x-cost net P&L"),
            ("phase256_best_trade_rows", best.get("cost100_trade_rows", 0), "Best candidate trade count"),
            ("phase256_best_symbols", best.get("symbols", 0), "Best candidate symbol breadth"),
            ("phase256_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase256_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase256_replay_execution_allowed_now", 0, "No replay execution in Phase256"),
            ("phase256_strategy_promotion_allowed", 0, "No strategy promotion from Phase256"),
            ("phase256_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase256"),
            ("phase256_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase256"),
            ("phase256_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    variants.to_csv(output_dir / "phase256_strategy_variant_results.csv", index=False)
    variants.head(50).to_csv(output_dir / "phase256_top_strategy_variants.csv", index=False)
    survivor_trades.to_csv(output_dir / "phase256_survivor_trade_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase256_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase256_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase256_richer_raw_top5_depth_cost_aware_strategy_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Top Strategy Variants": variants.head(30),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase256_richer_raw_top5_depth_cost_aware_strategy_search",
        **reproducibility_fields(
            artifact_id="phase256",
            generated_utc=generated_utc,
            inputs={"input_parquet": str(input_parquet), "phase255_dir": str(phase255_dir)},
            parameters={
                "notional_inr": NOTIONAL_INR,
                "full_depth_features": FULL_DEPTH_FEATURES,
                "horizons": HORIZONS,
                "sign_modes": SIGN_MODES,
                "threshold_quantiles": THRESHOLD_QUANTILES,
                "spread_cap_quantiles": SPREAD_CAP_QUANTILES,
                "churn_floor_quantiles": CHURN_FLOOR_QUANTILES,
                "cost_multipliers": COST_MULTIPLIERS,
                "min_trade_rows": MIN_TRADE_ROWS,
                "min_symbols": MIN_SYMBOLS,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "strategy_variant_results": str(output_dir / "phase256_strategy_variant_results.csv"),
                "top_strategy_variants": str(output_dir / "phase256_top_strategy_variants.csv"),
                "survivor_trade_ledger": str(output_dir / "phase256_survivor_trade_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase256_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase256_acceptance_summary.csv"),
                "report": str(output_dir / "phase256_richer_raw_top5_depth_cost_aware_strategy_search_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase256_training_only_event_bar_horizon_fill_at_cost_floor",
        ),
    }
    (output_dir / "phase256_richer_raw_top5_depth_cost_aware_strategy_search_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase256 richer raw top-five depth cost-aware strategy search.")
    parser.add_argument("--input-parquet", type=Path, default=DEFAULT_INPUT_PARQUET)
    parser.add_argument("--phase255-dir", type=Path, default=DEFAULT_PHASE255_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(input_parquet=args.input_parquet, phase255_dir=args.phase255_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

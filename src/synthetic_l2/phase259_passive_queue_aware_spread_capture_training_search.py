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
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, metric_value
from synthetic_l2.phase255_richer_raw_depth_feature_quality_interpretation import safe_float
from synthetic_l2.phase256_richer_raw_top5_depth_cost_aware_strategy_search import max_drawdown
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_PHASE258_DIR = Path("outputs/phase258")
DEFAULT_INPUT_PARQUET = Path("outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet")
DEFAULT_OUTPUT_DIR = Path("outputs/phase259")
NOTIONAL_INR = 100_000.0
HORIZONS = [3, 6, 10]
SPREAD_CAPTURE_FRACTIONS = [0.25, 0.50, 0.75]
SPREAD_MIN_QUANTILES = [0.50, 0.75]
QUEUE_MAX_QUANTILES = [0.50, 0.75, 0.90]
CHURN_MAX_QUANTILES = [0.50, 0.75, 0.90]
IMBALANCE_THRESHOLDS = [0.05, 0.15, 0.25]
REPLENISHMENT_QUANTILES = [0.50, 0.75]
COST_MULTIPLIERS = [1.0, 1.5, 2.0]
MIN_OPPORTUNITY_ROWS = 30
MIN_SYMBOLS = 8


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
    for column in [
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
    ]:
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
    return frame


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
    cost_bps = opportunities["zerodha_round_trip_charge_bps"] * cost_multiplier
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


def make_opportunities(
    frame: pd.DataFrame,
    mask: pd.Series,
    side: pd.Series,
    horizon: int,
    spread_capture_fraction: float,
    queue_haircut: float,
    adverse_haircut: float,
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
    fill_probability = (0.65 - 0.35 * queue_rank - 0.20 * churn_rank + 0.25 * l2_share).clip(0.02, 0.85)
    spread_capture_bps = selected["avg_spread_bps"].clip(lower=0.0) * spread_capture_fraction
    future_move_bps = selected["side"] * pd.to_numeric(selected[label], errors="coerce") * 10000.0
    adverse_penalty_bps = (
        selected["withdrawal_pressure_norm"].clip(0, 1) * adverse_haircut * selected["avg_spread_bps"].clip(lower=0.0)
        + selected["cancel_replace_pressure_bps"].fillna(0.0).clip(lower=0.0) * queue_haircut
    )
    selected["fill_probability"] = fill_probability
    selected["spread_capture_bps"] = spread_capture_bps
    selected["future_move_bps"] = future_move_bps
    selected["adverse_penalty_bps"] = adverse_penalty_bps
    selected["expected_gross_bps"] = fill_probability * (spread_capture_bps + future_move_bps - adverse_penalty_bps)
    selected["family_id"] = family_id
    return selected


def deterministic_controls(opportunities: pd.DataFrame, cost_multiplier: float) -> dict[str, Any]:
    if opportunities.empty:
        return {
            "side_flip_expected_net_pnl_inr": 0.0,
            "side_flip_degrades": 0,
            "random_side_expected_net_pnl_inr": 0.0,
            "random_side_beat": 0,
            "queue_adverse_expected_net_pnl_inr": 0.0,
            "queue_adversity_survives": 0,
        }
    base = passive_metrics(opportunities, cost_multiplier)["expected_net_pnl_inr"]
    flipped = opportunities.copy()
    flipped["expected_gross_bps"] = flipped["fill_probability"] * (
        flipped["spread_capture_bps"] - flipped["future_move_bps"] - flipped["adverse_penalty_bps"]
    )
    flip_net = passive_metrics(flipped, cost_multiplier)["expected_net_pnl_inr"]
    randomed = opportunities.copy()
    key = (
        randomed["symbol"].astype(str)
        + "_"
        + randomed["richer_event_bar_id"].astype(str)
        + "_"
        + randomed["trade_date"].astype(str)
        + "_passive"
    )
    random_side = key.map(stable_random_side)
    randomed["expected_gross_bps"] = randomed["fill_probability"] * (
        randomed["spread_capture_bps"] + random_side * randomed["future_move_bps"].abs() - randomed["adverse_penalty_bps"]
    )
    random_net = passive_metrics(randomed, cost_multiplier)["expected_net_pnl_inr"]
    adverse = opportunities.copy()
    adverse["expected_gross_bps"] = adverse["expected_gross_bps"] - adverse["fill_probability"] * adverse["avg_spread_bps"].clip(lower=0.0) * 0.50
    adverse_net = passive_metrics(adverse, cost_multiplier)["expected_net_pnl_inr"]
    return {
        "side_flip_expected_net_pnl_inr": flip_net,
        "side_flip_degrades": int(base > flip_net),
        "random_side_expected_net_pnl_inr": random_net,
        "random_side_beat": int(base > random_net),
        "queue_adverse_expected_net_pnl_inr": adverse_net,
        "queue_adversity_survives": int(adverse_net > 0),
    }


def build_training_search(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    spread_thresholds = {q: safe_float(frame["avg_spread_bps"].quantile(q), 0.0) for q in SPREAD_MIN_QUANTILES}
    bid_queue_caps = {q: safe_float(frame["bid_queue_pressure"].quantile(q), 0.0) for q in QUEUE_MAX_QUANTILES}
    ask_queue_caps = {q: safe_float(frame["ask_queue_pressure"].quantile(q), 0.0) for q in QUEUE_MAX_QUANTILES}
    churn_caps = {q: safe_float(frame["churn_pressure"].quantile(q), 0.0) for q in CHURN_MAX_QUANTILES}
    repl_thresholds = {q: safe_float(frame["depth_replenishment_pressure"].quantile(q), 0.0) for q in REPLENISHMENT_QUANTILES}
    rows: list[dict[str, Any]] = []
    survivor_ledgers: list[pd.DataFrame] = []
    variant_index = 0
    family_specs = [
        ("P258_PASSIVE_BID_REPLENISHMENT", "bid"),
        ("P258_PASSIVE_ASK_REPLENISHMENT", "ask"),
        ("P258_TWO_SIDED_HIGH_SPREAD_LOW_CHURN", "both"),
        ("P258_IMBALANCE_SKEWED_MAKER", "skew"),
    ]
    for family_id, mode in family_specs:
        for horizon in HORIZONS:
            for spread_q, spread_min in spread_thresholds.items():
                for queue_q in QUEUE_MAX_QUANTILES:
                    for churn_q, churn_cap in churn_caps.items():
                        for imbalance_threshold in IMBALANCE_THRESHOLDS:
                            for repl_q, repl_min in repl_thresholds.items():
                                for capture_fraction in SPREAD_CAPTURE_FRACTIONS:
                                    variant_index += 1
                                    bid_signal = (
                                        frame["avg_depth_beyond_l1_qty_imbalance"].ge(imbalance_threshold)
                                        & frame["avg_cum_top5_qty_imbalance"].ge(0)
                                        & frame["avg_order_count_imbalance_l1_l5"].ge(-0.25)
                                    )
                                    ask_signal = (
                                        frame["avg_depth_beyond_l1_qty_imbalance"].le(-imbalance_threshold)
                                        & frame["avg_cum_top5_qty_imbalance"].le(0)
                                        & frame["avg_order_count_imbalance_l1_l5"].le(0.25)
                                    )
                                    if mode == "bid":
                                        side = pd.Series(1, index=frame.index)
                                        mask = bid_signal & frame["bid_queue_pressure"].le(bid_queue_caps[queue_q])
                                    elif mode == "ask":
                                        side = pd.Series(-1, index=frame.index)
                                        mask = ask_signal & frame["ask_queue_pressure"].le(ask_queue_caps[queue_q])
                                    elif mode == "both":
                                        side = pd.Series(0, index=frame.index)
                                        side = side.mask(bid_signal, 1).mask(ask_signal, -1)
                                        mask = side.ne(0) & frame["bid_queue_pressure"].le(bid_queue_caps[queue_q]) & frame["ask_queue_pressure"].le(ask_queue_caps[queue_q])
                                    else:
                                        side = pd.Series(0, index=frame.index)
                                        side = side.mask(frame["avg_depth_beyond_l1_qty_imbalance"].ge(imbalance_threshold), 1)
                                        side = side.mask(frame["avg_depth_beyond_l1_qty_imbalance"].le(-imbalance_threshold), -1)
                                        mask = side.ne(0)
                                    mask = (
                                        mask
                                        & frame["avg_spread_bps"].ge(spread_min)
                                        & frame["churn_pressure"].le(churn_cap)
                                        & frame["depth_replenishment_pressure"].ge(repl_min)
                                        & frame["l2_l5_bid_share"].ge(0.50)
                                        & frame["l2_l5_ask_share"].ge(0.50)
                                        & frame["allowed_for_training_parameter_selection"].eq(1)
                                    )
                                    opportunities = make_opportunities(
                                        frame=frame,
                                        mask=mask,
                                        side=side,
                                        horizon=horizon,
                                        spread_capture_fraction=capture_fraction,
                                        queue_haircut=0.25,
                                        adverse_haircut=0.50,
                                        family_id=family_id,
                                    )
                                    candidate_id = (
                                        f"P259_{family_id}_H{horizon}_SPQ{str(spread_q).replace('.', 'p')}_"
                                        f"QQ{str(queue_q).replace('.', 'p')}_CQ{str(churn_q).replace('.', 'p')}_"
                                        f"I{str(imbalance_threshold).replace('.', 'p')}_RQ{str(repl_q).replace('.', 'p')}_"
                                        f"CF{str(capture_fraction).replace('.', 'p')}"
                                    )
                                    record: dict[str, Any] = {
                                        "candidate_id": candidate_id,
                                        "family_id": family_id,
                                        "quote_mode": mode,
                                        "uses_full_top_five_depth": 1,
                                        "uses_depth_beyond_l1": 1,
                                        "horizon": horizon,
                                        "spread_quantile": spread_q,
                                        "spread_min_bps": spread_min,
                                        "queue_quantile": queue_q,
                                        "churn_quantile": churn_q,
                                        "churn_cap": churn_cap,
                                        "imbalance_threshold": imbalance_threshold,
                                        "replenishment_quantile": repl_q,
                                        "replenishment_min": repl_min,
                                        "spread_capture_fraction": capture_fraction,
                                        "symbols": int(opportunities["symbol"].nunique()) if not opportunities.empty else 0,
                                        "trade_dates": int(opportunities["trade_date"].nunique()) if not opportunities.empty else 0,
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
                                        and record["cost100_expected_net_pnl_inr"] > 0
                                        and record["cost150_expected_net_pnl_inr"] > 0
                                        and record["cost200_expected_net_pnl_inr"] > 0
                                        and record["side_flip_degrades"] == 1
                                        and record["random_side_beat"] == 1
                                        and record["queue_adversity_survives"] == 1
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
                                                    "side",
                                                    "fill_probability",
                                                    "spread_capture_bps",
                                                    "future_move_bps",
                                                    "adverse_penalty_bps",
                                                    "expected_gross_bps",
                                                    "zerodha_round_trip_charge_bps",
                                                ]
                                            ]
                                        )
    variants = pd.DataFrame(rows).sort_values(
        ["survivor_candidate", "has_opportunities", "cost200_expected_net_pnl_inr", "cost100_expected_net_pnl_inr"],
        ascending=[False, False, False, False],
    )
    survivor_ledger = pd.concat(survivor_ledgers, ignore_index=True) if survivor_ledgers else pd.DataFrame()
    return variants, survivor_ledger


def build_gate_evaluation(phase258_dir: Path, variants: pd.DataFrame, frame: pd.DataFrame) -> pd.DataFrame:
    next_action = str(metric_value(phase258_dir / "phase258_acceptance_summary.csv", "phase258_next_best_action", ""))
    rows = [
        ("P259_PHASE258_WORK_ORDER_PRESENT", "run_phase259_passive_queue_aware_spread_capture_training_search" in next_action, next_action, "Phase258 next action targets Phase259", "hard"),
        ("P259_INPUT_ROWS_PRESENT", len(frame) >= 1000, len(frame), ">=1000 richer raw-depth event bars", "hard"),
        ("P259_VARIANTS_TESTED", len(variants) > 0, len(variants), ">0 passive variants", "hard"),
        ("P259_ALL_VARIANTS_USE_FULL_DEPTH", int(variants["uses_full_top_five_depth"].sum()) == len(variants), int(variants["uses_full_top_five_depth"].sum()), "all variants use full top-five depth", "hard"),
        ("P259_ALL_VARIANTS_USE_DEPTH_BEYOND_L1", int(variants["uses_depth_beyond_l1"].sum()) == len(variants), int(variants["uses_depth_beyond_l1"].sum()), "all variants use levels 2-5/beyond-L1", "hard"),
        ("P259_PASSIVE_CONTROLS_APPLIED", {"side_flip_degrades", "random_side_beat", "queue_adversity_survives"}.issubset(set(variants.columns)), "side_flip;random_side;queue_adversity", "passive controls present", "hard"),
        ("P259_NO_REPLAY_PROMOTION_OR_PAPER_LIVE", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase259 Passive Queue-aware Spread-capture Training Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase259 executes a training-only passive/queue-aware spread-capture search on the Phase254 richer raw top-five depth event bars.",
        "Every candidate uses full Zerodha top-five market-by-price depth and levels 2-5/beyond-L1 features.",
        "Expected passive P&L is fill-probability weighted and includes spread capture, future mid move, adverse-selection/queue penalties and modeled Zerodha charges.",
        "This is not paper/live acceptance, promotion, or a deployable profitability claim.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    input_parquet: Path = DEFAULT_INPUT_PARQUET,
    phase258_dir: Path = DEFAULT_PHASE258_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if as_int(metric_value(phase258_dir / "phase258_acceptance_summary.csv", "phase258_full_top_five_depth_required", 0)) != 1:
        raise RuntimeError("Phase258 does not require full top-five depth.")
    frame = load_event_bars(input_parquet)
    variants, survivor_ledger = build_training_search(frame)
    gates = build_gate_evaluation(phase258_dir, variants, frame)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    survivor_rows = int(variants["survivor_candidate"].sum()) if not variants.empty else 0
    positive_cost100 = int(variants["cost100_expected_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    positive_cost150 = int(variants["cost150_expected_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    positive_cost200 = int(variants["cost200_expected_net_pnl_inr"].gt(0).sum()) if not variants.empty else 0
    best = variants.iloc[0].to_dict() if not variants.empty else {}
    next_action = (
        "run_phase260_passive_queue_aware_spread_capture_interpretation_no_paper_live"
        if hard_pass == len(hard)
        else "repair_phase259_passive_queue_training_search_before_interpretation"
    )
    acceptance = pd.DataFrame(
        [
            ("phase259_passive_training_search_complete", 1, "Phase259 passive queue-aware training search completed"),
            ("phase259_input_event_bar_rows", len(frame), "Input event bars"),
            ("phase259_symbols", int(frame["symbol"].nunique()), "Input symbol breadth"),
            ("phase259_trade_dates", int(frame["trade_date"].nunique()), "Input trade dates"),
            ("phase259_variant_rows", len(variants), "Passive variants tested"),
            ("phase259_full_top_five_depth_variant_rows", int(variants["uses_full_top_five_depth"].sum()) if not variants.empty else 0, "Variants using full top-five depth"),
            ("phase259_depth_beyond_l1_variant_rows", int(variants["uses_depth_beyond_l1"].sum()) if not variants.empty else 0, "Variants using levels 2-5/beyond-L1"),
            ("phase259_cost100_positive_variant_rows", positive_cost100, "Variants positive at 1x Zerodha charge stack"),
            ("phase259_cost150_positive_variant_rows", positive_cost150, "Variants positive at 1.5x charges"),
            ("phase259_cost200_positive_variant_rows", positive_cost200, "Variants positive at 2x charges"),
            ("phase259_survivor_candidate_rows", survivor_rows, "Variants passing breadth, cost stress and controls"),
            ("phase259_best_candidate_id", best.get("candidate_id", ""), "Best candidate by survivor/cost200/cost100 ranking"),
            ("phase259_best_family_id", best.get("family_id", ""), "Best candidate family"),
            ("phase259_best_cost100_expected_net_pnl_inr", best.get("cost100_expected_net_pnl_inr", 0.0), "Best 1x-charge expected net P&L"),
            ("phase259_best_cost200_expected_net_pnl_inr", best.get("cost200_expected_net_pnl_inr", 0.0), "Best 2x-charge expected net P&L"),
            ("phase259_best_opportunity_rows", best.get("cost100_opportunity_rows", 0), "Best opportunity rows"),
            ("phase259_best_symbols", best.get("symbols", 0), "Best symbol breadth"),
            ("phase259_best_realized_fill_equivalent_rows", best.get("cost100_realized_fill_equivalent_rows", 0.0), "Best fill-equivalent rows"),
            ("phase259_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase259_hard_gate_rows", len(hard), "Hard gates evaluated"),
            ("phase259_replay_execution_allowed_now", 0, "No replay execution in Phase259"),
            ("phase259_strategy_promotion_allowed", 0, "No strategy promotion from Phase259"),
            ("phase259_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase259"),
            ("phase259_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase259"),
            ("phase259_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    variants.to_csv(output_dir / "phase259_passive_strategy_variant_results.csv", index=False)
    variants.head(50).to_csv(output_dir / "phase259_top_passive_strategy_variants.csv", index=False)
    survivor_ledger.to_csv(output_dir / "phase259_survivor_opportunity_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase259_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase259_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase259_passive_queue_aware_spread_capture_training_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Gate Evaluation": gates,
            "Top Passive Strategy Variants": variants.head(30),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase259_passive_queue_aware_spread_capture_training_search",
        **reproducibility_fields(
            artifact_id="phase259",
            generated_utc=generated_utc,
            inputs={"input_parquet": str(input_parquet), "phase258_dir": str(phase258_dir)},
            parameters={
                "notional_inr": NOTIONAL_INR,
                "horizons": HORIZONS,
                "spread_capture_fractions": SPREAD_CAPTURE_FRACTIONS,
                "spread_min_quantiles": SPREAD_MIN_QUANTILES,
                "queue_max_quantiles": QUEUE_MAX_QUANTILES,
                "churn_max_quantiles": CHURN_MAX_QUANTILES,
                "imbalance_thresholds": IMBALANCE_THRESHOLDS,
                "replenishment_quantiles": REPLENISHMENT_QUANTILES,
                "cost_multipliers": COST_MULTIPLIERS,
                "full_top_five_depth_required": 1,
                "l1_only_candidate_allowed": 0,
                "replay_execution_allowed_now": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "passive_strategy_variant_results": str(output_dir / "phase259_passive_strategy_variant_results.csv"),
                "top_passive_strategy_variants": str(output_dir / "phase259_top_passive_strategy_variants.csv"),
                "survivor_opportunity_ledger": str(output_dir / "phase259_survivor_opportunity_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase259_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase259_acceptance_summary.csv"),
                "report": str(output_dir / "phase259_passive_queue_aware_spread_capture_training_search_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase259_passive_queue_expected_fill_event_bar_proxy",
        ),
    }
    (output_dir / "phase259_passive_queue_aware_spread_capture_training_search_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase259 passive queue-aware spread-capture training search.")
    parser.add_argument("--input-parquet", type=Path, default=DEFAULT_INPUT_PARQUET)
    parser.add_argument("--phase258-dir", type=Path, default=DEFAULT_PHASE258_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(input_parquet=args.input_parquet, phase258_dir=args.phase258_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

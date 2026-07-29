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
DEFAULT_PHASE242_DIR = Path("outputs/phase242")
DEFAULT_OUTPUT_DIR = Path("outputs/phase243")
FORBIDDEN_HOLDOUT_DATES = {"2026-07-17"}
HORIZONS = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20]
EVENT_QUANTILES = [0.90, 0.925, 0.95, 0.975, 0.985, 0.99, 0.995]
SIGNAL_QUANTILES = [0.90, 0.925, 0.95, 0.975, 0.985, 0.99, 0.995]
SIGNAL_SOURCES = ["avg_microprice_dev", "avg_l1_imbalance", "avg_top5_market_by_price_imbalance", "bar_return"]
DIRECTIONS = ["reversal", "continuation"]
RANDOM_CONTROL_RUNS = 1000
RANDOM_SEED = 243
RANDOM_BEAT_THRESHOLD = 0.95


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


def candidate_id(signal_source: str, direction: str, horizon: int, event_quantile: float, signal_quantile: float) -> str:
    source = (
        signal_source.replace("avg_top5_market_by_price_imbalance", "TOP5_IMBALANCE")
        .replace("avg_l1_imbalance", "L1_IMBALANCE")
        .replace("avg_microprice_dev", "MICROPRICE")
        .replace("bar_return", "BAR_RETURN")
        .upper()
    )
    return f"P243_{source}_{direction.upper()}_H{horizon}_EQ{str(event_quantile).replace('.', '_')}_SQ{str(signal_quantile).replace('.', '_')}"


def load_training_bars(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    bars = pd.read_parquet(path).sort_values(["trade_date", "symbol", "source_event_bar_id"], kind="mergesort")
    bars = bars[~bars["trade_date"].astype(str).isin(FORBIDDEN_HOLDOUT_DATES)].copy()
    required = {
        "trade_date",
        "exchange",
        "symbol",
        "source_event_bar_id",
        "close_mid_price",
        "event_window_score",
        "avg_microprice_dev",
        "avg_l1_imbalance",
        "avg_top5_market_by_price_imbalance",
        "bar_return",
        "taker_round_trip_cost_floor_bps",
    }
    missing = sorted(required.difference(bars.columns))
    if missing:
        raise ValueError(f"Training bars missing required columns: {missing}")
    return bars.reset_index(drop=True)


def replay_variant(base: pd.DataFrame, signal_source: str, direction: str, horizon: int, event_quantile: float, signal_quantile: float) -> tuple[dict[str, Any], pd.DataFrame]:
    frame = base.copy()
    future_col = f"future_return_h{horizon}"
    frame[future_col] = (
        frame.groupby(["trade_date", "symbol"], sort=False)["close_mid_price"].shift(-horizon)
        / frame["close_mid_price"]
        - 1.0
    )
    event_threshold = float(frame["event_window_score"].quantile(event_quantile))
    event_base = frame[frame["event_window_score"].ge(event_threshold) & frame[future_col].notna()].copy()
    if event_base.empty:
        return {}, pd.DataFrame()
    signal_threshold = float(event_base[signal_source].abs().quantile(signal_quantile))
    selected = event_base[event_base[signal_source].abs().ge(signal_threshold)].copy()
    side = np.sign(selected[signal_source].astype(float))
    if direction == "reversal":
        side = -side
    selected["side"] = side
    selected = selected[selected["side"].ne(0)].copy()
    cid = candidate_id(signal_source, direction, horizon, event_quantile, signal_quantile)
    if selected.empty:
        return {}, pd.DataFrame()
    selected["candidate_id"] = cid
    selected["family_id"] = f"{signal_source}_{direction}"
    selected["horizon_event_bars"] = horizon
    selected["event_quantile"] = event_quantile
    selected["signal_quantile"] = signal_quantile
    selected["event_window_score_threshold"] = event_threshold
    selected["signal_abs_threshold"] = signal_threshold
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
        "family_id": f"{signal_source}_{direction}",
        "signal_source": signal_source,
        "direction": direction,
        "horizon_event_bars": horizon,
        "event_quantile": event_quantile,
        "signal_quantile": signal_quantile,
        "event_window_score_threshold": event_threshold,
        "signal_abs_threshold": signal_threshold,
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
    }
    keep = [
        "candidate_id",
        "family_id",
        "trade_date",
        "exchange",
        "symbol",
        "source_event_bar_id",
        "horizon_event_bars",
        "event_quantile",
        "signal_quantile",
        "side",
        "event_window_score",
        signal_source,
        "close_mid_price",
        future_col,
        "gross_pnl_inr",
        "cost_pnl_drag_inr",
        "net_pnl_inr",
    ]
    return summary, selected[keep]


def scan_variants(bars: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    rows: list[dict[str, Any]] = []
    survivor_ledgers: dict[str, pd.DataFrame] = {}
    for horizon in HORIZONS:
        for event_quantile in EVENT_QUANTILES:
            for signal_source in SIGNAL_SOURCES:
                for signal_quantile in SIGNAL_QUANTILES:
                    for direction in DIRECTIONS:
                        summary, ledger = replay_variant(bars, signal_source, direction, horizon, event_quantile, signal_quantile)
                        if not summary:
                            continue
                        rows.append(summary)
                        if summary["cost_stress_pass"] and summary["training_trades"] >= 10:
                            survivor_ledgers[summary["candidate_id"]] = ledger
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame, survivor_ledgers
    frame = frame.sort_values(["cost200_net_pnl_inr", "cost150_net_pnl_inr", "training_net_pnl_inr"], ascending=[False, False, False]).reset_index(drop=True)
    return frame, survivor_ledgers


def build_controls(candidates: pd.DataFrame, ledgers: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    rng = np.random.default_rng(RANDOM_SEED)
    candidate_pool = candidates[
        candidates["cost_stress_pass"].astype(bool)
        & candidates["training_trades"].ge(10)
        & candidates["training_dates"].ge(4)
        & candidates["training_symbols"].ge(8)
    ].head(200)
    for candidate in candidate_pool.to_dict("records"):
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
    merged = candidates.merge(controls, on="candidate_id", how="inner")
    merged["phase243_candidate_survived"] = (
        merged["control_pass_rows"].ge(4)
        & merged["training_dates"].ge(4)
        & merged["training_symbols"].ge(8)
        & merged["training_trades"].ge(10)
    )
    merged = merged.sort_values(["phase243_candidate_survived", "random_beat_fraction", "cost200_net_pnl_inr_y"], ascending=[False, False, False])
    return controls, merged.reset_index(drop=True)


def build_gate_evaluation(candidates: pd.DataFrame, controlled: pd.DataFrame, phase242_dir: Path) -> pd.DataFrame:
    phase242_next = str(metric_value(phase242_dir / "phase242_acceptance_summary.csv", "phase242_next_best_action", ""))
    survivor_rows = int(controlled["phase243_candidate_survived"].astype(bool).sum()) if not controlled.empty else 0
    rows = [
        ("P243_PHASE242_WORK_ORDER_PRESENT", "phase243_cost_stress_first" in phase242_next or "run_phase243" in phase242_next, phase242_next, "Phase242 next action targets Phase243", "hard"),
        ("P243_VARIANTS_EVALUATED", len(candidates) >= 3000, len(candidates), ">=3000 redesigned variants", "hard"),
        ("P243_COST200_SURVIVORS_FOUND", int(candidates["cost200_net_pnl_inr"].gt(0).sum()) > 0 if not candidates.empty else False, int(candidates["cost200_net_pnl_inr"].gt(0).sum()) if not candidates.empty else 0, ">0 variants positive at 2x costs", "hard"),
        ("P243_RANDOM_SIDE_CONTROLLED_SURVIVOR_FOUND", survivor_rows > 0, survivor_rows, ">0 variants pass side flip, random side, 1.5x and 2.0x cost", "hard"),
        ("P243_HOLDOUT_DATE_NOT_USED_FOR_TUNING", True, ";".join(sorted(FORBIDDEN_HOLDOUT_DATES)), "2026-07-17 excluded", "hard"),
        ("P243_NO_DOWNLOAD_OR_PAPER_LIVE_OR_PROFIT_CLAIM", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase243 Cost-stress-first Redesign Search",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase243 runs the redesign queue opened by Phase242 without using the 2026-07-17 holdout for tuning and without downloading more real dates.",
        "It searches stricter, lower-turnover variants and requires 1.5x/2.0x cost survival before random-side control evaluation.",
        "Survivors are research candidates for a future holdout only; no paper/live acceptance or deployable profitability claim is opened.",
        "",
    ]
    for title, frame in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(bars_path: Path = DEFAULT_BARS_PATH, phase242_dir: Path = DEFAULT_PHASE242_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    bars = load_training_bars(bars_path)
    candidates, ledgers = scan_variants(bars)
    controls, controlled = build_controls(candidates, ledgers)
    survivors = controlled[controlled["phase243_candidate_survived"].astype(bool)].copy() if not controlled.empty else pd.DataFrame()
    best = survivors.iloc[0].to_dict() if not survivors.empty else (controlled.iloc[0].to_dict() if not controlled.empty else {})
    best_id = str(best.get("candidate_id", ""))
    best_ledger = ledgers.get(best_id, pd.DataFrame())
    gates = build_gate_evaluation(candidates, controlled, phase242_dir)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    next_action = (
        "precommit_future_holdout_for_phase243_candidate_after_storage_decision_no_2026_07_17_tuning_no_paper_live"
        if not survivors.empty
        else "broaden_redesign_or_close_cost_stress_first_track_no_paper_live"
    )
    acceptance = pd.DataFrame(
        [
            ("phase243_cost_stress_first_redesign_complete", 1, "Phase243 redesign search completed"),
            ("phase243_training_event_bar_rows", int(len(bars)), "Training/discovery event bars used"),
            ("phase243_forbidden_holdout_dates", ";".join(sorted(FORBIDDEN_HOLDOUT_DATES)), "Dates excluded from tuning"),
            ("phase243_expanded_variant_rows", int(len(candidates)), "Redesigned variants evaluated"),
            ("phase243_net_positive_variant_rows", int(candidates["training_net_pnl_inr"].gt(0).sum()) if not candidates.empty else 0, "Net-positive variants after base costs"),
            ("phase243_cost150_positive_variant_rows", int(candidates["cost150_net_pnl_inr"].gt(0).sum()) if not candidates.empty else 0, "Positive under 1.5x costs"),
            ("phase243_cost200_positive_variant_rows", int(candidates["cost200_net_pnl_inr"].gt(0).sum()) if not candidates.empty else 0, "Positive under 2.0x costs"),
            ("phase243_controlled_candidate_rows", int(len(controlled)), "Cost-stress survivors with full controls evaluated"),
            ("phase243_survivor_candidate_rows", int(len(survivors)), "Candidates passing side flip, random side and cost stress controls"),
            ("phase243_best_candidate_id", best_id, "Best Phase243 survivor/candidate"),
            ("phase243_best_training_net_pnl_inr", as_float(best.get("training_net_pnl_inr", 0.0)), "Best training/discovery net P&L"),
            ("phase243_best_cost200_net_pnl_inr", as_float(best.get("cost200_net_pnl_inr_y", best.get("cost200_net_pnl_inr", 0.0))), "Best 2x-cost net P&L"),
            ("phase243_best_random_beat_fraction", as_float(best.get("random_beat_fraction", 0.0)), "Best random-side beat fraction"),
            ("phase243_best_trade_rows", as_int(best.get("training_trades", 0)), "Best selected trades"),
            ("phase243_best_dates", as_int(best.get("training_dates", 0)), "Best dates represented"),
            ("phase243_best_symbols", as_int(best.get("training_symbols", 0)), "Best symbols represented"),
            ("phase243_hard_gate_pass_rows", hard_pass, "Hard gates passed"),
            ("phase243_hard_gate_rows", int(len(hard)), "Hard gates evaluated"),
            ("phase243_future_holdout_precommit_allowed", int(not survivors.empty), "A future holdout precommit may be opened, but no current holdout acceptance"),
            ("phase243_download_more_dates_now_allowed", 0, "No additional raw-date download in Phase243"),
            ("phase243_holdout_parameter_tuning_allowed", 0, "No 2026-07-17 tuning"),
            ("phase243_strategy_promotion_allowed", 0, "No strategy promotion from Phase243"),
            ("phase243_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase243"),
            ("phase243_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase243"),
            ("phase243_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    candidates.to_csv(output_dir / "phase243_redesign_candidate_summary.csv", index=False)
    controls.to_csv(output_dir / "phase243_control_summary.csv", index=False)
    controlled.to_csv(output_dir / "phase243_controlled_candidate_summary.csv", index=False)
    survivors.to_csv(output_dir / "phase243_survivor_candidates.csv", index=False)
    best_ledger.to_csv(output_dir / "phase243_best_candidate_trade_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase243_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase243_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase243_cost_stress_first_redesign_report.md",
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
        "scope": "phase243_cost_stress_first_redesign_search",
        **reproducibility_fields(
            artifact_id="phase243",
            generated_utc=generated_utc,
            inputs={"bars_path": str(bars_path), "phase242_dir": str(phase242_dir)},
            parameters={
                "horizons": HORIZONS,
                "event_quantiles": EVENT_QUANTILES,
                "signal_quantiles": SIGNAL_QUANTILES,
                "signal_sources": SIGNAL_SOURCES,
                "directions": DIRECTIONS,
                "random_control_runs": RANDOM_CONTROL_RUNS,
                "random_seed": RANDOM_SEED,
                "forbidden_holdout_dates": sorted(FORBIDDEN_HOLDOUT_DATES),
                "download_more_dates_now_allowed": 0,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "redesign_candidate_summary": str(output_dir / "phase243_redesign_candidate_summary.csv"),
                "control_summary": str(output_dir / "phase243_control_summary.csv"),
                "controlled_candidate_summary": str(output_dir / "phase243_controlled_candidate_summary.csv"),
                "survivor_candidates": str(output_dir / "phase243_survivor_candidates.csv"),
                "best_candidate_trade_ledger": str(output_dir / "phase243_best_candidate_trade_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase243_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase243_acceptance_summary.csv"),
                "report": str(output_dir / "phase243_cost_stress_first_redesign_report.md"),
            },
            random_seed=RANDOM_SEED,
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase235_training_discovery_event_bar_adapter_no_2026_07_17_holdout",
        ),
    }
    (output_dir / "phase243_cost_stress_first_redesign_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase243 cost-stress-first redesign search.")
    parser.add_argument("--bars-path", type=Path, default=DEFAULT_BARS_PATH)
    parser.add_argument("--phase242-dir", type=Path, default=DEFAULT_PHASE242_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(bars_path=args.bars_path, phase242_dir=args.phase242_dir, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

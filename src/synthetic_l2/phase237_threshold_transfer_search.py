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


DEFAULT_PHASE235_BARS = Path("outputs/phase235/phase235_real_event_bars.parquet")
DEFAULT_OUTPUT_DIR = Path("outputs/phase237")
HORIZONS = [2, 3, 4, 5, 6, 8, 10]
EVENT_QUANTILES = [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
SIGNAL_QUANTILES = [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
SIGNAL_SOURCES = [
    "avg_microprice_dev",
    "avg_l1_imbalance",
    "avg_top5_market_by_price_imbalance",
    "bar_return",
]
DIRECTIONS = ["reversal", "continuation"]
RANDOM_CONTROL_RUNS = 1000
RANDOM_SEED = 237


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


def load_bars(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"{path} is missing; run Phase235 first")
    bars = pd.read_parquet(path)
    required = {
        "trade_date",
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
        raise ValueError(f"Phase235 bars missing required columns: {missing}")
    return bars.sort_values(["trade_date", "symbol", "source_event_bar_id"], kind="mergesort").reset_index(drop=True)


def replay_variant(
    base_bars: pd.DataFrame,
    *,
    signal_source: str,
    direction: str,
    horizon: int,
    event_quantile: float,
    signal_quantile: float,
) -> tuple[dict[str, Any], pd.DataFrame]:
    frame = base_bars.copy()
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
    candidate_id = (
        "P237_"
        + signal_source.replace("avg_top5_market_by_price_imbalance", "TOP5_IMBALANCE")
        .replace("avg_l1_imbalance", "L1_IMBALANCE")
        .replace("avg_microprice_dev", "MICROPRICE")
        .replace("bar_return", "BAR_RETURN")
        .upper()
        + f"_{direction.upper()}_H{horizon}_EQ{str(event_quantile).replace('.', '_')}_SQ{str(signal_quantile).replace('.', '_')}"
    )
    if selected.empty:
        return {
            "candidate_id": candidate_id,
            "family_id": f"{signal_source}_{direction}",
            "signal_source": signal_source,
            "direction": direction,
            "horizon_event_bars": horizon,
            "event_quantile": event_quantile,
            "signal_quantile": signal_quantile,
            "event_window_score_threshold": event_threshold,
            "signal_abs_threshold": signal_threshold,
            "real_anchor_trades": 0,
            "real_anchor_net_pnl_inr": 0.0,
            "real_anchor_positive": False,
            "real_anchor_breadth_pass": False,
        }, selected
    selected["candidate_id"] = candidate_id
    selected["family_id"] = f"{signal_source}_{direction}"
    selected["horizon_event_bars"] = horizon
    selected["event_quantile"] = event_quantile
    selected["signal_quantile"] = signal_quantile
    selected["gross_return"] = selected["side"] * selected[future_col].astype(float)
    selected["cost_return"] = selected["taker_round_trip_cost_floor_bps"].astype(float) / 10000.0
    selected["net_return"] = selected["gross_return"] - selected["cost_return"]
    selected["gross_pnl_inr"] = selected["gross_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["cost_pnl_drag_inr"] = selected["cost_return"] * DEFAULT_ORDER_NOTIONAL_INR
    selected["net_pnl_inr"] = selected["net_return"] * DEFAULT_ORDER_NOTIONAL_INR
    date_net = selected.groupby("trade_date", sort=True)["net_pnl_inr"].sum()
    symbol_net = selected.groupby("symbol", sort=True)["net_pnl_inr"].sum()
    net = float(selected["net_pnl_inr"].sum())
    denom = abs(net) if abs(net) > 0 else np.nan
    summary = {
        "candidate_id": candidate_id,
        "family_id": f"{signal_source}_{direction}",
        "signal_source": signal_source,
        "direction": direction,
        "horizon_event_bars": horizon,
        "event_quantile": event_quantile,
        "signal_quantile": signal_quantile,
        "event_window_score_threshold": event_threshold,
        "signal_abs_threshold": signal_threshold,
        "real_anchor_trades": int(len(selected)),
        "real_anchor_net_pnl_inr": net,
        "real_anchor_gross_pnl_inr": float(selected["gross_pnl_inr"].sum()),
        "real_anchor_cost_pnl_drag_inr": float(selected["cost_pnl_drag_inr"].sum()),
        "real_anchor_dates": int(selected["trade_date"].nunique()),
        "real_anchor_symbols": int(selected["symbol"].nunique()),
        "real_anchor_positive_dates": int((date_net > 0).sum()),
        "real_anchor_min_date_net_pnl_inr": float(date_net.min()),
        "real_anchor_max_date_contribution_abs": float(date_net.abs().max() / denom) if denom and not np.isnan(denom) else np.nan,
        "real_anchor_max_symbol_contribution_abs": float(symbol_net.abs().max() / denom) if denom and not np.isnan(denom) else np.nan,
        "real_anchor_precision_cost_clear": float((selected["net_return"] > 0).mean()),
    }
    summary["real_anchor_positive"] = bool(summary["real_anchor_net_pnl_inr"] > 0)
    summary["real_anchor_breadth_pass"] = bool(
        summary["real_anchor_trades"] >= 50
        and summary["real_anchor_dates"] >= 5
        and summary["real_anchor_symbols"] >= 20
        and summary["real_anchor_positive_dates"] >= 4
    )
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


def search_variants(bars: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    ledgers: list[pd.DataFrame] = []
    for horizon in HORIZONS:
        for event_quantile in EVENT_QUANTILES:
            for signal_source in SIGNAL_SOURCES:
                for direction in DIRECTIONS:
                    for signal_quantile in SIGNAL_QUANTILES:
                        summary, ledger = replay_variant(
                            bars,
                            signal_source=signal_source,
                            direction=direction,
                            horizon=horizon,
                            event_quantile=event_quantile,
                            signal_quantile=signal_quantile,
                        )
                        if summary:
                            rows.append(summary)
                        if not ledger.empty:
                            ledgers.append(ledger)
    summary_frame = pd.DataFrame(rows).sort_values(
        ["real_anchor_net_pnl_inr", "real_anchor_trades"], ascending=[False, False]
    )
    ledger_frame = pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()
    return summary_frame, ledger_frame


def build_controls(best_trades: pd.DataFrame) -> pd.DataFrame:
    if best_trades.empty:
        return pd.DataFrame(columns=["control_id", "net_pnl_inr", "passed"])
    gross = best_trades["gross_pnl_inr"].to_numpy(dtype=float)
    cost = best_trades["cost_pnl_drag_inr"].to_numpy(dtype=float)
    net = float(best_trades["net_pnl_inr"].sum())
    future_abs = np.abs(gross + cost)
    rng = np.random.default_rng(RANDOM_SEED)
    random_nets = []
    for _ in range(RANDOM_CONTROL_RUNS):
        random_nets.append(float((rng.choice([-1.0, 1.0], size=len(best_trades)) * future_abs - cost).sum()))
    random_nets = np.asarray(random_nets)
    rows = [
        {"control_id": "SIDE_FLIP", "net_pnl_inr": float((-gross - cost).sum()), "passed": bool((-gross - cost).sum() < 0)},
        {
            "control_id": "RANDOM_SIDE_1000_RUNS",
            "net_pnl_inr": net,
            "random_p95_net_pnl_inr": float(np.quantile(random_nets, 0.95)),
            "random_beat_fraction": float((net > random_nets).mean()),
            "passed": bool((net > random_nets).mean() >= 0.95),
        },
        {"control_id": "COST_150", "net_pnl_inr": float((gross - 1.5 * cost).sum()), "passed": bool((gross - 1.5 * cost).sum() > 0)},
        {"control_id": "COST_200", "net_pnl_inr": float((gross - 2.0 * cost).sum()), "passed": bool((gross - 2.0 * cost).sum() > 0)},
    ]
    return pd.DataFrame(rows)


def build_gate_evaluation(candidates: pd.DataFrame, controls: pd.DataFrame) -> pd.DataFrame:
    positive_breadth = candidates[
        candidates["real_anchor_positive"].astype(bool) & candidates["real_anchor_breadth_pass"].astype(bool)
    ]
    best = candidates.iloc[0].to_dict() if not candidates.empty else {}
    control_pass = int(controls["passed"].astype(bool).sum()) if not controls.empty else 0
    rows = [
        ("P237_EXPANDED_VARIANTS_EVALUATED", len(candidates) >= 3000, len(candidates), ">=3000 expanded variants", "hard"),
        ("P237_BREADTH_POSITIVE_CANDIDATE_FOUND", len(positive_breadth) > 0, len(positive_breadth), ">0 positive breadth candidates", "hard"),
        ("P237_BEST_CANDIDATE_NET_POSITIVE", as_float(best.get("real_anchor_net_pnl_inr", 0)) > 0, as_float(best.get("real_anchor_net_pnl_inr", 0)), ">0 best net P&L", "hard"),
        ("P237_BEST_CANDIDATE_BREADTH", bool(best.get("real_anchor_breadth_pass", False)), f"trades={best.get('real_anchor_trades', '')};dates={best.get('real_anchor_dates', '')};symbols={best.get('real_anchor_symbols', '')}", ">=50 trades, >=5 dates, >=20 symbols, >=4 positive dates", "hard"),
        ("P237_BEST_CANDIDATE_CONTROLS", control_pass >= 3, control_pass, ">=3 / 4 controls pass", "hard"),
        ("P237_NO_PAPER_LIVE_OR_PROMOTION_UNLOCK", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase237 Threshold-transfer / Expanded Real-anchor Strategy Search Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase237 widens the real-anchor strategy search after Phase236 found positive but too-sparse microprice-reversal pockets.",
        "The key redesign is real-quantile threshold transfer: event and signal cutoffs are computed on the Phase235 real-anchor event bars, not copied from synthetic score magnitudes.",
        "This is still research evidence only and does not unlock paper/live trading or a deployable profitability claim.",
        "",
    ]
    for title, table in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(table), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(bars_path: Path = DEFAULT_PHASE235_BARS, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    bars = load_bars(bars_path)
    candidates, ledger = search_variants(bars)
    passing = candidates[
        candidates["real_anchor_positive"].astype(bool) & candidates["real_anchor_breadth_pass"].astype(bool)
    ].copy()
    best = candidates.iloc[0].to_dict() if not candidates.empty else {}
    best_id = str(best.get("candidate_id", ""))
    best_trades = ledger[ledger["candidate_id"].astype(str).eq(best_id)].copy() if not ledger.empty else pd.DataFrame()
    controls = build_controls(best_trades)
    gates = build_gate_evaluation(candidates, controls)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    hard_rows = int(len(hard))
    search_pass = int(hard_pass == hard_rows and not hard.empty)
    next_action = (
        "run_phase238_precommit_unseen_real_anchor_or_walk_forward_validation_for_phase237_candidate_no_paper_live"
        if search_pass
        else "run_phase238_redesign_real_anchor_threshold_transfer_after_phase237_failure_no_paper_live"
    )
    acceptance = pd.DataFrame(
        [
            ("phase237_threshold_transfer_search_complete", 1, "Phase237 expanded real-anchor search completed"),
            ("phase237_expanded_variant_rows", int(len(candidates)), "Expanded variants evaluated"),
            ("phase237_positive_variant_rows", int(candidates["real_anchor_positive"].astype(bool).sum()) if not candidates.empty else 0, "Positive real-anchor variants"),
            ("phase237_breadth_positive_candidate_rows", int(len(passing)), "Positive breadth candidates"),
            ("phase237_best_candidate_id", best_id, "Best candidate by real-anchor net P&L"),
            ("phase237_best_family_id", best.get("family_id", ""), "Best candidate family"),
            ("phase237_best_real_anchor_net_pnl_inr", as_float(best.get("real_anchor_net_pnl_inr", 0.0)), "Best real-anchor net P&L after costs"),
            ("phase237_best_real_anchor_trade_rows", as_int(best.get("real_anchor_trades", 0)), "Best selected trades"),
            ("phase237_best_real_anchor_dates", as_int(best.get("real_anchor_dates", 0)), "Best dates represented"),
            ("phase237_best_real_anchor_symbols", as_int(best.get("real_anchor_symbols", 0)), "Best symbols represented"),
            ("phase237_best_control_pass_rows", int(controls["passed"].astype(bool).sum()) if not controls.empty else 0, "Best candidate controls passed"),
            ("phase237_best_control_rows", int(len(controls)), "Best candidate controls evaluated"),
            ("phase237_hard_gate_pass_rows", hard_pass, "Hard Phase237 gates passed"),
            ("phase237_hard_gate_rows", hard_rows, "Hard Phase237 gates evaluated"),
            ("phase237_candidate_opened_for_phase238", search_pass, "Whether Phase238 validation precommit is opened"),
            ("phase237_strategy_promotion_allowed", 0, "No strategy promotion from Phase237"),
            ("phase237_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase237"),
            ("phase237_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase237"),
            ("phase237_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    candidates.to_csv(output_dir / "phase237_expanded_candidate_summary.csv", index=False)
    passing.to_csv(output_dir / "phase237_breadth_positive_candidates.csv", index=False)
    best_trades.to_csv(output_dir / "phase237_best_candidate_trade_ledger.csv", index=False)
    controls.to_csv(output_dir / "phase237_best_candidate_controls.csv", index=False)
    gates.to_csv(output_dir / "phase237_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase237_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase237_threshold_transfer_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Best Candidate": pd.DataFrame([best]) if best else pd.DataFrame(),
            "Breadth-positive Candidates": passing.head(20),
            "Best Candidate Controls": controls,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase237_threshold_transfer_expanded_real_anchor_search",
        **reproducibility_fields(
            artifact_id="phase237",
            generated_utc=generated_utc,
            inputs={"phase235_real_event_bars": str(bars_path)},
            parameters={
                "horizons": HORIZONS,
                "event_quantiles": EVENT_QUANTILES,
                "signal_quantiles": SIGNAL_QUANTILES,
                "signal_sources": SIGNAL_SOURCES,
                "directions": DIRECTIONS,
                "random_control_runs": RANDOM_CONTROL_RUNS,
                "random_seed": RANDOM_SEED,
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "expanded_candidate_summary": str(output_dir / "phase237_expanded_candidate_summary.csv"),
                "breadth_positive_candidates": str(output_dir / "phase237_breadth_positive_candidates.csv"),
                "best_candidate_trade_ledger": str(output_dir / "phase237_best_candidate_trade_ledger.csv"),
                "best_candidate_controls": str(output_dir / "phase237_best_candidate_controls.csv"),
                "gate_evaluation": str(output_dir / "phase237_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase237_acceptance_summary.csv"),
                "report": str(output_dir / "phase237_threshold_transfer_search_report.md"),
            },
            random_seed=RANDOM_SEED,
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase235_real_anchor_event_bar_adapter",
        ),
    }
    (output_dir / "phase237_threshold_transfer_search_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase237 threshold-transfer / expanded real-anchor strategy search.")
    parser.add_argument("--bars-path", type=Path, default=DEFAULT_PHASE235_BARS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(bars_path=args.bars_path, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

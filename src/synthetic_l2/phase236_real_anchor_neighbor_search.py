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


DEFAULT_PHASE233_CATALOG = Path("outputs/phase233/phase233_neighbor_candidate_catalog.csv")
DEFAULT_PHASE235_BARS = Path("outputs/phase235/phase235_real_event_bars.parquet")
DEFAULT_OUTPUT_DIR = Path("outputs/phase236")


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


def load_inputs(catalog_path: Path, bars_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not catalog_path.exists():
        raise FileNotFoundError(catalog_path)
    if not bars_path.exists():
        raise FileNotFoundError(f"{bars_path} is missing; run Phase235 first to regenerate local ignored event-bar parquet")
    return pd.read_csv(catalog_path), pd.read_parquet(bars_path)


def replay_one(bars: pd.DataFrame, spec: dict[str, Any]) -> tuple[dict[str, Any], pd.DataFrame]:
    horizon = as_int(spec.get("horizon_event_bars", 3), 3)
    event_threshold = as_float(spec.get("event_window_score_threshold", 0.0), 0.0)
    micro_threshold = as_float(spec.get("abs_microprice_dev_threshold", 0.0), 0.0)
    frame = bars.copy()
    future_col = f"future_return_h{horizon}"
    frame[future_col] = (
        frame.groupby(["trade_date", "symbol"], sort=False)["close_mid_price"].shift(-horizon)
        / frame["close_mid_price"]
        - 1.0
    )
    trades = frame[
        frame[future_col].notna()
        & frame["event_window_score"].ge(event_threshold)
        & frame["avg_microprice_dev"].abs().ge(micro_threshold)
    ].copy()
    trades["side"] = -np.sign(trades["avg_microprice_dev"].astype(float))
    trades = trades[trades["side"].ne(0)].copy()
    trades["candidate_id"] = str(spec.get("candidate_id", ""))
    trades["horizon_event_bars"] = horizon
    trades["threshold_quantile"] = as_float(spec.get("threshold_quantile", 0.0), 0.0)
    trades["gross_return"] = trades["side"] * trades[future_col].astype(float)
    trades["cost_return"] = trades["taker_round_trip_cost_floor_bps"].astype(float) / 10000.0
    trades["net_return"] = trades["gross_return"] - trades["cost_return"]
    trades["gross_pnl_inr"] = trades["gross_return"] * DEFAULT_ORDER_NOTIONAL_INR
    trades["cost_pnl_drag_inr"] = trades["cost_return"] * DEFAULT_ORDER_NOTIONAL_INR
    trades["net_pnl_inr"] = trades["net_return"] * DEFAULT_ORDER_NOTIONAL_INR
    if trades.empty:
        return {
            "candidate_id": str(spec.get("candidate_id", "")),
            "parent_candidate_id": str(spec.get("parent_candidate_id", "")),
            "horizon_event_bars": horizon,
            "threshold_quantile": as_float(spec.get("threshold_quantile", 0.0), 0.0),
            "real_anchor_trades": 0,
            "real_anchor_net_pnl_inr": 0.0,
            "real_anchor_gross_pnl_inr": 0.0,
            "real_anchor_cost_pnl_drag_inr": 0.0,
            "real_anchor_dates": 0,
            "real_anchor_symbols": 0,
            "real_anchor_positive_dates": 0,
            "real_anchor_min_date_net_pnl_inr": 0.0,
            "real_anchor_precision_cost_clear": 0.0,
            "real_anchor_breadth_pass": False,
            "real_anchor_positive": False,
        }, trades
    date_net = trades.groupby("trade_date", sort=True)["net_pnl_inr"].sum()
    summary = {
        "candidate_id": str(spec.get("candidate_id", "")),
        "parent_candidate_id": str(spec.get("parent_candidate_id", "")),
        "horizon_event_bars": horizon,
        "threshold_quantile": as_float(spec.get("threshold_quantile", 0.0), 0.0),
        "event_window_score_threshold": event_threshold,
        "abs_microprice_dev_threshold": micro_threshold,
        "real_anchor_trades": int(len(trades)),
        "real_anchor_net_pnl_inr": float(trades["net_pnl_inr"].sum()),
        "real_anchor_gross_pnl_inr": float(trades["gross_pnl_inr"].sum()),
        "real_anchor_cost_pnl_drag_inr": float(trades["cost_pnl_drag_inr"].sum()),
        "real_anchor_dates": int(trades["trade_date"].nunique()),
        "real_anchor_symbols": int(trades["symbol"].nunique()),
        "real_anchor_positive_dates": int((date_net > 0).sum()),
        "real_anchor_min_date_net_pnl_inr": float(date_net.min()),
        "real_anchor_precision_cost_clear": float((trades["net_return"] > 0).mean()),
    }
    summary["real_anchor_breadth_pass"] = bool(summary["real_anchor_dates"] >= 3 and summary["real_anchor_symbols"] >= 5)
    summary["real_anchor_positive"] = bool(summary["real_anchor_net_pnl_inr"] > 0)
    keep = [
        "candidate_id",
        "trade_date",
        "exchange",
        "symbol",
        "source_event_bar_id",
        "horizon_event_bars",
        "threshold_quantile",
        "side",
        "event_window_score",
        "avg_microprice_dev",
        "avg_top5_market_by_price_imbalance",
        "close_mid_price",
        future_col,
        "gross_pnl_inr",
        "cost_pnl_drag_inr",
        "net_pnl_inr",
    ]
    return summary, trades[keep]


def replay_neighbors(catalog: pd.DataFrame, bars: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    ledgers: list[pd.DataFrame] = []
    for spec in catalog.to_dict("records"):
        summary, ledger = replay_one(bars, spec)
        rows.append(summary)
        if not ledger.empty:
            ledgers.append(ledger)
    summary_frame = pd.DataFrame(rows).sort_values(
        ["real_anchor_net_pnl_inr", "real_anchor_trades"], ascending=[False, False]
    )
    ledger_frame = pd.concat(ledgers, ignore_index=True) if ledgers else pd.DataFrame()
    return summary_frame, ledger_frame


def build_gate_evaluation(summary: pd.DataFrame) -> pd.DataFrame:
    positive = int(summary["real_anchor_positive"].astype(bool).sum()) if not summary.empty else 0
    breadth = int(summary["real_anchor_breadth_pass"].astype(bool).sum()) if not summary.empty else 0
    best = summary.iloc[0].to_dict() if not summary.empty else {}
    rows = [
        ("P236_NEIGHBOR_VARIANTS_REPLAYED", len(summary) >= 12, len(summary), ">=12 Phase233 neighbor variants", "hard"),
        ("P236_POSITIVE_REAL_ANCHOR_VARIANTS_FOUND", positive > 0, positive, ">0 positive real-anchor variants", "hard"),
        ("P236_BREADTH_PASSING_VARIANTS_FOUND", breadth > 0, breadth, ">0 positive variants with >=3 dates and >=5 symbols", "hard"),
        ("P236_BEST_VARIANT_TRADE_BREADTH", as_int(best.get("real_anchor_trades", 0)) >= 25, as_int(best.get("real_anchor_trades", 0)), "best variant has >=25 trades", "hard"),
        ("P236_NO_PAPER_LIVE_OR_PROMOTION_UNLOCK", True, 0, 0, "hard"),
    ]
    return pd.DataFrame(rows, columns=["gate_id", "passed", "observed_value", "required_value", "severity"])


def write_report(path: Path, tables: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase236 Real-anchor Neighbor Search Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase236 tests the Phase233 microprice-reversal horizon/threshold neighborhood on the Phase235 real-anchor event bars.",
        "It searches for breadth around the profitable synthetic candidate, but it does not tune on real data for promotion and does not unlock paper/live trading.",
        "",
    ]
    for title, table in tables.items():
        lines.extend([f"## {title}", "", _markdown_table(table), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    catalog_path: Path = DEFAULT_PHASE233_CATALOG,
    bars_path: Path = DEFAULT_PHASE235_BARS,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    catalog, bars = load_inputs(catalog_path, bars_path)
    summary, ledger = replay_neighbors(catalog, bars)
    gates = build_gate_evaluation(summary)
    hard = gates[gates["severity"].astype(str).eq("hard")]
    hard_pass = int(hard["passed"].astype(bool).sum()) if not hard.empty else 0
    hard_rows = int(len(hard))
    positive = int(summary["real_anchor_positive"].astype(bool).sum()) if not summary.empty else 0
    breadth = int(summary["real_anchor_breadth_pass"].astype(bool).sum()) if not summary.empty else 0
    best = summary.iloc[0].to_dict() if not summary.empty else {}
    search_pass = int(positive > 0 and breadth > 0 and as_int(best.get("real_anchor_trades", 0)) >= 25)
    next_action = (
        "run_phase237_real_anchor_breadth_validation_for_best_neighbor_no_paper_live"
        if search_pass
        else "run_phase237_redesign_threshold_transfer_or_expand_real_anchor_strategy_family_no_paper_live"
    )
    acceptance = pd.DataFrame(
        [
            ("phase236_real_anchor_neighbor_search_complete", 1, "Phase236 neighbor replay completed"),
            ("phase236_neighbor_variant_rows", int(len(summary)), "Phase233 neighbor variants replayed"),
            ("phase236_positive_real_anchor_variant_rows", positive, "Positive real-anchor variants after cost floor"),
            ("phase236_breadth_passing_variant_rows", breadth, "Positive variants passing date/symbol breadth"),
            ("phase236_best_candidate_id", best.get("candidate_id", ""), "Best real-anchor neighbor by net P&L"),
            ("phase236_best_real_anchor_net_pnl_inr", as_float(best.get("real_anchor_net_pnl_inr", 0.0)), "Best real-anchor net P&L after costs"),
            ("phase236_best_real_anchor_trade_rows", as_int(best.get("real_anchor_trades", 0)), "Best real-anchor selected trades"),
            ("phase236_best_real_anchor_dates", as_int(best.get("real_anchor_dates", 0)), "Best real-anchor dates represented"),
            ("phase236_best_real_anchor_symbols", as_int(best.get("real_anchor_symbols", 0)), "Best real-anchor symbols represented"),
            ("phase236_hard_gate_pass_rows", hard_pass, "Hard Phase236 gates passed"),
            ("phase236_hard_gate_rows", hard_rows, "Hard Phase236 gates evaluated"),
            ("phase236_real_anchor_neighbor_search_pass", search_pass, "Whether any neighbor passed positive breadth gates"),
            ("phase236_strategy_promotion_allowed", 0, "No strategy promotion from Phase236"),
            ("phase236_paper_or_live_acceptance_allowed", 0, "No paper/live acceptance from Phase236"),
            ("phase236_deployable_profitability_claim_allowed", 0, "No deployable profitability claim from Phase236"),
            ("phase236_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )
    summary.to_csv(output_dir / "phase236_real_anchor_neighbor_summary.csv", index=False)
    ledger.to_csv(output_dir / "phase236_real_anchor_neighbor_trade_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase236_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase236_acceptance_summary.csv", index=False)
    write_report(
        output_dir / "phase236_real_anchor_neighbor_search_report.md",
        {
            "Acceptance Summary": acceptance,
            "Neighbor Summary": summary,
            "Gate Evaluation": gates,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase236_real_anchor_neighbor_search",
        **reproducibility_fields(
            artifact_id="phase236",
            generated_utc=generated_utc,
            inputs={
                "phase233_neighbor_candidate_catalog": str(catalog_path),
                "phase235_real_event_bars": str(bars_path),
            },
            parameters={
                "candidate_family": "P231_MICROPRICE_REVERSAL",
                "paper_or_live_acceptance_allowed": 0,
                "deployable_profitability_claim_allowed": 0,
            },
            outputs={
                "neighbor_summary": str(output_dir / "phase236_real_anchor_neighbor_summary.csv"),
                "neighbor_trade_ledger": str(output_dir / "phase236_real_anchor_neighbor_trade_ledger.csv"),
                "gate_evaluation": str(output_dir / "phase236_gate_evaluation.csv"),
                "acceptance_summary": str(output_dir / "phase236_acceptance_summary.csv"),
                "report": str(output_dir / "phase236_real_anchor_neighbor_search_report.md"),
            },
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase235_real_anchor_event_bar_adapter",
        ),
    }
    (output_dir / "phase236_real_anchor_neighbor_search_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase236 real-anchor neighbor search.")
    parser.add_argument("--catalog-path", type=Path, default=DEFAULT_PHASE233_CATALOG)
    parser.add_argument("--bars-path", type=Path, default=DEFAULT_PHASE235_BARS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    manifest = run(catalog_path=args.catalog_path, bars_path=args.bars_path, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

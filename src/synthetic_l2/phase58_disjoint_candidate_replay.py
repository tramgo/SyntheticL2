from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase56_cost_clearing_label_discovery import (
    COST_HURDLE_MULTIPLIER,
    DEFAULT_DENSE_ROOT,
    DEFAULT_ORDER_NOTIONAL_INR,
    load_observations,
    parquet_files,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase58")
DEFAULT_PHASE57_TOP = Path("outputs/phase57/interaction_top_candidates.csv")
DEFAULT_PHASE57_BIN_EDGES = Path("outputs/phase57/interaction_bin_edges.csv")


def _parse_edge(value: str) -> float:
    value = str(value).strip()
    if value.lower() == "-inf":
        return float("-inf")
    if value.lower() == "inf":
        return float("inf")
    return float(value)


def load_bin_edges(path: Path) -> dict[str, np.ndarray]:
    frame = pd.read_csv(path)
    edges: dict[str, np.ndarray] = {}
    for _, row in frame.iterrows():
        edges[str(row["bin_feature"])] = np.array([_parse_edge(item) for item in str(row["edges"]).split(";")], dtype="float64")
    return edges


def load_phase57_candidate(path: Path) -> dict[str, Any]:
    frame = pd.read_csv(path)
    if "phase57_scale_candidate" in frame.columns:
        candidates = frame[frame["phase57_scale_candidate"].astype(str).str.lower().eq("true")].copy()
        if not candidates.empty:
            return candidates.iloc[0].to_dict()
    return frame.iloc[0].to_dict()


def _apply_edges(series: pd.Series, edges: np.ndarray) -> np.ndarray:
    values = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype="float64")
    return np.searchsorted(edges[1:-1], values, side="right").astype("int16")


def add_fixed_bins(observations: pd.DataFrame, edges: dict[str, np.ndarray]) -> pd.DataFrame:
    frame = observations.copy()
    frame["abs_one_tick_return"] = frame["one_tick_return"].abs()
    frame["abs_microprice_dev"] = frame["microprice_dev"].abs()
    source_columns = {
        "abs_ret_bin": "abs_one_tick_return",
        "micro_bin": "microprice_dev",
        "abs_micro_bin": "abs_microprice_dev",
        "imb_bin": "l1_imbalance",
        "spread_bin": "spread_bps",
        "depth_bin": "l1_depth_notional",
    }
    for feature, source in source_columns.items():
        if feature in edges:
            frame[feature] = _apply_edges(frame[source], edges[feature])
    return frame


def parse_cell_key(cell_key: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in str(cell_key).split("|"):
        if not item:
            continue
        key, value = item.split("=", 1)
        result[key] = int(float(value))
    return result


def select_validation_files(dense_root: Path, start_shard: int, limit_shards: int | None) -> list[Path]:
    files = parquet_files(dense_root, limit_shards=None)
    selected = files[int(start_shard) :]
    return selected[:limit_shards] if limit_shards is not None else selected


def replay_candidate(
    observations: pd.DataFrame, candidate: dict[str, Any], edges: dict[str, np.ndarray]
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    frame = add_fixed_bins(observations, edges)
    cell = parse_cell_key(str(candidate["cell_key"]))
    horizon = int(candidate["horizon_events"])
    side = int(candidate["side"])
    mask = pd.Series(True, index=frame.index)
    for column, value in cell.items():
        mask &= frame[column].eq(value)
    coverage_rows = []
    running = pd.Series(True, index=frame.index)
    for column, value in cell.items():
        column_match = frame[column].eq(value)
        running &= column_match
        coverage_rows.append(
            {
                "cell_component": f"{column}={value}",
                "component_match_rows": int(column_match.sum()),
                "component_match_fraction": float(column_match.mean()) if len(column_match) else 0.0,
                "cumulative_match_rows": int(running.sum()),
                "cumulative_match_fraction": float(running.mean()) if len(running) else 0.0,
            }
        )
    coverage = pd.DataFrame(coverage_rows)
    future = frame[f"future_return_h{horizon}"].astype(float)
    mask &= future.notna()
    trades = frame.loc[mask].copy()
    if trades.empty:
        empty_cols = [
            "shard_index",
            "trade_date",
            "symbol",
            "trades",
            "net_pnl_inr",
            "gross_pnl_proxy_inr",
            "cost_pnl_drag_proxy_inr",
            "precision_cost_clear",
            "mean_net_return",
            "positive_after_costs",
        ]
        return pd.DataFrame(columns=empty_cols), frame.head(0), coverage

    trades["side"] = side
    trades["gross_return"] = float(side) * trades[f"future_return_h{horizon}"].astype(float)
    trades["cost_return"] = trades["retail_cost_return"].astype(float)
    trades["net_return"] = trades["gross_return"] - trades["cost_return"]
    trades["cost_clear"] = trades["gross_return"] > (trades["cost_return"] * COST_HURDLE_MULTIPLIER)
    grouped = (
        trades.groupby(["shard_index", "trade_date", "symbol"], sort=True)
        .agg(
            trades=("net_return", "size"),
            net_pnl_inr=("net_return", lambda s: float(s.sum() * DEFAULT_ORDER_NOTIONAL_INR)),
            gross_pnl_proxy_inr=("gross_return", lambda s: float(s.sum() * DEFAULT_ORDER_NOTIONAL_INR)),
            cost_pnl_drag_proxy_inr=("cost_return", lambda s: float(s.sum() * DEFAULT_ORDER_NOTIONAL_INR)),
            precision_cost_clear=("cost_clear", "mean"),
            mean_net_return=("net_return", "mean"),
            worst_trade_pnl_inr=("net_return", lambda s: float(s.min() * DEFAULT_ORDER_NOTIONAL_INR)),
            best_trade_pnl_inr=("net_return", lambda s: float(s.max() * DEFAULT_ORDER_NOTIONAL_INR)),
        )
        .reset_index()
    )
    grouped["positive_after_costs"] = grouped["net_pnl_inr"] > 0
    return grouped, trades.head(5000), coverage


def summarize(daily_symbol: pd.DataFrame, files: list[Path], candidate: dict[str, Any], elapsed_seconds: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    if daily_symbol.empty:
        summary = pd.DataFrame(
            [
                {
                    "candidate_source": "phase57",
                    "horizon_events": int(candidate["horizon_events"]),
                    "side": int(candidate["side"]),
                    "cell_key": str(candidate["cell_key"]),
                    "symbols": 0,
                    "trade_dates": 0,
                    "trades": 0,
                    "net_pnl_inr": 0.0,
                    "gross_pnl_proxy_inr": 0.0,
                    "cost_pnl_drag_proxy_inr": 0.0,
                    "positive_symbol_fraction": 0.0,
                    "precision_cost_clear": 0.0,
                    "mean_net_return": 0.0,
                    "phase58_survives_disjoint_validation": False,
                }
            ]
        )
    else:
        trades = int(daily_symbol["trades"].sum())
        summary = pd.DataFrame(
            [
                {
                    "candidate_source": "phase57",
                    "horizon_events": int(candidate["horizon_events"]),
                    "side": int(candidate["side"]),
                    "cell_key": str(candidate["cell_key"]),
                    "symbols": int(daily_symbol["symbol"].nunique()),
                    "trade_dates": int(daily_symbol["trade_date"].nunique()),
                    "shard_symbol_rows": int(len(daily_symbol)),
                    "trades": trades,
                    "net_pnl_inr": float(daily_symbol["net_pnl_inr"].sum()),
                    "gross_pnl_proxy_inr": float(daily_symbol["gross_pnl_proxy_inr"].sum()),
                    "cost_pnl_drag_proxy_inr": float(daily_symbol["cost_pnl_drag_proxy_inr"].sum()),
                    "positive_symbol_fraction": float((daily_symbol["net_pnl_inr"] > 0).mean()),
                    "positive_symbol_rows": int((daily_symbol["net_pnl_inr"] > 0).sum()),
                    "precision_cost_clear": float(
                        np.average(daily_symbol["precision_cost_clear"], weights=daily_symbol["trades"])
                    )
                    if trades
                    else 0.0,
                    "mean_net_return": float(daily_symbol["net_pnl_inr"].sum() / (trades * DEFAULT_ORDER_NOTIONAL_INR))
                    if trades
                    else 0.0,
                    "worst_symbol_net_pnl_inr": float(daily_symbol["net_pnl_inr"].min()),
                    "best_symbol_net_pnl_inr": float(daily_symbol["net_pnl_inr"].max()),
                    "phase58_survives_disjoint_validation": bool(
                        daily_symbol["net_pnl_inr"].sum() > 0
                        and trades >= 50
                        and float((daily_symbol["net_pnl_inr"] > 0).mean()) >= 0.50
                    ),
                }
            ]
        )
    acceptance = pd.DataFrame(
        [
            ("phase58_disjoint_shards_scanned", len(files), "Dense shards scanned outside Phase57 discovery shard window"),
            ("phase58_trade_rows", int(summary.iloc[0]["trades"]), "Candidate trade rows on disjoint validation shards"),
            ("phase58_net_pnl_inr", float(summary.iloc[0]["net_pnl_inr"]), "After-cost net P&L on disjoint validation shards"),
            ("phase58_positive_symbol_fraction", float(summary.iloc[0]["positive_symbol_fraction"]), "Fraction of shard-symbol rows positive after costs"),
            ("phase58_precision_cost_clear", float(summary.iloc[0]["precision_cost_clear"]), "Trade-weighted cost-clearing precision"),
            ("phase58_survives_disjoint_validation", int(bool(summary.iloc[0]["phase58_survives_disjoint_validation"])), "1 means the Phase57 candidate survived disjoint validation"),
            ("phase58_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
            ("phase58_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
            ("phase58_recommend_scale_to_month_sweep", int(bool(summary.iloc[0]["phase58_survives_disjoint_validation"])), "1 means move to broader month/symbol sweep"),
        ],
        columns=["metric", "value", "description"],
    )
    return summary, acceptance


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase58 Disjoint Candidate Replay",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase58 replays the exact Phase57-discovered interaction rule on dense shards outside the discovery window.",
        "The Phase57 bin edges and cell key are reused without refitting.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase58_disjoint_candidate_replay_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase58(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    phase57_top: Path,
    phase57_bin_edges: Path,
    start_shard: int,
    limit_shards: int | None,
    max_rows_per_shard: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = select_validation_files(dense_root, start_shard, limit_shards)
    started = time.perf_counter()
    candidate = load_phase57_candidate(phase57_top)
    edges = load_bin_edges(phase57_bin_edges)
    observations = load_observations(files, max_rows_per_shard=max_rows_per_shard, train_fraction=0.0)
    daily_symbol, trade_sample, coverage = replay_candidate(observations, candidate, edges)
    elapsed = time.perf_counter() - started
    summary, acceptance = summarize(daily_symbol, files, candidate, elapsed)

    pd.DataFrame([candidate]).to_csv(output_dir / "phase57_candidate_replayed.csv", index=False)
    coverage.to_csv(output_dir / "disjoint_candidate_cell_coverage.csv", index=False)
    daily_symbol.to_csv(output_dir / "disjoint_candidate_daily_symbol.csv", index=False)
    trade_sample.to_csv(output_dir / "disjoint_candidate_trade_sample.csv", index=False)
    summary.to_csv(output_dir / "disjoint_candidate_summary.csv", index=False)
    acceptance.to_csv(output_dir / "disjoint_candidate_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Candidate Summary": summary,
            "Daily Symbol Results": daily_symbol,
            "Cell Coverage Diagnostics": coverage,
            "Replayed Phase57 Candidate": pd.DataFrame([candidate]),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase58_disjoint_candidate_replay",
        "start_shard": start_shard,
        "dense_shards_scanned": len(files),
        "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
        "survives_disjoint_validation": int(bool(summary.iloc[0]["phase58_survives_disjoint_validation"])),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase58",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase57_top_candidates": str(phase57_top),
                "phase57_bin_edges": str(phase57_bin_edges),
            },
            parameters={
                "start_shard": start_shard,
                "limit_shards": limit_shards if limit_shards is not None else "none_remaining_lake",
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "candidate_cell_key": str(candidate["cell_key"]),
                "candidate_side": int(candidate["side"]),
                "candidate_horizon_events": int(candidate["horizon_events"]),
                "validation_gate": "net_pnl_gt_0_and_trades_ge_50_and_positive_symbol_fraction_ge_0_50",
            },
            outputs={
                "candidate": str(output_dir / "phase57_candidate_replayed.csv"),
                "cell_coverage": str(output_dir / "disjoint_candidate_cell_coverage.csv"),
                "daily_symbol": str(output_dir / "disjoint_candidate_daily_symbol.csv"),
                "trade_sample": str(output_dir / "disjoint_candidate_trade_sample.csv"),
                "summary": str(output_dir / "disjoint_candidate_summary.csv"),
                "acceptance_summary": str(output_dir / "disjoint_candidate_acceptance_summary.csv"),
                "report": str(output_dir / "phase58_disjoint_candidate_replay_report.md"),
                "manifest": str(output_dir / "phase58_disjoint_candidate_replay_manifest.json"),
            },
            random_seed="none_deterministic_disjoint_candidate_replay",
            scenario_ids="phase58_disjoint_shards_after_phase57_discovery_window",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase58_fixed_phase57_candidate_no_refit",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase58_disjoint_candidate_replay_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay the Phase57 candidate on disjoint dense shards.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--phase57-top", type=Path, default=DEFAULT_PHASE57_TOP)
    parser.add_argument("--phase57-bin-edges", type=Path, default=DEFAULT_PHASE57_BIN_EDGES)
    parser.add_argument("--start-shard", type=int, default=8, help="Zero-based shard offset; 8 skips the Phase57 discovery window.")
    parser.add_argument("--limit-shards", type=int, default=24)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase58(
        args.dense_root,
        args.output_dir,
        args.base_dir,
        args.phase57_top,
        args.phase57_bin_edges,
        args.start_shard,
        args.limit_shards,
        args.max_rows_per_shard,
    )


if __name__ == "__main__":
    main()

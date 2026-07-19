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
    HORIZONS,
    load_observations,
    parquet_files,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase57")
BIN_COUNT = 8
MIN_TRAIN_TRADES = 100
TOP_TRAIN_CELLS_PER_TEMPLATE = 30

TEMPLATES: list[tuple[str, list[str]]] = [
    ("absret_spread_depth", ["abs_ret_bin", "spread_bin", "depth_bin"]),
    ("absret_imb_spread", ["abs_ret_bin", "imb_bin", "spread_bin"]),
    ("micro_imb_spread", ["micro_bin", "imb_bin", "spread_bin"]),
    ("absmicro_spread_depth", ["abs_micro_bin", "spread_bin", "depth_bin"]),
    ("signs_spread_depth", ["ret_sign", "imb_sign", "micro_sign", "spread_bin", "depth_bin"]),
    ("all_core_interaction", ["abs_ret_bin", "micro_bin", "imb_bin", "spread_bin", "depth_bin"]),
]


def _finite_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)


def _quantile_edges(series: pd.Series, bins: int = BIN_COUNT) -> np.ndarray:
    clean = _finite_series(series).dropna()
    if clean.empty:
        return np.array([-np.inf, np.inf], dtype="float64")
    qs = np.linspace(0.0, 1.0, bins + 1)
    edges = np.unique(np.quantile(clean.to_numpy(dtype="float64"), qs))
    if len(edges) <= 2:
        value = float(clean.iloc[0])
        edges = np.array([value - 1e-12, value + 1e-12], dtype="float64")
    edges[0] = -np.inf
    edges[-1] = np.inf
    return edges.astype("float64")


def _apply_edges(series: pd.Series, edges: np.ndarray) -> np.ndarray:
    values = _finite_series(series).fillna(0.0).to_numpy(dtype="float64")
    return np.searchsorted(edges[1:-1], values, side="right").astype("int16")


def add_supervised_features(observations: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = observations.copy()
    frame["abs_one_tick_return"] = frame["one_tick_return"].abs()
    frame["abs_microprice_dev"] = frame["microprice_dev"].abs()
    frame["ret_sign"] = np.sign(frame["one_tick_return"].fillna(0.0)).astype("int8")
    frame["imb_sign"] = np.sign(frame["l1_imbalance"].fillna(0.0)).astype("int8")
    frame["micro_sign"] = np.sign(frame["microprice_dev"].fillna(0.0)).astype("int8")
    train = frame[frame["split"] == "train"]
    edge_specs = {
        "abs_ret_bin": _quantile_edges(train["abs_one_tick_return"]),
        "micro_bin": _quantile_edges(train["microprice_dev"]),
        "abs_micro_bin": _quantile_edges(train["abs_microprice_dev"]),
        "imb_bin": _quantile_edges(train["l1_imbalance"]),
        "spread_bin": _quantile_edges(train["spread_bps"]),
        "depth_bin": _quantile_edges(train["l1_depth_notional"]),
    }
    source_columns = {
        "abs_ret_bin": "abs_one_tick_return",
        "micro_bin": "microprice_dev",
        "abs_micro_bin": "abs_microprice_dev",
        "imb_bin": "l1_imbalance",
        "spread_bin": "spread_bps",
        "depth_bin": "l1_depth_notional",
    }
    edge_rows = []
    for name, edges in edge_specs.items():
        frame[name] = _apply_edges(frame[source_columns[name]], edges)
        edge_rows.append({"bin_feature": name, "edges": ";".join(f"{value:.12g}" for value in edges)})
    return frame, pd.DataFrame(edge_rows)


def _evaluate_subset(subset: pd.DataFrame, horizon: int, side: int) -> dict[str, Any]:
    if subset.empty:
        return {
            "trades": 0,
            "net_pnl_inr": 0.0,
            "gross_pnl_proxy_inr": 0.0,
            "cost_pnl_drag_proxy_inr": 0.0,
            "mean_net_return": 0.0,
            "precision_cost_clear": 0.0,
            "symbols": 0,
            "positive_symbol_fraction": 0.0,
        }
    future = subset[f"future_return_h{horizon}"].astype(float)
    cost = subset["retail_cost_return"].astype(float)
    gross = float(side) * future
    net = gross - cost
    symbol_net = pd.DataFrame({"symbol": subset["symbol"], "net": net}).groupby("symbol", sort=False)["net"].sum()
    return {
        "trades": int(len(subset)),
        "net_pnl_inr": float(net.sum() * DEFAULT_ORDER_NOTIONAL_INR),
        "gross_pnl_proxy_inr": float(gross.sum() * DEFAULT_ORDER_NOTIONAL_INR),
        "cost_pnl_drag_proxy_inr": float(cost.sum() * DEFAULT_ORDER_NOTIONAL_INR),
        "mean_net_return": float(net.mean()),
        "precision_cost_clear": float((gross > (cost * COST_HURDLE_MULTIPLIER)).mean()),
        "symbols": int(symbol_net.shape[0]),
        "positive_symbol_fraction": float((symbol_net > 0).mean()) if int(symbol_net.shape[0]) else 0.0,
    }


def mine_interactions(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train = frame[frame["split"] == "train"].copy()
    test = frame[frame["split"] == "test"].copy()
    candidates: list[dict[str, Any]] = []
    for horizon in HORIZONS:
        for template_id, columns in TEMPLATES:
            grouped = train.dropna(subset=[f"future_return_h{horizon}"]).groupby(columns, sort=False)
            train_cells: list[dict[str, Any]] = []
            for key, group in grouped:
                key_tuple = key if isinstance(key, tuple) else (key,)
                key_filter = dict(zip(columns, key_tuple))
                for side in (-1, 1):
                    metrics = _evaluate_subset(group, horizon, side)
                    if metrics["trades"] < MIN_TRAIN_TRADES:
                        continue
                    if metrics["net_pnl_inr"] <= 0:
                        continue
                    train_cells.append(
                        {
                            "horizon_events": horizon,
                            "template_id": template_id,
                            "side": side,
                            "cell_key": "|".join(f"{col}={key_filter[col]}" for col in columns),
                            "columns": ";".join(columns),
                            "train_trades": metrics["trades"],
                            "train_net_pnl_inr": metrics["net_pnl_inr"],
                            "train_precision_cost_clear": metrics["precision_cost_clear"],
                            "train_mean_net_return": metrics["mean_net_return"],
                            "key_filter": key_filter,
                        }
                    )
            train_cells = sorted(
                train_cells,
                key=lambda item: (item["train_net_pnl_inr"], item["train_precision_cost_clear"], item["train_trades"]),
                reverse=True,
            )[:TOP_TRAIN_CELLS_PER_TEMPLATE]
            for rank, cell in enumerate(train_cells, start=1):
                mask = pd.Series(True, index=test.index)
                for column, value in cell["key_filter"].items():
                    mask &= test[column].eq(value)
                test_metrics = _evaluate_subset(test.loc[mask], horizon, int(cell["side"]))
                row = {key: value for key, value in cell.items() if key != "key_filter"}
                row.update(
                    {
                        "train_rank_within_template": rank,
                        "test_trades": test_metrics["trades"],
                        "test_net_pnl_inr": test_metrics["net_pnl_inr"],
                        "test_gross_pnl_proxy_inr": test_metrics["gross_pnl_proxy_inr"],
                        "test_cost_pnl_drag_proxy_inr": test_metrics["cost_pnl_drag_proxy_inr"],
                        "test_precision_cost_clear": test_metrics["precision_cost_clear"],
                        "test_mean_net_return": test_metrics["mean_net_return"],
                        "test_symbols": test_metrics["symbols"],
                        "test_positive_symbol_fraction": test_metrics["positive_symbol_fraction"],
                    }
                )
                candidates.append(row)
    catalog = pd.DataFrame(candidates)
    if catalog.empty:
        return catalog, pd.DataFrame()
    catalog["test_positive_after_costs"] = catalog["test_net_pnl_inr"] > 0
    catalog["phase57_scale_candidate"] = (
        catalog["test_positive_after_costs"]
        & (catalog["test_trades"] >= 20)
        & (catalog["test_precision_cost_clear"] >= 0.50)
        & (catalog["test_positive_symbol_fraction"] >= 0.50)
    )
    top = catalog.sort_values(
        ["phase57_scale_candidate", "test_net_pnl_inr", "test_precision_cost_clear", "train_net_pnl_inr"],
        ascending=[False, False, False, False],
        kind="mergesort",
    ).head(30)
    return catalog.reset_index(drop=True), top.reset_index(drop=True)


def acceptance_summary(
    observations: pd.DataFrame,
    catalog: pd.DataFrame,
    top: pd.DataFrame,
    files: list[Path],
    elapsed_seconds: float,
) -> pd.DataFrame:
    traded_test = catalog["test_trades"] > 0 if not catalog.empty else pd.Series(dtype=bool)
    rows = [
        ("phase57_dense_shards_scanned", len(files), "Dense shards scanned"),
        ("phase57_observation_rows", int(len(observations)), "Feature/label observations"),
        ("phase57_train_rows", int((observations["split"] == "train").sum()) if not observations.empty else 0, "Chronological train rows"),
        ("phase57_test_rows", int((observations["split"] == "test").sum()) if not observations.empty else 0, "Chronological test rows"),
        ("phase57_interaction_candidate_rows", int(len(catalog)), "Train-positive interaction cells evaluated on test"),
        ("phase57_positive_test_rows", int((catalog["test_net_pnl_inr"] > 0).sum()) if not catalog.empty else 0, "Interaction candidates positive after retail costs on test"),
        ("phase57_scale_candidate_rows", int(catalog["phase57_scale_candidate"].sum()) if not catalog.empty else 0, "Interaction candidates passing wider-replay gate"),
        (
            "phase57_best_traded_test_net_pnl_inr",
            float(catalog.loc[traded_test, "test_net_pnl_inr"].max()) if not catalog.empty and bool(traded_test.any()) else 0.0,
            "Best test net P&L among interaction candidates with test trades",
        ),
        ("phase57_best_rule_key", str(top.iloc[0]["cell_key"]) if not top.empty else "", "Best ranked interaction cell key"),
        ("phase57_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
        ("phase57_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
        ("phase57_recommend_scale_to_wider_dense_replay", int(catalog["phase57_scale_candidate"].sum() > 0) if not catalog.empty else 0, "1 means at least one supervised interaction candidate deserves wider replay"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase57 Supervised Interaction Ranker",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase57 moves beyond hand-tuned thresholds by mining train-positive feature-interaction cells and validating them on a later chronological test split.",
        "It remains dependency-light, deterministic, no-lookahead, and after-cost.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase57_supervised_interaction_ranker_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase57(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    limit_shards: int | None,
    max_rows_per_shard: int | None,
    train_fraction: float,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = parquet_files(dense_root, limit_shards=limit_shards)
    started = time.perf_counter()
    observations = load_observations(files, max_rows_per_shard, train_fraction)
    featured, bin_edges = add_supervised_features(observations)
    catalog, top = mine_interactions(featured)
    elapsed = time.perf_counter() - started
    acceptance = acceptance_summary(featured, catalog, top, files, elapsed)

    bin_edges.to_csv(output_dir / "interaction_bin_edges.csv", index=False)
    catalog.to_csv(output_dir / "interaction_candidate_catalog.csv", index=False)
    top.to_csv(output_dir / "interaction_top_candidates.csv", index=False)
    acceptance.to_csv(output_dir / "interaction_ranker_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Top Interaction Candidates": top,
            "Bin Edges": bin_edges,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase57_supervised_interaction_ranker",
        "dense_shards_scanned": len(files),
        "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
        "train_fraction": train_fraction,
        "recommend_scale_to_wider_dense_replay": int(catalog["phase57_scale_candidate"].sum() > 0) if not catalog.empty else 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase57",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase56_cost_clearing_label_discovery": "outputs/phase56/phase56_cost_clearing_label_discovery_report.md",
            },
            parameters={
                "limit_shards": limit_shards if limit_shards is not None else "none_full_lake",
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "train_fraction": train_fraction,
                "bin_count": BIN_COUNT,
                "min_train_trades": MIN_TRAIN_TRADES,
                "templates": ";".join(item[0] for item in TEMPLATES),
                "horizons": ";".join(str(item) for item in HORIZONS),
                "cost_hurdle_multiplier": COST_HURDLE_MULTIPLIER,
            },
            outputs={
                "bin_edges": str(output_dir / "interaction_bin_edges.csv"),
                "candidate_catalog": str(output_dir / "interaction_candidate_catalog.csv"),
                "top_candidates": str(output_dir / "interaction_top_candidates.csv"),
                "acceptance_summary": str(output_dir / "interaction_ranker_acceptance_summary.csv"),
                "report": str(output_dir / "phase57_supervised_interaction_ranker_report.md"),
                "manifest": str(output_dir / "phase57_supervised_interaction_ranker_manifest.json"),
            },
            random_seed="none_deterministic_interaction_cell_mining",
            scenario_ids="phase57_bounded_first_shards_chronological_split",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase57_train_test_interaction_cells_no_order_latency_model",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase57_supervised_interaction_ranker_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mine supervised feature-interaction cells for cost-clearing dense labels.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--limit-shards", type=int, default=8)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    parser.add_argument("--train-fraction", type=float, default=0.70)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase57(args.dense_root, args.output_dir, args.base_dir, args.limit_shards, args.max_rows_per_shard, args.train_fraction)


if __name__ == "__main__":
    main()

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
from synthetic_l2.phase57_supervised_interaction_ranker import (
    MIN_TRAIN_TRADES,
    TEMPLATES,
    _evaluate_subset,
    add_supervised_features,
)
from synthetic_l2.phase58_disjoint_candidate_replay import add_fixed_bins
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase59")
TOP_DISCOVERY_CELLS_PER_TEMPLATE = 20
RELAXED_BIN_COLUMNS = {"abs_ret_bin", "micro_bin", "abs_micro_bin", "imb_bin", "spread_bin", "depth_bin"}


def _edges_from_frame(bin_edges: pd.DataFrame) -> dict[str, np.ndarray]:
    def parse(value: str) -> float:
        value = str(value).strip()
        if value.lower() == "-inf":
            return float("-inf")
        if value.lower() == "inf":
            return float("inf")
        return float(value)

    return {
        str(row["bin_feature"]): np.array([parse(item) for item in str(row["edges"]).split(";")], dtype="float64")
        for _, row in bin_edges.iterrows()
    }


def _cell_key(columns: list[str], key: Any) -> tuple[dict[str, int], str]:
    key_tuple = key if isinstance(key, tuple) else (key,)
    values = {column: int(value) for column, value in zip(columns, key_tuple)}
    return values, "|".join(f"{column}={values[column]}" for column in columns)


def _symbol_stability(frame: pd.DataFrame, horizon: int, side: int) -> dict[str, Any]:
    if frame.empty:
        return {
            "symbols": 0,
            "shards": 0,
            "positive_symbol_rows": 0,
            "positive_symbol_fraction": 0.0,
            "positive_shard_rows": 0,
            "positive_shard_fraction": 0.0,
        }
    gross = float(side) * frame[f"future_return_h{horizon}"].astype(float)
    net = gross - frame["retail_cost_return"].astype(float)
    symbol_net = pd.DataFrame({"symbol": frame["symbol"], "net": net}).groupby("symbol", sort=False)["net"].sum()
    shard_net = pd.DataFrame({"shard_index": frame["shard_index"], "net": net}).groupby("shard_index", sort=False)["net"].sum()
    return {
        "symbols": int(symbol_net.shape[0]),
        "shards": int(shard_net.shape[0]),
        "positive_symbol_rows": int((symbol_net > 0).sum()),
        "positive_symbol_fraction": float((symbol_net > 0).mean()) if int(symbol_net.shape[0]) else 0.0,
        "positive_shard_rows": int((shard_net > 0).sum()),
        "positive_shard_fraction": float((shard_net > 0).mean()) if int(shard_net.shape[0]) else 0.0,
    }


def _mask_cell(frame: pd.DataFrame, cell: dict[str, int], relaxation_radius: int) -> pd.Series:
    mask = pd.Series(True, index=frame.index)
    for column, value in cell.items():
        if relaxation_radius > 0 and column in RELAXED_BIN_COLUMNS:
            mask &= frame[column].between(int(value) - relaxation_radius, int(value) + relaxation_radius)
        else:
            mask &= frame[column].eq(value)
    return mask


def _evaluate_cell(frame: pd.DataFrame, cell: dict[str, int], horizon: int, side: int, relaxation_radius: int) -> dict[str, Any]:
    subset = frame.loc[_mask_cell(frame, cell, relaxation_radius)].dropna(subset=[f"future_return_h{horizon}"])
    metrics = _evaluate_subset(subset, horizon, side)
    metrics.update(_symbol_stability(subset, horizon, side))
    return metrics


def _evaluate_group(group: pd.DataFrame, horizon: int, side: int) -> dict[str, Any]:
    metrics = _evaluate_subset(group, horizon, side)
    metrics.update(_symbol_stability(group, horizon, side))
    return metrics


def discover_cells(discovery: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for horizon in HORIZONS:
        for template_id, columns in TEMPLATES:
            grouped = discovery.dropna(subset=[f"future_return_h{horizon}"]).groupby(columns, sort=False)
            candidates: list[dict[str, Any]] = []
            for key, group in grouped:
                cell, cell_key = _cell_key(columns, key)
                for side in (-1, 1):
                    metrics = _evaluate_group(group, horizon, side)
                    if metrics["trades"] < MIN_TRAIN_TRADES:
                        continue
                    if metrics["net_pnl_inr"] <= 0:
                        continue
                    candidates.append(
                        {
                            "template_id": template_id,
                            "columns": ";".join(columns),
                            "cell_key": cell_key,
                            "side": side,
                            "horizon_events": horizon,
                            "cell": cell,
                            "discovery_trades": metrics["trades"],
                            "discovery_net_pnl_inr": metrics["net_pnl_inr"],
                            "discovery_precision_cost_clear": metrics["precision_cost_clear"],
                            "discovery_symbols": metrics["symbols"],
                            "discovery_shards": metrics["shards"],
                            "discovery_positive_symbol_fraction": metrics["positive_symbol_fraction"],
                            "discovery_positive_shard_fraction": metrics["positive_shard_fraction"],
                        }
                    )
            candidates = sorted(
                candidates,
                key=lambda row: (
                    row["discovery_shards"],
                    row["discovery_positive_symbol_fraction"],
                    row["discovery_net_pnl_inr"],
                    row["discovery_trades"],
                ),
                reverse=True,
            )[:TOP_DISCOVERY_CELLS_PER_TEMPLATE]
            rows.extend(candidates)
    if not rows:
        return pd.DataFrame()
    catalog = pd.DataFrame([{key: value for key, value in row.items() if key != "cell"} for row in rows])
    catalog["discovery_stable"] = (
        (catalog["discovery_shards"] >= 2)
        & (catalog["discovery_symbols"] >= 2)
        & (catalog["discovery_positive_symbol_fraction"] >= 0.50)
        & (catalog["discovery_positive_shard_fraction"] >= 0.50)
    )
    return catalog


def evaluate_validation(discovery_catalog: pd.DataFrame, validation: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, row in discovery_catalog.iterrows():
        cell = {item.split("=")[0]: int(item.split("=")[1]) for item in str(row["cell_key"]).split("|")}
        for radius in (0, 1):
            metrics = _evaluate_cell(validation, cell, int(row["horizon_events"]), int(row["side"]), relaxation_radius=radius)
            output = row.to_dict()
            output.update(
                {
                    "relaxation_radius": radius,
                    "validation_trades": metrics["trades"],
                    "validation_net_pnl_inr": metrics["net_pnl_inr"],
                    "validation_gross_pnl_proxy_inr": metrics["gross_pnl_proxy_inr"],
                    "validation_cost_pnl_drag_proxy_inr": metrics["cost_pnl_drag_proxy_inr"],
                    "validation_precision_cost_clear": metrics["precision_cost_clear"],
                    "validation_symbols": metrics["symbols"],
                    "validation_shards": metrics["shards"],
                    "validation_positive_symbol_fraction": metrics["positive_symbol_fraction"],
                    "validation_positive_shard_fraction": metrics["positive_shard_fraction"],
                }
            )
            rows.append(output)
    results = pd.DataFrame(rows)
    if results.empty:
        return results
    results["validation_positive_after_costs"] = results["validation_net_pnl_inr"] > 0
    results["phase59_scale_candidate"] = (
        results["discovery_stable"]
        & results["validation_positive_after_costs"]
        & (results["validation_trades"] >= 50)
        & (results["validation_precision_cost_clear"] >= 0.50)
        & (results["validation_positive_symbol_fraction"] >= 0.50)
        & (results["validation_positive_shard_fraction"] >= 0.50)
    )
    results["has_validation_trades"] = results["validation_trades"] > 0
    return results.sort_values(
        ["phase59_scale_candidate", "has_validation_trades", "validation_net_pnl_inr", "discovery_stable", "discovery_net_pnl_inr"],
        ascending=[False, False, False, False, False],
        kind="mergesort",
    ).reset_index(drop=True)


def acceptance_summary(
    discovery: pd.DataFrame,
    validation: pd.DataFrame,
    discovery_catalog: pd.DataFrame,
    validation_results: pd.DataFrame,
    discovery_files: list[Path],
    validation_files: list[Path],
    elapsed_seconds: float,
) -> pd.DataFrame:
    traded_validation = validation_results["validation_trades"] > 0 if not validation_results.empty else pd.Series(dtype=bool)
    rows = [
        ("phase59_discovery_shards", len(discovery_files), "Dense shards used to discover stable cells"),
        ("phase59_validation_shards", len(validation_files), "Disjoint dense shards used for validation"),
        ("phase59_discovery_observation_rows", int(len(discovery)), "Discovery observation rows"),
        ("phase59_validation_observation_rows", int(len(validation)), "Validation observation rows"),
        ("phase59_train_positive_cell_rows", int(len(discovery_catalog)), "Discovery train-positive cell rows"),
        ("phase59_discovery_stable_cell_rows", int(discovery_catalog["discovery_stable"].sum()) if not discovery_catalog.empty else 0, "Cells recurring across multiple discovery shards and symbols"),
        ("phase59_validation_result_rows", int(len(validation_results)), "Exact and relaxed validation result rows"),
        ("phase59_positive_validation_rows", int((validation_results["validation_net_pnl_inr"] > 0).sum()) if not validation_results.empty else 0, "Validation rows positive after retail costs"),
        ("phase59_scale_candidate_rows", int(validation_results["phase59_scale_candidate"].sum()) if not validation_results.empty else 0, "Stable cells passing disjoint validation gate"),
        (
            "phase59_best_traded_validation_net_pnl_inr",
            float(validation_results.loc[traded_validation, "validation_net_pnl_inr"].max())
            if (not validation_results.empty and bool(traded_validation.any()))
            else 0.0,
            "Best validation net P&L among rows that emitted at least one trade",
        ),
        ("phase59_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
        ("phase59_zerodha_cost_model_version", ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION, "Zerodha retail intraday cost model"),
        ("phase59_recommend_scale_to_month_sweep", int(validation_results["phase59_scale_candidate"].sum() > 0) if not validation_results.empty else 0, "1 means at least one stable candidate deserves month/symbol sweep"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase59 Stability-Filtered Neighborhoods",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase59 addresses the Phase58 failure mode: a single exact interaction cell was profitable in discovery but absent in disjoint validation.",
        "It requires discovery recurrence across shards/symbols and validates both exact and ±1-bin relaxed neighborhoods on disjoint shards.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase59_stability_filtered_neighborhoods_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase59(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    discovery_shards: int,
    validation_start_shard: int,
    validation_shards: int,
    max_rows_per_shard: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    all_files = parquet_files(dense_root, limit_shards=None)
    discovery_files = all_files[:discovery_shards]
    validation_files = all_files[validation_start_shard : validation_start_shard + validation_shards]
    started = time.perf_counter()

    discovery_obs = load_observations(discovery_files, max_rows_per_shard=max_rows_per_shard, train_fraction=1.0)
    discovery, bin_edges = add_supervised_features(discovery_obs)
    fixed_edges = _edges_from_frame(bin_edges)
    validation_obs = load_observations(validation_files, max_rows_per_shard=max_rows_per_shard, train_fraction=0.0)
    validation = add_fixed_bins(validation_obs, fixed_edges)

    discovery_catalog = discover_cells(discovery)
    validation_results = evaluate_validation(discovery_catalog, validation) if not discovery_catalog.empty else pd.DataFrame()
    elapsed = time.perf_counter() - started
    acceptance = acceptance_summary(
        discovery,
        validation,
        discovery_catalog,
        validation_results,
        discovery_files,
        validation_files,
        elapsed,
    )
    top = validation_results.head(30) if not validation_results.empty else pd.DataFrame()

    bin_edges.to_csv(output_dir / "stability_bin_edges.csv", index=False)
    discovery_catalog.to_csv(output_dir / "stability_discovery_cell_catalog.csv", index=False)
    validation_results.to_csv(output_dir / "stability_validation_results.csv", index=False)
    top.to_csv(output_dir / "stability_top_validation_results.csv", index=False)
    acceptance.to_csv(output_dir / "stability_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Top Validation Results": top,
            "Discovery Cell Catalog Sample": discovery_catalog.head(60),
            "Bin Edges": bin_edges,
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase59_stability_filtered_neighborhoods",
        "discovery_shards": discovery_shards,
        "validation_start_shard": validation_start_shard,
        "validation_shards": validation_shards,
        "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
        "recommend_scale_to_month_sweep": int(validation_results["phase59_scale_candidate"].sum() > 0) if not validation_results.empty else 0,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase59",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase58_disjoint_candidate_replay": "outputs/phase58/phase58_disjoint_candidate_replay_report.md",
            },
            parameters={
                "discovery_shards": discovery_shards,
                "validation_start_shard": validation_start_shard,
                "validation_shards": validation_shards,
                "max_rows_per_shard": max_rows_per_shard if max_rows_per_shard is not None else "none_full_shard_scan",
                "min_train_trades": MIN_TRAIN_TRADES,
                "relaxation_radii": "0;1",
                "templates": ";".join(item[0] for item in TEMPLATES),
                "horizons": ";".join(str(item) for item in HORIZONS),
                "validation_gate": "discovery_stable_and_validation_net_gt_0_and_trades_ge_50_and_precision_ge_0_50_and_positive_symbol_fraction_ge_0_50_and_positive_shard_fraction_ge_0_50",
            },
            outputs={
                "bin_edges": str(output_dir / "stability_bin_edges.csv"),
                "discovery_catalog": str(output_dir / "stability_discovery_cell_catalog.csv"),
                "validation_results": str(output_dir / "stability_validation_results.csv"),
                "top_validation_results": str(output_dir / "stability_top_validation_results.csv"),
                "acceptance_summary": str(output_dir / "stability_acceptance_summary.csv"),
                "report": str(output_dir / "phase59_stability_filtered_neighborhoods_report.md"),
                "manifest": str(output_dir / "phase59_stability_filtered_neighborhoods_manifest.json"),
            },
            random_seed="none_deterministic_stability_cell_mining",
            scenario_ids="phase59_discovery_shards_then_disjoint_validation_shards",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase59_stability_cells_no_additional_order_latency",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase59_stability_filtered_neighborhoods_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mine stable interaction neighborhoods and validate on disjoint dense shards.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--discovery-shards", type=int, default=8)
    parser.add_argument("--validation-start-shard", type=int, default=8)
    parser.add_argument("--validation-shards", type=int, default=24)
    parser.add_argument("--max-rows-per-shard", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase59(
        args.dense_root,
        args.output_dir,
        args.base_dir,
        args.discovery_shards,
        args.validation_start_shard,
        args.validation_shards,
        args.max_rows_per_shard,
    )


if __name__ == "__main__":
    main()

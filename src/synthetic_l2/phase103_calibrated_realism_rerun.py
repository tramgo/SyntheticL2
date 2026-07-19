from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import numpy as np

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase94_generator_realism_calibration_audit import (
    DEFAULT_MAX_REAL_FILES_PER_SYMBOL,
    DEFAULT_PHASE79_DIR,
    DEFAULT_PHASE80_DIR,
    DEFAULT_PHASE83_DIR,
    DEFAULT_PHASE93_DIR,
    DEFAULT_REAL_ROOT,
    build_audit_context,
    build_calibration_comparison,
    build_gap_summary,
    build_remediation_queue,
    synthetic_anchor_profile,
)
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_SYNTHETIC_DENSE_ROOT = Path(
    "raw_synthetic_l2_phase102_anchored_price_quality/profile=P98_FULL_BOOK_REBALANCE_BASE"
)
DEFAULT_OUTPUT_DIR = Path("outputs/phase103")
DEFAULT_SYMBOLS = ["HDFCBANK"]
DEFAULT_PROFILE_ID = "P98_FULL_BOOK_REBALANCE_BASE"


def real_anchor_profile_for_symbols(real_root: Path, symbols: list[str], max_files_per_symbol: int) -> pd.DataFrame:
    frames = []
    columns = [
        "collector_received_utc_ms",
        "trade_date",
        "tradingsymbol",
        "requested_symbol",
        "buy_1_price",
        "sell_1_price",
        "buy_1_quantity",
        "sell_1_quantity",
        "buy_2_quantity",
        "sell_2_quantity",
        "buy_3_quantity",
        "sell_3_quantity",
        "buy_4_quantity",
        "sell_4_quantity",
        "buy_5_quantity",
        "sell_5_quantity",
    ]
    for symbol in symbols:
        files = sorted((real_root / f"symbol={symbol}").glob("*.parquet"))
        if len(files) > max_files_per_symbol:
            indices = np.linspace(0, len(files) - 1, max_files_per_symbol).round().astype(int)
            files = [files[int(i)] for i in sorted(set(indices))]
        for path in files:
            frame = pd.read_parquet(path, columns=columns)
            frame["source_file"] = str(path)
            frames.append(frame)
    if not frames:
        raise FileNotFoundError(f"No real parquet files found under {real_root} for symbols {symbols}")
    raw = pd.concat(frames, ignore_index=True)
    raw["symbol"] = raw["tradingsymbol"].fillna(raw["requested_symbol"]).astype(str)
    raw["ts_ms"] = raw["collector_received_utc_ms"].astype(float)
    raw["mid_price"] = (raw["buy_1_price"].astype(float) + raw["sell_1_price"].astype(float)) / 2.0
    raw["spread"] = (raw["sell_1_price"].astype(float) - raw["buy_1_price"].astype(float)).clip(lower=0.0)
    raw["l1_depth"] = raw["buy_1_quantity"].astype(float) + raw["sell_1_quantity"].astype(float)
    raw["l5_depth"] = sum(raw[f"buy_{level}_quantity"].astype(float) + raw[f"sell_{level}_quantity"].astype(float) for level in range(1, 6))
    raw["l1_imbalance"] = (raw["buy_1_quantity"].astype(float) - raw["sell_1_quantity"].astype(float)) / raw["l1_depth"].replace(0, np.nan)
    raw = raw[(raw["buy_1_price"] > 0) & (raw["sell_1_price"] > 0) & (raw["sell_1_price"] >= raw["buy_1_price"])].copy()
    raw = raw.sort_values(["symbol", "ts_ms"], kind="mergesort")
    raw["gap_ms"] = raw.groupby("symbol", sort=False)["ts_ms"].diff()
    raw["tick_return"] = raw.groupby("symbol", sort=False)["mid_price"].pct_change()
    rows: list[dict[str, Any]] = []
    for symbol, group in raw.groupby("symbol", sort=True):
        rows.append(
            {
                "symbol": symbol,
                "trade_date": str(group["trade_date"].iloc[0]),
                "rows": int(len(group)),
                "sampled_files": int(group["source_file"].nunique()),
                "first_ts_ms": float(group["ts_ms"].min()),
                "last_ts_ms": float(group["ts_ms"].max()),
                "window_seconds": float((group["ts_ms"].max() - group["ts_ms"].min()) / 1000.0),
                "median_gap_ms": float(group["gap_ms"].median()),
                "p90_gap_ms": float(group["gap_ms"].quantile(0.90)),
                "p95_gap_ms": float(group["gap_ms"].quantile(0.95)),
                "gap_le_1s_fraction": float((group["gap_ms"] <= 1000).mean()),
                "median_spread_bps": float((group["spread"] / group["mid_price"].replace(0, np.nan) * 10000.0).median()),
                "p90_spread_bps": float((group["spread"] / group["mid_price"].replace(0, np.nan) * 10000.0).quantile(0.90)),
                "median_l1_depth": float(group["l1_depth"].median()),
                "median_l5_depth": float(group["l5_depth"].median()),
                "median_abs_l1_imbalance": float(group["l1_imbalance"].abs().median()),
                "one_tick_return_std": float(group["tick_return"].std(ddof=1)),
            }
        )
    return pd.DataFrame(rows)


def summarize_phase103(
    real: pd.DataFrame,
    synthetic: pd.DataFrame,
    comparison: pd.DataFrame,
    gaps: pd.DataFrame,
    profile_id: str = DEFAULT_PROFILE_ID,
) -> pd.DataFrame:
    compared_symbols = int(comparison["symbol"].nunique()) if not comparison.empty else 0
    gap_rows = int(len(comparison))
    gap_count = int(comparison["calibration_gap"].sum()) if not comparison.empty else 0
    gap_fraction = float(gap_count / gap_rows) if gap_rows else 1.0
    severe_metric_count = int((gaps["gap_fraction"] > 0.50).sum()) if not gaps.empty else 0
    calibration_pass = bool(compared_symbols >= 1 and gap_fraction <= 0.25 and severe_metric_count == 0)
    return pd.DataFrame(
        [
            ("phase103_profile_id", profile_id, "Calibrated synthetic profile audited"),
            ("phase103_real_symbols_profiled", int(real["symbol"].nunique()) if not real.empty else 0, "Real WebSocket symbols profiled"),
            ("phase103_synthetic_symbols_profiled", int(synthetic["symbol"].nunique()) if not synthetic.empty else 0, "Synthetic dense symbols profiled"),
            ("phase103_compared_symbols", compared_symbols, "Symbols present in both real and synthetic profiles"),
            ("phase103_symbol_metric_anchor_rows", gap_rows, "Symbol/metric calibration anchors compared"),
            ("phase103_calibration_gap_rows", gap_count, "Anchor rows outside ratio gates"),
            ("phase103_calibration_gap_fraction", gap_fraction, "Fraction of compared symbol/metric anchors outside gates"),
            ("phase103_severe_metric_gap_count", severe_metric_count, "Metrics where more than half of symbols fail calibration gates"),
            ("phase103_calibrated_realism_patch_pass", int(calibration_pass), "1 means patched calibrated HDFCBANK shard passes one-symbol realism readout"),
            ("phase103_strategy_replay_allowed", 0, "Strategy replay remains closed until multiday and broader-symbol realism gates pass"),
            ("phase103_recommend_next_action", "expand_calibrated_realism_rerun_to_32_symbols_or_collect_multiday_real_panel", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase103 Calibrated Realism Rerun",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase103 compares the patched calibrated dense synthetic shard against the available real Zerodha WebSocket anchor.",
        "This is a one-symbol calibrated readout, not permission to reopen strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase103_calibrated_realism_rerun_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase103(
    real_root: Path,
    synthetic_dense_root: Path,
    phase79_dir: Path,
    phase80_dir: Path,
    phase83_dir: Path,
    phase93_dir: Path,
    output_dir: Path,
    base_dir: Path,
    symbols: list[str],
    max_real_files_per_symbol: int,
    profile_id: str = DEFAULT_PROFILE_ID,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    real = real_anchor_profile_for_symbols(real_root, symbols, max_real_files_per_symbol)
    synthetic = synthetic_anchor_profile(synthetic_dense_root)
    synthetic = synthetic[synthetic["symbol"].astype(str).isin(symbols)].copy()
    comparison = build_calibration_comparison(real, synthetic)
    gaps = build_gap_summary(comparison)
    context = build_audit_context(phase79_dir, phase80_dir, phase83_dir, phase93_dir, comparison)
    remediation = build_remediation_queue(gaps, context)
    acceptance = summarize_phase103(real, synthetic, comparison, gaps, profile_id=profile_id)

    real.to_csv(output_dir / "real_anchor_profile.csv", index=False)
    synthetic.to_csv(output_dir / "calibrated_synthetic_anchor_profile.csv", index=False)
    comparison.to_csv(output_dir / "real_vs_calibrated_synthetic_comparison.csv", index=False)
    gaps.to_csv(output_dir / "calibrated_gap_summary.csv", index=False)
    context.to_csv(output_dir / "calibrated_audit_context_ledger.csv", index=False)
    remediation.to_csv(output_dir / "calibrated_remediation_queue.csv", index=False)
    acceptance.to_csv(output_dir / "phase103_calibrated_realism_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Calibration Gap Summary": gaps,
            "Real vs Calibrated Synthetic Comparison": comparison,
            "Remediation Queue": remediation,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase103_calibrated_realism_rerun"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase103",
            generated_utc=generated_utc,
            inputs={
                "real_one_day_l2_root": str(real_root),
                "synthetic_dense_root": str(synthetic_dense_root),
                "phase102_acceptance": "outputs/phase102/phase102_material_acceptance_summary.csv",
            },
            parameters={
                "symbols": symbols,
                "profile_id": profile_id,
                "max_real_files_per_symbol": max_real_files_per_symbol,
                "strategy_replay_policy": "closed",
                "scope_limitation": "one_symbol_calibrated_dense_readout",
            },
            outputs={
                "real_anchor_profile": str(output_dir / "real_anchor_profile.csv"),
                "synthetic_anchor_profile": str(output_dir / "calibrated_synthetic_anchor_profile.csv"),
                "comparison": str(output_dir / "real_vs_calibrated_synthetic_comparison.csv"),
                "gap_summary": str(output_dir / "calibrated_gap_summary.csv"),
                "acceptance_summary": str(output_dir / "phase103_calibrated_realism_acceptance_summary.csv"),
                "report": str(output_dir / "phase103_calibrated_realism_rerun_report.md"),
                "manifest": str(output_dir / "phase103_calibrated_realism_rerun_manifest.json"),
            },
            random_seed="none_deterministic_phase103_calibrated_realism_rerun",
            scenario_ids="phase103_hdfcbank_p98_full_book_rebalance_base",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase102_anchored_calibrated_dense_price_path",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase103_calibrated_realism_rerun_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run calibrated real-vs-synthetic realism rerun.")
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--synthetic-dense-root", type=Path, default=DEFAULT_SYNTHETIC_DENSE_ROOT)
    parser.add_argument("--phase79-dir", type=Path, default=DEFAULT_PHASE79_DIR)
    parser.add_argument("--phase80-dir", type=Path, default=DEFAULT_PHASE80_DIR)
    parser.add_argument("--phase83-dir", type=Path, default=DEFAULT_PHASE83_DIR)
    parser.add_argument("--phase93-dir", type=Path, default=DEFAULT_PHASE93_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--symbols", nargs="+", default=DEFAULT_SYMBOLS)
    parser.add_argument("--max-real-files-per-symbol", type=int, default=DEFAULT_MAX_REAL_FILES_PER_SYMBOL)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase103(
        args.real_root,
        args.synthetic_dense_root,
        args.phase79_dir,
        args.phase80_dir,
        args.phase83_dir,
        args.phase93_dir,
        args.output_dir,
        args.base_dir,
        args.symbols,
        args.max_real_files_per_symbol,
    )


if __name__ == "__main__":
    main()

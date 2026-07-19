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
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_DENSE_ROOT
from synthetic_l2.phase75_timestamp_contract_matrix_validator import (
    DEFAULT_STALENESS_LIMIT_SECONDS,
    DEFAULT_TIME_BUCKET_SECONDS,
    build_synchronous_matrix,
    monthly_files,
    timestamp_contract,
    unit_contract_summary,
)
from synthetic_l2.phase76_common_overlap_matrix_validator import hdfcbank_recheck, trimmed_coverage, trim_matrix
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase77")
DEFAULT_EXCLUDE_MONTH = "2026-01"
DEFAULT_MIN_MONTHS = 3


def available_trade_months(dense_root: Path, exclude_month: str) -> list[str]:
    months = sorted(
        path.name.replace("trade_month=", "")
        for path in dense_root.glob("trade_month=*")
        if path.is_dir() and path.name.replace("trade_month=", "") != exclude_month
    )
    if not months:
        raise FileNotFoundError(f"No disjoint trade_month partitions found under {dense_root}")
    return months


def contiguous_pass_window(coverage: pd.DataFrame) -> pd.DataFrame:
    passing = coverage[coverage["coverage_pass"].astype(str).str.lower().eq("true")].copy()
    if passing.empty:
        return pd.DataFrame()
    passing = passing.sort_values(["trade_date", "global_time_bucket_id"], kind="mergesort").reset_index(drop=True)
    groups: list[pd.DataFrame] = []
    for _, group in passing.groupby("trade_date", sort=True):
        group = group.copy()
        breaks = group["global_time_bucket_id"].astype(int).diff().fillna(1).ne(1).cumsum()
        for _, run in group.groupby(breaks, sort=False):
            groups.append(run)
    return max(groups, key=len).reset_index(drop=True)


def retest_month(
    dense_root: Path,
    trade_month: str,
    time_bucket_seconds: int,
    staleness_limit_seconds: int,
    max_rows_per_symbol: int | None,
) -> dict[str, pd.DataFrame]:
    files = monthly_files(dense_root, trade_month)
    contract = timestamp_contract(files, max_rows_per_symbol)
    contract_summary = unit_contract_summary(contract)
    timestamp_unit = str(contract_summary.iloc[0]["mode_inferred_timestamp_unit"]) if not contract_summary.empty else "unknown"
    matrix, coverage = build_synchronous_matrix(files, timestamp_unit, time_bucket_seconds, staleness_limit_seconds, max_rows_per_symbol)
    window = contiguous_pass_window(coverage)
    trimmed = trim_matrix(matrix, window)
    expected_symbols = int(coverage["expected_symbols"].max()) if not coverage.empty else int(trimmed["symbol"].nunique()) if not trimmed.empty else 0
    common_coverage = trimmed_coverage(trimmed, expected_symbols)
    recheck = hdfcbank_recheck(trimmed)
    for frame in (contract, contract_summary, matrix, coverage, window, trimmed, common_coverage, recheck):
        if not frame.empty:
            frame.insert(0, "retest_trade_month", trade_month)
    return {
        "contract": contract,
        "contract_summary": contract_summary,
        "matrix": matrix,
        "coverage": coverage,
        "window": window,
        "common_matrix": trimmed,
        "common_coverage": common_coverage,
        "recheck": recheck,
    }


def month_summary(trade_month: str, frames: dict[str, pd.DataFrame], elapsed_seconds: float) -> dict[str, Any]:
    contract_summary = frames["contract_summary"]
    coverage = frames["coverage"]
    window = frames["window"]
    common_matrix = frames["common_matrix"]
    common_coverage = frames["common_coverage"]
    recheck = frames["recheck"]

    timestamp_pass = bool(contract_summary.iloc[0]["timestamp_contract_pass"]) if not contract_summary.empty else False
    raw_coverage_pass_fraction = float(coverage["coverage_pass"].mean()) if not coverage.empty else 0.0
    common_coverage_pass_fraction = float(common_coverage["coverage_pass"].mean()) if not common_coverage.empty else 0.0
    fresh_cell_fraction = float(common_matrix["fresh_cell"].mean()) if not common_matrix.empty and "fresh_cell" in common_matrix else 0.0
    recheck_pass = bool(
        not recheck.empty
        and float(recheck.iloc[0]["net_pnl_inr"]) > 0
        and float(recheck.iloc[0]["precision_cost_clear"]) >= 0.55
        and float(recheck.iloc[0]["cost_drag_to_abs_gross_ratio"]) <= 0.50
        and float(recheck.iloc[0]["positive_target_fraction"]) >= 0.50
    )
    return {
        "trade_month": trade_month,
        "timestamp_contract_pass": int(timestamp_pass),
        "raw_matrix_rows": int(len(frames["matrix"])),
        "raw_coverage_bucket_rows": int(len(coverage)),
        "raw_coverage_pass_fraction": raw_coverage_pass_fraction,
        "common_overlap_bucket_count": int(len(window)),
        "common_overlap_matrix_rows": int(len(common_matrix)),
        "common_coverage_pass_fraction": common_coverage_pass_fraction,
        "fresh_cell_fraction": fresh_cell_fraction,
        "hdfcbank_recheck_rows": int(len(recheck)),
        "hdfcbank_recheck_pass": int(recheck_pass),
        "trades": int(recheck.iloc[0]["trades"]) if not recheck.empty else 0,
        "target_symbols": int(recheck.iloc[0]["target_symbols"]) if not recheck.empty else 0,
        "net_pnl_inr": float(recheck.iloc[0]["net_pnl_inr"]) if not recheck.empty else 0.0,
        "gross_pnl_proxy_inr": float(recheck.iloc[0]["gross_pnl_proxy_inr"]) if not recheck.empty else 0.0,
        "cost_pnl_drag_proxy_inr": float(recheck.iloc[0]["cost_pnl_drag_proxy_inr"]) if not recheck.empty else 0.0,
        "precision_cost_clear": float(recheck.iloc[0]["precision_cost_clear"]) if not recheck.empty else 0.0,
        "positive_target_fraction": float(recheck.iloc[0]["positive_target_fraction"]) if not recheck.empty else 0.0,
        "cost_drag_to_abs_gross_ratio": float(recheck.iloc[0]["cost_drag_to_abs_gross_ratio"]) if not recheck.empty else np.nan,
        "elapsed_seconds": elapsed_seconds,
    }


def summarize(months: pd.DataFrame, min_months: int) -> pd.DataFrame:
    months_tested = int(len(months))
    valid_months = months[
        months["timestamp_contract_pass"].eq(1)
        & months["common_coverage_pass_fraction"].ge(0.95)
        & months["fresh_cell_fraction"].ge(0.95)
        & months["hdfcbank_recheck_rows"].gt(0)
    ].copy()
    positive_months = int((valid_months["net_pnl_inr"] > 0).sum()) if not valid_months.empty else 0
    pass_months = int(valid_months["hdfcbank_recheck_pass"].sum()) if not valid_months.empty else 0
    total_net = float(valid_months["net_pnl_inr"].sum()) if not valid_months.empty else 0.0
    total_trades = int(valid_months["trades"].sum()) if not valid_months.empty else 0
    positive_month_fraction = positive_months / float(len(valid_months) or 1)
    pass_month_fraction = pass_months / float(len(valid_months) or 1)
    aggregate_pass = bool(
        months_tested >= int(min_months)
        and len(valid_months) >= int(min_months)
        and total_net > 0
        and total_trades >= 100
        and positive_month_fraction >= 0.60
        and pass_month_fraction >= 0.60
    )
    return pd.DataFrame(
        [
            ("phase77_disjoint_months_tested", months_tested, "Non-January months retested"),
            ("phase77_valid_months", int(len(valid_months)), "Months with timestamp/common-overlap/recheck evidence"),
            ("phase77_positive_months", positive_months, "Valid months with positive synthetic net P&L"),
            ("phase77_pass_months", pass_months, "Valid months passing per-month HDFCBANK quality gates"),
            ("phase77_total_trades", total_trades, "Aggregate HDFCBANK target trades across valid months"),
            ("phase77_total_net_pnl_inr", total_net, "Aggregate after-cost synthetic net P&L across valid months"),
            ("phase77_positive_month_fraction", positive_month_fraction, "Positive valid-month fraction"),
            ("phase77_pass_month_fraction", pass_month_fraction, "Per-month gate pass fraction"),
            ("phase77_hdfcbank_disjoint_retest_pass", int(aggregate_pass), "1 means HDFCBANK lead-lag survives disjoint-month falsification"),
            (
                "phase77_recommend_next_action",
                "expand_hdfcbank_timestamp_replay_with_risk_controls" if aggregate_pass else "retire_or_redesign_hdfcbank_lead_lag_before_more_shards",
                "Recommended next action",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase77 HDFCBANK Disjoint-Month Retest",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase77 retests the Phase76 HDFCBANK lead-lag clue on trade months that were not used by the January timestamp-alignment near-miss.",
        "Each month rebuilds a global timestamp matrix, trims to the longest common-overlap fresh window, and applies the same HDFCBANK threshold and retail cost profile.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase77_hdfcbank_disjoint_month_retest_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase77(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    trade_months: list[str],
    exclude_month: str,
    time_bucket_seconds: int,
    staleness_limit_seconds: int,
    max_rows_per_symbol: int | None,
    min_months: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not trade_months:
        trade_months = available_trade_months(dense_root, exclude_month)

    all_frames: dict[str, list[pd.DataFrame]] = {
        "contract": [],
        "contract_summary": [],
        "matrix": [],
        "coverage": [],
        "window": [],
        "common_matrix": [],
        "common_coverage": [],
        "recheck": [],
    }
    month_rows: list[dict[str, Any]] = []
    started = time.perf_counter()
    for trade_month in trade_months:
        month_started = time.perf_counter()
        frames = retest_month(dense_root, trade_month, time_bucket_seconds, staleness_limit_seconds, max_rows_per_symbol)
        elapsed = time.perf_counter() - month_started
        month_rows.append(month_summary(trade_month, frames, elapsed))
        for key, frame in frames.items():
            if not frame.empty:
                all_frames[key].append(frame)

    month_detail = pd.DataFrame(month_rows)
    acceptance = summarize(month_detail, min_months)

    concat_frames = {
        key: pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
        for key, frames in all_frames.items()
    }
    month_detail.to_csv(output_dir / "disjoint_month_detail.csv", index=False)
    acceptance.to_csv(output_dir / "disjoint_month_acceptance_summary.csv", index=False)
    concat_frames["contract_summary"].to_csv(output_dir / "timestamp_contract_summary_by_month.csv", index=False)
    concat_frames["window"].to_csv(output_dir / "common_overlap_window_by_month.csv", index=False)
    concat_frames["common_coverage"].to_csv(output_dir / "common_overlap_coverage_by_month.csv", index=False)
    concat_frames["recheck"].to_csv(output_dir / "hdfcbank_recheck_by_month.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Disjoint Month Detail": month_detail,
            "HDFCBANK Recheck By Month": concat_frames["recheck"],
            "Common-Overlap Coverage By Month": concat_frames["common_coverage"],
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase77_hdfcbank_disjoint_month_retest",
        "hdfcbank_disjoint_retest_pass": int(
            acceptance.loc[acceptance["metric"].eq("phase77_hdfcbank_disjoint_retest_pass"), "value"].iloc[0]
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase77",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase76_retest_gate": "outputs/phase76/common_overlap_acceptance_summary.csv",
            },
            parameters={
                "trade_months": ",".join(trade_months),
                "exclude_month": exclude_month,
                "time_bucket_seconds": time_bucket_seconds,
                "staleness_limit_seconds": staleness_limit_seconds,
                "max_rows_per_symbol": max_rows_per_symbol if max_rows_per_symbol is not None else "none_full_symbol_scan",
                "aggregate_gate": "valid_months_ge_min_and_total_net_positive_and_total_trades_ge_100_and_positive_month_fraction_ge_0_60_and_pass_month_fraction_ge_0_60",
            },
            outputs={
                "month_detail": str(output_dir / "disjoint_month_detail.csv"),
                "acceptance_summary": str(output_dir / "disjoint_month_acceptance_summary.csv"),
                "hdfcbank_recheck_by_month": str(output_dir / "hdfcbank_recheck_by_month.csv"),
                "common_overlap_coverage_by_month": str(output_dir / "common_overlap_coverage_by_month.csv"),
                "report": str(output_dir / "phase77_hdfcbank_disjoint_month_retest_report.md"),
                "manifest": str(output_dir / "phase77_hdfcbank_disjoint_month_retest_manifest.json"),
            },
            random_seed="none_deterministic_disjoint_month_retest",
            scenario_ids="phase77_hdfcbank_disjoint_month_timestamp_common_overlap",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase77_global_clock_common_overlap_retest",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase77_hdfcbank_disjoint_month_retest_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retest Phase76 HDFCBANK lead-lag clue on disjoint synthetic months.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--trade-months", nargs="*", default=[])
    parser.add_argument("--exclude-month", type=str, default=DEFAULT_EXCLUDE_MONTH)
    parser.add_argument("--time-bucket-seconds", type=int, default=DEFAULT_TIME_BUCKET_SECONDS)
    parser.add_argument("--staleness-limit-seconds", type=int, default=DEFAULT_STALENESS_LIMIT_SECONDS)
    parser.add_argument("--max-rows-per-symbol", type=int, default=250_000)
    parser.add_argument("--min-months", type=int, default=DEFAULT_MIN_MONTHS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase77(
        dense_root=args.dense_root,
        output_dir=args.output_dir,
        base_dir=args.base_dir,
        trade_months=list(args.trade_months),
        exclude_month=args.exclude_month,
        time_bucket_seconds=args.time_bucket_seconds,
        staleness_limit_seconds=args.staleness_limit_seconds,
        max_rows_per_symbol=args.max_rows_per_symbol,
        min_months=args.min_months,
    )


if __name__ == "__main__":
    main()

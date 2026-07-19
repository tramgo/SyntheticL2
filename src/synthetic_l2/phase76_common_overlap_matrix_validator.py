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
from synthetic_l2.phase61_lower_frequency_candidate_sweep import profile_cost_bps, retail_profile
from synthetic_l2.phase70_cross_symbol_lead_lag_labels import symbol_universe
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase76")
DEFAULT_PHASE75_DIR = Path("outputs/phase75")
DEFAULT_LEADER_SYMBOL = "HDFCBANK"
DEFAULT_LEADER_THRESHOLD = 0.00428699


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
    best = max(groups, key=len)
    return best.reset_index(drop=True)


def trim_matrix(matrix: pd.DataFrame, window: pd.DataFrame) -> pd.DataFrame:
    if matrix.empty or window.empty:
        return pd.DataFrame()
    keys = window[["trade_date", "global_time_bucket_id"]].copy()
    trimmed = matrix.merge(keys, on=["trade_date", "global_time_bucket_id"], how="inner")
    trimmed = trimmed.sort_values(["global_time_bucket_id", "symbol"], kind="mergesort").reset_index(drop=True)
    trimmed["next_bar_return"] = trimmed.groupby("symbol", sort=False)["close_mid_price"].shift(-1) / trimmed["close_mid_price"].replace(0, np.nan) - 1.0
    return trimmed


def trimmed_coverage(trimmed: pd.DataFrame, expected_symbols: int) -> pd.DataFrame:
    if trimmed.empty:
        return pd.DataFrame()
    coverage = (
        trimmed.groupby(["trade_date", "global_time_bucket_id"], sort=True)
        .agg(
            symbols_present=("symbol", "nunique"),
            fresh_symbols=("fresh_cell", "sum"),
            total_rows=("rows_in_bucket", "sum"),
            max_staleness_seconds=("staleness_seconds", "max"),
            median_staleness_seconds=("staleness_seconds", "median"),
        )
        .reset_index()
    )
    coverage["expected_symbols"] = int(expected_symbols)
    coverage["coverage_fraction"] = coverage["symbols_present"] / float(expected_symbols or 1)
    coverage["fresh_fraction"] = coverage["fresh_symbols"] / float(expected_symbols or 1)
    coverage["coverage_pass"] = coverage["coverage_fraction"].ge(0.95) & coverage["fresh_fraction"].ge(0.95)
    return coverage


def hdfcbank_recheck(trimmed: pd.DataFrame) -> pd.DataFrame:
    if trimmed.empty:
        return pd.DataFrame()
    target_symbols = [symbol for symbol in symbol_universe() if symbol != DEFAULT_LEADER_SYMBOL and symbol not in {"BANKBEES", "GOLDBEES", "ITBEES", "JUNIORBEES", "NIFTYBEES"}]
    leader = trimmed[trimmed["symbol"].eq(DEFAULT_LEADER_SYMBOL)][["trade_date", "global_time_bucket_id", "bar_return"]].rename(
        columns={"bar_return": "leader_bar_return"}
    )
    targets = trimmed[trimmed["symbol"].isin(target_symbols)].copy()
    joined = targets.merge(leader, on=["trade_date", "global_time_bucket_id"], how="inner")
    joined = joined[joined["next_bar_return"].notna() & joined["leader_bar_return"].abs().ge(float(DEFAULT_LEADER_THRESHOLD))].copy()
    if joined.empty:
        return pd.DataFrame()
    profile = retail_profile()
    slippage_ticks = float(profile["fixed_slippage_ticks"])
    impact_bps = float(profile["impact_bps"]) + float(profile.get("fees_bps", 0.0))
    zerodha_bps = profile_cost_bps(profile)
    joined["side"] = np.sign(joined["leader_bar_return"].astype(float))
    joined = joined[joined["side"].ne(0)].copy()
    joined["gross_return"] = joined["side"].astype(float) * joined["next_bar_return"].astype(float)
    joined["cost_return"] = (
        ((joined["avg_spread"].astype(float) / 2.0) / joined["close_mid_price"].astype(float))
        + (slippage_ticks * joined["avg_spread"].astype(float) / joined["close_mid_price"].astype(float))
        + (impact_bps / 10000.0)
        + (zerodha_bps / 10000.0)
    )
    joined["net_return"] = joined["gross_return"] - joined["cost_return"]
    symbol_net = joined.groupby("symbol", sort=True)["net_return"].sum()
    gross = float(joined["gross_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR)
    cost = float(joined["cost_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR)
    return pd.DataFrame(
        [
            {
                "rule_id": "P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK",
                "phase70_reference_rule_id": "P70_MEGA_HDFCBANK_MOMENTUM_Q70",
                "phase73_reference_rule_id": "P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK",
                "leader_symbol": DEFAULT_LEADER_SYMBOL,
                "alignment": "common_overlap_timestamp_bucket",
                "threshold": float(DEFAULT_LEADER_THRESHOLD),
                "trades": int(len(joined)),
                "target_symbols": int(joined["symbol"].nunique()),
                "net_pnl_inr": float(joined["net_return"].sum() * DEFAULT_ORDER_NOTIONAL_INR),
                "gross_pnl_proxy_inr": gross,
                "cost_pnl_drag_proxy_inr": cost,
                "precision_cost_clear": float((joined["gross_return"] > joined["cost_return"]).mean()),
                "positive_target_fraction": float((symbol_net > 0).mean()) if int(symbol_net.shape[0]) else 0.0,
                "cost_drag_to_abs_gross_ratio": cost / abs(gross) if abs(gross) > 0 else np.nan,
            }
        ]
    )


def summarize(window: pd.DataFrame, trimmed: pd.DataFrame, coverage: pd.DataFrame, recheck: pd.DataFrame) -> pd.DataFrame:
    coverage_pass_fraction = float(coverage["coverage_pass"].mean()) if not coverage.empty else 0.0
    fresh_cell_fraction = float(trimmed["fresh_cell"].mean()) if not trimmed.empty else 0.0
    matrix_pass = bool(coverage_pass_fraction >= 0.95 and fresh_cell_fraction >= 0.95)
    recheck_pass = bool(
        not recheck.empty
        and float(recheck.iloc[0]["net_pnl_inr"]) > 0
        and float(recheck.iloc[0]["precision_cost_clear"]) >= 0.55
        and float(recheck.iloc[0]["cost_drag_to_abs_gross_ratio"]) <= 0.50
        and float(recheck.iloc[0]["positive_target_fraction"]) >= 0.50
    )
    return pd.DataFrame(
        [
            ("phase76_common_overlap_bucket_count", int(len(window)), "Contiguous passing timestamp buckets selected from Phase75"),
            ("phase76_trimmed_matrix_rows", int(len(trimmed)), "Common-overlap matrix rows"),
            ("phase76_coverage_pass_fraction", coverage_pass_fraction, "Fraction of common-overlap buckets passing coverage/freshness"),
            ("phase76_fresh_cell_fraction", fresh_cell_fraction, "Fraction of common-overlap cells fresh"),
            ("phase76_common_overlap_matrix_pass", int(matrix_pass), "1 means synchronous matrix remediation passes on common overlap"),
            ("phase76_hdfcbank_recheck_passes_gate", int(recheck_pass), "1 means HDFCBANK near-miss passes after common-overlap remediation"),
            ("phase76_allow_hdfcbank_retest_expansion", int(matrix_pass and recheck_pass), "1 means HDFCBANK retest can expand"),
            (
                "phase76_recommend_next_action",
                "hdfcbank_disjoint_month_retest" if matrix_pass and recheck_pass else "cost_precision_filter_refinement_before_hdfcbank_retest",
                "Recommended next action",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase76 Common-Overlap Synchronous Matrix Validator",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase76 trims the Phase75 timestamp matrix to the contiguous common-overlap window where all symbols are fresh.",
        "It then rechecks the HDFCBANK lead-lag near-miss on that safer window.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase76_common_overlap_matrix_validator_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase76(phase75_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix = pd.read_csv(phase75_dir / "synchronous_timestamp_matrix.csv")
    coverage = pd.read_csv(phase75_dir / "synchronous_matrix_coverage.csv")
    window = contiguous_pass_window(coverage)
    trimmed = trim_matrix(matrix, window)
    expected_symbols = int(coverage["expected_symbols"].max()) if not coverage.empty else int(trimmed["symbol"].nunique()) if not trimmed.empty else 0
    coverage_trimmed = trimmed_coverage(trimmed, expected_symbols)
    recheck = hdfcbank_recheck(trimmed)
    acceptance = summarize(window, trimmed, coverage_trimmed, recheck)

    window.to_csv(output_dir / "common_overlap_window.csv", index=False)
    trimmed.to_csv(output_dir / "common_overlap_timestamp_matrix.csv", index=False)
    coverage_trimmed.to_csv(output_dir / "common_overlap_coverage.csv", index=False)
    recheck.to_csv(output_dir / "common_overlap_hdfcbank_recheck.csv", index=False)
    acceptance.to_csv(output_dir / "common_overlap_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Common-Overlap HDFCBANK Recheck": recheck,
            "Common-Overlap Coverage": coverage_trimmed,
            "Common-Overlap Window": window,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase76_common_overlap_matrix_validator",
        "allow_hdfcbank_retest_expansion": int(acceptance.loc[acceptance["metric"].eq("phase76_allow_hdfcbank_retest_expansion"), "value"].iloc[0]),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase76",
            generated_utc=generated_utc,
            inputs={
                "phase75_matrix": str(phase75_dir / "synchronous_timestamp_matrix.csv"),
                "phase75_coverage": str(phase75_dir / "synchronous_matrix_coverage.csv"),
            },
            parameters={
                "common_overlap_rule": "longest_contiguous_window_where_phase75_coverage_pass_is_true",
                "hdfcbank_recheck_gate": "net_positive_precision_ge_0_55_cost_drag_le_0_50_positive_targets_ge_0_50",
            },
            outputs={
                "common_overlap_window": str(output_dir / "common_overlap_window.csv"),
                "common_overlap_matrix": str(output_dir / "common_overlap_timestamp_matrix.csv"),
                "common_overlap_coverage": str(output_dir / "common_overlap_coverage.csv"),
                "hdfcbank_recheck": str(output_dir / "common_overlap_hdfcbank_recheck.csv"),
                "acceptance_summary": str(output_dir / "common_overlap_acceptance_summary.csv"),
                "report": str(output_dir / "phase76_common_overlap_matrix_validator_report.md"),
                "manifest": str(output_dir / "phase76_common_overlap_matrix_validator_manifest.json"),
            },
            random_seed="none_deterministic_common_overlap_validator",
            scenario_ids="phase76_common_overlap_timestamp_matrix",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase76_common_overlap_timestamp_bucket_alignment",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase76_common_overlap_matrix_validator_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate common-overlap timestamp matrix and HDFCBANK near-miss recheck.")
    parser.add_argument("--phase75-dir", type=Path, default=DEFAULT_PHASE75_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase76(args.phase75_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

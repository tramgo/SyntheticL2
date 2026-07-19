from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase61_lower_frequency_candidate_sweep import _safe_path
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_REAL_ROOT = Path("real_data_sample/l2_single_day")
DEFAULT_SYNTHETIC_COMPACT_ROOT = Path("raw_synthetic_l2_full_year_compact_monthly")
DEFAULT_PHASE79_DIR = Path("outputs/phase79")
DEFAULT_PHASE80_DIR = Path("outputs/phase80")
DEFAULT_PHASE83_DIR = Path("outputs/phase83")
DEFAULT_PHASE93_DIR = Path("outputs/phase93")
DEFAULT_OUTPUT_DIR = Path("outputs/phase94")
DEFAULT_MAX_REAL_FILES_PER_SYMBOL = 300


def metric_value(path: Path, metric: str, default: Any = None) -> Any:
    if not path.exists():
        return default
    frame = pd.read_csv(path)
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def parquet_pattern(root: Path) -> str:
    return _safe_path(root / "**" / "*.parquet")


def select_real_files(real_root: Path, max_files_per_symbol: int) -> list[Path]:
    selected: list[Path] = []
    for symbol_dir in sorted(path for path in real_root.glob("symbol=*") if path.is_dir()):
        files = sorted(symbol_dir.glob("*.parquet"))
        if not files:
            continue
        if len(files) <= max_files_per_symbol:
            selected.extend(files)
            continue
        indices = np.linspace(0, len(files) - 1, max_files_per_symbol).round().astype(int)
        selected.extend(files[int(i)] for i in sorted(set(indices)))
    return selected


def real_anchor_profile(real_root: Path, max_files_per_symbol: int) -> pd.DataFrame:
    files = select_real_files(real_root, max_files_per_symbol)
    if not files:
        raise FileNotFoundError(f"No real parquet files found under {real_root}")
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
    for path in files:
        frame = pd.read_parquet(path, columns=columns)
        frame["source_file"] = str(path)
        frames.append(frame)
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


def synthetic_anchor_profile(compact_root: Path) -> pd.DataFrame:
    pattern = parquet_pattern(compact_root)
    con = duckdb.connect()
    try:
        return con.execute(
            f"""
            with base as (
                select
                    symbol::varchar as symbol,
                    trade_month::varchar as trade_month,
                    trade_date::varchar as trade_date,
                    callback_received_utc_ms::double as ts_ms,
                    local_sequence_id::bigint as local_sequence_id,
                    regime_code::varchar as regime_code,
                    feed_profile::varchar as feed_profile,
                    coalesce(is_market_shock_day, false) as is_market_shock_day,
                    coalesce(is_symbol_shock, false) as is_symbol_shock,
                    ((buy_1_price + sell_1_price) / 2.0)::double as mid_price,
                    greatest(sell_1_price - buy_1_price, 0.0)::double as spread,
                    (buy_1_quantity + sell_1_quantity)::double as l1_depth,
                    (
                        buy_1_quantity + sell_1_quantity + buy_2_quantity + sell_2_quantity
                        + buy_3_quantity + sell_3_quantity + buy_4_quantity + sell_4_quantity
                        + buy_5_quantity + sell_5_quantity
                    )::double as l5_depth,
                    ((buy_1_quantity - sell_1_quantity) / nullif(buy_1_quantity + sell_1_quantity, 0.0))::double as l1_imbalance
                from read_parquet('{pattern}', union_by_name=true)
                where buy_1_price > 0 and sell_1_price > 0 and sell_1_price >= buy_1_price
            ),
            seq as (
                select
                    *,
                    ts_ms - lag(ts_ms) over (partition by symbol, trade_date order by local_sequence_id) as gap_ms,
                    mid_price / nullif(lag(mid_price) over (partition by symbol, trade_date order by local_sequence_id), 0.0) - 1.0 as tick_return
                from base
            )
            select
                symbol,
                count(*)::bigint as rows,
                count(distinct trade_month)::integer as months,
                count(distinct trade_date)::integer as dates,
                count(distinct regime_code)::integer as regimes,
                count(distinct feed_profile)::integer as feed_profiles,
                avg(case when is_market_shock_day then 1.0 else 0.0 end)::double as market_shock_row_fraction,
                avg(case when is_symbol_shock then 1.0 else 0.0 end)::double as symbol_shock_row_fraction,
                quantile_cont(gap_ms, 0.50)::double as median_gap_ms,
                quantile_cont(gap_ms, 0.90)::double as p90_gap_ms,
                quantile_cont(gap_ms, 0.95)::double as p95_gap_ms,
                avg(case when gap_ms <= 1000 then 1.0 else 0.0 end)::double as gap_le_1s_fraction,
                quantile_cont(spread / nullif(mid_price, 0.0) * 10000.0, 0.50)::double as median_spread_bps,
                quantile_cont(spread / nullif(mid_price, 0.0) * 10000.0, 0.90)::double as p90_spread_bps,
                quantile_cont(l1_depth, 0.50)::double as median_l1_depth,
                quantile_cont(l5_depth, 0.50)::double as median_l5_depth,
                quantile_cont(abs(l1_imbalance), 0.50)::double as median_abs_l1_imbalance,
                stddev_samp(tick_return)::double as one_tick_return_std
            from seq
            group by symbol
            order by symbol
            """
        ).fetchdf()
    finally:
        con.close()


def ratio_flag(ratio: float, lower: float, upper: float) -> bool:
    if pd.isna(ratio) or not np.isfinite(ratio):
        return True
    return bool(ratio < lower or ratio > upper)


def build_calibration_comparison(real: pd.DataFrame, synthetic: pd.DataFrame) -> pd.DataFrame:
    merged = real.merge(synthetic, on="symbol", how="inner", suffixes=("_real", "_synthetic"))
    rows: list[dict[str, Any]] = []
    metrics = [
        ("median_gap_ms", 0.20, 5.00, "received tick cadence"),
        ("p90_gap_ms", 0.20, 5.00, "tail received tick cadence"),
        ("median_spread_bps", 0.25, 4.00, "median spread scale"),
        ("p90_spread_bps", 0.25, 4.00, "tail spread scale"),
        ("median_l1_depth", 0.10, 10.00, "displayed L1 depth scale"),
        ("median_l5_depth", 0.10, 10.00, "displayed L5 depth scale"),
        ("median_abs_l1_imbalance", 0.25, 4.00, "L1 imbalance scale"),
        ("one_tick_return_std", 0.10, 10.00, "one-tick volatility scale"),
    ]
    for row in merged.to_dict("records"):
        for metric, lower, upper, category in metrics:
            real_value = float(row.get(f"{metric}_real") or 0.0)
            synthetic_value = float(row.get(f"{metric}_synthetic") or 0.0)
            ratio = synthetic_value / real_value if real_value > 0 else np.nan
            rows.append(
                {
                    "symbol": row["symbol"],
                    "category": category,
                    "metric": metric,
                    "real_value": real_value,
                    "synthetic_value": synthetic_value,
                    "synthetic_to_real_ratio": ratio,
                    "lower_ratio_gate": lower,
                    "upper_ratio_gate": upper,
                    "calibration_gap": ratio_flag(ratio, lower, upper),
                }
            )
    return pd.DataFrame(rows)


def build_audit_context(
    phase79_dir: Path,
    phase80_dir: Path,
    phase83_dir: Path,
    phase93_dir: Path,
    comparison: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "audit_item": "strategy_mining_status",
                "evidence": f"Phase93 pass={metric_value(phase93_dir / 'event_window_replay_acceptance_summary.csv', 'phase93_low_turnover_event_replay_pass', 'missing')}",
                "decision": "strategy_mining_stopped_until_generator_audit",
                "required_action": "Do not run new strategy replay until calibration gaps are triaged.",
            },
            {
                "audit_item": "compact_generator_diversity",
                "evidence": f"Phase80 compact diversity pass={metric_value(phase80_dir / 'dense_sampling_recalibration_acceptance_summary.csv', 'phase80_compact_generator_diversity_pass', 'missing')}",
                "decision": "compact_scenario_diversity_acceptable",
                "required_action": "Keep compact regime/feed diversity design; do not revert to prefix-only sampling.",
            },
            {
                "audit_item": "dense_prefix_sampling_bias",
                "evidence": f"Phase80 biased months={metric_value(phase80_dir / 'dense_sampling_recalibration_acceptance_summary.csv', 'phase80_dense_prefix_biased_months', 'missing')}",
                "decision": "prefix_sampling_not_allowed_for_acceptance",
                "required_action": "Require stratified windows/cached bars for any replay evidence.",
            },
            {
                "audit_item": "stratified_replay_cache",
                "evidence": f"Phase83 pass={metric_value(phase83_dir / 'stratified_source_event_bar_acceptance_summary.csv', 'phase83_stratified_bar_cache_pass', 'missing')}",
                "decision": "coverage_cache_usable",
                "required_action": "Use Phase83-like coverage tables for future replay audits.",
            },
            {
                "audit_item": "real_anchor_calibration",
                "evidence": f"{int(comparison['calibration_gap'].sum())}/{int(len(comparison))} symbol-metric anchors outside ratio gates",
                "decision": "calibration_triage_required",
                "required_action": "Rank spread/depth/cadence/volatility gaps and collect more real days before restarting strategy mining.",
            },
        ]
    )


def build_gap_summary(comparison: pd.DataFrame) -> pd.DataFrame:
    if comparison.empty:
        return pd.DataFrame()
    return (
        comparison.groupby(["category", "metric"], sort=True)
        .agg(
            symbol_metrics=("symbol", "count"),
            gap_count=("calibration_gap", "sum"),
            gap_fraction=("calibration_gap", "mean"),
            median_synthetic_to_real_ratio=("synthetic_to_real_ratio", "median"),
            min_synthetic_to_real_ratio=("synthetic_to_real_ratio", "min"),
            max_synthetic_to_real_ratio=("synthetic_to_real_ratio", "max"),
        )
        .reset_index()
    )


def build_remediation_queue(gaps: pd.DataFrame, context: pd.DataFrame) -> pd.DataFrame:
    ranked = gaps.sort_values(["gap_fraction", "symbol_metrics"], ascending=[False, False], kind="mergesort").head(5)
    rows: list[dict[str, Any]] = []
    priority = 1
    rows.append(
        {
            "priority": priority,
            "work_item": "collect_multi_day_real_anchor_panel",
            "why": "A single real WebSocket day cannot identify regime frequencies, annual tails, month effects, or stable cross-regime calibration.",
            "minimum_deliverable": "At least 5-10 full real trading days across normal, volatile, and shock-like sessions with the same 54-column WebSocket schema.",
            "acceptance_gate": "Real anchor profile table has multiple dates per symbol and reports stable cadence/spread/depth ranges before strategy mining resumes.",
        }
    )
    priority += 1
    for gap in ranked.to_dict("records"):
        rows.append(
            {
                "priority": priority,
                "work_item": f"calibrate_{gap['metric']}",
                "why": (
                    f"{float(gap['gap_fraction']):.2%} of symbol anchors are outside ratio gates; "
                    f"median synthetic/real ratio={float(gap['median_synthetic_to_real_ratio']):.3f}."
                ),
                "minimum_deliverable": f"Adjust generator calibration for {gap['category']} and rerun Phase94 comparison.",
                "acceptance_gate": "Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel.",
            }
        )
        priority += 1
    rows.append(
        {
            "priority": priority,
            "work_item": "freeze_strategy_replay_until_calibration_gate",
            "why": "Phase93 explicitly stopped strategy mining; new strategy branches would be fishing unless realism gaps are triaged.",
            "minimum_deliverable": "Machine-readable gate that blocks Phase95+ strategy replay unless Phase94 calibration_replay_resume_allowed=1.",
            "acceptance_gate": "No new strategy replay milestone is marked ready while calibration audit fails.",
        }
    )
    return pd.DataFrame(rows)


def summarize(real: pd.DataFrame, synthetic: pd.DataFrame, comparison: pd.DataFrame, gaps: pd.DataFrame, context: pd.DataFrame) -> pd.DataFrame:
    compared_symbols = int(comparison["symbol"].nunique()) if not comparison.empty else 0
    gap_count = int(comparison["calibration_gap"].sum()) if not comparison.empty else 0
    gap_rows = int(len(comparison))
    gap_fraction = float(gap_count / gap_rows) if gap_rows else 1.0
    severe_metric_count = int((gaps["gap_fraction"] > 0.50).sum()) if not gaps.empty else 0
    phase93_pass = metric_value(DEFAULT_PHASE93_DIR / "event_window_replay_acceptance_summary.csv", "phase93_low_turnover_event_replay_pass", 0)
    calibration_pass = bool(compared_symbols >= 30 and gap_fraction <= 0.25 and severe_metric_count == 0)
    resume_allowed = bool(calibration_pass and float(phase93_pass) == 1)
    return pd.DataFrame(
        [
            ("phase94_real_symbols_profiled", int(real["symbol"].nunique()) if not real.empty else 0, "Real one-day WebSocket symbols profiled"),
            ("phase94_synthetic_symbols_profiled", int(synthetic["symbol"].nunique()) if not synthetic.empty else 0, "Synthetic compact symbols profiled"),
            ("phase94_compared_symbols", compared_symbols, "Symbols present in both real and synthetic profiles"),
            ("phase94_symbol_metric_anchor_rows", gap_rows, "Symbol/metric calibration anchors compared"),
            ("phase94_calibration_gap_rows", gap_count, "Anchor rows outside ratio gates"),
            ("phase94_calibration_gap_fraction", gap_fraction, "Fraction of compared symbol/metric anchors outside gates"),
            ("phase94_severe_metric_gap_count", severe_metric_count, "Metrics where more than half of symbols fail calibration gates"),
            ("phase94_generator_calibration_pass", int(calibration_pass), "1 means current generator calibration is strong enough to reopen strategy mining"),
            ("phase94_strategy_replay_resume_allowed", int(resume_allowed), "1 means strategy mining may resume immediately"),
            ("phase94_recommend_next_action", "collect_multi_day_real_anchor_panel_and_calibrate_gaps", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase94 Generator Realism Calibration Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase94 executes the stop condition from Phase93: strategy mining pauses and the generator/calibration evidence is audited.",
        "The audit compares one-day real Zerodha WebSocket anchors against the synthetic compact full-year lake and consolidates Phase79/80/83/93 realism context.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase94_generator_realism_calibration_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase94(
    real_root: Path,
    synthetic_compact_root: Path,
    phase79_dir: Path,
    phase80_dir: Path,
    phase83_dir: Path,
    phase93_dir: Path,
    output_dir: Path,
    base_dir: Path,
    max_real_files_per_symbol: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    real = real_anchor_profile(real_root, max_real_files_per_symbol)
    synthetic = synthetic_anchor_profile(synthetic_compact_root)
    comparison = build_calibration_comparison(real, synthetic)
    gaps = build_gap_summary(comparison)
    context = build_audit_context(phase79_dir, phase80_dir, phase83_dir, phase93_dir, comparison)
    remediation = build_remediation_queue(gaps, context)
    acceptance = summarize(real, synthetic, comparison, gaps, context)

    real.to_csv(output_dir / "real_one_day_anchor_profile.csv", index=False)
    synthetic.to_csv(output_dir / "synthetic_compact_anchor_profile.csv", index=False)
    comparison.to_csv(output_dir / "real_vs_synthetic_calibration_comparison.csv", index=False)
    gaps.to_csv(output_dir / "calibration_gap_summary.csv", index=False)
    context.to_csv(output_dir / "generator_audit_context_ledger.csv", index=False)
    remediation.to_csv(output_dir / "calibration_remediation_queue.csv", index=False)
    acceptance.to_csv(output_dir / "generator_realism_calibration_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Calibration Gap Summary": gaps,
            "Audit Context Ledger": context,
            "Remediation Queue": remediation,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase94_generator_realism_calibration_audit"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase94",
            generated_utc=generated_utc,
            inputs={
                "real_one_day_l2_root": str(real_root),
                "synthetic_compact_root": str(synthetic_compact_root),
                "phase79_summary": str(phase79_dir / "generator_scenario_diversity_acceptance_summary.csv"),
                "phase80_summary": str(phase80_dir / "dense_sampling_recalibration_acceptance_summary.csv"),
                "phase83_summary": str(phase83_dir / "stratified_source_event_bar_acceptance_summary.csv"),
                "phase93_summary": str(phase93_dir / "event_window_replay_acceptance_summary.csv"),
            },
            parameters={
                "calibration_ratio_gates": "metric_specific_lower_upper_bounds_in_real_vs_synthetic_comparison",
                "strategy_mining_policy": "paused_after_phase93_until_calibration_audit_passes",
                "single_day_real_anchor_limitation": "cannot_estimate_regime_frequency_or_annual_tails",
                "max_real_files_per_symbol": max_real_files_per_symbol,
            },
            outputs={
                "real_anchor_profile": str(output_dir / "real_one_day_anchor_profile.csv"),
                "synthetic_anchor_profile": str(output_dir / "synthetic_compact_anchor_profile.csv"),
                "comparison": str(output_dir / "real_vs_synthetic_calibration_comparison.csv"),
                "gap_summary": str(output_dir / "calibration_gap_summary.csv"),
                "context_ledger": str(output_dir / "generator_audit_context_ledger.csv"),
                "remediation_queue": str(output_dir / "calibration_remediation_queue.csv"),
                "acceptance_summary": str(output_dir / "generator_realism_calibration_acceptance_summary.csv"),
                "report": str(output_dir / "phase94_generator_realism_calibration_audit_report.md"),
                "manifest": str(output_dir / "phase94_generator_realism_calibration_audit_manifest.json"),
            },
            random_seed="none_deterministic_generator_calibration_audit",
            scenario_ids="phase94_post_phase93_generator_realism_audit",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_calibration_audit",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase94_generator_realism_calibration_audit_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run generator realism calibration audit after strategy-mining stop.")
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--synthetic-compact-root", type=Path, default=DEFAULT_SYNTHETIC_COMPACT_ROOT)
    parser.add_argument("--phase79-dir", type=Path, default=DEFAULT_PHASE79_DIR)
    parser.add_argument("--phase80-dir", type=Path, default=DEFAULT_PHASE80_DIR)
    parser.add_argument("--phase83-dir", type=Path, default=DEFAULT_PHASE83_DIR)
    parser.add_argument("--phase93-dir", type=Path, default=DEFAULT_PHASE93_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--max-real-files-per-symbol", type=int, default=DEFAULT_MAX_REAL_FILES_PER_SYMBOL)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase94(
        args.real_root,
        args.synthetic_compact_root,
        args.phase79_dir,
        args.phase80_dir,
        args.phase83_dir,
        args.phase93_dir,
        args.output_dir,
        args.base_dir,
        args.max_real_files_per_symbol,
    )


if __name__ == "__main__":
    main()

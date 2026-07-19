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
from synthetic_l2.phase80_dense_sampling_recalibration_contract import entropy
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase81")
DEFAULT_PHASE80_DIR = Path("outputs/phase80")
DEFAULT_DENSE_ROOT = Path("raw_synthetic_l2_dense_full_year")
DEFAULT_CONTROL_SYMBOL = "HDFCBANK"


def select_regime_covering_dates(detail: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for month, month_frame in detail.groupby("trade_month", sort=True):
        by_day = (
            month_frame.groupby(["trade_month", "trade_date", "regime_code"], sort=True)
            .agg(
                source_rows=("row_count", "sum"),
                market_shock_rows=("market_shock_rows", "sum"),
                symbol_shock_rows=("symbol_shock_rows", "sum"),
                feed_profiles=("feed_profile", "nunique"),
            )
            .reset_index()
        )
        # One date per regime. Prefer days with shock evidence, then larger source coverage.
        by_day["shock_rows"] = by_day["market_shock_rows"].astype(int) + by_day["symbol_shock_rows"].astype(int)
        for regime_code, regime_frame in by_day.groupby("regime_code", sort=True):
            chosen = regime_frame.sort_values(
                ["shock_rows", "source_rows", "trade_date"],
                ascending=[False, False, True],
                kind="mergesort",
            ).iloc[0]
            rows.append(
                {
                    "trade_month": month,
                    "selected_trade_date": chosen["trade_date"],
                    "selected_regime_code": regime_code,
                    "source_rows": int(chosen["source_rows"]),
                    "market_shock_rows": int(chosen["market_shock_rows"]),
                    "symbol_shock_rows": int(chosen["symbol_shock_rows"]),
                    "feed_profiles_on_day": int(chosen["feed_profiles"]),
                    "selection_reason": "one_representative_source_day_per_regime_prefer_shock_then_rows",
                }
            )
    return pd.DataFrame(rows).sort_values(["trade_month", "selected_trade_date", "selected_regime_code"], kind="mergesort").reset_index(drop=True)


def build_monthly_plan(detail: pd.DataFrame, selected_dates: pd.DataFrame) -> pd.DataFrame:
    compact_rows: list[dict[str, Any]] = []
    for month, month_frame in detail.groupby("trade_month", sort=True):
        selected = selected_dates[selected_dates["trade_month"].eq(month)]
        selected_detail = month_frame[month_frame["trade_date"].isin(selected["selected_trade_date"].tolist())].copy()
        compact_regime_counts = month_frame.groupby("regime_code", sort=True)["row_count"].sum()
        selected_regime_counts = selected_detail.groupby("regime_code", sort=True)["row_count"].sum()
        compact_feed_counts = month_frame.groupby("feed_profile", sort=True)["row_count"].sum()
        selected_feed_counts = selected_detail.groupby("feed_profile", sort=True)["row_count"].sum()
        compact_rows.append(
            {
                "trade_month": month,
                "compact_days": int(month_frame["trade_date"].nunique()),
                "selected_days": int(selected["selected_trade_date"].nunique()),
                "compact_regime_codes": int(compact_regime_counts.shape[0]),
                "selected_regime_codes": int(selected_regime_counts.shape[0]),
                "regime_code_capture_fraction": float(selected_regime_counts.shape[0] / max(compact_regime_counts.shape[0], 1)),
                "compact_regime_entropy_bits": entropy(compact_regime_counts),
                "selected_regime_entropy_bits": entropy(selected_regime_counts),
                "regime_entropy_capture_fraction": entropy(selected_regime_counts) / entropy(compact_regime_counts) if entropy(compact_regime_counts) else 0.0,
                "compact_feed_profiles": int(compact_feed_counts.shape[0]),
                "selected_feed_profiles": int(selected_feed_counts.shape[0]),
                "feed_profile_capture_fraction": float(selected_feed_counts.shape[0] / max(compact_feed_counts.shape[0], 1)),
                "selected_source_rows": int(selected_detail["row_count"].sum()),
                "selected_market_shock_rows": int(selected_detail["market_shock_rows"].sum()),
                "selected_symbol_shock_rows": int(selected_detail["symbol_shock_rows"].sum()),
            }
        )
    plan = pd.DataFrame(compact_rows)
    plan["stratified_window_pass"] = (
        plan["regime_code_capture_fraction"].ge(1.0)
        & plan["regime_entropy_capture_fraction"].ge(0.75)
        & plan["feed_profile_capture_fraction"].ge(1.0)
    )
    return plan


def predicate_for_month(selected_dates: pd.DataFrame, month: str, feed_profiles: list[str]) -> str:
    dates = sorted(selected_dates[selected_dates["trade_month"].eq(month)]["selected_trade_date"].astype(str).unique().tolist())
    date_list = ", ".join(f"'{date}'" for date in dates)
    feed_list = ", ".join(f"'{feed}'" for feed in sorted(feed_profiles))
    return f"trade_month = '{month}' and trade_date in ({date_list}) and feed_profile in ({feed_list})"


def build_reader_contract(detail: pd.DataFrame, selected_dates: pd.DataFrame) -> pd.DataFrame:
    feed_profiles = sorted(detail["feed_profile"].astype(str).unique().tolist())
    rows = []
    for month in sorted(detail["trade_month"].astype(str).unique().tolist()):
        rows.append(
            {
                "trade_month": month,
                "reader_id": f"P81_STRATIFIED_DENSE_WINDOW_{month}",
                "dense_where_predicate": predicate_for_month(selected_dates, month, feed_profiles),
                "feed_profiles": "|".join(feed_profiles),
                "selected_trade_dates": "|".join(
                    sorted(selected_dates[selected_dates["trade_month"].eq(month)]["selected_trade_date"].astype(str).unique().tolist())
                ),
                "contract": "Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation.",
            }
        )
    return pd.DataFrame(rows)


def verify_dense_control(dense_root: Path, selected_dates: pd.DataFrame, detail: pd.DataFrame, control_symbol: str) -> pd.DataFrame:
    feed_profiles = sorted(detail["feed_profile"].astype(str).unique().tolist())
    rows: list[dict[str, Any]] = []
    con = duckdb.connect()
    try:
        for month in sorted(selected_dates["trade_month"].astype(str).unique().tolist()):
            path = dense_root / f"trade_month={month}" / f"symbol={control_symbol}" / "part-00000.parquet"
            selected = selected_dates[selected_dates["trade_month"].eq(month)]
            if not path.exists():
                rows.append(
                    {
                        "trade_month": month,
                        "control_symbol": control_symbol,
                        "dense_path_exists": False,
                        "selected_trade_dates_found": 0,
                        "selected_regime_codes_found": 0,
                        "selected_feed_profiles_found": 0,
                        "selected_dense_rows_found": 0,
                        "dense_control_pass": False,
                    }
                )
                continue
            predicate = predicate_for_month(selected_dates, month, feed_profiles)
            frame = con.execute(
                f"""
                select
                    count(*)::bigint as selected_dense_rows_found,
                    count(distinct trade_date)::integer as selected_trade_dates_found,
                    count(distinct regime_code)::integer as selected_regime_codes_found,
                    count(distinct feed_profile)::integer as selected_feed_profiles_found,
                    min(local_sequence_id)::bigint as min_local_sequence_id,
                    max(local_sequence_id)::bigint as max_local_sequence_id
                from read_parquet('{_safe_path(path)}', union_by_name=true)
                where {predicate}
                """
            ).fetchdf().iloc[0].to_dict()
            expected_dates = int(selected["selected_trade_date"].nunique())
            expected_regimes = int(selected["selected_regime_code"].nunique())
            expected_feeds = len(feed_profiles)
            rows.append(
                {
                    "trade_month": month,
                    "control_symbol": control_symbol,
                    "dense_path_exists": True,
                    "expected_selected_trade_dates": expected_dates,
                    "expected_selected_regime_codes": expected_regimes,
                    "expected_feed_profiles": expected_feeds,
                    **frame,
                    "dense_control_pass": bool(
                        int(frame["selected_trade_dates_found"]) == expected_dates
                        and int(frame["selected_regime_codes_found"]) == expected_regimes
                        and int(frame["selected_feed_profiles_found"]) == expected_feeds
                        and int(frame["selected_dense_rows_found"]) > 0
                    ),
                }
            )
    finally:
        con.close()
    return pd.DataFrame(rows)


def summarize(monthly_plan: pd.DataFrame, dense_control: pd.DataFrame) -> pd.DataFrame:
    plan_pass_fraction = float(monthly_plan["stratified_window_pass"].mean()) if not monthly_plan.empty else 0.0
    dense_control_pass_fraction = float(dense_control["dense_control_pass"].mean()) if not dense_control.empty else 0.0
    reader_pass = bool(plan_pass_fraction >= 1.0 and dense_control_pass_fraction >= 1.0)
    return pd.DataFrame(
        [
            ("phase81_months_planned", int(len(monthly_plan)), "Months with stratified dense-window plans"),
            ("phase81_plan_pass_fraction", plan_pass_fraction, "Fraction of month plans passing compact diversity capture gates"),
            ("phase81_dense_control_pass_fraction", dense_control_pass_fraction, "Fraction of month plans verified on dense control symbol"),
            ("phase81_min_selected_days", int(monthly_plan["selected_days"].min()), "Minimum selected source days per month"),
            ("phase81_max_selected_days", int(monthly_plan["selected_days"].max()), "Maximum selected source days per month"),
            ("phase81_stratified_dense_window_reader_pass", int(reader_pass), "1 means stratified reader contract is ready for replay use"),
            (
                "phase81_recommend_next_action",
                "rerun_hdfcbank_disjoint_retest_with_stratified_windows" if reader_pass else "fix_stratified_window_reader",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase81 Stratified Dense-Window Reader",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase81 implements the Phase80 recalibration contract by selecting source-day/regime/feed-profile balanced dense windows.",
        "It emits explicit predicates that future dense audits and replays can use instead of prefix-only `local_sequence_id` windows.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase81_stratified_dense_window_reader_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase81(phase80_dir: Path, dense_root: Path, output_dir: Path, base_dir: Path, control_symbol: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    detail = pd.read_csv(phase80_dir / "compact_daily_scenario_detail.csv")
    selected_dates = select_regime_covering_dates(detail)
    monthly_plan = build_monthly_plan(detail, selected_dates)
    reader_contract = build_reader_contract(detail, selected_dates)
    dense_control = verify_dense_control(dense_root, selected_dates, detail, control_symbol)
    acceptance = summarize(monthly_plan, dense_control)

    selected_dates.to_csv(output_dir / "stratified_selected_source_dates.csv", index=False)
    monthly_plan.to_csv(output_dir / "stratified_window_monthly_plan.csv", index=False)
    reader_contract.to_csv(output_dir / "stratified_dense_reader_contract.csv", index=False)
    dense_control.to_csv(output_dir / "stratified_dense_control_verification.csv", index=False)
    acceptance.to_csv(output_dir / "stratified_dense_window_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Stratified Window Monthly Plan": monthly_plan,
            "Dense Control Verification": dense_control,
            "Reader Contract Sample": reader_contract.head(12),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase81_stratified_dense_window_reader",
        "stratified_dense_window_reader_pass": int(
            acceptance.loc[acceptance["metric"].eq("phase81_stratified_dense_window_reader_pass"), "value"].iloc[0]
        ),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase81",
            generated_utc=generated_utc,
            inputs={
                "phase80_compact_daily_scenario_detail": str(phase80_dir / "compact_daily_scenario_detail.csv"),
                "dense_lake": str(dense_root),
            },
            parameters={
                "selection_policy": "one_source_day_per_regime_per_month_prefer_shock_then_rows_all_feed_profiles",
                "dense_control_symbol": control_symbol,
                "acceptance_gate": "all_months_capture_all_regimes_and_feeds_and_dense_control_symbol_verifies",
            },
            outputs={
                "selected_dates": str(output_dir / "stratified_selected_source_dates.csv"),
                "monthly_plan": str(output_dir / "stratified_window_monthly_plan.csv"),
                "reader_contract": str(output_dir / "stratified_dense_reader_contract.csv"),
                "dense_control": str(output_dir / "stratified_dense_control_verification.csv"),
                "acceptance_summary": str(output_dir / "stratified_dense_window_acceptance_summary.csv"),
                "report": str(output_dir / "phase81_stratified_dense_window_reader_report.md"),
                "manifest": str(output_dir / "phase81_stratified_dense_window_reader_manifest.json"),
            },
            random_seed="none_deterministic_stratified_window_selection",
            scenario_ids="phase81_source_day_regime_feed_balanced_dense_windows",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_reader_contract",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase81_stratified_dense_window_reader_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build stratified dense-window reader contract.")
    parser.add_argument("--phase80-dir", type=Path, default=DEFAULT_PHASE80_DIR)
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--control-symbol", type=str, default=DEFAULT_CONTROL_SYMBOL)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase81(args.phase80_dir, args.dense_root, args.output_dir, args.base_dir, args.control_symbol)


if __name__ == "__main__":
    main()

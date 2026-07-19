from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase56_cost_clearing_label_discovery import DEFAULT_DENSE_ROOT
from synthetic_l2.phase61_lower_frequency_candidate_sweep import _safe_path
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_OUTPUT_DIR = Path("outputs/phase75")
DEFAULT_TRADE_MONTH = "2026-01"
DEFAULT_TIME_BUCKET_SECONDS = 5_000
DEFAULT_STALENESS_LIMIT_SECONDS = 1_000


def monthly_files(dense_root: Path, trade_month: str) -> list[Path]:
    files = sorted((dense_root / f"trade_month={trade_month}").glob("symbol=*/part-00000.parquet"))
    if not files:
        raise FileNotFoundError(f"No dense parquet files for trade_month={trade_month} under {dense_root}")
    return files


def infer_timestamp_unit(median_positive_delta: float, min_timestamp: float) -> str:
    if median_positive_delta >= 500.0:
        return "milliseconds"
    if 0.5 <= median_positive_delta <= 10.0 and min_timestamp < 10_000_000_000:
        return "seconds_in_ms_named_column"
    if 0.0005 <= median_positive_delta < 0.5:
        return "subsecond_seconds"
    return "unknown"


def timestamp_contract(files: list[Path], max_rows_per_symbol: int | None) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    con = duckdb.connect()
    try:
        for path in files:
            filter_sql = "callback_received_utc_ms is not null"
            if max_rows_per_symbol is not None:
                filter_sql += f" and local_sequence_id <= {int(max_rows_per_symbol)}"
            sql = f"""
            with ordered as (
                select
                    any_value(trade_month) over ()::varchar as trade_month,
                    any_value(symbol) over ()::varchar as symbol,
                    local_sequence_id,
                    callback_received_utc_ms::double as ts_value,
                    callback_received_utc_ms::double - lag(callback_received_utc_ms::double) over (order by local_sequence_id) as delta_value
                from read_parquet('{_safe_path(path)}', union_by_name=true)
                where {filter_sql}
            ),
            positive_deltas as (
                select delta_value
                from ordered
                where delta_value > 0
            )
            select
                any_value(trade_month)::varchar as trade_month,
                any_value(symbol)::varchar as symbol,
                count(*)::bigint as rows_checked,
                min(ts_value)::double as min_timestamp_value,
                max(ts_value)::double as max_timestamp_value,
                min(delta_value)::double as min_delta_value,
                median(delta_value)::double as median_delta_value,
                median((select delta_value from positive_deltas limit 1))::double as unused_placeholder
            from ordered
            """
            stats = con.execute(sql).fetchdf().iloc[0].to_dict()
            pos = con.execute(
                f"""
                with ordered as (
                    select
                        callback_received_utc_ms::double - lag(callback_received_utc_ms::double) over (order by local_sequence_id) as delta_value
                    from read_parquet('{_safe_path(path)}', union_by_name=true)
                    where {filter_sql}
                )
                select
                    median(delta_value)::double as median_positive_delta_value,
                    quantile_cont(delta_value, 0.01)::double as p01_positive_delta_value,
                    quantile_cont(delta_value, 0.99)::double as p99_positive_delta_value,
                    count(*)::bigint as positive_delta_count
                from ordered
                where delta_value > 0
                """
            ).fetchdf().iloc[0].to_dict()
            stats.update(pos)
            stats["inferred_timestamp_unit"] = infer_timestamp_unit(
                float(stats.get("median_positive_delta_value") or 0.0),
                float(stats.get("min_timestamp_value") or 0.0),
            )
            stats["source_path"] = str(path)
            rows.append(stats)
    finally:
        con.close()
    frame = pd.DataFrame(rows)
    frame["unit_contract_pass"] = frame["inferred_timestamp_unit"].eq(frame["inferred_timestamp_unit"].mode().iloc[0])
    return frame.drop(columns=["unused_placeholder"], errors="ignore")


def unit_contract_summary(contract: pd.DataFrame) -> pd.DataFrame:
    if contract.empty:
        return pd.DataFrame()
    mode_unit = str(contract["inferred_timestamp_unit"].mode().iloc[0])
    return pd.DataFrame(
        [
            {
                "contract_id": "P75_timestamp_unit_contract",
                "partitions_checked": int(len(contract)),
                "symbols_checked": int(contract["symbol"].nunique()),
                "mode_inferred_timestamp_unit": mode_unit,
                "mismatched_unit_partitions": int((~contract["unit_contract_pass"]).sum()),
                "median_positive_delta_min": float(contract["median_positive_delta_value"].min()),
                "median_positive_delta_max": float(contract["median_positive_delta_value"].max()),
                "timestamp_contract_pass": bool((contract["unit_contract_pass"]).all() and mode_unit != "unknown"),
            }
        ]
    )


def query_global_timestamp_bars(
    path: Path,
    timestamp_unit: str,
    time_bucket_seconds: int,
    max_rows_per_symbol: int | None,
) -> pd.DataFrame:
    filter_sql = """
        callback_received_utc_ms is not null
        and buy_1_price > 0
        and sell_1_price > 0
        and sell_1_price >= buy_1_price
        and not coalesce(is_duplicate, false)
        and not coalesce(is_disconnect_gap, false)
        and not coalesce(is_out_of_order_injected, false)
    """
    if max_rows_per_symbol is not None:
        filter_sql += f" and local_sequence_id <= {int(max_rows_per_symbol)}"
    ts_expr = "callback_received_utc_ms / 1000.0" if timestamp_unit == "milliseconds" else "callback_received_utc_ms"
    con = duckdb.connect()
    try:
        sql = f"""
        with base as (
            select
                trade_date,
                trade_month,
                symbol,
                local_sequence_id,
                ({ts_expr})::double as timestamp_seconds,
                floor(({ts_expr}) / {int(time_bucket_seconds)})::bigint as global_time_bucket_id,
                ((buy_1_price + sell_1_price) / 2.0)::double as mid_price,
                greatest(sell_1_price - buy_1_price, 0.01)::double as spread,
                ((buy_1_quantity - sell_1_quantity) / nullif((buy_1_quantity + sell_1_quantity), 0.0))::double as l1_imbalance
            from read_parquet('{_safe_path(path)}', union_by_name=true)
            where {filter_sql}
        )
        select
            trade_date,
            trade_month,
            symbol,
            {int(time_bucket_seconds)}::integer as time_bucket_seconds,
            global_time_bucket_id,
            count(*)::bigint as rows_in_bucket,
            min(timestamp_seconds)::double as first_timestamp_seconds,
            max(timestamp_seconds)::double as last_timestamp_seconds,
            first(mid_price order by local_sequence_id)::double as open_mid_price,
            last(mid_price order by local_sequence_id)::double as close_mid_price,
            avg(spread)::double as avg_spread,
            avg(l1_imbalance)::double as avg_l1_imbalance
        from base
        group by trade_date, trade_month, symbol, global_time_bucket_id
        having count(*) >= 10
        """
        return con.execute(sql).fetchdf()
    finally:
        con.close()


def build_synchronous_matrix(
    files: list[Path],
    timestamp_unit: str,
    time_bucket_seconds: int,
    staleness_limit_seconds: int,
    max_rows_per_symbol: int | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    frames = [query_global_timestamp_bars(path, timestamp_unit, time_bucket_seconds, max_rows_per_symbol) for path in files]
    matrix = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if matrix.empty:
        return matrix, pd.DataFrame()
    matrix["bucket_end_seconds"] = (matrix["global_time_bucket_id"].astype(float) + 1.0) * float(time_bucket_seconds)
    matrix["staleness_seconds"] = matrix["bucket_end_seconds"] - matrix["last_timestamp_seconds"].astype(float)
    matrix["fresh_cell"] = matrix["staleness_seconds"].le(float(staleness_limit_seconds))
    matrix["bar_return"] = matrix["close_mid_price"] / matrix["open_mid_price"].replace(0, np.nan) - 1.0
    total_symbols = int(matrix["symbol"].nunique())
    coverage = (
        matrix.groupby(["trade_date", "global_time_bucket_id"], sort=True)
        .agg(
            symbols_present=("symbol", "nunique"),
            fresh_symbols=("fresh_cell", "sum"),
            total_rows=("rows_in_bucket", "sum"),
            min_first_timestamp_seconds=("first_timestamp_seconds", "min"),
            max_last_timestamp_seconds=("last_timestamp_seconds", "max"),
            max_staleness_seconds=("staleness_seconds", "max"),
            median_staleness_seconds=("staleness_seconds", "median"),
        )
        .reset_index()
    )
    coverage["expected_symbols"] = total_symbols
    coverage["coverage_fraction"] = coverage["symbols_present"] / float(total_symbols or 1)
    coverage["fresh_fraction"] = coverage["fresh_symbols"] / float(total_symbols or 1)
    coverage["coverage_pass"] = coverage["coverage_fraction"].ge(0.95) & coverage["fresh_fraction"].ge(0.95)
    return matrix, coverage


def summarize(
    contract_summary: pd.DataFrame,
    matrix: pd.DataFrame,
    coverage: pd.DataFrame,
    elapsed_seconds: float,
) -> pd.DataFrame:
    timestamp_pass = bool(contract_summary.iloc[0]["timestamp_contract_pass"]) if not contract_summary.empty else False
    coverage_pass_fraction = float(coverage["coverage_pass"].mean()) if not coverage.empty else 0.0
    fresh_cell_fraction = float(matrix["fresh_cell"].mean()) if not matrix.empty and "fresh_cell" in matrix else 0.0
    validator_pass = bool(timestamp_pass and coverage_pass_fraction >= 0.95 and fresh_cell_fraction >= 0.95)
    return pd.DataFrame(
        [
            ("phase75_timestamp_contract_pass", int(timestamp_pass), "1 means timestamp unit inferred consistently and not unknown"),
            ("phase75_matrix_bar_rows", int(len(matrix)), "Synchronous timestamp-bar matrix rows"),
            ("phase75_coverage_bucket_rows", int(len(coverage)), "Global timestamp buckets audited"),
            ("phase75_coverage_pass_fraction", coverage_pass_fraction, "Fraction of buckets passing symbol coverage and freshness"),
            ("phase75_fresh_cell_fraction", fresh_cell_fraction, "Fraction of symbol/bucket matrix cells within staleness limit"),
            ("phase75_synchronous_matrix_validator_pass", int(validator_pass), "1 means Phase74 alignment remediation gate passes"),
            ("phase75_elapsed_seconds", elapsed_seconds, "Elapsed seconds"),
            (
                "phase75_recommend_next_action",
                "hdfcbank_timestamp_refinement_retest" if validator_pass else "fix_synchronous_matrix_coverage_or_staleness",
                "Recommended next action",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase75 Timestamp Contract and Synchronous Matrix Validator",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase75 implements the first Phase74 remediation gate.",
        "It infers the timestamp unit per symbol partition and validates a global-clock cross-symbol matrix with coverage and staleness diagnostics.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase75_timestamp_contract_matrix_validator_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase75(
    dense_root: Path,
    output_dir: Path,
    base_dir: Path,
    trade_month: str,
    time_bucket_seconds: int,
    staleness_limit_seconds: int,
    max_rows_per_symbol: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    files = monthly_files(dense_root, trade_month)
    contract = timestamp_contract(files, max_rows_per_symbol)
    contract_summary = unit_contract_summary(contract)
    timestamp_unit = str(contract_summary.iloc[0]["mode_inferred_timestamp_unit"]) if not contract_summary.empty else "unknown"
    matrix, coverage = build_synchronous_matrix(files, timestamp_unit, time_bucket_seconds, staleness_limit_seconds, max_rows_per_symbol)
    elapsed = time.perf_counter() - started
    acceptance = summarize(contract_summary, matrix, coverage, elapsed)
    inventory = pd.DataFrame([{"symbol": path.parent.name.replace("symbol=", ""), "shard_path": str(path)} for path in files])

    inventory.to_csv(output_dir / "timestamp_validator_file_inventory.csv", index=False)
    contract.to_csv(output_dir / "timestamp_unit_contract_detail.csv", index=False)
    contract_summary.to_csv(output_dir / "timestamp_unit_contract_summary.csv", index=False)
    matrix.to_csv(output_dir / "synchronous_timestamp_matrix.csv", index=False)
    coverage.to_csv(output_dir / "synchronous_matrix_coverage.csv", index=False)
    acceptance.to_csv(output_dir / "timestamp_contract_matrix_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Timestamp Unit Contract Summary": contract_summary,
            "Synchronous Matrix Coverage": coverage,
            "Timestamp Unit Contract Detail": contract,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase75_timestamp_contract_matrix_validator",
        "validator_pass": int(acceptance.loc[acceptance["metric"].eq("phase75_synchronous_matrix_validator_pass"), "value"].iloc[0]),
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase75",
            generated_utc=generated_utc,
            inputs={
                "phase51_dense_lake": str(dense_root),
                "phase74_remediation_plan": "outputs/phase74/remediation_action_plan.csv",
            },
            parameters={
                "trade_month": trade_month,
                "time_bucket_seconds": time_bucket_seconds,
                "staleness_limit_seconds": staleness_limit_seconds,
                "max_rows_per_symbol": max_rows_per_symbol if max_rows_per_symbol is not None else "none_full_symbol_scan",
                "validator_gate": "consistent_timestamp_unit_and_coverage_pass_fraction_ge_0_95_and_fresh_cell_fraction_ge_0_95",
            },
            outputs={
                "file_inventory": str(output_dir / "timestamp_validator_file_inventory.csv"),
                "timestamp_unit_contract_detail": str(output_dir / "timestamp_unit_contract_detail.csv"),
                "timestamp_unit_contract_summary": str(output_dir / "timestamp_unit_contract_summary.csv"),
                "synchronous_timestamp_matrix": str(output_dir / "synchronous_timestamp_matrix.csv"),
                "synchronous_matrix_coverage": str(output_dir / "synchronous_matrix_coverage.csv"),
                "acceptance_summary": str(output_dir / "timestamp_contract_matrix_acceptance_summary.csv"),
                "report": str(output_dir / "phase75_timestamp_contract_matrix_validator_report.md"),
                "manifest": str(output_dir / "phase75_timestamp_contract_matrix_validator_manifest.json"),
            },
            random_seed="none_deterministic_timestamp_validator",
            scenario_ids="phase75_timestamp_contract_synchronous_matrix",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="phase75_global_clock_timestamp_bucket_alignment",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase75_timestamp_contract_matrix_validator_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate timestamp unit contract and synchronous cross-symbol matrix coverage.")
    parser.add_argument("--dense-root", type=Path, default=DEFAULT_DENSE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--trade-month", type=str, default=DEFAULT_TRADE_MONTH)
    parser.add_argument("--time-bucket-seconds", type=int, default=DEFAULT_TIME_BUCKET_SECONDS)
    parser.add_argument("--staleness-limit-seconds", type=int, default=DEFAULT_STALENESS_LIMIT_SECONDS)
    parser.add_argument("--max-rows-per-symbol", type=int, default=250_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase75(
        args.dense_root,
        args.output_dir,
        args.base_dir,
        args.trade_month,
        args.time_bucket_seconds,
        args.staleness_limit_seconds,
        args.max_rows_per_symbol,
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase95_real_anchor_panel_contract import EXPECTED_SYMBOLS
from synthetic_l2.phase96_real_anchor_panel_builder import REQUIRED_ZERODHA_L2_COLUMNS
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_ROOTS = [Path("scratch_azcopy_selected/raw_l2"), Path("real_data_sample/l2_multiday_panel")]
DEFAULT_OUTPUT_DIR = Path("outputs/phase142")
DEFAULT_EXCHANGE = "NSE"


def infer_part(path: Path, prefix: str) -> str:
    for part in path.parts:
        if part.startswith(prefix + "="):
            return part.split("=", 1)[1]
    return ""


def select_sample_files(files: list[Path]) -> list[Path]:
    if not files:
        return []
    if len(files) == 1:
        return [files[0]]
    return [files[0], files[-1]]


def discover_symbol_partitions(roots: list[Path], default_exchange: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for root in roots:
        if not root.exists():
            rows.append(
                {
                    "root": str(root),
                    "trade_date": "",
                    "exchange": default_exchange,
                    "symbol": "",
                    "symbol_dir": "",
                    "parquet_files": 0,
                    "bytes": 0,
                    "first_file": "",
                    "last_file": "",
                    "discovery_status": "missing_root",
                }
            )
            continue
        symbol_dirs = sorted(path for path in root.rglob("symbol=*") if path.is_dir())
        for symbol_dir in symbol_dirs:
            files = sorted(symbol_dir.glob("*.parquet"))
            rows.append(
                {
                    "root": str(root),
                    "trade_date": infer_part(symbol_dir, "trade_date"),
                    "exchange": infer_part(symbol_dir, "exchange") or default_exchange,
                    "symbol": symbol_dir.name.split("=", 1)[1],
                    "symbol_dir": str(symbol_dir),
                    "parquet_files": int(len(files)),
                    "bytes": int(sum(path.stat().st_size for path in files)),
                    "first_file": str(files[0]) if files else "",
                    "last_file": str(files[-1]) if files else "",
                    "discovery_status": "ok",
                }
            )
    return pd.DataFrame(rows)


def sample_schema_and_book(symbol_inventory: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in symbol_inventory.to_dict("records"):
        symbol_dir = Path(str(item.get("symbol_dir", "")))
        files = sorted(symbol_dir.glob("*.parquet")) if symbol_dir.exists() else []
        for path in select_sample_files(files):
            try:
                frame = pd.read_parquet(path)
                missing = sorted(set(REQUIRED_ZERODHA_L2_COLUMNS).difference(frame.columns))
                if {"buy_1_price", "sell_1_price"}.issubset(frame.columns) and not frame.empty:
                    buy_1 = pd.to_numeric(frame["buy_1_price"], errors="coerce")
                    sell_1 = pd.to_numeric(frame["sell_1_price"], errors="coerce")
                    l1_valid = bool(((buy_1 > 0) & (sell_1 > 0) & (sell_1 >= buy_1)).mean() >= 0.99)
                else:
                    l1_valid = False
                observed_trade_dates = (
                    "|".join(sorted(frame["trade_date"].dropna().astype(str).unique().tolist()))
                    if "trade_date" in frame.columns
                    else ""
                )
                observed_symbols = (
                    "|".join(sorted(frame["tradingsymbol"].dropna().astype(str).unique().tolist()))
                    if "tradingsymbol" in frame.columns
                    else ""
                )
                rows.append(
                    {
                        "root": item["root"],
                        "trade_date": item["trade_date"],
                        "exchange": item["exchange"],
                        "symbol": item["symbol"],
                        "file": str(path),
                        "rows": int(len(frame)),
                        "column_count": int(len(frame.columns)),
                        "missing_required_columns": "|".join(missing),
                        "required_schema_pass": bool(not missing),
                        "l1_book_sample_pass": l1_valid,
                        "observed_trade_dates": observed_trade_dates,
                        "observed_symbols": observed_symbols,
                        "sample_status": "ok",
                        "sample_error": "",
                    }
                )
            except Exception as exc:
                rows.append(
                    {
                        "root": item["root"],
                        "trade_date": item["trade_date"],
                        "exchange": item["exchange"],
                        "symbol": item["symbol"],
                        "file": str(path),
                        "rows": 0,
                        "column_count": 0,
                        "missing_required_columns": "",
                        "required_schema_pass": False,
                        "l1_book_sample_pass": False,
                        "observed_trade_dates": "",
                        "observed_symbols": "",
                        "sample_status": "failed",
                        "sample_error": repr(exc),
                    }
                )
    return pd.DataFrame(rows)


def build_date_readiness(symbol_inventory: pd.DataFrame, sample_checks: pd.DataFrame) -> pd.DataFrame:
    if symbol_inventory.empty:
        return pd.DataFrame()
    check_group = (
        sample_checks.groupby(["root", "trade_date", "exchange", "symbol"], sort=True)
        .agg(
            sample_files=("file", "count"),
            schema_pass=("required_schema_pass", "min"),
            l1_book_sample_pass=("l1_book_sample_pass", "min"),
            sample_failed=("sample_status", lambda values: int((values.astype(str) != "ok").sum())),
        )
        .reset_index()
        if not sample_checks.empty
        else pd.DataFrame(columns=["root", "trade_date", "exchange", "symbol", "sample_files", "schema_pass", "l1_book_sample_pass", "sample_failed"])
    )
    merged = symbol_inventory.merge(check_group, on=["root", "trade_date", "exchange", "symbol"], how="left")
    rows: list[dict[str, Any]] = []
    valid = merged[merged["discovery_status"].astype(str).eq("ok")]
    for (root, trade_date, exchange), group in valid.groupby(["root", "trade_date", "exchange"], sort=True):
        symbols = set(group["symbol"].dropna().astype(str))
        expected_symbols_with_files = set(group.loc[group["parquet_files"].astype(int).gt(0), "symbol"].dropna().astype(str)).intersection(EXPECTED_SYMBOLS)
        missing_expected = sorted(EXPECTED_SYMBOLS.difference(expected_symbols_with_files))
        schema_pass = bool(group["schema_pass"].fillna(False).astype(bool).all()) if not group.empty else False
        l1_pass = bool(group["l1_book_sample_pass"].fillna(False).astype(bool).all()) if not group.empty else False
        sample_failed = int(pd.to_numeric(group["sample_failed"], errors="coerce").fillna(0).sum())
        expected_fraction = len(expected_symbols_with_files) / len(EXPECTED_SYMBOLS)
        rows.append(
            {
                "root": root,
                "trade_date": trade_date,
                "exchange": exchange,
                "symbol_directories": int(len(symbols)),
                "expected_symbols_with_files": int(len(expected_symbols_with_files)),
                "expected_symbol_fraction": float(expected_fraction),
                "missing_expected_symbols": "|".join(missing_expected),
                "parquet_files": int(group["parquet_files"].sum()),
                "bytes": int(group["bytes"].sum()),
                "schema_sample_pass": schema_pass,
                "l1_book_sample_pass": l1_pass,
                "sample_failed_files": sample_failed,
                "ready_for_phase115_import": bool(expected_fraction >= 0.95 and schema_pass and sample_failed == 0),
            }
        )
    return pd.DataFrame(rows)


def summarize(symbol_inventory: pd.DataFrame, sample_checks: pd.DataFrame, date_readiness: pd.DataFrame) -> pd.DataFrame:
    ready = date_readiness[date_readiness["ready_for_phase115_import"].astype(bool)] if not date_readiness.empty else pd.DataFrame()
    roots_ready = (
        ready.groupby("root")["trade_date"].nunique().reset_index(name="ready_dates")
        if not ready.empty
        else pd.DataFrame(columns=["root", "ready_dates"])
    )
    max_ready_dates = int(roots_ready["ready_dates"].max()) if not roots_ready.empty else 0
    return pd.DataFrame(
        [
            ("phase142_roots_checked", int(symbol_inventory["root"].nunique()) if not symbol_inventory.empty else 0, "Distinct local roots inspected"),
            ("phase142_symbol_partition_rows", int(len(symbol_inventory)), "Symbol partition rows discovered"),
            ("phase142_sample_files_checked", int(len(sample_checks)), "First/last parquet samples read for schema and L1 book checks"),
            ("phase142_date_rows", int(len(date_readiness)), "Root/date readiness rows emitted"),
            ("phase142_ready_date_rows", int(len(ready)), "Root/date rows ready for Phase115 import"),
            ("phase142_max_ready_dates_in_one_root", max_ready_dates, "Maximum ready dates in any one checked root"),
            ("phase142_total_parquet_files", int(symbol_inventory["parquet_files"].sum()) if not symbol_inventory.empty else 0, "Total parquet files across checked roots"),
            ("phase142_total_bytes", int(symbol_inventory["bytes"].sum()) if not symbol_inventory.empty else 0, "Total bytes across checked roots"),
            ("phase142_strategy_replay_allowed", 0, "Local download verification does not unlock strategy replay"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase142 Local Real L2 Download Verifier",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase142 verifies local AzCopy/downloaded real Zerodha WebSocket top-five market-by-price partitions before or after Phase115 import.",
        "It checks date/symbol coverage, parquet counts/bytes, sampled required schema, and sampled L1 book sanity.",
        "Phase142 readiness is intentionally an import/download readiness flag: L1 book sample status is diagnostic here; Phase96 remains the authoritative real-anchor market-quality gate.",
        "It does not contact Azure and does not unlock strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase142_local_real_l2_download_verifier_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase142(roots: list[Path], output_dir: Path, base_dir: Path, default_exchange: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    symbol_inventory = discover_symbol_partitions(roots, default_exchange)
    sample_checks = sample_schema_and_book(symbol_inventory)
    date_readiness = build_date_readiness(symbol_inventory, sample_checks)
    acceptance = summarize(symbol_inventory, sample_checks, date_readiness)

    symbol_inventory.to_csv(output_dir / "local_real_l2_symbol_inventory.csv", index=False)
    sample_checks.to_csv(output_dir / "local_real_l2_sample_schema_checks.csv", index=False)
    date_readiness.to_csv(output_dir / "local_real_l2_date_readiness.csv", index=False)
    acceptance.to_csv(output_dir / "phase142_local_real_l2_download_verifier_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Date Readiness": date_readiness,
            "Sample Schema Checks": sample_checks.head(60),
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase142_local_real_l2_download_verifier",
        **reproducibility_fields(
            artifact_id="phase142",
            generated_utc=generated_utc,
            inputs={"roots": [str(path) for path in roots]},
            parameters={
                "default_exchange": default_exchange,
                "minimum_expected_symbol_fraction": 0.95,
                "sample_policy": "first_and_last_parquet_per_symbol_partition",
                "readiness_policy": "coverage_schema_and_readable_samples; l1_book_sample_pass_is_diagnostic_not_blocking",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "symbol_inventory": str(output_dir / "local_real_l2_symbol_inventory.csv"),
                "sample_schema_checks": str(output_dir / "local_real_l2_sample_schema_checks.csv"),
                "date_readiness": str(output_dir / "local_real_l2_date_readiness.csv"),
                "acceptance_summary": str(output_dir / "phase142_local_real_l2_download_verifier_acceptance_summary.csv"),
                "report": str(output_dir / "phase142_local_real_l2_download_verifier_report.md"),
                "manifest": str(output_dir / "phase142_local_real_l2_download_verifier_manifest.json"),
            },
            random_seed="none_deterministic_local_verifier",
            scenario_ids="phase142_local_real_l2_download_verifier",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase142_local_real_l2_download_verifier_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify local real L2 downloaded/imported date partitions.")
    parser.add_argument("--roots", nargs="+", type=Path, default=DEFAULT_ROOTS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--default-exchange", default=DEFAULT_EXCHANGE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase142(args.roots, args.output_dir, args.base_dir, args.default_exchange)


if __name__ == "__main__":
    main()

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


DEFAULT_OUTPUT_DIR = Path("outputs/phase147")
DEFAULT_SCRATCH_ROOT = Path("scratch_azcopy_selected/raw_l2")
DEFAULT_TARGET_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_REQUIRED_DATES = ["2026-07-10", "2026-07-14"]
DEFAULT_EXCHANGE = "NSE"


def date_root(root: Path, trade_date: str) -> Path:
    return root / f"trade_date={trade_date}"


def symbol_dir(root: Path, trade_date: str, exchange: str, symbol: str) -> Path:
    return date_root(root, trade_date) / f"exchange={exchange}" / f"symbol={symbol}"


def count_nested_date_parts(path: Path) -> int:
    return sum(1 for part in path.parts if part.startswith("trade_date="))


def sample_files(files: list[Path]) -> list[Path]:
    if not files:
        return []
    if len(files) == 1:
        return [files[0]]
    return [files[0], files[-1]]


def inspect_file(path: Path) -> dict[str, Any]:
    try:
        frame = pd.read_parquet(path)
        missing = sorted(set(REQUIRED_ZERODHA_L2_COLUMNS).difference(frame.columns))
        trade_dates = "|".join(sorted(frame["trade_date"].dropna().astype(str).unique().tolist())) if "trade_date" in frame.columns else ""
        symbols = "|".join(sorted(frame["tradingsymbol"].dropna().astype(str).unique().tolist())) if "tradingsymbol" in frame.columns else ""
        return {
            "file": str(path),
            "rows": int(len(frame)),
            "column_count": int(len(frame.columns)),
            "required_schema_pass": bool(not missing),
            "missing_required_columns": "|".join(missing),
            "observed_trade_dates": trade_dates,
            "observed_symbols": symbols,
            "read_status": "ok",
            "read_error": "",
        }
    except Exception as exc:
        return {
            "file": str(path),
            "rows": 0,
            "column_count": 0,
            "required_schema_pass": False,
            "missing_required_columns": "",
            "observed_trade_dates": "",
            "observed_symbols": "",
            "read_status": "failed",
            "read_error": repr(exc),
        }


def inspect_symbol_partition(root: Path, trade_date: str, exchange: str, symbol: str, location: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    direct_dir = symbol_dir(root, trade_date, exchange, symbol)
    nested_dirs = sorted(path for path in date_root(root, trade_date).rglob(f"symbol={symbol}") if path.is_dir()) if date_root(root, trade_date).exists() else []
    selected_dir = direct_dir if direct_dir.exists() else (nested_dirs[0] if nested_dirs else direct_dir)
    files = sorted(selected_dir.glob("*.parquet")) if selected_dir.exists() else []
    samples = []
    for path in sample_files(files):
        sample = inspect_file(path)
        sample.update({"location": location, "trade_date": trade_date, "exchange": exchange, "symbol": symbol})
        samples.append(sample)
    row = {
        "location": location,
        "root": str(root),
        "trade_date": trade_date,
        "exchange": exchange,
        "symbol": symbol,
        "symbol_dir": str(selected_dir),
        "direct_canonical_dir_exists": direct_dir.exists(),
        "symbol_dir_exists": selected_dir.exists(),
        "nested_trade_date_layout": bool(selected_dir.exists() and count_nested_date_parts(selected_dir) > 1),
        "parquet_files": int(len(files)),
        "bytes": int(sum(path.stat().st_size for path in files)),
        "first_file": str(files[0]) if files else "",
        "last_file": str(files[-1]) if files else "",
        "sample_files_checked": int(len(samples)),
        "sample_schema_pass": bool(samples and all(bool(item["required_schema_pass"]) for item in samples)),
        "sample_failed_files": int(sum(1 for item in samples if item["read_status"] != "ok")),
    }
    return row, samples


def build_intake(
    scratch_root: Path,
    target_root: Path,
    required_dates: list[str],
    exchange: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    partition_rows: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    date_rows: list[dict[str, Any]] = []
    for trade_date in required_dates:
        for location, root in [("scratch", scratch_root), ("target", target_root)]:
            rows_for_date: list[dict[str, Any]] = []
            for symbol in EXPECTED_SYMBOLS:
                row, samples = inspect_symbol_partition(root, trade_date, exchange, symbol, location)
                rows_for_date.append(row)
                partition_rows.append(row)
                sample_rows.extend(samples)
            frame = pd.DataFrame(rows_for_date)
            symbols_with_files = int(frame["parquet_files"].astype(int).gt(0).sum())
            canonical_symbols = int(frame["direct_canonical_dir_exists"].astype(bool).sum())
            nested_symbols = int(frame["nested_trade_date_layout"].astype(bool).sum())
            sample_failures = int(frame["sample_failed_files"].astype(int).sum())
            schema_symbols_pass = int(frame["sample_schema_pass"].astype(bool).sum())
            missing_symbols = sorted(frame.loc[frame["parquet_files"].astype(int).eq(0), "symbol"].astype(str).tolist())
            date_exists = date_root(root, trade_date).exists()
            complete = bool(symbols_with_files == len(EXPECTED_SYMBOLS) and sample_failures == 0 and schema_symbols_pass == symbols_with_files)
            clean_canonical = bool(complete and canonical_symbols == len(EXPECTED_SYMBOLS) and nested_symbols == 0)
            date_rows.append(
                {
                    "location": location,
                    "root": str(root),
                    "trade_date": trade_date,
                    "exchange": exchange,
                    "date_root_exists": date_exists,
                    "expected_symbols": len(EXPECTED_SYMBOLS),
                    "symbols_with_files": symbols_with_files,
                    "canonical_symbol_dirs": canonical_symbols,
                    "nested_trade_date_symbol_dirs": nested_symbols,
                    "parquet_files": int(frame["parquet_files"].astype(int).sum()),
                    "bytes": int(frame["bytes"].astype(int).sum()),
                    "sample_files_checked": int(frame["sample_files_checked"].astype(int).sum()),
                    "sample_failed_files": sample_failures,
                    "schema_symbols_pass": schema_symbols_pass,
                    "missing_symbols": "|".join(missing_symbols),
                    "date_complete_for_phase145": complete,
                    "date_clean_canonical_layout": clean_canonical,
                }
            )
    return pd.DataFrame(date_rows), pd.DataFrame(partition_rows), pd.DataFrame(sample_rows)


def summarize(date_intake: pd.DataFrame, required_dates: list[str]) -> pd.DataFrame:
    scratch = date_intake[date_intake["location"].astype(str).eq("scratch")] if not date_intake.empty else pd.DataFrame()
    target = date_intake[date_intake["location"].astype(str).eq("target")] if not date_intake.empty else pd.DataFrame()
    scratch_complete = int(scratch["date_complete_for_phase145"].astype(bool).sum()) if not scratch.empty else 0
    target_complete = int(target["date_complete_for_phase145"].astype(bool).sum()) if not target.empty else 0
    required_satisfied = 0
    ready_for_import = 0
    already_target = 0
    for trade_date in required_dates:
        srow = scratch[scratch["trade_date"].astype(str).eq(trade_date)] if not scratch.empty else pd.DataFrame()
        trow = target[target["trade_date"].astype(str).eq(trade_date)] if not target.empty else pd.DataFrame()
        sready = bool(not srow.empty and srow["date_complete_for_phase145"].astype(bool).any())
        tready = bool(not trow.empty and trow["date_complete_for_phase145"].astype(bool).any())
        required_satisfied += int(sready or tready)
        ready_for_import += int(sready and not tready)
        already_target += int(tready)
    nested_rows = int(date_intake["nested_trade_date_symbol_dirs"].astype(int).sum()) if not date_intake.empty else 0
    can_run_phase145 = bool(ready_for_import > 0)
    next_action = (
        "run_phase145_post_download_refresh_then_phase146_minimum_unlock_audit"
        if can_run_phase145
        else "download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase147"
    )
    return pd.DataFrame(
        [
            ("phase147_required_date_rows", len(required_dates), "Required dates checked in scratch and target"),
            ("phase147_required_dates_satisfied", required_satisfied, "Required dates complete in scratch or target"),
            ("phase147_required_dates_ready_for_import", ready_for_import, "Required dates complete in scratch but not target"),
            ("phase147_required_dates_already_in_target", already_target, "Required dates complete in canonical target"),
            ("phase147_scratch_complete_dates", scratch_complete, "Scratch required dates complete for Phase145"),
            ("phase147_target_complete_dates", target_complete, "Target required dates already complete"),
            ("phase147_nested_trade_date_symbol_dirs", nested_rows, "Nested duplicate trade_date symbol dirs across checked roots"),
            ("phase147_can_run_phase145_now", int(can_run_phase145), "1 means Phase145 should be run now"),
            ("phase147_strategy_replay_allowed", 0, "Download intake never unlocks strategy replay"),
            ("phase147_next_best_action", next_action, "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase147 AzCopy Download Intake Audit",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase147 validates local AzCopy landing-zone contents for configured required real L2 dates before Phase145 import/refresh is attempted.",
        "It is local-only: AzCopy owns Azure I/O; Python only inspects downloaded Parquet partitions.",
        "It checks complete 32-symbol coverage, sampled Zerodha top-five market-by-price schema, bytes/files, target-vs-scratch state, and duplicate nested `trade_date` layouts.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase147_azcopy_download_intake_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase147(
    output_dir: Path,
    base_dir: Path,
    scratch_root: Path,
    target_root: Path,
    required_dates: list[str],
    exchange: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    date_intake, symbol_intake, sample_checks = build_intake(scratch_root, target_root, required_dates, exchange)
    acceptance = summarize(date_intake, required_dates)
    date_intake.to_csv(output_dir / "phase147_date_intake.csv", index=False)
    symbol_intake.to_csv(output_dir / "phase147_symbol_intake.csv", index=False)
    sample_checks.to_csv(output_dir / "phase147_sample_schema_checks.csv", index=False)
    acceptance.to_csv(output_dir / "phase147_azcopy_download_intake_audit_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Date Intake": date_intake,
            "Sample Schema Checks": sample_checks.head(80),
        },
    )
    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase147_azcopy_download_intake_audit",
        **reproducibility_fields(
            artifact_id="phase147",
            generated_utc=generated_utc,
            inputs={
                "scratch_root": str(scratch_root),
                "target_root": str(target_root),
                "required_dates": required_dates,
            },
            parameters={
                "exchange": exchange,
                "expected_symbols": len(EXPECTED_SYMBOLS),
                "sample_policy": "first_and_last_parquet_per_symbol_partition",
                "azure_io_policy": "azcopy_only; python_local_validation_only",
                "strategy_replay_policy": "closed",
            },
            outputs={
                "date_intake": str(output_dir / "phase147_date_intake.csv"),
                "symbol_intake": str(output_dir / "phase147_symbol_intake.csv"),
                "sample_schema_checks": str(output_dir / "phase147_sample_schema_checks.csv"),
                "acceptance_summary": str(output_dir / "phase147_azcopy_download_intake_audit_acceptance_summary.csv"),
                "report": str(output_dir / "phase147_azcopy_download_intake_audit_report.md"),
                "manifest": str(output_dir / "phase147_azcopy_download_intake_audit_manifest.json"),
            },
            random_seed="none_deterministic_local_intake",
            scenario_ids="phase147_azcopy_download_intake_audit",
            cost_model_version="not_applicable",
            latency_model_version="not_applicable",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase147_azcopy_download_intake_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit local AzCopy landing-zone dates before Phase145 import.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--scratch-root", type=Path, default=DEFAULT_SCRATCH_ROOT)
    parser.add_argument("--target-root", type=Path, default=DEFAULT_TARGET_ROOT)
    parser.add_argument("--required-dates", nargs="+", default=DEFAULT_REQUIRED_DATES)
    parser.add_argument("--exchange", default=DEFAULT_EXCHANGE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase147(
        output_dir=args.output_dir,
        base_dir=args.base_dir,
        scratch_root=args.scratch_root,
        target_root=args.target_root,
        required_dates=args.required_dates,
        exchange=args.exchange,
    )


if __name__ == "__main__":
    main()

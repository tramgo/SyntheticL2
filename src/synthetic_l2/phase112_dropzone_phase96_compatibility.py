from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase96_real_anchor_panel_builder import (
    REQUIRED_ZERODHA_L2_COLUMNS,
    build_day_readiness,
    discover_symbol_files,
    sampled_symbol_day_diagnostics,
)
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase112")
DEFAULT_FIXTURE_ROOT = Path(".tmp/phase112_dropzone_fixture")
FIXTURE_SYMBOLS = ["HDFCBANK", "INFY"]
FIXTURE_TRADE_DATE = "2026-07-20"


def build_fixture_row(symbol: str, ts_ms: int, index: int) -> dict[str, Any]:
    row: dict[str, Any] = {
        "collector_received_utc": "2026-07-20T03:45:00Z",
        "collector_received_utc_ms": ts_ms,
        "collector_received_monotonic_ns": ts_ms * 1_000_000,
        "exchange_timestamp": "2026-07-20T03:44:59Z",
        "last_trade_time": "2026-07-20T03:44:59Z",
        "trade_date": FIXTURE_TRADE_DATE,
        "exchange": "NSE",
        "tradingsymbol": symbol,
        "requested_symbol": symbol,
        "instrument_token": 10_000 + index,
        "last_price": 100.0 + index,
        "last_traded_quantity": 10 + index,
        "volume_traded": 1000 + index,
        "average_traded_price": 100.0 + index,
        "total_buy_quantity": 100,
        "total_sell_quantity": 120,
    }
    for level in range(1, 6):
        row[f"buy_{level}_price"] = 100.0 - level * 0.05
        row[f"buy_{level}_quantity"] = 100 + level
        row[f"buy_{level}_orders"] = 1
        row[f"sell_{level}_price"] = 100.0 + level * 0.05
        row[f"sell_{level}_quantity"] = 120 + level
        row[f"sell_{level}_orders"] = 1
    return row


def create_dropzone_fixture(fixture_root: Path) -> None:
    if fixture_root.exists():
        shutil.rmtree(fixture_root)
    for symbol_index, symbol in enumerate(FIXTURE_SYMBOLS):
        target = fixture_root / "l2_multiday_panel" / f"trade_date={FIXTURE_TRADE_DATE}" / "exchange=NSE" / f"symbol={symbol}"
        target.mkdir(parents=True, exist_ok=True)
        frame = pd.DataFrame([build_fixture_row(symbol, 1_785_000_000_000 + i * 500, symbol_index) for i in range(3)])
        frame = frame[REQUIRED_ZERODHA_L2_COLUMNS]
        frame.to_parquet(target / "part-00000.parquet", index=False)


def build_checks(symbol_files: pd.DataFrame, symbol_day: pd.DataFrame, schema: pd.DataFrame, day_readiness: pd.DataFrame) -> pd.DataFrame:
    required_schema_pass = bool(not schema.empty and schema["required_schema_pass"].astype(bool).all())
    nested_dates = set(symbol_files.get("inferred_trade_date", pd.Series(dtype=str)).astype(str))
    nested_exchange = set(symbol_files.get("inferred_exchange", pd.Series(dtype=str)).astype(str))
    return pd.DataFrame(
        [
            {
                "check_id": "P112_NESTED_SYMBOL_DIRS_DISCOVERED",
                "passed": bool(len(symbol_files) == len(FIXTURE_SYMBOLS)),
                "detail": f"discovered_symbol_rows={len(symbol_files)}",
            },
            {
                "check_id": "P112_TRADE_DATE_INFERRED_FROM_PATH",
                "passed": bool(FIXTURE_TRADE_DATE in nested_dates),
                "detail": f"inferred_trade_dates={'|'.join(sorted(nested_dates))}",
            },
            {
                "check_id": "P112_EXCHANGE_INFERRED_FROM_PATH",
                "passed": bool("NSE" in nested_exchange),
                "detail": f"inferred_exchanges={'|'.join(sorted(nested_exchange))}",
            },
            {
                "check_id": "P112_REQUIRED_SCHEMA_VALID",
                "passed": required_schema_pass,
                "detail": f"schema_rows={len(schema)}",
            },
            {
                "check_id": "P112_SYMBOL_DAY_DIAGNOSTICS_BUILT",
                "passed": bool(not symbol_day.empty and symbol_day["trade_date"].astype(str).eq(FIXTURE_TRADE_DATE).all()),
                "detail": f"diagnostic_rows={len(symbol_day)}",
            },
            {
                "check_id": "P112_DAY_READINESS_BUILT",
                "passed": bool(not day_readiness.empty and day_readiness['trade_date'].astype(str).eq(FIXTURE_TRADE_DATE).any()),
                "detail": f"day_readiness_rows={len(day_readiness)}",
            },
        ]
    )


def summarize(checks: pd.DataFrame, symbol_files: pd.DataFrame, day_readiness: pd.DataFrame) -> pd.DataFrame:
    passed = int(checks["passed"].astype(bool).sum())
    return pd.DataFrame(
        [
            ("phase112_check_rows", int(len(checks)), "Drop-zone compatibility checks executed"),
            ("phase112_checks_passed", passed, "Drop-zone compatibility checks passing"),
            ("phase112_dropzone_compatibility_pass", int(passed == len(checks)), "1 means Phase96 can scan the Phase111 drop-zone layout"),
            ("phase112_fixture_symbol_rows", int(len(symbol_files)), "Fixture symbol partitions discovered"),
            ("phase112_fixture_day_rows", int(len(day_readiness)), "Fixture day readiness rows built"),
            ("phase112_strategy_replay_allowed", 0, "Strategy replay remains closed"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase112 Drop-zone Phase96 Compatibility",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase112 verifies that Phase96 can discover and diagnose the nested Phase111 drop-zone layout.",
        "The generated fixture is intentionally tiny and strategy replay remains closed.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase112_dropzone_phase96_compatibility_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase112(output_dir: Path, fixture_root: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    create_dropzone_fixture(fixture_root)
    symbol_files = discover_symbol_files(fixture_root)
    symbol_day, schema = sampled_symbol_day_diagnostics(symbol_files, max_files_per_symbol=10)
    day_readiness = build_day_readiness(symbol_day, schema)
    checks = build_checks(symbol_files, symbol_day, schema, day_readiness)
    acceptance = summarize(checks, symbol_files, day_readiness)

    symbol_files.to_csv(output_dir / "phase112_fixture_symbol_file_inventory.csv", index=False)
    symbol_day.to_csv(output_dir / "phase112_fixture_symbol_day_diagnostics.csv", index=False)
    schema.to_csv(output_dir / "phase112_fixture_schema_validation.csv", index=False)
    day_readiness.to_csv(output_dir / "phase112_fixture_day_readiness.csv", index=False)
    checks.to_csv(output_dir / "phase112_dropzone_compatibility_checks.csv", index=False)
    acceptance.to_csv(output_dir / "phase112_dropzone_compatibility_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Compatibility Checks": checks,
            "Fixture Symbol Inventory": symbol_files,
            "Fixture Day Readiness": day_readiness,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase112_dropzone_phase96_compatibility",
        **reproducibility_fields(
            artifact_id="phase112",
            generated_utc=generated_utc,
            inputs={"fixture_root": str(fixture_root)},
            parameters={
                "fixture_trade_date": FIXTURE_TRADE_DATE,
                "fixture_symbols": FIXTURE_SYMBOLS,
                "strategy_replay_policy": "closed",
            },
            outputs={
                "symbol_inventory": str(output_dir / "phase112_fixture_symbol_file_inventory.csv"),
                "symbol_day_diagnostics": str(output_dir / "phase112_fixture_symbol_day_diagnostics.csv"),
                "schema_validation": str(output_dir / "phase112_fixture_schema_validation.csv"),
                "day_readiness": str(output_dir / "phase112_fixture_day_readiness.csv"),
                "checks": str(output_dir / "phase112_dropzone_compatibility_checks.csv"),
                "acceptance_summary": str(output_dir / "phase112_dropzone_compatibility_acceptance_summary.csv"),
                "report": str(output_dir / "phase112_dropzone_phase96_compatibility_report.md"),
                "manifest": str(output_dir / "phase112_dropzone_phase96_compatibility_manifest.json"),
            },
            random_seed="none_deterministic_phase112_fixture",
            scenario_ids="phase112_phase111_dropzone_phase96_compatibility",
            cost_model_version="not_applicable",
            latency_model_version="phase111_dropzone_contract",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase112_dropzone_phase96_compatibility_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Phase96 compatibility with Phase111 drop-zone layout.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--fixture-root", type=Path, default=DEFAULT_FIXTURE_ROOT)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase112(args.output_dir, args.fixture_root, args.base_dir)


if __name__ == "__main__":
    main()

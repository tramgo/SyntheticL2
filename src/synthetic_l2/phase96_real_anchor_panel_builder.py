from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase95_real_anchor_panel_contract import EXPECTED_SYMBOLS
from synthetic_l2.reproducibility import reproducibility_fields
from synthetic_l2.zerodha_costs import ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION


DEFAULT_REAL_ROOT = Path("real_data_sample")
DEFAULT_PHASE95_DIR = Path("outputs/phase95")
DEFAULT_OUTPUT_DIR = Path("outputs/phase96")
DEFAULT_MAX_FILES_PER_SYMBOL = 50

REQUIRED_ZERODHA_L2_COLUMNS = [
    "collector_received_utc",
    "collector_received_utc_ms",
    "collector_received_monotonic_ns",
    "exchange_timestamp",
    "last_trade_time",
    "trade_date",
    "exchange",
    "tradingsymbol",
    "requested_symbol",
    "instrument_token",
    "last_price",
    "last_traded_quantity",
    "volume_traded",
    "average_traded_price",
    "total_buy_quantity",
    "total_sell_quantity",
    "buy_1_price",
    "buy_1_quantity",
    "buy_1_orders",
    "buy_2_price",
    "buy_2_quantity",
    "buy_2_orders",
    "buy_3_price",
    "buy_3_quantity",
    "buy_3_orders",
    "buy_4_price",
    "buy_4_quantity",
    "buy_4_orders",
    "buy_5_price",
    "buy_5_quantity",
    "buy_5_orders",
    "sell_1_price",
    "sell_1_quantity",
    "sell_1_orders",
    "sell_2_price",
    "sell_2_quantity",
    "sell_2_orders",
    "sell_3_price",
    "sell_3_quantity",
    "sell_3_orders",
    "sell_4_price",
    "sell_4_quantity",
    "sell_4_orders",
    "sell_5_price",
    "sell_5_quantity",
    "sell_5_orders",
]


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


def select_files(files: list[Path], limit: int) -> list[Path]:
    files = sorted(files)
    if len(files) <= limit:
        return files
    indices = np.linspace(0, len(files) - 1, limit).round().astype(int)
    return [files[int(i)] for i in sorted(set(indices))]


def discover_symbol_files(real_root: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for panel_root in sorted(path for path in real_root.iterdir() if path.is_dir()) if real_root.exists() else []:
        for symbol_dir in sorted(path for path in panel_root.rglob("symbol=*") if path.is_dir()):
            files = sorted(symbol_dir.glob("*.parquet"))
            relative_parts = symbol_dir.relative_to(panel_root).parts
            inferred_trade_dates = sorted(
                part.split("=", 1)[1] for part in relative_parts if part.startswith("trade_date=")
            )
            inferred_exchanges = sorted(
                part.split("=", 1)[1] for part in relative_parts if part.startswith("exchange=")
            )
            rows.append(
                {
                    "panel_name": panel_root.name,
                    "panel_root": str(panel_root),
                    "symbol_dir": str(symbol_dir),
                    "layout_path": str(symbol_dir.relative_to(panel_root)),
                    "inferred_trade_date": inferred_trade_dates[0] if inferred_trade_dates else "",
                    "inferred_exchange": inferred_exchanges[0] if inferred_exchanges else "",
                    "symbol": symbol_dir.name.replace("symbol=", ""),
                    "parquet_files": int(len(files)),
                    "first_file": str(files[0]) if files else "",
                    "last_file": str(files[-1]) if files else "",
                }
            )
    return pd.DataFrame(rows)


def sampled_symbol_day_diagnostics(symbol_files: pd.DataFrame, max_files_per_symbol: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    schema_rows: list[dict[str, Any]] = []
    for item in symbol_files.to_dict("records"):
        symbol_dir = Path(str(item.get("symbol_dir") or Path(item["panel_root"]).joinpath(f"symbol={item['symbol']}")))
        files = [path for path in symbol_dir.glob("*.parquet")]
        sampled = select_files(files, max_files_per_symbol)
        frames = []
        for path in sampled:
            try:
                frame = pd.read_parquet(path)
            except Exception as exc:  # pragma: no cover - diagnostics path
                rows.append(
                    {
                        "panel_name": item["panel_name"],
                        "symbol": item["symbol"],
                        "trade_date": "read_error",
                        "sampled_files": 1,
                        "sampled_rows": 0,
                        "read_errors": 1,
                        "error": str(exc),
                    }
                )
                continue
            schema_rows.append(
                {
                    "panel_name": item["panel_name"],
                    "symbol": item["symbol"],
                    "file": str(path),
                    "column_count": int(len(frame.columns)),
                    "missing_required_columns": "|".join(sorted(set(REQUIRED_ZERODHA_L2_COLUMNS).difference(frame.columns))),
                    "required_schema_pass": set(REQUIRED_ZERODHA_L2_COLUMNS).issubset(frame.columns),
                }
            )
            keep_cols = [
                col
                for col in [
                    "trade_date",
                    "collector_received_utc_ms",
                    "buy_1_price",
                    "sell_1_price",
                    "last_price",
                    "volume_traded",
                    "tradingsymbol",
                    "requested_symbol",
                ]
                if col in frame.columns
            ]
            frames.append(frame[keep_cols].copy())
        if not frames:
            continue
        data = pd.concat(frames, ignore_index=True)
        data["trade_date"] = data["trade_date"].astype(str) if "trade_date" in data.columns else "unknown"
        inferred_trade_date = str(item.get("inferred_trade_date") or "")
        if inferred_trade_date and inferred_trade_date.lower() != "nan" and "trade_date" in data.columns:
            data["trade_date"] = data["trade_date"].replace({"": inferred_trade_date, "unknown": inferred_trade_date, "None": inferred_trade_date})
        elif inferred_trade_date and inferred_trade_date.lower() != "nan":
            data["trade_date"] = inferred_trade_date
        if "collector_received_utc_ms" in data.columns:
            data["collector_received_utc_ms"] = pd.to_numeric(data["collector_received_utc_ms"], errors="coerce")
        for trade_date, group in data.groupby("trade_date", sort=True):
            valid_book = (
                (pd.to_numeric(group.get("buy_1_price", pd.Series(dtype=float)), errors="coerce") > 0)
                & (pd.to_numeric(group.get("sell_1_price", pd.Series(dtype=float)), errors="coerce") > 0)
                & (
                    pd.to_numeric(group.get("sell_1_price", pd.Series(dtype=float)), errors="coerce")
                    >= pd.to_numeric(group.get("buy_1_price", pd.Series(dtype=float)), errors="coerce")
                )
            )
            ts = group["collector_received_utc_ms"].dropna().sort_values() if "collector_received_utc_ms" in group.columns else pd.Series(dtype=float)
            gaps = ts.diff().dropna()
            rows.append(
                {
                    "panel_name": item["panel_name"],
                    "panel_root": item["panel_root"],
                    "symbol": item["symbol"],
                    "trade_date": trade_date,
                    "sampled_files": int(len(sampled)),
                    "sampled_rows": int(len(group)),
                    "read_errors": 0,
                    "valid_l1_book_fraction": float(valid_book.mean()) if len(group) else 0.0,
                    "first_receive_ms": float(ts.min()) if not ts.empty else np.nan,
                    "last_receive_ms": float(ts.max()) if not ts.empty else np.nan,
                    "median_gap_ms": float(gaps.median()) if not gaps.empty else np.nan,
                    "p90_gap_ms": float(gaps.quantile(0.90)) if not gaps.empty else np.nan,
                }
            )
    return pd.DataFrame(rows), pd.DataFrame(schema_rows)


def build_day_readiness(symbol_day: pd.DataFrame, schema: pd.DataFrame) -> pd.DataFrame:
    if symbol_day.empty:
        return pd.DataFrame()
    schema_fail = (
        schema.groupby(["panel_name", "symbol"], sort=True)["required_schema_pass"].min().reset_index()
        if not schema.empty
        else pd.DataFrame(columns=["panel_name", "symbol", "required_schema_pass"])
    )
    merged = symbol_day.merge(schema_fail, on=["panel_name", "symbol"], how="left")
    rows: list[dict[str, Any]] = []
    for (panel_name, trade_date), group in merged.groupby(["panel_name", "trade_date"], sort=True):
        symbols = set(group["symbol"].astype(str))
        missing = sorted(EXPECTED_SYMBOLS.difference(symbols))
        schema_pass = bool(group["required_schema_pass"].fillna(False).all())
        l1_pass = bool(group["valid_l1_book_fraction"].ge(0.99).all())
        timing_pass = bool(group["first_receive_ms"].notna().all() and group["last_receive_ms"].notna().all())
        rows.append(
            {
                "panel_name": panel_name,
                "trade_date": trade_date,
                "symbols_observed": int(len(symbols)),
                "expected_symbol_fraction": len(symbols.intersection(EXPECTED_SYMBOLS)) / len(EXPECTED_SYMBOLS),
                "missing_expected_symbols": "|".join(missing),
                "sampled_rows": int(group["sampled_rows"].sum()),
                "schema_pass": schema_pass,
                "l1_book_pass": l1_pass,
                "timing_pass": timing_pass,
                "day_ready_for_anchor_panel": bool(len(missing) <= 1 and schema_pass and l1_pass and timing_pass),
            }
        )
    return pd.DataFrame(rows)


def build_panel_manifest(day_readiness: pd.DataFrame) -> pd.DataFrame:
    if day_readiness.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for panel_name, group in day_readiness.groupby("panel_name", sort=True):
        ready_days = group[group["day_ready_for_anchor_panel"].astype(bool)]
        rows.append(
            {
                "panel_name": panel_name,
                "distinct_trade_dates": int(group["trade_date"].nunique()),
                "ready_trade_dates": int(ready_days["trade_date"].nunique()),
                "ready_trade_date_list": "|".join(sorted(ready_days["trade_date"].astype(str).unique())),
                "min_expected_symbol_fraction": float(group["expected_symbol_fraction"].min()),
                "all_days_schema_pass": bool(group["schema_pass"].all()),
                "all_days_l1_book_pass": bool(group["l1_book_pass"].all()),
                "all_days_timing_pass": bool(group["timing_pass"].all()),
                "panel_ready_for_phase94_rerun": bool(
                    ready_days["trade_date"].nunique() >= 5
                    and group["expected_symbol_fraction"].min() >= 0.95
                    and group["schema_pass"].all()
                    and group["timing_pass"].all()
                ),
            }
        )
    return pd.DataFrame(rows)


def build_replay_gate(panel_manifest: pd.DataFrame, phase95_dir: Path) -> pd.DataFrame:
    phase95_ready = metric_value(phase95_dir / "real_anchor_panel_acceptance_summary.csv", "phase95_real_anchor_panel_ready", 0)
    any_panel_ready = bool(panel_manifest["panel_ready_for_phase94_rerun"].any()) if not panel_manifest.empty else False
    return pd.DataFrame(
        [
            {
                "gate_id": "P96_REAL_PANEL_READY_FOR_PHASE94_RERUN",
                "gate_pass": any_panel_ready,
                "evidence": "At least one panel has >=5 ready trade dates with >=95% symbol coverage, schema pass, L1 book pass, and timing pass.",
                "next_action_if_fail": "collect_more_real_websocket_l2_days",
            },
            {
                "gate_id": "P96_STRATEGY_REPLAY_LOCK",
                "gate_pass": bool(any_panel_ready and int(float(phase95_ready)) == 1),
                "evidence": f"Phase95 real_anchor_panel_ready={phase95_ready}; Phase96 panel_ready={int(any_panel_ready)}.",
                "next_action_if_fail": "keep_strategy_replay_closed_until_phase94_rerun_passes",
            },
        ]
    )


def summarize(symbol_files: pd.DataFrame, day_readiness: pd.DataFrame, panel_manifest: pd.DataFrame, replay_gate: pd.DataFrame) -> pd.DataFrame:
    ready_panel_day_rows = int(day_readiness["day_ready_for_anchor_panel"].sum()) if not day_readiness.empty else 0
    max_ready_dates = int(panel_manifest["ready_trade_dates"].max()) if not panel_manifest.empty else 0
    ready_panels = int(panel_manifest["panel_ready_for_phase94_rerun"].sum()) if not panel_manifest.empty else 0
    replay_lock_pass = bool(replay_gate.loc[replay_gate["gate_id"].eq("P96_STRATEGY_REPLAY_LOCK"), "gate_pass"].iloc[0])
    return pd.DataFrame(
        [
            ("phase96_symbol_partitions_found", int(len(symbol_files)), "Symbol partitions discovered under real-data roots"),
            ("phase96_total_real_parquet_files", int(symbol_files["parquet_files"].sum()) if not symbol_files.empty else 0, "Total real Parquet files inventoried"),
            ("phase96_day_readiness_rows", int(len(day_readiness)), "Panel/day readiness rows built from deterministic samples"),
            (
                "phase96_ready_anchor_days",
                max_ready_dates,
                "Maximum distinct ready trade dates in any one real-data panel; duplicate copies of the same trade date across panels do not compound.",
            ),
            (
                "phase96_ready_panel_day_rows",
                ready_panel_day_rows,
                "Diagnostic count of ready panel/day rows before single-panel distinct-date de-duplication.",
            ),
            ("phase96_max_ready_dates_in_panel", max_ready_dates, "Maximum ready trade-date count in any panel"),
            ("phase96_panels_ready_for_phase94_rerun", ready_panels, "Panels with enough ready days for Phase94 rerun"),
            ("phase96_strategy_replay_unlocked", int(replay_lock_pass), "1 means strategy replay gate is reopened"),
            ("phase96_recommend_next_action", "collect_more_real_websocket_l2_days", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase96 Real Anchor Panel Builder",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase96 validates available real Zerodha WebSocket L2 data against the Phase95 multi-day panel contract.",
        "It uses deterministic per-symbol file sampling so the current 50k tiny-file one-day archive can be checked quickly, while preserving the replay lock until enough real days exist.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase96_real_anchor_panel_builder_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase96(real_root: Path, phase95_dir: Path, output_dir: Path, base_dir: Path, max_files_per_symbol: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    symbol_files = discover_symbol_files(real_root)
    symbol_day, schema = sampled_symbol_day_diagnostics(symbol_files, max_files_per_symbol)
    day_readiness = build_day_readiness(symbol_day, schema)
    panel_manifest = build_panel_manifest(day_readiness)
    replay_gate = build_replay_gate(panel_manifest, phase95_dir)
    acceptance = summarize(symbol_files, day_readiness, panel_manifest, replay_gate)

    symbol_files.to_csv(output_dir / "real_symbol_file_inventory.csv", index=False)
    symbol_day.to_csv(output_dir / "sampled_symbol_day_diagnostics.csv", index=False)
    schema.to_csv(output_dir / "sampled_schema_validation.csv", index=False)
    day_readiness.to_csv(output_dir / "real_day_readiness.csv", index=False)
    panel_manifest.to_csv(output_dir / "real_anchor_panel_manifest.csv", index=False)
    replay_gate.to_csv(output_dir / "real_anchor_replay_gate.csv", index=False)
    acceptance.to_csv(output_dir / "real_anchor_panel_builder_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Panel Manifest": panel_manifest,
            "Replay Gate": replay_gate,
            "Day Readiness": day_readiness,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {"generated_utc": generated_utc, "scope": "phase96_real_anchor_panel_builder"}
    manifest.update(
        reproducibility_fields(
            artifact_id="phase96",
            generated_utc=generated_utc,
            inputs={
                "real_root": str(real_root),
                "phase95_summary": str(phase95_dir / "real_anchor_panel_acceptance_summary.csv"),
            },
            parameters={
                "max_files_per_symbol": max_files_per_symbol,
                "minimum_ready_trade_dates": 5,
                "minimum_expected_symbol_fraction": 0.95,
                "strategy_replay_policy": "locked_until_phase94_rerun_passes_on_ready_panel",
            },
            outputs={
                "symbol_file_inventory": str(output_dir / "real_symbol_file_inventory.csv"),
                "sampled_symbol_day_diagnostics": str(output_dir / "sampled_symbol_day_diagnostics.csv"),
                "sampled_schema_validation": str(output_dir / "sampled_schema_validation.csv"),
                "day_readiness": str(output_dir / "real_day_readiness.csv"),
                "panel_manifest": str(output_dir / "real_anchor_panel_manifest.csv"),
                "replay_gate": str(output_dir / "real_anchor_replay_gate.csv"),
                "acceptance_summary": str(output_dir / "real_anchor_panel_builder_acceptance_summary.csv"),
                "report": str(output_dir / "phase96_real_anchor_panel_builder_report.md"),
                "manifest": str(output_dir / "phase96_real_anchor_panel_builder_manifest.json"),
            },
            random_seed="none_deterministic_file_sampling",
            scenario_ids="phase96_post_phase95_real_panel_builder",
            cost_model_version=ZERODHA_EQUITY_INTRADAY_NSE_MODEL_VERSION,
            latency_model_version="not_applicable_data_readiness_builder",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase96_real_anchor_panel_builder_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build/validate real anchor panel readiness from available real L2 data.")
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--phase95-dir", type=Path, default=DEFAULT_PHASE95_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--max-files-per-symbol", type=int, default=DEFAULT_MAX_FILES_PER_SYMBOL)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase96(args.real_root, args.phase95_dir, args.output_dir, args.base_dir, args.max_files_per_symbol)


if __name__ == "__main__":
    main()

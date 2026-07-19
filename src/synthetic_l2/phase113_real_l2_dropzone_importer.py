from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase95_real_anchor_panel_contract import EXPECTED_SYMBOLS
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_SOURCE_ROOT = Path("real_data_sample/l2_single_day")
DEFAULT_TARGET_ROOT = Path("real_data_sample/l2_multiday_panel")
DEFAULT_OUTPUT_DIR = Path("outputs/phase113")
DEFAULT_EXCHANGE = "NSE"


def infer_from_parts(path: Path, prefix: str) -> str:
    for part in path.parts:
        if part.startswith(prefix + "="):
            return part.split("=", 1)[1]
    return ""


def infer_trade_date_from_file(path: Path) -> str:
    try:
        frame = pd.read_parquet(path, columns=["trade_date"])
    except Exception:
        return ""
    if frame.empty or "trade_date" not in frame.columns:
        return ""
    values = frame["trade_date"].dropna().astype(str).unique().tolist()
    return str(values[0]) if values else ""


def discover_source_symbol_partitions(source_root: Path, default_exchange: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if not source_root.exists():
        return pd.DataFrame(
            [
                {
                    "source_root": str(source_root),
                    "source_symbol_dir": "",
                    "symbol": "",
                    "source_layout": "missing_source_root",
                    "inferred_trade_date": "",
                    "inferred_exchange": default_exchange,
                    "parquet_files": 0,
                    "first_file": "",
                    "last_file": "",
                    "ready_for_import": False,
                    "blocker": "source_root_missing",
                }
            ]
        )
    symbol_dirs = sorted(path for path in source_root.rglob("symbol=*") if path.is_dir())
    if not symbol_dirs and source_root.name.startswith("symbol="):
        symbol_dirs = [source_root]
    for symbol_dir in symbol_dirs:
        files = sorted(symbol_dir.glob("*.parquet"))
        symbol = symbol_dir.name.split("=", 1)[1]
        path_trade_date = infer_from_parts(symbol_dir, "trade_date")
        exchange = infer_from_parts(symbol_dir, "exchange") or default_exchange
        file_trade_date = infer_trade_date_from_file(files[0]) if files and not path_trade_date else ""
        trade_date = path_trade_date or file_trade_date
        source_layout = "nested_trade_date_exchange_symbol" if path_trade_date else "symbol_partition_with_file_trade_date"
        blocker = ""
        if not files:
            blocker = "no_parquet_files"
        elif not trade_date:
            blocker = "trade_date_not_in_path_or_first_file"
        elif symbol not in EXPECTED_SYMBOLS:
            blocker = "symbol_not_in_expected_universe"
        rows.append(
            {
                "source_root": str(source_root),
                "source_symbol_dir": str(symbol_dir),
                "symbol": symbol,
                "source_layout": source_layout,
                "inferred_trade_date": trade_date,
                "inferred_exchange": exchange,
                "parquet_files": int(len(files)),
                "first_file": str(files[0]) if files else "",
                "last_file": str(files[-1]) if files else "",
                "ready_for_import": bool(not blocker),
                "blocker": blocker,
            }
        )
    return pd.DataFrame(rows)


def build_import_plan(partitions: pd.DataFrame, target_root: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in partitions.to_dict("records"):
        if not bool(item.get("ready_for_import", False)):
            rows.append(
                {
                    "symbol": item.get("symbol", ""),
                    "trade_date": item.get("inferred_trade_date", ""),
                    "exchange": item.get("inferred_exchange", ""),
                    "source_symbol_dir": item.get("source_symbol_dir", ""),
                    "target_symbol_dir": "",
                    "parquet_files": int(item.get("parquet_files", 0) or 0),
                    "planned_action": "skip",
                    "blocker": item.get("blocker", "not_ready"),
                }
            )
            continue
        target_symbol_dir = (
            target_root
            / f"trade_date={item['inferred_trade_date']}"
            / f"exchange={item['inferred_exchange']}"
            / f"symbol={item['symbol']}"
        )
        rows.append(
            {
                "symbol": item["symbol"],
                "trade_date": item["inferred_trade_date"],
                "exchange": item["inferred_exchange"],
                "source_symbol_dir": item["source_symbol_dir"],
                "target_symbol_dir": str(target_symbol_dir),
                "parquet_files": int(item["parquet_files"]),
                "planned_action": "copy_symbol_partition",
                "blocker": "",
            }
        )
    return pd.DataFrame(rows)


def execute_import(import_plan: pd.DataFrame, overwrite: bool) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in import_plan.to_dict("records"):
        if item["planned_action"] != "copy_symbol_partition":
            rows.append({**item, "executed": False, "copied_files": 0, "execution_status": item.get("blocker", "skipped")})
            continue
        source_dir = Path(item["source_symbol_dir"])
        target_dir = Path(item["target_symbol_dir"])
        target_dir.mkdir(parents=True, exist_ok=True)
        copied = 0
        for source_file in sorted(source_dir.glob("*.parquet")):
            target_file = target_dir / source_file.name
            if target_file.exists() and not overwrite:
                continue
            shutil.copy2(source_file, target_file)
            copied += 1
        rows.append({**item, "executed": True, "copied_files": copied, "execution_status": "copied"})
    return pd.DataFrame(rows)


def summarize(partitions: pd.DataFrame, import_plan: pd.DataFrame, execution: pd.DataFrame, execute: bool) -> pd.DataFrame:
    ready = partitions[partitions["ready_for_import"].astype(bool)] if not partitions.empty else pd.DataFrame()
    ready_dates = sorted(ready["inferred_trade_date"].dropna().astype(str).unique().tolist()) if not ready.empty else []
    ready_symbols = sorted(ready["symbol"].dropna().astype(str).unique().tolist()) if not ready.empty else []
    copied_files = int(execution["copied_files"].sum()) if execute and not execution.empty and "copied_files" in execution.columns else 0
    return pd.DataFrame(
        [
            ("phase113_source_symbol_partitions", int(len(partitions)), "Source symbol partitions inspected"),
            ("phase113_ready_symbol_partitions", int(len(ready)), "Source symbol partitions ready for import"),
            ("phase113_ready_trade_dates", int(len(ready_dates)), "Distinct ready trade dates inferred"),
            ("phase113_ready_symbols", int(len(ready_symbols)), "Distinct ready symbols inferred"),
            ("phase113_ready_expected_symbol_fraction", len(set(ready_symbols).intersection(EXPECTED_SYMBOLS)) / len(EXPECTED_SYMBOLS), "Expected universe fraction ready in source"),
            ("phase113_import_plan_rows", int(len(import_plan)), "Import plan rows emitted"),
            ("phase113_execute_mode", int(execute), "1 means files were copied into the drop-zone"),
            ("phase113_copied_files", copied_files, "Parquet files copied when execute mode is enabled"),
            ("phase113_strategy_replay_allowed", 0, "Strategy replay remains closed"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase113 Real L2 Drop-zone Importer",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase113 creates a dry-run-safe import plan for normalizing real Zerodha WebSocket L2 parquet into the Phase111/112 multiday drop-zone layout.",
        "It does not enable strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase113_real_l2_dropzone_importer_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase113(
    source_root: Path,
    target_root: Path,
    output_dir: Path,
    base_dir: Path,
    default_exchange: str,
    execute: bool,
    overwrite: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    partitions = discover_source_symbol_partitions(source_root, default_exchange)
    import_plan = build_import_plan(partitions, target_root)
    execution = execute_import(import_plan, overwrite=overwrite) if execute else pd.DataFrame()
    acceptance = summarize(partitions, import_plan, execution, execute=execute)

    partitions.to_csv(output_dir / "phase113_source_partition_inventory.csv", index=False)
    import_plan.to_csv(output_dir / "phase113_dropzone_import_plan.csv", index=False)
    execution.to_csv(output_dir / "phase113_dropzone_import_execution.csv", index=False)
    acceptance.to_csv(output_dir / "phase113_dropzone_import_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Source Partition Inventory": partitions,
            "Drop-zone Import Plan": import_plan,
            "Import Execution": execution,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase113_real_l2_dropzone_importer",
        **reproducibility_fields(
            artifact_id="phase113",
            generated_utc=generated_utc,
            inputs={"source_root": str(source_root)},
            parameters={
                "target_root": str(target_root),
                "default_exchange": default_exchange,
                "execute": execute,
                "overwrite": overwrite,
                "strategy_replay_policy": "closed",
            },
            outputs={
                "source_inventory": str(output_dir / "phase113_source_partition_inventory.csv"),
                "import_plan": str(output_dir / "phase113_dropzone_import_plan.csv"),
                "execution": str(output_dir / "phase113_dropzone_import_execution.csv"),
                "acceptance_summary": str(output_dir / "phase113_dropzone_import_acceptance_summary.csv"),
                "report": str(output_dir / "phase113_real_l2_dropzone_importer_report.md"),
                "manifest": str(output_dir / "phase113_real_l2_dropzone_importer_manifest.json"),
            },
            random_seed="none_deterministic_phase113_import_plan",
            scenario_ids="phase113_real_l2_dropzone_importer",
            cost_model_version="not_applicable",
            latency_model_version="phase112_dropzone_compatibility",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase113_real_l2_dropzone_importer_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create or execute real L2 drop-zone import plan.")
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--target-root", type=Path, default=DEFAULT_TARGET_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--default-exchange", default=DEFAULT_EXCHANGE)
    parser.add_argument("--execute", action="store_true", help="Copy files into target drop-zone. Default is dry-run only.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing target files when --execute is used.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase113(
        args.source_root,
        args.target_root,
        args.output_dir,
        args.base_dir,
        args.default_exchange,
        args.execute,
        args.overwrite,
    )


if __name__ == "__main__":
    main()

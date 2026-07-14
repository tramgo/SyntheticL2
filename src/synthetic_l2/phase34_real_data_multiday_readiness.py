from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DATE_RE = re.compile(r"trade_date=(\d{4}-\d{2}-\d{2})")
EXCHANGE_RE = re.compile(r"exchange=([^/\\]+)")
SYMBOL_RE = re.compile(r"symbol=([^/\\]+)")


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def _extract(pattern: re.Pattern[str], value: str, default: str = "unknown") -> str:
    match = pattern.search(value)
    return match.group(1) if match else default


def build_symbol_day_coverage(manifest: pd.DataFrame, phase1_summary: pd.DataFrame) -> pd.DataFrame:
    frame = manifest.copy()
    frame["remote_path"] = frame["remote_path"].astype(str)
    frame["trade_date"] = frame["remote_path"].map(lambda value: _extract(DATE_RE, value))
    frame["exchange"] = frame["remote_path"].map(lambda value: _extract(EXCHANGE_RE, value))
    frame["symbol"] = frame["remote_path"].map(lambda value: _extract(SYMBOL_RE, value))
    grouped = (
        frame.groupby(["trade_date", "exchange", "symbol"], sort=True)
        .agg(parquet_files=("name", "count"), bytes=("bytes", "sum"))
        .reset_index()
    )
    phase1 = phase1_summary.rename(columns={"symbol": "symbol", "rows": "phase1_delta_rows"}).copy()
    grouped = grouped.merge(
        phase1[["symbol", "phase1_delta_rows", "book_valid_fraction", "stale_gap_gt_15s_count", "median_elapsed_ms", "p95_elapsed_ms"]],
        on="symbol",
        how="left",
    )
    grouped["raw_file_coverage_status"] = grouped["parquet_files"].map(lambda value: "raw_files_present" if int(value) > 0 else "raw_files_missing")
    grouped["phase1_delta_available"] = grouped["phase1_delta_rows"].fillna(0).astype(int) > 0
    grouped["class_b_event_grade_now"] = False
    grouped["blocking_reason"] = "Only one raw sample day is available and Stage A2 capture diagnostics remain open."
    return grouped


def build_day_inventory(symbol_day: pd.DataFrame, stage_a2_summary: pd.DataFrame) -> pd.DataFrame:
    stage = stage_a2_summary.iloc[0]
    rows = []
    for (trade_date, exchange), group in symbol_day.groupby(["trade_date", "exchange"], sort=True):
        symbols = int(group["symbol"].nunique())
        rows.append(
            {
                "trade_date": trade_date,
                "exchange": exchange,
                "symbols": symbols,
                "parquet_files": int(group["parquet_files"].sum()),
                "bytes": int(group["bytes"].sum()),
                "phase1_delta_rows": int(group["phase1_delta_rows"].fillna(0).sum()),
                "symbols_with_phase1_delta": int(group["phase1_delta_available"].sum()),
                "required_symbols": int(stage["symbols_evaluated"]),
                "full_universe_raw_day": bool(symbols >= int(stage["symbols_evaluated"])),
                "class_b_event_grade_day": False,
                "day_status": "raw_full_universe_day_not_class_b" if symbols >= int(stage["symbols_evaluated"]) else "partial_raw_day_not_class_b",
                "blocking_reason": "Stage A2 reports 0 acceptance-met rows and requires multi-day capture diagnostics.",
            }
        )
    return pd.DataFrame(rows)


def build_readiness(day_inventory: pd.DataFrame, stage_a2_summary: pd.DataFrame, phase22_milestones: pd.DataFrame) -> pd.DataFrame:
    stage = stage_a2_summary.iloc[0]
    min_days = int(stage["required_complete_days_min"])
    target_days = int(stage["required_complete_days_target"])
    raw_days = int(day_inventory["trade_date"].nunique()) if len(day_inventory) else 0
    full_universe_days = int(day_inventory["full_universe_raw_day"].sum()) if len(day_inventory) else 0
    class_b_days = int(day_inventory["class_b_event_grade_day"].sum()) if len(day_inventory) else 0
    return pd.DataFrame(
        [
            {"metric": "phase34_raw_trade_days_available", "value": raw_days, "description": "Unique raw trade dates detected in local real-data manifest"},
            {"metric": "phase34_full_universe_raw_days", "value": full_universe_days, "description": "Raw days covering the current required symbol universe"},
            {"metric": "phase34_class_b_event_grade_days", "value": class_b_days, "description": "Days currently passing Class B event-grade readiness"},
            {"metric": "phase34_required_complete_days_min", "value": min_days, "description": "Minimum complete days required by Stage A2"},
            {"metric": "phase34_required_complete_days_target", "value": target_days, "description": "Target complete days required by Stage A2"},
            {"metric": "phase34_days_needed_for_min", "value": max(min_days - class_b_days, 0), "description": "Additional Class B days needed for minimum"},
            {"metric": "phase34_days_needed_for_target", "value": max(target_days - class_b_days, 0), "description": "Additional Class B days needed for target"},
            {"metric": "phase34_stage_a2_open_contract_rows", "value": int(stage["open_contract_rows"]), "description": "Open Stage A2 capture contract rows"},
            {"metric": "phase34_phase22_milestones_extension_ready", "value": int(phase22_milestones["acceptance_permission"].astype(bool).sum()), "description": "Phase 22 real-data milestones currently allowed for extension/paper use"},
            {"metric": "phase34_replay_allowed_rows", "value": 0, "description": "Replay rows enabled by current multi-day real-data readiness"},
        ]
    )


def build_acquisition_plan(readiness: pd.DataFrame, day_inventory: pd.DataFrame) -> pd.DataFrame:
    value = {row["metric"]: int(row["value"]) for row in readiness.to_dict("records")}
    rows = [
        {
            "priority": 1,
            "action_id": "collect_class_b_days_minimum",
            "action": f"Collect or import {value['phase34_days_needed_for_min']} additional Class B event-grade trading days.",
            "current_blocker": "Minimum Class B day count is not met.",
            "acceptance_effect": "Unlocks minimum multi-day real-data requirement only after Stage A2 diagnostics also pass.",
        },
        {
            "priority": 2,
            "action_id": "close_stage_a2_capture_contracts",
            "action": "Produce connection-boundary, dropped-message, local-sequence, lossless-compaction and timestamp-semantics diagnostics for each collected day/symbol.",
            "current_blocker": f"{value['phase34_stage_a2_open_contract_rows']} Stage A2 contract rows remain open.",
            "acceptance_effect": "Converts raw days into Class B event-grade days when all diagnostics pass.",
        },
        {
            "priority": 3,
            "action_id": "expand_to_target_days",
            "action": f"Collect or import {value['phase34_days_needed_for_target']} Class B event-grade days for target coverage.",
            "current_blocker": "Target Class B day count is not met.",
            "acceptance_effect": "Supports stronger holdout, label stability and acceptance-grade replay prerequisites.",
        },
    ]
    if len(day_inventory):
        rows.append(
            {
                "priority": 4,
                "action_id": "preserve_current_raw_day",
                "action": "Keep the current full-universe raw sample day as a smoke/regression day, but do not treat it as Class B acceptance evidence.",
                "current_blocker": "Current day is raw/full-universe but not Stage A2 accepted.",
                "acceptance_effect": "Maintains schema and pipeline regression coverage without overstating acceptance readiness.",
            }
        )
    return pd.DataFrame(rows)


def run_phase34(manifest_path: Path, phase1_summary_path: Path, stage_a2_summary_path: Path, phase22_milestones_path: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = _read_csv(manifest_path)
    phase1_summary = _read_csv(phase1_summary_path)
    stage_a2_summary = _read_csv(stage_a2_summary_path)
    phase22_milestones = _read_csv(phase22_milestones_path)

    symbol_day = build_symbol_day_coverage(manifest, phase1_summary)
    day_inventory = build_day_inventory(symbol_day, stage_a2_summary)
    readiness = build_readiness(day_inventory, stage_a2_summary, phase22_milestones)
    acquisition = build_acquisition_plan(readiness, day_inventory)

    symbol_day.to_csv(output_dir / "symbol_day_real_data_coverage.csv", index=False)
    day_inventory.to_csv(output_dir / "real_data_day_inventory.csv", index=False)
    readiness.to_csv(output_dir / "multiday_real_data_readiness_summary.csv", index=False)
    acquisition.to_csv(output_dir / "multiday_real_data_acquisition_plan.csv", index=False)
    write_report(output_dir, readiness, day_inventory, symbol_day, acquisition)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest_out = {
        "generated_utc": generated_utc,
        "raw_trade_days_available": int(day_inventory["trade_date"].nunique()) if len(day_inventory) else 0,
        "class_b_event_grade_days": 0,
        "replay_allowed_rows": 0,
        "scope": "phase34_real_data_multiday_readiness_inventory_not_acceptance",
        "not_acceptance_result": True,
    }
    manifest_out.update(
        reproducibility_fields(
            artifact_id="phase34",
            generated_utc=generated_utc,
            inputs={
                "azure_files_manifest": str(manifest_path),
                "phase1_feature_summary": str(phase1_summary_path),
                "stage_a2_readiness_summary": str(stage_a2_summary_path),
                "phase22_real_data_milestone_catalog": str(phase22_milestones_path),
            },
            parameters={
                "class_b_policy": "raw_days_are_not_class_b_until_stage_a2_capture_diagnostics_acceptance_rows_are_met",
                "minimum_days_source": str(stage_a2_summary_path),
            },
            outputs={
                "symbol_day_coverage": str(output_dir / "symbol_day_real_data_coverage.csv"),
                "day_inventory": str(output_dir / "real_data_day_inventory.csv"),
                "readiness_summary": str(output_dir / "multiday_real_data_readiness_summary.csv"),
                "acquisition_plan": str(output_dir / "multiday_real_data_acquisition_plan.csv"),
                "report": str(output_dir / "phase34_real_data_multiday_readiness_report.md"),
                "manifest": str(output_dir / "phase34_real_data_multiday_readiness_manifest.json"),
            },
            random_seed="none_deterministic_manifest_inventory",
            scenario_ids="current_local_real_l2_manifest",
            cost_model_version="not_applicable_real_data_inventory",
            latency_model_version="stage_a2_capture_diagnostics_contract",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase34_real_data_multiday_readiness_manifest.json").write_text(json.dumps(manifest_out, indent=2), encoding="utf-8")


def write_report(output_dir: Path, readiness: pd.DataFrame, day_inventory: pd.DataFrame, symbol_day: pd.DataFrame, acquisition: pd.DataFrame) -> None:
    lines = [
        "# Phase 34 Real Data Multi-Day Readiness",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This milestone inventories local real L2 raw data against the multi-day Class B requirement.",
        "Raw/full-universe coverage is reported separately from Class B event-grade readiness.",
        "",
        "## Readiness Summary",
        "",
        _markdown_table(readiness),
        "",
        "## Day Inventory",
        "",
        _markdown_table(day_inventory),
        "",
        "## Acquisition Plan",
        "",
        _markdown_table(acquisition),
        "",
        "## Symbol-Day Coverage",
        "",
        _markdown_table(symbol_day),
        "",
    ]
    (output_dir / "phase34_real_data_multiday_readiness_report.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory local real L2 data against multi-day Class B readiness.")
    parser.add_argument("--manifest", type=Path, default=Path("real_data_sample/l2_single_day/azure_files_manifest.csv"))
    parser.add_argument("--phase1-summary", type=Path, default=Path("outputs/phase1/phase1_feature_summary.csv"))
    parser.add_argument("--stage-a2-summary", type=Path, default=Path("outputs/stage_a2/stage_a2_readiness_summary.csv"))
    parser.add_argument("--phase22-milestones", type=Path, default=Path("outputs/phase22/real_data_milestone_catalog.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase34"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase34(args.manifest, args.phase1_summary, args.stage_a2_summary, args.phase22_milestones, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

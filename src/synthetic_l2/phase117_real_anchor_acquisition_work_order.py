from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase95_real_anchor_panel_contract import EXPECTED_SYMBOLS
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_OUTPUT_DIR = Path("outputs/phase117")
DEFAULT_REAL_ROOT = Path("real_data_sample")
DEFAULT_PHASE115_DIR = Path("outputs/phase115")
DEFAULT_PHASE116_DIR = Path("outputs/phase116")
MIN_READY_REAL_DAYS = 5
TARGET_READY_REAL_DAYS = 10


def read_metric_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["metric", "value", "description"])
    return pd.read_csv(path)


def metric_value(frame: pd.DataFrame, metric: str, default: Any = None) -> Any:
    if frame.empty or "metric" not in frame.columns:
        return default
    rows = frame.loc[frame["metric"].astype(str).eq(metric), "value"]
    if rows.empty:
        return default
    value = rows.iloc[0]
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def infer_dates_from_path(path: Path) -> set[str]:
    dates: set[str] = set()
    for part in path.parts:
        if part.startswith("trade_date="):
            dates.add(part.split("=", 1)[1])
    return dates


def discover_local_panels(base_dir: Path, candidate_roots: list[Path]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for rel_root in candidate_roots:
        root = base_dir / rel_root
        if not root.exists():
            rows.append(
                {
                    "candidate_root": str(rel_root),
                    "panel_root": "",
                    "status": "missing_root",
                    "layout_type": "missing",
                    "parquet_files": 0,
                    "bytes": 0,
                    "symbols_observed": 0,
                    "expected_symbol_fraction": 0.0,
                    "trade_dates_observed": 0,
                    "trade_date_list": "",
                    "ready_candidate": False,
                    "recommended_action": "create_this_root_or_place_exported_real_l2_partitions_here",
                }
            )
            continue

        search_roots = [root]
        search_roots.extend(path for path in root.rglob("*") if path.is_dir() and path.name.startswith("trade_date="))
        search_roots.extend(
            path
            for path in root.rglob("*")
            if path.is_dir() and any(child.is_dir() and child.name.startswith("symbol=") for child in path.iterdir())
        )
        for panel_root in sorted(set(search_roots)):
            key = str(panel_root.resolve())
            if key in seen:
                continue
            seen.add(key)
            files = sorted(panel_root.rglob("*.parquet"))
            if not files:
                continue
            symbol_dirs = [path for path in panel_root.rglob("symbol=*") if path.is_dir()]
            symbols = sorted({path.name.split("=", 1)[1] for path in symbol_dirs})
            dates: set[str] = set()
            dates.update(infer_dates_from_path(panel_root))
            for file_path in files[:5000]:
                dates.update(infer_dates_from_path(file_path))
            if not dates and "single_day" in panel_root.name:
                dates.add("unknown_single_day")
            expected_fraction = len(set(symbols).intersection(EXPECTED_SYMBOLS)) / len(EXPECTED_SYMBOLS)
            layout_type = "trade_date_exchange_symbol" if dates and "exchange=" in str(panel_root) else (
                "trade_date_symbol" if dates else "symbol_only_or_unknown_date"
            )
            rows.append(
                {
                    "candidate_root": str(rel_root),
                    "panel_root": str(panel_root.relative_to(base_dir)),
                    "status": "found_parquet",
                    "layout_type": layout_type,
                    "parquet_files": int(len(files)),
                    "bytes": int(sum(file.stat().st_size for file in files)),
                    "symbols_observed": int(len(symbols)),
                    "expected_symbol_fraction": expected_fraction,
                    "trade_dates_observed": int(len(dates)),
                    "trade_date_list": "|".join(sorted(dates)),
                    "ready_candidate": bool(expected_fraction >= 0.95 and len(dates) >= 1),
                    "recommended_action": "validate_with_phase115_execute_import" if expected_fraction >= 0.95 else "complete_missing_symbols_before_import",
                }
            )
    return pd.DataFrame(rows)


def build_acquisition_slots(current_ready_days: int) -> pd.DataFrame:
    min_missing = max(0, MIN_READY_REAL_DAYS - current_ready_days)
    target_missing = max(0, TARGET_READY_REAL_DAYS - current_ready_days)
    rows: list[dict[str, Any]] = []
    for slot in range(1, target_missing + 1):
        required_for = "minimum_unlock" if slot <= min_missing else "preferred_target"
        rows.append(
            {
                "slot_id": f"REAL_L2_DAY_{current_ready_days + slot:02d}",
                "required_for": required_for,
                "trade_date": "TBD_real_nse_trading_day",
                "exchange": "NSE",
                "symbols_required": len(EXPECTED_SYMBOLS),
                "minimum_expected_symbol_fraction": 0.95,
                "required_layout": "real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet",
                "required_tick_content": "raw Zerodha WebSocket-like callbacks with L1-L5 bid/ask price, quantity and order count persisted per update",
                "acceptance_after_drop": "Phase115 --execute-import completes with Phase96 ready day count incremented",
            }
        )
    if not rows:
        rows.append(
            {
                "slot_id": "REAL_L2_DAY_TARGET_MET",
                "required_for": "none",
                "trade_date": "",
                "exchange": "NSE",
                "symbols_required": len(EXPECTED_SYMBOLS),
                "minimum_expected_symbol_fraction": 0.95,
                "required_layout": "already_satisfied",
                "required_tick_content": "already_satisfied",
                "acceptance_after_drop": "rerun Phase115 before opening replay",
            }
        )
    return pd.DataFrame(rows)


def build_import_execution_plan(base_dir: Path, current_ready_days: int) -> pd.DataFrame:
    source = base_dir / "real_data_sample" / "l2_multiday_panel"
    source_exists = source.exists()
    return pd.DataFrame(
        [
            {
                "step": 1,
                "action": "drop_or_sync_real_l2_exports",
                "command": "Place each new day under real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet",
                "runs_now": False,
                "why": "The current workspace has only one ready real anchor day; new external data must arrive before replay can unlock.",
            },
            {
                "step": 2,
                "action": "dry_run_discovery",
                "command": "python scripts/run_phase115_real_panel_refresh_orchestrator.py",
                "runs_now": True,
                "why": "Confirms candidate inventory without copying files.",
            },
            {
                "step": 3,
                "action": "execute_import_and_refresh_gates",
                "command": "python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import",
                "runs_now": bool(source_exists and current_ready_days < MIN_READY_REAL_DAYS),
                "why": "Copies normalized drop-zone files, verifies integrity, rebuilds Phase96 readiness and Phase110 replay-unlock evidence.",
            },
            {
                "step": 4,
                "action": "review_unlock",
                "command": "Import-Csv outputs/phase115/phase115_real_panel_refresh_acceptance_summary.csv",
                "runs_now": True,
                "why": "Replay remains closed unless ready real anchor days reach the required gate and downstream realism gates are refreshed.",
            },
        ]
    )


def build_acceptance_summary(
    phase115: pd.DataFrame,
    phase116: pd.DataFrame,
    inventory: pd.DataFrame,
    slots: pd.DataFrame,
) -> pd.DataFrame:
    ready_days = as_int(metric_value(phase115, "phase115_phase110_ready_real_anchor_days"))
    days_needed_min = max(0, MIN_READY_REAL_DAYS - ready_days)
    days_needed_target = max(0, TARGET_READY_REAL_DAYS - ready_days)
    replay_allowed = as_int(metric_value(phase115, "phase115_strategy_replay_allowed"))
    same_family_allowed = as_int(metric_value(phase116, "phase116_same_family_shard_continuation_allowed"))
    ready_candidates = int(inventory["ready_candidate"].astype(bool).sum()) if not inventory.empty else 0
    minimum_slots = int(slots["required_for"].astype(str).eq("minimum_unlock").sum()) if not slots.empty else 0
    return pd.DataFrame(
        [
            ("phase117_current_ready_real_anchor_days", ready_days, "Ready real anchor days proven by latest Phase115/Phase110 evidence"),
            ("phase117_additional_days_needed_for_min", days_needed_min, "Additional ready real days needed for minimum replay unlock consideration"),
            ("phase117_additional_days_needed_for_target", days_needed_target, "Additional ready real days needed for preferred 10-day target"),
            ("phase117_local_candidate_panel_rows", int(len(inventory)), "Local candidate panel roots/files inventoried"),
            ("phase117_ready_candidate_panel_rows", ready_candidates, "Candidate panels with broad enough symbol coverage for import validation"),
            ("phase117_minimum_unlock_acquisition_slots", minimum_slots, "Concrete missing day slots required for minimum unlock"),
            ("phase117_strategy_replay_allowed", replay_allowed, "Current replay allowed flag inherited from Phase115"),
            ("phase117_same_family_shard_continuation_allowed", same_family_allowed, "Current failed-family compute gate inherited from Phase116"),
            ("phase117_acquisition_gate_status", "open" if days_needed_min > 0 else "ready_for_phase115_execute_import", "Whether additional real data must be acquired before replay work"),
            (
                "phase117_next_best_action",
                f"drop_or_sync_{days_needed_min}_more_real_l2_days_then_run_phase115_with_execute_import"
                if days_needed_min > 0
                else "run_phase115_with_execute_import_and_review_unlock",
                "Recommended next milestone",
            ),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase117 Real Anchor Acquisition Work Order",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase117 converts the Phase116 next-action verdict into an operational work order.",
        "It does not claim more strategy evidence. It states exactly what real Zerodha WebSocket L2 data must be added before replay can reopen.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase117_real_anchor_acquisition_work_order_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def run_phase117(
    base_dir: Path,
    output_dir: Path,
    real_root: Path,
    phase115_dir: Path,
    phase116_dir: Path,
    candidate_roots: list[Path],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase115 = read_metric_table(base_dir / phase115_dir / "phase115_real_panel_refresh_acceptance_summary.csv")
    phase116 = read_metric_table(base_dir / phase116_dir / "phase116_profitability_verdict_acceptance_summary.csv")
    current_ready_days = as_int(metric_value(phase115, "phase115_phase110_ready_real_anchor_days"))

    roots = list(dict.fromkeys([real_root, *candidate_roots]))
    inventory = discover_local_panels(base_dir, roots)
    slots = build_acquisition_slots(current_ready_days)
    execution_plan = build_import_execution_plan(base_dir, current_ready_days)
    acceptance = build_acceptance_summary(phase115, phase116, inventory, slots)

    inventory.to_csv(output_dir / "local_real_l2_candidate_inventory.csv", index=False)
    slots.to_csv(output_dir / "real_l2_acquisition_slots.csv", index=False)
    execution_plan.to_csv(output_dir / "phase115_import_execution_plan.csv", index=False)
    acceptance.to_csv(output_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Local Real L2 Candidate Inventory": inventory,
            "Real L2 Acquisition Slots": slots,
            "Phase115 Import Execution Plan": execution_plan,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generated_utc": generated_utc,
        "scope": "phase117_real_anchor_acquisition_work_order",
        "current_ready_real_anchor_days": current_ready_days,
        "minimum_ready_real_days": MIN_READY_REAL_DAYS,
        "target_ready_real_days": TARGET_READY_REAL_DAYS,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase117",
            generated_utc=generated_utc,
            inputs={
                "phase115_acceptance": str(phase115_dir / "phase115_real_panel_refresh_acceptance_summary.csv"),
                "phase116_acceptance": str(phase116_dir / "phase116_profitability_verdict_acceptance_summary.csv"),
                "real_root": str(real_root),
                "candidate_roots": "|".join(str(root) for root in roots),
            },
            parameters={
                "minimum_ready_real_days": MIN_READY_REAL_DAYS,
                "target_ready_real_days": TARGET_READY_REAL_DAYS,
                "expected_symbols": "|".join(sorted(EXPECTED_SYMBOLS)),
                "data_layout_contract": "trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet",
                "strategy_policy": "no_strategy_replay_until_real_anchor_gate_reopens",
            },
            outputs={
                "local_real_l2_candidate_inventory": str(output_dir / "local_real_l2_candidate_inventory.csv"),
                "real_l2_acquisition_slots": str(output_dir / "real_l2_acquisition_slots.csv"),
                "phase115_import_execution_plan": str(output_dir / "phase115_import_execution_plan.csv"),
                "acceptance_summary": str(output_dir / "phase117_real_anchor_acquisition_acceptance_summary.csv"),
                "report": str(output_dir / "phase117_real_anchor_acquisition_work_order_report.md"),
                "manifest": str(output_dir / "phase117_real_anchor_acquisition_work_order_manifest.json"),
            },
            random_seed="none_deterministic_work_order",
            scenario_ids="phase117_real_anchor_expansion_work_order",
            cost_model_version="not_applicable_data_acquisition_gate",
            latency_model_version="not_applicable_data_acquisition_gate",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase117_real_anchor_acquisition_work_order_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase117 real-anchor acquisition/import work order.")
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--real-root", type=Path, default=DEFAULT_REAL_ROOT)
    parser.add_argument("--phase115-dir", type=Path, default=DEFAULT_PHASE115_DIR)
    parser.add_argument("--phase116-dir", type=Path, default=DEFAULT_PHASE116_DIR)
    parser.add_argument(
        "--candidate-root",
        type=Path,
        action="append",
        default=[Path("raw_l2"), Path("scratch_l2_sample_20260710_HDFCBANK")],
        help="Additional local root to scan for real L2 candidate panels. Can be passed multiple times.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase117(
        base_dir=args.base_dir,
        output_dir=args.output_dir,
        real_root=args.real_root,
        phase115_dir=args.phase115_dir,
        phase116_dir=args.phase116_dir,
        candidate_roots=args.candidate_root,
    )


if __name__ == "__main__":
    main()

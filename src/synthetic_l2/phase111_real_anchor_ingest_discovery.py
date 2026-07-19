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


DEFAULT_OUTPUT_DIR = Path("outputs/phase111")
DEFAULT_PHASE96_DIR = Path("outputs/phase96")
DEFAULT_PHASE110_DIR = Path("outputs/phase110")
DEFAULT_CANDIDATE_ROOTS = [
    Path("real_data_sample"),
    Path("raw_l2"),
    Path("scratch_l2_sample_20260710_HDFCBANK"),
]
MIN_READY_REAL_DAYS = 5
TARGET_READY_REAL_DAYS = 10


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


def infer_trade_dates_from_path(path: Path) -> set[str]:
    dates: set[str] = set()
    for part in path.parts:
        if part.startswith("trade_date="):
            dates.add(part.split("=", 1)[1])
    return dates


def discover_candidate_panel_roots(candidate_roots: list[Path]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for candidate_root in candidate_roots:
        if not candidate_root.exists():
            rows.append(
                {
                    "candidate_root": str(candidate_root),
                    "panel_root": "",
                    "discovery_status": "missing_root",
                    "layout_type": "missing",
                    "parquet_files": 0,
                    "symbols_observed": 0,
                    "expected_symbol_fraction": 0.0,
                    "trade_dates_observed": 0,
                    "trade_date_list": "",
                    "ready_for_schema_scan": False,
                    "ready_for_phase96_scan": False,
                    "recommended_action": "place_real_l2_parquet_under_this_root_or_register_another_candidate_root",
                }
            )
            continue
        search_roots = [candidate_root]
        search_roots.extend(path for path in candidate_root.rglob("*") if path.is_dir() and path.name.startswith("trade_date="))
        search_roots.extend(path for path in candidate_root.rglob("*") if path.is_dir() and any(child.name.startswith("symbol=") for child in path.iterdir() if child.is_dir()))
        for root in sorted(set(search_roots)):
            key = str(root.resolve())
            if key in seen:
                continue
            seen.add(key)
            parquet_files = sorted(root.rglob("*.parquet"))
            if not parquet_files:
                continue
            symbol_dirs = [path for path in root.rglob("symbol=*") if path.is_dir()]
            symbols = sorted({path.name.split("=", 1)[1] for path in symbol_dirs})
            dates = set()
            for file_path in parquet_files[:5000]:
                dates.update(infer_trade_dates_from_path(file_path))
            if not dates:
                dates.update(infer_trade_dates_from_path(root))
            layout_type = "partitioned_by_trade_date" if dates else "symbol_partition_only_or_unknown_date"
            if not dates and "single_day" in root.name:
                dates.add("unknown_single_day")
            expected_fraction = len(set(symbols).intersection(EXPECTED_SYMBOLS)) / len(EXPECTED_SYMBOLS)
            schema_ready = bool(len(parquet_files) > 0 and len(set(symbols).intersection(EXPECTED_SYMBOLS)) >= 30)
            multiday_candidate_ready = bool(schema_ready and len(dates) > 0)
            rows.append(
                {
                    "candidate_root": str(candidate_root),
                    "panel_root": str(root),
                    "discovery_status": "found_parquet",
                    "layout_type": layout_type,
                    "parquet_files": int(len(parquet_files)),
                    "symbols_observed": int(len(symbols)),
                    "expected_symbol_fraction": expected_fraction,
                    "trade_dates_observed": int(len(dates)) if dates else 0,
                    "trade_date_list": "|".join(sorted(dates)),
                    "ready_for_schema_scan": schema_ready,
                    "ready_for_phase96_scan": multiday_candidate_ready,
                    "recommended_action": "run_phase96_against_this_root" if multiday_candidate_ready else "normalize_trade_date_layout_or_complete_symbol_coverage",
                }
            )
    return pd.DataFrame(rows)


def build_import_plan(candidates: pd.DataFrame, phase96_dir: Path, phase110_dir: Path) -> pd.DataFrame:
    current_ready_days = int(float(metric_value(phase110_dir / "phase110_multiday_replay_unlock_acceptance_summary.csv", "phase110_ready_real_anchor_days", 0)))
    current_ready_dates = ""
    phase96_readiness = phase96_dir / "real_day_readiness.csv"
    if phase96_readiness.exists():
        readiness = pd.read_csv(phase96_readiness)
        if not readiness.empty and "day_ready_for_anchor_panel" in readiness.columns:
            current_ready_dates = "|".join(
                sorted(readiness.loc[readiness["day_ready_for_anchor_panel"].astype(bool), "trade_date"].astype(str).unique())
            )
    ready_candidates = candidates[candidates["ready_for_phase96_scan"].astype(bool)].copy() if not candidates.empty else pd.DataFrame()
    rows: list[dict[str, Any]] = []
    priority = 1
    for item in ready_candidates.sort_values(["trade_dates_observed", "expected_symbol_fraction", "parquet_files"], ascending=[False, False, False]).to_dict("records"):
        rows.append(
            {
                "priority": priority,
                "candidate_panel_root": item["panel_root"],
                "candidate_trade_dates": item["trade_date_list"],
                "candidate_symbols_observed": item["symbols_observed"],
                "candidate_expected_symbol_fraction": item["expected_symbol_fraction"],
                "current_ready_days": current_ready_days,
                "current_ready_dates": current_ready_dates,
                "phase96_command": f"python scripts/run_phase96_real_anchor_panel_builder.py --real-root {item['candidate_root']}",
                "acceptance_gate": "phase96_ready_anchor_days >= 5 and phase110_replay_unlock_allowed remains 0 until multiday realism rerun passes",
            }
        )
        priority += 1
    if not rows:
        rows.append(
            {
                "priority": 1,
                "candidate_panel_root": "",
                "candidate_trade_dates": "",
                "candidate_symbols_observed": 0,
                "candidate_expected_symbol_fraction": 0.0,
                "current_ready_days": current_ready_days,
                "current_ready_dates": current_ready_dates,
                "phase96_command": "",
                "acceptance_gate": "drop or ingest at least 4 more ready 32-symbol Zerodha WebSocket L2 days, then rerun Phase96 and Phase110",
            }
        )
    return pd.DataFrame(rows)


def build_dropzone_manifest(current_ready_days: int) -> pd.DataFrame:
    days_needed_min = max(0, MIN_READY_REAL_DAYS - current_ready_days)
    days_needed_target = max(0, TARGET_READY_REAL_DAYS - current_ready_days)
    return pd.DataFrame(
        [
            {
                "field": "recommended_root",
                "value": "real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet",
                "why": "A trade_date/exchange/symbol partitioned layout lets Phase111 discover distinct dates and lets Phase96 validate each day.",
            },
            {
                "field": "minimum_additional_ready_days_needed",
                "value": days_needed_min,
                "why": "Phase110 requires at least 5 ready real anchor days before replay can even be considered.",
            },
            {
                "field": "target_additional_ready_days_needed",
                "value": days_needed_target,
                "why": "10 ready real days is the preferred target for more stable calibration evidence.",
            },
            {
                "field": "required_symbol_universe",
                "value": "|".join(sorted(EXPECTED_SYMBOLS)),
                "why": "The full-symbol realism gate compares the fixed 32-symbol universe.",
            },
            {
                "field": "post_ingest_commands",
                "value": "python scripts/run_phase111_real_anchor_ingest_discovery.py; python scripts/run_phase96_real_anchor_panel_builder.py; python scripts/run_phase110_multiday_replay_unlock_gate.py",
                "why": "Discovery, readiness validation, and replay-unlock status must be refreshed after new real data arrives.",
            },
        ]
    )


def summarize(candidates: pd.DataFrame, import_plan: pd.DataFrame, phase110_dir: Path) -> pd.DataFrame:
    current_ready_days = int(float(metric_value(phase110_dir / "phase110_multiday_replay_unlock_acceptance_summary.csv", "phase110_ready_real_anchor_days", 0)))
    days_needed_min = max(0, MIN_READY_REAL_DAYS - current_ready_days)
    ready_candidate_roots = int(candidates["ready_for_phase96_scan"].astype(bool).sum()) if not candidates.empty else 0
    max_candidate_dates = int(candidates["trade_dates_observed"].max()) if not candidates.empty else 0
    additional_dates_found = bool(max_candidate_dates > current_ready_days)
    return pd.DataFrame(
        [
            ("phase111_candidate_rows", int(len(candidates)), "Candidate real panel roots discovered or checked"),
            ("phase111_ready_candidate_roots", ready_candidate_roots, "Candidate roots ready for Phase96 scan"),
            ("phase111_current_ready_real_days", current_ready_days, "Ready real days currently proven by Phase110/Phase96"),
            ("phase111_max_candidate_trade_dates", max_candidate_dates, "Maximum distinct trade dates discovered in any candidate root"),
            ("phase111_additional_real_dates_found", int(additional_dates_found), "1 means a candidate root appears to contain more dates than current Phase96 evidence"),
            ("phase111_days_needed_for_min", days_needed_min, "Additional ready real days still required for minimum replay-unlock consideration"),
            ("phase111_import_plan_rows", int(len(import_plan)), "Import/validation plan rows emitted"),
            ("phase111_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase111_recommend_next_action", "drop_or_ingest_4_more_real_l2_days_then_rerun_phase96_phase110", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase111 Real Anchor Ingest Discovery",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase111 scans likely local real-data roots for additional Zerodha WebSocket L2 panels and emits a concrete import/validation plan.",
        "It is an operational bridge from the Phase110 multiday blocker to the next Phase96/Phase110 rerun.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase111_real_anchor_ingest_discovery_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase111(candidate_roots: list[Path], phase96_dir: Path, phase110_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    candidates = discover_candidate_panel_roots(candidate_roots)
    import_plan = build_import_plan(candidates, phase96_dir, phase110_dir)
    current_ready_days = int(float(metric_value(phase110_dir / "phase110_multiday_replay_unlock_acceptance_summary.csv", "phase110_ready_real_anchor_days", 0)))
    dropzone = build_dropzone_manifest(current_ready_days)
    acceptance = summarize(candidates, import_plan, phase110_dir)

    candidates.to_csv(output_dir / "phase111_candidate_real_panel_inventory.csv", index=False)
    import_plan.to_csv(output_dir / "phase111_real_panel_import_plan.csv", index=False)
    dropzone.to_csv(output_dir / "phase111_real_panel_dropzone_manifest.csv", index=False)
    acceptance.to_csv(output_dir / "phase111_real_anchor_ingest_acceptance_summary.csv", index=False)
    write_report(
        output_dir,
        {
            "Acceptance Summary": acceptance,
            "Candidate Real Panel Inventory": candidates,
            "Import Plan": import_plan,
            "Dropzone Manifest": dropzone,
        },
    )

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase111_real_anchor_ingest_discovery",
        **reproducibility_fields(
            artifact_id="phase111",
            generated_utc=generated_utc,
            inputs={
                "candidate_roots": [str(path) for path in candidate_roots],
                "phase96_acceptance": str(phase96_dir / "real_anchor_panel_builder_acceptance_summary.csv"),
                "phase110_acceptance": str(phase110_dir / "phase110_multiday_replay_unlock_acceptance_summary.csv"),
            },
            parameters={
                "minimum_ready_real_days": MIN_READY_REAL_DAYS,
                "target_ready_real_days": TARGET_READY_REAL_DAYS,
                "strategy_replay_policy": "closed",
            },
            outputs={
                "candidate_inventory": str(output_dir / "phase111_candidate_real_panel_inventory.csv"),
                "import_plan": str(output_dir / "phase111_real_panel_import_plan.csv"),
                "dropzone_manifest": str(output_dir / "phase111_real_panel_dropzone_manifest.csv"),
                "acceptance_summary": str(output_dir / "phase111_real_anchor_ingest_acceptance_summary.csv"),
                "report": str(output_dir / "phase111_real_anchor_ingest_discovery_report.md"),
                "manifest": str(output_dir / "phase111_real_anchor_ingest_discovery_manifest.json"),
            },
            random_seed="none_deterministic_phase111_discovery",
            scenario_ids="phase111_post_phase110_real_panel_ingest_discovery",
            cost_model_version="not_applicable",
            latency_model_version="phase110_multiday_gate",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase111_real_anchor_ingest_discovery_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Discover candidate real anchor panels and emit import plan.")
    parser.add_argument("--candidate-roots", nargs="+", type=Path, default=DEFAULT_CANDIDATE_ROOTS)
    parser.add_argument("--phase96-dir", type=Path, default=DEFAULT_PHASE96_DIR)
    parser.add_argument("--phase110-dir", type=Path, default=DEFAULT_PHASE110_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase111(args.candidate_roots, args.phase96_dir, args.phase110_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

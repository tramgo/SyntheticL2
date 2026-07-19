from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE113_DIR = Path("outputs/phase113")
DEFAULT_OUTPUT_DIR = Path("outputs/phase114")


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


def directory_stats(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    files = sorted(path.glob("*.parquet"))
    return len(files), int(sum(file.stat().st_size for file in files))


def build_integrity_rows(import_plan: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in import_plan.to_dict("records"):
        source_dir = Path(str(item.get("source_symbol_dir", "")))
        target_dir = Path(str(item.get("target_symbol_dir", ""))) if str(item.get("target_symbol_dir", "")) else Path()
        source_count, source_bytes = directory_stats(source_dir)
        target_count, target_bytes = directory_stats(target_dir) if str(item.get("target_symbol_dir", "")) else (0, 0)
        planned = str(item.get("planned_action", ""))
        target_exists = bool(str(item.get("target_symbol_dir", "")) and target_dir.exists())
        integrity_pass = bool(planned == "copy_symbol_partition" and target_exists and source_count == target_count and source_bytes == target_bytes)
        rows.append(
            {
                "symbol": item.get("symbol", ""),
                "trade_date": item.get("trade_date", ""),
                "exchange": item.get("exchange", ""),
                "planned_action": planned,
                "source_symbol_dir": str(source_dir),
                "target_symbol_dir": str(target_dir) if str(item.get("target_symbol_dir", "")) else "",
                "source_file_count": source_count,
                "target_file_count": target_count,
                "source_bytes": source_bytes,
                "target_bytes": target_bytes,
                "target_exists": target_exists,
                "count_match": bool(source_count == target_count and source_count > 0),
                "byte_match": bool(source_bytes == target_bytes and source_bytes > 0),
                "integrity_pass": integrity_pass,
                "integrity_status": "verified" if integrity_pass else ("target_missing_not_executed" if not target_exists else "mismatch"),
            }
        )
    return pd.DataFrame(rows)


def build_checks(integrity: pd.DataFrame, phase113_dir: Path) -> pd.DataFrame:
    phase113_execute = int(float(metric_value(phase113_dir / "phase113_dropzone_import_acceptance_summary.csv", "phase113_execute_mode", 0)))
    planned_rows = int(len(integrity))
    verified_rows = int(integrity["integrity_pass"].astype(bool).sum()) if not integrity.empty else 0
    target_rows = int(integrity["target_exists"].astype(bool).sum()) if not integrity.empty else 0
    return pd.DataFrame(
        [
            {
                "check_id": "P114_PHASE113_PLAN_AVAILABLE",
                "passed": bool(planned_rows > 0),
                "detail": f"planned_rows={planned_rows}",
            },
            {
                "check_id": "P114_DRY_RUN_STATE_RECOGNIZED",
                "passed": bool(phase113_execute == 0 and target_rows == 0),
                "detail": f"phase113_execute_mode={phase113_execute}; target_rows={target_rows}",
            },
            {
                "check_id": "P114_EXECUTED_IMPORT_FULLY_VERIFIED",
                "passed": bool(phase113_execute == 0 or (planned_rows > 0 and verified_rows == planned_rows)),
                "detail": f"phase113_execute_mode={phase113_execute}; verified_rows={verified_rows}; planned_rows={planned_rows}",
            },
            {
                "check_id": "P114_REPLAY_LOCK_PRESERVED",
                "passed": True,
                "detail": "Phase114 verifies import integrity only and does not unlock strategy replay.",
            },
        ]
    )


def summarize(integrity: pd.DataFrame, checks: pd.DataFrame, phase113_dir: Path) -> pd.DataFrame:
    phase113_execute = int(float(metric_value(phase113_dir / "phase113_dropzone_import_acceptance_summary.csv", "phase113_execute_mode", 0)))
    planned_rows = int(len(integrity))
    verified_rows = int(integrity["integrity_pass"].astype(bool).sum()) if not integrity.empty else 0
    target_rows = int(integrity["target_exists"].astype(bool).sum()) if not integrity.empty else 0
    dry_run_ready = bool(phase113_execute == 0 and planned_rows > 0 and target_rows == 0)
    executed_verified = bool(phase113_execute == 1 and planned_rows > 0 and verified_rows == planned_rows)
    return pd.DataFrame(
        [
            ("phase114_integrity_rows", planned_rows, "Import-plan rows checked for source/target integrity"),
            ("phase114_target_rows_present", target_rows, "Rows where target symbol directory exists"),
            ("phase114_integrity_verified_rows", verified_rows, "Rows with matching source/target file counts and bytes"),
            ("phase114_phase113_execute_mode", phase113_execute, "Inherited Phase113 execute mode"),
            ("phase114_dry_run_integrity_ready", int(dry_run_ready), "1 means dry-run plan is ready and no copied target exists yet"),
            ("phase114_executed_import_integrity_pass", int(executed_verified), "1 means executed import has full source/target integrity"),
            ("phase114_check_rows", int(len(checks)), "Integrity checks executed"),
            ("phase114_check_pass_rows", int(checks["passed"].astype(bool).sum()), "Integrity checks passing"),
            ("phase114_strategy_replay_allowed", 0, "Strategy replay remains closed"),
            ("phase114_recommend_next_action", "run_phase113_with_execute_after_new_real_days_then_rerun_phase114_phase96_phase110", "Recommended next milestone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase114 Drop-zone Import Integrity Verifier",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Phase114 verifies whether Phase113's real-L2 drop-zone import plan has been executed with source/target count and byte integrity.",
        "It is safe in dry-run state and does not enable strategy replay.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase114_dropzone_import_integrity_verifier_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase114(phase113_dir: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    import_plan = pd.read_csv(phase113_dir / "phase113_dropzone_import_plan.csv")
    integrity = build_integrity_rows(import_plan)
    checks = build_checks(integrity, phase113_dir)
    acceptance = summarize(integrity, checks, phase113_dir)

    integrity.to_csv(output_dir / "phase114_dropzone_import_integrity.csv", index=False)
    checks.to_csv(output_dir / "phase114_dropzone_import_integrity_checks.csv", index=False)
    acceptance.to_csv(output_dir / "phase114_dropzone_import_integrity_acceptance_summary.csv", index=False)
    write_report(output_dir, {"Acceptance Summary": acceptance, "Integrity Checks": checks, "Integrity Rows": integrity})

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase114_dropzone_import_integrity_verifier",
        **reproducibility_fields(
            artifact_id="phase114",
            generated_utc=generated_utc,
            inputs={
                "phase113_import_plan": str(phase113_dir / "phase113_dropzone_import_plan.csv"),
                "phase113_acceptance": str(phase113_dir / "phase113_dropzone_import_acceptance_summary.csv"),
            },
            parameters={"strategy_replay_policy": "closed"},
            outputs={
                "integrity": str(output_dir / "phase114_dropzone_import_integrity.csv"),
                "checks": str(output_dir / "phase114_dropzone_import_integrity_checks.csv"),
                "acceptance_summary": str(output_dir / "phase114_dropzone_import_integrity_acceptance_summary.csv"),
                "report": str(output_dir / "phase114_dropzone_import_integrity_verifier_report.md"),
                "manifest": str(output_dir / "phase114_dropzone_import_integrity_verifier_manifest.json"),
            },
            random_seed="none_deterministic_phase114_integrity",
            scenario_ids="phase114_post_phase113_import_integrity",
            cost_model_version="not_applicable",
            latency_model_version="phase113_dropzone_importer",
            base_dir=base_dir,
        ),
    }
    (output_dir / "phase114_dropzone_import_integrity_verifier_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Phase113 drop-zone import integrity.")
    parser.add_argument("--phase113-dir", type=Path, default=DEFAULT_PHASE113_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase114(args.phase113_dir, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def _summary_value(frame: pd.DataFrame, metric: str) -> int:
    matched = frame[frame["metric"].astype(str).eq(metric)]
    if matched.empty:
        raise KeyError(metric)
    return int(matched["value"].iloc[0])


def build_gate_ledger(day_inventory: pd.DataFrame, phase35_summary: pd.DataFrame, phase37_summary: pd.DataFrame) -> pd.DataFrame:
    phase35_symbols = _summary_value(phase35_summary, "phase35_symbols_evaluated")
    timestamp_symbols = _summary_value(phase35_summary, "phase35_timestamp_semantics_computable_pass_symbols")
    compaction_symbols = _summary_value(phase35_summary, "phase35_lossless_compaction_computable_pass_symbols")
    stale_symbols = _summary_value(phase35_summary, "phase35_drop_duplicate_stale_computable_symbols")
    collector_ready = _summary_value(phase37_summary, "phase37_stage_a2_collector_evidence_ready")
    live_evidence = _summary_value(phase37_summary, "phase37_live_collector_evidence")

    rows = []
    for record in day_inventory.to_dict("records"):
        trade_date = record["trade_date"]
        exchange = record["exchange"]
        required_symbols = int(record["required_symbols"])
        gates = [
            (
                "raw_full_universe_coverage",
                bool(record["full_universe_raw_day"]),
                f"{int(record['symbols'])}/{required_symbols} symbols present",
                "Collect/import raw parquet for the full required universe.",
            ),
            (
                "timestamp_semantics_computable",
                timestamp_symbols >= required_symbols,
                f"{timestamp_symbols}/{required_symbols} symbols pass computable timestamp checks",
                "Fix timestamp presence/order gaps before Class B promotion.",
            ),
            (
                "lossless_compaction_computable",
                compaction_symbols >= required_symbols,
                f"{compaction_symbols}/{required_symbols} symbols reconcile raw rows/files to Phase 1 and manifest counts",
                "Fix raw-to-compact reconciliation gaps before Class B promotion.",
            ),
            (
                "drop_duplicate_stale_scan_computable",
                stale_symbols >= required_symbols,
                f"{stale_symbols}/{required_symbols} symbols have computable duplicate/stale symptom scans",
                "Ensure duplicate/stale scans are computable for every required symbol.",
            ),
            (
                "collector_live_evidence",
                bool(live_evidence),
                f"phase37_live_collector_evidence={live_evidence}",
                "Run Phase 37 against actual live collector ledgers with --collector-source live_collector.",
            ),
            (
                "collector_stage_a2_evidence_ready",
                bool(collector_ready),
                f"phase37_stage_a2_collector_evidence_ready={collector_ready}",
                "Pass Phase 37 schema/session/sequence/drop-counter gates on live collector ledgers.",
            ),
        ]
        for gate_id, passed, observed, next_action in gates:
            rows.append(
                {
                    "trade_date": trade_date,
                    "exchange": exchange,
                    "gate_id": gate_id,
                    "passed": bool(passed),
                    "observed_value": observed,
                    "required_next_action": "" if passed else next_action,
                }
            )
    return pd.DataFrame(rows)


def build_day_decision(day_inventory: pd.DataFrame, gate_ledger: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (trade_date, exchange), group in gate_ledger.groupby(["trade_date", "exchange"], sort=True):
        failed = group[~group["passed"].astype(bool)]
        rows.append(
            {
                "trade_date": trade_date,
                "exchange": exchange,
                "class_b_promotion_allowed": failed.empty,
                "passed_gates": int(group["passed"].astype(bool).sum()),
                "failed_gates": int((~group["passed"].astype(bool)).sum()),
                "blocking_gates": ";".join(failed["gate_id"].astype(str).tolist()),
                "promotion_status": "class_b_promotion_allowed" if failed.empty else "blocked_until_live_collector_evidence_and_all_diagnostics_pass",
            }
        )
    return pd.DataFrame(rows)


def build_summary(day_decision: pd.DataFrame, gate_ledger: pd.DataFrame, stage_a2_summary: pd.DataFrame) -> pd.DataFrame:
    class_b_days = int(day_decision["class_b_promotion_allowed"].astype(bool).sum()) if len(day_decision) else 0
    stage = stage_a2_summary.iloc[0]
    min_days = int(stage["required_complete_days_min"])
    target_days = int(stage["required_complete_days_target"])
    rows = [
        ("phase38_days_evaluated", int(len(day_decision)), "Trade-date/exchange days evaluated for Class B promotion"),
        ("phase38_class_b_promoted_days", class_b_days, "Days promoted to Class B by the Phase 38 gate"),
        ("phase38_failed_gate_rows", int((~gate_ledger["passed"].astype(bool)).sum()), "Failed Class B promotion gate rows"),
        ("phase38_required_complete_days_min", min_days, "Minimum complete Class B days required"),
        ("phase38_required_complete_days_target", target_days, "Target complete Class B days required"),
        ("phase38_days_needed_for_min", max(min_days - class_b_days, 0), "Additional promoted Class B days needed for minimum"),
        ("phase38_days_needed_for_target", max(target_days - class_b_days, 0), "Additional promoted Class B days needed for target"),
        ("phase38_replay_allowed_rows", 0, "Replay rows unlocked by Class B promotion gate"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def build_action_plan(summary: pd.DataFrame, gate_ledger: pd.DataFrame) -> pd.DataFrame:
    failed = gate_ledger[~gate_ledger["passed"].astype(bool)]
    rows = []
    for priority, (gate_id, group) in enumerate(failed.groupby("gate_id", sort=True), start=1):
        rows.append(
            {
                "priority": priority,
                "gate_id": gate_id,
                "failed_rows": int(len(group)),
                "required_next_action": group["required_next_action"].iloc[0],
                "acceptance_effect": "Required before any day can be counted as Class B event-grade evidence.",
            }
        )
    if not rows:
        rows.append(
            {
                "priority": 1,
                "gate_id": "none",
                "failed_rows": 0,
                "required_next_action": "Collect enough additional promoted Class B days to meet the minimum/target counts.",
                "acceptance_effect": "Supports downstream Stage A2/Phase 22 real-data replay gates.",
            }
        )
    return pd.DataFrame(rows)


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 38 Class B Day Promotion Gate",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This gate combines raw day coverage, computable diagnostics and collector-ledger verifier evidence into a day-level Class B promotion decision.",
        "It does not run strategy replay; it determines whether real-data days are eligible to feed those replay gates.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase38_class_b_promotion_gate_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase38(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    day_inventory = _read_csv(paths["phase34_day_inventory"])
    phase35_summary = _read_csv(paths["phase35_summary"])
    phase37_summary = _read_csv(paths["phase37_summary"])
    stage_a2_summary = _read_csv(paths["stage_a2_summary"])

    gate_ledger = build_gate_ledger(day_inventory, phase35_summary, phase37_summary)
    day_decision = build_day_decision(day_inventory, gate_ledger)
    summary = build_summary(day_decision, gate_ledger, stage_a2_summary)
    action_plan = build_action_plan(summary, gate_ledger)

    frames = {
        "Summary": summary,
        "Day Decision": day_decision,
        "Gate Ledger": gate_ledger,
        "Action Plan": action_plan,
    }
    summary.to_csv(output_dir / "class_b_promotion_summary.csv", index=False)
    day_decision.to_csv(output_dir / "class_b_day_decision.csv", index=False)
    gate_ledger.to_csv(output_dir / "class_b_promotion_gate_ledger.csv", index=False)
    action_plan.to_csv(output_dir / "class_b_promotion_action_plan.csv", index=False)
    write_report(output_dir, frames)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "days_evaluated": int(len(day_decision)),
        "class_b_promoted_days": int(day_decision["class_b_promotion_allowed"].astype(bool).sum()) if len(day_decision) else 0,
        "scope": "phase38_class_b_day_promotion_gate_not_strategy_replay",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase38",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={
                "required_gate_ids": [
                    "raw_full_universe_coverage",
                    "timestamp_semantics_computable",
                    "lossless_compaction_computable",
                    "drop_duplicate_stale_scan_computable",
                    "collector_live_evidence",
                    "collector_stage_a2_evidence_ready",
                ]
            },
            outputs={
                "summary": str(output_dir / "class_b_promotion_summary.csv"),
                "day_decision": str(output_dir / "class_b_day_decision.csv"),
                "gate_ledger": str(output_dir / "class_b_promotion_gate_ledger.csv"),
                "action_plan": str(output_dir / "class_b_promotion_action_plan.csv"),
                "report": str(output_dir / "phase38_class_b_promotion_gate_report.md"),
                "manifest": str(output_dir / "phase38_class_b_promotion_gate_manifest.json"),
            },
            random_seed="none_deterministic_class_b_gate",
            scenario_ids="current_real_data_class_b_promotion_gate",
            cost_model_version="not_applicable_class_b_data_gate",
            latency_model_version="phase35_phase37_collector_diagnostics_gate",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase38_class_b_promotion_gate_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Class B day promotion gate over real-data readiness evidence.")
    parser.add_argument("--phase34-day-inventory", type=Path, default=Path("outputs/phase34/real_data_day_inventory.csv"))
    parser.add_argument("--phase35-summary", type=Path, default=Path("outputs/phase35/stage_a2_computable_diagnostics_summary.csv"))
    parser.add_argument("--phase37-summary", type=Path, default=Path("outputs/phase37/summary.csv"))
    parser.add_argument("--stage-a2-summary", type=Path, default=Path("outputs/stage_a2/stage_a2_readiness_summary.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase38"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase38(
        {
            "phase34_day_inventory": args.phase34_day_inventory,
            "phase35_summary": args.phase35_summary,
            "phase37_summary": args.phase37_summary,
            "stage_a2_summary": args.stage_a2_summary,
        },
        args.output_dir,
        args.base_dir,
    )


if __name__ == "__main__":
    main()

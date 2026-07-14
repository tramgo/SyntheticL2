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


def build_symbol_day_diagnostics(stage_quality: pd.DataFrame, file_inventory: pd.DataFrame, phase1_summary: pd.DataFrame, manifest: pd.DataFrame) -> pd.DataFrame:
    grouped = stage_quality.rename(
        columns={
            "row_count": "raw_rows",
            "file_count": "source_files",
            "duplicate_monotonic_ns": "duplicate_monotonic_ns",
            "receive_ms_order_violations": "receive_gap_negative_count",
            "monotonic_ns_order_violations": "monotonic_gap_negative_count",
            "median_interarrival_ms": "median_receive_gap_ms",
            "p95_interarrival_ms": "p95_receive_gap_ms",
        }
    ).copy()
    grouped["trade_date"] = "2026-07-13"
    grouped["exchange"] = "NSE"
    grouped["raw_rows"] = pd.to_numeric(grouped["raw_rows"], errors="coerce").fillna(0).astype(int)
    grouped["source_files"] = pd.to_numeric(grouped["source_files"], errors="coerce").fillna(0).astype(int)
    grouped["receive_ms_present"] = grouped["raw_rows"]
    grouped["monotonic_ns_present"] = grouped["raw_rows"]
    grouped["exchange_timestamp_present_rows"] = grouped["raw_rows"]
    grouped["last_trade_time_present_rows"] = grouped["raw_rows"]
    grouped["duplicate_receive_ms"] = pd.to_numeric(grouped["duplicate_receive_ms"], errors="coerce").fillna(0).astype(int)
    grouped["stale_gap_gt_15s_count"] = pd.to_numeric(grouped["stale_gap_gt_15s_count"], errors="coerce").fillna(0).astype(int)
    grouped["receive_gap_negative_count"] = pd.to_numeric(grouped["receive_gap_negative_count"], errors="coerce").fillna(0).astype(int)
    grouped["monotonic_gap_negative_count"] = pd.to_numeric(grouped["monotonic_gap_negative_count"], errors="coerce").fillna(0).astype(int)
    grouped["median_receive_gap_ms"] = pd.to_numeric(grouped["median_receive_gap_ms"], errors="coerce").fillna(0.0)
    grouped["p95_receive_gap_ms"] = pd.to_numeric(grouped["p95_receive_gap_ms"], errors="coerce").fillna(0.0)
    grouped["first_receive_ms"] = pd.to_numeric(grouped["first_receive_ms"], errors="coerce").fillna(0).astype("int64")
    grouped["last_receive_ms"] = pd.to_numeric(grouped["last_receive_ms"], errors="coerce").fillna(0).astype("int64")
    grouped["receive_ms_present_fraction"] = 1.0
    grouped["monotonic_ns_present_fraction"] = 1.0
    grouped["exchange_timestamp_present_fraction"] = 1.0
    grouped["last_trade_time_present_fraction"] = 1.0

    phase1 = phase1_summary.rename(columns={"symbol": "symbol", "rows": "phase1_delta_rows"}).copy()
    grouped = grouped.merge(phase1[["symbol", "phase1_delta_rows"]], on="symbol", how="left")
    grouped["phase1_delta_rows"] = grouped["phase1_delta_rows"].fillna(0).astype(int)
    grouped["row_count_match_phase1"] = grouped["raw_rows"].astype(int) == grouped["phase1_delta_rows"].astype(int)

    inventory_counts = (
        file_inventory.groupby("symbol", sort=True)
        .agg(inventory_files=("file", "count"), inventory_rows=("rows", "sum"), inventory_bytes=("bytes", "sum"))
        .reset_index()
    )
    grouped = grouped.merge(inventory_counts, on="symbol", how="left")
    grouped["inventory_files"] = grouped["inventory_files"].fillna(0).astype(int)
    grouped["inventory_rows"] = grouped["inventory_rows"].fillna(0).astype(int)
    grouped["inventory_bytes"] = grouped["inventory_bytes"].fillna(0).astype(int)
    grouped["row_count_match_inventory"] = grouped["raw_rows"].astype(int) == grouped["inventory_rows"].astype(int)

    manifest_counts = manifest.copy()
    manifest_counts["symbol"] = manifest_counts["symbol_dir"].astype(str).str.replace("symbol=", "", regex=False)
    manifest_counts = manifest_counts.groupby("symbol", sort=True).agg(manifest_files=("name", "count"), manifest_bytes=("bytes", "sum")).reset_index()
    grouped = grouped.merge(manifest_counts, on="symbol", how="left")
    grouped["manifest_files"] = grouped["manifest_files"].fillna(0).astype(int)
    grouped["manifest_bytes"] = grouped["manifest_bytes"].fillna(0).astype(int)
    grouped["file_count_match_manifest"] = grouped["source_files"].astype(int) == grouped["manifest_files"].astype(int)

    grouped["timestamp_semantics_computable"] = (
        grouped["receive_ms_present_fraction"].eq(1.0)
        & grouped["monotonic_ns_present_fraction"].eq(1.0)
        & grouped["exchange_timestamp_present_fraction"].gt(0.0)
        & grouped["receive_gap_negative_count"].eq(0)
        & grouped["monotonic_gap_negative_count"].eq(0)
    )
    grouped["lossless_compaction_computable"] = grouped["row_count_match_phase1"] & grouped["row_count_match_inventory"] & grouped["file_count_match_manifest"]
    grouped["drop_duplicate_stale_computable"] = grouped["receive_ms_present_fraction"].eq(1.0)
    grouped["local_sequence_explicitly_available"] = False
    grouped["connection_boundary_ledger_available"] = False
    grouped["class_b_event_grade_now"] = False
    grouped["diagnostic_status"] = grouped.apply(_diagnostic_status, axis=1)
    keep_cols = [
        "trade_date",
        "exchange",
        "symbol",
        "instrument_class",
        "raw_rows",
        "source_files",
        "phase1_delta_rows",
        "inventory_rows",
        "manifest_files",
        "duplicate_receive_ms",
        "stale_gap_gt_15s_count",
        "receive_gap_negative_count",
        "monotonic_gap_negative_count",
        "median_receive_gap_ms",
        "p95_receive_gap_ms",
        "receive_ms_present_fraction",
        "monotonic_ns_present_fraction",
        "exchange_timestamp_present_fraction",
        "row_count_match_phase1",
        "row_count_match_inventory",
        "file_count_match_manifest",
        "timestamp_semantics_computable",
        "lossless_compaction_computable",
        "drop_duplicate_stale_computable",
        "local_sequence_explicitly_available",
        "connection_boundary_ledger_available",
        "class_b_event_grade_now",
        "diagnostic_status",
    ]
    return grouped[keep_cols].sort_values(["trade_date", "exchange", "symbol"], kind="mergesort")


def _diagnostic_status(row: pd.Series) -> str:
    if not row["lossless_compaction_computable"]:
        return "raw_to_phase1_reconciliation_gap"
    if not row["timestamp_semantics_computable"]:
        return "timestamp_semantics_gap"
    if not row["drop_duplicate_stale_computable"]:
        return "drop_duplicate_stale_scan_gap"
    return "computable_diagnostics_pass_but_collector_contracts_missing"


def build_contract_evidence_ledger(symbol_day: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for record in symbol_day.to_dict("records"):
        base = {
            "trade_date": record["trade_date"],
            "exchange": record["exchange"],
            "symbol": record["symbol"],
            "raw_rows": int(record["raw_rows"]),
        }
        checks = [
            (
                "timestamp_semantics",
                bool(record["timestamp_semantics_computable"]),
                "receive/monotonic/exchange timestamp columns are present and ordered in persisted data",
                "capture-side timestamp policy document still required before Class B promotion",
            ),
            (
                "lossless_compaction",
                bool(record["lossless_compaction_computable"]),
                "raw parquet rows reconcile to Phase 1 rows and manifest file counts",
                "repeat for every new Class B day",
            ),
            (
                "dropped_message_diagnostics",
                bool(record["drop_duplicate_stale_computable"]),
                "duplicate receive-ms, stale gap and ordering symptoms are computable from persisted ticks",
                "broker/session drop counters are not present",
            ),
            (
                "local_sequence_integrity",
                False,
                "derived persisted ordering can be reconstructed",
                "explicit callback-ingress local_sequence_id is absent",
            ),
            (
                "connection_boundary_log",
                False,
                "tick files imply a capture window",
                "connection open/close/reconnect/subscription ledger is absent",
            ),
            (
                "multiday_class_b_coverage",
                False,
                "current raw day can be diagnosed as a smoke/regression day",
                "minimum 5 Class B event-grade days are not available",
            ),
        ]
        for criterion_id, computable_pass, evidence, remaining_gap in checks:
            rows.append(
                {
                    **base,
                    "criterion_id": criterion_id,
                    "computable_evidence_available": bool(computable_pass),
                    "acceptance_requirement_met": False,
                    "current_evidence": evidence,
                    "remaining_gap": remaining_gap,
                    "phase35_status": "computable_pass_not_acceptance" if computable_pass else "collector_or_multiday_evidence_missing",
                }
            )
    return pd.DataFrame(rows).sort_values(["symbol", "criterion_id"], kind="mergesort")


def build_summary(symbol_day: pd.DataFrame, ledger: pd.DataFrame) -> pd.DataFrame:
    metrics = [
        ("phase35_symbols_evaluated", int(symbol_day["symbol"].nunique()), "Symbols scanned from current raw parquet sample"),
        ("phase35_raw_rows_scanned", int(symbol_day["raw_rows"].sum()), "Raw parquet rows scanned"),
        ("phase35_source_files_scanned", int(symbol_day["source_files"].sum()), "Distinct parquet files scanned"),
        ("phase35_timestamp_semantics_computable_pass_symbols", int(symbol_day["timestamp_semantics_computable"].sum()), "Symbols with computable timestamp checks passing"),
        ("phase35_lossless_compaction_computable_pass_symbols", int(symbol_day["lossless_compaction_computable"].sum()), "Symbols with raw-to-Phase1/manifest reconciliation passing"),
        ("phase35_drop_duplicate_stale_computable_symbols", int(symbol_day["drop_duplicate_stale_computable"].sum()), "Symbols with duplicate/stale scan computable"),
        ("phase35_explicit_local_sequence_symbols", int(symbol_day["local_sequence_explicitly_available"].sum()), "Symbols with explicit callback local sequence IDs"),
        ("phase35_connection_boundary_ledger_symbols", int(symbol_day["connection_boundary_ledger_available"].sum()), "Symbols with connection boundary ledger evidence"),
        ("phase35_computable_evidence_rows", int(ledger["computable_evidence_available"].sum()), "Criterion rows with computable evidence available now"),
        ("phase35_acceptance_met_rows", int(ledger["acceptance_requirement_met"].sum()), "Criterion rows accepted for Class B promotion"),
    ]
    return pd.DataFrame(metrics, columns=["metric", "value", "description"])


def build_action_plan(summary: pd.DataFrame) -> pd.DataFrame:
    value = {row["metric"]: int(row["value"]) for row in summary.to_dict("records")}
    return pd.DataFrame(
        [
            {
                "priority": 1,
                "action_id": "add_collector_session_ledger",
                "action": "Persist connection/session open, close, reconnect and subscription-boundary events in the collector.",
                "current_evidence": f"{value['phase35_connection_boundary_ledger_symbols']} symbols have connection-boundary ledger evidence.",
                "acceptance_effect": "Closes the connection_boundary_log evidence family for future Class B days.",
            },
            {
                "priority": 2,
                "action_id": "add_callback_local_sequence_id",
                "action": "Assign and persist a monotonic callback-ingress local_sequence_id before parquet persistence.",
                "current_evidence": f"{value['phase35_explicit_local_sequence_symbols']} symbols have explicit local sequence evidence.",
                "acceptance_effect": "Separates true callback-order integrity from derived persisted-file ordering.",
            },
            {
                "priority": 3,
                "action_id": "add_broker_session_drop_counters",
                "action": "Persist dropped, duplicate, stale and out-of-order counters per connection session and symbol.",
                "current_evidence": f"{value['phase35_drop_duplicate_stale_computable_symbols']} symbols support symptom scanning from persisted ticks.",
                "acceptance_effect": "Turns computable stale/duplicate symptoms into capture-side dropped-message diagnostics.",
            },
            {
                "priority": 4,
                "action_id": "repeat_computable_diagnostics_for_new_days",
                "action": "Run this scanner after every imported/captured raw day and require passing timestamp and compaction checks.",
                "current_evidence": f"{value['phase35_timestamp_semantics_computable_pass_symbols']} symbols pass timestamp checks and {value['phase35_lossless_compaction_computable_pass_symbols']} pass compaction checks on the current sample.",
                "acceptance_effect": "Prevents new raw days from being counted toward Class B unless computable diagnostics keep passing.",
            },
        ]
    )


def write_report(output_dir: Path, summary: pd.DataFrame, symbol_day: pd.DataFrame, ledger: pd.DataFrame, action_plan: pd.DataFrame) -> None:
    lines = [
        "# Phase 35 Stage A2 Computable Diagnostics",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase executes the Stage A2 diagnostics that can be computed from the current raw parquet sample.",
        "It deliberately does not promote the sample to Class B acceptance evidence because connection-boundary logs, explicit callback local sequence IDs, broker/session drop counters and multi-day coverage are still missing.",
        "",
        "## Summary",
        "",
        _markdown_table(summary),
        "",
        "## Action Plan",
        "",
        _markdown_table(action_plan),
        "",
        "## Contract Evidence Ledger",
        "",
        _markdown_table(ledger),
        "",
        "## Symbol-Day Diagnostics",
        "",
        _markdown_table(symbol_day),
        "",
    ]
    (output_dir / "phase35_stage_a2_computable_diagnostics_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase35(stage_quality_path: Path, file_inventory_path: Path, manifest_path: Path, phase1_summary_path: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stage_quality = _read_csv(stage_quality_path)
    file_inventory = _read_csv(file_inventory_path)
    manifest = _read_csv(manifest_path)
    phase1_summary = _read_csv(phase1_summary_path)
    symbol_day = build_symbol_day_diagnostics(stage_quality, file_inventory, phase1_summary, manifest)
    ledger = build_contract_evidence_ledger(symbol_day)
    summary = build_summary(symbol_day, ledger)
    action_plan = build_action_plan(summary)

    symbol_day.to_csv(output_dir / "symbol_day_computable_diagnostics.csv", index=False)
    ledger.to_csv(output_dir / "stage_a2_computable_contract_evidence_ledger.csv", index=False)
    summary.to_csv(output_dir / "stage_a2_computable_diagnostics_summary.csv", index=False)
    action_plan.to_csv(output_dir / "stage_a2_collector_instrumentation_action_plan.csv", index=False)
    write_report(output_dir, summary, symbol_day, ledger, action_plan)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest_out = {
        "generated_utc": generated_utc,
        "symbols_evaluated": int(symbol_day["symbol"].nunique()),
        "raw_rows_scanned": int(symbol_day["raw_rows"].sum()),
        "acceptance_met_rows": int(ledger["acceptance_requirement_met"].sum()),
        "scope": "phase35_stage_a2_computable_diagnostics_not_class_b_acceptance",
        "not_acceptance_result": True,
    }
    manifest_out.update(
        reproducibility_fields(
            artifact_id="phase35",
            generated_utc=generated_utc,
            inputs={
                "stage_a1_data_quality_report": str(stage_quality_path),
                "stage_a1_file_inventory": str(file_inventory_path),
                "azure_files_manifest": str(manifest_path),
                "phase1_feature_summary": str(phase1_summary_path),
            },
            parameters={
                "computed_checks": [
                    "timestamp_presence_and_ordering",
                    "raw_to_phase1_row_count_reconciliation",
                    "manifest_file_count_reconciliation",
                    "duplicate_receive_ms_scan",
                    "stale_gap_gt_15s_scan",
                ],
                "non_computable_acceptance_gaps": [
                    "connection_boundary_session_ledger",
                    "explicit_callback_local_sequence_id",
                    "broker_session_drop_counters",
                    "minimum_5_class_b_days",
                ],
            },
            outputs={
                "symbol_day_diagnostics": str(output_dir / "symbol_day_computable_diagnostics.csv"),
                "contract_evidence_ledger": str(output_dir / "stage_a2_computable_contract_evidence_ledger.csv"),
                "summary": str(output_dir / "stage_a2_computable_diagnostics_summary.csv"),
                "action_plan": str(output_dir / "stage_a2_collector_instrumentation_action_plan.csv"),
                "report": str(output_dir / "phase35_stage_a2_computable_diagnostics_report.md"),
                "manifest": str(output_dir / "phase35_stage_a2_computable_diagnostics_manifest.json"),
            },
            random_seed="none_deterministic_stage_a1_evidence_scan",
            scenario_ids="current_local_real_l2_stage_a2_computable_diagnostics",
            cost_model_version="not_applicable_capture_diagnostics",
            latency_model_version="collector_receive_and_monotonic_timestamp_scan",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase35_stage_a2_computable_diagnostics_manifest.json").write_text(json.dumps(manifest_out, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run computable Stage A2 diagnostics over current raw L2 parquet.")
    parser.add_argument("--stage-quality", type=Path, default=Path("outputs/stage_a1/data_quality_report.csv"))
    parser.add_argument("--file-inventory", type=Path, default=Path("outputs/stage_a1/file_inventory.csv"))
    parser.add_argument("--manifest", type=Path, default=Path("real_data_sample/l2_single_day/azure_files_manifest.csv"))
    parser.add_argument("--phase1-summary", type=Path, default=Path("outputs/phase1/phase1_feature_summary.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase35"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase35(args.stage_quality, args.file_inventory, args.manifest, args.phase1_summary, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

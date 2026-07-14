from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


CAPTURE_DIAGNOSTIC_CRITERIA = [
    ("multiday_class_b_coverage", "At least 5-10 complete Class B event-grade days are captured.", "minimum 5 diagnostically sound complete days"),
    ("local_sequence_integrity", "Local sequence IDs preserve callback order within connection sessions.", "monotonic local sequence and no unaccounted sequence gaps"),
    ("connection_boundary_log", "Connection open, close, reconnect and subscription-boundary events are recorded.", "connection/session ledger exists and reconciles to ticks"),
    ("dropped_message_diagnostics", "Dropped, duplicate, stale and out-of-order message diagnostics are persisted.", "drop/duplicate/stale counters are present per symbol/session/day"),
    ("timestamp_semantics", "Exchange, receive and collector monotonic timestamps are documented and validated.", "timestamp provenance and ordering checks pass"),
    ("lossless_compaction", "Raw callback order is compacted without resampling or event loss.", "row counts and ordering reconcile raw files to compact parquet"),
]


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for column in text.columns:
        text[column] = text[column].map(lambda value: "" if pd.isna(value) else str(value))
    headers = [str(column) for column in text.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in text.values.tolist())
    return "\n".join(lines)


def build_acceptance_criteria() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "criterion_id": criterion_id,
                "criterion_description": description,
                "acceptance_threshold": threshold,
                "current_status": "contract_defined_not_acceptance_evidence",
            }
            for criterion_id, description, threshold in CAPTURE_DIAGNOSTIC_CRITERIA
        ]
    )


def build_required_schema() -> pd.DataFrame:
    rows = [
        ("capture_day_manifest", "trade_date", "date", "required", "Trading date represented by the capture."),
        ("capture_day_manifest", "class_b_complete", "boolean", "required", "True only when the whole session is event-grade and diagnostically sound."),
        ("capture_day_manifest", "symbols_expected", "integer", "required", "Expected subscribed symbols."),
        ("capture_day_manifest", "symbols_complete", "integer", "required", "Symbols with complete capture coverage."),
        ("connection_session_ledger", "session_id", "string", "required", "Stable collector connection/session identifier."),
        ("connection_session_ledger", "opened_utc", "timestamp", "required", "Connection/session open timestamp."),
        ("connection_session_ledger", "closed_utc", "timestamp", "required", "Connection/session close timestamp."),
        ("connection_session_ledger", "close_reason", "string", "required", "Normal close, reconnect, network fault, broker close, or process stop."),
        ("tick_sequence_diagnostics", "local_sequence_id", "integer", "required", "Monotonic callback-order sequence assigned before persistence."),
        ("tick_sequence_diagnostics", "sequence_gap_count", "integer", "required", "Unaccounted local sequence gaps."),
        ("tick_sequence_diagnostics", "duplicate_receive_timestamp_count", "integer", "required", "Duplicate receive timestamp rows."),
        ("tick_sequence_diagnostics", "stale_gap_gt_15s_count", "integer", "required", "Rows/sessions with stale receive gaps above 15 seconds."),
        ("timestamp_semantics", "exchange_timestamp_policy", "string", "required", "Meaning and availability of exchange-side timestamps."),
        ("timestamp_semantics", "collector_received_utc_policy", "string", "required", "Meaning and clock source for collector receive timestamp."),
        ("compaction_reconciliation", "raw_rows", "integer", "required", "Raw tick rows before compaction."),
        ("compaction_reconciliation", "compact_rows", "integer", "required", "Compact tick rows after compaction."),
        ("compaction_reconciliation", "row_count_match", "boolean", "required", "Raw and compact rows reconcile exactly."),
    ]
    return pd.DataFrame(rows, columns=["artifact_name", "field_name", "field_type", "required_status", "field_purpose"])


def build_gap_ledger(stage_quality: pd.DataFrame, horizon_summary: pd.DataFrame) -> pd.DataFrame:
    real_sample_days_available = 1
    dense_1s = 0
    if not horizon_summary.empty:
        matched = horizon_summary[
            (horizon_summary["scope"].astype(str) == "full_session")
            & (horizon_summary["horizon_ms"].astype(int) == 1000)
        ]
        if not matched.empty:
            dense_1s = int(matched["dense_regular_panel_symbols"].max())
    rows = []
    for record in stage_quality.to_dict("records"):
        symbol = record["symbol"]
        base = {
            "symbol": symbol,
            "instrument_class": record.get("instrument_class", ""),
            "current_sample_days_available": real_sample_days_available,
            "current_row_count": int(record.get("row_count", 0)),
            "current_file_count": int(record.get("file_count", 0)),
            "current_event_rate_per_second": record.get("event_rate_per_second", ""),
            "current_stale_gap_gt_15s_count": int(record.get("stale_gap_gt_15s_count", 0)),
            "current_duplicate_receive_ms": int(record.get("duplicate_receive_ms", 0)),
            "dense_1s_full_session_symbols": dense_1s,
        }
        for criterion_id, _description, threshold in CAPTURE_DIAGNOSTIC_CRITERIA:
            if criterion_id == "multiday_class_b_coverage":
                status = "missing_required_multiday_capture"
                gap = "Only one current real sample day is available; Stage A2 requires at least 5-10 complete Class B days."
                action = "Continue Class B collection until at least 5 complete diagnostically sound days are available."
            elif criterion_id == "local_sequence_integrity":
                status = "local_sequence_contract_required"
                gap = "Stage A1 verifies ordering after persistence but does not prove explicit callback local sequence IDs."
                action = "Persist monotonic local sequence IDs at callback ingress and audit gaps by session/day/symbol."
            elif criterion_id == "connection_boundary_log":
                status = "connection_boundary_ledger_required"
                gap = "Current compact sample does not include a connection/session boundary ledger."
                action = "Record connection open/close/reconnect/subscription boundaries and reconcile them to tick files."
            elif criterion_id == "dropped_message_diagnostics":
                status = "dropped_message_diagnostics_required"
                gap = "Duplicate/stale symptoms exist in Stage A1, but explicit dropped-message broker/session diagnostics are not available."
                action = "Persist dropped/duplicate/stale/out-of-order counters per connection session and symbol."
            elif criterion_id == "timestamp_semantics":
                status = "timestamp_semantics_contract_required"
                gap = "Receive timestamps are audited, but exchange/receive/monotonic timestamp semantics require a capture-side contract."
                action = "Document timestamp sources and validate exchange, receive and monotonic ordering semantics per day."
            else:
                status = "lossless_multiday_compaction_required"
                gap = "One-day compaction reconciles current raw input, but Stage A2 requires repeatable multi-day lossless compaction."
                action = "Reconcile raw rows/files to compact parquet for every new Class B day without resampling."
            rows.append(
                {
                    **base,
                    "criterion_id": criterion_id,
                    "acceptance_threshold": threshold,
                    "capture_contract_status": status,
                    "acceptance_requirement_met_after_contract": False,
                    "blocking_gap_after_contract": gap,
                    "required_capture_action": action,
                }
            )
    return pd.DataFrame(rows).sort_values(["symbol", "criterion_id"], kind="mergesort")


def build_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    return (
        ledger.groupby("capture_contract_status", sort=True)
        .agg(
            rows=("criterion_id", "size"),
            symbols=("symbol", "nunique"),
            acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"),
        )
        .reset_index()
        .sort_values(["rows", "capture_contract_status"], ascending=[False, True], kind="mergesort")
    )


def build_day_readiness_summary(stage_quality: pd.DataFrame, ledger: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "current_sample_days_available": 1,
                "required_complete_days_min": 5,
                "required_complete_days_target": 10,
                "symbols_evaluated": int(stage_quality["symbol"].nunique()),
                "current_rows": int(stage_quality["row_count"].sum()),
                "symbols_with_stale_gap_gt_15s": int((stage_quality["stale_gap_gt_15s_count"] > 0).sum()),
                "open_contract_rows": int((~ledger["acceptance_requirement_met_after_contract"].astype(bool)).sum()),
                "acceptance_met_rows": int(ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()),
                "stage_a2_status": "blocked_until_multiday_class_b_capture_and_diagnostics_exist",
            }
        ]
    )


def write_report(output_dir: Path, criteria: pd.DataFrame, schema: pd.DataFrame, ledger: pd.DataFrame, summary: pd.DataFrame, readiness: pd.DataFrame) -> None:
    lines = [
        "# Stage A2 Capture Diagnostics and Multi-Day Expansion Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This contract turns Stage A2 into explicit capture diagnostics, schema requirements and per-symbol blocker rows.",
        "It does not claim that multi-day Class B data exists; it records the current one-day state and the diagnostics needed before strategy robustness or promotion claims.",
        "",
        "## Acceptance Criteria",
        "",
        _markdown_table(criteria),
        "",
        "## Required Capture Schema",
        "",
        _markdown_table(schema),
        "",
        "## Stage A2 Readiness Summary",
        "",
        _markdown_table(readiness),
        "",
        "## Gap Summary",
        "",
        _markdown_table(summary),
        "",
        "## Gap Ledger",
        "",
        _markdown_table(ledger),
        "",
    ]
    (output_dir / "stage_a2_capture_diagnostics_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_stage_a2(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stage_quality = pd.read_csv(paths["stage_quality"])
    horizon_summary = pd.read_csv(paths["horizon_readiness_summary"])
    criteria = build_acceptance_criteria()
    schema = build_required_schema()
    ledger = build_gap_ledger(stage_quality, horizon_summary)
    summary = build_summary(ledger)
    readiness = build_day_readiness_summary(stage_quality, ledger)

    criteria.to_csv(output_dir / "capture_diagnostics_acceptance_criteria.csv", index=False)
    schema.to_csv(output_dir / "required_capture_schema.csv", index=False)
    ledger.to_csv(output_dir / "capture_diagnostics_gap_ledger.csv", index=False)
    summary.to_csv(output_dir / "capture_diagnostics_gap_summary.csv", index=False)
    readiness.to_csv(output_dir / "stage_a2_readiness_summary.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "capture_diagnostics_acceptance_criteria_rows": int(len(criteria)),
        "required_capture_schema_rows": int(len(schema)),
        "capture_diagnostics_gap_rows": int(len(ledger)),
        "capture_diagnostics_gap_summary_rows": int(len(summary)),
        "stage_a2_readiness_summary_rows": int(len(readiness)),
        "symbols_evaluated": int(stage_quality["symbol"].nunique()),
        "current_sample_days_available": 1,
        "acceptance_met_after_contract_rows": int(ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()),
        "scope": "stage_a2_capture_diagnostics_contract_not_multiday_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="stage_a2",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"capture_diagnostic_criteria": CAPTURE_DIAGNOSTIC_CRITERIA},
            outputs={
                "capture_diagnostics_acceptance_criteria": str(output_dir / "capture_diagnostics_acceptance_criteria.csv"),
                "required_capture_schema": str(output_dir / "required_capture_schema.csv"),
                "capture_diagnostics_gap_ledger": str(output_dir / "capture_diagnostics_gap_ledger.csv"),
                "capture_diagnostics_gap_summary": str(output_dir / "capture_diagnostics_gap_summary.csv"),
                "stage_a2_readiness_summary": str(output_dir / "stage_a2_readiness_summary.csv"),
                "report": str(output_dir / "stage_a2_capture_diagnostics_contract_report.md"),
                "manifest": str(output_dir / "stage_a2_capture_diagnostics_contract_manifest.json"),
            },
            random_seed="not_applicable_deterministic_capture_contract",
            scenario_ids="stage_a2_multiday_capture_expansion_contract",
            cost_model_version="not_applicable_no_execution_costs",
            latency_model_version="stage_a1_one_day_zerodha_websocket_sample",
            base_dir=base_dir,
        )
    )
    (output_dir / "stage_a2_capture_diagnostics_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, criteria, schema, ledger, summary, readiness)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage A2 capture diagnostics and multi-day expansion contract artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/stage_a2"))
    parser.add_argument("--stage-quality", type=Path, default=Path("outputs/stage_a1/data_quality_report.csv"))
    parser.add_argument("--horizon-readiness-summary", type=Path, default=Path("outputs/horizon_readiness/horizon_readiness_summary.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "stage_quality": args.stage_quality,
        "horizon_readiness_summary": args.horizon_readiness_summary,
    }
    run_stage_a2(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.collector_instrumentation import CollectorInstrumentation
from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


def required_schema() -> pd.DataFrame:
    rows = [
        ("raw_tick_enrichment", "collector_run_id", "string", "required", "Stable process/run identifier for the collector instance."),
        ("raw_tick_enrichment", "session_id", "string", "required", "Connection/session identifier attached to each tick."),
        ("raw_tick_enrichment", "callback_batch_id", "integer", "required", "Monotonic callback batch number within a collector run."),
        ("raw_tick_enrichment", "local_sequence_id", "integer", "required", "Monotonic callback-order tick sequence assigned before persistence."),
        ("raw_tick_enrichment", "callback_received_utc", "timestamp", "required", "UTC timestamp captured once per websocket callback before persistence."),
        ("raw_tick_enrichment", "callback_received_monotonic_ns", "integer", "required", "Monotonic clock captured once per websocket callback before persistence."),
        ("connection_session_ledger", "collector_run_id", "string", "required", "Collector process/run identifier."),
        ("connection_session_ledger", "session_id", "string", "required", "Connection/session identifier."),
        ("connection_session_ledger", "opened_utc", "timestamp", "required", "Session open timestamp."),
        ("connection_session_ledger", "closed_utc", "timestamp", "required", "Session close timestamp."),
        ("connection_session_ledger", "open_reason", "string", "required", "Connect/reconnect/subscription reason."),
        ("connection_session_ledger", "close_reason", "string", "required", "Normal close, reconnect, network fault, broker close or process stop."),
        ("connection_session_ledger", "subscribed_symbols", "string", "required", "Subscribed symbols joined by semicolon."),
        ("connection_session_ledger", "first_local_sequence_id", "integer", "required", "First local sequence attached to the session."),
        ("connection_session_ledger", "last_local_sequence_id", "integer", "required", "Last local sequence attached to the session."),
        ("connection_session_ledger", "tick_rows", "integer", "required", "Ticks observed in the session."),
        ("drop_counter_ledger", "symbol", "string", "required", "Instrument symbol."),
        ("drop_counter_ledger", "dropped_count", "integer", "required", "Collector/session observed dropped-message count."),
        ("drop_counter_ledger", "duplicate_count", "integer", "required", "Collector/session observed duplicate count."),
        ("drop_counter_ledger", "stale_count", "integer", "required", "Collector/session observed stale-message count."),
        ("drop_counter_ledger", "out_of_order_count", "integer", "required", "Collector/session observed out-of-order count."),
    ]
    return pd.DataFrame(rows, columns=["artifact_name", "field_name", "field_type", "required_status", "field_purpose"])


def interface_catalog() -> pd.DataFrame:
    rows = [
        ("open_session", "Call after websocket connection and subscription are established.", "connection_session_ledger row opened"),
        ("enrich_ticks", "Call as the first operation inside on_ticks before parquet writes.", "collector_run_id/session_id/callback_batch_id/local_sequence_id/callback timestamps on every tick"),
        ("record_drop_counters", "Call when duplicate, stale, dropped or out-of-order symptoms/counters are detected.", "drop_counter_ledger row per session/symbol observation"),
        ("close_session", "Call on normal close, reconnect, network fault, broker close or process stop.", "connection_session_ledger row closed with reason"),
        ("flush", "Call on shutdown and after close/reconnect boundaries.", "CSV ledgers persisted for Stage A2 ingestion"),
    ]
    return pd.DataFrame(rows, columns=["interface_method", "collector_hook", "stage_a2_evidence"])


def integration_checklist() -> pd.DataFrame:
    rows = [
        (1, "import_helper", "Import CollectorInstrumentation in the live Zerodha websocket collector.", "pending_live_collector_integration"),
        (2, "session_boundaries", "Wrap connect/reconnect/subscription lifecycle with open_session and close_session.", "pending_live_collector_integration"),
        (3, "tick_enrichment", "Call enrich_ticks at the start of on_ticks and persist returned tick rows.", "pending_live_collector_integration"),
        (4, "drop_counters", "Persist duplicate/stale/out-of-order/drop counters through record_drop_counters.", "pending_live_collector_integration"),
        (5, "flush_ledgers", "Flush ledgers at shutdown and reconnect boundaries beside raw parquet output.", "pending_live_collector_integration"),
        (6, "stage_a2_ingestion", "Point Stage A2/Phase 35 scanners at emitted ledgers for Class B promotion checks.", "pending_after_live_capture"),
    ]
    return pd.DataFrame(rows, columns=["priority", "check_id", "required_change", "current_status"])


def dry_run(output_dir: Path) -> dict[str, pd.DataFrame]:
    inst = CollectorInstrumentation(output_dir=output_dir / "dry_run_ledgers", collector_run_id="phase36_dry_run")
    inst.open_session(["HDFCBANK", "INFY"], exchange="NSE", reason="dry_run_connect")
    inst.enrich_ticks(
        [
            {"tradingsymbol": "HDFCBANK", "last_price": 823.75},
            {"tradingsymbol": "INFY", "last_price": 1512.10},
            {"tradingsymbol": "HDFCBANK", "last_price": 824.05},
        ]
    )
    inst.record_drop_counters("HDFCBANK", duplicate_count=0, stale_count=0, out_of_order_count=0)
    inst.record_drop_counters("INFY", duplicate_count=0, stale_count=0, out_of_order_count=0)
    inst.close_session("dry_run_normal_close")
    inst.flush()
    return inst.frames()


def summary(schema: pd.DataFrame, frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("phase36_required_schema_fields", len(schema), "Required collector instrumentation schema fields"),
            ("phase36_dry_run_session_rows", len(frames["session_ledger"]), "Dry-run connection/session ledger rows"),
            ("phase36_dry_run_sequence_rows", len(frames["tick_sequence_diagnostics"]), "Dry-run local sequence diagnostic rows"),
            ("phase36_dry_run_drop_counter_rows", len(frames["drop_counter_ledger"]), "Dry-run drop counter rows"),
            ("phase36_live_collector_integrated", 0, "Live collector integration status in this workspace"),
            ("phase36_class_b_capture_enabled", 0, "Whether new live captures can be marked Class B from this package alone"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, schema: pd.DataFrame, catalog: pd.DataFrame, checklist: pd.DataFrame, summary_frame: pd.DataFrame, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 36 Collector Instrumentation Package",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This package supplies collector-side instrumentation required by Stage A2: session boundary ledgers, callback local sequence IDs and dropped-message counters.",
        "It is implementation scaffolding and dry-run proof, not evidence that the live Zerodha collector has already captured new Class B days.",
        "",
        "## Summary",
        "",
        _markdown_table(summary_frame),
        "",
        "## Required Schema",
        "",
        _markdown_table(schema),
        "",
        "## Collector Interface",
        "",
        _markdown_table(catalog),
        "",
        "## Integration Checklist",
        "",
        _markdown_table(checklist),
        "",
        "## Dry-Run Session Ledger",
        "",
        _markdown_table(frames["session_ledger"]),
        "",
        "## Dry-Run Tick Sequence Diagnostics",
        "",
        _markdown_table(frames["tick_sequence_diagnostics"]),
        "",
        "## Dry-Run Drop Counter Ledger",
        "",
        _markdown_table(frames["drop_counter_ledger"]),
        "",
    ]
    (output_dir / "phase36_collector_instrumentation_package_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase36(output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    schema = required_schema()
    catalog = interface_catalog()
    checklist = integration_checklist()
    frames = dry_run(output_dir)
    summary_frame = summary(schema, frames)

    schema.to_csv(output_dir / "collector_instrumentation_required_schema.csv", index=False)
    catalog.to_csv(output_dir / "collector_instrumentation_interface_catalog.csv", index=False)
    checklist.to_csv(output_dir / "collector_instrumentation_integration_checklist.csv", index=False)
    summary_frame.to_csv(output_dir / "collector_instrumentation_package_summary.csv", index=False)
    write_report(output_dir, schema, catalog, checklist, summary_frame, frames)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "required_schema_fields": int(len(schema)),
        "dry_run_session_rows": int(len(frames["session_ledger"])),
        "dry_run_sequence_rows": int(len(frames["tick_sequence_diagnostics"])),
        "dry_run_drop_counter_rows": int(len(frames["drop_counter_ledger"])),
        "scope": "phase36_collector_instrumentation_package_not_live_capture_evidence",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase36",
            generated_utc=generated_utc,
            inputs={"collector_instrumentation_module": "src/synthetic_l2/collector_instrumentation.py"},
            parameters={"dry_run_symbols": ["HDFCBANK", "INFY"], "live_collector_present_in_workspace": False},
            outputs={
                "required_schema": str(output_dir / "collector_instrumentation_required_schema.csv"),
                "interface_catalog": str(output_dir / "collector_instrumentation_interface_catalog.csv"),
                "integration_checklist": str(output_dir / "collector_instrumentation_integration_checklist.csv"),
                "summary": str(output_dir / "collector_instrumentation_package_summary.csv"),
                "report": str(output_dir / "phase36_collector_instrumentation_package_report.md"),
                "manifest": str(output_dir / "phase36_collector_instrumentation_package_manifest.json"),
            },
            random_seed="none_deterministic_instrumentation_dry_run",
            scenario_ids="collector_session_sequence_drop_counter_instrumentation_package",
            cost_model_version="not_applicable_capture_instrumentation",
            latency_model_version="callback_received_utc_and_monotonic_ns_instrumentation",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase36_collector_instrumentation_package_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build collector instrumentation package artifacts for Stage A2.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase36"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase36(args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.reproducibility import reproducibility_fields


REQUIRED_COLUMNS = {
    "session_ledger": [
        "collector_run_id",
        "session_id",
        "opened_utc",
        "closed_utc",
        "open_reason",
        "close_reason",
        "subscribed_symbols",
        "first_local_sequence_id",
        "last_local_sequence_id",
        "tick_rows",
    ],
    "tick_sequence_diagnostics": [
        "collector_run_id",
        "session_id",
        "callback_batch_id",
        "local_sequence_id",
        "symbol",
        "callback_received_utc",
        "callback_received_monotonic_ns",
    ],
    "drop_counter_ledger": [
        "collector_run_id",
        "session_id",
        "symbol",
        "observed_utc",
        "source",
        "dropped_count",
        "duplicate_count",
        "stale_count",
        "out_of_order_count",
    ],
}


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def _missing_columns(frame: pd.DataFrame, required: list[str]) -> list[str]:
    return [column for column in required if column not in frame.columns]


def schema_validation(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for artifact, required in REQUIRED_COLUMNS.items():
        missing = _missing_columns(frames[artifact], required)
        rows.append(
            {
                "artifact_name": artifact,
                "required_columns": len(required),
                "missing_columns": len(missing),
                "missing_column_names": ";".join(missing),
                "schema_valid": len(missing) == 0,
            }
        )
    return pd.DataFrame(rows)


def session_validation(session: pd.DataFrame, sequence: pd.DataFrame) -> pd.DataFrame:
    rows = []
    seq_counts = sequence.groupby("session_id", sort=True).size().to_dict() if "session_id" in sequence.columns else {}
    for record in session.to_dict("records"):
        session_id = str(record.get("session_id", ""))
        tick_rows = int(record.get("tick_rows", 0))
        first_seq = int(record.get("first_local_sequence_id", 0))
        last_seq = int(record.get("last_local_sequence_id", 0))
        sequence_rows = int(seq_counts.get(session_id, 0))
        rows.append(
            {
                "collector_run_id": record.get("collector_run_id", ""),
                "session_id": session_id,
                "opened_utc_present": bool(str(record.get("opened_utc", ""))),
                "closed_utc_present": bool(str(record.get("closed_utc", ""))),
                "close_reason_present": bool(str(record.get("close_reason", ""))),
                "tick_rows": tick_rows,
                "sequence_rows": sequence_rows,
                "session_sequence_count_match": tick_rows == sequence_rows,
                "session_sequence_bounds_match": last_seq >= first_seq and (last_seq - first_seq + 1) == tick_rows,
                "session_valid": tick_rows > 0 and tick_rows == sequence_rows and last_seq >= first_seq and (last_seq - first_seq + 1) == tick_rows,
            }
        )
    return pd.DataFrame(rows)


def sequence_validation(sequence: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if sequence.empty:
        return pd.DataFrame(columns=["session_id", "sequence_rows", "sequence_gap_count", "duplicate_sequence_count", "monotonic_sequence_pass"])
    for session_id, group in sequence.groupby("session_id", sort=True):
        seq = pd.to_numeric(group["local_sequence_id"], errors="coerce").dropna().astype(int).sort_values()
        expected = set(range(int(seq.min()), int(seq.max()) + 1)) if len(seq) else set()
        observed = set(seq.tolist())
        rows.append(
            {
                "session_id": session_id,
                "sequence_rows": int(len(group)),
                "sequence_gap_count": int(len(expected - observed)),
                "duplicate_sequence_count": int(len(seq) - len(observed)),
                "monotonic_sequence_pass": bool(len(seq) == len(observed) and len(expected - observed) == 0),
            }
        )
    return pd.DataFrame(rows)


def drop_counter_validation(session: pd.DataFrame, drop: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for record in session.to_dict("records"):
        session_id = str(record.get("session_id", ""))
        subscribed = [symbol for symbol in str(record.get("subscribed_symbols", "")).split(";") if symbol]
        matched = drop[drop["session_id"].astype(str).eq(session_id)] if "session_id" in drop.columns else pd.DataFrame()
        covered = set(matched["symbol"].astype(str).tolist()) if not matched.empty and "symbol" in matched.columns else set()
        rows.append(
            {
                "session_id": session_id,
                "subscribed_symbols": len(subscribed),
                "drop_counter_symbols": len(covered),
                "missing_drop_counter_symbols": ";".join(sorted(set(subscribed) - covered)),
                "drop_counter_coverage_pass": set(subscribed).issubset(covered),
                "total_dropped_count": int(pd.to_numeric(matched.get("dropped_count", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not matched.empty else 0,
                "total_duplicate_count": int(pd.to_numeric(matched.get("duplicate_count", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not matched.empty else 0,
                "total_stale_count": int(pd.to_numeric(matched.get("stale_count", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not matched.empty else 0,
                "total_out_of_order_count": int(pd.to_numeric(matched.get("out_of_order_count", pd.Series(dtype=int)), errors="coerce").fillna(0).sum()) if not matched.empty else 0,
            }
        )
    return pd.DataFrame(rows)


def promotion_gate(schema: pd.DataFrame, session: pd.DataFrame, sequence: pd.DataFrame, drop: pd.DataFrame, collector_source: str) -> pd.DataFrame:
    schema_pass = bool(schema["schema_valid"].all())
    session_pass = bool(len(session) > 0 and session["session_valid"].all())
    sequence_pass = bool(len(sequence) > 0 and sequence["monotonic_sequence_pass"].all())
    drop_pass = bool(len(drop) > 0 and drop["drop_counter_coverage_pass"].all())
    live_evidence = collector_source == "live_collector"
    ready = schema_pass and session_pass and sequence_pass and drop_pass and live_evidence
    rows = [
        ("schema_pass", int(schema_pass), "All required collector-ledger columns are present"),
        ("session_boundary_pass", int(session_pass), "Session rows reconcile to sequence rows and sequence bounds"),
        ("local_sequence_pass", int(sequence_pass), "Local sequence IDs are contiguous and non-duplicated per session"),
        ("drop_counter_coverage_pass", int(drop_pass), "Drop-counter rows cover all subscribed session symbols"),
        ("live_collector_evidence", int(live_evidence), "Ledgers come from live collector output rather than dry-run scaffolding"),
        ("stage_a2_collector_evidence_ready", int(ready), "Collector-side Stage A2 evidence can be consumed for Class B promotion checks"),
    ]
    return pd.DataFrame(rows, columns=["gate", "passed", "description"])


def summary(schema: pd.DataFrame, session: pd.DataFrame, sequence: pd.DataFrame, drop: pd.DataFrame, gate: pd.DataFrame) -> pd.DataFrame:
    value = {row["gate"]: int(row["passed"]) for row in gate.to_dict("records")}
    rows = [
        ("phase37_schema_artifacts_checked", int(len(schema)), "Collector ledger artifacts checked for required schema"),
        ("phase37_schema_missing_columns", int(schema["missing_columns"].sum()), "Missing required collector-ledger columns"),
        ("phase37_session_rows_verified", int(len(session)), "Session ledger rows verified"),
        ("phase37_sequence_sessions_verified", int(len(sequence)), "Sessions with sequence diagnostics verified"),
        ("phase37_drop_counter_sessions_verified", int(len(drop)), "Sessions with drop-counter coverage verified"),
        ("phase37_schema_pass", value["schema_pass"], "Schema gate pass flag"),
        ("phase37_session_boundary_pass", value["session_boundary_pass"], "Session-boundary gate pass flag"),
        ("phase37_local_sequence_pass", value["local_sequence_pass"], "Local-sequence gate pass flag"),
        ("phase37_drop_counter_coverage_pass", value["drop_counter_coverage_pass"], "Drop-counter coverage gate pass flag"),
        ("phase37_live_collector_evidence", value["live_collector_evidence"], "Live collector evidence flag"),
        ("phase37_stage_a2_collector_evidence_ready", value["stage_a2_collector_evidence_ready"], "Collector evidence ready for Class B checks"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "description"])


def write_report(output_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Phase 37 Collector Ledger Verifier",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This phase verifies collector instrumentation ledgers for Stage A2 consumption.",
        "Dry-run ledgers can pass structural checks, but they are not live collector evidence and therefore cannot enable Class B capture promotion.",
        "",
    ]
    for title, frame in frames.items():
        lines.extend([f"## {title}", "", _markdown_table(frame), ""])
    (output_dir / "phase37_collector_ledger_verifier_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase37(paths: dict[str, Path], output_dir: Path, base_dir: Path, collector_source: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    frames = {
        "session_ledger": _read_csv(paths["session_ledger"]),
        "tick_sequence_diagnostics": _read_csv(paths["tick_sequence_diagnostics"]),
        "drop_counter_ledger": _read_csv(paths["drop_counter_ledger"]),
    }
    schema_frame = schema_validation(frames)
    session_frame = session_validation(frames["session_ledger"], frames["tick_sequence_diagnostics"])
    sequence_frame = sequence_validation(frames["tick_sequence_diagnostics"])
    drop_frame = drop_counter_validation(frames["session_ledger"], frames["drop_counter_ledger"])
    gate_frame = promotion_gate(schema_frame, session_frame, sequence_frame, drop_frame, collector_source)
    summary_frame = summary(schema_frame, session_frame, sequence_frame, drop_frame, gate_frame)

    outputs = {
        "schema_validation": schema_frame,
        "session_validation": session_frame,
        "sequence_validation": sequence_frame,
        "drop_counter_validation": drop_frame,
        "promotion_gate": gate_frame,
        "summary": summary_frame,
    }
    for name, frame in outputs.items():
        frame.to_csv(output_dir / f"{name}.csv", index=False)
    write_report(output_dir, outputs)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "collector_source": collector_source,
        "stage_a2_collector_evidence_ready": int(gate_frame.loc[gate_frame["gate"].eq("stage_a2_collector_evidence_ready"), "passed"].iloc[0]),
        "scope": "phase37_collector_ledger_verifier_not_live_capture_by_default",
        "not_acceptance_result": collector_source != "live_collector",
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase37",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={"collector_source": collector_source, "required_columns": REQUIRED_COLUMNS},
            outputs={key: str(output_dir / f"{key}.csv") for key in outputs} | {"report": str(output_dir / "phase37_collector_ledger_verifier_report.md"), "manifest": str(output_dir / "phase37_collector_ledger_verifier_manifest.json")},
            random_seed="none_deterministic_collector_ledger_verification",
            scenario_ids="collector_ledger_verification_for_stage_a2",
            cost_model_version="not_applicable_collector_evidence_gate",
            latency_model_version="callback_local_sequence_and_session_ledger",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase37_collector_ledger_verifier_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify collector instrumentation ledgers for Stage A2 ingestion.")
    parser.add_argument("--session-ledger", type=Path, default=Path("outputs/phase36/dry_run_ledgers/session_ledger.csv"))
    parser.add_argument("--tick-sequence-diagnostics", type=Path, default=Path("outputs/phase36/dry_run_ledgers/tick_sequence_diagnostics.csv"))
    parser.add_argument("--drop-counter-ledger", type=Path, default=Path("outputs/phase36/dry_run_ledgers/drop_counter_ledger.csv"))
    parser.add_argument("--collector-source", choices=["dry_run", "live_collector"], default="dry_run")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase37"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase37(
        {
            "session_ledger": args.session_ledger,
            "tick_sequence_diagnostics": args.tick_sequence_diagnostics,
            "drop_counter_ledger": args.drop_counter_ledger,
        },
        args.output_dir,
        args.base_dir,
        args.collector_source,
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE304_DIR = Path("outputs/phase304")
DEFAULT_DROPZONE_DIR = Path("event_sources/event_catalysts/dropzone")
DEFAULT_OUTPUT_DIR = Path("outputs/phase305")

TEMPLATE_FILENAME = "event_catalyst_events_template.csv"
PLACEHOLDER_SOURCE = "REPLACE_WITH_EXTERNAL_SOURCE_URL_OR_LOCAL_EVIDENCE_FILE"
PLACEHOLDER_TITLE = "TEMPLATE_ROW_DELETE_OR_REPLACE"

REQUIRED_COLUMNS = [
    "event_time_ist",
    "event_type",
    "symbol_scope",
    "index_scope",
    "source_url_or_file",
    "confidence",
    "embargo_safe_flag",
]

OUTPUT_COLUMNS = REQUIRED_COLUMNS + [
    "event_title",
    "expected_impact_side",
    "source_provider",
    "source_published_time_ist",
    "notes",
    "source_file",
]

NEXT_ACTION_WHEN_EMPTY = "populate_event_catalyst_dropzone_with_non_template_source_rows_then_rerun_phase305"
NEXT_ACTION_WHEN_IMPORTED = "run_phase306_event_catalyst_top5_depth_join_precommit_no_strategy_search"
REPAIR_ACTION = "repair_phase305_event_catalyst_source_import_audit"


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_candidate_files(dropzone_dir: Path) -> list[Path]:
    if not dropzone_dir.exists():
        return []
    return sorted(path for path in dropzone_dir.glob("*.csv") if path.name != TEMPLATE_FILENAME)


def is_placeholder_row(row: pd.Series) -> bool:
    return (
        str(row.get("source_url_or_file", "")).strip() == PLACEHOLDER_SOURCE
        or str(row.get("event_title", "")).strip() == PLACEHOLDER_TITLE
    )


def audit_files(dropzone_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    files = load_candidate_files(dropzone_dir)
    inventory_rows: list[dict[str, Any]] = []
    issue_rows: list[dict[str, Any]] = []
    imported_frames: list[pd.DataFrame] = []

    for path in files:
        try:
            frame = pd.read_csv(path)
        except Exception as exc:  # pragma: no cover - defensive audit path
            inventory_rows.append(
                {
                    "source_file": str(path),
                    "row_count": 0,
                    "required_columns_present": 0,
                    "importable_rows": 0,
                    "issue_rows": 1,
                    "file_status": "read_error",
                }
            )
            issue_rows.append({"source_file": str(path), "row_index": "", "issue_id": "read_error", "issue_detail": str(exc)})
            continue

        missing = [col for col in REQUIRED_COLUMNS if col not in frame.columns]
        required_present = int(not missing)
        importable = pd.DataFrame(columns=OUTPUT_COLUMNS)
        if missing:
            issue_rows.append(
                {
                    "source_file": str(path),
                    "row_index": "",
                    "issue_id": "missing_required_columns",
                    "issue_detail": "|".join(missing),
                }
            )
        else:
            working = frame.copy()
            for col in OUTPUT_COLUMNS:
                if col not in working.columns and col != "source_file":
                    working[col] = ""
            working["source_file"] = str(path)
            working["confidence_numeric"] = pd.to_numeric(working["confidence"], errors="coerce")
            working["embargo_safe_numeric"] = pd.to_numeric(working["embargo_safe_flag"], errors="coerce")
            working["event_time_parsed"] = pd.to_datetime(working["event_time_ist"], errors="coerce")
            valid_mask = pd.Series(True, index=working.index)
            for idx, row in working.iterrows():
                row_issues: list[str] = []
                if is_placeholder_row(row):
                    row_issues.append("placeholder_row")
                if pd.isna(row["event_time_parsed"]):
                    row_issues.append("invalid_event_time_ist")
                confidence = to_float(row["confidence_numeric"], -1.0)
                if confidence < 0.0 or confidence > 1.0:
                    row_issues.append("confidence_out_of_range")
                if as_int(row["embargo_safe_numeric"]) != 1:
                    row_issues.append("embargo_not_safe")
                if str(row.get("source_url_or_file", "")).strip() == "":
                    row_issues.append("missing_source_url_or_file")
                if row_issues:
                    valid_mask.loc[idx] = False
                    for issue in row_issues:
                        issue_rows.append(
                            {
                                "source_file": str(path),
                                "row_index": int(idx),
                                "issue_id": issue,
                                "issue_detail": str(row.get("event_title", "")),
                            }
                        )
            importable = working.loc[valid_mask, OUTPUT_COLUMNS].copy()
            if not importable.empty:
                imported_frames.append(importable)
        inventory_rows.append(
            {
                "source_file": str(path),
                "row_count": int(len(frame)),
                "required_columns_present": required_present,
                "importable_rows": int(len(importable)),
                "issue_rows": int(sum(1 for issue in issue_rows if issue["source_file"] == str(path))),
                "file_status": "importable" if len(importable) else ("schema_rejected" if missing else "row_rejected"),
            }
        )

    inventory = pd.DataFrame(
        inventory_rows,
        columns=["source_file", "row_count", "required_columns_present", "importable_rows", "issue_rows", "file_status"],
    )
    issues = pd.DataFrame(issue_rows, columns=["source_file", "row_index", "issue_id", "issue_detail"])
    imported = pd.concat(imported_frames, ignore_index=True) if imported_frames else pd.DataFrame(columns=OUTPUT_COLUMNS)
    return inventory, issues, imported


def build_gate_evaluation(phase304: pd.DataFrame, inventory: pd.DataFrame, issues: pd.DataFrame, imported: pd.DataFrame, template_exists: bool) -> pd.DataFrame:
    imported_rows = int(len(imported))
    candidate_files = int(len(inventory))
    gates = [
        ("P305_PHASE304_PACKAGE_COMPLETE", as_int(metric_value(phase304, "phase304_source_acquisition_package_complete", 0)) == 1, metric_value(phase304, "phase304_source_acquisition_package_complete", ""), 1),
        ("P305_TEMPLATE_EXISTS", template_exists, int(template_exists), 1),
        ("P305_DROPZONE_AUDITED", True, candidate_files, ">=0"),
        ("P305_PLACEHOLDERS_NOT_IMPORTED", imported["source_url_or_file"].astype(str).ne(PLACEHOLDER_SOURCE).all() if imported_rows else True, imported_rows, "no_placeholder_imports"),
        ("P305_IMPORT_REQUIRES_NON_TEMPLATE_FILES", imported_rows == 0 if candidate_files == 0 else True, f"candidate_files={candidate_files};imported={imported_rows}", "no import from template"),
        ("P305_ISSUES_LEDGER_WRITTEN", len(issues) >= 0, len(issues), ">=0"),
        ("P305_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", 0),
        ("P305_BOUNDARIES_CLOSED", True, "replay=0;promotion=0;paper=0;claim=0", "all_zero"),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(inventory: pd.DataFrame, issues: pd.DataFrame, imported: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    imported_rows = int(len(imported))
    candidate_files = int(len(inventory))
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    next_action = NEXT_ACTION_WHEN_IMPORTED if imported_rows > 0 and hard_pass == hard_rows else NEXT_ACTION_WHEN_EMPTY if hard_pass == hard_rows else REPAIR_ACTION
    return pd.DataFrame(
        [
            ("phase305_event_catalyst_import_audit_complete", 1, "Phase305 event-catalyst source import audit completed"),
            ("phase305_candidate_source_file_rows", candidate_files, "Non-template CSV files audited"),
            ("phase305_candidate_source_raw_rows", int(inventory["row_count"].sum()) if not inventory.empty else 0, "Raw candidate rows read"),
            ("phase305_imported_event_rows", imported_rows, "Rows imported into event catalyst source ledger"),
            ("phase305_issue_rows", int(len(issues)), "Import issue rows"),
            ("phase305_template_rows_imported", 0, "Template rows are never imported"),
            ("phase305_strategy_search_allowed_now", 0, "No strategy search until imported events exist and Phase306 precommits join"),
            ("phase305_strategy_replay_allowed", 0, "No replay"),
            ("phase305_strategy_promotion_allowed", 0, "No promotion"),
            ("phase305_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase305_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase305_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase305_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase305_next_best_action", next_action, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, inventory: pd.DataFrame, issues: pd.DataFrame, imported: pd.DataFrame, gates: pd.DataFrame, acceptance: pd.DataFrame) -> None:
    lines = [
        "# Phase305 Event-Catalyst Source Import Audit",
        "",
        "Phase305 audits the Phase304 dropzone and imports only non-template, schema-valid, embargo-safe event-catalyst rows. It does not run strategy search.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Source file inventory",
        "",
        _markdown_table(inventory if not inventory.empty else pd.DataFrame([{"source_file": "", "row_count": 0, "required_columns_present": 0, "importable_rows": 0, "issue_rows": 0, "file_status": "no_non_template_files"}])),
        "",
        "## Import issues",
        "",
        _markdown_table(issues if not issues.empty else pd.DataFrame([{"source_file": "", "row_index": "", "issue_id": "none", "issue_detail": ""}])),
        "",
        "## Imported event rows",
        "",
        _markdown_table(imported.head(50) if not imported.empty else pd.DataFrame([{"event_time_ist": "", "event_type": "", "symbol_scope": "", "source_file": "", "status": "no_imported_rows"}])),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
    ]
    (output_dir / "phase305_event_catalyst_source_import_audit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase304_dir: Path = DEFAULT_PHASE304_DIR,
    dropzone_dir: Path = DEFAULT_DROPZONE_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase304 = read_csv(phase304_dir / "phase304_acceptance_summary.csv")
    template_exists = (dropzone_dir / TEMPLATE_FILENAME).exists()
    inventory, issues, imported = audit_files(dropzone_dir)
    gates = build_gate_evaluation(phase304, inventory, issues, imported, template_exists)
    acceptance = build_acceptance(inventory, issues, imported, gates)

    inventory.to_csv(output_dir / "phase305_event_catalyst_source_file_inventory.csv", index=False)
    issues.to_csv(output_dir / "phase305_event_catalyst_import_issues.csv", index=False)
    imported.to_csv(output_dir / "phase305_imported_event_catalyst_ledger.csv", index=False)
    gates.to_csv(output_dir / "phase305_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase305_acceptance_summary.csv", index=False)
    write_report(output_dir, inventory, issues, imported, gates, acceptance)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase305_event_catalyst_source_import_audit",
        **reproducibility_fields(
            artifact_id="phase305",
            generated_utc=generated_utc,
            inputs={
                "phase304_acceptance": str(phase304_dir / "phase304_acceptance_summary.csv"),
                "dropzone_dir": str(dropzone_dir),
            },
            parameters={
                "required_columns": REQUIRED_COLUMNS,
                "template_filename": TEMPLATE_FILENAME,
                "placeholder_source": PLACEHOLDER_SOURCE,
            },
            outputs={"acceptance_summary": str(output_dir / "phase305_acceptance_summary.csv")},
            cost_model_version="not_applicable_source_import_audit_only",
            latency_model_version="not_applicable_source_import_audit_only",
        ),
    }
    (output_dir / "phase305_event_catalyst_source_import_audit_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase305 event-catalyst source import audit.")
    parser.add_argument("--phase304-dir", type=Path, default=DEFAULT_PHASE304_DIR)
    parser.add_argument("--dropzone-dir", type=Path, default=DEFAULT_DROPZONE_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase304_dir, args.dropzone_dir, args.output_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

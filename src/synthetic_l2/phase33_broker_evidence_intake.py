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


def _empty_template(schema: pd.DataFrame, evidence_file_id: str) -> pd.DataFrame:
    fields = schema[schema["evidence_file_id"].eq(evidence_file_id)].sort_values("field_name", kind="mergesort")
    return pd.DataFrame(columns=fields["field_name"].tolist())


def _validate_file(path: Path, schema_rows: pd.DataFrame) -> dict:
    required = schema_rows[schema_rows["required"].astype(bool)]["field_name"].astype(str).tolist()
    all_fields = schema_rows["field_name"].astype(str).tolist()
    if not path.exists():
        return {
            "file_exists_now": False,
            "row_count": 0,
            "required_columns_present": False,
            "missing_required_columns": ";".join(required),
            "unexpected_columns": "",
            "schema_validation_status": "missing_external_file",
            "acceptance_import_ready": False,
        }
    try:
        frame = pd.read_csv(path)
    except Exception as exc:  # pragma: no cover - defensive against malformed user files
        return {
            "file_exists_now": True,
            "row_count": 0,
            "required_columns_present": False,
            "missing_required_columns": ";".join(required),
            "unexpected_columns": "",
            "schema_validation_status": f"unreadable_csv:{type(exc).__name__}",
            "acceptance_import_ready": False,
        }
    columns = list(map(str, frame.columns))
    missing = [field for field in required if field not in columns]
    unexpected = [field for field in columns if field not in all_fields]
    ready = len(missing) == 0 and len(frame) > 0
    return {
        "file_exists_now": True,
        "row_count": int(len(frame)),
        "required_columns_present": len(missing) == 0,
        "missing_required_columns": ";".join(missing),
        "unexpected_columns": ";".join(unexpected),
        "schema_validation_status": "schema_ready_nonempty" if ready else "schema_present_but_not_acceptance_ready",
        "acceptance_import_ready": bool(ready),
    }


def run_phase33(checklist_path: Path, schema_path: Path, tests_path: Path, output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    template_dir = output_dir / "broker_evidence_templates"
    template_dir.mkdir(parents=True, exist_ok=True)

    checklist = _read_csv(checklist_path)
    schema = _read_csv(schema_path)
    tests = _read_csv(tests_path)

    template_rows = []
    validation_rows = []
    for record in checklist.to_dict("records"):
        evidence_file_id = str(record["evidence_file_id"])
        expected_path = Path(str(record["expected_path"]))
        schema_rows = schema[schema["evidence_file_id"].eq(evidence_file_id)].copy()
        template = _empty_template(schema, evidence_file_id)
        template_path = template_dir / f"{evidence_file_id}.template.csv"
        template.to_csv(template_path, index=False)
        template_rows.append(
            {
                "evidence_file_id": evidence_file_id,
                "template_path": str(template_path),
                "expected_external_path": str(expected_path),
                "required_fields": int(schema_rows["required"].astype(bool).sum()),
                "total_fields": int(len(schema_rows)),
                "template_status": "template_generated_not_evidence",
            }
        )
        validation = _validate_file(base_dir / expected_path, schema_rows)
        validation_rows.append(
            {
                "evidence_file_id": evidence_file_id,
                "expected_external_path": str(expected_path),
                "evidence_domain": record["evidence_domain"],
                "required_for_gate": record["required_for_gate"],
                **validation,
                "next_action": f"Populate {expected_path} using {template_path} and rerun Phase 33.",
            }
        )

    template_inventory = pd.DataFrame(template_rows)
    validation_results = pd.DataFrame(validation_rows)
    ready_files = set(validation_results.loc[validation_results["acceptance_import_ready"].astype(bool), "evidence_file_id"].astype(str))

    test_rows = []
    for record in tests.to_dict("records"):
        test_id = str(record["test_id"])
        if test_id in {"order_lineage_join", "fill_quantity_match", "average_price_match"}:
            required_files = {"broker_order_fill_events", "strategy_order_linkage"}
        elif test_id in {"charge_component_match", "net_obligation_match"}:
            required_files = {"broker_contract_note_charges", "broker_order_fill_events", "strategy_order_linkage", "broker_reconciliation_tolerances"}
        else:
            required_files = set(checklist["evidence_file_id"].astype(str))
        missing = sorted(required_files - ready_files)
        test_rows.append(
            {
                "test_id": test_id,
                "test_description": record["test_description"],
                "acceptance_threshold": record["acceptance_threshold"],
                "required_evidence_files": ";".join(sorted(required_files)),
                "missing_or_not_ready_files": ";".join(missing),
                "test_import_ready": len(missing) == 0,
                "current_status": "ready_to_run_after_evidence_import" if len(missing) == 0 else "blocked_until_required_evidence_files_import_ready",
            }
        )
    test_readiness = pd.DataFrame(test_rows)

    overall = pd.DataFrame(
        [
            {"metric": "phase33_templates_generated", "value": int(len(template_inventory)), "description": "Broker evidence CSV templates generated"},
            {"metric": "phase33_expected_external_files", "value": int(len(validation_results)), "description": "Expected external broker evidence files checked"},
            {"metric": "phase33_external_files_present", "value": int(validation_results["file_exists_now"].astype(bool).sum()), "description": "Expected external files present now"},
            {"metric": "phase33_acceptance_import_ready_files", "value": int(validation_results["acceptance_import_ready"].astype(bool).sum()), "description": "External files with required columns and nonzero rows"},
            {"metric": "phase33_missing_external_files", "value": int((~validation_results["file_exists_now"].astype(bool)).sum()), "description": "Expected external files still missing"},
            {"metric": "phase33_reconciliation_tests_ready", "value": int(test_readiness["test_import_ready"].astype(bool).sum()), "description": "Broker reconciliation tests ready to run"},
            {"metric": "phase33_acceptance_ready", "value": 0, "description": "Broker evidence intake is not acceptance-ready without imported files"},
        ]
    )

    template_inventory.to_csv(output_dir / "broker_evidence_template_inventory.csv", index=False)
    validation_results.to_csv(output_dir / "broker_evidence_file_validation.csv", index=False)
    test_readiness.to_csv(output_dir / "broker_reconciliation_test_readiness.csv", index=False)
    overall.to_csv(output_dir / "broker_evidence_intake_overall_summary.csv", index=False)
    write_report(output_dir, overall, template_inventory, validation_results, test_readiness)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "templates_generated": int(len(template_inventory)),
        "external_files_present": int(validation_results["file_exists_now"].astype(bool).sum()),
        "acceptance_import_ready_files": int(validation_results["acceptance_import_ready"].astype(bool).sum()),
        "scope": "phase33_broker_evidence_intake_templates_and_validation_not_external_evidence",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase33",
            generated_utc=generated_utc,
            inputs={
                "phase20_m01_broker_evidence_import_checklist": str(checklist_path),
                "phase20_m01_broker_evidence_schema": str(schema_path),
                "phase20_m01_broker_reconciliation_test_catalog": str(tests_path),
            },
            parameters={
                "external_evidence_dir": "external_broker_evidence",
                "template_policy": "generate_empty_csv_templates_under_outputs_phase33_not_external_evidence",
                "acceptance_import_ready_rule": "expected_file_exists_required_columns_present_and_nonzero_rows",
            },
            outputs={
                "template_inventory": str(output_dir / "broker_evidence_template_inventory.csv"),
                "file_validation": str(output_dir / "broker_evidence_file_validation.csv"),
                "test_readiness": str(output_dir / "broker_reconciliation_test_readiness.csv"),
                "overall_summary": str(output_dir / "broker_evidence_intake_overall_summary.csv"),
                "report": str(output_dir / "phase33_broker_evidence_intake_report.md"),
                "manifest": str(output_dir / "phase33_broker_evidence_intake_manifest.json"),
                "templates": str(template_dir),
            },
            random_seed="none_deterministic_schema_validation",
            scenario_ids="phase20_m01_external_broker_evidence_contract",
            cost_model_version="zerodha_equity_intraday_nse_order_formula_v2_2026_07_14",
            latency_model_version="not_applicable_broker_evidence_intake",
            base_dir=base_dir,
        )
    )
    (output_dir / "phase33_broker_evidence_intake_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def write_report(output_dir: Path, overall: pd.DataFrame, templates: pd.DataFrame, validation: pd.DataFrame, tests: pd.DataFrame) -> None:
    lines = [
        "# Phase 33 Broker Evidence Intake",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This milestone generates broker evidence CSV templates and validates whether the expected external broker files are present and import-ready.",
        "Generated templates are not evidence and are intentionally kept under `outputs/phase33/` rather than `external_broker_evidence/`.",
        "",
        "## Overall Summary",
        "",
        _markdown_table(overall),
        "",
        "## Template Inventory",
        "",
        _markdown_table(templates),
        "",
        "## File Validation",
        "",
        _markdown_table(validation),
        "",
        "## Reconciliation Test Readiness",
        "",
        _markdown_table(tests),
        "",
    ]
    (output_dir / "phase33_broker_evidence_intake_report.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate and validate broker evidence intake templates.")
    parser.add_argument("--checklist", type=Path, default=Path("outputs/phase20_m01/broker_evidence_import_checklist.csv"))
    parser.add_argument("--schema", type=Path, default=Path("outputs/phase20_m01/broker_evidence_schema.csv"))
    parser.add_argument("--tests", type=Path, default=Path("outputs/phase20_m01/broker_reconciliation_test_catalog.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase33"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_phase33(args.checklist, args.schema, args.tests, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

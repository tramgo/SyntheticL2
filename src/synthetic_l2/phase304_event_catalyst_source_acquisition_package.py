from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.phase25_event_replay_expansion import _markdown_table
from synthetic_l2.phase254_materialize_richer_raw_top5_depth_event_bars import as_int, read_csv
from synthetic_l2.phase274_focused_capital_followthrough_interpretation import metric_value
from synthetic_l2.reproducibility import reproducibility_fields


DEFAULT_PHASE303_DIR = Path("outputs/phase303")
DEFAULT_OUTPUT_DIR = Path("outputs/phase304")
DEFAULT_DROPZONE_DIR = Path("event_sources/event_catalysts/dropzone")

NEXT_ACTION = "populate_event_catalyst_dropzone_then_run_phase305_event_catalyst_source_import_audit"
REPAIR_ACTION = "repair_phase304_event_catalyst_source_acquisition_package"

REQUIRED_COLUMNS = [
    "event_time_ist",
    "event_type",
    "symbol_scope",
    "index_scope",
    "source_url_or_file",
    "confidence",
    "embargo_safe_flag",
]

OPTIONAL_COLUMNS = [
    "event_title",
    "expected_impact_side",
    "source_provider",
    "source_published_time_ist",
    "notes",
]


def build_schema_contract() -> pd.DataFrame:
    rows = [
        ("event_time_ist", "datetime_ist", "required", "Timestamp at which the market could first react; no future publication time allowed."),
        ("event_type", "category", "required", "One of macro_release, rbi_policy, earnings_result, corporate_announcement, index_rebalance, block_deal, sector_news, other."),
        ("symbol_scope", "pipe_or_comma_symbols", "required", "NSE symbols affected directly; use ALL if index-wide."),
        ("index_scope", "category", "required", "NIFTY50, BANKNIFTY, SECTOR, ALL, or NONE."),
        ("source_url_or_file", "string", "required", "External URL or local evidence file path backing the event."),
        ("confidence", "float_0_to_1", "required", "Confidence that timestamp/scope are usable without hindsight."),
        ("embargo_safe_flag", "int_0_or_1", "required", "1 only if the event time is observable no later than the reaction window start."),
        ("event_title", "string", "optional", "Human-readable event title."),
        ("expected_impact_side", "category", "optional", "unknown, bullish, bearish, mixed; optional metadata only, not a label."),
        ("source_provider", "string", "optional", "NSE, BSE, RBI, company_ir, news_vendor, manual_ledger, etc."),
        ("source_published_time_ist", "datetime_ist", "optional", "Publication time if different from event time."),
        ("notes", "string", "optional", "Free-text notes for source audit."),
    ]
    return pd.DataFrame(rows, columns=["column_name", "data_type", "required_status", "description"])


def build_allowed_event_types() -> pd.DataFrame:
    rows = [
        ("macro_release", "Scheduled or surprise macro release affecting broad market or sector."),
        ("rbi_policy", "RBI policy/rate/liquidity event with timestamped release."),
        ("earnings_result", "Company result or guidance event with symbol-specific scope."),
        ("corporate_announcement", "Exchange/company announcement with timestamped public release."),
        ("index_rebalance", "Index inclusion/exclusion/rebalance event with known effective or announcement time."),
        ("block_deal", "Large block/bulk deal or ownership event when externally timestamped."),
        ("sector_news", "Sector-wide catalyst from an external feed or manual evidence ledger."),
        ("other", "Allowed only with notes and source evidence."),
    ]
    return pd.DataFrame(rows, columns=["event_type", "description"])


def build_template() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "event_time_ist": "2026-07-10 09:15:00+05:30",
                "event_type": "other",
                "symbol_scope": "HDFCBANK",
                "index_scope": "BANKNIFTY",
                "source_url_or_file": "REPLACE_WITH_EXTERNAL_SOURCE_URL_OR_LOCAL_EVIDENCE_FILE",
                "confidence": "0.80",
                "embargo_safe_flag": "1",
                "event_title": "TEMPLATE_ROW_DELETE_OR_REPLACE",
                "expected_impact_side": "unknown",
                "source_provider": "manual_ledger",
                "source_published_time_ist": "2026-07-10 09:15:00+05:30",
                "notes": "Template only; Phase305 must reject this placeholder if not replaced.",
            }
        ],
        columns=REQUIRED_COLUMNS + OPTIONAL_COLUMNS,
    )


def build_source_inventory(dropzone_dir: Path) -> pd.DataFrame:
    files = sorted(dropzone_dir.glob("*.csv")) if dropzone_dir.exists() else []
    rows: list[dict[str, object]] = []
    for path in files:
        try:
            frame = pd.read_csv(path, nrows=20)
            columns = list(frame.columns)
            row_count = int(len(pd.read_csv(path)))
        except Exception as exc:  # pragma: no cover - defensive audit path
            columns = []
            row_count = 0
            rows.append({"path": str(path), "row_count": row_count, "required_columns_present": 0, "read_error": str(exc)})
            continue
        rows.append(
            {
                "path": str(path),
                "row_count": row_count,
                "required_columns_present": int(set(REQUIRED_COLUMNS).issubset(set(columns))),
                "read_error": "",
            }
        )
    return pd.DataFrame(rows, columns=["path", "row_count", "required_columns_present", "read_error"])


def build_gate_evaluation(phase303: pd.DataFrame, schema: pd.DataFrame, template: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    required_schema = schema[schema["required_status"].eq("required")]
    non_template_rows = 0
    if not inventory.empty:
        non_template_rows = int(inventory.loc[~inventory["path"].astype(str).str.endswith("event_catalyst_events_template.csv"), "row_count"].sum())
    gates = [
        ("P304_PHASE303_SELECTOR_COMPLETE", as_int(metric_value(phase303, "phase303_material_new_selector_complete", 0)) == 1, metric_value(phase303, "phase303_material_new_selector_complete", ""), 1),
        ("P304_PHASE303_SELECTED_EXTERNAL_SOURCE", as_int(metric_value(phase303, "phase303_selected_requires_external_source", 0)) == 1, metric_value(phase303, "phase303_selected_requires_external_source", ""), 1),
        ("P304_REQUIRED_SCHEMA_DECLARED", set(REQUIRED_COLUMNS).issubset(set(required_schema["column_name"])), len(required_schema), len(REQUIRED_COLUMNS)),
        ("P304_TEMPLATE_EMITTED", set(REQUIRED_COLUMNS + OPTIONAL_COLUMNS).issubset(set(template.columns)), len(template.columns), len(REQUIRED_COLUMNS + OPTIONAL_COLUMNS)),
        ("P304_DROPZONE_INVENTORIED", True, len(inventory), ">=0"),
        ("P304_NO_STRATEGY_SEARCH_OPENED", True, "strategy_search_allowed_now=0", "0"),
        ("P304_EXTERNAL_ROWS_STILL_REQUIRED", non_template_rows == 0, non_template_rows, 0),
        ("P304_FULL_DEPTH_JOIN_REQUIREMENT_RETAINED", as_int(metric_value(phase303, "phase303_selected_uses_top_five_depth_levels_1_to_5", 0)) == 1, metric_value(phase303, "phase303_selected_uses_top_five_depth_levels_1_to_5", ""), 1),
    ]
    return pd.DataFrame([{"gate_id": g, "passed": bool(p), "observed_value": o, "required_value": r, "severity": "hard"} for g, p, o, r in gates])


def build_acceptance(schema: pd.DataFrame, inventory: pd.DataFrame, gates: pd.DataFrame) -> pd.DataFrame:
    hard_pass = int(gates["passed"].astype(bool).sum())
    hard_rows = int(len(gates))
    non_template_files = 0 if inventory.empty else int((~inventory["path"].astype(str).str.endswith("event_catalyst_events_template.csv")).sum())
    return pd.DataFrame(
        [
            ("phase304_source_acquisition_package_complete", 1, "Phase304 source acquisition package completed"),
            ("phase304_required_schema_rows", int(schema["required_status"].eq("required").sum()), "Required event schema rows"),
            ("phase304_optional_schema_rows", int(schema["required_status"].eq("optional").sum()), "Optional event schema rows"),
            ("phase304_dropzone_file_rows", len(inventory), "CSV files inventoried in dropzone"),
            ("phase304_non_template_source_file_rows", non_template_files, "Non-template source files currently present"),
            ("phase304_external_event_rows_imported", 0, "No event rows imported in Phase304"),
            ("phase304_strategy_search_allowed_now", 0, "No strategy search until source is populated and audited"),
            ("phase304_strategy_replay_allowed", 0, "No replay"),
            ("phase304_strategy_promotion_allowed", 0, "No promotion"),
            ("phase304_paper_or_live_acceptance_allowed", 0, "No paper/live"),
            ("phase304_deployable_profitability_claim_allowed", 0, "No deployable profitability claim"),
            ("phase304_hard_gate_pass_rows", hard_pass, "Passed hard gates"),
            ("phase304_hard_gate_rows", hard_rows, "Hard gates"),
            ("phase304_next_best_action", NEXT_ACTION if hard_pass == hard_rows else REPAIR_ACTION, "Recommended next action"),
        ],
        columns=["metric", "value", "description"],
    )


def write_report(output_dir: Path, schema: pd.DataFrame, allowed_types: pd.DataFrame, inventory: pd.DataFrame, gates: pd.DataFrame, acceptance: pd.DataFrame) -> None:
    lines = [
        "# Phase304 Event-Catalyst Source Acquisition Package",
        "",
        "Phase304 creates the acquisition package for the material-new external event-catalyst source selected by Phase303. It deliberately does not run strategy search.",
        "",
        "## Acceptance summary",
        "",
        _markdown_table(acceptance),
        "",
        "## Required schema",
        "",
        _markdown_table(schema),
        "",
        "## Allowed event types",
        "",
        _markdown_table(allowed_types),
        "",
        "## Dropzone inventory",
        "",
        _markdown_table(inventory if not inventory.empty else pd.DataFrame([{"path": "", "row_count": 0, "required_columns_present": 0, "read_error": "no csv files"}])),
        "",
        "## Gates",
        "",
        _markdown_table(gates),
        "",
        f"Next action: `{NEXT_ACTION}`.",
    ]
    (output_dir / "phase304_event_catalyst_source_acquisition_package_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    phase303_dir: Path = DEFAULT_PHASE303_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    dropzone_dir: Path = DEFAULT_DROPZONE_DIR,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    dropzone_dir.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).isoformat()
    phase303 = read_csv(phase303_dir / "phase303_acceptance_summary.csv")
    schema = build_schema_contract()
    allowed_types = build_allowed_event_types()
    template = build_template()
    template_path = dropzone_dir / "event_catalyst_events_template.csv"
    if not template_path.exists():
        template.to_csv(template_path, index=False)
    template.to_csv(output_dir / "phase304_event_catalyst_events_template.csv", index=False)
    inventory = build_source_inventory(dropzone_dir)
    gates = build_gate_evaluation(phase303, schema, template, inventory)
    acceptance = build_acceptance(schema, inventory, gates)

    schema.to_csv(output_dir / "phase304_event_catalyst_schema_contract.csv", index=False)
    allowed_types.to_csv(output_dir / "phase304_allowed_event_type_catalog.csv", index=False)
    inventory.to_csv(output_dir / "phase304_event_catalyst_dropzone_inventory.csv", index=False)
    gates.to_csv(output_dir / "phase304_gate_evaluation.csv", index=False)
    acceptance.to_csv(output_dir / "phase304_acceptance_summary.csv", index=False)
    write_report(output_dir, schema, allowed_types, inventory, gates, acceptance)

    manifest = {
        "generated_utc": generated_utc,
        "scope": "phase304_event_catalyst_source_acquisition_package",
        **reproducibility_fields(
            artifact_id="phase304",
            generated_utc=generated_utc,
            inputs={"phase303_acceptance": str(phase303_dir / "phase303_acceptance_summary.csv")},
            parameters={
                "dropzone_dir": str(dropzone_dir),
                "required_columns": REQUIRED_COLUMNS,
                "next_action": NEXT_ACTION,
            },
            outputs={"acceptance_summary": str(output_dir / "phase304_acceptance_summary.csv")},
            cost_model_version="not_applicable_source_acquisition_only",
            latency_model_version="not_applicable_source_acquisition_only",
        ),
    }
    (output_dir / "phase304_event_catalyst_source_acquisition_package_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return acceptance


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Phase304 event-catalyst source acquisition package.")
    parser.add_argument("--phase303-dir", type=Path, default=DEFAULT_PHASE303_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--dropzone-dir", type=Path, default=DEFAULT_DROPZONE_DIR)
    args = parser.parse_args()
    acceptance = run(args.phase303_dir, args.output_dir, args.dropzone_dir)
    print(acceptance.to_string(index=False))


if __name__ == "__main__":
    main()

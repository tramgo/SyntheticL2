from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from synthetic_l2.reproducibility import reproducibility_fields


BROKER_EVIDENCE_FILES = [
    {
        "evidence_file_id": "broker_order_fill_events",
        "expected_path": "external_broker_evidence/broker_order_fill_events.csv",
        "evidence_domain": "broker_exchange_fill_provenance",
        "required_for_gate": "G04_risk;G02_economic",
        "minimum_rows_policy": "one row per broker/exchange order or fill event used in validation",
        "acceptance_role": "Maps strategy decisions and simulated lifecycle states to broker/exchange order and fill records.",
    },
    {
        "evidence_file_id": "broker_contract_note_charges",
        "expected_path": "external_broker_evidence/broker_contract_note_charges.csv",
        "evidence_domain": "contract_note_cost_reconciliation",
        "required_for_gate": "G04_risk;G02_economic",
        "minimum_rows_policy": "one row per contract-note order/charge component used in validation",
        "acceptance_role": "Reconciles brokerage, STT, exchange transaction charges, SEBI charges, stamp duty, GST, total charges and net obligation.",
    },
    {
        "evidence_file_id": "strategy_order_linkage",
        "expected_path": "external_broker_evidence/strategy_order_linkage.csv",
        "evidence_domain": "strategy_to_broker_order_lineage",
        "required_for_gate": "G04_risk;G02_economic",
        "minimum_rows_policy": "one row per strategy order decision linked to broker/exchange order IDs",
        "acceptance_role": "Prevents orphan broker fills or synthetic orders from being counted in acceptance evidence.",
    },
    {
        "evidence_file_id": "broker_reconciliation_tolerances",
        "expected_path": "external_broker_evidence/broker_reconciliation_tolerances.csv",
        "evidence_domain": "reconciliation_thresholds",
        "required_for_gate": "G04_risk;G02_economic",
        "minimum_rows_policy": "one row per reconciliation metric and tolerance",
        "acceptance_role": "Defines auditable tolerances before comparing broker records, contract notes and internal lifecycle P&L.",
    },
]


BROKER_EVIDENCE_FIELDS = [
    ("broker_order_fill_events", "broker_order_id", "string", True, "Broker order identifier."),
    ("broker_order_fill_events", "broker_fill_id", "string", False, "Broker or exchange fill identifier where available."),
    ("broker_order_fill_events", "exchange_order_id", "string", False, "Exchange order identifier where available."),
    ("broker_order_fill_events", "trade_date", "date", True, "Trading date in exchange timezone."),
    ("broker_order_fill_events", "exchange", "string", True, "Exchange code such as NSE."),
    ("broker_order_fill_events", "symbol", "string", True, "Trading symbol."),
    ("broker_order_fill_events", "side", "string", True, "BUY or SELL."),
    ("broker_order_fill_events", "order_type", "string", True, "MARKET, LIMIT, SL, etc."),
    ("broker_order_fill_events", "order_status", "string", True, "COMPLETE, CANCELLED, REJECTED, PARTIAL, etc."),
    ("broker_order_fill_events", "order_timestamp_ist", "datetime", True, "Broker order timestamp in IST."),
    ("broker_order_fill_events", "exchange_timestamp_ist", "datetime", False, "Exchange timestamp in IST if supplied."),
    ("broker_order_fill_events", "quantity", "integer", True, "Order quantity."),
    ("broker_order_fill_events", "filled_quantity", "integer", True, "Filled quantity."),
    ("broker_order_fill_events", "average_price", "float", True, "Broker average execution price."),
    ("broker_order_fill_events", "limit_price", "float", False, "Limit price where applicable."),
    ("broker_order_fill_events", "rejection_reason", "string", False, "Reason for rejected orders."),
    ("broker_contract_note_charges", "contract_note_id", "string", True, "Broker contract-note identifier."),
    ("broker_contract_note_charges", "broker_order_id", "string", True, "Broker order identifier linked to order/fill events."),
    ("broker_contract_note_charges", "trade_date", "date", True, "Trading date in exchange timezone."),
    ("broker_contract_note_charges", "symbol", "string", True, "Trading symbol."),
    ("broker_contract_note_charges", "buy_turnover_inr", "float", True, "Contract-note buy turnover."),
    ("broker_contract_note_charges", "sell_turnover_inr", "float", True, "Contract-note sell turnover."),
    ("broker_contract_note_charges", "brokerage_inr", "float", True, "Brokerage charged."),
    ("broker_contract_note_charges", "stt_inr", "float", True, "Securities transaction tax."),
    ("broker_contract_note_charges", "exchange_transaction_charge_inr", "float", True, "Exchange transaction charges."),
    ("broker_contract_note_charges", "sebi_charge_inr", "float", True, "SEBI turnover charge."),
    ("broker_contract_note_charges", "stamp_duty_inr", "float", True, "Stamp duty."),
    ("broker_contract_note_charges", "gst_inr", "float", True, "Goods and Services Tax."),
    ("broker_contract_note_charges", "total_charges_inr", "float", True, "Total charges from broker note."),
    ("broker_contract_note_charges", "net_obligation_inr", "float", True, "Net settlement obligation."),
    ("strategy_order_linkage", "strategy_id", "string", True, "S01-S11 strategy identifier."),
    ("strategy_order_linkage", "internal_order_id", "string", True, "Internal simulated/live order identifier."),
    ("strategy_order_linkage", "broker_order_id", "string", True, "Broker order identifier."),
    ("strategy_order_linkage", "signal_timestamp_ist", "datetime", True, "Signal timestamp in IST."),
    ("strategy_order_linkage", "order_arrival_timestamp_ist", "datetime", True, "Order arrival timestamp in IST."),
    ("strategy_order_linkage", "validation_run_id", "string", True, "Validation run identifier."),
    ("broker_reconciliation_tolerances", "reconciliation_metric", "string", True, "Metric being reconciled."),
    ("broker_reconciliation_tolerances", "absolute_tolerance_inr", "float", False, "Absolute INR tolerance."),
    ("broker_reconciliation_tolerances", "relative_tolerance_bps", "float", False, "Relative bps tolerance."),
    ("broker_reconciliation_tolerances", "acceptance_policy", "string", True, "Predeclared pass/fail policy."),
]


RECONCILIATION_TESTS = [
    ("order_lineage_join", "broker_order_fill_events joins strategy_order_linkage on broker_order_id", "zero orphan accepted validation fills"),
    ("fill_quantity_match", "filled quantities reconcile between broker records and internal lifecycle orders", "zero unexplained quantity mismatch"),
    ("average_price_match", "broker average prices reconcile to internal fill prices within tolerance", "all tested fills within tolerance"),
    ("charge_component_match", "contract-note charge components reconcile to Zerodha formula and internal costs", "all charge components within predeclared tolerance"),
    ("net_obligation_match", "contract-note net obligation reconciles to internal realized cash-flow", "all reconciled orders within predeclared tolerance"),
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


def build_evidence_schema() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "evidence_file_id": evidence_file_id,
                "field_name": field_name,
                "field_type": field_type,
                "required": required,
                "description": description,
            }
            for evidence_file_id, field_name, field_type, required, description in BROKER_EVIDENCE_FIELDS
        ]
    )


def build_import_checklist(base_dir: Path) -> pd.DataFrame:
    rows = []
    for item in BROKER_EVIDENCE_FILES:
        path = base_dir / item["expected_path"]
        rows.append(
            {
                **item,
                "file_exists_now": path.exists(),
                "current_status": "external_evidence_available_for_validation" if path.exists() else "external_evidence_missing",
                "next_action": "run_reconciliation_validation" if path.exists() else f"place evidence file at {item['expected_path']}",
            }
        )
    return pd.DataFrame(rows)


def build_reconciliation_test_catalog() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "test_id": test_id,
                "test_description": description,
                "acceptance_threshold": threshold,
                "current_status": "blocked_until_external_broker_evidence_imported",
            }
            for test_id, description, threshold in RECONCILIATION_TESTS
        ]
    )


def _required_file_for_requirement(hardening_requirement: str) -> str:
    text = str(hardening_requirement)
    if "fill_provenance" in text:
        return "broker_order_fill_events;strategy_order_linkage"
    if "contract_note" in text or "cost_reconciliation" in text or "contract_note_reconciliation" in text:
        return "broker_contract_note_charges;broker_order_fill_events;strategy_order_linkage;broker_reconciliation_tolerances"
    return "broker_order_fill_events;broker_contract_note_charges;strategy_order_linkage"


def build_gap_ledger(
    execution_roadmap: pd.DataFrame,
    broker_readiness: pd.DataFrame,
    strategy_reconciliation: pd.DataFrame,
    import_checklist: pd.DataFrame,
) -> pd.DataFrame:
    m01 = execution_roadmap[
        execution_roadmap["execution_milestone"].astype(str) == "M01_broker_external_reconciliation"
    ].copy()
    if m01.empty:
        return pd.DataFrame()
    external_files_available = bool(import_checklist["file_exists_now"].astype(bool).all())
    proxy_formula_rows = int(broker_readiness["proxy_formula_available_now"].astype(bool).sum()) if "proxy_formula_available_now" in broker_readiness else 0
    contract_note_rows = int(broker_readiness["broker_contract_note_available_now"].astype(bool).sum()) if "broker_contract_note_available_now" in broker_readiness else 0
    actual_fill_rows = int(broker_readiness["actual_fill_available_now"].astype(bool).sum()) if "actual_fill_available_now" in broker_readiness else 0
    strategy_summary = strategy_reconciliation[
        ["strategy_id", "documented_zerodha_formula_ready", "broker_contract_note_reconciliation_ready", "missing_reconciliation_items"]
    ].copy()
    rows = m01.merge(strategy_summary, on="strategy_id", how="left")
    rows["required_external_files"] = rows["hardening_requirement"].map(_required_file_for_requirement)
    rows["contract_template_available"] = True
    rows["all_required_external_files_available_now"] = external_files_available
    rows["proxy_formula_ready_items"] = proxy_formula_rows
    rows["contract_note_ready_items"] = contract_note_rows
    rows["actual_fill_ready_items"] = actual_fill_rows
    rows["broker_evidence_status"] = rows.apply(
        lambda row: "acceptance_external_evidence_available"
        if external_files_available and bool(row.get("broker_contract_note_reconciliation_ready", False))
        else "proxy_formula_available_external_broker_evidence_missing"
        if bool(row.get("documented_zerodha_formula_ready", False)) and row["dependency_status"] == "proxy_to_upgrade"
        else "external_broker_evidence_missing",
        axis=1,
    )
    rows["acceptance_requirement_met_after_contract"] = False
    rows["blocking_gap_after_contract"] = rows.apply(
        lambda row: (
            "Contract/template exists, but broker/exchange order-fill records, strategy-order linkage and contract-note rows must be imported and reconciled."
            if not external_files_available
            else "Imported files still require reconciliation validation before acceptance."
        ),
        axis=1,
    )
    columns = [
        "execution_rank",
        "gate_id",
        "strategy_id",
        "hardening_requirement",
        "action_class",
        "dependency_status",
        "required_external_files",
        "contract_template_available",
        "all_required_external_files_available_now",
        "documented_zerodha_formula_ready",
        "broker_contract_note_reconciliation_ready",
        "missing_reconciliation_items",
        "proxy_formula_ready_items",
        "contract_note_ready_items",
        "actual_fill_ready_items",
        "broker_evidence_status",
        "acceptance_requirement_met_after_contract",
        "blocking_gap_after_contract",
        "required_next_evidence",
    ]
    for column in columns:
        if column not in rows:
            rows[column] = False if column.endswith("_ready") or column.endswith("_now") else ""
    return rows[columns].sort_values(["execution_rank"], kind="mergesort")


def build_gap_summary(gap_ledger: pd.DataFrame) -> pd.DataFrame:
    if gap_ledger.empty:
        return pd.DataFrame(columns=["broker_evidence_status", "gate_id", "rows", "strategies", "acceptance_met_rows"])
    grouped = (
        gap_ledger.groupby(["broker_evidence_status", "gate_id"], sort=True)
        .agg(
            rows=("hardening_requirement", "size"),
            strategies=("strategy_id", "nunique"),
            acceptance_met_rows=("acceptance_requirement_met_after_contract", "sum"),
        )
        .reset_index()
    )
    return grouped.sort_values(["broker_evidence_status", "gate_id"], kind="mergesort")


def write_report(
    output_dir: Path,
    import_checklist: pd.DataFrame,
    evidence_schema: pd.DataFrame,
    gap_summary: pd.DataFrame,
    gap_ledger: pd.DataFrame,
    reconciliation_tests: pd.DataFrame,
) -> None:
    lines = [
        "# Phase 20 M01 Broker Evidence Contract",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This phase converts the first Phase 20 execution milestone into a strict broker/external evidence intake contract.",
        "It does not make any strategy acceptance-ready. It records the files, fields and reconciliation tests required before broker/exchange fill provenance or contract-note cost reconciliation can clear the Phase 15 risk/economic gates.",
        "",
        "## Import Checklist",
        "",
        _markdown_table(import_checklist),
        "",
        "## Gap Summary",
        "",
        _markdown_table(gap_summary),
        "",
        "## Reconciliation Test Catalog",
        "",
        _markdown_table(reconciliation_tests),
        "",
        "## Required Evidence Schema",
        "",
        _markdown_table(evidence_schema),
        "",
        "## M01 Broker Evidence Gap Ledger",
        "",
        _markdown_table(gap_ledger.head(80)),
        "",
    ]
    (output_dir / "phase20_m01_broker_evidence_contract_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_phase20_m01(paths: dict[str, Path], output_dir: Path, base_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    execution_roadmap = pd.read_csv(paths["execution_roadmap"])
    broker_readiness = pd.read_csv(paths["broker_reconciliation_readiness"])
    strategy_reconciliation = pd.read_csv(paths["economic_reconciliation_strategy_summary"])
    import_checklist = build_import_checklist(base_dir)
    evidence_schema = build_evidence_schema()
    reconciliation_tests = build_reconciliation_test_catalog()
    gap_ledger = build_gap_ledger(execution_roadmap, broker_readiness, strategy_reconciliation, import_checklist)
    gap_summary = build_gap_summary(gap_ledger)

    import_checklist.to_csv(output_dir / "broker_evidence_import_checklist.csv", index=False)
    evidence_schema.to_csv(output_dir / "broker_evidence_schema.csv", index=False)
    reconciliation_tests.to_csv(output_dir / "broker_reconciliation_test_catalog.csv", index=False)
    gap_ledger.to_csv(output_dir / "broker_external_gap_ledger.csv", index=False)
    gap_summary.to_csv(output_dir / "broker_external_gap_summary.csv", index=False)

    generated_utc = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_utc": generated_utc,
        "broker_evidence_schema_rows": int(len(evidence_schema)),
        "broker_import_checklist_rows": int(len(import_checklist)),
        "broker_import_files_available": int(import_checklist["file_exists_now"].astype(bool).sum()),
        "broker_reconciliation_test_rows": int(len(reconciliation_tests)),
        "broker_external_gap_rows": int(len(gap_ledger)),
        "broker_external_gap_summary_rows": int(len(gap_summary)),
        "broker_external_gap_acceptance_met_rows": int(gap_ledger["acceptance_requirement_met_after_contract"].astype(bool).sum()) if not gap_ledger.empty else 0,
        "scope": "phase20_m01_broker_external_evidence_contract_not_acceptance",
        "not_acceptance_result": True,
    }
    manifest.update(
        reproducibility_fields(
            artifact_id="phase20_m01",
            generated_utc=generated_utc,
            inputs={key: str(value) for key, value in paths.items()},
            parameters={
                "broker_evidence_files": BROKER_EVIDENCE_FILES,
                "broker_evidence_fields": BROKER_EVIDENCE_FIELDS,
                "reconciliation_tests": RECONCILIATION_TESTS,
            },
            outputs={
                "broker_evidence_import_checklist": str(output_dir / "broker_evidence_import_checklist.csv"),
                "broker_evidence_schema": str(output_dir / "broker_evidence_schema.csv"),
                "broker_reconciliation_test_catalog": str(output_dir / "broker_reconciliation_test_catalog.csv"),
                "broker_external_gap_ledger": str(output_dir / "broker_external_gap_ledger.csv"),
                "broker_external_gap_summary": str(output_dir / "broker_external_gap_summary.csv"),
                "report": str(output_dir / "phase20_m01_broker_evidence_contract_report.md"),
                "manifest": str(output_dir / "broker_evidence_contract_manifest.json"),
            },
            random_seed="not_applicable_deterministic_broker_evidence_contract",
            scenario_ids="phase20_M01_broker_external_reconciliation_rows",
            cost_model_version="outputs/phase12/cost_schedule.csv_and_outputs/phase16/broker_reconciliation_readiness.csv",
            latency_model_version="outputs/phase12/execution_profiles.csv_or_not_applicable",
            base_dir=base_dir,
        )
    )
    (output_dir / "broker_evidence_contract_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_report(output_dir, import_checklist, evidence_schema, gap_summary, gap_ledger, reconciliation_tests)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase 20 M01 broker/external evidence contract artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase20_m01"))
    parser.add_argument("--execution-roadmap", type=Path, default=Path("outputs/phase20/acceptance_execution_roadmap.csv"))
    parser.add_argument("--broker-reconciliation-readiness", type=Path, default=Path("outputs/phase16/broker_reconciliation_readiness.csv"))
    parser.add_argument("--economic-reconciliation-strategy-summary", type=Path, default=Path("outputs/phase16/economic_reconciliation_strategy_summary.csv"))
    parser.add_argument("--base-dir", type=Path, default=Path("."))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = {
        "execution_roadmap": args.execution_roadmap,
        "broker_reconciliation_readiness": args.broker_reconciliation_readiness,
        "economic_reconciliation_strategy_summary": args.economic_reconciliation_strategy_summary,
    }
    run_phase20_m01(paths, args.output_dir, args.base_dir)


if __name__ == "__main__":
    main()

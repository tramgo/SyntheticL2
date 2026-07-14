# Phase 33 Broker Evidence Intake

Generated UTC: 2026-07-14T18:52:46.813417+00:00

This milestone generates broker evidence CSV templates and validates whether the expected external broker files are present and import-ready.
Generated templates are not evidence and are intentionally kept under `outputs/phase33/` rather than `external_broker_evidence/`.

## Overall Summary

| metric | value | description |
| --- | --- | --- |
| phase33_templates_generated | 4 | Broker evidence CSV templates generated |
| phase33_expected_external_files | 4 | Expected external broker evidence files checked |
| phase33_external_files_present | 0 | Expected external files present now |
| phase33_acceptance_import_ready_files | 0 | External files with required columns and nonzero rows |
| phase33_missing_external_files | 4 | Expected external files still missing |
| phase33_reconciliation_tests_ready | 0 | Broker reconciliation tests ready to run |
| phase33_acceptance_ready | 0 | Broker evidence intake is not acceptance-ready without imported files |

## Template Inventory

| evidence_file_id | template_path | expected_external_path | required_fields | total_fields | template_status |
| --- | --- | --- | --- | --- | --- |
| broker_order_fill_events | outputs\phase33\broker_evidence_templates\broker_order_fill_events.template.csv | external_broker_evidence\broker_order_fill_events.csv | 11 | 16 | template_generated_not_evidence |
| broker_contract_note_charges | outputs\phase33\broker_evidence_templates\broker_contract_note_charges.template.csv | external_broker_evidence\broker_contract_note_charges.csv | 14 | 14 | template_generated_not_evidence |
| strategy_order_linkage | outputs\phase33\broker_evidence_templates\strategy_order_linkage.template.csv | external_broker_evidence\strategy_order_linkage.csv | 6 | 6 | template_generated_not_evidence |
| broker_reconciliation_tolerances | outputs\phase33\broker_evidence_templates\broker_reconciliation_tolerances.template.csv | external_broker_evidence\broker_reconciliation_tolerances.csv | 2 | 4 | template_generated_not_evidence |

## File Validation

| evidence_file_id | expected_external_path | evidence_domain | required_for_gate | file_exists_now | row_count | required_columns_present | missing_required_columns | unexpected_columns | schema_validation_status | acceptance_import_ready | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| broker_order_fill_events | external_broker_evidence\broker_order_fill_events.csv | broker_exchange_fill_provenance | G04_risk;G02_economic | False | 0 | False | broker_order_id;trade_date;exchange;symbol;side;order_type;order_status;order_timestamp_ist;quantity;filled_quantity;average_price |  | missing_external_file | False | Populate external_broker_evidence\broker_order_fill_events.csv using outputs\phase33\broker_evidence_templates\broker_order_fill_events.template.csv and rerun Phase 33. |
| broker_contract_note_charges | external_broker_evidence\broker_contract_note_charges.csv | contract_note_cost_reconciliation | G04_risk;G02_economic | False | 0 | False | contract_note_id;broker_order_id;trade_date;symbol;buy_turnover_inr;sell_turnover_inr;brokerage_inr;stt_inr;exchange_transaction_charge_inr;sebi_charge_inr;stamp_duty_inr;gst_inr;total_charges_inr;net_obligation_inr |  | missing_external_file | False | Populate external_broker_evidence\broker_contract_note_charges.csv using outputs\phase33\broker_evidence_templates\broker_contract_note_charges.template.csv and rerun Phase 33. |
| strategy_order_linkage | external_broker_evidence\strategy_order_linkage.csv | strategy_to_broker_order_lineage | G04_risk;G02_economic | False | 0 | False | strategy_id;internal_order_id;broker_order_id;signal_timestamp_ist;order_arrival_timestamp_ist;validation_run_id |  | missing_external_file | False | Populate external_broker_evidence\strategy_order_linkage.csv using outputs\phase33\broker_evidence_templates\strategy_order_linkage.template.csv and rerun Phase 33. |
| broker_reconciliation_tolerances | external_broker_evidence\broker_reconciliation_tolerances.csv | reconciliation_thresholds | G04_risk;G02_economic | False | 0 | False | reconciliation_metric;acceptance_policy |  | missing_external_file | False | Populate external_broker_evidence\broker_reconciliation_tolerances.csv using outputs\phase33\broker_evidence_templates\broker_reconciliation_tolerances.template.csv and rerun Phase 33. |

## Reconciliation Test Readiness

| test_id | test_description | acceptance_threshold | required_evidence_files | missing_or_not_ready_files | test_import_ready | current_status |
| --- | --- | --- | --- | --- | --- | --- |
| order_lineage_join | broker_order_fill_events joins strategy_order_linkage on broker_order_id | zero orphan accepted validation fills | broker_order_fill_events;strategy_order_linkage | broker_order_fill_events;strategy_order_linkage | False | blocked_until_required_evidence_files_import_ready |
| fill_quantity_match | filled quantities reconcile between broker records and internal lifecycle orders | zero unexplained quantity mismatch | broker_order_fill_events;strategy_order_linkage | broker_order_fill_events;strategy_order_linkage | False | blocked_until_required_evidence_files_import_ready |
| average_price_match | broker average prices reconcile to internal fill prices within tolerance | all tested fills within tolerance | broker_order_fill_events;strategy_order_linkage | broker_order_fill_events;strategy_order_linkage | False | blocked_until_required_evidence_files_import_ready |
| charge_component_match | contract-note charge components reconcile to Zerodha formula and internal costs | all charge components within predeclared tolerance | broker_contract_note_charges;broker_order_fill_events;broker_reconciliation_tolerances;strategy_order_linkage | broker_contract_note_charges;broker_order_fill_events;broker_reconciliation_tolerances;strategy_order_linkage | False | blocked_until_required_evidence_files_import_ready |
| net_obligation_match | contract-note net obligation reconciles to internal realized cash-flow | all reconciled orders within predeclared tolerance | broker_contract_note_charges;broker_order_fill_events;broker_reconciliation_tolerances;strategy_order_linkage | broker_contract_note_charges;broker_order_fill_events;broker_reconciliation_tolerances;strategy_order_linkage | False | blocked_until_required_evidence_files_import_ready |

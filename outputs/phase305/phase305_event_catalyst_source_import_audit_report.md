# Phase305 Event-Catalyst Source Import Audit

Phase305 audits the Phase304 dropzone and imports only non-template, schema-valid, embargo-safe event-catalyst rows. It does not run strategy search.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase305_event_catalyst_import_audit_complete | 1 | Phase305 event-catalyst source import audit completed |
| phase305_candidate_source_file_rows | 0 | Non-template CSV files audited |
| phase305_candidate_source_raw_rows | 0 | Raw candidate rows read |
| phase305_imported_event_rows | 0 | Rows imported into event catalyst source ledger |
| phase305_issue_rows | 0 | Import issue rows |
| phase305_template_rows_imported | 0 | Template rows are never imported |
| phase305_strategy_search_allowed_now | 0 | No strategy search until imported events exist and Phase306 precommits join |
| phase305_strategy_replay_allowed | 0 | No replay |
| phase305_strategy_promotion_allowed | 0 | No promotion |
| phase305_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase305_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase305_hard_gate_pass_rows | 8 | Passed hard gates |
| phase305_hard_gate_rows | 8 | Hard gates |
| phase305_next_best_action | populate_event_catalyst_dropzone_with_non_template_source_rows_then_rerun_phase305 | Recommended next action |

## Source file inventory

| source_file | row_count | required_columns_present | importable_rows | issue_rows | file_status |
| --- | --- | --- | --- | --- | --- |
|  | 0 | 0 | 0 | 0 | no_non_template_files |

## Import issues

| source_file | row_index | issue_id | issue_detail |
| --- | --- | --- | --- |
|  |  | none |  |

## Imported event rows

| event_time_ist | event_type | symbol_scope | source_file | status |
| --- | --- | --- | --- | --- |
|  |  |  |  | no_imported_rows |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P305_PHASE304_PACKAGE_COMPLETE | True | 1 | 1 | hard |
| P305_TEMPLATE_EXISTS | True | 1 | 1 | hard |
| P305_DROPZONE_AUDITED | True | 0 | >=0 | hard |
| P305_PLACEHOLDERS_NOT_IMPORTED | True | 0 | no_placeholder_imports | hard |
| P305_IMPORT_REQUIRES_NON_TEMPLATE_FILES | True | candidate_files=0;imported=0 | no import from template | hard |
| P305_ISSUES_LEDGER_WRITTEN | True | 0 | >=0 | hard |
| P305_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P305_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

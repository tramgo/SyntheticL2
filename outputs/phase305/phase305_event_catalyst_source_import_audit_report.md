# Phase305 Event-Catalyst Source Import Audit

Phase305 audits the Phase304 dropzone and imports only non-template, schema-valid, embargo-safe event-catalyst rows. It does not run strategy search.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase305_event_catalyst_import_audit_complete | 1 | Phase305 event-catalyst source import audit completed |
| phase305_candidate_source_file_rows | 2 | Non-template CSV files audited |
| phase305_candidate_source_raw_rows | 2 | Raw candidate rows read |
| phase305_imported_event_rows | 2 | Rows imported into event catalyst source ledger |
| phase305_issue_rows | 0 | Import issue rows |
| phase305_template_rows_imported | 0 | Template rows are never imported |
| phase305_strategy_search_allowed_now | 0 | No strategy search until imported events exist and Phase306 precommits join |
| phase305_strategy_replay_allowed | 0 | No replay |
| phase305_strategy_promotion_allowed | 0 | No promotion |
| phase305_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase305_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase305_hard_gate_pass_rows | 8 | Passed hard gates |
| phase305_hard_gate_rows | 8 | Hard gates |
| phase305_next_best_action | run_phase306_event_catalyst_top5_depth_join_precommit_no_strategy_search | Recommended next action |

## Source file inventory

| source_file | row_count | required_columns_present | importable_rows | issue_rows | file_status |
| --- | --- | --- | --- | --- | --- |
| event_sources\event_catalysts\dropzone\event_catalysts_rbi_mpc_20260805.csv | 1 | 1 | 1 | 0 | importable |
| event_sources\event_catalysts\dropzone\event_catalysts_synthetic_calendar_rbi_mpc_20260820.csv | 1 | 1 | 1 | 0 | importable |

## Import issues

| source_file | row_index | issue_id | issue_detail |
| --- | --- | --- | --- |
|  |  | none |  |

## Imported event rows

| event_time_ist | event_type | symbol_scope | index_scope | source_url_or_file | confidence | embargo_safe_flag | event_title | expected_impact_side | source_provider | source_published_time_ist | notes | source_file |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-08-05 10:00:00+05:30 | rbi_policy | ALL | ALL | https://www.youtube.com/watch?v=XIdD58WOX30 | 0.9 | 1 | RBI MPC monetary policy statement - repo rate unchanged at 5.25% | unknown | RBI public broadcast and financial press | 2026-08-05 10:00:00+05:30 | Seed event catalyst row verified from public sources: RBI Governor monetary policy statement was scheduled for August 5 2026 at 10:00 IST; financial press reported repo rate unchanged at 5.25% and neutral stance. Use as exogenous market-wide event timestamp only, not as a directional label. | event_sources\event_catalysts\dropzone\event_catalysts_rbi_mpc_20260805.csv |
| 2026-08-20 15:30:00+05:30 | rbi_policy | ALL | ALL | event_sources/event_catalysts/dropzone/event_catalysts_rbi_mpc_20260805.csv | 0.8 | 1 | Synthetic-calendar aligned RBI MPC catalyst timestamp for dense-lake join validation | unknown | Derived synthetic-calendar alignment from verified RBI MPC seed event | 2026-08-05 10:00:00+05:30 | Synthetic-calendar alignment row for join validation only: preserves RBI MPC event type from the verified 2026-08-05 source, but shifts event_time_ist to 2026-08-20 15:30 IST so the event window overlaps row-level timestamps in the current dense synthetic top-five depth lake. Do not treat as a real-world event date, real-world event time, or directional label. | event_sources\event_catalysts\dropzone\event_catalysts_synthetic_calendar_rbi_mpc_20260820.csv |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P305_PHASE304_PACKAGE_COMPLETE | True | 1 | 1 | hard |
| P305_TEMPLATE_EXISTS | True | 1 | 1 | hard |
| P305_DROPZONE_AUDITED | True | 2 | >=0 | hard |
| P305_PLACEHOLDERS_NOT_IMPORTED | True | 2 | no_placeholder_imports | hard |
| P305_IMPORT_REQUIRES_NON_TEMPLATE_FILES | True | candidate_files=2;imported=2 | no import from template | hard |
| P305_ISSUES_LEDGER_WRITTEN | True | 0 | >=0 | hard |
| P305_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P305_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

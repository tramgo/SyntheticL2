# Phase 37 Collector Ledger Verifier

Generated UTC: 2026-07-16T13:42:04.537706+00:00

This phase verifies collector instrumentation ledgers for Stage A2 consumption.
Dry-run ledgers can pass structural checks, but they are not live collector evidence and therefore cannot enable Class B capture promotion.

## schema_validation

| artifact_name | required_columns | missing_columns | missing_column_names | schema_valid |
| --- | --- | --- | --- | --- |
| session_ledger | 10 | 0 |  | True |
| tick_sequence_diagnostics | 7 | 0 |  | True |
| drop_counter_ledger | 9 | 0 |  | True |

## session_validation

| collector_run_id | session_id | opened_utc_present | closed_utc_present | close_reason_present | tick_rows | sequence_rows | session_sequence_count_match | session_sequence_bounds_match | session_valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase36_dry_run | phase36_dry_run_session_0001 | True | True | True | 3 | 3 | True | True | True |

## sequence_validation

| session_id | sequence_rows | sequence_gap_count | duplicate_sequence_count | monotonic_sequence_pass |
| --- | --- | --- | --- | --- |
| phase36_dry_run_session_0001 | 3 | 0 | 0 | True |

## drop_counter_validation

| session_id | subscribed_symbols | drop_counter_symbols | missing_drop_counter_symbols | drop_counter_coverage_pass | total_dropped_count | total_duplicate_count | total_stale_count | total_out_of_order_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase36_dry_run_session_0001 | 2 | 2 |  | True | 0 | 0 | 0 | 0 |

## promotion_gate

| gate | passed | description |
| --- | --- | --- |
| schema_pass | 1 | All required collector-ledger columns are present |
| session_boundary_pass | 1 | Session rows reconcile to sequence rows and sequence bounds |
| local_sequence_pass | 1 | Local sequence IDs are contiguous and non-duplicated per session |
| drop_counter_coverage_pass | 1 | Drop-counter rows cover all subscribed session symbols |
| live_collector_evidence | 0 | Ledgers come from live collector output rather than dry-run scaffolding |
| stage_a2_collector_evidence_ready | 0 | Collector-side Stage A2 evidence can be consumed for Class B promotion checks |

## summary

| metric | value | description |
| --- | --- | --- |
| phase37_schema_artifacts_checked | 3 | Collector ledger artifacts checked for required schema |
| phase37_schema_missing_columns | 0 | Missing required collector-ledger columns |
| phase37_session_rows_verified | 1 | Session ledger rows verified |
| phase37_sequence_sessions_verified | 1 | Sessions with sequence diagnostics verified |
| phase37_drop_counter_sessions_verified | 1 | Sessions with drop-counter coverage verified |
| phase37_schema_pass | 1 | Schema gate pass flag |
| phase37_session_boundary_pass | 1 | Session-boundary gate pass flag |
| phase37_local_sequence_pass | 1 | Local-sequence gate pass flag |
| phase37_drop_counter_coverage_pass | 1 | Drop-counter coverage gate pass flag |
| phase37_live_collector_evidence | 0 | Live collector evidence flag |
| phase37_stage_a2_collector_evidence_ready | 0 | Collector evidence ready for Class B checks |

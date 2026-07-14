# Phase 36 Collector Instrumentation Package

Generated UTC: 2026-07-14T19:20:49.318188+00:00

This package supplies collector-side instrumentation required by Stage A2: session boundary ledgers, callback local sequence IDs and dropped-message counters.
It is implementation scaffolding and dry-run proof, not evidence that the live Zerodha collector has already captured new Class B days.

## Summary

| metric | value | description |
| --- | --- | --- |
| phase36_required_schema_fields | 21 | Required collector instrumentation schema fields |
| phase36_dry_run_session_rows | 1 | Dry-run connection/session ledger rows |
| phase36_dry_run_sequence_rows | 3 | Dry-run local sequence diagnostic rows |
| phase36_dry_run_drop_counter_rows | 2 | Dry-run drop counter rows |
| phase36_live_collector_integrated | 0 | Live collector integration status in this workspace |
| phase36_class_b_capture_enabled | 0 | Whether new live captures can be marked Class B from this package alone |

## Required Schema

| artifact_name | field_name | field_type | required_status | field_purpose |
| --- | --- | --- | --- | --- |
| raw_tick_enrichment | collector_run_id | string | required | Stable process/run identifier for the collector instance. |
| raw_tick_enrichment | session_id | string | required | Connection/session identifier attached to each tick. |
| raw_tick_enrichment | callback_batch_id | integer | required | Monotonic callback batch number within a collector run. |
| raw_tick_enrichment | local_sequence_id | integer | required | Monotonic callback-order tick sequence assigned before persistence. |
| raw_tick_enrichment | callback_received_utc | timestamp | required | UTC timestamp captured once per websocket callback before persistence. |
| raw_tick_enrichment | callback_received_monotonic_ns | integer | required | Monotonic clock captured once per websocket callback before persistence. |
| connection_session_ledger | collector_run_id | string | required | Collector process/run identifier. |
| connection_session_ledger | session_id | string | required | Connection/session identifier. |
| connection_session_ledger | opened_utc | timestamp | required | Session open timestamp. |
| connection_session_ledger | closed_utc | timestamp | required | Session close timestamp. |
| connection_session_ledger | open_reason | string | required | Connect/reconnect/subscription reason. |
| connection_session_ledger | close_reason | string | required | Normal close, reconnect, network fault, broker close or process stop. |
| connection_session_ledger | subscribed_symbols | string | required | Subscribed symbols joined by semicolon. |
| connection_session_ledger | first_local_sequence_id | integer | required | First local sequence attached to the session. |
| connection_session_ledger | last_local_sequence_id | integer | required | Last local sequence attached to the session. |
| connection_session_ledger | tick_rows | integer | required | Ticks observed in the session. |
| drop_counter_ledger | symbol | string | required | Instrument symbol. |
| drop_counter_ledger | dropped_count | integer | required | Collector/session observed dropped-message count. |
| drop_counter_ledger | duplicate_count | integer | required | Collector/session observed duplicate count. |
| drop_counter_ledger | stale_count | integer | required | Collector/session observed stale-message count. |
| drop_counter_ledger | out_of_order_count | integer | required | Collector/session observed out-of-order count. |

## Collector Interface

| interface_method | collector_hook | stage_a2_evidence |
| --- | --- | --- |
| open_session | Call after websocket connection and subscription are established. | connection_session_ledger row opened |
| enrich_ticks | Call as the first operation inside on_ticks before parquet writes. | collector_run_id/session_id/callback_batch_id/local_sequence_id/callback timestamps on every tick |
| record_drop_counters | Call when duplicate, stale, dropped or out-of-order symptoms/counters are detected. | drop_counter_ledger row per session/symbol observation |
| close_session | Call on normal close, reconnect, network fault, broker close or process stop. | connection_session_ledger row closed with reason |
| flush | Call on shutdown and after close/reconnect boundaries. | CSV ledgers persisted for Stage A2 ingestion |

## Integration Checklist

| priority | check_id | required_change | current_status |
| --- | --- | --- | --- |
| 1 | import_helper | Import CollectorInstrumentation in the live Zerodha websocket collector. | pending_live_collector_integration |
| 2 | session_boundaries | Wrap connect/reconnect/subscription lifecycle with open_session and close_session. | pending_live_collector_integration |
| 3 | tick_enrichment | Call enrich_ticks at the start of on_ticks and persist returned tick rows. | pending_live_collector_integration |
| 4 | drop_counters | Persist duplicate/stale/out-of-order/drop counters through record_drop_counters. | pending_live_collector_integration |
| 5 | flush_ledgers | Flush ledgers at shutdown and reconnect boundaries beside raw parquet output. | pending_live_collector_integration |
| 6 | stage_a2_ingestion | Point Stage A2/Phase 35 scanners at emitted ledgers for Class B promotion checks. | pending_after_live_capture |

## Dry-Run Session Ledger

| collector_run_id | session_id | exchange | opened_utc | closed_utc | open_reason | close_reason | subscribed_symbols | subscribed_symbol_count | first_local_sequence_id | last_local_sequence_id | tick_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase36_dry_run | phase36_dry_run_session_0001 | NSE | 2026-07-14T19:20:49.304943+00:00 | 2026-07-14T19:20:49.304985+00:00 | dry_run_connect | dry_run_normal_close | HDFCBANK;INFY | 2 | 1 | 3 | 3 |

## Dry-Run Tick Sequence Diagnostics

| collector_run_id | session_id | callback_batch_id | local_sequence_id | symbol | callback_received_utc | callback_received_monotonic_ns |
| --- | --- | --- | --- | --- | --- | --- |
| phase36_dry_run | phase36_dry_run_session_0001 | 1 | 1 | HDFCBANK | 2026-07-14T19:20:49.304961+00:00 | 135722986756500 |
| phase36_dry_run | phase36_dry_run_session_0001 | 1 | 2 | INFY | 2026-07-14T19:20:49.304961+00:00 | 135722986756500 |
| phase36_dry_run | phase36_dry_run_session_0001 | 1 | 3 | HDFCBANK | 2026-07-14T19:20:49.304961+00:00 | 135722986756500 |

## Dry-Run Drop Counter Ledger

| collector_run_id | session_id | symbol | observed_utc | source | dropped_count | duplicate_count | stale_count | out_of_order_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase36_dry_run | phase36_dry_run_session_0001 | HDFCBANK | 2026-07-14T19:20:49.304978+00:00 | collector_callback | 0 | 0 | 0 | 0 |
| phase36_dry_run | phase36_dry_run_session_0001 | INFY | 2026-07-14T19:20:49.304982+00:00 | collector_callback | 0 | 0 | 0 | 0 |

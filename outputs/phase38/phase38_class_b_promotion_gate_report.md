# Phase 38 Class B Day Promotion Gate

Generated UTC: 2026-07-16T13:46:56.661117+00:00

This gate combines raw day coverage, computable diagnostics and collector-ledger verifier evidence into a day-level Class B promotion decision.
It does not run strategy replay; it determines whether real-data days are eligible to feed those replay gates.

## Summary

| metric | value | description |
| --- | --- | --- |
| phase38_days_evaluated | 1 | Trade-date/exchange days evaluated for Class B promotion |
| phase38_class_b_promoted_days | 0 | Days promoted to Class B by the Phase 38 gate |
| phase38_failed_gate_rows | 2 | Failed Class B promotion gate rows |
| phase38_required_complete_days_min | 5 | Minimum complete Class B days required |
| phase38_required_complete_days_target | 10 | Target complete Class B days required |
| phase38_days_needed_for_min | 5 | Additional promoted Class B days needed for minimum |
| phase38_days_needed_for_target | 10 | Additional promoted Class B days needed for target |
| phase38_replay_allowed_rows | 0 | Replay rows unlocked by Class B promotion gate |

## Day Decision

| trade_date | exchange | class_b_promotion_allowed | passed_gates | failed_gates | blocking_gates | promotion_status |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07-13 | NSE | False | 4 | 2 | collector_live_evidence;collector_stage_a2_evidence_ready | blocked_until_live_collector_evidence_and_all_diagnostics_pass |

## Gate Ledger

| trade_date | exchange | gate_id | passed | observed_value | required_next_action |
| --- | --- | --- | --- | --- | --- |
| 2026-07-13 | NSE | raw_full_universe_coverage | True | 32/32 symbols present |  |
| 2026-07-13 | NSE | timestamp_semantics_computable | True | 32/32 symbols pass computable timestamp checks |  |
| 2026-07-13 | NSE | lossless_compaction_computable | True | 32/32 symbols reconcile raw rows/files to Phase 1 and manifest counts |  |
| 2026-07-13 | NSE | drop_duplicate_stale_scan_computable | True | 32/32 symbols have computable duplicate/stale symptom scans |  |
| 2026-07-13 | NSE | collector_live_evidence | False | phase37_live_collector_evidence=0 | Run Phase 37 against actual live collector ledgers with --collector-source live_collector. |
| 2026-07-13 | NSE | collector_stage_a2_evidence_ready | False | phase37_stage_a2_collector_evidence_ready=0 | Pass Phase 37 schema/session/sequence/drop-counter gates on live collector ledgers. |

## Action Plan

| priority | gate_id | failed_rows | required_next_action | acceptance_effect |
| --- | --- | --- | --- | --- |
| 1 | collector_live_evidence | 1 | Run Phase 37 against actual live collector ledgers with --collector-source live_collector. | Required before any day can be counted as Class B event-grade evidence. |
| 2 | collector_stage_a2_evidence_ready | 1 | Pass Phase 37 schema/session/sequence/drop-counter gates on live collector ledgers. | Required before any day can be counted as Class B event-grade evidence. |

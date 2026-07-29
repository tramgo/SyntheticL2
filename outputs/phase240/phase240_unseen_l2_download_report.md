# Phase240 Unseen Real L2 Download Report

Generated UTC: 2026-07-29T07:43:47.554590+00:00

Phase240 downloads raw unseen real L2 dates from Azure Files using a process-provided SAS token.
The SAS value is not written to disk. Downloads are resumable by local file-size checks.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase240_unseen_raw_l2_download_complete | 0 | Whether the full unseen raw L2 plan downloaded or already existed |
| phase240_partial_attempt | 1 | Whether --max-dates or --max-files limited the run |
| phase240_target_trade_dates | 2026-07-17 | Target unseen dates attempted |
| phase240_remote_manifest_files | 300 | Remote files in attempted manifest |
| phase240_remote_manifest_bytes | 10484123 | Remote bytes in attempted manifest |
| phase240_completed_files | 300 | Files processed |
| phase240_failed_files | 0 | Files failed |
| phase240_completed_dates | 0 | Dates fully downloaded |
| phase240_elapsed_seconds | 70.7451 | Elapsed seconds |
| phase240_validation_execution_allowed_now | 0 | Phase240 does not run validation |
| phase240_strategy_promotion_allowed | 0 | No strategy promotion from Phase240 |
| phase240_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase240 |
| phase240_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase240 |
| phase240_next_best_action | resume_phase240_unseen_raw_l2_download_no_paper_live | Recommended next milestone |

## Date Summary

| trade_date | remote_files | remote_bytes | symbols | completed_files | downloaded_files | skipped_existing_files | failed_files | completed_bytes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-17 | 300 | 10484123 | 1 | 300 | 0 | 300 | 0 | 10484123 |

## Failed Files

_No rows._

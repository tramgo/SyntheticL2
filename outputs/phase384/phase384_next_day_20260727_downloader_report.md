# Phase384 Next-Day 2026-07-27 Downloader

Generated: 2026-08-11T20:05:16.924671+00:00

Phase384 executes the Phase383 event-density repair download. It downloads/verifies the next no-lookahead real-L2 target day and does not run a strategy retest.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase384_next_day_20260727_downloader_complete | 1 | Phase384 complete |
| phase384_target_trade_date | 2026-07-27 | Phase383 target date |
| phase384_pending_post_close_event_rows | 13 | Known pending rows unlocked by target |
| phase384_sas_env_present | 1 | Supported SAS env present |
| phase384_truststore_injected | 1 | Truststore injected |
| phase384_dry_run | 0 | Dry-run mode |
| phase384_workers | 128 | Concurrent workers |
| phase384_discovered_file_rows | 5665 | Discovered target file rows |
| phase384_discovered_symbols | 32 | Discovered target symbols |
| phase384_download_manifest_rows | 5665 | Download manifest rows |
| phase384_existing_file_rows | 5662 | Existing/skipped file rows |
| phase384_downloaded_file_rows | 3 | Downloaded file rows |
| phase384_error_file_rows | 0 | Per-file error rows |
| phase384_local_symbols_after | 32 | Local symbols after |
| phase384_local_parquet_files_after | 5665 | Local parquet files after |
| phase384_local_bytes_after | 198041216 | Local bytes after |
| phase384_local_full_universe_after | 1 | Full universe local after |
| phase384_strategy_retest_executed_now | 0 | No retest in this phase |
| phase384_strategy_promotion_allowed | 0 | No promotion |
| phase384_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase384_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase384_hard_gate_pass_rows | 6 | Passed hard gates |
| phase384_hard_gate_rows | 6 | Hard gates |
| phase384_next_best_action | refresh_catalyst_event_count_after_20260727_then_rerun_frozen_retest_no_search | Recommended next action |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P384_PHASE383_PRECOMMIT_PRESENT | 1 | Phase383 complete |
| P384_TARGET_SELECTED | 1 | 2026-07-27 |
| P384_DISCOVERY_OR_WAIT_RECORDED | 1 | discovered_rows=5665; error=0 |
| P384_FULL_UNIVERSE_VERIFIED_OR_PENDING | 1 | local_symbols=32 |
| P384_NO_SECRET_MATERIAL_RECORDED | 1 | secret_rows=0 |
| P384_NO_STRATEGY_RETEST_OR_PROMOTION | 1 | download_only |

No retest, promotion, paper/live acceptance, or deployable profitability claim is opened.

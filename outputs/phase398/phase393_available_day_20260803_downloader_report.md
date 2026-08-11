# Phase393 Available-Day 2026-08-03 Downloader

Generated: 2026-08-11T21:01:30.933694+00:00

| metric | value | description |
| --- | --- | --- |
| phase393_available_day_20260803_downloader_complete | 1 | Phase393 complete |
| phase393_target_trade_date | 2026-08-04 | First nearby full partition after shell-only 2026-07-28/29 |
| phase393_pending_post_close_event_rows_from_phase392 | 9 | Rows from natural 2026-07-28 target |
| phase393_sas_env_present | 1 | Supported SAS env present |
| phase393_truststore_injected | 1 | Truststore injected |
| phase393_dry_run | 0 | Dry-run mode |
| phase393_workers | 128 | Concurrent workers |
| phase393_discovered_file_rows | 50499 | Discovered target file rows |
| phase393_discovered_symbols | 32 | Discovered target symbols |
| phase393_download_manifest_rows | 50499 | Download manifest rows |
| phase393_existing_file_rows | 50499 | Existing/skipped file rows |
| phase393_downloaded_file_rows | 0 | Downloaded file rows |
| phase393_error_file_rows | 0 | Per-file error rows |
| phase393_local_symbols_after | 32 | Local symbols after |
| phase393_local_parquet_files_after | 50499 | Local parquet files after |
| phase393_local_bytes_after | 1761442001 | Local bytes after |
| phase393_local_full_universe_after | 1 | Full universe local after |
| phase393_strategy_retest_executed_now | 0 | No retest |
| phase393_strategy_promotion_allowed | 0 | No promotion |
| phase393_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase393_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase393_next_best_action | refresh_catalyst_event_count_after_20260803_then_rerun_frozen_retest_no_search | Recommended next action |

| gate_id | passed | evidence |
| --- | --- | --- |
| P393_PHASE392_PROBE_PRESENT | 1 | Phase392 probe present |
| P393_TARGET_AVAILABLE_DISCOVERY | 1 | discovered_rows=50499; local_full=1; error=0 |
| P393_FULL_UNIVERSE_VERIFIED_OR_PENDING | 1 | local_symbols=32 |
| P393_NO_SECRET_MATERIAL_RECORDED | 1 | secret_rows=0 |
| P393_NO_RETEST_OR_PROMOTION | 1 | download_only |

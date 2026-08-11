# Phase392 Next-Day 2026-07-28 Downloader

Generated: 2026-08-11T20:20:18.709110+00:00

| metric | value | description |
| --- | --- | --- |
| phase392_next_day_20260728_downloader_complete | 0 | Phase392 complete |
| phase392_target_trade_date | 2026-07-28 | Next no-lookahead target |
| phase392_pending_post_close_event_rows | 9 | Known pending rows unlocked by target |
| phase392_sas_env_present | 1 | Supported SAS env present |
| phase392_truststore_injected | 1 | Truststore injected |
| phase392_dry_run | 1 | Dry-run mode |
| phase392_workers | 128 | Concurrent workers |
| phase392_discovered_file_rows | 0 | Discovered target file rows |
| phase392_discovered_symbols | 0 | Discovered target symbols |
| phase392_download_manifest_rows | 0 | Download manifest rows |
| phase392_existing_file_rows | 0 | Existing/skipped file rows |
| phase392_downloaded_file_rows | 0 | Downloaded file rows |
| phase392_error_file_rows | 0 | Per-file error rows |
| phase392_local_symbols_after | 0 | Local symbols after |
| phase392_local_parquet_files_after | 0 | Local parquet files after |
| phase392_local_bytes_after | 0 | Local bytes after |
| phase392_local_full_universe_after | 0 | Full universe local after |
| phase392_strategy_retest_executed_now | 0 | No retest |
| phase392_strategy_promotion_allowed | 0 | No promotion |
| phase392_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase392_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase392_next_best_action | refresh_catalyst_event_count_after_20260728_then_rerun_frozen_retest_no_search | Recommended next action |

| gate_id | passed | evidence |
| --- | --- | --- |
| P392_PHASE391_PRESENT | 1 | Phase391 complete |
| P392_TARGET_SELECTED | 1 | 2026-07-28 |
| P392_DISCOVERY_OR_WAIT_RECORDED | 0 | discovered_rows=0; error=0 |
| P392_FULL_UNIVERSE_VERIFIED_OR_PENDING | 1 | local_symbols=0 |
| P392_NO_SECRET_MATERIAL_RECORDED | 1 | secret_rows=0 |
| P392_NO_RETEST_OR_PROMOTION | 1 | download_only |

# Phase114 Drop-zone Import Integrity Verifier

Generated UTC: 2026-07-19T22:51:00.270044+00:00

Phase114 verifies whether Phase113's real-L2 drop-zone import plan has been executed with source/target count and byte integrity.
It is safe in dry-run state and does not enable strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase114_integrity_rows | 32 | Import-plan rows checked for source/target integrity |
| phase114_target_rows_present | 0 | Rows where target symbol directory exists |
| phase114_integrity_verified_rows | 0 | Rows with matching source/target file counts and bytes |
| phase114_phase113_execute_mode | 0 | Inherited Phase113 execute mode |
| phase114_dry_run_integrity_ready | 1 | 1 means dry-run plan is ready and no copied target exists yet |
| phase114_executed_import_integrity_pass | 0 | 1 means executed import has full source/target integrity |
| phase114_check_rows | 4 | Integrity checks executed |
| phase114_check_pass_rows | 4 | Integrity checks passing |
| phase114_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase114_recommend_next_action | run_phase113_with_execute_after_new_real_days_then_rerun_phase114_phase96_phase110 | Recommended next milestone |

## Integrity Checks

| check_id | passed | detail |
| --- | --- | --- |
| P114_PHASE113_PLAN_AVAILABLE | True | planned_rows=32 |
| P114_DRY_RUN_STATE_RECOGNIZED | True | phase113_execute_mode=0; target_rows=0 |
| P114_EXECUTED_IMPORT_FULLY_VERIFIED | True | phase113_execute_mode=0; verified_rows=0; planned_rows=32 |
| P114_REPLAY_LOCK_PRESERVED | True | Phase114 verifies import integrity only and does not unlock strategy replay. |

## Integrity Rows

| symbol | trade_date | exchange | planned_action | source_symbol_dir | target_symbol_dir | source_file_count | target_file_count | source_bytes | target_bytes | target_exists | count_match | byte_match | integrity_pass | integrity_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=ADANIPORTS | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=ADANIPORTS | 1569 | 0 | 54744007 | 0 | False | False | False | False | target_missing_not_executed |
| AXISBANK | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=AXISBANK | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=AXISBANK | 1569 | 0 | 55030126 | 0 | False | False | False | False | target_missing_not_executed |
| BAJAJ-AUTO | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=BAJAJ-AUTO | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=BAJAJ-AUTO | 1569 | 0 | 55531219 | 0 | False | False | False | False | target_missing_not_executed |
| BANKBEES | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=BANKBEES | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=BANKBEES | 1569 | 0 | 54858026 | 0 | False | False | False | False | target_missing_not_executed |
| BHARTIARTL | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=BHARTIARTL | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=BHARTIARTL | 1569 | 0 | 55190740 | 0 | False | False | False | False | target_missing_not_executed |
| BPCL | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=BPCL | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=BPCL | 1569 | 0 | 54256472 | 0 | False | False | False | False | target_missing_not_executed |
| BRITANNIA | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=BRITANNIA | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=BRITANNIA | 1569 | 0 | 54177058 | 0 | False | False | False | False | target_missing_not_executed |
| CIPLA | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=CIPLA | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=CIPLA | 1569 | 0 | 54425687 | 0 | False | False | False | False | target_missing_not_executed |
| DRREDDY | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=DRREDDY | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=DRREDDY | 1569 | 0 | 54592935 | 0 | False | False | False | False | target_missing_not_executed |
| GOLDBEES | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=GOLDBEES | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=GOLDBEES | 1568 | 0 | 54501651 | 0 | False | False | False | False | target_missing_not_executed |
| HCLTECH | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=HCLTECH | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=HCLTECH | 1569 | 0 | 56185830 | 0 | False | False | False | False | target_missing_not_executed |
| HDFCBANK | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=HDFCBANK | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=HDFCBANK | 1569 | 0 | 56719345 | 0 | False | False | False | False | target_missing_not_executed |
| HINDUNILVR | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=HINDUNILVR | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=HINDUNILVR | 1569 | 0 | 54585232 | 0 | False | False | False | False | target_missing_not_executed |
| ICICIBANK | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=ICICIBANK | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=ICICIBANK | 1569 | 0 | 55797042 | 0 | False | False | False | False | target_missing_not_executed |
| INFY | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=INFY | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=INFY | 1569 | 0 | 56702770 | 0 | False | False | False | False | target_missing_not_executed |
| ITBEES | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=ITBEES | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=ITBEES | 1569 | 0 | 54430478 | 0 | False | False | False | False | target_missing_not_executed |
| ITC | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=ITC | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=ITC | 1569 | 0 | 54356124 | 0 | False | False | False | False | target_missing_not_executed |
| JUNIORBEES | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=JUNIORBEES | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=JUNIORBEES | 1568 | 0 | 54832707 | 0 | False | False | False | False | target_missing_not_executed |
| KOTAKBANK | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=KOTAKBANK | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=KOTAKBANK | 1569 | 0 | 54705403 | 0 | False | False | False | False | target_missing_not_executed |
| LT | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=LT | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=LT | 1569 | 0 | 55064314 | 0 | False | False | False | False | target_missing_not_executed |
| M&M | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=M&M | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=M&M | 1569 | 0 | 55603819 | 0 | False | False | False | False | target_missing_not_executed |
| MARUTI | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=MARUTI | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=MARUTI | 1569 | 0 | 55534811 | 0 | False | False | False | False | target_missing_not_executed |
| NESTLEIND | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=NESTLEIND | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=NESTLEIND | 1569 | 0 | 54577884 | 0 | False | False | False | False | target_missing_not_executed |
| NIFTYBEES | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=NIFTYBEES | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=NIFTYBEES | 1568 | 0 | 55113499 | 0 | False | False | False | False | target_missing_not_executed |
| ONGC | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=ONGC | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=ONGC | 1569 | 0 | 54856635 | 0 | False | False | False | False | target_missing_not_executed |
| RELIANCE | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=RELIANCE | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=RELIANCE | 1569 | 0 | 55637533 | 0 | False | False | False | False | target_missing_not_executed |
| SBIN | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=SBIN | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=SBIN | 1569 | 0 | 55549327 | 0 | False | False | False | False | target_missing_not_executed |
| SUNPHARMA | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=SUNPHARMA | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=SUNPHARMA | 1569 | 0 | 54762618 | 0 | False | False | False | False | target_missing_not_executed |
| TCS | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=TCS | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=TCS | 1569 | 0 | 56845524 | 0 | False | False | False | False | target_missing_not_executed |
| TECHM | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=TECHM | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=TECHM | 1569 | 0 | 55179402 | 0 | False | False | False | False | target_missing_not_executed |
| ULTRACEMCO | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=ULTRACEMCO | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=ULTRACEMCO | 1569 | 0 | 54242826 | 0 | False | False | False | False | target_missing_not_executed |
| WIPRO | 2026-07-13 | NSE | copy_symbol_partition | real_data_sample\l2_single_day\symbol=WIPRO | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=WIPRO | 1569 | 0 | 55414740 | 0 | False | False | False | False | target_missing_not_executed |

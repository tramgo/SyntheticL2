# Phase 34 Real Data Multi-Day Readiness

Generated UTC: 2026-07-14T19:03:15.311936+00:00

This milestone inventories local real L2 raw data against the multi-day Class B requirement.
Raw/full-universe coverage is reported separately from Class B event-grade readiness.

## Readiness Summary

| metric | value | description |
| --- | --- | --- |
| phase34_raw_trade_days_available | 1 | Unique raw trade dates detected in local real-data manifest |
| phase34_full_universe_raw_days | 1 | Raw days covering the current required symbol universe |
| phase34_class_b_event_grade_days | 0 | Days currently passing Class B event-grade readiness |
| phase34_required_complete_days_min | 5 | Minimum complete days required by Stage A2 |
| phase34_required_complete_days_target | 10 | Target complete days required by Stage A2 |
| phase34_days_needed_for_min | 5 | Additional Class B days needed for minimum |
| phase34_days_needed_for_target | 10 | Additional Class B days needed for target |
| phase34_stage_a2_open_contract_rows | 192 | Open Stage A2 capture contract rows |
| phase34_phase22_milestones_extension_ready | 0 | Phase 22 real-data milestones currently allowed for extension/paper use |
| phase34_replay_allowed_rows | 0 | Replay rows enabled by current multi-day real-data readiness |

## Day Inventory

| trade_date | exchange | symbols | parquet_files | bytes | phase1_delta_rows | symbols_with_phase1_delta | required_symbols | full_universe_raw_day | class_b_event_grade_day | day_status | blocking_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-13 | NSE | 32 | 50205 | 1764005784 | 620853 | 32 | 32 | True | False | raw_full_universe_day_not_class_b | Stage A2 reports 0 acceptance-met rows and requires multi-day capture diagnostics. |

## Acquisition Plan

| priority | action_id | action | current_blocker | acceptance_effect |
| --- | --- | --- | --- | --- |
| 1 | collect_class_b_days_minimum | Collect or import 5 additional Class B event-grade trading days. | Minimum Class B day count is not met. | Unlocks minimum multi-day real-data requirement only after Stage A2 diagnostics also pass. |
| 2 | close_stage_a2_capture_contracts | Produce connection-boundary, dropped-message, local-sequence, lossless-compaction and timestamp-semantics diagnostics for each collected day/symbol. | 192 Stage A2 contract rows remain open. | Converts raw days into Class B event-grade days when all diagnostics pass. |
| 3 | expand_to_target_days | Collect or import 10 Class B event-grade days for target coverage. | Target Class B day count is not met. | Supports stronger holdout, label stability and acceptance-grade replay prerequisites. |
| 4 | preserve_current_raw_day | Keep the current full-universe raw sample day as a smoke/regression day, but do not treat it as Class B acceptance evidence. | Current day is raw/full-universe but not Stage A2 accepted. | Maintains schema and pipeline regression coverage without overstating acceptance readiness. |

## Symbol-Day Coverage

| trade_date | exchange | symbol | parquet_files | bytes | phase1_delta_rows | book_valid_fraction | stale_gap_gt_15s_count | median_elapsed_ms | p95_elapsed_ms | raw_file_coverage_status | phase1_delta_available | class_b_event_grade_now | blocking_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-13 | NSE | ADANIPORTS | 1569 | 54744007 | 13886 | 0.999928 | 2 | 1000 | 5500 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | AXISBANK | 1569 | 55030126 | 18309 | 0.999945 | 2 | 749 | 4913.65 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | BAJAJ-AUTO | 1569 | 55531219 | 25141 | 0.99996 | 2 | 741 | 4410.05 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | BANKBEES | 1569 | 54858026 | 18916 | 0.999947 | 2 | 1000 | 4833 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | BHARTIARTL | 1569 | 55190740 | 19560 | 0.999949 | 2 | 749 | 4762.4 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | BPCL | 1569 | 54256472 | 10684 | 0.999906 | 2 | 1602 | 6081.7 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | BRITANNIA | 1569 | 54177058 | 8526 | 0.999883 | 2 | 2000 | 7000.8 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | CIPLA | 1569 | 54425687 | 11664 | 0.999914 | 2 | 1194 | 5953.9 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | DRREDDY | 1569 | 54592935 | 12257 | 0.999918 | 2 | 1250 | 5750 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | GOLDBEES | 1568 | 54501651 | 12982 | 0.999846 | 2 | 1000 | 5680 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | HCLTECH | 1569 | 56185830 | 29266 | 0.999966 | 2 | 500 | 4158.8 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | HDFCBANK | 1569 | 56719345 | 35959 | 0.999972 | 2 | 500 | 1250 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | HINDUNILVR | 1569 | 54585232 | 12173 | 0.999918 | 2 | 1001 | 5859.45 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | ICICIBANK | 1569 | 55797042 | 26474 | 0.999962 | 2 | 500 | 4201.4 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | INFY | 1569 | 56702770 | 34511 | 0.999971 | 2 | 500 | 2627.1 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | ITBEES | 1569 | 54430478 | 11481 | 0.999826 | 2 | 1250 | 5993 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | ITC | 1569 | 54356124 | 12379 | 0.999919 | 2 | 1250 | 5750 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | JUNIORBEES | 1568 | 54832707 | 17442 | 0.999885 | 2 | 999 | 5021 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | KOTAKBANK | 1569 | 54705403 | 14091 | 0.999929 | 2 | 1000 | 5475.55 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | LT | 1569 | 55064314 | 19466 | 0.999949 | 2 | 749 | 4750 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | M&M | 1569 | 55603819 | 25699 | 0.999961 | 2 | 501 | 4285.45 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | MARUTI | 1569 | 55534811 | 27645 | 0.999964 | 2 | 502 | 4139.7 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | NESTLEIND | 1569 | 54577884 | 12918 | 0.999923 | 2 | 1000 | 5800.2 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | NIFTYBEES | 1568 | 55113499 | 22414 | 0.999911 | 2 | 749 | 4542 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | ONGC | 1569 | 54856635 | 17305 | 0.999942 | 2 | 750 | 5000 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | RELIANCE | 1569 | 55637533 | 26056 | 0.999962 | 2 | 500 | 4324 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | SBIN | 1569 | 55549327 | 24728 | 0.99996 | 2 | 500 | 4329 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | SUNPHARMA | 1569 | 54762618 | 14610 | 0.999932 | 2 | 982 | 5484 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | TCS | 1569 | 56845524 | 36467 | 0.999973 | 2 | 500 | 1250 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | TECHM | 1569 | 55179402 | 19124 | 0.999948 | 2 | 749 | 4856.7 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | ULTRACEMCO | 1569 | 54242826 | 8386 | 0.999881 | 2 | 2245 | 6772.6 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |
| 2026-07-13 | NSE | WIPRO | 1569 | 55414740 | 20334 | 0.999951 | 2 | 524 | 4730.8 | raw_files_present | True | False | Only one raw sample day is available and Stage A2 capture diagnostics remain open. |

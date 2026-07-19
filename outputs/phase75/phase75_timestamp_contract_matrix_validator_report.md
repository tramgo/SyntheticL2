# Phase75 Timestamp Contract and Synchronous Matrix Validator

Generated UTC: 2026-07-19T19:59:46.154117+00:00

Phase75 implements the first Phase74 remediation gate.
It infers the timestamp unit per symbol partition and validates a global-clock cross-symbol matrix with coverage and staleness diagnostics.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase75_timestamp_contract_pass | 1 | 1 means timestamp unit inferred consistently and not unknown |
| phase75_matrix_bar_rows | 197 | Synchronous timestamp-bar matrix rows |
| phase75_coverage_bucket_rows | 9 | Global timestamp buckets audited |
| phase75_coverage_pass_fraction | 0.555556 | Fraction of buckets passing symbol coverage and freshness |
| phase75_fresh_cell_fraction | 0.893401 | Fraction of symbol/bucket matrix cells within staleness limit |
| phase75_synchronous_matrix_validator_pass | 0 | 1 means Phase74 alignment remediation gate passes |
| phase75_elapsed_seconds | 13.822 | Elapsed seconds |
| phase75_recommend_next_action | fix_synchronous_matrix_coverage_or_staleness | Recommended next action |

## Timestamp Unit Contract Summary

| contract_id | partitions_checked | symbols_checked | mode_inferred_timestamp_unit | mismatched_unit_partitions | median_positive_delta_min | median_positive_delta_max | timestamp_contract_pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P75_timestamp_unit_contract | 32 | 32 | seconds_in_ms_named_column | 0 | 1 | 1 | True |

## Synchronous Matrix Coverage

| trade_date | global_time_bucket_id | symbols_present | fresh_symbols | total_rows | min_first_timestamp_seconds | max_last_timestamp_seconds | max_staleness_seconds | median_staleness_seconds | expected_symbols | coverage_fraction | fresh_fraction | coverage_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01-01 | 356804 | 32 | 32 | 1426414 | 1.78402e+09 | 1.78402e+09 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-01-01 | 356805 | 32 | 32 | 2032340 | 1.78402e+09 | 1.78403e+09 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-01-01 | 356806 | 32 | 32 | 2063860 | 1.78403e+09 | 1.78403e+09 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-01-01 | 356807 | 32 | 32 | 1437114 | 1.78404e+09 | 1.78404e+09 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-01-01 | 356808 | 32 | 32 | 836532 | 1.78404e+09 | 1.78404e+09 | 517 | 17 | 32 | 1 | 1 | True |
| 2026-01-01 | 356809 | 22 | 13 | 67408 | 1.78404e+09 | 1.78405e+09 | 4517 | 17 | 32 | 0.6875 | 0.40625 | False |
| 2026-01-01 | 356810 | 11 | 3 | 18308 | 1.78405e+09 | 1.78405e+09 | 4517 | 2017 | 32 | 0.34375 | 0.09375 | False |
| 2026-01-01 | 356811 | 3 | 0 | 2952 | 1.78406e+09 | 1.78406e+09 | 4517 | 4517 | 32 | 0.09375 | 0 | False |
| 2026-01-01 | 356812 | 1 | 0 | 1984 | 1.78406e+09 | 1.78406e+09 | 1017 | 1017 | 32 | 0.03125 | 0 | False |

## Timestamp Unit Contract Detail

| trade_month | symbol | rows_checked | min_timestamp_value | max_timestamp_value | min_delta_value | median_delta_value | median_positive_delta_value | p01_positive_delta_value | p99_positive_delta_value | positive_delta_count | inferred_timestamp_unit | source_path | unit_contract_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | ADANIPORTS | 250000 | 1.78402e+09 | 1.78404e+09 | -23933 | 1 | 1 | 1 | 1 | 249873 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ADANIPORTS\part-00000.parquet | True |
| 2026-01 | AXISBANK | 250000 | 1.78402e+09 | 1.78404e+09 | -24433 | 1 | 1 | 1 | 1 | 249873 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=AXISBANK\part-00000.parquet | True |
| 2026-01 | BAJAJ-AUTO | 250000 | 1.78402e+09 | 1.78405e+09 | -29433 | 1 | 1 | 1 | 1 | 249875 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BAJAJ-AUTO\part-00000.parquet | True |
| 2026-01 | BANKBEES | 250000 | 1.78402e+09 | 1.78405e+09 | -30933 | 1 | 1 | 1 | 1 | 249875 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BANKBEES\part-00000.parquet | True |
| 2026-01 | BHARTIARTL | 250000 | 1.78402e+09 | 1.78405e+09 | -29933 | 1 | 1 | 1 | 1 | 249875 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BHARTIARTL\part-00000.parquet | True |
| 2026-01 | BPCL | 250000 | 1.78402e+09 | 1.78406e+09 | -34933 | 1 | 1 | 1 | 1 | 249876 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BPCL\part-00000.parquet | True |
| 2026-01 | BRITANNIA | 250000 | 1.78402e+09 | 1.78405e+09 | -26383 | 1 | 1 | 1 | 1 | 249873 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BRITANNIA\part-00000.parquet | True |
| 2026-01 | CIPLA | 250000 | 1.78402e+09 | 1.78405e+09 | -24933 | 1 | 1 | 1 | 1 | 249873 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=CIPLA\part-00000.parquet | True |
| 2026-01 | DRREDDY | 250000 | 1.78402e+09 | 1.78404e+09 | -24433 | 1 | 1 | 1 | 1 | 249873 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=DRREDDY\part-00000.parquet | True |
| 2026-01 | GOLDBEES | 250000 | 1.78402e+09 | 1.78404e+09 | -24483 | 1 | 1 | 1 | 1 | 249873 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=GOLDBEES\part-00000.parquet | True |
| 2026-01 | HCLTECH | 250000 | 1.78402e+09 | 1.78406e+09 | -34983 | 1 | 1 | 1 | 1 | 249876 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=HCLTECH\part-00000.parquet | True |
| 2026-01 | HDFCBANK | 250000 | 1.78402e+09 | 1.78404e+09 | -24433 | 1 | 1 | 1 | 1 | 249873 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | True |
| 2026-01 | HINDUNILVR | 250000 | 1.78402e+09 | 1.78404e+09 | -24433 | 1 | 1 | 1 | 1 | 249873 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=HINDUNILVR\part-00000.parquet | True |
| 2026-01 | ICICIBANK | 250000 | 1.78402e+09 | 1.78405e+09 | -30983 | 1 | 1 | 1 | 1 | 249875 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ICICIBANK\part-00000.parquet | True |
| 2026-01 | INFY | 250000 | 1.78402e+09 | 1.78405e+09 | -30933 | 1 | 1 | 1 | 1 | 249874 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=INFY\part-00000.parquet | True |
| 2026-01 | ITBEES | 250000 | 1.78402e+09 | 1.78406e+09 | -35933 | 1 | 1 | 1 | 1 | 249874 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ITBEES\part-00000.parquet | True |
| 2026-01 | ITC | 250000 | 1.78402e+09 | 1.78405e+09 | -33883 | 1 | 1 | 1 | 1 | 249875 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ITC\part-00000.parquet | True |
| 2026-01 | JUNIORBEES | 250000 | 1.78402e+09 | 1.78405e+09 | -32433 | 1 | 1 | 1 | 1 | 249876 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=JUNIORBEES\part-00000.parquet | True |
| 2026-01 | KOTAKBANK | 250000 | 1.78402e+09 | 1.78406e+09 | -43433 | 1 | 1 | 1 | 1 | 249876 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=KOTAKBANK\part-00000.parquet | True |
| 2026-01 | LT | 250000 | 1.78402e+09 | 1.78407e+09 | -49983 | 1 | 1 | 1 | 1 | 249875 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=LT\part-00000.parquet | True |
| 2026-01 | M&M | 250000 | 1.78402e+09 | 1.78405e+09 | -28883 | 1 | 1 | 1 | 1 | 249874 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=M&M\part-00000.parquet | True |
| 2026-01 | MARUTI | 250000 | 1.78402e+09 | 1.78405e+09 | -25433 | 1 | 1 | 1 | 1 | 249873 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=MARUTI\part-00000.parquet | True |
| 2026-01 | NESTLEIND | 250000 | 1.78402e+09 | 1.78406e+09 | -42933 | 1 | 1 | 1 | 1 | 249874 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=NESTLEIND\part-00000.parquet | True |
| 2026-01 | NIFTYBEES | 250000 | 1.78402e+09 | 1.78405e+09 | -31383 | 1 | 1 | 1 | 1 | 249875 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=NIFTYBEES\part-00000.parquet | True |
| 2026-01 | ONGC | 250000 | 1.78402e+09 | 1.78405e+09 | -29483 | 1 | 1 | 1 | 1 | 249875 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ONGC\part-00000.parquet | True |
| 2026-01 | RELIANCE | 250000 | 1.78402e+09 | 1.78405e+09 | -24933 | 1 | 1 | 1 | 1 | 249873 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=RELIANCE\part-00000.parquet | True |
| 2026-01 | SBIN | 250000 | 1.78402e+09 | 1.78405e+09 | -30433 | 1 | 1 | 1 | 1 | 249875 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=SBIN\part-00000.parquet | True |
| 2026-01 | SUNPHARMA | 250000 | 1.78402e+09 | 1.78405e+09 | -33433 | 1 | 1 | 1 | 1 | 249875 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=SUNPHARMA\part-00000.parquet | True |
| 2026-01 | TCS | 250000 | 1.78402e+09 | 1.78406e+09 | -39433 | 1 | 1 | 1 | 1 | 249875 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=TCS\part-00000.parquet | True |
| 2026-01 | TECHM | 250000 | 1.78402e+09 | 1.78406e+09 | -37433 | 1 | 1 | 1 | 1 | 249874 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=TECHM\part-00000.parquet | True |
| 2026-01 | ULTRACEMCO | 250000 | 1.78402e+09 | 1.78405e+09 | -29383 | 1 | 1 | 1 | 1 | 249874 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ULTRACEMCO\part-00000.parquet | True |
| 2026-01 | WIPRO | 250000 | 1.78402e+09 | 1.78406e+09 | -38933 | 1 | 1 | 1 | 1 | 249875 | seconds_in_ms_named_column | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=WIPRO\part-00000.parquet | True |

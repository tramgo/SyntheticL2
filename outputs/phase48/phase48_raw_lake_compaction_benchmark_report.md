# Phase 48 Raw Lake Compaction Benchmark

Generated UTC: 2026-07-16T15:13:48.285875+00:00

This phase compacts the Phase 45 date/exchange/symbol raw parquet lake into larger monthly parquet files and benchmarks DuckDB SQL queries before and after compaction.
It is storage/query infrastructure evidence, not strategy acceptance evidence.

## Compaction Summary

| metric | value | description |
| --- | --- | --- |
| phase48_raw_partition_files | 8064 | Original raw date/exchange/symbol parquet files |
| phase48_compact_partition_files | 12 | Compacted monthly parquet files |
| phase48_file_count_reduction_ratio | 672 | Original file count divided by compact file count |
| phase48_raw_rows | 3012294 | Rows counted through original raw DuckDB view |
| phase48_compact_rows | 3012294 | Rows counted through compact DuckDB view |
| phase48_row_count_match | 1 | Compacted row count matches raw row count |
| phase48_raw_bytes | 491002806 | Original raw parquet bytes from Phase45 inventory |
| phase48_compact_bytes | 177847919 | Compacted parquet bytes |
| phase48_best_query_speedup_ratio | 571.826 | Best raw-to-compact query speedup ratio |
| phase48_median_query_speedup_ratio | 184.79 | Median raw-to-compact query speedup ratio |
| phase48_compact_root | raw_synthetic_l2_full_year_compact_monthly | Local compacted raw lake root; ignored by Git |
| phase48_duckdb_database | outputs\phase48\raw_lake_compaction.duckdb | Local DuckDB database path; ignored by Git |
| phase48_synthetic_full_year_acceptance_ready | 0 | Compaction benchmark is storage/query infrastructure evidence, not strategy acceptance |

## Speedup Comparison

| query_id | raw_elapsed_ms | compact_elapsed_ms | speedup_ratio |
| --- | --- | --- | --- |
| total_rows | 14424.4 | 25.2252 | 571.826 |
| hdfcbank_rows | 16980.1 | 55.417 | 306.407 |
| distinct_symbols | 23022.3 | 121.33 | 189.749 |
| distinct_feed_profiles | 25045.4 | 135.534 | 184.79 |
| distinct_trade_dates | 21178 | 124.513 | 170.086 |
| l1_l5_complete_rows | 90192.2 | 1565.67 | 57.606 |
| sample_microstructure_agg | 16847.9 | 833.45 | 20.2147 |

## Compact Inventory

| trade_month | file_path | rows | bytes |
| --- | --- | --- | --- |
| 2026-01 | raw_synthetic_l2_full_year_compact_monthly\trade_month=2026-01\part-00000.parquet | 263102 | 15531396 |
| 2026-02 | raw_synthetic_l2_full_year_compact_monthly\trade_month=2026-02\part-00000.parquet | 238970 | 14154209 |
| 2026-03 | raw_synthetic_l2_full_year_compact_monthly\trade_month=2026-03\part-00000.parquet | 262973 | 15265252 |
| 2026-04 | raw_synthetic_l2_full_year_compact_monthly\trade_month=2026-04\part-00000.parquet | 262883 | 15488920 |
| 2026-05 | raw_synthetic_l2_full_year_compact_monthly\trade_month=2026-05\part-00000.parquet | 251038 | 15121943 |
| 2026-06 | raw_synthetic_l2_full_year_compact_monthly\trade_month=2026-06\part-00000.parquet | 262929 | 15612191 |
| 2026-07 | raw_synthetic_l2_full_year_compact_monthly\trade_month=2026-07\part-00000.parquet | 275062 | 16242543 |
| 2026-08 | raw_synthetic_l2_full_year_compact_monthly\trade_month=2026-08\part-00000.parquet | 251003 | 14836075 |
| 2026-09 | raw_synthetic_l2_full_year_compact_monthly\trade_month=2026-09\part-00000.parquet | 262989 | 15914700 |
| 2026-10 | raw_synthetic_l2_full_year_compact_monthly\trade_month=2026-10\part-00000.parquet | 263098 | 15061201 |
| 2026-11 | raw_synthetic_l2_full_year_compact_monthly\trade_month=2026-11\part-00000.parquet | 250973 | 14768780 |
| 2026-12 | raw_synthetic_l2_full_year_compact_monthly\trade_month=2026-12\part-00000.parquet | 167274 | 9850709 |

## Benchmark Timings

| lake_layout | query_id | elapsed_ms | result_rows | description | sql |
| --- | --- | --- | --- | --- | --- |
| raw_symbol_day | total_rows | 14424.4 | 1 | Total rows | select count(*)::bigint as value from raw_l2_ticks |
| raw_symbol_day | distinct_symbols | 23022.3 | 1 | Distinct symbols | select count(distinct symbol)::bigint as value from raw_l2_ticks |
| raw_symbol_day | distinct_trade_dates | 21178 | 1 | Distinct trade dates | select count(distinct trade_date)::bigint as value from raw_l2_ticks |
| raw_symbol_day | distinct_feed_profiles | 25045.4 | 1 | Distinct feed profiles | select count(distinct feed_profile)::bigint as value from raw_l2_ticks |
| raw_symbol_day | l1_l5_complete_rows | 90192.2 | 1 | Rows with complete L1/L5 price/quantity state | select count(*)::bigint as value from raw_l2_ticks where buy_1_price is not null and sell_1_price is not null and buy_5_price is not null and sell_5_price is not null and buy_1_quantity > 0 and sell_1_quantity > 0 and buy_5_quantity > 0 and sell_5_quantity > 0 |
| raw_symbol_day | hdfcbank_rows | 16980.1 | 1 | HDFCBANK row count | select count(*)::bigint as value from raw_l2_ticks where symbol = 'HDFCBANK' |
| raw_symbol_day | sample_microstructure_agg | 16847.9 | 1 | HDFCBANK microstructure aggregate | select count(*)::bigint as rows, avg((sell_1_price + buy_1_price) / 2.0) as avg_mid, avg(sell_1_price - buy_1_price) as avg_spread, avg((buy_1_quantity - sell_1_quantity)::double / nullif((buy_1_quantity + sell_1_quantity), 0)) as avg_l1_imbalance from raw_l2_ticks where symbol = 'HDFCBANK' |
| compact_monthly | total_rows | 25.2252 | 1 | Total rows | select count(*)::bigint as value from compact_l2_ticks |
| compact_monthly | distinct_symbols | 121.33 | 1 | Distinct symbols | select count(distinct symbol)::bigint as value from compact_l2_ticks |
| compact_monthly | distinct_trade_dates | 124.513 | 1 | Distinct trade dates | select count(distinct trade_date)::bigint as value from compact_l2_ticks |
| compact_monthly | distinct_feed_profiles | 135.534 | 1 | Distinct feed profiles | select count(distinct feed_profile)::bigint as value from compact_l2_ticks |
| compact_monthly | l1_l5_complete_rows | 1565.67 | 1 | Rows with complete L1/L5 price/quantity state | select count(*)::bigint as value from compact_l2_ticks where buy_1_price is not null and sell_1_price is not null and buy_5_price is not null and sell_5_price is not null and buy_1_quantity > 0 and sell_1_quantity > 0 and buy_5_quantity > 0 and sell_5_quantity > 0 |
| compact_monthly | hdfcbank_rows | 55.417 | 1 | HDFCBANK row count | select count(*)::bigint as value from compact_l2_ticks where symbol = 'HDFCBANK' |
| compact_monthly | sample_microstructure_agg | 833.45 | 1 | HDFCBANK microstructure aggregate | select count(*)::bigint as rows, avg((sell_1_price + buy_1_price) / 2.0) as avg_mid, avg(sell_1_price - buy_1_price) as avg_spread, avg((buy_1_quantity - sell_1_quantity)::double / nullif((buy_1_quantity + sell_1_quantity), 0)) as avg_l1_imbalance from compact_l2_ticks where symbol = 'HDFCBANK' |

## Benchmark Results

| lake_layout | query_id | metric | value | description |
| --- | --- | --- | --- | --- |
| raw_symbol_day | total_rows | value | 3.01229e+06 | Total rows |
| raw_symbol_day | distinct_symbols | value | 32 | Distinct symbols |
| raw_symbol_day | distinct_trade_dates | value | 252 | Distinct trade dates |
| raw_symbol_day | distinct_feed_profiles | value | 5 | Distinct feed profiles |
| raw_symbol_day | l1_l5_complete_rows | value | 3.01229e+06 | Rows with complete L1/L5 price/quantity state |
| raw_symbol_day | hdfcbank_rows | value | 94110 | HDFCBANK row count |
| raw_symbol_day | sample_microstructure_agg | rows | 94110 | HDFCBANK microstructure aggregate |
| raw_symbol_day | sample_microstructure_agg | avg_mid | 819.075 | HDFCBANK microstructure aggregate |
| raw_symbol_day | sample_microstructure_agg | avg_spread | 0.124972 | HDFCBANK microstructure aggregate |
| raw_symbol_day | sample_microstructure_agg | avg_l1_imbalance | -0.572381 | HDFCBANK microstructure aggregate |
| compact_monthly | total_rows | value | 3.01229e+06 | Total rows |
| compact_monthly | distinct_symbols | value | 32 | Distinct symbols |
| compact_monthly | distinct_trade_dates | value | 252 | Distinct trade dates |
| compact_monthly | distinct_feed_profiles | value | 5 | Distinct feed profiles |
| compact_monthly | l1_l5_complete_rows | value | 3.01229e+06 | Rows with complete L1/L5 price/quantity state |
| compact_monthly | hdfcbank_rows | value | 94110 | HDFCBANK row count |
| compact_monthly | sample_microstructure_agg | rows | 94110 | HDFCBANK microstructure aggregate |
| compact_monthly | sample_microstructure_agg | avg_mid | 819.075 | HDFCBANK microstructure aggregate |
| compact_monthly | sample_microstructure_agg | avg_spread | 0.124972 | HDFCBANK microstructure aggregate |
| compact_monthly | sample_microstructure_agg | avg_l1_imbalance | -0.572381 | HDFCBANK microstructure aggregate |

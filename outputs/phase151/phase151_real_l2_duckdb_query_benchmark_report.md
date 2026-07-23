# Phase151 Real L2 DuckDB Query Benchmark

Generated UTC: 2026-07-23T08:58:39.832630+00:00

Phase151 verifies bounded local DuckDB queries over the real L2 Parquet panel cataloged by Phase150.
It deliberately uses partition-scoped Parquet scans and catalog metadata queries. It does not contact Azure, copy tick rows into DuckDB, or unlock strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase151_catalog_db_exists | 1 | Phase150 DuckDB catalog database exists locally |
| phase151_benchmark_partitions | 4 | Date/symbol partitions selected for bounded benchmark queries |
| phase151_queries_attempted | 9 | DuckDB queries attempted |
| phase151_failed_queries | 0 | DuckDB queries failed |
| phase151_total_query_elapsed_seconds | 7.22348 | Total elapsed seconds across benchmark queries |
| phase151_max_query_elapsed_seconds | 1.42338 | Slowest bounded benchmark query elapsed seconds |
| phase151_min_l1_book_valid_fraction | 0.999928 | Minimum valid L1 book fraction among spread/depth benchmark partitions |
| phase151_min_depth_level_5_present_fraction | 0.999928 | Minimum visible level-5 presence among benchmark partitions |
| phase151_strategy_replay_allowed | 0 | Query benchmark does not unlock strategy replay |
| phase151_next_best_action | use_partition_scoped_duckdb_queries_for_local_real_l2_analysis_after_phase148_downloads | Recommended next milestone |

## Benchmark Partitions

| trade_date | exchange | symbol | parquet_files | bytes | selection_reason |
| --- | --- | --- | --- | --- | --- |
| 2026-07-13 | NSE | ADANIPORTS | 1569 | 54744007 | largest_partition_for_requested_symbol |
| 2026-07-13 | NSE | HDFCBANK | 1569 | 56719345 | largest_partition_for_requested_symbol |
| 2026-07-13 | NSE | RELIANCE | 1569 | 55637533 | largest_partition_for_requested_symbol |
| 2026-07-13 | NSE | TCS | 1569 | 56845524 | largest_partition_overall |

## Query Timing Ledger

| query_id | status | elapsed_seconds | result_rows | sql | error |
| --- | --- | --- | --- | --- | --- |
| count_2026-07-13_ADANIPORTS | completed | 0.656911 | 1 | 
            SELECT
                '2026-07-13' AS trade_date,
                'NSE' AS exchange,
                'ADANIPORTS' AS symbol,
                count(*) AS rows,
                min(collector_received_utc_ms) AS min_received_ms,
                max(collector_received_utc_ms) AS max_received_ms,
                min(last_price) AS min_last_price,
                max(last_price) AS max_last_price
            FROM parquet_scan('real_data_sample/l2_multiday_panel/trade_date=2026-07-13/exchange=NSE/symbol=ADANIPORTS/*.parquet', union_by_name=true)
             |  |
| spread_depth_2026-07-13_ADANIPORTS | completed | 0.666746 | 1 | 
            SELECT
                '2026-07-13' AS trade_date,
                'NSE' AS exchange,
                'ADANIPORTS' AS symbol,
                count(*) AS rows,
                avg(sell_1_price - buy_1_price) AS avg_l1_spread_abs,
                avg(CASE WHEN buy_1_price > 0 AND sell_1_price >= buy_1_price THEN 1 ELSE 0 END) AS l1_book_valid_fraction,
                avg(CASE WHEN buy_5_quantity > 0 OR sell_5_quantity > 0 THEN 1 ELSE 0 END) AS depth_level_5_present_fraction,
                avg(total_buy_quantity) AS avg_total_buy_quantity,
                avg(total_sell_quantity) AS avg_total_sell_quantity
            FROM parquet_scan('real_data_sample/l2_multiday_panel/trade_date=2026-07-13/exchange=NSE/symbol=ADANIPORTS/*.parquet', union_by_name=true)
             |  |
| count_2026-07-13_HDFCBANK | completed | 0.781046 | 1 | 
            SELECT
                '2026-07-13' AS trade_date,
                'NSE' AS exchange,
                'HDFCBANK' AS symbol,
                count(*) AS rows,
                min(collector_received_utc_ms) AS min_received_ms,
                max(collector_received_utc_ms) AS max_received_ms,
                min(last_price) AS min_last_price,
                max(last_price) AS max_last_price
            FROM parquet_scan('real_data_sample/l2_multiday_panel/trade_date=2026-07-13/exchange=NSE/symbol=HDFCBANK/*.parquet', union_by_name=true)
             |  |
| spread_depth_2026-07-13_HDFCBANK | completed | 0.724559 | 1 | 
            SELECT
                '2026-07-13' AS trade_date,
                'NSE' AS exchange,
                'HDFCBANK' AS symbol,
                count(*) AS rows,
                avg(sell_1_price - buy_1_price) AS avg_l1_spread_abs,
                avg(CASE WHEN buy_1_price > 0 AND sell_1_price >= buy_1_price THEN 1 ELSE 0 END) AS l1_book_valid_fraction,
                avg(CASE WHEN buy_5_quantity > 0 OR sell_5_quantity > 0 THEN 1 ELSE 0 END) AS depth_level_5_present_fraction,
                avg(total_buy_quantity) AS avg_total_buy_quantity,
                avg(total_sell_quantity) AS avg_total_sell_quantity
            FROM parquet_scan('real_data_sample/l2_multiday_panel/trade_date=2026-07-13/exchange=NSE/symbol=HDFCBANK/*.parquet', union_by_name=true)
             |  |
| count_2026-07-13_RELIANCE | completed | 0.830884 | 1 | 
            SELECT
                '2026-07-13' AS trade_date,
                'NSE' AS exchange,
                'RELIANCE' AS symbol,
                count(*) AS rows,
                min(collector_received_utc_ms) AS min_received_ms,
                max(collector_received_utc_ms) AS max_received_ms,
                min(last_price) AS min_last_price,
                max(last_price) AS max_last_price
            FROM parquet_scan('real_data_sample/l2_multiday_panel/trade_date=2026-07-13/exchange=NSE/symbol=RELIANCE/*.parquet', union_by_name=true)
             |  |
| spread_depth_2026-07-13_RELIANCE | completed | 1.13784 | 1 | 
            SELECT
                '2026-07-13' AS trade_date,
                'NSE' AS exchange,
                'RELIANCE' AS symbol,
                count(*) AS rows,
                avg(sell_1_price - buy_1_price) AS avg_l1_spread_abs,
                avg(CASE WHEN buy_1_price > 0 AND sell_1_price >= buy_1_price THEN 1 ELSE 0 END) AS l1_book_valid_fraction,
                avg(CASE WHEN buy_5_quantity > 0 OR sell_5_quantity > 0 THEN 1 ELSE 0 END) AS depth_level_5_present_fraction,
                avg(total_buy_quantity) AS avg_total_buy_quantity,
                avg(total_sell_quantity) AS avg_total_sell_quantity
            FROM parquet_scan('real_data_sample/l2_multiday_panel/trade_date=2026-07-13/exchange=NSE/symbol=RELIANCE/*.parquet', union_by_name=true)
             |  |
| count_2026-07-13_TCS | completed | 0.970596 | 1 | 
            SELECT
                '2026-07-13' AS trade_date,
                'NSE' AS exchange,
                'TCS' AS symbol,
                count(*) AS rows,
                min(collector_received_utc_ms) AS min_received_ms,
                max(collector_received_utc_ms) AS max_received_ms,
                min(last_price) AS min_last_price,
                max(last_price) AS max_last_price
            FROM parquet_scan('real_data_sample/l2_multiday_panel/trade_date=2026-07-13/exchange=NSE/symbol=TCS/*.parquet', union_by_name=true)
             |  |
| spread_depth_2026-07-13_TCS | completed | 1.42338 | 1 | 
            SELECT
                '2026-07-13' AS trade_date,
                'NSE' AS exchange,
                'TCS' AS symbol,
                count(*) AS rows,
                avg(sell_1_price - buy_1_price) AS avg_l1_spread_abs,
                avg(CASE WHEN buy_1_price > 0 AND sell_1_price >= buy_1_price THEN 1 ELSE 0 END) AS l1_book_valid_fraction,
                avg(CASE WHEN buy_5_quantity > 0 OR sell_5_quantity > 0 THEN 1 ELSE 0 END) AS depth_level_5_present_fraction,
                avg(total_buy_quantity) AS avg_total_buy_quantity,
                avg(total_sell_quantity) AS avg_total_sell_quantity
            FROM parquet_scan('real_data_sample/l2_multiday_panel/trade_date=2026-07-13/exchange=NSE/symbol=TCS/*.parquet', union_by_name=true)
             |  |
| metadata_catalog_summary | completed | 0.0315163 | 1 | 
        SELECT
            count(*) AS cataloged_files,
            sum(bytes) AS cataloged_bytes,
            count(DISTINCT trade_date) AS cataloged_trade_dates,
            count(DISTINCT symbol) AS cataloged_symbols
        FROM real_l2_parquet_files
         |  |

## Query Results

| trade_date | exchange | symbol | rows | min_received_ms | max_received_ms | min_last_price | max_last_price | avg_l1_spread_abs | l1_book_valid_fraction | depth_level_5_present_fraction | avg_total_buy_quantity | avg_total_sell_quantity | cataloged_files | cataloged_bytes | cataloged_trade_dates | cataloged_symbols |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-13 | NSE | ADANIPORTS | 13886 | 1.78391e+12 | 1.78394e+12 | 1807.2 | 1825.6 |  |  |  |  |  |  |  |  |  |
| 2026-07-13 | NSE | ADANIPORTS | 13886 |  |  |  |  | 0.419602 | 0.999928 | 0.999928 | 148589 | 149035 |  |  |  |  |
| 2026-07-13 | NSE | HDFCBANK | 35959 | 1.78391e+12 | 1.78394e+12 | 811 | 821.9 |  |  |  |  |  |  |  |  |  |
| 2026-07-13 | NSE | HDFCBANK | 35959 |  |  |  |  | 0.119195 | 0.999972 | 0.999972 | 887499 | 1.08642e+06 |  |  |  |  |
| 2026-07-13 | NSE | RELIANCE | 26056 | 1.78391e+12 | 1.78394e+12 | 1295.1 | 1306.3 |  |  |  |  |  |  |  |  |  |
| 2026-07-13 | NSE | RELIANCE | 26056 |  |  |  |  | 0.196757 | 0.999962 | 0.999962 | 613332 | 795219 |  |  |  |  |
| 2026-07-13 | NSE | TCS | 36467 | 1.78391e+12 | 1.78394e+12 | 2069.6 | 2204.9 |  |  |  |  |  |  |  |  |  |
| 2026-07-13 | NSE | TCS | 36467 |  |  |  |  | 0.388431 | 0.999973 | 0.999973 | 357941 | 409110 |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  | 99272 | 3.49028e+09 | 3 | 32 |

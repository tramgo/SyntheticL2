# Phase 47 Raw Lake DuckDB Catalog

Generated UTC: 2026-07-16T14:56:44.517198+00:00

This phase registers the Phase 45 partitioned raw websocket-like L2 parquet lake as a DuckDB query source and runs benchmark/integrity SQL queries.
It is storage/query infrastructure for future raw-source experiments, not strategy acceptance evidence.

## Catalog Summary

| metric | value | description |
| --- | --- | --- |
| phase47_inventory_partitions | 8064 | Raw parquet partitions in Phase45 inventory |
| phase47_inventory_rows | 3012294 | Raw rows declared by Phase45 inventory |
| phase47_duckdb_total_rows | 3012294 | Rows counted through DuckDB raw view |
| phase47_duckdb_distinct_symbols | 32 | Distinct symbols counted through DuckDB raw view |
| phase47_duckdb_distinct_trade_dates | 252 | Distinct trade dates counted through DuckDB raw view |
| phase47_duckdb_distinct_feed_profiles | 5 | Distinct feed profiles counted through DuckDB raw view |
| phase47_duckdb_l1_l5_complete_rows | 3012294 | Rows with complete L1/L5 state through DuckDB raw view |
| phase47_benchmark_query_rows | 7 | DuckDB benchmark queries executed |
| phase47_max_query_elapsed_ms | 19746.1 | Slowest benchmark query elapsed milliseconds |
| phase47_raw_root | raw_synthetic_l2_full_year | Raw parquet lake root queried by DuckDB |
| phase47_duckdb_database | outputs\phase47\raw_lake.duckdb | Local DuckDB database path; ignored by Git |
| phase47_synthetic_full_year_acceptance_ready | 0 | DuckDB catalog is storage/query infrastructure evidence, not strategy acceptance |

## Benchmark Timings

| query_id | elapsed_ms | result_rows | description | sql |
| --- | --- | --- | --- | --- |
| total_rows | 5867.96 | 1 | Total rows query over raw L2 parquet view | select count(*)::bigint as value from raw_l2_ticks |
| distinct_symbols | 8577.26 | 1 | Distinct symbols query over raw L2 parquet view | select count(distinct symbol)::bigint as value from raw_l2_ticks |
| distinct_trade_dates | 8379.32 | 1 | Distinct trade dates query over raw L2 parquet view | select count(distinct trade_date)::bigint as value from raw_l2_ticks |
| distinct_feed_profiles | 8633.37 | 1 | Distinct feed profiles query over raw L2 parquet view | select count(distinct feed_profile)::bigint as value from raw_l2_ticks |
| l1_l5_complete_rows | 19746.1 | 1 | Rows with complete L1 and L5 price/quantity state | select count(*)::bigint as value from raw_l2_ticks where buy_1_price is not null and sell_1_price is not null and buy_5_price is not null and sell_5_price is not null and buy_1_quantity > 0 and sell_1_quantity > 0 and buy_5_quantity > 0 and sell_5_quantity > 0 |
| hdfcbank_rows | 7811.51 | 1 | Ticker-filtered raw-row count for HDFCBANK | select count(*)::bigint as value from raw_l2_ticks where symbol = 'HDFCBANK' |
| sample_microstructure_agg | 7499.78 | 1 | Ticker-filtered microstructure aggregate for HDFCBANK | select count(*)::bigint as rows, avg((sell_1_price + buy_1_price) / 2.0) as avg_mid, avg(sell_1_price - buy_1_price) as avg_spread, avg((buy_1_quantity - sell_1_quantity)::double / nullif((buy_1_quantity + sell_1_quantity), 0)) as avg_l1_imbalance from raw_l2_ticks where symbol = 'HDFCBANK' |

## Benchmark Results

| query_id | metric | value | description |
| --- | --- | --- | --- |
| total_rows | value | 3.01229e+06 | Total rows query over raw L2 parquet view |
| distinct_symbols | value | 32 | Distinct symbols query over raw L2 parquet view |
| distinct_trade_dates | value | 252 | Distinct trade dates query over raw L2 parquet view |
| distinct_feed_profiles | value | 5 | Distinct feed profiles query over raw L2 parquet view |
| l1_l5_complete_rows | value | 3.01229e+06 | Rows with complete L1 and L5 price/quantity state |
| hdfcbank_rows | value | 94110 | Ticker-filtered raw-row count for HDFCBANK |
| sample_microstructure_agg | rows | 94110 | Ticker-filtered microstructure aggregate for HDFCBANK |
| sample_microstructure_agg | avg_mid | 819.075 | Ticker-filtered microstructure aggregate for HDFCBANK |
| sample_microstructure_agg | avg_spread | 0.124972 | Ticker-filtered microstructure aggregate for HDFCBANK |
| sample_microstructure_agg | avg_l1_imbalance | -0.572381 | Ticker-filtered microstructure aggregate for HDFCBANK |

## Schema

| column_name | column_type | null | key | default | extra |
| --- | --- | --- | --- | --- | --- |
| collector_run_id | VARCHAR | YES |  |  |  |
| session_id | VARCHAR | YES |  |  |  |
| callback_batch_id | BIGINT | YES |  |  |  |
| local_sequence_id | BIGINT | YES |  |  |  |
| callback_received_utc_ms | BIGINT | YES |  |  |  |
| callback_received_monotonic_ns | BIGINT | YES |  |  |  |
| exchange_timestamp_ms | BIGINT | YES |  |  |  |
| last_trade_time_ms | BIGINT | YES |  |  |  |
| trade_date | VARCHAR | YES |  |  |  |
| exchange | VARCHAR | YES |  |  |  |
| symbol | VARCHAR | YES |  |  |  |
| instrument_token | BIGINT | YES |  |  |  |
| feed_profile | VARCHAR | YES |  |  |  |
| annual_event_id | BIGINT | YES |  |  |  |
| receive_sequence | BIGINT | YES |  |  |  |
| source_sequence | BIGINT | YES |  |  |  |
| regime_code | VARCHAR | YES |  |  |  |
| last_price | DOUBLE | YES |  |  |  |
| last_traded_quantity | BIGINT | YES |  |  |  |
| volume_traded | BIGINT | YES |  |  |  |
| average_traded_price | DOUBLE | YES |  |  |  |
| total_buy_quantity | BIGINT | YES |  |  |  |
| total_sell_quantity | BIGINT | YES |  |  |  |
| oi | BIGINT | YES |  |  |  |
| oi_day_high | BIGINT | YES |  |  |  |
| oi_day_low | BIGINT | YES |  |  |  |
| is_market_shock_day | BOOLEAN | YES |  |  |  |
| is_symbol_shock | BOOLEAN | YES |  |  |  |
| is_duplicate | BOOLEAN | YES |  |  |  |
| is_disconnect_gap | BOOLEAN | YES |  |  |  |
| is_out_of_order_injected | BOOLEAN | YES |  |  |  |
| buy_1_price | DOUBLE | YES |  |  |  |
| buy_1_quantity | BIGINT | YES |  |  |  |
| buy_1_orders | BIGINT | YES |  |  |  |
| sell_1_price | DOUBLE | YES |  |  |  |
| sell_1_quantity | BIGINT | YES |  |  |  |
| sell_1_orders | BIGINT | YES |  |  |  |
| buy_2_price | DOUBLE | YES |  |  |  |
| buy_2_quantity | BIGINT | YES |  |  |  |
| buy_2_orders | BIGINT | YES |  |  |  |
| sell_2_price | DOUBLE | YES |  |  |  |
| sell_2_quantity | BIGINT | YES |  |  |  |
| sell_2_orders | BIGINT | YES |  |  |  |
| buy_3_price | DOUBLE | YES |  |  |  |
| buy_3_quantity | BIGINT | YES |  |  |  |
| buy_3_orders | BIGINT | YES |  |  |  |
| sell_3_price | DOUBLE | YES |  |  |  |
| sell_3_quantity | BIGINT | YES |  |  |  |
| sell_3_orders | BIGINT | YES |  |  |  |
| buy_4_price | DOUBLE | YES |  |  |  |
| buy_4_quantity | BIGINT | YES |  |  |  |
| buy_4_orders | BIGINT | YES |  |  |  |
| sell_4_price | DOUBLE | YES |  |  |  |
| sell_4_quantity | BIGINT | YES |  |  |  |
| sell_4_orders | BIGINT | YES |  |  |  |
| buy_5_price | DOUBLE | YES |  |  |  |
| buy_5_quantity | BIGINT | YES |  |  |  |
| buy_5_orders | BIGINT | YES |  |  |  |
| sell_5_price | DOUBLE | YES |  |  |  |
| sell_5_quantity | BIGINT | YES |  |  |  |
| sell_5_orders | BIGINT | YES |  |  |  |

# Phase150 Real L2 DuckDB Catalog

Generated UTC: 2026-07-23T08:54:25.183831+00:00

Phase150 builds a metadata-first DuckDB catalog for the local real Zerodha top-five market-by-price Parquet panel.
It does not copy all tick rows into DuckDB. Bulk storage remains partitioned Parquet; DuckDB stores metadata, summaries, schema, templates, and a sample-file view.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase150_duckdb_available | 1 | DuckDB import and connection succeeded |
| phase150_catalog_db_created | 1 | Persistent DuckDB metadata catalog exists |
| phase150_parquet_files_cataloged | 99272 | Local real L2 Parquet files cataloged without row-copy ingest |
| phase150_cataloged_bytes | 3490276400 | Cataloged local Parquet bytes |
| phase150_trade_dates | 3 | Distinct trade dates cataloged |
| phase150_date_symbol_partitions | 96 | Date/exchange/symbol partitions cataloged |
| phase150_schema_columns | 54 | Columns in sampled Parquet schema |
| phase150_depth_columns_present | 30 | buy/sell level 1-5 price/quantity/orders columns present in sampled schema |
| phase150_sample_query_rows | 5 | Rows returned by DuckDB sample-file smoke query |
| phase150_strategy_replay_allowed | 0 | Cataloging local Parquet does not unlock strategy replay |
| phase150_next_best_action | use_duckdb_catalog_for_local_real_l2_queries_after_phase148_downloads | Recommended next milestone |

## Date Summary

| trade_date | exchange | symbols | parquet_files | bytes |
| --- | --- | --- | --- | --- |
| 2026-07-08 | NSE | 32 | 20507 | 719892449 |
| 2026-07-09 | NSE | 32 | 28560 | 1006378167 |
| 2026-07-13 | NSE | 32 | 50205 | 1764005784 |

## Schema Columns

| column_ordinal | column_name | arrow_type | nullable |
| --- | --- | --- | --- |
| 0 | collector_received_utc | large_string | True |
| 1 | collector_received_utc_ms | int64 | True |
| 2 | collector_received_monotonic_ns | int64 | True |
| 3 | exchange_timestamp | large_string | True |
| 4 | last_trade_time | large_string | True |
| 5 | trade_date | large_string | True |
| 6 | exchange | large_string | True |
| 7 | tradingsymbol | large_string | True |
| 8 | requested_symbol | large_string | True |
| 9 | instrument_token | int64 | True |
| 10 | last_price | double | True |
| 11 | last_traded_quantity | int64 | True |
| 12 | volume_traded | int64 | True |
| 13 | average_traded_price | double | True |
| 14 | total_buy_quantity | int64 | True |
| 15 | total_sell_quantity | int64 | True |
| 16 | oi | int64 | True |
| 17 | oi_day_high | int64 | True |
| 18 | oi_day_low | int64 | True |
| 19 | ohlc_open | double | True |
| 20 | ohlc_high | double | True |
| 21 | ohlc_low | double | True |
| 22 | ohlc_close | double | True |
| 23 | change | double | True |
| 24 | buy_1_price | double | True |
| 25 | buy_1_quantity | int64 | True |
| 26 | buy_1_orders | int64 | True |
| 27 | buy_2_price | double | True |
| 28 | buy_2_quantity | int64 | True |
| 29 | buy_2_orders | int64 | True |
| 30 | buy_3_price | double | True |
| 31 | buy_3_quantity | int64 | True |
| 32 | buy_3_orders | int64 | True |
| 33 | buy_4_price | double | True |
| 34 | buy_4_quantity | int64 | True |
| 35 | buy_4_orders | int64 | True |
| 36 | buy_5_price | double | True |
| 37 | buy_5_quantity | int64 | True |
| 38 | buy_5_orders | int64 | True |
| 39 | sell_1_price | double | True |
| 40 | sell_1_quantity | int64 | True |
| 41 | sell_1_orders | int64 | True |
| 42 | sell_2_price | double | True |
| 43 | sell_2_quantity | int64 | True |
| 44 | sell_2_orders | int64 | True |
| 45 | sell_3_price | double | True |
| 46 | sell_3_quantity | int64 | True |
| 47 | sell_3_orders | int64 | True |
| 48 | sell_4_price | double | True |
| 49 | sell_4_quantity | int64 | True |
| 50 | sell_4_orders | int64 | True |
| 51 | sell_5_price | double | True |
| 52 | sell_5_quantity | int64 | True |
| 53 | sell_5_orders | int64 | True |

## DuckDB Smoke Query

| rows | min_received_ms | max_received_ms | sample_file | catalog_tables |
| --- | --- | --- | --- | --- |
| 5 | 1783496075001 | 1783496081751 | real_data_sample/l2_multiday_panel/trade_date=2026-07-08/exchange=NSE/symbol=ADANIPORTS/part-073443_831343-000001.parquet | columns_df\|date_summary_df\|date_symbol_summary_df\|files_df\|query_templates_df\|real_l2_date_summary\|real_l2_date_symbol_summary\|real_l2_parquet_files\|real_l2_query_templates\|real_l2_sample_ticks\|real_l2_schema_columns |

## Query Templates

| template_id | description | sql_template |
| --- | --- | --- |
| read_one_symbol_day | Read one symbol/day directly from local partitioned Parquet. | SELECT * FROM parquet_scan('<root>/trade_date=<date>/exchange=NSE/symbol=<symbol>/*.parquet', union_by_name=true, filename=true) ORDER BY collector_received_utc_ms LIMIT 100; |
| count_one_symbol_day | Count rows for one symbol/day by scanning only that partition. | SELECT count(*) AS rows FROM parquet_scan('<root>/trade_date=<date>/exchange=NSE/symbol=<symbol>/*.parquet', union_by_name=true); |
| best_bid_ask_sample | Sample L1 book columns from one symbol/day without scanning the full lake. | SELECT trade_date, exchange, tradingsymbol, collector_received_utc_ms, last_price, buy_1_price, buy_1_quantity, sell_1_price, sell_1_quantity FROM parquet_scan('<root>/trade_date=<date>/exchange=NSE/symbol=<symbol>/*.parquet', union_by_name=true) ORDER BY collector_received_utc_ms LIMIT 100; |
| all_panel_glob | Full local panel glob for deliberate analytical scans; avoid for quick metadata checks. | SELECT * FROM parquet_scan('real_data_sample/l2_multiday_panel/**/*.parquet', hive_partitioning=true, union_by_name=true, filename=true); |

# Phase113 Real L2 Drop-zone Importer

Generated UTC: 2026-07-19T22:53:46.828635+00:00

Phase113 creates a dry-run-safe import plan for normalizing real Zerodha WebSocket L2 parquet into the Phase111/112 multiday drop-zone layout.
It does not enable strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase113_source_symbol_partitions | 32 | Source symbol partitions inspected |
| phase113_ready_symbol_partitions | 32 | Source symbol partitions ready for import |
| phase113_ready_trade_dates | 1 | Distinct ready trade dates inferred |
| phase113_ready_symbols | 32 | Distinct ready symbols inferred |
| phase113_ready_expected_symbol_fraction | 1 | Expected universe fraction ready in source |
| phase113_import_plan_rows | 32 | Import plan rows emitted |
| phase113_execute_mode | 0 | 1 means files were copied into the drop-zone |
| phase113_copied_files | 0 | Parquet files copied when execute mode is enabled |
| phase113_strategy_replay_allowed | 0 | Strategy replay remains closed |

## Source Partition Inventory

| source_root | source_symbol_dir | symbol | source_layout | inferred_trade_date | inferred_exchange | parquet_files | first_file | last_file | ready_for_import | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ADANIPORTS | ADANIPORTS | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034501_461115-000006.parquet | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-100140_980924-050206.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=AXISBANK | AXISBANK | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=AXISBANK\part-034501_605662-000007.parquet | real_data_sample\l2_single_day\symbol=AXISBANK\part-100122_227622-050181.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=BAJAJ-AUTO | BAJAJ-AUTO | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=BAJAJ-AUTO\part-034501_757997-000008.parquet | real_data_sample\l2_single_day\symbol=BAJAJ-AUTO\part-100122_365351-050182.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=BANKBEES | BANKBEES | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=BANKBEES\part-034515_611482-000036.parquet | real_data_sample\l2_single_day\symbol=BANKBEES\part-100141_131697-050207.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=BHARTIARTL | BHARTIARTL | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=BHARTIARTL\part-034501_889174-000009.parquet | real_data_sample\l2_single_day\symbol=BHARTIARTL\part-100141_292382-050208.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=BPCL | BPCL | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=BPCL\part-034502_038569-000010.parquet | real_data_sample\l2_single_day\symbol=BPCL\part-100122_503645-050183.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=BRITANNIA | BRITANNIA | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=BRITANNIA\part-034502_179937-000011.parquet | real_data_sample\l2_single_day\symbol=BRITANNIA\part-100122_650311-050184.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=CIPLA | CIPLA | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=CIPLA\part-034502_320381-000012.parquet | real_data_sample\l2_single_day\symbol=CIPLA\part-100141_444873-050209.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=DRREDDY | DRREDDY | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=DRREDDY\part-034502_452126-000013.parquet | real_data_sample\l2_single_day\symbol=DRREDDY\part-100122_785508-050185.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=GOLDBEES | GOLDBEES | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1568 | real_data_sample\l2_single_day\symbol=GOLDBEES\part-034516_327126-000042.parquet | real_data_sample\l2_single_day\symbol=GOLDBEES\part-100122_930799-050186.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=HCLTECH | HCLTECH | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=HCLTECH\part-034502_601925-000014.parquet | real_data_sample\l2_single_day\symbol=HCLTECH\part-100123_073528-050187.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=HDFCBANK | HDFCBANK | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=HDFCBANK\part-034502_729724-000015.parquet | real_data_sample\l2_single_day\symbol=HDFCBANK\part-100123_219242-050188.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=HINDUNILVR | HINDUNILVR | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=HINDUNILVR\part-034502_860555-000016.parquet | real_data_sample\l2_single_day\symbol=HINDUNILVR\part-100123_361642-050189.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ICICIBANK | ICICIBANK | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=ICICIBANK\part-034502_988562-000017.parquet | real_data_sample\l2_single_day\symbol=ICICIBANK\part-100123_501495-050190.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=INFY | INFY | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=INFY\part-034503_117898-000018.parquet | real_data_sample\l2_single_day\symbol=INFY\part-100123_638331-050191.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ITBEES | ITBEES | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=ITBEES\part-034517_017153-000048.parquet | real_data_sample\l2_single_day\symbol=ITBEES\part-100123_781513-050192.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ITC | ITC | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=ITC\part-034503_268298-000019.parquet | real_data_sample\l2_single_day\symbol=ITC\part-100123_923122-050193.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=JUNIORBEES | JUNIORBEES | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1568 | real_data_sample\l2_single_day\symbol=JUNIORBEES\part-034517_282487-000050.parquet | real_data_sample\l2_single_day\symbol=JUNIORBEES\part-100124_062827-050194.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=KOTAKBANK | KOTAKBANK | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=KOTAKBANK\part-034503_409193-000020.parquet | real_data_sample\l2_single_day\symbol=KOTAKBANK\part-100124_217580-050195.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=LT | LT | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=LT\part-034503_545025-000021.parquet | real_data_sample\l2_single_day\symbol=LT\part-100124_362972-050196.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=M&M | M&M | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=M&M\part-034503_695120-000022.parquet | real_data_sample\l2_single_day\symbol=M&M\part-100141_602057-050210.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=MARUTI | MARUTI | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=MARUTI\part-034503_823825-000023.parquet | real_data_sample\l2_single_day\symbol=MARUTI\part-100124_507989-050197.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=NESTLEIND | NESTLEIND | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=NESTLEIND\part-034503_950077-000024.parquet | real_data_sample\l2_single_day\symbol=NESTLEIND\part-100124_654903-050198.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=NIFTYBEES | NIFTYBEES | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1568 | real_data_sample\l2_single_day\symbol=NIFTYBEES\part-034518_008261-000056.parquet | real_data_sample\l2_single_day\symbol=NIFTYBEES\part-100124_794529-050199.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ONGC | ONGC | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=ONGC\part-034504_083380-000025.parquet | real_data_sample\l2_single_day\symbol=ONGC\part-100124_949284-050200.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=RELIANCE | RELIANCE | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=RELIANCE\part-034504_243903-000026.parquet | real_data_sample\l2_single_day\symbol=RELIANCE\part-100108_778994-050179.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=SBIN | SBIN | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=SBIN\part-034504_383495-000027.parquet | real_data_sample\l2_single_day\symbol=SBIN\part-100125_096592-050201.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=SUNPHARMA | SUNPHARMA | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=SUNPHARMA\part-034504_524718-000028.parquet | real_data_sample\l2_single_day\symbol=SUNPHARMA\part-100125_256362-050202.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=TCS | TCS | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=TCS\part-034504_658177-000029.parquet | real_data_sample\l2_single_day\symbol=TCS\part-100108_924738-050180.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=TECHM | TECHM | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=TECHM\part-034504_798344-000030.parquet | real_data_sample\l2_single_day\symbol=TECHM\part-100125_418803-050203.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=ULTRACEMCO | ULTRACEMCO | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=ULTRACEMCO\part-034504_922769-000031.parquet | real_data_sample\l2_single_day\symbol=ULTRACEMCO\part-100125_566742-050204.parquet | True |  |
| real_data_sample\l2_single_day | real_data_sample\l2_single_day\symbol=WIPRO | WIPRO | symbol_partition_with_file_trade_date | 2026-07-13 | NSE | 1569 | real_data_sample\l2_single_day\symbol=WIPRO\part-034505_052199-000032.parquet | real_data_sample\l2_single_day\symbol=WIPRO\part-100125_705145-050205.parquet | True |  |

## Drop-zone Import Plan

| symbol | trade_date | exchange | source_symbol_dir | target_symbol_dir | parquet_files | planned_action | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=ADANIPORTS | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=ADANIPORTS | 1569 | copy_symbol_partition |  |
| AXISBANK | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=AXISBANK | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=AXISBANK | 1569 | copy_symbol_partition |  |
| BAJAJ-AUTO | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=BAJAJ-AUTO | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=BAJAJ-AUTO | 1569 | copy_symbol_partition |  |
| BANKBEES | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=BANKBEES | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=BANKBEES | 1569 | copy_symbol_partition |  |
| BHARTIARTL | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=BHARTIARTL | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=BHARTIARTL | 1569 | copy_symbol_partition |  |
| BPCL | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=BPCL | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=BPCL | 1569 | copy_symbol_partition |  |
| BRITANNIA | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=BRITANNIA | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=BRITANNIA | 1569 | copy_symbol_partition |  |
| CIPLA | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=CIPLA | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=CIPLA | 1569 | copy_symbol_partition |  |
| DRREDDY | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=DRREDDY | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=DRREDDY | 1569 | copy_symbol_partition |  |
| GOLDBEES | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=GOLDBEES | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=GOLDBEES | 1568 | copy_symbol_partition |  |
| HCLTECH | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=HCLTECH | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=HCLTECH | 1569 | copy_symbol_partition |  |
| HDFCBANK | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=HDFCBANK | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=HDFCBANK | 1569 | copy_symbol_partition |  |
| HINDUNILVR | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=HINDUNILVR | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=HINDUNILVR | 1569 | copy_symbol_partition |  |
| ICICIBANK | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=ICICIBANK | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=ICICIBANK | 1569 | copy_symbol_partition |  |
| INFY | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=INFY | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=INFY | 1569 | copy_symbol_partition |  |
| ITBEES | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=ITBEES | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=ITBEES | 1569 | copy_symbol_partition |  |
| ITC | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=ITC | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=ITC | 1569 | copy_symbol_partition |  |
| JUNIORBEES | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=JUNIORBEES | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=JUNIORBEES | 1568 | copy_symbol_partition |  |
| KOTAKBANK | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=KOTAKBANK | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=KOTAKBANK | 1569 | copy_symbol_partition |  |
| LT | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=LT | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=LT | 1569 | copy_symbol_partition |  |
| M&M | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=M&M | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=M&M | 1569 | copy_symbol_partition |  |
| MARUTI | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=MARUTI | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=MARUTI | 1569 | copy_symbol_partition |  |
| NESTLEIND | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=NESTLEIND | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=NESTLEIND | 1569 | copy_symbol_partition |  |
| NIFTYBEES | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=NIFTYBEES | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=NIFTYBEES | 1568 | copy_symbol_partition |  |
| ONGC | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=ONGC | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=ONGC | 1569 | copy_symbol_partition |  |
| RELIANCE | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=RELIANCE | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=RELIANCE | 1569 | copy_symbol_partition |  |
| SBIN | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=SBIN | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=SBIN | 1569 | copy_symbol_partition |  |
| SUNPHARMA | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=SUNPHARMA | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=SUNPHARMA | 1569 | copy_symbol_partition |  |
| TCS | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=TCS | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=TCS | 1569 | copy_symbol_partition |  |
| TECHM | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=TECHM | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=TECHM | 1569 | copy_symbol_partition |  |
| ULTRACEMCO | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=ULTRACEMCO | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=ULTRACEMCO | 1569 | copy_symbol_partition |  |
| WIPRO | 2026-07-13 | NSE | real_data_sample\l2_single_day\symbol=WIPRO | real_data_sample\l2_multiday_panel\trade_date=2026-07-13\exchange=NSE\symbol=WIPRO | 1569 | copy_symbol_partition |  |

## Import Execution

_No rows._

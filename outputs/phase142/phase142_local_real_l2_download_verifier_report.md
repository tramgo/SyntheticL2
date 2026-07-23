# Phase142 Local Real L2 Download Verifier

Generated UTC: 2026-07-23T08:04:58.336425+00:00

Phase142 verifies local AzCopy/downloaded real Zerodha WebSocket top-five market-by-price partitions before or after Phase115 import.
It checks date/symbol coverage, parquet counts/bytes, sampled required schema, and sampled L1 book sanity.
It also reports whether downloaded scratch paths use canonical `trade_date/exchange/symbol` layout or contain duplicate nested `trade_date` path parts from older AzCopy destination usage.
Phase142 readiness is intentionally an import/download readiness flag: L1 book sample status is diagnostic here; Phase96 remains the authoritative real-anchor market-quality gate.
It does not contact Azure and does not unlock strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase142_roots_checked | 2 | Distinct local roots inspected |
| phase142_symbol_partition_rows | 160 | Symbol partition rows discovered |
| phase142_canonical_symbol_partition_rows | 96 | Symbol partitions with canonical trade_date/exchange/symbol layout |
| phase142_nested_trade_date_symbol_partition_rows | 64 | Symbol partitions with duplicate nested trade_date path parts |
| phase142_sample_files_checked | 320 | First/last parquet samples read for schema and L1 book checks |
| phase142_date_rows | 5 | Root/date readiness rows emitted |
| phase142_ready_date_rows | 5 | Root/date rows ready for Phase115 import |
| phase142_max_ready_dates_in_one_root | 3 | Maximum ready dates in any one checked root |
| phase142_total_parquet_files | 148339 | Total parquet files across checked roots |
| phase142_total_bytes | 5216547016 | Total bytes across checked roots |
| phase142_strategy_replay_allowed | 0 | Local download verification does not unlock strategy replay |

## Date Readiness

| root | trade_date | exchange | symbol_directories | nested_trade_date_symbol_dirs | canonical_symbol_dirs | expected_symbols_with_files | expected_symbol_fraction | missing_expected_symbols | parquet_files | bytes | schema_sample_pass | l1_book_sample_pass | sample_failed_files | ready_for_phase115_import |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_data_sample\l2_multiday_panel | 2026-07-08 | NSE | 32 | 0 | 32 | 32 | 1 |  | 20507 | 719892449 | True | False | 0 | True |
| real_data_sample\l2_multiday_panel | 2026-07-09 | NSE | 32 | 0 | 32 | 32 | 1 |  | 28560 | 1006378167 | True | False | 0 | True |
| real_data_sample\l2_multiday_panel | 2026-07-13 | NSE | 32 | 0 | 32 | 32 | 1 |  | 50205 | 1764005784 | True | False | 0 | True |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | 32 | 32 | 0 | 32 | 1 |  | 20507 | 719892449 | True | False | 0 | True |
| scratch_azcopy_selected\raw_l2 | 2026-07-09 | NSE | 32 | 32 | 0 | 32 | 1 |  | 28560 | 1006378167 | True | False | 0 | True |

## Sample Schema Checks

| root | trade_date | exchange | symbol | file | rows | column_count | missing_required_columns | required_schema_pass | l1_book_sample_pass | observed_trade_dates | observed_symbols | sample_status | sample_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | ADANIPORTS | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\part-073443_831343-000001.parquet | 5 | 54 |  | True | True | 2026-07-08 | ADANIPORTS | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | ADANIPORTS | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\part-100140_507866-020481.parquet | 1 | 54 |  | True | False | 2026-07-08 | ADANIPORTS | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | AXISBANK | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\part-073443_970901-000002.parquet | 18 | 54 |  | True | True | 2026-07-08 | AXISBANK | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | AXISBANK | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\part-100140_620396-020482.parquet | 1 | 54 |  | True | False | 2026-07-08 | AXISBANK | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | BAJAJ-AUTO | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\part-073444_080201-000003.parquet | 12 | 54 |  | True | True | 2026-07-08 | BAJAJ-AUTO | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | BAJAJ-AUTO | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\part-100140_731059-020483.parquet | 1 | 54 |  | True | False | 2026-07-08 | BAJAJ-AUTO | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | BANKBEES | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\part-073444_224685-000004.parquet | 10 | 54 |  | True | True | 2026-07-08 | BANKBEES | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | BANKBEES | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\part-100140_848136-020484.parquet | 1 | 54 |  | True | False | 2026-07-08 | BANKBEES | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | BHARTIARTL | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\part-073444_337478-000005.parquet | 12 | 54 |  | True | True | 2026-07-08 | BHARTIARTL | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | BHARTIARTL | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\part-100109_725200-020453.parquet | 4 | 54 |  | True | False | 2026-07-08 | BHARTIARTL | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | BPCL | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\part-073444_450400-000006.parquet | 6 | 54 |  | True | True | 2026-07-08 | BPCL | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | BPCL | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\part-100109_851351-020454.parquet | 3 | 54 |  | True | False | 2026-07-08 | BPCL | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | BRITANNIA | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\part-073444_559438-000007.parquet | 3 | 54 |  | True | True | 2026-07-08 | BRITANNIA | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | BRITANNIA | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\part-100140_948824-020485.parquet | 1 | 54 |  | True | False | 2026-07-08 | BRITANNIA | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | CIPLA | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\part-073444_685953-000008.parquet | 8 | 54 |  | True | True | 2026-07-08 | CIPLA | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | CIPLA | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\part-100110_070390-020456.parquet | 3 | 54 |  | True | False | 2026-07-08 | CIPLA | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | DRREDDY | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\part-073444_858308-000009.parquet | 6 | 54 |  | True | True | 2026-07-08 | DRREDDY | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | DRREDDY | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\part-100141_075547-020486.parquet | 1 | 54 |  | True | False | 2026-07-08 | DRREDDY | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | GOLDBEES | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\part-073444_976748-000010.parquet | 16 | 54 |  | True | True | 2026-07-08 | GOLDBEES | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | GOLDBEES | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\part-100141_199842-020487.parquet | 1 | 54 |  | True | False | 2026-07-08 | GOLDBEES | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | HCLTECH | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\part-073445_125270-000011.parquet | 8 | 54 |  | True | True | 2026-07-08 | HCLTECH | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | HCLTECH | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\part-100141_316106-020488.parquet | 1 | 54 |  | True | False | 2026-07-08 | HCLTECH | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | HDFCBANK | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\part-073445_239174-000012.parquet | 16 | 54 |  | True | True | 2026-07-08 | HDFCBANK | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | HDFCBANK | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\part-100141_430919-020489.parquet | 1 | 54 |  | True | False | 2026-07-08 | HDFCBANK | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | HINDUNILVR | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\part-073445_351918-000013.parquet | 4 | 54 |  | True | True | 2026-07-08 | HINDUNILVR | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | HINDUNILVR | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\part-100141_557253-020490.parquet | 1 | 54 |  | True | False | 2026-07-08 | HINDUNILVR | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | ICICIBANK | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\part-073445_486437-000014.parquet | 17 | 54 |  | True | True | 2026-07-08 | ICICIBANK | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | ICICIBANK | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\part-100141_666872-020491.parquet | 1 | 54 |  | True | False | 2026-07-08 | ICICIBANK | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | INFY | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=INFY\part-073445_602798-000015.parquet | 19 | 54 |  | True | True | 2026-07-08 | INFY | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | INFY | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=INFY\part-100141_770666-020492.parquet | 1 | 54 |  | True | False | 2026-07-08 | INFY | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | ITBEES | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\part-073445_718369-000016.parquet | 6 | 54 |  | True | True | 2026-07-08 | ITBEES | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | ITBEES | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\part-100141_879358-020493.parquet | 1 | 54 |  | True | False | 2026-07-08 | ITBEES | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | ITC | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=ITC\part-073445_866169-000017.parquet | 16 | 54 |  | True | True | 2026-07-08 | ITC | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | ITC | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=ITC\part-100142_006553-020494.parquet | 1 | 54 |  | True | False | 2026-07-08 | ITC | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | JUNIORBEES | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\part-073445_997997-000018.parquet | 12 | 54 |  | True | True | 2026-07-08 | JUNIORBEES | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | JUNIORBEES | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\part-100142_116738-020495.parquet | 1 | 54 |  | True | False | 2026-07-08 | JUNIORBEES | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | KOTAKBANK | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\part-073446_107086-000019.parquet | 19 | 54 |  | True | True | 2026-07-08 | KOTAKBANK | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | KOTAKBANK | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\part-100142_239451-020496.parquet | 1 | 54 |  | True | False | 2026-07-08 | KOTAKBANK | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | LT | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=LT\part-073446_226721-000020.parquet | 17 | 54 |  | True | True | 2026-07-08 | LT | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | LT | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=LT\part-100142_357559-020497.parquet | 1 | 54 |  | True | False | 2026-07-08 | LT | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | M&M | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=M&M\part-073446_344136-000021.parquet | 18 | 54 |  | True | True | 2026-07-08 | M&M | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | M&M | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=M&M\part-100142_459029-020498.parquet | 1 | 54 |  | True | False | 2026-07-08 | M&M | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | MARUTI | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\part-073446_469930-000022.parquet | 6 | 54 |  | True | True | 2026-07-08 | MARUTI | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | MARUTI | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\part-100142_602509-020499.parquet | 1 | 54 |  | True | False | 2026-07-08 | MARUTI | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | NESTLEIND | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\part-073446_613957-000023.parquet | 5 | 54 |  | True | True | 2026-07-08 | NESTLEIND | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | NESTLEIND | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\part-100142_710474-020500.parquet | 1 | 54 |  | True | False | 2026-07-08 | NESTLEIND | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | NIFTYBEES | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\part-073446_725850-000024.parquet | 12 | 54 |  | True | True | 2026-07-08 | NIFTYBEES | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | NIFTYBEES | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\part-100142_818192-020501.parquet | 1 | 54 |  | True | False | 2026-07-08 | NIFTYBEES | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | ONGC | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\part-073446_843264-000025.parquet | 6 | 54 |  | True | True | 2026-07-08 | ONGC | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | ONGC | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\part-100142_959084-020502.parquet | 1 | 54 |  | True | False | 2026-07-08 | ONGC | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | RELIANCE | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\part-073446_959823-000026.parquet | 18 | 54 |  | True | True | 2026-07-08 | RELIANCE | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | RELIANCE | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\part-100112_301811-020474.parquet | 3 | 54 |  | True | False | 2026-07-08 | RELIANCE | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | SBIN | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\part-073447_069045-000027.parquet | 16 | 54 |  | True | True | 2026-07-08 | SBIN | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | SBIN | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\part-100112_430562-020475.parquet | 2 | 54 |  | True | False | 2026-07-08 | SBIN | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | SUNPHARMA | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\part-073447_183315-000028.parquet | 17 | 54 |  | True | True | 2026-07-08 | SUNPHARMA | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | SUNPHARMA | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\part-100143_068866-020503.parquet | 1 | 54 |  | True | False | 2026-07-08 | SUNPHARMA | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | TCS | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=TCS\part-073447_291090-000029.parquet | 7 | 54 |  | True | True | 2026-07-08 | TCS | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | TCS | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=TCS\part-100143_191036-020504.parquet | 1 | 54 |  | True | False | 2026-07-08 | TCS | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | TECHM | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\part-073447_402618-000030.parquet | 4 | 54 |  | True | True | 2026-07-08 | TECHM | ok |  |
| scratch_azcopy_selected\raw_l2 | 2026-07-08 | NSE | TECHM | scratch_azcopy_selected\raw_l2\trade_date=2026-07-08\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\part-100143_301299-020505.parquet | 1 | 54 |  | True | False | 2026-07-08 | TECHM | ok |  |

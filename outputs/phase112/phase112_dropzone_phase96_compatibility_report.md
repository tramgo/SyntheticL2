# Phase112 Drop-zone Phase96 Compatibility

Generated UTC: 2026-07-19T22:44:47.647986+00:00

Phase112 verifies that Phase96 can discover and diagnose the nested Phase111 drop-zone layout.
The generated fixture is intentionally tiny and strategy replay remains closed.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase112_check_rows | 6 | Drop-zone compatibility checks executed |
| phase112_checks_passed | 6 | Drop-zone compatibility checks passing |
| phase112_dropzone_compatibility_pass | 1 | 1 means Phase96 can scan the Phase111 drop-zone layout |
| phase112_fixture_symbol_rows | 2 | Fixture symbol partitions discovered |
| phase112_fixture_day_rows | 1 | Fixture day readiness rows built |
| phase112_strategy_replay_allowed | 0 | Strategy replay remains closed |

## Compatibility Checks

| check_id | passed | detail |
| --- | --- | --- |
| P112_NESTED_SYMBOL_DIRS_DISCOVERED | True | discovered_symbol_rows=2 |
| P112_TRADE_DATE_INFERRED_FROM_PATH | True | inferred_trade_dates=2026-07-20 |
| P112_EXCHANGE_INFERRED_FROM_PATH | True | inferred_exchanges=NSE |
| P112_REQUIRED_SCHEMA_VALID | True | schema_rows=2 |
| P112_SYMBOL_DAY_DIAGNOSTICS_BUILT | True | diagnostic_rows=2 |
| P112_DAY_READINESS_BUILT | True | day_readiness_rows=1 |

## Fixture Symbol Inventory

| panel_name | panel_root | symbol_dir | layout_path | inferred_trade_date | inferred_exchange | symbol | parquet_files | first_file | last_file |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| l2_multiday_panel | .tmp\phase112_dropzone_fixture\l2_multiday_panel | .tmp\phase112_dropzone_fixture\l2_multiday_panel\trade_date=2026-07-20\exchange=NSE\symbol=HDFCBANK | trade_date=2026-07-20\exchange=NSE\symbol=HDFCBANK | 2026-07-20 | NSE | HDFCBANK | 1 | .tmp\phase112_dropzone_fixture\l2_multiday_panel\trade_date=2026-07-20\exchange=NSE\symbol=HDFCBANK\part-00000.parquet | .tmp\phase112_dropzone_fixture\l2_multiday_panel\trade_date=2026-07-20\exchange=NSE\symbol=HDFCBANK\part-00000.parquet |
| l2_multiday_panel | .tmp\phase112_dropzone_fixture\l2_multiday_panel | .tmp\phase112_dropzone_fixture\l2_multiday_panel\trade_date=2026-07-20\exchange=NSE\symbol=INFY | trade_date=2026-07-20\exchange=NSE\symbol=INFY | 2026-07-20 | NSE | INFY | 1 | .tmp\phase112_dropzone_fixture\l2_multiday_panel\trade_date=2026-07-20\exchange=NSE\symbol=INFY\part-00000.parquet | .tmp\phase112_dropzone_fixture\l2_multiday_panel\trade_date=2026-07-20\exchange=NSE\symbol=INFY\part-00000.parquet |

## Fixture Day Readiness

| panel_name | trade_date | symbols_observed | expected_symbol_fraction | missing_expected_symbols | sampled_rows | schema_pass | l1_book_pass | timing_pass | day_ready_for_anchor_panel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| l2_multiday_panel | 2026-07-20 | 2 | 0.0625 | ADANIPORTS\|AXISBANK\|BAJAJ-AUTO\|BANKBEES\|BHARTIARTL\|BPCL\|BRITANNIA\|CIPLA\|DRREDDY\|GOLDBEES\|HCLTECH\|HINDUNILVR\|ICICIBANK\|ITBEES\|ITC\|JUNIORBEES\|KOTAKBANK\|LT\|M&M\|MARUTI\|NESTLEIND\|NIFTYBEES\|ONGC\|RELIANCE\|SBIN\|SUNPHARMA\|TCS\|TECHM\|ULTRACEMCO\|WIPRO | 6 | True | True | True | False |

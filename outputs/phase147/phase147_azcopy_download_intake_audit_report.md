# Phase147 AzCopy Download Intake Audit

Generated UTC: 2026-07-28T15:22:30.276921+00:00

Phase147 validates local AzCopy landing-zone contents for configured required real L2 dates before Phase145 import/refresh is attempted.
It is local-only: AzCopy owns Azure I/O; Python only inspects downloaded Parquet partitions.
It checks complete 32-symbol coverage, sampled Zerodha top-five market-by-price schema, bytes/files, target-vs-scratch state, and duplicate nested `trade_date` layouts.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase147_required_date_rows | 2 | Required dates checked in scratch and target |
| phase147_required_dates_satisfied | 2 | Required dates complete in scratch or target |
| phase147_required_dates_ready_for_import | 0 | Required dates complete in scratch but not target |
| phase147_required_dates_already_in_target | 2 | Required dates complete in canonical target |
| phase147_scratch_complete_dates | 2 | Scratch required dates complete for Phase145 |
| phase147_target_complete_dates | 2 | Target required dates already complete |
| phase147_nested_trade_date_symbol_dirs | 0 | Nested duplicate trade_date symbol dirs across checked roots |
| phase147_can_run_phase145_now | 0 | 1 means Phase145 should be run now |
| phase147_strategy_replay_allowed | 0 | Download intake never unlocks strategy replay |
| phase147_next_best_action | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase147 | Recommended next milestone |

## Date Intake

| location | root | trade_date | exchange | date_root_exists | expected_symbols | symbols_with_files | canonical_symbol_dirs | nested_trade_date_symbol_dirs | parquet_files | bytes | sample_files_checked | sample_failed_files | schema_symbols_pass | missing_symbols | date_complete_for_phase145 | date_clean_canonical_layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| scratch | scratch_azcopy_selected\raw_l2 | 2026-07-10 | NSE | True | 32 | 32 | 32 | 0 | 50509 | 1765607327 | 64 | 0 | 32 |  | True | True |
| target | real_data_sample\l2_multiday_panel | 2026-07-10 | NSE | True | 32 | 32 | 32 | 0 | 50509 | 1765607327 | 64 | 0 | 32 |  | True | True |
| scratch | scratch_azcopy_selected\raw_l2 | 2026-07-14 | NSE | True | 32 | 32 | 32 | 0 | 49732 | 1750854292 | 64 | 0 | 32 |  | True | True |
| target | real_data_sample\l2_multiday_panel | 2026-07-14 | NSE | True | 32 | 32 | 32 | 0 | 49732 | 1750854292 | 64 | 0 | 32 |  | True | True |

## Sample Schema Checks

| file | rows | column_count | required_schema_pass | missing_required_columns | observed_trade_dates | observed_symbols | read_status | read_error | location | trade_date | exchange | symbol |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\part-034501_427736-000006.parquet | 1 | 54 | True |  | 2026-07-10 | ADANIPORTS | ok |  | scratch | 2026-07-10 | NSE | ADANIPORTS |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\part-100459_922852-050494.parquet | 1 | 54 | True |  | 2026-07-10 | ADANIPORTS | ok |  | scratch | 2026-07-10 | NSE | ADANIPORTS |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\part-034501_554219-000007.parquet | 1 | 54 | True |  | 2026-07-10 | AXISBANK | ok |  | scratch | 2026-07-10 | NSE | AXISBANK |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\part-100500_057541-050495.parquet | 1 | 54 | True |  | 2026-07-10 | AXISBANK | ok |  | scratch | 2026-07-10 | NSE | AXISBANK |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\part-034501_687922-000008.parquet | 1 | 54 | True |  | 2026-07-10 | BAJAJ-AUTO | ok |  | scratch | 2026-07-10 | NSE | BAJAJ-AUTO |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\part-100500_189033-050496.parquet | 1 | 54 | True |  | 2026-07-10 | BAJAJ-AUTO | ok |  | scratch | 2026-07-10 | NSE | BAJAJ-AUTO |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\part-034515_256625-000036.parquet | 2 | 54 | True |  | 2026-07-10 | BANKBEES | ok |  | scratch | 2026-07-10 | NSE | BANKBEES |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\part-100500_312515-050497.parquet | 1 | 54 | True |  | 2026-07-10 | BANKBEES | ok |  | scratch | 2026-07-10 | NSE | BANKBEES |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\part-034501_813567-000009.parquet | 1 | 54 | True |  | 2026-07-10 | BHARTIARTL | ok |  | scratch | 2026-07-10 | NSE | BHARTIARTL |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\part-100500_440202-050498.parquet | 1 | 54 | True |  | 2026-07-10 | BHARTIARTL | ok |  | scratch | 2026-07-10 | NSE | BHARTIARTL |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\part-034501_935674-000010.parquet | 1 | 54 | True |  | 2026-07-10 | BPCL | ok |  | scratch | 2026-07-10 | NSE | BPCL |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\part-100500_560374-050499.parquet | 1 | 54 | True |  | 2026-07-10 | BPCL | ok |  | scratch | 2026-07-10 | NSE | BPCL |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\part-034502_065410-000011.parquet | 1 | 54 | True |  | 2026-07-10 | BRITANNIA | ok |  | scratch | 2026-07-10 | NSE | BRITANNIA |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\part-100500_706610-050500.parquet | 1 | 54 | True |  | 2026-07-10 | BRITANNIA | ok |  | scratch | 2026-07-10 | NSE | BRITANNIA |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\part-034502_196217-000012.parquet | 1 | 54 | True |  | 2026-07-10 | CIPLA | ok |  | scratch | 2026-07-10 | NSE | CIPLA |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\part-100500_845851-050501.parquet | 1 | 54 | True |  | 2026-07-10 | CIPLA | ok |  | scratch | 2026-07-10 | NSE | CIPLA |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=DRREDDY\part-034502_333833-000013.parquet | 1 | 54 | True |  | 2026-07-10 | DRREDDY | ok |  | scratch | 2026-07-10 | NSE | DRREDDY |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=DRREDDY\part-100116_245030-050470.parquet | 3 | 54 | True |  | 2026-07-10 | DRREDDY | ok |  | scratch | 2026-07-10 | NSE | DRREDDY |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=GOLDBEES\part-034515_924773-000042.parquet | 2 | 54 | True |  | 2026-07-10 | GOLDBEES | ok |  | scratch | 2026-07-10 | NSE | GOLDBEES |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=GOLDBEES\part-100500_982747-050502.parquet | 1 | 54 | True |  | 2026-07-10 | GOLDBEES | ok |  | scratch | 2026-07-10 | NSE | GOLDBEES |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=HCLTECH\part-034502_462491-000014.parquet | 1 | 54 | True |  | 2026-07-10 | HCLTECH | ok |  | scratch | 2026-07-10 | NSE | HCLTECH |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=HCLTECH\part-100116_495078-050472.parquet | 3 | 54 | True |  | 2026-07-10 | HCLTECH | ok |  | scratch | 2026-07-10 | NSE | HCLTECH |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=HDFCBANK\part-034502_590319-000015.parquet | 1 | 54 | True |  | 2026-07-10 | HDFCBANK | ok |  | scratch | 2026-07-10 | NSE | HDFCBANK |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=HDFCBANK\part-100116_612297-050473.parquet | 8 | 54 | True |  | 2026-07-10 | HDFCBANK | ok |  | scratch | 2026-07-10 | NSE | HDFCBANK |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=HINDUNILVR\part-034502_714378-000016.parquet | 1 | 54 | True |  | 2026-07-10 | HINDUNILVR | ok |  | scratch | 2026-07-10 | NSE | HINDUNILVR |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=HINDUNILVR\part-100501_119585-050503.parquet | 1 | 54 | True |  | 2026-07-10 | HINDUNILVR | ok |  | scratch | 2026-07-10 | NSE | HINDUNILVR |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=ICICIBANK\part-034502_837031-000017.parquet | 1 | 54 | True |  | 2026-07-10 | ICICIBANK | ok |  | scratch | 2026-07-10 | NSE | ICICIBANK |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=ICICIBANK\part-100116_866685-050475.parquet | 4 | 54 | True |  | 2026-07-10 | ICICIBANK | ok |  | scratch | 2026-07-10 | NSE | ICICIBANK |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=INFY\part-034502_957663-000018.parquet | 1 | 54 | True |  | 2026-07-10 | INFY | ok |  | scratch | 2026-07-10 | NSE | INFY |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=INFY\part-100116_988612-050476.parquet | 6 | 54 | True |  | 2026-07-10 | INFY | ok |  | scratch | 2026-07-10 | NSE | INFY |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=ITBEES\part-034516_587518-000048.parquet | 2 | 54 | True |  | 2026-07-10 | ITBEES | ok |  | scratch | 2026-07-10 | NSE | ITBEES |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=ITBEES\part-100501_269037-050504.parquet | 1 | 54 | True |  | 2026-07-10 | ITBEES | ok |  | scratch | 2026-07-10 | NSE | ITBEES |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=ITC\part-034503_084233-000019.parquet | 1 | 54 | True |  | 2026-07-10 | ITC | ok |  | scratch | 2026-07-10 | NSE | ITC |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=ITC\part-100117_301894-050478.parquet | 7 | 54 | True |  | 2026-07-10 | ITC | ok |  | scratch | 2026-07-10 | NSE | ITC |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=JUNIORBEES\part-034516_831123-000050.parquet | 2 | 54 | True |  | 2026-07-10 | JUNIORBEES | ok |  | scratch | 2026-07-10 | NSE | JUNIORBEES |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=JUNIORBEES\part-100117_423795-050479.parquet | 3 | 54 | True |  | 2026-07-10 | JUNIORBEES | ok |  | scratch | 2026-07-10 | NSE | JUNIORBEES |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=KOTAKBANK\part-034503_210949-000020.parquet | 2 | 54 | True |  | 2026-07-10 | KOTAKBANK | ok |  | scratch | 2026-07-10 | NSE | KOTAKBANK |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=KOTAKBANK\part-100501_421627-050505.parquet | 1 | 54 | True |  | 2026-07-10 | KOTAKBANK | ok |  | scratch | 2026-07-10 | NSE | KOTAKBANK |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=LT\part-034503_332609-000021.parquet | 1 | 54 | True |  | 2026-07-10 | LT | ok |  | scratch | 2026-07-10 | NSE | LT |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=LT\part-100501_551617-050506.parquet | 1 | 54 | True |  | 2026-07-10 | LT | ok |  | scratch | 2026-07-10 | NSE | LT |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=M&M\part-034503_456777-000022.parquet | 1 | 54 | True |  | 2026-07-10 | M&M | ok |  | scratch | 2026-07-10 | NSE | M&M |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=M&M\part-100501_679090-050507.parquet | 1 | 54 | True |  | 2026-07-10 | M&M | ok |  | scratch | 2026-07-10 | NSE | M&M |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=MARUTI\part-034503_581048-000023.parquet | 1 | 54 | True |  | 2026-07-10 | MARUTI | ok |  | scratch | 2026-07-10 | NSE | MARUTI |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=MARUTI\part-100117_914479-050483.parquet | 5 | 54 | True |  | 2026-07-10 | MARUTI | ok |  | scratch | 2026-07-10 | NSE | MARUTI |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=NESTLEIND\part-034503_704039-000024.parquet | 1 | 54 | True |  | 2026-07-10 | NESTLEIND | ok |  | scratch | 2026-07-10 | NSE | NESTLEIND |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=NESTLEIND\part-100501_808605-050508.parquet | 1 | 54 | True |  | 2026-07-10 | NESTLEIND | ok |  | scratch | 2026-07-10 | NSE | NESTLEIND |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=NIFTYBEES\part-034517_509328-000056.parquet | 2 | 54 | True |  | 2026-07-10 | NIFTYBEES | ok |  | scratch | 2026-07-10 | NSE | NIFTYBEES |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=NIFTYBEES\part-100501_949071-050509.parquet | 1 | 54 | True |  | 2026-07-10 | NIFTYBEES | ok |  | scratch | 2026-07-10 | NSE | NIFTYBEES |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=ONGC\part-034503_830760-000025.parquet | 1 | 54 | True |  | 2026-07-10 | ONGC | ok |  | scratch | 2026-07-10 | NSE | ONGC |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=ONGC\part-100502_083531-050510.parquet | 1 | 54 | True |  | 2026-07-10 | ONGC | ok |  | scratch | 2026-07-10 | NSE | ONGC |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=RELIANCE\part-034503_950112-000026.parquet | 1 | 54 | True |  | 2026-07-10 | RELIANCE | ok |  | scratch | 2026-07-10 | NSE | RELIANCE |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=RELIANCE\part-100118_427973-050487.parquet | 3 | 54 | True |  | 2026-07-10 | RELIANCE | ok |  | scratch | 2026-07-10 | NSE | RELIANCE |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=SBIN\part-034504_082031-000027.parquet | 2 | 54 | True |  | 2026-07-10 | SBIN | ok |  | scratch | 2026-07-10 | NSE | SBIN |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=SBIN\part-100118_549569-050488.parquet | 7 | 54 | True |  | 2026-07-10 | SBIN | ok |  | scratch | 2026-07-10 | NSE | SBIN |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=SUNPHARMA\part-034504_206778-000028.parquet | 1 | 54 | True |  | 2026-07-10 | SUNPHARMA | ok |  | scratch | 2026-07-10 | NSE | SUNPHARMA |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=SUNPHARMA\part-100502_213121-050511.parquet | 1 | 54 | True |  | 2026-07-10 | SUNPHARMA | ok |  | scratch | 2026-07-10 | NSE | SUNPHARMA |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=TCS\part-034504_326835-000029.parquet | 1 | 54 | True |  | 2026-07-10 | TCS | ok |  | scratch | 2026-07-10 | NSE | TCS |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=TCS\part-100118_856115-050490.parquet | 7 | 54 | True |  | 2026-07-10 | TCS | ok |  | scratch | 2026-07-10 | NSE | TCS |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=TECHM\part-034504_447838-000030.parquet | 1 | 54 | True |  | 2026-07-10 | TECHM | ok |  | scratch | 2026-07-10 | NSE | TECHM |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=TECHM\part-100502_338219-050512.parquet | 1 | 54 | True |  | 2026-07-10 | TECHM | ok |  | scratch | 2026-07-10 | NSE | TECHM |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=ULTRACEMCO\part-034504_579897-000031.parquet | 1 | 54 | True |  | 2026-07-10 | ULTRACEMCO | ok |  | scratch | 2026-07-10 | NSE | ULTRACEMCO |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=ULTRACEMCO\part-100502_466504-050513.parquet | 1 | 54 | True |  | 2026-07-10 | ULTRACEMCO | ok |  | scratch | 2026-07-10 | NSE | ULTRACEMCO |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=WIPRO\part-034504_701826-000032.parquet | 1 | 54 | True |  | 2026-07-10 | WIPRO | ok |  | scratch | 2026-07-10 | NSE | WIPRO |
| scratch_azcopy_selected\raw_l2\trade_date=2026-07-10\exchange=NSE\symbol=WIPRO\part-100502_587143-050514.parquet | 1 | 54 | True |  | 2026-07-10 | WIPRO | ok |  | scratch | 2026-07-10 | NSE | WIPRO |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\part-034501_427736-000006.parquet | 1 | 54 | True |  | 2026-07-10 | ADANIPORTS | ok |  | target | 2026-07-10 | NSE | ADANIPORTS |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\part-100459_922852-050494.parquet | 1 | 54 | True |  | 2026-07-10 | ADANIPORTS | ok |  | target | 2026-07-10 | NSE | ADANIPORTS |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\part-034501_554219-000007.parquet | 1 | 54 | True |  | 2026-07-10 | AXISBANK | ok |  | target | 2026-07-10 | NSE | AXISBANK |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\part-100500_057541-050495.parquet | 1 | 54 | True |  | 2026-07-10 | AXISBANK | ok |  | target | 2026-07-10 | NSE | AXISBANK |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\part-034501_687922-000008.parquet | 1 | 54 | True |  | 2026-07-10 | BAJAJ-AUTO | ok |  | target | 2026-07-10 | NSE | BAJAJ-AUTO |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\part-100500_189033-050496.parquet | 1 | 54 | True |  | 2026-07-10 | BAJAJ-AUTO | ok |  | target | 2026-07-10 | NSE | BAJAJ-AUTO |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\part-034515_256625-000036.parquet | 2 | 54 | True |  | 2026-07-10 | BANKBEES | ok |  | target | 2026-07-10 | NSE | BANKBEES |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\part-100500_312515-050497.parquet | 1 | 54 | True |  | 2026-07-10 | BANKBEES | ok |  | target | 2026-07-10 | NSE | BANKBEES |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\part-034501_813567-000009.parquet | 1 | 54 | True |  | 2026-07-10 | BHARTIARTL | ok |  | target | 2026-07-10 | NSE | BHARTIARTL |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\part-100500_440202-050498.parquet | 1 | 54 | True |  | 2026-07-10 | BHARTIARTL | ok |  | target | 2026-07-10 | NSE | BHARTIARTL |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\part-034501_935674-000010.parquet | 1 | 54 | True |  | 2026-07-10 | BPCL | ok |  | target | 2026-07-10 | NSE | BPCL |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\part-100500_560374-050499.parquet | 1 | 54 | True |  | 2026-07-10 | BPCL | ok |  | target | 2026-07-10 | NSE | BPCL |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\part-034502_065410-000011.parquet | 1 | 54 | True |  | 2026-07-10 | BRITANNIA | ok |  | target | 2026-07-10 | NSE | BRITANNIA |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\part-100500_706610-050500.parquet | 1 | 54 | True |  | 2026-07-10 | BRITANNIA | ok |  | target | 2026-07-10 | NSE | BRITANNIA |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\part-034502_196217-000012.parquet | 1 | 54 | True |  | 2026-07-10 | CIPLA | ok |  | target | 2026-07-10 | NSE | CIPLA |
| real_data_sample\l2_multiday_panel\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\part-100500_845851-050501.parquet | 1 | 54 | True |  | 2026-07-10 | CIPLA | ok |  | target | 2026-07-10 | NSE | CIPLA |

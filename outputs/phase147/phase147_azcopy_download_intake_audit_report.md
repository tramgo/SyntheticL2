# Phase147 AzCopy Download Intake Audit

Generated UTC: 2026-07-23T18:47:35.541283+00:00

Phase147 validates local AzCopy landing-zone contents for configured required real L2 dates before Phase145 import/refresh is attempted.
It is local-only: AzCopy owns Azure I/O; Python only inspects downloaded Parquet partitions.
It checks complete 32-symbol coverage, sampled Zerodha top-five market-by-price schema, bytes/files, target-vs-scratch state, and duplicate nested `trade_date` layouts.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase147_required_date_rows | 2 | Required dates checked in scratch and target |
| phase147_required_dates_satisfied | 0 | Required dates complete in scratch or target |
| phase147_required_dates_ready_for_import | 0 | Required dates complete in scratch but not target |
| phase147_required_dates_already_in_target | 0 | Required dates complete in canonical target |
| phase147_scratch_complete_dates | 0 | Scratch required dates complete for Phase145 |
| phase147_target_complete_dates | 0 | Target required dates already complete |
| phase147_nested_trade_date_symbol_dirs | 0 | Nested duplicate trade_date symbol dirs across checked roots |
| phase147_can_run_phase145_now | 0 | 1 means Phase145 should be run now |
| phase147_strategy_replay_allowed | 0 | Download intake never unlocks strategy replay |
| phase147_next_best_action | download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase147 | Recommended next milestone |

## Date Intake

| location | root | trade_date | exchange | date_root_exists | expected_symbols | symbols_with_files | canonical_symbol_dirs | nested_trade_date_symbol_dirs | parquet_files | bytes | sample_files_checked | sample_failed_files | schema_symbols_pass | missing_symbols | date_complete_for_phase145 | date_clean_canonical_layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| scratch | scratch_azcopy_selected\raw_l2 | 2026-07-10 | NSE | True | 32 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | ADANIPORTS\|AXISBANK\|BAJAJ-AUTO\|BANKBEES\|BHARTIARTL\|BPCL\|BRITANNIA\|CIPLA\|DRREDDY\|GOLDBEES\|HCLTECH\|HDFCBANK\|HINDUNILVR\|ICICIBANK\|INFY\|ITBEES\|ITC\|JUNIORBEES\|KOTAKBANK\|LT\|M&M\|MARUTI\|NESTLEIND\|NIFTYBEES\|ONGC\|RELIANCE\|SBIN\|SUNPHARMA\|TCS\|TECHM\|ULTRACEMCO\|WIPRO | False | False |
| target | real_data_sample\l2_multiday_panel | 2026-07-10 | NSE | False | 32 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | ADANIPORTS\|AXISBANK\|BAJAJ-AUTO\|BANKBEES\|BHARTIARTL\|BPCL\|BRITANNIA\|CIPLA\|DRREDDY\|GOLDBEES\|HCLTECH\|HDFCBANK\|HINDUNILVR\|ICICIBANK\|INFY\|ITBEES\|ITC\|JUNIORBEES\|KOTAKBANK\|LT\|M&M\|MARUTI\|NESTLEIND\|NIFTYBEES\|ONGC\|RELIANCE\|SBIN\|SUNPHARMA\|TCS\|TECHM\|ULTRACEMCO\|WIPRO | False | False |
| scratch | scratch_azcopy_selected\raw_l2 | 2026-07-14 | NSE | False | 32 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | ADANIPORTS\|AXISBANK\|BAJAJ-AUTO\|BANKBEES\|BHARTIARTL\|BPCL\|BRITANNIA\|CIPLA\|DRREDDY\|GOLDBEES\|HCLTECH\|HDFCBANK\|HINDUNILVR\|ICICIBANK\|INFY\|ITBEES\|ITC\|JUNIORBEES\|KOTAKBANK\|LT\|M&M\|MARUTI\|NESTLEIND\|NIFTYBEES\|ONGC\|RELIANCE\|SBIN\|SUNPHARMA\|TCS\|TECHM\|ULTRACEMCO\|WIPRO | False | False |
| target | real_data_sample\l2_multiday_panel | 2026-07-14 | NSE | False | 32 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | ADANIPORTS\|AXISBANK\|BAJAJ-AUTO\|BANKBEES\|BHARTIARTL\|BPCL\|BRITANNIA\|CIPLA\|DRREDDY\|GOLDBEES\|HCLTECH\|HDFCBANK\|HINDUNILVR\|ICICIBANK\|INFY\|ITBEES\|ITC\|JUNIORBEES\|KOTAKBANK\|LT\|M&M\|MARUTI\|NESTLEIND\|NIFTYBEES\|ONGC\|RELIANCE\|SBIN\|SUNPHARMA\|TCS\|TECHM\|ULTRACEMCO\|WIPRO | False | False |

## Sample Schema Checks

_No rows._

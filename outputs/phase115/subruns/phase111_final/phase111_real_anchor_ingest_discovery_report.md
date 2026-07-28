# Phase111 Real Anchor Ingest Discovery

Generated UTC: 2026-07-28T15:11:10.775839+00:00

Phase111 scans likely local real-data roots for additional Zerodha WebSocket L2 panels and emits a concrete import/validation plan.
It is an operational bridge from the Phase110 multiday blocker to the next Phase96/Phase110 rerun.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase111_candidate_rows | 2 | Candidate real panel roots discovered or checked |
| phase111_ready_candidate_roots | 0 | Candidate roots ready for Phase96 scan |
| phase111_current_ready_real_days | 5 | Ready real days currently proven by Phase110/Phase96 |
| phase111_max_candidate_trade_dates | 0 | Maximum distinct trade dates discovered in any candidate root |
| phase111_additional_real_dates_found | 0 | 1 means a candidate root appears to contain more dates than current Phase96 evidence |
| phase111_days_needed_for_min | 0 | Additional ready real days still required for minimum replay-unlock consideration |
| phase111_import_plan_rows | 1 | Import/validation plan rows emitted |
| phase111_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase111_recommend_next_action | drop_or_ingest_4_more_real_l2_days_then_rerun_phase96_phase110 | Recommended next milestone |

## Candidate Real Panel Inventory

| candidate_root | panel_root | discovery_status | layout_type | parquet_files | symbols_observed | expected_symbol_fraction | trade_dates_observed | trade_date_list | ready_for_schema_scan | ready_for_phase96_scan | recommended_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| raw_l2 |  | missing_root | missing | 0 | 0 | 0 | 0 |  | False | False | place_real_l2_parquet_under_this_root_or_register_another_candidate_root |
| scratch_l2_sample_20260710_HDFCBANK |  | missing_root | missing | 0 | 0 | 0 | 0 |  | False | False | place_real_l2_parquet_under_this_root_or_register_another_candidate_root |

## Import Plan

| priority | candidate_panel_root | candidate_trade_dates | candidate_symbols_observed | candidate_expected_symbol_fraction | current_ready_days | current_ready_dates | phase96_command | acceptance_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  | 0 | 0 | 5 | 2026-07-08\|2026-07-09\|2026-07-10\|2026-07-13\|2026-07-14 |  | drop or ingest at least 4 more ready 32-symbol Zerodha WebSocket L2 days, then rerun Phase96 and Phase110 |

## Dropzone Manifest

| field | value | why |
| --- | --- | --- |
| recommended_root | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | A trade_date/exchange/symbol partitioned layout lets Phase111 discover distinct dates and lets Phase96 validate each day. |
| minimum_additional_ready_days_needed | 0 | Phase110 requires at least 5 ready real anchor days before replay can even be considered. |
| target_additional_ready_days_needed | 5 | 10 ready real days is the preferred target for more stable calibration evidence. |
| required_symbol_universe | ADANIPORTS\|AXISBANK\|BAJAJ-AUTO\|BANKBEES\|BHARTIARTL\|BPCL\|BRITANNIA\|CIPLA\|DRREDDY\|GOLDBEES\|HCLTECH\|HDFCBANK\|HINDUNILVR\|ICICIBANK\|INFY\|ITBEES\|ITC\|JUNIORBEES\|KOTAKBANK\|LT\|M&M\|MARUTI\|NESTLEIND\|NIFTYBEES\|ONGC\|RELIANCE\|SBIN\|SUNPHARMA\|TCS\|TECHM\|ULTRACEMCO\|WIPRO | The full-symbol realism gate compares the fixed 32-symbol universe. |
| post_ingest_commands | python scripts/run_phase111_real_anchor_ingest_discovery.py; python scripts/run_phase96_real_anchor_panel_builder.py; python scripts/run_phase110_multiday_replay_unlock_gate.py | Discovery, readiness validation, and replay-unlock status must be refreshed after new real data arrives. |

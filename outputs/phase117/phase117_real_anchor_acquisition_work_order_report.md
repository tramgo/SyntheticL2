# Phase117 Real Anchor Acquisition Work Order

Generated UTC: 2026-07-19T23:04:00.445286+00:00

Phase117 converts the Phase116 next-action verdict into an operational work order.
It does not claim more strategy evidence. It states exactly what real Zerodha WebSocket L2 data must be added before replay can reopen.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase117_current_ready_real_anchor_days | 1 | Ready real anchor days proven by latest Phase115/Phase110 evidence |
| phase117_additional_days_needed_for_min | 4 | Additional ready real days needed for minimum replay unlock consideration |
| phase117_additional_days_needed_for_target | 9 | Additional ready real days needed for preferred 10-day target |
| phase117_local_candidate_panel_rows | 4 | Local candidate panel roots/files inventoried |
| phase117_ready_candidate_panel_rows | 1 | Candidate panels with broad enough symbol coverage for import validation |
| phase117_minimum_unlock_acquisition_slots | 4 | Concrete missing day slots required for minimum unlock |
| phase117_strategy_replay_allowed | 0 | Current replay allowed flag inherited from Phase115 |
| phase117_same_family_shard_continuation_allowed | 0 | Current failed-family compute gate inherited from Phase116 |
| phase117_acquisition_gate_status | open | Whether additional real data must be acquired before replay work |
| phase117_next_best_action | drop_or_sync_4_more_real_l2_days_then_run_phase115_with_execute_import | Recommended next milestone |

## Local Real L2 Candidate Inventory

| candidate_root | panel_root | status | layout_type | parquet_files | bytes | symbols_observed | expected_symbol_fraction | trade_dates_observed | trade_date_list | ready_candidate | recommended_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_data_sample | real_data_sample | found_parquet | symbol_only_or_unknown_date | 50205 | 1764005784 | 32 | 1 | 0 |  | False | validate_with_phase115_execute_import |
| real_data_sample | real_data_sample\l2_single_day | found_parquet | trade_date_symbol | 50205 | 1764005784 | 32 | 1 | 1 | unknown_single_day | True | validate_with_phase115_execute_import |
| raw_l2 |  | missing_root | missing | 0 | 0 | 0 | 0 | 0 |  | False | create_this_root_or_place_exported_real_l2_partitions_here |
| scratch_l2_sample_20260710_HDFCBANK |  | missing_root | missing | 0 | 0 | 0 | 0 | 0 |  | False | create_this_root_or_place_exported_real_l2_partitions_here |

## Real L2 Acquisition Slots

| slot_id | required_for | trade_date | exchange | symbols_required | minimum_expected_symbol_fraction | required_layout | required_tick_content | acceptance_after_drop |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REAL_L2_DAY_02 | minimum_unlock | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha WebSocket-like callbacks with L1-L5 bid/ask price, quantity and order count persisted per update | Phase115 --execute-import completes with Phase96 ready day count incremented |
| REAL_L2_DAY_03 | minimum_unlock | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha WebSocket-like callbacks with L1-L5 bid/ask price, quantity and order count persisted per update | Phase115 --execute-import completes with Phase96 ready day count incremented |
| REAL_L2_DAY_04 | minimum_unlock | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha WebSocket-like callbacks with L1-L5 bid/ask price, quantity and order count persisted per update | Phase115 --execute-import completes with Phase96 ready day count incremented |
| REAL_L2_DAY_05 | minimum_unlock | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha WebSocket-like callbacks with L1-L5 bid/ask price, quantity and order count persisted per update | Phase115 --execute-import completes with Phase96 ready day count incremented |
| REAL_L2_DAY_06 | preferred_target | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha WebSocket-like callbacks with L1-L5 bid/ask price, quantity and order count persisted per update | Phase115 --execute-import completes with Phase96 ready day count incremented |
| REAL_L2_DAY_07 | preferred_target | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha WebSocket-like callbacks with L1-L5 bid/ask price, quantity and order count persisted per update | Phase115 --execute-import completes with Phase96 ready day count incremented |
| REAL_L2_DAY_08 | preferred_target | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha WebSocket-like callbacks with L1-L5 bid/ask price, quantity and order count persisted per update | Phase115 --execute-import completes with Phase96 ready day count incremented |
| REAL_L2_DAY_09 | preferred_target | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha WebSocket-like callbacks with L1-L5 bid/ask price, quantity and order count persisted per update | Phase115 --execute-import completes with Phase96 ready day count incremented |
| REAL_L2_DAY_10 | preferred_target | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha WebSocket-like callbacks with L1-L5 bid/ask price, quantity and order count persisted per update | Phase115 --execute-import completes with Phase96 ready day count incremented |

## Phase115 Import Execution Plan

| step | action | command | runs_now | why |
| --- | --- | --- | --- | --- |
| 1 | drop_or_sync_real_l2_exports | Place each new day under real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | False | The current workspace has only one ready real anchor day; new external data must arrive before replay can unlock. |
| 2 | dry_run_discovery | python scripts/run_phase115_real_panel_refresh_orchestrator.py | True | Confirms candidate inventory without copying files. |
| 3 | execute_import_and_refresh_gates | python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import | False | Copies normalized drop-zone files, verifies integrity, rebuilds Phase96 readiness and Phase110 replay-unlock evidence. |
| 4 | review_unlock | Import-Csv outputs/phase115/phase115_real_panel_refresh_acceptance_summary.csv | True | Replay remains closed unless ready real anchor days reach the required gate and downstream realism gates are refreshed. |

# Phase137 Post-Phase132 Real-Anchor Restart

Generated UTC: 2026-07-23T08:17:21.690150+00:00

Phase137 converts the Phase132 clean falsification into the next operational path: real Zerodha L2 anchor acquisition.
It does not reopen synthetic strategy work, run Phase133-136, emit order simulations, or change replay permissions.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase137_closed_branch_rows | 1 | Closed synthetic top-five-depth branch ledger rows |
| phase137_phase132_kill_switch_fired | 1 | Phase132 kill-switch flag carried forward |
| phase137_phase116_deep_book_blocklist_present | 1 | Phase116 DEEP_BOOK_LABEL_LIFT row present |
| phase137_current_ready_real_anchor_days | 3 | Ready real-anchor days currently proven |
| phase137_additional_days_needed_for_min | 2 | Additional ready real days needed for minimum replay-unlock review |
| phase137_additional_days_needed_for_target | 7 | Additional ready real days needed for preferred 10-day target |
| phase137_real_anchor_requirement_rows | 7 | Real-anchor acquisition requirement rows emitted |
| phase137_gate_rows | 5 | Gates evaluated |
| phase137_all_gates_pass | 1 | 1 means Phase137 restart work order is self-consistent |
| phase137_strategy_replay_allowed | 0 | Replay flag remains inherited from Phase115 |
| phase137_next_best_action | drop_or_sync_2_more_real_l2_days_then_run_phase115_execute_import | Recommended next milestone |
| phase137_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned cost model retained for audit continuity |

## Closed Synthetic Branch Ledger

| closed_branch_id | phase132_kill_switch_fired | phase132_surviving_feature_rows | phase132_labels_cleared_brier_lift | phase116_blocklist_entry_present | phase133_136_allowed | synthetic_strategy_branch_allowed | strategy_replay_allowed | closure_verdict | why |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PHASE131_132_TOP_FIVE_DEPTH_LABEL_LIFT | 1 | 0 | 0 | 1 | 0 | 0 | 0 | falsified | Phase132 found no top-five-depth diagnostic lift over Phase130 baselines; continuation plan says skip Phase133-136. |

## Real Anchor Acquisition Requirements

| slot_id | required_for | current_ready_real_anchor_days | trade_date | exchange | symbols_required | minimum_expected_symbol_fraction | required_layout | required_content | acceptance_command_after_drop | unlock_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| POST_P132_REAL_L2_DAY_04 | minimum_replay_unlock_review | 3 | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha Level-2/top-five market-by-price WebSocket updates with depth_level_1 through depth_level_5 bid/ask price, quantity and order-count fields | python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import | Replay remains closed until Phase115/Phase110 prove enough ready real-anchor days and downstream realism gates are refreshed. |
| POST_P132_REAL_L2_DAY_05 | minimum_replay_unlock_review | 3 | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha Level-2/top-five market-by-price WebSocket updates with depth_level_1 through depth_level_5 bid/ask price, quantity and order-count fields | python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import | Replay remains closed until Phase115/Phase110 prove enough ready real-anchor days and downstream realism gates are refreshed. |
| POST_P132_REAL_L2_DAY_06 | preferred_real_anchor_target | 3 | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha Level-2/top-five market-by-price WebSocket updates with depth_level_1 through depth_level_5 bid/ask price, quantity and order-count fields | python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import | Replay remains closed until Phase115/Phase110 prove enough ready real-anchor days and downstream realism gates are refreshed. |
| POST_P132_REAL_L2_DAY_07 | preferred_real_anchor_target | 3 | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha Level-2/top-five market-by-price WebSocket updates with depth_level_1 through depth_level_5 bid/ask price, quantity and order-count fields | python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import | Replay remains closed until Phase115/Phase110 prove enough ready real-anchor days and downstream realism gates are refreshed. |
| POST_P132_REAL_L2_DAY_08 | preferred_real_anchor_target | 3 | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha Level-2/top-five market-by-price WebSocket updates with depth_level_1 through depth_level_5 bid/ask price, quantity and order-count fields | python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import | Replay remains closed until Phase115/Phase110 prove enough ready real-anchor days and downstream realism gates are refreshed. |
| POST_P132_REAL_L2_DAY_09 | preferred_real_anchor_target | 3 | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha Level-2/top-five market-by-price WebSocket updates with depth_level_1 through depth_level_5 bid/ask price, quantity and order-count fields | python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import | Replay remains closed until Phase115/Phase110 prove enough ready real-anchor days and downstream realism gates are refreshed. |
| POST_P132_REAL_L2_DAY_10 | preferred_real_anchor_target | 3 | TBD_real_nse_trading_day | NSE | 32 | 0.95 | real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | raw Zerodha Level-2/top-five market-by-price WebSocket updates with depth_level_1 through depth_level_5 bid/ask price, quantity and order-count fields | python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import | Replay remains closed until Phase115/Phase110 prove enough ready real-anchor days and downstream realism gates are refreshed. |

## Operational Runbook

| step | action | command | runs_now | expected_evidence |
| --- | --- | --- | --- | --- |
| 1 | stop_synthetic_strategy_branching | No command. Do not run Phase133-136 for the closed Phase131-132 branch. | False | outputs/phase132/kill_switch_summary.csv has kill_switch_fired=1 and outputs/phase116/strategy_replay_blocklist.csv contains DEEP_BOOK_LABEL_LIFT. |
| 2 | collect_or_sync_real_l2_days | Add at least 2 new real NSE trading days under real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet | False | Each new day covers at least 95 percent of the current 32-symbol universe and includes top-five market-by-price depth fields. |
| 3 | dry_run_refresh | python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel | False | Phase115 discovers candidate days without copying files; use this if newly dropped data needs layout validation first. |
| 4 | execute_import_refresh | python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import | False | Phase113 copies files, Phase114 integrity passes, Phase96/Phase110 ready day counts update. |
| 5 | review_replay_unlock_gate | Import-Csv outputs/phase115/phase115_real_panel_refresh_acceptance_summary.csv | False | Replay remains closed unless Phase110/115 explicitly prove unlock conditions. |

## Gate Evaluation

| gate_id | gate_pass | evidence |
| --- | --- | --- |
| P137_PHASE132_BRANCH_CLOSED | 1 | closure_verdict=falsified |
| P137_PHASE133_136_SKIPPED | 1 | phase133_136_allowed=0 |
| P137_REAL_ANCHOR_DEFICIT_DECLARED | 1 | ready_real_anchor_days=3; days_needed_for_min=2 |
| P137_OPERATIONAL_RUNBOOK_DECLARED | 1 | post-Phase132 real-anchor acquisition runbook emitted |
| P137_REPLAY_REMAINS_CLOSED | 1 | phase115_strategy_replay_allowed=0 |

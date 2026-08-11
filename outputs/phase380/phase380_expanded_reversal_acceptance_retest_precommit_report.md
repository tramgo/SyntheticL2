# Phase380 Expanded Reversal Acceptance Retest Precommit

Generated: 2026-08-11T19:51:28.318225+00:00

Phase380 precommits the expanded real-L2 acceptance retest after Phase379 opened the event-count gate. It adapts the refreshed Phase379 work order into the Phase363/Phase381 execution schema without changing the frozen strategy parameters.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase380_expanded_reversal_acceptance_retest_precommit_complete | 1 | Phase380 complete |
| phase380_frozen_primary_scenario_id | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | Frozen primary scenario |
| phase380_adapted_work_order_rows | 233 | Expanded work-order rows |
| phase380_adapted_work_order_dates | 13 | Diagnostic dates |
| phase380_adapted_work_order_symbols | 27 | Symbols |
| phase380_phase379_estimated_selected_after_refresh | 32.29268292682927 | Phase379 selected-event estimate |
| phase380_event_floor_open | 1 | Event floor open |
| phase380_parameter_search_allowed | 0 | No search |
| phase380_strategy_retest_executed_now | 0 | No retest in precommit |
| phase380_strategy_promotion_allowed | 0 | No promotion |
| phase380_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase380_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase380_hard_gate_pass_rows | 6 | Passed gates |
| phase380_hard_gate_rows | 6 | Gates |
| phase380_next_best_action | execute_phase381_expanded_real_l2_frozen_reversal_acceptance_retest_no_search_no_paper_live | Recommended next action |

## Retest contract

| contract_id | source_thesis_id | frozen_primary_scenario_id | frozen_grid_id | work_order_source | adapted_work_order | parameter_search_allowed | strategy_retest_executed_now | full_depth_levels_1_to_5_required | levels_2_to_5_materiality_required | cost_model | acceptance_event_floor | paper_live_or_profit_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P380_EXPANDED_REAL_L2_RETEST_PRECOMMIT | P365_POST_CATALYST_IMPULSE_REVERSAL_AFTER_REPLENISHMENT | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | P362_D120_I2p5_D0p25_R0p0 | outputs\phase379\phase373_refreshed_execution_work_order.csv | phase380_phase360_execution_work_order.csv | 0 | 0 | 1 | 1 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | 30 | 0 |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P380_PHASE379_EVENT_FLOOR_OPEN | 1 | estimated_selected=32.29268292682927; floor=30 |
| P380_PHASE365_FROZEN_THESIS_PRESENT | 1 | P365_POST_CATALYST_IMPULSE_REVERSAL_AFTER_REPLENISHMENT |
| P380_EXPANDED_WORK_ORDER_PRESENT | 1 | rows=233 |
| P380_FULL_DEPTH_AND_COST_RULE_RETAINED | 1 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| P380_NO_SEARCH_NO_RETEST_YET | 1 | precommit_only |
| P380_NO_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No strategy retest, search, promotion, paper/live acceptance, or deployable profitability claim is opened in this precommit.

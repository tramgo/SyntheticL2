# Phase381 Expanded Reversal Acceptance Retest

Generated: 2026-08-11T19:55:05.285403+00:00

Phase381 executes the Phase380 precommitted expanded real-L2 frozen reversal retest. It uses one frozen grid row plus the registered same-filter continuation side-flip control. It performs no parameter search and opens no paper/live action.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase381_expanded_reversal_acceptance_retest_complete | 1 | Phase381 complete |
| phase381_work_order_rows | 233 | Expanded work-order rows replayed |
| phase381_missing_local_l2_rows | 0 | Rows whose diagnostic date has no local L2 root |
| phase381_event_feature_rows | 233 | Event feature rows |
| phase381_ready_event_feature_rows | 233 | Ready event feature rows |
| phase381_trade_rows | 56 | Trade ledger rows |
| phase381_scenario_rows | 2 | Scenario rows |
| phase381_primary_scenario_id | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | Frozen primary scenario |
| phase381_primary_selected_trade_rows | 19 | Primary capacity-selected trades |
| phase381_primary_diagnostic_dates | 11 | Primary diagnostic dates |
| phase381_primary_symbols | 11 | Primary symbols |
| phase381_primary_positive_symbols | 5 | Primary positive symbols |
| phase381_primary_positive_symbol_date_cells | 7 | Primary positive symbol-date cells |
| phase381_primary_net_pnl_inr | 2803.43 | Primary net PnL |
| phase381_primary_annualized_return_pct | 25.6896 | Primary annualized return |
| phase381_primary_above12 | 1 | Primary above 12% |
| phase381_primary_event_floor_met | 0 | Primary event floor |
| phase381_primary_breadth_met | 1 | Primary breadth gate |
| phase381_primary_acceptance_candidate | 0 | Primary acceptance candidate |
| phase381_side_flip_annualized_return_pct | -93.5524 | Side-flip control annualized return |
| phase381_strategy_promotion_allowed | 0 | Promotion allowed only if primary acceptance candidate |
| phase381_paper_or_live_acceptance_allowed | 0 | No paper/live action in this phase |
| phase381_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase381_hard_gate_pass_rows | 8 | Passed hard gates |
| phase381_hard_gate_rows | 8 | Hard gates |
| phase381_next_best_action | interpret_phase381_acceptance_result_no_paper_live | Recommended next action |

## Scenario summary

| scenario_id | scenario_role | scheduled_event_rows | capacity_selected_trade_rows | diagnostic_trade_dates | symbols | positive_trade_rows | positive_symbols | positive_symbol_date_cells | net_pnl_inr | annualized_return_pct | above12 | event_floor_met | breadth_met | acceptance_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | impulse_reversal_control | 28 | 19 | 11 | 11 | 10 | 5 | 7 | 2803.43 | 25.6896 | 1 | 0 | 1 | 0 |
| P362_D120_I2p5_D0p25_R0p0_CONTINUATION | impulse_continuation | 28 | 19 | 11 | 11 | 3 | 2 | 3 | -10209.1 | -93.5524 | 0 | 0 | 1 | 0 |

## Interpretation

| interpretation_id | value | evidence | decision |
| --- | --- | --- | --- |
| expanded_retest_executed | 1 | event_rows=233; scenario_rows=2 | Frozen expanded real-L2 retest executed. |
| primary_acceptance_candidate | 0 | ann=25.68958992557929; selected_trades=19; breadth=1 | Primary passes acceptance gates only if annualized return, event floor and breadth all pass. |
| side_flip_control_not_better | 1 | primary_ann=25.68958992557929; side_flip_ann=-93.55244161582728 | Primary reversal should dominate same-filter continuation control. |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P381_PHASE380_PRECOMMIT_PRESENT | 1 | Phase380 precommit complete |
| P381_NO_MISSING_LOCAL_L2_DATES | 1 | missing_rows=0 |
| P381_FROZEN_GRID_ONLY | 1 | P362_D120_I2p5_D0p25_R0p0 |
| P381_EVENT_FEATURES_READY | 1 | ready_rows=233 |
| P381_FULL_DEPTH_COST200_RETAINED | 1 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| P381_ACCEPTANCE_GATE_EVALUATED | 1 | ann>12.0; events>=30; breadth |
| P381_NO_PARAMETER_SEARCH | 1 | single frozen grid row plus side-flip control |
| P381_NO_PAPER_LIVE_OR_DEPLOYABLE_CLAIM | 1 | closed |

No paper/live acceptance or deployable profitability claim is opened.

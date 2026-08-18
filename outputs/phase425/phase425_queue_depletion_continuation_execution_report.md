# Phase425 Queue-Depletion Continuation Execution

Phase425 executes the Phase424 frozen queue-depletion continuation thesis with exact post-entry tick indexing.

No take-profit or stop bps threshold is introduced here because Phase424 did not freeze one; exits use the earliest tick satisfying the exact forward-tick and 250 ms hold rules inside the frozen max-hold window.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase425_queue_depletion_continuation_execution_complete | 1 | Phase425 execution completed |
| phase425_primary_scenario_id | P425_PRIMARY_QUEUE_DEPLETION_CONTINUATION | Primary frozen scenario |
| phase425_synthetic_scenario_rows | 3 | Synthetic scenario rows |
| phase425_real_anchor_scenario_rows | 3 | Real-anchor scenario rows |
| phase425_primary_completed_round_trips | 0 | Primary round trips |
| phase425_primary_trade_dates | 0 | Primary trade dates |
| phase425_primary_symbols | 0 | Primary symbols |
| phase425_primary_positive_date_fraction | 0 | Primary positive date fraction |
| phase425_primary_net_pnl_inr | 0 | Primary net P&L |
| phase425_primary_annualized_return_pct | 0 | Primary annualized return |
| phase425_l1_only_annualized_return_pct | 0 | L1-only control annualized return |
| phase425_l2_l5_edge_delta_vs_l1_only_pct | 0 | Primary minus L1-only annualized percentage points |
| phase425_cost200_acceptance_survivor_rows | 0 | Accepted synthetic scenarios |
| phase425_strategy_promotion_allowed | 0 | No promotion |
| phase425_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase425_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase425_hard_gate_pass_rows | 13 | Passed hard gates |
| phase425_hard_gate_rows | 19 | Hard gates |
| phase425_next_best_action | interpret_phase425_queue_depletion_continuation_no_paper_live | Recommended next action |

## Synthetic Scenario Summary

| panel | scenario_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | net_pnl_inr | gross_pnl_inr | cost200_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic | P425_PRIMARY_QUEUE_DEPLETION_CONTINUATION | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P425_L1_ONLY_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P425_SIDE_FLIP_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Real-Anchor Scenario Summary

| panel | scenario_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | net_pnl_inr | gross_pnl_inr | cost200_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_anchor | P425_PRIMARY_QUEUE_DEPLETION_CONTINUATION | 4 | 3 | 3 | 0 | -663.609 | -2.7 | 660.909 | -5.57431 | 0 |
| real_anchor | P425_L1_ONLY_CONTROL | 41 | 5 | 7 | 0 | -7444.78 | -701.68 | 6743.1 | -37.5217 | 0 |
| real_anchor | P425_SIDE_FLIP_CONTROL | 4 | 3 | 3 | 0 | -806.617 | -145.7 | 660.917 | -6.77558 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P425_EXECUTION_COMPLETE | True | 1 | 1 | hard |
| P425_PHASE424_PRECOMMIT_USED | True | run_phase425_queue_depletion_continuation_execution_no_paper_live | run_phase425 | hard |
| P425_TICK_ORDERED_SINGLE_NAME_REPLAY | True | timestamp_sorted_group_loop | present | hard |
| P425_EXACT_FORWARD_TICK_INDEXING | True | 3 | >=3 exact post-entry ticks | hard |
| P425_FORWARD_TIME_ENFORCED | True | 250 | >=250ms | hard |
| P425_FULL_DEPTH_L1_L5_REQUIRED | True | required_columns=L1-L5_price_quantity_orders | present | hard |
| P425_LEVELS_2_TO_5_MATERIAL | True | depletion_replenishment_order_thinning | present | hard |
| P425_L1_ONLY_CONTROL | False | 0 | >=5.0 | hard |
| P425_SIDE_FLIP_CONTROL | True | 0 | primary>=side_flip | hard |
| P425_TAKER_ONLY_EXECUTION | True | taker_entry_taker_exit | present | hard |
| P425_NO_LOOKAHEAD | True | rolling_baseline_before_signal_then_entry_next_tick | present | hard |
| P425_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P425_EVENT_FLOOR | False | 0 | >=30 | hard |
| P425_DATE_BREADTH | False | 0 | >=5 | hard |
| P425_SYMBOL_BREADTH | False | 0 | >=5 | hard |
| P425_POSITIVE_DATE_FRACTION | False | 0 | >=0.6 | hard |
| P425_ANNUALIZED_FLOOR | False | 0 | >=12.0 | hard |
| P425_REAL_ANCHOR_CROSS_CHECK | True | -5.57431 | same_sign | hard |
| P425_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: Phase425 remains no-promotion/no-paper-live unless all execution gates pass.

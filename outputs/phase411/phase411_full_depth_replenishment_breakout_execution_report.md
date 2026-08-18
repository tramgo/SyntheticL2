# Phase411 Full-Depth Replenishment Breakout Execution

Phase411 executes the Phase410 frozen taker-only replenishment-breakout thesis on bounded raw dense synthetic L1-L5 ticks and reserved real anchors.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase411_full_depth_replenishment_breakout_execution_complete | 1 | Phase411 execution completed |
| phase411_primary_scenario_id | P411_PRIMARY_REPLENISHMENT_BREAKOUT | Primary frozen scenario |
| phase411_synthetic_scenario_rows | 4 | Synthetic scenario rows |
| phase411_real_anchor_scenario_rows | 4 | Real-anchor scenario rows |
| phase411_primary_completed_round_trips | 0 | Primary round trips |
| phase411_primary_trade_dates | 0 | Primary trade dates |
| phase411_primary_symbols | 0 | Primary symbols |
| phase411_primary_positive_date_fraction | 0 | Primary positive date fraction |
| phase411_primary_net_pnl_inr | 0 | Primary net PnL |
| phase411_primary_annualized_return_pct | 0 | Primary annualized return |
| phase411_cost200_acceptance_survivor_rows | 0 | Accepted synthetic scenarios |
| phase411_strategy_promotion_allowed | 0 | No promotion |
| phase411_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase411_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase411_hard_gate_pass_rows | 15 | Passed hard gates |
| phase411_hard_gate_rows | 20 | Hard gates |
| phase411_next_best_action | interpret_phase411_failure_no_same_family_tuning | Recommended next action |

## Synthetic Scenario Summary

| panel | scenario_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | net_pnl_inr | gross_pnl_inr | cost200_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic | P411_PRIMARY_REPLENISHMENT_BREAKOUT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P411_SIDE_FLIP_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P411_LEVELS_2_TO_5_REMOVED_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P411_SPREAD_GATE_REMOVED_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Real-Anchor Scenario Summary

| panel | scenario_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | net_pnl_inr | gross_pnl_inr | cost200_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_anchor | P411_PRIMARY_REPLENISHMENT_BREAKOUT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P411_SIDE_FLIP_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P411_LEVELS_2_TO_5_REMOVED_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P411_SPREAD_GATE_REMOVED_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P411_EXECUTION_COMPLETE | True | 1 | 1 | hard |
| P411_PHASE410_ALLOWED_EXECUTION | True | run_phase411_full_depth_replenishment_breakout_execution_no_paper_live | run_phase411 | hard |
| P411_TICK_ORDERED_REPLAY | True | timestamp_sorted_group_loop | present | hard |
| P411_STATEFUL_SEQUENCE | True | impulse->rebuild->breakout | present | hard |
| P411_TAKER_ONLY_EXECUTION | True | taker_entry_taker_exit | present | hard |
| P411_FULL_DEPTH_L1_L5 | True | required_columns=L1-L5 | present | hard |
| P411_LEVELS_2_TO_5_MATERIAL | True | l2_l5_replenishment_and_imbalance_required | present | hard |
| P411_NO_LOOKAHEAD | True | features_before_entry_tick | present | hard |
| P411_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P411_FIXED_PARAMETERS | True | phase410_parameter_freeze | present | hard |
| P411_EVENT_FLOOR | False | 0 | >=30 | hard |
| P411_DATE_BREADTH | False | 0 | >=5 | hard |
| P411_SYMBOL_BREADTH | False | 0 | >=3 | hard |
| P411_POSITIVE_DATE_FRACTION | False | 0 | >=0.6 | hard |
| P411_ANNUALIZED_FLOOR | False | 0 | >=12.0 | hard |
| P411_SIDE_FLIP_CONTROL | True | 0 | primary>=side_flip | hard |
| P411_L2_L5_REMOVED_CONTROL | True | 0 | primary>=l2_removed | hard |
| P411_SPREAD_GATE_REMOVED_CONTROL | True | 1 | 1 | hard |
| P411_REAL_ANCHOR_CROSS_CHECK | True | 0 | same_sign | hard |
| P411_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: Phase411 is a synthetic/real-anchor backtest artifact only. It is not paper/live acceptance or a deployable profitability claim.

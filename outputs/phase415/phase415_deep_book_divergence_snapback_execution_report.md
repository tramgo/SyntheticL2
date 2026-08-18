# Phase415 Deep-Book Divergence Snapback Execution

Phase415 executes the Phase414 frozen taker-only deep-book divergence snapback thesis.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase415_deep_book_divergence_snapback_execution_complete | 1 | Phase415 execution completed |
| phase415_primary_scenario_id | P415_PRIMARY_DEEP_BOOK_DIVERGENCE_SNAPBACK | Primary frozen scenario |
| phase415_synthetic_scenario_rows | 4 | Synthetic scenario rows |
| phase415_real_anchor_scenario_rows | 4 | Real-anchor scenario rows |
| phase415_primary_completed_round_trips | 238 | Primary round trips |
| phase415_primary_trade_dates | 5 | Primary trade dates |
| phase415_primary_symbols | 3 | Primary symbols |
| phase415_primary_positive_date_fraction | 0 | Primary positive date fraction |
| phase415_primary_net_pnl_inr | -83261.8 | Primary net PnL |
| phase415_primary_annualized_return_pct | -419.639 | Primary annualized return |
| phase415_cost200_acceptance_survivor_rows | 0 | Accepted synthetic scenarios |
| phase415_strategy_promotion_allowed | 0 | No promotion |
| phase415_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase415_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase415_hard_gate_pass_rows | 18 | Passed hard gates |
| phase415_hard_gate_rows | 21 | Hard gates |
| phase415_next_best_action | interpret_phase415_failure_or_success_no_paper_live | Recommended next action |

## Synthetic Scenario Summary

| panel | scenario_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | net_pnl_inr | gross_pnl_inr | cost200_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic | P415_PRIMARY_DEEP_BOOK_DIVERGENCE_SNAPBACK | 238 | 5 | 3 | 0 | -83261.8 | -43928.5 | 39333.3 | -419.639 | 0 |
| synthetic | P415_SIDE_FLIP_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P415_LEVELS_2_TO_5_REMOVED_CONTROL | 244 | 5 | 4 | 0 | -85062.2 | -44737.7 | 40324.6 | -428.714 | 0 |
| synthetic | P415_TOP5_ONLY_CONTROL | 238 | 5 | 3 | 0 | -83261.8 | -43928.5 | 39333.3 | -419.639 | 0 |

## Real-Anchor Scenario Summary

| panel | scenario_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | net_pnl_inr | gross_pnl_inr | cost200_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_anchor | P415_PRIMARY_DEEP_BOOK_DIVERGENCE_SNAPBACK | 2 | 1 | 1 | 0 | -73520.4 | -73162.1 | 358.378 | -1852.71 | 0 |
| real_anchor | P415_SIDE_FLIP_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P415_LEVELS_2_TO_5_REMOVED_CONTROL | 2 | 1 | 1 | 0 | -73520.4 | -73162.1 | 358.378 | -1852.71 | 0 |
| real_anchor | P415_TOP5_ONLY_CONTROL | 2 | 1 | 1 | 0 | -73520.4 | -73162.1 | 358.378 | -1852.71 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P415_EXECUTION_COMPLETE | True | 1 | 1 | hard |
| P415_PHASE414_ALLOWED_EXECUTION | True | run_phase415_deep_book_divergence_snapback_execution_no_paper_live | run_phase415 | hard |
| P415_TICK_ORDERED_REPLAY | True | timestamp_sorted_group_loop | present | hard |
| P415_DEEP_BOOK_DIVERGENCE_SIGNAL | True | opposing_l2_l5_depth_pressure | present | hard |
| P415_NOT_PHASE410_THRESHOLD_RELAXATION | True | new_signal_shape | present | hard |
| P415_TAKER_ONLY_EXECUTION | True | taker_entry_taker_exit | present | hard |
| P415_FULL_DEPTH_L1_L5 | True | required_columns=L1-L5 | present | hard |
| P415_LEVELS_2_TO_5_MATERIAL | True | l2_l5_imbalance_required | present | hard |
| P415_NO_LOOKAHEAD | True | features_before_entry_tick | present | hard |
| P415_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P415_FIXED_PARAMETERS | True | phase414_parameter_freeze | present | hard |
| P415_EVENT_FLOOR | True | 238 | >=30 | hard |
| P415_DATE_BREADTH | True | 5 | >=5 | hard |
| P415_SYMBOL_BREADTH | True | 3 | >=3 | hard |
| P415_POSITIVE_DATE_FRACTION | False | 0 | >=0.6 | hard |
| P415_ANNUALIZED_FLOOR | False | -419.639 | >=12.0 | hard |
| P415_SIDE_FLIP_CONTROL | False | 0 | primary>=side_flip | hard |
| P415_L2_L5_REMOVED_CONTROL | True | -428.714 | primary>=l2_removed | hard |
| P415_TOP5_ONLY_CONTROL | True | -419.639 | primary>=top5_only | hard |
| P415_REAL_ANCHOR_CROSS_CHECK | True | -1852.71 | same_sign | hard |
| P415_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: no paper/live acceptance or deployable profitability claim is opened by Phase415.

# Phase422 Pair-Spread Realism Retest Execution

Phase422 executes the Phase421 repair retest with minimum forward-time filtering, full-depth unique-gate evaluation and real-anchor pair replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase422_pair_spread_realism_retest_execution_complete | 1 | Phase422 execution completed |
| phase422_primary_scenario_id | P422_PRIMARY_PAIR_SPREAD_REALISM_RETEST | Primary scenario |
| phase422_synthetic_scenario_rows | 4 | Synthetic scenario rows |
| phase422_real_anchor_scenario_rows | 4 | Real-anchor scenario rows |
| phase422_primary_completed_round_trips | 0 | Primary pair round trips |
| phase422_primary_trade_dates | 0 | Primary trade dates |
| phase422_primary_pairs | 0 | Primary pairs |
| phase422_primary_positive_date_fraction | 0 | Primary positive date fraction |
| phase422_primary_net_pnl_inr | 0 | Primary net P&L |
| phase422_primary_annualized_return_pct | 0 | Primary annualized return |
| phase422_l2_l5_edge_delta_vs_removed_pct | 0 | Primary minus L2-L5 removed annualized percentage points |
| phase422_cost200_acceptance_survivor_rows | 0 | Accepted synthetic scenarios |
| phase422_strategy_promotion_allowed | 0 | No promotion |
| phase422_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase422_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase422_hard_gate_pass_rows | 10 | Passed hard gates |
| phase422_hard_gate_rows | 17 | Hard gates |
| phase422_next_best_action | interpret_phase422_pair_spread_realism_retest_no_paper_live | Recommended next action |

## Synthetic Scenario Summary

| panel | scenario_id | completed_round_trips | trade_dates | pairs | positive_date_fraction | net_pnl_inr | gross_pnl_inr | cost200_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic | P422_PRIMARY_PAIR_SPREAD_REALISM_RETEST | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P422_SIDE_FLIP_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P422_L2_L5_REMOVED_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| synthetic | P422_SINGLE_LEG_PROXY_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Real-Anchor Scenario Summary

| panel | scenario_id | completed_round_trips | trade_dates | pairs | positive_date_fraction | net_pnl_inr | gross_pnl_inr | cost200_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_anchor | P422_PRIMARY_PAIR_SPREAD_REALISM_RETEST | 139 | 5 | 4 | 0 | -31111.8 | -2088.1 | 29023.7 | -156.803 | 0 |
| real_anchor | P422_SIDE_FLIP_CONTROL | 110 | 5 | 4 | 0 | -24649.4 | -1682.26 | 22967.1 | -124.233 | 0 |
| real_anchor | P422_L2_L5_REMOVED_CONTROL | 205 | 5 | 4 | 0 | -46027.3 | -3218.84 | 42808.4 | -231.977 | 0 |
| real_anchor | P422_SINGLE_LEG_PROXY_CONTROL | 139 | 5 | 4 | 0 | -15555.9 | -1044.05 | 29023.7 | -78.4017 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P422_EXECUTION_COMPLETE | True | 1 | 1 | hard |
| P422_PHASE421_PRECOMMIT_USED | True | run_phase422_pair_spread_realism_retest_execution_no_paper_live | run_phase422 | hard |
| P422_FORWARD_TIME_ENFORCED | True | 250 | >=250ms | hard |
| P422_FORWARD_TICKS_ENFORCED | False | elapsed_time_proxy_only; configured_min_ticks=3 | >=3 exact post-entry aligned ticks | hard |
| P422_FULL_DEPTH_UNIQUE_GATE | False | 0 | >=5.0 | hard |
| P422_REAL_ANCHOR_PAIR_PANEL_USED | True | 5 | >=1 | hard |
| P422_PAIR_MARKET_NEUTRAL | True | equal_notional_long_short | present | hard |
| P422_TAKER_ONLY | True | taker_both_legs | present | hard |
| P422_NO_LOOKAHEAD | True | rolling_before_entry | present | hard |
| P422_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0 | cost200_fixed_capital | hard |
| P422_EVENT_FLOOR | False | 0 | >=30 | hard |
| P422_DATE_BREADTH | False | 0 | >=5 | hard |
| P422_PAIR_BREADTH | False | 0 | >=2 | hard |
| P422_POSITIVE_DATE_FRACTION | False | 0 | >=0.6 | hard |
| P422_ANNUALIZED_FLOOR | False | 0 | >=12.0 | hard |
| P422_REAL_ANCHOR_SIGN | True | -156.803 | same_sign | hard |
| P422_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: Phase422 remains no-promotion/no-paper-live unless all repair gates pass.

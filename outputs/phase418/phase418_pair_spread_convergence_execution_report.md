# Phase418 Pair-Spread Convergence Execution

Phase418 executes the Phase417 frozen market-neutral full-depth pair-spread convergence thesis.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase418_pair_spread_convergence_execution_complete | 1 | Phase418 execution completed |
| phase418_primary_scenario_id | P418_PRIMARY_PAIR_SPREAD_CONVERGENCE | Primary scenario |
| phase418_synthetic_scenario_rows | 4 | Synthetic scenario rows |
| phase418_real_anchor_scenario_rows | 4 | Real-anchor scenario rows |
| phase418_primary_completed_round_trips | 189 | Primary pair round trips |
| phase418_primary_trade_dates | 5 | Primary trade dates |
| phase418_primary_pairs | 4 | Primary pairs |
| phase418_primary_positive_date_fraction | 0.8 | Primary positive date fraction |
| phase418_primary_net_pnl_inr | 15352.1 | Primary net P&L |
| phase418_primary_annualized_return_pct | 77.3748 | Primary annualized return |
| phase418_cost200_acceptance_survivor_rows | 3 | Accepted scenarios |
| phase418_strategy_promotion_allowed | 0 | No promotion |
| phase418_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase418_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase418_hard_gate_pass_rows | 20 | Passed hard gates |
| phase418_hard_gate_rows | 21 | Hard gates |
| phase418_next_best_action | interpret_phase418_pair_spread_convergence_no_paper_live | Recommended next action |

## Synthetic Scenario Summary

| panel | scenario_id | completed_round_trips | trade_dates | pairs | positive_date_fraction | net_pnl_inr | gross_pnl_inr | cost200_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic | P418_PRIMARY_PAIR_SPREAD_CONVERGENCE | 189 | 5 | 4 | 0.8 | 15352.1 | 54679.2 | 39327.1 | 77.3748 | 1 |
| synthetic | P418_SIDE_FLIP_CONTROL | 189 | 5 | 4 | 0 | -103163 | -63830.5 | 39332.1 | -519.939 | 0 |
| synthetic | P418_L2_L5_REMOVED_CONTROL | 240 | 5 | 4 | 0.8 | 19486.5 | 69496.2 | 50009.7 | 98.212 | 1 |
| synthetic | P418_SINGLE_LEG_PROXY_CONTROL | 189 | 5 | 4 | 0.8 | 7676.07 | 27339.6 | 39327.1 | 38.6874 | 1 |

## Real-Anchor Scenario Summary

| panel | scenario_id | completed_round_trips | trade_dates | pairs | positive_date_fraction | net_pnl_inr | gross_pnl_inr | cost200_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_anchor | P418_PRIMARY_PAIR_SPREAD_CONVERGENCE | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P418_SIDE_FLIP_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P418_L2_L5_REMOVED_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | P418_SINGLE_LEG_PROXY_CONTROL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P418_EXECUTION_COMPLETE | True | 1 | 1 | hard |
| P418_PHASE417_ALLOWED_EXECUTION | True | run_phase418_pair_spread_convergence_execution_no_paper_live | run_phase418 | hard |
| P418_TICK_ORDERED_PAIR_ALIGNMENT | True | merge_asof_no_lookahead_features | present | hard |
| P418_MARKET_NEUTRAL_PAIR_EXPOSURE | True | leg_notional=50000.0 | equal_notional | hard |
| P418_TAKER_ONLY_EXECUTION | True | taker_both_legs | present | hard |
| P418_FULL_DEPTH_L1_L5_BOTH_LEGS | True | required_columns_both_legs | present | hard |
| P418_LEVELS_2_TO_5_MATERIAL | True | l2_l5_liquidity_and_conflict_gate | present | hard |
| P418_NO_LOOKAHEAD | True | rolling_before_entry | present | hard |
| P418_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P418_FIXED_PARAMETERS | True | phase417_parameter_freeze | present | hard |
| P418_EVENT_FLOOR | True | 189 | >=30 | hard |
| P418_DATE_BREADTH | True | 5 | >=5 | hard |
| P418_PAIR_BREADTH | True | 4 | >=2 | hard |
| P418_POSITIVE_DATE_FRACTION | True | 0.8 | >=0.6 | hard |
| P418_ANNUALIZED_FLOOR | True | 77.3748 | >=12.0 | hard |
| P418_SIDE_FLIP_CONTROL | True | -519.939 | primary>=side_flip | hard |
| P418_L2_L5_REMOVED_CONTROL | False | 98.212 | primary>=l2_removed | hard |
| P418_SINGLE_LEG_PROXY_CONTROL | True | 38.6874 | primary>=single_leg_proxy | hard |
| P418_COST100_RANK_STABILITY | True | cost100_recorded | reported | hard |
| P418_REAL_ANCHOR_CROSS_CHECK | True | 0 | same_sign | hard |
| P418_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: Phase418 is not paper/live acceptance or a deployable profitability claim.

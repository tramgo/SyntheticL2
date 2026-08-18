# Phase441 External Catalyst Full-Depth Confirmation Execution

Phase441 executes the Phase440 external-catalyst plus full-depth confirmation source using local Phase387 event-feature evidence.

The execution is bounded by the Phase387 feature ledger's fixed event horizon; it does not claim fresh raw-horizon recomputation.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase441_external_catalyst_full_depth_complete | 1 | Phase441 execution completed |
| phase441_thesis_id | P441_EXTERNAL_CATALYST_FULL_DEPTH_CONFIRMATION_EXECUTION | Execution thesis |
| phase441_source_event_rows | 246 | Phase387 ready event rows available |
| phase441_best_scenario_id | P441_catalyst_reversal_H600_exhaustion_C3 | Best active scenario |
| phase441_best_completed_round_trips | 33 | Best round trips |
| phase441_best_trade_dates | 12 | Best dates |
| phase441_best_symbols | 19 | Best symbols |
| phase441_best_positive_date_fraction | 0.0833333 | Best positive-date fraction |
| phase441_best_gross_pnl_inr | -6535.74 | Best gross P&L |
| phase441_best_cost200_inr | 5443.85 | Best cost200 charges |
| phase441_best_net_pnl_inr | -11979.6 | Best net P&L |
| phase441_best_annualized_return_pct | -25.1571 | Best annualized return |
| phase441_cost200_acceptance_survivor_rows | 0 | Accepted scenario rows before controls |
| phase441_strategy_promotion_allowed | 0 | No promotion |
| phase441_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase441_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase441_hard_gate_pass_rows | 9 | Passed hard gates |
| phase441_hard_gate_rows | 14 | Hard gates |
| phase441_next_best_action | interpret_phase441_external_catalyst_full_depth_confirmation_no_paper_live | Recommended next action |

## Scenario Summary

| panel | scenario_id | family_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | gross_pnl_inr | cost200_inr | net_pnl_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| external_catalyst_full_depth | P441_catalyst_reversal_H600_exhaustion_C3 | official_catalyst_reversal | 33 | 12 | 19 | 0.0833333 | -6535.74 | 5443.85 | -11979.6 | -25.1571 | 0 |
| external_catalyst_full_depth | P441_catalyst_reversal_H1200_exhaustion_C3 | official_catalyst_reversal | 33 | 12 | 19 | 0.0833333 | -6535.74 | 5443.85 | -11979.6 | -25.1571 | 0 |
| external_catalyst_full_depth | P441_catalyst_reversal_H2400_exhaustion_C3 | official_catalyst_reversal | 33 | 12 | 19 | 0.0833333 | -6535.74 | 5443.85 | -11979.6 | -25.1571 | 0 |
| external_catalyst_full_depth | P441_catalyst_reversal_H600_replenishment_after_exhaustion_C3 | official_catalyst_reversal | 31 | 11 | 17 | 0.0909091 | -7673.24 | 5114.6 | -12787.8 | -29.2958 | 0 |
| external_catalyst_full_depth | P441_catalyst_reversal_H2400_replenishment_after_exhaustion_C3 | official_catalyst_reversal | 31 | 11 | 17 | 0.0909091 | -7673.24 | 5114.6 | -12787.8 | -29.2958 | 0 |
| external_catalyst_full_depth | P441_catalyst_reversal_H1200_replenishment_after_exhaustion_C3 | official_catalyst_reversal | 31 | 11 | 17 | 0.0909091 | -7673.24 | 5114.6 | -12787.8 | -29.2958 | 0 |
| external_catalyst_full_depth | P441_catalyst_reversal_H2400_replenishment_after_exhaustion_C5 | official_catalyst_reversal | 46 | 11 | 20 | 0.0909091 | -11754 | 7584.83 | -19338.8 | -44.3035 | 0 |
| external_catalyst_full_depth | P441_catalyst_reversal_H600_replenishment_after_exhaustion_C5 | official_catalyst_reversal | 46 | 11 | 20 | 0.0909091 | -11754 | 7584.83 | -19338.8 | -44.3035 | 0 |
| external_catalyst_full_depth | P441_catalyst_reversal_H1200_replenishment_after_exhaustion_C5 | official_catalyst_reversal | 46 | 11 | 20 | 0.0909091 | -11754 | 7584.83 | -19338.8 | -44.3035 | 0 |
| external_catalyst_full_depth | P441_catalyst_reversal_H600_exhaustion_C5 | official_catalyst_reversal | 53 | 12 | 22 | 0.0833333 | -13342.2 | 8740.4 | -22082.6 | -46.3734 | 0 |
| external_catalyst_full_depth | P441_catalyst_reversal_H1200_exhaustion_C5 | official_catalyst_reversal | 53 | 12 | 22 | 0.0833333 | -13342.2 | 8740.4 | -22082.6 | -46.3734 | 0 |
| external_catalyst_full_depth | P441_catalyst_reversal_H2400_exhaustion_C5 | official_catalyst_reversal | 53 | 12 | 22 | 0.0833333 | -13342.2 | 8740.4 | -22082.6 | -46.3734 | 0 |

## Controls For Best Scenario

| control | panel | scenario_id | family_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | gross_pnl_inr | cost200_inr | net_pnl_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| l1_only | l1_only_ablation | P441_catalyst_reversal_H600_exhaustion_C3 | official_catalyst_reversal | 34 | 12 | 21 | 0.166667 | -1341.02 | 5601.33 | -6942.35 | -14.5789 | 0 |
| side_flip | side_flip | P441_catalyst_reversal_H600_exhaustion_C3 | official_catalyst_reversal | 33 | 12 | 19 | 0.333333 | 4573.37 | 5443.42 | -870.048 | -1.8271 | 0 |
| time_shifted_catalyst | time_shifted_catalyst | P441_catalyst_reversal_H600_exhaustion_C3 | official_catalyst_reversal | 39 | 13 | 17 | 0.153846 | -4683.53 | 6423.75 | -11107.3 | -21.531 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P441_PHASE440_PRECOMMIT_USED | True | run_phase441_external_catalyst_full_depth_confirmation_no_paper_live | phase440_next_action | hard |
| P441_SOURCE_EVENT_FLOOR_AVAILABLE | True | 246 | >=30 | hard |
| P441_FULL_DEPTH_CONFIRMATION_USED | True | P441_catalyst_reversal_H600_exhaustion_C3 | l2_l5_confirmation | hard |
| P441_HORIZON_RECOMPUTE_LIMITATION_RECORDED | True | phase387_feature_ledger_fixed_horizon_seconds | recorded | hard |
| P441_L1_ONLY_CONTROL | False | -10.5782 | >=5 pct pts | hard |
| P441_SIDE_FLIP_CONTROL_NOT_DOMINANT | False | -1.8271 | primary>=side_flip | hard |
| P441_TIME_SHIFT_CONTROL_NOT_DOMINANT | False | -21.531 | primary>=time_shift | hard |
| P441_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P441_EVENT_FLOOR | True | 33 | >=30 | hard |
| P441_DATE_BREADTH | True | 12 | >=5 | hard |
| P441_SYMBOL_BREADTH | True | 19 | >=5 | hard |
| P441_POSITIVE_DATE_FRACTION | False | 0.0833333 | >=0.6 | hard |
| P441_ANNUALIZED_FLOOR | False | -25.1571 | >=12.0 | hard |
| P441_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: no strategy promotion, paper/live acceptance or deployable profitability claim is generated by Phase441.

# Phase405 Liquidity-Vacuum Continuation Execution

Phase405 executes the Phase404 fixed-threshold material-new full-depth L2 thesis.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase405_liquidity_vacuum_continuation_execution_complete | 1 | Phase405 execution completed |
| phase405_thesis_id | P404_CATALYST_LIQUIDITY_VACUUM_CONTINUATION_FULL_DEPTH | Executed thesis |
| phase405_event_feature_rows | 273 | Input event feature rows |
| phase405_ready_event_feature_rows | 270 | Ready rows |
| phase405_primary_raw_candidate_rows | 75 | Primary raw candidate rows |
| phase405_primary_capacity_selected_trade_rows | 28 | Primary selected trades |
| phase405_primary_diagnostic_dates | 16 | Primary diagnostic dates |
| phase405_primary_symbols | 14 | Primary symbols |
| phase405_primary_positive_symbols | 4 | Primary positive symbols |
| phase405_primary_net_pnl_inr | -11542.9 | Primary net PnL |
| phase405_primary_annualized_return_pct | -72.7204 | Primary annualized return |
| phase405_primary_above12 | 0 | Primary above 12% |
| phase405_primary_event_floor_met | 0 | Primary event floor |
| phase405_primary_breadth_met | 1 | Primary breadth |
| phase405_primary_acceptance_candidate | 0 | Primary acceptance |
| phase405_side_flip_annualized_return_pct | 5.12294 | Side-flip annualized return |
| phase405_depth_removed_annualized_return_pct | -71.1864 | Depth-removed control annualized return |
| phase405_strategy_promotion_allowed | 0 | No promotion |
| phase405_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase405_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase405_hard_gate_pass_rows | 6 | Passed hard gates |
| phase405_hard_gate_rows | 6 | Hard gates |
| phase405_next_best_action | interpret_phase405_liquidity_vacuum_continuation_no_paper_live | Recommended next action |

## Scenario Summary

| scenario_id | scenario_role | raw_candidate_rows | capacity_selected_trade_rows | diagnostic_dates | symbols | positive_symbols | positive_symbol_date_cells | net_pnl_inr | annualized_return_pct | above12 | event_floor_met | breadth_met | acceptance_candidate | avg_impulse_bps | avg_replenishment_ratio | avg_l2_l5_abs_imbalance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P405_LIQUIDITY_VACUUM_CONTINUATION_FULL_DEPTH | liquidity_vacuum_continuation | 75 | 28 | 16 | 14 | 4 | 5 | -11542.9 | -72.7204 | 0 | 0 | 1 | 0 | 32.3633 | -0.263548 | 0.407817 |
| P405_CONTROL_SIDE_FLIP | side_flip_control | 75 | 28 | 16 | 14 | 5 | 9 | 813.164 | 5.12294 | 0 | 0 | 1 | 0 | 32.3633 | -0.263548 | 0.407817 |
| P405_CONTROL_TOP5_ONLY_DEPTH_REMOVED | top5_only_depth_removed_control | 78 | 29 | 16 | 14 | 4 | 6 | -11299.4 | -71.1864 | 0 | 0 | 1 | 0 | 30.6777 | -0.285607 | 0.396241 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P405_PHASE404_PRECOMMIT_PRESENT | True | 1 | 1 | hard |
| P405_PRIMARY_SCENARIO_PRESENT | True | 1 | 1 | hard |
| P405_FULL_DEPTH_FILTER_APPLIED | True | top5_and_l2_l5_alignment | applied | hard |
| P405_CONTROLS_LOGGED | True | P405_LIQUIDITY_VACUUM_CONTINUATION_FULL_DEPTH;P405_CONTROL_SIDE_FLIP;P405_CONTROL_TOP5_ONLY_DEPTH_REMOVED | side_flip;depth_removed | hard |
| P405_COST200_FIXED_CAPITAL | True | cost=2.0;capital=250000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P405_NO_PROMOTION_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

No promotion, paper/live acceptance, deployable profitability claim, or parameter search is opened.

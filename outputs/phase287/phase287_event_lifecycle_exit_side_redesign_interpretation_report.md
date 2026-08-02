# Phase287 Event Lifecycle / Side / Exit Redesign Interpretation

Phase287 interprets the Phase286 lifecycle search as a no-survivor checkpoint and selects the next direct full-depth L2 liquidity-pressure strategy search.

This milestone does not open replay, promotion, paper/live acceptance, or a deployable profitability claim.

## Phase286 Summary

- variants: `60`
- scenarios: `720`
- sparse above-12 scenarios: `0`
- robust portfolio above-12 scenarios: `0`
- best annualized fixed-capital diagnostic: `3.462593252169461`
- best scheduled events: `4`
- best variant: `P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_E2_H8`

## Ranked Lifecycle Interpretation

| phase286_variant_id | lifecycle_family | grid_id | scenario_rows | selected_event_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_scenario_id | best_initial_capital_inr | best_fixed_notional_inr | best_max_concurrent_positions | best_notional_turnover_x_initial_capital | best_avg_open_notional_utilization | rejected_same_symbol_overlap_rows | rejected_max_concurrent_rows | uses_top5 | uses_levels_2_to_5 | l1_only_variant | uses_net_edge_as_live_mask | positive_but_below12 | too_sparse_for_sparse_diagnostic | too_sparse_for_portfolio_claim | full_depth_positive_clue | same_lifecycle_route_exhausted_for_acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_E2_H8 | queue_adversity_order_timing_test | P285_GRID_ORIG_E2_H8 | 12 | 234 | 8 | 0 | 0 | 4 | 0 | 0.0572797 | 1.86049 | 3.46259 | 109.924 | P271_P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_E2_H8_CAP100000_NOT75000_CONC2_COST200 | 100000 | 75000 | 2 | 2 | 0.982906 | 44 | 216 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 |
| P286_P285_ENTRY_DELAY_TEST_P285_GRID_ORIG_E2_H8 | entry_delay_test | P285_GRID_ORIG_E2_H8 | 12 | 861 | 7 | 0 | 0 | 0 | 0 | -4.0411 | -2.11328 | 1.63379 | 51.8663 | P271_P286_P285_ENTRY_DELAY_TEST_P285_GRID_ORIG_E2_H8_CAP100000_NOT75000_CONC2_COST200 | 100000 | 75000 | 2 | 2.5 | 0.981998 | 85 | 805 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_E0_H5 | queue_adversity_order_timing_test | P285_GRID_ORIG_E0_H5 | 12 | 234 | 12 | 0 | 0 | 4 | 0 | -0.868389 | 0.295672 | 0.631139 | 20.0362 | P271_P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_E0_H5_CAP100000_NOT75000_CONC2_COST200 | 100000 | 75000 | 2 | 3 | 0.982906 | 41 | 227 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 |
| P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_E1_H5 | queue_adversity_order_timing_test | P285_GRID_ORIG_E1_H5 | 12 | 234 | 12 | 0 | 0 | 4 | 0 | -1.85852 | -0.500661 | -0.165874 | -5.26584 | P271_P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_E1_H5_CAP100000_NOT25000_CONC2_COST200 | 100000 | 25000 | 2 | 1.5 | 0.491453 | 41 | 227 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| P286_P285_SIDE_FLIP_REVERSAL_TEST_P285_GRID_ORIG_E0_H5 | side_flip_reversal_test | P285_GRID_ORIG_E0_H5 | 12 | 640 | 11 | 0 | 0 | 8 | 0 | -14.8772 | -2.67073 | -0.166874 | -5.29757 | P271_P286_P285_SIDE_FLIP_REVERSAL_TEST_P285_GRID_ORIG_E0_H5_CAP100000_NOT25000_CONC2_COST200 | 100000 | 25000 | 2 | 2 | 0.489844 | 76 | 591 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| P286_P285_TAKE_PROFIT_STOP_TIMEOUT_TEST_P285_GRID_ORIG_E0_H5 | take_profit_stop_timeout_test | P285_GRID_ORIG_E0_H5 | 12 | 598 | 16 | 0 | 0 | 8 | 0 | -8.92514 | -5.92105 | -0.378657 | -12.0209 | P271_P286_P285_TAKE_PROFIT_STOP_TIMEOUT_TEST_P285_GRID_ORIG_E0_H5_CAP100000_NOT25000_CONC1_COST200 | 100000 | 25000 | 1 | 1 | 0.248328 | 108 | 563 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| P286_P285_ENTRY_DELAY_TEST_P285_GRID_ORIG_E0_H5 | entry_delay_test | P285_GRID_ORIG_E0_H5 | 12 | 861 | 14 | 0 | 0 | 8 | 0 | -2.4803 | -2.08539 | -0.474776 | -15.0722 | P271_P286_P285_ENTRY_DELAY_TEST_P285_GRID_ORIG_E0_H5_CAP100000_NOT25000_CONC1_COST200 | 100000 | 25000 | 1 | 1 | 0.248839 | 150 | 805 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| P286_P285_TAKE_PROFIT_STOP_TIMEOUT_TEST_P285_GRID_ORIG_E1_H5 | take_profit_stop_timeout_test | P285_GRID_ORIG_E1_H5 | 12 | 598 | 16 | 0 | 0 | 8 | 0 | -10.9231 | -7.24633 | -0.773686 | -24.5615 | P271_P286_P285_TAKE_PROFIT_STOP_TIMEOUT_TEST_P285_GRID_ORIG_E1_H5_CAP100000_NOT25000_CONC1_COST200 | 100000 | 25000 | 1 | 1 | 0.248328 | 108 | 563 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| P286_P285_ENTRY_DELAY_TEST_P285_GRID_ORIG_E1_H5 | entry_delay_test | P285_GRID_ORIG_E1_H5 | 12 | 861 | 14 | 0 | 0 | 8 | 0 | -3.58505 | -3.32458 | -0.896262 | -28.4528 | P271_P286_P285_ENTRY_DELAY_TEST_P285_GRID_ORIG_E1_H5_CAP100000_NOT25000_CONC1_COST200 | 100000 | 25000 | 1 | 1 | 0.248839 | 150 | 805 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| P286_P285_SIDE_FLIP_REVERSAL_TEST_P285_GRID_ORIG_E1_H5 | side_flip_reversal_test | P285_GRID_ORIG_E1_H5 | 12 | 640 | 11 | 0 | 0 | 8 | 0 | -16.7297 | -3.50655 | -0.900643 | -28.5918 | P271_P286_P285_SIDE_FLIP_REVERSAL_TEST_P285_GRID_ORIG_E1_H5_CAP100000_NOT25000_CONC2_COST200 | 100000 | 25000 | 2 | 2 | 0.489844 | 76 | 591 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| P286_P285_TAKE_PROFIT_STOP_TIMEOUT_TEST_P285_GRID_ORIG_E2_H8 | take_profit_stop_timeout_test | P285_GRID_ORIG_E2_H8 | 12 | 598 | 7 | 0 | 0 | 0 | 0 | -11.4523 | -2.18604 | -1.09302 | -34.699 | P271_P286_P285_TAKE_PROFIT_STOP_TIMEOUT_TEST_P285_GRID_ORIG_E2_H8_CAP100000_NOT25000_CONC2_COST200 | 100000 | 25000 | 2 | 1.25 | 0.496237 | 58 | 575 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 |
| P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_TP8_SL4_H10 | queue_adversity_order_timing_test | P285_GRID_ORIG_TP8_SL4_H10 | 12 | 234 | 8 | 0 | 0 | 4 | 0 | -5.60746 | -5.37783 | -1.34446 | -42.6812 | P271_P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_TP8_SL4_H10_CAP100000_NOT25000_CONC1_COST200 | 100000 | 25000 | 1 | 0.5 | 0.247863 | 45 | 227 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |

## Family Interpretation

| lifecycle_family | variant_rows | scenario_rows | selected_event_rows_max | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_variant_id | positive_but_below12_variants | full_depth_positive_clue_variants | preserve_liquidity_pressure_clue | close_lifecycle_family_for_acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| queue_adversity_order_timing_test | 12 | 144 | 234 | 29 | 0 | 0 | 56 | 0 | -66.9575 | -12.3923 | 3.46259 | 109.924 | P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_E2_H8 | 2 | 2 | 1 | 1 |
| entry_delay_test | 12 | 144 | 861 | 26 | 0 | 0 | 64 | 0 | -84.5295 | -13.1367 | 1.63379 | 51.8663 | P286_P285_ENTRY_DELAY_TEST_P285_GRID_ORIG_E2_H8 | 1 | 1 | 1 | 1 |
| side_flip_reversal_test | 12 | 144 | 640 | 27 | 0 | 0 | 72 | 0 | -69.9561 | -14.3245 | -0.166874 | -5.29757 | P286_P285_SIDE_FLIP_REVERSAL_TEST_P285_GRID_ORIG_E0_H5 | 0 | 0 | 0 | 1 |
| take_profit_stop_timeout_test | 12 | 144 | 598 | 24 | 0 | 0 | 64 | 0 | -51.9379 | -13.8355 | -0.378657 | -12.0209 | P286_P285_TAKE_PROFIT_STOP_TIMEOUT_TEST_P285_GRID_ORIG_E0_H5 | 0 | 0 | 0 | 1 |
| short_horizon_exit_test | 12 | 144 | 204 | 15 | 0 | 0 | 40 | 0 | -47.0933 | -9.77108 | -1.81253 | -57.5406 | P286_P285_SHORT_HORIZON_EXIT_TEST_P285_GRID_ORIG_E0_H5 | 0 | 0 | 0 | 1 |

## Interpretation Ledger

| finding_id | evidence | severity | finding_present | interpretation |
| --- | --- | --- | --- | --- |
| phase286_executed | scenario_rows=720 | evidence | 1 | Phase286 executed the lifecycle / side / exit redesign search. |
| no_sparse_above12_survivor | sparse_above12_rows=0;best_ann=3.462593252169461 | hard_negative | 1 | No Phase286 scenario crossed the fixed-capital >12% cost200 sparse diagnostic threshold. |
| no_robust_portfolio_survivor | robust_floor_rows=0;robust_above12_rows=0;best_events=4 | hard_negative | 1 | No Phase286 scenario met robust portfolio breadth or robust above-12 evidence. |
| best_case_too_small | best_ann=3.462593252169461;best_scheduled_events=4 | risk | 1 | The best lifecycle result is both below threshold and too sparse. |
| full_depth_boundary_preserved | l1_only=0;live_label_leakage=0;positive_full_depth_clues=3 | constraint | 1 | Full top-five depth and no-live-leakage boundaries held. |
| same_lifecycle_route_should_close_for_acceptance | cost200_above12=0;robust_above12=0 | decision | 1 | Do not keep iterating lifecycle side/exit knobs as an acceptance path. |
| next_route_should_change_edge_source | P287_FULL_DEPTH_LIQUIDITY_PRESSURE_STRATEGY_SEARCH | next_action | 1 | Move to a direct full-depth L2 liquidity-pressure strategy search instead of more lifecycle wrappers around the same proxy edge. |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| close_phase286_lifecycle_route_for_acceptance | 1 | sparse_above12=0;best_ann=3.462593252169461;best_events=4 | Do not accept, replay, or promote Phase286 lifecycle variants. |
| preserve_best_full_depth_lifecycle_clue | P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_E2_H8 | family=queue_adversity_order_timing_test;grid=P285_GRID_ORIG_E2_H8;scheduled_events=4 | Carry forward only as a clue for a different full-depth edge source. |
| preserved_lifecycle_families_for_feature_context | queue_adversity_order_timing_test;entry_delay_test | positive full-depth but below-12 diagnostics | Preserve as context, not as accepted strategies. |
| do_not_relax_annualized_denominator | 1 | fixed_initial_capital_required | Annualized return remains fixed-capital based, never unlimited-capital based. |
| do_not_claim_portfolio_return | 1 | best_scheduled_events=4;sparse_floor=8;robust_floor=30 | The evidence is too sparse for a portfolio-return claim. |
| selected_next_route | P287_FULL_DEPTH_LIQUIDITY_PRESSURE_STRATEGY_SEARCH | lifecycle route exhausted; direct L2 pressure edge source required | Run a direct full-depth liquidity-pressure search. |

## Phase288 Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P288_INPUTS | outputs/phase277/phase277_cost200_redesign_event_universe.csv;outputs/phase286/phase286_lifecycle_scenario_results.csv;outputs/phase286/phase286_lifecycle_variant_summary.csv | Use the event universe plus Phase286 failure evidence. |
| P288_PRESERVED_PHASE286_CLUES | P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_E2_H8;P286_P285_ENTRY_DELAY_TEST_P285_GRID_ORIG_E2_H8;P286_P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST_P285_GRID_ORIG_E0_H5 | Carry forward positive full-depth lifecycle clues only as diagnostic context. |
| P288_PRESERVED_LIFECYCLE_FAMILIES | queue_adversity_order_timing_test;entry_delay_test | Keep the best-performing lifecycle families as context for feature families, not as acceptance candidates. |
| P288_SEARCH_TYPE | direct_full_depth_l2_liquidity_pressure_strategy_search | Search direct pressure/exhaustion/continuation edges from top-five depth instead of wrapping the old proxy edge. |
| P288_REQUIRED_FEATURE_DIRECTIONS | beyond_l1_imbalance;depth_slope;spread_state;book_churn;withdrawal;replenishment;consensus;volume_shock;market_open_bucket;reversal_vs_continuation_side | Use the full depth of the L2 data and explicitly test reversal and continuation. |
| P288_CAPITAL_AND_COST | initial_capital_100000;cost200_required;fixed_notional_grid;max_concurrent_grid;annualized_denominator_fixed_capital | No unlimited-capital annualized return. |
| P288_ACCEPTANCE_DIAGNOSTICS | cost200_annualized_pct_gt_12.0;scheduled_event_rows_ge_8_for_sparse_discovery;scheduled_event_rows_ge_30_for_portfolio_claim | Sparse >12% is discovery only; robust portfolio claim needs a larger event floor. |
| P288_BOUNDARY | no_paper_live;no_strategy_replay;no_deployable_profitability_claim;l1_only_forbidden;net_edge_live_mask_forbidden | Boundaries remain closed until the evidence earns them. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P287_PHASE286_SEARCH_COMPLETE | True | 1 | Phase286 search complete | hard |
| P287_PHASE286_NEXT_ACTION_PRESENT | True | run_phase287_event_lifecycle_exit_side_redesign_interpretation_no_paper_live | Phase286 routes to Phase287 interpretation | hard |
| P287_PHASE286_GATES_PASS | True | 8/8 | Phase286 gates pass | hard |
| P287_RANKED_INTERPRETATION_PRESENT | True | 60 | >0 ranked variants | hard |
| P287_CLOSES_PHASE286_FOR_ACCEPTANCE | True | 1 | Phase286 closed for acceptance | hard |
| P287_NEXT_ROUTE_SELECTED | True | P287_FULL_DEPTH_LIQUIDITY_PRESSURE_STRATEGY_SEARCH | P287_FULL_DEPTH_LIQUIDITY_PRESSURE_STRATEGY_SEARCH | hard |
| P287_FULL_DEPTH_BOUNDARY_PRESERVED | True | l1_only=0;live_mask=0 | full-depth, no leakage | hard |
| P287_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |
| P287_ROUTE_CONTRACT_PRESENT | True | 8 | Phase288 route contract rows | hard |

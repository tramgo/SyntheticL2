# Phase414 Deep-Book Divergence Snapback Precommit

Phase414 freezes a materially new less-sparse full-depth L2 thesis using the Phase413 failure map.

The thesis trades a short-horizon taker snapback when a price impulse is opposed by levels 2-5 depth pressure and top-five does not strongly confirm the impulse.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase414_deep_book_divergence_snapback_precommit_complete | 1 | Phase414 precommit completed |
| phase414_thesis_id | P414_DEEP_BOOK_DIVERGENCE_SNAPBACK_TAKER_ONLY | Frozen thesis |
| phase414_material_new_after_phase413 | 1 | Deep-book divergence snapback, not Phase410 threshold relaxation |
| phase414_contract_rows | 24 | Contract rows |
| phase414_parameter_freeze_rows | 11 | Frozen parameter rows |
| phase414_parameter_freeze_hash | 8694fe2341e06baaf0e1ed4cf9aa300287b405b8958a3c1cff48d795e462af2b | Hash of frozen parameter table |
| phase414_phase413_synthetic_scan_points | 840 | Phase413 attribution scan points |
| phase414_phase413_l2_l5_replenishment_pass_rate | 0.00833333 | Phase413 sparsity clue |
| phase414_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha cost model |
| phase414_cost_multiplier | 2 | Cost200 |
| phase414_initial_capital_inr | 1e+06 | Fixed capital |
| phase414_fixed_notional_inr | 100000 | Fixed notional per trade |
| phase414_execution_results_generated | 0 | Precommit only |
| phase414_strategy_promotion_allowed | 0 | No promotion |
| phase414_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase414_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase414_execution_allowed_next | 1 | Whether Phase415 may run |
| phase414_hard_gate_pass_rows | 17 | Passed hard gates |
| phase414_hard_gate_rows | 17 | Hard gates |
| phase414_next_best_action | run_phase415_deep_book_divergence_snapback_execution_no_paper_live | Recommended next action |

## Frozen Thesis Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P414_DEEP_BOOK_DIVERGENCE_SNAPBACK_TAKER_ONLY | Material-new less-sparse full-depth L2 thesis after Phase413 attribution. |
| material_difference | deep_book_divergence_snapback_not_replenishment_breakout_not_market_making_not_passive | Uses opposing deeper-book pressure, not aligned replenishment breakout or two-sided quoting. |
| phase413_basis | top5_alignment_and_l2_l5_replenishment_were_sparsity_bottlenecks | Do not require simultaneous top-five alignment and high replenishment. |
| market_hypothesis | when short_impulse_runs_against_deeper_l2_l5_pressure_and_top5_does_not_confirm_it_price_may_snap_back | Depth disagreement, not price-bar reversal alone. |
| entry_side | opposite_impulse_toward_deeper_book_pressure | Taker entry in the deep-book pressure direction. |
| execution_profile | taker_entry_taker_stop_target_or_horizon_exit | No passive fill model, no maker rebate. |
| impulse_lookback_seconds | 20 | Past-only impulse window. |
| confirm_seconds | 5 | Past-only book confirmation window. |
| horizon_seconds | 120 | Fixed exit horizon. |
| min_abs_impulse_bps | 3 | Fixed impulse threshold. |
| min_opposing_l2_l5_imbalance | 0.08 | Required levels 2-5 pressure against impulse. |
| max_top5_alignment_with_impulse | 0.08 | Top-of-book must not strongly confirm impulse. |
| min_level_weighted_divergence | 0.05 | Level-weighted pressure must support snapback side. |
| max_spread_bps | 8 | Avoid wide-spread execution. |
| max_withdrawal_pressure | 0.25 | Reject severe depth pulling. |
| stop_bps | 10 | Fixed stop. |
| take_profit_bps | 14 | Fixed target. |
| full_depth_required | L1_to_L5_book_state_with_levels_2_to_5_directional_pressure | L1-only variants forbidden. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha equity intraday NSE formula. |
| cost_multiplier | 2 | Cost200 acceptance scoring. |
| capital | initial=1000000.0;notional=100000.0;max_concurrent=2 | Fixed capital denominator. |
| acceptance | round_trips>=30;dates>=5;symbols>=3;positive_date_fraction>=0.6;annualized>=12.0 | Must be profitable with breadth. |
| controls | side_flip;levels_2_to_5_removed;top5_only;spread_gate_removed;real_anchor_sign | Controls must be reported. |
| forbidden | phase410_threshold_relaxation;market_maker_rescue;passive_fill_rescue;bar_return_reversal_alone;promotion;paper_live;deployable_claim | Closed boundaries. |

## Frozen Parameters

| parameter_id | value | status |
| --- | --- | --- |
| P414_IMPULSE_LOOKBACK_SECONDS | 20 | fixed |
| P414_CONFIRM_SECONDS | 5 | fixed |
| P414_HORIZON_SECONDS | 120 | fixed |
| P414_MIN_ABS_IMPULSE_BPS | 3 | fixed |
| P414_MIN_OPPOSING_L2_L5_IMBALANCE | 0.08 | fixed |
| P414_MAX_TOP5_ALIGNMENT_WITH_IMPULSE | 0.08 | fixed |
| P414_MIN_LEVEL_WEIGHTED_DIVERGENCE | 0.05 | fixed |
| P414_MAX_SPREAD_BPS | 8 | fixed |
| P414_MAX_WITHDRAWAL_PRESSURE | 0.25 | fixed |
| P414_STOP_BPS | 10 | fixed |
| P414_TAKE_PROFIT_BPS | 14 | fixed |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| phase298_dense_root | raw_synthetic_l2_dense_full_year | Raw dense source root. |
| phase298_full_depth_required | 1 | Must be one. |
| phase298_levels_2_to_5_required | 1 | Must be one. |
| phase298_l1_only_variant_rows | 0 | Must be zero. |
| phase298_net_edge_live_mask_rows | 0 | Must be zero. |
| phase298_schema_present_columns_min | 30 | Minimum present L1-L5 price/quantity/order columns. |
| phase409_maker_route_closed | P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED | Closed market-maker context. |
| phase412_zero_event_verdict | P412_REPLENISHMENT_BREAKOUT_REJECTED_AS_ZERO_EVENT_FORM | Closed replenishment-breakout context. |
| phase413_synthetic_scan_points | 840 | Attribution universe size. |
| phase413_synthetic_pass_all_filters | 0 | Must be zero for zero-event diagnosis. |
| phase413_l2_l5_replenishment_pass_rate | 0.00833333 | Phase413 bottleneck evidence. |
| phase413_top5_alignment_first_failure_count | 483 | Phase413 earliest failure evidence. |
| execution_results_generated_now | 0 | Precommit only. |

## Phase415 Hard-Gate Contract

| gate_id | requirement | severity | phase414_precommitted |
| --- | --- | --- | --- |
| P415_TICK_ORDERED_REPLAY | Execution must iterate ticks in timestamp order. | hard | 1 |
| P415_DEEP_BOOK_DIVERGENCE_SIGNAL | Signal must require levels 2-5 pressure opposing impulse. | hard | 1 |
| P415_NOT_PHASE410_THRESHOLD_RELAXATION | No reuse of replenishment-breakout same-family thresholds as a rescue. | hard | 1 |
| P415_TAKER_ONLY_EXECUTION | No passive fills, no maker rebate, no two-sided quoting. | hard | 1 |
| P415_FULL_DEPTH_L1_L5 | Execution must read L1-L5 book state. | hard | 1 |
| P415_LEVELS_2_TO_5_MATERIAL | Removing levels 2-5 must be a logged control. | hard | 1 |
| P415_NO_LOOKAHEAD | All features must be computed before entry tick. | hard | 1 |
| P415_COST200_FIXED_CAPITAL | Use Zerodha cost200 with fixed capital and notional. | hard | 1 |
| P415_FIXED_PARAMETERS | No post-result tuning. | hard | 1 |
| P415_EVENT_FLOOR | Completed round trips >= 30. | hard | 1 |
| P415_DATE_BREADTH | Distinct trade dates >= 5. | hard | 1 |
| P415_SYMBOL_BREADTH | Distinct symbols >= 3. | hard | 1 |
| P415_POSITIVE_DATE_FRACTION | Positive date fraction >= 0.6. | hard | 1 |
| P415_ANNUALIZED_FLOOR | Annualized fixed-capital return >= 12.0 percent. | hard | 1 |
| P415_SIDE_FLIP_CONTROL | Side-flip must not dominate primary. | hard | 1 |
| P415_L2_L5_REMOVED_CONTROL | Levels 2-5 removed control must degrade or invalidate primary. | hard | 1 |
| P415_TOP5_ONLY_CONTROL | Top5-only control must be reported. | hard | 1 |
| P415_REAL_ANCHOR_CROSS_CHECK | Synthetic winner sign must be cross-checked on real anchors. | hard | 1 |
| P415_BOUNDARIES_CLOSED | No promotion, paper/live acceptance or deployable claim. | hard | 1 |

## Phase414 Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P414_PHASE298_RAW_DENSE_PRESENT | True | raw_synthetic_l2_dense_full_year | raw_synthetic_l2_dense_full_year | hard |
| P414_FULL_DEPTH_SCHEMA_PRESENT | True | 30 | >=30 | hard |
| P414_LEVELS_2_TO_5_REQUIRED | True | 1 | 1 | hard |
| P414_L1_ONLY_FORBIDDEN | True | 0 | 0 | hard |
| P414_NO_LOOKAHEAD_SOURCE | True | 0 | 0 | hard |
| P414_MARKET_MAKER_ROUTE_CLOSED | True | P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED | P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED | hard |
| P414_REPLENISHMENT_BREAKOUT_CLOSED | True | P412_REPLENISHMENT_BREAKOUT_REJECTED_AS_ZERO_EVENT_FORM | P412_REPLENISHMENT_BREAKOUT_REJECTED_AS_ZERO_EVENT_FORM | hard |
| P414_PHASE413_ATTRIBUTION_PRESENT | True | scan=840;pass_all=0 | scan>0;pass_all=0 | hard |
| P414_MATERIALLY_DIFFERENT_LESS_SPARSE_FORM | True | deep_book_divergence_snapback_not_replenishment_breakout_not_market_making_not_passive | different_closed_families | hard |
| P414_FULL_DEPTH_DIVERGENCE_REQUIRED | True | opposing_l2_l5_imbalance | present | hard |
| P414_FIXED_PARAMETERS_FROZEN | True | 11 | >=11 | hard |
| P414_TAKER_ONLY_PINNED | True | taker_only | present | hard |
| P414_COST200_FIXED_CAPITAL_PINNED | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P414_EXECUTION_HARD_GATES_PRECOMMITTED | True | 19 | 19 | hard |
| P414_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P414_FORBIDDEN_ROUTES_CLOSED | True | phase410_threshold_relaxation;market_maker_rescue;passive_fill_rescue;bar_return_reversal_alone;promotion;paper_live;deployable_claim | closed_routes_listed | hard |
| P414_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

No strategy result, promotion, paper/live acceptance or deployable profitability claim is generated by Phase414.

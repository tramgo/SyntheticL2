# Phase427 Broader Full-Depth Feature-Family Sweep Precommit

Phase427 freezes a broader full-depth L2 feature-family sweep after the narrow Phase424 queue-depletion route failed with zero synthetic events.

This is still not paper/live: it is a precommitted research sweep with exact-tick exits, cost200, fixed capital, L1-only controls and closed boundaries.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase427_broader_full_depth_feature_family_precommit_complete | 1 | Phase427 precommit completed |
| phase427_thesis_id | P427_BROADER_FULL_DEPTH_FEATURE_FAMILY_SWEEP | Frozen thesis |
| phase427_family_rows | 6 | Frozen family rows |
| phase427_scenario_grid_rows | 1458 | Frozen scenario rows |
| phase427_parameter_grid_hash | 15b6b16d70fd944b4a1dbac15df59f2021ab587f078b4bac555539e5f1a1d36b | Hash of frozen grid |
| phase427_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha cost model |
| phase427_cost_multiplier | 2 | Cost200 |
| phase427_initial_capital_inr | 1e+06 | Fixed capital |
| phase427_order_notional_inr | 100000 | Order notional |
| phase427_execution_results_generated | 0 | Precommit only |
| phase427_strategy_promotion_allowed | 0 | No promotion |
| phase427_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase427_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase427_execution_allowed_next | 1 | Whether Phase428 may run |
| phase427_hard_gate_pass_rows | 13 | Passed hard gates |
| phase427_hard_gate_rows | 13 | Hard gates |
| phase427_next_best_action | run_phase428_broader_full_depth_feature_family_sweep_no_paper_live | Recommended next action |

## Frozen Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P427_BROADER_FULL_DEPTH_FEATURE_FAMILY_SWEEP | Material-new broader full-depth L2 feature-family sweep after repeated narrow-route failures. |
| material_difference | precommitted_multi_family_sweep_not_single_threshold_rescue | Tests several distinct full-depth archetypes without post-result threshold edits. |
| families | depth_pressure_continuation;depth_pressure_reversal;spread_compression_breakout;spread_expansion_fade;queue_churn_followthrough;book_slope_migration | Frozen feature families. |
| scenario_rows | 1458 | Frozen scenario grid size. |
| execution_profile | single_name_taker_entry_taker_exit_exact_forward_ticks_cost200 | No passive fills or maker rebate. |
| full_depth_required | L1_to_L5_price_quantity_orders_levels_2_to_5_materiality | Primary scenarios require top-five book state. |
| controls | l1_only_removed_depth;side_flip;family_rank_stability;real_anchor_cross_check | Controls must be reported. |
| capital | initial=1000000.0;order_notional=100000.0 | Fixed capital denominator. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha equity intraday NSE formula. |
| cost_multiplier | 2 | Cost200 acceptance scoring. |
| acceptance | round_trips>=30;dates>=5;symbols>=5;positive_date_fraction>=0.6;annualized>=12.0;l2_l5_edge_delta>=5.0 | Broad search still needs profitability, breadth and full-depth uniqueness. |
| reporting_limit | top_survivors<=25 | Report bounded candidates, not unlimited curve-fit tables. |
| forbidden | pair_spread_rescue;queue_depletion_threshold_rescue;market_maker_rescue;passive_fill_rescue;bar_return_reversal_alone;post_result_threshold_tuning;promotion;paper_live;deployable_claim | Closed routes and boundaries. |

## Feature Families

| family_id | description | requires_l2_l5 | has_l1_only_control | has_side_flip_control |
| --- | --- | --- | --- | --- |
| depth_pressure_continuation | top5_and_l2_l5_imbalance_align_with_last_price_microtrend | 1 | 1 | 1 |
| depth_pressure_reversal | top5_and_l2_l5_imbalance_opposes_last_price_microtrend | 1 | 1 | 1 |
| spread_compression_breakout | spread_contracts_while_l2_l5_same_side_replenishes | 1 | 1 | 1 |
| spread_expansion_fade | spread_expands_while_opposite_l2_l5_absorbs | 1 | 1 | 1 |
| queue_churn_followthrough | order_count_churn_and_depth_replacement_align_with_direction | 1 | 1 | 1 |
| book_slope_migration | weighted_depth_slope_migrates_from_far_levels_to_l1 | 1 | 1 | 1 |

## Frozen Scenario Grid Sample

| scenario_id | family_id | lookback_ticks | forward_ticks | min_forward_hold_ms | max_hold_ticks | max_spread_bps | imbalance_threshold | depth_change_threshold | cost_multiplier | order_notional_inr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P428_depth_pressure_continuation_L60_F3_S4p0_I0p25_D0p1 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 4 | 0.25 | 0.1 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S4p0_I0p25_D0p25 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 4 | 0.25 | 0.25 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S4p0_I0p25_D0p4 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 4 | 0.25 | 0.4 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S4p0_I0p4_D0p1 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 4 | 0.4 | 0.1 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S4p0_I0p4_D0p25 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 4 | 0.4 | 0.25 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S4p0_I0p4_D0p4 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 4 | 0.4 | 0.4 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S4p0_I0p55_D0p1 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 4 | 0.55 | 0.1 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S4p0_I0p55_D0p25 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 4 | 0.55 | 0.25 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S4p0_I0p55_D0p4 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 4 | 0.55 | 0.4 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S8p0_I0p25_D0p1 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 8 | 0.25 | 0.1 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S8p0_I0p25_D0p25 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 8 | 0.25 | 0.25 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S8p0_I0p25_D0p4 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 8 | 0.25 | 0.4 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S8p0_I0p4_D0p1 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 8 | 0.4 | 0.1 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S8p0_I0p4_D0p25 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 8 | 0.4 | 0.25 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S8p0_I0p4_D0p4 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 8 | 0.4 | 0.4 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S8p0_I0p55_D0p1 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 8 | 0.55 | 0.1 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S8p0_I0p55_D0p25 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 8 | 0.55 | 0.25 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S8p0_I0p55_D0p4 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 8 | 0.55 | 0.4 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S12p0_I0p25_D0p1 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 12 | 0.25 | 0.1 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S12p0_I0p25_D0p25 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 12 | 0.25 | 0.25 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S12p0_I0p25_D0p4 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 12 | 0.25 | 0.4 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S12p0_I0p4_D0p1 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 12 | 0.4 | 0.1 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S12p0_I0p4_D0p25 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 12 | 0.4 | 0.25 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S12p0_I0p4_D0p4 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 12 | 0.4 | 0.4 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S12p0_I0p55_D0p1 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 12 | 0.55 | 0.1 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S12p0_I0p55_D0p25 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 12 | 0.55 | 0.25 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F3_S12p0_I0p55_D0p4 | depth_pressure_continuation | 60 | 3 | 250 | 60 | 12 | 0.55 | 0.4 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F6_S4p0_I0p25_D0p1 | depth_pressure_continuation | 60 | 6 | 250 | 60 | 4 | 0.25 | 0.1 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F6_S4p0_I0p25_D0p25 | depth_pressure_continuation | 60 | 6 | 250 | 60 | 4 | 0.25 | 0.25 | 2 | 100000 |
| P428_depth_pressure_continuation_L60_F6_S4p0_I0p25_D0p4 | depth_pressure_continuation | 60 | 6 | 250 | 60 | 4 | 0.25 | 0.4 | 2 | 100000 |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| phase298_dense_root | raw_synthetic_l2_dense_full_year | Raw dense source root. |
| phase298_full_depth_required | 1 | Must be one. |
| phase298_levels_2_to_5_required | 1 | Must be one. |
| phase298_l1_only_variant_rows | 0 | Must be zero. |
| phase298_schema_present_columns_min | 30 | Minimum L1-L5 schema columns. |
| phase426_selected_verdict | P426_QUEUE_DEPLETION_CONTINUATION_REJECTED_ZERO_SYNTHETIC_EVENTS | Queue-depletion closure context. |
| phase426_same_family_tuning_allowed | 0 | Must be zero. |
| scenario_grid_rows | 1458 | Precommitted scenario count. |
| family_rows | 6 | Precommitted family count. |
| symbol_rows | 32 | Precommitted symbol universe. |
| execution_results_generated_now | 0 | Precommit only. |

## Phase428 Hard-Gate Contract

| gate_id | requirement | severity | phase427_precommitted |
| --- | --- | --- | --- |
| P428_PHASE427_PRECOMMIT_USED | Execution must read Phase427 frozen grid. | hard | 1 |
| P428_TICK_ORDERED_REPLAY | Ticks consumed in exchange-time order. | hard | 1 |
| P428_EXACT_FORWARD_TICK_INDEXING | Every trade exit must use exact post-entry tick offsets. | hard | 1 |
| P428_FULL_DEPTH_PRIMARY_FEATURES | Primary scenarios require L2-L5 features. | hard | 1 |
| P428_L1_ONLY_CONTROL | Run removed-depth control for every surviving family. | hard | 1 |
| P428_SIDE_FLIP_CONTROL | Run side-flip control for every surviving family. | hard | 1 |
| P428_COST200_FIXED_CAPITAL | Use Zerodha cost200 and fixed INR 1,000,000 capital. | hard | 1 |
| P428_BREADTH_AND_RETURN_GATES | Apply event/date/symbol/positive-date/annualized gates. | hard | 1 |
| P428_REAL_ANCHOR_CROSS_CHECK | Replay top bounded survivors on available real anchors. | hard | 1 |
| P428_NO_POST_RESULT_TUNING | Do not add thresholds after seeing results. | hard | 1 |
| P428_BOUNDARIES_CLOSED | No promotion, paper/live or deployable claim. | hard | 1 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P427_PHASE298_RAW_DENSE_PRESENT | True | raw_synthetic_l2_dense_full_year | raw_synthetic_l2_dense_full_year | hard |
| P427_FULL_DEPTH_SCHEMA_PRESENT | True | 30 | >=30 | hard |
| P427_LEVELS_2_TO_5_REQUIRED | True | 1 | 1 | hard |
| P427_PHASE426_ROUTE_CLOSED | True | P426_QUEUE_DEPLETION_CONTINUATION_REJECTED_ZERO_SYNTHETIC_EVENTS | P426_QUEUE_DEPLETION_CONTINUATION_REJECTED_ZERO_SYNTHETIC_EVENTS | hard |
| P427_NO_SAME_FAMILY_TUNING | True | 0 | 0 | hard |
| P427_MULTI_FAMILY_GRID_FROZEN | True | 1458 | 1458 | hard |
| P427_FAMILY_BREADTH_FROZEN | True | 6 | 6 | hard |
| P427_EXACT_FORWARD_TICK_GRID_FROZEN | True | 3;6;12 | 3;6;12 | hard |
| P427_COST200_FIXED_CAPITAL_PINNED | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P427_EXECUTION_HARD_GATES_PRECOMMITTED | True | 11 | 11 | hard |
| P427_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P427_FORBIDDEN_ROUTES_CLOSED | True | pair_spread_rescue;queue_depletion_threshold_rescue;market_maker_rescue;passive_fill_rescue;bar_return_reversal_alone;post_result_threshold_tuning;promotion;paper_live;deployable_claim | closed_routes_listed | hard |
| P427_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

No Phase427 strategy result, promotion, paper/live acceptance or deployable claim is generated.

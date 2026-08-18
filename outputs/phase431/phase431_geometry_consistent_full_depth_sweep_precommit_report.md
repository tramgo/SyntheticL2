# Phase431 Geometry-Consistent Full-Depth Sweep Precommit

Phase431 freezes a timing-geometry repair before rerunning the broader full-depth feature-family sweep.

Only execution geometry is repaired. Feature thresholds remain inherited from Phase427; no signal tuning is performed.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase431_geometry_consistent_precommit_complete | 1 | Phase431 precommit completed |
| phase431_thesis_id | P431_GEOMETRY_CONSISTENT_FULL_DEPTH_FEATURE_SWEEP | Frozen thesis |
| phase431_grid_rows | 972 | Frozen geometry-consistent rows |
| phase431_parameter_grid_hash | 449e98404bc602a0e16d033809099f823f3fde3ee29c14a00dfb6bf0751a68c7 | Hash of frozen grid |
| phase431_synthetic_max_hold_ticks | 2500 | Synthetic repaired max hold |
| phase431_real_anchor_max_hold_ticks | 500 | Real-anchor repaired max hold |
| phase431_forward_ticks | 3 | Forward tick bucket |
| phase431_execution_results_generated | 0 | Precommit only |
| phase431_strategy_promotion_allowed | 0 | No promotion |
| phase431_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase431_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase431_execution_allowed_next | 1 | Whether Phase432 may run |
| phase431_hard_gate_pass_rows | 11 | Passed hard gates |
| phase431_hard_gate_rows | 11 | Hard gates |
| phase431_next_best_action | run_phase432_geometry_consistent_full_depth_feature_sweep_no_paper_live | Recommended next action |

## Frozen Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P431_GEOMETRY_CONSISTENT_FULL_DEPTH_FEATURE_SWEEP | Geometry-consistent repair precommit after Phase430. |
| relationship_to_phase427 | same_feature_threshold_grid_with_timing_geometry_repair_only | Feature thresholds are preserved; only max-hold geometry is repaired. |
| synthetic_geometry | forward_ticks=3;min_hold_ms=250.0;max_hold_ticks=2500 | From Phase430 synthetic feasibility recommendation. |
| real_anchor_geometry | forward_ticks=3;min_hold_ms=250.0;max_hold_ticks=500 | From Phase430 real-anchor feasibility recommendation. |
| scenario_rows | 972 | Frozen repaired grid rows. |
| families | depth_pressure_continuation;depth_pressure_reversal;spread_compression_breakout;spread_expansion_fade;queue_churn_followthrough;book_slope_migration | Same Phase427 feature families. |
| execution_profile | single_name_taker_entry_taker_exit_exact_forward_ticks_cost200 | No passive fills or maker rebate. |
| full_depth_required | L1_to_L5_price_quantity_orders_levels_2_to_5_materiality | Primary scenarios require top-five book state. |
| controls | l1_only_removed_depth;side_flip;real_anchor_cross_check | Controls must be reported. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha equity intraday NSE formula. |
| capital | initial=1000000.0;order_notional=100000.0 | Fixed capital denominator. |
| acceptance | round_trips>=30;dates>=5;symbols>=5;positive_date_fraction>=0.6;annualized>=12.0;l2_l5_edge_delta>=5.0 | Strict acceptance remains unchanged. |
| forbidden | feature_threshold_tuning;pair_spread_rescue;queue_depletion_threshold_rescue;market_maker_rescue;promotion;paper_live;deployable_claim | Closed routes and boundaries. |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| phase427_grid_rows | 1458 | Original broad sweep grid. |
| phase430_audit_complete | 1 | Timing audit complete. |
| phase430_timing_repair_precommit_allowed | 1 | Must be one. |
| phase430_synthetic_recommended_forward_ticks | 3 | Phase430 synthetic recommendation. |
| phase430_synthetic_recommended_max_hold_ticks | 2500 | Phase430 synthetic recommendation. |
| phase430_synthetic_feasible_fraction | 1 | Phase430 synthetic recommendation. |
| phase430_real_recommended_forward_ticks | 3 | Phase430 real-anchor recommendation. |
| phase430_real_recommended_max_hold_ticks | 500 | Phase430 real-anchor recommendation. |
| phase430_real_feasible_fraction | 1 | Phase430 real-anchor recommendation. |
| phase431_grid_rows | 972 | Repaired grid rows. |
| execution_results_generated_now | 0 | Precommit only. |

## Phase432 Hard-Gate Contract

| gate_id | requirement | severity | phase431_precommitted |
| --- | --- | --- | --- |
| P432_PHASE431_PRECOMMIT_USED | Execution must read Phase431 geometry grid. | hard | 1 |
| P432_PANEL_SPECIFIC_GEOMETRY | Synthetic uses max_hold=2500; real-anchor uses max_hold=500. | hard | 1 |
| P432_NO_FEATURE_THRESHOLD_TUNING | Feature thresholds must match Phase427 grid dimensions. | hard | 1 |
| P432_EXACT_FORWARD_TICK_INDEXING | Every trade exit uses exact post-entry tick indexing. | hard | 1 |
| P432_FULL_DEPTH_PRIMARY_FEATURES | Primary scenarios require L2-L5 features. | hard | 1 |
| P432_L1_ONLY_CONTROL | Run removed-depth control for top/surviving scenarios. | hard | 1 |
| P432_SIDE_FLIP_CONTROL | Run side-flip control for top/surviving scenarios. | hard | 1 |
| P432_COST200_FIXED_CAPITAL | Use Zerodha cost200 and fixed INR 1,000,000 capital. | hard | 1 |
| P432_BREADTH_AND_RETURN_GATES | Apply event/date/symbol/positive-date/annualized gates. | hard | 1 |
| P432_REAL_ANCHOR_CROSS_CHECK | Replay top synthetic candidates using real-anchor geometry. | hard | 1 |
| P432_BOUNDARIES_CLOSED | No promotion, paper/live or deployable claim. | hard | 1 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P431_PHASE430_COMPLETE | True | 1 | 1 | hard |
| P431_TIMING_REPAIR_ALLOWED | True | 1 | 1 | hard |
| P431_SYNTHETIC_GEOMETRY_MATCHES_AUDIT | True | 2500 | 2500 | hard |
| P431_REAL_GEOMETRY_MATCHES_AUDIT | True | 500 | 500 | hard |
| P431_FEATURE_THRESHOLDS_NOT_TUNED | True | phase427_threshold_dimensions_preserved_except_forward_bucket_repair | preserved | hard |
| P431_PANEL_GEOMETRY_GRID_FROZEN | True | 972 | 972 | hard |
| P431_COST200_FIXED_CAPITAL_PINNED | True | cost=2.0;capital=1000000.0 | cost200_fixed_capital | hard |
| P431_EXECUTION_HARD_GATES_PRECOMMITTED | True | 11 | 11 | hard |
| P431_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P431_FORBIDDEN_ROUTES_CLOSED | True | feature_threshold_tuning;pair_spread_rescue;queue_depletion_threshold_rescue;market_maker_rescue;promotion;paper_live;deployable_claim | closed_routes_listed | hard |
| P431_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

## Repaired Grid Sample

| scenario_id | panel | family_id | lookback_ticks | forward_ticks | min_forward_hold_ms | max_hold_ticks | max_spread_bps | imbalance_threshold | depth_change_threshold | cost_multiplier | order_notional_inr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S4p0_I0p25_D0p1 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 4 | 0.25 | 0.1 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S4p0_I0p25_D0p25 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 4 | 0.25 | 0.25 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S4p0_I0p25_D0p4 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 4 | 0.25 | 0.4 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S4p0_I0p4_D0p1 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 4 | 0.4 | 0.1 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S4p0_I0p4_D0p25 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 4 | 0.4 | 0.25 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S4p0_I0p4_D0p4 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 4 | 0.4 | 0.4 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S4p0_I0p55_D0p1 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 4 | 0.55 | 0.1 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S4p0_I0p55_D0p25 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 4 | 0.55 | 0.25 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S4p0_I0p55_D0p4 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 4 | 0.55 | 0.4 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p1 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 8 | 0.25 | 0.1 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p25 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 8 | 0.25 | 0.25 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p4 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 8 | 0.25 | 0.4 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p4_D0p1 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 8 | 0.4 | 0.1 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p4_D0p25 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 8 | 0.4 | 0.25 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p4_D0p4 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 8 | 0.4 | 0.4 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p55_D0p1 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 8 | 0.55 | 0.1 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p55_D0p25 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 8 | 0.55 | 0.25 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p55_D0p4 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 8 | 0.55 | 0.4 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p25_D0p1 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 12 | 0.25 | 0.1 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p25_D0p25 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 12 | 0.25 | 0.25 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p25_D0p4 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 12 | 0.25 | 0.4 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p4_D0p1 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 12 | 0.4 | 0.1 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p4_D0p25 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 12 | 0.4 | 0.25 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p4_D0p4 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 12 | 0.4 | 0.4 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p55_D0p1 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 12 | 0.55 | 0.1 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p55_D0p25 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 12 | 0.55 | 0.25 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S12p0_I0p55_D0p4 | synthetic | depth_pressure_continuation | 60 | 3 | 250 | 2500 | 12 | 0.55 | 0.4 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S4p0_I0p25_D0p1 | synthetic | depth_pressure_continuation | 180 | 3 | 250 | 2500 | 4 | 0.25 | 0.1 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S4p0_I0p25_D0p25 | synthetic | depth_pressure_continuation | 180 | 3 | 250 | 2500 | 4 | 0.25 | 0.25 | 2 | 100000 |
| P432_synthetic_depth_pressure_continuation_L180_F3_M2500_S4p0_I0p25_D0p4 | synthetic | depth_pressure_continuation | 180 | 3 | 250 | 2500 | 4 | 0.25 | 0.4 | 2 | 100000 |

No Phase431 strategy result, promotion, paper/live acceptance or deployable claim is generated.

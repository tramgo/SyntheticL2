# Phase410 Full-Depth Replenishment Breakout Precommit

Phase410 freezes a materially different full-depth L2 thesis after Phase409 falsified the tested retail two-sided market-maker route.

The thesis is taker-only continuation after a stateful sequence: impulse, levels 2-5 replenishment, spread control, then breakout confirmation.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase410_full_depth_replenishment_breakout_precommit_complete | 1 | Phase410 precommit completed |
| phase410_thesis_id | P410_FULL_DEPTH_REPLENISHMENT_BREAKOUT_TAKER_ONLY | Frozen thesis |
| phase410_material_new_after_phase409 | 1 | Not market-making, passive rescue, liquidity-vacuum rescue or bar-reversal rescue |
| phase410_contract_rows | 26 | Contract rows |
| phase410_parameter_freeze_rows | 13 | Frozen parameter rows |
| phase410_parameter_freeze_hash | 26ef1b2fb6ec4aa3fc7843275feb1e090ce7a9a7e33df0fd4673510b7a8f8482 | Hash of frozen parameter table |
| phase410_real_anchor_date_count | 16 | Local real anchor dates |
| phase410_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha cost model |
| phase410_cost_multiplier | 2 | Cost200 |
| phase410_initial_capital_inr | 1e+06 | Fixed capital |
| phase410_fixed_notional_inr | 100000 | Fixed notional per trade |
| phase410_execution_results_generated | 0 | Precommit only |
| phase410_strategy_promotion_allowed | 0 | No promotion |
| phase410_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase410_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase410_execution_allowed_next | 1 | Whether Phase411 may run |
| phase410_hard_gate_pass_rows | 17 | Passed hard gates |
| phase410_hard_gate_rows | 17 | Hard gates |
| phase410_next_best_action | run_phase411_full_depth_replenishment_breakout_execution_no_paper_live | Recommended next action |

## Frozen Thesis Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P410_FULL_DEPTH_REPLENISHMENT_BREAKOUT_TAKER_ONLY | Material-new full-depth L2 thesis after Phase409 falsified retail maker route. |
| material_difference | taker_only_replenishment_breakout_not_market_making_not_passive_not_vacuum | No two-sided quoting, no passive queue rescue, no liquidity-vacuum continuation. |
| market_hypothesis | when impulse is followed by levels_2_to_5_replenishment_and_spread_control_price_breaks_in_impulse_direction | Strong depth rebuild behind the move may indicate real continuation support. |
| event_sequence | impulse_window_then_rebuild_window_then_breakout_confirmation_window | Stateful sequence; not a one-bar reversal or same-event shortcut. |
| impulse_window_seconds | 30 | Past-only impulse measurement. |
| rebuild_confirm_seconds | 20 | Past-only depth rebuild confirmation window. |
| breakout_confirm_seconds | 10 | Past-only confirmation before taker entry. |
| horizon_seconds | 180 | Exit horizon if stop/target not reached. |
| entry_execution | taker_entry_after_breakout_confirmation | No passive fill model and no maker rebate. |
| exit_execution | taker_stop_or_target_or_horizon_exit | Taker-only close. |
| side_rule | trade_in_impulse_direction_only | Long after positive impulse; short after negative impulse. |
| min_abs_impulse_bps | 4 | Fixed threshold, no post-result tuning. |
| min_levels_2_to_5_replenishment_pressure | 0.12 | Core full-depth gate beyond L1. |
| min_top5_imbalance_alignment | 0.15 | Top-five alignment with side. |
| min_level_weighted_imbalance_alignment | 0.15 | Level-weighted L1-L5 alignment with side. |
| max_spread_bps | 8 | Avoid wide-spread conditions. |
| max_depth_withdrawal_pressure | 0.1 | Reject cases where visible book is being pulled. |
| stop_bps | 12 | Fixed stop, not optimized after results. |
| take_profit_bps | 18 | Fixed target, not optimized after results. |
| full_depth_required | L1_to_L5_book_state_with_levels_2_to_5_materiality | L1-only variants forbidden. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha equity intraday NSE formula. |
| cost_multiplier | 2 | Cost200 acceptance scoring. |
| capital | initial=1000000.0;notional=100000.0;max_concurrent=2 | Fixed capital denominator; no unlimited capital. |
| acceptance | round_trips>=30;dates>=5;symbols>=3;positive_date_fraction>=0.6;annualized>=12.0 | Profitability must meet breadth and annualized gates. |
| controls | side_flip;levels_2_to_5_removed;spread_gate_removed;synthetic_vs_real_anchor_sign | Controls required in execution phase. |
| forbidden | same_family_market_maker_tuning;passive_fill_rescue;liquidity_vacuum_rescue;bar_reversal_rescue;promotion;paper_live;deployable_profit_claim | Boundaries remain closed. |

## Frozen Parameters

| parameter_id | value | status |
| --- | --- | --- |
| P410_FIXED_SIGNAL | impulse_rebuild_breakout | single frozen signal form |
| P410_IMPULSE_LOOKBACK_SECONDS | 30 | past-only |
| P410_REBUILD_CONFIRM_SECONDS | 20 | past-only |
| P410_BREAKOUT_CONFIRM_SECONDS | 10 | past-only |
| P410_HORIZON_SECONDS | 180 | fixed |
| P410_STOP_BPS | 12 | fixed |
| P410_TAKE_PROFIT_BPS | 18 | fixed |
| P410_MIN_ABS_IMPULSE_BPS | 4 | fixed |
| P410_MIN_L2_L5_REPLENISHMENT_PRESSURE | 0.12 | fixed |
| P410_MIN_TOP5_IMBALANCE_ALIGNMENT | 0.15 | fixed |
| P410_MIN_LEVEL_WEIGHTED_IMBALANCE_ALIGNMENT | 0.15 | fixed |
| P410_MAX_SPREAD_BPS | 8 | fixed |
| P410_MAX_DEPTH_WITHDRAWAL_PRESSURE | 0.1 | fixed |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| phase298_dense_root | raw_synthetic_l2_dense_full_year | Raw dense source root. |
| phase298_raw_book_state_l1_l5_required | 1 | Full-depth source requirement. |
| phase298_levels_2_to_5_required | 1 | Levels 2-5 materiality. |
| phase298_l1_only_variant_rows | 0 | Must be zero. |
| phase298_net_edge_live_mask_rows | 0 | Must be zero. |
| phase298_schema_present_columns_min | 30 | Minimum present L1-L5 price/quantity/order columns in Phase298 schema audit. |
| phase403_material_new_thesis_required | 1 | Phase403 material-new requirement. |
| phase409_selected_verdict | P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED | Phase409 closure context. |
| phase409_same_family_tuning_allowed | 0 | Must be zero. |
| real_anchor_dates | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14;2026-07-15;2026-07-16;2026-07-17;2026-07-20;2026-07-21;2026-07-22;2026-07-23;2026-07-24;2026-07-27;2026-08-03;2026-08-04 | Verified local real L2 anchor dates. |
| real_anchor_date_count | 16 | At least 3 required. |
| execution_results_generated_now | 0 | Precommit only. |

## Phase411 Hard-Gate Contract

| gate_id | requirement | severity | phase410_precommitted |
| --- | --- | --- | --- |
| P411_TICK_ORDERED_REPLAY | Execution must iterate ticks in timestamp order; no bar-only shortcut. | hard | 1 |
| P411_STATEFUL_SEQUENCE | Signal requires impulse then depth rebuild then breakout confirmation. | hard | 1 |
| P411_TAKER_ONLY_EXECUTION | No passive fills, no two-sided quoting, no maker rebate. | hard | 1 |
| P411_FULL_DEPTH_L1_L5 | Execution must read all L1-L5 price/quantity/order fields where available. | hard | 1 |
| P411_LEVELS_2_TO_5_MATERIAL | At least one required signal gate must use levels 2-5 excluding L1. | hard | 1 |
| P411_NO_LOOKAHEAD | All feature windows must end before order arrival/fill evaluation. | hard | 1 |
| P411_COST200_FIXED_CAPITAL | Use Zerodha cost200, fixed initial capital and fixed notional. | hard | 1 |
| P411_FIXED_PARAMETERS | No post-result threshold tuning or rescue grid. | hard | 1 |
| P411_EVENT_FLOOR | Completed round trips >= 30. | hard | 1 |
| P411_DATE_BREADTH | Distinct trade dates >= 5. | hard | 1 |
| P411_SYMBOL_BREADTH | Distinct symbols >= 3. | hard | 1 |
| P411_POSITIVE_DATE_FRACTION | Positive date fraction >= 0.6. | hard | 1 |
| P411_ANNUALIZED_FLOOR | Annualized fixed-capital return >= 12.0 percent. | hard | 1 |
| P411_SIDE_FLIP_CONTROL | Side-flip control must not dominate the primary. | hard | 1 |
| P411_L2_L5_REMOVED_CONTROL | Removing levels 2-5 must degrade or invalidate the primary. | hard | 1 |
| P411_SPREAD_GATE_REMOVED_CONTROL | Spread-gate-removed control must be reported. | hard | 1 |
| P411_REAL_ANCHOR_CROSS_CHECK | Synthetic winner sign must be cross-checked on reserved real anchors. | hard | 1 |
| P411_BOUNDARIES_CLOSED | No promotion, paper/live acceptance or deployable claim. | hard | 1 |

## Phase410 Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P410_PHASE298_RAW_DENSE_PRESENT | True | raw_synthetic_l2_dense_full_year | raw_synthetic_l2_dense_full_year | hard |
| P410_FULL_DEPTH_SCHEMA_PRESENT | True | 30 | >=30 | hard |
| P410_LEVELS_2_TO_5_REQUIRED | True | 1 | 1 | hard |
| P410_L1_ONLY_FORBIDDEN | True | 0 | 0 | hard |
| P410_NO_LOOKAHEAD_SOURCE | True | 0 | 0 | hard |
| P410_PHASE403_MATERIAL_NEW_REQUIRED | True | 1 | 1 | hard |
| P410_PHASE409_MAKER_ROUTE_CLOSED | True | P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED | P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED | hard |
| P410_NO_SAME_FAMILY_TUNING | True | 0 | 0 | hard |
| P410_MATERIALLY_DIFFERENT_THESIS | True | taker_only_replenishment_breakout_not_market_making_not_passive_not_vacuum | not_closed_family | hard |
| P410_FIXED_PARAMETERS_FROZEN | True | 13 | >=13 | hard |
| P410_TAKER_ONLY_PINNED | True | taker_only | present | hard |
| P410_COST200_FIXED_CAPITAL_PINNED | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P410_REAL_ANCHORS_AT_LEAST_THREE | True | 16 | >=3 | hard |
| P410_EXECUTION_HARD_GATES_PRECOMMITTED | True | 18 | 18 | hard |
| P410_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P410_FORBIDDEN_ROUTES_CLOSED | True | same_family_market_maker_tuning;passive_fill_rescue;liquidity_vacuum_rescue;bar_reversal_rescue;promotion;paper_live;deployable_profit_claim | closed_routes_listed | hard |
| P410_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

No strategy result, promotion, paper/live acceptance or deployable profitability claim is generated by Phase410.

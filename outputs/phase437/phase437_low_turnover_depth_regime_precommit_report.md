# Phase437 Low-Turnover Full-Depth Regime Carry Precommit

Phase437 freezes a materially new lower-turnover and longer-horizon source after Phase436 showed dense event ranking remained cost-dominated.

The selected source uses early-session L1-L5 book pressure to take at most one trade per symbol/date, then holds for a precommitted longer tick horizon.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase437_low_turnover_precommit_complete | 1 | Phase437 precommit completed |
| phase437_thesis_id | P437_LOW_TURNOVER_FULL_DEPTH_REGIME_CARRY_PRECOMMIT | Frozen thesis |
| phase437_selected_source_id | opening_full_depth_regime_carry_one_trade_per_symbol_date | Selected lower-turnover source |
| phase437_grid_rows | 18 | Frozen scenario rows |
| phase437_grid_hash | 876b8c107924183e7c6dae45e717ac4302ec16f54249a474aa26bd2e7dee8a11 | Hash of frozen grid |
| phase437_max_trades_per_symbol_date | 1 | Turnover cap |
| phase437_min_hold_ticks | 1200 | Minimum longer-horizon hold |
| phase437_execution_results_generated | 0 | Precommit only |
| phase437_strategy_promotion_allowed | 0 | No promotion |
| phase437_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase437_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase437_execution_allowed_next | 1 | Whether Phase438 may execute |
| phase437_hard_gate_pass_rows | 11 | Passed hard gates |
| phase437_hard_gate_rows | 11 | Hard gates |
| phase437_next_best_action | run_phase438_low_turnover_depth_regime_carry_no_paper_live | Recommended next action |

## Frozen Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P437_LOW_TURNOVER_FULL_DEPTH_REGIME_CARRY_PRECOMMIT | Lower-turnover full-depth source precommit after Phase436. |
| selected_source | opening_full_depth_regime_carry_one_trade_per_symbol_date | One trade per symbol/date from early-session L1-L5 regime. |
| relationship_to_phase436 | materially_new_lower_turnover_longer_horizon_source | Directly responds to cost domination in Phase435. |
| turnover_policy | max_trades_per_symbol_date=1 | No dense tick-scalping. |
| entry_policy | observe_early_window_then_enter_after_fixed_tick_delay | Signal data precedes entry. |
| exit_policy | exit_after_precommitted_longer_hold_ticks_or_end_of_group | Longer horizon intended to reduce cost drag per gross opportunity. |
| early_window_ticks | 120;240;480 | Frozen early full-depth observation windows. |
| hold_ticks | 1200;2400;3600 | Frozen longer-horizon hold windows. |
| entry_delay_ticks | 5 | Frozen entry delay. |
| full_depth_features | L1_mid_spread_volume_plus_L2_to_L5_imbalance_depth_slope_order_churn_replenishment | Top-five depth is core. |
| direction_rule | sign_of_early_top5_pressure_plus_l2_l5_slope;optional_contrarian_variant_precommitted | Simple low-turnover directional regime, not learned after results. |
| controls_required | l1_only_ablation;side_flip;time_shuffle;real_anchor_cross_check | Controls must be emitted by Phase438. |
| capital_policy | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | Annualized return denominator is fixed capital. |
| acceptance_floor | round_trips_ge_30;dates_ge_5;symbols_ge_5;positive_date_fraction_ge_0.6;annualized_ge_12.0 | User profitability floor with breadth. |
| forbidden | dense_tick_scalping;same_phase435_ranker_rescue;same_phase427_threshold_sweep;market_maker_rescue_without_external_execution_source;promotion;paper_live;deployable_profitability_claim | Closed or forbidden routes. |
| execution_results_generated_now | 0 | Precommit only. |

## Frozen Scenario Grid

| scenario_id | family_id | direction_mode | early_window_ticks | hold_ticks | entry_delay_ticks | max_trades_per_symbol_date | cost_multiplier | order_notional_inr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P438_depth_regime_carry_E120_H1200_D5 | depth_regime_carry | with_early_full_depth_pressure | 120 | 1200 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_carry_E120_H2400_D5 | depth_regime_carry | with_early_full_depth_pressure | 120 | 2400 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_carry_E120_H3600_D5 | depth_regime_carry | with_early_full_depth_pressure | 120 | 3600 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_carry_E240_H1200_D5 | depth_regime_carry | with_early_full_depth_pressure | 240 | 1200 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_carry_E240_H2400_D5 | depth_regime_carry | with_early_full_depth_pressure | 240 | 2400 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_carry_E240_H3600_D5 | depth_regime_carry | with_early_full_depth_pressure | 240 | 3600 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_carry_E480_H1200_D5 | depth_regime_carry | with_early_full_depth_pressure | 480 | 1200 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_carry_E480_H2400_D5 | depth_regime_carry | with_early_full_depth_pressure | 480 | 2400 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_carry_E480_H3600_D5 | depth_regime_carry | with_early_full_depth_pressure | 480 | 3600 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_snapback_E120_H1200_D5 | depth_regime_snapback | against_early_full_depth_pressure | 120 | 1200 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_snapback_E120_H2400_D5 | depth_regime_snapback | against_early_full_depth_pressure | 120 | 2400 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_snapback_E120_H3600_D5 | depth_regime_snapback | against_early_full_depth_pressure | 120 | 3600 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_snapback_E240_H1200_D5 | depth_regime_snapback | against_early_full_depth_pressure | 240 | 1200 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_snapback_E240_H2400_D5 | depth_regime_snapback | against_early_full_depth_pressure | 240 | 2400 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_snapback_E240_H3600_D5 | depth_regime_snapback | against_early_full_depth_pressure | 240 | 3600 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_snapback_E480_H1200_D5 | depth_regime_snapback | against_early_full_depth_pressure | 480 | 1200 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_snapback_E480_H2400_D5 | depth_regime_snapback | against_early_full_depth_pressure | 480 | 2400 | 5 | 1 | 2 | 100000 |
| P438_depth_regime_snapback_E480_H3600_D5 | depth_regime_snapback | against_early_full_depth_pressure | 480 | 3600 | 5 | 1 | 2 | 100000 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P437_PHASE436_AVAILABLE | True | 1 | 1 | hard |
| P437_PHASE436_NEXT_ACTION_MATCHED | True | precommit_material_new_lower_turnover_horizon_or_pause_strategy_search | lower_turnover_or_longer_horizon | hard |
| P437_MATERIAL_NEW_SOURCE | True | opening_full_depth_regime_carry_one_trade_per_symbol_date | not_phase435_ranker_or_phase427_threshold_sweep | hard |
| P437_LOW_TURNOVER_PINNED | True | 1 | 1 | hard |
| P437_LONGER_HORIZON_PINNED | True | 1200;2400;3600 | min_hold_ticks>=1200 | hard |
| P437_FULL_DEPTH_L2_L5_REQUIRED | True | L1_mid_spread_volume_plus_L2_to_L5_imbalance_depth_slope_order_churn_replenishment | L2-L5 | hard |
| P437_GRID_FROZEN | True | 18 | 18 | hard |
| P437_COST200_FIXED_CAPITAL_PINNED | True | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | cost200_fixed_capital | hard |
| P437_CONTROLS_PRECOMMITTED | True | l1_only_ablation;side_flip;time_shuffle;real_anchor_cross_check | controls_present | hard |
| P437_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P437_BOUNDARIES_CLOSED | True | dense_tick_scalping;same_phase435_ranker_rescue;same_phase427_threshold_sweep;market_maker_rescue_without_external_execution_source;promotion;paper_live;deployable_profitability_claim | closed | hard |

Boundary: Phase438 may execute this lower-turnover source only. It may not retune Phase435, reopen dense tick scalping, or promote/paper/live anything from this precommit.

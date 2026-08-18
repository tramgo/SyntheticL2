# Phase448 Depth-Curvature Break/Repair Source Precommit

Phase448 responds to the Phase447 holdout rejection by freezing a genuinely new full-depth L2 source edge before any new result generation.

Selected source: `depth_curvature_break_repair`.

The source uses levels 2-5 as the primary information: curvature, slope, asymmetry, break rate and repair rate of visible liquidity beyond the touch.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase448_depth_curvature_precommit_complete | 1 | Phase448 source precommit completed |
| phase448_thesis_id | P448_DEPTH_CURVATURE_BREAK_REPAIR_PRECOMMIT | Frozen thesis/source precommit |
| phase448_selected_source_id | depth_curvature_break_repair | Selected materially new source |
| phase448_execution_results_generated | 0 | Precommit only |
| phase448_strategy_promotion_allowed | 0 | No promotion |
| phase448_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase448_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase448_execution_allowed_next | 1 | Whether Phase449 may execute |
| phase448_hard_gate_pass_rows | 12 | Passed hard gates |
| phase448_hard_gate_rows | 12 | Hard gates |
| phase448_next_best_action | run_phase449_depth_curvature_break_repair_no_paper_live | Recommended next action |

## Prior Evidence Boundary

| phase | route | verdict_or_status | reason_for_not_continuing |
| --- | --- | --- | --- |
| P409 | retail_two_sided_market_maker_cancel_latency | P409_CANCEL_RACE_MARKET_MAKER_FALSIFIED | closed: cancel-included attachment already executed; no same-family maker rescue |
| P435 | supervised_full_depth_event_ranker | -5167.5327371279 | closed for current evidence: learned ranker had negative validation net P&L and failed breadth/profit gates |
| P439 | low_turnover_full_depth_regime_carry | P439_LOW_TURNOVER_FULL_DEPTH_REGIME_CARRY_REJECTED_NO_GROSS_EDGE | closed: no gross edge under low-turnover carry |
| P447 | external_catalyst_continuation_stability | reject_catalyst_continuation_stability_or_precommit_new_source_edge | closed for same-route continuation: frozen chronological holdout failed |

## Source Scorecard

| source_id | material_new_axis | uses_l2_l5_core | non_closed_family | can_execute_next | why_selected |
| --- | --- | --- | --- | --- | --- |
| depth_curvature_break_repair | shape_change_in_depth_levels_2_to_5_curvature_before_short_horizon_break_or_repair | 1 | 1 | 1 | uses the geometry of liquidity across levels 2-5, not catalyst labels, passive making, supervised ranker selection, low-turnover carry or same threshold rescue |
| rerun_catalyst_continuation_with_new_dates | none_without_new_source | 1 | 0 | 0 | rejected: Phase447 failed the frozen stability holdout |
| market_maker_cancel_latency_again | none_without_external_execution_source | 1 | 0 | 0 | rejected: Phase407-409 already falsified the attached cancel-included charter |
| another_supervised_ranker | weak | 1 | 0 | 0 | rejected: Phase435 ranker failed; a new ranker alone is too close without a different label/source |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| phase298_available | 1 | Prior raw dense L1-L5 sweep available. |
| phase298_dense_root | raw_synthetic_l2_dense_full_year | Dense lake root recorded by Phase298. |
| dense_root_exists | 1 | Current dense root exists. |
| dense_parquet_file_count | 384 | Current dense Parquet file count. |
| levels_2_to_5_required | 1 | Phase448 requires depth beyond L1. |
| cost_multiplier | 2 | Cost200 scoring is pinned. |
| initial_capital_inr | 1e+06 | Fixed capital denominator. |
| order_notional_inr | 100000 | Fixed notional per order. |

## Frozen Phase449 Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P448_DEPTH_CURVATURE_BREAK_REPAIR_PRECOMMIT | Phase448 selected source precommit. |
| selected_source | depth_curvature_break_repair | Materially new full-depth source for Phase449. |
| source_row_hash | 74aa661f2b1869449fa03fee7a1096968cf86912de91e732873cbc406666c61d | Hash of selected source scorecard row. |
| market_hypothesis | levels_2_to_5_depth_curvature_break_or_repair_precedes_short_horizon_mid_move | Curvature across deeper visible book can reveal hidden pressure before L1 fully reflects it. |
| feature_family | L2_to_L5_convexity_slope_curvature_asymmetry_repair_rate_and_break_rate | Full top-five market-by-price depth remains core. |
| entry_logic | taker_entry_after_past_only_curvature_break_or_repair_confirmation | No passive fill, no maker rebate and no future label access. |
| side_rule | long_when_bid_depth_curvature_repairs_and_ask_curvature_breaks_short_when_opposite | Side is determined by L2-L5 shape change, not catalyst text or fitted rank. |
| sample_policy | bounded_month_symbol_stride_then_breadth_first_execution | Execution may start bounded but must report breadth and no acceptance if floors are not met. |
| horizon_ticks | 60 | Fixed exit horizon if stop/target not hit. |
| stop_bps | 10.0 | Fixed stop. |
| take_profit_bps | 16.0 | Fixed target. |
| min_event_spacing_ticks | 120 | Avoid overlapping events in the same symbol stream. |
| full_depth_required | L1_to_L5_book_state_with_levels_2_to_5_materiality | L1-only variants are controls, not the primary. |
| controls_required | l1_only_ablation;side_flip;time_reverse_or_shift;curvature_static_snapshot_without_repair | Controls must be emitted by Phase449. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha equity intraday NSE formula. |
| capital_policy | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | Annualized denominator is fixed capital. |
| acceptance_floor | round_trips_ge_30;dates_ge_5;symbols_ge_3;positive_date_fraction_ge_0p60;annualized_ge_12_cost200 | User profitability bar with breadth. |
| forbidden | catalyst_continuation_rescue;market_maker_rescue;supervised_ranker_retry;low_turnover_carry_retry;promotion;paper_live;deployable_profitability_claim | Closed boundaries. |
| execution_results_generated_now | 0 | Precommit only. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P448_PHASE447_AVAILABLE | True | P447 boundary row present | present | hard |
| P448_PHASE447_REJECTED_OR_NEW_SOURCE_REQUIRED | True | reject_catalyst_continuation_stability_or_precommit_new_source_edge | new source required | hard |
| P448_SELECTED_SOURCE_PRESENT | True | 1 | 1 | hard |
| P448_SELECTED_SOURCE_USES_L2_L5 | True | 1 | 1 | hard |
| P448_SELECTED_SOURCE_NOT_CLOSED_FAMILY | True | 1 | 1 | hard |
| P448_PHASE449_EXECUTION_ALLOWED | True | 1 | 1 | hard |
| P448_RAW_DENSE_LAKE_PRESENT | True | exists=1;files=384 | exists_and_files_gt_0 | hard |
| P448_PHASE298_FULL_DEPTH_SOURCE_PRESENT | True | 1 | 1 | hard |
| P448_COST200_FIXED_CAPITAL_PRECOMMITTED | True | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | cost200_fixed_capital | hard |
| P448_CONTROLS_PRECOMMITTED | True | l1_only_ablation;side_flip;time_reverse_or_shift;curvature_static_snapshot_without_repair | controls | hard |
| P448_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P448_BOUNDARIES_CLOSED | True | catalyst_continuation_rescue;market_maker_rescue;supervised_ranker_retry;low_turnover_carry_retry;promotion;paper_live;deployable_profitability_claim | closed | hard |

Boundary: Phase449 may execute this depth-curvature source only. It may not rescue catalyst continuation, market making, supervised ranker, or low-turnover carry routes.

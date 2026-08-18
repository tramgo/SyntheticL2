# Phase469 Source-Event-Aware Feature Repair Precommit

Phase469 freezes a repair for Phase468's constant dense-subtick churn features. It does not materialize the repaired matrix yet.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase469_source_event_aware_feature_repair_precommit_complete | 1 | Phase469 precommit completed |
| phase469_thesis_id | P469_SOURCE_EVENT_AWARE_FEATURE_REPAIR_PRECOMMIT | Precommit thesis |
| phase469_repaired_feature_count | 25 | Repaired feature count |
| phase469_repaired_l2_l5_feature_count | 10 | Repaired L2-L5 feature count |
| phase469_replaced_constant_feature_count | 6 | Constant features replaced |
| phase469_source_event_lookbacks | 1;3;5 | Pinned source-event lookbacks |
| phase469_min_varying_feature_floor | 18 | Phase470 variation floor |
| phase469_model_fit_generated | 0 | No model fit |
| phase469_strategy_pnl_generated | 0 | No strategy P&L |
| phase469_strategy_promotion_allowed | 0 | No promotion |
| phase469_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase469_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase469_phase470_allowed_next | 1 | Allows repaired matrix materialization only |
| phase469_hard_gate_pass_rows | 13 | Passed hard gates |
| phase469_hard_gate_rows | 13 | Hard gates |
| phase469_next_best_action | run_phase470_materialize_source_event_aware_l1_l5_feature_matrix_no_model_no_pnl | Recommended next action |

## Decision Ledger

| decision_id | decision_value | description |
| --- | --- | --- |
| selected_verdict | P469_REPAIR_CONSTANT_DENSE_SUBTICK_FEATURES | Phase468 matrix exists but the variation gate failed. |
| phase468_matrix_rows | 1792 | Phase468 matrix rows. |
| phase468_move_candidate_rows | 935 | Phase468 move candidates. |
| phase468_failed_gate_ids | P468_FEATURE_VARIATION_PRESENT | Failed Phase468 gates. |
| constant_feature_names | recent_mid_return_bps;ofi_l1_lookback;ofi_l25_lookback;l25_replenishment_events;l25_withdrawal_events;spread_change_lookback_bps | Features with one unique value. |
| source_event_lookbacks | 1;3;5 | Distinct source-event lookbacks selected. |
| same_20_dense_tick_churn_reuse_allowed | 0 | Do not reuse the constant dense-subtick churn features. |
| model_fit_allowed | 0 | No model fit in Phase469/470. |
| strategy_pnl_allowed | 0 | No strategy P&L. |
| paper_or_live_acceptance_allowed | 0 | No paper/live. |

## Repaired Feature Contract

| feature_name | feature_family | timestamp_rule | description | uses_l2_l5_depth | allowed_as_model_input |
| --- | --- | --- | --- | --- | --- |
| spread_bps | base | computed only from rows <= entry row inside each candidate window | entry best ask minus best bid in bps | 0 | 1 |
| l1_imbalance | base | computed only from rows <= entry row inside each candidate window | entry level-1 quantity imbalance | 0 | 1 |
| l25_imbalance | base | computed only from rows <= entry row inside each candidate window | entry levels 2-5 quantity imbalance | 1 | 1 |
| volume_delta_lookback | base | computed only from rows <= entry row inside each candidate window | entry volume minus lookback-start volume | 0 | 1 |
| l1_l5_bid_depth_slope | depth_curve_shape | computed only from rows <= entry row inside each candidate window | entry bid quantity slope over levels 1-5 | 1 | 1 |
| l1_l5_ask_depth_slope | depth_curve_shape | computed only from rows <= entry row inside each candidate window | entry ask quantity slope over levels 1-5 | 1 | 1 |
| l1_l5_depth_concentration | depth_curve_shape | computed only from rows <= entry row inside each candidate window | entry L1 depth share of total L1-L5 depth | 1 | 1 |
| l25_order_imbalance | depth_curve_shape | computed only from rows <= entry row inside each candidate window | entry levels 2-5 order-count imbalance | 1 | 1 |
| microprice_l1_minus_mid_bps | microprice_pressure | computed only from rows <= entry row inside each candidate window | L1 microprice displacement from mid at entry | 0 | 1 |
| microprice_l25_minus_mid_bps | microprice_pressure | computed only from rows <= entry row inside each candidate window | levels 2-5 microprice displacement from mid at entry | 1 | 1 |
| spread_mean_lookback_bps | spread_regime_context | computed only from rows <= entry row inside each candidate window | mean spread over past-only lookback | 0 | 1 |
| trade_qty_sum_lookback | volume_acceleration | computed only from rows <= entry row inside each candidate window | sum last_traded_quantity over lookback | 0 | 1 |
| trade_qty_accel_lookback | volume_acceleration | computed only from rows <= entry row inside each candidate window | second-half minus first-half traded quantity over lookback | 0 | 1 |
| minute_of_day | time_of_day_context | computed only from rows <= entry row inside each candidate window | known exchange timestamp minute bucket | 0 | 1 |
| source_event_mid_return_1 | source_event_price | computed from distinct source_annual_event_id rows at or before entry only | mid return versus previous distinct source event | 0 | 1 |
| source_event_mid_return_3 | source_event_price | computed from distinct source_annual_event_id rows at or before entry only | mid return versus three source events back | 0 | 1 |
| source_event_mid_return_5 | source_event_price | computed from distinct source_annual_event_id rows at or before entry only | mid return versus five source events back | 0 | 1 |
| source_event_l1_ofi_1 | source_event_ofi | computed from distinct source_annual_event_id rows at or before entry only | signed L1 depth change versus previous source event | 0 | 1 |
| source_event_l1_ofi_3 | source_event_ofi | computed from distinct source_annual_event_id rows at or before entry only | signed L1 depth change versus three source events back | 0 | 1 |
| source_event_l25_ofi_1 | source_event_ofi | computed from distinct source_annual_event_id rows at or before entry only | signed L2-L5 depth change versus previous source event | 1 | 1 |
| source_event_l25_ofi_3 | source_event_ofi | computed from distinct source_annual_event_id rows at or before entry only | signed L2-L5 depth change versus three source events back | 1 | 1 |
| source_event_l25_replenishment_count_5 | source_event_churn | computed from distinct source_annual_event_id rows at or before entry only | positive L2-L5 depth-change count across last five source events | 1 | 1 |
| source_event_l25_withdrawal_count_5 | source_event_churn | computed from distinct source_annual_event_id rows at or before entry only | negative L2-L5 depth-change count across last five source events | 1 | 1 |
| source_event_spread_change_3_bps | source_event_spread | computed from distinct source_annual_event_id rows at or before entry only | spread change versus three source events back | 0 | 1 |
| source_event_spread_vol_5_bps | source_event_spread | computed from distinct source_annual_event_id rows at or before entry only | spread volatility across last five source events | 0 | 1 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P469_PHASE468_COMPLETE | True | 1 | 1 | hard |
| P469_PHASE468_VARIATION_FAILURE_CONFIRMED | True | P468_FEATURE_VARIATION_PRESENT | P468_FEATURE_VARIATION_PRESENT | hard |
| P469_PHASE469_MODEL_PRECOMMIT_BLOCKED_BY_PHASE468 | True | 0 | 0 | hard |
| P469_CONSTANT_FEATURES_REPLACED | True |  | empty | hard |
| P469_SOURCE_EVENT_REPAIR_FEATURES_ADDED | True | 11 | 11 | hard |
| P469_REPAIRED_FEATURE_COUNT_GE_25 | True | 25 | >=25 | hard |
| P469_REPAIRED_L2_L5_FEATURE_COUNT_GE_10 | True | 10 | >=10 | hard |
| P469_MIN_VARYING_FEATURE_FLOOR_RAISED | True | 18 | >=18 | hard |
| P469_SOURCE_EVENT_LOOKBACKS_PINNED | True | 1;3;5 | 1;3;5 | hard |
| P469_SAME_CONSTANT_REUSE_REJECTED | True | 0 | 0 | hard |
| P469_NO_MODEL_FIT | True | precommit_only | no_model_fit | hard |
| P469_NO_STRATEGY_PNL | True | precommit_only | no_pnl | hard |
| P469_NO_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: Phase470 may materialize the repaired matrix only. Model fitting, strategy replay and P&L remain closed.

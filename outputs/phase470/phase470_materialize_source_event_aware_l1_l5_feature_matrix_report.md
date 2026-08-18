# Phase470 Source-Event-Aware L1-L5 Feature Matrix Materialization

Phase470 materializes the Phase469 repaired feature contract using distinct `source_annual_event_id` history at or before entry.

It does not fit a model and does not emit strategy P&L.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase470_source_event_aware_l1_l5_feature_matrix_complete | 1 | Phase470 matrix materialization completed |
| phase470_thesis_id | P470_MATERIALIZE_SOURCE_EVENT_AWARE_L1_L5_FEATURE_MATRIX | Matrix thesis |
| phase470_phase469_thesis_id | P469_SOURCE_EVENT_AWARE_FEATURE_REPAIR_PRECOMMIT | Precommit source |
| phase470_matrix_rows | 1792 | Matrix rows |
| phase470_feature_count | 25 | Feature count |
| phase470_l2_l5_feature_count | 10 | L2-L5 feature count |
| phase470_move_candidate_rows | 935 | Move candidates |
| phase470_train_rows | 1176 | Train rows |
| phase470_holdout_rows | 616 | Holdout rows |
| phase470_min_source_event_history_rows | 1 | Minimum distinct source-event history rows |
| phase470_model_fit_generated | 0 | No model fit |
| phase470_strategy_pnl_generated | 0 | No strategy P&L |
| phase470_strategy_promotion_allowed | 0 | No promotion |
| phase470_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase470_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase470_phase471_allowed_next | 1 | Allows model precommit only if all gates pass |
| phase470_hard_gate_pass_rows | 14 | Passed hard gates |
| phase470_hard_gate_rows | 14 | Hard gates |
| phase470_next_best_action | precommit_phase471_train_holdout_source_event_aware_l1_l5_model_no_replay | Recommended next action |

## Matrix Summary

| metric | value |
| --- | --- |
| selected_files | 21 |
| files_present | 21 |
| matrix_rows | 1792 |
| feature_count | 25 |
| l2_l5_feature_count | 10 |
| move_candidate_rows | 935 |
| trade_dates | 64 |
| symbols | 7 |
| train_rows | 1176 |
| holdout_rows | 616 |
| train_move_candidate_rows | 626 |
| holdout_move_candidate_rows | 309 |
| long_rows | 943 |
| short_rows | 838 |
| min_source_event_history_rows | 1 |
| median_source_event_history_rows | 9 |

## Feature Quality

| feature_name | present | non_null_rows | unique_values | finite_rows | uses_l2_l5_depth |
| --- | --- | --- | --- | --- | --- |
| spread_bps | 1 | 1792 | 1703 | 1792 | 0 |
| l1_imbalance | 1 | 1792 | 1317 | 1792 | 0 |
| l25_imbalance | 1 | 1792 | 1584 | 1792 | 1 |
| volume_delta_lookback | 1 | 1792 | 23 | 1792 | 0 |
| l1_l5_bid_depth_slope | 1 | 1792 | 1265 | 1792 | 1 |
| l1_l5_ask_depth_slope | 1 | 1792 | 1318 | 1792 | 1 |
| l1_l5_depth_concentration | 1 | 1792 | 382 | 1792 | 1 |
| l25_order_imbalance | 1 | 1792 | 148 | 1792 | 1 |
| microprice_l1_minus_mid_bps | 1 | 1792 | 1787 | 1792 | 0 |
| microprice_l25_minus_mid_bps | 1 | 1792 | 1785 | 1792 | 1 |
| spread_mean_lookback_bps | 1 | 1792 | 1703 | 1792 | 0 |
| trade_qty_sum_lookback | 1 | 1792 | 23 | 1792 | 0 |
| trade_qty_accel_lookback | 1 | 1792 | 23 | 1792 | 0 |
| minute_of_day | 1 | 1792 | 1005 | 1792 | 0 |
| source_event_mid_return_1 | 1 | 1792 | 1332 | 1792 | 0 |
| source_event_mid_return_3 | 1 | 1792 | 1336 | 1792 | 0 |
| source_event_mid_return_5 | 1 | 1792 | 1338 | 1792 | 0 |
| source_event_l1_ofi_1 | 1 | 1792 | 235 | 1792 | 0 |
| source_event_l1_ofi_3 | 1 | 1792 | 226 | 1792 | 0 |
| source_event_l25_ofi_1 | 1 | 1792 | 535 | 1792 | 1 |
| source_event_l25_ofi_3 | 1 | 1792 | 535 | 1792 | 1 |
| source_event_l25_replenishment_count_5 | 1 | 1792 | 6 | 1792 | 1 |
| source_event_l25_withdrawal_count_5 | 1 | 1792 | 5 | 1792 | 1 |
| source_event_spread_change_3_bps | 1 | 1792 | 1336 | 1792 | 0 |
| source_event_spread_vol_5_bps | 1 | 1792 | 1345 | 1792 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P470_PHASE469_PRECOMMIT_USED | True | 1 | 1 | hard |
| P470_MATRIX_ROWS_PRESENT | True | 1792 | >0 | hard |
| P470_FEATURE_COUNT_MATCHES_CONTRACT | True | 25 | 25 | hard |
| P470_L2_L5_FEATURE_COUNT_MATCHES_CONTRACT | True | 10 | 10 | hard |
| P470_ALL_FEATURES_FINITE | True | 1792 | 1792 | hard |
| P470_FEATURE_VARIATION_PRESENT | True | 25 | >=18 | hard |
| P470_L2_L5_FEATURE_VARIATION_PRESENT | True | 10 | >=8 | hard |
| P470_MOVE_CANDIDATES_PRESENT | True | 935 | >0 | hard |
| P470_TRAIN_AND_HOLDOUT_PRESENT | True | train=1176.0;holdout=616.0 | both>0 | hard |
| P470_BOTH_DIRECTIONS_PRESENT | True | long=943.0;short=838.0 | both>0 | hard |
| P470_SOURCE_EVENT_HISTORY_PRESENT | True | 1 | >=1 | hard |
| P470_NO_MODEL_FIT | True | matrix_only | no_model_fit | hard |
| P470_NO_STRATEGY_PNL | True | matrix_only | no_pnl | hard |
| P470_NO_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: Phase470 is matrix materialization only. Phase471 must precommit model fitting before any training, and strategy replay remains closed.

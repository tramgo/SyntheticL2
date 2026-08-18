# Phase468 Richer Past-Only L1-L5 Feature Matrix Materialization

Phase468 materializes the Phase467 richer past-only feature matrix. It does not fit a model and does not emit strategy P&L.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase468_richer_past_only_l1_l5_feature_matrix_complete | 1 | Phase468 matrix materialization completed |
| phase468_thesis_id | P468_MATERIALIZE_RICHER_PAST_ONLY_L1_L5_FEATURE_MATRIX | Matrix thesis |
| phase468_matrix_rows | 1792 | Matrix rows |
| phase468_feature_count | 20 | Feature count |
| phase468_l2_l5_feature_count | 9 | L2-L5 feature count |
| phase468_move_candidate_rows | 935 | Move candidates |
| phase468_train_rows | 1176 | Train rows |
| phase468_holdout_rows | 616 | Holdout rows |
| phase468_model_fit_generated | 0 | No model fit |
| phase468_strategy_pnl_generated | 0 | No strategy P&L |
| phase468_strategy_promotion_allowed | 0 | No promotion |
| phase468_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase468_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase468_phase469_allowed_next | 0 | Allows model precommit only if all gates pass |
| phase468_hard_gate_pass_rows | 11 | Passed hard gates |
| phase468_hard_gate_rows | 12 | Hard gates |
| phase468_next_best_action | repair_phase468_richer_matrix_materialization_before_model_precommit | Recommended next action |

## Matrix Summary

| metric | value |
| --- | --- |
| selected_files | 21 |
| files_present | 21 |
| matrix_rows | 1792 |
| feature_count | 20 |
| l2_l5_feature_count | 9 |
| move_candidate_rows | 935 |
| trade_dates | 64 |
| symbols | 7 |
| train_rows | 1176 |
| holdout_rows | 616 |
| train_move_candidate_rows | 626 |
| holdout_move_candidate_rows | 309 |
| long_rows | 943 |
| short_rows | 838 |

## Feature Quality

| feature_name | present | non_null_rows | unique_values | finite_rows |
| --- | --- | --- | --- | --- |
| recent_mid_return_bps | 1 | 1792 | 1 | 1792 |
| spread_bps | 1 | 1792 | 1703 | 1792 |
| l1_imbalance | 1 | 1792 | 1317 | 1792 |
| l25_imbalance | 1 | 1792 | 1584 | 1792 |
| volume_delta_lookback | 1 | 1792 | 23 | 1792 |
| l1_l5_bid_depth_slope | 1 | 1792 | 1265 | 1792 |
| l1_l5_ask_depth_slope | 1 | 1792 | 1318 | 1792 |
| l1_l5_depth_concentration | 1 | 1792 | 382 | 1792 |
| l25_order_imbalance | 1 | 1792 | 148 | 1792 |
| ofi_l1_lookback | 1 | 1792 | 1 | 1792 |
| ofi_l25_lookback | 1 | 1792 | 1 | 1792 |
| l25_replenishment_events | 1 | 1792 | 1 | 1792 |
| l25_withdrawal_events | 1 | 1792 | 1 | 1792 |
| microprice_l1_minus_mid_bps | 1 | 1792 | 1787 | 1792 |
| microprice_l25_minus_mid_bps | 1 | 1792 | 1785 | 1792 |
| spread_change_lookback_bps | 1 | 1792 | 1 | 1792 |
| spread_mean_lookback_bps | 1 | 1792 | 1703 | 1792 |
| trade_qty_sum_lookback | 1 | 1792 | 23 | 1792 |
| trade_qty_accel_lookback | 1 | 1792 | 23 | 1792 |
| minute_of_day | 1 | 1792 | 1005 | 1792 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P468_PHASE467_PRECOMMIT_USED | True | 1 | 1 | hard |
| P468_MATRIX_ROWS_PRESENT | True | 1792 | >0 | hard |
| P468_FEATURE_COUNT_MATCHES_CONTRACT | True | 20 | 20 | hard |
| P468_L2_L5_FEATURE_COUNT_MATCHES_CONTRACT | True | 9 | 9 | hard |
| P468_ALL_FEATURES_FINITE | True | 1792 | 1792 | hard |
| P468_FEATURE_VARIATION_PRESENT | False | 14 | >=15 | hard |
| P468_MOVE_CANDIDATES_PRESENT | True | 935 | >0 | hard |
| P468_TRAIN_AND_HOLDOUT_PRESENT | True | train=1176;holdout=616 | both>0 | hard |
| P468_BOTH_DIRECTIONS_PRESENT | True | long=943;short=838 | both>0 | hard |
| P468_NO_MODEL_FIT | True | matrix_only | no_model_fit | hard |
| P468_NO_STRATEGY_PNL | True | matrix_only | no_pnl | hard |
| P468_NO_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: Phase468 is matrix materialization only. Phase469 must precommit model fitting before any training, and strategy replay remains closed.

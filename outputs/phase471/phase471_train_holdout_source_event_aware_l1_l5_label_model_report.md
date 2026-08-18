# Phase471 Train/Holdout Source-Event-Aware L1-L5 Label Model

Phase471 trains and evaluates a class-weighted logistic model on the Phase470 source-event-aware feature-label matrix.

It does not create strategy P&L or acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase471_train_holdout_source_event_aware_l1_l5_label_model_complete | 1 | Phase471 model fit/evaluation completed |
| phase471_thesis_id | P471_TRAIN_HOLDOUT_SOURCE_EVENT_AWARE_L1_L5_LABEL_MODEL | Model fit thesis |
| phase471_primary_holdout_auc | 0.545578 | Primary holdout AUC |
| phase471_shuffled_holdout_auc | 0.42688 | Shuffled-label control AUC |
| phase471_auc_lift_vs_shuffled | 0.118698 | AUC lift versus shuffled-label control |
| phase471_primary_holdout_balanced_accuracy | 0.55205 | Primary holdout balanced accuracy |
| phase471_strategy_pnl_generated | 0 | No strategy P&L |
| phase471_strategy_promotion_allowed | 0 | No promotion |
| phase471_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase471_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase471_phase472_allowed_next | 1 | Allows score-to-signal replay only if all gates pass |
| phase471_hard_gate_pass_rows | 13 | Passed hard gates |
| phase471_hard_gate_rows | 13 | Hard gates |
| phase471_next_best_action | precommit_phase472_score_to_signal_replay_with_cost200_no_live | Recommended next action |

## Model Summary

| rows | positive_rate | auc | accuracy | balanced_accuracy | log_loss | tp | tn | fp | fn | model_id | train_rows | holdout_rows | primary_training_loss_path | shuffled_training_loss_path | l25_threshold_train_auc | l25_threshold_direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 309 | 0.556634 | 0.545578 | 0.553398 | 0.55205 | 0.696491 | 97 | 74 | 63 | 75 | P471_PRIMARY_CLASS_WEIGHTED_LOGISTIC_SOURCE_EVENT_L1_L5 | 626 | 309 | 0.694258;0.658590;0.653018;0.652522;0.652447 | 0.694079;0.683772;0.682154;0.682034;0.682014 | 0.511273 | positive |
| 309 | 0.556634 | 0.42688 | 0.446602 | 0.439038 | 0.715076 | 87 | 51 | 86 | 85 | P471_SHUFFLED_LABEL_CONTROL | 626 | 309 | 0.694258;0.658590;0.653018;0.652522;0.652447 | 0.694079;0.683772;0.682154;0.682034;0.682014 | 0.511273 | positive |
| 309 | 0.556634 | 0.478993 | 0.491909 | 0.491619 | 1.0791 | 85 | 67 | 70 | 87 | P471_L25_THRESHOLD_CONTROL | 626 | 309 | 0.694258;0.658590;0.653018;0.652522;0.652447 | 0.694079;0.683772;0.682154;0.682034;0.682014 | 0.511273 | positive |

## Primary Coefficients

| term | coefficient | train_mean | train_std | uses_l2_l5_depth |
| --- | --- | --- | --- | --- |
| intercept | 0.0170176 | 0 | 1 | 0 |
| spread_bps | -0.128766 | 2.09778 | 0.862394 | 0 |
| l1_imbalance | 0.0563168 | -0.179396 | 0.458249 | 0 |
| l25_imbalance | 0.0100787 | -0.145104 | 0.306345 | 1 |
| volume_delta_lookback | 0.0278318 | 329.329 | 67.4302 | 0 |
| l1_l5_bid_depth_slope | 0.00383506 | 131.49 | 54.532 | 1 |
| l1_l5_ask_depth_slope | 0.0598338 | 169.506 | 58.0458 | 1 |
| l1_l5_depth_concentration | -0.156462 | 0.117647 | 1.32306e-05 | 1 |
| l25_order_imbalance | 0.0121766 | -0.124011 | 0.265418 | 1 |
| microprice_l1_minus_mid_bps | 0.130965 | -0.197159 | 0.520587 | 0 |
| microprice_l25_minus_mid_bps | -0.0541316 | -0.428354 | 0.894634 | 1 |
| spread_mean_lookback_bps | -0.128769 | 2.09778 | 0.862394 | 0 |
| trade_qty_sum_lookback | 0.0278296 | 345.796 | 70.8017 | 0 |
| trade_qty_accel_lookback | 0.0278278 | 16.4665 | 3.37151 | 0 |
| minute_of_day | 0.012515 | 774.661 | 411.583 | 0 |
| source_event_mid_return_1 | -0.144304 | 0.0184396 | 2.14403 | 0 |
| source_event_mid_return_3 | 0.164205 | -0.127834 | 5.11907 | 0 |
| source_event_mid_return_5 | -0.186951 | 0.163913 | 10.936 | 0 |
| source_event_l1_ofi_1 | -0.045207 | 33.9489 | 228.6 | 0 |
| source_event_l1_ofi_3 | -0.0453824 | 29.0591 | 229.948 | 0 |
| source_event_l25_ofi_1 | 0.0838351 | 2.67412 | 217.961 | 1 |
| source_event_l25_ofi_3 | 0.0297919 | -11.3978 | 196.382 | 1 |
| source_event_l25_replenishment_count_5 | -0.280155 | 1.78435 | 1.33513 | 1 |
| source_event_l25_withdrawal_count_5 | 0.0562251 | 1.66613 | 1.2672 | 1 |
| source_event_spread_change_3_bps | 0.213518 | 5.25763e-05 | 0.00161028 | 0 |
| source_event_spread_vol_5_bps | 0.261666 | 0.00038658 | 0.000708788 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P471_PHASE470_MATRIX_USED | True | 1 | 1 | hard |
| P471_TRAIN_ROWS_PRESENT | True | 626 | >0 | hard |
| P471_HOLDOUT_ROWS_PRESENT | True | 309 | >0 | hard |
| P471_BOTH_CLASSES_TRAIN | True | 2 | 2 | hard |
| P471_BOTH_CLASSES_HOLDOUT | True | 2 | 2 | hard |
| P471_FULL_DEPTH_FEATURES_USED | True | 10 | >=10 | hard |
| P471_SOURCE_EVENT_FEATURES_USED | True | 11 | >=11 | hard |
| P471_HOLDOUT_AUC_GE_053 | True | 0.545578 | >=0.53 | hard |
| P471_AUC_LIFT_VS_SHUFFLED_GE_002 | True | 0.118698 | >=0.02 | hard |
| P471_BALANCED_ACCURACY_GE_052 | True | 0.55205 | >=0.52 | hard |
| P471_PRIMARY_NOT_WORSE_THAN_L25_THRESHOLD | True | primary=0.5455780003395009;threshold=0.4789933797317943 | primary>=threshold | hard |
| P471_NO_STRATEGY_PNL | True | model_fit_only | no_pnl | hard |
| P471_NO_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: a predictive label model is not a strategy. Any score-to-order replay must be separately precommitted with costs, latency, slippage and risk.

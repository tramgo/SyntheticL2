# Phase465 Train/Holdout Past-Only L1-L5 Label Model

Phase465 trains and evaluates the Phase464 frozen past-only model contract. It does not create strategy P&L or acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase465_train_holdout_past_only_l1_l5_label_model_complete | 1 | Phase465 model fit/evaluation completed |
| phase465_thesis_id | P465_TRAIN_HOLDOUT_PAST_ONLY_L1_L5_LABEL_MODEL | Model fit thesis |
| phase465_primary_holdout_auc | 0.557758 | Primary holdout AUC |
| phase465_shuffled_holdout_auc | 0.543117 | Shuffled-label control AUC |
| phase465_auc_lift_vs_shuffled | 0.014641 | AUC lift versus shuffled-label control |
| phase465_primary_holdout_balanced_accuracy | 0.555572 | Primary holdout balanced accuracy |
| phase465_strategy_pnl_generated | 0 | No strategy P&L |
| phase465_strategy_promotion_allowed | 0 | No promotion |
| phase465_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase465_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase465_phase466_allowed_next | 0 | Allows precommitted score-to-signal replay only if all gates pass |
| phase465_hard_gate_pass_rows | 12 | Passed hard gates |
| phase465_hard_gate_rows | 13 | Hard gates |
| phase465_next_best_action | interpret_phase465_predictive_model_failure_or_expand_past_only_features_before_replay | Recommended next action |

## Model Summary

| rows | positive_rate | auc | accuracy | balanced_accuracy | log_loss | tp | tn | fp | fn | model_id | train_rows | holdout_rows | primary_training_loss_path | shuffled_training_loss_path | l25_threshold_train_auc | l25_threshold_direction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 309 | 0.556634 | 0.557758 | 0.563107 | 0.555572 | 0.686736 | 107 | 67 | 70 | 65 | P465_PRIMARY_CLASS_WEIGHTED_LOGISTIC_L1_L5 | 626 | 309 | 0.694300;0.686997;0.685899;0.685891;0.685891 | 0.692944;0.690549;0.690188;0.690183;0.690183 | 0.511273 | positive |
| 309 | 0.556634 | 0.543117 | 0.527508 | 0.530279 | 0.690328 | 87 | 76 | 61 | 85 | P465_SHUFFLED_LABEL_CONTROL | 626 | 309 | 0.694300;0.686997;0.685899;0.685891;0.685891 | 0.692944;0.690549;0.690188;0.690183;0.690183 | 0.511273 | positive |
| 309 | 0.556634 | 0.478993 | 0.491909 | 0.491619 | 1.0791 | 85 | 67 | 70 | 87 | P465_L25_THRESHOLD_CONTROL | 626 | 309 | 0.694300;0.686997;0.685899;0.685891;0.685891 | 0.692944;0.690549;0.690188;0.690183;0.690183 | 0.511273 | positive |

## Primary Coefficients

| term | coefficient | train_mean | train_std |
| --- | --- | --- | --- |
| intercept | 0.00226169 | 0 | 1 |
| recent_mid_return_bps | -5.15189e-07 | 0 | 1 |
| spread_bps | -0.196596 | 2.09778 | 0.862394 |
| l1_imbalance | 0.108482 | -0.179396 | 0.458249 |
| l25_imbalance | -0.0407709 | -0.145104 | 0.306345 |
| volume_delta_lookback | 0.1137 | 329.329 | 67.4302 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P465_PHASE464_PRECOMMIT_USED | True | 1 | 1 | hard |
| P465_TRAIN_ROWS_PRESENT | True | 626 | >0 | hard |
| P465_HOLDOUT_ROWS_PRESENT | True | 309 | >0 | hard |
| P465_BOTH_CLASSES_TRAIN | True | 2 | 2 | hard |
| P465_BOTH_CLASSES_HOLDOUT | True | 2 | 2 | hard |
| P465_FULL_DEPTH_FEATURE_USED | True | l25_imbalance | l25_imbalance | hard |
| P465_FORBIDDEN_FEATURES_EXCLUDED | True |  | empty | hard |
| P465_HOLDOUT_AUC_GE_053 | True | 0.557758 | >=0.53 | hard |
| P465_AUC_LIFT_VS_SHUFFLED_GE_002 | False | 0.014641 | >=0.02 | hard |
| P465_BALANCED_ACCURACY_GE_052 | True | 0.555572 | >=0.52 | hard |
| P465_PRIMARY_NOT_WORSE_THAN_L25_THRESHOLD | True | primary=0.55775759633339;threshold=0.4789933797317943 | primary>=threshold | hard |
| P465_NO_STRATEGY_PNL | True | model_fit_only | no_pnl | hard |
| P465_NO_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: a predictive label model is not a strategy. Any score-to-order replay must be separately precommitted with costs, latency, slippage and risk.

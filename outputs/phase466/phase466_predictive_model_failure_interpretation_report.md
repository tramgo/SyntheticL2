# Phase466 Predictive Model Failure Interpretation

Phase466 interprets Phase465 and blocks score-to-signal replay from the weak five-feature model.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase466_predictive_model_failure_interpretation_complete | 1 | Phase466 interpretation completed |
| phase466_thesis_id | P466_PREDICTIVE_MODEL_FAILURE_INTERPRETATION | Interpretation thesis |
| phase466_selected_verdict | P466_WEAK_PREDICTIVE_SMELL_NOT_REPLAYABLE | Selected verdict |
| phase466_score_to_signal_replay_allowed | 0 | No replay from Phase465 model |
| phase466_same_five_feature_model_rescue_allowed | 0 | No same-model rescue |
| phase466_richer_past_only_feature_precommit_allowed | 1 | Allows Phase467 precommit only |
| phase466_strategy_pnl_generated | 0 | No strategy P&L |
| phase466_strategy_promotion_allowed | 0 | No promotion |
| phase466_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase466_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase466_hard_gate_pass_rows | 9 | Passed hard gates |
| phase466_hard_gate_rows | 9 | Hard gates |
| phase466_next_best_action | precommit_phase467_richer_past_only_l1_l5_feature_matrix_before_any_replay | Recommended next action |

## Decision Ledger

| decision_id | decision_value | description |
| --- | --- | --- |
| selected_verdict | P466_WEAK_PREDICTIVE_SMELL_NOT_REPLAYABLE | Phase465 has weak predictive signal but fails the shuffled-label lift gate. |
| primary_holdout_auc | 0.557758 | Primary holdout AUC. |
| primary_holdout_balanced_accuracy | 0.555572 | Primary holdout balanced accuracy. |
| shuffled_holdout_auc | 0.543117 | Shuffled-label control holdout AUC. |
| auc_lift_vs_shuffled | 0.014640977762688911 | Primary AUC lift versus shuffled-label control. |
| l25_threshold_holdout_auc | 0.478993 | Single L2-L5 threshold control holdout AUC. |
| failed_gate_count | 1 | Failed Phase465 hard gates. |
| failed_gate_ids | P465_AUC_LIFT_VS_SHUFFLED_GE_002 | Failed Phase465 gate ids. |
| score_to_signal_replay_allowed | 0 | Phase465 did not allow Phase466 replay. |
| same_five_feature_model_rescue_allowed | 0 | Do not retune the same weak feature set after seeing holdout controls. |
| materially_richer_past_only_features_allowed | 1 | A new precommitted matrix may add richer past-only L1-L5 window features. |
| strategy_promotion_allowed | 0 | No promotion. |
| paper_or_live_acceptance_allowed | 0 | No paper/live. |
| deployable_profitability_claim_allowed | 0 | No deployable claim. |

## Richer Past-Only Feature Plan

| feature_family | timestamp_rule | description | uses_l2_l5_depth |
| --- | --- | --- | --- |
| depth_curve_shape | past_only_window | Use L1-L5 bid/ask ladder slope, convexity and depth concentration over the lookback window. | 1 |
| ofi_and_depth_churn | past_only_window | Use signed changes in L1-L5 quantities and replenishment/withdrawal counts before entry. | 1 |
| microprice_pressure | past_only_window | Use L1 and L2-L5 microprice displacement from mid, computed before entry. | 1 |
| spread_regime_context | past_only_window | Use rolling spread percentile, spread compression/expansion and tight/loose regime flags. | 0 |
| volume_acceleration | past_only_window | Use rolling trade-volume acceleration and volume imbalance proxies before entry. | 0 |
| time_of_day_context | known_before_entry | Use open/midday/close bucket only, not future session outcomes. | 0 |
| symbol_normalization | known_before_entry | Normalize features within symbol/train split to avoid large-price or large-volume domination. | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P466_PHASE465_COMPLETE | True | 1 | 1 | hard |
| P466_PHASE465_REPLAY_NOT_ALLOWED | True | 0 | 0 | hard |
| P466_REQUIRED_FAILED_GATE_IDENTIFIED | True | P465_AUC_LIFT_VS_SHUFFLED_GE_002 | P465_AUC_LIFT_VS_SHUFFLED_GE_002 | hard |
| P466_EXACTLY_ONE_PREDICTIVE_GATE_FAILED | True | 1 | 1 | hard |
| P466_REPLAY_REJECTED | True | 0 | 0 | hard |
| P466_SAME_MODEL_RESCUE_REJECTED | True | 0 | 0 | hard |
| P466_RICHER_PAST_ONLY_FEATURES_SELECTED | True | 1 | 1 | hard |
| P466_NO_STRATEGY_PNL | True | interpretation_only | no_pnl | hard |
| P466_NO_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: Phase466 is interpretation only. A richer feature matrix must be precommitted before any additional model fit or P&L replay.

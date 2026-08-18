# Phase464 Past-Only L1-L5 Feature-Model Precommit

Phase464 freezes a model-fit contract over Phase463 actual-move labels. It does not train a model, emit strategy P&L, or make any acceptance claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase464_past_only_l1_l5_feature_model_precommit_complete | 1 | Phase464 precommit completed |
| phase464_thesis_id | P464_PAST_ONLY_L1_L5_FEATURE_MODEL_PRECOMMIT | Precommit thesis |
| phase464_model_family_id | class_weighted_regularized_logistic_direction_model_with_tree_baseline_diagnostic | Selected model family |
| phase464_train_rows | 1176 | Training rows |
| phase464_holdout_rows | 616 | Holdout rows |
| phase464_train_move_candidate_rows | 626 | Training move candidates |
| phase464_holdout_move_candidate_rows | 309 | Holdout move candidates |
| phase464_execution_results_generated | 0 | Precommit only |
| phase464_strategy_pnl_generated | 0 | No strategy P&L |
| phase464_strategy_promotion_allowed | 0 | No promotion |
| phase464_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase464_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase464_phase465_allowed_next | 1 | Allows model fit/evaluation only if all gates pass |
| phase464_hard_gate_pass_rows | 13 | Passed hard gates |
| phase464_hard_gate_rows | 13 | Hard gates |
| phase464_next_best_action | run_phase465_train_holdout_past_only_l1_l5_label_model_no_strategy_pnl | Recommended next action |

## Input Evidence

| evidence_id | observed_value | description |
| --- | --- | --- |
| phase463_phase464_allowed_next | 1 | Phase463 allowance |
| phase463_move_candidate_rows | 935.0 | Phase463 candidates |
| phase463_long_label_rows | 943.0 | Phase463 long labels |
| phase463_short_label_rows | 838.0 | Phase463 short labels |
| ledger_rows | 1792 | Rows in Phase463 ledger |
| train_rows | 1176 | Training rows |
| holdout_rows | 616 | Holdout rows |
| train_move_candidates | 626 | Training move candidates |
| holdout_move_candidates | 309 | Holdout move candidates |
| train_dates | 42 | Training trade dates |
| holdout_dates | 22 | Holdout trade dates |
| symbols | 7 | Ledger symbol breadth |

## Split Summary

| phase464_split | rows | move_candidate_rows | long_rows | short_rows | trade_dates | symbols |
| --- | --- | --- | --- | --- | --- | --- |
| holdout | 616 | 309 | 311 | 300 | 22 | 7 |
| train | 1176 | 626 | 632 | 538 | 42 | 7 |

## Feature Contract

| feature_name | allowed_as_model_input | timestamp_rule | source_definition | full_depth_l2_l5_feature |
| --- | --- | --- | --- | --- |
| recent_mid_return_bps | 1 | must be observable at or before entry row | entry row minus prior lookback mid price; computed before/at entry | 0 |
| spread_bps | 1 | must be observable at or before entry row | best ask minus best bid at entry | 0 |
| l1_imbalance | 1 | must be observable at or before entry row | top-of-book quantity imbalance at entry | 0 |
| l25_imbalance | 1 | must be observable at or before entry row | levels 2-5 bid/ask quantity imbalance at entry | 1 |
| volume_delta_lookback | 1 | must be observable at or before entry row | entry volume minus prior lookback volume | 0 |
| forward_return_bps | 0 | future label only; forbidden as predictor | computed using exit row after horizon | 0 |
| abs_forward_return_bps | 0 | future label only; forbidden as predictor | computed using exit row after horizon | 0 |
| label_side | 0 | future label only; forbidden as predictor | computed using exit row after horizon | 0 |
| move_candidate | 0 | future label only; forbidden as predictor | computed using exit row after horizon | 0 |

## Frozen Phase465 Model Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| phase464_thesis_id | P464_PAST_ONLY_L1_L5_FEATURE_MODEL_PRECOMMIT | Precommit thesis |
| model_family_id | class_weighted_regularized_logistic_direction_model_with_tree_baseline_diagnostic | Allowed model family |
| primary_model | class_weighted_l2_regularized_logistic_regression | Simple regularized baseline for direction/move labels |
| diagnostic_baseline | depth_feature_threshold_and_shuffled_label_controls | Controls only, not promotion |
| training_split | 2026-01;2026-02 | Training months |
| holdout_split | 2026-03 | Untouched holdout month |
| allowed_features | recent_mid_return_bps;spread_bps;l1_imbalance;l25_imbalance;volume_delta_lookback | Feature columns allowed as inputs |
| required_full_depth_features | l25_imbalance | L2-L5 feature columns required |
| forbidden_feature_columns | forward_return_bps;abs_forward_return_bps;label_side;move_candidate;exit_price;exit_row | Leakage columns forbidden as predictors |
| label_columns | forward_return_bps;abs_forward_return_bps;label_side;move_candidate | Future labels retained only as targets |
| minimum_train_rows | 500 | Training-row floor |
| minimum_holdout_rows | 200 | Holdout-row floor |
| minimum_train_move_candidates | 250 | Train candidate floor |
| minimum_holdout_move_candidates | 100 | Holdout candidate floor |
| split_summary_hash | 39509801689bee33752302943e65acc4ea4a015f2ca6a34d1387b229c14eccb5 | Frozen split summary hash |
| feature_contract_hash | 86ed4fd9b6b7e35fbe386251eeea424361356c04885cea60ebe0554a078ab6c6 | Frozen feature contract hash |
| phase465_allowed_next | 1 | Allows model fit/evaluation only |
| strategy_pnl_allowed | 0 | No strategy P&L in Phase464/465 |
| strategy_promotion_allowed | 0 | No promotion |
| paper_or_live_acceptance_allowed | 0 | No paper/live |
| deployable_profitability_claim_allowed | 0 | No deployable claim |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P464_PHASE463_PRECOMMIT_USED | True | 1 | 1 | hard |
| P464_LEDGER_ROWS_PRESENT | True | 1792 | >0 | hard |
| P464_MOVE_CANDIDATES_PRESENT | True | 935.0 | >0 | hard |
| P464_TRAIN_SPLIT_ROWS | True | 1176 | >=500 | hard |
| P464_HOLDOUT_SPLIT_ROWS | True | 616 | >=200 | hard |
| P464_TRAIN_MOVE_CANDIDATES | True | 626 | >=250 | hard |
| P464_HOLDOUT_MOVE_CANDIDATES | True | 309 | >=100 | hard |
| P464_FEATURE_COLUMNS_PRESENT | True | l1_imbalance;l25_imbalance;recent_mid_return_bps;spread_bps;volume_delta_lookback | recent_mid_return_bps;spread_bps;l1_imbalance;l25_imbalance;volume_delta_lookback | hard |
| P464_FULL_DEPTH_L2_L5_FEATURE_REQUIRED | True | l25_imbalance | >=1 L2-L5 feature | hard |
| P464_FORBIDDEN_LABELS_NOT_MODEL_INPUTS | True |  | empty | hard |
| P464_BOTH_DIRECTIONS_IN_TRAIN_AND_HOLDOUT | True | train_long=632;train_short=538;holdout_long=311;holdout_short=300 | all >0 | hard |
| P464_NO_STRATEGY_PNL | True | precommit_only | no_pnl | hard |
| P464_NO_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: future label columns are targets only. Phase465 may train/evaluate a past-only model, but strategy replay and P&L remain closed until separately precommitted.

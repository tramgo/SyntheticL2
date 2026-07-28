# Phase196 Expanded Feature Model Search

Generated UTC: 2026-07-28T19:47:21.737712+00:00

Phase196 expands from threshold grids to train-fitted linear feature families.
It preserves the Phase195 discipline: train-only fitting, validation-extension rejection, no untouched test replay, no promotion, and no paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase196_model_grid_rows | 64 | Expanded feature/model rows |
| phase196_train_selected_model_rows | 0 | Train-selected model rows |
| phase196_model_decision_rows | 0 | Model decision rows |
| phase196_passing_extension_gate_models | 0 | Models passing extension gates |
| phase196_best_model_id |  | Top model by extension screen |
| phase196_best_min_extension_net_bps |  | Best model minimum extension net bps |
| phase196_best_date_positive_fraction |  | Best model date-positive fraction |
| phase196_best_symbol_positive_fraction |  | Best model symbol-positive fraction |
| phase196_gate_rows | 6 | Gates evaluated |
| phase196_hard_gate_rows | 6 | Hard gates evaluated |
| phase196_hard_gate_pass_rows | 6 | Hard gates passed |
| phase196_expanded_model_search_complete | 1 | 1 means Phase196 completed |
| phase196_test_replay_allowed_next | 0 | No test replay opened |
| phase196_promotion_allowed | 0 | No promotion opened |
| phase196_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase196_forbidden_outputs | test_result;test_replay_execution;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim | Outputs forbidden in this phase |
| phase196_next_best_action | expand_non_receive_flow_features_or_pause_this_branch_no_test | Recommended next milestone |

## Top Model Decisions

_No rows._

## Train-selected Models

_No rows._

## Validation Extension Summary

_No rows._

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P196_PHASE195_COMPLETE | 1 | phase195_redesign_search_complete=1 | hard |
| P196_TRAIN_ONLY_FIT | 1 | train_summary_rows=128; selected_model_rows=0 | hard |
| P196_EVALUATION_EXCLUDES_TEST | 1 | test_partitions_used=0 | hard |
| P196_EXTENSION_BREADTH_GATES_APPLIED | 1 | selected_model_rows=0; decision_rows=0 | hard |
| P196_PASSING_MODEL_RECORDED | 1 | passing_models=0 | hard |
| P196_NO_TEST_REPLAY_OR_PROMOTION | 1 | test_replay_allowed_next=0; promotion_allowed=0 | hard |

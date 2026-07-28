# Phase198 Non-Receive-Flow Context Model Search

Generated UTC: 2026-07-28T20:06:09.210894+00:00

Phase198 runs a train/validation-only context model search using Phase197 feature families.
It excludes untouched test replay and does not create orders, fills, P&L, promotion or paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase198_model_grid_rows | 88 | Non-receive-flow context model rows |
| phase198_train_selected_model_rows | 0 | Train-selected model rows |
| phase198_model_decision_rows | 0 | Model decision rows |
| phase198_passing_extension_gate_models | 0 | Models passing extension gates |
| phase198_best_model_id |  | Top model by extension screen |
| phase198_best_feature_family |  | Top model feature family |
| phase198_best_min_extension_net_bps |  | Best model minimum validation/extension net bps |
| phase198_best_date_positive_fraction |  | Best model date-positive fraction |
| phase198_best_symbol_positive_fraction |  | Best model symbol-positive fraction |
| phase198_gate_rows | 6 | Gates evaluated |
| phase198_hard_gate_rows | 6 | Hard gates evaluated |
| phase198_hard_gate_pass_rows | 6 | Hard gates passed |
| phase198_context_model_search_complete | 1 | 1 means Phase198 completed |
| phase198_test_replay_allowed_next | 0 | No test replay opened |
| phase198_promotion_allowed | 0 | No promotion opened |
| phase198_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase198_forbidden_outputs | test_result;test_replay_execution;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim | Outputs forbidden in this phase |
| phase198_next_best_action | expand_or_pause_non_receive_flow_context_branch_no_test | Recommended next milestone |

## Top Model Decisions

_No rows._

## Train-selected Models

_No rows._

## Validation Extension Summary

_No rows._

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P198_PHASE197_COMPLETE | 1 | phase197_precommit_complete=1; ready_feature_families=5 | hard |
| P198_TRAIN_ONLY_FIT_AND_SELECTION | 1 | train_summary_rows=176; selected_model_rows=0 | hard |
| P198_EVALUATION_EXCLUDES_TEST | 1 | test_partitions_used=0 | hard |
| P198_EXTENSION_BREADTH_GATES_APPLIED | 1 | selected_model_rows=0; decision_rows=0 | hard |
| P198_PASSING_MODEL_RECORDED | 1 | passing_models=0 | hard |
| P198_NO_TEST_REPLAY_OR_PROMOTION | 1 | test_replay_allowed_next=0; promotion_allowed=0 | hard |

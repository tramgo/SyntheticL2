# Phase220 Event-only Model-fit Validation Interpretation

Generated UTC: 2026-07-28T22:09:54.948528+00:00

Phase220 interprets Phase219 validation dry-run metrics against base-rate and shuffled controls.
It opens only a Phase221 precommit-or-stop decision for the passing candidates; no replay, sealed test, promotion, paper/live, or profitability claim is opened.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase220_interpretation_rows | 21 | Validation interpretation rows |
| phase220_passing_candidate_rows | 5 | Passing validation candidate rows |
| phase220_candidate_family_rows | 1 | Candidate model families |
| phase220_best_mse_improvement_vs_base | 0.0100934 | Best validation MSE improvement versus base rate |
| phase220_best_improvement_vs_shuffle | 0.01073 | Best validation MSE improvement versus shuffled control |
| phase220_best_validation_correlation | 0.220575 | Best validation correlation |
| phase220_phase221_work_order_rows | 1 | Phase221 work-order rows |
| phase220_forbidden_execution_rows | 11 | Forbidden execution rows |
| phase220_gate_rows | 6 | Gates evaluated |
| phase220_hard_gate_rows | 6 | Hard gates evaluated |
| phase220_hard_gate_pass_rows | 6 | Hard gates passed |
| phase220_event_only_model_fit_validation_interpretation_complete | 1 | 1 means Phase220 completed |
| phase220_candidate_opened_for_phase221_precommit | 1 | 1 means Phase221 may precommit or stop a signal/replay contract |
| phase220_strategy_replay_allowed | 0 | No strategy replay opened |
| phase220_test_replay_allowed_next | 0 | No test replay opened |
| phase220_promotion_allowed | 0 | No promotion opened |
| phase220_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase220_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase220_forbidden_outputs | strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export | Outputs forbidden in this phase |
| phase220_next_best_action | run_phase221_event_only_signal_replay_precommit_or_stop_no_replay_no_test | Recommended next milestone |

## Validation Interpretation

| phase219_model_fit_id | phase218_model_spec_id | model_family | target_label | horizon_sec | train_rows_used_for_fit | test_rows_used | strategy_replay_allowed | promotion_allowed | split_role | rows | positive_rate | prediction_mean | mse | base_rate_mse | mse_improvement_vs_base | binary_accuracy | correlation | base_control_mse | shuffle_control_mse | improvement_vs_shuffle | passes_min_rows | passes_base_improvement | passes_shuffle_improvement | passes_correlation | interpretation_pass | candidate_opened_for_phase221_precommit | test_replay_allowed_next | profitability_claim_allowed | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.378231 | 0.356435 | 0.225079 | 0.235172 | 0.0100934 | 0.622405 | 0.220575 | 0.235172 | 0.235809 | 0.01073 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | phase221_precommit_candidate |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.622247 | 0.607013 | 0.226014 | 0.235056 | 0.00904191 | 0.629276 | 0.20407 | 0.235056 | 0.235916 | 0.00990177 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | phase221_precommit_candidate |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.33224 | 0.32949 | 0.216399 | 0.221857 | 0.00545801 | 0.66776 | 0.160105 | 0.221857 | 0.221826 | 0.00542716 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | phase221_precommit_candidate |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.340382 | 0.331609 | 0.219307 | 0.224522 | 0.00521501 | 0.65956 | 0.157466 | 0.224522 | 0.224275 | 0.00496794 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | phase221_precommit_candidate |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.193375 | 0.176223 | 0.152628 | 0.155981 | 0.00335315 | 0.806625 | 0.159248 | 0.155981 | 0.156552 | 0.00392368 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | phase221_precommit_candidate |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.184824 | 0.181165 | 0.14811 | 0.150664 | 0.00255374 | 0.815176 | 0.132913 | 0.150664 | 0.150533 | 0.0024228 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_up_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.33224 | 0.274906 | 0.219823 | 0.221857 | 0.00203356 | 0.66776 | 0.157643 | 0.221857 | 0.221941 | 0.00211828 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_up_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.33224 | 0.265815 | 0.221588 | 0.221857 | 0.000268159 | 0.66776 | 0.150913 | 0.221857 | 0.22216 | 0.000571276 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_up_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.184824 | 0.140025 | 0.150565 | 0.150664 | 9.87065e-05 | 0.815176 | 0.119193 | 0.150664 | 0.150576 | 1.11174e-05 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_up_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.184824 | 0.134141 | 0.150812 | 0.150664 | -0.000148273 | 0.815176 | 0.133777 | 0.150664 | 0.150594 | -0.000217965 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 15 | 1792 | 0 | 0 | 0 | validation | 845 | 0.693491 | 0.660673 | 0.214127 | 0.212561 | -0.00156582 | 0.693491 | 0.0267188 | 0.212561 | 0.21321 | -0.000916822 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_down_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.193375 | 0.121891 | 0.157764 | 0.155981 | -0.00178327 | 0.806625 | 0.153263 | 0.155981 | 0.156819 | -0.000945596 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_down_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.193375 | 0.125369 | 0.158085 | 0.155981 | -0.00210376 | 0.806625 | 0.132243 | 0.155981 | 0.156808 | -0.00127684 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_down_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.340382 | 0.248742 | 0.227981 | 0.224522 | -0.00345884 | 0.659618 | 0.152627 | 0.224522 | 0.224407 | -0.00357352 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_down_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.340382 | 0.255113 | 0.22883 | 0.224522 | -0.00430795 | 0.659618 | 0.116438 | 0.224522 | 0.224651 | -0.00417887 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_vol_expansion_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.378231 | 0.249476 | 0.242535 | 0.235172 | -0.00736265 | 0.621801 | 0.206414 | 0.235172 | 0.236355 | -0.00617994 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.378231 | 0.247155 | 0.242655 | 0.235172 | -0.00748324 | 0.621801 | 0.212958 | 0.235172 | 0.236384 | -0.00627112 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.622247 | 0.472221 | 0.248532 | 0.235056 | -0.0134762 | 0.550082 | 0.202966 | 0.235056 | 0.23512 | -0.0134118 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_vol_expansion_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.622247 | 0.475241 | 0.248548 | 0.235056 | -0.0134922 | 0.545513 | 0.190846 | 0.235056 | 0.235622 | -0.0129263 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_vol_expansion_conditional_label | 15 | 1792 | 0 | 0 | 0 | validation | 845 | 0.693491 | 0.4954 | 0.250753 | 0.212561 | -0.038192 | 0.485207 | 0.0705274 | 0.212561 | 0.211617 | -0.0391359 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_vol_expansion_conditional_label | 15 | 1792 | 0 | 0 | 0 | validation | 845 | 0.693491 | 0.490068 | 0.25383 | 0.212561 | -0.041269 | 0.486391 | 0.0468028 | 0.212561 | 0.211661 | -0.0421694 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_validation_edge_or_control_failure |

## Model Family Summary

| model_family | validation_rows | passing_validation_rows | best_mse_improvement_vs_base | best_improvement_vs_shuffle | best_correlation | candidate_family_for_phase221 | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| class_weighted_regularized_logistic_classification | 7 | 0 | 0.00203356 | 0.00211828 | 0.206414 | 0 | 0 | 0 |
| event_only_sparse_classification_diagnostic | 7 | 0 | 0.000268159 | 0.000571276 | 0.212958 | 0 | 0 | 0 |
| low_depth_tree_or_stump_diagnostic | 7 | 5 | 0.0100934 | 0.01073 | 0.220575 | 1 | 0 | 0 |

## Phase221 Work Order

| phase221_work_order_id | work_order | passing_candidate_rows | candidate_model_fit_ids | allowed_next_scope | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P221_EVENT_ONLY_SIGNAL_REPLAY_PRECOMMIT_OR_STOP | Decide whether the Phase220 passing validation candidates can be converted into a replay precommit contract, or stop/redesign without replay. | 5 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s;P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s;P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s;P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s;P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | signal_replay_precommit_decision_only_no_replay_no_test | 0 | 0 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase220 | allowed_in_phase220 | rationale |
| --- | --- | --- | --- |
| strategy_replay | 0 | 0 | Phase220 interprets validation metrics only and emits no replay, test, promotion, P&L, prediction export, or profitability artifact. |
| test_replay_execution | 0 | 0 | Phase220 interprets validation metrics only and emits no replay, test, promotion, P&L, prediction export, or profitability artifact. |
| test_result | 0 | 0 | Phase220 interprets validation metrics only and emits no replay, test, promotion, P&L, prediction export, or profitability artifact. |
| promotion | 0 | 0 | Phase220 interprets validation metrics only and emits no replay, test, promotion, P&L, prediction export, or profitability artifact. |
| paper_live_acceptance | 0 | 0 | Phase220 interprets validation metrics only and emits no replay, test, promotion, P&L, prediction export, or profitability artifact. |
| order_arrival | 0 | 0 | Phase220 interprets validation metrics only and emits no replay, test, promotion, P&L, prediction export, or profitability artifact. |
| fill_model | 0 | 0 | Phase220 interprets validation metrics only and emits no replay, test, promotion, P&L, prediction export, or profitability artifact. |
| pnl_replay | 0 | 0 | Phase220 interprets validation metrics only and emits no replay, test, promotion, P&L, prediction export, or profitability artifact. |
| profitability_claim | 0 | 0 | Phase220 interprets validation metrics only and emits no replay, test, promotion, P&L, prediction export, or profitability artifact. |
| threshold_widening | 0 | 0 | Phase220 interprets validation metrics only and emits no replay, test, promotion, P&L, prediction export, or profitability artifact. |
| row_level_prediction_export | 0 | 0 | Phase220 interprets validation metrics only and emits no replay, test, promotion, P&L, prediction export, or profitability artifact. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P220_PHASE219_COMPLETE | True | phase219_complete=1 | hard |
| P220_VALIDATION_INTERPRETATION_RECORDED | True | validation_rows=21 | hard |
| P220_PASSING_CANDIDATES_RECORDED | True | passing_rows=5 | hard |
| P220_CANDIDATE_FAMILY_RECORDED | True | candidate_families=1 | hard |
| P220_PHASE221_WORK_ORDER_RECORDED | True | work_order_rows=1 | hard |
| P220_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; replay_flags=0 | hard |

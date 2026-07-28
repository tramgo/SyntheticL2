# Phase211 Model-fit Validation Interpretation

Generated UTC: 2026-07-28T21:17:07.162841+00:00

Phase211 interprets Phase210 aggregate validation metrics against shuffled-target controls.
It does not use sealed test data, run replay, export row-level predictions, emit P&L, promote candidates, or make profitability claims.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase211_interpretation_rows | 12 | Model/horizon interpretation rows |
| phase211_family_summary_rows | 3 | Model-family summary rows |
| phase211_passing_interpretation_rows | 0 | Rows passing the control-aware interpretation screen |
| phase211_best_mse_improvement_pct_vs_control | 0.954266 | Best validation MSE improvement versus shuffled-target control |
| phase211_best_abs_validation_correlation | 0.143592 | Best absolute validation correlation |
| phase211_best_binary_accuracy_lift_vs_control | 0.0116096 | Best binary accuracy lift versus shuffled-target control |
| phase211_decision_rows | 1 | Decision ledger rows |
| phase211_forbidden_execution_rows | 11 | Forbidden execution rows |
| phase211_gate_rows | 6 | Gates evaluated |
| phase211_hard_gate_rows | 6 | Hard gates evaluated |
| phase211_hard_gate_pass_rows | 6 | Hard gates passed |
| phase211_model_fit_validation_interpretation_complete | 1 | 1 means Phase211 completed |
| phase211_candidate_opened_for_replay | 0 | No candidate opened for replay |
| phase211_strategy_replay_allowed | 0 | No strategy replay opened |
| phase211_test_replay_allowed_next | 0 | No test replay opened |
| phase211_promotion_allowed | 0 | No promotion opened |
| phase211_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase211_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase211_forbidden_outputs | strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export | Outputs forbidden in this phase |
| phase211_next_best_action | run_phase212_model_family_closure_or_redesign_precommit_no_replay_no_test | Recommended next milestone |

## Validation Interpretation

| phase211_interpretation_id | phase210_model_fit_id | phase209_model_spec_id | target_label | horizon_sec | validation_rows | validation_mse | control_validation_mse | mse_improvement_pct_vs_control | validation_correlation | validation_binary_accuracy | control_validation_binary_accuracy | binary_accuracy_lift_vs_control | mse_improvement_pass | correlation_pass | binary_accuracy_lift_pass | interpretation_pass | verdict | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P211_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | 363786 | 0.166626 | 0.16304 | -2.19983 | 0.0738069 | 0.795069 | 0.795072 | -2.74887e-06 | 0 | 0 | 0 | 0 | rejected_control_like_or_worse_mse | 0 | 0 | 0 | 0 | 0 |
| P211_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | 137477 | 0.211775 | 0.212105 | 0.155917 | 0.110658 | 0.695127 | 0.69512 | 7.27394e-06 | 0 | 1 | 0 | 0 | rejected_control_like_or_worse_mse | 0 | 0 | 0 | 0 | 0 |
| P211_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | 48064 | 0.239103 | 0.241406 | 0.954266 | 0.104053 | 0.595061 | 0.595019 | 4.16112e-05 | 0 | 1 | 0 | 0 | rejected_control_like_or_worse_mse | 0 | 0 | 0 | 0 | 0 |
| P211_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | 12059 | 0.247855 | 0.249415 | 0.625583 | 0.0748526 | 0.539597 | 0.527987 | 0.0116096 | 0 | 0 | 1 | 0 | rejected_control_like_or_worse_mse | 0 | 0 | 0 | 0 | 0 |
| P211_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | 363786 | 8790.69 | 8797.31 | 0.0753144 | 0.033177 |  |  | 0 | 0 | 0 | 1 | 0 | rejected_control_like_or_worse_mse | 0 | 0 | 0 | 0 | 0 |
| P211_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | 137477 | 23269.5 | 23275.6 | 0.0261344 | 0.0297601 |  |  | 0 | 0 | 0 | 1 | 0 | rejected_control_like_or_worse_mse | 0 | 0 | 0 | 0 | 0 |
| P211_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | 48064 | 66008 | 66488.4 | 0.722544 | 0.0965297 |  |  | 0 | 0 | 0 | 1 | 0 | rejected_control_like_or_worse_mse | 0 | 0 | 0 | 0 | 0 |
| P211_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | 12059 | 273838 | 263452 | -3.94257 | 0.143592 |  |  | 0 | 0 | 1 | 1 | 0 | rejected_control_like_or_worse_mse | 0 | 0 | 0 | 0 | 0 |
| P211_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | 363786 | 0.153643 | 0.149322 | -2.89332 | 0.073973 | 0.817428 | 0.817428 | 0 | 0 | 0 | 0 | 0 | rejected_control_like_or_worse_mse | 0 | 0 | 0 | 0 | 0 |
| P211_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | 137477 | 0.200239 | 0.197502 | -1.38613 | 0.0890257 | 0.729249 | 0.729249 | 0 | 0 | 0 | 0 | 0 | rejected_control_like_or_worse_mse | 0 | 0 | 0 | 0 | 0 |
| P211_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | 48064 | 0.231062 | 0.229583 | -0.644427 | 0.0635149 | 0.642498 | 0.642498 | 0 | 0 | 0 | 0 | 0 | rejected_control_like_or_worse_mse | 0 | 0 | 0 | 0 | 0 |
| P211_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | 12059 | 0.241328 | 0.241033 | -0.12222 | 0.0416012 | 0.594162 | 0.594162 | 0 | 0 | 0 | 0 | 0 | rejected_control_like_or_worse_mse | 0 | 0 | 0 | 0 | 0 |

## Family Summary

| phase211_family_summary_id | phase209_model_spec_id | interpreted_horizon_rows | passing_interpretation_rows | best_mse_improvement_pct_vs_control | best_abs_validation_correlation | best_binary_accuracy_lift_vs_control | family_verdict | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P211_FAMILY_P209_LINEAR_LOGIT_DIRECTION_BASELINE | P209_LINEAR_LOGIT_DIRECTION_BASELINE | 4 | 0 | 0.954266 | 0.110658 | 0.0116096 | closed_for_replay_redesign_required | 0 | 0 |
| P211_FAMILY_P209_MONOTONIC_TREE_DIAGNOSTIC | P209_MONOTONIC_TREE_DIAGNOSTIC | 4 | 0 | -0.12222 | 0.0890257 | 0 | closed_for_replay_redesign_required | 0 | 0 |
| P211_FAMILY_P209_RIDGE_RETURN_SIGN_BASELINE | P209_RIDGE_RETURN_SIGN_BASELINE | 4 | 0 | 0.722544 | 0.143592 | 0 | closed_for_replay_redesign_required | 0 | 0 |

## Decision Ledger

| phase211_decision_id | passing_interpretation_rows | model_families_with_pass | decision | rationale | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P211_VALIDATION_INTERPRETATION_DECISION | 0 | 0 | no_candidate_opened_for_replay | Validation dry-run metrics are compared with shuffled-target controls; replay and sealed test remain closed regardless of interpretation. | 0 | 0 | 0 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase211 | allowed_in_phase211 | rationale |
| --- | --- | --- | --- |
| strategy_replay | 0 | 0 | Phase211 interprets aggregate validation metrics only and keeps replay, test, P&L, promotion, and paper/live closed. |
| test_replay_execution | 0 | 0 | Phase211 interprets aggregate validation metrics only and keeps replay, test, P&L, promotion, and paper/live closed. |
| test_result | 0 | 0 | Phase211 interprets aggregate validation metrics only and keeps replay, test, P&L, promotion, and paper/live closed. |
| promotion | 0 | 0 | Phase211 interprets aggregate validation metrics only and keeps replay, test, P&L, promotion, and paper/live closed. |
| paper_live_acceptance | 0 | 0 | Phase211 interprets aggregate validation metrics only and keeps replay, test, P&L, promotion, and paper/live closed. |
| order_arrival | 0 | 0 | Phase211 interprets aggregate validation metrics only and keeps replay, test, P&L, promotion, and paper/live closed. |
| fill_model | 0 | 0 | Phase211 interprets aggregate validation metrics only and keeps replay, test, P&L, promotion, and paper/live closed. |
| pnl_replay | 0 | 0 | Phase211 interprets aggregate validation metrics only and keeps replay, test, P&L, promotion, and paper/live closed. |
| profitability_claim | 0 | 0 | Phase211 interprets aggregate validation metrics only and keeps replay, test, P&L, promotion, and paper/live closed. |
| threshold_widening | 0 | 0 | Phase211 interprets aggregate validation metrics only and keeps replay, test, P&L, promotion, and paper/live closed. |
| row_level_prediction_export | 0 | 0 | Phase211 interprets aggregate validation metrics only and keeps replay, test, P&L, promotion, and paper/live closed. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P211_PHASE210_COMPLETE | True | phase210_complete=1 | hard |
| P211_INTERPRETATION_ROWS_RECORDED | True | interpretation_rows=12 | hard |
| P211_FAMILY_SUMMARY_RECORDED | True | family_summary_rows=3 | hard |
| P211_DECISION_LEDGER_RECORDED | True | decision_rows=1 | hard |
| P211_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; replay_flags=0 | hard |
| P211_NO_TEST_REPLAY_OR_PROFITABILITY_CLAIM | True | closed_flags_sum=0 | hard |

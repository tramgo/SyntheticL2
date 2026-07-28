# Phase218 Event-only Model-fit Precommit-or-stop

Generated UTC: 2026-07-28T21:57:44.506227+00:00

Phase218 decides whether the Phase217 event-only design-matrix contract is strong enough to precommit a train/validation model-fit dry run.
It precommits a Phase219 dry run but does not execute model fitting, emit predictions, run replay, use sealed test, promote anything, or make profitability claims.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase218_decision_rows | 1 | Decision ledger rows |
| phase218_model_spec_rows | 3 | Model-family specification rows |
| phase218_target_contract_rows | 7 | Event-only target contract rows |
| phase218_feature_contract_rows | 18 | Event-only feature contract rows |
| phase218_control_contract_rows | 3 | Control contract rows |
| phase218_phase219_work_order_rows | 1 | Phase219 work-order rows |
| phase218_forbidden_execution_rows | 14 | Forbidden execution rows |
| phase218_gate_rows | 7 | Gates evaluated |
| phase218_hard_gate_rows | 7 | Hard gates evaluated |
| phase218_hard_gate_pass_rows | 7 | Hard gates passed |
| phase218_event_only_model_fit_precommit_or_stop_complete | 1 | 1 means Phase218 completed |
| phase218_model_fit_dry_run_precommitted_for_phase219 | 1 | 1 means Phase219 may execute train/validation fit dry run |
| phase218_model_fit_execution_allowed | 0 | No model fit execution in Phase218 |
| phase218_strategy_replay_allowed | 0 | No strategy replay opened |
| phase218_test_replay_allowed_next | 0 | No test replay opened |
| phase218_promotion_allowed | 0 | No promotion opened |
| phase218_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase218_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase218_forbidden_outputs | model_fit_execution;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_design_matrix_export;row_level_prediction_export | Outputs forbidden in this phase |
| phase218_next_best_action | run_phase219_event_only_train_validation_model_fit_dry_run_no_replay_no_test | Recommended next milestone |

## Decision Ledger

| phase218_decision_id | decision | phase217_complete | target_scope_rows | feature_binding_rows | control_plan_rows | target_row_observation_scope | minimum_target_scope_rows | minimum_feature_binding_rows | minimum_event_only_observations | model_fit_dry_run_precommitted_for_phase219 | model_fit_execution_allowed_phase218 | strategy_replay_allowed | test_replay_allowed_next | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P218_PRECOMMIT_EVENT_ONLY_MODEL_FIT_DRY_RUN | precommit_phase219_event_only_train_validation_model_fit_dry_run | 1 | 7 | 42 | 3 | 384282 | 3 | 18 | 10000 | 1 | 0 | 0 | 0 | 0 |

## Model Family Spec

| phase218_model_spec_id | model_family | target_labels | primary_horizons_sec | feature_policy | sample_policy | control_policy | selection_policy | allowed_next_phase_scope | model_fit_execution_allowed_phase218 | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_down_conditional_label;event_surprise_up_conditional_label;event_surprise_vol_expansion_conditional_label | 1;15;5 | phase217_same_horizon_receive_flow_features_only | event_surprise_bucket_equals_1_train_fit_validation_score_only | base_rate_and_event_time_shuffle_controls_required | validation_screening_only_test_sealed_no_replay | phase219_train_validation_fit_dry_run_only | 0 | 0 | 0 | 0 | 0 |
| P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_down_conditional_label;event_surprise_up_conditional_label;event_surprise_vol_expansion_conditional_label | 1;15;5 | phase217_same_horizon_receive_flow_features_only_nonnegative_transforms_where_required | event_surprise_bucket_equals_1_train_fit_validation_score_only | base_rate_and_event_time_shuffle_controls_required | diagnostic_validation_only_test_sealed_no_replay | phase219_train_validation_fit_dry_run_only | 0 | 0 | 0 | 0 | 0 |
| P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label;event_surprise_up_conditional_label;event_surprise_vol_expansion_conditional_label | 1;15;5 | phase217_same_horizon_receive_flow_features_only_depth_limited | event_surprise_bucket_equals_1_train_fit_validation_score_only | base_rate_and_event_time_shuffle_controls_required | interpretability_only_no_threshold_selection_for_test | phase219_train_validation_fit_dry_run_only | 0 | 0 | 0 | 0 | 0 |

## Event-only Target Contract

| phase218_target_contract_id | phase217_target_scope_id | label_name | horizon_sec | train_event_only_rows | validation_event_only_rows | total_event_only_rows | positive_rate_min | positive_rate_max | eligible_for_phase219_fit_dry_run | sealed_test_rows_used | model_fit_execution_allowed_phase218 | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P218_TARGET_EVENT_ONLY_H1s_event_surprise_down_conditional_label | P217_SCOPE_EVENT_ONLY_H1s_event_surprise_down_conditional_label | event_surprise_down_conditional_label | 1 | 52764 | 31457 | 84221 | 0.0116941 | 0.0160367 | 1 | 0 | 0 | 0 | 0 |
| P218_TARGET_EVENT_ONLY_H1s_event_surprise_up_conditional_label | P217_SCOPE_EVENT_ONLY_H1s_event_surprise_up_conditional_label | event_surprise_up_conditional_label | 1 | 52764 | 31457 | 84221 | 0.011833 | 0.0151348 | 1 | 0 | 0 | 0 | 0 |
| P218_TARGET_EVENT_ONLY_H1s_event_surprise_vol_expansion_conditional_label | P217_SCOPE_EVENT_ONLY_H1s_event_surprise_vol_expansion_conditional_label | event_surprise_vol_expansion_conditional_label | 1 | 52764 | 31457 | 84221 | 0.0235504 | 0.0313369 | 1 | 0 | 0 | 0 | 0 |
| P218_TARGET_EVENT_ONLY_H5s_event_surprise_down_conditional_label | P217_SCOPE_EVENT_ONLY_H5s_event_surprise_down_conditional_label | event_surprise_down_conditional_label | 5 | 25922 | 17072 | 42994 | 0.0292557 | 0.0419709 | 1 | 0 | 0 | 0 | 0 |
| P218_TARGET_EVENT_ONLY_H5s_event_surprise_up_conditional_label | P217_SCOPE_EVENT_ONLY_H5s_event_surprise_up_conditional_label | event_surprise_up_conditional_label | 5 | 25922 | 17072 | 42994 | 0.0289357 | 0.0409329 | 1 | 0 | 0 | 0 | 0 |
| P218_TARGET_EVENT_ONLY_H5s_event_surprise_vol_expansion_conditional_label | P217_SCOPE_EVENT_ONLY_H5s_event_surprise_vol_expansion_conditional_label | event_surprise_vol_expansion_conditional_label | 5 | 25922 | 17072 | 42994 | 0.0534895 | 0.0767712 | 1 | 0 | 0 | 0 | 0 |
| P218_TARGET_EVENT_ONLY_H15s_event_surprise_vol_expansion_conditional_label | P217_SCOPE_EVENT_ONLY_H15s_event_surprise_vol_expansion_conditional_label | event_surprise_vol_expansion_conditional_label | 15 | 1792 | 845 | 2637 | 0.0121921 | 0.0130643 | 1 | 0 | 0 | 0 | 0 |

## Event-only Feature Contract

| phase218_feature_contract_id | phase206_feature_id | feature_family | horizon_sec | required_columns | present_columns | target_bindings | same_horizon_binding | feature_available | eligible_for_phase219_fit_dry_run | model_fit_execution_allowed_phase218 | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P218_P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H1s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | 1 | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H5s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | 5 | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H15s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | 15 | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_DEPTH_REFRESH_INTENSITY_H1s | P206_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | 1 | depth_refresh_count;top5_qty_imbalance | depth_refresh_count;top5_qty_imbalance | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_DEPTH_REFRESH_INTENSITY_H5s | P206_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | 5 | depth_refresh_count;top5_qty_imbalance | depth_refresh_count;top5_qty_imbalance | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_DEPTH_REFRESH_INTENSITY_H15s | P206_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | 15 | depth_refresh_count;top5_qty_imbalance | depth_refresh_count;top5_qty_imbalance | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_QUOTE_CHURN_RATE_H1s | P206_QUOTE_CHURN_RATE | book_state_churn | 1 | quote_churn_count | quote_churn_count | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_QUOTE_CHURN_RATE_H5s | P206_QUOTE_CHURN_RATE | book_state_churn | 5 | quote_churn_count | quote_churn_count | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_QUOTE_CHURN_RATE_H15s | P206_QUOTE_CHURN_RATE | book_state_churn | 15 | quote_churn_count | quote_churn_count | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_RECEIVE_EVENT_RATE_ZSCORE_H1s | P206_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | 1 | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_RECEIVE_EVENT_RATE_ZSCORE_H5s | P206_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | 5 | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_RECEIVE_EVENT_RATE_ZSCORE_H15s | P206_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | 15 | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_RECEIVE_FLOW_REGIME_STATE_H1s | P206_RECEIVE_FLOW_REGIME_STATE | source_quality_context | 1 | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_RECEIVE_FLOW_REGIME_STATE_H5s | P206_RECEIVE_FLOW_REGIME_STATE | source_quality_context | 5 | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_RECEIVE_FLOW_REGIME_STATE_H15s | P206_RECEIVE_FLOW_REGIME_STATE | source_quality_context | 15 | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_STALE_QUOTE_DURATION_H1s | P206_STALE_QUOTE_DURATION | feed_staleness | 1 | stale_quote_duration_ms | stale_quote_duration_ms | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_STALE_QUOTE_DURATION_H5s | P206_STALE_QUOTE_DURATION | feed_staleness | 5 | stale_quote_duration_ms | stale_quote_duration_ms | 3 | 1 | 1 | 1 | 0 | 0 | 0 |
| P218_P206_STALE_QUOTE_DURATION_H15s | P206_STALE_QUOTE_DURATION | feed_staleness | 15 | stale_quote_duration_ms | stale_quote_duration_ms | 1 | 1 | 1 | 1 | 0 | 0 | 0 |

## Control Contract

| phase218_control_id | control_type | contract | required_for_phase219_fit_dry_run | target_scope_rows_covered | event_only_rows_covered | sealed_test_rows_used | model_fit_execution_allowed_phase218 | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P218_EVENT_ONLY_BASE_RATE_CONTROL | base_rate | Phase217 must compute event-only base-rate controls for each allowed label/horizon before any future fit. | 1 | 7 | 384282 | 0 | 0 | 0 | 0 |
| P218_EVENT_TIME_SHUFFLE_CONTROL | time_shuffle | Phase217 must preserve a shuffled event-time control to test whether event timing matters beyond label base rates. | 1 | 7 | 384282 | 0 | 0 | 0 | 0 |
| P218_SEALED_TEST_ZERO_USE_CONTROL | sealed_test | Phase217 may inventory sealed test rows but must use zero sealed test rows. | 1 | 7 | 0 | 0 | 0 | 0 | 0 |

## Phase219 Work Order

| phase219_work_order_id | work_order | model_fit_dry_run_precommitted | model_spec_rows | target_contract_rows | feature_contract_rows | control_contract_rows | allowed_next_scope | model_fit_execution_allowed_phase219 | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P219_EVENT_ONLY_TRAIN_VALIDATION_MODEL_FIT_DRY_RUN | Execute only a train/validation event-only model-fit dry run using Phase218 specs and controls; emit validation diagnostics, no strategy replay, no sealed test, no promotion. | 1 | 3 | 7 | 18 | 3 | train_validation_model_fit_dry_run_no_replay_no_test | 1 | 0 | 0 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase218 | allowed_in_phase218 | rationale |
| --- | --- | --- | --- |
| model_fit_execution | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| model_prediction | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| strategy_replay | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| test_replay_execution | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| test_result | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| promotion | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| paper_live_acceptance | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| order_arrival | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| fill_model | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| pnl_replay | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| profitability_claim | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| threshold_widening | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| row_level_design_matrix_export | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |
| row_level_prediction_export | 0 | 0 | Phase218 is a model-fit precommit decision only; model execution can happen only in a later gated dry-run phase. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P218_PHASE217_COMPLETE | True | phase217_complete=1 | hard |
| P218_DECISION_RECORDED | True | decision_rows=1; dry_run_precommitted=1 | hard |
| P218_MODEL_SPECS_RECORDED | True | model_specs=3 | hard |
| P218_TARGET_AND_FEATURE_CONTRACTS_RECORDED | True | targets=7; eligible_targets=7; features=18; eligible_features=18 | hard |
| P218_CONTROLS_RECORDED | True | controls=3; required=3 | hard |
| P218_PHASE219_WORK_ORDER_RECORDED | True | work_order=1; phase219_fit_allowed=1 | hard |
| P218_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; phase218_execution_flags=0 | hard |

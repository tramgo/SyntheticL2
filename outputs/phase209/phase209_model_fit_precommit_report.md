# Phase209 Model-fit Precommit Spec

Generated UTC: 2026-07-28T21:10:33.078514+00:00

Phase209 freezes the next model-fit design without executing the fit.
It records model families, feature sets, label targets, train/validation/test sealing rules, negative controls, and forbidden outputs.
It emits no model predictions, no strategy replay, no order/fill/P&L artifacts, no promotion, and no paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase209_model_spec_rows | 3 | Model-family specification rows |
| phase209_feature_set_rows | 24 | Feature-set contract rows |
| phase209_allowed_feature_set_rows | 24 | Feature-set rows allowed for future Phase210 design matrix |
| phase209_label_target_rows | 3 | Label-target contract rows |
| phase209_split_control_rows | 4 | Split/control contract rows |
| phase209_forbidden_execution_rows | 12 | Forbidden execution ledger rows |
| phase209_gate_rows | 6 | Gates evaluated |
| phase209_hard_gate_rows | 6 | Hard gates evaluated |
| phase209_hard_gate_pass_rows | 6 | Hard gates passed |
| phase209_model_fit_precommit_spec_complete | 1 | 1 means Phase209 completed |
| phase209_model_fit_execution_allowed | 0 | No model fitting executed/opened in Phase209 |
| phase209_strategy_replay_allowed | 0 | No strategy replay opened |
| phase209_test_replay_allowed_next | 0 | No test replay opened |
| phase209_promotion_allowed | 0 | No promotion opened |
| phase209_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase209_forbidden_outputs | model_fit;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening | Outputs forbidden in this phase |
| phase209_next_best_action | run_phase210_train_validation_model_fit_dry_run_no_replay_no_test | Recommended next milestone |

## Model Fit Spec

| phase209_model_spec_id | model_family | target_label | primary_horizons_sec | feature_policy | calibration_policy | selection_policy | negative_controls_required | allowed_next_phase_scope | model_fit_execution_allowed_phase209 | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P209_LINEAR_LOGIT_DIRECTION_BASELINE | regularized_logistic_classification | short_horizon_direction_label | 1;5;15;60 | phase206_nonoverlap_allowed_features_only | train_fit_validation_calibration_only | validation_screening_only_test_sealed | shuffled_time_date;target_symbol_excluded_cross_symbol;blocked_form_overlap | train_validation_fit_dry_run_only | 0 | 0 | 0 | 0 | 0 |
| P209_RIDGE_RETURN_SIGN_BASELINE | regularized_linear_return_sign_proxy | future_mid_return_bps_next_bucket | 1;5;15;60 | phase206_nonoverlap_allowed_features_only | train_only_standardization_validation_score_no_test | validation_screening_only_test_sealed | shuffled_time_date;target_symbol_excluded_cross_symbol;blocked_form_overlap | train_validation_fit_dry_run_only | 0 | 0 | 0 | 0 | 0 |
| P209_MONOTONIC_TREE_DIAGNOSTIC | monotonic_tree_or_gradient_boosting_diagnostic | execution_risk_spread_widen_next_bucket | 1;5;15;60 | phase206_nonoverlap_allowed_features_only_with_depth_direction_constraints | validation_diagnostic_only_no_threshold_selection_for_test | diagnostic_interpretability_only_test_sealed | shuffled_time_date;target_symbol_excluded_cross_symbol;blocked_form_overlap | train_validation_fit_dry_run_only | 0 | 0 | 0 | 0 | 0 |

## Feature Set Contract

| phase209_feature_set_id | phase206_feature_id | feature_family | horizon_sec | required_columns | feature_available | quality_gate_pass | trade_dates | symbols | total_feature_rows | allowed_for_phase210_design_matrix | model_fit_execution_allowed_phase209 | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P209_P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H1s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | 1 | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | 1 | 1 | 7 | 32 | 2165652 | 1 | 0 | 0 | 0 |
| P209_P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H5s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | 5 | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | 1 | 1 | 7 | 32 | 818832 | 1 | 0 | 0 | 0 |
| P209_P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H15s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | 15 | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | 1 | 1 | 7 | 32 | 286633 | 1 | 0 | 0 | 0 |
| P209_P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H60s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | 60 | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | 1 | 1 | 7 | 32 | 72139 | 1 | 0 | 0 | 0 |
| P209_P206_DEPTH_REFRESH_INTENSITY_H1s | P206_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | 1 | depth_refresh_count;top5_qty_imbalance | 1 | 1 | 7 | 32 | 2165652 | 1 | 0 | 0 | 0 |
| P209_P206_DEPTH_REFRESH_INTENSITY_H5s | P206_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | 5 | depth_refresh_count;top5_qty_imbalance | 1 | 1 | 7 | 32 | 818832 | 1 | 0 | 0 | 0 |
| P209_P206_DEPTH_REFRESH_INTENSITY_H15s | P206_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | 15 | depth_refresh_count;top5_qty_imbalance | 1 | 1 | 7 | 32 | 286633 | 1 | 0 | 0 | 0 |
| P209_P206_DEPTH_REFRESH_INTENSITY_H60s | P206_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | 60 | depth_refresh_count;top5_qty_imbalance | 1 | 1 | 7 | 32 | 72139 | 1 | 0 | 0 | 0 |
| P209_P206_QUOTE_CHURN_RATE_H1s | P206_QUOTE_CHURN_RATE | book_state_churn | 1 | quote_churn_count | 1 | 1 | 7 | 32 | 2165652 | 1 | 0 | 0 | 0 |
| P209_P206_QUOTE_CHURN_RATE_H5s | P206_QUOTE_CHURN_RATE | book_state_churn | 5 | quote_churn_count | 1 | 1 | 7 | 32 | 818832 | 1 | 0 | 0 | 0 |
| P209_P206_QUOTE_CHURN_RATE_H15s | P206_QUOTE_CHURN_RATE | book_state_churn | 15 | quote_churn_count | 1 | 1 | 7 | 32 | 286633 | 1 | 0 | 0 | 0 |
| P209_P206_QUOTE_CHURN_RATE_H60s | P206_QUOTE_CHURN_RATE | book_state_churn | 60 | quote_churn_count | 1 | 1 | 7 | 32 | 72139 | 1 | 0 | 0 | 0 |
| P209_P206_RECEIVE_EVENT_RATE_ZSCORE_H1s | P206_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | 1 | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | 1 | 1 | 7 | 32 | 2165652 | 1 | 0 | 0 | 0 |
| P209_P206_RECEIVE_EVENT_RATE_ZSCORE_H5s | P206_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | 5 | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | 1 | 1 | 7 | 32 | 818832 | 1 | 0 | 0 | 0 |
| P209_P206_RECEIVE_EVENT_RATE_ZSCORE_H15s | P206_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | 15 | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | 1 | 1 | 7 | 32 | 286633 | 1 | 0 | 0 | 0 |
| P209_P206_RECEIVE_EVENT_RATE_ZSCORE_H60s | P206_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | 60 | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | 1 | 1 | 7 | 32 | 72139 | 1 | 0 | 0 | 0 |
| P209_P206_RECEIVE_FLOW_REGIME_STATE_H1s | P206_RECEIVE_FLOW_REGIME_STATE | source_quality_context | 1 | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | 1 | 1 | 7 | 32 | 2165652 | 1 | 0 | 0 | 0 |
| P209_P206_RECEIVE_FLOW_REGIME_STATE_H5s | P206_RECEIVE_FLOW_REGIME_STATE | source_quality_context | 5 | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | 1 | 1 | 7 | 32 | 818832 | 1 | 0 | 0 | 0 |
| P209_P206_RECEIVE_FLOW_REGIME_STATE_H15s | P206_RECEIVE_FLOW_REGIME_STATE | source_quality_context | 15 | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | 1 | 1 | 7 | 32 | 286633 | 1 | 0 | 0 | 0 |
| P209_P206_RECEIVE_FLOW_REGIME_STATE_H60s | P206_RECEIVE_FLOW_REGIME_STATE | source_quality_context | 60 | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | 1 | 1 | 7 | 32 | 72139 | 1 | 0 | 0 | 0 |
| P209_P206_STALE_QUOTE_DURATION_H1s | P206_STALE_QUOTE_DURATION | feed_staleness | 1 | stale_quote_duration_ms | 1 | 1 | 7 | 32 | 2165652 | 1 | 0 | 0 | 0 |
| P209_P206_STALE_QUOTE_DURATION_H5s | P206_STALE_QUOTE_DURATION | feed_staleness | 5 | stale_quote_duration_ms | 1 | 1 | 7 | 32 | 818832 | 1 | 0 | 0 | 0 |
| P209_P206_STALE_QUOTE_DURATION_H15s | P206_STALE_QUOTE_DURATION | feed_staleness | 15 | stale_quote_duration_ms | 1 | 1 | 7 | 32 | 286633 | 1 | 0 | 0 | 0 |
| P209_P206_STALE_QUOTE_DURATION_H60s | P206_STALE_QUOTE_DURATION | feed_staleness | 60 | stale_quote_duration_ms | 1 | 1 | 7 | 32 | 72139 | 1 | 0 | 0 | 0 |

## Label Target Contract

| phase209_label_target_id | label_column | target_type | description | label_family_rows | label_partition_rows | label_available_rows | train_label_available_rows | validation_label_available_rows | test_label_available_rows_sealed | column_seen_in_sample | cost_latency_binding | test_selection_allowed | model_fit_execution_allowed_phase209 | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P209_PRIMARY_DIRECTION_TARGET | short_horizon_direction_label | classification_direction | future receive-flow direction label; no P&L label | 3 | 896 | 3342240 | 1079615 | 561386 | 0 | 1 | zerodha_equity_cost_catalog_plus_latency_queue_before_replay;zerodha_equity_cost_catalog_plus_receive_to_order_latency_catalog_before_replay;zerodha_equity_cost_catalog_plus_slippage_latency_stress_before_replay | 0 | 0 | 0 |
| P209_RETURN_PROXY_TARGET | future_mid_return_bps_next_bucket | regression_or_sign_proxy | future mid-return label for model diagnostics only | 3 | 896 | 3342240 | 1079615 | 561386 | 0 | 1 | zerodha_equity_cost_catalog_plus_latency_queue_before_replay;zerodha_equity_cost_catalog_plus_receive_to_order_latency_catalog_before_replay;zerodha_equity_cost_catalog_plus_slippage_latency_stress_before_replay | 0 | 0 | 0 |
| P209_EXECUTION_RISK_TARGET | execution_risk_spread_widen_next_bucket | classification_execution_risk | future spread-widening risk label; not a fill model | 3 | 896 | 3342240 | 1079615 | 561386 | 0 | 1 | zerodha_equity_cost_catalog_plus_latency_queue_before_replay;zerodha_equity_cost_catalog_plus_receive_to_order_latency_catalog_before_replay;zerodha_equity_cost_catalog_plus_slippage_latency_stress_before_replay | 0 | 0 | 0 |

## Split and Control Contract

| phase209_control_id | control_type | required_before_phase210 | contract | train_dates | validation_dates | test_dates_sealed | source_ablation_ids | model_fit_execution_allowed_phase209 | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P209_TRAIN_VALIDATION_TEST_SPLIT_CONTRACT | split | 1 | Fit on train only; screen/calibrate on validation only; keep test dates sealed and unused. | 2026-07-08;2026-07-09;2026-07-10 | 2026-07-13 | 2026-07-14 | P207_BLOCKED_FORM_OVERLAP_CONTROL;P207_SHUFFLED_TIME_NEGATIVE_CONTROL;P207_TARGET_SYMBOL_EXCLUDED_SYNCHRONY | 0 | 0 | 0 |
| P209_SHUFFLED_TIME_DATE_NEGATIVE_CONTROL | negative_control | 1 | Every model-family dry run must include a shuffled time/date control before edge interpretation. | 2026-07-08;2026-07-09;2026-07-10 | 2026-07-13 | 2026-07-14 | P207_BLOCKED_FORM_OVERLAP_CONTROL;P207_SHUFFLED_TIME_NEGATIVE_CONTROL;P207_TARGET_SYMBOL_EXCLUDED_SYNCHRONY | 0 | 0 | 0 |
| P209_TARGET_SYMBOL_EXCLUDED_CROSS_SYMBOL_CONTROL | leakage_control | 1 | Cross-symbol arrival synchrony must exclude the target symbol in any future design matrix. | 2026-07-08;2026-07-09;2026-07-10 | 2026-07-13 | 2026-07-14 | P207_BLOCKED_FORM_OVERLAP_CONTROL;P207_SHUFFLED_TIME_NEGATIVE_CONTROL;P207_TARGET_SYMBOL_EXCLUDED_SYNCHRONY | 0 | 0 | 0 |
| P209_BLOCKED_FORM_OVERLAP_CONTROL | reuse_control | 1 | No Phase164 form reuse, no fixed Phase167 S08 score, no passive queue replay form overlap. | 2026-07-08;2026-07-09;2026-07-10 | 2026-07-13 | 2026-07-14 | P207_BLOCKED_FORM_OVERLAP_CONTROL;P207_SHUFFLED_TIME_NEGATIVE_CONTROL;P207_TARGET_SYMBOL_EXCLUDED_SYNCHRONY | 0 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase209 | allowed_in_phase209 | rationale |
| --- | --- | --- | --- |
| model_fit | 0 | 0 | Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase. |
| model_prediction | 0 | 0 | Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase. |
| strategy_replay | 0 | 0 | Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase. |
| test_replay_execution | 0 | 0 | Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase. |
| test_result | 0 | 0 | Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase. |
| promotion | 0 | 0 | Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase. |
| paper_live_acceptance | 0 | 0 | Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase. |
| order_arrival | 0 | 0 | Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase. |
| fill_model | 0 | 0 | Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase. |
| pnl_replay | 0 | 0 | Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase. |
| profitability_claim | 0 | 0 | Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase. |
| threshold_widening | 0 | 0 | Phase209 is a model-fit precommit specification only; execution begins no earlier than a future gated dry-run phase. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P209_PHASE208_COMPLETE | True | phase208_complete=1 | hard |
| P209_MODEL_SPECS_RECORDED | True | model_spec_rows=3 | hard |
| P209_FEATURE_SET_CONTRACT_RECORDED | True | allowed_feature_rows=24 | hard |
| P209_LABEL_TARGET_CONTRACT_RECORDED | True | label_rows=3; columns_seen=3 | hard |
| P209_SPLIT_AND_CONTROL_CONTRACT_RECORDED | True | split_control_rows=4; required_controls=4 | hard |
| P209_FORBIDDEN_EXECUTION_LEDGER_CLEAN | True | forbidden_emitted=0; forbidden_flags=0 | hard |

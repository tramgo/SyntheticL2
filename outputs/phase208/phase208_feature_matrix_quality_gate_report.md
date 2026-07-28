# Phase208 Feature Matrix Quality Gate

Generated UTC: 2026-07-28T20:56:40.831023+00:00

Phase208 validates the Phase207 allowed feature matrix against Phase177 partition-quality evidence.
It does not fit models, run replay, emit orders/fills/P&L, promote anything, or open paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase208_quality_summary_rows | 24 | Feature/horizon quality rows |
| phase208_quality_pass_rows | 24 | Feature/horizon quality rows passed |
| phase208_blocking_gap_rows | 0 | Blocking quality gap rows |
| phase208_trade_dates_max | 7 | Maximum trade-date coverage |
| phase208_symbols_max | 32 | Maximum symbol coverage |
| phase208_gate_rows | 6 | Gates evaluated |
| phase208_hard_gate_rows | 6 | Hard gates evaluated |
| phase208_hard_gate_pass_rows | 6 | Hard gates passed |
| phase208_feature_matrix_quality_gate_complete | 1 | 1 means Phase208 completed |
| phase208_model_fit_allowed | 0 | No model fitting opened |
| phase208_strategy_replay_allowed | 0 | No strategy replay opened |
| phase208_test_replay_allowed_next | 0 | No test replay opened |
| phase208_promotion_allowed | 0 | No promotion opened |
| phase208_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase208_forbidden_outputs | model_fit;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening | Outputs forbidden in this phase |
| phase208_next_best_action | run_phase209_model_fit_precommit_spec_no_execution_no_replay | Recommended next milestone |

## Feature Matrix Quality Summary

| quality_id | phase206_feature_id | horizon_sec | feature_available | trade_dates | symbols | total_feature_rows | coverage_pass | missing_required_column_partitions | duplicate_bucket_rows | bucket_monotonic_violations | quality_gate_pass | model_fit_allowed | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P208_P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H1s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | 1 | 1 | 7 | 32 | 2165652 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H5s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | 5 | 1 | 7 | 32 | 818832 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H15s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | 15 | 1 | 7 | 32 | 286633 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H60s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | 60 | 1 | 7 | 32 | 72139 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_DEPTH_REFRESH_INTENSITY_H1s | P206_DEPTH_REFRESH_INTENSITY | 1 | 1 | 7 | 32 | 2165652 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_DEPTH_REFRESH_INTENSITY_H5s | P206_DEPTH_REFRESH_INTENSITY | 5 | 1 | 7 | 32 | 818832 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_DEPTH_REFRESH_INTENSITY_H15s | P206_DEPTH_REFRESH_INTENSITY | 15 | 1 | 7 | 32 | 286633 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_DEPTH_REFRESH_INTENSITY_H60s | P206_DEPTH_REFRESH_INTENSITY | 60 | 1 | 7 | 32 | 72139 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_QUOTE_CHURN_RATE_H1s | P206_QUOTE_CHURN_RATE | 1 | 1 | 7 | 32 | 2165652 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_QUOTE_CHURN_RATE_H5s | P206_QUOTE_CHURN_RATE | 5 | 1 | 7 | 32 | 818832 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_QUOTE_CHURN_RATE_H15s | P206_QUOTE_CHURN_RATE | 15 | 1 | 7 | 32 | 286633 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_QUOTE_CHURN_RATE_H60s | P206_QUOTE_CHURN_RATE | 60 | 1 | 7 | 32 | 72139 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_RECEIVE_EVENT_RATE_ZSCORE_H1s | P206_RECEIVE_EVENT_RATE_ZSCORE | 1 | 1 | 7 | 32 | 2165652 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_RECEIVE_EVENT_RATE_ZSCORE_H5s | P206_RECEIVE_EVENT_RATE_ZSCORE | 5 | 1 | 7 | 32 | 818832 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_RECEIVE_EVENT_RATE_ZSCORE_H15s | P206_RECEIVE_EVENT_RATE_ZSCORE | 15 | 1 | 7 | 32 | 286633 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_RECEIVE_EVENT_RATE_ZSCORE_H60s | P206_RECEIVE_EVENT_RATE_ZSCORE | 60 | 1 | 7 | 32 | 72139 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_RECEIVE_FLOW_REGIME_STATE_H1s | P206_RECEIVE_FLOW_REGIME_STATE | 1 | 1 | 7 | 32 | 2165652 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_RECEIVE_FLOW_REGIME_STATE_H5s | P206_RECEIVE_FLOW_REGIME_STATE | 5 | 1 | 7 | 32 | 818832 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_RECEIVE_FLOW_REGIME_STATE_H15s | P206_RECEIVE_FLOW_REGIME_STATE | 15 | 1 | 7 | 32 | 286633 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_RECEIVE_FLOW_REGIME_STATE_H60s | P206_RECEIVE_FLOW_REGIME_STATE | 60 | 1 | 7 | 32 | 72139 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_STALE_QUOTE_DURATION_H1s | P206_STALE_QUOTE_DURATION | 1 | 1 | 7 | 32 | 2165652 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_STALE_QUOTE_DURATION_H5s | P206_STALE_QUOTE_DURATION | 5 | 1 | 7 | 32 | 818832 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_STALE_QUOTE_DURATION_H15s | P206_STALE_QUOTE_DURATION | 15 | 1 | 7 | 32 | 286633 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| P208_P206_STALE_QUOTE_DURATION_H60s | P206_STALE_QUOTE_DURATION | 60 | 1 | 7 | 32 | 72139 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

## Blocking Gap Ledger

| gap_id | blocking | evidence | model_fit_allowed | strategy_replay_allowed |
| --- | --- | --- | --- | --- |
| P208_NO_BLOCKING_GAPS | 0 | all feature-matrix quality checks passed | 0 | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P208_PHASE207_COMPLETE | True | phase207_complete=1 | hard |
| P208_QUALITY_SUMMARY_RECORDED | True | quality_rows=24 | hard |
| P208_ALL_MATRIX_ROWS_PASS_QUALITY | True | quality_pass_rows=24; quality_rows=24 | hard |
| P208_NO_BLOCKING_GAPS | True | blocking_gaps=0 | hard |
| P208_ABLATION_AND_TERMINOLOGY_CONTROLS_PRESENT | True | ablation_rows=3; audit_rows=3 | hard |
| P208_NO_MODEL_FIT_REPLAY_OR_PROMOTION | True | forbidden_flag_sum=0 | hard |

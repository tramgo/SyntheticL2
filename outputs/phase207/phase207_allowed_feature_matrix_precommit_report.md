# Phase207 Allowed Feature Matrix Precommit

Generated UTC: 2026-07-28T20:52:02.167477+00:00

Phase207 builds an allowed feature/horizon availability matrix from the Phase206 catalog and Phase176 materialized features.
It emits no model fit, no replay, no orders/fills/P&L, no promotion and no paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase207_feature_matrix_rows | 24 | Feature/horizon matrix rows |
| phase207_feature_available_rows | 24 | Available feature/horizon rows |
| phase207_trade_dates_max | 7 | Maximum trade-date coverage |
| phase207_symbols_max | 32 | Maximum symbol coverage |
| phase207_target_exclusion_ablation_rows | 3 | Ablation spec rows |
| phase207_leakage_terminology_audit_rows | 3 | Leakage/terminology audit rows |
| phase207_gate_rows | 6 | Gates evaluated |
| phase207_hard_gate_rows | 6 | Hard gates evaluated |
| phase207_hard_gate_pass_rows | 6 | Hard gates passed |
| phase207_feature_matrix_precommit_complete | 1 | 1 means Phase207 completed |
| phase207_model_fit_allowed | 0 | No model fitting opened |
| phase207_strategy_replay_allowed | 0 | No strategy replay opened |
| phase207_test_replay_allowed_next | 0 | No test replay opened |
| phase207_promotion_allowed | 0 | No promotion opened |
| phase207_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase207_forbidden_outputs | model_fit;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening | Outputs forbidden in this phase |
| phase207_next_best_action | run_phase208_feature_matrix_quality_gate_no_model_no_replay | Recommended next milestone |

## Allowed Feature Matrix

| phase207_matrix_id | phase206_feature_id | feature_family | horizon_sec | required_columns | present_columns | required_column_count | present_column_count | feature_available | partition_rows | trade_dates | symbols | total_feature_rows | model_fit_allowed | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P206_RECEIVE_EVENT_RATE_ZSCORE_H1s | P206_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | 1 | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | 3 | 3 | 1 | 224 | 7 | 32 | 2165652 | 0 | 0 | 0 |
| P206_RECEIVE_EVENT_RATE_ZSCORE_H5s | P206_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | 5 | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | 3 | 3 | 1 | 224 | 7 | 32 | 818832 | 0 | 0 | 0 |
| P206_RECEIVE_EVENT_RATE_ZSCORE_H15s | P206_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | 15 | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | 3 | 3 | 1 | 224 | 7 | 32 | 286633 | 0 | 0 | 0 |
| P206_RECEIVE_EVENT_RATE_ZSCORE_H60s | P206_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | 60 | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | 3 | 3 | 1 | 224 | 7 | 32 | 72139 | 0 | 0 | 0 |
| P206_QUOTE_CHURN_RATE_H1s | P206_QUOTE_CHURN_RATE | book_state_churn | 1 | quote_churn_count | quote_churn_count | 1 | 1 | 1 | 224 | 7 | 32 | 2165652 | 0 | 0 | 0 |
| P206_QUOTE_CHURN_RATE_H5s | P206_QUOTE_CHURN_RATE | book_state_churn | 5 | quote_churn_count | quote_churn_count | 1 | 1 | 1 | 224 | 7 | 32 | 818832 | 0 | 0 | 0 |
| P206_QUOTE_CHURN_RATE_H15s | P206_QUOTE_CHURN_RATE | book_state_churn | 15 | quote_churn_count | quote_churn_count | 1 | 1 | 1 | 224 | 7 | 32 | 286633 | 0 | 0 | 0 |
| P206_QUOTE_CHURN_RATE_H60s | P206_QUOTE_CHURN_RATE | book_state_churn | 60 | quote_churn_count | quote_churn_count | 1 | 1 | 1 | 224 | 7 | 32 | 72139 | 0 | 0 | 0 |
| P206_DEPTH_REFRESH_INTENSITY_H1s | P206_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | 1 | depth_refresh_count;top5_qty_imbalance | depth_refresh_count;top5_qty_imbalance | 2 | 2 | 1 | 224 | 7 | 32 | 2165652 | 0 | 0 | 0 |
| P206_DEPTH_REFRESH_INTENSITY_H5s | P206_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | 5 | depth_refresh_count;top5_qty_imbalance | depth_refresh_count;top5_qty_imbalance | 2 | 2 | 1 | 224 | 7 | 32 | 818832 | 0 | 0 | 0 |
| P206_DEPTH_REFRESH_INTENSITY_H15s | P206_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | 15 | depth_refresh_count;top5_qty_imbalance | depth_refresh_count;top5_qty_imbalance | 2 | 2 | 1 | 224 | 7 | 32 | 286633 | 0 | 0 | 0 |
| P206_DEPTH_REFRESH_INTENSITY_H60s | P206_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | 60 | depth_refresh_count;top5_qty_imbalance | depth_refresh_count;top5_qty_imbalance | 2 | 2 | 1 | 224 | 7 | 32 | 72139 | 0 | 0 | 0 |
| P206_STALE_QUOTE_DURATION_H1s | P206_STALE_QUOTE_DURATION | feed_staleness | 1 | stale_quote_duration_ms | stale_quote_duration_ms | 1 | 1 | 1 | 224 | 7 | 32 | 2165652 | 0 | 0 | 0 |
| P206_STALE_QUOTE_DURATION_H5s | P206_STALE_QUOTE_DURATION | feed_staleness | 5 | stale_quote_duration_ms | stale_quote_duration_ms | 1 | 1 | 1 | 224 | 7 | 32 | 818832 | 0 | 0 | 0 |
| P206_STALE_QUOTE_DURATION_H15s | P206_STALE_QUOTE_DURATION | feed_staleness | 15 | stale_quote_duration_ms | stale_quote_duration_ms | 1 | 1 | 1 | 224 | 7 | 32 | 286633 | 0 | 0 | 0 |
| P206_STALE_QUOTE_DURATION_H60s | P206_STALE_QUOTE_DURATION | feed_staleness | 60 | stale_quote_duration_ms | stale_quote_duration_ms | 1 | 1 | 1 | 224 | 7 | 32 | 72139 | 0 | 0 | 0 |
| P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H1s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | 1 | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | 3 | 3 | 1 | 224 | 7 | 32 | 2165652 | 0 | 0 | 0 |
| P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H5s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | 5 | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | 3 | 3 | 1 | 224 | 7 | 32 | 818832 | 0 | 0 | 0 |
| P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H15s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | 15 | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | 3 | 3 | 1 | 224 | 7 | 32 | 286633 | 0 | 0 | 0 |
| P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_H60s | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | 60 | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | cross_symbol_arrival_count;cross_symbol_arrival_share;phase176_universe_symbols | 3 | 3 | 1 | 224 | 7 | 32 | 72139 | 0 | 0 | 0 |
| P206_RECEIVE_FLOW_REGIME_STATE_H1s | P206_RECEIVE_FLOW_REGIME_STATE | source_quality_context | 1 | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | 4 | 4 | 1 | 224 | 7 | 32 | 2165652 | 0 | 0 | 0 |
| P206_RECEIVE_FLOW_REGIME_STATE_H5s | P206_RECEIVE_FLOW_REGIME_STATE | source_quality_context | 5 | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | 4 | 4 | 1 | 224 | 7 | 32 | 818832 | 0 | 0 | 0 |
| P206_RECEIVE_FLOW_REGIME_STATE_H15s | P206_RECEIVE_FLOW_REGIME_STATE | source_quality_context | 15 | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | 4 | 4 | 1 | 224 | 7 | 32 | 286633 | 0 | 0 | 0 |
| P206_RECEIVE_FLOW_REGIME_STATE_H60s | P206_RECEIVE_FLOW_REGIME_STATE | source_quality_context | 60 | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | receive_event_rate_zscore;quote_churn_count;stale_quote_duration_ms;cross_symbol_arrival_share | 4 | 4 | 1 | 224 | 7 | 32 | 72139 | 0 | 0 | 0 |

## Target Exclusion and Negative-control Ablation Spec

| ablation_id | feature_id | required_before_model_fit | spec | matrix_rows_available | model_fit_allowed | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| P207_TARGET_SYMBOL_EXCLUDED_SYNCHRONY | P206_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | 1 | Future synchrony features must recompute cross_symbol_arrival_count/share excluding the target symbol before any model fitting. | 4 | 0 | 0 |
| P207_SHUFFLED_TIME_NEGATIVE_CONTROL | all_phase206_features | 1 | Any future model phase must include shuffled-time/date negative controls before edge interpretation. | 24 | 0 | 0 |
| P207_BLOCKED_FORM_OVERLAP_CONTROL | all_phase206_features | 1 | Any future model phase must prove no reuse of Phase164 forms, fixed Phase167 S08 score, or passive queue replay. | 24 | 0 | 0 |

## Leakage and Terminology Audit

| audit_id | audit_pass | evidence | model_fit_allowed |
| --- | --- | --- | --- |
| P207_LEAKAGE_CONTROLS_PRESENT | 1 | leakage_rows=6; feature_rows=6 | 0 |
| P207_TOP_FIVE_TERMINOLOGY_CORRECT | 1 | depth features are top-five market-by-price, not L3/L4 order-by-order | 0 |
| P207_MATRIX_NO_MODEL_OR_REPLAY_FLAGS | 1 | all matrix model/replay flags are 0 | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P207_PHASE206_COMPLETE | True | phase206_complete=1 | hard |
| P207_FEATURE_MATRIX_RECORDED | True | matrix_rows=24 | hard |
| P207_FEATURE_AVAILABILITY_POSITIVE | True | available_rows=24 | hard |
| P207_TARGET_EXCLUSION_ABLATION_SPEC_RECORDED | True | ablation_rows=3 | hard |
| P207_LEAKAGE_TERMINOLOGY_AUDIT_PASSED | True | audit_pass_rows=3 | hard |
| P207_NO_MODEL_FIT_REPLAY_OR_PROMOTION | True | forbidden_flag_sum=0 | hard |

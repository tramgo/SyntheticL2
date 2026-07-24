# Phase177 Receive-flow Feature Quality Audit

Generated UTC: 2026-07-24T11:07:19.663310+00:00

Phase177 is the quality-audit scaffold for Phase176 materialized receive-flow features.
When no feature parquet exists, Phase177 writes check catalog and gates only.
It does not emit signals, orders, fills, P&L, profitability claims, or paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase177_quality_check_rows | 30 | Predeclared feature-quality checks |
| phase177_gate_rows | 4 | Gates evaluated |
| phase177_hard_gate_rows | 2 | Hard gates evaluated |
| phase177_hard_gate_pass_rows | 2 | Hard gates passed |
| phase177_features_materialized | 0 | Inherited Phase176 feature materialization flag |
| phase177_feature_quality_audit_ran | 0 | 1 means feature-quality metrics were computed |
| phase177_strategy_replay_allowed | 0 | No strategy replay opened |
| phase177_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase177_forbidden_outputs | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | Outputs forbidden in this phase |
| phase177_next_best_action | add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_then_rerun_phase174_phase172_phase175_phase176_before_phase177 | Recommended next milestone |

## Quality Check Catalog

| feature_id | quality_check_id | check_family | definition | minimum_required_before_phase178 | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- |
| P175_RECEIVE_EVENT_RATE_ZSCORE | P177_P175_RECEIVE_EVENT_RATE_ZSCORE_COVERAGE_BY_DATE_SYMBOL_HORIZON | coverage_by_date_symbol_horizon | coverage rows must be reported for every materialized feature/date/symbol/horizon | pass_or_emit_blocking_gap_ledger | 0 |
| P175_RECEIVE_EVENT_RATE_ZSCORE | P177_P175_RECEIVE_EVENT_RATE_ZSCORE_STALENESS_AND_FORWARD_FILL | staleness_and_forward_fill | stale fraction and forward-fill fraction must be bounded and reported per symbol/horizon | pass_or_emit_blocking_gap_ledger | 0 |
| P175_RECEIVE_EVENT_RATE_ZSCORE | P177_P175_RECEIVE_EVENT_RATE_ZSCORE_TRAIN_TEST_LEAKAGE | train_test_leakage | train-fitted transforms only; no future receive events in any feature timestamp | pass_or_emit_blocking_gap_ledger | 0 |
| P175_RECEIVE_EVENT_RATE_ZSCORE | P177_P175_RECEIVE_EVENT_RATE_ZSCORE_BLOCKED_FAMILY_OVERLAP | blocked_family_overlap | feature names and formulas must not reproduce Phase164/Phase167/Phase131-136 blocked strategy forms | pass_or_emit_blocking_gap_ledger | 0 |
| P175_RECEIVE_EVENT_RATE_ZSCORE | P177_P175_RECEIVE_EVENT_RATE_ZSCORE_SCHEMA_AND_NULL_RATES | schema_and_null_rates | required feature columns must exist with null rates below predeclared thresholds | pass_or_emit_blocking_gap_ledger | 0 |
| P175_QUOTE_CHURN_RATE | P177_P175_QUOTE_CHURN_RATE_COVERAGE_BY_DATE_SYMBOL_HORIZON | coverage_by_date_symbol_horizon | coverage rows must be reported for every materialized feature/date/symbol/horizon | pass_or_emit_blocking_gap_ledger | 0 |
| P175_QUOTE_CHURN_RATE | P177_P175_QUOTE_CHURN_RATE_STALENESS_AND_FORWARD_FILL | staleness_and_forward_fill | stale fraction and forward-fill fraction must be bounded and reported per symbol/horizon | pass_or_emit_blocking_gap_ledger | 0 |
| P175_QUOTE_CHURN_RATE | P177_P175_QUOTE_CHURN_RATE_TRAIN_TEST_LEAKAGE | train_test_leakage | train-fitted transforms only; no future receive events in any feature timestamp | pass_or_emit_blocking_gap_ledger | 0 |
| P175_QUOTE_CHURN_RATE | P177_P175_QUOTE_CHURN_RATE_BLOCKED_FAMILY_OVERLAP | blocked_family_overlap | feature names and formulas must not reproduce Phase164/Phase167/Phase131-136 blocked strategy forms | pass_or_emit_blocking_gap_ledger | 0 |
| P175_QUOTE_CHURN_RATE | P177_P175_QUOTE_CHURN_RATE_SCHEMA_AND_NULL_RATES | schema_and_null_rates | required feature columns must exist with null rates below predeclared thresholds | pass_or_emit_blocking_gap_ledger | 0 |
| P175_DEPTH_REFRESH_INTENSITY | P177_P175_DEPTH_REFRESH_INTENSITY_COVERAGE_BY_DATE_SYMBOL_HORIZON | coverage_by_date_symbol_horizon | coverage rows must be reported for every materialized feature/date/symbol/horizon | pass_or_emit_blocking_gap_ledger | 0 |
| P175_DEPTH_REFRESH_INTENSITY | P177_P175_DEPTH_REFRESH_INTENSITY_STALENESS_AND_FORWARD_FILL | staleness_and_forward_fill | stale fraction and forward-fill fraction must be bounded and reported per symbol/horizon | pass_or_emit_blocking_gap_ledger | 0 |
| P175_DEPTH_REFRESH_INTENSITY | P177_P175_DEPTH_REFRESH_INTENSITY_TRAIN_TEST_LEAKAGE | train_test_leakage | train-fitted transforms only; no future receive events in any feature timestamp | pass_or_emit_blocking_gap_ledger | 0 |
| P175_DEPTH_REFRESH_INTENSITY | P177_P175_DEPTH_REFRESH_INTENSITY_BLOCKED_FAMILY_OVERLAP | blocked_family_overlap | feature names and formulas must not reproduce Phase164/Phase167/Phase131-136 blocked strategy forms | pass_or_emit_blocking_gap_ledger | 0 |
| P175_DEPTH_REFRESH_INTENSITY | P177_P175_DEPTH_REFRESH_INTENSITY_SCHEMA_AND_NULL_RATES | schema_and_null_rates | required feature columns must exist with null rates below predeclared thresholds | pass_or_emit_blocking_gap_ledger | 0 |
| P175_STALE_QUOTE_DURATION | P177_P175_STALE_QUOTE_DURATION_COVERAGE_BY_DATE_SYMBOL_HORIZON | coverage_by_date_symbol_horizon | coverage rows must be reported for every materialized feature/date/symbol/horizon | pass_or_emit_blocking_gap_ledger | 0 |
| P175_STALE_QUOTE_DURATION | P177_P175_STALE_QUOTE_DURATION_STALENESS_AND_FORWARD_FILL | staleness_and_forward_fill | stale fraction and forward-fill fraction must be bounded and reported per symbol/horizon | pass_or_emit_blocking_gap_ledger | 0 |
| P175_STALE_QUOTE_DURATION | P177_P175_STALE_QUOTE_DURATION_TRAIN_TEST_LEAKAGE | train_test_leakage | train-fitted transforms only; no future receive events in any feature timestamp | pass_or_emit_blocking_gap_ledger | 0 |
| P175_STALE_QUOTE_DURATION | P177_P175_STALE_QUOTE_DURATION_BLOCKED_FAMILY_OVERLAP | blocked_family_overlap | feature names and formulas must not reproduce Phase164/Phase167/Phase131-136 blocked strategy forms | pass_or_emit_blocking_gap_ledger | 0 |
| P175_STALE_QUOTE_DURATION | P177_P175_STALE_QUOTE_DURATION_SCHEMA_AND_NULL_RATES | schema_and_null_rates | required feature columns must exist with null rates below predeclared thresholds | pass_or_emit_blocking_gap_ledger | 0 |
| P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | P177_P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_COVERAGE_BY_DATE_SYMBOL_HORIZON | coverage_by_date_symbol_horizon | coverage rows must be reported for every materialized feature/date/symbol/horizon | pass_or_emit_blocking_gap_ledger | 0 |
| P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | P177_P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_STALENESS_AND_FORWARD_FILL | staleness_and_forward_fill | stale fraction and forward-fill fraction must be bounded and reported per symbol/horizon | pass_or_emit_blocking_gap_ledger | 0 |
| P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | P177_P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_TRAIN_TEST_LEAKAGE | train_test_leakage | train-fitted transforms only; no future receive events in any feature timestamp | pass_or_emit_blocking_gap_ledger | 0 |
| P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | P177_P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_BLOCKED_FAMILY_OVERLAP | blocked_family_overlap | feature names and formulas must not reproduce Phase164/Phase167/Phase131-136 blocked strategy forms | pass_or_emit_blocking_gap_ledger | 0 |
| P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | P177_P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY_SCHEMA_AND_NULL_RATES | schema_and_null_rates | required feature columns must exist with null rates below predeclared thresholds | pass_or_emit_blocking_gap_ledger | 0 |
| P175_RECEIVE_FLOW_REGIME_STATE | P177_P175_RECEIVE_FLOW_REGIME_STATE_COVERAGE_BY_DATE_SYMBOL_HORIZON | coverage_by_date_symbol_horizon | coverage rows must be reported for every materialized feature/date/symbol/horizon | pass_or_emit_blocking_gap_ledger | 0 |
| P175_RECEIVE_FLOW_REGIME_STATE | P177_P175_RECEIVE_FLOW_REGIME_STATE_STALENESS_AND_FORWARD_FILL | staleness_and_forward_fill | stale fraction and forward-fill fraction must be bounded and reported per symbol/horizon | pass_or_emit_blocking_gap_ledger | 0 |
| P175_RECEIVE_FLOW_REGIME_STATE | P177_P175_RECEIVE_FLOW_REGIME_STATE_TRAIN_TEST_LEAKAGE | train_test_leakage | train-fitted transforms only; no future receive events in any feature timestamp | pass_or_emit_blocking_gap_ledger | 0 |
| P175_RECEIVE_FLOW_REGIME_STATE | P177_P175_RECEIVE_FLOW_REGIME_STATE_BLOCKED_FAMILY_OVERLAP | blocked_family_overlap | feature names and formulas must not reproduce Phase164/Phase167/Phase131-136 blocked strategy forms | pass_or_emit_blocking_gap_ledger | 0 |
| P175_RECEIVE_FLOW_REGIME_STATE | P177_P175_RECEIVE_FLOW_REGIME_STATE_SCHEMA_AND_NULL_RATES | schema_and_null_rates | required feature columns must exist with null rates below predeclared thresholds | pass_or_emit_blocking_gap_ledger | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P177_PHASE176_FEATURES_MATERIALIZED | 0 | phase176_features_materialized=0 | activation |
| P177_FEATURE_ROOT_HAS_PARQUET | 0 | feature_root=derived_real_l2_receive_flow_features_phase176;parquet_files=0 | activation |
| P177_SCHEMA_AVAILABLE | 1 | feature_schema_rows=6 | hard |
| P177_NO_REPLAY_OR_PROFITABILITY_OUTPUTS | 1 | feature-quality scaffold only while materialization gate is closed; forbidden_outputs=buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | hard |

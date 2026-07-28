# Phase197 Non-Receive-Flow Feature Expansion Precommit

Generated UTC: 2026-07-28T19:54:27.361187+00:00

Phase197 responds to the Phase196 no-survivor result by precommitting broader context features.
It is not a strategy replay and it does not use the untouched test split.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase197_feature_contract_rows | 5 | Non-receive-flow feature family rows precommitted |
| phase197_availability_audit_rows | 15 | Feature/split availability rows |
| phase197_ready_feature_families | 5 | Feature families ready for future train/validation search |
| phase197_gate_rows | 7 | Gates evaluated |
| phase197_hard_gate_rows | 7 | Hard gates evaluated |
| phase197_hard_gate_pass_rows | 7 | Hard gates passed |
| phase197_non_receive_flow_feature_precommit_complete | 1 | 1 means Phase197 completed |
| phase197_strategy_replay_allowed | 0 | No strategy replay opened |
| phase197_test_replay_allowed_next | 0 | No test replay opened |
| phase197_promotion_allowed | 0 | No promotion opened |
| phase197_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase197_forbidden_outputs | test_result;test_replay_execution;strategy_replay;order_arrival;fill_model;pnl_replay;profitability_claim;promotion;paper_live_acceptance | Outputs forbidden in this phase |
| phase197_next_best_action | run_phase198_non_receive_flow_context_model_search_no_test | Recommended next milestone |

## Phase198 Candidate Matrix

| feature_id | feature_family | candidate_columns | derivation | non_receive_flow_dimension | leakage_boundary | precommit_status | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed | train_available | unassigned_available | validation_available | ready_for_phase198_search | phase198_allowed_use |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P197_TIME_OF_DAY_CONTEXT | intraday_time_context | seconds_from_open_ist;time_of_day_sin_ist;time_of_day_cos_ist | bucket timestamp transformed to IST session-relative features | session_clock | uses timestamp only; no target or future data | candidate_for_phase198_search_only | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | train_selection_and_validation_extension_screen_no_test |
| P197_SYMBOL_LIQUIDITY_REGIME | symbol_liquidity_regime | symbol_train_spread_bps_median;symbol_train_receive_event_count_median;relative_spread_to_symbol_train_median;relative_receive_count_to_symbol_train_median | symbol baselines fitted on train split only and applied to non-test rows | symbol_baseline_liquidity | train-only baselines; validation/unassigned not used for fitting | candidate_for_phase198_search_only | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | train_selection_and_validation_extension_screen_no_test |
| P197_MARKET_CONTEXT_LAGGED | lagged_market_context | prior_market_active_symbol_count;prior_market_median_spread_bps;prior_market_median_top5_imbalance;prior_market_receive_event_count_sum;prior_market_cross_symbol_arrival_share | cross-sectional market context lagged by one receive bucket | market_regime_context | prior bucket only; no same-bucket target return and no future data | candidate_for_phase198_search_only | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | train_selection_and_validation_extension_screen_no_test |
| P197_ASSET_CLASS_PROXY | instrument_context | asset_class_proxy | static symbol-name proxy for equity versus ETF-like BEES instruments | instrument_type | static symbol metadata proxy; no target data | candidate_for_phase198_search_only | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | train_selection_and_validation_extension_screen_no_test |
| P197_MICROSTRUCTURE_TRANSFORMS | nonlinear_microstructure_context | spread_bps;quote_churn_log;depth_refresh_log;stale_quote_log_ms | current observable L1/top-five state transformed into stable nonlinear context fields | liquidity_and_staleness_context | computed from current-or-prior observed book state only | candidate_for_phase198_search_only | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | train_selection_and_validation_extension_screen_no_test |

## Feature Availability Audit

| feature_id | feature_family | split_role | rows_scanned | candidate_columns | present_column_count | required_column_count | min_usable_rows_any_column | feature_available_for_future_search | test_rows_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P197_TIME_OF_DAY_CONTEXT | intraday_time_context | train | 1079615 | seconds_from_open_ist;time_of_day_sin_ist;time_of_day_cos_ist | 3 | 3 | 1079615 | 1 | 0 |
| P197_TIME_OF_DAY_CONTEXT | intraday_time_context | unassigned | 1133776 | seconds_from_open_ist;time_of_day_sin_ist;time_of_day_cos_ist | 3 | 3 | 1133776 | 1 | 0 |
| P197_TIME_OF_DAY_CONTEXT | intraday_time_context | validation | 561386 | seconds_from_open_ist;time_of_day_sin_ist;time_of_day_cos_ist | 3 | 3 | 561386 | 1 | 0 |
| P197_SYMBOL_LIQUIDITY_REGIME | symbol_liquidity_regime | train | 1079615 | symbol_train_spread_bps_median;symbol_train_receive_event_count_median;relative_spread_to_symbol_train_median;relative_receive_count_to_symbol_train_median | 4 | 4 | 1079615 | 1 | 0 |
| P197_SYMBOL_LIQUIDITY_REGIME | symbol_liquidity_regime | unassigned | 1133776 | symbol_train_spread_bps_median;symbol_train_receive_event_count_median;relative_spread_to_symbol_train_median;relative_receive_count_to_symbol_train_median | 4 | 4 | 1133776 | 1 | 0 |
| P197_SYMBOL_LIQUIDITY_REGIME | symbol_liquidity_regime | validation | 561386 | symbol_train_spread_bps_median;symbol_train_receive_event_count_median;relative_spread_to_symbol_train_median;relative_receive_count_to_symbol_train_median | 4 | 4 | 561386 | 1 | 0 |
| P197_MARKET_CONTEXT_LAGGED | lagged_market_context | train | 1079615 | prior_market_active_symbol_count;prior_market_median_spread_bps;prior_market_median_top5_imbalance;prior_market_receive_event_count_sum;prior_market_cross_symbol_arrival_share | 5 | 5 | 1079524 | 1 | 0 |
| P197_MARKET_CONTEXT_LAGGED | lagged_market_context | unassigned | 1133776 | prior_market_active_symbol_count;prior_market_median_spread_bps;prior_market_median_top5_imbalance;prior_market_receive_event_count_sum;prior_market_cross_symbol_arrival_share | 5 | 5 | 1133722 | 1 | 0 |
| P197_MARKET_CONTEXT_LAGGED | lagged_market_context | validation | 561386 | prior_market_active_symbol_count;prior_market_median_spread_bps;prior_market_median_top5_imbalance;prior_market_receive_event_count_sum;prior_market_cross_symbol_arrival_share | 5 | 5 | 561359 | 1 | 0 |
| P197_ASSET_CLASS_PROXY | instrument_context | train | 1079615 | asset_class_proxy | 1 | 1 | 1079615 | 1 | 0 |
| P197_ASSET_CLASS_PROXY | instrument_context | unassigned | 1133776 | asset_class_proxy | 1 | 1 | 1133776 | 1 | 0 |
| P197_ASSET_CLASS_PROXY | instrument_context | validation | 561386 | asset_class_proxy | 1 | 1 | 561386 | 1 | 0 |
| P197_MICROSTRUCTURE_TRANSFORMS | nonlinear_microstructure_context | train | 1079615 | spread_bps;quote_churn_log;depth_refresh_log;stale_quote_log_ms | 4 | 4 | 1079615 | 1 | 0 |
| P197_MICROSTRUCTURE_TRANSFORMS | nonlinear_microstructure_context | unassigned | 1133776 | spread_bps;quote_churn_log;depth_refresh_log;stale_quote_log_ms | 4 | 4 | 1133776 | 1 | 0 |
| P197_MICROSTRUCTURE_TRANSFORMS | nonlinear_microstructure_context | validation | 561386 | spread_bps;quote_churn_log;depth_refresh_log;stale_quote_log_ms | 4 | 4 | 561386 | 1 | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P197_PHASE196_COMPLETE | 1 | phase196_expanded_model_search_complete=1 | hard |
| P197_FEATURE_CONTRACT_RECORDED | 1 | feature_contract_rows=5 | hard |
| P197_AVAILABILITY_AUDIT_RECORDED | 1 | availability_rows=15 | hard |
| P197_TEST_SPLIT_NOT_USED | 1 | test_partitions_used=0 | hard |
| P197_LEAKAGE_BOUNDARIES_RECORDED | 1 | leakage_boundary_rows=5 | hard |
| P197_PHASE198_READY_FEATURES_RECORDED | 1 | ready_feature_families=5 | hard |
| P197_NO_REPLAY_OR_PROMOTION | 1 | strategy_replay=0; test_replay=0; promotion=0; paper_live=0 | hard |

# Phase184 Train/Validation Replay Dry-run

Generated UTC: 2026-07-28T16:43:13.972301+00:00

Phase184 runs a train/validation-only dry replay over the audited receive-flow feature and label stack.
It binds Phase180 retail/stressed cost and latency profiles and includes shuffled negative controls.
It does not use test rows, emit orders/fills, calculate contract-note P&L, claim profitability, open paper/live acceptance, or promote any candidate.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase184_partition_rows_scanned | 640 | Feature/label partitions scanned |
| phase184_train_partitions_used | 384 | Train partitions used |
| phase184_validation_partitions_used | 128 | Validation partitions used |
| phase184_test_partitions_used | 0 | Test partitions used |
| phase184_train_rows_used | 1079615 | Train rows used |
| phase184_validation_rows_used | 561386 | Validation rows used |
| phase184_fit_parameter_rows | 3 | Train-fitted family parameter rows |
| phase184_dry_run_summary_rows | 36 | Dry-run summary rows |
| phase184_gate_rows | 8 | Gates evaluated |
| phase184_hard_gate_rows | 8 | Hard gates evaluated |
| phase184_hard_gate_pass_rows | 8 | Hard gates passed |
| phase184_train_validation_dry_run_complete | 1 | 1 means Phase184 dry run completed |
| phase184_strategy_replay_dry_run_performed | 1 | Dry replay summary performed without orders/fills/P&L |
| phase184_test_rows_used | 0 | Test rows remain untouched |
| phase184_promotion_allowed | 0 | No promotion opened |
| phase184_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase184_forbidden_outputs | order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance;test_result;promotion | Outputs forbidden in this phase |
| phase184_next_best_action | build_phase185_validation_replay_interpretation_and_kill_switch_audit_no_test | Recommended next milestone |

## Validation Selection Screen

| strategy_family_id | latency_profile_id | split_role | control_name | dry_decision_events | gross_return_bps_proxy_mean | cost_bound_bps_mean | net_return_bps_after_cost_proxy_mean | net_positive_event_fraction | promotion_allowed | test_rows_used | rank_validation_net_proxy | selected_for_future_test_replay | selection_interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P179_RECEIVE_CADENCE_SHOCK_CONTEXT | P180_RETAIL_MARKETABLE_DEFAULT | validation | actual_time_order | 106368 | 2.11874 | 14.8516 | -12.7329 | 0.00480408 | 0 | 0 | 1 | 0 | validation screen only; no test rows used and no promotion opened |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_RETAIL_MARKETABLE_DEFAULT | validation | actual_time_order | 118056 | 1.40326 | 15.1626 | -13.7593 | 0.00418445 | 0 | 0 | 2 | 0 | validation screen only; no test rows used and no promotion opened |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_RETAIL_MARKETABLE_DEFAULT | validation | actual_time_order | 114425 | 0.219509 | 14.7775 | -14.558 | 0.00407254 | 0 | 0 | 3 | 0 | validation screen only; no test rows used and no promotion opened |
| P179_RECEIVE_CADENCE_SHOCK_CONTEXT | P180_STRESSED_RETAIL | validation | actual_time_order | 106368 | 2.11874 | 18.1349 | -16.0161 | 0.00362891 | 0 | 0 | 4 | 0 | validation screen only; no test rows used and no promotion opened |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_STRESSED_RETAIL | validation | actual_time_order | 118056 | 1.40326 | 18.6946 | -17.2914 | 0.00313411 | 0 | 0 | 5 | 0 | validation screen only; no test rows used and no promotion opened |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_STRESSED_RETAIL | validation | actual_time_order | 114425 | 0.219509 | 17.9491 | -17.7295 | 0.00305877 | 0 | 0 | 6 | 0 | validation screen only; no test rows used and no promotion opened |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P184_PHASE183_REPLAY_READINESS_PRECOMMITTED | 1 | phase183_replay_readiness_precommitted=1 | hard |
| P184_TRAIN_ROWS_PRESENT | 1 | train_rows=1079615 | hard |
| P184_VALIDATION_ROWS_PRESENT | 1 | validation_rows=561386 | hard |
| P184_TEST_ROWS_UNTOUCHED | 1 | test_rows_used=0 | hard |
| P184_TRAIN_ONLY_FIT_PARAMETERS | 1 | fit_parameter_rows=3 | hard |
| P184_COST_LATENCY_BOUND_SUMMARY | 1 | summary_rows=36 | hard |
| P184_NEGATIVE_CONTROLS_PRESENT | 1 | control_rows=24 | hard |
| P184_NO_PROMOTION_OR_PAPER_LIVE | 1 | promotion_allowed=0; paper_live_acceptance_allowed=0 | hard |

## Dry-run Summary Sample

| strategy_family_id | latency_profile_id | split_role | control_name | dry_decision_events | gross_return_bps_proxy_mean | cost_bound_bps_mean | net_return_bps_after_cost_proxy_mean | net_positive_event_fraction | promotion_allowed | test_rows_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_RETAIL_MARKETABLE_DEFAULT | train | actual_time_order | 223455 | 5.07401 | 14.7004 | -9.62638 | 0.00299837 | 0 | 0 |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_RETAIL_MARKETABLE_DEFAULT | train | shuffled_time_negative_control | 223455 | 0.634413 | 14.7004 | -14.066 | 0.00341903 | 0 | 0 |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_RETAIL_MARKETABLE_DEFAULT | train | shuffled_symbol_negative_control | 223455 | 0.444889 | 14.7004 | -14.2555 | 0.00152603 | 0 | 0 |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_RETAIL_MARKETABLE_DEFAULT | validation | actual_time_order | 114425 | 0.219509 | 14.7775 | -14.558 | 0.00407254 | 0 | 0 |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_RETAIL_MARKETABLE_DEFAULT | validation | shuffled_time_negative_control | 114425 | 0.868517 | 14.7775 | -13.909 | 0.00322482 | 0 | 0 |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_RETAIL_MARKETABLE_DEFAULT | validation | shuffled_symbol_negative_control | 114425 | -0.882995 | 14.7775 | -15.6605 | 0.00120603 | 0 | 0 |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_STRESSED_RETAIL | train | actual_time_order | 223455 | 5.07401 | 17.8865 | -12.8125 | 0.00218388 | 0 | 0 |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_STRESSED_RETAIL | train | shuffled_time_negative_control | 223455 | 0.634413 | 17.8865 | -17.2521 | 0.00265378 | 0 | 0 |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_STRESSED_RETAIL | train | shuffled_symbol_negative_control | 223455 | 0.444889 | 17.8865 | -17.4416 | 0.00121725 | 0 | 0 |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_STRESSED_RETAIL | validation | actual_time_order | 114425 | 0.219509 | 17.9491 | -17.7295 | 0.00305877 | 0 | 0 |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_STRESSED_RETAIL | validation | shuffled_time_negative_control | 114425 | 0.868517 | 17.9491 | -17.0805 | 0.00218484 | 0 | 0 |
| P179_SOURCE_QUALITY_REGIME_FILTER | P180_STRESSED_RETAIL | validation | shuffled_symbol_negative_control | 114425 | -0.882995 | 17.9491 | -18.8321 | 0.000873935 | 0 | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_RETAIL_MARKETABLE_DEFAULT | train | actual_time_order | 220402 | 1.69544 | 14.7741 | -13.0787 | 0.0031624 | 0 | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_RETAIL_MARKETABLE_DEFAULT | train | shuffled_time_negative_control | 220402 | -0.512872 | 14.7741 | -15.287 | 0.00352084 | 0 | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_RETAIL_MARKETABLE_DEFAULT | train | shuffled_symbol_negative_control | 220402 | 0.141433 | 14.7741 | -14.6327 | 0.00158801 | 0 | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_RETAIL_MARKETABLE_DEFAULT | validation | actual_time_order | 118056 | 1.40326 | 15.1626 | -13.7593 | 0.00418445 | 0 | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_RETAIL_MARKETABLE_DEFAULT | validation | shuffled_time_negative_control | 118056 | 0.598506 | 15.1626 | -14.5641 | 0.00357457 | 0 | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_RETAIL_MARKETABLE_DEFAULT | validation | shuffled_symbol_negative_control | 118056 | -0.431685 | 15.1626 | -15.5943 | 0.00130447 | 0 | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_STRESSED_RETAIL | train | actual_time_order | 220402 | 1.69544 | 18.0642 | -16.3688 | 0.00225043 | 0 | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_STRESSED_RETAIL | train | shuffled_time_negative_control | 220402 | -0.512872 | 18.0642 | -18.5771 | 0.00259526 | 0 | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_STRESSED_RETAIL | train | shuffled_symbol_negative_control | 220402 | 0.141433 | 18.0642 | -17.9228 | 0.00117966 | 0 | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_STRESSED_RETAIL | validation | actual_time_order | 118056 | 1.40326 | 18.6946 | -17.2914 | 0.00313411 | 0 | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_STRESSED_RETAIL | validation | shuffled_time_negative_control | 118056 | 0.598506 | 18.6946 | -18.0961 | 0.00265128 | 0 | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | P180_STRESSED_RETAIL | validation | shuffled_symbol_negative_control | 118056 | -0.431685 | 18.6946 | -19.1263 | 0.000991055 | 0 | 0 |

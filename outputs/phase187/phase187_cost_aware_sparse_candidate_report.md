# Phase187 Cost-aware Sparse Receive-flow Candidate

Generated UTC: 2026-07-28T16:57:22.691630+00:00

Phase187 builds a redesigned sparse candidate grid after Phase186 closed the previous receive-flow family set.
Selection is train-only; validation is evaluation-only; test replay, promotion, paper/live acceptance and P&L remain closed.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase187_candidate_grid_rows | 216 | Sparse candidate grid rows |
| phase187_train_selected_candidate_rows | 12 | Train-selected candidate rows |
| phase187_validation_summary_rows | 24 | Validation summary rows |
| phase187_best_validation_candidate_id | P187_TOP5_I85_S2p5_Z1_R100 | Best validation candidate |
| phase187_best_validation_latency_profile | P180_RETAIL_MARKETABLE_DEFAULT | Best validation latency profile |
| phase187_best_validation_net_bps_proxy_mean | 48.3994 | Best validation net return-bps proxy mean |
| phase187_validation_positive_all_profiles | 1 | 1 means at least one candidate is net positive under all allowed profiles |
| phase187_gate_rows | 7 | Gates evaluated |
| phase187_hard_gate_rows | 7 | Hard gates evaluated |
| phase187_hard_gate_pass_rows | 7 | Hard gates passed |
| phase187_cost_aware_sparse_candidate_complete | 1 | 1 means Phase187 completed |
| phase187_test_rows_used | 0 | Test rows remain untouched |
| phase187_test_replay_allowed_next | 0 | No test replay opened by Phase187 |
| phase187_promotion_allowed | 0 | No promotion opened |
| phase187_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase187_forbidden_outputs | test_result;test_replay;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim | Outputs forbidden in this phase |
| phase187_next_best_action | build_phase188_cost_aware_sparse_candidate_interpretation_no_test | Recommended next milestone |

## Train-selected Candidates

| candidate_id | min_train_net_bps | min_train_edge_over_control_bps | max_decision_rate_observed | total_profile_rows | imbalance_source | min_abs_imbalance | max_spread_bps | min_abs_event_zscore | max_decision_rate | test_replay_allowed_in_phase187 | selected_by_phase187_train_only | validation_used_for_selection | test_used_for_selection |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P187_TOP5_I85_S2p5_Z1_R100 | 7.98542 | 22.5378 | 0.001658 | 2 | top5 | 0.85 | 2.5 | 1 | 0.01 | 0 | 1 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R200 | 7.98542 | 0.269191 | 0.001658 | 2 | top5 | 0.85 | 2.5 | 1 | 0.02 | 0 | 1 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R50 | 7.98542 | 0.199179 | 0.001658 | 2 | top5 | 0.85 | 2.5 | 1 | 0.005 | 0 | 1 | 0 | 0 |
| P187_TOP5_I85_S10p0_Z1_R50 | -4.97167 | 21.8123 | 0.00341048 | 2 | top5 | 0.85 | 10 | 1 | 0.005 | 0 | 1 | 0 | 0 |
| P187_TOP5_I85_S10p0_Z1_R200 | -4.97167 | 11.0039 | 0.00341048 | 2 | top5 | 0.85 | 10 | 1 | 0.02 | 0 | 1 | 0 | 0 |
| P187_TOP5_I85_S10p0_Z1_R100 | -4.97167 | 10.9628 | 0.00341048 | 2 | top5 | 0.85 | 10 | 1 | 0.01 | 0 | 1 | 0 | 0 |
| P187_TOP5_I75_S2p5_Z1_R200 | -5.13565 | 0.220576 | 0.00413203 | 2 | top5 | 0.75 | 2.5 | 1 | 0.02 | 0 | 1 | 0 | 0 |
| P187_TOP5_I75_S2p5_Z1_R50 | -5.13565 | 0.200403 | 0.00413203 | 2 | top5 | 0.75 | 2.5 | 1 | 0.005 | 0 | 1 | 0 | 0 |
| P187_TOP5_I75_S2p5_Z1_R100 | -5.13565 | 0.193838 | 0.00413203 | 2 | top5 | 0.75 | 2.5 | 1 | 0.01 | 0 | 1 | 0 | 0 |
| P187_TOP5_I65_S2p5_Z1_R100 | -9.24881 | 4.97203 | 0.0077259 | 2 | top5 | 0.65 | 2.5 | 1 | 0.01 | 0 | 1 | 0 | 0 |
| P187_TOP5_I65_S2p5_Z1_R200 | -9.24881 | 0.21066 | 0.0077259 | 2 | top5 | 0.65 | 2.5 | 1 | 0.02 | 0 | 1 | 0 | 0 |
| P187_TOP5_I85_S5p0_Z1_R200 | -10.5807 | 12.612 | 0.00296495 | 2 | top5 | 0.85 | 5 | 1 | 0.02 | 0 | 1 | 0 | 0 |

## Validation Summary

| candidate_id | latency_profile_id | split_role | decision_events | decision_rate | gross_return_bps_proxy_mean | cost_bound_bps_mean | net_return_bps_after_cost_proxy_mean | net_positive_event_fraction | shuffled_time_net_bps_proxy_mean | net_edge_over_shuffled_time_bps | test_rows_used | promotion_allowed | min_train_net_bps | min_train_edge_over_control_bps | max_decision_rate_observed | validation_net_positive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 1323 | 0.00235667 | 60.5943 | 12.195 | 48.3994 | 0.00604686 | 33.2196 | 15.1798 | 0 | 0 | 7.98542 | 22.5378 | 0.001658 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | validation | 1323 | 0.00235667 | 60.5943 | 14.2634 | 46.3309 | 0.00604686 | 0.835387 | 45.4955 | 0 | 0 | 7.98542 | 22.5378 | 0.001658 | 1 |
| P187_TOP5_I85_S2p5_Z1_R200 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 1323 | 0.00235667 | 60.5943 | 12.195 | 48.3994 | 0.00604686 | 2.94759 | 45.4518 | 0 | 0 | 7.98542 | 0.269191 | 0.001658 | 1 |
| P187_TOP5_I85_S2p5_Z1_R200 | P180_STRESSED_RETAIL | validation | 1323 | 0.00235667 | 60.5943 | 14.2634 | 46.3309 | 0.00604686 | -14.2486 | 60.5796 | 0 | 0 | 7.98542 | 0.269191 | 0.001658 | 1 |
| P187_TOP5_I85_S2p5_Z1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 1323 | 0.00235667 | 60.5943 | 12.195 | 48.3994 | 0.00604686 | -12.1779 | 60.5773 | 0 | 0 | 7.98542 | 0.199179 | 0.001658 | 1 |
| P187_TOP5_I85_S2p5_Z1_R50 | P180_STRESSED_RETAIL | validation | 1323 | 0.00235667 | 60.5943 | 14.2634 | 46.3309 | 0.00604686 | -29.3724 | 75.7033 | 0 | 0 | 7.98542 | 0.199179 | 0.001658 | 1 |
| P187_TOP5_I85_S10p0_Z1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 2414 | 0.00430007 | 33.2558 | 15.3874 | 17.8683 | 0.004971 | -31.9283 | 49.7966 | 0 | 0 | -4.97167 | 21.8123 | 0.00341048 | 1 |
| P187_TOP5_I85_S10p0_Z1_R50 | P180_STRESSED_RETAIL | validation | 2414 | 0.00430007 | 33.2558 | 18.7571 | 14.4986 | 0.004971 | 14.3738 | 0.124855 | 0 | 0 | -4.97167 | 21.8123 | 0.00341048 | 1 |
| P187_TOP5_I85_S10p0_Z1_R200 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 2414 | 0.00430007 | 33.2558 | 15.3874 | 17.8683 | 0.004971 | -23.6447 | 41.513 | 0 | 0 | -4.97167 | 11.0039 | 0.00341048 | 1 |
| P187_TOP5_I85_S10p0_Z1_R200 | P180_STRESSED_RETAIL | validation | 2414 | 0.00430007 | 33.2558 | 18.7571 | 14.4986 | 0.004971 | -2.22831 | 16.727 | 0 | 0 | -4.97167 | 11.0039 | 0.00341048 | 1 |
| P187_TOP5_I85_S10p0_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 2414 | 0.00430007 | 33.2558 | 15.3874 | 17.8683 | 0.004971 | -7.08094 | 24.9493 | 0 | 0 | -4.97167 | 10.9628 | 0.00341048 | 1 |
| P187_TOP5_I85_S10p0_Z1_R100 | P180_STRESSED_RETAIL | validation | 2414 | 0.00430007 | 33.2558 | 18.7571 | 14.4986 | 0.004971 | -27.0964 | 41.595 | 0 | 0 | -4.97167 | 10.9628 | 0.00341048 | 1 |
| P187_TOP5_I75_S2p5_Z1_R200 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 3052 | 0.00543654 | 39.4472 | 12.1046 | 27.3426 | 0.0042595 | 7.54839 | 19.7942 | 0 | 0 | -5.13565 | 0.220576 | 0.00413203 | 1 |
| P187_TOP5_I75_S2p5_Z1_R200 | P180_STRESSED_RETAIL | validation | 3052 | 0.00543654 | 39.4472 | 14.0854 | 25.3618 | 0.0042595 | -0.950007 | 26.3118 | 0 | 0 | -5.13565 | 0.220576 | 0.00413203 | 1 |
| P187_TOP5_I75_S2p5_Z1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 3052 | 0.00543654 | 39.4472 | 12.1046 | 27.3426 | 0.0042595 | -25.1953 | 52.5379 | 0 | 0 | -5.13565 | 0.200403 | 0.00413203 | 1 |
| P187_TOP5_I75_S2p5_Z1_R50 | P180_STRESSED_RETAIL | validation | 3052 | 0.00543654 | 39.4472 | 14.0854 | 25.3618 | 0.0042595 | -0.994317 | 26.3561 | 0 | 0 | -5.13565 | 0.200403 | 0.00413203 | 1 |
| P187_TOP5_I75_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 3052 | 0.00543654 | 39.4472 | 12.1046 | 27.3426 | 0.0042595 | -31.7716 | 59.1142 | 0 | 0 | -5.13565 | 0.193838 | 0.00413203 | 1 |
| P187_TOP5_I75_S2p5_Z1_R100 | P180_STRESSED_RETAIL | validation | 3052 | 0.00543654 | 39.4472 | 14.0854 | 25.3618 | 0.0042595 | -0.968215 | 26.33 | 0 | 0 | -5.13565 | 0.193838 | 0.00413203 | 1 |
| P187_TOP5_I65_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 5173 | 0.00921469 | 23.3266 | 12.1423 | 11.1842 | 0.00289967 | 3.31275 | 7.87149 | 0 | 0 | -9.24881 | 4.97203 | 0.0077259 | 1 |
| P187_TOP5_I65_S2p5_Z1_R100 | P180_STRESSED_RETAIL | validation | 5173 | 0.00921469 | 23.3266 | 14.1324 | 9.19419 | 0.00289967 | -10.2979 | 19.4921 | 0 | 0 | -9.24881 | 4.97203 | 0.0077259 | 1 |
| P187_TOP5_I65_S2p5_Z1_R200 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 5173 | 0.00921469 | 23.3266 | 12.1423 | 11.1842 | 0.00289967 | -8.29148 | 19.4757 | 0 | 0 | -9.24881 | 0.21066 | 0.0077259 | 1 |
| P187_TOP5_I65_S2p5_Z1_R200 | P180_STRESSED_RETAIL | validation | 5173 | 0.00921469 | 23.3266 | 14.1324 | 9.19419 | 0.00289967 | -14.1757 | 23.3699 | 0 | 0 | -9.24881 | 0.21066 | 0.0077259 | 1 |
| P187_TOP5_I85_S5p0_Z1_R200 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 2197 | 0.00391353 | 54.7405 | 14.8018 | 39.9387 | 0.00546199 | -23.8953 | 63.834 | 0 | 0 | -10.5807 | 12.612 | 0.00296495 | 1 |
| P187_TOP5_I85_S5p0_Z1_R200 | P180_STRESSED_RETAIL | validation | 2197 | 0.00391353 | 54.7405 | 18.0645 | 36.676 | 0.00546199 | -45.4242 | 82.1002 | 0 | 0 | -10.5807 | 12.612 | 0.00296495 | 1 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P187_PHASE186_FAMILY_SET_CLOSED | 1 | phase186_current_family_set_closed=1 | hard |
| P187_TRAIN_ONLY_SELECTION | 1 | selected_candidate_rows=12 | hard |
| P187_VALIDATION_EVALUATED_NO_TEST | 1 | validation_rows=24; test_rows_used=0 | hard |
| P187_COST_LATENCY_BOUND | 1 | validation_summary_rows=24 | hard |
| P187_NEGATIVE_CONTROL_MARGIN_RECORDED | 1 | shuffled-time control edge column present | hard |
| P187_NO_TEST_REPLAY_OR_PROMOTION | 1 | test_rows_used=0; promotion_allowed=0 | hard |
| P187_VALIDATION_PASS_RECORDED | 1 | validation_positive_all_profiles=1 | hard |

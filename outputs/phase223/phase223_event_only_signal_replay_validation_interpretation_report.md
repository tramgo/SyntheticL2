# Phase223 Event-only Signal Replay Validation Interpretation

Generated UTC: 2026-07-29T05:16:44.904084+00:00

Phase223 interprets Phase222 aggregate train/validation signal replay outputs.
It decides whether broader replay or sealed test should remain closed; it emits no order/fill, P&L, row-level prediction, promotion, paper/live, or profitability artifact.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase223_interpretation_rows | 40 | Validation interpretation rows |
| phase223_profile_summary_rows | 2 | Cost profile summary rows |
| phase223_target_summary_rows | 5 | Target/horizon summary rows |
| phase223_validation_decision_events | 59654 | Validation decision events interpreted |
| phase223_positive_net_validation_rows | 0 | Rows with positive validation net-after-cost proxy |
| phase223_passing_interpretation_rows | 0 | Rows passing interpretation gates |
| phase223_cost_dominates_rows | 10 | Rows where cost bound dominates gross proxy edge |
| phase223_best_validation_net_after_cost_bps_proxy | -13.4207 | Best validation net-after-cost proxy |
| phase223_worst_validation_net_after_cost_bps_proxy | -18.4003 | Worst validation net-after-cost proxy |
| phase223_best_actual_vs_shuffle_net_edge_bps | 1 | Best actual-vs-shuffled net edge |
| phase223_phase224_work_order_rows | 1 | Phase224 work-order rows |
| phase223_forbidden_execution_rows | 11 | Forbidden execution rows |
| phase223_gate_rows | 7 | Gates evaluated |
| phase223_hard_gate_rows | 7 | Hard gates evaluated |
| phase223_hard_gate_pass_rows | 7 | Hard gates passed |
| phase223_event_only_signal_replay_validation_interpretation_complete | 1 | 1 means Phase223 completed |
| phase223_broader_replay_allowed_next | 0 | No broader replay opened |
| phase223_test_replay_allowed_next | 0 | No test replay opened |
| phase223_test_rows_used | 0 | No sealed test rows used |
| phase223_promotion_allowed | 0 | No promotion opened |
| phase223_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase223_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase223_forbidden_outputs | test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export;broader_replay_unlock | Outputs forbidden in this phase |
| phase223_next_best_action | run_phase224_event_only_signal_replay_closure_or_redesign_precommit_no_test | Recommended next milestone |

## Validation Interpretation

| phase221_candidate_id | phase219_model_fit_id | model_family | target_label | horizon_sec | split_role | threshold | latency_profile_id | control_name | decision_events | hit_rate | gross_label_payoff_bps_proxy_mean | cost_bound_bps_mean | net_after_cost_bps_proxy_mean | net_positive_event_fraction | test_rows_used | promotion_allowed | paper_or_live_acceptance_allowed | profitability_claim_allowed | shuffle_net_after_cost_bps_proxy_mean | shuffle_hit_rate | actual_vs_shuffle_net_edge_bps | actual_vs_shuffle_hit_rate_edge | passes_min_decision_events | passes_cost_positive | passes_actual_vs_shuffle_net | cost_dominates_gross_edge | interpretation_pass | broader_replay_allowed_next | test_replay_allowed_next | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P221_CANDIDATE_01 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | validation | 0.55 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 12 | 0.75 | 0.5 | 13.9207 | -13.4207 | 0 | 0 | 0 | 0 | 0 | -14.4207 | 0.25 | 1 | 0.5 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_02 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | validation | 0.65 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 6263 | 0.711001 | 0.633003 | 14.4247 | -13.7917 | 0 | 0 | 0 | 0 | 0 | -14.0465 | 0.626058 | 0.25483 | 0.0849433 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_02 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | validation | 0.6 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 9795 | 0.710669 | 0.632006 | 14.4307 | -13.7987 | 0 | 0 | 0 | 0 | 0 | -14.0508 | 0.626646 | 0.252067 | 0.0840225 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_02 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | validation | 0.7 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 1559 | 0.699808 | 0.599423 | 14.5936 | -13.9942 | 0 | 0 | 0 | 0 | 0 | -14.2155 | 0.626042 | 0.221296 | 0.0737652 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_02 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | validation | 0.55 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 12198 | 0.681833 | 0.545499 | 15.3233 | -14.7778 | 0 | 0 | 0 | 0 | 0 | -14.9517 | 0.623873 | 0.173881 | 0.0579603 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_01 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | validation | 0.55 | P180_STRESSED_RETAIL | actual_label_order | 12 | 0.75 | 0.5 | 16.2804 | -15.7804 | 0 | 0 | 0 | 0 | 0 | -16.7804 | 0.25 | 1 | 0.5 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_02 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | validation | 0.6 | P180_STRESSED_RETAIL | actual_label_order | 9795 | 0.710669 | 0.632006 | 17.2998 | -16.6678 | 0 | 0 | 0 | 0 | 0 | -16.9198 | 0.626646 | 0.252067 | 0.0840225 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_02 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | validation | 0.65 | P180_STRESSED_RETAIL | actual_label_order | 6263 | 0.711001 | 0.633003 | 17.3085 | -16.6754 | 0 | 0 | 0 | 0 | 0 | -16.9303 | 0.626058 | 0.25483 | 0.0849433 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_02 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | validation | 0.7 | P180_STRESSED_RETAIL | actual_label_order | 1559 | 0.699808 | 0.599423 | 17.6452 | -17.0458 | 0 | 0 | 0 | 0 | 0 | -17.2671 | 0.626042 | 0.221296 | 0.0737652 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_02 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | validation | 0.55 | P180_STRESSED_RETAIL | actual_label_order | 12198 | 0.681833 | 0.545499 | 18.9458 | -18.4003 | 0 | 0 | 0 | 0 | 0 | -18.5742 | 0.623873 | 0.173881 | 0.0579603 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_01 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | validation | 0.6 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_01 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | validation | 0.6 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_01 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | validation | 0.65 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_01 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | validation | 0.65 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_01 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | validation | 0.7 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_01 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | validation | 0.7 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_03 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 5 | validation | 0.55 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_03 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 5 | validation | 0.55 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_03 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 5 | validation | 0.6 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_03 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 5 | validation | 0.6 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_03 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 5 | validation | 0.65 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_03 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 5 | validation | 0.65 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_03 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 5 | validation | 0.7 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_03 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 5 | validation | 0.7 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_04 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 5 | validation | 0.55 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_04 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 5 | validation | 0.55 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_04 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 5 | validation | 0.6 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_04 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 5 | validation | 0.6 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_04 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 5 | validation | 0.65 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_04 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 5 | validation | 0.65 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_04 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 5 | validation | 0.7 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_04 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 5 | validation | 0.7 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_05 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 1 | validation | 0.55 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_05 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 1 | validation | 0.55 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_05 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 1 | validation | 0.6 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_05 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 1 | validation | 0.6 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_05 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 1 | validation | 0.65 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_05 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 1 | validation | 0.65 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_05 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 1 | validation | 0.7 | P180_RETAIL_MARKETABLE_DEFAULT | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |
| P221_CANDIDATE_05 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 1 | validation | 0.7 | P180_STRESSED_RETAIL | actual_label_order | 0 |  |  |  |  |  | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | insufficient_cost_positive_validation_edge |

## Cost Profile Summary

| latency_profile_id | validation_rows | decision_events | best_validation_net_after_cost_bps_proxy | worst_validation_net_after_cost_bps_proxy | positive_net_rows | actual_beats_shuffle_rows | passing_interpretation_rows | cost_dominates_rows | broader_replay_allowed_next | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P180_RETAIL_MARKETABLE_DEFAULT | 20 | 29827 | -13.4207 | -14.7778 | 0 | 5 | 0 | 5 | 0 | 0 |
| P180_STRESSED_RETAIL | 20 | 29827 | -15.7804 | -18.4003 | 0 | 5 | 0 | 5 | 0 | 0 |

## Target Horizon Summary

| target_label | horizon_sec | validation_profile_threshold_rows | decision_events | active_rows | best_validation_net_after_cost_bps_proxy | positive_net_rows | interpretation_pass_rows |
| --- | --- | --- | --- | --- | --- | --- | --- |
| event_surprise_down_conditional_label | 1 | 8 | 0 | 0 | 0 | 0 | 0 |
| event_surprise_down_conditional_label | 5 | 8 | 0 | 0 | 0 | 0 | 0 |
| event_surprise_up_conditional_label | 5 | 8 | 0 | 0 | 0 | 0 | 0 |
| event_surprise_vol_expansion_conditional_label | 1 | 8 | 24 | 2 | -13.4207 | 0 | 0 |
| event_surprise_vol_expansion_conditional_label | 5 | 8 | 59630 | 8 | -13.7917 | 0 | 0 |

## Phase224 Work Order

| phase224_work_order_id | work_order | phase223_passing_interpretation_rows | phase223_positive_net_validation_rows | recommended_decision | allowed_next_scope | broader_replay_allowed_next | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P224_EVENT_ONLY_SIGNAL_REPLAY_CLOSURE_OR_REDESIGN_PRECOMMIT | Close the current event-only signal replay branch for broader replay/test unless a material redesign is precommitted from Phase223 evidence. | 0 | 0 | close_current_signal_replay_candidate_set_and_precommit_redesign | closure_or_redesign_precommit_only_no_test_no_broader_replay | 0 | 0 | 0 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase223 | allowed_in_phase223 | rationale |
| --- | --- | --- | --- |
| test_replay_execution | 0 | 0 | Phase223 interprets aggregate Phase222 validation replay outputs only and emits no broader replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact. |
| test_result | 0 | 0 | Phase223 interprets aggregate Phase222 validation replay outputs only and emits no broader replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact. |
| promotion | 0 | 0 | Phase223 interprets aggregate Phase222 validation replay outputs only and emits no broader replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact. |
| paper_live_acceptance | 0 | 0 | Phase223 interprets aggregate Phase222 validation replay outputs only and emits no broader replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact. |
| order_arrival | 0 | 0 | Phase223 interprets aggregate Phase222 validation replay outputs only and emits no broader replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact. |
| fill_model | 0 | 0 | Phase223 interprets aggregate Phase222 validation replay outputs only and emits no broader replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact. |
| pnl_replay | 0 | 0 | Phase223 interprets aggregate Phase222 validation replay outputs only and emits no broader replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact. |
| profitability_claim | 0 | 0 | Phase223 interprets aggregate Phase222 validation replay outputs only and emits no broader replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact. |
| threshold_widening | 0 | 0 | Phase223 interprets aggregate Phase222 validation replay outputs only and emits no broader replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact. |
| row_level_prediction_export | 0 | 0 | Phase223 interprets aggregate Phase222 validation replay outputs only and emits no broader replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact. |
| broader_replay_unlock | 0 | 0 | Phase223 interprets aggregate Phase222 validation replay outputs only and emits no broader replay, test, order/fill, P&L, promotion, paper/live, row-level prediction, or profitability artifact. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P223_PHASE222_COMPLETE | True | phase222_complete=1 | hard |
| P223_VALIDATION_INTERPRETATION_RECORDED | True | validation_rows=40 | hard |
| P223_COST_PROFILE_INTERPRETATION_RECORDED | True | profile_rows=2 | hard |
| P223_NO_COST_POSITIVE_VALIDATION_PASS | True | passing_rows=0; positive_rows=0 | hard |
| P223_PHASE224_WORK_ORDER_RECORDED | True | work_order_rows=1 | hard |
| P223_TEST_ROWS_UNTOUCHED | True | test_rows_used=0 | hard |
| P223_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; forbidden_flags=0 | hard |

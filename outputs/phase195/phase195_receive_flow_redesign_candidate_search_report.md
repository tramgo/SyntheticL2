# Phase195 Receive-flow Redesign Candidate Search

Generated UTC: 2026-07-28T19:00:23.551356+00:00

Phase195 searches redesigned receive-flow candidates after Phase194 closed the prior sparse candidate.
Selection is train-only. Validation and unassigned extension dates are evaluation-only. The untouched test split remains excluded.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase195_candidate_grid_rows | 576 | Redesigned candidate grid rows |
| phase195_train_selected_candidate_rows | 22 | Train-selected candidate rows |
| phase195_candidate_decision_rows | 22 | Candidate decision rows |
| phase195_passing_extension_gate_candidates | 0 | Candidates passing date and symbol breadth extension gates |
| phase195_best_candidate_id | P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R50 | Top redesign candidate by extension screen |
| phase195_best_min_extension_net_bps | -12.411 | Best candidate minimum extension net bps |
| phase195_best_date_positive_fraction | 0 | Best candidate date-positive fraction |
| phase195_best_symbol_positive_fraction | 0 | Best candidate symbol-positive fraction |
| phase195_gate_rows | 6 | Gates evaluated |
| phase195_hard_gate_rows | 6 | Hard gates evaluated |
| phase195_hard_gate_pass_rows | 6 | Hard gates passed |
| phase195_redesign_search_complete | 1 | 1 means Phase195 completed |
| phase195_test_replay_allowed_next | 0 | No test replay opened |
| phase195_promotion_allowed | 0 | No promotion opened |
| phase195_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase195_forbidden_outputs | test_result;test_replay_execution;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim | Outputs forbidden in this phase |
| phase195_next_best_action | redesign_or_expand_feature_family_no_test | Recommended next milestone |

## Top Candidate Decisions

| candidate_id | min_train_net_bps | min_validation_net_bps | min_extension_net_bps | date_positive_fraction | date_control_positive_fraction | symbol_positive_fraction | validation_extension_gate_pass | test_replay_allowed_next | promotion_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R50 | 6.22577 | -13.017 | -12.411 | 0 | 1 | 0 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R100 | 6.22577 | -13.017 | -12.411 | 0 | 1 | 0 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q0_R50 | 5.96528 | -13.0113 | -12.4198 | 0 | 1 | 0 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q0_R100 | 5.96528 | -13.0113 | -12.4198 | 0 | 1 | 0 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q1_R100 | 56.6003 | -13.2485 | -12.9195 | 0 | 1 | 0 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q1_R50 | 56.6003 | -13.2485 | -12.9195 | 0 | 1 | 0 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q0_R100 | 55.2809 | -13.2308 | -12.9445 | 0 | 1 | 0 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q0_R50 | 55.2809 | -13.2308 | -12.9445 | 0 | 1 | 0 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S1p5_Z0_Q1_R100 | 7.20106 | -13.3173 | -13.0542 | 0 | 1 | 0 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S1p5_Z0_Q0_R100 | 4.23414 | -13.3887 | -13.2145 | 0 | 1 | 0 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q1_R50 | 1.30302 | 45.27 | -13.3426 | 0.333333 | 0.5 | 0.0967742 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q1_R100 | 1.30302 | 45.27 | -13.3426 | 0.333333 | 0.5 | 0.0967742 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q0_R50 | 1.04804 | 43.6433 | -13.3544 | 0.333333 | 0.666667 | 0.0967742 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q0_R100 | 1.04804 | 43.6433 | -13.3544 | 0.333333 | 0.833333 | 0.0967742 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q1_R100 | 31.7515 | 112.045 | -13.8538 | 0.333333 | 0.5 | 0.0666667 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q1_R50 | 31.7515 | 112.045 | -13.8538 | 0.333333 | 0.666667 | 0.0666667 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q0_R50 | 30.6441 | 105.795 | -13.8866 | 0.333333 | 1 | 0.0666667 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q0_R100 | 30.6441 | 105.795 | -13.8866 | 0.333333 | 1 | 0.0666667 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q1_R100 | 6.54183 | 90.106 | -20.4577 | 0.333333 | 0.666667 | 0.0967742 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q1_R50 | 6.54183 | 90.106 | -20.4577 | 0.333333 | 0.5 | 0.0967742 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q0_R100 | 5.7324 | 83.8255 | -20.5164 | 0.333333 | 0.666667 | 0.0967742 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q0_R50 | 5.7324 | 83.8255 | -20.5164 | 0.333333 | 0.5 | 0.0967742 | 0 | 0 | 0 |

## Train-selected Candidates

| candidate_id | min_train_net_bps | min_train_edge_bps | max_train_decision_rate | min_train_events | imbalance_source | side_mode | min_abs_imbalance | max_spread_bps | min_abs_event_zscore | min_quote_churn_count | max_decision_rate | test_replay_allowed_in_phase195 | selected_by_phase195_train_only | validation_used_for_selection | extension_used_for_selection | test_used_for_selection |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q1_R100 | 56.6003 | 70.3446 | 0.000527966 | 570 | top5 | follow_imbalance | 0.9 | 1.5 | 1 | 1 | 0.01 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q1_R50 | 56.6003 | 70.2997 | 0.000527966 | 570 | top5 | follow_imbalance | 0.9 | 1.5 | 1 | 1 | 0.005 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q0_R100 | 55.2809 | 68.9715 | 0.000538155 | 581 | top5 | follow_imbalance | 0.9 | 1.5 | 1 | 0 | 0.01 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q0_R50 | 55.2809 | 34.5573 | 0.000538155 | 581 | top5 | follow_imbalance | 0.9 | 1.5 | 1 | 0 | 0.005 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q1_R100 | 31.7515 | 46.3481 | 0.000802138 | 866 | top5 | follow_imbalance | 0.9 | 2.5 | 1 | 1 | 0.01 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q1_R50 | 31.7515 | 46.3236 | 0.000802138 | 866 | top5 | follow_imbalance | 0.9 | 2.5 | 1 | 1 | 0.005 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q0_R50 | 30.6441 | 45.2501 | 0.000821589 | 887 | top5 | follow_imbalance | 0.9 | 2.5 | 1 | 0 | 0.005 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q0_R100 | 30.6441 | 22.7034 | 0.000821589 | 887 | top5 | follow_imbalance | 0.9 | 2.5 | 1 | 0 | 0.01 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S1p5_Z0_Q1_R100 | 7.20106 | 11.1461 | 0.00682466 | 7368 | top5 | follow_imbalance | 0.9 | 1.5 | 0 | 1 | 0.01 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q1_R100 | 6.54183 | 25.6482 | 0.00144959 | 1565 | top5 | follow_imbalance | 0.9 | 5 | 1 | 1 | 0.01 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q1_R50 | 6.54183 | 0.0176719 | 0.00144959 | 1565 | top5 | follow_imbalance | 0.9 | 5 | 1 | 1 | 0.005 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R50 | 6.22577 | 9.94306 | 0.0018979 | 2049 | top5 | follow_imbalance | 0.8 | 1.5 | 1 | 1 | 0.005 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R100 | 6.22577 | 0.140651 | 0.0018979 | 2049 | top5 | follow_imbalance | 0.8 | 1.5 | 1 | 1 | 0.01 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q0_R50 | 5.96528 | 9.82286 | 0.00192383 | 2077 | top5 | follow_imbalance | 0.8 | 1.5 | 1 | 0 | 0.005 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q0_R100 | 5.96528 | 9.76989 | 0.00192383 | 2077 | top5 | follow_imbalance | 0.8 | 1.5 | 1 | 0 | 0.01 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q0_R100 | 5.7324 | 24.9087 | 0.0014922 | 1611 | top5 | follow_imbalance | 0.9 | 5 | 1 | 0 | 0.01 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q0_R50 | 5.7324 | 0.0617226 | 0.0014922 | 1611 | top5 | follow_imbalance | 0.9 | 5 | 1 | 0 | 0.005 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I90_S1p5_Z0_Q0_R100 | 4.23414 | 11.1895 | 0.00848173 | 9157 | top5 | follow_imbalance | 0.9 | 1.5 | 0 | 0 | 0.01 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q1_R50 | 1.30302 | 6.82857 | 0.00278155 | 3003 | top5 | follow_imbalance | 0.8 | 2.5 | 1 | 1 | 0.005 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q1_R100 | 1.30302 | 6.82489 | 0.00278155 | 3003 | top5 | follow_imbalance | 0.8 | 2.5 | 1 | 1 | 0.01 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q0_R50 | 1.04804 | 6.66158 | 0.00283342 | 3059 | top5 | follow_imbalance | 0.8 | 2.5 | 1 | 0 | 0.005 | 0 | 1 | 0 | 0 | 0 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q0_R100 | 1.04804 | 0.148616 | 0.00283342 | 3059 | top5 | follow_imbalance | 0.8 | 2.5 | 1 | 0 | 0.01 | 0 | 1 | 0 | 0 | 0 |

## Validation Extension Summary

| candidate_id | latency_profile_id | split_bucket | decision_events | decision_rate | max_decision_rate | decision_rate_pass | dates_with_events | symbols_with_events | net_return_bps_after_cost_proxy_mean | gross_return_bps_proxy_mean | cost_bound_bps_mean | net_edge_over_shuffled_time_bps_mean | net_positive_event_fraction | test_rows_used | promotion_allowed | min_train_net_bps | min_train_edge_bps | max_train_decision_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 432 | 0.000769524 | 0.01 | 1 | 1 | 26 | -11.3208 | 0.165605 | 11.4864 | 0.193113 | 0 | 0 | 0 | 56.6003 | 70.3446 | 0.000527966 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 695 | 0.000612996 | 0.01 | 1 | 2 | 27 | -11.1032 | 0.161685 | 11.2649 | 0.130992 | 0 | 0 | 0 | 56.6003 | 70.3446 | 0.000527966 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q1_R100 | P180_STRESSED_RETAIL | validation | 432 | 0.000769524 | 0.01 | 1 | 1 | 26 | -13.2485 | 0.165605 | 13.4141 | 0.167165 | 0 | 0 | 0 | 56.6003 | 70.3446 | 0.000527966 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q1_R100 | P180_STRESSED_RETAIL | validation_extension | 695 | 0.000612996 | 0.01 | 1 | 2 | 27 | -12.9195 | 0.161685 | 13.0811 | 0.168363 | 0 | 0 | 0 | 56.6003 | 70.3446 | 0.000527966 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 432 | 0.000769524 | 0.005 | 1 | 1 | 26 | -11.3208 | 0.165605 | 11.4864 | 0.18353 | 0 | 0 | 0 | 56.6003 | 70.2997 | 0.000527966 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 695 | 0.000612996 | 0.005 | 1 | 2 | 27 | -11.1032 | 0.161685 | 11.2649 | 0.200034 | 0 | 0 | 0 | 56.6003 | 70.2997 | 0.000527966 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q1_R50 | P180_STRESSED_RETAIL | validation | 432 | 0.000769524 | 0.005 | 1 | 1 | 26 | -13.2485 | 0.165605 | 13.4141 | 0.196782 | 0 | 0 | 0 | 56.6003 | 70.2997 | 0.000527966 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q1_R50 | P180_STRESSED_RETAIL | validation_extension | 695 | 0.000612996 | 0.005 | 1 | 2 | 27 | -12.9195 | 0.161685 | 13.0811 | 0.135264 | 0 | 0 | 0 | 56.6003 | 70.2997 | 0.000527966 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q0_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 444 | 0.0007909 | 0.01 | 1 | 1 | 26 | -11.3127 | 0.159043 | 11.4717 | 0.0938184 | 0 | 0 | 0 | 55.2809 | 68.9715 | 0.000538155 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q0_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 710 | 0.000626226 | 0.01 | 1 | 2 | 27 | -11.117 | 0.158624 | 11.2756 | 0.188453 | 0 | 0 | 0 | 55.2809 | 68.9715 | 0.000538155 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q0_R100 | P180_STRESSED_RETAIL | validation | 444 | 0.0007909 | 0.01 | 1 | 1 | 26 | -13.2308 | 0.159043 | 13.3898 | 0.0810387 | 0 | 0 | 0 | 55.2809 | 68.9715 | 0.000538155 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q0_R100 | P180_STRESSED_RETAIL | validation_extension | 710 | 0.000626226 | 0.01 | 1 | 2 | 27 | -12.9445 | 0.158624 | 13.1032 | 0.150264 | 0 | 0 | 0 | 55.2809 | 68.9715 | 0.000538155 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q0_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 444 | 0.0007909 | 0.005 | 1 | 1 | 26 | -11.3127 | 0.159043 | 11.4717 | 0.0991728 | 0 | 0 | 0 | 55.2809 | 34.5573 | 0.000538155 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q0_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 710 | 0.000626226 | 0.005 | 1 | 2 | 27 | -11.117 | 0.158624 | 11.2756 | 0.166707 | 0 | 0 | 0 | 55.2809 | 34.5573 | 0.000538155 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q0_R50 | P180_STRESSED_RETAIL | validation | 444 | 0.0007909 | 0.005 | 1 | 1 | 26 | -13.2308 | 0.159043 | 13.3898 | 0.117554 | 0 | 0 | 0 | 55.2809 | 34.5573 | 0.000538155 |
| P195_TOP5_FOLLOW_I90_S1p5_Z1_Q0_R50 | P180_STRESSED_RETAIL | validation_extension | 710 | 0.000626226 | 0.005 | 1 | 2 | 27 | -12.9445 | 0.158624 | 13.1032 | 0.102299 | 0 | 0 | 0 | 55.2809 | 34.5573 | 0.000538155 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 634 | 0.00112935 | 0.01 | 1 | 1 | 30 | 114.146 | 126.321 | 12.1749 | 63.2394 | 0.0126183 | 0 | 0 | 31.7515 | 46.3481 | 0.000802138 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 1017 | 0.000897003 | 0.01 | 1 | 2 | 27 | -11.8428 | 0.159696 | 12.0025 | 0.156561 | 0 | 0 | 0 | 31.7515 | 46.3481 | 0.000802138 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q1_R100 | P180_STRESSED_RETAIL | validation | 634 | 0.00112935 | 0.01 | 1 | 1 | 30 | 112.045 | 126.321 | 14.2751 | 94.7617 | 0.0126183 | 0 | 0 | 31.7515 | 46.3481 | 0.000802138 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q1_R100 | P180_STRESSED_RETAIL | validation_extension | 1017 | 0.000897003 | 0.01 | 1 | 2 | 27 | -13.8538 | 0.159696 | 14.0135 | 0.189796 | 0 | 0 | 0 | 31.7515 | 46.3481 | 0.000802138 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 634 | 0.00112935 | 0.005 | 1 | 1 | 30 | 114.146 | 126.321 | 12.1749 | 94.7336 | 0.0126183 | 0 | 0 | 31.7515 | 46.3236 | 0.000802138 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 1017 | 0.000897003 | 0.005 | 1 | 2 | 27 | -11.8428 | 0.159696 | 12.0025 | 0.175258 | 0 | 0 | 0 | 31.7515 | 46.3236 | 0.000802138 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q1_R50 | P180_STRESSED_RETAIL | validation | 634 | 0.00112935 | 0.005 | 1 | 1 | 30 | 112.045 | 126.321 | 14.2751 | 157.837 | 0.0126183 | 0 | 0 | 31.7515 | 46.3236 | 0.000802138 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q1_R50 | P180_STRESSED_RETAIL | validation_extension | 1017 | 0.000897003 | 0.005 | 1 | 2 | 27 | -13.8538 | 0.159696 | 14.0135 | 0.183919 | 0 | 0 | 0 | 31.7515 | 46.3236 | 0.000802138 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q0_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 667 | 0.00118813 | 0.005 | 1 | 1 | 30 | 107.888 | 120.07 | 12.1825 | 150.04 | 0.011994 | 0 | 0 | 30.6441 | 45.2501 | 0.000821589 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q0_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 1046 | 0.000922581 | 0.005 | 1 | 2 | 27 | -11.8684 | 0.149788 | 12.0182 | 0.186997 | 0 | 0 | 0 | 30.6441 | 45.2501 | 0.000821589 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q0_R50 | P180_STRESSED_RETAIL | validation | 667 | 0.00118813 | 0.005 | 1 | 1 | 30 | 105.795 | 120.07 | 14.275 | 60.1101 | 0.011994 | 0 | 0 | 30.6441 | 45.2501 | 0.000821589 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q0_R50 | P180_STRESSED_RETAIL | validation_extension | 1046 | 0.000922581 | 0.005 | 1 | 2 | 27 | -13.8866 | 0.149788 | 14.0363 | 0.0739872 | 0 | 0 | 0 | 30.6441 | 45.2501 | 0.000821589 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q0_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 667 | 0.00118813 | 0.01 | 1 | 1 | 30 | 107.888 | 120.07 | 12.1825 | 60.1294 | 0.011994 | 0 | 0 | 30.6441 | 22.7034 | 0.000821589 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q0_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 1046 | 0.000922581 | 0.01 | 1 | 2 | 27 | -11.8684 | 0.149788 | 12.0182 | 0.102103 | 0 | 0 | 0 | 30.6441 | 22.7034 | 0.000821589 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q0_R100 | P180_STRESSED_RETAIL | validation | 667 | 0.00118813 | 0.01 | 1 | 1 | 30 | 105.795 | 120.07 | 14.275 | 90.08 | 0.011994 | 0 | 0 | 30.6441 | 22.7034 | 0.000821589 |
| P195_TOP5_FOLLOW_I90_S2p5_Z1_Q0_R100 | P180_STRESSED_RETAIL | validation_extension | 1046 | 0.000922581 | 0.01 | 1 | 2 | 27 | -13.8866 | 0.149788 | 14.0363 | 0.174093 | 0 | 0 | 0 | 30.6441 | 22.7034 | 0.000821589 |
| P195_TOP5_FOLLOW_I90_S1p5_Z0_Q1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 4463 | 0.00794997 | 0.01 | 1 | 1 | 29 | -11.3132 | 0.231398 | 11.5446 | 0.236126 | 0.00156845 | 0 | 0 | 7.20106 | 11.1461 | 0.00682466 |
| P195_TOP5_FOLLOW_I90_S1p5_Z0_Q1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 7285 | 0.00642543 | 0.01 | 1 | 2 | 29 | -11.1346 | 0.240396 | 11.375 | 0.222168 | 0.00178449 | 0 | 0 | 7.20106 | 11.1461 | 0.00682466 |
| P195_TOP5_FOLLOW_I90_S1p5_Z0_Q1_R100 | P180_STRESSED_RETAIL | validation | 4463 | 0.00794997 | 0.01 | 1 | 1 | 29 | -13.3173 | 0.231398 | 13.5487 | 0.264702 | 0.00112032 | 0 | 0 | 7.20106 | 11.1461 | 0.00682466 |
| P195_TOP5_FOLLOW_I90_S1p5_Z0_Q1_R100 | P180_STRESSED_RETAIL | validation_extension | 7285 | 0.00642543 | 0.01 | 1 | 2 | 29 | -13.0542 | 0.240396 | 13.2946 | 0.236649 | 0.00137268 | 0 | 0 | 7.20106 | 11.1461 | 0.00682466 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 1114 | 0.00198437 | 0.01 | 1 | 1 | 31 | 93.1435 | 107.849 | 14.7058 | 89.9591 | 0.010772 | 0 | 0 | 6.54183 | 25.6482 | 0.00144959 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 1935 | 0.00170669 | 0.01 | 1 | 2 | 29 | -16.0521 | 0.121737 | 16.1739 | 0.14281 | 0 | 0 | 0 | 6.54183 | 25.6482 | 0.00144959 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q1_R100 | P180_STRESSED_RETAIL | validation | 1114 | 0.00198437 | 0.01 | 1 | 1 | 31 | 90.106 | 107.849 | 17.7432 | 53.9592 | 0.010772 | 0 | 0 | 6.54183 | 25.6482 | 0.00144959 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q1_R100 | P180_STRESSED_RETAIL | validation_extension | 1935 | 0.00170669 | 0.01 | 1 | 2 | 29 | -20.4577 | 0.121737 | 20.5795 | 0.138034 | 0 | 0 | 0 | 6.54183 | 25.6482 | 0.00144959 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 1114 | 0.00198437 | 0.005 | 1 | 1 | 31 | 93.1435 | 107.849 | 14.7058 | 107.874 | 0.010772 | 0 | 0 | 6.54183 | 0.0176719 | 0.00144959 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 1935 | 0.00170669 | 0.005 | 1 | 2 | 29 | -16.0521 | 0.121737 | 16.1739 | 0.1325 | 0 | 0 | 0 | 6.54183 | 0.0176719 | 0.00144959 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q1_R50 | P180_STRESSED_RETAIL | validation | 1114 | 0.00198437 | 0.005 | 1 | 1 | 31 | 90.106 | 107.849 | 17.7432 | 53.9803 | 0.010772 | 0 | 0 | 6.54183 | 0.0176719 | 0.00144959 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q1_R50 | P180_STRESSED_RETAIL | validation_extension | 1935 | 0.00170669 | 0.005 | 1 | 2 | 29 | -20.4577 | 0.121737 | 20.5795 | 0.108402 | 0 | 0 | 0 | 6.54183 | 0.0176719 | 0.00144959 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 1334 | 0.00237626 | 0.005 | 1 | 1 | 29 | -11.2088 | 0.150138 | 11.359 | 0.16032 | 0.000749625 | 0 | 0 | 6.22577 | 9.94306 | 0.0018979 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 2484 | 0.00219091 | 0.005 | 1 | 2 | 29 | -10.8443 | 0.148957 | 10.9932 | 0.172274 | 0.000402576 | 0 | 0 | 6.22577 | 9.94306 | 0.0018979 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R50 | P180_STRESSED_RETAIL | validation | 1334 | 0.00237626 | 0.005 | 1 | 1 | 29 | -13.017 | 0.150138 | 13.1671 | 0.184701 | 0.000749625 | 0 | 0 | 6.22577 | 9.94306 | 0.0018979 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R50 | P180_STRESSED_RETAIL | validation_extension | 2484 | 0.00219091 | 0.005 | 1 | 2 | 29 | -12.411 | 0.148957 | 12.5599 | 0.148141 | 0 | 0 | 0 | 6.22577 | 9.94306 | 0.0018979 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 1334 | 0.00237626 | 0.01 | 1 | 1 | 29 | -11.2088 | 0.150138 | 11.359 | 0.168403 | 0.000749625 | 0 | 0 | 6.22577 | 0.140651 | 0.0018979 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 2484 | 0.00219091 | 0.01 | 1 | 2 | 29 | -10.8443 | 0.148957 | 10.9932 | 0.145871 | 0.000402576 | 0 | 0 | 6.22577 | 0.140651 | 0.0018979 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R100 | P180_STRESSED_RETAIL | validation | 1334 | 0.00237626 | 0.01 | 1 | 1 | 29 | -13.017 | 0.150138 | 13.1671 | 0.167572 | 0.000749625 | 0 | 0 | 6.22577 | 0.140651 | 0.0018979 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q1_R100 | P180_STRESSED_RETAIL | validation_extension | 2484 | 0.00219091 | 0.01 | 1 | 2 | 29 | -12.411 | 0.148957 | 12.5599 | 0.120212 | 0 | 0 | 0 | 6.22577 | 0.140651 | 0.0018979 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q0_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 1355 | 0.00241367 | 0.005 | 1 | 1 | 29 | -11.2068 | 0.14708 | 11.3538 | 0.148114 | 0.000738007 | 0 | 0 | 5.96528 | 9.82286 | 0.00192383 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q0_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 2528 | 0.00222972 | 0.005 | 1 | 2 | 29 | -10.8501 | 0.14823 | 10.9984 | 0.175492 | 0.00039557 | 0 | 0 | 5.96528 | 9.82286 | 0.00192383 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q0_R50 | P180_STRESSED_RETAIL | validation | 1355 | 0.00241367 | 0.005 | 1 | 1 | 29 | -13.0113 | 0.14708 | 13.1584 | 0.183048 | 0.000738007 | 0 | 0 | 5.96528 | 9.82286 | 0.00192383 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q0_R50 | P180_STRESSED_RETAIL | validation_extension | 2528 | 0.00222972 | 0.005 | 1 | 2 | 29 | -12.4198 | 0.14823 | 12.568 | 0.132357 | 0 | 0 | 0 | 5.96528 | 9.82286 | 0.00192383 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q0_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 1355 | 0.00241367 | 0.01 | 1 | 1 | 29 | -11.2068 | 0.14708 | 11.3538 | 0.149291 | 0.000738007 | 0 | 0 | 5.96528 | 9.76989 | 0.00192383 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q0_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 2528 | 0.00222972 | 0.01 | 1 | 2 | 29 | -10.8501 | 0.14823 | 10.9984 | 0.182351 | 0.00039557 | 0 | 0 | 5.96528 | 9.76989 | 0.00192383 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q0_R100 | P180_STRESSED_RETAIL | validation | 1355 | 0.00241367 | 0.01 | 1 | 1 | 29 | -13.0113 | 0.14708 | 13.1584 | 0.0672543 | 0.000738007 | 0 | 0 | 5.96528 | 9.76989 | 0.00192383 |
| P195_TOP5_FOLLOW_I80_S1p5_Z1_Q0_R100 | P180_STRESSED_RETAIL | validation_extension | 2528 | 0.00222972 | 0.01 | 1 | 2 | 29 | -12.4198 | 0.14823 | 12.568 | 0.124029 | 0 | 0 | 0 | 5.96528 | 9.76989 | 0.00192383 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q0_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 1183 | 0.00210728 | 0.01 | 1 | 1 | 31 | 86.8442 | 101.559 | 14.7147 | 50.8105 | 0.0101437 | 0 | 0 | 5.7324 | 24.9087 | 0.0014922 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q0_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 2018 | 0.00177989 | 0.01 | 1 | 2 | 29 | -16.0982 | 0.114674 | 16.2128 | 0.121486 | 0 | 0 | 0 | 5.7324 | 24.9087 | 0.0014922 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q0_R100 | P180_STRESSED_RETAIL | validation | 1183 | 0.00210728 | 0.01 | 1 | 1 | 31 | 83.8255 | 101.559 | 17.7334 | 67.7678 | 0.0101437 | 0 | 0 | 5.7324 | 24.9087 | 0.0014922 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q0_R100 | P180_STRESSED_RETAIL | validation_extension | 2018 | 0.00177989 | 0.01 | 1 | 2 | 29 | -20.5164 | 0.114674 | 20.631 | 0.105836 | 0 | 0 | 0 | 5.7324 | 24.9087 | 0.0014922 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q0_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 1183 | 0.00210728 | 0.005 | 1 | 1 | 31 | 86.8442 | 101.559 | 14.7147 | 101.583 | 0.0101437 | 0 | 0 | 5.7324 | 0.0617226 | 0.0014922 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q0_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 2018 | 0.00177989 | 0.005 | 1 | 2 | 29 | -16.0982 | 0.114674 | 16.2128 | 0.114948 | 0 | 0 | 0 | 5.7324 | 0.0617226 | 0.0014922 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q0_R50 | P180_STRESSED_RETAIL | validation | 1183 | 0.00210728 | 0.005 | 1 | 1 | 31 | 83.8255 | 101.559 | 17.7334 | 101.547 | 0.0101437 | 0 | 0 | 5.7324 | 0.0617226 | 0.0014922 |
| P195_TOP5_FOLLOW_I90_S5p0_Z1_Q0_R50 | P180_STRESSED_RETAIL | validation_extension | 2018 | 0.00177989 | 0.005 | 1 | 2 | 29 | -20.5164 | 0.114674 | 20.631 | 0.121646 | 0 | 0 | 0 | 5.7324 | 0.0617226 | 0.0014922 |
| P195_TOP5_FOLLOW_I90_S1p5_Z0_Q0_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 5580 | 0.00993968 | 0.01 | 1 | 1 | 29 | -11.3629 | 0.210605 | 11.5735 | 0.204264 | 0.0016129 | 0 | 0 | 4.23414 | 11.1895 | 0.00848173 |
| P195_TOP5_FOLLOW_I90_S1p5_Z0_Q0_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 9349 | 0.0082459 | 0.01 | 1 | 2 | 29 | -11.229 | 0.214591 | 11.4436 | 0.215536 | 0.00139052 | 0 | 0 | 4.23414 | 11.1895 | 0.00848173 |
| P195_TOP5_FOLLOW_I90_S1p5_Z0_Q0_R100 | P180_STRESSED_RETAIL | validation | 5580 | 0.00993968 | 0.01 | 1 | 1 | 29 | -13.3887 | 0.210605 | 13.5993 | 0.183674 | 0.00125448 | 0 | 0 | 4.23414 | 11.1895 | 0.00848173 |
| P195_TOP5_FOLLOW_I90_S1p5_Z0_Q0_R100 | P180_STRESSED_RETAIL | validation_extension | 9349 | 0.0082459 | 0.01 | 1 | 2 | 29 | -13.2145 | 0.214591 | 13.4291 | 0.24395 | 0.00106963 | 0 | 0 | 4.23414 | 11.1895 | 0.00848173 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 2025 | 0.00360714 | 0.005 | 1 | 1 | 31 | 47.285 | 59.4057 | 12.1207 | 39.6793 | 0.00641975 | 0 | 0 | 1.30302 | 6.82857 | 0.00278155 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q1_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 3549 | 0.00313025 | 0.005 | 1 | 2 | 31 | -11.5651 | 0.154541 | 11.7197 | 0.189885 | 0.00028177 | 0 | 0 | 1.30302 | 6.82857 | 0.00278155 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q1_R50 | P180_STRESSED_RETAIL | validation | 2025 | 0.00360714 | 0.005 | 1 | 1 | 31 | 45.27 | 59.4057 | 14.1357 | 29.7771 | 0.00641975 | 0 | 0 | 1.30302 | 6.82857 | 0.00278155 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q1_R50 | P180_STRESSED_RETAIL | validation_extension | 3549 | 0.00313025 | 0.005 | 1 | 2 | 31 | -13.3426 | 0.154541 | 13.4971 | 0.13414 | 0 | 0 | 0 | 1.30302 | 6.82857 | 0.00278155 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 2025 | 0.00360714 | 0.01 | 1 | 1 | 31 | 47.285 | 59.4057 | 12.1207 | 49.5356 | 0.00641975 | 0 | 0 | 1.30302 | 6.82489 | 0.00278155 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 3549 | 0.00313025 | 0.01 | 1 | 2 | 31 | -11.5651 | 0.154541 | 11.7197 | 0.142093 | 0.00028177 | 0 | 0 | 1.30302 | 6.82489 | 0.00278155 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q1_R100 | P180_STRESSED_RETAIL | validation | 2025 | 0.00360714 | 0.01 | 1 | 1 | 31 | 45.27 | 59.4057 | 14.1357 | 29.7532 | 0.00641975 | 0 | 0 | 1.30302 | 6.82489 | 0.00278155 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q1_R100 | P180_STRESSED_RETAIL | validation_extension | 3549 | 0.00313025 | 0.01 | 1 | 2 | 31 | -13.3426 | 0.154541 | 13.4971 | 0.149739 | 0 | 0 | 0 | 1.30302 | 6.82489 | 0.00278155 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q0_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 2082 | 0.00370868 | 0.005 | 1 | 1 | 31 | 45.6545 | 57.779 | 12.1246 | 19.4055 | 0.006244 | 0 | 0 | 1.04804 | 6.66158 | 0.00283342 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q0_R50 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 3621 | 0.00319375 | 0.005 | 1 | 2 | 31 | -11.575 | 0.1516 | 11.7266 | 0.111626 | 0.000276167 | 0 | 0 | 1.04804 | 6.66158 | 0.00283342 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q0_R50 | P180_STRESSED_RETAIL | validation | 2082 | 0.00370868 | 0.005 | 1 | 1 | 31 | 43.6433 | 57.779 | 14.1358 | 28.9576 | 0.006244 | 0 | 0 | 1.04804 | 6.66158 | 0.00283342 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q0_R50 | P180_STRESSED_RETAIL | validation_extension | 3621 | 0.00319375 | 0.005 | 1 | 2 | 31 | -13.3544 | 0.1516 | 13.506 | 0.163159 | 0 | 0 | 0 | 1.04804 | 6.66158 | 0.00283342 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q0_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 2082 | 0.00370868 | 0.01 | 1 | 1 | 31 | 45.6545 | 57.779 | 12.1246 | 67.4015 | 0.006244 | 0 | 0 | 1.04804 | 0.148616 | 0.00283342 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q0_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation_extension | 3621 | 0.00319375 | 0.01 | 1 | 2 | 31 | -11.575 | 0.1516 | 11.7266 | 0.16022 | 0.000276167 | 0 | 0 | 1.04804 | 0.148616 | 0.00283342 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q0_R100 | P180_STRESSED_RETAIL | validation | 2082 | 0.00370868 | 0.01 | 1 | 1 | 31 | 43.6433 | 57.779 | 14.1358 | 57.8107 | 0.006244 | 0 | 0 | 1.04804 | 0.148616 | 0.00283342 |
| P195_TOP5_FOLLOW_I80_S2p5_Z1_Q0_R100 | P180_STRESSED_RETAIL | validation_extension | 3621 | 0.00319375 | 0.01 | 1 | 2 | 31 | -13.3544 | 0.1516 | 13.506 | 0.160846 | 0 | 0 | 0 | 1.04804 | 0.148616 | 0.00283342 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P195_PHASE194_CLOSURE_COMPLETE | 1 | phase194_fragility_decision_complete=1 | hard |
| P195_TRAIN_ONLY_SELECTION | 1 | selected_candidate_rows=22 | hard |
| P195_VALIDATION_EXTENSION_EVALUATED_NO_TEST | 1 | test_rows_used=0; decision_rows=22 | hard |
| P195_DATE_AND_SYMBOL_BREADTH_GATES_APPLIED | 1 | date_positive_fraction;symbol_positive_fraction;validation_extension_gate_pass | hard |
| P195_PASSING_CANDIDATE_RECORDED | 1 | passing_candidates=0 | hard |
| P195_NO_TEST_REPLAY_OR_PROMOTION | 1 | test_replay_allowed_next=0; promotion_allowed=0 | hard |

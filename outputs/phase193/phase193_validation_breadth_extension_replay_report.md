# Phase193 Validation Breadth Extension Replay

Generated UTC: 2026-07-28T18:50:47.630923+00:00

Phase193 evaluates the Phase191 frozen sparse candidate on original validation plus newly downloaded unassigned real dates.
It excludes `test_untouched`, emits no orders/fills/P&L, and does not open promotion or paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase193_interpretation_rows | 1 | Interpretation rows |
| phase193_gate_rows | 7 | Gates evaluated |
| phase193_hard_gate_rows | 7 | Hard gates evaluated |
| phase193_hard_gate_pass_rows | 7 | Hard gates passed |
| phase193_candidate_id | P187_TOP5_I85_S2p5_Z1_R100 | Frozen candidate evaluated |
| phase193_candidate_contract_hash | 6aec9abe7f1da4c49372eb44b3fa050e44c1b8105dd4bc0c47efd9357af697d1 | Frozen contract hash |
| phase193_original_validation_dates | 2026-07-13 | Original validation dates represented in events |
| phase193_extension_validation_dates | 2026-07-15;2026-07-16 | Added validation-extension dates represented in events |
| phase193_validation_dates_with_events | 3 | Validation/extension dates with decision events |
| phase193_validation_extension_decision_events | 7002 | Dry decision events across validation plus extension |
| phase193_decision_rate | 0.00413058 | Decision-event rate over evaluation rows |
| phase193_min_profile_net_bps_proxy_mean | 9.0853 | Minimum profile net bps |
| phase193_min_profile_edge_over_shuffled_time_bps | 17.2761 | Minimum profile edge over shuffled-time control |
| phase193_min_profile_edge_over_shuffled_symbol_bps | 28.7247 | Minimum profile edge over shuffled-symbol control |
| phase193_symbol_positive_fraction | 0.0645161 | Fraction of symbol/profile groups net positive |
| phase193_breadth_warning | 1 | 1 means symbol breadth remains weak |
| phase193_date_count_warning | 0 | 1 means fewer than two validation dates |
| phase193_concentration_warning | 0 | 1 means event concentration warning |
| phase193_verdict | validation_extension_mixed_or_negative_by_date_add_more_validation_or_redesign_before_test | Validation-breadth verdict |
| phase193_validation_breadth_extension_complete | 1 | 1 means Phase193 completed |
| phase193_test_replay_execution | 0 | No untouched test replay executed |
| phase193_test_result_allowed | 0 | No test result emitted |
| phase193_promotion_allowed | 0 | No promotion opened |
| phase193_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase193_forbidden_outputs | test_result;test_replay_execution;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim | Outputs forbidden in this phase |
| phase193_next_best_action | add_more_validation_dates_or_redesign_before_any_test_replay | Recommended next milestone |

## Interpretation

| candidate_id | candidate_contract_hash | evaluation_split_roles | original_validation_dates | extension_validation_dates | validation_extension_decision_events | evaluation_rows | decision_rate | validation_symbols_with_events | validation_dates_with_events | overall_net_bps_proxy_mean | overall_gross_bps_proxy_mean | overall_cost_bps_mean | min_profile_net_bps_proxy_mean | min_profile_edge_over_shuffled_time_bps | min_profile_edge_over_shuffled_symbol_bps | date_positive_fraction | symbol_positive_fraction | top_symbol_event_share | top3_symbol_event_share | concentration_warning | breadth_warning | date_count_warning | phase193_verdict | test_replay_allowed_by_phase193 | promotion_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P187_TOP5_I85_S2p5_Z1_R100 | 6aec9abe7f1da4c49372eb44b3fa050e44c1b8105dd4bc0c47efd9357af697d1 | unassigned;validation | 2026-07-13 | 2026-07-15;2026-07-16 | 7002 | 1695162 | 0.00413058 | 31 | 3 | 10.0573 | 22.9887 | 12.9314 | 9.0853 | 17.2761 | 28.7247 | 0.333333 | 0.0645161 | 0.0562696 | 0.160526 | 0 | 1 | 0 | validation_extension_mixed_or_negative_by_date_add_more_validation_or_redesign_before_test | 0 | 0 |

## By Date

| candidate_id | latency_profile_id | split_role | trade_date | decision_events | symbols | dates | gross_return_bps_proxy_mean | cost_bound_bps_mean | net_return_bps_after_cost_proxy_mean | net_positive_event_fraction | shuffled_time_net_bps_proxy_mean | shuffled_symbol_net_bps_proxy_mean | net_edge_over_shuffled_time_bps_mean | net_edge_over_shuffled_symbol_bps_mean | net_positive_group | beats_shuffled_time_group | beats_shuffled_symbol_group |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | unassigned | 2026-07-15 | 1189 | 28 | 1 | 0.166562 | 11.9534 | -11.7868 | 0.000841043 | -11.9848 | -28.7798 | 0.197923 | 16.993 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | unassigned | 2026-07-16 | 989 | 28 | 1 | 0.120314 | 11.6517 | -11.5314 | 0 | -11.5977 | -11.7224 | 0.0662763 | 0.191 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 2026-07-13 | 1323 | 30 | 1 | 60.5943 | 12.195 | 48.3994 | 0.00604686 | 2.90978 | -12.199 | 45.4896 | 60.5983 | 1 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | unassigned | 2026-07-15 | 1189 | 28 | 1 | 0.166562 | 13.9504 | -13.7838 | 0 | 11.2414 | -30.7768 | -25.0252 | 16.993 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | unassigned | 2026-07-16 | 989 | 28 | 1 | 0.120314 | 13.3652 | -13.2449 | 0 | -43.7153 | -13.4359 | 30.4704 | 0.191 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | validation | 2026-07-13 | 1323 | 30 | 1 | 60.5943 | 14.2634 | 46.3309 | 0.00604686 | -14.2729 | -14.2674 | 60.6039 | 60.5983 | 1 | 1 | 1 |

## By Symbol

| candidate_id | latency_profile_id | symbol | decision_events | symbols | dates | gross_return_bps_proxy_mean | cost_bound_bps_mean | net_return_bps_after_cost_proxy_mean | net_positive_event_fraction | shuffled_time_net_bps_proxy_mean | shuffled_symbol_net_bps_proxy_mean | net_edge_over_shuffled_time_bps_mean | net_edge_over_shuffled_symbol_bps_mean | net_positive_group | beats_shuffled_time_group | beats_shuffled_symbol_group |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ADANIPORTS | 78 | 1 | 3 | 0.413476 | 11.2371 | -10.8237 | 0 | -139.492 | -11.1562 | 128.669 | 0.332515 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | AXISBANK | 55 | 1 | 3 | 727.68 | 11.7589 | 715.921 | 0.0727273 | -11.8067 | -11.9231 | 727.727 | 727.844 | 1 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | BAJAJ-AUTO | 138 | 1 | 3 | 0.0829483 | 10.2398 | -10.1569 | 0 | -10.134 | -10.2643 | -0.0228487 | 0.107437 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | BANKBEES | 394 | 1 | 3 | 0.122124 | 12.7771 | -12.655 | 0 | -12.7655 | -12.7431 | 0.110578 | 0.0881772 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | BHARTIARTL | 60 | 1 | 3 | -0.172225 | 10.5696 | -10.7418 | 0 | -10.4467 | -10.4633 | -0.295089 | -0.27851 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | BPCL | 1 | 1 | 1 | 1.62483 | 14.7674 | -13.1426 | 0 | -14.7674 | -14.7674 | 1.62483 | 1.62483 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | BRITANNIA | 72 | 1 | 3 | 0.398016 | 11.5914 | -11.1934 | 0 | -150.51 | -11.8164 | 139.317 | 0.62298 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | CIPLA | 51 | 1 | 3 | 0.129542 | 11.7308 | -11.6013 | 0 | -11.6642 | -12.1625 | 0.0629508 | 0.561195 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | DRREDDY | 18 | 1 | 3 | 0.182054 | 11.5163 | -11.3342 | 0 | -11.4703 | -11.7675 | 0.136023 | 0.433224 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | GOLDBEES | 33 | 1 | 3 | 0.0128768 | 18.9678 | -18.9549 | 0 | -19.0325 | -19.0279 | 0.0775447 | 0.0729789 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | HCLTECH | 32 | 1 | 2 | 0.356127 | 12.2684 | -11.9122 | 0 | -12.2075 | -12.2928 | 0.295253 | 0.380567 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | HDFCBANK | 182 | 1 | 3 | 0.205038 | 11.3733 | -11.1683 | 0 | -11.4155 | -11.3546 | 0.247265 | 0.186362 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | HINDUNILVR | 57 | 1 | 3 | 0.112763 | 11.2585 | -11.1457 | 0 | -11.4374 | -10.9698 | 0.291657 | -0.175889 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ICICIBANK | 140 | 1 | 3 | 0.273631 | 10.8504 | -10.5768 | 0 | -10.9367 | -10.7302 | 0.359935 | 0.153362 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | INFY | 34 | 1 | 3 | 0.591954 | 11.6782 | -11.0862 | 0 | -11.7873 | -11.6415 | 0.701018 | 0.555255 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ITC | 6 | 1 | 1 | 6666.67 | 15.4133 | 6651.25 | 0.666667 | -15.456 | -15.3733 | 6666.71 | 6666.63 | 1 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | JUNIORBEES | 258 | 1 | 3 | 0.0404509 | 12.2954 | -12.255 | 0 | 26.6024 | -12.2707 | -38.8574 | 0.0156902 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | KOTAKBANK | 4 | 1 | 1 | 0 | 13.5551 | -13.5551 | 0 | -13.3832 | -13.6617 | -0.171995 | 0.106544 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | LT | 235 | 1 | 3 | 0.108064 | 10.1986 | -10.0905 | 0 | -10.1423 | -10.2842 | 0.0517244 | 0.193695 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | M&M | 228 | 1 | 3 | 0.0335127 | 10.4233 | -10.3898 | 0 | -10.4597 | -10.4624 | 0.069878 | 0.0726166 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | MARUTI | 70 | 1 | 3 | 0.276527 | 10.9246 | -10.6481 | 0 | -11.0235 | 132.285 | 0.375397 | -142.933 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | NESTLEIND | 51 | 1 | 3 | 0.0874616 | 11.4635 | -11.376 | 0 | -11.1492 | -11.5458 | -0.226794 | 0.169784 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | NIFTYBEES | 336 | 1 | 3 | 0.0889341 | 14.3127 | -14.2238 | 0 | -44.1521 | -14.4108 | 29.9283 | 0.18701 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ONGC | 109 | 1 | 3 | 0.177966 | 14.5143 | -14.3364 | 0.00917431 | -14.324 | 77.1242 | -0.0123984 | -91.4606 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | RELIANCE | 113 | 1 | 3 | 0.361061 | 11.2703 | -10.9093 | 0 | -11.4886 | -188.244 | 0.579308 | 177.335 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | SBIN | 42 | 1 | 3 | 0.313619 | 11.5499 | -11.2363 | 0 | -11.7775 | -11.2366 | 0.541208 | 0.000313719 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | SUNPHARMA | 152 | 1 | 3 | 0.185183 | 10.9802 | -10.795 | 0 | -10.9841 | -76.9866 | 0.189141 | 66.1916 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | TCS | 221 | 1 | 3 | 0.0894271 | 10.8858 | -10.7963 | 0 | 124.875 | -10.8804 | -135.671 | 0.0840616 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | TECHM | 31 | 1 | 3 | -0.446297 | 10.9869 | -11.4332 | 0 | -11.2151 | -10.8737 | -0.218055 | -0.559448 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ULTRACEMCO | 180 | 1 | 3 | 0.029331 | 10.9363 | -10.9069 | 0 | -10.8958 | -66.4982 | -0.0111429 | 55.5913 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | WIPRO | 120 | 1 | 3 | 0.128579 | 16.5757 | -16.4471 | 0 | 66.7433 | -16.7992 | -83.1904 | 0.352146 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ADANIPORTS | 78 | 1 | 3 | 0.413476 | 12.3889 | -11.9754 | 0 | -12.3902 | -12.3079 | 0.414812 | 0.332515 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | AXISBANK | 55 | 1 | 3 | 727.68 | 13.2009 | 714.479 | 0.0727273 | -13.3575 | -13.3651 | 727.836 | 727.844 | 1 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | BAJAJ-AUTO | 138 | 1 | 3 | 0.0829483 | 10.8054 | -10.7224 | 0 | -83.3443 | -10.8299 | 72.6219 | 0.107437 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | BANKBEES | 394 | 1 | 3 | 0.122124 | 15.1582 | -15.0361 | 0 | 10.2145 | -15.1243 | -25.2506 | 0.0881772 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | BHARTIARTL | 60 | 1 | 3 | -0.172225 | 11.5377 | -11.7099 | 0 | -11.1713 | -11.4314 | -0.538613 | -0.27851 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | BPCL | 1 | 1 | 1 | 1.62483 | 18.8295 | -17.2047 | 0 | -18.8295 | -18.8295 | 1.62483 | 1.62483 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | BRITANNIA | 72 | 1 | 3 | 0.398016 | 12.5633 | -12.1653 | 0 | -12.3777 | -12.7883 | 0.212409 | 0.62298 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | CIPLA | 51 | 1 | 3 | 0.129542 | 13.1201 | -12.9906 | 0 | -13.1829 | -13.5518 | 0.192337 | 0.561195 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | DRREDDY | 18 | 1 | 3 | 0.182054 | 12.9375 | -12.7554 | 0 | -12.8996 | -13.1886 | 0.144157 | 0.433224 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | GOLDBEES | 33 | 1 | 3 | 0.0128768 | 28.0701 | -28.0573 | 0 | -28.2194 | -28.1302 | 0.162129 | 0.0729789 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | HCLTECH | 32 | 1 | 2 | 0.356127 | 13.8845 | -13.5284 | 0 | -14.0077 | -13.9089 | 0.479319 | 0.380567 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | HDFCBANK | 182 | 1 | 3 | 0.205038 | 13.0671 | -12.862 | 0 | 41.7456 | -13.0484 | -54.6077 | 0.186362 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | HINDUNILVR | 57 | 1 | 3 | 0.112763 | 12.3621 | -12.2494 | 0 | -12.3209 | -12.0735 | 0.0715322 | -0.175889 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ICICIBANK | 140 | 1 | 3 | 0.273631 | 12.0275 | -11.7539 | 0 | -12.0249 | -11.9073 | 0.271002 | 0.153362 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | INFY | 34 | 1 | 3 | 0.591954 | 13.2205 | -12.6286 | 0 | -12.8915 | -13.1838 | 0.262876 | 0.555255 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ITC | 6 | 1 | 1 | 6666.67 | 19.8791 | 6646.79 | 0.666667 | -19.3881 | -19.839 | 6666.18 | 6666.63 | 1 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | JUNIORBEES | 258 | 1 | 3 | 0.0404509 | 14.2655 | -14.225 | 0 | -14.2104 | -14.2407 | -0.0146464 | 0.0156902 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | KOTAKBANK | 4 | 1 | 1 | 0 | 16.8595 | -16.8595 | 0 | -17.4155 | -16.9661 | 0.555992 | 0.106544 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | LT | 235 | 1 | 3 | 0.108064 | 10.8785 | -10.7704 | 0 | -53.5316 | -10.9641 | 42.7611 | 0.193695 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | M&M | 228 | 1 | 3 | 0.0335127 | 11.2026 | -11.1691 | 0 | -11.4406 | -11.2417 | 0.271564 | 0.0726166 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | MARUTI | 70 | 1 | 3 | 0.276527 | 11.6434 | -11.3669 | 0 | -11.6883 | 131.566 | 0.321355 | -142.933 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | NESTLEIND | 51 | 1 | 3 | 0.0874616 | 12.7868 | -12.6993 | 0 | -12.7966 | -12.8691 | 0.0972974 | 0.169784 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | NIFTYBEES | 336 | 1 | 3 | 0.0889341 | 18.5557 | -18.4668 | 0 | -18.5892 | -18.6538 | 0.122382 | 0.18701 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ONGC | 109 | 1 | 3 | 0.177966 | 19.1082 | -18.9303 | 0 | -110.778 | 72.5303 | 91.8477 | -91.4606 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | RELIANCE | 113 | 1 | 3 | 0.361061 | 12.5977 | -12.2366 | 0 | -12.7105 | -189.571 | 0.473892 | 177.335 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | SBIN | 42 | 1 | 3 | 0.313619 | 13.0985 | -12.7849 | 0 | -12.8576 | -12.7852 | 0.0727039 | 0.000313719 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | SUNPHARMA | 152 | 1 | 3 | 0.185183 | 12.0427 | -11.8575 | 0 | 119.629 | -78.0491 | -131.486 | 66.1916 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | TCS | 221 | 1 | 3 | 0.0894271 | 11.8832 | -11.7938 | 0 | -57.1802 | -11.8779 | 45.3864 | 0.0840616 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | TECHM | 31 | 1 | 3 | -0.446297 | 12.1639 | -12.6102 | 0 | -12.1789 | -12.0507 | -0.43129 | -0.559448 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ULTRACEMCO | 180 | 1 | 3 | 0.029331 | 11.6674 | -11.6381 | 0 | -11.6872 | -67.2294 | 0.0491136 | 55.5913 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | WIPRO | 120 | 1 | 3 | 0.128579 | 22.8775 | -22.7489 | 0 | -22.831 | -23.1011 | 0.0820433 | 0.352146 | 0 | 1 | 1 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P193_PHASE191_HASH_MATCH | 1 | candidate_contract_hash=6aec9abe7f1da4c49372eb44b3fa050e44c1b8105dd4bc0c47efd9357af697d1 | hard |
| P193_EXTENSION_ROWS_PRESENT | 1 | unassigned_extension_rows=1133776 | hard |
| P193_TEST_UNTOUCHED_EXCLUDED | 1 | test_partitions_used=0 | hard |
| P193_DATE_SYMBOL_AUDITS_PRESENT | 1 | date_rows=6; symbol_rows=62 | hard |
| P193_NEGATIVE_CONTROLS_PRESENT | 1 | shuffled_time;shuffled_symbol | hard |
| P193_DECISION_RATE_BUDGET_RESPECTED | 1 | decision_rate=0.004130578670357169; max_decision_rate=0.01 | hard |
| P193_NO_TEST_REPLAY_OR_PROMOTION | 1 | test_replay_allowed_by_phase193=0; promotion_allowed=0 | hard |

# Phase193 Validation Breadth Extension Replay

Generated UTC: 2026-07-28T18:10:52.508402+00:00

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
| phase193_extension_validation_dates | 2026-07-15 | Added validation-extension dates represented in events |
| phase193_validation_dates_with_events | 2 | Validation/extension dates with decision events |
| phase193_validation_extension_decision_events | 5024 | Dry decision events across validation plus extension |
| phase193_decision_rate | 0.00446857 | Decision-event rate over evaluation rows |
| phase193_min_profile_net_bps_proxy_mean | 17.8769 | Minimum profile net bps |
| phase193_min_profile_edge_over_shuffled_time_bps | 32.0118 | Minimum profile edge over shuffled-time control |
| phase193_min_profile_edge_over_shuffled_symbol_bps | 16.0748 | Minimum profile edge over shuffled-symbol control |
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
| P187_TOP5_I85_S2p5_Z1_R100 | 6aec9abe7f1da4c49372eb44b3fa050e44c1b8105dd4bc0c47efd9357af697d1 | unassigned;validation | 2026-07-13 | 2026-07-15 | 5024 | 1124297 | 0.00446857 | 31 | 2 | 18.8942 | 31.9922 | 13.0979 | 17.8769 | 32.0118 | 16.0748 | 0.5 | 0.0645161 | 0.0571258 | 0.158041 | 0 | 1 | 0 | validation_extension_mixed_or_negative_by_date_add_more_validation_or_redesign_before_test | 0 | 0 |

## By Date

| candidate_id | latency_profile_id | split_role | trade_date | decision_events | symbols | dates | gross_return_bps_proxy_mean | cost_bound_bps_mean | net_return_bps_after_cost_proxy_mean | net_positive_event_fraction | shuffled_time_net_bps_proxy_mean | shuffled_symbol_net_bps_proxy_mean | net_edge_over_shuffled_time_bps_mean | net_edge_over_shuffled_symbol_bps_mean | net_positive_group | beats_shuffled_time_group | beats_shuffled_symbol_group |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | unassigned | 2026-07-15 | 1189 | 28 | 1 | 0.166562 | 11.9534 | -11.7868 | 0.000841043 | 13.2333 | 13.2577 | -25.0201 | -25.0445 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | validation | 2026-07-13 | 1323 | 30 | 1 | 60.5943 | 12.195 | 48.3994 | 0.00604686 | -34.8678 | -4.62997 | 83.2672 | 53.0293 | 1 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | unassigned | 2026-07-15 | 1189 | 28 | 1 | 0.166562 | 13.9504 | -13.7838 | 0 | -22.3624 | 11.2607 | 8.57853 | -25.0445 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | validation | 2026-07-13 | 1323 | 30 | 1 | 60.5943 | 14.2634 | 46.3309 | 0.00604686 | -21.8474 | -6.69839 | 68.1783 | 53.0293 | 1 | 1 | 1 |

## By Symbol

| candidate_id | latency_profile_id | symbol | decision_events | symbols | dates | gross_return_bps_proxy_mean | cost_bound_bps_mean | net_return_bps_after_cost_proxy_mean | net_positive_event_fraction | shuffled_time_net_bps_proxy_mean | shuffled_symbol_net_bps_proxy_mean | net_edge_over_shuffled_time_bps_mean | net_edge_over_shuffled_symbol_bps_mean | net_positive_group | beats_shuffled_time_group | beats_shuffled_symbol_group |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ADANIPORTS | 42 | 1 | 2 | 0.516169 | 11.4556 | -10.9394 | 0 | -11.3282 | -11.3481 | 0.388803 | 0.408745 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | AXISBANK | 54 | 1 | 2 | 741.268 | 11.7812 | 729.487 | 0.0740741 | -11.7049 | -11.9939 | 741.192 | 741.481 | 1 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | BAJAJ-AUTO | 52 | 1 | 2 | 0.484503 | 10.8691 | -10.3846 | 0 | -11.3528 | -10.9303 | 0.96822 | 0.545702 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | BANKBEES | 220 | 1 | 2 | 0.0964906 | 12.8855 | -12.7891 | 0 | -58.3766 | 32.564 | 45.5875 | -45.3531 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | BHARTIARTL | 55 | 1 | 2 | -0.235105 | 10.5808 | -10.816 | 0 | -10.459 | -10.2465 | -0.356985 | -0.569489 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | BPCL | 1 | 1 | 1 | 1.62483 | 14.7674 | -13.1426 | 0 | -14.7674 | -16.3726 | 1.62483 | 3.22996 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | BRITANNIA | 10 | 1 | 2 | 0.280156 | 12.1956 | -11.9154 | 0 | -13.1526 | -12.3066 | 1.23716 | 0.39114 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | CIPLA | 22 | 1 | 2 | 0.142582 | 11.7635 | -11.6209 | 0 | 442.762 | -11.8475 | -454.382 | 0.226546 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | DRREDDY | 12 | 1 | 2 | -0.100946 | 11.646 | -11.7469 | 0 | -11.6722 | -11.3253 | -0.0747485 | -0.421623 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | GOLDBEES | 31 | 1 | 2 | 0.0137076 | 18.8826 | -18.8689 | 0 | -18.6247 | -18.7928 | -0.244276 | -0.076132 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | HCLTECH | 28 | 1 | 1 | 0.332754 | 12.185 | -11.8522 | 0 | -11.8851 | -12.4141 | 0.0328695 | 0.561934 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | HDFCBANK | 162 | 1 | 2 | 0.211303 | 11.3836 | -11.1723 | 0 | -11.2941 | 50.3693 | 0.121779 | -61.5416 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | HINDUNILVR | 31 | 1 | 2 | 0.0468057 | 11.5029 | -11.4561 | 0 | -12.0261 | -11.5695 | 0.569954 | 0.113421 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ICICIBANK | 122 | 1 | 2 | 0.293644 | 10.8829 | -10.5893 | 0 | 71.1524 | 70.7518 | -81.7417 | -81.3411 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | INFY | 32 | 1 | 2 | 0.599946 | 11.7184 | -11.1185 | 0 | -11.8464 | -11.5794 | 0.727945 | 0.460882 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ITC | 6 | 1 | 1 | 6666.67 | 15.4133 | 6651.25 | 0.666667 | -15.3186 | -15.4185 | 6666.57 | 6666.67 | 1 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | JUNIORBEES | 205 | 1 | 2 | 0.025846 | 12.3059 | -12.28 | 0 | 36.4596 | -12.2235 | -48.7396 | -0.0565361 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | KOTAKBANK | 4 | 1 | 1 | 0 | 13.5551 | -13.5551 | 0 | -13.3726 | -12.9879 | -0.182528 | -0.567264 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | LT | 121 | 1 | 2 | 0.0726996 | 10.3757 | -10.303 | 0 | -93.0251 | -10.5387 | 82.7221 | 0.23574 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | M&M | 176 | 1 | 2 | -0.00196159 | 10.3048 | -10.3067 | 0 | -10.5487 | -66.908 | 0.241993 | 56.6013 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | MARUTI | 43 | 1 | 2 | 0.30695 | 11.0256 | -10.7187 | 0 | -11.0778 | -11.2514 | 0.359142 | 0.532668 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | NESTLEIND | 37 | 1 | 2 | 0.12052 | 11.3475 | -11.227 | 0 | -11.6416 | -10.6119 | 0.414634 | -0.615021 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | NIFTYBEES | 287 | 1 | 2 | 0.0780823 | 14.4124 | -14.3343 | 0 | -84.1136 | -14.4456 | 69.7793 | 0.111303 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ONGC | 82 | 1 | 2 | 0.234129 | 14.3648 | -14.1307 | 0.0121951 | -14.4473 | 107.559 | 0.316651 | -121.689 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | RELIANCE | 91 | 1 | 2 | 0.317615 | 11.4061 | -11.0885 | 0 | -11.2657 | 98.3903 | 0.177227 | -109.479 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | SBIN | 35 | 1 | 2 | 0.362539 | 11.6262 | -11.2636 | 0 | -11.5229 | -11.5704 | 0.259308 | 0.306794 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | SUNPHARMA | 117 | 1 | 2 | 0.225238 | 10.9895 | -10.7642 | 0 | -10.9554 | -10.8761 | 0.191156 | 0.1119 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | TCS | 159 | 1 | 2 | 0.111587 | 11.0266 | -10.915 | 0 | 51.7009 | -11.1691 | -62.6158 | 0.254159 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | TECHM | 19 | 1 | 2 | -0.952583 | 11.1849 | -12.1374 | 0 | -10.8916 | -11.1009 | -1.24587 | -1.03651 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ULTRACEMCO | 175 | 1 | 2 | 0.0325773 | 10.9427 | -10.9101 | 0 | -10.791 | -11.0967 | -0.119127 | 0.186578 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | WIPRO | 81 | 1 | 2 | 0.340784 | 16.3451 | -16.0043 | 0 | -16.3139 | -16.1682 | 0.309604 | 0.163923 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ADANIPORTS | 42 | 1 | 2 | 0.516169 | 12.6641 | -12.1479 | 0 | -12.726 | -12.5567 | 0.578116 | 0.408745 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | AXISBANK | 54 | 1 | 2 | 741.268 | 13.2286 | 728.04 | 0.0740741 | 172.002 | -13.4414 | 556.037 | 741.481 | 1 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | BAJAJ-AUTO | 52 | 1 | 2 | 0.484503 | 11.5922 | -11.1077 | 0 | -204.213 | -11.6534 | 193.106 | 0.545702 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | BANKBEES | 220 | 1 | 2 | 0.0964906 | 15.2916 | -15.1952 | 0 | -15.258 | 30.1579 | 0.0628188 | -45.3531 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | BHARTIARTL | 55 | 1 | 2 | -0.235105 | 11.5521 | -11.7872 | 0 | 170.283 | -11.2177 | -182.071 | -0.569489 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | BPCL | 1 | 1 | 1 | 1.62483 | 18.8295 | -17.2047 | 0 | -18.2708 | -20.4346 | 1.06609 | 3.22996 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | BRITANNIA | 10 | 1 | 2 | 0.280156 | 13.3177 | -13.0375 | 0 | -13.3289 | -13.4287 | 0.291366 | 0.39114 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | CIPLA | 22 | 1 | 2 | 0.142582 | 13.1619 | -13.0193 | 0 | -13.6314 | -13.2458 | 0.612128 | 0.226546 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | DRREDDY | 12 | 1 | 2 | -0.100946 | 13.0984 | -13.1993 | 0 | -13.1842 | -12.7777 | -0.0151661 | -0.421623 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | GOLDBEES | 31 | 1 | 2 | 0.0137076 | 27.963 | -27.9493 | 0 | -27.7822 | -27.8731 | -0.16704 | -0.076132 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | HCLTECH | 28 | 1 | 1 | 0.332754 | 13.7788 | -13.4461 | 0 | -14.1309 | -14.008 | 0.684812 | 0.561934 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | HDFCBANK | 162 | 1 | 2 | 0.211303 | 13.079 | -12.8677 | 0 | -13.1035 | 48.6739 | 0.235767 | -61.5416 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | HINDUNILVR | 31 | 1 | 2 | 0.0468057 | 12.6681 | -12.6213 | 0 | -12.7257 | -12.7347 | 0.104385 | 0.113421 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ICICIBANK | 122 | 1 | 2 | 0.293644 | 12.0681 | -11.7745 | 0 | -12.2075 | 69.5666 | 0.432974 | -81.3411 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | INFY | 32 | 1 | 2 | 0.599946 | 13.2707 | -12.6708 | 0 | -13.2638 | -13.1316 | 0.593065 | 0.460882 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ITC | 6 | 1 | 1 | 6666.67 | 19.8791 | 6646.79 | 0.666667 | -20.3648 | -19.8843 | 6667.15 | 6666.67 | 1 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | JUNIORBEES | 205 | 1 | 2 | 0.025846 | 14.2787 | -14.2528 | 0 | -14.2348 | -14.1963 | -0.018048 | -0.0565361 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | KOTAKBANK | 4 | 1 | 1 | 0 | 16.8595 | -16.8595 | 0 | -16.8595 | -16.2923 | 0 | -0.567264 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | LT | 121 | 1 | 2 | 0.0726996 | 11.0984 | -11.0257 | 0 | -11.0411 | -11.2615 | 0.0153485 | 0.23574 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | M&M | 176 | 1 | 2 | -0.00196159 | 11.0546 | -11.0566 | 0 | -67.7985 | -67.6579 | 56.7419 | 56.6013 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | MARUTI | 43 | 1 | 2 | 0.30695 | 11.7698 | -11.4629 | 0 | -11.8621 | -11.9955 | 0.399228 | 0.532668 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | NESTLEIND | 37 | 1 | 2 | 0.12052 | 12.6416 | -12.5211 | 0 | -12.9205 | -11.9061 | 0.399358 | -0.615021 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | NIFTYBEES | 287 | 1 | 2 | 0.0780823 | 18.6799 | -18.6018 | 0 | -123.24 | -18.7131 | 104.638 | 0.111303 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ONGC | 82 | 1 | 2 | 0.234129 | 18.918 | -18.6839 | 0 | -18.8627 | 103.006 | 0.17884 | -121.689 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | RELIANCE | 91 | 1 | 2 | 0.317615 | 12.7677 | -12.4501 | 0 | -12.7114 | 97.0287 | 0.261248 | -109.479 | 0 | 1 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | SBIN | 35 | 1 | 2 | 0.362539 | 13.1944 | -12.8318 | 0 | -13.3489 | -13.1386 | 0.517087 | 0.306794 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | SUNPHARMA | 117 | 1 | 2 | 0.225238 | 12.0542 | -11.829 | 0 | 73.5513 | -11.9409 | -85.3803 | 0.1119 | 0 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | TCS | 159 | 1 | 2 | 0.111587 | 12.061 | -11.9494 | 0 | -12.1131 | -12.2036 | 0.163685 | 0.254159 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | TECHM | 19 | 1 | 2 | -0.952583 | 12.4146 | -13.3672 | 0 | -12.6259 | -12.3307 | -0.741332 | -1.03651 | 0 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ULTRACEMCO | 175 | 1 | 2 | 0.0325773 | 11.6755 | -11.6429 | 0 | -11.7077 | -11.8295 | 0.0648319 | 0.186578 | 0 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | WIPRO | 81 | 1 | 2 | 0.340784 | 22.5881 | -22.2474 | 0 | -22.525 | -22.4113 | 0.277662 | 0.163923 | 0 | 1 | 1 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P193_PHASE191_HASH_MATCH | 1 | candidate_contract_hash=6aec9abe7f1da4c49372eb44b3fa050e44c1b8105dd4bc0c47efd9357af697d1 | hard |
| P193_EXTENSION_ROWS_PRESENT | 1 | unassigned_extension_rows=562911 | hard |
| P193_TEST_UNTOUCHED_EXCLUDED | 1 | test_partitions_used=0 | hard |
| P193_DATE_SYMBOL_AUDITS_PRESENT | 1 | date_rows=4; symbol_rows=62 | hard |
| P193_NEGATIVE_CONTROLS_PRESENT | 1 | shuffled_time;shuffled_symbol | hard |
| P193_DECISION_RATE_BUDGET_RESPECTED | 1 | decision_rate=0.004468570137605988; max_decision_rate=0.01 | hard |
| P193_NO_TEST_REPLAY_OR_PROMOTION | 1 | test_replay_allowed_by_phase193=0; promotion_allowed=0 | hard |

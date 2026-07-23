# Phase133 Retail Passive Execution Model Upgrade

Generated UTC: 2026-07-23T08:39:33.584056+00:00

Phase133 emits a conservative visible-depth passive-fill contract and sanity-checks Phase89 passive queue-capture evidence under that contract.
It creates no strategy definitions, no order-arrival stream, no live-tagged fill model, and no promoted profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase133_hard_gate_rows | 5 | Hard execution-model gates evaluated |
| phase133_hard_gate_pass_rows | 5 | Hard execution-model gates passed |
| phase133_contract_created | 1 | Pinned execution contract emitted |
| phase133_phase132_kill_switch_fired | 1 | Inherited Phase132 kill-switch flag |
| phase133_phase132_surviving_feature_rows | 0 | Inherited Phase132 surviving feature rows |
| phase133_phase89_sanity_rows | 54 | Phase89 fill-assumption rows re-evaluated under Phase133 fill model |
| phase133_best_sanity_test_expected_net_pnl_inr | -23942.1 | Best Phase133 sanity replay expected test PnL |
| phase133_worst_sanity_test_expected_net_pnl_inr | -2.24521e+06 | Worst Phase133 sanity replay expected test PnL |
| phase133_phase134_open_allowed | 0 | 1 means Phase134 precommit may open |
| phase133_strategy_replay_allowed | 0 | Phase133 never unlocks strategy replay |
| phase133_next_best_action | stop_update_phase116_blocklist_do_not_open_phase134 | Recommended next milestone |

## Gate Evaluation

| gate | pass | observed | required | severity |
| --- | --- | --- | --- | --- |
| phase133_contract_created | True | phase133_retail_passive_visible_depth_fill_model_v1_2026_07_23 | non_empty_contract_version | hard |
| phase133_phase132_kill_switch_respected | True | kill_switch=1;phase134_open_allowed=False | kill_switch_blocks_phase134 | hard |
| phase133_no_phase132_surviving_features_promoted | True | surviving_features=0;sanity_survivors=0 | zero_promoted_survivors | hard |
| phase133_phase89_sanity_direction_consistent | True | 1 | 1 | hard |
| phase133_strategy_replay_remains_closed | True | 0 | 0 | hard |

## Latency Distribution

| quantile | latency_ms | description |
| --- | --- | --- |
| p01 | 25 | best_case_local_stack_but_not_zero_latency |
| p05 | 50 | lower_tail_retail_websocket_to_order_path |
| p25 | 90 | fast_retail_path |
| p50 | 175 | central_mass |
| p75 | 300 | central_mass_upper |
| p90 | 550 | fat_right_tail |
| p95 | 900 | fat_right_tail |
| p99 | 1750 | pathological_retail_network_or_app_delay |

## Phase6 Generator Anchor

| anchor_id | source_rows | book_state_update_fraction | spread_widening_fraction | best_price_shift_fraction | median_event_intensity_proxy | median_l5_quantity | fill_probability_scale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| phase6_generator_event_depth_anchor | 453600 | 0.874063 | 0.0857451 | 0.0250816 | 1.40082 | 398.5 | 1.25 |

## Cancel Intensity Inputs

| depth_level | cancel_intensity_source | cancel_intensity_mean | cancel_intensity_p50 | cancel_intensity_p90 | cancel_intensity_multiplier |
| --- | --- | --- | --- | --- | --- |
| 1 | phase132_top_five_depth_feature_matrix.p131_mean_cancel_intensity_depth_levels_2_5 | 0.536669 | 0.486885 | 0.938666 | 1.41385 |
| 2 | phase132_top_five_depth_feature_matrix.p131_mean_cancel_intensity_depth_levels_2_5 | 0.536669 | 0.486885 | 0.938666 | 1.48689 |
| 3 | phase132_top_five_depth_feature_matrix.p131_mean_cancel_intensity_depth_levels_2_5 | 0.536669 | 0.486885 | 0.938666 | 1.5 |
| 4 | phase132_top_five_depth_feature_matrix.p131_mean_cancel_intensity_depth_levels_2_5 | 0.536669 | 0.486885 | 0.938666 | 1.5 |
| 5 | phase132_top_five_depth_feature_matrix.p131_mean_cancel_intensity_depth_levels_2_5 | 0.536669 | 0.486885 | 0.938666 | 1.5 |

## Phase89 Sanity Replay

| candidate_id | feature_name | fill_assumption | inferred_depth_level | inferred_queue_percentile | phase89_base_fill_prob | phase133_model_fill_prob | fill_ratio_vs_phase89 | phase89_test_expected_fills | phase133_test_expected_fills | phase89_test_expected_net_pnl_inr | phase133_test_expected_net_pnl_inr | directionally_consistent_with_phase89 | phase133_passive_branch_survives | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P89_L5_IMBALANCE_Q0_9_I0_75 | l5_imbalance | pessimistic_queue | 5 | 0.9 | 0.12 | 0.0406173 | 0.338478 | 240.207 | 81.3047 | -187946 | -63615.4 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_9_I0_75 | l1_imbalance | pessimistic_queue | 1 | 0.9 | 0.12 | 0.0568976 | 0.474147 | 242.237 | 114.856 | -189428 | -89816.5 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_9_I0_75 | l5_imbalance | base_queue | 5 | 0.9 | 0.25 | 0.0406173 | 0.162469 | 450.05 | 73.1193 | -261152 | -42429.2 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_9_I0_75 | l1_imbalance | base_queue | 1 | 0.9 | 0.25 | 0.0568976 | 0.22759 | 453.425 | 103.195 | -263621 | -59997.7 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_9_I0_75 | l5_imbalance | optimistic_queue | 5 | 0.9 | 0.45 | 0.0406173 | 0.0902607 | 805.05 | 72.6644 | -265254 | -23942.1 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_9_I0_75 | l1_imbalance | optimistic_queue | 1 | 0.9 | 0.45 | 0.0568976 | 0.126439 | 810.225 | 102.444 | -269027 | -34015.6 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_9_I0_5 | l5_imbalance | pessimistic_queue | 5 | 0.9 | 0.12 | 0.0406173 | 0.338478 | 502.382 | 170.045 | -298011 | -100870 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_9_I0_5 | l1_imbalance | pessimistic_queue | 1 | 0.9 | 0.12 | 0.0568976 | 0.474147 | 503.421 | 238.695 | -298513 | -141539 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_9_I0_75 | microprice_dev | pessimistic_queue | 1 | 0.9 | 0.12 | 0.0568976 | 0.474147 | 349.403 | 165.668 | -333271 | -158019 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_9_I0_5 | l5_imbalance | optimistic_queue | 5 | 0.9 | 0.45 | 0.0406173 | 0.0902607 | 1534.05 | 138.464 | -377009 | -34029.1 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_9_I0_5 | l1_imbalance | optimistic_queue | 1 | 0.9 | 0.45 | 0.0568976 | 0.126439 | 1536.53 | 194.277 | -379480 | -47981.1 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_9_I0_5 | l5_imbalance | base_queue | 5 | 0.9 | 0.25 | 0.0406173 | 0.162469 | 900.925 | 146.373 | -394715 | -64129 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_9_I0_5 | l1_imbalance | base_queue | 1 | 0.9 | 0.25 | 0.0568976 | 0.22759 | 902.612 | 205.426 | -395910 | -90105.3 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_9_I0_5 | microprice_dev | pessimistic_queue | 1 | 0.9 | 0.12 | 0.0568976 | 0.474147 | 545.727 | 258.755 | -418659 | -198506 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_75_I0_75 | l1_imbalance | pessimistic_queue | 1 | 0.75 | 0.12 | 0.113795 | 0.948294 | 620.892 | 588.788 | -502157 | -476192 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_75_I0_75 | l5_imbalance | pessimistic_queue | 5 | 0.75 | 0.12 | 0.0812347 | 0.676955 | 621.864 | 420.974 | -502933 | -340463 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_9_I0_75 | microprice_dev | base_queue | 1 | 0.9 | 0.25 | 0.0568976 | 0.22759 | 682.075 | 155.234 | -507229 | -115440 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_9_I0_75 | microprice_dev | optimistic_queue | 1 | 0.9 | 0.45 | 0.0568976 | 0.126439 | 1269.34 | 160.494 | -603564 | -76314.1 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_9_I0_5 | microprice_dev | base_queue | 1 | 0.9 | 0.25 | 0.0568976 | 0.22759 | 1026.84 | 233.698 | -611954 | -139275 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_75_I0_75 | microprice_dev | pessimistic_queue | 1 | 0.75 | 0.12 | 0.113795 | 0.948294 | 761.292 | 721.928 | -686569 | -651069 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_9_I0_5 | microprice_dev | optimistic_queue | 1 | 0.9 | 0.45 | 0.0568976 | 0.126439 | 1841.51 | 232.839 | -692228 | -87524.7 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_75_I0_75 | l1_imbalance | base_queue | 1 | 0.75 | 0.25 | 0.113795 | 0.455181 | 1169.08 | 532.141 | -693072 | -315473 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_75_I0_75 | l5_imbalance | base_queue | 5 | 0.75 | 0.25 | 0.0812347 | 0.324939 | 1169.53 | 380.024 | -694637 | -225715 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_75_I0_75 | l1_imbalance | optimistic_queue | 1 | 0.75 | 0.45 | 0.113795 | 0.252878 | 2097.56 | 530.428 | -696599 | -176155 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_75_I0_75 | l5_imbalance | optimistic_queue | 5 | 0.75 | 0.45 | 0.0812347 | 0.180521 | 2096.32 | 378.432 | -699104 | -126203 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_75_I0_5 | l1_imbalance | pessimistic_queue | 1 | 0.75 | 0.12 | 0.113795 | 0.948294 | 1297.74 | 1230.63 | -811450 | -769492 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_75_I0_5 | l5_imbalance | pessimistic_queue | 5 | 0.75 | 0.12 | 0.0812347 | 0.676955 | 1302.23 | 881.553 | -811727 | -549503 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_75_I0_5 | microprice_dev | pessimistic_queue | 1 | 0.75 | 0.12 | 0.113795 | 0.948294 | 1332.82 | 1263.9 | -932470 | -884255 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_75_I0_75 | microprice_dev | base_queue | 1 | 0.75 | 0.25 | 0.113795 | 0.455181 | 1490.85 | 678.606 | -998433 | -454468 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_75_I0_5 | l5_imbalance | optimistic_queue | 5 | 0.75 | 0.45 | 0.0812347 | 0.180521 | 3989.7 | 720.226 | -999657 | -180460 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_75_I0_5 | l1_imbalance | optimistic_queue | 1 | 0.75 | 0.45 | 0.113795 | 0.252878 | 3985.76 | 1007.91 | -1.00094e+06 | -253116 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_5_I0_75 | l1_imbalance | pessimistic_queue | 1 | 0.5 | 0.12 | 0.22759 | 1 | 1207.06 | 1207.06 | -1.014e+06 | -1.014e+06 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_5_I0_75 | l5_imbalance | pessimistic_queue | 5 | 0.5 | 0.12 | 0.162469 | 1 | 1208.38 | 1208.38 | -1.01643e+06 | -1.01643e+06 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_75_I0_5 | l5_imbalance | base_queue | 5 | 0.75 | 0.25 | 0.0812347 | 0.324939 | 2340.13 | 760.397 | -1.06528e+06 | -346151 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_75_I0_5 | l1_imbalance | base_queue | 1 | 0.75 | 0.25 | 0.113795 | 0.455181 | 2334.97 | 1062.84 | -1.06528e+06 | -484896 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_75_I0_75 | microprice_dev | optimistic_queue | 1 | 0.75 | 0.45 | 0.113795 | 0.252878 | 2784.6 | 704.165 | -1.08008e+06 | -273128 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_5_I0_75 | microprice_dev | pessimistic_queue | 1 | 0.5 | 0.12 | 0.22759 | 1 | 1419.4 | 1419.4 | -1.21921e+06 | -1.21921e+06 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_75_I0_5 | microprice_dev | base_queue | 1 | 0.75 | 0.25 | 0.113795 | 0.455181 | 2489.33 | 1133.09 | -1.28827e+06 | -586395 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_75_I0_5 | microprice_dev | optimistic_queue | 1 | 0.75 | 0.45 | 0.113795 | 0.252878 | 4429.91 | 1120.23 | -1.29823e+06 | -328295 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_5_I0_75 | l1_imbalance | base_queue | 1 | 0.5 | 0.25 | 0.22759 | 0.910362 | 2268.94 | 2065.55 | -1.41464e+06 | -1.28783e+06 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_5_I0_75 | l5_imbalance | base_queue | 5 | 0.5 | 0.25 | 0.162469 | 0.649877 | 2272.2 | 1476.65 | -1.4176e+06 | -921265 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_5_I0_75 | l1_imbalance | optimistic_queue | 1 | 0.5 | 0.45 | 0.22759 | 0.505757 | 4071.6 | 2059.24 | -1.45694e+06 | -736855 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_5_I0_75 | l5_imbalance | optimistic_queue | 5 | 0.5 | 0.45 | 0.162469 | 0.361043 | 4079.36 | 1472.82 | -1.45843e+06 | -526555 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_5_I0_5 | l5_imbalance | pessimistic_queue | 5 | 0.5 | 0.12 | 0.162469 | 1 | 2574.67 | 2574.67 | -1.66775e+06 | -1.66775e+06 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_5_I0_5 | l1_imbalance | pessimistic_queue | 1 | 0.5 | 0.12 | 0.22759 | 1 | 2578.84 | 2578.84 | -1.66851e+06 | -1.66851e+06 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_5_I0_75 | microprice_dev | base_queue | 1 | 0.5 | 0.25 | 0.22759 | 0.910362 | 2699.08 | 2457.13 | -1.70071e+06 | -1.54826e+06 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_5_I0_75 | microprice_dev | optimistic_queue | 1 | 0.5 | 0.45 | 0.22759 | 0.505757 | 4911.3 | 2483.92 | -1.70985e+06 | -864769 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_5_I0_5 | microprice_dev | pessimistic_queue | 1 | 0.5 | 0.12 | 0.22759 | 1 | 2720.36 | 2720.36 | -1.84743e+06 | -1.84743e+06 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_5_I0_5 | l5_imbalance | optimistic_queue | 5 | 0.5 | 0.45 | 0.162469 | 0.361043 | 7882.31 | 2845.85 | -2.14001e+06 | -772636 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_5_I0_5 | l1_imbalance | optimistic_queue | 1 | 0.5 | 0.45 | 0.22759 | 0.505757 | 7883.66 | 3987.21 | -2.14207e+06 | -1.08337e+06 | True | False | 0 |
| P89_L5_IMBALANCE_Q0_5_I0_5 | l5_imbalance | base_queue | 5 | 0.5 | 0.25 | 0.162469 | 0.649877 | 4622.56 | 3004.1 | -2.21354e+06 | -1.43853e+06 | True | False | 0 |
| P89_L1_IMBALANCE_Q0_5_I0_5 | l1_imbalance | base_queue | 1 | 0.5 | 0.25 | 0.22759 | 0.910362 | 4626.93 | 4212.18 | -2.21453e+06 | -2.01603e+06 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_5_I0_5 | microprice_dev | optimistic_queue | 1 | 0.5 | 0.45 | 0.22759 | 0.505757 | 8544.6 | 4321.49 | -2.35841e+06 | -1.19278e+06 | True | False | 0 |
| P89_MICROPRICE_DEV_Q0_5_I0_5 | microprice_dev | base_queue | 1 | 0.5 | 0.25 | 0.22759 | 0.910362 | 4940.06 | 4497.24 | -2.46628e+06 | -2.24521e+06 | True | False | 0 |

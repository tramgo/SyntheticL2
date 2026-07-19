# Phase89 Passive Queue-Capture Cost-Floor Experiment

Generated UTC: 2026-07-19T21:09:35.408488+00:00

Phase89 starts the post-pivot feature class from Phase88.
It evaluates hypothetical passive L1 queue-capture candidates with pessimistic, base and optimistic fill assumptions.
Entry selection uses only current-bar features; next-bar movement is used only for markout/adverse-selection evaluation.
Optimistic-only profitability is not accepted as a survivor.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase89_candidate_specs | 18 | Passive feature candidates evaluated |
| phase89_fill_assumption_rows | 54 | Candidate/fill-assumption rows evaluated |
| phase89_assumption_pass_rows | 0 | Candidate/fill rows passing train and test gates |
| phase89_all_assumption_survivor_candidates | 0 | Candidates passing pessimistic, base and optimistic fill assumptions |
| phase89_best_test_expected_net_pnl_inr | -187946 | Best test expected net P&L under any fill assumption |
| phase89_best_worst_case_test_expected_net_pnl_inr | -265254 | Best candidate worst-case test expected net P&L across assumptions |
| phase89_passive_queue_cost_floor_pass | 0 | 1 means a passive candidate clears the cost floor under all fill assumptions |
| phase89_recommend_next_action | retire_simple_passive_imbalance_or_design_richer_passive_features | Recommended next milestone |

## Candidate Survival Summary

| candidate_id | feature_name | assumptions_passed | all_fill_assumptions_pass | best_test_expected_net_pnl_inr | worst_test_expected_net_pnl_inr | max_test_adverse_selection_rate |
| --- | --- | --- | --- | --- | --- | --- |
| P89_L5_IMBALANCE_Q0_9_I0_75 | l5_imbalance |  | False | -187946 | -265254 | 0.51522 |
| P89_L1_IMBALANCE_Q0_9_I0_75 | l1_imbalance |  | False | -189428 | -269027 | 0.516816 |
| P89_L5_IMBALANCE_Q0_9_I0_5 | l5_imbalance |  | False | -298011 | -394715 | 0.507366 |
| P89_L1_IMBALANCE_Q0_9_I0_5 | l1_imbalance |  | False | -298513 | -395910 | 0.50824 |
| P89_MICROPRICE_DEV_Q0_9_I0_75 | microprice_dev |  | False | -333271 | -603564 | 0.540384 |
| P89_MICROPRICE_DEV_Q0_9_I0_5 | microprice_dev |  | False | -418659 | -692228 | 0.52189 |
| P89_L1_IMBALANCE_Q0_75_I0_75 | l1_imbalance |  | False | -502157 | -696599 | 0.502258 |
| P89_L5_IMBALANCE_Q0_75_I0_75 | l5_imbalance |  | False | -502933 | -699104 | 0.504091 |
| P89_L5_IMBALANCE_Q0_75_I0_5 | l5_imbalance |  | False | -811727 | -1.06528e+06 | 0.49842 |
| P89_L1_IMBALANCE_Q0_75_I0_5 | l1_imbalance |  | False | -811450 | -1.06528e+06 | 0.496671 |
| P89_MICROPRICE_DEV_Q0_75_I0_75 | microprice_dev |  | False | -686569 | -1.08008e+06 | 0.505514 |
| P89_MICROPRICE_DEV_Q0_75_I0_5 | microprice_dev |  | False | -932470 | -1.29823e+06 | 0.493463 |
| P89_L1_IMBALANCE_Q0_5_I0_75 | l1_imbalance |  | False | -1.014e+06 | -1.45694e+06 | 0.507049 |
| P89_L5_IMBALANCE_Q0_5_I0_75 | l5_imbalance |  | False | -1.01643e+06 | -1.45843e+06 | 0.506091 |
| P89_MICROPRICE_DEV_Q0_5_I0_75 | microprice_dev |  | False | -1.21921e+06 | -1.70985e+06 | 0.506163 |
| P89_L5_IMBALANCE_Q0_5_I0_5 | l5_imbalance |  | False | -1.66775e+06 | -2.21354e+06 | 0.499514 |
| P89_L1_IMBALANCE_Q0_5_I0_5 | l1_imbalance |  | False | -1.66851e+06 | -2.21453e+06 | 0.500715 |
| P89_MICROPRICE_DEV_Q0_5_I0_5 | microprice_dev |  | False | -1.84743e+06 | -2.46628e+06 | 0.5 |

## Fill Assumption Results

| candidate_id | feature_name | feature_column | direction_rule | feature_abs_quantile | feature_abs_threshold | event_intensity_quantile | event_intensity_threshold | base_fill_prob | adverse_multiplier | favorable_multiplier | shock_multiplier | max_fill_prob | fill_assumption | train_observations | train_expected_fills | train_symbols | train_months | train_expected_net_pnl_inr | train_adverse_selection_rate | train_positive_months | train_max_month_contribution_abs | test_observations | test_expected_fills | test_symbols | test_months | test_expected_net_pnl_inr | test_adverse_selection_rate | test_positive_months | test_max_month_contribution_abs | train_pass | test_pass | assumption_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P89_L5_IMBALANCE_Q0_9_I0_75 | l5_imbalance | avg_l5_imbalance | side = sign(avg_l5_imbalance) | 0.9 | 0.573847 | 0.75 | 145.1 | 0.12 | 2.5 | 0.25 | 0.65 | 0.35 | pessimistic_queue | 1685 | 210.638 | 5 | 6 | -176116 | 0.490208 | 0 | 0.244144 | 1774 | 240.207 | 5 | 6 | -187946 | 0.51522 | 0 | 0.241245 | False | False | False |
| P89_L1_IMBALANCE_Q0_9_I0_75 | l1_imbalance | avg_l1_imbalance | side = sign(avg_l1_imbalance) | 0.9 | 0.573921 | 0.75 | 145.1 | 0.12 | 2.5 | 0.25 | 0.65 | 0.35 | pessimistic_queue | 1691 | 211.281 | 5 | 6 | -177899 | 0.490242 | 0 | 0.241698 | 1784 | 242.237 | 5 | 6 | -189428 | 0.516816 | 0 | 0.241961 | False | False | False |
| P89_L5_IMBALANCE_Q0_9_I0_75 | l5_imbalance | avg_l5_imbalance | side = sign(avg_l5_imbalance) | 0.9 | 0.573847 | 0.75 | 145.1 | 0.25 | 1.75 | 0.5 | 0.8 | 0.6 | base_queue | 1685 | 407.363 | 5 | 6 | -243099 | 0.490208 | 0 | 0.246415 | 1774 | 450.05 | 5 | 6 | -261152 | 0.51522 | 0 | 0.239748 | False | False | False |
| P89_L1_IMBALANCE_Q0_9_I0_75 | l1_imbalance | avg_l1_imbalance | side = sign(avg_l1_imbalance) | 0.9 | 0.573921 | 0.75 | 145.1 | 0.25 | 1.75 | 0.5 | 0.8 | 0.6 | base_queue | 1691 | 408.713 | 5 | 6 | -246718 | 0.490242 | 0 | 0.2428 | 1784 | 453.425 | 5 | 6 | -263621 | 0.516816 | 0 | 0.240612 | False | False | False |
| P89_L5_IMBALANCE_Q0_9_I0_75 | l5_imbalance | avg_l5_imbalance | side = sign(avg_l5_imbalance) | 0.9 | 0.573847 | 0.75 | 145.1 | 0.45 | 1.25 | 0.75 | 1 | 0.85 | optimistic_queue | 1685 | 755.212 | 5 | 6 | -230149 | 0.490208 | 0 | 0.249022 | 1774 | 805.05 | 5 | 6 | -265254 | 0.51522 | 0 | 0.240249 | False | False | False |
| P89_L1_IMBALANCE_Q0_9_I0_75 | l1_imbalance | avg_l1_imbalance | side = sign(avg_l1_imbalance) | 0.9 | 0.573921 | 0.75 | 145.1 | 0.45 | 1.25 | 0.75 | 1 | 0.85 | optimistic_queue | 1691 | 757.913 | 5 | 6 | -237107 | 0.490242 | 0 | 0.241715 | 1784 | 810.225 | 5 | 6 | -269027 | 0.516816 | 0 | 0.241314 | False | False | False |
| P89_L5_IMBALANCE_Q0_9_I0_5 | l5_imbalance | avg_l5_imbalance | side = sign(avg_l5_imbalance) | 0.9 | 0.573847 | 0.5 | 126.3 | 0.12 | 2.5 | 0.25 | 0.65 | 0.35 | pessimistic_queue | 3502 | 494.45 | 5 | 6 | -305577 | 0.496288 | 0 | 0.242507 | 3394 | 502.382 | 5 | 6 | -298011 | 0.507366 | 0 | 0.243506 | False | False | False |
| P89_L1_IMBALANCE_Q0_9_I0_5 | l1_imbalance | avg_l1_imbalance | side = sign(avg_l1_imbalance) | 0.9 | 0.573921 | 0.5 | 126.3 | 0.12 | 2.5 | 0.25 | 0.65 | 0.35 | pessimistic_queue | 3503 | 494.673 | 5 | 6 | -307246 | 0.496717 | 0 | 0.24119 | 3398 | 503.421 | 5 | 6 | -298513 | 0.50824 | 0 | 0.244859 | False | False | False |
| P89_MICROPRICE_DEV_Q0_9_I0_75 | microprice_dev | avg_microprice_dev | side = sign(avg_microprice_dev) | 0.9 | 0.000100514 | 0.75 | 145.1 | 0.12 | 2.5 | 0.25 | 0.65 | 0.35 | pessimistic_queue | 2816 | 328.8 | 8 | 6 | -356162 | 0.507457 | 0 | 0.252157 | 2761 | 349.403 | 8 | 6 | -333271 | 0.540384 | 0 | 0.230236 | False | False | False |
| P89_L5_IMBALANCE_Q0_9_I0_5 | l5_imbalance | avg_l5_imbalance | side = sign(avg_l5_imbalance) | 0.9 | 0.573847 | 0.5 | 126.3 | 0.45 | 1.25 | 0.75 | 1 | 0.85 | optimistic_queue | 3502 | 1574.21 | 5 | 6 | -392511 | 0.496288 | 0 | 0.263958 | 3394 | 1534.05 | 5 | 6 | -377009 | 0.507366 | 0 | 0.250804 | False | False | False |
| P89_L1_IMBALANCE_Q0_9_I0_5 | l1_imbalance | avg_l1_imbalance | side = sign(avg_l1_imbalance) | 0.9 | 0.573921 | 0.5 | 126.3 | 0.45 | 1.25 | 0.75 | 1 | 0.85 | optimistic_queue | 3503 | 1575 | 5 | 6 | -399297 | 0.496717 | 0 | 0.259472 | 3398 | 1536.53 | 5 | 6 | -379480 | 0.50824 | 0 | 0.253298 | False | False | False |
| P89_L5_IMBALANCE_Q0_9_I0_5 | l5_imbalance | avg_l5_imbalance | side = sign(avg_l5_imbalance) | 0.9 | 0.573847 | 0.5 | 126.3 | 0.25 | 1.75 | 0.5 | 0.8 | 0.6 | base_queue | 3502 | 903.35 | 5 | 6 | -410376 | 0.496288 | 0 | 0.249343 | 3394 | 900.925 | 5 | 6 | -394715 | 0.507366 | 0 | 0.244415 | False | False | False |
| P89_L1_IMBALANCE_Q0_9_I0_5 | l1_imbalance | avg_l1_imbalance | side = sign(avg_l1_imbalance) | 0.9 | 0.573921 | 0.5 | 126.3 | 0.25 | 1.75 | 0.5 | 0.8 | 0.6 | base_queue | 3503 | 903.763 | 5 | 6 | -413842 | 0.496717 | 0 | 0.247254 | 3398 | 902.612 | 5 | 6 | -395910 | 0.50824 | 0 | 0.246097 | False | False | False |
| P89_MICROPRICE_DEV_Q0_9_I0_5 | microprice_dev | avg_microprice_dev | side = sign(avg_microprice_dev) | 0.9 | 0.000100514 | 0.5 | 126.3 | 0.12 | 2.5 | 0.25 | 0.65 | 0.35 | pessimistic_queue | 4415 | 556.323 | 8 | 6 | -468007 | 0.500113 | 0 | 0.241636 | 4043 | 545.727 | 8 | 6 | -418659 | 0.52189 | 0 | 0.222777 | False | False | False |
| P89_L1_IMBALANCE_Q0_75_I0_75 | l1_imbalance | avg_l1_imbalance | side = sign(avg_l1_imbalance) | 0.75 | 0.414016 | 0.75 | 145.1 | 0.12 | 2.5 | 0.25 | 0.65 | 0.35 | pessimistic_queue | 4319 | 552.617 | 9 | 6 | -491863 | 0.497569 | 0 | 0.244017 | 4651 | 620.892 | 9 | 6 | -502157 | 0.502258 | 0 | 0.244636 | False | False | False |
| P89_L5_IMBALANCE_Q0_75_I0_75 | l5_imbalance | avg_l5_imbalance | side = sign(avg_l5_imbalance) | 0.75 | 0.414928 | 0.75 | 145.1 | 0.12 | 2.5 | 0.25 | 0.65 | 0.35 | pessimistic_queue | 4289 | 547.713 | 9 | 6 | -487511 | 0.496386 | 0 | 0.242063 | 4644 | 621.864 | 9 | 6 | -502933 | 0.504091 | 0 | 0.243832 | False | False | False |
| P89_MICROPRICE_DEV_Q0_9_I0_75 | microprice_dev | avg_microprice_dev | side = sign(avg_microprice_dev) | 0.9 | 0.000100514 | 0.75 | 145.1 | 0.25 | 1.75 | 0.5 | 0.8 | 0.6 | base_queue | 2816 | 661.813 | 8 | 6 | -543563 | 0.507457 | 0 | 0.282479 | 2761 | 682.075 | 8 | 6 | -507229 | 0.540384 | 0 | 0.233147 | False | False | False |
| P89_MICROPRICE_DEV_Q0_9_I0_75 | microprice_dev | avg_microprice_dev | side = sign(avg_microprice_dev) | 0.9 | 0.000100514 | 0.75 | 145.1 | 0.45 | 1.25 | 0.75 | 1 | 0.85 | optimistic_queue | 2816 | 1273.28 | 8 | 6 | -638045 | 0.507457 | 0 | 0.357538 | 2761 | 1269.34 | 8 | 6 | -603564 | 0.540384 | 0 | 0.233145 | False | False | False |
| P89_MICROPRICE_DEV_Q0_9_I0_5 | microprice_dev | avg_microprice_dev | side = sign(avg_microprice_dev) | 0.9 | 0.000100514 | 0.5 | 126.3 | 0.25 | 1.75 | 0.5 | 0.8 | 0.6 | base_queue | 4415 | 1074.72 | 8 | 6 | -694183 | 0.500113 | 0 | 0.257608 | 4043 | 1026.84 | 8 | 6 | -611954 | 0.52189 | 0 | 0.215841 | False | False | False |
| P89_MICROPRICE_DEV_Q0_75_I0_75 | microprice_dev | avg_microprice_dev | side = sign(avg_microprice_dev) | 0.75 | 5.20477e-05 | 0.75 | 145.1 | 0.12 | 2.5 | 0.25 | 0.65 | 0.35 | pessimistic_queue | 5985 | 717.347 | 16 | 6 | -734404 | 0.507602 | 0 | 0.248509 | 6166 | 761.292 | 16 | 6 | -686569 | 0.505514 | 0 | 0.225731 | False | False | False |
| P89_MICROPRICE_DEV_Q0_9_I0_5 | microprice_dev | avg_microprice_dev | side = sign(avg_microprice_dev) | 0.9 | 0.000100514 | 0.5 | 126.3 | 0.45 | 1.25 | 0.75 | 1 | 0.85 | optimistic_queue | 4415 | 1988.77 | 8 | 6 | -792245 | 0.500113 | 0 | 0.322128 | 4043 | 1841.51 | 8 | 6 | -692228 | 0.52189 | 0 | 0.221936 | False | False | False |
| P89_L1_IMBALANCE_Q0_75_I0_75 | l1_imbalance | avg_l1_imbalance | side = sign(avg_l1_imbalance) | 0.75 | 0.414016 | 0.75 | 145.1 | 0.25 | 1.75 | 0.5 | 0.8 | 0.6 | base_queue | 4319 | 1058.95 | 9 | 6 | -697524 | 0.497569 | 0 | 0.244686 | 4651 | 1169.08 | 9 | 6 | -693072 | 0.502258 | 0 | 0.245721 | False | False | False |
| P89_L5_IMBALANCE_Q0_75_I0_75 | l5_imbalance | avg_l5_imbalance | side = sign(avg_l5_imbalance) | 0.75 | 0.414928 | 0.75 | 145.1 | 0.25 | 1.75 | 0.5 | 0.8 | 0.6 | base_queue | 4289 | 1050.16 | 9 | 6 | -690583 | 0.496386 | 0 | 0.242986 | 4644 | 1169.53 | 9 | 6 | -694637 | 0.504091 | 0 | 0.244623 | False | False | False |
| P89_L1_IMBALANCE_Q0_75_I0_75 | l1_imbalance | avg_l1_imbalance | side = sign(avg_l1_imbalance) | 0.75 | 0.414016 | 0.75 | 145.1 | 0.45 | 1.25 | 0.75 | 1 | 0.85 | optimistic_queue | 4319 | 1942.99 | 9 | 6 | -725730 | 0.497569 | 0 | 0.25722 | 4651 | 2097.56 | 9 | 6 | -696599 | 0.502258 | 0 | 0.25328 | False | False | False |
| P89_L5_IMBALANCE_Q0_75_I0_75 | l5_imbalance | avg_l5_imbalance | side = sign(avg_l5_imbalance) | 0.75 | 0.414928 | 0.75 | 145.1 | 0.45 | 1.25 | 0.75 | 1 | 0.85 | optimistic_queue | 4289 | 1928.36 | 9 | 6 | -715531 | 0.496386 | 0 | 0.260886 | 4644 | 2096.32 | 9 | 6 | -699104 | 0.504091 | 0 | 0.25152 | False | False | False |
| P89_L1_IMBALANCE_Q0_75_I0_5 | l1_imbalance | avg_l1_imbalance | side = sign(avg_l1_imbalance) | 0.75 | 0.414016 | 0.5 | 126.3 | 0.12 | 2.5 | 0.25 | 0.65 | 0.35 | pessimistic_queue | 8998 | 1290.18 | 9 | 6 | -853126 | 0.499778 | 0 | 0.245056 | 8861 | 1297.74 | 9 | 6 | -811450 | 0.496671 | 0 | 0.257808 | False | False | False |
| P89_L5_IMBALANCE_Q0_75_I0_5 | l5_imbalance | avg_l5_imbalance | side = sign(avg_l5_imbalance) | 0.75 | 0.414928 | 0.5 | 126.3 | 0.12 | 2.5 | 0.25 | 0.65 | 0.35 | pessimistic_queue | 9001 | 1291.69 | 9 | 6 | -848037 | 0.499611 | 0 | 0.242416 | 8862 | 1302.23 | 9 | 6 | -811727 | 0.49842 | 0 | 0.258769 | False | False | False |
| P89_MICROPRICE_DEV_Q0_75_I0_5 | microprice_dev | avg_microprice_dev | side = sign(avg_microprice_dev) | 0.75 | 5.20477e-05 | 0.5 | 126.3 | 0.12 | 2.5 | 0.25 | 0.65 | 0.35 | pessimistic_queue | 10468 | 1387.45 | 16 | 6 | -1.05926e+06 | 0.501528 | 0 | 0.261575 | 9867 | 1332.82 | 16 | 6 | -932470 | 0.493463 | 0 | 0.236151 | False | False | False |
| P89_MICROPRICE_DEV_Q0_75_I0_75 | microprice_dev | avg_microprice_dev | side = sign(avg_microprice_dev) | 0.75 | 5.20477e-05 | 0.75 | 145.1 | 0.25 | 1.75 | 0.5 | 0.8 | 0.6 | base_queue | 5985 | 1425.33 | 16 | 6 | -1.08641e+06 | 0.507602 | 0 | 0.247515 | 6166 | 1490.85 | 16 | 6 | -998433 | 0.505514 | 0 | 0.225163 | False | False | False |
| P89_L5_IMBALANCE_Q0_75_I0_5 | l5_imbalance | avg_l5_imbalance | side = sign(avg_l5_imbalance) | 0.75 | 0.414928 | 0.5 | 126.3 | 0.45 | 1.25 | 0.75 | 1 | 0.85 | optimistic_queue | 9001 | 4053.38 | 9 | 6 | -1.14633e+06 | 0.499611 | 0 | 0.259053 | 8862 | 3989.7 | 9 | 6 | -999657 | 0.49842 | 0 | 0.274574 | False | False | False |

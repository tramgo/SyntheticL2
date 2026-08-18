# Phase474 Larger-Horizon Fewer-Trade Source-Event L1-L5 Experiment

Phase474 tests the Phase473 next path: larger forecast horizons and fewer top-confidence trades while retaining full-depth L1-L5 features, Zerodha cost200, and fixed-capital annualization.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase474_larger_horizon_fewer_trade_experiment_complete | 1 | Phase474 experiment completed |
| phase474_thesis_id | P474_LARGER_HORIZON_FEWER_TRADE_SOURCE_EVENT_L1_L5 | Experiment thesis |
| phase474_best_scenario_id | horizon_1800_top_0.05_cost200 | Best scenario |
| phase474_best_horizon_ticks | 1800 | Best horizon |
| phase474_best_top_fraction | 0.05 | Best top confidence fraction |
| phase474_best_trade_count | 31 | Best trade count |
| phase474_best_net_pnl_inr | -1464.1 | Best net P&L |
| phase474_best_annualized_return_pct | -16.7706 | Best fixed-capital annualized return |
| phase474_positive_net_scenario_rows | 0 | Positive net scenarios |
| phase474_above12_annualized_scenario_rows | 0 | Scenarios above 12% annualized |
| phase474_fixed_capital_inr | 100000 | Reusable capital denominator |
| phase474_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model version |
| phase474_zerodha_cost_source_url | https://zerodha.com/charges/ | Cost source |
| phase474_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase474_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase474_phase475_allowed_next | 0 | Allows expansion only if all gates pass |
| phase474_hard_gate_pass_rows | 10 | Passed hard gates |
| phase474_hard_gate_rows | 12 | Hard gates |
| phase474_next_best_action | interpret_phase474_larger_horizon_failure_or_precommit_catalyst_conditioned_subset | Recommended next action |

## Matrix Summary

| horizon_ticks | matrix_rows | train_rows | holdout_rows | move_candidate_rows | l2_l5_feature_count | source_event_feature_count | long_rows | short_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 480 | 1792 | 1176 | 616 | 1134 | 10 | 11 | 902 | 876 |
| 960 | 1792 | 1176 | 616 | 1242 | 10 | 11 | 862 | 924 |
| 1800 | 1792 | 1176 | 616 | 1311 | 10 | 11 | 812 | 973 |

## Model Summary

| horizon_ticks | model_id | train_rows | holdout_rows | rows | positive_rate | auc | accuracy | balanced_accuracy | log_loss | tp | tn | fp | fn | primary_training_loss_path | shuffled_training_loss_path |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 480 | P474_PRIMARY_DIRECTION_LOGISTIC | 1168 | 610 | 610 | 0.496721 | 0.563023 | 0.552459 | 0.55258 | 0.690192 | 173 | 164 | 143 | 130 | 0.693396;0.674824;0.672656;0.672571;0.672560 | 0.692375;0.686737;0.686243;0.686197;0.686191 |
| 480 | P474_SHUFFLED_LABEL_CONTROL | 1168 | 610 | 610 | 0.496721 | 0.501113 | 0.485246 | 0.48531 | 0.694609 | 150 | 146 | 161 | 153 | 0.693396;0.674824;0.672656;0.672571;0.672560 | 0.692375;0.686737;0.686243;0.686197;0.686191 |
| 960 | P474_PRIMARY_DIRECTION_LOGISTIC | 1170 | 616 | 616 | 0.501623 | 0.549624 | 0.519481 | 0.519423 | 0.692749 | 166 | 154 | 153 | 143 | 0.693323;0.660964;0.657351;0.657252;0.657243 | 0.692766;0.682106;0.679163;0.678941;0.678916 |
| 960 | P474_SHUFFLED_LABEL_CONTROL | 1170 | 616 | 616 | 0.501623 | 0.524662 | 0.50974 | 0.509893 | 0.692566 | 143 | 171 | 136 | 166 | 0.693323;0.660964;0.657351;0.657252;0.657243 | 0.692766;0.682106;0.679163;0.678941;0.678916 |
| 1800 | P474_PRIMARY_DIRECTION_LOGISTIC | 1170 | 615 | 615 | 0.461789 | 0.530148 | 0.517073 | 0.514611 | 0.691054 | 137 | 181 | 150 | 147 | 0.693812;0.663288;0.659976;0.659902;0.659897 | 0.693705;0.684035;0.682693;0.682600;0.682587 |
| 1800 | P474_SHUFFLED_LABEL_CONTROL | 1170 | 615 | 615 | 0.461789 | 0.487298 | 0.491057 | 0.492442 | 0.707203 | 145 | 157 | 174 | 139 | 0.693812;0.663288;0.659976;0.659902;0.659897 | 0.693705;0.684035;0.682693;0.682600;0.682587 |

## Scenario Summary

| scenario_id | horizon_ticks | top_fraction | trade_count | holdout_days | gross_pnl_inr | zerodha_total_charges_inr | adverse_slippage_inr | net_pnl_inr | annualized_return_pct | win_rate | avg_net_per_trade_inr | max_daily_drawdown_inr | primary_auc | shuffled_auc | auc_lift_vs_shuffled |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| horizon_480_top_0.05_cost200 | 480 | 0.05 | 30 | 22 | 505.927 | 2477.34 | 596.004 | -2567.42 | -29.4086 | 0.1 | -85.5806 | -2425.82 | 0.563023 | 0.501113 | 0.0619108 |
| horizon_480_top_0.10_cost200 | 480 | 0.1 | 61 | 22 | 465.639 | 5036.92 | 1211.2 | -5782.47 | -66.2356 | 0.0491803 | -94.7946 | -5361.67 | 0.563023 | 0.501113 | 0.0619108 |
| horizon_480_top_0.20_cost200 | 480 | 0.2 | 122 | 22 | 666.072 | 10071.4 | 2421.58 | -11826.9 | -135.472 | 0.0409836 | -96.9419 | -11529.6 | 0.563023 | 0.501113 | 0.0619108 |
| horizon_960_top_0.05_cost200 | 960 | 0.05 | 31 | 22 | 709.223 | 2561.3 | 616.511 | -2468.59 | -28.2766 | 0.0967742 | -79.6319 | -1896.08 | 0.549624 | 0.524662 | 0.0249623 |
| horizon_960_top_0.10_cost200 | 960 | 0.1 | 62 | 22 | 918.126 | 5121.78 | 1231.55 | -5435.21 | -62.2578 | 0.0645161 | -87.6646 | -5394.68 | 0.549624 | 0.524662 | 0.0249623 |
| horizon_960_top_0.20_cost200 | 960 | 0.2 | 123 | 22 | 2244.07 | 10156.3 | 2441.97 | -10354.2 | -118.603 | 0.0813008 | -84.1805 | -10197 | 0.549624 | 0.524662 | 0.0249623 |
| horizon_1800_top_0.05_cost200 | 1800 | 0.05 | 31 | 22 | 1713.31 | 2561.18 | 616.234 | -1464.1 | -16.7706 | 0.258065 | -47.2291 | -1351.02 | 0.530148 | 0.487298 | 0.0428492 |
| horizon_1800_top_0.10_cost200 | 1800 | 0.1 | 62 | 22 | 2102.64 | 5119.97 | 1231.76 | -4249.1 | -48.6715 | 0.209677 | -68.5338 | -3877.34 | 0.530148 | 0.487298 | 0.0428492 |
| horizon_1800_top_0.20_cost200 | 1800 | 0.2 | 123 | 22 | 3433.24 | 10155.4 | 2442.05 | -9164.2 | -104.972 | 0.162602 | -74.5057 | -9121.22 | 0.530148 | 0.487298 | 0.0428492 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P474_PHASE473_PRECOMMIT_USED | True | 1 | 1 | hard |
| P474_LARGER_HORIZONS_USED | True | 480;960;1800 | 480;960;1800 | hard |
| P474_MATRIX_ROWS_PRESENT_ALL_HORIZONS | True | 3 | 3 | hard |
| P474_FULL_DEPTH_FEATURES_USED | True | 10 | >=10 | hard |
| P474_FEWER_TRADE_SCENARIOS_USED | True | 0.05;0.1;0.2 | 0.05;0.10;0.20 | hard |
| P474_COST200_INCLUDED | True | 2 | 2 | hard |
| P474_FIXED_CAPITAL_USED | True | 100000 | 100000 | hard |
| P474_ALL_MODELS_HAVE_POSITIVE_AUC_LIFT | True | checked | all>0 | hard |
| P474_POSITIVE_NET_SCENARIO_EXISTS | False | 0 | >0 | hard |
| P474_ABOVE_12PCT_ANNUALIZED_SCENARIO_EXISTS | False | 0 | >0 | hard |
| P474_BEST_TRADE_COUNT_GE_10 | True | 31 | >=10 | hard |
| P474_NO_PAPER_LIVE_OR_CLAIM | True | synthetic_replay_only;paper=0;live=0 | no_paper_live | hard |

Boundary: Phase474 is synthetic-only replay evidence. It is not paper/live acceptance and not a deployable profitability claim.

# Phase124 Non-Trading Filter Baselines

Generated UTC: 2026-07-19T23:32:16.468067+00:00

Phase124 evaluates transparent non-trading baselines for Phase123 filter labels.
The outputs are calibration diagnostics only; no buy/sell side, order model, P&L replay or strategy promotion is emitted.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase124_model_result_rows | 82 | Baseline model rows evaluated |
| phase124_label_selection_rows | 2 | Labels with model selection rows |
| phase124_selected_filter_models | 2 | Non-trading filter models materially improving over train-prior baseline |
| phase124_gate_rows | 4 | Gates evaluated |
| phase124_all_gates_pass | 1 | 1 means all Phase124 gates pass |
| phase124_filter_integration_allowed_next | 2 | 1+ means selected non-trading filter(s) can be prepared for integration as abstention/diagnostic layers |
| phase124_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase124_next_best_action | prepare_phase125_filter_integration_contract_if_selected_models_exist | Recommended next milestone |
| phase124_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model retained for future filter validation |

## Model Selection

| label | selected_model_id | prior_brier | best_brier | brier_improvement | holdout_log_loss | holdout_accuracy | holdout_auc | model_selected | selection_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| regime_realism_risk_label | threshold_feed_imperfection_rate_ge_0.023808 | 0.205729 | 0.078125 | 0.127604 | 0.322014 | 0.96875 | 0.978873 | True | beats_prior_brier_by_minimum_margin |
| opportunity_abstention_label | threshold_mean_l1_depth_le_783.05498 | 0.248698 | 0.169271 | 0.0794271 | 0.522282 | 0.786458 | 0.783408 | True | beats_prior_brier_by_minimum_margin |

## Gate Evaluation

| gate_id | gate_pass | evidence |
| --- | --- | --- |
| P124_NON_TRADING_ONLY | 1 | All model outputs are label probabilities/screeners; strategy_replay_allowed remains 0. |
| P124_BASELINE_FIT_EXISTS | 1 | selection_rows=2 |
| P124_MATERIAL_CALIBRATION_IMPROVEMENT | 1 | selected_models=2 |
| P124_REPLAY_LOCK | 1 | No buy/sell signal or replay artifact emitted. |

## Top Model Results

| label | model_id | train_rows | holdout_rows | train_positive_rate | holdout_positive_rate | holdout_brier | holdout_log_loss | holdout_accuracy | holdout_auc | strategy_replay_allowed | feature | direction | threshold | train_prediction_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| opportunity_abstention_label | threshold_mean_l1_depth_le_783.05498 | 192 | 192 | 0.53125 | 0.536458 | 0.169271 | 0.522282 | 0.786458 | 0.783408 | 0 | mean_l1_depth | le | 783.055 | 0.25 |
| opportunity_abstention_label | threshold_mean_l5_depth_le_6655.8146 | 192 | 192 | 0.53125 | 0.536458 | 0.169271 | 0.522282 | 0.786458 | 0.783408 | 0 | mean_l5_depth | le | 6655.81 | 0.25 |
| opportunity_abstention_label | threshold_one_tick_return_std_le_4.854937e-05 | 192 | 192 | 0.53125 | 0.536458 | 0.174479 | 0.533725 | 0.776042 | 0.785917 | 0 | one_tick_return_std | le | 4.85494e-05 | 0.25 |
| opportunity_abstention_label | threshold_mean_l1_depth_le_790.99238 | 192 | 192 | 0.53125 | 0.536458 | 0.190104 | 0.568057 | 0.744792 | 0.730064 | 0 | mean_l1_depth | le | 790.992 | 0.5 |
| opportunity_abstention_label | threshold_mean_l5_depth_le_6723.3559 | 192 | 192 | 0.53125 | 0.536458 | 0.190104 | 0.568057 | 0.744792 | 0.730064 | 0 | mean_l5_depth | le | 6723.36 | 0.5 |
| opportunity_abstention_label | threshold_one_tick_return_std_le_6.6043103e-05 | 192 | 192 | 0.53125 | 0.536458 | 0.231771 | 0.659608 | 0.661458 | 0.646286 | 0 | one_tick_return_std | le | 6.60431e-05 | 0.5 |
| opportunity_abstention_label | train_prior_probability | 192 | 192 | 0.53125 | 0.536458 | 0.248698 | 0.690541 | 0.536458 | 0.5 | 0 |  |  |  | 0.53125 |
| opportunity_abstention_label | threshold_median_spread_bps_ge_2.2255695 | 192 | 192 | 0.53125 | 0.536458 | 0.255208 | 0.711106 | 0.614583 | 0.62245 | 0 | median_spread_bps | ge | 2.22557 | 0.5 |
| opportunity_abstention_label | threshold_p90_spread_bps_ge_2.2471652 | 192 | 192 | 0.53125 | 0.536458 | 0.257812 | 0.716827 | 0.609375 | 0.617596 | 0 | p90_spread_bps | ge | 2.24717 | 0.5 |
| opportunity_abstention_label | threshold_median_spread_bps_ge_3.0885691 | 192 | 192 | 0.53125 | 0.536458 | 0.265625 | 0.733993 | 0.59375 | 0.621359 | 0 | median_spread_bps | ge | 3.08857 | 0.25 |
| opportunity_abstention_label | threshold_mean_l1_depth_le_797.22646 | 192 | 192 | 0.53125 | 0.536458 | 0.268229 | 0.739715 | 0.588542 | 0.556943 | 0 | mean_l1_depth | le | 797.226 | 0.75 |
| opportunity_abstention_label | threshold_mean_l5_depth_le_6776.4785 | 192 | 192 | 0.53125 | 0.536458 | 0.268229 | 0.739715 | 0.588542 | 0.556943 | 0 | mean_l5_depth | le | 6776.48 | 0.75 |
| opportunity_abstention_label | threshold_p90_spread_bps_ge_3.1109058 | 192 | 192 | 0.53125 | 0.536458 | 0.270833 | 0.745437 | 0.583333 | 0.61165 | 0 | p90_spread_bps | ge | 3.11091 | 0.25 |
| opportunity_abstention_label | threshold_feed_imperfection_rate_le_0.023808 | 192 | 192 | 0.53125 | 0.536458 | 0.276042 | 0.756881 | 0.572917 | 0.547726 | 0 | feed_imperfection_rate | le | 0.023808 | 0.817708 |
| opportunity_abstention_label | threshold_feed_imperfection_rate_le_0.015872 | 192 | 192 | 0.53125 | 0.536458 | 0.278646 | 0.762603 | 0.567708 | 0.552798 | 0 | feed_imperfection_rate | le | 0.015872 | 0.661458 |
| opportunity_abstention_label | threshold_median_spread_bps_ge_1.5946701 | 192 | 192 | 0.53125 | 0.536458 | 0.28125 | 0.768325 | 0.5625 | 0.547944 | 0 | median_spread_bps | ge | 1.59467 | 0.75 |
| opportunity_abstention_label | threshold_p90_spread_bps_ge_1.6122126 | 192 | 192 | 0.53125 | 0.536458 | 0.283854 | 0.774047 | 0.557292 | 0.543089 | 0 | p90_spread_bps | ge | 1.61221 | 0.75 |
| opportunity_abstention_label | threshold_passive_min_adverse_rate_ge_0 | 192 | 192 | 0.53125 | 0.536458 | 0.294271 | 0.796935 | 0.536458 | 0.5 | 0 | passive_min_adverse_rate | ge | 0 | 1 |
| opportunity_abstention_label | threshold_feed_imperfection_rate_le_0.007936 | 192 | 192 | 0.53125 | 0.536458 | 0.296875 | 0.802657 | 0.53125 | 0.535617 | 0 | feed_imperfection_rate | le | 0.007936 | 0.390625 |
| opportunity_abstention_label | threshold_one_tick_return_std_le_9.3644324e-05 | 192 | 192 | 0.53125 | 0.536458 | 0.296875 | 0.802657 | 0.53125 | 0.4982 | 0 | one_tick_return_std | le | 9.36443e-05 | 0.75 |
| opportunity_abstention_label | threshold_passive_min_adverse_rate_le_0.99170003 | 192 | 192 | 0.53125 | 0.536458 | 0.299479 | 0.808379 | 0.526042 | 0.507854 | 0 | passive_min_adverse_rate | le | 0.9917 | 0.75 |
| opportunity_abstention_label | threshold_feed_imperfection_rate_ge_0.007936 | 192 | 192 | 0.53125 | 0.536458 | 0.309896 | 0.831266 | 0.505208 | 0.476983 | 0 | feed_imperfection_rate | ge | 0.007936 | 0.864583 |
| opportunity_abstention_label | threshold_passive_min_adverse_rate_ge_0.99170003 | 192 | 192 | 0.53125 | 0.536458 | 0.325521 | 0.865598 | 0.473958 | 0.492146 | 0 | passive_min_adverse_rate | ge | 0.9917 | 0.25 |
| opportunity_abstention_label | threshold_passive_min_adverse_rate_le_0 | 192 | 192 | 0.53125 | 0.536458 | 0.325521 | 0.865598 | 0.473958 | 0.466947 | 0 | passive_min_adverse_rate | le | 0 | 0.59375 |
| opportunity_abstention_label | threshold_one_tick_return_std_ge_9.3644324e-05 | 192 | 192 | 0.53125 | 0.536458 | 0.328125 | 0.87132 | 0.46875 | 0.5018 | 0 | one_tick_return_std | ge | 9.36443e-05 | 0.25 |
| opportunity_abstention_label | threshold_feed_imperfection_rate_ge_0.015872 | 192 | 192 | 0.53125 | 0.536458 | 0.328125 | 0.87132 | 0.46875 | 0.464383 | 0 | feed_imperfection_rate | ge | 0.015872 | 0.609375 |
| opportunity_abstention_label | threshold_p90_spread_bps_le_1.6122126 | 192 | 192 | 0.53125 | 0.536458 | 0.341146 | 0.89993 | 0.442708 | 0.456911 | 0 | p90_spread_bps | le | 1.61221 | 0.25 |
| opportunity_abstention_label | threshold_median_spread_bps_le_1.5946701 | 192 | 192 | 0.53125 | 0.536458 | 0.34375 | 0.905651 | 0.4375 | 0.452056 | 0 | median_spread_bps | le | 1.59467 | 0.25 |
| opportunity_abstention_label | threshold_feed_imperfection_rate_ge_0.023808 | 192 | 192 | 0.53125 | 0.536458 | 0.346354 | 0.911373 | 0.432292 | 0.447202 | 0 | feed_imperfection_rate | ge | 0.023808 | 0.338542 |
| opportunity_abstention_label | threshold_p90_spread_bps_le_3.1109058 | 192 | 192 | 0.53125 | 0.536458 | 0.354167 | 0.928539 | 0.416667 | 0.38835 | 0 | p90_spread_bps | le | 3.11091 | 0.75 |

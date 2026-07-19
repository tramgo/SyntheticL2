# Phase123 Filter Label Matrix Builder

Generated UTC: 2026-07-19T23:29:37.617804+00:00

Phase123 builds the first no-replay label matrix for the Phase122 non-trading filters.
Rows are symbol/month partitions. Labels describe cost toxicity, synthetic realism risk and abstention opportunity, not trade direction.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase123_filter_label_rows | 384 | Filter label matrix rows |
| phase123_filter_label_symbols | 32 | Symbols covered by label matrix |
| phase123_filter_label_months | 12 | Months covered by label matrix |
| phase123_label_diagnostic_rows | 3 | Filter labels diagnosed |
| phase123_labels_with_class_variation | 2 | Labels suitable for future classifier fitting |
| phase123_gate_rows | 4 | Label matrix gates evaluated |
| phase123_all_gates_pass | 1 | 1 means label matrix passes all no-replay readiness gates |
| phase123_filter_model_fit_allowed_next | 1 | 1 means a future non-trading filter model fit may be attempted |
| phase123_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase123_next_best_action | fit_phase124_non_trading_filter_baselines_if_class_variation_present | Recommended next milestone |
| phase123_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model retained for future filter validation |

## Filter Label Diagnostics

| label | rows | positive_rows | positive_rate | symbols | months | train_rows | holdout_rows | has_class_variation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cost_toxicity_label | 384 | 384 | 1 | 32 | 12 | 192 | 192 | False |
| regime_realism_risk_label | 384 | 122 | 0.317708 | 32 | 12 | 192 | 192 | True |
| opportunity_abstention_label | 384 | 205 | 0.533854 | 32 | 12 | 192 | 192 | True |

## Baseline Diagnostics

| label | train_positive_rate | holdout_positive_rate | absolute_train_holdout_rate_gap | baseline_model | model_fit_allowed_next |
| --- | --- | --- | --- | --- | --- |
| cost_toxicity_label | 1 | 1 | 0 | train_prior_probability | False |
| regime_realism_risk_label | 0.375 | 0.260417 | 0.114583 | train_prior_probability | True |
| opportunity_abstention_label | 0.53125 | 0.536458 | 0.00520833 | train_prior_probability | True |

## Gate Evaluation

| gate_id | gate_pass | evidence |
| --- | --- | --- |
| P123_LABEL_MATRIX_EXISTS | 1 | rows=384 |
| P123_BREADTH | 1 | symbols=32; months=12 |
| P123_LABEL_VARIATION | 1 | labels_with_class_variation=2 |
| P123_NO_REPLAY | 1 | phase122_strategy_replay_allowed=0 |

## Filter Label Matrix Sample

| trade_month | trade_date | symbol | train_split | rows_scanned | regime_count | feed_profile_count | market_shock_rows | symbol_shock_rows | duplicate_rate | disconnect_gap_rate | out_of_order_rate | feed_imperfection_rate | median_spread_bps | p90_spread_bps | mean_l1_depth | mean_l5_depth | one_tick_return_std | passive_min_adverse_rate | passive_max_cost_clearing_rate | cost_toxicity_label | regime_realism_risk_label | opportunity_abstention_label | label_source | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | 2026-01-01 | ADANIPORTS | train | 250000 | 1 | 2 | 0 | 0 | 0.007936 | 0 | 0 | 0.007936 | 2.15994 | 2.1901 | 793.856 | 6747.8 | 0.00010176 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | AXISBANK | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1.47874 | 1.50602 | 794.301 | 6751.73 | 7.9916e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | BAJAJ-AUTO | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0.023808 | 0.023808 | 2.85823 | 2.90346 | 792.714 | 6738.09 | 9.29248e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | BANKBEES | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.015872 | 0.023808 | 3.45611 | 3.48224 | 784.619 | 6669.29 | 4.41933e-05 | 0.987179 | 0 | 1 | 1 | 1 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | BHARTIARTL | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0 | 0.007936 | 1.54631 | 1.56691 | 792.602 | 6736.89 | 5.25021e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | BPCL | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1.60077 | 1.62127 | 796.047 | 6766.4 | 7.89895e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | BRITANNIA | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 3.65464 | 3.70233 | 788.284 | 6700.62 | 6.52266e-05 | 0 | 0 | 1 | 0 | 1 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | CIPLA | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0.007936 | 0.007936 | 2.74348 | 2.78087 | 791.366 | 6726.51 | 7.64578e-05 | 1 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | DRREDDY | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0.015872 | 0.015872 | 2.38796 | 2.41255 | 787.78 | 6696.35 | 6.11781e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | GOLDBEES | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.015872 | 0.023808 | 0.840477 | 0.850268 | 783.255 | 6657.54 | 5.66937e-05 | 0 | 0 | 1 | 1 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | HCLTECH | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.015872 | 0.023808 | 2.40828 | 2.44618 | 796.462 | 6769.73 | 0.000116489 | 1 | 0 | 1 | 1 | 1 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | HDFCBANK | train | 250000 | 1 | 2 | 0 | 0 | 0.015872 | 0.015872 | 0.023808 | 0.055552 | 1.19239 | 1.21507 | 795.223 | 6759.47 | 9.86125e-05 | 0.975694 | 0 | 1 | 1 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | HINDUNILVR | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1.84111 | 1.86428 | 786.493 | 6685 | 7.00539e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | ICICIBANK | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1.3885 | 1.41473 | 794.921 | 6756.75 | 8.20483e-05 | 0.987179 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | INFY | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.007936 | 0.015872 | 1.77117 | 1.80148 | 797.143 | 6775.83 | 9.20345e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | ITBEES | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.007936 | 0.015872 | 3.08642 | 3.10366 | 782.476 | 6650.77 | 5.28633e-05 | 0.996034 | 0 | 1 | 0 | 1 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | ITC | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.007936 | 0.015872 | 1.75162 | 1.77022 | 785.651 | 6677.98 | 7.49469e-05 | 1 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | JUNIORBEES | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0.007936 | 0.007936 | 3.54677 | 3.58506 | 783.032 | 6655.68 | 6.32698e-05 | 0.986111 | 0 | 1 | 0 | 1 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | KOTAKBANK | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2.575 | 2.62467 | 795.762 | 6763.86 | 9.47069e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | LT | train | 250000 | 1 | 2 | 0 | 0 | 0.007936 | 0.007936 | 0 | 0.015872 | 1.24894 | 1.26557 | 791.827 | 6730.54 | 9.32361e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | M&M | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.031744 | 0.023808 | 0.055552 | 1.24054 | 1.2598 | 793.047 | 6740.84 | 0.000102897 | 0 | 0 | 1 | 1 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | MARUTI | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.007936 | 0.015872 | 2.84252 | 2.89331 | 793.095 | 6741.22 | 7.79683e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | NESTLEIND | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.007936 | 0.015872 | 2.73504 | 2.77085 | 787.619 | 6694.67 | 8.68305e-05 | 1 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | NIFTYBEES | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0 | 0.007936 | 1.42964 | 1.44587 | 783.063 | 6655.86 | 6.58799e-05 | 0.990991 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | ONGC | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1.97973 | 2.01159 | 796.981 | 6774.24 | 9.29665e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | RELIANCE | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0.015872 | 0.015872 | 1.5075 | 1.5294 | 796.618 | 6771.28 | 7.08266e-05 | 0.993827 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | SBIN | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0.007936 | 0.007936 | 1.87582 | 1.91644 | 795.682 | 6763.24 | 0.000103729 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | SUNPHARMA | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0.007936 | 0.007936 | 2.03863 | 2.06537 | 786.572 | 6685.8 | 8.00573e-05 | 1 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | TCS | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.007936 | 0.015872 | 1.798 | 1.82017 | 796.398 | 6769.17 | 7.69784e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | TECHM | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 3.24844 | 3.29663 | 796.492 | 6770.15 | 6.94144e-05 | 0 | 0 | 1 | 0 | 1 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | ULTRACEMCO | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.015872 | 0.023808 | 2.54151 | 2.5729 | 791.573 | 6728.3 | 9.40858e-05 | 1 | 0 | 1 | 1 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-01 | 2026-01-01 | WIPRO | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.015872 | 0.023808 | 2.19479 | 2.22841 | 795.096 | 6758.39 | 7.18543e-05 | 0 | 0 | 1 | 1 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-02 | 2026-02-02 | ADANIPORTS | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0.015872 | 0.015872 | 2.20325 | 2.21043 | 798.477 | 6786.93 | 6.68748e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-02 | 2026-02-02 | AXISBANK | train | 250000 | 1 | 2 | 0 | 0 | 0.015872 | 0 | 0.007936 | 0.023808 | 1.50761 | 1.514 | 797.584 | 6779.58 | 5.76769e-05 | 0 | 0 | 1 | 1 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-02 | 2026-02-02 | BAJAJ-AUTO | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.007936 | 0.015872 | 2.90135 | 2.91871 | 797.763 | 6780.88 | 8.60896e-05 | 0 | 0 | 1 | 0 | 1 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-02 | 2026-02-02 | BANKBEES | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0.015872 | 0.023808 | 3.49307 | 3.5021 | 785.428 | 6676.26 | 3.81787e-05 | 0.987179 | 0 | 1 | 1 | 1 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-02 | 2026-02-02 | BHARTIARTL | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.007936 | 0 | 0.007936 | 1.56063 | 1.57011 | 796.378 | 6769.08 | 6.87151e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-02 | 2026-02-02 | BPCL | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0 | 0.007936 | 0.007936 | 1.62153 | 1.63132 | 796.841 | 6773.37 | 6.18573e-05 | 0 | 0 | 1 | 0 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-02 | 2026-02-02 | BRITANNIA | train | 250000 | 1 | 2 | 0 | 0 | 0.007936 | 0 | 0.023808 | 0.031744 | 3.7303 | 3.74462 | 788.571 | 6702.73 | 6.70689e-05 | 0 | 0 | 1 | 1 | 1 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |
| 2026-02 | 2026-02-02 | CIPLA | train | 250000 | 1 | 2 | 0 | 0 | 0 | 0.015872 | 0.015872 | 0.031744 | 2.79408 | 2.80308 | 787.823 | 6696.4 | 5.58202e-05 | 1 | 0 | 1 | 1 | 0 | phase79_partition_profile_plus_phase120_stage02_passive_toxicity | 0 |

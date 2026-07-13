# Phase 16 Metrics and Reporting Report

Generated UTC: 2026-07-13T21:01:47.635619+00:00

## Scope

This phase creates a metrics catalog and current-evidence scoreboards for Phase 11 predictive diagnostics and Phase 12 trading proxies.
No metric is acceptance-grade yet; current values are proxy/reporting evidence only.

## Metric Catalog Summary

| metric_category | current_status | metrics |
| --- | --- | --- |
| predictive | computed_proxy | 1 |
| predictive | proxy_available | 1 |
| predictive | sample_proxy | 8 |
| trading | computed_proxy | 4 |
| trading | proxy_available | 2 |
| trading | sample_proxy | 11 |

## Top Predictive Proxy Rows

| strategy_id | name | support_level | rows_evaluated | signal_rows | signal_fraction | directional_accuracy_nonzero | directional_accuracy_status | mean_future_return_when_signaled | signed_mean_future_return | information_coefficient_proxy | promotion_allowed | acceptance_status | metric_scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S06 | Absorption and exhaustion reversal | partial_missing_required_features | 2259228 | 33993 | 0.0150463 | 0.505455 | proxy_threshold_not_met | 1.80845e-07 | 2.70872e-05 | 2.70872e-05 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S08 | Cross-ticker/index lead-lag OFI | partial_missing_required_features | 2259228 | 442644 | 0.195927 | 0.504006 | proxy_threshold_not_met | -6.47159e-05 | 4.8916e-06 | 4.8916e-06 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S07 | Mean reversion after imbalance | runnable_proxy | 2259228 | 234925 | 0.103985 | 0.501421 | proxy_threshold_not_met | -4.12098e-05 | 2.68998e-05 | 2.68998e-05 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S09 | Pure queue-imbalance scalping | runnable_proxy | 2259228 | 585341 | 0.259089 | 0.49772 | proxy_threshold_not_met | -1.41628e-05 | -1.41998e-05 | -1.41998e-05 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S05 | Microprice entry/exit filter | runnable_proxy | 2259228 | 445798 | 0.197323 | 0.497367 | proxy_threshold_not_met | -3.15943e-05 | -3.00993e-05 | -3.00993e-05 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S02 | Pure multi-level OFI directional model | runnable_proxy | 2259228 | 898620 | 0.397755 | 0.485755 | proxy_threshold_not_met | 9.57081e-07 | -0.00011217 | -0.00011217 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S04 | Trade-flow plus depth confirmation | partial_missing_required_features | 2259228 | 424887 | 0.188067 | 0.480829 | proxy_threshold_not_met | -3.58172e-05 | -0.000203103 | -0.000203103 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S03 | Liquidity-vacuum breakout | partial_missing_required_features | 2259228 | 280476 | 0.124147 | 0.467834 | proxy_threshold_not_met | -5.59924e-05 | -0.000691527 | -0.000691527 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S01 | Momentum/breakout filtered by MLOFI | runnable_proxy | 2259228 | 164253 | 0.0727032 | 0.434982 | proxy_threshold_not_met | 2.01051e-05 | -0.00108613 | -0.00108613 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S10 | Passive market making | not_supported_by_current_product | 2259228 | 0 | 0 |  | proxy_threshold_not_met |  |  |  | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |

## Predictive Confusion / Rank Proxy Rows

| strategy_id | rows_evaluated | nonzero_signal_rows | directional_eval_rows | true_long_rows | false_long_rows | true_short_rows | false_short_rows | precision_long_proxy | recall_long_proxy | precision_short_proxy | recall_short_proxy | balanced_accuracy_proxy | rank_auc_proxy | incremental_r2_proxy | mean_signed_future_return_proxy | metric_scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S06 | 2259228 | 34484 | 33550 | 8791 | 8055 | 8167 | 8537 | 0.521845 | 0.507329 | 0.488925 | 0.503452 | 0.505391 | 0.500194 | 8.67678e-07 | 2.70872e-05 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S08 | 2259228 | 451923 | 434894 | 107834 | 112027 | 111355 | 103678 | 0.490464 | 0.509825 | 0.517851 | 0.498496 | 0.50416 | 0.501374 | 3.75725e-07 | 4.8916e-06 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S07 | 2259228 | 238126 | 227966 | 44401 | 45298 | 69906 | 68361 | 0.495 | 0.393759 | 0.505587 | 0.606802 | 0.50028 | 0.50197 | 5.50787e-06 | 2.68998e-05 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S05 | 2259228 | 451850 | 431486 | 179180 | 181737 | 35427 | 35142 | 0.496458 | 0.836032 | 0.502019 | 0.163135 | 0.499583 | 0.496143 | 1.25584e-05 | -3.00993e-05 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S09 | 2259228 | 593224 | 569284 | 214136 | 217081 | 69208 | 68859 | 0.496585 | 0.756678 | 0.501264 | 0.241742 | 0.49921 | 0.496284 | 3.10769e-06 | -1.41998e-05 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S02 | 2259228 | 911843 | 877100 | 212943 | 226071 | 213113 | 224973 | 0.485048 | 0.486264 | 0.486464 | 0.485248 | 0.485756 | 0.491032 | 0.000393025 | -0.00011217 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S04 | 2259228 | 431959 | 420091 | 100809 | 107807 | 101183 | 110292 | 0.483228 | 0.477539 | 0.478463 | 0.484152 | 0.480846 | 0.493531 | 0.000609508 | -0.000203103 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S03 | 2259228 | 285321 | 277765 | 66710 | 75270 | 63238 | 72547 | 0.469855 | 0.479042 | 0.465722 | 0.456566 | 0.467804 | 0.492536 | 0.00466175 | -0.000691527 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S01 | 2259228 | 168100 | 161956 | 36415 | 45736 | 34033 | 45772 | 0.443269 | 0.443075 | 0.426452 | 0.426644 | 0.43486 | 0.490981 | 0.00673538 | -0.00108613 | phase11_ternary_signal_predictive_proxy_not_acceptance |

## Signal Bucket Future Returns

| strategy_id | signal_score_bucket | rows | mean_future_return | mean_signed_future_return | positive_future_fraction | metric_scope |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | flat_signal | 2064735 | -6.33134e-06 | 0 | 0.481732 | ternary_signal_bucket_not_true_decile |
| S01 | long_signal | 83226 | -0.00105194 | -0.00105194 | 0.427466 | ternary_signal_bucket_not_true_decile |
| S01 | short_signal | 81027 | 0.00112124 | -0.00112124 | 0.552055 | ternary_signal_bucket_not_true_decile |
| S02 | flat_signal | 1330368 | -7.99047e-06 | 0 | 0.483629 | ternary_signal_bucket_not_true_decile |
| S02 | long_signal | 449803 | -0.000111091 | -0.000111091 | 0.466783 | ternary_signal_bucket_not_true_decile |
| S02 | short_signal | 448817 | 0.000113251 | -0.000113251 | 0.493741 | ternary_signal_bucket_not_true_decile |
| S03 | flat_signal | 1948512 | 3.04557e-06 | 0 | 0.481427 | ternary_signal_bucket_not_true_decile |
| S03 | long_signal | 143347 | -0.000731307 | -0.000731307 | 0.458614 | ternary_signal_bucket_not_true_decile |
| S03 | short_signal | 137129 | 0.000649944 | -0.000649944 | 0.518708 | ternary_signal_bucket_not_true_decile |
| S04 | flat_signal | 1804101 | 3.01982e-06 | 0 | 0.480744 | ternary_signal_bucket_not_true_decile |
| S04 | long_signal | 210888 | -0.000240683 | -0.000240683 | 0.470297 | ternary_signal_bucket_not_true_decile |
| S04 | short_signal | 213999 | 0.00016607 | -0.00016607 | 0.50684 | ternary_signal_bucket_not_true_decile |
| S05 | flat_signal | 1783190 | 2.41952e-06 | 0 | 0.484253 | ternary_signal_bucket_not_true_decile |
| S05 | long_signal | 374840 | -3.66862e-05 | -3.66862e-05 | 0.471632 | ternary_signal_bucket_not_true_decile |
| S05 | short_signal | 70958 | -4.69625e-06 | 4.69625e-06 | 0.488524 | ternary_signal_bucket_not_true_decile |
| S06 | flat_signal | 2194995 | -4.45393e-06 | 0 | 0.481953 | ternary_signal_bucket_not_true_decile |
| S06 | long_signal | 17034 | 2.7208e-05 | 2.7208e-05 | 0.509151 | ternary_signal_bucket_not_true_decile |
| S06 | short_signal | 16959 | -2.69659e-05 | 2.69659e-05 | 0.495818 | ternary_signal_bucket_not_true_decile |
| S07 | flat_signal | 1994063 | -4.46368e-08 | 0 | 0.483295 | ternary_signal_bucket_not_true_decile |
| S07 | long_signal | 90611 | -1.85506e-05 | -1.85506e-05 | 0.483455 | ternary_signal_bucket_not_true_decile |
| S07 | short_signal | 144314 | -5.54369e-05 | 5.54369e-05 | 0.467314 | ternary_signal_bucket_not_true_decile |
| S08 | flat_signal | 1786344 | 1.05668e-05 | 0 | 0.485827 | ternary_signal_bucket_not_true_decile |
| S08 | long_signal | 223829 | -5.91543e-05 | -5.91543e-05 | 0.475155 | ternary_signal_bucket_not_true_decile |
| S08 | short_signal | 218815 | -7.0405e-05 | 7.0405e-05 | 0.460836 | ternary_signal_bucket_not_true_decile |
| S09 | flat_signal | 1643647 | -9.00523e-07 | 0 | 0.484125 | ternary_signal_bucket_not_true_decile |
| S09 | long_signal | 445895 | -1.86162e-05 | -1.86162e-05 | 0.473874 | ternary_signal_bucket_not_true_decile |
| S09 | short_signal | 139446 | 7.76e-08 | -7.76e-08 | 0.487187 | ternary_signal_bucket_not_true_decile |

## Brier Score Proxy

| strategy_id | rows_evaluated | brier_score_proxy | baseline_brier_score_proxy | brier_skill_score_proxy | mean_predicted_up_probability | observed_up_fraction | metric_scope |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S06 | 2228988 | 0.250571 | 0.249875 | -0.00278699 | 0.500007 | 0.488809 | ternary_signal_probability_proxy_not_calibrated_model |
| S07 | 2228988 | 0.253697 | 0.249875 | -0.0152963 | 0.495181 | 0.488809 | ternary_signal_probability_proxy_not_calibrated_model |
| S01 | 2228988 | 0.254824 | 0.249875 | -0.019807 | 0.500197 | 0.488809 | ternary_signal_probability_proxy_not_calibrated_model |
| S03 | 2228988 | 0.256639 | 0.249875 | -0.027069 | 0.500558 | 0.488809 | ternary_signal_probability_proxy_not_calibrated_model |
| S08 | 2228988 | 0.257647 | 0.249875 | -0.0311065 | 0.50045 | 0.488809 | ternary_signal_probability_proxy_not_calibrated_model |
| S04 | 2228988 | 0.259047 | 0.249875 | -0.0367088 | 0.499721 | 0.488809 | ternary_signal_probability_proxy_not_calibrated_model |
| S05 | 2228988 | 0.259418 | 0.249875 | -0.038193 | 0.527266 | 0.488809 | ternary_signal_probability_proxy_not_calibrated_model |
| S09 | 2228988 | 0.26193 | 0.249875 | -0.0482466 | 0.527497 | 0.488809 | ternary_signal_probability_proxy_not_calibrated_model |
| S02 | 2228988 | 0.268373 | 0.249875 | -0.0740315 | 0.500088 | 0.488809 | ternary_signal_probability_proxy_not_calibrated_model |

## Calibration Curve Proxy

| strategy_id | probability_bucket | rows | mean_predicted_up_probability | observed_up_fraction | calibration_error_abs | metric_scope |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | 0.0_0.2 | 0 |  |  |  | ternary_signal_probability_bucket_proxy_not_acceptance |
| S01 | 0.2_0.4 | 81027 | 0.3 | 0.564898 | 0.264898 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S01 | 0.4_0.6 | 2064735 | 0.5 | 0.48789 | 0.0121103 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S01 | 0.6_0.8 | 83226 | 0.7 | 0.437544 | 0.262456 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S01 | 0.8_1.0 | 0 |  |  |  | ternary_signal_probability_bucket_proxy_not_acceptance |
| S02 | 0.0_0.2 | 0 |  |  |  | ternary_signal_probability_bucket_proxy_not_acceptance |
| S02 | 0.2_0.4 | 448817 | 0.3 | 0.501258 | 0.201258 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S02 | 0.4_0.6 | 1330368 | 0.5 | 0.489815 | 0.0101852 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S02 | 0.6_0.8 | 449803 | 0.7 | 0.473414 | 0.226586 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S02 | 0.8_1.0 | 0 |  |  |  | ternary_signal_probability_bucket_proxy_not_acceptance |
| S03 | 0.0_0.2 | 0 |  |  |  | ternary_signal_probability_bucket_proxy_not_acceptance |
| S03 | 0.2_0.4 | 137129 | 0.3 | 0.529042 | 0.229042 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S03 | 0.4_0.6 | 1948512 | 0.5 | 0.487702 | 0.0122981 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S03 | 0.6_0.8 | 143347 | 0.7 | 0.465374 | 0.234626 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S03 | 0.8_1.0 | 0 |  |  |  | ternary_signal_probability_bucket_proxy_not_acceptance |
| S04 | 0.0_0.2 | 0 |  |  |  | ternary_signal_probability_bucket_proxy_not_acceptance |
| S04 | 0.2_0.4 | 213999 | 0.3 | 0.515386 | 0.215386 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S04 | 0.4_0.6 | 1804101 | 0.5 | 0.486918 | 0.0130821 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S04 | 0.6_0.8 | 210888 | 0.7 | 0.478022 | 0.221978 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S04 | 0.8_1.0 | 0 |  |  |  | ternary_signal_probability_bucket_proxy_not_acceptance |
| S05 | 0.0_0.2 | 0 |  |  |  | ternary_signal_probability_bucket_proxy_not_acceptance |
| S05 | 0.2_0.4 | 70958 | 0.3 | 0.495251 | 0.195251 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S05 | 0.4_0.6 | 1783190 | 0.5 | 0.490822 | 0.00917849 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S05 | 0.6_0.8 | 374840 | 0.7 | 0.478017 | 0.221983 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S05 | 0.8_1.0 | 0 |  |  |  | ternary_signal_probability_bucket_proxy_not_acceptance |
| S06 | 0.0_0.2 | 0 |  |  |  | ternary_signal_probability_bucket_proxy_not_acceptance |
| S06 | 0.2_0.4 | 16959 | 0.3 | 0.503391 | 0.203391 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S06 | 0.4_0.6 | 2194995 | 0.5 | 0.488485 | 0.0115151 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S06 | 0.6_0.8 | 17034 | 0.7 | 0.516085 | 0.183915 | ternary_signal_probability_bucket_proxy_not_acceptance |
| S06 | 0.8_1.0 | 0 |  |  |  | ternary_signal_probability_bucket_proxy_not_acceptance |

## Feature Importance Stability Proxy

| feature_name | seed_runs | mean_abs_correlation_importance | std_abs_correlation_importance | mean_rank | rank_std | top3_frequency | coefficient_of_variation | metric_scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| momentum_3 | 12 | 0.206438 | 0.0144364 | 1 | 0 | 1 | 0.0699311 | seed_sampled_feature_target_association_proxy_not_model_importance |
| local_volatility_6 | 12 | 0.0257675 | 0.013169 | 2.5 | 1.73205 | 0.916667 | 0.511072 | seed_sampled_feature_target_association_proxy_not_model_importance |
| event_intensity_proxy | 12 | 0.00865064 | 0.00528295 | 4.08333 | 1.72986 | 0.583333 | 0.6107 | seed_sampled_feature_target_association_proxy_not_model_importance |
| spread_ticks | 12 | 0.00644963 | 0.00446098 | 5.16667 | 2.12489 | 0.166667 | 0.691664 | seed_sampled_feature_target_association_proxy_not_model_importance |
| mlofi_qty | 12 | 0.00549189 | 0.00361176 | 5.25 | 1.95982 | 0.166667 | 0.657653 | seed_sampled_feature_target_association_proxy_not_model_importance |
| l5_imbalance | 12 | 0.00332507 | 0.00164805 | 5.75 | 1.65831 | 0.0833333 | 0.495645 | seed_sampled_feature_target_association_proxy_not_model_importance |
| l1_imbalance | 12 | 0.00319357 | 0.00163514 | 6.33333 | 1.49747 | 0.0833333 | 0.512011 | seed_sampled_feature_target_association_proxy_not_model_importance |
| book_slope_l5 | 12 | 0.00236288 | 0.00134205 | 6.83333 | 1.6967 | 0 | 0.567974 | seed_sampled_feature_target_association_proxy_not_model_importance |
| book_convexity_l5 | 12 | 0.00119268 | 0.000943766 | 8.08333 | 1.1645 | 0 | 0.7913 | seed_sampled_feature_target_association_proxy_not_model_importance |

## Top Trading Proxy Rows

| strategy_id | name | execution_profile | trades | gross_pnl_units_proxy | net_pnl_units_proxy | mean_gross_return | mean_cost_return | mean_net_return | expectancy_per_trade_proxy | win_rate_net | turnover_trade_count_proxy | sample_trades | sample_sharpe_per_trade | sample_sortino_per_trade | sample_max_drawdown_units | sample_profit_factor | sample_average_win | sample_average_loss | sample_cost_to_gross_profit_ratio | markout_sample_trades | adverse_selection_rate_6bar_proxy | mean_markout_1bar | mean_markout_3bar | mean_markout_6bar | mean_mae_proxy | mean_mfe_proxy | worst_mae_proxy | best_mfe_proxy | metric_scope | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Momentum/breakout filtered by MLOFI | retail_marketable_default | 160471 | 1199.69 | 997.662 | 0.00747604 | 0.00125895 | 0.00621709 | 0.00621709 | 0.60333 | 160471 | 9259 | 0.213846 | 0.331068 | -0.524619 | 1.77236 | 0.0232438 | -0.0196507 | 0.0856347 | 8923 | 0.398184 | 2.70135e-06 | 1.77072e-05 | 0.000196456 | -0.00238645 | 0.00253643 | -0.0416622 | 0.0554532 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S03 | Liquidity-vacuum breakout | retail_marketable_default | 273427 | 1636.09 | 1308.89 | 0.00598365 | 0.00119667 | 0.00478697 | 0.00478697 | 0.569501 | 273427 | 9259 | 0.160113 | 0.255819 | -0.795059 | 1.5225 | 0.026787 | -0.0234706 | 0.0747603 | 9077 | 0.446183 | 2.41876e-05 | 1.58779e-05 | 0.000102934 | -0.00245573 | 0.00253797 | -0.0479894 | 0.057629 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S05 | Microprice entry/exit filter | zero_latency_spread_only_control | 449765 | 674.308 | 524.008 | 0.00149924 | 0.000334175 | 0.00116507 | 0.00116507 | 0.503579 | 449765 | 9259 | 0.0513977 | 0.0750563 | -0.988813 | 1.15628 | 0.0182139 | -0.0162956 | 0.0353931 | 9128 | 0.451906 | -3.82972e-05 | -9.64268e-05 | -0.00012704 | -0.00209191 | 0.00193822 | -0.0611192 | 0.0442088 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S06 | Absorption and exhaustion reversal | zero_latency_spread_only_control | 34373 | 13.5274 | 6.37734 | 0.000393546 | 0.000208012 | 0.000185533 | 0.000185533 | 0.495389 | 34373 | 9259 | 0.00758495 | 0.0120124 | -3.76123 | 1.02009 | 0.0257533 | -0.02468 | 0.0162801 | 9083 | 0.447209 | -6.34208e-06 | -6.3921e-05 | -0.000173062 | -0.00374866 | 0.00363658 | -0.0733991 | 0.0682515 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S08 | Cross-ticker/index lead-lag OFI | zero_latency_spread_only_control | 448403 | 4.23189 | -66.4233 | 9.43769e-06 | 0.000157571 | -0.000148133 | -0.000148133 | 0.495951 | 448403 | 9259 | -0.0075879 | -0.0108398 | -3.30475 | 0.978963 | 0.0188645 | -0.0191083 | 0.0166953 | 8790 | 0.39909 | -2.79952e-07 | 4.36221e-05 | -2.19628e-05 | -0.00275063 | 0.00274997 | -0.0569767 | 0.0568646 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S09 | Pure queue-imbalance scalping | zero_latency_spread_only_control | 590612 | -12.2901 | -160.155 | -2.08091e-05 | 0.000250359 | -0.000271168 | -0.000271168 | 0.482628 | 590612 | 9259 | -0.0202669 | -0.0295509 | -4.5915 | 0.945552 | 0.0168515 | -0.0162576 | 0.030569 | 9077 | 0.460174 | 1.77089e-05 | 3.41036e-05 | 4.78117e-05 | -0.00187329 | 0.00191828 | -0.0406373 | 0.0323077 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S02 | Pure multi-level OFI directional model | zero_latency_spread_only_control | 907352 | -83.6182 | -271.38 | -9.21563e-05 | 0.000206934 | -0.00029909 | -0.00029909 | 0.492282 | 907352 | 9259 | -0.0197281 | -0.028149 | -6.26033 | 0.946398 | 0.0179459 | -0.0184971 | 0.0231274 | 9055 | 0.429045 | -2.70915e-06 | -6.19323e-05 | -0.000182128 | -0.00267452 | 0.00252212 | -0.0517047 | 0.051633 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S04 | Trade-flow plus depth confirmation | retail_marketable_default | 414066 | 289.075 | -263.011 | 0.000698138 | 0.00133333 | -0.000635192 | -0.000635192 | 0.49204 | 414066 | 9259 | -0.0153991 | -0.0231219 | -5.56522 | 0.959935 | 0.0246358 | -0.0249049 | 0.104304 | 9051 | 0.451331 | 3.27896e-05 | 1.88319e-07 | -7.61258e-05 | -0.00248816 | 0.00245141 | -0.0487026 | 0.0568757 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S07 | Mean reversion after imbalance | zero_latency_spread_only_control | 237064 | -116.439 | -207.094 | -0.000491173 | 0.000382406 | -0.000873579 | -0.000873579 | 0.484494 | 237064 | 9259 | -0.037467 | -0.0517213 | -8.61432 | 0.899326 | 0.0162446 | -0.0171244 | 0.0474794 | 9169 | 0.461773 | -2.09209e-05 | 3.17886e-05 | 7.83943e-05 | -0.00163764 | 0.00170159 | -0.0322194 | 0.0378998 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S04 | Trade-flow plus depth confirmation | zero_latency_spread_only_control | 429202 | -305.186 | -391.27 | -0.000711055 | 0.000200568 | -0.000911623 | -0.000911623 | 0.483248 | 429202 | 9259 | -0.0284581 | -0.0435064 | -10.0675 | 0.927506 | 0.0260949 | -0.0256983 | 0.0160107 | 9072 | 0.445216 | 3.56585e-06 | -6.55587e-05 | -6.45412e-05 | -0.00396001 | 0.00390783 | -0.073244 | 0.0767334 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |

## Required Breakdown Coverage

| current_status | breakdowns |
| --- | --- |
| available | 6 |
| proxy_available | 6 |

| breakdown_name | source_column | current_status | available_in_trade_sample | distinct_values_in_sample |
| --- | --- | --- | --- | --- |
| ticker | symbol | available | True | 32 |
| day | trade_date | available | True | 63 |
| regime | regime_code | available | True | 18 |
| time_of_day | bar_index | proxy_available | True | 75 |
| volatility_bucket | volatility_bucket | proxy_available | True | 3 |
| spread_bucket | spread_ticks | proxy_available | True | 36 |
| liquidity_bucket | liquidity_bucket | proxy_available | True | 3 |
| long_short | side | available | True | 2 |
| latency_profile | execution_profile | available | True | 3 |
| cost_profile | execution_profile | proxy_available | True | 3 |
| random_seed | seed | proxy_available | True | 30 |
| event_vs_non_event_day | is_market_shock_day | available | True | 2 |

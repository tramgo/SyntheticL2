# Phase 16 Metrics and Reporting Report

Generated UTC: 2026-07-13T19:30:54.822598+00:00

## Scope

This phase creates a metrics catalog and current-evidence scoreboards for Phase 11 predictive diagnostics and Phase 12 trading proxies.
No metric is acceptance-grade yet; current values are proxy/reporting evidence only.

## Metric Catalog Summary

| metric_category | current_status | metrics |
| --- | --- | --- |
| predictive | computed_proxy | 1 |
| predictive | missing | 3 |
| predictive | proxy_available | 1 |
| predictive | sample_proxy | 5 |
| trading | computed_proxy | 4 |
| trading | proxy_available | 2 |
| trading | sample_proxy | 11 |

## Top Predictive Proxy Rows

| strategy_id | name | support_level | rows_evaluated | signal_rows | signal_fraction | directional_accuracy_nonzero | directional_accuracy_status | mean_future_return_when_signaled | signed_mean_future_return | information_coefficient_proxy | promotion_allowed | acceptance_status | metric_scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S08 | Cross-ticker/index lead-lag OFI | partial_missing_required_features | 2259039 | 442897 | 0.196055 | 0.506523 | proxy_threshold_not_met | -4.27931e-05 | 2.1323e-05 | 2.1323e-05 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S06 | Absorption and exhaustion reversal | partial_missing_required_features | 2259039 | 33809 | 0.0149661 | 0.505817 | proxy_threshold_not_met | 1.82526e-05 | 4.1775e-05 | 4.1775e-05 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S07 | Mean reversion after imbalance | runnable_proxy | 2259039 | 234969 | 0.104013 | 0.501803 | proxy_threshold_not_met | -4.18652e-05 | 2.61682e-05 | 2.61682e-05 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S09 | Pure queue-imbalance scalping | runnable_proxy | 2259039 | 585389 | 0.259132 | 0.497817 | proxy_threshold_not_met | -1.43682e-05 | -1.37599e-05 | -1.37599e-05 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S05 | Microprice entry/exit filter | runnable_proxy | 2259039 | 445761 | 0.197323 | 0.497055 | proxy_threshold_not_met | -3.28375e-05 | -3.17341e-05 | -3.17341e-05 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S02 | Pure multi-level OFI directional model | runnable_proxy | 2259039 | 889386 | 0.393701 | 0.485228 | proxy_threshold_not_met | -2.84664e-07 | -0.000113875 | -0.000113875 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S04 | Trade-flow plus depth confirmation | partial_missing_required_features | 2259039 | 424857 | 0.18807 | 0.480748 | proxy_threshold_not_met | -3.52956e-05 | -0.00020299 | -0.00020299 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S03 | Liquidity-vacuum breakout | partial_missing_required_features | 2259039 | 280437 | 0.12414 | 0.466749 | proxy_threshold_not_met | -5.55783e-05 | -0.000700219 | -0.000700219 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S01 | Momentum/breakout filtered by MLOFI | runnable_proxy | 2259039 | 164347 | 0.0727508 | 0.434302 | proxy_threshold_not_met | 7.63156e-06 | -0.00110589 | -0.00110589 | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |
| S10 | Passive market making | not_supported_by_current_product | 2259039 | 0 | 0 |  | proxy_threshold_not_met |  |  |  | False | blocked_not_promotable | phase11_5m_proxy_diagnostic |

## Predictive Confusion / Rank Proxy Rows

| strategy_id | rows_evaluated | nonzero_signal_rows | directional_eval_rows | true_long_rows | false_long_rows | true_short_rows | false_short_rows | precision_long_proxy | recall_long_proxy | precision_short_proxy | recall_short_proxy | balanced_accuracy_proxy | rank_auc_proxy | incremental_r2_proxy | mean_signed_future_return_proxy | metric_scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S08 | 2259039 | 451880 | 435060 | 107371 | 110054 | 112997 | 104638 | 0.49383 | 0.506445 | 0.519204 | 0.506597 | 0.506521 | 0.502297 | 7.05975e-06 | 2.1323e-05 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S06 | 2259039 | 34317 | 33348 | 8728 | 7977 | 8140 | 8503 | 0.522478 | 0.506529 | 0.489095 | 0.505057 | 0.505793 | 0.500201 | 2.06886e-06 | 4.1775e-05 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S07 | 2259039 | 238167 | 227980 | 44440 | 45270 | 69961 | 68309 | 0.495374 | 0.39415 | 0.505974 | 0.607137 | 0.500643 | 0.502032 | 5.29654e-06 | 2.61682e-05 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S05 | 2259039 | 451810 | 431574 | 179101 | 181928 | 35415 | 35130 | 0.496085 | 0.836018 | 0.50202 | 0.162945 | 0.499482 | 0.496062 | 1.45894e-05 | -3.17341e-05 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S09 | 2259039 | 593280 | 569452 | 214323 | 217020 | 69160 | 68949 | 0.496874 | 0.756598 | 0.500764 | 0.241666 | 0.499132 | 0.496394 | 3.04598e-06 | -1.37599e-05 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S02 | 2259039 | 902476 | 868144 | 210534 | 224331 | 210714 | 222565 | 0.484136 | 0.486111 | 0.486324 | 0.48435 | 0.48523 | 0.490756 | 0.000404352 | -0.000113875 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S04 | 2259039 | 431866 | 419989 | 100657 | 107829 | 101252 | 110251 | 0.4828 | 0.477255 | 0.478726 | 0.484272 | 0.480764 | 0.493478 | 0.000614027 | -0.00020299 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S03 | 2259039 | 285249 | 277691 | 66581 | 75508 | 63031 | 72571 | 0.468587 | 0.478477 | 0.464824 | 0.454969 | 0.466723 | 0.492268 | 0.00482047 | -0.000700219 | phase11_ternary_signal_predictive_proxy_not_acceptance |
| S01 | 2259039 | 168258 | 162030 | 36193 | 46006 | 34177 | 45654 | 0.440309 | 0.442203 | 0.428117 | 0.426237 | 0.43422 | 0.490851 | 0.00704728 | -0.00110589 | phase11_ternary_signal_predictive_proxy_not_acceptance |

## Signal Bucket Future Returns

| strategy_id | signal_score_bucket | rows | mean_future_return | mean_signed_future_return | positive_future_fraction | metric_scope |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | flat_signal | 2064452 | -4.78375e-06 | 0 | 0.481949 | ternary_signal_bucket_not_true_decile |
| S01 | long_signal | 83319 | -0.00108316 | -0.00108316 | 0.424163 | ternary_signal_bucket_not_true_decile |
| S01 | short_signal | 81028 | 0.00112927 | -0.00112927 | 0.550512 | ternary_signal_bucket_not_true_decile |
| S02 | flat_signal | 1339413 | -6.24782e-06 | 0 | 0.483868 | ternary_signal_bucket_not_true_decile |
| S02 | long_signal | 445543 | -0.000113942 | -0.000113942 | 0.465967 | ternary_signal_bucket_not_true_decile |
| S02 | short_signal | 443843 | 0.000113808 | -0.000113808 | 0.493871 | ternary_signal_bucket_not_true_decile |
| S03 | flat_signal | 1948362 | 3.5746e-06 | 0 | 0.481482 | ternary_signal_bucket_not_true_decile |
| S03 | long_signal | 143496 | -0.000738535 | -0.000738535 | 0.457275 | ternary_signal_bucket_not_true_decile |
| S03 | short_signal | 136941 | 0.000660069 | -0.000660069 | 0.519682 | ternary_signal_bucket_not_true_decile |
| S04 | flat_signal | 1803942 | 3.53337e-06 | 0 | 0.480846 | ternary_signal_bucket_not_true_decile |
| S04 | long_signal | 210826 | -0.000240096 | -0.000240096 | 0.469837 | ternary_signal_bucket_not_true_decile |
| S04 | short_signal | 214031 | 0.000166438 | -0.000166438 | 0.506603 | ternary_signal_bucket_not_true_decile |
| S05 | flat_signal | 1783038 | 3.37407e-06 | 0 | 0.484314 | ternary_signal_bucket_not_true_decile |
| S05 | long_signal | 374843 | -3.83941e-05 | -3.83941e-05 | 0.471424 | ternary_signal_bucket_not_true_decile |
| S05 | short_signal | 70918 | -3.46786e-06 | 3.46786e-06 | 0.488629 | ternary_signal_bucket_not_true_decile |
| S06 | flat_signal | 2194990 | -4.20899e-06 | 0 | 0.481978 | ternary_signal_bucket_not_true_decile |
| S06 | long_signal | 16904 | 6.00294e-05 | 6.00294e-05 | 0.508269 | ternary_signal_bucket_not_true_decile |
| S06 | short_signal | 16905 | -2.35217e-05 | 2.35217e-05 | 0.495946 | ternary_signal_bucket_not_true_decile |
| S07 | flat_signal | 1993830 | 6.09599e-07 | 0 | 0.48333 | ternary_signal_bucket_not_true_decile |
| S07 | long_signal | 90654 | -2.03428e-05 | -2.03428e-05 | 0.483653 | ternary_signal_bucket_not_true_decile |
| S07 | short_signal | 144315 | -5.53849e-05 | 5.53849e-05 | 0.466965 | ternary_signal_bucket_not_true_decile |
| S08 | flat_signal | 1785902 | 5.78495e-06 | 0 | 0.485562 | ternary_signal_bucket_not_true_decile |
| S08 | long_signal | 221338 | -2.14808e-05 | -2.14808e-05 | 0.478798 | ternary_signal_bucket_not_true_decile |
| S08 | short_signal | 221559 | -6.40841e-05 | 6.40841e-05 | 0.459687 | ternary_signal_bucket_not_true_decile |
| S09 | flat_signal | 1643410 | -1.28158e-07 | 0 | 0.483999 | ternary_signal_bucket_not_true_decile |
| S09 | long_signal | 445887 | -1.84642e-05 | -1.84642e-05 | 0.474287 | ternary_signal_bucket_not_true_decile |
| S09 | short_signal | 139502 | -1.27629e-06 | 1.27629e-06 | 0.487634 | ternary_signal_bucket_not_true_decile |

## Top Trading Proxy Rows

| strategy_id | name | execution_profile | trades | gross_pnl_units_proxy | net_pnl_units_proxy | mean_gross_return | mean_cost_return | mean_net_return | expectancy_per_trade_proxy | win_rate_net | turnover_trade_count_proxy | sample_trades | sample_sharpe_per_trade | sample_sortino_per_trade | sample_max_drawdown_units | sample_profit_factor | sample_average_win | sample_average_loss | sample_cost_to_gross_profit_ratio | markout_sample_trades | adverse_selection_rate_6bar_proxy | mean_markout_1bar | mean_markout_3bar | mean_markout_6bar | mean_mae_proxy | mean_mfe_proxy | worst_mae_proxy | best_mfe_proxy | metric_scope | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Momentum/breakout filtered by MLOFI | retail_marketable_default | 160629 | 1196.04 | 993.766 | 0.00744598 | 0.00125926 | 0.00618672 | 0.00618672 | 0.603023 | 160629 | 9259 | 0.230755 | 0.362593 | -0.766743 | 1.85277 | 0.0230711 | -0.0194414 | 0.084805 | 8937 | 0.390511 | -1.53573e-05 | -1.99239e-05 | 0.000110605 | -0.00244988 | 0.00250982 | -0.048384 | 0.0375448 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S03 | Liquidity-vacuum breakout | retail_marketable_default | 273433 | 1638.12 | 1310.9 | 0.00599094 | 0.00119669 | 0.00479424 | 0.00479424 | 0.568969 | 273433 | 9259 | 0.148255 | 0.235525 | -0.922928 | 1.47815 | 0.0267537 | -0.0237439 | 0.075413 | 9068 | 0.446625 | 9.18676e-06 | -9.09546e-05 | 3.29237e-05 | -0.00257256 | 0.00259575 | -0.058881 | 0.0513245 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S05 | Microprice entry/exit filter | zero_latency_spread_only_control | 449723 | 674.085 | 523.749 | 0.00149889 | 0.000334287 | 0.0011646 | 0.0011646 | 0.503712 | 449723 | 9259 | 0.0600022 | 0.0923037 | -0.900772 | 1.18252 | 0.0182753 | -0.016043 | 0.0352464 | 9149 | 0.456443 | -1.21327e-05 | -7.90329e-05 | -0.000189727 | -0.00208542 | 0.00188096 | -0.0541586 | 0.0322474 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S06 | Absorption and exhaustion reversal | zero_latency_spread_only_control | 34199 | 13.5054 | 6.33407 | 0.000394906 | 0.000209694 | 0.000185212 | 0.000185212 | 0.494459 | 34199 | 9259 | 0.0120956 | 0.0191423 | -3.29565 | 1.03211 | 0.0256112 | -0.0245533 | 0.0162196 | 9088 | 0.450264 | 2.45129e-05 | 9.93581e-07 | -0.000146388 | -0.00373946 | 0.00370922 | -0.0560511 | 0.0658114 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S08 | Cross-ticker/index lead-lag OFI | zero_latency_spread_only_control | 448520 | 1.40284 | -69.3333 | 3.12771e-06 | 0.00015771 | -0.000154582 | -0.000154582 | 0.496232 | 448520 | 9259 | -0.00649199 | -0.00921075 | -3.1969 | 0.982027 | 0.0191147 | -0.0192347 | 0.0165918 | 8815 | 0.38979 | -1.30104e-05 | -2.54964e-05 | -0.000145605 | -0.00282269 | 0.00269403 | -0.0564932 | 0.0449866 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S09 | Pure queue-imbalance scalping | zero_latency_spread_only_control | 590670 | -13.6481 | -161.495 | -2.31062e-05 | 0.000250304 | -0.00027341 | -0.00027341 | 0.482606 | 590670 | 9259 | -0.0188124 | -0.0268216 | -6.22198 | 0.94916 | 0.0166383 | -0.0163689 | 0.0307712 | 9076 | 0.462208 | -2.72106e-05 | 3.84863e-05 | 2.16805e-05 | -0.00187 | 0.00186979 | -0.0625313 | 0.0323371 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S02 | Pure multi-level OFI directional model | zero_latency_spread_only_control | 898020 | -85.7117 | -271.664 | -9.54452e-05 | 0.00020707 | -0.000302515 | -0.000302515 | 0.492408 | 898020 | 9259 | -0.0140747 | -0.0203023 | -4.26363 | 0.962119 | 0.018034 | -0.0180798 | 0.0231368 | 9034 | 0.42971 | -1.50696e-05 | -7.25091e-05 | -0.000197181 | -0.0027137 | 0.00252617 | -0.0622316 | 0.0650779 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S04 | Trade-flow plus depth confirmation | retail_marketable_default | 414097 | 290.045 | -262.089 | 0.000700428 | 0.00133334 | -0.000632917 | -0.000632917 | 0.49229 | 414097 | 9259 | -0.0160164 | -0.0246905 | -5.96539 | 0.958249 | 0.0243497 | -0.0248193 | 0.105099 | 9067 | 0.4448 | -7.68306e-06 | -3.11884e-05 | -2.79435e-05 | -0.00248662 | 0.00244082 | -0.0562778 | 0.053311 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S07 | Mean reversion after imbalance | zero_latency_spread_only_control | 237102 | -116.533 | -207.189 | -0.000491488 | 0.000382349 | -0.000873837 | -0.000873837 | 0.484521 | 237102 | 9259 | -0.02746 | -0.0405573 | -6.66959 | 0.925919 | 0.0165024 | -0.0167945 | 0.0465093 | 9176 | 0.468178 | 8.07195e-06 | 3.78362e-05 | 3.87341e-05 | -0.00161873 | 0.00168355 | -0.0408371 | 0.0466217 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S04 | Trade-flow plus depth confirmation | zero_latency_spread_only_control | 429109 | -313.789 | -399.916 | -0.000731257 | 0.000200711 | -0.000931968 | -0.000931968 | 0.483166 | 429109 | 9259 | -0.0311369 | -0.0478113 | -11.2323 | 0.921085 | 0.0259061 | -0.0255461 | 0.0160557 | 9074 | 0.45162 | -0.000132294 | -0.000193714 | -0.000201188 | -0.00416868 | 0.00377846 | -0.0607617 | 0.0552476 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |

## Required Breakdown Coverage

| current_status | breakdowns |
| --- | --- |
| available | 6 |
| missing | 1 |
| proxy_available | 5 |

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
| random_seed | seed | missing | False | 0 |
| event_vs_non_event_day | is_market_shock_day | available | True | 2 |

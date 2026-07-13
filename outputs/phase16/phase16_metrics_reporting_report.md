# Phase 16 Metrics and Reporting Report

Generated UTC: 2026-07-13T18:57:42.184071+00:00

## Scope

This phase creates a metrics catalog and current-evidence scoreboards for Phase 11 predictive diagnostics and Phase 12 trading proxies.
No metric is acceptance-grade yet; current values are proxy/reporting evidence only.

## Metric Catalog Summary

| metric_category | current_status | metrics |
| --- | --- | --- |
| predictive | computed_proxy | 1 |
| predictive | missing | 8 |
| predictive | proxy_available | 1 |
| trading | computed_proxy | 4 |
| trading | missing | 2 |
| trading | proxy_available | 2 |
| trading | sample_proxy | 9 |

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

## Top Trading Proxy Rows

| strategy_id | name | execution_profile | trades | gross_pnl_units_proxy | net_pnl_units_proxy | mean_gross_return | mean_cost_return | mean_net_return | expectancy_per_trade_proxy | win_rate_net | turnover_trade_count_proxy | sample_trades | sample_sharpe_per_trade | sample_sortino_per_trade | sample_max_drawdown_units | sample_profit_factor | sample_average_win | sample_average_loss | sample_cost_to_gross_profit_ratio | metric_scope | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Momentum/breakout filtered by MLOFI | retail_marketable_default | 160629 | 1196.04 | 1140.05 | 0.00744598 | 0.000348576 | 0.00709741 | 0.00709741 | 0.617286 | 160629 | 83090 | 0.249077 | 0.398663 | -1.80166 | 1.93719 | 0.0235849 | -0.0193276 | 0.0236987 | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S03 | Liquidity-vacuum breakout | retail_marketable_default | 273433 | 1638.12 | 1559.92 | 0.00599094 | 0.000286006 | 0.00570493 | 0.00570493 | 0.581305 | 273433 |  |  |  |  |  |  |  |  | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S05 | Microprice entry/exit filter | zero_latency_spread_only_control | 449723 | 674.085 | 523.749 | 0.00149889 | 0.000334287 | 0.0011646 | 0.0011646 | 0.503712 | 449723 |  |  |  |  |  |  |  |  | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S04 | Trade-flow plus depth confirmation | retail_marketable_default | 414097 | 290.045 | 115.024 | 0.000700428 | 0.000422657 | 0.000277771 | 0.000277771 | 0.504995 | 414097 |  |  |  |  |  |  |  |  | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S06 | Absorption and exhaustion reversal | zero_latency_spread_only_control | 34199 | 13.5054 | 6.33407 | 0.000394906 | 0.000209694 | 0.000185212 | 0.000185212 | 0.494459 | 34199 |  |  |  |  |  |  |  |  | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S08 | Cross-ticker/index lead-lag OFI | zero_latency_spread_only_control | 448520 | 1.40284 | -69.3333 | 3.12771e-06 | 0.00015771 | -0.000154582 | -0.000154582 | 0.496232 | 448520 |  |  |  |  |  |  |  |  | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S03 | Liquidity-vacuum breakout | stressed_retail | 271051 | 104.674 | -61.4669 | 0.000386179 | 0.000612951 | -0.000226772 | -0.000226772 | 0.490196 | 271051 |  |  |  |  |  |  |  |  | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S09 | Pure queue-imbalance scalping | zero_latency_spread_only_control | 590670 | -13.6481 | -161.495 | -2.31062e-05 | 0.000250304 | -0.00027341 | -0.00027341 | 0.482606 | 590670 |  |  |  |  |  |  |  |  | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S02 | Pure multi-level OFI directional model | zero_latency_spread_only_control | 898020 | -85.7117 | -271.664 | -9.54452e-05 | 0.00020707 | -0.000302515 | -0.000302515 | 0.492408 | 898020 |  |  |  |  |  |  |  |  | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |
| S09 | Pure queue-imbalance scalping | retail_marketable_default | 573331 | 103.561 | -215.696 | 0.000180631 | 0.000556846 | -0.000376215 | -0.000376215 | 0.479976 | 573331 |  |  |  |  |  |  |  |  | phase12_5m_marketable_proxy_not_acceptance | simulated_marketable_proxy_not_acceptance |

## Required Breakdown Coverage

| current_status | breakdowns |
| --- | --- |
| available | 6 |
| missing | 3 |
| proxy_available | 3 |

| breakdown_name | source_column | current_status | available_in_trade_sample | distinct_values_in_sample |
| --- | --- | --- | --- | --- |
| ticker | symbol | available | True | 30 |
| day | trade_date | available | True | 63 |
| regime | regime_code | available | True | 18 |
| time_of_day | bar_index | proxy_available | True | 75 |
| volatility_bucket | volatility_bucket | missing | False | 0 |
| spread_bucket | spread_ticks | proxy_available | True | 15 |
| liquidity_bucket | liquidity_bucket | missing | False | 0 |
| long_short | side | available | True | 2 |
| latency_profile | execution_profile | available | True | 2 |
| cost_profile | execution_profile | proxy_available | True | 2 |
| random_seed | seed | missing | False | 0 |
| event_vs_non_event_day | is_market_shock_day | available | True | 2 |

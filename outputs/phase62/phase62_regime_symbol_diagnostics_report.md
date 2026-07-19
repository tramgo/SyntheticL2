# Phase62 Regime and Symbol Dependence Diagnostics

Generated UTC: 2026-07-19T19:18:45.606761+00:00

Phase62 diagnoses why the Phase60 lower-frequency candidate failed the Phase61 wider sweep.
It rolls the wider-sweep P&L up by symbol, month partition, instrument class, dominant regime, feed profile and loss reason.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase62_source_rows | 48 | Phase61 shard-symbol rows diagnosed |
| phase62_total_trades | 645 | Total candidate trades diagnosed |
| phase62_total_net_pnl_inr | -88748 | Total Phase61 wider-sweep net P&L |
| phase62_positive_symbol_rows | 7 | Shard-symbol rows positive after costs |
| phase62_positive_symbol_fraction | 0.145833 | Fraction of shard-symbol rows positive |
| phase62_viable_symbol_count | 1 | Symbols with positive aggregate P&L and at least 10 trades |
| phase62_viable_month_count | 0 | Trade-month partitions with positive aggregate P&L and at least 50 trades |
| phase62_viable_regime_count | 0 | Dominant regimes with positive aggregate P&L and at least 50 trades |
| phase62_viable_feed_profile_count | 0 | Dominant feed profiles with positive aggregate P&L and at least 50 trades |
| phase62_recommend_regime_symbol_specialization | 1 | 1 means a narrower specialization deserves a follow-up bounded replay |
| phase62_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |

## Candidate

| rule_id | signal_id | feature | side_mode | bar_events | feature_quantile | abs_threshold | discovery_trades | discovery_net_pnl_inr | discovery_gross_pnl_proxy_inr | discovery_cost_pnl_drag_proxy_inr | discovery_mean_net_return | discovery_precision_cost_clear | discovery_symbols | discovery_shards | discovery_positive_symbol_fraction | discovery_positive_shard_fraction | discovery_positive_after_costs | validation_trades | validation_net_pnl_inr | validation_gross_pnl_proxy_inr | validation_cost_pnl_drag_proxy_inr | validation_mean_net_return | validation_precision_cost_clear | validation_symbols | validation_shards | validation_positive_symbol_fraction | validation_positive_shard_fraction | validation_positive_after_costs | phase60_scale_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P60_BAR_MOMENTUM_B5000_Q70 | BAR_MOMENTUM | prev_bar_return | sign | 5000 | 0.7 | 0.00345298 | 115 | 903.264 | 14984.7 | 14081.5 | 7.85447e-05 | 0.382609 | 8 | 8 | 0.5 | 0.5 | True | 119 | 180.942 | 13864.1 | 13683.2 | 1.52052e-05 | 0.411765 | 8 | 8 | 0.625 | 0.625 | True | True |

## Symbol Rollup

| symbol | instrument_class | shard_symbol_rows | symbols | trade_dates | trades | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | positive_rows | mean_precision_cost_clear | positive_row_fraction | mean_net_pnl_per_trade_inr | cost_drag_to_abs_gross_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KOTAKBANK | EQUITY | 2 | 1 | 2 | 30 | 69.1643 | 3871.03 | 3801.86 | 1 | 0.380383 | 0.5 | 2.30548 | 0.982133 |
| NIFTYBEES | ETF | 2 | 1 | 2 | 19 | -358.439 | 1717.46 | 2075.9 | 1 | 0.352564 | 0.5 | -18.8652 | 1.2087 |
| RELIANCE | EQUITY | 2 | 1 | 2 | 33 | -443.631 | 3202.21 | 3645.84 | 1 | 0.303571 | 0.5 | -13.4434 | 1.13854 |
| NESTLEIND | EQUITY | 2 | 1 | 2 | 25 | -776.116 | 2449.72 | 3225.84 | 1 | 0.416667 | 0.5 | -31.0447 | 1.31682 |
| BRITANNIA | EQUITY | 1 | 1 | 1 | 9 | -1377.01 | -85.5121 | 1291.5 | 0 | 0.222222 | 0 | -153.001 | 15.1031 |
| HDFCBANK | EQUITY | 1 | 1 | 1 | 16 | -1404.07 | 289.749 | 1693.82 | 0 | 0.375 | 0 | -87.7543 | 5.84582 |
| ITBEES | ETF | 1 | 1 | 1 | 8 | -1567.92 | -493.749 | 1074.17 | 0 | 0.25 | 0 | -195.99 | 2.17554 |
| HINDUNILVR | EQUITY | 1 | 1 | 1 | 11 | -1590.9 | -316.414 | 1274.49 | 0 | 0.363636 | 0 | -144.628 | 4.02792 |
| DRREDDY | EQUITY | 1 | 1 | 1 | 7 | -1741.99 | -873.44 | 868.546 | 0 | 0 | 0 | -248.855 | 0.994397 |
| CIPLA | EQUITY | 1 | 1 | 1 | 12 | -2073.94 | -520.33 | 1553.61 | 0 | 0.333333 | 0 | -172.828 | 2.98581 |
| ICICIBANK | EQUITY | 1 | 1 | 1 | 15 | -2382.09 | -746.864 | 1635.22 | 0 | 0.4 | 0 | -158.806 | 2.18945 |
| BANKBEES | ETF | 1 | 1 | 1 | 8 | -2385.1 | -1264.1 | 1121 | 0 | 0 | 0 | -298.137 | 0.886801 |
| MARUTI | EQUITY | 2 | 1 | 2 | 20 | -2399.99 | 216.495 | 2616.48 | 1 | 0.227273 | 0.5 | -119.999 | 12.0856 |
| BAJAJ-AUTO | EQUITY | 1 | 1 | 1 | 19 | -2403.74 | 89.1836 | 2492.92 | 0 | 0.368421 | 0 | -126.513 | 27.9527 |
| BPCL | EQUITY | 1 | 1 | 1 | 15 | -2525.45 | -845.18 | 1680.27 | 0 | 0.266667 | 0 | -168.363 | 1.98806 |
| INFY | EQUITY | 1 | 1 | 1 | 18 | -2546 | -479.809 | 2066.19 | 0 | 0.388889 | 0 | -141.444 | 4.30627 |
| BHARTIARTL | EQUITY | 1 | 1 | 1 | 9 | -2621.79 | -1621.72 | 1000.07 | 0 | 0 | 0 | -291.31 | 0.616672 |
| AXISBANK | EQUITY | 1 | 1 | 1 | 14 | -2934.13 | -1390.97 | 1543.15 | 0 | 0.214286 | 0 | -209.581 | 1.10941 |
| ITC | EQUITY | 2 | 1 | 2 | 22 | -2989.43 | -478.48 | 2510.95 | 0 | 0.3125 | 0 | -135.883 | 5.24776 |
| GOLDBEES | ETF | 1 | 1 | 1 | 13 | -3029.09 | -1723.54 | 1305.55 | 0 | 0.230769 | 0 | -233.007 | 0.757478 |
| SBIN | EQUITY | 2 | 1 | 2 | 33 | -3111.74 | 724.979 | 3836.72 | 1 | 0.272556 | 0.5 | -94.2952 | 5.29218 |
| JUNIORBEES | ETF | 2 | 1 | 2 | 18 | -3498.57 | -955.283 | 2543.28 | 0 | 0.2875 | 0 | -194.365 | 2.66233 |
| ONGC | EQUITY | 2 | 1 | 2 | 33 | -3746.39 | 134.865 | 3881.26 | 0 | 0.265385 | 0 | -113.527 | 28.7789 |
| M&M | EQUITY | 2 | 1 | 2 | 30 | -3783.49 | -589.163 | 3194.32 | 0 | 0.361607 | 0 | -126.116 | 5.4218 |
| TCS | EQUITY | 2 | 1 | 2 | 29 | -3969.3 | -637.961 | 3331.34 | 0 | 0.27381 | 0 | -136.872 | 5.22185 |
| HCLTECH | EQUITY | 1 | 1 | 1 | 16 | -4095.62 | -2107.44 | 1988.18 | 0 | 0.125 | 0 | -255.976 | 0.943409 |
| ADANIPORTS | EQUITY | 1 | 1 | 1 | 12 | -4110.38 | -2661.95 | 1448.44 | 0 | 0.166667 | 0 | -342.532 | 0.544128 |
| SUNPHARMA | EQUITY | 2 | 1 | 2 | 25 | -4116.42 | -1154.21 | 2962.2 | 0 | 0.236111 | 0 | -164.657 | 2.56643 |
| WIPRO | EQUITY | 2 | 1 | 2 | 32 | -4337.68 | -468.893 | 3868.79 | 1 | 0.298039 | 0.5 | -135.553 | 8.25089 |
| ULTRACEMCO | EQUITY | 2 | 1 | 2 | 35 | -4872.88 | -459.618 | 4413.26 | 0 | 0.344771 | 0 | -139.225 | 9.60201 |
| TECHM | EQUITY | 2 | 1 | 2 | 32 | -5017.94 | -639.64 | 4378.3 | 0 | 0.254545 | 0 | -156.811 | 6.84494 |
| LT | EQUITY | 2 | 1 | 2 | 27 | -6605.99 | -3727.56 | 2878.43 | 0 | 0.296703 | 0 | -244.666 | 0.772202 |

## Month Rollup

| trade_month_partition | shard_symbol_rows | symbols | trade_dates | trades | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | positive_rows | mean_precision_cost_clear | positive_row_fraction | mean_net_pnl_per_trade_inr | cost_drag_to_abs_gross_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | 16 | 16 | 1 | 259 | -13330.1 | 17722.9 | 31053.1 | 7 | 0.422955 | 0.4375 | -51.4677 | 1.75214 |
| 2026-02 | 32 | 32 | 1 | 386 | -75417.9 | -29269.1 | 46148.8 | 0 | 0.20955 | 0 | -195.383 | 1.57671 |

## Instrument Class Rollup

| instrument_class | shard_symbol_rows | symbols | trade_dates | trades | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | positive_rows | mean_precision_cost_clear | positive_row_fraction | mean_net_pnl_per_trade_inr | cost_drag_to_abs_gross_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ETF | 7 | 5 | 2 | 66 | -10839.1 | -2719.21 | 8119.9 | 1 | 0.251557 | 0.142857 | -164.229 | 2.98613 |
| EQUITY | 41 | 27 | 2 | 579 | -77908.9 | -8826.93 | 69082 | 6 | 0.285658 | 0.146341 | -134.558 | 7.82627 |

## Regime Rollup

| dominant_regime_code | shard_symbol_rows | symbols | trade_dates | trades | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | positive_rows | mean_precision_cost_clear | positive_row_fraction | mean_net_pnl_per_trade_inr | cost_drag_to_abs_gross_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D04 | 48 | 32 | 2 | 645 | -88748 | -11546.1 | 77201.9 | 7 | 0.280685 | 0.145833 | -137.594 | 6.68638 |

## Feed Profile Rollup

| dominant_feed_profile | shard_symbol_rows | symbols | trade_dates | trades | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | positive_rows | mean_precision_cost_clear | positive_row_fraction | mean_net_pnl_per_trade_inr | cost_drag_to_abs_gross_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| disconnect_scenario | 48 | 32 | 2 | 645 | -88748 | -11546.1 | 77201.9 | 7 | 0.280685 | 0.145833 | -137.594 | 6.68638 |

## Loss Reason Rollup

| loss_reason | shard_symbol_rows | symbols | trade_dates | trades | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | positive_rows | mean_precision_cost_clear | positive_row_fraction | mean_net_pnl_per_trade_inr | cost_drag_to_abs_gross_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| positive_after_costs | 7 | 7 | 1 | 116 | 6290.53 | 20189.3 | 13898.8 | 7 | 0.514123 | 1 | 54.2287 | 0.688423 |
| cost_drag_over_gross_edge | 9 | 9 | 2 | 149 | -12069.7 | 6053.03 | 18122.7 | 0 | 0.370568 | 0 | -81.0045 | 2.99399 |
| wrong_direction | 32 | 30 | 2 | 380 | -82968.9 | -37788.5 | 45180.4 | 0 | 0.20434 | 0 | -218.339 | 1.19561 |

## Shock Rollup

| market_shock_bucket | symbol_shock_bucket | shard_symbol_rows | symbols | trade_dates | trades | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | positive_rows | mean_precision_cost_clear | positive_row_fraction | mean_net_pnl_per_trade_inr | cost_drag_to_abs_gross_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no_market_shock_rows | no_symbol_shock_rows | 48 | 32 | 2 | 645 | -88748 | -11546.1 | 77201.9 | 7 | 0.280685 | 0.145833 | -137.594 | 6.68638 |

## P&L Concentration

| metric | value | description |
| --- | --- | --- |
| total_net_pnl_inr | -88748 | Total Phase61 wider-sweep net P&L |
| positive_rows | 7 | Shard-symbol rows positive after costs |
| negative_rows | 41 | Shard-symbol rows negative after costs |
| positive_net_pnl_inr | 6290.53 | Sum of positive shard-symbol net P&L |
| negative_net_pnl_inr | -95038.6 | Sum of negative shard-symbol net P&L |
| top_5_rows_net_pnl_inr | 5915.21 | Net P&L concentration in best five shard-symbol rows |
| worst_5_rows_net_pnl_inr | -21073 | Net P&L concentration in worst five shard-symbol rows |

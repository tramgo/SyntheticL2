# Phase60 Lower-Frequency Meta Replay

Generated UTC: 2026-07-19T19:11:52.804460+00:00

Phase60 pivots away from dense marketable micro-trading by aggregating dense ticks into event bars.
Thresholds are fit on discovery bars and tested on disjoint validation bars after Zerodha retail costs.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase60_discovery_shards | 8 | Dense shards used for lower-frequency threshold discovery |
| phase60_validation_shards | 8 | Disjoint dense shards used for validation |
| phase60_discovery_bar_rows | 2534 | Discovery event-bar rows |
| phase60_validation_bar_rows | 2512 | Validation event-bar rows |
| phase60_rule_rows | 36 | Lower-frequency rule rows evaluated |
| phase60_validation_positive_rows | 4 | Rules positive after retail costs on validation |
| phase60_scale_candidate_rows | 1 | Rules passing lower-frequency scale gate |
| phase60_best_traded_validation_net_pnl_inr | 4939 | Best validation net P&L among rows that emitted validation trades |
| phase60_elapsed_seconds | 9.74305 | Elapsed seconds |
| phase60_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |
| phase60_recommend_scale_to_month_sweep | 1 | 1 means at least one lower-frequency rule deserves a broader month/symbol sweep |

## Top Lower-Frequency Results

| rule_id | signal_id | feature | side_mode | bar_events | feature_quantile | abs_threshold | discovery_trades | discovery_net_pnl_inr | discovery_gross_pnl_proxy_inr | discovery_cost_pnl_drag_proxy_inr | discovery_mean_net_return | discovery_precision_cost_clear | discovery_symbols | discovery_shards | discovery_positive_symbol_fraction | discovery_positive_shard_fraction | discovery_positive_after_costs | validation_trades | validation_net_pnl_inr | validation_gross_pnl_proxy_inr | validation_cost_pnl_drag_proxy_inr | validation_mean_net_return | validation_precision_cost_clear | validation_symbols | validation_shards | validation_positive_symbol_fraction | validation_positive_shard_fraction | validation_positive_after_costs | phase60_scale_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P60_BAR_MOMENTUM_B5000_Q70 | BAR_MOMENTUM | prev_bar_return | sign | 5000 | 0.7 | 0.00345298 | 115 | 903.264 | 14984.7 | 14081.5 | 7.85447e-05 | 0.382609 | 8 | 8 | 0.5 | 0.5 | True | 119 | 180.942 | 13864.1 | 13683.2 | 1.52052e-05 | 0.411765 | 8 | 8 | 0.625 | 0.625 | True | True |
| P60_BAR_MOMENTUM_B10000_Q50 | BAR_MOMENTUM | prev_bar_return | sign | 10000 | 0.5 | 0.00371387 | 92 | -7536.67 | 3749.32 | 11286 | -0.000819203 | 0.369565 | 8 | 8 | 0.25 | 0.25 | False | 93 | 4939 | 15651.5 | 10712.5 | 0.000531075 | 0.451613 | 8 | 8 | 0.625 | 0.625 | True | False |
| P60_BAR_CONTRARIAN_B10000_Q90 | BAR_CONTRARIAN | prev_bar_return | opposite | 10000 | 0.9 | 0.00824448 | 19 | -1516.38 | 775.432 | 2291.81 | -0.000798096 | 0.421053 | 8 | 8 | 0.5 | 0.5 | False | 20 | 467.718 | 2749.13 | 2281.42 | 0.000233859 | 0.55 | 7 | 7 | 0.285714 | 0.285714 | True | False |
| P60_BAR_MOMENTUM_B10000_Q70 | BAR_MOMENTUM | prev_bar_return | sign | 10000 | 0.7 | 0.00544563 | 55 | -6008.29 | 731.723 | 6740.02 | -0.00109242 | 0.363636 | 8 | 8 | 0.375 | 0.375 | False | 55 | 417.036 | 6756.39 | 6339.35 | 7.58246e-05 | 0.4 | 8 | 8 | 0.375 | 0.375 | True | False |
| P60_BAR_MOMENTUM_B5000_Q50 | BAR_MOMENTUM | prev_bar_return | sign | 5000 | 0.5 | 0.00212317 | 192 | -2074.86 | 21694.1 | 23769 | -0.000108066 | 0.395833 | 8 | 8 | 0.375 | 0.375 | False | 198 | -1703.9 | 21201.4 | 22905.3 | -8.60555e-05 | 0.409091 | 8 | 8 | 0.625 | 0.625 | False | False |
| P60_BAR_CONTRARIAN_B1000_Q90 | BAR_CONTRARIAN | prev_bar_return | opposite | 1000 | 0.9 | 0.00279777 | 197 | -1476.65 | 22696.4 | 24173.1 | -7.49568e-05 | 0.401015 | 8 | 8 | 0.5 | 0.5 | False | 181 | -1869.76 | 19017.7 | 20887.4 | -0.000103302 | 0.403315 | 8 | 8 | 0.5 | 0.5 | False | False |
| P60_BAR_MICROPRICE_B10000_Q90 | BAR_MICROPRICE | avg_microprice_dev | sign | 10000 | 0.9 | 7.75273e-05 | 19 | -365.701 | 2084.45 | 2450.15 | -0.000192474 | 0.526316 | 1 | 1 | 0 | 0 | False | 23 | -2727.59 | 354.495 | 3082.09 | -0.00118591 | 0.347826 | 1 | 1 | 0 | 0 | False | False |
| P60_BAR_CONTRARIAN_B5000_Q90 | BAR_CONTRARIAN | prev_bar_return | opposite | 5000 | 0.9 | 0.00580853 | 39 | -10151.9 | -5422.48 | 4729.43 | -0.00260305 | 0.153846 | 8 | 8 | 0.125 | 0.125 | False | 43 | -4300.7 | 660.315 | 4961.02 | -0.00100016 | 0.232558 | 8 | 8 | 0.375 | 0.375 | False | False |
| P60_BAR_MOMENTUM_B10000_Q90 | BAR_MOMENTUM | prev_bar_return | sign | 10000 | 0.9 | 0.00824448 | 19 | -3067.25 | -775.432 | 2291.81 | -0.00161434 | 0.368421 | 8 | 8 | 0.125 | 0.125 | False | 20 | -5030.55 | -2749.13 | 2281.42 | -0.00251527 | 0.3 | 7 | 7 | 0.142857 | 0.142857 | False | False |
| P60_BAR_MOMENTUM_B5000_Q90 | BAR_MOMENTUM | prev_bar_return | sign | 5000 | 0.9 | 0.00580853 | 39 | 693.056 | 5422.48 | 4729.43 | 0.000177707 | 0.384615 | 8 | 8 | 0.25 | 0.25 | True | 43 | -5621.33 | -660.315 | 4961.02 | -0.00130729 | 0.395349 | 8 | 8 | 0.25 | 0.25 | False | False |
| P60_BAR_MICROPRICE_B5000_Q90 | BAR_MICROPRICE | avg_microprice_dev | sign | 5000 | 0.9 | 7.76804e-05 | 39 | -3267.27 | 1762.36 | 5029.63 | -0.000837761 | 0.358974 | 1 | 1 | 0 | 0 | False | 48 | -6044.43 | 387.948 | 6432.38 | -0.00125926 | 0.291667 | 1 | 1 | 0 | 0 | False | False |
| P60_BAR_IMBALANCE_B10000_Q90 | BAR_IMBALANCE | avg_l1_imbalance | sign | 10000 | 0.9 | 0.566708 | 19 | -882.741 | 1566.97 | 2449.71 | -0.000464601 | 0.526316 | 1 | 1 | 0 | 0 | False | 46 | -6704.61 | -1193.19 | 5511.42 | -0.00145752 | 0.347826 | 2 | 2 | 0 | 0 | False | False |
| P60_BAR_CONTRARIAN_B10000_Q70 | BAR_CONTRARIAN | prev_bar_return | opposite | 10000 | 0.7 | 0.00544563 | 55 | -7471.74 | -731.723 | 6740.02 | -0.0013585 | 0.436364 | 8 | 8 | 0.25 | 0.25 | False | 55 | -13095.7 | -6756.39 | 6339.35 | -0.00238104 | 0.4 | 8 | 8 | 0.25 | 0.25 | False | False |
| P60_BAR_IMBALANCE_B5000_Q90 | BAR_IMBALANCE | avg_l1_imbalance | sign | 5000 | 0.9 | 0.565462 | 39 | -5432.66 | -405.306 | 5027.35 | -0.00139299 | 0.307692 | 1 | 1 | 0 | 0 | False | 93 | -13203.4 | -2017.57 | 11185.8 | -0.00141972 | 0.290323 | 2 | 2 | 0 | 0 | False | False |
| P60_BAR_IMBALANCE_B10000_Q70 | BAR_IMBALANCE | avg_l1_imbalance | sign | 10000 | 0.7 | 0.214845 | 55 | -2943.17 | 4313.52 | 7256.69 | -0.000535122 | 0.472727 | 3 | 3 | 0.333333 | 0.333333 | False | 92 | -13950.1 | -3092.93 | 10857.2 | -0.00151632 | 0.380435 | 4 | 4 | 0 | 0 | False | False |
| P60_BAR_MICROPRICE_B10000_Q70 | BAR_MICROPRICE | avg_microprice_dev | sign | 10000 | 0.7 | 2.31875e-05 | 55 | -1912.92 | 5344.7 | 7257.62 | -0.000347804 | 0.490909 | 3 | 3 | 0.333333 | 0.333333 | False | 115 | -16237.5 | -2538.44 | 13699.1 | -0.00141196 | 0.365217 | 5 | 5 | 0 | 0 | False | False |
| P60_BAR_MICROPRICE_B10000_Q50 | BAR_MICROPRICE | avg_microprice_dev | sign | 10000 | 0.5 | 9.70866e-06 | 92 | -8376.89 | 3566.07 | 11943 | -0.000910531 | 0.434783 | 4 | 4 | 0 | 0 | False | 138 | -19907.4 | -3579.93 | 16327.4 | -0.00144256 | 0.347826 | 6 | 6 | 0 | 0 | False | False |
| P60_BAR_IMBALANCE_B10000_Q50 | BAR_IMBALANCE | avg_l1_imbalance | sign | 10000 | 0.5 | 0.087248 | 92 | -8376.89 | 3566.07 | 11943 | -0.000910531 | 0.434783 | 4 | 4 | 0 | 0 | False | 161 | -22809.5 | -4175.31 | 18634.2 | -0.00141674 | 0.335404 | 7 | 7 | 0 | 0 | False | False |
| P60_BAR_CONTRARIAN_B10000_Q50 | BAR_CONTRARIAN | prev_bar_return | opposite | 10000 | 0.5 | 0.00371387 | 92 | -15035.3 | -3749.32 | 11286 | -0.00163427 | 0.423913 | 8 | 8 | 0 | 0 | False | 93 | -26364 | -15651.5 | 10712.5 | -0.00283484 | 0.397849 | 8 | 8 | 0 | 0 | False | False |
| P60_BAR_IMBALANCE_B5000_Q70 | BAR_IMBALANCE | avg_l1_imbalance | sign | 5000 | 0.7 | 0.21453 | 115 | -11661.3 | 3509.96 | 15171.3 | -0.00101403 | 0.347826 | 3 | 3 | 0 | 0 | False | 194 | -27478 | -4552.3 | 22925.7 | -0.00141639 | 0.314433 | 5 | 5 | 0 | 0 | False | False |
| P60_BAR_CONTRARIAN_B5000_Q70 | BAR_CONTRARIAN | prev_bar_return | opposite | 5000 | 0.7 | 0.00345298 | 115 | -29066.2 | -14984.7 | 14081.5 | -0.00252749 | 0.182609 | 8 | 8 | 0 | 0 | False | 119 | -27547.3 | -13864.1 | 13683.2 | -0.0023149 | 0.226891 | 8 | 8 | 0 | 0 | False | False |
| P60_BAR_MICROPRICE_B1000_Q90 | BAR_MICROPRICE | avg_microprice_dev | sign | 1000 | 0.9 | 7.74054e-05 | 197 | -22842.3 | 2563.63 | 25405.9 | -0.00115951 | 0.152284 | 1 | 1 | 0 | 0 | False | 244 | -31796.2 | 900.661 | 32696.9 | -0.00130312 | 0.118852 | 1 | 1 | 0 | 0 | False | False |
| P60_BAR_MICROPRICE_B5000_Q70 | BAR_MICROPRICE | avg_microprice_dev | sign | 5000 | 0.7 | 2.31786e-05 | 115 | -12970.7 | 2201.42 | 15172.1 | -0.00112789 | 0.356522 | 3 | 3 | 0 | 0 | False | 239 | -31874.3 | -3388.67 | 28485.7 | -0.00133365 | 0.32636 | 5 | 5 | 0 | 0 | False | False |
| P60_BAR_MOMENTUM_B1000_Q90 | BAR_MOMENTUM | prev_bar_return | sign | 1000 | 0.9 | 0.00279777 | 197 | -46869.5 | -22696.4 | 24173.1 | -0.00237916 | 0.238579 | 8 | 8 | 0 | 0 | False | 181 | -39905.1 | -19017.7 | 20887.4 | -0.0022047 | 0.276243 | 8 | 8 | 0 | 0 | False | False |
| P60_BAR_CONTRARIAN_B5000_Q50 | BAR_CONTRARIAN | prev_bar_return | opposite | 5000 | 0.5 | 0.00212317 | 192 | -45463.1 | -21694.1 | 23769 | -0.00236787 | 0.21875 | 8 | 8 | 0 | 0 | False | 198 | -44106.7 | -21201.4 | 22905.3 | -0.00222761 | 0.222222 | 8 | 8 | 0 | 0 | False | False |
| P60_BAR_MICROPRICE_B5000_Q50 | BAR_MICROPRICE | avg_microprice_dev | sign | 5000 | 0.5 | 8.2227e-06 | 192 | -19912.5 | 5012.29 | 24924.8 | -0.00103711 | 0.369792 | 4 | 4 | 0 | 0 | False | 332 | -44394.7 | -5909.31 | 38485.3 | -0.00133719 | 0.313253 | 7 | 7 | 0 | 0 | False | False |
| P60_BAR_IMBALANCE_B5000_Q50 | BAR_IMBALANCE | avg_l1_imbalance | sign | 5000 | 0.5 | 0.0860185 | 192 | -21242.6 | 3544.23 | 24786.9 | -0.00110639 | 0.364583 | 5 | 5 | 0 | 0 | False | 336 | -44860.3 | -5942.98 | 38917.3 | -0.00133513 | 0.309524 | 8 | 8 | 0 | 0 | False | False |
| P60_BAR_CONTRARIAN_B1000_Q70 | BAR_CONTRARIAN | prev_bar_return | opposite | 1000 | 0.7 | 0.00108167 | 591 | -56290.3 | 16883.6 | 73173.9 | -0.000952459 | 0.321489 | 8 | 8 | 0.125 | 0.125 | False | 595 | -47303.9 | 21629.1 | 68933.1 | -0.000795024 | 0.352941 | 8 | 8 | 0 | 0 | False | False |
| P60_BAR_IMBALANCE_B1000_Q90 | BAR_IMBALANCE | avg_l1_imbalance | sign | 1000 | 0.9 | 0.564505 | 197 | -24541.6 | 857.15 | 25398.7 | -0.00124577 | 0.137056 | 1 | 1 | 0 | 0 | False | 460 | -58071.4 | -2559.26 | 55512.1 | -0.00126242 | 0.115217 | 2 | 2 | 0 | 0 | False | False |
| P60_BAR_CONTRARIAN_B1000_Q50 | BAR_CONTRARIAN | prev_bar_return | opposite | 1000 | 0.5 | 0 | 964 | -104747 | 15018 | 119765 | -0.00108658 | 0.28527 | 8 | 8 | 0 | 0 | False | 927 | -82434.4 | 24618.4 | 107053 | -0.00088926 | 0.323625 | 8 | 8 | 0 | 0 | False | False |
| P60_BAR_MOMENTUM_B1000_Q70 | BAR_MOMENTUM | prev_bar_return | sign | 1000 | 0.7 | 0.00108167 | 591 | -90057.5 | -16883.6 | 73173.9 | -0.00152382 | 0.291032 | 8 | 8 | 0 | 0 | False | 595 | -90562.2 | -21629.1 | 68933.1 | -0.00152205 | 0.272269 | 8 | 8 | 0 | 0 | False | False |
| P60_BAR_IMBALANCE_B1000_Q70 | BAR_IMBALANCE | avg_l1_imbalance | sign | 1000 | 0.7 | 0.216181 | 590 | -71101.3 | 6643.86 | 77745.1 | -0.00120511 | 0.150847 | 3 | 3 | 0 | 0 | False | 991 | -121300 | -4175.98 | 117124 | -0.00122401 | 0.133199 | 6 | 6 | 0 | 0 | False | False |
| P60_BAR_MOMENTUM_B1000_Q50 | BAR_MOMENTUM | prev_bar_return | sign | 1000 | 0.5 | 0 | 964 | -134783 | -15018 | 119765 | -0.00139816 | 0.267635 | 8 | 8 | 0 | 0 | False | 927 | -131671 | -24618.4 | 107053 | -0.0014204 | 0.266451 | 8 | 8 | 0 | 0 | False | False |
| P60_BAR_MICROPRICE_B1000_Q70 | BAR_MICROPRICE | avg_microprice_dev | sign | 1000 | 0.7 | 2.33585e-05 | 590 | -68618.5 | 9131.42 | 77749.9 | -0.00116302 | 0.149153 | 3 | 3 | 0 | 0 | False | 1208 | -147545 | -3564.53 | 143980 | -0.0012214 | 0.137417 | 5 | 5 | 0 | 0 | False | False |
| P60_BAR_IMBALANCE_B1000_Q50 | BAR_IMBALANCE | avg_l1_imbalance | sign | 1000 | 0.5 | 0.0894569 | 983 | -118880 | 8053.17 | 126934 | -0.00120936 | 0.160732 | 5 | 5 | 0 | 0 | False | 1702 | -204757 | -7653.78 | 197103 | -0.00120304 | 0.135135 | 8 | 8 | 0 | 0 | False | False |
| P60_BAR_MICROPRICE_B1000_Q50 | BAR_MICROPRICE | avg_microprice_dev | sign | 1000 | 0.5 | 7.00295e-06 | 984 | -119191 | 8012.33 | 127204 | -0.00121129 | 0.158537 | 5 | 5 | 0 | 0 | False | 1839 | -218003 | -5090.46 | 212912 | -0.00118544 | 0.13975 | 8 | 8 | 0 | 0 | False | False |

## Oracle Summary

| split | bar_events | bars | oracle_trades | oracle_trade_fraction | oracle_net_pnl_inr |
| --- | --- | --- | --- | --- | --- |
| discovery | 1000 | 1966 | 555 | 0.282299 | 108195 |
| discovery | 5000 | 384 | 260 | 0.677083 | 72873.6 |
| discovery | 10000 | 184 | 148 | 0.804348 | 56471.4 |
| validation | 1000 | 1946 | 588 | 0.302158 | 114986 |
| validation | 5000 | 382 | 268 | 0.701571 | 78224.8 |
| validation | 10000 | 184 | 149 | 0.809783 | 60112.5 |

## Rule Thresholds

| rule_id | signal_id | feature | side_mode | bar_events | feature_quantile | abs_threshold |
| --- | --- | --- | --- | --- | --- | --- |
| P60_BAR_MOMENTUM_B1000_Q50 | BAR_MOMENTUM | prev_bar_return | sign | 1000 | 0.5 | 0 |
| P60_BAR_MOMENTUM_B1000_Q70 | BAR_MOMENTUM | prev_bar_return | sign | 1000 | 0.7 | 0.00108167 |
| P60_BAR_MOMENTUM_B1000_Q90 | BAR_MOMENTUM | prev_bar_return | sign | 1000 | 0.9 | 0.00279777 |
| P60_BAR_CONTRARIAN_B1000_Q50 | BAR_CONTRARIAN | prev_bar_return | opposite | 1000 | 0.5 | 0 |
| P60_BAR_CONTRARIAN_B1000_Q70 | BAR_CONTRARIAN | prev_bar_return | opposite | 1000 | 0.7 | 0.00108167 |
| P60_BAR_CONTRARIAN_B1000_Q90 | BAR_CONTRARIAN | prev_bar_return | opposite | 1000 | 0.9 | 0.00279777 |
| P60_BAR_IMBALANCE_B1000_Q50 | BAR_IMBALANCE | avg_l1_imbalance | sign | 1000 | 0.5 | 0.0894569 |
| P60_BAR_IMBALANCE_B1000_Q70 | BAR_IMBALANCE | avg_l1_imbalance | sign | 1000 | 0.7 | 0.216181 |
| P60_BAR_IMBALANCE_B1000_Q90 | BAR_IMBALANCE | avg_l1_imbalance | sign | 1000 | 0.9 | 0.564505 |
| P60_BAR_MICROPRICE_B1000_Q50 | BAR_MICROPRICE | avg_microprice_dev | sign | 1000 | 0.5 | 7.00295e-06 |
| P60_BAR_MICROPRICE_B1000_Q70 | BAR_MICROPRICE | avg_microprice_dev | sign | 1000 | 0.7 | 2.33585e-05 |
| P60_BAR_MICROPRICE_B1000_Q90 | BAR_MICROPRICE | avg_microprice_dev | sign | 1000 | 0.9 | 7.74054e-05 |
| P60_BAR_MOMENTUM_B5000_Q50 | BAR_MOMENTUM | prev_bar_return | sign | 5000 | 0.5 | 0.00212317 |
| P60_BAR_MOMENTUM_B5000_Q70 | BAR_MOMENTUM | prev_bar_return | sign | 5000 | 0.7 | 0.00345298 |
| P60_BAR_MOMENTUM_B5000_Q90 | BAR_MOMENTUM | prev_bar_return | sign | 5000 | 0.9 | 0.00580853 |
| P60_BAR_CONTRARIAN_B5000_Q50 | BAR_CONTRARIAN | prev_bar_return | opposite | 5000 | 0.5 | 0.00212317 |
| P60_BAR_CONTRARIAN_B5000_Q70 | BAR_CONTRARIAN | prev_bar_return | opposite | 5000 | 0.7 | 0.00345298 |
| P60_BAR_CONTRARIAN_B5000_Q90 | BAR_CONTRARIAN | prev_bar_return | opposite | 5000 | 0.9 | 0.00580853 |
| P60_BAR_IMBALANCE_B5000_Q50 | BAR_IMBALANCE | avg_l1_imbalance | sign | 5000 | 0.5 | 0.0860185 |
| P60_BAR_IMBALANCE_B5000_Q70 | BAR_IMBALANCE | avg_l1_imbalance | sign | 5000 | 0.7 | 0.21453 |
| P60_BAR_IMBALANCE_B5000_Q90 | BAR_IMBALANCE | avg_l1_imbalance | sign | 5000 | 0.9 | 0.565462 |
| P60_BAR_MICROPRICE_B5000_Q50 | BAR_MICROPRICE | avg_microprice_dev | sign | 5000 | 0.5 | 8.2227e-06 |
| P60_BAR_MICROPRICE_B5000_Q70 | BAR_MICROPRICE | avg_microprice_dev | sign | 5000 | 0.7 | 2.31786e-05 |
| P60_BAR_MICROPRICE_B5000_Q90 | BAR_MICROPRICE | avg_microprice_dev | sign | 5000 | 0.9 | 7.76804e-05 |
| P60_BAR_MOMENTUM_B10000_Q50 | BAR_MOMENTUM | prev_bar_return | sign | 10000 | 0.5 | 0.00371387 |
| P60_BAR_MOMENTUM_B10000_Q70 | BAR_MOMENTUM | prev_bar_return | sign | 10000 | 0.7 | 0.00544563 |
| P60_BAR_MOMENTUM_B10000_Q90 | BAR_MOMENTUM | prev_bar_return | sign | 10000 | 0.9 | 0.00824448 |
| P60_BAR_CONTRARIAN_B10000_Q50 | BAR_CONTRARIAN | prev_bar_return | opposite | 10000 | 0.5 | 0.00371387 |
| P60_BAR_CONTRARIAN_B10000_Q70 | BAR_CONTRARIAN | prev_bar_return | opposite | 10000 | 0.7 | 0.00544563 |
| P60_BAR_CONTRARIAN_B10000_Q90 | BAR_CONTRARIAN | prev_bar_return | opposite | 10000 | 0.9 | 0.00824448 |
| P60_BAR_IMBALANCE_B10000_Q50 | BAR_IMBALANCE | avg_l1_imbalance | sign | 10000 | 0.5 | 0.087248 |
| P60_BAR_IMBALANCE_B10000_Q70 | BAR_IMBALANCE | avg_l1_imbalance | sign | 10000 | 0.7 | 0.214845 |
| P60_BAR_IMBALANCE_B10000_Q90 | BAR_IMBALANCE | avg_l1_imbalance | sign | 10000 | 0.9 | 0.566708 |
| P60_BAR_MICROPRICE_B10000_Q50 | BAR_MICROPRICE | avg_microprice_dev | sign | 10000 | 0.5 | 9.70866e-06 |
| P60_BAR_MICROPRICE_B10000_Q70 | BAR_MICROPRICE | avg_microprice_dev | sign | 10000 | 0.7 | 2.31875e-05 |
| P60_BAR_MICROPRICE_B10000_Q90 | BAR_MICROPRICE | avg_microprice_dev | sign | 10000 | 0.9 | 7.75273e-05 |

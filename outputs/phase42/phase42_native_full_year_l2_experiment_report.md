# Phase 42 Native Full-Year Synthetic L2 Experiment

Generated UTC: 2026-07-16T14:15:02.363336+00:00

This phase builds a native 252-trading-day synthetic L2 event-state product from the existing 189-day synthetic universe, recomputes event features, and runs strategy execution directly on those event rows.
It is synthetic-only experiment evidence, not broker/paper/live acceptance.

## Overall Summary

| metric | value | description |
| --- | --- | --- |
| phase42_native_full_year_event_rows | 3.01229e+06 | Native 252-day synthetic L2 event-state rows generated |
| phase42_synthetic_year_days | 252 | Synthetic trading days generated |
| phase42_symbols | 32 | Symbols represented |
| phase42_feed_profiles | 5 | Feed profiles represented |
| phase42_strategy_profile_rows | 15 | Strategy/profile rows evaluated |
| phase42_total_strategy_trades | 6.84622e+06 | Total simulated strategy trades across profiles |
| phase42_profitable_strategy_profile_rows | 0 | Annual positive P&L rows across all profiles |
| phase42_profitable_realistic_strategy_profile_rows | 0 | Annual positive P&L rows under retail/stressed profiles |
| phase42_best_annual_net_pnl_inr | -4.33712e+06 | Best annual net P&L across all profiles |
| phase42_best_realistic_annual_net_pnl_inr | -2.21015e+07 | Best annual net P&L under retail/stressed profiles |
| phase42_sample_trade_rows | 30000 | Persisted deterministic sample trade rows |
| phase42_synthetic_full_year_acceptance_ready | 0 | Native full-year synthetic run is experiment evidence, not acceptance |

## Strategy Results

| strategy_id | execution_profile | trades | symbols | synthetic_year_days | mean_gross_return | mean_cost_return | mean_zerodha_charge_return | mean_net_return | annual_net_pnl_inr | worst_daily_net_pnl_inr | max_drawdown_inr | positive_day_fraction | annualized_sharpe_proxy | synthetic_full_year_acceptance_ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S07 | zero_latency_spread_only_control | 388607 | 9 | 252 | 3.24404e-05 | 0.000144047 | 0 | -0.000111607 | -4.33712e+06 | -76606.3 | -4.35937e+06 | 0.0538922 | -16.2718 | False |
| S09 | zero_latency_spread_only_control | 587720 | 9 | 252 | -2.0843e-05 | 0.000138869 | 0 | -0.000159712 | -9.38662e+06 | -234435 | -9.37535e+06 | 0.047619 | -17.3184 | False |
| S05 | zero_latency_spread_only_control | 587504 | 16 | 252 | -2.98319e-05 | 0.000171563 | 0 | -0.000201395 | -1.18321e+07 | -574887 | -1.1834e+07 | 0.134921 | -9.87298 | False |
| S01 | retail_marketable_default | 221610 | 30 | 252 | 9.75873e-05 | 0.0010949 | 0.000826813 | -0.000997314 | -2.21015e+07 | -336957 | -2.20183e+07 | 0.0119048 | -18.8393 | False |
| S02 | zero_latency_spread_only_control | 585487 | 32 | 252 | -0.000298613 | 0.000158226 | 0 | -0.000456839 | -2.67473e+07 | -1.48569e+06 | -2.66424e+07 | 0.165975 | -7.88645 | False |
| S01 | zero_latency_spread_only_control | 236828 | 30 | 252 | -0.00101686 | 0.000132344 | 0 | -0.00114921 | -2.72165e+07 | -493523 | -2.71475e+07 | 0.0238095 | -17.0842 | False |
| S01 | stressed_retail | 213588 | 30 | 252 | 5.47072e-05 | 0.00133065 | 0.00082681 | -0.00127594 | -2.72526e+07 | -460577 | -2.71887e+07 | 0.00396825 | -18.3655 | False |
| S07 | retail_marketable_default | 370332 | 9 | 252 | 1.92691e-05 | 0.0011305 | 0.00082681 | -0.00111123 | -4.11525e+07 | -326079 | -4.0867e+07 | 0 | -156.667 | False |
| S07 | stressed_retail | 359950 | 9 | 252 | 2.57721e-05 | 0.00139031 | 0.000826809 | -0.00136454 | -4.91165e+07 | -371748 | -4.88034e+07 | 0 | -174.491 | False |
| S02 | retail_marketable_default | 552886 | 32 | 252 | 3.65404e-06 | 0.00110846 | 0.000826809 | -0.0011048 | -6.1083e+07 | -1.16537e+06 | -6.08579e+07 | 0.00829876 | -15.9342 | False |
| S09 | retail_marketable_default | 560616 | 9 | 252 | -7.96414e-06 | 0.00112533 | 0.000826811 | -0.00113329 | -6.3534e+07 | -474320 | -6.32945e+07 | 0 | -128.307 | False |
| S05 | retail_marketable_default | 560295 | 16 | 252 | -3.48302e-05 | 0.00116974 | 0.000826811 | -0.00120457 | -6.74916e+07 | -1.00801e+06 | -6.73108e+07 | 0 | -37.4287 | False |
| S02 | stressed_retail | 531419 | 32 | 252 | -1.3618e-05 | 0.00133221 | 0.000826809 | -0.00134583 | -7.152e+07 | -1.46148e+06 | -7.13333e+07 | 0 | -16.0834 | False |
| S09 | stressed_retail | 544871 | 9 | 252 | -1.2825e-05 | 0.0013851 | 0.000826811 | -0.00139792 | -7.61688e+07 | -534863 | -7.58878e+07 | 0 | -141.821 | False |
| S05 | stressed_retail | 544508 | 16 | 252 | -4.09866e-05 | 0.00144134 | 0.00082681 | -0.00148232 | -8.07137e+07 | -1.103e+06 | -8.04905e+07 | 0 | -41.3542 | False |

## Top Realistic Results

| strategy_id | execution_profile | trades | symbols | synthetic_year_days | mean_gross_return | mean_cost_return | mean_zerodha_charge_return | mean_net_return | annual_net_pnl_inr | worst_daily_net_pnl_inr | max_drawdown_inr | positive_day_fraction | annualized_sharpe_proxy | synthetic_full_year_acceptance_ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | retail_marketable_default | 221610 | 30 | 252 | 9.75873e-05 | 0.0010949 | 0.000826813 | -0.000997314 | -2.21015e+07 | -336957 | -2.20183e+07 | 0.0119048 | -18.8393 | False |
| S01 | stressed_retail | 213588 | 30 | 252 | 5.47072e-05 | 0.00133065 | 0.00082681 | -0.00127594 | -2.72526e+07 | -460577 | -2.71887e+07 | 0.00396825 | -18.3655 | False |
| S07 | retail_marketable_default | 370332 | 9 | 252 | 1.92691e-05 | 0.0011305 | 0.00082681 | -0.00111123 | -4.11525e+07 | -326079 | -4.0867e+07 | 0 | -156.667 | False |
| S07 | stressed_retail | 359950 | 9 | 252 | 2.57721e-05 | 0.00139031 | 0.000826809 | -0.00136454 | -4.91165e+07 | -371748 | -4.88034e+07 | 0 | -174.491 | False |
| S02 | retail_marketable_default | 552886 | 32 | 252 | 3.65404e-06 | 0.00110846 | 0.000826809 | -0.0011048 | -6.1083e+07 | -1.16537e+06 | -6.08579e+07 | 0.00829876 | -15.9342 | False |
| S09 | retail_marketable_default | 560616 | 9 | 252 | -7.96414e-06 | 0.00112533 | 0.000826811 | -0.00113329 | -6.3534e+07 | -474320 | -6.32945e+07 | 0 | -128.307 | False |
| S05 | retail_marketable_default | 560295 | 16 | 252 | -3.48302e-05 | 0.00116974 | 0.000826811 | -0.00120457 | -6.74916e+07 | -1.00801e+06 | -6.73108e+07 | 0 | -37.4287 | False |
| S02 | stressed_retail | 531419 | 32 | 252 | -1.3618e-05 | 0.00133221 | 0.000826809 | -0.00134583 | -7.152e+07 | -1.46148e+06 | -7.13333e+07 | 0 | -16.0834 | False |
| S09 | stressed_retail | 544871 | 9 | 252 | -1.2825e-05 | 0.0013851 | 0.000826811 | -0.00139792 | -7.61688e+07 | -534863 | -7.58878e+07 | 0 | -141.821 | False |
| S05 | stressed_retail | 544508 | 16 | 252 | -4.09866e-05 | 0.00144134 | 0.00082681 | -0.00148232 | -8.07137e+07 | -1.103e+06 | -8.04905e+07 | 0 | -41.3542 | False |

## Daily PnL Sample

| synthetic_year_day | daily_net_pnl_inr | daily_trades | running_net_pnl_inr | running_peak_inr | drawdown_inr | strategy_id | execution_profile |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | -68988.6 | 888 | -68988.6 | -68988.6 | 0 | S01 | zero_latency_spread_only_control |
| 2 | -150466 | 778 | -219455 | -68988.6 | -150466 | S01 | zero_latency_spread_only_control |
| 3 | -9196.87 | 35 | -228652 | -68988.6 | -159663 | S01 | zero_latency_spread_only_control |
| 4 | -65422.2 | 521 | -294074 | -68988.6 | -225085 | S01 | zero_latency_spread_only_control |
| 5 | -381923 | 1449 | -675997 | -68988.6 | -607009 | S01 | zero_latency_spread_only_control |
| 6 | -172403 | 2215 | -848401 | -68988.6 | -779412 | S01 | zero_latency_spread_only_control |
| 7 | -32778.7 | 118 | -881179 | -68988.6 | -812191 | S01 | zero_latency_spread_only_control |
| 8 | -38699.8 | 552 | -919879 | -68988.6 | -850890 | S01 | zero_latency_spread_only_control |
| 9 | -104215 | 666 | -1.02409e+06 | -68988.6 | -955106 | S01 | zero_latency_spread_only_control |
| 10 | 9816.48 | 1441 | -1.01428e+06 | -68988.6 | -945289 | S01 | zero_latency_spread_only_control |
| 11 | -54066.4 | 1336 | -1.06834e+06 | -68988.6 | -999356 | S01 | zero_latency_spread_only_control |
| 12 | -133034 | 2095 | -1.20138e+06 | -68988.6 | -1.13239e+06 | S01 | zero_latency_spread_only_control |
| 13 | -13882.1 | 72 | -1.21526e+06 | -68988.6 | -1.14627e+06 | S01 | zero_latency_spread_only_control |
| 14 | -177223 | 985 | -1.39248e+06 | -68988.6 | -1.3235e+06 | S01 | zero_latency_spread_only_control |
| 15 | -11696.7 | 66 | -1.40418e+06 | -68988.6 | -1.33519e+06 | S01 | zero_latency_spread_only_control |
| 16 | -178593 | 1923 | -1.58277e+06 | -68988.6 | -1.51378e+06 | S01 | zero_latency_spread_only_control |
| 17 | -2815.53 | 34 | -1.58559e+06 | -68988.6 | -1.5166e+06 | S01 | zero_latency_spread_only_control |
| 18 | -31103.5 | 293 | -1.61669e+06 | -68988.6 | -1.5477e+06 | S01 | zero_latency_spread_only_control |
| 19 | -19927.1 | 119 | -1.63662e+06 | -68988.6 | -1.56763e+06 | S01 | zero_latency_spread_only_control |
| 20 | -119091 | 1221 | -1.75571e+06 | -68988.6 | -1.68672e+06 | S01 | zero_latency_spread_only_control |
| 21 | 2209.39 | 294 | -1.7535e+06 | -68988.6 | -1.68451e+06 | S01 | zero_latency_spread_only_control |
| 22 | -220671 | 1302 | -1.97417e+06 | -68988.6 | -1.90518e+06 | S01 | zero_latency_spread_only_control |
| 23 | -101010 | 773 | -2.07518e+06 | -68988.6 | -2.00619e+06 | S01 | zero_latency_spread_only_control |
| 24 | -43898.7 | 330 | -2.11908e+06 | -68988.6 | -2.05009e+06 | S01 | zero_latency_spread_only_control |
| 25 | -225060 | 2032 | -2.34414e+06 | -68988.6 | -2.27515e+06 | S01 | zero_latency_spread_only_control |
| 26 | -151739 | 1008 | -2.49588e+06 | -68988.6 | -2.42689e+06 | S01 | zero_latency_spread_only_control |
| 27 | -28587.8 | 906 | -2.52447e+06 | -68988.6 | -2.45548e+06 | S01 | zero_latency_spread_only_control |
| 28 | -127647 | 2093 | -2.65211e+06 | -68988.6 | -2.58313e+06 | S01 | zero_latency_spread_only_control |
| 29 | -33752.8 | 593 | -2.68587e+06 | -68988.6 | -2.61688e+06 | S01 | zero_latency_spread_only_control |
| 30 | -75846.3 | 701 | -2.76171e+06 | -68988.6 | -2.69273e+06 | S01 | zero_latency_spread_only_control |
| 31 | -3800.42 | 17 | -2.76551e+06 | -68988.6 | -2.69653e+06 | S01 | zero_latency_spread_only_control |
| 32 | -139165 | 1621 | -2.90468e+06 | -68988.6 | -2.83569e+06 | S01 | zero_latency_spread_only_control |
| 33 | -200780 | 1487 | -3.10546e+06 | -68988.6 | -3.03647e+06 | S01 | zero_latency_spread_only_control |
| 34 | -207102 | 1087 | -3.31256e+06 | -68988.6 | -3.24357e+06 | S01 | zero_latency_spread_only_control |
| 35 | -6849.96 | 62 | -3.31941e+06 | -68988.6 | -3.25042e+06 | S01 | zero_latency_spread_only_control |
| 36 | -385662 | 2164 | -3.70507e+06 | -68988.6 | -3.63609e+06 | S01 | zero_latency_spread_only_control |
| 37 | -73896.8 | 418 | -3.77897e+06 | -68988.6 | -3.70998e+06 | S01 | zero_latency_spread_only_control |
| 38 | -75194.1 | 371 | -3.85416e+06 | -68988.6 | -3.78518e+06 | S01 | zero_latency_spread_only_control |
| 39 | -53757.2 | 308 | -3.90792e+06 | -68988.6 | -3.83893e+06 | S01 | zero_latency_spread_only_control |
| 40 | -43650.2 | 262 | -3.95157e+06 | -68988.6 | -3.88258e+06 | S01 | zero_latency_spread_only_control |
| 41 | -116517 | 593 | -4.06809e+06 | -68988.6 | -3.9991e+06 | S01 | zero_latency_spread_only_control |
| 42 | -119410 | 1477 | -4.1875e+06 | -68988.6 | -4.11851e+06 | S01 | zero_latency_spread_only_control |
| 43 | -56484.3 | 982 | -4.24398e+06 | -68988.6 | -4.175e+06 | S01 | zero_latency_spread_only_control |
| 44 | -184250 | 1580 | -4.42823e+06 | -68988.6 | -4.35924e+06 | S01 | zero_latency_spread_only_control |
| 45 | -57819.3 | 1592 | -4.48605e+06 | -68988.6 | -4.41706e+06 | S01 | zero_latency_spread_only_control |
| 46 | -6041.13 | 44 | -4.49209e+06 | -68988.6 | -4.42311e+06 | S01 | zero_latency_spread_only_control |
| 47 | -224891 | 1616 | -4.71698e+06 | -68988.6 | -4.648e+06 | S01 | zero_latency_spread_only_control |
| 48 | -79102.3 | 812 | -4.79609e+06 | -68988.6 | -4.7271e+06 | S01 | zero_latency_spread_only_control |
| 49 | -51658.3 | 1034 | -4.84775e+06 | -68988.6 | -4.77876e+06 | S01 | zero_latency_spread_only_control |
| 50 | -58656.6 | 362 | -4.9064e+06 | -68988.6 | -4.83741e+06 | S01 | zero_latency_spread_only_control |
| 51 | -123231 | 497 | -5.02963e+06 | -68988.6 | -4.96064e+06 | S01 | zero_latency_spread_only_control |
| 52 | -169551 | 1443 | -5.19918e+06 | -68988.6 | -5.1302e+06 | S01 | zero_latency_spread_only_control |
| 53 | -435.269 | 3 | -5.19962e+06 | -68988.6 | -5.13063e+06 | S01 | zero_latency_spread_only_control |
| 54 | -34451.9 | 620 | -5.23407e+06 | -68988.6 | -5.16508e+06 | S01 | zero_latency_spread_only_control |
| 55 | -54518.9 | 375 | -5.28859e+06 | -68988.6 | -5.2196e+06 | S01 | zero_latency_spread_only_control |
| 56 | -57470.6 | 465 | -5.34606e+06 | -68988.6 | -5.27707e+06 | S01 | zero_latency_spread_only_control |
| 57 | -110091 | 1077 | -5.45615e+06 | -68988.6 | -5.38716e+06 | S01 | zero_latency_spread_only_control |
| 58 | -2805.01 | 17 | -5.45896e+06 | -68988.6 | -5.38997e+06 | S01 | zero_latency_spread_only_control |
| 59 | -45368.7 | 460 | -5.50432e+06 | -68988.6 | -5.43534e+06 | S01 | zero_latency_spread_only_control |
| 60 | -124361 | 883 | -5.62869e+06 | -68988.6 | -5.5597e+06 | S01 | zero_latency_spread_only_control |

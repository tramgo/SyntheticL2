# Phase154 Full-partition Real Cadence Anchor

Generated UTC: 2026-07-23T09:39:56.170115+00:00

Phase154 recomputes real-anchor received-cadence profiles from full local Parquet partitions using DuckDB.
It replaces sampled-file cadence anchors for calibration diagnostics. It does not contact Azure, generate signals, compute fills, run P&L, or unlock strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase154_catalog_db_exists | 1 | Phase150 DuckDB catalog database exists locally |
| phase154_partitions_selected | 96 | Date/symbol partitions selected for full-partition cadence profiling |
| phase154_partition_profiles_completed | 96 | Partition cadence profiles completed |
| phase154_failed_partition_profiles | 0 | Partition cadence profiles failed |
| phase154_trade_dates_profiled | 3 | Trade dates profiled |
| phase154_symbols_profiled | 32 | Symbols profiled |
| phase154_total_rows_profiled | 1238275 | Tick/update rows profiled |
| phase154_total_elapsed_seconds | 561.827 | Total elapsed seconds across partition cadence profiles |
| phase154_max_partition_elapsed_seconds | 22.3616 | Slowest partition cadence profile elapsed seconds |
| phase154_median_symbol_ticks_per_second | 0.791127 | Median symbol-level tick/update rate across full partitions |
| phase154_median_symbol_p95_gap_ms | 4908.7 | Median symbol-level p95 inter-update gap |
| phase154_max_symbol_p95_gap_ms | 7565.7 | Maximum symbol-level p95 inter-update gap |
| phase154_sample_bias_flag_rows | 42 | Phase106 sampled-file cadence rows outside sampled/full comparison bands |
| phase154_strategy_replay_allowed | 0 | Cadence anchor profiling does not unlock strategy replay |
| phase154_next_best_action | use_phase154_full_partition_cadence_anchors_for_generator_calibration_contract | Recommended next milestone |

## Date Cadence Anchor

| trade_date | exchange | symbols | rows | median_symbol_ticks_per_second | min_symbol_ticks_per_second | max_symbol_ticks_per_second | median_symbol_gap_ms | max_symbol_p95_gap_ms | median_gap_le_1s_fraction | max_gap_gt_5s_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-08 | NSE | 32 | 226430 | 0.744352 | 0.270623 | 1.60612 | 750 | 7565.7 | 0.69771 | 0.284034 |
| 2026-07-09 | NSE | 32 | 390992 | 1.01036 | 0.36957 | 1.60342 | 740 | 6911.05 | 0.764197 | 0.1599 |
| 2026-07-13 | NSE | 32 | 620853 | 0.820932 | 0.368191 | 1.60122 | 749.5 | 7000.8 | 0.710207 | 0.171613 |

## Symbol Cadence Anchor

| exchange | symbol | trade_dates | rows | gap_rows | median_ticks_per_second | min_ticks_per_second | max_ticks_per_second | median_gap_ms | median_p95_gap_ms | max_p95_gap_ms | median_gap_le_1s_fraction | max_gap_gt_5s_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NSE | ADANIPORTS | 3 | 27481 | 27478 | 0.611978 | 0.608848 | 0.632754 | 1000 | 5500 | 5750 | 0.546345 | 0.0744444 |
| NSE | AXISBANK | 3 | 43257 | 43254 | 1.05634 | 0.803904 | 1.28446 | 501 | 4380.75 | 4913.65 | 0.773267 | 0.0458816 |
| NSE | BAJAJ-AUTO | 3 | 36720 | 36717 | 0.544953 | 0.513967 | 1.10386 | 1000 | 5939.25 | 6309 | 0.536706 | 0.10219 |
| NSE | BANKBEES | 3 | 41253 | 41250 | 1.0177 | 0.83796 | 1.04164 | 999 | 4450 | 4833 | 0.769716 | 0.0396511 |
| NSE | BHARTIARTL | 3 | 46148 | 46145 | 0.857632 | 0.741167 | 1.55351 | 749 | 4762.4 | 5455.2 | 0.708779 | 0.0599969 |
| NSE | BPCL | 3 | 20739 | 20736 | 0.469109 | 0.430168 | 0.484334 | 1635.5 | 6081.7 | 6750.95 | 0.392118 | 0.131148 |
| NSE | BRITANNIA | 3 | 16325 | 16322 | 0.374337 | 0.270623 | 0.418364 | 2000 | 7000.8 | 7565.7 | 0.345689 | 0.284034 |
| NSE | CIPLA | 3 | 22213 | 22210 | 0.511422 | 0.443813 | 0.513215 | 1378 | 5953.9 | 6747.95 | 0.438237 | 0.13224 |
| NSE | DRREDDY | 3 | 34854 | 34851 | 0.538172 | 0.428645 | 1.45642 | 1250 | 5750 | 6750 | 0.461243 | 0.138551 |
| NSE | GOLDBEES | 3 | 29870 | 29867 | 0.747537 | 0.57515 | 0.797371 | 750 | 5250 | 5680 | 0.667216 | 0.0802712 |
| NSE | HCLTECH | 3 | 40610 | 40607 | 0.622566 | 0.37403 | 1.28499 | 1000 | 5324.85 | 7000 | 0.520642 | 0.156667 |
| NSE | HDFCBANK | 3 | 70803 | 70800 | 1.60342 | 1.57887 | 1.60612 | 500 | 1250 | 1250 | 0.921965 | 0.00589577 |
| NSE | HINDUNILVR | 3 | 29461 | 29458 | 0.577162 | 0.534487 | 0.945193 | 1000 | 5859.45 | 5997.2 | 0.5779 | 0.0905357 |
| NSE | ICICIBANK | 3 | 58334 | 58331 | 1.42608 | 1.16241 | 1.49492 | 500 | 3403 | 4201.4 | 0.896955 | 0.0200582 |
| NSE | INFY | 3 | 58214 | 58211 | 1.09783 | 1.08717 | 1.51529 | 500 | 3922.15 | 4344.8 | 0.829054 | 0.0222613 |
| NSE | ITBEES | 3 | 18963 | 18960 | 0.36957 | 0.306924 | 0.508645 | 2001 | 6911.05 | 7230.15 | 0.306614 | 0.210585 |
| NSE | ITC | 3 | 32733 | 32730 | 0.822439 | 0.543529 | 1.01539 | 749 | 4815.4 | 5750 | 0.727574 | 0.0858782 |
| NSE | JUNIORBEES | 3 | 38437 | 38434 | 0.933484 | 0.772736 | 0.989387 | 999 | 4511 | 5021 | 0.760716 | 0.0517172 |
| NSE | KOTAKBANK | 3 | 42075 | 42072 | 1.06033 | 0.618702 | 1.44398 | 500 | 4051.3 | 5475.55 | 0.833298 | 0.0704755 |
| NSE | LT | 3 | 50307 | 50304 | 1.40131 | 0.8547 | 1.43292 | 500 | 3367 | 4750 | 0.885798 | 0.0394041 |
| NSE | M&M | 3 | 51233 | 51230 | 1.1268 | 1.10136 | 1.28469 | 501 | 4285.45 | 4380.55 | 0.825434 | 0.0219255 |
| NSE | MARUTI | 3 | 48890 | 48887 | 1.00533 | 0.938485 | 1.21383 | 683 | 4212 | 4508 | 0.774621 | 0.027951 |
| NSE | NESTLEIND | 3 | 22657 | 22654 | 0.456223 | 0.43567 | 0.56717 | 1251 | 6232.4 | 6750 | 0.437565 | 0.130853 |
| NSE | NIFTYBEES | 3 | 44715 | 44712 | 1.02395 | 0.993022 | 1.02876 | 749 | 4467.05 | 4542 | 0.790702 | 0.0289564 |
| NSE | ONGC | 3 | 32786 | 32783 | 0.759816 | 0.675666 | 0.767427 | 750 | 5002 | 5206.15 | 0.663951 | 0.0582035 |
| NSE | RELIANCE | 3 | 58141 | 58138 | 1.45536 | 1.14409 | 1.51042 | 500 | 2999 | 4324 | 0.890378 | 0.0236039 |
| NSE | SBIN | 3 | 50664 | 50661 | 1.1835 | 1.08575 | 1.20194 | 500 | 4257.7 | 4329 | 0.825014 | 0.0247098 |
| NSE | SUNPHARMA | 3 | 32921 | 32918 | 0.64149 | 0.552725 | 1.04094 | 982 | 5484 | 6110.5 | 0.600041 | 0.0972851 |
| NSE | TCS | 3 | 57870 | 57867 | 1.18181 | 0.6973 | 1.60122 | 500 | 4250.7 | 5251 | 0.819414 | 0.0583632 |
| NSE | TECHM | 3 | 29591 | 29588 | 0.536466 | 0.401899 | 0.839689 | 1238.5 | 5806.1 | 6778.5 | 0.471861 | 0.151061 |
| NSE | ULTRACEMCO | 3 | 17353 | 17350 | 0.387798 | 0.368191 | 0.44975 | 2000 | 6772.6 | 6863.8 | 0.31124 | 0.170066 |
| NSE | WIPRO | 3 | 32657 | 32654 | 0.709104 | 0.359391 | 0.892817 | 751 | 5142.2 | 7000 | 0.601747 | 0.173996 |

## Phase106 Sample Bias Audit

| symbol | trade_date | metric | phase154_full_partition_value | phase106_sampled_files_value | sampled_to_full_ratio | sample_bias_flag |
| --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | 2026-07-13 | median_gap_ms | 1000 | 1000 | 1 | within_band |
| ADANIPORTS | 2026-07-13 | p90_gap_ms | 4556.6 | 439477 | 96.4484 | sampled_high_vs_full |
| ADANIPORTS | 2026-07-13 | p95_gap_ms | 5500 | 451864 | 82.1572 | sampled_high_vs_full |
| ADANIPORTS | 2026-07-13 | gap_le_1s_fraction | 0.546345 | 0.541176 | 0.99054 | within_band |
| AXISBANK | 2026-07-13 | median_gap_ms | 749 | 750 | 1.00134 | within_band |
| AXISBANK | 2026-07-13 | p90_gap_ms | 3877.3 | 305453 | 78.7797 | sampled_high_vs_full |
| AXISBANK | 2026-07-13 | p95_gap_ms | 4913.65 | 450681 | 91.7203 | sampled_high_vs_full |
| AXISBANK | 2026-07-13 | gap_le_1s_fraction | 0.697455 | 0.621053 | 0.890456 | within_band |
| BAJAJ-AUTO | 2026-07-13 | median_gap_ms | 741 | 500 | 0.674764 | within_band |
| BAJAJ-AUTO | 2026-07-13 | p90_gap_ms | 1251 | 1250 | 0.999201 | within_band |
| BAJAJ-AUTO | 2026-07-13 | p95_gap_ms | 4410.05 | 439771 | 99.7202 | sampled_high_vs_full |
| BAJAJ-AUTO | 2026-07-13 | gap_le_1s_fraction | 0.826492 | 0.847001 | 1.02482 | within_band |
| BANKBEES | 2026-07-13 | median_gap_ms | 1000 | 1000 | 1 | within_band |
| BANKBEES | 2026-07-13 | p90_gap_ms | 3909.6 | 2351.6 | 0.601494 | within_band |
| BANKBEES | 2026-07-13 | p95_gap_ms | 4833 | 446695 | 92.4259 | sampled_high_vs_full |
| BANKBEES | 2026-07-13 | gap_le_1s_fraction | 0.734021 | 0.741935 | 1.01078 | within_band |
| BHARTIARTL | 2026-07-13 | median_gap_ms | 749 | 750 | 1.00134 | within_band |
| BHARTIARTL | 2026-07-13 | p90_gap_ms | 3250 | 3949.1 | 1.21511 | within_band |
| BHARTIARTL | 2026-07-13 | p95_gap_ms | 4762.4 | 449395 | 94.3631 | sampled_high_vs_full |
| BHARTIARTL | 2026-07-13 | gap_le_1s_fraction | 0.708779 | 0.675875 | 0.953577 | within_band |
| BPCL | 2026-07-13 | median_gap_ms | 1602 | 1750 | 1.09238 | within_band |
| BPCL | 2026-07-13 | p90_gap_ms | 5239.4 | 448824 | 85.6632 | sampled_high_vs_full |
| BPCL | 2026-07-13 | p95_gap_ms | 6081.7 | 454186 | 74.6807 | sampled_high_vs_full |
| BPCL | 2026-07-13 | gap_le_1s_fraction | 0.392118 | 0.374593 | 0.955306 | within_band |
| BRITANNIA | 2026-07-13 | median_gap_ms | 2000 | 1750 | 0.875 | within_band |
| BRITANNIA | 2026-07-13 | p90_gap_ms | 5923 | 450023 | 75.9789 | sampled_high_vs_full |
| BRITANNIA | 2026-07-13 | p95_gap_ms | 7000.8 | 455515 | 65.0662 | sampled_high_vs_full |
| BRITANNIA | 2026-07-13 | gap_le_1s_fraction | 0.345689 | 0.405109 | 1.17189 | within_band |
| CIPLA | 2026-07-13 | median_gap_ms | 1194 | 1500 | 1.25628 | within_band |
| CIPLA | 2026-07-13 | p90_gap_ms | 5000 | 447132 | 89.4263 | sampled_high_vs_full |
| CIPLA | 2026-07-13 | p95_gap_ms | 5953.9 | 453908 | 76.2372 | sampled_high_vs_full |
| CIPLA | 2026-07-13 | gap_le_1s_fraction | 0.47595 | 0.417957 | 0.878153 | within_band |
| DRREDDY | 2026-07-13 | median_gap_ms | 1250 | 1749 | 1.3992 | within_band |
| DRREDDY | 2026-07-13 | p90_gap_ms | 4792.5 | 446827 | 93.2346 | sampled_high_vs_full |
| DRREDDY | 2026-07-13 | p95_gap_ms | 5750 | 453890 | 78.9374 | sampled_high_vs_full |
| DRREDDY | 2026-07-13 | gap_le_1s_fraction | 0.461243 | 0.368098 | 0.798056 | within_band |
| GOLDBEES | 2026-07-13 | median_gap_ms | 1000 | 1000 | 1 | within_band |
| GOLDBEES | 2026-07-13 | p90_gap_ms | 4700 | 439314 | 93.4711 | sampled_high_vs_full |
| GOLDBEES | 2026-07-13 | p95_gap_ms | 5680 | 451649 | 79.5156 | sampled_high_vs_full |
| GOLDBEES | 2026-07-13 | gap_le_1s_fraction | 0.508589 | 0.51 | 1.00277 | within_band |
| HCLTECH | 2026-07-13 | median_gap_ms | 500 | 500 | 1 | within_band |
| HCLTECH | 2026-07-13 | p90_gap_ms | 1250 | 1214.8 | 0.97184 | within_band |
| HCLTECH | 2026-07-13 | p95_gap_ms | 4158.8 | 437736 | 105.255 | sampled_high_vs_full |
| HCLTECH | 2026-07-13 | gap_le_1s_fraction | 0.874492 | 0.872437 | 0.997651 | within_band |
| HDFCBANK | 2026-07-13 | median_gap_ms | 500 | 499 | 0.998 | within_band |
| HDFCBANK | 2026-07-13 | p90_gap_ms | 1000 | 1000 | 1 | within_band |
| HDFCBANK | 2026-07-13 | p95_gap_ms | 1250 | 1250 | 1 | within_band |
| HDFCBANK | 2026-07-13 | gap_le_1s_fraction | 0.921965 | 0.91921 | 0.997012 | within_band |
| HINDUNILVR | 2026-07-13 | median_gap_ms | 1001 | 1000 | 0.999001 | within_band |
| HINDUNILVR | 2026-07-13 | p90_gap_ms | 4910.6 | 442440 | 90.099 | sampled_high_vs_full |
| HINDUNILVR | 2026-07-13 | p95_gap_ms | 5859.45 | 451842 | 77.1133 | sampled_high_vs_full |
| HINDUNILVR | 2026-07-13 | gap_le_1s_fraction | 0.496139 | 0.515544 | 1.03911 | within_band |
| ICICIBANK | 2026-07-13 | median_gap_ms | 500 | 500 | 1 | within_band |
| ICICIBANK | 2026-07-13 | p90_gap_ms | 2000 | 2000 | 1 | within_band |
| ICICIBANK | 2026-07-13 | p95_gap_ms | 4201.4 | 439902 | 104.704 | sampled_high_vs_full |
| ICICIBANK | 2026-07-13 | gap_le_1s_fraction | 0.828844 | 0.818296 | 0.987273 | within_band |
| INFY | 2026-07-13 | median_gap_ms | 500 | 500 | 1 | within_band |
| INFY | 2026-07-13 | p90_gap_ms | 1000 | 1000 | 1 | within_band |
| INFY | 2026-07-13 | p95_gap_ms | 2627.1 | 1775 | 0.67565 | within_band |
| INFY | 2026-07-13 | gap_le_1s_fraction | 0.912199 | 0.909519 | 0.997062 | within_band |
| ITBEES | 2026-07-13 | median_gap_ms | 1250 | 1250 | 1 | within_band |
| ITBEES | 2026-07-13 | p90_gap_ms | 5000 | 446258 | 89.2515 | sampled_high_vs_full |
| ITBEES | 2026-07-13 | p95_gap_ms | 5993 | 452908 | 75.5728 | sampled_high_vs_full |
| ITBEES | 2026-07-13 | gap_le_1s_fraction | 0.45993 | 0.442529 | 0.962165 | within_band |
| ITC | 2026-07-13 | median_gap_ms | 1250 | 1254.5 | 1.0036 | within_band |
| ITC | 2026-07-13 | p90_gap_ms | 4782.3 | 443821 | 92.8049 | sampled_high_vs_full |
| ITC | 2026-07-13 | p95_gap_ms | 5750 | 452335 | 78.6669 | sampled_high_vs_full |
| ITC | 2026-07-13 | gap_le_1s_fraction | 0.468412 | 0.447154 | 0.954618 | within_band |
| JUNIORBEES | 2026-07-13 | median_gap_ms | 999 | 999 | 1 | within_band |
| JUNIORBEES | 2026-07-13 | p90_gap_ms | 4251 | 4750 | 1.11738 | within_band |
| JUNIORBEES | 2026-07-13 | p95_gap_ms | 5021 | 450119 | 89.6474 | sampled_high_vs_full |
| JUNIORBEES | 2026-07-13 | gap_le_1s_fraction | 0.714925 | 0.702857 | 0.983121 | within_band |
| KOTAKBANK | 2026-07-13 | median_gap_ms | 1000 | 750 | 0.75 | within_band |
| KOTAKBANK | 2026-07-13 | p90_gap_ms | 4514.1 | 6375 | 1.41224 | within_band |
| KOTAKBANK | 2026-07-13 | p95_gap_ms | 5475.55 | 450484 | 82.2719 | sampled_high_vs_full |
| KOTAKBANK | 2026-07-13 | gap_le_1s_fraction | 0.562952 | 0.640657 | 1.13803 | within_band |
| LT | 2026-07-13 | median_gap_ms | 749 | 749 | 1 | within_band |
| LT | 2026-07-13 | p90_gap_ms | 3430.8 | 3750.7 | 1.09324 | within_band |
| LT | 2026-07-13 | p95_gap_ms | 4750 | 448220 | 94.3621 | sampled_high_vs_full |
| LT | 2026-07-13 | gap_le_1s_fraction | 0.711636 | 0.710924 | 0.999 | within_band |

## Profile Timing Ledger

| trade_date | exchange | symbol | status | elapsed_seconds | error |
| --- | --- | --- | --- | --- | --- |
| 2026-07-08 | NSE | ADANIPORTS | completed | 0.322952 |  |
| 2026-07-08 | NSE | AXISBANK | completed | 0.280412 |  |
| 2026-07-08 | NSE | BAJAJ-AUTO | completed | 0.264408 |  |
| 2026-07-08 | NSE | BANKBEES | completed | 0.274475 |  |
| 2026-07-08 | NSE | BHARTIARTL | completed | 0.293998 |  |
| 2026-07-08 | NSE | BPCL | completed | 0.296182 |  |
| 2026-07-08 | NSE | BRITANNIA | completed | 0.321356 |  |
| 2026-07-08 | NSE | CIPLA | completed | 0.33978 |  |
| 2026-07-08 | NSE | DRREDDY | completed | 0.355478 |  |
| 2026-07-08 | NSE | GOLDBEES | completed | 0.363165 |  |
| 2026-07-08 | NSE | HCLTECH | completed | 0.377108 |  |
| 2026-07-08 | NSE | HDFCBANK | completed | 0.426245 |  |
| 2026-07-08 | NSE | HINDUNILVR | completed | 0.424383 |  |
| 2026-07-08 | NSE | ICICIBANK | completed | 0.45315 |  |
| 2026-07-08 | NSE | INFY | completed | 0.460394 |  |
| 2026-07-08 | NSE | ITBEES | completed | 0.533401 |  |
| 2026-07-08 | NSE | ITC | completed | 0.487583 |  |
| 2026-07-08 | NSE | JUNIORBEES | completed | 0.550757 |  |
| 2026-07-08 | NSE | KOTAKBANK | completed | 0.575205 |  |
| 2026-07-08 | NSE | LT | completed | 0.642978 |  |
| 2026-07-08 | NSE | M&M | completed | 0.727429 |  |
| 2026-07-08 | NSE | MARUTI | completed | 0.681737 |  |
| 2026-07-08 | NSE | NESTLEIND | completed | 0.663075 |  |
| 2026-07-08 | NSE | NIFTYBEES | completed | 0.82637 |  |
| 2026-07-08 | NSE | ONGC | completed | 0.812476 |  |
| 2026-07-08 | NSE | RELIANCE | completed | 0.942329 |  |
| 2026-07-08 | NSE | SBIN | completed | 0.951293 |  |
| 2026-07-08 | NSE | SUNPHARMA | completed | 0.986952 |  |
| 2026-07-08 | NSE | TCS | completed | 1.1101 |  |
| 2026-07-08 | NSE | TECHM | completed | 1.04932 |  |
| 2026-07-08 | NSE | ULTRACEMCO | completed | 0.963542 |  |
| 2026-07-08 | NSE | WIPRO | completed | 1.18173 |  |
| 2026-07-09 | NSE | ADANIPORTS | completed | 1.53466 |  |
| 2026-07-09 | NSE | AXISBANK | completed | 1.93313 |  |
| 2026-07-09 | NSE | BAJAJ-AUTO | completed | 2.15158 |  |
| 2026-07-09 | NSE | BANKBEES | completed | 2.0377 |  |
| 2026-07-09 | NSE | BHARTIARTL | completed | 2.16715 |  |
| 2026-07-09 | NSE | BPCL | completed | 2.44805 |  |
| 2026-07-09 | NSE | BRITANNIA | completed | 2.40982 |  |
| 2026-07-09 | NSE | CIPLA | completed | 2.40099 |  |
| 2026-07-09 | NSE | DRREDDY | completed | 2.42993 |  |
| 2026-07-09 | NSE | GOLDBEES | completed | 2.69052 |  |
| 2026-07-09 | NSE | HCLTECH | completed | 2.89201 |  |
| 2026-07-09 | NSE | HDFCBANK | completed | 3.25402 |  |
| 2026-07-09 | NSE | HINDUNILVR | completed | 2.42421 |  |
| 2026-07-09 | NSE | ICICIBANK | completed | 2.8513 |  |
| 2026-07-09 | NSE | INFY | completed | 3.31669 |  |
| 2026-07-09 | NSE | ITBEES | completed | 2.97653 |  |
| 2026-07-09 | NSE | ITC | completed | 3.50096 |  |
| 2026-07-09 | NSE | JUNIORBEES | completed | 3.18461 |  |
| 2026-07-09 | NSE | KOTAKBANK | completed | 3.28833 |  |
| 2026-07-09 | NSE | LT | completed | 3.40251 |  |
| 2026-07-09 | NSE | M&M | completed | 2.97381 |  |
| 2026-07-09 | NSE | MARUTI | completed | 2.97083 |  |
| 2026-07-09 | NSE | NESTLEIND | completed | 3.29138 |  |
| 2026-07-09 | NSE | NIFTYBEES | completed | 3.89282 |  |
| 2026-07-09 | NSE | ONGC | completed | 3.85518 |  |
| 2026-07-09 | NSE | RELIANCE | completed | 4.46105 |  |
| 2026-07-09 | NSE | SBIN | completed | 3.38039 |  |
| 2026-07-09 | NSE | SUNPHARMA | completed | 3.48204 |  |
| 2026-07-09 | NSE | TCS | completed | 3.58901 |  |
| 2026-07-09 | NSE | TECHM | completed | 3.74736 |  |
| 2026-07-09 | NSE | ULTRACEMCO | completed | 4.52581 |  |
| 2026-07-09 | NSE | WIPRO | completed | 3.83463 |  |
| 2026-07-13 | NSE | ADANIPORTS | completed | 8.27736 |  |
| 2026-07-13 | NSE | AXISBANK | completed | 7.73543 |  |
| 2026-07-13 | NSE | BAJAJ-AUTO | completed | 8.0737 |  |
| 2026-07-13 | NSE | BANKBEES | completed | 9.29022 |  |
| 2026-07-13 | NSE | BHARTIARTL | completed | 8.01342 |  |
| 2026-07-13 | NSE | BPCL | completed | 8.70653 |  |
| 2026-07-13 | NSE | BRITANNIA | completed | 10.1583 |  |
| 2026-07-13 | NSE | CIPLA | completed | 9.43799 |  |
| 2026-07-13 | NSE | DRREDDY | completed | 11.817 |  |
| 2026-07-13 | NSE | GOLDBEES | completed | 9.89304 |  |
| 2026-07-13 | NSE | HCLTECH | completed | 10.5222 |  |
| 2026-07-13 | NSE | HDFCBANK | completed | 11.3787 |  |
| 2026-07-13 | NSE | HINDUNILVR | completed | 12.9583 |  |
| 2026-07-13 | NSE | ICICIBANK | completed | 13.527 |  |
| 2026-07-13 | NSE | INFY | completed | 12.6529 |  |
| 2026-07-13 | NSE | ITBEES | completed | 12.086 |  |
| 2026-07-13 | NSE | ITC | completed | 14.2399 |  |
| 2026-07-13 | NSE | JUNIORBEES | completed | 13.0067 |  |
| 2026-07-13 | NSE | KOTAKBANK | completed | 12.4217 |  |
| 2026-07-13 | NSE | LT | completed | 12.3131 |  |
| 2026-07-13 | NSE | M&M | completed | 14.2564 |  |
| 2026-07-13 | NSE | MARUTI | completed | 14.735 |  |
| 2026-07-13 | NSE | NESTLEIND | completed | 18.9628 |  |
| 2026-07-13 | NSE | NIFTYBEES | completed | 16.0165 |  |
| 2026-07-13 | NSE | ONGC | completed | 17.3078 |  |
| 2026-07-13 | NSE | RELIANCE | completed | 18.0013 |  |
| 2026-07-13 | NSE | SBIN | completed | 21.3294 |  |
| 2026-07-13 | NSE | SUNPHARMA | completed | 21.0497 |  |
| 2026-07-13 | NSE | TCS | completed | 22.3616 |  |
| 2026-07-13 | NSE | TECHM | completed | 21.1257 |  |
| 2026-07-13 | NSE | ULTRACEMCO | completed | 21.6393 |  |
| 2026-07-13 | NSE | WIPRO | completed | 22.2928 |  |

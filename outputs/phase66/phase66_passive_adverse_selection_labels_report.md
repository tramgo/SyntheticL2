# Phase66 Passive Adverse-Selection Labels

Generated UTC: 2026-07-19T19:33:26.126953+00:00

Phase66 labels inferred passive touch opportunities for adverse selection and cost-clearing behavior.
These are not observed broker fills; they are received-tick L2 labels for hypothetical passive orders.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase66_shards_scanned | 32 | Dense shards scanned |
| phase66_label_rows | 28 | Shard/symbol/strategy/side/bucket rows with inferred touches |
| phase66_candidate_orders | 5681976 | Hypothetical passive order candidates in labeled rows |
| phase66_inferred_touches | 68850 | Inferred passive touch opportunities |
| phase66_strategy_rollup_rows | 4 | Strategy/side rollup rows |
| phase66_bucket_rollup_rows | 16 | Strategy/side/spread/imbalance bucket rollup rows |
| phase66_label_candidate_rows | 0 | Bucket rows passing adverse-selection label gate |
| phase66_best_mean_after_cost_bps_if_touched | -17.0135 | Best bucket mean after-cost bps conditional on touch |
| phase66_best_cost_clearing_rate | 0 | Best bucket cost-clearing rate conditional on touch |
| phase66_survives_label_gate | 0 | 1 means at least one passive label bucket deserves targeted replay |
| phase66_elapsed_seconds | 13.1448 | Elapsed seconds |
| phase66_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |
| phase66_recommend_next_action | retire_naive_passive_imbalance_and_return_to_feature_design | Recommended next action |

## Strategy Rollup

| strategy_id | side | shard_symbol_label_rows | symbols | trade_dates | candidate_orders | inferred_touches | mean_gross_bps_if_touched | median_gross_bps_if_touched | mean_after_cost_bps_if_touched | mean_adverse_selection_rate | mean_cost_clearing_rate | worst_gross_bps_if_touched | best_gross_bps_if_touched | mean_spread_bps | mean_abs_l1_imbalance | touch_rate | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P66_FADE_IMBALANCE | -1 | 9 | 8 | 1 | 1963488 | 27600 | -17.1556 | -12.3241 | -25.4237 | 1 | 0 | -196.239 | 0 | 2.42491 | 0.495079 | 0.0140566 | False |
| P66_JOIN_IMBALANCE | 1 | 9 | 8 | 1 | 1961504 | 19650 | -19.2213 | -13.231 | -27.4895 | 1 | 0 | -248.387 | 0 | 2.44553 | 0.495981 | 0.0100178 | False |
| P66_JOIN_IMBALANCE | -1 | 5 | 5 | 1 | 878492 | 13200 | -20.1663 | -14.2687 | -28.4344 | 0.994286 | 0 | -213.436 | 2.22045e-12 | 2.12033 | 0.448986 | 0.0150257 | False |
| P66_FADE_IMBALANCE | 1 | 5 | 5 | 1 | 878492 | 8400 | -26.4037 | -15.2937 | -34.6718 | 1 | 0 | -294.158 | 0 | 2.12033 | 0.448986 | 0.00956184 | False |

## Bucket Rollup

| strategy_id | side | spread_bucket | imbalance_bucket | shard_symbol_label_rows | symbols | trade_dates | candidate_orders | inferred_touches | mean_gross_bps_if_touched | median_gross_bps_if_touched | mean_after_cost_bps_if_touched | mean_adverse_selection_rate | mean_cost_clearing_rate | worst_gross_bps_if_touched | best_gross_bps_if_touched | mean_spread_bps | mean_abs_l1_imbalance | touch_rate | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P66_JOIN_IMBALANCE | 1 | S03_2p5_5bp | I01_0p30_0p40 | 2 | 2 | 1 | 247916 | 2350 | -8.74538 | -7.06069 | -17.0135 | 1 | 0 | -103.347 | -0.24621 | 3.09319 | 0.364147 | 0.00947902 | False |
| P66_FADE_IMBALANCE | -1 | S03_2p5_5bp | I01_0p30_0p40 | 2 | 2 | 1 | 249900 | 3600 | -12.4415 | -10.8733 | -20.7096 | 1 | 0 | -58.4302 | -0.245801 | 3.00038 | 0.360085 | 0.0144058 | False |
| P66_JOIN_IMBALANCE | -1 | S03_2p5_5bp | I03_0p60_0p80 | 1 | 1 | 1 | 247916 | 3800 | -12.6008 | -8.28201 | -20.8689 | 1 | 0 | -106.542 | 0 | 3.55595 | 0.697282 | 0.0153278 | False |
| P66_FADE_IMBALANCE | -1 | S03_2p5_5bp | I03_0p60_0p80 | 1 | 1 | 1 | 245932 | 3050 | -15.505 | -10.8259 | -23.7732 | 1 | 0 | -78.5099 | -1.53799 | 3.08849 | 0.740932 | 0.0124018 | False |
| P66_FADE_IMBALANCE | -1 | S02_1_2p5bp | I03_0p60_0p80 | 1 | 1 | 1 | 247916 | 3700 | -16.1367 | -12.3241 | -24.4049 | 1 | 0 | -114.241 | -1.07105 | 1.43273 | 0.621444 | 0.0149244 | False |
| P66_FADE_IMBALANCE | -1 | S02_1_2p5bp | I02_0p40_0p60 | 2 | 2 | 1 | 491864 | 6950 | -18.2888 | -14.0034 | -26.5569 | 1 | 0 | -87.1198 | -0.872753 | 1.63256 | 0.477167 | 0.0141299 | False |
| P66_JOIN_IMBALANCE | 1 | S03_2p5_5bp | I03_0p60_0p80 | 1 | 1 | 1 | 245932 | 2350 | -18.4008 | -13.9168 | -26.6689 | 1 | 0 | -78.5219 | -1.53681 | 3.08849 | 0.740932 | 0.00955549 | False |
| P66_FADE_IMBALANCE | 1 | S03_2p5_5bp | I03_0p60_0p80 | 1 | 1 | 1 | 247916 | 2100 | -20.1876 | -12.9141 | -28.4557 | 1 | 0 | -194.088 | 0 | 3.55595 | 0.697282 | 0.00847061 | False |
| P66_FADE_IMBALANCE | -1 | S03_2p5_5bp | I02_0p40_0p60 | 3 | 3 | 1 | 727876 | 10300 | -20.4326 | -13.1568 | -28.7007 | 1 | 0 | -196.239 | 0 | 2.67903 | 0.472943 | 0.0141508 | False |
| P66_JOIN_IMBALANCE | 1 | S02_1_2p5bp | I02_0p40_0p60 | 2 | 2 | 1 | 491864 | 5100 | -21.0767 | -14.978 | -29.3448 | 1 | 0 | -196.799 | 0 | 1.63256 | 0.477167 | 0.0103687 | False |
| P66_JOIN_IMBALANCE | 1 | S02_1_2p5bp | I03_0p60_0p80 | 1 | 1 | 1 | 247916 | 2350 | -21.7667 | -9.9591 | -30.0348 | 1 | 0 | -214.759 | -1.42699 | 1.43273 | 0.621444 | 0.00947902 | False |
| P66_JOIN_IMBALANCE | -1 | S02_1_2p5bp | I01_0p30_0p40 | 3 | 3 | 1 | 394564 | 5900 | -21.8964 | -16.2585 | -30.1645 | 1 | 0 | -120.198 | 0 | 1.94943 | 0.325487 | 0.0149532 | False |
| P66_JOIN_IMBALANCE | -1 | S02_1_2p5bp | I02_0p40_0p60 | 1 | 1 | 1 | 236012 | 3500 | -22.5415 | -14.2687 | -30.8096 | 0.971429 | 0 | -213.436 | 2.22045e-12 | 1.19743 | 0.571184 | 0.0148298 | False |
| P66_JOIN_IMBALANCE | 1 | S03_2p5_5bp | I02_0p40_0p60 | 3 | 3 | 1 | 727876 | 7500 | -24.3935 | -16.3121 | -32.6616 | 1 | 0 | -248.387 | 0 | 2.67903 | 0.472943 | 0.010304 | False |
| P66_FADE_IMBALANCE | 1 | S02_1_2p5bp | I02_0p40_0p60 | 1 | 1 | 1 | 236012 | 2400 | -26.8722 | -12.8429 | -35.1403 | 1 | 0 | -240.517 | 0 | 1.19743 | 0.571184 | 0.010169 | False |
| P66_FADE_IMBALANCE | 1 | S02_1_2p5bp | I01_0p30_0p40 | 3 | 3 | 1 | 394564 | 3900 | -28.3196 | -15.6216 | -36.5877 | 1 | 0 | -294.158 | 0 | 1.94943 | 0.325487 | 0.00988433 | False |

## Symbol Rollup

| symbol | strategy_id | side | shard_symbol_label_rows | symbols | trade_dates | candidate_orders | inferred_touches | mean_gross_bps_if_touched | median_gross_bps_if_touched | mean_after_cost_bps_if_touched | mean_adverse_selection_rate | mean_cost_clearing_rate | worst_gross_bps_if_touched | best_gross_bps_if_touched | mean_spread_bps | mean_abs_l1_imbalance | touch_rate | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BANKBEES | P66_FADE_IMBALANCE | -1 | 1 | 1 | 1 | 243948 | 3500 | -11.7709 | -8.63445 | -20.039 | 1 | 0 | -58.4302 | -0.245801 | 3.45861 | 0.328295 | 0.0143473 | False |
| NESTLEIND | P66_JOIN_IMBALANCE | 1 | 2 | 1 | 1 | 245932 | 2550 | -12.5417 | -8.83809 | -20.8098 | 1 | 0 | -222.904 | 0 | 2.7346 | 0.406509 | 0.0103687 | False |
| JUNIORBEES | P66_JOIN_IMBALANCE | -1 | 1 | 1 | 1 | 247916 | 3800 | -12.6008 | -8.28201 | -20.8689 | 1 | 0 | -106.542 | 0 | 3.55595 | 0.697282 | 0.0153278 | False |
| ITBEES | P66_FADE_IMBALANCE | -1 | 1 | 1 | 1 | 245932 | 3050 | -15.505 | -10.8259 | -23.7732 | 1 | 0 | -78.5099 | -1.53799 | 3.08849 | 0.740932 | 0.0124018 | False |
| BANKBEES | P66_JOIN_IMBALANCE | 1 | 1 | 1 | 1 | 243948 | 2250 | -16.1267 | -12.7573 | -24.3948 | 1 | 0 | -103.347 | -0.24621 | 3.45861 | 0.328295 | 0.00922328 | False |
| NIFTYBEES | P66_FADE_IMBALANCE | -1 | 1 | 1 | 1 | 247916 | 3700 | -16.1367 | -12.3241 | -24.4049 | 1 | 0 | -114.241 | -1.07105 | 1.43273 | 0.621444 | 0.0149244 | False |
| ITC | P66_FADE_IMBALANCE | -1 | 1 | 1 | 1 | 245932 | 3500 | -16.347 | -12.2659 | -24.6151 | 1 | 0 | -76.1688 | -0.872753 | 1.75413 | 0.509928 | 0.0142316 | False |
| ULTRACEMCO | P66_FADE_IMBALANCE | -1 | 2 | 1 | 1 | 243948 | 3450 | -17.3682 | -13.1344 | -25.6363 | 1 | 0 | -152.475 | -0.422083 | 2.54413 | 0.414387 | 0.0141424 | False |
| SUNPHARMA | P66_JOIN_IMBALANCE | -1 | 1 | 1 | 1 | 89196 | 1450 | -17.373 | -16.2585 | -25.6412 | 1 | 0 | -74.0778 | 0 | 2.04402 | 0.305639 | 0.0162563 | False |
| ITBEES | P66_JOIN_IMBALANCE | 1 | 1 | 1 | 1 | 245932 | 2350 | -18.4008 | -13.9168 | -26.6689 | 1 | 0 | -78.5219 | -1.53681 | 3.08849 | 0.740932 | 0.00955549 | False |
| CIPLA | P66_FADE_IMBALANCE | -1 | 1 | 1 | 1 | 247916 | 3600 | -19.7224 | -11.6343 | -27.9905 | 1 | 0 | -142.935 | -0.680643 | 2.74954 | 0.568911 | 0.014521 | False |
| ITC | P66_JOIN_IMBALANCE | 1 | 1 | 1 | 1 | 245932 | 2450 | -19.7344 | -13.231 | -28.0025 | 1 | 0 | -196.799 | -0.873134 | 1.75413 | 0.509928 | 0.0099621 | False |
| ICICIBANK | P66_JOIN_IMBALANCE | -1 | 1 | 1 | 1 | 249900 | 3700 | -19.8201 | -14.2071 | -28.0882 | 1 | 0 | -69.8714 | -1.11022e-12 | 1.39362 | 0.367678 | 0.0148059 | False |
| NESTLEIND | P66_FADE_IMBALANCE | -1 | 1 | 1 | 1 | 241964 | 3350 | -19.951 | -13.6752 | -28.2192 | 1 | 0 | -196.239 | 0 | 2.74144 | 0.413017 | 0.013845 | False |
| JUNIORBEES | P66_FADE_IMBALANCE | 1 | 1 | 1 | 1 | 247916 | 2100 | -20.1876 | -12.9141 | -28.4557 | 1 | 0 | -194.088 | 0 | 3.55595 | 0.697282 | 0.00847061 | False |
| RELIANCE | P66_FADE_IMBALANCE | -1 | 1 | 1 | 1 | 245932 | 3450 | -20.2305 | -15.7409 | -28.4986 | 1 | 0 | -87.1198 | -2.24316 | 1.51099 | 0.444407 | 0.0140283 | False |
| NIFTYBEES | P66_JOIN_IMBALANCE | 1 | 1 | 1 | 1 | 247916 | 2350 | -21.7667 | -9.9591 | -30.0348 | 1 | 0 | -214.759 | -1.42699 | 1.43273 | 0.621444 | 0.00947902 | False |
| RELIANCE | P66_JOIN_IMBALANCE | 1 | 1 | 1 | 1 | 245932 | 2650 | -22.419 | -16.725 | -30.6871 | 1 | 0 | -176.488 | 0 | 1.51099 | 0.444407 | 0.0107753 | False |
| HDFCBANK | P66_JOIN_IMBALANCE | -1 | 1 | 1 | 1 | 236012 | 3500 | -22.5415 | -14.2687 | -30.8096 | 0.971429 | 0 | -213.436 | 2.22045e-12 | 1.19743 | 0.571184 | 0.0148298 | False |
| CIPLA | P66_JOIN_IMBALANCE | 1 | 1 | 1 | 1 | 247916 | 2550 | -23.7614 | -16.3878 | -32.0295 | 1 | 0 | -164.884 | 0 | 2.74954 | 0.568911 | 0.0102857 | False |
| ICICIBANK | P66_FADE_IMBALANCE | 1 | 1 | 1 | 1 | 249900 | 2550 | -23.9967 | -15.2937 | -32.2648 | 1 | 0 | -294.158 | 0 | 1.39362 | 0.367678 | 0.0102041 | False |
| ULTRACEMCO | P66_JOIN_IMBALANCE | 1 | 1 | 1 | 1 | 237996 | 2500 | -25.6997 | -12.7807 | -33.9678 | 1 | 0 | -248.387 | -1.26652 | 2.5461 | 0.436899 | 0.0105044 | False |
| HCLTECH | P66_FADE_IMBALANCE | 1 | 1 | 1 | 1 | 55468 | 600 | -26.7978 | -15.6216 | -35.0659 | 1 | 0 | -157.59 | -4.40546 | 2.41064 | 0.303145 | 0.010817 | False |
| HDFCBANK | P66_FADE_IMBALANCE | 1 | 1 | 1 | 1 | 236012 | 2400 | -26.8722 | -12.8429 | -35.1403 | 1 | 0 | -240.517 | 0 | 1.19743 | 0.571184 | 0.010169 | False |
| HCLTECH | P66_JOIN_IMBALANCE | -1 | 1 | 1 | 1 | 55468 | 750 | -28.4962 | -24.5849 | -36.7643 | 1 | 0 | -120.198 | -4.41696 | 2.41064 | 0.303145 | 0.0135213 | False |
| SUNPHARMA | P66_FADE_IMBALANCE | 1 | 1 | 1 | 1 | 89196 | 750 | -34.1643 | -19.2659 | -42.4324 | 1 | 0 | -179.821 | -1.52913 | 2.04402 | 0.305639 | 0.00840845 | False |

## Label Rows

| shard_index | trade_date | symbol | strategy_id | side | spread_bucket | imbalance_bucket | candidate_orders | inferred_touches | mean_gross_bps_if_touched | median_gross_bps_if_touched | adverse_selection_rate | cost_clearing_rate | mean_after_cost_bps_if_touched | worst_gross_bps_if_touched | best_gross_bps_if_touched | mean_spread_bps | mean_abs_l1_imbalance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 2026-01-01 | BANKBEES | P66_FADE_IMBALANCE | -1 | S03_2p5_5bp | I01_0p30_0p40 | 243948 | 3500 | -11.7709 | -8.63445 | 1 | 0 | -20.039 | -58.4302 | -0.245801 | 3.45861 | 0.328295 |
| 4 | 2026-01-01 | BANKBEES | P66_JOIN_IMBALANCE | 1 | S03_2p5_5bp | I01_0p30_0p40 | 243948 | 2250 | -16.1267 | -12.7573 | 1 | 0 | -24.3948 | -103.347 | -0.24621 | 3.45861 | 0.328295 |
| 8 | 2026-01-01 | CIPLA | P66_JOIN_IMBALANCE | 1 | S03_2p5_5bp | I02_0p40_0p60 | 247916 | 2550 | -23.7614 | -16.3878 | 1 | 0 | -32.0295 | -164.884 | 0 | 2.74954 | 0.568911 |
| 8 | 2026-01-01 | CIPLA | P66_FADE_IMBALANCE | -1 | S03_2p5_5bp | I02_0p40_0p60 | 247916 | 3600 | -19.7224 | -11.6343 | 1 | 0 | -27.9905 | -142.935 | -0.680643 | 2.74954 | 0.568911 |
| 11 | 2026-01-01 | HCLTECH | P66_JOIN_IMBALANCE | -1 | S02_1_2p5bp | I01_0p30_0p40 | 55468 | 750 | -28.4962 | -24.5849 | 1 | 0 | -36.7643 | -120.198 | -4.41696 | 2.41064 | 0.303145 |
| 11 | 2026-01-01 | HCLTECH | P66_FADE_IMBALANCE | 1 | S02_1_2p5bp | I01_0p30_0p40 | 55468 | 600 | -26.7978 | -15.6216 | 1 | 0 | -35.0659 | -157.59 | -4.40546 | 2.41064 | 0.303145 |
| 12 | 2026-01-01 | HDFCBANK | P66_JOIN_IMBALANCE | -1 | S02_1_2p5bp | I02_0p40_0p60 | 236012 | 3500 | -22.5415 | -14.2687 | 0.971429 | 0 | -30.8096 | -213.436 | 2.22045e-12 | 1.19743 | 0.571184 |
| 12 | 2026-01-01 | HDFCBANK | P66_FADE_IMBALANCE | 1 | S02_1_2p5bp | I02_0p40_0p60 | 236012 | 2400 | -26.8722 | -12.8429 | 1 | 0 | -35.1403 | -240.517 | 0 | 1.19743 | 0.571184 |
| 14 | 2026-01-01 | ICICIBANK | P66_FADE_IMBALANCE | 1 | S02_1_2p5bp | I01_0p30_0p40 | 249900 | 2550 | -23.9967 | -15.2937 | 1 | 0 | -32.2648 | -294.158 | 0 | 1.39362 | 0.367678 |
| 14 | 2026-01-01 | ICICIBANK | P66_JOIN_IMBALANCE | -1 | S02_1_2p5bp | I01_0p30_0p40 | 249900 | 3700 | -19.8201 | -14.2071 | 1 | 0 | -28.0882 | -69.8714 | -1.11022e-12 | 1.39362 | 0.367678 |
| 16 | 2026-01-01 | ITBEES | P66_FADE_IMBALANCE | -1 | S03_2p5_5bp | I03_0p60_0p80 | 245932 | 3050 | -15.505 | -10.8259 | 1 | 0 | -23.7732 | -78.5099 | -1.53799 | 3.08849 | 0.740932 |
| 16 | 2026-01-01 | ITBEES | P66_JOIN_IMBALANCE | 1 | S03_2p5_5bp | I03_0p60_0p80 | 245932 | 2350 | -18.4008 | -13.9168 | 1 | 0 | -26.6689 | -78.5219 | -1.53681 | 3.08849 | 0.740932 |
| 17 | 2026-01-01 | ITC | P66_JOIN_IMBALANCE | 1 | S02_1_2p5bp | I02_0p40_0p60 | 245932 | 2450 | -19.7344 | -13.231 | 1 | 0 | -28.0025 | -196.799 | -0.873134 | 1.75413 | 0.509928 |
| 17 | 2026-01-01 | ITC | P66_FADE_IMBALANCE | -1 | S02_1_2p5bp | I02_0p40_0p60 | 245932 | 3500 | -16.347 | -12.2659 | 1 | 0 | -24.6151 | -76.1688 | -0.872753 | 1.75413 | 0.509928 |
| 18 | 2026-01-01 | JUNIORBEES | P66_FADE_IMBALANCE | 1 | S03_2p5_5bp | I03_0p60_0p80 | 247916 | 2100 | -20.1876 | -12.9141 | 1 | 0 | -28.4557 | -194.088 | 0 | 3.55595 | 0.697282 |
| 18 | 2026-01-01 | JUNIORBEES | P66_JOIN_IMBALANCE | -1 | S03_2p5_5bp | I03_0p60_0p80 | 247916 | 3800 | -12.6008 | -8.28201 | 1 | 0 | -20.8689 | -106.542 | 0 | 3.55595 | 0.697282 |
| 23 | 2026-01-01 | NESTLEIND | P66_JOIN_IMBALANCE | 1 | S03_2p5_5bp | I01_0p30_0p40 | 3968 | 100 | -1.36407 | -1.36407 | 1 | 0 | -9.63219 | -1.36407 | -1.36407 | 2.72777 | 0.4 |
| 23 | 2026-01-01 | NESTLEIND | P66_FADE_IMBALANCE | -1 | S03_2p5_5bp | I02_0p40_0p60 | 241964 | 3350 | -19.951 | -13.6752 | 1 | 0 | -28.2192 | -196.239 | 0 | 2.74144 | 0.413017 |
| 23 | 2026-01-01 | NESTLEIND | P66_JOIN_IMBALANCE | 1 | S03_2p5_5bp | I02_0p40_0p60 | 241964 | 2450 | -23.7193 | -16.3121 | 1 | 0 | -31.9874 | -222.904 | 0 | 2.74144 | 0.413017 |
| 24 | 2026-01-01 | NIFTYBEES | P66_FADE_IMBALANCE | -1 | S02_1_2p5bp | I03_0p60_0p80 | 247916 | 3700 | -16.1367 | -12.3241 | 1 | 0 | -24.4049 | -114.241 | -1.07105 | 1.43273 | 0.621444 |
| 24 | 2026-01-01 | NIFTYBEES | P66_JOIN_IMBALANCE | 1 | S02_1_2p5bp | I03_0p60_0p80 | 247916 | 2350 | -21.7667 | -9.9591 | 1 | 0 | -30.0348 | -214.759 | -1.42699 | 1.43273 | 0.621444 |
| 26 | 2026-01-01 | RELIANCE | P66_JOIN_IMBALANCE | 1 | S02_1_2p5bp | I02_0p40_0p60 | 245932 | 2650 | -22.419 | -16.725 | 1 | 0 | -30.6871 | -176.488 | 0 | 1.51099 | 0.444407 |
| 26 | 2026-01-01 | RELIANCE | P66_FADE_IMBALANCE | -1 | S02_1_2p5bp | I02_0p40_0p60 | 245932 | 3450 | -20.2305 | -15.7409 | 1 | 0 | -28.4986 | -87.1198 | -2.24316 | 1.51099 | 0.444407 |
| 28 | 2026-01-01 | SUNPHARMA | P66_FADE_IMBALANCE | 1 | S02_1_2p5bp | I01_0p30_0p40 | 89196 | 750 | -34.1643 | -19.2659 | 1 | 0 | -42.4324 | -179.821 | -1.52913 | 2.04402 | 0.305639 |
| 28 | 2026-01-01 | SUNPHARMA | P66_JOIN_IMBALANCE | -1 | S02_1_2p5bp | I01_0p30_0p40 | 89196 | 1450 | -17.373 | -16.2585 | 1 | 0 | -25.6412 | -74.0778 | 0 | 2.04402 | 0.305639 |
| 31 | 2026-01-01 | ULTRACEMCO | P66_FADE_IMBALANCE | -1 | S03_2p5_5bp | I01_0p30_0p40 | 5952 | 100 | -13.1121 | -13.1121 | 1 | 0 | -21.3802 | -19.0275 | -7.19668 | 2.54216 | 0.391875 |
| 31 | 2026-01-01 | ULTRACEMCO | P66_JOIN_IMBALANCE | 1 | S03_2p5_5bp | I02_0p40_0p60 | 237996 | 2500 | -25.6997 | -12.7807 | 1 | 0 | -33.9678 | -248.387 | -1.26652 | 2.5461 | 0.436899 |
| 31 | 2026-01-01 | ULTRACEMCO | P66_FADE_IMBALANCE | -1 | S03_2p5_5bp | I02_0p40_0p60 | 237996 | 3350 | -21.6243 | -13.1568 | 1 | 0 | -29.8924 | -152.475 | -0.422083 | 2.5461 | 0.436899 |

# Phase68 Replenishment-After-Touch Labels

Generated UTC: 2026-07-19T19:38:27.200367+00:00

Phase68 tests whether visible same-side L1 replenishment after an inferred passive touch reduces adverse selection.
The labels remain hypothetical received-tick L2 labels, not observed broker fills or true queue-position evidence.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase68_shards_scanned | 32 | Dense shards scanned |
| phase68_label_rows | 56 | Shard/symbol/strategy/side/replenishment bucket rows |
| phase68_inferred_touches | 68850 | Inferred passive touch opportunities labeled with replenishment |
| phase68_bucket_rollup_rows | 32 | Aggregated replenishment bucket rows |
| phase68_label_candidate_rows | 0 | Replenishment bucket rows passing label gate |
| phase68_best_mean_after_cost_bps_if_touched | -13.236 | Best bucket mean after-cost bps conditional on touch |
| phase68_best_cost_clearing_rate | 0 | Best bucket cost-clearing rate conditional on touch |
| phase68_best_adverse_selection_rate | 0.9375 | Lowest bucket adverse-selection rate conditional on touch |
| phase68_survives_replenishment_gate | 0 | 1 means a replenishment bucket deserves targeted replay |
| phase68_elapsed_seconds | 11.7763 | Elapsed seconds |
| phase68_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |
| phase68_recommend_next_action | advance_to_spread_transition_feature_family | Recommended next action |

## Bucket Rollup

| strategy_id | side | spread_bucket | imbalance_bucket | replenishment_bucket | shard_symbol_label_rows | symbols | trade_dates | inferred_touches | mean_replenishment_ratio | median_replenishment_ratio | mean_gross_bps_if_touched | median_gross_bps_if_touched | mean_after_cost_bps_if_touched | mean_adverse_selection_rate | mean_cost_clearing_rate | worst_gross_bps_if_touched | best_gross_bps_if_touched | mean_spread_bps | mean_abs_l1_imbalance | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 2 | 2 | 1 | 400 | 0.940019 | 0.943818 | -4.9679 | -4.20582 | -13.236 | 1 | 0 | -30.03 | -0.24621 | 3.09517 | 0.363051 | False |
| P68_JOIN_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I03_0p60_0p80 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 700 | 0.968042 | 0.967066 | -7.03199 | -4.99142 | -15.3001 | 1 | 0 | -27.8344 | 0 | 3.5568 | 0.696902 | False |
| P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 2 | 2 | 1 | 1950 | 1.0046 | 1 | -9.46491 | -7.28781 | -17.733 | 1 | 0 | -103.347 | -0.24621 | 3.09074 | 0.363817 | False |
| P68_FADE_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I03_0p60_0p80 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 840 | 0.970476 | 0.983103 | -11.2197 | -6.0867 | -19.4879 | 1 | 0 | -71.4031 | -1.07124 | 1.43317 | 0.622436 | False |
| P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 2 | 2 | 1 | 920 | 0.902712 | 0.905735 | -11.9652 | -10.8713 | -20.2333 | 1 | 0 | -58.4302 | -0.245801 | 3.00237 | 0.360011 | False |
| P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 2 | 2 | 1 | 2680 | 1.00278 | 1 | -12.6015 | -10.8733 | -20.8696 | 1 | 0 | -58.4302 | -0.245801 | 3.00199 | 0.360284 | False |
| P68_JOIN_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I03_0p60_0p80 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 3100 | 1.00622 | 1 | -13.8583 | -8.96351 | -22.1264 | 1 | 0 | -106.542 | 0 | 3.56112 | 0.697194 | False |
| P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I03_0p60_0p80 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 400 | 0.964061 | 0.969972 | -14.4666 | -7.69361 | -22.7347 | 1 | 0 | -78.5219 | -1.53681 | 3.08318 | 0.739704 | False |
| P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I03_0p60_0p80 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 540 | 0.962063 | 0.970874 | -14.4729 | -10.8259 | -22.741 | 1 | 0 | -38.4615 | -1.53846 | 3.0962 | 0.740643 | False |
| P68_JOIN_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 640 | 0.964062 | 0.96753 | -14.9791 | -9.51505 | -23.2472 | 0.9375 | 0 | -105.389 | 2.22045e-12 | 1.19929 | 0.571118 | False |
| P68_FADE_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 2 | 2 | 1 | 1520 | 0.963328 | 0.964813 | -15.0129 | -11.7208 | -23.281 | 1 | 0 | -87.1198 | -0.872753 | 1.63431 | 0.476656 | False |
| P68_JOIN_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 2 | 2 | 1 | 1080 | 0.955433 | 0.969437 | -15.3386 | -8.14599 | -23.6068 | 1 | 0 | -196.799 | 0 | 1.63035 | 0.477614 | False |
| P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 3 | 3 | 1 | 1360 | 0.965468 | 0.970367 | -15.6774 | -9.3116 | -23.9455 | 1 | 0 | -222.904 | 0 | 2.67535 | 0.473659 | False |
| P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I03_0p60_0p80 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2510 | 1.00721 | 1 | -15.7271 | -10.8259 | -23.9952 | 1 | 0 | -78.5099 | -1.53799 | 3.09061 | 0.74143 | False |
| P68_FADE_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I03_0p60_0p80 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2860 | 1.00503 | 1 | -17.5809 | -14.6241 | -25.849 | 1 | 0 | -114.241 | -1.07105 | 1.43506 | 0.622014 | False |
| P68_FADE_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I03_0p60_0p80 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 1780 | 1.00698 | 1 | -18.9533 | -13.6612 | -27.2214 | 1 | 0 | -194.088 | 0 | 3.55051 | 0.697216 | False |
| P68_FADE_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 2 | 2 | 1 | 5430 | 1.00737 | 1 | -19.2048 | -14.7968 | -27.4729 | 1 | 0 | -87.1198 | -0.872753 | 1.63471 | 0.47726 | False |
| P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I03_0p60_0p80 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 1950 | 1.01166 | 1 | -19.2078 | -13.9427 | -27.4759 | 1 | 0 | -78.5219 | -1.53681 | 3.08596 | 0.74056 | False |
| P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 3 | 3 | 1 | 2180 | 0.96106 | 0.970414 | -19.7071 | -9.57003 | -27.9752 | 1 | 0 | -196.239 | 0 | 2.68198 | 0.471088 | False |
| P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 3 | 3 | 1 | 8120 | 1.00768 | 1 | -20.6273 | -13.8523 | -28.8955 | 1 | 0 | -196.239 | 0 | 2.68303 | 0.473021 | False |
| P68_JOIN_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 3 | 3 | 1 | 1280 | 0.956894 | 0.963114 | -20.7082 | -12.4137 | -28.9763 | 1 | 0 | -120.198 | 0 | 1.9532 | 0.325803 | False |
| P68_JOIN_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I03_0p60_0p80 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 440 | 0.969335 | 0.970543 | -20.928 | -7.88336 | -29.1961 | 1 | 0 | -214.759 | -1.42699 | 1.42947 | 0.619661 | False |
| P68_FADE_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 3 | 3 | 1 | 860 | 0.957175 | 0.969958 | -21.0611 | -13.7533 | -29.3293 | 1 | 0 | -179.821 | -1.11022e-12 | 1.94418 | 0.325671 | False |
| P68_JOIN_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I03_0p60_0p80 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 1910 | 1.01044 | 1 | -21.9598 | -13.5588 | -30.228 | 1 | 0 | -214.759 | -1.42699 | 1.4305 | 0.620564 | False |
| P68_JOIN_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 3 | 3 | 1 | 4620 | 1.00678 | 1 | -22.1545 | -16.2585 | -30.4226 | 1 | 0 | -120.198 | 0 | 1.95312 | 0.325407 | False |
| P68_JOIN_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 2 | 2 | 1 | 4020 | 1.01179 | 1 | -22.5045 | -16.9867 | -30.7726 | 1 | 0 | -196.799 | 0 | 1.62962 | 0.477317 | False |
| P68_JOIN_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2860 | 1.01033 | 1 | -24.2338 | -17.4017 | -32.5019 | 0.979021 | 0 | -213.436 | 2.22045e-12 | 1.1995 | 0.571258 | False |
| P68_FADE_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 1920 | 1.00689 | 1 | -25.1361 | -13.2219 | -33.4042 | 1 | 0 | -240.517 | 0 | 1.19426 | 0.571179 | False |
| P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 3 | 3 | 1 | 6140 | 1.0106 | 1 | -26.3811 | -16.4813 | -34.6492 | 1 | 0 | -248.387 | 0 | 2.67328 | 0.473513 | False |
| P68_FADE_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I03_0p60_0p80 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 320 | 0.959226 | 0.966942 | -27.0532 | -9.42783 | -35.3213 | 1 | 0 | -194.088 | 0 | 3.55249 | 0.696972 | False |
| P68_FADE_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 3 | 3 | 1 | 3040 | 1.00975 | 1 | -30.663 | -19.2659 | -38.9312 | 1 | 0 | -294.158 | 0 | 1.94395 | 0.325234 | False |
| P68_FADE_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 480 | 0.939931 | 0.953488 | -33.8166 | -8.71105 | -42.0847 | 1 | 0 | -240.517 | 0 | 1.19614 | 0.570641 | False |

## Strategy Rollup

| strategy_id | side | replenishment_bucket | shard_symbol_label_rows | symbols | trade_dates | inferred_touches | mean_replenishment_ratio | median_replenishment_ratio | mean_gross_bps_if_touched | median_gross_bps_if_touched | mean_after_cost_bps_if_touched | mean_adverse_selection_rate | mean_cost_clearing_rate | worst_gross_bps_if_touched | best_gross_bps_if_touched | mean_spread_bps | mean_abs_l1_imbalance | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P68_JOIN_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 9 | 8 | 1 | 3680 | 0.957856 | 0.970367 | -13.6711 | -7.88336 | -21.9392 | 1 | 0 | -222.904 | 0 | 2.44331 | 0.495741 | False |
| P68_FADE_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 9 | 8 | 1 | 6000 | 0.949755 | 0.970874 | -15.4189 | -10.8259 | -23.687 | 1 | 0 | -196.239 | 0 | 2.42763 | 0.494409 | False |
| P68_JOIN_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 5 | 5 | 1 | 2620 | 0.960557 | 0.964454 | -16.8271 | -11.1172 | -25.0952 | 0.9875 | 0 | -120.198 | 2.22045e-12 | 2.12314 | 0.449086 | False |
| P68_FADE_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 9 | 8 | 1 | 21600 | 1.00618 | 1 | -17.6447 | -13.6977 | -25.9128 | 1 | 0 | -196.239 | 0 | 2.42757 | 0.495288 | False |
| P68_JOIN_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 9 | 8 | 1 | 15970 | 1.00963 | 1 | -20.4722 | -14.9346 | -28.7403 | 1 | 0 | -248.387 | 0 | 2.44189 | 0.495992 | False |
| P68_JOIN_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 5 | 5 | 1 | 10580 | 1.00738 | 1 | -20.9111 | -16.2585 | -29.1792 | 0.995804 | 0 | -213.436 | 2.22045e-12 | 2.12399 | 0.448935 | False |
| P68_FADE_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 5 | 5 | 1 | 1660 | 0.954136 | 0.966942 | -24.8106 | -9.42783 | -33.0788 | 1 | 0 | -240.517 | 0 | 2.11623 | 0.448925 | False |
| P68_FADE_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 5 | 5 | 1 | 6740 | 1.00863 | 1 | -27.2157 | -15.6216 | -35.4838 | 1 | 0 | -294.158 | 0 | 2.11532 | 0.448819 | False |

## Symbol Rollup

| symbol | strategy_id | side | replenishment_bucket | shard_symbol_label_rows | symbols | trade_dates | inferred_touches | mean_replenishment_ratio | median_replenishment_ratio | mean_gross_bps_if_touched | median_gross_bps_if_touched | mean_after_cost_bps_if_touched | mean_adverse_selection_rate | mean_cost_clearing_rate | worst_gross_bps_if_touched | best_gross_bps_if_touched | mean_spread_bps | mean_abs_l1_imbalance | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JUNIORBEES | P68_JOIN_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 700 | 0.968042 | 0.967066 | -7.03199 | -4.99142 | -15.3001 | 1 | 0 | -27.8344 | 0 | 3.5568 | 0.696902 | False |
| BANKBEES | P68_JOIN_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 360 | 0.971875 | 0.979473 | -8.57173 | -7.04757 | -16.8398 | 1 | 0 | -30.03 | -0.24621 | 3.46257 | 0.326101 | False |
| ULTRACEMCO | P68_JOIN_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 480 | 0.965131 | 0.970639 | -9.88846 | -9.3116 | -18.1566 | 1 | 0 | -26.6464 | -1.26652 | 2.54299 | 0.435863 | False |
| NESTLEIND | P68_JOIN_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 2 | 1 | 1 | 480 | 0.938692 | 0.939142 | -10.127 | -4.42659 | -18.3951 | 1 | 0 | -222.904 | 0 | 2.73036 | 0.407408 | False |
| BANKBEES | P68_FADE_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 880 | 0.971227 | 0.977273 | -10.8183 | -8.63042 | -19.0864 | 1 | 0 | -58.4302 | -0.245801 | 3.46259 | 0.328265 | False |
| NIFTYBEES | P68_FADE_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 840 | 0.970476 | 0.983103 | -11.2197 | -6.0867 | -19.4879 | 1 | 0 | -71.4031 | -1.07124 | 1.43317 | 0.622436 | False |
| RELIANCE | P68_JOIN_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 520 | 0.949851 | 0.965543 | -11.9756 | -8.32807 | -20.2437 | 1 | 0 | -76.0657 | 0 | 1.50861 | 0.444061 | False |
| BANKBEES | P68_FADE_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2620 | 1.00556 | 1 | -12.0908 | -8.63445 | -20.359 | 1 | 0 | -58.4302 | -0.245801 | 3.46182 | 0.328811 | False |
| ITC | P68_FADE_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 740 | 0.971358 | 0.974874 | -12.9356 | -11.3102 | -21.2037 | 1 | 0 | -43.3552 | -0.872753 | 1.75622 | 0.509077 | False |
| NESTLEIND | P68_JOIN_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 2 | 1 | 1 | 2070 | 1.00499 | 1 | -13.0703 | -8.92266 | -21.3384 | 1 | 0 | -222.904 | 0 | 2.73272 | 0.406604 | False |
| ICICIBANK | P68_FADE_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 540 | 0.948057 | 0.952756 | -13.2768 | -8.28958 | -21.5449 | 1 | 0 | -58.7618 | -1.11022e-12 | 1.38969 | 0.366248 | False |
| JUNIORBEES | P68_JOIN_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 3100 | 1.00622 | 1 | -13.8583 | -8.96351 | -22.1264 | 1 | 0 | -106.542 | 0 | 3.56112 | 0.697194 | False |
| HCLTECH | P68_FADE_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 160 | 0.956474 | 0.970377 | -14.3329 | -15.6216 | -22.6011 | 1 | 0 | -26.049 | -4.40546 | 2.40543 | 0.30405 | False |
| ITBEES | P68_JOIN_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 400 | 0.964061 | 0.969972 | -14.4666 | -7.69361 | -22.7347 | 1 | 0 | -78.5219 | -1.53681 | 3.08318 | 0.739704 | False |
| ITBEES | P68_FADE_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 540 | 0.962063 | 0.970874 | -14.4729 | -10.8259 | -22.741 | 1 | 0 | -38.4615 | -1.53846 | 3.0962 | 0.740643 | False |
| HDFCBANK | P68_JOIN_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 640 | 0.964062 | 0.96753 | -14.9791 | -9.51505 | -23.2472 | 0.9375 | 0 | -105.389 | 2.22045e-12 | 1.19929 | 0.571118 | False |
| ITBEES | P68_FADE_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2510 | 1.00721 | 1 | -15.7271 | -10.8259 | -23.9952 | 1 | 0 | -78.5099 | -1.53799 | 3.09061 | 0.74143 | False |
| SUNPHARMA | P68_JOIN_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 280 | 0.958106 | 0.957063 | -16.1181 | -12.4429 | -24.3862 | 1 | 0 | -74.0778 | 0 | 2.04896 | 0.305317 | False |
| ICICIBANK | P68_JOIN_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 760 | 0.956723 | 0.964454 | -16.9295 | -11.1172 | -25.1976 | 1 | 0 | -61.9963 | -2.07569 | 1.3966 | 0.368118 | False |
| RELIANCE | P68_FADE_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 780 | 0.955298 | 0.954751 | -17.0902 | -12.1313 | -25.3584 | 1 | 0 | -87.1198 | -2.24316 | 1.51241 | 0.444235 | False |
| ULTRACEMCO | P68_FADE_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 2 | 1 | 1 | 760 | 0.896013 | 0.905683 | -17.1428 | -11.2071 | -25.4109 | 1 | 0 | -152.475 | -0.422083 | 2.54561 | 0.413236 | False |
| ITC | P68_FADE_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2760 | 1.00724 | 1 | -17.2616 | -13.1142 | -25.5298 | 1 | 0 | -76.1688 | -0.872753 | 1.75588 | 0.50995 | False |
| ULTRACEMCO | P68_FADE_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 2 | 1 | 1 | 2690 | 1.00513 | 1 | -17.4299 | -14.3508 | -25.698 | 1 | 0 | -152.475 | -0.422083 | 2.54599 | 0.414452 | False |
| BANKBEES | P68_JOIN_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 1890 | 1.00919 | 1 | -17.5657 | -13.2116 | -25.8339 | 1 | 0 | -103.347 | -0.24621 | 3.45371 | 0.327634 | False |
| NIFTYBEES | P68_FADE_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2860 | 1.00503 | 1 | -17.5809 | -14.6241 | -25.849 | 1 | 0 | -114.241 | -1.07105 | 1.43506 | 0.622014 | False |
| SUNPHARMA | P68_JOIN_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 1170 | 1.0089 | 1 | -17.6734 | -16.2585 | -25.9415 | 1 | 0 | -74.0778 | 0 | 2.04677 | 0.305566 | False |
| CIPLA | P68_JOIN_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 440 | 0.962052 | 0.970367 | -18.2539 | -9.66999 | -26.522 | 1 | 0 | -164.884 | 0 | 2.75011 | 0.570297 | False |
| ITC | P68_JOIN_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 560 | 0.961016 | 0.973331 | -18.7017 | -7.9639 | -26.9698 | 1 | 0 | -196.799 | -0.873134 | 1.75209 | 0.511167 | False |
| CIPLA | P68_FADE_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 820 | 0.960819 | 0.970414 | -18.8154 | -9.57003 | -27.0835 | 1 | 0 | -142.935 | -0.680643 | 2.75167 | 0.567549 | False |
| JUNIORBEES | P68_FADE_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 1780 | 1.00698 | 1 | -18.9533 | -13.6612 | -27.2214 | 1 | 0 | -194.088 | 0 | 3.55051 | 0.697216 | False |
| NESTLEIND | P68_FADE_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 640 | 0.964533 | 0.966511 | -19.1325 | -13.0924 | -27.4006 | 1 | 0 | -196.239 | 0 | 2.7452 | 0.410998 | False |
| ITBEES | P68_JOIN_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 1950 | 1.01166 | 1 | -19.2078 | -13.9427 | -27.4759 | 1 | 0 | -78.5219 | -1.53681 | 3.08596 | 0.74056 | False |
| CIPLA | P68_FADE_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2780 | 1.006 | 1 | -19.9899 | -13.6977 | -28.2581 | 1 | 0 | -142.935 | -0.680643 | 2.75461 | 0.56899 | False |
| ITC | P68_JOIN_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 1890 | 1.0091 | 1 | -20.0404 | -14.9346 | -28.3085 | 1 | 0 | -196.799 | -0.873134 | 1.75115 | 0.510175 | False |
| NESTLEIND | P68_FADE_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2710 | 1.00678 | 1 | -20.1443 | -13.8523 | -28.4125 | 1 | 0 | -196.239 | 0 | 2.74467 | 0.412924 | False |
| ICICIBANK | P68_JOIN_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2940 | 1.01033 | 1 | -20.5673 | -14.5098 | -28.8354 | 1 | 0 | -69.8714 | -1.11022e-12 | 1.39602 | 0.367584 | False |
| NIFTYBEES | P68_JOIN_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 440 | 0.969335 | 0.970543 | -20.928 | -7.88336 | -29.1961 | 1 | 0 | -214.759 | -1.42699 | 1.42947 | 0.619661 | False |
| RELIANCE | P68_FADE_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2670 | 1.00751 | 1 | -21.1479 | -16.4794 | -29.416 | 1 | 0 | -87.1198 | -2.24316 | 1.51354 | 0.444569 | False |
| NIFTYBEES | P68_JOIN_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 1910 | 1.01044 | 1 | -21.9598 | -13.5588 | -30.228 | 1 | 0 | -214.759 | -1.42699 | 1.4305 | 0.620564 | False |
| HDFCBANK | P68_JOIN_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2860 | 1.01033 | 1 | -24.2338 | -17.4017 | -32.5019 | 0.979021 | 0 | -213.436 | 2.22045e-12 | 1.1995 | 0.571258 | False |
| CIPLA | P68_JOIN_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2110 | 1.00971 | 1 | -24.9099 | -17.1116 | -33.178 | 1 | 0 | -164.884 | 0 | 2.74245 | 0.569378 | False |
| RELIANCE | P68_JOIN_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2130 | 1.01448 | 1 | -24.9686 | -19.0389 | -33.2367 | 1 | 0 | -176.488 | 0 | 1.50809 | 0.44446 | False |
| HDFCBANK | P68_FADE_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 1920 | 1.00689 | 1 | -25.1361 | -13.2219 | -33.4042 | 1 | 0 | -240.517 | 0 | 1.19426 | 0.571179 | False |
| ICICIBANK | P68_FADE_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2010 | 1.01105 | 1 | -26.8767 | -20.065 | -35.1448 | 1 | 0 | -294.158 | 0 | 1.39012 | 0.367808 | False |
| JUNIORBEES | P68_FADE_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 320 | 0.959226 | 0.966942 | -27.0532 | -9.42783 | -35.3213 | 1 | 0 | -194.088 | 0 | 3.55249 | 0.696972 | False |
| HCLTECH | P68_JOIN_IMBALANCE_REPLENISH | -1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 510 | 1.00112 | 1 | -28.2229 | -26.1633 | -36.491 | 1 | 0 | -120.198 | -4.41696 | 2.41656 | 0.30307 | False |
| HCLTECH | P68_JOIN_IMBALANCE_REPLENISH | -1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 240 | 0.955853 | 0.963114 | -29.0769 | -12.4137 | -37.3451 | 1 | 0 | -120.198 | -4.41696 | 2.41404 | 0.303974 | False |
| ULTRACEMCO | P68_JOIN_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 2020 | 1.01209 | 1 | -29.4568 | -15.7574 | -37.7249 | 1 | 0 | -248.387 | -1.26652 | 2.53971 | 0.437954 | False |
| HCLTECH | P68_FADE_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 440 | 1.00685 | 1 | -31.3304 | -15.6216 | -39.5985 | 1 | 0 | -157.59 | -4.40546 | 2.4033 | 0.302794 | False |
| SUNPHARMA | P68_FADE_IMBALANCE_REPLENISH | 1 | R03_rebuilt_1p00_1p50 | 1 | 1 | 1 | 590 | 1.01136 | 1 | -33.782 | -19.2659 | -42.0502 | 1 | 0 | -179.821 | -1.52913 | 2.03842 | 0.3051 | False |
| HDFCBANK | P68_FADE_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 480 | 0.939931 | 0.953488 | -33.8166 | -8.71105 | -42.0847 | 1 | 0 | -240.517 | 0 | 1.19614 | 0.570641 | False |
| SUNPHARMA | P68_FADE_IMBALANCE_REPLENISH | 1 | R02_partial_0p50_1p00 | 1 | 1 | 1 | 160 | 0.966993 | 0.969958 | -35.5737 | -13.7533 | -43.8418 | 1 | 0 | -179.821 | -1.52913 | 2.03742 | 0.306714 | False |

## Label Rows

| shard_index | trade_date | symbol | strategy_id | side | spread_bucket | imbalance_bucket | replenishment_bucket | inferred_touches | mean_replenishment_ratio | median_replenishment_ratio | mean_gross_bps_if_touched | median_gross_bps_if_touched | adverse_selection_rate | cost_clearing_rate | mean_after_cost_bps_if_touched | worst_gross_bps_if_touched | best_gross_bps_if_touched | mean_spread_bps | mean_abs_l1_imbalance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 2026-01-01 | BANKBEES | P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 360 | 0.971875 | 0.979473 | -8.57173 | -7.04757 | 1 | 0 | -16.8398 | -30.03 | -0.24621 | 3.46257 | 0.326101 |
| 4 | 2026-01-01 | BANKBEES | P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 2620 | 1.00556 | 1 | -12.0908 | -8.63445 | 1 | 0 | -20.359 | -58.4302 | -0.245801 | 3.46182 | 0.328811 |
| 4 | 2026-01-01 | BANKBEES | P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 1890 | 1.00919 | 1 | -17.5657 | -13.2116 | 1 | 0 | -25.8339 | -103.347 | -0.24621 | 3.45371 | 0.327634 |
| 4 | 2026-01-01 | BANKBEES | P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 880 | 0.971227 | 0.977273 | -10.8183 | -8.63042 | 1 | 0 | -19.0864 | -58.4302 | -0.245801 | 3.46259 | 0.328265 |
| 8 | 2026-01-01 | CIPLA | P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 2780 | 1.006 | 1 | -19.9899 | -13.6977 | 1 | 0 | -28.2581 | -142.935 | -0.680643 | 2.75461 | 0.56899 |
| 8 | 2026-01-01 | CIPLA | P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 2110 | 1.00971 | 1 | -24.9099 | -17.1116 | 1 | 0 | -33.178 | -164.884 | 0 | 2.74245 | 0.569378 |
| 8 | 2026-01-01 | CIPLA | P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 820 | 0.960819 | 0.970414 | -18.8154 | -9.57003 | 1 | 0 | -27.0835 | -142.935 | -0.680643 | 2.75167 | 0.567549 |
| 8 | 2026-01-01 | CIPLA | P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 440 | 0.962052 | 0.970367 | -18.2539 | -9.66999 | 1 | 0 | -26.522 | -164.884 | 0 | 2.75011 | 0.570297 |
| 11 | 2026-01-01 | HCLTECH | P68_FADE_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 160 | 0.956474 | 0.970377 | -14.3329 | -15.6216 | 1 | 0 | -22.6011 | -26.049 | -4.40546 | 2.40543 | 0.30405 |
| 11 | 2026-01-01 | HCLTECH | P68_FADE_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 440 | 1.00685 | 1 | -31.3304 | -15.6216 | 1 | 0 | -39.5985 | -157.59 | -4.40546 | 2.4033 | 0.302794 |
| 11 | 2026-01-01 | HCLTECH | P68_JOIN_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 240 | 0.955853 | 0.963114 | -29.0769 | -12.4137 | 1 | 0 | -37.3451 | -120.198 | -4.41696 | 2.41404 | 0.303974 |
| 11 | 2026-01-01 | HCLTECH | P68_JOIN_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 510 | 1.00112 | 1 | -28.2229 | -26.1633 | 1 | 0 | -36.491 | -120.198 | -4.41696 | 2.41656 | 0.30307 |
| 12 | 2026-01-01 | HDFCBANK | P68_JOIN_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 640 | 0.964062 | 0.96753 | -14.9791 | -9.51505 | 0.9375 | 0 | -23.2472 | -105.389 | 2.22045e-12 | 1.19929 | 0.571118 |
| 12 | 2026-01-01 | HDFCBANK | P68_FADE_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 1920 | 1.00689 | 1 | -25.1361 | -13.2219 | 1 | 0 | -33.4042 | -240.517 | 0 | 1.19426 | 0.571179 |
| 12 | 2026-01-01 | HDFCBANK | P68_FADE_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 480 | 0.939931 | 0.953488 | -33.8166 | -8.71105 | 1 | 0 | -42.0847 | -240.517 | 0 | 1.19614 | 0.570641 |
| 12 | 2026-01-01 | HDFCBANK | P68_JOIN_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 2860 | 1.01033 | 1 | -24.2338 | -17.4017 | 0.979021 | 0 | -32.5019 | -213.436 | 2.22045e-12 | 1.1995 | 0.571258 |
| 14 | 2026-01-01 | ICICIBANK | P68_JOIN_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 760 | 0.956723 | 0.964454 | -16.9295 | -11.1172 | 1 | 0 | -25.1976 | -61.9963 | -2.07569 | 1.3966 | 0.368118 |
| 14 | 2026-01-01 | ICICIBANK | P68_FADE_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 540 | 0.948057 | 0.952756 | -13.2768 | -8.28958 | 1 | 0 | -21.5449 | -58.7618 | -1.11022e-12 | 1.38969 | 0.366248 |
| 14 | 2026-01-01 | ICICIBANK | P68_JOIN_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 2940 | 1.01033 | 1 | -20.5673 | -14.5098 | 1 | 0 | -28.8354 | -69.8714 | -1.11022e-12 | 1.39602 | 0.367584 |
| 14 | 2026-01-01 | ICICIBANK | P68_FADE_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 2010 | 1.01105 | 1 | -26.8767 | -20.065 | 1 | 0 | -35.1448 | -294.158 | 0 | 1.39012 | 0.367808 |
| 16 | 2026-01-01 | ITBEES | P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I03_0p60_0p80 | R02_partial_0p50_1p00 | 400 | 0.964061 | 0.969972 | -14.4666 | -7.69361 | 1 | 0 | -22.7347 | -78.5219 | -1.53681 | 3.08318 | 0.739704 |
| 16 | 2026-01-01 | ITBEES | P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I03_0p60_0p80 | R03_rebuilt_1p00_1p50 | 1950 | 1.01166 | 1 | -19.2078 | -13.9427 | 1 | 0 | -27.4759 | -78.5219 | -1.53681 | 3.08596 | 0.74056 |
| 16 | 2026-01-01 | ITBEES | P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I03_0p60_0p80 | R02_partial_0p50_1p00 | 540 | 0.962063 | 0.970874 | -14.4729 | -10.8259 | 1 | 0 | -22.741 | -38.4615 | -1.53846 | 3.0962 | 0.740643 |
| 16 | 2026-01-01 | ITBEES | P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I03_0p60_0p80 | R03_rebuilt_1p00_1p50 | 2510 | 1.00721 | 1 | -15.7271 | -10.8259 | 1 | 0 | -23.9952 | -78.5099 | -1.53799 | 3.09061 | 0.74143 |
| 17 | 2026-01-01 | ITC | P68_FADE_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 740 | 0.971358 | 0.974874 | -12.9356 | -11.3102 | 1 | 0 | -21.2037 | -43.3552 | -0.872753 | 1.75622 | 0.509077 |
| 17 | 2026-01-01 | ITC | P68_JOIN_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 560 | 0.961016 | 0.973331 | -18.7017 | -7.9639 | 1 | 0 | -26.9698 | -196.799 | -0.873134 | 1.75209 | 0.511167 |
| 17 | 2026-01-01 | ITC | P68_FADE_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 2760 | 1.00724 | 1 | -17.2616 | -13.1142 | 1 | 0 | -25.5298 | -76.1688 | -0.872753 | 1.75588 | 0.50995 |
| 17 | 2026-01-01 | ITC | P68_JOIN_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 1890 | 1.0091 | 1 | -20.0404 | -14.9346 | 1 | 0 | -28.3085 | -196.799 | -0.873134 | 1.75115 | 0.510175 |
| 18 | 2026-01-01 | JUNIORBEES | P68_FADE_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I03_0p60_0p80 | R02_partial_0p50_1p00 | 320 | 0.959226 | 0.966942 | -27.0532 | -9.42783 | 1 | 0 | -35.3213 | -194.088 | 0 | 3.55249 | 0.696972 |
| 18 | 2026-01-01 | JUNIORBEES | P68_JOIN_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I03_0p60_0p80 | R02_partial_0p50_1p00 | 700 | 0.968042 | 0.967066 | -7.03199 | -4.99142 | 1 | 0 | -15.3001 | -27.8344 | 0 | 3.5568 | 0.696902 |
| 18 | 2026-01-01 | JUNIORBEES | P68_JOIN_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I03_0p60_0p80 | R03_rebuilt_1p00_1p50 | 3100 | 1.00622 | 1 | -13.8583 | -8.96351 | 1 | 0 | -22.1264 | -106.542 | 0 | 3.56112 | 0.697194 |
| 18 | 2026-01-01 | JUNIORBEES | P68_FADE_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I03_0p60_0p80 | R03_rebuilt_1p00_1p50 | 1780 | 1.00698 | 1 | -18.9533 | -13.6612 | 1 | 0 | -27.2214 | -194.088 | 0 | 3.55051 | 0.697216 |
| 23 | 2026-01-01 | NESTLEIND | P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 440 | 0.96922 | 0.970121 | -18.8899 | -7.48911 | 1 | 0 | -27.158 | -222.904 | 0 | 2.73295 | 0.414815 |
| 23 | 2026-01-01 | NESTLEIND | P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 40 | 0.908163 | 0.908163 | -1.36407 | -1.36407 | 1 | 0 | -9.63219 | -1.36407 | -1.36407 | 2.72777 | 0.4 |
| 23 | 2026-01-01 | NESTLEIND | P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 640 | 0.964533 | 0.966511 | -19.1325 | -13.0924 | 1 | 0 | -27.4006 | -196.239 | 0 | 2.7452 | 0.410998 |
| 23 | 2026-01-01 | NESTLEIND | P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 60 | 1 | 1 | -1.36407 | -1.36407 | 1 | 0 | -9.63219 | -1.36407 | -1.36407 | 2.72777 | 0.4 |
| 23 | 2026-01-01 | NESTLEIND | P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 2010 | 1.00998 | 1 | -24.7765 | -16.4813 | 1 | 0 | -33.0446 | -222.904 | 0 | 2.73767 | 0.413207 |
| 23 | 2026-01-01 | NESTLEIND | P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 2710 | 1.00678 | 1 | -20.1443 | -13.8523 | 1 | 0 | -28.4125 | -196.239 | 0 | 2.74467 | 0.412924 |
| 24 | 2026-01-01 | NIFTYBEES | P68_JOIN_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I03_0p60_0p80 | R02_partial_0p50_1p00 | 440 | 0.969335 | 0.970543 | -20.928 | -7.88336 | 1 | 0 | -29.1961 | -214.759 | -1.42699 | 1.42947 | 0.619661 |
| 24 | 2026-01-01 | NIFTYBEES | P68_FADE_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I03_0p60_0p80 | R02_partial_0p50_1p00 | 840 | 0.970476 | 0.983103 | -11.2197 | -6.0867 | 1 | 0 | -19.4879 | -71.4031 | -1.07124 | 1.43317 | 0.622436 |
| 24 | 2026-01-01 | NIFTYBEES | P68_JOIN_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I03_0p60_0p80 | R03_rebuilt_1p00_1p50 | 1910 | 1.01044 | 1 | -21.9598 | -13.5588 | 1 | 0 | -30.228 | -214.759 | -1.42699 | 1.4305 | 0.620564 |
| 24 | 2026-01-01 | NIFTYBEES | P68_FADE_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I03_0p60_0p80 | R03_rebuilt_1p00_1p50 | 2860 | 1.00503 | 1 | -17.5809 | -14.6241 | 1 | 0 | -25.849 | -114.241 | -1.07105 | 1.43506 | 0.622014 |
| 26 | 2026-01-01 | RELIANCE | P68_JOIN_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 520 | 0.949851 | 0.965543 | -11.9756 | -8.32807 | 1 | 0 | -20.2437 | -76.0657 | 0 | 1.50861 | 0.444061 |
| 26 | 2026-01-01 | RELIANCE | P68_FADE_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 780 | 0.955298 | 0.954751 | -17.0902 | -12.1313 | 1 | 0 | -25.3584 | -87.1198 | -2.24316 | 1.51241 | 0.444235 |
| 26 | 2026-01-01 | RELIANCE | P68_JOIN_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 2130 | 1.01448 | 1 | -24.9686 | -19.0389 | 1 | 0 | -33.2367 | -176.488 | 0 | 1.50809 | 0.44446 |
| 26 | 2026-01-01 | RELIANCE | P68_FADE_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 2670 | 1.00751 | 1 | -21.1479 | -16.4794 | 1 | 0 | -29.416 | -87.1198 | -2.24316 | 1.51354 | 0.444569 |
| 28 | 2026-01-01 | SUNPHARMA | P68_FADE_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 160 | 0.966993 | 0.969958 | -35.5737 | -13.7533 | 1 | 0 | -43.8418 | -179.821 | -1.52913 | 2.03742 | 0.306714 |
| 28 | 2026-01-01 | SUNPHARMA | P68_JOIN_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 1170 | 1.0089 | 1 | -17.6734 | -16.2585 | 1 | 0 | -25.9415 | -74.0778 | 0 | 2.04677 | 0.305566 |
| 28 | 2026-01-01 | SUNPHARMA | P68_FADE_IMBALANCE_REPLENISH | 1 | S02_1_2p5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 590 | 1.01136 | 1 | -33.782 | -19.2659 | 1 | 0 | -42.0502 | -179.821 | -1.52913 | 2.03842 | 0.3051 |
| 28 | 2026-01-01 | SUNPHARMA | P68_JOIN_IMBALANCE_REPLENISH | -1 | S02_1_2p5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 280 | 0.958106 | 0.957063 | -16.1181 | -12.4429 | 1 | 0 | -24.3862 | -74.0778 | 0 | 2.04896 | 0.305317 |
| 31 | 2026-01-01 | ULTRACEMCO | P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 480 | 0.965131 | 0.970639 | -9.88846 | -9.3116 | 1 | 0 | -18.1566 | -26.6464 | -1.26652 | 2.54299 | 0.435863 |
| 31 | 2026-01-01 | ULTRACEMCO | P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I01_0p30_0p40 | R03_rebuilt_1p00_1p50 | 60 | 1 | 1 | -13.1121 | -13.1121 | 1 | 0 | -21.3802 | -19.0275 | -7.19668 | 2.54216 | 0.391757 |
| 31 | 2026-01-01 | ULTRACEMCO | P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I02_0p40_0p60 | R02_partial_0p50_1p00 | 720 | 0.957829 | 0.977169 | -21.1735 | -9.30212 | 1 | 0 | -29.4416 | -152.475 | -0.422083 | 2.54906 | 0.434716 |
| 31 | 2026-01-01 | ULTRACEMCO | P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I01_0p30_0p40 | R02_partial_0p50_1p00 | 40 | 0.834196 | 0.834196 | -13.1121 | -13.1121 | 1 | 0 | -21.3802 | -19.0275 | -7.19668 | 2.54216 | 0.391757 |
| 31 | 2026-01-01 | ULTRACEMCO | P68_FADE_IMBALANCE_REPLENISH | -1 | S03_2p5_5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 2630 | 1.01026 | 1 | -21.7477 | -15.5894 | 1 | 0 | -30.0158 | -152.475 | -0.422083 | 2.54982 | 0.437147 |
| 31 | 2026-01-01 | ULTRACEMCO | P68_JOIN_IMBALANCE_REPLENISH | 1 | S03_2p5_5bp | I02_0p40_0p60 | R03_rebuilt_1p00_1p50 | 2020 | 1.01209 | 1 | -29.4568 | -15.7574 | 1 | 0 | -37.7249 | -248.387 | -1.26652 | 2.53971 | 0.437954 |

# Phase69 Spread-Transition Labels

Generated UTC: 2026-07-19T19:42:22.076328+00:00

Phase69 tests spread compression/expansion as a new feature family after replenishment-after-touch failed.
Labels are no-lookahead received-tick outcomes with marketable retail cost proxies.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase69_shards_scanned | 32 | Dense shards scanned |
| phase69_label_rows | 298 | Shard/symbol/spread-transition label rows |
| phase69_signal_rows | 319500 | No-lookahead spread-transition signal rows |
| phase69_bucket_rollup_rows | 28 | Aggregated spread-transition bucket rows |
| phase69_label_candidate_rows | 0 | Bucket rows passing spread-transition label gate |
| phase69_best_mean_after_cost_bps | -10.0305 | Best bucket mean after-cost bps |
| phase69_best_cost_clearing_rate | 0 | Best bucket cost-clearing rate |
| phase69_survives_spread_transition_gate | 0 | 1 means a spread-transition bucket deserves targeted replay |
| phase69_elapsed_seconds | 5.87652 | Elapsed seconds |
| phase69_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |
| phase69_recommend_next_action | advance_to_cross_symbol_lead_lag_feature_family | Recommended next action |

## Bucket Rollup

| strategy_id | transition_type | side | spread_bucket | spread_change_bucket | recent_return_bucket | shard_symbol_label_rows | symbols | trade_dates | signal_rows | mean_gross_bps | median_gross_bps | mean_after_cost_bps | mean_cost_clearing_rate | mean_adverse_direction_rate | worst_gross_bps | best_gross_bps | mean_spread_bps | mean_spread_change_bps | mean_abs_recent_return_bps | mean_cost_bps | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1 | 1 | 1 | 1150 | 0 | -0 | -10.0305 | 0 | 1 | -0 | -0 | 0.841616 | 0.0025569 | 30.2417 | 10.0305 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1 | 1 | 1 | 1150 | 0 | 0 | -10.0305 | 0 | 1 | 0 | 0 | 0.841616 | 0.0025569 | 30.2417 | 10.0305 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1 | 1 | 1 | 2100 | 0 | -0 | -10.0318 | 0 | 1 | -0 | -0 | 0.842483 | -0.00171332 | 20.322 | 10.0318 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1 | 1 | 1 | 2100 | 0 | 0 | -10.0318 | 0 | 1 | 0 | 0 | 0.842483 | -0.00171332 | 20.322 | 10.0318 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 20 | 20 | 1 | 49100 | 0 | -0 | -11.3863 | 0 | 1 | -0 | -0 | 1.74542 | -0.00478443 | 27.3838 | 11.3863 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 20 | 20 | 1 | 49100 | 0 | 0 | -11.3863 | 0 | 1 | 0 | 0 | 1.74542 | -0.00478443 | 27.3838 | 11.3863 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 20 | 20 | 1 | 32300 | 0 | -0 | -11.3897 | 0 | 1 | -0 | -0 | 1.74772 | 0.00621933 | 35.4839 | 11.3897 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 20 | 20 | 1 | 32300 | 0 | 0 | -11.3897 | 0 | 1 | 0 | 0 | 1.74772 | 0.00621933 | 35.4839 | 11.3897 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 20 | 20 | 1 | 8950 | 0 | -0 | -11.3912 | 0 | 1 | -0 | -0 | 1.74875 | -0.00140836 | 8.14565 | 11.3912 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 20 | 20 | 1 | 8950 | 0 | 0 | -11.3912 | 0 | 1 | 0 | 0 | 1.74875 | -0.00140836 | 8.14565 | 11.3912 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 20 | 20 | 1 | 6700 | 0 | 0 | -11.3916 | 0 | 1 | 0 | 0 | 1.74897 | 0.00137438 | 8.02363 | 11.3916 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 20 | 20 | 1 | 6700 | 0 | -0 | -11.3916 | 0 | 1 | -0 | -0 | 1.74897 | 0.00137438 | 8.02363 | 11.3916 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 2 | 2 | 1 | 250 | 0 | -0 | -12.041 | 0 | 1 | -0 | -0 | 2.18191 | -0.00107178 | 4.91171 | 12.041 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 2 | 2 | 1 | 250 | 0 | 0 | -12.041 | 0 | 1 | 0 | 0 | 2.18191 | -0.00107178 | 4.91171 | 12.041 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 1 | 1 | 1 | 50 | 0 | 0 | -12.0518 | 0 | 1 | 0 | 0 | 2.18914 | 0.00107775 | 4.92314 | 12.0518 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 1 | 1 | 1 | 50 | 0 | -0 | -12.0518 | 0 | 1 | -0 | -0 | 2.18914 | 0.00107775 | 4.92314 | 12.0518 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 10 | 10 | 1 | 1150 | 0 | 0 | -13.309 | 0 | 1 | 0 | 0 | 3.02725 | 0.00126203 | 4.16657 | 13.309 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 10 | 10 | 1 | 1150 | 0 | -0 | -13.309 | 0 | 1 | -0 | -0 | 3.02725 | 0.00126203 | 4.16657 | 13.309 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 11 | 11 | 1 | 7900 | 0 | -0 | -13.3116 | 0 | 1 | -0 | -0 | 3.02898 | -0.0023237 | 7.63706 | 13.3116 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 11 | 11 | 1 | 7900 | 0 | 0 | -13.3116 | 0 | 1 | 0 | 0 | 3.02898 | -0.0023237 | 7.63706 | 13.3116 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 11 | 11 | 1 | 4900 | 0 | 0 | -13.3172 | 0 | 1 | 0 | 0 | 3.03269 | 0.00218071 | 7.17074 | 13.3172 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 11 | 11 | 1 | 4900 | 0 | -0 | -13.3172 | 0 | 1 | -0 | -0 | 3.03269 | 0.00218071 | 7.17074 | 13.3172 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 11 | 11 | 1 | 25600 | 0 | 0 | -13.3185 | 0 | 1 | 0 | 0 | 3.0336 | -0.00779253 | 26.0576 | 13.3185 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 11 | 11 | 1 | 25600 | 0 | -0 | -13.3185 | 0 | 1 | -0 | -0 | 3.0336 | -0.00779253 | 26.0576 | 13.3185 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 10 | 10 | 1 | 2000 | 0 | -0 | -13.3208 | 0 | 1 | -0 | -0 | 3.03514 | -0.00123396 | 4.09125 | 13.3208 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 10 | 10 | 1 | 2000 | 0 | 0 | -13.3208 | 0 | 1 | 0 | 0 | 3.03514 | -0.00123396 | 4.09125 | 13.3208 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 11 | 11 | 1 | 17600 | 0 | -0 | -13.3223 | 0 | 1 | -0 | -0 | 3.03611 | 0.0100539 | 33.3327 | 13.3223 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 11 | 11 | 1 | 17600 | 0 | 0 | -13.3223 | 0 | 1 | 0 | 0 | 3.03611 | 0.0100539 | 33.3327 | 13.3223 | False |

## Strategy Rollup

| strategy_id | transition_type | side | shard_symbol_label_rows | symbols | trade_dates | signal_rows | mean_gross_bps | median_gross_bps | mean_after_cost_bps | mean_cost_clearing_rate | mean_adverse_direction_rate | worst_gross_bps | best_gross_bps | mean_spread_bps | mean_spread_change_bps | mean_abs_recent_return_bps | mean_cost_bps | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 75 | 32 | 1 | 95900 | 0 | 0 | -12.2107 | 0 | 1 | 0 | 0 | 2.29506 | -0.00335108 | 15.3639 | 12.2107 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | 75 | 32 | 1 | 95900 | 0 | -0 | -12.2107 | 0 | 1 | -0 | -0 | 2.29506 | -0.00335108 | 15.3639 | 12.2107 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 74 | 32 | 1 | 63850 | 0 | -0 | -12.2139 | 0 | 1 | -0 | -0 | 2.29721 | 0.00409068 | 18.8178 | 12.2139 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | 74 | 32 | 1 | 63850 | 0 | 0 | -12.2139 | 0 | 1 | 0 | 0 | 2.29721 | 0.00409068 | 18.8178 | 12.2139 | False |

## Symbol Rollup

| symbol | strategy_id | transition_type | side | shard_symbol_label_rows | symbols | trade_dates | signal_rows | mean_gross_bps | median_gross_bps | mean_after_cost_bps | mean_cost_clearing_rate | mean_adverse_direction_rate | worst_gross_bps | best_gross_bps | mean_spread_bps | mean_spread_change_bps | mean_abs_recent_return_bps | mean_cost_bps | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 1 | 1 | 1 | 1150 | 0 | -0 | -10.0305 | 0 | 1 | -0 | -0 | 0.841616 | 0.0025569 | 30.2417 | 10.0305 | False |
| GOLDBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 1 | 1 | 1 | 1150 | 0 | 0 | -10.0305 | 0 | 1 | 0 | 0 | 0.841616 | 0.0025569 | 30.2417 | 10.0305 | False |
| GOLDBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | 1 | 1 | 1 | 2100 | 0 | -0 | -10.0318 | 0 | 1 | -0 | -0 | 0.842483 | -0.00171332 | 20.322 | 10.0318 | False |
| GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 1 | 1 | 1 | 2100 | 0 | 0 | -10.0318 | 0 | 1 | 0 | 0 | 0.842483 | -0.00171332 | 20.322 | 10.0318 | False |
| HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 1500 | 0 | 0 | -10.5585 | 0 | 1 | 0 | 0 | 1.19359 | 0.00319413 | 26.5463 | 10.5585 | False |
| HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 1500 | 0 | -0 | -10.5585 | 0 | 1 | -0 | -0 | 1.19359 | 0.00319413 | 26.5463 | 10.5585 | False |
| HDFCBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 2600 | 0 | -0 | -10.5591 | 0 | 1 | -0 | -0 | 1.19401 | -0.00237974 | 19.9053 | 10.5591 | False |
| HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 2600 | 0 | 0 | -10.5591 | 0 | 1 | 0 | 0 | 1.19401 | -0.00237974 | 19.9053 | 10.5591 | False |
| M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 1750 | 0 | -0 | -10.6353 | 0 | 1 | -0 | -0 | 1.24477 | 0.00255523 | 20.4562 | 10.6353 | False |
| M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 1750 | 0 | 0 | -10.6353 | 0 | 1 | 0 | 0 | 1.24477 | 0.00255523 | 20.4562 | 10.6353 | False |
| M&M | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 2650 | 0 | -0 | -10.6417 | 0 | 1 | -0 | -0 | 1.24905 | -0.00219017 | 17.5662 | 10.6417 | False |
| M&M | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 2650 | 0 | 0 | -10.6417 | 0 | 1 | 0 | 0 | 1.24905 | -0.00219017 | 17.5662 | 10.6417 | False |
| LT | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 1650 | 0 | -0 | -10.6538 | 0 | 1 | -0 | -0 | 1.25714 | 0.00326691 | 25.9696 | 10.6538 | False |
| LT | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 1650 | 0 | 0 | -10.6538 | 0 | 1 | 0 | 0 | 1.25714 | 0.00326691 | 25.9696 | 10.6538 | False |
| LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 2750 | 0 | 0 | -10.6617 | 0 | 1 | 0 | 0 | 1.26238 | -0.00240271 | 19.1429 | 10.6617 | False |
| LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 2750 | 0 | -0 | -10.6617 | 0 | 1 | -0 | -0 | 1.26238 | -0.00240271 | 19.1429 | 10.6617 | False |
| ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 2050 | 0 | 0 | -10.859 | 0 | 1 | 0 | 0 | 1.3939 | 0.00305451 | 21.8086 | 10.859 | False |
| ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 2050 | 0 | -0 | -10.859 | 0 | 1 | -0 | -0 | 1.3939 | 0.00305451 | 21.8086 | 10.859 | False |
| ICICIBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 3100 | 0 | -0 | -10.8645 | 0 | 1 | -0 | -0 | 1.39758 | -0.00247307 | 17.7074 | 10.8645 | False |
| ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 3100 | 0 | 0 | -10.8645 | 0 | 1 | 0 | 0 | 1.39758 | -0.00247307 | 17.7074 | 10.8645 | False |
| NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 2250 | 0 | -0 | -10.9193 | 0 | 1 | -0 | -0 | 1.43413 | -0.00244119 | 17.0344 | 10.9193 | False |
| NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 2250 | 0 | 0 | -10.9193 | 0 | 1 | 0 | 0 | 1.43413 | -0.00244119 | 17.0344 | 10.9193 | False |
| NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 1650 | 0 | -0 | -10.9234 | 0 | 1 | -0 | -0 | 1.43684 | 0.00327156 | 22.7206 | 10.9234 | False |
| NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 1650 | 0 | 0 | -10.9234 | 0 | 1 | 0 | 0 | 1.43684 | 0.00327156 | 22.7206 | 10.9234 | False |
| AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 2800 | 0 | -0 | -10.9939 | 0 | 1 | -0 | -0 | 1.48386 | -0.00285627 | 19.2535 | 10.9939 | False |
| AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 2800 | 0 | 0 | -10.9939 | 0 | 1 | 0 | 0 | 1.48386 | -0.00285627 | 19.2535 | 10.9939 | False |
| AXISBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 1900 | 0 | 0 | -11.0003 | 0 | 1 | 0 | 0 | 1.48814 | 0.00326465 | 21.9025 | 11.0003 | False |
| AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 1900 | 0 | -0 | -11.0003 | 0 | 1 | -0 | -0 | 1.48814 | 0.00326465 | 21.9025 | 11.0003 | False |
| RELIANCE | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 2850 | 0 | -0 | -11.0346 | 0 | 1 | -0 | -0 | 1.51098 | -0.00274415 | 18.1606 | 11.0346 | False |
| RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 2850 | 0 | 0 | -11.0346 | 0 | 1 | 0 | 0 | 1.51098 | -0.00274415 | 18.1606 | 11.0346 | False |
| RELIANCE | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 1900 | 0 | 0 | -11.0357 | 0 | 1 | 0 | 0 | 1.5117 | 0.00318438 | 21.0181 | 11.0357 | False |
| RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 1900 | 0 | -0 | -11.0357 | 0 | 1 | -0 | -0 | 1.5117 | 0.00318438 | 21.0181 | 11.0357 | False |
| BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 1950 | 0 | -0 | -11.0965 | 0 | 1 | -0 | -0 | 1.55223 | 0.00269884 | 17.3695 | 11.0965 | False |
| BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 1950 | 0 | 0 | -11.0965 | 0 | 1 | 0 | 0 | 1.55223 | 0.00269884 | 17.3695 | 11.0965 | False |
| BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 2750 | 0 | -0 | -11.098 | 0 | 1 | -0 | -0 | 1.55328 | -0.00239569 | 15.4362 | 11.098 | False |
| BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 2750 | 0 | 0 | -11.098 | 0 | 1 | 0 | 0 | 1.55328 | -0.00239569 | 15.4362 | 11.098 | False |
| BPCL | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 2950 | 0 | -0 | -11.1748 | 0 | 1 | -0 | -0 | 1.60443 | -0.00307484 | 19.1641 | 11.1748 | False |
| BPCL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 2950 | 0 | 0 | -11.1748 | 0 | 1 | 0 | 0 | 1.60443 | -0.00307484 | 19.1641 | 11.1748 | False |
| BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 1900 | 0 | -0 | -11.1824 | 0 | 1 | -0 | -0 | 1.60952 | 0.00367817 | 22.8113 | 11.1824 | False |
| BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 1900 | 0 | 0 | -11.1824 | 0 | 1 | 0 | 0 | 1.60952 | 0.00367817 | 22.8113 | 11.1824 | False |
| ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 2750 | 0 | -0 | -11.3988 | 0 | 1 | -0 | -0 | 1.75381 | -0.00275786 | 15.7127 | 11.3988 | False |
| ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 2750 | 0 | 0 | -11.3988 | 0 | 1 | 0 | 0 | 1.75381 | -0.00275786 | 15.7127 | 11.3988 | False |
| ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 1850 | 0 | 0 | -11.4036 | 0 | 1 | 0 | 0 | 1.75701 | 0.00320886 | 18.2188 | 11.4036 | False |
| ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 1850 | 0 | -0 | -11.4036 | 0 | 1 | -0 | -0 | 1.75701 | 0.00320886 | 18.2188 | 11.4036 | False |
| INFY | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 3100 | 0 | -0 | -11.4267 | 0 | 1 | -0 | -0 | 1.77241 | -0.00320175 | 18.0496 | 11.4267 | False |
| INFY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 3100 | 0 | 0 | -11.4267 | 0 | 1 | 0 | 0 | 1.77241 | -0.00320175 | 18.0496 | 11.4267 | False |
| INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 2050 | 0 | -0 | -11.434 | 0 | 1 | -0 | -0 | 1.77723 | 0.00414667 | 23.2634 | 11.434 | False |
| INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 2050 | 0 | 0 | -11.434 | 0 | 1 | 0 | 0 | 1.77723 | 0.00414667 | 23.2634 | 11.434 | False |
| TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 3050 | 0 | 0 | -11.4645 | 0 | 1 | 0 | 0 | 1.79759 | -0.00283691 | 15.7592 | 11.4645 | False |
| TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 3050 | 0 | -0 | -11.4645 | 0 | 1 | -0 | -0 | 1.79759 | -0.00283691 | 15.7592 | 11.4645 | False |
| TCS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 2000 | 0 | 0 | -11.4828 | 0 | 1 | 0 | 0 | 1.8098 | 0.00323818 | 17.9008 | 11.4828 | False |
| TCS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 2000 | 0 | -0 | -11.4828 | 0 | 1 | -0 | -0 | 1.8098 | 0.00323818 | 17.9008 | 11.4828 | False |
| HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 2850 | 0 | -0 | -11.5295 | 0 | 1 | -0 | -0 | 1.84094 | -0.00287889 | 15.6086 | 11.5295 | False |
| HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 2850 | 0 | 0 | -11.5295 | 0 | 1 | 0 | 0 | 1.84094 | -0.00287889 | 15.6086 | 11.5295 | False |
| HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 2050 | 0 | 0 | -11.5371 | 0 | 1 | 0 | 0 | 1.84599 | 0.00352515 | 19.0106 | 11.5371 | False |
| HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 2050 | 0 | -0 | -11.5371 | 0 | 1 | -0 | -0 | 1.84599 | 0.00352515 | 19.0106 | 11.5371 | False |
| SBIN | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 3200 | 0 | -0 | -11.592 | 0 | 1 | -0 | -0 | 1.88259 | -0.00367643 | 19.5307 | 11.592 | False |
| SBIN | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 3200 | 0 | 0 | -11.592 | 0 | 1 | 0 | 0 | 1.88259 | -0.00367643 | 19.5307 | 11.592 | False |
| SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 1900 | 0 | 0 | -11.5928 | 0 | 1 | 0 | 0 | 1.88313 | 0.00484137 | 25.5513 | 11.5928 | False |
| SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 1900 | 0 | -0 | -11.5928 | 0 | 1 | -0 | -0 | 1.88313 | 0.00484137 | 25.5513 | 11.5928 | False |
| ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 3150 | 0 | 0 | -11.7474 | 0 | 1 | 0 | 0 | 1.98621 | -0.00355662 | 17.9132 | 11.7474 | False |
| ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 3150 | 0 | -0 | -11.7474 | 0 | 1 | -0 | -0 | 1.98621 | -0.00355662 | 17.9132 | 11.7474 | False |
| ONGC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 2000 | 0 | -0 | -11.7483 | 0 | 1 | -0 | -0 | 1.98677 | 0.00450503 | 22.5695 | 11.7483 | False |
| ONGC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 2000 | 0 | 0 | -11.7483 | 0 | 1 | 0 | 0 | 1.98677 | 0.00450503 | 22.5695 | 11.7483 | False |
| SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 1850 | 0 | -0 | -11.8311 | 0 | 1 | -0 | -0 | 2.04198 | 0.00450326 | 21.9632 | 11.8311 | False |
| SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 1850 | 0 | 0 | -11.8311 | 0 | 1 | 0 | 0 | 2.04198 | 0.00450326 | 21.9632 | 11.8311 | False |
| SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 3300 | 0 | 0 | -11.8353 | 0 | 1 | 0 | 0 | 2.04478 | -0.00356385 | 17.4496 | 11.8353 | False |
| SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 3300 | 0 | -0 | -11.8353 | 0 | 1 | -0 | -0 | 2.04478 | -0.00356385 | 17.4496 | 11.8353 | False |
| ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 2350 | 0 | -0 | -12.0174 | 0 | 1 | -0 | -0 | 2.16621 | 0.00494762 | 22.6996 | 12.0174 | False |
| ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 2350 | 0 | 0 | -12.0174 | 0 | 1 | 0 | 0 | 2.16621 | 0.00494762 | 22.6996 | 12.0174 | False |
| ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 3 | 1 | 1 | 3100 | 0 | 0 | -12.0211 | 0 | 1 | 0 | 0 | 2.16864 | -0.00305808 | 14.1218 | 12.0211 | False |
| ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | 3 | 1 | 1 | 3100 | 0 | -0 | -12.0211 | 0 | 1 | -0 | -0 | 2.16864 | -0.00305808 | 14.1218 | 12.0211 | False |
| WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 3 | 1 | 1 | 2200 | 0 | 0 | -12.0652 | 0 | 1 | 0 | 0 | 2.19807 | 0.00346932 | 15.7228 | 12.0652 | False |
| WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 3 | 1 | 1 | 2200 | 0 | -0 | -12.0652 | 0 | 1 | -0 | -0 | 2.19807 | 0.00346932 | 15.7228 | 12.0652 | False |
| WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | 3 | 1 | 1 | 3150 | 0 | -0 | -12.0688 | 0 | 1 | -0 | -0 | 2.20048 | -0.00281646 | 12.7888 | 12.0688 | False |
| WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 3 | 1 | 1 | 3150 | 0 | 0 | -12.0688 | 0 | 1 | 0 | 0 | 2.20048 | -0.00281646 | 12.7888 | 12.0688 | False |
| DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 2900 | 0 | -0 | -12.3497 | 0 | 1 | -0 | -0 | 2.38772 | -0.00360046 | 15.0548 | 12.3497 | False |
| DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 2900 | 0 | 0 | -12.3497 | 0 | 1 | 0 | 0 | 2.38772 | -0.00360046 | 15.0548 | 12.3497 | False |
| DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 2350 | 0 | 0 | -12.3579 | 0 | 1 | 0 | 0 | 2.3932 | 0.00451679 | 18.8212 | 12.3579 | False |
| DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 2350 | 0 | -0 | -12.3579 | 0 | 1 | -0 | -0 | 2.3932 | 0.00451679 | 18.8212 | 12.3579 | False |
| HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 3050 | 0 | 0 | -12.3895 | 0 | 1 | 0 | 0 | 2.41422 | -0.00515729 | 21.3917 | 12.3895 | False |
| HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 3050 | 0 | -0 | -12.3895 | 0 | 1 | -0 | -0 | 2.41422 | -0.00515729 | 21.3917 | 12.3895 | False |
| HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 2200 | 0 | -0 | -12.3909 | 0 | 1 | -0 | -0 | 2.41518 | 0.00567073 | 23.352 | 12.3909 | False |
| HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 2200 | 0 | 0 | -12.3909 | 0 | 1 | 0 | 0 | 2.41518 | 0.00567073 | 23.352 | 12.3909 | False |
| ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 3 | 1 | 1 | 3050 | 0 | 0 | -12.5778 | 0 | 1 | 0 | 0 | 2.53982 | -0.00367637 | 14.459 | 12.5778 | False |
| ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | 3 | 1 | 1 | 3050 | 0 | -0 | -12.5778 | 0 | 1 | -0 | -0 | 2.53982 | -0.00367637 | 14.459 | 12.5778 | False |
| ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 3 | 1 | 1 | 2200 | 0 | -0 | -12.5846 | 0 | 1 | -0 | -0 | 2.54434 | 0.00395319 | 15.4619 | 12.5846 | False |
| ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 3 | 1 | 1 | 2200 | 0 | 0 | -12.5846 | 0 | 1 | 0 | 0 | 2.54434 | 0.00395319 | 15.4619 | 12.5846 | False |
| KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | 3 | 1 | 1 | 3250 | 0 | -0 | -12.6613 | 0 | 1 | -0 | -0 | 2.59542 | -0.00313622 | 12.1144 | 12.6613 | False |
| KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 3 | 1 | 1 | 3250 | 0 | 0 | -12.6613 | 0 | 1 | 0 | 0 | 2.59542 | -0.00313622 | 12.1144 | 12.6613 | False |
| KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 3 | 1 | 1 | 2050 | 0 | 0 | -12.6666 | 0 | 1 | 0 | 0 | 2.59896 | 0.00423439 | 16.2631 | 12.6666 | False |
| KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 3 | 1 | 1 | 2050 | 0 | -0 | -12.6666 | 0 | 1 | -0 | -0 | 2.59896 | 0.00423439 | 16.2631 | 12.6666 | False |
| NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | 3 | 1 | 1 | 3100 | 0 | -0 | -12.877 | 0 | 1 | -0 | -0 | 2.73925 | -0.00368512 | 13.4573 | 12.877 | False |
| NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 3 | 1 | 1 | 3100 | 0 | 0 | -12.877 | 0 | 1 | 0 | 0 | 2.73925 | -0.00368512 | 13.4573 | 12.877 | False |
| NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 3 | 1 | 1 | 2200 | 0 | 0 | -12.88 | 0 | 1 | 0 | 0 | 2.74126 | 0.00451548 | 16.392 | 12.88 | False |
| NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 3 | 1 | 1 | 2200 | 0 | -0 | -12.88 | 0 | 1 | -0 | -0 | 2.74126 | 0.00451548 | 16.392 | 12.88 | False |
| CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 3 | 1 | 1 | 2350 | 0 | 0 | -12.8868 | 0 | 1 | 0 | 0 | 2.7458 | 0.00415139 | 15.0538 | 12.8868 | False |
| CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 3 | 1 | 1 | 2350 | 0 | -0 | -12.8868 | 0 | 1 | -0 | -0 | 2.7458 | 0.00415139 | 15.0538 | 12.8868 | False |
| CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 3 | 1 | 1 | 3250 | 0 | 0 | -12.9066 | 0 | 1 | 0 | 0 | 2.75901 | -0.00357349 | 12.9838 | 12.9066 | False |
| CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | 3 | 1 | 1 | 3250 | 0 | -0 | -12.9066 | 0 | 1 | -0 | -0 | 2.75901 | -0.00357349 | 12.9838 | 12.9066 | False |
| MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 3 | 1 | 1 | 2250 | 0 | -0 | -13.0446 | 0 | 1 | -0 | -0 | 2.85101 | 0.00447788 | 15.6293 | 13.0446 | False |
| MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 3 | 1 | 1 | 2250 | 0 | 0 | -13.0446 | 0 | 1 | 0 | 0 | 2.85101 | 0.00447788 | 15.6293 | 13.0446 | False |
| MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 3 | 1 | 1 | 3300 | 0 | 0 | -13.055 | 0 | 1 | 0 | 0 | 2.8579 | -0.00411669 | 14.4196 | 13.055 | False |
| MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | 3 | 1 | 1 | 3300 | 0 | -0 | -13.055 | 0 | 1 | -0 | -0 | 2.8579 | -0.00411669 | 14.4196 | 13.055 | False |
| BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 3 | 1 | 1 | 2200 | 0 | 0 | -13.0657 | 0 | 1 | 0 | 0 | 2.86502 | 0.00484984 | 16.8355 | 13.0657 | False |
| BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 3 | 1 | 1 | 2200 | 0 | -0 | -13.0657 | 0 | 1 | -0 | -0 | 2.86502 | 0.00484984 | 16.8355 | 13.0657 | False |
| BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 3 | 1 | 1 | 3450 | 0 | 0 | -13.0736 | 0 | 1 | 0 | 0 | 2.87033 | -0.00396009 | 13.8147 | 13.0736 | False |
| BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | 3 | 1 | 1 | 3450 | 0 | -0 | -13.0736 | 0 | 1 | -0 | -0 | 2.87033 | -0.00396009 | 13.8147 | 13.0736 | False |
| ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | 2 | 1 | 1 | 2750 | 0 | -0 | -13.3975 | 0 | 1 | -0 | -0 | 3.08628 | -0.00484038 | 15.6857 | 13.3975 | False |
| ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 2 | 1 | 1 | 2750 | 0 | 0 | -13.3975 | 0 | 1 | 0 | 0 | 3.08628 | -0.00484038 | 15.6857 | 13.3975 | False |
| ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 2 | 1 | 1 | 2000 | 0 | -0 | -13.4076 | 0 | 1 | -0 | -0 | 3.09301 | 0.00515279 | 16.655 | 13.4076 | False |
| ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 2 | 1 | 1 | 2000 | 0 | 0 | -13.4076 | 0 | 1 | 0 | 0 | 3.09301 | 0.00515279 | 16.655 | 13.4076 | False |
| TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 3 | 1 | 1 | 3250 | 0 | 0 | -13.6448 | 0 | 1 | 0 | 0 | 3.25114 | -0.0039265 | 12.0596 | 13.6448 | False |
| TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | 3 | 1 | 1 | 3250 | 0 | -0 | -13.6448 | 0 | 1 | -0 | -0 | 3.25114 | -0.0039265 | 12.0596 | 13.6448 | False |
| TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 3 | 1 | 1 | 2350 | 0 | -0 | -13.6549 | 0 | 1 | -0 | -0 | 3.25786 | 0.00489554 | 14.9872 | 13.6549 | False |
| TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 3 | 1 | 1 | 2350 | 0 | 0 | -13.6549 | 0 | 1 | 0 | 0 | 3.25786 | 0.00489554 | 14.9872 | 13.6549 | False |
| BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 3 | 1 | 1 | 2050 | 0 | 0 | -13.9501 | 0 | 1 | 0 | 0 | 3.45464 | 0.00417158 | 12.0476 | 13.9501 | False |
| BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 3 | 1 | 1 | 2050 | 0 | -0 | -13.9501 | 0 | 1 | -0 | -0 | 3.45464 | 0.00417158 | 12.0476 | 13.9501 | False |
| BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 3 | 1 | 1 | 3450 | 0 | 0 | -13.9525 | 0 | 1 | 0 | 0 | 3.45626 | -0.00368831 | 10.6632 | 13.9525 | False |
| BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | 3 | 1 | 1 | 3450 | 0 | -0 | -13.9525 | 0 | 1 | -0 | -0 | 3.45626 | -0.00368831 | 10.6632 | 13.9525 | False |
| JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 3 | 1 | 1 | 1950 | 0 | -0 | -14.0993 | 0 | 1 | -0 | -0 | 3.55412 | 0.00467526 | 13.108 | 14.0993 | False |
| JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 3 | 1 | 1 | 1950 | 0 | 0 | -14.0993 | 0 | 1 | 0 | 0 | 3.55412 | 0.00467526 | 13.108 | 14.0993 | False |
| JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 3 | 1 | 1 | 3450 | 0 | 0 | -14.102 | 0 | 1 | 0 | 0 | 3.55593 | -0.00400252 | 11.2588 | 14.102 | False |
| JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | 3 | 1 | 1 | 3450 | 0 | -0 | -14.102 | 0 | 1 | -0 | -0 | 3.55593 | -0.00400252 | 11.2588 | 14.102 | False |
| BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | 3 | 1 | 1 | 3200 | 0 | -0 | -14.2641 | 0 | 1 | -0 | -0 | 3.66399 | -0.00421385 | 11.4969 | 14.2641 | False |
| BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 3 | 1 | 1 | 3200 | 0 | 0 | -14.2641 | 0 | 1 | 0 | 0 | 3.66399 | -0.00421385 | 11.4969 | 14.2641 | False |
| BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 3 | 1 | 1 | 2050 | 0 | 0 | -14.2702 | 0 | 1 | 0 | 0 | 3.66808 | 0.00570734 | 15.5196 | 14.2702 | False |
| BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 3 | 1 | 1 | 2050 | 0 | -0 | -14.2702 | 0 | 1 | -0 | -0 | 3.66808 | 0.00570734 | 15.5196 | 14.2702 | False |

## Label Rows

| shard_index | trade_date | symbol | strategy_id | transition_type | side | spread_bucket | spread_change_bucket | recent_return_bucket | signal_rows | mean_gross_bps | median_gross_bps | mean_after_cost_bps | cost_clearing_rate | adverse_direction_rate | worst_gross_bps | best_gross_bps | mean_spread_bps | mean_spread_change_bps | mean_abs_recent_return_bps | mean_cost_bps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -12.0143 | 0 | 1 | -0 | -0 | 2.1641 | 0.00155494 | 7.1896 | 12.0143 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -12.0156 | 0 | 1 | -0 | -0 | 2.16497 | -0.00164283 | 7.58555 | 12.0156 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -12.0143 | 0 | 1 | 0 | 0 | 2.1641 | 0.00155494 | 7.1896 | 12.0143 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -12.0156 | 0 | 1 | 0 | 0 | 2.16497 | -0.00164283 | 7.58555 | 12.0156 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -12.0116 | 0 | 1 | 0 | 0 | 2.16229 | -0.00646272 | 29.8753 | 12.0116 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | -0 | -12.0206 | 0 | 1 | -0 | -0 | 2.16832 | 0.0083403 | 38.2097 | 12.0206 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -12.0361 | 0 | 1 | 0 | 0 | 2.17866 | -0.00106868 | 4.90439 | 12.0361 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -12.0361 | 0 | 1 | -0 | -0 | 2.17866 | -0.00106868 | 4.90439 | 12.0361 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -12.0116 | 0 | 1 | -0 | -0 | 2.16229 | -0.00646272 | 29.8753 | 12.0116 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | 0 | -12.0206 | 0 | 1 | 0 | 0 | 2.16832 | 0.0083403 | 38.2097 | 12.0206 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -10.9936 | 0 | 1 | 0 | 0 | 1.48367 | -0.00128428 | 8.65905 | 10.9936 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -11.005 | 0 | 1 | -0 | -0 | 1.49127 | 0.00133329 | 8.9396 | 11.005 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -10.9936 | 0 | 1 | -0 | -0 | 1.48367 | -0.00128428 | 8.65905 | 10.9936 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -11.005 | 0 | 1 | 0 | 0 | 1.49127 | 0.00133329 | 8.9396 | 11.005 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | 0 | -10.9956 | 0 | 1 | 0 | 0 | 1.485 | 0.005196 | 34.8653 | 10.9956 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | -0 | -10.9956 | 0 | 1 | -0 | -0 | 1.485 | 0.005196 | 34.8653 | 10.9956 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -10.9942 | 0 | 1 | -0 | -0 | 1.48404 | -0.00442826 | 29.848 | 10.9942 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -10.9942 | 0 | 1 | 0 | 0 | 1.48404 | -0.00442826 | 29.848 | 10.9942 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | -0 | -13.0821 | 0 | 1 | -0 | -0 | 2.87596 | -0.00117142 | 4.07442 | 13.0821 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -13.0747 | 0 | 1 | 0 | 0 | 2.87108 | 0.0110704 | 38.3749 | 13.0747 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | 0 | -13.0676 | 0 | 1 | 0 | 0 | 2.86632 | -0.00215877 | 7.53399 | 13.0676 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -13.0771 | 0 | 1 | 0 | 0 | 2.87267 | 0.00226015 | 7.85645 | 13.0771 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | 0 | -13.0712 | 0 | 1 | 0 | 0 | 2.86873 | -0.00855007 | 29.8356 | 13.0712 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -13.0451 | 0 | 1 | -0 | -0 | 2.8513 | 0.00121897 | 4.27513 | 13.0451 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -13.0451 | 0 | 1 | 0 | 0 | 2.8513 | 0.00121897 | 4.27513 | 13.0451 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -13.0771 | 0 | 1 | -0 | -0 | 2.87267 | 0.00226015 | 7.85645 | 13.0771 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | -0 | -13.0676 | 0 | 1 | -0 | -0 | 2.86632 | -0.00215877 | 7.53399 | 13.0676 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -13.0747 | 0 | 1 | -0 | -0 | 2.87108 | 0.0110704 | 38.3749 | 13.0747 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | 0 | -13.0821 | 0 | 1 | 0 | 0 | 2.87596 | -0.00117142 | 4.07442 | 13.0821 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | -0 | -13.0712 | 0 | 1 | -0 | -0 | 2.86873 | -0.00855007 | 29.8356 | 13.0712 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -13.9362 | 0 | 1 | -0 | -0 | 3.44538 | 0.00152485 | 4.42678 | 13.9362 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | -0 | -13.9631 | 0 | 1 | -0 | -0 | 3.46331 | 0.00853831 | 24.6254 | 13.9631 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -13.9599 | 0 | 1 | 0 | 0 | 3.46116 | -0.00706254 | 20.4023 | 13.9599 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 400 | 0 | -0 | -13.9487 | 0 | 1 | -0 | -0 | 3.45369 | -0.00135037 | 3.9087 | 13.9487 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 400 | 0 | 0 | -13.9487 | 0 | 1 | 0 | 0 | 3.45369 | -0.00135037 | 3.9087 | 13.9487 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -13.9599 | 0 | 1 | -0 | -0 | 3.46116 | -0.00706254 | 20.4023 | 13.9599 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -13.951 | 0 | 1 | 0 | 0 | 3.45522 | 0.00245158 | 7.09064 | 13.951 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -13.951 | 0 | 1 | -0 | -0 | 3.45522 | 0.00245158 | 7.09064 | 13.951 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1300 | 0 | -0 | -13.949 | 0 | 1 | -0 | -0 | 3.45392 | -0.00265201 | 7.67873 | 13.949 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | 0 | -13.9631 | 0 | 1 | 0 | 0 | 3.46331 | 0.00853831 | 24.6254 | 13.9631 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1300 | 0 | 0 | -13.949 | 0 | 1 | 0 | 0 | 3.45392 | -0.00265201 | 7.67873 | 13.949 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -13.9362 | 0 | 1 | 0 | 0 | 3.44538 | 0.00152485 | 4.42678 | 13.9362 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -11.1044 | 0 | 1 | 0 | 0 | 1.55749 | -0.00138489 | 8.89489 | 11.1044 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -11.0909 | 0 | 1 | 0 | 0 | 1.54852 | 0.00417706 | 26.8929 | 11.0909 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -11.0917 | 0 | 1 | -0 | -0 | 1.54908 | -0.00340649 | 21.9774 | 11.0917 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -11.0909 | 0 | 1 | -0 | -0 | 1.54852 | 0.00417706 | 26.8929 | 11.0909 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -11.102 | 0 | 1 | 0 | 0 | 1.55594 | 0.00122062 | 7.84606 | 11.102 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -11.1044 | 0 | 1 | -0 | -0 | 1.55749 | -0.00138489 | 8.89489 | 11.1044 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -11.102 | 0 | 1 | -0 | -0 | 1.55594 | 0.00122062 | 7.84606 | 11.102 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -11.0917 | 0 | 1 | 0 | 0 | 1.54908 | -0.00340649 | 21.9774 | 11.0917 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -11.1859 | 0 | 1 | 0 | 0 | 1.61185 | 0.00144698 | 8.97436 | 11.1859 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -11.1859 | 0 | 1 | -0 | -0 | 1.61185 | 0.00144698 | 8.97436 | 11.1859 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | -0 | -11.1766 | 0 | 1 | -0 | -0 | 1.60564 | -0.00140321 | 8.7386 | 11.1766 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | -0 | -11.1729 | 0 | 1 | -0 | -0 | 1.60321 | -0.00474646 | 29.5897 | 11.1729 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | 0 | -11.1766 | 0 | 1 | 0 | 0 | 1.60564 | -0.00140321 | 8.7386 | 11.1766 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | 0 | -11.1729 | 0 | 1 | 0 | 0 | 1.60321 | -0.00474646 | 29.5897 | 11.1729 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | 0 | -11.1789 | 0 | 1 | 0 | 0 | 1.60719 | 0.00590936 | 36.6482 | 11.1789 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | -0 | -11.1789 | 0 | 1 | -0 | -0 | 1.60719 | 0.00590936 | 36.6482 | 11.1789 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1350 | 0 | -0 | -14.2667 | 0 | 1 | -0 | -0 | 3.66569 | 0.0127278 | 34.582 | 14.2667 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -14.2614 | 0 | 1 | 0 | 0 | 3.6622 | 0.00290725 | 7.93323 | 14.2614 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -14.2827 | 0 | 1 | -0 | -0 | 3.67636 | 0.001487 | 4.04347 | 14.2827 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -14.2508 | 0 | 1 | 0 | 0 | 3.65515 | -0.00296871 | 8.11914 | 14.2508 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -14.2508 | 0 | 1 | -0 | -0 | 3.65515 | -0.00296871 | 8.11914 | 14.2508 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -14.2614 | 0 | 1 | -0 | -0 | 3.6622 | 0.00290725 | 7.93323 | 14.2614 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | 0 | -14.2759 | 0 | 1 | 0 | 0 | 3.67186 | -0.00129383 | 3.5218 | 14.2759 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1350 | 0 | 0 | -14.2667 | 0 | 1 | 0 | 0 | 3.66569 | 0.0127278 | 34.582 | 14.2667 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | -0 | -14.2759 | 0 | 1 | -0 | -0 | 3.67186 | -0.00129383 | 3.5218 | 14.2759 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -14.2656 | 0 | 1 | 0 | 0 | 3.66496 | -0.00837901 | 22.8498 | 14.2656 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -14.2656 | 0 | 1 | -0 | -0 | 3.66496 | -0.00837901 | 22.8498 | 14.2656 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -14.2827 | 0 | 1 | 0 | 0 | 3.67636 | 0.001487 | 4.04347 | 14.2827 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.9371 | 0 | 1 | 0 | 0 | 2.77932 | -0.00115918 | 4.17072 | 12.9371 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -12.8932 | 0 | 1 | 0 | 0 | 2.75003 | -0.00194557 | 7.08295 | 12.8932 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.8718 | 0 | 1 | 0 | 0 | 2.73579 | 0.00112222 | 4.102 | 12.8718 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.9371 | 0 | 1 | -0 | -0 | 2.77932 | -0.00115918 | 4.17072 | 12.9371 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.8718 | 0 | 1 | -0 | -0 | 2.73579 | 0.00112222 | 4.102 | 12.8718 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2550 | 0 | 0 | -12.8896 | 0 | 1 | 0 | 0 | 2.74768 | -0.00761572 | 27.6979 | 12.8896 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -12.8945 | 0 | 1 | 0 | 0 | 2.75094 | 0.00941041 | 34.0683 | 12.8945 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2550 | 0 | -0 | -12.8896 | 0 | 1 | -0 | -0 | 2.74768 | -0.00761572 | 27.6979 | 12.8896 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -12.8945 | 0 | 1 | -0 | -0 | 2.75094 | 0.00941041 | 34.0683 | 12.8945 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -12.8941 | 0 | 1 | 0 | 0 | 2.75068 | 0.00192152 | 6.99095 | 12.8941 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -12.8932 | 0 | 1 | -0 | -0 | 2.75003 | -0.00194557 | 7.08295 | 12.8932 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -12.8941 | 0 | 1 | -0 | -0 | 2.75068 | 0.00192152 | 6.99095 | 12.8941 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -12.3442 | 0 | 1 | -0 | -0 | 2.38403 | -0.00168064 | 7.04662 | 12.3442 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | 0 | -12.3585 | 0 | 1 | 0 | 0 | 2.3936 | 0.0018494 | 7.72476 | 12.3585 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2550 | 0 | -0 | -12.3552 | 0 | 1 | -0 | -0 | 2.39142 | -0.00552028 | 23.0629 | 12.3552 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2550 | 0 | 0 | -12.3552 | 0 | 1 | 0 | 0 | 2.39142 | -0.00552028 | 23.0629 | 12.3552 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | -0 | -12.3573 | 0 | 1 | -0 | -0 | 2.3928 | 0.00718417 | 29.9176 | 12.3573 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | 0 | -12.3573 | 0 | 1 | 0 | 0 | 2.3928 | 0.00718417 | 29.9176 | 12.3573 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | -0 | -12.3585 | 0 | 1 | -0 | -0 | 2.3936 | 0.0018494 | 7.72476 | 12.3585 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -12.3442 | 0 | 1 | 0 | 0 | 2.38403 | -0.00168064 | 7.04662 | 12.3442 |
| 10 | 2026-01-01 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1150 | 0 | 0 | -10.0305 | 0 | 1 | 0 | 0 | 0.841616 | 0.0025569 | 30.2417 | 10.0305 |
| 10 | 2026-01-01 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -10.0318 | 0 | 1 | 0 | 0 | 0.842483 | -0.00171332 | 20.322 | 10.0318 |
| 10 | 2026-01-01 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1150 | 0 | -0 | -10.0305 | 0 | 1 | -0 | -0 | 0.841616 | 0.0025569 | 30.2417 | 10.0305 |
| 10 | 2026-01-01 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -10.0318 | 0 | 1 | -0 | -0 | 0.842483 | -0.00171332 | 20.322 | 10.0318 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -12.3868 | 0 | 1 | -0 | -0 | 2.41243 | 0.00151737 | 6.29231 | 12.3868 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -12.3961 | 0 | 1 | 0 | 0 | 2.41865 | -0.00183271 | 7.57452 | 12.3961 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -12.395 | 0 | 1 | -0 | -0 | 2.41792 | 0.0098241 | 40.4117 | 12.395 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | 0 | -12.3828 | 0 | 1 | 0 | 0 | 2.40979 | -0.00848186 | 35.209 | 12.3828 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -12.3961 | 0 | 1 | -0 | -0 | 2.41865 | -0.00183271 | 7.57452 | 12.3961 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -12.3868 | 0 | 1 | 0 | 0 | 2.41243 | 0.00151737 | 6.29231 | 12.3868 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | -0 | -12.3828 | 0 | 1 | -0 | -0 | 2.40979 | -0.00848186 | 35.209 | 12.3828 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -12.395 | 0 | 1 | 0 | 0 | 2.41792 | 0.0098241 | 40.4117 | 12.395 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | -0 | -10.5664 | 0 | 1 | -0 | -0 | 1.19882 | 0.00525959 | 43.5948 | 10.5664 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -10.5543 | 0 | 1 | 0 | 0 | 1.19076 | -0.00106438 | 8.93868 | 10.5543 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | 0 | -10.5664 | 0 | 1 | 0 | 0 | 1.19882 | 0.00525959 | 43.5948 | 10.5664 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -10.5543 | 0 | 1 | -0 | -0 | 1.19076 | -0.00106438 | 8.93868 | 10.5543 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -10.5507 | 0 | 1 | -0 | -0 | 1.18835 | 0.00112868 | 9.4978 | 10.5507 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -10.564 | 0 | 1 | 0 | 0 | 1.19725 | -0.0036951 | 30.872 | 10.564 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -10.5507 | 0 | 1 | 0 | 0 | 1.18835 | 0.00112868 | 9.4978 | 10.5507 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -10.564 | 0 | 1 | -0 | -0 | 1.19725 | -0.0036951 | 30.872 | 10.564 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -11.5351 | 0 | 1 | 0 | 0 | 1.84466 | 0.00138129 | 7.48802 | 11.5351 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -11.5351 | 0 | 1 | -0 | -0 | 1.84466 | 0.00138129 | 7.48802 | 11.5351 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -11.5364 | 0 | 1 | -0 | -0 | 1.84555 | -0.00420236 | 22.7483 | 11.5364 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -11.5226 | 0 | 1 | 0 | 0 | 1.83634 | -0.00155543 | 8.46887 | 11.5226 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | 0 | -11.5391 | 0 | 1 | 0 | 0 | 1.84733 | 0.00566901 | 30.5331 | 11.5391 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | -0 | -11.5391 | 0 | 1 | -0 | -0 | 1.84733 | 0.00566901 | 30.5331 | 11.5391 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -11.5226 | 0 | 1 | -0 | -0 | 1.83634 | -0.00155543 | 8.46887 | 11.5226 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -11.5364 | 0 | 1 | 0 | 0 | 1.84555 | -0.00420236 | 22.7483 | 11.5364 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -10.8725 | 0 | 1 | 0 | 0 | 1.40291 | -0.00122086 | 8.70345 | 10.8725 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -10.8574 | 0 | 1 | 0 | 0 | 1.39287 | 0.00115016 | 8.26001 | 10.8574 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -10.8725 | 0 | 1 | -0 | -0 | 1.40291 | -0.00122086 | 8.70345 | 10.8725 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2600 | 0 | 0 | -10.8565 | 0 | 1 | 0 | 0 | 1.39226 | -0.00372529 | 26.7113 | 10.8565 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2600 | 0 | -0 | -10.8565 | 0 | 1 | -0 | -0 | 1.39226 | -0.00372529 | 26.7113 | 10.8565 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -10.8605 | 0 | 1 | 0 | 0 | 1.39494 | 0.00495885 | 35.3573 | 10.8605 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -10.8605 | 0 | 1 | -0 | -0 | 1.39494 | 0.00495885 | 35.3573 | 10.8605 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -10.8574 | 0 | 1 | -0 | -0 | 1.39287 | 0.00115016 | 8.26001 | 10.8574 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -11.4226 | 0 | 1 | -0 | -0 | 1.76964 | -0.00125332 | 7.08279 | 11.4226 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2650 | 0 | -0 | -11.4309 | 0 | 1 | -0 | -0 | 1.77517 | -0.00515018 | 29.0165 | 11.4309 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -11.4346 | 0 | 1 | 0 | 0 | 1.77766 | 0.00147373 | 8.2893 | 11.4346 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -11.4226 | 0 | 1 | 0 | 0 | 1.76964 | -0.00125332 | 7.08279 | 11.4226 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -11.4346 | 0 | 1 | -0 | -0 | 1.77766 | 0.00147373 | 8.2893 | 11.4346 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -11.4333 | 0 | 1 | -0 | -0 | 1.7768 | 0.0068196 | 38.2374 | 11.4333 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2650 | 0 | 0 | -11.4309 | 0 | 1 | 0 | 0 | 1.77517 | -0.00515018 | 29.0165 | 11.4309 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -11.4333 | 0 | 1 | 0 | 0 | 1.7768 | 0.0068196 | 38.2374 | 11.4333 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -13.4085 | 0 | 1 | 0 | 0 | 3.09356 | 0.00218346 | 7.06189 | 13.4085 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -13.4068 | 0 | 1 | 0 | 0 | 3.09246 | 0.00812211 | 26.248 | 13.4068 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -13.3977 | 0 | 1 | -0 | -0 | 3.08641 | -0.00721459 | 23.3787 | 13.3977 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -13.3977 | 0 | 1 | 0 | 0 | 3.08641 | -0.00721459 | 23.3787 | 13.3977 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -13.4068 | 0 | 1 | -0 | -0 | 3.09246 | 0.00812211 | 26.248 | 13.4068 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | -0 | -13.3973 | 0 | 1 | -0 | -0 | 3.08614 | -0.00246616 | 7.99261 | 13.3973 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | 0 | -13.3973 | 0 | 1 | 0 | 0 | 3.08614 | -0.00246616 | 7.99261 | 13.3973 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -13.4085 | 0 | 1 | -0 | -0 | 3.09356 | 0.00218346 | 7.06189 | 13.4085 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -11.3999 | 0 | 1 | 0 | 0 | 1.7545 | -0.00142649 | 8.12547 | 11.3999 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -11.4048 | 0 | 1 | -0 | -0 | 1.7578 | 0.00139175 | 7.91044 | 11.4048 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -11.3999 | 0 | 1 | -0 | -0 | 1.7545 | -0.00142649 | 8.12547 | 11.3999 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -11.4025 | 0 | 1 | 0 | 0 | 1.75622 | 0.00502597 | 28.5272 | 11.4025 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -11.3978 | 0 | 1 | -0 | -0 | 1.75312 | -0.00408923 | 23.2998 | 11.3978 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -11.3978 | 0 | 1 | 0 | 0 | 1.75312 | -0.00408923 | 23.2998 | 11.3978 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -11.4025 | 0 | 1 | -0 | -0 | 1.75622 | 0.00502597 | 28.5272 | 11.4025 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -11.4048 | 0 | 1 | 0 | 0 | 1.7578 | 0.00139175 | 7.91044 | 11.4048 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -14.1054 | 0 | 1 | 0 | 0 | 3.55818 | 0.00256609 | 7.21218 | 14.1054 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -14.1077 | 0 | 1 | -0 | -0 | 3.55971 | -0.00147284 | 4.14185 | 14.1077 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1200 | 0 | -0 | -14.0946 | 0 | 1 | -0 | -0 | 3.55099 | -0.00276141 | 7.77784 | 14.0946 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -14.1037 | 0 | 1 | -0 | -0 | 3.55707 | -0.0077733 | 21.8567 | 14.1037 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -14.1077 | 0 | 1 | 0 | 0 | 3.55971 | -0.00147284 | 4.14185 | 14.1077 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -14.0856 | 0 | 1 | -0 | -0 | 3.54498 | 0.00145088 | 4.09234 | 14.0856 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | 0 | -14.1069 | 0 | 1 | 0 | 0 | 3.55919 | 0.0100088 | 28.0196 | 14.1069 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1200 | 0 | 0 | -14.0946 | 0 | 1 | 0 | 0 | 3.55099 | -0.00276141 | 7.77784 | 14.0946 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -14.1054 | 0 | 1 | -0 | -0 | 3.55818 | 0.00256609 | 7.21218 | 14.1054 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -14.1037 | 0 | 1 | 0 | 0 | 3.55707 | -0.0077733 | 21.8567 | 14.1037 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | -0 | -14.1069 | 0 | 1 | -0 | -0 | 3.55919 | 0.0100088 | 28.0196 | 14.1069 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -14.0856 | 0 | 1 | 0 | 0 | 3.54498 | 0.00145088 | 4.09234 | 14.0856 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.7072 | 0 | 1 | -0 | -0 | 2.62605 | 0.00103401 | 3.93752 | 12.7072 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -12.7049 | 0 | 1 | -0 | -0 | 2.6245 | -0.00103361 | 3.9383 | 12.7049 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -12.6313 | 0 | 1 | 0 | 0 | 2.57548 | -0.00165836 | 6.44094 | 12.6313 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -12.6506 | 0 | 1 | 0 | 0 | 2.58835 | 0.00981462 | 37.667 | 12.6506 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -12.6506 | 0 | 1 | -0 | -0 | 2.58835 | 0.00981462 | 37.667 | 12.6506 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2950 | 0 | -0 | -12.6476 | 0 | 1 | -0 | -0 | 2.58629 | -0.00671668 | 25.964 | 12.6476 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -12.6419 | 0 | 1 | -0 | -0 | 2.58249 | 0.00185452 | 7.18471 | 12.6419 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -12.6313 | 0 | 1 | -0 | -0 | 2.57548 | -0.00165836 | 6.44094 | 12.6313 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.7072 | 0 | 1 | 0 | 0 | 2.62605 | 0.00103401 | 3.93752 | 12.7072 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -12.7049 | 0 | 1 | 0 | 0 | 2.6245 | -0.00103361 | 3.9383 | 12.7049 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2950 | 0 | 0 | -12.6476 | 0 | 1 | 0 | 0 | 2.58629 | -0.00671668 | 25.964 | 12.6476 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -12.6419 | 0 | 1 | 0 | 0 | 2.58249 | 0.00185452 | 7.18471 | 12.6419 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -10.6796 | 0 | 1 | -0 | -0 | 1.27431 | -0.00104012 | 8.16222 | 10.6796 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1500 | 0 | 0 | -10.6483 | 0 | 1 | 0 | 0 | 1.25342 | 0.00541211 | 43.0401 | 10.6483 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1500 | 0 | -0 | -10.6483 | 0 | 1 | -0 | -0 | 1.25342 | 0.00541211 | 43.0401 | 10.6483 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -10.6796 | 0 | 1 | 0 | 0 | 1.27431 | -0.00104012 | 8.16222 | 10.6796 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2650 | 0 | -0 | -10.6438 | 0 | 1 | -0 | -0 | 1.25046 | -0.0037653 | 30.1235 | 10.6438 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2650 | 0 | 0 | -10.6438 | 0 | 1 | 0 | 0 | 1.25046 | -0.0037653 | 30.1235 | 10.6438 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -10.6594 | 0 | 1 | -0 | -0 | 1.26087 | 0.0011217 | 8.89903 | 10.6594 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -10.6594 | 0 | 1 | 0 | 0 | 1.26087 | 0.0011217 | 8.89903 | 10.6594 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -10.65 | 0 | 1 | -0 | -0 | 1.25459 | -0.00117973 | 9.41 | 10.65 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -10.6377 | 0 | 1 | 0 | 0 | 1.24641 | 0.00120291 | 9.65034 | 10.6377 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -10.65 | 0 | 1 | 0 | 0 | 1.25459 | -0.00117973 | 9.41 | 10.65 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -10.6377 | 0 | 1 | -0 | -0 | 1.24641 | 0.00120291 | 9.65034 | 10.6377 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -10.6328 | 0 | 1 | 0 | 0 | 1.24312 | 0.00390755 | 31.262 | 10.6328 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2450 | 0 | -0 | -10.6334 | 0 | 1 | -0 | -0 | 1.24351 | -0.0032006 | 25.7224 | 10.6334 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2450 | 0 | 0 | -10.6334 | 0 | 1 | 0 | 0 | 1.24351 | -0.0032006 | 25.7224 | 10.6334 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -10.6328 | 0 | 1 | -0 | -0 | 1.24312 | 0.00390755 | 31.262 | 10.6328 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | 0 | -13.0427 | 0 | 1 | 0 | 0 | 2.84973 | -0.00232989 | 8.17708 | 13.0427 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -13.05 | 0 | 1 | 0 | 0 | 2.85455 | 0.0104012 | 36.2395 | 13.05 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | -0 | -13.0427 | 0 | 1 | -0 | -0 | 2.84973 | -0.00232989 | 8.17708 | 13.0427 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -13.0342 | 0 | 1 | -0 | -0 | 2.84406 | 0.00188044 | 6.6097 | 13.0342 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -13.0498 | 0 | 1 | 0 | 0 | 2.85443 | 0.00115201 | 4.03881 | 13.0498 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -13.05 | 0 | 1 | -0 | -0 | 2.85455 | 0.0104012 | 36.2395 | 13.05 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -13.0739 | 0 | 1 | -0 | -0 | 2.87052 | -0.00131734 | 4.59166 | 13.0739 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2200 | 0 | 0 | -13.0483 | 0 | 1 | 0 | 0 | 2.85346 | -0.00870285 | 30.4901 | 13.0483 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -13.0739 | 0 | 1 | 0 | 0 | 2.87052 | -0.00131734 | 4.59166 | 13.0739 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -13.0498 | 0 | 1 | -0 | -0 | 2.85443 | 0.00115201 | 4.03881 | 13.0498 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2200 | 0 | -0 | -13.0483 | 0 | 1 | -0 | -0 | 2.85346 | -0.00870285 | 30.4901 | 13.0483 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -13.0342 | 0 | 1 | 0 | 0 | 2.84406 | 0.00188044 | 6.6097 | 13.0342 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -12.8882 | 0 | 1 | -0 | -0 | 2.74671 | 0.00203471 | 7.4089 | 12.8882 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | 0 | -12.8654 | 0 | 1 | 0 | 0 | 2.73149 | 0.00116644 | 4.26812 | 12.8654 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -12.857 | 0 | 1 | 0 | 0 | 2.7259 | -0.00218946 | 8.03239 | 12.857 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | -0 | -12.8803 | 0 | 1 | -0 | -0 | 2.74143 | -0.00757887 | 27.6611 | 12.8803 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -12.8882 | 0 | 1 | 0 | 0 | 2.74671 | 0.00203471 | 7.4089 | 12.8882 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -12.8938 | 0 | 1 | 0 | 0 | 2.75043 | -0.00128703 | 4.67856 | 12.8938 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1500 | 0 | -0 | -12.8865 | 0 | 1 | -0 | -0 | 2.74558 | 0.0103453 | 37.499 | 12.8865 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | -0 | -12.8654 | 0 | 1 | -0 | -0 | 2.73149 | 0.00116644 | 4.26812 | 12.8654 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1500 | 0 | 0 | -12.8865 | 0 | 1 | 0 | 0 | 2.74558 | 0.0103453 | 37.499 | 12.8865 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -12.857 | 0 | 1 | -0 | -0 | 2.7259 | -0.00218946 | 8.03239 | 12.857 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -12.8938 | 0 | 1 | -0 | -0 | 2.75043 | -0.00128703 | 4.67856 | 12.8938 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | 0 | -12.8803 | 0 | 1 | 0 | 0 | 2.74143 | -0.00757887 | 27.6611 | 12.8803 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1250 | 0 | -0 | -10.9196 | 0 | 1 | -0 | -0 | 1.4343 | 0.0052685 | 36.5869 | 10.9196 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -10.9234 | 0 | 1 | -0 | -0 | 1.43683 | -0.00110193 | 7.66901 | 10.9234 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -10.9272 | 0 | 1 | -0 | -0 | 1.43939 | 0.00127462 | 8.85426 | 10.9272 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -10.9153 | 0 | 1 | -0 | -0 | 1.43142 | -0.00378044 | 26.3999 | 10.9153 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -10.9272 | 0 | 1 | 0 | 0 | 1.43939 | 0.00127462 | 8.85426 | 10.9272 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -10.9153 | 0 | 1 | 0 | 0 | 1.43142 | -0.00378044 | 26.3999 | 10.9153 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1250 | 0 | 0 | -10.9196 | 0 | 1 | 0 | 0 | 1.4343 | 0.0052685 | 36.5869 | 10.9196 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -10.9234 | 0 | 1 | 0 | 0 | 1.43683 | -0.00110193 | 7.66901 | 10.9234 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -11.751 | 0 | 1 | -0 | -0 | 1.98856 | -0.00137704 | 6.92144 | 11.751 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -11.7489 | 0 | 1 | -0 | -0 | 1.98718 | 0.00754743 | 37.7714 | 11.7489 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -11.7477 | 0 | 1 | 0 | 0 | 1.98636 | 0.00146263 | 7.3676 | 11.7477 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -11.751 | 0 | 1 | 0 | 0 | 1.98856 | -0.00137704 | 6.92144 | 11.751 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -11.7489 | 0 | 1 | 0 | 0 | 1.98718 | 0.00754743 | 37.7714 | 11.7489 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -11.7439 | 0 | 1 | 0 | 0 | 1.98387 | -0.0057362 | 28.9049 | 11.7439 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -11.7477 | 0 | 1 | -0 | -0 | 1.98636 | 0.00146263 | 7.3676 | 11.7477 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -11.7439 | 0 | 1 | -0 | -0 | 1.98387 | -0.0057362 | 28.9049 | 11.7439 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -11.0348 | 0 | 1 | -0 | -0 | 1.51114 | 0.00136893 | 9.05865 | 11.0348 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -11.0365 | 0 | 1 | -0 | -0 | 1.51226 | 0.00499983 | 32.9776 | 11.0365 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -11.0348 | 0 | 1 | 0 | 0 | 1.51114 | 0.00136893 | 9.05865 | 11.0348 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -11.0353 | 0 | 1 | 0 | 0 | 1.51146 | -0.00132173 | 8.74219 | 11.0353 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -11.0365 | 0 | 1 | 0 | 0 | 1.51226 | 0.00499983 | 32.9776 | 11.0365 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | 0 | -11.0339 | 0 | 1 | 0 | 0 | 1.5105 | -0.00416656 | 27.5791 | 11.0339 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -11.0353 | 0 | 1 | -0 | -0 | 1.51146 | -0.00132173 | 8.74219 | 11.0353 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | -0 | -11.0339 | 0 | 1 | -0 | -0 | 1.5105 | -0.00416656 | 27.5791 | 11.0339 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -11.5875 | 0 | 1 | -0 | -0 | 1.87955 | -0.00141087 | 7.51493 | 11.5875 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -11.5875 | 0 | 1 | 0 | 0 | 1.87955 | -0.00141087 | 7.51493 | 11.5875 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -11.5949 | 0 | 1 | -0 | -0 | 1.88453 | 0.00841711 | 44.3708 | 11.5949 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -11.5949 | 0 | 1 | 0 | 0 | 1.88453 | 0.00841711 | 44.3708 | 11.5949 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | 0 | -11.5966 | 0 | 1 | 0 | 0 | 1.88563 | -0.00594199 | 31.5465 | 11.5966 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -11.5907 | 0 | 1 | -0 | -0 | 1.88174 | 0.00126562 | 6.73178 | 11.5907 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -11.5907 | 0 | 1 | 0 | 0 | 1.88174 | 0.00126562 | 6.73178 | 11.5907 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | -0 | -11.5966 | 0 | 1 | -0 | -0 | 1.88563 | -0.00594199 | 31.5465 | 11.5966 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 950 | 0 | 0 | -11.8386 | 0 | 1 | 0 | 0 | 2.04701 | -0.00173794 | 8.49061 | 11.8386 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | -0 | -11.8373 | 0 | 1 | -0 | -0 | 2.04609 | 0.00767615 | 37.3955 | 11.8373 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -11.832 | 0 | 1 | -0 | -0 | 2.04255 | -0.00538977 | 26.4086 | 11.832 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 950 | 0 | -0 | -11.8386 | 0 | 1 | -0 | -0 | 2.04701 | -0.00173794 | 8.49061 | 11.8386 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | 0 | -11.8373 | 0 | 1 | 0 | 0 | 2.04609 | 0.00767615 | 37.3955 | 11.8373 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -11.832 | 0 | 1 | 0 | 0 | 2.04255 | -0.00538977 | 26.4086 | 11.832 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -11.8249 | 0 | 1 | -0 | -0 | 2.03786 | 0.00133037 | 6.53092 | 11.8249 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -11.8249 | 0 | 1 | 0 | 0 | 2.03786 | 0.00133037 | 6.53092 | 11.8249 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -11.4603 | 0 | 1 | -0 | -0 | 1.7948 | -0.00145843 | 8.12491 | 11.4603 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -11.4981 | 0 | 1 | 0 | 0 | 1.81996 | 0.00136544 | 7.50207 | 11.4981 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -11.4603 | 0 | 1 | 0 | 0 | 1.7948 | -0.00145843 | 8.12491 | 11.4603 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -11.4981 | 0 | 1 | -0 | -0 | 1.81996 | 0.00136544 | 7.50207 | 11.4981 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -11.4687 | 0 | 1 | -0 | -0 | 1.80039 | -0.00421539 | 23.3935 | 11.4687 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -11.4676 | 0 | 1 | 0 | 0 | 1.79965 | 0.00511092 | 28.2995 | 11.4676 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -11.4676 | 0 | 1 | -0 | -0 | 1.79965 | 0.00511092 | 28.2995 | 11.4676 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -11.4687 | 0 | 1 | 0 | 0 | 1.80039 | -0.00421539 | 23.3935 | 11.4687 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -13.6614 | 0 | 1 | 0 | 0 | 3.26216 | 0.00138523 | 4.24244 | 13.6614 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -13.6495 | 0 | 1 | -0 | -0 | 3.25423 | 0.00224085 | 6.88438 | 13.6495 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -13.6608 | 0 | 1 | 0 | 0 | 3.26179 | -0.00260485 | 7.99177 | 13.6608 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -13.6608 | 0 | 1 | -0 | -0 | 3.26179 | -0.00260485 | 7.99177 | 13.6608 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -13.6495 | 0 | 1 | 0 | 0 | 3.25423 | 0.00224085 | 6.88438 | 13.6495 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -13.6213 | 0 | 1 | 0 | 0 | 3.23548 | -0.0011868 | 3.66816 | 13.6213 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -13.6614 | 0 | 1 | -0 | -0 | 3.26216 | 0.00138523 | 4.24244 | 13.6614 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -13.6213 | 0 | 1 | -0 | -0 | 3.23548 | -0.0011868 | 3.66816 | 13.6213 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -13.6539 | 0 | 1 | 0 | 0 | 3.25719 | 0.0110605 | 33.8347 | 13.6539 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2700 | 0 | 0 | -13.6523 | 0 | 1 | 0 | 0 | 3.25614 | -0.00798785 | 24.5189 | 13.6523 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -13.6539 | 0 | 1 | -0 | -0 | 3.25719 | 0.0110605 | 33.8347 | 13.6539 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2700 | 0 | -0 | -13.6523 | 0 | 1 | -0 | -0 | 3.25614 | -0.00798785 | 24.5189 | 13.6523 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.5849 | 0 | 1 | 0 | 0 | 2.54453 | 0.00107865 | 4.23908 | 12.5849 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.563 | 0 | 1 | -0 | -0 | 2.52994 | -0.00106721 | 4.21834 | 12.563 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.5849 | 0 | 1 | -0 | -0 | 2.54453 | 0.00107865 | 4.23908 | 12.5849 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.563 | 0 | 1 | 0 | 0 | 2.52994 | -0.00106721 | 4.21834 | 12.563 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | -0 | -12.583 | 0 | 1 | -0 | -0 | 2.54328 | -0.00182554 | 7.18024 | 12.583 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -12.5775 | 0 | 1 | -0 | -0 | 2.53962 | 0.00168721 | 6.6451 | 12.5775 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -12.5775 | 0 | 1 | 0 | 0 | 2.53962 | 0.00168721 | 6.6451 | 12.5775 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | 0 | -12.5875 | 0 | 1 | 0 | 0 | 2.54623 | -0.00813636 | 31.9784 | 12.5875 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | 0 | -12.5914 | 0 | 1 | 0 | 0 | 2.54888 | 0.0090937 | 35.5014 | 12.5914 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | 0 | -12.583 | 0 | 1 | 0 | 0 | 2.54328 | -0.00182554 | 7.18024 | 12.583 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | -0 | -12.5875 | 0 | 1 | -0 | -0 | 2.54623 | -0.00813636 | 31.9784 | 12.5875 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | -0 | -12.5914 | 0 | 1 | -0 | -0 | 2.54888 | 0.0090937 | 35.5014 | 12.5914 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -12.0459 | 0 | 1 | -0 | -0 | 2.18516 | -0.00107488 | 4.91902 | 12.0459 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.0518 | 0 | 1 | 0 | 0 | 2.18914 | 0.00107775 | 4.92314 | 12.0518 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -12.0459 | 0 | 1 | 0 | 0 | 2.18516 | -0.00107488 | 4.91902 | 12.0459 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.0518 | 0 | 1 | -0 | -0 | 2.18914 | 0.00107775 | 4.92314 | 12.0518 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -12.0758 | 0 | 1 | 0 | 0 | 2.20515 | 0.00164725 | 7.46561 | 12.0758 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -12.0971 | 0 | 1 | 0 | 0 | 2.21932 | -0.00179036 | 8.05914 | 12.0971 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -12.0635 | 0 | 1 | -0 | -0 | 2.19695 | -0.00558414 | 25.3882 | 12.0635 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -12.0758 | 0 | 1 | -0 | -0 | 2.20515 | 0.00164725 | 7.46561 | 12.0758 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -12.0971 | 0 | 1 | -0 | -0 | 2.21932 | -0.00179036 | 8.05914 | 12.0971 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -12.068 | 0 | 1 | -0 | -0 | 2.19991 | 0.00768296 | 34.7796 | 12.068 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -12.068 | 0 | 1 | 0 | 0 | 2.19991 | 0.00768296 | 34.7796 | 12.068 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -12.0635 | 0 | 1 | 0 | 0 | 2.19695 | -0.00558414 | 25.3882 | 12.0635 |

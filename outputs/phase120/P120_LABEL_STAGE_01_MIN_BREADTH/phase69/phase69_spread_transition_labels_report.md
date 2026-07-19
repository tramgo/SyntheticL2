# Phase69 Spread-Transition Labels

Generated UTC: 2026-07-19T23:16:23.321425+00:00

Phase69 tests spread compression/expansion as a new feature family after replenishment-after-touch failed.
Labels are no-lookahead received-tick outcomes with marketable retail cost proxies.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase69_shards_scanned | 128 | Dense shards scanned |
| phase69_label_rows | 1254 | Shard/symbol/spread-transition label rows |
| phase69_signal_rows | 1312100 | No-lookahead spread-transition signal rows |
| phase69_bucket_rollup_rows | 46 | Aggregated spread-transition bucket rows |
| phase69_label_candidate_rows | 0 | Bucket rows passing spread-transition label gate |
| phase69_best_mean_after_cost_bps | -10.0382 | Best bucket mean after-cost bps |
| phase69_best_cost_clearing_rate | 0 | Best bucket cost-clearing rate |
| phase69_survives_spread_transition_gate | 0 | 1 means a spread-transition bucket deserves targeted replay |
| phase69_elapsed_seconds | 25.0073 | Elapsed seconds |
| phase69_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |
| phase69_recommend_next_action | advance_to_cross_symbol_lead_lag_feature_family | Recommended next action |

## Bucket Rollup

| strategy_id | transition_type | side | spread_bucket | spread_change_bucket | recent_return_bucket | shard_symbol_label_rows | symbols | trade_dates | signal_rows | mean_gross_bps | median_gross_bps | mean_after_cost_bps | mean_cost_clearing_rate | mean_adverse_direction_rate | worst_gross_bps | best_gross_bps | mean_spread_bps | mean_spread_change_bps | mean_abs_recent_return_bps | mean_cost_bps | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 3 | 1 | 3 | 5100 | 0 | 0 | -10.0382 | 0 | 1 | 0 | 0 | 0.846748 | -0.00213297 | 25.1839 | 10.0382 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 3 | 1 | 3 | 5100 | 0 | -0 | -10.0382 | 0 | 1 | -0 | -0 | 0.846748 | -0.00213297 | 25.1839 | 10.0382 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 3 | 1 | 3 | 4050 | 0 | 0 | -10.0399 | 0 | 1 | 0 | 0 | 0.847852 | 0.00232472 | 27.372 | 10.0399 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 3 | 1 | 3 | 4050 | 0 | -0 | -10.0399 | 0 | 1 | -0 | -0 | 0.847852 | 0.00232472 | 27.372 | 10.0399 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 60 | 20 | 3 | 29650 | 0 | 0 | -11.4185 | 0 | 1 | 0 | 0 | 1.76693 | 0.00141814 | 8.13381 | 11.4185 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 60 | 20 | 3 | 29650 | 0 | -0 | -11.4185 | 0 | 1 | -0 | -0 | 1.76693 | 0.00141814 | 8.13381 | 11.4185 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 60 | 20 | 3 | 108400 | 0 | 0 | -11.4193 | 0 | 1 | 0 | 0 | 1.76745 | 0.00518349 | 29.3205 | 11.4193 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 60 | 20 | 3 | 108400 | 0 | -0 | -11.4193 | 0 | 1 | -0 | -0 | 1.76745 | 0.00518349 | 29.3205 | 11.4193 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 59 | 20 | 3 | 23900 | 0 | 0 | -11.4305 | 0 | 1 | 0 | 0 | 1.77493 | -0.00141331 | 8.05049 | 11.4305 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 59 | 20 | 3 | 23900 | 0 | -0 | -11.4305 | 0 | 1 | -0 | -0 | 1.77493 | -0.00141331 | 8.05049 | 11.4305 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 61 | 21 | 4 | 124200 | 0 | 0 | -11.4308 | 0 | 1 | 0 | 0 | 1.77513 | -0.00507774 | 28.3836 | 11.4308 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 61 | 21 | 4 | 124200 | 0 | -0 | -11.4308 | 0 | 1 | -0 | -0 | 1.77513 | -0.00507774 | 28.3836 | 11.4308 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 5 | 4 | 2 | 700 | 0 | -0 | -12.2295 | 0 | 1 | -0 | -0 | 2.3076 | -0.00105165 | 4.57266 | 12.2295 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 5 | 4 | 2 | 700 | 0 | 0 | -12.2295 | 0 | 1 | 0 | 0 | 2.3076 | -0.00105165 | 4.57266 | 12.2295 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 8 | 4 | 3 | 850 | 0 | 0 | -12.2612 | 0 | 1 | 0 | 0 | 2.32869 | 0.00109397 | 4.70684 | 12.2612 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 8 | 4 | 3 | 850 | 0 | -0 | -12.2612 | 0 | 1 | -0 | -0 | 2.32869 | 0.00109397 | 4.70684 | 12.2612 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 49 | 25 | 4 | 9150 | 0 | 0 | -13.9204 | 0 | 1 | 0 | 0 | 3.43482 | 0.00138752 | 4.06292 | 13.9204 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 49 | 25 | 4 | 9150 | 0 | -0 | -13.9204 | 0 | 1 | -0 | -0 | 3.43482 | 0.00138752 | 4.06292 | 13.9204 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 57 | 30 | 4 | 26050 | 0 | 0 | -13.9303 | 0 | 1 | 0 | 0 | 3.44143 | 0.00249407 | 7.2629 | 13.9303 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 57 | 30 | 4 | 26050 | 0 | -0 | -13.9303 | 0 | 1 | -0 | -0 | 3.44143 | 0.00249407 | 7.2629 | 13.9303 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 58 | 30 | 4 | 24400 | 0 | -0 | -13.9682 | 0 | 1 | -0 | -0 | 3.46673 | -0.00261818 | 7.53408 | 13.9682 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 58 | 30 | 4 | 24400 | 0 | 0 | -13.9682 | 0 | 1 | 0 | 0 | 3.46673 | -0.00261818 | 7.53408 | 13.9682 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 59 | 31 | 4 | 139050 | 0 | 0 | -13.9691 | 0 | 1 | 0 | 0 | 3.46732 | -0.0128789 | 35.7717 | 13.9691 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 59 | 31 | 4 | 139050 | 0 | -0 | -13.9691 | 0 | 1 | -0 | -0 | 3.46732 | -0.0128789 | 35.7717 | 13.9691 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 59 | 31 | 4 | 113450 | 0 | 0 | -13.9825 | 0 | 1 | 0 | 0 | 3.47622 | 0.0144889 | 39.9785 | 13.9825 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 59 | 31 | 4 | 113450 | 0 | -0 | -13.9825 | 0 | 1 | -0 | -0 | 3.47622 | 0.0144889 | 39.9785 | 13.9825 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 44 | 23 | 4 | 7550 | 0 | -0 | -14.0463 | 0 | 1 | -0 | -0 | 3.51879 | -0.00146518 | 4.17478 | 14.0463 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 44 | 23 | 4 | 7550 | 0 | 0 | -14.0463 | 0 | 1 | 0 | 0 | 3.51879 | -0.00146518 | 4.17478 | 14.0463 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R01_0p25_2p5bp | 2 | 2 | 1 | 150 | 0 | 0 | -15.9597 | 0 | 1 | 0 | 0 | 4.79437 | 0.00114914 | 2.39661 | 15.9597 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R01_0p25_2p5bp | 2 | 2 | 1 | 150 | 0 | -0 | -15.9597 | 0 | 1 | -0 | -0 | 4.79437 | 0.00114914 | 2.39661 | 15.9597 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R01_0p25_2p5bp | 2 | 2 | 1 | 200 | 0 | -0 | -16.0762 | 0 | 1 | -0 | -0 | 4.87205 | -0.00118789 | 2.43662 | 16.0762 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R01_0p25_2p5bp | 2 | 2 | 1 | 200 | 0 | 0 | -16.0762 | 0 | 1 | 0 | 0 | 4.87205 | -0.00118789 | 2.43662 | 16.0762 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 5 | 5 | 1 | 450 | 0 | 0 | -16.9024 | 0 | 1 | 0 | 0 | 5.42286 | 0.0018869 | 3.50187 | 16.9024 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 5 | 5 | 1 | 450 | 0 | -0 | -16.9024 | 0 | 1 | -0 | -0 | 5.42286 | 0.0018869 | 3.50187 | 16.9024 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 7 | 7 | 1 | 19150 | 0 | 0 | -17.0339 | 0 | 1 | 0 | 0 | 5.51053 | -0.0219111 | 39.7988 | 17.0339 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 7 | 7 | 1 | 19150 | 0 | -0 | -17.0339 | 0 | 1 | -0 | -0 | 5.51053 | -0.0219111 | 39.7988 | 17.0339 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 7 | 7 | 1 | 2850 | 0 | 0 | -17.0341 | 0 | 1 | 0 | 0 | 5.51062 | 0.00398177 | 7.19752 | 17.0341 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 7 | 7 | 1 | 2850 | 0 | -0 | -17.0341 | 0 | 1 | -0 | -0 | 5.51062 | 0.00398177 | 7.19752 | 17.0341 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 7 | 7 | 1 | 1900 | 0 | -0 | -17.0466 | 0 | 1 | -0 | -0 | 5.51899 | -0.00408386 | 7.42061 | 17.0466 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 7 | 7 | 1 | 1900 | 0 | 0 | -17.0466 | 0 | 1 | 0 | 0 | 5.51899 | -0.00408386 | 7.42061 | 17.0466 | False |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 7 | 7 | 1 | 14250 | 0 | 0 | -17.0555 | 0 | 1 | 0 | 0 | 5.52489 | 0.0296257 | 53.595 | 17.0555 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 7 | 7 | 1 | 14250 | 0 | -0 | -17.0555 | 0 | 1 | -0 | -0 | 5.52489 | 0.0296257 | 53.595 | 17.0555 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 4 | 4 | 1 | 400 | 0 | -0 | -17.1265 | 0 | 1 | -0 | -0 | 5.57222 | -0.00197834 | 3.55178 | 17.1265 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 4 | 4 | 1 | 400 | 0 | 0 | -17.1265 | 0 | 1 | 0 | 0 | 5.57222 | -0.00197834 | 3.55178 | 17.1265 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R01_0p25_2p5bp | 1 | 1 | 1 | 200 | 0 | -0 | -17.6841 | 0 | 1 | -0 | -0 | 5.94398 | -0.00146548 | 2.46589 | 17.6841 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R01_0p25_2p5bp | 1 | 1 | 1 | 200 | 0 | 0 | -17.6841 | 0 | 1 | 0 | 0 | 5.94398 | -0.00146548 | 2.46589 | 17.6841 | False |

## Strategy Rollup

| strategy_id | transition_type | side | shard_symbol_label_rows | symbols | trade_dates | signal_rows | mean_gross_bps | median_gross_bps | mean_after_cost_bps | mean_cost_clearing_rate | mean_adverse_direction_rate | worst_gross_bps | best_gross_bps | mean_spread_bps | mean_spread_change_bps | mean_abs_recent_return_bps | mean_cost_bps | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P69_SPREAD_TRANSITION_FADE | expansion | 1 | 317 | 32 | 4 | 309300 | 0 | 0 | -13.1061 | 0 | 1 | 0 | 0 | 2.89196 | 0.00543787 | 18.2545 | 13.1061 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 317 | 32 | 4 | 309300 | 0 | -0 | -13.1061 | 0 | 1 | -0 | -0 | 2.89196 | 0.00543787 | 18.2545 | 13.1061 | False |
| P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 310 | 32 | 4 | 346750 | 0 | 0 | -13.1362 | 0 | 1 | 0 | 0 | 2.91205 | -0.00507961 | 17.3809 | 13.1362 | False |
| P69_SPREAD_TRANSITION_FADE | compression | -1 | 310 | 32 | 4 | 346750 | 0 | -0 | -13.1362 | 0 | 1 | -0 | -0 | 2.91205 | -0.00507961 | 17.3809 | 13.1362 | False |

## Symbol Rollup

| symbol | strategy_id | transition_type | side | shard_symbol_label_rows | symbols | trade_dates | signal_rows | mean_gross_bps | median_gross_bps | mean_after_cost_bps | mean_cost_clearing_rate | mean_adverse_direction_rate | worst_gross_bps | best_gross_bps | mean_spread_bps | mean_spread_change_bps | mean_abs_recent_return_bps | mean_cost_bps | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 6 | 1 | 4 | 8150 | 0 | 0 | -11.2949 | 0 | 1 | 0 | 0 | 1.68453 | -0.00571454 | 31.144 | 11.2949 | False |
| GOLDBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | 6 | 1 | 4 | 8150 | 0 | -0 | -11.2949 | 0 | 1 | -0 | -0 | 1.68453 | -0.00571454 | 31.144 | 11.2949 | False |
| GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 6 | 1 | 4 | 6550 | 0 | -0 | -11.3058 | 0 | 1 | -0 | -0 | 1.6918 | 0.00366092 | 23.4967 | 11.3058 | False |
| GOLDBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 6 | 1 | 4 | 6550 | 0 | 0 | -11.3058 | 0 | 1 | 0 | 0 | 1.6918 | 0.00366092 | 23.4967 | 11.3058 | False |
| HDFCBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | 7 | 1 | 4 | 10350 | 0 | -0 | -11.3181 | 0 | 1 | -0 | -0 | 1.69998 | -0.00401114 | 23.1265 | 11.3181 | False |
| HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 7 | 1 | 4 | 10350 | 0 | 0 | -11.3181 | 0 | 1 | 0 | 0 | 1.69998 | -0.00401114 | 23.1265 | 11.3181 | False |
| M&M | P69_SPREAD_TRANSITION_FADE | compression | -1 | 8 | 1 | 4 | 9950 | 0 | -0 | -11.4612 | 0 | 1 | -0 | -0 | 1.7954 | -0.00404829 | 20.6988 | 11.4612 | False |
| M&M | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 8 | 1 | 4 | 9950 | 0 | 0 | -11.4612 | 0 | 1 | 0 | 0 | 1.7954 | -0.00404829 | 20.6988 | 11.4612 | False |
| HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 9 | 1 | 4 | 8800 | 0 | 0 | -11.4634 | 0 | 1 | 0 | 0 | 1.79684 | 0.00393688 | 21.6482 | 11.4634 | False |
| HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 9 | 1 | 4 | 8800 | 0 | -0 | -11.4634 | 0 | 1 | -0 | -0 | 1.79684 | 0.00393688 | 21.6482 | 11.4634 | False |
| LT | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 8 | 1 | 4 | 8600 | 0 | -0 | -11.4931 | 0 | 1 | -0 | -0 | 1.81662 | 0.00489171 | 23.3927 | 11.4931 | False |
| LT | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 8 | 1 | 4 | 8600 | 0 | 0 | -11.4931 | 0 | 1 | 0 | 0 | 1.81662 | 0.00489171 | 23.3927 | 11.4931 | False |
| RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 8 | 1 | 4 | 10300 | 0 | 0 | -11.602 | 0 | 1 | 0 | 0 | 1.88928 | -0.00431916 | 20.9 | 11.602 | False |
| RELIANCE | P69_SPREAD_TRANSITION_FADE | compression | -1 | 8 | 1 | 4 | 10300 | 0 | -0 | -11.602 | 0 | 1 | -0 | -0 | 1.88928 | -0.00431916 | 20.9 | 11.602 | False |
| RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 8 | 1 | 4 | 9150 | 0 | -0 | -11.6131 | 0 | 1 | -0 | -0 | 1.89667 | 0.00465236 | 22.3433 | 11.6131 | False |
| RELIANCE | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 8 | 1 | 4 | 9150 | 0 | 0 | -11.6131 | 0 | 1 | 0 | 0 | 1.89667 | 0.00465236 | 22.3433 | 11.6131 | False |
| ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 8 | 1 | 4 | 10700 | 0 | 0 | -11.6414 | 0 | 1 | 0 | 0 | 1.91551 | -0.00437985 | 20.5687 | 11.6414 | False |
| ICICIBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | 8 | 1 | 4 | 10700 | 0 | -0 | -11.6414 | 0 | 1 | -0 | -0 | 1.91551 | -0.00437985 | 20.5687 | 11.6414 | False |
| M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 9 | 1 | 4 | 8800 | 0 | -0 | -11.7397 | 0 | 1 | -0 | -0 | 1.98105 | 0.00415694 | 20.0404 | 11.7397 | False |
| M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 9 | 1 | 4 | 8800 | 0 | 0 | -11.7397 | 0 | 1 | 0 | 0 | 1.98105 | 0.00415694 | 20.0404 | 11.7397 | False |
| LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 9 | 1 | 4 | 9600 | 0 | 0 | -11.7489 | 0 | 1 | 0 | 0 | 1.98719 | -0.00396388 | 19.4488 | 11.7489 | False |
| LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | 9 | 1 | 4 | 9600 | 0 | -0 | -11.7489 | 0 | 1 | -0 | -0 | 1.98719 | -0.00396388 | 19.4488 | 11.7489 | False |
| AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 8 | 1 | 4 | 9350 | 0 | -0 | -11.8436 | 0 | 1 | -0 | -0 | 2.05029 | 0.0047476 | 21.4071 | 11.8436 | False |
| AXISBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 8 | 1 | 4 | 9350 | 0 | 0 | -11.8436 | 0 | 1 | 0 | 0 | 2.05029 | 0.0047476 | 21.4071 | 11.8436 | False |
| ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 9 | 1 | 4 | 9950 | 0 | 0 | -11.9159 | 0 | 1 | 0 | 0 | 2.09852 | 0.00420604 | 19.4126 | 11.9159 | False |
| ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 9 | 1 | 4 | 9950 | 0 | -0 | -11.9159 | 0 | 1 | -0 | -0 | 2.09852 | 0.00420604 | 19.4126 | 11.9159 | False |
| NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | 9 | 1 | 4 | 9350 | 0 | -0 | -11.9984 | 0 | 1 | -0 | -0 | 2.15351 | -0.00351927 | 16.458 | 11.9984 | False |
| NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 9 | 1 | 4 | 9350 | 0 | 0 | -11.9984 | 0 | 1 | 0 | 0 | 2.15351 | -0.00351927 | 16.458 | 11.9984 | False |
| NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 9 | 1 | 4 | 8350 | 0 | 0 | -12.0121 | 0 | 1 | 0 | 0 | 2.16266 | 0.00396589 | 18.4732 | 12.0121 | False |
| NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 9 | 1 | 4 | 8350 | 0 | -0 | -12.0121 | 0 | 1 | -0 | -0 | 2.16266 | 0.00396589 | 18.4732 | 12.0121 | False |
| AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 9 | 1 | 4 | 11250 | 0 | 0 | -12.1171 | 0 | 1 | 0 | 0 | 2.23263 | -0.00416733 | 18.9407 | 12.1171 | False |
| AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | 9 | 1 | 4 | 11250 | 0 | -0 | -12.1171 | 0 | 1 | -0 | -0 | 2.23263 | -0.00416733 | 18.9407 | 12.1171 | False |
| BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 9 | 1 | 4 | 9600 | 0 | -0 | -12.1257 | 0 | 1 | -0 | -0 | 2.23838 | 0.00466054 | 19.4155 | 12.1257 | False |
| BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 9 | 1 | 4 | 9600 | 0 | 0 | -12.1257 | 0 | 1 | 0 | 0 | 2.23838 | 0.00466054 | 19.4155 | 12.1257 | False |
| BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 9 | 1 | 4 | 10400 | 0 | 0 | -12.1346 | 0 | 1 | 0 | 0 | 2.24433 | -0.00424409 | 18.4207 | 12.1346 | False |
| BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | 9 | 1 | 4 | 10400 | 0 | -0 | -12.1346 | 0 | 1 | -0 | -0 | 2.24433 | -0.00424409 | 18.4207 | 12.1346 | False |
| TCS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 8 | 1 | 4 | 9550 | 0 | 0 | -12.1756 | 0 | 1 | 0 | 0 | 2.27163 | 0.00565499 | 22.3327 | 12.1756 | False |
| TCS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 8 | 1 | 4 | 9550 | 0 | -0 | -12.1756 | 0 | 1 | -0 | -0 | 2.27163 | 0.00565499 | 22.3327 | 12.1756 | False |
| SBIN | P69_SPREAD_TRANSITION_FADE | compression | -1 | 8 | 1 | 4 | 11100 | 0 | -0 | -12.3092 | 0 | 1 | -0 | -0 | 2.3607 | -0.0055851 | 21.8687 | 12.3092 | False |
| SBIN | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 8 | 1 | 4 | 11100 | 0 | 0 | -12.3092 | 0 | 1 | 0 | 0 | 2.3607 | -0.0055851 | 21.8687 | 12.3092 | False |
| BPCL | P69_SPREAD_TRANSITION_FADE | compression | -1 | 8 | 1 | 4 | 10700 | 0 | -0 | -12.3717 | 0 | 1 | -0 | -0 | 2.40238 | -0.00543181 | 20.3946 | 12.3717 | False |
| BPCL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 8 | 1 | 4 | 10700 | 0 | 0 | -12.3717 | 0 | 1 | 0 | 0 | 2.40238 | -0.00543181 | 20.3946 | 12.3717 | False |
| TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 9 | 1 | 4 | 11150 | 0 | 0 | -12.3871 | 0 | 1 | 0 | 0 | 2.41263 | -0.00439011 | 18.1196 | 12.3871 | False |
| TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | 9 | 1 | 4 | 11150 | 0 | -0 | -12.3871 | 0 | 1 | -0 | -0 | 2.41263 | -0.00439011 | 18.1196 | 12.3871 | False |
| INFY | P69_SPREAD_TRANSITION_FADE | compression | -1 | 8 | 1 | 4 | 11100 | 0 | -0 | -12.4424 | 0 | 1 | -0 | -0 | 2.44955 | -0.0053464 | 20.7137 | 12.4424 | False |
| INFY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 8 | 1 | 4 | 11100 | 0 | 0 | -12.4424 | 0 | 1 | 0 | 0 | 2.44955 | -0.0053464 | 20.7137 | 12.4424 | False |
| ONGC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 8 | 1 | 4 | 9800 | 0 | -0 | -12.505 | 0 | 1 | -0 | -0 | 2.49124 | 0.00612227 | 22.4597 | 12.505 | False |
| ONGC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 8 | 1 | 4 | 9800 | 0 | 0 | -12.505 | 0 | 1 | 0 | 0 | 2.49124 | 0.00612227 | 22.4597 | 12.505 | False |
| SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 9 | 1 | 4 | 10000 | 0 | 0 | -12.5462 | 0 | 1 | 0 | 0 | 2.5187 | 0.00538975 | 20.8665 | 12.5462 | False |
| SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 9 | 1 | 4 | 10000 | 0 | -0 | -12.5462 | 0 | 1 | -0 | -0 | 2.5187 | 0.00538975 | 20.8665 | 12.5462 | False |
| ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 10 | 1 | 4 | 10400 | 0 | 0 | -12.6894 | 0 | 1 | 0 | 0 | 2.61417 | 0.00603394 | 20.019 | 12.6894 | False |
| ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 10 | 1 | 4 | 10400 | 0 | -0 | -12.6894 | 0 | 1 | -0 | -0 | 2.61417 | 0.00603394 | 20.019 | 12.6894 | False |
| HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 9 | 1 | 4 | 9500 | 0 | -0 | -12.7083 | 0 | 1 | -0 | -0 | 2.6268 | 0.0045948 | 17.3049 | 12.7083 | False |
| HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 9 | 1 | 4 | 9500 | 0 | 0 | -12.7083 | 0 | 1 | 0 | 0 | 2.6268 | 0.0045948 | 17.3049 | 12.7083 | False |
| HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 9 | 1 | 4 | 10450 | 0 | 0 | -12.7147 | 0 | 1 | 0 | 0 | 2.63105 | -0.00438809 | 16.4578 | 12.7147 | False |
| HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | 9 | 1 | 4 | 10450 | 0 | -0 | -12.7147 | 0 | 1 | -0 | -0 | 2.63105 | -0.00438809 | 16.4578 | 12.7147 | False |
| ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 9 | 1 | 4 | 11150 | 0 | 0 | -12.7265 | 0 | 1 | 0 | 0 | 2.6389 | -0.00488787 | 18.3178 | 12.7265 | False |
| ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | 9 | 1 | 4 | 11150 | 0 | -0 | -12.7265 | 0 | 1 | -0 | -0 | 2.6389 | -0.00488787 | 18.3178 | 12.7265 | False |
| BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 9 | 1 | 4 | 9300 | 0 | 0 | -12.7511 | 0 | 1 | 0 | 0 | 2.65533 | 0.00607366 | 21.1905 | 12.7511 | False |
| BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 9 | 1 | 4 | 9300 | 0 | -0 | -12.7511 | 0 | 1 | -0 | -0 | 2.65533 | 0.00607366 | 21.1905 | 12.7511 | False |
| INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 9 | 1 | 4 | 9500 | 0 | 0 | -12.7747 | 0 | 1 | 0 | 0 | 2.67106 | 0.00573771 | 21.1668 | 12.7747 | False |
| INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 9 | 1 | 4 | 9500 | 0 | -0 | -12.7747 | 0 | 1 | -0 | -0 | 2.67106 | 0.00573771 | 21.1668 | 12.7747 | False |
| WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 11 | 1 | 4 | 10000 | 0 | 0 | -12.7775 | 0 | 1 | 0 | 0 | 2.67294 | 0.00523073 | 18.1573 | 12.7775 | False |
| WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 11 | 1 | 4 | 10000 | 0 | -0 | -12.7775 | 0 | 1 | -0 | -0 | 2.67294 | 0.00523073 | 18.1573 | 12.7775 | False |
| WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | 11 | 1 | 4 | 11550 | 0 | -0 | -12.7792 | 0 | 1 | -0 | -0 | 2.67406 | -0.0043644 | 15.8497 | 12.7792 | False |
| WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 11 | 1 | 4 | 11550 | 0 | 0 | -12.7792 | 0 | 1 | 0 | 0 | 2.67406 | -0.0043644 | 15.8497 | 12.7792 | False |
| SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | 9 | 1 | 4 | 11350 | 0 | -0 | -12.8736 | 0 | 1 | -0 | -0 | 2.73697 | -0.00454747 | 16.5675 | 12.8736 | False |
| SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 9 | 1 | 4 | 11350 | 0 | 0 | -12.8736 | 0 | 1 | 0 | 0 | 2.73697 | -0.00454747 | 16.5675 | 12.8736 | False |
| SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 9 | 1 | 4 | 9200 | 0 | 0 | -12.8738 | 0 | 1 | 0 | 0 | 2.73714 | 0.00531763 | 19.2343 | 12.8738 | False |
| SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 9 | 1 | 4 | 9200 | 0 | -0 | -12.8738 | 0 | 1 | -0 | -0 | 2.73714 | 0.00531763 | 19.2343 | 12.8738 | False |
| ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | 10 | 1 | 4 | 11000 | 0 | -0 | -12.9755 | 0 | 1 | -0 | -0 | 2.80495 | -0.00556073 | 18.7346 | 12.9755 | False |
| ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 10 | 1 | 4 | 11000 | 0 | 0 | -12.9755 | 0 | 1 | 0 | 0 | 2.80495 | -0.00556073 | 18.7346 | 12.9755 | False |
| KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 11 | 1 | 4 | 10450 | 0 | 0 | -13.0157 | 0 | 1 | 0 | 0 | 2.83171 | 0.00520721 | 17.0258 | 13.0157 | False |
| KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 11 | 1 | 4 | 10450 | 0 | -0 | -13.0157 | 0 | 1 | -0 | -0 | 2.83171 | 0.00520721 | 17.0258 | 13.0157 | False |
| ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | 9 | 1 | 4 | 10250 | 0 | -0 | -13.1618 | 0 | 1 | -0 | -0 | 2.92912 | -0.00486449 | 16.1216 | 13.1618 | False |
| ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 9 | 1 | 4 | 10250 | 0 | 0 | -13.1618 | 0 | 1 | 0 | 0 | 2.92912 | -0.00486449 | 16.1216 | 13.1618 | False |
| ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 9 | 1 | 4 | 9000 | 0 | -0 | -13.1694 | 0 | 1 | -0 | -0 | 2.93417 | 0.00549755 | 17.5247 | 13.1694 | False |
| ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 9 | 1 | 4 | 9000 | 0 | 0 | -13.1694 | 0 | 1 | 0 | 0 | 2.93417 | 0.00549755 | 17.5247 | 13.1694 | False |
| KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 11 | 1 | 4 | 11350 | 0 | 0 | -13.19 | 0 | 1 | 0 | 0 | 2.9479 | -0.00474366 | 15.5463 | 13.19 | False |
| KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | 11 | 1 | 4 | 11350 | 0 | -0 | -13.19 | 0 | 1 | -0 | -0 | 2.9479 | -0.00474366 | 15.5463 | 13.19 | False |
| DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | 10 | 1 | 4 | 11050 | 0 | -0 | -13.4656 | 0 | 1 | -0 | -0 | 3.13164 | -0.00476976 | 14.8121 | 13.4656 | False |
| DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 10 | 1 | 4 | 11050 | 0 | 0 | -13.4656 | 0 | 1 | 0 | 0 | 3.13164 | -0.00476976 | 14.8121 | 13.4656 | False |
| NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | 11 | 1 | 4 | 10700 | 0 | -0 | -13.4746 | 0 | 1 | -0 | -0 | 3.13762 | -0.00505766 | 15.0346 | 13.4746 | False |
| NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 11 | 1 | 4 | 10700 | 0 | 0 | -13.4746 | 0 | 1 | 0 | 0 | 3.13762 | -0.00505766 | 15.0346 | 13.4746 | False |
| DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 12 | 1 | 4 | 10500 | 0 | -0 | -13.5797 | 0 | 1 | -0 | -0 | 3.20775 | 0.00490614 | 14.8138 | 13.5797 | False |
| DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 12 | 1 | 4 | 10500 | 0 | 0 | -13.5797 | 0 | 1 | 0 | 0 | 3.20775 | 0.00490614 | 14.8138 | 13.5797 | False |
| HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 12 | 1 | 4 | 10450 | 0 | 0 | -13.6004 | 0 | 1 | 0 | 0 | 3.22152 | 0.00515964 | 15.8768 | 13.6004 | False |
| HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 12 | 1 | 4 | 10450 | 0 | -0 | -13.6004 | 0 | 1 | -0 | -0 | 3.22152 | 0.00515964 | 15.8768 | 13.6004 | False |
| MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 12 | 1 | 4 | 11100 | 0 | 0 | -13.6175 | 0 | 1 | 0 | 0 | 3.2329 | 0.00520542 | 15.3654 | 13.6175 | False |
| MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 12 | 1 | 4 | 11100 | 0 | -0 | -13.6175 | 0 | 1 | -0 | -0 | 3.2329 | 0.00520542 | 15.3654 | 13.6175 | False |
| MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | 11 | 1 | 4 | 11750 | 0 | -0 | -13.6573 | 0 | 1 | -0 | -0 | 3.25947 | -0.00526732 | 15.7724 | 13.6573 | False |
| MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 11 | 1 | 4 | 11750 | 0 | 0 | -13.6573 | 0 | 1 | 0 | 0 | 3.25947 | -0.00526732 | 15.7724 | 13.6573 | False |
| NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 12 | 1 | 4 | 10350 | 0 | 0 | -13.6937 | 0 | 1 | 0 | 0 | 3.2837 | 0.00533552 | 15.4576 | 13.6937 | False |
| NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 12 | 1 | 4 | 10350 | 0 | -0 | -13.6937 | 0 | 1 | -0 | -0 | 3.2837 | 0.00533552 | 15.4576 | 13.6937 | False |
| HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 11 | 1 | 4 | 11100 | 0 | 0 | -13.7011 | 0 | 1 | 0 | 0 | 3.28864 | -0.0052763 | 16.6151 | 13.7011 | False |
| HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | 11 | 1 | 4 | 11100 | 0 | -0 | -13.7011 | 0 | 1 | -0 | -0 | 3.28864 | -0.0052763 | 16.6151 | 13.7011 | False |
| CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | 12 | 1 | 4 | 11250 | 0 | -0 | -13.7065 | 0 | 1 | -0 | -0 | 3.29223 | -0.00439877 | 12.9455 | 13.7065 | False |
| CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 12 | 1 | 4 | 11250 | 0 | 0 | -13.7065 | 0 | 1 | 0 | 0 | 3.29223 | -0.00439877 | 12.9455 | 13.7065 | False |
| CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 12 | 1 | 4 | 10250 | 0 | 0 | -13.7118 | 0 | 1 | 0 | 0 | 3.29582 | 0.00487976 | 14.129 | 13.7118 | False |
| CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 12 | 1 | 4 | 10250 | 0 | -0 | -13.7118 | 0 | 1 | -0 | -0 | 3.29582 | 0.00487976 | 14.129 | 13.7118 | False |
| ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 13 | 1 | 4 | 10100 | 0 | -0 | -13.7523 | 0 | 1 | -0 | -0 | 3.32279 | 0.00696953 | 18.5397 | 13.7523 | False |
| ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 13 | 1 | 4 | 10100 | 0 | 0 | -13.7523 | 0 | 1 | 0 | 0 | 3.32279 | 0.00696953 | 18.5397 | 13.7523 | False |
| BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 12 | 1 | 4 | 10100 | 0 | -0 | -13.81 | 0 | 1 | -0 | -0 | 3.36124 | 0.0060395 | 16.794 | 13.81 | False |
| BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 12 | 1 | 4 | 10100 | 0 | 0 | -13.81 | 0 | 1 | 0 | 0 | 3.36124 | 0.0060395 | 16.794 | 13.81 | False |
| BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | 11 | 1 | 4 | 11650 | 0 | -0 | -13.8583 | 0 | 1 | -0 | -0 | 3.39347 | -0.0058148 | 16.4257 | 13.8583 | False |
| BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 11 | 1 | 4 | 11650 | 0 | 0 | -13.8583 | 0 | 1 | 0 | 0 | 3.39347 | -0.0058148 | 16.4257 | 13.8583 | False |
| ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 14 | 1 | 4 | 10700 | 0 | 0 | -14.172 | 0 | 1 | 0 | 0 | 3.60259 | -0.00773758 | 19.7893 | 14.172 | False |
| ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | 14 | 1 | 4 | 10700 | 0 | -0 | -14.172 | 0 | 1 | -0 | -0 | 3.60259 | -0.00773758 | 19.7893 | 14.172 | False |
| TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 12 | 1 | 4 | 12100 | 0 | 0 | -14.4173 | 0 | 1 | 0 | 0 | 3.76614 | -0.00577304 | 14.8901 | 14.4173 | False |
| TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | 12 | 1 | 4 | 12100 | 0 | -0 | -14.4173 | 0 | 1 | -0 | -0 | 3.76614 | -0.00577304 | 14.8901 | 14.4173 | False |
| TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 12 | 1 | 4 | 10400 | 0 | 0 | -14.4237 | 0 | 1 | 0 | 0 | 3.77038 | 0.00640584 | 16.1476 | 14.4237 | False |
| TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 12 | 1 | 4 | 10400 | 0 | -0 | -14.4237 | 0 | 1 | -0 | -0 | 3.77038 | 0.00640584 | 16.1476 | 14.4237 | False |
| BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 11 | 1 | 4 | 11850 | 0 | 0 | -14.6159 | 0 | 1 | 0 | 0 | 3.89853 | -0.0055102 | 13.1727 | 14.6159 | False |
| BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | 11 | 1 | 4 | 11850 | 0 | -0 | -14.6159 | 0 | 1 | -0 | -0 | 3.89853 | -0.0055102 | 13.1727 | 14.6159 | False |
| BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 11 | 1 | 4 | 10250 | 0 | 0 | -14.617 | 0 | 1 | 0 | 0 | 3.89924 | 0.0061597 | 14.48 | 14.617 | False |
| BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 11 | 1 | 4 | 10250 | 0 | -0 | -14.617 | 0 | 1 | -0 | -0 | 3.89924 | 0.0061597 | 14.48 | 14.617 | False |
| BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | 11 | 1 | 4 | 11250 | 0 | -0 | -14.8194 | 0 | 1 | -0 | -0 | 4.03416 | -0.00584936 | 13.9135 | 14.8194 | False |
| BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 11 | 1 | 4 | 11250 | 0 | 0 | -14.8194 | 0 | 1 | 0 | 0 | 4.03416 | -0.00584936 | 13.9135 | 14.8194 | False |
| JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 11 | 1 | 4 | 9750 | 0 | 0 | -14.8373 | 0 | 1 | 0 | 0 | 4.04613 | 0.00632316 | 14.5441 | 14.8373 | False |
| JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 11 | 1 | 4 | 9750 | 0 | -0 | -14.8373 | 0 | 1 | -0 | -0 | 4.04613 | 0.00632316 | 14.5441 | 14.8373 | False |
| ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | 9 | 1 | 4 | 10500 | 0 | -0 | -14.9028 | 0 | 1 | -0 | -0 | 4.08979 | -0.00741854 | 17.8648 | 14.9028 | False |
| ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 9 | 1 | 4 | 10500 | 0 | 0 | -14.9028 | 0 | 1 | 0 | 0 | 4.08979 | -0.00741854 | 17.8648 | 14.9028 | False |
| ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 9 | 1 | 4 | 9650 | 0 | 0 | -14.9281 | 0 | 1 | 0 | 0 | 4.10665 | 0.00863453 | 19.7191 | 14.9281 | False |
| ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 9 | 1 | 4 | 9650 | 0 | -0 | -14.9281 | 0 | 1 | -0 | -0 | 4.10665 | 0.00863453 | 19.7191 | 14.9281 | False |
| BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | 12 | 1 | 4 | 10550 | 0 | -0 | -15.0027 | 0 | 1 | -0 | -0 | 4.15636 | 0.00629066 | 14.6461 | 15.0027 | False |
| BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | 12 | 1 | 4 | 10550 | 0 | 0 | -15.0027 | 0 | 1 | 0 | 0 | 4.15636 | 0.00629066 | 14.6461 | 15.0027 | False |
| JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | 13 | 1 | 4 | 11650 | 0 | 0 | -15.2579 | 0 | 1 | 0 | 0 | 4.32653 | -0.00519192 | 11.9642 | 15.2579 | False |
| JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | 13 | 1 | 4 | 11650 | 0 | -0 | -15.2579 | 0 | 1 | -0 | -0 | 4.32653 | -0.00519192 | 11.9642 | 15.2579 | False |

## Label Rows

| shard_index | trade_date | symbol | strategy_id | transition_type | side | spread_bucket | spread_change_bucket | recent_return_bucket | signal_rows | mean_gross_bps | median_gross_bps | mean_after_cost_bps | cost_clearing_rate | adverse_direction_rate | worst_gross_bps | best_gross_bps | mean_spread_bps | mean_spread_change_bps | mean_abs_recent_return_bps | mean_cost_bps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -12.0156 | 0 | 1 | 0 | 0 | 2.16497 | -0.00164283 | 7.58555 | 12.0156 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | 0 | -12.0206 | 0 | 1 | 0 | 0 | 2.16832 | 0.0083403 | 38.2097 | 12.0206 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -12.0116 | 0 | 1 | -0 | -0 | 2.16229 | -0.00646272 | 29.8753 | 12.0116 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -12.0143 | 0 | 1 | -0 | -0 | 2.1641 | 0.00155494 | 7.1896 | 12.0143 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -12.0156 | 0 | 1 | -0 | -0 | 2.16497 | -0.00164283 | 7.58555 | 12.0156 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -12.0143 | 0 | 1 | 0 | 0 | 2.1641 | 0.00155494 | 7.1896 | 12.0143 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | -0 | -12.0206 | 0 | 1 | -0 | -0 | 2.16832 | 0.0083403 | 38.2097 | 12.0206 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -12.0361 | 0 | 1 | 0 | 0 | 2.17866 | -0.00106868 | 4.90439 | 12.0361 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -12.0361 | 0 | 1 | -0 | -0 | 2.17866 | -0.00106868 | 4.90439 | 12.0361 |
| 1 | 2026-01-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -12.0116 | 0 | 1 | 0 | 0 | 2.16229 | -0.00646272 | 29.8753 | 12.0116 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -11.005 | 0 | 1 | -0 | -0 | 1.49127 | 0.00133329 | 8.9396 | 11.005 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -10.9936 | 0 | 1 | -0 | -0 | 1.48367 | -0.00128428 | 8.65905 | 10.9936 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -10.9942 | 0 | 1 | 0 | 0 | 1.48404 | -0.00442826 | 29.848 | 10.9942 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -11.005 | 0 | 1 | 0 | 0 | 1.49127 | 0.00133329 | 8.9396 | 11.005 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | 0 | -10.9956 | 0 | 1 | 0 | 0 | 1.485 | 0.005196 | 34.8653 | 10.9956 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -10.9936 | 0 | 1 | 0 | 0 | 1.48367 | -0.00128428 | 8.65905 | 10.9936 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | -0 | -10.9956 | 0 | 1 | -0 | -0 | 1.485 | 0.005196 | 34.8653 | 10.9956 |
| 2 | 2026-01-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -10.9942 | 0 | 1 | -0 | -0 | 1.48404 | -0.00442826 | 29.848 | 10.9942 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -13.0771 | 0 | 1 | -0 | -0 | 2.87267 | 0.00226015 | 7.85645 | 13.0771 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -13.0451 | 0 | 1 | 0 | 0 | 2.8513 | 0.00121897 | 4.27513 | 13.0451 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -13.0747 | 0 | 1 | 0 | 0 | 2.87108 | 0.0110704 | 38.3749 | 13.0747 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | 0 | -13.0676 | 0 | 1 | 0 | 0 | 2.86632 | -0.00215877 | 7.53399 | 13.0676 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | -0 | -13.0676 | 0 | 1 | -0 | -0 | 2.86632 | -0.00215877 | 7.53399 | 13.0676 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | -0 | -13.0821 | 0 | 1 | -0 | -0 | 2.87596 | -0.00117142 | 4.07442 | 13.0821 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -13.0747 | 0 | 1 | -0 | -0 | 2.87108 | 0.0110704 | 38.3749 | 13.0747 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | 0 | -13.0821 | 0 | 1 | 0 | 0 | 2.87596 | -0.00117142 | 4.07442 | 13.0821 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -13.0771 | 0 | 1 | 0 | 0 | 2.87267 | 0.00226015 | 7.85645 | 13.0771 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | 0 | -13.0712 | 0 | 1 | 0 | 0 | 2.86873 | -0.00855007 | 29.8356 | 13.0712 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -13.0451 | 0 | 1 | -0 | -0 | 2.8513 | 0.00121897 | 4.27513 | 13.0451 |
| 3 | 2026-01-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | -0 | -13.0712 | 0 | 1 | -0 | -0 | 2.86873 | -0.00855007 | 29.8356 | 13.0712 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -13.9362 | 0 | 1 | -0 | -0 | 3.44538 | 0.00152485 | 4.42678 | 13.9362 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -13.951 | 0 | 1 | -0 | -0 | 3.45522 | 0.00245158 | 7.09064 | 13.951 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | -0 | -13.9631 | 0 | 1 | -0 | -0 | 3.46331 | 0.00853831 | 24.6254 | 13.9631 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 400 | 0 | -0 | -13.9487 | 0 | 1 | -0 | -0 | 3.45369 | -0.00135037 | 3.9087 | 13.9487 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -13.9599 | 0 | 1 | 0 | 0 | 3.46116 | -0.00706254 | 20.4023 | 13.9599 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -13.9362 | 0 | 1 | 0 | 0 | 3.44538 | 0.00152485 | 4.42678 | 13.9362 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1300 | 0 | 0 | -13.949 | 0 | 1 | 0 | 0 | 3.45392 | -0.00265201 | 7.67873 | 13.949 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | 0 | -13.9631 | 0 | 1 | 0 | 0 | 3.46331 | 0.00853831 | 24.6254 | 13.9631 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1300 | 0 | -0 | -13.949 | 0 | 1 | -0 | -0 | 3.45392 | -0.00265201 | 7.67873 | 13.949 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -13.9599 | 0 | 1 | -0 | -0 | 3.46116 | -0.00706254 | 20.4023 | 13.9599 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -13.951 | 0 | 1 | 0 | 0 | 3.45522 | 0.00245158 | 7.09064 | 13.951 |
| 4 | 2026-01-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 400 | 0 | 0 | -13.9487 | 0 | 1 | 0 | 0 | 3.45369 | -0.00135037 | 3.9087 | 13.9487 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -11.0909 | 0 | 1 | 0 | 0 | 1.54852 | 0.00417706 | 26.8929 | 11.0909 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -11.1044 | 0 | 1 | 0 | 0 | 1.55749 | -0.00138489 | 8.89489 | 11.1044 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -11.102 | 0 | 1 | 0 | 0 | 1.55594 | 0.00122062 | 7.84606 | 11.102 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -11.0917 | 0 | 1 | 0 | 0 | 1.54908 | -0.00340649 | 21.9774 | 11.0917 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -11.102 | 0 | 1 | -0 | -0 | 1.55594 | 0.00122062 | 7.84606 | 11.102 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -11.1044 | 0 | 1 | -0 | -0 | 1.55749 | -0.00138489 | 8.89489 | 11.1044 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -11.0909 | 0 | 1 | -0 | -0 | 1.54852 | 0.00417706 | 26.8929 | 11.0909 |
| 5 | 2026-01-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -11.0917 | 0 | 1 | -0 | -0 | 1.54908 | -0.00340649 | 21.9774 | 11.0917 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | 0 | -11.1766 | 0 | 1 | 0 | 0 | 1.60564 | -0.00140321 | 8.7386 | 11.1766 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | -0 | -11.1766 | 0 | 1 | -0 | -0 | 1.60564 | -0.00140321 | 8.7386 | 11.1766 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | -0 | -11.1729 | 0 | 1 | -0 | -0 | 1.60321 | -0.00474646 | 29.5897 | 11.1729 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -11.1859 | 0 | 1 | -0 | -0 | 1.61185 | 0.00144698 | 8.97436 | 11.1859 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -11.1859 | 0 | 1 | 0 | 0 | 1.61185 | 0.00144698 | 8.97436 | 11.1859 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | 0 | -11.1729 | 0 | 1 | 0 | 0 | 1.60321 | -0.00474646 | 29.5897 | 11.1729 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | -0 | -11.1789 | 0 | 1 | -0 | -0 | 1.60719 | 0.00590936 | 36.6482 | 11.1789 |
| 6 | 2026-01-01 | BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | 0 | -11.1789 | 0 | 1 | 0 | 0 | 1.60719 | 0.00590936 | 36.6482 | 11.1789 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -14.2656 | 0 | 1 | 0 | 0 | 3.66496 | -0.00837901 | 22.8498 | 14.2656 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -14.2656 | 0 | 1 | -0 | -0 | 3.66496 | -0.00837901 | 22.8498 | 14.2656 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -14.2827 | 0 | 1 | 0 | 0 | 3.67636 | 0.001487 | 4.04347 | 14.2827 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -14.2827 | 0 | 1 | -0 | -0 | 3.67636 | 0.001487 | 4.04347 | 14.2827 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -14.2508 | 0 | 1 | 0 | 0 | 3.65515 | -0.00296871 | 8.11914 | 14.2508 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -14.2508 | 0 | 1 | -0 | -0 | 3.65515 | -0.00296871 | 8.11914 | 14.2508 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1350 | 0 | -0 | -14.2667 | 0 | 1 | -0 | -0 | 3.66569 | 0.0127278 | 34.582 | 14.2667 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -14.2614 | 0 | 1 | 0 | 0 | 3.6622 | 0.00290725 | 7.93323 | 14.2614 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -14.2614 | 0 | 1 | -0 | -0 | 3.6622 | 0.00290725 | 7.93323 | 14.2614 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | 0 | -14.2759 | 0 | 1 | 0 | 0 | 3.67186 | -0.00129383 | 3.5218 | 14.2759 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1350 | 0 | 0 | -14.2667 | 0 | 1 | 0 | 0 | 3.66569 | 0.0127278 | 34.582 | 14.2667 |
| 7 | 2026-01-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | -0 | -14.2759 | 0 | 1 | -0 | -0 | 3.67186 | -0.00129383 | 3.5218 | 14.2759 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.9371 | 0 | 1 | 0 | 0 | 2.77932 | -0.00115918 | 4.17072 | 12.9371 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.8718 | 0 | 1 | 0 | 0 | 2.73579 | 0.00112222 | 4.102 | 12.8718 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.9371 | 0 | 1 | -0 | -0 | 2.77932 | -0.00115918 | 4.17072 | 12.9371 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.8718 | 0 | 1 | -0 | -0 | 2.73579 | 0.00112222 | 4.102 | 12.8718 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -12.8932 | 0 | 1 | 0 | 0 | 2.75003 | -0.00194557 | 7.08295 | 12.8932 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2550 | 0 | 0 | -12.8896 | 0 | 1 | 0 | 0 | 2.74768 | -0.00761572 | 27.6979 | 12.8896 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -12.8941 | 0 | 1 | 0 | 0 | 2.75068 | 0.00192152 | 6.99095 | 12.8941 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -12.8932 | 0 | 1 | -0 | -0 | 2.75003 | -0.00194557 | 7.08295 | 12.8932 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -12.8941 | 0 | 1 | -0 | -0 | 2.75068 | 0.00192152 | 6.99095 | 12.8941 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -12.8945 | 0 | 1 | 0 | 0 | 2.75094 | 0.00941041 | 34.0683 | 12.8945 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2550 | 0 | -0 | -12.8896 | 0 | 1 | -0 | -0 | 2.74768 | -0.00761572 | 27.6979 | 12.8896 |
| 8 | 2026-01-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -12.8945 | 0 | 1 | -0 | -0 | 2.75094 | 0.00941041 | 34.0683 | 12.8945 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -12.3442 | 0 | 1 | -0 | -0 | 2.38403 | -0.00168064 | 7.04662 | 12.3442 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | 0 | -12.3585 | 0 | 1 | 0 | 0 | 2.3936 | 0.0018494 | 7.72476 | 12.3585 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | -0 | -12.3585 | 0 | 1 | -0 | -0 | 2.3936 | 0.0018494 | 7.72476 | 12.3585 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -12.3442 | 0 | 1 | 0 | 0 | 2.38403 | -0.00168064 | 7.04662 | 12.3442 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2550 | 0 | 0 | -12.3552 | 0 | 1 | 0 | 0 | 2.39142 | -0.00552028 | 23.0629 | 12.3552 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | -0 | -12.3573 | 0 | 1 | -0 | -0 | 2.3928 | 0.00718417 | 29.9176 | 12.3573 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2550 | 0 | -0 | -12.3552 | 0 | 1 | -0 | -0 | 2.39142 | -0.00552028 | 23.0629 | 12.3552 |
| 9 | 2026-01-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | 0 | -12.3573 | 0 | 1 | 0 | 0 | 2.3928 | 0.00718417 | 29.9176 | 12.3573 |
| 10 | 2026-01-01 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1150 | 0 | -0 | -10.0305 | 0 | 1 | -0 | -0 | 0.841616 | 0.0025569 | 30.2417 | 10.0305 |
| 10 | 2026-01-01 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -10.0318 | 0 | 1 | -0 | -0 | 0.842483 | -0.00171332 | 20.322 | 10.0318 |
| 10 | 2026-01-01 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -10.0318 | 0 | 1 | 0 | 0 | 0.842483 | -0.00171332 | 20.322 | 10.0318 |
| 10 | 2026-01-01 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1150 | 0 | 0 | -10.0305 | 0 | 1 | 0 | 0 | 0.841616 | 0.0025569 | 30.2417 | 10.0305 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -12.3868 | 0 | 1 | -0 | -0 | 2.41243 | 0.00151737 | 6.29231 | 12.3868 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -12.3961 | 0 | 1 | 0 | 0 | 2.41865 | -0.00183271 | 7.57452 | 12.3961 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -12.3961 | 0 | 1 | -0 | -0 | 2.41865 | -0.00183271 | 7.57452 | 12.3961 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -12.3868 | 0 | 1 | 0 | 0 | 2.41243 | 0.00151737 | 6.29231 | 12.3868 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -12.395 | 0 | 1 | -0 | -0 | 2.41792 | 0.0098241 | 40.4117 | 12.395 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | 0 | -12.3828 | 0 | 1 | 0 | 0 | 2.40979 | -0.00848186 | 35.209 | 12.3828 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | -0 | -12.3828 | 0 | 1 | -0 | -0 | 2.40979 | -0.00848186 | 35.209 | 12.3828 |
| 11 | 2026-01-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -12.395 | 0 | 1 | 0 | 0 | 2.41792 | 0.0098241 | 40.4117 | 12.395 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -10.5543 | 0 | 1 | -0 | -0 | 1.19076 | -0.00106438 | 8.93868 | 10.5543 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | 0 | -10.5664 | 0 | 1 | 0 | 0 | 1.19882 | 0.00525959 | 43.5948 | 10.5664 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -10.5543 | 0 | 1 | 0 | 0 | 1.19076 | -0.00106438 | 8.93868 | 10.5543 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -10.5507 | 0 | 1 | -0 | -0 | 1.18835 | 0.00112868 | 9.4978 | 10.5507 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -10.5507 | 0 | 1 | 0 | 0 | 1.18835 | 0.00112868 | 9.4978 | 10.5507 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -10.564 | 0 | 1 | 0 | 0 | 1.19725 | -0.0036951 | 30.872 | 10.564 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -10.564 | 0 | 1 | -0 | -0 | 1.19725 | -0.0036951 | 30.872 | 10.564 |
| 12 | 2026-01-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | -0 | -10.5664 | 0 | 1 | -0 | -0 | 1.19882 | 0.00525959 | 43.5948 | 10.5664 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -11.5351 | 0 | 1 | 0 | 0 | 1.84466 | 0.00138129 | 7.48802 | 11.5351 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | 0 | -11.5391 | 0 | 1 | 0 | 0 | 1.84733 | 0.00566901 | 30.5331 | 11.5391 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | -0 | -11.5391 | 0 | 1 | -0 | -0 | 1.84733 | 0.00566901 | 30.5331 | 11.5391 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -11.5226 | 0 | 1 | -0 | -0 | 1.83634 | -0.00155543 | 8.46887 | 11.5226 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -11.5364 | 0 | 1 | 0 | 0 | 1.84555 | -0.00420236 | 22.7483 | 11.5364 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -11.5351 | 0 | 1 | -0 | -0 | 1.84466 | 0.00138129 | 7.48802 | 11.5351 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -11.5364 | 0 | 1 | -0 | -0 | 1.84555 | -0.00420236 | 22.7483 | 11.5364 |
| 13 | 2026-01-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -11.5226 | 0 | 1 | 0 | 0 | 1.83634 | -0.00155543 | 8.46887 | 11.5226 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -10.8574 | 0 | 1 | -0 | -0 | 1.39287 | 0.00115016 | 8.26001 | 10.8574 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2600 | 0 | -0 | -10.8565 | 0 | 1 | -0 | -0 | 1.39226 | -0.00372529 | 26.7113 | 10.8565 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -10.8605 | 0 | 1 | 0 | 0 | 1.39494 | 0.00495885 | 35.3573 | 10.8605 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2600 | 0 | 0 | -10.8565 | 0 | 1 | 0 | 0 | 1.39226 | -0.00372529 | 26.7113 | 10.8565 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -10.8574 | 0 | 1 | 0 | 0 | 1.39287 | 0.00115016 | 8.26001 | 10.8574 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -10.8725 | 0 | 1 | -0 | -0 | 1.40291 | -0.00122086 | 8.70345 | 10.8725 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -10.8725 | 0 | 1 | 0 | 0 | 1.40291 | -0.00122086 | 8.70345 | 10.8725 |
| 14 | 2026-01-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -10.8605 | 0 | 1 | -0 | -0 | 1.39494 | 0.00495885 | 35.3573 | 10.8605 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -11.4333 | 0 | 1 | 0 | 0 | 1.7768 | 0.0068196 | 38.2374 | 11.4333 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2650 | 0 | -0 | -11.4309 | 0 | 1 | -0 | -0 | 1.77517 | -0.00515018 | 29.0165 | 11.4309 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -11.4226 | 0 | 1 | -0 | -0 | 1.76964 | -0.00125332 | 7.08279 | 11.4226 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -11.4333 | 0 | 1 | -0 | -0 | 1.7768 | 0.0068196 | 38.2374 | 11.4333 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2650 | 0 | 0 | -11.4309 | 0 | 1 | 0 | 0 | 1.77517 | -0.00515018 | 29.0165 | 11.4309 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -11.4346 | 0 | 1 | 0 | 0 | 1.77766 | 0.00147373 | 8.2893 | 11.4346 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -11.4346 | 0 | 1 | -0 | -0 | 1.77766 | 0.00147373 | 8.2893 | 11.4346 |
| 15 | 2026-01-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -11.4226 | 0 | 1 | 0 | 0 | 1.76964 | -0.00125332 | 7.08279 | 11.4226 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -13.4085 | 0 | 1 | 0 | 0 | 3.09356 | 0.00218346 | 7.06189 | 13.4085 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | 0 | -13.3973 | 0 | 1 | 0 | 0 | 3.08614 | -0.00246616 | 7.99261 | 13.3973 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -13.4085 | 0 | 1 | -0 | -0 | 3.09356 | 0.00218346 | 7.06189 | 13.4085 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | -0 | -13.3973 | 0 | 1 | -0 | -0 | 3.08614 | -0.00246616 | 7.99261 | 13.3973 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -13.4068 | 0 | 1 | 0 | 0 | 3.09246 | 0.00812211 | 26.248 | 13.4068 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -13.4068 | 0 | 1 | -0 | -0 | 3.09246 | 0.00812211 | 26.248 | 13.4068 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -13.3977 | 0 | 1 | 0 | 0 | 3.08641 | -0.00721459 | 23.3787 | 13.3977 |
| 16 | 2026-01-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -13.3977 | 0 | 1 | -0 | -0 | 3.08641 | -0.00721459 | 23.3787 | 13.3977 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -11.3999 | 0 | 1 | 0 | 0 | 1.7545 | -0.00142649 | 8.12547 | 11.3999 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -11.3978 | 0 | 1 | -0 | -0 | 1.75312 | -0.00408923 | 23.2998 | 11.3978 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -11.4025 | 0 | 1 | 0 | 0 | 1.75622 | 0.00502597 | 28.5272 | 11.4025 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -11.4025 | 0 | 1 | -0 | -0 | 1.75622 | 0.00502597 | 28.5272 | 11.4025 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -11.3978 | 0 | 1 | 0 | 0 | 1.75312 | -0.00408923 | 23.2998 | 11.3978 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -11.4048 | 0 | 1 | -0 | -0 | 1.7578 | 0.00139175 | 7.91044 | 11.4048 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -11.4048 | 0 | 1 | 0 | 0 | 1.7578 | 0.00139175 | 7.91044 | 11.4048 |
| 17 | 2026-01-01 | ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -11.3999 | 0 | 1 | -0 | -0 | 1.7545 | -0.00142649 | 8.12547 | 11.3999 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -14.1054 | 0 | 1 | 0 | 0 | 3.55818 | 0.00256609 | 7.21218 | 14.1054 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -14.1077 | 0 | 1 | -0 | -0 | 3.55971 | -0.00147284 | 4.14185 | 14.1077 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1200 | 0 | -0 | -14.0946 | 0 | 1 | -0 | -0 | 3.55099 | -0.00276141 | 7.77784 | 14.0946 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1200 | 0 | 0 | -14.0946 | 0 | 1 | 0 | 0 | 3.55099 | -0.00276141 | 7.77784 | 14.0946 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -14.1054 | 0 | 1 | -0 | -0 | 3.55818 | 0.00256609 | 7.21218 | 14.1054 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -14.0856 | 0 | 1 | 0 | 0 | 3.54498 | 0.00145088 | 4.09234 | 14.0856 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -14.1037 | 0 | 1 | 0 | 0 | 3.55707 | -0.0077733 | 21.8567 | 14.1037 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | -0 | -14.1069 | 0 | 1 | -0 | -0 | 3.55919 | 0.0100088 | 28.0196 | 14.1069 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -14.1037 | 0 | 1 | -0 | -0 | 3.55707 | -0.0077733 | 21.8567 | 14.1037 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | 0 | -14.1069 | 0 | 1 | 0 | 0 | 3.55919 | 0.0100088 | 28.0196 | 14.1069 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -14.1077 | 0 | 1 | 0 | 0 | 3.55971 | -0.00147284 | 4.14185 | 14.1077 |
| 18 | 2026-01-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -14.0856 | 0 | 1 | -0 | -0 | 3.54498 | 0.00145088 | 4.09234 | 14.0856 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.7072 | 0 | 1 | 0 | 0 | 2.62605 | 0.00103401 | 3.93752 | 12.7072 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -12.7049 | 0 | 1 | -0 | -0 | 2.6245 | -0.00103361 | 3.9383 | 12.7049 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.7072 | 0 | 1 | -0 | -0 | 2.62605 | 0.00103401 | 3.93752 | 12.7072 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2950 | 0 | -0 | -12.6476 | 0 | 1 | -0 | -0 | 2.58629 | -0.00671668 | 25.964 | 12.6476 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -12.6506 | 0 | 1 | -0 | -0 | 2.58835 | 0.00981462 | 37.667 | 12.6506 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -12.6313 | 0 | 1 | -0 | -0 | 2.57548 | -0.00165836 | 6.44094 | 12.6313 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -12.6419 | 0 | 1 | -0 | -0 | 2.58249 | 0.00185452 | 7.18471 | 12.6419 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -12.6506 | 0 | 1 | 0 | 0 | 2.58835 | 0.00981462 | 37.667 | 12.6506 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -12.6313 | 0 | 1 | 0 | 0 | 2.57548 | -0.00165836 | 6.44094 | 12.6313 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -12.7049 | 0 | 1 | 0 | 0 | 2.6245 | -0.00103361 | 3.9383 | 12.7049 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -12.6419 | 0 | 1 | 0 | 0 | 2.58249 | 0.00185452 | 7.18471 | 12.6419 |
| 19 | 2026-01-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2950 | 0 | 0 | -12.6476 | 0 | 1 | 0 | 0 | 2.58629 | -0.00671668 | 25.964 | 12.6476 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -10.6796 | 0 | 1 | -0 | -0 | 1.27431 | -0.00104012 | 8.16222 | 10.6796 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2650 | 0 | 0 | -10.6438 | 0 | 1 | 0 | 0 | 1.25046 | -0.0037653 | 30.1235 | 10.6438 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -10.6594 | 0 | 1 | -0 | -0 | 1.26087 | 0.0011217 | 8.89903 | 10.6594 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -10.6594 | 0 | 1 | 0 | 0 | 1.26087 | 0.0011217 | 8.89903 | 10.6594 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1500 | 0 | -0 | -10.6483 | 0 | 1 | -0 | -0 | 1.25342 | 0.00541211 | 43.0401 | 10.6483 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -10.6796 | 0 | 1 | 0 | 0 | 1.27431 | -0.00104012 | 8.16222 | 10.6796 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1500 | 0 | 0 | -10.6483 | 0 | 1 | 0 | 0 | 1.25342 | 0.00541211 | 43.0401 | 10.6483 |
| 20 | 2026-01-01 | LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2650 | 0 | -0 | -10.6438 | 0 | 1 | -0 | -0 | 1.25046 | -0.0037653 | 30.1235 | 10.6438 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -10.6377 | 0 | 1 | 0 | 0 | 1.24641 | 0.00120291 | 9.65034 | 10.6377 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -10.65 | 0 | 1 | -0 | -0 | 1.25459 | -0.00117973 | 9.41 | 10.65 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -10.6328 | 0 | 1 | 0 | 0 | 1.24312 | 0.00390755 | 31.262 | 10.6328 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2450 | 0 | -0 | -10.6334 | 0 | 1 | -0 | -0 | 1.24351 | -0.0032006 | 25.7224 | 10.6334 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -10.65 | 0 | 1 | 0 | 0 | 1.25459 | -0.00117973 | 9.41 | 10.65 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -10.6377 | 0 | 1 | -0 | -0 | 1.24641 | 0.00120291 | 9.65034 | 10.6377 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -10.6328 | 0 | 1 | -0 | -0 | 1.24312 | 0.00390755 | 31.262 | 10.6328 |
| 21 | 2026-01-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2450 | 0 | 0 | -10.6334 | 0 | 1 | 0 | 0 | 1.24351 | -0.0032006 | 25.7224 | 10.6334 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | 0 | -13.0427 | 0 | 1 | 0 | 0 | 2.84973 | -0.00232989 | 8.17708 | 13.0427 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -13.0498 | 0 | 1 | 0 | 0 | 2.85443 | 0.00115201 | 4.03881 | 13.0498 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -13.0342 | 0 | 1 | -0 | -0 | 2.84406 | 0.00188044 | 6.6097 | 13.0342 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -13.05 | 0 | 1 | 0 | 0 | 2.85455 | 0.0104012 | 36.2395 | 13.05 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | -0 | -13.0427 | 0 | 1 | -0 | -0 | 2.84973 | -0.00232989 | 8.17708 | 13.0427 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -13.0739 | 0 | 1 | -0 | -0 | 2.87052 | -0.00131734 | 4.59166 | 13.0739 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -13.05 | 0 | 1 | -0 | -0 | 2.85455 | 0.0104012 | 36.2395 | 13.05 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2200 | 0 | 0 | -13.0483 | 0 | 1 | 0 | 0 | 2.85346 | -0.00870285 | 30.4901 | 13.0483 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -13.0739 | 0 | 1 | 0 | 0 | 2.87052 | -0.00131734 | 4.59166 | 13.0739 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2200 | 0 | -0 | -13.0483 | 0 | 1 | -0 | -0 | 2.85346 | -0.00870285 | 30.4901 | 13.0483 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -13.0342 | 0 | 1 | 0 | 0 | 2.84406 | 0.00188044 | 6.6097 | 13.0342 |
| 22 | 2026-01-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -13.0498 | 0 | 1 | -0 | -0 | 2.85443 | 0.00115201 | 4.03881 | 13.0498 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -12.8882 | 0 | 1 | -0 | -0 | 2.74671 | 0.00203471 | 7.4089 | 12.8882 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | -0 | -12.8654 | 0 | 1 | -0 | -0 | 2.73149 | 0.00116644 | 4.26812 | 12.8654 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1500 | 0 | 0 | -12.8865 | 0 | 1 | 0 | 0 | 2.74558 | 0.0103453 | 37.499 | 12.8865 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -12.857 | 0 | 1 | -0 | -0 | 2.7259 | -0.00218946 | 8.03239 | 12.857 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1500 | 0 | -0 | -12.8865 | 0 | 1 | -0 | -0 | 2.74558 | 0.0103453 | 37.499 | 12.8865 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -12.8938 | 0 | 1 | 0 | 0 | 2.75043 | -0.00128703 | 4.67856 | 12.8938 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | -0 | -12.8803 | 0 | 1 | -0 | -0 | 2.74143 | -0.00757887 | 27.6611 | 12.8803 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -12.8882 | 0 | 1 | 0 | 0 | 2.74671 | 0.00203471 | 7.4089 | 12.8882 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -12.857 | 0 | 1 | 0 | 0 | 2.7259 | -0.00218946 | 8.03239 | 12.857 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | 0 | -12.8654 | 0 | 1 | 0 | 0 | 2.73149 | 0.00116644 | 4.26812 | 12.8654 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | 0 | -12.8803 | 0 | 1 | 0 | 0 | 2.74143 | -0.00757887 | 27.6611 | 12.8803 |
| 23 | 2026-01-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -12.8938 | 0 | 1 | -0 | -0 | 2.75043 | -0.00128703 | 4.67856 | 12.8938 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -10.9272 | 0 | 1 | -0 | -0 | 1.43939 | 0.00127462 | 8.85426 | 10.9272 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1250 | 0 | 0 | -10.9196 | 0 | 1 | 0 | 0 | 1.4343 | 0.0052685 | 36.5869 | 10.9196 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -10.9234 | 0 | 1 | 0 | 0 | 1.43683 | -0.00110193 | 7.66901 | 10.9234 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1250 | 0 | -0 | -10.9196 | 0 | 1 | -0 | -0 | 1.4343 | 0.0052685 | 36.5869 | 10.9196 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -10.9234 | 0 | 1 | -0 | -0 | 1.43683 | -0.00110193 | 7.66901 | 10.9234 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -10.9272 | 0 | 1 | 0 | 0 | 1.43939 | 0.00127462 | 8.85426 | 10.9272 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -10.9153 | 0 | 1 | 0 | 0 | 1.43142 | -0.00378044 | 26.3999 | 10.9153 |
| 24 | 2026-01-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -10.9153 | 0 | 1 | -0 | -0 | 1.43142 | -0.00378044 | 26.3999 | 10.9153 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -11.751 | 0 | 1 | -0 | -0 | 1.98856 | -0.00137704 | 6.92144 | 11.751 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -11.7489 | 0 | 1 | -0 | -0 | 1.98718 | 0.00754743 | 37.7714 | 11.7489 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -11.751 | 0 | 1 | 0 | 0 | 1.98856 | -0.00137704 | 6.92144 | 11.751 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -11.7477 | 0 | 1 | 0 | 0 | 1.98636 | 0.00146263 | 7.3676 | 11.7477 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -11.7439 | 0 | 1 | -0 | -0 | 1.98387 | -0.0057362 | 28.9049 | 11.7439 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -11.7477 | 0 | 1 | -0 | -0 | 1.98636 | 0.00146263 | 7.3676 | 11.7477 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -11.7439 | 0 | 1 | 0 | 0 | 1.98387 | -0.0057362 | 28.9049 | 11.7439 |
| 25 | 2026-01-01 | ONGC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -11.7489 | 0 | 1 | 0 | 0 | 1.98718 | 0.00754743 | 37.7714 | 11.7489 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -11.0348 | 0 | 1 | -0 | -0 | 1.51114 | 0.00136893 | 9.05865 | 11.0348 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -11.0353 | 0 | 1 | -0 | -0 | 1.51146 | -0.00132173 | 8.74219 | 11.0353 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -11.0365 | 0 | 1 | -0 | -0 | 1.51226 | 0.00499983 | 32.9776 | 11.0365 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | -0 | -11.0339 | 0 | 1 | -0 | -0 | 1.5105 | -0.00416656 | 27.5791 | 11.0339 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -11.0365 | 0 | 1 | 0 | 0 | 1.51226 | 0.00499983 | 32.9776 | 11.0365 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | 0 | -11.0339 | 0 | 1 | 0 | 0 | 1.5105 | -0.00416656 | 27.5791 | 11.0339 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -11.0348 | 0 | 1 | 0 | 0 | 1.51114 | 0.00136893 | 9.05865 | 11.0348 |
| 26 | 2026-01-01 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -11.0353 | 0 | 1 | 0 | 0 | 1.51146 | -0.00132173 | 8.74219 | 11.0353 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -11.5875 | 0 | 1 | -0 | -0 | 1.87955 | -0.00141087 | 7.51493 | 11.5875 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -11.5875 | 0 | 1 | 0 | 0 | 1.87955 | -0.00141087 | 7.51493 | 11.5875 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | 0 | -11.5966 | 0 | 1 | 0 | 0 | 1.88563 | -0.00594199 | 31.5465 | 11.5966 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -11.5949 | 0 | 1 | -0 | -0 | 1.88453 | 0.00841711 | 44.3708 | 11.5949 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -11.5949 | 0 | 1 | 0 | 0 | 1.88453 | 0.00841711 | 44.3708 | 11.5949 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -11.5907 | 0 | 1 | -0 | -0 | 1.88174 | 0.00126562 | 6.73178 | 11.5907 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -11.5907 | 0 | 1 | 0 | 0 | 1.88174 | 0.00126562 | 6.73178 | 11.5907 |
| 27 | 2026-01-01 | SBIN | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | -0 | -11.5966 | 0 | 1 | -0 | -0 | 1.88563 | -0.00594199 | 31.5465 | 11.5966 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 950 | 0 | -0 | -11.8386 | 0 | 1 | -0 | -0 | 2.04701 | -0.00173794 | 8.49061 | 11.8386 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | 0 | -11.8373 | 0 | 1 | 0 | 0 | 2.04609 | 0.00767615 | 37.3955 | 11.8373 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | -0 | -11.8373 | 0 | 1 | -0 | -0 | 2.04609 | 0.00767615 | 37.3955 | 11.8373 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -11.8249 | 0 | 1 | -0 | -0 | 2.03786 | 0.00133037 | 6.53092 | 11.8249 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -11.832 | 0 | 1 | 0 | 0 | 2.04255 | -0.00538977 | 26.4086 | 11.832 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -11.8249 | 0 | 1 | 0 | 0 | 2.03786 | 0.00133037 | 6.53092 | 11.8249 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 950 | 0 | 0 | -11.8386 | 0 | 1 | 0 | 0 | 2.04701 | -0.00173794 | 8.49061 | 11.8386 |
| 28 | 2026-01-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -11.832 | 0 | 1 | -0 | -0 | 2.04255 | -0.00538977 | 26.4086 | 11.832 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -11.4676 | 0 | 1 | -0 | -0 | 1.79965 | 0.00511092 | 28.2995 | 11.4676 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -11.4687 | 0 | 1 | 0 | 0 | 1.80039 | -0.00421539 | 23.3935 | 11.4687 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -11.4676 | 0 | 1 | 0 | 0 | 1.79965 | 0.00511092 | 28.2995 | 11.4676 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -11.4687 | 0 | 1 | -0 | -0 | 1.80039 | -0.00421539 | 23.3935 | 11.4687 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -11.4603 | 0 | 1 | 0 | 0 | 1.7948 | -0.00145843 | 8.12491 | 11.4603 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -11.4981 | 0 | 1 | -0 | -0 | 1.81996 | 0.00136544 | 7.50207 | 11.4981 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -11.4603 | 0 | 1 | -0 | -0 | 1.7948 | -0.00145843 | 8.12491 | 11.4603 |
| 29 | 2026-01-01 | TCS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -11.4981 | 0 | 1 | 0 | 0 | 1.81996 | 0.00136544 | 7.50207 | 11.4981 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -13.6495 | 0 | 1 | 0 | 0 | 3.25423 | 0.00224085 | 6.88438 | 13.6495 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -13.6539 | 0 | 1 | 0 | 0 | 3.25719 | 0.0110605 | 33.8347 | 13.6539 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -13.6213 | 0 | 1 | -0 | -0 | 3.23548 | -0.0011868 | 3.66816 | 13.6213 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -13.6614 | 0 | 1 | -0 | -0 | 3.26216 | 0.00138523 | 4.24244 | 13.6614 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -13.6213 | 0 | 1 | 0 | 0 | 3.23548 | -0.0011868 | 3.66816 | 13.6213 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -13.6608 | 0 | 1 | -0 | -0 | 3.26179 | -0.00260485 | 7.99177 | 13.6608 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -13.6495 | 0 | 1 | -0 | -0 | 3.25423 | 0.00224085 | 6.88438 | 13.6495 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -13.6608 | 0 | 1 | 0 | 0 | 3.26179 | -0.00260485 | 7.99177 | 13.6608 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2700 | 0 | -0 | -13.6523 | 0 | 1 | -0 | -0 | 3.25614 | -0.00798785 | 24.5189 | 13.6523 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -13.6539 | 0 | 1 | -0 | -0 | 3.25719 | 0.0110605 | 33.8347 | 13.6539 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2700 | 0 | 0 | -13.6523 | 0 | 1 | 0 | 0 | 3.25614 | -0.00798785 | 24.5189 | 13.6523 |
| 30 | 2026-01-01 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -13.6614 | 0 | 1 | 0 | 0 | 3.26216 | 0.00138523 | 4.24244 | 13.6614 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.5849 | 0 | 1 | 0 | 0 | 2.54453 | 0.00107865 | 4.23908 | 12.5849 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.563 | 0 | 1 | 0 | 0 | 2.52994 | -0.00106721 | 4.21834 | 12.563 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.563 | 0 | 1 | -0 | -0 | 2.52994 | -0.00106721 | 4.21834 | 12.563 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.5849 | 0 | 1 | -0 | -0 | 2.54453 | 0.00107865 | 4.23908 | 12.5849 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | -0 | -12.583 | 0 | 1 | -0 | -0 | 2.54328 | -0.00182554 | 7.18024 | 12.583 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -12.5775 | 0 | 1 | -0 | -0 | 2.53962 | 0.00168721 | 6.6451 | 12.5775 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | -0 | -12.5875 | 0 | 1 | -0 | -0 | 2.54623 | -0.00813636 | 31.9784 | 12.5875 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | -0 | -12.5914 | 0 | 1 | -0 | -0 | 2.54888 | 0.0090937 | 35.5014 | 12.5914 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -12.5775 | 0 | 1 | 0 | 0 | 2.53962 | 0.00168721 | 6.6451 | 12.5775 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | 0 | -12.5875 | 0 | 1 | 0 | 0 | 2.54623 | -0.00813636 | 31.9784 | 12.5875 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | 0 | -12.5914 | 0 | 1 | 0 | 0 | 2.54888 | 0.0090937 | 35.5014 | 12.5914 |
| 31 | 2026-01-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | 0 | -12.583 | 0 | 1 | 0 | 0 | 2.54328 | -0.00182554 | 7.18024 | 12.583 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -12.0459 | 0 | 1 | -0 | -0 | 2.18516 | -0.00107488 | 4.91902 | 12.0459 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -12.0758 | 0 | 1 | 0 | 0 | 2.20515 | 0.00164725 | 7.46561 | 12.0758 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -12.0971 | 0 | 1 | 0 | 0 | 2.21932 | -0.00179036 | 8.05914 | 12.0971 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.0518 | 0 | 1 | 0 | 0 | 2.18914 | 0.00107775 | 4.92314 | 12.0518 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -12.0459 | 0 | 1 | 0 | 0 | 2.18516 | -0.00107488 | 4.91902 | 12.0459 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.0518 | 0 | 1 | -0 | -0 | 2.18914 | 0.00107775 | 4.92314 | 12.0518 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -12.0635 | 0 | 1 | -0 | -0 | 2.19695 | -0.00558414 | 25.3882 | 12.0635 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -12.0758 | 0 | 1 | -0 | -0 | 2.20515 | 0.00164725 | 7.46561 | 12.0758 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -12.0971 | 0 | 1 | -0 | -0 | 2.21932 | -0.00179036 | 8.05914 | 12.0971 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -12.068 | 0 | 1 | -0 | -0 | 2.19991 | 0.00768296 | 34.7796 | 12.068 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -12.068 | 0 | 1 | 0 | 0 | 2.19991 | 0.00768296 | 34.7796 | 12.068 |
| 32 | 2026-01-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -12.0635 | 0 | 1 | 0 | 0 | 2.19695 | -0.00558414 | 25.3882 | 12.0635 |
| 33 | 2026-02-02 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -12.0705 | 0 | 1 | 0 | 0 | 2.20162 | 0.00109007 | 4.95119 | 12.0705 |
| 33 | 2026-02-02 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -12.0657 | 0 | 1 | 0 | 0 | 2.19837 | -0.0016269 | 7.3975 | 12.0657 |
| 33 | 2026-02-02 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 700 | 0 | -0 | -12.0765 | 0 | 1 | -0 | -0 | 2.20558 | 0.00156348 | 7.08642 | 12.0765 |
| 33 | 2026-02-02 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -12.0657 | 0 | 1 | -0 | -0 | 2.19837 | -0.0016269 | 7.3975 | 12.0657 |
| 33 | 2026-02-02 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | 0 | -12.0748 | 0 | 1 | 0 | 0 | 2.20448 | 0.00628111 | 28.4658 | 12.0748 |
| 33 | 2026-02-02 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | -0 | -12.0653 | 0 | 1 | -0 | -0 | 2.19809 | -0.00681834 | 31.0393 | 12.0653 |
| 33 | 2026-02-02 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | 0 | -12.0653 | 0 | 1 | 0 | 0 | 2.19809 | -0.00681834 | 31.0393 | 12.0653 |
| 33 | 2026-02-02 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | -0 | -12.0748 | 0 | 1 | -0 | -0 | 2.20448 | 0.00628111 | 28.4658 | 12.0748 |
| 33 | 2026-02-02 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 700 | 0 | 0 | -12.0765 | 0 | 1 | 0 | 0 | 2.20558 | 0.00156348 | 7.08642 | 12.0765 |
| 33 | 2026-02-02 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -12.0705 | 0 | 1 | -0 | -0 | 2.20162 | 0.00109007 | 4.95119 | 12.0705 |
| 34 | 2026-02-02 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -11.0301 | 0 | 1 | -0 | -0 | 1.50796 | 0.00123551 | 8.19286 | 11.0301 |
| 34 | 2026-02-02 | AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -11.0257 | 0 | 1 | -0 | -0 | 1.50503 | -0.00119565 | 7.94312 | 11.0257 |
| 34 | 2026-02-02 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | 0 | -11.0253 | 0 | 1 | 0 | 0 | 1.5048 | -0.00413106 | 27.454 | 11.0253 |
| 34 | 2026-02-02 | AXISBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -11.0301 | 0 | 1 | 0 | 0 | 1.50796 | 0.00123551 | 8.19286 | 11.0301 |
| 34 | 2026-02-02 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -11.0257 | 0 | 1 | 0 | 0 | 1.50503 | -0.00119565 | 7.94312 | 11.0257 |
| 34 | 2026-02-02 | AXISBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | 0 | -11.033 | 0 | 1 | 0 | 0 | 1.50994 | 0.00392243 | 25.976 | 11.033 |
| 34 | 2026-02-02 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | -0 | -11.033 | 0 | 1 | -0 | -0 | 1.50994 | 0.00392243 | 25.976 | 11.033 |
| 34 | 2026-02-02 | AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | -0 | -11.0253 | 0 | 1 | -0 | -0 | 1.5048 | -0.00413106 | 27.454 | 11.0253 |
| 35 | 2026-02-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -13.0976 | 0 | 1 | -0 | -0 | 2.88634 | 0.0012766 | 4.42321 | 13.0976 |
| 35 | 2026-02-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -13.0976 | 0 | 1 | 0 | 0 | 2.88634 | 0.0012766 | 4.42321 | 13.0976 |
| 35 | 2026-02-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2200 | 0 | 0 | -13.1123 | 0 | 1 | 0 | 0 | 2.8961 | -0.00842269 | 29.1117 | 13.1123 |
| 35 | 2026-02-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -13.1187 | 0 | 1 | -0 | -0 | 2.9004 | 0.00199162 | 6.86834 | 13.1187 |
| 35 | 2026-02-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -13.1049 | 0 | 1 | -0 | -0 | 2.8912 | -0.00234778 | 8.11917 | 13.1049 |
| 35 | 2026-02-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -13.1187 | 0 | 1 | 0 | 0 | 2.9004 | 0.00199162 | 6.86834 | 13.1187 |
| 35 | 2026-02-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | -0 | -13.1279 | 0 | 1 | -0 | -0 | 2.9065 | 0.00826877 | 28.4424 | 13.1279 |
| 35 | 2026-02-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -13.1049 | 0 | 1 | 0 | 0 | 2.8912 | -0.00234778 | 8.11917 | 13.1049 |
| 35 | 2026-02-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | 0 | -13.1279 | 0 | 1 | 0 | 0 | 2.9065 | 0.00826877 | 28.4424 | 13.1279 |
| 35 | 2026-02-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2200 | 0 | -0 | -13.1123 | 0 | 1 | -0 | -0 | 2.8961 | -0.00842269 | 29.1117 | 13.1123 |
| 36 | 2026-02-02 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -14.0016 | 0 | 1 | -0 | -0 | 3.48902 | -0.00156568 | 4.48767 | 14.0016 |
| 36 | 2026-02-02 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -14.0035 | 0 | 1 | -0 | -0 | 3.49027 | -0.00237975 | 6.81867 | 14.0035 |
| 36 | 2026-02-02 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | 0 | -13.9996 | 0 | 1 | 0 | 0 | 3.48766 | -0.00708609 | 20.3166 | 13.9996 |
| 36 | 2026-02-02 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1250 | 0 | 0 | -14.0112 | 0 | 1 | 0 | 0 | 3.49541 | 0.00283244 | 8.10298 | 14.0112 |
| 36 | 2026-02-02 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -14.011 | 0 | 1 | -0 | -0 | 3.49522 | 0.00174436 | 4.99068 | 14.011 |
| 36 | 2026-02-02 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -14.0016 | 0 | 1 | 0 | 0 | 3.48902 | -0.00156568 | 4.48767 | 14.0016 |
| 36 | 2026-02-02 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1500 | 0 | -0 | -14.01 | 0 | 1 | -0 | -0 | 3.49457 | 0.00735064 | 21.0272 | 14.01 |
| 36 | 2026-02-02 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | -0 | -13.9996 | 0 | 1 | -0 | -0 | 3.48766 | -0.00708609 | 20.3166 | 13.9996 |
| 36 | 2026-02-02 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -14.0035 | 0 | 1 | 0 | 0 | 3.49027 | -0.00237975 | 6.81867 | 14.0035 |
| 36 | 2026-02-02 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -14.011 | 0 | 1 | 0 | 0 | 3.49522 | 0.00174436 | 4.99068 | 14.011 |
| 36 | 2026-02-02 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1250 | 0 | -0 | -14.0112 | 0 | 1 | -0 | -0 | 3.49541 | 0.00283244 | 8.10298 | 14.0112 |
| 36 | 2026-02-02 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1500 | 0 | 0 | -14.01 | 0 | 1 | 0 | 0 | 3.49457 | 0.00735064 | 21.0272 | 14.01 |
| 37 | 2026-02-02 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -11.1091 | 0 | 1 | 0 | 0 | 1.56067 | 0.00122355 | 7.8384 | 11.1091 |
| 37 | 2026-02-02 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | 0 | -11.1081 | 0 | 1 | 0 | 0 | 1.55996 | -0.00469969 | 30.1477 | 11.1081 |
| 37 | 2026-02-02 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | -0 | -11.1148 | 0 | 1 | -0 | -0 | 1.56444 | 0.00435549 | 27.83 | 11.1148 |
| 37 | 2026-02-02 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -11.0969 | 0 | 1 | 0 | 0 | 1.55255 | -0.00132701 | 8.54677 | 11.0969 |
| 37 | 2026-02-02 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | -0 | -11.1081 | 0 | 1 | -0 | -0 | 1.55996 | -0.00469969 | 30.1477 | 11.1081 |
| 37 | 2026-02-02 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -11.1091 | 0 | 1 | -0 | -0 | 1.56067 | 0.00122355 | 7.8384 | 11.1091 |
| 37 | 2026-02-02 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | 0 | -11.1148 | 0 | 1 | 0 | 0 | 1.56444 | 0.00435549 | 27.83 | 11.1148 |
| 37 | 2026-02-02 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -11.0969 | 0 | 1 | -0 | -0 | 1.55255 | -0.00132701 | 8.54677 | 11.0969 |
| 38 | 2026-02-02 | BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -11.1943 | 0 | 1 | 0 | 0 | 1.61744 | 0.00121796 | 7.53582 | 11.1943 |
| 38 | 2026-02-02 | BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | 0 | -11.2045 | 0 | 1 | 0 | 0 | 1.62427 | 0.0044843 | 27.577 | 11.2045 |
| 38 | 2026-02-02 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -11.1982 | 0 | 1 | 0 | 0 | 1.62005 | -0.00148872 | 9.18906 | 11.1982 |
| 38 | 2026-02-02 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -11.1943 | 0 | 1 | -0 | -0 | 1.61744 | 0.00121796 | 7.53582 | 11.1943 |
| 38 | 2026-02-02 | BPCL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -11.1954 | 0 | 1 | -0 | -0 | 1.6182 | -0.00454715 | 28.0931 | 11.1954 |
| 38 | 2026-02-02 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | -0 | -11.2045 | 0 | 1 | -0 | -0 | 1.62427 | 0.0044843 | 27.577 | 11.2045 |
| 38 | 2026-02-02 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -11.1954 | 0 | 1 | 0 | 0 | 1.6182 | -0.00454715 | 28.0931 | 11.1954 |
| 38 | 2026-02-02 | BPCL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -11.1982 | 0 | 1 | -0 | -0 | 1.62005 | -0.00148872 | 9.18906 | 11.1982 |
| 39 | 2026-02-02 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -14.3525 | 0 | 1 | 0 | 0 | 3.72291 | -0.0110581 | 29.7334 | 14.3525 |
| 39 | 2026-02-02 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | -0 | -14.3517 | 0 | 1 | -0 | -0 | 3.7224 | 0.0013842 | 3.71972 | 14.3517 |
| 39 | 2026-02-02 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -14.3688 | 0 | 1 | 0 | 0 | 3.73379 | 0.0100359 | 26.855 | 14.3688 |
| 39 | 2026-02-02 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -14.3525 | 0 | 1 | -0 | -0 | 3.72291 | -0.0110581 | 29.7334 | 14.3525 |
| 39 | 2026-02-02 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -14.3565 | 0 | 1 | -0 | -0 | 3.72556 | -0.00173579 | 4.65912 | 14.3565 |
| 39 | 2026-02-02 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -14.3688 | 0 | 1 | -0 | -0 | 3.73379 | 0.0100359 | 26.855 | 14.3688 |
| 39 | 2026-02-02 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -14.3565 | 0 | 1 | 0 | 0 | 3.72556 | -0.00173579 | 4.65912 | 14.3565 |
| 39 | 2026-02-02 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | 0 | -14.3517 | 0 | 1 | 0 | 0 | 3.7224 | 0.0013842 | 3.71972 | 14.3517 |
| 39 | 2026-02-02 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -14.3488 | 0 | 1 | -0 | -0 | 3.72048 | -0.00308077 | 8.28269 | 14.3488 |
| 39 | 2026-02-02 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -14.3488 | 0 | 1 | 0 | 0 | 3.72048 | -0.00308077 | 8.28269 | 14.3488 |
| 39 | 2026-02-02 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -14.3646 | 0 | 1 | 0 | 0 | 3.73096 | 0.00269329 | 7.22099 | 14.3646 |
| 39 | 2026-02-02 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -14.3646 | 0 | 1 | -0 | -0 | 3.73096 | 0.00269329 | 7.22099 | 14.3646 |
| 40 | 2026-02-02 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 350 | 0 | 0 | -12.9586 | 0 | 1 | 0 | 0 | 2.79363 | 0.00119815 | 4.2886 | 12.9586 |
| 40 | 2026-02-02 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -12.9669 | 0 | 1 | -0 | -0 | 2.79921 | 0.0022244 | 7.9462 | 12.9669 |
| 40 | 2026-02-02 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -12.9525 | 0 | 1 | -0 | -0 | 2.78959 | -0.00136249 | 4.88418 | 12.9525 |
| 40 | 2026-02-02 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -12.9496 | 0 | 1 | 0 | 0 | 2.78768 | -0.00213813 | 7.67107 | 12.9496 |
| 40 | 2026-02-02 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -12.9632 | 0 | 1 | 0 | 0 | 2.79675 | 0.00693473 | 24.779 | 12.9632 |
| 40 | 2026-02-02 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -12.9525 | 0 | 1 | 0 | 0 | 2.78959 | -0.00136249 | 4.88418 | 12.9525 |
| 40 | 2026-02-02 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -12.9632 | 0 | 1 | -0 | -0 | 2.79675 | 0.00693473 | 24.779 | 12.9632 |
| 40 | 2026-02-02 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 350 | 0 | -0 | -12.9586 | 0 | 1 | -0 | -0 | 2.79363 | 0.00119815 | 4.2886 | 12.9586 |
| 40 | 2026-02-02 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -12.9496 | 0 | 1 | -0 | -0 | 2.78768 | -0.00213813 | 7.67107 | 12.9496 |
| 40 | 2026-02-02 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -12.9544 | 0 | 1 | -0 | -0 | 2.79083 | -0.0069569 | 24.9416 | 12.9544 |
| 40 | 2026-02-02 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -12.9544 | 0 | 1 | 0 | 0 | 2.79083 | -0.0069569 | 24.9416 | 12.9544 |
| 40 | 2026-02-02 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -12.9669 | 0 | 1 | 0 | 0 | 2.79921 | 0.0022244 | 7.9462 | 12.9669 |
| 41 | 2026-02-02 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -12.3875 | 0 | 1 | 0 | 0 | 2.41292 | -0.00170779 | 7.08034 | 12.3875 |
| 41 | 2026-02-02 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 950 | 0 | 0 | -12.4085 | 0 | 1 | 0 | 0 | 2.42695 | 0.00196115 | 8.08187 | 12.4085 |
| 41 | 2026-02-02 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 950 | 0 | -0 | -12.4085 | 0 | 1 | -0 | -0 | 2.42695 | 0.00196115 | 8.08187 | 12.4085 |
| 41 | 2026-02-02 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -12.3977 | 0 | 1 | 0 | 0 | 2.41974 | 0.00117049 | 4.83714 | 12.3977 |
| 41 | 2026-02-02 | DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -12.3875 | 0 | 1 | -0 | -0 | 2.41292 | -0.00170779 | 7.08034 | 12.3875 |
| 41 | 2026-02-02 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -12.3977 | 0 | 1 | -0 | -0 | 2.41974 | 0.00117049 | 4.83714 | 12.3977 |
| 41 | 2026-02-02 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -12.3991 | 0 | 1 | 0 | 0 | 2.42063 | -0.00558451 | 23.0756 | 12.3991 |
| 41 | 2026-02-02 | DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -12.3991 | 0 | 1 | -0 | -0 | 2.42063 | -0.00558451 | 23.0756 | 12.3991 |
| 41 | 2026-02-02 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | 0 | -12.4075 | 0 | 1 | 0 | 0 | 2.42628 | 0.00553369 | 22.801 | 12.4075 |
| 41 | 2026-02-02 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | -0 | -12.4075 | 0 | 1 | -0 | -0 | 2.42628 | 0.00553369 | 22.801 | 12.4075 |
| 42 | 2026-02-02 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -10.0404 | 0 | 1 | 0 | 0 | 0.848207 | -0.00255708 | 30.1677 | 10.0404 |
| 42 | 2026-02-02 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | 0 | -10.0445 | 0 | 1 | 0 | 0 | 0.8509 | 0.00235302 | 27.646 | 10.0445 |
| 42 | 2026-02-02 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -10.0404 | 0 | 1 | -0 | -0 | 0.848207 | -0.00255708 | 30.1677 | 10.0404 |
| 42 | 2026-02-02 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | -0 | -10.0445 | 0 | 1 | -0 | -0 | 0.8509 | 0.00235302 | 27.646 | 10.0445 |
| 43 | 2026-02-02 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -12.4358 | 0 | 1 | -0 | -0 | 2.44515 | 0.00672302 | 27.4814 | 12.4358 |
| 43 | 2026-02-02 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -12.4238 | 0 | 1 | 0 | 0 | 2.43711 | -0.00703798 | 28.8975 | 12.4238 |
| 43 | 2026-02-02 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | -0 | -12.4345 | 0 | 1 | -0 | -0 | 2.44423 | 0.00109398 | 4.47738 | 12.4345 |
| 43 | 2026-02-02 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -12.4238 | 0 | 1 | -0 | -0 | 2.43711 | -0.00703798 | 28.8975 | 12.4238 |
| 43 | 2026-02-02 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -12.4313 | 0 | 1 | 0 | 0 | 2.44215 | 0.00203673 | 8.33832 | 12.4313 |
| 43 | 2026-02-02 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -12.4101 | 0 | 1 | 0 | 0 | 2.42796 | -0.00188349 | 7.75487 | 12.4101 |
| 43 | 2026-02-02 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -12.4358 | 0 | 1 | 0 | 0 | 2.44515 | 0.00672302 | 27.4814 | 12.4358 |
| 43 | 2026-02-02 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -12.4101 | 0 | 1 | -0 | -0 | 2.42796 | -0.00188349 | 7.75487 | 12.4101 |
| 43 | 2026-02-02 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -12.4313 | 0 | 1 | -0 | -0 | 2.44215 | 0.00203673 | 8.33832 | 12.4313 |
| 43 | 2026-02-02 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | 0 | -12.4345 | 0 | 1 | 0 | 0 | 2.44423 | 0.00109398 | 4.47738 | 12.4345 |
| 44 | 2026-02-02 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -10.5867 | 0 | 1 | -0 | -0 | 1.2124 | 0.00105708 | 8.72015 | 10.5867 |
| 44 | 2026-02-02 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -10.5867 | 0 | 1 | 0 | 0 | 1.2124 | 0.00105708 | 8.72015 | 10.5867 |
| 44 | 2026-02-02 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -10.591 | 0 | 1 | -0 | -0 | 1.21528 | 0.00392937 | 32.332 | 10.591 |
| 44 | 2026-02-02 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2300 | 0 | -0 | -10.5836 | 0 | 1 | -0 | -0 | 1.21034 | -0.00405546 | 33.5597 | 10.5836 |
| 44 | 2026-02-02 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2300 | 0 | 0 | -10.5836 | 0 | 1 | 0 | 0 | 1.21034 | -0.00405546 | 33.5597 | 10.5836 |
| 44 | 2026-02-02 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -10.591 | 0 | 1 | 0 | 0 | 1.21528 | 0.00392937 | 32.332 | 10.591 |
| 45 | 2026-02-02 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | -0 | -11.5897 | 0 | 1 | -0 | -0 | 1.88104 | 0.00150796 | 8.0169 | 11.5897 |
| 45 | 2026-02-02 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | -0 | -11.5821 | 0 | 1 | -0 | -0 | 1.87597 | -0.00140234 | 7.47678 | 11.5821 |
| 45 | 2026-02-02 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | -0 | -11.5825 | 0 | 1 | -0 | -0 | 1.87626 | -0.00463233 | 24.7175 | 11.5825 |
| 45 | 2026-02-02 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | 0 | -11.5897 | 0 | 1 | 0 | 0 | 1.88104 | 0.00150796 | 8.0169 | 11.5897 |
| 45 | 2026-02-02 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | 0 | -11.5825 | 0 | 1 | 0 | 0 | 1.87626 | -0.00463233 | 24.7175 | 11.5825 |
| 45 | 2026-02-02 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | -0 | -11.588 | 0 | 1 | -0 | -0 | 1.87995 | 0.00506562 | 26.9326 | 11.588 |
| 45 | 2026-02-02 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | 0 | -11.588 | 0 | 1 | 0 | 0 | 1.87995 | 0.00506562 | 26.9326 | 11.588 |
| 45 | 2026-02-02 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | 0 | -11.5821 | 0 | 1 | 0 | 0 | 1.87597 | -0.00140234 | 7.47678 | 11.5821 |
| 46 | 2026-02-02 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -10.9013 | 0 | 1 | -0 | -0 | 1.42209 | -0.00132638 | 9.32515 | 10.9013 |
| 46 | 2026-02-02 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | -0 | -10.897 | 0 | 1 | -0 | -0 | 1.41924 | -0.00393233 | 27.7083 | 10.897 |
| 46 | 2026-02-02 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -10.9031 | 0 | 1 | 0 | 0 | 1.42329 | 0.00122468 | 8.60394 | 10.9031 |
| 46 | 2026-02-02 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -10.9031 | 0 | 1 | -0 | -0 | 1.42329 | 0.00122468 | 8.60394 | 10.9031 |
| 46 | 2026-02-02 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -10.9013 | 0 | 1 | 0 | 0 | 1.42209 | -0.00132638 | 9.32515 | 10.9013 |
| 46 | 2026-02-02 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | 0 | -10.9027 | 0 | 1 | 0 | 0 | 1.42303 | 0.00329176 | 23.1178 | 10.9027 |
| 46 | 2026-02-02 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | 0 | -10.897 | 0 | 1 | 0 | 0 | 1.41924 | -0.00393233 | 27.7083 | 10.897 |
| 46 | 2026-02-02 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | -0 | -10.9027 | 0 | 1 | -0 | -0 | 1.42303 | 0.00329176 | 23.1178 | 10.9027 |
| 47 | 2026-02-02 | INFY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -11.4649 | 0 | 1 | -0 | -0 | 1.79782 | -0.00156281 | 8.69477 | 11.4649 |
| 47 | 2026-02-02 | INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | 0 | -11.4795 | 0 | 1 | 0 | 0 | 1.80759 | 0.00154548 | 8.55096 | 11.4795 |
| 47 | 2026-02-02 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | -0 | -11.4768 | 0 | 1 | -0 | -0 | 1.8058 | 0.00624814 | 34.5688 | 11.4768 |
| 47 | 2026-02-02 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -11.4649 | 0 | 1 | 0 | 0 | 1.79782 | -0.00156281 | 8.69477 | 11.4649 |
| 47 | 2026-02-02 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | -0 | -11.4795 | 0 | 1 | -0 | -0 | 1.80759 | 0.00154548 | 8.55096 | 11.4795 |
| 47 | 2026-02-02 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | 0 | -11.4682 | 0 | 1 | 0 | 0 | 1.80008 | -0.0055031 | 30.6238 | 11.4682 |
| 47 | 2026-02-02 | INFY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | -0 | -11.4682 | 0 | 1 | -0 | -0 | 1.80008 | -0.0055031 | 30.6238 | 11.4682 |
| 47 | 2026-02-02 | INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | 0 | -11.4768 | 0 | 1 | 0 | 0 | 1.8058 | 0.00624814 | 34.5688 | 11.4768 |
| 48 | 2026-02-02 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | -0 | -13.4197 | 0 | 1 | -0 | -0 | 3.10102 | 0.00954222 | 30.7576 | 13.4197 |
| 48 | 2026-02-02 | ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -13.3977 | 0 | 1 | -0 | -0 | 3.08637 | -0.00243562 | 7.89263 | 13.3977 |
| 48 | 2026-02-02 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -13.3977 | 0 | 1 | 0 | 0 | 3.08637 | -0.00243562 | 7.89263 | 13.3977 |
| 48 | 2026-02-02 | ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1100 | 0 | 0 | -13.416 | 0 | 1 | 0 | 0 | 3.0986 | 0.00248548 | 8.02135 | 13.416 |
| 48 | 2026-02-02 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1100 | 0 | -0 | -13.416 | 0 | 1 | -0 | -0 | 3.0986 | 0.00248548 | 8.02135 | 13.416 |
| 48 | 2026-02-02 | ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | -0 | -13.4062 | 0 | 1 | -0 | -0 | 3.09209 | -0.00793871 | 25.687 | 13.4062 |
| 48 | 2026-02-02 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | 0 | -13.4062 | 0 | 1 | 0 | 0 | 3.09209 | -0.00793871 | 25.687 | 13.4062 |
| 48 | 2026-02-02 | ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | 0 | -13.4197 | 0 | 1 | 0 | 0 | 3.10102 | 0.00954222 | 30.7576 | 13.4197 |
| 49 | 2026-02-02 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -11.4443 | 0 | 1 | -0 | -0 | 1.78409 | 0.00148384 | 8.31789 | 11.4443 |
| 49 | 2026-02-02 | ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -11.4443 | 0 | 1 | 0 | 0 | 1.78409 | 0.00148384 | 8.31789 | 11.4443 |
| 49 | 2026-02-02 | ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -11.4342 | 0 | 1 | -0 | -0 | 1.77739 | -0.00151118 | 8.50066 | 11.4342 |
| 49 | 2026-02-02 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -11.4342 | 0 | 1 | 0 | 0 | 1.77739 | -0.00151118 | 8.50066 | 11.4342 |
| 49 | 2026-02-02 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | -0 | -11.4425 | 0 | 1 | -0 | -0 | 1.7829 | 0.00447621 | 25.1058 | 11.4425 |
| 49 | 2026-02-02 | ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | 0 | -11.4425 | 0 | 1 | 0 | 0 | 1.7829 | 0.00447621 | 25.1058 | 11.4425 |
| 49 | 2026-02-02 | ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -11.4365 | 0 | 1 | -0 | -0 | 1.77889 | -0.0041899 | 23.5789 | 11.4365 |
| 49 | 2026-02-02 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -11.4365 | 0 | 1 | 0 | 0 | 1.77889 | -0.0041899 | 23.5789 | 11.4365 |
| 50 | 2026-02-02 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -14.1282 | 0 | 1 | 0 | 0 | 3.57336 | -0.00241899 | 6.76896 | 14.1282 |
| 50 | 2026-02-02 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -14.1467 | 0 | 1 | -0 | -0 | 3.58574 | -0.0017458 | 4.86874 | 14.1467 |
| 50 | 2026-02-02 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -14.1425 | 0 | 1 | 0 | 0 | 3.58294 | -0.00918879 | 25.6772 | 14.1425 |
| 50 | 2026-02-02 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | -0 | -14.1459 | 0 | 1 | -0 | -0 | 3.58519 | 0.00274672 | 7.66084 | 14.1459 |
| 50 | 2026-02-02 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | 0 | -14.1578 | 0 | 1 | 0 | 0 | 3.59314 | 0.00952009 | 26.494 | 14.1578 |
| 50 | 2026-02-02 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | -0 | -14.1431 | 0 | 1 | -0 | -0 | 3.58335 | 0.00131406 | 3.66721 | 14.1431 |
| 50 | 2026-02-02 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -14.1282 | 0 | 1 | -0 | -0 | 3.57336 | -0.00241899 | 6.76896 | 14.1282 |
| 50 | 2026-02-02 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | 0 | -14.1459 | 0 | 1 | 0 | 0 | 3.58519 | 0.00274672 | 7.66084 | 14.1459 |
| 50 | 2026-02-02 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | 0 | -14.1431 | 0 | 1 | 0 | 0 | 3.58335 | 0.00131406 | 3.66721 | 14.1431 |
| 50 | 2026-02-02 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | -0 | -14.1578 | 0 | 1 | -0 | -0 | 3.59314 | 0.00952009 | 26.494 | 14.1578 |
| 50 | 2026-02-02 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -14.1425 | 0 | 1 | -0 | -0 | 3.58294 | -0.00918879 | 25.6772 | 14.1425 |
| 50 | 2026-02-02 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -14.1467 | 0 | 1 | 0 | 0 | 3.58574 | -0.0017458 | 4.86874 | 14.1467 |
| 51 | 2026-02-02 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -12.6794 | 0 | 1 | 0 | 0 | 2.60753 | -0.00204378 | 7.83344 | 12.6794 |
| 51 | 2026-02-02 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -12.6794 | 0 | 1 | -0 | -0 | 2.60753 | -0.00204378 | 7.83344 | 12.6794 |
| 51 | 2026-02-02 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1050 | 0 | 0 | -12.6907 | 0 | 1 | 0 | 0 | 2.61507 | 0.00196946 | 7.5295 | 12.6907 |
| 51 | 2026-02-02 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1050 | 0 | -0 | -12.6907 | 0 | 1 | -0 | -0 | 2.61507 | 0.00196946 | 7.5295 | 12.6907 |
| 51 | 2026-02-02 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -12.6743 | 0 | 1 | 0 | 0 | 2.60412 | 0.00101685 | 3.90466 | 12.6743 |
| 51 | 2026-02-02 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | 0 | -12.687 | 0 | 1 | 0 | 0 | 2.61258 | -0.00711815 | 27.2497 | 12.687 |
| 51 | 2026-02-02 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -12.6743 | 0 | 1 | -0 | -0 | 2.60412 | 0.00101685 | 3.90466 | 12.6743 |
| 51 | 2026-02-02 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | -0 | -12.687 | 0 | 1 | -0 | -0 | 2.61258 | -0.00711815 | 27.2497 | 12.687 |
| 51 | 2026-02-02 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -12.6981 | 0 | 1 | 0 | 0 | 2.62 | 0.00675595 | 25.7714 | 12.6981 |
| 51 | 2026-02-02 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -12.6981 | 0 | 1 | -0 | -0 | 2.62 | 0.00675595 | 25.7714 | 12.6981 |
| 52 | 2026-02-02 | LT | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -10.6726 | 0 | 1 | -0 | -0 | 1.26964 | 0.0010179 | 8.01732 | 10.6726 |
| 52 | 2026-02-02 | LT | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2300 | 0 | -0 | -10.6763 | 0 | 1 | -0 | -0 | 1.27211 | 0.00354268 | 27.8381 | 10.6763 |
| 52 | 2026-02-02 | LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | -0 | -10.6707 | 0 | 1 | -0 | -0 | 1.26838 | -0.00401137 | 31.6759 | 10.6707 |
| 52 | 2026-02-02 | LT | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -10.6726 | 0 | 1 | 0 | 0 | 1.26964 | 0.0010179 | 8.01732 | 10.6726 |
| 52 | 2026-02-02 | LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | 0 | -10.6493 | 0 | 1 | 0 | 0 | 1.25414 | -0.00110197 | 8.78668 | 10.6493 |
| 52 | 2026-02-02 | LT | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2300 | 0 | 0 | -10.6763 | 0 | 1 | 0 | 0 | 1.27211 | 0.00354268 | 27.8381 | 10.6763 |
| 52 | 2026-02-02 | LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | -0 | -10.6493 | 0 | 1 | -0 | -0 | 1.25414 | -0.00110197 | 8.78668 | 10.6493 |
| 52 | 2026-02-02 | LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | 0 | -10.6707 | 0 | 1 | 0 | 0 | 1.26838 | -0.00401137 | 31.6759 | 10.6707 |
| 53 | 2026-02-02 | M&M | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -10.6509 | 0 | 1 | -0 | -0 | 1.25521 | -0.00109374 | 8.71451 | 10.6509 |
| 53 | 2026-02-02 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -10.6637 | 0 | 1 | -0 | -0 | 1.2637 | 0.00112144 | 8.87568 | 10.6637 |
| 53 | 2026-02-02 | M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -10.6637 | 0 | 1 | 0 | 0 | 1.2637 | 0.00112144 | 8.87568 | 10.6637 |
| 53 | 2026-02-02 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -10.657 | 0 | 1 | 0 | 0 | 1.25926 | -0.0033962 | 26.9642 | 10.657 |
| 53 | 2026-02-02 | M&M | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -10.657 | 0 | 1 | -0 | -0 | 1.25926 | -0.0033962 | 26.9642 | 10.657 |
| 53 | 2026-02-02 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | -0 | -10.6627 | 0 | 1 | -0 | -0 | 1.26305 | 0.00336452 | 26.6096 | 10.6627 |
| 53 | 2026-02-02 | M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | 0 | -10.6627 | 0 | 1 | 0 | 0 | 1.26305 | 0.00336452 | 26.6096 | 10.6627 |
| 53 | 2026-02-02 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -10.6509 | 0 | 1 | 0 | 0 | 1.25521 | -0.00109374 | 8.71451 | 10.6509 |
| 54 | 2026-02-02 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -13.0996 | 0 | 1 | -0 | -0 | 2.88765 | 0.00108287 | 3.75122 | 13.0996 |
| 54 | 2026-02-02 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -13.1015 | 0 | 1 | 0 | 0 | 2.88895 | -0.00220264 | 7.62685 | 13.1015 |
| 54 | 2026-02-02 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | -0 | -13.1227 | 0 | 1 | -0 | -0 | 2.90305 | 0.00738384 | 25.4087 | 13.1227 |
| 54 | 2026-02-02 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | -0 | -13.1087 | 0 | 1 | -0 | -0 | 2.89372 | -0.00712643 | 24.6141 | 13.1087 |
| 54 | 2026-02-02 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -13.0996 | 0 | 1 | 0 | 0 | 2.88765 | 0.00108287 | 3.75122 | 13.0996 |
| 54 | 2026-02-02 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | 0 | -13.1227 | 0 | 1 | 0 | 0 | 2.90305 | 0.00738384 | 25.4087 | 13.1227 |
| 54 | 2026-02-02 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 950 | 0 | -0 | -13.1148 | 0 | 1 | -0 | -0 | 2.89778 | 0.00210925 | 7.27791 | 13.1148 |
| 54 | 2026-02-02 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 950 | 0 | 0 | -13.1148 | 0 | 1 | 0 | 0 | 2.89778 | 0.00210925 | 7.27791 | 13.1148 |
| 54 | 2026-02-02 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | 0 | -13.1087 | 0 | 1 | 0 | 0 | 2.89372 | -0.00712643 | 24.6141 | 13.1087 |
| 54 | 2026-02-02 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -13.1015 | 0 | 1 | -0 | -0 | 2.88895 | -0.00220264 | 7.62685 | 13.1015 |
| 55 | 2026-02-02 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -12.928 | 0 | 1 | -0 | -0 | 2.77323 | -0.00815616 | 29.4539 | 12.928 |
| 55 | 2026-02-02 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | -0 | -12.9353 | 0 | 1 | -0 | -0 | 2.77811 | 0.00189221 | 6.81069 | 12.9353 |
| 55 | 2026-02-02 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -12.9244 | 0 | 1 | -0 | -0 | 2.77086 | -0.00196849 | 7.10478 | 12.9244 |
| 55 | 2026-02-02 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -12.9362 | 0 | 1 | 0 | 0 | 2.77874 | 0.00125407 | 4.51324 | 12.9362 |
| 55 | 2026-02-02 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | -0 | -12.9419 | 0 | 1 | -0 | -0 | 2.78249 | 0.00867097 | 31.1664 | 12.9419 |
| 55 | 2026-02-02 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -12.9486 | 0 | 1 | 0 | 0 | 2.78697 | -0.0012627 | 4.53081 | 12.9486 |
| 55 | 2026-02-02 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | 0 | -12.9419 | 0 | 1 | 0 | 0 | 2.78249 | 0.00867097 | 31.1664 | 12.9419 |
| 55 | 2026-02-02 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -12.928 | 0 | 1 | 0 | 0 | 2.77323 | -0.00815616 | 29.4539 | 12.928 |
| 55 | 2026-02-02 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -12.9362 | 0 | 1 | -0 | -0 | 2.77874 | 0.00125407 | 4.51324 | 12.9362 |
| 55 | 2026-02-02 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | 0 | -12.9353 | 0 | 1 | 0 | 0 | 2.77811 | 0.00189221 | 6.81069 | 12.9353 |
| 55 | 2026-02-02 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -12.9486 | 0 | 1 | -0 | -0 | 2.78697 | -0.0012627 | 4.53081 | 12.9486 |
| 55 | 2026-02-02 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -12.9244 | 0 | 1 | 0 | 0 | 2.77086 | -0.00196849 | 7.10478 | 12.9244 |
| 56 | 2026-02-02 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -10.9378 | 0 | 1 | -0 | -0 | 1.44644 | -0.00127955 | 8.84667 | 10.9378 |
| 56 | 2026-02-02 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | 0 | -10.9398 | 0 | 1 | 0 | 0 | 1.4478 | 0.00423969 | 29.2906 | 10.9398 |
| 56 | 2026-02-02 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -10.9435 | 0 | 1 | -0 | -0 | 1.45028 | 0.00134484 | 9.27302 | 10.9435 |
| 56 | 2026-02-02 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | 0 | -10.9337 | 0 | 1 | 0 | 0 | 1.44369 | -0.00375966 | 26.0743 | 10.9337 |
| 56 | 2026-02-02 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -10.9435 | 0 | 1 | 0 | 0 | 1.45028 | 0.00134484 | 9.27302 | 10.9435 |
| 56 | 2026-02-02 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | -0 | -10.9398 | 0 | 1 | -0 | -0 | 1.4478 | 0.00423969 | 29.2906 | 10.9398 |
| 56 | 2026-02-02 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -10.9378 | 0 | 1 | 0 | 0 | 1.44644 | -0.00127955 | 8.84667 | 10.9378 |
| 56 | 2026-02-02 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | -0 | -10.9337 | 0 | 1 | -0 | -0 | 1.44369 | -0.00375966 | 26.0743 | 10.9337 |
| 57 | 2026-02-02 | ONGC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -11.7806 | 0 | 1 | 0 | 0 | 2.00834 | 0.00149968 | 7.4692 | 11.7806 |
| 57 | 2026-02-02 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -11.7806 | 0 | 1 | -0 | -0 | 2.00834 | 0.00149968 | 7.4692 | 11.7806 |
| 57 | 2026-02-02 | ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -11.7705 | 0 | 1 | -0 | -0 | 2.00157 | -0.00173273 | 8.65546 | 11.7705 |
| 57 | 2026-02-02 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -11.7705 | 0 | 1 | 0 | 0 | 2.00157 | -0.00173273 | 8.65546 | 11.7705 |
| 57 | 2026-02-02 | ONGC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -11.7813 | 0 | 1 | 0 | 0 | 2.00876 | 0.00552313 | 27.4558 | 11.7813 |
| 57 | 2026-02-02 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -11.7813 | 0 | 1 | -0 | -0 | 2.00876 | 0.00552313 | 27.4558 | 11.7813 |
| 57 | 2026-02-02 | ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | -0 | -11.7719 | 0 | 1 | -0 | -0 | 2.00254 | -0.00584657 | 29.1971 | 11.7719 |
| 57 | 2026-02-02 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | 0 | -11.7719 | 0 | 1 | 0 | 0 | 2.00254 | -0.00584657 | 29.1971 | 11.7719 |
| 58 | 2026-02-02 | RELIANCE | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -11.0598 | 0 | 1 | 0 | 0 | 1.52776 | 0.00146903 | 9.61547 | 11.0598 |
| 58 | 2026-02-02 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | -0 | -11.0659 | 0 | 1 | -0 | -0 | 1.53187 | 0.00396615 | 25.8478 | 11.0659 |
| 58 | 2026-02-02 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -11.0441 | 0 | 1 | 0 | 0 | 1.51732 | -0.00115089 | 7.58861 | 11.0441 |
| 58 | 2026-02-02 | RELIANCE | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -11.0441 | 0 | 1 | -0 | -0 | 1.51732 | -0.00115089 | 7.58861 | 11.0441 |
| 58 | 2026-02-02 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2200 | 0 | 0 | -11.0608 | 0 | 1 | 0 | 0 | 1.52846 | -0.00378142 | 24.7288 | 11.0608 |
| 58 | 2026-02-02 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -11.0598 | 0 | 1 | -0 | -0 | 1.52776 | 0.00146903 | 9.61547 | 11.0598 |
| 58 | 2026-02-02 | RELIANCE | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2200 | 0 | -0 | -11.0608 | 0 | 1 | -0 | -0 | 1.52846 | -0.00378142 | 24.7288 | 11.0608 |
| 58 | 2026-02-02 | RELIANCE | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | 0 | -11.0659 | 0 | 1 | 0 | 0 | 1.53187 | 0.00396615 | 25.8478 | 11.0659 |
| 59 | 2026-02-02 | SBIN | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -11.6466 | 0 | 1 | -0 | -0 | 1.91902 | -0.00533514 | 27.8046 | 11.6466 |
| 59 | 2026-02-02 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | -0 | -11.656 | 0 | 1 | -0 | -0 | 1.92522 | 0.00500564 | 25.9865 | 11.656 |
| 59 | 2026-02-02 | SBIN | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -11.6447 | 0 | 1 | -0 | -0 | 1.91771 | -0.00165734 | 8.63977 | 11.6447 |
| 59 | 2026-02-02 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -11.6466 | 0 | 1 | 0 | 0 | 1.91902 | -0.00533514 | 27.8046 | 11.6466 |
| 59 | 2026-02-02 | SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | 0 | -11.656 | 0 | 1 | 0 | 0 | 1.92522 | 0.00500564 | 25.9865 | 11.656 |
| 59 | 2026-02-02 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -11.6447 | 0 | 1 | 0 | 0 | 1.91771 | -0.00165734 | 8.63977 | 11.6447 |
| 59 | 2026-02-02 | SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -11.6476 | 0 | 1 | 0 | 0 | 1.91965 | 0.00147374 | 7.67481 | 11.6476 |
| 59 | 2026-02-02 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -11.6476 | 0 | 1 | -0 | -0 | 1.91965 | 0.00147374 | 7.67481 | 11.6476 |
| 60 | 2026-02-02 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -11.8605 | 0 | 1 | -0 | -0 | 2.0616 | -0.00152163 | 7.38681 | 11.8605 |
| 60 | 2026-02-02 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -11.8736 | 0 | 1 | 0 | 0 | 2.07033 | 0.00157085 | 7.58628 | 11.8736 |
| 60 | 2026-02-02 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | 0 | -11.8707 | 0 | 1 | 0 | 0 | 2.06838 | 0.00529758 | 25.5921 | 11.8707 |
| 60 | 2026-02-02 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | -0 | -11.8707 | 0 | 1 | -0 | -0 | 2.06838 | 0.00529758 | 25.5921 | 11.8707 |
| 60 | 2026-02-02 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -11.8605 | 0 | 1 | 0 | 0 | 2.0616 | -0.00152163 | 7.38681 | 11.8605 |
| 60 | 2026-02-02 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -11.8639 | 0 | 1 | -0 | -0 | 2.06386 | -0.00520145 | 25.2071 | 11.8639 |
| 60 | 2026-02-02 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -11.8639 | 0 | 1 | 0 | 0 | 2.06386 | -0.00520145 | 25.2071 | 11.8639 |
| 60 | 2026-02-02 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -11.8736 | 0 | 1 | -0 | -0 | 2.07033 | 0.00157085 | 7.58628 | 11.8736 |
| 61 | 2026-02-02 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | -0 | -11.5069 | 0 | 1 | -0 | -0 | 1.82583 | 0.00147739 | 8.08966 | 11.5069 |
| 61 | 2026-02-02 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -11.5075 | 0 | 1 | -0 | -0 | 1.82625 | 0.00522264 | 28.5793 | 11.5075 |
| 61 | 2026-02-02 | TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -11.498 | 0 | 1 | -0 | -0 | 1.81995 | -0.00141029 | 7.74488 | 11.498 |
| 61 | 2026-02-02 | TCS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | 0 | -11.5069 | 0 | 1 | 0 | 0 | 1.82583 | 0.00147739 | 8.08966 | 11.5069 |
| 61 | 2026-02-02 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -11.498 | 0 | 1 | 0 | 0 | 1.81995 | -0.00141029 | 7.74488 | 11.498 |
| 61 | 2026-02-02 | TCS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -11.5075 | 0 | 1 | 0 | 0 | 1.82625 | 0.00522264 | 28.5793 | 11.5075 |
| 61 | 2026-02-02 | TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -11.4995 | 0 | 1 | -0 | -0 | 1.82089 | -0.0055276 | 30.3871 | 11.4995 |
| 61 | 2026-02-02 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -11.4995 | 0 | 1 | 0 | 0 | 1.82089 | -0.0055276 | 30.3871 | 11.4995 |
| 62 | 2026-02-02 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -13.7126 | 0 | 1 | -0 | -0 | 3.29634 | -0.00239153 | 7.25619 | 13.7126 |
| 62 | 2026-02-02 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -13.7124 | 0 | 1 | 0 | 0 | 3.29618 | -0.0113824 | 34.5694 | 13.7124 |
| 62 | 2026-02-02 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -13.711 | 0 | 1 | 0 | 0 | 3.29526 | 0.00226843 | 6.88445 | 13.711 |
| 62 | 2026-02-02 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -13.7126 | 0 | 1 | 0 | 0 | 3.29634 | -0.00239153 | 7.25619 | 13.7126 |
| 62 | 2026-02-02 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -13.7021 | 0 | 1 | -0 | -0 | 3.28931 | 0.0014075 | 4.27654 | 13.7021 |
| 62 | 2026-02-02 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -13.7124 | 0 | 1 | -0 | -0 | 3.29618 | -0.0113824 | 34.5694 | 13.7124 |
| 62 | 2026-02-02 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -13.7021 | 0 | 1 | 0 | 0 | 3.28931 | 0.0014075 | 4.27654 | 13.7021 |
| 62 | 2026-02-02 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -13.711 | 0 | 1 | -0 | -0 | 3.29526 | 0.00226843 | 6.88445 | 13.711 |
| 62 | 2026-02-02 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -13.7313 | 0 | 1 | 0 | 0 | 3.30881 | -0.00135776 | 4.10405 | 13.7313 |
| 62 | 2026-02-02 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2300 | 0 | 0 | -13.732 | 0 | 1 | 0 | 0 | 3.30927 | 0.0103801 | 31.3457 | 13.732 |
| 62 | 2026-02-02 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -13.7313 | 0 | 1 | -0 | -0 | 3.30881 | -0.00135776 | 4.10405 | 13.7313 |
| 62 | 2026-02-02 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2300 | 0 | -0 | -13.732 | 0 | 1 | -0 | -0 | 3.30927 | 0.0103801 | 31.3457 | 13.732 |
| 63 | 2026-02-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -12.6419 | 0 | 1 | -0 | -0 | 2.58255 | 0.00195036 | 7.55123 | 12.6419 |
| 63 | 2026-02-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -12.6419 | 0 | 1 | 0 | 0 | 2.58255 | 0.00195036 | 7.55123 | 12.6419 |
| 63 | 2026-02-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -12.6275 | 0 | 1 | 0 | 0 | 2.57294 | -0.00707805 | 27.5438 | 12.6275 |
| 63 | 2026-02-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -12.6198 | 0 | 1 | -0 | -0 | 2.56778 | -0.00109943 | 4.28146 | 12.6198 |
| 63 | 2026-02-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -12.6332 | 0 | 1 | -0 | -0 | 2.57675 | -0.00186902 | 7.24906 | 12.6332 |
| 63 | 2026-02-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -12.6198 | 0 | 1 | 0 | 0 | 2.56778 | -0.00109943 | 4.28146 | 12.6198 |
| 63 | 2026-02-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -12.6275 | 0 | 1 | -0 | -0 | 2.57294 | -0.00707805 | 27.5438 | 12.6275 |
| 63 | 2026-02-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -12.6332 | 0 | 1 | 0 | 0 | 2.57675 | -0.00186902 | 7.24906 | 12.6332 |
| 63 | 2026-02-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | -0 | -12.6394 | 0 | 1 | -0 | -0 | 2.58083 | 0.0073888 | 28.6304 | 12.6394 |
| 63 | 2026-02-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | 0 | -12.6335 | 0 | 1 | 0 | 0 | 2.57694 | 0.0011063 | 4.29306 | 12.6335 |
| 63 | 2026-02-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | -0 | -12.6335 | 0 | 1 | -0 | -0 | 2.57694 | 0.0011063 | 4.29306 | 12.6335 |
| 63 | 2026-02-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | 0 | -12.6394 | 0 | 1 | 0 | 0 | 2.58083 | 0.0073888 | 28.6304 | 12.6394 |
| 64 | 2026-02-02 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -12.1099 | 0 | 1 | 0 | 0 | 2.22785 | -0.0017876 | 8.02539 | 12.1099 |
| 64 | 2026-02-02 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -12.1186 | 0 | 1 | -0 | -0 | 2.23368 | 0.00163159 | 7.30246 | 12.1186 |
| 64 | 2026-02-02 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -12.1186 | 0 | 1 | 0 | 0 | 2.23368 | 0.00163159 | 7.30246 | 12.1186 |
| 64 | 2026-02-02 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -12.1099 | 0 | 1 | -0 | -0 | 2.22785 | -0.0017876 | 8.02539 | 12.1099 |
| 64 | 2026-02-02 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | 0 | -12.1056 | 0 | 1 | 0 | 0 | 2.22499 | -0.00622537 | 27.9829 | 12.1056 |
| 64 | 2026-02-02 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -12.1151 | 0 | 1 | -0 | -0 | 2.23131 | 0.00620898 | 27.8051 | 12.1151 |
| 64 | 2026-02-02 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -12.1151 | 0 | 1 | 0 | 0 | 2.23131 | 0.00620898 | 27.8051 | 12.1151 |
| 64 | 2026-02-02 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | -0 | -12.1056 | 0 | 1 | -0 | -0 | 2.22499 | -0.00622537 | 27.9829 | 12.1056 |
| 65 | 2026-03-02 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.0752 | 0 | 1 | -0 | -0 | 2.20471 | 0.00109312 | 4.95813 | 12.0752 |
| 65 | 2026-03-02 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -12.0775 | 0 | 1 | 0 | 0 | 2.20623 | -0.00185862 | 8.42144 | 12.0775 |
| 65 | 2026-03-02 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | 0 | -12.0606 | 0 | 1 | 0 | 0 | 2.19498 | -0.00588277 | 26.8196 | 12.0606 |
| 65 | 2026-03-02 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.0752 | 0 | 1 | 0 | 0 | 2.20471 | 0.00109312 | 4.95813 | 12.0752 |
| 65 | 2026-03-02 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | 0 | -12.0646 | 0 | 1 | 0 | 0 | 2.19765 | 0.00166907 | 7.59174 | 12.0646 |
| 65 | 2026-03-02 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | 0 | -12.069 | 0 | 1 | 0 | 0 | 2.2006 | 0.00531645 | 24.1467 | 12.069 |
| 65 | 2026-03-02 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | -0 | -12.069 | 0 | 1 | -0 | -0 | 2.2006 | 0.00531645 | 24.1467 | 12.069 |
| 65 | 2026-03-02 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -12.0775 | 0 | 1 | -0 | -0 | 2.20623 | -0.00185862 | 8.42144 | 12.0775 |
| 65 | 2026-03-02 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 850 | 0 | -0 | -12.0646 | 0 | 1 | -0 | -0 | 2.19765 | 0.00166907 | 7.59174 | 12.0646 |
| 65 | 2026-03-02 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | -0 | -12.0606 | 0 | 1 | -0 | -0 | 2.19498 | -0.00588277 | 26.8196 | 12.0606 |
| 66 | 2026-03-02 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -11.0277 | 0 | 1 | 0 | 0 | 1.50639 | -0.00131044 | 8.69871 | 11.0277 |
| 66 | 2026-03-02 | AXISBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -11.0247 | 0 | 1 | 0 | 0 | 1.50441 | 0.00118753 | 7.89268 | 11.0247 |
| 66 | 2026-03-02 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -11.028 | 0 | 1 | 0 | 0 | 1.50656 | -0.00496132 | 32.9592 | 11.028 |
| 66 | 2026-03-02 | AXISBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -11.0357 | 0 | 1 | 0 | 0 | 1.5117 | 0.00449956 | 29.7522 | 11.0357 |
| 66 | 2026-03-02 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -11.0247 | 0 | 1 | -0 | -0 | 1.50441 | 0.00118753 | 7.89268 | 11.0247 |
| 66 | 2026-03-02 | AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -11.028 | 0 | 1 | -0 | -0 | 1.50656 | -0.00496132 | 32.9592 | 11.028 |
| 66 | 2026-03-02 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -11.0357 | 0 | 1 | -0 | -0 | 1.5117 | 0.00449956 | 29.7522 | 11.0357 |
| 66 | 2026-03-02 | AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -11.0277 | 0 | 1 | -0 | -0 | 1.50639 | -0.00131044 | 8.69871 | 11.0277 |
| 67 | 2026-03-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -13.1347 | 0 | 1 | -0 | -0 | 2.91104 | 0.00213062 | 7.31983 | 13.1347 |
| 67 | 2026-03-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 700 | 0 | 0 | -13.136 | 0 | 1 | 0 | 0 | 2.91191 | -0.0022938 | 7.87635 | 13.136 |
| 67 | 2026-03-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -13.1307 | 0 | 1 | -0 | -0 | 2.90839 | -0.00126936 | 4.36448 | 13.1307 |
| 67 | 2026-03-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -13.1307 | 0 | 1 | 0 | 0 | 2.90839 | -0.00126936 | 4.36448 | 13.1307 |
| 67 | 2026-03-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 700 | 0 | -0 | -13.136 | 0 | 1 | -0 | -0 | 2.91191 | -0.0022938 | 7.87635 | 13.136 |
| 67 | 2026-03-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | -0 | -13.1447 | 0 | 1 | -0 | -0 | 2.91775 | 0.00738587 | 25.2976 | 13.1447 |
| 67 | 2026-03-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -13.1422 | 0 | 1 | 0 | 0 | 2.91603 | 0.00122723 | 4.2094 | 13.1422 |
| 67 | 2026-03-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -13.1348 | 0 | 1 | 0 | 0 | 2.91114 | -0.00763309 | 26.2388 | 13.1348 |
| 67 | 2026-03-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -13.1348 | 0 | 1 | -0 | -0 | 2.91114 | -0.00763309 | 26.2388 | 13.1348 |
| 67 | 2026-03-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -13.1422 | 0 | 1 | -0 | -0 | 2.91603 | 0.00122723 | 4.2094 | 13.1422 |
| 67 | 2026-03-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | 0 | -13.1447 | 0 | 1 | 0 | 0 | 2.91775 | 0.00738587 | 25.2976 | 13.1447 |
| 67 | 2026-03-02 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -13.1347 | 0 | 1 | 0 | 0 | 2.91104 | 0.00213062 | 7.31983 | 13.1347 |
| 68 | 2026-03-02 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -14.2405 | 0 | 1 | 0 | 0 | 3.64823 | 0.00232457 | 6.3714 | 14.2405 |
| 68 | 2026-03-02 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -14.2405 | 0 | 1 | -0 | -0 | 3.64823 | 0.00232457 | 6.3714 | 14.2405 |
| 68 | 2026-03-02 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 350 | 0 | 0 | -14.2432 | 0 | 1 | 0 | 0 | 3.65007 | -0.00165306 | 4.52898 | 14.2432 |
| 68 | 2026-03-02 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -14.2281 | 0 | 1 | -0 | -0 | 3.64001 | -0.00837152 | 23.0019 | 14.2281 |
| 68 | 2026-03-02 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 600 | 0 | 0 | -14.2371 | 0 | 1 | 0 | 0 | 3.64598 | 0.00157066 | 4.30745 | 14.2371 |
| 68 | 2026-03-02 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -14.2281 | 0 | 1 | 0 | 0 | 3.64001 | -0.00837152 | 23.0019 | 14.2281 |
| 68 | 2026-03-02 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 350 | 0 | -0 | -14.2432 | 0 | 1 | -0 | -0 | 3.65007 | -0.00165306 | 4.52898 | 14.2432 |
| 68 | 2026-03-02 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | 0 | -14.2363 | 0 | 1 | 0 | 0 | 3.64543 | -0.00252326 | 6.92233 | 14.2363 |
| 68 | 2026-03-02 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 600 | 0 | -0 | -14.2371 | 0 | 1 | -0 | -0 | 3.64598 | 0.00157066 | 4.30745 | 14.2371 |
| 68 | 2026-03-02 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -14.2371 | 0 | 1 | 0 | 0 | 3.64596 | 0.00806348 | 22.0979 | 14.2371 |
| 68 | 2026-03-02 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -14.2371 | 0 | 1 | -0 | -0 | 3.64596 | 0.00806348 | 22.0979 | 14.2371 |
| 68 | 2026-03-02 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | -0 | -14.2363 | 0 | 1 | -0 | -0 | 3.64543 | -0.00252326 | 6.92233 | 14.2363 |
| 69 | 2026-03-02 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -11.1328 | 0 | 1 | 0 | 0 | 1.57645 | -0.00121965 | 7.73733 | 11.1328 |
| 69 | 2026-03-02 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -11.1235 | 0 | 1 | 0 | 0 | 1.57022 | 0.00118269 | 7.53162 | 11.1235 |
| 69 | 2026-03-02 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -11.1254 | 0 | 1 | 0 | 0 | 1.57152 | -0.00431172 | 27.4907 | 11.1254 |
| 69 | 2026-03-02 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -11.1337 | 0 | 1 | 0 | 0 | 1.57705 | 0.00396958 | 25.15 | 11.1337 |
| 69 | 2026-03-02 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -11.1235 | 0 | 1 | -0 | -0 | 1.57022 | 0.00118269 | 7.53162 | 11.1235 |
| 69 | 2026-03-02 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -11.1328 | 0 | 1 | -0 | -0 | 1.57645 | -0.00121965 | 7.73733 | 11.1328 |
| 69 | 2026-03-02 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -11.1337 | 0 | 1 | -0 | -0 | 1.57705 | 0.00396958 | 25.15 | 11.1337 |
| 69 | 2026-03-02 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -11.1254 | 0 | 1 | -0 | -0 | 1.57152 | -0.00431172 | 27.4907 | 11.1254 |
| 70 | 2026-03-02 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | -0 | -11.2184 | 0 | 1 | -0 | -0 | 1.63352 | 0.00143336 | 8.7734 | 11.2184 |
| 70 | 2026-03-02 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | -0 | -11.2233 | 0 | 1 | -0 | -0 | 1.63677 | 0.00419645 | 25.6318 | 11.2233 |
| 70 | 2026-03-02 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | 0 | -11.2168 | 0 | 1 | 0 | 0 | 1.63248 | -0.00423171 | 25.9401 | 11.2168 |
| 70 | 2026-03-02 | BPCL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | -0 | -11.2168 | 0 | 1 | -0 | -0 | 1.63248 | -0.00423171 | 25.9401 | 11.2168 |
| 70 | 2026-03-02 | BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | 0 | -11.2184 | 0 | 1 | 0 | 0 | 1.63352 | 0.00143336 | 8.7734 | 11.2184 |
| 70 | 2026-03-02 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -11.2227 | 0 | 1 | 0 | 0 | 1.63636 | -0.00113137 | 6.91389 | 11.2227 |
| 70 | 2026-03-02 | BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | 0 | -11.2233 | 0 | 1 | 0 | 0 | 1.63677 | 0.00419645 | 25.6318 | 11.2233 |
| 70 | 2026-03-02 | BPCL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -11.2227 | 0 | 1 | -0 | -0 | 1.63636 | -0.00113137 | 6.91389 | 11.2227 |
| 71 | 2026-03-02 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -14.3605 | 0 | 1 | -0 | -0 | 3.72828 | 0.00269234 | 7.21977 | 14.3605 |
| 71 | 2026-03-02 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 1050 | 0 | -0 | -14.3629 | 0 | 1 | -0 | -0 | 3.72984 | 0.00144062 | 3.86193 | 14.3629 |
| 71 | 2026-03-02 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | -0 | -14.365 | 0 | 1 | -0 | -0 | 3.73123 | 0.00883043 | 23.652 | 14.365 |
| 71 | 2026-03-02 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -14.3556 | 0 | 1 | -0 | -0 | 3.72496 | -0.00855381 | 22.9786 | 14.3556 |
| 71 | 2026-03-02 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -14.3605 | 0 | 1 | 0 | 0 | 3.72828 | 0.00269234 | 7.21977 | 14.3605 |
| 71 | 2026-03-02 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -14.3556 | 0 | 1 | 0 | 0 | 3.72496 | -0.00855381 | 22.9786 | 14.3556 |
| 71 | 2026-03-02 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 1050 | 0 | 0 | -14.3629 | 0 | 1 | 0 | 0 | 3.72984 | 0.00144062 | 3.86193 | 14.3629 |
| 71 | 2026-03-02 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | 0 | -14.365 | 0 | 1 | 0 | 0 | 3.73123 | 0.00883043 | 23.652 | 14.365 |
| 71 | 2026-03-02 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -14.362 | 0 | 1 | -0 | -0 | 3.72924 | -0.00234758 | 6.29605 | 14.362 |
| 71 | 2026-03-02 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -14.362 | 0 | 1 | 0 | 0 | 3.72924 | -0.00234758 | 6.29605 | 14.362 |
| 71 | 2026-03-02 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | -0 | -14.3553 | 0 | 1 | -0 | -0 | 3.72477 | -0.00144421 | 3.87938 | 14.3553 |
| 71 | 2026-03-02 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | 0 | -14.3553 | 0 | 1 | 0 | 0 | 3.72477 | -0.00144421 | 3.87938 | 14.3553 |
| 72 | 2026-03-02 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1000 | 0 | -0 | -12.9723 | 0 | 1 | -0 | -0 | 2.80281 | 0.00212137 | 7.56513 | 12.9723 |
| 72 | 2026-03-02 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -12.9727 | 0 | 1 | 0 | 0 | 2.80308 | -0.00117909 | 4.20639 | 12.9727 |
| 72 | 2026-03-02 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | 0 | -12.9632 | 0 | 1 | 0 | 0 | 2.79672 | -0.00553912 | 19.8066 | 12.9632 |
| 72 | 2026-03-02 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -12.9744 | 0 | 1 | -0 | -0 | 2.80416 | -0.0021639 | 7.71716 | 12.9744 |
| 72 | 2026-03-02 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 1000 | 0 | 0 | -12.9723 | 0 | 1 | 0 | 0 | 2.80281 | 0.00212137 | 7.56513 | 12.9723 |
| 72 | 2026-03-02 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | -0 | -12.97 | 0 | 1 | -0 | -0 | 2.80123 | 0.00565355 | 20.1716 | 12.97 |
| 72 | 2026-03-02 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | 0 | -12.97 | 0 | 1 | 0 | 0 | 2.80123 | 0.00565355 | 20.1716 | 12.97 |
| 72 | 2026-03-02 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | -0 | -12.9632 | 0 | 1 | -0 | -0 | 2.79672 | -0.00553912 | 19.8066 | 12.9632 |
| 72 | 2026-03-02 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -12.9727 | 0 | 1 | -0 | -0 | 2.80308 | -0.00117909 | 4.20639 | 12.9727 |
| 72 | 2026-03-02 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | 0 | -12.9594 | 0 | 1 | 0 | 0 | 2.79419 | 0.00126789 | 4.53804 | 12.9594 |
| 72 | 2026-03-02 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | -0 | -12.9594 | 0 | 1 | -0 | -0 | 2.79419 | 0.00126789 | 4.53804 | 12.9594 |
| 72 | 2026-03-02 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -12.9744 | 0 | 1 | 0 | 0 | 2.80416 | -0.0021639 | 7.71716 | 12.9744 |
| 73 | 2026-03-02 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.4148 | 0 | 1 | 0 | 0 | 2.43112 | 0.00118149 | 4.85987 | 12.4148 |
| 73 | 2026-03-02 | DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -12.4459 | 0 | 1 | -0 | -0 | 2.45182 | -0.00108246 | 4.41508 | 12.4459 |
| 73 | 2026-03-02 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.4148 | 0 | 1 | -0 | -0 | 2.43112 | 0.00118149 | 4.85987 | 12.4148 |
| 73 | 2026-03-02 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 1150 | 0 | 0 | -12.422 | 0 | 1 | 0 | 0 | 2.43595 | 0.00200159 | 8.21777 | 12.422 |
| 73 | 2026-03-02 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -12.4459 | 0 | 1 | 0 | 0 | 2.45182 | -0.00108246 | 4.41508 | 12.4459 |
| 73 | 2026-03-02 | DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -12.4294 | 0 | 1 | -0 | -0 | 2.44086 | -0.00175439 | 7.18993 | 12.4294 |
| 73 | 2026-03-02 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -12.417 | 0 | 1 | 0 | 0 | 2.43259 | -0.00626231 | 25.7518 | 12.417 |
| 73 | 2026-03-02 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 1150 | 0 | -0 | -12.422 | 0 | 1 | -0 | -0 | 2.43595 | 0.00200159 | 8.21777 | 12.422 |
| 73 | 2026-03-02 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -12.4307 | 0 | 1 | 0 | 0 | 2.44173 | 0.00609832 | 24.9454 | 12.4307 |
| 73 | 2026-03-02 | DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -12.417 | 0 | 1 | -0 | -0 | 2.43259 | -0.00626231 | 25.7518 | 12.417 |
| 73 | 2026-03-02 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -12.4307 | 0 | 1 | -0 | -0 | 2.44173 | 0.00609832 | 24.9454 | 12.4307 |
| 73 | 2026-03-02 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -12.4294 | 0 | 1 | 0 | 0 | 2.44086 | -0.00175439 | 7.18993 | 12.4294 |
| 74 | 2026-03-02 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1200 | 0 | 0 | -10.0447 | 0 | 1 | 0 | 0 | 0.85104 | 0.00206422 | 24.2283 | 10.0447 |
| 74 | 2026-03-02 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | 0 | -10.0425 | 0 | 1 | 0 | 0 | 0.849554 | -0.00212851 | 25.0621 | 10.0425 |
| 74 | 2026-03-02 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1200 | 0 | -0 | -10.0447 | 0 | 1 | -0 | -0 | 0.85104 | 0.00206422 | 24.2283 | 10.0447 |
| 74 | 2026-03-02 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S01_le_1bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | -0 | -10.0425 | 0 | 1 | -0 | -0 | 0.849554 | -0.00212851 | 25.0621 | 10.0425 |
| 75 | 2026-03-02 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -12.4865 | 0 | 1 | 0 | 0 | 2.47893 | 0.00102376 | 4.12984 | 12.4865 |
| 75 | 2026-03-02 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -12.4742 | 0 | 1 | -0 | -0 | 2.47072 | -0.00101784 | 4.11956 | 12.4742 |
| 75 | 2026-03-02 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -12.4686 | 0 | 1 | 0 | 0 | 2.467 | 0.00664929 | 26.937 | 12.4686 |
| 75 | 2026-03-02 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -12.4818 | 0 | 1 | 0 | 0 | 2.47581 | -0.002112 | 8.53285 | 12.4818 |
| 75 | 2026-03-02 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -12.4574 | 0 | 1 | -0 | -0 | 2.45949 | -0.00800837 | 32.5905 | 12.4574 |
| 75 | 2026-03-02 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -12.4689 | 0 | 1 | -0 | -0 | 2.46718 | 0.00174688 | 7.08017 | 12.4689 |
| 75 | 2026-03-02 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -12.4689 | 0 | 1 | 0 | 0 | 2.46718 | 0.00174688 | 7.08017 | 12.4689 |
| 75 | 2026-03-02 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -12.4574 | 0 | 1 | 0 | 0 | 2.45949 | -0.00800837 | 32.5905 | 12.4574 |
| 75 | 2026-03-02 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -12.4818 | 0 | 1 | -0 | -0 | 2.47581 | -0.002112 | 8.53285 | 12.4818 |
| 75 | 2026-03-02 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -12.4686 | 0 | 1 | -0 | -0 | 2.467 | 0.00664929 | 26.937 | 12.4686 |
| 75 | 2026-03-02 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -12.4742 | 0 | 1 | 0 | 0 | 2.47072 | -0.00101784 | 4.11956 | 12.4742 |
| 75 | 2026-03-02 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -12.4865 | 0 | 1 | -0 | -0 | 2.47893 | 0.00102376 | 4.12984 | 12.4865 |
| 76 | 2026-03-02 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | -0 | -10.5945 | 0 | 1 | -0 | -0 | 1.21756 | 0.00300214 | 24.6424 | 10.5945 |
| 76 | 2026-03-02 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | 0 | -10.5945 | 0 | 1 | 0 | 0 | 1.21756 | 0.00300214 | 24.6424 | 10.5945 |
| 76 | 2026-03-02 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -10.5932 | 0 | 1 | -0 | -0 | 1.21672 | 0.00112376 | 9.23721 | 10.5932 |
| 76 | 2026-03-02 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | -0 | -10.5885 | 0 | 1 | -0 | -0 | 1.21359 | -0.00366536 | 30.2133 | 10.5885 |
| 76 | 2026-03-02 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | 0 | -10.5885 | 0 | 1 | 0 | 0 | 1.21359 | -0.00366536 | 30.2133 | 10.5885 |
| 76 | 2026-03-02 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -10.5932 | 0 | 1 | 0 | 0 | 1.21672 | 0.00112376 | 9.23721 | 10.5932 |
| 76 | 2026-03-02 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -10.5952 | 0 | 1 | -0 | -0 | 1.21803 | -0.00113027 | 9.27931 | 10.5952 |
| 76 | 2026-03-02 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -10.5952 | 0 | 1 | 0 | 0 | 1.21803 | -0.00113027 | 9.27931 | 10.5952 |
| 77 | 2026-03-02 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 900 | 0 | -0 | -11.5841 | 0 | 1 | -0 | -0 | 1.87735 | 0.00158053 | 8.41682 | 11.5841 |
| 77 | 2026-03-02 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -11.5823 | 0 | 1 | 0 | 0 | 1.87613 | -0.00483428 | 25.7694 | 11.5823 |
| 77 | 2026-03-02 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -11.5906 | 0 | 1 | -0 | -0 | 1.88166 | 0.0039369 | 20.9013 | 11.5906 |
| 77 | 2026-03-02 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -11.5823 | 0 | 1 | -0 | -0 | 1.87613 | -0.00483428 | 25.7694 | 11.5823 |
| 77 | 2026-03-02 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -11.5906 | 0 | 1 | 0 | 0 | 1.88166 | 0.0039369 | 20.9013 | 11.5906 |
| 77 | 2026-03-02 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 900 | 0 | 0 | -11.5841 | 0 | 1 | 0 | 0 | 1.87735 | 0.00158053 | 8.41682 | 11.5841 |
| 77 | 2026-03-02 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -11.5901 | 0 | 1 | -0 | -0 | 1.88132 | -0.00129342 | 6.87337 | 11.5901 |
| 77 | 2026-03-02 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -11.5901 | 0 | 1 | 0 | 0 | 1.88132 | -0.00129342 | 6.87337 | 11.5901 |
| 78 | 2026-03-02 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -10.8993 | 0 | 1 | 0 | 0 | 1.42076 | -0.00115008 | 8.09432 | 10.8993 |
| 78 | 2026-03-02 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | 0 | -10.8989 | 0 | 1 | 0 | 0 | 1.42049 | -0.00366889 | 25.8348 | 10.8989 |
| 78 | 2026-03-02 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | -0 | -10.8989 | 0 | 1 | -0 | -0 | 1.42049 | -0.00366889 | 25.8348 | 10.8989 |
| 78 | 2026-03-02 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 700 | 0 | -0 | -10.8979 | 0 | 1 | -0 | -0 | 1.41985 | 0.00122351 | 8.61502 | 10.8979 |
| 78 | 2026-03-02 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -10.9046 | 0 | 1 | 0 | 0 | 1.42432 | 0.00384246 | 26.9625 | 10.9046 |
| 78 | 2026-03-02 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -10.8993 | 0 | 1 | -0 | -0 | 1.42076 | -0.00115008 | 8.09432 | 10.8993 |
| 78 | 2026-03-02 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -10.9046 | 0 | 1 | -0 | -0 | 1.42432 | 0.00384246 | 26.9625 | 10.9046 |
| 78 | 2026-03-02 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 700 | 0 | 0 | -10.8979 | 0 | 1 | 0 | 0 | 1.41985 | 0.00122351 | 8.61502 | 10.8979 |
| 79 | 2026-03-02 | INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -11.5005 | 0 | 1 | 0 | 0 | 1.8216 | 0.00140869 | 7.73447 | 11.5005 |
| 79 | 2026-03-02 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -11.5005 | 0 | 1 | -0 | -0 | 1.8216 | 0.00140869 | 7.73447 | 11.5005 |
| 79 | 2026-03-02 | INFY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | -0 | -11.4873 | 0 | 1 | -0 | -0 | 1.81281 | -0.0059734 | 32.962 | 11.4873 |
| 79 | 2026-03-02 | INFY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -11.4973 | 0 | 1 | -0 | -0 | 1.81949 | -0.00135772 | 7.46381 | 11.4973 |
| 79 | 2026-03-02 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1550 | 0 | 0 | -11.4873 | 0 | 1 | 0 | 0 | 1.81281 | -0.0059734 | 32.962 | 11.4873 |
| 79 | 2026-03-02 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -11.4973 | 0 | 1 | 0 | 0 | 1.81949 | -0.00135772 | 7.46381 | 11.4973 |
| 79 | 2026-03-02 | INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | 0 | -11.4967 | 0 | 1 | 0 | 0 | 1.81903 | 0.00499674 | 27.4499 | 11.4967 |
| 79 | 2026-03-02 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | -0 | -11.4967 | 0 | 1 | -0 | -0 | 1.81903 | 0.00499674 | 27.4499 | 11.4967 |
| 80 | 2026-03-02 | ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -13.458 | 0 | 1 | 0 | 0 | 3.12656 | 0.00210227 | 6.72663 | 13.458 |
| 80 | 2026-03-02 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -13.458 | 0 | 1 | -0 | -0 | 3.12656 | 0.00210227 | 6.72663 | 13.458 |
| 80 | 2026-03-02 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -13.4519 | 0 | 1 | -0 | -0 | 3.12253 | 0.00746897 | 23.9005 | 13.4519 |
| 80 | 2026-03-02 | ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -13.4519 | 0 | 1 | 0 | 0 | 3.12253 | 0.00746897 | 23.9005 | 13.4519 |
| 80 | 2026-03-02 | ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -13.4545 | 0 | 1 | -0 | -0 | 3.12425 | -0.00244268 | 7.81763 | 13.4545 |
| 80 | 2026-03-02 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -13.4545 | 0 | 1 | 0 | 0 | 3.12425 | -0.00244268 | 7.81763 | 13.4545 |
| 80 | 2026-03-02 | ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1350 | 0 | -0 | -13.4342 | 0 | 1 | -0 | -0 | 3.11069 | -0.0096155 | 30.9092 | 13.4342 |
| 80 | 2026-03-02 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1350 | 0 | 0 | -13.4342 | 0 | 1 | 0 | 0 | 3.11069 | -0.0096155 | 30.9092 | 13.4342 |
| 81 | 2026-03-02 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -11.4438 | 0 | 1 | 0 | 0 | 1.78381 | -0.00133725 | 7.49714 | 11.4438 |
| 81 | 2026-03-02 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -11.4405 | 0 | 1 | 0 | 0 | 1.78157 | -0.00386587 | 21.7081 | 11.4405 |
| 81 | 2026-03-02 | ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -11.445 | 0 | 1 | 0 | 0 | 1.78462 | 0.00326791 | 18.3035 | 11.445 |
| 81 | 2026-03-02 | ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -11.4405 | 0 | 1 | -0 | -0 | 1.78157 | -0.00386587 | 21.7081 | 11.4405 |
| 81 | 2026-03-02 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -11.4409 | 0 | 1 | -0 | -0 | 1.78187 | 0.00144194 | 8.09252 | 11.4409 |
| 81 | 2026-03-02 | ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -11.4409 | 0 | 1 | 0 | 0 | 1.78187 | 0.00144194 | 8.09252 | 11.4409 |
| 81 | 2026-03-02 | ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -11.4438 | 0 | 1 | -0 | -0 | 1.78381 | -0.00133725 | 7.49714 | 11.4438 |
| 81 | 2026-03-02 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -11.445 | 0 | 1 | -0 | -0 | 1.78462 | 0.00326791 | 18.3035 | 11.445 |
| 82 | 2026-03-02 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | -0 | -14.3635 | 0 | 1 | -0 | -0 | 3.73023 | 0.00827136 | 22.1647 | 14.3635 |
| 82 | 2026-03-02 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | 0 | -14.3635 | 0 | 1 | 0 | 0 | 3.73023 | 0.00827136 | 22.1647 | 14.3635 |
| 82 | 2026-03-02 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | 0 | -14.3541 | 0 | 1 | 0 | 0 | 3.72401 | -0.00127512 | 3.4248 | 14.3541 |
| 82 | 2026-03-02 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | -0 | -14.3604 | 0 | 1 | -0 | -0 | 3.72819 | -0.0028893 | 7.75082 | 14.3604 |
| 82 | 2026-03-02 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 400 | 0 | -0 | -14.3652 | 0 | 1 | -0 | -0 | 3.73138 | 0.00136787 | 3.66574 | 14.3652 |
| 82 | 2026-03-02 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | 0 | -14.362 | 0 | 1 | 0 | 0 | 3.72927 | 0.0027503 | 7.37098 | 14.362 |
| 82 | 2026-03-02 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1350 | 0 | -0 | -14.3515 | 0 | 1 | -0 | -0 | 3.72225 | -0.00910594 | 24.4794 | 14.3515 |
| 82 | 2026-03-02 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | -0 | -14.3541 | 0 | 1 | -0 | -0 | 3.72401 | -0.00127512 | 3.4248 | 14.3541 |
| 82 | 2026-03-02 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | -0 | -14.362 | 0 | 1 | -0 | -0 | 3.72927 | 0.0027503 | 7.37098 | 14.362 |
| 82 | 2026-03-02 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 800 | 0 | 0 | -14.3604 | 0 | 1 | 0 | 0 | 3.72819 | -0.0028893 | 7.75082 | 14.3604 |
| 82 | 2026-03-02 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 400 | 0 | 0 | -14.3652 | 0 | 1 | 0 | 0 | 3.73138 | 0.00136787 | 3.66574 | 14.3652 |
| 82 | 2026-03-02 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1350 | 0 | 0 | -14.3515 | 0 | 1 | 0 | 0 | 3.72225 | -0.00910594 | 24.4794 | 14.3515 |
| 83 | 2026-03-02 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -12.7094 | 0 | 1 | -0 | -0 | 2.62753 | 0.00103519 | 3.93974 | 12.7094 |
| 83 | 2026-03-02 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -12.7087 | 0 | 1 | 0 | 0 | 2.62709 | -0.00103564 | 3.94218 | 12.7087 |
| 83 | 2026-03-02 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -12.7094 | 0 | 1 | 0 | 0 | 2.62753 | 0.00103519 | 3.93974 | 12.7094 |
| 83 | 2026-03-02 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -12.7087 | 0 | 1 | -0 | -0 | 2.62709 | -0.00103564 | 3.94218 | 12.7087 |
| 83 | 2026-03-02 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | -0 | -12.7091 | 0 | 1 | -0 | -0 | 2.62732 | 0.00570932 | 21.7137 | 12.7091 |
| 83 | 2026-03-02 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -12.6943 | 0 | 1 | -0 | -0 | 2.61742 | 0.00198184 | 7.57803 | 12.6943 |
| 83 | 2026-03-02 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 700 | 0 | 0 | -12.7163 | 0 | 1 | 0 | 0 | 2.63211 | -0.00178279 | 6.77307 | 12.7163 |
| 83 | 2026-03-02 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -12.6943 | 0 | 1 | 0 | 0 | 2.61742 | 0.00198184 | 7.57803 | 12.6943 |
| 83 | 2026-03-02 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 700 | 0 | -0 | -12.7163 | 0 | 1 | -0 | -0 | 2.63211 | -0.00178279 | 6.77307 | 12.7163 |
| 83 | 2026-03-02 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -12.6989 | 0 | 1 | 0 | 0 | 2.62055 | -0.00666355 | 25.4378 | 12.6989 |
| 83 | 2026-03-02 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | 0 | -12.7091 | 0 | 1 | 0 | 0 | 2.62732 | 0.00570932 | 21.7137 | 12.7091 |
| 83 | 2026-03-02 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -12.6989 | 0 | 1 | -0 | -0 | 2.62055 | -0.00666355 | 25.4378 | 12.6989 |
| 84 | 2026-03-02 | LT | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -10.6753 | 0 | 1 | 0 | 0 | 1.27148 | 0.00119542 | 9.4009 | 10.6753 |
| 84 | 2026-03-02 | LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | 0 | -10.6712 | 0 | 1 | 0 | 0 | 1.26872 | -0.0032332 | 25.491 | 10.6712 |
| 84 | 2026-03-02 | LT | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -10.6757 | 0 | 1 | -0 | -0 | 1.27174 | 0.00257439 | 20.2319 | 10.6757 |
| 84 | 2026-03-02 | LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | -0 | -10.6712 | 0 | 1 | -0 | -0 | 1.26872 | -0.0032332 | 25.491 | 10.6712 |
| 84 | 2026-03-02 | LT | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -10.6753 | 0 | 1 | -0 | -0 | 1.27148 | 0.00119542 | 9.4009 | 10.6753 |
| 84 | 2026-03-02 | LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -10.6796 | 0 | 1 | 0 | 0 | 1.2743 | -0.00107281 | 8.41815 | 10.6796 |
| 84 | 2026-03-02 | LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -10.6796 | 0 | 1 | -0 | -0 | 1.2743 | -0.00107281 | 8.41815 | 10.6796 |
| 84 | 2026-03-02 | LT | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -10.6757 | 0 | 1 | 0 | 0 | 1.27174 | 0.00257439 | 20.2319 | 10.6757 |
| 85 | 2026-03-02 | M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -10.6715 | 0 | 1 | 0 | 0 | 1.26893 | 0.00110606 | 8.71636 | 10.6715 |
| 85 | 2026-03-02 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -10.6726 | 0 | 1 | 0 | 0 | 1.26963 | -0.00120452 | 9.48649 | 10.6726 |
| 85 | 2026-03-02 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | 0 | -10.6671 | 0 | 1 | 0 | 0 | 1.26595 | -0.00396776 | 31.355 | 10.6671 |
| 85 | 2026-03-02 | M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -10.6738 | 0 | 1 | 0 | 0 | 1.27045 | 0.00351265 | 27.627 | 10.6738 |
| 85 | 2026-03-02 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -10.6738 | 0 | 1 | -0 | -0 | 1.27045 | 0.00351265 | 27.627 | 10.6738 |
| 85 | 2026-03-02 | M&M | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -10.6726 | 0 | 1 | -0 | -0 | 1.26963 | -0.00120452 | 9.48649 | 10.6726 |
| 85 | 2026-03-02 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -10.6715 | 0 | 1 | -0 | -0 | 1.26893 | 0.00110606 | 8.71636 | 10.6715 |
| 85 | 2026-03-02 | M&M | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1600 | 0 | -0 | -10.6671 | 0 | 1 | -0 | -0 | 1.26595 | -0.00396776 | 31.355 | 10.6671 |
| 86 | 2026-03-02 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 700 | 0 | 0 | -13.1323 | 0 | 1 | 0 | 0 | 2.90946 | -0.0022398 | 7.69685 | 13.1323 |
| 86 | 2026-03-02 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | 0 | -13.1345 | 0 | 1 | 0 | 0 | 2.91094 | 0.00692521 | 23.7898 | 13.1345 |
| 86 | 2026-03-02 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -13.1212 | 0 | 1 | -0 | -0 | 2.90206 | -0.00821299 | 28.3314 | 13.1212 |
| 86 | 2026-03-02 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -13.1212 | 0 | 1 | 0 | 0 | 2.90206 | -0.00821299 | 28.3314 | 13.1212 |
| 86 | 2026-03-02 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -13.1235 | 0 | 1 | -0 | -0 | 2.90361 | 0.00117971 | 4.06314 | 13.1235 |
| 86 | 2026-03-02 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 700 | 0 | -0 | -13.1323 | 0 | 1 | -0 | -0 | 2.90946 | -0.0022398 | 7.69685 | 13.1323 |
| 86 | 2026-03-02 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 950 | 0 | 0 | -13.1272 | 0 | 1 | 0 | 0 | 2.90608 | 0.00228714 | 7.8704 | 13.1272 |
| 86 | 2026-03-02 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1850 | 0 | -0 | -13.1345 | 0 | 1 | -0 | -0 | 2.91094 | 0.00692521 | 23.7898 | 13.1345 |
| 86 | 2026-03-02 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -13.1386 | 0 | 1 | 0 | 0 | 2.91367 | -0.00127398 | 4.37241 | 13.1386 |
| 86 | 2026-03-02 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 950 | 0 | -0 | -13.1272 | 0 | 1 | -0 | -0 | 2.90608 | 0.00228714 | 7.8704 | 13.1272 |
| 86 | 2026-03-02 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -13.1235 | 0 | 1 | 0 | 0 | 2.90361 | 0.00117971 | 4.06314 | 13.1235 |
| 86 | 2026-03-02 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -13.1386 | 0 | 1 | -0 | -0 | 2.91367 | -0.00127398 | 4.37241 | 13.1386 |
| 87 | 2026-03-02 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | -0 | -12.9504 | 0 | 1 | -0 | -0 | 2.7882 | 0.0056455 | 20.2337 | 12.9504 |
| 87 | 2026-03-02 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -12.9354 | 0 | 1 | -0 | -0 | 2.7782 | 0.00135011 | 4.85948 | 12.9354 |
| 87 | 2026-03-02 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -12.9427 | 0 | 1 | -0 | -0 | 2.78306 | -0.00652606 | 23.4584 | 12.9427 |
| 87 | 2026-03-02 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -12.9474 | 0 | 1 | 0 | 0 | 2.78621 | 0.00210209 | 7.54678 | 12.9474 |
| 87 | 2026-03-02 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -12.9427 | 0 | 1 | 0 | 0 | 2.78306 | -0.00652606 | 23.4584 | 12.9427 |
| 87 | 2026-03-02 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -12.949 | 0 | 1 | -0 | -0 | 2.78727 | -0.00136021 | 4.88009 | 12.949 |
| 87 | 2026-03-02 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -12.949 | 0 | 1 | 0 | 0 | 2.78727 | -0.00136021 | 4.88009 | 12.949 |
| 87 | 2026-03-02 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -12.9474 | 0 | 1 | -0 | -0 | 2.78621 | 0.00210209 | 7.54678 | 12.9474 |
| 87 | 2026-03-02 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -12.9354 | 0 | 1 | 0 | 0 | 2.7782 | 0.00135011 | 4.85948 | 12.9354 |
| 87 | 2026-03-02 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -12.9468 | 0 | 1 | -0 | -0 | 2.78579 | -0.00187742 | 6.73808 | 12.9468 |
| 87 | 2026-03-02 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | 0 | -12.9504 | 0 | 1 | 0 | 0 | 2.7882 | 0.0056455 | 20.2337 | 12.9504 |
| 87 | 2026-03-02 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -12.9468 | 0 | 1 | 0 | 0 | 2.78579 | -0.00187742 | 6.73808 | 12.9468 |
| 88 | 2026-03-02 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | 0 | -10.9534 | 0 | 1 | 0 | 0 | 1.45682 | 0.00281147 | 19.294 | 10.9534 |
| 88 | 2026-03-02 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1450 | 0 | -0 | -10.9534 | 0 | 1 | -0 | -0 | 1.45682 | 0.00281147 | 19.294 | 10.9534 |
| 88 | 2026-03-02 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -10.9557 | 0 | 1 | -0 | -0 | 1.45841 | -0.00123069 | 8.43861 | 10.9557 |
| 88 | 2026-03-02 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | 0 | -10.9472 | 0 | 1 | 0 | 0 | 1.45274 | -0.00321459 | 22.13 | 10.9472 |
| 88 | 2026-03-02 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -10.9557 | 0 | 1 | 0 | 0 | 1.45841 | -0.00123069 | 8.43861 | 10.9557 |
| 88 | 2026-03-02 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | -0 | -10.9498 | 0 | 1 | -0 | -0 | 1.45443 | 0.0012537 | 8.62092 | 10.9498 |
| 88 | 2026-03-02 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | -0 | -10.9472 | 0 | 1 | -0 | -0 | 1.45274 | -0.00321459 | 22.13 | 10.9472 |
| 88 | 2026-03-02 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | 0 | -10.9498 | 0 | 1 | 0 | 0 | 1.45443 | 0.0012537 | 8.62092 | 10.9498 |
| 89 | 2026-03-02 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -11.8213 | 0 | 1 | 0 | 0 | 2.03548 | -0.00132758 | 6.52008 | 11.8213 |
| 89 | 2026-03-02 | ONGC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | 0 | -11.8201 | 0 | 1 | 0 | 0 | 2.03467 | 0.0015278 | 7.50886 | 11.8201 |
| 89 | 2026-03-02 | ONGC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -11.817 | 0 | 1 | 0 | 0 | 2.0326 | 0.00527898 | 25.942 | 11.817 |
| 89 | 2026-03-02 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | 0 | -11.8119 | 0 | 1 | 0 | 0 | 2.02917 | -0.00551426 | 27.2019 | 11.8119 |
| 89 | 2026-03-02 | ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -11.8213 | 0 | 1 | -0 | -0 | 2.03548 | -0.00132758 | 6.52008 | 11.8213 |
| 89 | 2026-03-02 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | -0 | -11.8201 | 0 | 1 | -0 | -0 | 2.03467 | 0.0015278 | 7.50886 | 11.8201 |
| 89 | 2026-03-02 | ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | -0 | -11.8119 | 0 | 1 | -0 | -0 | 2.02917 | -0.00551426 | 27.2019 | 11.8119 |
| 89 | 2026-03-02 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -11.817 | 0 | 1 | -0 | -0 | 2.0326 | 0.00527898 | 25.942 | 11.817 |
| 90 | 2026-03-02 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1500 | 0 | 0 | -11.0709 | 0 | 1 | 0 | 0 | 1.5352 | -0.00439343 | 28.6491 | 11.0709 |
| 90 | 2026-03-02 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -11.0839 | 0 | 1 | 0 | 0 | 1.54388 | -0.00117986 | 7.64078 | 11.0839 |
| 90 | 2026-03-02 | RELIANCE | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -11.0839 | 0 | 1 | -0 | -0 | 1.54388 | -0.00117986 | 7.64078 | 11.0839 |
| 90 | 2026-03-02 | RELIANCE | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | 0 | -11.0722 | 0 | 1 | 0 | 0 | 1.53608 | 0.00133489 | 8.69344 | 11.0722 |
| 90 | 2026-03-02 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | -0 | -11.0722 | 0 | 1 | -0 | -0 | 1.53608 | 0.00133489 | 8.69344 | 11.0722 |
| 90 | 2026-03-02 | RELIANCE | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1500 | 0 | -0 | -11.0709 | 0 | 1 | -0 | -0 | 1.5352 | -0.00439343 | 28.6491 | 11.0709 |
| 90 | 2026-03-02 | RELIANCE | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | 0 | -11.0795 | 0 | 1 | 0 | 0 | 1.54091 | 0.00398882 | 25.8944 | 11.0795 |
| 90 | 2026-03-02 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1650 | 0 | -0 | -11.0795 | 0 | 1 | -0 | -0 | 1.54091 | 0.00398882 | 25.8944 | 11.0795 |
| 91 | 2026-03-02 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -11.6603 | 0 | 1 | 0 | 0 | 1.92811 | -0.00142241 | 7.37225 | 11.6603 |
| 91 | 2026-03-02 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | -0 | -11.6604 | 0 | 1 | -0 | -0 | 1.92822 | 0.00523153 | 27.1225 | 11.6604 |
| 91 | 2026-03-02 | SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -11.6581 | 0 | 1 | 0 | 0 | 1.92664 | 0.00143786 | 7.4614 | 11.6581 |
| 91 | 2026-03-02 | SBIN | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -11.6603 | 0 | 1 | -0 | -0 | 1.92811 | -0.00142241 | 7.37225 | 11.6603 |
| 91 | 2026-03-02 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | 0 | -11.6526 | 0 | 1 | 0 | 0 | 1.923 | -0.00561782 | 29.2459 | 11.6526 |
| 91 | 2026-03-02 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -11.6581 | 0 | 1 | -0 | -0 | 1.92664 | 0.00143786 | 7.4614 | 11.6581 |
| 91 | 2026-03-02 | SBIN | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | -0 | -11.6526 | 0 | 1 | -0 | -0 | 1.923 | -0.00561782 | 29.2459 | 11.6526 |
| 91 | 2026-03-02 | SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | 0 | -11.6604 | 0 | 1 | 0 | 0 | 1.92822 | 0.00523153 | 27.1225 | 11.6604 |
| 92 | 2026-03-02 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | -0 | -11.8848 | 0 | 1 | -0 | -0 | 2.07777 | 0.00588771 | 28.3176 | 11.8848 |
| 92 | 2026-03-02 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -11.885 | 0 | 1 | 0 | 0 | 2.07794 | -0.00142761 | 6.87198 | 11.885 |
| 92 | 2026-03-02 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | 0 | -11.8779 | 0 | 1 | 0 | 0 | 2.07319 | 0.00173244 | 8.35554 | 11.8779 |
| 92 | 2026-03-02 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -11.885 | 0 | 1 | -0 | -0 | 2.07794 | -0.00142761 | 6.87198 | 11.885 |
| 92 | 2026-03-02 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -11.8768 | 0 | 1 | -0 | -0 | 2.07243 | -0.00500114 | 24.1424 | 11.8768 |
| 92 | 2026-03-02 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1400 | 0 | 0 | -11.8848 | 0 | 1 | 0 | 0 | 2.07777 | 0.00588771 | 28.3176 | 11.8848 |
| 92 | 2026-03-02 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -11.8768 | 0 | 1 | 0 | 0 | 2.07243 | -0.00500114 | 24.1424 | 11.8768 |
| 92 | 2026-03-02 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 750 | 0 | -0 | -11.8779 | 0 | 1 | -0 | -0 | 2.07319 | 0.00173244 | 8.35554 | 11.8779 |
| 93 | 2026-03-02 | TCS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -11.5451 | 0 | 1 | 0 | 0 | 1.85131 | 0.00162637 | 8.78545 | 11.5451 |
| 93 | 2026-03-02 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -11.5451 | 0 | 1 | -0 | -0 | 1.85131 | 0.00162637 | 8.78545 | 11.5451 |
| 93 | 2026-03-02 | TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -11.5366 | 0 | 1 | -0 | -0 | 1.84566 | -0.00134565 | 7.29325 | 11.5366 |
| 93 | 2026-03-02 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -11.5366 | 0 | 1 | 0 | 0 | 1.84566 | -0.00134565 | 7.29325 | 11.5366 |
| 93 | 2026-03-02 | TCS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -11.5352 | 0 | 1 | 0 | 0 | 1.84469 | 0.00492952 | 26.6945 | 11.5352 |
| 93 | 2026-03-02 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | 0 | -11.5256 | 0 | 1 | 0 | 0 | 1.83835 | -0.00555423 | 30.2671 | 11.5256 |
| 93 | 2026-03-02 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -11.5352 | 0 | 1 | -0 | -0 | 1.84469 | 0.00492952 | 26.6945 | 11.5352 |
| 93 | 2026-03-02 | TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | -0 | -11.5256 | 0 | 1 | -0 | -0 | 1.83835 | -0.00555423 | 30.2671 | 11.5256 |
| 94 | 2026-03-02 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -13.7485 | 0 | 1 | 0 | 0 | 3.32027 | -0.00270203 | 8.1397 | 13.7485 |
| 94 | 2026-03-02 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -13.7381 | 0 | 1 | -0 | -0 | 3.31334 | 0.00212035 | 6.4004 | 13.7381 |
| 94 | 2026-03-02 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -13.7381 | 0 | 1 | 0 | 0 | 3.31334 | 0.00212035 | 6.4004 | 13.7381 |
| 94 | 2026-03-02 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -13.7485 | 0 | 1 | -0 | -0 | 3.32027 | -0.00270203 | 8.1397 | 13.7485 |
| 94 | 2026-03-02 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -13.7428 | 0 | 1 | -0 | -0 | 3.31643 | 0.00953262 | 28.7146 | 13.7428 |
| 94 | 2026-03-02 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -13.7514 | 0 | 1 | 0 | 0 | 3.32219 | -0.00145723 | 4.38679 | 13.7514 |
| 94 | 2026-03-02 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | -0 | -13.731 | 0 | 1 | -0 | -0 | 3.30855 | -0.00958744 | 29.012 | 13.731 |
| 94 | 2026-03-02 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -13.7428 | 0 | 1 | 0 | 0 | 3.31643 | 0.00953262 | 28.7146 | 13.7428 |
| 94 | 2026-03-02 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | 0 | -13.731 | 0 | 1 | 0 | 0 | 3.30855 | -0.00958744 | 29.012 | 13.731 |
| 94 | 2026-03-02 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -13.7359 | 0 | 1 | -0 | -0 | 3.31182 | 0.00131647 | 3.97379 | 13.7359 |
| 94 | 2026-03-02 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -13.7359 | 0 | 1 | 0 | 0 | 3.31182 | 0.00131647 | 3.97379 | 13.7359 |
| 94 | 2026-03-02 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -13.7514 | 0 | 1 | -0 | -0 | 3.32219 | -0.00145723 | 4.38679 | 13.7514 |
| 95 | 2026-03-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -12.628 | 0 | 1 | -0 | -0 | 2.57327 | 0.00110315 | 4.28695 | 12.628 |
| 95 | 2026-03-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -12.6255 | 0 | 1 | -0 | -0 | 2.57161 | 0.00211751 | 8.23472 | 12.6255 |
| 95 | 2026-03-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -12.6429 | 0 | 1 | -0 | -0 | 2.58316 | -0.0020029 | 7.75476 | 12.6429 |
| 95 | 2026-03-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -12.628 | 0 | 1 | 0 | 0 | 2.57327 | 0.00110315 | 4.28695 | 12.628 |
| 95 | 2026-03-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | -0 | -12.6224 | 0 | 1 | -0 | -0 | 2.56951 | -0.00804128 | 31.3113 | 12.6224 |
| 95 | 2026-03-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | -0 | -12.6332 | 0 | 1 | -0 | -0 | 2.57674 | 0.00651763 | 25.2744 | 12.6332 |
| 95 | 2026-03-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1950 | 0 | 0 | -12.6332 | 0 | 1 | 0 | 0 | 2.57674 | 0.00651763 | 25.2744 | 12.6332 |
| 95 | 2026-03-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 1800 | 0 | 0 | -12.6224 | 0 | 1 | 0 | 0 | 2.56951 | -0.00804128 | 31.3113 | 12.6224 |
| 95 | 2026-03-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -12.6255 | 0 | 1 | 0 | 0 | 2.57161 | 0.00211751 | 8.23472 | 12.6255 |
| 95 | 2026-03-02 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -12.6429 | 0 | 1 | 0 | 0 | 2.58316 | -0.0020029 | 7.75476 | 12.6429 |
| 96 | 2026-03-02 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.1455 | 0 | 1 | 0 | 0 | 2.25162 | -0.00101441 | 4.50527 | 12.1455 |
| 96 | 2026-03-02 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -12.1504 | 0 | 1 | -0 | -0 | 2.25486 | 0.00172281 | 7.64241 | 12.1504 |
| 96 | 2026-03-02 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | -0 | -12.1355 | 0 | 1 | -0 | -0 | 2.24494 | -0.00706597 | 31.5105 | 12.1355 |
| 96 | 2026-03-02 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -12.1504 | 0 | 1 | 0 | 0 | 2.25486 | 0.00172281 | 7.64241 | 12.1504 |
| 96 | 2026-03-02 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.1455 | 0 | 1 | -0 | -0 | 2.25162 | -0.00101441 | 4.50527 | 12.1455 |
| 96 | 2026-03-02 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 1750 | 0 | 0 | -12.1355 | 0 | 1 | 0 | 0 | 2.24494 | -0.00706597 | 31.5105 | 12.1355 |
| 96 | 2026-03-02 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | 0 | -12.1505 | 0 | 1 | 0 | 0 | 2.25493 | -0.00158355 | 7.02432 | 12.1505 |
| 96 | 2026-03-02 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2200 | 0 | -0 | -12.145 | 0 | 1 | -0 | -0 | 2.25122 | 0.00594974 | 26.4142 | 12.145 |
| 96 | 2026-03-02 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R03_5_10bp | 550 | 0 | -0 | -12.1505 | 0 | 1 | -0 | -0 | 2.25493 | -0.00158355 | 7.02432 | 12.1505 |
| 96 | 2026-03-02 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -12.1581 | 0 | 1 | 0 | 0 | 2.26001 | 0.00102107 | 4.51799 | 12.1581 |
| 96 | 2026-03-02 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S02_1_2p5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -12.1581 | 0 | 1 | -0 | -0 | 2.26001 | 0.00102107 | 4.51799 | 12.1581 |
| 96 | 2026-03-02 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 2200 | 0 | 0 | -12.145 | 0 | 1 | 0 | 0 | 2.25122 | 0.00594974 | 26.4142 | 12.145 |
| 97 | 2026-04-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -15.2277 | 0 | 1 | -0 | -0 | 4.30642 | 0.0024379 | 5.65402 | 15.2277 |
| 97 | 2026-04-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -15.1125 | 0 | 1 | -0 | -0 | 4.22957 | -0.00186868 | 4.41275 | 15.1125 |
| 97 | 2026-04-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -15.1125 | 0 | 1 | 0 | 0 | 4.22957 | -0.00186868 | 4.41275 | 15.1125 |
| 97 | 2026-04-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -15.2277 | 0 | 1 | 0 | 0 | 4.30642 | 0.0024379 | 5.65402 | 15.2277 |
| 97 | 2026-04-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2900 | 0 | -0 | -15.1765 | 0 | 1 | -0 | -0 | 4.27226 | -0.0251313 | 59.2362 | 15.1765 |
| 97 | 2026-04-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2900 | 0 | 0 | -15.1765 | 0 | 1 | 0 | 0 | 4.27226 | -0.0251313 | 59.2362 | 15.1765 |
| 97 | 2026-04-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -15.1343 | 0 | 1 | -0 | -0 | 4.2441 | -0.00324645 | 7.65394 | 15.1343 |
| 97 | 2026-04-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -15.1343 | 0 | 1 | 0 | 0 | 4.2441 | -0.00324645 | 7.65394 | 15.1343 |
| 97 | 2026-04-01 | ADANIPORTS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | -0 | -15.2005 | 0 | 1 | -0 | -0 | 4.28823 | 0.0309929 | 71.9369 | 15.2005 |
| 97 | 2026-04-01 | ADANIPORTS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | 0 | -15.2005 | 0 | 1 | 0 | 0 | 4.28823 | 0.0309929 | 71.9369 | 15.2005 |
| 98 | 2026-04-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -14.3458 | 0 | 1 | 0 | 0 | 3.71848 | -0.00247705 | 6.67838 | 14.3458 |
| 98 | 2026-04-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -14.32 | 0 | 1 | -0 | -0 | 3.70124 | 0.00109561 | 2.96011 | 14.32 |
| 98 | 2026-04-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -14.32 | 0 | 1 | 0 | 0 | 3.70124 | 0.00109561 | 2.96011 | 14.32 |
| 98 | 2026-04-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -14.3458 | 0 | 1 | -0 | -0 | 3.71848 | -0.00247705 | 6.67838 | 14.3458 |
| 98 | 2026-04-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | 0 | -14.3222 | 0 | 1 | 0 | 0 | 3.70269 | -0.00155285 | 4.19585 | 14.3222 |
| 98 | 2026-04-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3000 | 0 | -0 | -14.2912 | 0 | 1 | -0 | -0 | 3.68203 | -0.016165 | 44.0296 | 14.2912 |
| 98 | 2026-04-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3000 | 0 | 0 | -14.2912 | 0 | 1 | 0 | 0 | 3.68203 | -0.016165 | 44.0296 | 14.2912 |
| 98 | 2026-04-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | -0 | -14.3222 | 0 | 1 | -0 | -0 | 3.70269 | -0.00155285 | 4.19585 | 14.3222 |
| 98 | 2026-04-01 | AXISBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | -0 | -14.3043 | 0 | 1 | -0 | -0 | 3.69078 | 0.0195109 | 52.6781 | 14.3043 |
| 98 | 2026-04-01 | AXISBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2400 | 0 | 0 | -14.3043 | 0 | 1 | 0 | 0 | 3.69078 | 0.0195109 | 52.6781 | 14.3043 |
| 99 | 2026-04-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | -0 | -15.9224 | 0 | 1 | -0 | -0 | 4.76949 | 0.0301043 | 62.8548 | 15.9224 |
| 99 | 2026-04-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | 0 | -15.9224 | 0 | 1 | 0 | 0 | 4.76949 | 0.0301043 | 62.8548 | 15.9224 |
| 99 | 2026-04-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -15.9088 | 0 | 1 | 0 | 0 | 4.76044 | -0.00382065 | 8.0285 | 15.9088 |
| 99 | 2026-04-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -15.9088 | 0 | 1 | -0 | -0 | 4.76044 | -0.00382065 | 8.0285 | 15.9088 |
| 99 | 2026-04-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | 0 | -15.8936 | 0 | 1 | 0 | 0 | 4.7503 | -0.0244268 | 51.5132 | 15.8936 |
| 99 | 2026-04-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -15.7996 | 0 | 1 | -0 | -0 | 4.68768 | -0.00186842 | 3.98599 | 15.7996 |
| 99 | 2026-04-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -15.7996 | 0 | 1 | 0 | 0 | 4.68768 | -0.00186842 | 3.98599 | 15.7996 |
| 99 | 2026-04-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | -0 | -15.8936 | 0 | 1 | -0 | -0 | 4.7503 | -0.0244268 | 51.5132 | 15.8936 |
| 99 | 2026-04-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -15.9083 | 0 | 1 | -0 | -0 | 4.76009 | 0.00166109 | 3.48956 | 15.9083 |
| 99 | 2026-04-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -15.9263 | 0 | 1 | 0 | 0 | 4.77212 | 0.00387847 | 8.11632 | 15.9263 |
| 99 | 2026-04-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -15.9263 | 0 | 1 | -0 | -0 | 4.77212 | 0.00387847 | 8.11632 | 15.9263 |
| 99 | 2026-04-01 | BAJAJ-AUTO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -15.9083 | 0 | 1 | 0 | 0 | 4.76009 | 0.00166109 | 3.48956 | 15.9083 |
| 100 | 2026-04-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -17.108 | 0 | 1 | 0 | 0 | 5.55993 | -0.00398363 | 7.15477 | 17.108 |
| 100 | 2026-04-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2850 | 0 | 0 | -17.0972 | 0 | 1 | 0 | 0 | 5.55272 | -0.0219843 | 39.6793 | 17.0972 |
| 100 | 2026-04-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2850 | 0 | -0 | -17.0972 | 0 | 1 | -0 | -0 | 5.55272 | -0.0219843 | 39.6793 | 17.0972 |
| 100 | 2026-04-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -17.1098 | 0 | 1 | -0 | -0 | 5.56112 | 0.0272942 | 48.9042 | 17.1098 |
| 100 | 2026-04-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -17.108 | 0 | 1 | -0 | -0 | 5.55993 | -0.00398363 | 7.15477 | 17.108 |
| 100 | 2026-04-01 | BANKBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | -0 | -17.0799 | 0 | 1 | -0 | -0 | 5.54121 | 0.00406167 | 7.33523 | 17.0799 |
| 100 | 2026-04-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -17.1098 | 0 | 1 | 0 | 0 | 5.56112 | 0.0272942 | 48.9042 | 17.1098 |
| 100 | 2026-04-01 | BANKBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 650 | 0 | 0 | -17.0799 | 0 | 1 | 0 | 0 | 5.54121 | 0.00406167 | 7.33523 | 17.0799 |
| 101 | 2026-04-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -14.1445 | 0 | 1 | -0 | -0 | 3.58423 | 0.00128421 | 3.58295 | 14.1445 |
| 101 | 2026-04-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -14.1442 | 0 | 1 | 0 | 0 | 3.58407 | 0.00280054 | 7.80751 | 14.1442 |
| 101 | 2026-04-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -14.1442 | 0 | 1 | -0 | -0 | 3.58407 | 0.00280054 | 7.80751 | 14.1442 |
| 101 | 2026-04-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3050 | 0 | 0 | -14.1516 | 0 | 1 | 0 | 0 | 3.58898 | -0.0175269 | 49.073 | 14.1516 |
| 101 | 2026-04-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3050 | 0 | -0 | -14.1516 | 0 | 1 | -0 | -0 | 3.58898 | -0.0175269 | 49.073 | 14.1516 |
| 101 | 2026-04-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -14.1445 | 0 | 1 | 0 | 0 | 3.58423 | 0.00128421 | 3.58295 | 14.1445 |
| 101 | 2026-04-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -14.1686 | 0 | 1 | -0 | -0 | 3.6003 | 0.0217311 | 60.2597 | 14.1686 |
| 101 | 2026-04-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | 0 | -14.2136 | 0 | 1 | 0 | 0 | 3.63033 | -0.00301491 | 8.30479 | 14.2136 |
| 101 | 2026-04-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | -0 | -14.2136 | 0 | 1 | -0 | -0 | 3.63033 | -0.00301491 | 8.30479 | 14.2136 |
| 101 | 2026-04-01 | BHARTIARTL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | 0 | -14.1871 | 0 | 1 | 0 | 0 | 3.61263 | -0.0013056 | 3.61399 | 14.1871 |
| 101 | 2026-04-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -14.1686 | 0 | 1 | 0 | 0 | 3.6003 | 0.0217311 | 60.2597 | 14.1686 |
| 101 | 2026-04-01 | BHARTIARTL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | -0 | -14.1871 | 0 | 1 | -0 | -0 | 3.61263 | -0.0013056 | 3.61399 | 14.1871 |
| 102 | 2026-04-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -15.8891 | 0 | 1 | 0 | 0 | 4.74734 | -0.00300687 | 6.3338 | 15.8891 |
| 102 | 2026-04-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -15.8878 | 0 | 1 | -0 | -0 | 4.74644 | 0.00199852 | 4.21374 | 15.8878 |
| 102 | 2026-04-01 | BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | 0 | -15.747 | 0 | 1 | 0 | 0 | 4.65261 | 0.00432532 | 9.29656 | 15.747 |
| 102 | 2026-04-01 | BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | 0 | -15.92 | 0 | 1 | 0 | 0 | 4.7679 | 0.0296506 | 62.0641 | 15.92 |
| 102 | 2026-04-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | -0 | -15.747 | 0 | 1 | -0 | -0 | 4.65261 | 0.00432532 | 9.29656 | 15.747 |
| 102 | 2026-04-01 | BPCL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3150 | 0 | -0 | -15.9018 | 0 | 1 | -0 | -0 | 4.75576 | -0.022899 | 48.3586 | 15.9018 |
| 102 | 2026-04-01 | BPCL | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -15.8878 | 0 | 1 | 0 | 0 | 4.74644 | 0.00199852 | 4.21374 | 15.8878 |
| 102 | 2026-04-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3150 | 0 | 0 | -15.9018 | 0 | 1 | 0 | 0 | 4.75576 | -0.022899 | 48.3586 | 15.9018 |
| 102 | 2026-04-01 | BPCL | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | -0 | -15.92 | 0 | 1 | -0 | -0 | 4.7679 | 0.0296506 | 62.0641 | 15.92 |
| 102 | 2026-04-01 | BPCL | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -15.8891 | 0 | 1 | -0 | -0 | 4.74734 | -0.00300687 | 6.3338 | 15.8891 |
| 103 | 2026-04-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -16.9716 | 0 | 1 | -0 | -0 | 5.46896 | 0.00149507 | 2.73373 | 16.9716 |
| 103 | 2026-04-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -16.9716 | 0 | 1 | 0 | 0 | 5.46896 | 0.00149507 | 2.73373 | 16.9716 |
| 103 | 2026-04-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -17.0259 | 0 | 1 | 0 | 0 | 5.50517 | 0.00425311 | 7.73353 | 17.0259 |
| 103 | 2026-04-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -17.0503 | 0 | 1 | -0 | -0 | 5.52146 | 0.025541 | 46.1973 | 17.0503 |
| 103 | 2026-04-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -17.0503 | 0 | 1 | 0 | 0 | 5.52146 | 0.025541 | 46.1973 | 17.0503 |
| 103 | 2026-04-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -17.0259 | 0 | 1 | -0 | -0 | 5.50517 | 0.00425311 | 7.73353 | 17.0259 |
| 103 | 2026-04-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -17.0647 | 0 | 1 | -0 | -0 | 5.53105 | -0.00331289 | 5.99227 | 17.0647 |
| 103 | 2026-04-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -17.0647 | 0 | 1 | 0 | 0 | 5.53105 | -0.00331289 | 5.99227 | 17.0647 |
| 103 | 2026-04-01 | BRITANNIA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | -0 | -17.0254 | 0 | 1 | -0 | -0 | 5.50485 | -0.0201682 | 36.736 | 17.0254 |
| 103 | 2026-04-01 | BRITANNIA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | 0 | -17.0254 | 0 | 1 | 0 | 0 | 5.50485 | -0.0201682 | 36.736 | 17.0254 |
| 104 | 2026-04-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -16.0033 | 0 | 1 | 0 | 0 | 4.82347 | 0.00216047 | 4.47798 | 16.0033 |
| 104 | 2026-04-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | 0 | -16.0318 | 0 | 1 | 0 | 0 | 4.84248 | -0.00428344 | 8.84618 | 16.0318 |
| 104 | 2026-04-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | -0 | -16.019 | 0 | 1 | -0 | -0 | 4.83391 | 0.0208233 | 42.9781 | 16.019 |
| 104 | 2026-04-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -16.0689 | 0 | 1 | -0 | -0 | 4.86722 | 0.0037191 | 7.64159 | 16.0689 |
| 104 | 2026-04-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -16.0033 | 0 | 1 | -0 | -0 | 4.82347 | 0.00216047 | 4.47798 | 16.0033 |
| 104 | 2026-04-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -15.9632 | 0 | 1 | -0 | -0 | 4.79671 | -0.0021057 | 4.38866 | 15.9632 |
| 104 | 2026-04-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | 0 | -15.9958 | 0 | 1 | 0 | 0 | 4.81843 | -0.016336 | 33.9321 | 15.9958 |
| 104 | 2026-04-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | 0 | -16.019 | 0 | 1 | 0 | 0 | 4.83391 | 0.0208233 | 42.9781 | 16.019 |
| 104 | 2026-04-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 450 | 0 | -0 | -16.0318 | 0 | 1 | -0 | -0 | 4.84248 | -0.00428344 | 8.84618 | 16.0318 |
| 104 | 2026-04-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | -0 | -15.9958 | 0 | 1 | -0 | -0 | 4.81843 | -0.016336 | 33.9321 | 15.9958 |
| 104 | 2026-04-01 | CIPLA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -16.0689 | 0 | 1 | 0 | 0 | 4.86722 | 0.0037191 | 7.64159 | 16.0689 |
| 104 | 2026-04-01 | CIPLA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -15.9632 | 0 | 1 | 0 | 0 | 4.79671 | -0.0021057 | 4.38866 | 15.9632 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -15.9634 | 0 | 1 | -0 | -0 | 4.79688 | -0.00375835 | 7.83782 | 15.9634 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 350 | 0 | -0 | -15.9745 | 0 | 1 | -0 | -0 | 4.80428 | -0.001982 | 4.12249 | 15.9745 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -15.9717 | 0 | 1 | 0 | 0 | 4.80237 | 0.0256023 | 53.2314 | 15.9717 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 350 | 0 | 0 | -15.9745 | 0 | 1 | 0 | 0 | 4.80428 | -0.001982 | 4.12249 | 15.9745 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -15.93 | 0 | 1 | -0 | -0 | 4.77458 | 0.00171149 | 3.58204 | 15.93 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2900 | 0 | -0 | -15.9396 | 0 | 1 | -0 | -0 | 4.78102 | -0.0183649 | 38.5384 | 15.9396 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -15.93 | 0 | 1 | 0 | 0 | 4.77458 | 0.00171149 | 3.58204 | 15.93 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2900 | 0 | 0 | -15.9396 | 0 | 1 | 0 | 0 | 4.78102 | -0.0183649 | 38.5384 | 15.9396 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -15.9717 | 0 | 1 | -0 | -0 | 4.80237 | 0.0256023 | 53.2314 | 15.9717 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -15.9718 | 0 | 1 | 0 | 0 | 4.80248 | 0.00345401 | 7.19477 | 15.9718 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R01_0p25_2p5bp | 50 | 0 | 0 | -15.8861 | 0 | 1 | 0 | 0 | 4.74533 | 0.00112564 | 2.3721 | 15.8861 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -15.9634 | 0 | 1 | 0 | 0 | 4.79688 | -0.00375835 | 7.83782 | 15.9634 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -15.9718 | 0 | 1 | -0 | -0 | 4.80248 | 0.00345401 | 7.19477 | 15.9718 |
| 105 | 2026-04-01 | DRREDDY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R01_0p25_2p5bp | 50 | 0 | -0 | -15.8861 | 0 | 1 | -0 | -0 | 4.74533 | 0.00112564 | 2.3721 | 15.8861 |
| 106 | 2026-04-01 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -12.5471 | 0 | 1 | 0 | 0 | 2.51931 | 0.00105738 | 4.1971 | 12.5471 |
| 106 | 2026-04-01 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 50 | 0 | 0 | -12.4992 | 0 | 1 | 0 | 0 | 2.48736 | -0.0166087 | 66.7724 | 12.4992 |
| 106 | 2026-04-01 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2600 | 0 | -0 | -12.5752 | 0 | 1 | -0 | -0 | 2.53806 | -0.0092589 | 36.5903 | 12.5752 |
| 106 | 2026-04-01 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -12.5768 | 0 | 1 | 0 | 0 | 2.53914 | 0.00208534 | 8.21375 | 12.5768 |
| 106 | 2026-04-01 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S02_1_2p5bp | C01_lt_1bp | R04_ge_10bp | 50 | 0 | -0 | -12.4992 | 0 | 1 | -0 | -0 | 2.48736 | -0.0166087 | 66.7724 | 12.4992 |
| 106 | 2026-04-01 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | 0 | -12.5804 | 0 | 1 | 0 | 0 | 2.54153 | -0.00202076 | 7.9498 | 12.5804 |
| 106 | 2026-04-01 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -12.5768 | 0 | 1 | -0 | -0 | 2.53914 | 0.00208534 | 8.21375 | 12.5768 |
| 106 | 2026-04-01 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -12.5471 | 0 | 1 | -0 | -0 | 2.51931 | 0.00105738 | 4.1971 | 12.5471 |
| 106 | 2026-04-01 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2600 | 0 | 0 | -12.5752 | 0 | 1 | 0 | 0 | 2.53806 | -0.0092589 | 36.5903 | 12.5752 |
| 106 | 2026-04-01 | GOLDBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -12.5913 | 0 | 1 | -0 | -0 | 2.54876 | 0.0118486 | 46.4533 | 12.5913 |
| 106 | 2026-04-01 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -12.5913 | 0 | 1 | 0 | 0 | 2.54876 | 0.0118486 | 46.4533 | 12.5913 |
| 106 | 2026-04-01 | GOLDBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 400 | 0 | -0 | -12.5804 | 0 | 1 | -0 | -0 | 2.54153 | -0.00202076 | 7.9498 | 12.5804 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -15.9553 | 0 | 1 | 0 | 0 | 4.79145 | -0.00178566 | 3.72742 | 15.9553 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -15.9517 | 0 | 1 | 0 | 0 | 4.78903 | 0.0020355 | 4.25263 | 15.9517 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -15.9517 | 0 | 1 | -0 | -0 | 4.78903 | 0.0020355 | 4.25263 | 15.9517 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2900 | 0 | 0 | -15.9266 | 0 | 1 | 0 | 0 | 4.77233 | -0.0210974 | 44.3092 | 15.9266 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -15.9553 | 0 | 1 | -0 | -0 | 4.79145 | -0.00178566 | 3.72742 | 15.9553 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -15.9102 | 0 | 1 | 0 | 0 | 4.76137 | -0.00365351 | 7.67496 | 15.9102 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R01_0p25_2p5bp | 150 | 0 | 0 | -15.8936 | 0 | 1 | 0 | 0 | 4.75033 | -0.00112858 | 2.37573 | 15.8936 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2900 | 0 | -0 | -15.9266 | 0 | 1 | -0 | -0 | 4.77233 | -0.0210974 | 44.3092 | 15.9266 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R01_0p25_2p5bp | 100 | 0 | 0 | -16.0332 | 0 | 1 | 0 | 0 | 4.8434 | 0.00117264 | 2.42111 | 16.0332 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | 0 | -15.7687 | 0 | 1 | 0 | 0 | 4.66708 | 0.00253981 | 5.44197 | 15.7687 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R01_0p25_2p5bp | 100 | 0 | -0 | -16.0332 | 0 | 1 | -0 | -0 | 4.8434 | 0.00117264 | 2.42111 | 16.0332 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | -0 | -15.7687 | 0 | 1 | -0 | -0 | 4.66708 | 0.00253981 | 5.44197 | 15.7687 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2200 | 0 | 0 | -15.9438 | 0 | 1 | 0 | 0 | 4.78377 | 0.0255526 | 53.2581 | 15.9438 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R01_0p25_2p5bp | 150 | 0 | -0 | -15.8936 | 0 | 1 | -0 | -0 | 4.75033 | -0.00112858 | 2.37573 | 15.8936 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -15.9102 | 0 | 1 | -0 | -0 | 4.76137 | -0.00365351 | 7.67496 | 15.9102 |
| 107 | 2026-04-01 | HCLTECH | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2200 | 0 | -0 | -15.9438 | 0 | 1 | -0 | -0 | 4.78377 | 0.0255526 | 53.2581 | 15.9438 |
| 108 | 2026-04-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | 0 | -13.1309 | 0 | 1 | 0 | 0 | 2.9085 | -0.00152348 | 5.23804 | 13.1309 |
| 108 | 2026-04-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -13.2286 | 0 | 1 | 0 | 0 | 2.97367 | 0.0163796 | 54.8953 | 13.2286 |
| 108 | 2026-04-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3250 | 0 | -0 | -13.2102 | 0 | 1 | -0 | -0 | 2.96141 | -0.012944 | 43.7842 | 13.2102 |
| 108 | 2026-04-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3250 | 0 | 0 | -13.2102 | 0 | 1 | 0 | 0 | 2.96141 | -0.012944 | 43.7842 | 13.2102 |
| 108 | 2026-04-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -13.1864 | 0 | 1 | -0 | -0 | 2.94553 | 0.0013317 | 4.5175 | 13.1864 |
| 108 | 2026-04-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -13.273 | 0 | 1 | 0 | 0 | 3.00325 | 0.00222002 | 7.39714 | 13.273 |
| 108 | 2026-04-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -13.2286 | 0 | 1 | -0 | -0 | 2.97367 | 0.0163796 | 54.8953 | 13.2286 |
| 108 | 2026-04-01 | HDFCBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -13.273 | 0 | 1 | -0 | -0 | 3.00325 | 0.00222002 | 7.39714 | 13.273 |
| 108 | 2026-04-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -13.1864 | 0 | 1 | 0 | 0 | 2.94553 | 0.0013317 | 4.5175 | 13.1864 |
| 108 | 2026-04-01 | HDFCBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | -0 | -13.1309 | 0 | 1 | -0 | -0 | 2.9085 | -0.00152348 | 5.23804 | 13.1309 |
| 109 | 2026-04-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -15.0433 | 0 | 1 | 0 | 0 | 4.18344 | -0.00354249 | 8.45946 | 15.0433 |
| 109 | 2026-04-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -14.9173 | 0 | 1 | -0 | -0 | 4.09948 | 0.00233264 | 5.69028 | 14.9173 |
| 109 | 2026-04-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -15.0367 | 0 | 1 | 0 | 0 | 4.17905 | 0.00174572 | 4.1773 | 15.0367 |
| 109 | 2026-04-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2300 | 0 | 0 | -14.9941 | 0 | 1 | 0 | 0 | 4.15067 | 0.0181336 | 43.5876 | 14.9941 |
| 109 | 2026-04-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -15.0433 | 0 | 1 | -0 | -0 | 4.18344 | -0.00354249 | 8.45946 | 15.0433 |
| 109 | 2026-04-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -15.0201 | 0 | 1 | -0 | -0 | 4.168 | -0.00173814 | 4.16974 | 15.0201 |
| 109 | 2026-04-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2650 | 0 | -0 | -14.9728 | 0 | 1 | -0 | -0 | 4.13643 | -0.0162921 | 39.4367 | 14.9728 |
| 109 | 2026-04-01 | HINDUNILVR | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -14.9173 | 0 | 1 | 0 | 0 | 4.09948 | 0.00233264 | 5.69028 | 14.9173 |
| 109 | 2026-04-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2650 | 0 | 0 | -14.9728 | 0 | 1 | 0 | 0 | 4.13643 | -0.0162921 | 39.4367 | 14.9728 |
| 109 | 2026-04-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2300 | 0 | -0 | -14.9941 | 0 | 1 | -0 | -0 | 4.15067 | 0.0181336 | 43.5876 | 14.9941 |
| 109 | 2026-04-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -15.0201 | 0 | 1 | 0 | 0 | 4.168 | -0.00173814 | 4.16974 | 15.0201 |
| 109 | 2026-04-01 | HINDUNILVR | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -15.0367 | 0 | 1 | -0 | -0 | 4.17905 | 0.00174572 | 4.1773 | 15.0367 |
| 110 | 2026-04-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2800 | 0 | 0 | -13.9543 | 0 | 1 | 0 | 0 | 3.45742 | -0.0186362 | 54.1042 | 13.9543 |
| 110 | 2026-04-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -13.9769 | 0 | 1 | 0 | 0 | 3.47252 | 0.00250335 | 7.18956 | 13.9769 |
| 110 | 2026-04-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -13.9785 | 0 | 1 | -0 | -0 | 3.4736 | 0.00156696 | 4.51232 | 13.9785 |
| 110 | 2026-04-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2650 | 0 | 0 | -13.9615 | 0 | 1 | 0 | 0 | 3.46224 | 0.0180926 | 52.0954 | 13.9615 |
| 110 | 2026-04-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -13.8515 | 0 | 1 | -0 | -0 | 3.38891 | -0.00137873 | 4.06835 | 13.8515 |
| 110 | 2026-04-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2650 | 0 | -0 | -13.9615 | 0 | 1 | -0 | -0 | 3.46224 | 0.0180926 | 52.0954 | 13.9615 |
| 110 | 2026-04-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2800 | 0 | -0 | -13.9543 | 0 | 1 | -0 | -0 | 3.45742 | -0.0186362 | 54.1042 | 13.9543 |
| 110 | 2026-04-01 | ICICIBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -13.9785 | 0 | 1 | 0 | 0 | 3.4736 | 0.00156696 | 4.51232 | 13.9785 |
| 110 | 2026-04-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -13.9769 | 0 | 1 | -0 | -0 | 3.47252 | 0.00250335 | 7.18956 | 13.9769 |
| 110 | 2026-04-01 | ICICIBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -13.8515 | 0 | 1 | 0 | 0 | 3.38891 | -0.00137873 | 4.06835 | 13.8515 |
| 111 | 2026-04-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -15.449 | 0 | 1 | -0 | -0 | 4.45392 | 0.00301123 | 6.76301 | 15.449 |
| 111 | 2026-04-01 | INFY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3100 | 0 | -0 | -15.3861 | 0 | 1 | -0 | -0 | 4.41197 | -0.0192429 | 43.6844 | 15.3861 |
| 111 | 2026-04-01 | INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -15.449 | 0 | 1 | 0 | 0 | 4.45392 | 0.00301123 | 6.76301 | 15.449 |
| 111 | 2026-04-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -15.3823 | 0 | 1 | 0 | 0 | 4.40943 | -0.00272777 | 6.18142 | 15.3823 |
| 111 | 2026-04-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -15.2887 | 0 | 1 | -0 | -0 | 4.34707 | 0.00113353 | 2.60756 | 15.2887 |
| 111 | 2026-04-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | -0 | -15.4132 | 0 | 1 | -0 | -0 | 4.43008 | 0.0250022 | 56.2997 | 15.4132 |
| 111 | 2026-04-01 | INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | 0 | -15.4132 | 0 | 1 | 0 | 0 | 4.43008 | 0.0250022 | 56.2997 | 15.4132 |
| 111 | 2026-04-01 | INFY | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3100 | 0 | 0 | -15.3861 | 0 | 1 | 0 | 0 | 4.41197 | -0.0192429 | 43.6844 | 15.3861 |
| 111 | 2026-04-01 | INFY | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -15.3823 | 0 | 1 | -0 | -0 | 4.40943 | -0.00272777 | 6.18142 | 15.3823 |
| 111 | 2026-04-01 | INFY | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -15.2887 | 0 | 1 | 0 | 0 | 4.34707 | 0.00113353 | 2.60756 | 15.2887 |
| 112 | 2026-04-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -17.9226 | 0 | 1 | 0 | 0 | 6.10297 | 0.0046545 | 7.62418 | 17.9226 |
| 112 | 2026-04-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -17.9355 | 0 | 1 | 0 | 0 | 6.1116 | 0.00186703 | 3.05487 | 17.9355 |
| 112 | 2026-04-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -17.8288 | 0 | 1 | -0 | -0 | 6.04047 | -0.00182492 | 3.02115 | 17.8288 |
| 112 | 2026-04-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | 0 | -17.8996 | 0 | 1 | 0 | 0 | 6.08768 | -0.0284948 | 46.9715 | 17.8996 |
| 112 | 2026-04-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -17.9355 | 0 | 1 | -0 | -0 | 6.1116 | 0.00186703 | 3.05487 | 17.9355 |
| 112 | 2026-04-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | -0 | -17.8996 | 0 | 1 | -0 | -0 | 6.08768 | -0.0284948 | 46.9715 | 17.8996 |
| 112 | 2026-04-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | -0 | -17.9339 | 0 | 1 | -0 | -0 | 6.11051 | 0.0392847 | 64.0765 | 17.9339 |
| 112 | 2026-04-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -17.8288 | 0 | 1 | 0 | 0 | 6.04047 | -0.00182492 | 3.02115 | 17.8288 |
| 112 | 2026-04-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | 0 | -17.9092 | 0 | 1 | 0 | 0 | 6.09404 | -0.00433382 | 7.11297 | 17.9092 |
| 112 | 2026-04-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 1900 | 0 | 0 | -17.9339 | 0 | 1 | 0 | 0 | 6.11051 | 0.0392847 | 64.0765 | 17.9339 |
| 112 | 2026-04-01 | ITBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 600 | 0 | -0 | -17.9092 | 0 | 1 | -0 | -0 | 6.09404 | -0.00433382 | 7.11297 | 17.9092 |
| 112 | 2026-04-01 | ITBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -17.9226 | 0 | 1 | -0 | -0 | 6.10297 | 0.0046545 | 7.62418 | 17.9226 |
| 113 | 2026-04-01 | ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -16.6528 | 0 | 1 | -0 | -0 | 5.25643 | -0.00390565 | 7.44101 | 16.6528 |
| 113 | 2026-04-01 | ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | 0 | -16.6543 | 0 | 1 | 0 | 0 | 5.25748 | 0.0267575 | 50.729 | 16.6543 |
| 113 | 2026-04-01 | ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -16.6229 | 0 | 1 | -0 | -0 | 5.23652 | -0.00182871 | 3.49223 | 16.6229 |
| 113 | 2026-04-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -16.6705 | 0 | 1 | -0 | -0 | 5.26825 | 0.00184965 | 3.51093 | 16.6705 |
| 113 | 2026-04-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -16.6229 | 0 | 1 | 0 | 0 | 5.23652 | -0.00182871 | 3.49223 | 16.6229 |
| 113 | 2026-04-01 | ITC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2950 | 0 | -0 | -16.6279 | 0 | 1 | -0 | -0 | 5.23988 | -0.0216261 | 41.4507 | 16.6279 |
| 113 | 2026-04-01 | ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -16.6705 | 0 | 1 | 0 | 0 | 5.26825 | 0.00184965 | 3.51093 | 16.6705 |
| 113 | 2026-04-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -16.6528 | 0 | 1 | 0 | 0 | 5.25643 | -0.00390565 | 7.44101 | 16.6528 |
| 113 | 2026-04-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -16.6196 | 0 | 1 | -0 | -0 | 5.23429 | 0.00378319 | 7.22517 | 16.6196 |
| 113 | 2026-04-01 | ITC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -16.6196 | 0 | 1 | 0 | 0 | 5.23429 | 0.00378319 | 7.22517 | 16.6196 |
| 113 | 2026-04-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2950 | 0 | 0 | -16.6279 | 0 | 1 | 0 | 0 | 5.23988 | -0.0216261 | 41.4507 | 16.6279 |
| 113 | 2026-04-01 | ITC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | -0 | -16.6543 | 0 | 1 | -0 | -0 | 5.25748 | 0.0267575 | 50.729 | 16.6543 |
| 114 | 2026-04-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -17.6907 | 0 | 1 | 0 | 0 | 5.94838 | 0.00441536 | 7.41667 | 17.6907 |
| 114 | 2026-04-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R01_0p25_2p5bp | 200 | 0 | 0 | -17.6841 | 0 | 1 | 0 | 0 | 5.94398 | -0.00146548 | 2.46589 | 17.6841 |
| 114 | 2026-04-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -17.6454 | 0 | 1 | 0 | 0 | 5.91817 | -0.00429666 | 7.26331 | 17.6454 |
| 114 | 2026-04-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -17.6454 | 0 | 1 | -0 | -0 | 5.91817 | -0.00429666 | 7.26331 | 17.6454 |
| 114 | 2026-04-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R01_0p25_2p5bp | 200 | 0 | -0 | -17.6841 | 0 | 1 | -0 | -0 | 5.94398 | -0.00146548 | 2.46589 | 17.6841 |
| 114 | 2026-04-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -17.6907 | 0 | 1 | -0 | -0 | 5.94838 | 0.00441536 | 7.41667 | 17.6907 |
| 114 | 2026-04-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | 0 | -17.6843 | 0 | 1 | 0 | 0 | 5.94415 | 0.0251432 | 42.2208 | 17.6843 |
| 114 | 2026-04-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | -0 | -17.6843 | 0 | 1 | -0 | -0 | 5.94415 | 0.0251432 | 42.2208 | 17.6843 |
| 114 | 2026-04-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | 0 | -17.5669 | 0 | 1 | 0 | 0 | 5.86587 | -0.0024363 | 4.15245 | 17.5669 |
| 114 | 2026-04-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | -0 | -17.5669 | 0 | 1 | -0 | -0 | 5.86587 | -0.0024363 | 4.15245 | 17.5669 |
| 114 | 2026-04-01 | JUNIORBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | 0 | -17.667 | 0 | 1 | 0 | 0 | 5.93256 | -0.0206651 | 34.9065 | 17.667 |
| 114 | 2026-04-01 | JUNIORBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | -0 | -17.667 | 0 | 1 | -0 | -0 | 5.93256 | -0.0206651 | 34.9065 | 17.667 |
| 115 | 2026-04-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -14.527 | 0 | 1 | 0 | 0 | 3.83927 | -0.00292954 | 7.65554 | 14.527 |
| 115 | 2026-04-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -14.6024 | 0 | 1 | -0 | -0 | 3.88954 | -0.00100883 | 2.5937 | 14.6024 |
| 115 | 2026-04-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -14.6024 | 0 | 1 | 0 | 0 | 3.88954 | -0.00100883 | 2.5937 | 14.6024 |
| 115 | 2026-04-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3100 | 0 | 0 | -14.486 | 0 | 1 | 0 | 0 | 3.81193 | -0.0201893 | 53.1801 | 14.486 |
| 115 | 2026-04-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | -0 | -14.5014 | 0 | 1 | -0 | -0 | 3.82221 | 0.0231966 | 60.43 | 14.5014 |
| 115 | 2026-04-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -14.4955 | 0 | 1 | 0 | 0 | 3.81828 | 0.00291088 | 7.62702 | 14.4955 |
| 115 | 2026-04-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -14.527 | 0 | 1 | -0 | -0 | 3.83927 | -0.00292954 | 7.65554 | 14.527 |
| 115 | 2026-04-01 | KOTAKBANK | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -14.4955 | 0 | 1 | -0 | -0 | 3.81828 | 0.00291088 | 7.62702 | 14.4955 |
| 115 | 2026-04-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2500 | 0 | 0 | -14.5014 | 0 | 1 | 0 | 0 | 3.82221 | 0.0231966 | 60.43 | 14.5014 |
| 115 | 2026-04-01 | KOTAKBANK | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3100 | 0 | -0 | -14.486 | 0 | 1 | -0 | -0 | 3.81193 | -0.0201893 | 53.1801 | 14.486 |
| 116 | 2026-04-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -13.9617 | 0 | 1 | -0 | -0 | 3.4624 | 0.00293967 | 8.48699 | 13.9617 |
| 116 | 2026-04-01 | LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -13.8769 | 0 | 1 | -0 | -0 | 3.40583 | -0.00116036 | 3.40699 | 13.8769 |
| 116 | 2026-04-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -13.8769 | 0 | 1 | 0 | 0 | 3.40583 | -0.00116036 | 3.40699 | 13.8769 |
| 116 | 2026-04-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -13.9751 | 0 | 1 | -0 | -0 | 3.47133 | 0.0213298 | 61.2276 | 13.9751 |
| 116 | 2026-04-01 | LT | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -13.9751 | 0 | 1 | 0 | 0 | 3.47133 | 0.0213298 | 61.2276 | 13.9751 |
| 116 | 2026-04-01 | LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -13.9101 | 0 | 1 | -0 | -0 | 3.42801 | -0.00281948 | 8.22906 | 13.9101 |
| 116 | 2026-04-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -13.9101 | 0 | 1 | 0 | 0 | 3.42801 | -0.00281948 | 8.22906 | 13.9101 |
| 116 | 2026-04-01 | LT | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2800 | 0 | -0 | -13.959 | 0 | 1 | -0 | -0 | 3.46056 | -0.0174703 | 50.7456 | 13.959 |
| 116 | 2026-04-01 | LT | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -13.9617 | 0 | 1 | 0 | 0 | 3.4624 | 0.00293967 | 8.48699 | 13.9617 |
| 116 | 2026-04-01 | LT | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2800 | 0 | 0 | -13.959 | 0 | 1 | 0 | 0 | 3.46056 | -0.0174703 | 50.7456 | 13.959 |
| 117 | 2026-04-01 | M&M | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -13.8748 | 0 | 1 | -0 | -0 | 3.40448 | -0.00263756 | 7.74519 | 13.8748 |
| 117 | 2026-04-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -13.9352 | 0 | 1 | -0 | -0 | 3.44472 | 0.00136891 | 3.9694 | 13.9352 |
| 117 | 2026-04-01 | M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -13.9352 | 0 | 1 | 0 | 0 | 3.44472 | 0.00136891 | 3.9694 | 13.9352 |
| 117 | 2026-04-01 | M&M | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2900 | 0 | -0 | -13.884 | 0 | 1 | -0 | -0 | 3.41057 | -0.0157062 | 46.1928 | 13.884 |
| 117 | 2026-04-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -13.8971 | 0 | 1 | -0 | -0 | 3.41932 | 0.018791 | 54.7479 | 13.8971 |
| 117 | 2026-04-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -13.8748 | 0 | 1 | 0 | 0 | 3.40448 | -0.00263756 | 7.74519 | 13.8748 |
| 117 | 2026-04-01 | M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -13.8971 | 0 | 1 | 0 | 0 | 3.41932 | 0.018791 | 54.7479 | 13.8971 |
| 117 | 2026-04-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2900 | 0 | 0 | -13.884 | 0 | 1 | 0 | 0 | 3.41057 | -0.0157062 | 46.1928 | 13.884 |
| 117 | 2026-04-01 | M&M | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -13.8828 | 0 | 1 | -0 | -0 | 3.40978 | 0.00303741 | 8.9057 | 13.8828 |
| 117 | 2026-04-01 | M&M | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -13.8828 | 0 | 1 | 0 | 0 | 3.40978 | 0.00303741 | 8.9057 | 13.8828 |
| 118 | 2026-04-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | 0 | -15.1584 | 0 | 1 | 0 | 0 | 4.26018 | -0.00156272 | 3.66893 | 15.1584 |
| 118 | 2026-04-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | 0 | -15.1981 | 0 | 1 | 0 | 0 | 4.28663 | 0.0231932 | 53.944 | 15.1981 |
| 118 | 2026-04-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -15.1642 | 0 | 1 | 0 | 0 | 4.26405 | 0.00181755 | 4.26223 | 15.1642 |
| 118 | 2026-04-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -15.1911 | 0 | 1 | -0 | -0 | 4.28197 | 0.00305261 | 7.12981 | 15.1911 |
| 118 | 2026-04-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -15.1911 | 0 | 1 | 0 | 0 | 4.28197 | 0.00305261 | 7.12981 | 15.1911 |
| 118 | 2026-04-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -15.1642 | 0 | 1 | -0 | -0 | 4.26405 | 0.00181755 | 4.26223 | 15.1642 |
| 118 | 2026-04-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2350 | 0 | -0 | -15.1981 | 0 | 1 | -0 | -0 | 4.28663 | 0.0231932 | 53.944 | 15.1981 |
| 118 | 2026-04-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 300 | 0 | -0 | -15.1584 | 0 | 1 | -0 | -0 | 4.26018 | -0.00156272 | 3.66893 | 15.1584 |
| 118 | 2026-04-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -15.1263 | 0 | 1 | -0 | -0 | 4.2388 | -0.00375242 | 8.84548 | 15.1263 |
| 118 | 2026-04-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3000 | 0 | 0 | -15.1786 | 0 | 1 | 0 | 0 | 4.27365 | -0.0192195 | 45.0818 | 15.1786 |
| 118 | 2026-04-01 | MARUTI | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3000 | 0 | -0 | -15.1786 | 0 | 1 | -0 | -0 | 4.27365 | -0.0192195 | 45.0818 | 15.1786 |
| 118 | 2026-04-01 | MARUTI | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -15.1263 | 0 | 1 | 0 | 0 | 4.2388 | -0.00375242 | 8.84548 | 15.1263 |
| 119 | 2026-04-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | -0 | -16.0265 | 0 | 1 | -0 | -0 | 4.8389 | 0.00234051 | 4.83656 | 16.0265 |
| 119 | 2026-04-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -15.9761 | 0 | 1 | -0 | -0 | 4.80529 | -0.00343608 | 7.14736 | 15.9761 |
| 119 | 2026-04-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | -0 | -16.0005 | 0 | 1 | -0 | -0 | 4.82158 | 0.0234016 | 48.4265 | 16.0005 |
| 119 | 2026-04-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -15.9761 | 0 | 1 | 0 | 0 | 4.80529 | -0.00343608 | 7.14736 | 15.9761 |
| 119 | 2026-04-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | -0 | -15.9735 | 0 | 1 | -0 | -0 | 4.80361 | -0.0199917 | 41.6954 | 15.9735 |
| 119 | 2026-04-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | 0 | -16.0265 | 0 | 1 | 0 | 0 | 4.8389 | 0.00234051 | 4.83656 | 16.0265 |
| 119 | 2026-04-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2100 | 0 | 0 | -16.0005 | 0 | 1 | 0 | 0 | 4.82158 | 0.0234016 | 48.4265 | 16.0005 |
| 119 | 2026-04-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | 0 | -15.9735 | 0 | 1 | 0 | 0 | 4.80361 | -0.0199917 | 41.6954 | 15.9735 |
| 119 | 2026-04-01 | NESTLEIND | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -16.0104 | 0 | 1 | -0 | -0 | 4.82818 | 0.00382276 | 7.9214 | 16.0104 |
| 119 | 2026-04-01 | NESTLEIND | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -16.0104 | 0 | 1 | 0 | 0 | 4.82818 | 0.00382276 | 7.9214 | 16.0104 |
| 120 | 2026-04-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -14.129 | 0 | 1 | -0 | -0 | 3.57395 | -0.00145181 | 4.05713 | 14.129 |
| 120 | 2026-04-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -14.1669 | 0 | 1 | -0 | -0 | 3.59921 | 0.00205348 | 5.70456 | 14.1669 |
| 120 | 2026-04-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -14.129 | 0 | 1 | 0 | 0 | 3.57395 | -0.00145181 | 4.05713 | 14.129 |
| 120 | 2026-04-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -14.1669 | 0 | 1 | 0 | 0 | 3.59921 | 0.00205348 | 5.70456 | 14.1669 |
| 120 | 2026-04-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2600 | 0 | -0 | -14.132 | 0 | 1 | -0 | -0 | 3.5759 | -0.0136458 | 38.3049 | 14.132 |
| 120 | 2026-04-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -14.1377 | 0 | 1 | 0 | 0 | 3.57972 | 0.0162133 | 45.2122 | 14.1377 |
| 120 | 2026-04-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | -0 | -14.1114 | 0 | 1 | -0 | -0 | 3.56218 | -0.00220895 | 6.20147 | 14.1114 |
| 120 | 2026-04-01 | NIFTYBEES | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | 0 | -14.1711 | 0 | 1 | 0 | 0 | 3.602 | 0.00123337 | 3.42229 | 14.1711 |
| 120 | 2026-04-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2600 | 0 | 0 | -14.132 | 0 | 1 | 0 | 0 | 3.5759 | -0.0136458 | 38.3049 | 14.132 |
| 120 | 2026-04-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -14.1377 | 0 | 1 | -0 | -0 | 3.57972 | 0.0162133 | 45.2122 | 14.1377 |
| 120 | 2026-04-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 250 | 0 | 0 | -14.1114 | 0 | 1 | 0 | 0 | 3.56218 | -0.00220895 | 6.20147 | 14.1114 |
| 120 | 2026-04-01 | NIFTYBEES | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | -0 | -14.1711 | 0 | 1 | -0 | -0 | 3.602 | 0.00123337 | 3.42229 | 14.1711 |
| 121 | 2026-04-01 | ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -14.5832 | 0 | 1 | -0 | -0 | 3.87672 | -0.00165389 | 4.26621 | 14.5832 |
| 121 | 2026-04-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -14.5832 | 0 | 1 | 0 | 0 | 3.87672 | -0.00165389 | 4.26621 | 14.5832 |
| 121 | 2026-04-01 | ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -14.6284 | 0 | 1 | -0 | -0 | 3.90682 | -0.00269924 | 6.90783 | 14.6284 |
| 121 | 2026-04-01 | ONGC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -14.6756 | 0 | 1 | 0 | 0 | 3.93831 | 0.00243055 | 6.1688 | 14.6756 |
| 121 | 2026-04-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -14.6756 | 0 | 1 | -0 | -0 | 3.93831 | 0.00243055 | 6.1688 | 14.6756 |
| 121 | 2026-04-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -14.6284 | 0 | 1 | 0 | 0 | 3.90682 | -0.00269924 | 6.90783 | 14.6284 |
| 121 | 2026-04-01 | ONGC | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3200 | 0 | -0 | -14.6561 | 0 | 1 | -0 | -0 | 3.92534 | -0.0181033 | 46.2853 | 14.6561 |
| 121 | 2026-04-01 | ONGC | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | 0 | -14.6687 | 0 | 1 | 0 | 0 | 3.93372 | 0.023708 | 59.9939 | 14.6687 |
| 121 | 2026-04-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3200 | 0 | 0 | -14.6561 | 0 | 1 | 0 | 0 | 3.92534 | -0.0181033 | 46.2853 | 14.6561 |
| 121 | 2026-04-01 | ONGC | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2250 | 0 | -0 | -14.6687 | 0 | 1 | -0 | -0 | 3.93372 | 0.023708 | 59.9939 | 14.6687 |
| 122 | 2026-04-01 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -13.2403 | 0 | 1 | 0 | 0 | 2.98146 | -0.00212519 | 7.1331 | 13.2403 |
| 122 | 2026-04-01 | RELIANCE | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | 0 | -13.2907 | 0 | 1 | 0 | 0 | 3.01504 | 0.00208037 | 6.90201 | 13.2907 |
| 122 | 2026-04-01 | RELIANCE | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -13.2403 | 0 | 1 | -0 | -0 | 2.98146 | -0.00212519 | 7.1331 | 13.2403 |
| 122 | 2026-04-01 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 300 | 0 | -0 | -13.2907 | 0 | 1 | -0 | -0 | 3.01504 | 0.00208037 | 6.90201 | 13.2907 |
| 122 | 2026-04-01 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2850 | 0 | 0 | -13.2471 | 0 | 1 | 0 | 0 | 2.98596 | -0.0164342 | 55.1379 | 13.2471 |
| 122 | 2026-04-01 | RELIANCE | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2850 | 0 | -0 | -13.2471 | 0 | 1 | -0 | -0 | 2.98596 | -0.0164342 | 55.1379 | 13.2471 |
| 122 | 2026-04-01 | RELIANCE | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2450 | 0 | 0 | -13.2655 | 0 | 1 | 0 | 0 | 2.99827 | 0.0180108 | 59.7571 | 13.2655 |
| 122 | 2026-04-01 | RELIANCE | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2450 | 0 | -0 | -13.2655 | 0 | 1 | -0 | -0 | 2.99827 | 0.0180108 | 59.7571 | 13.2655 |
| 123 | 2026-04-01 | SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -14.3365 | 0 | 1 | 0 | 0 | 3.71225 | 0.00144815 | 3.89845 | 14.3365 |
| 123 | 2026-04-01 | SBIN | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | -0 | -14.3185 | 0 | 1 | -0 | -0 | 3.70028 | -0.00342618 | 9.25926 | 14.3185 |
| 123 | 2026-04-01 | SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2450 | 0 | 0 | -14.3802 | 0 | 1 | 0 | 0 | 3.74138 | 0.0218592 | 58.2317 | 14.3802 |
| 123 | 2026-04-01 | SBIN | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -14.3911 | 0 | 1 | 0 | 0 | 3.74866 | 0.00236884 | 6.32043 | 14.3911 |
| 123 | 2026-04-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2900 | 0 | 0 | -14.3666 | 0 | 1 | 0 | 0 | 3.73229 | -0.019869 | 53.5661 | 14.3666 |
| 123 | 2026-04-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -14.3911 | 0 | 1 | -0 | -0 | 3.74866 | 0.00236884 | 6.32043 | 14.3911 |
| 123 | 2026-04-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2450 | 0 | -0 | -14.3802 | 0 | 1 | -0 | -0 | 3.74138 | 0.0218592 | 58.2317 | 14.3802 |
| 123 | 2026-04-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 100 | 0 | 0 | -14.3185 | 0 | 1 | 0 | 0 | 3.70028 | -0.00342618 | 9.25926 | 14.3185 |
| 123 | 2026-04-01 | SBIN | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2900 | 0 | -0 | -14.3666 | 0 | 1 | -0 | -0 | 3.73229 | -0.019869 | 53.5661 | 14.3666 |
| 123 | 2026-04-01 | SBIN | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -14.3365 | 0 | 1 | -0 | -0 | 3.71225 | 0.00144815 | 3.89845 | 14.3365 |
| 124 | 2026-04-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -14.8396 | 0 | 1 | 0 | 0 | 4.04767 | 0.00133104 | 3.28802 | 14.8396 |
| 124 | 2026-04-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -14.8396 | 0 | 1 | -0 | -0 | 4.04767 | 0.00133104 | 3.28802 | 14.8396 |
| 124 | 2026-04-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | -0 | -14.9169 | 0 | 1 | -0 | -0 | 4.09922 | -0.00168438 | 4.10491 | 14.9169 |
| 124 | 2026-04-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 200 | 0 | 0 | -14.9169 | 0 | 1 | 0 | 0 | 4.09922 | -0.00168438 | 4.10491 | 14.9169 |
| 124 | 2026-04-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | -0 | -14.8979 | 0 | 1 | -0 | -0 | 4.08655 | -0.0158259 | 38.8227 | 14.8979 |
| 124 | 2026-04-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | 0 | -14.9331 | 0 | 1 | 0 | 0 | 4.11 | 0.00293258 | 7.13534 | 14.9331 |
| 124 | 2026-04-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2750 | 0 | 0 | -14.8979 | 0 | 1 | 0 | 0 | 4.08655 | -0.0158259 | 38.8227 | 14.8979 |
| 124 | 2026-04-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 500 | 0 | -0 | -14.9331 | 0 | 1 | -0 | -0 | 4.11 | 0.00293258 | 7.13534 | 14.9331 |
| 124 | 2026-04-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -14.8905 | 0 | 1 | -0 | -0 | 4.08159 | -0.00313744 | 7.67278 | 14.8905 |
| 124 | 2026-04-01 | SUNPHARMA | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | 0 | -14.9226 | 0 | 1 | 0 | 0 | 4.103 | 0.0200999 | 48.9075 | 14.9226 |
| 124 | 2026-04-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -14.8905 | 0 | 1 | 0 | 0 | 4.08159 | -0.00313744 | 7.67278 | 14.8905 |
| 124 | 2026-04-01 | SUNPHARMA | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2050 | 0 | -0 | -14.9226 | 0 | 1 | -0 | -0 | 4.103 | 0.0200999 | 48.9075 | 14.9226 |
| 125 | 2026-04-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | 0 | -14.1607 | 0 | 1 | 0 | 0 | 3.59502 | -0.00291029 | 8.09535 | 14.1607 |
| 125 | 2026-04-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | -0 | -14.1702 | 0 | 1 | -0 | -0 | 3.60139 | 0.00248425 | 6.89796 | 14.1702 |
| 125 | 2026-04-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -14.1844 | 0 | 1 | 0 | 0 | 3.61082 | -0.00152218 | 4.21501 | 14.1844 |
| 125 | 2026-04-01 | TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -14.1844 | 0 | 1 | -0 | -0 | 3.61082 | -0.00152218 | 4.21501 | 14.1844 |
| 125 | 2026-04-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -14.1741 | 0 | 1 | -0 | -0 | 3.60399 | 0.0230234 | 63.813 | 14.1741 |
| 125 | 2026-04-01 | TCS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 150 | 0 | 0 | -14.1702 | 0 | 1 | 0 | 0 | 3.60139 | 0.00248425 | 6.89796 | 14.1702 |
| 125 | 2026-04-01 | TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | -0 | -14.1607 | 0 | 1 | -0 | -0 | 3.59502 | -0.00291029 | 8.09535 | 14.1607 |
| 125 | 2026-04-01 | TCS | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3050 | 0 | 0 | -14.1497 | 0 | 1 | 0 | 0 | 3.58775 | -0.0155669 | 43.5552 | 14.1497 |
| 125 | 2026-04-01 | TCS | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3050 | 0 | -0 | -14.1497 | 0 | 1 | -0 | -0 | 3.58775 | -0.0155669 | 43.5552 | 14.1497 |
| 125 | 2026-04-01 | TCS | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -14.1741 | 0 | 1 | 0 | 0 | 3.60399 | 0.0230234 | 63.813 | 14.1741 |
| 126 | 2026-04-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -16.5918 | 0 | 1 | -0 | -0 | 5.2158 | 0.00237932 | 4.56175 | 16.5918 |
| 126 | 2026-04-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | -0 | -16.6015 | 0 | 1 | -0 | -0 | 5.22228 | 0.028726 | 54.8586 | 16.6015 |
| 126 | 2026-04-01 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -16.5643 | 0 | 1 | 0 | 0 | 5.19745 | 0.00405269 | 7.79356 | 16.5643 |
| 126 | 2026-04-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -16.4872 | 0 | 1 | 0 | 0 | 5.14604 | -0.00182343 | 3.5413 | 16.4872 |
| 126 | 2026-04-01 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | -0 | -16.6251 | 0 | 1 | -0 | -0 | 5.238 | -0.00514943 | 9.83091 | 16.6251 |
| 126 | 2026-04-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 3100 | 0 | 0 | -16.5739 | 0 | 1 | 0 | 0 | 5.20388 | -0.0216456 | 41.6625 | 16.5739 |
| 126 | 2026-04-01 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 3100 | 0 | -0 | -16.5739 | 0 | 1 | -0 | -0 | 5.20388 | -0.0216456 | 41.6625 | 16.5739 |
| 126 | 2026-04-01 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -16.5918 | 0 | 1 | 0 | 0 | 5.2158 | 0.00237932 | 4.56175 | 16.5918 |
| 126 | 2026-04-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | 0 | -16.6251 | 0 | 1 | 0 | 0 | 5.238 | -0.00514943 | 9.83091 | 16.6251 |
| 126 | 2026-04-01 | TECHM | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -16.5643 | 0 | 1 | -0 | -0 | 5.19745 | 0.00405269 | 7.79356 | 16.5643 |
| 126 | 2026-04-01 | TECHM | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2150 | 0 | 0 | -16.6015 | 0 | 1 | 0 | 0 | 5.22228 | 0.028726 | 54.8586 | 16.6015 |
| 126 | 2026-04-01 | TECHM | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -16.4872 | 0 | 1 | -0 | -0 | 5.14604 | -0.00182343 | 3.5413 | 16.4872 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 400 | 0 | 0 | -16.1922 | 0 | 1 | 0 | 0 | 4.94942 | 0.0194319 | 39.2782 | 16.1922 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R01_0p25_2p5bp | 50 | 0 | 0 | -16.2588 | 0 | 1 | 0 | 0 | 4.99376 | -0.00124719 | 2.4975 | 16.2588 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | 0 | -16.167 | 0 | 1 | 0 | 0 | 4.93259 | -0.00405841 | 8.22774 | 16.167 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -16.3354 | 0 | 1 | 0 | 0 | 5.04487 | 0.00265188 | 5.25433 | 16.3354 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R01_0p25_2p5bp | 50 | 0 | -0 | -16.2588 | 0 | 1 | -0 | -0 | 4.99376 | -0.00124719 | 2.4975 | 16.2588 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 50 | 0 | -0 | -16.167 | 0 | 1 | -0 | -0 | 4.93259 | -0.00405841 | 8.22774 | 16.167 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | -0 | -16.3427 | 0 | 1 | -0 | -0 | 5.0497 | 0.00184344 | 3.64806 | 16.3427 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 700 | 0 | 0 | -16.2017 | 0 | 1 | 0 | 0 | 4.95575 | -0.0470238 | 95.4941 | 16.2017 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | 0 | -16.354 | 0 | 1 | 0 | 0 | 5.05725 | 0.0346334 | 68.1787 | 16.354 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 700 | 0 | -0 | -16.2017 | 0 | 1 | -0 | -0 | 4.95575 | -0.0470238 | 95.4941 | 16.2017 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -16.3463 | 0 | 1 | 0 | 0 | 5.05213 | -0.0187935 | 37.1852 | 16.3463 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -16.3354 | 0 | 1 | -0 | -0 | 5.04487 | 0.00265188 | 5.25433 | 16.3354 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -16.321 | 0 | 1 | -0 | -0 | 5.03528 | -0.00360497 | 7.14904 | 16.321 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 400 | 0 | -0 | -16.1922 | 0 | 1 | -0 | -0 | 4.94942 | 0.0194319 | 39.2782 | 16.1922 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 1700 | 0 | -0 | -16.354 | 0 | 1 | -0 | -0 | 5.05725 | 0.0346334 | 68.1787 | 16.354 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S04_gt_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -16.321 | 0 | 1 | 0 | 0 | 5.03528 | -0.00360497 | 7.14904 | 16.321 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | 0 | -16.2339 | 0 | 1 | 0 | 0 | 4.97719 | -0.00247847 | 4.97967 | 16.2339 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S04_gt_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -16.3463 | 0 | 1 | -0 | -0 | 5.05213 | -0.0187935 | 37.1852 | 16.3463 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 100 | 0 | -0 | -16.2339 | 0 | 1 | -0 | -0 | 4.97719 | -0.00247847 | 4.97967 | 16.2339 |
| 127 | 2026-04-01 | ULTRACEMCO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S04_gt_5bp | C01_lt_1bp | R02_2p5_5bp | 150 | 0 | 0 | -16.3427 | 0 | 1 | 0 | 0 | 5.0497 | 0.00184344 | 3.64806 | 16.3427 |
| 128 | 2026-04-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | -0 | -14.5969 | 0 | 1 | -0 | -0 | 3.88587 | -0.00194239 | 4.99861 | 14.5969 |
| 128 | 2026-04-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3150 | 0 | -0 | -14.5509 | 0 | 1 | -0 | -0 | 3.85521 | -0.0174044 | 45.378 | 14.5509 |
| 128 | 2026-04-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | 0 | -14.5415 | 0 | 1 | 0 | 0 | 3.84892 | 0.00285921 | 7.42243 | 14.5415 |
| 128 | 2026-04-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | compression | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | -0 | -14.5699 | 0 | 1 | -0 | -0 | 3.86786 | -0.00253532 | 6.55533 | 14.5699 |
| 128 | 2026-04-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 350 | 0 | 0 | -14.5699 | 0 | 1 | 0 | 0 | 3.86786 | -0.00253532 | 6.55533 | 14.5699 |
| 128 | 2026-04-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R03_5_10bp | 200 | 0 | -0 | -14.5415 | 0 | 1 | -0 | -0 | 3.84892 | 0.00285921 | 7.42243 | 14.5415 |
| 128 | 2026-04-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | 0 | -14.5446 | 0 | 1 | 0 | 0 | 3.85097 | 0.00140284 | 3.63603 | 14.5446 |
| 128 | 2026-04-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 3150 | 0 | 0 | -14.5509 | 0 | 1 | 0 | 0 | 3.85521 | -0.0174044 | 45.378 | 14.5509 |
| 128 | 2026-04-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | -0 | -14.5838 | 0 | 1 | -0 | -0 | 3.87711 | 0.0263339 | 67.821 | 14.5838 |
| 128 | 2026-04-01 | WIPRO | P69_SPREAD_TRANSITION_FADE | expansion | 1 | S03_2p5_5bp | C01_lt_1bp | R04_ge_10bp | 2000 | 0 | 0 | -14.5838 | 0 | 1 | 0 | 0 | 3.87711 | 0.0263339 | 67.821 | 14.5838 |
| 128 | 2026-04-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | expansion | -1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 250 | 0 | -0 | -14.5446 | 0 | 1 | -0 | -0 | 3.85097 | 0.00140284 | 3.63603 | 14.5446 |
| 128 | 2026-04-01 | WIPRO | P69_SPREAD_TRANSITION_MOMENTUM | compression | 1 | S03_2p5_5bp | C01_lt_1bp | R02_2p5_5bp | 50 | 0 | 0 | -14.5969 | 0 | 1 | 0 | 0 | 3.88587 | -0.00194239 | 4.99861 | 14.5969 |

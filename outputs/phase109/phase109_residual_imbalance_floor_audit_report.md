# Phase103 Calibrated Realism Rerun

Generated UTC: 2026-07-19T22:34:43.688898+00:00

Phase103 compares the patched calibrated dense synthetic shard against the available real Zerodha WebSocket anchor.
This is a one-symbol calibrated readout, not permission to reopen strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase103_profile_id | P109_SYMBOL_AWARE_RESIDUAL_IMBALANCE_FLOOR | Calibrated synthetic profile audited |
| phase103_real_symbols_profiled | 32 | Real WebSocket symbols profiled |
| phase103_synthetic_symbols_profiled | 32 | Synthetic dense symbols profiled |
| phase103_compared_symbols | 32 | Symbols present in both real and synthetic profiles |
| phase103_symbol_metric_anchor_rows | 256 | Symbol/metric calibration anchors compared |
| phase103_calibration_gap_rows | 0 | Anchor rows outside ratio gates |
| phase103_calibration_gap_fraction | 0 | Fraction of compared symbol/metric anchors outside gates |
| phase103_severe_metric_gap_count | 0 | Metrics where more than half of symbols fail calibration gates |
| phase103_calibrated_realism_patch_pass | 1 | 1 means patched calibrated HDFCBANK shard passes one-symbol realism readout |
| phase103_strategy_replay_allowed | 0 | Strategy replay remains closed until multiday and broader-symbol realism gates pass |
| phase103_recommend_next_action | expand_calibrated_realism_rerun_to_32_symbols_or_collect_multiday_real_panel | Recommended next milestone |

## Calibration Gap Summary

| category | metric | symbol_metrics | gap_count | gap_fraction | median_synthetic_to_real_ratio | min_synthetic_to_real_ratio | max_synthetic_to_real_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L1 imbalance scale | median_abs_l1_imbalance | 32 | 0 | 0 | 0.634204 | 0.270734 | 1.7549 |
| displayed L1 depth scale | median_l1_depth | 32 | 0 | 0 | 1.35896 | 0.271336 | 7.09735 |
| displayed L5 depth scale | median_l5_depth | 32 | 0 | 0 | 0.998932 | 0.132923 | 6.91278 |
| median spread scale | median_spread_bps | 32 | 0 | 0 | 1.00498 | 0.751177 | 1.99958 |
| one-tick volatility scale | one_tick_return_std | 32 | 0 | 0 | 0.265841 | 0.121734 | 0.596925 |
| received tick cadence | median_gap_ms | 32 | 0 | 0 | 0.666667 | 0.23359 | 1.002 |
| tail received tick cadence | p90_gap_ms | 32 | 0 | 0 | 1 | 0.200046 | 1.00009 |
| tail spread scale | p90_spread_bps | 32 | 0 | 0 | 1.13643 | 0.985194 | 1.35755 |

## Real vs Calibrated Synthetic Comparison

| symbol | category | metric | real_value | synthetic_value | synthetic_to_real_ratio | lower_ratio_gate | upper_ratio_gate | calibration_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | received tick cadence | median_gap_ms | 1000 | 500 | 0.5 | 0.2 | 5 | False |
| ADANIPORTS | tail received tick cadence | p90_gap_ms | 439477 | 439477 | 1 | 0.2 | 5 | False |
| ADANIPORTS | median spread scale | median_spread_bps | 2.20726 | 2.21299 | 1.00259 | 0.25 | 4 | False |
| ADANIPORTS | tail spread scale | p90_spread_bps | 3.85933 | 4.40101 | 1.14036 | 0.25 | 4 | False |
| ADANIPORTS | displayed L1 depth scale | median_l1_depth | 131 | 806 | 6.15267 | 0.1 | 10 | False |
| ADANIPORTS | displayed L5 depth scale | median_l5_depth | 1088 | 6851 | 6.29688 | 0.1 | 10 | False |
| ADANIPORTS | L1 imbalance scale | median_abs_l1_imbalance | 0.62963 | 0.212851 | 0.338058 | 0.25 | 4 | False |
| ADANIPORTS | one-tick volatility scale | one_tick_return_std | 0.000441155 | 0.0001296 | 0.293773 | 0.1 | 10 | False |
| AXISBANK | received tick cadence | median_gap_ms | 750 | 500 | 0.666667 | 0.2 | 5 | False |
| AXISBANK | tail received tick cadence | p90_gap_ms | 305453 | 305453 | 1 | 0.2 | 5 | False |
| AXISBANK | median spread scale | median_spread_bps | 1.51435 | 1.51669 | 1.00155 | 0.25 | 4 | False |
| AXISBANK | tail spread scale | p90_spread_bps | 3.02595 | 3.76405 | 1.24392 | 0.25 | 4 | False |
| AXISBANK | displayed L1 depth scale | median_l1_depth | 249 | 808 | 3.24498 | 0.1 | 10 | False |
| AXISBANK | displayed L5 depth scale | median_l5_depth | 3048 | 6870 | 2.25394 | 0.1 | 10 | False |
| AXISBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.549598 | 0.35 | 0.636829 | 0.25 | 4 | False |
| AXISBANK | one-tick volatility scale | one_tick_return_std | 0.000423171 | 0.000121026 | 0.285997 | 0.1 | 10 | False |
| BAJAJ-AUTO | received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.2 | 5 | False |
| BAJAJ-AUTO | tail received tick cadence | p90_gap_ms | 1250 | 692 | 0.5536 | 0.2 | 5 | False |
| BAJAJ-AUTO | median spread scale | median_spread_bps | 2.46627 | 3.34493 | 1.35627 | 0.25 | 4 | False |
| BAJAJ-AUTO | tail spread scale | p90_spread_bps | 4.37443 | 4.89536 | 1.11908 | 0.25 | 4 | False |
| BAJAJ-AUTO | displayed L1 depth scale | median_l1_depth | 61 | 52 | 0.852459 | 0.1 | 10 | False |
| BAJAJ-AUTO | displayed L5 depth scale | median_l5_depth | 366 | 443 | 1.21038 | 0.1 | 10 | False |
| BAJAJ-AUTO | L1 imbalance scale | median_abs_l1_imbalance | 0.578947 | 0.95122 | 1.64302 | 0.25 | 4 | False |
| BAJAJ-AUTO | one-tick volatility scale | one_tick_return_std | 0.00071201 | 0.000121237 | 0.170274 | 0.1 | 10 | False |
| BANKBEES | received tick cadence | median_gap_ms | 1000 | 500 | 0.5 | 0.2 | 5 | False |
| BANKBEES | tail received tick cadence | p90_gap_ms | 2351.6 | 692 | 0.294268 | 0.2 | 5 | False |
| BANKBEES | median spread scale | median_spread_bps | 3.33389 | 3.823 | 1.14671 | 0.25 | 4 | False |
| BANKBEES | tail spread scale | p90_spread_bps | 5.65504 | 5.86178 | 1.03656 | 0.25 | 4 | False |
| BANKBEES | displayed L1 depth scale | median_l1_depth | 403 | 800 | 1.98511 | 0.1 | 10 | False |
| BANKBEES | displayed L5 depth scale | median_l5_depth | 5262 | 6800 | 1.29228 | 0.1 | 10 | False |
| BANKBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.808031 | 0.327922 | 0.405829 | 0.25 | 4 | False |
| BANKBEES | one-tick volatility scale | one_tick_return_std | 0.000217665 | 0.000105674 | 0.485491 | 0.1 | 10 | False |
| BHARTIARTL | received tick cadence | median_gap_ms | 750 | 500 | 0.666667 | 0.2 | 5 | False |
| BHARTIARTL | tail received tick cadence | p90_gap_ms | 3949.1 | 3949 | 0.999975 | 0.2 | 5 | False |
| BHARTIARTL | median spread scale | median_spread_bps | 2.09293 | 1.57693 | 0.753459 | 0.25 | 4 | False |
| BHARTIARTL | tail spread scale | p90_spread_bps | 3.15637 | 3.65759 | 1.1588 | 0.25 | 4 | False |
| BHARTIARTL | displayed L1 depth scale | median_l1_depth | 415 | 806 | 1.94217 | 0.1 | 10 | False |
| BHARTIARTL | displayed L5 depth scale | median_l5_depth | 3715 | 6851 | 1.84415 | 0.1 | 10 | False |
| BHARTIARTL | L1 imbalance scale | median_abs_l1_imbalance | 0.547826 | 0.350282 | 0.639405 | 0.25 | 4 | False |
| BHARTIARTL | one-tick volatility scale | one_tick_return_std | 0.00043748 | 0.000120189 | 0.274729 | 0.1 | 10 | False |
| BPCL | received tick cadence | median_gap_ms | 1750 | 500 | 0.285714 | 0.2 | 5 | False |
| BPCL | tail received tick cadence | p90_gap_ms | 448824 | 448824 | 1 | 0.2 | 5 | False |
| BPCL | median spread scale | median_spread_bps | 1.63921 | 1.63584 | 0.997947 | 0.25 | 4 | False |
| BPCL | tail spread scale | p90_spread_bps | 4.89996 | 4.88996 | 0.997959 | 0.25 | 4 | False |
| BPCL | displayed L1 depth scale | median_l1_depth | 2059 | 810 | 0.393395 | 0.1 | 10 | False |
| BPCL | displayed L5 depth scale | median_l5_depth | 19762 | 6885 | 0.348396 | 0.1 | 10 | False |
| BPCL | L1 imbalance scale | median_abs_l1_imbalance | 0.653486 | 0.35 | 0.535589 | 0.25 | 4 | False |
| BPCL | one-tick volatility scale | one_tick_return_std | 0.000615309 | 0.000129686 | 0.210766 | 0.1 | 10 | False |
| BRITANNIA | received tick cadence | median_gap_ms | 1750 | 500 | 0.285714 | 0.2 | 5 | False |
| BRITANNIA | tail received tick cadence | p90_gap_ms | 450023 | 450023 | 1 | 0.2 | 5 | False |
| BRITANNIA | median spread scale | median_spread_bps | 2.81756 | 3.74625 | 1.32961 | 0.25 | 4 | False |
| BRITANNIA | tail spread scale | p90_spread_bps | 5.59754 | 5.63021 | 1.00584 | 0.25 | 4 | False |
| BRITANNIA | displayed L1 depth scale | median_l1_depth | 35 | 42 | 1.2 | 0.1 | 10 | False |
| BRITANNIA | displayed L5 depth scale | median_l5_depth | 406.5 | 352 | 0.865929 | 0.1 | 10 | False |
| BRITANNIA | L1 imbalance scale | median_abs_l1_imbalance | 0.542036 | 0.95122 | 1.7549 | 0.25 | 4 | False |
| BRITANNIA | one-tick volatility scale | one_tick_return_std | 0.00049004 | 0.000103935 | 0.212096 | 0.1 | 10 | False |
| CIPLA | received tick cadence | median_gap_ms | 1500 | 500 | 0.333333 | 0.2 | 5 | False |
| CIPLA | tail received tick cadence | p90_gap_ms | 447132 | 447132 | 1 | 0.2 | 5 | False |
| CIPLA | median spread scale | median_spread_bps | 2.80387 | 2.81009 | 1.00222 | 0.25 | 4 | False |
| CIPLA | tail spread scale | p90_spread_bps | 4.90069 | 4.92208 | 1.00436 | 0.25 | 4 | False |
| CIPLA | displayed L1 depth scale | median_l1_depth | 136 | 802 | 5.89706 | 0.1 | 10 | False |
| CIPLA | displayed L5 depth scale | median_l5_depth | 1594 | 6816 | 4.27604 | 0.1 | 10 | False |
| CIPLA | L1 imbalance scale | median_abs_l1_imbalance | 0.675676 | 0.568528 | 0.841421 | 0.25 | 4 | False |
| CIPLA | one-tick volatility scale | one_tick_return_std | 0.000439541 | 0.000103891 | 0.236361 | 0.1 | 10 | False |
| DRREDDY | received tick cadence | median_gap_ms | 1749 | 500 | 0.285878 | 0.2 | 5 | False |
| DRREDDY | tail received tick cadence | p90_gap_ms | 446827 | 446827 | 1 | 0.2 | 5 | False |
| DRREDDY | median spread scale | median_spread_bps | 3.24649 | 2.43869 | 0.751177 | 0.25 | 4 | False |
| DRREDDY | tail spread scale | p90_spread_bps | 4.86934 | 4.86512 | 0.999134 | 0.25 | 4 | False |
| DRREDDY | displayed L1 depth scale | median_l1_depth | 271.5 | 802 | 2.95396 | 0.1 | 10 | False |
| DRREDDY | displayed L5 depth scale | median_l5_depth | 2642 | 6816 | 2.57986 | 0.1 | 10 | False |
| DRREDDY | L1 imbalance scale | median_abs_l1_imbalance | 0.618831 | 0.207254 | 0.334912 | 0.25 | 4 | False |
| DRREDDY | one-tick volatility scale | one_tick_return_std | 0.000542243 | 0.000100334 | 0.185036 | 0.1 | 10 | False |
| GOLDBEES | received tick cadence | median_gap_ms | 1000 | 500 | 0.5 | 0.2 | 5 | False |
| GOLDBEES | tail received tick cadence | p90_gap_ms | 439314 | 439314 | 1 | 0.2 | 5 | False |
| GOLDBEES | median spread scale | median_spread_bps | 0.857082 | 0.856267 | 0.99905 | 0.25 | 4 | False |
| GOLDBEES | tail spread scale | p90_spread_bps | 2.56487 | 2.55598 | 0.996532 | 0.25 | 4 | False |
| GOLDBEES | displayed L1 depth scale | median_l1_depth | 11211.5 | 11235 | 1.0021 | 0.1 | 10 | False |
| GOLDBEES | displayed L5 depth scale | median_l5_depth | 95705.5 | 95501 | 0.997863 | 0.1 | 10 | False |
| GOLDBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.747425 | 0.202353 | 0.270734 | 0.25 | 4 | False |
| GOLDBEES | one-tick volatility scale | one_tick_return_std | 0.000285098 | 0.000103335 | 0.362454 | 0.1 | 10 | False |
| HCLTECH | received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.2 | 5 | False |
| HCLTECH | tail received tick cadence | p90_gap_ms | 1214.8 | 692 | 0.569641 | 0.2 | 5 | False |
| HCLTECH | median spread scale | median_spread_bps | 3.25574 | 2.4614 | 0.75602 | 0.25 | 4 | False |
| HCLTECH | tail spread scale | p90_spread_bps | 4.26218 | 4.88698 | 1.14659 | 0.25 | 4 | False |
| HCLTECH | displayed L1 depth scale | median_l1_depth | 339.5 | 810 | 2.38586 | 0.1 | 10 | False |
| HCLTECH | displayed L5 depth scale | median_l5_depth | 4819 | 6885 | 1.42872 | 0.1 | 10 | False |
| HCLTECH | L1 imbalance scale | median_abs_l1_imbalance | 0.660606 | 0.293963 | 0.44499 | 0.25 | 4 | False |
| HCLTECH | one-tick volatility scale | one_tick_return_std | 0.000923066 | 0.000125175 | 0.135608 | 0.1 | 10 | False |
| HDFCBANK | received tick cadence | median_gap_ms | 499 | 500 | 1.002 | 0.2 | 5 | False |
| HDFCBANK | tail received tick cadence | p90_gap_ms | 1000 | 692 | 0.692 | 0.2 | 5 | False |
| HDFCBANK | median spread scale | median_spread_bps | 1.22048 | 1.22299 | 1.00206 | 0.25 | 4 | False |
| HDFCBANK | tail spread scale | p90_spread_bps | 2.45085 | 3.03719 | 1.23924 | 0.25 | 4 | False |
| HDFCBANK | displayed L1 depth scale | median_l1_depth | 1010 | 808 | 0.8 | 0.1 | 10 | False |
| HDFCBANK | displayed L5 depth scale | median_l5_depth | 15104 | 6868 | 0.454714 | 0.1 | 10 | False |
| HDFCBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.622123 | 0.572368 | 0.920024 | 0.25 | 4 | False |
| HDFCBANK | one-tick volatility scale | one_tick_return_std | 0.000266132 | 0.000121544 | 0.456707 | 0.1 | 10 | False |
| HINDUNILVR | received tick cadence | median_gap_ms | 1000 | 500 | 0.5 | 0.2 | 5 | False |
| HINDUNILVR | tail received tick cadence | p90_gap_ms | 442440 | 442440 | 1 | 0.2 | 5 | False |
| HINDUNILVR | median spread scale | median_spread_bps | 1.4103 | 1.88454 | 1.33626 | 0.25 | 4 | False |
| HINDUNILVR | tail spread scale | p90_spread_bps | 3.52032 | 4.20642 | 1.1949 | 0.25 | 4 | False |
| HINDUNILVR | displayed L1 depth scale | median_l1_depth | 188.5 | 802 | 4.25464 | 0.1 | 10 | False |
| HINDUNILVR | displayed L5 depth scale | median_l5_depth | 1287 | 6816 | 5.29604 | 0.1 | 10 | False |
| HINDUNILVR | L1 imbalance scale | median_abs_l1_imbalance | 0.627765 | 0.35 | 0.557533 | 0.25 | 4 | False |
| HINDUNILVR | one-tick volatility scale | one_tick_return_std | 0.000449187 | 0.000105665 | 0.235235 | 0.1 | 10 | False |
| ICICIBANK | received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.2 | 5 | False |
| ICICIBANK | tail received tick cadence | p90_gap_ms | 2000 | 692 | 0.346 | 0.2 | 5 | False |
| ICICIBANK | median spread scale | median_spread_bps | 1.41784 | 1.42577 | 1.0056 | 0.25 | 4 | False |
| ICICIBANK | tail spread scale | p90_spread_bps | 2.84353 | 3.53903 | 1.24459 | 0.25 | 4 | False |
| ICICIBANK | displayed L1 depth scale | median_l1_depth | 580 | 810 | 1.39655 | 0.1 | 10 | False |
| ICICIBANK | displayed L5 depth scale | median_l5_depth | 6394 | 6884 | 1.07663 | 0.1 | 10 | False |
| ICICIBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.618943 | 0.368771 | 0.595807 | 0.25 | 4 | False |
| ICICIBANK | one-tick volatility scale | one_tick_return_std | 0.00027235 | 0.000120141 | 0.441129 | 0.1 | 10 | False |
| INFY | received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.2 | 5 | False |
| INFY | tail received tick cadence | p90_gap_ms | 1000 | 692 | 0.692 | 0.2 | 5 | False |
| INFY | median spread scale | median_spread_bps | 1.81422 | 1.81598 | 1.00097 | 0.25 | 4 | False |
| INFY | tail spread scale | p90_spread_bps | 3.66367 | 4.50825 | 1.23053 | 0.25 | 4 | False |
| INFY | displayed L1 depth scale | median_l1_depth | 613 | 810 | 1.32137 | 0.1 | 10 | False |
| INFY | displayed L5 depth scale | median_l5_depth | 9352 | 6885 | 0.736206 | 0.1 | 10 | False |
| INFY | L1 imbalance scale | median_abs_l1_imbalance | 0.758157 | 0.75 | 0.989241 | 0.25 | 4 | False |
| INFY | one-tick volatility scale | one_tick_return_std | 0.00067843 | 0.000124183 | 0.183044 | 0.1 | 10 | False |
| ITBEES | received tick cadence | median_gap_ms | 1250 | 500 | 0.4 | 0.2 | 5 | False |
| ITBEES | tail received tick cadence | p90_gap_ms | 446258 | 446258 | 1 | 0.2 | 5 | False |
| ITBEES | median spread scale | median_spread_bps | 3.12794 | 3.11429 | 0.995637 | 0.25 | 4 | False |
| ITBEES | tail spread scale | p90_spread_bps | 6.29723 | 6.20399 | 0.985194 | 0.25 | 4 | False |
| ITBEES | displayed L1 depth scale | median_l1_depth | 134432 | 193832 | 1.44186 | 0.1 | 10 | False |
| ITBEES | displayed L5 depth scale | median_l5_depth | 2.15215e+06 | 1.64733e+06 | 0.765433 | 0.1 | 10 | False |
| ITBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.68474 | 0.740336 | 1.08119 | 0.25 | 4 | False |
| ITBEES | one-tick volatility scale | one_tick_return_std | 0.000841952 | 0.000102494 | 0.121734 | 0.1 | 10 | False |
| ITC | received tick cadence | median_gap_ms | 1254.5 | 500 | 0.398565 | 0.2 | 5 | False |
| ITC | tail received tick cadence | p90_gap_ms | 443821 | 443821 | 1 | 0.2 | 5 | False |
| ITC | median spread scale | median_spread_bps | 1.78715 | 1.78604 | 0.999377 | 0.25 | 4 | False |
| ITC | tail spread scale | p90_spread_bps | 3.92555 | 5.32912 | 1.35755 | 0.25 | 4 | False |
| ITC | displayed L1 depth scale | median_l1_depth | 5559 | 13371 | 2.40529 | 0.1 | 10 | False |
| ITC | displayed L5 depth scale | median_l5_depth | 113657 | 113657 | 1 | 0.1 | 10 | False |
| ITC | L1 imbalance scale | median_abs_l1_imbalance | 0.589392 | 0.509905 | 0.865137 | 0.25 | 4 | False |
| ITC | one-tick volatility scale | one_tick_return_std | 0.000353813 | 0.000105297 | 0.297606 | 0.1 | 10 | False |
| JUNIORBEES | received tick cadence | median_gap_ms | 999 | 500 | 0.500501 | 0.2 | 5 | False |
| JUNIORBEES | tail received tick cadence | p90_gap_ms | 4750 | 4750 | 1 | 0.2 | 5 | False |
| JUNIORBEES | median spread scale | median_spread_bps | 3.60078 | 3.9655 | 1.10129 | 0.25 | 4 | False |
| JUNIORBEES | tail spread scale | p90_spread_bps | 5.53578 | 6.03954 | 1.091 | 0.25 | 4 | False |
| JUNIORBEES | displayed L1 depth scale | median_l1_depth | 417 | 798 | 1.91367 | 0.1 | 10 | False |
| JUNIORBEES | displayed L5 depth scale | median_l5_depth | 8912 | 6784 | 0.761221 | 0.1 | 10 | False |
| JUNIORBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.863238 | 0.69774 | 0.808283 | 0.25 | 4 | False |
| JUNIORBEES | one-tick volatility scale | one_tick_return_std | 0.000210559 | 9.6082e-05 | 0.456319 | 0.1 | 10 | False |
| KOTAKBANK | received tick cadence | median_gap_ms | 750 | 500 | 0.666667 | 0.2 | 5 | False |
| KOTAKBANK | tail received tick cadence | p90_gap_ms | 6375 | 6375 | 1 | 0.2 | 5 | False |
| KOTAKBANK | median spread scale | median_spread_bps | 2.62329 | 2.63624 | 1.00493 | 0.25 | 4 | False |
| KOTAKBANK | tail spread scale | p90_spread_bps | 3.96432 | 4.03352 | 1.01745 | 0.25 | 4 | False |
| KOTAKBANK | displayed L1 depth scale | median_l1_depth | 1719 | 808 | 0.470041 | 0.1 | 10 | False |
| KOTAKBANK | displayed L5 depth scale | median_l5_depth | 25525 | 6870 | 0.269148 | 0.1 | 10 | False |
| KOTAKBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.670857 | 0.602273 | 0.897766 | 0.25 | 4 | False |
| KOTAKBANK | one-tick volatility scale | one_tick_return_std | 0.000438758 | 0.00012056 | 0.274776 | 0.1 | 10 | False |
| LT | received tick cadence | median_gap_ms | 749 | 500 | 0.667557 | 0.2 | 5 | False |
| LT | tail received tick cadence | p90_gap_ms | 3750.7 | 3751 | 1.00008 | 0.2 | 5 | False |
| LT | median spread scale | median_spread_bps | 1.27755 | 1.50341 | 1.17679 | 0.25 | 4 | False |
| LT | tail spread scale | p90_spread_bps | 2.8018 | 3.54682 | 1.26591 | 0.25 | 4 | False |
| LT | displayed L1 depth scale | median_l1_depth | 106 | 56 | 0.528302 | 0.1 | 10 | False |
| LT | displayed L5 depth scale | median_l5_depth | 481 | 481 | 1 | 0.1 | 10 | False |
| LT | L1 imbalance scale | median_abs_l1_imbalance | 0.549296 | 0.457143 | 0.832234 | 0.25 | 4 | False |
| LT | one-tick volatility scale | one_tick_return_std | 0.000333916 | 0.000114174 | 0.341925 | 0.1 | 10 | False |
| M&M | received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.2 | 5 | False |
| M&M | tail received tick cadence | p90_gap_ms | 1250 | 692 | 0.5536 | 0.2 | 5 | False |
| M&M | median spread scale | median_spread_bps | 1.26723 | 1.27467 | 1.00587 | 0.25 | 4 | False |
| M&M | tail spread scale | p90_spread_bps | 2.86439 | 3.46674 | 1.21029 | 0.25 | 4 | False |
| M&M | displayed L1 depth scale | median_l1_depth | 47 | 50 | 1.06383 | 0.1 | 10 | False |
| M&M | displayed L5 depth scale | median_l5_depth | 447 | 424 | 0.948546 | 0.1 | 10 | False |
| M&M | L1 imbalance scale | median_abs_l1_imbalance | 0.676548 | 0.189189 | 0.279639 | 0.25 | 4 | False |
| M&M | one-tick volatility scale | one_tick_return_std | 0.000420129 | 0.000112336 | 0.267384 | 0.1 | 10 | False |
| MARUTI | received tick cadence | median_gap_ms | 749 | 500 | 0.667557 | 0.2 | 5 | False |
| MARUTI | tail received tick cadence | p90_gap_ms | 1250 | 692 | 0.5536 | 0.2 | 5 | False |
| MARUTI | median spread scale | median_spread_bps | 2.91153 | 2.93049 | 1.00651 | 0.25 | 4 | False |
| MARUTI | tail spread scale | p90_spread_bps | 4.36205 | 4.36944 | 1.00169 | 0.25 | 4 | False |
| MARUTI | displayed L1 depth scale | median_l1_depth | 40 | 44 | 1.1 | 0.1 | 10 | False |
| MARUTI | displayed L5 depth scale | median_l5_depth | 411 | 375 | 0.912409 | 0.1 | 10 | False |
| MARUTI | L1 imbalance scale | median_abs_l1_imbalance | 0.592949 | 0.5 | 0.843243 | 0.25 | 4 | False |
| MARUTI | one-tick volatility scale | one_tick_return_std | 0.000428897 | 0.000111125 | 0.259095 | 0.1 | 10 | False |
| NESTLEIND | received tick cadence | median_gap_ms | 1000 | 500 | 0.5 | 0.2 | 5 | False |
| NESTLEIND | tail received tick cadence | p90_gap_ms | 443604 | 443604 | 1 | 0.2 | 5 | False |
| NESTLEIND | median spread scale | median_spread_bps | 2.44069 | 2.79654 | 1.1458 | 0.25 | 4 | False |
| NESTLEIND | tail spread scale | p90_spread_bps | 4.18819 | 4.87753 | 1.16459 | 0.25 | 4 | False |
| NESTLEIND | displayed L1 depth scale | median_l1_depth | 349 | 802 | 2.29799 | 0.1 | 10 | False |
| NESTLEIND | displayed L5 depth scale | median_l5_depth | 2850 | 6817 | 2.39193 | 0.1 | 10 | False |
| NESTLEIND | L1 imbalance scale | median_abs_l1_imbalance | 0.619048 | 0.41196 | 0.665474 | 0.25 | 4 | False |
| NESTLEIND | one-tick volatility scale | one_tick_return_std | 0.000651157 | 0.000100298 | 0.15403 | 0.1 | 10 | False |
| NIFTYBEES | received tick cadence | median_gap_ms | 501 | 500 | 0.998004 | 0.2 | 5 | False |
| NIFTYBEES | tail received tick cadence | p90_gap_ms | 2320.2 | 692 | 0.29825 | 0.2 | 5 | False |
| NIFTYBEES | median spread scale | median_spread_bps | 1.45757 | 1.45886 | 1.00089 | 0.25 | 4 | False |
| NIFTYBEES | tail spread scale | p90_spread_bps | 3.6412 | 3.62565 | 0.99573 | 0.25 | 4 | False |
| NIFTYBEES | displayed L1 depth scale | median_l1_depth | 2941 | 798 | 0.271336 | 0.1 | 10 | False |
| NIFTYBEES | displayed L5 depth scale | median_l5_depth | 51029.5 | 6783 | 0.132923 | 0.1 | 10 | False |
| NIFTYBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.803454 | 0.620915 | 0.772807 | 0.25 | 4 | False |
| NIFTYBEES | one-tick volatility scale | one_tick_return_std | 0.00014983 | 8.8358e-05 | 0.589721 | 0.1 | 10 | False |
| ONGC | received tick cadence | median_gap_ms | 749 | 500 | 0.667557 | 0.2 | 5 | False |
| ONGC | tail received tick cadence | p90_gap_ms | 4017 | 4017 | 1 | 0.2 | 5 | False |
| ONGC | median spread scale | median_spread_bps | 1.62121 | 2.3811 | 1.46872 | 0.25 | 4 | False |
| ONGC | tail spread scale | p90_spread_bps | 3.6357 | 4.02818 | 1.10795 | 0.25 | 4 | False |
| ONGC | displayed L1 depth scale | median_l1_depth | 1042 | 810 | 0.777351 | 0.1 | 10 | False |
| ONGC | displayed L5 depth scale | median_l5_depth | 7000.5 | 6884 | 0.983358 | 0.1 | 10 | False |
| ONGC | L1 imbalance scale | median_abs_l1_imbalance | 0.612081 | 0.35 | 0.57182 | 0.25 | 4 | False |
| ONGC | one-tick volatility scale | one_tick_return_std | 0.000511555 | 0.000122298 | 0.239072 | 0.1 | 10 | False |
| RELIANCE | received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.2 | 5 | False |
| RELIANCE | tail received tick cadence | p90_gap_ms | 2142.4 | 692 | 0.323002 | 0.2 | 5 | False |
| RELIANCE | median spread scale | median_spread_bps | 0.771159 | 1.542 | 1.99958 | 0.25 | 4 | False |
| RELIANCE | tail spread scale | p90_spread_bps | 3.07882 | 3.07289 | 0.998074 | 0.25 | 4 | False |
| RELIANCE | displayed L1 depth scale | median_l1_depth | 986 | 810 | 0.821501 | 0.1 | 10 | False |
| RELIANCE | displayed L5 depth scale | median_l5_depth | 11881.5 | 6885 | 0.579472 | 0.1 | 10 | False |
| RELIANCE | L1 imbalance scale | median_abs_l1_imbalance | 0.716704 | 0.44359 | 0.61893 | 0.25 | 4 | False |
| RELIANCE | one-tick volatility scale | one_tick_return_std | 0.00020142 | 0.000120233 | 0.596925 | 0.1 | 10 | False |
| SBIN | received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.2 | 5 | False |
| SBIN | tail received tick cadence | p90_gap_ms | 1750 | 692 | 0.395429 | 0.2 | 5 | False |
| SBIN | median spread scale | median_spread_bps | 1.92548 | 1.92885 | 1.00175 | 0.25 | 4 | False |
| SBIN | tail spread scale | p90_spread_bps | 3.84497 | 3.83021 | 0.99616 | 0.25 | 4 | False |
| SBIN | displayed L1 depth scale | median_l1_depth | 1048 | 808 | 0.770992 | 0.1 | 10 | False |
| SBIN | displayed L5 depth scale | median_l5_depth | 13743.5 | 6868 | 0.499727 | 0.1 | 10 | False |
| SBIN | L1 imbalance scale | median_abs_l1_imbalance | 0.648919 | 0.35 | 0.539359 | 0.25 | 4 | False |
| SBIN | one-tick volatility scale | one_tick_return_std | 0.000389548 | 0.000120499 | 0.30933 | 0.1 | 10 | False |
| SUNPHARMA | received tick cadence | median_gap_ms | 751 | 500 | 0.665779 | 0.2 | 5 | False |
| SUNPHARMA | tail received tick cadence | p90_gap_ms | 436729 | 436729 | 1 | 0.2 | 5 | False |
| SUNPHARMA | median spread scale | median_spread_bps | 1.55695 | 2.08162 | 1.33699 | 0.25 | 4 | False |
| SUNPHARMA | tail spread scale | p90_spread_bps | 3.12826 | 4.14543 | 1.32515 | 0.25 | 4 | False |
| SUNPHARMA | displayed L1 depth scale | median_l1_depth | 113 | 802 | 7.09735 | 0.1 | 10 | False |
| SUNPHARMA | displayed L5 depth scale | median_l5_depth | 986 | 6816 | 6.91278 | 0.1 | 10 | False |
| SUNPHARMA | L1 imbalance scale | median_abs_l1_imbalance | 0.61039 | 0.294872 | 0.483088 | 0.25 | 4 | False |
| SUNPHARMA | one-tick volatility scale | one_tick_return_std | 0.000344815 | 9.59112e-05 | 0.278153 | 0.1 | 10 | False |
| TCS | received tick cadence | median_gap_ms | 499 | 500 | 1.002 | 0.2 | 5 | False |
| TCS | tail received tick cadence | p90_gap_ms | 1000 | 692 | 0.692 | 0.2 | 5 | False |
| TCS | median spread scale | median_spread_bps | 1.83008 | 1.83926 | 1.00502 | 0.25 | 4 | False |
| TCS | tail spread scale | p90_spread_bps | 3.21444 | 3.65551 | 1.13721 | 0.25 | 4 | False |
| TCS | displayed L1 depth scale | median_l1_depth | 231 | 810 | 3.50649 | 0.1 | 10 | False |
| TCS | displayed L5 depth scale | median_l5_depth | 2997 | 6885 | 2.2973 | 0.1 | 10 | False |
| TCS | L1 imbalance scale | median_abs_l1_imbalance | 0.682609 | 0.350384 | 0.513301 | 0.25 | 4 | False |
| TCS | one-tick volatility scale | one_tick_return_std | 0.000649264 | 0.000123173 | 0.189712 | 0.1 | 10 | False |
| TECHM | received tick cadence | median_gap_ms | 501 | 500 | 0.998004 | 0.2 | 5 | False |
| TECHM | tail received tick cadence | p90_gap_ms | 3499.7 | 3500 | 1.00009 | 0.2 | 5 | False |
| TECHM | median spread scale | median_spread_bps | 3.28655 | 3.9316 | 1.19627 | 0.25 | 4 | False |
| TECHM | tail spread scale | p90_spread_bps | 4.67165 | 5.30536 | 1.13565 | 0.25 | 4 | False |
| TECHM | displayed L1 depth scale | median_l1_depth | 137 | 810 | 5.91241 | 0.1 | 10 | False |
| TECHM | displayed L5 depth scale | median_l5_depth | 1436 | 6886 | 4.79526 | 0.1 | 10 | False |
| TECHM | L1 imbalance scale | median_abs_l1_imbalance | 0.625668 | 0.5 | 0.799145 | 0.25 | 4 | False |
| TECHM | one-tick volatility scale | one_tick_return_std | 0.00086675 | 0.000124063 | 0.143136 | 0.1 | 10 | False |
| ULTRACEMCO | received tick cadence | median_gap_ms | 2140.5 | 500 | 0.23359 | 0.2 | 5 | False |
| ULTRACEMCO | tail received tick cadence | p90_gap_ms | 450515 | 450515 | 0.999999 | 0.2 | 5 | False |
| ULTRACEMCO | median spread scale | median_spread_bps | 2.58498 | 2.58942 | 1.00172 | 0.25 | 4 | False |
| ULTRACEMCO | tail spread scale | p90_spread_bps | 4.31611 | 5.1558 | 1.19455 | 0.25 | 4 | False |
| ULTRACEMCO | displayed L1 depth scale | median_l1_depth | 30 | 33 | 1.1 | 0.1 | 10 | False |
| ULTRACEMCO | displayed L5 depth scale | median_l5_depth | 309 | 282 | 0.912621 | 0.1 | 10 | False |
| ULTRACEMCO | L1 imbalance scale | median_abs_l1_imbalance | 0.666667 | 0.421053 | 0.631579 | 0.25 | 4 | False |
| ULTRACEMCO | one-tick volatility scale | one_tick_return_std | 0.000441904 | 0.000116794 | 0.264297 | 0.1 | 10 | False |
| WIPRO | received tick cadence | median_gap_ms | 501 | 500 | 0.998004 | 0.2 | 5 | False |
| WIPRO | tail received tick cadence | p90_gap_ms | 3459.2 | 692 | 0.200046 | 0.2 | 5 | False |
| WIPRO | median spread scale | median_spread_bps | 2.22785 | 2.24809 | 1.00908 | 0.25 | 4 | False |
| WIPRO | tail spread scale | p90_spread_bps | 3.40812 | 3.90912 | 1.147 | 0.25 | 4 | False |
| WIPRO | displayed L1 depth scale | median_l1_depth | 1427 | 810 | 0.567624 | 0.1 | 10 | False |
| WIPRO | displayed L5 depth scale | median_l5_depth | 14713 | 6885 | 0.467954 | 0.1 | 10 | False |
| WIPRO | L1 imbalance scale | median_abs_l1_imbalance | 0.701962 | 0.384181 | 0.547296 | 0.25 | 4 | False |
| WIPRO | one-tick volatility scale | one_tick_return_std | 0.000506627 | 0.0001212 | 0.23923 | 0.1 | 10 | False |

## Remediation Queue

| priority | work_item | why | minimum_deliverable | acceptance_gate |
| --- | --- | --- | --- | --- |
| 1 | collect_multi_day_real_anchor_panel | A single real WebSocket day cannot identify regime frequencies, annual tails, month effects, or stable cross-regime calibration. | At least 5-10 full real trading days across normal, volatile, and shock-like sessions with the same 54-column WebSocket schema. | Real anchor profile table has multiple dates per symbol and reports stable cadence/spread/depth ranges before strategy mining resumes. |
| 2 | calibrate_median_abs_l1_imbalance | 0.00% of symbol anchors are outside ratio gates; median synthetic/real ratio=0.634. | Adjust generator calibration for L1 imbalance scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 3 | calibrate_median_l1_depth | 0.00% of symbol anchors are outside ratio gates; median synthetic/real ratio=1.359. | Adjust generator calibration for displayed L1 depth scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 4 | calibrate_median_l5_depth | 0.00% of symbol anchors are outside ratio gates; median synthetic/real ratio=0.999. | Adjust generator calibration for displayed L5 depth scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 5 | calibrate_median_spread_bps | 0.00% of symbol anchors are outside ratio gates; median synthetic/real ratio=1.005. | Adjust generator calibration for median spread scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 6 | calibrate_one_tick_return_std | 0.00% of symbol anchors are outside ratio gates; median synthetic/real ratio=0.266. | Adjust generator calibration for one-tick volatility scale and rerun Phase94 comparison. | Gap fraction <= 25% for this metric on the current one-day anchor, then confirm with multi-day real panel. |
| 7 | freeze_strategy_replay_until_calibration_gate | Phase93 explicitly stopped strategy mining; new strategy branches would be fishing unless realism gaps are triaged. | Machine-readable gate that blocks Phase95+ strategy replay unless Phase94 calibration_replay_resume_allowed=1. | No new strategy replay milestone is marked ready while calibration audit fails. |

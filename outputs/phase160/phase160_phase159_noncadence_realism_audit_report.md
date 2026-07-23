# Phase160 Phase159 Non-cadence Realism Audit

Generated UTC: 2026-07-23T10:12:03.796582+00:00

Phase160 profiles spread, visible depth, L1 imbalance, and one-tick volatility from the actual Phase159 generated dense shard.
It replaces stale non-cadence assumptions with generated-shard evidence. It does not run strategy replay, fills, P&L, or Azure reads.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase160_symbols_compared | 32 | Symbols compared |
| phase160_anchor_metric_rows | 192 | Non-cadence symbol/metric rows compared |
| phase160_calibration_gap_rows | 0 | Non-cadence rows outside gates |
| phase160_calibration_gap_fraction | 0 | Fraction of non-cadence rows outside gates |
| phase160_severe_metric_gap_count | 0 | Non-cadence metrics with gap_fraction > 50% |
| phase160_phase159_dense_rows_profiled | 16838528 | Phase159 dense rows profiled |
| phase160_generated_noncadence_realism_pass | 1 | 1 means generated Phase159 non-cadence profile passes Phase106-style gate |
| phase160_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase160_next_best_action | combine_phase159_cadence_and_phase160_noncadence_acceptance_then_plan_broader_materialization | Recommended next milestone |

## Generated Non-cadence Gap Summary

| category | metric | symbol_metrics | gap_count | gap_fraction | median_synthetic_to_real_ratio | min_synthetic_to_real_ratio | max_synthetic_to_real_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L1 imbalance scale | median_abs_l1_imbalance | 32 | 0 | 0 | 0.638103 | 0.270734 | 1.75028 |
| displayed L1 depth scale | median_l1_depth | 32 | 0 | 0 | 1.32867 | 0.265896 | 6.93805 |
| displayed L5 depth scale | median_l5_depth | 32 | 0 | 0 | 0.978391 | 0.130258 | 6.75862 |
| median spread scale | median_spread_bps | 32 | 0 | 0 | 1.00132 | 0.749184 | 1.99357 |
| one-tick volatility scale | one_tick_return_std | 32 | 0 | 0 | 0.260655 | 0.106275 | 1.22717 |
| tail spread scale | p90_spread_bps | 32 | 0 | 0 | 0.768782 | 0.340354 | 1.02287 |

## Depth Imbalance Override Contract

_No rows._

## Generated Non-cadence Comparison

| symbol | category | metric | real_value | synthetic_value | synthetic_to_real_ratio | lower_ratio_gate | upper_ratio_gate | calibration_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | median spread scale | median_spread_bps | 2.20726 | 2.19884 | 0.996186 | 0.25 | 4 | False |
| ADANIPORTS | tail spread scale | p90_spread_bps | 3.85933 | 3.30267 | 0.855764 | 0.25 | 4 | False |
| ADANIPORTS | displayed L1 depth scale | median_l1_depth | 131 | 790 | 6.03053 | 0.1 | 10 | False |
| ADANIPORTS | displayed L5 depth scale | median_l5_depth | 1088 | 6715 | 6.17188 | 0.1 | 10 | False |
| ADANIPORTS | L1 imbalance scale | median_abs_l1_imbalance | 0.62963 | 0.214128 | 0.340086 | 0.25 | 4 | False |
| ADANIPORTS | one-tick volatility scale | one_tick_return_std | 0.000441155 | 0.000118974 | 0.269686 | 0.1 | 10 | False |
| AXISBANK | median spread scale | median_spread_bps | 1.51435 | 1.51502 | 1.00044 | 0.25 | 4 | False |
| AXISBANK | tail spread scale | p90_spread_bps | 3.02595 | 2.34059 | 0.773505 | 0.25 | 4 | False |
| AXISBANK | displayed L1 depth scale | median_l1_depth | 249 | 790 | 3.17269 | 0.1 | 10 | False |
| AXISBANK | displayed L5 depth scale | median_l5_depth | 3048 | 6716 | 2.20341 | 0.1 | 10 | False |
| AXISBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.549598 | 0.35 | 0.636829 | 0.25 | 4 | False |
| AXISBANK | one-tick volatility scale | one_tick_return_std | 0.000423171 | 0.000121337 | 0.286733 | 0.1 | 10 | False |
| BAJAJ-AUTO | median spread scale | median_spread_bps | 2.46627 | 2.91579 | 1.18227 | 0.25 | 4 | False |
| BAJAJ-AUTO | tail spread scale | p90_spread_bps | 4.37443 | 4.37908 | 1.00106 | 0.25 | 4 | False |
| BAJAJ-AUTO | displayed L1 depth scale | median_l1_depth | 61 | 52 | 0.852459 | 0.1 | 10 | False |
| BAJAJ-AUTO | displayed L5 depth scale | median_l5_depth | 366 | 434 | 1.18579 | 0.1 | 10 | False |
| BAJAJ-AUTO | L1 imbalance scale | median_abs_l1_imbalance | 0.578947 | 0.6 | 1.03636 | 0.25 | 4 | False |
| BAJAJ-AUTO | one-tick volatility scale | one_tick_return_std | 0.00071201 | 9.73462e-05 | 0.13672 | 0.1 | 10 | False |
| BANKBEES | median spread scale | median_spread_bps | 3.33389 | 3.66584 | 1.09957 | 0.25 | 4 | False |
| BANKBEES | tail spread scale | p90_spread_bps | 5.65504 | 5.16736 | 0.913761 | 0.25 | 4 | False |
| BANKBEES | displayed L1 depth scale | median_l1_depth | 403 | 784 | 1.94541 | 0.1 | 10 | False |
| BANKBEES | displayed L5 depth scale | median_l5_depth | 5262 | 6665 | 1.26663 | 0.1 | 10 | False |
| BANKBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.808031 | 0.327922 | 0.405829 | 0.25 | 4 | False |
| BANKBEES | one-tick volatility scale | one_tick_return_std | 0.000217665 | 0.000117415 | 0.539432 | 0.1 | 10 | False |
| BHARTIARTL | median spread scale | median_spread_bps | 2.09293 | 1.57484 | 0.752461 | 0.25 | 4 | False |
| BHARTIARTL | tail spread scale | p90_spread_bps | 3.15637 | 2.16555 | 0.686088 | 0.25 | 4 | False |
| BHARTIARTL | displayed L1 depth scale | median_l1_depth | 415 | 788 | 1.8988 | 0.1 | 10 | False |
| BHARTIARTL | displayed L5 depth scale | median_l5_depth | 3715 | 6700 | 1.8035 | 0.1 | 10 | False |
| BHARTIARTL | L1 imbalance scale | median_abs_l1_imbalance | 0.547826 | 0.350267 | 0.639377 | 0.25 | 4 | False |
| BHARTIARTL | one-tick volatility scale | one_tick_return_std | 0.00043748 | 0.000113935 | 0.260436 | 0.1 | 10 | False |
| BPCL | median spread scale | median_spread_bps | 1.63921 | 1.63329 | 0.99639 | 0.25 | 4 | False |
| BPCL | tail spread scale | p90_spread_bps | 4.89996 | 1.66772 | 0.340354 | 0.25 | 4 | False |
| BPCL | displayed L1 depth scale | median_l1_depth | 2059 | 794 | 0.385624 | 0.1 | 10 | False |
| BPCL | displayed L5 depth scale | median_l5_depth | 19762 | 6748 | 0.341463 | 0.1 | 10 | False |
| BPCL | L1 imbalance scale | median_abs_l1_imbalance | 0.653486 | 0.350097 | 0.535737 | 0.25 | 4 | False |
| BPCL | one-tick volatility scale | one_tick_return_std | 0.000615309 | 0.000117222 | 0.190509 | 0.1 | 10 | False |
| BRITANNIA | median spread scale | median_spread_bps | 2.81756 | 3.73327 | 1.325 | 0.25 | 4 | False |
| BRITANNIA | tail spread scale | p90_spread_bps | 5.59754 | 4.73751 | 0.846356 | 0.25 | 4 | False |
| BRITANNIA | displayed L1 depth scale | median_l1_depth | 35 | 41 | 1.17143 | 0.1 | 10 | False |
| BRITANNIA | displayed L5 depth scale | median_l5_depth | 406.5 | 345 | 0.848708 | 0.1 | 10 | False |
| BRITANNIA | L1 imbalance scale | median_abs_l1_imbalance | 0.542036 | 0.948718 | 1.75028 | 0.25 | 4 | False |
| BRITANNIA | one-tick volatility scale | one_tick_return_std | 0.00049004 | 9.14695e-05 | 0.186657 | 0.1 | 10 | False |
| CIPLA | median spread scale | median_spread_bps | 2.80387 | 2.79967 | 0.998502 | 0.25 | 4 | False |
| CIPLA | tail spread scale | p90_spread_bps | 4.90069 | 3.58827 | 0.732196 | 0.25 | 4 | False |
| CIPLA | displayed L1 depth scale | median_l1_depth | 136 | 786 | 5.77941 | 0.1 | 10 | False |
| CIPLA | displayed L5 depth scale | median_l5_depth | 1594 | 6680 | 4.19072 | 0.1 | 10 | False |
| CIPLA | L1 imbalance scale | median_abs_l1_imbalance | 0.675676 | 0.568627 | 0.841569 | 0.25 | 4 | False |
| CIPLA | one-tick volatility scale | one_tick_return_std | 0.000439541 | 7.91082e-05 | 0.179979 | 0.1 | 10 | False |
| DRREDDY | median spread scale | median_spread_bps | 3.24649 | 2.43222 | 0.749184 | 0.25 | 4 | False |
| DRREDDY | tail spread scale | p90_spread_bps | 4.86934 | 3.28726 | 0.675093 | 0.25 | 4 | False |
| DRREDDY | displayed L1 depth scale | median_l1_depth | 271.5 | 786 | 2.89503 | 0.1 | 10 | False |
| DRREDDY | displayed L5 depth scale | median_l5_depth | 2642 | 6681 | 2.52877 | 0.1 | 10 | False |
| DRREDDY | L1 imbalance scale | median_abs_l1_imbalance | 0.618831 | 0.207237 | 0.334884 | 0.25 | 4 | False |
| DRREDDY | one-tick volatility scale | one_tick_return_std | 0.000542243 | 8.24529e-05 | 0.152059 | 0.1 | 10 | False |
| GOLDBEES | median spread scale | median_spread_bps | 0.857082 | 0.855884 | 0.998603 | 0.25 | 4 | False |
| GOLDBEES | tail spread scale | p90_spread_bps | 2.56487 | 0.881205 | 0.343567 | 0.25 | 4 | False |
| GOLDBEES | displayed L1 depth scale | median_l1_depth | 11211.5 | 10983 | 0.979619 | 0.1 | 10 | False |
| GOLDBEES | displayed L5 depth scale | median_l5_depth | 95705.5 | 93360 | 0.975493 | 0.1 | 10 | False |
| GOLDBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.747425 | 0.202353 | 0.270734 | 0.25 | 4 | False |
| GOLDBEES | one-tick volatility scale | one_tick_return_std | 0.000285098 | 9.84643e-05 | 0.34537 | 0.1 | 10 | False |
| HCLTECH | median spread scale | median_spread_bps | 3.25574 | 2.4565 | 0.754515 | 0.25 | 4 | False |
| HCLTECH | tail spread scale | p90_spread_bps | 4.26218 | 3.33533 | 0.782541 | 0.25 | 4 | False |
| HCLTECH | displayed L1 depth scale | median_l1_depth | 339.5 | 792 | 2.33284 | 0.1 | 10 | False |
| HCLTECH | displayed L5 depth scale | median_l5_depth | 4819 | 6732 | 1.39697 | 0.1 | 10 | False |
| HCLTECH | L1 imbalance scale | median_abs_l1_imbalance | 0.660606 | 0.293729 | 0.444636 | 0.25 | 4 | False |
| HCLTECH | one-tick volatility scale | one_tick_return_std | 0.000923066 | 0.000132187 | 0.143205 | 0.1 | 10 | False |
| HDFCBANK | median spread scale | median_spread_bps | 1.22048 | 1.22195 | 1.00121 | 0.25 | 4 | False |
| HDFCBANK | tail spread scale | p90_spread_bps | 2.45085 | 1.87945 | 0.766859 | 0.25 | 4 | False |
| HDFCBANK | displayed L1 depth scale | median_l1_depth | 1010 | 792 | 0.784158 | 0.1 | 10 | False |
| HDFCBANK | displayed L5 depth scale | median_l5_depth | 15104 | 6731 | 0.445644 | 0.1 | 10 | False |
| HDFCBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.622123 | 0.572368 | 0.920024 | 0.25 | 4 | False |
| HDFCBANK | one-tick volatility scale | one_tick_return_std | 0.000266132 | 0.000326589 | 1.22717 | 0.1 | 10 | False |
| HINDUNILVR | median spread scale | median_spread_bps | 1.4103 | 1.87735 | 1.33116 | 0.25 | 4 | False |
| HINDUNILVR | tail spread scale | p90_spread_bps | 3.52032 | 2.41599 | 0.686299 | 0.25 | 4 | False |
| HINDUNILVR | displayed L1 depth scale | median_l1_depth | 188.5 | 786 | 4.16976 | 0.1 | 10 | False |
| HINDUNILVR | displayed L5 depth scale | median_l5_depth | 1287 | 6681 | 5.19114 | 0.1 | 10 | False |
| HINDUNILVR | L1 imbalance scale | median_abs_l1_imbalance | 0.627765 | 0.35 | 0.557533 | 0.25 | 4 | False |
| HINDUNILVR | one-tick volatility scale | one_tick_return_std | 0.000449187 | 0.000104665 | 0.233011 | 0.1 | 10 | False |
| ICICIBANK | median spread scale | median_spread_bps | 1.41784 | 1.42373 | 1.00416 | 0.25 | 4 | False |
| ICICIBANK | tail spread scale | p90_spread_bps | 2.84353 | 2.19152 | 0.770704 | 0.25 | 4 | False |
| ICICIBANK | displayed L1 depth scale | median_l1_depth | 580 | 790 | 1.36207 | 0.1 | 10 | False |
| ICICIBANK | displayed L5 depth scale | median_l5_depth | 6394 | 6714 | 1.05005 | 0.1 | 10 | False |
| ICICIBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.618943 | 0.368771 | 0.595807 | 0.25 | 4 | False |
| ICICIBANK | one-tick volatility scale | one_tick_return_std | 0.00027235 | 0.000186817 | 0.685946 | 0.1 | 10 | False |
| INFY | median spread scale | median_spread_bps | 1.81422 | 1.81463 | 1.00022 | 0.25 | 4 | False |
| INFY | tail spread scale | p90_spread_bps | 3.66367 | 2.80323 | 0.765143 | 0.25 | 4 | False |
| INFY | displayed L1 depth scale | median_l1_depth | 613 | 794 | 1.29527 | 0.1 | 10 | False |
| INFY | displayed L5 depth scale | median_l5_depth | 9352 | 6749 | 0.721664 | 0.1 | 10 | False |
| INFY | L1 imbalance scale | median_abs_l1_imbalance | 0.758157 | 0.75 | 0.989241 | 0.25 | 4 | False |
| INFY | one-tick volatility scale | one_tick_return_std | 0.00067843 | 0.000135265 | 0.19938 | 0.1 | 10 | False |
| ITBEES | median spread scale | median_spread_bps | 3.12794 | 3.11534 | 0.995972 | 0.25 | 4 | False |
| ITBEES | tail spread scale | p90_spread_bps | 6.29723 | 3.2159 | 0.510685 | 0.25 | 4 | False |
| ITBEES | displayed L1 depth scale | median_l1_depth | 134432 | 189481 | 1.40949 | 0.1 | 10 | False |
| ITBEES | displayed L5 depth scale | median_l5_depth | 2.15215e+06 | 1.61035e+06 | 0.748252 | 0.1 | 10 | False |
| ITBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.68474 | 0.740336 | 1.08119 | 0.25 | 4 | False |
| ITBEES | one-tick volatility scale | one_tick_return_std | 0.000841952 | 8.94786e-05 | 0.106275 | 0.1 | 10 | False |
| ITC | median spread scale | median_spread_bps | 1.78715 | 1.78332 | 0.997856 | 0.25 | 4 | False |
| ITC | tail spread scale | p90_spread_bps | 3.92555 | 1.8175 | 0.462991 | 0.25 | 4 | False |
| ITC | displayed L1 depth scale | median_l1_depth | 5559 | 13137 | 2.36319 | 0.1 | 10 | False |
| ITC | displayed L5 depth scale | median_l5_depth | 113657 | 111651 | 0.98235 | 0.1 | 10 | False |
| ITC | L1 imbalance scale | median_abs_l1_imbalance | 0.589392 | 0.509905 | 0.865137 | 0.25 | 4 | False |
| ITC | one-tick volatility scale | one_tick_return_std | 0.000353813 | 0.00010439 | 0.295042 | 0.1 | 10 | False |
| JUNIORBEES | median spread scale | median_spread_bps | 3.60078 | 3.66388 | 1.01753 | 0.25 | 4 | False |
| JUNIORBEES | tail spread scale | p90_spread_bps | 5.53578 | 4.53654 | 0.819494 | 0.25 | 4 | False |
| JUNIORBEES | displayed L1 depth scale | median_l1_depth | 417 | 784 | 1.8801 | 0.1 | 10 | False |
| JUNIORBEES | displayed L5 depth scale | median_l5_depth | 8912 | 6663 | 0.747644 | 0.1 | 10 | False |
| JUNIORBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.863238 | 0.69774 | 0.808283 | 0.25 | 4 | False |
| JUNIORBEES | one-tick volatility scale | one_tick_return_std | 0.000210559 | 0.000110065 | 0.522728 | 0.1 | 10 | False |
| KOTAKBANK | median spread scale | median_spread_bps | 2.62329 | 2.63373 | 1.00398 | 0.25 | 4 | False |
| KOTAKBANK | tail spread scale | p90_spread_bps | 3.96432 | 4.05497 | 1.02287 | 0.25 | 4 | False |
| KOTAKBANK | displayed L1 depth scale | median_l1_depth | 1719 | 790 | 0.45957 | 0.1 | 10 | False |
| KOTAKBANK | displayed L5 depth scale | median_l5_depth | 25525 | 6715 | 0.263075 | 0.1 | 10 | False |
| KOTAKBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.670857 | 0.601583 | 0.896738 | 0.25 | 4 | False |
| KOTAKBANK | one-tick volatility scale | one_tick_return_std | 0.000438758 | 0.000114461 | 0.260874 | 0.1 | 10 | False |
| LT | median spread scale | median_spread_bps | 1.27755 | 1.27309 | 0.996515 | 0.25 | 4 | False |
| LT | tail spread scale | p90_spread_bps | 2.8018 | 1.56477 | 0.558487 | 0.25 | 4 | False |
| LT | displayed L1 depth scale | median_l1_depth | 106 | 56 | 0.528302 | 0.1 | 10 | False |
| LT | displayed L5 depth scale | median_l5_depth | 481 | 472 | 0.981289 | 0.1 | 10 | False |
| LT | L1 imbalance scale | median_abs_l1_imbalance | 0.549296 | 0.416667 | 0.758547 | 0.25 | 4 | False |
| LT | one-tick volatility scale | one_tick_return_std | 0.000333916 | 0.000178414 | 0.534308 | 0.1 | 10 | False |
| M&M | median spread scale | median_spread_bps | 1.26723 | 1.26943 | 1.00174 | 0.25 | 4 | False |
| M&M | tail spread scale | p90_spread_bps | 2.86439 | 1.63786 | 0.571799 | 0.25 | 4 | False |
| M&M | displayed L1 depth scale | median_l1_depth | 47 | 48 | 1.02128 | 0.1 | 10 | False |
| M&M | displayed L5 depth scale | median_l5_depth | 447 | 414 | 0.926174 | 0.1 | 10 | False |
| M&M | L1 imbalance scale | median_abs_l1_imbalance | 0.676548 | 0.189189 | 0.279639 | 0.25 | 4 | False |
| M&M | one-tick volatility scale | one_tick_return_std | 0.000420129 | 0.000116006 | 0.276119 | 0.1 | 10 | False |
| MARUTI | median spread scale | median_spread_bps | 2.91153 | 2.91595 | 1.00152 | 0.25 | 4 | False |
| MARUTI | tail spread scale | p90_spread_bps | 4.36205 | 3.77543 | 0.865517 | 0.25 | 4 | False |
| MARUTI | displayed L1 depth scale | median_l1_depth | 40 | 44 | 1.1 | 0.1 | 10 | False |
| MARUTI | displayed L5 depth scale | median_l5_depth | 411 | 368 | 0.895377 | 0.1 | 10 | False |
| MARUTI | L1 imbalance scale | median_abs_l1_imbalance | 0.592949 | 0.5 | 0.843243 | 0.25 | 4 | False |
| MARUTI | one-tick volatility scale | one_tick_return_std | 0.000428897 | 0.000113449 | 0.264513 | 0.1 | 10 | False |
| NESTLEIND | median spread scale | median_spread_bps | 2.44069 | 2.78757 | 1.14212 | 0.25 | 4 | False |
| NESTLEIND | tail spread scale | p90_spread_bps | 4.18819 | 3.5922 | 0.857697 | 0.25 | 4 | False |
| NESTLEIND | displayed L1 depth scale | median_l1_depth | 349 | 786 | 2.25215 | 0.1 | 10 | False |
| NESTLEIND | displayed L5 depth scale | median_l5_depth | 2850 | 6682 | 2.34456 | 0.1 | 10 | False |
| NESTLEIND | L1 imbalance scale | median_abs_l1_imbalance | 0.619048 | 0.411932 | 0.665428 | 0.25 | 4 | False |
| NESTLEIND | one-tick volatility scale | one_tick_return_std | 0.000651157 | 8.27475e-05 | 0.127078 | 0.1 | 10 | False |
| NIFTYBEES | median spread scale | median_spread_bps | 1.45757 | 1.45408 | 0.997606 | 0.25 | 4 | False |
| NIFTYBEES | tail spread scale | p90_spread_bps | 3.6412 | 1.83775 | 0.50471 | 0.25 | 4 | False |
| NIFTYBEES | displayed L1 depth scale | median_l1_depth | 2941 | 782 | 0.265896 | 0.1 | 10 | False |
| NIFTYBEES | displayed L5 depth scale | median_l5_depth | 51029.5 | 6647 | 0.130258 | 0.1 | 10 | False |
| NIFTYBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.803454 | 0.620865 | 0.772745 | 0.25 | 4 | False |
| NIFTYBEES | one-tick volatility scale | one_tick_return_std | 0.00014983 | 8.97553e-05 | 0.599048 | 0.1 | 10 | False |
| ONGC | median spread scale | median_spread_bps | 1.62121 | 2.02071 | 1.24642 | 0.25 | 4 | False |
| ONGC | tail spread scale | p90_spread_bps | 3.6357 | 2.50247 | 0.688305 | 0.25 | 4 | False |
| ONGC | displayed L1 depth scale | median_l1_depth | 1042 | 792 | 0.760077 | 0.1 | 10 | False |
| ONGC | displayed L5 depth scale | median_l5_depth | 7000.5 | 6731 | 0.961503 | 0.1 | 10 | False |
| ONGC | L1 imbalance scale | median_abs_l1_imbalance | 0.612081 | 0.35 | 0.57182 | 0.25 | 4 | False |
| ONGC | one-tick volatility scale | one_tick_return_std | 0.000511555 | 0.000114353 | 0.22354 | 0.1 | 10 | False |
| RELIANCE | median spread scale | median_spread_bps | 0.771159 | 1.53736 | 1.99357 | 0.25 | 4 | False |
| RELIANCE | tail spread scale | p90_spread_bps | 3.07882 | 2.33669 | 0.758955 | 0.25 | 4 | False |
| RELIANCE | displayed L1 depth scale | median_l1_depth | 986 | 792 | 0.803245 | 0.1 | 10 | False |
| RELIANCE | displayed L5 depth scale | median_l5_depth | 11881.5 | 6732 | 0.566595 | 0.1 | 10 | False |
| RELIANCE | L1 imbalance scale | median_abs_l1_imbalance | 0.716704 | 0.44359 | 0.61893 | 0.25 | 4 | False |
| RELIANCE | one-tick volatility scale | one_tick_return_std | 0.00020142 | 0.000209142 | 1.03834 | 0.1 | 10 | False |
| SBIN | median spread scale | median_spread_bps | 1.92548 | 1.92611 | 1.00033 | 0.25 | 4 | False |
| SBIN | tail spread scale | p90_spread_bps | 3.84497 | 2.97597 | 0.77399 | 0.25 | 4 | False |
| SBIN | displayed L1 depth scale | median_l1_depth | 1048 | 792 | 0.755725 | 0.1 | 10 | False |
| SBIN | displayed L5 depth scale | median_l5_depth | 13743.5 | 6730 | 0.489686 | 0.1 | 10 | False |
| SBIN | L1 imbalance scale | median_abs_l1_imbalance | 0.648919 | 0.35 | 0.539359 | 0.25 | 4 | False |
| SBIN | one-tick volatility scale | one_tick_return_std | 0.000389548 | 0.000118425 | 0.304006 | 0.1 | 10 | False |
| SUNPHARMA | median spread scale | median_spread_bps | 1.55695 | 2.07516 | 1.33284 | 0.25 | 4 | False |
| SUNPHARMA | tail spread scale | p90_spread_bps | 3.12826 | 2.67214 | 0.854194 | 0.25 | 4 | False |
| SUNPHARMA | displayed L1 depth scale | median_l1_depth | 113 | 784 | 6.93805 | 0.1 | 10 | False |
| SUNPHARMA | displayed L5 depth scale | median_l5_depth | 986 | 6664 | 6.75862 | 0.1 | 10 | False |
| SUNPHARMA | L1 imbalance scale | median_abs_l1_imbalance | 0.61039 | 0.295039 | 0.483362 | 0.25 | 4 | False |
| SUNPHARMA | one-tick volatility scale | one_tick_return_std | 0.000344815 | 9.08425e-05 | 0.263453 | 0.1 | 10 | False |
| TCS | median spread scale | median_spread_bps | 1.83008 | 1.8324 | 1.00127 | 0.25 | 4 | False |
| TCS | tail spread scale | p90_spread_bps | 3.21444 | 2.30826 | 0.71809 | 0.25 | 4 | False |
| TCS | displayed L1 depth scale | median_l1_depth | 231 | 792 | 3.42857 | 0.1 | 10 | False |
| TCS | displayed L5 depth scale | median_l5_depth | 2997 | 6733 | 2.24658 | 0.1 | 10 | False |
| TCS | L1 imbalance scale | median_abs_l1_imbalance | 0.682609 | 0.350427 | 0.513365 | 0.25 | 4 | False |
| TCS | one-tick volatility scale | one_tick_return_std | 0.000649264 | 0.000137557 | 0.211866 | 0.1 | 10 | False |
| TECHM | median spread scale | median_spread_bps | 3.28655 | 3.32708 | 1.01233 | 0.25 | 4 | False |
| TECHM | tail spread scale | p90_spread_bps | 4.67165 | 4.1092 | 0.879602 | 0.25 | 4 | False |
| TECHM | displayed L1 depth scale | median_l1_depth | 137 | 792 | 5.78102 | 0.1 | 10 | False |
| TECHM | displayed L5 depth scale | median_l5_depth | 1436 | 6732 | 4.68802 | 0.1 | 10 | False |
| TECHM | L1 imbalance scale | median_abs_l1_imbalance | 0.625668 | 0.498361 | 0.796525 | 0.25 | 4 | False |
| TECHM | one-tick volatility scale | one_tick_return_std | 0.00086675 | 0.000109906 | 0.126802 | 0.1 | 10 | False |
| ULTRACEMCO | median spread scale | median_spread_bps | 2.58498 | 2.58851 | 1.00137 | 0.25 | 4 | False |
| ULTRACEMCO | tail spread scale | p90_spread_bps | 4.31611 | 3.48311 | 0.807001 | 0.25 | 4 | False |
| ULTRACEMCO | displayed L1 depth scale | median_l1_depth | 30 | 32 | 1.06667 | 0.1 | 10 | False |
| ULTRACEMCO | displayed L5 depth scale | median_l5_depth | 309 | 274 | 0.886731 | 0.1 | 10 | False |
| ULTRACEMCO | L1 imbalance scale | median_abs_l1_imbalance | 0.666667 | 0.428571 | 0.642857 | 0.25 | 4 | False |
| ULTRACEMCO | one-tick volatility scale | one_tick_return_std | 0.000441904 | 9.88418e-05 | 0.223673 | 0.1 | 10 | False |
| WIPRO | median spread scale | median_spread_bps | 2.22785 | 2.24146 | 1.00611 | 0.25 | 4 | False |
| WIPRO | tail spread scale | p90_spread_bps | 3.40812 | 2.88196 | 0.845616 | 0.25 | 4 | False |
| WIPRO | displayed L1 depth scale | median_l1_depth | 1427 | 792 | 0.555011 | 0.1 | 10 | False |
| WIPRO | displayed L5 depth scale | median_l5_depth | 14713 | 6732 | 0.457555 | 0.1 | 10 | False |
| WIPRO | L1 imbalance scale | median_abs_l1_imbalance | 0.701962 | 0.385269 | 0.548846 | 0.25 | 4 | False |
| WIPRO | one-tick volatility scale | one_tick_return_std | 0.000506627 | 0.000112537 | 0.22213 | 0.1 | 10 | False |

# Phase158 Phase106-style Full Realism Audit

Generated UTC: 2026-07-23T10:00:02.902149+00:00

Phase158 reruns the Phase106-style realism decision using Phase157 full-partition cadence anchors for cadence metrics and preserved Phase106 non-cadence gates for spread, depth, imbalance, and volatility.
It is an audit only: no strategy replay, no fills, no P&L, and no Azure reads.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase158_phase157_rewire_ready | 1 | Inherited Phase157 cadence rewire readiness |
| phase158_symbols_compared | 32 | Symbols present in full rewired realism audit |
| phase158_anchor_metric_rows | 320 | Symbol/metric anchor rows compared |
| phase158_calibration_gap_rows | 87 | Rows outside Phase158 gates |
| phase158_calibration_gap_fraction | 0.271875 | Fraction of rows outside Phase158 gates |
| phase158_severe_metric_gap_count | 2 | Metrics with gap_fraction > 50% |
| phase158_cadence_gap_rows | 56 | Cadence rows outside full-partition cadence gates |
| phase158_non_cadence_gap_rows | 31 | Preserved non-cadence rows outside existing gates |
| phase158_full_rewired_realism_pass | 0 | 1 means full rewired realism audit passes |
| phase158_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase158_next_best_action | fix_phase158_remaining_distributional_cadence_depth_imbalance_gaps_before_strategy_replay | Recommended next milestone |

## Gap Summary

| category | metric | anchor_source | symbol_metrics | gap_count | gap_fraction | median_synthetic_to_real_ratio | min_synthetic_to_real_ratio | max_synthetic_to_real_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L1 imbalance scale | median_abs_l1_imbalance | phase106_existing_non_cadence_real_anchor | 32 | 15 | 0.46875 | 0.272869 | 0 | 1.08119 |
| displayed L1 depth scale | median_l1_depth | phase106_existing_non_cadence_real_anchor | 32 | 7 | 0.21875 | 2.14155 | 0.00596584 | 26.9333 |
| displayed L5 depth scale | median_l5_depth | phase106_existing_non_cadence_real_anchor | 32 | 9 | 0.28125 | 1.63643 | 0.00316706 | 22.2265 |
| median spread scale | median_spread_bps | phase106_existing_non_cadence_real_anchor | 32 | 0 | 0 | 1.00498 | 0.751177 | 1.99958 |
| one-tick volatility scale | one_tick_return_std | phase106_existing_non_cadence_real_anchor | 32 | 0 | 0 | 0.265841 | 0.121734 | 0.596925 |
| rewired received tick cadence | median_gap_ms | phase154_full_partition_via_phase155_phase157 | 32 | 8 | 0.25 | 0.666223 | 0.249875 | 1 |
| rewired received tick cadence distribution | gap_le_1s_fraction | phase154_full_partition_via_phase155_phase157 | 32 | 17 | 0.53125 | 1.34217 | 1.01681 | 3.00794 |
| rewired tail received tick cadence | p90_gap_ms | phase154_full_partition_via_phase155_phase157 | 32 | 31 | 0.96875 | 0.129133 | 0.0844167 | 0.5 |
| rewired tail received tick cadence | p95_gap_ms | phase154_full_partition_via_phase155_phase157 | 32 | 0 | 0 | 1 | 0.999895 | 1.00007 |
| tail spread scale | p90_spread_bps | phase106_existing_non_cadence_real_anchor | 32 | 0 | 0 | 1.13643 | 0.985194 | 1.35755 |

## Remediation Queue

| priority | metric | work_item | gap_count | gap_fraction | rationale |
| --- | --- | --- | --- | --- | --- |
| 1 | p90_gap_ms | add_distributional_tail_cadence_model_not_only_p95_point_target | 31 | 0.96875 | Phase156 pins p95 but leaves p90 too dense for many symbols. |
| 2 | gap_le_1s_fraction | calibrate_idle_gap_frequency_to_match_gap_distribution | 17 | 0.53125 | Phase156 p95 idle gaps reduce dense-overstatement but the <=1s fraction remains too high/low for part of the universe. |
| 3 | median_abs_l1_imbalance | revisit_l1_imbalance_floor_and_side_skew_model | 15 | 0.46875 | Existing imbalance gates are preserved and remain a broad non-cadence blocker. |
| 4 | median_l5_depth | revisit_symbol_depth_scale_overrides_with_full_partition_non_cadence_anchors | 9 | 0.28125 | Existing non-cadence depth gates are preserved and still show symbol failures. |
| 5 | median_gap_ms | calibrate_symbol_median_cadence_without_breaking_p95_targets | 8 | 0.25 | Phase156 pins p95 but keeps median gaps at the dense 500ms baseline for slower symbols. |
| 6 | median_l1_depth | revisit_symbol_depth_scale_overrides_with_full_partition_non_cadence_anchors | 7 | 0.21875 | Existing non-cadence depth gates are preserved and still show symbol failures. |

## Rewired Realism Comparison

| symbol | category | metric | real_value | synthetic_value | synthetic_to_real_ratio | lower_ratio_gate | upper_ratio_gate | calibration_gap | anchor_source | synthetic_source | gate_type | absolute_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | rewired received tick cadence | median_gap_ms | 1000 | 500 | 0.5 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ADANIPORTS | rewired tail received tick cadence | p90_gap_ms | 4500 | 500 | 0.111111 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ADANIPORTS | rewired tail received tick cadence | p95_gap_ms | 5500 | 5500 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ADANIPORTS | rewired received tick cadence distribution | gap_le_1s_fraction | 0.546345 | 0.922508 | 1.68851 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.376163 |
| AXISBANK | rewired received tick cadence | median_gap_ms | 501 | 500 | 0.998004 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| AXISBANK | rewired tail received tick cadence | p90_gap_ms | 2001 | 500 | 0.249875 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| AXISBANK | rewired tail received tick cadence | p95_gap_ms | 4380.75 | 4381 | 1.00006 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| AXISBANK | rewired received tick cadence distribution | gap_le_1s_fraction | 0.773267 | 0.92258 | 1.19309 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.149313 |
| BAJAJ-AUTO | rewired received tick cadence | median_gap_ms | 1000 | 500 | 0.5 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BAJAJ-AUTO | rewired tail received tick cadence | p90_gap_ms | 4910.5 | 500 | 0.101823 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BAJAJ-AUTO | rewired tail received tick cadence | p95_gap_ms | 5939.25 | 5939 | 0.999958 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BAJAJ-AUTO | rewired received tick cadence distribution | gap_le_1s_fraction | 0.536706 | 0.922307 | 1.71846 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.385601 |
| BANKBEES | rewired received tick cadence | median_gap_ms | 999 | 500 | 0.500501 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BANKBEES | rewired tail received tick cadence | p90_gap_ms | 1255 | 500 | 0.398406 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BANKBEES | rewired tail received tick cadence | p95_gap_ms | 4450 | 4450 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BANKBEES | rewired received tick cadence distribution | gap_le_1s_fraction | 0.769716 | 0.922602 | 1.19863 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.152886 |
| BHARTIARTL | rewired received tick cadence | median_gap_ms | 749 | 500 | 0.667557 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BHARTIARTL | rewired tail received tick cadence | p90_gap_ms | 3250 | 500 | 0.153846 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BHARTIARTL | rewired tail received tick cadence | p95_gap_ms | 4762.4 | 4762 | 0.999916 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BHARTIARTL | rewired received tick cadence distribution | gap_le_1s_fraction | 0.708779 | 0.922572 | 1.30164 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.213794 |
| BPCL | rewired received tick cadence | median_gap_ms | 1635.5 | 500 | 0.305717 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BPCL | rewired tail received tick cadence | p90_gap_ms | 5239.4 | 500 | 0.0954308 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BPCL | rewired tail received tick cadence | p95_gap_ms | 6081.7 | 6082 | 1.00005 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BPCL | rewired received tick cadence distribution | gap_le_1s_fraction | 0.392118 | 0.922307 | 2.35211 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.530188 |
| BRITANNIA | rewired received tick cadence | median_gap_ms | 2000 | 500 | 0.25 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BRITANNIA | rewired tail received tick cadence | p90_gap_ms | 5923 | 500 | 0.0844167 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BRITANNIA | rewired tail received tick cadence | p95_gap_ms | 7000.8 | 7001 | 1.00003 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| BRITANNIA | rewired received tick cadence distribution | gap_le_1s_fraction | 0.345689 | 0.922288 | 2.66797 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.576598 |
| CIPLA | rewired received tick cadence | median_gap_ms | 1378 | 500 | 0.362845 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| CIPLA | rewired tail received tick cadence | p90_gap_ms | 5000 | 500 | 0.1 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| CIPLA | rewired tail received tick cadence | p95_gap_ms | 5953.9 | 5954 | 1.00002 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| CIPLA | rewired received tick cadence distribution | gap_le_1s_fraction | 0.438237 | 0.922302 | 2.10457 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.484065 |
| DRREDDY | rewired received tick cadence | median_gap_ms | 1250 | 500 | 0.4 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| DRREDDY | rewired tail received tick cadence | p90_gap_ms | 4792.5 | 500 | 0.10433 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| DRREDDY | rewired tail received tick cadence | p95_gap_ms | 5750 | 5750 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| DRREDDY | rewired received tick cadence distribution | gap_le_1s_fraction | 0.461243 | 0.92233 | 1.99966 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.461086 |
| GOLDBEES | rewired received tick cadence | median_gap_ms | 750 | 500 | 0.666667 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| GOLDBEES | rewired tail received tick cadence | p90_gap_ms | 3999 | 500 | 0.125031 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| GOLDBEES | rewired tail received tick cadence | p95_gap_ms | 5250 | 5250 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| GOLDBEES | rewired received tick cadence distribution | gap_le_1s_fraction | 0.667216 | 0.922565 | 1.38271 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.255349 |
| HCLTECH | rewired received tick cadence | median_gap_ms | 1000 | 500 | 0.5 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| HCLTECH | rewired tail received tick cadence | p90_gap_ms | 4500 | 500 | 0.111111 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| HCLTECH | rewired tail received tick cadence | p95_gap_ms | 5324.85 | 5325 | 1.00003 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| HCLTECH | rewired received tick cadence distribution | gap_le_1s_fraction | 0.520642 | 0.922573 | 1.77199 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.401932 |
| HINDUNILVR | rewired received tick cadence | median_gap_ms | 1000 | 500 | 0.5 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| HINDUNILVR | rewired tail received tick cadence | p90_gap_ms | 4750 | 500 | 0.105263 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| HINDUNILVR | rewired tail received tick cadence | p95_gap_ms | 5859.45 | 5859 | 0.999923 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| HINDUNILVR | rewired received tick cadence distribution | gap_le_1s_fraction | 0.5779 | 0.922323 | 1.59599 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.344423 |
| ICICIBANK | rewired received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ICICIBANK | rewired tail received tick cadence | p90_gap_ms | 1001 | 500 | 0.4995 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ICICIBANK | rewired tail received tick cadence | p95_gap_ms | 3403 | 3403 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ICICIBANK | rewired received tick cadence distribution | gap_le_1s_fraction | 0.896955 | 0.922379 | 1.02834 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.0254241 |
| INFY | rewired received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| INFY | rewired tail received tick cadence | p90_gap_ms | 2001 | 500 | 0.249875 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| INFY | rewired tail received tick cadence | p95_gap_ms | 3922.15 | 3922 | 0.999962 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| INFY | rewired received tick cadence distribution | gap_le_1s_fraction | 0.829054 | 0.922567 | 1.1128 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.0935134 |
| ITBEES | rewired received tick cadence | median_gap_ms | 2001 | 500 | 0.249875 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ITBEES | rewired tail received tick cadence | p90_gap_ms | 5828.9 | 500 | 0.0857795 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ITBEES | rewired tail received tick cadence | p95_gap_ms | 6911.05 | 6911 | 0.999993 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ITBEES | rewired received tick cadence distribution | gap_le_1s_fraction | 0.306614 | 0.922276 | 3.00794 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.615663 |
| ITC | rewired received tick cadence | median_gap_ms | 749 | 500 | 0.667557 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ITC | rewired tail received tick cadence | p90_gap_ms | 3752.8 | 500 | 0.133234 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ITC | rewired tail received tick cadence | p95_gap_ms | 4815.4 | 4815 | 0.999917 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ITC | rewired received tick cadence distribution | gap_le_1s_fraction | 0.727574 | 0.922599 | 1.26805 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.195025 |
| JUNIORBEES | rewired received tick cadence | median_gap_ms | 999 | 500 | 0.500501 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| JUNIORBEES | rewired tail received tick cadence | p90_gap_ms | 3347.7 | 500 | 0.149356 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| JUNIORBEES | rewired tail received tick cadence | p95_gap_ms | 4511 | 4511 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| JUNIORBEES | rewired received tick cadence distribution | gap_le_1s_fraction | 0.760716 | 0.922586 | 1.21279 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.16187 |
| KOTAKBANK | rewired received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| KOTAKBANK | rewired tail received tick cadence | p90_gap_ms | 3000 | 500 | 0.166667 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| KOTAKBANK | rewired tail received tick cadence | p95_gap_ms | 4051.3 | 4051 | 0.999926 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| KOTAKBANK | rewired received tick cadence distribution | gap_le_1s_fraction | 0.833298 | 0.922598 | 1.10717 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.0893005 |
| LT | rewired received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| LT | rewired tail received tick cadence | p90_gap_ms | 1001 | 500 | 0.4995 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| LT | rewired tail received tick cadence | p95_gap_ms | 3367 | 3367 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| LT | rewired received tick cadence distribution | gap_le_1s_fraction | 0.885798 | 0.922391 | 1.04131 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.0365932 |
| M&M | rewired received tick cadence | median_gap_ms | 501 | 500 | 0.998004 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| M&M | rewired tail received tick cadence | p90_gap_ms | 1750 | 500 | 0.285714 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| M&M | rewired tail received tick cadence | p95_gap_ms | 4285.45 | 4285 | 0.999895 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| M&M | rewired received tick cadence distribution | gap_le_1s_fraction | 0.825434 | 0.922578 | 1.11769 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.0971444 |
| MARUTI | rewired received tick cadence | median_gap_ms | 683 | 500 | 0.732064 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| MARUTI | rewired tail received tick cadence | p90_gap_ms | 2502 | 500 | 0.19984 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| MARUTI | rewired tail received tick cadence | p95_gap_ms | 4212 | 4212 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| MARUTI | rewired received tick cadence distribution | gap_le_1s_fraction | 0.774621 | 0.922593 | 1.19103 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.147973 |
| NESTLEIND | rewired received tick cadence | median_gap_ms | 1251 | 500 | 0.39968 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| NESTLEIND | rewired tail received tick cadence | p90_gap_ms | 5209.8 | 500 | 0.095973 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| NESTLEIND | rewired tail received tick cadence | p95_gap_ms | 6232.4 | 6232 | 0.999936 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| NESTLEIND | rewired received tick cadence distribution | gap_le_1s_fraction | 0.437565 | 0.9223 | 2.1078 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.484735 |
| NIFTYBEES | rewired received tick cadence | median_gap_ms | 749 | 500 | 0.667557 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| NIFTYBEES | rewired tail received tick cadence | p90_gap_ms | 2751.8 | 500 | 0.181699 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| NIFTYBEES | rewired tail received tick cadence | p95_gap_ms | 4467.05 | 4467 | 0.999989 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| NIFTYBEES | rewired received tick cadence distribution | gap_le_1s_fraction | 0.790702 | 0.922576 | 1.16678 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.131874 |
| ONGC | rewired received tick cadence | median_gap_ms | 750 | 500 | 0.666667 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ONGC | rewired tail received tick cadence | p90_gap_ms | 4001 | 500 | 0.124969 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ONGC | rewired tail received tick cadence | p95_gap_ms | 5002 | 5002 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ONGC | rewired received tick cadence distribution | gap_le_1s_fraction | 0.663951 | 0.922579 | 1.38953 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.258628 |
| RELIANCE | rewired received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| RELIANCE | rewired tail received tick cadence | p90_gap_ms | 1001 | 500 | 0.4995 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| RELIANCE | rewired tail received tick cadence | p95_gap_ms | 2999 | 2999 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| RELIANCE | rewired received tick cadence distribution | gap_le_1s_fraction | 0.890378 | 0.922499 | 1.03608 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.0321213 |
| SBIN | rewired received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| SBIN | rewired tail received tick cadence | p90_gap_ms | 2000 | 500 | 0.25 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| SBIN | rewired tail received tick cadence | p95_gap_ms | 4257.7 | 4258 | 1.00007 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| SBIN | rewired received tick cadence distribution | gap_le_1s_fraction | 0.825014 | 0.922585 | 1.11827 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.0975705 |
| SUNPHARMA | rewired received tick cadence | median_gap_ms | 982 | 500 | 0.509165 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| SUNPHARMA | rewired tail received tick cadence | p90_gap_ms | 4577 | 500 | 0.109242 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| SUNPHARMA | rewired tail received tick cadence | p95_gap_ms | 5484 | 5484 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| SUNPHARMA | rewired received tick cadence distribution | gap_le_1s_fraction | 0.600041 | 0.922535 | 1.53745 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.322494 |
| TCS | rewired received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| TCS | rewired tail received tick cadence | p90_gap_ms | 2000 | 500 | 0.25 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| TCS | rewired tail received tick cadence | p95_gap_ms | 4250.7 | 4251 | 1.00007 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| TCS | rewired received tick cadence distribution | gap_le_1s_fraction | 0.819414 | 0.922609 | 1.12594 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.103194 |
| TECHM | rewired received tick cadence | median_gap_ms | 1238.5 | 500 | 0.403714 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| TECHM | rewired tail received tick cadence | p90_gap_ms | 4764.2 | 500 | 0.104949 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| TECHM | rewired tail received tick cadence | p95_gap_ms | 5806.1 | 5806 | 0.999983 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| TECHM | rewired received tick cadence distribution | gap_le_1s_fraction | 0.471861 | 0.922311 | 1.95462 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.45045 |
| ULTRACEMCO | rewired received tick cadence | median_gap_ms | 2000 | 500 | 0.25 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ULTRACEMCO | rewired tail received tick cadence | p90_gap_ms | 5569.4 | 500 | 0.0897763 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ULTRACEMCO | rewired tail received tick cadence | p95_gap_ms | 6772.6 | 6773 | 1.00006 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| ULTRACEMCO | rewired received tick cadence distribution | gap_le_1s_fraction | 0.31124 | 0.922289 | 2.96328 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.611049 |
| WIPRO | rewired received tick cadence | median_gap_ms | 751 | 500 | 0.665779 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| WIPRO | rewired tail received tick cadence | p90_gap_ms | 4227 | 500 | 0.118287 | 0.5 | 2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| WIPRO | rewired tail received tick cadence | p95_gap_ms | 5142.2 | 5142 | 0.999961 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| WIPRO | rewired received tick cadence distribution | gap_le_1s_fraction | 0.601747 | 0.922573 | 1.53316 | -0.2 | 0.2 | True | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.320827 |
| HDFCBANK | rewired received tick cadence | median_gap_ms | 500 | 500 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| HDFCBANK | rewired tail received tick cadence | p90_gap_ms | 1000 | 500 | 0.5 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| HDFCBANK | rewired tail received tick cadence | p95_gap_ms | 1250 | 1250 | 1 | 0.5 | 2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | ratio |  |
| HDFCBANK | rewired received tick cadence distribution | gap_le_1s_fraction | 0.921965 | 0.937459 | 1.01681 | -0.2 | 0.2 | False | phase154_full_partition_via_phase155_phase157 | phase156_symbol_tail_cadence_smoke | absolute_delta | 0.0154949 |
| ADANIPORTS | median spread scale | median_spread_bps | 2.20726 | 2.21299 | 1.00259 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ADANIPORTS | tail spread scale | p90_spread_bps | 3.85933 | 4.40101 | 1.14036 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ADANIPORTS | displayed L1 depth scale | median_l1_depth | 131 | 806 | 6.15267 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ADANIPORTS | displayed L5 depth scale | median_l5_depth | 1088 | 6851 | 6.29688 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ADANIPORTS | L1 imbalance scale | median_abs_l1_imbalance | 0.62963 | 0.212851 | 0.338058 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ADANIPORTS | one-tick volatility scale | one_tick_return_std | 0.000441155 | 0.0001296 | 0.293773 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| AXISBANK | median spread scale | median_spread_bps | 1.51435 | 1.51669 | 1.00155 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| AXISBANK | tail spread scale | p90_spread_bps | 3.02595 | 3.76405 | 1.24392 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| AXISBANK | displayed L1 depth scale | median_l1_depth | 249 | 808 | 3.24498 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| AXISBANK | displayed L5 depth scale | median_l5_depth | 3048 | 6870 | 2.25394 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| AXISBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.549598 | 0.022409 | 0.0407734 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| AXISBANK | one-tick volatility scale | one_tick_return_std | 0.000423171 | 0.000121026 | 0.285997 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BAJAJ-AUTO | median spread scale | median_spread_bps | 2.46627 | 3.34493 | 1.35627 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BAJAJ-AUTO | tail spread scale | p90_spread_bps | 4.37443 | 4.89536 | 1.11908 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BAJAJ-AUTO | displayed L1 depth scale | median_l1_depth | 61 | 806 | 13.2131 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BAJAJ-AUTO | displayed L5 depth scale | median_l5_depth | 366 | 6852.5 | 18.7227 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BAJAJ-AUTO | L1 imbalance scale | median_abs_l1_imbalance | 0.578947 | 0 | 0 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BAJAJ-AUTO | one-tick volatility scale | one_tick_return_std | 0.00071201 | 0.000121237 | 0.170274 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BANKBEES | median spread scale | median_spread_bps | 3.33389 | 3.823 | 1.14671 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BANKBEES | tail spread scale | p90_spread_bps | 5.65504 | 5.86178 | 1.03656 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BANKBEES | displayed L1 depth scale | median_l1_depth | 403 | 800 | 1.98511 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BANKBEES | displayed L5 depth scale | median_l5_depth | 5262 | 6800 | 1.29228 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BANKBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.808031 | 0.327922 | 0.405829 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BANKBEES | one-tick volatility scale | one_tick_return_std | 0.000217665 | 0.000105674 | 0.485491 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BHARTIARTL | median spread scale | median_spread_bps | 2.09293 | 1.57693 | 0.753459 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BHARTIARTL | tail spread scale | p90_spread_bps | 3.15637 | 3.65759 | 1.1588 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BHARTIARTL | displayed L1 depth scale | median_l1_depth | 415 | 806 | 1.94217 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BHARTIARTL | displayed L5 depth scale | median_l5_depth | 3715 | 6851 | 1.84415 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BHARTIARTL | L1 imbalance scale | median_abs_l1_imbalance | 0.547826 | 0.0797721 | 0.145616 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BHARTIARTL | one-tick volatility scale | one_tick_return_std | 0.00043748 | 0.000120189 | 0.274729 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BPCL | median spread scale | median_spread_bps | 1.63921 | 1.63584 | 0.997947 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BPCL | tail spread scale | p90_spread_bps | 4.89996 | 4.88996 | 0.997959 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BPCL | displayed L1 depth scale | median_l1_depth | 2059 | 810 | 0.393395 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BPCL | displayed L5 depth scale | median_l5_depth | 19762 | 6885 | 0.348396 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BPCL | L1 imbalance scale | median_abs_l1_imbalance | 0.653486 | 0.0528053 | 0.0808055 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BPCL | one-tick volatility scale | one_tick_return_std | 0.000615309 | 0.000129686 | 0.210766 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BRITANNIA | median spread scale | median_spread_bps | 2.81756 | 3.74625 | 1.32961 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BRITANNIA | tail spread scale | p90_spread_bps | 5.59754 | 5.63021 | 1.00584 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BRITANNIA | displayed L1 depth scale | median_l1_depth | 35 | 802 | 22.9143 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BRITANNIA | displayed L5 depth scale | median_l5_depth | 406.5 | 6816 | 16.7675 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BRITANNIA | L1 imbalance scale | median_abs_l1_imbalance | 0.542036 | 0 | 0 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| BRITANNIA | one-tick volatility scale | one_tick_return_std | 0.00049004 | 0.000103935 | 0.212096 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| CIPLA | median spread scale | median_spread_bps | 2.80387 | 2.81009 | 1.00222 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| CIPLA | tail spread scale | p90_spread_bps | 4.90069 | 4.92208 | 1.00436 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| CIPLA | displayed L1 depth scale | median_l1_depth | 136 | 802 | 5.89706 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| CIPLA | displayed L5 depth scale | median_l5_depth | 1594 | 6816 | 4.27604 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| CIPLA | L1 imbalance scale | median_abs_l1_imbalance | 0.675676 | 0.568528 | 0.841421 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| CIPLA | one-tick volatility scale | one_tick_return_std | 0.000439541 | 0.000103891 | 0.236361 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| DRREDDY | median spread scale | median_spread_bps | 3.24649 | 2.43869 | 0.751177 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| DRREDDY | tail spread scale | p90_spread_bps | 4.86934 | 4.86512 | 0.999134 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| DRREDDY | displayed L1 depth scale | median_l1_depth | 271.5 | 802 | 2.95396 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| DRREDDY | displayed L5 depth scale | median_l5_depth | 2642 | 6816 | 2.57986 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| DRREDDY | L1 imbalance scale | median_abs_l1_imbalance | 0.618831 | 0.207254 | 0.334912 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| DRREDDY | one-tick volatility scale | one_tick_return_std | 0.000542243 | 0.000100334 | 0.185036 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| GOLDBEES | median spread scale | median_spread_bps | 0.857082 | 0.856267 | 0.99905 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| GOLDBEES | tail spread scale | p90_spread_bps | 2.56487 | 2.55598 | 0.996532 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| GOLDBEES | displayed L1 depth scale | median_l1_depth | 11211.5 | 800 | 0.0713553 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| GOLDBEES | displayed L5 depth scale | median_l5_depth | 95705.5 | 6800 | 0.0710513 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| GOLDBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.747425 | 0.202279 | 0.270635 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| GOLDBEES | one-tick volatility scale | one_tick_return_std | 0.000285098 | 0.000103335 | 0.362454 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HCLTECH | median spread scale | median_spread_bps | 3.25574 | 2.4614 | 0.75602 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HCLTECH | tail spread scale | p90_spread_bps | 4.26218 | 4.88698 | 1.14659 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HCLTECH | displayed L1 depth scale | median_l1_depth | 339.5 | 810 | 2.38586 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HCLTECH | displayed L5 depth scale | median_l5_depth | 4819 | 6885 | 1.42872 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HCLTECH | L1 imbalance scale | median_abs_l1_imbalance | 0.660606 | 0.293963 | 0.44499 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HCLTECH | one-tick volatility scale | one_tick_return_std | 0.000923066 | 0.000125175 | 0.135608 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HDFCBANK | median spread scale | median_spread_bps | 1.22048 | 1.22299 | 1.00206 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HDFCBANK | tail spread scale | p90_spread_bps | 2.45085 | 3.03719 | 1.23924 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HDFCBANK | displayed L1 depth scale | median_l1_depth | 1010 | 808 | 0.8 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HDFCBANK | displayed L5 depth scale | median_l5_depth | 15104 | 6868 | 0.454714 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HDFCBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.622123 | 0.572368 | 0.920024 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HDFCBANK | one-tick volatility scale | one_tick_return_std | 0.000266132 | 0.000121544 | 0.456707 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HINDUNILVR | median spread scale | median_spread_bps | 1.4103 | 1.88454 | 1.33626 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HINDUNILVR | tail spread scale | p90_spread_bps | 3.52032 | 4.20642 | 1.1949 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HINDUNILVR | displayed L1 depth scale | median_l1_depth | 188.5 | 802 | 4.25464 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HINDUNILVR | displayed L5 depth scale | median_l5_depth | 1287 | 6816 | 5.29604 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HINDUNILVR | L1 imbalance scale | median_abs_l1_imbalance | 0.627765 | 0.0730897 | 0.116428 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| HINDUNILVR | one-tick volatility scale | one_tick_return_std | 0.000449187 | 0.000105665 | 0.235235 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ICICIBANK | median spread scale | median_spread_bps | 1.41784 | 1.42577 | 1.0056 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ICICIBANK | tail spread scale | p90_spread_bps | 2.84353 | 3.53903 | 1.24459 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ICICIBANK | displayed L1 depth scale | median_l1_depth | 580 | 810 | 1.39655 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ICICIBANK | displayed L5 depth scale | median_l5_depth | 6394 | 6884 | 1.07663 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ICICIBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.618943 | 0.368771 | 0.595807 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ICICIBANK | one-tick volatility scale | one_tick_return_std | 0.00027235 | 0.000120141 | 0.441129 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| INFY | median spread scale | median_spread_bps | 1.81422 | 1.81598 | 1.00097 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| INFY | tail spread scale | p90_spread_bps | 3.66367 | 4.50825 | 1.23053 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| INFY | displayed L1 depth scale | median_l1_depth | 613 | 810 | 1.32137 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| INFY | displayed L5 depth scale | median_l5_depth | 9352 | 6885 | 0.736206 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| INFY | L1 imbalance scale | median_abs_l1_imbalance | 0.758157 | 0.1875 | 0.24731 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| INFY | one-tick volatility scale | one_tick_return_std | 0.00067843 | 0.000124183 | 0.183044 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ITBEES | median spread scale | median_spread_bps | 3.12794 | 3.11429 | 0.995637 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ITBEES | tail spread scale | p90_spread_bps | 6.29723 | 6.20399 | 0.985194 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ITBEES | displayed L1 depth scale | median_l1_depth | 134432 | 802 | 0.00596584 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ITBEES | displayed L5 depth scale | median_l5_depth | 2.15215e+06 | 6816 | 0.00316706 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ITBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.68474 | 0.740331 | 1.08119 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ITBEES | one-tick volatility scale | one_tick_return_std | 0.000841952 | 0.000102494 | 0.121734 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ITC | median spread scale | median_spread_bps | 1.78715 | 1.78604 | 0.999377 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ITC | tail spread scale | p90_spread_bps | 3.92555 | 5.32912 | 1.35755 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ITC | displayed L1 depth scale | median_l1_depth | 5559 | 800 | 0.143911 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ITC | displayed L5 depth scale | median_l5_depth | 113657 | 6800 | 0.0598291 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ITC | L1 imbalance scale | median_abs_l1_imbalance | 0.589392 | 0.509868 | 0.865075 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ITC | one-tick volatility scale | one_tick_return_std | 0.000353813 | 0.000105297 | 0.297606 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| JUNIORBEES | median spread scale | median_spread_bps | 3.60078 | 3.9655 | 1.10129 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| JUNIORBEES | tail spread scale | p90_spread_bps | 5.53578 | 6.03954 | 1.091 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| JUNIORBEES | displayed L1 depth scale | median_l1_depth | 417 | 798 | 1.91367 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| JUNIORBEES | displayed L5 depth scale | median_l5_depth | 8912 | 6784 | 0.761221 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| JUNIORBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.863238 | 0.69774 | 0.808283 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| JUNIORBEES | one-tick volatility scale | one_tick_return_std | 0.000210559 | 9.6082e-05 | 0.456319 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| KOTAKBANK | median spread scale | median_spread_bps | 2.62329 | 2.63624 | 1.00493 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| KOTAKBANK | tail spread scale | p90_spread_bps | 3.96432 | 4.03352 | 1.01745 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| KOTAKBANK | displayed L1 depth scale | median_l1_depth | 1719 | 808 | 0.470041 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| KOTAKBANK | displayed L5 depth scale | median_l5_depth | 25525 | 6870 | 0.269148 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| KOTAKBANK | L1 imbalance scale | median_abs_l1_imbalance | 0.670857 | 0.150568 | 0.224441 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| KOTAKBANK | one-tick volatility scale | one_tick_return_std | 0.000438758 | 0.00012056 | 0.274776 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| LT | median spread scale | median_spread_bps | 1.27755 | 1.50341 | 1.17679 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| LT | tail spread scale | p90_spread_bps | 2.8018 | 3.54682 | 1.26591 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| LT | displayed L1 depth scale | median_l1_depth | 106 | 806 | 7.60377 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| LT | displayed L5 depth scale | median_l5_depth | 481 | 6850 | 14.2412 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| LT | L1 imbalance scale | median_abs_l1_imbalance | 0.549296 | 0.0903955 | 0.164566 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| LT | one-tick volatility scale | one_tick_return_std | 0.000333916 | 0.000114174 | 0.341925 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| M&M | median spread scale | median_spread_bps | 1.26723 | 1.27467 | 1.00587 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| M&M | tail spread scale | p90_spread_bps | 2.86439 | 3.46674 | 1.21029 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| M&M | displayed L1 depth scale | median_l1_depth | 47 | 806 | 17.1489 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| M&M | displayed L5 depth scale | median_l5_depth | 447 | 6850 | 15.3244 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| M&M | L1 imbalance scale | median_abs_l1_imbalance | 0.676548 | 0.18612 | 0.275102 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| M&M | one-tick volatility scale | one_tick_return_std | 0.000420129 | 0.000112336 | 0.267384 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| MARUTI | median spread scale | median_spread_bps | 2.91153 | 2.93049 | 1.00651 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| MARUTI | tail spread scale | p90_spread_bps | 4.36205 | 4.36944 | 1.00169 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| MARUTI | displayed L1 depth scale | median_l1_depth | 40 | 806 | 20.15 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| MARUTI | displayed L5 depth scale | median_l5_depth | 411 | 6851 | 16.6691 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| MARUTI | L1 imbalance scale | median_abs_l1_imbalance | 0.592949 | 0.132653 | 0.223718 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| MARUTI | one-tick volatility scale | one_tick_return_std | 0.000428897 | 0.000111125 | 0.259095 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| NESTLEIND | median spread scale | median_spread_bps | 2.44069 | 2.79654 | 1.1458 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| NESTLEIND | tail spread scale | p90_spread_bps | 4.18819 | 4.87753 | 1.16459 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| NESTLEIND | displayed L1 depth scale | median_l1_depth | 349 | 802 | 2.29799 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| NESTLEIND | displayed L5 depth scale | median_l5_depth | 2850 | 6817 | 2.39193 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| NESTLEIND | L1 imbalance scale | median_abs_l1_imbalance | 0.619048 | 0.41196 | 0.665474 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| NESTLEIND | one-tick volatility scale | one_tick_return_std | 0.000651157 | 0.000100298 | 0.15403 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| NIFTYBEES | median spread scale | median_spread_bps | 1.45757 | 1.45886 | 1.00089 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| NIFTYBEES | tail spread scale | p90_spread_bps | 3.6412 | 3.62565 | 0.99573 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| NIFTYBEES | displayed L1 depth scale | median_l1_depth | 2941 | 798 | 0.271336 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| NIFTYBEES | displayed L5 depth scale | median_l5_depth | 51029.5 | 6783 | 0.132923 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| NIFTYBEES | L1 imbalance scale | median_abs_l1_imbalance | 0.803454 | 0.620915 | 0.772807 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| NIFTYBEES | one-tick volatility scale | one_tick_return_std | 0.00014983 | 8.8358e-05 | 0.589721 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ONGC | median spread scale | median_spread_bps | 1.62121 | 2.3811 | 1.46872 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ONGC | tail spread scale | p90_spread_bps | 3.6357 | 4.02818 | 1.10795 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ONGC | displayed L1 depth scale | median_l1_depth | 1042 | 810 | 0.777351 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ONGC | displayed L5 depth scale | median_l5_depth | 7000.5 | 6884 | 0.983358 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ONGC | L1 imbalance scale | median_abs_l1_imbalance | 0.612081 | 0.047619 | 0.0777987 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ONGC | one-tick volatility scale | one_tick_return_std | 0.000511555 | 0.000122298 | 0.239072 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| RELIANCE | median spread scale | median_spread_bps | 0.771159 | 1.542 | 1.99958 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| RELIANCE | tail spread scale | p90_spread_bps | 3.07882 | 3.07289 | 0.998074 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| RELIANCE | displayed L1 depth scale | median_l1_depth | 986 | 810 | 0.821501 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| RELIANCE | displayed L5 depth scale | median_l5_depth | 11881.5 | 6885 | 0.579472 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| RELIANCE | L1 imbalance scale | median_abs_l1_imbalance | 0.716704 | 0.44359 | 0.61893 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| RELIANCE | one-tick volatility scale | one_tick_return_std | 0.00020142 | 0.000120233 | 0.596925 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| SBIN | median spread scale | median_spread_bps | 1.92548 | 1.92885 | 1.00175 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| SBIN | tail spread scale | p90_spread_bps | 3.84497 | 3.83021 | 0.99616 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| SBIN | displayed L1 depth scale | median_l1_depth | 1048 | 808 | 0.770992 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| SBIN | displayed L5 depth scale | median_l5_depth | 13743.5 | 6868 | 0.499727 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| SBIN | L1 imbalance scale | median_abs_l1_imbalance | 0.648919 | 0.047619 | 0.0733821 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| SBIN | one-tick volatility scale | one_tick_return_std | 0.000389548 | 0.000120499 | 0.30933 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| SUNPHARMA | median spread scale | median_spread_bps | 1.55695 | 2.08162 | 1.33699 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| SUNPHARMA | tail spread scale | p90_spread_bps | 3.12826 | 4.14543 | 1.32515 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| SUNPHARMA | displayed L1 depth scale | median_l1_depth | 113 | 802 | 7.09735 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| SUNPHARMA | displayed L5 depth scale | median_l5_depth | 986 | 6816 | 6.91278 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| SUNPHARMA | L1 imbalance scale | median_abs_l1_imbalance | 0.61039 | 0.294872 | 0.483088 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| SUNPHARMA | one-tick volatility scale | one_tick_return_std | 0.000344815 | 9.59112e-05 | 0.278153 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| TCS | median spread scale | median_spread_bps | 1.83008 | 1.83926 | 1.00502 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| TCS | tail spread scale | p90_spread_bps | 3.21444 | 3.65551 | 1.13721 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| TCS | displayed L1 depth scale | median_l1_depth | 231 | 810 | 3.50649 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| TCS | displayed L5 depth scale | median_l5_depth | 2997 | 6885 | 2.2973 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| TCS | L1 imbalance scale | median_abs_l1_imbalance | 0.682609 | 0.00717703 | 0.0105141 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| TCS | one-tick volatility scale | one_tick_return_std | 0.000649264 | 0.000123173 | 0.189712 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| TECHM | median spread scale | median_spread_bps | 3.28655 | 3.9316 | 1.19627 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| TECHM | tail spread scale | p90_spread_bps | 4.67165 | 5.30536 | 1.13565 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| TECHM | displayed L1 depth scale | median_l1_depth | 137 | 810 | 5.91241 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| TECHM | displayed L5 depth scale | median_l5_depth | 1436 | 6886 | 4.79526 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| TECHM | L1 imbalance scale | median_abs_l1_imbalance | 0.625668 | 0.125 | 0.199786 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| TECHM | one-tick volatility scale | one_tick_return_std | 0.00086675 | 0.000124063 | 0.143136 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ULTRACEMCO | median spread scale | median_spread_bps | 2.58498 | 2.58942 | 1.00172 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ULTRACEMCO | tail spread scale | p90_spread_bps | 4.31611 | 5.1558 | 1.19455 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ULTRACEMCO | displayed L1 depth scale | median_l1_depth | 30 | 808 | 26.9333 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ULTRACEMCO | displayed L5 depth scale | median_l5_depth | 309 | 6868 | 22.2265 | 0.1 | 10 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ULTRACEMCO | L1 imbalance scale | median_abs_l1_imbalance | 0.666667 | 0.427617 | 0.641425 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| ULTRACEMCO | one-tick volatility scale | one_tick_return_std | 0.000441904 | 0.000116794 | 0.264297 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| WIPRO | median spread scale | median_spread_bps | 2.22785 | 2.24809 | 1.00908 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| WIPRO | tail spread scale | p90_spread_bps | 3.40812 | 3.90912 | 1.147 | 0.25 | 4 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| WIPRO | displayed L1 depth scale | median_l1_depth | 1427 | 810 | 0.567624 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| WIPRO | displayed L5 depth scale | median_l5_depth | 14713 | 6885 | 0.467954 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| WIPRO | L1 imbalance scale | median_abs_l1_imbalance | 0.701962 | 0.0960452 | 0.136824 | 0.25 | 4 | True | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |
| WIPRO | one-tick volatility scale | one_tick_return_std | 0.000506627 | 0.0001212 | 0.23923 | 0.1 | 10 | False | phase106_existing_non_cadence_real_anchor | phase106_existing_synthetic_anchor_profile | ratio |  |

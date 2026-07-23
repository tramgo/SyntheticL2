# Phase159 Distributional Cadence Smoke

Generated UTC: 2026-07-23T10:06:51.535090+00:00

Phase159 smoke-tests a distributional generator cadence profile built from Phase155 full-partition targets.
It allocates deterministic dense subtick gaps to median, p90, p95, and gap<=1s targets instead of pinning p95 alone.
It materializes a bounded local dense shard only. It does not run strategy replay, fills, P&L, or Azure reads.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase159_profile_id | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | Distributional cadence profile smoke-tested |
| phase159_base_profile_id | P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE | Base generator profile inherited |
| phase159_smoke_symbols | 32 | Symbols in distributional cadence smoke |
| phase159_smoke_dense_rows | 16838528 | Dense rows materialized |
| phase159_smoke_bytes | 357615839 | Compressed dense smoke bytes |
| phase159_elapsed_seconds | 52.2429 | Dense smoke elapsed seconds |
| phase158_phase157_rewire_ready | 1 | Inherited Phase157 cadence rewire readiness |
| phase158_symbols_compared | 32 | Symbols present in full rewired realism audit |
| phase158_anchor_metric_rows | 320 | Symbol/metric anchor rows compared |
| phase158_calibration_gap_rows | 39 | Rows outside Phase158 gates |
| phase158_calibration_gap_fraction | 0.121875 | Fraction of rows outside Phase158 gates |
| phase158_severe_metric_gap_count | 0 | Metrics with gap_fraction > 50% |
| phase158_cadence_gap_rows | 8 | Cadence rows outside full-partition cadence gates |
| phase158_non_cadence_gap_rows | 31 | Preserved non-cadence rows outside existing gates |
| phase158_full_rewired_realism_pass | 1 | 1 means full rewired realism audit passes |
| phase158_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase158_next_best_action | fix_phase158_remaining_distributional_cadence_depth_imbalance_gaps_before_strategy_replay | Recommended next milestone |

## Distributional Cadence Profile

| symbol | rows | trade_dates | median_gap_ms | p90_gap_ms | p95_gap_ms | gap_le_1s_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | 526144 | 22 | 1000 | 4500 | 5500 | 0.531993 |
| AXISBANK | 526400 | 22 | 501 | 2001 | 4381 | 0.75111 |
| BAJAJ-AUTO | 526144 | 22 | 1000 | 4910 | 5939 | 0.516281 |
| BANKBEES | 525824 | 22 | 999 | 1255 | 4450 | 0.751235 |
| BHARTIARTL | 526656 | 22 | 749 | 3250 | 4762 | 0.68837 |
| BPCL | 526592 | 22 | 5239 | 5239 | 6082 | 0.375585 |
| BRITANNIA | 526592 | 22 | 5923 | 5923 | 7001 | 0.328657 |
| CIPLA | 525824 | 22 | 5000 | 5000 | 5954 | 0.422465 |
| DRREDDY | 525952 | 22 | 4792 | 4792 | 5750 | 0.453855 |
| GOLDBEES | 526208 | 22 | 750 | 3999 | 5250 | 0.657032 |
| HCLTECH | 525952 | 22 | 1000 | 4500 | 5325 | 0.500766 |
| HDFCBANK | 526080 | 22 | 500 | 500 | 1250 | 0.937277 |
| HINDUNILVR | 525248 | 22 | 1000 | 4750 | 5859 | 0.563226 |
| ICICIBANK | 526016 | 22 | 500 | 1001 | 3403 | 0.876381 |
| INFY | 526400 | 22 | 500 | 2001 | 3922 | 0.81379 |
| ITBEES | 526400 | 22 | 5829 | 5829 | 6911 | 0.297416 |
| ITC | 526528 | 22 | 749 | 3753 | 4815 | 0.719544 |
| JUNIORBEES | 525376 | 22 | 999 | 3348 | 4511 | 0.750995 |
| KOTAKBANK | 525952 | 22 | 500 | 3000 | 4051 | 0.813622 |
| LT | 525952 | 22 | 500 | 1001 | 3367 | 0.87639 |
| M&M | 526528 | 22 | 501 | 1750 | 4285 | 0.813704 |
| MARUTI | 526656 | 22 | 683 | 2502 | 4212 | 0.766791 |
| NESTLEIND | 525824 | 22 | 5210 | 5210 | 6232 | 0.422459 |
| NIFTYBEES | 526784 | 22 | 749 | 2752 | 4467 | 0.782274 |
| ONGC | 526016 | 22 | 750 | 4001 | 5002 | 0.64141 |
| RELIANCE | 525696 | 22 | 500 | 1001 | 2999 | 0.876389 |
| SBIN | 525760 | 22 | 500 | 2000 | 4258 | 0.813696 |
| SUNPHARMA | 526080 | 22 | 982 | 4577 | 5484 | 0.578911 |
| TCS | 526592 | 22 | 500 | 2000 | 4251 | 0.798118 |
| TECHM | 525888 | 22 | 4764 | 4764 | 5806 | 0.453853 |
| ULTRACEMCO | 527168 | 22 | 5569 | 5569 | 6773 | 0.297415 |
| WIPRO | 527296 | 22 | 751 | 4227 | 5142 | 0.594533 |

## Rewired Gap Summary

| category | metric | anchor_source | symbol_metrics | gap_count | gap_fraction | median_synthetic_to_real_ratio | min_synthetic_to_real_ratio | max_synthetic_to_real_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L1 imbalance scale | median_abs_l1_imbalance | phase106_existing_non_cadence_real_anchor | 32 | 15 | 0.46875 | 0.272869 | 0 | 1.08119 |
| displayed L1 depth scale | median_l1_depth | phase106_existing_non_cadence_real_anchor | 32 | 7 | 0.21875 | 2.14155 | 0.00596584 | 26.9333 |
| displayed L5 depth scale | median_l5_depth | phase106_existing_non_cadence_real_anchor | 32 | 9 | 0.28125 | 1.63643 | 0.00316706 | 22.2265 |
| median spread scale | median_spread_bps | phase106_existing_non_cadence_real_anchor | 32 | 0 | 0 | 1.00498 | 0.751177 | 1.99958 |
| one-tick volatility scale | one_tick_return_std | phase106_existing_non_cadence_real_anchor | 32 | 0 | 0 | 0.265841 | 0.121734 | 0.596925 |
| rewired received tick cadence | median_gap_ms | phase154_full_partition_via_phase155_phase157 | 32 | 8 | 0.25 | 1 | 1 | 4.16467 |
| rewired received tick cadence distribution | gap_le_1s_fraction | phase154_full_partition_via_phase155_phase157 | 32 | 0 | 0 | 0.975299 | 0.95073 | 1.01661 |
| rewired tail received tick cadence | p90_gap_ms | phase154_full_partition_via_phase155_phase157 | 32 | 0 | 0 | 1 | 0.5 | 1.00009 |
| rewired tail received tick cadence | p95_gap_ms | phase154_full_partition_via_phase155_phase157 | 32 | 0 | 0 | 1 | 0.999895 | 1.00007 |
| tail spread scale | p90_spread_bps | phase106_existing_non_cadence_real_anchor | 32 | 0 | 0 | 1.13643 | 0.985194 | 1.35755 |

## Remediation Queue

| priority | metric | work_item | gap_count | gap_fraction | rationale |
| --- | --- | --- | --- | --- | --- |
| 1 | median_abs_l1_imbalance | revisit_l1_imbalance_floor_and_side_skew_model | 15 | 0.46875 | Existing imbalance gates are preserved and remain a broad non-cadence blocker. |
| 2 | median_l5_depth | revisit_symbol_depth_scale_overrides_with_full_partition_non_cadence_anchors | 9 | 0.28125 | Existing non-cadence depth gates are preserved and still show symbol failures. |
| 3 | median_gap_ms | calibrate_symbol_median_cadence_without_breaking_p95_targets | 8 | 0.25 | Phase156 pins p95 but keeps median gaps at the dense 500ms baseline for slower symbols. |
| 4 | median_l1_depth | revisit_symbol_depth_scale_overrides_with_full_partition_non_cadence_anchors | 7 | 0.21875 | Existing non-cadence depth gates are preserved and still show symbol failures. |

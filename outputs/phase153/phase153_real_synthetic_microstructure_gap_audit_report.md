# Phase153 Real-vs-synthetic Microstructure Gap Audit

Generated UTC: 2026-07-23T09:07:20.986985+00:00

Phase153 compares bounded Phase152 full-partition real microstructure profiles against Phase106 calibrated synthetic anchor metrics, and audits whether older sampled real-anchor cadence profiles may be biased.
It is diagnostic-only: no strategy, no replay unlock, no P&L, no Azure I/O.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase153_overlap_symbols | 6 | Symbols compared between Phase152 full real profiles and Phase106 synthetic anchor |
| phase153_real_synthetic_gap_rows | 18 | Real-vs-synthetic metric comparison rows |
| phase153_real_synthetic_gap_flag_rows | 11 | Real-vs-synthetic rows outside the 0.80-1.25 ratio band or missing |
| phase153_sample_bias_rows | 12 | Phase152 full-partition vs Phase106 sampled-anchor comparison rows |
| phase153_sample_bias_flag_rows | 3 | Sample-bias rows outside the 0.50-2.00 sampled/full ratio band or missing |
| phase153_phase106_severe_metric_gap_count | 1 | Inherited Phase106 severe metric gap count |
| phase153_recommendation_rows | 2 | Generated diagnostic recommendations |
| phase153_strategy_replay_allowed | 0 | Gap audit does not unlock strategy replay |
| phase153_next_best_action | recompute_real_anchor_cadence_profiles_from_full_partitions_after_phase148_downloads | Recommended next milestone |

## Diagnostic Recommendations

| recommendation_id | priority | evidence | action |
| --- | --- | --- | --- |
| P153_RECOMPUTE_REAL_CADENCE_ANCHORS_FROM_FULL_PARTITIONS | high | 3 profiled symbols show older sampled p95 gap much higher than Phase152 full partition p95 gap. | Use Phase152-style full-partition DuckDB profiles for future cadence calibration before changing generator cadence parameters. |
| P153_KEEP_REPLAY_CLOSED_USE_GAPS_FOR_GENERATOR_DIAGNOSTICS | high | tail cadence synthetic_low_vs_real rows=6; displayed depth synthetic_high_vs_real proxy rows=1. | Treat gaps as generator diagnostics only; do not open strategy replay or tune strategies to these selected partitions. |

## Real-vs-synthetic Gap Matrix

| symbol | category | real_metric | synthetic_metric | real_phase152_value | synthetic_phase106_value | synthetic_to_real_ratio | gap_flag | metric_basis |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | received_tick_cadence_median_gap | median_gap_ms | median_gap_ms | 1000 | 500 | 0.5 | synthetic_low_vs_real | phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor |
| ADANIPORTS | received_tick_cadence_tail_gap | p95_gap_ms | p95_gap_ms | 5500 | 792 | 0.144 | synthetic_low_vs_real | phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor |
| ADANIPORTS | displayed_l1_depth_scale_proxy | avg_best_bid_qty_plus_avg_best_ask_qty | median_l1_depth | 267.903 | 806 | 3.00855 | synthetic_high_vs_real | proxy_only_depth_aggregation_differs |
| HCLTECH | received_tick_cadence_median_gap | median_gap_ms | median_gap_ms | 500 | 500 | 1 | within_band | phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor |
| HCLTECH | received_tick_cadence_tail_gap | p95_gap_ms | p95_gap_ms | 4158.8 | 792 | 0.19044 | synthetic_low_vs_real | phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor |
| HCLTECH | displayed_l1_depth_scale_proxy | avg_best_bid_qty_plus_avg_best_ask_qty | median_l1_depth | 732.341 | 810 | 1.10604 | within_band | proxy_only_depth_aggregation_differs |
| HDFCBANK | received_tick_cadence_median_gap | median_gap_ms | median_gap_ms | 500 | 500 | 1 | within_band | phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor |
| HDFCBANK | received_tick_cadence_tail_gap | p95_gap_ms | p95_gap_ms | 1250 | 792 | 0.6336 | synthetic_low_vs_real | phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor |
| HDFCBANK | displayed_l1_depth_scale_proxy | avg_best_bid_qty_plus_avg_best_ask_qty | median_l1_depth | 2056.85 | 808 | 0.392833 | synthetic_low_vs_real | proxy_only_depth_aggregation_differs |
| INFY | received_tick_cadence_median_gap | median_gap_ms | median_gap_ms | 500 | 500 | 1 | within_band | phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor |
| INFY | received_tick_cadence_tail_gap | p95_gap_ms | p95_gap_ms | 2627.1 | 792 | 0.301473 | synthetic_low_vs_real | phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor |
| INFY | displayed_l1_depth_scale_proxy | avg_best_bid_qty_plus_avg_best_ask_qty | median_l1_depth | 1258.73 | 810 | 0.643508 | synthetic_low_vs_real | proxy_only_depth_aggregation_differs |
| RELIANCE | received_tick_cadence_median_gap | median_gap_ms | median_gap_ms | 500 | 500 | 1 | within_band | phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor |
| RELIANCE | received_tick_cadence_tail_gap | p95_gap_ms | p95_gap_ms | 4324 | 792 | 0.183164 | synthetic_low_vs_real | phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor |
| RELIANCE | displayed_l1_depth_scale_proxy | avg_best_bid_qty_plus_avg_best_ask_qty | median_l1_depth | 1351.14 | 810 | 0.599493 | synthetic_low_vs_real | proxy_only_depth_aggregation_differs |
| TCS | received_tick_cadence_median_gap | median_gap_ms | median_gap_ms | 500 | 500 | 1 | within_band | phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor |
| TCS | received_tick_cadence_tail_gap | p95_gap_ms | p95_gap_ms | 1250 | 792 | 0.6336 | synthetic_low_vs_real | phase152_full_local_partition_vs_phase106_calibrated_synthetic_anchor |
| TCS | displayed_l1_depth_scale_proxy | avg_best_bid_qty_plus_avg_best_ask_qty | median_l1_depth | 655.795 | 810 | 1.23514 | within_band | proxy_only_depth_aggregation_differs |

## Phase152 vs Phase106 Real Sample Bias

| symbol | metric | phase152_full_partition_value | phase106_sampled_anchor_value | sampled_to_full_ratio | sample_bias_flag | interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | median_gap_ms | 1000 | 1000 | 1 | within_band | no_large_sample_bias_flag |
| ADANIPORTS | p95_gap_ms | 5500 | 451864 | 82.1572 | sampled_high_vs_full | older_sampled_anchor_may_overstate_tail_cadence_gap |
| HCLTECH | median_gap_ms | 500 | 500 | 1 | within_band | no_large_sample_bias_flag |
| HCLTECH | p95_gap_ms | 4158.8 | 437736 | 105.255 | sampled_high_vs_full | older_sampled_anchor_may_overstate_tail_cadence_gap |
| HDFCBANK | median_gap_ms | 500 | 499 | 0.998 | within_band | no_large_sample_bias_flag |
| HDFCBANK | p95_gap_ms | 1250 | 1250 | 1 | within_band | no_large_sample_bias_flag |
| INFY | median_gap_ms | 500 | 500 | 1 | within_band | no_large_sample_bias_flag |
| INFY | p95_gap_ms | 2627.1 | 1775 | 0.67565 | within_band | no_large_sample_bias_flag |
| RELIANCE | median_gap_ms | 500 | 500 | 1 | within_band | no_large_sample_bias_flag |
| RELIANCE | p95_gap_ms | 4324 | 440431 | 101.857 | sampled_high_vs_full | older_sampled_anchor_may_overstate_tail_cadence_gap |
| TCS | median_gap_ms | 500 | 499 | 0.998 | within_band | no_large_sample_bias_flag |
| TCS | p95_gap_ms | 1250 | 1001 | 0.8008 | within_band | no_large_sample_bias_flag |

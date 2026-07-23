# Phase162 Phase159 Full-year Materialization Audit

Generated UTC: 2026-07-23T10:37:17.217748+00:00

Phase162 materializes the Phase159 distributional cadence profile across the local compact full-year synthetic lake.
It reruns cadence and generated non-cadence realism checks from local Parquet only. It does not stream Azure files, run strategy replay, fills, P&L, or profitability claims.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase162_profile_id | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | Distributional cadence profile materialized |
| phase162_requested_max_months | 0 | 0 means all local compact months |
| phase162_months_materialized | 12 | Synthetic months materialized locally |
| phase162_symbols_materialized | 32 | Symbols materialized |
| phase162_partition_files | 384 | Dense partition files written |
| phase162_expected_partition_files | 384 | Expected month/symbol shards from observed scope |
| phase162_missing_partition_files | 0 | Missing month/symbol shards |
| phase162_dense_rows | 192786816 | Dense rows materialized |
| phase162_dense_bytes | 4141341739 | Compressed dense bytes |
| phase162_elapsed_seconds | 610.819 | Materialization and audit elapsed seconds |
| phase162_combined_anchor_metric_rows | 320 | Combined cadence plus generated non-cadence rows |
| phase162_combined_gap_rows | 12 | Combined rows outside gates |
| phase162_combined_gap_fraction | 0.0375 | Combined full-year gap fraction |
| phase162_combined_severe_metric_gap_count | 0 | Combined metrics with gap_fraction > 0.50 |
| phase162_cadence_gap_rows | 8 | Cadence gaps from full-year distributional audit |
| phase162_generated_noncadence_gap_rows | 4 | Generated non-cadence gaps from full-year parquet |
| phase162_full_year_realism_audit_pass | 1 | 1 means full-year materialization/audit passes |
| phase162_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase162_azure_read_policy | forbidden_for_analysis_download_first_then_local | No Python direct Azure scanning in this phase |
| phase162_next_best_action | review_full_year_materialization_then_prepare_synthetic_only_replay_preflight_if_accepted | Recommended next milestone |

## Combined Metric Gate

| metric_family | category | metric | symbol_metrics | gap_count | gap_fraction | median_synthetic_to_real_ratio | min_synthetic_to_real_ratio | max_synthetic_to_real_ratio | evidence_source | metric_gate_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cadence | rewired received tick cadence | median_gap_ms | 32 | 8 | 0.25 | 1 | 1 | 4.16467 | phase159_distributional_generated_cadence | 1 |
| generated_non_cadence | one-tick volatility scale | one_tick_return_std | 32 | 4 | 0.125 | 0.192309 | 0.077689 | 0.844861 | phase160_generated_phase159_parquet | 1 |
| cadence | rewired received tick cadence distribution | gap_le_1s_fraction | 32 | 0 | 0 | 0.975304 | 0.950769 | 1.01662 | phase159_distributional_generated_cadence | 1 |
| generated_non_cadence | L1 imbalance scale | median_abs_l1_imbalance | 32 | 0 | 0 | 0.634204 | 0.270734 | 1.7549 | phase160_generated_phase159_parquet | 1 |
| generated_non_cadence | displayed L1 depth scale | median_l1_depth | 32 | 0 | 0 | 1.35896 | 0.271336 | 7.09735 | phase160_generated_phase159_parquet | 1 |
| generated_non_cadence | displayed L5 depth scale | median_l5_depth | 32 | 0 | 0 | 0.998932 | 0.132923 | 6.91278 | phase160_generated_phase159_parquet | 1 |
| generated_non_cadence | median spread scale | median_spread_bps | 32 | 0 | 0 | 1.00498 | 0.751177 | 1.99958 | phase160_generated_phase159_parquet | 1 |
| cadence | rewired tail received tick cadence | p90_gap_ms | 32 | 0 | 0 | 1 | 0.5 | 1.00009 | phase159_distributional_generated_cadence | 1 |
| generated_non_cadence | tail spread scale | p90_spread_bps | 32 | 0 | 0 | 1.13643 | 0.985194 | 1.35755 | phase160_generated_phase159_parquet | 1 |
| cadence | rewired tail received tick cadence | p95_gap_ms | 32 | 0 | 0 | 1 | 0.999895 | 1.00007 | phase159_distributional_generated_cadence | 1 |

## Cadence Gap Summary

| category | metric | anchor_source | symbol_metrics | gap_count | gap_fraction | median_synthetic_to_real_ratio | min_synthetic_to_real_ratio | max_synthetic_to_real_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rewired received tick cadence | median_gap_ms | phase154_full_partition_via_phase155_phase157 | 32 | 8 | 0.25 | 1 | 1 | 4.16467 |
| rewired received tick cadence distribution | gap_le_1s_fraction | phase154_full_partition_via_phase155_phase157 | 32 | 0 | 0 | 0.975304 | 0.950769 | 1.01662 |
| rewired tail received tick cadence | p90_gap_ms | phase154_full_partition_via_phase155_phase157 | 32 | 0 | 0 | 1 | 0.5 | 1.00009 |
| rewired tail received tick cadence | p95_gap_ms | phase154_full_partition_via_phase155_phase157 | 32 | 0 | 0 | 1 | 0.999895 | 1.00007 |

## Generated Non-cadence Gap Summary

| category | metric | symbol_metrics | gap_count | gap_fraction | median_synthetic_to_real_ratio | min_synthetic_to_real_ratio | max_synthetic_to_real_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L1 imbalance scale | median_abs_l1_imbalance | 32 | 0 | 0 | 0.634204 | 0.270734 | 1.7549 |
| displayed L1 depth scale | median_l1_depth | 32 | 0 | 0 | 1.35896 | 0.271336 | 7.09735 |
| displayed L5 depth scale | median_l5_depth | 32 | 0 | 0 | 0.998932 | 0.132923 | 6.91278 |
| median spread scale | median_spread_bps | 32 | 0 | 0 | 1.00498 | 0.751177 | 1.99958 |
| one-tick volatility scale | one_tick_return_std | 32 | 4 | 0.125 | 0.192309 | 0.077689 | 0.844861 |
| tail spread scale | p90_spread_bps | 32 | 0 | 0 | 1.13643 | 0.985194 | 1.35755 |

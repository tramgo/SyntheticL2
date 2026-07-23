# Phase161 Combined Realism Handoff Gate

Generated UTC: 2026-07-23T10:14:51.908887+00:00

Phase161 combines Phase159 distributional cadence evidence with Phase160 generated non-cadence evidence.
It decides whether the bounded generated shard is ready for broader materialization/audit. It does not open strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase161_phase159_full_rewired_realism_pass | 1 | Inherited Phase159 Phase158-style pass |
| phase161_phase160_generated_noncadence_realism_pass | 1 | Inherited Phase160 generated non-cadence pass |
| phase161_combined_symbols | 32 | Symbols in combined bounded handoff |
| phase161_combined_anchor_metric_rows | 320 | Combined cadence plus generated non-cadence rows |
| phase161_combined_gap_rows | 8 | Combined rows outside gates |
| phase161_combined_gap_fraction | 0.025 | Combined bounded gap fraction |
| phase161_combined_severe_metric_gap_count | 0 | Combined metrics with gap_fraction > 0.50 |
| phase161_cadence_gap_rows | 8 | Cadence gaps from Phase159 distributional audit |
| phase161_generated_noncadence_gap_rows | 0 | Generated non-cadence gaps from Phase160 audit |
| phase161_bounded_realism_handoff_pass | 1 | 1 means bounded realism handoff gate passes |
| phase161_smoke_months_materialized | 1 | Synthetic months materialized in current bounded smoke |
| phase161_broader_materialization_required | 1 | 1 means all-12-month materialization still required |
| phase161_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase161_next_best_action | materialize_phase159_distributional_profile_all_12_months_then_rerun_combined_audit | Recommended next milestone |

## Combined Metric Gate

| metric_family | category | metric | symbol_metrics | gap_count | gap_fraction | median_synthetic_to_real_ratio | min_synthetic_to_real_ratio | max_synthetic_to_real_ratio | evidence_source | metric_gate_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cadence | rewired received tick cadence | median_gap_ms | 32 | 8 | 0.25 | 1 | 1 | 4.16467 | phase159_distributional_generated_cadence | 1 |
| cadence | rewired received tick cadence distribution | gap_le_1s_fraction | 32 | 0 | 0 | 0.975299 | 0.95073 | 1.01661 | phase159_distributional_generated_cadence | 1 |
| generated_non_cadence | L1 imbalance scale | median_abs_l1_imbalance | 32 | 0 | 0 | 0.638103 | 0.270734 | 1.75028 | phase160_generated_phase159_parquet | 1 |
| generated_non_cadence | displayed L1 depth scale | median_l1_depth | 32 | 0 | 0 | 1.32867 | 0.265896 | 6.93805 | phase160_generated_phase159_parquet | 1 |
| generated_non_cadence | displayed L5 depth scale | median_l5_depth | 32 | 0 | 0 | 0.978391 | 0.130258 | 6.75862 | phase160_generated_phase159_parquet | 1 |
| generated_non_cadence | median spread scale | median_spread_bps | 32 | 0 | 0 | 1.00132 | 0.749184 | 1.99357 | phase160_generated_phase159_parquet | 1 |
| generated_non_cadence | one-tick volatility scale | one_tick_return_std | 32 | 0 | 0 | 0.260655 | 0.106275 | 1.22717 | phase160_generated_phase159_parquet | 1 |
| cadence | rewired tail received tick cadence | p90_gap_ms | 32 | 0 | 0 | 1 | 0.5 | 1.00009 | phase159_distributional_generated_cadence | 1 |
| generated_non_cadence | tail spread scale | p90_spread_bps | 32 | 0 | 0 | 0.768782 | 0.340354 | 1.02287 | phase160_generated_phase159_parquet | 1 |
| cadence | rewired tail received tick cadence | p95_gap_ms | 32 | 0 | 0 | 1 | 0.999895 | 1.00007 | phase159_distributional_generated_cadence | 1 |

## Broader Materialization Plan

| priority | work_item | current_smoke_months | current_smoke_symbols | current_smoke_rows | current_smoke_bytes | estimated_12m_rows | estimated_12m_compressed_bytes | acceptance_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | materialize_phase159_distributional_profile_all_12_months | 1 | 32 | 16838528 | 357615839 | 202062336 | 4291390068 | All 12 synthetic months materialized locally with P159 distributional cadence profile and no missing symbol/month shards. |
| 2 | rerun_phase159_phase160_style_audits_on_broader_materialization | 1 | 32 | 16838528 | 357615839 | 202062336 | 4291390068 | Combined cadence and generated non-cadence gap fraction remains <=0.25 with zero severe metric gaps across broader materialization. |
| 3 | only_then_prepare_synthetic_only_strategy_replay_preflight | 1 | 32 | 16838528 | 357615839 | 202062336 | 4291390068 | Replay preflight may be considered only after broader materialization/audit passes; this phase itself keeps replay closed. |

# Phase 49 Dense Tick-Rate Expansion Calibration

Generated UTC: 2026-07-16T15:17:58.948242+00:00

This phase turns up the synthetic tick-rate faucet for a controlled dense raw-L2 shard, measures compression and throughput, and estimates the multiplier required for the 80GB-class dense lake.
It is a dense-generation calibration milestone, not strategy acceptance evidence.

## Dense Expansion Summary

| metric | value | description |
| --- | --- | --- |
| phase49_dense_shard_symbols | HDFCBANK | Symbols included in dense calibration shard |
| phase49_dense_multiplier | 64 | Dense subticks generated per source raw event |
| phase49_source_rows_densified | 94110 | Source compact-raw rows densified |
| phase49_dense_rows_materialized | 6023040 | Dense raw rows materialized |
| phase49_dense_partition_files | 12 | Dense shard parquet files written |
| phase49_dense_bytes | 90102511 | Compressed dense shard bytes |
| phase49_dense_bytes_per_row | 14.9596 | Measured compressed dense bytes per row |
| phase49_elapsed_seconds | 15.6136 | Dense shard materialization elapsed seconds |
| phase49_rows_per_second | 385756 | Dense materialization throughput |
| phase49_target_dense_raw_gb | 83.24 | Dense raw target size |
| phase49_estimated_rows_for_target_dense_lake | 5.97463e+09 | Rows implied by target GB at measured dense compression |
| phase49_estimated_full_universe_multiplier_for_target | 1983.41 | Full-universe source-row multiplier implied by target dense size |
| phase49_estimated_hours_for_target_at_measured_rate | 4.30225 | Rough runtime estimate for target rows at measured shard throughput |
| phase49_available_disk_gb | 169.913 | Free disk after dense shard |
| phase49_dense_output_root | raw_synthetic_l2_dense_phase49_hdfcbank_x64 | Local dense shard root; ignored by Git |
| phase49_full_80gb_dense_lake_materialized | 0 | 80GB-class dense full-universe lake not yet materialized |
| phase49_synthetic_full_year_acceptance_ready | 0 | Dense generation calibration is storage/input evidence, not strategy acceptance |

## Dense Shard Inventory

| trade_month | symbol | source_rows | dense_rows | multiplier | file_path | bytes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | HDFCBANK | 8220 | 526080 | 64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | 7746199 |
| 2026-02 | HDFCBANK | 7476 | 478464 | 64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64\trade_month=2026-02\symbol=HDFCBANK\part-00000.parquet | 7252358 |
| 2026-03 | HDFCBANK | 8220 | 526080 | 64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64\trade_month=2026-03\symbol=HDFCBANK\part-00000.parquet | 7781793 |
| 2026-04 | HDFCBANK | 8212 | 525568 | 64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64\trade_month=2026-04\symbol=HDFCBANK\part-00000.parquet | 7785363 |
| 2026-05 | HDFCBANK | 7848 | 502272 | 64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64\trade_month=2026-05\symbol=HDFCBANK\part-00000.parquet | 7516891 |
| 2026-06 | HDFCBANK | 8198 | 524672 | 64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64\trade_month=2026-06\symbol=HDFCBANK\part-00000.parquet | 7724067 |
| 2026-07 | HDFCBANK | 8587 | 549568 | 64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64\trade_month=2026-07\symbol=HDFCBANK\part-00000.parquet | 8029165 |
| 2026-08 | HDFCBANK | 7841 | 501824 | 64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64\trade_month=2026-08\symbol=HDFCBANK\part-00000.parquet | 7459772 |
| 2026-09 | HDFCBANK | 8208 | 525312 | 64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64\trade_month=2026-09\symbol=HDFCBANK\part-00000.parquet | 7872523 |
| 2026-10 | HDFCBANK | 8212 | 525568 | 64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64\trade_month=2026-10\symbol=HDFCBANK\part-00000.parquet | 7769526 |
| 2026-11 | HDFCBANK | 7858 | 502912 | 64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64\trade_month=2026-11\symbol=HDFCBANK\part-00000.parquet | 7523741 |
| 2026-12 | HDFCBANK | 5230 | 334720 | 64 | raw_synthetic_l2_dense_phase49_hdfcbank_x64\trade_month=2026-12\symbol=HDFCBANK\part-00000.parquet | 5641113 |

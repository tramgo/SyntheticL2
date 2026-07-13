# Phase 8 Retail Feed Emulator Report

Generated UTC: 2026-07-13T14:55:05.712002+00:00

## Scope

This phase emulates retail receive-feed effects over synthetic L2 book states.
Latency profiles are test profiles, not measured Zerodha production latencies.

## Feed Profile Validation

| feed_profile | observed_rows | source_rows | source_kept_rows | dropped_rows | duplicate_rows | drop_fraction | duplicate_fraction | median_latency_ms | p95_latency_ms | p99_latency_ms | disconnect_gap_rows | out_of_order_injected_rows | receive_order_violation_rows | symbols |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| disconnect_scenario | 447546 | 453600 | 445545 | 8055 | 2001 | 0.017757936507936507 | 0.0044911288422044915 | 200.0 | 6100.0 | 16500.0 | 4152 | 7944 | 0 | 32 |
| good_retail | 453613 | 453600 | 453098 | 502 | 515 | 0.0011067019400352734 | 0.0011366194509796997 | 50.0 | 100.0 | 150.0 | 0 | 511 | 0 | 32 |
| ideal_research | 453600 | 453600 | 453600 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 32 |
| normal_retail | 453050 | 453600 | 452025 | 1575 | 1025 | 0.003472222222222222 | 0.0022675736961451248 | 200.0 | 400.0 | 1300.0 | 0 | 1640 | 0 | 32 |
| stressed_retail | 451230 | 453600 | 448132 | 5468 | 3098 | 0.012054673721340389 | 0.00691314166361697 | 400.0 | 2100.0 | 6550.0 | 1032 | 5466 | 0 | 32 |

## Outputs

- `retail_feed_observations.parquet`
- `retail_feed_dropped_events.csv`
- `feed_profile_summary.csv`
- `retail_feed_manifest.json`

# Phase 8 Retail Feed Emulator Report

Generated UTC: 2026-07-13T20:32:32.228171+00:00

## Scope

This phase emulates retail receive-feed effects over synthetic L2 book states.
Latency profiles are test profiles, not measured Zerodha production latencies.

## Feed Profile Validation

| feed_profile | observed_rows | source_rows | source_kept_rows | dropped_rows | duplicate_rows | drop_fraction | duplicate_fraction | median_latency_ms | p95_latency_ms | p99_latency_ms | disconnect_gap_rows | out_of_order_injected_rows | receive_order_violation_rows | symbols |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| disconnect_scenario | 447662 | 453600 | 445547 | 8053 | 2115 | 0.01775352733686067 | 0.00474697394438746 | 200.0 | 6245.799999999814 | 16600.0 | 4237 | 7970 | 0 | 32 |
| good_retail | 453581 | 453600 | 453048 | 552 | 533 | 0.001216931216931217 | 0.0011764757818156133 | 50.0 | 100.0 | 150.0 | 0 | 553 | 0 | 32 |
| ideal_research | 453600 | 453600 | 453600 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0 | 0 | 0 | 32 |
| normal_retail | 453126 | 453600 | 452042 | 1558 | 1084 | 0.0034347442680776013 | 0.0023980072648116767 | 200.0 | 400.0 | 1300.0 | 0 | 1644 | 0 | 32 |
| stressed_retail | 451259 | 453600 | 448213 | 5387 | 3046 | 0.01187610229276896 | 0.006795876067851669 | 400.0 | 2150.0 | 6600.0 | 1097 | 5375 | 0 | 32 |

## Outputs

- `retail_feed_observations.parquet`
- `retail_feed_dropped_events.csv`
- `feed_profile_summary.csv`
- `retail_feed_manifest.json`

# Phase152 Real L2 Microstructure Profile

Generated UTC: 2026-07-23T09:03:02.364490+00:00

Phase152 profiles bounded local real L2 partitions for update cadence, tick gaps, L1 spread sanity, and visible depth-level-5 presence.
It is diagnostics-only: no signals, no order-arrival stream, no fills, no P&L, no Azure I/O, and no replay unlock.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase152_catalog_db_exists | 1 | Phase150 DuckDB catalog database exists locally |
| phase152_profile_partitions | 6 | Bounded date/symbol partitions profiled |
| phase152_failed_partition_profiles | 0 | Partition profile queries failed |
| phase152_total_profile_elapsed_seconds | 10.3129 | Total elapsed seconds across profile queries |
| phase152_max_profile_elapsed_seconds | 2.7945 | Slowest bounded profile query elapsed seconds |
| phase152_min_ticks_per_second | 0.608848 | Minimum observed tick/update rate among profiled partitions |
| phase152_max_p95_gap_ms | 5500 | Maximum p95 inter-update gap among profiled partitions |
| phase152_min_l1_book_valid_fraction | 0.999928 | Minimum valid L1 book fraction among profiled partitions |
| phase152_min_depth_level_5_present_fraction | 0.999928 | Minimum visible level-5 presence among profiled partitions |
| phase152_strategy_replay_allowed | 0 | Microstructure profiling does not unlock strategy replay |
| phase152_next_best_action | use_profiles_for_real_anchor_diagnostics_after_phase148_downloads_not_strategy_replay | Recommended next milestone |

## Profile Partitions

| trade_date | exchange | symbol | parquet_files | bytes | selection_reason |
| --- | --- | --- | --- | --- | --- |
| 2026-07-13 | NSE | ADANIPORTS | 1569 | 54744007 | phase151_benchmark_partition |
| 2026-07-13 | NSE | HCLTECH | 1569 | 56185830 | top_byte_partition_from_phase150_catalog |
| 2026-07-13 | NSE | HDFCBANK | 1569 | 56719345 | phase151_benchmark_partition |
| 2026-07-13 | NSE | INFY | 1569 | 56702770 | top_byte_partition_from_phase150_catalog |
| 2026-07-13 | NSE | RELIANCE | 1569 | 55637533 | phase151_benchmark_partition |
| 2026-07-13 | NSE | TCS | 1569 | 56845524 | phase151_benchmark_partition |

## Microstructure Profiles

| trade_date | exchange | symbol | selection_reason | parquet_files | bytes | rows | min_received_ms | max_received_ms | observed_seconds | ticks_per_second | median_gap_ms | p90_gap_ms | p95_gap_ms | gap_le_100ms_fraction | gap_le_500ms_fraction | gap_le_1s_fraction | gap_gt_5s_fraction | min_last_price | max_last_price | avg_l1_spread_abs | median_l1_spread_abs | l1_book_valid_fraction | depth_level_5_present_fraction | avg_best_bid_qty | avg_best_ask_qty |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-13 | NSE | ADANIPORTS | phase151_benchmark_partition | 1569 | 54744007 | 13886 | 1.78391e+12 | 1.78394e+12 | 22807 | 0.608848 | 1000 | 4556.6 | 5500 | 0.185078 | 0.333069 | 0.546306 | 0.0733112 | 1807.2 | 1825.6 | 0.419602 | 0.4 | 0.999928 | 0.999928 | 167.233 | 100.67 |
| 2026-07-13 | NSE | HCLTECH | top_byte_partition_from_phase150_catalog | 1569 | 56185830 | 29266 | 1.78391e+12 | 1.78394e+12 | 22775.2 | 1.28499 | 500 | 1250 | 4158.8 | 0.242637 | 0.561334 | 0.874462 | 0.0166405 | 1162 | 1236.9 | 0.329044 | 0.3 | 0.999966 | 0.999966 | 313.83 | 418.511 |
| 2026-07-13 | NSE | HDFCBANK | phase151_benchmark_partition | 1569 | 56719345 | 35959 | 1.78391e+12 | 1.78394e+12 | 22775.1 | 1.57887 | 500 | 1000 | 1250 | 0.250202 | 0.590283 | 0.921939 | 0.0058956 | 811 | 821.9 | 0.119195 | 0.1 | 0.999972 | 0.999972 | 909.321 | 1147.53 |
| 2026-07-13 | NSE | INFY | top_byte_partition_from_phase150_catalog | 1569 | 56702770 | 34511 | 1.78391e+12 | 1.78394e+12 | 22775.2 | 1.51529 | 500 | 1000 | 2627.1 | 0.248472 | 0.581264 | 0.912173 | 0.0074469 | 1057.1 | 1114.8 | 0.233317 | 0.2 | 0.999971 | 0.999971 | 448.574 | 810.152 |
| 2026-07-13 | NSE | RELIANCE | phase151_benchmark_partition | 1569 | 55637533 | 26056 | 1.78391e+12 | 1.78394e+12 | 22774.5 | 1.14409 | 500 | 2001 | 4324 | 0.236683 | 0.535846 | 0.830097 | 0.023603 | 1295.1 | 1306.3 | 0.196757 | 0.2 | 0.999962 | 0.999962 | 827.2 | 523.941 |
| 2026-07-13 | NSE | TCS | phase151_benchmark_partition | 1569 | 56845524 | 36467 | 1.78391e+12 | 1.78394e+12 | 22774.5 | 1.60122 | 500 | 1000 | 1250 | 0.250583 | 0.590589 | 0.924507 | 0.00521019 | 2069.6 | 2204.9 | 0.388431 | 0.4 | 0.999973 | 0.999973 | 268.184 | 387.611 |

## Profile Timing Ledger

| trade_date | exchange | symbol | status | elapsed_seconds | error |
| --- | --- | --- | --- | --- | --- |
| 2026-07-13 | NSE | ADANIPORTS | completed | 0.899766 |  |
| 2026-07-13 | NSE | HCLTECH | completed | 0.99269 |  |
| 2026-07-13 | NSE | HDFCBANK | completed | 1.36475 |  |
| 2026-07-13 | NSE | INFY | completed | 1.91966 |  |
| 2026-07-13 | NSE | RELIANCE | completed | 2.34157 |  |
| 2026-07-13 | NSE | TCS | completed | 2.7945 |  |

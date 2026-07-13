# Phase 10 Storage Size Estimate Report

Generated UTC: 2026-07-13T15:15:08.675675+00:00

## Interpretation

Parquet/Zstandard remains the durable high-volume storage format. DuckDB remains the local query layer.
The raw source-file footprint is measured from many tiny real sample files and includes file-container overhead; compact Parquet is the better planning basis.
All forward projections are evidence-labelled estimates from the one-day real sample and current Phase 9 Parquet products, not capacity guarantees.

## Measured Footprint

| layer | rows | file_bytes | bytes_per_row | size_mb | evidence_scope |
| --- | --- | --- | --- | --- | --- |
| real_raw_source_files | 620853 | 1764005784 | 2841.2615933240236 | 1682.287010192871 | measured_real_sample_raw_l2_tiny_files |
| real_compact_ticks | 620853 | 41641489 | 67.07141465048892 | 39.71241855621338 | measured_real_sample_compact_parquet |
| tier_a_raw_synthetic_events | 2276143 | 16129601 | 7.086374186507614 | 15.382386207580566 | measured_current_synthetic_phase9 |
| tier_b_compact_l2_state | 2259039 | 165943933 | 73.45775482406457 | 158.25646686553955 | measured_current_synthetic_phase9 |
| tier_c_features_5m | 2259039 | 128897765 | 57.058671851172114 | 122.92648792266846 | measured_current_synthetic_phase9 |

## Real Sample Per-Symbol Summary

| stat | real_events_per_ticker_day | raw_source_bytes_per_event | compact_parquet_bytes_per_event | event_rate_per_second |
| --- | --- | --- | --- | --- |
| min | 8386.0 | 1558.8209614171717 | 58.07216113343202 | 0.3681906301938709 |
| median | 18612.5 | 2952.859244713017 | 66.3850253222862 | 0.8209321241336272 |
| mean | 19401.65625 | 3316.9420775876606 | 66.96566309405408 | 0.8527699053487685 |
| max | 36467.0 | 6468.2597185785835 | 80.08082919606306 | 1.6012210853070985 |

## Generation Profile Estimates

| profile | symbols | days | event_retention_multiplier | estimated_event_rows | estimated_total_gb | evidence_label |
| --- | --- | --- | --- | --- | --- | --- |
| Small | 5 | 10 | 1.0 | 930625 | 0.07000784296542406 | projected_from_one_day_real_tick_density_and_phase9_parquet_sizes |
| Medium | 32 | 63 | 1.0 | 37522800 | 2.8227162677794695 | projected_from_one_day_real_tick_density_and_phase9_parquet_sizes |
| Full | 32 | 252 | 1.0 | 150091200 | 11.290865073911846 | projected_from_one_day_real_tick_density_and_phase9_parquet_sizes |
| Dense | 10 | 63 | 4.0 | 46903500 | 3.5208627358078957 | projected_from_one_day_real_tick_density_and_phase9_parquet_sizes |
| Feature-only | 32 | 252 | 1.0 | 150091200 | 0.032139088958501816 | projected_from_one_day_real_tick_density_and_phase9_parquet_sizes |

## Three-Month Feature Interval Estimates

| interval_seconds | symbols | days | estimated_rows | estimated_gb |
| --- | --- | --- | --- | --- |
| 1 | 32 | 63 | 45360000 | 2.410431723110378 |
| 5 | 32 | 63 | 9072000 | 0.48208634462207556 |
| 15 | 32 | 63 | 3024000 | 0.1606954475864768 |
| 60 | 32 | 63 | 756000 | 0.04017386119812727 |
| 300 | 32 | 63 | 151200 | 0.008034772239625454 |

## Top Regime Event-Rate Contributions

| quarter_profile | regime_code | regime_family | days | avg_event_rate_multiplier | weighted_event_rate_contribution |
| --- | --- | --- | --- | --- | --- |
| Q-B | D04 | Gradual bullish trend | 11 | 1.1 | 0.19206349206349208 |
| Q-A | D01 | Normal balanced | 12 | 1.0 | 0.19047619047619047 |
| Q-B | D05 | Strong rally | 7 | 1.35 | 0.15 |
| Q-C | D07 | Sell-off/panic | 6 | 1.55 | 0.14761904761904762 |
| Q-C | D03 | High-volatility sideways | 8 | 1.15 | 0.146031746031746 |
| Q-B | D01 | Normal balanced | 9 | 1.0 | 0.14285714285714285 |
| Q-C | D06 | Gradual bearish trend | 7 | 1.1 | 0.12222222222222223 |
| Q-A | D04 | Gradual bullish trend | 7 | 1.1 | 0.12222222222222223 |
| Q-B | D12 | Event day | 5 | 1.35 | 0.10714285714285715 |
| Q-C | D12 | Event day | 5 | 1.35 | 0.10714285714285715 |
| Q-A | D12 | Event day | 5 | 1.35 | 0.10714285714285715 |
| Q-A | D03 | High-volatility sideways | 5 | 1.15 | 0.09126984126984125 |

## Delta-State Guidance

- Keep full L2 snapshots at session start and after reconnect/disconnect boundaries.
- Store delta-state rows for changed fields between checkpoints.
- Use 30-300 second periodic full checkpoints; shorter intervals are safer for research replay, longer intervals compress better.
- Treat delta-state as an optimization layer over reproducible Tier A/B products until replay validation proves lossless reconstruction.

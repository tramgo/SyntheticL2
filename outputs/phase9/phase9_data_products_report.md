# Phase 9 Data Products Report

Generated UTC: 2026-07-13T20:33:07.583810+00:00

## Scope

This phase assembles formal Tier A/B/C/D synthetic data products from Phase 7 and Phase 8 outputs.
Tier D is a deterministic 15-minute resampled feature panel derived from the current Tier C 5-minute feature product.

## Validation

- tier_a_events: 2276282
- tier_a_event_kinds: 4
- tier_b_rows: 2259228
- tier_b_profiles: 5
- tier_b_symbols: 32
- tier_c_rows: 2259228
- tier_c_profiles: 5
- tier_c_symbols: 32
- tier_c_future_label_nulls: 30240
- tier_b_crossed_l1_rows: 0
- tier_d_resampled_rows: 755996
- tier_d_resampled_profiles: 5
- tier_d_resampled_symbols: 32
- tier_d_target_interval_minutes: 15
- tier_d_incomplete_panels: 21749

## Tier A Event Kinds

| event_kind | rows |
| --- | --- |
| received_l2_state | 2252450 |
| dropped_l2_state | 15550 |
| duplicate_l2_state | 6778 |
| shock_definition | 1504 |

## Tier B Profiles

| feed_profile | rows | symbols |
| --- | --- | --- |
| disconnect_scenario | 447662 | 32 |
| good_retail | 453581 | 32 |
| ideal_research | 453600 | 32 |
| normal_retail | 453126 | 32 |
| stressed_retail | 451259 | 32 |

## Tier D Resampled 15-Minute Summary

| feed_profile | target_interval_minutes | rows | symbols | trade_dates | scenario_days | complete_panels | incomplete_panels | mean_source_rows | median_spread_ticks | mean_event_intensity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| disconnect_scenario | 15 | 151197 | 32 | 63 | 63 | 141363 | 9834 | 2.9607862589866203 | 4.0 | 1.2588913862531126 |
| good_retail | 15 | 151200 | 32 | 63 | 63 | 150119 | 1081 | 2.9998743386243385 | 4.0 | 1.2588928663458745 |
| ideal_research | 15 | 151200 | 32 | 63 | 63 | 151200 | 0 | 3.0 | 4.0 | 1.2589027311902063 |
| normal_retail | 15 | 151200 | 32 | 63 | 63 | 148581 | 2619 | 2.9968650793650795 | 4.0 | 1.2588987291118114 |
| stressed_retail | 15 | 151199 | 32 | 63 | 63 | 142984 | 8215 | 2.9845369347680872 | 4.0 | 1.2588996323820973 |

## Outputs

- `tier_a/raw_synthetic_events.parquet`
- `tier_b/compact_l2_state.parquet`
- `tier_c/features_5m.parquet`
- `tier_d/resampled_features_15m.parquet`
- `tier_d/resampled_panel_summary.csv`
- `data_product_manifest.json`

# Phase 9 Data Products Report

Generated UTC: 2026-07-13T19:37:18.862222+00:00

## Scope

This phase assembles formal Tier A/B/C/D synthetic data products from Phase 7 and Phase 8 outputs.
Tier D is a deterministic 15-minute resampled feature panel derived from the current Tier C 5-minute feature product.

## Validation

- tier_a_events: 2276143
- tier_a_event_kinds: 4
- tier_b_rows: 2259039
- tier_b_profiles: 5
- tier_b_symbols: 32
- tier_c_rows: 2259039
- tier_c_profiles: 5
- tier_c_symbols: 32
- tier_c_future_label_nulls: 30240
- tier_b_crossed_l1_rows: 0
- tier_d_resampled_rows: 756000
- tier_d_resampled_profiles: 5
- tier_d_resampled_symbols: 32
- tier_d_target_interval_minutes: 15
- tier_d_incomplete_panels: 21633

## Tier A Event Kinds

| event_kind | rows |
| --- | --- |
| received_l2_state | 2252400 |
| dropped_l2_state | 15600 |
| duplicate_l2_state | 6639 |
| shock_definition | 1504 |

## Tier B Profiles

| feed_profile | rows | symbols |
| --- | --- | --- |
| disconnect_scenario | 447546 | 32 |
| good_retail | 453613 | 32 |
| ideal_research | 453600 | 32 |
| normal_retail | 453050 | 32 |
| stressed_retail | 451230 | 32 |

## Tier D Resampled 15-Minute Summary

| feed_profile | target_interval_minutes | rows | symbols | trade_dates | scenario_days | complete_panels | incomplete_panels | mean_source_rows | median_spread_ticks | mean_event_intensity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| disconnect_scenario | 15 | 151200 | 32 | 63 | 63 | 141457 | 9743 | 2.9599603174603173 | 4.0 | 1.2588994966713658 |
| good_retail | 15 | 151200 | 32 | 63 | 63 | 150185 | 1015 | 3.000085978835979 | 4.0 | 1.2588937742745754 |
| ideal_research | 15 | 151200 | 32 | 63 | 63 | 151200 | 0 | 3.0 | 4.0 | 1.2589027311902063 |
| normal_retail | 15 | 151200 | 32 | 63 | 63 | 148621 | 2579 | 2.996362433862434 | 4.0 | 1.2589130475985058 |
| stressed_retail | 15 | 151200 | 32 | 63 | 63 | 142904 | 8296 | 2.9843253968253967 | 4.0 | 1.258865149822306 |

## Outputs

- `tier_a/raw_synthetic_events.parquet`
- `tier_b/compact_l2_state.parquet`
- `tier_c/features_5m.parquet`
- `tier_d/resampled_features_15m.parquet`
- `tier_d/resampled_panel_summary.csv`
- `data_product_manifest.json`

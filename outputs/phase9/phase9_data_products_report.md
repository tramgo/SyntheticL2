# Phase 9 Data Products Report

Generated UTC: 2026-07-13T15:04:22.071431+00:00

## Scope

This phase assembles formal Tier A/B/C synthetic data products from Phase 7 and Phase 8 outputs.
Tier C is currently a 5-minute feature product; finer horizons remain gated by source/feed support.

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

## Outputs

- `tier_a/raw_synthetic_events.parquet`
- `tier_b/compact_l2_state.parquet`
- `tier_c/features_5m.parquet`
- `data_product_manifest.json`

# Phase 6 L2 Book Generator Report

Generated UTC: 2026-07-13T20:31:55.953698+00:00

## Scope

This phase generates one synthetic top-five market-by-price book state per Phase 5 price bar.
It does not yet produce individual exchange order events or deterministic queue/fill priority.

## Validation

- book_rows: 453600
- profiles: 3
- scenario_days: 189
- symbols: 32
- crossed_or_locked_l1_rows: 0
- bid_depth_sort_error_rows: 0
- ask_depth_sort_error_rows: 0
- nonpositive_quantity_rows: 0
- nonpositive_order_rows: 0
- tick_grid_error_rows: 0
- median_spread_ticks: 4.0
- q95_spread_ticks: 22.0

## Event Label Counts

| book_event_label | rows |
| --- | --- |
| book_state_update | 396475 |
| spread_widening | 38894 |
| best_price_shift | 11377 |
| replenishment | 6430 |
| multi_level_sweep | 424 |

## Outputs

- `l2_book_states_5m.parquet`
- `l2_book_summary.csv`
- `l2_book_manifest.json`

# Phase 5 Price Process Report

Generated UTC: 2026-07-13T20:30:27.989652+00:00

## Scope

This phase generates deterministic 5-minute synthetic OHLC price paths from the Phase 4 scenario calendar.
It does not yet generate L2 depth states, order-book events, retail feed effects or strategy fills.

## Validation

- bar_rows: 453600
- daily_rows: 6048
- profiles: 3
- scenario_days: 189
- symbols: 32
- bars_per_symbol_day_min: 75
- bars_per_symbol_day_max: 75
- min_price: 27.62
- max_tick_grid_error: 7.275957614183426e-12
- high_low_violations: 0

## Profile Summary

| quarter_profile | symbol_days | median_daily_return | q05_daily_return | q95_daily_return | median_high_low_range |
| --- | --- | --- | --- | --- | --- |
| Q-A | 2016 | 0.000578424761955354 | -0.0355040698909406 | 0.03520566053574181 | 0.02223107982515171 |
| Q-B | 2016 | 0.0010797583633636032 | -0.025583664482373647 | 0.03890214614480464 | 0.025233548338767897 |
| Q-C | 2016 | 0.00036177980352880557 | -0.037103305248282925 | 0.02523972208134151 | 0.024652167815092163 |

## Outputs

- `price_paths_5m.parquet`
- `daily_price_summary.csv`
- `price_process_manifest.json`

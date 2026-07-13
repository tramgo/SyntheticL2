# Horizon Readiness Gate Report

Generated UTC: 2026-07-13T20:54:03.992141+00:00

## Interpretation

This gate converts observed Zerodha received-feed coverage into explicit horizon-readiness decisions.
It separates dense regular-panel support from event-driven feature support so sparse 100 ms, 250 ms, 500 ms and 1-second panels are not accidentally treated as complete data.

## Horizon Decisions

| scope | window_name | horizon_ms | symbols_evaluated | dense_regular_panel_symbols | event_driven_symbols | median_coverage_fraction | min_coverage_fraction | median_forward_fill_fraction | max_forward_fill_fraction | readiness_status | usable_for_dense_regular_panel | usable_for_event_driven_features | caveat | median_event_rate_per_second | median_p95_gap_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full_session | full_session | 100 | 32 | 0 |  | 0.0652177 | 0.0326304 | 0.934782 | 0.96737 | event_driven_or_sparse_only | False | False | Do not treat this horizon as a complete dense panel across all symbols; use event-time logic or explicit forward-fill/staleness controls. |  |  |
| full_session | full_session | 250 | 32 | 0 |  | 0.16069 | 0.080764 | 0.83931 | 0.919236 | event_driven_or_sparse_only | False | False | Do not treat this horizon as a complete dense panel across all symbols; use event-time logic or explicit forward-fill/staleness controls. |  |  |
| full_session | full_session | 500 | 32 | 0 |  | 0.296507 | 0.157026 | 0.703493 | 0.842974 | event_driven_or_sparse_only | False | False | Do not treat this horizon as a complete dense panel across all symbols; use event-time logic or explicit forward-fill/staleness controls. |  |  |
| full_session | full_session | 1000 | 32 | 0 |  | 0.500922 | 0.297449 | 0.499078 | 0.702551 | event_driven_or_sparse_only | False | True | Do not treat this horizon as a complete dense panel across all symbols; use event-time logic or explicit forward-fill/staleness controls. |  |  |
| full_session | full_session | 5000 | 32 | 30 |  | 0.943591 | 0.885645 | 0.0564091 | 0.114355 | event_driven_or_sparse_only | False | True | Do not treat this horizon as a complete dense panel across all symbols; use event-time logic or explicit forward-fill/staleness controls. |  |  |
| full_session | full_session | 15000 | 32 | 32 |  | 0.988808 | 0.987508 | 0.0111916 | 0.0124918 | dense_regular_panel_supported | True | True | All symbols pass the 90% dense regular-panel gate. |  |  |
| full_session | full_session | 60000 | 32 | 32 |  | 0.994737 | 0.992126 | 0.00526316 | 0.00787402 | dense_regular_panel_supported | True | True | All symbols pass the 90% dense regular-panel gate. |  |  |
| open_window | open_0915_0920 | 100 | 32 | 0 |  | 0.0556667 | 0.0183333 | 0.944333 | 0.981667 | unsupported_sparse_subsecond | False | False | Sub-second horizons are sparse in the current retail received-feed sample; do not use as dense panels. | 0.68 | 6571.42 |
| open_window | open_0915_0920 | 250 | 32 | 0 |  | 0.137083 | 0.0458333 | 0.862917 | 0.954167 | unsupported_sparse_subsecond | False | False | Sub-second horizons are sparse in the current retail received-feed sample; do not use as dense panels. | 0.68 | 6571.42 |
| open_window | open_0915_0920 | 500 | 32 | 0 |  | 0.240833 | 0.0866667 | 0.759167 | 0.913333 | unsupported_sparse_subsecond | False | False | Sub-second horizons are sparse in the current retail received-feed sample; do not use as dense panels. | 0.68 | 6571.42 |
| open_window | open_0915_0920 | 1000 | 32 | 0 | 12 | 0.41 | 0.166667 | 0.59 | 0.833333 | event_driven_1s_supported_for_active_symbols | False | True | 12/32 symbols pass the event-driven 1-second gate; dense 1-second panels still require explicit forward-fill/staleness controls. | 0.68 | 6571.42 |
| open_window | open_0915_0920 | 5000 | 32 | 13 |  | 0.858333 | 0.716667 | 0.141667 | 0.283333 | sparse_or_forward_fill_only | False | False | Use only with explicit coverage, staleness and forward-fill labels. | 0.68 | 6571.42 |
| open_window | open_0915_0920 | 15000 | 32 | 32 |  | 1 | 1 | 0 | 0 | dense_regular_panel_supported | True | False | All symbols pass the 90% dense regular-panel gate in this window. | 0.68 | 6571.42 |
| open_window | open_0915_0920 | 60000 | 32 | 32 |  | 1 | 1 | 0 | 0 | dense_regular_panel_supported | True | False | All symbols pass the 90% dense regular-panel gate in this window. | 0.68 | 6571.42 |

## Open-Window One-Second Symbol Decisions

| window_name | symbol | rows | window_seconds | event_rate_per_second | coverage_fraction | forward_fill_fraction | median_gap_ms | p95_gap_ms | dense_1s_ready | event_driven_1s_ready | readiness_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| open_0915_0920 | HCLTECH | 445 | 300 | 1.48333 | 0.736667 | 0.263333 | 500 | 1251 | False | True | event_driven_1s_ready |
| open_0915_0920 | LT | 433 | 300 | 1.44333 | 0.726667 | 0.273333 | 500 | 1251 | False | True | event_driven_1s_ready |
| open_0915_0920 | ONGC | 425 | 300 | 1.41667 | 0.74 | 0.26 | 500 | 1250.85 | False | True | event_driven_1s_ready |
| open_0915_0920 | MARUTI | 420 | 300 | 1.4 | 0.74 | 0.26 | 501 | 1509 | False | True | event_driven_1s_ready |
| open_0915_0920 | INFY | 416 | 300 | 1.38667 | 0.743333 | 0.256667 | 500 | 1550.7 | False | True | event_driven_1s_ready |
| open_0915_0920 | TCS | 413 | 300 | 1.37667 | 0.746667 | 0.253333 | 500 | 1476.65 | False | True | event_driven_1s_ready |
| open_0915_0920 | HDFCBANK | 413 | 300 | 1.37667 | 0.743333 | 0.256667 | 500 | 1251.45 | False | True | event_driven_1s_ready |
| open_0915_0920 | SBIN | 352 | 300 | 1.17333 | 0.626667 | 0.373333 | 501 | 4044.5 | False | True | event_driven_1s_ready |
| open_0915_0920 | BHARTIARTL | 350 | 300 | 1.16667 | 0.626667 | 0.373333 | 500 | 4175.8 | False | True | event_driven_1s_ready |
| open_0915_0920 | WIPRO | 349 | 300 | 1.16333 | 0.626667 | 0.373333 | 500 | 4012.35 | False | True | event_driven_1s_ready |
| open_0915_0920 | M&M | 347 | 300 | 1.15667 | 0.623333 | 0.376667 | 500.5 | 4085.5 | False | True | event_driven_1s_ready |
| open_0915_0920 | ICICIBANK | 345 | 300 | 1.15 | 0.623333 | 0.376667 | 500 | 4122.95 | False | True | event_driven_1s_ready |
| open_0915_0920 | ITC | 289 | 300 | 0.963333 | 0.513333 | 0.486667 | 500 | 4533.25 | False | False | not_1s_ready |
| open_0915_0920 | DRREDDY | 287 | 300 | 0.956667 | 0.533333 | 0.466667 | 501 | 4572.75 | False | False | not_1s_ready |
| open_0915_0920 | ADANIPORTS | 211 | 300 | 0.703333 | 0.42 | 0.58 | 636.5 | 6214.75 | False | False | not_1s_ready |
| open_0915_0920 | GOLDBEES | 205 | 300 | 0.683333 | 0.403333 | 0.596667 | 749 | 6414.05 | False | False | not_1s_ready |
| open_0915_0920 | AXISBANK | 203 | 300 | 0.676667 | 0.413333 | 0.586667 | 749 | 7664.35 | False | False | not_1s_ready |
| open_0915_0920 | SUNPHARMA | 203 | 300 | 0.676667 | 0.406667 | 0.593333 | 749 | 7896.3 | False | False | not_1s_ready |
| open_0915_0920 | BAJAJ-AUTO | 191 | 300 | 0.636667 | 0.406667 | 0.593333 | 750 | 7588.4 | False | False | not_1s_ready |
| open_0915_0920 | RELIANCE | 186 | 300 | 0.62 | 0.403333 | 0.596667 | 997 | 6728.8 | False | False | not_1s_ready |
| open_0915_0920 | BPCL | 185 | 300 | 0.616667 | 0.39 | 0.61 | 751 | 7600.9 | False | False | not_1s_ready |
| open_0915_0920 | KOTAKBANK | 144 | 300 | 0.48 | 0.296667 | 0.703333 | 750 | 8224.1 | False | False | not_1s_ready |
| open_0915_0920 | NIFTYBEES | 127 | 300 | 0.423333 | 0.29 | 0.71 | 1000 | 7625 | False | False | not_1s_ready |
| open_0915_0920 | JUNIORBEES | 117 | 300 | 0.39 | 0.29 | 0.71 | 1070.5 | 7202 | False | False | not_1s_ready |
| open_0915_0920 | CIPLA | 62 | 300 | 0.206667 | 0.19 | 0.81 | 4973 | 8749 | False | False | not_1s_ready |
| open_0915_0920 | BRITANNIA | 62 | 300 | 0.206667 | 0.183333 | 0.816667 | 4770 | 9001 | False | False | not_1s_ready |
| open_0915_0920 | TECHM | 61 | 300 | 0.203333 | 0.183333 | 0.816667 | 4454 | 9091.1 | False | False | not_1s_ready |
| open_0915_0920 | HINDUNILVR | 61 | 300 | 0.203333 | 0.166667 | 0.833333 | 4437.5 | 9602.65 | False | False | not_1s_ready |
| open_0915_0920 | ITBEES | 60 | 300 | 0.2 | 0.186667 | 0.813333 | 5001 | 8985.8 | False | False | not_1s_ready |
| open_0915_0920 | NESTLEIND | 60 | 300 | 0.2 | 0.18 | 0.82 | 4915 | 9077.7 | False | False | not_1s_ready |
| open_0915_0920 | ULTRACEMCO | 58 | 300 | 0.193333 | 0.173333 | 0.826667 | 4999 | 10052.8 | False | False | not_1s_ready |
| open_0915_0920 | BANKBEES | 56 | 300 | 0.186667 | 0.183333 | 0.816667 | 5072 | 9931.4 | False | False | not_1s_ready |

## Key Caveat

The current one-day retail WebSocket sample can support event-driven 1-second work for active symbols/windows, but not dense full-session 1-second panels across the full universe.

# Phase83 Stratified Source-Event Bar Cache

Generated UTC: 2026-07-19T20:51:53.909015+00:00

Phase83 materializes reusable source-event aligned bars for the Phase81 stratified windows.
This repairs the Phase82 timestamp-bucket coverage issue by aligning on per-symbol source-event ordinal inside each selected source day and feed profile.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase83_raw_candidate_bar_rows | 167215 | Raw stratified source-event bars before core coverage trimming |
| phase83_cached_bar_rows | 160150 | Stratified source-event bars materialized |
| phase83_core_bar_retained_fraction | 0.957749 | Fraction of raw candidate bars retained after core coverage trimming |
| phase83_months_cached | 12 | Months represented in cached bars |
| phase83_coverage_bucket_rows | 5005 | Cross-symbol event-bar coverage rows |
| phase83_mean_monthly_coverage_pass_fraction | 1 | Mean monthly coverage pass fraction |
| phase83_min_monthly_coverage_pass_fraction | 1 | Worst monthly coverage pass fraction |
| phase83_stratified_bar_cache_pass | 1 | 1 means cache is ready for full stratified replay |
| phase83_elapsed_seconds | 2.5444 | Elapsed seconds |
| phase83_recommend_next_action | rerun_hdfcbank_on_cached_stratified_event_bars | Recommended next milestone |

## Monthly Summary

| trade_month | bar_rows | trade_dates | feed_profiles | regime_codes | symbols | coverage_bucket_rows | coverage_pass_fraction | median_symbols_present | market_shock_buckets | symbol_shock_symbol_bars |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | 12671 | 11 | 5 | 11 | 32 | 396 | 1 | 32 | 72 | 792 |
| 2026-02 | 13822 | 12 | 5 | 12 | 32 | 432 | 1 | 32 | 108 | 1332 |
| 2026-03 | 13824 | 12 | 5 | 12 | 32 | 432 | 1 | 32 | 72 | 648 |
| 2026-04 | 12671 | 11 | 5 | 11 | 32 | 396 | 1 | 32 | 72 | 864 |
| 2026-05 | 13854 | 12 | 5 | 12 | 32 | 433 | 1 | 32 | 109 | 361 |
| 2026-06 | 14976 | 13 | 5 | 13 | 32 | 468 | 1 | 32 | 180 | 1584 |
| 2026-07 | 13824 | 12 | 5 | 12 | 32 | 432 | 1 | 32 | 36 | 648 |
| 2026-08 | 14976 | 13 | 5 | 13 | 32 | 468 | 1 | 32 | 72 | 1404 |
| 2026-09 | 12671 | 11 | 5 | 11 | 32 | 396 | 1 | 32 | 108 | 1260 |
| 2026-10 | 12671 | 11 | 5 | 11 | 32 | 396 | 1 | 32 | 0 | 252 |
| 2026-11 | 16126 | 14 | 5 | 14 | 32 | 504 | 1 | 32 | 108 | 1404 |
| 2026-12 | 8064 | 7 | 5 | 7 | 32 | 252 | 1 | 32 | 72 | 576 |

## Coverage Sample

| trade_month | trade_date | feed_profile | source_event_bar_id | symbols_present | total_source_events | min_source_events_in_bar | regimes | market_shock_bar | symbol_shock_symbols | expected_symbols | coverage_fraction | coverage_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | 2026-01-01 | disconnect_scenario | 0 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | disconnect_scenario | 1 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | disconnect_scenario | 2 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | disconnect_scenario | 3 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | disconnect_scenario | 4 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | disconnect_scenario | 5 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | disconnect_scenario | 6 | 32 | 318 | 8 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | good_retail | 0 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | good_retail | 1 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | good_retail | 2 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | good_retail | 3 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | good_retail | 4 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | good_retail | 5 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | good_retail | 6 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | ideal_research | 0 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | ideal_research | 1 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | ideal_research | 2 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | ideal_research | 3 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | ideal_research | 4 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | ideal_research | 5 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | ideal_research | 6 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | ideal_research | 7 | 32 | 160 | 5 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | normal_retail | 0 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | normal_retail | 1 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | normal_retail | 2 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | normal_retail | 3 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | normal_retail | 4 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | normal_retail | 5 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | normal_retail | 6 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | stressed_retail | 0 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | stressed_retail | 1 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | stressed_retail | 2 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | stressed_retail | 3 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | stressed_retail | 4 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | stressed_retail | 5 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-01 | stressed_retail | 6 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | disconnect_scenario | 0 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | disconnect_scenario | 1 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | disconnect_scenario | 2 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | disconnect_scenario | 3 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | disconnect_scenario | 4 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | disconnect_scenario | 5 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | disconnect_scenario | 6 | 32 | 309 | 7 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | good_retail | 0 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | good_retail | 1 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | good_retail | 2 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | good_retail | 3 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | good_retail | 4 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | good_retail | 5 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | good_retail | 6 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | ideal_research | 0 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | ideal_research | 1 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | ideal_research | 2 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | ideal_research | 3 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | ideal_research | 4 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | ideal_research | 5 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | ideal_research | 6 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | ideal_research | 7 | 32 | 160 | 5 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | normal_retail | 0 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | normal_retail | 1 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | normal_retail | 2 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | normal_retail | 3 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | normal_retail | 4 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | normal_retail | 5 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | normal_retail | 6 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | stressed_retail | 0 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | stressed_retail | 1 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | stressed_retail | 2 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | stressed_retail | 3 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | stressed_retail | 4 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | stressed_retail | 5 | 32 | 320 | 10 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-02 | stressed_retail | 6 | 32 | 318 | 9 | 1 | 1 | 4 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | disconnect_scenario | 0 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | disconnect_scenario | 1 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | disconnect_scenario | 2 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | disconnect_scenario | 3 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | disconnect_scenario | 4 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | disconnect_scenario | 5 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | disconnect_scenario | 6 | 32 | 319 | 9 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | good_retail | 0 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | good_retail | 1 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | good_retail | 2 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | good_retail | 3 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | good_retail | 4 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | good_retail | 5 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | good_retail | 6 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | ideal_research | 0 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | ideal_research | 1 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | ideal_research | 2 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | ideal_research | 3 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | ideal_research | 4 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | ideal_research | 5 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | ideal_research | 6 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | ideal_research | 7 | 32 | 160 | 5 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | normal_retail | 0 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | normal_retail | 1 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | normal_retail | 2 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | normal_retail | 3 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | normal_retail | 4 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | normal_retail | 5 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | normal_retail | 6 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | stressed_retail | 0 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | stressed_retail | 1 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | stressed_retail | 2 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | stressed_retail | 3 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | stressed_retail | 4 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | stressed_retail | 5 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-06 | stressed_retail | 6 | 32 | 320 | 10 | 1 | 0 | 0 | 32 | 1 | True |
| 2026-01 | 2026-01-07 | disconnect_scenario | 0 | 32 | 320 | 10 | 1 | 1 | 13 | 32 | 1 | True |
| 2026-01 | 2026-01-07 | disconnect_scenario | 1 | 32 | 320 | 10 | 1 | 1 | 13 | 32 | 1 | True |
| 2026-01 | 2026-01-07 | disconnect_scenario | 2 | 32 | 320 | 10 | 1 | 1 | 13 | 32 | 1 | True |
| 2026-01 | 2026-01-07 | disconnect_scenario | 3 | 32 | 320 | 10 | 1 | 1 | 13 | 32 | 1 | True |
| 2026-01 | 2026-01-07 | disconnect_scenario | 4 | 32 | 320 | 10 | 1 | 1 | 13 | 32 | 1 | True |
| 2026-01 | 2026-01-07 | disconnect_scenario | 5 | 32 | 320 | 10 | 1 | 1 | 13 | 32 | 1 | True |
| 2026-01 | 2026-01-07 | disconnect_scenario | 6 | 32 | 303 | 6 | 1 | 1 | 13 | 32 | 1 | True |
| 2026-01 | 2026-01-07 | good_retail | 0 | 32 | 320 | 10 | 1 | 1 | 13 | 32 | 1 | True |
| 2026-01 | 2026-01-07 | good_retail | 1 | 32 | 320 | 10 | 1 | 1 | 13 | 32 | 1 | True |
| 2026-01 | 2026-01-07 | good_retail | 2 | 32 | 320 | 10 | 1 | 1 | 13 | 32 | 1 | True |
| 2026-01 | 2026-01-07 | good_retail | 3 | 32 | 320 | 10 | 1 | 1 | 13 | 32 | 1 | True |
| 2026-01 | 2026-01-07 | good_retail | 4 | 32 | 320 | 10 | 1 | 1 | 13 | 32 | 1 | True |

# Phase 10 Storage and Size Optimization Report

Generated UTC: 2026-07-13T19:37:21.763074+00:00

## Scope

This phase measures current Parquet product sizes, audits physical column types, and estimates storage for the plan profiles.
Parquet/Zstandard remains the durable format. DuckDB remains the analytic query layer. SQLite is not used for high-volume tick/L2 storage.

## Current Product Inventory

| dataset | file_count | total_rows | mb | bytes_per_row | tiny_file_warning |
| --- | --- | --- | --- | --- | --- |
| stage_a1_compact_real_ticks | 32 | 620853 | 39.7124 | 67.0714 | True |
| phase5_price_paths_5m | 1 | 453600 | 16.9416 | 39.1635 | False |
| phase6_l2_book_states_5m | 1 | 453600 | 26.1987 | 60.5628 | False |
| phase8_retail_feed_observations | 1 | 2259039 | 152.3552 | 70.7186 | False |
| phase9_tier_a_raw_synthetic_events | 1 | 2276143 | 15.3824 | 7.0864 | False |
| phase9_tier_b_compact_l2_state | 1 | 2259039 | 158.2565 | 73.4578 | False |
| phase9_tier_c_features_5m | 1 | 2259039 | 122.9265 | 57.0587 | False |
| phase9_tier_d_resampled_features_15m | 1 | 756000 | 55.2252 | 76.5976 | False |

## Size Estimates

| profile | tickers | trading_days | feed_profiles | event_multiplier | estimated_feed_rows | total_gb | conservative_total_gb | aggressive_total_gb |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Small | 5 | 10 | 1 | 1.0000 | 970082.8125 | 0.1475 | 0.1032 | 0.3687 |
| Medium | 32 | 63 | 5 | 1.0000 | 195568695.0000 | 29.7315 | 20.8121 | 74.3288 |
| Full | 32 | 252 | 5 | 1.0000 | 782274780.0000 | 118.9261 | 83.2482 | 297.3151 |
| Dense | 10 | 63 | 5 | 4.0000 | 244460868.7500 | 37.1644 | 26.0151 | 92.9110 |
| Feature-only | 32 | 63 | 5 | 1.0000 | 195568695.0000 | 28.4408 | 19.9086 | 71.1020 |

## Partition Recommendations

| dataset | recommended_partitioning | action |
| --- | --- | --- |
| stage_a1_compact_real_ticks | layer=audit_or_calibration/trade_date=YYYY-MM-DD/symbol=ABC/part-*.parquet | consider compaction into 128-512 MB files before large multi-day expansion |
| phase5_price_paths_5m | layer=audit_or_calibration/trade_date=YYYY-MM-DD/symbol=ABC/part-*.parquet | keep current single-file product until it exceeds practical rewrite threshold |
| phase6_l2_book_states_5m | layer=l2_state/trade_date=YYYY-MM-DD/symbol=ABC/part-*.parquet | keep current single-file product until it exceeds practical rewrite threshold |
| phase8_retail_feed_observations | layer=l2_state/trade_date=YYYY-MM-DD/symbol=ABC/part-*.parquet | keep current single-file product until it exceeds practical rewrite threshold |
| phase9_tier_a_raw_synthetic_events | layer=raw_events/trade_date=YYYY-MM-DD/symbol=ABC/part-*.parquet | keep current single-file product until it exceeds practical rewrite threshold |
| phase9_tier_b_compact_l2_state | layer=l2_state/trade_date=YYYY-MM-DD/symbol=ABC/part-*.parquet | keep current single-file product until it exceeds practical rewrite threshold |
| phase9_tier_c_features_5m | layer=features_5m/trading_month=YYYY-MM/symbol=ABC/part-*.parquet | keep current single-file product until it exceeds practical rewrite threshold |
| phase9_tier_d_resampled_features_15m | layer=features_15m/trading_month=YYYY-MM/symbol=ABC/part-*.parquet | keep current single-file product until it exceeds practical rewrite threshold |

## Type Optimization Candidates

| dataset | column | arrow_type | recommended_type_note |
| --- | --- | --- | --- |
| stage_a1_compact_real_ticks | last_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| stage_a1_compact_real_ticks | average_traded_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| stage_a1_compact_real_ticks | buy_1_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| stage_a1_compact_real_ticks | buy_2_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| stage_a1_compact_real_ticks | buy_3_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| stage_a1_compact_real_ticks | buy_4_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| stage_a1_compact_real_ticks | buy_5_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| stage_a1_compact_real_ticks | sell_1_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| stage_a1_compact_real_ticks | sell_2_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| stage_a1_compact_real_ticks | sell_3_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| stage_a1_compact_real_ticks | sell_4_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| stage_a1_compact_real_ticks | sell_5_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| phase5_price_paths_5m | quarter_profile | large_string | dictionary encoding recommended |
| phase5_price_paths_5m | symbol | large_string | dictionary encoding recommended |
| phase5_price_paths_5m | regime_code | large_string | dictionary encoding recommended |
| phase5_price_paths_5m | bar_return | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| phase5_price_paths_5m | cumulative_return | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| phase5_price_paths_5m | spread_multiplier | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| phase6_l2_book_states_5m | quarter_profile | large_string | dictionary encoding recommended |
| phase6_l2_book_states_5m | symbol | large_string | dictionary encoding recommended |
| phase6_l2_book_states_5m | regime_code | large_string | dictionary encoding recommended |
| phase6_l2_book_states_5m | mid_price | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| phase6_l2_book_states_5m | spread | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |
| phase6_l2_book_states_5m | book_event_label | large_string | dictionary encoding recommended |
| phase6_l2_book_states_5m | bar_return | double | candidate for fixed-point integer ticks where exact tick-grid replay is required |

## Caveats

- Estimates use the current one-day real received-tick row rate and current synthetic product bytes-per-row.
- The current Phase 6-9 synthetic stream is 5-minute state based; event-driven expansion will change row counts and should rerun this phase.
- Conservative/aggressive totals are storage-planning bands, not statistical confidence intervals.

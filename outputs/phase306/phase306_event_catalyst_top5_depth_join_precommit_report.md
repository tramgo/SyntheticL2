# Phase306 Event-Catalyst Top-Five Depth Join Precommit

Phase306 precommits the event-catalyst to top-five market-by-price depth join. It does not materialize joined features and does not run strategy search.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase306_join_precommit_complete | 1 | Phase306 event-catalyst top-five depth join precommit completed |
| phase306_imported_event_rows | 1 | Imported event-catalyst rows available |
| phase306_event_universe_rows | 32 | Event x symbol join work-order rows |
| phase306_event_rows_with_depth_month | 1 | Distinct events with matching dense month |
| phase306_symbol_rows | 32 | Symbols in join universe |
| phase306_pre_event_seconds | 900 | Pre-event window |
| phase306_post_event_seconds | 1800 | Post-event window |
| phase306_event_bucket_seconds | 1 | Join bucket size |
| phase306_full_depth_levels_1_to_5_required | 1 | Top-five market-by-price depth required |
| phase306_strategy_search_allowed_now | 0 | No strategy search in Phase306 |
| phase306_strategy_replay_allowed | 0 | No replay |
| phase306_strategy_promotion_allowed | 0 | No promotion |
| phase306_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase306_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase306_hard_gate_pass_rows | 8 | Passed hard gates |
| phase306_hard_gate_rows | 8 | Hard gates |
| phase306_next_best_action | run_phase307_event_catalyst_top5_depth_join_materialization_no_strategy_search | Recommended next action |

## Join contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P306_JOIN_CLOCK | event_time_ist | Join windows are centered on observable event timestamp. |
| P306_PRE_WINDOW | 900 | Seconds before event for pre-catalyst top-five depth context. |
| P306_POST_WINDOW | 1800 | Seconds after event for response measurement. |
| P306_BUCKET_SECONDS | 1 | One-second bucket for joined event/depth response features. |
| P306_FULL_DEPTH_REQUIRED | 1 | Use top-five market-by-price depth levels 1-5; no L1-only join. |
| P306_NO_DIRECTIONAL_LABEL | 1 | Event source provides catalyst timing, not bullish/bearish truth labels. |
| P306_NO_STRATEGY_SEARCH | 1 | Materialization precommit only; no P&L, replay or optimization. |

## Event-symbol universe

| event_id | event_time_ist | event_type | symbol | trade_month | dense_file_path | dense_rows | pre_event_seconds | post_event_seconds | event_bucket_seconds | source_url_or_file |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | ADANIPORTS | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ADANIPORTS\part-00000.parquet | 15549968 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | AXISBANK | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=AXISBANK\part-00000.parquet | 15555918 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | BAJAJ-AUTO | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BAJAJ-AUTO\part-00000.parquet | 15542034 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | BANKBEES | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BANKBEES\part-00000.parquet | 15557902 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | BHARTIARTL | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BHARTIARTL\part-00000.parquet | 15575752 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | BPCL | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BPCL\part-00000.parquet | 15512283 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | BRITANNIA | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BRITANNIA\part-00000.parquet | 15561869 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | CIPLA | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=CIPLA\part-00000.parquet | 15549968 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | DRREDDY | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=DRREDDY\part-00000.parquet | 15563852 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | GOLDBEES | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=GOLDBEES\part-00000.parquet | 15551951 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | HCLTECH | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=HCLTECH\part-00000.parquet | 15575752 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | HDFCBANK | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=HDFCBANK\part-00000.parquet | 15551951 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | HINDUNILVR | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=HINDUNILVR\part-00000.parquet | 15542034 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | ICICIBANK | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ICICIBANK\part-00000.parquet | 15569802 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | INFY | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=INFY\part-00000.parquet | 15565835 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | ITBEES | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ITBEES\part-00000.parquet | 15551951 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | ITC | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ITC\part-00000.parquet | 15577736 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | JUNIORBEES | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=JUNIORBEES\part-00000.parquet | 15547985 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | KOTAKBANK | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=KOTAKBANK\part-00000.parquet | 15557902 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | LT | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=LT\part-00000.parquet | 15581703 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | M&M | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=M&M\part-00000.parquet | 15565835 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | MARUTI | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=MARUTI\part-00000.parquet | 15569802 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | NESTLEIND | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=NESTLEIND\part-00000.parquet | 15524184 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | NIFTYBEES | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=NIFTYBEES\part-00000.parquet | 15553935 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | ONGC | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ONGC\part-00000.parquet | 15561869 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | RELIANCE | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=RELIANCE\part-00000.parquet | 15569802 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | SBIN | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=SBIN\part-00000.parquet | 15595587 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | SUNPHARMA | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=SUNPHARMA\part-00000.parquet | 15561869 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | TCS | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=TCS\part-00000.parquet | 15546001 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | TECHM | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=TECHM\part-00000.parquet | 15569802 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | ULTRACEMCO | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ULTRACEMCO\part-00000.parquet | 15534101 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |
| P306_EVT_0001 | 2026-08-05 10:00:00+05:30 | rbi_policy | WIPRO | 2026-08 | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=WIPRO\part-00000.parquet | 15546001 | 900 | 1800 | 1 | https://www.youtube.com/watch?v=XIdD58WOX30 |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P306_PHASE305_IMPORTED_EVENTS | True | 1 | >0 | hard |
| P306_EVENT_UNIVERSE_EXPANDED | True | 32 | >0 | hard |
| P306_FULL_DEPTH_SCHEMA_AVAILABLE | True | 1 | 1 | hard |
| P306_JOIN_CONTRACT_PRESENT | True | 7 | >=7 | hard |
| P306_NO_L1_ONLY_JOIN | True | full_depth_levels_1_to_5_required | required | hard |
| P306_NO_DIRECTIONAL_LABEL_FROM_EVENT | True | event_timestamp_only | required | hard |
| P306_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P306_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

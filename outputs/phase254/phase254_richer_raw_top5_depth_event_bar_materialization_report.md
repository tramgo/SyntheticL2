# Phase254 Richer Raw Top-five Depth Event-bar Materialization

Generated UTC: 2026-07-29T10:43:53.061263+00:00

Phase254 materializes compact event bars from existing local raw Zerodha top-five market-by-price parquet.
It reads explicit buy/sell levels 1-5 price, quantity and order-count fields, carries cost-floor fields and does not run replay, promotion, paper/live or profitability claims.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase254_richer_raw_depth_materialization_complete | 1 | Phase254 richer raw-depth event-bar materialization completed |
| phase254_raw_root_used | real_data_sample\l2_single_day | Existing local raw root used |
| phase254_events_per_bar | 20 | Receive events per richer raw-depth event bar |
| phase254_max_files_per_symbol | 100 | Bounded raw parquet files read per symbol |
| phase254_source_parquet_files_read | 3200 | Source raw parquet shards read |
| phase254_excluded_invalid_source_tick_rows | 4 | Invalid crossed/locked/nonpositive/missing raw ticks excluded before aggregation |
| phase254_event_bar_rows | 1636 | Materialized richer event bars |
| phase254_trade_dates | 1 | Trade dates represented |
| phase254_symbols | 32 | Symbols represented |
| phase254_source_tick_rows | 32426 | Source raw tick rows represented |
| phase254_training_allowed_event_bar_rows | 1636 | Rows allowed for downstream training selection |
| phase254_crossed_or_locked_tick_rows | 0 | Crossed/locked source tick rows |
| phase254_nonpositive_depth_tick_rows | 0 | Nonpositive full-depth source rows |
| phase254_missing_level_tick_rows | 0 | Rows missing required level fields |
| phase254_mean_spread_bps | 2.8444 | Mean event-bar spread bps |
| phase254_median_spread_bps | 2.67259 | Median event-bar spread bps |
| phase254_mean_top5_imbalance | -0.0152604 | Mean cumulative top-five imbalance |
| phase254_mean_depth_beyond_l1_imbalance | -0.00522297 | Mean depth-beyond-L1 imbalance |
| phase254_hard_gate_pass_rows | 8 | Hard gates passed |
| phase254_hard_gate_rows | 8 | Hard gates evaluated |
| phase254_download_more_dates_now_allowed | 0 | No raw-date download in Phase254 |
| phase254_replay_execution_allowed_now | 0 | No replay execution in Phase254 |
| phase254_strategy_promotion_allowed | 0 | No strategy promotion from Phase254 |
| phase254_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase254 |
| phase254_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase254 |
| phase254_next_best_action | run_phase255_richer_raw_depth_feature_quality_interpretation_no_replay_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P254_PHASE253_WORK_ORDER_PRESENT | True | run_phase254_materialize_richer_raw_top5_depth_event_bars_existing_raw_only_no_paper_live | Phase253 next action targets Phase254 | hard |
| P254_EVENT_BARS_MATERIALIZED | True | 1636 | >0 richer raw-depth event bars | hard |
| P254_REAL_DATE_OUTPUT | True | 1 | >=1 real trade date for first richer-depth materialization | hard |
| P254_SYMBOL_BREADTH | True | 32 | >=20 symbols | hard |
| P254_SOURCE_TICK_COUNTS_RETAINED | True | 32426 | >0 source ticks represented | hard |
| P254_RAW_DEPTH_QUALITY_PASS | True | crossed=0.0;missing=0.0 | 0 crossed/locked and 0 missing level rows | hard |
| P254_COST_FIELDS_CARRIED | True | zerodha_round_trip_charge_bps;taker_round_trip_cost_floor_bps | cost floor fields present | hard |
| P254_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

## Daily Quality Summary

| trade_date | event_bar_rows | symbols | source_tick_rows | mean_spread_bps | crossed_or_locked_tick_rows | nonpositive_depth_tick_rows | missing_level_tick_rows |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-13 | 1636 | 32 | 32426 | 2.8444 | 0 | 0 | 0 |

## Symbol Feature Summary

| symbol | event_bar_rows | trade_dates | source_tick_rows | mean_spread_bps | mean_top5_imbalance | mean_depth_beyond_l1_imbalance |
| --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | 47 | 1 | 931 | 3.23815 | 0.127218 | 0.139336 |
| AXISBANK | 52 | 1 | 1037 | 2.35117 | -0.114074 | -0.0988528 |
| BAJAJ-AUTO | 50 | 1 | 998 | 3.19763 | -0.0196678 | -0.0473845 |
| BANKBEES | 44 | 1 | 868 | 3.14687 | -0.474136 | -0.370195 |
| BHARTIARTL | 53 | 1 | 1044 | 2.53254 | 0.0990141 | 0.10774 |
| BPCL | 24 | 1 | 461 | 4.17632 | -0.0663903 | -0.0861014 |
| BRITANNIA | 16 | 1 | 311 | 3.69125 | -0.153137 | -0.153459 |
| CIPLA | 17 | 1 | 338 | 3.79517 | 0.150494 | 0.132294 |
| DRREDDY | 42 | 1 | 829 | 3.55896 | 0.061028 | 0.0864894 |
| GOLDBEES | 24 | 1 | 479 | 1.99143 | -0.179466 | -0.155314 |
| HCLTECH | 79 | 1 | 1572 | 3.7454 | 0.0184492 | 0.0434178 |
| HDFCBANK | 108 | 1 | 2141 | 2.09098 | 0.0579995 | -0.000850907 |
| HINDUNILVR | 20 | 1 | 391 | 2.54182 | 0.201338 | 0.154371 |
| ICICIBANK | 80 | 1 | 1597 | 2.12905 | -0.0997183 | -0.0833934 |
| INFY | 101 | 1 | 2011 | 2.89239 | -0.138561 | -0.130352 |
| ITBEES | 17 | 1 | 334 | 5.40269 | 0.529853 | 0.541169 |
| ITC | 29 | 1 | 561 | 3.33205 | 0.238199 | 0.236689 |
| JUNIORBEES | 22 | 1 | 435 | 5.69731 | -0.143081 | -0.134428 |
| KOTAKBANK | 25 | 1 | 481 | 3.23825 | -0.0896873 | -0.106527 |
| LT | 102 | 1 | 2026 | 1.6073 | -0.0510211 | -0.00578598 |
| M&M | 86 | 1 | 1719 | 2.3367 | 0.0141487 | 0.0309463 |
| MARUTI | 94 | 1 | 1872 | 3.38704 | -0.00303262 | 0.00252574 |
| NESTLEIND | 19 | 1 | 375 | 3.831 | 0.17946 | 0.158502 |
| NIFTYBEES | 39 | 1 | 774 | 1.84974 | 0.00647981 | 0.00763795 |
| ONGC | 97 | 1 | 1932 | 3.02062 | -0.052333 | -0.0209421 |
| RELIANCE | 56 | 1 | 1107 | 2.31566 | -0.160867 | -0.156778 |
| SBIN | 42 | 1 | 840 | 2.93385 | 0.0746066 | 0.0862678 |
| SUNPHARMA | 28 | 1 | 547 | 3.29643 | 0.133827 | 0.136756 |
| TCS | 110 | 1 | 2186 | 2.61377 | 0.0279115 | 0.0656381 |
| TECHM | 43 | 1 | 846 | 3.37899 | -0.071875 | -0.0596573 |
| ULTRACEMCO | 16 | 1 | 315 | 3.6193 | 0.0531706 | 0.0848731 |
| WIPRO | 54 | 1 | 1068 | 2.56352 | 0.0276993 | 0.00107192 |

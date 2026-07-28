# Phase176 Receive-flow Feature Materializer

Generated UTC: 2026-07-28T16:04:39.149822+00:00

Phase176 is the executable materialization scaffold for the Phase175 feature schema.
When Phase175 activation is closed, Phase176 writes plan/templates/gates only and materializes no feature parquet.
It does not emit signals, orders, fills, P&L, profitability claims, or paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase176_materialization_plan_rows | 6 | Feature materialization plan rows |
| phase176_sql_template_rows | 3 | DuckDB/local SQL templates declared |
| phase176_gate_rows | 4 | Gates evaluated |
| phase176_hard_gate_rows | 3 | Hard gates evaluated |
| phase176_hard_gate_pass_rows | 3 | Hard gates passed |
| phase176_activation_ready | 1 | Inherited Phase175 activation gate |
| phase176_materialized_partition_rows | 640 | Feature partition rows written to inventory |
| phase176_materialized_feature_rows | 2209164 | Feature rows written across all horizons |
| phase176_feature_parquet_files | 640 | Feature parquet files present under feature root |
| phase176_features_materialized | 1 | 1 means feature parquet was materialized |
| phase176_strategy_replay_allowed | 0 | No strategy replay opened |
| phase176_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase176_forbidden_outputs | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | Outputs forbidden in this phase |
| phase176_next_best_action | run_phase177_feature_quality_audit | Recommended next milestone |

## Materialization Plan

| feature_id | feature_family | materialization_status | target_layout | allowed_horizons | minimum_source_days | leakage_control | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P175_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | materialized_feature_file_family | derived_real_l2_receive_flow_features_phase176\trade_date=YYYY-MM-DD\exchange=NSE\symbol=SYMBOL\p175_receive_event_rate_zscore.parquet | 1s;5s;15s;60s with coverage/staleness reporting | 5 | baseline statistics fitted on train dates only before test-date transform | 0 |
| P175_QUOTE_CHURN_RATE | book_state_churn | materialized_feature_file_family | derived_real_l2_receive_flow_features_phase176\trade_date=YYYY-MM-DD\exchange=NSE\symbol=SYMBOL\p175_quote_churn_rate.parquet | 1s;5s;15s;60s with symbol-specific coverage gates | 5 | computed only from events received at or before the feature timestamp | 0 |
| P175_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | materialized_feature_file_family | derived_real_l2_receive_flow_features_phase176\trade_date=YYYY-MM-DD\exchange=NSE\symbol=SYMBOL\p175_depth_refresh_intensity.parquet | 1s;5s;15s;60s with depth-field completeness gates | 5 | uses top-five market-by-price state only; no inferred hidden order events | 0 |
| P175_STALE_QUOTE_DURATION | feed_staleness | materialized_feature_file_family | derived_real_l2_receive_flow_features_phase176\trade_date=YYYY-MM-DD\exchange=NSE\symbol=SYMBOL\p175_stale_quote_duration.parquet | event_time;1s;5s;15s | 5 | forward state duration censored at the current timestamp; no future duration completion | 0 |
| P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | materialized_feature_file_family | derived_real_l2_receive_flow_features_phase176\trade_date=YYYY-MM-DD\exchange=NSE\symbol=SYMBOL\p175_cross_symbol_arrival_synchrony.parquet | 1s native synchrony source plus 5s/15s aggregations | 5 | computed from contemporaneous receive buckets only; target symbol exclusion required in ablation | 0 |
| P175_RECEIVE_FLOW_REGIME_STATE | source_quality_context | materialized_feature_file_family | derived_real_l2_receive_flow_features_phase176\trade_date=YYYY-MM-DD\exchange=NSE\symbol=SYMBOL\p175_receive_flow_regime_state.parquet | daily fitted context with intraday labels | 5 | fit context model on train dates only; report train/test date separation | 0 |

## DuckDB SQL Templates

| template_id | purpose | sql_template | output_path | strategy_replay_allowed |
| --- | --- | --- | --- | --- |
| P176_BASE_RECEIVE_EVENTS | local-only source view over downloaded Zerodha top-five market-by-price Parquet | SELECT trade_date, exchange, tradingsymbol AS symbol, collector_received_utc_ms AS receive_ms, buy_1_price, buy_1_quantity, sell_1_price, sell_1_quantity, buy_1_quantity, buy_2_quantity, buy_3_quantity, buy_4_quantity, buy_5_quantity, sell_1_quantity, sell_2_quantity, sell_3_quantity, sell_4_quantity, sell_5_quantity FROM read_parquet('real_data_sample/l2_multiday_panel/trade_date=*/exchange=NSE/symbol=*/*.parquet', hive_partitioning=true, union_by_name=true) |  | 0 |
| P176_1S_BUCKET_FEATURES | 1-second bucket receive-event/churn/staleness/synchrony features after activation opens | WITH ordered AS (... event-time sorted source ...), buckets AS (... floor(receive_ms/1000) ... ) SELECT trade_date, exchange, symbol, bucket_1s, receive_event_count, quote_churn_count, depth_refresh_count, stale_quote_duration_ms, cross_symbol_arrival_count FROM buckets | derived_real_l2_receive_flow_features_phase176\horizon=1s | 0 |
| P176_5S_15S_60S_AGGREGATIONS | higher-horizon aggregations from already materialized 1-second features | SELECT trade_date, exchange, symbol, horizon, bucket_ts, aggregate_receive_flow_features FROM phase176_1s_features GROUP BY trade_date, exchange, symbol, horizon, bucket_ts | derived_real_l2_receive_flow_features_phase176\horizon={5s,15s,60s} | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P176_PHASE175_ACTIVATION_READY | 1 | phase175_activation_ready=1;ready_dates=5;additional_needed=0 | activation |
| P176_SCHEMA_AVAILABLE | 1 | feature_schema_rows=6 | hard |
| P176_LOCAL_REAL_ROOT_EXISTS | 1 | real_data_sample\l2_multiday_panel | hard |
| P176_NO_REPLAY_OR_PROFITABILITY_OUTPUTS | 1 | materializer scaffold only while activation gate is closed; forbidden_outputs=buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | hard |

## Feature Partition Inventory

| horizon_sec | trade_date | exchange | symbol | rows | parquet_file | bytes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-07-08 | NSE | ADANIPORTS | 3618 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\receive_flow_features.parquet | 186589 |
| 1 | 2026-07-08 | NSE | AXISBANK | 5830 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\receive_flow_features.parquet | 305627 |
| 1 | 2026-07-08 | NSE | BAJAJ-AUTO | 3324 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_features.parquet | 157900 |
| 1 | 2026-07-08 | NSE | BANKBEES | 5646 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\receive_flow_features.parquet | 289503 |
| 1 | 2026-07-08 | NSE | BHARTIARTL | 3953 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\receive_flow_features.parquet | 203970 |
| 1 | 2026-07-08 | NSE | BPCL | 2853 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\receive_flow_features.parquet | 145222 |
| 1 | 2026-07-08 | NSE | BRITANNIA | 2152 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\receive_flow_features.parquet | 109413 |
| 1 | 2026-07-08 | NSE | CIPLA | 2954 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\receive_flow_features.parquet | 146748 |
| 1 | 2026-07-08 | NSE | DRREDDY | 2936 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\receive_flow_features.parquet | 148447 |
| 1 | 2026-07-08 | NSE | GOLDBEES | 4079 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\receive_flow_features.parquet | 209397 |
| 1 | 2026-07-08 | NSE | HCLTECH | 2707 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\receive_flow_features.parquet | 137237 |
| 1 | 2026-07-08 | NSE | HDFCBANK | 6817 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\receive_flow_features.parquet | 366160 |
| 1 | 2026-07-08 | NSE | HINDUNILVR | 3471 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\receive_flow_features.parquet | 178167 |
| 1 | 2026-07-08 | NSE | ICICIBANK | 6211 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\receive_flow_features.parquet | 325563 |
| 1 | 2026-07-08 | NSE | INFY | 5153 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=INFY\receive_flow_features.parquet | 271057 |
| 1 | 2026-07-08 | NSE | ITBEES | 2356 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\receive_flow_features.parquet | 120435 |
| 1 | 2026-07-08 | NSE | ITC | 4272 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ITC\receive_flow_features.parquet | 220130 |
| 1 | 2026-07-08 | NSE | JUNIORBEES | 5242 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\receive_flow_features.parquet | 270693 |
| 1 | 2026-07-08 | NSE | KOTAKBANK | 4945 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\receive_flow_features.parquet | 258423 |
| 1 | 2026-07-08 | NSE | LT | 6329 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=LT\receive_flow_features.parquet | 319812 |
| 1 | 2026-07-08 | NSE | M&M | 6038 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=M&M\receive_flow_features.parquet | 309993 |
| 1 | 2026-07-08 | NSE | MARUTI | 4918 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\receive_flow_features.parquet | 236423 |
| 1 | 2026-07-08 | NSE | NESTLEIND | 2944 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\receive_flow_features.parquet | 147957 |
| 1 | 2026-07-08 | NSE | NIFTYBEES | 5017 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\receive_flow_features.parquet | 266167 |
| 1 | 2026-07-08 | NSE | ONGC | 4122 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\receive_flow_features.parquet | 219302 |
| 1 | 2026-07-08 | NSE | RELIANCE | 6548 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\receive_flow_features.parquet | 343213 |
| 1 | 2026-07-08 | NSE | SBIN | 5500 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\receive_flow_features.parquet | 289968 |
| 1 | 2026-07-08 | NSE | SUNPHARMA | 3353 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\receive_flow_features.parquet | 167538 |
| 1 | 2026-07-08 | NSE | TCS | 3905 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=TCS\receive_flow_features.parquet | 198772 |
| 1 | 2026-07-08 | NSE | TECHM | 2803 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\receive_flow_features.parquet | 141121 |
| 1 | 2026-07-08 | NSE | ULTRACEMCO | 3044 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ULTRACEMCO\receive_flow_features.parquet | 144642 |
| 1 | 2026-07-08 | NSE | WIPRO | 2626 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=WIPRO\receive_flow_features.parquet | 137348 |
| 1 | 2026-07-09 | NSE | ADANIPORTS | 5554 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ADANIPORTS\receive_flow_features.parquet | 260865 |
| 1 | 2026-07-09 | NSE | AXISBANK | 7447 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=AXISBANK\receive_flow_features.parquet | 369139 |
| 1 | 2026-07-09 | NSE | BAJAJ-AUTO | 5050 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_features.parquet | 230483 |
| 1 | 2026-07-09 | NSE | BANKBEES | 8886 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BANKBEES\receive_flow_features.parquet | 424665 |
| 1 | 2026-07-09 | NSE | BHARTIARTL | 9412 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BHARTIARTL\receive_flow_features.parquet | 480904 |
| 1 | 2026-07-09 | NSE | BPCL | 4697 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BPCL\receive_flow_features.parquet | 224881 |
| 1 | 2026-07-09 | NSE | BRITANNIA | 4230 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BRITANNIA\receive_flow_features.parquet | 195949 |
| 1 | 2026-07-09 | NSE | CIPLA | 4887 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=CIPLA\receive_flow_features.parquet | 228232 |
| 1 | 2026-07-09 | NSE | DRREDDY | 9054 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=DRREDDY\receive_flow_features.parquet | 463284 |
| 1 | 2026-07-09 | NSE | GOLDBEES | 6408 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=GOLDBEES\receive_flow_features.parquet | 314947 |
| 1 | 2026-07-09 | NSE | HCLTECH | 5478 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=HCLTECH\receive_flow_features.parquet | 263699 |
| 1 | 2026-07-09 | NSE | HDFCBANK | 9420 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=HDFCBANK\receive_flow_features.parquet | 499782 |
| 1 | 2026-07-09 | NSE | HINDUNILVR | 6947 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=HINDUNILVR\receive_flow_features.parquet | 337762 |
| 1 | 2026-07-09 | NSE | ICICIBANK | 9153 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ICICIBANK\receive_flow_features.parquet | 472798 |
| 1 | 2026-07-09 | NSE | INFY | 7567 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=INFY\receive_flow_features.parquet | 379825 |
| 1 | 2026-07-09 | NSE | ITBEES | 3873 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ITBEES\receive_flow_features.parquet | 190336 |
| 1 | 2026-07-09 | NSE | ITC | 7310 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ITC\receive_flow_features.parquet | 355705 |
| 1 | 2026-07-09 | NSE | JUNIORBEES | 8590 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=JUNIORBEES\receive_flow_features.parquet | 411872 |
| 1 | 2026-07-09 | NSE | KOTAKBANK | 8944 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=KOTAKBANK\receive_flow_features.parquet | 464426 |
| 1 | 2026-07-09 | NSE | LT | 9073 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=LT\receive_flow_features.parquet | 458970 |
| 1 | 2026-07-09 | NSE | M&M | 7705 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=M&M\receive_flow_features.parquet | 384625 |
| 1 | 2026-07-09 | NSE | MARUTI | 7380 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=MARUTI\receive_flow_features.parquet | 328206 |
| 1 | 2026-07-09 | NSE | NESTLEIND | 4455 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=NESTLEIND\receive_flow_features.parquet | 213410 |
| 1 | 2026-07-09 | NSE | NIFTYBEES | 8020 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=NIFTYBEES\receive_flow_features.parquet | 394094 |
| 1 | 2026-07-09 | NSE | ONGC | 5783 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ONGC\receive_flow_features.parquet | 281386 |
| 1 | 2026-07-09 | NSE | RELIANCE | 9018 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=RELIANCE\receive_flow_features.parquet | 471087 |
| 1 | 2026-07-09 | NSE | SBIN | 7834 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=SBIN\receive_flow_features.parquet | 399105 |
| 1 | 2026-07-09 | NSE | SUNPHARMA | 7323 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=SUNPHARMA\receive_flow_features.parquet | 354683 |
| 1 | 2026-07-09 | NSE | TCS | 7970 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=TCS\receive_flow_features.parquet | 400735 |
| 1 | 2026-07-09 | NSE | TECHM | 4930 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=TECHM\receive_flow_features.parquet | 238421 |
| 1 | 2026-07-09 | NSE | ULTRACEMCO | 3980 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ULTRACEMCO\receive_flow_features.parquet | 181176 |
| 1 | 2026-07-09 | NSE | WIPRO | 5789 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=WIPRO\receive_flow_features.parquet | 285270 |
| 1 | 2026-07-10 | NSE | ADANIPORTS | 9547 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\receive_flow_features.parquet | 458544 |
| 1 | 2026-07-10 | NSE | AXISBANK | 10802 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\receive_flow_features.parquet | 522405 |
| 1 | 2026-07-10 | NSE | BAJAJ-AUTO | 9728 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_features.parquet | 425829 |
| 1 | 2026-07-10 | NSE | BANKBEES | 9231 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\receive_flow_features.parquet | 433624 |
| 1 | 2026-07-10 | NSE | BHARTIARTL | 11366 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\receive_flow_features.parquet | 549939 |
| 1 | 2026-07-10 | NSE | BPCL | 6759 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\receive_flow_features.parquet | 322343 |
| 1 | 2026-07-10 | NSE | BRITANNIA | 6030 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\receive_flow_features.parquet | 264917 |
| 1 | 2026-07-10 | NSE | CIPLA | 7908 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\receive_flow_features.parquet | 360859 |
| 1 | 2026-07-10 | NSE | DRREDDY | 13142 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=DRREDDY\receive_flow_features.parquet | 653965 |
| 1 | 2026-07-10 | NSE | GOLDBEES | 9150 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=GOLDBEES\receive_flow_features.parquet | 434172 |
| 1 | 2026-07-10 | NSE | HCLTECH | 14318 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=HCLTECH\receive_flow_features.parquet | 699675 |
| 1 | 2026-07-10 | NSE | HDFCBANK | 15044 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=HDFCBANK\receive_flow_features.parquet | 764743 |
| 1 | 2026-07-10 | NSE | HINDUNILVR | 8662 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=HINDUNILVR\receive_flow_features.parquet | 414963 |
| 1 | 2026-07-10 | NSE | ICICIBANK | 11237 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ICICIBANK\receive_flow_features.parquet | 546845 |
| 1 | 2026-07-10 | NSE | INFY | 15211 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=INFY\receive_flow_features.parquet | 769812 |
| 1 | 2026-07-10 | NSE | ITBEES | 6824 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ITBEES\receive_flow_features.parquet | 320859 |
| 1 | 2026-07-10 | NSE | ITC | 11085 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ITC\receive_flow_features.parquet | 533870 |
| 1 | 2026-07-10 | NSE | JUNIORBEES | 13254 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=JUNIORBEES\receive_flow_features.parquet | 641516 |
| 1 | 2026-07-10 | NSE | KOTAKBANK | 10165 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=KOTAKBANK\receive_flow_features.parquet | 488264 |
| 1 | 2026-07-10 | NSE | LT | 10641 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=LT\receive_flow_features.parquet | 503554 |
| 1 | 2026-07-10 | NSE | M&M | 9988 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=M&M\receive_flow_features.parquet | 473838 |
| 1 | 2026-07-10 | NSE | MARUTI | 11105 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=MARUTI\receive_flow_features.parquet | 497095 |
| 1 | 2026-07-10 | NSE | NESTLEIND | 7879 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=NESTLEIND\receive_flow_features.parquet | 369614 |
| 1 | 2026-07-10 | NSE | NIFTYBEES | 11228 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=NIFTYBEES\receive_flow_features.parquet | 540324 |
| 1 | 2026-07-10 | NSE | ONGC | 9396 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ONGC\receive_flow_features.parquet | 453611 |
| 1 | 2026-07-10 | NSE | RELIANCE | 11460 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=RELIANCE\receive_flow_features.parquet | 553044 |
| 1 | 2026-07-10 | NSE | SBIN | 12206 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=SBIN\receive_flow_features.parquet | 612762 |
| 1 | 2026-07-10 | NSE | SUNPHARMA | 9909 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=SUNPHARMA\receive_flow_features.parquet | 464041 |
| 1 | 2026-07-10 | NSE | TCS | 16260 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=TCS\receive_flow_features.parquet | 814692 |
| 1 | 2026-07-10 | NSE | TECHM | 9552 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=TECHM\receive_flow_features.parquet | 455919 |
| 1 | 2026-07-10 | NSE | ULTRACEMCO | 6526 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ULTRACEMCO\receive_flow_features.parquet | 286682 |
| 1 | 2026-07-10 | NSE | WIPRO | 10158 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=WIPRO\receive_flow_features.parquet | 490268 |
| 1 | 2026-07-13 | NSE | ADANIPORTS | 9454 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ADANIPORTS\receive_flow_features.parquet | 440118 |
| 1 | 2026-07-13 | NSE | AXISBANK | 10798 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=AXISBANK\receive_flow_features.parquet | 525831 |
| 1 | 2026-07-13 | NSE | BAJAJ-AUTO | 14299 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_features.parquet | 653935 |
| 1 | 2026-07-13 | NSE | BANKBEES | 13184 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BANKBEES\receive_flow_features.parquet | 604448 |
| 1 | 2026-07-13 | NSE | BHARTIARTL | 11539 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BHARTIARTL\receive_flow_features.parquet | 559836 |
| 1 | 2026-07-13 | NSE | BPCL | 8035 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BPCL\receive_flow_features.parquet | 372981 |
| 1 | 2026-07-13 | NSE | BRITANNIA | 6760 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BRITANNIA\receive_flow_features.parquet | 300416 |
| 1 | 2026-07-13 | NSE | CIPLA | 8388 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=CIPLA\receive_flow_features.parquet | 390621 |
| 1 | 2026-07-13 | NSE | DRREDDY | 8736 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=DRREDDY\receive_flow_features.parquet | 410864 |
| 1 | 2026-07-13 | NSE | GOLDBEES | 8948 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=GOLDBEES\receive_flow_features.parquet | 424803 |
| 1 | 2026-07-13 | NSE | HCLTECH | 14297 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=HCLTECH\receive_flow_features.parquet | 740965 |
| 1 | 2026-07-13 | NSE | HDFCBANK | 16566 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=HDFCBANK\receive_flow_features.parquet | 871706 |
| 1 | 2026-07-13 | NSE | HINDUNILVR | 8592 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=HINDUNILVR\receive_flow_features.parquet | 404356 |
| 1 | 2026-07-13 | NSE | ICICIBANK | 13717 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ICICIBANK\receive_flow_features.parquet | 701011 |
| 1 | 2026-07-13 | NSE | INFY | 16207 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=INFY\receive_flow_features.parquet | 858311 |
| 1 | 2026-07-13 | NSE | ITBEES | 8306 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ITBEES\receive_flow_features.parquet | 394776 |
| 1 | 2026-07-13 | NSE | ITC | 8758 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ITC\receive_flow_features.parquet | 404714 |
| 1 | 2026-07-13 | NSE | JUNIORBEES | 11802 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=JUNIORBEES\receive_flow_features.parquet | 568034 |
| 1 | 2026-07-13 | NSE | KOTAKBANK | 9403 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=KOTAKBANK\receive_flow_features.parquet | 450327 |
| 1 | 2026-07-13 | NSE | LT | 11479 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=LT\receive_flow_features.parquet | 548503 |
| 1 | 2026-07-13 | NSE | M&M | 14146 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=M&M\receive_flow_features.parquet | 671251 |
| 1 | 2026-07-13 | NSE | MARUTI | 15407 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=MARUTI\receive_flow_features.parquet | 691867 |
| 1 | 2026-07-13 | NSE | NESTLEIND | 9036 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=NESTLEIND\receive_flow_features.parquet | 437809 |
| 1 | 2026-07-13 | NSE | NIFTYBEES | 13040 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=NIFTYBEES\receive_flow_features.parquet | 651115 |
| 1 | 2026-07-13 | NSE | ONGC | 10645 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ONGC\receive_flow_features.parquet | 530307 |
| 1 | 2026-07-13 | NSE | RELIANCE | 13220 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=RELIANCE\receive_flow_features.parquet | 668013 |
| 1 | 2026-07-13 | NSE | SBIN | 13085 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=SBIN\receive_flow_features.parquet | 659280 |
| 1 | 2026-07-13 | NSE | SUNPHARMA | 9573 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=SUNPHARMA\receive_flow_features.parquet | 450643 |
| 1 | 2026-07-13 | NSE | TCS | 16807 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=TCS\receive_flow_features.parquet | 872545 |
| 1 | 2026-07-13 | NSE | TECHM | 11317 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=TECHM\receive_flow_features.parquet | 563801 |
| 1 | 2026-07-13 | NSE | ULTRACEMCO | 6784 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ULTRACEMCO\receive_flow_features.parquet | 298595 |
| 1 | 2026-07-13 | NSE | WIPRO | 11491 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=WIPRO\receive_flow_features.parquet | 599285 |
| 1 | 2026-07-14 | NSE | ADANIPORTS | 9871 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ADANIPORTS\receive_flow_features.parquet | 476236 |
| 1 | 2026-07-14 | NSE | AXISBANK | 12369 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=AXISBANK\receive_flow_features.parquet | 607772 |
| 1 | 2026-07-14 | NSE | BAJAJ-AUTO | 15119 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_features.parquet | 692929 |
| 1 | 2026-07-14 | NSE | BANKBEES | 12042 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BANKBEES\receive_flow_features.parquet | 575338 |
| 1 | 2026-07-14 | NSE | BHARTIARTL | 13068 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BHARTIARTL\receive_flow_features.parquet | 656369 |
| 1 | 2026-07-14 | NSE | BPCL | 8730 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BPCL\receive_flow_features.parquet | 417062 |
| 1 | 2026-07-14 | NSE | BRITANNIA | 8238 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BRITANNIA\receive_flow_features.parquet | 366534 |
| 1 | 2026-07-14 | NSE | CIPLA | 8978 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=CIPLA\receive_flow_features.parquet | 421327 |
| 1 | 2026-07-14 | NSE | DRREDDY | 8456 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=DRREDDY\receive_flow_features.parquet | 395548 |
| 1 | 2026-07-14 | NSE | GOLDBEES | 9933 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=GOLDBEES\receive_flow_features.parquet | 483249 |
| 1 | 2026-07-14 | NSE | HCLTECH | 15678 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=HCLTECH\receive_flow_features.parquet | 800460 |
| 1 | 2026-07-14 | NSE | HDFCBANK | 15864 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=HDFCBANK\receive_flow_features.parquet | 818226 |
| 1 | 2026-07-14 | NSE | HINDUNILVR | 10846 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=HINDUNILVR\receive_flow_features.parquet | 519547 |
| 1 | 2026-07-14 | NSE | ICICIBANK | 13574 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ICICIBANK\receive_flow_features.parquet | 691440 |
| 1 | 2026-07-14 | NSE | INFY | 15629 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=INFY\receive_flow_features.parquet | 801633 |
| 1 | 2026-07-14 | NSE | ITBEES | 6618 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ITBEES\receive_flow_features.parquet | 318743 |
| 1 | 2026-07-14 | NSE | ITC | 12350 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ITC\receive_flow_features.parquet | 617708 |
| 1 | 2026-07-14 | NSE | JUNIORBEES | 11963 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=JUNIORBEES\receive_flow_features.parquet | 573407 |
| 1 | 2026-07-14 | NSE | KOTAKBANK | 11204 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=KOTAKBANK\receive_flow_features.parquet | 559734 |
| 1 | 2026-07-14 | NSE | LT | 12561 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=LT\receive_flow_features.parquet | 604800 |
| 1 | 2026-07-14 | NSE | M&M | 13068 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=M&M\receive_flow_features.parquet | 629012 |
| 1 | 2026-07-14 | NSE | MARUTI | 11008 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=MARUTI\receive_flow_features.parquet | 491933 |
| 1 | 2026-07-14 | NSE | NESTLEIND | 9368 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=NESTLEIND\receive_flow_features.parquet | 443292 |
| 1 | 2026-07-14 | NSE | NIFTYBEES | 11590 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=NIFTYBEES\receive_flow_features.parquet | 574909 |
| 1 | 2026-07-14 | NSE | ONGC | 10278 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ONGC\receive_flow_features.parquet | 513706 |
| 1 | 2026-07-14 | NSE | RELIANCE | 13625 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=RELIANCE\receive_flow_features.parquet | 691314 |
| 1 | 2026-07-14 | NSE | SBIN | 12764 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=SBIN\receive_flow_features.parquet | 640612 |
| 1 | 2026-07-14 | NSE | SUNPHARMA | 11509 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=SUNPHARMA\receive_flow_features.parquet | 555076 |
| 1 | 2026-07-14 | NSE | TCS | 15792 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=TCS\receive_flow_features.parquet | 793500 |
| 1 | 2026-07-14 | NSE | TECHM | 11095 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=TECHM\receive_flow_features.parquet | 539034 |
| 1 | 2026-07-14 | NSE | ULTRACEMCO | 7965 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ULTRACEMCO\receive_flow_features.parquet | 351136 |
| 1 | 2026-07-14 | NSE | WIPRO | 9396 | derived_real_l2_receive_flow_features_phase176\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=WIPRO\receive_flow_features.parquet | 465864 |
| 5 | 2026-07-08 | NSE | ADANIPORTS | 1618 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\receive_flow_features.parquet | 98415 |
| 5 | 2026-07-08 | NSE | AXISBANK | 1700 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\receive_flow_features.parquet | 106193 |
| 5 | 2026-07-08 | NSE | BAJAJ-AUTO | 1595 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_features.parquet | 89620 |
| 5 | 2026-07-08 | NSE | BANKBEES | 1694 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\receive_flow_features.parquet | 107210 |
| 5 | 2026-07-08 | NSE | BHARTIARTL | 1617 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\receive_flow_features.parquet | 99817 |
| 5 | 2026-07-08 | NSE | BPCL | 1579 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\receive_flow_features.parquet | 94496 |
| 5 | 2026-07-08 | NSE | BRITANNIA | 1526 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\receive_flow_features.parquet | 86013 |
| 5 | 2026-07-08 | NSE | CIPLA | 1573 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\receive_flow_features.parquet | 92188 |
| 5 | 2026-07-08 | NSE | DRREDDY | 1583 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\receive_flow_features.parquet | 95120 |
| 5 | 2026-07-08 | NSE | GOLDBEES | 1643 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\receive_flow_features.parquet | 100815 |
| 5 | 2026-07-08 | NSE | HCLTECH | 1565 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\receive_flow_features.parquet | 94556 |
| 5 | 2026-07-08 | NSE | HDFCBANK | 1746 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\receive_flow_features.parquet | 111542 |
| 5 | 2026-07-08 | NSE | HINDUNILVR | 1619 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\receive_flow_features.parquet | 98971 |
| 5 | 2026-07-08 | NSE | ICICIBANK | 1723 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\receive_flow_features.parquet | 107127 |
| 5 | 2026-07-08 | NSE | INFY | 1683 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=INFY\receive_flow_features.parquet | 102832 |
| 5 | 2026-07-08 | NSE | ITBEES | 1586 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\receive_flow_features.parquet | 92281 |
| 5 | 2026-07-08 | NSE | ITC | 1644 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ITC\receive_flow_features.parquet | 100054 |
| 5 | 2026-07-08 | NSE | JUNIORBEES | 1686 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\receive_flow_features.parquet | 107430 |
| 5 | 2026-07-08 | NSE | KOTAKBANK | 1665 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\receive_flow_features.parquet | 102539 |
| 5 | 2026-07-08 | NSE | LT | 1734 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=LT\receive_flow_features.parquet | 108071 |
| 5 | 2026-07-08 | NSE | M&M | 1715 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=M&M\receive_flow_features.parquet | 108525 |
| 5 | 2026-07-08 | NSE | MARUTI | 1680 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\receive_flow_features.parquet | 98295 |
| 5 | 2026-07-08 | NSE | NESTLEIND | 1581 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\receive_flow_features.parquet | 94349 |
| 5 | 2026-07-08 | NSE | NIFTYBEES | 1688 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\receive_flow_features.parquet | 106580 |
| 5 | 2026-07-08 | NSE | ONGC | 1629 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\receive_flow_features.parquet | 103657 |
| 5 | 2026-07-08 | NSE | RELIANCE | 1732 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\receive_flow_features.parquet | 107613 |
| 5 | 2026-07-08 | NSE | SBIN | 1687 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\receive_flow_features.parquet | 105449 |
| 5 | 2026-07-08 | NSE | SUNPHARMA | 1601 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\receive_flow_features.parquet | 94680 |
| 5 | 2026-07-08 | NSE | TCS | 1652 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=TCS\receive_flow_features.parquet | 100411 |
| 5 | 2026-07-08 | NSE | TECHM | 1575 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\receive_flow_features.parquet | 93652 |
| 5 | 2026-07-08 | NSE | ULTRACEMCO | 1578 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ULTRACEMCO\receive_flow_features.parquet | 88770 |
| 5 | 2026-07-08 | NSE | WIPRO | 1570 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=WIPRO\receive_flow_features.parquet | 97238 |
| 5 | 2026-07-09 | NSE | ADANIPORTS | 2449 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ADANIPORTS\receive_flow_features.parquet | 139827 |
| 5 | 2026-07-09 | NSE | AXISBANK | 2523 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=AXISBANK\receive_flow_features.parquet | 149799 |
| 5 | 2026-07-09 | NSE | BAJAJ-AUTO | 2391 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_features.parquet | 128057 |
| 5 | 2026-07-09 | NSE | BANKBEES | 2538 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BANKBEES\receive_flow_features.parquet | 147233 |
| 5 | 2026-07-09 | NSE | BHARTIARTL | 2559 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BHARTIARTL\receive_flow_features.parquet | 151734 |
| 5 | 2026-07-09 | NSE | BPCL | 2422 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BPCL\receive_flow_features.parquet | 139531 |
| 5 | 2026-07-09 | NSE | BRITANNIA | 2365 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BRITANNIA\receive_flow_features.parquet | 125708 |
| 5 | 2026-07-09 | NSE | CIPLA | 2408 | derived_real_l2_receive_flow_features_phase176\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=CIPLA\receive_flow_features.parquet | 136590 |

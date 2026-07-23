# Phase176 Receive-flow Feature Materializer

Generated UTC: 2026-07-23T19:01:26.367624+00:00

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
| phase176_activation_ready | 0 | Inherited Phase175 activation gate |
| phase176_features_materialized | 0 | 1 means feature parquet was materialized |
| phase176_strategy_replay_allowed | 0 | No strategy replay opened |
| phase176_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase176_forbidden_outputs | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | Outputs forbidden in this phase |
| phase176_next_best_action | add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_then_rerun_phase174_phase172_phase175_before_phase176_materialization | Recommended next milestone |

## Materialization Plan

| feature_id | feature_family | materialization_status | target_layout | allowed_horizons | minimum_source_days | leakage_control | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P175_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | gated_pending_phase175_activation | derived_real_l2_receive_flow_features_phase176\trade_date=YYYY-MM-DD\exchange=NSE\symbol=SYMBOL\p175_receive_event_rate_zscore.parquet | 1s;5s;15s;60s with coverage/staleness reporting | 5 | baseline statistics fitted on train dates only before test-date transform | 0 |
| P175_QUOTE_CHURN_RATE | book_state_churn | gated_pending_phase175_activation | derived_real_l2_receive_flow_features_phase176\trade_date=YYYY-MM-DD\exchange=NSE\symbol=SYMBOL\p175_quote_churn_rate.parquet | 1s;5s;15s;60s with symbol-specific coverage gates | 5 | computed only from events received at or before the feature timestamp | 0 |
| P175_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | gated_pending_phase175_activation | derived_real_l2_receive_flow_features_phase176\trade_date=YYYY-MM-DD\exchange=NSE\symbol=SYMBOL\p175_depth_refresh_intensity.parquet | 1s;5s;15s;60s with depth-field completeness gates | 5 | uses top-five market-by-price state only; no inferred hidden order events | 0 |
| P175_STALE_QUOTE_DURATION | feed_staleness | gated_pending_phase175_activation | derived_real_l2_receive_flow_features_phase176\trade_date=YYYY-MM-DD\exchange=NSE\symbol=SYMBOL\p175_stale_quote_duration.parquet | event_time;1s;5s;15s | 5 | forward state duration censored at the current timestamp; no future duration completion | 0 |
| P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | gated_pending_phase175_activation | derived_real_l2_receive_flow_features_phase176\trade_date=YYYY-MM-DD\exchange=NSE\symbol=SYMBOL\p175_cross_symbol_arrival_synchrony.parquet | 1s native synchrony source plus 5s/15s aggregations | 5 | computed from contemporaneous receive buckets only; target symbol exclusion required in ablation | 0 |
| P175_RECEIVE_FLOW_REGIME_STATE | source_quality_context | gated_pending_phase175_activation | derived_real_l2_receive_flow_features_phase176\trade_date=YYYY-MM-DD\exchange=NSE\symbol=SYMBOL\p175_receive_flow_regime_state.parquet | daily fitted context with intraday labels | 5 | fit context model on train dates only; report train/test date separation | 0 |

## DuckDB SQL Templates

| template_id | purpose | sql_template | output_path | strategy_replay_allowed |
| --- | --- | --- | --- | --- |
| P176_BASE_RECEIVE_EVENTS | local-only source view over downloaded Zerodha top-five market-by-price Parquet | SELECT trade_date, exchange, tradingsymbol AS symbol, collector_received_utc_ms AS receive_ms, buy_1_price, buy_1_quantity, sell_1_price, sell_1_quantity, buy_1_quantity, buy_2_quantity, buy_3_quantity, buy_4_quantity, buy_5_quantity, sell_1_quantity, sell_2_quantity, sell_3_quantity, sell_4_quantity, sell_5_quantity FROM read_parquet('real_data_sample/l2_multiday_panel/trade_date=*/exchange=NSE/symbol=*/*.parquet', hive_partitioning=true, union_by_name=true) |  | 0 |
| P176_1S_BUCKET_FEATURES | 1-second bucket receive-event/churn/staleness/synchrony features after activation opens | WITH ordered AS (... event-time sorted source ...), buckets AS (... floor(receive_ms/1000) ... ) SELECT trade_date, exchange, symbol, bucket_1s, receive_event_count, quote_churn_count, depth_refresh_count, stale_quote_duration_ms, cross_symbol_arrival_count FROM buckets | derived_real_l2_receive_flow_features_phase176\horizon=1s | 0 |
| P176_5S_15S_60S_AGGREGATIONS | higher-horizon aggregations from already materialized 1-second features | SELECT trade_date, exchange, symbol, horizon, bucket_ts, aggregate_receive_flow_features FROM phase176_1s_features GROUP BY trade_date, exchange, symbol, horizon, bucket_ts | derived_real_l2_receive_flow_features_phase176\horizon={5s,15s,60s} | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P176_PHASE175_ACTIVATION_READY | 0 | phase175_activation_ready=0;ready_dates=3;additional_needed=2 | activation |
| P176_SCHEMA_AVAILABLE | 1 | feature_schema_rows=6 | hard |
| P176_LOCAL_REAL_ROOT_EXISTS | 1 | real_data_sample\l2_multiday_panel | hard |
| P176_NO_REPLAY_OR_PROFITABILITY_OUTPUTS | 1 | materializer scaffold only while activation gate is closed; forbidden_outputs=buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | hard |

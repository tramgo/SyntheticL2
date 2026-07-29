# Phase253 Richer Raw Top-five Depth Feature-materialization Precommit

Generated UTC: 2026-07-29T10:17:10.280210+00:00

Phase253 precommits the next executable materializer for raw Zerodha top-five market-by-price depth.
It is a precommit only: no new downloads, no replay, no strategy promotion, no paper/live acceptance and no profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase253_richer_raw_depth_precommit_complete | 1 | Phase253 richer raw-depth materialization precommit completed |
| phase253_raw_root_rows | 3 | Raw roots inspected |
| phase253_usable_raw_root_rows | 3 | Local raw roots usable without new download |
| phase253_schema_present_rows | 38 | Core/raw depth fields present |
| phase253_schema_rows | 38 | Core/raw depth fields required |
| phase253_raw_depth_level_columns | 30 | Explicit buy/sell level 1-5 price/quantity/order columns |
| phase253_feature_catalog_rows | 26 | Feature catalog rows |
| phase253_materialization_contract_rows | 10 | Materialization contract rows |
| phase253_hard_gate_pass_rows | 6 | Hard gates passed |
| phase253_hard_gate_rows | 6 | Hard gates evaluated |
| phase253_phase254_materialization_allowed_next | 1 | Whether Phase254 materialization is allowed next |
| phase253_download_more_dates_now_allowed | 0 | No raw-date download in Phase253 |
| phase253_replay_execution_allowed_now | 0 | No replay execution in Phase253 |
| phase253_strategy_promotion_allowed | 0 | No strategy promotion from Phase253 |
| phase253_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase253 |
| phase253_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase253 |
| phase253_next_best_action | run_phase254_materialize_richer_raw_top5_depth_event_bars_existing_raw_only_no_paper_live | Recommended next milestone |

## Raw Root Inventory

| raw_root | exists | trade_date_dir_rows | sample_parquet_rows | sample_path | usable_without_new_download |
| --- | --- | --- | --- | --- | --- |
| real_data_sample\l2_multiday_panel | 1 | 7 | 3 | real_data_sample\l2_multiday_panel\trade_date=2026-07-16\exchange=NSE\symbol=ADANIPORTS\part-034500_837289-000001.parquet | 1 |
| real_data_sample\l2_unseen_validation | 1 | 2 | 3 | real_data_sample\l2_unseen_validation\trade_date=2026-07-20\exchange=NSE\symbol=ADANIPORTS\part-034500_938067-000001.parquet | 1 |
| real_data_sample\l2_single_day | 1 | 0 | 3 | real_data_sample\l2_single_day\symbol=ADANIPORTS\part-034501_461115-000006.parquet | 1 |

## Raw Schema Contract

| column | column_group | required_for_phase254 | present_in_sample_schema |
| --- | --- | --- | --- |
| collector_received_utc | core_tick | 1 | 1 |
| collector_received_utc_ms | core_tick | 1 | 1 |
| trade_date | core_tick | 1 | 1 |
| exchange | core_tick | 1 | 1 |
| tradingsymbol | core_tick | 1 | 1 |
| last_price | core_tick | 1 | 1 |
| last_traded_quantity | core_tick | 1 | 1 |
| volume_traded | core_tick | 1 | 1 |
| buy_1_price | raw_depth_l1_to_l5 | 1 | 1 |
| buy_1_quantity | raw_depth_l1_to_l5 | 1 | 1 |
| buy_1_orders | raw_depth_l1_to_l5 | 1 | 1 |
| buy_2_price | raw_depth_l1_to_l5 | 1 | 1 |
| buy_2_quantity | raw_depth_l1_to_l5 | 1 | 1 |
| buy_2_orders | raw_depth_l1_to_l5 | 1 | 1 |
| buy_3_price | raw_depth_l1_to_l5 | 1 | 1 |
| buy_3_quantity | raw_depth_l1_to_l5 | 1 | 1 |
| buy_3_orders | raw_depth_l1_to_l5 | 1 | 1 |
| buy_4_price | raw_depth_l1_to_l5 | 1 | 1 |
| buy_4_quantity | raw_depth_l1_to_l5 | 1 | 1 |
| buy_4_orders | raw_depth_l1_to_l5 | 1 | 1 |
| buy_5_price | raw_depth_l1_to_l5 | 1 | 1 |
| buy_5_quantity | raw_depth_l1_to_l5 | 1 | 1 |
| buy_5_orders | raw_depth_l1_to_l5 | 1 | 1 |
| sell_1_price | raw_depth_l1_to_l5 | 1 | 1 |
| sell_1_quantity | raw_depth_l1_to_l5 | 1 | 1 |
| sell_1_orders | raw_depth_l1_to_l5 | 1 | 1 |
| sell_2_price | raw_depth_l1_to_l5 | 1 | 1 |
| sell_2_quantity | raw_depth_l1_to_l5 | 1 | 1 |
| sell_2_orders | raw_depth_l1_to_l5 | 1 | 1 |
| sell_3_price | raw_depth_l1_to_l5 | 1 | 1 |
| sell_3_quantity | raw_depth_l1_to_l5 | 1 | 1 |
| sell_3_orders | raw_depth_l1_to_l5 | 1 | 1 |
| sell_4_price | raw_depth_l1_to_l5 | 1 | 1 |
| sell_4_quantity | raw_depth_l1_to_l5 | 1 | 1 |
| sell_4_orders | raw_depth_l1_to_l5 | 1 | 1 |
| sell_5_price | raw_depth_l1_to_l5 | 1 | 1 |
| sell_5_quantity | raw_depth_l1_to_l5 | 1 | 1 |
| sell_5_orders | raw_depth_l1_to_l5 | 1 | 1 |

## Richer Depth Feature Catalog

| feature_name | feature_group | definition | purpose |
| --- | --- | --- | --- |
| l1_mid_price | level_1_price | mean of buy_1_price and sell_1_price | top-of-book price anchor |
| l1_spread | level_1_price | sell_1_price minus buy_1_price | spread and tradability guard |
| level_n_spread_1_to_5 | per_level_price | sell_n_price minus buy_n_price for n=1..5 | per-level book-width shape |
| buy_quantity_1_to_5 | per_level_quantity | buy_n_quantity for n=1..5 | visible bid-side depth by level |
| sell_quantity_1_to_5 | per_level_quantity | sell_n_quantity for n=1..5 | visible ask-side depth by level |
| buy_orders_1_to_5 | per_level_order_count | buy_n_orders for n=1..5 | visible bid queue-count shape |
| sell_orders_1_to_5 | per_level_order_count | sell_n_orders for n=1..5 | visible ask queue-count shape |
| cum_buy_qty_l1_l5 | cumulative_depth | sum buy_1_quantity..buy_5_quantity | full visible bid depth |
| cum_sell_qty_l1_l5 | cumulative_depth | sum sell_1_quantity..sell_5_quantity | full visible ask depth |
| cum_top5_qty_imbalance | cumulative_depth | (cum_buy_qty_l1_l5 - cum_sell_qty_l1_l5)/(cum_buy_qty_l1_l5 + cum_sell_qty_l1_l5) | full visible depth imbalance |
| depth_beyond_l1_qty_imbalance | depth_beyond_l1 | levels 2..5 bid/ask imbalance | separate deeper book pressure from top-of-book |
| level_weighted_depth_imbalance | weighted_depth | near-level weighted bid/ask imbalance across levels 1..5 | book pressure emphasizing executable levels |
| depth_slope_bid | depth_shape | slope of bid quantities across levels 1..5 | bid-side depth shape |
| depth_slope_ask | depth_shape | slope of ask quantities across levels 1..5 | ask-side depth shape |
| depth_convexity_bid | depth_shape | curvature of bid quantities across levels 1..5 | bid-side replenishment shape |
| depth_convexity_ask | depth_shape | curvature of ask quantities across levels 1..5 | ask-side replenishment shape |
| order_count_imbalance_l1_l5 | order_count_shape | buy order-count total versus sell order-count total | visible queue crowding |
| avg_qty_per_order_bid_l1_l5 | order_size_shape | cum buy quantity divided by cum buy orders | visible bid order-size proxy |
| avg_qty_per_order_ask_l1_l5 | order_size_shape | cum sell quantity divided by cum sell orders | visible ask order-size proxy |
| delta_per_level_qty_1_to_5 | event_sequence | receive-order change in each buy/sell level quantity | add/cancel/consume proxy |
| delta_per_level_orders_1_to_5 | event_sequence | receive-order change in each buy/sell level order count | queue-count transition proxy |
| price_shift_level_1_to_5 | event_sequence | receive-order change in per-level bid/ask prices | book move and queue-roll proxy |
| depth_replenishment_pressure | event_sequence | positive depth deltas after adverse price move | replenishment proxy |
| depth_withdrawal_pressure | event_sequence | negative depth deltas before/with price move | withdrawal proxy |
| top5_book_churn | event_sequence | sum absolute per-level quantity/order changes | book activity independent of trade volume |
| event_bar_future_mid_return | label | future close-mid return over configured event-bar horizons | training target for Phase254+ searches |

## Materialization Contract

| contract_id | requirement | severity |
| --- | --- | --- |
| P253_EXISTING_RAW_ONLY | Phase254 must use existing local raw parquet roots only; no new Azure/raw downloads. | hard |
| P253_EXPLICIT_LEVELS_1_TO_5 | Phase254 must read buy/sell levels 1..5 price, quantity and order-count columns directly. | hard |
| P253_RECEIVE_ORDER_SORT | Ticks must be sorted by trade_date, exchange, symbol, collector_received_utc_ms and monotonic timestamp when present. | hard |
| P253_EVENT_BAR_CLOCK_DECLARED | Event bars must use a declared receive-event clock and retain source tick counts per bar. | hard |
| P253_NO_FORBIDDEN_TUNING | 2026-07-17 and 2026-07-20 remain excluded from downstream parameter selection. | hard |
| P253_LEVEL_SHAPE_FEATURES_REQUIRED | Outputs must include per-level, cumulative, weighted, slope/convexity and order-count features. | hard |
| P253_DELTA_SEQUENCE_FEATURES_REQUIRED | Outputs must include receive-order deltas for per-level quantity, price and order-count changes. | hard |
| P253_SCHEMA_QUALITY_GATES | Outputs must check crossed/locked books, nonpositive quantities, missing levels and invalid sorting. | hard |
| P253_COST_MODEL_CARRIED | Downstream outputs must carry Zerodha modeled cost/spread floor fields before replay. | hard |
| P253_NO_REPLAY_PAPER_LIVE | Phase253 is precommit only; no replay, promotion, paper/live or profitability claim. | hard |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P253_PHASE252_WORK_ORDER_PRESENT | True | run_phase253_richer_raw_top5_depth_feature_materialization_precommit_no_new_downloads_no_paper_live | Phase252 next action targets Phase253 | hard |
| P253_LOCAL_RAW_ROOT_AVAILABLE | True | 3 | >0 usable local raw roots | hard |
| P253_RAW_SCHEMA_PRESENT | True | 38/38 | all core/depth fields present in sample schema | hard |
| P253_FEATURE_CATALOG_WRITTEN | True | 26 | >=20 richer raw-depth features | hard |
| P253_CONTRACT_WRITTEN | True | 10 | >=10 materialization contract rows | hard |
| P253_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

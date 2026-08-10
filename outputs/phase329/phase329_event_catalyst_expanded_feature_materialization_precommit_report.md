# Phase329 Event-Catalyst Expanded Feature Materialization Precommit

Phase329 precommits compact event-symbol feature materialization from the repaired Phase327 and accepted Phase328 expanded top-five-depth join.
It does not materialize features, run strategy search, replay, promote, or claim profitability.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase329_expanded_feature_materialization_precommit_complete | 1 | Phase329 expanded feature materialization precommit completed |
| phase329_feature_catalog_rows | 23 | Feature catalog rows |
| phase329_depth_beyond_l1_feature_rows | 14 | Feature rows using visible depth levels 2-5 |
| phase329_lookahead_target_only_rows | 6 | Target-only lookahead columns explicitly separated |
| phase329_materialization_contract_rows | 14 | Materialization contract rows |
| phase329_processing_work_order_rows | 7 | Processing work-order rows |
| phase329_expected_feature_rows | 1600 | Expected event-symbol feature rows for Phase330 |
| phase329_full_depth_required | 1 | Zerodha visible levels 1-5 required |
| phase329_depth_beyond_l1_required | 1 | Visible levels 2-5 materiality required |
| phase329_l1_only_variant_rows_allowed | 0 | No L1-only variants allowed |
| phase329_net_edge_live_mask_rows_allowed | 0 | No net-edge live lookahead mask allowed |
| phase329_strategy_search_allowed_now | 0 | No strategy search in Phase329 |
| phase329_strategy_replay_allowed | 0 | No replay |
| phase329_strategy_promotion_allowed | 0 | No promotion |
| phase329_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase329_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase329_hard_gate_pass_rows | 11 | Passed hard gates |
| phase329_hard_gate_rows | 11 | Hard gates |
| phase329_next_best_action | run_phase330_event_catalyst_expanded_feature_materialization_no_strategy_search | Recommended next action |

## Feature catalog

| feature_id | formula | feature_family | description | feature_role | phase330_materialization_required | uses_depth_beyond_l1 | lookahead_target_only |
| --- | --- | --- | --- | --- | --- | --- | --- |
| event_clock_relative_second | relative_second | event_clock | Event-relative second from -900 through +1800. | context | 1 | 0 | 0 |
| l1_spread | sell_1_price - buy_1_price | top_of_book_l1 | Best bid/ask spread. | signal | 1 | 0 | 0 |
| l1_mid | (sell_1_price + buy_1_price) / 2 | top_of_book_l1 | Best bid/ask midpoint. | signal | 1 | 0 | 0 |
| l1_microprice | weighted best quote by opposite-side quantity | top_of_book_l1 | Best-level microprice. | signal | 1 | 0 | 0 |
| l1_queue_imbalance | (buy_1_quantity - sell_1_quantity) / total_l1_qty | top_of_book_l1 | Best-level quantity imbalance. | signal | 1 | 0 | 0 |
| depth_l1_l5_qty_imbalance | sum_qty_bid_l1_l5 vs sum_qty_ask_l1_l5 | top_five_depth | Quantity imbalance across Zerodha visible market-by-price levels 1-5. | signal | 1 | 1 | 0 |
| depth_l2_l5_qty_imbalance | sum_qty_bid_l2_l5 vs sum_qty_ask_l2_l5 | top_five_depth_beyond_l1 | Quantity imbalance across visible depth levels 2-5. | signal | 1 | 1 | 0 |
| depth_l1_l5_order_imbalance | sum_orders_bid_l1_l5 vs sum_orders_ask_l1_l5 | top_five_depth | Order-count imbalance across Zerodha visible market-by-price levels 1-5. | signal | 1 | 1 | 0 |
| depth_l2_l5_order_imbalance | sum_orders_bid_l2_l5 vs sum_orders_ask_l2_l5 | top_five_depth_beyond_l1 | Order-count imbalance across visible depth levels 2-5. | signal | 1 | 1 | 0 |
| bid_depth_slope_l1_l5 | buy_1_price - buy_5_price | top_five_depth | Bid-side price ladder slope across levels 1-5. | signal | 1 | 1 | 0 |
| ask_depth_slope_l1_l5 | sell_5_price - sell_1_price | top_five_depth | Ask-side price ladder slope across levels 1-5. | signal | 1 | 1 | 0 |
| l2_l5_depth_share | depth_l2_l5_qty / depth_l1_l5_qty | top_five_depth_beyond_l1 | Share of displayed quantity beyond best bid/ask. | signal | 1 | 1 | 0 |
| depth_pressure | depth_l1_l5_qty_imbalance / max(l1_spread,tick) | top_five_depth | Full visible-depth imbalance normalized by spread. | signal | 1 | 1 | 0 |
| depth_l2_l5_pressure | depth_l2_l5_qty_imbalance / max(l1_spread,tick) | top_five_depth_beyond_l1 | Levels 2-5 imbalance normalized by spread. | signal | 1 | 1 | 0 |
| pre_900s_mean_features | mean(signal features where relative_second < 0) | pre_event_context | Pre-event feature means over the full 900s lead-in. | signal | 1 | 1 | 0 |
| pre_300s_mean_features | mean(signal features where -300 <= relative_second < 0) | pre_event_context | Near-event feature means over the last 300s before the event. | signal | 1 | 1 | 0 |
| event_nearest_features | nearest row to relative_second=0 | event_context | At-event feature snapshot. | signal | 1 | 1 | 0 |
| pre_post_pressure_delta_diagnostic | post depth_pressure minus pre depth_pressure | diagnostic | Pressure shift diagnostic separated from live entry features unless explicitly treated as a target. | diagnostic | 1 | 1 | 1 |
| post_60s_response | midpoint return at +60s from event_mid | target_response | Short response target, excluded from live signal features. | target | 1 | 0 | 1 |
| post_300s_response | midpoint return at +300s from event_mid | target_response | Five-minute response target, excluded from live signal features. | target | 1 | 0 | 1 |
| post_900s_response | midpoint return at +900s from event_mid | target_response | Fifteen-minute response target, excluded from live signal features. | target | 1 | 0 | 1 |
| post_1800s_response | midpoint return at +1800s from event_mid | target_response | Thirty-minute response target, excluded from live signal features. | target | 1 | 0 | 1 |
| post_depth_pressure_shift | post depth_pressure minus pre depth_pressure | target_response | Liquidity-pressure response target, excluded from live signal features. | target | 1 | 1 | 1 |

## Materialization contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P329_INPUT_JOIN | outputs/phase327/phase327_joined_expanded_event_top5_depth.parquet | Use the repaired and Phase328-audited expanded joined parquet. |
| P329_INPUT_QUALITY | outputs/phase328/phase328_acceptance_summary.csv | Require Phase328 quality audit before feature materialization. |
| P329_MIN_JOIN_ROWS | 141708530 | Preserve Phase328 audited joined-row count unless Phase327 is rerun. |
| P329_EVENT_SYMBOL_SCOPE | 50_events_x_32_symbols | Feature matrix should produce one compact row per event and symbol. |
| P329_EXPECTED_FEATURE_ROWS | 1600 | One compact feature row per event-symbol pair. |
| P329_WINDOW | relative_second=-900..1800 | Use only the audited event-relative window. |
| P329_FULL_DEPTH_REQUIRED | zerodha_visible_depth_levels_1_to_5 | Retain full Zerodha top-five market-by-price depth. |
| P329_DEPTH_BEYOND_L1_REQUIRED | visible_depth_levels_2_to_5_material | Feature matrix must include material depth-beyond-L1 features. |
| P329_NO_L1_ONLY_VARIANTS | l1_only_variant_rows=0 | No downstream strategy family may use only top-of-book fields. |
| P329_TARGET_SEPARATION | target_columns_not_live_signal_features | Post-event returns and pressure shifts must be targets/diagnostics, not live signal inputs. |
| P329_NO_NET_EDGE_LIVE_MASK | net_edge_live_mask_rows=0 | No future outcome mask may be used to select live rows. |
| P329_NO_STRATEGY_SEARCH | strategy_search_allowed_now=0 | Precommit only; no P&L, replay or optimization. |
| P329_BOUNDARIES | replay=0;promotion=0;paper=0;claim=0 | No acceptance boundary changes. |
| P329_NEXT | run_phase330_event_catalyst_expanded_feature_materialization_no_strategy_search | Materialize compact expanded feature matrix next. |

## Processing work order

| work_order_id | scope | description |
| --- | --- | --- |
| load_joined_parquet | DuckDB scan over outputs/phase327/phase327_joined_expanded_event_top5_depth.parquet | Avoid loading all 141.7M joined rows into pandas at once. |
| derive_tick_features | SQL expressions for spread, mid, microprice, depth imbalances, depth slopes and pressure | Use Zerodha visible levels 1-5 and depth-beyond-L1 levels 2-5. |
| aggregate_signal_features | group by event_id,event_time_ist,event_type,symbol | Produce compact event-symbol feature rows. |
| preserve_event_symbol_breadth | expect 50 events x 32 symbols = 1600 rows | Reject partial event-symbol feature coverage. |
| separate_targets | post_60s/post_300s/post_900s/post_1800s response columns | Keep target columns explicitly outside live feature set. |
| write_outputs | outputs/phase330/phase330_event_catalyst_expanded_feature_matrix.parquet | Feature materialization target. |
| quality_audit | outputs/phase330/phase330_feature_quality.csv | Validate full-depth features, target separation and 50x32 coverage. |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P329_PHASE328_COMPLETE | True | 1 | 1 | hard |
| P329_PHASE328_JOIN_BREADTH_OK | True | events=50;symbols=32;min_event_symbols=32;min_symbol_events=50 | 50_events_x_32_symbols | hard |
| P329_PHASE328_DEPTH_OK | True | 141708530 | all_joined_rows | hard |
| P329_PHASE328_BOOK_QUALITY_OK | True | crossed=0;bid_sort=0;ask_sort=0 | 0 | hard |
| P329_FEATURE_CATALOG_NONEMPTY | True | 23 | >0 | hard |
| P329_DEPTH_BEYOND_L1_FEATURES_PRESENT | True | 14 | >=9 | hard |
| P329_TARGET_COLUMNS_SEPARATED | True | 6 | >=6 | hard |
| P329_CONTRACT_ROWS_PRESENT | True | 14 | >=14 | hard |
| P329_WORK_ORDER_ROWS_PRESENT | True | 7 | >=7 | hard |
| P329_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P329_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

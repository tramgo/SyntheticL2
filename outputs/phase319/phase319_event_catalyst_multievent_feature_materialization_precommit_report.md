# Phase319 Event-Catalyst Multi-Event Feature Materialization Precommit

Phase319 precommits compact event-symbol feature materialization from the accepted Phase317/318 multi-event top-five depth join.
It does not materialize features, run strategy search, replay, promote, or claim profitability.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase319_multievent_feature_materialization_precommit_complete | 1 | Phase319 multi-event feature materialization precommit completed |
| phase319_feature_catalog_rows | 22 | Feature catalog rows |
| phase319_depth_beyond_l1_feature_rows | 13 | Feature rows using depth levels 2-5 |
| phase319_lookahead_target_only_rows | 5 | Target-only lookahead columns explicitly separated |
| phase319_materialization_contract_rows | 13 | Materialization contract rows |
| phase319_processing_work_order_rows | 6 | Processing work-order rows |
| phase319_full_depth_required | 1 | Depth levels 1-5 required |
| phase319_depth_beyond_l1_required | 1 | Depth levels 2-5 materiality required |
| phase319_l1_only_variant_rows_allowed | 0 | No L1-only variants allowed |
| phase319_net_edge_live_mask_rows_allowed | 0 | No net-edge live lookahead mask allowed |
| phase319_strategy_search_allowed_now | 0 | No strategy search in Phase319 |
| phase319_strategy_replay_allowed | 0 | No replay |
| phase319_strategy_promotion_allowed | 0 | No promotion |
| phase319_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase319_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase319_hard_gate_pass_rows | 10 | Passed hard gates |
| phase319_hard_gate_rows | 10 | Hard gates |
| phase319_next_best_action | run_phase320_event_catalyst_multievent_feature_materialization_no_strategy_search | Recommended next action |

## Feature catalog

| feature_id | formula | feature_family | description | feature_role | phase320_materialization_required | uses_depth_beyond_l1 | lookahead_target_only |
| --- | --- | --- | --- | --- | --- | --- | --- |
| event_clock_relative_second | relative_second | event_clock | Event-relative second from -900 through +1800. | context | 1 | 0 | 0 |
| l1_spread | sell_1_price - buy_1_price | top_of_book | Best bid/ask spread. | signal | 1 | 0 | 0 |
| l1_mid | (sell_1_price + buy_1_price) / 2 | top_of_book | Best bid/ask midpoint. | signal | 1 | 0 | 0 |
| l1_microprice | weighted best quote by opposite-side quantity | top_of_book | Best-level microprice. | signal | 1 | 0 | 0 |
| l1_queue_imbalance | (buy_1_quantity - sell_1_quantity) / total_l1_qty | top_of_book | Best-level quantity imbalance. | signal | 1 | 0 | 0 |
| depth_l1_l5_qty_imbalance | sum_qty_bid_l1_l5 vs sum_qty_ask_l1_l5 | full_depth | Quantity imbalance across depth levels 1-5. | signal | 1 | 1 | 0 |
| depth_l2_l5_qty_imbalance | sum_qty_bid_l2_l5 vs sum_qty_ask_l2_l5 | depth_beyond_l1 | Quantity imbalance across depth levels 2-5. | signal | 1 | 1 | 0 |
| depth_l1_l5_order_imbalance | sum_orders_bid_l1_l5 vs sum_orders_ask_l1_l5 | full_depth | Order-count imbalance across depth levels 1-5. | signal | 1 | 1 | 0 |
| depth_l2_l5_order_imbalance | sum_orders_bid_l2_l5 vs sum_orders_ask_l2_l5 | depth_beyond_l1 | Order-count imbalance across depth levels 2-5. | signal | 1 | 1 | 0 |
| bid_depth_slope_l1_l5 | buy_1_price - buy_5_price | full_depth | Bid-side price ladder slope across depth levels 1-5. | signal | 1 | 1 | 0 |
| ask_depth_slope_l1_l5 | sell_5_price - sell_1_price | full_depth | Ask-side price ladder slope across depth levels 1-5. | signal | 1 | 1 | 0 |
| l2_l5_depth_share | depth_l2_l5_qty / depth_l1_l5_qty | depth_beyond_l1 | Share of displayed quantity beyond top of book. | signal | 1 | 1 | 0 |
| depth_pressure | depth_l1_l5_qty_imbalance / max(l1_spread,tick) | full_depth | Full-depth imbalance normalized by spread. | signal | 1 | 1 | 0 |
| depth_l2_l5_pressure | depth_l2_l5_qty_imbalance / max(l1_spread,tick) | depth_beyond_l1 | Depth-beyond-L1 imbalance normalized by spread. | signal | 1 | 1 | 0 |
| pre_900s_mean_features | mean(signal features where relative_second < 0) | pre_event_context | Pre-event feature means over the full 900s lead-in. | signal | 1 | 1 | 0 |
| pre_300s_mean_features | mean(signal features where -300 <= relative_second < 0) | pre_event_context | Near-event feature means over the last 300s before the event. | signal | 1 | 1 | 0 |
| event_nearest_features | nearest row to relative_second=0 | event_context | At-event feature snapshot. | signal | 1 | 1 | 0 |
| post_60s_response | midpoint return at +60s from event_mid | target_response | Short response target, excluded from live signal features. | target | 1 | 0 | 1 |
| post_300s_response | midpoint return at +300s from event_mid | target_response | Five-minute response target, excluded from live signal features. | target | 1 | 0 | 1 |
| post_900s_response | midpoint return at +900s from event_mid | target_response | Fifteen-minute response target, excluded from live signal features. | target | 1 | 0 | 1 |
| post_1800s_response | midpoint return at +1800s from event_mid | target_response | Thirty-minute response target, excluded from live signal features. | target | 1 | 0 | 1 |
| post_depth_pressure_shift | post depth_pressure minus pre depth_pressure | target_response | Liquidity-pressure response target, excluded from live signal features. | target | 1 | 1 | 1 |

## Materialization contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P319_INPUT_JOIN | outputs/phase317/phase317_joined_multievent_top5_depth.parquet | Use the accepted local Phase317 joined parquet. |
| P319_INPUT_QUALITY | outputs/phase318/phase318_acceptance_summary.csv | Require Phase318 quality audit before feature materialization. |
| P319_MIN_JOIN_ROWS | 28350310 | Preserve Phase318 audited joined-row count unless Phase317 is rerun. |
| P319_EVENT_SYMBOL_SCOPE | 10_events_x_32_symbols | Feature matrix should produce one compact row per event and symbol. |
| P319_WINDOW | relative_second=-900..1800 | Use only the audited event-relative window. |
| P319_FULL_DEPTH_REQUIRED | depth_levels_1_to_5 | Retain full Zerodha top-five market-by-price depth. |
| P319_DEPTH_BEYOND_L1_REQUIRED | depth_levels_2_to_5_material | Feature matrix must include material depth-beyond-L1 features. |
| P319_NO_L1_ONLY_VARIANTS | l1_only_variant_rows=0 | No downstream strategy family may use only top-of-book fields. |
| P319_TARGET_SEPARATION | target_columns_not_live_signal_features | Post-event returns and pressure shifts must be targets/diagnostics, not live signal inputs. |
| P319_NO_NET_EDGE_LIVE_MASK | net_edge_live_mask_rows=0 | No future outcome mask may be used to select live rows. |
| P319_NO_STRATEGY_SEARCH | strategy_search_allowed_now=0 | Precommit only; no P&L, replay or optimization. |
| P319_BOUNDARIES | replay=0;promotion=0;paper=0;claim=0 | No acceptance boundary changes. |
| P319_NEXT | run_phase320_event_catalyst_multievent_feature_materialization_no_strategy_search | Materialize compact multi-event feature matrix next. |

## Processing work order

| work_order_id | scope | description |
| --- | --- | --- |
| load_joined_parquet | DuckDB scan over outputs/phase317/phase317_joined_multievent_top5_depth.parquet | Avoid loading all 28.35M rows into pandas at once. |
| derive_tick_features | SQL expressions for spread, mid, microprice, depth imbalances, depth slopes and pressures | Use depth levels 1-5 and depth levels 2-5. |
| aggregate_signal_features | group by event_id,event_time_ist,event_type,symbol | Produce compact event-symbol feature rows. |
| separate_targets | post_60s/post_300s/post_900s/post_1800s response columns | Keep target columns explicitly outside live feature set. |
| write_outputs | outputs/phase320/phase320_event_catalyst_multievent_feature_matrix.csv | Feature materialization target. |
| quality_audit | outputs/phase320/phase320_feature_quality.csv | Validate full-depth features, target separation and 10x32 coverage. |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P319_PHASE318_COMPLETE | True | 1 | 1 | hard |
| P319_PHASE318_JOIN_BREADTH_OK | True | events=10;symbols=32 | >=10_events_x_32_symbols | hard |
| P319_PHASE318_DEPTH_OK | True | 28350310 | all_joined_rows | hard |
| P319_FEATURE_CATALOG_NONEMPTY | True | 22 | >0 | hard |
| P319_DEPTH_BEYOND_L1_FEATURES_PRESENT | True | 13 | >=8 | hard |
| P319_TARGET_COLUMNS_SEPARATED | True | 5 | >=5 | hard |
| P319_CONTRACT_ROWS_PRESENT | True | 13 | >=13 | hard |
| P319_WORK_ORDER_ROWS_PRESENT | True | 6 | >=6 | hard |
| P319_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P319_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

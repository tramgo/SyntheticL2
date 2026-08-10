# Phase309 Event-Catalyst Feature Precommit

Phase309 precommits full-depth event-catalyst feature construction before any strategy search.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase309_event_feature_precommit_complete | 1 | Phase309 event-catalyst feature precommit completed |
| phase309_feature_catalog_rows | 18 | Feature catalog rows |
| phase309_depth_beyond_l1_feature_rows | 9 | Features using depth levels 2-5 |
| phase309_materialization_contract_rows | 8 | Materialization contract rows |
| phase309_full_depth_required | 1 | Top-five market-by-price depth required |
| phase309_l1_only_candidate_allowed | 0 | L1-only candidate path closed |
| phase309_strategy_search_allowed_now | 0 | No strategy search in Phase309 |
| phase309_strategy_replay_allowed | 0 | No replay |
| phase309_strategy_promotion_allowed | 0 | No promotion |
| phase309_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase309_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase309_hard_gate_pass_rows | 7 | Passed hard gates |
| phase309_hard_gate_rows | 7 | Hard gates |
| phase309_next_best_action | run_phase310_event_catalyst_feature_materialization_no_strategy_search | Recommended next action |

## Feature catalog

| feature_id | formula | feature_family | description | phase310_materialization_required | uses_depth_beyond_l1 |
| --- | --- | --- | --- | --- | --- |
| event_clock | relative_second | event_time_alignment | Event-relative second from -900 to +1800. | 1 | 0 |
| l1_spread | sell_1_price - buy_1_price | top_of_book | Quoted spread at best bid/ask. | 1 | 0 |
| l1_mid | (sell_1_price + buy_1_price) / 2 | top_of_book | Best bid/ask midpoint. | 1 | 0 |
| l1_microprice | weighted best quote by opposite-side quantity | top_of_book | Microprice using L1 bid/ask prices and quantities. | 1 | 0 |
| l1_queue_imbalance | (buy_1_quantity - sell_1_quantity) / total_l1_qty | top_of_book | Best-level queue imbalance. | 1 | 0 |
| l1_l5_qty_imbalance | sum_buy_qty_l1_l5 vs sum_sell_qty_l1_l5 | full_depth | Aggregate quantity imbalance across levels 1-5. | 1 | 1 |
| l2_l5_qty_imbalance | sum_buy_qty_l2_l5 vs sum_sell_qty_l2_l5 | depth_beyond_l1 | Depth-beyond-L1 quantity imbalance. | 1 | 1 |
| l1_l5_order_imbalance | sum_buy_orders_l1_l5 vs sum_sell_orders_l1_l5 | full_depth | Aggregate order-count imbalance across levels 1-5. | 1 | 1 |
| l2_l5_order_imbalance | sum_buy_orders_l2_l5 vs sum_sell_orders_l2_l5 | depth_beyond_l1 | Depth-beyond-L1 order-count imbalance. | 1 | 1 |
| bid_depth_slope_l1_l5 | buy_1_price - buy_5_price | full_depth | Bid-side depth price slope across levels 1-5. | 1 | 1 |
| ask_depth_slope_l1_l5 | sell_5_price - sell_1_price | full_depth | Ask-side depth price slope across levels 1-5. | 1 | 1 |
| depth_pressure | l1_l5_qty_imbalance / spread | full_depth | Liquidity pressure normalized by spread. | 1 | 1 |
| l2_l5_pressure | l2_l5_qty_imbalance / spread | depth_beyond_l1 | Beyond-L1 pressure normalized by spread. | 1 | 1 |
| event_pre_mean_mid | mean mid where relative_second < 0 | event_context | Pre-event reference midpoint. | 1 | 0 |
| event_post_return_60s | mid at +60s vs event mid | event_response | Short post-event midpoint response. | 1 | 0 |
| event_post_return_300s | mid at +300s vs event mid | event_response | Five-minute post-event midpoint response. | 1 | 0 |
| event_post_return_900s | mid at +900s vs event mid | event_response | Fifteen-minute post-event midpoint response. | 1 | 0 |
| event_post_depth_pressure_shift | post pressure minus pre pressure | full_depth_response | Full-depth pressure change around event. | 1 | 1 |

## Materialization contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P309_INPUT | outputs/phase307/phase307_joined_event_top5_depth.parquet | Use Phase307 joined event/depth artifact. |
| P309_QUALITY_GATE | phase308_hard_issue_rows == 0 | Only materialize if Phase308 quality audit passes. |
| P309_DEPTH_REQUIREMENT | levels_1_to_5_required | Feature set must preserve top-five market-by-price depth. |
| P309_L2_L5_MATERIALITY | depth_beyond_l1_required | At least one material feature family must use levels 2-5. |
| P309_NO_L1_ONLY_SEARCH | l1_only_candidate_allowed=0 | Do not open L1-only strategies from this branch. |
| P309_EVENT_BOUNDARY | event rows are catalysts only | No directional labels from event source. |
| P309_NO_STRATEGY_SEARCH | strategy_search_allowed_now=0 | Precommit only; no P&L or optimization. |
| P309_NEXT | run_phase310_event_catalyst_feature_materialization_no_strategy_search | Materialize features before searching strategies. |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P309_PHASE308_COMPLETE | True | 1 | 1 | hard |
| P309_PHASE308_NO_HARD_ISSUES | True | 0 | 0 | hard |
| P309_FEATURE_CATALOG_NONEMPTY | True | 18 | >0 | hard |
| P309_DEPTH_BEYOND_L1_FEATURES_PRESENT | True | 9 | >0 | hard |
| P309_CONTRACT_ROWS_PRESENT | True | 8 | >=8 | hard |
| P309_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P309_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

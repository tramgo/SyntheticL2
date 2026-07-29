# Phase252 Close or Broaden After Pair/Basket No-survivor Search

Generated UTC: 2026-07-29T10:11:29.735362+00:00

Phase252 closes the aggregate-feature pair/basket relative-value branch and opens a richer raw top-five depth materialization route.
It does not download new data, run a replay, promote a strategy, open paper/live acceptance or claim profitability.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase252_close_or_broaden_complete | 1 | Phase252 close/broaden decision completed |
| phase252_closed_scope | aggregate_pair_basket_relative_value_on_phase235_event_bars | Scope closed under current evidence |
| phase252_phase251_variant_rows | 3840 | Phase251 variants considered |
| phase252_phase251_base_positive_rows | 0 | Phase251 base-cost positive variants |
| phase252_phase251_cost200_positive_rows | 0 | Phase251 2x-cost positive variants |
| phase252_phase251_survivor_rows | 0 | Phase251 controlled survivors |
| phase252_raw_root_rows | 3 | Raw roots inspected |
| phase252_raw_depth_schema_present_rows | 30 | Raw depth schema fields present |
| phase252_raw_depth_schema_rows | 30 | Raw depth schema fields required |
| phase252_closure_rows | 3 | Closure ledger rows |
| phase252_failure_attribution_rows | 4 | Failure attribution rows |
| phase252_broaden_queue_rows | 3 | Materially different broaden routes |
| phase252_selected_next_route | P252_RICHER_RAW_TOP5_DEPTH_EVENT_BARS | Highest-priority next route |
| phase252_threshold_relaxation_only_allowed | 0 | No threshold relaxation loop |
| phase252_download_more_dates_now_allowed | 0 | No raw-date download in Phase252 |
| phase252_replay_execution_allowed_now | 0 | No replay execution in Phase252 |
| phase252_strategy_promotion_allowed | 0 | No strategy promotion from Phase252 |
| phase252_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase252 |
| phase252_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase252 |
| phase252_hard_gate_pass_rows | 7 | Hard gates passed |
| phase252_hard_gate_rows | 7 | Hard gates evaluated |
| phase252_next_best_action | run_phase253_richer_raw_top5_depth_feature_materialization_precommit_no_new_downloads_no_paper_live | Recommended next milestone |

## Raw Depth Inventory

| raw_root | exists | trade_date_dir_rows | sample_parquet_rows | sampled_path |
| --- | --- | --- | --- | --- |
| real_data_sample\l2_multiday_panel | 1 | 7 | 10 | real_data_sample\l2_multiday_panel\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\part-073443_831343-000001.parquet |
| real_data_sample\l2_unseen_validation | 1 | 2 | 10 | real_data_sample\l2_multiday_panel\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\part-073443_831343-000001.parquet |
| real_data_sample\l2_single_day | 1 | 0 | 5 | real_data_sample\l2_multiday_panel\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\part-073443_831343-000001.parquet |

## Raw Depth Schema Contract

| column | required_for_richer_raw_depth | present_in_sample_schema |
| --- | --- | --- |
| buy_1_price | 1 | 1 |
| buy_1_quantity | 1 | 1 |
| buy_1_orders | 1 | 1 |
| buy_2_price | 1 | 1 |
| buy_2_quantity | 1 | 1 |
| buy_2_orders | 1 | 1 |
| buy_3_price | 1 | 1 |
| buy_3_quantity | 1 | 1 |
| buy_3_orders | 1 | 1 |
| buy_4_price | 1 | 1 |
| buy_4_quantity | 1 | 1 |
| buy_4_orders | 1 | 1 |
| buy_5_price | 1 | 1 |
| buy_5_quantity | 1 | 1 |
| buy_5_orders | 1 | 1 |
| sell_1_price | 1 | 1 |
| sell_1_quantity | 1 | 1 |
| sell_1_orders | 1 | 1 |
| sell_2_price | 1 | 1 |
| sell_2_quantity | 1 | 1 |
| sell_2_orders | 1 | 1 |
| sell_3_price | 1 | 1 |
| sell_3_quantity | 1 | 1 |
| sell_3_orders | 1 | 1 |
| sell_4_price | 1 | 1 |
| sell_4_quantity | 1 | 1 |
| sell_4_orders | 1 | 1 |
| sell_5_price | 1 | 1 |
| sell_5_quantity | 1 | 1 |
| sell_5_orders | 1 | 1 |

## Closure Ledger

| decision_id | scope | decision | observed_value | required_value | rationale | reuse_allowed_without_material_redesign |
| --- | --- | --- | --- | --- | --- | --- |
| P252_CLOSE_AGGREGATE_PAIR_BASKET_RELATIVE_VALUE | phase251_pair_basket_relative_value_on_phase235_aggregate_event_bars | closed_for_current_evidence_set | 0 | >0 controlled survivors | Phase251 found no controlled survivor across market-neutral pair/basket variants. | 0 |
| P252_BLOCK_THRESHOLD_RELAXATION_LOOP | phase251_variant_thresholds | blocked | 0 | >0 positive at 2x modeled costs | Relaxing thresholds after zero base-cost and zero 2x-cost positives would not address cost-floor dominance. | 0 |
| P252_KEEP_NEW_DOWNLOADS_CLOSED | fresh_real_l2_dates | blocked_until_material_new_richer_depth_candidate | 0 | future_holdout_precommit_allowed=1 | No Phase251 survivor qualifies for fresh holdout data spend. | 0 |

## Failure Attribution

| failure_mode | observed_metric | observed_value | interpretation |
| --- | --- | --- | --- |
| aggregate_pair_basket_cost_floor_dominance | phase251_net_positive_variant_rows | 0 | No tested pair/basket variant was positive even at base modeled costs. |
| no_2x_cost_positive_variants | phase251_cost200_positive_variant_rows | 0 | The branch produced no cost-stress candidates for controls. |
| aggregate_depth_feature_limit | phase251_full_top_five_depth_variant_rows | 3840 | Phase251 used top-five aggregate and depth-beyond-L1 features, but not explicit per-level book-shape features from raw parquet. |
| best_failed_candidate_cost_drag | phase251_best_training_net_pnl_inr | -1681.1779513204742 | The best failed candidate had positive gross P&L but modeled cost drag exceeded the edge. |

## Material Broaden Queue

| priority | route_id | route | why_materially_different | allowed_sources | precommit_next | replay_allowed_now |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | P252_RICHER_RAW_TOP5_DEPTH_EVENT_BARS | rebuild_event_bars_from_raw_top5_depth_levels | Moves from aggregate Phase235 depth features to explicit per-level buy/sell price, quantity and order-count shape features from raw parquet. | existing downloaded raw parquet under real_data_sample; no new raw-date downloads | phase253_richer_raw_top5_depth_feature_materialization_precommit | 0 |
| 2 | P252_DEPTH_EVENT_SEQUENCE_MODEL | top5_depth_event_sequence_prediction | Uses changes in per-level book shape, queue count and replenishment/withdrawal sequences rather than static aggregate imbalance. | raw top-five market-by-price tick stream and receive-order deltas | phase253_depth_event_sequence_precommit | 0 |
| 3 | P252_LOW_TURNOVER_OPENING_DEPTH_SHOCK | opening_depth_shock_low_turnover_only | Separates opening price-discovery/depth depletion from normal intraday microstructure and requires lower turnover. | existing raw open-window L2 parquet plus cost model | phase253_opening_depth_shock_precommit | 0 |

## Guardrail Ledger

| guardrail_id | requirement | active |
| --- | --- | --- |
| P252_NO_PROFITABILITY_CLAIM | No deployable profitability claim because Phase251 found zero positive variants and zero survivors. | 1 |
| P252_NO_MORE_DATE_DOWNLOAD | No fresh real L2 date downloads until a richer raw-depth candidate is frozen. | 1 |
| P252_NO_THRESHOLD_RELAXATION_ONLY | Do not continue by relaxing Phase251 thresholds; next route must change the feature source. | 1 |
| P252_RAW_DEPTH_REQUIRED_NEXT | The next primary route must use explicit raw buy/sell levels 1-5 price, quantity and order-count fields. | 1 |
| P252_COSTS_AND_CONTROLS_REMAIN | Zerodha modeled costs, spread/slippage, 2x-cost stress, side-flip and random-side controls remain mandatory. | 1 |
| P252_NO_PAPER_LIVE | Paper/live acceptance remains closed. | 1 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P252_PHASE251_WORK_ORDER_PRESENT | True | close_or_broaden_phase251_pair_basket_relative_value_search_no_downloads_no_paper_live | Phase251 next action asks close/broaden | hard |
| P252_CLOSURE_LEDGER_WRITTEN | True | 3 | >=3 closure rows | hard |
| P252_FAILURE_ATTRIBUTION_WRITTEN | True | 4 | >=4 failure rows | hard |
| P252_MATERIAL_BROADEN_QUEUE_WRITTEN | True | 3 | >=3 materially different routes | hard |
| P252_RAW_DEPTH_SCHEMA_AVAILABLE | True | 30/30 | all raw buy/sell levels 1-5 fields present in sample schema | hard |
| P252_GUARDRAILS_ACTIVE | True | all active | all guardrails active | hard |
| P252_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

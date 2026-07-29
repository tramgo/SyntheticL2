# Phase258 Passive Queue-aware Spread-capture Precommit

Generated UTC: 2026-07-29T11:09:26.807781+00:00

Phase258 precommits the next materially different route after Phase257 closed the full-depth taker-threshold search.
It specifies a passive queue-aware spread-capture proxy using the same Zerodha top-five market-by-price depth surface.
It is not a replay, promotion, paper/live acceptance or deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase258_passive_queue_precommit_complete | 1 | Phase258 passive queue-aware spread-capture precommit completed |
| phase258_selected_route | P258_PASSIVE_QUEUE_AWARE_SPREAD_CAPTURE | Selected route |
| phase258_input_event_bar_rows | 1636 | Input richer event bars |
| phase258_input_symbols | 32 | Input symbol breadth |
| phase258_input_trade_dates | 1 | Input trade dates |
| phase258_mean_spread_bps | 2.8444 | Mean spread bps in input |
| phase258_mean_l2_l5_bid_share | 0.853238 | Mean bid depth share from levels 2-5 |
| phase258_mean_l2_l5_ask_share | 0.829775 | Mean ask depth share from levels 2-5 |
| phase258_order_model_contract_rows | 8 | Order model contract rows |
| phase258_feature_contract_rows | 15 | Feature contract rows |
| phase258_candidate_family_rows | 5 | Candidate family rows |
| phase258_control_contract_rows | 7 | Control contract rows |
| phase258_full_top_five_depth_required | 1 | Levels 1-5 required |
| phase258_l1_only_candidate_allowed | 0 | L1-only candidate forbidden |
| phase258_hard_gate_pass_rows | 8 | Hard gates passed |
| phase258_hard_gate_rows | 8 | Hard gates evaluated |
| phase258_download_more_dates_now_allowed | 0 | No new download in Phase258 |
| phase258_replay_execution_allowed_now | 0 | No replay execution in Phase258 |
| phase258_strategy_promotion_allowed | 0 | No strategy promotion from Phase258 |
| phase258_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase258 |
| phase258_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase258 |
| phase258_next_best_action | run_phase259_passive_queue_aware_spread_capture_training_search_full_top5_depth_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P258_PHASE257_WORK_ORDER_PRESENT | True | run_phase258_passive_queue_aware_spread_capture_precommit_full_top5_depth_no_paper_live | Phase257 next action targets Phase258 | hard |
| P258_INPUT_PRESENT | True | 1 | Phase254 richer event bars exist | hard |
| P258_EVENT_BAR_BREADTH | True | rows=1636.0;symbols=32.0 | >=1000 rows and >=20 symbols | hard |
| P258_FULL_DEPTH_FEATURE_CONTRACT | True | 9 | >=6 required full-depth features | hard |
| P258_NO_L1_ONLY_CANDIDATES | True | l1_only_depth_imbalance forbidden | L1-only candidate explicitly forbidden | hard |
| P258_PASSIVE_FAMILY_CATALOG_WRITTEN | True | 5 | >=4 passive/queue-aware families | hard |
| P258_CONTROL_CONTRACT_WRITTEN | True | 6 | >=5 required controls | hard |
| P258_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

## Order Model Contract

| model_component | contract_value | description |
| --- | --- | --- |
| quote_side | bid_or_ask_or_both | Passive quotes may be placed on bid, ask or both sides according to depth signal |
| quote_price | best_bid_or_best_ask_proxy | Use level-1 same-side price as passive quote proxy; no crossing of spread |
| queue_position_proxy | same_side_l1_quantity_and_order_count | Approximate ahead quantity and queue crowding from L1 quantity/order count |
| fill_probability_proxy | opposite_trade_pressure_minus_same_side_queue | Fill likelihood rises with opposite pressure and falls with queue depth/order crowding |
| adverse_selection_proxy | future_mid_move_against_quote | Penalize fills followed by unfavorable mid-price movement |
| cancel_replace_proxy | top5_churn_and_l1_price_shift | Higher churn or L1 price shifts increase cancel/replace/adverse fill risk |
| latency_proxy | next_event_bar_arrival | Assume quote becomes active after at least one event-bar latency step |
| cost_stack | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Apply statutory/brokerage cost stack; passive model may avoid taker spread crossing but not charges |

## Feature Contract

| feature_status | feature | description |
| --- | --- | --- |
| required | avg_spread_bps | Spread capture ceiling and liquidity filter |
| required | avg_cum_buy_qty_l1_l5 | Full bid-side visible depth |
| required | avg_cum_sell_qty_l1_l5 | Full ask-side visible depth |
| required | avg_cum_buy_qty_l2_l5 | Beyond-L1 bid depth; prevents L1-only candidate |
| required | avg_cum_sell_qty_l2_l5 | Beyond-L1 ask depth; prevents L1-only candidate |
| required | avg_cum_top5_qty_imbalance | Full top-five imbalance |
| required | avg_depth_beyond_l1_qty_imbalance | Levels 2-5 imbalance |
| required | avg_order_count_imbalance_l1_l5 | Order-count crowding imbalance |
| required | top5_qty_churn_sum | Depth churn / queue instability |
| required | top5_order_churn_sum | Order-count churn / cancel pressure |
| required | depth_replenishment_pressure | Passive support and replenishment |
| required | depth_withdrawal_pressure | Withdrawal/adverse-selection risk |
| required | l1_price_shift_abs_sum | Cancel/replace and queue-loss proxy |
| required | taker_round_trip_cost_floor_bps | Cost reference and stress floor |
| forbidden | l1_only_depth_imbalance | No L1-only candidate family is allowed |

## Candidate Family Catalog

| candidate_family_id | quote_side | description | required_signal_groups |
| --- | --- | --- | --- |
| P258_PASSIVE_BID_REPLENISHMENT | bid | Quote bid when levels 2-5 bid depth replenishes and adverse ask pressure is low | full_top5_depth;queue_proxy;adverse_selection |
| P258_PASSIVE_ASK_REPLENISHMENT | ask | Quote ask when levels 2-5 ask depth replenishes and adverse bid pressure is low | full_top5_depth;queue_proxy;adverse_selection |
| P258_TWO_SIDED_HIGH_SPREAD_LOW_CHURN | both | Quote both sides only when spread is wide enough and top-five churn is low | spread_capture;low_churn;queue_proxy |
| P258_IMBALANCE_SKEWED_MAKER | bid_or_ask | Skew passive side with top-five and levels 2-5 imbalance agreement | top5_imbalance;beyond_l1_imbalance;order_count |
| P258_QUEUE_AVOIDANCE_FILTER | filter | Block passive quote when L1 queue crowding, withdrawal or price-shift risk is high | queue_adversity;withdrawal;price_shift |

## Control Contract

| control_id | control_status | description |
| --- | --- | --- |
| random_side_control | required | Passive quote direction must beat deterministic random side |
| side_flip_control | required | Signal side flip should degrade or invert expected edge |
| cost_stress | required | Evaluate at base, 1.5x and 2x statutory/brokerage charges |
| queue_adversity_stress | required | Haircut fills or edge when queue crowding/churn is high |
| nonfill_model | required | Unfilled quote opportunities must not receive spread capture |
| forbidden_dates | required | Keep 2026-07-17 and 2026-07-20 excluded from parameter selection |
| paper_live_claim | forbidden | No paper/live acceptance or deployable profitability claim |

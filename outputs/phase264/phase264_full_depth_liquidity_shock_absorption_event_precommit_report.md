# Phase264 Full-depth Liquidity-shock Absorption Event Precommit

Generated UTC: 2026-08-02T02:05:05.739889+00:00

Phase264 precommits the next materially different route after Phase263 closed the repaired passive spread-capture/fill-model path.
The route remains full-depth: Zerodha top-five market-by-price rows 1-5 and levels 2-5 features are mandatory, and L1-only variants are forbidden.
This is not replay execution, strategy promotion, paper/live acceptance or a deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase264_liquidity_shock_precommit_complete | 1 | Phase264 full-depth liquidity-shock/absorption event precommit completed |
| phase264_selected_route | P264_FULL_DEPTH_LIQUIDITY_SHOCK_ABSORPTION_EVENT_MODEL | Selected route |
| phase264_input_event_bar_rows | 1636 | Input event bars |
| phase264_input_symbols | 32 | Input symbols |
| phase264_input_trade_dates | 1 | Input trade dates |
| phase264_mean_l2_l5_bid_share | 0.853238 | Mean bid depth share from levels 2-5 |
| phase264_mean_l2_l5_ask_share | 0.829775 | Mean ask depth share from levels 2-5 |
| phase264_mean_abs_l2_l5_imbalance | 0.228722 | Mean absolute L2-L5 imbalance |
| phase264_feature_catalog_rows | 16 | Feature catalog rows |
| phase264_event_family_rows | 5 | Event family rows |
| phase264_label_contract_rows | 5 | Label contract rows |
| phase264_search_grid_contract_rows | 6 | Search grid contract rows |
| phase264_control_contract_rows | 8 | Control contract rows |
| phase264_full_top_five_depth_required | 1 | Zerodha top-five rows 1-5 required |
| phase264_levels_2_to_5_materiality_required | 1 | Levels 2-5 features required |
| phase264_l1_only_candidate_allowed | 0 | L1-only candidates forbidden |
| phase264_threshold_relaxation_only_allowed | 0 | Threshold relaxation only forbidden |
| phase264_hard_gate_pass_rows | 11 | Hard gates passed |
| phase264_hard_gate_rows | 11 | Hard gates evaluated |
| phase264_download_more_dates_now_allowed | 0 | No new download in Phase264 |
| phase264_replay_execution_allowed_now | 0 | No replay execution in Phase264 |
| phase264_strategy_promotion_allowed | 0 | No strategy promotion from Phase264 |
| phase264_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase264 |
| phase264_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase264 |
| phase264_next_best_action | run_phase265_full_depth_liquidity_shock_absorption_event_training_search_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P264_PHASE263_WORK_ORDER_PRESENT | True | run_phase264_full_depth_liquidity_shock_absorption_event_precommit_no_paper_live | Phase263 next action targets Phase264 | hard |
| P264_PHASE263_DEPTH_CONTRACT_PRESENT | True | 1 | Phase263 route requires levels 1-5 and L2-L5 | hard |
| P264_PHASE263_ROUTE_CONTRACT_PRESENT | True | 1 | Phase263 route is liquidity-shock/absorption | hard |
| P264_INPUT_PRESENT | True | 1 | Phase254 richer raw top-five event bars exist | hard |
| P264_INPUT_BREADTH | True | rows=1636.0;symbols=32.0 | >=1000 rows and >=20 symbols | hard |
| P264_FEATURE_CATALOG_WRITTEN | True | 16 | >=15 feature rows plus L1-only forbidden row | hard |
| P264_FULL_DEPTH_EVENT_FAMILIES_WRITTEN | True | 5 | >=5 event families with L2-L5/top-five features | hard |
| P264_LABEL_CONTRACT_WRITTEN | True | 5 | required labels and no-leakage contract | hard |
| P264_SEARCH_GRID_WRITTEN | True | 6 | >=6 search-grid rows | hard |
| P264_CONTROLS_WRITTEN | True | 8 | required controls and forbidden continuations | hard |
| P264_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

## Feature Catalog

| feature_group | feature | description |
| --- | --- | --- |
| depth_stock | avg_cum_buy_qty_l1_l5 | Full visible bid-side quantity across Zerodha top-five rows 1-5 |
| depth_stock | avg_cum_sell_qty_l1_l5 | Full visible ask-side quantity across Zerodha top-five rows 1-5 |
| depth_stock | avg_cum_buy_qty_l2_l5 | Bid depth beyond L1; required levels 2-5 materiality |
| depth_stock | avg_cum_sell_qty_l2_l5 | Ask depth beyond L1; required levels 2-5 materiality |
| imbalance | avg_cum_top5_qty_imbalance | Top-five quantity imbalance |
| imbalance | avg_depth_beyond_l1_qty_imbalance | Levels 2-5 quantity imbalance |
| imbalance | avg_level_weighted_depth_imbalance | Near-level weighted depth imbalance |
| imbalance | avg_order_count_imbalance_l1_l5 | Top-five order-count imbalance |
| shock | depth_replenishment_pressure | Visible-depth replenishment event pressure |
| shock | depth_withdrawal_pressure | Visible-depth withdrawal event pressure |
| shock | top5_qty_churn_sum | Top-five quantity churn / instability |
| shock | top5_order_churn_sum | Top-five order-count churn / cancel pressure |
| shock | l1_price_shift_abs_sum | L1 price movement / spread-book instability proxy |
| liquidity | avg_spread_bps | Spread compression/expansion context and cost hurdle context |
| cost | taker_round_trip_cost_floor_bps | Zerodha cost floor for directional event hurdle |
| forbidden | l1_only_depth_imbalance | No L1-only feature set or candidate family is allowed |

## Event Family Catalog

| event_family_id | direction_space | description | required_full_depth_features |
| --- | --- | --- | --- |
| P265_L2L5_BID_ABSORPTION_CONTINUATION | long | bid-side levels 2-5 replenish while top-five imbalance and level-weighted imbalance support bids after a liquidity shock | avg_cum_buy_qty_l2_l5;avg_depth_beyond_l1_qty_imbalance;avg_level_weighted_depth_imbalance;depth_replenishment_pressure;top5_qty_churn_sum |
| P265_L2L5_ASK_ABSORPTION_CONTINUATION | short | ask-side levels 2-5 replenish while top-five imbalance and level-weighted imbalance support asks after a liquidity shock | avg_cum_sell_qty_l2_l5;avg_depth_beyond_l1_qty_imbalance;avg_level_weighted_depth_imbalance;depth_replenishment_pressure;top5_qty_churn_sum |
| P265_WITHDRAWAL_REVERSAL_AFTER_SHOCK | long_or_short | detect aggressive withdrawal/churn events and trade reversal only when opposite-side levels 2-5 absorption appears | depth_withdrawal_pressure;top5_qty_churn_sum;top5_order_churn_sum;avg_cum_buy_qty_l2_l5;avg_cum_sell_qty_l2_l5 |
| P265_SPREAD_COMPRESSION_ABSORPTION | long_or_short | require spread compression after high churn plus agreement between top-five and levels 2-5 imbalance | avg_spread_bps;l1_price_shift_abs_sum;avg_cum_top5_qty_imbalance;avg_depth_beyond_l1_qty_imbalance |
| P265_DEPTH_CHURN_EXHAUSTION_FILTER | filter | filter or downweight events with excessive churn/order-cancel pressure without replenishment confirmation | top5_qty_churn_sum;top5_order_churn_sum;depth_replenishment_pressure;depth_withdrawal_pressure |

## Label Contract

| label_id | label_status | description |
| --- | --- | --- |
| future_mid_return_h3 | required | 3-event-bar future mid return label |
| future_mid_return_h6 | required | 6-event-bar future mid return label |
| future_mid_return_h10 | required | 10-event-bar future mid return label |
| cost_hurdled_return | required | Directional label must exceed Zerodha cost floor at 1x, 1.5x and 2x stress before candidate survival |
| no_future_feature_leakage | required | Future labels may not be used as features or filters |

## Search Grid Contract

| grid_component | contract_value | description |
| --- | --- | --- |
| horizons | 3;6;10 | Evaluate the same event horizons available in Phase254 |
| imbalance_quantiles | 0.60;0.75;0.90 | Threshold top-five and levels 2-5 imbalance strength |
| shock_quantiles | 0.60;0.75;0.90 | Threshold replenishment, withdrawal and churn event intensity |
| spread_regimes | low;mid;high;compression | Separate spread/compression context from directional depth shock |
| cost_multipliers | 1.0;1.5;2.0 | Stress Zerodha statutory/brokerage charges |
| breadth_floors | opportunities>=30;symbols>=8;dates>=1 | Minimum breadth before any survivor discussion on current available data |

## Control Contract

| control_id | control_status | description |
| --- | --- | --- |
| random_side_control | required | Candidate must beat deterministic random side under the same event mask |
| side_flip_control | required | Flipping the liquidity-shock direction should degrade or invert edge |
| cost_stress | required | Evaluate base, 1.5x and 2x Zerodha cost floors |
| shuffle_label_control | required | Candidate must beat shuffled future-return labels |
| event_breadth_control | required | Candidate must clear minimum event, symbol and date breadth floors |
| no_l1_only_control | required | Every event family must use top-five and levels 2-5 features |
| threshold_relaxation_only | forbidden | Do not continue the failed passive route by merely relaxing thresholds |
| paper_live_or_deployable_profitability_claim | forbidden | Phase264/265 cannot claim paper/live/deployable profitability |

# Phase261 Passive Opportunity Breadth and Fill-model Repair Precommit

Generated UTC: 2026-07-29T11:31:00.728816+00:00

Phase261 converts the Phase260 route decision into an executable Phase262 search contract.
The repair is deliberately full-depth: Zerodha top-five market-by-price rows 1-5 remain required, and L1-only variants are forbidden.
It separates opportunity discovery from fill-probability scoring so the next search can test broader passive opportunities without pretending every quote fills.
This is not a replay, not a strategy promotion, not paper/live acceptance and not a deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase261_passive_repair_precommit_complete | 1 | Phase261 passive opportunity breadth and fill-model repair precommit completed |
| phase261_selected_route | P261_PASSIVE_OPPORTUNITY_BREADTH_AND_FILL_MODEL_REPAIR | Selected route |
| phase261_input_event_bar_rows | 1636 | Input richer raw top-five event bars |
| phase261_input_symbols | 32 | Input symbol breadth |
| phase261_input_trade_dates | 1 | Input trade dates |
| phase261_mean_spread_bps | 2.8444 | Mean spread bps in input |
| phase261_median_spread_bps | 2.67259 | Median spread bps in input |
| phase261_mean_l2_l5_bid_share | 0.853238 | Mean bid depth share from levels 2-5 |
| phase261_mean_l2_l5_ask_share | 0.829775 | Mean ask depth share from levels 2-5 |
| phase261_repair_contract_rows | 5 | Repair contract rows |
| phase261_fill_probability_grid_rows | 12 | Fill probability grid rows |
| phase261_candidate_family_rows | 5 | Broadened candidate family rows |
| phase261_control_contract_rows | 9 | Control contract rows |
| phase261_full_top_five_depth_required | 1 | Zerodha top-five rows 1-5 required |
| phase261_levels_2_to_5_materiality_required | 1 | Beyond-L1 depth required |
| phase261_l1_only_candidate_allowed | 0 | L1-only candidate forbidden |
| phase261_download_more_dates_now_allowed | 0 | No new download in Phase261 |
| phase261_replay_execution_allowed_now | 0 | No replay execution in Phase261 |
| phase261_strategy_promotion_allowed | 0 | No strategy promotion from Phase261 |
| phase261_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase261 |
| phase261_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase261 |
| phase261_hard_gate_pass_rows | 10 | Hard gates passed |
| phase261_hard_gate_rows | 10 | Hard gates evaluated |
| phase261_next_best_action | run_phase262_passive_opportunity_breadth_fill_model_training_search_full_top5_depth_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P261_PHASE260_WORK_ORDER_PRESENT | True | run_phase261_passive_opportunity_breadth_fill_model_repair_precommit_full_top5_depth_no_paper_live | Phase260 next action targets Phase261 | hard |
| P261_PHASE260_DEPTH_CONTRACT_PRESENT | True | 1 | levels_1_to_5_required present in Phase260 route | hard |
| P261_INPUT_PRESENT | True | 1 | Phase254 richer raw top-five event bars exist | hard |
| P261_EVENT_BAR_BREADTH | True | rows=1636.0;symbols=32.0 | >=1000 rows and >=20 symbols | hard |
| P261_REPAIR_CONTRACT_WRITTEN | True | 5 | >=5 repair contract rows | hard |
| P261_FILL_GRID_WRITTEN | True | 12 | >=12 fill grid rows | hard |
| P261_FULL_DEPTH_FAMILY_CATALOG_WRITTEN | True | 5 | >=5 families using l1_l5, l2_l5 and top5 features | hard |
| P261_CONTROLS_WRITTEN | True | 7 | >=7 required controls | hard |
| P261_L1_ONLY_FORBIDDEN | True | l1_only_candidate_family forbidden | L1-only candidates explicitly forbidden | hard |
| P261_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

## Opportunity Repair Contract

| repair_id | repair_contract | description | why_it_matters |
| --- | --- | --- | --- |
| P261_REPAIR_OPPORTUNITY_FILTER | separate_opportunity_filter_from_fill_probability | Generate candidate passive quote opportunities from spread, replenishment and full-depth regime first; score fill probability afterward. | prevents_one_tick_or_one_symbol_overfiltering |
| P261_REPAIR_FILL_GRID | calibrated_fill_probability_grid | Search fill-probability assumptions over base fill rate, queue haircuts, churn haircuts, levels 2-5 support boosts and non-fill stress. | prevents_single_formula_overfit |
| P261_REPAIR_BREADTH | broaden_spread_replenishment_and_imbalance_thresholds | Include lower spread quantiles and softer replenishment/imbalance thresholds before queue-adversity penalties are applied. | increases_symbol_and_opportunity_breadth |
| P261_REPAIR_SIDE_SPACE | bid_ask_both_and_skewed_quote_sides | Keep bid-only, ask-only, two-sided and imbalance-skewed maker candidates so profitable direction is not assumed. | forces_side_controls |
| P261_REPAIR_DEPTH_CORE | levels_1_to_5_required_l2_l5_materiality_required | Require top-five quantities/order counts and levels 2-5 shares in every candidate; L1-only variants are invalid by contract. | protects_core_project_objective |

## Fill Probability Grid

| fill_model_id | profile | base_fill_probability | queue_haircut | churn_haircut | levels_2_to_5_support_boost | nonfill_stress_multiplier | queue_adversity_multiplier | adverse_selection_penalty_multiplier | max_fill_probability_cap | formula_contract |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P261_FILL_conservative_low_fill_QA0p75 | conservative_low_fill | 0.08 | 0.55 | 0.6 | 0.05 | 1.25 | 0.75 | 1.25 | 0.35 | fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture |
| P261_FILL_conservative_low_fill_QA1p0 | conservative_low_fill | 0.08 | 0.55 | 0.6 | 0.05 | 1.25 | 1 | 1.25 | 0.35 | fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture |
| P261_FILL_conservative_low_fill_QA1p25 | conservative_low_fill | 0.08 | 0.55 | 0.6 | 0.05 | 1.25 | 1.25 | 1.25 | 0.35 | fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture |
| P261_FILL_baseline_conservative_QA0p75 | baseline_conservative | 0.14 | 0.7 | 0.75 | 0.08 | 1 | 0.75 | 1 | 0.35 | fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture |
| P261_FILL_baseline_conservative_QA1p0 | baseline_conservative | 0.14 | 0.7 | 0.75 | 0.08 | 1 | 1 | 1 | 0.35 | fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture |
| P261_FILL_baseline_conservative_QA1p25 | baseline_conservative | 0.14 | 0.7 | 0.75 | 0.08 | 1 | 1.25 | 1 | 0.35 | fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture |
| P261_FILL_balanced_depth_supported_QA0p75 | balanced_depth_supported | 0.2 | 0.8 | 0.85 | 0.12 | 0.85 | 0.75 | 1 | 0.35 | fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture |
| P261_FILL_balanced_depth_supported_QA1p0 | balanced_depth_supported | 0.2 | 0.8 | 0.85 | 0.12 | 0.85 | 1 | 1 | 0.35 | fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture |
| P261_FILL_balanced_depth_supported_QA1p25 | balanced_depth_supported | 0.2 | 0.8 | 0.85 | 0.12 | 0.85 | 1.25 | 1 | 0.35 | fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture |
| P261_FILL_optimistic_but_capped_QA0p75 | optimistic_but_capped | 0.28 | 0.9 | 0.9 | 0.16 | 0.7 | 0.75 | 0.85 | 0.35 | fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture |
| P261_FILL_optimistic_but_capped_QA1p0 | optimistic_but_capped | 0.28 | 0.9 | 0.9 | 0.16 | 0.7 | 1 | 0.85 | 0.35 | fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture |
| P261_FILL_optimistic_but_capped_QA1p25 | optimistic_but_capped | 0.28 | 0.9 | 0.9 | 0.16 | 0.7 | 1.25 | 0.85 | 0.35 | fill_probability = capped(base_fill * queue_haircut * churn_haircut + levels_2_to_5_support_boost); unfilled quotes receive no spread capture |

## Broadened Candidate Family Catalog

| candidate_family_id | quote_side | threshold_grid_contract | required_full_depth_features |
| --- | --- | --- | --- |
| P262_BROAD_PASSIVE_BID_REPLENISHMENT | bid | spread_quantile in [0.25,0.50,0.75]; bid_replenishment_quantile in [0.40,0.60,0.75]; abs_beyond_l1_imbalance >= [0.00,0.03,0.06] | avg_cum_buy_qty_l1_l5;avg_cum_buy_qty_l2_l5;avg_depth_beyond_l1_qty_imbalance;depth_replenishment_pressure;top5_qty_churn_sum;top5_order_churn_sum |
| P262_BROAD_PASSIVE_ASK_REPLENISHMENT | ask | spread_quantile in [0.25,0.50,0.75]; ask_replenishment_quantile in [0.40,0.60,0.75]; abs_beyond_l1_imbalance >= [0.00,0.03,0.06] | avg_cum_sell_qty_l1_l5;avg_cum_sell_qty_l2_l5;avg_depth_beyond_l1_qty_imbalance;depth_replenishment_pressure;top5_qty_churn_sum;top5_order_churn_sum |
| P262_TWO_SIDED_SPREAD_CAPTURE_LOW_CHURN | both | spread_quantile in [0.50,0.75,0.90]; top5_churn_quantile <= [0.40,0.60,0.75]; price_shift_quantile <= [0.50,0.75] | avg_spread_bps;avg_cum_buy_qty_l1_l5;avg_cum_sell_qty_l1_l5;avg_cum_buy_qty_l2_l5;avg_cum_sell_qty_l2_l5;l1_price_shift_abs_sum |
| P262_IMBALANCE_SKEWED_MAKER_BROAD | bid_or_ask | top5 and levels-2-to-5 imbalance agree; imbalance threshold in [0.02,0.05,0.10]; spread_quantile >= [0.25,0.50] | avg_cum_top5_qty_imbalance;avg_depth_beyond_l1_qty_imbalance;avg_order_count_imbalance_l1_l5;avg_spread_bps |
| P262_QUEUE_REPAIR_AVOIDANCE_OVERLAY | filter | Block or haircut opportunities with high L1 queue crowding, top-five churn, withdrawal pressure or L1 price shifts. | avg_order_count_imbalance_l1_l5;top5_qty_churn_sum;top5_order_churn_sum;depth_withdrawal_pressure;l1_price_shift_abs_sum |

## Control Contract

| control_id | control_status | description |
| --- | --- | --- |
| random_side_control | required | Every candidate must beat deterministic random side under the same opportunity and fill model grid. |
| side_flip_control | required | Flipping bid/ask interpretation must degrade or invert edge, not improve it by accident. |
| cost_stress | required | Evaluate Zerodha statutory/brokerage charges at base, 1.5x and 2x. |
| queue_adversity_stress | required | Stress L1 queue crowding and top-five churn with fill haircut and adverse-selection penalty multipliers. |
| nonfill_stress | required | Unfilled passive quotes must earn zero spread capture and may still incur opportunity/latency risk in sensitivity checks. |
| opportunity_breadth_floor | required | Best candidate must exceed minimum opportunity, symbol and fill-equivalent breadth before any promotion discussion. |
| levels_1_to_5_depth_requirement | required | Use Zerodha top-five depth rows 1-5; levels 2-5 materiality is mandatory. |
| l1_only_candidate_family | forbidden | No L1-only strategy, feature, filter or candidate variant can survive. |
| paper_live_or_deployable_profitability_claim | forbidden | Phase261/262 cannot claim paper/live/deployable profitability. |

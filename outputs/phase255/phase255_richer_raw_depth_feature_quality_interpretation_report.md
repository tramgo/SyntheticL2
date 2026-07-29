# Phase255 Richer Raw Top-five Depth Feature-quality Interpretation

Generated UTC: 2026-07-29T10:51:37.154775+00:00

Phase255 audits the Phase254 compact event-bar product before any strategy search consumes it.
It checks feature health, levels 2-5 contribution inside Zerodha's top-five market-by-price book, and simple future-return label association.
It does not execute replay, promote a strategy, open paper/live acceptance or claim profitability.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase255_feature_quality_interpretation_complete | 1 | Phase255 richer raw-depth feature quality interpretation completed |
| phase255_input_event_bar_rows | 1636 | Phase254 richer raw-depth event bars audited |
| phase255_trade_dates | 1 | Trade dates represented |
| phase255_symbols | 32 | Symbols represented |
| phase255_source_tick_rows | 32426 | Source raw ticks represented by audited event bars |
| phase255_feature_rows | 18 | Features audited |
| phase255_full_depth_feature_rows | 11 | Audited features using levels 2-5/top-five depth shape |
| phase255_healthy_feature_rows | 18 | Healthy features by missingness/finite/variation gate |
| phase255_healthy_full_depth_feature_rows | 11 | Healthy full-depth features |
| phase255_max_abs_spearman_ic | 0.147539 | Maximum absolute Spearman IC across audited feature/label pairs |
| phase255_max_abs_full_depth_spearman_ic | 0.147539 | Maximum absolute Spearman IC for full-depth features |
| phase255_top_full_depth_feature | avg_order_count_imbalance_l1_l5 | Top full-depth feature by absolute Spearman IC |
| phase255_top_full_depth_label | future_return_h10 | Top full-depth horizon label by absolute Spearman IC |
| phase255_hard_gate_pass_rows | 9 | Hard gates passed |
| phase255_hard_gate_rows | 9 | Hard gates evaluated |
| phase255_strategy_search_allowed_next | 1 | Whether Phase256 training-only cost-aware strategy search is allowed next |
| phase255_replay_execution_allowed_now | 0 | No replay execution in Phase255 |
| phase255_strategy_promotion_allowed | 0 | No strategy promotion from Phase255 |
| phase255_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase255 |
| phase255_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase255 |
| phase255_next_best_action | run_phase256_richer_raw_top5_depth_cost_aware_strategy_search_training_only_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P255_PHASE254_WORK_ORDER_PRESENT | True | run_phase255_richer_raw_depth_feature_quality_interpretation_no_replay_no_paper_live | Phase254 next action targets Phase255 | hard |
| P255_INPUT_EVENT_BARS_PRESENT | True | 1636 | >=1000 richer raw-depth event bars | hard |
| P255_SYMBOL_BREADTH_RETAINED | True | 32 | >=20 symbols | hard |
| P255_HEALTHY_FEATURE_COUNT | True | 18 | >=12 healthy features | hard |
| P255_HEALTHY_FULL_DEPTH_FEATURE_COUNT | True | 11 | >=8 healthy full-depth features | hard |
| P255_LEVELS_2_5_DEPTH_SHARE_MATERIAL | True | bid=0.8836;ask=0.8618 | median levels 2-5 share >=25% on both sides | hard |
| P255_BEYOND_L1_IMBALANCE_NOT_DEGENERATE | True | std=0.288994;corr=0.938459 | levels 2-5 imbalance varies and is not identical to top-five imbalance | hard |
| P255_FULL_DEPTH_LABEL_ASSOCIATION_VISIBLE | True | 0.147539 | >=0.02 absolute Spearman IC for at least one full-depth feature/horizon | hard |
| P255_NO_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

## Full Depth Contribution Summary

| metric | value | description |
| --- | --- | --- |
| median_bid_depth_share_from_levels_2_5 | 0.883648 | Median share of visible bid quantity contributed by levels 2-5 |
| median_ask_depth_share_from_levels_2_5 | 0.861755 | Median share of visible ask quantity contributed by levels 2-5 |
| p10_bid_depth_share_from_levels_2_5 | 0.718995 | 10th percentile bid quantity share from levels 2-5 |
| p10_ask_depth_share_from_levels_2_5 | 0.680054 | 10th percentile ask quantity share from levels 2-5 |
| top5_vs_beyond_l1_imbalance_corr | 0.938459 | Correlation between cumulative top-five imbalance and levels 2-5 imbalance |
| beyond_l1_imbalance_std | 0.288994 | Variation of levels 2-5 imbalance |
| top5_imbalance_std | 0.289602 | Variation of cumulative top-five imbalance |

## Feature Quality Audit

| feature | is_full_depth_feature | rows | non_null_rows | missing_pct | finite_pct | unique_values | std | mean | median | p01 | p99 | healthy_for_search |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| avg_spread_bps | 0 | 1636 | 1636 | 0 | 1 | 1635 | 1.30805 | 2.8444 | 2.67259 | 0.793196 | 8.27759 | 1 |
| bar_return_bps | 0 | 1636 | 1636 | 0 | 1 | 1570 | 8.88833 | 0.359939 | 0 | -24.2219 | 23.8918 | 1 |
| avg_cum_top5_qty_imbalance | 0 | 1636 | 1636 | 0 | 1 | 1636 | 0.289602 | -0.0152604 | -0.0201193 | -0.763296 | 0.66966 | 1 |
| avg_depth_beyond_l1_qty_imbalance | 1 | 1636 | 1636 | 0 | 1 | 1636 | 0.288994 | -0.00522297 | -0.00989065 | -0.719887 | 0.720442 | 1 |
| avg_level_weighted_depth_imbalance | 1 | 1636 | 1636 | 0 | 1 | 1636 | 0.298204 | -0.0326867 | -0.0388163 | -0.750462 | 0.694336 | 1 |
| avg_depth_slope_bid | 1 | 1636 | 1636 | 0 | 1 | 1565 | 1685.86 | 264.441 | 28.3125 | -728.141 | 4671.35 | 1 |
| avg_depth_slope_ask | 1 | 1636 | 1636 | 0 | 1 | 1548 | 1001.78 | 199.001 | 13.5625 | -1136.34 | 4214.16 | 1 |
| avg_depth_convexity_bid | 1 | 1636 | 1636 | 0 | 1 | 1565 | 87454.1 | -7159.08 | 28.125 | -36633.5 | 10070.5 | 1 |
| avg_depth_convexity_ask | 1 | 1636 | 1636 | 0 | 1 | 1564 | 7244.73 | -402.963 | 0.125 | -19524.5 | 11703.4 | 1 |
| avg_order_count_imbalance_l1_l5 | 1 | 1636 | 1636 | 0 | 1 | 1636 | 0.191176 | 0.0157224 | 0.0085475 | -0.416336 | 0.534234 | 1 |
| avg_qty_per_order_bid_l1_l5 | 0 | 1636 | 1636 | 0 | 1 | 1636 | 2439.93 | 378.257 | 76.5498 | 4.43396 | 6579.59 | 1 |
| avg_qty_per_order_ask_l1_l5 | 0 | 1636 | 1636 | 0 | 1 | 1636 | 740.535 | 274.358 | 74.7181 | 4.29803 | 4011.22 | 1 |
| top5_qty_churn_sum | 1 | 1636 | 1636 | 0 | 1 | 1617 | 980889 | 165058 | 29228.5 | 1090 | 2.15671e+06 | 1 |
| top5_order_churn_sum | 1 | 1636 | 1636 | 0 | 1 | 536 | 212.058 | 293.694 | 250 | 37 | 1262.3 | 1 |
| depth_replenishment_pressure | 1 | 1636 | 1636 | 0 | 1 | 1481 | 73894.5 | 13992.2 | 2937 | 74.05 | 223853 | 1 |
| depth_withdrawal_pressure | 1 | 1636 | 1636 | 0 | 1 | 1478 | 28586.5 | 9528.43 | 2923.5 | 89.35 | 141959 | 1 |
| l1_price_shift_abs_sum | 0 | 1636 | 1636 | 0 | 1 | 721 | 22.3253 | 4.88289 | 1.6 | 0 | 45.65 | 1 |
| volume_increment_sum | 0 | 1636 | 1636 | 0 | 1 | 1559 | 46856.4 | 16262.8 | 4808 | 69.4 | 217080 | 1 |

## Top Feature Label Associations

| feature | is_full_depth_feature | label | usable_pair_rows | pearson_ic | spearman_ic | abs_spearman_ic | top_minus_bottom_future_return_bps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| avg_order_count_imbalance_l1_l5 | 1 | future_return_h10 | 1316 | 0.11815 | 0.147539 | 0.147539 | 7.43122 |
| avg_order_count_imbalance_l1_l5 | 1 | future_return_h6 | 1444 | 0.0798463 | 0.0984476 | 0.0984476 | 3.19996 |
| avg_order_count_imbalance_l1_l5 | 1 | future_return_h3 | 1540 | 0.0563807 | 0.07236 | 0.07236 | 1.60647 |
| avg_cum_top5_qty_imbalance | 0 | future_return_h3 | 1540 | 0.0290951 | 0.0606113 | 0.0606113 | 1.654 |
| avg_level_weighted_depth_imbalance | 1 | future_return_h3 | 1540 | 0.026444 | 0.0593991 | 0.0593991 | 1.84225 |
| avg_depth_convexity_ask | 1 | future_return_h6 | 1444 | -0.049543 | -0.0590689 | 0.0590689 | -1.96555 |
| avg_depth_slope_bid | 1 | future_return_h10 | 1316 | -0.0069752 | 0.055191 | 0.055191 | 5.60214 |
| avg_depth_beyond_l1_qty_imbalance | 1 | future_return_h3 | 1540 | 0.0242263 | 0.0527479 | 0.0527479 | 1.40435 |
| avg_depth_beyond_l1_qty_imbalance | 1 | future_return_h10 | 1316 | 0.0217965 | 0.0491746 | 0.0491746 | 1.20974 |
| avg_depth_convexity_ask | 1 | future_return_h10 | 1316 | -0.0382132 | -0.0480791 | 0.0480791 | -1.58248 |
| avg_cum_top5_qty_imbalance | 0 | future_return_h6 | 1444 | 0.0221902 | 0.0447406 | 0.0447406 | 1.63161 |
| avg_depth_slope_ask | 1 | future_return_h10 | 1316 | -0.050798 | 0.0441377 | 0.0441377 | 2.83514 |
| avg_depth_slope_ask | 1 | future_return_h3 | 1540 | -0.044667 | 0.0425894 | 0.0425894 | 1.19241 |
| avg_depth_beyond_l1_qty_imbalance | 1 | future_return_h6 | 1444 | 0.0207695 | 0.0411593 | 0.0411593 | 1.69663 |
| avg_cum_top5_qty_imbalance | 0 | future_return_h10 | 1316 | 0.0194965 | 0.0410537 | 0.0410537 | 1.62782 |
| avg_level_weighted_depth_imbalance | 1 | future_return_h6 | 1444 | 0.0137117 | 0.0388981 | 0.0388981 | 1.0741 |
| depth_replenishment_pressure | 1 | future_return_h10 | 1316 | -0.0276773 | 0.0364898 | 0.0364898 | 3.63522 |
| avg_level_weighted_depth_imbalance | 1 | future_return_h10 | 1316 | 0.0129072 | 0.0337331 | 0.0337331 | 2.03551 |
| top5_order_churn_sum | 1 | future_return_h6 | 1444 | 0.0625375 | 0.0322732 | 0.0322732 | 2.80005 |
| avg_depth_slope_bid | 1 | future_return_h6 | 1444 | 0.00526672 | 0.0315201 | 0.0315201 | 2.39944 |
| avg_qty_per_order_ask_l1_l5 | 0 | future_return_h10 | 1316 | -0.0444565 | 0.0256844 | 0.0256844 | 1.56211 |
| avg_depth_convexity_bid | 1 | future_return_h10 | 1316 | 0.0546292 | -0.0256721 | 0.0256721 | 1.22444 |
| avg_depth_slope_ask | 1 | future_return_h6 | 1444 | -0.105294 | 0.0254961 | 0.0254961 | 1.48672 |
| bar_return_bps | 0 | future_return_h10 | 1316 | -0.00954153 | 0.0246061 | 0.0246061 | 2.10561 |
| depth_withdrawal_pressure | 1 | future_return_h10 | 1316 | -0.107094 | 0.0238568 | 0.0238568 | 0.243689 |
| depth_replenishment_pressure | 1 | future_return_h3 | 1540 | 0.0378423 | 0.0231723 | 0.0231723 | 1.44156 |
| depth_replenishment_pressure | 1 | future_return_h6 | 1444 | -0.0104718 | 0.0227236 | 0.0227236 | 2.0314 |
| top5_qty_churn_sum | 1 | future_return_h6 | 1444 | -0.0137533 | 0.0223439 | 0.0223439 | 0.500701 |
| top5_order_churn_sum | 1 | future_return_h10 | 1316 | 0.0529852 | 0.0216918 | 0.0216918 | 2.75491 |
| avg_depth_convexity_bid | 1 | future_return_h6 | 1444 | -0.00666739 | -0.0202905 | 0.0202905 | 1.08179 |

# Phase296 Full-Year Top-Five-Depth Strategy-Family Sweep

Phase296 executes a full-year synthetic-only family sweep on Phase42's 3.0M-row event-state.

The annualized return denominator is fixed initial capital. The reused scheduler rejects trades when cash, same-symbol overlap, or max-concurrent constraints are hit.

Depth terminology note: this Phase42 input has top-five-depth feature proxies (`l5_imbalance` and a derived beyond-L1 proxy), not persisted raw bid/ask price and quantity for every book level. Raw L1-L5 book-state persistence remains a separate dense-lake milestone.

No replay, promotion, paper/live acceptance, or deployable profitability claim is opened by this search.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase296_full_year_sweep_complete | 1 | Phase296 full-year top-five-depth strategy family sweep completed |
| phase296_selected_route | P296_FULL_YEAR_TOP5_DEPTH_STRATEGY_FAMILY_SWEEP | Selected route |
| phase296_input_rows | 3012294 | Full-year event-state rows |
| phase296_input_trade_dates | 252 | Synthetic trading dates |
| phase296_input_symbols | 32 | Symbols |
| phase296_input_feed_profiles | 5 | Feed profiles |
| phase296_variant_rows | 360 | Profile-specific variants evaluated |
| phase296_scenario_rows | 720 | Cost200 fixed-capital scenarios evaluated |
| phase296_sparse_above12_scenario_rows | 0 | Above-12 sparse diagnostic rows |
| phase296_robust_portfolio_floor_scenario_rows | 0 | Robust floor rows |
| phase296_robust_portfolio_above12_scenario_rows | 0 | Robust above-12 rows |
| phase296_best_variant_id | P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H3 | Best variant |
| phase296_best_strategy_family | P296_TOP5_PRESSURE_CONTINUATION | Best family |
| phase296_best_feed_profile | disconnect_scenario | Best feed profile |
| phase296_best_cost200_annualized_pct | 2.90651 | Best fixed-capital annualized diagnostic |
| phase296_best_realized_net_pnl_inr | 13263.8 | Best net P&L |
| phase296_best_scheduled_event_rows | 6 | Best scheduled events |
| phase296_best_observed_trade_dates | 115 | Best observed dates |
| phase296_best_initial_capital_inr | 1e+06 | Fixed initial capital denominator |
| phase296_best_fixed_notional_inr | 100000 | Best fixed order notional |
| phase296_best_max_concurrent_positions | 2 | Best max concurrent positions |
| phase296_l1_only_variant_rows | 0 | L1-only variants |
| phase296_net_edge_live_mask_rows | 0 | Net edge live masks |
| phase296_annualized_denominator | fixed_initial_capital | Annualized denominator |
| phase296_strategy_replay_allowed | 0 | No replay |
| phase296_strategy_promotion_allowed | 0 | No promotion |
| phase296_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase296_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase296_hard_gate_pass_rows | 11 | Passed hard gates |
| phase296_hard_gate_rows | 11 | Hard gates |
| phase296_next_best_action | run_phase297_full_year_top5_depth_strategy_family_sweep_interpretation_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P296_PHASE295_WORK_ORDER_PRESENT | True | run_phase296_full_year_top5_depth_strategy_family_sweep_no_paper_live | Phase295 routes to Phase296 | hard |
| P296_INPUT_FULL_YEAR_PRESENT | True | rows=3012294;dates=252 | full-year Phase42 event-state | hard |
| P296_TOP5_DEPTH_PROXY_PRESENT | True | l1+l5+beyond_l1_proxy | top-five-depth proxy columns | hard |
| P296_VARIANTS_PRESENT | True | 360 | >=300 profile-specific variants | hard |
| P296_SCENARIOS_PRESENT | True | 720 | >=600 fixed-capital cost200 scenarios | hard |
| P296_FIXED_CAPITAL_REQUIRED | True | 1e+06 | fixed initial capital denominator | hard |
| P296_COST200_REQUIRED | True | cost200 | Zerodha cost stress profile | hard |
| P296_FULL_DEPTH_REQUIRED | True | l1_only=0 | top-five and levels 2-5 proxy required | hard |
| P296_NO_LIVE_NET_EDGE_MASKS | True | 0 | no net/gross edge live masks | hard |
| P296_FIXED_CAPITAL_ANNUALIZED_DENOMINATOR | True | fixed_initial_capital | no unlimited-capital annualization | hard |
| P296_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |

## Family Summary

| strategy_family | feed_profiles | scenario_rows | variant_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_variant_id | best_feed_profile |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P296_TOP5_PRESSURE_CONTINUATION | 5 | 120 | 60 | 6 | 0 | 0 | 0 | 0 | -0.509573 | -0.0740299 | 2.90651 | 13263.8 | P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H3 | disconnect_scenario |
| P296_MICROPRICE_DEPTH_REVERSAL | 5 | 120 | 60 | 6 | 0 | 0 | 0 | 0 | -0.825585 | -0.0494438 | 0.356236 | 1470.18 | P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H6 | good_retail |
| P296_TOP5_PRESSURE_REVERSAL_RANGE | 5 | 120 | 60 | 6 | 0 | 0 | 0 | 0 | -3.43115 | -0.163534 | 0.205132 | 626.793 | P296_TOP5_PRESSURE_REVERSAL_RANGE_STRESSED_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H6 | stressed_retail |
| P296_BEYOND_L1_ABSORPTION_CONTINUATION | 5 | 120 | 60 | 6 | 0 | 0 | 0 | 0 | -1.56106 | -0.107605 | 0.137739 | 623.106 | P296_BEYOND_L1_ABSORPTION_CONTINUATION_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H3 | good_retail |
| P296_SPREAD_COMPRESSED_MLOFI_FOLLOW | 5 | 120 | 60 | 6 | 0 | 0 | 0 | 0 | -2.23677 | -0.0885558 | 0.135137 | 900.915 | P296_SPREAD_COMPRESSED_MLOFI_FOLLOW_DISCONNECT_SCENARIO_IQ70_BQ70_NOT_WIDE_DL3_H6 | disconnect_scenario |
| P296_LIQUIDITY_VACUUM_MOMENTUM_CONTINUATION | 5 | 120 | 60 | 6 | 0 | 0 | 0 | 0 | -5.09981 | -0.226888 | 0.0831976 | 561.253 | P296_LIQUIDITY_VACUUM_MOMENTUM_CONTINUATION_STRESSED_RETAIL_IQ70_BQ70_NOT_WIDE_DL3_H6 | stressed_retail |

## Top Variants

| phase296_variant_id | feed_profile | strategy_family | spread_regime | daily_event_limit | exit_horizon_ticks | scenario_rows | selected_event_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_scheduled_event_rows | best_scenario_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H3 | disconnect_scenario | P296_TOP5_PRESSURE_CONTINUATION | NOT_WIDE | 3 | 3 | 2 | 321 | 6 | 0 | 0 | 0 | 0 | -0.024095 | 1.44121 | 2.90651 | 13263.8 | 6 | P271_P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H3_CAP1000000_NOT100000_CONC2_COST200 |
| P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H6 | disconnect_scenario | P296_TOP5_PRESSURE_CONTINUATION | NOT_WIDE | 3 | 6 | 2 | 294 | 5 | 0 | 0 | 0 | 0 | -0.137593 | 1.0306 | 2.19879 | 9859.67 | 5 | P271_P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL1_H3 | disconnect_scenario | P296_TOP5_PRESSURE_CONTINUATION | NOT_WIDE | 1 | 3 | 2 | 109 | 2 | 0 | 0 | 0 | 0 | -0.126511 | 0.877773 | 1.88206 | 8140.65 | 2 | P271_P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL1_H3_CAP1000000_NOT100000_CONC2_COST200 |
| P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H1 | disconnect_scenario | P296_TOP5_PRESSURE_CONTINUATION | NOT_WIDE | 3 | 1 | 2 | 333 | 6 | 0 | 0 | 0 | 0 | -0.0614146 | 0.72899 | 1.51939 | 6994.04 | 6 | P271_P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H1_CAP1000000_NOT100000_CONC2_COST200 |
| P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL1_H6 | disconnect_scenario | P296_TOP5_PRESSURE_CONTINUATION | NOT_WIDE | 1 | 6 | 2 | 100 | 2 | 0 | 0 | 0 | 0 | 0.0104511 | 0.617495 | 1.22454 | 4859.28 | 2 | P271_P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL1_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL1_H1 | disconnect_scenario | P296_TOP5_PRESSURE_CONTINUATION | NOT_WIDE | 1 | 1 | 2 | 115 | 2 | 0 | 0 | 0 | 0 | -0.0515763 | 0.381628 | 0.814832 | 3718.48 | 2 | P271_P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL1_H1_CAP1000000_NOT100000_CONC2_COST200 |
| P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H6 | good_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 6 | 2 | 104 | 2 | 0 | 0 | 0 | 0 | 0.338684 | 0.34746 | 0.356236 | 1470.18 | 1 | P271_P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H6_CAP1000000_NOT100000_CONC1_COST200 |
| P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ85_BQ70_NOT_WIDE_DL1_H6 | ideal_research | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 6 | 2 | 104 | 2 | 0 | 0 | 0 | 0 | 0.338684 | 0.34746 | 0.356236 | 1470.18 | 1 | P271_P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ85_BQ70_NOT_WIDE_DL1_H6_CAP1000000_NOT100000_CONC1_COST200 |
| P296_MICROPRICE_DEPTH_REVERSAL_NORMAL_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H6 | normal_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 6 | 2 | 104 | 2 | 0 | 0 | 0 | 0 | 0.338684 | 0.34746 | 0.356236 | 1470.18 | 1 | P271_P296_MICROPRICE_DEPTH_REVERSAL_NORMAL_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H6_CAP1000000_NOT100000_CONC1_COST200 |
| P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H3 | good_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 3 | 3 | 2 | 302 | 4 | 0 | 0 | 0 | 0 | -0.264511 | -0.015096 | 0.234319 | 1032.12 | 2 | P271_P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H3_CAP1000000_NOT100000_CONC1_COST200 |
| P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ85_BQ70_NOT_WIDE_DL3_H3 | ideal_research | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 3 | 3 | 2 | 302 | 4 | 0 | 0 | 0 | 0 | -0.264511 | -0.015096 | 0.234319 | 1032.12 | 2 | P271_P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ85_BQ70_NOT_WIDE_DL3_H3_CAP1000000_NOT100000_CONC1_COST200 |
| P296_MICROPRICE_DEPTH_REVERSAL_NORMAL_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H3 | normal_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 3 | 3 | 2 | 302 | 4 | 0 | 0 | 0 | 0 | -0.151805 | 0.0402109 | 0.232227 | 1032.12 | 2 | P271_P296_MICROPRICE_DEPTH_REVERSAL_NORMAL_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H3_CAP1000000_NOT100000_CONC1_COST200 |
| P296_TOP5_PRESSURE_REVERSAL_RANGE_STRESSED_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H6 | stressed_retail | P296_TOP5_PRESSURE_REVERSAL_RANGE | NOT_WIDE | 3 | 6 | 2 | 209 | 5 | 0 | 0 | 0 | 0 | 0.0372076 | 0.12117 | 0.205132 | 626.793 | 3 | P271_P296_TOP5_PRESSURE_REVERSAL_RANGE_STRESSED_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 |
| P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H3 | good_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 3 | 2 | 106 | 2 | 0 | 0 | 0 | 0 | 0.0345142 | 0.119683 | 0.204853 | 861.682 | 1 | P271_P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H3_CAP1000000_NOT100000_CONC1_COST200 |
| P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ85_BQ70_NOT_WIDE_DL1_H3 | ideal_research | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 3 | 2 | 106 | 2 | 0 | 0 | 0 | 0 | 0.0345142 | 0.119683 | 0.204853 | 861.682 | 1 | P271_P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ85_BQ70_NOT_WIDE_DL1_H3_CAP1000000_NOT100000_CONC1_COST200 |
| P296_MICROPRICE_DEPTH_REVERSAL_NORMAL_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H3 | normal_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 3 | 2 | 107 | 2 | 0 | 0 | 0 | 0 | 0.0341917 | 0.118565 | 0.202938 | 861.682 | 1 | P271_P296_MICROPRICE_DEPTH_REVERSAL_NORMAL_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H3_CAP1000000_NOT100000_CONC1_COST200 |
| P296_MICROPRICE_DEPTH_REVERSAL_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H3 | disconnect_scenario | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 3 | 3 | 2 | 316 | 6 | 0 | 0 | 0 | 0 | -0.0967466 | 0.0509839 | 0.198714 | 914.717 | 3 | P271_P296_MICROPRICE_DEPTH_REVERSAL_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H3_CAP1000000_NOT100000_CONC1_COST200 |
| P296_TOP5_PRESSURE_REVERSAL_RANGE_STRESSED_RETAIL_IQ70_BQ70_NOT_WIDE_DL3_H6 | stressed_retail | P296_TOP5_PRESSURE_REVERSAL_RANGE | NOT_WIDE | 3 | 6 | 2 | 240 | 5 | 0 | 0 | 0 | 0 | 0.0314834 | 0.102528 | 0.173574 | 626.793 | 3 | P271_P296_TOP5_PRESSURE_REVERSAL_RANGE_STRESSED_RETAIL_IQ70_BQ70_NOT_WIDE_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 |
| P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ70_BQ70_NOT_WIDE_DL1_H6 | good_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 6 | 2 | 157 | 2 | 0 | 0 | 0 | 0 | -0.0799177 | 0.0380714 | 0.156061 | 972.282 | 2 | P271_P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ70_BQ70_NOT_WIDE_DL1_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ70_BQ70_NOT_WIDE_DL1_H6 | ideal_research | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 6 | 2 | 157 | 2 | 0 | 0 | 0 | 0 | -0.0799177 | 0.0380714 | 0.156061 | 972.282 | 2 | P271_P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ70_BQ70_NOT_WIDE_DL1_H6_CAP1000000_NOT100000_CONC2_COST200 |

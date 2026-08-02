# Phase297 Full-Year Top-Five-Depth Strategy-Family Sweep Interpretation

Phase297 interprets Phase296 as a clean negative result for the Phase42 full-year top-five-depth proxy sweep.

No replay, promotion, paper/live acceptance, or deployable profitability claim is opened.

The selected next route moves from proxy features to raw dense top-five market-by-price book-state strategy work.

## Phase296 Summary

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
| phase296_best_cost200_annualized_pct | 2.906506686547222 | Best fixed-capital annualized diagnostic |
| phase296_best_realized_net_pnl_inr | 13263.820196544862 | Best net P&L |
| phase296_best_scheduled_event_rows | 6 | Best scheduled events |
| phase296_best_observed_trade_dates | 115 | Best observed dates |
| phase296_best_initial_capital_inr | 1000000.0 | Fixed initial capital denominator |
| phase296_best_fixed_notional_inr | 100000.0 | Best fixed order notional |
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
| P297_PHASE296_SWEEP_COMPLETE | True | 1 | Phase296 sweep complete | hard |
| P297_PHASE296_NEXT_ACTION_PRESENT | True | run_phase297_full_year_top5_depth_strategy_family_sweep_interpretation_no_paper_live | Phase296 routes to Phase297 interpretation | hard |
| P297_PHASE296_GATES_PASS | True | 11/11 | Phase296 hard gates pass | hard |
| P297_RANKED_INTERPRETATION_PRESENT | True | 360 | >0 ranked variants | hard |
| P297_CLOSES_PHASE296_FOR_ACCEPTANCE | True | 1 | Phase296 closed for acceptance | hard |
| P297_NO_SURVIVOR_TO_PROMOTE | True | sparse_above12=0;robust_above12=0 | no Phase296 survivor | hard |
| P297_BEST_TOO_SPARSE | True | 6 | <8 | hard |
| P297_FIXED_CAPITAL_DENOMINATOR | True | fixed_initial_capital | fixed_initial_capital | hard |
| P297_FULL_DEPTH_PROXY_BOUNDARY | True | l1_only=0;live_mask=0 | top-five proxy, no leakage | hard |
| P297_NEXT_ROUTE_SELECTED | True | P298_RAW_DENSE_TOP5_BOOK_STATE_STRATEGY_SWEEP | P298_RAW_DENSE_TOP5_BOOK_STATE_STRATEGY_SWEEP | hard |
| P297_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |
| P297_ROUTE_CONTRACT_PRESENT | True | 9 | Phase298 route contract rows | hard |

## Interpretation Ledger

| finding_id | evidence | severity | finding_present | interpretation |
| --- | --- | --- | --- | --- |
| phase296_executed | scenario_rows=720 | evidence | 1 | Phase296 executed the full-year top-five-depth proxy sweep. |
| phase296_failed_above12 | sparse_above12=0;best_ann=2.906506686547222 | hard_negative | 1 | No fixed-capital cost200 scenario exceeded the 12% sparse-discovery threshold. |
| phase296_no_robust_portfolio_evidence | robust_floor=0;robust_above12=0;best_events=6 | hard_negative | 1 | No robust portfolio evidence exists. |
| phase296_too_sparse_best_case | best_scheduled_events=6 | constraint | 1 | The best result is also too sparse for the sparse diagnostic event floor. |
| fixed_capital_boundary_preserved | fixed_initial_capital | constraint | 1 | No unlimited-capital annualization. |
| full_depth_proxy_boundary_preserved | l1_only=0;live_label_leakage=0 | constraint | 1 | Top-five/depth-beyond-L1 proxy and no live leakage boundaries held. |
| proxy_input_limit_identified | Phase42 lacks raw L1-L5 persisted book state columns | design_gap | 1 | The next search should use raw dense top-five book-state artifacts, not more Phase42 proxy variants. |
| raw_book_state_clues_preserved | clue_variants=9 | research_clue | 1 | Positive-but-below-threshold pockets can seed raw-book-state work without opening acceptance. |
| next_route_should_use_raw_book_state | P298_RAW_DENSE_TOP5_BOOK_STATE_STRATEGY_SWEEP | next_action | 1 | Move from proxy features to raw dense top-five book-state strategy sweep. |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| close_phase296_for_acceptance | 1 | best_ann=2.906506686547222;sparse_above12=0 | Do not accept, replay, or promote Phase296. |
| close_phase42_proxy_sweep_for_direct_acceptance | 1 | full_year_proxy_sweep_no_survivor | Avoid more minor proxy-only grid tweaks as the next action. |
| preserve_best_phase296_clue_for_raw_book_state | P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H3 | family=P296_TOP5_PRESSURE_CONTINUATION;feed=disconnect_scenario;max_ann=2.906506686547222 | Carry only as a raw-book-state clue, not as a strategy. |
| do_not_claim_portfolio_return | 1 | no_above12;no_robust_floor;best_events_below_floor | No deployable or robust annual return claim. |
| do_not_relax_annualized_denominator | 1 | fixed_initial_capital_required | Annualized return remains fixed-capital based. |
| selected_next_route | P298_RAW_DENSE_TOP5_BOOK_STATE_STRATEGY_SWEEP | Phase42 proxy input limit plus no survivor | Move to raw dense top-five book-state strategy sweep. |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P298_INPUTS | raw_synthetic_l2_dense_full_year;raw_l2_like_partitions;date_exchange_symbol_top5_book_state | Use the raw dense top-five book-state lake or raw-lake partitions, not only Phase42 proxy features. |
| P298_REQUIRED_BOOK_SCOPE | bid_price_1_to_5;ask_price_1_to_5;bid_qty_1_to_5;ask_qty_1_to_5;order_count_1_to_5_if_available | Persisted market-by-price levels 1-5 are required. |
| P298_TERMINOLOGY | Zerodha_top_five_market_by_price_depth_levels_1_to_5_not_universal_market_data_L1_to_L5 | Use correct terminology for book levels. |
| P298_STRATEGY_SEEDS | top5_pressure_continuation;microprice_depth_reversal;beyond_l1_absorption;spread_compressed_mlofi | Seed from Phase296 clues but recompute from raw levels. |
| P298_FEATURES | level_weighted_imbalance;depth_beyond_l1;queue_size_slope;spread_ticks;microprice_l1_to_l5;book_churn;level_replenishment | Exploit raw book levels rather than proxy-only l5 imbalance. |
| P298_COST_CAPITAL | fixed_initial_capital;cost200_required;Zerodha_intraday_equity_formula;max_concurrent_scheduler | No unlimited capital or simplified bps-only costs. |
| P298_DISCOVERY_GATE | annualized_pct_gt_12.0;scheduled_event_rows_ge_8;multi_date_required | Sparse discovery remains a clue only. |
| P298_PORTFOLIO_GATE | scheduled_event_rows_ge_30;multi_symbol_and_multi_regime_required | Portfolio/profitability claims require robust breadth. |
| P298_BOUNDARY | no_paper_live;no_strategy_replay;no_deployable_profitability_claim;net_edge_live_mask_forbidden | Synthetic-only search; no acceptance until earned. |

## Family Interpretation

| strategy_family | feed_profiles | scenario_rows | variant_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_variant_id | best_feed_profile | close_proxy_family_for_acceptance | preserve_family_for_raw_book_state_sweep |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P296_TOP5_PRESSURE_CONTINUATION | 5 | 120 | 60 | 6 | 0 | 0 | 0 | 0 | -0.509573 | -0.0740299 | 2.90651 | 13263.8 | P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H3 | disconnect_scenario | 1 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL | 5 | 120 | 60 | 6 | 0 | 0 | 0 | 0 | -0.825585 | -0.0494438 | 0.356236 | 1470.18 | P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H6 | good_retail | 1 | 1 |
| P296_TOP5_PRESSURE_REVERSAL_RANGE | 5 | 120 | 60 | 6 | 0 | 0 | 0 | 0 | -3.43115 | -0.163534 | 0.205132 | 626.793 | P296_TOP5_PRESSURE_REVERSAL_RANGE_STRESSED_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H6 | stressed_retail | 1 | 0 |
| P296_BEYOND_L1_ABSORPTION_CONTINUATION | 5 | 120 | 60 | 6 | 0 | 0 | 0 | 0 | -1.56106 | -0.107605 | 0.137739 | 623.106 | P296_BEYOND_L1_ABSORPTION_CONTINUATION_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H3 | good_retail | 1 | 0 |
| P296_SPREAD_COMPRESSED_MLOFI_FOLLOW | 5 | 120 | 60 | 6 | 0 | 0 | 0 | 0 | -2.23677 | -0.0885558 | 0.135137 | 900.915 | P296_SPREAD_COMPRESSED_MLOFI_FOLLOW_DISCONNECT_SCENARIO_IQ70_BQ70_NOT_WIDE_DL3_H6 | disconnect_scenario | 1 | 0 |
| P296_LIQUIDITY_VACUUM_MOMENTUM_CONTINUATION | 5 | 120 | 60 | 6 | 0 | 0 | 0 | 0 | -5.09981 | -0.226888 | 0.0831976 | 561.253 | P296_LIQUIDITY_VACUUM_MOMENTUM_CONTINUATION_STRESSED_RETAIL_IQ70_BQ70_NOT_WIDE_DL3_H6 | stressed_retail | 1 | 0 |

## Top Ranked Variants

| phase296_variant_id | feed_profile | strategy_family | spread_regime | daily_event_limit | exit_horizon_ticks | scenario_rows | selected_event_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_scheduled_event_rows | best_scenario_id | above12_sparse_survivor | robust_portfolio_survivor | positive_but_below12 | too_sparse_for_sparse_diagnostic | too_sparse_for_portfolio_claim | preserve_as_raw_book_state_clue | current_proxy_sweep_acceptance_closed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H3 | disconnect_scenario | P296_TOP5_PRESSURE_CONTINUATION | NOT_WIDE | 3 | 3 | 2 | 321 | 6 | 0 | 0 | 0 | 0 | -0.024095 | 1.44121 | 2.90651 | 13263.8 | 6 | P271_P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H3_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H6 | disconnect_scenario | P296_TOP5_PRESSURE_CONTINUATION | NOT_WIDE | 3 | 6 | 2 | 294 | 5 | 0 | 0 | 0 | 0 | -0.137593 | 1.0306 | 2.19879 | 9859.67 | 5 | P271_P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL1_H3 | disconnect_scenario | P296_TOP5_PRESSURE_CONTINUATION | NOT_WIDE | 1 | 3 | 2 | 109 | 2 | 0 | 0 | 0 | 0 | -0.126511 | 0.877773 | 1.88206 | 8140.65 | 2 | P271_P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL1_H3_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H1 | disconnect_scenario | P296_TOP5_PRESSURE_CONTINUATION | NOT_WIDE | 3 | 1 | 2 | 333 | 6 | 0 | 0 | 0 | 0 | -0.0614146 | 0.72899 | 1.51939 | 6994.04 | 6 | P271_P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H1_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL1_H6 | disconnect_scenario | P296_TOP5_PRESSURE_CONTINUATION | NOT_WIDE | 1 | 6 | 2 | 100 | 2 | 0 | 0 | 0 | 0 | 0.0104511 | 0.617495 | 1.22454 | 4859.28 | 2 | P271_P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL1_H6_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL1_H1 | disconnect_scenario | P296_TOP5_PRESSURE_CONTINUATION | NOT_WIDE | 1 | 1 | 2 | 115 | 2 | 0 | 0 | 0 | 0 | -0.0515763 | 0.381628 | 0.814832 | 3718.48 | 2 | P271_P296_TOP5_PRESSURE_CONTINUATION_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL1_H1_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H6 | good_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 6 | 2 | 104 | 2 | 0 | 0 | 0 | 0 | 0.338684 | 0.34746 | 0.356236 | 1470.18 | 1 | P271_P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H6_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ85_BQ70_NOT_WIDE_DL1_H6 | ideal_research | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 6 | 2 | 104 | 2 | 0 | 0 | 0 | 0 | 0.338684 | 0.34746 | 0.356236 | 1470.18 | 1 | P271_P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ85_BQ70_NOT_WIDE_DL1_H6_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL_NORMAL_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H6 | normal_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 6 | 2 | 104 | 2 | 0 | 0 | 0 | 0 | 0.338684 | 0.34746 | 0.356236 | 1470.18 | 1 | P271_P296_MICROPRICE_DEPTH_REVERSAL_NORMAL_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H6_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H3 | good_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 3 | 3 | 2 | 302 | 4 | 0 | 0 | 0 | 0 | -0.264511 | -0.015096 | 0.234319 | 1032.12 | 2 | P271_P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H3_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ85_BQ70_NOT_WIDE_DL3_H3 | ideal_research | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 3 | 3 | 2 | 302 | 4 | 0 | 0 | 0 | 0 | -0.264511 | -0.015096 | 0.234319 | 1032.12 | 2 | P271_P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ85_BQ70_NOT_WIDE_DL3_H3_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL_NORMAL_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H3 | normal_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 3 | 3 | 2 | 302 | 4 | 0 | 0 | 0 | 0 | -0.151805 | 0.0402109 | 0.232227 | 1032.12 | 2 | P271_P296_MICROPRICE_DEPTH_REVERSAL_NORMAL_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H3_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| P296_TOP5_PRESSURE_REVERSAL_RANGE_STRESSED_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H6 | stressed_retail | P296_TOP5_PRESSURE_REVERSAL_RANGE | NOT_WIDE | 3 | 6 | 2 | 209 | 5 | 0 | 0 | 0 | 0 | 0.0372076 | 0.12117 | 0.205132 | 626.793 | 3 | P271_P296_TOP5_PRESSURE_REVERSAL_RANGE_STRESSED_RETAIL_IQ85_BQ70_NOT_WIDE_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H3 | good_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 3 | 2 | 106 | 2 | 0 | 0 | 0 | 0 | 0.0345142 | 0.119683 | 0.204853 | 861.682 | 1 | P271_P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H3_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ85_BQ70_NOT_WIDE_DL1_H3 | ideal_research | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 3 | 2 | 106 | 2 | 0 | 0 | 0 | 0 | 0.0345142 | 0.119683 | 0.204853 | 861.682 | 1 | P271_P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ85_BQ70_NOT_WIDE_DL1_H3_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL_NORMAL_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H3 | normal_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 3 | 2 | 107 | 2 | 0 | 0 | 0 | 0 | 0.0341917 | 0.118565 | 0.202938 | 861.682 | 1 | P271_P296_MICROPRICE_DEPTH_REVERSAL_NORMAL_RETAIL_IQ85_BQ70_NOT_WIDE_DL1_H3_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H3 | disconnect_scenario | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 3 | 3 | 2 | 316 | 6 | 0 | 0 | 0 | 0 | -0.0967466 | 0.0509839 | 0.198714 | 914.717 | 3 | P271_P296_MICROPRICE_DEPTH_REVERSAL_DISCONNECT_SCENARIO_IQ85_BQ70_NOT_WIDE_DL3_H3_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| P296_TOP5_PRESSURE_REVERSAL_RANGE_STRESSED_RETAIL_IQ70_BQ70_NOT_WIDE_DL3_H6 | stressed_retail | P296_TOP5_PRESSURE_REVERSAL_RANGE | NOT_WIDE | 3 | 6 | 2 | 240 | 5 | 0 | 0 | 0 | 0 | 0.0314834 | 0.102528 | 0.173574 | 626.793 | 3 | P271_P296_TOP5_PRESSURE_REVERSAL_RANGE_STRESSED_RETAIL_IQ70_BQ70_NOT_WIDE_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ70_BQ70_NOT_WIDE_DL1_H6 | good_retail | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 6 | 2 | 157 | 2 | 0 | 0 | 0 | 0 | -0.0799177 | 0.0380714 | 0.156061 | 972.282 | 2 | P271_P296_MICROPRICE_DEPTH_REVERSAL_GOOD_RETAIL_IQ70_BQ70_NOT_WIDE_DL1_H6_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
| P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ70_BQ70_NOT_WIDE_DL1_H6 | ideal_research | P296_MICROPRICE_DEPTH_REVERSAL | NOT_WIDE | 1 | 6 | 2 | 157 | 2 | 0 | 0 | 0 | 0 | -0.0799177 | 0.0380714 | 0.156061 | 972.282 | 2 | P271_P296_MICROPRICE_DEPTH_REVERSAL_IDEAL_RESEARCH_IQ70_BQ70_NOT_WIDE_DL1_H6_CAP1000000_NOT100000_CONC2_COST200 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |

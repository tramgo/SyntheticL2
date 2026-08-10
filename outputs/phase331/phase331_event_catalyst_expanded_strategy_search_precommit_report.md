# Phase331 Event-Catalyst Expanded Strategy Search Precommit

Phase331 precommits the training-only strategy search over the Phase330 expanded top-five-depth feature matrix.
It carries the attached passive-aware execution realism constraints as execution-policy boundaries without reopening the already-falsified Phase300 passive-aware route.
It does not execute strategy search, replay, promote, open paper/live acceptance, or claim profitability.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase331_expanded_strategy_search_precommit_complete | 1 | Phase331 expanded strategy search precommit completed |
| phase331_strategy_family_rows | 15 | Strategy family rows |
| phase331_depth_beyond_l1_family_rows | 15 | Families using depth levels 2-5 |
| phase331_search_grid_rows | 69120 | Search grid rows before family expansion |
| phase331_expanded_variant_upper_bound_rows | 1036800 | Family x grid upper bound |
| phase331_cost200_grid_rows | 17280 | 2x cost-stress grid rows |
| phase331_passive_aware_grid_rows | 34560 | Passive-aware execution grid rows |
| phase331_event_bucket_policy_rows | 5 | Observable event-bucket policies |
| phase331_acceptance_contract_rows | 17 | Acceptance contract rows |
| phase331_work_order_rows | 10 | Phase332 work-order rows |
| phase331_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha cost model version |
| phase331_full_depth_required | 1 | Depth levels 1-5 required |
| phase331_depth_beyond_l1_required | 1 | Depth levels 2-5 materiality required |
| phase331_l1_only_candidate_allowed | 0 | L1-only candidate path closed |
| phase331_net_edge_live_mask_rows_allowed | 0 | No net-edge live lookahead mask allowed |
| phase331_fixed_capital_required | 1 | Fixed initial capital denominator required |
| phase331_cost200_required | 1 | 2x cost stress required |
| phase331_passive_realism_penalties_required | 1 | Fill probability, adverse selection and forced flatten required for passive-aware rows |
| phase331_strategy_search_execution_allowed_next | 1 | Phase332 training-only search may run if gates pass |
| phase331_strategy_replay_allowed | 0 | No replay |
| phase331_strategy_promotion_allowed | 0 | No promotion |
| phase331_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase331_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase331_hard_gate_pass_rows | 14 | Passed hard gates |
| phase331_hard_gate_rows | 14 | Hard gates |
| phase331_next_best_action | run_phase332_event_catalyst_expanded_strategy_search_training_only_no_replay | Recommended next action |

## Strategy family catalog

| family_id | signal_formula | required_live_feature_columns | target_columns | uses_depth_beyond_l1 | description |
| --- | --- | --- | --- | --- | --- |
| P331_DEPTH_PRESSURE_CONTINUATION | sign(event_depth_l2_l5_pressure) | event_depth_l2_l5_pressure | target_post_300s_mid_return_bps;target_post_900s_mid_return_bps | 1 | Follow depth-beyond-L1 pressure after catalyst events. |
| P331_DEPTH_PRESSURE_REVERSAL | -sign(event_depth_l2_l5_pressure) | event_depth_l2_l5_pressure | target_post_300s_mid_return_bps;target_post_900s_mid_return_bps | 1 | Fade depth-beyond-L1 pressure after catalyst events. |
| P331_DEPTH_ACCEL_CONTINUATION | sign(event_depth_l2_l5_pressure - pre300_depth_l2_l5_pressure_avg) | event_depth_l2_l5_pressure;pre300_depth_l2_l5_pressure_avg | target_post_300s_mid_return_bps;target_post_900s_mid_return_bps | 1 | Follow event-time acceleration versus pre-event depth-beyond-L1 pressure. |
| P331_DEPTH_ACCEL_REVERSAL | -sign(event_depth_l2_l5_pressure - pre300_depth_l2_l5_pressure_avg) | event_depth_l2_l5_pressure;pre300_depth_l2_l5_pressure_avg | target_post_300s_mid_return_bps;target_post_900s_mid_return_bps | 1 | Fade event-time acceleration versus pre-event depth-beyond-L1 pressure. |
| P331_QTY_IMBALANCE_CONTINUATION | sign(event_depth_l2_l5_qty_imbalance) | event_depth_l2_l5_qty_imbalance | target_post_60s_mid_return_bps;target_post_300s_mid_return_bps | 1 | Follow levels 2-5 quantity imbalance. |
| P331_QTY_IMBALANCE_REVERSAL | -sign(event_depth_l2_l5_qty_imbalance) | event_depth_l2_l5_qty_imbalance | target_post_60s_mid_return_bps;target_post_300s_mid_return_bps | 1 | Fade levels 2-5 quantity imbalance. |
| P331_ORDER_IMBALANCE_CONTINUATION | sign(event_depth_l2_l5_order_imbalance) | event_depth_l2_l5_order_imbalance | target_post_60s_mid_return_bps;target_post_300s_mid_return_bps | 1 | Follow order-count imbalance across levels 2-5. |
| P331_ORDER_IMBALANCE_REVERSAL | -sign(event_depth_l2_l5_order_imbalance) | event_depth_l2_l5_order_imbalance | target_post_60s_mid_return_bps;target_post_300s_mid_return_bps | 1 | Fade order-count imbalance across levels 2-5. |
| P331_MICROPRICE_DEPTH_CONFIRM | sign(pre300_microprice_minus_mid_avg) when same sign as event_depth_l2_l5_qty_imbalance | pre300_microprice_minus_mid_avg;event_depth_l2_l5_qty_imbalance | target_post_60s_mid_return_bps;target_post_300s_mid_return_bps | 1 | Require top-of-book microprice and depth-beyond-L1 quantity imbalance to agree. |
| P331_PRE900_TO_EVENT_PRESSURE_SHIFT | sign(event_depth_l2_l5_pressure - pre900_depth_l2_l5_pressure_avg) | event_depth_l2_l5_pressure;pre900_depth_l2_l5_pressure_avg | target_post_300s_mid_return_bps;target_post_1800s_mid_return_bps | 1 | Trade pressure shifts from long pre-event context into event time. |
| P331_DEPTH_SHARE_COMPRESSION_REVERSAL | -sign(event_l2_l5_depth_share - pre300_l2_l5_depth_share_avg) | event_l2_l5_depth_share;pre300_l2_l5_depth_share_avg | target_post_300s_mid_return_bps;target_post_900s_mid_return_bps | 1 | Fade sudden displayed-depth compression beyond L1. |
| P331_DEPTH_SHARE_EXPANSION_CONTINUATION | sign(event_l2_l5_depth_share - pre300_l2_l5_depth_share_avg) | event_l2_l5_depth_share;pre300_l2_l5_depth_share_avg | target_post_300s_mid_return_bps;target_post_900s_mid_return_bps | 1 | Follow sudden displayed-depth expansion beyond L1. |
| P331_SPREAD_ADJUSTED_PRESSURE_CONTINUATION | sign(event_depth_pressure) | event_depth_pressure;event_l1_spread | target_post_60s_mid_return_bps;target_post_300s_mid_return_bps | 1 | Follow spread-adjusted full visible-depth pressure. |
| P331_SPREAD_ADJUSTED_PRESSURE_REVERSAL | -sign(event_depth_pressure) | event_depth_pressure;event_l1_spread | target_post_60s_mid_return_bps;target_post_300s_mid_return_bps | 1 | Fade spread-adjusted full visible-depth pressure. |
| P331_DEPTH_PRESSURE_TARGET_SHIFT | sign(pre300_depth_l2_l5_pressure_avg) | pre300_depth_l2_l5_pressure_avg | target_post_300s_depth_pressure_shift | 1 | Use pre-event L2-L5 pressure to predict subsequent liquidity-pressure shift. |

## Search grid preview

| horizon_seconds | threshold_policy | cost_profile | initial_capital_inr | fixed_notional_inr | max_concurrent_positions | side_policy | execution_policy | event_bucket_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_short | taker_entry_taker_exit | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_short | taker_entry_taker_exit | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_short | taker_entry_taker_exit | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_short | taker_entry_taker_exit | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_short | taker_entry_taker_exit | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_short | passive_aware_directional_with_penalties | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_short | passive_aware_directional_with_penalties | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_short | passive_aware_directional_with_penalties | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_short | passive_aware_directional_with_penalties | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_short | passive_aware_directional_with_penalties | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_only | taker_entry_taker_exit | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_only | taker_entry_taker_exit | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_only | taker_entry_taker_exit | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_only | taker_entry_taker_exit | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_only | taker_entry_taker_exit | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_only | passive_aware_directional_with_penalties | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_only | passive_aware_directional_with_penalties | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_only | passive_aware_directional_with_penalties | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_only | passive_aware_directional_with_penalties | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_only | passive_aware_directional_with_penalties | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | short_only | taker_entry_taker_exit | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | short_only | taker_entry_taker_exit | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | short_only | taker_entry_taker_exit | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | short_only | taker_entry_taker_exit | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | short_only | taker_entry_taker_exit | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | short_only | passive_aware_directional_with_penalties | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | short_only | passive_aware_directional_with_penalties | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | short_only | passive_aware_directional_with_penalties | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | short_only | passive_aware_directional_with_penalties | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | short_only | passive_aware_directional_with_penalties | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_short | taker_entry_taker_exit | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_short | taker_entry_taker_exit | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_short | taker_entry_taker_exit | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_short | taker_entry_taker_exit | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_short | taker_entry_taker_exit | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_short | passive_aware_directional_with_penalties | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_short | passive_aware_directional_with_penalties | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_short | passive_aware_directional_with_penalties | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_short | passive_aware_directional_with_penalties | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_short | passive_aware_directional_with_penalties | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_only | taker_entry_taker_exit | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_only | taker_entry_taker_exit | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_only | taker_entry_taker_exit | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_only | taker_entry_taker_exit | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_only | taker_entry_taker_exit | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_only | passive_aware_directional_with_penalties | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_only | passive_aware_directional_with_penalties | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_only | passive_aware_directional_with_penalties | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_only | passive_aware_directional_with_penalties | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_only | passive_aware_directional_with_penalties | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | short_only | taker_entry_taker_exit | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | short_only | taker_entry_taker_exit | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | short_only | taker_entry_taker_exit | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | short_only | taker_entry_taker_exit | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | short_only | taker_entry_taker_exit | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | short_only | passive_aware_directional_with_penalties | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | short_only | passive_aware_directional_with_penalties | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | short_only | passive_aware_directional_with_penalties | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | short_only | passive_aware_directional_with_penalties | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | short_only | passive_aware_directional_with_penalties | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_short | taker_entry_taker_exit | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_short | taker_entry_taker_exit | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_short | taker_entry_taker_exit | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_short | taker_entry_taker_exit | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_short | taker_entry_taker_exit | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_short | passive_aware_directional_with_penalties | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_short | passive_aware_directional_with_penalties | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_short | passive_aware_directional_with_penalties | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_short | passive_aware_directional_with_penalties | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_short | passive_aware_directional_with_penalties | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_only | taker_entry_taker_exit | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_only | taker_entry_taker_exit | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_only | taker_entry_taker_exit | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_only | taker_entry_taker_exit | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_only | taker_entry_taker_exit | liquidity_shock_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_only | passive_aware_directional_with_penalties | all_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_only | passive_aware_directional_with_penalties | preopen_gap_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_only | passive_aware_directional_with_penalties | earnings_like_events |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_only | passive_aware_directional_with_penalties | macro_or_index_context |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_only | passive_aware_directional_with_penalties | liquidity_shock_context |

## Acceptance contract

| contract_id | contract_value | description |
| --- | --- | --- |
| fixed_capital_denominator | required | Annualized return must be net P&L divided by fixed initial capital; no unlimited-capital return. |
| annualized_research_lead_threshold_pct | 12.0 | Sparse >12% annualized is a research lead only, not acceptance. |
| cost200_profile_required | zerodha_2x_all_in_cost_proxy | Every candidate family must be scored under a 2x cost stress profile. |
| zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Use documented Zerodha equity intraday NSE charges. |
| minimum_scheduled_event_rows_for_acceptance | 30 | Below 30 scheduled events is sparse clue only. |
| minimum_symbol_date_breadth_for_acceptance | 2_symbols_x_2_dates_positive | Avoid single-symbol/single-date pockets. |
| full_depth_required | zerodha_visible_depth_levels_1_to_5 | Use top-five market-by-price depth. |
| depth_beyond_l1_required | depth_levels_2_to_5_material | No L1-only strategy candidates. |
| target_separation | target_columns_prefixed_and_not_live_features | No target column may be used as a live signal input. |
| net_edge_live_mask | forbidden | No lookahead net-edge live mask. |
| passive_fill_policy_if_used | pessimistic_back_of_queue_fill_probability | Passive-aware variants must include fill probability, not assumed fills. |
| adverse_selection_if_passive | required | Passive-aware variants must penalize filled passive orders for toxicity/adverse selection. |
| forced_flatten_if_passive | required | Any unfilled/unexited passive-aware inventory must pay taker flatten cost. |
| maker_rebate_assumption | forbidden | Retail maker rebate is not assumed. |
| phase331_execution_now | forbidden | Phase331 is precommit only; Phase332 may run training-only search. |
| strategy_replay_allowed | forbidden | No replay opens from Phase331. |
| paper_live_or_profitability_claim | forbidden | No paper/live/deployable claim from precommit or training search. |

## Phase332 work order

| work_order_id | scope | description |
| --- | --- | --- |
| load_phase330_matrix | outputs/phase330/phase330_event_catalyst_expanded_feature_matrix.parquet | Use the accepted compact expanded matrix. |
| expand_family_grid | family_catalog x search_grid | Evaluate directional full-depth families only. |
| compute_signed_signals | family-specific live feature formulas | Use no target_ columns in signal construction. |
| score_targets | target_post_{60,300,900,1800}s_mid_return_bps and target_post_300s_depth_pressure_shift | Targets are outcomes only. |
| apply_event_bucket_policy | event_bucket_policy | Bucket policies must be observable context labels, not target/net-edge filters. |
| apply_zerodha_costs | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Apply brokerage, STT, transaction, GST, SEBI, stamp duty, and slippage/cost stress. |
| apply_fixed_capital_scheduler | initial_capital, fixed_notional, max_concurrent_positions | Reject unlimited-capital annual-return math. |
| apply_passive_aware_penalties | fill_probability + adverse_selection + forced_flatten | Only for passive-aware execution-policy rows. |
| apply_controls | side_flip + random_side + shuffled_label + no_l1_only + no_net_edge_mask | Controls decide whether a clue is meaningful. |
| write_training_search_outputs | outputs/phase332 | Training-only search outputs; no replay/promotion/paper-live. |

## Zerodha cost component catalog

| component | formula | side | rate | source_url | rounding_or_cap |
| --- | --- | --- | --- | --- | --- |
| brokerage | min(0.03% of executed order value, Rs 20) per buy/sell executed order | buy_and_sell | 0.0003 | https://zerodha.com/charges/ | Rs 20 cap per executed order |
| stt | 0.025% on equity intraday sell side; rounded to nearest rupee | sell | 0.00025 | https://support.zerodha.com/category/account-opening/resident-individual/ri-charges/articles/how-is-the-securities-transaction-tax-stt-calculated | nearest rupee |
| nse_transaction_charge | 0.00307% of buy plus sell turnover | buy_and_sell | 3.07e-05 | https://zerodha.com/charges/ | unrounded analytical estimate |
| sebi_charge | Rs 10 per crore of buy plus sell turnover | buy_and_sell | 1e-06 | https://zerodha.com/charges/ | unrounded analytical estimate |
| stamp_duty | 0.003% on buy side | buy | 3e-05 | https://zerodha.com/charges/ | unrounded analytical estimate |
| gst | 18% of brokerage plus SEBI charges plus transaction charges | buy_and_sell | 0.18 | https://zerodha.com/charges/ | unrounded analytical estimate |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P331_PHASE330_COMPLETE | True | 1 | 1 | hard |
| P331_PHASE330_MATRIX_BREADTH | True | 1600 | 1600 | hard |
| P331_PHASE330_TARGET_SEPARATION | True | 0 | 0 | hard |
| P331_PHASE330_DEPTH_COLUMNS_PRESENT | True | 23 | >=20 | hard |
| P331_FAMILY_CATALOG_PRESENT | True | 15 | >=15 | hard |
| P331_ALL_FAMILIES_USE_DEPTH_BEYOND_L1 | True | 15/15 | all | hard |
| P331_SEARCH_GRID_PRESENT | True | 69120 | >0 | hard |
| P331_COST200_PRESENT | True | 17280 | >0 | hard |
| P331_PASSIVE_AWARE_ROWS_PRESENT | True | 34560 | >0 | hard |
| P331_FIXED_CAPITAL_PRESENT | True | present | present | hard |
| P331_PASSIVE_REALISM_PENALTIES_PRESENT | True | fill+adverse+flatten | present | hard |
| P331_WORK_ORDER_PRESENT | True | 10 | >=10 | hard |
| P331_NO_STRATEGY_SEARCH_EXECUTED_NOW | True | phase331_execution_now=0 | 0 | hard |
| P331_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |


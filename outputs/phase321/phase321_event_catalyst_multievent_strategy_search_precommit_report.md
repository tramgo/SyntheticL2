# Phase321 Event-Catalyst Multi-Event Strategy Search Precommit

Phase321 precommits the training-only strategy search over the Phase320 multi-event top-five-depth feature matrix.
It includes the attached passive-aware execution realism constraints as execution-policy boundaries, but does not reopen the older Phase300 route.
It does not execute strategy search, replay, promote, open paper/live acceptance, or claim profitability.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase321_multievent_strategy_search_precommit_complete | 1 | Phase321 multi-event strategy search precommit completed |
| phase321_strategy_family_rows | 10 | Strategy family rows |
| phase321_depth_beyond_l1_family_rows | 10 | Families using depth levels 2-5 |
| phase321_search_grid_rows | 13824 | Search grid rows before family expansion |
| phase321_expanded_variant_upper_bound_rows | 138240 | Family x grid upper bound |
| phase321_cost200_grid_rows | 3456 | 2x cost-stress grid rows |
| phase321_passive_aware_grid_rows | 6912 | Passive-aware execution grid rows |
| phase321_acceptance_contract_rows | 16 | Acceptance contract rows |
| phase321_work_order_rows | 8 | Phase322 work-order rows |
| phase321_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha cost model version |
| phase321_full_depth_required | 1 | Depth levels 1-5 required |
| phase321_depth_beyond_l1_required | 1 | Depth levels 2-5 materiality required |
| phase321_l1_only_candidate_allowed | 0 | L1-only candidate path closed |
| phase321_net_edge_live_mask_rows_allowed | 0 | No net-edge live lookahead mask allowed |
| phase321_fixed_capital_required | 1 | Fixed initial capital denominator required |
| phase321_cost200_required | 1 | 2x cost stress required |
| phase321_passive_realism_penalties_required | 1 | Fill probability, adverse selection and forced flatten required for passive-aware rows |
| phase321_strategy_search_execution_allowed_next | 1 | Phase322 training-only search may run if gates pass |
| phase321_strategy_replay_allowed | 0 | No replay |
| phase321_strategy_promotion_allowed | 0 | No promotion |
| phase321_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase321_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase321_hard_gate_pass_rows | 13 | Passed hard gates |
| phase321_hard_gate_rows | 13 | Hard gates |
| phase321_next_best_action | run_phase322_event_catalyst_multievent_strategy_search_training_only_no_replay | Recommended next action |

## Strategy family catalog

| family_id | signal_formula | required_live_feature_columns | target_columns | uses_depth_beyond_l1 | description |
| --- | --- | --- | --- | --- | --- |
| P321_DEPTH_PRESSURE_CONTINUATION | sign(event_depth_l2_l5_pressure) | event_depth_l2_l5_pressure | target_post_300s_mid_return_bps;target_post_900s_mid_return_bps | 1 | Follow depth-beyond-L1 pressure after catalyst events. |
| P321_DEPTH_PRESSURE_REVERSAL | -sign(event_depth_l2_l5_pressure) | event_depth_l2_l5_pressure | target_post_300s_mid_return_bps;target_post_900s_mid_return_bps | 1 | Fade depth-beyond-L1 pressure after catalyst events. |
| P321_DEPTH_ACCEL_CONTINUATION | sign(event_depth_l2_l5_pressure - pre300_depth_l2_l5_pressure_avg) | event_depth_l2_l5_pressure;pre300_depth_l2_l5_pressure_avg | target_post_300s_mid_return_bps;target_post_900s_mid_return_bps | 1 | Follow event-time acceleration versus pre-event depth-beyond-L1 pressure. |
| P321_DEPTH_ACCEL_REVERSAL | -sign(event_depth_l2_l5_pressure - pre300_depth_l2_l5_pressure_avg) | event_depth_l2_l5_pressure;pre300_depth_l2_l5_pressure_avg | target_post_300s_mid_return_bps;target_post_900s_mid_return_bps | 1 | Fade event-time acceleration versus pre-event depth-beyond-L1 pressure. |
| P321_QTY_IMBALANCE_CONTINUATION | sign(event_depth_l2_l5_qty_imbalance) | event_depth_l2_l5_qty_imbalance | target_post_60s_mid_return_bps;target_post_300s_mid_return_bps | 1 | Follow depth levels 2-5 quantity imbalance. |
| P321_QTY_IMBALANCE_REVERSAL | -sign(event_depth_l2_l5_qty_imbalance) | event_depth_l2_l5_qty_imbalance | target_post_60s_mid_return_bps;target_post_300s_mid_return_bps | 1 | Fade depth levels 2-5 quantity imbalance. |
| P321_ORDER_IMBALANCE_CONTINUATION | sign(event_depth_l2_l5_order_imbalance) | event_depth_l2_l5_order_imbalance | target_post_60s_mid_return_bps;target_post_300s_mid_return_bps | 1 | Follow order-count imbalance across depth levels 2-5. |
| P321_ORDER_IMBALANCE_REVERSAL | -sign(event_depth_l2_l5_order_imbalance) | event_depth_l2_l5_order_imbalance | target_post_60s_mid_return_bps;target_post_300s_mid_return_bps | 1 | Fade order-count imbalance across depth levels 2-5. |
| P321_MICROPRICE_DEPTH_CONFIRM | sign(pre300_microprice_minus_mid_avg) when same sign as event_depth_l2_l5_qty_imbalance | pre300_microprice_minus_mid_avg;event_depth_l2_l5_qty_imbalance | target_post_60s_mid_return_bps;target_post_300s_mid_return_bps | 1 | Require top-of-book microprice and depth-beyond-L1 quantity imbalance to agree. |
| P321_DEPTH_PRESSURE_TARGET_SHIFT | sign(pre300_depth_l2_l5_pressure_avg) | pre300_depth_l2_l5_pressure_avg | target_post_300s_depth_pressure_shift | 1 | Use pre-event depth pressure to predict subsequent liquidity-pressure shift. |

## Search grid preview

| horizon_seconds | threshold_policy | cost_profile | initial_capital_inr | fixed_notional_inr | max_concurrent_positions | side_policy | execution_policy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 1 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 2 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 25000 | 4 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 1 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 1 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 1 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 1 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 1 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 1 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 2 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 2 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 2 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 2 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 2 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 2 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 4 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 4 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 4 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 4 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 4 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 4 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 1 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 1 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 1 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 1 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 1 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 1 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 2 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 2 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 2 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 2 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 2 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 2 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 4 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 4 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 4 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 4 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 4 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 4 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 1 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 1 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 1 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 1 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 1 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 1 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 2 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 2 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 2 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 2 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 2 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 2 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 4 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 4 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 4 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 4 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 4 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 4 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 250000 | 25000 | 1 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 250000 | 25000 | 1 | long_short | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 250000 | 25000 | 1 | long_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 250000 | 25000 | 1 | long_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 250000 | 25000 | 1 | short_only | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 250000 | 25000 | 1 | short_only | passive_aware_directional_with_penalties |
| 60 | top_10pct_abs_signal | zerodha_base | 250000 | 25000 | 2 | long_short | taker_entry_taker_exit |
| 60 | top_10pct_abs_signal | zerodha_base | 250000 | 25000 | 2 | long_short | passive_aware_directional_with_penalties |

## Acceptance contract

| contract_id | contract_value | description |
| --- | --- | --- |
| fixed_capital_denominator | required | Annualized return must be net P&L divided by fixed initial capital; no unlimited-capital return. |
| annualized_research_lead_threshold_pct | 12.0 | Sparse >12% annualized is a research lead only, not acceptance. |
| cost200_profile_required | zerodha_2x_all_in_cost_proxy | Every candidate family must be scored under a 2x cost stress profile. |
| zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Use documented Zerodha equity intraday NSE charges. |
| minimum_scheduled_event_rows_for_acceptance | 30 | Below 30 scheduled events is sparse clue only. |
| minimum_symbol_date_breadth_for_acceptance | 2_symbols_x_2_dates_positive | Avoid single-symbol/single-date pockets. |
| full_depth_required | depth_levels_1_to_5 | Use top-five market-by-price depth. |
| depth_beyond_l1_required | depth_levels_2_to_5_material | No L1-only strategy candidates. |
| target_separation | target_columns_prefixed_and_not_live_features | No target column may be used as a live signal input. |
| net_edge_live_mask | forbidden | No lookahead net-edge live mask. |
| passive_fill_policy_if_used | pessimistic_back_of_queue_fill_probability | Passive-aware variants must include fill probability, not assumed fills. |
| adverse_selection_if_passive | required | Passive-aware variants must penalize filled passive orders for toxicity/adverse selection. |
| forced_flatten_if_passive | required | Any unfilled/unexited passive-aware inventory must pay taker flatten cost. |
| maker_rebate_assumption | forbidden | Retail maker rebate is not assumed. |
| phase321_execution_now | forbidden | Phase321 is precommit only; Phase322 may run training-only search. |
| paper_live_or_profitability_claim | forbidden | No paper/live/deployable claim from precommit or training search. |

## Phase322 work order

| work_order_id | scope | description |
| --- | --- | --- |
| load_phase320_matrix | outputs/phase320/phase320_event_catalyst_multievent_feature_matrix.csv | Use the accepted compact matrix. |
| expand_family_grid | family_catalog x search_grid | Evaluate directional full-depth families only. |
| compute_signed_signals | family-specific live feature formulas | Use no target_ columns in signal construction. |
| score_targets | target_post_{60,300,900,1800}s_mid_return_bps and target_post_300s_depth_pressure_shift | Targets are outcomes only. |
| apply_zerodha_costs | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Apply brokerage, STT, transaction, GST, SEBI, stamp duty, and slippage/cost stress. |
| apply_fixed_capital_scheduler | initial_capital, fixed_notional, max_concurrent_positions | Reject unlimited-capital annual-return math. |
| apply_passive_aware_penalties | fill_probability + adverse_selection + forced_flatten | Only for passive-aware execution-policy rows. |
| write_training_search_outputs | outputs/phase322 | Training-only search outputs; no replay/promotion. |

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
| P321_PHASE320_COMPLETE | True | 1 | 1 | hard |
| P321_PHASE320_MATRIX_BREADTH | True | 320 | 320 | hard |
| P321_PHASE320_TARGET_SEPARATION | True | 0 | 0 | hard |
| P321_FAMILY_CATALOG_PRESENT | True | 10 | >=10 | hard |
| P321_ALL_FAMILIES_USE_DEPTH_BEYOND_L1 | True | 10/10 | all | hard |
| P321_SEARCH_GRID_PRESENT | True | 13824 | >0 | hard |
| P321_COST200_PRESENT | True | 3456 | >0 | hard |
| P321_PASSIVE_AWARE_ROWS_PRESENT | True | 6912 | >0 | hard |
| P321_FIXED_CAPITAL_PRESENT | True | present | present | hard |
| P321_PASSIVE_REALISM_PENALTIES_PRESENT | True | fill+adverse+flatten | present | hard |
| P321_WORK_ORDER_PRESENT | True | 8 | >=8 | hard |
| P321_NO_STRATEGY_SEARCH_EXECUTED_NOW | True | phase321_execution_now=0 | 0 | hard |
| P321_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |


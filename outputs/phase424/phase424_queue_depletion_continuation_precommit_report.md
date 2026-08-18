# Phase424 Queue-Depletion Continuation Precommit

Phase424 freezes a materially new full-depth L2 thesis after Phase423 falsified the pair-spread positive lead.

The thesis is queue-depletion continuation: when levels 2-5 on the opposite side visibly evaporate, order counts thin, same-side deeper liquidity replenishes, and L1 pressure confirms the direction, the next few exact ticks may continue before costs overwhelm the move.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase424_queue_depletion_continuation_precommit_complete | 1 | Phase424 precommit completed |
| phase424_thesis_id | P424_FULL_DEPTH_QUEUE_DEPLETION_CONTINUATION | Frozen thesis |
| phase424_material_new_full_depth | 1 | Queue-depletion continuation |
| phase424_contract_rows | 17 | Contract rows |
| phase424_symbol_catalog_rows | 32 | Frozen symbols |
| phase424_parameter_freeze_rows | 20 | Frozen parameter rows |
| phase424_parameter_freeze_hash | c2d6af1dec28f743762b7b1865bded9184983e7f52be8f8e1f0e0e5efa82157d | Hash of frozen parameter table |
| phase424_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha cost model |
| phase424_cost_multiplier | 2 | Cost200 |
| phase424_initial_capital_inr | 1e+06 | Fixed capital |
| phase424_order_notional_inr | 100000 | Order notional |
| phase424_exact_forward_ticks_required | 3 | No proxy-only tick gate |
| phase424_execution_results_generated | 0 | Precommit only |
| phase424_strategy_promotion_allowed | 0 | No promotion |
| phase424_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase424_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase424_execution_allowed_next | 1 | Whether Phase425 may run |
| phase424_hard_gate_pass_rows | 17 | Passed hard gates |
| phase424_hard_gate_rows | 17 | Hard gates |
| phase424_next_best_action | run_phase425_queue_depletion_continuation_execution_no_paper_live | Recommended next action |

## Frozen Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P424_FULL_DEPTH_QUEUE_DEPLETION_CONTINUATION | Material-new single-name full-depth L2 source after Phase423. |
| material_difference | queue_depletion_continuation_not_pair_spread_not_market_making_not_bar_reversal | Continuation after visible opposite-side depth evaporation, not a rescue of closed routes. |
| market_hypothesis | when_l2_l5_opposite_queue_evaporates_and_l1_pressure_confirms_direction_short_horizon_continuation_may_pay_after_cost200 | A liquidity-consumption continuation thesis using the full top-five book. |
| entry_signal | opposite_l2_l5_depth_depletion_plus_order_count_thinning_plus_l1_imbalance_confirmation | Requires levels 2-5 depth and order-count features. |
| long_rule | ask_l2_l5_depletes_ask_order_count_thins_bid_l2_l5_replenishes_l1_imbalance_bid_dominant | Buy when ask-side queues thin and bid pressure confirms. |
| short_rule | bid_l2_l5_depletes_bid_order_count_thins_ask_l2_l5_replenishes_l1_imbalance_ask_dominant | Sell/short-side simulation mirror for research scoring only. |
| exit_rule | exit_after_entry_forward_ticks_stop_or_max_hold_ticks | Uses exact forward tick indexing in Phase425, not elapsed-time proxy-only. |
| execution_profile | taker_entry_then_taker_exit_cost200_no_passive_fill_no_maker_rebate | Directional taker execution with Zerodha costs. |
| full_depth_required | L1_to_L5_price_quantity_orders_with_levels_2_to_5_materiality | Top-five market-by-price book state is mandatory. |
| l1_only_control | remove_l2_l5_depletion_replenishment_and_order_count_terms | Primary must beat L1-only control by the frozen edge margin. |
| side_flip_control | invert_direction_for_same_events | Side-flip must not dominate primary. |
| real_anchor_cross_check | replay_same_frozen_rules_on_available_local_real_l2_dates | Check sign and cost survival on real anchors if enough rows exist. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha equity intraday NSE formula. |
| cost_multiplier | 2 | Cost200 acceptance scoring. |
| capital | initial=1000000.0;order_notional=100000.0 | Fixed capital denominator, no unlimited capital. |
| acceptance | round_trips>=30;dates>=5;symbols>=5;positive_date_fraction>=0.6;annualized>=12.0;l2_l5_edge_delta>=5.0 | Must be profitable with breadth and full-depth uniqueness. |
| forbidden | pair_spread_rescue;market_maker_rescue;passive_fill_rescue;bar_return_reversal_alone;post_result_threshold_tuning;promotion;paper_live;deployable_claim | Closed routes and boundaries. |

## Symbol Catalog

| symbol | exchange | universe_role | phase424_included |
| --- | --- | --- | --- |
| ADANIPORTS | NSE | liquid_cash_equity_or_etf | 1 |
| AXISBANK | NSE | liquid_cash_equity_or_etf | 1 |
| BAJAJ-AUTO | NSE | liquid_cash_equity_or_etf | 1 |
| BANKBEES | NSE | liquid_cash_equity_or_etf | 1 |
| BHARTIARTL | NSE | liquid_cash_equity_or_etf | 1 |
| BPCL | NSE | liquid_cash_equity_or_etf | 1 |
| BRITANNIA | NSE | liquid_cash_equity_or_etf | 1 |
| CIPLA | NSE | liquid_cash_equity_or_etf | 1 |
| DRREDDY | NSE | liquid_cash_equity_or_etf | 1 |
| GOLDBEES | NSE | liquid_cash_equity_or_etf | 1 |
| HCLTECH | NSE | liquid_cash_equity_or_etf | 1 |
| HDFCBANK | NSE | liquid_cash_equity_or_etf | 1 |
| HINDUNILVR | NSE | liquid_cash_equity_or_etf | 1 |
| ICICIBANK | NSE | liquid_cash_equity_or_etf | 1 |
| INFY | NSE | liquid_cash_equity_or_etf | 1 |
| ITBEES | NSE | liquid_cash_equity_or_etf | 1 |
| ITC | NSE | liquid_cash_equity_or_etf | 1 |
| JUNIORBEES | NSE | liquid_cash_equity_or_etf | 1 |
| KOTAKBANK | NSE | liquid_cash_equity_or_etf | 1 |
| LT | NSE | liquid_cash_equity_or_etf | 1 |
| M&M | NSE | liquid_cash_equity_or_etf | 1 |
| MARUTI | NSE | liquid_cash_equity_or_etf | 1 |
| NESTLEIND | NSE | liquid_cash_equity_or_etf | 1 |
| NIFTYBEES | NSE | liquid_cash_equity_or_etf | 1 |
| ONGC | NSE | liquid_cash_equity_or_etf | 1 |
| RELIANCE | NSE | liquid_cash_equity_or_etf | 1 |
| SBIN | NSE | liquid_cash_equity_or_etf | 1 |
| SUNPHARMA | NSE | liquid_cash_equity_or_etf | 1 |
| TCS | NSE | liquid_cash_equity_or_etf | 1 |
| TECHM | NSE | liquid_cash_equity_or_etf | 1 |
| ULTRACEMCO | NSE | liquid_cash_equity_or_etf | 1 |
| WIPRO | NSE | liquid_cash_equity_or_etf | 1 |

## Frozen Parameters

| parameter_id | value | status |
| --- | --- | --- |
| P424_LOOKBACK_TICKS | 180 | fixed |
| P424_ENTRY_FORWARD_TICKS | 3 | fixed |
| P424_MIN_FORWARD_HOLD_MS | 250 | fixed |
| P424_MAX_HOLD_TICKS | 30 | fixed |
| P424_MIN_L2_L5_OPPOSITE_DEPLETION | 0.35 | fixed |
| P424_MIN_L2_L5_SAME_SIDE_REPLENISHMENT | 0.1 | fixed |
| P424_MIN_L1_IMBALANCE_CONFIRMATION | 0.55 | fixed |
| P424_MAX_SPREAD_BPS | 8 | fixed |
| P424_MAX_OPPOSITE_L1_NOTIONAL_INR | 1.5e+06 | fixed |
| P424_MIN_L2_L5_DEPTH_NOTIONAL_INR | 2e+06 | fixed |
| P424_INITIAL_CAPITAL_INR | 1e+06 | fixed |
| P424_ORDER_NOTIONAL_INR | 100000 | fixed |
| P424_COST_MULTIPLIER | 2 | fixed |
| P424_MIN_COMPLETED_ROUND_TRIPS | 30 | fixed |
| P424_MIN_TRADE_DATES | 5 | fixed |
| P424_MIN_SYMBOLS | 5 | fixed |
| P424_MIN_POSITIVE_DATE_FRACTION | 0.6 | fixed |
| P424_ANNUALIZED_THRESHOLD_PCT | 12 | fixed |
| P424_MIN_L2_L5_EDGE_DELTA_VS_L1_ONLY_PCT | 5 | fixed |
| P424_SYMBOL_COUNT | 32 | fixed |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| phase298_dense_root | raw_synthetic_l2_dense_full_year | Raw dense source root. |
| phase298_full_depth_required | 1 | Must be one. |
| phase298_levels_2_to_5_required | 1 | Must be one. |
| phase298_l1_only_variant_rows | 0 | Must be zero. |
| phase298_net_edge_live_mask_rows | 0 | Must be zero. |
| phase298_schema_present_columns_min | 30 | Minimum L1-L5 schema columns. |
| phase423_selected_verdict | P423_PAIR_SPREAD_POSITIVE_LEAD_FALSIFIED_BY_REALISM_RETEST | Pair-spread route closure context. |
| phase423_same_family_tuning_allowed | 0 | Must be zero. |
| symbol_catalog_rows | 32 | Precommitted symbol count. |
| execution_results_generated_now | 0 | Precommit only. |

## Phase425 Hard-Gate Contract

| gate_id | requirement | severity | phase424_precommitted |
| --- | --- | --- | --- |
| P425_PHASE424_PRECOMMIT_USED | Execution must read Phase424 frozen contract and parameter freeze. | hard | 1 |
| P425_TICK_ORDERED_SINGLE_NAME_REPLAY | Ticks must be consumed in exchange-time order with no lookahead. | hard | 1 |
| P425_EXACT_FORWARD_TICK_INDEXING | Exit evaluation must use at least 3 exact post-entry ticks, not proxy-only elapsed time. | hard | 1 |
| P425_FORWARD_TIME_ENFORCED | Exit must also be at least 250.0 ms after entry. | hard | 1 |
| P425_FULL_DEPTH_L1_L5_REQUIRED | Feature rows must include L1-L5 price, quantity and order count fields. | hard | 1 |
| P425_LEVELS_2_TO_5_MATERIAL | Primary entry must require L2-L5 depletion/replenishment/order-count thinning. | hard | 1 |
| P425_L1_ONLY_CONTROL | L1-only control must be run and primary must beat it by the frozen edge margin. | hard | 1 |
| P425_SIDE_FLIP_CONTROL | Side-flip control must be run and must not dominate primary. | hard | 1 |
| P425_TAKER_ONLY_EXECUTION | No passive fill, queue priority advantage or maker rebate. | hard | 1 |
| P425_NO_LOOKAHEAD | All rolling queue-depletion features must be computed before entry tick. | hard | 1 |
| P425_COST200_FIXED_CAPITAL | Use Zerodha cost200 with fixed INR 1,000,000 denominator. | hard | 1 |
| P425_EVENT_FLOOR | Completed round trips >= 30. | hard | 1 |
| P425_DATE_BREADTH | Distinct trade dates >= 5. | hard | 1 |
| P425_SYMBOL_BREADTH | Distinct symbols >= 5. | hard | 1 |
| P425_POSITIVE_DATE_FRACTION | Positive date fraction >= 0.6. | hard | 1 |
| P425_ANNUALIZED_FLOOR | Annualized fixed-capital return >= 12.0 percent. | hard | 1 |
| P425_REAL_ANCHOR_CROSS_CHECK | Replay on available local real L2 dates and report sign/cost survival. | hard | 1 |
| P425_BOUNDARIES_CLOSED | No promotion, paper/live acceptance or deployable claim in Phase425. | hard | 1 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P424_PHASE298_RAW_DENSE_PRESENT | True | raw_synthetic_l2_dense_full_year | raw_synthetic_l2_dense_full_year | hard |
| P424_FULL_DEPTH_SCHEMA_PRESENT | True | 30 | >=30 | hard |
| P424_LEVELS_2_TO_5_REQUIRED | True | 1 | 1 | hard |
| P424_L1_ONLY_FORBIDDEN_AS_PRIMARY | True | 0 | 0 | hard |
| P424_NO_NET_EDGE_LIVE_MASK | True | 0 | 0 | hard |
| P424_PHASE423_PAIR_ROUTE_CLOSED | True | P423_PAIR_SPREAD_POSITIVE_LEAD_FALSIFIED_BY_REALISM_RETEST | P423_PAIR_SPREAD_POSITIVE_LEAD_FALSIFIED_BY_REALISM_RETEST | hard |
| P424_NO_SAME_FAMILY_TUNING | True | 0 | 0 | hard |
| P424_MATERIAL_NEW_QUEUE_DEPLETION | True | queue_depletion_continuation_not_pair_spread_not_market_making_not_bar_reversal | queue_depletion_not_pair | hard |
| P424_SYMBOL_CATALOG_FROZEN | True | 32 | >=5 | hard |
| P424_FIXED_PARAMETERS_FROZEN | True | 20 | >=20 | hard |
| P424_EXACT_FORWARD_TICK_REQUIREMENT_FROZEN | True | ticks=3;ms=250.0 | ticks>=3;ms>=250 | hard |
| P424_FULL_DEPTH_UNIQUE_GATE_FROZEN | True | 5 | >0 | hard |
| P424_COST200_FIXED_CAPITAL_PINNED | True | cost=2.0;capital=1000000.0;order_notional=100000.0 | cost200_fixed_capital | hard |
| P424_EXECUTION_HARD_GATES_PRECOMMITTED | True | 18 | 18 | hard |
| P424_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P424_FORBIDDEN_ROUTES_CLOSED | True | pair_spread_rescue;market_maker_rescue;passive_fill_rescue;bar_return_reversal_alone;post_result_threshold_tuning;promotion;paper_live;deployable_claim | closed_routes_listed | hard |
| P424_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

No Phase424 strategy result, promotion, paper/live acceptance or deployable claim is generated.

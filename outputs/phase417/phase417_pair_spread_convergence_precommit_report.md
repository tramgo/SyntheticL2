# Phase417 Pair-Spread Convergence Precommit

Phase417 freezes a materially new non-directional full-depth L2 source after Phase416 closed the directional snapback route.

The thesis is market-neutral pair-spread convergence with taker-only equal-notional long/short legs and L1-L5 depth checks on both legs.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase417_pair_spread_convergence_precommit_complete | 1 | Phase417 precommit completed |
| phase417_thesis_id | P417_FULL_DEPTH_PAIR_SPREAD_CONVERGENCE_MARKET_NEUTRAL | Frozen thesis |
| phase417_material_new_non_directional | 1 | Market-neutral pair-spread convergence |
| phase417_contract_rows | 23 | Contract rows |
| phase417_pair_catalog_rows | 4 | Frozen pairs |
| phase417_parameter_freeze_rows | 15 | Frozen parameter rows |
| phase417_parameter_freeze_hash | 40e174686fa3b84c9f5b1da791b67c93900edeb742d45871686192d02b07df58 | Hash of frozen parameter table |
| phase417_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha cost model |
| phase417_cost_multiplier | 2 | Cost200 |
| phase417_initial_capital_inr | 1e+06 | Fixed capital |
| phase417_pair_notional_inr | 100000 | Gross pair notional |
| phase417_execution_results_generated | 0 | Precommit only |
| phase417_strategy_promotion_allowed | 0 | No promotion |
| phase417_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase417_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase417_execution_allowed_next | 1 | Whether Phase418 may run |
| phase417_hard_gate_pass_rows | 16 | Passed hard gates |
| phase417_hard_gate_rows | 16 | Hard gates |
| phase417_next_best_action | run_phase418_pair_spread_convergence_execution_no_paper_live | Recommended next action |

## Frozen Thesis Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P417_FULL_DEPTH_PAIR_SPREAD_CONVERGENCE_MARKET_NEUTRAL | Material-new non-directional full-depth L2 source after Phase416. |
| material_difference | market_neutral_pair_spread_convergence_not_single_name_directional_not_market_making | Long/short pair exposure, not one-name direction or passive quoting. |
| market_hypothesis | temporary_pair_spread_dislocation_with_adequate_l2_l5_liquidity_and_no_deep_book_conflict_may_converge | Non-directional relative-value thesis. |
| entry_signal | rolling_log_mid_spread_zscore_abs_ge_entry_threshold | Pair spread z-score, not bar-return reversal alone. |
| side_rule | if spread high short leg_a_long_leg_b; if spread low long_leg_a_short_leg_b | Market-neutral pair direction. |
| exit_rule | exit_on_zscore_reversion_stop_or_max_hold_ticks | Fixed exit, stop and max hold. |
| execution_profile | taker_entry_both_legs_taker_exit_both_legs_cost200 | No passive fills and no maker rebate. |
| lookback_ticks | 240 | Fixed rolling pair spread lookback. |
| entry_zscore | 1.75 | Fixed entry z-score. |
| exit_zscore | 0.35 | Fixed convergence exit. |
| stop_zscore | 3.25 | Fixed divergence stop. |
| max_hold_ticks | 360 | Fixed max hold. |
| max_spread_bps_per_leg | 8 | Avoid wide-spread execution per leg. |
| min_l2_l5_liquidity_per_leg_inr | 2e+06 | Full-depth liquidity gate beyond L1. |
| max_abs_l2_l5_imbalance_conflict | 0.65 | Avoid severe deep-book pressure against required leg direction. |
| full_depth_required | L1_to_L5_both_legs_with_levels_2_to_5_liquidity_and_imbalance | L1-only variants forbidden. |
| pair_catalog_rows | 4 | Precommitted pairs. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha equity intraday NSE formula. |
| cost_multiplier | 2 | Cost200 acceptance scoring. |
| capital | initial=1000000.0;pair_notional=100000.0;leg_notional=50000.0 | Fixed capital denominator, no unlimited capital. |
| acceptance | round_trips>=30;dates>=5;pairs>=2;positive_date_fraction>=0.6;annualized>=12.0 | Must be profitable with breadth. |
| controls | side_flip;levels_2_to_5_removed;single_leg_proxy;cost100_rank_stability;real_anchor_sign | Controls must be reported. |
| forbidden | directional_snapback_rescue;market_maker_rescue;passive_fill_rescue;bar_return_reversal_alone;promotion;paper_live;deployable_claim | Closed routes and boundaries. |

## Pair Catalog

| pair_id | leg_a | leg_b | gross_pair_notional_inr | leg_notional_inr | relationship |
| --- | --- | --- | --- | --- | --- |
| HDFCBANK_ICICIBANK | HDFCBANK | ICICIBANK | 100000 | 50000 | sector_or_macro_linked_large_liquid_names |
| HDFCBANK_AXISBANK | HDFCBANK | AXISBANK | 100000 | 50000 | sector_or_macro_linked_large_liquid_names |
| INFY_TCS | INFY | TCS | 100000 | 50000 | sector_or_macro_linked_large_liquid_names |
| RELIANCE_ONGC | RELIANCE | ONGC | 100000 | 50000 | sector_or_macro_linked_large_liquid_names |

## Frozen Parameters

| parameter_id | value | status |
| --- | --- | --- |
| P417_LOOKBACK_TICKS | 240 | fixed |
| P417_ENTRY_ZSCORE | 1.75 | fixed |
| P417_EXIT_ZSCORE | 0.35 | fixed |
| P417_STOP_ZSCORE | 3.25 | fixed |
| P417_MAX_HOLD_TICKS | 360 | fixed |
| P417_MAX_SPREAD_BPS_PER_LEG | 8 | fixed |
| P417_MIN_L2_L5_LIQUIDITY_PER_LEG_INR | 2e+06 | fixed |
| P417_MAX_ABS_L2_L5_IMBALANCE_CONFLICT | 0.65 | fixed |
| P417_INITIAL_CAPITAL_INR | 1e+06 | fixed |
| P417_PAIR_NOTIONAL_INR | 100000 | fixed |
| P417_COST_MULTIPLIER | 2 | fixed |
| P417_PAIR_HDFCBANK_ICICIBANK | HDFCBANK/ICICIBANK | fixed |
| P417_PAIR_HDFCBANK_AXISBANK | HDFCBANK/AXISBANK | fixed |
| P417_PAIR_INFY_TCS | INFY/TCS | fixed |
| P417_PAIR_RELIANCE_ONGC | RELIANCE/ONGC | fixed |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| phase298_dense_root | raw_synthetic_l2_dense_full_year | Raw dense source root. |
| phase298_full_depth_required | 1 | Must be one. |
| phase298_levels_2_to_5_required | 1 | Must be one. |
| phase298_l1_only_variant_rows | 0 | Must be zero. |
| phase298_net_edge_live_mask_rows | 0 | Must be zero. |
| phase298_schema_present_columns_min | 30 | Minimum L1-L5 schema columns. |
| phase416_selected_verdict | P416_DEEP_BOOK_DIVERGENCE_SNAPBACK_REJECTED_NON_SPARSE_NEGATIVE | Directional snapback closure context. |
| phase416_same_family_tuning_allowed | 0 | Must be zero. |
| pair_catalog_rows | 4 | Precommitted pair count. |
| symbols_needed | AXISBANK;HDFCBANK;ICICIBANK;INFY;ONGC;RELIANCE;TCS | Symbols required by Phase418. |
| execution_results_generated_now | 0 | Precommit only. |

## Phase418 Hard-Gate Contract

| gate_id | requirement | severity | phase417_precommitted |
| --- | --- | --- | --- |
| P418_TICK_ORDERED_PAIR_ALIGNMENT | Pair ticks must be aligned by timestamp without lookahead. | hard | 1 |
| P418_MARKET_NEUTRAL_PAIR_EXPOSURE | Both legs must be entered and exited with equal fixed notional. | hard | 1 |
| P418_TAKER_ONLY_EXECUTION | No passive fills, no maker rebate. | hard | 1 |
| P418_FULL_DEPTH_L1_L5_BOTH_LEGS | Both legs must use L1-L5 book state. | hard | 1 |
| P418_LEVELS_2_TO_5_MATERIAL | Levels 2-5 liquidity and imbalance gates required. | hard | 1 |
| P418_NO_LOOKAHEAD | Rolling z-score and depth features must be known before entry. | hard | 1 |
| P418_COST200_FIXED_CAPITAL | Use Zerodha cost200 and fixed INR 1,000,000 capital. | hard | 1 |
| P418_FIXED_PARAMETERS | No post-result tuning. | hard | 1 |
| P418_EVENT_FLOOR | Completed pair round trips >= 30. | hard | 1 |
| P418_DATE_BREADTH | Distinct trade dates >= 5. | hard | 1 |
| P418_PAIR_BREADTH | Distinct pairs >= 2. | hard | 1 |
| P418_POSITIVE_DATE_FRACTION | Positive date fraction >= 0.6. | hard | 1 |
| P418_ANNUALIZED_FLOOR | Annualized fixed-capital return >= 12.0 percent. | hard | 1 |
| P418_SIDE_FLIP_CONTROL | Side-flip pair direction must not dominate primary. | hard | 1 |
| P418_L2_L5_REMOVED_CONTROL | Removing levels 2-5 must degrade or invalidate primary. | hard | 1 |
| P418_SINGLE_LEG_PROXY_CONTROL | Pair result must not be explainable by one leg only. | hard | 1 |
| P418_COST100_RANK_STABILITY | Cost100 rank must not reverse acceptance ordering. | hard | 1 |
| P418_REAL_ANCHOR_CROSS_CHECK | Synthetic result sign must be checked on real anchors if available. | hard | 1 |
| P418_BOUNDARIES_CLOSED | No promotion, paper/live acceptance or deployable claim. | hard | 1 |

## Phase417 Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P417_PHASE298_RAW_DENSE_PRESENT | True | raw_synthetic_l2_dense_full_year | raw_synthetic_l2_dense_full_year | hard |
| P417_FULL_DEPTH_SCHEMA_PRESENT | True | 30 | >=30 | hard |
| P417_LEVELS_2_TO_5_REQUIRED | True | 1 | 1 | hard |
| P417_L1_ONLY_FORBIDDEN | True | 0 | 0 | hard |
| P417_NO_LOOKAHEAD_SOURCE | True | 0 | 0 | hard |
| P417_PHASE416_DIRECTIONAL_ROUTE_CLOSED | True | P416_DEEP_BOOK_DIVERGENCE_SNAPBACK_REJECTED_NON_SPARSE_NEGATIVE | P416_DEEP_BOOK_DIVERGENCE_SNAPBACK_REJECTED_NON_SPARSE_NEGATIVE | hard |
| P417_NO_SAME_FAMILY_TUNING | True | 0 | 0 | hard |
| P417_MARKET_NEUTRAL_MATERIAL_NEW | True | market_neutral_pair_spread_convergence_not_single_name_directional_not_market_making | market_neutral_not_directional | hard |
| P417_PAIR_CATALOG_FROZEN | True | 4 | >=4 | hard |
| P417_FIXED_PARAMETERS_FROZEN | True | 15 | >=15 | hard |
| P417_TAKER_ONLY_PINNED | True | taker_only_pair | present | hard |
| P417_COST200_FIXED_CAPITAL_PINNED | True | cost=2.0;capital=1000000.0;pair_notional=100000.0 | cost200_fixed_capital | hard |
| P417_EXECUTION_HARD_GATES_PRECOMMITTED | True | 19 | 19 | hard |
| P417_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P417_FORBIDDEN_ROUTES_CLOSED | True | directional_snapback_rescue;market_maker_rescue;passive_fill_rescue;bar_return_reversal_alone;promotion;paper_live;deployable_claim | closed_routes_listed | hard |
| P417_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

No strategy result, promotion, paper/live acceptance or deployable profitability claim is generated by Phase417.

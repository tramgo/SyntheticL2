# Phase311 Event-Catalyst Strategy Search Precommit

Phase311 defines the allowed training-only event-catalyst strategy search. It does not execute the search.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase311_strategy_search_precommit_complete | 1 | Phase311 event-catalyst strategy search precommit completed |
| phase311_strategy_family_rows | 8 | Strategy family rows |
| phase311_search_grid_rows | 432 | Search grid rows before family expansion |
| phase311_expanded_variant_upper_bound_rows | 3456 | Family x grid upper bound |
| phase311_capital_contract_rows | 8 | Fixed-capital contract rows |
| phase311_control_contract_rows | 9 | Control contract rows |
| phase311_full_depth_required | 1 | Full top-five depth required |
| phase311_depth_beyond_l1_required | 1 | Levels 2-5 materiality required |
| phase311_l1_only_candidate_allowed | 0 | L1-only candidate path closed |
| phase311_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha cost model version |
| phase311_strategy_search_execution_allowed_next | 1 | Phase312 training-only search may run if gates pass |
| phase311_strategy_replay_allowed | 0 | No replay |
| phase311_strategy_promotion_allowed | 0 | No promotion |
| phase311_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase311_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase311_hard_gate_pass_rows | 9 | Passed hard gates |
| phase311_hard_gate_rows | 9 | Hard gates |
| phase311_next_best_action | run_phase312_event_catalyst_strategy_search_training_only | Recommended next action |

## Strategy family catalog

| family_id | signal_formula | target_columns | description |
| --- | --- | --- | --- |
| event_depth_pressure_continuation | go_with_sign(event_l2_l5_pressure) | target_return_300s_bps;target_return_900s_bps | Tests whether L2-L5 pressure at event time follows through. |
| event_depth_pressure_reversal | go_against_sign(event_l2_l5_pressure) | target_return_300s_bps;target_return_900s_bps | Tests whether strong L2-L5 pressure mean-reverts after the event. |
| pre_event_pressure_shift_continuation | go_with_sign(event_l2_l5_pressure - pre_mean_l2_l5_pressure) | target_return_300s_bps;target_return_900s_bps | Tests whether pressure acceleration predicts continuation. |
| pre_event_pressure_shift_reversal | go_against_sign(event_l2_l5_pressure - pre_mean_l2_l5_pressure) | target_return_300s_bps;target_return_900s_bps | Tests whether pressure acceleration is an overreaction. |
| microprice_dislocation_continuation | go_with_sign((event_l1_microprice - event_l1_mid) / event_l1_mid) | target_return_60s_bps;target_return_300s_bps | Tests microprice dislocation follow-through. |
| microprice_dislocation_reversal | go_against_sign((event_l1_microprice - event_l1_mid) / event_l1_mid) | target_return_60s_bps;target_return_300s_bps | Tests microprice dislocation reversal. |
| pre_event_trend_reversal | go_against_sign((event_l1_mid / pre_mean_l1_mid) - 1) | target_return_300s_bps;target_return_900s_bps | Tests bar-return reversal around event context. |
| pre_event_trend_continuation | go_with_sign((event_l1_mid / pre_mean_l1_mid) - 1) | target_return_300s_bps;target_return_900s_bps | Tests event-time trend continuation. |

## Search grid

| horizon_seconds | threshold_policy | fixed_notional_inr | cost_profile | max_concurrent_positions |
| --- | --- | --- | --- | --- |
| 60 | top_25pct_abs_signal | 25000 | zerodha_base | 1 |
| 60 | top_25pct_abs_signal | 25000 | zerodha_base | 2 |
| 60 | top_25pct_abs_signal | 25000 | zerodha_base | 4 |
| 60 | top_25pct_abs_signal | 25000 | zerodha_plus_1bp_slippage | 1 |
| 60 | top_25pct_abs_signal | 25000 | zerodha_plus_1bp_slippage | 2 |
| 60 | top_25pct_abs_signal | 25000 | zerodha_plus_1bp_slippage | 4 |
| 60 | top_25pct_abs_signal | 25000 | zerodha_plus_2bp_slippage | 1 |
| 60 | top_25pct_abs_signal | 25000 | zerodha_plus_2bp_slippage | 2 |
| 60 | top_25pct_abs_signal | 25000 | zerodha_plus_2bp_slippage | 4 |
| 60 | top_25pct_abs_signal | 25000 | zerodha_2x_all_in_cost_proxy | 1 |
| 60 | top_25pct_abs_signal | 25000 | zerodha_2x_all_in_cost_proxy | 2 |
| 60 | top_25pct_abs_signal | 25000 | zerodha_2x_all_in_cost_proxy | 4 |
| 60 | top_25pct_abs_signal | 50000 | zerodha_base | 1 |
| 60 | top_25pct_abs_signal | 50000 | zerodha_base | 2 |
| 60 | top_25pct_abs_signal | 50000 | zerodha_base | 4 |
| 60 | top_25pct_abs_signal | 50000 | zerodha_plus_1bp_slippage | 1 |
| 60 | top_25pct_abs_signal | 50000 | zerodha_plus_1bp_slippage | 2 |
| 60 | top_25pct_abs_signal | 50000 | zerodha_plus_1bp_slippage | 4 |
| 60 | top_25pct_abs_signal | 50000 | zerodha_plus_2bp_slippage | 1 |
| 60 | top_25pct_abs_signal | 50000 | zerodha_plus_2bp_slippage | 2 |
| 60 | top_25pct_abs_signal | 50000 | zerodha_plus_2bp_slippage | 4 |
| 60 | top_25pct_abs_signal | 50000 | zerodha_2x_all_in_cost_proxy | 1 |
| 60 | top_25pct_abs_signal | 50000 | zerodha_2x_all_in_cost_proxy | 2 |
| 60 | top_25pct_abs_signal | 50000 | zerodha_2x_all_in_cost_proxy | 4 |
| 60 | top_25pct_abs_signal | 100000 | zerodha_base | 1 |
| 60 | top_25pct_abs_signal | 100000 | zerodha_base | 2 |
| 60 | top_25pct_abs_signal | 100000 | zerodha_base | 4 |
| 60 | top_25pct_abs_signal | 100000 | zerodha_plus_1bp_slippage | 1 |
| 60 | top_25pct_abs_signal | 100000 | zerodha_plus_1bp_slippage | 2 |
| 60 | top_25pct_abs_signal | 100000 | zerodha_plus_1bp_slippage | 4 |
| 60 | top_25pct_abs_signal | 100000 | zerodha_plus_2bp_slippage | 1 |
| 60 | top_25pct_abs_signal | 100000 | zerodha_plus_2bp_slippage | 2 |
| 60 | top_25pct_abs_signal | 100000 | zerodha_plus_2bp_slippage | 4 |
| 60 | top_25pct_abs_signal | 100000 | zerodha_2x_all_in_cost_proxy | 1 |
| 60 | top_25pct_abs_signal | 100000 | zerodha_2x_all_in_cost_proxy | 2 |
| 60 | top_25pct_abs_signal | 100000 | zerodha_2x_all_in_cost_proxy | 4 |
| 60 | top_50pct_abs_signal | 25000 | zerodha_base | 1 |
| 60 | top_50pct_abs_signal | 25000 | zerodha_base | 2 |
| 60 | top_50pct_abs_signal | 25000 | zerodha_base | 4 |
| 60 | top_50pct_abs_signal | 25000 | zerodha_plus_1bp_slippage | 1 |
| 60 | top_50pct_abs_signal | 25000 | zerodha_plus_1bp_slippage | 2 |
| 60 | top_50pct_abs_signal | 25000 | zerodha_plus_1bp_slippage | 4 |
| 60 | top_50pct_abs_signal | 25000 | zerodha_plus_2bp_slippage | 1 |
| 60 | top_50pct_abs_signal | 25000 | zerodha_plus_2bp_slippage | 2 |
| 60 | top_50pct_abs_signal | 25000 | zerodha_plus_2bp_slippage | 4 |
| 60 | top_50pct_abs_signal | 25000 | zerodha_2x_all_in_cost_proxy | 1 |
| 60 | top_50pct_abs_signal | 25000 | zerodha_2x_all_in_cost_proxy | 2 |
| 60 | top_50pct_abs_signal | 25000 | zerodha_2x_all_in_cost_proxy | 4 |
| 60 | top_50pct_abs_signal | 50000 | zerodha_base | 1 |
| 60 | top_50pct_abs_signal | 50000 | zerodha_base | 2 |
| 60 | top_50pct_abs_signal | 50000 | zerodha_base | 4 |
| 60 | top_50pct_abs_signal | 50000 | zerodha_plus_1bp_slippage | 1 |
| 60 | top_50pct_abs_signal | 50000 | zerodha_plus_1bp_slippage | 2 |
| 60 | top_50pct_abs_signal | 50000 | zerodha_plus_1bp_slippage | 4 |
| 60 | top_50pct_abs_signal | 50000 | zerodha_plus_2bp_slippage | 1 |
| 60 | top_50pct_abs_signal | 50000 | zerodha_plus_2bp_slippage | 2 |
| 60 | top_50pct_abs_signal | 50000 | zerodha_plus_2bp_slippage | 4 |
| 60 | top_50pct_abs_signal | 50000 | zerodha_2x_all_in_cost_proxy | 1 |
| 60 | top_50pct_abs_signal | 50000 | zerodha_2x_all_in_cost_proxy | 2 |
| 60 | top_50pct_abs_signal | 50000 | zerodha_2x_all_in_cost_proxy | 4 |

## Fixed-capital return contract

| contract_id | contract_value | description |
| --- | --- | --- |
| initial_capital_grid_inr | 100000;250000;500000 | Fixed starting capital scenarios; no unlimited capital. |
| per_trade_notional_grid_inr | 25000;50000;100000 | Per-symbol event allocation before capital/concurrency gates. |
| capital_allocation_rule | rank_by_abs_signal_then_allocate_until_cash_or_concurrency_exhausted | Avoid pretending every signal has independent capital. |
| portfolio_return_formula | net_pnl_inr / initial_capital_inr | Only fixed-capital net P&L divided by initial capital is portfolio return. |
| annualized_return_formula | portfolio_return * 252 / observed_trade_dates | Allowed only as sparse research diagnostic while observed_trade_dates is recorded. |
| annualized_profitability_research_threshold | >=12pct | User-requested research-lead threshold; not deployable acceptance. |
| minimum_dates_for_deployable_claim | not_satisfied | One synthetic event date cannot support deployable annual-return claim. |
| same_symbol_overlap_policy | one_position_per_symbol_event_window | Prevent stacking same-symbol event decisions. |

## Control contract

| control_id | control_status | description |
| --- | --- | --- |
| full_top_five_depth_required | required | Every allowed family must include L1-L5 or L2-L5 materiality. |
| depth_beyond_l1_required | required | At least one signal term must use levels 2-5. |
| l1_only_candidate_allowed | forbidden | L1-only event strategies are not allowed in this branch. |
| zerodha_cost_model_required | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Use the documented Zerodha equity intraday NSE charge model. |
| slippage_stress_required | required | Search must include additional 1bp/2bp and 2x cost-stress profiles. |
| post_event_target_as_feature | forbidden | target_ columns are labels/diagnostics only, not inputs. |
| portfolio_return_without_fixed_capital | forbidden | No unlimited-capital annual return. |
| paper_live_or_deployable_profitability_claim | forbidden | No paper/live or deployable claim from Phase312. |
| strategy_execution_now | forbidden | Phase311 is a precommit only. |

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
| P311_PHASE310_COMPLETE | True | 1 | 1 | hard |
| P311_PHASE310_FULL_DEPTH_FEATURES | True | 1 | 1 | hard |
| P311_FAMILY_CATALOG_NONEMPTY | True | 8 | >=8 | hard |
| P311_SEARCH_GRID_NONEMPTY | True | 432 | >0 | hard |
| P311_FIXED_CAPITAL_CONTRACT_PRESENT | True | 8 | >=8 | hard |
| P311_ZERODHA_COST_MODEL_REFERENCED | True | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | present | hard |
| P311_DEPTH_BEYOND_L1_REQUIRED | True | present | present | hard |
| P311_NO_EXECUTION_OPENED | True | strategy_execution_now=0 | 0 | hard |
| P311_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

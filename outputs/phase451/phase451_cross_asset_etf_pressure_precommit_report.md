# Phase451 Cross-Asset ETF Pressure Source Precommit

Phase451 freezes a low-turnover external/cross-asset source after Phase450 closed the high-turnover depth-curvature route.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase451_cross_asset_precommit_complete | 1 | Phase451 precommit completed |
| phase451_thesis_id | P451_CROSS_ASSET_ETF_PRESSURE_PRECOMMIT | Frozen thesis/source precommit |
| phase451_selected_source_id | cross_asset_etf_depth_pressure_lead_lag | Selected source |
| phase451_execution_results_generated | 0 | Precommit only |
| phase451_strategy_promotion_allowed | 0 | No promotion |
| phase451_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase451_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase451_execution_allowed_next | 1 | Whether Phase452 may execute |
| phase451_hard_gate_pass_rows | 11 | Passed hard gates |
| phase451_hard_gate_rows | 11 | Hard gates |
| phase451_next_best_action | run_phase452_cross_asset_etf_pressure_no_paper_live | Recommended next action |

## Prior Boundary

| phase | route | verdict_or_status | reason_for_not_continuing |
| --- | --- | --- | --- |
| P450 | depth_curvature_dynamic_route | P450_DEPTH_CURVATURE_DYNAMIC_ROUTE_REJECTED_COST_AND_CONTROLS | closed; next action requires new low-turnover external or cross-asset source edge |
| P447 | catalyst_continuation_stability | rejected_by_frozen_holdout | do not tune/reuse catalyst continuation as source |
| P409 | retail_two_sided_market_maker_cancel_latency | falsified | do not reopen attached cancel-included charter without new external execution source |
| P435 | supervised_full_depth_event_ranker | rejected | do not retry ranker without materially different label/source |

## Source Scorecard

| source_id | material_new_axis | uses_l2_l5_core | low_turnover_or_external | can_execute_next | why_selected |
| --- | --- | --- | --- | --- | --- |
| cross_asset_etf_depth_pressure_lead_lag | cross_asset_external_proxy_plus_full_depth_confirmation | 1 | 1 | 1 | selected: lower turnover and external/cross-asset information source after Phase450 |
| another_depth_curvature_threshold | none | 1 | 0 | 0 | rejected: Phase450 closed same-source rescue |
| another_catalyst_continuation | none | 1 | 0 | 0 | rejected: Phase447 holdout failed |
| another_market_maker_cancel_race | none | 1 | 0 | 0 | rejected: Phase407-409 already falsified attached charter |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| dense_root_exists | 1 | Raw dense L1-L5 lake root exists. |
| dense_parquet_file_count | 384 | Current dense Parquet file count. |
| available_symbol_count | 32 | Symbols available under dense root. |
| available_month_count | 12 | Trade months available under dense root. |
| etf_proxies | NIFTYBEES;BANKBEES;ITBEES | Cross-asset source instruments. |
| target_symbols | AXISBANK;HDFCBANK;ICICIBANK;INFY;HCLTECH;TCS;RELIANCE | Liquid target symbols. |
| months | 2026-01;2026-02;2026-03;2026-04;2026-05;2026-06 | Frozen execution months. |
| missing_required_symbols |  | Must be empty. |
| missing_required_months |  | Must be empty. |
| cost_multiplier | 2 | Cost200 scoring. |
| initial_capital_inr | 1e+06 | Fixed capital denominator. |
| order_notional_inr | 100000 | Fixed order notional. |

## Frozen Phase452 Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P451_CROSS_ASSET_ETF_PRESSURE_PRECOMMIT | Phase451 selected source precommit. |
| selected_source | cross_asset_etf_depth_pressure_lead_lag | Materially new low-turnover cross-asset source. |
| market_hypothesis | etf_proxy_l2_l5_depth_pressure_and_return_leads_constituent_short_horizon_move | ETF/order-book pressure may reveal basket demand before all constituents adjust. |
| source_instruments | NIFTYBEES;BANKBEES;ITBEES | ETF/index-proxy source instruments. |
| target_symbols | AXISBANK;HDFCBANK;ICICIBANK;INFY;HCLTECH;TCS;RELIANCE | Frozen target basket. |
| months | 2026-01;2026-02;2026-03;2026-04;2026-05;2026-06 | Frozen bounded execution months before results. |
| feature_family | etf_return_bps_plus_etf_l2_l5_imbalance_pressure_minus_target_l1_l2_l5_confirmation | Primary source is cross-asset ETF pressure plus full-depth target confirmation. |
| entry_logic | one_low_turnover_taker_event_per_target_date_when_proxy_pressure_agrees_with_target_depth | Low turnover before costs. |
| max_events_per_target_date | 1 | No dense churning. |
| horizon_ticks | 240 | Fixed exit horizon. |
| stop_bps | 18.0 | Fixed stop. |
| take_profit_bps | 30.0 | Fixed take profit. |
| sample_stride | 4096 | Deterministic bounded scan stride. |
| controls_required | source_time_shift;side_flip;target_only_l1_l5_without_etf_proxy;etf_l1_only_ablation | Controls required in Phase452. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha equity intraday NSE formula. |
| capital_policy | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | Annualized denominator is fixed capital. |
| acceptance_floor | round_trips_ge_30;dates_ge_5;symbols_ge_3;positive_date_fraction_ge_0p60;annualized_ge_12_cost200;controls_not_dominant | User profitability bar with breadth. |
| forbidden | same_depth_curvature_rescue;catalyst_rescue;market_maker_rescue;supervised_ranker_retry;promotion;paper_live;deployable_profitability_claim | Closed boundaries. |
| execution_results_generated_now | 0 | Precommit only. |
| contract_hash | 42311b5acbe45bdda6d441781603f6db49a815045089a2b9fc40a47991acca8f | Hash of frozen contract rows above. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P451_PHASE450_AVAILABLE | True | 1 | 1 | hard |
| P451_NEXT_ACTION_MATCHED | True | precommit_new_low_turnover_external_or_cross_asset_source_edge | external_or_cross_asset | hard |
| P451_SELECTED_SOURCE_PRESENT | True | 1 | 1 | hard |
| P451_SELECTED_SOURCE_USES_L2_L5 | True | 1 | 1 | hard |
| P451_SELECTED_SOURCE_LOW_TURNOVER_EXTERNAL | True | 1 | 1 | hard |
| P451_DENSE_ROOT_PRESENT | True | exists=1;files=384 | exists_and_files | hard |
| P451_REQUIRED_SYMBOLS_AVAILABLE | True |  | empty | hard |
| P451_REQUIRED_MONTHS_AVAILABLE | True |  | empty | hard |
| P451_COST200_FIXED_CAPITAL | True | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | cost200_fixed_capital | hard |
| P451_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P451_BOUNDARIES_CLOSED | True | same_depth_curvature_rescue;catalyst_rescue;market_maker_rescue;supervised_ranker_retry;promotion;paper_live;deployable_profitability_claim | closed | hard |

Boundary: Phase452 may execute only this cross-asset ETF pressure source. It may not rescue Phase449, catalyst continuation, market making or supervised-ranker routes.

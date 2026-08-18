# Phase457 Delayed Intraday Cross-Asset Displacement Precommit

Phase457 freezes a materially new timing/label source after Phase456 closed the first-window cross-asset form.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase457_delayed_cross_asset_precommit_complete | 1 | Phase457 precommit completed |
| phase457_thesis_id | P457_DELAYED_INTRADAY_CROSS_ASSET_DISPLACEMENT_PRECOMMIT | Delayed timing-source thesis |
| phase457_selected_source_id | delayed_intraday_cross_asset_etf_displacement | Selected source |
| phase457_execution_results_generated | 0 | Precommit only |
| phase457_strategy_promotion_allowed | 0 | No promotion |
| phase457_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase457_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase457_execution_allowed_next | 1 | Whether Phase458 may execute |
| phase457_hard_gate_pass_rows | 10 | Passed hard gates |
| phase457_hard_gate_rows | 10 | Hard gates |
| phase457_next_best_action | run_phase458_delayed_intraday_cross_asset_displacement_no_paper_live | Recommended next action |

## Prior Boundary

| phase | route | verdict_or_status | boundary |
| --- | --- | --- | --- |
| P456 | first_window_cross_asset_etf_pressure | P456_FIRST_WINDOW_CROSS_ASSET_ETF_PRESSURE_REJECTED_ZERO_GROSS_EDGE | closed: first-window form produced zero gross edge and failed controls |
| P455 | contiguous_first_window_execution | 0 | same-form rescue not allowed |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| dense_root_exists | 1 | Dense root exists. |
| selected_file_rows | 30 | Frozen selected file rows. |
| selected_files_present | 30 | Selected files present. |
| months | 2026-01;2026-02;2026-03 | Frozen months. |
| source_instruments | NIFTYBEES;BANKBEES;ITBEES | ETF/index proxies. |
| target_symbols | AXISBANK;HDFCBANK;ICICIBANK;INFY;HCLTECH;TCS;RELIANCE | Target symbols. |
| window_start_row | 5000 | Delayed intraday row offset; not first-window. |
| window_rows_per_symbol_date | 271 | Rows needed from each delayed window. |
| entry_index | 20 | Entry row within delayed window. |
| horizon_ticks | 240 | Fixed horizon. |
| guard_ticks | 10 | Guard rows. |

## Selected Files

| trade_month | symbol | path | exists |
| --- | --- | --- | --- |
| 2026-01 | NIFTYBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=NIFTYBEES\part-00000.parquet | 1 |
| 2026-01 | BANKBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BANKBEES\part-00000.parquet | 1 |
| 2026-01 | ITBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ITBEES\part-00000.parquet | 1 |
| 2026-01 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=AXISBANK\part-00000.parquet | 1 |
| 2026-01 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | 1 |
| 2026-01 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ICICIBANK\part-00000.parquet | 1 |
| 2026-01 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=INFY\part-00000.parquet | 1 |
| 2026-01 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=HCLTECH\part-00000.parquet | 1 |
| 2026-01 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=TCS\part-00000.parquet | 1 |
| 2026-01 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=RELIANCE\part-00000.parquet | 1 |
| 2026-02 | NIFTYBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=NIFTYBEES\part-00000.parquet | 1 |
| 2026-02 | BANKBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=BANKBEES\part-00000.parquet | 1 |
| 2026-02 | ITBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ITBEES\part-00000.parquet | 1 |
| 2026-02 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=AXISBANK\part-00000.parquet | 1 |
| 2026-02 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=HDFCBANK\part-00000.parquet | 1 |
| 2026-02 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ICICIBANK\part-00000.parquet | 1 |
| 2026-02 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=INFY\part-00000.parquet | 1 |
| 2026-02 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=HCLTECH\part-00000.parquet | 1 |
| 2026-02 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=TCS\part-00000.parquet | 1 |
| 2026-02 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=RELIANCE\part-00000.parquet | 1 |
| 2026-03 | NIFTYBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=NIFTYBEES\part-00000.parquet | 1 |
| 2026-03 | BANKBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=BANKBEES\part-00000.parquet | 1 |
| 2026-03 | ITBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ITBEES\part-00000.parquet | 1 |
| 2026-03 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=AXISBANK\part-00000.parquet | 1 |
| 2026-03 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=HDFCBANK\part-00000.parquet | 1 |
| 2026-03 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ICICIBANK\part-00000.parquet | 1 |
| 2026-03 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=INFY\part-00000.parquet | 1 |
| 2026-03 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=HCLTECH\part-00000.parquet | 1 |
| 2026-03 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=TCS\part-00000.parquet | 1 |
| 2026-03 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=RELIANCE\part-00000.parquet | 1 |

## Frozen Phase458 Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P457_DELAYED_INTRADAY_CROSS_ASSET_DISPLACEMENT_PRECOMMIT | Phase457 delayed timing-source precommit. |
| selected_source | delayed_intraday_cross_asset_etf_displacement | Materially new timing/label source after Phase456. |
| material_difference | delayed_intraday_window_not_first_window_cross_asset_pressure | Changes timing/label source, not thresholds or side-rule tuning. |
| source_instruments | NIFTYBEES;BANKBEES;ITBEES | ETF/index-proxy source instruments. |
| target_symbols | AXISBANK;HDFCBANK;ICICIBANK;INFY;HCLTECH;TCS;RELIANCE | Frozen target basket. |
| months | 2026-01;2026-02;2026-03 | Frozen bounded execution months. |
| window_start_row | 5000 | Start delayed contiguous window at this per-symbol/date row. |
| window_rows_per_symbol_date | 271 | Keep contiguous rows for entry plus horizon. |
| entry_index | 20 | Entry index within window. |
| horizon_ticks | 240 | Fixed exit horizon. |
| guard_ticks | 10 | Guard ticks. |
| max_events_per_target_date | 1 | Low-turnover cap. |
| side_rule | long_when_delayed_etf_proxy_pressure_and_target_l2_l5_pressure_agree_short_when_opposite | Frozen side rule. |
| controls_required | source_time_shift;side_flip;target_only_l1_l5;etf_l1_only_ablation | Required controls. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha equity intraday NSE formula. |
| cost_multiplier | 2.0 | Cost200. |
| capital_policy | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | Fixed capital and notional. |
| acceptance_floor | round_trips_ge_30;dates_ge_5;symbols_ge_3;positive_date_fraction_ge_0p60;annualized_ge_12_cost200;controls_not_dominant | User profitability bar with breadth. |
| forbidden | first_window_cross_asset_rescue;threshold_relaxation;side_rule_tuning;catalyst_rescue;market_maker_rescue;promotion;paper_live;deployable_profitability_claim | Closed boundaries. |
| execution_results_generated_now | 0 | Precommit only. |
| contract_hash | 9570a1ddbd0aeb56798f2e49dd024049708123494182bdd85e8c10706fcfd0cd | Hash of frozen contract rows above. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P457_PHASE456_AVAILABLE | True | 1 | 1 | hard |
| P457_NEXT_ACTION_MATCHED | True | precommit_material_new_timing_or_label_source_not_first_window_cross_asset_pressure | material_new_timing | hard |
| P457_NOT_FIRST_WINDOW | True | 5000 | >0 | hard |
| P457_CONTIGUOUS_WINDOW_FROZEN | True | 271 | >=261 | hard |
| P457_SELECTED_FILES_PRESENT | True | 30 | 30 | hard |
| P457_LOW_TURNOVER_CAP_RETAINED | True | 1 | 1 | hard |
| P457_COST200_FIXED_CAPITAL | True | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | cost200_fixed_capital | hard |
| P457_CONTROLS_PRECOMMITTED | True | source_time_shift;side_flip;target_only_l1_l5;etf_l1_only_ablation | controls | hard |
| P457_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P457_BOUNDARIES_CLOSED | True | first_window_cross_asset_rescue;threshold_relaxation;side_rule_tuning;catalyst_rescue;market_maker_rescue;promotion;paper_live;deployable_profitability_claim | closed | hard |

Boundary: commit this precommit before Phase458 generates delayed-window trades or P&L.

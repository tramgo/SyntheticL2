# Phase454 Contiguous Tick-Window Cross-Asset ETF Pressure Precommit

Phase454 repairs only the Phase452 data-access mismatch by freezing contiguous raw tick windows per symbol/date. It does not change the Phase451 signal source or side rule.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase454_contiguous_precommit_complete | 1 | Phase454 precommit completed |
| phase454_thesis_id | P454_CONTIGUOUS_TICK_WINDOW_CROSS_ASSET_ETF_PRESSURE_PRECOMMIT | Repaired execution-access thesis |
| phase454_window_rows_per_symbol_date | 271 | Contiguous rows per symbol/date |
| phase454_execution_results_generated | 0 | Precommit only |
| phase454_strategy_promotion_allowed | 0 | No promotion |
| phase454_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase454_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase454_execution_allowed_next | 1 | Whether Phase455 may execute |
| phase454_hard_gate_pass_rows | 11 | Passed hard gates |
| phase454_hard_gate_rows | 11 | Hard gates |
| phase454_next_best_action | run_phase455_contiguous_cross_asset_etf_pressure_no_paper_live | Recommended next action |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| phase451_contract_available | 1 | Prior source/target/month contract available. |
| dense_root_exists | 1 | Dense root exists. |
| selected_file_rows | 60 | Frozen file rows. |
| selected_files_present | 60 | Selected files present. |
| months | 2026-01;2026-02;2026-03;2026-04;2026-05;2026-06 | Frozen months inherited from Phase451. |
| symbols | NIFTYBEES;BANKBEES;ITBEES;AXISBANK;HDFCBANK;ICICIBANK;INFY;HCLTECH;TCS;RELIANCE | Frozen source plus target symbols inherited from Phase451. |
| window_rows_per_symbol_date | 271 | Contiguous rows required per symbol/date. |
| entry_index | 20 | Frozen entry index. |
| horizon_ticks | 240 | Frozen horizon. |
| guard_ticks | 10 | Frozen guard. |

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
| 2026-04 | NIFTYBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=NIFTYBEES\part-00000.parquet | 1 |
| 2026-04 | BANKBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=BANKBEES\part-00000.parquet | 1 |
| 2026-04 | ITBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=ITBEES\part-00000.parquet | 1 |
| 2026-04 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=AXISBANK\part-00000.parquet | 1 |
| 2026-04 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=HDFCBANK\part-00000.parquet | 1 |
| 2026-04 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=ICICIBANK\part-00000.parquet | 1 |
| 2026-04 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=INFY\part-00000.parquet | 1 |
| 2026-04 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=HCLTECH\part-00000.parquet | 1 |
| 2026-04 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=TCS\part-00000.parquet | 1 |
| 2026-04 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=RELIANCE\part-00000.parquet | 1 |
| 2026-05 | NIFTYBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=NIFTYBEES\part-00000.parquet | 1 |
| 2026-05 | BANKBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=BANKBEES\part-00000.parquet | 1 |
| 2026-05 | ITBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=ITBEES\part-00000.parquet | 1 |
| 2026-05 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=AXISBANK\part-00000.parquet | 1 |
| 2026-05 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=HDFCBANK\part-00000.parquet | 1 |
| 2026-05 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=ICICIBANK\part-00000.parquet | 1 |
| 2026-05 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=INFY\part-00000.parquet | 1 |
| 2026-05 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=HCLTECH\part-00000.parquet | 1 |
| 2026-05 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=TCS\part-00000.parquet | 1 |
| 2026-05 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=RELIANCE\part-00000.parquet | 1 |
| 2026-06 | NIFTYBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=NIFTYBEES\part-00000.parquet | 1 |
| 2026-06 | BANKBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=BANKBEES\part-00000.parquet | 1 |
| 2026-06 | ITBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=ITBEES\part-00000.parquet | 1 |
| 2026-06 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=AXISBANK\part-00000.parquet | 1 |
| 2026-06 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=HDFCBANK\part-00000.parquet | 1 |
| 2026-06 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=ICICIBANK\part-00000.parquet | 1 |
| 2026-06 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=INFY\part-00000.parquet | 1 |
| 2026-06 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=HCLTECH\part-00000.parquet | 1 |
| 2026-06 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=TCS\part-00000.parquet | 1 |
| 2026-06 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=RELIANCE\part-00000.parquet | 1 |

## Frozen Phase455 Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P454_CONTIGUOUS_TICK_WINDOW_CROSS_ASSET_ETF_PRESSURE_PRECOMMIT | Phase454 repaired access precommit. |
| repair_type | contiguous_raw_tick_window_access | Repairs Phase452 sparse-stride access failure. |
| source_instruments | NIFTYBEES;BANKBEES;ITBEES | Keep Phase451 ETF proxies. |
| target_symbols | AXISBANK;HDFCBANK;ICICIBANK;INFY;HCLTECH;TCS;RELIANCE | Keep Phase451 targets. |
| months | 2026-01;2026-02;2026-03;2026-04;2026-05;2026-06 | Keep Phase451 months. |
| entry_index | 20 | Keep Phase452 event index. |
| horizon_ticks | 240 | Keep Phase451 horizon. |
| guard_ticks | 10 | Guard rows beyond horizon. |
| window_rows_per_symbol_date | 271 | Minimum contiguous rows per symbol/date. |
| max_events_per_target_date | 1 | Keep low-turnover cap. |
| side_rule | unchanged_from_phase451_cross_asset_etf_pressure | No signal/side rescue after Phase452. |
| controls_required | source_time_shift;side_flip;target_only_l1_l5_without_etf_proxy;etf_l1_only_ablation | Keep Phase451 controls. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha cost model. |
| cost_multiplier | 2.0 | Cost200. |
| capital_policy | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | Fixed capital and notional. |
| acceptance_floor | round_trips_ge_30;dates_ge_5;symbols_ge_3;positive_date_fraction_ge_0p60;annualized_ge_12_cost200;controls_not_dominant | Keep Phase451 acceptance floor. |
| forbidden | threshold_relaxation;side_rule_change;source_universe_change;catalyst_rescue;market_maker_rescue;promotion;paper_live;deployable_profitability_claim | Closed boundaries. |
| execution_results_generated_now | 0 | Precommit only. |
| contract_hash | f724dbead002e8c07828a132fbf55beaa87e6180e850cf74503393a3bc0c070d | Hash of frozen repair contract rows above. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P454_PHASE453_AVAILABLE | True | 1 | 1 | hard |
| P454_REPAIR_NEXT_ACTION_MATCHED | True | precommit_phase454_contiguous_tick_window_cross_asset_etf_pressure_no_results | contiguous_repair | hard |
| P454_SOURCE_NOT_CLOSED | True | 0 | 0 | hard |
| P454_STRIDE_CONTRACT_CLOSED | True | 1 | 1 | hard |
| P454_CONTIGUOUS_WINDOW_FROZEN | True | 271 | >=261 | hard |
| P454_SELECTED_FILES_PRESENT | True | 60 | 60 | hard |
| P454_NO_SIGNAL_OR_SIDE_CHANGE | True | unchanged_from_phase451_cross_asset_etf_pressure | unchanged | hard |
| P454_LOW_TURNOVER_CAP_RETAINED | True | 1 | 1 | hard |
| P454_COST200_FIXED_CAPITAL | True | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | cost200_fixed_capital | hard |
| P454_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P454_BOUNDARIES_CLOSED | True | threshold_relaxation;side_rule_change;source_universe_change;catalyst_rescue;market_maker_rescue;promotion;paper_live;deployable_profitability_claim | closed | hard |

Boundary: commit this precommit before Phase455 generates any trades or P&L.

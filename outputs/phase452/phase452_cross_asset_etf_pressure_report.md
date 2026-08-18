# Phase452 Cross-Asset ETF Pressure Execution

Phase452 executes the Phase451 frozen cross-asset ETF pressure source with a low-turnover one-event-per-target-date cap.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase452_cross_asset_execution_complete | 1 | Phase452 execution completed |
| phase452_thesis_id | P452_CROSS_ASSET_ETF_PRESSURE_EXECUTION | Execution thesis |
| phase452_best_scenario_id | P452_cross_asset_etf_pressure_primary | Primary scenario |
| phase452_best_completed_round_trips | 0 | Primary completed round trips |
| phase452_best_trade_dates | 0 | Primary dates |
| phase452_best_symbols | 0 | Primary symbols |
| phase452_best_positive_date_fraction | 0 | Primary positive-date fraction |
| phase452_best_gross_pnl_inr | 0 | Primary gross P&L |
| phase452_best_cost200_inr | 0 | Primary Zerodha cost200 |
| phase452_best_net_pnl_inr | 0 | Primary net P&L |
| phase452_best_annualized_return_pct | 0 | Fixed-capital annualized return |
| phase452_acceptance_survivor | 0 | Accepted only if every hard gate passes |
| phase452_strategy_promotion_allowed | 0 | No promotion |
| phase452_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase452_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase452_hard_gate_pass_rows | 7 | Passed hard gates |
| phase452_hard_gate_rows | 16 | Hard gates |
| phase452_next_best_action | interpret_phase452_cross_asset_etf_pressure_no_paper_live | Recommended next action |

## Scenario Summary

| scenario_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | gross_pnl_inr | cost200_inr | net_pnl_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P452_cross_asset_etf_pressure_primary | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P452_cross_asset_etf_pressure_source_time_shift | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P452_cross_asset_etf_pressure_side_flip | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P452_cross_asset_target_only_l1_l5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P452_cross_asset_etf_l1_only | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

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

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P452_PHASE451_PRECOMMIT_USED | True | 1 | 1 | hard |
| P452_REQUIRED_FILES_PRESENT | True | 60 | 60 | hard |
| P452_LOW_TURNOVER_CAP_APPLIED | True | max_one_event_per_target_date | applied | hard |
| P452_CROSS_ASSET_SOURCE_USED | True | NIFTYBEES;BANKBEES;ITBEES | etf_proxies | hard |
| P452_FULL_DEPTH_L2_L5_PRIMARY | True | ETF and target l2_l5 pressure used | levels_2_to_5 | hard |
| P452_COMPLETED_ROUND_TRIPS_GE_30 | False | 0 | >=30 | hard |
| P452_DATE_BREADTH_GE_5 | False | 0 | >=5 | hard |
| P452_SYMBOL_BREADTH_GE_3 | False | 0 | >=3 | hard |
| P452_POSITIVE_DATE_FRACTION_GE_0_60 | False | 0 | >=0.60 | hard |
| P452_ANNUALIZED_GE_12_COST200 | False | 0 | >=12.0 | hard |
| P452_TIME_SHIFT_NOT_DOMINANT | False | primary=0.0;shift=0.0 | primary_gt_shift | hard |
| P452_SIDE_FLIP_NOT_DOMINANT | False | primary=0.0;side_flip=0.0 | primary_gt_side_flip | hard |
| P452_TARGET_ONLY_NOT_DOMINANT | False | primary=0.0;target_only=0.0 | primary_gt_target_only | hard |
| P452_ETF_L1_ONLY_NOT_DOMINANT | False | primary=0.0;etf_l1=0.0 | primary_gt_etf_l1 | hard |
| P452_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P452_NO_PROMOTION_PAPER_LIVE | True | promotion=0;paper_live=0;claim=0 | all_zero | hard |

Boundary: no strategy promotion, paper/live acceptance or deployable profitability claim is emitted by Phase452.

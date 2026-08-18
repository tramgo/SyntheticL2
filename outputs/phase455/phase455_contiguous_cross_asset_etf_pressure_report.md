# Phase455 Contiguous Cross-Asset ETF Pressure Execution

Phase455 executes the repaired Phase454 contiguous raw tick-window contract for the Phase451 cross-asset ETF pressure source.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase455_contiguous_cross_asset_execution_complete | 1 | Phase455 execution completed |
| phase455_thesis_id | P455_CONTIGUOUS_CROSS_ASSET_ETF_PRESSURE_EXECUTION | Execution thesis |
| phase455_best_scenario_id | P455_contiguous_cross_asset_etf_pressure_primary | Primary scenario |
| phase455_best_completed_round_trips | 284 | Primary completed round trips |
| phase455_best_trade_dates | 129 | Primary dates |
| phase455_best_symbols | 3 | Primary symbols |
| phase455_best_positive_date_fraction | 0 | Primary positive-date fraction |
| phase455_best_gross_pnl_inr | 0 | Primary gross P&L |
| phase455_best_cost200_inr | 46912.6 | Primary Zerodha cost200 |
| phase455_best_net_pnl_inr | -46912.6 | Primary net P&L |
| phase455_best_annualized_return_pct | -9.16432 | Fixed-capital annualized return |
| phase455_acceptance_survivor | 0 | Accepted only if every hard gate passes |
| phase455_strategy_promotion_allowed | 0 | No promotion |
| phase455_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase455_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase455_hard_gate_pass_rows | 12 | Passed hard gates |
| phase455_hard_gate_rows | 17 | Hard gates |
| phase455_next_best_action | interpret_phase455_contiguous_cross_asset_etf_pressure_no_paper_live | Recommended next action |

## Scenario Summary

| scenario_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | gross_pnl_inr | cost200_inr | net_pnl_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P455_contiguous_cross_asset_etf_pressure_primary | 284 | 129 | 3 | 0 | 0 | 46912.6 | -46912.6 | -9.16432 | 0 |
| P455_contiguous_cross_asset_etf_pressure_source_time_shift | 281 | 128 | 3 | 0 | 0 | 46416.9 | -46416.9 | -9.13832 | 0 |
| P455_contiguous_cross_asset_etf_pressure_side_flip | 284 | 129 | 3 | 0 | 0 | 46912.6 | -46912.6 | -9.16432 | 0 |
| P455_contiguous_cross_asset_target_only_l1_l5 | 900 | 129 | 7 | 0 | 0 | 148647 | -148647 | -29.0381 | 0 |
| P455_contiguous_cross_asset_etf_l1_only | 284 | 129 | 3 | 0 | 0 | 46912.6 | -46912.6 | -9.16432 | 0 |

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
| P455_PHASE454_PRECOMMIT_USED | True | 1 | 1 | hard |
| P455_REQUIRED_FILES_PRESENT | True | 60 | 60 | hard |
| P455_CONTIGUOUS_METRICS_PRESENT | True | 1290 | >0 | hard |
| P455_LOW_TURNOVER_CAP_APPLIED | True | max_one_event_per_target_date | applied | hard |
| P455_CROSS_ASSET_SOURCE_USED | True | NIFTYBEES;BANKBEES;ITBEES | etf_proxies | hard |
| P455_FULL_DEPTH_L2_L5_PRIMARY | True | ETF and target L2-L5 pressure used | levels_2_to_5 | hard |
| P455_COMPLETED_ROUND_TRIPS_GE_30 | True | 284 | >=30 | hard |
| P455_DATE_BREADTH_GE_5 | True | 129 | >=5 | hard |
| P455_SYMBOL_BREADTH_GE_3 | True | 3 | >=3 | hard |
| P455_POSITIVE_DATE_FRACTION_GE_0_60 | False | 0 | >=0.60 | hard |
| P455_ANNUALIZED_GE_12_COST200 | False | -9.16432 | >=12.0 | hard |
| P455_TIME_SHIFT_NOT_DOMINANT | False | primary=-46912.583123133605;shift=-46416.8572100976 | primary_gt_shift | hard |
| P455_SIDE_FLIP_NOT_DOMINANT | False | primary=-46912.583123133605;side_flip=-46912.583123133605 | primary_gt_side_flip | hard |
| P455_TARGET_ONLY_NOT_DOMINANT | True | primary=-46912.583123133605;target_only=-148647.3566089416 | primary_gt_target_only | hard |
| P455_ETF_L1_ONLY_NOT_DOMINANT | False | primary=-46912.583123133605;etf_l1=-46912.583123133605 | primary_gt_etf_l1 | hard |
| P455_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P455_NO_PROMOTION_PAPER_LIVE | True | promotion=0;paper_live=0;claim=0 | all_zero | hard |

Boundary: no strategy promotion, paper/live acceptance or deployable profitability claim is emitted by Phase455.

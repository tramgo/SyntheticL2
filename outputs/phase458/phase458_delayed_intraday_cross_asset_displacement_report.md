# Phase458 Delayed Intraday Cross-Asset Displacement Execution

Phase458 executes the Phase457 delayed intraday timing-source contract using contiguous raw L1-L5 windows starting at row 5000 per symbol/date.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase458_delayed_cross_asset_execution_complete | 1 | Phase458 execution completed |
| phase458_thesis_id | P458_DELAYED_INTRADAY_CROSS_ASSET_DISPLACEMENT_EXECUTION | Execution thesis |
| phase458_best_scenario_id | P458_delayed_cross_asset_displacement_primary | Primary scenario |
| phase458_best_completed_round_trips | 146 | Primary completed round trips |
| phase458_best_trade_dates | 64 | Primary dates |
| phase458_best_symbols | 3 | Primary symbols |
| phase458_best_positive_date_fraction | 0 | Primary positive-date fraction |
| phase458_best_gross_pnl_inr | 0 | Primary gross P&L |
| phase458_best_cost200_inr | 24116.2 | Primary Zerodha cost200 |
| phase458_best_net_pnl_inr | -24116.2 | Primary net P&L |
| phase458_best_annualized_return_pct | -9.49575 | Fixed-capital annualized return |
| phase458_acceptance_survivor | 0 | Accepted only if every hard gate passes |
| phase458_strategy_promotion_allowed | 0 | No promotion |
| phase458_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase458_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase458_hard_gate_pass_rows | 13 | Passed hard gates |
| phase458_hard_gate_rows | 18 | Hard gates |
| phase458_next_best_action | interpret_phase458_delayed_intraday_cross_asset_displacement_no_paper_live | Recommended next action |

## Scenario Summary

| scenario_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | gross_pnl_inr | cost200_inr | net_pnl_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P458_delayed_cross_asset_displacement_primary | 146 | 64 | 3 | 0 | 0 | 24116.2 | -24116.2 | -9.49575 | 0 |
| P458_delayed_cross_asset_displacement_source_time_shift | 144 | 63 | 3 | 0 | 0 | 23785.8 | -23785.8 | -9.51432 | 0 |
| P458_delayed_cross_asset_displacement_side_flip | 146 | 64 | 3 | 0 | 0 | 24116.2 | -24116.2 | -9.49575 | 0 |
| P458_delayed_cross_asset_target_only_l1_l5 | 446 | 64 | 7 | 0 | 0 | 73665.4 | -73665.4 | -29.0057 | 0 |
| P458_delayed_cross_asset_etf_l1_only | 146 | 64 | 3 | 0 | 0 | 24116.2 | -24116.2 | -9.49575 | 0 |

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

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P458_PHASE457_PRECOMMIT_USED | True | 1 | 1 | hard |
| P458_REQUIRED_FILES_PRESENT | True | 30 | 30 | hard |
| P458_DELAYED_METRICS_PRESENT | True | 640 | >0 | hard |
| P458_NOT_FIRST_WINDOW | True | window_start_row=5000 | not_first_window | hard |
| P458_LOW_TURNOVER_CAP_APPLIED | True | max_one_event_per_target_date | applied | hard |
| P458_CROSS_ASSET_SOURCE_USED | True | NIFTYBEES;BANKBEES;ITBEES | etf_proxies | hard |
| P458_FULL_DEPTH_L2_L5_PRIMARY | True | ETF and target L2-L5 pressure used | levels_2_to_5 | hard |
| P458_COMPLETED_ROUND_TRIPS_GE_30 | True | 146 | >=30 | hard |
| P458_DATE_BREADTH_GE_5 | True | 64 | >=5 | hard |
| P458_SYMBOL_BREADTH_GE_3 | True | 3 | >=3 | hard |
| P458_POSITIVE_DATE_FRACTION_GE_0_60 | False | 0 | >=0.60 | hard |
| P458_ANNUALIZED_GE_12_COST200 | False | -9.49575 | >=12.0 | hard |
| P458_TIME_SHIFT_NOT_DOMINANT | False | primary=-24116.1968623696;shift=-23785.8080896416 | primary_gt_shift | hard |
| P458_SIDE_FLIP_NOT_DOMINANT | False | primary=-24116.1968623696;side_flip=-24116.1968623696 | primary_gt_side_flip | hard |
| P458_TARGET_ONLY_NOT_DOMINANT | True | primary=-24116.1968623696;target_only=-73665.3896771728 | primary_gt_target_only | hard |
| P458_ETF_L1_ONLY_NOT_DOMINANT | False | primary=-24116.1968623696;etf_l1=-24116.1968623696 | primary_gt_etf_l1 | hard |
| P458_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P458_NO_PROMOTION_PAPER_LIVE | True | promotion=0;paper_live=0;claim=0 | all_zero | hard |

Boundary: no strategy promotion, paper/live acceptance or deployable profitability claim is emitted by Phase458.

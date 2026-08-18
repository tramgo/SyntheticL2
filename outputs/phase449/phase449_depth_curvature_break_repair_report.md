# Phase449 Depth-Curvature Break/Repair Execution

Phase449 executes the Phase448 frozen depth-curvature source on deterministic strided raw dense L1-L5 Parquet shards.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase449_depth_curvature_execution_complete | 1 | Phase449 execution completed |
| phase449_thesis_id | P449_DEPTH_CURVATURE_BREAK_REPAIR_EXECUTION | Execution thesis |
| phase449_best_scenario_id | P449_depth_curvature_repair_primary | Primary scenario |
| phase449_best_completed_round_trips | 1512 | Primary completed round trips |
| phase449_best_trade_dates | 252 | Primary dates |
| phase449_best_symbols | 3 | Primary symbols |
| phase449_best_positive_date_fraction | 0.166667 | Primary positive-date fraction |
| phase449_best_gross_pnl_inr | 8437.8 | Primary gross P&L |
| phase449_best_cost200_inr | 247300 | Primary Zerodha cost200 |
| phase449_best_net_pnl_inr | -238862 | Primary net P&L |
| phase449_best_annualized_return_pct | -23.8862 | Fixed-capital annualized return |
| phase449_acceptance_survivor | 0 | Accepted only if every hard gate passes |
| phase449_strategy_promotion_allowed | 0 | No promotion |
| phase449_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase449_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase449_hard_gate_pass_rows | 9 | Passed hard gates |
| phase449_hard_gate_rows | 14 | Hard gates |
| phase449_next_best_action | interpret_phase449_depth_curvature_break_repair_no_paper_live | Recommended next action |

## Scenario Summary

| scenario_id | completed_round_trips | trade_dates | symbols | positive_date_fraction | gross_pnl_inr | cost200_inr | net_pnl_inr | annualized_return_pct | acceptance_survivor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P449_depth_curvature_repair_primary | 1512 | 252 | 3 | 0.166667 | 8437.8 | 247300 | -238862 | -23.8862 | 0 |
| P449_depth_curvature_repair_l1_only_ablation | 1481 | 252 | 3 | 0.206349 | 23725.3 | 242323 | -218598 | -21.8598 | 0 |
| P449_depth_curvature_repair_side_flip_control | 1512 | 252 | 3 | 0.142857 | -35617.8 | 247306 | -282924 | -28.2924 | 0 |
| P449_depth_curvature_static_snapshot_control | 1512 | 252 | 3 | 0.218254 | 51085.4 | 247292 | -196207 | -19.6207 | 0 |
| P449_depth_curvature_time_shift_control | 1512 | 252 | 3 | 0.190476 | 13217.9 | 247280 | -234062 | -23.4062 | 0 |

## Selected Files

| path | trade_month | symbol |
| --- | --- | --- |
| raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ADANIPORTS\part-00000.parquet | 2026-01 | ADANIPORTS |
| raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ADANIPORTS\part-00000.parquet | 2026-02 | ADANIPORTS |
| raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ADANIPORTS\part-00000.parquet | 2026-03 | ADANIPORTS |
| raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=ADANIPORTS\part-00000.parquet | 2026-04 | ADANIPORTS |
| raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=ADANIPORTS\part-00000.parquet | 2026-05 | ADANIPORTS |
| raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=ADANIPORTS\part-00000.parquet | 2026-06 | ADANIPORTS |
| raw_synthetic_l2_dense_full_year\trade_month=2026-07\symbol=ADANIPORTS\part-00000.parquet | 2026-07 | ADANIPORTS |
| raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ADANIPORTS\part-00000.parquet | 2026-08 | ADANIPORTS |
| raw_synthetic_l2_dense_full_year\trade_month=2026-09\symbol=ADANIPORTS\part-00000.parquet | 2026-09 | ADANIPORTS |
| raw_synthetic_l2_dense_full_year\trade_month=2026-10\symbol=ADANIPORTS\part-00000.parquet | 2026-10 | ADANIPORTS |
| raw_synthetic_l2_dense_full_year\trade_month=2026-11\symbol=ADANIPORTS\part-00000.parquet | 2026-11 | ADANIPORTS |
| raw_synthetic_l2_dense_full_year\trade_month=2026-12\symbol=ADANIPORTS\part-00000.parquet | 2026-12 | ADANIPORTS |
| raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=AXISBANK\part-00000.parquet | 2026-01 | AXISBANK |
| raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=AXISBANK\part-00000.parquet | 2026-02 | AXISBANK |
| raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=AXISBANK\part-00000.parquet | 2026-03 | AXISBANK |
| raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=AXISBANK\part-00000.parquet | 2026-04 | AXISBANK |
| raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=AXISBANK\part-00000.parquet | 2026-05 | AXISBANK |
| raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=AXISBANK\part-00000.parquet | 2026-06 | AXISBANK |
| raw_synthetic_l2_dense_full_year\trade_month=2026-07\symbol=AXISBANK\part-00000.parquet | 2026-07 | AXISBANK |
| raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=AXISBANK\part-00000.parquet | 2026-08 | AXISBANK |
| raw_synthetic_l2_dense_full_year\trade_month=2026-09\symbol=AXISBANK\part-00000.parquet | 2026-09 | AXISBANK |
| raw_synthetic_l2_dense_full_year\trade_month=2026-10\symbol=AXISBANK\part-00000.parquet | 2026-10 | AXISBANK |
| raw_synthetic_l2_dense_full_year\trade_month=2026-11\symbol=AXISBANK\part-00000.parquet | 2026-11 | AXISBANK |
| raw_synthetic_l2_dense_full_year\trade_month=2026-12\symbol=AXISBANK\part-00000.parquet | 2026-12 | AXISBANK |
| raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-01 | BAJAJ-AUTO |
| raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-02 | BAJAJ-AUTO |
| raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-03 | BAJAJ-AUTO |
| raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-04 | BAJAJ-AUTO |
| raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-05 | BAJAJ-AUTO |
| raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-06 | BAJAJ-AUTO |
| raw_synthetic_l2_dense_full_year\trade_month=2026-07\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-07 | BAJAJ-AUTO |
| raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-08 | BAJAJ-AUTO |
| raw_synthetic_l2_dense_full_year\trade_month=2026-09\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-09 | BAJAJ-AUTO |
| raw_synthetic_l2_dense_full_year\trade_month=2026-10\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-10 | BAJAJ-AUTO |
| raw_synthetic_l2_dense_full_year\trade_month=2026-11\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-11 | BAJAJ-AUTO |
| raw_synthetic_l2_dense_full_year\trade_month=2026-12\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-12 | BAJAJ-AUTO |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P449_PHASE448_PRECOMMIT_USED | True | 1 | 1 | hard |
| P449_RAW_FILES_SCANNED | True | 36 | >0 | hard |
| P449_FULL_DEPTH_L2_L5_PRIMARY | True | dynamic_curvature_score uses buy/sell quantities at levels 2-5 | levels_2_to_5 | hard |
| P449_COMPLETED_ROUND_TRIPS_GE_30 | True | 1512 | >=30 | hard |
| P449_DATE_BREADTH_GE_5 | True | 252 | >=5 | hard |
| P449_SYMBOL_BREADTH_GE_3 | True | 3 | >=3 | hard |
| P449_POSITIVE_DATE_FRACTION_GE_0_60 | False | 0.166667 | >=0.60 | hard |
| P449_ANNUALIZED_GE_12_COST200 | False | -23.8862 | >=12.0 | hard |
| P449_L1_ONLY_NOT_DOMINANT | False | primary=-238862.03393146786;l1=-218598.1333378012 | primary_gt_l1 | hard |
| P449_SIDE_FLIP_NOT_DOMINANT | True | primary=-238862.03393146786;side_flip=-282923.80438962794 | primary_gt_side_flip | hard |
| P449_STATIC_SNAPSHOT_NOT_DOMINANT | False | primary=-238862.03393146786;static=-196206.98747506447 | primary_gt_static | hard |
| P449_TIME_SHIFT_NOT_DOMINANT | False | primary=-238862.03393146786;shift=-234062.1660561393 | primary_gt_shift | hard |
| P449_COST200_FIXED_CAPITAL | True | cost=2.0;capital=1000000.0;notional=100000.0 | cost200_fixed_capital | hard |
| P449_NO_PROMOTION_PAPER_LIVE | True | promotion=0;paper_live=0;claim=0 | all_zero | hard |

Boundary: no paper/live acceptance, strategy promotion or deployable profitability claim is emitted by Phase449.

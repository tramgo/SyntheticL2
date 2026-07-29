# Phase226 Cost-aware Event Label Materialization Dry Run

Generated UTC: 2026-07-29T05:36:34.354323+00:00

Phase226 materializes train/validation-only cost-aware event labels from Phase225 contracts.
Unavailable contracted horizons are recorded explicitly; no model fit, replay, sealed test, promotion, paper/live, or profitability artifact is emitted.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase226_horizon_availability_rows | 3 | Contracted horizon availability rows |
| phase226_available_horizon_rows | 2 | Available contracted horizons |
| phase226_blocked_horizon_rows | 1 | Unavailable contracted horizons |
| phase226_label_partition_rows | 256 | Materialized label partition rows |
| phase226_materialized_horizons | 2 | Materialized horizons |
| phase226_total_label_rows | 45631 | Total materialized event rows |
| phase226_cost_aware_actionable_rows | 136 | Cost-aware actionable label rows |
| phase226_cost_aware_up_rows | 45 | Cost-aware up rows |
| phase226_cost_aware_down_rows | 91 | Cost-aware down rows |
| phase226_split_summary_rows | 4 | Split quality summary rows |
| phase226_quality_pass_rows | 0 | Split quality pass rows |
| phase226_negative_control_summary_rows | 12 | Negative-control summary rows |
| phase226_sealed_test_rows_available | 184909 | Sealed test rows available but not used |
| phase226_test_rows_used | 0 | No sealed test rows used |
| phase226_model_fit_allowed_next | 0 | No model fit opened |
| phase226_strategy_replay_allowed | 0 | No strategy replay opened |
| phase226_broader_replay_allowed_next | 0 | No broader replay opened |
| phase226_test_replay_allowed_next | 0 | No test replay opened |
| phase226_promotion_allowed | 0 | No promotion opened |
| phase226_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase226_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase226_forbidden_execution_rows | 14 | Forbidden execution rows |
| phase226_gate_rows | 7 | Gates evaluated |
| phase226_hard_gate_rows | 7 | Hard gates evaluated |
| phase226_hard_gate_pass_rows | 7 | Hard gates passed |
| phase226_cost_aware_event_label_materialization_dry_run_complete | 1 | 1 means Phase226 completed |
| phase226_forbidden_outputs | model_fit;model_prediction;strategy_replay;broader_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export | Outputs forbidden in this phase |
| phase226_next_best_action | run_phase227_cost_aware_event_label_quality_interpretation_no_fit_no_replay_no_test | Recommended next milestone |

## Horizon Availability Ledger

| phase225_label_contract_id | horizon_sec | phase181_allowed_partitions | phase214_allowed_partitions | materialization_available | blocked_reason | test_rows_used |
| --- | --- | --- | --- | --- | --- | --- |
| P225_COST_AWARE_EVENT_MOVE_H5s | 5 | 128 | 128 | 1 |  | 0 |
| P225_COST_AWARE_EVENT_MOVE_H15s | 15 | 128 | 128 | 1 |  | 0 |
| P225_COST_AWARE_EVENT_MOVE_H30s | 30 | 0 | 0 | 0 | contracted_horizon_not_available_in_current_phase181_phase214_train_validation_inputs | 0 |

## Label Partition Inventory

| horizon_sec | trade_date | exchange | symbol | split_role | rows | cost_aware_actionable_rows | cost_aware_up_rows | cost_aware_down_rows | label_file | bytes | test_rows_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 2026-07-08 | NSE | ADANIPORTS | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | AXISBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | BANKBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | BHARTIARTL | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | BPCL | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | BRITANNIA | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | CIPLA | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | DRREDDY | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | GOLDBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | HCLTECH | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | HDFCBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | HINDUNILVR | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | ICICIBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | INFY | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=INFY\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | ITBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | ITC | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ITC\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | JUNIORBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | KOTAKBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | LT | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=LT\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | M&M | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=M&M\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | MARUTI | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | NESTLEIND | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | NIFTYBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | ONGC | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | RELIANCE | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | SBIN | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | SUNPHARMA | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | TCS | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=TCS\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | TECHM | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | ULTRACEMCO | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ULTRACEMCO\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-08 | NSE | WIPRO | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=WIPRO\cost_aware_event_labels.parquet | 8375 | 0 |
| 5 | 2026-07-09 | NSE | ADANIPORTS | train | 240 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ADANIPORTS\cost_aware_event_labels.parquet | 17472 | 0 |
| 5 | 2026-07-09 | NSE | AXISBANK | train | 268 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=AXISBANK\cost_aware_event_labels.parquet | 17626 | 0 |
| 5 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 210 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BAJAJ-AUTO\cost_aware_event_labels.parquet | 16636 | 0 |
| 5 | 2026-07-09 | NSE | BANKBEES | train | 318 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BANKBEES\cost_aware_event_labels.parquet | 20512 | 0 |
| 5 | 2026-07-09 | NSE | BHARTIARTL | train | 667 | 2 | 2 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BHARTIARTL\cost_aware_event_labels.parquet | 28485 | 0 |
| 5 | 2026-07-09 | NSE | BPCL | train | 192 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BPCL\cost_aware_event_labels.parquet | 14505 | 0 |
| 5 | 2026-07-09 | NSE | BRITANNIA | train | 732 | 3 | 2 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BRITANNIA\cost_aware_event_labels.parquet | 24810 | 0 |
| 5 | 2026-07-09 | NSE | CIPLA | train | 209 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=CIPLA\cost_aware_event_labels.parquet | 15479 | 0 |
| 5 | 2026-07-09 | NSE | DRREDDY | train | 1216 | 4 | 1 | 3 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=DRREDDY\cost_aware_event_labels.parquet | 38714 | 0 |
| 5 | 2026-07-09 | NSE | GOLDBEES | train | 316 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=GOLDBEES\cost_aware_event_labels.parquet | 16525 | 0 |
| 5 | 2026-07-09 | NSE | HCLTECH | train | 664 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=HCLTECH\cost_aware_event_labels.parquet | 25518 | 0 |
| 5 | 2026-07-09 | NSE | HDFCBANK | train | 459 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=HDFCBANK\cost_aware_event_labels.parquet | 21556 | 0 |
| 5 | 2026-07-09 | NSE | HINDUNILVR | train | 428 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=HINDUNILVR\cost_aware_event_labels.parquet | 23444 | 0 |
| 5 | 2026-07-09 | NSE | ICICIBANK | train | 441 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ICICIBANK\cost_aware_event_labels.parquet | 20050 | 0 |
| 5 | 2026-07-09 | NSE | INFY | train | 296 | 1 | 1 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=INFY\cost_aware_event_labels.parquet | 18204 | 0 |
| 5 | 2026-07-09 | NSE | ITBEES | train | 431 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ITBEES\cost_aware_event_labels.parquet | 15865 | 0 |
| 5 | 2026-07-09 | NSE | ITC | train | 403 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ITC\cost_aware_event_labels.parquet | 17210 | 0 |
| 5 | 2026-07-09 | NSE | JUNIORBEES | train | 325 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=JUNIORBEES\cost_aware_event_labels.parquet | 20604 | 0 |
| 5 | 2026-07-09 | NSE | KOTAKBANK | train | 489 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=KOTAKBANK\cost_aware_event_labels.parquet | 21759 | 0 |
| 5 | 2026-07-09 | NSE | LT | train | 446 | 1 | 1 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=LT\cost_aware_event_labels.parquet | 24304 | 0 |
| 5 | 2026-07-09 | NSE | M&M | train | 321 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=M&M\cost_aware_event_labels.parquet | 20142 | 0 |
| 5 | 2026-07-09 | NSE | MARUTI | train | 410 | 2 | 0 | 2 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=MARUTI\cost_aware_event_labels.parquet | 20227 | 0 |
| 5 | 2026-07-09 | NSE | NESTLEIND | train | 165 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=NESTLEIND\cost_aware_event_labels.parquet | 15383 | 0 |
| 5 | 2026-07-09 | NSE | NIFTYBEES | train | 237 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=NIFTYBEES\cost_aware_event_labels.parquet | 17059 | 0 |
| 5 | 2026-07-09 | NSE | ONGC | train | 220 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ONGC\cost_aware_event_labels.parquet | 16741 | 0 |
| 5 | 2026-07-09 | NSE | RELIANCE | train | 402 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=RELIANCE\cost_aware_event_labels.parquet | 21376 | 0 |
| 5 | 2026-07-09 | NSE | SBIN | train | 387 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=SBIN\cost_aware_event_labels.parquet | 19059 | 0 |
| 5 | 2026-07-09 | NSE | SUNPHARMA | train | 487 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=SUNPHARMA\cost_aware_event_labels.parquet | 22266 | 0 |
| 5 | 2026-07-09 | NSE | TCS | train | 506 | 1 | 1 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=TCS\cost_aware_event_labels.parquet | 25187 | 0 |
| 5 | 2026-07-09 | NSE | TECHM | train | 586 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=TECHM\cost_aware_event_labels.parquet | 24351 | 0 |
| 5 | 2026-07-09 | NSE | ULTRACEMCO | train | 99 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ULTRACEMCO\cost_aware_event_labels.parquet | 13216 | 0 |
| 5 | 2026-07-09 | NSE | WIPRO | train | 779 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=WIPRO\cost_aware_event_labels.parquet | 28231 | 0 |
| 5 | 2026-07-10 | NSE | ADANIPORTS | train | 379 | 3 | 1 | 2 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\cost_aware_event_labels.parquet | 20608 | 0 |
| 5 | 2026-07-10 | NSE | AXISBANK | train | 253 | 2 | 2 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\cost_aware_event_labels.parquet | 17163 | 0 |
| 5 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 435 | 2 | 1 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\cost_aware_event_labels.parquet | 23164 | 0 |
| 5 | 2026-07-10 | NSE | BANKBEES | train | 201 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\cost_aware_event_labels.parquet | 16628 | 0 |
| 5 | 2026-07-10 | NSE | BHARTIARTL | train | 256 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\cost_aware_event_labels.parquet | 17558 | 0 |
| 5 | 2026-07-10 | NSE | BPCL | train | 155 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\cost_aware_event_labels.parquet | 13801 | 0 |
| 5 | 2026-07-10 | NSE | BRITANNIA | train | 509 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\cost_aware_event_labels.parquet | 21883 | 0 |
| 5 | 2026-07-10 | NSE | CIPLA | train | 256 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\cost_aware_event_labels.parquet | 17582 | 0 |
| 5 | 2026-07-10 | NSE | DRREDDY | train | 504 | 6 | 2 | 4 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=DRREDDY\cost_aware_event_labels.parquet | 24116 | 0 |
| 5 | 2026-07-10 | NSE | GOLDBEES | train | 311 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=GOLDBEES\cost_aware_event_labels.parquet | 16699 | 0 |
| 5 | 2026-07-10 | NSE | HCLTECH | train | 1091 | 5 | 5 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=HCLTECH\cost_aware_event_labels.parquet | 34973 | 0 |
| 5 | 2026-07-10 | NSE | HDFCBANK | train | 525 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=HDFCBANK\cost_aware_event_labels.parquet | 21308 | 0 |
| 5 | 2026-07-10 | NSE | HINDUNILVR | train | 239 | 1 | 1 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=HINDUNILVR\cost_aware_event_labels.parquet | 16915 | 0 |
| 5 | 2026-07-10 | NSE | ICICIBANK | train | 254 | 1 | 1 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=ICICIBANK\cost_aware_event_labels.parquet | 16794 | 0 |
| 5 | 2026-07-10 | NSE | INFY | train | 671 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=INFY\cost_aware_event_labels.parquet | 24991 | 0 |
| 5 | 2026-07-10 | NSE | ITBEES | train | 696 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=ITBEES\cost_aware_event_labels.parquet | 18312 | 0 |
| 5 | 2026-07-10 | NSE | ITC | train | 364 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=ITC\cost_aware_event_labels.parquet | 15787 | 0 |
| 5 | 2026-07-10 | NSE | JUNIORBEES | train | 456 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=JUNIORBEES\cost_aware_event_labels.parquet | 24088 | 0 |
| 5 | 2026-07-10 | NSE | KOTAKBANK | train | 181 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=KOTAKBANK\cost_aware_event_labels.parquet | 14627 | 0 |
| 5 | 2026-07-10 | NSE | LT | train | 199 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=LT\cost_aware_event_labels.parquet | 16372 | 0 |
| 5 | 2026-07-10 | NSE | M&M | train | 185 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=M&M\cost_aware_event_labels.parquet | 15704 | 0 |
| 5 | 2026-07-10 | NSE | MARUTI | train | 281 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=MARUTI\cost_aware_event_labels.parquet | 18511 | 0 |
| 5 | 2026-07-10 | NSE | NESTLEIND | train | 260 | 1 | 1 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=NESTLEIND\cost_aware_event_labels.parquet | 17886 | 0 |
| 5 | 2026-07-10 | NSE | NIFTYBEES | train | 297 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=NIFTYBEES\cost_aware_event_labels.parquet | 17273 | 0 |
| 5 | 2026-07-10 | NSE | ONGC | train | 340 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=ONGC\cost_aware_event_labels.parquet | 19487 | 0 |
| 5 | 2026-07-10 | NSE | RELIANCE | train | 241 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=RELIANCE\cost_aware_event_labels.parquet | 16387 | 0 |
| 5 | 2026-07-10 | NSE | SBIN | train | 383 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=SBIN\cost_aware_event_labels.parquet | 20484 | 0 |
| 5 | 2026-07-10 | NSE | SUNPHARMA | train | 221 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=SUNPHARMA\cost_aware_event_labels.parquet | 17277 | 0 |
| 5 | 2026-07-10 | NSE | TCS | train | 815 | 2 | 1 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=TCS\cost_aware_event_labels.parquet | 32935 | 0 |
| 5 | 2026-07-10 | NSE | TECHM | train | 456 | 2 | 0 | 2 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=TECHM\cost_aware_event_labels.parquet | 22920 | 0 |
| 5 | 2026-07-10 | NSE | ULTRACEMCO | train | 627 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=ULTRACEMCO\cost_aware_event_labels.parquet | 23055 | 0 |
| 5 | 2026-07-10 | NSE | WIPRO | train | 532 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-10\exchange=NSE\symbol=WIPRO\cost_aware_event_labels.parquet | 23626 | 0 |
| 5 | 2026-07-13 | NSE | ADANIPORTS | validation | 364 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=ADANIPORTS\cost_aware_event_labels.parquet | 21112 | 0 |
| 5 | 2026-07-13 | NSE | AXISBANK | validation | 345 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=AXISBANK\cost_aware_event_labels.parquet | 19328 | 0 |
| 5 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 969 | 3 | 2 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=BAJAJ-AUTO\cost_aware_event_labels.parquet | 39928 | 0 |
| 5 | 2026-07-13 | NSE | BANKBEES | validation | 427 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=BANKBEES\cost_aware_event_labels.parquet | 23047 | 0 |
| 5 | 2026-07-13 | NSE | BHARTIARTL | validation | 320 | 4 | 1 | 3 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=BHARTIARTL\cost_aware_event_labels.parquet | 19204 | 0 |
| 5 | 2026-07-13 | NSE | BPCL | validation | 901 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=BPCL\cost_aware_event_labels.parquet | 23696 | 0 |
| 5 | 2026-07-13 | NSE | BRITANNIA | validation | 795 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=BRITANNIA\cost_aware_event_labels.parquet | 24464 | 0 |
| 5 | 2026-07-13 | NSE | CIPLA | validation | 328 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=CIPLA\cost_aware_event_labels.parquet | 18362 | 0 |
| 5 | 2026-07-13 | NSE | DRREDDY | validation | 96 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=DRREDDY\cost_aware_event_labels.parquet | 13634 | 0 |
| 5 | 2026-07-13 | NSE | GOLDBEES | validation | 306 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=GOLDBEES\cost_aware_event_labels.parquet | 16569 | 0 |
| 5 | 2026-07-13 | NSE | HCLTECH | validation | 961 | 2 | 1 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=HCLTECH\cost_aware_event_labels.parquet | 37331 | 0 |
| 5 | 2026-07-13 | NSE | HDFCBANK | validation | 677 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=HDFCBANK\cost_aware_event_labels.parquet | 26747 | 0 |
| 5 | 2026-07-13 | NSE | HINDUNILVR | validation | 257 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=HINDUNILVR\cost_aware_event_labels.parquet | 17627 | 0 |
| 5 | 2026-07-13 | NSE | ICICIBANK | validation | 488 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=ICICIBANK\cost_aware_event_labels.parquet | 23179 | 0 |
| 5 | 2026-07-13 | NSE | INFY | validation | 789 | 2 | 1 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=INFY\cost_aware_event_labels.parquet | 32790 | 0 |
| 5 | 2026-07-13 | NSE | ITBEES | validation | 950 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=ITBEES\cost_aware_event_labels.parquet | 24994 | 0 |
| 5 | 2026-07-13 | NSE | ITC | validation | 119 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=ITC\cost_aware_event_labels.parquet | 12630 | 0 |
| 5 | 2026-07-13 | NSE | JUNIORBEES | validation | 401 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=JUNIORBEES\cost_aware_event_labels.parquet | 22859 | 0 |
| 5 | 2026-07-13 | NSE | KOTAKBANK | validation | 176 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=KOTAKBANK\cost_aware_event_labels.parquet | 14922 | 0 |
| 5 | 2026-07-13 | NSE | LT | validation | 320 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=LT\cost_aware_event_labels.parquet | 20690 | 0 |
| 5 | 2026-07-13 | NSE | M&M | validation | 552 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=M&M\cost_aware_event_labels.parquet | 27553 | 0 |
| 5 | 2026-07-13 | NSE | MARUTI | validation | 580 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=MARUTI\cost_aware_event_labels.parquet | 25317 | 0 |
| 5 | 2026-07-13 | NSE | NESTLEIND | validation | 424 | 4 | 1 | 3 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=NESTLEIND\cost_aware_event_labels.parquet | 21544 | 0 |
| 5 | 2026-07-13 | NSE | NIFTYBEES | validation | 447 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=NIFTYBEES\cost_aware_event_labels.parquet | 23165 | 0 |
| 5 | 2026-07-13 | NSE | ONGC | validation | 507 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=ONGC\cost_aware_event_labels.parquet | 24683 | 0 |
| 5 | 2026-07-13 | NSE | RELIANCE | validation | 587 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=RELIANCE\cost_aware_event_labels.parquet | 22195 | 0 |
| 5 | 2026-07-13 | NSE | SBIN | validation | 499 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=SBIN\cost_aware_event_labels.parquet | 21527 | 0 |
| 5 | 2026-07-13 | NSE | SUNPHARMA | validation | 387 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=SUNPHARMA\cost_aware_event_labels.parquet | 21666 | 0 |
| 5 | 2026-07-13 | NSE | TCS | validation | 911 | 4 | 3 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=TCS\cost_aware_event_labels.parquet | 37595 | 0 |
| 5 | 2026-07-13 | NSE | TECHM | validation | 713 | 5 | 3 | 2 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=TECHM\cost_aware_event_labels.parquet | 32618 | 0 |
| 5 | 2026-07-13 | NSE | ULTRACEMCO | validation | 764 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=ULTRACEMCO\cost_aware_event_labels.parquet | 24239 | 0 |
| 5 | 2026-07-13 | NSE | WIPRO | validation | 712 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=5s\trade_date=2026-07-13\exchange=NSE\symbol=WIPRO\cost_aware_event_labels.parquet | 31750 | 0 |
| 15 | 2026-07-08 | NSE | ADANIPORTS | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | AXISBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | BANKBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | BHARTIARTL | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | BPCL | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | BRITANNIA | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | CIPLA | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | DRREDDY | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | GOLDBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | HCLTECH | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | HDFCBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | HINDUNILVR | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | ICICIBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | INFY | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=INFY\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | ITBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | ITC | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=ITC\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | JUNIORBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | KOTAKBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | LT | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=LT\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | M&M | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=M&M\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | MARUTI | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | NESTLEIND | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | NIFTYBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | ONGC | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | RELIANCE | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | SBIN | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | SUNPHARMA | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | TCS | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=TCS\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | TECHM | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | ULTRACEMCO | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=ULTRACEMCO\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-08 | NSE | WIPRO | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-08\exchange=NSE\symbol=WIPRO\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-09 | NSE | ADANIPORTS | train | 5 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=ADANIPORTS\cost_aware_event_labels.parquet | 10720 | 0 |
| 15 | 2026-07-09 | NSE | AXISBANK | train | 1 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=AXISBANK\cost_aware_event_labels.parquet | 10578 | 0 |
| 15 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 11 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=BAJAJ-AUTO\cost_aware_event_labels.parquet | 10931 | 0 |
| 15 | 2026-07-09 | NSE | BANKBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=BANKBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-09 | NSE | BHARTIARTL | train | 14 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=BHARTIARTL\cost_aware_event_labels.parquet | 11023 | 0 |
| 15 | 2026-07-09 | NSE | BPCL | train | 8 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=BPCL\cost_aware_event_labels.parquet | 10787 | 0 |
| 15 | 2026-07-09 | NSE | BRITANNIA | train | 175 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=BRITANNIA\cost_aware_event_labels.parquet | 15358 | 0 |
| 15 | 2026-07-09 | NSE | CIPLA | train | 10 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=CIPLA\cost_aware_event_labels.parquet | 10829 | 0 |
| 15 | 2026-07-09 | NSE | DRREDDY | train | 525 | 7 | 2 | 5 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=DRREDDY\cost_aware_event_labels.parquet | 25398 | 0 |
| 15 | 2026-07-09 | NSE | GOLDBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=GOLDBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-09 | NSE | HCLTECH | train | 129 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=HCLTECH\cost_aware_event_labels.parquet | 14383 | 0 |
| 15 | 2026-07-09 | NSE | HDFCBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=HDFCBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-09 | NSE | HINDUNILVR | train | 52 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=HINDUNILVR\cost_aware_event_labels.parquet | 12156 | 0 |
| 15 | 2026-07-09 | NSE | ICICIBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=ICICIBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-09 | NSE | INFY | train | 2 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=INFY\cost_aware_event_labels.parquet | 10590 | 0 |
| 15 | 2026-07-09 | NSE | ITBEES | train | 85 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=ITBEES\cost_aware_event_labels.parquet | 12187 | 0 |
| 15 | 2026-07-09 | NSE | ITC | train | 4 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=ITC\cost_aware_event_labels.parquet | 10643 | 0 |
| 15 | 2026-07-09 | NSE | JUNIORBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=JUNIORBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-09 | NSE | KOTAKBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=KOTAKBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-09 | NSE | LT | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=LT\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-09 | NSE | M&M | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=M&M\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-09 | NSE | MARUTI | train | 3 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=MARUTI\cost_aware_event_labels.parquet | 10636 | 0 |
| 15 | 2026-07-09 | NSE | NESTLEIND | train | 10 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=NESTLEIND\cost_aware_event_labels.parquet | 10850 | 0 |
| 15 | 2026-07-09 | NSE | NIFTYBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=NIFTYBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-09 | NSE | ONGC | train | 1 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=ONGC\cost_aware_event_labels.parquet | 10558 | 0 |
| 15 | 2026-07-09 | NSE | RELIANCE | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=RELIANCE\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-09 | NSE | SBIN | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=SBIN\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-09 | NSE | SUNPHARMA | train | 90 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=SUNPHARMA\cost_aware_event_labels.parquet | 13241 | 0 |
| 15 | 2026-07-09 | NSE | TCS | train | 10 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=TCS\cost_aware_event_labels.parquet | 10868 | 0 |
| 15 | 2026-07-09 | NSE | TECHM | train | 43 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=TECHM\cost_aware_event_labels.parquet | 11888 | 0 |
| 15 | 2026-07-09 | NSE | ULTRACEMCO | train | 2 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=ULTRACEMCO\cost_aware_event_labels.parquet | 10596 | 0 |
| 15 | 2026-07-09 | NSE | WIPRO | train | 180 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-09\exchange=NSE\symbol=WIPRO\cost_aware_event_labels.parquet | 15782 | 0 |
| 15 | 2026-07-10 | NSE | ADANIPORTS | train | 2 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\cost_aware_event_labels.parquet | 10652 | 0 |
| 15 | 2026-07-10 | NSE | AXISBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 7 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\cost_aware_event_labels.parquet | 10812 | 0 |
| 15 | 2026-07-10 | NSE | BANKBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-10 | NSE | BHARTIARTL | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-10 | NSE | BPCL | train | 5 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\cost_aware_event_labels.parquet | 10681 | 0 |
| 15 | 2026-07-10 | NSE | BRITANNIA | train | 70 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\cost_aware_event_labels.parquet | 12744 | 0 |
| 15 | 2026-07-10 | NSE | CIPLA | train | 9 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\cost_aware_event_labels.parquet | 10844 | 0 |
| 15 | 2026-07-10 | NSE | DRREDDY | train | 2 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=DRREDDY\cost_aware_event_labels.parquet | 10605 | 0 |
| 15 | 2026-07-10 | NSE | GOLDBEES | train | 1 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=GOLDBEES\cost_aware_event_labels.parquet | 10578 | 0 |
| 15 | 2026-07-10 | NSE | HCLTECH | train | 131 | 1 | 1 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=HCLTECH\cost_aware_event_labels.parquet | 14623 | 0 |
| 15 | 2026-07-10 | NSE | HDFCBANK | train | 1 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=HDFCBANK\cost_aware_event_labels.parquet | 10578 | 0 |
| 15 | 2026-07-10 | NSE | HINDUNILVR | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=HINDUNILVR\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-10 | NSE | ICICIBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=ICICIBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-10 | NSE | INFY | train | 1 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=INFY\cost_aware_event_labels.parquet | 10558 | 0 |
| 15 | 2026-07-10 | NSE | ITBEES | train | 56 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=ITBEES\cost_aware_event_labels.parquet | 11545 | 0 |
| 15 | 2026-07-10 | NSE | ITC | train | 1 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=ITC\cost_aware_event_labels.parquet | 10552 | 0 |
| 15 | 2026-07-10 | NSE | JUNIORBEES | train | 1 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=JUNIORBEES\cost_aware_event_labels.parquet | 10588 | 0 |
| 15 | 2026-07-10 | NSE | KOTAKBANK | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=KOTAKBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-10 | NSE | LT | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=LT\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-10 | NSE | M&M | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=M&M\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-10 | NSE | MARUTI | train | 2 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=MARUTI\cost_aware_event_labels.parquet | 10632 | 0 |
| 15 | 2026-07-10 | NSE | NESTLEIND | train | 21 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=NESTLEIND\cost_aware_event_labels.parquet | 11293 | 0 |
| 15 | 2026-07-10 | NSE | NIFTYBEES | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=NIFTYBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-10 | NSE | ONGC | train | 1 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=ONGC\cost_aware_event_labels.parquet | 10558 | 0 |
| 15 | 2026-07-10 | NSE | RELIANCE | train | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=RELIANCE\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-10 | NSE | SBIN | train | 1 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=SBIN\cost_aware_event_labels.parquet | 10558 | 0 |
| 15 | 2026-07-10 | NSE | SUNPHARMA | train | 2 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=SUNPHARMA\cost_aware_event_labels.parquet | 10647 | 0 |
| 15 | 2026-07-10 | NSE | TCS | train | 1 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=TCS\cost_aware_event_labels.parquet | 10552 | 0 |
| 15 | 2026-07-10 | NSE | TECHM | train | 28 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=TECHM\cost_aware_event_labels.parquet | 11487 | 0 |
| 15 | 2026-07-10 | NSE | ULTRACEMCO | train | 28 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=ULTRACEMCO\cost_aware_event_labels.parquet | 11408 | 0 |
| 15 | 2026-07-10 | NSE | WIPRO | train | 61 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-10\exchange=NSE\symbol=WIPRO\cost_aware_event_labels.parquet | 12329 | 0 |
| 15 | 2026-07-13 | NSE | ADANIPORTS | validation | 6 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=ADANIPORTS\cost_aware_event_labels.parquet | 10771 | 0 |
| 15 | 2026-07-13 | NSE | AXISBANK | validation | 3 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=AXISBANK\cost_aware_event_labels.parquet | 10703 | 0 |
| 15 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 66 | 6 | 3 | 3 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=BAJAJ-AUTO\cost_aware_event_labels.parquet | 12968 | 0 |
| 15 | 2026-07-13 | NSE | BANKBEES | validation | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=BANKBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-13 | NSE | BHARTIARTL | validation | 1 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=BHARTIARTL\cost_aware_event_labels.parquet | 10613 | 0 |
| 15 | 2026-07-13 | NSE | BPCL | validation | 47 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=BPCL\cost_aware_event_labels.parquet | 11588 | 0 |
| 15 | 2026-07-13 | NSE | BRITANNIA | validation | 77 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=BRITANNIA\cost_aware_event_labels.parquet | 12732 | 0 |
| 15 | 2026-07-13 | NSE | CIPLA | validation | 22 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=CIPLA\cost_aware_event_labels.parquet | 11270 | 0 |
| 15 | 2026-07-13 | NSE | DRREDDY | validation | 1 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=DRREDDY\cost_aware_event_labels.parquet | 10598 | 0 |
| 15 | 2026-07-13 | NSE | GOLDBEES | validation | 4 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=GOLDBEES\cost_aware_event_labels.parquet | 10677 | 0 |
| 15 | 2026-07-13 | NSE | HCLTECH | validation | 179 | 3 | 1 | 2 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=HCLTECH\cost_aware_event_labels.parquet | 16150 | 0 |
| 15 | 2026-07-13 | NSE | HDFCBANK | validation | 1 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=HDFCBANK\cost_aware_event_labels.parquet | 10603 | 0 |
| 15 | 2026-07-13 | NSE | HINDUNILVR | validation | 4 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=HINDUNILVR\cost_aware_event_labels.parquet | 10743 | 0 |
| 15 | 2026-07-13 | NSE | ICICIBANK | validation | 1 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=ICICIBANK\cost_aware_event_labels.parquet | 10608 | 0 |
| 15 | 2026-07-13 | NSE | INFY | validation | 1 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=INFY\cost_aware_event_labels.parquet | 10583 | 0 |
| 15 | 2026-07-13 | NSE | ITBEES | validation | 151 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=ITBEES\cost_aware_event_labels.parquet | 14123 | 0 |
| 15 | 2026-07-13 | NSE | ITC | validation | 2 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=ITC\cost_aware_event_labels.parquet | 10625 | 0 |
| 15 | 2026-07-13 | NSE | JUNIORBEES | validation | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=JUNIORBEES\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-13 | NSE | KOTAKBANK | validation | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=KOTAKBANK\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-13 | NSE | LT | validation | 1 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=LT\cost_aware_event_labels.parquet | 10572 | 0 |
| 15 | 2026-07-13 | NSE | M&M | validation | 0 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=M&M\cost_aware_event_labels.parquet | 8375 | 0 |
| 15 | 2026-07-13 | NSE | MARUTI | validation | 1 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=MARUTI\cost_aware_event_labels.parquet | 10593 | 0 |
| 15 | 2026-07-13 | NSE | NESTLEIND | validation | 31 | 2 | 1 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=NESTLEIND\cost_aware_event_labels.parquet | 11650 | 0 |
| 15 | 2026-07-13 | NSE | NIFTYBEES | validation | 1 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=NIFTYBEES\cost_aware_event_labels.parquet | 10608 | 0 |
| 15 | 2026-07-13 | NSE | ONGC | validation | 6 | 0 | 0 | 0 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=ONGC\cost_aware_event_labels.parquet | 10746 | 0 |
| 15 | 2026-07-13 | NSE | RELIANCE | validation | 4 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=RELIANCE\cost_aware_event_labels.parquet | 10733 | 0 |
| 15 | 2026-07-13 | NSE | SBIN | validation | 2 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=SBIN\cost_aware_event_labels.parquet | 10647 | 0 |
| 15 | 2026-07-13 | NSE | SUNPHARMA | validation | 3 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=SUNPHARMA\cost_aware_event_labels.parquet | 10708 | 0 |
| 15 | 2026-07-13 | NSE | TCS | validation | 3 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=TCS\cost_aware_event_labels.parquet | 10677 | 0 |
| 15 | 2026-07-13 | NSE | TECHM | validation | 106 | 3 | 2 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=TECHM\cost_aware_event_labels.parquet | 14181 | 0 |
| 15 | 2026-07-13 | NSE | ULTRACEMCO | validation | 29 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=ULTRACEMCO\cost_aware_event_labels.parquet | 11485 | 0 |
| 15 | 2026-07-13 | NSE | WIPRO | validation | 92 | 1 | 0 | 1 | derived_phase226_cost_aware_event_labels\horizon=15s\trade_date=2026-07-13\exchange=NSE\symbol=WIPRO\cost_aware_event_labels.parquet | 13677 | 0 |

## Split Quality Summary

| horizon_sec | split_role | partitions | rows | cost_aware_actionable_rows | symbols | trade_dates | passes_min_event_count | passes_min_symbol_count | passes_min_trade_date_count | quality_gate_pass | test_rows_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | train | 96 | 25922 | 48 | 32 | 3 | 0 | 1 | 0 | 0 | 0 |
| 5 | validation | 32 | 17072 | 37 | 32 | 1 | 0 | 1 | 0 | 0 | 0 |
| 15 | train | 96 | 1792 | 22 | 32 | 3 | 0 | 1 | 0 | 0 | 0 |
| 15 | validation | 32 | 845 | 29 | 32 | 1 | 0 | 1 | 0 | 0 | 0 |

## Negative Control Summary

| control_id | horizon_sec | split_role | control_status | reference_actionable_rows | materialized_in_phase226 | model_fit_allowed | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P225_CONTROL_EVENT_TIME_SHUFFLE | 5 | train | precommitted_for_phase227_interpretation | 48 | 0 | 0 | 0 |
| P225_CONTROL_SYMBOL_DATE_BASE_RATE | 5 | train | aggregate_base_rate_available_from_phase226_inventory | 48 | 0 | 0 | 0 |
| P225_CONTROL_COST_HURDLE_ABLATION | 5 | train | cost_hurdle_effect_measured_by_actionable_rate_and_phase214_event_filter | 48 | 0 | 0 | 0 |
| P225_CONTROL_EVENT_TIME_SHUFFLE | 5 | validation | precommitted_for_phase227_interpretation | 37 | 0 | 0 | 0 |
| P225_CONTROL_SYMBOL_DATE_BASE_RATE | 5 | validation | aggregate_base_rate_available_from_phase226_inventory | 37 | 0 | 0 | 0 |
| P225_CONTROL_COST_HURDLE_ABLATION | 5 | validation | cost_hurdle_effect_measured_by_actionable_rate_and_phase214_event_filter | 37 | 0 | 0 | 0 |
| P225_CONTROL_EVENT_TIME_SHUFFLE | 15 | train | precommitted_for_phase227_interpretation | 22 | 0 | 0 | 0 |
| P225_CONTROL_SYMBOL_DATE_BASE_RATE | 15 | train | aggregate_base_rate_available_from_phase226_inventory | 22 | 0 | 0 | 0 |
| P225_CONTROL_COST_HURDLE_ABLATION | 15 | train | cost_hurdle_effect_measured_by_actionable_rate_and_phase214_event_filter | 22 | 0 | 0 | 0 |
| P225_CONTROL_EVENT_TIME_SHUFFLE | 15 | validation | precommitted_for_phase227_interpretation | 29 | 0 | 0 | 0 |
| P225_CONTROL_SYMBOL_DATE_BASE_RATE | 15 | validation | aggregate_base_rate_available_from_phase226_inventory | 29 | 0 | 0 | 0 |
| P225_CONTROL_COST_HURDLE_ABLATION | 15 | validation | cost_hurdle_effect_measured_by_actionable_rate_and_phase214_event_filter | 29 | 0 | 0 | 0 |

## Sealed Test Exclusion Ledger

| horizon_sec | trade_date | exchange | symbol | split_role | sealed_test_rows_available | sealed_test_rows_used | materialized_in_phase226 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 2026-07-14 | NSE | ADANIPORTS | test_untouched | 4199 | 0 | 0 |
| 5 | 2026-07-14 | NSE | AXISBANK | test_untouched | 4332 | 0 | 0 |
| 5 | 2026-07-14 | NSE | BAJAJ-AUTO | test_untouched | 4438 | 0 | 0 |
| 5 | 2026-07-14 | NSE | BANKBEES | test_untouched | 4241 | 0 | 0 |
| 5 | 2026-07-14 | NSE | BHARTIARTL | test_untouched | 4402 | 0 | 0 |
| 5 | 2026-07-14 | NSE | BPCL | test_untouched | 4127 | 0 | 0 |
| 5 | 2026-07-14 | NSE | BRITANNIA | test_untouched | 4099 | 0 | 0 |
| 5 | 2026-07-14 | NSE | CIPLA | test_untouched | 4185 | 0 | 0 |
| 5 | 2026-07-14 | NSE | DRREDDY | test_untouched | 4169 | 0 | 0 |
| 5 | 2026-07-14 | NSE | GOLDBEES | test_untouched | 4174 | 0 | 0 |
| 5 | 2026-07-14 | NSE | HCLTECH | test_untouched | 4472 | 0 | 0 |
| 5 | 2026-07-14 | NSE | HDFCBANK | test_untouched | 4476 | 0 | 0 |
| 5 | 2026-07-14 | NSE | HINDUNILVR | test_untouched | 4212 | 0 | 0 |
| 5 | 2026-07-14 | NSE | ICICIBANK | test_untouched | 4377 | 0 | 0 |
| 5 | 2026-07-14 | NSE | INFY | test_untouched | 4475 | 0 | 0 |
| 5 | 2026-07-14 | NSE | ITBEES | test_untouched | 3980 | 0 | 0 |
| 5 | 2026-07-14 | NSE | ITC | test_untouched | 4325 | 0 | 0 |
| 5 | 2026-07-14 | NSE | JUNIORBEES | test_untouched | 4249 | 0 | 0 |
| 5 | 2026-07-14 | NSE | KOTAKBANK | test_untouched | 4266 | 0 | 0 |
| 5 | 2026-07-14 | NSE | LT | test_untouched | 4364 | 0 | 0 |
| 5 | 2026-07-14 | NSE | M&M | test_untouched | 4369 | 0 | 0 |
| 5 | 2026-07-14 | NSE | MARUTI | test_untouched | 4222 | 0 | 0 |
| 5 | 2026-07-14 | NSE | NESTLEIND | test_untouched | 4193 | 0 | 0 |
| 5 | 2026-07-14 | NSE | NIFTYBEES | test_untouched | 4239 | 0 | 0 |
| 5 | 2026-07-14 | NSE | ONGC | test_untouched | 4246 | 0 | 0 |
| 5 | 2026-07-14 | NSE | RELIANCE | test_untouched | 4383 | 0 | 0 |
| 5 | 2026-07-14 | NSE | SBIN | test_untouched | 4350 | 0 | 0 |
| 5 | 2026-07-14 | NSE | SUNPHARMA | test_untouched | 4263 | 0 | 0 |
| 5 | 2026-07-14 | NSE | TCS | test_untouched | 4473 | 0 | 0 |
| 5 | 2026-07-14 | NSE | TECHM | test_untouched | 4289 | 0 | 0 |
| 5 | 2026-07-14 | NSE | ULTRACEMCO | test_untouched | 4080 | 0 | 0 |
| 5 | 2026-07-14 | NSE | WIPRO | test_untouched | 4204 | 0 | 0 |
| 15 | 2026-07-14 | NSE | ADANIPORTS | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | AXISBANK | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | BAJAJ-AUTO | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | BANKBEES | test_untouched | 1499 | 0 | 0 |
| 15 | 2026-07-14 | NSE | BHARTIARTL | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | BPCL | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | BRITANNIA | test_untouched | 1500 | 0 | 0 |
| 15 | 2026-07-14 | NSE | CIPLA | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | DRREDDY | test_untouched | 1500 | 0 | 0 |
| 15 | 2026-07-14 | NSE | GOLDBEES | test_untouched | 1500 | 0 | 0 |
| 15 | 2026-07-14 | NSE | HCLTECH | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | HDFCBANK | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | HINDUNILVR | test_untouched | 1499 | 0 | 0 |
| 15 | 2026-07-14 | NSE | ICICIBANK | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | INFY | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | ITBEES | test_untouched | 1499 | 0 | 0 |
| 15 | 2026-07-14 | NSE | ITC | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | JUNIORBEES | test_untouched | 1499 | 0 | 0 |
| 15 | 2026-07-14 | NSE | KOTAKBANK | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | LT | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | M&M | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | MARUTI | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | NESTLEIND | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | NIFTYBEES | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | ONGC | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | RELIANCE | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | SBIN | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | SUNPHARMA | test_untouched | 1501 | 0 | 0 |
| 15 | 2026-07-14 | NSE | TCS | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | TECHM | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | ULTRACEMCO | test_untouched | 1502 | 0 | 0 |
| 15 | 2026-07-14 | NSE | WIPRO | test_untouched | 1502 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase226 | allowed_in_phase226 | rationale |
| --- | --- | --- | --- |
| model_fit | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| model_prediction | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| strategy_replay | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| broader_replay | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| test_replay_execution | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| test_result | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| promotion | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| paper_live_acceptance | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| order_arrival | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| fill_model | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| pnl_replay | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| profitability_claim | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| threshold_widening | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |
| row_level_prediction_export | 0 | 0 | Phase226 materializes train/validation cost-aware labels only and emits no fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, row-level prediction export, threshold-widening, or profitability artifact. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P226_PHASE225_COMPLETE | True | phase225_complete=1 | hard |
| P226_HORIZON_AVAILABILITY_RECORDED | True | availability_rows=3; available=2; blocked=1 | hard |
| P226_LABELS_MATERIALIZED_FOR_AVAILABLE_HORIZONS | True | materialized_horizons=2; inventory_rows=256 | hard |
| P226_QUALITY_SUMMARY_RECORDED | True | summary_rows=4; quality_pass_rows=0; actionable_rows=136 | hard |
| P226_NEGATIVE_CONTROL_SUMMARY_RECORDED | True | control_rows=12 | hard |
| P226_TEST_ROWS_UNTOUCHED | True | sealed_test_rows_used=0 | hard |
| P226_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; forbidden_flags=0 | hard |

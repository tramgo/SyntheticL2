# Phase219 Event-only Train/Validation Model-fit Dry Run

Generated UTC: 2026-07-28T22:04:30.954896+00:00

Phase219 executes the Phase218-precommitted train/validation event-only model-fit dry run.
It joins Phase176 receive-flow features with Phase214 event-surprise labels, filters to event_surprise_bucket == 1, fits aggregate diagnostic models, and writes only aggregate metrics/coefficient/control ledgers.
It does not export row-level design matrices or predictions, use sealed test rows, run strategy replay, emit orders/fills/P&L, promote anything, open paper/live acceptance, or make profitability claims.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase219_event_only_partition_rows | 384 | Train/validation event-only joined partition rows |
| phase219_event_only_joined_rows | 129852 | Joined event-only design-matrix rows across partition inventory |
| phase219_model_fit_rows | 21 | Unique model/target/horizon fits |
| phase219_metric_rows | 42 | Train/validation metric rows |
| phase219_validation_metric_rows | 21 | Validation metric rows |
| phase219_coefficient_rows | 231 | Coefficient rows |
| phase219_control_rows | 42 | Base-rate and shuffled-control rows |
| phase219_forbidden_execution_rows | 12 | Forbidden execution rows |
| phase219_gate_rows | 7 | Gates evaluated |
| phase219_hard_gate_rows | 7 | Hard gates evaluated |
| phase219_hard_gate_pass_rows | 7 | Hard gates passed |
| phase219_event_only_train_validation_model_fit_dry_run_complete | 1 | 1 means Phase219 completed |
| phase219_model_fit_execution | 1 | Train/validation event-only model fitting executed |
| phase219_strategy_replay_allowed | 0 | No strategy replay opened |
| phase219_test_replay_allowed_next | 0 | No test replay opened |
| phase219_test_rows_used | 0 | No sealed test rows used |
| phase219_promotion_allowed | 0 | No promotion opened |
| phase219_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase219_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase219_forbidden_outputs | strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_design_matrix_export;row_level_prediction_export | Outputs forbidden in this phase |
| phase219_next_best_action | run_phase220_event_only_model_fit_validation_interpretation_no_replay_no_test | Recommended next milestone |

## Event-only Design Matrix Partition Inventory

| horizon_sec | trade_date | exchange | symbol | split_role | feature_file_exists | label_file_exists | event_only_joined_rows | test_rows_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-07-08 | NSE | ADANIPORTS | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | AXISBANK | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | BANKBEES | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | BHARTIARTL | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | BPCL | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | BRITANNIA | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | CIPLA | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | DRREDDY | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | GOLDBEES | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | HCLTECH | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | HDFCBANK | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | HINDUNILVR | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | ICICIBANK | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | INFY | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | ITBEES | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | ITC | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | JUNIORBEES | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | KOTAKBANK | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | LT | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | M&M | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | MARUTI | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | NESTLEIND | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | NIFTYBEES | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | ONGC | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | RELIANCE | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | SBIN | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | SUNPHARMA | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | TCS | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | TECHM | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | ULTRACEMCO | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-08 | NSE | WIPRO | train | 1 | 1 | 0 | 0 |
| 1 | 2026-07-09 | NSE | ADANIPORTS | train | 1 | 1 | 509 | 0 |
| 1 | 2026-07-09 | NSE | AXISBANK | train | 1 | 1 | 529 | 0 |
| 1 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 1 | 1 | 328 | 0 |
| 1 | 2026-07-09 | NSE | BANKBEES | train | 1 | 1 | 855 | 0 |
| 1 | 2026-07-09 | NSE | BHARTIARTL | train | 1 | 1 | 960 | 0 |
| 1 | 2026-07-09 | NSE | BPCL | train | 1 | 1 | 365 | 0 |
| 1 | 2026-07-09 | NSE | BRITANNIA | train | 1 | 1 | 909 | 0 |
| 1 | 2026-07-09 | NSE | CIPLA | train | 1 | 1 | 421 | 0 |
| 1 | 2026-07-09 | NSE | DRREDDY | train | 1 | 1 | 5218 | 0 |
| 1 | 2026-07-09 | NSE | GOLDBEES | train | 1 | 1 | 590 | 0 |
| 1 | 2026-07-09 | NSE | HCLTECH | train | 1 | 1 | 1575 | 0 |
| 1 | 2026-07-09 | NSE | HDFCBANK | train | 1 | 1 | 866 | 0 |
| 1 | 2026-07-09 | NSE | HINDUNILVR | train | 1 | 1 | 659 | 0 |
| 1 | 2026-07-09 | NSE | ICICIBANK | train | 1 | 1 | 822 | 0 |
| 1 | 2026-07-09 | NSE | INFY | train | 1 | 1 | 541 | 0 |
| 1 | 2026-07-09 | NSE | ITBEES | train | 1 | 1 | 705 | 0 |
| 1 | 2026-07-09 | NSE | ITC | train | 1 | 1 | 789 | 0 |
| 1 | 2026-07-09 | NSE | JUNIORBEES | train | 1 | 1 | 815 | 0 |
| 1 | 2026-07-09 | NSE | KOTAKBANK | train | 1 | 1 | 760 | 0 |
| 1 | 2026-07-09 | NSE | LT | train | 1 | 1 | 805 | 0 |
| 1 | 2026-07-09 | NSE | M&M | train | 1 | 1 | 592 | 0 |
| 1 | 2026-07-09 | NSE | MARUTI | train | 1 | 1 | 729 | 0 |
| 1 | 2026-07-09 | NSE | NESTLEIND | train | 1 | 1 | 287 | 0 |
| 1 | 2026-07-09 | NSE | NIFTYBEES | train | 1 | 1 | 657 | 0 |
| 1 | 2026-07-09 | NSE | ONGC | train | 1 | 1 | 543 | 0 |
| 1 | 2026-07-09 | NSE | RELIANCE | train | 1 | 1 | 790 | 0 |
| 1 | 2026-07-09 | NSE | SBIN | train | 1 | 1 | 590 | 0 |
| 1 | 2026-07-09 | NSE | SUNPHARMA | train | 1 | 1 | 773 | 0 |
| 1 | 2026-07-09 | NSE | TCS | train | 1 | 1 | 807 | 0 |
| 1 | 2026-07-09 | NSE | TECHM | train | 1 | 1 | 1291 | 0 |
| 1 | 2026-07-09 | NSE | ULTRACEMCO | train | 1 | 1 | 185 | 0 |
| 1 | 2026-07-09 | NSE | WIPRO | train | 1 | 1 | 1976 | 0 |
| 1 | 2026-07-10 | NSE | ADANIPORTS | train | 1 | 1 | 704 | 0 |
| 1 | 2026-07-10 | NSE | AXISBANK | train | 1 | 1 | 565 | 0 |
| 1 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 1 | 1 | 711 | 0 |
| 1 | 2026-07-10 | NSE | BANKBEES | train | 1 | 1 | 593 | 0 |
| 1 | 2026-07-10 | NSE | BHARTIARTL | train | 1 | 1 | 663 | 0 |
| 1 | 2026-07-10 | NSE | BPCL | train | 1 | 1 | 290 | 0 |
| 1 | 2026-07-10 | NSE | BRITANNIA | train | 1 | 1 | 879 | 0 |
| 1 | 2026-07-10 | NSE | CIPLA | train | 1 | 1 | 437 | 0 |
| 1 | 2026-07-10 | NSE | DRREDDY | train | 1 | 1 | 925 | 0 |
| 1 | 2026-07-10 | NSE | GOLDBEES | train | 1 | 1 | 715 | 0 |
| 1 | 2026-07-10 | NSE | HCLTECH | train | 1 | 1 | 1321 | 0 |
| 1 | 2026-07-10 | NSE | HDFCBANK | train | 1 | 1 | 1255 | 0 |
| 1 | 2026-07-10 | NSE | HINDUNILVR | train | 1 | 1 | 533 | 0 |
| 1 | 2026-07-10 | NSE | ICICIBANK | train | 1 | 1 | 612 | 0 |
| 1 | 2026-07-10 | NSE | INFY | train | 1 | 1 | 1263 | 0 |
| 1 | 2026-07-10 | NSE | ITBEES | train | 1 | 1 | 1249 | 0 |
| 1 | 2026-07-10 | NSE | ITC | train | 1 | 1 | 617 | 0 |
| 1 | 2026-07-10 | NSE | JUNIORBEES | train | 1 | 1 | 1165 | 0 |
| 1 | 2026-07-10 | NSE | KOTAKBANK | train | 1 | 1 | 452 | 0 |
| 1 | 2026-07-10 | NSE | LT | train | 1 | 1 | 544 | 0 |
| 1 | 2026-07-10 | NSE | M&M | train | 1 | 1 | 472 | 0 |
| 1 | 2026-07-10 | NSE | MARUTI | train | 1 | 1 | 680 | 0 |
| 1 | 2026-07-10 | NSE | NESTLEIND | train | 1 | 1 | 419 | 0 |
| 1 | 2026-07-10 | NSE | NIFTYBEES | train | 1 | 1 | 697 | 0 |
| 1 | 2026-07-10 | NSE | ONGC | train | 1 | 1 | 693 | 0 |
| 1 | 2026-07-10 | NSE | RELIANCE | train | 1 | 1 | 656 | 0 |
| 1 | 2026-07-10 | NSE | SBIN | train | 1 | 1 | 809 | 0 |
| 1 | 2026-07-10 | NSE | SUNPHARMA | train | 1 | 1 | 443 | 0 |
| 1 | 2026-07-10 | NSE | TCS | train | 1 | 1 | 1457 | 0 |
| 1 | 2026-07-10 | NSE | TECHM | train | 1 | 1 | 683 | 0 |
| 1 | 2026-07-10 | NSE | ULTRACEMCO | train | 1 | 1 | 1107 | 0 |
| 1 | 2026-07-10 | NSE | WIPRO | train | 1 | 1 | 914 | 0 |
| 1 | 2026-07-13 | NSE | ADANIPORTS | validation | 1 | 1 | 709 | 0 |
| 1 | 2026-07-13 | NSE | AXISBANK | validation | 1 | 1 | 565 | 0 |
| 1 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 1 | 1 | 1285 | 0 |
| 1 | 2026-07-13 | NSE | BANKBEES | validation | 1 | 1 | 1133 | 0 |
| 1 | 2026-07-13 | NSE | BHARTIARTL | validation | 1 | 1 | 667 | 0 |
| 1 | 2026-07-13 | NSE | BPCL | validation | 1 | 1 | 1851 | 0 |
| 1 | 2026-07-13 | NSE | BRITANNIA | validation | 1 | 1 | 1368 | 0 |
| 1 | 2026-07-13 | NSE | CIPLA | validation | 1 | 1 | 528 | 0 |
| 1 | 2026-07-13 | NSE | DRREDDY | validation | 1 | 1 | 207 | 0 |
| 1 | 2026-07-13 | NSE | GOLDBEES | validation | 1 | 1 | 661 | 0 |
| 1 | 2026-07-13 | NSE | HCLTECH | validation | 1 | 1 | 1317 | 0 |
| 1 | 2026-07-13 | NSE | HDFCBANK | validation | 1 | 1 | 1513 | 0 |
| 1 | 2026-07-13 | NSE | HINDUNILVR | validation | 1 | 1 | 529 | 0 |
| 1 | 2026-07-13 | NSE | ICICIBANK | validation | 1 | 1 | 1031 | 0 |
| 1 | 2026-07-13 | NSE | INFY | validation | 1 | 1 | 1459 | 0 |
| 1 | 2026-07-13 | NSE | ITBEES | validation | 1 | 1 | 2136 | 0 |
| 1 | 2026-07-13 | NSE | ITC | validation | 1 | 1 | 217 | 0 |
| 1 | 2026-07-13 | NSE | JUNIORBEES | validation | 1 | 1 | 933 | 0 |
| 1 | 2026-07-13 | NSE | KOTAKBANK | validation | 1 | 1 | 322 | 0 |
| 1 | 2026-07-13 | NSE | LT | validation | 1 | 1 | 670 | 0 |
| 1 | 2026-07-13 | NSE | M&M | validation | 1 | 1 | 1139 | 0 |
| 1 | 2026-07-13 | NSE | MARUTI | validation | 1 | 1 | 1359 | 0 |
| 1 | 2026-07-13 | NSE | NESTLEIND | validation | 1 | 1 | 586 | 0 |
| 1 | 2026-07-13 | NSE | NIFTYBEES | validation | 1 | 1 | 980 | 0 |
| 1 | 2026-07-13 | NSE | ONGC | validation | 1 | 1 | 853 | 0 |
| 1 | 2026-07-13 | NSE | RELIANCE | validation | 1 | 1 | 962 | 0 |
| 1 | 2026-07-13 | NSE | SBIN | validation | 1 | 1 | 932 | 0 |
| 1 | 2026-07-13 | NSE | SUNPHARMA | validation | 1 | 1 | 713 | 0 |
| 1 | 2026-07-13 | NSE | TCS | validation | 1 | 1 | 1550 | 0 |
| 1 | 2026-07-13 | NSE | TECHM | validation | 1 | 1 | 954 | 0 |
| 1 | 2026-07-13 | NSE | ULTRACEMCO | validation | 1 | 1 | 1317 | 0 |
| 1 | 2026-07-13 | NSE | WIPRO | validation | 1 | 1 | 1011 | 0 |
| 5 | 2026-07-08 | NSE | ADANIPORTS | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | AXISBANK | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | BANKBEES | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | BHARTIARTL | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | BPCL | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | BRITANNIA | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | CIPLA | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | DRREDDY | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | GOLDBEES | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | HCLTECH | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | HDFCBANK | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | HINDUNILVR | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | ICICIBANK | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | INFY | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | ITBEES | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | ITC | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | JUNIORBEES | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | KOTAKBANK | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | LT | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | M&M | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | MARUTI | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | NESTLEIND | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | NIFTYBEES | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | ONGC | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | RELIANCE | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | SBIN | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | SUNPHARMA | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | TCS | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | TECHM | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | ULTRACEMCO | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-08 | NSE | WIPRO | train | 1 | 1 | 0 | 0 |
| 5 | 2026-07-09 | NSE | ADANIPORTS | train | 1 | 1 | 240 | 0 |
| 5 | 2026-07-09 | NSE | AXISBANK | train | 1 | 1 | 268 | 0 |
| 5 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 1 | 1 | 210 | 0 |
| 5 | 2026-07-09 | NSE | BANKBEES | train | 1 | 1 | 318 | 0 |
| 5 | 2026-07-09 | NSE | BHARTIARTL | train | 1 | 1 | 667 | 0 |
| 5 | 2026-07-09 | NSE | BPCL | train | 1 | 1 | 192 | 0 |
| 5 | 2026-07-09 | NSE | BRITANNIA | train | 1 | 1 | 732 | 0 |
| 5 | 2026-07-09 | NSE | CIPLA | train | 1 | 1 | 209 | 0 |
| 5 | 2026-07-09 | NSE | DRREDDY | train | 1 | 1 | 1216 | 0 |
| 5 | 2026-07-09 | NSE | GOLDBEES | train | 1 | 1 | 316 | 0 |
| 5 | 2026-07-09 | NSE | HCLTECH | train | 1 | 1 | 664 | 0 |
| 5 | 2026-07-09 | NSE | HDFCBANK | train | 1 | 1 | 459 | 0 |
| 5 | 2026-07-09 | NSE | HINDUNILVR | train | 1 | 1 | 428 | 0 |
| 5 | 2026-07-09 | NSE | ICICIBANK | train | 1 | 1 | 441 | 0 |
| 5 | 2026-07-09 | NSE | INFY | train | 1 | 1 | 296 | 0 |
| 5 | 2026-07-09 | NSE | ITBEES | train | 1 | 1 | 431 | 0 |
| 5 | 2026-07-09 | NSE | ITC | train | 1 | 1 | 403 | 0 |
| 5 | 2026-07-09 | NSE | JUNIORBEES | train | 1 | 1 | 325 | 0 |
| 5 | 2026-07-09 | NSE | KOTAKBANK | train | 1 | 1 | 489 | 0 |
| 5 | 2026-07-09 | NSE | LT | train | 1 | 1 | 446 | 0 |
| 5 | 2026-07-09 | NSE | M&M | train | 1 | 1 | 321 | 0 |
| 5 | 2026-07-09 | NSE | MARUTI | train | 1 | 1 | 410 | 0 |
| 5 | 2026-07-09 | NSE | NESTLEIND | train | 1 | 1 | 165 | 0 |
| 5 | 2026-07-09 | NSE | NIFTYBEES | train | 1 | 1 | 237 | 0 |
| 5 | 2026-07-09 | NSE | ONGC | train | 1 | 1 | 220 | 0 |
| 5 | 2026-07-09 | NSE | RELIANCE | train | 1 | 1 | 402 | 0 |
| 5 | 2026-07-09 | NSE | SBIN | train | 1 | 1 | 387 | 0 |
| 5 | 2026-07-09 | NSE | SUNPHARMA | train | 1 | 1 | 487 | 0 |
| 5 | 2026-07-09 | NSE | TCS | train | 1 | 1 | 506 | 0 |
| 5 | 2026-07-09 | NSE | TECHM | train | 1 | 1 | 586 | 0 |
| 5 | 2026-07-09 | NSE | ULTRACEMCO | train | 1 | 1 | 99 | 0 |
| 5 | 2026-07-09 | NSE | WIPRO | train | 1 | 1 | 779 | 0 |
| 5 | 2026-07-10 | NSE | ADANIPORTS | train | 1 | 1 | 379 | 0 |
| 5 | 2026-07-10 | NSE | AXISBANK | train | 1 | 1 | 253 | 0 |
| 5 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 1 | 1 | 435 | 0 |
| 5 | 2026-07-10 | NSE | BANKBEES | train | 1 | 1 | 201 | 0 |
| 5 | 2026-07-10 | NSE | BHARTIARTL | train | 1 | 1 | 256 | 0 |
| 5 | 2026-07-10 | NSE | BPCL | train | 1 | 1 | 155 | 0 |
| 5 | 2026-07-10 | NSE | BRITANNIA | train | 1 | 1 | 509 | 0 |
| 5 | 2026-07-10 | NSE | CIPLA | train | 1 | 1 | 256 | 0 |
| 5 | 2026-07-10 | NSE | DRREDDY | train | 1 | 1 | 504 | 0 |
| 5 | 2026-07-10 | NSE | GOLDBEES | train | 1 | 1 | 311 | 0 |
| 5 | 2026-07-10 | NSE | HCLTECH | train | 1 | 1 | 1091 | 0 |
| 5 | 2026-07-10 | NSE | HDFCBANK | train | 1 | 1 | 525 | 0 |
| 5 | 2026-07-10 | NSE | HINDUNILVR | train | 1 | 1 | 239 | 0 |
| 5 | 2026-07-10 | NSE | ICICIBANK | train | 1 | 1 | 254 | 0 |
| 5 | 2026-07-10 | NSE | INFY | train | 1 | 1 | 671 | 0 |
| 5 | 2026-07-10 | NSE | ITBEES | train | 1 | 1 | 696 | 0 |
| 5 | 2026-07-10 | NSE | ITC | train | 1 | 1 | 364 | 0 |
| 5 | 2026-07-10 | NSE | JUNIORBEES | train | 1 | 1 | 456 | 0 |
| 5 | 2026-07-10 | NSE | KOTAKBANK | train | 1 | 1 | 181 | 0 |
| 5 | 2026-07-10 | NSE | LT | train | 1 | 1 | 199 | 0 |
| 5 | 2026-07-10 | NSE | M&M | train | 1 | 1 | 185 | 0 |
| 5 | 2026-07-10 | NSE | MARUTI | train | 1 | 1 | 281 | 0 |
| 5 | 2026-07-10 | NSE | NESTLEIND | train | 1 | 1 | 260 | 0 |
| 5 | 2026-07-10 | NSE | NIFTYBEES | train | 1 | 1 | 297 | 0 |
| 5 | 2026-07-10 | NSE | ONGC | train | 1 | 1 | 340 | 0 |
| 5 | 2026-07-10 | NSE | RELIANCE | train | 1 | 1 | 241 | 0 |
| 5 | 2026-07-10 | NSE | SBIN | train | 1 | 1 | 383 | 0 |
| 5 | 2026-07-10 | NSE | SUNPHARMA | train | 1 | 1 | 221 | 0 |
| 5 | 2026-07-10 | NSE | TCS | train | 1 | 1 | 815 | 0 |
| 5 | 2026-07-10 | NSE | TECHM | train | 1 | 1 | 456 | 0 |
| 5 | 2026-07-10 | NSE | ULTRACEMCO | train | 1 | 1 | 627 | 0 |
| 5 | 2026-07-10 | NSE | WIPRO | train | 1 | 1 | 532 | 0 |
| 5 | 2026-07-13 | NSE | ADANIPORTS | validation | 1 | 1 | 364 | 0 |
| 5 | 2026-07-13 | NSE | AXISBANK | validation | 1 | 1 | 345 | 0 |
| 5 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 1 | 1 | 969 | 0 |
| 5 | 2026-07-13 | NSE | BANKBEES | validation | 1 | 1 | 427 | 0 |
| 5 | 2026-07-13 | NSE | BHARTIARTL | validation | 1 | 1 | 320 | 0 |
| 5 | 2026-07-13 | NSE | BPCL | validation | 1 | 1 | 901 | 0 |
| 5 | 2026-07-13 | NSE | BRITANNIA | validation | 1 | 1 | 795 | 0 |
| 5 | 2026-07-13 | NSE | CIPLA | validation | 1 | 1 | 328 | 0 |
| 5 | 2026-07-13 | NSE | DRREDDY | validation | 1 | 1 | 96 | 0 |
| 5 | 2026-07-13 | NSE | GOLDBEES | validation | 1 | 1 | 306 | 0 |
| 5 | 2026-07-13 | NSE | HCLTECH | validation | 1 | 1 | 961 | 0 |
| 5 | 2026-07-13 | NSE | HDFCBANK | validation | 1 | 1 | 677 | 0 |
| 5 | 2026-07-13 | NSE | HINDUNILVR | validation | 1 | 1 | 257 | 0 |
| 5 | 2026-07-13 | NSE | ICICIBANK | validation | 1 | 1 | 488 | 0 |
| 5 | 2026-07-13 | NSE | INFY | validation | 1 | 1 | 789 | 0 |
| 5 | 2026-07-13 | NSE | ITBEES | validation | 1 | 1 | 950 | 0 |
| 5 | 2026-07-13 | NSE | ITC | validation | 1 | 1 | 119 | 0 |
| 5 | 2026-07-13 | NSE | JUNIORBEES | validation | 1 | 1 | 401 | 0 |
| 5 | 2026-07-13 | NSE | KOTAKBANK | validation | 1 | 1 | 176 | 0 |
| 5 | 2026-07-13 | NSE | LT | validation | 1 | 1 | 320 | 0 |
| 5 | 2026-07-13 | NSE | M&M | validation | 1 | 1 | 552 | 0 |
| 5 | 2026-07-13 | NSE | MARUTI | validation | 1 | 1 | 580 | 0 |
| 5 | 2026-07-13 | NSE | NESTLEIND | validation | 1 | 1 | 424 | 0 |
| 5 | 2026-07-13 | NSE | NIFTYBEES | validation | 1 | 1 | 447 | 0 |
| 5 | 2026-07-13 | NSE | ONGC | validation | 1 | 1 | 507 | 0 |
| 5 | 2026-07-13 | NSE | RELIANCE | validation | 1 | 1 | 587 | 0 |
| 5 | 2026-07-13 | NSE | SBIN | validation | 1 | 1 | 499 | 0 |
| 5 | 2026-07-13 | NSE | SUNPHARMA | validation | 1 | 1 | 387 | 0 |
| 5 | 2026-07-13 | NSE | TCS | validation | 1 | 1 | 911 | 0 |
| 5 | 2026-07-13 | NSE | TECHM | validation | 1 | 1 | 713 | 0 |
| 5 | 2026-07-13 | NSE | ULTRACEMCO | validation | 1 | 1 | 764 | 0 |
| 5 | 2026-07-13 | NSE | WIPRO | validation | 1 | 1 | 712 | 0 |
| 15 | 2026-07-08 | NSE | ADANIPORTS | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | AXISBANK | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | BANKBEES | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | BHARTIARTL | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | BPCL | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | BRITANNIA | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | CIPLA | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | DRREDDY | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | GOLDBEES | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | HCLTECH | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | HDFCBANK | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | HINDUNILVR | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | ICICIBANK | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | INFY | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | ITBEES | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | ITC | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | JUNIORBEES | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | KOTAKBANK | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | LT | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | M&M | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | MARUTI | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | NESTLEIND | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | NIFTYBEES | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | ONGC | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | RELIANCE | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | SBIN | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | SUNPHARMA | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | TCS | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | TECHM | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | ULTRACEMCO | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-08 | NSE | WIPRO | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | ADANIPORTS | train | 1 | 1 | 5 | 0 |
| 15 | 2026-07-09 | NSE | AXISBANK | train | 1 | 1 | 1 | 0 |
| 15 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 1 | 1 | 11 | 0 |
| 15 | 2026-07-09 | NSE | BANKBEES | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | BHARTIARTL | train | 1 | 1 | 14 | 0 |
| 15 | 2026-07-09 | NSE | BPCL | train | 1 | 1 | 8 | 0 |
| 15 | 2026-07-09 | NSE | BRITANNIA | train | 1 | 1 | 175 | 0 |
| 15 | 2026-07-09 | NSE | CIPLA | train | 1 | 1 | 10 | 0 |
| 15 | 2026-07-09 | NSE | DRREDDY | train | 1 | 1 | 525 | 0 |
| 15 | 2026-07-09 | NSE | GOLDBEES | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | HCLTECH | train | 1 | 1 | 129 | 0 |
| 15 | 2026-07-09 | NSE | HDFCBANK | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | HINDUNILVR | train | 1 | 1 | 52 | 0 |
| 15 | 2026-07-09 | NSE | ICICIBANK | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | INFY | train | 1 | 1 | 2 | 0 |
| 15 | 2026-07-09 | NSE | ITBEES | train | 1 | 1 | 85 | 0 |
| 15 | 2026-07-09 | NSE | ITC | train | 1 | 1 | 4 | 0 |
| 15 | 2026-07-09 | NSE | JUNIORBEES | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | KOTAKBANK | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | LT | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | M&M | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | MARUTI | train | 1 | 1 | 3 | 0 |
| 15 | 2026-07-09 | NSE | NESTLEIND | train | 1 | 1 | 10 | 0 |
| 15 | 2026-07-09 | NSE | NIFTYBEES | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | ONGC | train | 1 | 1 | 1 | 0 |
| 15 | 2026-07-09 | NSE | RELIANCE | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | SBIN | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-09 | NSE | SUNPHARMA | train | 1 | 1 | 90 | 0 |
| 15 | 2026-07-09 | NSE | TCS | train | 1 | 1 | 10 | 0 |
| 15 | 2026-07-09 | NSE | TECHM | train | 1 | 1 | 43 | 0 |
| 15 | 2026-07-09 | NSE | ULTRACEMCO | train | 1 | 1 | 2 | 0 |
| 15 | 2026-07-09 | NSE | WIPRO | train | 1 | 1 | 180 | 0 |
| 15 | 2026-07-10 | NSE | ADANIPORTS | train | 1 | 1 | 2 | 0 |
| 15 | 2026-07-10 | NSE | AXISBANK | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 1 | 1 | 7 | 0 |
| 15 | 2026-07-10 | NSE | BANKBEES | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | BHARTIARTL | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | BPCL | train | 1 | 1 | 5 | 0 |
| 15 | 2026-07-10 | NSE | BRITANNIA | train | 1 | 1 | 70 | 0 |
| 15 | 2026-07-10 | NSE | CIPLA | train | 1 | 1 | 9 | 0 |
| 15 | 2026-07-10 | NSE | DRREDDY | train | 1 | 1 | 2 | 0 |
| 15 | 2026-07-10 | NSE | GOLDBEES | train | 1 | 1 | 1 | 0 |
| 15 | 2026-07-10 | NSE | HCLTECH | train | 1 | 1 | 131 | 0 |
| 15 | 2026-07-10 | NSE | HDFCBANK | train | 1 | 1 | 1 | 0 |
| 15 | 2026-07-10 | NSE | HINDUNILVR | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | ICICIBANK | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | INFY | train | 1 | 1 | 1 | 0 |
| 15 | 2026-07-10 | NSE | ITBEES | train | 1 | 1 | 56 | 0 |
| 15 | 2026-07-10 | NSE | ITC | train | 1 | 1 | 1 | 0 |
| 15 | 2026-07-10 | NSE | JUNIORBEES | train | 1 | 1 | 1 | 0 |
| 15 | 2026-07-10 | NSE | KOTAKBANK | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | LT | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | M&M | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | MARUTI | train | 1 | 1 | 2 | 0 |
| 15 | 2026-07-10 | NSE | NESTLEIND | train | 1 | 1 | 21 | 0 |
| 15 | 2026-07-10 | NSE | NIFTYBEES | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | ONGC | train | 1 | 1 | 1 | 0 |
| 15 | 2026-07-10 | NSE | RELIANCE | train | 1 | 1 | 0 | 0 |
| 15 | 2026-07-10 | NSE | SBIN | train | 1 | 1 | 1 | 0 |
| 15 | 2026-07-10 | NSE | SUNPHARMA | train | 1 | 1 | 2 | 0 |
| 15 | 2026-07-10 | NSE | TCS | train | 1 | 1 | 1 | 0 |
| 15 | 2026-07-10 | NSE | TECHM | train | 1 | 1 | 28 | 0 |
| 15 | 2026-07-10 | NSE | ULTRACEMCO | train | 1 | 1 | 28 | 0 |
| 15 | 2026-07-10 | NSE | WIPRO | train | 1 | 1 | 61 | 0 |
| 15 | 2026-07-13 | NSE | ADANIPORTS | validation | 1 | 1 | 6 | 0 |
| 15 | 2026-07-13 | NSE | AXISBANK | validation | 1 | 1 | 3 | 0 |
| 15 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 1 | 1 | 66 | 0 |
| 15 | 2026-07-13 | NSE | BANKBEES | validation | 1 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | BHARTIARTL | validation | 1 | 1 | 1 | 0 |
| 15 | 2026-07-13 | NSE | BPCL | validation | 1 | 1 | 47 | 0 |
| 15 | 2026-07-13 | NSE | BRITANNIA | validation | 1 | 1 | 77 | 0 |
| 15 | 2026-07-13 | NSE | CIPLA | validation | 1 | 1 | 22 | 0 |
| 15 | 2026-07-13 | NSE | DRREDDY | validation | 1 | 1 | 1 | 0 |
| 15 | 2026-07-13 | NSE | GOLDBEES | validation | 1 | 1 | 4 | 0 |
| 15 | 2026-07-13 | NSE | HCLTECH | validation | 1 | 1 | 179 | 0 |
| 15 | 2026-07-13 | NSE | HDFCBANK | validation | 1 | 1 | 1 | 0 |
| 15 | 2026-07-13 | NSE | HINDUNILVR | validation | 1 | 1 | 4 | 0 |
| 15 | 2026-07-13 | NSE | ICICIBANK | validation | 1 | 1 | 1 | 0 |
| 15 | 2026-07-13 | NSE | INFY | validation | 1 | 1 | 1 | 0 |
| 15 | 2026-07-13 | NSE | ITBEES | validation | 1 | 1 | 151 | 0 |
| 15 | 2026-07-13 | NSE | ITC | validation | 1 | 1 | 2 | 0 |
| 15 | 2026-07-13 | NSE | JUNIORBEES | validation | 1 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | KOTAKBANK | validation | 1 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | LT | validation | 1 | 1 | 1 | 0 |
| 15 | 2026-07-13 | NSE | M&M | validation | 1 | 1 | 0 | 0 |
| 15 | 2026-07-13 | NSE | MARUTI | validation | 1 | 1 | 1 | 0 |
| 15 | 2026-07-13 | NSE | NESTLEIND | validation | 1 | 1 | 31 | 0 |
| 15 | 2026-07-13 | NSE | NIFTYBEES | validation | 1 | 1 | 1 | 0 |
| 15 | 2026-07-13 | NSE | ONGC | validation | 1 | 1 | 6 | 0 |
| 15 | 2026-07-13 | NSE | RELIANCE | validation | 1 | 1 | 4 | 0 |
| 15 | 2026-07-13 | NSE | SBIN | validation | 1 | 1 | 2 | 0 |
| 15 | 2026-07-13 | NSE | SUNPHARMA | validation | 1 | 1 | 3 | 0 |
| 15 | 2026-07-13 | NSE | TCS | validation | 1 | 1 | 3 | 0 |
| 15 | 2026-07-13 | NSE | TECHM | validation | 1 | 1 | 106 | 0 |
| 15 | 2026-07-13 | NSE | ULTRACEMCO | validation | 1 | 1 | 29 | 0 |
| 15 | 2026-07-13 | NSE | WIPRO | validation | 1 | 1 | 92 | 0 |

## Train/Validation Model Metrics

| phase219_model_fit_id | phase218_model_spec_id | model_family | target_label | horizon_sec | train_rows_used_for_fit | test_rows_used | strategy_replay_allowed | promotion_allowed | split_role | rows | positive_rate | prediction_mean | mse | base_rate_mse | mse_improvement_vs_base | binary_accuracy | correlation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_down_conditional_label | 1 | 52764 | 0 | 0 | 0 | train | 52764 | 0.176219 | 0.176232 | 0.143431 | 0.145166 | 0.00173447 | 0.823781 | 0.109309 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_down_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.193375 | 0.121891 | 0.157764 | 0.155981 | -0.00178327 | 0.806625 | 0.153263 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_down_conditional_label | 1 | 52764 | 0 | 0 | 0 | train | 52764 | 0.176219 | 0.176228 | 0.143638 | 0.145166 | 0.00152723 | 0.823781 | 0.102571 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_down_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.193375 | 0.125369 | 0.158085 | 0.155981 | -0.00210376 | 0.806625 | 0.132243 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 1 | 52764 | 0 | 0 | 0 | train | 52764 | 0.176219 | 0.176231 | 0.143243 | 0.145166 | 0.00192217 | 0.823781 | 0.115071 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.193375 | 0.176223 | 0.152628 | 0.155981 | 0.00335315 | 0.806625 | 0.159248 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_up_conditional_label | 1 | 52764 | 0 | 0 | 0 | train | 52764 | 0.181165 | 0.181176 | 0.146466 | 0.148344 | 0.0018783 | 0.818835 | 0.112526 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_up_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.184824 | 0.140025 | 0.150565 | 0.150664 | 9.87065e-05 | 0.815176 | 0.119193 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_up_conditional_label | 1 | 52764 | 0 | 0 | 0 | train | 52764 | 0.181165 | 0.181177 | 0.146987 | 0.148344 | 0.0013573 | 0.818835 | 0.0956565 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_up_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.184824 | 0.134141 | 0.150812 | 0.150664 | -0.000148273 | 0.815176 | 0.133777 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 1 | 52764 | 0 | 0 | 0 | train | 52764 | 0.181165 | 0.181166 | 0.146268 | 0.148344 | 0.0020761 | 0.818835 | 0.118301 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.184824 | 0.181165 | 0.14811 | 0.150664 | 0.00255374 | 0.815176 | 0.132913 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_vol_expansion_conditional_label | 1 | 52764 | 0 | 0 | 0 | train | 52764 | 0.356436 | 0.356457 | 0.223465 | 0.229389 | 0.0059249 | 0.642123 | 0.160717 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_vol_expansion_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.378231 | 0.249476 | 0.242535 | 0.235172 | -0.00736265 | 0.621801 | 0.206414 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | 52764 | 0 | 0 | 0 | train | 52764 | 0.356436 | 0.356457 | 0.223541 | 0.229389 | 0.00584807 | 0.641858 | 0.159671 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.378231 | 0.247155 | 0.242655 | 0.235172 | -0.00748324 | 0.621801 | 0.212958 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | 52764 | 0 | 0 | 0 | train | 52764 | 0.356436 | 0.356439 | 0.222746 | 0.229389 | 0.00664335 | 0.642559 | 0.170179 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | 52764 | 0 | 0 | 0 | validation | 31457 | 0.378231 | 0.356435 | 0.225079 | 0.235172 | 0.0100934 | 0.622405 | 0.220575 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_down_conditional_label | 5 | 25922 | 0 | 0 | 0 | train | 25922 | 0.33161 | 0.33161 | 0.218179 | 0.221645 | 0.00346592 | 0.668274 | 0.125049 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_down_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.340382 | 0.248742 | 0.227981 | 0.224522 | -0.00345884 | 0.659618 | 0.152627 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_down_conditional_label | 5 | 25922 | 0 | 0 | 0 | train | 25922 | 0.33161 | 0.33161 | 0.218796 | 0.221645 | 0.00284928 | 0.668313 | 0.113381 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_down_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.340382 | 0.255113 | 0.22883 | 0.224522 | -0.00430795 | 0.659618 | 0.116438 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 5 | 25922 | 0 | 0 | 0 | train | 25922 | 0.33161 | 0.331613 | 0.217837 | 0.221645 | 0.00380766 | 0.66839 | 0.131069 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.340382 | 0.331609 | 0.219307 | 0.224522 | 0.00521501 | 0.65956 | 0.157466 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_up_conditional_label | 5 | 25922 | 0 | 0 | 0 | train | 25922 | 0.329488 | 0.329488 | 0.216311 | 0.220926 | 0.00461525 | 0.670049 | 0.144535 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_up_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.33224 | 0.274906 | 0.219823 | 0.221857 | 0.00203356 | 0.66776 | 0.157643 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_up_conditional_label | 5 | 25922 | 0 | 0 | 0 | train | 25922 | 0.329488 | 0.329488 | 0.217821 | 0.220926 | 0.00310481 | 0.67055 | 0.118548 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_up_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.33224 | 0.265815 | 0.221588 | 0.221857 | 0.000268159 | 0.66776 | 0.150913 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 5 | 25922 | 0 | 0 | 0 | train | 25922 | 0.329488 | 0.329488 | 0.216099 | 0.220926 | 0.00482661 | 0.670666 | 0.147808 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.33224 | 0.32949 | 0.216399 | 0.221857 | 0.00545801 | 0.66776 | 0.160105 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_vol_expansion_conditional_label | 5 | 25922 | 0 | 0 | 0 | train | 25922 | 0.607013 | 0.607013 | 0.23098 | 0.238548 | 0.00756806 | 0.623216 | 0.178117 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_vol_expansion_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.622247 | 0.475241 | 0.248548 | 0.235056 | -0.0134922 | 0.545513 | 0.190846 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | 25922 | 0 | 0 | 0 | train | 25922 | 0.607013 | 0.607013 | 0.231087 | 0.238548 | 0.00746077 | 0.622329 | 0.176849 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.622247 | 0.472221 | 0.248532 | 0.235056 | -0.0134762 | 0.550082 | 0.202966 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | 25922 | 0 | 0 | 0 | train | 25922 | 0.607013 | 0.607013 | 0.230075 | 0.238548 | 0.00847358 | 0.625376 | 0.188471 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | 25922 | 0 | 0 | 0 | validation | 17072 | 0.622247 | 0.607013 | 0.226014 | 0.235056 | 0.00904191 | 0.629276 | 0.20407 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_vol_expansion_conditional_label | 15 | 1792 | 0 | 0 | 0 | train | 1792 | 0.660714 | 0.660714 | 0.220995 | 0.224171 | 0.0031761 | 0.660714 | 0.11903 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | class_weighted_regularized_logistic_classification | event_surprise_vol_expansion_conditional_label | 15 | 1792 | 0 | 0 | 0 | validation | 845 | 0.693491 | 0.4954 | 0.250753 | 0.212561 | -0.038192 | 0.485207 | 0.0705274 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_vol_expansion_conditional_label | 15 | 1792 | 0 | 0 | 0 | train | 1792 | 0.660714 | 0.660714 | 0.220119 | 0.224171 | 0.00405198 | 0.66183 | 0.134445 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_only_sparse_classification_diagnostic | event_surprise_vol_expansion_conditional_label | 15 | 1792 | 0 | 0 | 0 | validation | 845 | 0.693491 | 0.490068 | 0.25383 | 0.212561 | -0.041269 | 0.486391 | 0.0468028 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 15 | 1792 | 0 | 0 | 0 | train | 1792 | 0.660714 | 0.660714 | 0.220741 | 0.224171 | 0.00342979 | 0.660714 | 0.123693 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 15 | 1792 | 0 | 0 | 0 | validation | 845 | 0.693491 | 0.660673 | 0.214127 | 0.212561 | -0.00156582 | 0.693491 | 0.0267188 |

## Model Coefficient Ledger

| phase219_model_fit_id | phase218_model_spec_id | target_label | horizon_sec | coefficient_name | coefficient_value | model_fit_execution | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 1 | intercept | 0.176219 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 1 | cross_symbol_arrival_count | -0.00337085 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 1 | cross_symbol_arrival_share | -0.00337085 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 1 | depth_refresh_count | -0.053836 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 1 | phase176_universe_symbols | -5.97177e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 1 | quote_churn_count | 0.0708092 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 1 | receive_event_count | 0.00739832 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 1 | receive_event_rate_baseline_days | -0.0173966 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 1 | receive_event_rate_zscore | 0.00546675 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 1 | stale_quote_duration_ms | -0.0128767 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 1 | top5_qty_imbalance | -0.0144873 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | intercept | 0.176219 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | cross_symbol_arrival_count | -0.00347702 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | cross_symbol_arrival_share | -0.00347702 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | depth_refresh_count | -0.0536658 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | phase176_universe_symbols | -1.52866e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | quote_churn_count | 0.0710262 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | receive_event_count | 0.00684367 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | receive_event_rate_baseline_days | -0.016959 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | receive_event_rate_zscore | 0.00552838 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | stale_quote_duration_ms | -0.0128355 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | top5_qty_imbalance | 0.00184285 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | intercept | 0.176219 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | cross_symbol_arrival_count | -0.00765411 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | cross_symbol_arrival_share | -0.00765411 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | depth_refresh_count | -0.068201 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | phase176_universe_symbols | 2.70447e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | quote_churn_count | 0.0687841 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | receive_event_count | 0.0176704 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | receive_event_rate_baseline_days | -0.0207029 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | receive_event_rate_zscore | 0.0114374 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | stale_quote_duration_ms | -0.0182364 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 1 | top5_qty_imbalance | -0.0147616 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 1 | intercept | 0.181165 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 1 | cross_symbol_arrival_count | -0.00549799 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 1 | cross_symbol_arrival_share | -0.00549799 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 1 | depth_refresh_count | -0.0288543 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 1 | phase176_universe_symbols | -1.80676e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 1 | quote_churn_count | 0.0540225 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 1 | receive_event_count | 0.000388299 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 1 | receive_event_rate_baseline_days | -0.0146361 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 1 | receive_event_rate_zscore | -0.00190883 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 1 | stale_quote_duration_ms | -0.0143704 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 1 | top5_qty_imbalance | 0.0228752 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | intercept | 0.181165 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | cross_symbol_arrival_count | -0.00535237 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | cross_symbol_arrival_share | -0.00535237 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | depth_refresh_count | -0.0300868 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | phase176_universe_symbols | -1.23186e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | quote_churn_count | 0.0544751 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | receive_event_count | 0.00159854 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | receive_event_rate_baseline_days | -0.0154937 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | receive_event_rate_zscore | -0.00214079 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | stale_quote_duration_ms | -0.0144229 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | top5_qty_imbalance | 0.000895089 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | intercept | 0.181165 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | cross_symbol_arrival_count | -0.00915885 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | cross_symbol_arrival_share | -0.00915885 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | depth_refresh_count | -0.0489247 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | phase176_universe_symbols | -1.17572e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | quote_churn_count | 0.0539096 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | receive_event_count | 0.0192733 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | receive_event_rate_baseline_days | -0.0178958 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | receive_event_rate_zscore | -0.00175306 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | stale_quote_duration_ms | -0.0205697 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 1 | top5_qty_imbalance | 0.0226181 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 1 | intercept | 0.356436 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 1 | cross_symbol_arrival_count | -0.00941494 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 1 | cross_symbol_arrival_share | -0.00941494 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 1 | depth_refresh_count | -0.0873552 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 1 | phase176_universe_symbols | -8.06353e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 1 | quote_churn_count | 0.126498 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 1 | receive_event_count | 0.0100819 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 1 | receive_event_rate_baseline_days | -0.0356797 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 1 | receive_event_rate_zscore | 0.00424139 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 1 | stale_quote_duration_ms | -0.0268395 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 1 | top5_qty_imbalance | 0.00886834 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | intercept | 0.356436 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | cross_symbol_arrival_count | -0.00936144 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | cross_symbol_arrival_share | -0.00936144 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | depth_refresh_count | -0.0879626 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | phase176_universe_symbols | -2.6434e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | quote_churn_count | 0.126781 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | receive_event_count | 0.010596 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | receive_event_rate_baseline_days | -0.0360345 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | receive_event_rate_zscore | 0.00413336 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | stale_quote_duration_ms | -0.0268582 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | top5_qty_imbalance | 0.000858548 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | intercept | 0.356436 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | cross_symbol_arrival_count | -0.0171831 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | cross_symbol_arrival_share | -0.0171831 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | depth_refresh_count | -0.118049 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | phase176_universe_symbols | 1.33234e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | quote_churn_count | 0.12369 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | receive_event_count | 0.0367764 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | receive_event_rate_baseline_days | -0.0423363 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | receive_event_rate_zscore | 0.00983499 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | stale_quote_duration_ms | -0.0369533 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 1 | top5_qty_imbalance | 0.00840683 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 5 | intercept | 0.33161 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 5 | cross_symbol_arrival_count | -0.00142502 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 5 | cross_symbol_arrival_share | -0.00142502 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 5 | depth_refresh_count | -0.0726855 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 5 | phase176_universe_symbols | -8.77346e-14 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 5 | quote_churn_count | 0.10957 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 5 | receive_event_count | -0.00253069 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 5 | receive_event_rate_baseline_days | -0.0264464 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 5 | receive_event_rate_zscore | 0.0124116 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 5 | stale_quote_duration_ms | -0.00848518 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_down_conditional_label | 5 | top5_qty_imbalance | -0.0252211 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | intercept | 0.33161 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | cross_symbol_arrival_count | -0.00160251 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | cross_symbol_arrival_share | -0.00160251 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | depth_refresh_count | -0.0698873 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | phase176_universe_symbols | -1.12898e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | quote_churn_count | 0.108207 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | receive_event_count | -0.00451156 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | receive_event_rate_baseline_days | -0.0253889 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | receive_event_rate_zscore | 0.0127015 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | stale_quote_duration_ms | -0.00850296 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | top5_qty_imbalance | -0.00422534 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | intercept | 0.33161 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | cross_symbol_arrival_count | -0.00635762 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | cross_symbol_arrival_share | -0.00635762 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | depth_refresh_count | -0.0948746 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | phase176_universe_symbols | 1.05208e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | quote_churn_count | 0.111791 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | receive_event_count | 0.0195476 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | receive_event_rate_baseline_days | -0.0285519 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | receive_event_rate_zscore | 0.00920487 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | stale_quote_duration_ms | -0.0123608 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_down_conditional_label | 5 | top5_qty_imbalance | -0.025788 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 5 | intercept | 0.329488 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 5 | cross_symbol_arrival_count | -8.31582e-05 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 5 | cross_symbol_arrival_share | -8.31582e-05 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 5 | depth_refresh_count | 0.00449404 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 5 | phase176_universe_symbols | -1.08854e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 5 | quote_churn_count | 0.0358214 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 5 | receive_event_count | 0.00861518 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 5 | receive_event_rate_baseline_days | -0.0211802 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 5 | receive_event_rate_zscore | 0.00121799 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 5 | stale_quote_duration_ms | -0.00438222 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_up_conditional_label | 5 | top5_qty_imbalance | 0.0397382 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | intercept | 0.329488 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | cross_symbol_arrival_count | 0.00010966 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | cross_symbol_arrival_share | 0.00010966 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | depth_refresh_count | 0.00246497 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | phase176_universe_symbols | -2.27766e-14 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | quote_churn_count | 0.0359828 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | receive_event_count | 0.0106807 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | receive_event_rate_baseline_days | -0.0223347 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | receive_event_rate_zscore | 0.00100715 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | stale_quote_duration_ms | -0.00446936 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | top5_qty_imbalance | -0.00804567 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | intercept | 0.329488 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | cross_symbol_arrival_count | -0.00292342 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | cross_symbol_arrival_share | -0.00292342 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | depth_refresh_count | -0.0251987 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | phase176_universe_symbols | -6.28547e-14 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | quote_churn_count | 0.0410926 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | receive_event_count | 0.03381 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | receive_event_rate_baseline_days | -0.0211903 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | receive_event_rate_zscore | 0.00529049 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | stale_quote_duration_ms | -0.0118055 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_up_conditional_label | 5 | top5_qty_imbalance | 0.0395386 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 5 | intercept | 0.607013 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 5 | cross_symbol_arrival_count | -0.00225292 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 5 | cross_symbol_arrival_share | -0.00225292 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 5 | depth_refresh_count | -0.0609671 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 5 | phase176_universe_symbols | -1.48944e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 5 | quote_churn_count | 0.114256 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 5 | receive_event_count | 0.0106034 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 5 | receive_event_rate_baseline_days | -0.0453935 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 5 | receive_event_rate_zscore | 0.0104321 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 5 | stale_quote_duration_ms | -0.0109321 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 5 | top5_qty_imbalance | 0.015591 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | intercept | 0.607013 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | cross_symbol_arrival_count | -0.00222748 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | cross_symbol_arrival_share | -0.00222748 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | depth_refresh_count | -0.0603873 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | phase176_universe_symbols | -1.01925e-13 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | quote_churn_count | 0.11317 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | receive_event_count | 0.0108035 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | receive_event_rate_baseline_days | -0.0455506 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | receive_event_rate_zscore | 0.0104916 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | stale_quote_duration_ms | -0.0110329 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | top5_qty_imbalance | -0.011658 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | intercept | 0.607013 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | cross_symbol_arrival_count | -0.00836864 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | cross_symbol_arrival_share | -0.00836864 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | depth_refresh_count | -0.102568 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | phase176_universe_symbols | 2.91503e-14 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | quote_churn_count | 0.119961 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | receive_event_count | 0.0486509 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | receive_event_rate_baseline_days | -0.0470508 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | receive_event_rate_zscore | 0.0132128 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | stale_quote_duration_ms | -0.0200235 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 5 | top5_qty_imbalance | 0.0147283 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 15 | intercept | 0.660714 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 15 | cross_symbol_arrival_count | -0.00800156 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 15 | cross_symbol_arrival_share | -0.00800156 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 15 | depth_refresh_count | 0.00309351 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 15 | phase176_universe_symbols | -9.73395e-16 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 15 | quote_churn_count | 0.0134321 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 15 | receive_event_count | 0.00622355 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 15 | receive_event_rate_baseline_days | -0.0398805 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 15 | receive_event_rate_zscore | 0.0212227 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 15 | stale_quote_duration_ms | 0.00706008 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_BALANCED_LOGIT | event_surprise_vol_expansion_conditional_label | 15 | top5_qty_imbalance | 0.00983517 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | intercept | 0.660714 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | cross_symbol_arrival_count | -0.00743966 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | cross_symbol_arrival_share | -0.00743966 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | depth_refresh_count | 0.00324519 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | phase176_universe_symbols | 1.27655e-14 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | quote_churn_count | 0.0140763 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | receive_event_count | 0.00049502 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | receive_event_rate_baseline_days | -0.0394103 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | receive_event_rate_zscore | 0.0218912 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | stale_quote_duration_ms | 0.00588906 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | top5_qty_imbalance | -0.0315798 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | intercept | 0.660714 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | cross_symbol_arrival_count | -0.0117366 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | cross_symbol_arrival_share | -0.0117366 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | depth_refresh_count | 0.0564477 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | phase176_universe_symbols | 4.16877e-15 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | quote_churn_count | -0.0456109 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | receive_event_count | 0.0109053 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | receive_event_rate_baseline_days | -0.043359 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | receive_event_rate_zscore | 0.0184985 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | stale_quote_duration_ms | 0.00458104 | 1 | 0 | 0 |
| P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC | event_surprise_vol_expansion_conditional_label | 15 | top5_qty_imbalance | 0.0102644 | 1 | 0 | 0 |

## Control Metrics

| phase219_control_id | phase219_model_fit_id | control_type | validation_rows | validation_mse | validation_binary_accuracy | test_rows_used | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | event_only_base_rate | 31457 | 0.155981 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H1s | event_time_shuffle | 31457 | 0.156819 | 0.806625 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | event_only_base_rate | 31457 | 0.155981 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | event_time_shuffle | 31457 | 0.156808 | 0.806625 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | event_only_base_rate | 31457 | 0.155981 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | event_time_shuffle | 31457 | 0.156552 | 0.806625 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | event_only_base_rate | 31457 | 0.150664 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H1s | event_time_shuffle | 31457 | 0.150576 | 0.815176 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | event_only_base_rate | 31457 | 0.150664 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | event_time_shuffle | 31457 | 0.150594 | 0.815176 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | event_only_base_rate | 31457 | 0.150664 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H1s | event_time_shuffle | 31457 | 0.150533 | 0.815176 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | event_only_base_rate | 31457 | 0.235172 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H1s | event_time_shuffle | 31457 | 0.236355 | 0.621769 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | event_only_base_rate | 31457 | 0.235172 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | event_time_shuffle | 31457 | 0.236384 | 0.621769 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | event_only_base_rate | 31457 | 0.235172 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | event_time_shuffle | 31457 | 0.235809 | 0.621769 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | event_only_base_rate | 17072 | 0.224522 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_down_conditional_label_H5s | event_time_shuffle | 17072 | 0.224407 | 0.659618 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | event_only_base_rate | 17072 | 0.224522 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | event_time_shuffle | 17072 | 0.224651 | 0.659618 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | event_only_base_rate | 17072 | 0.224522 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | event_time_shuffle | 17072 | 0.224275 | 0.659618 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | event_only_base_rate | 17072 | 0.221857 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_up_conditional_label_H5s | event_time_shuffle | 17072 | 0.221941 | 0.66776 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | event_only_base_rate | 17072 | 0.221857 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | event_time_shuffle | 17072 | 0.22216 | 0.66776 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | event_only_base_rate | 17072 | 0.221857 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | event_time_shuffle | 17072 | 0.221826 | 0.66776 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | event_only_base_rate | 17072 | 0.235056 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H5s | event_time_shuffle | 17072 | 0.235622 | 0.622247 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | event_only_base_rate | 17072 | 0.235056 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | event_time_shuffle | 17072 | 0.23512 | 0.622247 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | event_only_base_rate | 17072 | 0.235056 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | event_time_shuffle | 17072 | 0.235916 | 0.622247 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | event_only_base_rate | 845 | 0.212561 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | P219_P218_EVENT_ONLY_BALANCED_LOGIT_event_surprise_vol_expansion_conditional_label_H15s | event_time_shuffle | 845 | 0.211617 | 0.693491 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | event_only_base_rate | 845 | 0.212561 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P219_P218_EVENT_ONLY_COMPLEMENT_NB_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | event_time_shuffle | 845 | 0.211661 | 0.693491 | 0 | 0 |
| P219_BASE_RATE_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | event_only_base_rate | 845 | 0.212561 |  | 0 | 0 |
| P219_SHUFFLED_P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H15s | event_time_shuffle | 845 | 0.21321 | 0.693491 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase219 | allowed_in_phase219 | rationale |
| --- | --- | --- | --- |
| strategy_replay | 0 | 0 | Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed. |
| test_replay_execution | 0 | 0 | Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed. |
| test_result | 0 | 0 | Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed. |
| promotion | 0 | 0 | Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed. |
| paper_live_acceptance | 0 | 0 | Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed. |
| order_arrival | 0 | 0 | Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed. |
| fill_model | 0 | 0 | Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed. |
| pnl_replay | 0 | 0 | Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed. |
| profitability_claim | 0 | 0 | Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed. |
| threshold_widening | 0 | 0 | Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed. |
| row_level_design_matrix_export | 0 | 0 | Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed. |
| row_level_prediction_export | 0 | 0 | Phase219 fits train/validation event-only dry-run models and emits aggregate diagnostics only; no replay, sealed test, fills, P&L, promotion, or paper/live artifact is allowed. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P219_PHASE218_COMPLETE_AND_PRECOMMITTED | True | phase218_complete=1; dry_run_precommitted=1 | hard |
| P219_EVENT_ONLY_DESIGN_MATRIX_JOINED | True | event_only_joined_rows=129852 | hard |
| P219_MODEL_FITS_RECORDED | True | model_fit_rows=21 | hard |
| P219_VALIDATION_METRICS_RECORDED | True | validation_metric_rows=21 | hard |
| P219_CONTROLS_RECORDED | True | control_rows=42 | hard |
| P219_TEST_REPLAY_AND_TEST_ROWS_CLOSED | True | test_rows_used=0 | hard |
| P219_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; replay_flags=0 | hard |

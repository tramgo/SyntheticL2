# Phase210 Train/Validation Model-fit Dry Run

Generated UTC: 2026-07-28T21:11:42.417147+00:00

Phase210 joins Phase176 receive-flow feature partitions to Phase181 receive-flow labels and fits train-only ridge dry-run models.
It scores train and validation aggregates, records shuffled-target controls, and exports only aggregate metrics/coefficient ledgers.
It does not use sealed test rows, run strategy replay, emit orders/fills/P&L, promote anything, or open paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase210_design_matrix_partition_rows | 512 | Train/validation joined partition rows |
| phase210_design_matrix_joined_rows | 1641001 | Joined train/validation design-matrix rows |
| phase210_model_fit_rows | 12 | Unique model/horizon fits |
| phase210_metric_rows | 24 | Train/validation metric rows |
| phase210_validation_metric_rows | 12 | Validation metric rows |
| phase210_coefficient_rows | 132 | Coefficient rows |
| phase210_negative_control_rows | 12 | Negative-control rows |
| phase210_forbidden_execution_rows | 11 | Forbidden execution rows |
| phase210_gate_rows | 7 | Gates evaluated |
| phase210_hard_gate_rows | 7 | Hard gates evaluated |
| phase210_hard_gate_pass_rows | 7 | Hard gates passed |
| phase210_train_validation_model_fit_dry_run_complete | 1 | 1 means Phase210 completed |
| phase210_model_fit_execution | 1 | Train/validation model fitting executed |
| phase210_strategy_replay_allowed | 0 | No strategy replay opened |
| phase210_test_replay_allowed_next | 0 | No test replay opened |
| phase210_test_rows_used | 0 | No sealed test rows used |
| phase210_promotion_allowed | 0 | No promotion opened |
| phase210_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase210_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase210_forbidden_outputs | strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export | Outputs forbidden in this phase |
| phase210_next_best_action | run_phase211_model_fit_validation_interpretation_no_replay_no_test | Recommended next milestone |

## Design Matrix Partition Inventory

| horizon_sec | trade_date | exchange | symbol | split_role | feature_file_exists | label_file_exists | joined_rows | test_rows_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-07-08 | NSE | ADANIPORTS | train | 1 | 1 | 3617 | 0 |
| 1 | 2026-07-08 | NSE | AXISBANK | train | 1 | 1 | 5829 | 0 |
| 1 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 1 | 1 | 3323 | 0 |
| 1 | 2026-07-08 | NSE | BANKBEES | train | 1 | 1 | 5645 | 0 |
| 1 | 2026-07-08 | NSE | BHARTIARTL | train | 1 | 1 | 3952 | 0 |
| 1 | 2026-07-08 | NSE | BPCL | train | 1 | 1 | 2852 | 0 |
| 1 | 2026-07-08 | NSE | BRITANNIA | train | 1 | 1 | 2151 | 0 |
| 1 | 2026-07-08 | NSE | CIPLA | train | 1 | 1 | 2953 | 0 |
| 1 | 2026-07-08 | NSE | DRREDDY | train | 1 | 1 | 2935 | 0 |
| 1 | 2026-07-08 | NSE | GOLDBEES | train | 1 | 1 | 4078 | 0 |
| 1 | 2026-07-08 | NSE | HCLTECH | train | 1 | 1 | 2706 | 0 |
| 1 | 2026-07-08 | NSE | HDFCBANK | train | 1 | 1 | 6816 | 0 |
| 1 | 2026-07-08 | NSE | HINDUNILVR | train | 1 | 1 | 3470 | 0 |
| 1 | 2026-07-08 | NSE | ICICIBANK | train | 1 | 1 | 6210 | 0 |
| 1 | 2026-07-08 | NSE | INFY | train | 1 | 1 | 5152 | 0 |
| 1 | 2026-07-08 | NSE | ITBEES | train | 1 | 1 | 2355 | 0 |
| 1 | 2026-07-08 | NSE | ITC | train | 1 | 1 | 4271 | 0 |
| 1 | 2026-07-08 | NSE | JUNIORBEES | train | 1 | 1 | 5241 | 0 |
| 1 | 2026-07-08 | NSE | KOTAKBANK | train | 1 | 1 | 4944 | 0 |
| 1 | 2026-07-08 | NSE | LT | train | 1 | 1 | 6328 | 0 |
| 1 | 2026-07-08 | NSE | M&M | train | 1 | 1 | 6037 | 0 |
| 1 | 2026-07-08 | NSE | MARUTI | train | 1 | 1 | 4917 | 0 |
| 1 | 2026-07-08 | NSE | NESTLEIND | train | 1 | 1 | 2943 | 0 |
| 1 | 2026-07-08 | NSE | NIFTYBEES | train | 1 | 1 | 5016 | 0 |
| 1 | 2026-07-08 | NSE | ONGC | train | 1 | 1 | 4121 | 0 |
| 1 | 2026-07-08 | NSE | RELIANCE | train | 1 | 1 | 6547 | 0 |
| 1 | 2026-07-08 | NSE | SBIN | train | 1 | 1 | 5499 | 0 |
| 1 | 2026-07-08 | NSE | SUNPHARMA | train | 1 | 1 | 3352 | 0 |
| 1 | 2026-07-08 | NSE | TCS | train | 1 | 1 | 3904 | 0 |
| 1 | 2026-07-08 | NSE | TECHM | train | 1 | 1 | 2802 | 0 |
| 1 | 2026-07-08 | NSE | ULTRACEMCO | train | 1 | 1 | 3043 | 0 |
| 1 | 2026-07-08 | NSE | WIPRO | train | 1 | 1 | 2625 | 0 |
| 1 | 2026-07-09 | NSE | ADANIPORTS | train | 1 | 1 | 5553 | 0 |
| 1 | 2026-07-09 | NSE | AXISBANK | train | 1 | 1 | 7446 | 0 |
| 1 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 1 | 1 | 5049 | 0 |
| 1 | 2026-07-09 | NSE | BANKBEES | train | 1 | 1 | 8885 | 0 |
| 1 | 2026-07-09 | NSE | BHARTIARTL | train | 1 | 1 | 9411 | 0 |
| 1 | 2026-07-09 | NSE | BPCL | train | 1 | 1 | 4696 | 0 |
| 1 | 2026-07-09 | NSE | BRITANNIA | train | 1 | 1 | 4229 | 0 |
| 1 | 2026-07-09 | NSE | CIPLA | train | 1 | 1 | 4886 | 0 |
| 1 | 2026-07-09 | NSE | DRREDDY | train | 1 | 1 | 9053 | 0 |
| 1 | 2026-07-09 | NSE | GOLDBEES | train | 1 | 1 | 6407 | 0 |
| 1 | 2026-07-09 | NSE | HCLTECH | train | 1 | 1 | 5477 | 0 |
| 1 | 2026-07-09 | NSE | HDFCBANK | train | 1 | 1 | 9419 | 0 |
| 1 | 2026-07-09 | NSE | HINDUNILVR | train | 1 | 1 | 6946 | 0 |
| 1 | 2026-07-09 | NSE | ICICIBANK | train | 1 | 1 | 9152 | 0 |
| 1 | 2026-07-09 | NSE | INFY | train | 1 | 1 | 7566 | 0 |
| 1 | 2026-07-09 | NSE | ITBEES | train | 1 | 1 | 3872 | 0 |
| 1 | 2026-07-09 | NSE | ITC | train | 1 | 1 | 7309 | 0 |
| 1 | 2026-07-09 | NSE | JUNIORBEES | train | 1 | 1 | 8589 | 0 |
| 1 | 2026-07-09 | NSE | KOTAKBANK | train | 1 | 1 | 8943 | 0 |
| 1 | 2026-07-09 | NSE | LT | train | 1 | 1 | 9072 | 0 |
| 1 | 2026-07-09 | NSE | M&M | train | 1 | 1 | 7704 | 0 |
| 1 | 2026-07-09 | NSE | MARUTI | train | 1 | 1 | 7379 | 0 |
| 1 | 2026-07-09 | NSE | NESTLEIND | train | 1 | 1 | 4454 | 0 |
| 1 | 2026-07-09 | NSE | NIFTYBEES | train | 1 | 1 | 8019 | 0 |
| 1 | 2026-07-09 | NSE | ONGC | train | 1 | 1 | 5782 | 0 |
| 1 | 2026-07-09 | NSE | RELIANCE | train | 1 | 1 | 9017 | 0 |
| 1 | 2026-07-09 | NSE | SBIN | train | 1 | 1 | 7833 | 0 |
| 1 | 2026-07-09 | NSE | SUNPHARMA | train | 1 | 1 | 7322 | 0 |
| 1 | 2026-07-09 | NSE | TCS | train | 1 | 1 | 7969 | 0 |
| 1 | 2026-07-09 | NSE | TECHM | train | 1 | 1 | 4929 | 0 |
| 1 | 2026-07-09 | NSE | ULTRACEMCO | train | 1 | 1 | 3979 | 0 |
| 1 | 2026-07-09 | NSE | WIPRO | train | 1 | 1 | 5788 | 0 |
| 1 | 2026-07-10 | NSE | ADANIPORTS | train | 1 | 1 | 9546 | 0 |
| 1 | 2026-07-10 | NSE | AXISBANK | train | 1 | 1 | 10801 | 0 |
| 1 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 1 | 1 | 9727 | 0 |
| 1 | 2026-07-10 | NSE | BANKBEES | train | 1 | 1 | 9229 | 0 |
| 1 | 2026-07-10 | NSE | BHARTIARTL | train | 1 | 1 | 11365 | 0 |
| 1 | 2026-07-10 | NSE | BPCL | train | 1 | 1 | 6758 | 0 |
| 1 | 2026-07-10 | NSE | BRITANNIA | train | 1 | 1 | 6029 | 0 |
| 1 | 2026-07-10 | NSE | CIPLA | train | 1 | 1 | 7907 | 0 |
| 1 | 2026-07-10 | NSE | DRREDDY | train | 1 | 1 | 13141 | 0 |
| 1 | 2026-07-10 | NSE | GOLDBEES | train | 1 | 1 | 9148 | 0 |
| 1 | 2026-07-10 | NSE | HCLTECH | train | 1 | 1 | 14317 | 0 |
| 1 | 2026-07-10 | NSE | HDFCBANK | train | 1 | 1 | 15043 | 0 |
| 1 | 2026-07-10 | NSE | HINDUNILVR | train | 1 | 1 | 8661 | 0 |
| 1 | 2026-07-10 | NSE | ICICIBANK | train | 1 | 1 | 11236 | 0 |
| 1 | 2026-07-10 | NSE | INFY | train | 1 | 1 | 15210 | 0 |
| 1 | 2026-07-10 | NSE | ITBEES | train | 1 | 1 | 6822 | 0 |
| 1 | 2026-07-10 | NSE | ITC | train | 1 | 1 | 11084 | 0 |
| 1 | 2026-07-10 | NSE | JUNIORBEES | train | 1 | 1 | 13252 | 0 |
| 1 | 2026-07-10 | NSE | KOTAKBANK | train | 1 | 1 | 10164 | 0 |
| 1 | 2026-07-10 | NSE | LT | train | 1 | 1 | 10640 | 0 |
| 1 | 2026-07-10 | NSE | M&M | train | 1 | 1 | 9987 | 0 |
| 1 | 2026-07-10 | NSE | MARUTI | train | 1 | 1 | 11104 | 0 |
| 1 | 2026-07-10 | NSE | NESTLEIND | train | 1 | 1 | 7878 | 0 |
| 1 | 2026-07-10 | NSE | NIFTYBEES | train | 1 | 1 | 11226 | 0 |
| 1 | 2026-07-10 | NSE | ONGC | train | 1 | 1 | 9395 | 0 |
| 1 | 2026-07-10 | NSE | RELIANCE | train | 1 | 1 | 11459 | 0 |
| 1 | 2026-07-10 | NSE | SBIN | train | 1 | 1 | 12205 | 0 |
| 1 | 2026-07-10 | NSE | SUNPHARMA | train | 1 | 1 | 9908 | 0 |
| 1 | 2026-07-10 | NSE | TCS | train | 1 | 1 | 16259 | 0 |
| 1 | 2026-07-10 | NSE | TECHM | train | 1 | 1 | 9551 | 0 |
| 1 | 2026-07-10 | NSE | ULTRACEMCO | train | 1 | 1 | 6525 | 0 |
| 1 | 2026-07-10 | NSE | WIPRO | train | 1 | 1 | 10157 | 0 |
| 1 | 2026-07-13 | NSE | ADANIPORTS | validation | 1 | 1 | 9453 | 0 |
| 1 | 2026-07-13 | NSE | AXISBANK | validation | 1 | 1 | 10797 | 0 |
| 1 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 1 | 1 | 14298 | 0 |
| 1 | 2026-07-13 | NSE | BANKBEES | validation | 1 | 1 | 13183 | 0 |
| 1 | 2026-07-13 | NSE | BHARTIARTL | validation | 1 | 1 | 11538 | 0 |
| 1 | 2026-07-13 | NSE | BPCL | validation | 1 | 1 | 8034 | 0 |
| 1 | 2026-07-13 | NSE | BRITANNIA | validation | 1 | 1 | 6759 | 0 |
| 1 | 2026-07-13 | NSE | CIPLA | validation | 1 | 1 | 8387 | 0 |
| 1 | 2026-07-13 | NSE | DRREDDY | validation | 1 | 1 | 8735 | 0 |
| 1 | 2026-07-13 | NSE | GOLDBEES | validation | 1 | 1 | 8947 | 0 |
| 1 | 2026-07-13 | NSE | HCLTECH | validation | 1 | 1 | 14296 | 0 |
| 1 | 2026-07-13 | NSE | HDFCBANK | validation | 1 | 1 | 16565 | 0 |
| 1 | 2026-07-13 | NSE | HINDUNILVR | validation | 1 | 1 | 8591 | 0 |
| 1 | 2026-07-13 | NSE | ICICIBANK | validation | 1 | 1 | 13716 | 0 |
| 1 | 2026-07-13 | NSE | INFY | validation | 1 | 1 | 16206 | 0 |
| 1 | 2026-07-13 | NSE | ITBEES | validation | 1 | 1 | 8304 | 0 |
| 1 | 2026-07-13 | NSE | ITC | validation | 1 | 1 | 8757 | 0 |
| 1 | 2026-07-13 | NSE | JUNIORBEES | validation | 1 | 1 | 11801 | 0 |
| 1 | 2026-07-13 | NSE | KOTAKBANK | validation | 1 | 1 | 9402 | 0 |
| 1 | 2026-07-13 | NSE | LT | validation | 1 | 1 | 11478 | 0 |
| 1 | 2026-07-13 | NSE | M&M | validation | 1 | 1 | 14145 | 0 |
| 1 | 2026-07-13 | NSE | MARUTI | validation | 1 | 1 | 15406 | 0 |
| 1 | 2026-07-13 | NSE | NESTLEIND | validation | 1 | 1 | 9035 | 0 |
| 1 | 2026-07-13 | NSE | NIFTYBEES | validation | 1 | 1 | 13039 | 0 |
| 1 | 2026-07-13 | NSE | ONGC | validation | 1 | 1 | 10644 | 0 |
| 1 | 2026-07-13 | NSE | RELIANCE | validation | 1 | 1 | 13219 | 0 |
| 1 | 2026-07-13 | NSE | SBIN | validation | 1 | 1 | 13084 | 0 |
| 1 | 2026-07-13 | NSE | SUNPHARMA | validation | 1 | 1 | 9572 | 0 |
| 1 | 2026-07-13 | NSE | TCS | validation | 1 | 1 | 16806 | 0 |
| 1 | 2026-07-13 | NSE | TECHM | validation | 1 | 1 | 11316 | 0 |
| 1 | 2026-07-13 | NSE | ULTRACEMCO | validation | 1 | 1 | 6783 | 0 |
| 1 | 2026-07-13 | NSE | WIPRO | validation | 1 | 1 | 11490 | 0 |
| 5 | 2026-07-08 | NSE | ADANIPORTS | train | 1 | 1 | 1617 | 0 |
| 5 | 2026-07-08 | NSE | AXISBANK | train | 1 | 1 | 1699 | 0 |
| 5 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 1 | 1 | 1594 | 0 |
| 5 | 2026-07-08 | NSE | BANKBEES | train | 1 | 1 | 1693 | 0 |
| 5 | 2026-07-08 | NSE | BHARTIARTL | train | 1 | 1 | 1616 | 0 |
| 5 | 2026-07-08 | NSE | BPCL | train | 1 | 1 | 1578 | 0 |
| 5 | 2026-07-08 | NSE | BRITANNIA | train | 1 | 1 | 1525 | 0 |
| 5 | 2026-07-08 | NSE | CIPLA | train | 1 | 1 | 1572 | 0 |
| 5 | 2026-07-08 | NSE | DRREDDY | train | 1 | 1 | 1582 | 0 |
| 5 | 2026-07-08 | NSE | GOLDBEES | train | 1 | 1 | 1642 | 0 |
| 5 | 2026-07-08 | NSE | HCLTECH | train | 1 | 1 | 1564 | 0 |
| 5 | 2026-07-08 | NSE | HDFCBANK | train | 1 | 1 | 1745 | 0 |
| 5 | 2026-07-08 | NSE | HINDUNILVR | train | 1 | 1 | 1618 | 0 |
| 5 | 2026-07-08 | NSE | ICICIBANK | train | 1 | 1 | 1722 | 0 |
| 5 | 2026-07-08 | NSE | INFY | train | 1 | 1 | 1682 | 0 |
| 5 | 2026-07-08 | NSE | ITBEES | train | 1 | 1 | 1585 | 0 |
| 5 | 2026-07-08 | NSE | ITC | train | 1 | 1 | 1643 | 0 |
| 5 | 2026-07-08 | NSE | JUNIORBEES | train | 1 | 1 | 1685 | 0 |
| 5 | 2026-07-08 | NSE | KOTAKBANK | train | 1 | 1 | 1664 | 0 |
| 5 | 2026-07-08 | NSE | LT | train | 1 | 1 | 1733 | 0 |
| 5 | 2026-07-08 | NSE | M&M | train | 1 | 1 | 1714 | 0 |
| 5 | 2026-07-08 | NSE | MARUTI | train | 1 | 1 | 1679 | 0 |
| 5 | 2026-07-08 | NSE | NESTLEIND | train | 1 | 1 | 1580 | 0 |
| 5 | 2026-07-08 | NSE | NIFTYBEES | train | 1 | 1 | 1687 | 0 |
| 5 | 2026-07-08 | NSE | ONGC | train | 1 | 1 | 1628 | 0 |
| 5 | 2026-07-08 | NSE | RELIANCE | train | 1 | 1 | 1731 | 0 |
| 5 | 2026-07-08 | NSE | SBIN | train | 1 | 1 | 1686 | 0 |
| 5 | 2026-07-08 | NSE | SUNPHARMA | train | 1 | 1 | 1600 | 0 |
| 5 | 2026-07-08 | NSE | TCS | train | 1 | 1 | 1651 | 0 |
| 5 | 2026-07-08 | NSE | TECHM | train | 1 | 1 | 1574 | 0 |
| 5 | 2026-07-08 | NSE | ULTRACEMCO | train | 1 | 1 | 1577 | 0 |
| 5 | 2026-07-08 | NSE | WIPRO | train | 1 | 1 | 1569 | 0 |
| 5 | 2026-07-09 | NSE | ADANIPORTS | train | 1 | 1 | 2448 | 0 |
| 5 | 2026-07-09 | NSE | AXISBANK | train | 1 | 1 | 2522 | 0 |
| 5 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 1 | 1 | 2390 | 0 |
| 5 | 2026-07-09 | NSE | BANKBEES | train | 1 | 1 | 2537 | 0 |
| 5 | 2026-07-09 | NSE | BHARTIARTL | train | 1 | 1 | 2558 | 0 |
| 5 | 2026-07-09 | NSE | BPCL | train | 1 | 1 | 2421 | 0 |
| 5 | 2026-07-09 | NSE | BRITANNIA | train | 1 | 1 | 2364 | 0 |
| 5 | 2026-07-09 | NSE | CIPLA | train | 1 | 1 | 2407 | 0 |
| 5 | 2026-07-09 | NSE | DRREDDY | train | 1 | 1 | 2539 | 0 |
| 5 | 2026-07-09 | NSE | GOLDBEES | train | 1 | 1 | 2469 | 0 |
| 5 | 2026-07-09 | NSE | HCLTECH | train | 1 | 1 | 2462 | 0 |
| 5 | 2026-07-09 | NSE | HDFCBANK | train | 1 | 1 | 2557 | 0 |
| 5 | 2026-07-09 | NSE | HINDUNILVR | train | 1 | 1 | 2484 | 0 |
| 5 | 2026-07-09 | NSE | ICICIBANK | train | 1 | 1 | 2548 | 0 |
| 5 | 2026-07-09 | NSE | INFY | train | 1 | 1 | 2532 | 0 |
| 5 | 2026-07-09 | NSE | ITBEES | train | 1 | 1 | 2350 | 0 |
| 5 | 2026-07-09 | NSE | ITC | train | 1 | 1 | 2527 | 0 |
| 5 | 2026-07-09 | NSE | JUNIORBEES | train | 1 | 1 | 2525 | 0 |
| 5 | 2026-07-09 | NSE | KOTAKBANK | train | 1 | 1 | 2555 | 0 |
| 5 | 2026-07-09 | NSE | LT | train | 1 | 1 | 2557 | 0 |
| 5 | 2026-07-09 | NSE | M&M | train | 1 | 1 | 2505 | 0 |
| 5 | 2026-07-09 | NSE | MARUTI | train | 1 | 1 | 2493 | 0 |
| 5 | 2026-07-09 | NSE | NESTLEIND | train | 1 | 1 | 2386 | 0 |
| 5 | 2026-07-09 | NSE | NIFTYBEES | train | 1 | 1 | 2514 | 0 |
| 5 | 2026-07-09 | NSE | ONGC | train | 1 | 1 | 2451 | 0 |
| 5 | 2026-07-09 | NSE | RELIANCE | train | 1 | 1 | 2539 | 0 |
| 5 | 2026-07-09 | NSE | SBIN | train | 1 | 1 | 2520 | 0 |
| 5 | 2026-07-09 | NSE | SUNPHARMA | train | 1 | 1 | 2517 | 0 |
| 5 | 2026-07-09 | NSE | TCS | train | 1 | 1 | 2530 | 0 |
| 5 | 2026-07-09 | NSE | TECHM | train | 1 | 1 | 2392 | 0 |
| 5 | 2026-07-09 | NSE | ULTRACEMCO | train | 1 | 1 | 2358 | 0 |
| 5 | 2026-07-09 | NSE | WIPRO | train | 1 | 1 | 2447 | 0 |
| 5 | 2026-07-10 | NSE | ADANIPORTS | train | 1 | 1 | 4276 | 0 |
| 5 | 2026-07-10 | NSE | AXISBANK | train | 1 | 1 | 4310 | 0 |
| 5 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 1 | 1 | 4202 | 0 |
| 5 | 2026-07-10 | NSE | BANKBEES | train | 1 | 1 | 4105 | 0 |
| 5 | 2026-07-10 | NSE | BHARTIARTL | train | 1 | 1 | 4351 | 0 |
| 5 | 2026-07-10 | NSE | BPCL | train | 1 | 1 | 4073 | 0 |
| 5 | 2026-07-10 | NSE | BRITANNIA | train | 1 | 1 | 3917 | 0 |
| 5 | 2026-07-10 | NSE | CIPLA | train | 1 | 1 | 4190 | 0 |
| 5 | 2026-07-10 | NSE | DRREDDY | train | 1 | 1 | 4375 | 0 |
| 5 | 2026-07-10 | NSE | GOLDBEES | train | 1 | 1 | 4250 | 0 |
| 5 | 2026-07-10 | NSE | HCLTECH | train | 1 | 1 | 4425 | 0 |
| 5 | 2026-07-10 | NSE | HDFCBANK | train | 1 | 1 | 4448 | 0 |
| 5 | 2026-07-10 | NSE | HINDUNILVR | train | 1 | 1 | 4184 | 0 |
| 5 | 2026-07-10 | NSE | ICICIBANK | train | 1 | 1 | 4342 | 0 |
| 5 | 2026-07-10 | NSE | INFY | train | 1 | 1 | 4460 | 0 |
| 5 | 2026-07-10 | NSE | ITBEES | train | 1 | 1 | 4066 | 0 |
| 5 | 2026-07-10 | NSE | ITC | train | 1 | 1 | 4335 | 0 |
| 5 | 2026-07-10 | NSE | JUNIORBEES | train | 1 | 1 | 4329 | 0 |
| 5 | 2026-07-10 | NSE | KOTAKBANK | train | 1 | 1 | 4285 | 0 |
| 5 | 2026-07-10 | NSE | LT | train | 1 | 1 | 4270 | 0 |
| 5 | 2026-07-10 | NSE | M&M | train | 1 | 1 | 4236 | 0 |
| 5 | 2026-07-10 | NSE | MARUTI | train | 1 | 1 | 4273 | 0 |
| 5 | 2026-07-10 | NSE | NESTLEIND | train | 1 | 1 | 4127 | 0 |
| 5 | 2026-07-10 | NSE | NIFTYBEES | train | 1 | 1 | 4295 | 0 |
| 5 | 2026-07-10 | NSE | ONGC | train | 1 | 1 | 4237 | 0 |
| 5 | 2026-07-10 | NSE | RELIANCE | train | 1 | 1 | 4360 | 0 |
| 5 | 2026-07-10 | NSE | SBIN | train | 1 | 1 | 4354 | 0 |
| 5 | 2026-07-10 | NSE | SUNPHARMA | train | 1 | 1 | 4285 | 0 |
| 5 | 2026-07-10 | NSE | TCS | train | 1 | 1 | 4481 | 0 |
| 5 | 2026-07-10 | NSE | TECHM | train | 1 | 1 | 4254 | 0 |
| 5 | 2026-07-10 | NSE | ULTRACEMCO | train | 1 | 1 | 4018 | 0 |
| 5 | 2026-07-10 | NSE | WIPRO | train | 1 | 1 | 4321 | 0 |
| 5 | 2026-07-13 | NSE | ADANIPORTS | validation | 1 | 1 | 4268 | 0 |
| 5 | 2026-07-13 | NSE | AXISBANK | validation | 1 | 1 | 4285 | 0 |
| 5 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 1 | 1 | 4384 | 0 |
| 5 | 2026-07-13 | NSE | BANKBEES | validation | 1 | 1 | 4285 | 0 |
| 5 | 2026-07-13 | NSE | BHARTIARTL | validation | 1 | 1 | 4367 | 0 |
| 5 | 2026-07-13 | NSE | BPCL | validation | 1 | 1 | 4189 | 0 |
| 5 | 2026-07-13 | NSE | BRITANNIA | validation | 1 | 1 | 4043 | 0 |
| 5 | 2026-07-13 | NSE | CIPLA | validation | 1 | 1 | 4212 | 0 |
| 5 | 2026-07-13 | NSE | DRREDDY | validation | 1 | 1 | 4258 | 0 |
| 5 | 2026-07-13 | NSE | GOLDBEES | validation | 1 | 1 | 4227 | 0 |
| 5 | 2026-07-13 | NSE | HCLTECH | validation | 1 | 1 | 4400 | 0 |
| 5 | 2026-07-13 | NSE | HDFCBANK | validation | 1 | 1 | 4473 | 0 |
| 5 | 2026-07-13 | NSE | HINDUNILVR | validation | 1 | 1 | 4217 | 0 |
| 5 | 2026-07-13 | NSE | ICICIBANK | validation | 1 | 1 | 4388 | 0 |
| 5 | 2026-07-13 | NSE | INFY | validation | 1 | 1 | 4471 | 0 |
| 5 | 2026-07-13 | NSE | ITBEES | validation | 1 | 1 | 4192 | 0 |
| 5 | 2026-07-13 | NSE | ITC | validation | 1 | 1 | 4227 | 0 |
| 5 | 2026-07-13 | NSE | JUNIORBEES | validation | 1 | 1 | 4245 | 0 |
| 5 | 2026-07-13 | NSE | KOTAKBANK | validation | 1 | 1 | 4253 | 0 |
| 5 | 2026-07-13 | NSE | LT | validation | 1 | 1 | 4319 | 0 |
| 5 | 2026-07-13 | NSE | M&M | validation | 1 | 1 | 4396 | 0 |
| 5 | 2026-07-13 | NSE | MARUTI | validation | 1 | 1 | 4442 | 0 |
| 5 | 2026-07-13 | NSE | NESTLEIND | validation | 1 | 1 | 4206 | 0 |
| 5 | 2026-07-13 | NSE | NIFTYBEES | validation | 1 | 1 | 4323 | 0 |
| 5 | 2026-07-13 | NSE | ONGC | validation | 1 | 1 | 4308 | 0 |
| 5 | 2026-07-13 | NSE | RELIANCE | validation | 1 | 1 | 4366 | 0 |
| 5 | 2026-07-13 | NSE | SBIN | validation | 1 | 1 | 4353 | 0 |
| 5 | 2026-07-13 | NSE | SUNPHARMA | validation | 1 | 1 | 4236 | 0 |
| 5 | 2026-07-13 | NSE | TCS | validation | 1 | 1 | 4484 | 0 |
| 5 | 2026-07-13 | NSE | TECHM | validation | 1 | 1 | 4288 | 0 |
| 5 | 2026-07-13 | NSE | ULTRACEMCO | validation | 1 | 1 | 4084 | 0 |
| 5 | 2026-07-13 | NSE | WIPRO | validation | 1 | 1 | 4288 | 0 |
| 15 | 2026-07-08 | NSE | ADANIPORTS | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | AXISBANK | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | BANKBEES | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | BHARTIARTL | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | BPCL | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | BRITANNIA | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | CIPLA | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | DRREDDY | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | GOLDBEES | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | HCLTECH | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | HDFCBANK | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | HINDUNILVR | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | ICICIBANK | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | INFY | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | ITBEES | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | ITC | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | JUNIORBEES | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | KOTAKBANK | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | LT | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | M&M | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | MARUTI | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | NESTLEIND | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | NIFTYBEES | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | ONGC | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | RELIANCE | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | SBIN | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | SUNPHARMA | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | TCS | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | TECHM | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | ULTRACEMCO | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-08 | NSE | WIPRO | train | 1 | 1 | 583 | 0 |
| 15 | 2026-07-09 | NSE | ADANIPORTS | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | AXISBANK | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | BANKBEES | train | 1 | 1 | 859 | 0 |
| 15 | 2026-07-09 | NSE | BHARTIARTL | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | BPCL | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | BRITANNIA | train | 1 | 1 | 857 | 0 |
| 15 | 2026-07-09 | NSE | CIPLA | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | DRREDDY | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | GOLDBEES | train | 1 | 1 | 859 | 0 |
| 15 | 2026-07-09 | NSE | HCLTECH | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | HDFCBANK | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | HINDUNILVR | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | ICICIBANK | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | INFY | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | ITBEES | train | 1 | 1 | 859 | 0 |
| 15 | 2026-07-09 | NSE | ITC | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | JUNIORBEES | train | 1 | 1 | 859 | 0 |
| 15 | 2026-07-09 | NSE | KOTAKBANK | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | LT | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | M&M | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | MARUTI | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | NESTLEIND | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | NIFTYBEES | train | 1 | 1 | 859 | 0 |
| 15 | 2026-07-09 | NSE | ONGC | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | RELIANCE | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | SBIN | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | SUNPHARMA | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | TCS | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | TECHM | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | ULTRACEMCO | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-09 | NSE | WIPRO | train | 1 | 1 | 858 | 0 |
| 15 | 2026-07-10 | NSE | ADANIPORTS | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | AXISBANK | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | BANKBEES | train | 1 | 1 | 1501 | 0 |
| 15 | 2026-07-10 | NSE | BHARTIARTL | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | BPCL | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | BRITANNIA | train | 1 | 1 | 1501 | 0 |
| 15 | 2026-07-10 | NSE | CIPLA | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | DRREDDY | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | GOLDBEES | train | 1 | 1 | 1501 | 0 |
| 15 | 2026-07-10 | NSE | HCLTECH | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | HDFCBANK | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | HINDUNILVR | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | ICICIBANK | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | INFY | train | 1 | 1 | 1501 | 0 |
| 15 | 2026-07-10 | NSE | ITBEES | train | 1 | 1 | 1501 | 0 |
| 15 | 2026-07-10 | NSE | ITC | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | JUNIORBEES | train | 1 | 1 | 1500 | 0 |
| 15 | 2026-07-10 | NSE | KOTAKBANK | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | LT | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | M&M | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | MARUTI | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | NESTLEIND | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | NIFTYBEES | train | 1 | 1 | 1501 | 0 |
| 15 | 2026-07-10 | NSE | ONGC | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | RELIANCE | train | 1 | 1 | 1501 | 0 |
| 15 | 2026-07-10 | NSE | SBIN | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | SUNPHARMA | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | TCS | train | 1 | 1 | 1501 | 0 |
| 15 | 2026-07-10 | NSE | TECHM | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-10 | NSE | ULTRACEMCO | train | 1 | 1 | 1501 | 0 |
| 15 | 2026-07-10 | NSE | WIPRO | train | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | ADANIPORTS | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | AXISBANK | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | BANKBEES | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | BHARTIARTL | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | BPCL | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | BRITANNIA | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | CIPLA | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | DRREDDY | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | GOLDBEES | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | HCLTECH | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | HDFCBANK | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | HINDUNILVR | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | ICICIBANK | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | INFY | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | ITBEES | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | ITC | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | JUNIORBEES | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | KOTAKBANK | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | LT | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | M&M | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | MARUTI | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | NESTLEIND | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | NIFTYBEES | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | ONGC | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | RELIANCE | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | SBIN | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | SUNPHARMA | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | TCS | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | TECHM | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | ULTRACEMCO | validation | 1 | 1 | 1502 | 0 |
| 15 | 2026-07-13 | NSE | WIPRO | validation | 1 | 1 | 1502 | 0 |
| 60 | 2026-07-08 | NSE | ADANIPORTS | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | AXISBANK | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | BANKBEES | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | BHARTIARTL | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | BPCL | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | BRITANNIA | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | CIPLA | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | DRREDDY | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | GOLDBEES | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | HCLTECH | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | HDFCBANK | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | HINDUNILVR | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | ICICIBANK | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | INFY | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | ITBEES | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | ITC | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | JUNIORBEES | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | KOTAKBANK | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | LT | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | M&M | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | MARUTI | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | NESTLEIND | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | NIFTYBEES | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | ONGC | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | RELIANCE | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | SBIN | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | SUNPHARMA | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | TCS | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | TECHM | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | ULTRACEMCO | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-08 | NSE | WIPRO | train | 1 | 1 | 147 | 0 |
| 60 | 2026-07-09 | NSE | ADANIPORTS | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | AXISBANK | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | BANKBEES | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | BHARTIARTL | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | BPCL | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | BRITANNIA | train | 1 | 1 | 215 | 0 |
| 60 | 2026-07-09 | NSE | CIPLA | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | DRREDDY | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | GOLDBEES | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | HCLTECH | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | HDFCBANK | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | HINDUNILVR | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | ICICIBANK | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | INFY | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | ITBEES | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | ITC | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | JUNIORBEES | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | KOTAKBANK | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | LT | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | M&M | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | MARUTI | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | NESTLEIND | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | NIFTYBEES | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | ONGC | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | RELIANCE | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | SBIN | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | SUNPHARMA | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | TCS | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | TECHM | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | ULTRACEMCO | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-09 | NSE | WIPRO | train | 1 | 1 | 216 | 0 |
| 60 | 2026-07-10 | NSE | ADANIPORTS | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | AXISBANK | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | BANKBEES | train | 1 | 1 | 376 | 0 |
| 60 | 2026-07-10 | NSE | BHARTIARTL | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | BPCL | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | BRITANNIA | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | CIPLA | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | DRREDDY | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | GOLDBEES | train | 1 | 1 | 376 | 0 |
| 60 | 2026-07-10 | NSE | HCLTECH | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | HDFCBANK | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | HINDUNILVR | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | ICICIBANK | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | INFY | train | 1 | 1 | 376 | 0 |
| 60 | 2026-07-10 | NSE | ITBEES | train | 1 | 1 | 376 | 0 |
| 60 | 2026-07-10 | NSE | ITC | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | JUNIORBEES | train | 1 | 1 | 375 | 0 |
| 60 | 2026-07-10 | NSE | KOTAKBANK | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | LT | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | M&M | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | MARUTI | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | NESTLEIND | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | NIFTYBEES | train | 1 | 1 | 376 | 0 |
| 60 | 2026-07-10 | NSE | ONGC | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | RELIANCE | train | 1 | 1 | 376 | 0 |
| 60 | 2026-07-10 | NSE | SBIN | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | SUNPHARMA | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | TCS | train | 1 | 1 | 376 | 0 |
| 60 | 2026-07-10 | NSE | TECHM | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | ULTRACEMCO | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-10 | NSE | WIPRO | train | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | ADANIPORTS | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | AXISBANK | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | BANKBEES | validation | 1 | 1 | 376 | 0 |
| 60 | 2026-07-13 | NSE | BHARTIARTL | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | BPCL | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | BRITANNIA | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | CIPLA | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | DRREDDY | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | GOLDBEES | validation | 1 | 1 | 376 | 0 |
| 60 | 2026-07-13 | NSE | HCLTECH | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | HDFCBANK | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | HINDUNILVR | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | ICICIBANK | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | INFY | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | ITBEES | validation | 1 | 1 | 376 | 0 |
| 60 | 2026-07-13 | NSE | ITC | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | JUNIORBEES | validation | 1 | 1 | 376 | 0 |
| 60 | 2026-07-13 | NSE | KOTAKBANK | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | LT | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | M&M | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | MARUTI | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | NESTLEIND | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | NIFTYBEES | validation | 1 | 1 | 376 | 0 |
| 60 | 2026-07-13 | NSE | ONGC | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | RELIANCE | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | SBIN | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | SUNPHARMA | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | TCS | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | TECHM | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | ULTRACEMCO | validation | 1 | 1 | 377 | 0 |
| 60 | 2026-07-13 | NSE | WIPRO | validation | 1 | 1 | 377 | 0 |

## Train/Validation Model Metrics

| phase210_model_fit_id | phase209_model_spec_id | model_family | target_label | horizon_sec | split_role | train_rows_used_for_fit | test_rows_used | strategy_replay_allowed | promotion_allowed | rows | target_mean | prediction_mean | mse | mae | correlation | binary_accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | regularized_logistic_classification | short_horizon_direction_label | 1 | train | 693503 | 0 | 0 | 0 | 693503 | 0.196184 | 0.196184 | 0.155862 | 0.311727 | 0.107835 | 0.803816 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | regularized_logistic_classification | short_horizon_direction_label | 1 | validation | 693503 | 0 | 0 | 0 | 363786 | 0.204928 | 0.137452 | 0.166626 | 0.283991 | 0.0738069 | 0.795069 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | regularized_logistic_classification | short_horizon_direction_label | 5 | train | 268273 | 0 | 0 | 0 | 268273 | 0.297954 | 0.297954 | 0.205937 | 0.411874 | 0.124467 | 0.702009 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | regularized_logistic_classification | short_horizon_direction_label | 5 | validation | 268273 | 0 | 0 | 0 | 137477 | 0.30488 | 0.255469 | 0.211775 | 0.399423 | 0.110658 | 0.695127 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | regularized_logistic_classification | short_horizon_direction_label | 15 | train | 94169 | 0 | 0 | 0 | 94169 | 0.393654 | 0.393654 | 0.235904 | 0.471807 | 0.108053 | 0.605815 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | regularized_logistic_classification | short_horizon_direction_label | 15 | validation | 94169 | 0 | 0 | 0 | 48064 | 0.404981 | 0.3779 | 0.239103 | 0.471848 | 0.104053 | 0.595061 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | regularized_logistic_classification | short_horizon_direction_label | 60 | train | 23670 | 0 | 0 | 0 | 23670 | 0.450317 | 0.450317 | 0.246017 | 0.492033 | 0.0782346 | 0.553781 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | regularized_logistic_classification | short_horizon_direction_label | 60 | validation | 23670 | 0 | 0 | 0 | 12059 | 0.472013 | 0.477898 | 0.247855 | 0.495964 | 0.0748526 | 0.539597 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | regularized_linear_return_sign_proxy | future_mid_return_bps_next_bucket | 1 | train | 693503 | 0 | 0 | 0 | 693503 | -1.3321 | -1.3321 | 13261.8 | 3.27098 | 0.0171488 |  |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | regularized_linear_return_sign_proxy | future_mid_return_bps_next_bucket | 1 | validation | 693503 | 0 | 0 | 0 | 363786 | -0.870259 | 0.500399 | 8790.69 | 2.64257 | 0.033177 |  |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | regularized_linear_return_sign_proxy | future_mid_return_bps_next_bucket | 5 | train | 268273 | 0 | 0 | 0 | 268273 | -3.44358 | -3.44358 | 34256.8 | 8.421 | 0.0288146 |  |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | regularized_linear_return_sign_proxy | future_mid_return_bps_next_bucket | 5 | validation | 268273 | 0 | 0 | 0 | 137477 | -2.30285 | 1.54635 | 23269.5 | 6.65923 | 0.0297601 |  |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | regularized_linear_return_sign_proxy | future_mid_return_bps_next_bucket | 15 | train | 94169 | 0 | 0 | 0 | 94169 | -9.81021 | -9.81021 | 96034 | 34.014 | 0.127103 |  |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | regularized_linear_return_sign_proxy | future_mid_return_bps_next_bucket | 15 | validation | 94169 | 0 | 0 | 0 | 48064 | -6.58684 | -4.21741 | 66008 | 26.5394 | 0.0965297 |  |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | regularized_linear_return_sign_proxy | future_mid_return_bps_next_bucket | 60 | train | 23670 | 0 | 0 | 0 | 23670 | -39.0295 | -39.0295 | 265108 | 149.856 | 0.561524 |  |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | regularized_linear_return_sign_proxy | future_mid_return_bps_next_bucket | 60 | validation | 23670 | 0 | 0 | 0 | 12059 | -26.2593 | 19.2255 | 273838 | 120.925 | 0.143592 |  |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | monotonic_tree_or_gradient_boosting_diagnostic | execution_risk_spread_widen_next_bucket | 1 | train | 693503 | 0 | 0 | 0 | 693503 | 0.17342 | 0.17342 | 0.14194 | 0.283881 | 0.0990003 | 0.82658 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | monotonic_tree_or_gradient_boosting_diagnostic | execution_risk_spread_widen_next_bucket | 1 | validation | 693503 | 0 | 0 | 0 | 363786 | 0.182572 | 0.110326 | 0.153643 | 0.251041 | 0.073973 | 0.817428 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | monotonic_tree_or_gradient_boosting_diagnostic | execution_risk_spread_widen_next_bucket | 5 | train | 268273 | 0 | 0 | 0 | 268273 | 0.264276 | 0.264276 | 0.192701 | 0.385403 | 0.0944001 | 0.735724 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | monotonic_tree_or_gradient_boosting_diagnostic | execution_risk_spread_widen_next_bucket | 5 | validation | 268273 | 0 | 0 | 0 | 137477 | 0.270751 | 0.205143 | 0.200239 | 0.362265 | 0.0890257 | 0.729249 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | monotonic_tree_or_gradient_boosting_diagnostic | execution_risk_spread_widen_next_bucket | 15 | train | 94169 | 0 | 0 | 0 | 94169 | 0.351506 | 0.351506 | 0.22709 | 0.454179 | 0.0614204 | 0.648494 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | monotonic_tree_or_gradient_boosting_diagnostic | execution_risk_spread_widen_next_bucket | 15 | validation | 94169 | 0 | 0 | 0 | 48064 | 0.357502 | 0.31049 | 0.231062 | 0.444697 | 0.0635149 | 0.642498 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | monotonic_tree_or_gradient_boosting_diagnostic | execution_risk_spread_widen_next_bucket | 60 | train | 23670 | 0 | 0 | 0 | 23670 | 0.399958 | 0.399958 | 0.239572 | 0.479146 | 0.0417967 | 0.600169 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | monotonic_tree_or_gradient_boosting_diagnostic | execution_risk_spread_widen_next_bucket | 60 | validation | 23670 | 0 | 0 | 0 | 12059 | 0.405838 | 0.381164 | 0.241328 | 0.476851 | 0.0416012 | 0.594162 |

## Model Coefficient Ledger

| phase210_model_fit_id | phase209_model_spec_id | target_label | horizon_sec | coefficient_name | coefficient_value | model_fit_execution | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | intercept | 0.196184 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | cross_symbol_arrival_count | -0.011779 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | cross_symbol_arrival_share | -0.011779 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | depth_refresh_count | -0.0485055 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | phase176_universe_symbols | 4.09178e-12 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | quote_churn_count | 0.024951 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | receive_event_count | 0.0363591 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | receive_event_rate_baseline_days | -0.0256389 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | receive_event_rate_zscore | -0.00604611 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | stale_quote_duration_ms | 0.00639654 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | top5_qty_imbalance | 0.0215107 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | intercept | 0.297954 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | cross_symbol_arrival_count | -0.00673456 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | cross_symbol_arrival_share | -0.00673456 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | depth_refresh_count | -0.0126321 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | phase176_universe_symbols | 2.08059e-13 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | quote_churn_count | 0.0398526 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | receive_event_count | 0.0112055 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | receive_event_rate_baseline_days | -0.0210345 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | receive_event_rate_zscore | 0.0052438 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | stale_quote_duration_ms | -0.00309276 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | top5_qty_imbalance | 0.0345827 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | intercept | 0.393654 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | cross_symbol_arrival_count | -0.00573857 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | cross_symbol_arrival_share | -0.00573857 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | depth_refresh_count | 0.0158369 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | phase176_universe_symbols | -3.75586e-13 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | quote_churn_count | 0.0158971 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | receive_event_count | 0.000973557 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | receive_event_rate_baseline_days | -0.00974208 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | receive_event_rate_zscore | -0.00310012 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | stale_quote_duration_ms | 0.00698096 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | top5_qty_imbalance | 0.0416672 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | intercept | 0.450317 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | cross_symbol_arrival_count | 0.00369599 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | cross_symbol_arrival_share | 0.00369599 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | depth_refresh_count | 0.0470766 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | phase176_universe_symbols | -5.02484e-14 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | quote_churn_count | -0.0244638 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | receive_event_count | -0.00775772 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | receive_event_rate_baseline_days | 0.00961818 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | receive_event_rate_zscore | 7.13022e-07 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | stale_quote_duration_ms | 0.0048339 | 1 | 0 | 0 |
| P210_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | top5_qty_imbalance | 0.0345101 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | intercept | -1.3321 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | cross_symbol_arrival_count | 0.792635 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | cross_symbol_arrival_share | 0.792635 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | depth_refresh_count | -2.5884 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | phase176_universe_symbols | -1.35752e-10 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | quote_churn_count | 1.12639 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | receive_event_count | 0.586859 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | receive_event_rate_baseline_days | 0.724938 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | receive_event_rate_zscore | 0.182889 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | stale_quote_duration_ms | -1.7434 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | top5_qty_imbalance | 0.518061 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | intercept | -3.44358 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | cross_symbol_arrival_count | 2.34541 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | cross_symbol_arrival_share | 2.34541 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | depth_refresh_count | -3.32523 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | phase176_universe_symbols | -4.10992e-11 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | quote_churn_count | 1.17191 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | receive_event_count | 3.79565 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | receive_event_rate_baseline_days | 1.8745 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | receive_event_rate_zscore | -2.62609 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | stale_quote_duration_ms | -1.19719 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | top5_qty_imbalance | 1.33927 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | intercept | -9.81021 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | cross_symbol_arrival_count | 16.9936 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | cross_symbol_arrival_share | 16.9936 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | depth_refresh_count | 12.0137 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | phase176_universe_symbols | 2.23051e-11 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | quote_churn_count | 6.61563 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | receive_event_count | -1.23045 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | receive_event_rate_baseline_days | -0.778736 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | receive_event_rate_zscore | -14.8049 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | stale_quote_duration_ms | 12.317 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | top5_qty_imbalance | 3.86238 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | intercept | -39.0295 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | cross_symbol_arrival_count | 162.683 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | cross_symbol_arrival_share | 162.683 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | depth_refresh_count | 213.606 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | phase176_universe_symbols | 8.11661e-10 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | quote_churn_count | 82.2182 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | receive_event_count | -201.475 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | receive_event_rate_baseline_days | -0.902675 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | receive_event_rate_zscore | -55.2462 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | stale_quote_duration_ms | 106.284 | 1 | 0 | 0 |
| P210_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | top5_qty_imbalance | 10.9691 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | intercept | 0.17342 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | cross_symbol_arrival_count | -0.0110042 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | cross_symbol_arrival_share | -0.0110042 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | depth_refresh_count | -0.0438493 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | phase176_universe_symbols | 3.21926e-12 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | quote_churn_count | 0.0148597 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | receive_event_count | 0.0402918 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | receive_event_rate_baseline_days | -0.026917 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | receive_event_rate_zscore | -0.00584308 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | stale_quote_duration_ms | 0.00654214 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | top5_qty_imbalance | -0.00281754 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | intercept | 0.264276 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | cross_symbol_arrival_count | -0.00603486 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | cross_symbol_arrival_share | -0.00603486 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | depth_refresh_count | -0.0087181 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | phase176_universe_symbols | 3.37928e-13 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | quote_churn_count | 0.0238894 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | receive_event_count | 0.0134353 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | receive_event_rate_baseline_days | -0.026825 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | receive_event_rate_zscore | 0.0073815 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | stale_quote_duration_ms | -0.00247516 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | top5_qty_imbalance | -0.00342679 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | intercept | 0.351506 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | cross_symbol_arrival_count | -0.00278459 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | cross_symbol_arrival_share | -0.00278459 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | depth_refresh_count | 0.0440955 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | phase176_universe_symbols | 2.41982e-13 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | quote_churn_count | -0.0139398 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | receive_event_count | -0.00870055 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | receive_event_rate_baseline_days | -0.0195176 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | receive_event_rate_zscore | -0.00124006 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | stale_quote_duration_ms | 0.00577113 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | top5_qty_imbalance | -0.00123553 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | intercept | 0.399958 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | cross_symbol_arrival_count | 0.00414564 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | cross_symbol_arrival_share | 0.00414564 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | depth_refresh_count | 0.0938339 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | phase176_universe_symbols | -1.44659e-13 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | quote_churn_count | -0.0640583 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | receive_event_count | -0.0189129 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | receive_event_rate_baseline_days | -0.0103741 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | receive_event_rate_zscore | -0.000987479 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | stale_quote_duration_ms | 0.00874223 | 1 | 0 | 0 |
| P210_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | top5_qty_imbalance | -0.00386487 | 1 | 0 | 0 |

## Negative Control Metrics

| phase210_control_id | phase209_model_spec_id | target_label | horizon_sec | control_type | validation_rows | validation_mse | validation_binary_accuracy | test_rows_used | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P210_SHUFFLED_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H1s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 1 | shuffled_target_negative_control | 363786 | 0.16304 | 0.795072 | 0 | 0 |
| P210_SHUFFLED_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H5s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 5 | shuffled_target_negative_control | 137477 | 0.212105 | 0.69512 | 0 | 0 |
| P210_SHUFFLED_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H15s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 15 | shuffled_target_negative_control | 48064 | 0.241406 | 0.595019 | 0 | 0 |
| P210_SHUFFLED_P209_LINEAR_LOGIT_DIRECTION_BASELINE_H60s | P209_LINEAR_LOGIT_DIRECTION_BASELINE | short_horizon_direction_label | 60 | shuffled_target_negative_control | 12059 | 0.249415 | 0.527987 | 0 | 0 |
| P210_SHUFFLED_P209_RIDGE_RETURN_SIGN_BASELINE_H1s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 1 | shuffled_target_negative_control | 363786 | 8797.31 |  | 0 | 0 |
| P210_SHUFFLED_P209_RIDGE_RETURN_SIGN_BASELINE_H5s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 5 | shuffled_target_negative_control | 137477 | 23275.6 |  | 0 | 0 |
| P210_SHUFFLED_P209_RIDGE_RETURN_SIGN_BASELINE_H15s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 15 | shuffled_target_negative_control | 48064 | 66488.4 |  | 0 | 0 |
| P210_SHUFFLED_P209_RIDGE_RETURN_SIGN_BASELINE_H60s | P209_RIDGE_RETURN_SIGN_BASELINE | future_mid_return_bps_next_bucket | 60 | shuffled_target_negative_control | 12059 | 263452 |  | 0 | 0 |
| P210_SHUFFLED_P209_MONOTONIC_TREE_DIAGNOSTIC_H1s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 1 | shuffled_target_negative_control | 363786 | 0.149322 | 0.817428 | 0 | 0 |
| P210_SHUFFLED_P209_MONOTONIC_TREE_DIAGNOSTIC_H5s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 5 | shuffled_target_negative_control | 137477 | 0.197502 | 0.729249 | 0 | 0 |
| P210_SHUFFLED_P209_MONOTONIC_TREE_DIAGNOSTIC_H15s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 15 | shuffled_target_negative_control | 48064 | 0.229583 | 0.642498 | 0 | 0 |
| P210_SHUFFLED_P209_MONOTONIC_TREE_DIAGNOSTIC_H60s | P209_MONOTONIC_TREE_DIAGNOSTIC | execution_risk_spread_widen_next_bucket | 60 | shuffled_target_negative_control | 12059 | 0.241033 | 0.594162 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase210 | allowed_in_phase210 | rationale |
| --- | --- | --- | --- |
| strategy_replay | 0 | 0 | Phase210 fits train/validation dry-run models only and does not run replay, test replay, fills, P&L, promotion, or paper/live acceptance. |
| test_replay_execution | 0 | 0 | Phase210 fits train/validation dry-run models only and does not run replay, test replay, fills, P&L, promotion, or paper/live acceptance. |
| test_result | 0 | 0 | Phase210 fits train/validation dry-run models only and does not run replay, test replay, fills, P&L, promotion, or paper/live acceptance. |
| promotion | 0 | 0 | Phase210 fits train/validation dry-run models only and does not run replay, test replay, fills, P&L, promotion, or paper/live acceptance. |
| paper_live_acceptance | 0 | 0 | Phase210 fits train/validation dry-run models only and does not run replay, test replay, fills, P&L, promotion, or paper/live acceptance. |
| order_arrival | 0 | 0 | Phase210 fits train/validation dry-run models only and does not run replay, test replay, fills, P&L, promotion, or paper/live acceptance. |
| fill_model | 0 | 0 | Phase210 fits train/validation dry-run models only and does not run replay, test replay, fills, P&L, promotion, or paper/live acceptance. |
| pnl_replay | 0 | 0 | Phase210 fits train/validation dry-run models only and does not run replay, test replay, fills, P&L, promotion, or paper/live acceptance. |
| profitability_claim | 0 | 0 | Phase210 fits train/validation dry-run models only and does not run replay, test replay, fills, P&L, promotion, or paper/live acceptance. |
| threshold_widening | 0 | 0 | Phase210 fits train/validation dry-run models only and does not run replay, test replay, fills, P&L, promotion, or paper/live acceptance. |
| row_level_prediction_export | 0 | 0 | Phase210 fits train/validation dry-run models only and does not run replay, test replay, fills, P&L, promotion, or paper/live acceptance. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P210_PHASE209_COMPLETE | True | phase209_complete=1 | hard |
| P210_DESIGN_MATRIX_JOINED | True | joined_rows=1641001 | hard |
| P210_MODEL_FITS_RECORDED | True | model_fit_rows=12 | hard |
| P210_VALIDATION_METRICS_RECORDED | True | validation_metric_rows=12 | hard |
| P210_NEGATIVE_CONTROLS_RECORDED | True | negative_control_rows=12 | hard |
| P210_TEST_REPLAY_AND_TEST_ROWS_CLOSED | True | test_rows_used=0 | hard |
| P210_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; replay_flags=0 | hard |

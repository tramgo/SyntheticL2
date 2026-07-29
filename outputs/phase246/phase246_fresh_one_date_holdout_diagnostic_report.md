# Phase246 Fresh One-date Holdout Diagnostic

Generated UTC: 2026-07-29T09:05:55.177423+00:00

Phase246 applies the frozen Phase244 candidate to one fresh unseen real L2 date (`2026-07-20`) using the disk-conscious one-date-first policy.
It is an early-falsification diagnostic only: one date can reject the candidate, but one date cannot accept or promote it.
No thresholds, horizons, symbols, costs, controls, paper/live routing or profitability claims are changed by this phase.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase246_fresh_one_date_holdout_diagnostic_complete | 1 | Phase246 one-date fresh holdout diagnostic completed |
| phase246_trade_date | 2026-07-20 | Fresh unseen real date used |
| phase246_requested_policy | one_new_date_first | Storage/download policy selected |
| phase246_candidate_id | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | Frozen Phase244 candidate |
| phase246_parameter_tuning_used | 0 | No Phase246 parameter tuning |
| phase246_raw_symbol_dirs | 32 | Raw symbol directories represented |
| phase246_raw_parquet_files | 50421 | Raw parquet files represented |
| phase246_source_feature_rows_15s | 48095 | 15-second source feature rows materialized |
| phase246_real_event_bar_rows | 4832 | Phase235-compatible event bars materialized |
| phase246_trade_rows | 9 | Frozen candidate trades selected |
| phase246_net_pnl_inr | 645.948 | One-date diagnostic net P&L after costs |
| phase246_symbols | 9 | Symbols represented in selected trades |
| phase246_control_pass_rows | 2 | Controls passed |
| phase246_control_rows | 4 | Controls evaluated |
| phase246_diagnostic_gate_pass_rows | 1 | Diagnostic gates passed |
| phase246_diagnostic_gate_rows | 4 | Diagnostic gates evaluated |
| phase246_hard_gate_pass_rows | 7 | Hard gates passed |
| phase246_hard_gate_rows | 7 | Hard gates evaluated |
| phase246_one_date_diagnostic_candidate_survived | 0 | One-date diagnostic survived; still not acceptance |
| phase246_full_acceptance_allowed | 0 | One-date diagnostic cannot satisfy full acceptance |
| phase246_strategy_promotion_allowed | 0 | No strategy promotion from Phase246 |
| phase246_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase246 |
| phase246_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase246 |
| phase246_next_best_action | close_or_redesign_phase244_candidate_after_phase246_one_date_failure_no_more_downloads_no_paper_live | Recommended next milestone |

## Diagnostic Summary

| candidate_id | diagnostic_trade_rows | diagnostic_net_pnl_inr | diagnostic_gross_pnl_inr | diagnostic_cost_pnl_drag_inr | diagnostic_dates | diagnostic_symbols | diagnostic_positive_symbols | diagnostic_precision_cost_clear | diagnostic_max_symbol_contribution_abs | materialized_event_bars | materialized_symbols | raw_symbols | raw_parquet_files | raw_symbol_dirs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | 9 | 645.948 | 1772.97 | 1127.02 | 1 | 9 | 4 | 0.444444 | 0.702798 | 4832 | 32 | 32 | 50421 | 32 |

## Controls

| control_id | net_pnl_inr | passed | random_p95_net_pnl_inr | random_beat_fraction |
| --- | --- | --- | --- | --- |
| SIDE_FLIP | -2900 | True |  |  |
| RANDOM_SIDE_1000_RUNS | 645.948 | False | 765.207 | 0.939 |
| COST_150 | 82.4358 | True |  |  |
| COST_200 | -481.076 | False |  |  |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P246_ONE_NEW_DATE_POLICY_SELECTED | True | one_new_date_first | one_new_date_first | hard |
| P246_FORBIDDEN_TUNING_DATE_EXCLUDED | True | 2026-07-20 | not 2026-07-17 | hard |
| P246_RAW_L2_PRESENT | True | 50421 | >0 raw parquet files | hard |
| P246_EVENT_BARS_MATERIALIZED | True | 4832 | >0 event bars | hard |
| P246_FROZEN_PHASE244_CANDIDATE_REPLAYED | True | 9 | >=1 frozen-candidate trade | hard |
| P246_DIAGNOSTIC_NET_POSITIVE | True | 645.948 | >0 net P&L after modeled costs | diagnostic |
| P246_DIAGNOSTIC_MIN_TRADES | False | 9 | >=20 trades | diagnostic |
| P246_DIAGNOSTIC_MIN_SYMBOLS | False | 9 | >=10 symbols | diagnostic |
| P246_DIAGNOSTIC_CONTROLS | False | 2/4 | 4/4 controls | diagnostic |
| P246_FULL_ACCEPTANCE_CLOSED_ONE_DATE_ONLY | True | 1 | 1 | hard |
| P246_NO_TUNING_PROMOTION_PAPER_OR_LIVE | True | 0 | 0 | hard |

## Symbol Inventory

| trade_date | exchange | symbol | source_1s_rows | raw_parquet_files |
| --- | --- | --- | --- | --- |
| 2026-07-20 | NSE | ADANIPORTS | 9314 | 1576 |
| 2026-07-20 | NSE | AXISBANK | 16839 | 1576 |
| 2026-07-20 | NSE | BAJAJ-AUTO | 14581 | 1576 |
| 2026-07-20 | NSE | BANKBEES | 14791 | 1576 |
| 2026-07-20 | NSE | BHARTIARTL | 11201 | 1576 |
| 2026-07-20 | NSE | BPCL | 8951 | 1575 |
| 2026-07-20 | NSE | BRITANNIA | 6334 | 1574 |
| 2026-07-20 | NSE | CIPLA | 9715 | 1576 |
| 2026-07-20 | NSE | DRREDDY | 9333 | 1576 |
| 2026-07-20 | NSE | GOLDBEES | 8980 | 1576 |
| 2026-07-20 | NSE | HCLTECH | 10692 | 1575 |
| 2026-07-20 | NSE | HDFCBANK | 16945 | 1576 |
| 2026-07-20 | NSE | HINDUNILVR | 9384 | 1575 |
| 2026-07-20 | NSE | ICICIBANK | 16595 | 1576 |
| 2026-07-20 | NSE | INFY | 16128 | 1576 |
| 2026-07-20 | NSE | ITBEES | 7096 | 1576 |
| 2026-07-20 | NSE | ITC | 15980 | 1576 |
| 2026-07-20 | NSE | JUNIORBEES | 14697 | 1576 |
| 2026-07-20 | NSE | KOTAKBANK | 15298 | 1576 |
| 2026-07-20 | NSE | LT | 13355 | 1576 |
| 2026-07-20 | NSE | M&M | 13011 | 1576 |
| 2026-07-20 | NSE | MARUTI | 12555 | 1576 |
| 2026-07-20 | NSE | NESTLEIND | 9712 | 1576 |
| 2026-07-20 | NSE | NIFTYBEES | 14280 | 1576 |
| 2026-07-20 | NSE | ONGC | 9894 | 1576 |
| 2026-07-20 | NSE | RELIANCE | 15592 | 1575 |
| 2026-07-20 | NSE | SBIN | 15329 | 1575 |
| 2026-07-20 | NSE | SUNPHARMA | 9766 | 1575 |
| 2026-07-20 | NSE | TCS | 14439 | 1575 |
| 2026-07-20 | NSE | TECHM | 9889 | 1575 |
| 2026-07-20 | NSE | ULTRACEMCO | 11848 | 1575 |
| 2026-07-20 | NSE | WIPRO | 9095 | 1576 |

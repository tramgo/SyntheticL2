# Phase241 One-date Unseen Real L2 Diagnostic

Generated UTC: 2026-07-29T08:04:04.327864+00:00

Phase241 materializes the downloaded 2026-07-17 raw Zerodha-websocket-like top-five market-by-price L2 data into Phase235-compatible event bars.
It replays only the frozen Phase237 candidate with frozen thresholds and no parameter tuning.
Because disk pressure limits validation to one new real date, this is an early-falsification diagnostic only, not full five-date acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase241_one_date_unseen_diagnostic_complete | 1 | Phase241 one-date diagnostic completed |
| phase241_trade_date | 2026-07-17 | Unseen real date used |
| phase241_candidate_id | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | Frozen Phase237 candidate |
| phase241_parameter_tuning_used | 0 | No Phase241 parameter tuning |
| phase241_source_feature_rows_15s | 48094 | 15-second source feature rows materialized |
| phase241_real_event_bar_rows | 4832 | Phase235-compatible event bars materialized |
| phase241_raw_symbols | 32 | Raw symbols represented |
| phase241_raw_parquet_files | 50787 | Raw parquet files represented |
| phase241_trade_rows | 15 | Frozen candidate trades selected |
| phase241_net_pnl_inr | 700.437 | One-date diagnostic net P&L after costs |
| phase241_symbols | 13 | Symbols represented in selected trades |
| phase241_control_pass_rows | 1 | Controls passed |
| phase241_control_rows | 4 | Controls evaluated |
| phase241_diagnostic_gate_pass_rows | 2 | Diagnostic gates passed |
| phase241_diagnostic_gate_rows | 3 | Diagnostic gates evaluated |
| phase241_hard_gate_pass_rows | 5 | Hard gates passed |
| phase241_hard_gate_rows | 5 | Hard gates evaluated |
| phase241_one_date_diagnostic_candidate_survived | 0 | One-date diagnostic survived; still not acceptance |
| phase241_full_five_date_acceptance_allowed | 0 | One-date diagnostic cannot satisfy full acceptance |
| phase241_strategy_promotion_allowed | 0 | No strategy promotion from Phase241 |
| phase241_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase241 |
| phase241_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase241 |
| phase241_next_best_action | close_or_redesign_phase237_candidate_after_one_date_unseen_real_l2_diagnostic_failure_no_paper_live | Recommended next milestone |

## Diagnostic Summary

| candidate_id | diagnostic_trade_rows | diagnostic_net_pnl_inr | diagnostic_gross_pnl_inr | diagnostic_cost_pnl_drag_inr | diagnostic_dates | diagnostic_symbols | diagnostic_positive_symbols | diagnostic_precision_cost_clear | diagnostic_max_symbol_contribution_abs | materialized_event_bars | materialized_symbols | raw_symbols | raw_parquet_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | 15 | 700.437 | 2553.23 | 1852.79 | 1 | 13 | 6 | 0.466667 | 1.1998 | 4832 | 32 | 32 | 50787 |

## Controls

| control_id | net_pnl_inr | passed | random_p95_net_pnl_inr | random_beat_fraction |
| --- | --- | --- | --- | --- |
| SIDE_FLIP | -4406.02 | True |  |  |
| RANDOM_SIDE_1000_RUNS | 700.437 | False | 1081.87 | 0.912 |
| COST_150 | -225.958 | False |  |  |
| COST_200 | -1152.35 | False |  |  |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P241_ONE_DATE_RAW_L2_PRESENT | True | 50787 | >0 raw parquet files | hard |
| P241_EVENT_BARS_MATERIALIZED | True | 4832 | >0 event bars | hard |
| P241_FROZEN_CANDIDATE_REPLAYED | True | 15 | >=1 frozen-candidate trade | hard |
| P241_DIAGNOSTIC_NET_POSITIVE | True | 700.437 | >0 one-date net P&L after costs | diagnostic |
| P241_DIAGNOSTIC_SYMBOL_BREADTH | True | 13 | >=5 symbols on one-date diagnostic | diagnostic |
| P241_DIAGNOSTIC_CONTROLS | False | 1 | >=3 / 4 controls pass | diagnostic |
| P241_FULL_ACCEPTANCE_CLOSED_ONE_DATE_ONLY | True | 1 | 1 | hard |
| P241_NO_PAPER_LIVE_OR_PROMOTION_UNLOCK | True | 0 | 0 | hard |

## Symbol Inventory

| trade_date | exchange | symbol | source_1s_rows | raw_parquet_files |
| --- | --- | --- | --- | --- |
| 2026-07-17 | NSE | ADANIPORTS | 9788 | 1587 |
| 2026-07-17 | NSE | AXISBANK | 15187 | 1587 |
| 2026-07-17 | NSE | BAJAJ-AUTO | 16014 | 1587 |
| 2026-07-17 | NSE | BANKBEES | 12160 | 1587 |
| 2026-07-17 | NSE | BHARTIARTL | 11307 | 1587 |
| 2026-07-17 | NSE | BPCL | 7766 | 1587 |
| 2026-07-17 | NSE | BRITANNIA | 6408 | 1587 |
| 2026-07-17 | NSE | CIPLA | 9665 | 1588 |
| 2026-07-17 | NSE | DRREDDY | 9658 | 1587 |
| 2026-07-17 | NSE | GOLDBEES | 9591 | 1587 |
| 2026-07-17 | NSE | HCLTECH | 11264 | 1587 |
| 2026-07-17 | NSE | HDFCBANK | 16885 | 1587 |
| 2026-07-17 | NSE | HINDUNILVR | 10211 | 1587 |
| 2026-07-17 | NSE | ICICIBANK | 15199 | 1587 |
| 2026-07-17 | NSE | INFY | 15746 | 1587 |
| 2026-07-17 | NSE | ITBEES | 7084 | 1587 |
| 2026-07-17 | NSE | ITC | 16719 | 1588 |
| 2026-07-17 | NSE | JUNIORBEES | 14291 | 1587 |
| 2026-07-17 | NSE | KOTAKBANK | 12686 | 1587 |
| 2026-07-17 | NSE | LT | 14368 | 1588 |
| 2026-07-17 | NSE | M&M | 13089 | 1587 |
| 2026-07-17 | NSE | MARUTI | 12478 | 1587 |
| 2026-07-17 | NSE | NESTLEIND | 9219 | 1587 |
| 2026-07-17 | NSE | NIFTYBEES | 12712 | 1587 |
| 2026-07-17 | NSE | ONGC | 10037 | 1587 |
| 2026-07-17 | NSE | RELIANCE | 14957 | 1587 |
| 2026-07-17 | NSE | SBIN | 14058 | 1587 |
| 2026-07-17 | NSE | SUNPHARMA | 12336 | 1587 |
| 2026-07-17 | NSE | TCS | 16592 | 1587 |
| 2026-07-17 | NSE | TECHM | 15841 | 1587 |
| 2026-07-17 | NSE | ULTRACEMCO | 8714 | 1587 |
| 2026-07-17 | NSE | WIPRO | 13263 | 1587 |

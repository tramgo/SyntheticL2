# Phase342 Official-Catalyst Real-Day Survivor Diagnostic Execution

Generated: 2026-08-11T07:55:44.687845+00:00

Phase342 executes the no-lookahead official-catalyst diagnostic on local raw Zerodha WebSocket top-five L2 ticks. It is still diagnostic-only.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase342_official_catalyst_real_day_survivor_diagnostic_execution_complete | 1 | Phase342 execution completed |
| phase342_phase341_complete | 1 | Phase341 complete |
| phase342_work_order_rows | 98 | Work-order rows |
| phase342_filled_trade_rows | 98 | Rows with entry/exit ticks |
| phase342_capacity_selected_trade_rows | 37 | Capacity-capped selected rows |
| phase342_capacity_capped_net_pnl_inr | -2644.99 | Capacity-capped net PnL |
| phase342_capacity_capped_annualized_return_pct | -38.0879 | Capacity-capped fixed-capital annualized return |
| phase342_capacity_capped_positive_symbol_date_cells | 8 | Capacity-capped positive symbol-date cells |
| phase342_isolated_all_events_net_pnl_inr | -8858.83 | All isolated-event diagnostic net PnL |
| phase342_isolated_all_events_annualized_return_pct | -127.567 | All isolated-event diagnostic fixed-capital annualized return |
| phase342_sbin_filled_rows | 8 | SBIN filled diagnostic rows |
| phase342_sbin_capacity_selected_rows | 3 | SBIN capacity-selected rows |
| phase342_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned cost model |
| phase342_cost_profile | zerodha_2x_all_in_cost_proxy | 2x cost profile |
| phase342_strategy_promotion_allowed | 0 | No promotion |
| phase342_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase342_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase342_hard_gate_pass_rows | 8 | Passed hard gates |
| phase342_hard_gate_rows | 8 | Hard gates |
| phase342_next_best_action | run_phase343_official_catalyst_real_day_diagnostic_interpretation_no_paper_live | Recommended next action |

## Portfolio summary

| scope | trade_rows | diagnostic_trade_dates | symbols | positive_trade_rows | positive_symbol_date_cells | net_pnl_inr | side_flip_net_pnl_inr | annualized_return_pct | side_flip_annualized_return_pct | initial_capital_inr | annualization_diagnostic_days |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| isolated_all_events_diagnostic | 98 | 7 | 23 | 35 | 26 | -8858.83 | -23427.9 | -127.567 | -337.362 | 250000 | 7 |
| capacity_capped_portfolio_diagnostic | 37 | 7 | 16 | 10 | 8 | -2644.99 | -9533.19 | -38.0879 | -137.278 | 250000 | 7 |

## Gate evaluation

| gate_id | passed | observed | required |
| --- | --- | --- | --- |
| P342_PHASE341_COMPLETE | True | 1 | 1 |
| P342_EXECUTION_ALLOWED_BY_PRECOMMIT | True | 1 | 1 |
| P342_WORK_ORDER_ROWS_RECONCILED | True | 98/98 | all |
| P342_FILLED_DIAGNOSTIC_ROWS_PRESENT | True | 98 | >0 |
| P342_CAPACITY_CAPPED_ROWS_PRESENT | True | 37 | >0 |
| P342_FIXED_CAPITAL_SUMMARY_PRESENT | True | present | present |
| P342_COST_MODEL_PINNED | True | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | pinned |
| P342_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | True | closed | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened by Phase342.
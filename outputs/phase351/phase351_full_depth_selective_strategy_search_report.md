# Phase351 Full-Depth Selective Dense Strategy Search

Phase351 tests lower-turnover full-depth selective strategies on the existing dense synthetic top-five market-by-price lake.
It is a strategy-search milestone, not a paper/live or deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase351_dense_input_root | raw_synthetic_l2_dense_full_year | Dense top-five input root |
| phase351_shards_requested | 32 | Shard limit requested |
| phase351_shards_scanned | 32 | Dense parquet shards scanned |
| phase351_strategy_rows | 3 | Full-depth selective strategies tested |
| phase351_execution_profile_rows | 3 | Execution profiles tested |
| phase351_event_ledger_rows | 162 | Daily/symbol event result rows |
| phase351_scenario_rows | 9 | Scenario summary rows |
| phase351_above12_rows | 0 | Rows above 12% fixed-capital annualized diagnostic |
| phase351_acceptance_candidate_rows | 0 | Rows passing event floor, breadth, and >12 diagnostic |
| phase351_initial_capital_inr | 1e+06 | Fixed annual return denominator |
| phase351_order_notional_inr | 75000 | Per-event notional below 100000 |
| phase351_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model used |
| phase351_strategy_replay_allowed | 0 | No replay unlock |
| phase351_strategy_promotion_allowed | 0 | No promotion unlock |
| phase351_paper_or_live_acceptance_allowed | 0 | No paper/live unlock |
| phase351_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase351_next_best_action | interpret_phase351_or_expand_if_acceptance_candidates_exist | Recommended next milestone |

## Top Scenario Summary

| strategy_id | execution_profile | fill_model_id | horizon_ticks | trade_dates | scheduled_events | expected_filled_events | positive_symbols | positive_symbol_dates | expected_net_pnl_inr | annualized_pct_fixed_capital | avg_fill_probability | avg_depth25_materiality | avg_abs_deep_imbalance_2_5 | avg_spread_bps | worst_event_pnl_inr | above12 | event_floor_met | breadth_met | acceptance_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P351_FULL_DEPTH_SHOCK_REVERSAL | passive_pessimistic_back_of_queue_cost200 | P351_PASSIVE_PESSIMISTIC_BACK_OF_QUEUE | 6 | 1 | 761 | 204.516 | 0 | 0 | -41721.6 | -4.17216 | 0.271229 | 0.882351 | 0.40636 | 2.14172 | -1189.53 | 0 | 1 | 0 | 0 |
| P351_FULL_DEPTH_SHOCK_REVERSAL | passive_base_back_of_queue_cost200 | P351_PASSIVE_BASE_BACK_OF_QUEUE | 6 | 1 | 761 | 306.773 | 0 | 0 | -56013.2 | -5.60132 | 0.406844 | 0.882351 | 0.40636 | 2.14172 | -1168.33 | 0 | 1 | 0 | 0 |
| P351_FULL_DEPTH_SHOCK_REVERSAL | taker_cost200_fixed_capital | P351_TAKER_DETERMINISTIC | 6 | 1 | 761 | 761 | 0 | 0 | -127652 | -12.7652 | 1 | 0.882351 | 0.40636 | 2.14172 | -1152.7 | 0 | 1 | 0 | 0 |
| P351_VOLUME_ABSORPTION_REVERSAL | passive_pessimistic_back_of_queue_cost200 | P351_PASSIVE_PESSIMISTIC_BACK_OF_QUEUE | 6 | 1 | 2364 | 639.838 | 0 | 0 | -129297 | -12.9297 | 0.270985 | 0.882351 | 0.391075 | 2.16619 | -1189.53 | 0 | 1 | 0 | 0 |
| P351_VOLUME_ABSORPTION_REVERSAL | passive_base_back_of_queue_cost200 | P351_PASSIVE_BASE_BACK_OF_QUEUE | 6 | 1 | 2364 | 959.758 | 0 | 0 | -173598 | -17.3598 | 0.406477 | 0.882351 | 0.391075 | 2.16619 | -1168.33 | 0 | 1 | 0 | 0 |
| P351_VOLUME_ABSORPTION_REVERSAL | taker_cost200_fixed_capital | P351_TAKER_DETERMINISTIC | 6 | 1 | 2364 | 2364 | 0 | 0 | -390623 | -39.0623 | 1 | 0.882351 | 0.391075 | 2.16619 | -1152.7 | 0 | 1 | 0 | 0 |
| P351_DEEP_PRESSURE_CONTINUATION | passive_pessimistic_back_of_queue_cost200 | P351_PASSIVE_PESSIMISTIC_BACK_OF_QUEUE | 6 | 1 | 17615 | 4787.83 | 0 | 0 | -963620 | -96.362 | 0.271894 | 0.882348 | 0.374361 | 2.07519 | -1189.53 | 0 | 1 | 0 | 0 |
| P351_DEEP_PRESSURE_CONTINUATION | passive_base_back_of_queue_cost200 | P351_PASSIVE_BASE_BACK_OF_QUEUE | 6 | 1 | 17615 | 7181.75 | 0 | 0 | -1.29409e+06 | -129.409 | 0.407841 | 0.882348 | 0.374361 | 2.07519 | -1168.33 | 0 | 1 | 0 | 0 |
| P351_DEEP_PRESSURE_CONTINUATION | taker_cost200_fixed_capital | P351_TAKER_DETERMINISTIC | 6 | 1 | 17615 | 17615 | 0 | 0 | -2.89153e+06 | -289.153 | 1 | 0.882348 | 0.374361 | 2.07519 | -1152.7 | 0 | 1 | 0 | 0 |

## Gates

| gate_id | passed | evidence |
| --- | --- | --- |
| P351_PHASE52_RECONCILED | 1 | Phase52 stale-running marker reconciled before Phase351 search. |
| P351_FULL_DEPTH_1_5_USED | 1 | All rows use top-five depth fields. |
| P351_DEPTH_2_5_MATERIALITY_USED | 1 | Depth levels 2-5 materiality is required. |
| P351_L1_ONLY_FORBIDDEN | 1 | No L1-only variant rows. |
| P351_COST200_FIXED_CAPITAL | 1 | Zerodha cost model at 2x stress with fixed initial capital. |
| P351_PASSIVE_REALISM_APPLIED | 1 | Passive profiles include fill probability, adverse selection, and forced flatten proxies. |
| P351_NO_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | No promotion, paper/live, or deployable profitability claim. |

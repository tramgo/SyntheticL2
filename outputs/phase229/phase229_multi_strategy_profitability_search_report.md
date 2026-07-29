# Phase229 Multi-strategy Profitability Search

Generated UTC: 2026-07-29T05:57:21.087514+00:00

Phase229 pivots from additional guardrail-only work into a concrete strategy-discovery screen.
It ranks already executed synthetic tick/depth strategy replays net of modeled Zerodha-style costs.
A positive row here means synthetic-candidate evidence only; it is not paper/live readiness or a deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase229_multi_strategy_profitability_search_complete | 1 | Strategy discovery ranking completed |
| phase229_source_summary_rows | 36 | Strategy/profile summary rows ranked |
| phase229_distinct_strategy_ids | 12 | Distinct strategy ids evaluated |
| phase229_realistic_profile_rows | 24 | Retail/stressed profile rows evaluated |
| phase229_control_profile_rows | 12 | Zero-latency control profile rows evaluated |
| phase229_phase164_trade_ledger_rows | 37424 | Phase164 daily/symbol/profile ledger rows referenced |
| phase229_phase164_trade_dates | 252 | Phase164 trade dates referenced |
| phase229_phase164_symbols | 32 | Phase164 symbols referenced |
| phase229_positive_realistic_candidate_rows | 0 | Positive net-after-cost realistic profile rows |
| phase229_positive_any_profile_rows | 0 | Positive net-after-cost rows across all profiles |
| phase229_best_strategy_id | P164_S06_ABSORPTION_REVERSAL | Best strategy/profile by annual net P&L |
| phase229_best_execution_profile | zero_latency_spread_only_control | Best execution profile by annual net P&L |
| phase229_best_annual_net_pnl_inr | -189513 | Best annual net P&L in ranked universe |
| phase229_strategy_promotion_allowed | 0 | No promotion from synthetic search alone |
| phase229_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from synthetic search alone |
| phase229_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from synthetic search alone |
| phase229_next_best_action | run_phase230_expand_low_turnover_high_edge_strategy_search_no_generator_profit_tuning | Next strategy-discovery milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | interpretation |
| --- | --- | --- | --- | --- |
| P229_INPUT_UNIVERSE_AVAILABLE | True | 36 | >0 strategy/profile rows | Existing synthetic replay summaries are available for strategy discovery. |
| P229_SEVERAL_STRATEGIES_EVALUATED | True | 12 | >=3 distinct strategy ids | The phase tests several existing strategy forms instead of a single shard loop. |
| P229_REALISTIC_COST_PROFILES_EVALUATED | True | 24 | >0 retail/stressed profile rows | Ranking includes costed realistic retail execution profiles. |
| P229_SYNTHETIC_PROFITABLE_REALISTIC_CANDIDATE_FOUND | False | 0 | >0 positive realistic net-after-cost rows | If this fails, no tested strategy is currently profitable after realistic modeled costs. |
| P229_SYNTHETIC_PROFITABLE_ANY_PROFILE_FOUND | False | 0 | >0 positive net-after-cost rows | Diagnostic control profitability is tracked separately from realistic tradability. |

## Top Ranked Strategy/Profile Rows

| source_phase | strategy_id | source_strategy_id | feature_family | feature_status | execution_profile | trade_dates | trades | annual_net_pnl_inr | mean_net_return_per_trade | mean_gross_return_per_trade | mean_cost_return_per_trade | worst_daily_net_pnl_inr | max_drawdown_inr | worst_trade_pnl_inr | positive_day_fraction | annualized_sharpe_proxy | positive_after_costs | risk_proxy_pass | synthetic_replay_candidate | is_realistic_profile | is_control_profile | cost_drag_ratio_to_abs_gross | candidate_class | next_diagnostic |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase164_full_year_synthetic | P164_S06_ABSORPTION_REVERSAL | S06 | absorption_exhaustion_reversal | replayable_from_local_l1_l5_book_state | zero_latency_spread_only_control | 233 | 9603 | -189513 | -0.000197347 | 0 | 0.000197347 | -13555.1 | -189505 | -43.1143 | 0 | -6.52241 | False | True | False | False | True |  | rejected_negative_after_cost | gross_edge_smaller_than_cost_drag |
| phase164_full_year_synthetic | P164_S05_MICROPRICE_FILTER | S05 | microprice_with_depth_filter | replayable_from_local_l1_l5_book_state | zero_latency_spread_only_control | 61 | 35518 | -320466 | -9.02264e-05 | 3.32689e-07 | 9.05591e-05 | -45908.3 | -317921 | -1793.05 | 0 | -10.9357 | False | False | False | False | True | 272.203 | rejected_negative_after_cost | gross_edge_smaller_than_cost_drag |
| phase164_full_year_synthetic | P164_S09_QUEUE_IMBALANCE_SCALP | S09 | queue_imbalance_scalping_guarded | replayable_from_local_l1_l5_book_state_guarded_not_phase52_dense_id | zero_latency_spread_only_control | 95 | 79552 | -692233 | -8.70165e-05 | 1.03155e-06 | 8.8048e-05 | -34334.6 | -687912 | -741.707 | 0 | -21.182 | False | False | False | False | True | 85.3552 | rejected_negative_after_cost | gross_edge_smaller_than_cost_drag |
| phase164_full_year_synthetic | P164_S04_TRADE_FLOW_DEPTH | S04 | trade_flow_depth_confirmation | replayable_from_local_l1_l5_book_state | zero_latency_spread_only_control | 225 | 41762 | -809134 | -0.000193749 | 0 | 0.000193749 | -41666.2 | -808314 | -51.471 | 0 | -7.80341 | False | False | False | False | True |  | rejected_negative_after_cost | gross_edge_smaller_than_cost_drag |
| phase164_full_year_synthetic | P164_S06_ABSORPTION_REVERSAL | S06 | absorption_exhaustion_reversal | replayable_from_local_l1_l5_book_state | retail_marketable_default | 233 | 9417 | -1.38206e+06 | -0.00146762 | 0 | 0.00146762 | -81625 | -1.38195e+06 | -217.024 | 0 | -7.96365 | False | False | False | True | False |  | rejected_negative_after_cost | gross_edge_smaller_than_cost_drag |
| phase164_full_year_synthetic | P164_S06_ABSORPTION_REVERSAL | S06 | absorption_exhaustion_reversal | replayable_from_local_l1_l5_book_state | stressed_retail | 233 | 9417 | -1.89422e+06 | -0.00201149 | 0 | 0.00201149 | -115444 | -1.89408e+06 | -318.253 | 0 | -7.72096 | False | False | False | True | False |  | rejected_negative_after_cost | gross_edge_smaller_than_cost_drag |
| phase164_full_year_synthetic | P164_S03_LIQUIDITY_VACUUM | S03 | liquidity_vacuum_breakout | replayable_from_local_l1_l5_book_state | zero_latency_spread_only_control | 55 | 274177 | -3.3266e+06 | -0.00012133 | 0 | 0.00012133 | -278691 | -3.25044e+06 | -51.5187 | 0 | -13.9373 | False | False | False | False | True |  | rejected_negative_after_cost | turnover_too_high_costs_dominate |
| phase164_full_year_synthetic | P164_S05_MICROPRICE_FILTER | S05 | microprice_with_depth_filter | replayable_from_local_l1_l5_book_state | retail_marketable_default | 67 | 35249 | -4.04311e+06 | -0.00114701 | 2.77814e-07 | 0.00114729 | -434670 | -4.00765e+06 | -1896.16 | 0 | -13.0501 | False | False | False | True | False | 4129.71 | rejected_negative_after_cost | gross_edge_smaller_than_cost_drag |
| phase167_cross_symbol_s08 | P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | S08 | cross_symbol_lead_lag | precommitted_phase167_single_s08_branch | zero_latency_spread_only_control | 252 | 273062 | -4.1439e+06 | -0.000151757 | -1.56119e-08 | 0.000151741 | 0 | 0 | -314.325 | 0 | 0 | False | False | False | False | True | 9719.6 | rejected_negative_after_cost | turnover_too_high_costs_dominate |
| phase164_full_year_synthetic | P164_S01_MLOFI_BREAKOUT | S01 | momentum_breakout_mlofi | replayable_from_local_l1_l5_book_state | zero_latency_spread_only_control | 240 | 224845 | -4.73255e+06 | -0.000210481 | -9.95981e-07 | 0.000209485 | -334617 | -4.73202e+06 | -755.755 | 0 | -6.68854 | False | False | False | False | True | 210.33 | rejected_negative_after_cost | turnover_too_high_costs_dominate |
| phase164_full_year_synthetic | P164_S05_MICROPRICE_FILTER | S05 | microprice_with_depth_filter | replayable_from_local_l1_l5_book_state | stressed_retail | 67 | 35235 | -5.20578e+06 | -0.00147745 | 2.77925e-07 | 0.00147772 | -573650 | -5.16066e+06 | -1926.59 | 0 | -12.8122 | False | False | False | True | False | 5316.99 | rejected_negative_after_cost | gross_edge_smaller_than_cost_drag |
| phase164_full_year_synthetic | P164_S04_TRADE_FLOW_DEPTH | S04 | trade_flow_depth_confirmation | replayable_from_local_l1_l5_book_state | retail_marketable_default | 225 | 41392 | -6.03399e+06 | -0.00145777 | 0 | 0.00145777 | -275080 | -6.02609e+06 | -242.094 | 0 | -8.85837 | False | False | False | True | False |  | rejected_negative_after_cost | gross_edge_smaller_than_cost_drag |

## Family Summary

| source_phase | source_strategy_id | feature_family | profiles_evaluated | realistic_profiles_evaluated | control_profiles_evaluated | total_trades | positive_after_cost_profiles | synthetic_candidate_profiles | best_strategy_id | best_execution_profile | best_annual_net_pnl_inr | best_realistic_execution_profile | best_realistic_annual_net_pnl_inr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase164_full_year_synthetic | S06 | absorption_exhaustion_reversal | 3 | 2 | 1 | 28437 | 0 | 0 | P164_S06_ABSORPTION_REVERSAL | zero_latency_spread_only_control | -189513 | retail_marketable_default | -1.38206e+06 |
| phase164_full_year_synthetic | S05 | microprice_with_depth_filter | 3 | 2 | 1 | 106002 | 0 | 0 | P164_S05_MICROPRICE_FILTER | zero_latency_spread_only_control | -320466 | retail_marketable_default | -4.04311e+06 |
| phase164_full_year_synthetic | S04 | trade_flow_depth_confirmation | 3 | 2 | 1 | 124546 | 0 | 0 | P164_S04_TRADE_FLOW_DEPTH | zero_latency_spread_only_control | -809134 | retail_marketable_default | -6.03399e+06 |
| phase164_full_year_synthetic | S09 | queue_imbalance_scalping_guarded | 3 | 2 | 1 | 238340 | 0 | 0 | P164_S09_QUEUE_IMBALANCE_SCALP | zero_latency_spread_only_control | -692233 | retail_marketable_default | -9.05188e+06 |
| phase167_cross_symbol_s08 | S08 | cross_symbol_lead_lag | 3 | 2 | 1 | 817814 | 0 | 0 | P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | zero_latency_spread_only_control | -4.1439e+06 | retail_marketable_default | -2.82511e+07 |
| phase164_full_year_synthetic | S01 | momentum_breakout_mlofi | 3 | 2 | 1 | 670081 | 0 | 0 | P164_S01_MLOFI_BREAKOUT | zero_latency_spread_only_control | -4.73255e+06 | retail_marketable_default | -3.35295e+07 |
| phase164_full_year_synthetic | S03 | liquidity_vacuum_breakout | 3 | 2 | 1 | 817583 | 0 | 0 | P164_S03_LIQUIDITY_VACUUM | zero_latency_spread_only_control | -3.3266e+06 | retail_marketable_default | -3.37073e+07 |
| phase164_full_year_synthetic | S02 | multi_level_order_flow_imbalance | 3 | 2 | 1 | 2539367 | 0 | 0 | P164_S02_MULTI_LEVEL_OFI | zero_latency_spread_only_control | -1.04276e+07 | retail_marketable_default | -1.04826e+08 |
| phase164_full_year_synthetic | S07 | imbalance_mean_reversion | 3 | 2 | 1 | 3087594 | 0 | 0 | P164_S07_IMBALANCE_MEAN_REVERSION | zero_latency_spread_only_control | -1.15997e+07 | retail_marketable_default | -1.24628e+08 |
| phase52_dense_partial | DENSE_S01_L1_IMBALANCE | DENSE_S01_L1_IMBALANCE | 3 | 2 | 1 | 268269333 | 0 | 0 | DENSE_S01_L1_IMBALANCE | zero_latency_spread_only_control | -1.54677e+09 | retail_marketable_default | -1.23948e+10 |
| phase52_dense_partial | DENSE_S03_1T_MOMENTUM | DENSE_S03_1T_MOMENTUM | 3 | 2 | 1 | 263585104 | 0 | 0 | DENSE_S03_1T_MOMENTUM | zero_latency_spread_only_control | -2.07147e+09 | retail_marketable_default | -1.38106e+10 |
| phase52_dense_partial | DENSE_S02_MICROPRICE | DENSE_S02_MICROPRICE | 3 | 2 | 1 | 265175128 | 0 | 0 | DENSE_S02_MICROPRICE | zero_latency_spread_only_control | -2.20327e+09 | retail_marketable_default | -1.42514e+10 |

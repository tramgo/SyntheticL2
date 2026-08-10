# Phase322 Event-Catalyst Multi-Event Strategy Search Training-Only

Phase322 executes the precommitted training-only strategy search over the Phase320 feature matrix.
It reports fixed-capital research diagnostics only. It does not replay, promote, open paper/live acceptance, or claim deployable profitability.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase322_multievent_strategy_search_training_complete | 1 | Phase322 training-only strategy search completed |
| phase322_scenario_rows | 138240 | Scenario rows evaluated |
| phase322_family_rows | 10 | Distinct families evaluated |
| phase322_cost200_scenario_rows | 34560 | 2x cost-stress scenarios |
| phase322_passive_aware_scenario_rows | 69120 | Passive-aware scenarios |
| phase322_above12_annualized_scenario_rows | 3127 | Scenarios above 12% annualized research threshold |
| phase322_cost200_above12_scenario_rows | 320 | 2x cost scenarios above 12% annualized |
| phase322_cost200_acceptance_grade_candidate_rows | 0 | 2x cost scenarios meeting acceptance-grade breadth |
| phase322_best_scenario_id | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_base | Best scenario id |
| phase322_best_family_id | P321_DEPTH_ACCEL_REVERSAL | Best scenario family |
| phase322_best_execution_policy | taker_entry_taker_exit | Best execution policy |
| phase322_best_cost_profile | zerodha_base | Best cost profile |
| phase322_best_annualized_return_pct | 85.0813 | Best annualized fixed-capital research metric |
| phase322_best_scheduled_event_rows | 8 | Best scheduled event rows |
| phase322_best_cost200_annualized_return_pct | 64.2398 | Best 2x-cost annualized return |
| phase322_best_cost200_scheduled_event_rows | 8 | Best 2x-cost scheduled events |
| phase322_annualized_denominator | fixed_initial_capital | No unlimited capital denominator |
| phase322_strategy_replay_allowed | 0 | No replay |
| phase322_strategy_promotion_allowed | 0 | No promotion |
| phase322_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase322_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase322_hard_gate_pass_rows | 9 | Passed hard gates |
| phase322_hard_gate_rows | 9 | Hard gates |
| phase322_next_best_action | run_phase323_event_catalyst_multievent_strategy_search_interpretation_no_replay | Recommended next action |

## Interpretation metrics

| metric | value | description |
| --- | --- | --- |
| phase322_best_scenario_id | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_base | Best scenario by annualized return |
| phase322_best_family_id | P321_DEPTH_ACCEL_REVERSAL | Best scenario family |
| phase322_best_execution_policy | taker_entry_taker_exit | Best scenario execution policy |
| phase322_best_cost_profile | zerodha_base | Best scenario cost profile |
| phase322_best_annualized_return_pct | 85.0813 | Best annualized fixed-capital research metric |
| phase322_best_net_pnl_inr | 2700.99 | Best net P&L |
| phase322_best_scheduled_event_rows | 8 | Best scheduled event rows |
| phase322_cost200_above12_scenario_rows | 320 | 2x cost scenarios above 12% annualized |
| phase322_cost200_acceptance_grade_candidate_rows | 0 | 2x cost scenarios meeting acceptance-grade event/date/symbol floor |
| phase322_best_cost200_annualized_return_pct | 64.2398 | Best 2x-cost annualized return |
| phase322_best_cost200_scheduled_event_rows | 8 | Best 2x-cost scheduled events |
| phase322_broadest_scenario_id | P321_MICROPRICE_DEPTH_CONFIRM_H60_all_nonzero_signal_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC2_zerodha_base | Scenario with broadest event support |
| phase322_broadest_annualized_return_pct | 59.1363 | Broadest scenario annualized return |
| phase322_broadest_scheduled_event_rows | 10 | Broadest scheduled event rows |

## Top scenarios

| family_id | horizon_seconds | threshold_policy | cost_profile | initial_capital_inr | fixed_notional_inr | max_concurrent_positions | side_policy | execution_policy | scheduled_event_rows | symbol_rows | observed_trade_dates | trade_rows | avg_fill_probability | gross_pnl_inr | cost_inr | passive_penalty_inr | net_pnl_inr | portfolio_return_pct | annualized_return_pct | above12_annualized | robust_event_floor_met | acceptance_grade_candidate | profitability_claim_allowed | scenario_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 1 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 3362.63 | 661.636 | 0 | 2700.99 | 2.70099 | 85.0813 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_base |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 2 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 3362.63 | 661.636 | 0 | 2700.99 | 2.70099 | 85.0813 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_base |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 4 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 3362.63 | 661.636 | 0 | 2700.99 | 2.70099 | 85.0813 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_base |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_plus_1bp_slippage | 100000 | 100000 | 1 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 3362.63 | 822.134 | 0 | 2540.5 | 2.5405 | 80.0256 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_plus_1bp_slippage |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_plus_1bp_slippage | 100000 | 100000 | 2 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 3362.63 | 822.134 | 0 | 2540.5 | 2.5405 | 80.0256 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_plus_1bp_slippage |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_plus_1bp_slippage | 100000 | 100000 | 4 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 3362.63 | 822.134 | 0 | 2540.5 | 2.5405 | 80.0256 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_plus_1bp_slippage |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_25pct_abs_signal | zerodha_base | 100000 | 100000 | 1 | long_only | taker_entry_taker_exit | 9 | 5 | 9 | 9 | 1 | 3431.29 | 744.32 | 0 | 2686.97 | 2.68697 | 75.2353 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_25pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_base |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_25pct_abs_signal | zerodha_base | 100000 | 100000 | 2 | long_only | taker_entry_taker_exit | 9 | 5 | 9 | 9 | 1 | 3431.29 | 744.32 | 0 | 2686.97 | 2.68697 | 75.2353 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_25pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_base |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_25pct_abs_signal | zerodha_base | 100000 | 100000 | 4 | long_only | taker_entry_taker_exit | 9 | 5 | 9 | 9 | 1 | 3431.29 | 744.32 | 0 | 2686.97 | 2.68697 | 75.2353 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_25pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_base |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_plus_2bp_slippage | 100000 | 100000 | 1 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 3362.63 | 982.632 | 0 | 2380 | 2.38 | 74.9699 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_plus_2bp_slippage |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_plus_2bp_slippage | 100000 | 100000 | 2 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 3362.63 | 982.632 | 0 | 2380 | 2.38 | 74.9699 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_plus_2bp_slippage |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_plus_2bp_slippage | 100000 | 100000 | 4 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 3362.63 | 982.632 | 0 | 2380 | 2.38 | 74.9699 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_plus_2bp_slippage |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_25pct_abs_signal | zerodha_plus_1bp_slippage | 100000 | 100000 | 1 | long_only | taker_entry_taker_exit | 9 | 5 | 9 | 9 | 1 | 3431.29 | 924.824 | 0 | 2506.47 | 2.50647 | 70.1811 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_25pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_plus_1bp_slippage |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_25pct_abs_signal | zerodha_plus_1bp_slippage | 100000 | 100000 | 2 | long_only | taker_entry_taker_exit | 9 | 5 | 9 | 9 | 1 | 3431.29 | 924.824 | 0 | 2506.47 | 2.50647 | 70.1811 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_25pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_plus_1bp_slippage |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_25pct_abs_signal | zerodha_plus_1bp_slippage | 100000 | 100000 | 4 | long_only | taker_entry_taker_exit | 9 | 5 | 9 | 9 | 1 | 3431.29 | 924.824 | 0 | 2506.47 | 2.50647 | 70.1811 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_25pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_plus_1bp_slippage |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_25pct_abs_signal | zerodha_plus_2bp_slippage | 100000 | 100000 | 1 | long_only | taker_entry_taker_exit | 9 | 5 | 9 | 9 | 1 | 3431.29 | 1105.33 | 0 | 2325.96 | 2.32596 | 65.127 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_25pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_plus_2bp_slippage |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_25pct_abs_signal | zerodha_plus_2bp_slippage | 100000 | 100000 | 2 | long_only | taker_entry_taker_exit | 9 | 5 | 9 | 9 | 1 | 3431.29 | 1105.33 | 0 | 2325.96 | 2.32596 | 65.127 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_25pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_plus_2bp_slippage |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_25pct_abs_signal | zerodha_plus_2bp_slippage | 100000 | 100000 | 4 | long_only | taker_entry_taker_exit | 9 | 5 | 9 | 9 | 1 | 3431.29 | 1105.33 | 0 | 2325.96 | 2.32596 | 65.127 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_25pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_plus_2bp_slippage |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 1 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 3362.63 | 1323.27 | 0 | 2039.36 | 2.03936 | 64.2398 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_2x_all_in_cost_proxy |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 2 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 3362.63 | 1323.27 | 0 | 2039.36 | 2.03936 | 64.2398 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 4 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 3362.63 | 1323.27 | 0 | 2039.36 | 2.03936 | 64.2398 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 1 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 2521.97 | 592.627 | 0 | 1929.35 | 1.92935 | 60.7744 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT75000_CONC1_zerodha_base |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 2 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 2521.97 | 592.627 | 0 | 1929.35 | 1.92935 | 60.7744 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT75000_CONC2_zerodha_base |
| P321_DEPTH_ACCEL_REVERSAL | 1800 | top_10pct_abs_signal | zerodha_base | 100000 | 75000 | 4 | long_only | taker_entry_taker_exit | 8 | 5 | 8 | 8 | 1 | 2521.97 | 592.627 | 0 | 1929.35 | 1.92935 | 60.7744 | 1 | 0 | 0 | 0 | P321_DEPTH_ACCEL_REVERSAL_H1800_top_10pct_abs_signal_long_only_taker_entry_taker_exit_CAP100000_NOT75000_CONC4_zerodha_base |
| P321_MICROPRICE_DEPTH_CONFIRM | 60 | all_nonzero_signal | zerodha_base | 100000 | 50000 | 2 | long_only | taker_entry_taker_exit | 10 | 4 | 10 | 20 | 1 | 3421.12 | 1074.45 | 0 | 2346.68 | 2.34668 | 59.1363 | 1 | 0 | 0 | 0 | P321_MICROPRICE_DEPTH_CONFIRM_H60_all_nonzero_signal_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC2_zerodha_base |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P322_PHASE321_COMPLETE | True | 1 | 1 | hard |
| P322_PHASE321_EXECUTION_ALLOWED | True | 1 | 1 | hard |
| P322_SCENARIOS_PRODUCED | True | 138240 | >0 | hard |
| P322_VARIANT_COVERAGE_COMPLETE | True | 138240/138240 | equal | hard |
| P322_COST200_SCENARIOS_PRESENT | True | 34560 | >0 | hard |
| P322_PASSIVE_AWARE_SCENARIOS_PRESENT | True | 69120 | >0 | hard |
| P322_FIXED_CAPITAL_DENOMINATOR | True | all_positive | all_positive | hard |
| P322_NO_PROFITABILITY_CLAIM | True | profitability_claim_allowed=0 | 0 | hard |
| P322_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

# Phase332 Event-Catalyst Expanded Strategy Search Training-Only

Phase332 executes the precommitted training-only strategy search over the Phase330 expanded feature matrix.
It reports fixed-capital research diagnostics only. It does not replay, promote, open paper/live acceptance, or claim deployable profitability.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase332_expanded_strategy_search_training_complete | 1 | Phase332 training-only strategy search completed |
| phase332_scenario_rows | 1036800 | Scenario rows evaluated |
| phase332_family_rows | 15 | Distinct families evaluated |
| phase332_cost200_scenario_rows | 259200 | 2x cost-stress scenarios |
| phase332_passive_aware_scenario_rows | 518400 | Passive-aware scenarios |
| phase332_event_bucket_policy_rows | 5 | Event-bucket policies evaluated |
| phase332_above12_annualized_scenario_rows | 564 | Scenarios above 12% annualized research threshold |
| phase332_cost200_above12_scenario_rows | 0 | 2x cost scenarios above 12% annualized |
| phase332_cost200_acceptance_grade_candidate_rows | 0 | 2x cost scenarios meeting acceptance-grade breadth |
| phase332_best_scenario_id | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_base | Best scenario id |
| phase332_best_family_id | P331_DEPTH_ACCEL_REVERSAL | Best scenario family |
| phase332_best_execution_policy | taker_entry_taker_exit | Best execution policy |
| phase332_best_cost_profile | zerodha_base | Best cost profile |
| phase332_best_event_bucket_policy | all_events | Best event bucket policy |
| phase332_best_annualized_return_pct | 30.5362 | Best annualized fixed-capital research metric |
| phase332_best_scheduled_event_rows | 40 | Best scheduled event rows |
| phase332_best_cost200_scenario_id | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | Best 2x-cost scenario id |
| phase332_best_cost200_annualized_return_pct | 11.5176 | Best 2x-cost annualized return |
| phase332_best_cost200_scheduled_event_rows | 40 | Best 2x-cost scheduled events |
| phase332_best_acceptance_grade_cost200_scenario_id |  | Best 2x-cost acceptance-grade scenario id |
| phase332_best_acceptance_grade_cost200_annualized_return_pct |  | Best 2x-cost acceptance-grade annualized return |
| phase332_scenario_parquet_written | 1 | Scenario parquet written |
| phase332_scenario_parquet_bytes | 18894815 | Scenario parquet bytes |
| phase332_annualized_denominator | fixed_initial_capital | No unlimited capital denominator |
| phase332_strategy_replay_allowed | 0 | No replay |
| phase332_strategy_promotion_allowed | 0 | No promotion |
| phase332_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase332_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase332_hard_gate_pass_rows | 10 | Passed hard gates |
| phase332_hard_gate_rows | 10 | Hard gates |
| phase332_next_best_action | run_phase333_event_catalyst_expanded_strategy_search_interpretation_no_replay | Recommended next action |

## Interpretation metrics

| metric | value | description |
| --- | --- | --- |
| phase332_best_scenario_id | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_base | Best scenario by annualized return |
| phase332_best_family_id | P331_DEPTH_ACCEL_REVERSAL | Best scenario family |
| phase332_best_execution_policy | taker_entry_taker_exit | Best scenario execution policy |
| phase332_best_cost_profile | zerodha_base | Best scenario cost profile |
| phase332_best_event_bucket_policy | all_events | Best event bucket policy |
| phase332_best_annualized_return_pct | 30.5362 | Best annualized fixed-capital research metric |
| phase332_best_net_pnl_inr | 4847.01 | Best net P&L |
| phase332_best_scheduled_event_rows | 40 | Best scheduled event rows |
| phase332_cost200_above12_scenario_rows | 0 | 2x cost scenarios above 12% annualized |
| phase332_cost200_acceptance_grade_candidate_rows | 0 | 2x cost scenarios meeting event/date/symbol floor |
| phase332_best_cost200_scenario_id | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | Best 2x-cost scenario id |
| phase332_best_cost200_annualized_return_pct | 11.5176 | Best 2x-cost annualized return |
| phase332_best_cost200_scheduled_event_rows | 40 | Best 2x-cost scheduled events |
| phase332_best_acceptance_grade_cost200_scenario_id |  | Best 2x-cost acceptance-grade scenario id |
| phase332_best_acceptance_grade_cost200_annualized_return_pct |  | Best 2x-cost acceptance-grade annualized return |
| phase332_broadest_scenario_id | P331_DEPTH_ACCEL_REVERSAL_H900_all_nonzero_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_base | Scenario with broadest event support |
| phase332_broadest_annualized_return_pct | 23.8371 | Broadest scenario annualized return |
| phase332_broadest_scheduled_event_rows | 50 | Broadest scheduled event rows |

## Top scenarios

| family_id | horizon_seconds | threshold_policy | cost_profile | initial_capital_inr | fixed_notional_inr | max_concurrent_positions | side_policy | execution_policy | event_bucket_policy | scheduled_event_rows | symbol_rows | observed_trade_dates | trade_rows | avg_fill_probability | gross_pnl_inr | cost_inr | passive_penalty_inr | net_pnl_inr | portfolio_return_pct | annualized_return_pct | above12_annualized | robust_event_floor_met | acceptance_grade_candidate | profitability_claim_allowed | scenario_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 1 | long_only | taker_entry_taker_exit | all_events | 40 | 6 | 40 | 40 | 1 | 8154.87 | 3307.86 | 0 | 4847.01 | 4.84701 | 30.5362 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 2 | long_only | taker_entry_taker_exit | all_events | 40 | 6 | 40 | 40 | 1 | 8154.87 | 3307.86 | 0 | 4847.01 | 4.84701 | 30.5362 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 4 | long_only | taker_entry_taker_exit | all_events | 40 | 6 | 40 | 40 | 1 | 8154.87 | 3307.86 | 0 | 4847.01 | 4.84701 | 30.5362 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 1 | long_only | taker_entry_taker_exit | macro_or_index_context | 40 | 6 | 40 | 40 | 1 | 8154.87 | 3307.86 | 0 | 4847.01 | 4.84701 | 30.5362 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 2 | long_only | taker_entry_taker_exit | macro_or_index_context | 40 | 6 | 40 | 40 | 1 | 8154.87 | 3307.86 | 0 | 4847.01 | 4.84701 | 30.5362 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 100000 | 100000 | 4 | long_only | taker_entry_taker_exit | macro_or_index_context | 40 | 6 | 40 | 40 | 1 | 8154.87 | 3307.86 | 0 | 4847.01 | 4.84701 | 30.5362 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_25pct_abs_signal | zerodha_base | 100000 | 50000 | 2 | long_only | taker_entry_taker_exit | all_events | 48 | 13 | 48 | 90 | 1 | 10014.6 | 4834.44 | 0 | 5180.18 | 5.18018 | 27.196 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_25pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC2_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_25pct_abs_signal | zerodha_base | 100000 | 50000 | 4 | long_only | taker_entry_taker_exit | all_events | 48 | 13 | 48 | 90 | 1 | 10014.6 | 4834.44 | 0 | 5180.18 | 5.18018 | 27.196 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_25pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC4_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_25pct_abs_signal | zerodha_base | 100000 | 50000 | 2 | long_only | taker_entry_taker_exit | macro_or_index_context | 48 | 13 | 48 | 90 | 1 | 10014.6 | 4834.44 | 0 | 5180.18 | 5.18018 | 27.196 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_25pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC2_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_25pct_abs_signal | zerodha_base | 100000 | 50000 | 4 | long_only | taker_entry_taker_exit | macro_or_index_context | 48 | 13 | 48 | 90 | 1 | 10014.6 | 4834.44 | 0 | 5180.18 | 5.18018 | 27.196 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_25pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC4_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 2 | long_only | taker_entry_taker_exit | all_events | 40 | 10 | 40 | 69 | 1 | 7991.26 | 3706.6 | 0 | 4284.66 | 4.28466 | 26.9934 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC2_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 4 | long_only | taker_entry_taker_exit | all_events | 40 | 10 | 40 | 69 | 1 | 7991.26 | 3706.6 | 0 | 4284.66 | 4.28466 | 26.9934 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC4_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 2 | long_only | taker_entry_taker_exit | macro_or_index_context | 40 | 10 | 40 | 69 | 1 | 7991.26 | 3706.6 | 0 | 4284.66 | 4.28466 | 26.9934 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC2_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 100000 | 50000 | 4 | long_only | taker_entry_taker_exit | macro_or_index_context | 40 | 10 | 40 | 69 | 1 | 7991.26 | 3706.6 | 0 | 4284.66 | 4.28466 | 26.9934 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC4_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_25pct_abs_signal | zerodha_base | 250000 | 100000 | 2 | long_only | taker_entry_taker_exit | all_events | 48 | 13 | 48 | 90 | 1 | 20029.3 | 7442.61 | 0 | 12586.6 | 5.03466 | 26.432 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_25pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_25pct_abs_signal | zerodha_base | 250000 | 100000 | 4 | long_only | taker_entry_taker_exit | all_events | 48 | 13 | 48 | 90 | 1 | 20029.3 | 7442.61 | 0 | 12586.6 | 5.03466 | 26.432 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_25pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_25pct_abs_signal | zerodha_base | 250000 | 100000 | 2 | long_only | taker_entry_taker_exit | macro_or_index_context | 48 | 13 | 48 | 90 | 1 | 20029.3 | 7442.61 | 0 | 12586.6 | 5.03466 | 26.432 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_25pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_25pct_abs_signal | zerodha_base | 250000 | 100000 | 4 | long_only | taker_entry_taker_exit | macro_or_index_context | 48 | 13 | 48 | 90 | 1 | 20029.3 | 7442.61 | 0 | 12586.6 | 5.03466 | 26.432 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_25pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 250000 | 100000 | 2 | long_only | taker_entry_taker_exit | all_events | 40 | 10 | 40 | 69 | 1 | 15982.5 | 5706.03 | 0 | 10276.5 | 4.1106 | 25.8968 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 250000 | 100000 | 4 | long_only | taker_entry_taker_exit | all_events | 40 | 10 | 40 | 69 | 1 | 15982.5 | 5706.03 | 0 | 10276.5 | 4.1106 | 25.8968 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 250000 | 100000 | 2 | long_only | taker_entry_taker_exit | macro_or_index_context | 40 | 10 | 40 | 69 | 1 | 15982.5 | 5706.03 | 0 | 10276.5 | 4.1106 | 25.8968 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_base | 250000 | 100000 | 4 | long_only | taker_entry_taker_exit | macro_or_index_context | 40 | 10 | 40 | 69 | 1 | 15982.5 | 5706.03 | 0 | 10276.5 | 4.1106 | 25.8968 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_base |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_plus_1bp_slippage | 100000 | 100000 | 1 | long_only | taker_entry_taker_exit | all_events | 40 | 6 | 40 | 40 | 1 | 8154.87 | 4109.5 | 0 | 4045.37 | 4.04537 | 25.4858 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_plus_1bp_slippage |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_plus_1bp_slippage | 100000 | 100000 | 2 | long_only | taker_entry_taker_exit | all_events | 40 | 6 | 40 | 40 | 1 | 8154.87 | 4109.5 | 0 | 4045.37 | 4.04537 | 25.4858 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_plus_1bp_slippage |
| P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | zerodha_plus_1bp_slippage | 100000 | 100000 | 4 | long_only | taker_entry_taker_exit | all_events | 40 | 6 | 40 | 40 | 1 | 8154.87 | 4109.5 | 0 | 4045.37 | 4.04537 | 25.4858 | 1 | 1 | 0 | 0 | P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_plus_1bp_slippage |

## Family summary

| family_id | cost_profile | execution_policy | scenario_rows | above12_rows | acceptance_grade_rows | best_annualized_return_pct | best_net_pnl_inr | max_scheduled_event_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P331_DEPTH_ACCEL_REVERSAL | zerodha_base | taker_entry_taker_exit | 8640 | 162 | 0 | 30.5362 | 20266.9 | 50 |
| P331_DEPTH_ACCEL_REVERSAL | zerodha_plus_1bp_slippage | taker_entry_taker_exit | 8640 | 88 | 0 | 25.4858 | 16358 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | zerodha_base | taker_entry_taker_exit | 8640 | 156 | 0 | 21.9053 | 12236.2 | 50 |
| P331_DEPTH_ACCEL_REVERSAL | zerodha_plus_2bp_slippage | taker_entry_taker_exit | 8640 | 48 | 0 | 20.4355 | 12449.1 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | zerodha_plus_1bp_slippage | taker_entry_taker_exit | 8640 | 64 | 0 | 18.0256 | 8941.25 | 50 |
| P331_DEPTH_SHARE_COMPRESSION_REVERSAL | zerodha_base | taker_entry_taker_exit | 8640 | 14 | 0 | 14.4411 | 12986.4 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | zerodha_plus_2bp_slippage | taker_entry_taker_exit | 8640 | 32 | 0 | 14.1458 | 7016.76 | 50 |
| P331_DEPTH_SHARE_EXPANSION_CONTINUATION | zerodha_base | taker_entry_taker_exit | 8640 | 0 | 0 | 11.9548 | 8830.54 | 50 |
| P331_DEPTH_ACCEL_REVERSAL | zerodha_2x_all_in_cost_proxy | taker_entry_taker_exit | 8640 | 0 | 0 | 11.5176 | 5144.04 | 50 |
| P331_PRE900_TO_EVENT_PRESSURE_SHIFT | zerodha_base | taker_entry_taker_exit | 8640 | 0 | 0 | 10.8788 | 1726.79 | 50 |
| P331_DEPTH_SHARE_COMPRESSION_REVERSAL | zerodha_plus_1bp_slippage | taker_entry_taker_exit | 8640 | 0 | 0 | 10.4206 | 9799.66 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | zerodha_base | taker_entry_taker_exit | 8640 | 0 | 0 | 9.75228 | 1470.58 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | zerodha_base | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 7.22096 | 3581.82 | 50 |
| P331_DEPTH_SHARE_EXPANSION_CONTINUATION | zerodha_plus_1bp_slippage | taker_entry_taker_exit | 8640 | 0 | 0 | 6.90818 | 4862.74 | 50 |
| P331_DEPTH_SHARE_COMPRESSION_REVERSAL | zerodha_plus_2bp_slippage | taker_entry_taker_exit | 8640 | 0 | 0 | 6.80181 | 6612.87 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | zerodha_2x_all_in_cost_proxy | taker_entry_taker_exit | 8640 | 0 | 0 | 5.90016 | 2926.67 | 50 |
| P331_PRE900_TO_EVENT_PRESSURE_SHIFT | zerodha_plus_1bp_slippage | taker_entry_taker_exit | 8640 | 0 | 0 | 5.82754 | 925.006 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | zerodha_plus_1bp_slippage | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 4.8443 | 2402.92 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | zerodha_plus_1bp_slippage | taker_entry_taker_exit | 8640 | 0 | 0 | 4.70079 | 708.849 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | zerodha_plus_2bp_slippage | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 2.46764 | 1224.03 | 50 |
| P331_DEPTH_SHARE_EXPANSION_CONTINUATION | zerodha_plus_2bp_slippage | taker_entry_taker_exit | 8640 | 0 | 0 | 1.86153 | 894.95 | 50 |
| P331_DEPTH_ACCEL_REVERSAL | zerodha_base | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 1.11836 | 1109.49 | 50 |
| P331_DEPTH_PRESSURE_CONTINUATION | zerodha_base | taker_entry_taker_exit | 8640 | 0 | 0 | 1.05606 | 523.839 | 50 |
| P331_DEPTH_PRESSURE_TARGET_SHIFT | zerodha_base | taker_entry_taker_exit | 8640 | 0 | 0 | 1.05606 | 523.839 | 50 |
| P331_SPREAD_ADJUSTED_PRESSURE_CONTINUATION | zerodha_base | taker_entry_taker_exit | 8640 | 0 | 0 | 1.05606 | 523.839 | 50 |
| P331_DEPTH_SHARE_COMPRESSION_REVERSAL | zerodha_base | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 1.05471 | 1025.41 | 50 |
| P331_PRE900_TO_EVENT_PRESSURE_SHIFT | zerodha_plus_2bp_slippage | taker_entry_taker_exit | 8640 | 0 | 0 | 0.776291 | 123.221 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | zerodha_2x_all_in_cost_proxy | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | zerodha_2x_all_in_cost_proxy | taker_entry_taker_exit | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | zerodha_base | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | zerodha_plus_1bp_slippage | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | zerodha_plus_2bp_slippage | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | zerodha_plus_2bp_slippage | taker_entry_taker_exit | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_ACCEL_REVERSAL | zerodha_2x_all_in_cost_proxy | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_ACCEL_REVERSAL | zerodha_plus_1bp_slippage | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_ACCEL_REVERSAL | zerodha_plus_2bp_slippage | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_CONTINUATION | zerodha_2x_all_in_cost_proxy | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_CONTINUATION | zerodha_2x_all_in_cost_proxy | taker_entry_taker_exit | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_CONTINUATION | zerodha_base | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_CONTINUATION | zerodha_plus_1bp_slippage | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_CONTINUATION | zerodha_plus_1bp_slippage | taker_entry_taker_exit | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_CONTINUATION | zerodha_plus_2bp_slippage | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_CONTINUATION | zerodha_plus_2bp_slippage | taker_entry_taker_exit | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_REVERSAL | zerodha_2x_all_in_cost_proxy | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_REVERSAL | zerodha_2x_all_in_cost_proxy | taker_entry_taker_exit | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_REVERSAL | zerodha_base | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_REVERSAL | zerodha_base | taker_entry_taker_exit | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_REVERSAL | zerodha_plus_1bp_slippage | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_REVERSAL | zerodha_plus_1bp_slippage | taker_entry_taker_exit | 8640 | 0 | 0 | 0 | 0 | 50 |
| P331_DEPTH_PRESSURE_REVERSAL | zerodha_plus_2bp_slippage | passive_aware_directional_with_penalties | 8640 | 0 | 0 | 0 | 0 | 50 |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P332_PHASE331_COMPLETE | True | 1 | 1 | hard |
| P332_PHASE331_EXECUTION_ALLOWED | True | 1 | 1 | hard |
| P332_SCENARIOS_PRODUCED | True | 1036800 | >0 | hard |
| P332_VARIANT_COVERAGE_COMPLETE | True | 1036800/1036800 | equal | hard |
| P332_COST200_SCENARIOS_PRESENT | True | 259200 | >0 | hard |
| P332_PASSIVE_AWARE_SCENARIOS_PRESENT | True | 518400 | >0 | hard |
| P332_EVENT_BUCKET_SCENARIOS_PRESENT | True | 5 | >=5 | hard |
| P332_FIXED_CAPITAL_DENOMINATOR | True | all_positive | all_positive | hard |
| P332_NO_PROFITABILITY_CLAIM | True | profitability_claim_allowed=0 | 0 | hard |
| P332_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

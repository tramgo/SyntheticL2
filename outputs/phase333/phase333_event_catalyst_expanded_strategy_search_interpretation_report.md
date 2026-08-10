# Phase333 Event-Catalyst Expanded Strategy Search Interpretation

Phase333 interprets the Phase332 full expanded strategy surface. It does not run replay, promote a strategy, open paper/live acceptance, or claim deployable profitability.
The central verdict is crisp: the expanded full-depth search found real base-cost research pockets, but no 2x Zerodha cost-stress scenario exceeded the user's >12% annualized threshold.
Because the best 2x-cost result reached 11.517554062957867% over 40 scheduled events, the clue is preserved for a focused cost-stress-margin redesign rather than discarded.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase333_event_catalyst_expanded_strategy_search_interpretation_complete | 1 | Phase333 interpretation completed |
| phase333_base_or_slippage_profitable_research_pockets_exist | 1 | Base/slippage research pockets above 12 exist |
| phase333_cost200_profitability_bar_passed | 0 | 2x-cost >12% bar passed |
| phase333_cost200_acceptance_grade_candidates_exist | 0 | 2x-cost acceptance-grade candidates exist |
| phase333_best_cost200_near_miss_preserved | 1 | Near-miss preserved as redesign clue |
| phase333_preserved_family_for_redesign | P331_DEPTH_ACCEL_REVERSAL | Family preserved for redesign |
| phase333_passive_aware_rescue_status | falsified_as_primary_rescue | Passive-aware rescue status |
| phase333_next_design_focus | cost_stress_margin_and_turnover_reduction | Next design focus |
| phase333_replay_allowed | 0 | No replay |
| phase333_strategy_promotion_allowed | 0 | No promotion |
| phase333_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase333_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase333_selected_next_route | P334_COST_STRESS_MARGIN_REDESIGN_PRECOMMIT | Selected next route |
| phase333_hard_gate_pass_rows | 8 | Passed hard gates |
| phase333_hard_gate_rows | 8 | Hard gates |
| phase333_next_best_action | run_phase334_cost_stress_margin_redesign_precommit_no_replay | Recommended next action |

## Decision ledger

| decision_id | decision_value | evidence | interpretation |
| --- | --- | --- | --- |
| phase332_search_complete | 1 | scenario_rows=1036800 | The expanded training-only search ran to completion. |
| base_or_slippage_profitable_research_pockets_exist | 1 | above12_scenario_rows=564 | Profitable-looking pockets exist before the strict 2x cost-stress bar. |
| cost200_profitability_bar_passed | 0 | cost200_above12_scenario_rows=0; threshold>12.0 | The user threshold is not met under the 2x Zerodha all-in cost proxy. |
| cost200_acceptance_grade_candidates_exist | 0 | cost200_acceptance_grade_candidate_rows=0 | No acceptance-grade candidate exists without passing both cost and breadth gates. |
| best_cost200_near_miss_preserved | 1 | best_cost200=11.517554062957867; gap_to_12=0.482445937042133; events=40 | The near-miss is broad enough to redesign around, but it is not accepted as profitable. |
| preserved_family_for_redesign | P331_DEPTH_ACCEL_REVERSAL | Phase332 best family | Depth-acceleration reversal remains the strongest actionable clue. |
| passive_aware_rescue_status | falsified_as_primary_rescue | best_passive=7.220955903503546; best_taker=30.5361528844332 | Passive-aware execution realism stays required, but it did not rescue the branch. |
| next_design_focus | cost_stress_margin_and_turnover_reduction | 2x cost miss is 0.482445937 pct points below 12 | The next test should reduce cost drag without lowering the annualized or cost-stress bar. |
| forbidden_next_actions | no_replay_no_promotion_no_paper_live_no_profit_claim | all acceptance gates closed | Do not jump to replay or declare profitability from Phase332. |
| selected_next_route | P334_COST_STRESS_MARGIN_REDESIGN_PRECOMMIT | run_phase334_cost_stress_margin_redesign_precommit_no_replay | Precommit a narrow redesign around the preserved cost-stress near miss, then execute it. |

## 2x-cost near-miss scenarios

| scenario_id | family_id | horizon_seconds | threshold_policy | side_policy | execution_policy | event_bucket_policy | initial_capital_inr | fixed_notional_inr | max_concurrent_positions | scheduled_event_rows | symbol_rows | observed_trade_dates | trade_rows | gross_pnl_inr | cost_inr | passive_penalty_inr | net_pnl_inr | annualized_return_pct | annualized_gap_to_12pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 40 | 10 | 40 | 69 | 15982.5 | 11412.1 | 0 | 4570.46 | 11.5176 | 0.482446 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 40 | 10 | 40 | 69 | 15982.5 | 11412.1 | 0 | 4570.46 | 11.5176 | 0.482446 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 2 | 40 | 10 | 40 | 69 | 15982.5 | 11412.1 | 0 | 4570.46 | 11.5176 | 0.482446 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 40 | 10 | 40 | 69 | 15982.5 | 11412.1 | 0 | 4570.46 | 11.5176 | 0.482446 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_25pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_25pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 48 | 13 | 48 | 90 | 20029.3 | 14885.2 | 0 | 5144.04 | 10.8025 | 1.19751 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_25pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_25pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 48 | 13 | 48 | 90 | 20029.3 | 14885.2 | 0 | 5144.04 | 10.8025 | 1.19751 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_25pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_25pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 2 | 48 | 13 | 48 | 90 | 20029.3 | 14885.2 | 0 | 5144.04 | 10.8025 | 1.19751 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_25pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_25pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 48 | 13 | 48 | 90 | 20029.3 | 14885.2 | 0 | 5144.04 | 10.8025 | 1.19751 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 100000 | 100000 | 2 | 40 | 6 | 40 | 40 | 8154.87 | 6615.72 | 0 | 1539.15 | 9.69662 | 2.30338 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 100000 | 100000 | 2 | 40 | 6 | 40 | 40 | 8154.87 | 6615.72 | 0 | 1539.15 | 9.69662 | 2.30338 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 100000 | 100000 | 4 | 40 | 6 | 40 | 40 | 8154.87 | 6615.72 | 0 | 1539.15 | 9.69662 | 2.30338 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 100000 | 100000 | 1 | 40 | 6 | 40 | 40 | 8154.87 | 6615.72 | 0 | 1539.15 | 9.69662 | 2.30338 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 100000 | 100000 | 1 | 40 | 6 | 40 | 40 | 8154.87 | 6615.72 | 0 | 1539.15 | 9.69662 | 2.30338 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_10pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 100000 | 100000 | 4 | 40 | 6 | 40 | 40 | 8154.87 | 6615.72 | 0 | 1539.15 | 9.69662 | 2.30338 |
| P331_DEPTH_ACCEL_REVERSAL_H900_all_nonzero_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | all_nonzero_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 50 | 17 | 50 | 100 | 20093.4 | 16539 | 0 | 3554.46 | 7.16579 | 4.83421 |
| P331_DEPTH_ACCEL_REVERSAL_H900_all_nonzero_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | all_nonzero_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 50 | 17 | 50 | 100 | 20093.4 | 16539 | 0 | 3554.46 | 7.16579 | 4.83421 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_50pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_50pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 50 | 17 | 50 | 100 | 20093.4 | 16539 | 0 | 3554.46 | 7.16579 | 4.83421 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_50pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_50pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 50 | 17 | 50 | 100 | 20093.4 | 16539 | 0 | 3554.46 | 7.16579 | 4.83421 |
| P331_DEPTH_ACCEL_REVERSAL_H900_all_nonzero_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | all_nonzero_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 2 | 50 | 17 | 50 | 100 | 20093.4 | 16539 | 0 | 3554.46 | 7.16579 | 4.83421 |
| P331_DEPTH_ACCEL_REVERSAL_H900_all_nonzero_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | all_nonzero_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 50 | 17 | 50 | 100 | 20093.4 | 16539 | 0 | 3554.46 | 7.16579 | 4.83421 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_50pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_50pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 2 | 50 | 17 | 50 | 100 | 20093.4 | 16539 | 0 | 3554.46 | 7.16579 | 4.83421 |
| P331_DEPTH_ACCEL_REVERSAL_H900_top_50pct_abs_signal_macro_or_index_context_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P331_DEPTH_ACCEL_REVERSAL | 900 | top_50pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 50 | 17 | 50 | 100 | 20093.4 | 16539 | 0 | 3554.46 | 7.16579 | 4.83421 |
| P331_MICROPRICE_DEPTH_CONFIRM_H1800_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P331_MICROPRICE_DEPTH_CONFIRM | 1800 | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 50 | 4 | 50 | 96 | 18804.8 | 15878.1 | 0 | 2926.67 | 5.90016 | 6.09984 |
| P331_MICROPRICE_DEPTH_CONFIRM_H1800_top_10pct_abs_signal_all_events_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P331_MICROPRICE_DEPTH_CONFIRM | 1800 | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 50 | 4 | 50 | 96 | 18804.8 | 15878.1 | 0 | 2926.67 | 5.90016 | 6.09984 |
| P331_MICROPRICE_DEPTH_CONFIRM_H1800_top_10pct_abs_signal_all_events_long_short_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P331_MICROPRICE_DEPTH_CONFIRM | 1800 | top_10pct_abs_signal | long_short | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 50 | 4 | 50 | 96 | 18804.8 | 15878.1 | 0 | 2926.67 | 5.90016 | 6.09984 |

## Cost profile gap

| family_id | threshold_policy | side_policy | execution_policy | event_bucket_policy | initial_capital_inr | fixed_notional_inr | max_concurrent_positions | base_best_annualized_return_pct | cost200_best_annualized_return_pct | base_max_scheduled_events | cost200_max_scheduled_events | cost_stress_drag_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 2 | 25.8968 | 11.5176 | 40 | 40 | 14.3792 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 25.8968 | 11.5176 | 40 | 40 | 14.3792 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 25.8968 | 11.5176 | 40 | 40 | 14.3792 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 25.8968 | 11.5176 | 40 | 40 | 14.3792 |
| P331_DEPTH_ACCEL_REVERSAL | top_25pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 2 | 26.432 | 10.8025 | 48 | 48 | 15.6295 |
| P331_DEPTH_ACCEL_REVERSAL | top_25pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 26.432 | 10.8025 | 48 | 48 | 15.6295 |
| P331_DEPTH_ACCEL_REVERSAL | top_25pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 26.432 | 10.8025 | 48 | 48 | 15.6295 |
| P331_DEPTH_ACCEL_REVERSAL | top_25pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 26.432 | 10.8025 | 48 | 48 | 15.6295 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 100000 | 100000 | 2 | 30.5362 | 9.69662 | 40 | 40 | 20.8395 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 100000 | 100000 | 1 | 30.5362 | 9.69662 | 40 | 40 | 20.8395 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 100000 | 100000 | 4 | 30.5362 | 9.69662 | 40 | 40 | 20.8395 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 100000 | 100000 | 1 | 30.5362 | 9.69662 | 40 | 40 | 20.8395 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 100000 | 100000 | 4 | 30.5362 | 9.69662 | 40 | 40 | 20.8395 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 100000 | 100000 | 2 | 30.5362 | 9.69662 | 40 | 40 | 20.8395 |
| P331_DEPTH_ACCEL_REVERSAL | all_nonzero_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 2 | 23.8371 | 7.16579 | 50 | 50 | 16.6713 |
| P331_DEPTH_ACCEL_REVERSAL | top_50pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 2 | 23.8371 | 7.16579 | 50 | 50 | 16.6713 |
| P331_DEPTH_ACCEL_REVERSAL | all_nonzero_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 23.8371 | 7.16579 | 50 | 50 | 16.6713 |
| P331_DEPTH_ACCEL_REVERSAL | top_50pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 23.8371 | 7.16579 | 50 | 50 | 16.6713 |
| P331_DEPTH_ACCEL_REVERSAL | all_nonzero_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 23.8371 | 7.16579 | 50 | 50 | 16.6713 |
| P331_DEPTH_ACCEL_REVERSAL | top_50pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 23.8371 | 7.16579 | 50 | 50 | 16.6713 |
| P331_DEPTH_ACCEL_REVERSAL | top_50pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 23.8371 | 7.16579 | 50 | 50 | 16.6713 |
| P331_DEPTH_ACCEL_REVERSAL | all_nonzero_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 23.8371 | 7.16579 | 50 | 50 | 16.6713 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 21.9053 | 5.90016 | 50 | 50 | 16.0052 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 21.9053 | 5.90016 | 50 | 50 | 16.0052 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_10pct_abs_signal | long_short | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 21.9053 | 5.90016 | 50 | 50 | 16.0052 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_10pct_abs_signal | long_short | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 21.9053 | 5.90016 | 50 | 50 | 16.0052 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 21.9053 | 5.90016 | 50 | 50 | 16.0052 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_10pct_abs_signal | long_short | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 21.9053 | 5.90016 | 50 | 50 | 16.0052 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_10pct_abs_signal | long_short | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 2 | 21.9053 | 5.90016 | 50 | 50 | 16.0052 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 2 | 21.9053 | 5.90016 | 50 | 50 | 16.0052 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 500000 | 100000 | 2 | 12.9484 | 5.75878 | 40 | 40 | 7.1896 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 500000 | 100000 | 2 | 12.9484 | 5.75878 | 40 | 40 | 7.1896 |
| P331_DEPTH_ACCEL_REVERSAL | top_25pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 500000 | 100000 | 2 | 13.216 | 5.40124 | 48 | 48 | 7.81474 |
| P331_DEPTH_ACCEL_REVERSAL | top_25pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 500000 | 100000 | 2 | 13.216 | 5.40124 | 48 | 48 | 7.81474 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 75000 | 2 | 17.3273 | 4.44766 | 40 | 40 | 12.8797 |
| P331_DEPTH_ACCEL_REVERSAL | top_10pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 75000 | 2 | 17.3273 | 4.44766 | 40 | 40 | 12.8797 |
| P331_DEPTH_ACCEL_REVERSAL | top_50pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 500000 | 100000 | 4 | 20.4291 | 4.17388 | 50 | 50 | 16.2552 |
| P331_DEPTH_ACCEL_REVERSAL | top_50pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 500000 | 100000 | 4 | 20.4291 | 4.17388 | 50 | 50 | 16.2552 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_50pct_abs_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 20.6362 | 3.96428 | 50 | 50 | 16.672 |
| P331_MICROPRICE_DEPTH_CONFIRM | all_nonzero_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 20.6362 | 3.96428 | 50 | 50 | 16.672 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_50pct_abs_signal | long_short | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 2 | 20.6362 | 3.96428 | 50 | 50 | 16.672 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_25pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 2 | 20.6362 | 3.96428 | 50 | 50 | 16.672 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_25pct_abs_signal | long_short | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 20.6362 | 3.96428 | 50 | 50 | 16.672 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_50pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 20.6362 | 3.96428 | 50 | 50 | 16.672 |
| P331_MICROPRICE_DEPTH_CONFIRM | all_nonzero_signal | long_short | taker_entry_taker_exit | all_events | 250000 | 100000 | 2 | 20.6362 | 3.96428 | 50 | 50 | 16.672 |
| P331_MICROPRICE_DEPTH_CONFIRM | all_nonzero_signal | long_only | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 20.6362 | 3.96428 | 50 | 50 | 16.672 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_25pct_abs_signal | long_only | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 20.6362 | 3.96428 | 50 | 50 | 16.672 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_50pct_abs_signal | long_short | taker_entry_taker_exit | all_events | 250000 | 100000 | 4 | 20.6362 | 3.96428 | 50 | 50 | 16.672 |
| P331_MICROPRICE_DEPTH_CONFIRM | all_nonzero_signal | long_short | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 20.6362 | 3.96428 | 50 | 50 | 16.672 |
| P331_MICROPRICE_DEPTH_CONFIRM | top_50pct_abs_signal | long_short | taker_entry_taker_exit | macro_or_index_context | 250000 | 100000 | 4 | 20.6362 | 3.96428 | 50 | 50 | 16.672 |

## Family cost-stress interpretation

| family_id | execution_policy | cost_profile | scenario_rows | above12_rows | acceptance_grade_rows | best_annualized_return_pct | median_annualized_return_pct | best_net_pnl_inr | max_scheduled_event_rows | max_symbol_rows | max_observed_trade_dates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P331_DEPTH_ACCEL_REVERSAL | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 11.5176 | 0 | 5144.04 | 50 | 28 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 5.90016 | 0 | 2926.67 | 50 | 6 | 50 |
| P331_QTY_IMBALANCE_REVERSAL | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 5 | 50 |
| P331_ORDER_IMBALANCE_CONTINUATION | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 10 | 50 |
| P331_QTY_IMBALANCE_CONTINUATION | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 5 | 50 |
| P331_DEPTH_PRESSURE_TARGET_SHIFT | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_QTY_IMBALANCE_REVERSAL | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 5 | 50 |
| P331_PRE900_TO_EVENT_PRESSURE_SHIFT | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 27 | 50 |
| P331_DEPTH_SHARE_COMPRESSION_REVERSAL | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 32 | 50 |
| P331_DEPTH_PRESSURE_REVERSAL | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_DEPTH_PRESSURE_REVERSAL | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_ORDER_IMBALANCE_REVERSAL | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 10 | 50 |
| P331_DEPTH_PRESSURE_CONTINUATION | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_DEPTH_SHARE_EXPANSION_CONTINUATION | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 32 | 50 |
| P331_DEPTH_SHARE_COMPRESSION_REVERSAL | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 32 | 50 |
| P331_SPREAD_ADJUSTED_PRESSURE_REVERSAL | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_SPREAD_ADJUSTED_PRESSURE_CONTINUATION | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_DEPTH_PRESSURE_TARGET_SHIFT | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_DEPTH_SHARE_EXPANSION_CONTINUATION | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 32 | 50 |
| P331_PRE900_TO_EVENT_PRESSURE_SHIFT | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 27 | 50 |
| P331_ORDER_IMBALANCE_CONTINUATION | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 10 | 50 |
| P331_ORDER_IMBALANCE_REVERSAL | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 10 | 50 |
| P331_DEPTH_ACCEL_REVERSAL | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 28 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 6 | 50 |
| P331_SPREAD_ADJUSTED_PRESSURE_CONTINUATION | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 28 | 50 |
| P331_DEPTH_PRESSURE_CONTINUATION | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_QTY_IMBALANCE_CONTINUATION | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 5 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | passive_aware_directional_with_penalties | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 28 | 50 |
| P331_SPREAD_ADJUSTED_PRESSURE_REVERSAL | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_DEPTH_ACCEL_REVERSAL | taker_entry_taker_exit | zerodha_base | 8640 | 162 | 0 | 30.5362 | 0 | 20266.9 | 50 | 28 | 50 |
| P331_DEPTH_ACCEL_REVERSAL | taker_entry_taker_exit | zerodha_plus_1bp_slippage | 8640 | 88 | 0 | 25.4858 | 0 | 16358 | 50 | 28 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | taker_entry_taker_exit | zerodha_base | 8640 | 156 | 0 | 21.9053 | 0 | 12236.2 | 50 | 6 | 50 |
| P331_DEPTH_ACCEL_REVERSAL | taker_entry_taker_exit | zerodha_plus_2bp_slippage | 8640 | 48 | 0 | 20.4355 | 0 | 12449.1 | 50 | 28 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | taker_entry_taker_exit | zerodha_plus_1bp_slippage | 8640 | 64 | 0 | 18.0256 | 0 | 8941.25 | 50 | 6 | 50 |
| P331_DEPTH_SHARE_COMPRESSION_REVERSAL | taker_entry_taker_exit | zerodha_base | 8640 | 14 | 0 | 14.4411 | 0 | 12986.4 | 50 | 32 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | taker_entry_taker_exit | zerodha_plus_2bp_slippage | 8640 | 32 | 0 | 14.1458 | 0 | 7016.76 | 50 | 6 | 50 |
| P331_DEPTH_SHARE_EXPANSION_CONTINUATION | taker_entry_taker_exit | zerodha_base | 8640 | 0 | 0 | 11.9548 | 0 | 8830.54 | 50 | 32 | 50 |
| P331_PRE900_TO_EVENT_PRESSURE_SHIFT | taker_entry_taker_exit | zerodha_base | 8640 | 0 | 0 | 10.8788 | 0 | 1726.79 | 50 | 27 | 50 |
| P331_DEPTH_SHARE_COMPRESSION_REVERSAL | taker_entry_taker_exit | zerodha_plus_1bp_slippage | 8640 | 0 | 0 | 10.4206 | 0 | 9799.66 | 50 | 32 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | taker_entry_taker_exit | zerodha_base | 8640 | 0 | 0 | 9.75228 | 0 | 1470.58 | 50 | 28 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | passive_aware_directional_with_penalties | zerodha_base | 8640 | 0 | 0 | 7.22096 | 0 | 3581.82 | 50 | 6 | 50 |
| P331_DEPTH_SHARE_EXPANSION_CONTINUATION | taker_entry_taker_exit | zerodha_plus_1bp_slippage | 8640 | 0 | 0 | 6.90818 | 0 | 4862.74 | 50 | 32 | 50 |
| P331_DEPTH_SHARE_COMPRESSION_REVERSAL | taker_entry_taker_exit | zerodha_plus_2bp_slippage | 8640 | 0 | 0 | 6.80181 | 0 | 6612.87 | 50 | 32 | 50 |
| P331_PRE900_TO_EVENT_PRESSURE_SHIFT | taker_entry_taker_exit | zerodha_plus_1bp_slippage | 8640 | 0 | 0 | 5.82754 | 0 | 925.006 | 50 | 27 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | passive_aware_directional_with_penalties | zerodha_plus_1bp_slippage | 8640 | 0 | 0 | 4.8443 | 0 | 2402.92 | 50 | 6 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | taker_entry_taker_exit | zerodha_plus_1bp_slippage | 8640 | 0 | 0 | 4.70079 | 0 | 708.849 | 50 | 28 | 50 |
| P331_MICROPRICE_DEPTH_CONFIRM | passive_aware_directional_with_penalties | zerodha_plus_2bp_slippage | 8640 | 0 | 0 | 2.46764 | 0 | 1224.03 | 50 | 6 | 50 |
| P331_DEPTH_SHARE_EXPANSION_CONTINUATION | taker_entry_taker_exit | zerodha_plus_2bp_slippage | 8640 | 0 | 0 | 1.86153 | 0 | 894.95 | 50 | 32 | 50 |
| P331_DEPTH_ACCEL_REVERSAL | passive_aware_directional_with_penalties | zerodha_base | 8640 | 0 | 0 | 1.11836 | 0 | 1109.49 | 50 | 28 | 50 |
| P331_DEPTH_PRESSURE_TARGET_SHIFT | taker_entry_taker_exit | zerodha_base | 8640 | 0 | 0 | 1.05606 | 0 | 523.839 | 50 | 7 | 50 |
| P331_SPREAD_ADJUSTED_PRESSURE_CONTINUATION | taker_entry_taker_exit | zerodha_base | 8640 | 0 | 0 | 1.05606 | 0 | 523.839 | 50 | 7 | 50 |
| P331_DEPTH_PRESSURE_CONTINUATION | taker_entry_taker_exit | zerodha_base | 8640 | 0 | 0 | 1.05606 | 0 | 523.839 | 50 | 7 | 50 |
| P331_DEPTH_SHARE_COMPRESSION_REVERSAL | passive_aware_directional_with_penalties | zerodha_base | 8640 | 0 | 0 | 1.05471 | 0 | 1025.41 | 50 | 32 | 50 |
| P331_PRE900_TO_EVENT_PRESSURE_SHIFT | taker_entry_taker_exit | zerodha_plus_2bp_slippage | 8640 | 0 | 0 | 0.776291 | 0 | 123.221 | 50 | 27 | 50 |
| P331_SPREAD_ADJUSTED_PRESSURE_CONTINUATION | passive_aware_directional_with_penalties | zerodha_plus_2bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_QTY_IMBALANCE_CONTINUATION | passive_aware_directional_with_penalties | zerodha_base | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 5 | 50 |
| P331_SPREAD_ADJUSTED_PRESSURE_REVERSAL | taker_entry_taker_exit | zerodha_plus_2bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_DEPTH_PRESSURE_TARGET_SHIFT | taker_entry_taker_exit | zerodha_plus_1bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_QTY_IMBALANCE_CONTINUATION | passive_aware_directional_with_penalties | zerodha_plus_2bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 5 | 50 |
| P331_PRE900_TO_EVENT_PRESSURE_SHIFT | passive_aware_directional_with_penalties | zerodha_plus_1bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 27 | 50 |
| P331_QTY_IMBALANCE_CONTINUATION | taker_entry_taker_exit | zerodha_base | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 5 | 50 |
| P331_DEPTH_SHARE_COMPRESSION_REVERSAL | passive_aware_directional_with_penalties | zerodha_plus_1bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 32 | 50 |
| P331_DEPTH_SHARE_EXPANSION_CONTINUATION | passive_aware_directional_with_penalties | zerodha_plus_2bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 32 | 50 |
| P331_QTY_IMBALANCE_REVERSAL | taker_entry_taker_exit | zerodha_plus_1bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 5 | 50 |
| P331_QTY_IMBALANCE_REVERSAL | passive_aware_directional_with_penalties | zerodha_plus_2bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 5 | 50 |
| P331_ORDER_IMBALANCE_REVERSAL | taker_entry_taker_exit | zerodha_base | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 10 | 50 |
| P331_ORDER_IMBALANCE_REVERSAL | passive_aware_directional_with_penalties | zerodha_plus_2bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 10 | 50 |
| P331_DEPTH_PRESSURE_REVERSAL | passive_aware_directional_with_penalties | zerodha_base | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_DEPTH_PRESSURE_REVERSAL | taker_entry_taker_exit | zerodha_base | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_DEPTH_PRESSURE_TARGET_SHIFT | passive_aware_directional_with_penalties | zerodha_plus_1bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_PRE900_TO_EVENT_PRESSURE_SHIFT | passive_aware_directional_with_penalties | zerodha_base | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 27 | 50 |
| P331_QTY_IMBALANCE_CONTINUATION | taker_entry_taker_exit | zerodha_plus_1bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 5 | 50 |
| P331_DEPTH_PRESSURE_TARGET_SHIFT | passive_aware_directional_with_penalties | zerodha_base | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_SPREAD_ADJUSTED_PRESSURE_REVERSAL | taker_entry_taker_exit | zerodha_base | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_DEPTH_ACCEL_CONTINUATION | taker_entry_taker_exit | zerodha_plus_2bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 28 | 50 |
| P331_SPREAD_ADJUSTED_PRESSURE_CONTINUATION | passive_aware_directional_with_penalties | zerodha_plus_1bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_DEPTH_PRESSURE_CONTINUATION | passive_aware_directional_with_penalties | zerodha_base | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 7 | 50 |
| P331_ORDER_IMBALANCE_CONTINUATION | taker_entry_taker_exit | zerodha_plus_2bp_slippage | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 10 | 50 |
| P331_ORDER_IMBALANCE_CONTINUATION | taker_entry_taker_exit | zerodha_base | 8640 | 0 | 0 | 0 | 0 | 0 | 50 | 10 | 50 |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P333_PHASE332_COMPLETE | True | 1 | 1 | hard |
| P333_DECISION_ROWS_PRESENT | True | 10 | >=10 | hard |
| P333_COST200_FAILURE_INTERPRETED | True | present | present | hard |
| P333_NEAR_MISS_DECISION_PRESENT | True | present | present | hard |
| P333_PASSIVE_AWARE_STATUS_PRESENT | True | present | present | hard |
| P333_PROFITABILITY_CLAIM_CLOSED | True | 0 | 0 | hard |
| P333_REPLAY_CLOSED | True | 0 | 0 | hard |
| P333_NEXT_ROUTE_SELECTED | True | P334_COST_STRESS_MARGIN_REDESIGN_PRECOMMIT | selected | hard |


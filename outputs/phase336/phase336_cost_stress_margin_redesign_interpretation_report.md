# Phase336 Cost-Stress Margin Redesign Interpretation

Phase336 interprets Phase335 positive training-only cost-stress results.
It preserves candidates for holdout precommit, but does not replay, promote, open paper/live acceptance, or claim deployable profitability.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase336_cost_stress_margin_redesign_interpretation_complete | 1 | Phase336 interpretation completed |
| phase336_cost200_profitable_training_pockets_exist | 1 | 2x-cost profitable training pockets exist |
| phase336_cost200_acceptance_grade_training_candidates_exist | 1 | 2x-cost acceptance-grade training candidates exist |
| phase336_candidate_rows_preserved | 32 | Acceptance-grade candidates preserved |
| phase336_best_acceptance_grade_candidate | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | Best candidate preserved |
| phase336_best_acceptance_grade_annualized_return_pct | 19.32314001122077 | Best acceptance-grade annualized return |
| phase336_best_acceptance_grade_scheduled_events | 47 | Best acceptance-grade scheduled events |
| phase336_candidate_lanes_preserved | P334_LANE_B_TURNOVER_COMPRESSION;P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN;P334_LANE_D_HORIZON_AND_EXIT_MARGIN | Candidate lanes preserved |
| phase336_passive_aware_status | diagnostic_only_no_acceptance_grade_rows | Passive-aware status |
| phase336_replay_allowed | 0 | No replay |
| phase336_strategy_promotion_allowed | 0 | No promotion |
| phase336_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase336_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase336_selected_next_route | P337_COST_STRESS_HOLDOUT_VALIDATION_PRECOMMIT | Selected next route |
| phase336_hard_gate_pass_rows | 8 | Passed hard gates |
| phase336_hard_gate_rows | 8 | Hard gates |
| phase336_next_best_action | run_phase337_cost_stress_holdout_validation_precommit_no_replay | Recommended next action |

## Decision ledger

| decision_id | decision_value | evidence | interpretation |
| --- | --- | --- | --- |
| phase335_training_complete | 1 | scenario_rows=6720 | Phase335 completed the training-only redesign search. |
| cost200_profitable_training_pockets_exist | 1 | cost200_above12=138 | The redesigned training surface crossed the user >12% threshold under 2x costs. |
| cost200_acceptance_grade_training_candidates_exist | 1 | acceptance_rows=32 | Training-only candidates pass cost, breadth, and control diagnostics. |
| best_acceptance_grade_candidate_preserved | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | annualized=19.32314001122077; events=47 | Preserve the best candidate for holdout precommit. |
| candidate_lanes_preserved | P334_LANE_B_TURNOVER_COMPRESSION;P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN;P334_LANE_D_HORIZON_AND_EXIT_MARGIN | candidate_rows=32 | Preserve all lanes that generated acceptance-grade rows. |
| passive_aware_status | diagnostic_only_no_acceptance_grade_rows | passive acceptance-grade rows=0 | Passive-aware realism remains diagnostic and should not be used to claim acceptance. |
| failure_modes_recorded | 3 | sparse; passive; holdout_required | Record reasons this is not yet final profitability. |
| replay_allowed_now | 0 | training-only evidence | No replay opens directly from Phase336. |
| paper_live_or_profitability_claim_allowed | 0 | closed | No paper/live or deployable profitability claim opens. |
| selected_next_route | P337_COST_STRESS_HOLDOUT_VALIDATION_PRECOMMIT | run_phase337_cost_stress_holdout_validation_precommit_no_replay | Precommit holdout/falsification for the preserved training candidates. |

## Acceptance-grade candidates

| scenario_id | lane_id | horizon_seconds | signal_quantile | spread_max_quantile | depth_share_min_quantile | top_n_per_event | side_policy | execution_policy | cost_profile | initial_capital_inr | fixed_notional_inr | max_concurrent_positions | scheduled_event_rows | symbol_rows | observed_trade_dates | trade_rows | net_pnl_inr | annualized_return_pct | side_flip_annualized_return_pct | random_side_annualized_return_pct | control_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 47 | 16 | 47 | 86 | 9009.8 | 19.3231 | -80.3328 | -33.1341 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 47 | 16 | 47 | 86 | 9009.8 | 19.3231 | -80.3328 | -33.1341 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP4_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 47 | 16 | 47 | 86 | 9009.8 | 19.3231 | -80.3328 | -33.1341 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP4_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 47 | 16 | 47 | 86 | 9009.8 | 19.3231 | -80.3328 | -33.1341 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p500_TOP3_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.5 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 1 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p500_TOP3_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.5 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 2 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p500_TOP3_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.5 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 4 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p500_TOP4_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 1 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p500_TOP4_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 2 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p500_TOP4_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 4 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p750_TOP3_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.75 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 1 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p750_TOP3_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.75 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 2 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p750_TOP3_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.75 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 4 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p750_TOP4_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.75 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 1 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p750_TOP4_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.75 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 2 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p750_TOP4_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.75 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 4 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 |
| P335_P334_LANE_B_TURNOVER_COMPRESSION_SQ0p500_SPQ0p500_DSQ0p500_TOP2_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_B_TURNOVER_COMPRESSION | 1800 | 0.5 | 0.5 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 |
| P335_P334_LANE_B_TURNOVER_COMPRESSION_SQ0p500_SPQ0p500_DSQ0p500_TOP2_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_B_TURNOVER_COMPRESSION | 1800 | 0.5 | 0.5 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p500_TOP3_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.5 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p500_TOP3_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.5 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p500_TOP4_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p500_TOP4_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p750_TOP3_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.75 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p750_TOP3_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.75 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p750_TOP4_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.75 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p750_TOP4_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.75 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p500_TOP4_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT50000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 50000 | 4 | 46 | 21 | 46 | 153 | 5967.18 | 13.0759 | -85.1209 | -52.3718 | 1 |
| P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p750_TOP4_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT50000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.75 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 50000 | 4 | 46 | 21 | 46 | 153 | 5967.18 | 13.0759 | -85.1209 | -52.3718 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 50000 | 2 | 47 | 16 | 47 | 86 | 2378.36 | 12.752 | -111.818 | -52.8195 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 50000 | 4 | 47 | 16 | 47 | 86 | 2378.36 | 12.752 | -111.818 | -52.8195 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP4_H900_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 50000 | 2 | 47 | 16 | 47 | 86 | 2378.36 | 12.752 | -111.818 | -52.8195 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP4_H900_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 50000 | 4 | 47 | 16 | 47 | 86 | 2378.36 | 12.752 | -111.818 | -52.8195 | 1 |

## Failure modes

| failure_mode | scenario_rows | interpretation |
| --- | --- | --- |
| sparse_high_return_not_acceptance_grade | 106 | Some high-return rows are too sparse and must not drive validation. |
| passive_aware_no_cost200_acceptance | 0 | Passive-aware route did not produce acceptance-grade candidates; keep it diagnostic. |
| candidate_count_requires_holdout | 32 | Positive training candidates exist, so next step must be precommitted holdout/falsification, not a profitability claim. |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P336_PHASE335_COMPLETE | True | 1 | 1 | hard |
| P336_DECISION_ROWS_PRESENT | True | 10 | >=10 | hard |
| P336_ACCEPTANCE_CANDIDATES_INTERPRETED | True | 32 | >0 | hard |
| P336_HOLDOUT_ROUTE_SELECTED | True | P337_COST_STRESS_HOLDOUT_VALIDATION_PRECOMMIT | selected | hard |
| P336_REPLAY_REMAINS_CLOSED | True | 0 | 0 | hard |
| P336_PROFITABILITY_CLAIM_CLOSED | True | 0 | 0 | hard |
| P336_NEXT_IS_PRECOMMIT_NOT_REPLAY | True | P337_COST_STRESS_HOLDOUT_VALIDATION_PRECOMMIT | precommit | hard |
| P336_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |


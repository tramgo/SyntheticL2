# Phase337 Cost-Stress Holdout Validation Precommit

Phase337 freezes Phase336 acceptance-grade training candidates and reconciles the attached passive-aware execution charter into the current holdout contract.
It is precommit-only: no holdout result, replay, promotion, paper/live acceptance, or deployable profitability claim is produced here.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase337_cost_stress_holdout_validation_precommit_complete | 1 | Phase337 precommit completed |
| phase337_candidate_rows_frozen | 32 | Frozen candidate rows |
| phase337_best_frozen_candidate | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | Best frozen candidate |
| phase337_best_frozen_annualized_return_pct | 19.3231 | Best training annualized return carried into holdout precommit |
| phase337_best_frozen_scheduled_events | 47 | Best frozen candidate scheduled events |
| phase337_candidate_lanes_frozen | P334_LANE_B_TURNOVER_COMPRESSION;P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN;P334_LANE_D_HORIZON_AND_EXIT_MARGIN | Frozen candidate lanes |
| phase337_attached_passive_aware_charter_reconciled | 1 | Attached passive-aware charter reconciled |
| phase337_passive_fill_model_required | 1 | Passive fill probability required |
| phase337_adverse_selection_penalty_required | 1 | Passive adverse-selection penalty required |
| phase337_forced_flatten_cost_required | 1 | Forced flatten cost required |
| phase337_maker_rebate_allowed | 0 | No maker rebate |
| phase337_cost_profile_required | zerodha_2x_all_in_cost_proxy | Required cost profile |
| phase337_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned cost model |
| phase337_annualized_threshold_pct | 12 | Required annualized threshold |
| phase337_robust_event_floor | 30 | Required scheduled-event floor |
| phase337_full_depth_required | 1 | Full top-five depth required |
| phase337_levels_2_to_5_required | 1 | Levels 2-5 materiality required |
| phase337_l1_only_allowed | 0 | No L1-only variants |
| phase337_net_edge_live_mask_allowed | 0 | No lookahead masks |
| phase337_strategy_replay_allowed | 0 | No replay |
| phase337_strategy_promotion_allowed | 0 | No promotion |
| phase337_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase337_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase337_phase338_execution_allowed_next | 1 | Phase338 execution allowed next |
| phase337_contract_rows | 30 | Holdout contract rows |
| phase337_phase338_work_order_rows | 8 | Phase338 work-order rows |
| phase337_hard_gate_pass_rows | 12 | Passed hard gates |
| phase337_hard_gate_rows | 12 | Hard gates |
| phase337_next_best_action | run_phase338_cost_stress_holdout_validation_execution_no_replay | Recommended next action |

## Frozen candidate ledger

| freeze_rank | scenario_id | lane_id | horizon_seconds | signal_quantile | spread_max_quantile | depth_share_min_quantile | top_n_per_event | side_policy | execution_policy | cost_profile | initial_capital_inr | fixed_notional_inr | max_concurrent_positions | scheduled_event_rows | symbol_rows | observed_trade_dates | trade_rows | net_pnl_inr | annualized_return_pct | side_flip_annualized_return_pct | random_side_annualized_return_pct | control_pass | frozen_for_holdout | candidate_selection_source | holdout_tuning_allowed | posthoc_filter_addition_allowed | primary_holdout_execution_policy | passive_aware_diagnostic_required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 47 | 16 | 47 | 86 | 9009.8 | 19.3231 | -80.3328 | -33.1341 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 2 | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 47 | 16 | 47 | 86 | 9009.8 | 19.3231 | -80.3328 | -33.1341 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 3 | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP4_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 47 | 16 | 47 | 86 | 9009.8 | 19.3231 | -80.3328 | -33.1341 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 4 | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP4_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 47 | 16 | 47 | 86 | 9009.8 | 19.3231 | -80.3328 | -33.1341 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 5 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p500_TOP3_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.5 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 1 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 6 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p500_TOP3_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.5 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 2 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 7 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p500_TOP3_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.5 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 4 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 8 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p500_TOP4_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 1 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 9 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p500_TOP4_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 2 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 10 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p500_TOP4_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 4 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 11 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p750_TOP3_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.75 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 1 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 12 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p750_TOP3_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.75 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 2 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 13 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p750_TOP3_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.75 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 4 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 14 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p750_TOP4_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC1_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.75 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 1 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 15 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p750_TOP4_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.75 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 2 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 16 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p350_DSQ0p750_TOP4_H1800_long_only_taker_entry_taker_exit_CAP100000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.35 | 0.75 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 100000 | 4 | 45 | 9 | 45 | 45 | 2695.4 | 15.0942 | -98.4482 | -71.9317 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 17 | P335_P334_LANE_B_TURNOVER_COMPRESSION_SQ0p500_SPQ0p500_DSQ0p500_TOP2_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_B_TURNOVER_COMPRESSION | 1800 | 0.5 | 0.5 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 18 | P335_P334_LANE_B_TURNOVER_COMPRESSION_SQ0p500_SPQ0p500_DSQ0p500_TOP2_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_B_TURNOVER_COMPRESSION | 1800 | 0.5 | 0.5 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 19 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p500_TOP3_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.5 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 20 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p500_TOP3_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.5 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 21 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p500_TOP4_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 22 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p500_TOP4_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 23 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p750_TOP3_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.75 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 24 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p750_TOP3_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.75 | 3 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 25 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p750_TOP4_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.75 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 26 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p750_TOP4_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.75 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 46 | 16 | 46 | 90 | 6368.14 | 13.9545 | -79.1899 | -67.5762 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 27 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p500_TOP4_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT50000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 50000 | 4 | 46 | 21 | 46 | 153 | 5967.18 | 13.0759 | -85.1209 | -52.3718 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 28 | P335_P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN_SQ0p500_SPQ0p500_DSQ0p750_TOP4_H1800_long_only_taker_entry_taker_exit_CAP250000_NOT50000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_C_SPREAD_AND_BOOK_QUALITY_MARGIN | 1800 | 0.5 | 0.5 | 0.75 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 50000 | 4 | 46 | 21 | 46 | 153 | 5967.18 | 13.0759 | -85.1209 | -52.3718 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 29 | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 50000 | 2 | 47 | 16 | 47 | 86 | 2378.36 | 12.752 | -111.818 | -52.8195 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 30 | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 50000 | 4 | 47 | 16 | 47 | 86 | 2378.36 | 12.752 | -111.818 | -52.8195 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 31 | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP4_H900_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC2_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 50000 | 2 | 47 | 16 | 47 | 86 | 2378.36 | 12.752 | -111.818 | -52.8195 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |
| 32 | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP4_H900_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC4_zerodha_2x_all_in_cost_proxy | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 50000 | 4 | 47 | 16 | 47 | 86 | 2378.36 | 12.752 | -111.818 | -52.8195 | 1 | 1 | phase336_acceptance_grade_candidate_ledger | 0 | 0 | taker_entry_taker_exit | 1 |

## Passive-aware charter reconciliation

| charter_item | status | phase337_interpretation | phase337_requirement |
| --- | --- | --- | --- |
| attached_charter_present | applied | The attached passive-aware execution charter was read and reconciled into the current Phase337 precommit. | charter_text_recorded_before_results |
| stale_phase_numbering | renumbered_not_reopened | The document uses older Phase300 language; current repo evidence already has Phase300/Phase336 state, so the substance is carried forward without reopening old Phase300 as accepted. | use_current_phase337_route |
| passive_aware_hybrid_execution | required_as_holdout_diagnostic | Passive-aware hybrid execution must be evaluated alongside frozen directional candidates, but it cannot override failed primary passive-aware evidence unless it passes all realism penalties. | phase338_compare_taker_primary_vs_passive_aware_diagnostic |
| fill_model | required | Passive entries must draw from a pessimistic retail queue-depth fill probability, never assumed fills. | fill_probability_applied_to_every_passive_entry |
| adverse_selection | required | Filled passive orders must pay a fill-conditioned toxicity/adverse-selection penalty. | adverse_selection_penalty_applied_to_every_passive_fill |
| forced_flatten | required | Any unexited inventory must pay taker flatten spread plus full statutory costs by signal expiry or end of day. | forced_flatten_cost_applied_to_leftover_inventory |
| no_maker_rebate | required | No maker rebate is allowed for retail execution assumptions. | maker_rebate_assumed_zero |
| terminal_killswitch | preserved | If holdout fails breadth, 2x cost, or realism-penalty requirements, the route closes rather than being rescued by weakening penalties. | no_rescue_iteration_after_phase338_failure |

## Holdout contract

| contract_id | contract_value | description |
| --- | --- | --- |
| input_candidates | outputs/phase336/phase336_acceptance_grade_candidate_ledger.csv | Freeze Phase336-preserved acceptance-grade training candidates before any holdout result. |
| candidate_rows_frozen | 32 | All Phase336 candidate rows are carried forward without post-hoc filtering. |
| candidate_selection_tuning_allowed | 0 | No holdout-date tuning, no post-result candidate selection, no new filters. |
| primary_scope | phase335_cost200_acceptance_grade_candidates | Primary holdout validates the positive cost-stress training pocket. |
| charter_scope | attached_passive_aware_directional_execution_charter | The attached passive-aware charter is applied as a Phase337/Phase338 execution diagnostic contract. |
| annualized_threshold_pct | 12 | User profitability threshold remains >12%. |
| robust_event_floor | 30 | Sparse pockets below 30 scheduled events remain discovery clues only. |
| minimum_positive_symbol_date_cells | 2 | Breadth cannot be a single symbol/date pocket. |
| required_cost_profile | zerodha_2x_all_in_cost_proxy | 2x Zerodha all-in cost stress is required. |
| cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha equity intraday NSE cost formula. |
| fixed_capital_denominator | required | Annualized return must use fixed initial capital, not unlimited capital. |
| initial_capital_source | frozen_candidate_initial_capital_inr | Use the frozen candidate's capital denominator. |
| full_top_five_depth_required | 1 | Use market-by-price top-five depth. |
| levels_2_to_5_materiality_required | 1 | Depth beyond L1 must be material to features/filters/diagnostics. |
| l1_only_variant_rows_allowed | 0 | No L1-only variants. |
| net_edge_live_mask_rows_allowed | 0 | No future outcome/net-edge live masks. |
| passive_fill_model_required | 1 | Passive-aware diagnostic must use queue-depth fill probability. |
| adverse_selection_penalty_required | 1 | Passive fills must include toxicity/adverse-selection penalty. |
| forced_flatten_cost_required | 1 | Leftover inventory must pay taker flatten plus full costs. |
| maker_rebate_allowed | 0 | No maker rebate for retail assumptions. |
| passive_aware_primary_rescue_allowed | 0 | Prior passive-aware evidence remains diagnostic; it cannot rescue the route unless all hard gates pass. |
| rank_stability_required | 1x_to_2x_no_ordering_reversal | Cost-stress ranking should not depend on fragile cost-order reversal. |
| negative_controls_required | side_flip;random_side;breadth | Holdout execution must preserve controls. |
| kill_switch_no_weakening | 1 | Do not weaken realism penalties, cost threshold, or event floor to rescue failure. |
| strategy_replay_allowed | 0 | Phase337 is precommit only. |
| strategy_promotion_allowed | 0 | No strategy promotion opens here. |
| paper_or_live_acceptance_allowed | 0 | No paper/live acceptance opens here. |
| deployable_profitability_claim_allowed | 0 | No deployable profitability claim opens here. |
| phase338_execution_allowed_next | 1 | If gates pass, Phase338 may execute the frozen holdout contract. |
| charter_requirements_recorded | 8 | Charter-derived requirements recorded in reconciliation ledger. |

## Phase338 work order

| work_order_id | action | requirements | frozen_candidate_rows |
| --- | --- | --- | --- |
| P338_FREEZE_INPUTS | load_frozen_candidates | Use only Phase337 frozen candidate rows; no post-hoc additions. | 32 |
| P338_PRIMARY_HOLDOUT | execute_taker_policy_holdout | Evaluate frozen primary execution policies under 2x Zerodha costs and fixed capital. | 32 |
| P338_PASSIVE_AWARE_DIAGNOSTIC | execute_passive_aware_hybrid_diagnostic | Apply fill probability, adverse selection, forced flatten, no maker rebate. | 32 |
| P338_FULL_DEPTH_AUDIT | verify_l1_l5_depth_materiality | Confirm levels 2-5 are used and L1-only rows are zero. | 32 |
| P338_NO_LOOKAHEAD_AUDIT | verify_no_future_masks | Confirm net_edge_live_mask_rows and target live-mask rows are zero. | 32 |
| P338_CONTROLS | run_side_flip_random_side_breadth_controls | Require no cost-stress order reversal and positive breadth. | 32 |
| P338_KILLSWITCH | apply_no_rescue_killswitch | Close route if event floor, 2x cost, breadth, or realism penalties fail. | 32 |
| P338_REPORTING | write_holdout_execution_ledgers | Write scenario, control, passive diagnostic, gate, and interpretation outputs. | 32 |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P337_PHASE336_COMPLETE | True | 1 | 1 | hard |
| P337_PHASE336_ROUTE_MATCH | True | run_phase337_cost_stress_holdout_validation_precommit_no_replay | run_phase337_cost_stress_holdout_validation_precommit_no_replay | hard |
| P337_CANDIDATES_FROZEN | True | 32 | >0 | hard |
| P337_ACCEPTANCE_EVENT_FLOOR_FROZEN | True | 45 | >=30 | hard |
| P337_CHARTER_RECONCILED | True | 8 | >0 | hard |
| P337_PASSIVE_REALISM_PENALTIES_REQUIRED | True | adverse_selection;fill_model;forced_flatten;no_maker_rebate | adverse_selection;fill_model;forced_flatten;no_maker_rebate | hard |
| P337_COST200_FIXED_CAPITAL_REQUIRED | True | cost=zerodha_2x_all_in_cost_proxy;capital=required | zerodha_2x_all_in_cost_proxy;fixed | hard |
| P337_FULL_DEPTH_REQUIRED | True | top5=1;l2_l5=1 | both=1 | hard |
| P337_L1_ONLY_FORBIDDEN | True | 0 | 0 | hard |
| P337_NO_LOOKAHEAD | True | 0 | 0 | hard |
| P337_BOUNDARIES_CLOSED | True | phase336_replay=0;phase336_claim=0;contract_replay=0;contract_claim=0 | all_zero | hard |
| P337_PHASE338_WORK_ORDER_PRESENT | True | 8 | >=8 | hard |


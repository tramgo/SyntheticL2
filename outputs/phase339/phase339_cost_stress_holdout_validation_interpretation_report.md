# Phase339 Cost-Stress Holdout Validation Interpretation

Phase339 interprets the Phase338 synthetic holdout execution.
It preserves the primary taker survivors, records that passive-aware diagnostics did not rescue the edge, requires official NSE/SEBI/BSE catalyst-calendar alignment before real-day diagnostics, and keeps paper/live/profitability claims closed.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase339_cost_stress_holdout_validation_interpretation_complete | 1 | Phase339 interpretation completed |
| phase339_primary_taker_route_survived_synthetic_holdout | 1 | Primary taker route survived synthetic holdout |
| phase339_survivor_rows_preserved | 8 | Phase338 survivor rows preserved |
| phase339_best_survivor_candidate | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | Best survivor candidate |
| phase339_best_survivor_annualized_return_pct | 20.8293 | Best survivor annualized return |
| phase339_best_survivor_scheduled_events | 34 | Best survivor scheduled events |
| phase339_best_survivor_positive_symbol_date_cells | 30 | Best survivor positive symbol-date cells |
| phase339_passive_aware_route_status | diagnostic_failed_not_primary_rescue | Passive-aware route status |
| phase339_passive_aware_cost200_acceptance_rows | 0.0 | Passive-aware 2x-cost acceptance rows |
| phase339_synthetic_holdout_boundary | not_deployable_profitability | Synthetic holdout boundary |
| phase339_selected_next_route | P340_OFFICIAL_CATALYST_CALENDAR_ACQUISITION_PRECOMMIT | Selected next route |
| phase339_contract_rows | 26 | Phase340 official catalyst calendar contract rows |
| phase339_real_event_overlap_date_rows | 3 | Local real dates overlapping event-catalyst calendar |
| phase339_real_event_overlap_symbol_rows | 32 | Symbols on overlapping real/event dates |
| phase339_real_event_overlap_dates | 2026-07-14;2026-07-15;2026-07-16 | Overlapping real/event dates |
| phase339_real_event_overlap_event_types | synthetic_calendar_rbi_policy_like | Overlapping event types |
| phase339_sbin_real_event_overlap_date_rows | 3 | SBIN real/event overlap dates |
| phase339_strategy_replay_allowed | 0 | No replay |
| phase339_strategy_promotion_allowed | 0 | No promotion |
| phase339_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase339_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase339_hard_gate_pass_rows | 11 | Passed hard gates |
| phase339_hard_gate_rows | 11 | Hard gates |
| phase339_next_best_action | run_phase340_official_catalyst_calendar_acquisition_precommit_no_paper_live | Recommended next action |

## Survivor ledger

| source_scenario_id | freeze_rank | lane_id | horizon_seconds | signal_quantile | spread_max_quantile | depth_share_min_quantile | top_n_per_event | side_policy | execution_policy | cost_profile | initial_capital_inr | fixed_notional_inr | max_concurrent_positions | scheduled_event_rows | symbol_rows | observed_trade_dates | trade_rows | positive_symbol_date_cells | net_pnl_inr | annualized_return_pct | side_flip_annualized_return_pct | random_side_annualized_return_pct | control_pass | holdout_acceptance_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | 1 | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 34 | 17 | 34 | 62 | 30 | 7025.75 | 20.8293 | -81.631 | -33.2343 | 1 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | 2 | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 34 | 17 | 34 | 62 | 30 | 7025.75 | 20.8293 | -81.631 | -33.2343 | 1 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP4_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | 3 | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 2 | 34 | 17 | 34 | 62 | 30 | 7025.75 | 20.8293 | -81.631 | -33.2343 | 1 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP4_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC4_zerodha_2x_all_in_cost_proxy | 4 | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 250000 | 100000 | 4 | 34 | 17 | 34 | 62 | 30 | 7025.75 | 20.8293 | -81.631 | -33.2343 | 1 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC2_zerodha_2x_all_in_cost_proxy | 29 | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 50000 | 2 | 34 | 17 | 34 | 62 | 28 | 1979.24 | 14.6697 | -113.406 | -52.9098 | 1 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC4_zerodha_2x_all_in_cost_proxy | 30 | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 2 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 50000 | 4 | 34 | 17 | 34 | 62 | 28 | 1979.24 | 14.6697 | -113.406 | -52.9098 | 1 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP4_H900_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC2_zerodha_2x_all_in_cost_proxy | 31 | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 50000 | 2 | 34 | 17 | 34 | 62 | 28 | 1979.24 | 14.6697 | -113.406 | -52.9098 | 1 | 1 |
| P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP4_H900_long_only_taker_entry_taker_exit_CAP100000_NOT50000_CONC4_zerodha_2x_all_in_cost_proxy | 32 | P334_LANE_D_HORIZON_AND_EXIT_MARGIN | 900 | 0.75 | 1 | 0.5 | 4 | long_only | taker_entry_taker_exit | zerodha_2x_all_in_cost_proxy | 100000 | 50000 | 4 | 34 | 17 | 34 | 62 | 28 | 1979.24 | 14.6697 | -113.406 | -52.9098 | 1 | 1 |

## Failure and limit ledger

| failure_or_limit | observed_value | interpretation |
| --- | --- | --- |
| passive_aware_charter_not_primary_rescue | passive_above12=0;passive_acceptance=0 | Passive-aware execution with fill/adverse/flatten penalties did not produce 2x-cost above-12 rows; keep it diagnostic. |
| synthetic_holdout_not_deployable_profitability | 1 | The holdout partition is synthetic/deterministic from the generated feature matrix, so it cannot by itself prove live profitability. |
| primary_route_survived_but_requires_replication | 8 | Primary taker route survived Phase338, so the next honest step is controlled replication precommit rather than paper/live promotion. |
| do_not_tune_same_holdout | closed | Do not add filters, weaken cost stress, lower event floor, or reuse holdout outcomes for tuning. |

## Decision ledger

| decision_id | decision_value | evidence | interpretation |
| --- | --- | --- | --- |
| phase338_execution_complete | 1 | Phase338 hard gates passed before interpretation. | Phase338 can be interpreted. |
| primary_taker_route_survived_synthetic_holdout | 1 | acceptance_rows=8 | Primary taker execution remains the only surviving route. |
| best_survivor_preserved | P335_P334_LANE_D_HORIZON_AND_EXIT_MARGIN_SQ0p750_SPQ1p000_DSQ0p500_TOP2_H900_long_only_taker_entry_taker_exit_CAP250000_NOT100000_CONC2_zerodha_2x_all_in_cost_proxy | annualized=20.82928580629932;events=34;symbol_date_cells=30 | Preserve the best Phase338 survivor for replication precommit. |
| survivor_rows_preserved | 8 | primary_acceptance=8 | Carry forward all Phase338 primary 2x-cost survivors. |
| passive_aware_route_status | diagnostic_failed_not_primary_rescue | passive_acceptance=0 | Attached passive-aware charter did not produce accepted 2x-cost diagnostics. |
| synthetic_holdout_boundary | not_deployable_profitability | synthetic event-hash partition | Do not claim live profitability from synthetic holdout evidence. |
| paper_live_or_promotion_allowed | 0 | closed | No paper/live, promotion, or deployable profitability opens from Phase339. |
| next_route | P340_OFFICIAL_CATALYST_CALENDAR_ACQUISITION_PRECOMMIT | run_phase340_official_catalyst_calendar_acquisition_precommit_no_paper_live | Acquire and align official NSE/SEBI/BSE catalyst calendars before any catalyst-grounded real-day survivor diagnostic. |

## Phase340 real-day diagnostic contract

| contract_id | contract_value | description |
| --- | --- | --- |
| input_survivors | outputs/phase339/phase339_survivor_ledger.csv | Use only Phase339-preserved Phase338 primary 2x-cost survivors. |
| survivor_rows | 8 | Survivors cannot be expanded by post-hoc search. |
| official_catalyst_calendar_required | 1 | Do not rely on synthetic event labels for catalyst-grounded real-day validation. |
| official_sources | NSE corporate announcements;NSE financial results;SEBI corporate filings index;BSE corporate filings as cross-check | Use exchange/regulator-published filings and announcements as the catalyst calendar source. |
| real_data_root | real_data_sample/l2_multiday_panel | Use already-downloaded local real Zerodha WebSocket top-five L2 after official catalyst dates are aligned. |
| derived_real_feature_root | derived_real_l2_receive_flow_features_phase176 | Use local Phase176 real receive-flow features for the first live-day compatibility diagnostic. |
| local_real_dates_available | 7 | Current local imported real panel has seven dates and thirty-two symbols. |
| real_day_goal | official_catalyst_aligned_schema_compatibility_and_survivor_directional_diagnostic | Test whether the synthetic survivor has an honest real-day analogue only after official catalyst-date alignment; do not claim direct strategy validation if schemas differ. |
| schema_gap_must_be_logged | 1 | Phase340 must explicitly log synthetic Phase330 vs real Phase176 schema gaps. |
| annualized_threshold_pct | 12 | Do not lower >12% annualized threshold. |
| robust_event_floor | 30 | Do not accept sparse sub-30-event pockets. |
| minimum_positive_symbol_date_cells | 2 | Breadth must not be single symbol/date. |
| cost_profile_required | zerodha_2x_all_in_cost_proxy | 2x Zerodha all-in cost stress remains required. |
| cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha equity intraday cost formula. |
| fixed_capital_denominator | required | Annualized return remains fixed-capital, not unlimited capital. |
| full_top_five_depth_required | 1 | Top-five market-by-price depth remains core. |
| levels_2_to_5_materiality_required | 1 | Levels 2-5/beyond-L1 materiality remains required. |
| l1_only_allowed | 0 | No L1-only variants. |
| net_edge_live_mask_allowed | 0 | No future outcome/net-edge live masks. |
| passive_aware_status | diagnostic_failed_not_primary_rescue | Do not use passive-aware diagnostics to rescue acceptance. |
| holdout_tuning_allowed | 0 | No tuning on Phase338 holdout outcomes. |
| strategy_replay_allowed | 0 | Phase339 is interpretation only. |
| strategy_promotion_allowed | 0 | No promotion. |
| paper_or_live_acceptance_allowed | 0 | No paper/live acceptance. |
| deployable_profitability_claim_allowed | 0 | No deployable profitability claim. |
| phase340_precommit_allowed_next | 1 | If gates pass, Phase340 may precommit official catalyst calendar acquisition and alignment. |

## Real/event overlap ledger

| real_root | real_date_rows | real_symbol_rows | event_calendar_date_rows | event_calendar_symbol_rows | overlap_event_symbol_rows | overlap_date_rows | overlap_symbol_rows | overlap_dates | overlap_event_types | sbin_overlap_date_rows | sbin_overlap_dates | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_data_sample\l2_multiday_panel | 7 | 32 | 50 | 32 | 96 | 3 | 32 | 2026-07-14;2026-07-15;2026-07-16 | synthetic_calendar_rbi_policy_like | 3 | 2026-07-14;2026-07-15;2026-07-16 | real L2 overlaps event-catalyst calendar |
| derived_real_l2_receive_flow_features_phase176 | 7 | 32 | 50 | 32 | 96 | 3 | 32 | 2026-07-14;2026-07-15;2026-07-16 | synthetic_calendar_rbi_policy_like | 3 | 2026-07-14;2026-07-15;2026-07-16 | real L2 overlaps event-catalyst calendar |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P339_PHASE338_COMPLETE | True | 1 | 1 | hard |
| P339_PHASE338_GATES_PASSED | True | 12/12 | all | hard |
| P339_PRIMARY_SURVIVORS_PRESENT | True | phase338=8;ledger=8 | >0 | hard |
| P339_PASSIVE_STATUS_RECORDED | True | 0 | 0 | hard |
| P339_SYNTHETIC_BOUNDARY_RECORDED | True | recorded | recorded | hard |
| P339_REAL_DAY_CONTRACT_PRESENT | True | 26 | >=20 | hard |
| P339_REAL_EVENT_DATE_OVERLAP_PRESENT | True | 3 | >0 | hard |
| P339_SBIN_EVENT_DATE_OVERLAP_PRESENT | True | 3 | >0 | hard |
| P339_FULL_DEPTH_PRESERVED | True | top5=1;l2_l5=1 | both=1 | hard |
| P339_NO_LOOKAHEAD_OR_L1_ONLY | True | l1=0;lookahead=0 | both=0 | hard |
| P339_BOUNDARIES_CLOSED | True | replay=0;claim=0;contract_claim=0 | all_zero | hard |


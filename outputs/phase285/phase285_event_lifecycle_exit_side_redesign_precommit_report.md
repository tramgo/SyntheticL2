# Phase285 Event Lifecycle / Side / Exit Redesign Precommit

Generated UTC: 2026-08-02T07:58:53.281371+00:00

Phase285 converts the Phase284 decision into an executable Phase286 search contract.
The selected pivot is not another static filter layer: Phase286 must test trade side, entry delay, exit horizon, take-profit/stop/timeout behavior, latency bucket, queue adversity, and fixed-capital cost200 capacity.
Full Zerodha top-five rows 1-5 and levels 2-5 / beyond-L1 materiality remain mandatory; L1-only variants and net-edge live masks remain forbidden.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase285_lifecycle_redesign_precommit_complete | 1 | Phase285 event lifecycle/side/exit redesign precommit completed |
| phase285_selected_route | P285_EVENT_LIFECYCLE_EXIT_SIDE_REDESIGN_PRECOMMIT | Selected route |
| phase285_preserved_phase283_clue_rows | 10 | Preserved Phase283 clue rows |
| phase285_phase286_lifecycle_seed_rows | 10 | Eligible Phase286 lifecycle seeds |
| phase285_event_universe_rows | 1280 | Full-depth event universe rows |
| phase285_event_universe_dates | 8 | Event-universe dates |
| phase285_event_universe_symbols | 7 | Event-universe symbols |
| phase285_phase283_scheduled_rows | 27 | Phase283 scheduled rows sampled |
| phase285_phase283_rejected_same_symbol_overlap_rows | 234 | Same-symbol overlap bottleneck rows |
| phase285_phase283_rejected_max_concurrent_rows | 4215 | Max-concurrency bottleneck rows |
| phase285_lifecycle_family_rows | 5 | Lifecycle families defined |
| phase285_phase286_allowed_lifecycle_family_rows | 5 | Lifecycle families allowed for Phase286 |
| phase285_entry_exit_grid_rows | 12 | Entry/exit grid rows |
| phase285_capital_cost_contract_rows | 8 | Capital/cost contract rows |
| phase285_cost200_required | 1 | Cost200 required |
| phase285_fixed_capital_required | 1 | Fixed-capital denominator required |
| phase285_sparse_diagnostic_event_floor | 8 | Sparse diagnostic event floor |
| phase285_robust_portfolio_event_floor | 30 | Robust portfolio event floor |
| phase285_full_depth_required | 1 | Full top-five and levels 2-5 required |
| phase285_beyond_l1_features_required | 1 | Beyond-L1 features required |
| phase285_l1_only_allowed | 0 | L1-only variants forbidden |
| phase285_net_edge_live_mask_allowed | 0 | Net/gross edge live masks forbidden |
| phase285_strategy_replay_allowed | 0 | No strategy replay unlocked |
| phase285_strategy_promotion_allowed | 0 | No strategy promotion unlocked |
| phase285_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance |
| phase285_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase285_hard_gate_pass_rows | 12 | Hard gates passed |
| phase285_hard_gate_rows | 12 | Hard gates evaluated |
| phase285_next_best_action | run_phase286_event_lifecycle_exit_side_redesign_search_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P285_PHASE284_WORK_ORDER_PRESENT | True | run_phase285_event_lifecycle_exit_side_redesign_precommit_no_paper_live | Phase284 next action targets Phase285 | hard |
| P285_PHASE284_INTERPRETATION_COMPLETE | True | 1 | Phase284 complete | hard |
| P285_PHASE283_CLOSED_AND_COST_PRESERVED | True | close=1;do_not_relax=1;do_not_claim=1 | Phase283 closed, cost threshold preserved, portfolio claim blocked | hard |
| P285_ROUTE_CONTRACT_PRESENT | True | 8 | Phase284 route contract present | hard |
| P285_LIFECYCLE_SEEDS_PRESENT | True | 10 | >0 eligible full-depth lifecycle seeds | hard |
| P285_EVENT_UNIVERSE_DIAGNOSTICS_PRESENT | True | 11 | event-universe diagnostics present | hard |
| P285_LIFECYCLE_FAMILIES_PRESENT | True | families=5;allowed=5 | >=5 lifecycle families allowed | hard |
| P285_ENTRY_EXIT_GRID_PRESENT | True | grid=12;allowed=12 | >=12 lifecycle grid rows allowed | hard |
| P285_CAPITAL_COST_CONTROLS_PRESENT | True | 8 | capital/cost controls present | hard |
| P285_FULL_DEPTH_AND_LEAKAGE_BOUNDARY | True | l1_allowed_sum=0;live_mask_allowed_sum=0 | L1-only and live label masks forbidden | hard |
| P285_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |
| P285_NEXT_ROUTE_SELECTED | True | P286 lifecycle search | Phase286 search route selected | hard |

## Preserved Phase283 Clues

| phase283_variant_id | ensemble_family_id | ensemble_family | bucket_id | vote_threshold | seed_ids | included_target_families | max_annualized_pct | median_annualized_pct | max_scheduled_event_rows | selected_event_rows | cost200_above12_sparse_diagnostic_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | full_depth_positive_clue | near_miss_under_12 | too_sparse_for_portfolio_claim | uses_top5 | uses_levels_2_to_5 | l1_only_variant | uses_net_edge_as_live_mask | preserve_as_lifecycle_seed_not_acceptance | eligible_for_phase286_lifecycle_seed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P283_P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE_V1_P282_DEPTH_STABLE_BUCKET | P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE | adverse_avoid_net_label_ensemble | P282_DEPTH_STABLE_BUCKET | 1 | P280_SPREAD_REPLENISH_COMBO_Q70;P280_ADVERSE_SELECTION_AVOID_Q60;P280_ADVERSE_SELECTION_AVOID_Q80;P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | adverse_selection_avoidance;net_edge_distribution_shift;spread_cost_margin | 11.2825 | 7.55433 | 3 | 199 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| P283_P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE_V2_ALL_EVENTS | P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE | adverse_avoid_net_label_ensemble | ALL_EVENTS | 2 | P280_SPREAD_REPLENISH_COMBO_Q70;P280_ADVERSE_SELECTION_AVOID_Q60;P280_ADVERSE_SELECTION_AVOID_Q80;P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | adverse_selection_avoidance;net_edge_distribution_shift;spread_cost_margin | 11.2825 | 7.7784 | 3 | 121 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| P283_P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE_V2_P282_DEPTH_STABLE_BUCKET | P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE | adverse_avoid_net_label_ensemble | P282_DEPTH_STABLE_BUCKET | 2 | P280_SPREAD_REPLENISH_COMBO_Q70;P280_ADVERSE_SELECTION_AVOID_Q60;P280_ADVERSE_SELECTION_AVOID_Q80;P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | adverse_selection_avoidance;net_edge_distribution_shift;spread_cost_margin | 11.2825 | 7.55433 | 3 | 63 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| P283_P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE_V2_P282_SPREAD_COMPRESSED_BUCKET | P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE | adverse_avoid_net_label_ensemble | P282_SPREAD_COMPRESSED_BUCKET | 2 | P280_SPREAD_REPLENISH_COMBO_Q70;P280_ADVERSE_SELECTION_AVOID_Q60;P280_ADVERSE_SELECTION_AVOID_Q80;P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | adverse_selection_avoidance;net_edge_distribution_shift;spread_cost_margin | 11.2825 | 7.7784 | 3 | 121 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| P283_P282_FAMILY_VOTE_ENSEMBLE_V2_ALL_EVENTS | P282_FAMILY_VOTE_ENSEMBLE | family_vote_ensemble | ALL_EVENTS | 2 | P280_SPREAD_REPLENISH_COMBO_Q70;P280_TIME_TO_EXIT_SHORT_HQ90;P280_ADVERSE_SELECTION_AVOID_Q60;P280_ADVERSE_SELECTION_AVOID_Q80;P280_REPLENISH_CONFIRM_Q50;P280_TIME_TO_EXIT_SHORT_HQ70;P280_TIME_TO_EXIT_SHORT_HQ80;P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | adverse_selection_avoidance;depth_replenishment_confirmation;net_edge_distribution_shift;spread_cost_margin;time_to_exit | 11.2825 | 7.72063 | 3 | 317 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| P283_P282_FAMILY_VOTE_ENSEMBLE_V2_P282_DEPTH_STABLE_BUCKET | P282_FAMILY_VOTE_ENSEMBLE | family_vote_ensemble | P282_DEPTH_STABLE_BUCKET | 2 | P280_SPREAD_REPLENISH_COMBO_Q70;P280_TIME_TO_EXIT_SHORT_HQ90;P280_ADVERSE_SELECTION_AVOID_Q60;P280_ADVERSE_SELECTION_AVOID_Q80;P280_REPLENISH_CONFIRM_Q50;P280_TIME_TO_EXIT_SHORT_HQ70;P280_TIME_TO_EXIT_SHORT_HQ80;P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | adverse_selection_avoidance;depth_replenishment_confirmation;net_edge_distribution_shift;spread_cost_margin;time_to_exit | 11.2825 | 7.55433 | 3 | 143 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| P283_P282_FAMILY_VOTE_ENSEMBLE_V2_P282_SPREAD_COMPRESSED_BUCKET | P282_FAMILY_VOTE_ENSEMBLE | family_vote_ensemble | P282_SPREAD_COMPRESSED_BUCKET | 2 | P280_SPREAD_REPLENISH_COMBO_Q70;P280_TIME_TO_EXIT_SHORT_HQ90;P280_ADVERSE_SELECTION_AVOID_Q60;P280_ADVERSE_SELECTION_AVOID_Q80;P280_REPLENISH_CONFIRM_Q50;P280_TIME_TO_EXIT_SHORT_HQ70;P280_TIME_TO_EXIT_SHORT_HQ80;P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | adverse_selection_avoidance;depth_replenishment_confirmation;net_edge_distribution_shift;spread_cost_margin;time_to_exit | 11.2825 | 7.72063 | 3 | 304 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| P283_P282_FAMILY_VOTE_ENSEMBLE_V3_ALL_EVENTS | P282_FAMILY_VOTE_ENSEMBLE | family_vote_ensemble | ALL_EVENTS | 3 | P280_SPREAD_REPLENISH_COMBO_Q70;P280_TIME_TO_EXIT_SHORT_HQ90;P280_ADVERSE_SELECTION_AVOID_Q60;P280_ADVERSE_SELECTION_AVOID_Q80;P280_REPLENISH_CONFIRM_Q50;P280_TIME_TO_EXIT_SHORT_HQ70;P280_TIME_TO_EXIT_SHORT_HQ80;P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | adverse_selection_avoidance;depth_replenishment_confirmation;net_edge_distribution_shift;spread_cost_margin;time_to_exit | 11.2825 | 7.7784 | 3 | 121 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| P283_P282_FAMILY_VOTE_ENSEMBLE_V3_P282_DEPTH_STABLE_BUCKET | P282_FAMILY_VOTE_ENSEMBLE | family_vote_ensemble | P282_DEPTH_STABLE_BUCKET | 3 | P280_SPREAD_REPLENISH_COMBO_Q70;P280_TIME_TO_EXIT_SHORT_HQ90;P280_ADVERSE_SELECTION_AVOID_Q60;P280_ADVERSE_SELECTION_AVOID_Q80;P280_REPLENISH_CONFIRM_Q50;P280_TIME_TO_EXIT_SHORT_HQ70;P280_TIME_TO_EXIT_SHORT_HQ80;P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | adverse_selection_avoidance;depth_replenishment_confirmation;net_edge_distribution_shift;spread_cost_margin;time_to_exit | 11.2825 | 7.55433 | 3 | 63 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| P283_P282_FAMILY_VOTE_ENSEMBLE_V3_P282_SPREAD_COMPRESSED_BUCKET | P282_FAMILY_VOTE_ENSEMBLE | family_vote_ensemble | P282_SPREAD_COMPRESSED_BUCKET | 3 | P280_SPREAD_REPLENISH_COMBO_Q70;P280_TIME_TO_EXIT_SHORT_HQ90;P280_ADVERSE_SELECTION_AVOID_Q60;P280_ADVERSE_SELECTION_AVOID_Q80;P280_REPLENISH_CONFIRM_Q50;P280_TIME_TO_EXIT_SHORT_HQ70;P280_TIME_TO_EXIT_SHORT_HQ80;P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | adverse_selection_avoidance;depth_replenishment_confirmation;net_edge_distribution_shift;spread_cost_margin;time_to_exit | 11.2825 | 7.7784 | 3 | 121 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |

## Event Universe Diagnostics

| diagnostic_id | diagnostic_value | description |
| --- | --- | --- |
| event_universe_rows | 1280 | Phase277 full-depth event universe rows |
| event_universe_dates | 8 | Distinct event-universe dates |
| event_universe_symbols | 7 | Distinct event-universe symbols |
| event_universe_median_spread_bps | 4.91581 | Median event-universe spread |
| event_universe_positive_net_edge_rows | 547 | Rows with positive inherited net edge |
| phase283_ledger_rows | 4476 | Phase283 scheduled/rejected ledger rows sampled |
| phase283_scheduled_rows | 27 | Phase283 scheduled rows in ledger |
| phase283_rejected_rows | 4449 | Phase283 rejected rows in ledger |
| phase283_rejected_same_symbol_overlap_rows | 234 | Rejected same-symbol overlap rows |
| phase283_rejected_max_concurrent_rows | 4215 | Rejected max-concurrent rows |
| phase283_scheduled_median_net_edge_bps | 4.01483 | Median scheduled net edge in Phase283 ledger |

## Lifecycle Family Catalog

| lifecycle_family_id | lifecycle_family | primary_change | side_policy | entry_policy | exit_policy | eligible_seed_rows | cost_profile_required | fixed_capital_required | full_depth_required | levels_2_to_5_required | beyond_l1_features_required | l1_only_allowed | net_edge_live_mask_allowed | phase286_search_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P285_SIDE_FLIP_REVERSAL_TEST | side_flip_reversal_test | test whether the sparse follow-through clue is actually a reversal edge after entry costs | original;inverse | same_event | fixed_horizon | 10 | cost200 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| P285_ENTRY_DELAY_TEST | entry_delay_test | delay entry by one or more ticks/bars to avoid immediate adverse selection after the L2 signal | original;inverse | delay_1;delay_2;delay_3 | fixed_horizon | 10 | cost200 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| P285_SHORT_HORIZON_EXIT_TEST | short_horizon_exit_test | test whether edge exists before the current horizon leaks away | original;inverse | same_event;delay_1 | horizon_3;horizon_5;horizon_8 | 10 | cost200 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| P285_TAKE_PROFIT_STOP_TIMEOUT_TEST | take_profit_stop_timeout_test | bound tail losses and harvest early positive excursions instead of waiting for a fixed exit only | original;inverse | same_event;delay_1 | take_profit_4_8_bps;stop_loss_4_8_bps;timeout_horizon_5_10 | 10 | cost200 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST | queue_adversity_order_timing_test | stress order arrival timing and queue adversity rather than assuming the signal can trade instantly | original;inverse | latency_bucket_fast;latency_bucket_slow | fixed_horizon;timeout_horizon_5_10 | 10 | cost200 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |

## Entry Exit Grid Contract

| grid_id | side_multiplier | entry_delay_ticks | exit_horizon_ticks | take_profit_bps | stop_loss_bps | latency_bucket | cost_profile_required | fixed_capital_initial_capital_inr | full_depth_required | phase286_search_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P285_GRID_ORIG_E0_H3 | 1 | 0 | 3 |  |  | base | cost200 | 100000 | 1 | 1 |
| P285_GRID_ORIG_E0_H5 | 1 | 0 | 5 |  |  | base | cost200 | 100000 | 1 | 1 |
| P285_GRID_ORIG_E1_H5 | 1 | 1 | 5 |  |  | base | cost200 | 100000 | 1 | 1 |
| P285_GRID_ORIG_E2_H8 | 1 | 2 | 8 |  |  | slow | cost200 | 100000 | 1 | 1 |
| P285_GRID_INV_E0_H3 | -1 | 0 | 3 |  |  | base | cost200 | 100000 | 1 | 1 |
| P285_GRID_INV_E0_H5 | -1 | 0 | 5 |  |  | base | cost200 | 100000 | 1 | 1 |
| P285_GRID_INV_E1_H5 | -1 | 1 | 5 |  |  | base | cost200 | 100000 | 1 | 1 |
| P285_GRID_INV_E2_H8 | -1 | 2 | 8 |  |  | slow | cost200 | 100000 | 1 | 1 |
| P285_GRID_ORIG_TP4_SL4_H5 | 1 | 0 | 5 | 4 | 4 | base | cost200 | 100000 | 1 | 1 |
| P285_GRID_ORIG_TP8_SL4_H10 | 1 | 1 | 10 | 8 | 4 | slow | cost200 | 100000 | 1 | 1 |
| P285_GRID_INV_TP4_SL4_H5 | -1 | 0 | 5 | 4 | 4 | base | cost200 | 100000 | 1 | 1 |
| P285_GRID_INV_TP8_SL4_H10 | -1 | 1 | 10 | 8 | 4 | slow | cost200 | 100000 | 1 | 1 |

## Capital Cost Contract

| contract_id | contract_value | description | severity |
| --- | --- | --- | --- |
| P285_INITIAL_CAPITAL_INR | 100000.0 | Fixed capital denominator for Phase286 diagnostics | hard |
| P285_FIXED_NOTIONAL_GRID_INR | 25000;50000;75000;100000 | Fixed notional grid for lifecycle search | hard |
| P285_MAX_CONCURRENT_GRID | 1;2;4 | Concurrency grid to reduce two-trade bottleneck diagnostics | hard |
| P285_COST200_REQUIRED | Zerodha cost200 required for all acceptance diagnostics | hard |  |
| P285_ANNUALIZED_FORMULA | realized_net_pnl / initial_capital * 100 * 252 / observed_trade_dates | Fixed-capital annualized diagnostic formula | hard |
| P285_SPARSE_DIAGNOSTIC_EVENT_FLOOR | 8 | Minimum scheduled events for sparse >12 diagnostic | hard |
| P285_ROBUST_PORTFOLIO_EVENT_FLOOR | 30 | Minimum scheduled events for robust portfolio-return claim | hard |
| P285_NO_PROMOTION | no replay, promotion, paper/live, or deployable profitability claim | Boundaries remain closed | hard |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P286_INPUTS | outputs/phase277/phase277_cost200_redesign_event_universe.csv;outputs/phase285/phase285_preserved_phase283_clue_catalog.csv;outputs/phase285/phase285_lifecycle_family_catalog.csv;outputs/phase285/phase285_entry_exit_grid_contract.csv | Use full-depth event universe plus Phase285 lifecycle contract. |
| P286_LIFECYCLE_SEEDS | P283_P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE_V1_P282_DEPTH_STABLE_BUCKET;P283_P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE_V2_ALL_EVENTS;P283_P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE_V2_P282_DEPTH_STABLE_BUCKET;P283_P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE_V2_P282_SPREAD_COMPRESSED_BUCKET;P283_P282_FAMILY_VOTE_ENSEMBLE_V2_ALL_EVENTS;P283_P282_FAMILY_VOTE_ENSEMBLE_V2_P282_DEPTH_STABLE_BUCKET;P283_P282_FAMILY_VOTE_ENSEMBLE_V2_P282_SPREAD_COMPRESSED_BUCKET;P283_P282_FAMILY_VOTE_ENSEMBLE_V3_ALL_EVENTS;P283_P282_FAMILY_VOTE_ENSEMBLE_V3_P282_DEPTH_STABLE_BUCKET;P283_P282_FAMILY_VOTE_ENSEMBLE_V3_P282_SPREAD_COMPRESSED_BUCKET | Use preserved Phase283 full-depth near-misses only as search seeds. |
| P286_LIFECYCLE_FAMILIES | P285_SIDE_FLIP_REVERSAL_TEST;P285_ENTRY_DELAY_TEST;P285_SHORT_HORIZON_EXIT_TEST;P285_TAKE_PROFIT_STOP_TIMEOUT_TEST;P285_QUEUE_ADVERSITY_ORDER_TIMING_TEST | Execute allowed lifecycle families. |
| P286_ENTRY_EXIT_GRIDS | P285_GRID_ORIG_E0_H3;P285_GRID_ORIG_E0_H5;P285_GRID_ORIG_E1_H5;P285_GRID_ORIG_E2_H8;P285_GRID_INV_E0_H3;P285_GRID_INV_E0_H5;P285_GRID_INV_E1_H5;P285_GRID_INV_E2_H8;P285_GRID_ORIG_TP4_SL4_H5;P285_GRID_ORIG_TP8_SL4_H10;P285_GRID_INV_TP4_SL4_H5;P285_GRID_INV_TP8_SL4_H10 | Execute side/entry/exit/take-profit/stop/latency grid. |
| P286_SEARCH_TYPE | event_lifecycle_exit_side_redesign_search | Execute lifecycle search next. |
| P286_ACCEPTANCE_DIAGNOSTICS | cost200_annualized_pct_gt_12.0;scheduled_event_rows_ge_8_for_sparse_diagnostic;scheduled_event_rows_ge_30_for_portfolio_claim | Sparse >12 is a discovery clue; robust portfolio claim needs the larger event floor. |
| P286_BOUNDARY | no_paper_live;no_strategy_replay;no_deployable_profitability_claim;fixed_capital_required;full_depth_required;l1_only_forbidden;net_edge_live_mask_forbidden | Boundaries remain closed. |

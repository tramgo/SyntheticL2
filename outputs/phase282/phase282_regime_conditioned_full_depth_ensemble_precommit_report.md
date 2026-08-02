# Phase282 Regime-conditioned Full-depth Ensemble Precommit

Generated UTC: 2026-08-02T07:24:37.893284+00:00

Phase282 precommits a broader regime-conditioned full-depth ensemble search after Phase281 closed Phase280 for acceptance.
The next executable search must keep cost200, fixed-capital annualization, full-depth L2, event floors, and no paper/live boundaries.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase282_regime_conditioned_ensemble_precommit_complete | 1 | Phase282 regime-conditioned full-depth ensemble precommit completed |
| phase282_selected_route | P282_REGIME_CONDITIONED_FULL_DEPTH_ENSEMBLE_PRECOMMIT | Selected route |
| phase282_preserved_clue_rows | 8 | Preserved Phase281 clue rows |
| phase282_phase283_search_seed_rows | 8 | Eligible Phase283 search seeds |
| phase282_ensemble_family_rows | 4 | Ensemble families defined |
| phase282_phase283_allowed_ensemble_rows | 4 | Ensemble families allowed for Phase283 |
| phase282_regime_bucket_rows | 4 | Regime/time/spread/depth buckets defined |
| phase282_min_event_floor_diagnostic | 8 | Minimum scheduled-event floor for sparse diagnostic ranking |
| phase282_min_events_for_robust_portfolio_claim | 30 | Minimum scheduled-event floor for robust portfolio-return claim |
| phase282_cost200_required | 1 | Cost200 required |
| phase282_fixed_capital_required | 1 | Fixed-capital denominator required |
| phase282_full_depth_required | 1 | Full top-five and levels 2-5 required |
| phase282_l1_only_allowed | 0 | L1-only ensembles forbidden |
| phase282_net_edge_live_mask_allowed | 0 | Net/gross edge live masks forbidden |
| phase282_strategy_replay_allowed | 0 | No strategy replay unlocked |
| phase282_strategy_promotion_allowed | 0 | No strategy promotion unlocked |
| phase282_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance |
| phase282_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase282_hard_gate_pass_rows | 11 | Hard gates passed |
| phase282_hard_gate_rows | 11 | Hard gates evaluated |
| phase282_next_best_action | run_phase283_regime_conditioned_full_depth_ensemble_search_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P282_PHASE281_WORK_ORDER_PRESENT | True | run_phase282_regime_conditioned_full_depth_ensemble_precommit_no_paper_live | Phase281 next action targets Phase282 | hard |
| P282_PHASE281_INTERPRETATION_COMPLETE | True | 1 | Phase281 complete | hard |
| P282_PHASE280_CLOSED_AND_COST_PRESERVED | True | close=1;do_not_relax=1;do_not_claim=1 | Phase280 closed, cost threshold preserved, portfolio claim blocked | hard |
| P282_ROUTE_CONTRACT_PRESENT | True | 6 | Phase281 route contract present | hard |
| P282_CLUE_SEEDS_PRESENT | True | 8 | >0 eligible full-depth search seeds | hard |
| P282_ENSEMBLES_PRESENT | True | ensembles=4;allowed=4 | >=4 ensembles and >=3 allowed | hard |
| P282_REGIME_BUCKETS_PRESENT | True | buckets=4;allowed=4 | >=4 regime buckets allowed | hard |
| P282_SCORING_CONTROLS_PRESENT | True | 7 | scoring controls present | hard |
| P282_FULL_DEPTH_AND_LEAKAGE_BOUNDARY | True | l1_allowed_sum=0;live_mask_allowed_sum=0 | L1-only and live label masks forbidden | hard |
| P282_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |
| P282_NEXT_ROUTE_SELECTED | True | P283 ensemble search | Phase283 search route selected | hard |

## Preserved Clue Catalog

| phase280_variant_id | target_family_id | target_family | target_rule | max_annualized_pct | median_annualized_pct | max_scheduled_event_rows | selected_event_rows | material_full_depth_clue | near_miss_under_12 | uses_top5 | uses_levels_2_to_5 | l1_only_variant | uses_net_edge_as_offline_label | uses_net_edge_as_live_mask | preserve_as_ensemble_seed_not_acceptance | eligible_for_phase283_search_seed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P280_SPREAD_REPLENISH_COMBO_Q70 | P279_SPREAD_COST_MARGIN_TARGET | spread_cost_margin | avg_spread_bps <= q30 and depth_replenish_withdraw_ratio >= q70 and avg_depth_beyond_l1_qty_imbalance >= q60 | 11.2825 | 5.05313 | 3 | 67 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| P280_TIME_TO_EXIT_SHORT_HQ90 | P279_TIME_TO_EXIT_TARGET | time_to_exit | horizon <= 10 and depth_replenish_withdraw_ratio >= 12.933958 | 9.37048 | 4.14152 | 2 | 128 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| P280_ADVERSE_SELECTION_AVOID_Q60 | P279_ADVERSE_SELECTION_AVOIDANCE_TARGET | adverse_selection_avoidance | top5_churn_pressure <= 445889.435425 and depth_withdrawal_pressure <= 10300.394075 | 7.56387 | 5.90132 | 4 | 430 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| P280_ADVERSE_SELECTION_AVOID_Q80 | P279_ADVERSE_SELECTION_AVOIDANCE_TARGET | adverse_selection_avoidance | top5_churn_pressure <= 71224.830695 and depth_withdrawal_pressure <= 1231.635970 | 6.08829 | 6.07953 | 4 | 230 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| P280_REPLENISH_CONFIRM_Q50 | P279_REPLENISHMENT_CONFIRMATION_TARGET | depth_replenishment_confirmation | depth_replenish_withdraw_ratio >= 5.126904 and avg_level_weighted_depth_imbalance >= 0.557013 | 5.16974 | 3.24487 | 5 | 190 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| P280_TIME_TO_EXIT_SHORT_HQ70 | P279_TIME_TO_EXIT_TARGET | time_to_exit | horizon <= 10 and depth_replenish_withdraw_ratio >= 8.417774 | 4.49603 | 2.15341 | 3 | 384 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| P280_TIME_TO_EXIT_SHORT_HQ80 | P279_TIME_TO_EXIT_TARGET | time_to_exit | horizon <= 10 and depth_replenish_withdraw_ratio >= 10.699868 | 4.49603 | 2.15341 | 3 | 256 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | P279_NET_EDGE_DISTRIBUTION_SHIFT_TARGET | net_edge_distribution_shift | offline net-edge-positive label AND depth_consensus_imbalance >= 0.590831 and event_sparsity_pressure <= 1470251.984942 | 4.27432 | 4.17851 | 2 | 47 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 1 |

## Ensemble Family Catalog

| ensemble_family_id | ensemble_family | included_target_families | ensemble_rule | matched_target_family_rows | matched_target_families | cost_profile_required | fixed_capital_required | full_depth_required | levels_2_to_5_required | l1_only_allowed | net_edge_live_mask_allowed | phase283_search_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P282_SPREAD_REPLENISH_ADVERSE_ENSEMBLE | spread_replenish_adverse_ensemble | spread_cost_margin;depth_replenishment_confirmation;adverse_selection_avoidance | combine low-spread, replenishment-confirmed, low-withdrawal/low-churn full-depth clues | 3 | spread_cost_margin;depth_replenishment_confirmation;adverse_selection_avoidance | cost200 | 1 | 1 | 1 | 0 | 0 | 1 |
| P282_TIME_GATED_REPLENISH_ENSEMBLE | time_gated_replenish_ensemble | time_to_exit;depth_replenishment_confirmation;spread_cost_margin | condition short-exit clues by time-of-day and spread state before fixed-capital scoring | 3 | time_to_exit;depth_replenishment_confirmation;spread_cost_margin | cost200 | 1 | 1 | 1 | 0 | 0 | 1 |
| P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE | adverse_avoid_net_label_ensemble | adverse_selection_avoidance;net_edge_distribution_shift;spread_cost_margin | use net-edge labels only offline while live masks remain observable full-depth features | 3 | adverse_selection_avoidance;net_edge_distribution_shift;spread_cost_margin | cost200 | 1 | 1 | 1 | 0 | 0 | 1 |
| P282_FAMILY_VOTE_ENSEMBLE | family_vote_ensemble | spread_cost_margin;time_to_exit;adverse_selection_avoidance;depth_replenishment_confirmation;net_edge_distribution_shift | require two or more positive full-depth family votes with regime-specific thresholds | 5 | spread_cost_margin;time_to_exit;adverse_selection_avoidance;depth_replenishment_confirmation;net_edge_distribution_shift | cost200 | 1 | 1 | 1 | 0 | 0 | 1 |

## Regime Bucket Contract

| bucket_id | bucket_type | bucket_rule | purpose | full_depth_required | cost_profile_required | phase283_search_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| P282_TIME_OPEN_BUCKET | time_of_day | early/open bucket derived from richer_event_bar_id lower quantiles or available event timestamps | test whether near-miss edge is concentrated near the open without assuming a universal all-day effect | 1 | cost200 | 1 |
| P282_TIME_LATER_BUCKET | time_of_day | later bucket derived from richer_event_bar_id upper quantiles or available event timestamps | control for open-only overfitting and identify later-session pockets | 1 | cost200 | 1 |
| P282_SPREAD_COMPRESSED_BUCKET | spread_state | avg_spread_bps at or below configurable lower/middle quantiles | reduce cost hurdle and slippage pressure without lowering the Zerodha cost model | 1 | cost200 | 1 |
| P282_DEPTH_STABLE_BUCKET | depth_state | low top5 churn and low withdrawal pressure with positive levels 2-5 imbalance | distinguish stable liquidity from noisy one-bar depth flickers | 1 | cost200 | 1 |

## Scoring Control Contract

| scoring_control_id | scoring_control_value | severity |
| --- | --- | --- |
| P282_FIXED_CAPITAL_DENOMINATOR | annualized_return = realized_net_pnl / initial_capital * 100 * 252 / observed_trade_dates | hard |
| P282_COST200_REQUIRED | all Phase283 scenarios must use Zerodha cost200 or stronger stress | hard |
| P282_MIN_EVENT_FLOOR_DIAGNOSTIC | 8 | hard |
| P282_ROBUST_PORTFOLIO_CLAIM_FLOOR | 30 | hard |
| P282_NO_LABEL_LEAKAGE | net/gross edge may only define offline diagnostics, never live selection masks | hard |
| P282_FULL_DEPTH_REQUIRED | top-five rows 1-5 and levels 2-5/beyond-L1 materiality required | hard |
| P282_NO_PROMOTION | no strategy replay, promotion, paper/live acceptance, or deployable profitability claim | hard |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P283_INPUTS | outputs/phase280/phase280_material_target_scenario_results.csv;outputs/phase280/phase280_sample_material_target_scheduled_event_ledger.csv;outputs/phase282/phase282_ensemble_family_catalog.csv;outputs/phase282/phase282_regime_bucket_contract.csv | Use Phase280 evidence and Phase282 ensemble/regime contracts. |
| P283_SEARCH_SEEDS | P280_SPREAD_REPLENISH_COMBO_Q70;P280_TIME_TO_EXIT_SHORT_HQ90;P280_ADVERSE_SELECTION_AVOID_Q60;P280_ADVERSE_SELECTION_AVOID_Q80;P280_REPLENISH_CONFIRM_Q50;P280_TIME_TO_EXIT_SHORT_HQ70;P280_TIME_TO_EXIT_SHORT_HQ80;P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | Use preserved Phase280 full-depth clues as seeds, not accepted strategies. |
| P283_ENSEMBLE_FAMILIES | P282_SPREAD_REPLENISH_ADVERSE_ENSEMBLE;P282_TIME_GATED_REPLENISH_ENSEMBLE;P282_ADVERSE_AVOID_NET_LABEL_ENSEMBLE;P282_FAMILY_VOTE_ENSEMBLE | Execute allowed ensemble families. |
| P283_REGIME_BUCKETS | P282_TIME_OPEN_BUCKET;P282_TIME_LATER_BUCKET;P282_SPREAD_COMPRESSED_BUCKET;P282_DEPTH_STABLE_BUCKET | Evaluate regime/time/spread/depth buckets. |
| P283_SEARCH_TYPE | regime_conditioned_full_depth_ensemble_search | Execute the next search milestone. |
| P283_BOUNDARY | no_paper_live;no_deployable_profitability_claim;cost200_required;fixed_capital_required;full_depth_required;l1_only_forbidden;net_edge_live_mask_forbidden | Boundaries remain closed. |

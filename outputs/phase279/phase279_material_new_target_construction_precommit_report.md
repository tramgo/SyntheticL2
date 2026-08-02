# Phase279 Material New Target-construction Precommit

Generated UTC: 2026-08-02T06:57:01.052956+00:00

Phase279 precommits materially different target construction after Phase278 closed the filter-redesign route for acceptance.
The next executable search must retain cost200, full-depth L2, and no paper/live boundaries.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase279_target_construction_precommit_complete | 1 | Phase279 material new target-construction precommit completed |
| phase279_selected_route | P279_MATERIAL_NEW_TARGET_CONSTRUCTION_PRECOMMIT | Selected route |
| phase279_target_family_rows | 5 | Target families defined |
| phase279_phase280_allowed_target_family_rows | 5 | Target families allowed for Phase280 search |
| phase279_preserved_clue_rows | 5 | Preserved Phase277 clue rows |
| phase279_phase280_anchor_clue_rows | 5 | Clues eligible as Phase280 anchors |
| phase279_cost200_required | 1 | Cost200 required |
| phase279_full_depth_required | 1 | Full top-five and levels 2-5 required |
| phase279_l1_only_allowed | 0 | L1-only targets forbidden |
| phase279_strategy_replay_allowed | 0 | No strategy replay unlocked |
| phase279_strategy_promotion_allowed | 0 | No strategy promotion unlocked |
| phase279_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance |
| phase279_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase279_hard_gate_pass_rows | 9 | Hard gates passed |
| phase279_hard_gate_rows | 9 | Hard gates evaluated |
| phase279_next_best_action | run_phase280_material_new_target_construction_search_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P279_PHASE278_WORK_ORDER_PRESENT | True | run_phase279_material_new_target_construction_precommit_no_paper_live | Phase278 next action targets Phase279 | hard |
| P279_PHASE278_INTERPRETATION_COMPLETE | True | 1 | Phase278 complete | hard |
| P279_FILTER_ROUTE_CLOSED | True | close_filter=1;do_not_relax=1 | filter route closed and cost threshold preserved | hard |
| P279_ROUTE_CONTRACT_PRESENT | True | 5 | Phase279 route contract present | hard |
| P279_TARGET_FAMILIES_PRESENT | True | targets=5;allowed=5 | >=5 target families and >=4 allowed | hard |
| P279_PRESERVED_CLUES_PRESENT | True | 5 | >0 preserved full-depth clues | hard |
| P279_FULL_DEPTH_AND_L1_BOUNDARY | True | full_depth=True;l1_forbidden=True | full-depth required and L1-only forbidden | hard |
| P279_CONTROLS_PRESENT | True | 6 | control contract present | hard |
| P279_NEXT_ROUTE_SELECTED | True | P280 material target search | Phase280 route selected | hard |

## Preserved Clue Catalog

| phase277_variant_id | redesign_family | feature_rule | max_annualized_pct | median_annualized_pct | cost200_above12_scenario_rows | uses_top5 | uses_levels_2_to_5 | l1_only_variant | preserve_as_clue_not_acceptance | eligible_for_phase280_anchor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P277_REPLENISH_WITHDRAW_GE_Q90 | depth_replenishment_withdrawal | depth_replenish_withdraw_ratio >= 12.933958 | 9.37048 | 4.14152 | 0 | 0 | 1 | 0 | 1 | 1 |
| P277_SPREAD_LE_Q80 | spread_regime | avg_spread_bps <= 2.559387 | 9.37048 | 4.14152 | 0 | 0 | 0 | 0 | 1 | 1 |
| P277_REPLENISH_CHURN_Q70 | replenishment_churn_filter | depth_replenish_withdraw_ratio >= 8.417774 and top5_churn_pressure <= 342736.393969 | 7.72063 | 6.89571 | 0 | 1 | 1 | 0 | 1 | 1 |
| P277_CHURN_LE_Q60 | event_sparsity | top5_churn_pressure <= 445889.435425 | 6.91175 | 4.72638 | 0 | 1 | 0 | 0 | 1 | 1 |
| P277_CHURN_LE_Q80 | event_sparsity | top5_churn_pressure <= 71224.830695 | 6.08829 | 6.07953 | 0 | 1 | 0 | 0 | 1 | 1 |

## Target Family Catalog

| target_family_id | target_family | target_definition | primary_features | preserved_clue_dependency | matched_preserved_clue_rows | matched_preserved_clues | cost_profile_required | full_depth_required | levels_2_to_5_required | l1_only_allowed | event_universe_rows | phase280_search_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P279_SPREAD_COST_MARGIN_TARGET | spread_cost_margin | classify events where observable spread and full-depth pressure imply enough gross edge margin to survive cost200 | avg_spread_bps;avg_cum_top5_qty_imbalance;avg_depth_beyond_l1_qty_imbalance;avg_level_weighted_depth_imbalance | P277_SPREAD_LE_Q80;P277_REPLENISH_WITHDRAW_GE_Q90 | 2 | P277_SPREAD_LE_Q80;P277_REPLENISH_WITHDRAW_GE_Q90 | cost200 | 1 | 1 | 0 | 1280 | 1 |
| P279_ADVERSE_SELECTION_AVOIDANCE_TARGET | adverse_selection_avoidance | filter events likely to avoid immediate adverse selection after entry using churn and depth withdrawal pressure | top5_churn_pressure;depth_withdrawal_pressure;depth_replenishment_pressure;avg_depth_beyond_l1_qty_imbalance | P277_CHURN_LE_Q60;P277_CHURN_LE_Q80 | 2 | P277_CHURN_LE_Q60;P277_CHURN_LE_Q80 | cost200 | 1 | 1 | 0 | 1280 | 1 |
| P279_REPLENISHMENT_CONFIRMATION_TARGET | depth_replenishment_confirmation | require replenishment dominance to persist as confirmation rather than a one-bar filter | depth_replenish_withdraw_ratio;depth_replenishment_pressure;avg_level_weighted_depth_imbalance | P277_REPLENISH_WITHDRAW_GE_Q90;P277_REPLENISH_CHURN_Q70 | 2 | P277_REPLENISH_WITHDRAW_GE_Q90;P277_REPLENISH_CHURN_Q70 | cost200 | 1 | 1 | 0 | 1280 | 1 |
| P279_TIME_TO_EXIT_TARGET | time_to_exit | vary event exit target and holding horizon to test if the edge exists at a different exit time rather than only at the current horizon | horizon;richer_event_bar_id;avg_spread_bps;depth_replenish_withdraw_ratio | P277_REPLENISH_WITHDRAW_GE_Q90 | 1 | P277_REPLENISH_WITHDRAW_GE_Q90 | cost200 | 1 | 1 | 0 | 1280 | 1 |
| P279_NET_EDGE_DISTRIBUTION_SHIFT_TARGET | net_edge_distribution_shift | evaluate target construction that improves the distribution tail of net edge under cost200 without using net edge as a live selection feature | full_depth_features_for_selection;net_edge_bps_for_offline_label_only | P277_REPLENISH_WITHDRAW_GE_Q90;P277_SPREAD_LE_Q80;P277_REPLENISH_CHURN_Q70 | 3 | P277_REPLENISH_WITHDRAW_GE_Q90;P277_SPREAD_LE_Q80;P277_REPLENISH_CHURN_Q70 | cost200 | 1 | 1 | 0 | 1280 | 1 |

## Control Contract

| control_id | control_value | severity |
| --- | --- | --- |
| P279_NO_LABEL_LEAKAGE | net_edge_bps and gross_edge_bps may define offline labels only, not live selection masks | hard |
| P279_COST200_REQUIRED | all Phase280 scoring must include cost200 or stronger stress | hard |
| P279_FULL_DEPTH_REQUIRED | top-five rows 1-5 and levels 2-5 materiality required | hard |
| P279_L1_ONLY_FORBIDDEN | L1-only target families and variants forbidden | hard |
| P279_NO_PROMOTION | no strategy replay, promotion, paper/live, or deployable profitability claim | hard |
| P279_ACCEPTANCE_THRESHOLD | diagnostic acceptance remains annualized > 12 percent under cost200 with stability evidence | hard |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P280_INPUT | outputs/phase277/phase277_cost200_redesign_event_universe.csv;outputs/phase279/phase279_target_family_catalog.csv | Use cost200 event universe and Phase279 target contract. |
| P280_TARGET_FAMILIES | P279_SPREAD_COST_MARGIN_TARGET;P279_ADVERSE_SELECTION_AVOIDANCE_TARGET;P279_REPLENISHMENT_CONFIRMATION_TARGET;P279_TIME_TO_EXIT_TARGET;P279_NET_EDGE_DISTRIBUTION_SHIFT_TARGET | Execute materially new target-construction families. |
| P280_ANCHOR_CLUES | P277_REPLENISH_WITHDRAW_GE_Q90;P277_SPREAD_LE_Q80;P277_REPLENISH_CHURN_Q70;P277_CHURN_LE_Q60;P277_CHURN_LE_Q80 | Use preserved full-depth clues as anchors, not accepted strategies. |
| P280_SEARCH_TYPE | material_new_target_construction_search | Execute target-construction search next. |
| P280_BOUNDARY | no_paper_live;no_deployable_profitability_claim;cost200_required;full_depth_required;l1_only_forbidden | Boundaries remain closed. |

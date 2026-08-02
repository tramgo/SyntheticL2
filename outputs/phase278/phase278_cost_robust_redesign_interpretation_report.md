# Phase278 Cost-robust Redesign Interpretation

Generated UTC: 2026-08-02T06:51:00.400609+00:00

Phase278 interprets the Phase277 cost-robust full-depth redesign search.
It closes the current filter-redesign route for acceptance and selects a materially new target-construction precommit.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase278_interpretation_complete | 1 | Phase278 cost-robust redesign interpretation completed |
| phase278_selected_next_route | P278_MATERIAL_NEW_TARGET_CONSTRUCTION_PRECOMMIT | Selected next route |
| phase278_phase277_variant_rows | 47 | Phase277 variants interpreted |
| phase278_phase277_scenario_rows | 282 | Phase277 scenarios interpreted |
| phase278_phase277_cost200_above12_scenario_rows | 0 | Phase277 cost200 above-12 rows |
| phase278_phase277_best_cost200_annualized_pct | 9.370481974163102 | Best Phase277 cost200 annualized diagnostic |
| phase278_material_clue_variant_rows | 25 | Full-depth material clue rows |
| phase278_close_filter_redesign_for_acceptance | 1 | Close Phase277 filter redesign for acceptance |
| phase278_best_preserved_clue_variant | P277_REPLENISH_WITHDRAW_GE_Q90 | Best preserved clue variant |
| phase278_best_preserved_clue_family | depth_replenishment_withdrawal | Best preserved clue family |
| phase278_do_not_relax_cost_threshold | 1 | Keep cost200 threshold |
| phase278_strategy_replay_allowed | 0 | No strategy replay unlocked |
| phase278_strategy_promotion_allowed | 0 | No strategy promotion unlocked |
| phase278_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance |
| phase278_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase278_hard_gate_pass_rows | 7 | Hard gates passed |
| phase278_hard_gate_rows | 7 | Hard gates evaluated |
| phase278_next_best_action | run_phase279_material_new_target_construction_precommit_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P278_PHASE277_WORK_ORDER_PRESENT | True | run_phase278_cost_robust_redesign_interpretation_no_paper_live | Phase277 next action targets Phase278 | hard |
| P278_PHASE277_SEARCH_COMPLETE | True | 1 | Phase277 complete | hard |
| P278_PHASE277_HARD_GATES_PASS | True | 9/9 | Phase277 hard gates pass | hard |
| P278_RESULTS_PRESENT | True | 47 | Phase277 variants interpreted | hard |
| P278_OUTCOME_CLASSIFIED_AS_NO_COST200_SURVIVOR | True | cost200_above12=0;best_ann=9.370481974163102 | no accepted cost200 survivor | hard |
| P278_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |
| P278_NEXT_ROUTE_SELECTED | True | P278_MATERIAL_NEW_TARGET_CONSTRUCTION_PRECOMMIT | Phase279 material target construction selected | hard |

## Ranked Cost-robust Redesign Interpretation

| phase277_variant_id | redesign_family | feature_rule | scenario_rows | selected_event_rows | cost200_above12_scenario_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | min_net_pnl_inr | best_scenario_id | best_initial_capital_inr | best_fixed_notional_inr | best_max_concurrent_positions | best_scheduled_event_rows | uses_top5 | uses_levels_2_to_5 | l1_only_variant | near_miss_under_12 | material_clue | close_for_acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P277_REPLENISH_WITHDRAW_GE_Q90 | depth_replenishment_withdrawal | depth_replenish_withdraw_ratio >= 12.933958 | 6 | 128 | 0 | 3.5978 | 4.14152 | 9.37048 | 297.476 | 114.216 | P271_P277_REPLENISH_WITHDRAW_GE_Q90_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 2 | 0 | 1 | 0 | 1 | 1 | 1 |
| P277_SPREAD_LE_Q80 | spread_regime | avg_spread_bps <= 2.559387 | 6 | 276 | 0 | 3.5978 | 4.14152 | 9.37048 | 297.476 | 114.216 | P271_P277_SPREAD_LE_Q80_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 2 | 0 | 0 | 0 | 1 | 1 | 1 |
| P277_REPLENISH_CHURN_Q70 | replenishment_churn_filter | depth_replenish_withdraw_ratio >= 8.417774 and top5_churn_pressure <= 342736.393969 | 6 | 234 | 0 | 3.03539 | 6.89571 | 7.72063 | 245.099 | 96.3616 | P271_P277_REPLENISH_CHURN_Q70_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 3 | 1 | 1 | 0 | 1 | 1 | 1 |
| P277_CHURN_LE_Q60 | event_sparsity | top5_churn_pressure <= 445889.435425 | 6 | 512 | 0 | 1.27051 | 4.72638 | 6.91175 | 219.421 | 40.3336 | P271_P277_CHURN_LE_Q60_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 4 | 1 | 0 | 0 | 1 | 1 | 1 |
| P277_CHURN_LE_Q80 | event_sparsity | top5_churn_pressure <= 71224.830695 | 6 | 256 | 0 | 3.03539 | 6.07953 | 6.08829 | 193.279 | 96.3616 | P271_P277_CHURN_LE_Q80_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 4 | 1 | 0 | 0 | 1 | 1 | 1 |
| P277_REPLENISH_CHURN_Q80 | replenishment_churn_filter | depth_replenish_withdraw_ratio >= 10.699868 and top5_churn_pressure <= 71224.830695 | 6 | 138 | 0 | 3.03539 | 6.07953 | 6.08829 | 193.279 | 96.3616 | P271_P277_REPLENISH_CHURN_Q80_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 4 | 1 | 1 | 0 | 1 | 1 | 1 |
| P277_SPARSITY_PRESSURE_LE_Q80 | spread_and_churn_sparsity | event_sparsity_pressure <= 250903.160053 | 6 | 256 | 0 | 3.03539 | 6.07953 | 6.08829 | 193.279 | 96.3616 | P271_P277_SPARSITY_PRESSURE_LE_Q80_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 4 | 1 | 0 | 0 | 1 | 1 | 1 |
| P277_SPARSITY_PRESSURE_LE_Q90 | spread_and_churn_sparsity | event_sparsity_pressure <= 166225.822836 | 6 | 128 | 0 | 2.74058 | 3.75212 | 5.48115 | 174.005 | 87.0024 | P271_P277_SPARSITY_PRESSURE_LE_Q90_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 3 | 1 | 0 | 0 | 1 | 1 | 1 |
| P277_REPLENISH_CHURN_Q60 | replenishment_churn_filter | depth_replenish_withdraw_ratio >= 5.629741 and top5_churn_pressure <= 445889.435425 | 6 | 367 | 0 | 2.11938 | 4.81496 | 5.39114 | 171.147 | 67.282 | P271_P277_REPLENISH_CHURN_Q60_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 3 | 1 | 1 | 0 | 1 | 1 | 1 |
| P277_WEIGHTED_DEPTH_GE_Q90 | levels_2_to_5_depth | avg_level_weighted_depth_imbalance >= 0.670035 | 6 | 128 | 0 | -1.0455 | 0.675588 | 4.79335 | 152.17 | -33.1904 | P271_P277_WEIGHTED_DEPTH_GE_Q90_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 3 | 0 | 1 | 0 | 1 | 1 | 1 |
| P277_REPLENISH_WITHDRAW_GE_Q70 | depth_replenishment_withdrawal | depth_replenish_withdraw_ratio >= 8.417774 | 6 | 384 | 0 | -0.378428 | 2.15341 | 4.49603 | 142.731 | -12.0136 | P271_P277_REPLENISH_WITHDRAW_GE_Q70_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 3 | 0 | 1 | 0 | 1 | 1 | 1 |
| P277_REPLENISH_WITHDRAW_GE_Q80 | depth_replenishment_withdrawal | depth_replenish_withdraw_ratio >= 10.699868 | 6 | 256 | 0 | -0.378428 | 2.15341 | 4.49603 | 142.731 | -12.0136 | P271_P277_REPLENISH_WITHDRAW_GE_Q80_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 3 | 0 | 1 | 0 | 1 | 1 | 1 |
| P277_SPARSITY_PRESSURE_LE_Q70 | spread_and_churn_sparsity | event_sparsity_pressure <= 825012.273327 | 6 | 384 | 0 | -0.378428 | 2.15341 | 4.49603 | 142.731 | -12.0136 | P271_P277_SPARSITY_PRESSURE_LE_Q70_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 3 | 1 | 0 | 0 | 1 | 1 | 1 |
| P277_SPREAD_LE_Q70 | spread_regime | avg_spread_bps <= 3.515855 | 6 | 400 | 0 | -0.378428 | 2.15341 | 4.49603 | 142.731 | -12.0136 | P271_P277_SPREAD_LE_Q70_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 3 | 0 | 0 | 0 | 1 | 1 | 1 |
| P277_SPARSITY_PRESSURE_LE_Q60 | spread_and_churn_sparsity | event_sparsity_pressure <= 1470251.984942 | 6 | 512 | 0 | 1.23132 | 1.67535 | 4.23877 | 134.564 | 39.0897 | P271_P277_SPARSITY_PRESSURE_LE_Q60_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 3 | 1 | 0 | 0 | 1 | 1 | 1 |
| P277_SPREAD_LE_Q60 | spread_regime | avg_spread_bps <= 4.195193 | 6 | 527 | 0 | 1.23132 | 1.67535 | 4.23877 | 134.564 | 39.0897 | P271_P277_SPREAD_LE_Q60_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 3 | 0 | 0 | 0 | 1 | 1 | 1 |
| P277_CHURN_LE_Q70 | event_sparsity | top5_churn_pressure <= 342736.393969 | 6 | 384 | 0 | -1.1234 | 0.49799 | 4.23877 | 134.564 | -35.6636 | P271_P277_CHURN_LE_Q70_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 3 | 1 | 0 | 0 | 1 | 1 | 1 |
| P277_BEYOND_L1_IMBALANCE_GE_Q90 | levels_2_to_5_depth | avg_depth_beyond_l1_qty_imbalance >= 0.671965 | 6 | 128 | 0 | 2.06712 | 2.40897 | 4.13424 | 131.246 | 65.6229 | P271_P277_BEYOND_L1_IMBALANCE_GE_Q90_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 3 | 0 | 1 | 0 | 1 | 1 | 1 |
| P277_CHURN_LE_Q50 | event_sparsity | top5_churn_pressure <= 610494.118466 | 6 | 640 | 0 | 1.38535 | 1.47996 | 3.14913 | 99.9725 | 43.9795 | P271_P277_CHURN_LE_Q50_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 4 | 1 | 0 | 0 | 1 | 1 | 1 |
| P277_SPREAD_LE_Q50 | spread_regime | avg_spread_bps <= 4.915814 | 6 | 677 | 0 | 1.38535 | 1.47996 | 3.14913 | 99.9725 | 43.9795 | P271_P277_SPREAD_LE_Q50_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 4 | 0 | 0 | 0 | 1 | 1 | 1 |

## Interpretation Ledger

| finding_id | evidence | severity | finding_present | interpretation |
| --- | --- | --- | --- | --- |
| cost_robust_redesign_executed | variants=47;scenarios=282 | evidence | 1 | Phase277 executed the intended redesign search. |
| cost200_acceptance_failed | cost200_above12=0;best_ann=9.370481974163102 | hard_negative | 1 | No cost200 redesign cleared the >12% diagnostic threshold. |
| best_filter_is_near_miss_not_survivor | best_ann=9.370481974163102;threshold=12.0 | risk | 1 | The best replenishment/withdrawal clue is useful but below acceptance. |
| full_depth_boundary_preserved | l1_only=0;material_clues=25 | constraint | 1 | No L1-only fallback occurred; full-depth evidence remains central. |
| same_filter_family_should_close_for_acceptance | cost200_median_above12=0;cost200_worst_case_above12=0 | decision | 1 | Do not keep iterating the same filter family for acceptance. |
| next_route_should_change_target_construction | P278_MATERIAL_NEW_TARGET_CONSTRUCTION_PRECOMMIT | next_action | 1 | Move to materially different target construction rather than relaxing cost stress. |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| close_phase277_filter_redesign_for_acceptance | 1 | cost200_above12=0;best_ann=9.370481974163102 | Do not promote or continue this same filter route as accepted. |
| preserve_replenishment_withdrawal_clue | 1 | top_variant=P277_REPLENISH_WITHDRAW_GE_Q90;max_ann=9.370481974163102 | Keep the best full-depth clue for future feature construction. |
| do_not_relax_cost_threshold | 1 | cost200_required;threshold=12 | Do not downgrade acceptance to cost100 or below-12 cost200. |
| selected_next_route | P278_MATERIAL_NEW_TARGET_CONSTRUCTION_PRECOMMIT | filter redesign exhausted without cost200 survivor | Precommit a materially new target construction. |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P279_INPUT | outputs/phase277/phase277_cost_robust_redesign_variant_summary.csv;outputs/phase277/phase277_cost200_redesign_event_universe.csv | Use Phase277 redesign evidence and event universe. |
| P279_PRESERVED_CLUES | P277_REPLENISH_WITHDRAW_GE_Q90;P277_SPREAD_LE_Q80;P277_REPLENISH_CHURN_Q70;P277_CHURN_LE_Q60;P277_CHURN_LE_Q80 | Preserve useful full-depth near-miss clues without accepting them. |
| P279_TARGET_CHANGE | event_target_construction_not_filter_relaxation | Change target construction rather than only tuning filters. |
| P279_REQUIRED_DIRECTIONS | net_edge_distribution_shift;time_to_exit;adverse_selection_avoidance;depth_replenishment_confirmation;spread_cost_margin | Explore materially different labels/targets around cost robustness. |
| P279_BOUNDARY | no_paper_live;no_deployable_profitability_claim;full_depth_required;l1_only_forbidden | Boundaries remain closed. |

# Phase281 Material Target-construction Interpretation

Generated UTC: 2026-08-02T07:16:35.201127+00:00

Phase281 interprets the Phase280 material target-construction search.
It preserves the full-depth near-miss clue, closes the route for acceptance, and selects a broader regime-conditioned ensemble precommit.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase281_interpretation_complete | 1 | Phase281 material target-construction interpretation completed |
| phase281_selected_next_route | P281_REGIME_CONDITIONED_FULL_DEPTH_ENSEMBLE_PRECOMMIT | Selected next route |
| phase281_phase280_target_family_rows | 5 | Phase280 target families interpreted |
| phase281_phase280_variant_rows | 24 | Phase280 variants interpreted |
| phase281_phase280_scenario_rows | 144 | Phase280 scenarios interpreted |
| phase281_phase280_cost200_above12_scenario_rows | 0 | Phase280 cost200 above-12 rows |
| phase281_phase280_best_cost200_annualized_pct | 11.28247573982665 | Best Phase280 cost200 annualized diagnostic |
| phase281_phase280_best_scheduled_event_rows | 2 | Best Phase280 scheduled events |
| phase281_material_clue_variant_rows | 19 | Full-depth material clue rows |
| phase281_near_miss_variant_rows | 19 | Near-miss variants below 12% |
| phase281_close_phase280_for_acceptance | 1 | Close Phase280 target construction for acceptance |
| phase281_best_preserved_clue_variant | P280_SPREAD_REPLENISH_COMBO_Q70 | Best preserved clue variant |
| phase281_best_preserved_clue_family | spread_cost_margin | Best preserved clue family |
| phase281_do_not_relax_cost_threshold | 1 | Keep cost200 threshold |
| phase281_do_not_claim_portfolio_return | 1 | Sparse diagnostic is not a robust annual portfolio claim |
| phase281_strategy_replay_allowed | 0 | No strategy replay unlocked |
| phase281_strategy_promotion_allowed | 0 | No strategy promotion unlocked |
| phase281_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance |
| phase281_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase281_hard_gate_pass_rows | 8 | Hard gates passed |
| phase281_hard_gate_rows | 8 | Hard gates evaluated |
| phase281_next_best_action | run_phase282_regime_conditioned_full_depth_ensemble_precommit_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P281_PHASE280_WORK_ORDER_PRESENT | True | run_phase281_material_new_target_construction_interpretation_no_paper_live | Phase280 next action targets Phase281 | hard |
| P281_PHASE280_SEARCH_COMPLETE | True | 1 | Phase280 complete | hard |
| P281_PHASE280_HARD_GATES_PASS | True | 9/9 | Phase280 hard gates pass | hard |
| P281_RESULTS_PRESENT | True | 24 | Phase280 variants interpreted | hard |
| P281_OUTCOME_CLASSIFIED_AS_NO_COST200_SURVIVOR | True | cost200_above12=0;best_ann=11.28247573982665 | no accepted cost200 survivor | hard |
| P281_FULL_DEPTH_BOUNDARY_PRESERVED | True | l1_only=0;live_leakage=0 | full-depth/no-leakage preserved | hard |
| P281_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |
| P281_NEXT_ROUTE_SELECTED | True | P281_REGIME_CONDITIONED_FULL_DEPTH_ENSEMBLE_PRECOMMIT | Phase282 ensemble precommit selected | hard |

## Ranked Variant Interpretation

| phase280_variant_id | target_family_id | target_family | target_rule | scenario_rows | selected_event_rows | max_scheduled_event_rows | cost200_above12_scenario_rows | max_annualized_pct | median_annualized_pct | min_annualized_pct | max_net_pnl_inr | best_scenario_id | best_initial_capital_inr | best_fixed_notional_inr | best_max_concurrent_positions | uses_top5 | uses_levels_2_to_5 | l1_only_variant | uses_net_edge_as_offline_label | uses_net_edge_as_live_mask | near_miss_under_12 | too_sparse_for_portfolio_claim | material_full_depth_clue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P280_SPREAD_REPLENISH_COMBO_Q70 | P279_SPREAD_COST_MARGIN_TARGET | spread_cost_margin | avg_spread_bps <= q30 and depth_replenish_withdraw_ratio >= q70 and avg_depth_beyond_l1_qty_imbalance >= q60 | 6 | 67 | 3 | 0 | 11.2825 | 5.05313 | 4.46503 | 358.174 | P271_P280_SPREAD_REPLENISH_COMBO_Q70_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_TIME_TO_EXIT_SHORT_HQ90 | P279_TIME_TO_EXIT_TARGET | time_to_exit | horizon <= 10 and depth_replenish_withdraw_ratio >= 12.933958 | 6 | 128 | 2 | 0 | 9.37048 | 4.14152 | 3.5978 | 297.476 | P271_P280_TIME_TO_EXIT_SHORT_HQ90_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_ADVERSE_SELECTION_AVOID_Q60 | P279_ADVERSE_SELECTION_AVOIDANCE_TARGET | adverse_selection_avoidance | top5_churn_pressure <= 445889.435425 and depth_withdrawal_pressure <= 10300.394075 | 6 | 430 | 4 | 0 | 7.56387 | 5.90132 | 2.11938 | 240.123 | P271_P280_ADVERSE_SELECTION_AVOID_Q60_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_ADVERSE_SELECTION_AVOID_Q80 | P279_ADVERSE_SELECTION_AVOIDANCE_TARGET | adverse_selection_avoidance | top5_churn_pressure <= 71224.830695 and depth_withdrawal_pressure <= 1231.635970 | 6 | 230 | 4 | 0 | 6.08829 | 6.07953 | 3.03539 | 193.279 | P271_P280_ADVERSE_SELECTION_AVOID_Q80_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_REPLENISH_CONFIRM_Q50 | P279_REPLENISHMENT_CONFIRMATION_TARGET | depth_replenishment_confirmation | depth_replenish_withdraw_ratio >= 5.126904 and avg_level_weighted_depth_imbalance >= 0.557013 | 6 | 190 | 5 | 0 | 5.16974 | 3.24487 | 0.659998 | 164.119 | P271_P280_REPLENISH_CONFIRM_Q50_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_TIME_TO_EXIT_SHORT_HQ70 | P279_TIME_TO_EXIT_TARGET | time_to_exit | horizon <= 10 and depth_replenish_withdraw_ratio >= 8.417774 | 6 | 384 | 3 | 0 | 4.49603 | 2.15341 | -0.378428 | 142.731 | P271_P280_TIME_TO_EXIT_SHORT_HQ70_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_TIME_TO_EXIT_SHORT_HQ80 | P279_TIME_TO_EXIT_TARGET | time_to_exit | horizon <= 10 and depth_replenish_withdraw_ratio >= 10.699868 | 6 | 256 | 3 | 0 | 4.49603 | 2.15341 | -0.378428 | 142.731 | P271_P280_TIME_TO_EXIT_SHORT_HQ80_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | P279_NET_EDGE_DISTRIBUTION_SHIFT_TARGET | net_edge_distribution_shift | offline net-edge-positive label AND depth_consensus_imbalance >= 0.590831 and event_sparsity_pressure <= 1470251.984942 | 6 | 47 | 2 | 0 | 4.27432 | 4.17851 | 2.13716 | 135.693 | P271_P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 1 |
| P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q70 | P279_NET_EDGE_DISTRIBUTION_SHIFT_TARGET | net_edge_distribution_shift | offline net-edge-positive label AND depth_consensus_imbalance >= 0.603199 and event_sparsity_pressure <= 825012.273327 | 6 | 47 | 2 | 0 | 4.27432 | 4.17851 | 2.13716 | 135.693 | P271_P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q70_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 1 |
| P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q80 | P279_NET_EDGE_DISTRIBUTION_SHIFT_TARGET | net_edge_distribution_shift | offline net-edge-positive label AND depth_consensus_imbalance >= 0.616025 and event_sparsity_pressure <= 250903.160053 | 6 | 31 | 2 | 0 | 4.27432 | 4.17851 | 2.13716 | 135.693 | P271_P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q80_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 1 |
| P280_REPLENISH_CONFIRM_Q70 | P279_REPLENISHMENT_CONFIRMATION_TARGET | depth_replenishment_confirmation | depth_replenish_withdraw_ratio >= 8.417774 and avg_level_weighted_depth_imbalance >= 0.607609 | 6 | 58 | 2 | 0 | 4.27432 | 4.17851 | 2.13716 | 135.693 | P271_P280_REPLENISH_CONFIRM_Q70_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_REPLENISH_CONFIRM_Q80 | P279_REPLENISHMENT_CONFIRMATION_TARGET | depth_replenishment_confirmation | depth_replenish_withdraw_ratio >= 10.699868 and avg_level_weighted_depth_imbalance >= 0.634034 | 6 | 58 | 2 | 0 | 4.27432 | 4.17851 | 2.13716 | 135.693 | P271_P280_REPLENISH_CONFIRM_Q80_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_ADVERSE_SELECTION_AVOID_Q70 | P279_ADVERSE_SELECTION_AVOIDANCE_TARGET | adverse_selection_avoidance | top5_churn_pressure <= 342736.393969 and depth_withdrawal_pressure <= 6712.574807 | 6 | 296 | 3 | 0 | 4.23877 | 2.86822 | 2.11938 | 134.564 | P271_P280_ADVERSE_SELECTION_AVOID_Q70_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q50 | P279_NET_EDGE_DISTRIBUTION_SHIFT_TARGET | net_edge_distribution_shift | offline net-edge-positive label AND depth_consensus_imbalance >= 0.575120 and event_sparsity_pressure <= 2187162.832698 | 6 | 61 | 3 | 0 | 4.23606 | 4.14603 | 2.028 | 134.478 | P271_P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q50_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 1 |
| P280_REPLENISH_CONFIRM_Q60 | P279_REPLENISHMENT_CONFIRMATION_TARGET | depth_replenishment_confirmation | depth_replenish_withdraw_ratio >= 5.629741 and avg_level_weighted_depth_imbalance >= 0.582283 | 6 | 83 | 4 | 0 | 2.88694 | 2.4373 | 0.993832 | 91.6488 | P271_P280_REPLENISH_CONFIRM_Q60_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_TIME_TO_EXIT_SHORT_HQ50 | P279_TIME_TO_EXIT_TARGET | time_to_exit | horizon <= 10 and depth_replenish_withdraw_ratio >= 5.126904 | 6 | 640 | 4 | 0 | 2.80107 | 2.67105 | 1.27051 | 88.923 | P271_P280_TIME_TO_EXIT_SHORT_HQ50_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_ADVERSE_SELECTION_AVOID_Q50 | P279_ADVERSE_SELECTION_AVOIDANCE_TARGET | adverse_selection_avoidance | top5_churn_pressure <= 610494.118466 and depth_withdrawal_pressure <= 13616.795344 | 6 | 555 | 4 | 0 | 2.54102 | 1.1759 | 1.0813 | 80.6673 | P271_P280_ADVERSE_SELECTION_AVOID_Q50_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_REPLENISH_CONFIRM_Q90 | P279_REPLENISHMENT_CONFIRMATION_TARGET | depth_replenishment_confirmation | depth_replenish_withdraw_ratio >= 12.933958 and avg_level_weighted_depth_imbalance >= 0.670035 | 6 | 23 | 2 | 0 | 2.22481 | 1.44097 | 0.328571 | 70.6288 | P271_P280_REPLENISH_CONFIRM_Q90_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_TIME_TO_EXIT_SHORT_HQ60 | P279_TIME_TO_EXIT_TARGET | time_to_exit | horizon <= 10 and depth_replenish_withdraw_ratio >= 5.629741 | 6 | 512 | 4 | 0 | 0.549313 | 0.18005 | 0.0854428 | 17.4385 | P271_P280_TIME_TO_EXIT_SHORT_HQ60_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| P280_SPREAD_COST_MARGIN_Q50 | P279_SPREAD_COST_MARGIN_TARGET | spread_cost_margin | avg_spread_bps <= 4.915814 and depth_consensus_imbalance >= 0.575120 | 6 | 204 | 3 | 0 | -1.15098 | -2.21956 | -6.57629 | -36.5391 | P271_P280_SPREAD_COST_MARGIN_Q50_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |

## Family Interpretation

| target_family_id | target_family | variant_rows | scenario_rows | cost200_above12_scenario_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | max_scheduled_event_rows | material_clue_variants | near_miss_variants | close_family_for_acceptance | preserve_for_ensemble_search |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P279_SPREAD_COST_MARGIN_TARGET | spread_cost_margin | 6 | 36 | 0 | -55.0747 | -4.18719 | 11.2825 | 358.174 | 3 | 1 | 1 | 1 | 1 |
| P279_TIME_TO_EXIT_TARGET | time_to_exit | 5 | 30 | 0 | -0.378428 | 2.67105 | 9.37048 | 297.476 | 4 | 5 | 5 | 1 | 1 |
| P279_ADVERSE_SELECTION_AVOIDANCE_TARGET | adverse_selection_avoidance | 4 | 24 | 0 | 1.0813 | 3.10723 | 7.56387 | 240.123 | 4 | 4 | 4 | 1 | 1 |
| P279_REPLENISHMENT_CONFIRMATION_TARGET | depth_replenishment_confirmation | 5 | 30 | 0 | 0.328571 | 2.88694 | 5.16974 | 164.119 | 5 | 5 | 5 | 1 | 1 |
| P279_NET_EDGE_DISTRIBUTION_SHIFT_TARGET | net_edge_distribution_shift | 4 | 24 | 0 | 2.028 | 4.17851 | 4.27432 | 135.693 | 3 | 4 | 4 | 1 | 1 |

## Interpretation Ledger

| finding_id | evidence | severity | finding_present | interpretation |
| --- | --- | --- | --- | --- |
| phase280_executed | scenario_rows=144 | evidence | 1 | Phase280 executed the target-construction search. |
| cost200_acceptance_failed | cost200_above12=0;best_ann=11.28247573982665 | hard_negative | 1 | No Phase280 target crossed the >12% cost200 diagnostic threshold. |
| near_miss_is_too_sparse | best_ann=11.28247573982665;best_scheduled_events=2 | risk | 1 | The top clue is close but too sparse for a robust portfolio-return claim. |
| full_depth_boundary_preserved | l1_only=0;live_label_leakage=0 | constraint | 1 | Full-depth and no-live-leakage constraints held. |
| material_clues_exist | material_clue_variants=19 | evidence | 1 | Preserve useful L2 clues for a broader ensemble search. |
| same_target_construction_should_close_for_acceptance | all_families_cost200_above12=0 | decision | 1 | Do not keep iterating the same Phase280 target masks for acceptance. |
| next_route_broadens_search_not_thresholds | P281_REGIME_CONDITIONED_FULL_DEPTH_ENSEMBLE_PRECOMMIT | next_action | 1 | Move to regime-conditioned full-depth ensembles instead of relaxing cost stress. |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| close_phase280_target_construction_for_acceptance | 1 | cost200_above12=0;best_ann=11.28247573982665 | Do not accept or promote Phase280 target construction. |
| preserve_best_near_miss_full_depth_clue | P280_SPREAD_REPLENISH_COMBO_Q70 | family=spread_cost_margin;best_ann=11.28247573982665;scheduled_events=2 | Keep the top full-depth clue as an ensemble seed. |
| do_not_relax_cost_threshold | 1 | cost200_required;threshold=12 | Do not downgrade acceptance to cost100 or below-12 cost200. |
| do_not_claim_portfolio_return | 1 | best_scheduled_events=2;min_required=30 | Sparse diagnostic is not a robust annual portfolio claim. |
| selected_next_route | P281_REGIME_CONDITIONED_FULL_DEPTH_ENSEMBLE_PRECOMMIT | target construction near-miss without survivor | Precommit a regime-conditioned full-depth ensemble search. |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P282_INPUTS | outputs/phase280/phase280_material_target_scenario_results.csv;outputs/phase280/phase280_sample_material_target_scheduled_event_ledger.csv | Use Phase280 scenarios and scheduled-event evidence. |
| P282_PRESERVED_CLUES | P280_SPREAD_REPLENISH_COMBO_Q70;P280_TIME_TO_EXIT_SHORT_HQ90;P280_ADVERSE_SELECTION_AVOID_Q60;P280_ADVERSE_SELECTION_AVOID_Q80;P280_REPLENISH_CONFIRM_Q50;P280_TIME_TO_EXIT_SHORT_HQ70;P280_TIME_TO_EXIT_SHORT_HQ80;P280_NET_EDGE_SHIFT_LABEL_ANCHORED_Q60 | Seed ensemble search with positive full-depth near-miss clues only as clues. |
| P282_PRESERVED_FAMILIES | P279_SPREAD_COST_MARGIN_TARGET;P279_TIME_TO_EXIT_TARGET;P279_ADVERSE_SELECTION_AVOIDANCE_TARGET;P279_REPLENISHMENT_CONFIRMATION_TARGET;P279_NET_EDGE_DISTRIBUTION_SHIFT_TARGET | Carry forward families with positive max annualized diagnostics. |
| P282_SEARCH_TYPE | regime_conditioned_full_depth_ensemble | Combine multiple full-depth L2 targets under regime/time/spread buckets. |
| P282_REQUIRED_DIRECTIONS | regime_conditioning;family_ensemble;time_of_day_filter;spread_state_filter;event_count_floor;fixed_capital_cost200 | Broaden the search axis rather than relaxing cost stress. |
| P282_BOUNDARY | no_paper_live;no_deployable_profitability_claim;full_depth_required;l1_only_forbidden;net_edge_live_mask_forbidden | Boundaries remain closed. |

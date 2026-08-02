# Phase276 Multiday Synthetic Follow-through Interpretation

Generated UTC: 2026-08-02T06:36:21.570969+00:00

Phase276 interprets the Phase275 synthetic multiday follow-through.
The conclusion is not promotion: the pocket has a sparse normal-cost positive signal but fails 2x-cost robustness.
The selected next route is a cost-robust full-depth redesign search.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase276_interpretation_complete | 1 | Phase276 multiday synthetic follow-through interpretation completed |
| phase276_selected_next_route | P276_COST_ROBUST_FULL_DEPTH_REDESIGN_SEARCH | Selected next route |
| phase276_phase275_scenario_rows | 4800 | Phase275 scenarios interpreted |
| phase276_phase275_synthetic_date_rows | 8 | Synthetic dates per Phase275 scenario |
| phase276_phase275_cost100_above12_scenario_rows | 2 | Phase275 cost100 above-12 rows |
| phase276_phase275_cost200_above12_scenario_rows | 0 | Phase275 cost200 above-12 rows |
| phase276_phase275_best_synthetic_multiday_annualized_pct | 15.091000980326113 | Best Phase275 synthetic multiday annualized diagnostic |
| phase276_ranked_profile_rows | 5 | Ranked interpreted profile rows |
| phase276_normal_cost_sparse_positive_profile_rows | 2 | Normal-cost sparse-positive profile rows |
| phase276_cost200_failed_profile_rows | 3 | Cost200 failed profile rows |
| phase276_best_redesign_anchor_profile | TOP2_PRIORITY_SUBSET:cost200 | Best redesign anchor profile |
| phase276_best_redesign_anchor_max_annualized_pct | 9.88209 | Best redesign anchor max synthetic annualized diagnostic |
| phase276_phase275_as_is_promotion_allowed | 0 | Phase275 pocket cannot be promoted as-is |
| phase276_portfolio_claim_allowed | 0 | Robust real portfolio claim remains closed |
| phase276_strategy_replay_allowed | 0 | No strategy replay unlocked |
| phase276_strategy_promotion_allowed | 0 | No strategy promotion unlocked |
| phase276_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance |
| phase276_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase276_hard_gate_pass_rows | 7 | Hard gates passed |
| phase276_hard_gate_rows | 7 | Hard gates evaluated |
| phase276_next_best_action | run_phase277_cost_robust_full_depth_redesign_search_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P276_PHASE275_WORK_ORDER_PRESENT | True | run_phase276_multiday_synthetic_followthrough_interpretation_no_paper_live | Phase275 next action targets Phase276 | hard |
| P276_PHASE275_SEARCH_COMPLETE | True | 1 | Phase275 complete | hard |
| P276_PHASE275_HARD_GATES_PASS | True | 9/9 | Phase275 hard gates pass | hard |
| P276_RESULTS_PRESENT | True | scenarios=4800;ranked=5 | Phase275 results interpreted | hard |
| P276_OUTCOME_CLASSIFIED_AS_FRAGILE | True | cost100_above12=2;cost200_above12=0 | normal-cost positive but cost200 failed | hard |
| P276_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |
| P276_NEXT_ROUTE_SELECTED | True | P276_COST_ROBUST_FULL_DEPTH_REDESIGN_SEARCH | Phase277 cost-robust redesign selected | hard |

## Ranked Multiday Synthetic Profiles

| phase275_scope_profile_id | phase275_scope_id | phase275_scope_candidate_id | cost_profile | scenario_rows | synthetic_above12_scenario_rows | above12_fraction | min_annualized_pct | median_annualized_pct | max_annualized_pct | mean_net_pnl_inr | max_net_pnl_inr | min_net_pnl_inr | best_scenario_id | best_order_policy | best_synthetic_regime | best_synthetic_seed | best_initial_capital_inr | best_fixed_notional_inr | best_max_concurrent_positions | best_scheduled_event_rows | cost200_profile | normal_cost_sparse_positive | cost200_failed | median_failed | worst_case_failed | redesign_priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TOP2_PRIORITY_SUBSET:cost200 | TOP2_PRIORITY_SUBSET | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION;P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost200 | 960 | 0 | 0 | -14.3877 | -3.78656 | 9.88209 | -189.909 | 313.717 | -768.734 | P271_P275_TOP2_PRIORITY_SUBSET_REVERSE_RANK_TIME_BASE_BOOTSTRAP_SEED202_CAP100000_NOT100000_CONC1_COST200 | reverse_rank_time | base_bootstrap | 202 | 100000 | 100000 | 1 | 2 | 1 | 0 | 1 | 1 | 1 | 1 |
| PRIORITY01:cost200 | PRIORITY01 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | cost200 | 960 | 0 | 0 | -13.9498 | -1.90269 | 4.49778 | -112.974 | 319.233 | -671.615 | P271_P275_PRIORITY01_TIME_REVERSE_RANK_BASE_BOOTSTRAP_SEED404_CAP100000_NOT100000_CONC1_COST200 | time_reverse_rank | base_bootstrap | 404 | 100000 | 100000 | 1 | 2 | 1 | 0 | 1 | 1 | 1 | 1 |
| PRIORITY02:cost200 | PRIORITY02 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost200 | 960 | 0 | 0 | -7.24864 | -0.620703 | 2.88157 | -77.8617 | 182.957 | -460.231 | P271_P275_PRIORITY02_DETERMINISTIC_SHUFFLE_BASE_BOOTSTRAP_SEED404_CAP100000_NOT75000_CONC2_COST200 | deterministic_shuffle | base_bootstrap | 404 | 100000 | 75000 | 2 | 2 | 1 | 0 | 1 | 1 | 1 | 1 |
| TOP2_PRIORITY_SUBSET:cost100 | TOP2_PRIORITY_SUBSET | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION;P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost100 | 960 | 2 | 0.00208333 | -9.17878 | 0.518136 | 15.091 | 14.0375 | 665.355 | -421.763 | P271_P275_TOP2_PRIORITY_SUBSET_REVERSE_RANK_TIME_BASE_BOOTSTRAP_SEED202_CAP100000_NOT100000_CONC1_COST100 | reverse_rank_time | base_bootstrap | 202 | 100000 | 100000 | 1 | 2 | 0 | 1 | 0 | 1 | 1 | 1 |
| TOP2_PRIORITY_SUBSET:cost100_plus_1bp | TOP2_PRIORITY_SUBSET | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION;P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost100_plus_1bp | 960 | 2 | 0.00208333 | -9.80878 | -0.0542935 | 14.461 | -10.6291 | 607.021 | -455.096 | P271_P275_TOP2_PRIORITY_SUBSET_REVERSE_RANK_TIME_BASE_BOOTSTRAP_SEED202_CAP100000_NOT100000_CONC1_COST100_PLUS_1BP | reverse_rank_time | base_bootstrap | 202 | 100000 | 100000 | 1 | 2 | 0 | 1 | 0 | 1 | 1 | 1 |

## Interpretation Ledger

| finding_id | evidence | severity | finding_present | interpretation |
| --- | --- | --- | --- | --- |
| synthetic_multiday_search_executed | scenario_rows=4800;synthetic_dates=8 | evidence | 1 | Phase275 moved beyond one-date diagnostics into synthetic multiday testing. |
| normal_cost_sparse_positive_exists | cost100_above12=2;best_ann=15.091000980326113 | research_positive | 1 | A small normal-cost pocket exists, but it is sparse. |
| cost200_multiday_failure | cost200_above12=0;cost200_median_above12=0;cost200_worst_above12=0 | hard_negative | 1 | The focused pocket does not survive 2x-cost synthetic multiday stress. |
| sparsity_warning | sparse_positive_profiles=2;scenario_rows=4800 | risk | 1 | Above-12 outcomes are rare and concentrated, so do not overfit to the best seed/regime. |
| full_depth_route_still_material | sample ledger preserves top-five and levels 2-5 depth features | constraint | 1 | Do not fall back to L1-only features; redesign must remain full-depth. |
| next_route_should_redesign_for_cost_robustness | P276_COST_ROBUST_FULL_DEPTH_REDESIGN_SEARCH | next_action | 1 | The next executable search should target edge magnitude, fill selectivity, and cost robustness. |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| close_phase275_for_promotion | 1 | cost200_above12=0;portfolio_claim=0 | No promotion, paper/live, or deployable profitability claim is allowed. |
| recognize_fragile_normal_cost_pocket | 1 | cost100_above12=2;best_profile=TOP2_PRIORITY_SUBSET:cost100 | Keep the signal as a research clue, not as an accepted strategy. |
| reject_as_is_focused_pocket | 1 | cost200_multiday_above12=0 | The Phase275 focused pocket should not be continued unchanged. |
| selected_redesign_anchor_profile | TOP2_PRIORITY_SUBSET:cost200 | redesign_priority=1;max_ann=9.882085380326114 | Use the strongest fragile profiles as anchors for redesign. |
| selected_next_route | P276_COST_ROBUST_FULL_DEPTH_REDESIGN_SEARCH | cost robustness failed but normal-cost pocket exists | Execute a cost-robust full-depth redesign search. |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P277_INPUT | outputs/phase275/phase275_multiday_synthetic_scenario_results.csv;outputs/phase275/phase275_sample_synthetic_scheduled_event_ledger.csv | Use Phase275 scenario and scheduled-event evidence. |
| P277_ANCHOR_PROFILES | TOP2_PRIORITY_SUBSET:cost200;PRIORITY01:cost200;PRIORITY02:cost200 | Anchor redesign on fragile normal-cost and near-surviving cost-stress profiles. |
| P277_SEARCH_TYPE | cost_robust_full_depth_redesign_search | Execute a new search, not a paper/live route. |
| P277_OBJECTIVE | increase_cost200_above12_and_median_stability_without_l1_only_fallback | Target cost robustness while retaining full-depth L2 materiality. |
| P277_REQUIRED_FEATURE_FAMILIES | top5_imbalance;levels_2_to_5_depth;depth_replenishment_withdrawal;spread_regime;event_sparsity | Keep full-depth order-book features central. |
| P277_BOUNDARY | no_paper_live;no_deployable_profitability_claim;no_strategy_replay_until_cost_robust_multiday_acceptance | Boundaries remain closed. |

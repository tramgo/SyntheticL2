# Phase274 Focused Capital Follow-through Interpretation

Generated UTC: 2026-08-02T03:20:43.180625+00:00

Phase274 interprets the Phase273 focused follow-through search.
The result is strong enough to continue into synthetic-only multi-date follow-through, but not strong enough for replay promotion or portfolio-return claims.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase274_interpretation_complete | 1 | Phase274 focused capital follow-through interpretation completed |
| phase274_selected_next_route | P274_FOCUSED_CAPITAL_MULTIDAY_SYNTHETIC_FOLLOWTHROUGH_SEARCH | Selected next route |
| phase274_phase273_scenario_rows | 3600 | Phase273 scenarios interpreted |
| phase274_phase273_cost100_above12_scenario_rows | 332 | Phase273 cost100 above-12 rows |
| phase274_phase273_cost200_above12_scenario_rows | 121 | Phase273 cost200 above-12 rows |
| phase274_ranked_scope_profile_rows | 15 | Ranked scope/profile rows |
| phase274_cost200_survivor_scope_profile_rows | 3 | Scope/profile rows with 2x-cost above-12 diagnostics |
| phase274_median_positive_scope_profile_rows | 2 | Scope/profile rows with median above 12% |
| phase274_worst_case_positive_scope_profile_rows | 0 | Scope/profile rows with worst case above 12% |
| phase274_best_scope_profile | TOP2_PRIORITY_SUBSET:cost200 | Best ranked scope/profile |
| phase274_best_scenario_id | P271_P273_TOP2_PRIORITY_SUBSET_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST200 | Best scenario ID |
| phase274_best_order_policy | deterministic_shuffle | Best order policy |
| phase274_best_max_annualized_pct | 102.404 | Best max one-date annualized diagnostic |
| phase274_best_median_annualized_pct | -24.7511 | Best median one-date annualized diagnostic |
| phase274_portfolio_claim_allowed | 0 | Robust portfolio claim remains closed |
| phase274_strategy_replay_allowed | 0 | No strategy replay unlocked |
| phase274_strategy_promotion_allowed | 0 | No strategy promotion unlocked |
| phase274_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance |
| phase274_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase274_hard_gate_pass_rows | 7 | Hard gates passed |
| phase274_hard_gate_rows | 7 | Hard gates evaluated |
| phase274_next_best_action | run_phase275_focused_capital_multiday_synthetic_followthrough_search_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P274_PHASE273_WORK_ORDER_PRESENT | True | run_phase274_focused_capital_followthrough_interpretation_no_paper_live | Phase273 next action targets Phase274 | hard |
| P274_PHASE273_SEARCH_COMPLETE | True | 1 | Phase273 complete | hard |
| P274_PHASE273_HARD_GATES_PASS | True | 8/8 | Phase273 hard gates pass | hard |
| P274_RESULTS_PRESENT | True | results=3600;ranked=15 | Phase273 results ranked | hard |
| P274_COST200_SURVIVAL_RECOGNIZED | True | 121 | >0 cost200 diagnostic survivors | hard |
| P274_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |
| P274_NEXT_ROUTE_SELECTED | True | P274_FOCUSED_CAPITAL_MULTIDAY_SYNTHETIC_FOLLOWTHROUGH_SEARCH | Phase275 multi-date follow-through selected | hard |

## Ranked Follow-through Scope Profiles

| phase273_scope_id | phase273_scope_candidate_id | cost_profile | scenario_rows | above12_scenario_rows | above12_fraction | median_annualized_pct | min_annualized_pct | max_annualized_pct | max_realized_net_pnl_inr | best_scenario_id | best_order_policy | best_initial_capital_inr | best_fixed_notional_inr | best_max_concurrent_positions | best_scheduled_event_rows | best_notional_turnover_x_initial_capital | worst_drawdown_inr | followthrough_preserve | cost200_survivor | median_positive | worst_case_positive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TOP2_PRIORITY_SUBSET | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION;P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost200 | 240 | 47 | 0.195833 | -24.7511 | -80.9927 | 102.404 | 507.956 | P271_P273_TOP2_PRIORITY_SUBSET_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST200 | deterministic_shuffle | 100000 | 100000 | 1 | 4 | 4 | -1690.82 | 1 | 1 | 0 | 0 |
| PRIORITY02 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost200 | 240 | 39 | 0.1625 | -13.2407 | -39.6573 | 47.003 | 284.88 | P271_P273_PRIORITY02_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST200 | deterministic_shuffle | 100000 | 100000 | 1 | 2 | 2 | -553.791 | 1 | 1 | 0 | 0 |
| PRIORITY01 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | cost200 | 240 | 35 | 0.145833 | -26.2668 | -73.0037 | 87.7304 | 435.171 | P271_P273_PRIORITY01_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST200 | deterministic_shuffle | 100000 | 100000 | 1 | 3 | 3 | -875.638 | 1 | 1 | 0 | 0 |
| TOP2_PRIORITY_SUBSET | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION;P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost100 | 240 | 158 | 0.658333 | 17.9013 | -11.5405 | 190.635 | 945.612 | P271_P273_TOP2_PRIORITY_SUBSET_TIME_RANK_CAP100000_NOT125000_CONC1_COST100 | time_rank | 100000 | 125000 | 1 | 6 | 6 | -1168.45 | 1 | 0 | 1 | 0 |
| TOP2_PRIORITY_SUBSET | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION;P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost100_plus_1bp | 240 | 129 | 0.5375 | 13.1673 | -19.9405 | 175.667 | 871.362 | P271_P273_TOP2_PRIORITY_SUBSET_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST100_PLUS_1BP | deterministic_shuffle | 100000 | 100000 | 1 | 4 | 4 | -1230.95 | 1 | 0 | 1 | 0 |
| PRIORITY01 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | cost100 | 240 | 91 | 0.379167 | 10.4611 | -0.0788538 | 150.237 | 745.225 | P271_P273_PRIORITY01_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST100 | deterministic_shuffle | 100000 | 100000 | 1 | 3 | 3 | -605.895 | 1 | 0 | 0 | 0 |
| PRIORITY01 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | cost100_plus_1bp | 240 | 87 | 0.3625 | 4.55742 | -8.89885 | 142.677 | 707.725 | P271_P273_PRIORITY01_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST100_PLUS_1BP | deterministic_shuffle | 100000 | 100000 | 1 | 3 | 3 | -630.895 | 1 | 0 | 0 | 0 |
| TOP2_PRIORITY_SUBSET | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION;P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost100_plus_2bp | 240 | 83 | 0.345833 | 6.47349 | -28.3405 | 165.587 | 821.362 | P271_P273_TOP2_PRIORITY_SUBSET_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST100_PLUS_2BP | deterministic_shuffle | 100000 | 100000 | 1 | 4 | 4 | -1293.45 | 1 | 0 | 0 | 0 |
| PRIORITY02 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost100 | 240 | 83 | 0.345833 | 5.92211 | -8.40385 | 88.6743 | 698.286 | P271_P273_PRIORITY02_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST100 | deterministic_shuffle | 100000 | 100000 | 1 | 2 | 2 | -444.827 | 1 | 0 | 0 | 0 |
| PRIORITY02 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost100_plus_1bp | 240 | 79 | 0.329167 | 2.73011 | -12.1839 | 83.6343 | 648.286 | P271_P273_PRIORITY02_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST100_PLUS_1BP | deterministic_shuffle | 100000 | 100000 | 1 | 2 | 2 | -457.327 | 1 | 0 | 0 | 0 |
| PRIORITY01 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | cost100_plus_2bp | 240 | 75 | 0.3125 | -0.993717 | -17.7189 | 135.117 | 670.225 | P271_P273_PRIORITY01_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST100_PLUS_2BP | deterministic_shuffle | 100000 | 100000 | 1 | 3 | 3 | -655.895 | 1 | 0 | 0 | 0 |
| PRIORITY02 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost100_plus_2bp | 240 | 69 | 0.2875 | -0.291717 | -15.9639 | 78.5943 | 598.286 | P271_P273_PRIORITY02_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST100_PLUS_2BP | deterministic_shuffle | 100000 | 100000 | 1 | 2 | 2 | -469.827 | 1 | 0 | 0 | 0 |
| TOP2_PRIORITY_SUBSET | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION;P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost150 | 240 | 64 | 0.266667 | -2.17463 | -46.2666 | 144.075 | 714.659 | P271_P273_TOP2_PRIORITY_SUBSET_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST150 | deterministic_shuffle | 100000 | 100000 | 1 | 4 | 4 | -1426.83 | 1 | 0 | 0 | 0 |
| PRIORITY01 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | cost150 | 240 | 55 | 0.229167 | -9.59825 | -36.5413 | 118.984 | 590.198 | P271_P273_PRIORITY01_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST150 | deterministic_shuffle | 100000 | 100000 | 1 | 3 | 3 | -709.247 | 1 | 0 | 0 | 0 |
| PRIORITY02 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | cost150 | 240 | 53 | 0.220833 | -4.59398 | -24.0306 | 67.8387 | 491.583 | P271_P273_PRIORITY02_DETERMINISTIC_SHUFFLE_CAP100000_NOT100000_CONC1_COST150 | deterministic_shuffle | 100000 | 100000 | 1 | 2 | 2 | -496.502 | 1 | 0 | 0 | 0 |

## Interpretation Ledger

| finding_id | evidence | severity | finding_present | interpretation |
| --- | --- | --- | --- | --- |
| focused_followthrough_strengthened_signal | cost100_above12=332;cost200_above12=121;best_ann=190.6353099362237 | research_positive | 1 | Phase273 strengthened the candidate-specific one-date diagnostic. |
| top2_subset_is_best_scope | TOP2_PRIORITY_SUBSET | research_positive | 1 | The two priority candidates combine better than either broad pooling or single-candidate-only best case. |
| order_policy_fragility_remains | median_positive_rows=2;worst_case_positive_rows=0 | risk | 1 | Some order policies and scenario settings remain negative, so this is not ready for promotion. |
| cost200_survivor_profiles_exist | cost200_scope_profile_rows=3 | research_positive | 1 | 2x-cost diagnostic survival exists but remains one-date evidence. |
| one_date_blocks_portfolio_claim | observed_trade_dates=1;required>=5 | hard_boundary | 1 | Annualized values remain one-date mechanical diagnostics. |
| next_step_must_execute_multiday_synthetic_followthrough | scenario_rows=3600 | next_action | 1 | Move from one-date diagnostic to synthetic-only multi-date follow-through search. |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| preserve_phase273_followthrough_pockets | 1 | preserved_scope_profile_rows=15;top_scope=TOP2_PRIORITY_SUBSET | Keep Phase273 pockets for multi-date synthetic follow-through. |
| do_not_promote_or_claim_portfolio_return | 1 | one_date_diagnostic_only | No replay, paper/live, or deployable annual return claim. |
| do_not_continue_broad_pooled_allocator | 1 | Phase272 pooled_above12=0 | Continue focused top-two/candidate route instead of all-ranked pooling. |
| selected_next_route | P274_FOCUSED_CAPITAL_MULTIDAY_SYNTHETIC_FOLLOWTHROUGH_SEARCH | execute synthetic-only multi-date follow-through search | Next step should execute a broader synthetic follow-through search. |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P275_INPUT | outputs/phase273/phase273_followthrough_scenario_results.csv;outputs/phase273/phase273_order_policy_stability_summary.csv | Use Phase273 focused follow-through evidence. |
| P275_SCOPE_PROFILES | TOP2_PRIORITY_SUBSET:cost200;PRIORITY02:cost200;PRIORITY01:cost200;TOP2_PRIORITY_SUBSET:cost100;TOP2_PRIORITY_SUBSET:cost100_plus_1bp | Focus on strongest top-two and priority scope/cost profiles. |
| P275_SEARCH_TYPE | focused_capital_multiday_synthetic_followthrough_search | Execute synthetic-only multi-date or multi-seed follow-through, not a precommit-only step. |
| P275_DEPTH_REQUIREMENT | full_top_five_rows_1_to_5_and_levels_2_to_5_required | Keep full-depth L2 requirement. |
| P275_BOUNDARY | no_paper_live;no_deployable_profitability_claim_until_multiday_acceptance | No claim until multi-date gates pass. |

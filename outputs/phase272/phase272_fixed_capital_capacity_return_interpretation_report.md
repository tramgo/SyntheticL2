# Phase272 Fixed-capital Capacity-return Interpretation

Generated UTC: 2026-08-02T03:09:15.966905+00:00

Phase272 interprets Phase271's fixed-capital scheduled diagnostics.
The key finding is candidate-specific profitable one-date pockets, while the pooled all-ranked allocator is not yet profitable.
The next step is focused candidate follow-through, not replay promotion or paper/live acceptance.
Annualized values remain one-date mechanical diagnostics until enough dates exist for a robust portfolio claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase272_interpretation_complete | 1 | Phase272 fixed-capital capacity-return interpretation completed |
| phase272_selected_next_route | P272_FOCUSED_CAPITAL_AWARE_CANDIDATE_FOLLOWTHROUGH_SEARCH | Selected next route |
| phase272_phase271_scenario_rows | 4320 | Phase271 scenario rows interpreted |
| phase272_phase271_scope_rows | 18 | Phase271 scheduling scopes interpreted |
| phase272_phase271_observed_trade_dates | 1 | Observed dates remain one-date diagnostic |
| phase272_ranked_capital_candidate_rows | 17 | Per-candidate capital-aware rows ranked |
| phase272_followthrough_priority_candidate_rows | 2 | Candidates with 2x and multi-profile one-date diagnostic support |
| phase272_pooled_above12_scenario_rows | 0 | Pooled all-ranked lead above-12 diagnostic rows |
| phase272_best_candidate_id | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | Best follow-through candidate |
| phase272_best_scenario_id | P271_CAND003_CAP100000_NOT100000_CONC1_COST100 | Best scenario for best candidate |
| phase272_best_cost_profile | cost100 | Best cost profile |
| phase272_best_realized_net_pnl_inr | 545.516 | Best realized net P&L |
| phase272_best_mechanical_one_date_annualized_portfolio_return_pct | 137.47 | Best one-date annualized diagnostic |
| phase272_best_cost200_above12_scenario_rows | 3 | Best candidate 2x-cost above-12 rows |
| phase272_portfolio_claim_allowed | 0 | Robust portfolio claim remains closed |
| phase272_strategy_replay_allowed | 0 | No strategy replay unlocked |
| phase272_strategy_promotion_allowed | 0 | No strategy promotion unlocked |
| phase272_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance |
| phase272_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase272_hard_gate_pass_rows | 9 | Hard gates passed |
| phase272_hard_gate_rows | 9 | Hard gates evaluated |
| phase272_next_best_action | run_phase273_focused_capital_aware_candidate_followthrough_search_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P272_PHASE271_WORK_ORDER_PRESENT | True | run_phase272_fixed_capital_capacity_return_interpretation_no_paper_live | Phase271 next action targets Phase272 | hard |
| P272_PHASE271_ANALYSIS_COMPLETE | True | 1 | Phase271 complete | hard |
| P272_PHASE271_HARD_GATES_PASS | True | 12/12 | Phase271 hard gates pass | hard |
| P272_SCENARIOS_PRESENT | True | 4320 | >0 Phase271 scenarios | hard |
| P272_PRIORITY_POCKETS_FOUND | True | 2 | >0 follow-through priority candidates | hard |
| P272_FULL_DEPTH_PRESERVED | True | full=1;l2_l5=1;l1_only=0 | full-depth and no L1-only | hard |
| P272_ONE_DATE_BOUNDARY_RECOGNIZED | True | dates=1;portfolio_claim=0 | one-date diagnostic only | hard |
| P272_NO_PROMOTION_OR_DEPLOYABLE_CLAIM | True | 0 | deployable claim closed | hard |
| P272_NEXT_ROUTE_SELECTED | True | P272_FOCUSED_CAPITAL_AWARE_CANDIDATE_FOLLOWTHROUGH_SEARCH | Phase273 focused follow-through selected | hard |

## Ranked Capital-aware Research Pockets

| scope_candidate_id | best_scenario_id | best_scope_id | best_cost_profile | best_initial_capital_inr | best_fixed_notional_inr | best_max_concurrent_positions | best_scheduled_event_rows | best_rejected_event_rows | best_realized_net_pnl_inr | best_portfolio_return_pct | best_mechanical_one_date_annualized_portfolio_return_pct | best_notional_turnover_x_initial_capital | best_max_drawdown_inr | cost100_above12_scenario_rows | cost150_above12_scenario_rows | cost200_above12_scenario_rows | cost100_plus_1bp_above12_scenario_rows | cost100_plus_2bp_above12_scenario_rows | robust_cost_profile_count | followthrough_priority | portfolio_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | P271_CAND003_CAP100000_NOT100000_CONC1_COST100 | CAND003 | cost100 | 100000 | 100000 | 1 | 5 | 6 | 545.516 | 0.545516 | 137.47 | 5 | -128.855 | 9 | 6 | 3 | 9 | 6 | 5 | 1 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | P271_CAND001_CAP100000_NOT100000_CONC1_COST100 | CAND001 | cost100 | 100000 | 100000 | 1 | 2 | 7 | 289.164 | 0.289164 | 72.8694 | 2 | 0 | 6 | 4 | 3 | 6 | 6 | 5 | 1 | 0 |
| P268_P268_ASK_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPMID | P271_CAND004_CAP100000_NOT100000_CONC1_COST100 | CAND004 | cost100 | 100000 | 100000 | 1 | 6 | 9 | 492.952 | 0.492952 | 124.224 | 6 | -112.875 | 21 | 6 | 0 | 18 | 10 | 4 | 0 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPCOMPRESSION | P271_CAND014_CAP100000_NOT100000_CONC1_COST100 | CAND014 | cost100 | 100000 | 100000 | 1 | 4 | 4 | 341.719 | 0.341719 | 86.1133 | 4 | -128.855 | 6 | 3 | 0 | 6 | 6 | 4 | 0 | 0 |
| P268_P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR_H10_IQ0p75_SQ0p75_SPMID | P271_CAND017_CAP100000_NOT100000_CONC1_COST100 | CAND017 | cost100 | 100000 | 100000 | 1 | 9 | 42 | 265.44 | 0.26544 | 66.8908 | 9 | -276.888 | 6 | 0 | 0 | 3 | 1 | 3 | 0 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPHIGH | P271_CAND006_CAP100000_NOT100000_CONC1_COST100 | CAND006 | cost100 | 100000 | 100000 | 1 | 1 | 5 | 78.1911 | 0.0781911 | 19.7042 | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 3 | 0 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p75_SPCOMPRESSION | P271_CAND012_CAP100000_NOT100000_CONC1_COST100 | CAND012 | cost100 | 100000 | 100000 | 1 | 6 | 7 | 111.957 | 0.111957 | 28.2131 | 6 | -262.177 | 2 | 0 | 0 | 1 | 0 | 2 | 0 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPLOW | P271_CAND010_CAP100000_NOT100000_CONC2_COST100 | CAND010 | cost100 | 100000 | 100000 | 2 | 8 | 4 | 61.3595 | 0.0613595 | 15.4626 | 4 | -109.837 | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| P268_P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR_H10_IQ0p9_SQ0p75_SPMID | P271_CAND002_CAP100000_NOT25000_CONC4_COST100 | CAND002 | cost100 | 100000 | 25000 | 4 | 18 | 11 | 56.682 | 0.056682 | 14.2839 | 4.5 | -113.983 | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p75_SPLOW | P271_CAND015_CAP1000000_NOT25000_CONC8_COST100 | CAND015 | cost100 | 1e+06 | 25000 | 8 | 6 | 2 | -12.3134 | -0.00123134 | -0.310297 | 0.15 | -65.5442 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPHIGH | P271_CAND005_CAP1000000_NOT25000_CONC1_COST100 | CAND005 | cost100 | 1e+06 | 25000 | 1 | 3 | 8 | -12.8388 | -0.00128388 | -0.323539 | 0.075 | -85.1299 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p5_SPLOW | P271_CAND011_CAP1000000_NOT25000_CONC8_COST100 | CAND011 | cost100 | 1e+06 | 25000 | 8 | 9 | 3 | -18.5886 | -0.00185886 | -0.468432 | 0.225 | -94.219 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p6_SPLOW | P271_CAND013_CAP1000000_NOT25000_CONC8_COST100 | CAND013 | cost100 | 1e+06 | 25000 | 8 | 7 | 3 | -27.6106 | -0.00276106 | -0.695786 | 0.175 | -80.8414 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPLOW | P271_CAND016_CAP1000000_NOT25000_CONC1_COST100 | CAND016 | cost100 | 1e+06 | 25000 | 1 | 4 | 6 | -34.8807 | -0.00348807 | -0.878994 | 0.1 | -85.83 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPCOMPRESSION | P271_CAND007_CAP1000000_NOT25000_CONC1_COST100 | CAND007 | cost100 | 1e+06 | 25000 | 1 | 5 | 9 | -45.5445 | -0.00455445 | -1.14772 | 0.125 | -116.042 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPCOMPRESSION | P271_CAND008_CAP1000000_NOT25000_CONC1_COST100 | CAND008 | cost100 | 1e+06 | 25000 | 1 | 5 | 9 | -45.5445 | -0.00455445 | -1.14772 | 0.125 | -116.042 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPHIGH | P271_CAND009_CAP1000000_NOT25000_CONC1_COST100 | CAND009 | cost100 | 1e+06 | 25000 | 1 | 4 | 8 | -47.9664 | -0.00479664 | -1.20875 | 0.1 | -120.257 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Scope Summary

| scope_id | scope_candidate_id | scenario_rows | cost_profile_rows | above12_scenario_rows | best_annualized_pct | best_realized_net_pnl_inr | max_scheduled_event_rows |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CAND004 | P268_P268_ASK_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPMID | 240 | 5 | 55 | 124.224 | 492.952 | 9 |
| CAND003 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | 240 | 5 | 33 | 137.47 | 545.516 | 8 |
| CAND001 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | 240 | 5 | 25 | 72.8694 | 289.164 | 4 |
| CAND014 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPCOMPRESSION | 240 | 5 | 21 | 86.1133 | 341.719 | 6 |
| CAND017 | P268_P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR_H10_IQ0p75_SQ0p75_SPMID | 240 | 5 | 10 | 66.8908 | 265.44 | 31 |
| CAND002 | P268_P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR_H10_IQ0p9_SQ0p75_SPMID | 240 | 5 | 4 | 14.2839 | 226.728 | 20 |
| CAND012 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p75_SPCOMPRESSION | 240 | 5 | 3 | 28.2131 | 111.957 | 9 |
| CAND006 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPHIGH | 240 | 5 | 3 | 19.7042 | 78.1911 | 2 |
| CAND010 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPLOW | 240 | 5 | 3 | 15.4626 | 122.719 | 9 |
| CAND015 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p75_SPLOW | 240 | 5 | 0 | -0.310297 | -6.15669 | 6 |
| CAND005 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPHIGH | 240 | 5 | 0 | -0.323539 | -12.8388 | 6 |
| CAND011 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p5_SPLOW | 240 | 5 | 0 | -0.468432 | -9.29429 | 9 |
| CAND013 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p6_SPLOW | 240 | 5 | 0 | -0.695786 | -13.8053 | 7 |
| CAND016 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPLOW | 240 | 5 | 0 | -0.878994 | -24.191 | 7 |
| ALL_RANKED_LEADS | ALL_RANKED_LEADS | 240 | 5 | 0 | -0.933074 | -37.0268 | 40 |
| CAND007 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPCOMPRESSION | 240 | 5 | 0 | -1.14772 | -29.9914 | 10 |
| CAND008 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPCOMPRESSION | 240 | 5 | 0 | -1.14772 | -29.9914 | 10 |
| CAND009 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPHIGH | 240 | 5 | 0 | -1.20875 | -47.9664 | 7 |

## Interpretation Ledger

| finding_id | evidence | severity | finding_present | interpretation |
| --- | --- | --- | --- | --- |
| fixed_capital_scheduler_materialized | scenario_rows=4320;observed_dates=1 | positive_mechanics | 1 | Capital-aware denominator and scheduler are now materialized. |
| per_candidate_profitable_pockets_found | cost100_above12=58;cost200_above12=6;best_candidate=P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION;best_ann=137.4701128605055 | research_positive | 1 | Small one-date capital-aware pockets exist and should be chased with focused follow-through. |
| pooled_allocator_not_yet_working | pooled_above12_scenarios=0 | important_context | 1 | Pooling all ranked leads diluted the edge; follow-through should isolate candidates first. |
| cost200_survival_is_sparse_but_nonzero | cost200_above12=6;followthrough_priority_candidates=2 | research_positive | 1 | Some pockets survive 2x modeled Zerodha costs on the one-date diagnostic. |
| one_date_only_blocks_portfolio_claim | observed_dates=1;min_required=5;portfolio_claim_allowed=0 | hard_boundary | 1 | Do not call the annualized diagnostic a robust annual portfolio return. |
| deployable_profitability_claim_closed | deployable_profitability_claim_allowed=0 | hard_boundary | 1 | No paper/live or deployable profitability claim is opened by this result. |
| focused_followthrough_required | priority_candidates=2 | next_action | 1 | Next step should test focused candidate subsets and parameter neighborhoods, not broad pooled averaging. |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| preserve_phase271_capital_aware_pockets | 1 | priority_candidates=2;best_candidate=P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | Keep the profitable diagnostic pockets for immediate focused strategy follow-through. |
| do_not_claim_robust_annual_portfolio_return | 1 | observed_dates=1;min_required=5 | One-date annualization is a diagnostic only. |
| do_not_promote_or_paper_live | 1 | acceptance_grade_scenario_rows=0 | No replay promotion, paper/live, or deployable claim is allowed. |
| avoid_broad_pooled_allocator_for_next_step | 1 | ALL_RANKED_LEADS produced no above-12 diagnostic scenarios | Do not average away small candidate-specific edges. |
| selected_next_route | P272_FOCUSED_CAPITAL_AWARE_CANDIDATE_FOLLOWTHROUGH_SEARCH | focused candidate follow-through search | Test the specific profitable pockets and near-neighbor parameterizations next. |

## Next Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P273_INPUT | outputs/phase271/phase271_capital_scenario_results.csv;outputs/phase271/phase271_scheduled_event_ledger.csv | Use capital-aware scenario and event evidence from Phase271. |
| P273_CANDIDATE_SCOPE | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION;P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH;P268_P268_ASK_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPMID;P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPCOMPRESSION;P268_P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR_H10_IQ0p75_SQ0p75_SPMID | Focus on top per-candidate pockets rather than the all-ranked pooled allocator. |
| P273_SEARCH_TYPE | focused_capital_aware_candidate_followthrough_search | Evaluate top-candidate subsets, cost profiles, notional/concurrency neighborhoods and event-order sensitivity. |
| P273_DEPTH_REQUIREMENT | full_top_five_rows_1_to_5_and_levels_2_to_5_required | Preserve the full-depth Zerodha L2 objective. |
| P273_ACCEPTANCE_BOUNDARY | one_date_diagnostic_only;no_paper_live;no_deployable_profitability_claim | Do not relabel diagnostics as robust portfolio results. |
| P273_OUTPUT | focused_candidate_followthrough_results_and_interpretation | Produce a concrete next search, not just a plan. |

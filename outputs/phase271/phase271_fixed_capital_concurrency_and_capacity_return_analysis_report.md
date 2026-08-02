# Phase271 Fixed-capital Concurrency and Capacity Return Analysis

Generated UTC: 2026-08-02T03:02:16.423186+00:00

Phase271 converts the Phase269 fixed-notional research leads into scheduled fixed-capital diagnostics.
Each event consumes capital until its modeled horizon exit, same-symbol overlaps are rejected, and concurrency limits are enforced.
The annualized values in this phase are one-date mechanical diagnostics because the current evidence has one observed trade date.
Full Zerodha top-five market-by-price rows 1-5 and levels 2-5 remain mandatory; L1-only candidates remain forbidden.
This phase does not unlock replay, promotion, paper/live acceptance, or deployable profitability claims.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase271_fixed_capital_analysis_complete | 1 | Phase271 fixed-capital/concurrency/capacity analysis completed |
| phase271_selected_route | P271_FIXED_CAPITAL_CONCURRENCY_AND_CAPACITY_RETURN_ANALYSIS | Selected route |
| phase271_phase269_research_lead_rows | 17 | Phase269 ranked fixed-notional leads used |
| phase271_input_event_rows | 245 | Phase268 event rows used for scheduling |
| phase271_input_symbols | 17 | Input symbols |
| phase271_observed_trade_dates | 1 | Observed trade dates |
| phase271_scenario_rows | 4320 | Capital/concurrency/cost scenarios evaluated |
| phase271_scope_rows | 18 | Pooled plus per-candidate scheduling scopes |
| phase271_total_scheduled_event_rows | 37440 | Scheduled event rows across scenarios |
| phase271_cost100_annualized_above_12pct_scenario_rows | 58 | Cost100 scenarios above 12% one-date annualized diagnostic |
| phase271_cost150_annualized_above_12pct_scenario_rows | 19 | Cost150 scenarios above 12% one-date annualized diagnostic |
| phase271_cost200_annualized_above_12pct_scenario_rows | 6 | Cost200 scenarios above 12% one-date annualized diagnostic |
| phase271_cost100_plus_1bp_annualized_above_12pct_scenario_rows | 44 | Cost100 plus 1bp scenarios above 12% one-date annualized diagnostic |
| phase271_cost100_plus_2bp_annualized_above_12pct_scenario_rows | 30 | Cost100 plus 2bp scenarios above 12% one-date annualized diagnostic |
| phase271_best_scenario_id | P271_CAND003_CAP100000_NOT100000_CONC1_COST100 | Best mechanical one-date annualized scenario |
| phase271_best_realized_net_pnl_inr | 545.516 | Best scenario realized net P&L |
| phase271_best_portfolio_return_pct | 0.545516 | Best scenario one-date portfolio return percent |
| phase271_best_mechanical_one_date_annualized_portfolio_return_pct | 137.47 | Best scenario mechanical one-date annualized percent |
| phase271_best_scheduled_event_rows | 5 | Best scenario scheduled events |
| phase271_best_rejected_event_rows | 6 | Best scenario rejected events |
| phase271_best_notional_turnover_x_initial_capital | 5 | Best scenario notional turnover / capital |
| phase271_best_max_drawdown_inr | -128.855 | Best scenario max drawdown |
| phase271_annualized_return_is_robust_portfolio_claim | 0 | Only one observed date, annualized values are mechanical diagnostics |
| phase271_portfolio_claim_allowed | 0 | Robust portfolio claim allowed only with >=5 observed dates |
| phase271_unlimited_capital_assumption_allowed | 0 | Unlimited capital forbidden |
| phase271_fixed_notional_proxy_as_portfolio_return_allowed | 0 | Fixed-notional proxy cannot be relabeled |
| phase271_full_top_five_depth_required | 1 | Zerodha top-five rows 1-5 required |
| phase271_levels_2_to_5_materiality_required | 1 | Levels 2-5 materiality required |
| phase271_l1_only_candidate_allowed | 0 | L1-only candidates forbidden |
| phase271_acceptance_grade_scenario_rows | 0 | Robust portfolio acceptance rows |
| phase271_hard_gate_pass_rows | 12 | Hard gates passed |
| phase271_hard_gate_rows | 12 | Hard gates evaluated |
| phase271_strategy_replay_allowed | 0 | No strategy replay unlocked |
| phase271_strategy_promotion_allowed | 0 | No promotion unlocked |
| phase271_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance |
| phase271_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase271_next_best_action | run_phase272_fixed_capital_capacity_return_interpretation_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P271_PHASE270_WORK_ORDER_PRESENT | True | run_phase271_fixed_capital_concurrency_and_capacity_return_analysis_no_paper_live | Phase270 next action targets Phase271 | hard |
| P271_PHASE270_PRECOMMIT_COMPLETE | True | 1 | Phase270 fixed-capital precommit complete | hard |
| P271_RESEARCH_LEADS_PRESENT | True | 17 | >0 Phase269 research leads | hard |
| P271_EVENT_LEDGER_PRESENT | True | 245 | >0 Phase268 events for leads | hard |
| P271_SCENARIO_GRID_COMPLETE | True | 4320 | (pooled + per-lead) * 4*3*4*5 scenarios | hard |
| P271_FIXED_CAPITAL_DENOMINATOR_USED | True | 100000.0;250000.0;500000.0;1000000.0 | initial capital denominator | hard |
| P271_SCHEDULER_MATERIALIZED | True | 37440 | >0 scheduled events | hard |
| P271_UNLIMITED_CAPITAL_FORBIDDEN | True | 0 | no unlimited capital or robust claim from one date | hard |
| P271_FULL_TOP_FIVE_DEPTH_PRESERVED | True | full_depth=1200;variants=1200 | all variants full-depth | hard |
| P271_LEVELS_2_TO_5_MATERIALITY_PRESERVED | True | l2_l5=1200;l1_only=0;variants=1200 | levels 2-5 materiality and no L1-only | hard |
| P271_COST_STRESS_PROFILES_PRESENT | True | cost100;cost100_plus_1bp;cost100_plus_2bp;cost150;cost200 | base, 1.5x, 2x, plus slippage | hard |
| P271_NO_REPLAY_PROMOTION_PAPER_LIVE | True | 0 | replay/promotion/paper-live remain closed | hard |

## Top Capital Scenarios

| scenario_id | scope_id | scope_candidate_id | initial_capital_inr | fixed_notional_inr | max_concurrent_positions | cost_profile | cost_multiplier | extra_slippage_bps | input_event_rows | scheduled_event_rows | rejected_event_rows | rejected_same_symbol_overlap_rows | rejected_max_concurrent_rows | rejected_insufficient_cash_rows | candidate_rows | scheduled_candidate_rows | symbols | scheduled_symbols | observed_trade_dates | realized_net_pnl_inr | portfolio_return_pct | mechanical_one_date_annualized_portfolio_return_pct | annualized_return_is_robust_portfolio_claim | annualized_above_12pct_research_diagnostic | scheduled_notional_inr | notional_turnover_x_initial_capital | avg_open_notional_utilization | max_drawdown_inr | portfolio_claim_allowed | strategy_replay_allowed | promotion_allowed | paper_or_live_acceptance_allowed | deployable_profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P271_CAND003_CAP100000_NOT100000_CONC1_COST100 | CAND003 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | 100000 | 100000 | 1 | cost100 | 1 | 0 | 11 | 5 | 6 | 2 | 4 | 0 | 1 | 1 | 7 | 5 | 1 | 545.516 | 0.545516 | 137.47 | 0 | 1 | 500000 | 5 | 0.545455 | -128.855 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND003_CAP100000_NOT100000_CONC1_COST100_PLUS_1BP | CAND003 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | 100000 | 100000 | 1 | cost100_plus_1bp | 1 | 1 | 11 | 5 | 6 | 2 | 4 | 0 | 1 | 1 | 7 | 5 | 1 | 495.516 | 0.495516 | 124.87 | 0 | 1 | 500000 | 5 | 0.545455 | -143.647 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND004_CAP100000_NOT100000_CONC1_COST100 | CAND004 | P268_P268_ASK_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPMID | 100000 | 100000 | 1 | cost100 | 1 | 0 | 15 | 6 | 9 | 2 | 7 | 0 | 1 | 1 | 7 | 4 | 1 | 492.952 | 0.492952 | 124.224 | 0 | 1 | 600000 | 6 | 0.6 | -112.875 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND003_CAP100000_NOT100000_CONC1_COST100_PLUS_2BP | CAND003 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | 100000 | 100000 | 1 | cost100_plus_2bp | 1 | 2 | 11 | 5 | 6 | 2 | 4 | 0 | 1 | 1 | 7 | 5 | 1 | 445.516 | 0.445516 | 112.27 | 0 | 1 | 500000 | 5 | 0.545455 | -163.647 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND004_CAP100000_NOT100000_CONC1_COST100_PLUS_1BP | CAND004 | P268_P268_ASK_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPMID | 100000 | 100000 | 1 | cost100_plus_1bp | 1 | 1 | 15 | 6 | 9 | 2 | 7 | 0 | 1 | 1 | 7 | 4 | 1 | 432.952 | 0.432952 | 109.104 | 0 | 1 | 600000 | 6 | 0.6 | -122.875 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND004_CAP100000_NOT100000_CONC1_COST100_PLUS_2BP | CAND004 | P268_P268_ASK_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPMID | 100000 | 100000 | 1 | cost100_plus_2bp | 1 | 2 | 15 | 6 | 9 | 2 | 7 | 0 | 1 | 1 | 7 | 4 | 1 | 372.952 | 0.372952 | 93.9839 | 0 | 1 | 600000 | 6 | 0.6 | -132.875 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND014_CAP100000_NOT100000_CONC1_COST100 | CAND014 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPCOMPRESSION | 100000 | 100000 | 1 | cost100 | 1 | 0 | 8 | 4 | 4 | 1 | 3 | 0 | 1 | 1 | 5 | 4 | 1 | 341.719 | 0.341719 | 86.1133 | 0 | 1 | 400000 | 4 | 0.5 | -128.855 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND003_CAP100000_NOT100000_CONC1_COST150 | CAND003 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | 100000 | 100000 | 1 | cost150 | 1.5 | 0 | 11 | 5 | 6 | 2 | 4 | 0 | 1 | 1 | 7 | 5 | 1 | 338.813 | 0.338813 | 85.381 | 0 | 1 | 500000 | 5 | 0.545455 | -206.328 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND014_CAP100000_NOT100000_CONC1_COST100_PLUS_1BP | CAND014 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPCOMPRESSION | 100000 | 100000 | 1 | cost100_plus_1bp | 1 | 1 | 8 | 4 | 4 | 1 | 3 | 0 | 1 | 1 | 5 | 4 | 1 | 301.719 | 0.301719 | 76.0333 | 0 | 1 | 400000 | 4 | 0.5 | -143.647 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND001_CAP100000_NOT100000_CONC1_COST100 | CAND001 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | 100000 | 100000 | 1 | cost100 | 1 | 0 | 9 | 2 | 7 | 3 | 4 | 0 | 1 | 1 | 4 | 2 | 1 | 289.164 | 0.289164 | 72.8694 | 0 | 1 | 200000 | 2 | 0.777778 | 0 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND003_CAP100000_NOT50000_CONC1_COST100 | CAND003 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | 100000 | 50000 | 1 | cost100 | 1 | 0 | 11 | 5 | 6 | 2 | 4 | 0 | 1 | 1 | 7 | 5 | 1 | 272.758 | 0.272758 | 68.7351 | 0 | 1 | 250000 | 2.5 | 0.272727 | -64.4275 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND001_CAP100000_NOT100000_CONC1_COST100_PLUS_1BP | CAND001 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | 100000 | 100000 | 1 | cost100_plus_1bp | 1 | 1 | 9 | 2 | 7 | 3 | 4 | 0 | 1 | 1 | 4 | 2 | 1 | 269.164 | 0.269164 | 67.8294 | 0 | 1 | 200000 | 2 | 0.777778 | 0 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND017_CAP100000_NOT100000_CONC1_COST100 | CAND017 | P268_P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR_H10_IQ0p75_SQ0p75_SPMID | 100000 | 100000 | 1 | cost100 | 1 | 0 | 51 | 9 | 42 | 4 | 38 | 0 | 1 | 1 | 11 | 5 | 1 | 265.44 | 0.26544 | 66.8908 | 0 | 1 | 900000 | 9 | 0.823529 | -276.888 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND014_CAP100000_NOT100000_CONC1_COST100_PLUS_2BP | CAND014 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPCOMPRESSION | 100000 | 100000 | 1 | cost100_plus_2bp | 1 | 2 | 8 | 4 | 4 | 1 | 3 | 0 | 1 | 1 | 5 | 4 | 1 | 261.719 | 0.261719 | 65.9533 | 0 | 1 | 400000 | 4 | 0.5 | -163.647 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND001_CAP100000_NOT100000_CONC1_COST100_PLUS_2BP | CAND001 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | 100000 | 100000 | 1 | cost100_plus_2bp | 1 | 2 | 9 | 2 | 7 | 3 | 4 | 0 | 1 | 1 | 4 | 2 | 1 | 249.164 | 0.249164 | 62.7894 | 0 | 1 | 200000 | 2 | 0.777778 | 0 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND003_CAP100000_NOT50000_CONC1_COST100_PLUS_1BP | CAND003 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | 100000 | 50000 | 1 | cost100_plus_1bp | 1 | 1 | 11 | 5 | 6 | 2 | 4 | 0 | 1 | 1 | 7 | 5 | 1 | 247.758 | 0.247758 | 62.4351 | 0 | 1 | 250000 | 2.5 | 0.272727 | -71.8233 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND004_CAP100000_NOT50000_CONC1_COST100 | CAND004 | P268_P268_ASK_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPMID | 100000 | 50000 | 1 | cost100 | 1 | 0 | 15 | 6 | 9 | 2 | 7 | 0 | 1 | 1 | 7 | 4 | 1 | 246.476 | 0.246476 | 62.112 | 0 | 1 | 300000 | 3 | 0.3 | -56.4375 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND004_CAP100000_NOT100000_CONC1_COST150 | CAND004 | P268_P268_ASK_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPMID | 100000 | 100000 | 1 | cost150 | 1.5 | 0 | 15 | 6 | 9 | 2 | 7 | 0 | 1 | 1 | 7 | 4 | 1 | 244.908 | 0.244908 | 61.7169 | 0 | 1 | 600000 | 6 | 0.6 | -154.216 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND003_CAP100000_NOT50000_CONC1_COST100_PLUS_2BP | CAND003 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | 100000 | 50000 | 1 | cost100_plus_2bp | 1 | 2 | 11 | 5 | 6 | 2 | 4 | 0 | 1 | 1 | 7 | 5 | 1 | 222.758 | 0.222758 | 56.1351 | 0 | 1 | 250000 | 2.5 | 0.272727 | -81.8233 | 0 | 0 | 0 | 0 | 0 |
| P271_CAND003_CAP250000_NOT100000_CONC1_COST100 | CAND003 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | 250000 | 100000 | 1 | cost100 | 1 | 0 | 11 | 5 | 6 | 2 | 4 | 0 | 1 | 1 | 7 | 5 | 1 | 545.516 | 0.218207 | 54.988 | 0 | 1 | 500000 | 2 | 0.218182 | -128.855 | 0 | 0 | 0 | 0 | 0 |

## Proxy Reconciliation

| cost_profile | phase269_best_fixed_notional_proxy_candidate_id | phase269_best_cost100_fixed_notional_annualized_pct | best_phase271_scenario_id | phase271_best_mechanical_one_date_annualized_portfolio_return_pct | phase271_best_portfolio_return_pct | annualized_return_is_robust_portfolio_claim | reconciliation_note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cost100 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | 197.073 | P271_CAND003_CAP100000_NOT100000_CONC1_COST100 | 137.47 | 0.545516 | 0 | Phase269 proxy is not portfolio return; Phase271 applies fixed capital and scheduling to pooled and per-candidate scopes, still one-date mechanics only. |
| cost100_plus_1bp | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | 197.073 | P271_CAND003_CAP100000_NOT100000_CONC1_COST100_PLUS_1BP | 124.87 | 0.495516 | 0 | Phase269 proxy is not portfolio return; Phase271 applies fixed capital and scheduling to pooled and per-candidate scopes, still one-date mechanics only. |
| cost100_plus_2bp | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | 197.073 | P271_CAND003_CAP100000_NOT100000_CONC1_COST100_PLUS_2BP | 112.27 | 0.445516 | 0 | Phase269 proxy is not portfolio return; Phase271 applies fixed capital and scheduling to pooled and per-candidate scopes, still one-date mechanics only. |
| cost150 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | 197.073 | P271_CAND003_CAP100000_NOT100000_CONC1_COST150 | 85.381 | 0.338813 | 0 | Phase269 proxy is not portfolio return; Phase271 applies fixed capital and scheduling to pooled and per-candidate scopes, still one-date mechanics only. |
| cost200 | P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | 197.073 | P271_CAND003_CAP100000_NOT100000_CONC1_COST200 | 33.2918 | 0.13211 | 0 | Phase269 proxy is not portfolio return; Phase271 applies fixed capital and scheduling to pooled and per-candidate scopes, still one-date mechanics only. |

## Candidate Capacity Diagnostics

| candidate_id | family_id | cost_profile | scenario_rows | scheduled_event_rows | symbols | realized_net_pnl_inr | scheduled_notional_inr | avg_net_edge_bps | avg_depth_beyond_l1_qty_imbalance | avg_level_weighted_depth_imbalance | avg_spread_bps | return_on_scheduled_notional_bps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P268_P268_ASK_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPMID | P268_ASK_ABSORPTION_BREADTH_REPAIR | cost100 | 84 | 444 | 7 | 12834.7 | 2.105e+07 | 5.9992 | -0.572893 | -0.586593 | 2.77457 | 6.09726 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 84 | 408 | 7 | 6999.71 | 1.91875e+07 | 3.84206 | 0.566703 | 0.437788 | 2.59178 | 3.64806 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 84 | 252 | 4 | 6163.53 | 1.1525e+07 | 4.87348 | 0.546682 | 0.619466 | 4.47409 | 5.34796 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 96 | 504 | 6 | 331.266 | 2.37e+07 | -0.00697492 | 0.560464 | 0.476622 | 1.55972 | 0.139775 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p75_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 48 | 384 | 7 | 67.9043 | 1.84e+07 | 0.0278293 | 0.583238 | 0.477499 | 3.03226 | 0.0369045 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 48 | 264 | 5 | -980.942 | 1.27e+07 | -1.23431 | 0.543792 | 0.48597 | 2.87784 | -0.772395 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p75_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 48 | 276 | 5 | -2265.14 | 1.34e+07 | -1.54458 | 0.54635 | 0.425723 | 1.56114 | -1.6904 |
| P268_P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR_H10_IQ0p9_SQ0p75_SPMID | P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR | cost100 | 96 | 1128 | 11 | -2839.32 | 5.225e+07 | -0.348366 | -0.314117 | -0.335528 | 2.71615 | -0.54341 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p5_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 48 | 408 | 6 | -3535.46 | 1.975e+07 | -1.62607 | 0.561204 | 0.465746 | 1.56446 | -1.7901 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p6_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 48 | 324 | 5 | -3703.07 | 1.575e+07 | -2.22225 | 0.555259 | 0.445199 | 1.5598 | -2.35116 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPHIGH | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 48 | 84 | 2 | -4034.22 | 4e+06 | -10.7831 | 0.572696 | 0.573188 | 5.40086 | -10.0856 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 48 | 300 | 5 | -4169.87 | 1.435e+07 | -2.88043 | 0.556766 | 0.444773 | 1.54012 | -2.90583 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 48 | 408 | 8 | -6150.02 | 1.935e+07 | -3.0673 | 0.579392 | 0.487445 | 2.81297 | -3.17831 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 84 | 444 | 8 | -6804.99 | 2.1e+07 | -3.14045 | 0.571486 | 0.486005 | 2.7785 | -3.24047 |
| P268_P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR_H10_IQ0p75_SQ0p75_SPMID | P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR | cost100 | 96 | 1284 | 11 | -7251.54 | 5.8375e+07 | -1.32046 | -0.176859 | -0.153548 | 2.62324 | -1.24223 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPHIGH | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 60 | 300 | 7 | -10469.1 | 1.41375e+07 | -7.41705 | 0.568424 | 0.581964 | 3.95324 | -7.40518 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPHIGH | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100 | 84 | 276 | 6 | -12170.9 | 1.3e+07 | -9.449 | 0.613088 | 0.645949 | 4.0266 | -9.36225 |
| P268_P268_ASK_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPMID | P268_ASK_ABSORPTION_BREADTH_REPAIR | cost100_plus_1bp | 84 | 444 | 7 | 10729.7 | 2.105e+07 | 4.9992 | -0.572893 | -0.586593 | 2.77457 | 5.09726 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100_plus_1bp | 84 | 408 | 7 | 5080.96 | 1.91875e+07 | 2.84206 | 0.566703 | 0.437788 | 2.59178 | 2.64806 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p75_SPHIGH | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100_plus_1bp | 84 | 252 | 4 | 5011.03 | 1.1525e+07 | 3.87348 | 0.546682 | 0.619466 | 4.47409 | 4.34796 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p75_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100_plus_1bp | 48 | 384 | 7 | -1772.1 | 1.84e+07 | -0.972171 | 0.583238 | 0.477499 | 3.03226 | -0.963095 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p5_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100_plus_1bp | 96 | 504 | 6 | -2038.73 | 2.37e+07 | -1.00697 | 0.560464 | 0.476622 | 1.55972 | -0.860225 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100_plus_1bp | 48 | 264 | 5 | -2250.94 | 1.27e+07 | -2.23431 | 0.543792 | 0.48597 | 2.87784 | -1.7724 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p75_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100_plus_1bp | 48 | 276 | 5 | -3605.14 | 1.34e+07 | -2.54458 | 0.54635 | 0.425723 | 1.56114 | -2.6904 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p9_SPHIGH | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100_plus_1bp | 48 | 84 | 2 | -4434.22 | 4e+06 | -11.7831 | 0.572696 | 0.573188 | 5.40086 | -11.0856 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p6_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100_plus_1bp | 48 | 324 | 5 | -5278.07 | 1.575e+07 | -3.22225 | 0.555259 | 0.445199 | 1.5598 | -3.35116 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H6_IQ0p9_SQ0p5_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100_plus_1bp | 48 | 408 | 6 | -5510.46 | 1.975e+07 | -2.62607 | 0.561204 | 0.465746 | 1.56446 | -2.7901 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPLOW | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100_plus_1bp | 48 | 300 | 5 | -5604.87 | 1.435e+07 | -3.88043 | 0.556766 | 0.444773 | 1.54012 | -3.90583 |
| P268_P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR_H10_IQ0p9_SQ0p75_SPMID | P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR | cost100_plus_1bp | 96 | 1128 | 11 | -8064.32 | 5.225e+07 | -1.34837 | -0.314117 | -0.335528 | 2.71615 | -1.54341 |
| P268_P268_BID_ABSORPTION_BREADTH_REPAIR_H10_IQ0p9_SQ0p6_SPCOMPRESSION | P268_BID_ABSORPTION_BREADTH_REPAIR | cost100_plus_1bp | 48 | 408 | 8 | -8085.02 | 1.935e+07 | -4.0673 | 0.579392 | 0.487445 | 2.81297 | -4.17831 |

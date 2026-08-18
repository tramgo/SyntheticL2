# Phase481 Real-L2 Capacity Sensitivity Precommit

Phase481 freezes a no-download capacity sensitivity retest for the current 16-date real-L2 official-catalyst panel. It does not execute the retest.

The purpose is to determine whether the latest 25-trade result is caused by the capacity selector or by the signal economics themselves.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase481_real_l2_capacity_sensitivity_precommit_complete | 1 | Phase481 complete if all gates pass |
| phase481_thesis_id | P481_REAL_L2_CAPACITY_SENSITIVITY_PRECOMMIT | Phase481 thesis |
| phase481_local_real_l2_date_rows | 16 | Local dates used |
| phase481_input_work_order_rows | 273 | Frozen work-order rows |
| phase481_capacity_policy_rows | 5 | Frozen capacity policies |
| phase481_prior_scheduled_primary_candidates | 34 | Prior scheduled primary candidates |
| phase481_prior_capacity_selected_trades | 25 | Prior baseline selected trades |
| phase481_prior_net_pnl_inr | 992.965 | Prior baseline net PnL |
| phase481_prior_annualized_return_pct | 7.14935 | Prior baseline annualized return |
| phase481_strategy_retest_executed_now | 0 | Precommit only |
| phase481_download_executed_now | 0 | No download |
| phase481_strategy_promotion_allowed | 0 | No promotion |
| phase481_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase481_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase481_hard_gate_pass_rows | 9 | Passed hard gates |
| phase481_hard_gate_rows | 9 | Hard gates |
| phase481_next_best_action | execute_phase482_real_l2_capacity_sensitivity_no_search_no_download_no_paper_live | Recommended next action |

## Prior Evidence

| evidence_id | value | description |
| --- | --- | --- |
| phase480_local_real_l2_dates | 16 | Current local real-L2 dates. |
| phase480_full_32_symbol_days | 16 | Dates with all configured symbols present. |
| phase480_official_catalyst_overlap_dates | 16 | Official-catalyst overlap dates. |
| phase387_scheduled_primary_candidates | 34 | Scheduled candidates before capacity selection. |
| phase387_primary_selected_trades | 25 | Actual baseline capacity-selected trades. |
| phase387_primary_net_pnl_inr | 992.965 | Actual baseline net PnL. |
| phase387_primary_annualized_return_pct | 7.14935 | Actual baseline annualized return. |
| phase388_capacity_selected_gap | 5 | Remaining trade gap to 30 selected trades. |
| phase388_acceptance_candidate | 0 | Acceptance remains closed. |

## Capacity Policy Catalog

| capacity_policy_id | policy_role | selection_rule | max_concurrent_positions | per_symbol_date_cap | per_trade_date_cap | all_ready_events | acceptance_role |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P481_BASELINE_MAX3_CONCURRENT | baseline | reproduce Phase387 apply_capacity: sort by decision_ms, canonical_work_order_id; keep if active exits < 3 | 3 |  |  | 0 | primary |
| P481_MAX5_CONCURRENT | looser_capacity | same active-exit overlap logic as baseline but max concurrent positions = 5 | 5 |  |  | 0 | sensitivity |
| P481_ONE_PER_SYMBOL_DATE | breadth_first | after readiness and signal filters, keep earliest candidate per scenario, diagnostic_trade_date, symbol |  | 1 |  | 0 | sensitivity |
| P481_TWO_PER_TRADE_DATE | date_balanced | after readiness and signal filters, keep earliest two candidates per scenario and diagnostic_trade_date |  |  | 2 | 0 | sensitivity |
| P481_ALL_READY_DIAGNOSTIC | upper_bound_diagnostic | select every scheduled ready candidate; not sufficient alone for acceptance because it ignores capital overlap |  |  |  | 1 | diagnostic_only |

## Execution Contract

| contract_key | contract_value | description |
| --- | --- | --- |
| contract_id | P481_REAL_L2_CAPACITY_SENSITIVITY_PRECOMMIT | Frozen Phase481 contract identifier. |
| input_work_order | outputs\phase400\phase386_phase360_execution_work_order.csv | Use the latest 16-date adapted official-catalyst work order. |
| input_work_order_rows | 273 | Expected rows in frozen work order. |
| input_trade_ledger | outputs\phase401\phase387_trade_ledger.csv | Reuse Phase401 event/trade features; do not rebuild signal after seeing capacity outcomes. |
| scheduled_primary_candidates | 34 | Current primary scheduled candidate count before capacity policy. |
| primary_scenario_id | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | Frozen reversal-control scenario. |
| side_flip_control_scenario_id | P362_D120_I2p5_D0p25_R0p0_CONTINUATION | Frozen continuation side-flip control. |
| cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha cost model. |
| cost_multiplier | 2 | Cost200 remains required. |
| minimum_selected_trades | 30 | Event floor cannot be softened. |
| annualized_return_floor_pct | 12 | User research profitability bar retained. |
| full_depth_required | L1 plus top-five market-by-price depth; levels 2-5 materiality retained | Core project objective. |
| no_download_allowed | 1 | Use current local 16-date panel first. |
| parameter_search_allowed | 0 | No post-result tuning. |
| paper_live_or_profit_claim_allowed | 0 | Boundaries closed. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P481_PHASE480_COMPLETE | True | 1 | 1 | hard |
| P481_CURRENT_16_DATE_PANEL_USED | True | 16 | >=16 | hard |
| P481_WORK_ORDER_PRESENT | True | 273 | >=273 | hard |
| P481_PRIOR_TRADE_LEDGER_PRESENT | True | 34 | >0 | hard |
| P481_CAPACITY_POLICY_GRID_FROZEN | True | 5 | 5 | hard |
| P481_FULL_DEPTH_L2_L5_RETAINED | True | 1 | 1 | hard |
| P481_COST200_RETAINED | True | 1 | 1 | hard |
| P481_NO_DOWNLOAD_OR_RETEST_NOW | True | download=0;retest=0 | both_zero | hard |
| P481_NO_PROMOTION_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: no download, no retest in this phase, no strategy promotion, no paper/live, no deployable profitability claim.

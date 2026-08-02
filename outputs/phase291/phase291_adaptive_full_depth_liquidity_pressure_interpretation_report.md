# Phase291 Adaptive Full-Depth Liquidity-Pressure Interpretation

Phase291 interprets Phase290 as a high-annualized but too-sparse adaptive pressure spark and selects breadth repair as the next route.

No replay, promotion, paper/live acceptance, or deployable profitability claim is opened.

## Phase290 Summary

| metric | value | description |
| --- | --- | --- |
| phase290_adaptive_liquidity_pressure_search_complete | 1 | Phase290 adaptive full-depth liquidity-pressure expansion search completed |
| phase290_selected_route | P290_ADAPTIVE_FULL_DEPTH_LIQUIDITY_PRESSURE_EXPANSION_SEARCH | Selected route |
| phase290_variant_rows | 246 | Adaptive variants evaluated |
| phase290_scenario_rows | 984 | Cost200 fixed-capital scenarios evaluated |
| phase290_sparse_above12_scenario_rows | 0 | Above-12 sparse diagnostic rows with event floor met |
| phase290_robust_portfolio_floor_scenario_rows | 0 | Scenarios meeting robust portfolio event floor |
| phase290_robust_portfolio_above12_scenario_rows | 0 | Robust floor scenarios above 12 percent |
| phase290_best_variant_id | P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_INV_H10 | Best Phase290 variant |
| phase290_best_adaptive_family | exhaustion_reversal_adaptive | Best adaptive family |
| phase290_best_primary_pressure_column | depth_withdrawal_pressure | Best primary pressure feature |
| phase290_best_interaction_column | churn_withdraw_interaction | Best interaction feature |
| phase290_best_side_mode | INV | Best side mode |
| phase290_best_market_bucket | OPEN | Best market bucket |
| phase290_best_cost200_annualized_pct | 28.55657959303009 | Best cost200 fixed-capital annualized diagnostic |
| phase290_best_realized_net_pnl_inr | 113.31976028980193 | Best realized net P&L |
| phase290_best_scheduled_event_rows | 1 | Best scheduled event rows |
| phase290_l1_only_variant_rows | 0 | L1-only variants |
| phase290_net_edge_live_mask_rows | 0 | Live masks using net/gross edge |
| phase290_strategy_replay_allowed | 0 | No strategy replay unlocked |
| phase290_strategy_promotion_allowed | 0 | No strategy promotion unlocked |
| phase290_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance |
| phase290_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase290_hard_gate_pass_rows | 8 | Hard gates passed |
| phase290_hard_gate_rows | 8 | Hard gates evaluated |
| phase290_next_best_action | run_phase291_adaptive_full_depth_liquidity_pressure_interpretation_no_paper_live | Recommended next milestone |

## Ranked Adaptive Interpretation

| phase290_variant_id | adaptive_family | primary_pressure_column | interaction_column | spread_state | market_bucket | side_mode | exit_horizon_ticks | scenario_rows | selected_event_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_scenario_id | best_initial_capital_inr | best_fixed_notional_inr | best_max_concurrent_positions | best_notional_turnover_x_initial_capital | best_avg_open_notional_utilization | rejected_same_symbol_overlap_rows | rejected_max_concurrent_rows | uses_top5 | uses_levels_2_to_5 | l1_only_variant | uses_net_edge_as_live_mask | annualized_above12_but_too_sparse | positive_but_below12 | too_sparse_for_sparse_diagnostic | too_sparse_for_portfolio_claim | full_depth_positive_clue | same_adaptive_route_exhausted_for_acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_INV_H10 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | OPEN | INV | 10 | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 14.2783 | 14.2783 | 28.5566 | 113.32 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_INV_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_PRESSURE_SIGN_REV_H10 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | OPEN | PRESSURE_SIGN_REV | 10 | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 14.2783 | 14.2783 | 28.5566 | 113.32 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_PRESSURE_SIGN_REV_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_INV_H8 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | OPEN | INV | 8 | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 10.58 | 10.58 | 21.1599 | 83.9679 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_INV_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_PRESSURE_SIGN_REV_H8 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | OPEN | PRESSURE_SIGN_REV | 8 | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 10.58 | 10.58 | 21.1599 | 83.9679 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_PRESSURE_SIGN_REV_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_ANYSPREAD_OPEN_INV_H10 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | ANYSPREAD | OPEN | INV | 10 | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0.952027 | 4.99761 | 8.09117 | 64.2157 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_ANYSPREAD_OPEN_INV_H10_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 0.25 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_ANYSPREAD_OPEN_PRESSURE_SIGN_REV_H10 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | ANYSPREAD | OPEN | PRESSURE_SIGN_REV | 10 | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0.952027 | 4.99761 | 8.09117 | 64.2157 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_ANYSPREAD_OPEN_PRESSURE_SIGN_REV_H10_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 0.25 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_INV_H5 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | OPEN | INV | 5 | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 4.01792 | 4.01792 | 8.03584 | 31.8882 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_INV_H5_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_PRESSURE_SIGN_REV_H5 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | OPEN | PRESSURE_SIGN_REV | 5 | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 4.01792 | 4.01792 | 8.03584 | 31.8882 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_PRESSURE_SIGN_REV_H5_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P45_S45_I55_NOTWIDE_OPEN_INV_H10 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | OPEN | INV | 10 | 4 | 5 | 2 | 0 | 0 | 0 | 0 | 2.87096 | 5.7335 | 5.74191 | 113.927 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P45_S45_I55_NOTWIDE_OPEN_INV_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.8 | 0 | 4 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P45_S45_I55_NOTWIDE_OPEN_PRESSURE_SIGN_REV_H10 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | OPEN | PRESSURE_SIGN_REV | 10 | 4 | 5 | 2 | 0 | 0 | 0 | 0 | 2.87096 | 5.7335 | 5.74191 | 113.927 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P45_S45_I55_NOTWIDE_OPEN_PRESSURE_SIGN_REV_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.8 | 0 | 4 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P45_S45_I55_NOTWIDE_ALL_ORIG_H10 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | ALL | ORIG | 10 | 4 | 133 | 2 | 0 | 0 | 0 | 0 | 2.58189 | 5.15792 | 5.16379 | 163.93 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P45_S45_I55_NOTWIDE_ALL_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.992481 | 29 | 117 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_ALL_ORIG_H10 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | ALL | ORIG | 10 | 4 | 98 | 2 | 0 | 0 | 0 | 0 | 2.57679 | 5.14716 | 5.15357 | 163.605 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_ALL_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.989796 | 21 | 88 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_ANYSPREAD_OPEN_INV_H8 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | ANYSPREAD | OPEN | INV | 8 | 4 | 2 | 2 | 0 | 0 | 0 | 0 | -0.493117 | 2.39843 | 5.04342 | 40.0271 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_ANYSPREAD_OPEN_INV_H8_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 0.25 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_ANYSPREAD_OPEN_PRESSURE_SIGN_REV_H8 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | ANYSPREAD | OPEN | PRESSURE_SIGN_REV | 8 | 4 | 2 | 2 | 0 | 0 | 0 | 0 | -0.493117 | 2.39843 | 5.04342 | 40.0271 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_ANYSPREAD_OPEN_PRESSURE_SIGN_REV_H8_CAP100000_NOT50000_CONC2_COST200 | 100000 | 50000 | 2 | 1 | 0.25 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P45_S45_I55_NOTWIDE_OPEN_INV_H8 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | OPEN | INV | 8 | 4 | 5 | 2 | 0 | 0 | 0 | 0 | 2.13236 | 4.25524 | 4.26473 | 84.6176 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P45_S45_I55_NOTWIDE_OPEN_INV_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.8 | 0 | 4 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P45_S45_I55_NOTWIDE_OPEN_PRESSURE_SIGN_REV_H8 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | OPEN | PRESSURE_SIGN_REV | 8 | 4 | 5 | 2 | 0 | 0 | 0 | 0 | 2.13236 | 4.25524 | 4.26473 | 84.6176 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P45_S45_I55_NOTWIDE_OPEN_PRESSURE_SIGN_REV_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.8 | 0 | 4 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P45_S45_I55_NOTWIDE_ALL_ORIG_H8 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | ALL | ORIG | 8 | 4 | 133 | 2 | 0 | 0 | 0 | 0 | 2.0314 | 4.05705 | 4.0628 | 128.978 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P45_S45_I55_NOTWIDE_ALL_ORIG_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.992481 | 29 | 117 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_ALL_ORIG_H8 | exhaustion_reversal_adaptive | depth_withdrawal_pressure | churn_withdraw_interaction | NOTWIDE | ALL | ORIG | 8 | 4 | 98 | 2 | 0 | 0 | 0 | 0 | 2.02629 | 4.04629 | 4.05258 | 128.653 | P271_P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_ALL_ORIG_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.989796 | 21 | 88 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_REPLENISHMENT_ABSORPTION_ADAPTIVE_P45_S45_I55_ANYSPREAD_ALL_ORIG_H10 | replenishment_absorption_adaptive | replenishment_dominance | spread_compression_score | ANYSPREAD | ALL | ORIG | 10 | 4 | 109 | 2 | 0 | 0 | 0 | 0 | 1.88029 | 1.9502 | 4.04021 | 128.261 | P271_P290_P290_REPLENISHMENT_ABSORPTION_ADAPTIVE_P45_S45_I55_ANYSPREAD_ALL_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.990826 | 8 | 105 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P290_P290_REPLENISHMENT_ABSORPTION_ADAPTIVE_P45_S45_I55_ANYSPREAD_ALL_PRESSURE_SIGN_CONT_H10 | replenishment_absorption_adaptive | replenishment_dominance | spread_compression_score | ANYSPREAD | ALL | PRESSURE_SIGN_CONT | 10 | 4 | 109 | 2 | 0 | 0 | 0 | 0 | 1.88029 | 1.9502 | 4.04021 | 128.261 | P271_P290_P290_REPLENISHMENT_ABSORPTION_ADAPTIVE_P45_S45_I55_ANYSPREAD_ALL_PRESSURE_SIGN_CONT_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.990826 | 8 | 105 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |

## Family Interpretation

| adaptive_family | variant_rows | scenario_rows | selected_event_rows_max | max_scheduled_event_rows | above12_but_too_sparse_variants | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_variant_id | full_depth_positive_clue_variants | preserve_breadth_repair_clue | close_family_for_acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| exhaustion_reversal_adaptive | 72 | 288 | 285 | 3 | 4 | 0 | 0 | 0 | 0 | -111.568 | -6.25451 | 28.5566 | 163.93 | P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_INV_H10 | 32 | 1 | 1 |
| replenishment_absorption_adaptive | 54 | 216 | 109 | 2 | 0 | 0 | 0 | 0 | 0 | -14.3078 | -0.287694 | 4.04021 | 128.261 | P290_P290_REPLENISHMENT_ABSORPTION_ADAPTIVE_P45_S45_I55_ANYSPREAD_ALL_ORIG_H10 | 24 | 0 | 1 |
| pressure_continuation_adaptive | 72 | 288 | 221 | 10 | 0 | 0 | 0 | 12 | 0 | -38.3974 | -4.78617 | 2.38046 | 75.57 | P290_P290_PRESSURE_CONTINUATION_ADAPTIVE_P45_S45_I55_NOTWIDE_ALL_ORIG_H8 | 4 | 0 | 1 |
| liquidity_vacuum_adaptive | 48 | 192 | 163 | 4 | 0 | 0 | 0 | 0 | 0 | -19.8069 | -4.27044 | 0.476207 | 15.1177 | P290_P290_LIQUIDITY_VACUUM_ADAPTIVE_P65_S55_I55_ANYSPREAD_ALL_ORIG_H10 | 7 | 0 | 1 |

## Interpretation Ledger

| finding_id | evidence | severity | finding_present | interpretation |
| --- | --- | --- | --- | --- |
| phase290_executed | scenario_rows=984 | evidence | 1 | Phase290 executed adaptive full-depth pressure expansion. |
| above12_spark_exists_but_too_sparse | best_ann=28.55657959303009;best_events=1;spark_variants=4 | research_clue | 1 | The high annualized result is a spark, not an accepted strategy. |
| no_sparse_above12_survivor | sparse_above12_rows=0 | hard_negative | 1 | No Phase290 scenario met both >12% and the sparse event floor. |
| no_robust_portfolio_survivor | robust_floor_rows=0;robust_above12_rows=0 | hard_negative | 1 | No robust portfolio evidence exists. |
| full_depth_boundary_preserved | l1_only=0;live_label_leakage=0 | constraint | 1 | Full-depth and no-live-leakage boundaries held. |
| same_adaptive_route_should_close_for_acceptance | event_floor_failed | decision | 1 | Do not accept the one-event adaptive spark. |
| next_route_should_repair_breadth | P291_ADAPTIVE_PRESSURE_BREADTH_REPAIR_SEARCH | next_action | 1 | Search whether adaptive pressure clues can be broadened without relaxing cost/capital rules. |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| close_phase290_adaptive_route_for_acceptance | 1 | best_ann=28.55657959303009;best_events=1;event_floor=8 | Do not accept, replay, or promote Phase290. |
| preserve_best_adaptive_pressure_spark | P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_INV_H10 | family=exhaustion_reversal_adaptive;interaction=churn_withdraw_interaction;scheduled_events=1 | Carry forward only as a breadth-repair clue. |
| preserved_families_for_breadth_repair | exhaustion_reversal_adaptive | above-12 but too sparse or positive diagnostics | Preserve families as search context, not as accepted strategies. |
| do_not_relax_annualized_denominator | 1 | fixed_initial_capital_required | Annualized return remains fixed-capital based. |
| do_not_claim_portfolio_return | 1 | best_scheduled_events=1;robust_floor=30 | Evidence is too sparse for a portfolio-return claim. |
| selected_next_route | P291_ADAPTIVE_PRESSURE_BREADTH_REPAIR_SEARCH | adaptive route found spark but failed breadth | Run adaptive pressure breadth repair. |

## Phase292 Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P292_INPUTS | outputs/phase277/phase277_cost200_redesign_event_universe.csv;outputs/phase290/phase290_adaptive_pressure_scenario_results.csv;outputs/phase290/phase290_adaptive_pressure_variant_summary.csv | Use event universe plus Phase290 spark evidence. |
| P292_PRESERVED_PHASE290_SPARKS | P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_INV_H10;P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_PRESSURE_SIGN_REV_H10;P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_INV_H8;P290_P290_EXHAUSTION_REVERSAL_ADAPTIVE_P65_S55_I55_NOTWIDE_OPEN_PRESSURE_SIGN_REV_H8 | Carry forward above-12 but too-sparse adaptive variants only as breadth-repair clues. |
| P292_PRESERVED_ADAPTIVE_FAMILIES | exhaustion_reversal_adaptive | Keep adaptive families with sparks for breadth repair. |
| P292_SEARCH_TYPE | adaptive_pressure_breadth_repair_search | Broaden event counts while preserving observable full-depth L2 masks. |
| P292_REQUIRED_DIRECTIONS | looser_but_feature_only_thresholds;family_context_transfer;open_to_all_bucket_transfer;horizon_and_concurrency_breadth;cost200_fixed_capital_scheduler | Repair breadth without using future labels as live masks. |
| P292_CAPITAL_AND_COST | initial_capital_100000;cost200_required;fixed_notional_grid;max_concurrent_grid;annualized_denominator_fixed_capital | No unlimited-capital annualized return. |
| P292_ACCEPTANCE_DIAGNOSTICS | cost200_annualized_pct_gt_12.0;scheduled_event_rows_ge_8_for_sparse_discovery;scheduled_event_rows_ge_30_for_portfolio_claim | Sparse >12% remains discovery only; robust portfolio claim needs a larger event floor. |
| P292_BOUNDARY | no_paper_live;no_strategy_replay;no_deployable_profitability_claim;l1_only_forbidden;net_edge_live_mask_forbidden | Boundaries remain closed until evidence earns them. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P291_PHASE290_SEARCH_COMPLETE | True | 1 | Phase290 search complete | hard |
| P291_PHASE290_NEXT_ACTION_PRESENT | True | run_phase291_adaptive_full_depth_liquidity_pressure_interpretation_no_paper_live | Phase290 routes to Phase291 interpretation | hard |
| P291_PHASE290_GATES_PASS | True | 8/8 | Phase290 gates pass | hard |
| P291_RANKED_INTERPRETATION_PRESENT | True | 246 | >0 ranked variants | hard |
| P291_CLOSES_PHASE290_FOR_ACCEPTANCE | True | 1 | Phase290 closed for acceptance | hard |
| P291_NEXT_ROUTE_SELECTED | True | P291_ADAPTIVE_PRESSURE_BREADTH_REPAIR_SEARCH | P291_ADAPTIVE_PRESSURE_BREADTH_REPAIR_SEARCH | hard |
| P291_FULL_DEPTH_BOUNDARY_PRESERVED | True | l1_only=0;live_mask=0 | full-depth, no leakage | hard |
| P291_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |
| P291_ROUTE_CONTRACT_PRESENT | True | 8 | Phase292 route contract rows | hard |

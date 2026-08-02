# Phase289 Full-Depth Liquidity-Pressure Interpretation

Phase289 interprets Phase288 as a no-survivor fixed-grid pressure search and selects adaptive full-depth liquidity-pressure expansion as the next route.

No replay, promotion, paper/live acceptance, or deployable profitability claim is opened.

## Phase288 Summary

| metric | value | description |
| --- | --- | --- |
| phase288_liquidity_pressure_search_complete | 1 | Phase288 direct full-depth liquidity-pressure search completed |
| phase288_selected_route | P288_FULL_DEPTH_LIQUIDITY_PRESSURE_STRATEGY_SEARCH | Selected route |
| phase288_variant_rows | 192 | Variants evaluated |
| phase288_scenario_rows | 2304 | Cost200 fixed-capital scenarios evaluated |
| phase288_sparse_above12_scenario_rows | 0 | Above-12 sparse diagnostic rows with event floor met |
| phase288_robust_portfolio_floor_scenario_rows | 0 | Scenarios meeting robust portfolio event floor |
| phase288_robust_portfolio_above12_scenario_rows | 0 | Robust floor scenarios above 12 percent |
| phase288_best_variant_id | P288_P288_EXHAUSTION_REVERSAL_Q70_ORIG_H10 | Best Phase288 variant |
| phase288_best_liquidity_family | exhaustion_reversal | Best liquidity family |
| phase288_best_pressure_column | depth_withdrawal_pressure | Best pressure feature |
| phase288_best_side_mode | ORIG | Best side mode |
| phase288_best_cost200_annualized_pct | 5.391389753841644 | Best cost200 fixed-capital annualized diagnostic |
| phase288_best_realized_net_pnl_inr | 171.15523028068714 | Best realized net P&L |
| phase288_best_scheduled_event_rows | 1 | Best scheduled event rows |
| phase288_l1_only_variant_rows | 0 | L1-only variants |
| phase288_net_edge_live_mask_rows | 0 | Live masks using net/gross edge |
| phase288_strategy_replay_allowed | 0 | No strategy replay unlocked |
| phase288_strategy_promotion_allowed | 0 | No strategy promotion unlocked |
| phase288_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance |
| phase288_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase288_hard_gate_pass_rows | 8 | Hard gates passed |
| phase288_hard_gate_rows | 8 | Hard gates evaluated |
| phase288_next_best_action | run_phase289_full_depth_liquidity_pressure_interpretation_no_paper_live | Recommended next milestone |

## Ranked Pressure Interpretation

| phase288_variant_id | liquidity_family | pressure_column | side_mode | exit_horizon_ticks | scenario_rows | selected_event_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_scenario_id | best_initial_capital_inr | best_fixed_notional_inr | best_max_concurrent_positions | best_notional_turnover_x_initial_capital | best_avg_open_notional_utilization | rejected_same_symbol_overlap_rows | rejected_max_concurrent_rows | uses_top5 | uses_levels_2_to_5 | l1_only_variant | uses_net_edge_as_live_mask | positive_but_below12 | too_sparse_for_sparse_diagnostic | too_sparse_for_portfolio_claim | full_depth_positive_clue | same_pressure_route_exhausted_for_acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P288_P288_EXHAUSTION_REVERSAL_Q50_ORIG_H10 | exhaustion_reversal | depth_withdrawal_pressure | ORIG | 10 | 12 | 109 | 4 | 0 | 0 | 0 | 0 | 0.33799 | 2.64069 | 5.39139 | 171.155 | P271_P288_P288_EXHAUSTION_REVERSAL_Q50_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.990826 | 49 | 96 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_EXHAUSTION_REVERSAL_Q60_ORIG_H10 | exhaustion_reversal | depth_withdrawal_pressure | ORIG | 10 | 12 | 87 | 4 | 0 | 0 | 0 | 0 | 0.33799 | 2.64069 | 5.39139 | 171.155 | P271_P288_P288_EXHAUSTION_REVERSAL_Q60_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.988506 | 42 | 76 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_EXHAUSTION_REVERSAL_Q70_ORIG_H10 | exhaustion_reversal | depth_withdrawal_pressure | ORIG | 10 | 12 | 65 | 4 | 0 | 0 | 0 | 0 | 0.33799 | 2.64069 | 5.39139 | 171.155 | P271_P288_P288_EXHAUSTION_REVERSAL_Q70_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.984615 | 31 | 56 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_EXHAUSTION_REVERSAL_Q80_ORIG_H10 | exhaustion_reversal | depth_withdrawal_pressure | ORIG | 10 | 12 | 44 | 4 | 0 | 0 | 0 | 0 | 0.33799 | 2.64069 | 5.39139 | 171.155 | P271_P288_P288_EXHAUSTION_REVERSAL_Q80_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.977273 | 18 | 41 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_EXHAUSTION_REVERSAL_Q50_ORIG_H8 | exhaustion_reversal | depth_withdrawal_pressure | ORIG | 8 | 12 | 109 | 4 | 0 | 0 | 0 | 0 | -0.267878 | 2.07625 | 4.25312 | 135.02 | P271_P288_P288_EXHAUSTION_REVERSAL_Q50_ORIG_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.990826 | 49 | 96 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_EXHAUSTION_REVERSAL_Q60_ORIG_H8 | exhaustion_reversal | depth_withdrawal_pressure | ORIG | 8 | 12 | 87 | 4 | 0 | 0 | 0 | 0 | -0.267878 | 2.07625 | 4.25312 | 135.02 | P271_P288_P288_EXHAUSTION_REVERSAL_Q60_ORIG_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.988506 | 42 | 76 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_EXHAUSTION_REVERSAL_Q70_ORIG_H8 | exhaustion_reversal | depth_withdrawal_pressure | ORIG | 8 | 12 | 65 | 4 | 0 | 0 | 0 | 0 | -0.267878 | 2.07625 | 4.25312 | 135.02 | P271_P288_P288_EXHAUSTION_REVERSAL_Q70_ORIG_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.984615 | 31 | 56 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_EXHAUSTION_REVERSAL_Q80_ORIG_H8 | exhaustion_reversal | depth_withdrawal_pressure | ORIG | 8 | 12 | 44 | 4 | 0 | 0 | 0 | 0 | -0.267878 | 2.07625 | 4.25312 | 135.02 | P271_P288_P288_EXHAUSTION_REVERSAL_Q80_ORIG_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.977273 | 18 | 41 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_REPLENISHMENT_ABSORPTION_Q50_ORIG_H10 | replenishment_absorption | replenishment_dominance | ORIG | 10 | 12 | 29 | 4 | 0 | 0 | 0 | 0 | 0.985227 | 1.57911 | 3.94091 | 125.108 | P271_P288_P288_REPLENISHMENT_ABSORPTION_Q50_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.965517 | 11 | 26 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_REPLENISHMENT_ABSORPTION_Q60_ORIG_H10 | replenishment_absorption | replenishment_dominance | ORIG | 10 | 12 | 23 | 4 | 0 | 0 | 0 | 0 | 0.985227 | 1.57911 | 3.94091 | 125.108 | P271_P288_P288_REPLENISHMENT_ABSORPTION_Q60_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.956522 | 9 | 20 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_REPLENISHMENT_ABSORPTION_Q70_ORIG_H10 | replenishment_absorption | replenishment_dominance | ORIG | 10 | 12 | 18 | 4 | 0 | 0 | 0 | 0 | 0.985227 | 1.57911 | 3.94091 | 125.108 | P271_P288_P288_REPLENISHMENT_ABSORPTION_Q70_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.944444 | 5 | 17 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_SPREAD_COMPRESSION_PRESSURE_Q50_ORIG_H10 | spread_compression_pressure | replenishment_dominance | ORIG | 10 | 12 | 38 | 4 | 0 | 0 | 0 | 0 | 0.985227 | 1.57911 | 3.94091 | 125.108 | P271_P288_P288_SPREAD_COMPRESSION_PRESSURE_Q50_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.973684 | 16 | 34 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_SPREAD_COMPRESSION_PRESSURE_Q60_ORIG_H10 | spread_compression_pressure | replenishment_dominance | ORIG | 10 | 12 | 30 | 4 | 0 | 0 | 0 | 0 | 0.985227 | 1.57911 | 3.94091 | 125.108 | P271_P288_P288_SPREAD_COMPRESSION_PRESSURE_Q60_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.966667 | 11 | 27 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_SPREAD_COMPRESSION_PRESSURE_Q70_ORIG_H10 | spread_compression_pressure | replenishment_dominance | ORIG | 10 | 12 | 23 | 4 | 0 | 0 | 0 | 0 | 0.985227 | 1.57911 | 3.94091 | 125.108 | P271_P288_P288_SPREAD_COMPRESSION_PRESSURE_Q70_ORIG_H10_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.956522 | 9 | 20 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_REPLENISHMENT_ABSORPTION_Q50_ORIG_H8 | replenishment_absorption | replenishment_dominance | ORIG | 8 | 12 | 29 | 4 | 0 | 0 | 0 | 0 | 0.512441 | 1.06207 | 2.97494 | 94.4424 | P271_P288_P288_REPLENISHMENT_ABSORPTION_Q50_ORIG_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.965517 | 11 | 26 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_REPLENISHMENT_ABSORPTION_Q60_ORIG_H8 | replenishment_absorption | replenishment_dominance | ORIG | 8 | 12 | 23 | 4 | 0 | 0 | 0 | 0 | 0.512441 | 1.06207 | 2.97494 | 94.4424 | P271_P288_P288_REPLENISHMENT_ABSORPTION_Q60_ORIG_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.956522 | 9 | 20 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_REPLENISHMENT_ABSORPTION_Q70_ORIG_H8 | replenishment_absorption | replenishment_dominance | ORIG | 8 | 12 | 18 | 4 | 0 | 0 | 0 | 0 | 0.512441 | 1.06207 | 2.97494 | 94.4424 | P271_P288_P288_REPLENISHMENT_ABSORPTION_Q70_ORIG_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.944444 | 5 | 17 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_SPREAD_COMPRESSION_PRESSURE_Q50_ORIG_H8 | spread_compression_pressure | replenishment_dominance | ORIG | 8 | 12 | 38 | 4 | 0 | 0 | 0 | 0 | 0.512441 | 1.06207 | 2.97494 | 94.4424 | P271_P288_P288_SPREAD_COMPRESSION_PRESSURE_Q50_ORIG_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.973684 | 16 | 34 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_SPREAD_COMPRESSION_PRESSURE_Q60_ORIG_H8 | spread_compression_pressure | replenishment_dominance | ORIG | 8 | 12 | 30 | 4 | 0 | 0 | 0 | 0 | 0.512441 | 1.06207 | 2.97494 | 94.4424 | P271_P288_P288_SPREAD_COMPRESSION_PRESSURE_Q60_ORIG_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.966667 | 11 | 27 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| P288_P288_SPREAD_COMPRESSION_PRESSURE_Q70_ORIG_H8 | spread_compression_pressure | replenishment_dominance | ORIG | 8 | 12 | 23 | 4 | 0 | 0 | 0 | 0 | 0.512441 | 1.06207 | 2.97494 | 94.4424 | P271_P288_P288_SPREAD_COMPRESSION_PRESSURE_Q70_ORIG_H8_CAP100000_NOT100000_CONC1_COST200 | 100000 | 100000 | 1 | 1 | 0.956522 | 9 | 20 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |

## Family Interpretation

| liquidity_family | variant_rows | scenario_rows | selected_event_rows_max | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_variant_id | positive_but_below12_variants | full_depth_positive_clue_variants | preserve_adaptive_expansion_clue | close_family_for_acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| exhaustion_reversal | 32 | 384 | 109 | 6 | 0 | 0 | 0 | 0 | -16.9013 | -5.15563 | 5.39139 | 171.155 | P288_P288_EXHAUSTION_REVERSAL_Q50_ORIG_H10 | 16 | 16 | 1 | 1 |
| replenishment_absorption | 32 | 384 | 29 | 4 | 0 | 0 | 0 | 0 | -14.391 | -5.79538 | 3.94091 | 125.108 | P288_P288_REPLENISHMENT_ABSORPTION_Q50_ORIG_H10 | 10 | 10 | 1 | 1 |
| spread_compression_pressure | 32 | 384 | 38 | 4 | 0 | 0 | 0 | 0 | -14.3587 | -5.58979 | 3.94091 | 125.108 | P288_P288_SPREAD_COMPRESSION_PRESSURE_Q50_ORIG_H10 | 10 | 10 | 1 | 1 |
| pressure_continuation | 32 | 384 | 111 | 12 | 0 | 0 | 72 | 0 | -35.7566 | -9.20729 | 2.62604 | 83.3665 | P288_P288_PRESSURE_CONTINUATION_Q50_ORIG_H10 | 12 | 12 | 1 | 1 |
| liquidity_vacuum | 32 | 384 | 73 | 7 | 0 | 0 | 0 | 0 | -15.4261 | -6.82114 | 0.434236 | 13.7853 | P288_P288_LIQUIDITY_VACUUM_Q50_ORIG_H10 | 4 | 4 | 1 | 1 |
| open_pressure_burst | 32 | 384 | 55 | 5 | 0 | 0 | 0 | 0 | -11.0028 | -5.87343 | 0.350327 | 11.1215 | P288_P288_OPEN_PRESSURE_BURST_Q50_INV_H10 | 4 | 4 | 1 | 1 |

## Interpretation Ledger

| finding_id | evidence | severity | finding_present | interpretation |
| --- | --- | --- | --- | --- |
| phase288_executed | scenario_rows=2304 | evidence | 1 | Phase288 executed the direct full-depth liquidity-pressure strategy search. |
| no_sparse_above12_survivor | sparse_above12_rows=0;best_ann=5.391389753841644 | hard_negative | 1 | No Phase288 scenario crossed the fixed-capital >12% sparse diagnostic threshold. |
| no_robust_portfolio_survivor | robust_floor_rows=0;robust_above12_rows=0;best_events=1 | hard_negative | 1 | No Phase288 scenario met robust breadth or robust above-12 evidence. |
| best_case_too_sparse | best_ann=5.391389753841644;best_scheduled_events=1 | risk | 1 | The best Phase288 result is below threshold and too sparse. |
| full_depth_boundary_preserved | l1_only=0;live_label_leakage=0;positive_full_depth_clues=56 | constraint | 1 | Full top-five depth and no-live-leakage boundaries held. |
| same_pressure_route_should_close_for_acceptance | cost200_above12=0;robust_above12=0 | decision | 1 | Do not accept the fixed-grid Phase288 pressure route. |
| next_route_should_expand_pressure_family_adaptively | P289_ADAPTIVE_FULL_DEPTH_LIQUIDITY_PRESSURE_EXPANSION_SEARCH | next_action | 1 | Move to adaptive thresholds and family-specific pressure interactions instead of repeating the fixed grid. |

## Decision Ledger

| decision_id | decision_value | evidence | description |
| --- | --- | --- | --- |
| close_phase288_pressure_route_for_acceptance | 1 | sparse_above12=0;best_ann=5.391389753841644;best_events=1 | Do not accept, replay, or promote Phase288 pressure variants. |
| preserve_best_full_depth_pressure_clue | P288_P288_EXHAUSTION_REVERSAL_Q50_ORIG_H10 | family=exhaustion_reversal;pressure=depth_withdrawal_pressure;scheduled_events=1 | Carry forward only as a clue for adaptive expansion. |
| preserved_pressure_families_for_expansion | exhaustion_reversal;replenishment_absorption;spread_compression_pressure;pressure_continuation;liquidity_vacuum;open_pressure_burst | positive full-depth but below-12 diagnostics | Preserve families as search context, not as accepted strategies. |
| do_not_relax_annualized_denominator | 1 | fixed_initial_capital_required | Annualized return remains fixed-capital based, never unlimited-capital based. |
| do_not_claim_portfolio_return | 1 | best_scheduled_events=1;sparse_floor=8;robust_floor=30 | Evidence is too sparse for a portfolio-return claim. |
| selected_next_route | P289_ADAPTIVE_FULL_DEPTH_LIQUIDITY_PRESSURE_EXPANSION_SEARCH | fixed pressure grid exhausted; adaptive feature interactions required | Run an adaptive full-depth pressure expansion search. |

## Phase290 Route Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| P290_INPUTS | outputs/phase277/phase277_cost200_redesign_event_universe.csv;outputs/phase288/phase288_liquidity_pressure_scenario_results.csv;outputs/phase288/phase288_liquidity_pressure_variant_summary.csv | Use event universe plus Phase288 failure evidence. |
| P290_PRESERVED_PHASE288_CLUES | P288_P288_EXHAUSTION_REVERSAL_Q50_ORIG_H10;P288_P288_EXHAUSTION_REVERSAL_Q60_ORIG_H10;P288_P288_EXHAUSTION_REVERSAL_Q70_ORIG_H10;P288_P288_EXHAUSTION_REVERSAL_Q80_ORIG_H10;P288_P288_EXHAUSTION_REVERSAL_Q50_ORIG_H8;P288_P288_EXHAUSTION_REVERSAL_Q60_ORIG_H8;P288_P288_EXHAUSTION_REVERSAL_Q70_ORIG_H8;P288_P288_EXHAUSTION_REVERSAL_Q80_ORIG_H8;P288_P288_REPLENISHMENT_ABSORPTION_Q50_ORIG_H10;P288_P288_REPLENISHMENT_ABSORPTION_Q60_ORIG_H10;P288_P288_REPLENISHMENT_ABSORPTION_Q70_ORIG_H10;P288_P288_SPREAD_COMPRESSION_PRESSURE_Q50_ORIG_H10 | Carry forward positive full-depth pressure clues only as diagnostic context. |
| P290_PRESERVED_PRESSURE_FAMILIES | exhaustion_reversal;replenishment_absorption;spread_compression_pressure;pressure_continuation;liquidity_vacuum;open_pressure_burst | Keep positive but below-threshold families for adaptive expansion. |
| P290_SEARCH_TYPE | adaptive_full_depth_liquidity_pressure_expansion_search | Expand thresholds and feature interactions while preserving observable full-depth L2 masks. |
| P290_REQUIRED_DIRECTIONS | family_specific_thresholds;pressure_feature_interactions;side_by_pressure_sign;horizon_by_spread_state;open_vs_nonopen_buckets;cost200_fixed_capital_scheduler | Search more flexibly without using future labels as live masks. |
| P290_CAPITAL_AND_COST | initial_capital_100000;cost200_required;fixed_notional_grid;max_concurrent_grid;annualized_denominator_fixed_capital | No unlimited-capital annualized return. |
| P290_ACCEPTANCE_DIAGNOSTICS | cost200_annualized_pct_gt_12.0;scheduled_event_rows_ge_8_for_sparse_discovery;scheduled_event_rows_ge_30_for_portfolio_claim | Sparse >12% remains discovery only; robust portfolio claim needs a larger event floor. |
| P290_BOUNDARY | no_paper_live;no_strategy_replay;no_deployable_profitability_claim;l1_only_forbidden;net_edge_live_mask_forbidden | Boundaries remain closed until evidence earns them. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P289_PHASE288_SEARCH_COMPLETE | True | 1 | Phase288 search complete | hard |
| P289_PHASE288_NEXT_ACTION_PRESENT | True | run_phase289_full_depth_liquidity_pressure_interpretation_no_paper_live | Phase288 routes to Phase289 interpretation | hard |
| P289_PHASE288_GATES_PASS | True | 8/8 | Phase288 gates pass | hard |
| P289_RANKED_INTERPRETATION_PRESENT | True | 192 | >0 ranked variants | hard |
| P289_CLOSES_PHASE288_FOR_ACCEPTANCE | True | 1 | Phase288 closed for acceptance | hard |
| P289_NEXT_ROUTE_SELECTED | True | P289_ADAPTIVE_FULL_DEPTH_LIQUIDITY_PRESSURE_EXPANSION_SEARCH | P289_ADAPTIVE_FULL_DEPTH_LIQUIDITY_PRESSURE_EXPANSION_SEARCH | hard |
| P289_FULL_DEPTH_BOUNDARY_PRESERVED | True | l1_only=0;live_mask=0 | full-depth, no leakage | hard |
| P289_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |
| P289_ROUTE_CONTRACT_PRESENT | True | 8 | Phase290 route contract rows | hard |

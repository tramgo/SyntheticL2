# Phase294 Full-Depth Pressure Absorption Continuation Search

Synthetic-only search of continuation after top-five L2 pressure/absorption. No replay, paper/live, promotion, or profitability claim is opened.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase294_continuation_search_complete | 1 | Phase294 full-depth pressure absorption continuation search completed |
| phase294_selected_route | P294_FULL_DEPTH_PRESSURE_ABSORPTION_CONTINUATION_SEARCH | Selected route |
| phase294_variant_rows | 840 | Variants evaluated |
| phase294_scenario_rows | 3360 | Cost200 fixed-capital scenarios evaluated |
| phase294_family_rows | 4 | Continuation families evaluated |
| phase294_sparse_above12_scenario_rows | 0 | Above-12 sparse diagnostic rows |
| phase294_robust_portfolio_floor_scenario_rows | 0 | Robust floor rows |
| phase294_robust_portfolio_above12_scenario_rows | 0 | Robust above-12 rows |
| phase294_discovery_survivor_variant_rows | 0 | Variants with sparse above-12 rows |
| phase294_robust_survivor_variant_rows | 0 | Variants with robust above-12 rows |
| phase294_best_variant_id | P294_P294_SPREAD_COMPRESSED_ABSORPTION_CONT_P65_S55_I35_NOTWIDE_OPEN_ORIG_H13 | Best variant |
| phase294_best_continuation_family | spread_compressed_absorption_continuation | Best continuation family |
| phase294_best_side_mode | ORIG | Best side mode |
| phase294_best_market_bucket | OPEN | Best market bucket |
| phase294_best_cost200_annualized_pct | 7.83935 | Best annualized diagnostic |
| phase294_best_realized_net_pnl_inr | 93.3256 | Best net P&L |
| phase294_best_scheduled_event_rows | 1 | Best scheduled events |
| phase294_l1_only_variant_rows | 0 | L1-only variants |
| phase294_net_edge_live_mask_rows | 0 | Net edge live masks |
| phase294_strategy_replay_allowed | 0 | No replay |
| phase294_strategy_promotion_allowed | 0 | No promotion |
| phase294_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase294_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase294_hard_gate_pass_rows | 9 | Hard gates passed |
| phase294_hard_gate_rows | 9 | Hard gates |
| phase294_next_best_action | run_phase295_full_depth_pressure_absorption_continuation_interpretation_no_paper_live | Next action |

## Family Summary

| continuation_family | variant_rows | scenario_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_variant_id | discovery_survivor_family | robust_survivor_family |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| spread_compressed_absorption_continuation | 216 | 864 | 4 | 0 | 0 | 0 | 0 | 0.793878 | 7.83935 | 203.259 | P294_P294_SPREAD_COMPRESSED_ABSORPTION_CONT_P65_S55_I35_ANYSPREAD_OPEN_ORIG_H13 | 0 | 0 |
| withdrawal_followthrough_continuation | 216 | 864 | 4 | 0 | 0 | 0 | 0 | 1.21395 | 7.48304 | 237.557 | P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P35_S35_I35_NOTWIDE_ALL_ORIG_H13 | 0 | 0 |
| replenishment_absorption_continuation | 192 | 768 | 2 | 0 | 0 | 0 | 0 | 0.614884 | 5.55934 | 176.487 | P294_P294_REPLENISHMENT_ABSORPTION_CONT_P50_S45_I35_ANYSPREAD_ALL_ORIG_H13 | 0 | 0 |
| consensus_depth_continuation | 216 | 864 | 10 | 0 | 0 | 28 | 0 | -4.64042 | 2.55031 | 80.9623 | P294_P294_CONSENSUS_DEPTH_CONT_P35_S35_I35_NOTWIDE_ALL_ORIG_H8 | 0 | 0 |

## Top Variants

| phase294_variant_id | continuation_family | market_bucket | side_mode | exit_horizon_ticks | scenario_rows | selected_event_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P294_P294_SPREAD_COMPRESSED_ABSORPTION_CONT_P65_S55_I35_ANYSPREAD_OPEN_ORIG_H13 | spread_compressed_absorption_continuation | OPEN | ORIG | 13 | 4 | 8 | 2 | 0 | 0 | 0 | 0 | 3.65108 | 3.78538 | 7.83935 | 93.3256 |
| P294_P294_SPREAD_COMPRESSED_ABSORPTION_CONT_P65_S55_I35_ANYSPREAD_OPEN_PRESSURE_SIGN_CONT_H13 | spread_compressed_absorption_continuation | OPEN | PRESSURE_SIGN_CONT | 13 | 4 | 8 | 2 | 0 | 0 | 0 | 0 | 3.65108 | 3.78538 | 7.83935 | 93.3256 |
| P294_P294_SPREAD_COMPRESSED_ABSORPTION_CONT_P65_S55_I35_NOTWIDE_OPEN_ORIG_H13 | spread_compressed_absorption_continuation | OPEN | ORIG | 13 | 4 | 8 | 2 | 0 | 0 | 0 | 0 | 3.65108 | 3.78538 | 7.83935 | 93.3256 |
| P294_P294_SPREAD_COMPRESSED_ABSORPTION_CONT_P65_S55_I35_NOTWIDE_OPEN_PRESSURE_SIGN_CONT_H13 | spread_compressed_absorption_continuation | OPEN | PRESSURE_SIGN_CONT | 13 | 4 | 8 | 2 | 0 | 0 | 0 | 0 | 3.65108 | 3.78538 | 7.83935 | 93.3256 |
| P294_P294_SPREAD_COMPRESSED_ABSORPTION_CONT_P65_S55_I55_ANYSPREAD_OPEN_ORIG_H13 | spread_compressed_absorption_continuation | OPEN | ORIG | 13 | 4 | 7 | 2 | 0 | 0 | 0 | 0 | 3.64638 | 3.78186 | 7.83467 | 93.2698 |
| P294_P294_SPREAD_COMPRESSED_ABSORPTION_CONT_P65_S55_I55_ANYSPREAD_OPEN_PRESSURE_SIGN_CONT_H13 | spread_compressed_absorption_continuation | OPEN | PRESSURE_SIGN_CONT | 13 | 4 | 7 | 2 | 0 | 0 | 0 | 0 | 3.64638 | 3.78186 | 7.83467 | 93.2698 |
| P294_P294_SPREAD_COMPRESSED_ABSORPTION_CONT_P65_S55_I55_NOTWIDE_OPEN_ORIG_H13 | spread_compressed_absorption_continuation | OPEN | ORIG | 13 | 4 | 7 | 2 | 0 | 0 | 0 | 0 | 3.64638 | 3.78186 | 7.83467 | 93.2698 |
| P294_P294_SPREAD_COMPRESSED_ABSORPTION_CONT_P65_S55_I55_NOTWIDE_OPEN_PRESSURE_SIGN_CONT_H13 | spread_compressed_absorption_continuation | OPEN | PRESSURE_SIGN_CONT | 13 | 4 | 7 | 2 | 0 | 0 | 0 | 0 | 3.64638 | 3.78186 | 7.83467 | 93.2698 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P35_S35_I35_NOTWIDE_ALL_ORIG_H13 | withdrawal_followthrough_continuation | ALL | ORIG | 13 | 4 | 299 | 2 | 0 | 0 | 0 | 0 | 2.52092 | 3.13122 | 7.48304 | 237.557 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P35_S35_I35_NOTWIDE_ALL_PRESSURE_SIGN_CONT_H13 | withdrawal_followthrough_continuation | ALL | PRESSURE_SIGN_CONT | 13 | 4 | 299 | 2 | 0 | 0 | 0 | 0 | 2.52092 | 3.13122 | 7.48304 | 237.557 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P35_S35_I35_NOTWIDE_NONOPEN_ORIG_H13 | withdrawal_followthrough_continuation | NONOPEN | ORIG | 13 | 4 | 147 | 2 | 0 | 0 | 0 | 0 | 3.22822 | 3.48487 | 7.48304 | 237.557 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P35_S35_I35_NOTWIDE_NONOPEN_PRESSURE_SIGN_CONT_H13 | withdrawal_followthrough_continuation | NONOPEN | PRESSURE_SIGN_CONT | 13 | 4 | 147 | 2 | 0 | 0 | 0 | 0 | 3.22822 | 3.48487 | 7.48304 | 237.557 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P50_S45_I35_NOTWIDE_ALL_ORIG_H13 | withdrawal_followthrough_continuation | ALL | ORIG | 13 | 4 | 180 | 2 | 0 | 0 | 0 | 0 | 2.4717 | 3.10661 | 7.48304 | 237.557 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P50_S45_I35_NOTWIDE_ALL_PRESSURE_SIGN_CONT_H13 | withdrawal_followthrough_continuation | ALL | PRESSURE_SIGN_CONT | 13 | 4 | 180 | 2 | 0 | 0 | 0 | 0 | 2.4717 | 3.10661 | 7.48304 | 237.557 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P50_S45_I35_NOTWIDE_NONOPEN_ORIG_H13 | withdrawal_followthrough_continuation | NONOPEN | ORIG | 13 | 4 | 142 | 2 | 0 | 0 | 0 | 0 | 3.74152 | 7.47855 | 7.48304 | 237.557 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P50_S45_I35_NOTWIDE_NONOPEN_PRESSURE_SIGN_CONT_H13 | withdrawal_followthrough_continuation | NONOPEN | PRESSURE_SIGN_CONT | 13 | 4 | 142 | 2 | 0 | 0 | 0 | 0 | 3.74152 | 7.47855 | 7.48304 | 237.557 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P35_S35_I55_NOTWIDE_ALL_ORIG_H13 | withdrawal_followthrough_continuation | ALL | ORIG | 13 | 4 | 151 | 2 | 0 | 0 | 0 | 0 | 3.38535 | 6.77019 | 6.7707 | 214.943 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P35_S35_I55_NOTWIDE_ALL_PRESSURE_SIGN_CONT_H13 | withdrawal_followthrough_continuation | ALL | PRESSURE_SIGN_CONT | 13 | 4 | 151 | 2 | 0 | 0 | 0 | 0 | 3.38535 | 6.77019 | 6.7707 | 214.943 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P35_S35_I55_NOTWIDE_NONOPEN_ORIG_H13 | withdrawal_followthrough_continuation | NONOPEN | ORIG | 13 | 4 | 142 | 2 | 0 | 0 | 0 | 0 | 3.38535 | 6.77019 | 6.7707 | 214.943 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P35_S35_I55_NOTWIDE_NONOPEN_PRESSURE_SIGN_CONT_H13 | withdrawal_followthrough_continuation | NONOPEN | PRESSURE_SIGN_CONT | 13 | 4 | 142 | 2 | 0 | 0 | 0 | 0 | 3.38535 | 6.77019 | 6.7707 | 214.943 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P65_S55_I35_NOTWIDE_ALL_ORIG_H13 | withdrawal_followthrough_continuation | ALL | ORIG | 13 | 4 | 135 | 2 | 0 | 0 | 0 | 0 | 3.38107 | 6.76118 | 6.76214 | 214.671 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P65_S55_I35_NOTWIDE_ALL_PRESSURE_SIGN_CONT_H13 | withdrawal_followthrough_continuation | ALL | PRESSURE_SIGN_CONT | 13 | 4 | 135 | 2 | 0 | 0 | 0 | 0 | 3.38107 | 6.76118 | 6.76214 | 214.671 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P65_S55_I35_NOTWIDE_NONOPEN_ORIG_H13 | withdrawal_followthrough_continuation | NONOPEN | ORIG | 13 | 4 | 130 | 2 | 0 | 0 | 0 | 0 | 3.38107 | 6.76118 | 6.76214 | 214.671 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P65_S55_I35_NOTWIDE_NONOPEN_PRESSURE_SIGN_CONT_H13 | withdrawal_followthrough_continuation | NONOPEN | PRESSURE_SIGN_CONT | 13 | 4 | 130 | 2 | 0 | 0 | 0 | 0 | 3.38107 | 6.76118 | 6.76214 | 214.671 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P50_S45_I55_NOTWIDE_ALL_ORIG_H13 | withdrawal_followthrough_continuation | ALL | ORIG | 13 | 4 | 126 | 2 | 0 | 0 | 0 | 0 | 3.38012 | 6.75917 | 6.76023 | 214.611 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P50_S45_I55_NOTWIDE_ALL_PRESSURE_SIGN_CONT_H13 | withdrawal_followthrough_continuation | ALL | PRESSURE_SIGN_CONT | 13 | 4 | 126 | 2 | 0 | 0 | 0 | 0 | 3.38012 | 6.75917 | 6.76023 | 214.611 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P50_S45_I55_NOTWIDE_NONOPEN_ORIG_H13 | withdrawal_followthrough_continuation | NONOPEN | ORIG | 13 | 4 | 121 | 2 | 0 | 0 | 0 | 0 | 3.38012 | 6.75917 | 6.76023 | 214.611 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P50_S45_I55_NOTWIDE_NONOPEN_PRESSURE_SIGN_CONT_H13 | withdrawal_followthrough_continuation | NONOPEN | PRESSURE_SIGN_CONT | 13 | 4 | 121 | 2 | 0 | 0 | 0 | 0 | 3.38012 | 6.75917 | 6.76023 | 214.611 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P65_S55_I55_NOTWIDE_ALL_ORIG_H13 | withdrawal_followthrough_continuation | ALL | ORIG | 13 | 4 | 98 | 2 | 0 | 0 | 0 | 0 | 3.377 | 6.75262 | 6.75401 | 214.413 |
| P294_P294_WITHDRAWAL_FOLLOWTHROUGH_CONT_P65_S55_I55_NOTWIDE_ALL_PRESSURE_SIGN_CONT_H13 | withdrawal_followthrough_continuation | ALL | PRESSURE_SIGN_CONT | 13 | 4 | 98 | 2 | 0 | 0 | 0 | 0 | 3.377 | 6.75262 | 6.75401 | 214.413 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P294_PHASE293_WORK_ORDER_PRESENT | True | run_phase294_full_depth_pressure_absorption_continuation_search_no_paper_live | Phase293 routes to Phase294 | hard |
| P294_VARIANTS_PRESENT | True | 840 | >=250 continuation variants | hard |
| P294_SCENARIOS_PRESENT | True | 3360 | >=1000 fixed-capital scenarios | hard |
| P294_MULTIPLE_FAMILIES_TESTED | True | 4 | >=4 continuation families | hard |
| P294_COST_AND_FIXED_CAPITAL_REQUIRED | True | cost200=1;fixed_capital=1 | cost200 fixed-capital scoring | hard |
| P294_FULL_DEPTH_REQUIRED | True | catalog_l1=0 | full-depth, no L1-only | hard |
| P294_NO_LIVE_NET_EDGE_MASKS | True | 0 | no net/gross edge live masks | hard |
| P294_FIXED_CAPITAL_ANNUALIZED_DENOMINATOR | True | fixed_initial_capital | no unlimited-capital denominator | hard |
| P294_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |

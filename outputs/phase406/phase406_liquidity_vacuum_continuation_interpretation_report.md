# Phase406 Liquidity-Vacuum Continuation Interpretation

Phase406 interprets the Phase405 fixed-threshold material-new full-depth L2 thesis.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase406_liquidity_vacuum_continuation_interpretation_complete | 1 | Phase406 interpretation completed |
| phase406_selected_decision | P406_LIQUIDITY_VACUUM_CONTINUATION_REJECTED | Selected decision |
| phase406_primary_raw_candidate_rows | 75 | Primary raw candidates |
| phase406_primary_capacity_selected_trade_rows | 28 | Primary selected trades |
| phase406_primary_net_pnl_inr | -11542.9 | Primary net PnL |
| phase406_primary_annualized_return_pct | -72.7204 | Primary annualized return |
| phase406_primary_above12 | 0 | Primary above 12% |
| phase406_primary_event_floor_met | 0 | Primary event floor |
| phase406_primary_breadth_met | 1 | Primary breadth |
| phase406_primary_acceptance_candidate | 0 | Primary acceptance |
| phase406_side_flip_annualized_return_pct | 5.12294 | Side flip |
| phase406_depth_removed_annualized_return_pct | -71.1864 | Depth removed |
| phase406_same_threshold_rescue_allowed | 0 | No threshold rescue |
| phase406_strategy_promotion_allowed | 0 | No promotion |
| phase406_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase406_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase406_hard_gate_pass_rows | 6 | Passed hard gates |
| phase406_hard_gate_rows | 6 | Hard gates |
| phase406_next_best_action | precommit_next_materially_new_l2_thesis_or_pause_strategy_search_no_paper_live | Recommended next action |

## Decision Ledger

| decision_id | decision_value | evidence | decision_status |
| --- | --- | --- | --- |
| selected_decision | P406_LIQUIDITY_VACUUM_CONTINUATION_REJECTED | Primary thesis is negative after cost200. | reject |
| primary_profitability | 0 | annualized=-72.72039100722851 | >12.0 |
| primary_event_floor | 0 | selected_events=28 | >=30 |
| primary_acceptance | 0 | acceptance=0 | 0 means rejected |
| side_flip_control | 5.12294 | Opposite side does not clear >12 either. | diagnostic |
| depth_removed_control | -71.1864 | Removing levels 2-5 does not rescue the idea. | diagnostic |
| same_threshold_rescue_allowed | 0 | Fixed-threshold first test failed; no parameter rescue opened. | forbidden |
| paper_live_or_profit_claim | 0 | promotion=0;paper=0;claim=0 | closed |
| next_action | precommit_next_materially_new_l2_thesis_or_pause_strategy_search_no_paper_live | Move only to materially new thesis, or pause strategy search. | next |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P406_PHASE405_COMPLETE | True | 1 | 1 | hard |
| P406_PRIMARY_SCENARIO_INTERPRETED | True | 1 | 1 | hard |
| P406_PRIMARY_REJECTED | True | 0 | 0 | hard |
| P406_DECISION_REJECTS_BRANCH | True | P406_LIQUIDITY_VACUUM_CONTINUATION_REJECTED | P406_LIQUIDITY_VACUUM_CONTINUATION_REJECTED | hard |
| P406_NO_PARAMETER_RESCUE | True | 0 | 0 | hard |
| P406_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

## Scenario Summary

| scenario_id | scenario_role | raw_candidate_rows | capacity_selected_trade_rows | diagnostic_dates | symbols | positive_symbols | positive_symbol_date_cells | net_pnl_inr | annualized_return_pct | above12 | event_floor_met | breadth_met | acceptance_candidate | avg_impulse_bps | avg_replenishment_ratio | avg_l2_l5_abs_imbalance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P405_LIQUIDITY_VACUUM_CONTINUATION_FULL_DEPTH | liquidity_vacuum_continuation | 75 | 28 | 16 | 14 | 4 | 5 | -11542.9 | -72.7204 | 0 | 0 | 1 | 0 | 32.3633 | -0.263548 | 0.407817 |
| P405_CONTROL_SIDE_FLIP | side_flip_control | 75 | 28 | 16 | 14 | 5 | 9 | 813.164 | 5.12294 | 0 | 0 | 1 | 0 | 32.3633 | -0.263548 | 0.407817 |
| P405_CONTROL_TOP5_ONLY_DEPTH_REMOVED | top5_only_depth_removed_control | 78 | 29 | 16 | 14 | 4 | 6 | -11299.4 | -71.1864 | 0 | 0 | 1 | 0 | 30.6777 | -0.285607 | 0.396241 |

No promotion, paper/live acceptance, deployable profitability claim, or same-threshold rescue is opened.

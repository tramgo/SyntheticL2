# Phase433 Geometry-Consistent Sweep Interpretation

Phase433 interprets Phase432 as a real negative result after repairing timing geometry.

The broader full-depth feature sweep produced active synthetic trades, but the best active scenario was sparse and negative after Zerodha cost200. No strategy acceptance or paper/live boundary is opened.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase433_geometry_consistent_sweep_interpretation_complete | 1 | Phase433 interpretation completed |
| phase433_selected_verdict | P433_GEOMETRY_CONSISTENT_FULL_DEPTH_SWEEP_REJECTED_NEGATIVE_SPARSE | Selected verdict |
| phase433_phase432_best_completed_round_trips | 10 | Phase432 best active round trips |
| phase433_phase432_best_annualized_return_pct | -20.21273903621011 | Phase432 best active annualized return |
| phase433_phase432_active_synthetic_scenario_rows | 27 | Phase432 active scenario rows |
| phase433_strategy_promotion_allowed | 0 | No promotion |
| phase433_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase433_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase433_same_threshold_family_tuning_allowed | 0 | No threshold tuning |
| phase433_hard_gate_pass_rows | 8 | Passed hard gates |
| phase433_hard_gate_rows | 8 | Hard gates |
| phase433_next_best_action | pause_for_strategy_decision_report_or_precommit_material_new_non_threshold_source | Recommended next action |

## Decision Ledger

| decision_id | decision_value | evidence | status |
| --- | --- | --- | --- |
| selected_verdict | P433_GEOMETRY_CONSISTENT_FULL_DEPTH_SWEEP_REJECTED_NEGATIVE_SPARSE | After timing repair, the broader full-depth sweep produced active but sparse negative synthetic trades and no survivor. | terminal_for_this_sweep |
| phase432_next_action_matched | interpret_phase432_geometry_consistent_full_depth_feature_sweep_no_paper_live | Phase433 implements the Phase432 next-action string. | basis |
| synthetic_grid_rows | 486 | Synthetic grid rows evaluated. | evidence |
| active_synthetic_scenario_rows | 27 | Scenarios with at least one synthetic trade. | evidence |
| best_active_scenario_id | P432_synthetic_depth_pressure_continuation_L60_F3_M2500_S8p0_I0p25_D0p1 | Best active scenario after corrected ranking. | failure |
| best_active_family_id | depth_pressure_continuation | Best active family. | failure |
| best_active_round_trips | 10 | Sparse versus event floor. | failure |
| best_active_trade_dates | 2 | Sparse versus date breadth. | failure |
| best_active_symbols | 1 | Sparse versus symbol breadth. | failure |
| best_active_net_pnl_inr | -1604.185637794453 | Negative after cost200. | failure |
| best_active_annualized_return_pct | -20.21273903621011 | Failed annualized floor. | failure |
| phase432_failed_hard_gates | P432_L1_ONLY_CONTROL;P432_EVENT_FLOOR;P432_DATE_BREADTH;P432_SYMBOL_BREADTH;P432_POSITIVE_DATE_FRACTION;P432_ANNUALIZED_FLOOR | Explicit failed gate basis. | basis |
| real_anchor_active_scenario_rows | 0 | Matching real-anchor rows had no active trades. | real_anchor_gap |
| strategy_promotion_allowed | 0 | No accepted survivor. | closed |
| paper_or_live_acceptance_allowed | 0 | No paper/live acceptance. | closed |
| deployable_profitability_claim_allowed | 0 | No deployable claim. | closed |
| same_threshold_family_tuning_allowed | 0 | Do not tune thresholds after seeing the negative sparse result. | closed |
| next_action | pause_for_strategy_decision_report_or_precommit_material_new_non_threshold_source | Decide whether to pause or precommit a materially new non-threshold source. | next |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P433_PHASE432_COMPLETE | True | 1 | 1 | hard |
| P433_PHASE432_GATES_EVALUATED | True | 17 | 17 | hard |
| P433_PHASE432_FAILED_GATES_PRESENT | True | passed=11/17;failed=P432_L1_ONLY_CONTROL;P432_EVENT_FLOOR;P432_DATE_BREADTH;P432_SYMBOL_BREADTH;P432_POSITIVE_DATE_FRACTION;P432_ANNUALIZED_FLOOR | failed_gates_nonempty | hard |
| P433_ACTIVE_BUT_SPARSE_RESULT_RECORDED | True | 10 | 0<trips<30 | hard |
| P433_NEGATIVE_COST200_CONFIRMED | True | -20.2127 | <0 | hard |
| P433_VERDICT_PRESENT | True | P433_GEOMETRY_CONSISTENT_FULL_DEPTH_SWEEP_REJECTED_NEGATIVE_SPARSE | P433_GEOMETRY_CONSISTENT_FULL_DEPTH_SWEEP_REJECTED_NEGATIVE_SPARSE | hard |
| P433_NO_THRESHOLD_TUNING | True | 0 | 0 | hard |
| P433_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: do not tune the same threshold-family sweep after seeing this result.

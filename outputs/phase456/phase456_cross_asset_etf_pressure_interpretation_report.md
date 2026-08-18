# Phase456 Cross-Asset ETF Pressure Interpretation

Phase456 formally interprets the repaired Phase455 cross-asset ETF pressure execution. The first-window form is rejected because it produced zero gross edge and failed control dominance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase456_cross_asset_interpretation_complete | 1 | Phase456 interpretation completed |
| phase456_thesis_id | P456_CROSS_ASSET_ETF_PRESSURE_INTERPRETATION | Interpretation thesis |
| phase456_selected_verdict | P456_FIRST_WINDOW_CROSS_ASSET_ETF_PRESSURE_REJECTED_ZERO_GROSS_EDGE | Selected verdict |
| phase456_same_form_rescue_allowed | 0 | No same-form rescue |
| phase456_strategy_promotion_allowed | 0 | No promotion |
| phase456_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase456_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase456_hard_gate_pass_rows | 8 | Passed hard gates |
| phase456_hard_gate_rows | 8 | Hard gates |
| phase456_next_best_action | precommit_material_new_timing_or_label_source_not_first_window_cross_asset_pressure | Recommended next action |

## Decision Ledger

| decision_id | decision_value | description | required_or_implication |
| --- | --- | --- | --- |
| selected_verdict | P456_FIRST_WINDOW_CROSS_ASSET_ETF_PRESSURE_REJECTED_ZERO_GROSS_EDGE | The repaired first-window cross-asset ETF pressure source is rejected. | terminal_for_first_window_form |
| acceptance_survivor | 0 | No accepted survivor. | 0 |
| primary_completed_round_trips | 284 | Breadth was sufficient for a real verdict. | >=30 |
| primary_trade_dates | 129 | Date breadth was sufficient. | >=5 |
| primary_symbols | 3 | Symbol breadth was sufficient. | >=3 |
| primary_gross_pnl_inr | 0 | Gross edge before costs. | positive_required_for_any_costed_edge |
| primary_net_pnl_inr | -46912.6 | Net P&L after Zerodha cost200. | >0_required |
| primary_annualized_return_pct | -9.16432 | Fixed-capital annualized return. | >=12_required |
| source_time_shift_net_pnl_inr | -46416.9 | Time-shift control. | primary_should_dominate |
| side_flip_net_pnl_inr | -46912.6 | Side-flip control. | primary_should_dominate |
| etf_l1_only_net_pnl_inr | -46912.6 | ETF L1-only control. | primary_should_dominate |
| failed_gate_ids | P455_POSITIVE_DATE_FRACTION_GE_0_60;P455_ANNUALIZED_GE_12_COST200;P455_TIME_SHIFT_NOT_DOMINANT;P455_SIDE_FLIP_NOT_DOMINANT;P455_ETF_L1_ONLY_NOT_DOMINANT | Failed Phase455 gates. | must_be_empty_for_acceptance |
| same_first_window_cross_asset_rescue_allowed | 0 | Do not tune the same first-window source after this result. | 0 |
| paper_live_or_profit_claim | 0 | No promotion, paper/live acceptance or deployable claim. | 0 |
| next_action | precommit_material_new_timing_or_label_source_not_first_window_cross_asset_pressure | Next source must alter timing/label source materially, not tweak this failed form. | material_new |

## Durable Byproducts

| byproduct_id | status | description |
| --- | --- | --- |
| contiguous_window_reader | reusable | Reads first contiguous raw L1-L5 tick windows per symbol/date from monthly Parquet partitions. |
| cross_asset_signal_metrics | reusable | Daily proxy/target L1-L5 pressure metrics for ETF-to-constituent experiments. |
| low_turnover_control_harness | reusable | Source-shift, side-flip, target-only and ETF L1-only controls. |
| negative_evidence_first_window | ledger | First-window proxy pressure produced zero gross edge and only costs. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P456_PHASE455_COMPLETE | True | 1 | 1 | hard |
| P456_PHASE455_REAL_TRADES_PRESENT | True | 284 | >0 | hard |
| P456_NO_ACCEPTANCE_SURVIVOR | True | 0 | 0 | hard |
| P456_FAILED_GATE_BASIS_PRESENT | True | P455_POSITIVE_DATE_FRACTION_GE_0_60;P455_ANNUALIZED_GE_12_COST200;P455_TIME_SHIFT_NOT_DOMINANT;P455_SIDE_FLIP_NOT_DOMINANT;P455_ETF_L1_ONLY_NOT_DOMINANT | >0 | hard |
| P456_VERDICT_REJECTS_FIRST_WINDOW_FORM | True | P456_FIRST_WINDOW_CROSS_ASSET_ETF_PRESSURE_REJECTED_ZERO_GROSS_EDGE | REJECTED | hard |
| P456_SAME_FORM_RESCUE_CLOSED | True | 0 | 0 | hard |
| P456_BOUNDARIES_CLOSED | True | 0 | 0 | hard |
| P456_NEXT_ACTION_MATERIAL_NEW | True | precommit_material_new_timing_or_label_source_not_first_window_cross_asset_pressure | material_new | hard |

Boundary: do not tune the same first-window cross-asset pressure form. A new phase must precommit a materially different timing or label source.

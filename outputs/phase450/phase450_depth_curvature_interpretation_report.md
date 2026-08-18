# Phase450 Depth-Curvature Break/Repair Interpretation

Phase450 formally interprets Phase449. It records the depth-curvature dynamic route as rejected under cost200 and control dominance evidence.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase450_depth_curvature_interpretation_complete | 1 | Phase450 interpretation completed |
| phase450_thesis_id | P450_DEPTH_CURVATURE_BREAK_REPAIR_INTERPRETATION | Interpretation thesis |
| phase450_selected_verdict | P450_DEPTH_CURVATURE_DYNAMIC_ROUTE_REJECTED_COST_AND_CONTROLS | Selected verdict |
| phase450_phase449_acceptance_survivor | 0 | Phase449 survivor status |
| phase450_same_source_rescue_allowed | 0 | No same-source rescue |
| phase450_strategy_promotion_allowed | 0 | No promotion |
| phase450_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase450_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase450_hard_gate_pass_rows | 7 | Passed hard gates |
| phase450_hard_gate_rows | 7 | Hard gates |
| phase450_next_best_action | precommit_new_low_turnover_external_or_cross_asset_source_edge | Recommended next action |

## Decision Ledger

| decision_id | decision_value | description | required_or_implication |
| --- | --- | --- | --- |
| selected_verdict | P450_DEPTH_CURVATURE_DYNAMIC_ROUTE_REJECTED_COST_AND_CONTROLS | Phase449 is rejected as a stable/profitable strategy route. | terminal_for_this_dynamic_curvature_form |
| acceptance_survivor | 0 | No accepted survivor. | 0 |
| primary_net_pnl_inr | -238862 | Primary net P&L after cost200. | >0_required_else_reject |
| primary_annualized_return_pct | -23.8862 | Fixed-capital annualized return. | >=12_required |
| primary_positive_date_fraction | 0.166667 | Positive-date fraction. | >=0.60_required |
| l1_only_net_pnl_inr | -218598 | L1-only control net P&L. | primary_should_dominate |
| static_curvature_net_pnl_inr | -196207 | Static curvature control net P&L. | primary_should_dominate |
| time_shift_net_pnl_inr | -234062 | Time-shift control net P&L. | primary_should_dominate |
| failed_gate_ids | P449_POSITIVE_DATE_FRACTION_GE_0_60;P449_ANNUALIZED_GE_12_COST200;P449_L1_ONLY_NOT_DOMINANT;P449_STATIC_SNAPSHOT_NOT_DOMINANT;P449_TIME_SHIFT_NOT_DOMINANT | Failed hard gates. | must_be_empty_for_acceptance |
| same_source_rescue_allowed | 0 | Do not tune this dynamic curvature source after failure. | 0 |
| paper_live_or_profit_claim | 0 | No promotion, paper/live acceptance or deployable profitability claim. | 0 |
| next_action | precommit_new_low_turnover_external_or_cross_asset_source_edge | Next work must be a new source edge, preferably lower-turnover/external/cross-asset. | new_source |

## Durable Byproducts

| byproduct_id | status | description |
| --- | --- | --- |
| phase449_strided_parquet_scanner | reusable | Efficiently scans raw dense Parquet batches without loading full 80GB-style lake into memory. |
| phase449_l2_l5_curvature_features | diagnostic | Reusable feature engineering for depth curvature, asymmetry and repair/break rate. |
| phase449_control_harness | reusable | L1-only, side-flip, static-snapshot and time-shift controls can be reused for future L2 source tests. |
| negative_evidence_cost200 | ledger | High event count with negative net P&L shows turnover/cost mismatch. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P450_PHASE449_COMPLETE | True | 1 | 1 | hard |
| P450_NO_ACCEPTANCE_SURVIVOR | True | 0 | 0 | hard |
| P450_FAILED_GATE_BASIS_PRESENT | True | P449_POSITIVE_DATE_FRACTION_GE_0_60;P449_ANNUALIZED_GE_12_COST200;P449_L1_ONLY_NOT_DOMINANT;P449_STATIC_SNAPSHOT_NOT_DOMINANT;P449_TIME_SHIFT_NOT_DOMINANT | >0 | hard |
| P450_VERDICT_REJECTS_ROUTE | True | P450_DEPTH_CURVATURE_DYNAMIC_ROUTE_REJECTED_COST_AND_CONTROLS | REJECTED | hard |
| P450_SAME_SOURCE_RESCUE_CLOSED | True | 0 | 0 | hard |
| P450_BOUNDARIES_CLOSED | True | 0 | 0 | hard |
| P450_NEXT_ACTION_NEW_SOURCE | True | precommit_new_low_turnover_external_or_cross_asset_source_edge | new_source | hard |

Boundary: do not tune this same dynamic curvature source. The next executable route must be precommitted as a new source edge.

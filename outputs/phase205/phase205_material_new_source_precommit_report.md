# Phase205 Material New Source Precommit

Generated UTC: 2026-07-28T20:41:53.761699+00:00

Phase205 selects the next post-passive-closure route.
It precommits a material source path only; no replay, test, orders, fills, P&L, promotion, or paper/live acceptance is opened.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase205_evidence_rows | 5 | Source evidence rows |
| phase205_route_scorecard_rows | 3 | Route scorecard rows |
| phase205_selected_source_contract_rows | 1 | Selected source contract rows |
| phase205_phase206_work_order_rows | 3 | Phase206 work-order rows |
| phase205_selected_route_id | P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | Selected route |
| phase205_gate_rows | 6 | Gates evaluated |
| phase205_hard_gate_rows | 6 | Hard gates evaluated |
| phase205_hard_gate_pass_rows | 6 | Hard gates passed |
| phase205_material_new_source_precommit_complete | 1 | 1 means Phase205 completed |
| phase205_strategy_replay_allowed | 0 | No strategy replay opened |
| phase205_test_replay_allowed_next | 0 | No test replay opened |
| phase205_promotion_allowed | 0 | No promotion opened |
| phase205_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase205_forbidden_outputs | strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening | Outputs forbidden in this phase |
| phase205_next_best_action | run_phase206_selected_source_nonoverlap_feature_contract_no_replay | Recommended next milestone |

## Source Evidence Ledger

| evidence_id | source_route | status | evidence | replay_allowed |
| --- | --- | --- | --- | --- |
| P205_PHASE204_CLOSURE | post_passive_closure | ready | passive_closed=1; material_new_source_required=1; threshold_widening_allowed=0 | 0 |
| P205_PHASE203_PASSIVE_REJECTION | passive_label_breadth_alternative | candidate_gate_closed | materialized_rows=696; redesigned_pass_rows=0; adverse_ceiling_met=0 | 0 |
| P205_PHASE171_EXTERNAL_SOURCE | real_receive_flow_external_orderflow_context | selected_axis_available | selected_source=P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW; gates_pass=1; azure_policy=forbidden_for_analysis_download_first_then_local | 0 |
| P205_PHASE172_LOCAL_PANEL | real_receive_flow_external_orderflow_context | ready | ready_dates=7; symbol_day_rows=224; rows=3654137; bytes=10525885744 | 1 |
| P205_PHASE175_177_FEATURE_QUALITY | real_receive_flow_external_orderflow_context | quality_ready | schema_activation=1; features_materialized=1; quality_audit=1 | 0 |

## Route Scorecard

| route_id | phase204_queue_item | route_class | priority | evidence_ready | blocked_reason | selected_route | allowed_next_scope | strategy_replay_allowed | phase204_queue_rows_available |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | precommit_non_passive_external_orderflow_or_context_source | material_new_non_passive_source | 1 | 1 |  | 1 | source_contract_refresh_and_feature_family_precommit_no_replay | 0 | 3 |
| P205_PASSIVE_LABEL_BREADTH_EXPANSION_ONLY | expand_redesigned_passive_label_materialization_breadth | passive_label_only_alternative | 2 | 1 | replay_closed_candidate_gate_zero | 0 | label_only_breadth_expansion_no_replay | 0 | 3 |
| P205_REAL_ANCHOR_CALIBRATION_REFRESH | return_to_real_anchor_microstructure_calibration | calibration_audit | 3 | 1 | not_primary_source_precommit_route | 0 | local_calibration_audit_no_replay | 0 | 3 |

## Selected Source Contract

| contract_id | selected_route_id | selected_source_family | material_difference | required_inputs_next | first_allowed_deliverable | forbidden_next | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P205_SELECTED_SOURCE_ROUTE | P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | real_receive_flow_context_source_refresh | Re-enters the real multiday receive-flow source as a source-contract refresh after the passive queue redesign closed, not as a replay of the failed passive or prior context models. | phase171_source_contract;phase172_local_panel;phase175_schema;phase176_features;phase177_quality;phase204_guardrails | Phase206 refreshed source contract and non-overlap feature-family catalog | strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening | 0 | 0 | 0 | 0 |

## Phase206 Work Order

| work_order_id | selected_route_id | action | allowed_scope | strategy_replay_allowed |
| --- | --- | --- | --- | --- |
| P206_WO01_SOURCE_NON_OVERLAP_AUDIT | P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | audit selected source against failed Phase194-204 forms | source_contract_no_replay | 0 |
| P206_WO02_FEATURE_FAMILY_CATALOG | P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | catalog materially new receive-flow context features without model fitting | feature_contract_no_replay | 0 |
| P206_WO03_PRE_REPLAY_GUARDRAILS | P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | carry forward no-threshold-widening, train-only selection, and no test replay guardrails | guardrail_contract_no_replay | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P205_PHASE204_EVIDENCE_RECORDED | True | evidence_rows=5 | hard |
| P205_SINGLE_ROUTE_SELECTED | True | selected_routes=1 | hard |
| P205_SELECTED_ROUTE_IS_MATERIAL_NEW_SOURCE | True | selected_route=P205_REAL_RECEIVE_FLOW_CONTEXT_SOURCE_REFRESH | hard |
| P205_PASSIVE_REPLAY_REMAINS_CLOSED | True | source_evidence_replay_flags_sum=1; phase172_unlock_is_source_not_replay | hard |
| P205_PHASE206_WORK_ORDER_RECORDED | True | work_order_rows=3 | hard |
| P205_NO_REPLAY_OR_PROMOTION | True | strategy_replay=0; test_replay=0; promotion=0; paper_live=0 | hard |

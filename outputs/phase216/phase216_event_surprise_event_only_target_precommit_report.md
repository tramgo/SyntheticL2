# Phase216 Event-surprise Event-only Target Precommit

Generated UTC: 2026-07-28T21:44:13.939159+00:00

Phase216 converts Phase215's sparse-label interpretation into an event-only target contract.
It permits only event_surprise_bucket == 1 targets for future design-matrix precommit and keeps model fitting, replay, sealed test, promotion, paper/live acceptance, and profitability claims closed.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase216_event_only_target_rows | 7 | Allowed event-only target rows |
| phase216_full_train_validation_target_rows | 7 | Allowed targets with both train and validation interpretable |
| phase216_excluded_target_rows | 10 | Excluded split/horizon/label rows |
| phase216_event_only_contract_rows | 1 | Event-only target contract rows |
| phase216_control_contract_rows | 3 | Control contract rows |
| phase216_phase217_work_order_rows | 1 | Phase217 work-order rows |
| phase216_forbidden_execution_rows | 13 | Forbidden execution rows |
| phase216_gate_rows | 7 | Gates evaluated |
| phase216_hard_gate_rows | 7 | Hard gates evaluated |
| phase216_hard_gate_pass_rows | 7 | Hard gates passed |
| phase216_event_surprise_event_only_target_precommit_complete | 1 | 1 means Phase216 completed |
| phase216_model_fit_allowed_next | 0 | No model fit opened |
| phase216_strategy_replay_allowed | 0 | No strategy replay opened |
| phase216_test_replay_allowed_next | 0 | No test replay opened |
| phase216_promotion_allowed | 0 | No promotion opened |
| phase216_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase216_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase216_forbidden_outputs | model_fit;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export | Outputs forbidden in this phase |
| phase216_next_best_action | run_phase217_event_only_design_matrix_precommit_no_model_no_replay_no_test | Recommended next milestone |

## Event-only Target Allowlist

| phase216_target_id | label_name | horizon_sec | allowed_split_roles | train_interpretable | validation_interpretable | event_only_filter | positive_rate_min | positive_rate_max | event_surprise_share_min | allowed_for_phase217_design_matrix | model_fit_allowed_now | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P216_EVENT_ONLY_H1s_event_surprise_down_conditional_label | event_surprise_down_conditional_label | 1 | train;validation | 1 | 1 | event_surprise_bucket == 1 | 0.0116941 | 0.0160367 | 0.0760833 | 1 | 0 | 0 | 0 |
| P216_EVENT_ONLY_H1s_event_surprise_up_conditional_label | event_surprise_up_conditional_label | 1 | train;validation | 1 | 1 | event_surprise_bucket == 1 | 0.011833 | 0.0151348 | 0.0760833 | 1 | 0 | 0 | 0 |
| P216_EVENT_ONLY_H1s_event_surprise_vol_expansion_conditional_label | event_surprise_vol_expansion_conditional_label | 1 | train;validation | 1 | 1 | event_surprise_bucket == 1 | 0.0235504 | 0.0313369 | 0.0760833 | 1 | 0 | 0 | 0 |
| P216_EVENT_ONLY_H5s_event_surprise_down_conditional_label | event_surprise_down_conditional_label | 5 | train;validation | 1 | 1 | event_surprise_bucket == 1 | 0.0292557 | 0.0419709 | 0.0966255 | 1 | 0 | 0 | 0 |
| P216_EVENT_ONLY_H5s_event_surprise_up_conditional_label | event_surprise_up_conditional_label | 5 | train;validation | 1 | 1 | event_surprise_bucket == 1 | 0.0289357 | 0.0409329 | 0.0966255 | 1 | 0 | 0 | 0 |
| P216_EVENT_ONLY_H5s_event_surprise_vol_expansion_conditional_label | event_surprise_vol_expansion_conditional_label | 5 | train;validation | 1 | 1 | event_surprise_bucket == 1 | 0.0534895 | 0.0767712 | 0.0966255 | 1 | 0 | 0 | 0 |
| P216_EVENT_ONLY_H15s_event_surprise_vol_expansion_conditional_label | event_surprise_vol_expansion_conditional_label | 15 | train;validation | 1 | 1 | event_surprise_bucket == 1 | 0.0121921 | 0.0130643 | 0.0175807 | 1 | 0 | 0 | 0 |

## Excluded Target Ledger

| phase216_exclusion_id | split_role | horizon_sec | label_name | positive_rate | event_surprise_share | exclusion_reason | excluded_from_phase217_design_matrix | threshold_widening_allowed | model_fit_allowed_now | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P216_EXCLUDE_train_H15s_event_surprise_up_conditional_label | train | 15 | event_surprise_up_conditional_label | 0.00857876 | 0.0190296 | label_positive_rate_outside_event_surprise_interpretation_band | 1 | 0 | 0 | 0 | 0 |
| P216_EXCLUDE_train_H15s_event_surprise_down_conditional_label | train | 15 | event_surprise_down_conditional_label | 0.00809487 | 0.0190296 | label_positive_rate_outside_event_surprise_interpretation_band | 1 | 0 | 0 | 0 | 0 |
| P216_EXCLUDE_train_H60s_event_surprise_up_conditional_label | train | 60 | event_surprise_up_conditional_label | 0.00572075 | 0.0120406 | label_positive_rate_outside_event_surprise_interpretation_band | 1 | 0 | 0 | 0 | 0 |
| P216_EXCLUDE_train_H60s_event_surprise_down_conditional_label | train | 60 | event_surprise_down_conditional_label | 0.00567911 | 0.0120406 | label_positive_rate_outside_event_surprise_interpretation_band | 1 | 0 | 0 | 0 | 0 |
| P216_EXCLUDE_train_H60s_event_surprise_vol_expansion_conditional_label | train | 60 | event_surprise_vol_expansion_conditional_label | 0.00844314 | 0.0120406 | label_positive_rate_outside_event_surprise_interpretation_band | 1 | 0 | 0 | 0 | 0 |
| P216_EXCLUDE_validation_H15s_event_surprise_up_conditional_label | validation | 15 | event_surprise_up_conditional_label | 0.00761485 | 0.0175807 | label_positive_rate_outside_event_surprise_interpretation_band | 1 | 0 | 0 | 0 | 0 |
| P216_EXCLUDE_validation_H15s_event_surprise_down_conditional_label | validation | 15 | event_surprise_down_conditional_label | 0.00746921 | 0.0175807 | label_positive_rate_outside_event_surprise_interpretation_band | 1 | 0 | 0 | 0 | 0 |
| P216_EXCLUDE_validation_H60s_event_surprise_up_conditional_label | validation | 60 | event_surprise_up_conditional_label | 0.00340229 | 0.00779501 | label_positive_rate_outside_event_surprise_interpretation_band | 1 | 0 | 0 | 0 | 0 |
| P216_EXCLUDE_validation_H60s_event_surprise_down_conditional_label | validation | 60 | event_surprise_down_conditional_label | 0.00414589 | 0.00779501 | label_positive_rate_outside_event_surprise_interpretation_band | 1 | 0 | 0 | 0 | 0 |
| P216_EXCLUDE_validation_H60s_event_surprise_vol_expansion_conditional_label | validation | 60 | event_surprise_vol_expansion_conditional_label | 0.00580525 | 0.00779501 | label_positive_rate_outside_event_surprise_interpretation_band | 1 | 0 | 0 | 0 | 0 |

## Event-only Target Contract

| phase216_contract_id | contract | allowed_target_rows | allowed_full_train_validation_target_rows | excluded_split_horizon_label_rows | sealed_test_policy | threshold_widening_allowed | model_fit_allowed_now | strategy_replay_allowed | test_replay_allowed_next | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P216_EVENT_ONLY_TARGET_CONTRACT | Use Phase214 event-surprise labels only on rows where event_surprise_bucket == 1; do not train all-row predictors on sparse conditional labels. | 7 | 7 | 10 | record_inventory_only_zero_rows_used | 0 | 0 | 0 | 0 | 0 |

## Control Contract

| phase216_control_id | control_type | requirement | required_for_phase217 | model_fit_allowed_now | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- |
| P216_EVENT_ONLY_BASE_RATE_CONTROL | base_rate | Phase217 must compute event-only base-rate controls for each allowed label/horizon before any future fit. | 1 | 0 | 0 |
| P216_EVENT_TIME_SHUFFLE_CONTROL | time_shuffle | Phase217 must preserve a shuffled event-time control to test whether event timing matters beyond label base rates. | 1 | 0 | 0 |
| P216_SEALED_TEST_ZERO_USE_CONTROL | sealed_test | Phase217 may inventory sealed test rows but must use zero sealed test rows. | 1 | 0 | 0 |

## Phase217 Work Order

| phase217_work_order_id | work_order | allowed_target_rows | full_train_validation_target_rows | required_control_rows | allowed_next_scope | model_fit_allowed_next | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P217_EVENT_ONLY_DESIGN_MATRIX_PRECOMMIT | Precommit an event-only design matrix using only allowed Phase216 label/horizon rows and event_surprise_bucket == 1 filter. | 7 | 7 | 3 | design_matrix_contract_only_no_model_no_replay_no_test | 0 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase216 | allowed_in_phase216 | rationale |
| --- | --- | --- | --- |
| model_fit | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| model_prediction | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| strategy_replay | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| test_replay_execution | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| test_result | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| promotion | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| paper_live_acceptance | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| order_arrival | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| fill_model | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| pnl_replay | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| profitability_claim | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| threshold_widening | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| row_level_prediction_export | 0 | 0 | Phase216 is an event-only target precommit and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P216_PHASE215_COMPLETE | True | phase215_complete=1 | hard |
| P216_PHASE215_PASSING_ROWS_POSITIVE | True | passing_rows=14 | hard |
| P216_ALLOWLIST_RECORDED | True | allowlist_rows=7; full_train_validation_rows=7 | hard |
| P216_EXCLUSION_LEDGER_RECORDED | True | exclusion_rows=10 | hard |
| P216_EVENT_ONLY_CONTRACT_RECORDED | True | contract_rows=1 | hard |
| P216_CONTROLS_AND_WORK_ORDER_RECORDED | True | controls=3; work_order=1 | hard |
| P216_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; replay_flags=0 | hard |

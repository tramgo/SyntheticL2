# Phase215 Event-surprise Label Quality Interpretation

Generated UTC: 2026-07-28T21:39:16.795259+00:00

Phase215 interprets Phase214 event-surprise label balance and sparsity before any model-fit precommit.
It keeps model fitting, replay, sealed test, promotion, paper/live acceptance, and profitability claims closed.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase215_interpretation_rows | 24 | Split/horizon/label interpretation rows |
| phase215_passing_interpretation_rows | 14 | Rows passing event-only interpretation screen |
| phase215_label_family_summary_rows | 3 | Label-family summary rows |
| phase215_label_families_with_interpretable_rows | 3 | Label families with at least one interpretable row |
| phase215_decision_rows | 1 | Decision ledger rows |
| phase215_phase216_work_order_rows | 1 | Phase216 work-order rows |
| phase215_forbidden_execution_rows | 13 | Forbidden execution rows |
| phase215_gate_rows | 7 | Gates evaluated |
| phase215_hard_gate_rows | 7 | Hard gates evaluated |
| phase215_hard_gate_pass_rows | 7 | Hard gates passed |
| phase215_event_surprise_label_quality_interpretation_complete | 1 | 1 means Phase215 completed |
| phase215_model_fit_allowed_next | 0 | No model fit opened |
| phase215_strategy_replay_allowed | 0 | No strategy replay opened |
| phase215_test_replay_allowed_next | 0 | No test replay opened |
| phase215_promotion_allowed | 0 | No promotion opened |
| phase215_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase215_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase215_forbidden_outputs | model_fit;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export | Outputs forbidden in this phase |
| phase215_next_best_action | run_phase216_event_surprise_label_redesign_or_event_only_target_precommit_no_model_no_replay_no_test | Recommended next milestone |

## Label Quality Interpretation

| phase215_interpretation_id | split_role | horizon_sec | label_name | total_rows | event_surprise_rows | event_surprise_share | positive_rate | sparse_event_surprise_partitions | event_density_pass | positive_rate_interpretation_pass | train_validation_scope_pass | interpretation_pass | verdict | model_fit_allowed_next | strategy_replay_allowed | test_replay_allowed_next | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P215_train_H1s_event_surprise_up_conditional_label | train | 1 | event_surprise_up_conditional_label | 693503 | 52764 | 0.0760833 | 0.011833 | 32 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_train_H1s_event_surprise_down_conditional_label | train | 1 | event_surprise_down_conditional_label | 693503 | 52764 | 0.0760833 | 0.0116941 | 32 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_train_H1s_event_surprise_vol_expansion_conditional_label | train | 1 | event_surprise_vol_expansion_conditional_label | 693503 | 52764 | 0.0760833 | 0.0235504 | 32 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_train_H5s_event_surprise_up_conditional_label | train | 5 | event_surprise_up_conditional_label | 268273 | 25922 | 0.0966255 | 0.0289357 | 32 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_train_H5s_event_surprise_down_conditional_label | train | 5 | event_surprise_down_conditional_label | 268273 | 25922 | 0.0966255 | 0.0292557 | 32 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_train_H5s_event_surprise_vol_expansion_conditional_label | train | 5 | event_surprise_vol_expansion_conditional_label | 268273 | 25922 | 0.0966255 | 0.0534895 | 32 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_train_H15s_event_surprise_up_conditional_label | train | 15 | event_surprise_up_conditional_label | 94169 | 1792 | 0.0190296 | 0.00857876 | 53 | 1 | 0 | 1 | 0 | label_positive_rate_outside_event_surprise_interpretation_band | 0 | 0 | 0 | 0 |
| P215_train_H15s_event_surprise_down_conditional_label | train | 15 | event_surprise_down_conditional_label | 94169 | 1792 | 0.0190296 | 0.00809487 | 53 | 1 | 0 | 1 | 0 | label_positive_rate_outside_event_surprise_interpretation_band | 0 | 0 | 0 | 0 |
| P215_train_H15s_event_surprise_vol_expansion_conditional_label | train | 15 | event_surprise_vol_expansion_conditional_label | 94169 | 1792 | 0.0190296 | 0.0130643 | 53 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_train_H60s_event_surprise_up_conditional_label | train | 60 | event_surprise_up_conditional_label | 23670 | 285 | 0.0120406 | 0.00572075 | 72 | 1 | 0 | 1 | 0 | label_positive_rate_outside_event_surprise_interpretation_band | 0 | 0 | 0 | 0 |
| P215_train_H60s_event_surprise_down_conditional_label | train | 60 | event_surprise_down_conditional_label | 23670 | 285 | 0.0120406 | 0.00567911 | 72 | 1 | 0 | 1 | 0 | label_positive_rate_outside_event_surprise_interpretation_band | 0 | 0 | 0 | 0 |
| P215_train_H60s_event_surprise_vol_expansion_conditional_label | train | 60 | event_surprise_vol_expansion_conditional_label | 23670 | 285 | 0.0120406 | 0.00844314 | 72 | 1 | 0 | 1 | 0 | label_positive_rate_outside_event_surprise_interpretation_band | 0 | 0 | 0 | 0 |
| P215_validation_H1s_event_surprise_up_conditional_label | validation | 1 | event_surprise_up_conditional_label | 363786 | 31457 | 0.0864712 | 0.0151348 | 0 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_validation_H1s_event_surprise_down_conditional_label | validation | 1 | event_surprise_down_conditional_label | 363786 | 31457 | 0.0864712 | 0.0160367 | 0 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_validation_H1s_event_surprise_vol_expansion_conditional_label | validation | 1 | event_surprise_vol_expansion_conditional_label | 363786 | 31457 | 0.0864712 | 0.0313369 | 0 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_validation_H5s_event_surprise_up_conditional_label | validation | 5 | event_surprise_up_conditional_label | 137477 | 17072 | 0.124181 | 0.0409329 | 0 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_validation_H5s_event_surprise_down_conditional_label | validation | 5 | event_surprise_down_conditional_label | 137477 | 17072 | 0.124181 | 0.0419709 | 0 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_validation_H5s_event_surprise_vol_expansion_conditional_label | validation | 5 | event_surprise_vol_expansion_conditional_label | 137477 | 17072 | 0.124181 | 0.0767712 | 0 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_validation_H15s_event_surprise_up_conditional_label | validation | 15 | event_surprise_up_conditional_label | 48064 | 845 | 0.0175807 | 0.00761485 | 4 | 1 | 0 | 1 | 0 | label_positive_rate_outside_event_surprise_interpretation_band | 0 | 0 | 0 | 0 |
| P215_validation_H15s_event_surprise_down_conditional_label | validation | 15 | event_surprise_down_conditional_label | 48064 | 845 | 0.0175807 | 0.00746921 | 4 | 1 | 0 | 1 | 0 | label_positive_rate_outside_event_surprise_interpretation_band | 0 | 0 | 0 | 0 |
| P215_validation_H15s_event_surprise_vol_expansion_conditional_label | validation | 15 | event_surprise_vol_expansion_conditional_label | 48064 | 845 | 0.0175807 | 0.0121921 | 4 | 1 | 1 | 1 | 1 | label_interpretable_for_event_only_precommit_not_model_fit | 0 | 0 | 0 | 0 |
| P215_validation_H60s_event_surprise_up_conditional_label | validation | 60 | event_surprise_up_conditional_label | 12059 | 94 | 0.00779501 | 0.00340229 | 9 | 1 | 0 | 1 | 0 | label_positive_rate_outside_event_surprise_interpretation_band | 0 | 0 | 0 | 0 |
| P215_validation_H60s_event_surprise_down_conditional_label | validation | 60 | event_surprise_down_conditional_label | 12059 | 94 | 0.00779501 | 0.00414589 | 9 | 1 | 0 | 1 | 0 | label_positive_rate_outside_event_surprise_interpretation_band | 0 | 0 | 0 | 0 |
| P215_validation_H60s_event_surprise_vol_expansion_conditional_label | validation | 60 | event_surprise_vol_expansion_conditional_label | 12059 | 94 | 0.00779501 | 0.00580525 | 9 | 1 | 0 | 1 | 0 | label_positive_rate_outside_event_surprise_interpretation_band | 0 | 0 | 0 | 0 |

## Label Family Summary

| phase215_label_family_summary_id | label_name | interpreted_split_horizon_rows | passing_interpretation_rows | min_event_surprise_share | min_positive_rate | max_positive_rate | family_verdict | model_fit_allowed_next | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P215_FAMILY_event_surprise_down_conditional_label | event_surprise_down_conditional_label | 8 | 4 | 0.00779501 | 0.00414589 | 0.0419709 | event_only_target_precommit_required_before_model_fit | 0 | 0 |
| P215_FAMILY_event_surprise_up_conditional_label | event_surprise_up_conditional_label | 8 | 4 | 0.00779501 | 0.00340229 | 0.0409329 | event_only_target_precommit_required_before_model_fit | 0 | 0 |
| P215_FAMILY_event_surprise_vol_expansion_conditional_label | event_surprise_vol_expansion_conditional_label | 8 | 6 | 0.00779501 | 0.00580525 | 0.0767712 | event_only_target_precommit_required_before_model_fit | 0 | 0 |

## Decision Ledger

| phase215_decision_id | passing_interpretation_rows | label_families_with_interpretable_rows | decision | rationale | model_fit_allowed_next | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P215_EVENT_SURPRISE_LABEL_QUALITY_DECISION | 14 | 3 | event_only_target_precommit_required_no_model_fit | Phase214 labels are materialized, but positive rates are sparse and must be interpreted as event-only targets before any model-fit precommit. | 0 | 0 | 0 | 0 | 0 | 0 |

## Phase216 Work Order

| phase216_work_order_id | decision | required_action | allowed_next_scope | model_fit_allowed_next | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- |
| P216_EVENT_ONLY_TARGET_OR_LABEL_REDESIGN_PRECOMMIT | event_only_target_precommit_required_no_model_fit | Precommit whether Phase214 labels should be narrowed to event-only rows or redesigned for better class balance before any model fit. | precommit_only_no_model_no_replay_no_test | 0 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase215 | allowed_in_phase215 | rationale |
| --- | --- | --- | --- |
| model_fit | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| model_prediction | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| strategy_replay | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| test_replay_execution | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| test_result | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| promotion | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| paper_live_acceptance | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| order_arrival | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| fill_model | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| pnl_replay | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| profitability_claim | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| threshold_widening | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| row_level_prediction_export | 0 | 0 | Phase215 interprets label quality only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P215_PHASE214_COMPLETE | True | phase214_complete=1 | hard |
| P215_SEALED_TEST_STILL_UNUSED | True | sealed_test_rows_used=0 | hard |
| P215_INTERPRETATION_ROWS_RECORDED | True | interpretation_rows=24 | hard |
| P215_LABEL_FAMILY_SUMMARY_RECORDED | True | family_rows=3 | hard |
| P215_DECISION_LEDGER_RECORDED | True | decision_rows=1 | hard |
| P215_PHASE216_WORK_ORDER_RECORDED | True | work_order_rows=1 | hard |
| P215_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; replay_flags=0 | hard |

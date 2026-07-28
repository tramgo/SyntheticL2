# Phase213 Material New Model Source Precommit

Generated UTC: 2026-07-28T21:26:27.228636+00:00

Phase213 selects a materially new source after Phase212 closed the current model families for replay.
It precommits an event-surprise conditional label source and a Phase214 materialization work order without fitting models, running replay, using sealed test, or making profitability claims.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase213_source_selection_rows | 1 | Material-new-source selection rows |
| phase213_selected_source_id | P213_EVENT_SURPRISE_CONDITIONAL_LABEL_SOURCE | Selected material source |
| phase213_label_contract_rows | 3 | Conditional label contract rows |
| phase213_feature_requirement_rows | 3 | Feature requirement rows |
| phase213_control_contract_rows | 3 | Control contract rows |
| phase213_phase214_work_order_rows | 1 | Phase214 work-order rows |
| phase213_forbidden_execution_rows | 13 | Forbidden execution rows |
| phase213_gate_rows | 8 | Gates evaluated |
| phase213_hard_gate_rows | 8 | Hard gates evaluated |
| phase213_hard_gate_pass_rows | 8 | Hard gates passed |
| phase213_material_new_model_source_precommit_complete | 1 | 1 means Phase213 completed |
| phase213_model_fit_allowed_next | 0 | No model fit opened |
| phase213_strategy_replay_allowed | 0 | No strategy replay opened |
| phase213_test_replay_allowed_next | 0 | No test replay opened |
| phase213_promotion_allowed | 0 | No promotion opened |
| phase213_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase213_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase213_forbidden_outputs | model_fit;model_prediction;strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export | Outputs forbidden in this phase |
| phase213_next_best_action | run_phase214_event_surprise_label_contract_materialization_no_model_no_replay_no_test | Recommended next milestone |

## Material Source Selection

| phase213_source_id | phase212_redesign_id | selection_rank | selected_for_phase214 | source_type | source_theme | source_description | why_materially_different | phase211_failure_addressed | non_selected_alternatives_preserved | model_fit_allowed_now | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P213_EVENT_SURPRISE_CONDITIONAL_LABEL_SOURCE | P212_EVENT_SURPRISE_CONDITIONAL_LABEL_SOURCE | 1 | 1 | material_new_conditional_label_source | material_new_label_source | Define labels around receive-event surprise conditional on symbol/date liquidity regime, not raw next-bucket direction. | Moves from broad base-rate labels to conditional event-surprise labels designed to defeat shuffled-target/base-rate controls. | control_like_mse;weak_global_correlation;base_rate_accuracy | P212_REGIME_STRATIFIED_FEATURE_SOURCE;P212_CROSS_SECTIONAL_RELATIVE_FLOW_SOURCE | 0 | 0 | 0 | 0 | 0 | 0 |

## Conditional Label Contract

| phase213_label_contract_id | label_name | label_definition | conditioning_fields | balance_requirement | control_requirement | materialization_allowed_next | model_fit_allowed_now | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P213_EVENT_SURPRISE_UP_LABEL | event_surprise_up_conditional_label | Future mid-return exceeds same-symbol/date liquidity-regime conditional baseline after a receive-event surprise bucket. | symbol;trade_date;horizon_sec;spread_regime;liquidity_regime;receive_event_rate_zscore_bucket | validation_positive_rate_between_0p35_and_0p65_or_abstain | shuffled_target_control;shuffled_event_time_control;base_rate_accuracy_control | 1 | 0 | 0 |
| P213_EVENT_SURPRISE_DOWN_LABEL | event_surprise_down_conditional_label | Future mid-return underperforms same-symbol/date liquidity-regime conditional baseline after a receive-event surprise bucket. | symbol;trade_date;horizon_sec;spread_regime;liquidity_regime;receive_event_rate_zscore_bucket | validation_positive_rate_between_0p35_and_0p65_or_abstain | shuffled_target_control;shuffled_event_time_control;base_rate_accuracy_control | 1 | 0 | 0 |
| P213_EVENT_SURPRISE_VOL_EXPANSION_LABEL | event_surprise_vol_expansion_conditional_label | Future absolute return or spread expansion exceeds conditional baseline after receive-event surprise. | symbol;trade_date;horizon_sec;spread_regime;liquidity_regime;receive_event_rate_zscore_bucket | validation_positive_rate_between_0p35_and_0p65_or_abstain | shuffled_target_control;shuffled_event_time_control;base_rate_accuracy_control | 1 | 0 | 0 |

## Feature Requirement Contract

| phase213_feature_requirement_id | required_feature_source | requirement | leakage_control | required_for_phase214 | model_fit_allowed_now | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| P213_RECEIVE_EVENT_SURPRISE_BUCKETS | phase176_receive_event_rate_zscore;receive_event_count;receive_event_rate_baseline_days | Create causal receive-event surprise buckets from prior-date baselines only. | bucket assignment must use only current/past receive timestamps and prior-date baseline state | 1 | 0 | 0 |
| P213_LIQUIDITY_REGIME_BUCKETS | spread;top5_qty_imbalance;stale_quote_duration_ms;quote_churn_count | Create causal spread/liquidity/churn regimes for conditional baselines. | regime state must be computed at or before feature bucket timestamp | 1 | 0 | 0 |
| P213_CONDITIONAL_BASELINE_STATE | train_only_symbol_date_horizon_regime_baselines | Estimate label baselines on train split only; validation uses frozen train baselines; sealed test unused. | no validation/test target values in baseline estimation | 1 | 0 | 0 |

## Control Contract

| phase213_control_id | control_type | requirement | required_before_model_fit | test_replay_allowed_next |
| --- | --- | --- | --- | --- |
| P213_BALANCED_BASE_RATE_CONTROL | base_rate | Report class balance by split/horizon/regime and reject labels where validation base-rate dominates. | 1 | 0 |
| P213_SHUFFLED_EVENT_TIME_CONTROL | time_shuffle | Shuffle receive-event surprise bucket times within symbol/date before interpretation. | 1 | 0 |
| P213_TRAIN_BASELINE_ONLY_CONTROL | leakage_control | Prove conditional baselines are estimated from train split only and sealed test remains unused. | 1 | 0 |

## Phase214 Work Order

| phase214_work_order_id | phase213_source_id | work_order | label_contract_rows | feature_requirement_rows | control_rows | allowed_next_scope | model_fit_allowed_next | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P214_EVENT_SURPRISE_CONDITIONAL_LABEL_MATERIALIZATION | P213_EVENT_SURPRISE_CONDITIONAL_LABEL_SOURCE | Materialize event-surprise conditional label contract over train/validation partitions only, with sealed test inventory recorded but unused. | 3 | 3 | 3 | label_contract_materialization_and_quality_no_model_no_replay_no_test | 0 | 0 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase213 | allowed_in_phase213 | rationale |
| --- | --- | --- | --- |
| model_fit | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| model_prediction | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| strategy_replay | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| test_replay_execution | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| test_result | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| promotion | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| paper_live_acceptance | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| order_arrival | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| fill_model | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| pnl_replay | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| profitability_claim | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| threshold_widening | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |
| row_level_prediction_export | 0 | 0 | Phase213 is a material-new-source precommit only and emits no model, prediction, replay, order/fill/P&L, promotion, or paper/live artifact. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P213_PHASE212_COMPLETE | True | phase212_complete=1 | hard |
| P213_CURRENT_FAMILIES_CLOSED | True | families_closed=3 | hard |
| P213_MATERIAL_SOURCE_SELECTED | True | selection_rows=1 | hard |
| P213_LABEL_CONTRACT_RECORDED | True | label_contract_rows=3 | hard |
| P213_FEATURE_REQUIREMENTS_RECORDED | True | feature_requirement_rows=3 | hard |
| P213_CONTROL_CONTRACT_RECORDED | True | control_rows=3 | hard |
| P213_PHASE214_WORK_ORDER_RECORDED | True | work_order_rows=1 | hard |
| P213_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; replay_flags=0 | hard |

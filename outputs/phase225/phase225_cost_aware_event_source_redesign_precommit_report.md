# Phase225 Cost-aware Event Source Redesign Precommit

Generated UTC: 2026-07-29T05:28:32.011315+00:00

Phase225 freezes a cost-aware actionable event label/source redesign before any label materialization, model fit, replay, broader replay, or sealed test.
The key move is economic: labels must clear the Zerodha cost/latency hurdle before they are allowed to become candidates.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase225_cost_hurdle_rows | 2 | Cost hurdle contract rows |
| phase225_label_contract_rows | 3 | Cost-aware label contract rows |
| phase225_negative_control_rows | 3 | Negative-control contract rows |
| phase225_phase226_work_order_rows | 1 | Phase226 work-order rows |
| phase225_selected_route_id | P224_COST_AWARE_ACTIONABLE_EVENT_LABELS | Selected redesign route |
| phase225_label_materialization_allowed_next | 1 | Label materialization allowed next |
| phase225_model_fit_allowed_next | 0 | No model fit opened |
| phase225_strategy_replay_allowed | 0 | No strategy replay opened |
| phase225_broader_replay_allowed_next | 0 | No broader replay opened |
| phase225_test_replay_allowed_next | 0 | No test replay opened |
| phase225_test_rows_used | 0 | No sealed test rows used |
| phase225_promotion_allowed | 0 | No promotion opened |
| phase225_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase225_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase225_forbidden_execution_rows | 16 | Forbidden execution rows |
| phase225_gate_rows | 7 | Gates evaluated |
| phase225_hard_gate_rows | 7 | Hard gates evaluated |
| phase225_hard_gate_pass_rows | 7 | Hard gates passed |
| phase225_cost_aware_event_source_redesign_precommit_complete | 1 | 1 means Phase225 completed |
| phase225_forbidden_outputs | label_materialization;feature_materialization;model_fit;model_prediction;strategy_replay;broader_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export | Outputs forbidden in this phase |
| phase225_next_best_action | run_phase226_cost_aware_event_label_materialization_dry_run_no_fit_no_replay_no_test | Recommended next milestone |

## Cost Hurdle Contract

| phase225_cost_hurdle_id | latency_profile_id | hurdle_role | minimum_forward_edge_bps_rule | statutory_cost_catalog_rows_bound | latency_profile_rows_bound | target_net_after_cost_floor_bps | safety_margin_bps | label_positive_condition | label_negative_condition | neutral_condition | model_fit_allowed_now | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P225_COST_HURDLE_RETAIL_MARKETABLE | P180_RETAIL_MARKETABLE_DEFAULT | primary_train_validation_acceptance_hurdle | gross_forward_move_bps_must_exceed_phase180_statutory_cost_plus_spread_latency_slippage_bound | 26 | 1 | 0 | 1 | forward_signed_move_bps - estimated_cost_bound_bps >= 1.0 | forward_signed_move_bps + estimated_cost_bound_bps <= -1.0 | otherwise_no_action_label | 0 | 0 | 0 |
| P225_COST_HURDLE_STRESSED_RETAIL | P180_STRESSED_RETAIL | stress_acceptance_hurdle | candidate_must_remain_nonnegative_under_stressed_retail_bound_before_replay_precommit | 26 | 1 | 0 | 0 | forward_signed_move_bps - stressed_estimated_cost_bound_bps >= 0.0 | forward_signed_move_bps + stressed_estimated_cost_bound_bps <= 0.0 | otherwise_no_action_label | 0 | 0 | 0 |

## Label Contract

| phase225_label_contract_id | label_family | horizon_sec | source_event_filter | price_reference | directional_labels | positive_label_rule | negative_label_rule | neutral_label_rule | minimum_event_count_per_split | minimum_symbol_count_per_split | minimum_trade_date_count_per_split | allowed_splits | sealed_test_rows_used | threshold_widening_allowed | model_fit_allowed_now | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P225_COST_AWARE_EVENT_MOVE_H5s | cost_aware_actionable_event_move | 5 | event_surprise_bucket == 1 | last_price_at_event_to_future_mid_or_last_price_proxy | cost_aware_up;cost_aware_down;neutral_no_action | future_up_move_bps_exceeds_retail_cost_hurdle_and_stress_nonnegative | future_down_move_bps_exceeds_retail_cost_hurdle_and_stress_nonnegative | forward_move_does_not_clear_cost_hurdle | 1000 | 8 | 5 | train;validation | 0 | 0 | 0 | 0 | 0 |
| P225_COST_AWARE_EVENT_MOVE_H15s | cost_aware_actionable_event_move | 15 | event_surprise_bucket == 1 | last_price_at_event_to_future_mid_or_last_price_proxy | cost_aware_up;cost_aware_down;neutral_no_action | future_up_move_bps_exceeds_retail_cost_hurdle_and_stress_nonnegative | future_down_move_bps_exceeds_retail_cost_hurdle_and_stress_nonnegative | forward_move_does_not_clear_cost_hurdle | 1000 | 8 | 5 | train;validation | 0 | 0 | 0 | 0 | 0 |
| P225_COST_AWARE_EVENT_MOVE_H30s | cost_aware_actionable_event_move | 30 | event_surprise_bucket == 1 | last_price_at_event_to_future_mid_or_last_price_proxy | cost_aware_up;cost_aware_down;neutral_no_action | future_up_move_bps_exceeds_retail_cost_hurdle_and_stress_nonnegative | future_down_move_bps_exceeds_retail_cost_hurdle_and_stress_nonnegative | forward_move_does_not_clear_cost_hurdle | 1000 | 8 | 5 | train;validation | 0 | 0 | 0 | 0 | 0 |

## Negative Control Contract

| phase225_control_id | control_type | purpose | required_before_fit | pass_condition | model_fit_allowed_now | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| P225_CONTROL_EVENT_TIME_SHUFFLE | event_time_shuffle_within_symbol_date_split | Reject labels whose apparent signal survives only because of event timing leakage or base-rate structure. | 1 | model_or_screen_must_beat_shuffled_control_on_validation_before_replay_precommit | 0 | 0 |
| P225_CONTROL_SYMBOL_DATE_BASE_RATE | symbol_date_base_rate | Reject labels explained by symbol/date unconditional actionability rates. | 1 | validation lift must exceed symbol-date base-rate control | 0 | 0 |
| P225_CONTROL_COST_HURDLE_ABLATION | cost_hurdle_ablation | Quantify whether cost-aware labels materially reduce churn versus pre-cost event-only labels. | 1 | activation budget and positive-label rate must remain above minimum counts after cost hurdle | 0 | 0 |

## Phase226 Work Order

| phase226_work_order_id | work_order | label_contract_rows | negative_control_rows | required_inputs | required_outputs | allowed_next_scope | label_materialization_allowed_next | model_fit_allowed_next | strategy_replay_allowed | broader_replay_allowed_next | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P226_COST_AWARE_EVENT_LABEL_MATERIALIZATION_DRY_RUN | Materialize train/validation-only cost-aware actionable event labels using Phase225 frozen label and control contracts. | 3 | 3 | phase176_features;phase214_event_surprise_labels;phase180_cost_latency_catalogs | label_partition_inventory;quality_summary;control_summary;acceptance_summary | label_materialization_dry_run_only_no_fit_no_replay_no_test | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase225 | allowed_in_phase225 | rationale |
| --- | --- | --- | --- |
| label_materialization | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| feature_materialization | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| model_fit | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| model_prediction | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| strategy_replay | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| broader_replay | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| test_replay_execution | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| test_result | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| promotion | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| paper_live_acceptance | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| order_arrival | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| fill_model | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| pnl_replay | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| profitability_claim | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| threshold_widening | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |
| row_level_prediction_export | 0 | 0 | Phase225 precommits source/label/control contracts only and emits no materialized labels, fit, prediction, replay, test, order/fill, P&L, promotion, paper/live, threshold-widening, or profitability artifact. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P225_PHASE224_COMPLETE | True | phase224_complete=1 | hard |
| P225_SELECTED_ROUTE_BOUND | True | phase224_selected=P224_COST_AWARE_ACTIONABLE_EVENT_LABELS; work_selected=P224_COST_AWARE_ACTIONABLE_EVENT_LABELS | hard |
| P225_COST_HURDLES_BOUND | True | cost_hurdle_rows=2; cost_rows=26; latency_rows=2 | hard |
| P225_LABEL_CONTRACT_RECORDED | True | label_rows=3 | hard |
| P225_NEGATIVE_CONTROLS_RECORDED | True | control_rows=3 | hard |
| P225_PHASE226_MATERIALIZATION_WORK_ORDER_RECORDED | True | work_order_rows=1; materialization_next=1 | hard |
| P225_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; forbidden_flags=0 | hard |

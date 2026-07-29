# Phase221 Event-only Signal Replay Precommit-or-stop

Generated UTC: 2026-07-29T04:56:51.828316+00:00

Phase221 freezes Phase220 passing candidates and precommits a train/validation-only signal replay dry-run contract for Phase222.
It does not execute replay, use sealed test, emit predictions, compute P&L, promote anything, open paper/live acceptance, or make profitability claims.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase221_decision_rows | 1 | Decision rows |
| phase221_candidate_rows | 5 | Frozen candidate rows |
| phase221_signal_rule_rows | 5 | Signal rule contract rows |
| phase221_replay_contract_rows | 1 | Replay precommit contract rows |
| phase221_phase222_work_order_rows | 1 | Phase222 work-order rows |
| phase221_forbidden_execution_rows | 11 | Forbidden execution rows |
| phase221_gate_rows | 8 | Gates evaluated |
| phase221_hard_gate_rows | 8 | Hard gates evaluated |
| phase221_hard_gate_pass_rows | 8 | Hard gates passed |
| phase221_event_only_signal_replay_precommit_or_stop_complete | 1 | 1 means Phase221 completed |
| phase221_phase222_replay_dry_run_precommitted | 1 | 1 means Phase222 may execute train/validation replay dry run |
| phase221_strategy_replay_execution_allowed | 0 | No strategy replay execution in Phase221 |
| phase221_strategy_replay_allowed_next | 1 | 1 means next phase may execute gated train/validation replay |
| phase221_test_replay_allowed_next | 0 | No test replay opened |
| phase221_promotion_allowed | 0 | No promotion opened |
| phase221_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase221_profitability_claim_allowed | 0 | No profitability claim is allowed |
| phase221_forbidden_outputs | strategy_replay_execution;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim;threshold_widening;row_level_prediction_export | Outputs forbidden in this phase |
| phase221_next_best_action | run_phase222_event_only_train_validation_signal_replay_dry_run_no_test | Recommended next milestone |

## Decision

| phase221_decision_id | decision | phase220_complete | passing_candidate_rows | candidate_model_families | candidate_family_rows | best_mse_improvement_vs_base | best_improvement_vs_shuffle | best_validation_correlation | phase222_replay_dry_run_precommitted | strategy_replay_execution_allowed_phase221 | strategy_replay_allowed_next | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P221_PRECOMMIT_EVENT_ONLY_TRAIN_VALIDATION_REPLAY_DRY_RUN | precommit_phase222_event_only_train_validation_signal_replay_dry_run | 1 | 5 | low_depth_tree_or_stump_diagnostic | 1 | 0.0100934 | 0.01073 | 0.220575 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |

## Frozen Candidate Contract

| phase221_candidate_id | phase219_model_fit_id | model_family | target_label | horizon_sec | rows | positive_rate | mse_improvement_vs_base | improvement_vs_shuffle | correlation | binary_accuracy | candidate_frozen_for_phase222 | threshold_widening_allowed | strategy_replay_execution_allowed_phase221 | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P221_CANDIDATE_01 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 1 | 31457 | 0.378231 | 0.0100934 | 0.01073 | 0.220575 | 0.622405 | 1 | 0 | 0 | 0 |
| P221_CANDIDATE_02 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_vol_expansion_conditional_label | 5 | 17072 | 0.622247 | 0.00904191 | 0.00990177 | 0.20407 | 0.629276 | 1 | 0 | 0 | 0 |
| P221_CANDIDATE_03 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_up_conditional_label | 5 | 17072 | 0.33224 | 0.00545801 | 0.00542716 | 0.160105 | 0.66776 | 1 | 0 | 0 | 0 |
| P221_CANDIDATE_04 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 5 | 17072 | 0.340382 | 0.00521501 | 0.00496794 | 0.157466 | 0.65956 | 1 | 0 | 0 | 0 |
| P221_CANDIDATE_05 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | low_depth_tree_or_stump_diagnostic | event_surprise_down_conditional_label | 1 | 31457 | 0.193375 | 0.00335315 | 0.00392368 | 0.159248 | 0.806625 | 1 | 0 | 0 | 0 |

## Signal Rule Contract

| phase221_signal_rule_id | phase221_candidate_id | phase219_model_fit_id | target_label | horizon_sec | signal_direction_policy | entry_filter | threshold_policy | max_threshold_grid_values | position_sizing_policy | row_level_prediction_export_allowed | strategy_replay_execution_allowed_phase221 | test_replay_allowed_next | promotion_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P221_SIGNAL_RULE_01 | P221_CANDIDATE_01 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H1s | event_surprise_vol_expansion_conditional_label | 1 | event_only_probability_score_ranked_direction_for_target_label | event_surprise_bucket == 1 and validation_precommitted_candidate_only | phase222_train_validation_diagnostic_threshold_grid_predeclared_no_test | 0.55;0.60;0.65;0.70 | unit_notional_diagnostic_only | 0 | 0 | 0 | 0 |
| P221_SIGNAL_RULE_02 | P221_CANDIDATE_02 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_vol_expansion_conditional_label_H5s | event_surprise_vol_expansion_conditional_label | 5 | event_only_probability_score_ranked_direction_for_target_label | event_surprise_bucket == 1 and validation_precommitted_candidate_only | phase222_train_validation_diagnostic_threshold_grid_predeclared_no_test | 0.55;0.60;0.65;0.70 | unit_notional_diagnostic_only | 0 | 0 | 0 | 0 |
| P221_SIGNAL_RULE_03 | P221_CANDIDATE_03 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_up_conditional_label_H5s | event_surprise_up_conditional_label | 5 | event_only_probability_score_ranked_direction_for_target_label | event_surprise_bucket == 1 and validation_precommitted_candidate_only | phase222_train_validation_diagnostic_threshold_grid_predeclared_no_test | 0.55;0.60;0.65;0.70 | unit_notional_diagnostic_only | 0 | 0 | 0 | 0 |
| P221_SIGNAL_RULE_04 | P221_CANDIDATE_04 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H5s | event_surprise_down_conditional_label | 5 | event_only_probability_score_ranked_direction_for_target_label | event_surprise_bucket == 1 and validation_precommitted_candidate_only | phase222_train_validation_diagnostic_threshold_grid_predeclared_no_test | 0.55;0.60;0.65;0.70 | unit_notional_diagnostic_only | 0 | 0 | 0 | 0 |
| P221_SIGNAL_RULE_05 | P221_CANDIDATE_05 | P219_P218_EVENT_ONLY_TREE_STUMP_DIAGNOSTIC_event_surprise_down_conditional_label_H1s | event_surprise_down_conditional_label | 1 | event_only_probability_score_ranked_direction_for_target_label | event_surprise_bucket == 1 and validation_precommitted_candidate_only | phase222_train_validation_diagnostic_threshold_grid_predeclared_no_test | 0.55;0.60;0.65;0.70 | unit_notional_diagnostic_only | 0 | 0 | 0 | 0 |

## Replay Cost Latency Contract

| phase221_replay_contract_id | contract | candidate_rows | cost_component_rows_required | latency_profile_rows_required | allowed_splits | sealed_test_rows_used | strategy_replay_execution_allowed_phase221 | strategy_replay_execution_allowed_phase222 | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P221_EVENT_ONLY_TRAIN_VALIDATION_REPLAY_CONTRACT | Phase222 may run only train/validation diagnostic signal replay for frozen Phase221 candidates, with Phase180 Zerodha cost components and latency/slippage profiles bound before any net metric. | 5 | 26 | 3 | train;validation | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

## Phase222 Work Order

| phase222_work_order_id | work_order | phase222_replay_dry_run_precommitted | candidate_rows | signal_rule_rows | replay_contract_rows | allowed_next_scope | strategy_replay_execution_allowed_phase222 | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed | profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P222_EVENT_ONLY_TRAIN_VALIDATION_SIGNAL_REPLAY_DRY_RUN | Run train/validation-only event-only signal replay for frozen Phase221 candidates with Phase180 costs/latency; no sealed test, no promotion, no paper/live, no profitability claim. | 1 | 5 | 5 | 1 | train_validation_signal_replay_dry_run_no_test | 1 | 0 | 0 | 0 | 0 |

## Forbidden Execution Ledger

| forbidden_output | emitted_in_phase221 | allowed_in_phase221 | rationale |
| --- | --- | --- | --- |
| strategy_replay_execution | 0 | 0 | Phase221 precommits a future replay contract only and emits no replay, test, promotion, P&L, prediction export, paper/live, or profitability artifact. |
| test_replay_execution | 0 | 0 | Phase221 precommits a future replay contract only and emits no replay, test, promotion, P&L, prediction export, paper/live, or profitability artifact. |
| test_result | 0 | 0 | Phase221 precommits a future replay contract only and emits no replay, test, promotion, P&L, prediction export, paper/live, or profitability artifact. |
| promotion | 0 | 0 | Phase221 precommits a future replay contract only and emits no replay, test, promotion, P&L, prediction export, paper/live, or profitability artifact. |
| paper_live_acceptance | 0 | 0 | Phase221 precommits a future replay contract only and emits no replay, test, promotion, P&L, prediction export, paper/live, or profitability artifact. |
| order_arrival | 0 | 0 | Phase221 precommits a future replay contract only and emits no replay, test, promotion, P&L, prediction export, paper/live, or profitability artifact. |
| fill_model | 0 | 0 | Phase221 precommits a future replay contract only and emits no replay, test, promotion, P&L, prediction export, paper/live, or profitability artifact. |
| pnl_replay | 0 | 0 | Phase221 precommits a future replay contract only and emits no replay, test, promotion, P&L, prediction export, paper/live, or profitability artifact. |
| profitability_claim | 0 | 0 | Phase221 precommits a future replay contract only and emits no replay, test, promotion, P&L, prediction export, paper/live, or profitability artifact. |
| threshold_widening | 0 | 0 | Phase221 precommits a future replay contract only and emits no replay, test, promotion, P&L, prediction export, paper/live, or profitability artifact. |
| row_level_prediction_export | 0 | 0 | Phase221 precommits a future replay contract only and emits no replay, test, promotion, P&L, prediction export, paper/live, or profitability artifact. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P221_PHASE220_COMPLETE | True | phase220_complete=1 | hard |
| P221_DECISION_RECORDED | True | decision_rows=1; phase222_precommitted=1 | hard |
| P221_CANDIDATES_FROZEN | True | candidate_rows=5 | hard |
| P221_SIGNAL_RULE_CONTRACT_RECORDED | True | signal_rule_rows=5; candidate_rows=5 | hard |
| P221_REPLAY_COST_LATENCY_CONTRACT_RECORDED | True | replay_contract_rows=1 | hard |
| P221_PHASE222_WORK_ORDER_RECORDED | True | work_order_rows=1 | hard |
| P221_PHASE221_REPLAY_EXECUTION_CLOSED | True | phase221_replay_execution=0 | hard |
| P221_FORBIDDEN_OUTPUTS_CLEAN | True | forbidden_emitted=0; replay_flags=0 | hard |

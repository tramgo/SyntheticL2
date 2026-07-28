# Phase191 Diagnostic Test Replay Precommit

Generated UTC: 2026-07-28T17:17:15.018163+00:00

Phase191 freezes the diagnostic-test replay contract but does not execute test replay.
The candidate, command contract and abort rules are explicit so any later diagnostic test run cannot silently reselect or promote.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase191_candidate_contract_rows | 1 | Frozen candidate contract rows |
| phase191_future_command_contract_rows | 1 | Future command contract rows |
| phase191_abort_rule_rows | 5 | Abort rule rows |
| phase191_precommit_matrix_rows | 6 | Precommit matrix rows |
| phase191_candidate_id | P187_TOP5_I85_S2p5_Z1_R100 | Frozen candidate |
| phase191_candidate_contract_hash | 6aec9abe7f1da4c49372eb44b3fa050e44c1b8105dd4bc0c47efd9357af697d1 | Frozen candidate hash |
| phase191_gate_rows | 5 | Gates evaluated |
| phase191_hard_gate_rows | 5 | Hard gates evaluated |
| phase191_hard_gate_pass_rows | 5 | Hard gates passed |
| phase191_diagnostic_test_precommit_complete | 1 | 1 means diagnostic precommit completed |
| phase191_test_replay_execution | 0 | No test replay executed |
| phase191_test_result_allowed | 0 | No test result emitted |
| phase191_test_replay_allowed_next | 0 | No test replay opened by Phase191 |
| phase191_promotion_allowed | 0 | No promotion opened |
| phase191_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase191_forbidden_outputs | test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim | Outputs forbidden in this phase |
| phase191_next_best_action | either_add_real_validation_date_or_explicitly_authorize_phase192_diagnostic_test_replay | Recommended next milestone |

## Frozen Candidate Contract

| candidate_id | imbalance_source | min_abs_imbalance | max_spread_bps | min_abs_event_zscore | max_decision_rate | allowed_latency_profiles | candidate_contract_hash | selection_source_phase | validation_interpretation_phase | test_precommit_decision_phase | diagnostic_spec_phase | may_change_before_test_replay | test_replay_execution_allowed_by_phase191 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P187_TOP5_I85_S2p5_Z1_R100 | top5 | 0.85 | 2.5 | 1 | 0.01 | P180_RETAIL_MARKETABLE_DEFAULT;P180_STRESSED_RETAIL | 6aec9abe7f1da4c49372eb44b3fa050e44c1b8105dd4bc0c47efd9357af697d1 | phase187_train_only | phase188 | phase189 | phase190 | 0 | 0 |

## Future Command Contract

| command_contract_id | future_runner | allowed_phase | required_candidate_contract_hash | required_split_role | allowed_latency_profiles | negative_controls_required | may_emit_test_result_in_phase191 | may_emit_orders_or_fills | may_open_promotion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P191_FUTURE_RUNNER | scripts/run_phase192_diagnostic_test_replay.py | phase192_or_later_only | 6aec9abe7f1da4c49372eb44b3fa050e44c1b8105dd4bc0c47efd9357af697d1 | test_untouched | P180_RETAIL_MARKETABLE_DEFAULT;P180_STRESSED_RETAIL | shuffled_time;shuffled_symbol | 0 | 0 | 0 |

## Abort Rules

| abort_rule_id | condition | action |
| --- | --- | --- |
| P191_HASH_MISMATCH | candidate_contract_hash_at_execution != phase191_required_candidate_contract_hash | abort_before_reading_test_rows |
| P191_SPLIT_MISMATCH | any_input_row_split_role != test_untouched | abort_and_mark_test_contaminated |
| P191_COST_LATENCY_MISSING | any_net_metric_without_phase180_retail_or_stressed_profile | invalidate_result |
| P191_NEGATIVE_CONTROLS_MISSING | missing_shuffled_time_or_shuffled_symbol_control | block_interpretation |
| P191_PROMOTION_ATTEMPT | paper_live_acceptance_or_promotion_opened_from_diagnostic_test | invalidate_and_return_to_precommit |

## Precommit Matrix

| precommit_item | observed | required | pass |
| --- | --- | --- | --- |
| phase189_decision_complete | 1 | 1 | 1 |
| phase190_diagnostic_spec_written | 1 | 1 | 1 |
| candidate_frozen | 1 | 1 | 1 |
| future_command_declared | 1 | 1 | 1 |
| abort_rules_declared | 5 | 5 | 1 |
| phase191_test_execution_closed | 0 | 0 | 1 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P191_PREVIOUS_PRECOMMIT_CHAIN_PASS | 1 | matrix_pass_rows=6/6 | hard |
| P191_CANDIDATE_HASH_DECLARED | 1 | candidate_rows=1 | hard |
| P191_FUTURE_COMMAND_CONTRACT_DECLARED | 1 | command_rows=1 | hard |
| P191_TEST_REPLAY_EXECUTION_CLOSED | 1 | test_replay_execution=0 | hard |
| P191_PROMOTION_AND_PAPER_LIVE_CLOSED | 1 | promotion_allowed=0; paper_live_acceptance_allowed=0 | hard |

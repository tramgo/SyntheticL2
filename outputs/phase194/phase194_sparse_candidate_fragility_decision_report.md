# Phase194 Sparse Candidate Fragility Decision

Generated UTC: 2026-07-28T18:53:03.616043+00:00

Phase194 turns the Phase193 validation-extension evidence into a no-test research decision.
It closes the frozen sparse candidate for test replay and writes redesign gates.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase194_decision_rows | 1 | Fragility decision rows |
| phase194_blueprint_rows | 3 | Redesign blueprint rows |
| phase194_gate_rows | 6 | Gates evaluated |
| phase194_hard_gate_rows | 6 | Hard gates evaluated |
| phase194_hard_gate_pass_rows | 6 | Hard gates passed |
| phase194_candidate_id | P187_TOP5_I85_S2p5_Z1_R100 | Candidate assessed |
| phase194_extension_validation_dates | 2026-07-15;2026-07-16 | Extension dates in decision |
| phase194_all_extension_profile_dates_negative | 1 | 1 means every extension profile/date row is net negative |
| phase194_decision | close_frozen_sparse_candidate_for_test_replay_redesign_required | Decision |
| phase194_fragility_decision_complete | 1 | 1 means Phase194 completed |
| phase194_test_replay_allowed_next | 0 | No test replay opened |
| phase194_promotion_allowed | 0 | No promotion opened |
| phase194_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase194_forbidden_outputs | test_result;test_replay_execution;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim | Outputs forbidden in this phase |
| phase194_next_best_action | redesign_receive_flow_candidate_with_date_and_symbol_breadth_gates_before_test | Recommended next milestone |

## Fragility Decision

| candidate_id | candidate_contract_hash | original_validation_dates | extension_validation_dates | latency_profiles_evaluated | extension_profile_date_rows | negative_extension_profile_date_rows | all_extension_profile_dates_negative | original_validation_positive_all_profiles | phase193_min_profile_net_bps_proxy_mean | phase193_verdict | phase194_decision | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P187_TOP5_I85_S2p5_Z1_R100 | 6aec9abe7f1da4c49372eb44b3fa050e44c1b8105dd4bc0c47efd9357af697d1 | 2026-07-13 | 2026-07-15;2026-07-16 | P180_RETAIL_MARKETABLE_DEFAULT;P180_STRESSED_RETAIL | 4 | 4 | 1 | 1 | 9.0853 | validation_extension_mixed_or_negative_by_date_add_more_validation_or_redesign_before_test | close_frozen_sparse_candidate_for_test_replay_redesign_required | 0 | 0 | 0 |

## Redesign Blueprint

| blueprint_id | closed_candidate_id | design_change | rationale | required_gate |
| --- | --- | --- | --- | --- |
| P194_REGIME_CONSISTENT_RECEIVE_FLOW | P187_TOP5_I85_S2p5_Z1_R100 | Require candidate to be net positive by date under both retail latency profiles before any test precommit. | The frozen sparse candidate was positive on the original validation date but negative on every added validation-extension profile/date row. | date_positive_fraction_equals_1_before_test_precommit |
| P194_SYMBOL_BREADTH_FILTER | P187_TOP5_I85_S2p5_Z1_R100 | Penalize or reject candidates with symbol-positive fraction below 25 percent, even when aggregate net is positive. | Phase193 symbol-positive fraction remained about 6.45 percent, indicating narrow symbol support. | symbol_positive_fraction_ge_0p25 |
| P194_EXTENSION_FIRST_SELECTION_DISCIPLINE | P187_TOP5_I85_S2p5_Z1_R100 | Use train-only selection, validation for screening, validation-extension for rejection, and keep test untouched until all validation-extension gates pass. | Avoid letting one strong validation date dominate the decision and accidentally spend the only untouched test split. | test_replay_allowed_next_equals_0_until_extension_pass |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P194_PHASE193_EVIDENCE_PRESENT | 1 | decision_rows=1 | hard |
| P194_EXTENSION_NEGATIVE_RECORDED | 1 | negative_extension_profile_date_rows=4; extension_profile_date_rows=4 | hard |
| P194_TEST_REPLAY_CLOSED | 1 | test_replay_allowed_next=0 | hard |
| P194_PROMOTION_CLOSED | 1 | promotion_allowed=0 | hard |
| P194_PAPER_LIVE_CLOSED | 1 | paper_or_live_acceptance_allowed=0 | hard |
| P194_REDESIGN_BLUEPRINT_WRITTEN | 1 | blueprint_rows=3 | hard |

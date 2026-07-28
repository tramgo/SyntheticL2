# Phase200 Material New Hypothesis Precommit

Generated UTC: 2026-07-28T20:15:43.149612+00:00

Phase200 selects the highest-priority materially new hypothesis from Phase199: passive queue-position/adverse-selection survival.
It is a label-contract and label-expansion precommit only; no strategy replay, test replay, orders, fills, P&L, promotion or paper/live acceptance is opened.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase200_selected_hypothesis_id | P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY | Selected material new hypothesis |
| phase200_selected_hypothesis_rows | 1 | Selected hypothesis rows |
| phase200_label_contract_rows | 6 | Passive queue label contract rows |
| phase200_stage_action_rows | 4 | Next stage action rows |
| phase200_prior_evidence_rows | 5 | Prior evidence rows |
| phase200_gate_rows | 7 | Gates evaluated |
| phase200_hard_gate_rows | 7 | Hard gates evaluated |
| phase200_hard_gate_pass_rows | 7 | Hard gates passed |
| phase200_material_new_hypothesis_precommit_complete | 1 | 1 means Phase200 completed |
| phase200_strategy_replay_allowed | 0 | No strategy replay opened |
| phase200_test_replay_allowed_next | 0 | No test replay opened |
| phase200_promotion_allowed | 0 | No promotion opened |
| phase200_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase200_forbidden_outputs | strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim | Outputs forbidden in this phase |
| phase200_next_best_action | run_phase201_passive_queue_label_only_stage01_expansion_no_replay | Recommended next milestone |

## Selected Hypothesis

| hypothesis_id | hypothesis_family | material_difference | recommended_next_action | priority | test_replay_allowed_next | phase200_selected_for_precommit | phase200_precommit_scope | strategy_replay_allowed | promotion_allowed | paper_or_live_acceptance_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY | passive_execution_microstructure | Switch from marketable receive-flow/context signals to passive queue-position and adverse-selection survival labels. | precommit_passive_queue_position_label_contract_no_test | 1 | 0 | 1 | label_contract_only_no_strategy_replay | 0 | 0 | 0 |

## Passive Queue Label Contract

| contract_id | hypothesis_id | label_name | definition | source_evidence | required_before_search | feature_contract_rows_available | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P200_PASSIVE_SURVIVAL_LABEL | P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY | passive_queue_survival_without_adverse_markout | A hypothetical maker order is acceptable only if inferred touch/fill survival is followed by adverse-selection below the Phase200 ceiling and no spread-widening penalty breach. | phase66_adverse_selection;phase68_replenishment;phase69_spread_transition;phase118_feature_contract | 1 | 3 | 0 | 0 |
| P200_QUEUE_RECOVERY_FEATURES | P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY | queue_recovery_feature_set | Use pre-touch imbalance, replenishment bucket, spread transition bucket, event intensity, time-of-day and symbol-liquidity tier; forbid future returns or post-entry unavailable features. | outputs/phase118/richer_passive_feature_contract.csv | 1 | 3 | 0 | 0 |
| P200_LABEL_ONLY_EXPANSION_FIRST | P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY | stage01_label_coverage_expansion | Run Phase120 Stage 01 label-only expansion before any candidate replay, then rebuild richer passive joined labels. | outputs/phase120/passive_label_expansion_stage_plan.csv | 1 | 3 | 0 | 0 |
| P200_BREADTH_REQUIREMENT | P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY | minimum_breadth_gate | Require multi-month and multi-symbol label stability before any bounded pilot replay; one-month pockets are not enough. | phase119_max_candidate_trade_dates;phase120_current_label_months | 1 | 3 | 0 | 0 |
| P200_COST_TOXICITY_BOUND | P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY | cost_toxicity_bound | Reject candidate buckets whose passive adverse-selection rate or cost-clearing rate remains toxic after label expansion. | phase66_best_cost_clearing_rate;phase123_cost_toxicity_label | 1 | 3 | 0 | 0 |
| P200_NO_TEST_OR_REPLAY | P200_QUEUE_PASSIVE_QUEUE_POSITION_PROXY | no_test_no_replay_guard | Phase200 cannot run strategy replay, test replay, order arrival, fill model, P&L replay, promotion or paper/live acceptance. | phase199_material_redesign_contract | 1 | 3 | 0 | 0 |

## Label-only Stage Action Plan

| action_id | stage_id | priority | action | command | required_next | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| P200_RUN_PASSIVE_ADVERSE_SELECTION_LABELS | P120_LABEL_STAGE_01_MIN_BREADTH | 1 | run_passive_adverse_selection_labels | python scripts/run_phase66_passive_adverse_selection_labels.py --limit-shards 128 --output-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase66 | 1 | 0 |
| P200_RUN_REPLENISHMENT_AFTER_TOUCH_LABELS | P120_LABEL_STAGE_01_MIN_BREADTH | 2 | run_replenishment_after_touch_labels | python scripts/run_phase68_replenishment_after_touch_labels.py --limit-shards 128 --output-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase68 | 1 | 0 |
| P200_RUN_SPREAD_TRANSITION_LABELS | P120_LABEL_STAGE_01_MIN_BREADTH | 3 | run_spread_transition_labels | python scripts/run_phase69_spread_transition_labels.py --limit-shards 128 --output-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase69 | 1 | 0 |
| P200_RERUN_RICHER_PASSIVE_JOINED_LABELS | P120_LABEL_STAGE_01_MIN_BREADTH | 4 | rerun_richer_passive_joined_labels | python scripts/run_phase119_richer_passive_label_builder.py --phase66-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase66 --phase68-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase68 --phase69-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase69 --output-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase119 | 1 | 0 |

## Prior Passive Evidence

| evidence_id | observed | interpretation |
| --- | --- | --- |
| P200_PHASE120_LABEL_EXPANSION_ALLOWED | 1 | Label-only expansion is allowed without replay. |
| P200_PHASE120_REPLAY_CLOSED | 0 | Passive replay remains closed. |
| P200_FEATURE_CONTRACT_AVAILABLE | 3 | Phase118 passive feature contracts available. |
| P200_STAGE_PLAN_AVAILABLE | 3 | Phase120 staged label expansion commands available. |
| P200_CURRENT_COVERAGE_ROWS | 96 | Current passive label coverage rows available for stage planning. |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P200_PHASE199_BRANCH_DECISION_COMPLETE | 1 | phase199_complete=1; material_required=1 | hard |
| P200_PRIORITY_HYPOTHESIS_SELECTED | 1 | selected_rows=1 | hard |
| P200_MATERIAL_DIFFERENCE_RECORDED | 1 | passive queue-position differs from receive-flow/context marketable search | hard |
| P200_LABEL_CONTRACT_RECORDED | 1 | contract_rows=6 | hard |
| P200_LABEL_ONLY_EXPANSION_ACTIONS_RECORDED | 1 | action_rows=4 | hard |
| P200_PHASE120_LABEL_EXPANSION_ALLOWED_REPLAY_CLOSED | 1 | label_expansion_allowed=1; replay_allowed=0 | hard |
| P200_NO_TEST_REPLAY_OR_PROMOTION | 1 | test_replay=0; strategy_replay=0; promotion=0; paper_live=0 | hard |

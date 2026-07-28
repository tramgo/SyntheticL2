# Phase201 Passive Queue Label-only Stage 01 Acceptance

Generated UTC: 2026-07-28T20:20:26.190215+00:00

Phase201 records the Phase120 Stage 01 label-only passive expansion for the Phase200 passive queue hypothesis.
It does not open strategy replay, test replay, orders, fills, P&L, promotion or paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase201_stage01_shards_scanned | 128 | Stage 01 dense shards scanned |
| phase201_inferred_touches | 274244 | Passive inferred touches |
| phase201_joined_label_candidate_rows | 696 | Joined richer passive candidates |
| phase201_pre_replay_candidate_rows | 0 | Candidates passing pre-replay gates |
| phase201_max_candidate_symbols | 4 | Max candidate symbol breadth |
| phase201_max_candidate_trade_dates | 4 | Max candidate date breadth |
| phase201_dominant_failure_reason | adverse_selection_gate_failed\|breadth_gate_failed | Dominant failure reason |
| phase201_decision | stage01_breadth_improved_but_gates_failed_redesign_passive_features_before_stage02 | Stage 01 decision |
| phase201_gate_rows | 6 | Gates evaluated |
| phase201_hard_gate_rows | 6 | Hard gates evaluated |
| phase201_hard_gate_pass_rows | 6 | Hard gates passed |
| phase201_label_only_stage01_complete | 1 | 1 means Phase201 completed |
| phase201_strategy_replay_allowed | 0 | No strategy replay opened |
| phase201_test_replay_allowed_next | 0 | No test replay opened |
| phase201_promotion_allowed | 0 | No promotion opened |
| phase201_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase201_forbidden_outputs | strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim | Outputs forbidden in this phase |
| phase201_next_best_action | run_phase202_passive_feature_redesign_precommit_no_replay | Recommended next milestone |

## Stage 01 Label Outcome

| summary_id | phase66_shards_scanned | phase66_inferred_touches | phase66_label_candidate_rows | phase66_best_mean_after_cost_bps_if_touched | phase119_joined_label_candidate_rows | phase119_pre_replay_candidate_rows | phase119_max_candidate_symbols | phase119_max_candidate_trade_dates | phase119_bounded_pilot_replay_allowed | family_dominant_failure_reason | stage01_label_expansion_complete | stage01_replay_candidate_survived | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P201_STAGE01_PASSIVE_LABEL_OUTCOME | 128 | 274244 | 0 | -22.4421 | 696 | 0 | 4 | 4 | 0 | adverse_selection_gate_failed\|breadth_gate_failed | 1 | False | 0 | 0 | 0 | 0 |

## Decision

| decision_id | phase201_decision | next_best_action | pre_replay_candidate_rows | max_candidate_trade_dates | max_candidate_symbols | strategy_replay_allowed | test_replay_allowed_next | promotion_allowed | paper_or_live_acceptance_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P201_STAGE01_PASSIVE_QUEUE_DECISION | stage01_breadth_improved_but_gates_failed_redesign_passive_features_before_stage02 | run_phase202_passive_feature_redesign_precommit_no_replay | 0 | 4 | 4 | 0 | 0 | 0 | 0 |

## Artifact Inventory

| stage_id | phase | artifact_path | artifact_exists | strategy_replay_allowed |
| --- | --- | --- | --- | --- |
| P120_LABEL_STAGE_01_MIN_BREADTH | phase66 | outputs\phase120\P120_LABEL_STAGE_01_MIN_BREADTH\phase66\passive_label_acceptance_summary.csv | 1 | 0 |
| P120_LABEL_STAGE_01_MIN_BREADTH | phase68 | outputs\phase120\P120_LABEL_STAGE_01_MIN_BREADTH\phase68\phase68_replenishment_after_touch_labels_manifest.json | 1 | 0 |
| P120_LABEL_STAGE_01_MIN_BREADTH | phase69 | outputs\phase120\P120_LABEL_STAGE_01_MIN_BREADTH\phase69\phase69_spread_transition_labels_manifest.json | 1 | 0 |
| P120_LABEL_STAGE_01_MIN_BREADTH | phase119 | outputs\phase120\P120_LABEL_STAGE_01_MIN_BREADTH\phase119\phase119_richer_passive_label_builder_acceptance_summary.csv | 1 | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P201_PHASE200_PRECOMMIT_COMPLETE | 1 | phase200_complete=1 | hard |
| P201_STAGE01_ARTIFACTS_PRESENT | 1 | artifact_rows=4; present=4 | hard |
| P201_LABEL_ONLY_EXPANSION_RECORDED | 1 | phase66_shards=128 | hard |
| P201_PHASE119_OUTCOME_RECORDED | 1 | joined_rows=696; pre_replay=0 | hard |
| P201_REPLAY_REMAINS_CLOSED | 1 | strategy_replay=0; test_replay=0 | hard |
| P201_PROMOTION_AND_PAPER_LIVE_CLOSED | 1 | promotion=0; paper_live=0 | hard |

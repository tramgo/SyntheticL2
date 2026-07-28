# Phase203 Redesigned Passive Label Materialization

Generated UTC: 2026-07-28T20:32:13.690818+00:00

Phase203 materializes the Phase202 redesigned passive labels over existing Phase119 joined passive candidates.
It remains label-only: no replay, test, orders, fills, P&L, promotion or paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase203_materialized_label_rows | 696 | Rows in redesigned passive label materialization |
| phase203_feature_summary_rows | 5 | Rows in redesigned feature summary |
| phase203_symbol_breadth_audit_rows | 2 | Rows in symbol/month stability audit |
| phase203_adverse_selection_audit_rows | 1 | Rows in adverse-selection audit |
| phase203_redesigned_candidate_pass_rows | 0 | Rows passing all redesigned passive labels |
| phase203_max_candidate_symbols | 4 | Maximum candidate symbol breadth observed |
| phase203_max_candidate_trade_dates | 4 | Maximum candidate trade-date breadth observed |
| phase203_adverse_selection_ceiling_met | 0 | 1 means any candidate met the toxicity ceiling |
| phase203_symbol_month_stability_requirement_rows | 0 | Feature-family rows meeting symbol/month stability requirement |
| phase203_candidate_gate_open | 0 | 1 means Phase204 candidate precommit may be considered |
| phase203_gate_rows | 7 | Gates evaluated |
| phase203_hard_gate_rows | 7 | Hard gates evaluated |
| phase203_hard_gate_pass_rows | 7 | Hard gates passed |
| phase203_label_materialization_complete | 1 | 1 means Phase203 completed |
| phase203_strategy_replay_allowed | 0 | No strategy replay opened |
| phase203_test_replay_allowed_next | 0 | No test replay opened |
| phase203_promotion_allowed | 0 | No promotion opened |
| phase203_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase203_forbidden_outputs | strategy_replay;test_replay_execution;test_result;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim | Outputs forbidden in this phase |
| phase203_next_best_action | redesign_passive_labels_or_expand_label_materialization_before_replay | Recommended next milestone |

## Redesigned Feature Summary

| label_id | candidate_rows | pass_rows | pass_fraction | max_symbols_among_pass | max_trade_dates_among_pass | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- |
| p203_queue_recovery_persistence_label | 696 | 180 | 0.258621 | 4 | 4 | 0 | 0 |
| p203_toxicity_abstention_filter_label | 696 | 0 | 0 | 0 | 0 | 0 | 0 |
| p203_symbol_month_stability_label | 696 | 0 | 0 | 0 | 0 | 0 | 0 |
| p203_spread_compression_cancel_guard_label | 696 | 0 | 0 | 0 | 0 | 0 | 0 |
| p203_redesigned_candidate_pass | 696 | 0 | 0 | 0 | 0 | 0 | 0 |

## Adverse Selection Audit

| audit_id | candidate_rows | phase201_adverse_failure_rows | toxicity_abstention_pass_rows | min_baseline_adverse_selection_rate | min_replenishment_adverse_selection_rate | min_spread_adverse_direction_rate | adverse_selection_ceiling | adverse_selection_ceiling_met | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P203_ADVERSE_SELECTION_VS_STAGE01 | 696 | 696 | 0 | 0.980392 | 0.976202 | 1 | 0.75 | 0 | 0 | 0 |

## Symbol/Month Stability Audit

| feature_family_id | base_strategy_id | candidate_rows | max_symbols | max_trade_dates | mean_label_quality_score | redesigned_pass_rows | symbol_month_stability_requirement_met | strategy_replay_allowed | test_replay_allowed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P118_RICHER_PASSIVE_LABEL_COMPOSITE | P68_FADE_IMBALANCE_REPLENISH | 348 | 4 | 4 | 1.00476 | 0 | 0 | 0 | 0 |
| P118_RICHER_PASSIVE_LABEL_COMPOSITE | P68_JOIN_IMBALANCE_REPLENISH | 348 | 4 | 4 | 1.00708 | 0 | 0 | 0 | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P203_PHASE202_COMPLETE | True | phase202_complete=1 | hard |
| P203_ACTION_PLAN_PRESENT | True | action_rows=3 | hard |
| P203_JOINED_LABEL_CANDIDATES_PRESENT | True | materialized_rows=696 | hard |
| P203_REDESIGNED_FEATURE_LABELS_MATERIALIZED | True | feature_summary_rows=5 | hard |
| P203_ADVERSE_SELECTION_AUDIT_RECORDED | True | adverse_audit_rows=1 | hard |
| P203_SYMBOL_MONTH_STABILITY_AUDIT_RECORDED | True | breadth_audit_rows=2 | hard |
| P203_NO_REPLAY_OR_PROMOTION | True | strategy_replay=0; test_replay=0; promotion=0; paper_live=0 | hard |

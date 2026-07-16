# Phase 39 Synthetic-Only Acceptance Path

Generated UTC: 2026-07-16T13:57:46.872772+00:00

This phase records the explicit synthetic-only path selected because Zerodha fills and contract notes are unavailable.
It allows controlled synthetic experiments and redesign diagnostics to continue, but it does not promote current strategies and does not open paper/live broker readiness.

## Summary

| metric | value | description |
| --- | --- | --- |
| phase39_policy_rows | 4 | Synthetic-only acceptance policy rows |
| phase39_gate_rows | 7 | Synthetic-only gate ledger rows |
| phase39_broker_blockers_deferred_for_synthetic_only | 3 | Broker evidence gates deferred only for synthetic-only experiments |
| phase39_strategies_evaluated | 11 | Strategy/control families evaluated |
| phase39_alpha_strategies_evaluated | 9 | Alpha strategy families evaluated |
| phase39_synthetic_experiment_allowed_strategies | 11 | Families allowed to continue in synthetic-only experiments |
| phase39_synthetic_strategy_acceptance_ready | 0 | Families accepted for synthetic-only strategy promotion |
| phase39_paper_or_live_acceptance_ready | 0 | Families ready for paper/live broker acceptance |
| phase39_synthetic_replay_available_strategies | 9 | Families with current synthetic replay artifacts |
| phase39_total_existing_synthetic_replay_trades | 797626 | Existing strategy/control synthetic/proxy replay trade rows available |
| phase39_realistic_positive_strategy_rows | 0 | Families with at least one realistic positive profile |

## Policy

| policy_id | allowed | acceptance_scope | evidence_status | observed_value | boundary |
| --- | --- | --- | --- | --- | --- |
| synthetic_experiment_continuation | True | synthetic_only_experiment | allowed_without_zerodha_fills_or_contract_notes | 856471 synthetic/proxy replay trade rows available | May run experiments/redesign diagnostics; does not promote strategies or imply broker readiness. |
| synthetic_strategy_acceptance | False | synthetic_only_strategy_promotion | blocked_by_current_strategy_economics | phase25_positive_profiles=0; phase29_realistic_positive_profiles=0 | No current alpha strategy may be accepted until synthetic replay clears positive after-cost economics. |
| paper_or_live_broker_acceptance | False | real_broker_or_paper_live | blocked_by_missing_zerodha_fills_and_contract_notes | Zerodha fills/contract notes are unavailable for this experiment path | Broker/paper/live readiness remains closed; broker reconciliation is not waived outside synthetic-only scope. |
| class_b_real_data_replay_acceptance | False | real_l2_multiday_acceptance | blocked_by_phase38_class_b_gate | phase38_class_b_promoted_days=0 | Real-data acceptance replay still requires promoted Class B days and remains separate from synthetic-only experiments. |

## Gate Ledger

| gate_id | gate_group | passed_for_synthetic_experiments | passed_for_strategy_acceptance | observed_value | required_next_action |
| --- | --- | --- | --- | --- | --- |
| synthetic_only_scope_declared | scope | True | False | synthetic-only acceptance path selected because Zerodha fills/contract notes are unavailable |  |
| synthetic_event_replay_available | synthetic_evidence | True | False | phase25_trades=113848; phase29_trades=742623 |  |
| positive_after_cost_economics | economics | True | False | phase25_positive_profiles=0; phase29_realistic_positive_profiles=0 | Redesign strategy signals/labels until synthetic replay clears after-cost economics. |
| zerodha_real_fill_required_for_synthetic_only | broker_evidence_deferred | True | False | deferred only inside synthetic-only experiment scope | Provide Zerodha fill/contract-note/reconciliation evidence before broker, paper, or live readiness. |
| contract_note_required_for_synthetic_only | broker_evidence_deferred | True | False | deferred only inside synthetic-only experiment scope | Provide Zerodha fill/contract-note/reconciliation evidence before broker, paper, or live readiness. |
| broker_reconciliation_required_for_synthetic_only | broker_evidence_deferred | True | False | deferred only inside synthetic-only experiment scope | Provide Zerodha fill/contract-note/reconciliation evidence before broker, paper, or live readiness. |
| real_broker_or_paper_acceptance_closed | broker_boundary | True | False | synthetic-only path does not claim real fill quality or contract-note cost reconciliation | Keep broker acceptance closed until real execution artifacts exist. |

## Strategy Decisions

| strategy_id | strategy_name | evidence_scope | current_decision | synthetic_experiment_allowed | synthetic_strategy_acceptance_ready | paper_or_live_acceptance_ready | synthetic_replay_available | synthetic_replay_source | synthetic_trade_rows | execution_profiles | positive_after_cost_profiles | realistic_positive_profiles | best_mean_net_return | experiment_status | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Momentum/breakout filtered by MLOFI | runnable_proxy_event_replay_salvage_feature_edge | reject_current_signal_form_redesign_required | True | False | False | True | phase25_event_order_replay | 4377 | 3 | 0 | 0 | -0.000484858 | synthetic_experiment_allowed_redesign_required | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| S02 | Pure multi-level OFI directional model | runnable_proxy_event_replay_salvage_feature_edge | reject_current_signal_form_redesign_required | True | False | False | True | phase25_event_order_replay | 27321 | 3 | 0 | 0 | -0.000335916 | synthetic_experiment_allowed_redesign_required | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| S03 | Liquidity-vacuum breakout | partial_proxy_label_replay | reject_current_proxy_label_execution_form | True | False | False | True | phase29_partial_proxy_replay | 22469 | 3 | 0 | 0 | -7.90804e-05 | synthetic_experiment_allowed_redesign_required | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| S04 | Trade-flow plus depth confirmation | partial_proxy_label_replay | reject_current_proxy_label_execution_form | True | False | False | True | phase29_partial_proxy_replay | 112654 | 3 | 0 | 0 | -8.44832e-05 | synthetic_experiment_allowed_redesign_required | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| S05 | Microprice entry/exit filter | runnable_proxy_event_replay_salvage_feature_edge | reject_current_signal_form_redesign_required | True | False | False | True | phase25_event_order_replay | 8475 | 3 | 0 | 0 | -0.000974655 | synthetic_experiment_allowed_redesign_required | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| S06 | Absorption and exhaustion reversal | partial_proxy_label_replay | reject_current_proxy_label_execution_form | True | False | False | True | phase29_partial_proxy_replay | 208728 | 3 | 0 | 0 | -0.000109038 | synthetic_experiment_allowed_redesign_required | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| S07 | Mean reversion after imbalance | runnable_proxy_event_replay_salvage_feature_edge | reject_current_signal_form_redesign_required | True | False | False | True | phase25_event_order_replay | 6355 | 3 | 0 | 0 | -0.000873183 | synthetic_experiment_allowed_redesign_required | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| S08 | Cross-ticker/index lead-lag OFI | partial_proxy_label_replay | reject_current_proxy_label_execution_form | True | False | False | True | phase29_partial_proxy_replay | 398772 | 3 | 0 | 0 | -0.0001214 | synthetic_experiment_allowed_redesign_required | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| S09 | Pure queue-imbalance scalping | runnable_proxy_event_replay_salvage_feature_edge | reject_current_signal_form_redesign_required | True | False | False | True | phase25_event_order_replay | 8475 | 3 | 0 | 0 | -0.000981921 | synthetic_experiment_allowed_redesign_required | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| S10 | Passive market making | non_alpha_control_or_risk_filter | non_alpha_control_do_not_promote | True | False | False | False | none | 0 | 0 | 0 | 0 | 0 | control_or_risk_plumbing_allowed | Use only as execution/risk control plumbing; exclude from alpha promotion. |
| S11 | Spoof-like wall filter | non_alpha_control_or_risk_filter | non_alpha_control_do_not_promote | True | False | False | False | none | 0 | 0 | 0 | 0 | 0 | control_or_risk_plumbing_allowed | Use only as execution/risk control plumbing; exclude from alpha promotion. |

## Experiment Queue

| priority | strategy_id | strategy_name | experiment_track | allowed_scope | must_not_claim | synthetic_trade_rows | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S01 | Momentum/breakout filtered by MLOFI | alpha_redesign_diagnostics | synthetic_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation | 4377 | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| 2 | S02 | Pure multi-level OFI directional model | alpha_redesign_diagnostics | synthetic_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation | 27321 | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| 3 | S03 | Liquidity-vacuum breakout | alpha_redesign_diagnostics | synthetic_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation | 22469 | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| 4 | S04 | Trade-flow plus depth confirmation | alpha_redesign_diagnostics | synthetic_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation | 112654 | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| 5 | S05 | Microprice entry/exit filter | alpha_redesign_diagnostics | synthetic_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation | 8475 | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| 6 | S06 | Absorption and exhaustion reversal | alpha_redesign_diagnostics | synthetic_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation | 208728 | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| 7 | S07 | Mean reversion after imbalance | alpha_redesign_diagnostics | synthetic_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation | 6355 | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| 8 | S08 | Cross-ticker/index lead-lag OFI | alpha_redesign_diagnostics | synthetic_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation | 398772 | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| 9 | S09 | Pure queue-imbalance scalping | alpha_redesign_diagnostics | synthetic_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation | 8475 | Continue synthetic-only redesign/diagnostics; do not promote until realistic after-cost replay turns positive. |
| 10 | S10 | Passive market making | control_risk_plumbing | synthetic_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation | 0 | Use only as execution/risk control plumbing; exclude from alpha promotion. |
| 11 | S11 | Spoof-like wall filter | control_risk_plumbing | synthetic_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation | 0 | Use only as execution/risk control plumbing; exclude from alpha promotion. |

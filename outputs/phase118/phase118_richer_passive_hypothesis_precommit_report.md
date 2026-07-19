# Phase118 Richer Passive Hypothesis Precommit

Generated UTC: 2026-07-19T23:07:02.542045+00:00

Phase118 precommits a materially different passive/liquidity-resilience branch after simple passive labels and simple passive queue replay failed.
It is deliberately label-only: no bounded or full-year replay is allowed until adverse-selection, replenishment and spread-transition feasibility gates pass.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase118_prior_label_evidence_rows | 5 | Prior passive/liquidity label and replay evidence rows reviewed |
| phase118_prior_surviving_gate_rows | 0 | Prior passive/liquidity rows that survived their gate |
| phase118_prior_candidate_rows | 0 | Candidate rows found by prior passive/liquidity gates |
| phase118_feature_family_rows | 3 | New richer passive feature families precommitted |
| phase118_candidate_template_rows | 3 | Candidate templates emitted for future label construction |
| phase118_pre_replay_gate_rows | 6 | Pre-replay and replay gates locked |
| phase118_bounded_pilot_replay_allowed | 0 | 1 means a bounded replay may run immediately |
| phase118_full_year_replay_allowed | 0 | Full-year replay remains closed |
| phase118_next_best_action | implement_label_builder_for_p118_richer_passive_features_before_any_replay | Recommended next milestone |
| phase118_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model version carried into any future replay |

## Prior Passive Label Failure Ledger

| evidence_id | scope | rows_or_candidates | candidate_rows | best_after_cost_bps | survives_gate | decision | best_expected_net_pnl_inr |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P66_PASSIVE_ADVERSE_SELECTION_LABELS | simple join/fade passive imbalance labels | 5681976 | 0 | -17.0135 | 0 | simple_passive_imbalance_labels_failed |  |
| P67_FEATURE_DESIGN_BUDGET | post-Phase66 feature-design budget gate | 4 | 0 | -17.0135 | 0 | full_year_replay_blocked_by_budget_gate |  |
| P68_REPLENISHMENT_AFTER_TOUCH | post-touch replenishment labels | 68850 | 0 | -13.236 | 0 | replenishment_label_gate_failed |  |
| P69_SPREAD_TRANSITION_LABELS | spread compression/expansion transition labels | 319500 | 0 | -10.0305 | 0 | spread_transition_label_gate_failed |  |
| P89_SIMPLE_PASSIVE_QUEUE_COST_FLOOR | simple passive queue expected-value replay under pessimistic/base/optimistic fills | 54 | 0 |  | 0 | simple_passive_queue_replay_failed | -187946 |

## Richer Passive Feature Contract

| feature_family_id | hypothesis | uses_prior_failed_evidence | allowed_features | forbidden_features | direction_policy | turnover_policy |
| --- | --- | --- | --- | --- | --- | --- |
| P118_QUEUE_RECOVERY_AFTER_ADVERSE_TOUCH | A passive fill is only acceptable after an adverse touch if L1/L5 replenishment and spread non-expansion jointly indicate queue recovery. | P66 adverse-selection labels; P68 replenishment labels; P69 spread-transition labels | pre-touch imbalance bucket, replenishment bucket, spread transition bucket, event intensity bucket, time-of-day bucket, symbol liquidity tier | future return, realized next-bar P&L, post-entry labels unavailable at order decision time | maker only; quote on the side implied by precommitted queue-recovery condition | low turnover only; no dense event-by-event marketable conversion |
| P118_SPREAD_COMPRESSION_MAKER_ONLY | When spread expansion is followed by reliable compression without adverse markout, a maker order may earn spread without paying the taker spread penalty. | P69 spread-transition labels; P89 passive queue cost floor | spread transition state, recent spread percentile, depth imbalance persistence, shock flag, symbol liquidity tier | candidate ranking by test P&L or optimistic-only fill results | maker only; no crossing; stale quote cancellation mandatory | one candidate per symbol per event-window; daily order budget capped before replay |
| P118_REPLENISHMENT_STABILITY_FILTER | Passive fills are least toxic where post-touch replenishment is stable across train months and adverse-selection labels are below a strict ceiling. | P68 replenishment buckets; P66 passive adverse-selection buckets | replenishment bucket stability, adverse-selection bucket, depth rebuild rate, symbol liquidity tier | single-symbol pocket selection, threshold widening after replay, HDFCBANK-only revival | maker only; side chosen by pre-touch label family | must survive minimum symbol/month breadth before any replay expansion |

## Pre-Replay Feasibility Gates

| gate_id | stage | requirement | pass_threshold | failure_action |
| --- | --- | --- | --- | --- |
| P118_NO_PNL_SELECTION | pre_replay | Candidate filters must be selected from label quality and train-only feature distributions, not directional P&L. | no test P&L field used in candidate construction | discard candidate spec and rewrite precommit |
| P118_ADVERSE_SELECTION_CEILING | pre_replay | Candidate buckets must show materially lower adverse-selection risk than simple Phase66/68 labels. | train adverse-selection rate <= 0.45 and at least 10 percentage points below simple passive baseline | do not run replay |
| P118_REPLENISHMENT_AND_SPREAD_CONFIRMATION | pre_replay | Candidate must combine replenishment and non-expanding/compressing spread context. | replenishment stability pass == 1 and spread non-expansion/compression pass == 1 | keep as label research only |
| P118_BREADTH_BEFORE_REPLAY | pre_replay | Candidate label rows must span enough symbols and months to avoid a one-pocket illusion. | symbols >= 20 and train months >= 4 before replay | collect more real/synthetic label coverage before replay |
| P118_FILL_MODEL_CONSERVATISM | replay_gate | Replay, if later allowed, must pass pessimistic, base and optimistic fill models separately. | all_fill_assumptions_pass == 1; optimistic-only success rejected | retire feature family |
| P118_COMPUTE_BUDGET | replay_gate | No large dense replay is allowed until pre-replay label gates pass. | bounded pilot first; full-year replay only after pilot pass and Phase117/115 real-anchor path reviewed | block same-family shard continuation |

## Candidate Spec Template

| candidate_template_id | feature_family_id | threshold_policy | adverse_selection_rate_max | symbols_min | train_months_min | replenishment_required | spread_non_expansion_required | max_daily_orders_per_symbol | pilot_replay_allowed_now | why_not_allowed_now |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P118_QUEUE_RECOVERY_AFTER_ADVERSE_TOUCH_STRICT | P118_QUEUE_RECOVERY_AFTER_ADVERSE_TOUCH | train_only_strict | 0.45 | 20 | 4 | True | True | 20 | False | Phase66/68/69/89 current labels have zero candidate rows and Phase116/117 keep replay gates closed. |
| P118_SPREAD_COMPRESSION_MAKER_ONLY_STRICT | P118_SPREAD_COMPRESSION_MAKER_ONLY | train_only_strict | 0.45 | 20 | 4 | True | True | 20 | False | Phase66/68/69/89 current labels have zero candidate rows and Phase116/117 keep replay gates closed. |
| P118_REPLENISHMENT_STABILITY_FILTER_STRICT | P118_REPLENISHMENT_STABILITY_FILTER | train_only_strict | 0.45 | 20 | 4 | True | True | 20 | False | Phase66/68/69/89 current labels have zero candidate rows and Phase116/117 keep replay gates closed. |

## Replay Permission Gate

| permission_id | permission | evidence |
| --- | --- | --- |
| P118_LABEL_ONLY_DESIGN | allowed | Richer passive feature contract and gates may be designed without replay. |
| P118_BOUNDED_PILOT_REPLAY | closed | current_label_candidate_rows=0; requires label gates to pass first |
| P118_FULL_YEAR_REPLAY | closed | phase116_accepted_strategy_rows=0; same_family_allowed=0; phase117_strategy_replay_allowed=0 |
| P118_SAME_FAMILY_DENSE_SHARDS | blocked | Phase116 blocks continuation of current failed dense/cross-symbol/event-window families. |

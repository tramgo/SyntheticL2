# Phase178 Receive-flow Feature Handoff Precommit

Generated UTC: 2026-07-28T16:14:15.534784+00:00

Phase178 defines how audited receive-flow features may be handed to a later strategy precommit phase.
It does not emit signals, orders, fills, P&L, profitability claims, or paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase178_handoff_feature_rows | 6 | Feature families handed off for future precommit only |
| phase178_train_test_policy_rows | 1 | Chronological train/validation/test split policies |
| phase178_blocklist_policy_rows | 3 | Blocked-family policies carried forward |
| phase178_gate_rows | 7 | Gates evaluated |
| phase178_hard_gate_rows | 7 | Hard gates evaluated |
| phase178_hard_gate_pass_rows | 7 | Hard gates passed |
| phase178_handoff_ready | 1 | 1 means Phase179 precommit may be built |
| phase178_strategy_replay_allowed | 0 | No strategy replay opened |
| phase178_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase178_forbidden_outputs | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | Outputs forbidden in this phase |
| phase178_next_best_action | build_phase179_strategy_family_precommit_no_replay | Recommended next milestone |

## Allowed Feature Handoff

| feature_id | feature_family | handoff_status | allowed_horizons_materialized_seconds | available_trade_dates | available_symbol_count | allowed_downstream_use | required_before_replay | forbidden_direct_use | leakage_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P175_RECEIVE_EVENT_RATE_ZSCORE | receive_cadence | allowed_for_phase179_precommit_only | 1;5;15;60 | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14 | 32 | feature_candidate_for_future_strategy_precommit_only | phase179_strategy_family_precommit;train_test_split;leakage_audit;blocklist_overlap_audit;cost_latency_catalog_binding | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | baseline statistics fitted on train dates only before test-date transform |
| P175_QUOTE_CHURN_RATE | book_state_churn | allowed_for_phase179_precommit_only | 1;5;15;60 | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14 | 32 | feature_candidate_for_future_strategy_precommit_only | phase179_strategy_family_precommit;train_test_split;leakage_audit;blocklist_overlap_audit;cost_latency_catalog_binding | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | computed only from events received at or before the feature timestamp |
| P175_DEPTH_REFRESH_INTENSITY | top_five_depth_churn | allowed_for_phase179_precommit_only | 1;5;15;60 | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14 | 32 | feature_candidate_for_future_strategy_precommit_only | phase179_strategy_family_precommit;train_test_split;leakage_audit;blocklist_overlap_audit;cost_latency_catalog_binding | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | uses top-five market-by-price state only; no inferred hidden order events |
| P175_STALE_QUOTE_DURATION | feed_staleness | allowed_for_phase179_precommit_only | 1;5;15;60 | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14 | 32 | feature_candidate_for_future_strategy_precommit_only | phase179_strategy_family_precommit;train_test_split;leakage_audit;blocklist_overlap_audit;cost_latency_catalog_binding | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | forward state duration censored at the current timestamp; no future duration completion |
| P175_CROSS_SYMBOL_ARRIVAL_SYNCHRONY | cross_symbol_receive_flow | allowed_for_phase179_precommit_only | 1;5;15;60 | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14 | 32 | feature_candidate_for_future_strategy_precommit_only | phase179_strategy_family_precommit;train_test_split;leakage_audit;blocklist_overlap_audit;cost_latency_catalog_binding | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | computed from contemporaneous receive buckets only; target symbol exclusion required in ablation |
| P175_RECEIVE_FLOW_REGIME_STATE | source_quality_context | allowed_for_phase179_precommit_only | 1;5;15;60 | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14 | 32 | feature_candidate_for_future_strategy_precommit_only | phase179_strategy_family_precommit;train_test_split;leakage_audit;blocklist_overlap_audit;cost_latency_catalog_binding | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | fit context model on train dates only; report train/test date separation |

## Train/Test Split Policy

| split_id | train_dates | validation_dates | test_dates | fit_policy | selection_policy | final_test_policy | minimum_dates_required | split_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P178_CHRONOLOGICAL_3_1_1 | 2026-07-08;2026-07-09;2026-07-10 | 2026-07-13 | 2026-07-14 | fit baselines/transforms/model choices on train_dates only | validation_dates may select predeclared thresholds only after Phase179 | test_dates are untouched until the replay phase precommit passes | 5 | 1 |

## Blocklist Carry-forward Policy

| blocked_source | handoff_rule | overlap_allowed |
| --- | --- | --- |
| PHASE164_S01_TO_S07_S09_SYNTHETIC_FORMS | feature may not recreate blocked synthetic signal formulas or thresholds | 0 |
| PHASE167_S08_FIXED_CROSS_SYMBOL_LEAD_LAG_FORM | cross-symbol arrival synchrony is context only; fixed S08 lead-lag score remains forbidden | 0 |
| PHASE131_TO_136_TOP_FIVE_DEPTH_PASSIVE_BRANCH | depth refresh/churn may describe feed/book context only; passive queue/fill claims remain closed | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P178_PHASE176_FEATURES_MATERIALIZED | 1 | phase176_features_materialized=1 | hard |
| P178_PHASE177_QUALITY_AUDIT_RAN | 1 | phase177_feature_quality_audit_ran=1 | hard |
| P178_COVERAGE_COMPLETE | 1 | coverage_pass_rows=20/20 | hard |
| P178_PARTITION_QUALITY_CLEAN | 1 | missing_required=0;duplicate_buckets=0;monotonic_violations=0;partitions=640 | hard |
| P178_HANDOFF_FEATURES_DECLARED | 1 | handoff_feature_rows=6 | hard |
| P178_CHRONOLOGICAL_SPLIT_DECLARED | 1 | {'split_id': 'P178_CHRONOLOGICAL_3_1_1', 'train_dates': '2026-07-08;2026-07-09;2026-07-10', 'validation_dates': '2026-07-13', 'test_dates': '2026-07-14', 'fit_policy': 'fit baselines/transforms/model choices on train_dates only', 'selection_policy': 'validation_dates may select predeclared thresholds only after Phase179', 'final_test_policy': 'test_dates are untouched until the replay phase precommit passes', 'minimum_dates_required': 5, 'split_pass': 1} | hard |
| P178_NO_REPLAY_OR_PROFITABILITY_OUTPUTS | 1 | handoff precommit only; forbidden_outputs=buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | hard |

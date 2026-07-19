# Phase125 Filter Integration Contract

Generated UTC: 2026-07-19T23:34:44.456118+00:00

Phase125 packages selected Phase124 filters as diagnostic/abstention integration rules.
The contract deliberately emits no buy/sell signals and does not open strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase125_filter_rules | 2 | Selected non-trading filter rules integrated |
| phase125_abstention_filter_rules | 1 | Rules allowed to block future candidate generation only |
| phase125_filter_flag_rows | 768 | Symbol/month filter flag rows emitted |
| phase125_flagged_symbol_month_rows | 277 | Total flagged symbol/month rows across all filters |
| phase125_filter_impact_rows | 2 | Filter impact summary rows |
| phase125_gate_rows | 4 | Integration gates evaluated |
| phase125_all_gates_pass | 1 | 1 means integration contract is internally consistent |
| phase125_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase125_ready_real_anchor_days | 1 | Real-anchor days still available |
| phase125_real_anchor_days_needed_for_min | 4 | Additional real days still needed for minimum strategy replay gate |
| phase125_next_best_action | use_filters_as_diagnostics_only_and_continue_real_anchor_acquisition | Recommended next milestone |
| phase125_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model retained for audit continuity |

## Filter Integration Rules

| filter_id | source_label | selected_model_id | feature | direction | threshold | holdout_brier | brier_improvement | holdout_auc | integration_action | usage_scope | may_block_candidate_generation | may_change_order_side_or_size | may_open_replay | may_support_profitability_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P125_REGIME_REALISM_RISK | regime_realism_risk_label | threshold_feed_imperfection_rate_ge_0.023808 | feed_imperfection_rate | ge | 0.023808 | 0.078125 | 0.127604 | 0.978873 | flag_symbol_month_for_realism_review | generator_diagnostics_and_evidence_weighting | False | False | False | False |
| P125_OPPORTUNITY_ABSTENTION | opportunity_abstention_label | threshold_mean_l1_depth_le_783.05498 | mean_l1_depth | le | 783.055 | 0.169271 | 0.0794271 | 0.783408 | disable_future_strategy_candidate_generation_for_symbol_month | pre_replay_abstention_filter_only | True | False | False | False |

## Filter Impact Summary

| filter_id | source_label | integration_action | rows | flagged_rows | symbols | months | flagged_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P125_OPPORTUNITY_ABSTENTION | opportunity_abstention_label | disable_future_strategy_candidate_generation_for_symbol_month | 384 | 156 | 32 | 12 | 0.40625 |
| P125_REGIME_REALISM_RISK | regime_realism_risk_label | flag_symbol_month_for_realism_review | 384 | 121 | 32 | 12 | 0.315104 |

## Guardrails

| guardrail_id | requirement | enforcement |
| --- | --- | --- |
| P125_NO_TRADE_SIGNAL | Integrated filters may only emit diagnostic or abstention flags. | No side, order model, order quantity, or entry/exit field is emitted. |
| P125_NO_REPLAY_OPEN | Filter integration cannot open strategy replay. | may_open_replay is false for every rule and strategy_replay_allowed remains 0. |
| P125_NO_PROFITABILITY_CLAIM | Filter holdout calibration does not imply trading profitability. | Reports call the filters diagnostics/abstention only. |
| P125_REAL_ANCHOR_PRECEDENCE | Real-anchor acquisition remains the higher-priority path for strategy evidence. | Phase117-ready-day blocker is carried into acceptance summary. |

## Gate Evaluation

| gate_id | gate_pass | evidence |
| --- | --- | --- |
| P125_SELECTED_RULES_PRESENT | 1 | rules=2 |
| P125_FLAGS_GENERATED | 1 | flag_rows=768 |
| P125_RULES_CANNOT_OPEN_REPLAY | 1 | all may_open_replay false |
| P125_GLOBAL_REPLAY_LOCK | 1 | phase116_same_family_shard_continuation_allowed=0 |

## Filter Flags Sample

| trade_month | symbol | feature_value | filter_id | source_label | filter_flag | integration_action | may_open_replay |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | ADANIPORTS | 0.007936 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | AXISBANK | 0 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | BAJAJ-AUTO | 0.023808 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 1 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | BANKBEES | 0.023808 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 1 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | BHARTIARTL | 0.007936 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | BPCL | 0 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | BRITANNIA | 0 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | CIPLA | 0.007936 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | DRREDDY | 0.015872 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | GOLDBEES | 0.023808 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 1 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | HCLTECH | 0.023808 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 1 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | HDFCBANK | 0.055552 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 1 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | HINDUNILVR | 0 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | ICICIBANK | 0 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | INFY | 0.015872 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | ITBEES | 0.015872 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | ITC | 0.015872 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | JUNIORBEES | 0.007936 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | KOTAKBANK | 0 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | LT | 0.015872 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | M&M | 0.055552 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 1 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | MARUTI | 0.015872 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | NESTLEIND | 0.015872 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | NIFTYBEES | 0.007936 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | ONGC | 0 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | RELIANCE | 0.015872 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | SBIN | 0.007936 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | SUNPHARMA | 0.007936 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | TCS | 0.015872 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | TECHM | 0 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | ULTRACEMCO | 0.023808 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 1 | flag_symbol_month_for_realism_review | 0 |
| 2026-01 | WIPRO | 0.023808 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 1 | flag_symbol_month_for_realism_review | 0 |
| 2026-02 | ADANIPORTS | 0.015872 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-02 | AXISBANK | 0.023808 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 1 | flag_symbol_month_for_realism_review | 0 |
| 2026-02 | BAJAJ-AUTO | 0.015872 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-02 | BANKBEES | 0.023808 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 1 | flag_symbol_month_for_realism_review | 0 |
| 2026-02 | BHARTIARTL | 0.007936 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-02 | BPCL | 0.007936 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 0 | flag_symbol_month_for_realism_review | 0 |
| 2026-02 | BRITANNIA | 0.031744 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 1 | flag_symbol_month_for_realism_review | 0 |
| 2026-02 | CIPLA | 0.031744 | P125_REGIME_REALISM_RISK | regime_realism_risk_label | 1 | flag_symbol_month_for_realism_review | 0 |

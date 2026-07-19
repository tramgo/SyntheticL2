# Phase127 Allowed-Universe Precommit Queue

Generated UTC: 2026-07-19T23:40:38.645556+00:00

Phase127 converts the Phase126 permission ledger into an allowed universe for future label/precommit design.
It separates clean allowed contexts, realism-review contexts and blocked contexts. Replay remains closed.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase127_allowed_context_rows | 228 | Symbol/month contexts allowed for precommit design only |
| phase127_clean_allowed_context_rows | 141 | Allowed contexts without realism-review warning |
| phase127_realism_review_context_rows | 87 | Allowed contexts retaining realism-review warning |
| phase127_blocked_context_rows | 156 | Contexts blocked from candidate generation |
| phase127_work_package_rows | 2 | Precommit-design work packages emitted |
| phase127_gate_rows | 5 | Gates evaluated |
| phase127_all_gates_pass | 1 | 1 means queue obeys guardrails |
| phase127_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase127_next_best_action | design_next_label_matrix_only_from_phase127_allowed_contexts_or_continue_real_anchor_acquisition | Recommended next milestone |
| phase127_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model retained for audit continuity |

## Precommit Work Packages

| work_package_id | context_bucket | symbol_month_rows | symbols | months | allowed_deliverable | forbidden_deliverable | next_command_policy | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P127_WP01_CLEAN_CONTEXT_LABEL_DESIGN | clean_allowed_contexts | 141 | 32 | 8 | new_feature_label_matrix_or_precommit_spec | buy_sell_signal_or_pnl_replay | must consume candidate_generation_permission_ledger before selecting rows | 0 |
| P127_WP02_REALISM_REVIEW_CONTEXT_LABEL_DESIGN | allowed_with_realism_review | 87 | 31 | 8 | new_feature_label_matrix_or_precommit_spec | buy_sell_signal_or_pnl_replay | must consume candidate_generation_permission_ledger before selecting rows | 0 |

## Allowed Queue Sample

| queue_rank | trade_month | symbol | priority_bucket | realism_review_flag | opportunity_abstention_flag | candidate_generation_allowed | precommit_scope | strategy_replay_allowed | must_include_guardrail | why |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-01 | ADANIPORTS | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 2 | 2026-01 | AXISBANK | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 3 | 2026-01 | BHARTIARTL | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 4 | 2026-01 | BPCL | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 5 | 2026-01 | BRITANNIA | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 6 | 2026-01 | CIPLA | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 7 | 2026-01 | DRREDDY | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 8 | 2026-01 | HINDUNILVR | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 9 | 2026-01 | ICICIBANK | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 10 | 2026-01 | INFY | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 11 | 2026-01 | ITC | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 12 | 2026-01 | KOTAKBANK | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 13 | 2026-01 | LT | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 14 | 2026-01 | MARUTI | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 15 | 2026-01 | NESTLEIND | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 16 | 2026-01 | NIFTYBEES | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 17 | 2026-01 | ONGC | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 18 | 2026-01 | RELIANCE | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 19 | 2026-01 | SBIN | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 20 | 2026-01 | SUNPHARMA | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 21 | 2026-01 | TCS | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 22 | 2026-01 | TECHM | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 23 | 2026-02 | ADANIPORTS | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 24 | 2026-02 | BAJAJ-AUTO | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 25 | 2026-02 | BHARTIARTL | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 26 | 2026-02 | BPCL | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 27 | 2026-02 | DRREDDY | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 28 | 2026-02 | GOLDBEES | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 29 | 2026-02 | HCLTECH | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 30 | 2026-02 | HINDUNILVR | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 31 | 2026-02 | ITBEES | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 32 | 2026-02 | ITC | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 33 | 2026-02 | JUNIORBEES | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 34 | 2026-02 | KOTAKBANK | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 35 | 2026-02 | LT | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 36 | 2026-02 | M&M | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 37 | 2026-02 | NESTLEIND | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 38 | 2026-02 | NIFTYBEES | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 39 | 2026-02 | RELIANCE | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 40 | 2026-02 | SBIN | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 41 | 2026-02 | SUNPHARMA | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 42 | 2026-02 | TECHM | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 43 | 2026-02 | ULTRACEMCO | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 44 | 2026-02 | WIPRO | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 45 | 2026-03 | ADANIPORTS | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 46 | 2026-03 | BAJAJ-AUTO | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 47 | 2026-03 | BHARTIARTL | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 48 | 2026-03 | BPCL | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 49 | 2026-03 | HCLTECH | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |
| 50 | 2026-03 | INFY | P1_clean_allowed | 0 | 0 | 1 | label_or_feature_design_only | 0 | standard_no_replay_guardrail | allowed for label/precommit design only; replay still closed |

## Blocked Context Sample

| trade_month | symbol | realism_review_flag | opportunity_abstention_flag | blocked_reason | override_allowed | strategy_replay_allowed | why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | ITBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-01 | JUNIORBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-03 | BANKBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-03 | BRITANNIA | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-03 | CIPLA | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-03 | DRREDDY | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-03 | GOLDBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-03 | HINDUNILVR | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-03 | ITBEES | 1 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-03 | ITC | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-03 | JUNIORBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-03 | NIFTYBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-03 | SUNPHARMA | 1 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-05 | BANKBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-05 | DRREDDY | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-05 | ITBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | ADANIPORTS | 1 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | AXISBANK | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | BAJAJ-AUTO | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | BANKBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | BHARTIARTL | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | BPCL | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | BRITANNIA | 1 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | CIPLA | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | DRREDDY | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | GOLDBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | HCLTECH | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | HDFCBANK | 1 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | HINDUNILVR | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | ICICIBANK | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | INFY | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | ITBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | ITC | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | JUNIORBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | KOTAKBANK | 1 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | LT | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | M&M | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | MARUTI | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | NESTLEIND | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | NIFTYBEES | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | ONGC | 1 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | RELIANCE | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | SBIN | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | SUNPHARMA | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | TCS | 1 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | TECHM | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | ULTRACEMCO | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-06 | WIPRO | 0 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-07 | BANKBEES | 1 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-07 | GOLDBEES | 1 | 1 | opportunity_abstention_filter | False | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |

## Guardrails

| guardrail_id | requirement | enforcement |
| --- | --- | --- |
| P127_USE_PERMISSION_LEDGER | Future synthetic candidate design must start from Phase126 allowed rows. | Allowed queue and blocked ledger are emitted separately. |
| P127_BLOCK_ABSTENTION_ROWS | Rows blocked by opportunity-abstention cannot be used for candidate generation. | override_allowed is false for every blocked row. |
| P127_REALISM_WARNINGS_SURVIVE | Allowed rows with realism-risk flags must remain marked. | Priority bucket separates clean rows from realism-review rows. |
| P127_NO_REPLAY | The precommit queue cannot open strategy replay. | strategy_replay_allowed remains 0 in all outputs. |

## Gate Evaluation

| gate_id | gate_pass | evidence |
| --- | --- | --- |
| P127_ALLOWED_QUEUE_EXISTS | 1 | allowed_rows=228 |
| P127_BLOCKED_LEDGER_EXISTS | 1 | blocked_rows=156 |
| P127_WORK_PACKAGES_DECLARED | 1 | work_packages=2 |
| P127_NO_REPLAY | 1 | all emitted strategy_replay_allowed fields are 0 |
| P127_REAL_ANCHOR_STILL_PRIMARY | 1 | ready_real_anchor_days=1; days_needed=4 |

# Phase126 Candidate-Generation Permission Ledger

Generated UTC: 2026-07-19T23:37:11.087297+00:00

Phase126 converts Phase125 diagnostic/abstention filters into a symbol/month permission ledger for future precommit design.
The ledger can block candidate generation in low-opportunity rows, but it cannot open strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase126_symbol_month_rows | 384 | Symbol/month permission rows |
| phase126_candidate_generation_allowed_rows | 228 | Rows allowed for future precommit/label design only |
| phase126_opportunity_blocked_rows | 156 | Rows blocked by opportunity-abstention filter |
| phase126_realism_review_rows | 121 | Rows flagged for realism review |
| phase126_gate_rows | 5 | Gates evaluated |
| phase126_all_gates_pass | 1 | 1 means permission ledger obeys guardrails |
| phase126_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase126_next_best_action | use_permission_ledger_for_future_precommit_design_and_continue_real_anchor_acquisition | Recommended next milestone |
| phase126_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model retained for audit continuity |

## Month Summary

| trade_month | symbol_month_rows | candidate_generation_allowed_rows | opportunity_blocked_rows | realism_review_rows | allowed_fraction | opportunity_blocked_fraction | realism_review_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | 32 | 30 | 2 | 8 | 0.9375 | 0.0625 | 0.25 |
| 2026-02 | 32 | 32 | 0 | 10 | 1 | 0 | 0.3125 |
| 2026-03 | 32 | 21 | 11 | 8 | 0.65625 | 0.34375 | 0.25 |
| 2026-04 | 32 | 32 | 0 | 23 | 1 | 0 | 0.71875 |
| 2026-05 | 32 | 29 | 3 | 10 | 0.90625 | 0.09375 | 0.3125 |
| 2026-06 | 32 | 0 | 32 | 6 | 0 | 1 | 0.1875 |
| 2026-07 | 32 | 28 | 4 | 15 | 0.875 | 0.125 | 0.46875 |
| 2026-08 | 32 | 32 | 0 | 9 | 1 | 0 | 0.28125 |
| 2026-09 | 32 | 0 | 32 | 8 | 0 | 1 | 0.25 |
| 2026-10 | 32 | 0 | 32 | 9 | 0 | 1 | 0.28125 |
| 2026-11 | 32 | 24 | 8 | 9 | 0.75 | 0.25 | 0.28125 |
| 2026-12 | 32 | 0 | 32 | 6 | 0 | 1 | 0.1875 |

## Symbol Summary

| symbol | months | candidate_generation_allowed_months | opportunity_blocked_months | realism_review_months | allowed_fraction | opportunity_blocked_fraction | realism_review_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ITBEES | 12 | 3 | 9 | 2 | 0.25 | 0.75 | 0.166667 |
| BANKBEES | 12 | 4 | 8 | 4 | 0.333333 | 0.666667 | 0.333333 |
| GOLDBEES | 12 | 5 | 7 | 6 | 0.416667 | 0.583333 | 0.5 |
| JUNIORBEES | 12 | 5 | 7 | 4 | 0.416667 | 0.583333 | 0.333333 |
| DRREDDY | 12 | 5 | 7 | 2 | 0.416667 | 0.583333 | 0.166667 |
| NIFTYBEES | 12 | 5 | 7 | 2 | 0.416667 | 0.583333 | 0.166667 |
| SUNPHARMA | 12 | 6 | 6 | 4 | 0.5 | 0.5 | 0.333333 |
| CIPLA | 12 | 7 | 5 | 4 | 0.583333 | 0.416667 | 0.333333 |
| HINDUNILVR | 12 | 7 | 5 | 4 | 0.583333 | 0.416667 | 0.333333 |
| NESTLEIND | 12 | 7 | 5 | 4 | 0.583333 | 0.416667 | 0.333333 |
| BRITANNIA | 12 | 7 | 5 | 3 | 0.583333 | 0.416667 | 0.25 |
| ITC | 12 | 7 | 5 | 1 | 0.583333 | 0.416667 | 0.0833333 |
| ICICIBANK | 12 | 8 | 4 | 6 | 0.666667 | 0.333333 | 0.5 |
| SBIN | 12 | 8 | 4 | 6 | 0.666667 | 0.333333 | 0.5 |
| ULTRACEMCO | 12 | 8 | 4 | 6 | 0.666667 | 0.333333 | 0.5 |
| ADANIPORTS | 12 | 8 | 4 | 5 | 0.666667 | 0.333333 | 0.416667 |
| HDFCBANK | 12 | 8 | 4 | 5 | 0.666667 | 0.333333 | 0.416667 |
| INFY | 12 | 8 | 4 | 5 | 0.666667 | 0.333333 | 0.416667 |
| M&M | 12 | 8 | 4 | 5 | 0.666667 | 0.333333 | 0.416667 |
| RELIANCE | 12 | 8 | 4 | 5 | 0.666667 | 0.333333 | 0.416667 |
| TCS | 12 | 8 | 4 | 5 | 0.666667 | 0.333333 | 0.416667 |
| KOTAKBANK | 12 | 8 | 4 | 4 | 0.666667 | 0.333333 | 0.333333 |
| LT | 12 | 8 | 4 | 4 | 0.666667 | 0.333333 | 0.333333 |
| MARUTI | 12 | 8 | 4 | 4 | 0.666667 | 0.333333 | 0.333333 |
| TECHM | 12 | 8 | 4 | 4 | 0.666667 | 0.333333 | 0.333333 |
| WIPRO | 12 | 8 | 4 | 4 | 0.666667 | 0.333333 | 0.333333 |
| AXISBANK | 12 | 8 | 4 | 3 | 0.666667 | 0.333333 | 0.25 |
| ONGC | 12 | 8 | 4 | 3 | 0.666667 | 0.333333 | 0.25 |
| BAJAJ-AUTO | 12 | 8 | 4 | 2 | 0.666667 | 0.333333 | 0.166667 |
| BHARTIARTL | 12 | 8 | 4 | 2 | 0.666667 | 0.333333 | 0.166667 |
| HCLTECH | 12 | 8 | 4 | 2 | 0.666667 | 0.333333 | 0.166667 |
| BPCL | 12 | 8 | 4 | 1 | 0.666667 | 0.333333 | 0.0833333 |

## Guardrails

| guardrail_id | requirement | enforcement |
| --- | --- | --- |
| P126_PRECOMMIT_ONLY | Allowed rows may be used only for future feature-label/precommit design. | candidate_generation_status never implies replay or profitability. |
| P126_ABSTENTION_BLOCKS_GENERATION | Opportunity-abstention rows block future candidate generation. | candidate_generation_allowed is 0 when opportunity_abstention_flag is 1. |
| P126_REALISM_REVIEW_WARNING | Realism-risk rows must be marked for generator/evidence review. | realism_review_flag is retained even when candidate generation is allowed. |
| P126_REPLAY_CLOSED | No row may open strategy replay. | strategy_replay_allowed is 0 for all symbol/month permissions. |

## Gate Evaluation

| gate_id | gate_pass | evidence |
| --- | --- | --- |
| P126_PERMISSION_LEDGER_EXISTS | 1 | rows=384 |
| P126_ABSTENTION_ENFORCED | 1 | opportunity-abstention rows have candidate_generation_allowed=0 |
| P126_ROW_REPLAY_LOCK | 1 | all row-level strategy_replay_allowed values are 0 |
| P126_GLOBAL_REPLAY_LOCK | 1 | phase116_same_family_shard_continuation_allowed=0 |
| P126_REAL_ANCHOR_STILL_BLOCKED | 1 | ready_real_anchor_days=1; days_needed=4 |

## Permission Ledger Sample

| trade_month | symbol | realism_review_flag | opportunity_abstention_flag | candidate_generation_allowed | candidate_generation_status | strategy_replay_allowed | why |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | ADANIPORTS | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | AXISBANK | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | BAJAJ-AUTO | 1 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design with realism-review warning; replay still closed |
| 2026-01 | BANKBEES | 1 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design with realism-review warning; replay still closed |
| 2026-01 | BHARTIARTL | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | BPCL | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | BRITANNIA | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | CIPLA | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | DRREDDY | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | GOLDBEES | 1 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design with realism-review warning; replay still closed |
| 2026-01 | HCLTECH | 1 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design with realism-review warning; replay still closed |
| 2026-01 | HDFCBANK | 1 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design with realism-review warning; replay still closed |
| 2026-01 | HINDUNILVR | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | ICICIBANK | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | INFY | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | ITBEES | 0 | 1 | 0 | blocked_by_opportunity_abstention_filter | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-01 | ITC | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | JUNIORBEES | 0 | 1 | 0 | blocked_by_opportunity_abstention_filter | 0 | blocked: low-opportunity symbol/month; no candidate generation or replay |
| 2026-01 | KOTAKBANK | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | LT | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | M&M | 1 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design with realism-review warning; replay still closed |
| 2026-01 | MARUTI | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | NESTLEIND | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | NIFTYBEES | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | ONGC | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | RELIANCE | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | SBIN | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | SUNPHARMA | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | TCS | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | TECHM | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-01 | ULTRACEMCO | 1 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design with realism-review warning; replay still closed |
| 2026-01 | WIPRO | 1 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design with realism-review warning; replay still closed |
| 2026-02 | ADANIPORTS | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-02 | AXISBANK | 1 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design with realism-review warning; replay still closed |
| 2026-02 | BAJAJ-AUTO | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-02 | BANKBEES | 1 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design with realism-review warning; replay still closed |
| 2026-02 | BHARTIARTL | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-02 | BPCL | 0 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design only; replay still closed |
| 2026-02 | BRITANNIA | 1 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design with realism-review warning; replay still closed |
| 2026-02 | CIPLA | 1 | 0 | 1 | allowed_for_precommit_design_only | 0 | allowed for label/precommit design with realism-review warning; replay still closed |

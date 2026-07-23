# Phase170 Filter-conditioned Feasibility Matrix

Generated UTC: 2026-07-23T16:01:19.627978+00:00

Phase170 converts Phase129/130 diagnostic filters into a no-replay context feasibility matrix.
It emits no trade side, no order intent, no fill model, no P&L replay and no profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase170_matrix_rows | 228 | Filter-conditioned context rows |
| phase170_strict_context_rows | 6 | Stable, liquid and non-toxic rows |
| phase170_strict_context_symbols | 3 | Strict-tier symbols |
| phase170_strict_context_months | 5 | Strict-tier months |
| phase170_stable_non_toxic_rows | 75 | Stable and non-toxic rows |
| phase170_liquid_non_toxic_rows | 29 | Liquid and non-toxic rows |
| phase170_gate_rows | 6 | Gates evaluated |
| phase170_all_gates_pass | 1 | 1 means matrix obeys no-replay guardrails |
| phase170_replay_ready | 0 | 1 means context matrix alone is broad enough to request replay precommit |
| phase170_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase170_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase170_next_best_action | do_not_replay_filter_only_contexts_design_new_external_or_orderflow_feature_source | Recommended next milestone |
| phase170_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model retained for audit continuity |

## Context Tier Summary

| tier_id | rows | symbols | months | median_spread_bps | median_feed_imperfection_rate | strategy_replay_allowed | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| strict_stable_liquid_non_toxic | 6 | 3 | 5 | 2.6047 | 0.011904 | 0 | context_filter_only_not_signal |
| stable_non_toxic | 75 | 17 | 7 | 1.85512 | 0.007936 | 0 | context_filter_only_not_signal |
| liquid_non_toxic | 29 | 19 | 7 | 3.60231 | 0.023808 | 0 | context_filter_only_not_signal |

## Diagnostic Model Evidence

| label | selected_model_id | prior_brier | best_brier | brier_improvement | holdout_log_loss | holdout_accuracy | holdout_auc | model_selected | selection_reason | strategy_replay_allowed | phase170_use |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p129_regime_stability_label | threshold_feed_imperfection_rate_le_0.015872 | 0.258112 | 0.0828571 | 0.175255 | 0.322165 | 0.928571 | 0.904762 | True | beats_prior_brier_by_minimum_margin | 0 | diagnostic_filter_only |
| p129_liquidity_opportunity_label | threshold_median_spread_bps_ge_4.0782951 | 0.0848528 | 0.0721429 | 0.01271 | 0.297409 | 0.946429 | 0.5 | True | beats_prior_brier_by_minimum_margin | 0 | diagnostic_filter_only |
| p129_cost_toxicity_refinement_label | threshold_passive_min_adverse_rate_ge_0.99099099 | 0.229815 | 0.104286 | 0.12553 | 0.371675 | 0.892857 | 0.85 | True | beats_prior_brier_by_minimum_margin | 0 | diagnostic_filter_only |

## Blocked Family Overlap Audit

| candidate_design_id | overlaps_blocked_trade_family | blocked_reference_tokens | why |
| --- | --- | --- | --- |
| P170_FILTER_CONTEXT_ONLY | 0 | S01;S02;S03;S04;S05;S06;S07;S09;S08 | Phase170 emits context filters only and no side/order/P&L replay. |
| P170_REOPEN_TAKER_PASSIVE_OR_S08 | 1 | S01;S02;S03;S04;S05;S06;S07;S09;S08 | Any replay using closed Phase164, simple passive or Phase167 S08 forms is forbidden. |

## Gate Evaluation

| gate_id | gate_pass | evidence |
| --- | --- | --- |
| P170_PHASE169_SOURCE_MATCH | 1 | P130_FILTER_CONDITIONED_DIAGNOSTICS |
| P170_MATRIX_PRESENT | 1 | matrix_rows=228 |
| P170_DIAGNOSTIC_MODELS_PRESENT | 1 | selected_models=3 |
| P170_STRICT_TIER_TOO_NARROW_FOR_REPLAY | 1 | strict_rows=6; strict_symbols=3; strict_months=5 |
| P170_BLOCKED_FAMILY_OVERLAP_AUDITED | 1 | overlap audit includes safe context-only row and blocked reopen row |
| P170_NO_REPLAY | 1 | all replay flags are 0 |

## Context Matrix Sample

| trade_month | symbol | priority_bucket | realism_review_flag | candidate_generation_allowed | rows_scanned | feed_imperfection_rate | median_spread_bps | p90_spread_bps | mean_l1_depth | mean_l5_depth | one_tick_return_std | passive_min_adverse_rate | passive_max_cost_clearing_rate | p129_regime_stability_label | p129_liquidity_opportunity_label | p129_cost_toxicity_refinement_label | p129_cost_toxicity_refinement_bucket | tier_strict_stable_liquid_non_toxic | tier_stable_non_toxic | tier_liquid_non_toxic | phase170_context_score | phase170_feasibility_bucket | phase170_scope | strategy_replay_allowed | forbidden_outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | KOTAKBANK | P1_clean_allowed | 0 | 1 | 250000 | 0 | 2.575 | 2.62467 | 795.762 | 6763.86 | 9.47069e-05 | 0 | 0 | 1 | 1 | 0 | broad_cost_toxic_no_adverse_touch | 1 | 1 | 1 | 5 | strict_stable_liquid_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-02 | BAJAJ-AUTO | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 2.90135 | 2.91871 | 797.763 | 6780.88 | 8.60896e-05 | 0 | 0 | 1 | 1 | 0 | broad_cost_toxic_no_adverse_touch | 1 | 1 | 1 | 5 | strict_stable_liquid_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-05 | KOTAKBANK | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 2.61335 | 2.65428 | 794.734 | 6755.27 | 8.79014e-05 | 0 | 0 | 1 | 1 | 0 | broad_cost_toxic_no_adverse_touch | 1 | 1 | 1 | 5 | strict_stable_liquid_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-05 | WIPRO | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 2.22111 | 2.25632 | 796.684 | 6771.84 | 0.000102549 | 0 | 0 | 1 | 1 | 0 | broad_cost_toxic_no_adverse_touch | 1 | 1 | 1 | 5 | strict_stable_liquid_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-08 | BAJAJ-AUTO | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.89212 | 2.90234 | 795.159 | 6758.83 | 7.27295e-05 | 0 | 0 | 1 | 1 | 0 | broad_cost_toxic_no_adverse_touch | 1 | 1 | 1 | 5 | strict_stable_liquid_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-11 | KOTAKBANK | P1_clean_allowed | 0 | 1 | 250000 | 0 | 2.59605 | 2.60824 | 793.999 | 6749.05 | 7.2273e-05 | 0 | 0 | 1 | 1 | 0 | broad_cost_toxic_no_adverse_touch | 1 | 1 | 1 | 5 | strict_stable_liquid_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-01 | ADANIPORTS | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.15994 | 2.1901 | 793.856 | 6747.8 | 0.00010176 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-01 | AXISBANK | P1_clean_allowed | 0 | 1 | 250000 | 0 | 1.47874 | 1.50602 | 794.301 | 6751.73 | 7.9916e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-01 | BHARTIARTL | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 1.54631 | 1.56691 | 792.602 | 6736.89 | 5.25021e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-01 | BPCL | P1_clean_allowed | 0 | 1 | 250000 | 0 | 1.60077 | 1.62127 | 796.047 | 6766.4 | 7.89895e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-01 | DRREDDY | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 2.38796 | 2.41255 | 787.78 | 6696.35 | 6.11781e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-01 | HINDUNILVR | P1_clean_allowed | 0 | 1 | 250000 | 0 | 1.84111 | 1.86428 | 786.493 | 6685 | 7.00539e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-01 | INFY | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.77117 | 1.80148 | 797.143 | 6775.83 | 9.20345e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-01 | LT | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.24894 | 1.26557 | 791.827 | 6730.54 | 9.32361e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-01 | MARUTI | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 2.84252 | 2.89331 | 793.095 | 6741.22 | 7.79683e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-01 | ONGC | P1_clean_allowed | 0 | 1 | 250000 | 0 | 1.97973 | 2.01159 | 796.981 | 6774.24 | 9.29665e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-01 | SBIN | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 1.87582 | 1.91644 | 795.682 | 6763.24 | 0.000103729 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-01 | TCS | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.798 | 1.82017 | 796.398 | 6769.17 | 7.69784e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-02 | ADANIPORTS | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 2.20325 | 2.21043 | 798.477 | 6786.93 | 6.68748e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-02 | BHARTIARTL | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 1.56063 | 1.57011 | 796.378 | 6769.08 | 6.87151e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-02 | BPCL | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 1.62153 | 1.63132 | 796.841 | 6773.37 | 6.18573e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-02 | DRREDDY | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.42346 | 2.43348 | 788.554 | 6702.72 | 4.71197e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-02 | GOLDBEES | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 0.848896 | 0.853825 | 786.936 | 6688.91 | 5.86634e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-02 | HINDUNILVR | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.87935 | 1.88501 | 789.094 | 6707.19 | 5.35569e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-02 | KOTAKBANK | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.61575 | 2.62674 | 799.715 | 6797.8 | 6.97825e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-02 | LT | P1_clean_allowed | 0 | 1 | 250000 | 0 | 1.27136 | 1.27551 | 797.108 | 6775.31 | 7.11801e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-02 | M&M | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.26099 | 1.26912 | 795.459 | 6761.3 | 6.48857e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-02 | SBIN | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 1.92178 | 1.92957 | 799.445 | 6795.4 | 5.85322e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-02 | WIPRO | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.23003 | 2.23801 | 799.539 | 6796.09 | 6.23047e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-03 | ADANIPORTS | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.20167 | 2.21153 | 788.57 | 6702.83 | 4.90765e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-03 | BAJAJ-AUTO | P1_clean_allowed | 0 | 1 | 250000 | 0 | 2.91531 | 2.92626 | 788.521 | 6702.27 | 5.19054e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-03 | BHARTIARTL | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.57546 | 1.58504 | 787.554 | 6694.15 | 6.66237e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-03 | BPCL | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.63639 | 1.6442 | 791.335 | 6726.44 | 4.85732e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-03 | INFY | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.81785 | 1.82732 | 789.508 | 6711.11 | 5.93294e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-03 | KOTAKBANK | P1_clean_allowed | 0 | 1 | 250000 | 0 | 2.62674 | 2.64061 | 789.795 | 6713.52 | 4.54278e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-03 | LT | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.27136 | 1.27701 | 787.825 | 6696.6 | 3.90394e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-03 | M&M | P1_clean_allowed | 0 | 1 | 250000 | 0.015872 | 1.26916 | 1.27518 | 787.295 | 6691.88 | 6.13591e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-03 | MARUTI | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.9074 | 2.92334 | 786.334 | 6683.84 | 5.40384e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-03 | ONGC | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 2.03475 | 2.04616 | 791.426 | 6726.92 | 5.69017e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |
| 2026-03 | TCS | P1_clean_allowed | 0 | 1 | 250000 | 0.007936 | 1.84425 | 1.85443 | 790.014 | 6715.19 | 8.03219e-05 | 0 | 0 | 1 | 0 | 0 | broad_cost_toxic_no_adverse_touch | 0 | 1 | 0 | 4 | stable_non_toxic_context | filter_conditioned_context_feasibility_no_replay | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |

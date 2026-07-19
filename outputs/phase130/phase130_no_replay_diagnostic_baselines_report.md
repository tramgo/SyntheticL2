# Phase130 No-Replay Diagnostic Baselines

Generated UTC: 2026-07-19T23:51:41.031249+00:00

Phase130 fits deterministic baseline screeners for Phase129 diagnostic labels using a chronological holdout.
These are label diagnostics only. They do not authorize strategy replay, order simulation, or profitability claims.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase130_label_matrix_rows | 228 | Phase129 rows split for no-replay diagnostic baselines |
| phase130_baseline_result_rows | 237 | Prior and threshold baseline evaluations emitted |
| phase130_selection_rows | 3 | Label-level model selection rows emitted |
| phase130_selected_diagnostic_models | 3 | Labels with material holdout Brier improvement over prior |
| phase130_gate_rows | 6 | Gates evaluated |
| phase130_all_gates_pass | 1 | 1 means Phase130 obeys no-replay guardrails |
| phase130_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase130_current_ready_real_anchor_days | 1 | Real anchor days currently ready from Phase117 |
| phase130_additional_real_anchor_days_needed | 4 | Additional real anchor days needed before replay unlock |
| phase130_next_best_action | promote_selected_diagnostics_to_phase131_permission_update_or_continue_real_anchor_acquisition | Recommended next milestone |
| phase130_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model retained for audit continuity |

## Chronological Split Summary

| phase130_split | rows | symbols | months | trade_months | strategy_replay_allowed | p129_regime_stability_label_positive_rate | p129_liquidity_opportunity_label_positive_rate | p129_cost_toxicity_refinement_label_positive_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holdout | 56 | 32 | 2 | 2026-08;2026-11 | 0 | 0.625 | 0.0535714 | 0.357143 |
| train | 172 | 32 | 6 | 2026-01;2026-02;2026-03;2026-04;2026-05;2026-07 | 0 | 0.47093 | 0.238372 | 0.372093 |

## Diagnostic Model Selection

| label | selected_model_id | prior_brier | best_brier | brier_improvement | holdout_log_loss | holdout_accuracy | holdout_auc | model_selected | selection_reason | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p129_regime_stability_label | threshold_feed_imperfection_rate_le_0.015872 | 0.258112 | 0.0828571 | 0.175255 | 0.322165 | 0.928571 | 0.904762 | True | beats_prior_brier_by_minimum_margin | 0 |
| p129_liquidity_opportunity_label | threshold_median_spread_bps_ge_4.0782951 | 0.0848528 | 0.0721429 | 0.01271 | 0.297409 | 0.946429 | 0.5 | True | beats_prior_brier_by_minimum_margin | 0 |
| p129_cost_toxicity_refinement_label | threshold_passive_min_adverse_rate_ge_0.99099099 | 0.229815 | 0.104286 | 0.12553 | 0.371675 | 0.892857 | 0.85 | True | beats_prior_brier_by_minimum_margin | 0 |

## Best Baseline Results

| label | model_id | train_rows | holdout_rows | train_positive_rate | holdout_positive_rate | holdout_brier | holdout_log_loss | holdout_accuracy | holdout_auc | strategy_replay_allowed | forbidden_outputs | feature | direction | threshold | train_prediction_rate | baseline_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p129_cost_toxicity_refinement_label | threshold_passive_min_adverse_rate_ge_0.99099099 | 172 | 56 | 0.372093 | 0.357143 | 0.104286 | 0.371675 | 0.892857 | 0.85 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | passive_min_adverse_rate | ge | 0.990991 | 0.261628 | single_feature_threshold |
| p129_cost_toxicity_refinement_label | threshold_passive_min_adverse_rate_ge_1 | 172 | 56 | 0.372093 | 0.357143 | 0.147143 | 0.470696 | 0.821429 | 0.75 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | passive_min_adverse_rate | ge | 1 | 0.19186 | single_feature_threshold |
| p129_cost_toxicity_refinement_label | threshold_one_tick_return_std_le_5.3568678e-05 | 172 | 56 | 0.372093 | 0.357143 | 0.211429 | 0.619228 | 0.714286 | 0.655556 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | one_tick_return_std | le | 5.35687e-05 | 0.104651 | single_feature_threshold |
| p129_cost_toxicity_refinement_label | train_prior_probability | 172 | 56 | 0.372093 | 0.357143 | 0.229815 | 0.652238 | 0.642857 | 0.5 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim |  |  |  | 0.372093 | prior |
| p129_cost_toxicity_refinement_label | threshold_mean_l1_depth_le_785.66711 | 172 | 56 | 0.372093 | 0.357143 | 0.232857 | 0.668738 | 0.678571 | 0.605556 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | mean_l1_depth | le | 785.667 | 0.104651 | single_feature_threshold |
| p129_liquidity_opportunity_label | threshold_median_spread_bps_ge_4.0782951 | 172 | 56 | 0.238372 | 0.0535714 | 0.0721429 | 0.297409 | 0.946429 | 0.5 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | median_spread_bps | ge | 4.0783 | 0.104651 | single_feature_threshold |
| p129_liquidity_opportunity_label | threshold_p90_spread_bps_ge_4.1309086 | 172 | 56 | 0.238372 | 0.0535714 | 0.0721429 | 0.297409 | 0.946429 | 0.5 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | p90_spread_bps | ge | 4.13091 | 0.104651 | single_feature_threshold |
| p129_liquidity_opportunity_label | threshold_mean_l1_depth_ge_974.78298 | 172 | 56 | 0.238372 | 0.0535714 | 0.0721429 | 0.297409 | 0.946429 | 0.5 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | mean_l1_depth | ge | 974.783 | 0.104651 | single_feature_threshold |
| p129_liquidity_opportunity_label | threshold_mean_l5_depth_ge_8285.6157 | 172 | 56 | 0.238372 | 0.0535714 | 0.0721429 | 0.297409 | 0.946429 | 0.5 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | mean_l5_depth | ge | 8285.62 | 0.104651 | single_feature_threshold |
| p129_liquidity_opportunity_label | threshold_one_tick_return_std_ge_0.00010453475 | 172 | 56 | 0.238372 | 0.0535714 | 0.0721429 | 0.297409 | 0.946429 | 0.5 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | one_tick_return_std | ge | 0.000104535 | 0.25 | single_feature_threshold |
| p129_regime_stability_label | threshold_feed_imperfection_rate_le_0.015872 | 172 | 56 | 0.47093 | 0.625 | 0.0828571 | 0.322165 | 0.928571 | 0.904762 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | feed_imperfection_rate | le | 0.015872 | 0.593023 | single_feature_threshold |
| p129_regime_stability_label | threshold_realism_review_flag_le_0 | 172 | 56 | 0.47093 | 0.625 | 0.0828571 | 0.322165 | 0.928571 | 0.904762 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | realism_review_flag | le | 0 | 0.593023 | single_feature_threshold |
| p129_regime_stability_label | threshold_regime_realism_risk_label_le_0 | 172 | 56 | 0.47093 | 0.625 | 0.104286 | 0.371675 | 0.892857 | 0.857143 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | regime_realism_risk_label | le | 0 | 0.55814 | single_feature_threshold |
| p129_regime_stability_label | threshold_feed_imperfection_rate_le_0.007936 | 172 | 56 | 0.47093 | 0.625 | 0.179286 | 0.544962 | 0.767857 | 0.785714 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | feed_imperfection_rate | le | 0.007936 | 0.337209 | single_feature_threshold |
| p129_regime_stability_label | threshold_feed_imperfection_rate_le_0.023808 | 172 | 56 | 0.47093 | 0.625 | 0.19 | 0.569717 | 0.75 | 0.666667 | 0 | buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim | feed_imperfection_rate | le | 0.023808 | 0.773256 | single_feature_threshold |

## Guardrails

| guardrail_id | requirement | enforcement |
| --- | --- | --- |
| P130_NO_REPLAY | Phase130 fits diagnostic label baselines only and cannot emit strategy replay artifacts. | strategy_replay_allowed=0 and forbidden_outputs carried through every model row. |
| P130_CHRONOLOGICAL_HOLDOUT | Model diagnostics must be evaluated on later months than the fit set. | phase130_split assigns the final two trade months to holdout. |
| P130_BASELINES_NOT_TRADING_RULES | Selected models are screeners for label quality, not buy/sell rules. | Forbidden outputs remain buy_sell_signal;side;order_arrival;fill_model;pnl_replay;profitability_claim. |
| P130_REAL_ANCHOR_REMAINS_PRIMARY | More real Zerodha L2 days remain the primary path to future replay unlock. | Phase117 real-anchor blocker is carried into the acceptance summary. |

## Gate Evaluation

| gate_id | gate_pass | evidence |
| --- | --- | --- |
| P130_SPLIT_EXISTS | 1 | split_rows=2; holdout_rows=56 |
| P130_BASELINE_RESULTS_EXIST | 1 | baseline_result_rows=237 |
| P130_SELECTION_ROWS_EXIST | 1 | selection_rows=3 |
| P130_MATERIAL_DIAGNOSTIC_SIGNAL | 1 | selected_models=3 |
| P130_NO_REPLAY | 1 | strategy_replay_allowed remains 0 |
| P130_REAL_ANCHOR_STILL_PRIMARY | 1 | ready_real_anchor_days=1; days_needed=4 |

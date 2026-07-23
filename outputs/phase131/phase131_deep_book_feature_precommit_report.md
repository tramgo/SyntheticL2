# Phase131 Deep-Book Feature and Cost-Stress Precommit

Generated UTC: 2026-07-23T05:58:29.562086+00:00

Phase131 locks the deep-book feature catalog, base/harsh cost regimes, and evaluation rules before Phase132 diagnostics touch data.
It emits specifications only and explicitly forbids strategy code, order simulation, P&L replay, and profitability claims.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase131_feature_catalog_rows | 10 | Precommitted L2-L5 feature definitions |
| phase131_l1_only_feature_rows | 0 | Feature definitions incorrectly depending only on L1 |
| phase131_cost_regime_rows | 2 | Immutable cost regimes declared |
| phase131_phase130_baseline_reference_rows | 3 | Phase130 baseline references for Phase132 ordering/lift checks |
| phase131_allowed_context_rows | 228 | Allowed Phase129 contexts locked as Phase132 dataset |
| phase131_brier_lift_margin | 0.005 | Minimum Brier lift over Phase130 baseline required in Phase132 |
| phase131_gate_rows | 7 | Gates evaluated |
| phase131_all_gates_pass | 1 | 1 means Phase131 precommit is self-consistent |
| phase131_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase131_next_best_action | run_phase132_deep_book_feature_diagnostics_or_stop_if_precommit_fails | Recommended next milestone |
| phase131_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha model retained unchanged |

## Feature Catalog

| feature_id | definition | required_depth_levels | minimum_depth_level | maximum_depth_level | directional_use | candidate_label_targets | forbidden_use | phase132_model_family | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p131_l2_l5_depth_ratio_bid | bid_level_2_quantity / max(sum(bid_level_2_quantity..bid_level_5_quantity), 1) | L2,L3,L4,L5 | 2 | 5 | bid_resilience_context | p129_regime_stability_label;p129_liquidity_opportunity_label | entry_side_or_order_signal | single_feature_threshold;two_feature_threshold_combo | 0 |
| p131_l2_l5_depth_ratio_ask | ask_level_2_quantity / max(sum(ask_level_2_quantity..ask_level_5_quantity), 1) | L2,L3,L4,L5 | 2 | 5 | ask_resilience_context | p129_regime_stability_label;p129_liquidity_opportunity_label | entry_side_or_order_signal | single_feature_threshold;two_feature_threshold_combo | 0 |
| p131_cumulative_notional_imbalance_top5 | (sum(bid_level_1_notional..bid_level_5_notional) - sum(ask_level_1_notional..ask_level_5_notional)) / max(total_top5_notional, 1) | L1,L2,L3,L4,L5 | 2 | 5 | deep_book_pressure_context | p129_liquidity_opportunity_label;p129_cost_toxicity_refinement_label | entry_side_or_order_signal | single_feature_threshold;two_feature_threshold_combo | 0 |
| p131_book_thinning_event_rate_1s | rolling_1s_count(sum_top5_depth_t < 0.75 * rolling_5s_median_sum_top5_depth) | L1,L2,L3,L4,L5 | 2 | 5 | liquidity_withdrawal_context | p129_regime_stability_label;p129_cost_toxicity_refinement_label | entry_side_or_order_signal | single_feature_threshold;two_feature_threshold_combo | 0 |
| p131_level_crossing_hazard_bid | rolling_1s_rate(best_bid_price moves through prior bid_level_2_price or deeper bid levels) | L2,L3,L4,L5 | 2 | 5 | bid_queue_depletion_context | p129_cost_toxicity_refinement_label | entry_side_or_order_signal | single_feature_threshold;two_feature_threshold_combo | 0 |
| p131_level_crossing_hazard_ask | rolling_1s_rate(best_ask_price moves through prior ask_level_2_price or deeper ask levels) | L2,L3,L4,L5 | 2 | 5 | ask_queue_depletion_context | p129_cost_toxicity_refinement_label | entry_side_or_order_signal | single_feature_threshold;two_feature_threshold_combo | 0 |
| p131_depth_slope_top5_bid | linear_slope(level_index, bid_level_1_quantity..bid_level_5_quantity) | L1,L2,L3,L4,L5 | 2 | 5 | bid_depth_shape_context | p129_regime_stability_label;p129_liquidity_opportunity_label | entry_side_or_order_signal | single_feature_threshold;two_feature_threshold_combo | 0 |
| p131_depth_slope_top5_ask | linear_slope(level_index, ask_level_1_quantity..ask_level_5_quantity) | L1,L2,L3,L4,L5 | 2 | 5 | ask_depth_shape_context | p129_regime_stability_label;p129_liquidity_opportunity_label | entry_side_or_order_signal | single_feature_threshold;two_feature_threshold_combo | 0 |
| p131_mean_cancel_intensity_l2_l5 | rolling_mean(abs(delta_depth_l2..delta_depth_l5) where price level persists and depth decreases) | L2,L3,L4,L5 | 2 | 5 | passive_fill_realism_context | p129_cost_toxicity_refinement_label | entry_side_or_order_signal | single_feature_threshold;two_feature_threshold_combo | 0 |
| p131_deep_book_pressure_signed | signed combination of top5 notional imbalance, bid/ask depth slopes, and l2_l5 cancel-intensity asymmetry | L2,L3,L4,L5 | 2 | 5 | deep_book_context_only | p129_regime_stability_label;p129_liquidity_opportunity_label;p129_cost_toxicity_refinement_label | entry_side_or_order_signal | single_feature_threshold;two_feature_threshold_combo | 0 |

## Cost Regimes

| cost_regime_id | cost_model_version | zerodha_formula_edit_allowed | spread_cross_cost_multiplier | brokerage_multiplier | stt_multiplier | transaction_charge_multiplier | sebi_charge_multiplier | stamp_duty_multiplier | gst_multiplier | description | immutable_after_phase131 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | Pinned Zerodha equity intraday NSE retail cash cost model unchanged. | 1 |
| harsh | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | 0 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | Pinned Zerodha formula plus 25 percent uplift to spread-cross cost and every per-leg fee component. | 1 |

## Phase130 Baseline Reference

| label | reference_family | selected_model_id | best_brier | holdout_auc | minimum_brier_lift_required_for_phase132 | strategy_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| p129_regime_stability_label | phase130_l1_context_diagnostic_baseline | threshold_feed_imperfection_rate_le_0.015872 | 0.0828571 | 0.904762 | 0.005 | 0 |
| p129_liquidity_opportunity_label | phase130_l1_context_diagnostic_baseline | threshold_median_spread_bps_ge_4.0782951 | 0.0721429 | 0.5 | 0.005 | 0 |
| p129_cost_toxicity_refinement_label | phase130_l1_context_diagnostic_baseline | threshold_passive_min_adverse_rate_ge_0.99099099 | 0.104286 | 0.85 | 0.005 | 0 |

## Guardrails

| guardrail_id | requirement | enforcement |
| --- | --- | --- |
| P131_RETAIL_CASH_EQUITY_ONLY | Instrument scope remains NSE cash equity in the 32-symbol Phase96/Phase129 panel. | Allowed dataset is locked to Phase129 allowed_context_label_matrix.csv. |
| P131_DEPTH_REQUIRES_L2_L5 | No precommitted feature may depend only on L1. | Feature catalog must set minimum_depth_level >= 2 for every feature. |
| P131_COST_MODEL_PINNED | Base regime must preserve the pinned Zerodha equity intraday NSE model exactly. | cost_model_version must equal zerodha_equity_intraday_nse_order_formula_v2_2026_07_14. |
| P131_HARSH_REGIME_IMMUTABLE | Harsh stress factors are declared once and cannot be edited by later phases in this plan. | phase131_cost_regimes.csv records immutable_after_phase131=1 for base and harsh. |
| P131_NO_REPLAY_OR_PROFIT_CLAIMS | Phase131 ships specifications only. | Forbidden outputs: strategy_code;buy_sell_signal;order_arrival_stream;live_tagged_fill_model;pnl_replay;profitability_claim. |

## Gate Evaluation

| gate_id | gate_pass | evidence |
| --- | --- | --- |
| P131_FEATURE_CATALOG_SIZE | 1 | feature_rows=10 |
| P131_NO_L1_ONLY_FEATURES | 1 | minimum_depth_level>=2 for every feature |
| P131_COST_REGIMES_LOCKED | 1 | cost_regimes=base;harsh |
| P131_PINNED_COST_MODEL_MATCH | 1 | repo_cost_model=zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| P131_ALLOWED_DATASET_EXISTS | 1 | allowed_context_rows=228 |
| P131_PHASE130_BASELINE_REFERENCE_EXISTS | 1 | baseline_reference_rows=3 |
| P131_NO_REPLAY | 1 | feature and baseline artifacts keep strategy_replay_allowed=0 |

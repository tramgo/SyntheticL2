# Phase 11 Strategy Validation Matrix Report

Generated UTC: 2026-07-13T20:47:00.298235+00:00

## Scope

This phase defines strategy experiments and runs preliminary signal diagnostics against current Phase 9 Tier C features.
These diagnostics are not strategy acceptance results. The current feature product is 5-minute synthetic data derived from a one-day real sample.

## Support Levels

| support_level | strategies |
| --- | --- |
| runnable_proxy | 5 |
| partial_missing_required_features | 4 |
| not_supported_by_current_product | 2 |

## Preliminary Signal Diagnostics

| strategy_id | signal_rows | signal_fraction | signed_mean_future_return | directional_accuracy_nonzero | status |
| --- | --- | --- | --- | --- | --- |
| S01 | 164253 | 0.0727032 | -0.00108613 | 0.434982 | diagnostic_only_not_acceptance_test |
| S02 | 898620 | 0.397755 | -0.00011217 | 0.485755 | diagnostic_only_not_acceptance_test |
| S03 | 280476 | 0.124147 | -0.000691527 | 0.467834 | diagnostic_only_not_acceptance_test |
| S04 | 424887 | 0.188067 | -0.000203103 | 0.480829 | diagnostic_only_not_acceptance_test |
| S05 | 445798 | 0.197323 | -3.00993e-05 | 0.497367 | diagnostic_only_not_acceptance_test |
| S06 | 33993 | 0.0150463 | 2.70872e-05 | 0.505455 | diagnostic_only_not_acceptance_test |
| S07 | 234925 | 0.103985 | 2.68998e-05 | 0.501421 | diagnostic_only_not_acceptance_test |
| S08 | 442644 | 0.195927 | 4.8916e-06 | 0.504006 | diagnostic_only_not_acceptance_test |
| S09 | 585341 | 0.259089 | -1.41998e-05 | 0.49772 | diagnostic_only_not_acceptance_test |
| S10 | 0 | 0 |  |  | not_evaluated_missing_product_support |
| S11 | 0 | 0 |  |  | not_evaluated_missing_product_support |

## Feature Availability

| strategy_id | support_level | proxy_features_present | proxy_features_absent | plan_missing_features |
| --- | --- | --- | --- | --- |
| S01 | runnable_proxy | 5 | 0 | trade_flow_confirmation; true_1s_lookbacks; market_or_sector_alignment |
| S02 | runnable_proxy | 4 | 0 | true_l1_ofi; next_quote_move_label; multi_horizon_second_labels |
| S03 | partial_missing_required_features | 4 | 0 | explicit_depth_withdrawal_rate; aggressive_trade_flow; multi_level_sweep_labels |
| S04 | partial_missing_required_features | 4 | 0 | aggressive_trade_imbalance; absorption_label; exhaustion_label |
| S05 | runnable_proxy | 4 | 0 | next_tick_direction; entry_slippage; parent_strategy_linkage |
| S06 | partial_missing_required_features | 4 | 0 | signed_aggressive_flow; flow_reversal; replenishment_rate |
| S07 | runnable_proxy | 4 | 0 | explicit_replenishment_rate; trend_suppression_gate |
| S08 | partial_missing_required_features | 5 | 0 | sector_mapping; leader_labels; timestamp_skew_simulations; explicit_lead_lag_scenarios |
| S09 | runnable_proxy | 3 | 0 | queue_position; 50_100_250_500ms_labels; cost_model |
| S10 | not_supported_by_current_product | 0 | 0 | queue_position; fill_model; inventory_model; cancellation_latency; order_simulator |
| S11 | not_supported_by_current_product | 0 | 0 | order_lifetime_proxy; wall_tracking; touch/non_touch_events; cancellation_labels |

## Outputs

- `strategy_validation_matrix.csv`
- `baseline_strategy_matrix.csv`
- `strategy_feature_availability.csv`
- `strategy_signal_diagnostics.csv`
- `strategy_validation_manifest.json`

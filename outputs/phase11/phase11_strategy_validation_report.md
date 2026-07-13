# Phase 11 Strategy Validation Matrix Report

Generated UTC: 2026-07-13T15:21:14.568470+00:00

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
| S01 | 164347 | 0.0727508 | -0.00110589 | 0.434302 | diagnostic_only_not_acceptance_test |
| S02 | 889386 | 0.393701 | -0.000113875 | 0.485228 | diagnostic_only_not_acceptance_test |
| S03 | 280437 | 0.12414 | -0.000700219 | 0.466749 | diagnostic_only_not_acceptance_test |
| S04 | 424857 | 0.18807 | -0.00020299 | 0.480748 | diagnostic_only_not_acceptance_test |
| S05 | 445761 | 0.197323 | -3.17341e-05 | 0.497055 | diagnostic_only_not_acceptance_test |
| S06 | 33809 | 0.0149661 | 4.1775e-05 | 0.505817 | diagnostic_only_not_acceptance_test |
| S07 | 234969 | 0.104013 | 2.61682e-05 | 0.501803 | diagnostic_only_not_acceptance_test |
| S08 | 442897 | 0.196055 | 2.1323e-05 | 0.506523 | diagnostic_only_not_acceptance_test |
| S09 | 585389 | 0.259132 | -1.37599e-05 | 0.497817 | diagnostic_only_not_acceptance_test |
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

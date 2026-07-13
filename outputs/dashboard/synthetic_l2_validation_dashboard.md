# SyntheticL2 Validation Dashboard Summary

Generated UTC: 2026-07-13T22:23:52.565047+00:00

This dashboard is static research traceability output, not strategy promotion evidence.

## Summary Metrics

| metric | value | note |
| --- | --- | --- |
| quality_checks | 24 | Phase 14 quality rows |
| quality_warn_checks | 0 | Current quality warnings |
| quality_fail_checks | 0 | Current quality failures |
| holdout_proxy_rows | 15 | Phase 14 holdout generator proxy rows |
| holdout_proxy_available_rows | 15 | Holdout proxy rows structurally available |
| full_run_lifecycle_risk_rows | 81 | Phase 12 full-run fill-adjusted risk rows |
| full_run_lifecycle_fill_models | 3 | Phase 12 full-run fill models |
| full_run_lifecycle_daily_halt_rows | 21299578 | Phase 12 full-run lifecycle halt rows |
| robustness_dimension_rows | 11 | Phase 13 robustness dimension rows |
| robustness_dimension_registered_rows | 9 | Phase 13 registered robustness proxy rows |
| strategies | 11 | Phase 15 strategies |
| promoted_strategies | 0 | Promotion allowed count |
| acceptance_blockers | 50 | Phase 15 blocker rows |
| metric_catalog_rows | 29 | Phase 16 metric catalog rows |
| predictive_holdout_summary_rows | 11 | Phase 16 predictive holdout stability summary rows |
| predictive_holdout_all_cell_pass_rows | 0 | Predictive holdout all-cell pass rows |
| economic_viability_rows | 27 | Phase 16 economic viability frontier rows |
| economic_viability_net_positive_rows | 4 | Phase 16 net-positive proxy rows |
| economic_viability_retail_stress_positive_rows | 2 | Retail/stress net-positive proxy rows |
| acceptance_grade_metrics | 0 | Acceptance-grade metrics |
| missing_metrics | 0 | Missing metric rows |
| p1_gaps | 0 | Phase 17 P1 backlog rows |

## Quality Status

| status | checks |
| --- | --- |
| pass | 24 |

## Holdout Generator Realism Proxy

| quarter_profile | feed_profile | holdout_role | scenario_days | feature_rows | symbols | regimes | market_shock_days | median_spread_ticks | nonzero_mid_return_fraction | structural_ready_for_holdout_proxy | realism_status | acceptance_eligible_now | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-A | disconnect_scenario | development_reference_profile | 63 | 149177 | 32 | 18 | 7 | 4.0 | 0.9677430166848776 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-A | good_retail | development_reference_profile | 63 | 151225 | 32 | 18 | 7 | 4.0 | 0.9656009257728552 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-A | ideal_research | development_reference_profile | 63 | 151200 | 32 | 18 | 7 | 4.0 | 0.9667857142857142 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-A | normal_retail | development_reference_profile | 63 | 151070 | 32 | 18 | 7 | 4.0 | 0.9653736678361023 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-A | stressed_retail | development_reference_profile | 63 | 150394 | 32 | 18 | 7 | 4.0 | 0.964679441999016 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-B | disconnect_scenario | bullish_high_momentum_holdout_proxy | 63 | 149207 | 32 | 18 | 10 | 4.0 | 0.9684063080150396 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-B | good_retail | bullish_high_momentum_holdout_proxy | 63 | 151175 | 32 | 18 | 10 | 4.0 | 0.9668794443525716 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-B | ideal_research | bullish_high_momentum_holdout_proxy | 63 | 151200 | 32 | 18 | 10 | 4.0 | 0.9678505291005292 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-B | normal_retail | bullish_high_momentum_holdout_proxy | 63 | 151016 | 32 | 18 | 10 | 4.0 | 0.9666260528685702 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-B | stressed_retail | bullish_high_momentum_holdout_proxy | 63 | 150414 | 32 | 18 | 10 | 4.0 | 0.966226548060686 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-C | disconnect_scenario | stressed_volatile_holdout_proxy | 63 | 149278 | 32 | 18 | 8 | 4.0 | 0.9697544179316444 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-C | good_retail | stressed_volatile_holdout_proxy | 63 | 151181 | 32 | 18 | 8 | 4.0 | 0.96852117660288 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-C | ideal_research | stressed_volatile_holdout_proxy | 63 | 151200 | 32 | 18 | 8 | 4.0 | 0.9695767195767196 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-C | normal_retail | stressed_volatile_holdout_proxy | 63 | 151040 | 32 | 18 | 8 | 4.0 | 0.9681475105932204 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-C | stressed_retail | stressed_volatile_holdout_proxy | 63 | 150451 | 32 | 18 | 8 | 4.0 | 0.9671055692551064 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |

## Phase 12 Full-Run Lifecycle Risk Proxy

| fill_model | strategy_profiles | orders | mean_fill_ratio | risk_adjusted_net_pnl_inr | daily_halt_rows | position_limit_breach_rows |
| --- | --- | --- | --- | --- | --- | --- |
| neutral_partial | 27 | 10375860 | 0.7045303605574683 | 205634027.27410844 | 7329401 | 3241574 |
| optimistic_marketable | 27 | 10375860 | 0.9859071061166582 | 295398866.74432045 | 7877052 | 3757171 |
| pessimistic_partial | 27 | 10375860 | 0.37155813610202526 | 120472769.73654498 | 6093125 | 2422779 |

## Phase 13 Robustness Dimension Proxy

| dimension_status | strategies |
| --- | --- |
| robustness_proxy_dimensions_available_not_acceptance | 9 |
| not_registered_for_phase13_proxy_run | 2 |

## Economic Viability Frontier

| strategy_id | name | support_level | execution_profile | trades | gross_edge_bps | cost_drag_bps | zerodha_charge_bps | non_zerodha_cost_bps | net_edge_bps | break_even_cost_bps | cost_surplus_bps | additional_gross_edge_needed_bps | cost_reduction_needed_bps | gross_edge_covers_cost | net_positive_proxy | retail_or_stress_profile | economic_frontier_status | promotion_allowed | acceptance_status | acceptance_eligible_now | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Momentum/breakout filtered by MLOFI | runnable_proxy | retail_marketable_default | 160471 | 74.760393289249 | 10.249237888938 | 8.266592935395762 | 1.9826449535422377 | 64.51115540031 | 74.760393289249 | 64.511155400311 | 0.0 | 0.0 | True | True | True | net_positive_proxy_not_acceptance | False | blocked_not_promotable | False | Proxy net edge is positive for this profile, but acceptance still requires broker/exchange fills, multi-day holdout and stress-profile confirmation. |
| S03 | Liquidity-vacuum breakout | partial_missing_required_features | retail_marketable_default | 273427 | 59.836470487996 | 9.620566718578 | 8.260697152932746 | 1.359869565645253 | 50.215903769418 | 59.836470487996 | 50.215903769418 | 0.0 | 0.0 | True | True | True | net_positive_proxy_not_acceptance | False | blocked_not_promotable | False | Proxy net edge is positive for this profile, but acceptance still requires broker/exchange fills, multi-day holdout and stress-profile confirmation. |
| S05 | Microprice entry/exit filter | runnable_proxy | zero_latency_spread_only_control | 449765 | 14.992445437322 | 3.341745249178 | 0.0 | 3.341745249178 | 11.650700188144 | 14.992445437322 | 11.650700188144 | 0.0 | 0.0 | True | True | False | control_profile_not_deployable | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S06 | Absorption and exhaustion reversal | partial_missing_required_features | zero_latency_spread_only_control | 34373 | 3.935459142181 | 2.080124557989 | 0.0 | 2.080124557989 | 1.855334584192 | 3.935459142181 | 1.855334584192 | 0.0 | 0.0 | True | True | False | control_profile_not_deployable | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S08 | Cross-ticker/index lead-lag OFI | partial_missing_required_features | zero_latency_spread_only_control | 448403 | 0.0943769477099951 | 1.57570748739 | 0.0 | 1.57570748739 | -1.4813305396799998 | 0.0943769477099951 | -1.4813305396800047 | 1.4813305396799998 | 1.4813305396800047 | False | False | False | control_profile_not_deployable | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S09 | Pure queue-imbalance scalping | runnable_proxy | zero_latency_spread_only_control | 590612 | -0.2080910803893485 | 2.503588038854 | 0.0 | 2.503588038854 | -2.711679119243 | -0.2080910803893485 | -2.7116791192433483 | 2.711679119243 | 2.7116791192433483 | False | False | False | control_profile_not_deployable | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S02 | Pure multi-level OFI directional model | runnable_proxy | zero_latency_spread_only_control | 907352 | -0.9215628481930452 | 2.069336138396 | 0.0 | 2.069336138396 | -2.990898986589 | -0.9215628481930452 | -2.990898986589045 | 2.990898986589 | 2.990898986589045 | False | False | False | control_profile_not_deployable | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S04 | Trade-flow plus depth confirmation | partial_missing_required_features | retail_marketable_default | 414066 | 6.981384287435 | 10.987891999384 | 8.261469729475738 | 2.7264222699082623 | -4.006507711948 | 6.981384287435 | -4.006507711949001 | 4.006507711948 | 4.006507711949001 | False | False | True | below_break_even_after_costs | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S03 | Liquidity-vacuum breakout | partial_missing_required_features | stressed_retail | 270999 | 3.692505532512 | 11.3991014165 | 8.270247998190266 | 3.128853418309733 | -7.706595883988 | 3.692505532512 | -7.706595883987999 | 7.706595883988 | 7.706595883987999 | False | False | True | below_break_even_after_costs | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S07 | Mean reversion after imbalance | runnable_proxy | zero_latency_spread_only_control | 237064 | -4.911728289385 | 3.824058354058 | 0.0 | 3.824058354058 | -8.735786643444 | -4.911728289385 | -8.735786643443 | 8.735786643444 | 8.735786643443 | False | False | False | control_profile_not_deployable | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S04 | Trade-flow plus depth confirmation | partial_missing_required_features | zero_latency_spread_only_control | 429202 | -7.1105476438010005 | 2.005682032167 | 0.0 | 2.005682032167 | -9.116229675968 | -7.1105476438010005 | -9.116229675968 | 9.116229675968 | 9.116229675968 | False | False | False | control_profile_not_deployable | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S09 | Pure queue-imbalance scalping | runnable_proxy | retail_marketable_default | 573028 | 1.7996209664949998 | 12.339237888551 | 8.268573781734355 | 4.070664106816645 | -10.539616922056 | 1.7996209664949998 | -10.539616922056 | 10.539616922056 | 10.539616922056 | False | False | True | below_break_even_after_costs | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S08 | Cross-ticker/index lead-lag OFI | partial_missing_required_features | retail_marketable_default | 431798 | 0.3049667915600301 | 10.959285472087998 | 8.267795228804319 | 2.69149024328368 | -10.654318680528 | 0.3049667915600301 | -10.654318680527968 | 10.654318680528 | 10.654318680527968 | False | False | True | below_break_even_after_costs | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S07 | Mean reversion after imbalance | runnable_proxy | retail_marketable_default | 229792 | 3.231440639469 | 13.89326489566 | 8.266996167304834 | 5.626268728355166 | -10.66182425619 | 3.231440639469 | -10.661824256191 | 10.66182425619 | 10.661824256191 | False | False | True | below_break_even_after_costs | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S06 | Absorption and exhaustion reversal | partial_missing_required_features | stressed_retail | 32935 | 2.526985915549 | 13.221550126634 | 8.269792530893584 | 4.951757595740416 | -10.694564211084 | 2.526985915549 | -10.694564211085 | 10.694564211084 | 10.694564211085 | False | False | True | below_break_even_after_costs | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S01 | Momentum/breakout filtered by MLOFI | runnable_proxy | stressed_retail | 158070 | 1.03743080932 | 12.37159007637 | 8.268246537919211 | 4.103343538450789 | -11.33415926705 | 1.03743080932 | -11.33415926705 | 11.33415926705 | 11.33415926705 | False | False | True | below_break_even_after_costs | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S02 | Pure multi-level OFI directional model | runnable_proxy | retail_marketable_default | 879151 | 0.4019765980417236 | 11.832794974048 | 8.26839372161083 | 3.564401252437172 | -11.430818376006 | 0.4019765980417236 | -11.430818376006275 | 11.430818376006 | 11.430818376006275 | False | False | True | below_break_even_after_costs | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |
| S09 | Pure queue-imbalance scalping | runnable_proxy | stressed_retail | 567805 | 2.042345443432 | 14.9065766132 | 8.268595855650151 | 6.637980757549848 | -12.864231169767 | 2.042345443432 | -12.864231169768 | 12.864231169767 | 12.864231169768 | False | False | True | below_break_even_after_costs | False | blocked_not_promotable | False | Proxy net edge is not positive after the current cost/slippage/latency assumptions; improve gross edge, lower turnover/cost exposure, or reject the strategy before promotion. |

## Predictive Holdout Stability

| strategy_id | name | support_level | stability_cells | cells_with_minimum_rows | cells_beating_local_majority | cell_beat_fraction | untouched_test_cells | untouched_test_cells_beating_local_majority | min_accuracy_excess_vs_majority | median_accuracy_excess_vs_majority | worst_segment_status | acceptance_eligible_now | blocker | metric_scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S08 | Cross-ticker/index lead-lag OFI | partial_missing_required_features | 45 | 45 | 5 | 0.1111111111111111 | 15 | 0 | -0.0559028187286236 | -0.0190096221544238 | fails_some_holdout_stability_cells | False | Proxy holdout stability cells do not consistently beat local majority baselines; acceptance requires multi-seed, walk-forward and later real holdout predictive validation. | phase16_predictive_holdout_stability_summary_proxy_not_acceptance |
| S05 | Microprice entry/exit filter | runnable_proxy | 45 | 45 | 4 | 0.0888888888888888 | 15 | 0 | -0.0322389825495415 | -0.0101295130598365 | fails_some_holdout_stability_cells | False | Proxy holdout stability cells do not consistently beat local majority baselines; acceptance requires multi-seed, walk-forward and later real holdout predictive validation. | phase16_predictive_holdout_stability_summary_proxy_not_acceptance |
| S02 | Pure multi-level OFI directional model | runnable_proxy | 45 | 45 | 4 | 0.0888888888888888 | 15 | 4 | -0.0620126794432704 | -0.0176678445229682 | fails_some_holdout_stability_cells | False | Proxy holdout stability cells do not consistently beat local majority baselines; acceptance requires multi-seed, walk-forward and later real holdout predictive validation. | phase16_predictive_holdout_stability_summary_proxy_not_acceptance |
| S07 | Mean reversion after imbalance | runnable_proxy | 45 | 45 | 4 | 0.0888888888888888 | 15 | 1 | -0.0176427346238666 | -0.0071253071253071 | fails_some_holdout_stability_cells | False | Proxy holdout stability cells do not consistently beat local majority baselines; acceptance requires multi-seed, walk-forward and later real holdout predictive validation. | phase16_predictive_holdout_stability_summary_proxy_not_acceptance |
| S06 | Absorption and exhaustion reversal | partial_missing_required_features | 45 | 10 | 1 | 0.0222222222222222 | 15 | 0 | -0.1195652173913043 | -0.0248528449967299 | fails_some_holdout_stability_cells | False | Proxy holdout stability cells do not consistently beat local majority baselines; acceptance requires multi-seed, walk-forward and later real holdout predictive validation. | phase16_predictive_holdout_stability_summary_proxy_not_acceptance |
| S03 | Liquidity-vacuum breakout | partial_missing_required_features | 45 | 45 | 0 | 0.0 | 15 | 0 | -0.1369958275382476 | -0.0488489612577203 | fails_some_holdout_stability_cells | False | Proxy holdout stability cells do not consistently beat local majority baselines; acceptance requires multi-seed, walk-forward and later real holdout predictive validation. | phase16_predictive_holdout_stability_summary_proxy_not_acceptance |
| S01 | Momentum/breakout filtered by MLOFI | runnable_proxy | 45 | 45 | 0 | 0.0 | 15 | 0 | -0.1673688242052853 | -0.0603063178047224 | fails_some_holdout_stability_cells | False | Proxy holdout stability cells do not consistently beat local majority baselines; acceptance requires multi-seed, walk-forward and later real holdout predictive validation. | phase16_predictive_holdout_stability_summary_proxy_not_acceptance |
| S04 | Trade-flow plus depth confirmation | partial_missing_required_features | 45 | 45 | 0 | 0.0 | 15 | 0 | -0.0877592888078412 | -0.035155442200317 | fails_some_holdout_stability_cells | False | Proxy holdout stability cells do not consistently beat local majority baselines; acceptance requires multi-seed, walk-forward and later real holdout predictive validation. | phase16_predictive_holdout_stability_summary_proxy_not_acceptance |
| S09 | Pure queue-imbalance scalping | runnable_proxy | 45 | 45 | 0 | 0.0 | 15 | 0 | -0.0309600367478181 | -0.0080994119605015 | fails_some_holdout_stability_cells | False | Proxy holdout stability cells do not consistently beat local majority baselines; acceptance requires multi-seed, walk-forward and later real holdout predictive validation. | phase16_predictive_holdout_stability_summary_proxy_not_acceptance |
| S10 | Passive market making | not_supported_by_current_product | 0 | 0 | 0 | 0.0 | 0 | 0 |  |  | not_supported_by_current_product | False | Strategy is not supported by the current feature product for predictive holdout stability validation. | phase16_predictive_holdout_stability_summary_proxy_not_acceptance |
| S11 | Spoof-like wall filter | not_supported_by_current_product | 0 | 0 | 0 | 0.0 | 0 | 0 |  |  | not_supported_by_current_product | False | Strategy is not supported by the current feature product for predictive holdout stability validation. | phase16_predictive_holdout_stability_summary_proxy_not_acceptance |

## Acceptance Blockers by Gate

| gate_id | blockers |
| --- | --- |
| G01_predictive | 11 |
| G02_economic | 11 |
| G03_robustness | 11 |
| G04_risk | 11 |
| G05_realism | 6 |

## Metric Status

| metric_category | current_status | metrics |
| --- | --- | --- |
| predictive | computed_proxy | 1 |
| predictive | proxy_available | 1 |
| predictive | sample_proxy | 10 |
| trading | computed_proxy | 4 |
| trading | proxy_available | 2 |
| trading | sample_proxy | 11 |

## Gap Priority

| priority | gaps |
| --- | --- |
| P2 | 32 |

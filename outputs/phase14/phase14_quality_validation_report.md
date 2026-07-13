# Phase 14 Synthetic Data Quality Validation Report

Generated UTC: 2026-07-13T21:58:55.281182+00:00

## Scope

This phase validates current synthetic products against structural, marginal, temporal, cross-sectional, conditional, discriminator-proxy and counterfactual checks.
It is a quality gate diagnostic, not strategy acceptance.

## Status Summary

| level | status | checks |
| --- | --- | --- |
| L1_structural | pass | 5 |
| L2_marginal | pass | 4 |
| L3_temporal | pass | 4 |
| L4_cross_sectional | pass | 2 |
| L5_conditional | pass | 4 |
| L6_strategy_neutral_realism | pass | 1 |
| L7_counterfactual | pass | 4 |

## Level 1 Structural

| level | check_name | value | threshold_warn | threshold_fail | status | evidence |
| --- | --- | --- | --- | --- | --- | --- |
| L1_structural | phase6_crossed_l1_rows | 0 | 1 | 1 | pass | Phase 6/DuckDB validation has 0 crossed L1 rows. |
| L1_structural | phase9_negative_spread_rows | 0 | 1 | 1 | pass | Tier C spread_ticks should be non-negative. |
| L1_structural | phase9_nonpositive_mid_price_rows | 0 | 1 | 1 | pass | Tier C mid_price should be positive. |
| L1_structural | phase9_future_label_null_fraction | 0.0133851 | 0.02 | 0.05 | pass | Expected terminal rows per symbol/profile/day have null forward labels. |
| L1_structural | phase6_summary_groups | 170 | 1 | 0 | pass | Phase 6 L2 book summary groups exist. |

## Level 2 Marginal

| level | metric | symbols_compared | median_relative_or_absolute_error | status | evidence | real_5m_bar_symbols |
| --- | --- | --- | --- | --- | --- | --- |
| L2_marginal | spread_ticks_median | 32 | 1.13687e-12 | pass | Real one-day symbol calibration versus current Phase 9 synthetic feature aggregates. | 32 |
| L2_marginal | spread_ticks_q95 | 32 | 1.07371e-12 | pass | Real one-day symbol calibration versus current Phase 9 synthetic feature aggregates. | 32 |
| L2_marginal | nonzero_price_change_fraction | 32 | 0.010954 | pass | Horizon-matched 5-minute real-derived bars versus current Phase 9 5-minute synthetic feature aggregates. | 32 |
| L2_marginal | l5_imbalance_median | 32 | 0.486332 | pass | Real one-day symbol calibration versus current Phase 9 synthetic feature aggregates. | 32 |

## Real-Derived 5-Minute Symbol Marginals

| symbol | real_5m_bars | real_ticks_in_5m_bars | spread_ticks_median | spread_ticks_q95 | nonzero_price_change_fraction | l5_imbalance_median |
| --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | 77 | 13885 | 4 | 7 | 0.974026 | 0.158513 |
| AXISBANK | 77 | 18308 | 2 | 3 | 0.961039 | -0.0524158 |
| BAJAJ-AUTO | 77 | 25140 | 6 | 8 | 0.987013 | 0.00343643 |
| BANKBEES | 76 | 18915 | 20 | 28 | 0.973684 | 0.167612 |
| BHARTIARTL | 77 | 19559 | 3 | 6 | 0.987013 | -0.00562567 |
| BPCL | 77 | 10683 | 1 | 3 | 0.883117 | -0.0525606 |
| BRITANNIA | 77 | 8525 | 4 | 5 | 0.948052 | 0.00571429 |
| CIPLA | 77 | 11663 | 4 | 6 | 0.961039 | 0.413088 |
| DRREDDY | 77 | 12256 | 4 | 5 | 0.974026 | 0.106969 |
| GOLDBEES | 76 | 12980 | 1 | 2 | 0.907895 | -0.157629 |
| HCLTECH | 77 | 29265 | 3 | 4.2 | 0.974026 | -0.18416 |
| HDFCBANK | 77 | 35958 | 2 | 3 | 0.974026 | -0.440181 |
| HINDUNILVR | 77 | 12172 | 4 | 7 | 0.948052 | 0.0517375 |
| ICICIBANK | 77 | 26473 | 2 | 3.2 | 0.948052 | -0.252836 |
| INFY | 77 | 34510 | 2 | 3 | 0.987013 | -0.110118 |
| ITBEES | 76 | 11479 | 1 | 2 | 0.921053 | 0.576055 |
| ITC | 77 | 12378 | 1 | 2 | 0.87013 | 0.329611 |
| JUNIORBEES | 76 | 17440 | 28 | 43.875 | 0.986842 | -0.668286 |
| KOTAKBANK | 77 | 14090 | 2 | 3 | 0.961039 | -0.0830894 |
| LT | 77 | 19465 | 5 | 9.2 | 0.987013 | 0.0146341 |
| M&M | 77 | 25698 | 3 | 7 | 0.974026 | -0.154859 |
| MARUTI | 77 | 27644 | 4 | 5 | 0.961039 | -0.0490956 |
| NESTLEIND | 77 | 12917 | 4 | 6 | 0.961039 | 0.270278 |
| NIFTYBEES | 76 | 22412 | 4 | 8 | 0.921053 | 0.38671 |
| ONGC | 77 | 17304 | 4 | 7 | 0.974026 | 0.03409 |
| RELIANCE | 77 | 26055 | 2 | 3 | 0.948052 | 0.264917 |
| SBIN | 77 | 24727 | 2 | 3 | 0.987013 | 0.0470679 |
| SUNPHARMA | 77 | 14609 | 3 | 6.2 | 0.948052 | -0.160256 |
| TCS | 77 | 36466 | 4 | 5 | 0.974026 | -0.038875 |
| TECHM | 77 | 19123 | 5 | 6 | 0.974026 | -0.0664458 |
| ULTRACEMCO | 77 | 8385 | 3 | 5 | 0.948052 | 0.259832 |
| WIPRO | 77 | 20333 | 4 | 5 | 0.961039 | -0.0593338 |

## Warning Triage

_No rows._

## Holdout Generator Realism Proxy

| quarter_profile | feed_profile | holdout_role | scenario_days | feature_rows | symbols | regimes | market_shock_days | median_spread_ticks | nonzero_mid_return_fraction | structural_ready_for_holdout_proxy | realism_status | acceptance_eligible_now | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-A | disconnect_scenario | development_reference_profile | 63 | 149177 | 32 | 18 | 7 | 4 | 0.967743 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-A | good_retail | development_reference_profile | 63 | 151225 | 32 | 18 | 7 | 4 | 0.965601 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-A | ideal_research | development_reference_profile | 63 | 151200 | 32 | 18 | 7 | 4 | 0.966786 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-A | normal_retail | development_reference_profile | 63 | 151070 | 32 | 18 | 7 | 4 | 0.965374 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-A | stressed_retail | development_reference_profile | 63 | 150394 | 32 | 18 | 7 | 4 | 0.964679 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-B | disconnect_scenario | bullish_high_momentum_holdout_proxy | 63 | 149207 | 32 | 18 | 10 | 4 | 0.968406 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-B | good_retail | bullish_high_momentum_holdout_proxy | 63 | 151175 | 32 | 18 | 10 | 4 | 0.966879 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-B | ideal_research | bullish_high_momentum_holdout_proxy | 63 | 151200 | 32 | 18 | 10 | 4 | 0.967851 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-B | normal_retail | bullish_high_momentum_holdout_proxy | 63 | 151016 | 32 | 18 | 10 | 4 | 0.966626 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-B | stressed_retail | bullish_high_momentum_holdout_proxy | 63 | 150414 | 32 | 18 | 10 | 4 | 0.966227 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-C | disconnect_scenario | stressed_volatile_holdout_proxy | 63 | 149278 | 32 | 18 | 8 | 4 | 0.969754 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-C | good_retail | stressed_volatile_holdout_proxy | 63 | 151181 | 32 | 18 | 8 | 4 | 0.968521 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-C | ideal_research | stressed_volatile_holdout_proxy | 63 | 151200 | 32 | 18 | 8 | 4 | 0.969577 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-C | normal_retail | stressed_volatile_holdout_proxy | 63 | 151040 | 32 | 18 | 8 | 4 | 0.968148 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |
| Q-C | stressed_retail | stressed_volatile_holdout_proxy | 63 | 150451 | 32 | 18 | 8 | 4 | 0.967106 | True | holdout_proxy_available_not_acceptance | False | Holdout generator/feed-profile coverage exists as synthetic proxy evidence, but it is not acceptance-grade until the Phase 14 warning is resolved and strategies are rerun on holdout configs with full event/tick execution and later multi-day real holdout. |

## Caveats

- Real evidence is still a one-day sample.
- Current Phase 6-9 synthetic products are 5-minute state/feature products, not full tick-event simulation.
- Fail/warn labels identify engineering work, not trading conclusions.

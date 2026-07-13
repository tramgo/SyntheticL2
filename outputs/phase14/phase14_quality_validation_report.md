# Phase 14 Synthetic Data Quality Validation Report

Generated UTC: 2026-07-13T21:38:42.511747+00:00

## Scope

This phase validates current synthetic products against structural, marginal, temporal, cross-sectional, conditional, discriminator-proxy and counterfactual checks.
It is a quality gate diagnostic, not strategy acceptance.

## Status Summary

| level | status | checks |
| --- | --- | --- |
| L1_structural | pass | 5 |
| L2_marginal | pass | 3 |
| L2_marginal | warn | 1 |
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

| level | metric | symbols_compared | median_relative_or_absolute_error | status | evidence |
| --- | --- | --- | --- | --- | --- |
| L2_marginal | spread_ticks_median | 32 | 1.13687e-12 | pass | Real one-day symbol calibration versus current Phase 9 synthetic feature aggregates. |
| L2_marginal | spread_ticks_q95 | 32 | 1.07371e-12 | pass | Real one-day symbol calibration versus current Phase 9 synthetic feature aggregates. |
| L2_marginal | nonzero_price_change_fraction | 32 | 1.20472 | warn | Real one-day symbol calibration versus current Phase 9 synthetic feature aggregates. |
| L2_marginal | l5_imbalance_median | 32 | 0.486332 | pass | Real one-day symbol calibration versus current Phase 9 synthetic feature aggregates. |

## Warning Triage

| level | validation_table | metric | status | observed_value | acceptance_impact | root_cause | next_required_evidence | not_acceptance_waiver |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L2_marginal | level2_marginal | nonzero_price_change_fraction | warn | 1.20472 | blocks_realism_gate | Current Phase 9 features are 5-minute synthetic state/features, while the calibration reference is one-day received-tick activity; price-change frequency is therefore not expected to match tick-level nonzero-change frequency without a dedicated event/tick generator or horizon-specific tolerance. | Either add a horizon-matched comparison for 5-minute synthetic features versus 5-minute real-derived features, or introduce a tick/event-level generator that can target received-tick nonzero price-change frequency directly. | True |

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

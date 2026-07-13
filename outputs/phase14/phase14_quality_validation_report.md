# Phase 14 Synthetic Data Quality Validation Report

Generated UTC: 2026-07-13T20:35:16.473029+00:00

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

## Caveats

- Real evidence is still a one-day sample.
- Current Phase 6-9 synthetic products are 5-minute state/feature products, not full tick-event simulation.
- Fail/warn labels identify engineering work, not trading conclusions.

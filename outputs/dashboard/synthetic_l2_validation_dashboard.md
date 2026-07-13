# SyntheticL2 Validation Dashboard Summary

Generated UTC: 2026-07-13T21:49:29.318761+00:00

This dashboard is static research traceability output, not strategy promotion evidence.

## Summary Metrics

| metric | value | note |
| --- | --- | --- |
| quality_checks | 24 | Phase 14 quality rows |
| quality_warn_checks | 1 | Current quality warnings |
| quality_fail_checks | 0 | Current quality failures |
| holdout_proxy_rows | 15 | Phase 14 holdout generator proxy rows |
| holdout_proxy_available_rows | 15 | Holdout proxy rows structurally available |
| full_run_lifecycle_risk_rows | 81 | Phase 12 full-run fill-adjusted risk rows |
| full_run_lifecycle_fill_models | 3 | Phase 12 full-run fill models |
| full_run_lifecycle_daily_halt_rows | 21299578 | Phase 12 full-run lifecycle halt rows |
| strategies | 11 | Phase 15 strategies |
| promoted_strategies | 0 | Promotion allowed count |
| acceptance_blockers | 55 | Phase 15 blocker rows |
| metric_catalog_rows | 28 | Phase 16 metric catalog rows |
| acceptance_grade_metrics | 0 | Acceptance-grade metrics |
| missing_metrics | 0 | Missing metric rows |
| p1_gaps | 0 | Phase 17 P1 backlog rows |

## Quality Status

| status | checks |
| --- | --- |
| pass | 23 |
| warn | 1 |

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

## Acceptance Blockers by Gate

| gate_id | blockers |
| --- | --- |
| G01_predictive | 11 |
| G02_economic | 11 |
| G03_robustness | 11 |
| G04_risk | 11 |
| G05_realism | 11 |

## Metric Status

| metric_category | current_status | metrics |
| --- | --- | --- |
| predictive | computed_proxy | 1 |
| predictive | proxy_available | 1 |
| predictive | sample_proxy | 9 |
| trading | computed_proxy | 4 |
| trading | proxy_available | 2 |
| trading | sample_proxy | 11 |

## Gap Priority

| priority | gaps |
| --- | --- |
| P2 | 32 |

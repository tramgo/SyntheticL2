# Phase447 Catalyst Continuation Stability Holdout Execution

Phase447 executes the Phase446 frozen chronological holdout. It does not tune parameters, drop losing dates, drop symbols, or make a paper/live claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase447_stability_holdout_complete | 1 | Phase447 holdout audit completed |
| phase447_thesis_id | P447_CATALYST_CONTINUATION_STABILITY_HOLDOUT_EXECUTION | Holdout execution thesis |
| phase447_locked_scenario_id | P444_catalyst_continuation_H600_replenishment_after_exhaustion_C5 | Locked scenario audited |
| phase447_holdout_completed_round_trips | 12 | Holdout trades |
| phase447_holdout_trade_dates | 3 | Holdout dates |
| phase447_holdout_symbols | 9 | Holdout symbols |
| phase447_holdout_gross_pnl_inr | 1061.95 | Holdout gross P&L |
| phase447_holdout_cost200_inr | 1974.42 | Holdout Zerodha cost200 |
| phase447_holdout_net_pnl_inr | -912.466 | Holdout net P&L after cost200 |
| phase447_holdout_annualized_return_pct | -7.66471 | Holdout annualized return with fixed INR 1,000,000 capital |
| phase447_holdout_positive_date_fraction | 0.333333 | Holdout positive-date fraction |
| phase447_acceptance_survivor | 0 | Accepted only if every hard holdout gate passes |
| phase447_strategy_promotion_allowed | 0 | No paper/live/deployable promotion in Phase447 |
| phase447_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase447_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase447_hard_gate_pass_rows | 7 | Passed hard gates |
| phase447_hard_gate_rows | 10 | Hard gates |
| phase447_next_best_action | reject_catalyst_continuation_stability_or_precommit_new_source_edge | Recommended next action |

## Split Summary

| split | completed_round_trips | trade_dates | symbols | positive_date_fraction | gross_pnl_inr | cost200_inr | net_pnl_inr | annualized_return_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| development | 34 | 8 | 15 | 0.375 | 8326.12 | 5609.09 | 2717.03 | 8.55865 |
| holdout | 12 | 3 | 9 | 0.333333 | 1061.95 | 1974.42 | -912.466 | -7.66471 |
| all_locked | 46 | 11 | 20 | 0.363636 | 9388.07 | 7583.5 | 1804.57 | 4.1341 |

## Date P&L

| diagnostic_trade_date | split | completed_round_trips | symbols | gross_pnl_inr | cost200_inr | net_pnl_inr |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07-10 | development | 2 | 2 | -73.83 | 330.683 | -404.513 |
| 2026-07-13 | development | 2 | 2 | -429.65 | 330.529 | -760.179 |
| 2026-07-14 | development | 5 | 2 | 3155.9 | 826.079 | 2329.82 |
| 2026-07-15 | development | 5 | 5 | 2941.9 | 820.433 | 2121.47 |
| 2026-07-16 | development | 5 | 4 | -35.9 | 826.447 | -862.347 |
| 2026-07-20 | development | 5 | 2 | -21.6 | 825.67 | -847.27 |
| 2026-07-21 | development | 5 | 3 | 2324.5 | 823.132 | 1501.37 |
| 2026-07-22 | development | 5 | 4 | 464.8 | 826.116 | -361.316 |
| 2026-07-23 | holdout | 4 | 4 | 1789.5 | 658.319 | 1131.18 |
| 2026-07-24 | holdout | 5 | 4 | 131.3 | 823.222 | -691.922 |
| 2026-07-27 | holdout | 3 | 3 | -858.85 | 492.874 | -1351.72 |

## Symbol P&L

| split | symbol | completed_round_trips | trade_dates | gross_pnl_inr | cost200_inr | net_pnl_inr |
| --- | --- | --- | --- | --- | --- | --- |
| development | HCLTECH | 5 | 3 | 3865.2 | 826.17 | 3039.03 |
| development | M&M | 5 | 2 | 2204.8 | 826.237 | 1378.56 |
| development | CIPLA | 1 | 1 | 1069.5 | 165.19 | 904.31 |
| development | AXISBANK | 1 | 1 | 808 | 165.235 | 642.765 |
| development | BHARTIARTL | 2 | 1 | 622.2 | 330.07 | 292.13 |
| development | HINDUNILVR | 1 | 1 | 267.9 | 165.256 | 102.644 |
| development | MARUTI | 2 | 2 | 420 | 324.538 | 95.4616 |
| development | ICICIBANK | 2 | 1 | 367.2 | 330.128 | 37.0717 |
| development | ULTRACEMCO | 1 | 1 | 152 | 162.223 | -10.2234 |
| development | SBIN | 1 | 1 | 19.4 | 165.325 | -145.925 |
| development | ONGC | 1 | 1 | -192.23 | 165.335 | -357.565 |
| development | HDFCBANK | 2 | 2 | -290.2 | 330.421 | -620.621 |
| development | WIPRO | 5 | 4 | 128.55 | 826.756 | -698.206 |
| development | INFY | 2 | 2 | -472.4 | 330.602 | -803.002 |
| development | RELIANCE | 3 | 1 | -643.8 | 495.599 | -1139.4 |
| holdout | BPCL | 1 | 1 | 1895.4 | 165.471 | 1729.93 |
| holdout | LT | 1 | 1 | 275.6 | 162.804 | 112.796 |
| holdout | HCLTECH | 2 | 2 | 380.4 | 330.501 | 49.8992 |
| holdout | TCS | 1 | 1 | 13.5 | 165.132 | -151.632 |
| holdout | KOTAKBANK | 1 | 1 | -141.35 | 165.279 | -306.629 |
| holdout | ICICIBANK | 2 | 1 | -82.8 | 330.121 | -412.921 |
| holdout | ULTRACEMCO | 2 | 2 | -224 | 324.679 | -548.679 |
| holdout | CIPLA | 1 | 1 | -393.3 | 165.126 | -558.426 |
| holdout | TECHM | 1 | 1 | -661.5 | 165.304 | -826.804 |

## Phase444 Control Context

| control | net_pnl_inr | annualized_return_pct | positive_date_fraction | note |
| --- | --- | --- | --- | --- |
| l1_only | -1424.44 | -2.99133 | 0.25 | L1-only ablation context; not used for holdout selection. |
| reversal | -19338.8 | -44.3035 | 0.0909091 | Opposite-direction control context; not used for holdout selection. |
| time_shifted_catalyst | 1959.08 | 3.7976 | 0.615385 | Temporal catalyst-shift control context; not used for holdout selection. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P447_PHASE446_PRECOMMIT_AVAILABLE | True | phase446_stability_precommit_complete | 1 | hard |
| P447_LOCKED_SCENARIO_ONLY | True | P444_catalyst_continuation_H600_replenishment_after_exhaustion_C5 | P444_catalyst_continuation_H600_replenishment_after_exhaustion_C5 | hard |
| P447_FROZEN_HOLDOUT_DATES_MATCH | True | 2026-07-23;2026-07-24;2026-07-27 | 2026-07-23;2026-07-24;2026-07-27 | hard |
| P447_NO_PARAMETER_TUNING | True | Phase447 reads Phase446 locked contract and filters only locked scenario/date split. | no tuning | hard |
| P447_HOLDOUT_TRADES_PRESENT | True | 12 | >0 | hard |
| P447_HOLDOUT_NET_PNL_POSITIVE | False | -912.466 | >0.0 | hard |
| P447_HOLDOUT_ANNUALIZED_GE_12 | False | -7.66471 | >=12.0 | hard |
| P447_HOLDOUT_POSITIVE_DATE_FRACTION_GE_0_60 | False | 0.333333 | >=0.6 | hard |
| P447_COST200_FIXED_CAPITAL | True | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | cost200_fixed_1000000_capital | hard |
| P447_NO_PROMOTION_PAPER_LIVE | True | execution-only stability audit | closed | hard |

Verdict: the locked Phase444 diagnostic is accepted only if all hard Phase447 gates pass. Otherwise it remains a useful clue, not a tradable/stable strategy.

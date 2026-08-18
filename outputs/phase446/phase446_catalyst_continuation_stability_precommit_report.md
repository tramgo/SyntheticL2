# Phase446 Catalyst Continuation Stability Holdout Precommit

Phase446 freezes a no-tuning chronological stability audit for the positive Phase444 diagnostic.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase446_stability_precommit_complete | 1 | Phase446 precommit completed |
| phase446_thesis_id | P446_CATALYST_CONTINUATION_STABILITY_HOLDOUT_PRECOMMIT | Frozen thesis |
| phase446_locked_scenario_id | P444_catalyst_continuation_H600_replenishment_after_exhaustion_C5 | Locked candidate |
| phase446_holdout_dates | 2026-07-23;2026-07-24;2026-07-27 | Frozen holdout dates |
| phase446_execution_results_generated | 0 | Precommit only |
| phase446_strategy_promotion_allowed | 0 | No promotion |
| phase446_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase446_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase446_execution_allowed_next | 1 | Whether Phase447 may execute |
| phase446_hard_gate_pass_rows | 9 | Passed hard gates |
| phase446_hard_gate_rows | 9 | Hard gates |
| phase446_next_best_action | run_phase447_catalyst_continuation_stability_holdout_no_paper_live | Recommended next action |

## Evidence Registry

| evidence_id | value | description |
| --- | --- | --- |
| phase445_next_action | precommit_catalyst_continuation_stability_repair_or_add_real_holdout | Phase445 requires stability repair or real holdout. |
| phase445_best_net_pnl_inr | 1804.5673675401536 | Positive diagnostic net P&L. |
| phase445_best_annualized_pct | 4.134099787455624 | Positive diagnostic annualized return. |
| locked_trade_rows | 46 | Locked scenario trade rows. |
| locked_dates | 11 | Locked scenario dates. |
| locked_positive_dates | 4 | Positive date count before holdout audit. |

## Frozen Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P446_CATALYST_CONTINUATION_STABILITY_HOLDOUT_PRECOMMIT | Stability/holdout precommit after Phase445 positive diagnostic. |
| locked_scenario_id | P444_catalyst_continuation_H600_replenishment_after_exhaustion_C5 | No parameter tuning from Phase444. |
| split_policy | chronological_last_third_dates_as_holdout_min_3_dates | Holdout split frozen before Phase447. |
| holdout_dates | 2026-07-23;2026-07-24;2026-07-27 | Frozen holdout dates. |
| development_dates | 2026-07-10;2026-07-13;2026-07-14;2026-07-15;2026-07-16;2026-07-20;2026-07-21;2026-07-22 | Frozen development dates. |
| acceptance_floor | holdout_net_pnl_gt_0.0;holdout_annualized_ge_12.0;holdout_positive_date_fraction_ge_0.6 | Holdout stability requirements. |
| controls_required | locked_scenario_only;no_new_filters;date_pnl_concentration;symbol_pnl_concentration;time_shift_context | No same-result tuning. |
| capital_policy | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | Annualized denominator fixed. |
| forbidden | new_thresholds;drop_bad_dates;drop_bad_symbols;promotion;paper_live;deployable_profitability_claim | Closed boundaries. |
| execution_results_generated_now | 0 | Precommit only. |

## Frozen Date Split

| diagnostic_trade_date | split |
| --- | --- |
| 2026-07-10 | development |
| 2026-07-13 | development |
| 2026-07-14 | development |
| 2026-07-15 | development |
| 2026-07-16 | development |
| 2026-07-20 | development |
| 2026-07-21 | development |
| 2026-07-22 | development |
| 2026-07-23 | holdout |
| 2026-07-24 | holdout |
| 2026-07-27 | holdout |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P446_PHASE445_AVAILABLE | True | 1 | 1 | hard |
| P446_PHASE445_NEXT_ACTION_MATCHED | True | precommit_catalyst_continuation_stability_repair_or_add_real_holdout | stability_or_holdout | hard |
| P446_POSITIVE_DIAGNOSTIC_PRESENT | True | 1804.5673675401536 | >0 | hard |
| P446_LOCKED_SCENARIO_PRESENT | True | 46 | >0 | hard |
| P446_NO_PARAMETER_TUNING | True | P444_catalyst_continuation_H600_replenishment_after_exhaustion_C5 | locked | hard |
| P446_HOLDOUT_SPLIT_FROZEN | True | 3 | >=3 | hard |
| P446_COST200_FIXED_CAPITAL_PINNED | True | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | cost200_fixed_capital | hard |
| P446_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P446_BOUNDARIES_CLOSED | True | new_thresholds;drop_bad_dates;drop_bad_symbols;promotion;paper_live;deployable_profitability_claim | closed | hard |

Boundary: Phase447 may audit the locked scenario only. It may not drop bad dates, drop symbols, add thresholds, or open promotion/paper/live.

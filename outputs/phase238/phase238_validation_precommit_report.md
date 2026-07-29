# Phase238 Validation Precommit Report

Generated UTC: 2026-07-29T07:07:43.074251+00:00

Phase238 freezes the Phase237 candidate and precommits validation rules.
It does not validate on the same real-anchor sample used for Phase237 threshold-transfer discovery.
The primary validation route requires unseen real L2 dates; the current local sample supports only diagnostic walk-forward checks.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase238_validation_precommit_complete | 1 | Phase238 validation precommit completed |
| phase238_candidate_id | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | Frozen Phase237 candidate |
| phase238_phase237_net_pnl_inr | 7041.52 | Phase237 discovery net P&L |
| phase238_phase237_trade_rows | 71 | Phase237 discovery trade count |
| phase238_phase237_dates | 6 | Phase237 discovery date count |
| phase238_phase237_symbols | 21 | Phase237 discovery symbol count |
| phase238_primary_validation_contract_rows | 1 | Primary unseen-validation contracts |
| phase238_walk_forward_diagnostic_contract_rows | 1 | Diagnostic fallback contracts |
| phase238_local_unseen_validation_dates_available | 0 | Whether enough local unseen validation dates exist now |
| phase238_min_unseen_validation_dates_required | 5 | Minimum unseen dates required |
| phase238_phase239_work_order_rows | 4 | Phase239 work-order rows |
| phase238_hard_gate_pass_rows | 5 | Hard Phase238 gates passed |
| phase238_hard_gate_rows | 5 | Hard Phase238 gates evaluated |
| phase238_strategy_promotion_allowed | 0 | No strategy promotion from Phase238 |
| phase238_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase238 |
| phase238_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase238 |
| phase238_next_best_action | run_phase239_acquire_or_materialize_unseen_real_anchor_validation_dates_no_paper_live | Recommended next milestone |

## Frozen Candidate

| candidate_id | family_id | signal_source | direction | horizon_event_bars | event_quantile | signal_quantile | event_window_score_threshold | signal_abs_threshold | source_event_bar_adapter | cost_model_version | phase237_net_pnl_inr | phase237_trades | phase237_dates | phase237_symbols | frozen_for_phase238 | parameter_tuning_allowed_in_phase238 | paper_or_live_acceptance_allowed | deployable_profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | bar_return_reversal | bar_return | reversal | 6 | 0.95 | 0.95 | 8.3341 | 0.00564863 | phase235_real_anchor_event_bar_adapter | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | 7041.52 | 71 | 6 | 21 | 1 | 0 | 0 | 0 |

## Validation Data Availability

| availability_check | passed | observed_value | required_value | interpretation |
| --- | --- | --- | --- | --- |
| P238_PHASE235_REAL_EVENT_BARS_AVAILABLE | True | 7 | >0 local real event-bar dates | Local real event bars are available for diagnostics and split accounting. |
| P238_PHASE237_CANDIDATE_FROZEN | True | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | frozen candidate id | Phase238 may not tune thresholds or candidate selection. |
| P238_CURRENT_LOCAL_DATES_DISCOVERY_CONTAMINATED | True | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14;2026-07-15;2026-07-16 | all Phase235 dates treated as Phase237 discovery data | Because real quantile thresholds were selected on Phase235 bars, current dates cannot prove unseen acceptance. |
| P238_TRULY_UNSEEN_LOCAL_DATES_AVAILABLE | False | 0 | >=5 dates not used by Phase237 discovery | No currently materialized local Phase235 dates qualify as truly unseen validation dates. |
| P238_PHASE237_DISCOVERY_TRADE_DATES | True | 2026-07-09;2026-07-10;2026-07-13;2026-07-14;2026-07-15;2026-07-16 | best candidate trade dates recorded | Trade-date breadth is known for the discovery result. |

## Validation Contract

| contract_id | validation_type | input_data | candidate_id | parameter_tuning_allowed | minimum_dates | minimum_symbols | minimum_trades | required_controls | acceptance_rule | result_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P238_UNSEEN_REAL_ANCHOR_PRIMARY | acceptance_candidate_validation | future downloaded real Zerodha-websocket-like L2 dates not used by Phase237 | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | 0 | 5 | 20 | 50 | side_flip;random_side_1000;cost_150;cost_200;date_symbol_concentration | net_pnl_after_costs_positive AND >=3/4 controls pass AND date/symbol/trade breadth met | validation_candidate_only_no_paper_live |
| P238_WALK_FORWARD_DIAGNOSTIC_FALLBACK | non_acceptance_diagnostic | existing Phase235 real event bars split by date order | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | 0 | 6 | 21 | 71 | rolling_prefix_date_freeze;leave_one_date;cost_stress | diagnostic_only_not_promotional_even_if_positive | diagnostic_only |

## Phase239 Work Order

| step_order | phase239_task | candidate_id | detail | evidence |
| --- | --- | --- | --- | --- |
| 1 | acquire_or_materialize_unseen_real_l2_dates | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | Download/materialize at least 5 real L2 dates not present in Phase235/Phase237 discovery outputs. | date inventory proving new dates are outside Phase237 discovery sample |
| 2 | rebuild_phase235_event_bar_adapter_for_unseen_dates | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | Use identical Phase235 event-bar adapter; no threshold recalibration on validation dates. | unseen real event-bar coverage summary |
| 3 | replay_frozen_phase237_candidate | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | Apply frozen Phase237 event threshold, signal threshold, horizon, side rule and Zerodha cost model. | unseen validation trade ledger and summary |
| 4 | controls_and_decision | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | Run side-flip, random-side, cost stress and concentration controls; decide validate, redesign or close. | Phase239 gate evaluation and no paper/live promotion boundary |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P238_PHASE237_CANDIDATE_OPENED | True | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | frozen Phase237 candidate | hard |
| P238_PRIMARY_UNSEEN_CONTRACT_WRITTEN | True | 1 | 1 | hard |
| P238_DIAGNOSTIC_FALLBACK_CONTRACT_WRITTEN | True | 1 | 1 | hard |
| P238_LOCAL_UNSEEN_ACCEPTANCE_DATA_AVAILABLE_NOW | False | 0 | 1 | soft |
| P238_PHASE239_WORK_ORDER_REQUIRED | True | 1 | 1 | hard |
| P238_NO_PAPER_LIVE_OR_PROMOTION_UNLOCK | True | 0 | 0 | hard |

# Phase92 Low-Turnover Event-Window Precommit

Generated UTC: 2026-07-19T21:17:45.115357+00:00

Phase92 precommits a lower-turnover event-window feature class after Phase91 falsified simple cross-symbol imbalance.
It computes feature-only thresholds from train months and locks replay gates before Phase93 inspects next-bar outcomes.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase92_event_feature_rows | 160150 | Event-window design rows built from Phase83 cached bars |
| phase92_train_rows | 81818 | Train rows used for feature thresholds |
| phase92_test_rows | 78332 | Locked test rows reserved for Phase93 replay |
| phase92_signal_family_rows | 3 | Low-turnover event-window families precommitted |
| phase92_candidate_spec_rows | 12 | Candidate specs precommitted |
| phase92_validation_gate_rows | 6 | Validation gates locked |
| phase92_phase91_cross_symbol_pass | 0 | Phase91 pass flag used only as pivot context |
| phase92_ready_for_replay | 1 | 1 means Phase93 low-turnover event replay may run |
| phase92_recommend_next_action | run_precommitted_low_turnover_event_window_replay | Recommended next milestone |

## Feature Diagnostics

| feature | train_rows | train_p50 | train_p90 | train_p95 | train_p975 |
| --- | --- | --- | --- | --- | --- |
| event_window_score | 81818 | 16.2999 | 54.3162 | 72.3652 | 89.9766 |
| abs_bar_return_bps | 81818 | 37.5352 | 124.334 | 166.608 | 215.813 |
| book_dislocation_score | 81818 | 0.627716 | 2.03652 | 2.63561 | 2.88012 |
| taker_round_trip_cost_floor_bps | 81818 | 10.9053 | 13.1523 | 13.863 | 14.5773 |

## Precommitted Signal Families

| family_id | hypothesis | direction_rule | required_filters | target_holding_period | turnover_intent | why_not_posthoc |
| --- | --- | --- | --- | --- | --- | --- |
| P92_SHOCK_EXHAUSTION_REVERSAL | Large shock/event-window bars may overextend and reverse after immediate liquidity exhaustion. | side = -sign(bar_return) | shock_bar AND abs_bar_return_bps threshold AND event_window_score threshold AND cost_floor threshold | next_source_event_bar | low_turnover_event_only | Shock exhaustion is precommitted after Phase91 failure and before Phase93 replay. |
| P92_SHOCK_CONTINUATION | Some high-intensity shock bars may continue when the event-window score is extreme enough to clear retail costs. | side = sign(bar_return) | shock_bar AND abs_bar_return_bps threshold AND event_window_score threshold AND cost_floor threshold | next_source_event_bar | low_turnover_event_only | Continuation is locked as the competing hypothesis, not chosen after inspecting replay P&L. |
| P92_BOOK_DISLOCATION_REVERSAL | Extreme book dislocation with large current move may revert when displayed L1/L5 pressure is stretched. | side = -sign(bar_return) | book_dislocation_score threshold AND abs_bar_return_bps threshold AND event_window_score threshold AND cost_floor threshold | next_source_event_bar | low_turnover_event_only | Book-dislocation threshold is feature-only and train-period calibrated before replay. |

## Candidate Specs

| candidate_id | family_id | direction_rule | requires_shock_bar | event_window_score_quantile | event_window_score_threshold | abs_bar_return_bps_quantile | abs_bar_return_bps_threshold | book_dislocation_score_quantile | book_dislocation_score_threshold | max_taker_round_trip_cost_floor_bps | train_months | test_months |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | side = -sign(bar_return) | True | 0.95 | 72.3652 | 0.95 | 166.608 | 0 | 0 | 10.9053 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_95_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | side = -sign(bar_return) | True | 0.95 | 72.3652 | 0.975 | 215.813 | 0 | 0 | 10.9053 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_95 | P92_SHOCK_EXHAUSTION_REVERSAL | side = -sign(bar_return) | True | 0.975 | 89.9766 | 0.95 | 166.608 | 0 | 0 | 10.9053 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P92_SHOCK_EXHAUSTION_REVERSAL_E0_975_M0_975 | P92_SHOCK_EXHAUSTION_REVERSAL | side = -sign(bar_return) | True | 0.975 | 89.9766 | 0.975 | 215.813 | 0 | 0 | 10.9053 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P92_SHOCK_CONTINUATION_E0_95_M0_95 | P92_SHOCK_CONTINUATION | side = sign(bar_return) | True | 0.95 | 72.3652 | 0.95 | 166.608 | 0 | 0 | 10.9053 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P92_SHOCK_CONTINUATION_E0_95_M0_975 | P92_SHOCK_CONTINUATION | side = sign(bar_return) | True | 0.95 | 72.3652 | 0.975 | 215.813 | 0 | 0 | 10.9053 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P92_SHOCK_CONTINUATION_E0_975_M0_95 | P92_SHOCK_CONTINUATION | side = sign(bar_return) | True | 0.975 | 89.9766 | 0.95 | 166.608 | 0 | 0 | 10.9053 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P92_SHOCK_CONTINUATION_E0_975_M0_975 | P92_SHOCK_CONTINUATION | side = sign(bar_return) | True | 0.975 | 89.9766 | 0.975 | 215.813 | 0 | 0 | 10.9053 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P92_BOOK_DISLOCATION_REVERSAL_E0_95_M0_95 | P92_BOOK_DISLOCATION_REVERSAL | side = -sign(bar_return) | False | 0.95 | 72.3652 | 0.95 | 166.608 | 0.95 | 2.63561 | 10.9053 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P92_BOOK_DISLOCATION_REVERSAL_E0_95_M0_975 | P92_BOOK_DISLOCATION_REVERSAL | side = -sign(bar_return) | False | 0.95 | 72.3652 | 0.975 | 215.813 | 0.95 | 2.63561 | 10.9053 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P92_BOOK_DISLOCATION_REVERSAL_E0_975_M0_95 | P92_BOOK_DISLOCATION_REVERSAL | side = -sign(bar_return) | False | 0.975 | 89.9766 | 0.95 | 166.608 | 0.95 | 2.63561 | 10.9053 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P92_BOOK_DISLOCATION_REVERSAL_E0_975_M0_975 | P92_BOOK_DISLOCATION_REVERSAL | side = -sign(bar_return) | False | 0.975 | 89.9766 | 0.975 | 215.813 | 0.95 | 2.63561 | 10.9053 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |

## Validation Gates

| gate_id | requirement | pass_threshold |
| --- | --- | --- |
| P92_NO_LABEL_INSPECTION | Phase92 may compute event-window features and train thresholds only; no directional P&L or next_bar_return replay is evaluated. | No candidate selected using replay P&L. |
| P92_LOW_TURNOVER | Replay must be low turnover: 50 to 1500 trades per split, at least 10 symbols, and no daily burst over 10% of split trades. | 50<=trades<=1500; symbols>=10; max_day_trade_fraction<=0.10 |
| P92_COST_FLOOR | Only rows below the train p50 taker round-trip cost floor may trade, and gross edge must clear at least 1.5x realized cost drag on test. | cost_floor_filter=1; test_abs_gross_to_cost_drag_ratio>=1.5 |
| P92_AFTER_COST_SURVIVAL | After-cost net P&L must be positive in train and test with precision_cost_clear >= 0.56. | train_net>0; test_net>0; train_precision>=0.56; test_precision>=0.56 |
| P92_MONTH_AND_SYMBOL_BREADTH | At least 4 test months positive; no single month or symbol may contribute more than 40% of absolute test net P&L. | test_positive_months>=4; max_month_contribution_abs<=0.40; max_symbol_contribution_abs<=0.40 |
| P92_RETIREMENT | If no low-turnover event-window candidate passes, stop strategy mining and return to generator realism/calibration audit. | No threshold widening in Phase93. |

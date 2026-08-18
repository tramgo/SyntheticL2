# Phase430 Timing-Geometry Audit

Phase430 audits whether exact forward-tick exits, elapsed-time holds and max-hold tick windows are feasible on synthetic and real L2 cadence.

This phase does not tune strategy signals and does not generate promotion/paper/live claims.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase430_timing_geometry_audit_complete | 1 | Phase430 audit completed |
| phase430_audit_id | P430_TIMING_GEOMETRY_AUDIT | Audit id |
| phase430_synthetic_groups | 16 | Synthetic symbol/date groups |
| phase430_real_anchor_groups | 40 | Real-anchor symbol/date groups |
| phase430_synthetic_median_gap_median | 1 | Median of synthetic group median gaps |
| phase430_real_anchor_median_gap_median | 1 | Median of real-anchor group median gaps |
| phase430_phase428_max_hold_60_feasible_fraction | 0 | Best synthetic feasibility at 60 max-hold ticks |
| phase430_recommended_geometry_rows | 2 | Recommended geometry rows |
| phase430_timing_repair_precommit_allowed | 1 | Whether Phase431 may precommit repaired geometry |
| phase430_strategy_promotion_allowed | 0 | No promotion |
| phase430_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase430_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase430_hard_gate_pass_rows | 8 | Passed hard gates |
| phase430_hard_gate_rows | 8 | Hard gates |
| phase430_next_best_action | precommit_phase431_geometry_consistent_full_depth_sweep | Recommended next action |

## Cadence Summary

| panel | trade_date | symbol | ticks | positive_gaps | zero_or_negative_gaps | median_gap | p90_gap | p95_gap | p99_gap | max_gap | unit_guess |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic | 2026-01-01 | ADANIPORTS | 25000 | 4983 | 20016 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-01-01 | AXISBANK | 25000 | 5483 | 19516 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-01-01 | BAJAJ-AUTO | 25000 | 5983 | 19016 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-01-01 | BANKBEES | 25000 | 5483 | 19516 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-01-01 | BHARTIARTL | 25000 | 5483 | 19516 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-01-01 | BPCL | 25000 | 5483 | 19516 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-01-01 | BRITANNIA | 25000 | 5983 | 19016 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-01-01 | CIPLA | 25000 | 5483 | 19516 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-02-02 | ADANIPORTS | 25000 | 5983 | 19016 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-02-02 | AXISBANK | 25000 | 5983 | 19016 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-02-02 | BAJAJ-AUTO | 25000 | 6483 | 18516 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-02-02 | BANKBEES | 25000 | 5983 | 19016 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-02-02 | BHARTIARTL | 25000 | 5483 | 19516 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-02-02 | BPCL | 25000 | 4983 | 20016 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-02-02 | BRITANNIA | 25000 | 5983 | 19016 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| synthetic | 2026-02-02 | CIPLA | 25000 | 4983 | 20016 | 1 | 1 | 1 | 1 | 1 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-17 | ADANIPORTS | 761 | 575 | 185 | 1 | 5 | 7 | 8 | 417 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-17 | AXISBANK | 801 | 588 | 212 | 1 | 5.3 | 7 | 8 | 425 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-17 | BAJAJ-AUTO | 1406 | 917 | 488 | 1 | 1 | 2 | 7 | 425 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-17 | BANKBEES | 404 | 359 | 44 | 1 | 8 | 8 | 9 | 1.78426e+09 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-17 | BHARTIARTL | 763 | 562 | 200 | 1 | 5 | 7 | 8 | 426 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-17 | BPCL | 269 | 252 | 16 | 5 | 7 | 8 | 9 | 425 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-17 | BRITANNIA | 230 | 215 | 14 | 6 | 8 | 8 | 9 | 417 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-17 | CIPLA | 332 | 290 | 41 | 3 | 7 | 8 | 9 | 417 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-20 | ADANIPORTS | 346 | 317 | 28 | 4 | 7 | 7 | 8 | 434 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-20 | AXISBANK | 1792 | 1130 | 661 | 1 | 1 | 1 | 1 | 448 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-20 | BAJAJ-AUTO | 731 | 586 | 144 | 1 | 5 | 6.75 | 8 | 434 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-20 | BANKBEES | 1493 | 1071 | 421 | 1 | 1 | 1 | 2 | 1.78452e+09 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-20 | BHARTIARTL | 816 | 586 | 229 | 1 | 5 | 6 | 7.15 | 446 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-20 | BPCL | 327 | 298 | 28 | 4 | 7 | 8 | 8.03 | 449 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-20 | BRITANNIA | 266 | 255 | 10 | 4 | 7.6 | 8 | 9 | 449 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-20 | CIPLA | 433 | 362 | 70 | 3 | 7 | 7 | 9 | 449 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-21 | ADANIPORTS | 494 | 407 | 86 | 1 | 6 | 7 | 9 | 423 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-21 | AXISBANK | 1654 | 1019 | 634 | 1 | 1 | 1 | 4 | 422 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-21 | BAJAJ-AUTO | 1253 | 938 | 314 | 1 | 1 | 2 | 5 | 423 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-21 | BANKBEES | 975 | 815 | 159 | 1 | 2 | 4 | 7 | 1.78461e+09 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-21 | BHARTIARTL | 578 | 462 | 115 | 1 | 5 | 6 | 7.39 | 422 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-21 | BPCL | 293 | 274 | 18 | 4 | 7 | 8 | 9 | 410 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-21 | BRITANNIA | 332 | 310 | 21 | 3 | 8 | 8 | 8.91 | 423 | milliseconds_or_dense_subtick_counter |
| real_anchor | 2026-07-21 | CIPLA | 338 | 311 | 26 | 3 | 7 | 8 | 9 | 410 | milliseconds_or_dense_subtick_counter |

## Hold-Window Feasibility

| panel | forward_ticks | max_hold_ticks | scan_points_possible | scan_points_feasible_min_hold | median_max_window_hold | p95_max_window_hold | feasible_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| real_anchor | 3 | 30 | 133 | 0 | 68.25 | 112.325 | 0 |
| real_anchor | 3 | 60 | 126 | 11 | 112 | 201.55 | 0.0873016 |
| real_anchor | 3 | 120 | 116 | 24 | 190.5 | 289.125 | 0.206897 |
| real_anchor | 3 | 250 | 100 | 44 | 420.25 | 568.9 | 0.44 |
| real_anchor | 3 | 500 | 62 | 62 | 318.25 | 337.4 | 1 |
| real_anchor | 3 | 1000 | 23 | 23 | 0 | 0 | 1 |
| real_anchor | 3 | 1500 | 6 | 6 | 0 | 0 | 1 |
| real_anchor | 3 | 2500 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | 3 | 5000 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | 6 | 30 | 133 | 0 | 68.25 | 112.325 | 0 |
| real_anchor | 6 | 60 | 125 | 11 | 112 | 201.55 | 0.088 |
| real_anchor | 6 | 120 | 116 | 24 | 190.5 | 289.125 | 0.206897 |
| real_anchor | 6 | 250 | 100 | 44 | 420.25 | 568.9 | 0.44 |
| real_anchor | 6 | 500 | 62 | 62 | 318.25 | 337.4 | 1 |
| real_anchor | 6 | 1000 | 23 | 23 | 0 | 0 | 1 |
| real_anchor | 6 | 1500 | 6 | 6 | 0 | 0 | 1 |
| real_anchor | 6 | 2500 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | 6 | 5000 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | 12 | 30 | 131 | 0 | 68.25 | 112.325 | 0 |
| real_anchor | 12 | 60 | 125 | 11 | 112 | 201.55 | 0.088 |
| real_anchor | 12 | 120 | 116 | 24 | 190.5 | 289.125 | 0.206897 |
| real_anchor | 12 | 250 | 97 | 42 | 420.25 | 530 | 0.43299 |
| real_anchor | 12 | 500 | 59 | 59 | 318.25 | 337.6 | 1 |
| real_anchor | 12 | 1000 | 22 | 22 | 0 | 0 | 1 |
| real_anchor | 12 | 1500 | 5 | 5 | 0 | 0 | 1 |
| real_anchor | 12 | 2500 | 0 | 0 | 0 | 0 | 0 |
| real_anchor | 12 | 5000 | 0 | 0 | 0 | 0 | 0 |
| synthetic | 3 | 30 | 1600 | 0 | 5 | 15 | 0 |
| synthetic | 3 | 60 | 1600 | 0 | 10 | 30 | 0 |
| synthetic | 3 | 120 | 1600 | 0 | 20 | 60 | 0 |
| synthetic | 3 | 250 | 1584 | 17 | 42 | 112.4 | 0.0107323 |
| synthetic | 3 | 500 | 1568 | 74 | 84 | 210.925 | 0.0471939 |
| synthetic | 3 | 1000 | 1536 | 313 | 169.75 | 358.375 | 0.203776 |
| synthetic | 3 | 1500 | 1504 | 1140 | 254.5 | 501.925 | 0.757979 |
| synthetic | 3 | 2500 | 1440 | 1440 | 424.5 | 756.85 | 1 |
| synthetic | 3 | 5000 | 1280 | 1280 | 841.75 | 1232.22 | 1 |
| synthetic | 6 | 30 | 1600 | 0 | 5 | 15 | 0 |
| synthetic | 6 | 60 | 1600 | 0 | 10 | 30 | 0 |
| synthetic | 6 | 120 | 1600 | 0 | 20 | 60 | 0 |
| synthetic | 6 | 250 | 1584 | 17 | 42 | 112.4 | 0.0107323 |
| synthetic | 6 | 500 | 1568 | 74 | 84 | 210.925 | 0.0471939 |
| synthetic | 6 | 1000 | 1536 | 313 | 169.75 | 358.375 | 0.203776 |
| synthetic | 6 | 1500 | 1504 | 1140 | 254.5 | 501.925 | 0.757979 |
| synthetic | 6 | 2500 | 1440 | 1440 | 424.5 | 756.85 | 1 |
| synthetic | 6 | 5000 | 1280 | 1280 | 841.75 | 1232.22 | 1 |
| synthetic | 12 | 30 | 1600 | 0 | 5 | 15 | 0 |
| synthetic | 12 | 60 | 1600 | 0 | 10 | 30 | 0 |
| synthetic | 12 | 120 | 1600 | 0 | 20 | 60 | 0 |
| synthetic | 12 | 250 | 1584 | 17 | 42 | 112.4 | 0.0107323 |
| synthetic | 12 | 500 | 1568 | 74 | 84 | 210.925 | 0.0471939 |
| synthetic | 12 | 1000 | 1536 | 313 | 169.75 | 358.375 | 0.203776 |
| synthetic | 12 | 1500 | 1504 | 1140 | 254.5 | 501.925 | 0.757979 |
| synthetic | 12 | 2500 | 1440 | 1440 | 424.5 | 756.85 | 1 |
| synthetic | 12 | 5000 | 1280 | 1280 | 841.75 | 1232.22 | 1 |

## Recommended Timing Geometry

| panel | recommended_forward_ticks | recommended_max_hold_ticks | feasible_fraction | recommendation |
| --- | --- | --- | --- | --- |
| real_anchor | 3 | 500 | 1 | geometry_feasible_for_precommit |
| synthetic | 3 | 2500 | 1 | geometry_feasible_for_precommit |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P430_PHASE429_REQUIRED_AUDIT | True | 1 | 1 | hard |
| P430_SYNTHETIC_CADENCE_MEASURED | True | True | True | hard |
| P430_REAL_ANCHOR_CADENCE_MEASURED | True | True | True | hard |
| P430_TIMESTAMP_UNIT_GUESSED | True | milliseconds_or_dense_subtick_counter | nonempty | hard |
| P430_PHASE428_GEOMETRY_DIAGNOSED | True | 0 | 0 | hard |
| P430_FEASIBLE_REPAIR_GEOMETRY_FOUND | True | 2 | >=1 | hard |
| P430_NO_SIGNAL_THRESHOLD_TUNING | True | timing_only | timing_only | hard |
| P430_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: timing repair only; no signal threshold tuning in Phase430.

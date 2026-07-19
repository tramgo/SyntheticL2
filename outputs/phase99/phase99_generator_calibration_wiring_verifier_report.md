# Phase99 Generator Calibration Wiring Verifier

Generated UTC: 2026-07-19T21:44:02.582187+00:00

Phase99 verifies that Phase98 calibration profiles are available in code and affect generator outputs when explicitly selected.
It also checks that legacy default behavior is preserved and strategy replay remains locked.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase99_profile_rows | 5 | Generator calibration profiles available in code |
| phase99_wiring_check_rows | 5 | Wiring checks executed |
| phase99_wiring_checks_passed | 5 | Wiring checks passed |
| phase99_wiring_pass | 1 | 1 means calibration profiles are wired and replay lock is preserved |
| phase99_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase99_recommend_next_action | run_calibrated_generator_quality_smoke_no_strategy_replay | Recommended next milestone |

## Wiring Checks

| check_id | passed | detail |
| --- | --- | --- |
| P99_PHASE98_READY | True | phase98_ready_for_generator_patch_wiring=1.0 |
| P99_REPLAY_LOCK_PRESERVED | True | phase98_strategy_replay_allowed=0.0 |
| P99_DEFAULT_PROFILE_IDENTITY | True | build_raw_ticks(events) equals explicit P98_LEGACY_DEFAULT output |
| P99_BOOK_PROFILE_HAS_EFFECT | True | P98_FULL_BOOK_REBALANCE_BASE changes depth metrics on fixture |
| P99_DENSE_PROFILE_HAS_EFFECT | True | P98_FULL_BOOK_REBALANCE_STRONG changes dense timing metrics on fixture |

## Profiles In Code

| profile_id | event_timing_tail_gap_multiplier | event_timing_burst_throttle_fraction | price_micro_step_spread_fraction | price_jump_size_scale | book_l1_quantity_skew_scale | book_depth_ladder_multiplier | book_l1_l5_share_ratio | spread_preserve_current_scale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P98_FULL_BOOK_REBALANCE_BASE | 4 | 0.2 | 0.04 | 0.75 | 1.5 | 0.8 | 0.85 | 1 |
| P98_FULL_BOOK_REBALANCE_STRONG | 6 | 0.35 | 0.03 | 0.6 | 1.75 | 0.65 | 0.85 | 1 |
| P98_LEGACY_DEFAULT | 1 | 0 | 0.08 | 1 | 1 | 1 | 1 | 1 |
| P98_TIMING_ONLY_CONSERVATIVE | 2 | 0.1 | 0.08 | 1 | 1 | 1 | 1 | 1 |
| P98_TIMING_VOL_MODERATE | 4 | 0.2 | 0.04 | 0.75 | 1 | 1 | 1 | 1 |

## Phase45 Book Profile Effects

| profile_id | rows | median_l1_depth | median_l5_depth | median_abs_l1_imbalance_proxy | schema_columns | default_matches_legacy_explicit |
| --- | --- | --- | --- | --- | --- | --- |
| P98_LEGACY_DEFAULT | 8 | 2950 | 25075 | 0.1 | 61 | True |
| P98_FULL_BOOK_REBALANCE_BASE | 8 | 2006 | 19706 | 0.149796 | 61 | True |
| P98_FULL_BOOK_REBALANCE_STRONG | 8 | 1630.5 | 16015.5 | 0.175154 | 61 | True |

## Phase49 Dense Profile Effects

| profile_id | source_rows | dense_rows | median_callback_gap_ms | p90_callback_gap_ms | last_price_std | max_dense_subtick_id |
| --- | --- | --- | --- | --- | --- | --- |
| P98_LEGACY_DEFAULT | 8 | 32 | 1 | 97 | 2.32795 | 3 |
| P98_TIMING_VOL_MODERATE | 8 | 32 | 4 | 88 | 2.32795 | 3 |
| P98_FULL_BOOK_REBALANCE_STRONG | 8 | 32 | 6 | 81 | 2.32795 | 3 |

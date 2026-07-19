# Phase100 Calibrated Generator Quality Smoke

Generated UTC: 2026-07-19T21:47:11.952700+00:00

Phase100 runs a fixture-level generator quality smoke for the Phase98/99 calibration profiles.
It checks that profiles move failed calibration anchors in the intended direction while preserving spread and keeping strategy replay locked.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase100_profiles_smoked | 5 | Profiles evaluated in generator quality smoke |
| phase100_dense_multiplier | 8 | Dense multiplier used for fixture smoke |
| phase100_profile_comparison_rows | 4 | Non-legacy profiles compared with legacy |
| phase100_quality_check_rows | 7 | Quality smoke checks executed |
| phase100_quality_checks_passed | 7 | Quality smoke checks passed |
| phase100_quality_smoke_pass | 1 | 1 means calibrated generator quality smoke passed |
| phase100_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase100_recommend_next_action | run_small_calibrated_phase49_shard_quality_audit_no_strategy_replay | Recommended next milestone |

## Quality Checks

| check_id | passed | detail |
| --- | --- | --- |
| P100_PHASE99_WIRING_PASS | True | phase99_wiring_pass=1.0 |
| P100_REPLAY_LOCK_PRESERVED | True | phase99_strategy_replay_allowed=0.0 |
| P100_SEVERE_GAPS_PRESENT_FOR_SMOKE | True | phase97_severe_patch_rows=2.0 |
| P100_TIMING_PROFILE_MOVES_TAIL_GAP | True | P98_TIMING_VOL_MODERATE should increase p90 callback gap vs legacy on fixture. |
| P100_FULL_PROFILE_REDUCES_OR_PRESERVES_VOL | True | P98_FULL_BOOK_REBALANCE_BASE should not increase last-price fixture volatility vs legacy. |
| P100_FULL_PROFILE_INCREASES_L1_IMBALANCE | True | P98_FULL_BOOK_REBALANCE_BASE should increase L1 imbalance dispersion vs legacy. |
| P100_SPREAD_ANCHOR_PRESERVED | True | All calibrated profiles should preserve median spread proxy within 5%. |

## Profile Comparison vs Legacy

| profile_id | p90_gap_ms_ratio_vs_legacy | last_price_std_ratio_vs_legacy | median_abs_l1_imbalance_ratio_vs_legacy | median_l5_depth_ratio_vs_legacy | spread_bps_ratio_vs_legacy | tail_gap_improves | volatility_not_increased | l1_imbalance_increases | spread_preserved |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P98_FULL_BOOK_REBALANCE_BASE | 1.03217 | 0.999999 | 1.49796 | 0.785882 | 1 | True | True | True | True |
| P98_FULL_BOOK_REBALANCE_STRONG | 1.04826 | 0.999999 | 1.75154 | 0.638704 | 1 | True | True | True | True |
| P98_TIMING_ONLY_CONSERVATIVE | 1.0134 | 1 | 1 | 1 | 1 | True | True | True | True |
| P98_TIMING_VOL_MODERATE | 1.03217 | 0.999999 | 1 | 1 | 1 | True | True | True | True |

## Raw Book Profile Smoke

| profile_id | raw_rows | median_l1_depth | median_l5_depth | median_abs_l1_imbalance_proxy | median_spread_bps_proxy |
| --- | --- | --- | --- | --- | --- |
| P98_FULL_BOOK_REBALANCE_BASE | 8 | 2006 | 19706 | 0.149796 | 0.996512 |
| P98_FULL_BOOK_REBALANCE_STRONG | 8 | 1630.5 | 16015.5 | 0.175154 | 0.996512 |
| P98_LEGACY_DEFAULT | 8 | 2950 | 25075 | 0.1 | 0.996512 |
| P98_TIMING_ONLY_CONSERVATIVE | 8 | 2950 | 25075 | 0.1 | 0.996512 |
| P98_TIMING_VOL_MODERATE | 8 | 2950 | 25075 | 0.1 | 0.996512 |

## Dense Timing Profile Smoke

| profile_id | source_rows | dense_rows | dense_multiplier | median_callback_gap_ms | p90_callback_gap_ms | last_price_std | spread_preservation_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P98_FULL_BOOK_REBALANCE_BASE | 8 | 64 | 8 | 4 | 77 | 2.3094 | 0.996512 |
| P98_FULL_BOOK_REBALANCE_STRONG | 8 | 64 | 8 | 6 | 78.2 | 2.3094 | 0.996512 |
| P98_LEGACY_DEFAULT | 8 | 64 | 8 | 1 | 74.6 | 2.3094 | 0.996512 |
| P98_TIMING_ONLY_CONSERVATIVE | 8 | 64 | 8 | 2 | 75.6 | 2.3094 | 0.996512 |
| P98_TIMING_VOL_MODERATE | 8 | 64 | 8 | 4 | 77 | 2.3094 | 0.996512 |

# Phase101 Calibrated Phase49 Shard Quality Audit

Generated UTC: 2026-07-19T21:58:06.683680+00:00

Phase101 materializes small calibrated Phase49 dense shards for generator-quality auditing only.
It compares calibrated profiles against the legacy profile on timing, volatility, spread and book-shape metrics. It does not run strategy replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase101_profiles_audited | 3 | Calibration profiles materialized in shard audit |
| phase101_symbols_audited | 1 | Symbols audited |
| phase101_months_audited | 12 | Months audited |
| phase101_dense_multiplier | 8 | Dense multiplier used for bounded quality audit |
| phase101_dense_rows_materialized | 2258640 | Dense rows materialized locally for quality audit |
| phase101_quality_rows | 36 | Profile/month quality rows |
| phase101_quality_check_rows | 5 | Quality checks executed |
| phase101_quality_checks_passed | 4 | Quality checks passed |
| phase101_quality_audit_pass | 0 | 1 means small calibrated Phase49 quality audit passed |
| phase101_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase101_recommend_next_action | rerun_phase94_on_multiday_real_panel_when_available | Recommended next milestone |

## Quality Checks

| check_id | passed | detail |
| --- | --- | --- |
| P101_PHASE100_PASS | True | phase100_quality_smoke_pass=1.0 |
| P101_REPLAY_LOCK_PRESERVED | True | phase100_strategy_replay_allowed=0.0 |
| P101_TIMING_PROFILE_IMPROVES_ALL_MONTHS | True | P98_TIMING_VOL_MODERATE should improve p90 gap for every HDFCBANK month in shard audit. |
| P101_BOOK_PROFILE_REDUCES_OR_PRESERVES_VOL_ALL_MONTHS | False | P98_FULL_BOOK_REBALANCE_BASE should not increase one-tick volatility in any audited month. |
| P101_SPREAD_PRESERVED | True | All calibrated profiles must preserve median spread within 5% for every audited month. |

## Profile Comparison

| profile_id | month_rows | median_p90_gap_ratio | median_one_tick_vol_ratio | median_l1_imbalance_ratio | median_l5_depth_ratio | median_spread_ratio | tail_gap_improved_month_fraction | volatility_not_increased_month_fraction | spread_preserved_month_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P98_FULL_BOOK_REBALANCE_BASE | 12 | 1.01036 | 0.999989 | 1 | 1 | 1 | 1 | 0.5 | 1 |
| P98_TIMING_VOL_MODERATE | 12 | 1.01036 | 0.999989 | 1 | 1 | 1 | 1 | 0.5 | 1 |

## Quality by Profile Month

| profile_id | trade_month | symbol | source_rows | dense_rows | bytes | median_gap_ms | p90_gap_ms | p95_gap_ms | one_tick_return_std | median_spread_bps | p90_spread_bps | median_l1_depth | median_l5_depth | median_abs_l1_imbalance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P98_LEGACY_DEFAULT | 2026-01 | HDFCBANK | 8220 | 65760 | 1726504 | 1 | 193 | 293 | 0.00136953 | 1.21981 | 1.87641 | 792 | 6731 | 0.572368 |
| P98_LEGACY_DEFAULT | 2026-02 | HDFCBANK | 7476 | 59808 | 1576975 | 1 | 193 | 293 | 0.00135155 | 1.22647 | 3.03748 | 818 | 6953 | 0.572368 |
| P98_LEGACY_DEFAULT | 2026-03 | HDFCBANK | 8220 | 65760 | 1727334 | 1 | 193 | 293 | 0.00128116 | 1.22395 | 1.88667 | 792 | 6731 | 0.572238 |
| P98_LEGACY_DEFAULT | 2026-04 | HDFCBANK | 8212 | 65696 | 1748751 | 1 | 193 | 293 | 0.00124394 | 1.22399 | 2.97371 | 814 | 6918.5 | 0.572072 |
| P98_LEGACY_DEFAULT | 2026-05 | HDFCBANK | 7848 | 62784 | 1656031 | 1 | 193 | 293 | 0.00114978 | 1.2282 | 3.02572 | 830 | 7055 | 0.572727 |
| P98_LEGACY_DEFAULT | 2026-06 | HDFCBANK | 8198 | 65584 | 1739001 | 1 | 193 | 293 | 0.00140728 | 1.22941 | 3.04618 | 802 | 6818 | 0.572559 |
| P98_LEGACY_DEFAULT | 2026-07 | HDFCBANK | 8587 | 68696 | 1785742 | 1 | 193 | 293 | 0.00123307 | 1.2273 | 1.87935 | 812 | 6903 | 0.572368 |
| P98_LEGACY_DEFAULT | 2026-08 | HDFCBANK | 7841 | 62728 | 1657161 | 1 | 193 | 293 | 0.00140269 | 1.22858 | 2.97177 | 840 | 7140 | 0.572178 |
| P98_LEGACY_DEFAULT | 2026-09 | HDFCBANK | 8208 | 65664 | 1763095 | 1 | 193 | 293 | 0.00182389 | 1.2288 | 3.10443 | 826 | 7021 | 0.572398 |
| P98_LEGACY_DEFAULT | 2026-10 | HDFCBANK | 8212 | 65696 | 1720309 | 1 | 193 | 293 | 0.00100068 | 1.21803 | 1.25258 | 794 | 6748 | 0.572165 |
| P98_LEGACY_DEFAULT | 2026-11 | HDFCBANK | 7858 | 62864 | 1661868 | 1 | 193 | 293 | 0.00128204 | 1.22489 | 3.03545 | 816 | 6935.5 | 0.572238 |
| P98_LEGACY_DEFAULT | 2026-12 | HDFCBANK | 5230 | 41840 | 1058953 | 1 | 193 | 293 | 0.00142375 | 1.2253 | 3.03141 | 770 | 6544 | 0.572368 |
| P98_TIMING_VOL_MODERATE | 2026-01 | HDFCBANK | 8220 | 65760 | 2115872 | 4 | 195 | 295 | 0.00136964 | 1.21981 | 1.87641 | 792 | 6731 | 0.572368 |
| P98_TIMING_VOL_MODERATE | 2026-02 | HDFCBANK | 7476 | 59808 | 1939517 | 4 | 195 | 295 | 0.00135135 | 1.22647 | 3.03748 | 818 | 6953 | 0.572368 |
| P98_TIMING_VOL_MODERATE | 2026-03 | HDFCBANK | 8220 | 65760 | 2135217 | 4 | 195 | 295 | 0.00128118 | 1.22395 | 1.88667 | 792 | 6731 | 0.572238 |
| P98_TIMING_VOL_MODERATE | 2026-04 | HDFCBANK | 8212 | 65696 | 2140231 | 4 | 195 | 295 | 0.00124367 | 1.22399 | 2.97371 | 814 | 6918.5 | 0.572072 |
| P98_TIMING_VOL_MODERATE | 2026-05 | HDFCBANK | 7848 | 62784 | 2051720 | 4 | 195 | 295 | 0.00114979 | 1.2282 | 3.02572 | 830 | 7055 | 0.572727 |
| P98_TIMING_VOL_MODERATE | 2026-06 | HDFCBANK | 8198 | 65584 | 2117918 | 4 | 195 | 295 | 0.00140724 | 1.22941 | 3.04618 | 802 | 6818 | 0.572559 |
| P98_TIMING_VOL_MODERATE | 2026-07 | HDFCBANK | 8587 | 68696 | 2231018 | 4 | 195 | 295 | 0.0012331 | 1.2273 | 1.87935 | 812 | 6903 | 0.572368 |
| P98_TIMING_VOL_MODERATE | 2026-08 | HDFCBANK | 7841 | 62728 | 2037396 | 4 | 195 | 295 | 0.00140249 | 1.22858 | 2.97177 | 840 | 7140 | 0.572178 |
| P98_TIMING_VOL_MODERATE | 2026-09 | HDFCBANK | 8208 | 65664 | 2143952 | 4 | 195 | 295 | 0.00182408 | 1.2288 | 3.10443 | 826 | 7021 | 0.572398 |
| P98_TIMING_VOL_MODERATE | 2026-10 | HDFCBANK | 8212 | 65696 | 2105716 | 4 | 195 | 295 | 0.00100054 | 1.21803 | 1.25258 | 794 | 6748 | 0.572165 |
| P98_TIMING_VOL_MODERATE | 2026-11 | HDFCBANK | 7858 | 62864 | 2028522 | 4 | 195 | 295 | 0.00128188 | 1.22489 | 3.03545 | 816 | 6935.5 | 0.572238 |
| P98_TIMING_VOL_MODERATE | 2026-12 | HDFCBANK | 5230 | 41840 | 1390660 | 4 | 195 | 295 | 0.0014238 | 1.2253 | 3.03141 | 770 | 6544 | 0.572368 |
| P98_FULL_BOOK_REBALANCE_BASE | 2026-01 | HDFCBANK | 8220 | 65760 | 2115872 | 4 | 195 | 295 | 0.00136964 | 1.21981 | 1.87641 | 792 | 6731 | 0.572368 |
| P98_FULL_BOOK_REBALANCE_BASE | 2026-02 | HDFCBANK | 7476 | 59808 | 1939517 | 4 | 195 | 295 | 0.00135135 | 1.22647 | 3.03748 | 818 | 6953 | 0.572368 |
| P98_FULL_BOOK_REBALANCE_BASE | 2026-03 | HDFCBANK | 8220 | 65760 | 2135217 | 4 | 195 | 295 | 0.00128118 | 1.22395 | 1.88667 | 792 | 6731 | 0.572238 |
| P98_FULL_BOOK_REBALANCE_BASE | 2026-04 | HDFCBANK | 8212 | 65696 | 2140231 | 4 | 195 | 295 | 0.00124367 | 1.22399 | 2.97371 | 814 | 6918.5 | 0.572072 |
| P98_FULL_BOOK_REBALANCE_BASE | 2026-05 | HDFCBANK | 7848 | 62784 | 2051720 | 4 | 195 | 295 | 0.00114979 | 1.2282 | 3.02572 | 830 | 7055 | 0.572727 |
| P98_FULL_BOOK_REBALANCE_BASE | 2026-06 | HDFCBANK | 8198 | 65584 | 2117918 | 4 | 195 | 295 | 0.00140724 | 1.22941 | 3.04618 | 802 | 6818 | 0.572559 |
| P98_FULL_BOOK_REBALANCE_BASE | 2026-07 | HDFCBANK | 8587 | 68696 | 2231018 | 4 | 195 | 295 | 0.0012331 | 1.2273 | 1.87935 | 812 | 6903 | 0.572368 |
| P98_FULL_BOOK_REBALANCE_BASE | 2026-08 | HDFCBANK | 7841 | 62728 | 2037396 | 4 | 195 | 295 | 0.00140249 | 1.22858 | 2.97177 | 840 | 7140 | 0.572178 |
| P98_FULL_BOOK_REBALANCE_BASE | 2026-09 | HDFCBANK | 8208 | 65664 | 2143952 | 4 | 195 | 295 | 0.00182408 | 1.2288 | 3.10443 | 826 | 7021 | 0.572398 |
| P98_FULL_BOOK_REBALANCE_BASE | 2026-10 | HDFCBANK | 8212 | 65696 | 2105716 | 4 | 195 | 295 | 0.00100054 | 1.21803 | 1.25258 | 794 | 6748 | 0.572165 |
| P98_FULL_BOOK_REBALANCE_BASE | 2026-11 | HDFCBANK | 7858 | 62864 | 2028522 | 4 | 195 | 295 | 0.00128188 | 1.22489 | 3.03545 | 816 | 6935.5 | 0.572238 |
| P98_FULL_BOOK_REBALANCE_BASE | 2026-12 | HDFCBANK | 5230 | 41840 | 1390660 | 4 | 195 | 295 | 0.0014238 | 1.2253 | 3.03141 | 770 | 6544 | 0.572368 |

## Shard Inventory

| trade_month | symbol | source_rows | dense_rows | multiplier | file_path | bytes | profile_id | output_root |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | HDFCBANK | 8220 | 65760 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | 1726504 | P98_LEGACY_DEFAULT | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT |
| 2026-02 | HDFCBANK | 7476 | 59808 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT\trade_month=2026-02\symbol=HDFCBANK\part-00000.parquet | 1576975 | P98_LEGACY_DEFAULT | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT |
| 2026-03 | HDFCBANK | 8220 | 65760 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT\trade_month=2026-03\symbol=HDFCBANK\part-00000.parquet | 1727334 | P98_LEGACY_DEFAULT | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT |
| 2026-04 | HDFCBANK | 8212 | 65696 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT\trade_month=2026-04\symbol=HDFCBANK\part-00000.parquet | 1748751 | P98_LEGACY_DEFAULT | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT |
| 2026-05 | HDFCBANK | 7848 | 62784 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT\trade_month=2026-05\symbol=HDFCBANK\part-00000.parquet | 1656031 | P98_LEGACY_DEFAULT | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT |
| 2026-06 | HDFCBANK | 8198 | 65584 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT\trade_month=2026-06\symbol=HDFCBANK\part-00000.parquet | 1739001 | P98_LEGACY_DEFAULT | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT |
| 2026-07 | HDFCBANK | 8587 | 68696 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT\trade_month=2026-07\symbol=HDFCBANK\part-00000.parquet | 1785742 | P98_LEGACY_DEFAULT | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT |
| 2026-08 | HDFCBANK | 7841 | 62728 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT\trade_month=2026-08\symbol=HDFCBANK\part-00000.parquet | 1657161 | P98_LEGACY_DEFAULT | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT |
| 2026-09 | HDFCBANK | 8208 | 65664 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT\trade_month=2026-09\symbol=HDFCBANK\part-00000.parquet | 1763095 | P98_LEGACY_DEFAULT | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT |
| 2026-10 | HDFCBANK | 8212 | 65696 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT\trade_month=2026-10\symbol=HDFCBANK\part-00000.parquet | 1720309 | P98_LEGACY_DEFAULT | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT |
| 2026-11 | HDFCBANK | 7858 | 62864 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT\trade_month=2026-11\symbol=HDFCBANK\part-00000.parquet | 1661868 | P98_LEGACY_DEFAULT | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT |
| 2026-12 | HDFCBANK | 5230 | 41840 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT\trade_month=2026-12\symbol=HDFCBANK\part-00000.parquet | 1058953 | P98_LEGACY_DEFAULT | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_LEGACY_DEFAULT |
| 2026-01 | HDFCBANK | 8220 | 65760 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | 2115872 | P98_TIMING_VOL_MODERATE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE |
| 2026-02 | HDFCBANK | 7476 | 59808 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE\trade_month=2026-02\symbol=HDFCBANK\part-00000.parquet | 1939517 | P98_TIMING_VOL_MODERATE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE |
| 2026-03 | HDFCBANK | 8220 | 65760 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE\trade_month=2026-03\symbol=HDFCBANK\part-00000.parquet | 2135217 | P98_TIMING_VOL_MODERATE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE |
| 2026-04 | HDFCBANK | 8212 | 65696 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE\trade_month=2026-04\symbol=HDFCBANK\part-00000.parquet | 2140231 | P98_TIMING_VOL_MODERATE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE |
| 2026-05 | HDFCBANK | 7848 | 62784 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE\trade_month=2026-05\symbol=HDFCBANK\part-00000.parquet | 2051720 | P98_TIMING_VOL_MODERATE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE |
| 2026-06 | HDFCBANK | 8198 | 65584 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE\trade_month=2026-06\symbol=HDFCBANK\part-00000.parquet | 2117918 | P98_TIMING_VOL_MODERATE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE |
| 2026-07 | HDFCBANK | 8587 | 68696 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE\trade_month=2026-07\symbol=HDFCBANK\part-00000.parquet | 2231018 | P98_TIMING_VOL_MODERATE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE |
| 2026-08 | HDFCBANK | 7841 | 62728 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE\trade_month=2026-08\symbol=HDFCBANK\part-00000.parquet | 2037396 | P98_TIMING_VOL_MODERATE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE |
| 2026-09 | HDFCBANK | 8208 | 65664 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE\trade_month=2026-09\symbol=HDFCBANK\part-00000.parquet | 2143952 | P98_TIMING_VOL_MODERATE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE |
| 2026-10 | HDFCBANK | 8212 | 65696 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE\trade_month=2026-10\symbol=HDFCBANK\part-00000.parquet | 2105716 | P98_TIMING_VOL_MODERATE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE |
| 2026-11 | HDFCBANK | 7858 | 62864 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE\trade_month=2026-11\symbol=HDFCBANK\part-00000.parquet | 2028522 | P98_TIMING_VOL_MODERATE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE |
| 2026-12 | HDFCBANK | 5230 | 41840 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE\trade_month=2026-12\symbol=HDFCBANK\part-00000.parquet | 1390660 | P98_TIMING_VOL_MODERATE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_TIMING_VOL_MODERATE |
| 2026-01 | HDFCBANK | 8220 | 65760 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | 2115872 | P98_FULL_BOOK_REBALANCE_BASE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE |
| 2026-02 | HDFCBANK | 7476 | 59808 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE\trade_month=2026-02\symbol=HDFCBANK\part-00000.parquet | 1939517 | P98_FULL_BOOK_REBALANCE_BASE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE |
| 2026-03 | HDFCBANK | 8220 | 65760 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE\trade_month=2026-03\symbol=HDFCBANK\part-00000.parquet | 2135217 | P98_FULL_BOOK_REBALANCE_BASE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE |
| 2026-04 | HDFCBANK | 8212 | 65696 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE\trade_month=2026-04\symbol=HDFCBANK\part-00000.parquet | 2140231 | P98_FULL_BOOK_REBALANCE_BASE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE |
| 2026-05 | HDFCBANK | 7848 | 62784 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE\trade_month=2026-05\symbol=HDFCBANK\part-00000.parquet | 2051720 | P98_FULL_BOOK_REBALANCE_BASE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE |
| 2026-06 | HDFCBANK | 8198 | 65584 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE\trade_month=2026-06\symbol=HDFCBANK\part-00000.parquet | 2117918 | P98_FULL_BOOK_REBALANCE_BASE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE |
| 2026-07 | HDFCBANK | 8587 | 68696 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE\trade_month=2026-07\symbol=HDFCBANK\part-00000.parquet | 2231018 | P98_FULL_BOOK_REBALANCE_BASE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE |
| 2026-08 | HDFCBANK | 7841 | 62728 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE\trade_month=2026-08\symbol=HDFCBANK\part-00000.parquet | 2037396 | P98_FULL_BOOK_REBALANCE_BASE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE |
| 2026-09 | HDFCBANK | 8208 | 65664 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE\trade_month=2026-09\symbol=HDFCBANK\part-00000.parquet | 2143952 | P98_FULL_BOOK_REBALANCE_BASE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE |
| 2026-10 | HDFCBANK | 8212 | 65696 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE\trade_month=2026-10\symbol=HDFCBANK\part-00000.parquet | 2105716 | P98_FULL_BOOK_REBALANCE_BASE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE |
| 2026-11 | HDFCBANK | 7858 | 62864 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE\trade_month=2026-11\symbol=HDFCBANK\part-00000.parquet | 2028522 | P98_FULL_BOOK_REBALANCE_BASE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE |
| 2026-12 | HDFCBANK | 5230 | 41840 | 8 | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE\trade_month=2026-12\symbol=HDFCBANK\part-00000.parquet | 1390660 | P98_FULL_BOOK_REBALANCE_BASE | raw_synthetic_l2_phase102_anchored_price_quality\profile=P98_FULL_BOOK_REBALANCE_BASE |

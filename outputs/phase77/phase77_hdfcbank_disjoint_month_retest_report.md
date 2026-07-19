# Phase77 HDFCBANK Disjoint-Month Retest

Generated UTC: 2026-07-19T20:09:04.364903+00:00

Phase77 retests the Phase76 HDFCBANK lead-lag clue on trade months that were not used by the January timestamp-alignment near-miss.
Each month rebuilds a global timestamp matrix, trims to the longest common-overlap fresh window, and applies the same HDFCBANK threshold and retail cost profile.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase77_disjoint_months_tested | 11 | Non-January months retested |
| phase77_valid_months | 10 | Months with timestamp/common-overlap/recheck evidence |
| phase77_positive_months | 3 | Valid months with positive synthetic net P&L |
| phase77_pass_months | 2 | Valid months passing per-month HDFCBANK quality gates |
| phase77_total_trades | 624 | Aggregate HDFCBANK target trades across valid months |
| phase77_total_net_pnl_inr | -130842 | Aggregate after-cost synthetic net P&L across valid months |
| phase77_positive_month_fraction | 0.3 | Positive valid-month fraction |
| phase77_pass_month_fraction | 0.2 | Per-month gate pass fraction |
| phase77_hdfcbank_disjoint_retest_pass | 0 | 1 means HDFCBANK lead-lag survives disjoint-month falsification |
| phase77_recommend_next_action | retire_or_redesign_hdfcbank_lead_lag_before_more_shards | Recommended next action |

## Disjoint Month Detail

| trade_month | timestamp_contract_pass | raw_matrix_rows | raw_coverage_bucket_rows | raw_coverage_pass_fraction | common_overlap_bucket_count | common_overlap_matrix_rows | common_coverage_pass_fraction | fresh_cell_fraction | hdfcbank_recheck_rows | hdfcbank_recheck_pass | trades | target_symbols | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | precision_cost_clear | positive_target_fraction | cost_drag_to_abs_gross_ratio | elapsed_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02 | 1 | 217 | 13 | 0.384615 | 5 | 160 | 1 | 1 | 1 | 0 | 78 | 26 | -32419 | -23042.4 | 9376.58 | 0.025641 | 0 | 0.406927 | 14.3212 |
| 2026-03 | 1 | 226 | 10 | 0.5 | 5 | 160 | 1 | 1 | 1 | 0 | 26 | 26 | -16599.3 | -13478.9 | 3120.4 | 0 | 0 | 0.231503 | 13.0585 |
| 2026-04 | 1 | 234 | 11 | 0.454545 | 5 | 160 | 1 | 1 | 1 | 0 | 104 | 26 | -57051.8 | -41295.1 | 15756.7 | 0.519231 | 0.0769231 | 0.381563 | 14.8303 |
| 2026-05 | 1 | 234 | 11 | 0.454545 | 5 | 160 | 1 | 1 | 1 | 1 | 52 | 26 | 18679.7 | 24910.4 | 6230.7 | 1 | 1 | 0.250124 | 13.3607 |
| 2026-06 | 1 | 225 | 9 | 0.555556 | 5 | 160 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | 14.626 |
| 2026-07 | 1 | 231 | 11 | 0.454545 | 5 | 160 | 1 | 1 | 1 | 0 | 78 | 26 | -32936.9 | -23547.8 | 9389.11 | 0.410256 | 0 | 0.398726 | 14.1822 |
| 2026-08 | 1 | 211 | 11 | 0.454545 | 5 | 160 | 1 | 1 | 1 | 0 | 104 | 26 | 4414.43 | 16896.6 | 12482.2 | 0.653846 | 0.653846 | 0.738739 | 14.4885 |
| 2026-09 | 1 | 210 | 9 | 0.555556 | 5 | 160 | 1 | 1 | 1 | 0 | 26 | 26 | -3386.94 | -380.663 | 3006.28 | 0.0384615 | 0.0384615 | 7.89746 | 14.7252 |
| 2026-10 | 1 | 216 | 11 | 0.454545 | 5 | 160 | 1 | 1 | 1 | 1 | 78 | 26 | 11018 | 20378.4 | 9360.32 | 0.679487 | 0.884615 | 0.459327 | 13.2794 |
| 2026-11 | 1 | 230 | 12 | 0.416667 | 5 | 160 | 1 | 1 | 1 | 0 | 52 | 26 | -12957.7 | -6718.4 | 6239.31 | 0.0192308 | 0 | 0.928691 | 13.2191 |
| 2026-12 | 1 | 220 | 11 | 0.454545 | 5 | 160 | 1 | 1 | 1 | 0 | 26 | 26 | -9602.87 | -6479.15 | 3123.72 | 0 | 0 | 0.482118 | 13.1649 |

## HDFCBANK Recheck By Month

| retest_trade_month | rule_id | phase70_reference_rule_id | phase73_reference_rule_id | leader_symbol | alignment | threshold | trades | target_symbols | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | precision_cost_clear | positive_target_fraction | cost_drag_to_abs_gross_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02 | P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK | HDFCBANK | common_overlap_timestamp_bucket | 0.00428699 | 78 | 26 | -32419 | -23042.4 | 9376.58 | 0.025641 | 0 | 0.406927 |
| 2026-03 | P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK | HDFCBANK | common_overlap_timestamp_bucket | 0.00428699 | 26 | 26 | -16599.3 | -13478.9 | 3120.4 | 0 | 0 | 0.231503 |
| 2026-04 | P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK | HDFCBANK | common_overlap_timestamp_bucket | 0.00428699 | 104 | 26 | -57051.8 | -41295.1 | 15756.7 | 0.519231 | 0.0769231 | 0.381563 |
| 2026-05 | P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK | HDFCBANK | common_overlap_timestamp_bucket | 0.00428699 | 52 | 26 | 18679.7 | 24910.4 | 6230.7 | 1 | 1 | 0.250124 |
| 2026-07 | P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK | HDFCBANK | common_overlap_timestamp_bucket | 0.00428699 | 78 | 26 | -32936.9 | -23547.8 | 9389.11 | 0.410256 | 0 | 0.398726 |
| 2026-08 | P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK | HDFCBANK | common_overlap_timestamp_bucket | 0.00428699 | 104 | 26 | 4414.43 | 16896.6 | 12482.2 | 0.653846 | 0.653846 | 0.738739 |
| 2026-09 | P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK | HDFCBANK | common_overlap_timestamp_bucket | 0.00428699 | 26 | 26 | -3386.94 | -380.663 | 3006.28 | 0.0384615 | 0.0384615 | 7.89746 |
| 2026-10 | P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK | HDFCBANK | common_overlap_timestamp_bucket | 0.00428699 | 78 | 26 | 11018 | 20378.4 | 9360.32 | 0.679487 | 0.884615 | 0.459327 |
| 2026-11 | P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK | HDFCBANK | common_overlap_timestamp_bucket | 0.00428699 | 52 | 26 | -12957.7 | -6718.4 | 6239.31 | 0.0192308 | 0 | 0.928691 |
| 2026-12 | P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK | HDFCBANK | common_overlap_timestamp_bucket | 0.00428699 | 26 | 26 | -9602.87 | -6479.15 | 3123.72 | 0 | 0 | 0.482118 |

## Common-Overlap Coverage By Month

| retest_trade_month | trade_date | global_time_bucket_id | symbols_present | fresh_symbols | total_rows | max_staleness_seconds | median_staleness_seconds | expected_symbols | coverage_fraction | fresh_fraction | coverage_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02 | 2026-02-02 | 357322 | 32 | 32 | 621156 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-02 | 357323 | 32 | 32 | 2004614 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-02 | 357324 | 32 | 32 | 2069016 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-02 | 357325 | 32 | 32 | 1857362 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-02 | 357326 | 32 | 32 | 1040848 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-02 | 357806 | 32 | 32 | 945348 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-02 | 357807 | 32 | 32 | 2065438 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-02 | 357808 | 32 | 32 | 2079852 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-02 | 357809 | 32 | 32 | 1624446 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-02 | 357810 | 32 | 32 | 986212 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-04 | 2026-04-01 | 356821 | 32 | 32 | 835996 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-04 | 2026-04-01 | 356822 | 32 | 32 | 1950978 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-04 | 2026-04-01 | 356823 | 32 | 32 | 1998978 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-04 | 2026-04-01 | 356824 | 32 | 32 | 1692152 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-04 | 2026-04-01 | 356825 | 32 | 32 | 986288 | 17 | 1 | 32 | 1 | 1 | True |
| 2026-05 | 2026-05-01 | 357339 | 32 | 32 | 136400 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-05 | 2026-05-01 | 357340 | 32 | 32 | 1935646 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-05 | 2026-05-01 | 357341 | 32 | 32 | 2034036 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-05 | 2026-05-01 | 357342 | 32 | 32 | 2065408 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-05 | 2026-05-01 | 357343 | 32 | 32 | 1092678 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-06 | 2026-06-01 | 357875 | 32 | 32 | 702608 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-06 | 2026-06-01 | 357876 | 32 | 32 | 2011650 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-06 | 2026-06-01 | 357877 | 32 | 32 | 2064040 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-06 | 2026-06-01 | 357878 | 32 | 32 | 1823962 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-06 | 2026-06-01 | 357879 | 32 | 32 | 996624 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-07 | 2026-07-01 | 356855 | 32 | 32 | 12950 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-07 | 2026-07-01 | 356856 | 32 | 32 | 1732750 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-07 | 2026-07-01 | 356857 | 32 | 32 | 2018694 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-07 | 2026-07-01 | 356858 | 32 | 32 | 2065946 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-07 | 2026-07-01 | 356859 | 32 | 32 | 1253768 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-08 | 2026-08-03 | 357426 | 32 | 32 | 1254232 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-08 | 2026-08-03 | 357427 | 32 | 32 | 2014530 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-08 | 2026-08-03 | 357428 | 32 | 32 | 2089622 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-08 | 2026-08-03 | 357429 | 32 | 32 | 1550068 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-08 | 2026-08-03 | 357430 | 32 | 32 | 868676 | 517 | 1 | 32 | 1 | 1 | True |
| 2026-09 | 2026-09-01 | 357927 | 32 | 32 | 1021406 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-09 | 2026-09-01 | 357928 | 32 | 32 | 2036498 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-09 | 2026-09-01 | 357929 | 32 | 32 | 2055766 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-09 | 2026-09-01 | 357930 | 32 | 32 | 1656482 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-09 | 2026-09-01 | 357931 | 32 | 32 | 981680 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-10 | 2026-10-01 | 356942 | 32 | 32 | 932352 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-10 | 2026-10-01 | 356943 | 32 | 32 | 2052958 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-10 | 2026-10-01 | 356944 | 32 | 32 | 2036522 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-10 | 2026-10-01 | 356945 | 32 | 32 | 1702704 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-10 | 2026-10-01 | 356946 | 32 | 32 | 964920 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-11 | 2026-11-02 | 357460 | 32 | 32 | 190350 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-11 | 2026-11-02 | 357461 | 32 | 32 | 1965260 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-11 | 2026-11-02 | 357462 | 32 | 32 | 2046696 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-11 | 2026-11-02 | 357463 | 32 | 32 | 2034796 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-11 | 2026-11-02 | 357464 | 32 | 32 | 1054826 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-12 | 2026-12-01 | 357996 | 32 | 32 | 769236 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-12 | 2026-12-01 | 357997 | 32 | 32 | 2007292 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-12 | 2026-12-01 | 357998 | 32 | 32 | 2086104 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-12 | 2026-12-01 | 357999 | 32 | 32 | 1757986 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-12 | 2026-12-01 | 358000 | 32 | 32 | 1016446 | 1 | 1 | 32 | 1 | 1 | True |

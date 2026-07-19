# Phase82 Stratified HDFCBANK Disjoint Retest

Generated UTC: 2026-07-19T20:46:55.733671+00:00

Phase82 reruns the HDFCBANK lead-lag clue through the Phase81 stratified dense-window reader.
It is a bounded scenario-balanced dense replay, not a full 6B-row sweep.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase82_months_tested | 2 | Stratified months retested |
| phase82_valid_months | 0 | Months with coverage/freshness/recheck evidence |
| phase82_positive_months | 0 | Valid months with positive synthetic net P&L |
| phase82_pass_months | 0 | Valid months passing per-month HDFCBANK gates |
| phase82_total_trades | 0 | Aggregate stratified HDFCBANK trades |
| phase82_total_net_pnl_inr | 0 | Aggregate after-cost synthetic net P&L |
| phase82_positive_month_fraction | 0 | Positive valid-month fraction |
| phase82_pass_month_fraction | 0 | Per-month pass fraction |
| phase82_median_coverage_pass_fraction | 0.3419 | Median monthly timestamp bucket coverage pass fraction |
| phase82_stratified_hdfcbank_retest_pass | 0 | 1 means HDFCBANK survives stratified disjoint retest |
| phase82_recommend_next_action | materialize_cached_stratified_bars_and_fix_alignment_coverage | Recommended next milestone |

## Month Detail

| trade_month | matrix_rows | coverage_bucket_rows | coverage_pass_fraction | fresh_cell_fraction | recheck_rows | hdfcbank_recheck_pass | trades | target_symbols | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | precision_cost_clear | positive_target_fraction | cost_drag_to_abs_gross_ratio | elapsed_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02 | 2853 | 93 | 0.387097 | 0.461269 | 1 | 0 | 134 | 26 | -28784 | -12276 | 16507.9 | 0.201493 | 0.0384615 | 1.34473 | 59.7988 |
| 2026-03 | 2701 | 91 | 0.296703 | 0.363199 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | 64.1964 |

## HDFCBANK Recheck By Month

| trade_month | rule_id | phase76_reference_rule_id | leader_symbol | alignment | threshold | trades | target_symbols | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | precision_cost_clear | positive_target_fraction | cost_drag_to_abs_gross_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02 | P82_STRATIFIED_HDFCBANK_MOMENTUM_Q70_RECHECK | P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK | HDFCBANK | stratified_source_day_feed_timestamp_bucket | 0.00428699 | 134 | 26 | -28784 | -12276 | 16507.9 | 0.201493 | 0.0384615 | 1.34473 |

## Coverage Sample

| trade_month | trade_date | feed_profile | global_time_bucket_id | symbols_present | fresh_symbols | total_rows | max_staleness_seconds | median_staleness_seconds | expected_symbols | coverage_fraction | fresh_fraction | coverage_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02 | 2026-02-04 | disconnect_scenario | 357391 | 32 | 32 | 89532 | 17 | 9 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-04 | disconnect_scenario | 357392 | 16 | 0 | 6468 | 4985 | 4517 | 32 | 0.5 | 0 | False |
| 2026-02 | 2026-02-04 | good_retail | 357391 | 32 | 32 | 92012 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-04 | good_retail | 357392 | 32 | 0 | 3988 | 4917 | 4867 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-04 | ideal_research | 357391 | 32 | 32 | 93312 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-04 | ideal_research | 357392 | 32 | 0 | 2688 | 4917 | 4917 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-04 | normal_retail | 357391 | 32 | 32 | 88012 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-04 | normal_retail | 357392 | 32 | 0 | 7988 | 4917 | 4767 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-04 | stressed_retail | 357391 | 32 | 32 | 82320 | 17 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-04 | stressed_retail | 357392 | 27 | 0 | 13680 | 4767 | 4517 | 32 | 0.84375 | 0 | False |
| 2026-02 | 2026-02-05 | disconnect_scenario | 357408 | 25 | 25 | 14500 | 1 | 1 | 32 | 0.78125 | 0.78125 | False |
| 2026-02 | 2026-02-05 | disconnect_scenario | 357409 | 32 | 0 | 81500 | 3517 | 3517 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-05 | good_retail | 357408 | 32 | 32 | 18600 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-05 | good_retail | 357409 | 32 | 0 | 77400 | 3517 | 3467 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-05 | ideal_research | 357408 | 32 | 32 | 22400 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-05 | ideal_research | 357409 | 32 | 0 | 73600 | 3517 | 3517 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-05 | normal_retail | 357408 | 32 | 32 | 12100 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-05 | normal_retail | 357409 | 32 | 0 | 83900 | 3517 | 3317 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-05 | stressed_retail | 357408 | 24 | 24 | 8250 | 1 | 1 | 32 | 0.75 | 0.75 | False |
| 2026-02 | 2026-02-05 | stressed_retail | 357409 | 32 | 0 | 87750 | 3517 | 3267 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-10 | disconnect_scenario | 357460 | 32 | 32 | 65500 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-10 | disconnect_scenario | 357461 | 32 | 0 | 30500 | 4517 | 4251 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-10 | good_retail | 357460 | 32 | 32 | 70100 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-10 | good_retail | 357461 | 32 | 0 | 25900 | 4317 | 4267 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-10 | ideal_research | 357460 | 32 | 32 | 73600 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-10 | ideal_research | 357461 | 32 | 0 | 22400 | 4317 | 4317 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-10 | normal_retail | 357460 | 32 | 32 | 62200 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-10 | normal_retail | 357461 | 32 | 0 | 33800 | 4317 | 4117 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-10 | stressed_retail | 357460 | 32 | 32 | 48000 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-10 | stressed_retail | 357461 | 32 | 0 | 48000 | 4267 | 4017 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-13 | disconnect_scenario | 357547 | 32 | 0 | 96000 | 2518 | 2018 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-13 | good_retail | 357547 | 32 | 0 | 96000 | 2318 | 2268 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-13 | ideal_research | 357547 | 32 | 0 | 96000 | 2318 | 2318 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-13 | normal_retail | 357547 | 32 | 0 | 96000 | 2318 | 2118 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-13 | stressed_retail | 357547 | 32 | 0 | 96000 | 2268 | 1893 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-17 | disconnect_scenario | 357581 | 32 | 32 | 64517 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-17 | disconnect_scenario | 357582 | 32 | 0 | 31483 | 4518 | 4018 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-17 | good_retail | 357581 | 32 | 32 | 78777 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-17 | good_retail | 357582 | 32 | 0 | 17223 | 4518 | 4468 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-17 | ideal_research | 357581 | 32 | 32 | 80544 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-17 | ideal_research | 357582 | 32 | 0 | 15456 | 4518 | 4518 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-17 | normal_retail | 357581 | 32 | 32 | 73455 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-17 | normal_retail | 357582 | 32 | 0 | 22545 | 4518 | 4318 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-17 | stressed_retail | 357581 | 32 | 32 | 61034 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-17 | stressed_retail | 357582 | 32 | 0 | 34966 | 4518 | 4268 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-18 | disconnect_scenario | 357633 | 32 | 32 | 96000 | 518 | 18 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-18 | good_retail | 357633 | 32 | 32 | 96000 | 318 | 268 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-18 | ideal_research | 357633 | 32 | 32 | 96000 | 318 | 318 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-18 | normal_retail | 357633 | 32 | 32 | 95817 | 318 | 118 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-18 | normal_retail | 357634 | 1 | 0 | 183 | 4818 | 4818 | 32 | 0.03125 | 0 | False |
| 2026-02 | 2026-02-18 | stressed_retail | 357633 | 32 | 32 | 91238 | 268 | 18 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-18 | stressed_retail | 357634 | 15 | 0 | 4762 | 4768 | 4768 | 32 | 0.46875 | 0 | False |
| 2026-02 | 2026-02-19 | disconnect_scenario | 357650 | 27 | 27 | 32000 | 1 | 1 | 32 | 0.84375 | 0.84375 | False |
| 2026-02 | 2026-02-19 | disconnect_scenario | 357651 | 32 | 0 | 64000 | 4018 | 3984 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-19 | good_retail | 357650 | 32 | 32 | 45550 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-19 | good_retail | 357651 | 32 | 0 | 50450 | 3918 | 3868 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-19 | ideal_research | 357650 | 32 | 32 | 48000 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-19 | ideal_research | 357651 | 32 | 0 | 48000 | 3918 | 3918 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-19 | normal_retail | 357650 | 32 | 32 | 36100 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-19 | normal_retail | 357651 | 32 | 0 | 59900 | 3918 | 3718 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-19 | stressed_retail | 357650 | 29 | 29 | 18000 | 1 | 1 | 32 | 0.90625 | 0.90625 | False |
| 2026-02 | 2026-02-19 | stressed_retail | 357651 | 32 | 0 | 78000 | 4018 | 3393 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-20 | disconnect_scenario | 357668 | 32 | 0 | 96000 | 2518 | 2518 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-20 | good_retail | 357668 | 32 | 0 | 96000 | 2518 | 2468 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-20 | ideal_research | 357668 | 32 | 0 | 96000 | 2518 | 2518 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-20 | normal_retail | 357668 | 32 | 0 | 96000 | 2518 | 2418 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-20 | stressed_retail | 357668 | 32 | 0 | 96000 | 2518 | 2018 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-23 | disconnect_scenario | 357685 | 32 | 13 | 96000 | 1518 | 1018 | 32 | 1 | 0.40625 | False |
| 2026-02 | 2026-02-23 | good_retail | 357685 | 32 | 0 | 96000 | 1118 | 1068 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-23 | ideal_research | 357685 | 32 | 0 | 96000 | 1118 | 1118 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-23 | normal_retail | 357685 | 32 | 20 | 96000 | 1118 | 918 | 32 | 1 | 0.625 | False |
| 2026-02 | 2026-02-23 | stressed_retail | 357685 | 32 | 26 | 96000 | 1268 | 768 | 32 | 1 | 0.8125 | False |
| 2026-02 | 2026-02-24 | disconnect_scenario | 357702 | 32 | 32 | 79102 | 18 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-24 | disconnect_scenario | 357703 | 28 | 0 | 16898 | 4984 | 4518 | 32 | 0.875 | 0 | False |
| 2026-02 | 2026-02-24 | good_retail | 357702 | 32 | 32 | 85477 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-24 | good_retail | 357703 | 32 | 0 | 10523 | 4718 | 4668 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-24 | ideal_research | 357702 | 32 | 32 | 86944 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-24 | ideal_research | 357703 | 32 | 0 | 9056 | 4718 | 4718 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-24 | normal_retail | 357702 | 32 | 32 | 81410 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-24 | normal_retail | 357703 | 32 | 0 | 14590 | 4718 | 4518 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-24 | stressed_retail | 357702 | 32 | 32 | 75102 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-24 | stressed_retail | 357703 | 32 | 0 | 20898 | 4768 | 4518 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-25 | disconnect_scenario | 357754 | 32 | 32 | 96000 | 518 | 518 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-25 | good_retail | 357754 | 32 | 32 | 96000 | 518 | 468 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-25 | ideal_research | 357754 | 32 | 32 | 96000 | 518 | 518 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-25 | normal_retail | 357754 | 32 | 32 | 96000 | 518 | 318 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-25 | stressed_retail | 357754 | 32 | 32 | 94585 | 518 | 268 | 32 | 1 | 1 | True |
| 2026-02 | 2026-02-25 | stressed_retail | 357755 | 5 | 0 | 1415 | 4768 | 4768 | 32 | 0.15625 | 0 | False |
| 2026-02 | 2026-02-27 | disconnect_scenario | 357789 | 32 | 0 | 96000 | 3018 | 2518 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-27 | good_retail | 357789 | 32 | 0 | 96000 | 2718 | 2668 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-27 | ideal_research | 357789 | 32 | 0 | 96000 | 2718 | 2718 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-27 | normal_retail | 357789 | 32 | 0 | 96000 | 2718 | 2518 | 32 | 1 | 0 | False |
| 2026-02 | 2026-02-27 | stressed_retail | 357789 | 32 | 0 | 96000 | 2768 | 2268 | 32 | 1 | 0 | False |
| 2026-03 | 2026-03-02 | disconnect_scenario | 357806 | 32 | 2 | 96000 | 1517 | 1017 | 32 | 1 | 0.0625 | False |
| 2026-03 | 2026-03-02 | good_retail | 357806 | 32 | 0 | 96000 | 1317 | 1267 | 32 | 1 | 0 | False |
| 2026-03 | 2026-03-02 | ideal_research | 357806 | 32 | 0 | 96000 | 1317 | 1317 | 32 | 1 | 0 | False |
| 2026-03 | 2026-03-02 | normal_retail | 357806 | 32 | 5 | 96000 | 1317 | 1117 | 32 | 1 | 0.15625 | False |
| 2026-03 | 2026-03-02 | stressed_retail | 357806 | 32 | 13 | 96000 | 1517 | 1017 | 32 | 1 | 0.40625 | False |
| 2026-03 | 2026-03-03 | disconnect_scenario | 357823 | 32 | 32 | 89112 | 17 | 17 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-03 | disconnect_scenario | 357824 | 15 | 0 | 6888 | 4985 | 4517 | 32 | 0.46875 | 0 | False |
| 2026-03 | 2026-03-03 | good_retail | 357823 | 32 | 32 | 91762 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-03 | good_retail | 357824 | 32 | 0 | 4238 | 4917 | 4867 | 32 | 1 | 0 | False |
| 2026-03 | 2026-03-03 | ideal_research | 357823 | 32 | 32 | 93312 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-03 | ideal_research | 357824 | 32 | 0 | 2688 | 4917 | 4917 | 32 | 1 | 0 | False |
| 2026-03 | 2026-03-03 | normal_retail | 357823 | 32 | 32 | 86496 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-03 | normal_retail | 357824 | 32 | 0 | 9504 | 4917 | 4717 | 32 | 1 | 0 | False |
| 2026-03 | 2026-03-03 | stressed_retail | 357823 | 32 | 32 | 80128 | 17 | 1 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-03 | stressed_retail | 357824 | 28 | 0 | 15872 | 4985 | 4517 | 32 | 0.875 | 0 | False |
| 2026-03 | 2026-03-04 | disconnect_scenario | 357875 | 32 | 27 | 95516 | 1017 | 517 | 32 | 1 | 0.84375 | False |
| 2026-03 | 2026-03-04 | disconnect_scenario | 357876 | 1 | 0 | 484 | 4517 | 4517 | 32 | 0.03125 | 0 | False |
| 2026-03 | 2026-03-04 | good_retail | 357875 | 32 | 32 | 96000 | 717 | 667 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-04 | ideal_research | 357875 | 32 | 32 | 96000 | 717 | 717 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-04 | normal_retail | 357875 | 32 | 32 | 96000 | 717 | 517 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-04 | stressed_retail | 357875 | 32 | 32 | 96000 | 767 | 267 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-05 | disconnect_scenario | 357892 | 31 | 31 | 60000 | 1 | 1 | 32 | 0.96875 | 0.96875 | True |
| 2026-03 | 2026-03-05 | disconnect_scenario | 357893 | 32 | 0 | 36000 | 4517 | 4017 | 32 | 1 | 0 | False |
| 2026-03 | 2026-03-05 | good_retail | 357892 | 32 | 32 | 68400 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-05 | good_retail | 357893 | 32 | 0 | 27600 | 4317 | 4267 | 32 | 1 | 0 | False |
| 2026-03 | 2026-03-05 | ideal_research | 357892 | 32 | 32 | 73600 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-03 | 2026-03-05 | ideal_research | 357893 | 32 | 0 | 22400 | 4317 | 4317 | 32 | 1 | 0 | False |

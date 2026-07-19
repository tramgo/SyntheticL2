# Phase76 Common-Overlap Synchronous Matrix Validator

Generated UTC: 2026-07-19T20:03:13.488126+00:00

Phase76 trims the Phase75 timestamp matrix to the contiguous common-overlap window where all symbols are fresh.
It then rechecks the HDFCBANK lead-lag near-miss on that safer window.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase76_common_overlap_bucket_count | 5 | Contiguous passing timestamp buckets selected from Phase75 |
| phase76_trimmed_matrix_rows | 160 | Common-overlap matrix rows |
| phase76_coverage_pass_fraction | 1 | Fraction of common-overlap buckets passing coverage/freshness |
| phase76_fresh_cell_fraction | 1 | Fraction of common-overlap cells fresh |
| phase76_common_overlap_matrix_pass | 1 | 1 means synchronous matrix remediation passes on common overlap |
| phase76_hdfcbank_recheck_passes_gate | 1 | 1 means HDFCBANK near-miss passes after common-overlap remediation |
| phase76_allow_hdfcbank_retest_expansion | 1 | 1 means HDFCBANK retest can expand |
| phase76_recommend_next_action | hdfcbank_disjoint_month_retest | Recommended next action |

## Common-Overlap HDFCBANK Recheck

| rule_id | phase70_reference_rule_id | phase73_reference_rule_id | leader_symbol | alignment | threshold | trades | target_symbols | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | precision_cost_clear | positive_target_fraction | cost_drag_to_abs_gross_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P76_COMMON_OVERLAP_HDFCBANK_MOMENTUM_Q70_RECHECK | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK | HDFCBANK | common_overlap_timestamp_bucket | 0.00428699 | 78 | 26 | 23654.9 | 32993.4 | 9338.46 | 0.589744 | 0.923077 | 0.283041 |

## Common-Overlap Coverage

| trade_date | global_time_bucket_id | symbols_present | fresh_symbols | total_rows | max_staleness_seconds | median_staleness_seconds | expected_symbols | coverage_fraction | fresh_fraction | coverage_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01-01 | 356804 | 32 | 32 | 1426414 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-01-01 | 356805 | 32 | 32 | 2032340 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-01-01 | 356806 | 32 | 32 | 2063860 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-01-01 | 356807 | 32 | 32 | 1437114 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-01-01 | 356808 | 32 | 32 | 836532 | 517 | 17 | 32 | 1 | 1 | True |

## Common-Overlap Window

| trade_date | global_time_bucket_id | symbols_present | fresh_symbols | total_rows | min_first_timestamp_seconds | max_last_timestamp_seconds | max_staleness_seconds | median_staleness_seconds | expected_symbols | coverage_fraction | fresh_fraction | coverage_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01-01 | 356804 | 32 | 32 | 1426414 | 1.78402e+09 | 1.78402e+09 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-01-01 | 356805 | 32 | 32 | 2032340 | 1.78402e+09 | 1.78403e+09 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-01-01 | 356806 | 32 | 32 | 2063860 | 1.78403e+09 | 1.78403e+09 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-01-01 | 356807 | 32 | 32 | 1437114 | 1.78404e+09 | 1.78404e+09 | 1 | 1 | 32 | 1 | 1 | True |
| 2026-01-01 | 356808 | 32 | 32 | 836532 | 1.78404e+09 | 1.78404e+09 | 517 | 17 | 32 | 1 | 1 | True |

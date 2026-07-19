# Phase84 Cached Stratified HDFCBANK Retest

Generated UTC: 2026-07-19T20:53:37.759770+00:00

Phase84 retests the HDFCBANK lead-lag clue on the Phase83 coverage-valid cached source-event bars.
This is the fair full stratified retest after the Phase82 timestamp-bucket coverage failure.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase84_cached_bar_rows | 160150 | Cached stratified bars read |
| phase84_months_tested | 12 | Months represented in cached bars |
| phase84_valid_months | 12 | Months with HDFCBANK recheck trades |
| phase84_positive_months | 3 | Valid months with positive after-cost synthetic P&L |
| phase84_pass_months | 0 | Valid months passing quality gates |
| phase84_total_trades | 58988 | Aggregate HDFCBANK target trades |
| phase84_total_net_pnl_inr | -6.97746e+06 | Aggregate after-cost synthetic net P&L |
| phase84_positive_month_fraction | 0.25 | Positive valid-month fraction |
| phase84_pass_month_fraction | 0 | Per-month gate pass fraction |
| phase84_cached_stratified_hdfcbank_pass | 0 | 1 means HDFCBANK survives cached stratified retest |
| phase84_recommend_next_action | retire_hdfcbank_lead_lag_after_cached_stratified_falsification | Recommended next milestone |

## Monthly HDFCBANK Recheck

| trade_month | trades | target_symbols | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | precision_cost_clear | positive_target_fraction | cost_drag_to_abs_gross_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | 4682 | 26 | 840303 | 1.46021e+06 | 619904 | 0.49402 | 1 | 0.424532 |
| 2026-02 | 5216 | 26 | 213682 | 927047 | 713365 | 0.502492 | 0.692308 | 0.769503 |
| 2026-03 | 5152 | 26 | -827640 | -156845 | 670795 | 0.411685 | 0 | 4.27681 |
| 2026-04 | 4434 | 26 | -1.18021e+06 | -582488 | 597722 | 0.456698 | 0 | 1.02615 |
| 2026-05 | 5273 | 26 | -710519 | -7485.17 | 703034 | 0.399583 | 0 | 93.9235 |
| 2026-06 | 5614 | 26 | -598650 | 185942 | 784592 | 0.395262 | 0.0384615 | 4.21955 |
| 2026-07 | 4354 | 26 | -1.15058e+06 | -591819 | 558765 | 0.354616 | 0 | 0.944149 |
| 2026-08 | 5901 | 26 | -1.83818e+06 | -1.05244e+06 | 785737 | 0.3596 | 0 | 0.746584 |
| 2026-09 | 5277 | 26 | -828078 | -110538 | 717540 | 0.431874 | 0 | 6.49136 |
| 2026-10 | 4391 | 26 | -722259 | -181232 | 541028 | 0.416989 | 0 | 2.98528 |
| 2026-11 | 6001 | 26 | 155521 | 968839 | 813318 | 0.485919 | 0.692308 | 0.839477 |
| 2026-12 | 2693 | 26 | -330849 | 35471.5 | 366320 | 0.470108 | 0 | 10.3272 |

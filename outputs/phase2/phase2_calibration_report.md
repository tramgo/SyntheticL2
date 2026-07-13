# Phase 2 Empirical Calibration Report

Generated UTC: 2026-07-13T20:30:08.939747+00:00

## Scope

This report calibrates one-day received-tick distributions from Phase 1 outputs.
It does not certify regime stability, strategy profitability, queue fills or shock frequencies.

## Inventory

- Symbols calibrated: 32
- Rows represented: 620853
- Symbols with >15s stale gaps: 32
- Symbols with book-valid fraction below 99.9%: 0

## Instrument-Class Summary

| instrument_class | symbols | rows | median_event_rate_per_second | median_spread_ticks | median_book_valid_fraction | median_l5_imbalance | total_volume_increment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| equity | 27 | 537618 | 0.8396891797680396 | 4.0 | 0.9999477096841665 | -0.0011467889908256881 | 187046042.0 |
| etf | 5 | 83235 | 0.7727358997628363 | 4.000000000005684 | 0.9998853342506593 | 0.16302367941712204 | 85686346.0 |

## Five-Second Cross-Symbol Correlation Summary

| metric | value | evidence_label |
| --- | --- | --- |
| five_second_pairwise_corr_count | 992.0 | weak_one_day |
| five_second_pairwise_corr_median | 0.04352251141775541 | weak_one_day |
| five_second_pairwise_corr_q05 | -0.05057314631409772 | weak_one_day |
| five_second_pairwise_corr_q95 | 0.2428643184774939 | weak_one_day |

## Largest Stale-Gap Counts

| symbol | instrument_class | stale_gap_gt_15s_count | elapsed_ms_median | elapsed_ms_q95 |
| --- | --- | --- | --- | --- |
| ADANIPORTS | equity | 2 | 1000.0 | 5500.0 |
| AXISBANK | equity | 2 | 749.0 | 4913.649999999998 |
| BAJAJ-AUTO | equity | 2 | 741.0 | 4410.049999999999 |
| BANKBEES | etf | 2 | 1000.0 | 4833.0 |
| BHARTIARTL | equity | 2 | 749.0 | 4762.399999999994 |
| BPCL | equity | 2 | 1602.0 | 6081.699999999999 |
| BRITANNIA | equity | 2 | 2000.0 | 7000.799999999999 |
| CIPLA | equity | 2 | 1194.0 | 5953.9 |

## Tightest Median Spreads

| symbol | instrument_class | spread_ticks_median | spread_ticks_q95 | reference_ltp_median |
| --- | --- | --- | --- | --- |
| ITBEES | etf | 1.0000000000003553 | 2.0000000000007105 | 32.13 |
| BPCL | equity | 1.0000000000011369 | 3.0000000000034106 | 306.0 |
| ITC | equity | 1.0000000000011369 | 3.0000000000022737 | 280.1 |
| GOLDBEES | etf | 1.000000000001421 | 3.000000000002842 | 116.82 |
| KOTAKBANK | equity | 2.000000000001137 | 3.0000000000034106 | 379.8 |
| ICICIBANK | equity | 2.0000000000022737 | 5.0000000000045475 | 1403.5 |
| HDFCBANK | equity | 2.0000000000022737 | 5.0000000000045475 | 818.7 |
| AXISBANK | equity | 2.0000000000022737 | 5.0000000000045475 | 1320.3 |

## Outputs

- `price_tick_calibration.csv`
- `activity_calibration.csv`
- `depth_calibration.csv`
- `trade_flow_calibration.csv`
- `cross_section_class_summary.csv`
- `cross_section_correlation_summary.csv`
- `parameter_evidence_ledger.csv`
- `calibration_manifest.json`

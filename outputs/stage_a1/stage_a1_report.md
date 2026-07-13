# Stage A1 Tick-Stream Audit Report

Generated UTC: 2026-07-13T20:46:03.676557+00:00
Input directory: `real_data_sample\l2_single_day`
Output directory: `outputs\stage_a1`

## Scope

This report audits the current one-day Zerodha WebSocket L2 sample as a received-tick stream.
It does not claim multi-day calibration, strategy profitability, or exchange-order reconstruction.

## Inventory

- Symbols discovered: 32
- Parquet files: 50205
- Rows: 620853
- Bytes: 1764005784
- Manifest present: True
- Manifest rows: 50205
- Missing local files from manifest: 0
- Extra local files not in manifest: 0
- Size mismatches: 0

## Class Profile

| instrument_class | symbols | rows | median_event_rate_per_second | median_interarrival_ms | total_files | total_bytes |
| --- | --- | --- | --- | --- | --- | --- |
| equity | 27 | 537618 | 0.8396891797680396 | 749.0 | 42363 | 1490269423 |
| etf | 5 | 83235 | 0.7727358997628363 | 1000.0 | 7842 | 273736361 |

## Stage A1 Gate Status

| Gate | Status | Evidence |
|---|---|---|
| All 32 requested symbols represented | PASS | Found 32 symbols |
| Manifest/file completeness | PASS | Compared local files to manifest |
| Schema consistency | PASS | 50205/50205 files match first schema |
| Receive ordering | PASS | 0 monotonic-ns order violations |
| Book not crossed | PASS | 0 crossed best-book rows |
| Depth price sorting | PASS | Bid errors 0, ask errors 0 |
| Horizon coverage measured | PASS | 224 symbol/horizon rows |
| Parameter evidence labelled | PASS | See `parameter_evidence_ledger.csv` |

## Largest Receive Gaps

| symbol | instrument_class | max_interarrival_ms | p95_interarrival_ms | stale_gap_gt_15s_count |
| --- | --- | --- | --- | --- |
| BRITANNIA | equity | 211233.0 | 7000.799999999999 | 2 |
| ULTRACEMCO | equity | 211233.0 | 6772.5999999999985 | 2 |
| NESTLEIND | equity | 211232.0 | 5800.199999999999 | 2 |
| HINDUNILVR | equity | 211231.0 | 5859.449999999999 | 2 |
| ITC | equity | 211230.0 | 5750.0 | 2 |

## 1-Second Horizon Support

The 90% gate is a dense full-session regular-panel gate, not a claim that 1-second or sub-second received ticks are absent.
Symbols below the dense full-session 90% one-second bin coverage gate: ADANIPORTS, AXISBANK, BAJAJ-AUTO, BANKBEES, BHARTIARTL, BPCL, BRITANNIA, CIPLA, DRREDDY, GOLDBEES, HCLTECH, HDFCBANK, HINDUNILVR, ICICIBANK, INFY, ITBEES, ITC, JUNIORBEES, KOTAKBANK, LT, M&M, MARUTI, NESTLEIND, NIFTYBEES, ONGC, RELIANCE, SBIN, SUNPHARMA, TCS, TECHM, ULTRACEMCO, WIPRO
Use event-driven ticks and window-specific coverage audits before enabling 1-second features for active periods such as the open.

## Outputs

- `compact_ticks_by_symbol/symbol=*/ticks.parquet`
- `data_quality_report.csv` and `data_quality_report.parquet`
- `horizon_coverage.csv`
- `schema_report.csv`
- `file_inventory.csv`
- `manifest_check.json`
- `parameter_evidence_ledger.csv`

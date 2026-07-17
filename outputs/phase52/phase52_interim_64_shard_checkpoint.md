# Phase52 Interim Checkpoint: Dense Replay First 64 Shards

Generated: 2026-07-17 11:34 IST

## Scope

This is the eighth interim evidence checkpoint for the Phase52 full-year dense synthetic L2 strategy replay.
The live replay continues from `outputs/phase52/dense_replay_daily_symbol.csv`; this note freezes the first 64-shard partial summary.

## Replay progress

| Metric | Value |
|---|---:|
| Dense input shards | 384 |
| Shards replayed in this checkpoint | 64 |
| Completion | 16.67% |
| Aggregated dense tick trade count | 446,158,826 |
| Strategy/profile result rows | 9 |
| Positive after-cost rows | 0 |
| Synthetic candidate rows | 0 |
| Replay elapsed seconds | 37,831.657511 |
| Zerodha cost model version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| Acceptance ready | 0 |

## Interim strategy/profile ranking

All first-64-shard strategy/profile combinations remain negative after costs.

| Strategy | Execution profile | Trades | Annualized net P&L INR | Sharpe-like proxy | Candidate |
|---|---|---:|---:|---:|---|
| DENSE_S01_L1_IMBALANCE | zero_latency_spread_only_control | 50,393,239 | -871,137,822.39 | -10.034279 | False |
| DENSE_S03_1T_MOMENTUM | zero_latency_spread_only_control | 49,604,534 | -1,173,197,497.68 | -6.223831 | False |
| DENSE_S02_MICROPRICE | zero_latency_spread_only_control | 49,895,387 | -1,245,675,487.74 | -8.447603 | False |
| DENSE_S01_L1_IMBALANCE | retail_marketable_default | 49,837,796 | -6,949,529,153.05 | -12.273117 | False |
| DENSE_S03_1T_MOMENTUM | retail_marketable_default | 49,002,824 | -7,773,289,306.66 | -6.422273 | False |
| DENSE_S02_MICROPRICE | retail_marketable_default | 49,292,318 | -8,013,033,885.87 | -7.668017 | False |
| DENSE_S01_L1_IMBALANCE | stressed_retail | 49,837,718 | -9,415,407,669.65 | -11.936196 | False |
| DENSE_S03_1T_MOMENTUM | stressed_retail | 49,002,766 | -10,825,976,933.44 | -6.391408 | False |
| DENSE_S02_MICROPRICE | stressed_retail | 49,292,244 | -11,212,512,485.62 | -7.645634 | False |

## Interpretation

This checkpoint does not close Phase52 because only 64 of 384 dense shards have completed.
It extends the first-8 through first-56 shard evidence: the first-pass dense signal catalog continues to show no synthetic-only after-cost edge.

Acceptance remains closed because there are zero positive-after-cost strategy/profile rows and zero synthetic candidate rows.

# Phase52 Interim Checkpoint: Dense Replay First 40 Shards

Generated: 2026-07-17 06:34 IST

## Scope

This is the fifth interim evidence checkpoint for the Phase52 full-year dense synthetic L2 strategy replay.
The live replay continues from `outputs/phase52/dense_replay_daily_symbol.csv`; this note freezes the first 40-shard partial summary.

## Replay progress

| Metric | Value |
|---|---:|
| Dense input shards | 384 |
| Shards replayed in this checkpoint | 40 |
| Completion | 10.42% |
| Aggregated dense tick trade count | 286,817,093 |
| Strategy/profile result rows | 9 |
| Positive after-cost rows | 0 |
| Synthetic candidate rows | 0 |
| Replay elapsed seconds | 19,840.237676 |
| Zerodha cost model version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| Acceptance ready | 0 |

## Interim strategy/profile ranking

All first-40-shard strategy/profile combinations remain negative after costs.

| Strategy | Execution profile | Trades | Annualized net P&L INR | Sharpe-like proxy | Candidate |
|---|---|---:|---:|---:|---|
| DENSE_S01_L1_IMBALANCE | zero_latency_spread_only_control | 32,390,551 | -569,362,516.34 | -8.463688 | False |
| DENSE_S03_1T_MOMENTUM | zero_latency_spread_only_control | 31,898,822 | -767,372,122.63 | -5.263874 | False |
| DENSE_S02_MICROPRICE | zero_latency_spread_only_control | 32,082,085 | -817,752,434.23 | -6.493200 | False |
| DENSE_S01_L1_IMBALANCE | retail_marketable_default | 32,025,559 | -4,493,301,745.83 | -9.772751 | False |
| DENSE_S03_1T_MOMENTUM | retail_marketable_default | 31,515,942 | -5,037,029,857.23 | -5.358485 | False |
| DENSE_S02_MICROPRICE | retail_marketable_default | 31,681,341 | -5,199,049,458.42 | -5.875505 | False |
| DENSE_S01_L1_IMBALANCE | stressed_retail | 32,025,539 | -6,096,022,037.43 | -9.572140 | False |
| DENSE_S03_1T_MOMENTUM | stressed_retail | 31,515,925 | -7,025,416,078.94 | -5.345157 | False |
| DENSE_S02_MICROPRICE | stressed_retail | 31,681,329 | -7,287,845,371.61 | -5.872161 | False |

## Interpretation

This checkpoint does not close Phase52 because only 40 of 384 dense shards have completed.
It extends the first-8, first-16, first-24, and first-32 shard evidence: the first-pass dense signal catalog continues to show no synthetic-only after-cost edge.

Acceptance remains closed because there are zero positive-after-cost strategy/profile rows and zero synthetic candidate rows.

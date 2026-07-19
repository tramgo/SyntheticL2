# Phase52 Interim Checkpoint: Dense Replay First 112 Shards

Generated: 2026-07-19 16:06 IST

## Scope

This is an interim evidence checkpoint for the Phase52 full-year dense synthetic L2 strategy replay.
The live replay advanced while detached; this note freezes the latest material partial summary, which was written at the 112-shard boundary.

The daily-symbol checkpoint subsequently reached 114 shards before the old worker stopped making shard-boundary writes. The replay was resumed from the durable CSV checkpoint after preserving this evidence.

## Replay progress

| Metric | Value |
|---|---:|
| Dense input shards | 384 |
| Shards replayed in this partial summary | 112 |
| Completion at partial summary | 29.17% |
| Aggregated dense tick trade count | 797,029,565 |
| Strategy/profile result rows | 9 |
| Positive after-cost rows | 0 |
| Synthetic candidate rows | 0 |
| Replay elapsed seconds | 90,525.240898 |
| Zerodha cost model version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| Acceptance ready | 0 |

## Interim strategy/profile ranking

All first-112-shard strategy/profile combinations remain negative after costs.

| Strategy | Execution profile | Trades | Annualized net P&L INR | Sharpe-like proxy | Candidate |
|---|---|---:|---:|---:|---|
| DENSE_S01_L1_IMBALANCE | zero_latency_spread_only_control | 90,068,501 | -1,546,766,171.08 | -9.682022 | False |
| DENSE_S03_1T_MOMENTUM | zero_latency_spread_only_control | 88,584,746 | -2,071,472,217.98 | -6.086762 | False |
| DENSE_S02_MICROPRICE | zero_latency_spread_only_control | 89,084,762 | -2,203,270,237.31 | -9.214466 | False |
| DENSE_S01_L1_IMBALANCE | retail_marketable_default | 89,100,465 | -12,394,755,228.79 | -11.636677 | False |
| DENSE_S03_1T_MOMENTUM | retail_marketable_default | 87,500,212 | -13,810,649,253.64 | -6.263092 | False |
| DENSE_S02_MICROPRICE | retail_marketable_default | 88,045,262 | -14,251,396,619.83 | -7.925121 | False |
| DENSE_S01_L1_IMBALANCE | stressed_retail | 89,100,367 | -16,784,152,074.39 | -11.335122 | False |
| DENSE_S03_1T_MOMENTUM | stressed_retail | 87,500,146 | -19,215,592,511.42 | -6.236383 | False |
| DENSE_S02_MICROPRICE | stressed_retail | 88,045,104 | -19,925,530,601.94 | -7.905552 | False |

## Interpretation

This checkpoint does not close Phase52 because only 112 of 384 dense shards are represented in the latest material partial summary.
It extends the first-8 through first-64 shard evidence: the first-pass dense signal catalog continues to show no synthetic-only after-cost edge.

Acceptance remains closed because there are zero positive-after-cost strategy/profile rows and zero synthetic candidate rows.

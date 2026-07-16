# Phase52 Interim Checkpoint: Dense Replay First 24 Shards

Generated: 2026-07-17 03:44 IST

## Scope

This is the third interim evidence checkpoint for the Phase52 full-year dense synthetic L2 strategy replay.
The live replay continues from `outputs/phase52/dense_replay_daily_symbol.csv`; this note freezes the first 24-shard partial summary.

## Replay progress

| Metric | Value |
|---|---:|
| Dense input shards | 384 |
| Shards replayed in this checkpoint | 24 |
| Completion | 6.25% |
| Aggregated dense tick trade count | 175,530,833 |
| Strategy/profile result rows | 9 |
| Positive after-cost rows | 0 |
| Synthetic candidate rows | 0 |
| Replay elapsed seconds | 9,749.017320 |
| Zerodha cost model version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| Acceptance ready | 0 |

## Interim strategy/profile ranking

All first-24-shard strategy/profile combinations remain negative after costs.

| Strategy | Execution profile | Trades | Annualized net P&L INR | Sharpe-like proxy | Candidate |
|---|---|---:|---:|---:|---|
| DENSE_S01_L1_IMBALANCE | zero_latency_spread_only_control | 19,863,282 | -332,006,079.70 | -9.017584 | False |
| DENSE_S03_1T_MOMENTUM | zero_latency_spread_only_control | 19,498,840 | -455,808,479.82 | -5.638194 | False |
| DENSE_S02_MICROPRICE | zero_latency_spread_only_control | 19,605,708 | -493,075,554.95 | -12.269221 | False |
| DENSE_S01_L1_IMBALANCE | retail_marketable_default | 19,651,006 | -2,706,304,982.50 | -11.180229 | False |
| DENSE_S03_1T_MOMENTUM | retail_marketable_default | 19,272,812 | -3,041,460,446.43 | -5.905655 | False |
| DENSE_S02_MICROPRICE | retail_marketable_default | 19,357,703 | -3,157,101,293.17 | -10.898667 | False |
| DENSE_S01_L1_IMBALANCE | stressed_retail | 19,650,976 | -3,655,862,669.28 | -10.858869 | False |
| DENSE_S03_1T_MOMENTUM | stressed_retail | 19,272,811 | -4,231,514,682.59 | -5.863696 | False |
| DENSE_S02_MICROPRICE | stressed_retail | 19,357,695 | -4,420,289,788.79 | -10.838257 | False |

## Interpretation

This checkpoint does not close Phase52 because only 24 of 384 dense shards have completed.
It extends the first-8 and first-16 shard evidence: the first-pass dense signal catalog continues to show no synthetic-only after-cost edge.

Acceptance remains closed because there are zero positive-after-cost strategy/profile rows and zero synthetic candidate rows.

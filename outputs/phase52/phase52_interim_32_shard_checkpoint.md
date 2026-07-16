# Phase52 Interim Checkpoint: Dense Replay First 32 Shards

Generated: 2026-07-17 05:08 IST

## Scope

This is the fourth interim evidence checkpoint for the Phase52 full-year dense synthetic L2 strategy replay.
The live replay continues from `outputs/phase52/dense_replay_daily_symbol.csv`; this note freezes the first 32-shard partial summary.

## Replay progress

| Metric | Value |
|---|---:|
| Dense input shards | 384 |
| Shards replayed in this checkpoint | 32 |
| Completion | 8.33% |
| Aggregated dense tick trade count | 233,825,437 |
| Strategy/profile result rows | 9 |
| Positive after-cost rows | 0 |
| Synthetic candidate rows | 0 |
| Replay elapsed seconds | 14,811.200223 |
| Zerodha cost model version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| Acceptance ready | 0 |

## Interim strategy/profile ranking

All first-32-shard strategy/profile combinations remain negative after costs.

| Strategy | Execution profile | Trades | Annualized net P&L INR | Sharpe-like proxy | Candidate |
|---|---|---:|---:|---:|---|
| DENSE_S01_L1_IMBALANCE | zero_latency_spread_only_control | 26,414,873 | -434,859,293.80 | -9.210381 | False |
| DENSE_S03_1T_MOMENTUM | zero_latency_spread_only_control | 25,999,275 | -583,817,395.25 | -5.777909 | False |
| DENSE_S02_MICROPRICE | zero_latency_spread_only_control | 26,142,868 | -634,579,496.58 | -8.100127 | False |
| DENSE_S01_L1_IMBALANCE | retail_marketable_default | 26,127,227 | -3,578,289,136.55 | -11.425696 | False |
| DENSE_S03_1T_MOMENTUM | retail_marketable_default | 25,699,418 | -3,984,358,919.79 | -6.081708 | False |
| DENSE_S02_MICROPRICE | retail_marketable_default | 25,807,577 | -4,140,856,359.14 | -6.960945 | False |
| DENSE_S01_L1_IMBALANCE | stressed_retail | 26,127,201 | -4,827,424,534.99 | -11.099413 | False |
| DENSE_S03_1T_MOMENTUM | stressed_retail | 25,699,421 | -5,523,700,260.33 | -6.034681 | False |
| DENSE_S02_MICROPRICE | stressed_retail | 25,807,577 | -5,779,412,235.66 | -6.931338 | False |

## Interpretation

This checkpoint does not close Phase52 because only 32 of 384 dense shards have completed.
It extends the first-8, first-16, and first-24 shard evidence: the first-pass dense signal catalog continues to show no synthetic-only after-cost edge.

Acceptance remains closed because there are zero positive-after-cost strategy/profile rows and zero synthetic candidate rows.

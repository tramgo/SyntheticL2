# Phase52 Interim Checkpoint: Dense Replay First 16 Shards

Generated: 2026-07-17 02:33 IST

## Scope

This is the second interim evidence checkpoint for the Phase52 full-year dense synthetic L2 strategy replay.
The live replay continues from `outputs/phase52/dense_replay_daily_symbol.csv`; this note freezes the first 16-shard partial summary.

## Replay progress

| Metric | Value |
|---|---:|
| Dense input shards | 384 |
| Shards replayed in this checkpoint | 16 |
| Completion | 4.17% |
| Aggregated dense tick trade count | 116,777,364 |
| Strategy/profile result rows | 9 |
| Positive after-cost rows | 0 |
| Synthetic candidate rows | 0 |
| Replay elapsed seconds | 5,498.220818 |
| Zerodha cost model version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| Acceptance ready | 0 |

## Interim strategy/profile ranking

All first-16-shard strategy/profile combinations remain negative after costs.

| Strategy | Execution profile | Trades | Annualized net P&L INR | Sharpe-like proxy | Candidate |
|---|---|---:|---:|---:|---|
| DENSE_S01_L1_IMBALANCE | zero_latency_spread_only_control | 13,140,951 | -217,045,264.93 | -9.575117 | False |
| DENSE_S03_1T_MOMENTUM | zero_latency_spread_only_control | 12,997,703 | -305,364,077.89 | -5.572454 | False |
| DENSE_S02_MICROPRICE | zero_latency_spread_only_control | 13,070,447 | -325,642,009.54 | -12.941180 | False |
| DENSE_S01_L1_IMBALANCE | retail_marketable_default | 13,000,110 | -1,782,678,696.18 | -11.660044 | False |
| DENSE_S03_1T_MOMENTUM | retail_marketable_default | 12,862,378 | -2,034,355,280.40 | -5.859896 | False |
| DENSE_S02_MICROPRICE | retail_marketable_default | 12,921,650 | -2,097,896,844.58 | -11.398773 | False |
| DENSE_S01_L1_IMBALANCE | stressed_retail | 13,000,102 | -2,405,703,210.67 | -11.357314 | False |
| DENSE_S03_1T_MOMENTUM | stressed_retail | 12,862,373 | -2,831,617,944.71 | -5.814183 | False |
| DENSE_S02_MICROPRICE | stressed_retail | 12,921,650 | -2,934,664,451.68 | -11.336561 | False |

## Interpretation

This checkpoint does not close Phase52 because only 16 of 384 dense shards have completed.
It does strengthen the interim conclusion from the 8-shard checkpoint: the first-pass dense signal catalog is not showing a synthetic-only after-cost edge.

Acceptance remains closed because there are zero positive-after-cost strategy/profile rows and zero synthetic candidate rows.

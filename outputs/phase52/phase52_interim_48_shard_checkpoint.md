# Phase52 Interim Checkpoint: Dense Replay First 48 Shards

Generated: 2026-07-17 08:06 IST

## Scope

This is the sixth interim evidence checkpoint for the Phase52 full-year dense synthetic L2 strategy replay.
The live replay continues from `outputs/phase52/dense_replay_daily_symbol.csv`; this note freezes the first 48-shard partial summary.

## Replay progress

| Metric | Value |
|---|---:|
| Dense input shards | 384 |
| Shards replayed in this checkpoint | 48 |
| Completion | 12.50% |
| Aggregated dense tick trade count | 339,759,464 |
| Strategy/profile result rows | 9 |
| Positive after-cost rows | 0 |
| Synthetic candidate rows | 0 |
| Replay elapsed seconds | 25,425.337118 |
| Zerodha cost model version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| Acceptance ready | 0 |

## Interim strategy/profile ranking

All first-48-shard strategy/profile combinations remain negative after costs.

| Strategy | Execution profile | Trades | Annualized net P&L INR | Sharpe-like proxy | Candidate |
|---|---|---:|---:|---:|---|
| DENSE_S01_L1_IMBALANCE | zero_latency_spread_only_control | 38,336,641 | -661,021,977.68 | -9.448830 | False |
| DENSE_S03_1T_MOMENTUM | zero_latency_spread_only_control | 37,800,656 | -897,957,486.57 | -5.788968 | False |
| DENSE_S02_MICROPRICE | zero_latency_spread_only_control | 38,027,114 | -952,137,958.21 | -7.403562 | False |
| DENSE_S01_L1_IMBALANCE | retail_marketable_default | 37,906,184 | -5,280,613,214.22 | -11.227117 | False |
| DENSE_S03_1T_MOMENTUM | retail_marketable_default | 37,348,300 | -5,935,798,080.18 | -5.950501 | False |
| DENSE_S02_MICROPRICE | retail_marketable_default | 37,543,083 | -6,110,757,089.32 | -6.743387 | False |
| DENSE_S01_L1_IMBALANCE | stressed_retail | 37,906,146 | -7,152,589,171.11 | -10.947395 | False |
| DENSE_S03_1T_MOMENTUM | stressed_retail | 37,348,271 | -8,269,906,259.76 | -5.926122 | False |
| DENSE_S02_MICROPRICE | stressed_retail | 37,543,069 | -8,552,619,991.96 | -6.727177 | False |

## Interpretation

This checkpoint does not close Phase52 because only 48 of 384 dense shards have completed.
It extends the first-8 through first-40 shard evidence: the first-pass dense signal catalog continues to show no synthetic-only after-cost edge.

Acceptance remains closed because there are zero positive-after-cost strategy/profile rows and zero synthetic candidate rows.

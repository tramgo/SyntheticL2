# Phase52 Interim Checkpoint: Dense Replay First 56 Shards

Generated: 2026-07-17 09:50 IST

## Scope

This is the seventh interim evidence checkpoint for the Phase52 full-year dense synthetic L2 strategy replay.
The live replay continues from `outputs/phase52/dense_replay_daily_symbol.csv`; this note freezes the first 56-shard partial summary.

## Replay progress

| Metric | Value |
|---|---:|
| Dense input shards | 384 |
| Shards replayed in this checkpoint | 56 |
| Completion | 14.58% |
| Aggregated dense tick trade count | 393,062,360 |
| Strategy/profile result rows | 9 |
| Positive after-cost rows | 0 |
| Synthetic candidate rows | 0 |
| Replay elapsed seconds | 31,614.360173 |
| Zerodha cost model version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| Acceptance ready | 0 |

## Interim strategy/profile ranking

All first-56-shard strategy/profile combinations remain negative after costs.

| Strategy | Execution profile | Trades | Annualized net P&L INR | Sharpe-like proxy | Candidate |
|---|---|---:|---:|---:|---|
| DENSE_S01_L1_IMBALANCE | zero_latency_spread_only_control | 44,371,752 | -773,739,621.12 | -9.714736 | False |
| DENSE_S03_1T_MOMENTUM | zero_latency_spread_only_control | 43,703,155 | -1,046,066,650.57 | -6.108896 | False |
| DENSE_S02_MICROPRICE | zero_latency_spread_only_control | 43,968,177 | -1,114,191,539.60 | -8.072131 | False |
| DENSE_S01_L1_IMBALANCE | retail_marketable_default | 43,881,788 | -6,139,131,757.34 | -11.804114 | False |
| DENSE_S03_1T_MOMENTUM | retail_marketable_default | 43,187,419 | -6,887,477,140.98 | -6.291059 | False |
| DENSE_S02_MICROPRICE | retail_marketable_default | 43,440,497 | -7,110,235,694.45 | -7.312740 | False |
| DENSE_S01_L1_IMBALANCE | stressed_retail | 43,881,742 | -8,323,704,408.48 | -11.493182 | False |
| DENSE_S03_1T_MOMENTUM | stressed_retail | 43,187,371 | -9,602,293,305.14 | -6.263144 | False |
| DENSE_S02_MICROPRICE | stressed_retail | 43,440,459 | -9,962,111,251.73 | -7.296897 | False |

## Interpretation

This checkpoint does not close Phase52 because only 56 of 384 dense shards have completed.
It extends the first-8 through first-48 shard evidence: the first-pass dense signal catalog continues to show no synthetic-only after-cost edge.

Acceptance remains closed because there are zero positive-after-cost strategy/profile rows and zero synthetic candidate rows.

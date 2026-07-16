# Phase52 Interim Checkpoint: Dense Replay First 8 Shards

Generated: 2026-07-17 01:35 IST

## Scope

This is an interim evidence checkpoint for the Phase52 full-year dense synthetic L2 strategy replay.
The live replay continues from `outputs/phase52/dense_replay_daily_symbol.csv`; this note freezes the first 8-shard summary so the milestone can be reviewed and versioned without waiting for all 384 shards.

## Replay progress

| Metric | Value |
|---|---:|
| Dense input shards | 384 |
| Shards replayed in this checkpoint | 8 |
| Completion | 2.08% |
| Aggregated dense tick trade count | 58,416,838 |
| Strategy/profile result rows | 9 |
| Positive after-cost rows | 0 |
| Synthetic candidate rows | 0 |
| Zerodha cost model version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| Acceptance ready | 0 |

## Interim strategy/profile ranking

All first-8-shard strategy/profile combinations are negative after costs.

| Strategy | Execution profile | Trades | Annualized net P&L INR | Sharpe-like proxy | Candidate |
|---|---|---:|---:|---:|---|
| DENSE_S01_L1_IMBALANCE | zero_latency_spread_only_control | 6,579,424 | -120,794,166.49 | -11.058371 | False |
| DENSE_S03_1T_MOMENTUM | zero_latency_spread_only_control | 6,494,848 | -170,128,761.75 | -5.562909 | False |
| DENSE_S02_MICROPRICE | zero_latency_spread_only_control | 6,535,151 | -175,780,810.83 | -14.925121 | False |
| DENSE_S01_L1_IMBALANCE | retail_marketable_default | 6,508,024 | -928,973,397.63 | -11.322354 | False |
| DENSE_S03_1T_MOMENTUM | retail_marketable_default | 6,431,943 | -1,069,425,502.85 | -5.919804 | False |
| DENSE_S02_MICROPRICE | retail_marketable_default | 6,463,736 | -1,087,738,123.44 | -13.182695 | False |
| DENSE_S01_L1_IMBALANCE | stressed_retail | 6,508,032 | -1,265,355,770.74 | -11.069718 | False |
| DENSE_S03_1T_MOMENTUM | stressed_retail | 6,431,938 | -1,502,855,554.36 | -5.859343 | False |
| DENSE_S02_MICROPRICE | stressed_retail | 6,463,742 | -1,531,812,854.72 | -13.050132 | False |

## Interpretation

This checkpoint does not close Phase52 because only 8 of 384 dense shards have completed.
It does, however, confirm that the full replay path is executing over the dense tick lake, applying the configured strategy signals, latency profiles, Zerodha-style cost model, and candidate gates.

At this checkpoint, even the zero-latency spread-only controls are negative. That is useful evidence: the first-pass dense signal catalog is not showing a trivial synthetic-only edge after spread/cost accounting.

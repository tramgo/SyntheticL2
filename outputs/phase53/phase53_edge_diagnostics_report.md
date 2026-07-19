# Phase53 Edge Diagnostics

Generated UTC: 2026-07-19T18:32:02.206603+00:00

Source: `outputs\phase52\dense_replay_daily_symbol.csv`

Phase53 pauses the Phase52 brute-force shard replay and diagnoses whether the current dense tick-level signal catalog has any evidence of edge.

## Summary

| metric | value | description |
| --- | --- | --- |
| phase53_phase52_shards_observed | 116 | Unique Phase52 dense shards in the checkpoint ledger |
| phase53_phase52_max_shard_index | 116 | Highest shard index observed in the checkpoint ledger |
| phase53_dense_trade_rows_observed | 826538294 | Aggregated dense tick trade count in the checkpoint ledger |
| phase53_strategy_profile_rows | 9 | Strategy/profile rows analyzed |
| phase53_profitable_strategy_profiles | 0 | Aggregate strategy/profile rows with positive net P&L |
| phase53_positive_daily_symbol_rows | 0 | Daily-symbol strategy/profile rows with positive net P&L |
| phase53_gross_positive_strategy_profiles | 3 | Aggregate strategy/profile rows with positive gross return before costs |
| phase53_positive_gross_daily_symbol_rows | 3116 | Daily-symbol rows with positive gross return before costs |
| phase53_best_net_daily_symbol_pnl_inr | -201.0034256410256 | Best single daily-symbol net P&L row |
| phase53_best_net_daily_symbol_key | 2026-02-10|GOLDBEES|DENSE_S01_L1_IMBALANCE|retail_marketable_default | Best single daily-symbol row key |
| phase53_recommend_continue_phase52_bruteforce | 0 | 0 means pause brute-force shard replay and pivot to edge diagnostics/design |

## Strategy/Profile Diagnostics

| strategy_id | execution_profile | trades | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | positive_net_rows | positive_gross_rows | profitable_after_cost | gross_positive_total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DENSE_S01_L1_IMBALANCE | zero_latency_spread_only_control | 93466441 | -1608587550.5717995 | -3115016.1805510297 | 1605472534.3913167 | 0 | 622 | False | False |
| DENSE_S03_1T_MOMENTUM | zero_latency_spread_only_control | 91831765 | -2151640734.383605 | 87563.9513967089 | 2151728298.334946 | 0 | 286 | False | True |
| DENSE_S02_MICROPRICE | zero_latency_spread_only_control | 92356378 | -2288846947.130142 | -1332121.2816695094 | 2287514825.8480535 | 0 | 120 | False | False |
| DENSE_S01_L1_IMBALANCE | retail_marketable_default | 92446850 | -12870728903.147472 | -3004910.9264933188 | 12867723992.22022 | 0 | 633 | False | False |
| DENSE_S03_1T_MOMENTUM | retail_marketable_default | 90713975 | -14330527479.386763 | 204304.7492744735 | 14330731784.133919 | 0 | 292 | False | True |
| DENSE_S02_MICROPRICE | retail_marketable_default | 91281178 | -14789121797.213419 | -1304245.02062087 | 14787817552.191917 | 0 | 121 | False | False |
| DENSE_S01_L1_IMBALANCE | stressed_retail | 92446768 | -17431991310.889385 | -3004910.9264933188 | 17428986399.961536 | 0 | 633 | False | False |
| DENSE_S03_1T_MOMENTUM | stressed_retail | 90713907 | -19942398951.052666 | 203892.07594160305 | 19942602843.128613 | 0 | 288 | False | True |
| DENSE_S02_MICROPRICE | stressed_retail | 91281032 | -20681076545.048107 | -1304245.02062087 | 20679772300.027527 | 0 | 121 | False | False |

## Decision

The current dense replay catalog has no positive after-cost strategy/profile rows and no positive daily-symbol net rows in the observed checkpoint ledger.
Continuing the same shard-by-shard replay is low-value until the strategy catalog changes.
The next best action is to design lower-turnover and more selective variants, then replay those against a bounded shard set before spending compute on the full dense lake.
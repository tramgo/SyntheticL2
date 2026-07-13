# Phase 12 Event-Driven Backtester Report

Generated UTC: 2026-07-13T20:19:10.050864+00:00

## Scope

This artifact exercises an event-driven order lifecycle over the Phase 12 sampled trade ledger.
It covers market orders, marketable limits, passive-limit proxies, cancel/replace, partial fills and rejection scenarios.
It is still proxy evidence: no individual exchange order identity, queue priority or passive-fill truth is claimed.

## Order Model Counts

| order_model | orders |
| --- | --- |
| market_order | 2351 |
| marketable_limit_order | 1908 |
| passive_limit_order | 738 |
| cancel_replace | 699 |
| partial_fill | 526 |
| rejection_scenario | 258 |

## Order Summary

| order_model | order_status | orders | mean_fill_ratio | total_filled_qty | mean_event_net_return | total_event_net_pnl_units |
| --- | --- | --- | --- | --- | --- | --- |
| cancel_replace | FILLED | 653 | 1 | 653 | -0.000772397 | -0.504375 |
| cancel_replace | REJECTED_OR_CANCELLED | 46 | 0 | 0 | 0 | 0 |
| market_order | FILLED | 2351 | 1 | 2351 | -0.0018867 | -4.43564 |
| marketable_limit_order | FILLED | 1793 | 1 | 1793 | -0.00104515 | -1.87396 |
| marketable_limit_order | REJECTED_OR_CANCELLED | 115 | 0 | 0 | 0 | 0 |
| partial_fill | FILLED | 526 | 0.45 | 236.7 | -0.000480177 | -0.252573 |
| passive_limit_order | FILLED | 738 | 0.65 | 479.7 | -0.00147185 | -1.08622 |
| rejection_scenario | REJECTED_OR_CANCELLED | 258 | 0 | 0 | 0 | 0 |

## Outputs

- `event_backtest_order_trace.parquet` (local/generated analytical trace)
- `event_backtest_order_summary.csv`
- `event_backtest_pnl_trace.csv`
- `order_model_catalog.csv`
- `slippage_model_catalog.csv`
- `event_backtest_manifest.json`

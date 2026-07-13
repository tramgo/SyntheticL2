# Phase 12 Event-Driven Backtester Report

Generated UTC: 2026-07-13T21:14:41.065400+00:00

## Scope

This artifact exercises an event-driven order lifecycle over the Phase 12 sampled trade ledger.
It covers market orders, marketable limits, passive-limit proxies, cancel/replace, partial fills and rejection scenarios.
It is still proxy evidence: no individual exchange order identity, queue priority or passive-fill truth is claimed.

## Order Model Counts

| order_model | orders |
| --- | --- |
| market_order | 2337 |
| marketable_limit_order | 1906 |
| passive_limit_order | 757 |
| cancel_replace | 723 |
| partial_fill | 515 |
| rejection_scenario | 242 |

## Order Summary

| order_model | order_status | orders | mean_fill_ratio | total_filled_qty | mean_event_net_return | total_event_net_pnl_units |
| --- | --- | --- | --- | --- | --- | --- |
| cancel_replace | FILLED | 669 | 1 | 669 | -0.00201849 | -1.35037 |
| cancel_replace | REJECTED_OR_CANCELLED | 54 | 0 | 0 | 0 | 0 |
| market_order | FILLED | 2337 | 1 | 2337 | -0.00136143 | -3.18167 |
| marketable_limit_order | FILLED | 1783 | 1 | 1783 | -0.000971305 | -1.73184 |
| marketable_limit_order | REJECTED_OR_CANCELLED | 123 | 0 | 0 | 0 | 0 |
| partial_fill | FILLED | 515 | 0.45 | 231.75 | -0.000359627 | -0.185208 |
| passive_limit_order | FILLED | 757 | 0.65 | 492.05 | -0.00136966 | -1.03683 |
| rejection_scenario | REJECTED_OR_CANCELLED | 242 | 0 | 0 | 0 | 0 |

## Outputs

- `event_backtest_order_trace.parquet` (local/generated analytical trace)
- `event_backtest_order_summary.csv`
- `event_backtest_pnl_trace.csv`
- `order_model_catalog.csv`
- `slippage_model_catalog.csv`
- `event_backtest_manifest.json`

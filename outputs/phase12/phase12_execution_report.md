# Phase 12 Backtest and Execution Simulator Report

Generated UTC: 2026-07-13T15:26:01.338288+00:00

## Scope

This is an event-driven execution-simulator smoke run over received synthetic L2 feed events.
It validates the event lifecycle and execution accounting shape; it does not validate or promote any strategy.
Cost rows use current Zerodha equity intraday charge formulas where explicit, with source URLs recorded in `cost_schedule.csv`.

## Summary

- feed_profile: normal_retail
- input_events: 50000
- candidate_signals: 100
- orders_emitted: 100
- filled_orders: 99
- partial_or_rejected_orders: 1
- symbols: 5
- decision_latency_ms: 100
- broker_latency_ms: 200
- order_model: marketable_limit_order
- slippage_model: depth_consuming_book_walk
- total_charges: 514.0570180487125
- total_brokerage: 242.24744999977952
- total_stt: 198.0
- total_transaction_charge: 24.789989049977436
- total_sebi_charge: 0.8074914999992652
- total_gst: 48.21208749895612
- total_stamp: 0.0
- ending_mark_to_market_pnl: -813.0570180480136
- promotion_allowed: False
- evidence_label: phase12_execution_plumbing_smoke_only

## Order Status

| status | orders |
| --- | --- |
| FILLED | 99 |
| REJECTED_OR_CANCELLED | 1 |

## Event Lifecycle Covered

synthetic feed event -> strategy feature update -> signal decision -> decision latency -> order submission -> broker/network latency -> order arrival -> fill simulation -> partial/reject handling -> charges -> P&L/risk update

## Outputs

- `backtest_order_trace.parquet`
- `backtest_pnl_trace.csv`
- `execution_summary.csv`
- `order_model_catalog.csv`
- `slippage_model_catalog.csv`
- `cost_schedule.csv`
- `execution_manifest.json`

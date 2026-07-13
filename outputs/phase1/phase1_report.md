# Phase 1 Received-Tick Feature Report

Generated UTC: 2026-07-13T14:14:58.349858+00:00
Input directory: `outputs\stage_a1\compact_ticks_by_symbol`
Output directory: `outputs\phase1`

## Scope

This phase normalizes the Stage A1 compact received-tick stream and derives consecutive received-tick deltas.
Derived add/cancel/aggressor fields remain inference labels, not direct exchange-order observations.

## Inventory

- Symbols processed: 32
- Rows processed: 620853
- Symbols with volume reversals: 0
- Symbols with 15s stale gaps: 32

## Outputs

- `normalized_ticks_by_symbol/symbol=*/normalized_ticks.parquet`
- `received_tick_deltas_by_symbol/symbol=*/received_tick_deltas.parquet`
- `phase1_feature_summary.csv`

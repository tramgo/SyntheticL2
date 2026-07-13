# Phase 12 Order Lifecycle and Risk Proxy Report

Generated UTC: 2026-07-13T18:57:40.420629+00:00

## Scope

This layer adds deterministic partial-fill, queue-position bucket and risk-control proxy evidence over the Phase 12 sampled trade ledger.
It is not exchange queue truth and must not be used as acceptance-grade passive-fill validation.

Lifecycle rows: 750000

## Fill Model Summary

| fill_model | strategy_profiles | mean_fill_ratio | partial_fill_fraction | no_fill_fraction |
| --- | --- | --- | --- | --- |
| neutral_partial | 2 | 0.724614 | 1 | 0 |
| optimistic_marketable | 2 | 0.991635 | 0.162787 | 0 |
| pessimistic_partial | 2 | 0.407446 | 1 | 0 |

## Risk Summary

| fill_model | strategy_profiles | max_drawdown_units | position_limit_breach_rows | daily_loss_limit_breach_rows |
| --- | --- | --- | --- | --- |
| neutral_partial | 2 | -55.8545 | 198446 | 155804 |
| optimistic_marketable | 2 | -74.4726 | 209610 | 158789 |
| pessimistic_partial | 2 | -33.5127 | 169625 | 145265 |

## Risk Limits

```json
{
  "daily_loss_limit_units": -0.75,
  "drawdown_warn_units": -1.0,
  "max_abs_position_units": 15.0,
  "tail_loss_quantile": 0.01
}
```

# Phase 12 Order Lifecycle and Risk Proxy Report

Generated UTC: 2026-07-13T20:24:49.895217+00:00

## Scope

This layer adds deterministic partial-fill, queue-position bucket and risk-control proxy evidence over the Phase 12 sampled trade ledger.
It is not exchange queue truth and must not be used as acceptance-grade passive-fill validation.

Lifecycle rows: 749979

## Fill Model Summary

| fill_model | strategy_profiles | mean_fill_ratio | partial_fill_fraction | no_fill_fraction |
| --- | --- | --- | --- | --- |
| neutral_partial | 27 | 0.704458 | 1 | 0 |
| optimistic_marketable | 27 | 0.985887 | 0.290652 | 0 |
| pessimistic_partial | 27 | 0.371428 | 1 | 0 |

## Risk Summary

| fill_model | strategy_profiles | max_drawdown_units | position_limit_breach_rows | daily_loss_limit_breach_rows |
| --- | --- | --- | --- | --- |
| neutral_partial | 27 | -5.88735 | 81771 | 8922 |
| optimistic_marketable | 27 | -9.76114 | 105776 | 16669 |
| pessimistic_partial | 27 | -2.08648 | 45463 | 1957 |

## Risk Limits

```json
{
  "daily_loss_limit_units": -0.75,
  "drawdown_warn_units": -1.0,
  "max_abs_position_units": 15.0,
  "tail_loss_quantile": 0.01
}
```

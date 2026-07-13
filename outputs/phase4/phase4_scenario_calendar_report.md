# Phase 4 Synthetic Scenario Calendar Report

Generated UTC: 2026-07-13T20:30:12.862684+00:00

## Scope

This phase creates deterministic synthetic-quarter scenario calendars.
It designs regime coverage and stress conditions; it does not generate prices, books or strategy results.

## Observed Anchor

- Observed one-day candidate regime: D04 / Gradual bullish trend
- Evidence label: one_day_candidate_not_promotable

## Profile Summary

| quarter_profile | days | unique_regimes | gap_days | market_shock_days | event_cluster_days | avg_vol_multiplier | avg_event_rate_multiplier | avg_spread_multiplier | avg_depth_multiplier | avg_correlation_multiplier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-A | 63 | 18 | 8 | 7 | 5 | 1.257936507936508 | 1.1261904761904762 | 1.119047619047619 | 0.9341269841269841 | 1.0603174603174603 |
| Q-B | 63 | 18 | 8 | 10 | 6 | 1.2873015873015872 | 1.1500000000000001 | 1.1039682539682538 | 0.9380952380952381 | 1.0722222222222222 |
| Q-C | 63 | 18 | 8 | 8 | 6 | 1.3984126984126983 | 1.184920634920635 | 1.2087301587301589 | 0.8936507936507936 | 1.107936507936508 |

## Outputs

- `scenario_calendar.csv`
- `scenario_calendar.jsonl`
- `regime_mix_summary.csv`
- `profile_summary.csv`
- `scenario_manifest.json`

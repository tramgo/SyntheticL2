# Phase 7 Shock Library Report

Generated UTC: 2026-07-13T14:47:46.168630+00:00

## Scope

This phase generates a synthetic shock/event schedule with required L2 effects and counterfactual variants.
It does not yet mutate the Phase 6 book-state stream; Phase 8+ can consume these events.

## Validation

- shock_events: 1504
- market_events: 200
- ticker_events: 1304
- counterfactual_groups: 366
- scenario_days: 56
- target_symbols: 32
- variants: 5
- null_required_effect_rows: 0
- invalid_duration_rows: 0

## Top Shock-Type Rows

| scope | shock_type | variant | events | median_abs_jump_bps | median_volatility_multiplier | median_spread_multiplier |
| --- | --- | --- | --- | --- | --- | --- |
| ticker | earnings_miss | quick_recovery | 41 | 93.534 | 3.7821 | 2.8047 |
| ticker | earnings_miss | positive_shock | 41 | 114.4614 | 3.887 | 2.8352 |
| ticker | earnings_miss | negative_shock | 41 | 89.9103 | 3.562 | 2.5476 |
| ticker | earnings_miss | continuation | 41 | 90.6797 | 3.6899 | 2.707 |
| ticker | guidance_change | continuation | 40 | 100.74889999999999 | 3.80555 | 2.5545999999999998 |
| ticker | guidance_change | negative_shock | 40 | 100.01265000000001 | 3.8171 | 2.8916500000000003 |
| ticker | guidance_change | positive_shock | 40 | 92.13419999999999 | 3.6923500000000002 | 2.81245 |
| ticker | guidance_change | quick_recovery | 40 | 97.28005 | 3.8693 | 2.46335 |
| ticker | earnings_beat | continuation | 39 | 111.7744 | 3.5771 | 2.5612 |
| ticker | earnings_beat | negative_shock | 39 | 106.1 | 3.6822 | 2.7819 |
| ticker | earnings_beat | positive_shock | 39 | 116.0038 | 4.2672 | 2.7104 |
| ticker | earnings_beat | quick_recovery | 39 | 112.2439 | 3.7101 | 2.6109 |

## Most Populated Scenario Days

| quarter_profile | scenario_day | trade_date | regime_code | events | market_events | ticker_events | targets |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q-A | 42 | 2026-09-09 | D07 | 73 | 5 | 68 | ADANIPORTS|BAJAJ-AUTO|BANKBEES|BHARTIARTL|BPCL|BRITANNIA|CIPLA|DRREDDY|GOLDBEES|HINDUNILVR|ITBEES|ITC|JUNIORBEES|KOTAKBANK|NESTLEIND|ONGC|SUNPHARMA |
| Q-C | 63 | 2026-10-08 | D07 | 73 | 5 | 68 | ADANIPORTS|BAJAJ-AUTO|BANKBEES|BHARTIARTL|BPCL|BRITANNIA|CIPLA|DRREDDY|GOLDBEES|HINDUNILVR|ITBEES|ITC|JUNIORBEES|KOTAKBANK|NESTLEIND|ONGC|SUNPHARMA |
| Q-C | 3 | 2026-07-16 | D07 | 73 | 5 | 68 | ADANIPORTS|BAJAJ-AUTO|BANKBEES|BHARTIARTL|BPCL|BRITANNIA|CIPLA|DRREDDY|GOLDBEES|HINDUNILVR|ITBEES|ITC|JUNIORBEES|KOTAKBANK|NESTLEIND|ONGC|SUNPHARMA |
| Q-B | 54 | 2026-09-25 | D20 | 73 | 5 | 68 | ADANIPORTS|BAJAJ-AUTO|BANKBEES|BHARTIARTL|BPCL|BRITANNIA|CIPLA|DRREDDY|GOLDBEES|HINDUNILVR|ITBEES|ITC|JUNIORBEES|KOTAKBANK|NESTLEIND|ONGC|SUNPHARMA |
| Q-C | 42 | 2026-09-09 | D20 | 61 | 5 | 56 | ADANIPORTS|BAJAJ-AUTO|BANKBEES|BHARTIARTL|BPCL|BRITANNIA|CIPLA|DRREDDY|GOLDBEES|HINDUNILVR|ITBEES|ITC|JUNIORBEES|KOTAKBANK |
| Q-A | 52 | 2026-09-23 | D07 | 61 | 5 | 56 | ADANIPORTS|BAJAJ-AUTO|BANKBEES|BHARTIARTL|BPCL|BRITANNIA|CIPLA|DRREDDY|GOLDBEES|HINDUNILVR|ITBEES|ITC|JUNIORBEES|KOTAKBANK |
| Q-C | 35 | 2026-08-31 | D07 | 61 | 5 | 56 | ADANIPORTS|BAJAJ-AUTO|BANKBEES|BHARTIARTL|BPCL|BRITANNIA|CIPLA|DRREDDY|GOLDBEES|HINDUNILVR|ITBEES|ITC|JUNIORBEES|KOTAKBANK |
| Q-A | 5 | 2026-07-20 | D07 | 57 | 5 | 52 | ADANIPORTS|BAJAJ-AUTO|BANKBEES|BHARTIARTL|BPCL|BRITANNIA|CIPLA|DRREDDY|GOLDBEES|HINDUNILVR|ITBEES|ITC|JUNIORBEES |
| Q-C | 28 | 2026-08-20 | D07 | 53 | 5 | 48 | ADANIPORTS|BAJAJ-AUTO|BANKBEES|BHARTIARTL|BPCL|BRITANNIA|CIPLA|DRREDDY|GOLDBEES|HINDUNILVR|ITBEES|ITC |
| Q-C | 52 | 2026-09-23 | D07 | 53 | 5 | 48 | ADANIPORTS|BAJAJ-AUTO|BANKBEES|BHARTIARTL|BPCL|BRITANNIA|CIPLA|DRREDDY|GOLDBEES|HINDUNILVR|ITBEES|ITC |
| Q-C | 13 | 2026-07-30 | D07 | 49 | 5 | 44 | ADANIPORTS|BAJAJ-AUTO|BANKBEES|BHARTIARTL|BPCL|BRITANNIA|CIPLA|DRREDDY|GOLDBEES|HINDUNILVR|ITBEES |
| Q-A | 39 | 2026-09-04 | D13 | 45 | 5 | 40 | ADANIPORTS|BAJAJ-AUTO|BANKBEES|BHARTIARTL|BPCL|BRITANNIA|CIPLA|DRREDDY|GOLDBEES|HINDUNILVR |

## Outputs

- `shock_library.csv`
- `shock_library.jsonl`
- `shock_type_summary.csv`
- `shock_day_summary.csv`
- `shock_library_manifest.json`

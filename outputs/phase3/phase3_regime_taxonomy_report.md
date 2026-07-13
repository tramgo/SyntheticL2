# Phase 3 Regime Taxonomy Report

Generated UTC: 2026-07-13T14:23:20.124572+00:00

## Scope

This phase assigns one-day candidate daily, intraday and ticker-specific regime labels.
Labels are engineering inputs for scenario design, not statistically validated regime claims.

## Daily Candidate

| trade_date | daily_regime_code | daily_regime | classification_reason | median_symbol_return | return_iqr | five_second_pairwise_corr_median | intraday_bins | stale_or_feed_state_fraction | liquidity_withdrawal_state_fraction | evidence_label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-13 | D04 | Gradual bullish trend | positive median cross-symbol drift | 0.006497786986579435 | 0.023934162940476122 | 0.0435225114177554 | 77 | 0.025974025974025976 | 0.0 | one_day_candidate_not_promotable |

## Intraday State Counts

| intraday_state | bins |
| --- | --- |
| I04 | 73 |
| I01 | 2 |
| I18 | 2 |

## Ticker-State Counts

| ticker_state | symbols |
| --- | --- |
| illiquid/stale | 15 |
| market follower | 7 |
| high-beta follower | 7 |
| spread stress | 2 |
| laggard | 1 |

## Outputs

- `daily_regime_observation.csv`
- `intraday_market_states.csv`
- `ticker_state_profile.csv`
- `symbol_intraday_features.csv`
- `regime_manifest.json`

# Phase73 Timestamp Alignment and Shock-Panel Audit

Generated UTC: 2026-07-19T19:55:22.375157+00:00

Phase73 audits the two Phase72 near-misses before any replay expansion.
It rechecks HDFCBANK cross-symbol lead-lag with timestamp-aligned bars and audits shock scenario coverage across bounded dense shards.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase73_symbols_loaded | 32 | Symbols loaded for timestamp matrix |
| phase73_timestamp_bar_rows | 192 | Timestamp-aligned symbol bar rows |
| phase73_hdfcbank_recheck_positive | 1 | 1 means HDFCBANK lead-lag near-miss remains positive under timestamp alignment |
| phase73_hdfcbank_recheck_passes_gate | 0 | 1 means timestamp-aligned HDFCBANK recheck passes quality gates |
| phase73_shock_months_audited | 4 | Trade-month partitions included in shock-panel audit |
| phase73_balanced_shock_months | 1 | Months with broad market shock or meaningful symbol-shock coverage |
| phase73_allow_replay_expansion | 0 | 1 means near-miss replay expansion is allowed |
| phase73_elapsed_seconds | 15.9494 | Elapsed seconds |
| phase73_recommend_next_action | generator_alignment_remediation_plan | Recommended next action |

## HDFCBANK Timestamp Recheck

| rule_id | phase70_reference_rule_id | leader_symbol | alignment | threshold | trades | target_symbols | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | precision_cost_clear | positive_target_fraction | cost_drag_to_abs_gross_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P73_TIMESTAMP_HDFCBANK_MOMENTUM_Q70_RECHECK | P70_MEGA_HDFCBANK_MOMENTUM_Q70 | HDFCBANK | timestamp_bucket | 0.00428699 | 70 | 26 | 10434.6 | 18822.9 | 8388.26 | 0.471429 | 0.769231 | 0.445642 |

## Shock Panel Monthly

| trade_month | shard_count | symbols | row_count | market_shock_rows | symbol_shock_rows | market_shock_symbols | symbol_shock_symbols | regimes | feed_profiles | market_shock_symbol_fraction | symbol_shock_symbol_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | 32 | 32 | 8000000 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| 2026-02 | 32 | 32 | 8000000 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| 2026-03 | 32 | 32 | 8000000 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| 2026-04 | 32 | 32 | 8000000 | 8000000 | 250000 | 32 | 1 | 1 | 1 | 1 | 0.03125 |

## Shock Panel Detail Sample

| shard_index | trade_month | symbol | row_count | market_shock_rows | symbol_shock_rows | regime_count | dominant_regime_code | dominant_feed_profile | has_market_shock | has_symbol_shock |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-01 | ADANIPORTS | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 2 | 2026-01 | AXISBANK | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 3 | 2026-01 | BAJAJ-AUTO | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 4 | 2026-01 | BANKBEES | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 5 | 2026-01 | BHARTIARTL | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 6 | 2026-01 | BPCL | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 7 | 2026-01 | BRITANNIA | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 8 | 2026-01 | CIPLA | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 9 | 2026-01 | DRREDDY | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 10 | 2026-01 | GOLDBEES | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 11 | 2026-01 | HCLTECH | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 12 | 2026-01 | HDFCBANK | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 13 | 2026-01 | HINDUNILVR | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 14 | 2026-01 | ICICIBANK | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 15 | 2026-01 | INFY | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 16 | 2026-01 | ITBEES | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 17 | 2026-01 | ITC | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 18 | 2026-01 | JUNIORBEES | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 19 | 2026-01 | KOTAKBANK | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 20 | 2026-01 | LT | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 21 | 2026-01 | M&M | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 22 | 2026-01 | MARUTI | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 23 | 2026-01 | NESTLEIND | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 24 | 2026-01 | NIFTYBEES | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 25 | 2026-01 | ONGC | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 26 | 2026-01 | RELIANCE | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 27 | 2026-01 | SBIN | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 28 | 2026-01 | SUNPHARMA | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 29 | 2026-01 | TCS | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 30 | 2026-01 | TECHM | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 31 | 2026-01 | ULTRACEMCO | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 32 | 2026-01 | WIPRO | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 33 | 2026-02 | ADANIPORTS | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 34 | 2026-02 | AXISBANK | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 35 | 2026-02 | BAJAJ-AUTO | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 36 | 2026-02 | BANKBEES | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 37 | 2026-02 | BHARTIARTL | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 38 | 2026-02 | BPCL | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 39 | 2026-02 | BRITANNIA | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 40 | 2026-02 | CIPLA | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 41 | 2026-02 | DRREDDY | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 42 | 2026-02 | GOLDBEES | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 43 | 2026-02 | HCLTECH | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 44 | 2026-02 | HDFCBANK | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 45 | 2026-02 | HINDUNILVR | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 46 | 2026-02 | ICICIBANK | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 47 | 2026-02 | INFY | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 48 | 2026-02 | ITBEES | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 49 | 2026-02 | ITC | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 50 | 2026-02 | JUNIORBEES | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 51 | 2026-02 | KOTAKBANK | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 52 | 2026-02 | LT | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 53 | 2026-02 | M&M | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 54 | 2026-02 | MARUTI | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 55 | 2026-02 | NESTLEIND | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 56 | 2026-02 | NIFTYBEES | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 57 | 2026-02 | ONGC | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 58 | 2026-02 | RELIANCE | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 59 | 2026-02 | SBIN | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 60 | 2026-02 | SUNPHARMA | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 61 | 2026-02 | TCS | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 62 | 2026-02 | TECHM | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 63 | 2026-02 | ULTRACEMCO | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 64 | 2026-02 | WIPRO | 250000 | 0 | 0 | 1 | D04 | disconnect_scenario | False | False |
| 65 | 2026-03 | ADANIPORTS | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 66 | 2026-03 | AXISBANK | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 67 | 2026-03 | BAJAJ-AUTO | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 68 | 2026-03 | BANKBEES | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 69 | 2026-03 | BHARTIARTL | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 70 | 2026-03 | BPCL | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 71 | 2026-03 | BRITANNIA | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 72 | 2026-03 | CIPLA | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 73 | 2026-03 | DRREDDY | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 74 | 2026-03 | GOLDBEES | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 75 | 2026-03 | HCLTECH | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 76 | 2026-03 | HDFCBANK | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 77 | 2026-03 | HINDUNILVR | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 78 | 2026-03 | ICICIBANK | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 79 | 2026-03 | INFY | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |
| 80 | 2026-03 | ITBEES | 250000 | 0 | 0 | 1 | D06 | disconnect_scenario | False | False |

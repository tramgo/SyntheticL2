# Phase70 Cross-Symbol Lead-Lag Labels

Generated UTC: 2026-07-19T19:45:27.919497+00:00

Phase70 tests whether ETF and mega-cap event-bar returns lead related target symbols at the next event bar.
This is the first cross-symbol feature-family scan after the single-symbol families failed their bounded gates.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase70_trade_month | 2026-01 | Dense trade-month partition scanned |
| phase70_symbols_loaded | 32 | Symbols loaded into event-bar matrix |
| phase70_bar_rows | 1597 | Symbol event-bar rows |
| phase70_pair_rows | 16280 | Leader-target pair rows before thresholding |
| phase70_rule_rows | 48 | Lead-lag threshold rules evaluated |
| phase70_label_candidate_rows | 0 | Rules passing cross-symbol lead-lag gate |
| phase70_best_net_pnl_inr | 38915.7 | Best after-cost rule P&L |
| phase70_best_precision_cost_clear | 0.494845 | Best cost-clearing precision |
| phase70_survives_cross_symbol_gate | 0 | 1 means a lead-lag rule deserves disjoint-month replay |
| phase70_elapsed_seconds | 5.93785 | Elapsed seconds |
| phase70_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |
| phase70_recommend_next_action | advance_to_shock_resilience_feature_family | Recommended next action |

## Top Rule Results

| rule_id | group_id | leader_symbol | side_mode | feature_quantile | abs_leader_return_threshold | trades | target_symbols | trade_dates | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | mean_net_bps | precision_cost_clear | positive_target_fraction | positive_date_fraction | cost_drag_to_abs_gross_ratio | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P70_MEGA_HDFCBANK_MOMENTUM_Q70 | MEGA_HDFCBANK_MOMENTUM | HDFCBANK | sign | 0.7 | 0.00428699 | 390 | 26 | 1 | 38915.7 | 85632.7 | 46717 | 9.9784 | 0.479487 | 0.769231 | 1 | 0.54555 | False |
| P70_MEGA_HDFCBANK_MOMENTUM_Q50 | MEGA_HDFCBANK_MOMENTUM | HDFCBANK | sign | 0.5 | 0.0025251 | 649 | 26 | 1 | 16193.4 | 93947.1 | 77753.7 | 2.49512 | 0.451464 | 0.615385 | 1 | 0.827633 | False |
| P70_ETF_NIFTY_FADE_Q90 | ETF_NIFTY_FADE | NIFTYBEES | opposite | 0.9 | 0.00702457 | 134 | 27 | 1 | 2141.54 | 18139.1 | 15997.6 | 1.59816 | 0.440299 | 0.592593 | 1 | 0.881938 | False |
| P70_ETF_IT_FADE_Q90 | ETF_IT_FADE | ITBEES | opposite | 0.9 | 0.00371632 | 25 | 5 | 1 | -1098.82 | 1958.62 | 3057.43 | -4.39527 | 0.32 | 0.2 | 0 | 1.56102 | False |
| P70_ETF_BANK_FADE_Q90 | ETF_BANK_FADE | BANKBEES | opposite | 0.9 | 0.00446845 | 25 | 5 | 1 | -1905.86 | 929.801 | 2835.66 | -7.62342 | 0.4 | 0.8 | 0 | 3.04975 | False |
| P70_MEGA_INFY_FADE_Q90 | MEGA_INFY_FADE | INFY | opposite | 0.9 | 0.00746335 | 129 | 26 | 1 | -3090.54 | 12351.9 | 15442.4 | -2.39576 | 0.364341 | 0.5 | 0 | 1.25021 | False |
| P70_ETF_BANK_MOMENTUM_Q90 | ETF_BANK_MOMENTUM | BANKBEES | sign | 0.9 | 0.00446845 | 25 | 5 | 1 | -3765.46 | -929.801 | 2835.66 | -15.0618 | 0.32 | 0.2 | 0 | 3.04975 | False |
| P70_ETF_BANK_MOMENTUM_Q70 | ETF_BANK_MOMENTUM | BANKBEES | sign | 0.7 | 0.0028846 | 75 | 5 | 1 | -4088.43 | 4417.34 | 8505.77 | -5.45124 | 0.44 | 0.2 | 0 | 1.92554 | False |
| P70_ETF_BANK_MOMENTUM_Q50 | ETF_BANK_MOMENTUM | BANKBEES | sign | 0.5 | 0.00176684 | 125 | 5 | 1 | -4145.69 | 10024.5 | 14170.2 | -3.31655 | 0.488 | 0.4 | 0 | 1.41356 | False |
| P70_MEGA_HDFCBANK_MOMENTUM_Q90 | MEGA_HDFCBANK_MOMENTUM | HDFCBANK | sign | 0.9 | 0.00759339 | 130 | 26 | 1 | -4607.42 | 10963.6 | 15571 | -3.54417 | 0.415385 | 0.384615 | 0 | 1.42025 | False |
| P70_ETF_IT_MOMENTUM_Q90 | ETF_IT_MOMENTUM | ITBEES | sign | 0.9 | 0.00371632 | 25 | 5 | 1 | -5016.05 | -1958.62 | 3057.43 | -20.0642 | 0.4 | 0 | 0 | 1.56102 | False |
| P70_MEGA_RELIANCE_FADE_Q90 | MEGA_RELIANCE_FADE | RELIANCE | opposite | 0.9 | 0.0064994 | 129 | 26 | 1 | -6624.89 | 8830.91 | 15455.8 | -5.13558 | 0.379845 | 0.384615 | 0 | 1.75019 | False |
| P70_ETF_IT_MOMENTUM_Q70 | ETF_IT_MOMENTUM | ITBEES | sign | 0.7 | 0.00276838 | 75 | 5 | 1 | -6644.18 | 2512.86 | 9157.04 | -8.8589 | 0.44 | 0 | 0 | 3.64407 | False |
| P70_MEGA_TCS_FADE_Q90 | MEGA_TCS_FADE | TCS | opposite | 0.9 | 0.00708769 | 129 | 26 | 1 | -8085.58 | 7367.6 | 15453.2 | -6.26789 | 0.372093 | 0.423077 | 0 | 2.09745 | False |
| P70_ETF_IT_MOMENTUM_Q50 | ETF_IT_MOMENTUM | ITBEES | sign | 0.5 | 0.00185329 | 120 | 5 | 1 | -10492.2 | 4155.06 | 14647.2 | -8.74347 | 0.408333 | 0 | 0 | 3.52515 | False |
| P70_ETF_IT_FADE_Q70 | ETF_IT_FADE | ITBEES | opposite | 0.7 | 0.00276838 | 75 | 5 | 1 | -11669.9 | -2512.86 | 9157.04 | -15.5599 | 0.306667 | 0 | 0 | 3.64407 | False |
| P70_ETF_BANK_FADE_Q70 | ETF_BANK_FADE | BANKBEES | opposite | 0.7 | 0.0028846 | 75 | 5 | 1 | -12923.1 | -4417.34 | 8505.77 | -17.2308 | 0.333333 | 0 | 0 | 1.92554 | False |
| P70_MEGA_ICICIBANK_FADE_Q90 | MEGA_ICICIBANK_FADE | ICICIBANK | opposite | 0.9 | 0.00683099 | 129 | 26 | 1 | -14706.4 | 763.015 | 15469.4 | -11.4003 | 0.325581 | 0.269231 | 0 | 20.2741 | False |
| P70_MEGA_ICICIBANK_MOMENTUM_Q90 | MEGA_ICICIBANK_MOMENTUM | ICICIBANK | sign | 0.9 | 0.00683099 | 129 | 26 | 1 | -16232.5 | -763.015 | 15469.4 | -12.5833 | 0.294574 | 0.192308 | 0 | 20.2741 | False |
| P70_MEGA_INFY_MOMENTUM_Q70 | MEGA_INFY_MOMENTUM | INFY | sign | 0.7 | 0.00439831 | 388 | 26 | 1 | -17671.8 | 28680.1 | 46351.9 | -4.55459 | 0.494845 | 0.230769 | 0 | 1.61617 | False |
| P70_ETF_NIFTY_FADE_Q70 | ETF_NIFTY_FADE | NIFTYBEES | opposite | 0.7 | 0.00332297 | 404 | 27 | 1 | -18517.5 | 29681.3 | 48198.7 | -4.58353 | 0.344059 | 0.444444 | 0 | 1.62388 | False |
| P70_ETF_IT_FADE_Q50 | ETF_IT_FADE | ITBEES | opposite | 0.5 | 0.00185329 | 120 | 5 | 1 | -18802.3 | -4155.06 | 14647.2 | -15.6686 | 0.266667 | 0 | 0 | 3.52515 | False |
| P70_MEGA_TCS_MOMENTUM_Q90 | MEGA_TCS_MOMENTUM | TCS | sign | 0.9 | 0.00708769 | 129 | 26 | 1 | -22820.8 | -7367.6 | 15453.2 | -17.6905 | 0.310078 | 0.115385 | 0 | 2.09745 | False |
| P70_ETF_BANK_FADE_Q50 | ETF_BANK_FADE | BANKBEES | opposite | 0.5 | 0.00176684 | 125 | 5 | 1 | -24194.6 | -10024.5 | 14170.2 | -19.3557 | 0.296 | 0 | 0 | 1.41356 | False |
| P70_MEGA_RELIANCE_MOMENTUM_Q90 | MEGA_RELIANCE_MOMENTUM | RELIANCE | sign | 0.9 | 0.0064994 | 129 | 26 | 1 | -24286.7 | -8830.91 | 15455.8 | -18.8269 | 0.317829 | 0.115385 | 0 | 1.75019 | False |
| P70_MEGA_HDFCBANK_FADE_Q90 | MEGA_HDFCBANK_FADE | HDFCBANK | opposite | 0.9 | 0.00759339 | 130 | 26 | 1 | -26534.5 | -10963.6 | 15571 | -20.4112 | 0.238462 | 0.0384615 | 0 | 1.42025 | False |
| P70_MEGA_INFY_MOMENTUM_Q90 | MEGA_INFY_MOMENTUM | INFY | sign | 0.9 | 0.00746335 | 129 | 26 | 1 | -27794.3 | -12351.9 | 15442.4 | -21.5459 | 0.294574 | 0.153846 | 0 | 1.25021 | False |
| P70_MEGA_INFY_MOMENTUM_Q50 | MEGA_INFY_MOMENTUM | INFY | sign | 0.5 | 0.00290289 | 648 | 26 | 1 | -33861.1 | 43552.2 | 77413.3 | -5.22548 | 0.467593 | 0.230769 | 0 | 1.77748 | False |
| P70_ETF_NIFTY_MOMENTUM_Q90 | ETF_NIFTY_MOMENTUM | NIFTYBEES | sign | 0.9 | 0.00702457 | 134 | 27 | 1 | -34136.7 | -18139.1 | 15997.6 | -25.4752 | 0.179104 | 0.111111 | 0 | 0.881938 | False |
| P70_MEGA_TCS_MOMENTUM_Q70 | MEGA_TCS_MOMENTUM | TCS | sign | 0.7 | 0.00347661 | 389 | 26 | 1 | -36996.8 | 9480.88 | 46477.7 | -9.51076 | 0.375321 | 0.0769231 | 0 | 4.90226 | False |

## Lead-Lag Spec Catalog

| group_id | leader_symbol | target_symbols | side_mode | description |
| --- | --- | --- | --- | --- |
| ETF_NIFTY_MOMENTUM | NIFTYBEES | ('ADANIPORTS', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'DRREDDY', 'HCLTECH', 'HDFCBANK', 'HINDUNILVR', 'ICICIBANK', 'INFY', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'ONGC', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TCS', 'TECHM', 'ULTRACEMCO', 'WIPRO') | sign | NIFTYBEES return leads broad equities. |
| ETF_NIFTY_FADE | NIFTYBEES | ('ADANIPORTS', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'DRREDDY', 'HCLTECH', 'HDFCBANK', 'HINDUNILVR', 'ICICIBANK', 'INFY', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'ONGC', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TCS', 'TECHM', 'ULTRACEMCO', 'WIPRO') | opposite | Fade NIFTYBEES return against broad equities. |
| ETF_BANK_MOMENTUM | BANKBEES | ('AXISBANK', 'HDFCBANK', 'ICICIBANK', 'KOTAKBANK', 'SBIN') | sign | BANKBEES return leads banks. |
| ETF_BANK_FADE | BANKBEES | ('AXISBANK', 'HDFCBANK', 'ICICIBANK', 'KOTAKBANK', 'SBIN') | opposite | Fade BANKBEES return against banks. |
| ETF_IT_MOMENTUM | ITBEES | ('HCLTECH', 'INFY', 'TCS', 'TECHM', 'WIPRO') | sign | ITBEES return leads IT large caps. |
| ETF_IT_FADE | ITBEES | ('HCLTECH', 'INFY', 'TCS', 'TECHM', 'WIPRO') | opposite | Fade ITBEES return against IT large caps. |
| MEGA_HDFCBANK_MOMENTUM | HDFCBANK | ('ADANIPORTS', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'DRREDDY', 'HCLTECH', 'HINDUNILVR', 'ICICIBANK', 'INFY', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'ONGC', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TCS', 'TECHM', 'ULTRACEMCO', 'WIPRO') | sign | HDFCBANK return leads other equities. |
| MEGA_HDFCBANK_FADE | HDFCBANK | ('ADANIPORTS', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'DRREDDY', 'HCLTECH', 'HINDUNILVR', 'ICICIBANK', 'INFY', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'ONGC', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TCS', 'TECHM', 'ULTRACEMCO', 'WIPRO') | opposite | Fade HDFCBANK return against other equities. |
| MEGA_ICICIBANK_MOMENTUM | ICICIBANK | ('ADANIPORTS', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'DRREDDY', 'HCLTECH', 'HDFCBANK', 'HINDUNILVR', 'INFY', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'ONGC', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TCS', 'TECHM', 'ULTRACEMCO', 'WIPRO') | sign | ICICIBANK return leads other equities. |
| MEGA_ICICIBANK_FADE | ICICIBANK | ('ADANIPORTS', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'DRREDDY', 'HCLTECH', 'HDFCBANK', 'HINDUNILVR', 'INFY', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'ONGC', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TCS', 'TECHM', 'ULTRACEMCO', 'WIPRO') | opposite | Fade ICICIBANK return against other equities. |
| MEGA_INFY_MOMENTUM | INFY | ('ADANIPORTS', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'DRREDDY', 'HCLTECH', 'HDFCBANK', 'HINDUNILVR', 'ICICIBANK', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'ONGC', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TCS', 'TECHM', 'ULTRACEMCO', 'WIPRO') | sign | INFY return leads other equities. |
| MEGA_INFY_FADE | INFY | ('ADANIPORTS', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'DRREDDY', 'HCLTECH', 'HDFCBANK', 'HINDUNILVR', 'ICICIBANK', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'ONGC', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TCS', 'TECHM', 'ULTRACEMCO', 'WIPRO') | opposite | Fade INFY return against other equities. |
| MEGA_RELIANCE_MOMENTUM | RELIANCE | ('ADANIPORTS', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'DRREDDY', 'HCLTECH', 'HDFCBANK', 'HINDUNILVR', 'ICICIBANK', 'INFY', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'ONGC', 'SBIN', 'SUNPHARMA', 'TCS', 'TECHM', 'ULTRACEMCO', 'WIPRO') | sign | RELIANCE return leads other equities. |
| MEGA_RELIANCE_FADE | RELIANCE | ('ADANIPORTS', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'DRREDDY', 'HCLTECH', 'HDFCBANK', 'HINDUNILVR', 'ICICIBANK', 'INFY', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'ONGC', 'SBIN', 'SUNPHARMA', 'TCS', 'TECHM', 'ULTRACEMCO', 'WIPRO') | opposite | Fade RELIANCE return against other equities. |
| MEGA_TCS_MOMENTUM | TCS | ('ADANIPORTS', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'DRREDDY', 'HCLTECH', 'HDFCBANK', 'HINDUNILVR', 'ICICIBANK', 'INFY', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'ONGC', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TECHM', 'ULTRACEMCO', 'WIPRO') | sign | TCS return leads other equities. |
| MEGA_TCS_FADE | TCS | ('ADANIPORTS', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'DRREDDY', 'HCLTECH', 'HDFCBANK', 'HINDUNILVR', 'ICICIBANK', 'INFY', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'ONGC', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TECHM', 'ULTRACEMCO', 'WIPRO') | opposite | Fade TCS return against other equities. |

## Thresholds

| group_id | feature_quantile | abs_leader_return_threshold |
| --- | --- | --- |
| ETF_BANK_FADE | 0.5 | 0.00176684 |
| ETF_BANK_FADE | 0.7 | 0.0028846 |
| ETF_BANK_FADE | 0.9 | 0.00446845 |
| ETF_BANK_MOMENTUM | 0.5 | 0.00176684 |
| ETF_BANK_MOMENTUM | 0.7 | 0.0028846 |
| ETF_BANK_MOMENTUM | 0.9 | 0.00446845 |
| ETF_IT_FADE | 0.5 | 0.00185329 |
| ETF_IT_FADE | 0.7 | 0.00276838 |
| ETF_IT_FADE | 0.9 | 0.00371632 |
| ETF_IT_MOMENTUM | 0.5 | 0.00185329 |
| ETF_IT_MOMENTUM | 0.7 | 0.00276838 |
| ETF_IT_MOMENTUM | 0.9 | 0.00371632 |
| ETF_NIFTY_FADE | 0.5 | 0.00216614 |
| ETF_NIFTY_FADE | 0.7 | 0.00332297 |
| ETF_NIFTY_FADE | 0.9 | 0.00702457 |
| ETF_NIFTY_MOMENTUM | 0.5 | 0.00216614 |
| ETF_NIFTY_MOMENTUM | 0.7 | 0.00332297 |
| ETF_NIFTY_MOMENTUM | 0.9 | 0.00702457 |
| MEGA_HDFCBANK_FADE | 0.5 | 0.0025251 |
| MEGA_HDFCBANK_FADE | 0.7 | 0.00428699 |
| MEGA_HDFCBANK_FADE | 0.9 | 0.00759339 |
| MEGA_HDFCBANK_MOMENTUM | 0.5 | 0.0025251 |
| MEGA_HDFCBANK_MOMENTUM | 0.7 | 0.00428699 |
| MEGA_HDFCBANK_MOMENTUM | 0.9 | 0.00759339 |
| MEGA_ICICIBANK_FADE | 0.5 | 0.00208275 |
| MEGA_ICICIBANK_FADE | 0.7 | 0.00353528 |
| MEGA_ICICIBANK_FADE | 0.9 | 0.00683099 |
| MEGA_ICICIBANK_MOMENTUM | 0.5 | 0.00208275 |
| MEGA_ICICIBANK_MOMENTUM | 0.7 | 0.00353528 |
| MEGA_ICICIBANK_MOMENTUM | 0.9 | 0.00683099 |
| MEGA_INFY_FADE | 0.5 | 0.00290289 |
| MEGA_INFY_FADE | 0.7 | 0.00439831 |
| MEGA_INFY_FADE | 0.9 | 0.00746335 |
| MEGA_INFY_MOMENTUM | 0.5 | 0.00290289 |
| MEGA_INFY_MOMENTUM | 0.7 | 0.00439831 |
| MEGA_INFY_MOMENTUM | 0.9 | 0.00746335 |
| MEGA_RELIANCE_FADE | 0.5 | 0.00281347 |
| MEGA_RELIANCE_FADE | 0.7 | 0.00408287 |
| MEGA_RELIANCE_FADE | 0.9 | 0.0064994 |
| MEGA_RELIANCE_MOMENTUM | 0.5 | 0.00281347 |
| MEGA_RELIANCE_MOMENTUM | 0.7 | 0.00408287 |
| MEGA_RELIANCE_MOMENTUM | 0.9 | 0.0064994 |
| MEGA_TCS_FADE | 0.5 | 0.00240221 |
| MEGA_TCS_FADE | 0.7 | 0.00347661 |
| MEGA_TCS_FADE | 0.9 | 0.00708769 |
| MEGA_TCS_MOMENTUM | 0.5 | 0.00240221 |
| MEGA_TCS_MOMENTUM | 0.7 | 0.00347661 |
| MEGA_TCS_MOMENTUM | 0.9 | 0.00708769 |

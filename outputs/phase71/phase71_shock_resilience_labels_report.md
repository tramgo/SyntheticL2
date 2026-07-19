# Phase71 Shock-Resilience Labels

Generated UTC: 2026-07-19T19:49:22.134876+00:00

Phase71 tests whether market/symbol shock tags create lower-frequency momentum or mean-reversion labels that survive costs.
Shock candidates must beat matched no-shock controls before any wider replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase71_shards_scanned | 128 | Dense shards scanned |
| phase71_bar_rows | 9072 | Shock/control event-bar rows |
| phase71_shock_bar_rows | 2265 | Event-bar rows with market or symbol shock tags |
| phase71_rule_rows | 36 | Shock resilience rules evaluated |
| phase71_label_candidate_rows | 0 | Shock rules passing label gate |
| phase71_best_net_pnl_inr | 13311.4 | Best after-cost rule P&L |
| phase71_survives_shock_resilience_gate | 0 | 1 means a shock-resilience rule deserves replay |
| phase71_elapsed_seconds | 54.9316 | Elapsed seconds |
| phase71_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |
| phase71_recommend_next_action | research_audit_and_generator_assumption_review | Recommended next action |

## Top Rule Results

| rule_id | signal_id | side_mode | bar_events | shock_bucket | feature_quantile | abs_prev_return_threshold | trades | symbols | trade_months | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | mean_net_bps | precision_cost_clear | positive_symbol_fraction | positive_month_fraction | cost_drag_to_abs_gross_ratio | matched_no_shock_control_net_pnl_inr | label_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P71_SHOCK_MEAN_REVERSION_B10000_market_shock_Q90 | SHOCK_MEAN_REVERSION | opposite | 10000 | market_shock | 0.9 | 0.0148054 | 72 | 29 | 1 | 13311.4 | 24096.1 | 10784.7 | 18.488 | 0.611111 | 0.689655 | 1 | 0.447572 | -10934.8 | False |
| P71_SHOCK_MEAN_REVERSION_B10000_market_shock_Q70 | SHOCK_MEAN_REVERSION | opposite | 10000 | market_shock | 0.7 | 0.00862762 | 214 | 31 | 1 | 10530.5 | 42692.2 | 32161.7 | 4.92079 | 0.518692 | 0.612903 | 1 | 0.753339 | -45378.3 | False |
| P71_SHOCK_MEAN_REVERSION_B10000_symbol_shock_Q50 | SHOCK_MEAN_REVERSION | opposite | 10000 | symbol_shock | 0.5 | 0.0067027 | 12 | 1 | 1 | 7553.21 | 9370.46 | 1817.25 | 62.9434 | 0.75 | 1 | 1 | 0.193934 | -90474 | False |
| P71_SHOCK_MEAN_REVERSION_B10000_symbol_shock_Q70 | SHOCK_MEAN_REVERSION | opposite | 10000 | symbol_shock | 0.7 | 0.00993432 | 7 | 1 | 1 | 6850.04 | 7909.78 | 1059.74 | 97.8578 | 0.714286 | 1 | 1 | 0.133978 | -45378.3 | False |
| P71_SHOCK_MEAN_REVERSION_B10000_symbol_shock_Q90 | SHOCK_MEAN_REVERSION | opposite | 10000 | symbol_shock | 0.9 | 0.0170414 | 3 | 1 | 1 | 6149.7 | 6603.82 | 454.125 | 204.99 | 1 | 1 | 1 | 0.068767 | -10934.8 | False |
| P71_SHOCK_MEAN_REVERSION_B5000_symbol_shock_Q70 | SHOCK_MEAN_REVERSION | opposite | 5000 | symbol_shock | 0.7 | 0.00843277 | 15 | 1 | 1 | 3103.64 | 5371.81 | 2268.17 | 20.6909 | 0.466667 | 1 | 1 | 0.422235 | -152171 | False |
| P71_SHOCK_MEAN_REVERSION_B5000_symbol_shock_Q50 | SHOCK_MEAN_REVERSION | opposite | 5000 | symbol_shock | 0.5 | 0.00521117 | 24 | 1 | 1 | 1751.33 | 5387.41 | 3636.09 | 7.29719 | 0.5 | 1 | 1 | 0.674923 | -285025 | False |
| P71_SHOCK_MOMENTUM_B5000_symbol_shock_Q90 | SHOCK_MOMENTUM | sign | 5000 | symbol_shock | 0.9 | 0.0121253 | 5 | 1 | 1 | -744.091 | 11.0706 | 755.162 | -14.8818 | 0.2 | 0 | 0 | 68.2132 | -63587.5 | False |
| P71_SHOCK_MEAN_REVERSION_B5000_symbol_shock_Q90 | SHOCK_MEAN_REVERSION | opposite | 5000 | symbol_shock | 0.9 | 0.0121253 | 5 | 1 | 1 | -766.232 | -11.0706 | 755.162 | -15.3246 | 0.2 | 0 | 0 | 68.2132 | -46510.2 | False |
| P71_SHOCK_MEAN_REVERSION_B10000_market_shock_Q50 | SHOCK_MEAN_REVERSION | opposite | 10000 | market_shock | 0.5 | 0.00556539 | 356 | 31 | 1 | -2682.58 | 51162.7 | 53845.3 | -0.753535 | 0.474719 | 0.612903 | 0 | 1.05243 | -90474 | False |
| P71_SHOCK_MOMENTUM_B10000_symbol_shock_Q90 | SHOCK_MOMENTUM | sign | 10000 | symbol_shock | 0.9 | 0.0170414 | 3 | 1 | 1 | -7057.95 | -6603.82 | 454.125 | -235.265 | 0 | 0 | 0 | 0.068767 | -41902.7 | False |
| P71_SHOCK_MOMENTUM_B5000_symbol_shock_Q70 | SHOCK_MOMENTUM | sign | 5000 | symbol_shock | 0.7 | 0.00843277 | 15 | 1 | 1 | -7639.98 | -5371.81 | 2268.17 | -50.9332 | 0.266667 | 0 | 0 | 0.422235 | -179002 | False |
| P71_SHOCK_MOMENTUM_B10000_symbol_shock_Q70 | SHOCK_MOMENTUM | sign | 10000 | symbol_shock | 0.7 | 0.00993432 | 7 | 1 | 1 | -8969.52 | -7909.78 | 1059.74 | -128.136 | 0.285714 | 0 | 0 | 0.133978 | -113175 | False |
| P71_SHOCK_MOMENTUM_B5000_symbol_shock_Q50 | SHOCK_MOMENTUM | sign | 5000 | symbol_shock | 0.5 | 0.00521117 | 24 | 1 | 1 | -9023.5 | -5387.41 | 3636.09 | -37.5979 | 0.291667 | 0 | 0 | 0.674923 | -268288 | False |
| P71_SHOCK_MEAN_REVERSION_B5000_market_shock_Q90 | SHOCK_MEAN_REVERSION | opposite | 5000 | market_shock | 0.9 | 0.0113232 | 149 | 31 | 1 | -9767.08 | 12689.9 | 22457 | -6.55509 | 0.395973 | 0.483871 | 0 | 1.76967 | -46510.2 | False |
| P71_SHOCK_MEAN_REVERSION_B10000_no_shock_control_Q90 | SHOCK_MEAN_REVERSION | opposite | 10000 | no_shock_control | 0.9 | 0.00781177 | 221 | 32 | 3 | -10934.8 | 15483.9 | 26418.8 | -4.94789 | 0.493213 | 0.40625 | 0.333333 | 1.70621 | -10934.8 | False |
| P71_SHOCK_MOMENTUM_B10000_symbol_shock_Q50 | SHOCK_MOMENTUM | sign | 10000 | symbol_shock | 0.5 | 0.0067027 | 12 | 1 | 1 | -11187.7 | -9370.46 | 1817.25 | -93.2309 | 0.25 | 0 | 0 | 0.193934 | -174568 | False |
| P71_SHOCK_MEAN_REVERSION_B5000_market_shock_Q70 | SHOCK_MEAN_REVERSION | opposite | 5000 | market_shock | 0.7 | 0.00634354 | 445 | 31 | 1 | -28586.7 | 38647.1 | 67233.8 | -6.42397 | 0.438202 | 0.419355 | 0 | 1.73968 | -152171 | False |
| P71_SHOCK_MOMENTUM_B10000_market_shock_Q90 | SHOCK_MOMENTUM | sign | 10000 | market_shock | 0.9 | 0.0148054 | 72 | 29 | 1 | -34880.9 | -24096.1 | 10784.7 | -48.4456 | 0.263889 | 0.137931 | 0 | 0.447572 | -41902.7 | False |
| P71_SHOCK_MOMENTUM_B5000_market_shock_Q90 | SHOCK_MOMENTUM | sign | 5000 | market_shock | 0.9 | 0.0113232 | 149 | 31 | 1 | -35147 | -12689.9 | 22457 | -23.5886 | 0.442953 | 0.290323 | 0 | 1.76967 | -63587.5 | False |
| P71_SHOCK_MOMENTUM_B10000_no_shock_control_Q90 | SHOCK_MOMENTUM | sign | 10000 | no_shock_control | 0.9 | 0.00781177 | 221 | 32 | 3 | -41902.7 | -15483.9 | 26418.8 | -18.9605 | 0.339367 | 0.09375 | 0 | 1.70621 | -41902.7 | False |
| P71_SHOCK_MEAN_REVERSION_B10000_no_shock_control_Q70 | SHOCK_MEAN_REVERSION | opposite | 10000 | no_shock_control | 0.7 | 0.00508762 | 662 | 32 | 3 | -45378.3 | 33898.3 | 79276.6 | -6.85473 | 0.486405 | 0.3125 | 0.333333 | 2.33866 | -45378.3 | False |
| P71_SHOCK_MEAN_REVERSION_B5000_no_shock_control_Q90 | SHOCK_MEAN_REVERSION | opposite | 5000 | no_shock_control | 0.9 | 0.00564507 | 461 | 32 | 3 | -46510.2 | 8538.63 | 55048.9 | -10.089 | 0.336226 | 0.1875 | 0 | 6.44703 | -46510.2 | False |
| P71_SHOCK_MEAN_REVERSION_B5000_market_shock_Q50 | SHOCK_MEAN_REVERSION | opposite | 5000 | market_shock | 0.5 | 0.00382101 | 742 | 31 | 1 | -49632.2 | 62604.8 | 112237 | -6.68898 | 0.440701 | 0.387097 | 0 | 1.79279 | -285025 | False |
| P71_SHOCK_MOMENTUM_B5000_no_shock_control_Q90 | SHOCK_MOMENTUM | sign | 5000 | no_shock_control | 0.9 | 0.00564507 | 461 | 32 | 3 | -63587.5 | -8538.63 | 55048.9 | -13.7934 | 0.336226 | 0.0625 | 0 | 6.44703 | -63587.5 | False |
| P71_SHOCK_MOMENTUM_B10000_market_shock_Q70 | SHOCK_MOMENTUM | sign | 10000 | market_shock | 0.7 | 0.00862762 | 214 | 31 | 1 | -74853.9 | -42692.2 | 32161.7 | -34.9785 | 0.350467 | 0.129032 | 0 | 0.753339 | -113175 | False |
| P71_SHOCK_MEAN_REVERSION_B10000_no_shock_control_Q50 | SHOCK_MEAN_REVERSION | opposite | 10000 | no_shock_control | 0.5 | 0.00333146 | 1103 | 32 | 3 | -90474 | 42046.8 | 132521 | -8.20253 | 0.458749 | 0.09375 | 0.333333 | 3.15174 | -90474 | False |
| P71_SHOCK_MOMENTUM_B10000_market_shock_Q50 | SHOCK_MOMENTUM | sign | 10000 | market_shock | 0.5 | 0.00556539 | 356 | 31 | 1 | -105008 | -51162.7 | 53845.3 | -29.4966 | 0.398876 | 0.193548 | 0 | 1.05243 | -174568 | False |
| P71_SHOCK_MOMENTUM_B5000_market_shock_Q70 | SHOCK_MOMENTUM | sign | 5000 | market_shock | 0.7 | 0.00634354 | 445 | 31 | 1 | -105881 | -38647.1 | 67233.8 | -23.7935 | 0.377528 | 0.225806 | 0 | 1.73968 | -179002 | False |
| P71_SHOCK_MOMENTUM_B10000_no_shock_control_Q70 | SHOCK_MOMENTUM | sign | 10000 | no_shock_control | 0.7 | 0.00508762 | 662 | 32 | 3 | -113175 | -33898.3 | 79276.6 | -17.0959 | 0.362538 | 0.03125 | 0 | 2.33866 | -113175 | False |
| P71_SHOCK_MEAN_REVERSION_B5000_no_shock_control_Q70 | SHOCK_MEAN_REVERSION | opposite | 5000 | no_shock_control | 0.7 | 0.00329154 | 1381 | 32 | 3 | -152171 | 13415.7 | 165586 | -11.0189 | 0.361332 | 0.03125 | 0 | 12.3428 | -152171 | False |
| P71_SHOCK_MOMENTUM_B10000_no_shock_control_Q50 | SHOCK_MOMENTUM | sign | 10000 | no_shock_control | 0.5 | 0.00333146 | 1103 | 32 | 3 | -174568 | -42046.8 | 132521 | -15.8266 | 0.370807 | 0.03125 | 0 | 3.15174 | -174568 | False |
| P71_SHOCK_MOMENTUM_B5000_market_shock_Q50 | SHOCK_MOMENTUM | sign | 5000 | market_shock | 0.5 | 0.00382101 | 742 | 31 | 1 | -174842 | -62604.8 | 112237 | -23.5636 | 0.382749 | 0.16129 | 0 | 1.79279 | -268288 | False |
| P71_SHOCK_MOMENTUM_B5000_no_shock_control_Q70 | SHOCK_MOMENTUM | sign | 5000 | no_shock_control | 0.7 | 0.00329154 | 1381 | 32 | 3 | -179002 | -13415.7 | 165586 | -12.9618 | 0.30992 | 0 | 0 | 12.3428 | -179002 | False |
| P71_SHOCK_MOMENTUM_B5000_no_shock_control_Q50 | SHOCK_MOMENTUM | sign | 5000 | no_shock_control | 0.5 | 0.00207756 | 2301 | 32 | 3 | -268288 | 8368.37 | 276657 | -11.6596 | 0.338548 | 0 | 0 | 33.0598 | -268288 | False |
| P71_SHOCK_MEAN_REVERSION_B5000_no_shock_control_Q50 | SHOCK_MEAN_REVERSION | opposite | 5000 | no_shock_control | 0.5 | 0.00207756 | 2301 | 32 | 3 | -285025 | -8368.37 | 276657 | -12.387 | 0.34811 | 0 | 0 | 33.0598 | -285025 | False |

## Rule Thresholds

| rule_id | signal_id | side_mode | bar_events | shock_bucket | feature_quantile | abs_prev_return_threshold |
| --- | --- | --- | --- | --- | --- | --- |
| P71_SHOCK_MOMENTUM_B5000_market_shock_Q50 | SHOCK_MOMENTUM | sign | 5000 | market_shock | 0.5 | 0.00382101 |
| P71_SHOCK_MOMENTUM_B5000_market_shock_Q70 | SHOCK_MOMENTUM | sign | 5000 | market_shock | 0.7 | 0.00634354 |
| P71_SHOCK_MOMENTUM_B5000_market_shock_Q90 | SHOCK_MOMENTUM | sign | 5000 | market_shock | 0.9 | 0.0113232 |
| P71_SHOCK_MEAN_REVERSION_B5000_market_shock_Q50 | SHOCK_MEAN_REVERSION | opposite | 5000 | market_shock | 0.5 | 0.00382101 |
| P71_SHOCK_MEAN_REVERSION_B5000_market_shock_Q70 | SHOCK_MEAN_REVERSION | opposite | 5000 | market_shock | 0.7 | 0.00634354 |
| P71_SHOCK_MEAN_REVERSION_B5000_market_shock_Q90 | SHOCK_MEAN_REVERSION | opposite | 5000 | market_shock | 0.9 | 0.0113232 |
| P71_SHOCK_MOMENTUM_B5000_no_shock_control_Q50 | SHOCK_MOMENTUM | sign | 5000 | no_shock_control | 0.5 | 0.00207756 |
| P71_SHOCK_MOMENTUM_B5000_no_shock_control_Q70 | SHOCK_MOMENTUM | sign | 5000 | no_shock_control | 0.7 | 0.00329154 |
| P71_SHOCK_MOMENTUM_B5000_no_shock_control_Q90 | SHOCK_MOMENTUM | sign | 5000 | no_shock_control | 0.9 | 0.00564507 |
| P71_SHOCK_MEAN_REVERSION_B5000_no_shock_control_Q50 | SHOCK_MEAN_REVERSION | opposite | 5000 | no_shock_control | 0.5 | 0.00207756 |
| P71_SHOCK_MEAN_REVERSION_B5000_no_shock_control_Q70 | SHOCK_MEAN_REVERSION | opposite | 5000 | no_shock_control | 0.7 | 0.00329154 |
| P71_SHOCK_MEAN_REVERSION_B5000_no_shock_control_Q90 | SHOCK_MEAN_REVERSION | opposite | 5000 | no_shock_control | 0.9 | 0.00564507 |
| P71_SHOCK_MOMENTUM_B5000_symbol_shock_Q50 | SHOCK_MOMENTUM | sign | 5000 | symbol_shock | 0.5 | 0.00521117 |
| P71_SHOCK_MOMENTUM_B5000_symbol_shock_Q70 | SHOCK_MOMENTUM | sign | 5000 | symbol_shock | 0.7 | 0.00843277 |
| P71_SHOCK_MOMENTUM_B5000_symbol_shock_Q90 | SHOCK_MOMENTUM | sign | 5000 | symbol_shock | 0.9 | 0.0121253 |
| P71_SHOCK_MEAN_REVERSION_B5000_symbol_shock_Q50 | SHOCK_MEAN_REVERSION | opposite | 5000 | symbol_shock | 0.5 | 0.00521117 |
| P71_SHOCK_MEAN_REVERSION_B5000_symbol_shock_Q70 | SHOCK_MEAN_REVERSION | opposite | 5000 | symbol_shock | 0.7 | 0.00843277 |
| P71_SHOCK_MEAN_REVERSION_B5000_symbol_shock_Q90 | SHOCK_MEAN_REVERSION | opposite | 5000 | symbol_shock | 0.9 | 0.0121253 |
| P71_SHOCK_MOMENTUM_B10000_market_shock_Q50 | SHOCK_MOMENTUM | sign | 10000 | market_shock | 0.5 | 0.00556539 |
| P71_SHOCK_MOMENTUM_B10000_market_shock_Q70 | SHOCK_MOMENTUM | sign | 10000 | market_shock | 0.7 | 0.00862762 |
| P71_SHOCK_MOMENTUM_B10000_market_shock_Q90 | SHOCK_MOMENTUM | sign | 10000 | market_shock | 0.9 | 0.0148054 |
| P71_SHOCK_MEAN_REVERSION_B10000_market_shock_Q50 | SHOCK_MEAN_REVERSION | opposite | 10000 | market_shock | 0.5 | 0.00556539 |
| P71_SHOCK_MEAN_REVERSION_B10000_market_shock_Q70 | SHOCK_MEAN_REVERSION | opposite | 10000 | market_shock | 0.7 | 0.00862762 |
| P71_SHOCK_MEAN_REVERSION_B10000_market_shock_Q90 | SHOCK_MEAN_REVERSION | opposite | 10000 | market_shock | 0.9 | 0.0148054 |
| P71_SHOCK_MOMENTUM_B10000_no_shock_control_Q50 | SHOCK_MOMENTUM | sign | 10000 | no_shock_control | 0.5 | 0.00333146 |
| P71_SHOCK_MOMENTUM_B10000_no_shock_control_Q70 | SHOCK_MOMENTUM | sign | 10000 | no_shock_control | 0.7 | 0.00508762 |
| P71_SHOCK_MOMENTUM_B10000_no_shock_control_Q90 | SHOCK_MOMENTUM | sign | 10000 | no_shock_control | 0.9 | 0.00781177 |
| P71_SHOCK_MEAN_REVERSION_B10000_no_shock_control_Q50 | SHOCK_MEAN_REVERSION | opposite | 10000 | no_shock_control | 0.5 | 0.00333146 |
| P71_SHOCK_MEAN_REVERSION_B10000_no_shock_control_Q70 | SHOCK_MEAN_REVERSION | opposite | 10000 | no_shock_control | 0.7 | 0.00508762 |
| P71_SHOCK_MEAN_REVERSION_B10000_no_shock_control_Q90 | SHOCK_MEAN_REVERSION | opposite | 10000 | no_shock_control | 0.9 | 0.00781177 |
| P71_SHOCK_MOMENTUM_B10000_symbol_shock_Q50 | SHOCK_MOMENTUM | sign | 10000 | symbol_shock | 0.5 | 0.0067027 |
| P71_SHOCK_MOMENTUM_B10000_symbol_shock_Q70 | SHOCK_MOMENTUM | sign | 10000 | symbol_shock | 0.7 | 0.00993432 |
| P71_SHOCK_MOMENTUM_B10000_symbol_shock_Q90 | SHOCK_MOMENTUM | sign | 10000 | symbol_shock | 0.9 | 0.0170414 |
| P71_SHOCK_MEAN_REVERSION_B10000_symbol_shock_Q50 | SHOCK_MEAN_REVERSION | opposite | 10000 | symbol_shock | 0.5 | 0.0067027 |
| P71_SHOCK_MEAN_REVERSION_B10000_symbol_shock_Q70 | SHOCK_MEAN_REVERSION | opposite | 10000 | symbol_shock | 0.7 | 0.00993432 |
| P71_SHOCK_MEAN_REVERSION_B10000_symbol_shock_Q90 | SHOCK_MEAN_REVERSION | opposite | 10000 | symbol_shock | 0.9 | 0.0170414 |

# Phase 29 Partial Strategy Proxy Replay

Generated UTC: 2026-07-14T18:25:13.495456+00:00

This milestone converts the Phase 28 weak proxy labels for S03/S04/S06/S08 into executable replay signals.
It is an execution diagnostic, not strategy acceptance evidence.

## Overall Summary

| metric | value | description |
| --- | --- | --- |
| phase29_partial_strategies_replayed | 4 | Partial strategy proxy families replayed |
| phase29_strategy_profile_rows | 12 | Strategy/profile summary rows |
| phase29_total_replay_trades | 742623 | Total partial-strategy proxy replay trades |
| phase29_positive_after_cost_rows | 0 | Rows with positive mean net return after costs |
| phase29_realistic_positive_rows | 0 | Retail/stressed rows positive after costs |
| phase29_proxy_candidate_rows | 0 | Rows passing realistic, positive, trade-count and proxy-risk checks |
| phase29_acceptance_ready | 0 | Partial strategy replay uses weak proxy labels, not acceptance evidence |

## Strategy/Profile Summary

| model_id | model_type | execution_profile | trades | symbols | scenario_days | mean_gross_return | mean_cost_return | mean_zerodha_charge_return | mean_net_return | win_rate_net | total_net_pnl_inr | market_shock_trade_fraction | disconnect_trade_fraction | acceptance_ready | replay_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S03 | partial_strategy_proxy | retail_marketable_default | 7424 | 30 | 1 | -5.5491e-08 | 0.000964945 | 0.000826812 | -0.000965001 | 0.00080819 | -716416 | 0 | 0 | False | event_order_replay_not_acceptance |
| S03 | partial_strategy_proxy | stressed_retail | 7452 | 30 | 1 | 7.94566e-07 | 0.00114277 | 0.000826812 | -0.00114197 | 0.000536769 | -850999 | 0 | 0 | False | event_order_replay_not_acceptance |
| S03 | partial_strategy_proxy | zero_latency_spread_only_control | 7593 | 30 | 1 | 9.15611e-06 | 8.82365e-05 | 0 | -7.90804e-05 | 0.293296 | -60045.7 | 0 | 0 | False | event_order_replay_not_acceptance |
| S04 | partial_strategy_proxy | retail_marketable_default | 36920 | 32 | 1 | 3.12657e-06 | 0.00100991 | 0.000826812 | -0.00100678 | 0.000460455 | -3.71704e+06 | 0 | 0 | False | event_order_replay_not_acceptance |
| S04 | partial_strategy_proxy | stressed_retail | 37253 | 32 | 1 | -6.00917e-08 | 0.00120549 | 0.000826812 | -0.00120555 | 0.000161061 | -4.49102e+06 | 0 | 0 | False | event_order_replay_not_acceptance |
| S04 | partial_strategy_proxy | zero_latency_spread_only_control | 38481 | 32 | 1 | 4.32351e-06 | 8.88067e-05 | 0 | -8.44832e-05 | 0.063226 | -325100 | 0 | 0 | False | event_order_replay_not_acceptance |
| S06 | partial_strategy_proxy | retail_marketable_default | 68476 | 32 | 1 | -7.63435e-08 | 0.00104301 | 0.000826812 | -0.00104308 | 0.000175244 | -7.14263e+06 | 0 | 0 | False | event_order_replay_not_acceptance |
| S06 | partial_strategy_proxy | stressed_retail | 69008 | 32 | 1 | -2.97453e-07 | 0.00125192 | 0.000826812 | -0.00125222 | 7.24554e-05 | -8.6413e+06 | 0 | 0 | False | event_order_replay_not_acceptance |
| S06 | partial_strategy_proxy | zero_latency_spread_only_control | 71244 | 32 | 1 | -2.59854e-07 | 0.000108778 | 0 | -0.000109038 | 0.0349643 | -776830 | 0 | 0 | False | event_order_replay_not_acceptance |
| S08 | partial_strategy_proxy | retail_marketable_default | 132924 | 32 | 1 | 5.91801e-07 | 0.00105767 | 0.000826812 | -0.00105707 | 0.00230207 | -1.40511e+07 | 0 | 0 | False | event_order_replay_not_acceptance |
| S08 | partial_strategy_proxy | stressed_retail | 132860 | 32 | 1 | 9.39235e-07 | 0.00126743 | 0.000826812 | -0.00126649 | 0.00142255 | -1.68265e+07 | 0 | 0 | False | event_order_replay_not_acceptance |
| S08 | partial_strategy_proxy | zero_latency_spread_only_control | 132988 | 32 | 1 | -2.09531e-07 | 0.000121191 | 0 | -0.0001214 | 0.20468 | -1.61448e+06 | 0 | 0 | False | event_order_replay_not_acceptance |

## Candidate Summary

| model_id | execution_profile | trades | mean_net_return | best_peer_partial_strategy_mean_net_return | lift_vs_best_peer_partial_strategy | positive_after_costs | beats_peer_proxy | enough_trades_for_proxy_candidate | risk_status | realistic_charged_profile | risk_not_breached_proxy | partial_proxy_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S03 | zero_latency_spread_only_control | 7593 | -7.90804e-05 | -8.44832e-05 | 5.40284e-06 | False | True | True | risk_not_breached_proxy | False | True | False |
| S04 | zero_latency_spread_only_control | 38481 | -8.44832e-05 | -7.90804e-05 | -5.40284e-06 | False | False | True | risk_breached_proxy | False | False | False |
| S06 | zero_latency_spread_only_control | 71244 | -0.000109038 | -7.90804e-05 | -2.99576e-05 | False | False | True | risk_breached_proxy | False | False | False |
| S08 | zero_latency_spread_only_control | 132988 | -0.0001214 | -7.90804e-05 | -4.232e-05 | False | False | True | risk_breached_proxy | False | False | False |
| S03 | retail_marketable_default | 7424 | -0.000965001 | -0.00100678 | 4.17805e-05 | False | True | True | risk_breached_proxy | True | False | False |
| S04 | retail_marketable_default | 36920 | -0.00100678 | -0.000965001 | -4.17805e-05 | False | False | True | risk_breached_proxy | True | False | False |
| S06 | retail_marketable_default | 68476 | -0.00104308 | -0.000965001 | -7.80843e-05 | False | False | True | risk_breached_proxy | True | False | False |
| S08 | retail_marketable_default | 132924 | -0.00105707 | -0.000965001 | -9.20738e-05 | False | False | True | risk_breached_proxy | True | False | False |
| S03 | stressed_retail | 7452 | -0.00114197 | -0.00120555 | 6.35709e-05 | False | True | True | risk_breached_proxy | True | False | False |
| S04 | stressed_retail | 37253 | -0.00120555 | -0.00114197 | -6.35709e-05 | False | False | True | risk_breached_proxy | True | False | False |
| S06 | stressed_retail | 69008 | -0.00125222 | -0.00114197 | -0.000110242 | False | False | True | risk_breached_proxy | True | False | False |
| S08 | stressed_retail | 132860 | -0.00126649 | -0.00114197 | -0.000124512 | False | False | True | risk_breached_proxy | True | False | False |

## Risk Summary

| model_id | model_type | execution_profile | trade_dates | worst_daily_net_pnl_inr | tail_loss_1pct_trade_pnl_inr | max_intraday_drawdown_inr | daily_loss_breach_days | drawdown_breach_days | risk_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S03 | partial_strategy_proxy | retail_marketable_default | 1 | -716416 | -174.175 | -716350 | 1 | 1 | risk_breached_proxy |
| S03 | partial_strategy_proxy | stressed_retail | 1 | -850999 | -188.201 | -850832 | 1 | 1 | risk_breached_proxy |
| S03 | partial_strategy_proxy | zero_latency_spread_only_control | 1 | -60045.7 | -107.831 | -60041.9 | 0 | 0 | risk_not_breached_proxy |
| S04 | partial_strategy_proxy | retail_marketable_default | 1 | -3.71704e+06 | -200.135 | -3.71689e+06 | 1 | 1 | risk_breached_proxy |
| S04 | partial_strategy_proxy | stressed_retail | 1 | -4.49102e+06 | -226.346 | -4.49086e+06 | 1 | 1 | risk_breached_proxy |
| S04 | partial_strategy_proxy | zero_latency_spread_only_control | 1 | -325100 | -100.317 | -325042 | 1 | 1 | risk_breached_proxy |
| S06 | partial_strategy_proxy | retail_marketable_default | 1 | -7.14263e+06 | -207.933 | -7.14249e+06 | 1 | 1 | risk_breached_proxy |
| S06 | partial_strategy_proxy | stressed_retail | 1 | -8.6413e+06 | -234.509 | -8.64116e+06 | 1 | 1 | risk_breached_proxy |
| S06 | partial_strategy_proxy | zero_latency_spread_only_control | 1 | -776830 | -109.453 | -776836 | 1 | 1 | risk_breached_proxy |
| S08 | partial_strategy_proxy | retail_marketable_default | 1 | -1.40511e+07 | -221.382 | -1.40512e+07 | 1 | 1 | risk_breached_proxy |
| S08 | partial_strategy_proxy | stressed_retail | 1 | -1.68265e+07 | -244.676 | -1.68264e+07 | 1 | 1 | risk_breached_proxy |
| S08 | partial_strategy_proxy | zero_latency_spread_only_control | 1 | -1.61448e+06 | -126.773 | -1.6147e+06 | 1 | 1 | risk_breached_proxy |

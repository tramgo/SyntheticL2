# Phase 25 Event Replay Expansion

Generated UTC: 2026-07-14T17:54:22.910392+00:00

This milestone expands actual strategy execution over the Stage B2 event-ordered feature product.
It produces trade/order-style replay rows with Zerodha order-formula costs where applicable.
It is stronger than static planning, but it is still not acceptance-grade because it uses a small Stage B2 engineering subset.

## Summary

| metric | value | description |
| --- | --- | --- |
| phase25_models_replayed | 8 | Strategies and baselines replayed |
| phase25_strategy_models_replayed | 5 | Strategy models replayed |
| phase25_baseline_models_replayed | 3 | Baseline models replayed |
| phase25_execution_profiles | 3 | Execution profiles evaluated |
| phase25_total_trades | 113848 | Total event-order replay trades |
| phase25_positive_strategy_profile_rows | 0 | Strategy/profile rows with positive mean net return |
| phase25_risk_breached_rows | 12 | Model/profile rows with proxy risk breaches |
| phase25_beats_best_baseline_rows | 3 | Strategy/profile rows beating best baseline proxy |
| phase25_acceptance_ready | 0 | Event replay is execution evidence, not acceptance evidence |

## Replay Summary

| model_id | model_type | execution_profile | trades | symbols | scenario_days | mean_gross_return | mean_cost_return | mean_zerodha_charge_return | mean_net_return | win_rate_net | total_net_pnl_inr | market_shock_trade_fraction | disconnect_trade_fraction | acceptance_ready | replay_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B01 | baseline | retail_marketable_default | 2801 | 2 | 8 | 2.85904e-05 | 0.00190301 | 0.000826809 | -0.00187442 | 0.100678 | -525024 | 0.124598 | 0 | False | event_order_replay_not_acceptance |
| B01 | baseline | stressed_retail | 2723 | 2 | 8 | 7.52167e-05 | 0.00213583 | 0.000826808 | -0.00206062 | 0.0822622 | -561106 | 0.124495 | 0 | False | event_order_replay_not_acceptance |
| B01 | baseline | zero_latency_spread_only_control | 2951 | 2 | 8 | -2.2221e-05 | 0.000943912 | 0 | -0.000966133 | 0.257879 | -285106 | 0.125381 | 0.0010166 | False | event_order_replay_not_acceptance |
| B03 | baseline | retail_marketable_default | 13873 | 5 | 8 | 3.01351e-05 | 0.00113451 | 0.000826813 | -0.00110437 | 0.265768 | -1.5321e+06 | 0.123261 | 0 | False | event_order_replay_not_acceptance |
| B03 | baseline | stressed_retail | 13475 | 5 | 8 | -2.13817e-05 | 0.00132025 | 0.000826812 | -0.00134163 | 0.230649 | -1.80785e+06 | 0.123191 | 0 | False | event_order_replay_not_acceptance |
| B03 | baseline | zero_latency_spread_only_control | 14547 | 5 | 8 | -0.000250254 | 0.000222918 | 0 | -0.000473172 | 0.422974 | -688323 | 0.124424 | 0.000962398 | False | event_order_replay_not_acceptance |
| B06 | baseline | retail_marketable_default | 2801 | 2 | 8 | 4.24572e-05 | 0.00190301 | 0.000826809 | -0.00186055 | 0.10282 | -521140 | 0.124598 | 0 | False | event_order_replay_not_acceptance |
| B06 | baseline | stressed_retail | 2723 | 2 | 8 | 5.36632e-05 | 0.00213583 | 0.000826808 | -0.00208217 | 0.0811605 | -566975 | 0.124495 | 0 | False | event_order_replay_not_acceptance |
| B06 | baseline | zero_latency_spread_only_control | 2951 | 2 | 8 | 3.8009e-05 | 0.000943912 | 0 | -0.000905903 | 0.265673 | -267332 | 0.125381 | 0.0010166 | False | event_order_replay_not_acceptance |
| S01 | strategy | retail_marketable_default | 1449 | 4 | 8 | -2.23756e-05 | 0.000953595 | 0.000826822 | -0.000975971 | 0.322981 | -141418 | 0.200138 | 0 | False | event_order_replay_not_acceptance |
| S01 | strategy | stressed_retail | 1404 | 4 | 8 | 7.23217e-05 | 0.00113094 | 0.000826809 | -0.00105862 | 0.299858 | -148630 | 0.198718 | 0 | False | event_order_replay_not_acceptance |
| S01 | strategy | zero_latency_spread_only_control | 1524 | 4 | 8 | -0.00043616 | 4.86982e-05 | 0 | -0.000484858 | 0.477034 | -73892.4 | 0.197507 | 0 | False | event_order_replay_not_acceptance |
| S02 | strategy | retail_marketable_default | 9035 | 5 | 8 | -5.26556e-05 | 0.0011991 | 0.000826814 | -0.00125176 | 0.24228 | -1.13096e+06 | 0.135805 | 0 | False | event_order_replay_not_acceptance |
| S02 | strategy | stressed_retail | 8793 | 5 | 8 | 1.47712e-05 | 0.0013918 | 0.000826812 | -0.00137703 | 0.211646 | -1.21083e+06 | 0.136813 | 0 | False | event_order_replay_not_acceptance |
| S02 | strategy | zero_latency_spread_only_control | 9493 | 5 | 8 | -5.53825e-05 | 0.000280533 | 0 | -0.000335916 | 0.420415 | -318885 | 0.137786 | 0.000842726 | False | event_order_replay_not_acceptance |
| S05 | strategy | retail_marketable_default | 2801 | 2 | 8 | -4.67514e-05 | 0.00190414 | 0.00082681 | -0.00195089 | 0.0996073 | -546445 | 0.126383 | 0 | False | event_order_replay_not_acceptance |
| S05 | strategy | stressed_retail | 2723 | 2 | 8 | -5.43716e-05 | 0.00213701 | 0.00082681 | -0.00219139 | 0.0657363 | -596714 | 0.126331 | 0 | False | event_order_replay_not_acceptance |
| S05 | strategy | zero_latency_spread_only_control | 2951 | 2 | 8 | -2.96758e-05 | 0.000944979 | 0 | -0.000974655 | 0.265334 | -287621 | 0.127076 | 0.0010166 | False | event_order_replay_not_acceptance |
| S07 | strategy | retail_marketable_default | 2098 | 2 | 6 | 0.0001056 | 0.00193311 | 0.000826805 | -0.00182751 | 0.0981888 | -383412 | 0.166349 | 0 | False | event_order_replay_not_acceptance |
| S07 | strategy | stressed_retail | 2040 | 2 | 6 | 0.000128749 | 0.00216605 | 0.000826803 | -0.0020373 | 0.0745098 | -415610 | 0.166667 | 0 | False | event_order_replay_not_acceptance |
| S07 | strategy | zero_latency_spread_only_control | 2217 | 2 | 6 | 9.96971e-05 | 0.00097288 | 0 | -0.000873183 | 0.251691 | -193585 | 0.167343 | 0.00090212 | False | event_order_replay_not_acceptance |
| S09 | strategy | retail_marketable_default | 2801 | 2 | 8 | -4.24572e-05 | 0.00190301 | 0.00082681 | -0.00194546 | 0.101035 | -544925 | 0.124598 | 0 | False | event_order_replay_not_acceptance |
| S09 | strategy | stressed_retail | 2723 | 2 | 8 | -5.36632e-05 | 0.00213584 | 0.00082681 | -0.0021895 | 0.0657363 | -596201 | 0.124495 | 0 | False | event_order_replay_not_acceptance |
| S09 | strategy | zero_latency_spread_only_control | 2951 | 2 | 8 | -3.8009e-05 | 0.000943912 | 0 | -0.000981921 | 0.264995 | -289765 | 0.125381 | 0.0010166 | False | event_order_replay_not_acceptance |

## Risk Summary

| model_id | model_type | execution_profile | trade_dates | worst_daily_net_pnl_inr | tail_loss_1pct_trade_pnl_inr | max_intraday_drawdown_inr | daily_loss_breach_days | drawdown_breach_days | risk_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B01 | baseline | retail_marketable_default | 8 | -84102.3 | -722.837 | -84200.9 | 1 | 0 | risk_breached_proxy |
| B01 | baseline | stressed_retail | 8 | -84310.2 | -760.446 | -84333.3 | 1 | 0 | risk_breached_proxy |
| B01 | baseline | zero_latency_spread_only_control | 8 | -55359.6 | -661.409 | -55074.7 | 0 | 0 | risk_not_breached_proxy |
| B03 | baseline | retail_marketable_default | 8 | -226550 | -726.949 | -226361 | 8 | 8 | risk_breached_proxy |
| B03 | baseline | stressed_retail | 8 | -276034 | -843.021 | -275673 | 8 | 8 | risk_breached_proxy |
| B03 | baseline | zero_latency_spread_only_control | 8 | -192152 | -833.264 | -192252 | 3 | 3 | risk_breached_proxy |
| B06 | baseline | retail_marketable_default | 8 | -73481.9 | -761.246 | -73016.1 | 0 | 0 | risk_not_breached_proxy |
| B06 | baseline | stressed_retail | 8 | -77594.8 | -805.113 | -77111.2 | 2 | 0 | risk_breached_proxy |
| B06 | baseline | zero_latency_spread_only_control | 8 | -40310.1 | -668.745 | -40114 | 0 | 0 | risk_not_breached_proxy |
| S01 | strategy | retail_marketable_default | 8 | -35211.8 | -956.839 | -35361.2 | 0 | 0 | risk_not_breached_proxy |
| S01 | strategy | stressed_retail | 8 | -40747.1 | -738.136 | -40393.5 | 0 | 0 | risk_not_breached_proxy |
| S01 | strategy | zero_latency_spread_only_control | 8 | -48018.5 | -1048.94 | -49084.9 | 0 | 0 | risk_not_breached_proxy |
| S02 | strategy | retail_marketable_default | 8 | -182570 | -867.004 | -183467 | 8 | 8 | risk_breached_proxy |
| S02 | strategy | stressed_retail | 8 | -168802 | -716.328 | -168560 | 8 | 8 | risk_breached_proxy |
| S02 | strategy | zero_latency_spread_only_control | 8 | -50894.4 | -648.936 | -68919.5 | 0 | 0 | risk_not_breached_proxy |
| S05 | strategy | retail_marketable_default | 8 | -95669 | -768.4 | -95709.1 | 1 | 0 | risk_breached_proxy |
| S05 | strategy | stressed_retail | 8 | -102416 | -812.485 | -102404 | 1 | 1 | risk_breached_proxy |
| S05 | strategy | zero_latency_spread_only_control | 8 | -67120.1 | -685.66 | -66726.5 | 0 | 0 | risk_not_breached_proxy |
| S07 | strategy | retail_marketable_default | 6 | -73503.4 | -819.656 | -73037.5 | 0 | 0 | risk_not_breached_proxy |
| S07 | strategy | stressed_retail | 6 | -73987.5 | -843.021 | -73503.9 | 0 | 0 | risk_not_breached_proxy |
| S07 | strategy | zero_latency_spread_only_control | 6 | -42110.8 | -719.485 | -42413.2 | 0 | 0 | risk_not_breached_proxy |
| S09 | strategy | retail_marketable_default | 8 | -94141.3 | -768.4 | -94181.3 | 1 | 0 | risk_breached_proxy |
| S09 | strategy | stressed_retail | 8 | -100945 | -812.485 | -100934 | 1 | 1 | risk_breached_proxy |
| S09 | strategy | zero_latency_spread_only_control | 8 | -68200.8 | -685.66 | -67807.3 | 0 | 0 | risk_not_breached_proxy |

## Baseline Comparison

| model_id | execution_profile | strategy_mean_net_return | best_baseline_mean_net_return | net_return_lift_vs_best_baseline | beats_best_baseline_proxy | comparison_scope |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | retail_marketable_default | -0.000975971 | -0.00110437 | 0.000128403 | True | stage_b2_event_replay_proxy |
| S01 | stressed_retail | -0.00105862 | -0.00134163 | 0.000283011 | True | stage_b2_event_replay_proxy |
| S01 | zero_latency_spread_only_control | -0.000484858 | -0.000473172 | -1.16862e-05 | False | stage_b2_event_replay_proxy |
| S02 | retail_marketable_default | -0.00125176 | -0.00110437 | -0.000147386 | False | stage_b2_event_replay_proxy |
| S02 | stressed_retail | -0.00137703 | -0.00134163 | -3.54045e-05 | False | stage_b2_event_replay_proxy |
| S02 | zero_latency_spread_only_control | -0.000335916 | -0.000473172 | 0.000137256 | True | stage_b2_event_replay_proxy |
| S05 | retail_marketable_default | -0.00195089 | -0.00110437 | -0.000846519 | False | stage_b2_event_replay_proxy |
| S05 | stressed_retail | -0.00219139 | -0.00134163 | -0.000849757 | False | stage_b2_event_replay_proxy |
| S05 | zero_latency_spread_only_control | -0.000974655 | -0.000473172 | -0.000501483 | False | stage_b2_event_replay_proxy |
| S07 | retail_marketable_default | -0.00182751 | -0.00110437 | -0.000723137 | False | stage_b2_event_replay_proxy |
| S07 | stressed_retail | -0.0020373 | -0.00134163 | -0.000695673 | False | stage_b2_event_replay_proxy |
| S07 | zero_latency_spread_only_control | -0.000873183 | -0.000473172 | -0.000400011 | False | stage_b2_event_replay_proxy |
| S09 | retail_marketable_default | -0.00194546 | -0.00110437 | -0.000841091 | False | stage_b2_event_replay_proxy |
| S09 | stressed_retail | -0.0021895 | -0.00134163 | -0.000847871 | False | stage_b2_event_replay_proxy |
| S09 | zero_latency_spread_only_control | -0.000981921 | -0.000473172 | -0.000508749 | False | stage_b2_event_replay_proxy |

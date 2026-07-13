# Phase 12 Execution Simulator Report

Generated UTC: 2026-07-13T16:18:43.766106+00:00

## Scope

This is the first marketable-order execution proxy over Phase 9 Tier C feature events and Phase 11 proxy signals.
It applies event-latency shifts, stale/disconnect cancellation, spread/slippage/profile-fee costs and one-step mark-to-next-event P&L.
It is not a tick-accurate queue simulator and must not be used for strategy acceptance.

## Execution Profile Overview

| execution_profile | strategies | trades | mean_net_return | total_net_pnl_units |
| --- | --- | --- | --- | --- |
| retail_marketable_default | 9 | 3423379 | 0.000972142 | 1209.71 |
| stressed_retail | 9 | 3389678 | -0.000758381 | -2757.51 |
| zero_latency_spread_only_control | 9 | 3537597 | -0.00175777 | -3800.61 |

## Strategy/Profile Summary

| strategy_id | execution_profile | trades | mean_gross_return | mean_cost_return | mean_net_return | win_rate_net | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | retail_marketable_default | 160629 | 0.00744598 | 0.000348576 | 0.00709741 | 0.617286 | simulated_marketable_proxy_not_acceptance |
| S01 | stressed_retail | 158348 | 0.000164358 | 0.000710917 | -0.000546559 | 0.478333 | simulated_marketable_proxy_not_acceptance |
| S01 | zero_latency_spread_only_control | 166910 | -0.00785586 | 9.03624e-05 | -0.00794622 | 0.355767 | simulated_marketable_proxy_not_acceptance |
| S02 | retail_marketable_default | 870505 | 3.8756e-05 | 0.000506832 | -0.000468076 | 0.489151 | simulated_marketable_proxy_not_acceptance |
| S02 | stressed_retail | 862030 | 9.22067e-06 | 0.000909244 | -0.000900023 | 0.477762 | simulated_marketable_proxy_not_acceptance |
| S02 | zero_latency_spread_only_control | 898020 | -9.54452e-05 | 0.00020707 | -0.000302515 | 0.492408 | simulated_marketable_proxy_not_acceptance |
| S03 | retail_marketable_default | 273433 | 0.00599094 | 0.000286006 | 0.00570493 | 0.581305 | simulated_marketable_proxy_not_acceptance |
| S03 | stressed_retail | 271051 | 0.000386179 | 0.000612951 | -0.000226772 | 0.490196 | simulated_marketable_proxy_not_acceptance |
| S03 | zero_latency_spread_only_control | 283344 | -0.00661601 | 7.12232e-05 | -0.00668723 | 0.405574 | simulated_marketable_proxy_not_acceptance |
| S04 | retail_marketable_default | 414097 | 0.000700428 | 0.000422657 | 0.000277771 | 0.504995 | simulated_marketable_proxy_not_acceptance |
| S04 | stressed_retail | 410639 | -6.61458e-05 | 0.00078298 | -0.000849126 | 0.479701 | simulated_marketable_proxy_not_acceptance |
| S04 | zero_latency_spread_only_control | 429109 | -0.000731257 | 0.000200711 | -0.000931968 | 0.483166 | simulated_marketable_proxy_not_acceptance |
| S05 | retail_marketable_default | 436366 | -0.000951408 | 0.000621957 | -0.00157336 | 0.461947 | simulated_marketable_proxy_not_acceptance |
| S05 | stressed_retail | 432404 | 5.17184e-05 | 0.00103794 | -0.000986218 | 0.466557 | simulated_marketable_proxy_not_acceptance |
| S05 | zero_latency_spread_only_control | 449723 | 0.00149889 | 0.000334287 | 0.0011646 | 0.503712 | simulated_marketable_proxy_not_acceptance |
| S06 | retail_marketable_default | 32989 | -0.000699299 | 0.000434174 | -0.00113347 | 0.485071 | simulated_marketable_proxy_not_acceptance |
| S06 | stressed_retail | 32771 | 0.000157292 | 0.000798658 | -0.000641366 | 0.49022 | simulated_marketable_proxy_not_acceptance |
| S06 | zero_latency_spread_only_control | 34199 | 0.000394906 | 0.000209694 | 0.000185212 | 0.494459 | simulated_marketable_proxy_not_acceptance |
| S07 | retail_marketable_default | 229939 | 0.000322956 | 0.000712422 | -0.000389466 | 0.489752 | simulated_marketable_proxy_not_acceptance |
| S07 | stressed_retail | 227954 | 7.53148e-05 | 0.0011432 | -0.00106789 | 0.479141 | simulated_marketable_proxy_not_acceptance |
| S07 | zero_latency_spread_only_control | 237102 | -0.000491488 | 0.000382349 | -0.000873837 | 0.484521 | simulated_marketable_proxy_not_acceptance |
| S08 | retail_marketable_default | 432090 | 2.88221e-05 | 0.000419057 | -0.000390235 | 0.491578 | simulated_marketable_proxy_not_acceptance |
| S08 | stressed_retail | 426402 | -6.02431e-05 | 0.000780441 | -0.000840685 | 0.48087 | simulated_marketable_proxy_not_acceptance |
| S08 | zero_latency_spread_only_control | 448520 | 3.12771e-06 | 0.00015771 | -0.000154582 | 0.496232 | simulated_marketable_proxy_not_acceptance |
| S09 | retail_marketable_default | 573331 | 0.000180631 | 0.000556846 | -0.000376215 | 0.479976 | simulated_marketable_proxy_not_acceptance |
| S09 | stressed_retail | 568079 | 0.00019675 | 0.000963542 | -0.000766792 | 0.470644 | simulated_marketable_proxy_not_acceptance |
| S09 | zero_latency_spread_only_control | 590670 | -2.31062e-05 | 0.000250304 | -0.00027341 | 0.482606 | simulated_marketable_proxy_not_acceptance |

## Caveats

- Current features are 5-minute synthetic feature events, not true tick-level order events.
- Passive orders, partial fills, cancel/replace and order rejections are represented as requirements, not realistic queue simulation.
- Explicit fees are placeholder profile-level bps assumptions, not verified brokerage/statutory/exchange charges.
- Refresh costs from broker/exchange sources before making economic or deployability claims.
- Spread crossing, fixed slippage and impact remain internal execution assumptions.
- Zero-latency/spread-only profile is a leakage/control profile, not a deployable model.

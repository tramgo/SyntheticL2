# Phase 12 Execution Simulator Report

Generated UTC: 2026-07-13T20:19:03.602431+00:00

## Scope

This is the first marketable-order execution proxy over Phase 9 Tier C feature events and Phase 11 proxy signals.
It applies event-latency shifts, stale/disconnect cancellation, spread/slippage/profile-fee costs and one-step mark-to-next-event P&L.
It is not a tick-accurate queue simulator and must not be used for strategy acceptance.

## Execution Profile Overview

| execution_profile | strategies | trades | mean_net_return | total_net_pnl_units |
| --- | --- | --- | --- | --- |
| retail_marketable_default | 9 | 3423379 | 6.14539e-05 | -1907.92 |
| stressed_retail | 9 | 3389678 | -0.00151907 | -5335.99 |
| zero_latency_spread_only_control | 9 | 3537597 | -0.00175777 | -3800.61 |

## Strategy/Profile Summary

| strategy_id | execution_profile | trades | mean_gross_return | mean_cost_return | mean_net_return | win_rate_net | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | retail_marketable_default | 160629 | 0.00744598 | 0.00125926 | 0.00618672 | 0.603023 | simulated_marketable_proxy_not_acceptance |
| S01 | stressed_retail | 158348 | 0.000164358 | 0.0014716 | -0.00130725 | 0.461452 | simulated_marketable_proxy_not_acceptance |
| S01 | zero_latency_spread_only_control | 166910 | -0.00785586 | 9.03624e-05 | -0.00794622 | 0.355767 | simulated_marketable_proxy_not_acceptance |
| S02 | retail_marketable_default | 870505 | 3.8756e-05 | 0.00141752 | -0.00137876 | 0.469293 | simulated_marketable_proxy_not_acceptance |
| S02 | stressed_retail | 862030 | 9.22067e-06 | 0.00166993 | -0.00166071 | 0.46099 | simulated_marketable_proxy_not_acceptance |
| S02 | zero_latency_spread_only_control | 898020 | -9.54452e-05 | 0.00020707 | -0.000302515 | 0.492408 | simulated_marketable_proxy_not_acceptance |
| S03 | retail_marketable_default | 273433 | 0.00599094 | 0.00119669 | 0.00479424 | 0.568969 | simulated_marketable_proxy_not_acceptance |
| S03 | stressed_retail | 271051 | 0.000386179 | 0.00137364 | -0.00098746 | 0.475446 | simulated_marketable_proxy_not_acceptance |
| S03 | zero_latency_spread_only_control | 283344 | -0.00661601 | 7.12232e-05 | -0.00668723 | 0.405574 | simulated_marketable_proxy_not_acceptance |
| S04 | retail_marketable_default | 414097 | 0.000700428 | 0.00133334 | -0.000632917 | 0.49229 | simulated_marketable_proxy_not_acceptance |
| S04 | stressed_retail | 410639 | -6.61458e-05 | 0.00154367 | -0.00160981 | 0.463748 | simulated_marketable_proxy_not_acceptance |
| S04 | zero_latency_spread_only_control | 429109 | -0.000731257 | 0.000200711 | -0.000931968 | 0.483166 | simulated_marketable_proxy_not_acceptance |
| S05 | retail_marketable_default | 436366 | -0.000951408 | 0.00153265 | -0.00248405 | 0.440043 | simulated_marketable_proxy_not_acceptance |
| S05 | stressed_retail | 432404 | 5.17184e-05 | 0.00179862 | -0.00174691 | 0.449062 | simulated_marketable_proxy_not_acceptance |
| S05 | zero_latency_spread_only_control | 449723 | 0.00149889 | 0.000334287 | 0.0011646 | 0.503712 | simulated_marketable_proxy_not_acceptance |
| S06 | retail_marketable_default | 32989 | -0.000699299 | 0.00134486 | -0.00204416 | 0.471005 | simulated_marketable_proxy_not_acceptance |
| S06 | stressed_retail | 32771 | 0.000157292 | 0.00155935 | -0.00140205 | 0.47478 | simulated_marketable_proxy_not_acceptance |
| S06 | zero_latency_spread_only_control | 34199 | 0.000394906 | 0.000209694 | 0.000185212 | 0.494459 | simulated_marketable_proxy_not_acceptance |
| S07 | retail_marketable_default | 229939 | 0.000322956 | 0.00162311 | -0.00130015 | 0.465489 | simulated_marketable_proxy_not_acceptance |
| S07 | stressed_retail | 227954 | 7.53148e-05 | 0.00190389 | -0.00182858 | 0.459873 | simulated_marketable_proxy_not_acceptance |
| S07 | zero_latency_spread_only_control | 237102 | -0.000491488 | 0.000382349 | -0.000873837 | 0.484521 | simulated_marketable_proxy_not_acceptance |
| S08 | retail_marketable_default | 432090 | 2.88221e-05 | 0.00132974 | -0.00130092 | 0.471971 | simulated_marketable_proxy_not_acceptance |
| S08 | stressed_retail | 426402 | -6.02431e-05 | 0.00154113 | -0.00160137 | 0.464902 | simulated_marketable_proxy_not_acceptance |
| S08 | zero_latency_spread_only_control | 448520 | 3.12771e-06 | 0.00015771 | -0.000154582 | 0.496232 | simulated_marketable_proxy_not_acceptance |
| S09 | retail_marketable_default | 573331 | 0.000180631 | 0.00146753 | -0.0012869 | 0.457629 | simulated_marketable_proxy_not_acceptance |
| S09 | stressed_retail | 568079 | 0.00019675 | 0.00172423 | -0.00152748 | 0.452729 | simulated_marketable_proxy_not_acceptance |
| S09 | zero_latency_spread_only_control | 590670 | -2.31062e-05 | 0.000250304 | -0.00027341 | 0.482606 | simulated_marketable_proxy_not_acceptance |

## Caveats

- Current features are 5-minute synthetic feature events, not true tick-level order events.
- Sampled trades carry a deterministic seed column assigned from the Phase 13 seed plan by quarter profile and scenario day; this is reporting lineage, not independent multi-seed acceptance evidence.
- Passive orders, partial fills, cancel/replace and order rejections are represented as requirements, not realistic queue simulation.
- Zerodha equity-intraday statutory/brokerage charges are modeled as a normalized bps estimate for returns and as representative rupee order-formula scenarios.
- The rupee scenarios apply the brokerage cap and STT rounding, but DP charges, broker contract-note rounding and actual broker fills remain outside the normalized return proxy.
- Spread crossing, fixed slippage and impact remain internal execution assumptions.
- Zero-latency/spread-only profile is a leakage/control profile, not a deployable model.

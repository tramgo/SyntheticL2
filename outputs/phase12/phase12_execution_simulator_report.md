# Phase 12 Execution Simulator Report

Generated UTC: 2026-07-13T20:34:49.506867+00:00

## Scope

This is the first marketable-order execution proxy over Phase 9 Tier C feature events and Phase 11 proxy signals.
It applies event-latency shifts, stale/disconnect cancellation, spread/slippage/profile-fee costs and one-step mark-to-next-event P&L.
It is not a tick-accurate queue simulator and must not be used for strategy acceptance.

## Execution Profile Overview

| execution_profile | strategies | trades | mean_net_return | total_net_pnl_units |
| --- | --- | --- | --- | --- |
| retail_marketable_default | 9 | 3431146 | 6.91002e-05 | -1915.3 |
| stressed_retail | 9 | 3397772 | -0.00151803 | -5363.6 |
| zero_latency_spread_only_control | 9 | 3546942 | -0.00174877 | -3775.44 |

## Strategy/Profile Summary

| strategy_id | execution_profile | trades | mean_gross_return | mean_cost_return | mean_net_return | win_rate_net | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | retail_marketable_default | 160471 | 0.00747604 | 0.00125895 | 0.00621709 | 0.60333 | simulated_marketable_proxy_not_acceptance |
| S01 | stressed_retail | 158070 | 0.000103743 | 0.00147102 | -0.00136728 | 0.459961 | simulated_marketable_proxy_not_acceptance |
| S01 | zero_latency_spread_only_control | 166760 | -0.00783377 | 9.00559e-05 | -0.00792383 | 0.355625 | simulated_marketable_proxy_not_acceptance |
| S02 | retail_marketable_default | 879151 | 4.01977e-05 | 0.00141713 | -0.00137693 | 0.469246 | simulated_marketable_proxy_not_acceptance |
| S02 | stressed_retail | 870977 | -2.82146e-06 | 0.00166907 | -0.00167189 | 0.460865 | simulated_marketable_proxy_not_acceptance |
| S02 | zero_latency_spread_only_control | 907352 | -9.21563e-05 | 0.000206934 | -0.00029909 | 0.492282 | simulated_marketable_proxy_not_acceptance |
| S03 | retail_marketable_default | 273427 | 0.00598365 | 0.00119667 | 0.00478697 | 0.569501 | simulated_marketable_proxy_not_acceptance |
| S03 | stressed_retail | 270999 | 0.000369251 | 0.00137357 | -0.00100432 | 0.475854 | simulated_marketable_proxy_not_acceptance |
| S03 | zero_latency_spread_only_control | 283411 | -0.00659093 | 7.12069e-05 | -0.00666214 | 0.406025 | simulated_marketable_proxy_not_acceptance |
| S04 | retail_marketable_default | 414066 | 0.000698138 | 0.00133333 | -0.000635192 | 0.49204 | simulated_marketable_proxy_not_acceptance |
| S04 | stressed_retail | 410666 | -7.55037e-05 | 0.0015436 | -0.0016191 | 0.46343 | simulated_marketable_proxy_not_acceptance |
| S04 | zero_latency_spread_only_control | 429202 | -0.000711055 | 0.000200568 | -0.000911623 | 0.483248 | simulated_marketable_proxy_not_acceptance |
| S05 | retail_marketable_default | 436284 | -0.000952926 | 0.00153257 | -0.00248549 | 0.439936 | simulated_marketable_proxy_not_acceptance |
| S05 | stressed_retail | 432377 | 6.93865e-05 | 0.00179854 | -0.00172915 | 0.449161 | simulated_marketable_proxy_not_acceptance |
| S05 | zero_latency_spread_only_control | 449765 | 0.00149924 | 0.000334175 | 0.00116507 | 0.503579 | simulated_marketable_proxy_not_acceptance |
| S06 | retail_marketable_default | 33129 | -0.000654282 | 0.00134295 | -0.00199724 | 0.47146 | simulated_marketable_proxy_not_acceptance |
| S06 | stressed_retail | 32935 | 0.000252699 | 0.00155586 | -0.00130317 | 0.476029 | simulated_marketable_proxy_not_acceptance |
| S06 | zero_latency_spread_only_control | 34373 | 0.000393546 | 0.000208012 | 0.000185533 | 0.495389 | simulated_marketable_proxy_not_acceptance |
| S07 | retail_marketable_default | 229792 | 0.000323144 | 0.00162331 | -0.00130017 | 0.465699 | simulated_marketable_proxy_not_acceptance |
| S07 | stressed_retail | 227842 | 4.60237e-05 | 0.00190395 | -0.00185793 | 0.459397 | simulated_marketable_proxy_not_acceptance |
| S07 | zero_latency_spread_only_control | 237064 | -0.000491173 | 0.000382406 | -0.000873579 | 0.484494 | simulated_marketable_proxy_not_acceptance |
| S08 | retail_marketable_default | 431798 | 3.04967e-05 | 0.00132984 | -0.00129934 | 0.472042 | simulated_marketable_proxy_not_acceptance |
| S08 | stressed_retail | 426101 | -4.7918e-05 | 0.00154122 | -0.00158913 | 0.465171 | simulated_marketable_proxy_not_acceptance |
| S08 | zero_latency_spread_only_control | 448403 | 9.43769e-06 | 0.000157571 | -0.000148133 | 0.495951 | simulated_marketable_proxy_not_acceptance |
| S09 | retail_marketable_default | 573028 | 0.000179962 | 0.00146775 | -0.00128779 | 0.457531 | simulated_marketable_proxy_not_acceptance |
| S09 | stressed_retail | 567805 | 0.000204235 | 0.00172449 | -0.00152025 | 0.452747 | simulated_marketable_proxy_not_acceptance |
| S09 | zero_latency_spread_only_control | 590612 | -2.08091e-05 | 0.000250359 | -0.000271168 | 0.482628 | simulated_marketable_proxy_not_acceptance |

## Caveats

- Current features are 5-minute synthetic feature events, not true tick-level order events.
- Sampled trades carry a deterministic seed column assigned from the Phase 13 seed plan by quarter profile and scenario day; this is reporting lineage, not independent multi-seed acceptance evidence.
- Passive orders, partial fills, cancel/replace and order rejections are represented as requirements, not realistic queue simulation.
- Zerodha equity-intraday statutory/brokerage charges are modeled as a normalized bps estimate for returns and as representative rupee order-formula scenarios.
- The rupee scenarios apply the brokerage cap and STT rounding, but DP charges, broker contract-note rounding and actual broker fills remain outside the normalized return proxy.
- Spread crossing, fixed slippage and impact remain internal execution assumptions.
- Zero-latency/spread-only profile is a leakage/control profile, not a deployable model.

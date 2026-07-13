# Phase 12 Execution Simulator Report

Generated UTC: 2026-07-13T21:14:14.204109+00:00

## Scope

This is the first marketable-order execution proxy over Phase 9 Tier C feature events and Phase 11 proxy signals.
It applies event-latency shifts, stale/disconnect cancellation, spread/slippage/profile-fee costs and one-step mark-to-next-event P&L.
It is not a tick-accurate queue simulator and must not be used for strategy acceptance.

## Execution Profile Overview

| execution_profile | strategies | trades | mean_net_return | total_net_pnl_units | total_net_pnl_inr | mean_zerodha_charge_bps |
| --- | --- | --- | --- | --- | --- | --- |
| retail_marketable_default | 9 | 3431146 | 0.000303233 | -1112.26 | -1.11226e+08 | 8.26555 |
| stressed_retail | 9 | 3397772 | -0.00128424 | -4569.2 | -4.5692e+08 | 8.26903 |
| zero_latency_spread_only_control | 9 | 3546942 | -0.00174877 | -3775.44 | -3.77544e+08 | 0 |

## Strategy/Profile Summary

| strategy_id | execution_profile | trades | mean_gross_return | mean_cost_return | mean_zerodha_charge_bps | mean_net_return | total_net_pnl_inr | win_rate_net | zerodha_charge_model_basis | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | retail_marketable_default | 160471 | 0.00747604 | 0.00102492 | 8.26659 | 0.00645112 | 1.03522e+08 | 0.606994 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S01 | stressed_retail | 158070 | 0.000103743 | 0.00123716 | 8.26825 | -0.00113342 | -1.79159e+07 | 0.464668 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S01 | zero_latency_spread_only_control | 166760 | -0.00783377 | 9.00559e-05 | 0 | -0.00792383 | -1.32138e+08 | 0.355625 | not_applied_control_profile | simulated_marketable_proxy_not_acceptance |
| S02 | retail_marketable_default | 879151 | 4.01977e-05 | 0.00118328 | 8.26839 | -0.00114308 | -1.00494e+08 | 0.474953 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S02 | stressed_retail | 870977 | -2.82146e-06 | 0.00143524 | 8.26859 | -0.00143806 | -1.25252e+08 | 0.466183 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S02 | zero_latency_spread_only_control | 907352 | -9.21563e-05 | 0.000206934 | 0 | -0.00029909 | -2.7138e+07 | 0.492282 | not_applied_control_profile | simulated_marketable_proxy_not_acceptance |
| S03 | retail_marketable_default | 273427 | 0.00598365 | 0.000962057 | 8.2607 | 0.00502159 | 1.37304e+08 | 0.57257 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S03 | stressed_retail | 270999 | 0.000369251 | 0.00113991 | 8.27025 | -0.00077066 | -2.08848e+07 | 0.480053 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S03 | zero_latency_spread_only_control | 283411 | -0.00659093 | 7.12069e-05 | 0 | -0.00666214 | -1.88812e+08 | 0.406025 | not_applied_control_profile | simulated_marketable_proxy_not_acceptance |
| S04 | retail_marketable_default | 414066 | 0.000698138 | 0.00109879 | 8.26147 | -0.000400651 | -1.65896e+07 | 0.495513 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S04 | stressed_retail | 410666 | -7.55037e-05 | 0.00130996 | 8.27049 | -0.00138546 | -5.68963e+07 | 0.46821 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S04 | zero_latency_spread_only_control | 429202 | -0.000711055 | 0.000200568 | 0 | -0.000911623 | -3.9127e+07 | 0.483248 | not_applied_control_profile | simulated_marketable_proxy_not_acceptance |
| S05 | retail_marketable_default | 436284 | -0.000952926 | 0.00129854 | 8.26659 | -0.00225147 | -9.82279e+07 | 0.445618 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S05 | stressed_retail | 432377 | 6.93865e-05 | 0.0015647 | 8.26847 | -0.00149531 | -6.46538e+07 | 0.454691 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S05 | zero_latency_spread_only_control | 449765 | 0.00149924 | 0.000334175 | 0 | 0.00116507 | 5.24008e+07 | 0.503579 | not_applied_control_profile | simulated_marketable_proxy_not_acceptance |
| S06 | retail_marketable_default | 33129 | -0.000654282 | 0.00110855 | 8.26287 | -0.00176284 | -5.8401e+06 | 0.474811 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S06 | stressed_retail | 32935 | 0.000252699 | 0.00132216 | 8.26979 | -0.00106946 | -3.52225e+06 | 0.48034 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S06 | zero_latency_spread_only_control | 34373 | 0.000393546 | 0.000208012 | 0 | 0.000185533 | 637734 | 0.495389 | not_applied_control_profile | simulated_marketable_proxy_not_acceptance |
| S07 | retail_marketable_default | 229792 | 0.000323144 | 0.00138933 | 8.267 | -0.00106618 | -2.45e+07 | 0.473293 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S07 | stressed_retail | 227842 | 4.60237e-05 | 0.00167017 | 8.26903 | -0.00162415 | -3.70049e+07 | 0.465889 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S07 | zero_latency_spread_only_control | 237064 | -0.000491173 | 0.000382406 | 0 | -0.000873579 | -2.07094e+07 | 0.484494 | not_applied_control_profile | simulated_marketable_proxy_not_acceptance |
| S08 | retail_marketable_default | 431798 | 3.04967e-05 | 0.00109593 | 8.2678 | -0.00106543 | -4.60051e+07 | 0.477225 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S08 | stressed_retail | 426101 | -4.7918e-05 | 0.00130731 | 8.26778 | -0.00135522 | -5.77463e+07 | 0.469896 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S08 | zero_latency_spread_only_control | 448403 | 9.43769e-06 | 0.000157571 | 0 | -0.000148133 | -6.64233e+06 | 0.495951 | not_applied_control_profile | simulated_marketable_proxy_not_acceptance |
| S09 | retail_marketable_default | 573028 | 0.000179962 | 0.00123392 | 8.26857 | -0.00105396 | -6.0395e+07 | 0.463148 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S09 | stressed_retail | 567805 | 0.000204235 | 0.00149066 | 8.2686 | -0.00128642 | -7.30437e+07 | 0.458492 | zerodha_equity_intraday_nse_order_formula_per_trade | simulated_marketable_proxy_not_acceptance |
| S09 | zero_latency_spread_only_control | 590612 | -2.08091e-05 | 0.000250359 | 0 | -0.000271168 | -1.60155e+07 | 0.482628 | not_applied_control_profile | simulated_marketable_proxy_not_acceptance |

## Caveats

- Current features are 5-minute synthetic feature events, not true tick-level order events.
- Sampled trades carry a deterministic seed column assigned from the Phase 13 seed plan by quarter profile and scenario day; this is reporting lineage, not independent multi-seed acceptance evidence.
- Passive orders, partial fills, cancel/replace and order rejections are represented as requirements, not realistic queue simulation.
- Retail and stressed profiles apply the Zerodha equity-intraday NSE rupee order formula per simulated round trip using configured `order_notional_inr`, including brokerage cap, STT rounding, transaction charge, SEBI charge, stamp duty and GST.
- Representative rupee scenarios are retained for auditability; DP charges, broker contract-note rounding and actual broker fills remain outside this proxy.
- Spread crossing, fixed slippage and impact remain internal execution assumptions.
- Zero-latency/spread-only profile is a leakage/control profile, not a deployable model.

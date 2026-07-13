# Phase 12 Execution Simulator Report

Generated UTC: 2026-07-13T21:22:12.023451+00:00

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

## Full-Run Risk Proxy Summary

| strategy_id | execution_profile | trades | trade_dates | worst_daily_net_pnl_inr | tail_loss_1pct_trade_pnl_inr | max_intraday_drawdown_inr | daily_loss_warn_days | drawdown_warn_days | position_warn_days | risk_evidence_scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | retail_marketable_default | 160471 | 63 | -294196 | -6718.93 | -363951 | 2 | 3 | 17 | full_execution_summary_proxy_no_fills |
| S01 | stressed_retail | 158070 | 63 | -4.38609e+06 | -6355.9 | -4.38461e+06 | 39 | 41 | 18 | full_execution_summary_proxy_no_fills |
| S01 | zero_latency_spread_only_control | 166760 | 63 | -7.73645e+06 | -8314.01 | -7.738e+06 | 63 | 63 | 20 | full_execution_summary_proxy_no_fills |
| S02 | retail_marketable_default | 879151 | 63 | -2.4282e+06 | -7016.36 | -2.45888e+06 | 63 | 63 | 0 | full_execution_summary_proxy_no_fills |
| S02 | stressed_retail | 870977 | 63 | -3.02469e+06 | -6833.91 | -3.02458e+06 | 63 | 63 | 0 | full_execution_summary_proxy_no_fills |
| S02 | zero_latency_spread_only_control | 907352 | 63 | -1.7356e+06 | -6949.47 | -1.77975e+06 | 55 | 61 | 0 | full_execution_summary_proxy_no_fills |
| S03 | retail_marketable_default | 273427 | 60 | -395511 | -7999.18 | -408842 | 6 | 7 | 22 | full_execution_summary_proxy_no_fills |
| S03 | stressed_retail | 270999 | 60 | -6.02188e+06 | -6299.45 | -6.02478e+06 | 27 | 31 | 22 | full_execution_summary_proxy_no_fills |
| S03 | zero_latency_spread_only_control | 283411 | 60 | -2.7519e+07 | -9467.71 | -2.75202e+07 | 44 | 44 | 22 | full_execution_summary_proxy_no_fills |
| S04 | retail_marketable_default | 414066 | 60 | -4.02483e+06 | -8776.85 | -4.09426e+06 | 26 | 37 | 6 | full_execution_summary_proxy_no_fills |
| S04 | stressed_retail | 410666 | 60 | -3.86432e+06 | -6609.02 | -3.90628e+06 | 41 | 40 | 6 | full_execution_summary_proxy_no_fills |
| S04 | zero_latency_spread_only_control | 429202 | 60 | -4.32104e+06 | -8640.5 | -4.33786e+06 | 42 | 44 | 5 | full_execution_summary_proxy_no_fills |
| S05 | retail_marketable_default | 436284 | 63 | -4.82368e+06 | -7045.1 | -4.8965e+06 | 58 | 63 | 63 | full_execution_summary_proxy_no_fills |
| S05 | stressed_retail | 432377 | 63 | -8.04801e+06 | -6847.87 | -8.06818e+06 | 54 | 63 | 63 | full_execution_summary_proxy_no_fills |
| S05 | zero_latency_spread_only_control | 449765 | 63 | -2.31953e+06 | -6403.69 | -2.32885e+06 | 14 | 37 | 63 | full_execution_summary_proxy_no_fills |
| S06 | retail_marketable_default | 33129 | 54 | -941443 | -8520.49 | -992879 | 21 | 22 | 0 | full_execution_summary_proxy_no_fills |
| S06 | stressed_retail | 32935 | 54 | -521309 | -6296.75 | -525307 | 18 | 17 | 0 | full_execution_summary_proxy_no_fills |
| S06 | zero_latency_spread_only_control | 34373 | 54 | -282528 | -8358.8 | -443046 | 11 | 15 | 0 | full_execution_summary_proxy_no_fills |
| S07 | retail_marketable_default | 229792 | 59 | -1.63271e+06 | -6787.47 | -1.81724e+06 | 44 | 54 | 44 | full_execution_summary_proxy_no_fills |
| S07 | stressed_retail | 227842 | 59 | -2.59844e+06 | -6158.01 | -2.65117e+06 | 44 | 57 | 44 | full_execution_summary_proxy_no_fills |
| S07 | zero_latency_spread_only_control | 237064 | 59 | -3.81934e+06 | -6286.31 | -3.82588e+06 | 44 | 51 | 44 | full_execution_summary_proxy_no_fills |
| S08 | retail_marketable_default | 431798 | 63 | -2.01361e+06 | -7141.42 | -2.0188e+06 | 62 | 62 | 42 | full_execution_summary_proxy_no_fills |
| S08 | stressed_retail | 426101 | 63 | -2.33058e+06 | -7175.83 | -2.33786e+06 | 63 | 63 | 36 | full_execution_summary_proxy_no_fills |
| S08 | zero_latency_spread_only_control | 448403 | 63 | -1.00346e+06 | -7020.09 | -1.0129e+06 | 33 | 29 | 42 | full_execution_summary_proxy_no_fills |
| S09 | retail_marketable_default | 573028 | 63 | -1.69625e+06 | -6439.6 | -1.69696e+06 | 62 | 63 | 63 | full_execution_summary_proxy_no_fills |
| S09 | stressed_retail | 567805 | 63 | -1.83695e+06 | -6472.91 | -1.83647e+06 | 63 | 63 | 63 | full_execution_summary_proxy_no_fills |
| S09 | zero_latency_spread_only_control | 590612 | 63 | -911328 | -6343.36 | -930397 | 51 | 53 | 63 | full_execution_summary_proxy_no_fills |

## Caveats

- Current features are 5-minute synthetic feature events, not true tick-level order events.
- Sampled trades carry a deterministic seed column assigned from the Phase 13 seed plan by quarter profile and scenario day; this is reporting lineage, not independent multi-seed acceptance evidence.
- Passive orders, partial fills, cancel/replace and order rejections are represented as requirements, not realistic queue simulation.
- Retail and stressed profiles apply the Zerodha equity-intraday NSE rupee order formula per simulated round trip using configured `order_notional_inr`, including brokerage cap, STT rounding, transaction charge, SEBI charge, stamp duty and GST.
- Representative rupee scenarios are retained for auditability; DP charges, broker contract-note rounding and actual broker fills remain outside this proxy.
- Full-run risk diagnostics cover all simulated marketable proxy trades, but they still use synthetic 5-minute feature events and not broker/exchange-confirmed fills.
- Spread crossing, fixed slippage and impact remain internal execution assumptions.
- Zero-latency/spread-only profile is a leakage/control profile, not a deployable model.

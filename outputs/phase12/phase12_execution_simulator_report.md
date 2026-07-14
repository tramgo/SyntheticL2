# Phase 12 Execution Simulator Report

Generated UTC: 2026-07-14T14:42:17.929454+00:00

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

## Full-Run Lifecycle / Fill-Adjusted Risk Proxy Summary

| strategy_id | execution_profile | fill_model | orders | mean_fill_ratio | filled_net_pnl_inr | risk_adjusted_net_pnl_inr | worst_daily_risk_adjusted_net_pnl_inr | tail_loss_1pct_filled_pnl_inr | max_intraday_drawdown_inr | max_abs_position_units | daily_halt_rows | risk_evidence_scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | retail_marketable_default | neutral_partial | 160471 | 0.723818 | 7.58e+07 | 7.58742e+07 | -75482.5 | -4825.39 | -181226 | 1245 | 1156 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S01 | retail_marketable_default | optimistic_marketable | 160471 | 0.991478 | 1.02923e+08 | 1.03082e+08 | -76395.4 | -6648.71 | -313393 | 1660 | 3554 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S01 | retail_marketable_default | pessimistic_partial | 160471 | 0.405851 | 4.34786e+07 | 4.34786e+07 | -10713.5 | -2740.89 | -34952.7 | 747 | 0 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S01 | stressed_retail | neutral_partial | 158070 | 0.726291 | -1.24716e+07 | 6.89391e+06 | -78550.3 | -4541.44 | -3.2853e+06 | 1183.5 | 71717 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S01 | stressed_retail | optimistic_marketable | 158070 | 0.992315 | -1.76045e+07 | 9.6519e+06 | -79882.1 | -6295.44 | -4.38353e+06 | 1578 | 79915 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S01 | stressed_retail | pessimistic_partial | 158070 | 0.409941 | -6.42734e+06 | 3.27099e+06 | -76825 | -2632.97 | -1.96787e+06 | 710.1 | 59325 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S01 | zero_latency_spread_only_control | neutral_partial | 166760 | 0.723504 | -9.39421e+07 | -4.78506e+06 | -79039.1 | -5749.41 | -5.51772e+06 | 1359.75 | 156066 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S01 | zero_latency_spread_only_control | optimistic_marketable | 166760 | 0.991168 | -1.30417e+08 | -4.82783e+06 | -79837.1 | -8147.21 | -7.35696e+06 | 1813 | 159044 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S01 | zero_latency_spread_only_control | pessimistic_partial | 166760 | 0.405841 | -5.08599e+07 | -4.74928e+06 | -78412.3 | -3173.59 | -3.31063e+06 | 815.85 | 144061 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S02 | retail_marketable_default | neutral_partial | 879151 | 0.719796 | -7.13472e+07 | -4.7811e+06 | -80098.8 | -4993.81 | -1.72374e+06 | 273.86 | 812367 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S02 | retail_marketable_default | optimistic_marketable | 879151 | 0.990631 | -9.92684e+07 | -4.7945e+06 | -81241 | -6902.46 | -2.39034e+06 | 389.19 | 830520 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S02 | retail_marketable_default | pessimistic_partial | 879151 | 0.397913 | -3.82282e+07 | -4.75055e+06 | -77166.6 | -2836.13 | -1.03086e+06 | 156.9 | 755561 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S02 | stressed_retail | neutral_partial | 870977 | 0.720118 | -8.95442e+07 | -4.76835e+06 | -77969.8 | -4899.92 | -2.24408e+06 | 302.05 | 825407 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S02 | stressed_retail | optimistic_marketable | 870977 | 0.990745 | -1.23921e+08 | -4.81302e+06 | -85647.8 | -6749.27 | -3.01849e+06 | 436.1 | 839258 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S02 | stressed_retail | pessimistic_partial | 870977 | 0.398432 | -4.87039e+07 | -4.75362e+06 | -76900.3 | -2778.54 | -1.3154e+06 | 146.85 | 784332 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S02 | zero_latency_spread_only_control | neutral_partial | 907352 | 0.718182 | -1.79699e+07 | -3.62574e+06 | -78924.9 | -4918.37 | -1.03619e+06 | 282.93 | 630123 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S02 | zero_latency_spread_only_control | optimistic_marketable | 907352 | 0.990104 | -2.64178e+07 | -3.71542e+06 | -78299.5 | -6844.94 | -1.68363e+06 | 393.92 | 701205 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S02 | zero_latency_spread_only_control | pessimistic_partial | 907352 | 0.395196 | -8.05356e+06 | -3.26889e+06 | -77537.7 | -2752.62 | -397466 | 151.5 | 412655 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S03 | retail_marketable_default | neutral_partial | 273427 | 0.697521 | 9.92587e+07 | 9.98526e+07 | -76891.3 | -5294.87 | -306632 | 2503.02 | 3597 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S03 | retail_marketable_default | optimistic_marketable | 273427 | 0.983358 | 1.3613e+08 | 1.37048e+08 | -77468.4 | -7735.3 | -408842 | 3530.68 | 4099 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S03 | retail_marketable_default | pessimistic_partial | 273427 | 0.360408 | 5.5424e+07 | 5.56549e+07 | -75974.9 | -3039.77 | -183979 | 1480.25 | 2347 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S03 | stressed_retail | neutral_partial | 270999 | 0.702749 | -1.32835e+07 | 1.62328e+07 | -77640.6 | -4386.59 | -4.50999e+06 | 2163.9 | 151888 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S03 | stressed_retail | optimistic_marketable | 270999 | 0.985112 | -2.0134e+07 | 2.04956e+07 | -77931.3 | -6159.56 | -6.0221e+06 | 3341.98 | 172197 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S03 | stressed_retail | pessimistic_partial | 270999 | 0.369092 | -5.32486e+06 | 8.64023e+06 | -76699 | -2573.81 | -2.69634e+06 | 1163.2 | 128446 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S03 | zero_latency_spread_only_control | neutral_partial | 283411 | 0.658219 | -1.20372e+08 | -3.03774e+06 | -80597.4 | -5927.15 | -1.54705e+07 | 2098.58 | 269394 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S03 | zero_latency_spread_only_control | optimistic_marketable | 283411 | 0.970941 | -1.82091e+08 | -2.93729e+06 | -82170 | -8987.97 | -2.58838e+07 | 3554.02 | 272891 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S03 | zero_latency_spread_only_control | pessimistic_partial | 283411 | 0.293194 | -4.8677e+07 | -3.1027e+06 | -77446.3 | -3032.82 | -5.85902e+06 | 961.95 | 254498 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S04 | retail_marketable_default | neutral_partial | 414066 | 0.695582 | -1.06416e+07 | 8.50435e+06 | -79434.8 | -6015.88 | -2.69945e+06 | 689.28 | 288080 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S04 | retail_marketable_default | optimistic_marketable | 414066 | 0.982899 | -1.60264e+07 | 1.20709e+07 | -79165 | -8582.59 | -3.97801e+06 | 957.22 | 294253 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S04 | retail_marketable_default | pessimistic_partial | 414066 | 0.356708 | -4.37185e+06 | 4.28234e+06 | -76850.9 | -3403.96 | -1.20492e+06 | 376.6 | 247158 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S04 | stressed_retail | neutral_partial | 410666 | 0.700966 | -3.93705e+07 | -3.04391e+06 | -78243.4 | -4620.53 | -2.44581e+06 | 715.59 | 373115 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S04 | stressed_retail | optimistic_marketable | 410666 | 0.9847 | -5.58729e+07 | -3.05418e+06 | -81715.4 | -6464.16 | -3.74179e+06 | 985.41 | 379984 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S04 | stressed_retail | pessimistic_partial | 410666 | 0.365665 | -1.99075e+07 | -2.80533e+06 | -77747.2 | -2710.51 | -1.36799e+06 | 396.15 | 339202 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S04 | zero_latency_spread_only_control | neutral_partial | 429202 | 0.657991 | -2.66678e+07 | -1.65314e+06 | -81069.7 | -5568.97 | -3.08659e+06 | 743.05 | 334442 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S04 | zero_latency_spread_only_control | optimistic_marketable | 429202 | 0.970886 | -3.82924e+07 | -2.55274e+06 | -79320.5 | -8316.9 | -4.28395e+06 | 1031.3 | 386418 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S04 | zero_latency_spread_only_control | pessimistic_partial | 429202 | 0.292763 | -1.30001e+07 | -1.75987e+06 | -77072.7 | -2912.95 | -1.66982e+06 | 402.75 | 225020 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S05 | retail_marketable_default | neutral_partial | 436284 | 0.706696 | -7.20038e+07 | -3.64077e+06 | -79392.5 | -5049.4 | -3.59026e+06 | 4692.99 | 392101 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S05 | retail_marketable_default | optimistic_marketable | 436284 | 0.987117 | -9.77493e+07 | -3.59799e+06 | -80296.3 | -6993.53 | -4.87604e+06 | 7061.01 | 399069 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S05 | retail_marketable_default | pessimistic_partial | 436284 | 0.373949 | -4.12313e+07 | -842109 | -77140.4 | -2909.79 | -5.01997e+06 | 2523.1 | 331160 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S05 | stressed_retail | neutral_partial | 432377 | 0.70804 | -4.75108e+07 | 6.70389e+06 | -78967.3 | -4939.91 | -7.25692e+06 | 4658.75 | 336851 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S05 | stressed_retail | optimistic_marketable | 432377 | 0.987562 | -6.43883e+07 | 7.87261e+06 | -81087.1 | -6771.86 | -8.47126e+06 | 6992.15 | 349978 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S05 | stressed_retail | pessimistic_partial | 432377 | 0.376195 | -2.73092e+07 | 4.44923e+06 | -76591.1 | -2819.79 | -5.63029e+06 | 2471.1 | 304069 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S05 | zero_latency_spread_only_control | neutral_partial | 449765 | 0.697598 | 3.61173e+07 | 3.62467e+07 | -77329.7 | -4503.37 | -686945 | 4629.96 | 74310 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S05 | zero_latency_spread_only_control | optimistic_marketable | 449765 | 0.984263 | 5.14003e+07 | 5.69152e+07 | -79601.2 | -6292.8 | -1.80153e+06 | 7243.04 | 109208 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S05 | zero_latency_spread_only_control | pessimistic_partial | 449765 | 0.358338 | 1.81235e+07 | 2.3641e+07 | -77283.5 | -2518.39 | -2.66366e+06 | 2387.55 | 70540 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S06 | retail_marketable_default | neutral_partial | 33129 | 0.699173 | -4.17325e+06 | -1.77059e+06 | -80907.8 | -5750.93 | -746366 | 123.52 | 11699 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S06 | retail_marketable_default | optimistic_marketable | 33129 | 0.984115 | -5.77481e+06 | -1.89126e+06 | -78857.5 | -8343.71 | -993178 | 181.73 | 15678 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S06 | retail_marketable_default | pessimistic_partial | 33129 | 0.362646 | -2.2742e+06 | -1.23862e+06 | -77763.8 | -3310.31 | -450316 | 65.1 | 5642 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S06 | stressed_retail | neutral_partial | 32935 | 0.700493 | -2.49929e+06 | -1.3544e+06 | -78420.8 | -4455.95 | -392303 | 135.26 | 8865 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S06 | stressed_retail | optimistic_marketable | 32935 | 0.984597 | -3.47846e+06 | -1.37032e+06 | -77352.6 | -6201.07 | -524808 | 190.09 | 13043 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S06 | stressed_retail | pessimistic_partial | 32935 | 0.36474 | -1.33848e+06 | -1.04428e+06 | -77116.2 | -2623.2 | -233442 | 70.4 | 3252 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S06 | zero_latency_spread_only_control | neutral_partial | 34373 | 0.664462 | 514737 | 910290 | -77236.6 | -5307.83 | -311477 | 141.26 | 5042 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S06 | zero_latency_spread_only_control | optimistic_marketable | 34373 | 0.973005 | 642134 | 1.42516e+06 | -78971.7 | -7979.75 | -435538 | 204.74 | 8892 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S06 | zero_latency_spread_only_control | pessimistic_partial | 34373 | 0.303644 | 367071 | 447312 | -75484 | -2857.14 | -178706 | 67.5 | 729 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S07 | retail_marketable_default | neutral_partial | 229792 | 0.703949 | -1.50621e+07 | 1.52098e+06 | -77210.4 | -4612.63 | -1.5057e+06 | 1103.32 | 150634 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S07 | retail_marketable_default | optimistic_marketable | 229792 | 0.986331 | -2.35232e+07 | 861283 | -81133.2 | -6635.99 | -1.85293e+06 | 1411.97 | 176734 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S07 | retail_marketable_default | pessimistic_partial | 229792 | 0.369045 | -5.18484e+06 | 3.97471e+06 | -76093 | -2554.49 | -1.14319e+06 | 772.05 | 104216 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S07 | stressed_retail | neutral_partial | 227842 | 0.706737 | -2.54463e+07 | 1.06424e+06 | -78344.1 | -4196.01 | -2.10703e+06 | 1097.27 | 157713 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S07 | stressed_retail | optimistic_marketable | 227842 | 0.987231 | -3.63066e+07 | -930626 | -82351.4 | -6015.48 | -2.68083e+06 | 1407.64 | 180715 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S07 | stressed_retail | pessimistic_partial | 227842 | 0.373765 | -1.26294e+07 | 1.69552e+06 | -76442.5 | -2377.58 | -1.43941e+06 | 767.4 | 122154 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S07 | zero_latency_spread_only_control | neutral_partial | 237064 | 0.704302 | -1.28829e+07 | 675357 | -77223 | -4211.18 | -2.06328e+06 | 1132.29 | 102612 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S07 | zero_latency_spread_only_control | optimistic_marketable | 237064 | 0.986478 | -1.99032e+07 | 149854 | -80560.2 | -6062.1 | -3.57474e+06 | 1456.18 | 132446 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S07 | zero_latency_spread_only_control | pessimistic_partial | 237064 | 0.36956 | -4.71203e+06 | 2.09954e+06 | -76218.2 | -2299.57 | -1.00695e+06 | 793.2 | 66500 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S08 | retail_marketable_default | neutral_partial | 431798 | 0.710411 | -3.18292e+07 | -4.66809e+06 | -79551.2 | -5001.98 | -1.1516e+06 | 1124.31 | 362548 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S08 | retail_marketable_default | optimistic_marketable | 431798 | 0.987713 | -4.51783e+07 | -4.7664e+06 | -78762.8 | -7023.86 | -1.82558e+06 | 1507.14 | 380664 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S08 | retail_marketable_default | pessimistic_partial | 431798 | 0.381744 | -1.60829e+07 | -3.90362e+06 | -76646.6 | -2874.24 | -592207 | 665.1 | 279729 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S08 | stressed_retail | neutral_partial | 426101 | 0.710354 | -4.05251e+07 | -4.76286e+06 | -80333.9 | -5034.21 | -1.65061e+06 | 1121.66 | 372114 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S08 | stressed_retail | optimistic_marketable | 426101 | 0.987695 | -5.6889e+07 | -4.79161e+06 | -79285.7 | -7049.97 | -2.28313e+06 | 1504.04 | 387868 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S08 | stressed_retail | pessimistic_partial | 426101 | 0.381648 | -2.11675e+07 | -4.46415e+06 | -77532.3 | -2897.66 | -1.04501e+06 | 663 | 302061 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S08 | zero_latency_spread_only_control | neutral_partial | 448403 | 0.710286 | -3.75204e+06 | 1.0069e+06 | -76593.6 | -4927.13 | -749048 | 1377.39 | 124685 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S08 | zero_latency_spread_only_control | optimistic_marketable | 448403 | 0.987672 | -6.26403e+06 | 1.10665e+06 | -82531.3 | -6901.78 | -1.00601e+06 | 1846.66 | 160494 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S08 | zero_latency_spread_only_control | pessimistic_partial | 448403 | 0.381535 | -860506 | 1.55953e+06 | -76245.2 | -2834.79 | -452705 | 814.5 | 83264 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S09 | retail_marketable_default | neutral_partial | 573028 | 0.718423 | -4.30213e+07 | -3.23484e+06 | -77714.7 | -4603.82 | -1.87188e+06 | 3912.04 | 494542 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S09 | retail_marketable_default | optimistic_marketable | 573028 | 0.990482 | -5.97117e+07 | -4.75154e+06 | -83919.3 | -6362.84 | -1.69267e+06 | 5121.76 | 529327 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S09 | retail_marketable_default | pessimistic_partial | 573028 | 0.394853 | -2.31987e+07 | 692267 | -78936.7 | -2628.72 | -2.53768e+06 | 2458.2 | 427634 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S09 | stressed_retail | neutral_partial | 567805 | 0.718412 | -5.21539e+07 | -4.74279e+06 | -77564.3 | -4630.99 | -1.85345e+06 | 3872.99 | 522825 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S09 | stressed_retail | optimistic_marketable | 567805 | 0.990475 | -7.22586e+07 | -4.7551e+06 | -81594.4 | -6388.19 | -1.83209e+06 | 5070.56 | 533108 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S09 | stressed_retail | pessimistic_partial | 567805 | 0.394841 | -2.82604e+07 | -99792.3 | -76793.5 | -2651.74 | -2.60249e+06 | 2433.75 | 449356 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S09 | zero_latency_spread_only_control | neutral_partial | 590612 | 0.718246 | -1.10372e+07 | 17123 | -76988.6 | -4520.35 | -2.02749e+06 | 4015.85 | 295508 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S09 | zero_latency_spread_only_control | optimistic_marketable | 590612 | 0.990421 | -1.57159e+07 | -1.73051e+06 | -87270.5 | -6266.76 | -1.29455e+06 | 5257.4 | 376490 | full_run_fill_adjusted_proxy_all_simulated_trades |
| S09 | zero_latency_spread_only_control | pessimistic_partial | 590612 | 0.394563 | -5.51977e+06 | 3.36944e+06 | -77126 | -2574.45 | -2.75754e+06 | 2523.75 | 190214 | full_run_fill_adjusted_proxy_all_simulated_trades |

## Full-Run Lifecycle Risk Breach Severity

| strategy_id | execution_profile | fill_model | breach_days | daily_loss_breach_days | position_limit_breach_days | drawdown_breach_days | daily_halt_days | risk_severity_score | risk_severity_band | risk_pass_candidate_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S03 | zero_latency_spread_only_control | optimistic_marketable | 45 | 45 | 22 | 44 | 45 | 2751.96 | high_proxy_breach_severity | False |
| S03 | zero_latency_spread_only_control | neutral_partial | 44 | 44 | 17 | 43 | 44 | 1679.02 | high_proxy_breach_severity | False |
| S05 | stressed_retail | optimistic_marketable | 63 | 55 | 63 | 63 | 55 | 1110.62 | high_proxy_breach_severity | False |
| S05 | stressed_retail | neutral_partial | 63 | 54 | 63 | 60 | 54 | 941.724 | high_proxy_breach_severity | False |
| S01 | zero_latency_spread_only_control | optimistic_marketable | 63 | 63 | 20 | 63 | 63 | 901.956 | high_proxy_breach_severity | False |
| S05 | retail_marketable_default | optimistic_marketable | 63 | 60 | 63 | 63 | 60 | 756.443 | high_proxy_breach_severity | False |
| S03 | stressed_retail | optimistic_marketable | 38 | 29 | 22 | 31 | 29 | 736.55 | high_proxy_breach_severity | False |
| S05 | stressed_retail | pessimistic_partial | 63 | 53 | 63 | 55 | 53 | 734.515 | high_proxy_breach_severity | False |
| S01 | zero_latency_spread_only_control | neutral_partial | 63 | 63 | 14 | 63 | 63 | 708.967 | high_proxy_breach_severity | False |
| S03 | zero_latency_spread_only_control | pessimistic_partial | 42 | 42 | 6 | 41 | 42 | 690.141 | high_proxy_breach_severity | False |
| S05 | retail_marketable_default | pessimistic_partial | 63 | 55 | 63 | 57 | 55 | 676.11 | high_proxy_breach_severity | False |
| S05 | retail_marketable_default | neutral_partial | 63 | 60 | 63 | 63 | 60 | 580.505 | high_proxy_breach_severity | False |
| S03 | stressed_retail | neutral_partial | 36 | 28 | 18 | 28 | 28 | 557.61 | high_proxy_breach_severity | False |
| S01 | stressed_retail | optimistic_marketable | 47 | 40 | 18 | 41 | 40 | 556.262 | high_proxy_breach_severity | False |
| S04 | zero_latency_spread_only_control | optimistic_marketable | 45 | 45 | 5 | 44 | 45 | 541.521 | high_proxy_breach_severity | False |
| S07 | zero_latency_spread_only_control | optimistic_marketable | 58 | 47 | 44 | 50 | 47 | 504.733 | high_proxy_breach_severity | False |
| S04 | retail_marketable_default | optimistic_marketable | 37 | 27 | 6 | 37 | 27 | 481.112 | high_proxy_breach_severity | False |
| S04 | stressed_retail | optimistic_marketable | 42 | 42 | 6 | 40 | 42 | 478.887 | high_proxy_breach_severity | False |
| S01 | zero_latency_spread_only_control | pessimistic_partial | 62 | 62 | 1 | 62 | 62 | 474.999 | high_proxy_breach_severity | False |
| S02 | stressed_retail | optimistic_marketable | 63 | 63 | 0 | 63 | 63 | 441.849 | high_proxy_breach_severity | False |
| S09 | zero_latency_spread_only_control | pessimistic_partial | 63 | 36 | 63 | 30 | 36 | 434.8 | high_proxy_breach_severity | False |
| S01 | stressed_retail | neutral_partial | 45 | 39 | 12 | 40 | 39 | 434.581 | high_proxy_breach_severity | False |
| S09 | stressed_retail | pessimistic_partial | 63 | 57 | 63 | 58 | 57 | 434.162 | high_proxy_breach_severity | False |
| S09 | retail_marketable_default | pessimistic_partial | 63 | 56 | 63 | 56 | 56 | 427.377 | high_proxy_breach_severity | False |
| S05 | zero_latency_spread_only_control | optimistic_marketable | 63 | 17 | 63 | 37 | 17 | 418.505 | high_proxy_breach_severity | False |
| S09 | stressed_retail | optimistic_marketable | 63 | 63 | 63 | 63 | 63 | 414.62 | high_proxy_breach_severity | False |
| S07 | stressed_retail | optimistic_marketable | 57 | 48 | 44 | 57 | 48 | 413.524 | high_proxy_breach_severity | False |
| S04 | zero_latency_spread_only_control | neutral_partial | 43 | 42 | 3 | 42 | 42 | 410.187 | high_proxy_breach_severity | False |
| S05 | zero_latency_spread_only_control | pessimistic_partial | 63 | 13 | 63 | 15 | 13 | 404.435 | high_proxy_breach_severity | False |
| S09 | zero_latency_spread_only_control | neutral_partial | 63 | 50 | 63 | 47 | 50 | 402.749 | high_proxy_breach_severity | False |
| S09 | retail_marketable_default | optimistic_marketable | 63 | 63 | 63 | 63 | 63 | 401.702 | high_proxy_breach_severity | False |
| S09 | retail_marketable_default | neutral_partial | 63 | 60 | 63 | 61 | 60 | 393.047 | high_proxy_breach_severity | False |
| S09 | stressed_retail | neutral_partial | 63 | 63 | 63 | 63 | 63 | 392.805 | high_proxy_breach_severity | False |
| S08 | stressed_retail | optimistic_marketable | 63 | 63 | 36 | 63 | 63 | 388.394 | high_proxy_breach_severity | False |
| S02 | retail_marketable_default | optimistic_marketable | 63 | 63 | 0 | 63 | 63 | 379.034 | high_proxy_breach_severity | False |
| S02 | stressed_retail | neutral_partial | 63 | 63 | 0 | 63 | 63 | 364.408 | high_proxy_breach_severity | False |
| S09 | zero_latency_spread_only_control | optimistic_marketable | 63 | 55 | 63 | 52 | 55 | 358.253 | high_proxy_breach_severity | False |
| S07 | stressed_retail | neutral_partial | 56 | 42 | 44 | 55 | 42 | 343.157 | high_proxy_breach_severity | False |
| S08 | retail_marketable_default | optimistic_marketable | 62 | 62 | 42 | 62 | 62 | 340.32 | high_proxy_breach_severity | False |
| S03 | stressed_retail | pessimistic_partial | 27 | 23 | 10 | 23 | 23 | 337.065 | high_proxy_breach_severity | False |

## Full-Run Lifecycle Risk Limit Sensitivity

| strategy_id | execution_profile | fill_model | risk_limit_profile | breach_days | daily_loss_breach_days | drawdown_breach_days | position_limit_breach_days | tail_trade_loss_breach | risk_limit_severity_score | risk_limit_status | risk_pass_candidate_under_limit_profile |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S03 | zero_latency_spread_only_control | optimistic_marketable | tight_capital_preservation | 46 | 46 | 45 | 31 | False | 8960 | high_proxy_breach_under_limit_profile | False |
| S03 | zero_latency_spread_only_control | optimistic_marketable | current_proxy_limits | 45 | 45 | 44 | 22 | False | 6645.49 | high_proxy_breach_under_limit_profile | False |
| S03 | zero_latency_spread_only_control | neutral_partial | tight_capital_preservation | 45 | 45 | 44 | 27 | False | 5370.01 | high_proxy_breach_under_limit_profile | False |
| S03 | zero_latency_spread_only_control | neutral_partial | current_proxy_limits | 44 | 44 | 43 | 17 | False | 3981.76 | high_proxy_breach_under_limit_profile | False |
| S05 | stressed_retail | optimistic_marketable | tight_capital_preservation | 63 | 56 | 63 | 63 | False | 3453.67 | high_proxy_breach_under_limit_profile | False |
| S03 | zero_latency_spread_only_control | optimistic_marketable | expanded_research_limits | 41 | 0 | 41 | 11 | False | 3329.89 | high_proxy_breach_under_limit_profile | False |
| S05 | stressed_retail | neutral_partial | tight_capital_preservation | 63 | 54 | 61 | 63 | False | 2861.16 | high_proxy_breach_under_limit_profile | False |
| S01 | zero_latency_spread_only_control | optimistic_marketable | tight_capital_preservation | 63 | 63 | 63 | 40 | False | 2667.28 | high_proxy_breach_under_limit_profile | False |
| S05 | stressed_retail | optimistic_marketable | current_proxy_limits | 63 | 55 | 63 | 63 | False | 2454.53 | high_proxy_breach_under_limit_profile | False |
| S03 | stressed_retail | optimistic_marketable | tight_capital_preservation | 42 | 31 | 33 | 29 | False | 2313.69 | high_proxy_breach_under_limit_profile | False |
| S05 | retail_marketable_default | optimistic_marketable | tight_capital_preservation | 63 | 60 | 63 | 63 | False | 2260.38 | high_proxy_breach_under_limit_profile | False |
| S05 | stressed_retail | pessimistic_partial | tight_capital_preservation | 63 | 53 | 58 | 63 | False | 2142.75 | high_proxy_breach_under_limit_profile | False |
| S03 | zero_latency_spread_only_control | pessimistic_partial | tight_capital_preservation | 44 | 44 | 42 | 15 | False | 2072.02 | high_proxy_breach_under_limit_profile | False |
| S05 | stressed_retail | neutral_partial | current_proxy_limits | 63 | 54 | 60 | 63 | False | 2056.9 | high_proxy_breach_under_limit_profile | False |
| S01 | zero_latency_spread_only_control | neutral_partial | tight_capital_preservation | 63 | 63 | 63 | 31 | False | 2017.54 | high_proxy_breach_under_limit_profile | False |
| S03 | zero_latency_spread_only_control | neutral_partial | expanded_research_limits | 40 | 0 | 39 | 7 | False | 1997.45 | high_proxy_breach_under_limit_profile | False |
| S01 | zero_latency_spread_only_control | optimistic_marketable | current_proxy_limits | 63 | 63 | 63 | 20 | False | 1968.37 | high_proxy_breach_under_limit_profile | False |
| S05 | retail_marketable_default | pessimistic_partial | tight_capital_preservation | 63 | 55 | 59 | 63 | False | 1943.74 | high_proxy_breach_under_limit_profile | False |
| S03 | stressed_retail | neutral_partial | tight_capital_preservation | 39 | 28 | 30 | 26 | False | 1710.26 | high_proxy_breach_under_limit_profile | False |
| S03 | stressed_retail | optimistic_marketable | current_proxy_limits | 38 | 29 | 31 | 22 | False | 1658.52 | high_proxy_breach_under_limit_profile | False |
| S01 | stressed_retail | optimistic_marketable | tight_capital_preservation | 56 | 40 | 43 | 37 | False | 1646.25 | high_proxy_breach_under_limit_profile | False |
| S05 | retail_marketable_default | neutral_partial | tight_capital_preservation | 63 | 60 | 63 | 63 | False | 1641.89 | high_proxy_breach_under_limit_profile | False |
| S05 | stressed_retail | pessimistic_partial | current_proxy_limits | 63 | 53 | 55 | 63 | False | 1561.95 | high_proxy_breach_under_limit_profile | False |
| S05 | retail_marketable_default | optimistic_marketable | current_proxy_limits | 63 | 60 | 63 | 63 | False | 1558.22 | high_proxy_breach_under_limit_profile | False |
| S04 | zero_latency_spread_only_control | optimistic_marketable | tight_capital_preservation | 46 | 45 | 46 | 17 | False | 1556.81 | high_proxy_breach_under_limit_profile | False |
| S03 | zero_latency_spread_only_control | pessimistic_partial | current_proxy_limits | 42 | 42 | 41 | 6 | False | 1529.05 | high_proxy_breach_under_limit_profile | False |
| S01 | zero_latency_spread_only_control | neutral_partial | current_proxy_limits | 63 | 63 | 63 | 14 | False | 1490.17 | high_proxy_breach_under_limit_profile | False |
| S04 | retail_marketable_default | optimistic_marketable | tight_capital_preservation | 40 | 27 | 38 | 20 | False | 1438.83 | high_proxy_breach_under_limit_profile | False |
| S05 | retail_marketable_default | pessimistic_partial | current_proxy_limits | 63 | 55 | 57 | 63 | False | 1411.63 | high_proxy_breach_under_limit_profile | False |
| S07 | zero_latency_spread_only_control | optimistic_marketable | tight_capital_preservation | 59 | 47 | 54 | 59 | False | 1378.36 | high_proxy_breach_under_limit_profile | False |
| S04 | stressed_retail | optimistic_marketable | tight_capital_preservation | 44 | 44 | 42 | 20 | False | 1370.29 | high_proxy_breach_under_limit_profile | False |
| S03 | zero_latency_spread_only_control | optimistic_marketable | stress_capacity_limits | 35 | 0 | 35 | 3 | False | 1335.95 | high_proxy_breach_under_limit_profile | False |
| S05 | stressed_retail | optimistic_marketable | expanded_research_limits | 63 | 0 | 59 | 63 | False | 1253.75 | high_proxy_breach_under_limit_profile | False |
| S05 | zero_latency_spread_only_control | optimistic_marketable | tight_capital_preservation | 63 | 18 | 41 | 63 | False | 1249.75 | high_proxy_breach_under_limit_profile | False |
| S01 | stressed_retail | neutral_partial | tight_capital_preservation | 52 | 39 | 40 | 30 | False | 1241.59 | high_proxy_breach_under_limit_profile | False |
| S01 | zero_latency_spread_only_control | pessimistic_partial | tight_capital_preservation | 63 | 63 | 62 | 15 | False | 1238.02 | high_proxy_breach_under_limit_profile | False |
| S03 | stressed_retail | neutral_partial | current_proxy_limits | 36 | 28 | 28 | 18 | False | 1229.93 | high_proxy_breach_under_limit_profile | False |
| S01 | stressed_retail | optimistic_marketable | current_proxy_limits | 47 | 40 | 41 | 18 | False | 1190.23 | high_proxy_breach_under_limit_profile | False |
| S09 | zero_latency_spread_only_control | pessimistic_partial | tight_capital_preservation | 63 | 41 | 37 | 63 | False | 1189.64 | high_proxy_breach_under_limit_profile | False |
| S05 | zero_latency_spread_only_control | pessimistic_partial | tight_capital_preservation | 63 | 14 | 22 | 63 | False | 1147.53 | high_proxy_breach_under_limit_profile | False |

## Full-Run Risk Acceptance Readiness Ledger

| risk_requirement | proxy_evidence_available | acceptance_requirement_met | rows |
| --- | --- | --- | --- |
| broker_exchange_fill_provenance | False | False | 11 |
| contract_note_and_cost_reconciliation | False | False | 11 |
| daily_equity_curve_and_halt_coverage | False | False | 2 |
| daily_equity_curve_and_halt_coverage | True | False | 9 |
| daily_loss_limit_validation | False | False | 2 |
| daily_loss_limit_validation | True | False | 9 |
| drawdown_breach_validation | False | False | 2 |
| drawdown_breach_validation | True | False | 9 |
| position_limit_validation | False | False | 2 |
| position_limit_validation | True | False | 9 |
| strategy_full_run_coverage | False | False | 2 |
| strategy_full_run_coverage | True | False | 9 |
| tail_loss_validation | False | False | 2 |
| tail_loss_validation | True | False | 9 |

| strategy_id | risk_requirement | observed_value | current_evidence_status | proxy_evidence_available | acceptance_requirement_met | blocking_gap |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | broker_exchange_fill_provenance | not available in current Phase 12 proxy | missing_broker_exchange_fill_provenance | False | False | The current run has no broker/exchange fill, rejection, queue or contract-note provenance. |
| S01 | contract_note_and_cost_reconciliation | Zerodha formula applied; contract-note reconciliation not available | proxy_formula_available_contract_note_missing | False | False | Zerodha rupee order formulas are applied, but broker contract notes and actual fills are missing. |
| S01 | daily_equity_curve_and_halt_coverage | 567 daily rows over up to 63 trade dates | proxy_daily_risk_state_available_not_acceptance | True | False | Daily risk state exists only as simulated proxy rows and has not been reconciled to actual order/fill state. |
| S01 | daily_loss_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_daily_loss_summary_available_not_acceptance | True | False | Daily-loss and halt checks are proxy diagnostics and do not prove deployable halt enforcement. |
| S01 | drawdown_breach_validation | 9 severity rows; high_severity_rows=6 | proxy_drawdown_breach_summary_available_not_acceptance | True | False | Drawdown summaries are proxy diagnostics and include high-severity rows; no broker/exchange-confirmed drawdown validation exists. |
| S01 | position_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_position_limit_summary_available_not_acceptance | True | False | Position exposure is inferred from proxy signal/fill rows and does not prove enforceable position-limit behavior. |
| S01 | strategy_full_run_coverage | 9 lifecycle rows; profiles=3; fill_models=3; support_level=runnable_proxy | proxy_full_run_available_not_acceptance | True | False | Current coverage is synthetic 5-minute marketable proxy evidence, not broker/exchange-confirmed acceptance evidence. |
| S01 | tail_loss_validation | 36 sensitivity rows; all_profile_pass_rows=4; high_limit_rows=26 | proxy_tail_loss_sensitivity_available_not_acceptance | True | False | Tail-loss sensitivity is proxy-only and does not prove acceptance-grade tail behavior under broker/exchange fills. |
| S02 | broker_exchange_fill_provenance | not available in current Phase 12 proxy | missing_broker_exchange_fill_provenance | False | False | The current run has no broker/exchange fill, rejection, queue or contract-note provenance. |
| S02 | contract_note_and_cost_reconciliation | Zerodha formula applied; contract-note reconciliation not available | proxy_formula_available_contract_note_missing | False | False | Zerodha rupee order formulas are applied, but broker contract notes and actual fills are missing. |
| S02 | daily_equity_curve_and_halt_coverage | 567 daily rows over up to 63 trade dates | proxy_daily_risk_state_available_not_acceptance | True | False | Daily risk state exists only as simulated proxy rows and has not been reconciled to actual order/fill state. |
| S02 | daily_loss_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_daily_loss_summary_available_not_acceptance | True | False | Daily-loss and halt checks are proxy diagnostics and do not prove deployable halt enforcement. |
| S02 | drawdown_breach_validation | 9 severity rows; high_severity_rows=9 | proxy_drawdown_breach_summary_available_not_acceptance | True | False | Drawdown summaries are proxy diagnostics and include high-severity rows; no broker/exchange-confirmed drawdown validation exists. |
| S02 | position_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_position_limit_summary_available_not_acceptance | True | False | Position exposure is inferred from proxy signal/fill rows and does not prove enforceable position-limit behavior. |
| S02 | strategy_full_run_coverage | 9 lifecycle rows; profiles=3; fill_models=3; support_level=runnable_proxy | proxy_full_run_available_not_acceptance | True | False | Current coverage is synthetic 5-minute marketable proxy evidence, not broker/exchange-confirmed acceptance evidence. |
| S02 | tail_loss_validation | 36 sensitivity rows; all_profile_pass_rows=1; high_limit_rows=32 | proxy_tail_loss_sensitivity_available_not_acceptance | True | False | Tail-loss sensitivity is proxy-only and does not prove acceptance-grade tail behavior under broker/exchange fills. |
| S03 | broker_exchange_fill_provenance | not available in current Phase 12 proxy | missing_broker_exchange_fill_provenance | False | False | The current run has no broker/exchange fill, rejection, queue or contract-note provenance. |
| S03 | contract_note_and_cost_reconciliation | Zerodha formula applied; contract-note reconciliation not available | proxy_formula_available_contract_note_missing | False | False | Zerodha rupee order formulas are applied, but broker contract notes and actual fills are missing. |
| S03 | daily_equity_curve_and_halt_coverage | 540 daily rows over up to 60 trade dates | proxy_daily_risk_state_available_not_acceptance | True | False | Daily risk state exists only as simulated proxy rows and has not been reconciled to actual order/fill state. |
| S03 | daily_loss_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_daily_loss_summary_available_not_acceptance | True | False | Daily-loss and halt checks are proxy diagnostics and do not prove deployable halt enforcement. |
| S03 | drawdown_breach_validation | 9 severity rows; high_severity_rows=7 | proxy_drawdown_breach_summary_available_not_acceptance | True | False | Drawdown summaries are proxy diagnostics and include high-severity rows; no broker/exchange-confirmed drawdown validation exists. |
| S03 | position_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_position_limit_summary_available_not_acceptance | True | False | Position exposure is inferred from proxy signal/fill rows and does not prove enforceable position-limit behavior. |
| S03 | strategy_full_run_coverage | 9 lifecycle rows; profiles=3; fill_models=3; support_level=partial_missing_required_features | proxy_full_run_available_not_acceptance | True | False | Current coverage is synthetic 5-minute marketable proxy evidence, not broker/exchange-confirmed acceptance evidence. |
| S03 | tail_loss_validation | 36 sensitivity rows; all_profile_pass_rows=1; high_limit_rows=30 | proxy_tail_loss_sensitivity_available_not_acceptance | True | False | Tail-loss sensitivity is proxy-only and does not prove acceptance-grade tail behavior under broker/exchange fills. |
| S04 | broker_exchange_fill_provenance | not available in current Phase 12 proxy | missing_broker_exchange_fill_provenance | False | False | The current run has no broker/exchange fill, rejection, queue or contract-note provenance. |
| S04 | contract_note_and_cost_reconciliation | Zerodha formula applied; contract-note reconciliation not available | proxy_formula_available_contract_note_missing | False | False | Zerodha rupee order formulas are applied, but broker contract notes and actual fills are missing. |
| S04 | daily_equity_curve_and_halt_coverage | 540 daily rows over up to 60 trade dates | proxy_daily_risk_state_available_not_acceptance | True | False | Daily risk state exists only as simulated proxy rows and has not been reconciled to actual order/fill state. |
| S04 | daily_loss_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_daily_loss_summary_available_not_acceptance | True | False | Daily-loss and halt checks are proxy diagnostics and do not prove deployable halt enforcement. |
| S04 | drawdown_breach_validation | 9 severity rows; high_severity_rows=9 | proxy_drawdown_breach_summary_available_not_acceptance | True | False | Drawdown summaries are proxy diagnostics and include high-severity rows; no broker/exchange-confirmed drawdown validation exists. |
| S04 | position_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_position_limit_summary_available_not_acceptance | True | False | Position exposure is inferred from proxy signal/fill rows and does not prove enforceable position-limit behavior. |
| S04 | strategy_full_run_coverage | 9 lifecycle rows; profiles=3; fill_models=3; support_level=partial_missing_required_features | proxy_full_run_available_not_acceptance | True | False | Current coverage is synthetic 5-minute marketable proxy evidence, not broker/exchange-confirmed acceptance evidence. |
| S04 | tail_loss_validation | 36 sensitivity rows; all_profile_pass_rows=0; high_limit_rows=33 | proxy_tail_loss_sensitivity_available_not_acceptance | True | False | Tail-loss sensitivity is proxy-only and does not prove acceptance-grade tail behavior under broker/exchange fills. |
| S05 | broker_exchange_fill_provenance | not available in current Phase 12 proxy | missing_broker_exchange_fill_provenance | False | False | The current run has no broker/exchange fill, rejection, queue or contract-note provenance. |
| S05 | contract_note_and_cost_reconciliation | Zerodha formula applied; contract-note reconciliation not available | proxy_formula_available_contract_note_missing | False | False | Zerodha rupee order formulas are applied, but broker contract notes and actual fills are missing. |
| S05 | daily_equity_curve_and_halt_coverage | 567 daily rows over up to 63 trade dates | proxy_daily_risk_state_available_not_acceptance | True | False | Daily risk state exists only as simulated proxy rows and has not been reconciled to actual order/fill state. |
| S05 | daily_loss_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_daily_loss_summary_available_not_acceptance | True | False | Daily-loss and halt checks are proxy diagnostics and do not prove deployable halt enforcement. |
| S05 | drawdown_breach_validation | 9 severity rows; high_severity_rows=9 | proxy_drawdown_breach_summary_available_not_acceptance | True | False | Drawdown summaries are proxy diagnostics and include high-severity rows; no broker/exchange-confirmed drawdown validation exists. |
| S05 | position_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_position_limit_summary_available_not_acceptance | True | False | Position exposure is inferred from proxy signal/fill rows and does not prove enforceable position-limit behavior. |
| S05 | strategy_full_run_coverage | 9 lifecycle rows; profiles=3; fill_models=3; support_level=runnable_proxy | proxy_full_run_available_not_acceptance | True | False | Current coverage is synthetic 5-minute marketable proxy evidence, not broker/exchange-confirmed acceptance evidence. |
| S05 | tail_loss_validation | 36 sensitivity rows; all_profile_pass_rows=0; high_limit_rows=36 | proxy_tail_loss_sensitivity_available_not_acceptance | True | False | Tail-loss sensitivity is proxy-only and does not prove acceptance-grade tail behavior under broker/exchange fills. |
| S06 | broker_exchange_fill_provenance | not available in current Phase 12 proxy | missing_broker_exchange_fill_provenance | False | False | The current run has no broker/exchange fill, rejection, queue or contract-note provenance. |
| S06 | contract_note_and_cost_reconciliation | Zerodha formula applied; contract-note reconciliation not available | proxy_formula_available_contract_note_missing | False | False | Zerodha rupee order formulas are applied, but broker contract notes and actual fills are missing. |
| S06 | daily_equity_curve_and_halt_coverage | 486 daily rows over up to 54 trade dates | proxy_daily_risk_state_available_not_acceptance | True | False | Daily risk state exists only as simulated proxy rows and has not been reconciled to actual order/fill state. |
| S06 | daily_loss_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_daily_loss_summary_available_not_acceptance | True | False | Daily-loss and halt checks are proxy diagnostics and do not prove deployable halt enforcement. |
| S06 | drawdown_breach_validation | 9 severity rows; high_severity_rows=2 | proxy_drawdown_breach_summary_available_not_acceptance | True | False | Drawdown summaries are proxy diagnostics and include high-severity rows; no broker/exchange-confirmed drawdown validation exists. |
| S06 | position_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_position_limit_summary_available_not_acceptance | True | False | Position exposure is inferred from proxy signal/fill rows and does not prove enforceable position-limit behavior. |
| S06 | strategy_full_run_coverage | 9 lifecycle rows; profiles=3; fill_models=3; support_level=partial_missing_required_features | proxy_full_run_available_not_acceptance | True | False | Current coverage is synthetic 5-minute marketable proxy evidence, not broker/exchange-confirmed acceptance evidence. |
| S06 | tail_loss_validation | 36 sensitivity rows; all_profile_pass_rows=7; high_limit_rows=14 | proxy_tail_loss_sensitivity_available_not_acceptance | True | False | Tail-loss sensitivity is proxy-only and does not prove acceptance-grade tail behavior under broker/exchange fills. |
| S07 | broker_exchange_fill_provenance | not available in current Phase 12 proxy | missing_broker_exchange_fill_provenance | False | False | The current run has no broker/exchange fill, rejection, queue or contract-note provenance. |
| S07 | contract_note_and_cost_reconciliation | Zerodha formula applied; contract-note reconciliation not available | proxy_formula_available_contract_note_missing | False | False | Zerodha rupee order formulas are applied, but broker contract notes and actual fills are missing. |
| S07 | daily_equity_curve_and_halt_coverage | 531 daily rows over up to 59 trade dates | proxy_daily_risk_state_available_not_acceptance | True | False | Daily risk state exists only as simulated proxy rows and has not been reconciled to actual order/fill state. |
| S07 | daily_loss_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_daily_loss_summary_available_not_acceptance | True | False | Daily-loss and halt checks are proxy diagnostics and do not prove deployable halt enforcement. |
| S07 | drawdown_breach_validation | 9 severity rows; high_severity_rows=9 | proxy_drawdown_breach_summary_available_not_acceptance | True | False | Drawdown summaries are proxy diagnostics and include high-severity rows; no broker/exchange-confirmed drawdown validation exists. |
| S07 | position_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_position_limit_summary_available_not_acceptance | True | False | Position exposure is inferred from proxy signal/fill rows and does not prove enforceable position-limit behavior. |
| S07 | strategy_full_run_coverage | 9 lifecycle rows; profiles=3; fill_models=3; support_level=runnable_proxy | proxy_full_run_available_not_acceptance | True | False | Current coverage is synthetic 5-minute marketable proxy evidence, not broker/exchange-confirmed acceptance evidence. |
| S07 | tail_loss_validation | 36 sensitivity rows; all_profile_pass_rows=0; high_limit_rows=32 | proxy_tail_loss_sensitivity_available_not_acceptance | True | False | Tail-loss sensitivity is proxy-only and does not prove acceptance-grade tail behavior under broker/exchange fills. |
| S08 | broker_exchange_fill_provenance | not available in current Phase 12 proxy | missing_broker_exchange_fill_provenance | False | False | The current run has no broker/exchange fill, rejection, queue or contract-note provenance. |
| S08 | contract_note_and_cost_reconciliation | Zerodha formula applied; contract-note reconciliation not available | proxy_formula_available_contract_note_missing | False | False | Zerodha rupee order formulas are applied, but broker contract notes and actual fills are missing. |
| S08 | daily_equity_curve_and_halt_coverage | 567 daily rows over up to 63 trade dates | proxy_daily_risk_state_available_not_acceptance | True | False | Daily risk state exists only as simulated proxy rows and has not been reconciled to actual order/fill state. |
| S08 | daily_loss_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_daily_loss_summary_available_not_acceptance | True | False | Daily-loss and halt checks are proxy diagnostics and do not prove deployable halt enforcement. |
| S08 | drawdown_breach_validation | 9 severity rows; high_severity_rows=8 | proxy_drawdown_breach_summary_available_not_acceptance | True | False | Drawdown summaries are proxy diagnostics and include high-severity rows; no broker/exchange-confirmed drawdown validation exists. |
| S08 | position_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_position_limit_summary_available_not_acceptance | True | False | Position exposure is inferred from proxy signal/fill rows and does not prove enforceable position-limit behavior. |
| S08 | strategy_full_run_coverage | 9 lifecycle rows; profiles=3; fill_models=3; support_level=partial_missing_required_features | proxy_full_run_available_not_acceptance | True | False | Current coverage is synthetic 5-minute marketable proxy evidence, not broker/exchange-confirmed acceptance evidence. |
| S08 | tail_loss_validation | 36 sensitivity rows; all_profile_pass_rows=1; high_limit_rows=28 | proxy_tail_loss_sensitivity_available_not_acceptance | True | False | Tail-loss sensitivity is proxy-only and does not prove acceptance-grade tail behavior under broker/exchange fills. |
| S09 | broker_exchange_fill_provenance | not available in current Phase 12 proxy | missing_broker_exchange_fill_provenance | False | False | The current run has no broker/exchange fill, rejection, queue or contract-note provenance. |
| S09 | contract_note_and_cost_reconciliation | Zerodha formula applied; contract-note reconciliation not available | proxy_formula_available_contract_note_missing | False | False | Zerodha rupee order formulas are applied, but broker contract notes and actual fills are missing. |
| S09 | daily_equity_curve_and_halt_coverage | 567 daily rows over up to 63 trade dates | proxy_daily_risk_state_available_not_acceptance | True | False | Daily risk state exists only as simulated proxy rows and has not been reconciled to actual order/fill state. |
| S09 | daily_loss_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_daily_loss_summary_available_not_acceptance | True | False | Daily-loss and halt checks are proxy diagnostics and do not prove deployable halt enforcement. |
| S09 | drawdown_breach_validation | 9 severity rows; high_severity_rows=9 | proxy_drawdown_breach_summary_available_not_acceptance | True | False | Drawdown summaries are proxy diagnostics and include high-severity rows; no broker/exchange-confirmed drawdown validation exists. |
| S09 | position_limit_validation | 9 severity rows; current_limit_pass_rows=0 | proxy_position_limit_summary_available_not_acceptance | True | False | Position exposure is inferred from proxy signal/fill rows and does not prove enforceable position-limit behavior. |
| S09 | strategy_full_run_coverage | 9 lifecycle rows; profiles=3; fill_models=3; support_level=runnable_proxy | proxy_full_run_available_not_acceptance | True | False | Current coverage is synthetic 5-minute marketable proxy evidence, not broker/exchange-confirmed acceptance evidence. |
| S09 | tail_loss_validation | 36 sensitivity rows; all_profile_pass_rows=0; high_limit_rows=36 | proxy_tail_loss_sensitivity_available_not_acceptance | True | False | Tail-loss sensitivity is proxy-only and does not prove acceptance-grade tail behavior under broker/exchange fills. |
| S10 | broker_exchange_fill_provenance | not available in current Phase 12 proxy | missing_broker_exchange_fill_provenance | False | False | The current run has no broker/exchange fill, rejection, queue or contract-note provenance. |
| S10 | contract_note_and_cost_reconciliation | Zerodha formula applied; contract-note reconciliation not available | proxy_formula_available_contract_note_missing | False | False | Zerodha rupee order formulas are applied, but broker contract notes and actual fills are missing. |
| S10 | daily_equity_curve_and_halt_coverage | 0 daily rows over up to 0 trade dates | missing_daily_risk_state | False | False | Daily risk state exists only as simulated proxy rows and has not been reconciled to actual order/fill state. |
| S10 | daily_loss_limit_validation | 0 severity rows; current_limit_pass_rows=0 | missing_daily_loss_summary | False | False | Daily-loss and halt checks are proxy diagnostics and do not prove deployable halt enforcement. |
| S10 | drawdown_breach_validation | 0 severity rows; high_severity_rows=0 | missing_drawdown_summary | False | False | Drawdown summaries are proxy diagnostics and include high-severity rows; no broker/exchange-confirmed drawdown validation exists. |
| S10 | position_limit_validation | 0 severity rows; current_limit_pass_rows=0 | missing_position_limit_summary | False | False | Position exposure is inferred from proxy signal/fill rows and does not prove enforceable position-limit behavior. |
| S10 | strategy_full_run_coverage | 0 lifecycle rows; profiles=0; fill_models=0; support_level=not_supported_by_current_product | missing_current_proxy_run | False | False | Current coverage is synthetic 5-minute marketable proxy evidence, not broker/exchange-confirmed acceptance evidence. |
| S10 | tail_loss_validation | 0 sensitivity rows; all_profile_pass_rows=0; high_limit_rows=0 | missing_tail_loss_sensitivity | False | False | Tail-loss sensitivity is proxy-only and does not prove acceptance-grade tail behavior under broker/exchange fills. |

## Caveats

- Current features are 5-minute synthetic feature events, not true tick-level order events.
- Sampled trades carry a deterministic seed column assigned from the Phase 13 seed plan by quarter profile and scenario day; this is reporting lineage, not independent multi-seed acceptance evidence.
- Passive orders, partial fills, cancel/replace and order rejections are represented as requirements, not realistic queue simulation.
- Retail and stressed profiles apply the Zerodha equity-intraday NSE rupee order formula per simulated round trip using configured `order_notional_inr`, including brokerage cap, STT rounding, transaction charge, SEBI charge, stamp duty and GST.
- Representative rupee scenarios are retained for auditability; DP charges, broker contract-note rounding and actual broker fills remain outside this proxy.
- Full-run risk diagnostics now include no-fill, fill-adjusted lifecycle, breach-severity, risk-limit sensitivity and risk acceptance-readiness summaries over all simulated marketable proxy trades, but they still use synthetic 5-minute feature events and not broker/exchange-confirmed fills.
- Spread crossing, fixed slippage and impact remain internal execution assumptions.
- Zero-latency/spread-only profile is a leakage/control profile, not a deployable model.

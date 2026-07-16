# Phase 43 Native Full-Year Cost-Aware Salvage Scan

Generated UTC: 2026-07-16T14:21:11.672332+00:00

This phase scans sparse, high-confidence strategy variants over the native 252-day synthetic L2 event stream.
It tests whether threshold, spread and liquidity filters can rescue full-year economics under Zerodha-style costs. It is not acceptance evidence.

## Summary

| metric | value | description |
| --- | --- | --- |
| phase43_input_event_rows | 3.01229e+06 | Native full-year L2 event rows scanned |
| phase43_variants_registered | 60 | Cost-aware strategy variants registered |
| phase43_variant_profile_rows | 180 | Variant/profile rows evaluated |
| phase43_total_variant_trades | 5.02757e+06 | Total simulated trades across variant/profile rows |
| phase43_positive_variant_profile_rows | 4 | Annual positive P&L variant/profile rows |
| phase43_positive_realistic_variant_profile_rows | 0 | Annual positive P&L retail/stressed rows |
| phase43_deeper_synthetic_candidate_rows | 0 | Realistic positive rows with enough trades |
| phase43_best_annual_net_pnl_inr | 85087.1 | Best annual net P&L across all variant profiles |
| phase43_best_realistic_annual_net_pnl_inr | -184924 | Best annual net P&L across retail/stressed variant profiles |
| phase43_synthetic_full_year_acceptance_ready | 0 | Cost-aware salvage scan is experiment evidence, not acceptance |

## Top Variant Results

| variant_id | strategy_id | execution_profile | threshold_quantile | spread_quantile | liquidity_quantile | trades | annual_net_pnl_inr | mean_gross_return | mean_cost_return | mean_zerodha_charge_return | mean_net_return | worst_daily_net_pnl_inr | max_drawdown_inr | positive_day_fraction | annualized_sharpe_proxy | realistic_profile | positive_after_costs | enough_trades | candidate_for_deeper_synthetic_replay |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S07_q98_sp25_liq75 | S07 | zero_latency_spread_only_control | 0.98 | 0.25 | 0.75 | 8624 | 85087.1 | 0.000329752 | 0.000231089 | 0 | 9.86631e-05 | -20510.4 | -61080.3 | 0.506329 | 1.54424 | False | True | True | False |
| S07_q98_sp50_liq75 | S07 | zero_latency_spread_only_control | 0.98 | 0.5 | 0.75 | 8624 | 85087.1 | 0.000329752 | 0.000231089 | 0 | 9.86631e-05 | -20510.4 | -61080.3 | 0.506329 | 1.54424 | False | True | True | False |
| S05_q98_sp25_liq75 | S05 | zero_latency_spread_only_control | 0.98 | 0.25 | 0.75 | 8285 | 3917.99 | 0.000162245 | 0.000157516 | 0 | 4.72902e-06 | -22170.4 | -71550.4 | 0.511628 | 0.112665 | False | True | True | False |
| S05_q98_sp50_liq75 | S05 | zero_latency_spread_only_control | 0.98 | 0.5 | 0.75 | 8285 | 3917.99 | 0.000162245 | 0.000157516 | 0 | 4.72902e-06 | -22170.4 | -71550.4 | 0.511628 | 0.112665 | False | True | True | False |
| S07_q90_sp50_liq75 | S07 | zero_latency_spread_only_control | 0.9 | 0.5 | 0.75 | 21087 | -30477 | 0.000185643 | 0.000200096 | 0 | -1.4453e-05 | -28679.5 | -121816 | 0.47619 | -0.389085 | False | False | True | False |
| S07_q90_sp25_liq75 | S07 | zero_latency_spread_only_control | 0.9 | 0.25 | 0.75 | 18329 | -33046.8 | 0.000198209 | 0.000216238 | 0 | -1.80298e-05 | -28679.5 | -128026 | 0.428571 | -0.432519 | False | False | True | False |
| S07_q98_sp25_liq50 | S07 | zero_latency_spread_only_control | 0.98 | 0.25 | 0.5 | 18045 | -34200.8 | 0.000177786 | 0.000196739 | 0 | -1.89531e-05 | -20971 | -138353 | 0.471154 | -0.480902 | False | False | True | False |
| S07_q98_sp50_liq50 | S07 | zero_latency_spread_only_control | 0.98 | 0.5 | 0.5 | 18045 | -34200.8 | 0.000177786 | 0.000196739 | 0 | -1.89531e-05 | -20971 | -138353 | 0.471154 | -0.480902 | False | False | True | False |
| S07_q95_sp25_liq75 | S07 | zero_latency_spread_only_control | 0.95 | 0.25 | 0.75 | 16694 | -79838.8 | 0.00018292 | 0.000230745 | 0 | -4.78248e-05 | -28679.5 | -159065 | 0.297619 | -1.01195 | False | False | True | False |
| S07_q95_sp50_liq75 | S07 | zero_latency_spread_only_control | 0.95 | 0.5 | 0.75 | 16694 | -79838.8 | 0.00018292 | 0.000230745 | 0 | -4.78248e-05 | -28679.5 | -159065 | 0.297619 | -1.01195 | False | False | True | False |
| S01_q98_sp25_liq75 | S01 | retail_marketable_default | 0.98 | 0.25 | 0.75 | 1726 | -184924 | 0.000119851 | 0.00119126 | 0.000826856 | -0.0010714 | -16305.6 | -185057 | 0.267241 | -6.02875 | True | False | True | False |
| S05_q98_sp25_liq50 | S05 | zero_latency_spread_only_control | 0.98 | 0.25 | 0.5 | 22812 | -192353 | 7.26261e-05 | 0.000156947 | 0 | -8.4321e-05 | -24852.7 | -210070 | 0.38961 | -3.38436 | False | False | True | False |
| S05_q98_sp50_liq50 | S05 | zero_latency_spread_only_control | 0.98 | 0.5 | 0.5 | 22812 | -192353 | 7.26261e-05 | 0.000156947 | 0 | -8.4321e-05 | -24852.7 | -210070 | 0.38961 | -3.38436 | False | False | True | False |
| S01_q98_sp25_liq50 | S01 | retail_marketable_default | 0.98 | 0.25 | 0.5 | 2193 | -250930 | 2.50424e-05 | 0.00116928 | 0.000826845 | -0.00114423 | -16683 | -251568 | 0.276316 | -6.74007 | True | False | True | False |
| S07_q90_sp25_liq50 | S07 | zero_latency_spread_only_control | 0.9 | 0.25 | 0.5 | 33275 | -252619 | 0.000114122 | 0.00019004 | 0 | -7.59184e-05 | -28679.5 | -320964 | 0.396552 | -2.6621 | False | False | True | False |
| S01_q98_sp25_liq75 | S01 | stressed_retail | 0.98 | 0.25 | 0.75 | 1622 | -261010 | -9.62827e-05 | 0.0015129 | 0.000826856 | -0.00160918 | -21236.1 | -261248 | 0.25 | -8.40506 | True | False | True | False |
| S02_q98_sp25_liq75 | S02 | retail_marketable_default | 0.98 | 0.25 | 0.75 | 2858 | -275071 | 0.000148444 | 0.0011109 | 0.000826815 | -0.000962458 | -37706.3 | -283503 | 0.280899 | -6.64251 | True | False | True | False |
| S02_q98_sp25_liq50 | S02 | retail_marketable_default | 0.98 | 0.25 | 0.5 | 2894 | -276977 | 0.000153384 | 0.00111046 | 0.000826815 | -0.000957073 | -37706.3 | -285409 | 0.280899 | -6.6972 | True | False | True | False |
| S02_q98_sp25_liq50 | S02 | zero_latency_spread_only_control | 0.98 | 0.25 | 0.5 | 3130 | -285593 | -0.000805928 | 0.000106511 | 0 | -0.000912439 | -44153.8 | -274542 | 0.247191 | -6.59231 | False | False | True | False |
| S02_q98_sp25_liq75 | S02 | zero_latency_spread_only_control | 0.98 | 0.25 | 0.75 | 3091 | -287599 | -0.000823736 | 0.000106705 | 0 | -0.00093044 | -44153.8 | -276547 | 0.247191 | -6.63873 | False | False | True | False |
| S01_q98_sp25_liq50 | S01 | stressed_retail | 0.98 | 0.25 | 0.5 | 2055 | -318498 | -7.09963e-05 | 0.00147887 | 0.000826849 | -0.00154987 | -21442.6 | -318590 | 0.213793 | -8.84906 | True | False | True | False |
| S07_q95_sp25_liq50 | S07 | zero_latency_spread_only_control | 0.95 | 0.25 | 0.5 | 30687 | -326669 | 9.41012e-05 | 0.000200553 | 0 | -0.000106452 | -28679.5 | -393016 | 0.327103 | -3.36205 | False | False | True | False |
| S07_q95_sp50_liq50 | S07 | zero_latency_spread_only_control | 0.95 | 0.5 | 0.5 | 30687 | -326669 | 9.41012e-05 | 0.000200553 | 0 | -0.000106452 | -28679.5 | -393016 | 0.327103 | -3.36205 | False | False | True | False |
| S07_q90_sp50_liq50 | S07 | zero_latency_spread_only_control | 0.9 | 0.5 | 0.5 | 38957 | -351280 | 8.41203e-05 | 0.000174292 | 0 | -9.01713e-05 | -44601 | -415252 | 0.358333 | -3.23122 | False | False | True | False |
| S02_q98_sp25_liq75 | S02 | stressed_retail | 0.98 | 0.25 | 0.75 | 2709 | -433843 | -0.000211605 | 0.00138988 | 0.000826815 | -0.00160149 | -52529.1 | -430521 | 0.137931 | -7.97463 | True | False | True | False |
| S02_q98_sp25_liq50 | S02 | stressed_retail | 0.98 | 0.25 | 0.5 | 2746 | -434183 | -0.000192072 | 0.00138908 | 0.000826814 | -0.00158115 | -52529.1 | -430861 | 0.137931 | -7.98074 | True | False | True | False |
| S09_q98_sp25_liq75 | S09 | zero_latency_spread_only_control | 0.98 | 0.25 | 0.75 | 11109 | -544256 | -0.000267914 | 0.00022201 | 0 | -0.000489923 | -57053.8 | -533421 | 0.276786 | -6.68088 | False | False | True | False |
| S09_q98_sp50_liq75 | S09 | zero_latency_spread_only_control | 0.98 | 0.5 | 0.75 | 11109 | -544256 | -0.000267914 | 0.00022201 | 0 | -0.000489923 | -57053.8 | -533421 | 0.276786 | -6.68088 | False | False | True | False |
| S01_q98_sp50_liq75 | S01 | retail_marketable_default | 0.98 | 0.5 | 0.75 | 7022 | -603224 | 0.000307447 | 0.0011665 | 0.000826832 | -0.000859049 | -36146.1 | -605812 | 0.272 | -7.05164 | True | False | True | False |
| S05_q95_sp25_liq75 | S05 | zero_latency_spread_only_control | 0.95 | 0.25 | 0.75 | 21039 | -693172 | -0.000106948 | 0.000222522 | 0 | -0.00032947 | -84147.6 | -679746 | 0.368 | -5.70583 | False | False | True | False |
| S01_q98_sp50_liq50 | S01 | retail_marketable_default | 0.98 | 0.5 | 0.5 | 7914 | -711974 | 0.000256882 | 0.00115652 | 0.000826829 | -0.000899639 | -36146.1 | -711932 | 0.22619 | -6.98834 | True | False | True | False |
| S09_q95_sp25_liq75 | S09 | zero_latency_spread_only_control | 0.95 | 0.25 | 0.75 | 20995 | -715115 | -0.000118307 | 0.000222305 | 0 | -0.000340612 | -85803.8 | -701688 | 0.368 | -5.6733 | False | False | True | False |
| S09_q95_sp50_liq75 | S09 | zero_latency_spread_only_control | 0.95 | 0.5 | 0.75 | 20995 | -715115 | -0.000118307 | 0.000222305 | 0 | -0.000340612 | -85803.8 | -701688 | 0.368 | -5.6733 | False | False | True | False |
| S05_q90_sp25_liq75 | S05 | zero_latency_spread_only_control | 0.9 | 0.25 | 0.75 | 33367 | -737423 | -4.76635e-05 | 0.00017334 | 0 | -0.000221004 | -84147.6 | -723996 | 0.380952 | -5.45169 | False | False | True | False |
| S01_q95_sp25_liq75 | S01 | retail_marketable_default | 0.95 | 0.25 | 0.75 | 6887 | -759609 | 3.45746e-05 | 0.00113754 | 0.000826822 | -0.00110296 | -38061.7 | -759352 | 0.223776 | -9.64406 | True | False | True | False |
| S09_q98_sp25_liq50 | S09 | zero_latency_spread_only_control | 0.98 | 0.25 | 0.5 | 24867 | -821914 | -0.000140608 | 0.000189917 | 0 | -0.000330524 | -57053.8 | -824876 | 0.253968 | -7.16804 | False | False | True | False |
| S09_q98_sp50_liq50 | S09 | zero_latency_spread_only_control | 0.98 | 0.5 | 0.5 | 24867 | -821914 | -0.000140608 | 0.000189917 | 0 | -0.000330524 | -57053.8 | -824876 | 0.253968 | -7.16804 | False | False | True | False |
| S02_q95_sp25_liq75 | S02 | zero_latency_spread_only_control | 0.95 | 0.25 | 0.75 | 12879 | -829873 | -0.000546415 | 9.79463e-05 | 0 | -0.000644361 | -95763.5 | -829699 | 0.282895 | -6.69087 | False | False | True | False |
| S01_q98_sp25_liq75 | S01 | zero_latency_spread_only_control | 0.98 | 0.25 | 0.75 | 1944 | -878572 | -0.00437383 | 0.000145573 | 0 | -0.0045194 | -67850.7 | -878494 | 0.110169 | -11.0312 | False | False | True | False |
| S02_q95_sp25_liq50 | S02 | zero_latency_spread_only_control | 0.95 | 0.25 | 0.5 | 14602 | -888965 | -0.000511676 | 9.712e-05 | 0 | -0.000608796 | -95507.4 | -888219 | 0.301205 | -6.74516 | False | False | True | False |
| S09_q90_sp25_liq75 | S09 | zero_latency_spread_only_control | 0.9 | 0.25 | 0.75 | 23950 | -892129 | -0.000169606 | 0.00020289 | 0 | -0.000372496 | -84147.6 | -891181 | 0.263514 | -6.72328 | False | False | True | False |
| S09_q90_sp50_liq75 | S09 | zero_latency_spread_only_control | 0.9 | 0.5 | 0.75 | 30283 | -931386 | -0.000129047 | 0.000178513 | 0 | -0.000307561 | -84147.6 | -930438 | 0.291391 | -6.64761 | False | False | True | False |
| S01_q95_sp25_liq75 | S01 | stressed_retail | 0.95 | 0.25 | 0.75 | 6519 | -943611 | -1.77171e-05 | 0.00142976 | 0.000826835 | -0.00144748 | -44080.7 | -944526 | 0.198582 | -10.9162 | True | False | True | False |
| S01_q98_sp50_liq75 | S01 | stressed_retail | 0.98 | 0.5 | 0.75 | 6562 | -951185 | -1.0842e-05 | 0.00143869 | 0.00082682 | -0.00144954 | -61877.2 | -951770 | 0.272 | -8.44931 | True | False | True | False |
| S05_q95_sp25_liq50 | S05 | zero_latency_spread_only_control | 0.95 | 0.25 | 0.5 | 43204 | -987092 | -3.65375e-05 | 0.000191935 | 0 | -0.000228472 | -84147.6 | -991821 | 0.270833 | -6.27036 | False | False | True | False |
| S07_q98_sp25_liq75 | S07 | retail_marketable_default | 0.98 | 0.25 | 0.75 | 8181 | -997628 | 0.000202569 | 0.00142201 | 0.00082679 | -0.00121944 | -51229.2 | -983964 | 0.0897436 | -14.5697 | True | False | True | False |
| S07_q98_sp50_liq75 | S07 | retail_marketable_default | 0.98 | 0.5 | 0.75 | 8181 | -997628 | 0.000202569 | 0.00142201 | 0.00082679 | -0.00121944 | -51229.2 | -983964 | 0.0897436 | -14.5697 | True | False | True | False |
| S09_q95_sp25_liq50 | S09 | zero_latency_spread_only_control | 0.95 | 0.25 | 0.5 | 43160 | -1.00903e+06 | -4.19911e-05 | 0.000191798 | 0 | -0.000233789 | -85803.8 | -1.01376e+06 | 0.270833 | -6.19532 | False | False | True | False |
| S09_q95_sp50_liq50 | S09 | zero_latency_spread_only_control | 0.95 | 0.5 | 0.5 | 43160 | -1.00903e+06 | -4.19911e-05 | 0.000191798 | 0 | -0.000233789 | -85803.8 | -1.01376e+06 | 0.270833 | -6.19532 | False | False | True | False |
| S05_q98_sp25_liq75 | S05 | retail_marketable_default | 0.98 | 0.25 | 0.75 | 7884 | -1.02575e+06 | 4.81545e-05 | 0.00134921 | 0.000826814 | -0.00130105 | -49217.4 | -995087 | 0.0705882 | -13.6581 | True | False | True | False |
| S05_q98_sp50_liq75 | S05 | retail_marketable_default | 0.98 | 0.5 | 0.75 | 7884 | -1.02575e+06 | 4.81545e-05 | 0.00134921 | 0.000826814 | -0.00130105 | -49217.4 | -995087 | 0.0705882 | -13.6581 | True | False | True | False |
| S01_q95_sp25_liq50 | S01 | retail_marketable_default | 0.95 | 0.25 | 0.5 | 9103 | -1.03968e+06 | -1.94505e-05 | 0.00112268 | 0.000826821 | -0.00114213 | -38895.4 | -1.03903e+06 | 0.172973 | -10.5859 | True | False | True | False |
| S01_q98_sp50_liq50 | S01 | stressed_retail | 0.98 | 0.5 | 0.5 | 7388 | -1.05197e+06 | 1.48854e-06 | 0.00142538 | 0.000826816 | -0.00142389 | -61877.2 | -1.0523e+06 | 0.189024 | -7.87334 | True | False | True | False |
| S05_q90_sp25_liq50 | S05 | zero_latency_spread_only_control | 0.9 | 0.25 | 0.5 | 77503 | -1.13107e+06 | 5.42298e-07 | 0.000146481 | 0 | -0.000145939 | -84147.6 | -1.14014e+06 | 0.319588 | -5.78755 | False | False | True | False |
| S01_q95_sp25_liq50 | S01 | stressed_retail | 0.95 | 0.25 | 0.5 | 8648 | -1.1777e+06 | 4.47537e-05 | 0.00140657 | 0.000826829 | -0.00136181 | -44280.9 | -1.17844e+06 | 0.131148 | -10.8671 | True | False | True | False |
| S05_q95_sp50_liq75 | S05 | zero_latency_spread_only_control | 0.95 | 0.5 | 0.75 | 29932 | -1.1839e+06 | -0.000158548 | 0.000236983 | 0 | -0.000395531 | -157879 | -1.15591e+06 | 0.368 | -5.28798 | False | False | True | False |
| S01_q98_sp25_liq50 | S01 | zero_latency_spread_only_control | 0.98 | 0.25 | 0.5 | 2493 | -1.20141e+06 | -0.00468548 | 0.000133633 | 0 | -0.00481912 | -75704.9 | -1.20141e+06 | 0.0382166 | -12.1017 | False | False | True | False |
| S05_q90_sp50_liq75 | S05 | zero_latency_spread_only_control | 0.9 | 0.5 | 0.75 | 42260 | -1.22815e+06 | -9.6686e-05 | 0.000193932 | 0 | -0.000290618 | -157879 | -1.20016e+06 | 0.380952 | -5.29498 | False | False | True | False |
| S09_q90_sp50_liq50 | S09 | zero_latency_spread_only_control | 0.9 | 0.5 | 0.5 | 63427 | -1.24878e+06 | -4.2595e-05 | 0.000154289 | 0 | -0.000196884 | -84147.6 | -1.25344e+06 | 0.205882 | -7.14205 | False | False | True | False |
| S02_q95_sp25_liq75 | S02 | retail_marketable_default | 0.95 | 0.25 | 0.75 | 12066 | -1.26488e+06 | 4.53224e-05 | 0.00109363 | 0.000826823 | -0.0010483 | -97546.2 | -1.26894e+06 | 0.205298 | -8.35827 | True | False | True | False |

## Top Realistic Variant Results

| variant_id | strategy_id | execution_profile | threshold_quantile | spread_quantile | liquidity_quantile | trades | annual_net_pnl_inr | mean_gross_return | mean_cost_return | mean_zerodha_charge_return | mean_net_return | worst_daily_net_pnl_inr | max_drawdown_inr | positive_day_fraction | annualized_sharpe_proxy | realistic_profile | positive_after_costs | enough_trades | candidate_for_deeper_synthetic_replay |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01_q98_sp25_liq75 | S01 | retail_marketable_default | 0.98 | 0.25 | 0.75 | 1726 | -184924 | 0.000119851 | 0.00119126 | 0.000826856 | -0.0010714 | -16305.6 | -185057 | 0.267241 | -6.02875 | True | False | True | False |
| S01_q98_sp25_liq50 | S01 | retail_marketable_default | 0.98 | 0.25 | 0.5 | 2193 | -250930 | 2.50424e-05 | 0.00116928 | 0.000826845 | -0.00114423 | -16683 | -251568 | 0.276316 | -6.74007 | True | False | True | False |
| S01_q98_sp25_liq75 | S01 | stressed_retail | 0.98 | 0.25 | 0.75 | 1622 | -261010 | -9.62827e-05 | 0.0015129 | 0.000826856 | -0.00160918 | -21236.1 | -261248 | 0.25 | -8.40506 | True | False | True | False |
| S02_q98_sp25_liq75 | S02 | retail_marketable_default | 0.98 | 0.25 | 0.75 | 2858 | -275071 | 0.000148444 | 0.0011109 | 0.000826815 | -0.000962458 | -37706.3 | -283503 | 0.280899 | -6.64251 | True | False | True | False |
| S02_q98_sp25_liq50 | S02 | retail_marketable_default | 0.98 | 0.25 | 0.5 | 2894 | -276977 | 0.000153384 | 0.00111046 | 0.000826815 | -0.000957073 | -37706.3 | -285409 | 0.280899 | -6.6972 | True | False | True | False |
| S01_q98_sp25_liq50 | S01 | stressed_retail | 0.98 | 0.25 | 0.5 | 2055 | -318498 | -7.09963e-05 | 0.00147887 | 0.000826849 | -0.00154987 | -21442.6 | -318590 | 0.213793 | -8.84906 | True | False | True | False |
| S02_q98_sp25_liq75 | S02 | stressed_retail | 0.98 | 0.25 | 0.75 | 2709 | -433843 | -0.000211605 | 0.00138988 | 0.000826815 | -0.00160149 | -52529.1 | -430521 | 0.137931 | -7.97463 | True | False | True | False |
| S02_q98_sp25_liq50 | S02 | stressed_retail | 0.98 | 0.25 | 0.5 | 2746 | -434183 | -0.000192072 | 0.00138908 | 0.000826814 | -0.00158115 | -52529.1 | -430861 | 0.137931 | -7.98074 | True | False | True | False |
| S01_q98_sp50_liq75 | S01 | retail_marketable_default | 0.98 | 0.5 | 0.75 | 7022 | -603224 | 0.000307447 | 0.0011665 | 0.000826832 | -0.000859049 | -36146.1 | -605812 | 0.272 | -7.05164 | True | False | True | False |
| S01_q98_sp50_liq50 | S01 | retail_marketable_default | 0.98 | 0.5 | 0.5 | 7914 | -711974 | 0.000256882 | 0.00115652 | 0.000826829 | -0.000899639 | -36146.1 | -711932 | 0.22619 | -6.98834 | True | False | True | False |
| S01_q95_sp25_liq75 | S01 | retail_marketable_default | 0.95 | 0.25 | 0.75 | 6887 | -759609 | 3.45746e-05 | 0.00113754 | 0.000826822 | -0.00110296 | -38061.7 | -759352 | 0.223776 | -9.64406 | True | False | True | False |
| S01_q95_sp25_liq75 | S01 | stressed_retail | 0.95 | 0.25 | 0.75 | 6519 | -943611 | -1.77171e-05 | 0.00142976 | 0.000826835 | -0.00144748 | -44080.7 | -944526 | 0.198582 | -10.9162 | True | False | True | False |
| S01_q98_sp50_liq75 | S01 | stressed_retail | 0.98 | 0.5 | 0.75 | 6562 | -951185 | -1.0842e-05 | 0.00143869 | 0.00082682 | -0.00144954 | -61877.2 | -951770 | 0.272 | -8.44931 | True | False | True | False |
| S07_q98_sp25_liq75 | S07 | retail_marketable_default | 0.98 | 0.25 | 0.75 | 8181 | -997628 | 0.000202569 | 0.00142201 | 0.00082679 | -0.00121944 | -51229.2 | -983964 | 0.0897436 | -14.5697 | True | False | True | False |
| S07_q98_sp50_liq75 | S07 | retail_marketable_default | 0.98 | 0.5 | 0.75 | 8181 | -997628 | 0.000202569 | 0.00142201 | 0.00082679 | -0.00121944 | -51229.2 | -983964 | 0.0897436 | -14.5697 | True | False | True | False |
| S05_q98_sp25_liq75 | S05 | retail_marketable_default | 0.98 | 0.25 | 0.75 | 7884 | -1.02575e+06 | 4.81545e-05 | 0.00134921 | 0.000826814 | -0.00130105 | -49217.4 | -995087 | 0.0705882 | -13.6581 | True | False | True | False |
| S05_q98_sp50_liq75 | S05 | retail_marketable_default | 0.98 | 0.5 | 0.75 | 7884 | -1.02575e+06 | 4.81545e-05 | 0.00134921 | 0.000826814 | -0.00130105 | -49217.4 | -995087 | 0.0705882 | -13.6581 | True | False | True | False |
| S01_q95_sp25_liq50 | S01 | retail_marketable_default | 0.95 | 0.25 | 0.5 | 9103 | -1.03968e+06 | -1.94505e-05 | 0.00112268 | 0.000826821 | -0.00114213 | -38895.4 | -1.03903e+06 | 0.172973 | -10.5859 | True | False | True | False |
| S01_q98_sp50_liq50 | S01 | stressed_retail | 0.98 | 0.5 | 0.5 | 7388 | -1.05197e+06 | 1.48854e-06 | 0.00142538 | 0.000826816 | -0.00142389 | -61877.2 | -1.0523e+06 | 0.189024 | -7.87334 | True | False | True | False |
| S01_q95_sp25_liq50 | S01 | stressed_retail | 0.95 | 0.25 | 0.5 | 8648 | -1.1777e+06 | 4.47537e-05 | 0.00140657 | 0.000826829 | -0.00136181 | -44280.9 | -1.17844e+06 | 0.131148 | -10.8671 | True | False | True | False |
| S02_q95_sp25_liq75 | S02 | retail_marketable_default | 0.95 | 0.25 | 0.75 | 12066 | -1.26488e+06 | 4.53224e-05 | 0.00109363 | 0.000826823 | -0.0010483 | -97546.2 | -1.26894e+06 | 0.205298 | -8.35827 | True | False | True | False |
| S05_q98_sp25_liq75 | S05 | stressed_retail | 0.98 | 0.25 | 0.75 | 7689 | -1.3023e+06 | 0.000120262 | 0.00181397 | 0.000826816 | -0.00169371 | -63703.2 | -1.26551e+06 | 0.0722892 | -13.638 | True | False | True | False |
| S05_q98_sp50_liq75 | S05 | stressed_retail | 0.98 | 0.5 | 0.75 | 7689 | -1.3023e+06 | 0.000120262 | 0.00181397 | 0.000826816 | -0.00169371 | -63703.2 | -1.26551e+06 | 0.0722892 | -13.638 | True | False | True | False |
| S02_q95_sp25_liq50 | S02 | retail_marketable_default | 0.95 | 0.25 | 0.5 | 13677 | -1.40407e+06 | 6.53716e-05 | 0.00109197 | 0.000826823 | -0.0010266 | -104006 | -1.40561e+06 | 0.174699 | -8.42758 | True | False | True | False |
| S07_q98_sp25_liq75 | S07 | stressed_retail | 0.98 | 0.25 | 0.75 | 7941 | -1.41973e+06 | 9.91697e-05 | 0.00188702 | 0.000826819 | -0.00178785 | -50986.7 | -1.38956e+06 | 0 | -20.7196 | True | False | True | False |
| S07_q98_sp50_liq75 | S07 | stressed_retail | 0.98 | 0.5 | 0.75 | 7941 | -1.41973e+06 | 9.91697e-05 | 0.00188702 | 0.000826819 | -0.00178785 | -50986.7 | -1.38956e+06 | 0 | -20.7196 | True | False | True | False |
| S09_q98_sp25_liq75 | S09 | retail_marketable_default | 0.98 | 0.25 | 0.75 | 10541 | -1.5731e+06 | -8.08044e-05 | 0.00141156 | 0.000826802 | -0.00149236 | -75187.2 | -1.55107e+06 | 0.0363636 | -15.4465 | True | False | True | False |
| S09_q98_sp50_liq75 | S09 | retail_marketable_default | 0.98 | 0.5 | 0.75 | 10541 | -1.5731e+06 | -8.08044e-05 | 0.00141156 | 0.000826802 | -0.00149236 | -75187.2 | -1.55107e+06 | 0.0363636 | -15.4465 | True | False | True | False |
| S02_q95_sp25_liq75 | S02 | stressed_retail | 0.95 | 0.25 | 0.75 | 11406 | -1.6399e+06 | -7.58495e-05 | 0.0013619 | 0.000826817 | -0.00143775 | -82664.6 | -1.63931e+06 | 0.107383 | -10.373 | True | False | True | False |
| S01_q90_sp25_liq75 | S01 | retail_marketable_default | 0.9 | 0.25 | 0.75 | 15247 | -1.67571e+06 | 2.68947e-05 | 0.00112594 | 0.000826816 | -0.00109904 | -69630.6 | -1.6728e+06 | 0.132075 | -12.3704 | True | False | True | False |
| S02_q98_sp50_liq75 | S02 | retail_marketable_default | 0.98 | 0.5 | 0.75 | 14792 | -1.71977e+06 | -6.09971e-06 | 0.00115654 | 0.000826808 | -0.00116264 | -130884 | -1.71489e+06 | 0.235849 | -9.16776 | True | False | True | False |
| S02_q98_sp50_liq50 | S02 | retail_marketable_default | 0.98 | 0.5 | 0.5 | 14850 | -1.72698e+06 | -6.72386e-06 | 0.00115623 | 0.000826808 | -0.00116295 | -130884 | -1.7221e+06 | 0.231481 | -9.0826 | True | False | True | False |
| S02_q95_sp25_liq50 | S02 | stressed_retail | 0.95 | 0.25 | 0.5 | 12892 | -1.82883e+06 | -5.91888e-05 | 0.00135939 | 0.000826814 | -0.00141858 | -91468.9 | -1.82436e+06 | 0.109756 | -10.5252 | True | False | True | False |
| S01_q95_sp50_liq75 | S01 | retail_marketable_default | 0.95 | 0.5 | 0.75 | 21694 | -1.92205e+06 | 0.000250176 | 0.00113616 | 0.000826809 | -0.000885984 | -79875.8 | -1.93352e+06 | 0.213333 | -9.92944 | True | False | True | False |
| S02_q98_sp50_liq75 | S02 | stressed_retail | 0.98 | 0.5 | 0.75 | 14102 | -1.93878e+06 | 4.44279e-05 | 0.00141925 | 0.000826802 | -0.00137482 | -123282 | -1.93221e+06 | 0.152381 | -10.5907 | True | False | True | False |
| S02_q98_sp50_liq50 | S02 | stressed_retail | 0.98 | 0.5 | 0.5 | 14161 | -1.93983e+06 | 4.90059e-05 | 0.00141884 | 0.000826802 | -0.00136984 | -123282 | -1.93326e+06 | 0.149533 | -10.4603 | True | False | True | False |
| S09_q98_sp25_liq75 | S09 | stressed_retail | 0.98 | 0.25 | 0.75 | 10207 | -1.95696e+06 | -4.2262e-05 | 0.00187501 | 0.000826821 | -0.00191727 | -52809.8 | -1.92757e+06 | 0.0277778 | -18.8422 | True | False | True | False |
| S09_q98_sp50_liq75 | S09 | stressed_retail | 0.98 | 0.5 | 0.75 | 10207 | -1.95696e+06 | -4.2262e-05 | 0.00187501 | 0.000826821 | -0.00191727 | -52809.8 | -1.92757e+06 | 0.0277778 | -18.8422 | True | False | True | False |
| S07_q95_sp25_liq75 | S07 | retail_marketable_default | 0.95 | 0.25 | 0.75 | 15778 | -1.96231e+06 | 0.000178959 | 0.00142266 | 0.000826797 | -0.0012437 | -70995.7 | -1.91863e+06 | 0.0357143 | -18.303 | True | False | True | False |
| S07_q95_sp50_liq75 | S07 | retail_marketable_default | 0.95 | 0.5 | 0.75 | 15778 | -1.96231e+06 | 0.000178959 | 0.00142266 | 0.000826797 | -0.0012437 | -70995.7 | -1.91863e+06 | 0.0357143 | -18.303 | True | False | True | False |
| S07_q90_sp25_liq75 | S07 | retail_marketable_default | 0.9 | 0.25 | 0.75 | 17319 | -2.09805e+06 | 0.000174862 | 0.00138627 | 0.000826798 | -0.00121141 | -70995.7 | -2.0546e+06 | 0.0357143 | -20.4168 | True | False | True | False |
| S01_q90_sp25_liq75 | S01 | stressed_retail | 0.9 | 0.25 | 0.75 | 14605 | -2.13888e+06 | -5.04512e-05 | 0.00141403 | 0.000826825 | -0.00146448 | -76172.3 | -2.14285e+06 | 0.151899 | -12.994 | True | False | True | False |
| S07_q98_sp25_liq50 | S07 | retail_marketable_default | 0.98 | 0.25 | 0.5 | 17143 | -2.25231e+06 | 7.14882e-05 | 0.00138532 | 0.000826803 | -0.00131383 | -51229.2 | -2.23173e+06 | 0.0480769 | -22.3996 | True | False | True | False |
| S07_q98_sp50_liq50 | S07 | retail_marketable_default | 0.98 | 0.5 | 0.5 | 17143 | -2.25231e+06 | 7.14882e-05 | 0.00138532 | 0.000826803 | -0.00131383 | -51229.2 | -2.23173e+06 | 0.0480769 | -22.3996 | True | False | True | False |
| S01_q95_sp50_liq50 | S01 | retail_marketable_default | 0.95 | 0.5 | 0.5 | 25810 | -2.40165e+06 | 0.000195313 | 0.00112582 | 0.000826811 | -0.000930511 | -79875.8 | -2.40831e+06 | 0.180412 | -10.3047 | True | False | True | False |
| S07_q90_sp50_liq75 | S07 | retail_marketable_default | 0.9 | 0.5 | 0.75 | 19932 | -2.42765e+06 | 0.000121405 | 0.00133937 | 0.000826799 | -0.00121797 | -70995.7 | -2.38421e+06 | 0.0357143 | -21.5217 | True | False | True | False |
| S07_q95_sp25_liq75 | S07 | stressed_retail | 0.95 | 0.25 | 0.75 | 15314 | -2.6376e+06 | 0.000165598 | 0.00188795 | 0.000826801 | -0.00172235 | -79698.4 | -2.58206e+06 | 0 | -21.1548 | True | False | True | False |
| S07_q95_sp50_liq75 | S07 | stressed_retail | 0.95 | 0.5 | 0.75 | 15314 | -2.6376e+06 | 0.000165598 | 0.00188795 | 0.000826801 | -0.00172235 | -79698.4 | -2.58206e+06 | 0 | -21.1548 | True | False | True | False |
| S01_q90_sp25_liq50 | S01 | retail_marketable_default | 0.9 | 0.25 | 0.5 | 23422 | -2.64599e+06 | -2.20274e-05 | 0.00110768 | 0.000826816 | -0.0011297 | -72068.1 | -2.64058e+06 | 0.136585 | -13.1944 | True | False | True | False |
| S01_q95_sp50_liq75 | S01 | stressed_retail | 0.95 | 0.5 | 0.75 | 20495 | -2.73391e+06 | 6.39085e-05 | 0.00139785 | 0.000826811 | -0.00133394 | -97450.1 | -2.73415e+06 | 0.198675 | -11.0061 | True | False | True | False |
| S07_q90_sp25_liq75 | S07 | stressed_retail | 0.9 | 0.25 | 0.75 | 16795 | -2.77402e+06 | 0.000178519 | 0.00183021 | 0.000826803 | -0.00165169 | -79698.4 | -2.71847e+06 | 0 | -23.3119 | True | False | True | False |
| S02_q90_sp25_liq75 | S02 | retail_marketable_default | 0.9 | 0.25 | 0.75 | 26861 | -2.8325e+06 | 3.64151e-05 | 0.00109092 | 0.000826816 | -0.0010545 | -135276 | -2.82445e+06 | 0.0886076 | -12.0012 | True | False | True | False |
| S05_q98_sp25_liq50 | S05 | retail_marketable_default | 0.98 | 0.25 | 0.5 | 21806 | -2.91615e+06 | 1.02469e-05 | 0.00134756 | 0.000826812 | -0.00133731 | -62352.6 | -2.91243e+06 | 0.0392157 | -16.99 | True | False | True | False |
| S05_q98_sp50_liq50 | S05 | retail_marketable_default | 0.98 | 0.5 | 0.5 | 21806 | -2.91615e+06 | 1.02469e-05 | 0.00134756 | 0.000826812 | -0.00133731 | -62352.6 | -2.91243e+06 | 0.0392157 | -16.99 | True | False | True | False |
| S09_q95_sp25_liq75 | S09 | retail_marketable_default | 0.95 | 0.25 | 0.75 | 19863 | -2.98694e+06 | -9.09883e-05 | 0.00141278 | 0.000826806 | -0.00150377 | -125904 | -2.94593e+06 | 0.0403226 | -14.8249 | True | False | True | False |
| S09_q95_sp50_liq75 | S09 | retail_marketable_default | 0.95 | 0.5 | 0.75 | 19863 | -2.98694e+06 | -9.09883e-05 | 0.00141278 | 0.000826806 | -0.00150377 | -125904 | -2.94593e+06 | 0.0403226 | -14.8249 | True | False | True | False |
| S05_q95_sp25_liq75 | S05 | retail_marketable_default | 0.95 | 0.25 | 0.75 | 19907 | -3.00112e+06 | -9.45383e-05 | 0.00141303 | 0.000826806 | -0.00150757 | -127204 | -2.96012e+06 | 0.0403226 | -14.7523 | True | False | True | False |
| S07_q98_sp25_liq50 | S07 | stressed_retail | 0.98 | 0.25 | 0.5 | 16648 | -3.02292e+06 | 3.18526e-05 | 0.00184764 | 0.000826816 | -0.00181579 | -66378.8 | -2.98325e+06 | 0.0192308 | -28.4647 | True | False | True | False |
| S07_q98_sp50_liq50 | S07 | stressed_retail | 0.98 | 0.5 | 0.5 | 16648 | -3.02292e+06 | 3.18526e-05 | 0.00184764 | 0.000826816 | -0.00181579 | -66378.8 | -2.98325e+06 | 0.0192308 | -28.4647 | True | False | True | False |
| S01_q90_sp25_liq50 | S01 | stressed_retail | 0.9 | 0.25 | 0.5 | 22513 | -3.07075e+06 | 2.13221e-05 | 0.00138531 | 0.00082682 | -0.00136399 | -81427.2 | -3.07009e+06 | 0.0686275 | -13.8599 | True | False | True | False |

## Strategy Rollup

| strategy_id | execution_profile | variants | positive_rows | candidate_rows | best_annual_net_pnl_inr | best_mean_net_return | min_trades | max_trades | best_positive_day_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S07 | zero_latency_spread_only_control | 12 | 2 | 0 | 85087.1 | 9.86631e-05 | 8624 | 38957 | 0.506329 |
| S05 | zero_latency_spread_only_control | 12 | 2 | 0 | 3917.99 | 4.72902e-06 | 8285 | 87403 | 0.511628 |
| S01 | retail_marketable_default | 12 | 0 | 0 | -184924 | -0.000859049 | 1726 | 58489 | 0.276316 |
| S01 | stressed_retail | 12 | 0 | 0 | -261010 | -0.0012482 | 1622 | 56139 | 0.272 |
| S02 | retail_marketable_default | 12 | 0 | 0 | -275071 | -0.000957073 | 2858 | 110741 | 0.280899 |
| S02 | zero_latency_spread_only_control | 12 | 0 | 0 | -285593 | -0.000441854 | 3091 | 117357 | 0.30303 |
| S02 | stressed_retail | 12 | 0 | 0 | -433843 | -0.00130889 | 2709 | 105416 | 0.152381 |
| S09 | zero_latency_spread_only_control | 12 | 0 | 0 | -544256 | -0.000196884 | 11109 | 63427 | 0.368 |
| S01 | zero_latency_spread_only_control | 12 | 0 | 0 | -878572 | -0.00131359 | 1944 | 62896 | 0.175 |
| S07 | retail_marketable_default | 12 | 0 | 0 | -997628 | -0.00121141 | 8181 | 36941 | 0.0897436 |
| S05 | retail_marketable_default | 12 | 0 | 0 | -1.02575e+06 | -0.00127894 | 7884 | 83100 | 0.0705882 |
| S05 | stressed_retail | 12 | 0 | 0 | -1.3023e+06 | -0.00167916 | 7689 | 80517 | 0.0722892 |
| S07 | stressed_retail | 12 | 0 | 0 | -1.41973e+06 | -0.00161094 | 7941 | 35843 | 0.0338983 |
| S09 | retail_marketable_default | 12 | 0 | 0 | -1.5731e+06 | -0.00125037 | 10541 | 60281 | 0.0748299 |
| S09 | stressed_retail | 12 | 0 | 0 | -1.95696e+06 | -0.00163713 | 10207 | 58308 | 0.0743243 |

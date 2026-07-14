# Phase 28 Richer Event Label Support

Generated UTC: 2026-07-14T18:19:00.657872+00:00

This milestone engineers explicit proxy labels for the partial strategy families S03/S04/S06/S08 from the current received-tick delta product.
All labels remain weak market-by-price inferences and are not exchange-observed order events.

## Overall Summary

| metric | value | description |
| --- | --- | --- |
| phase28_received_delta_rows | 620853 | Received tick-delta rows scanned |
| phase28_symbols_evaluated | 32 | Symbols evaluated |
| phase28_partial_strategy_families | 4 | Partial strategy families evaluated |
| phase28_proxy_feature_engineered_families | 4 | Partial families with proxy feature labels now engineered |
| phase28_total_proxy_label_rows | 290162 | Total proxy label rows or buckets across S03/S04/S06/S08 |
| phase28_acceptance_ready | 0 | Richer labels are weak market-by-price proxies, not acceptance evidence |

## Strategy Support Summary

| strategy_id | feature_label_family | proxy_rows | symbols_with_proxy | symbols_evaluated | support_upgrade_status | acceptance_ready | required_next_evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S03 | liquidity vacuum/reversal | 47449 | 31 | 32 | partial_proxy_feature_engineered | False | multi-day Class B labels, common-shock controls, broker/exchange fill/cost reconciliation and acceptance replay |
| S04 | trade-flow plus depth confirmation | 38481 | 32 | 32 | partial_proxy_feature_engineered | False | multi-day Class B labels, common-shock controls, broker/exchange fill/cost reconciliation and acceptance replay |
| S06 | absorption-like replenishment | 71244 | 32 | 32 | partial_proxy_feature_engineered | False | multi-day Class B labels, common-shock controls, broker/exchange fill/cost reconciliation and acceptance replay |
| S08 | cross-symbol/index lead-lag OFI | 132988 | 32 | 32 | partial_proxy_feature_engineered | False | multi-day lead-lag stability, timestamp-skew tests, simultaneous-shock controls and out-of-sample acceptance replay |

## Feature Label Catalog

| strategy_id | feature_label | required_inputs | current_support | acceptance_blocker |
| --- | --- | --- | --- | --- |
| S03 | liquidity_vacuum_reversal_proxy | depth withdrawal, spread widening/normalization, local volatility, future mid move | proxy_feature_available | market-by-price feed cannot prove hidden liquidity, exact queue state or true cause of withdrawal/reversal |
| S04 | trade_flow_depth_confirmation_proxy | volume increment, weak aggressor side, MLOFI sign, L5 imbalance sign | proxy_feature_available | aggressor side is weakly inferred and not exchange-confirmed |
| S06 | absorption_like_replenishment_proxy | volume increment, weak aggressor side, visible replenishment, low realized mid move | proxy_feature_available | cannot distinguish iceberg/absorption from ordinary market-by-price aggregation and replenishment |
| S08 | cross_symbol_lead_lag_mlofi_proxy | 5s receive bucket, symbol MLOFI, ex-self market MLOFI, next-bucket return | proxy_feature_available | one-day receive-time correlation is not causal lead-lag and needs multi-day timestamp-skew/common-shock controls |

## Event Label Summary

| symbol | rows | usable_short_horizon_rows | s03_liquidity_vacuum_proxy_rows | s03_reversal_candidate_proxy_rows | s04_trade_flow_depth_confirm_rows | s06_absorption_like_proxy_rows | s08_lead_lag_bucket_rows | medium_confidence_rows | low_confidence_rows | stale_gap_gt_5s_rows | acceptance_grade |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | 13886 | 12865 | 1625 | 214 | 670 | 893 | 4127 | 0 | 0 | 1018 | False |
| AXISBANK | 18309 | 17464 | 1103 | 122 | 1131 | 1938 | 4183 | 0 | 0 | 840 | False |
| BAJAJ-AUTO | 25141 | 24588 | 3359 | 682 | 1521 | 1281 | 4261 | 0 | 0 | 549 | False |
| BANKBEES | 18916 | 18166 | 59 | 24 | 300 | 696 | 4002 | 0 | 0 | 750 | False |
| BHARTIARTL | 19560 | 18768 | 1573 | 196 | 1155 | 1910 | 4300 | 0 | 0 | 788 | False |
| BPCL | 10684 | 9438 | 74 | 14 | 354 | 920 | 3988 | 0 | 0 | 1243 | False |
| BRITANNIA | 8526 | 7060 | 465 | 43 | 229 | 470 | 3606 | 0 | 0 | 1463 | False |
| CIPLA | 11664 | 10529 | 810 | 74 | 464 | 839 | 4024 | 0 | 0 | 1131 | False |
| DRREDDY | 12257 | 11185 | 1317 | 63 | 532 | 677 | 4124 | 0 | 0 | 1065 | False |
| GOLDBEES | 12982 | 11937 | 6 | 1 | 385 | 1494 | 4078 | 0 | 0 | 1042 | False |
| HCLTECH | 29266 | 28773 | 4012 | 635 | 2588 | 4140 | 4343 | 0 | 0 | 487 | False |
| HDFCBANK | 35959 | 35740 | 1109 | 206 | 2890 | 7405 | 4447 | 0 | 0 | 212 | False |
| HINDUNILVR | 12173 | 11066 | 1226 | 123 | 532 | 597 | 4041 | 0 | 0 | 1102 | False |
| ICICIBANK | 26474 | 25939 | 1803 | 268 | 1927 | 3451 | 4334 | 0 | 0 | 531 | False |
| INFY | 34511 | 34247 | 4316 | 758 | 3240 | 5436 | 4449 | 0 | 0 | 257 | False |
| ITBEES | 11481 | 10336 | 0 | 0 | 376 | 1488 | 4006 | 0 | 0 | 1143 | False |
| ITC | 12379 | 11311 | 24 | 6 | 671 | 2247 | 4097 | 0 | 0 | 1063 | False |
| JUNIORBEES | 17442 | 16539 | 203 | 70 | 436 | 1175 | 4005 | 0 | 0 | 902 | False |
| KOTAKBANK | 14091 | 13095 | 119 | 17 | 745 | 1986 | 4104 | 0 | 0 | 993 | False |
| LT | 19466 | 18694 | 2669 | 389 | 1349 | 1347 | 4222 | 0 | 0 | 767 | False |
| M&M | 25699 | 25185 | 3608 | 831 | 1769 | 1765 | 4329 | 0 | 0 | 511 | False |
| MARUTI | 27645 | 27273 | 3272 | 562 | 1623 | 2035 | 4406 | 0 | 0 | 369 | False |
| NESTLEIND | 12918 | 11777 | 799 | 90 | 507 | 705 | 3946 | 0 | 0 | 1137 | False |
| NIFTYBEES | 22414 | 21763 | 5 | 0 | 866 | 2859 | 4214 | 0 | 0 | 649 | False |
| ONGC | 17305 | 16439 | 73 | 15 | 1014 | 2881 | 4204 | 0 | 0 | 863 | False |
| RELIANCE | 26056 | 25435 | 1210 | 196 | 1843 | 4220 | 4287 | 0 | 0 | 615 | False |
| SBIN | 24728 | 24111 | 1318 | 200 | 1757 | 3745 | 4285 | 0 | 0 | 611 | False |
| SUNPHARMA | 14610 | 13566 | 1336 | 161 | 833 | 1176 | 4074 | 0 | 0 | 1040 | False |
| TCS | 36467 | 36271 | 6565 | 1195 | 3531 | 4029 | 4474 | 0 | 0 | 190 | False |
| TECHM | 19124 | 18292 | 2580 | 360 | 1315 | 1786 | 4139 | 0 | 0 | 828 | False |
| ULTRACEMCO | 8386 | 6958 | 773 | 78 | 251 | 339 | 3723 | 0 | 0 | 1426 | False |
| WIPRO | 20334 | 19550 | 38 | 9 | 1677 | 5314 | 4166 | 0 | 0 | 781 | False |

## Lead-Lag Proxy Summary

| symbol | lead_lag_bucket_rows | lead_lag_abs_corr_proxy | lead_lag_corr_proxy | s08_proxy_available | acceptance_grade | limitation |
| --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | 4127 | 0.0199261 | -0.0199261 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| AXISBANK | 4183 | 0.0236892 | 0.0236892 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| BAJAJ-AUTO | 4261 | 0.0101917 | -0.0101917 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| BANKBEES | 4002 | 0.00802841 | -0.00802841 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| BHARTIARTL | 4300 | 0.026432 | 0.026432 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| BPCL | 3988 | 0.0116549 | -0.0116549 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| BRITANNIA | 3606 | 0.0306556 | -0.0306556 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| CIPLA | 4024 | 0.0213542 | -0.0213542 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| DRREDDY | 4124 | 0.00166903 | 0.00166903 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| GOLDBEES | 4078 | 0.0154273 | 0.0154273 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| HCLTECH | 4343 | 0.00155302 | -0.00155302 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| HDFCBANK | 4447 | 0.009415 | -0.009415 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| HINDUNILVR | 4041 | 0.00418414 | -0.00418414 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| ICICIBANK | 4334 | 0.00337159 | -0.00337159 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| INFY | 4449 | 0.00551953 | 0.00551953 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| ITBEES | 4006 | 0.0531771 | -0.0531771 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| ITC | 4097 | 0.0111328 | 0.0111328 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| JUNIORBEES | 4005 | 0.000589774 | -0.000589774 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| KOTAKBANK | 4104 | 0.026926 | -0.026926 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| LT | 4222 | 0.0206193 | 0.0206193 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| M&M | 4329 | 0.00572641 | 0.00572641 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| MARUTI | 4406 | 0.00798038 | 0.00798038 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| NESTLEIND | 3946 | 0.0182752 | -0.0182752 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| NIFTYBEES | 4214 | 0.00244 | 0.00244 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| ONGC | 4204 | 0.00497107 | -0.00497107 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| RELIANCE | 4287 | 0.0103011 | -0.0103011 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| SBIN | 4285 | 0.00461747 | 0.00461747 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| SUNPHARMA | 4074 | 0.00850735 | 0.00850735 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| TCS | 4474 | 0.0138424 | 0.0138424 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| TECHM | 4139 | 0.00454524 | -0.00454524 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| ULTRACEMCO | 3723 | 0.0046229 | -0.0046229 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |
| WIPRO | 4166 | 0.00983889 | -0.00983889 | True | False | One-day receive-bucket lead-lag proxy; not causal and not exchange-synchronized. |

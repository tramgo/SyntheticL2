# Phase 27 Feature Edge Cost-Hurdle Scan

Generated UTC: 2026-07-14T18:11:13.891950+00:00

This milestone checks whether raw event-level features contain enough directional edge to clear execution costs.
It is a diagnostic for signal redesign, not a strategy promotion result.

## Overall Summary

| metric | value | description |
| --- | --- | --- |
| phase27_feature_candidates_registered | 112 | Feature/horizon/threshold candidates registered |
| phase27_candidate_profile_rows | 336 | Candidate/profile replay summary rows |
| phase27_total_replay_trades | 1213296 | Total trades across feature-edge replays |
| phase27_positive_after_cost_rows | 0 | Rows with positive mean net return after costs |
| phase27_realistic_cost_clearing_rows | 0 | Retail/stressed rows passing net, baseline, trade-count and risk filters |
| phase27_zero_latency_edge_control_rows | 0 | Frictionless positive feature-edge controls |
| phase27_rejected_candidate_rows | 336 | Candidate/profile rows rejected by at least one diagnostic |
| phase27_acceptance_ready | 0 | Feature-edge scan is diagnostic evidence, not acceptance evidence |

## Feature Family Summary

| feature_family | execution_profile | candidate_rows | positive_after_cost_rows | realistic_cost_clearing_rows | zero_latency_edge_control_rows | max_mean_net_return | max_cost_hurdle_ratio | median_trades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| depth_imbalance | retail_marketable_default | 16 | 0 | 0 | 0 | -0.00134022 | 0.0905054 | 3006 |
| depth_imbalance | stressed_retail | 16 | 0 | 0 | 0 | -0.00155394 | 0.0545793 | 2918.5 |
| depth_imbalance | zero_latency_spread_only_control | 16 | 0 | 0 | 0 | -0.000420072 | 0.255076 | 3162 |
| depth_mean_reversion | retail_marketable_default | 16 | 0 | 0 | 0 | -0.00126327 | 0.135285 | 3006 |
| depth_mean_reversion | stressed_retail | 16 | 0 | 0 | 0 | -0.0014081 | 0.150725 | 2918.5 |
| depth_mean_reversion | zero_latency_spread_only_control | 16 | 0 | 0 | 0 | -0.000347248 | 0.30429 | 3162 |
| microprice_pressure | retail_marketable_default | 16 | 0 | 0 | 0 | -0.00129368 | 0.0300949 | 2985.5 |
| microprice_pressure | stressed_retail | 16 | 0 | 0 | 0 | -0.00151676 | 0.0107637 | 2894 |
| microprice_pressure | zero_latency_spread_only_control | 16 | 0 | 0 | 0 | -0.000326397 | 0.204136 | 3152 |
| order_flow_imbalance | retail_marketable_default | 16 | 0 | 0 | 0 | -0.00117389 | 0.0629081 | 3624.5 |
| order_flow_imbalance | stressed_retail | 16 | 0 | 0 | 0 | -0.00133067 | 0.0795306 | 3506 |
| order_flow_imbalance | zero_latency_spread_only_control | 16 | 0 | 0 | 0 | -0.000301735 | -0.0775416 | 3823.5 |
| short_horizon_momentum | retail_marketable_default | 16 | 0 | 0 | 0 | -0.000926039 | 0.151163 | 2949.5 |
| short_horizon_momentum | stressed_retail | 16 | 0 | 0 | 0 | -0.00122072 | 0.0419652 | 2811 |
| short_horizon_momentum | zero_latency_spread_only_control | 16 | 0 | 0 | 0 | -0.000501581 | -1.44727 | 3145 |
| top_of_book_imbalance | retail_marketable_default | 16 | 0 | 0 | 0 | -0.0012374 | 0.082808 | 3027.5 |
| top_of_book_imbalance | stressed_retail | 16 | 0 | 0 | 0 | -0.00144835 | 0.0200836 | 2940.5 |
| top_of_book_imbalance | zero_latency_spread_only_control | 16 | 0 | 0 | 0 | -0.000266252 | 0.24311 | 3187.5 |
| top_of_book_mean_reversion | retail_marketable_default | 16 | 0 | 0 | 0 | -0.00127076 | 0.121445 | 3027.5 |
| top_of_book_mean_reversion | stressed_retail | 16 | 0 | 0 | 0 | -0.00143646 | 0.147006 | 2940.5 |
| top_of_book_mean_reversion | zero_latency_spread_only_control | 16 | 0 | 0 | 0 | -0.000384129 | 0.318613 | 3187.5 |

## Top Candidate Diagnostics

| candidate_id | feature_id | feature_family | execution_profile | horizon_events | threshold_quantile | trades | mean_gross_return | mean_cost_return | mean_net_return | best_baseline_mean_net_return | net_return_lift_vs_best_baseline | positive_after_costs | beats_best_baseline_proxy | enough_trades_for_edge | risk_status | realistic_charged_profile | risk_not_breached_proxy | cost_hurdle_ratio | realistic_cost_clearing_edge | zero_latency_edge_control |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F03_l1_imbalance_h3_q50 | F03_l1_imbalance | top_of_book_imbalance | zero_latency_spread_only_control | 3 | 0.5 | 8227 | 8.55192e-05 | 0.000351771 | -0.000266252 | -0.000473172 | 0.00020692 | False | True | True | risk_breached_proxy | False | False | 0.24311 | False | False |
| F03_l1_imbalance_h2_q50 | F03_l1_imbalance | top_of_book_imbalance | zero_latency_spread_only_control | 2 | 0.5 | 8340 | 7.48634e-05 | 0.000351812 | -0.000276948 | -0.000473172 | 0.000196224 | False | True | True | risk_not_breached_proxy | False | True | 0.212794 | False | False |
| F03_l1_imbalance_h5_q50 | F03_l1_imbalance | top_of_book_imbalance | zero_latency_spread_only_control | 5 | 0.5 | 7992 | 7.2391e-05 | 0.000351825 | -0.000279434 | -0.000473172 | 0.000193738 | False | True | True | risk_breached_proxy | False | False | 0.205759 | False | False |
| F02_mlofi_qty_event_h2_q50 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 2 | 0.5 | 9283 | -2.17133e-05 | 0.000280021 | -0.000301735 | -0.000473172 | 0.000171437 | False | True | True | risk_not_breached_proxy | False | True | -0.0775416 | False | False |
| F03_l1_imbalance_h1_q50 | F03_l1_imbalance | top_of_book_imbalance | zero_latency_spread_only_control | 1 | 0.5 | 8453 | 3.21786e-05 | 0.000351951 | -0.000319772 | -0.000473172 | 0.0001534 | False | True | True | risk_not_breached_proxy | False | True | 0.0914294 | False | False |
| F05_microprice_dev_h3_q50 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 3 | 0.5 | 7103 | 8.37196e-05 | 0.000410117 | -0.000326397 | -0.000473172 | 0.000146774 | False | True | True | risk_breached_proxy | False | False | 0.204136 | False | False |
| F05_microprice_dev_h5_q50 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 5 | 0.5 | 6891 | 7.61913e-05 | 0.000410642 | -0.00033445 | -0.000473172 | 0.000138722 | False | True | True | risk_breached_proxy | False | False | 0.185542 | False | False |
| F02_mlofi_qty_event_h1_q50 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 1 | 0.5 | 9405 | -6.09689e-05 | 0.000279899 | -0.000340868 | -0.000473172 | 0.000132304 | False | True | True | risk_not_breached_proxy | False | True | -0.217825 | False | False |
| F02_mlofi_qty_event_h5_q50 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 5 | 0.5 | 8885 | -6.05842e-05 | 0.000280447 | -0.000341032 | -0.000473172 | 0.00013214 | False | True | True | risk_not_breached_proxy | False | True | -0.216027 | False | False |
| F05_microprice_dev_h2_q50 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 2 | 0.5 | 7204 | 6.72622e-05 | 0.000410009 | -0.000342747 | -0.000473172 | 0.000130425 | False | True | True | risk_breached_proxy | False | False | 0.164051 | False | False |
| F02_mlofi_qty_event_h3_q50 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 3 | 0.5 | 9136 | -6.56205e-05 | 0.000280141 | -0.000345761 | -0.000473172 | 0.00012741 | False | True | True | risk_breached_proxy | False | False | -0.234241 | False | False |
| F06_l5_mean_reversion_h5_q50 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 5 | 0.5 | 6904 | 6.36462e-05 | 0.000410894 | -0.000347248 | -0.000473172 | 0.000125924 | False | True | True | risk_breached_proxy | False | False | 0.154897 | False | False |
| F06_l5_mean_reversion_h1_q50 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 1 | 0.5 | 7304 | 2.96452e-05 | 0.000410979 | -0.000381334 | -0.000473172 | 9.1838e-05 | False | True | True | risk_not_breached_proxy | False | True | 0.0721331 | False | False |
| F07_l1_mean_reversion_h1_q50 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 1 | 0.5 | 8453 | -3.21786e-05 | 0.000351951 | -0.000384129 | -0.000473172 | 8.90427e-05 | False | True | True | risk_not_breached_proxy | False | True | -0.0914294 | False | False |
| F05_microprice_dev_h1_q50 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 1 | 0.5 | 7300 | 2.29809e-05 | 0.000410241 | -0.000387261 | -0.000473172 | 8.59113e-05 | False | True | True | risk_not_breached_proxy | False | True | 0.056018 | False | False |
| F06_l5_mean_reversion_h2_q50 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 2 | 0.5 | 7212 | 1.01742e-05 | 0.000410525 | -0.000400351 | -0.000473172 | 7.28209e-05 | False | True | True | risk_breached_proxy | False | False | 0.0247833 | False | False |
| F06_l5_mean_reversion_h3_q50 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 3 | 0.5 | 7105 | 9.11502e-06 | 0.000410957 | -0.000401842 | -0.000473172 | 7.13299e-05 | False | True | True | risk_breached_proxy | False | False | 0.02218 | False | False |
| F04_l5_imbalance_h3_q50 | F04_l5_imbalance | depth_imbalance | zero_latency_spread_only_control | 3 | 0.5 | 7105 | -9.11502e-06 | 0.000410957 | -0.000420072 | -0.000473172 | 5.30998e-05 | False | True | True | risk_breached_proxy | False | False | -0.02218 | False | False |
| F04_l5_imbalance_h2_q50 | F04_l5_imbalance | depth_imbalance | zero_latency_spread_only_control | 2 | 0.5 | 7212 | -1.01742e-05 | 0.000410525 | -0.000420699 | -0.000473172 | 5.24725e-05 | False | True | True | risk_breached_proxy | False | False | -0.0247833 | False | False |
| F02_mlofi_qty_event_h5_q70 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 5 | 0.7 | 5143 | -9.10184e-05 | 0.000331585 | -0.000422604 | -0.000473172 | 5.05683e-05 | False | True | True | risk_not_breached_proxy | False | True | -0.274495 | False | False |
| F07_l1_mean_reversion_h5_q50 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 5 | 0.5 | 7992 | -7.2391e-05 | 0.000351825 | -0.000424216 | -0.000473172 | 4.89558e-05 | False | True | True | risk_breached_proxy | False | False | -0.205759 | False | False |
| F07_l1_mean_reversion_h2_q50 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 2 | 0.5 | 8340 | -7.48634e-05 | 0.000351812 | -0.000426675 | -0.000473172 | 4.6497e-05 | False | True | True | risk_breached_proxy | False | False | -0.212794 | False | False |
| F07_l1_mean_reversion_h3_q50 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 3 | 0.5 | 8227 | -8.55192e-05 | 0.000351771 | -0.000437291 | -0.000473172 | 3.58813e-05 | False | True | True | risk_breached_proxy | False | False | -0.24311 | False | False |
| F07_l1_mean_reversion_h5_q70 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 5 | 0.7 | 4170 | 0.000205532 | 0.000645084 | -0.000439552 | -0.000473172 | 3.36198e-05 | False | True | True | risk_breached_proxy | False | False | 0.318613 | False | False |
| F02_mlofi_qty_event_h2_q70 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 2 | 0.7 | 5387 | -0.00010784 | 0.00033197 | -0.00043981 | -0.000473172 | 3.33616e-05 | False | True | True | risk_not_breached_proxy | False | True | -0.32485 | False | False |
| F04_l5_imbalance_h1_q50 | F04_l5_imbalance | depth_imbalance | zero_latency_spread_only_control | 1 | 0.5 | 7304 | -2.96452e-05 | 0.000410979 | -0.000440624 | -0.000473172 | 3.25476e-05 | False | True | True | risk_not_breached_proxy | False | True | -0.0721331 | False | False |
| F02_mlofi_qty_event_h3_q70 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 3 | 0.7 | 5292 | -0.000139019 | 0.000331598 | -0.000470617 | -0.000473172 | 2.55475e-06 | False | True | True | risk_not_breached_proxy | False | True | -0.419241 | False | False |
| F04_l5_imbalance_h5_q50 | F04_l5_imbalance | depth_imbalance | zero_latency_spread_only_control | 5 | 0.5 | 6904 | -6.36462e-05 | 0.000410894 | -0.00047454 | -0.000473172 | -1.36843e-06 | False | False | True | risk_breached_proxy | False | False | -0.154897 | False | False |
| F02_mlofi_qty_event_h1_q70 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 1 | 0.7 | 5474 | -0.000157533 | 0.000331695 | -0.000489228 | -0.000473172 | -1.60566e-05 | False | False | True | risk_not_breached_proxy | False | True | -0.474934 | False | False |
| F01_momentum_3_event_h5_q50 | F01_momentum_3_event | short_horizon_momentum | zero_latency_spread_only_control | 5 | 0.5 | 6802 | -0.000296625 | 0.000204955 | -0.000501581 | -0.000473172 | -2.84088e-05 | False | False | True | risk_breached_proxy | False | False | -1.44727 | False | False |
| F07_l1_mean_reversion_h3_q70 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 3 | 0.7 | 4293 | 0.000133218 | 0.000644975 | -0.000511758 | -0.000473172 | -3.85858e-05 | False | False | True | risk_not_breached_proxy | False | True | 0.206547 | False | False |
| F01_momentum_3_event_h3_q50 | F01_momentum_3_event | short_horizon_momentum | zero_latency_spread_only_control | 3 | 0.5 | 7054 | -0.000329092 | 0.000204291 | -0.000533383 | -0.000473172 | -6.0211e-05 | False | False | True | risk_breached_proxy | False | False | -1.6109 | False | False |
| F06_l5_mean_reversion_h5_q70 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 5 | 0.7 | 4125 | 9.26827e-05 | 0.000651231 | -0.000558548 | -0.000473172 | -8.53766e-05 | False | False | True | risk_breached_proxy | False | False | 0.142319 | False | False |
| F07_l1_mean_reversion_h2_q70 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 2 | 0.7 | 4356 | 8.48955e-05 | 0.000644502 | -0.000559606 | -0.000473172 | -8.64343e-05 | False | False | True | risk_not_breached_proxy | False | True | 0.131723 | False | False |
| F02_mlofi_qty_event_h5_q85 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 5 | 0.85 | 2357 | -0.000153447 | 0.000411378 | -0.000564825 | -0.000473172 | -9.16533e-05 | False | False | True | risk_not_breached_proxy | False | True | -0.373007 | False | False |
| F01_momentum_3_event_h2_q50 | F01_momentum_3_event | short_horizon_momentum | zero_latency_spread_only_control | 2 | 0.5 | 7174 | -0.000373672 | 0.000204066 | -0.000577738 | -0.000473172 | -0.000104566 | False | False | True | risk_breached_proxy | False | False | -1.83113 | False | False |
| F01_momentum_3_event_h1_q50 | F01_momentum_3_event | short_horizon_momentum | zero_latency_spread_only_control | 1 | 0.5 | 7303 | -0.000375777 | 0.000203695 | -0.000579472 | -0.000473172 | -0.0001063 | False | False | True | risk_breached_proxy | False | False | -1.8448 | False | False |
| F05_microprice_dev_h3_q70 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 3 | 0.7 | 4248 | 7.4265e-05 | 0.000657674 | -0.000583409 | -0.000473172 | -0.000110237 | False | False | True | risk_breached_proxy | False | False | 0.112921 | False | False |
| F01_momentum_3_event_h5_q70 | F01_momentum_3_event | short_horizon_momentum | zero_latency_spread_only_control | 5 | 0.7 | 4088 | -0.000398066 | 0.000185913 | -0.000583978 | -0.000473172 | -0.000110806 | False | False | True | risk_breached_proxy | False | False | -2.14114 | False | False |
| F02_mlofi_qty_event_h2_q85 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 2 | 0.85 | 2462 | -0.000174957 | 0.000411447 | -0.000586404 | -0.000473172 | -0.000113232 | False | False | True | risk_not_breached_proxy | False | True | -0.425225 | False | False |

## Rejection Ledger

| candidate_id | feature_id | feature_family | execution_profile | horizon_events | rejection_reasons | realistic_cost_clearing_edge | phase27_scope |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F03_l1_imbalance_h3_q50 | F03_l1_imbalance | top_of_book_imbalance | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h2_q50 | F03_l1_imbalance | top_of_book_imbalance | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h5_q50 | F03_l1_imbalance | top_of_book_imbalance | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h2_q50 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h1_q50 | F03_l1_imbalance | top_of_book_imbalance | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F05_microprice_dev_h3_q50 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F05_microprice_dev_h5_q50 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h1_q50 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h5_q50 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F05_microprice_dev_h2_q50 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h3_q50 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F06_l5_mean_reversion_h5_q50 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F06_l5_mean_reversion_h1_q50 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F07_l1_mean_reversion_h1_q50 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F05_microprice_dev_h1_q50 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F06_l5_mean_reversion_h2_q50 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F06_l5_mean_reversion_h3_q50 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h3_q50 | F04_l5_imbalance | depth_imbalance | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h2_q50 | F04_l5_imbalance | depth_imbalance | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h5_q70 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F07_l1_mean_reversion_h5_q50 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F07_l1_mean_reversion_h2_q50 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F07_l1_mean_reversion_h3_q50 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F07_l1_mean_reversion_h5_q70 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h2_q70 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h1_q50 | F04_l5_imbalance | depth_imbalance | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h3_q70 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h5_q50 | F04_l5_imbalance | depth_imbalance | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h1_q70 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h5_q50 | F01_momentum_3_event | short_horizon_momentum | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F07_l1_mean_reversion_h3_q70 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h3_q50 | F01_momentum_3_event | short_horizon_momentum | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F06_l5_mean_reversion_h5_q70 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F07_l1_mean_reversion_h2_q70 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h5_q85 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h2_q50 | F01_momentum_3_event | short_horizon_momentum | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h1_q50 | F01_momentum_3_event | short_horizon_momentum | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F05_microprice_dev_h3_q70 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h5_q70 | F01_momentum_3_event | short_horizon_momentum | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h2_q85 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F07_l1_mean_reversion_h1_q70 | F07_l1_mean_reversion | top_of_book_mean_reversion | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F05_microprice_dev_h2_q70 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h1_q85 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F06_l5_mean_reversion_h3_q70 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F05_microprice_dev_h5_q70 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F06_l5_mean_reversion_h2_q70 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h3_q85 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F05_microprice_dev_h1_q70 | F05_microprice_dev | microprice_pressure | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F06_l5_mean_reversion_h1_q70 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h1_q70 | F04_l5_imbalance | depth_imbalance | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F06_l5_mean_reversion_h5_q85 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h2_q70 | F04_l5_imbalance | depth_imbalance | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h1_q70 | F03_l1_imbalance | top_of_book_imbalance | zero_latency_spread_only_control | 1 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h3_q70 | F04_l5_imbalance | depth_imbalance | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h3_q70 | F01_momentum_3_event | short_horizon_momentum | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h5_q95 | F04_l5_imbalance | depth_imbalance | zero_latency_spread_only_control | 5 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F06_l5_mean_reversion_h3_q85 | F06_l5_mean_reversion | depth_mean_reversion | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h2_q95 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h2_q70 | F01_momentum_3_event | short_horizon_momentum | zero_latency_spread_only_control | 2 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy;proxy_risk_breached_or_missing | False | feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h3_q95 | F02_mlofi_qty_event | order_flow_imbalance | zero_latency_spread_only_control | 3 | zero_latency_control_not_retail_edge;net_return_not_positive_after_costs;does_not_beat_best_baseline_proxy | False | feature_edge_cost_hurdle_scan_not_acceptance |

## Candidate Catalog

| candidate_id | feature_id | feature_family | feature_column | polarity | horizon_events | threshold_quantile | threshold_value | candidate_scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F01_momentum_3_event_h1_q50 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 1 | 0.5 | 0.00184354 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h1_q70 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 1 | 0.7 | 0.00306118 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h1_q85 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 1 | 0.85 | 0.00447612 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h1_q95 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 1 | 0.95 | 0.00665901 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h2_q50 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 2 | 0.5 | 0.00184354 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h2_q70 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 2 | 0.7 | 0.00306118 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h2_q85 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 2 | 0.85 | 0.00447612 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h2_q95 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 2 | 0.95 | 0.00665901 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h3_q50 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 3 | 0.5 | 0.00184354 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h3_q70 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 3 | 0.7 | 0.00306118 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h3_q85 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 3 | 0.85 | 0.00447612 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h3_q95 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 3 | 0.95 | 0.00665901 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h5_q50 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 5 | 0.5 | 0.00184354 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h5_q70 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 5 | 0.7 | 0.00306118 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h5_q85 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 5 | 0.85 | 0.00447612 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F01_momentum_3_event_h5_q95 | F01_momentum_3_event | short_horizon_momentum | momentum_3_event | 1 | 5 | 0.95 | 0.00665901 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h1_q50 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 1 | 0.5 | 1 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h1_q70 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 1 | 0.7 | 2 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h1_q85 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 1 | 0.85 | 4 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h1_q95 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 1 | 0.95 | 6 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h2_q50 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 2 | 0.5 | 1 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h2_q70 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 2 | 0.7 | 2 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h2_q85 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 2 | 0.85 | 4 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h2_q95 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 2 | 0.95 | 6 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h3_q50 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 3 | 0.5 | 1 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h3_q70 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 3 | 0.7 | 2 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h3_q85 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 3 | 0.85 | 4 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h3_q95 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 3 | 0.95 | 6 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h5_q50 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 5 | 0.5 | 1 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h5_q70 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 5 | 0.7 | 2 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h5_q85 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 5 | 0.85 | 4 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F02_mlofi_qty_event_h5_q95 | F02_mlofi_qty_event | order_flow_imbalance | mlofi_qty_event | 1 | 5 | 0.95 | 6 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h1_q50 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 1 | 0.5 | 0.111111 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h1_q70 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 1 | 0.7 | 0.216216 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h1_q85 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 1 | 0.85 | 0.324251 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h1_q95 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 1 | 0.95 | 0.331522 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h2_q50 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 2 | 0.5 | 0.111111 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h2_q70 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 2 | 0.7 | 0.216216 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h2_q85 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 2 | 0.85 | 0.324251 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h2_q95 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 2 | 0.95 | 0.331522 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h3_q50 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 3 | 0.5 | 0.111111 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h3_q70 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 3 | 0.7 | 0.216216 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h3_q85 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 3 | 0.85 | 0.324251 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h3_q95 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 3 | 0.95 | 0.331522 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h5_q50 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 5 | 0.5 | 0.111111 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h5_q70 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 5 | 0.7 | 0.216216 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h5_q85 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 5 | 0.85 | 0.324251 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F03_l1_imbalance_h5_q95 | F03_l1_imbalance | top_of_book_imbalance | l1_imbalance | 1 | 5 | 0.95 | 0.331522 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h1_q50 | F04_l5_imbalance | depth_imbalance | l5_imbalance | 1 | 1 | 0.5 | 0.0804741 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h1_q70 | F04_l5_imbalance | depth_imbalance | l5_imbalance | 1 | 1 | 0.7 | 0.214022 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h1_q85 | F04_l5_imbalance | depth_imbalance | l5_imbalance | 1 | 1 | 0.85 | 0.32443 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h1_q95 | F04_l5_imbalance | depth_imbalance | l5_imbalance | 1 | 1 | 0.95 | 0.331242 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h2_q50 | F04_l5_imbalance | depth_imbalance | l5_imbalance | 1 | 2 | 0.5 | 0.0804741 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h2_q70 | F04_l5_imbalance | depth_imbalance | l5_imbalance | 1 | 2 | 0.7 | 0.214022 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h2_q85 | F04_l5_imbalance | depth_imbalance | l5_imbalance | 1 | 2 | 0.85 | 0.32443 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h2_q95 | F04_l5_imbalance | depth_imbalance | l5_imbalance | 1 | 2 | 0.95 | 0.331242 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h3_q50 | F04_l5_imbalance | depth_imbalance | l5_imbalance | 1 | 3 | 0.5 | 0.0804741 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h3_q70 | F04_l5_imbalance | depth_imbalance | l5_imbalance | 1 | 3 | 0.7 | 0.214022 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h3_q85 | F04_l5_imbalance | depth_imbalance | l5_imbalance | 1 | 3 | 0.85 | 0.32443 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |
| F04_l5_imbalance_h3_q95 | F04_l5_imbalance | depth_imbalance | l5_imbalance | 1 | 3 | 0.95 | 0.331242 | phase27_feature_edge_cost_hurdle_scan_not_acceptance |

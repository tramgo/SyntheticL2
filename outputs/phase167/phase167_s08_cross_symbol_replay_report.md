# Phase167 S08 Cross-symbol Lead-lag Replay

Generated UTC: 2026-07-23T13:16:40.928494+00:00

Phase167 runs one precommitted S08 cross-symbol lead-lag branch from the local Phase166 cache.
The replay models feed bucket, feature update, signal, latency, order arrival, fill proxy, Zerodha/internal costs, and P&L/risk update.
This is synthetic-only evidence. Broker/paper/live acceptance and deployable profitability claims remain closed.

Full trade-level ledger: `outputs/phase167/phase167_s08_cross_symbol_trade_ledger.parquet`

## acceptance

| metric | value | description |
| --- | --- | --- |
| phase167_source_cache_ready | 1 | Inherited Phase166 S08 cache-ready flag |
| phase167_cache_files_scanned | 12 | Phase166 monthly cache files scanned |
| phase167_strategy_id | P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | Exactly one precommitted S08 alpha branch |
| phase167_score_threshold | 0.42 | Fixed absolute score threshold set before replay |
| phase167_execution_profile_rows | 3 | Execution profile variants replayed side by side |
| phase167_trade_rows | 817814 | Full trade-level rows written to parquet |
| phase167_positive_after_cost_profile_rows | 0 | Profile rows positive after all costs |
| phase167_candidate_profile_rows | 0 | Rows passing positive, coverage, stability and precision gates |
| phase167_best_execution_profile | zero_latency_spread_only_control | Best profile by annual net P&L |
| phase167_best_annual_net_pnl_inr | -4.1439e+06 | Best annual after-cost net P&L |
| phase167_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha equity intraday NSE charge formula reused |
| phase167_strategy_promotion_allowed | 0 | Synthetic-only promotion gate; paper/live remains closed regardless |
| phase167_paper_or_live_acceptance_allowed | 0 | Broker/paper/live acceptance remains closed |
| phase167_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from synthetic-only replay |
| phase167_azure_read_policy | forbidden_for_analysis_download_first_then_local | No direct Python Azure scanning |
| phase167_next_best_action | close_s08_current_form_and_update_blocklist_candidate | Recommended next milestone |
| phase167_elapsed_seconds | 198.827 | Runner elapsed seconds |

## profile_summary

| strategy_id | source_strategy_id | feature_family | feature_status | execution_profile | trades | symbols | months | trade_dates | sum_gross_return | sum_cost_return | sum_net_return | mean_gross_return | mean_cost_return | mean_net_return | gross_pnl_inr | cost_pnl_drag_inr | annual_net_pnl_inr | worst_trade_pnl_inr | precision_cost_clear | mean_spread_bps | total_latency_buckets | fixed_slippage_ticks | internal_impact_bps | zerodha_charge_bps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | S08 | cross_symbol_lead_lag | precommitted_phase167_single_s08_branch | zero_latency_spread_only_control | 273062 | 5 | 12 | 252 | -0.00426301 | 41.4347 | -41.439 | -1.56119e-08 | 0.000151741 | -0.000151757 | -426.301 | 4.14347e+06 | -4.1439e+06 | -314.325 | 1.83109e-05 | 3.03482 | 0 | 0 | 0 | 0 |
| P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | S08 | cross_symbol_lead_lag | precommitted_phase167_single_s08_branch | retail_marketable_default | 272592 | 5 | 12 | 252 | 0.000954917 | 282.512 | -282.511 | 3.5031e-09 | 0.00103639 | -0.00103639 | 95.4917 | 2.82512e+07 | -2.82511e+07 | -402.857 | 1.10055e-05 | 3.03451 | 2 | 1 | 0.5 | 8.26812 |
| P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | S08 | cross_symbol_lead_lag | precommitted_phase167_single_s08_branch | stressed_retail | 272160 | 5 | 12 | 252 | 0.000531413 | 325.026 | -325.025 | 1.95258e-09 | 0.00119425 | -0.00119424 | 53.1413 | 3.25026e+07 | -3.25025e+07 | -418.667 | 7.34862e-06 | 3.03447 | 4 | 2 | 2 | 8.26812 |

## split_summary

| execution_profile | split | trades | symbols | months | gross_pnl_inr | cost_pnl_drag_inr | net_pnl_inr | precision_cost_clear |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| retail_marketable_default | test | 132037 | 5 | 6 | -353.056 | 1.36911e+07 | -1.36915e+07 | 7.57363e-06 |
| retail_marketable_default | train | 140555 | 4 | 6 | 448.548 | 1.45601e+07 | -1.45596e+07 | 1.42293e-05 |
| stressed_retail | test | 131822 | 5 | 6 | -803.09 | 1.57497e+07 | -1.57505e+07 | 0 |
| stressed_retail | train | 140338 | 4 | 6 | 856.232 | 1.67529e+07 | -1.6752e+07 | 1.42513e-05 |
| zero_latency_spread_only_control | test | 132263 | 5 | 6 | -264.895 | 2.01388e+06 | -2.01414e+06 | 1.51214e-05 |
| zero_latency_spread_only_control | train | 140799 | 4 | 6 | -161.405 | 2.12959e+06 | -2.12975e+06 | 2.1307e-05 |

## monthly_summary

| execution_profile | split | trade_month | trades | symbols | gross_pnl_inr | cost_pnl_drag_inr | net_pnl_inr | precision_cost_clear |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| retail_marketable_default | test | 2026-07 | 25941 | 4 | -32.1692 | 2.67052e+06 | -2.67056e+06 | 0 |
| retail_marketable_default | test | 2026-08 | 21796 | 4 | -141.105 | 2.29369e+06 | -2.29383e+06 | 0 |
| retail_marketable_default | test | 2026-09 | 22754 | 5 | 259.868 | 2.39134e+06 | -2.39108e+06 | 4.39483e-05 |
| retail_marketable_default | test | 2026-10 | 24839 | 4 | -187.378 | 2.53348e+06 | -2.53367e+06 | 0 |
| retail_marketable_default | test | 2026-11 | 22513 | 4 | -252.273 | 2.33278e+06 | -2.33303e+06 | 0 |
| retail_marketable_default | test | 2026-12 | 14194 | 4 | 0 | 1.4693e+06 | -1.4693e+06 | 0 |
| retail_marketable_default | train | 2026-01 | 24517 | 4 | 0 | 2.52106e+06 | -2.52106e+06 | 0 |
| retail_marketable_default | train | 2026-02 | 21356 | 4 | 19.5642 | 2.22359e+06 | -2.22357e+06 | 0 |
| retail_marketable_default | train | 2026-03 | 23456 | 4 | 206.188 | 2.41212e+06 | -2.41191e+06 | 4.2633e-05 |
| retail_marketable_default | train | 2026-04 | 24173 | 4 | -259.666 | 2.50598e+06 | -2.50624e+06 | 0 |
| retail_marketable_default | train | 2026-05 | 24195 | 4 | -18.8494 | 2.51128e+06 | -2.5113e+06 | 0 |
| retail_marketable_default | train | 2026-06 | 22858 | 4 | 501.312 | 2.38608e+06 | -2.38558e+06 | 4.37484e-05 |
| stressed_retail | test | 2026-07 | 25904 | 4 | 4.21484 | 3.0756e+06 | -3.0756e+06 | 0 |
| stressed_retail | test | 2026-08 | 21763 | 4 | -80.4127 | 2.63382e+06 | -2.6339e+06 | 0 |
| stressed_retail | test | 2026-09 | 22714 | 5 | -162.485 | 2.74576e+06 | -2.74592e+06 | 0 |
| stressed_retail | test | 2026-10 | 24794 | 4 | -233.751 | 2.92018e+06 | -2.92041e+06 | 0 |
| stressed_retail | test | 2026-11 | 22478 | 4 | -330.656 | 2.68401e+06 | -2.68434e+06 | 0 |
| stressed_retail | test | 2026-12 | 14169 | 4 | 0 | 1.69035e+06 | -1.69035e+06 | 0 |
| stressed_retail | train | 2026-01 | 24483 | 4 | 74.3558 | 2.90402e+06 | -2.90394e+06 | 0 |
| stressed_retail | train | 2026-02 | 21327 | 4 | 53.9809 | 2.55728e+06 | -2.55723e+06 | 0 |
| stressed_retail | train | 2026-03 | 23418 | 4 | 276.801 | 2.77782e+06 | -2.77754e+06 | 4.27022e-05 |
| stressed_retail | train | 2026-04 | 24134 | 4 | -298.164 | 2.88285e+06 | -2.88315e+06 | 0 |
| stressed_retail | train | 2026-05 | 24156 | 4 | 41.9527 | 2.88853e+06 | -2.88848e+06 | 0 |
| stressed_retail | train | 2026-06 | 22820 | 4 | 707.306 | 2.74235e+06 | -2.74165e+06 | 4.38212e-05 |
| zero_latency_spread_only_control | test | 2026-07 | 25978 | 4 | -75.6623 | 376199 | -376275 | 3.84941e-05 |
| zero_latency_spread_only_control | test | 2026-08 | 21832 | 4 | -227.82 | 366066 | -366294 | 0 |
| zero_latency_spread_only_control | test | 2026-09 | 22798 | 5 | 87.697 | 379078 | -378990 | 4.38635e-05 |
| zero_latency_spread_only_control | test | 2026-10 | 24880 | 4 | -49.1102 | 336702 | -336751 | 0 |
| zero_latency_spread_only_control | test | 2026-11 | 22554 | 4 | 0 | 341738 | -341738 | 0 |
| zero_latency_spread_only_control | test | 2026-12 | 14221 | 4 | 0 | 214097 | -214097 | 0 |
| zero_latency_spread_only_control | train | 2026-01 | 24557 | 4 | 34.7709 | 352728 | -352693 | 4.07216e-05 |
| zero_latency_spread_only_control | train | 2026-02 | 21396 | 4 | 0 | 334884 | -334884 | 0 |
| zero_latency_spread_only_control | train | 2026-03 | 23500 | 4 | -56.1451 | 337700 | -337756 | 0 |
| zero_latency_spread_only_control | train | 2026-04 | 24210 | 4 | -259.666 | 368128 | -368388 | 4.13052e-05 |
| zero_latency_spread_only_control | train | 2026-05 | 24234 | 4 | 119.635 | 371463 | -371343 | 4.12643e-05 |
| zero_latency_spread_only_control | train | 2026-06 | 22902 | 4 | 0 | 364691 | -364691 | 0 |

## symbol_summary

| execution_profile | split | symbol | trades | months | gross_pnl_inr | cost_pnl_drag_inr | net_pnl_inr | precision_cost_clear |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| retail_marketable_default | test | BRITANNIA | 5365 | 6 | 101.904 | 590492 | -590390 | 0.000186393 |
| retail_marketable_default | test | CIPLA | 1 | 1 | 0 | 119.876 | -119.876 | 0 |
| retail_marketable_default | test | DRREDDY | 126525 | 6 | -454.96 | 1.30858e+07 | -1.30862e+07 | 0 |
| retail_marketable_default | test | HINDUNILVR | 27 | 6 | 0 | 2736.47 | -2736.47 | 0 |
| retail_marketable_default | test | SUNPHARMA | 119 | 6 | 0 | 12006.8 | -12006.8 | 0 |
| retail_marketable_default | train | BRITANNIA | 5732 | 6 | 788.764 | 626516 | -625728 | 0.000348918 |
| retail_marketable_default | train | DRREDDY | 134653 | 6 | -340.216 | 1.39166e+07 | -1.39169e+07 | 0 |
| retail_marketable_default | train | HINDUNILVR | 44 | 6 | 0 | 4381.91 | -4381.91 | 0 |
| retail_marketable_default | train | SUNPHARMA | 126 | 6 | 0 | 12646 | -12646 | 0 |
| stressed_retail | test | BRITANNIA | 5348 | 6 | -315.047 | 669882 | -670197 | 0 |
| stressed_retail | test | CIPLA | 1 | 1 | 0 | 135.576 | -135.576 | 0 |
| stressed_retail | test | DRREDDY | 126329 | 6 | -488.044 | 1.50629e+07 | -1.50634e+07 | 0 |
| stressed_retail | test | HINDUNILVR | 26 | 6 | 0 | 3029.47 | -3029.47 | 0 |
| stressed_retail | test | SUNPHARMA | 118 | 6 | 0 | 13736.9 | -13736.9 | 0 |
| stressed_retail | train | BRITANNIA | 5711 | 6 | 1004.71 | 710964 | -709959 | 0.000350201 |
| stressed_retail | train | DRREDDY | 134457 | 6 | -148.476 | 1.60222e+07 | -1.60224e+07 | 0 |
| stressed_retail | train | HINDUNILVR | 44 | 6 | 0 | 5062.54 | -5062.54 | 0 |
| stressed_retail | train | SUNPHARMA | 126 | 6 | 0 | 14601.4 | -14601.4 | 0 |
| zero_latency_spread_only_control | test | BRITANNIA | 5391 | 6 | -283.088 | 119709 | -119993 | 0.000185494 |
| zero_latency_spread_only_control | test | CIPLA | 1 | 1 | 0 | 31.4906 | -31.4906 | 0 |
| zero_latency_spread_only_control | test | DRREDDY | 126724 | 6 | 18.1922 | 1.89225e+06 | -1.89223e+06 | 7.89117e-06 |
| zero_latency_spread_only_control | test | HINDUNILVR | 28 | 6 | 0 | 377.522 | -377.522 | 0 |
| zero_latency_spread_only_control | test | SUNPHARMA | 119 | 6 | 0 | 1510.93 | -1510.93 | 0 |
| zero_latency_spread_only_control | train | BRITANNIA | 5760 | 6 | -55.3461 | 123484 | -123540 | 0.000173611 |
| zero_latency_spread_only_control | train | DRREDDY | 134866 | 6 | -106.059 | 2.00403e+06 | -2.00414e+06 | 1.48295e-05 |
| zero_latency_spread_only_control | train | HINDUNILVR | 46 | 6 | 0 | 536.131 | -536.131 | 0 |
| zero_latency_spread_only_control | train | SUNPHARMA | 127 | 6 | 0 | 1543.22 | -1543.22 | 0 |

## gate_evaluation

| strategy_id | execution_profile | train_net_pnl_inr | test_net_pnl_inr | test_trades | test_symbols | test_positive_months | test_precision_cost_clear | test_max_month_contribution_abs | test_max_symbol_contribution_abs | train_positive_after_costs | test_positive_after_costs | coverage_pass | stability_pass | precision_pass | phase167_profile_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | zero_latency_spread_only_control | -2.12975e+06 | -2.01414e+06 | 132263 | 5 | 0 | 1.51214e-05 | 0.188164 | 0.939472 | False | False | False | False | False | False |
| P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | retail_marketable_default | -1.45596e+07 | -1.36915e+07 | 132037 | 5 | 0 | 7.57363e-06 | 0.195052 | 0.955793 | False | False | False | False | False | False |
| P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | stressed_retail | -1.6752e+07 | -1.57505e+07 | 131822 | 5 | 0 | 0 | 0.19527 | 0.956376 | False | False | False | False | False | False |

## execution_profile_catalog

| execution_profile | decision_latency_buckets | broker_latency_buckets | total_latency_buckets | fixed_slippage_ticks | internal_impact_bps | zerodha_charge_bps | apply_zerodha_equity_intraday_charges | order_notional_inr | cancel_on_stale_or_disconnect | fill_model | fill_ratio | description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| zero_latency_spread_only_control | 0 | 0 | 0 | 0 | 0 | 0 | False | 100000 | False | marketable_full_fill_proxy | 1 | Leakage/control profile with zero latency and spread/slippage controls only. Not deployable and excludes statutory/brokerage charges. |
| retail_marketable_default | 1 | 1 | 2 | 1 | 0.5 | 8.26812 | True | 100000 | True | marketable_full_fill_proxy | 1 | Default marketable retail proxy with next-event latency, Zerodha equity-intraday charge estimate, and internal impact/slippage assumptions. |
| stressed_retail | 2 | 2 | 4 | 2 | 2 | 8.26812 | True | 100000 | True | marketable_full_fill_proxy | 1 | Stress proxy with longer event latency, Zerodha equity-intraday charge estimate, and higher internal impact/slippage assumptions. |

## zerodha_charge_component_catalog

| component | formula | side | rate | source_url | rounding_or_cap |
| --- | --- | --- | --- | --- | --- |
| brokerage | min(0.03% of executed order value, Rs 20) per buy/sell executed order | buy_and_sell | 0.0003 | https://zerodha.com/charges/ | Rs 20 cap per executed order |
| stt | 0.025% on equity intraday sell side; rounded to nearest rupee | sell | 0.00025 | https://support.zerodha.com/category/account-opening/resident-individual/ri-charges/articles/how-is-the-securities-transaction-tax-stt-calculated | nearest rupee |
| nse_transaction_charge | 0.00307% of buy plus sell turnover | buy_and_sell | 3.07e-05 | https://zerodha.com/charges/ | unrounded analytical estimate |
| sebi_charge | Rs 10 per crore of buy plus sell turnover | buy_and_sell | 1e-06 | https://zerodha.com/charges/ | unrounded analytical estimate |
| stamp_duty | 0.003% on buy side | buy | 3e-05 | https://zerodha.com/charges/ | unrounded analytical estimate |
| gst | 18% of brokerage plus SEBI charges plus transaction charges | buy_and_sell | 0.18 | https://zerodha.com/charges/ | unrounded analytical estimate |

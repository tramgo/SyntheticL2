# Phase 26 Strategy Salvage Scan

Generated UTC: 2026-07-14T18:01:10.732277+00:00

This milestone answers the immediate post-Phase-25 question: do simple threshold, spread and liquidity filters salvage any event-order strategy after realistic costs?
It is an execution diagnostic and rejection/salvage screen, not a promotion or acceptance result.

## Overall Summary

| metric | value | description |
| --- | --- | --- |
| phase26_variants_registered | 120 | Strategy parameter/filter variants registered |
| phase26_variant_profile_rows | 282 | Variant/profile replay summary rows |
| phase26_total_replay_trades | 542406 | Total trades across all variant/profile replays |
| phase26_positive_after_cost_rows | 17 | Variant/profile rows with positive mean net return after costs |
| phase26_realistic_positive_after_cost_rows | 0 | Retail/stressed rows with positive mean net return after Zerodha-style costs |
| phase26_zero_latency_positive_control_rows | 17 | Frictionless control rows that are positive but not retail survivors |
| phase26_beats_best_baseline_rows | 204 | Variant/profile rows beating best baseline proxy |
| phase26_salvage_candidate_rows | 0 | Rows passing positive net, baseline, trade-count and proxy-risk filters |
| phase26_rejected_rows | 282 | Variant/profile rows rejected by at least one diagnostic |
| phase26_acceptance_ready | 0 | Parameter scan is execution diagnostic evidence, not acceptance evidence |

## Top Candidate Rows

| variant_id | parent_strategy_id | execution_profile | trades | mean_gross_return | mean_cost_return | mean_net_return | total_net_pnl_inr | best_baseline_mean_net_return | net_return_lift_vs_best_baseline | positive_after_costs | beats_best_baseline_proxy | enough_trades_for_candidate | risk_status | risk_not_breached_proxy | realistic_charged_profile | salvage_candidate_proxy | zero_latency_positive_control |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S07_q70_sp080_liqmed | S07 | zero_latency_spread_only_control | 498 | 0.000201846 | 5.55458e-05 | 0.0001463 | 7285.74 | -0.000473172 | 0.000619472 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S07_q70_sp100_liqmed | S07 | zero_latency_spread_only_control | 498 | 0.000201846 | 5.55458e-05 | 0.0001463 | 7285.74 | -0.000473172 | 0.000619472 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S07_q70_sp050_liqmed | S07 | zero_latency_spread_only_control | 493 | 0.000193396 | 5.50042e-05 | 0.000138392 | 6822.7 | -0.000473172 | 0.000611563 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S07_q70_sp050_liqall | S07 | zero_latency_spread_only_control | 898 | 0.000179632 | 5.49864e-05 | 0.000124645 | 11193.2 | -0.000473172 | 0.000597817 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S07_q50_sp050_liqall | S07 | zero_latency_spread_only_control | 2682 | 0.000138431 | 4.99781e-05 | 8.84533e-05 | 23723.2 | -0.000473172 | 0.000561625 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S09_q50_sp080_liqmed | S09 | zero_latency_spread_only_control | 1810 | 0.000138463 | 5.50725e-05 | 8.33906e-05 | 15093.7 | -0.000473172 | 0.000556563 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S09_q50_sp100_liqmed | S09 | zero_latency_spread_only_control | 1810 | 0.000138463 | 5.50725e-05 | 8.33906e-05 | 15093.7 | -0.000473172 | 0.000556563 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S09_q50_sp050_liqmed | S09 | zero_latency_spread_only_control | 1795 | 0.000130296 | 5.46658e-05 | 7.56298e-05 | 13575.6 | -0.000473172 | 0.000548802 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S07_q50_sp080_liqall | S07 | zero_latency_spread_only_control | 3243 | 0.000123568 | 5.91079e-05 | 6.44605e-05 | 20904.5 | -0.000473172 | 0.000537632 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S07_q50_sp050_liqmed | S07 | zero_latency_spread_only_control | 1923 | 0.000107979 | 4.80192e-05 | 5.99603e-05 | 11530.4 | -0.000473172 | 0.000533132 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S07_q50_sp080_liqmed | S07 | zero_latency_spread_only_control | 1943 | 0.000102969 | 4.85615e-05 | 5.44074e-05 | 10571.4 | -0.000473172 | 0.000527579 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S07_q50_sp100_liqmed | S07 | zero_latency_spread_only_control | 1943 | 0.000102969 | 4.85615e-05 | 5.44074e-05 | 10571.4 | -0.000473172 | 0.000527579 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S07_q70_sp080_liqall | S07 | zero_latency_spread_only_control | 1057 | 0.000101242 | 6.33304e-05 | 3.79112e-05 | 4007.21 | -0.000473172 | 0.000511083 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S05_q70_sp080_liqall | S05 | zero_latency_spread_only_control | 1464 | 0.000113489 | 8.0708e-05 | 3.27809e-05 | 4799.13 | -0.000473172 | 0.000505953 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S09_q50_sp080_liqall | S09 | zero_latency_spread_only_control | 5546 | 6.89742e-05 | 3.98215e-05 | 2.91527e-05 | 16168.1 | -0.000473172 | 0.000502325 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S05_q50_sp080_liqall | S05 | zero_latency_spread_only_control | 4393 | 6.33476e-05 | 5.47632e-05 | 8.58431e-06 | 3771.09 | -0.000473172 | 0.000481756 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S09_q70_sp050_liqmed | S09 | zero_latency_spread_only_control | 804 | 5.70292e-05 | 5.4574e-05 | 2.45519e-06 | 197.397 | -0.000473172 | 0.000475627 | True | True | True | risk_not_breached_proxy | True | False | False | True |
| S09_q70_sp080_liqmed | S09 | zero_latency_spread_only_control | 809 | 5.02797e-05 | 5.491e-05 | -4.6303e-06 | -374.591 | -0.000473172 | 0.000468542 | False | True | True | risk_not_breached_proxy | True | False | False | False |
| S09_q70_sp100_liqmed | S09 | zero_latency_spread_only_control | 809 | 5.02797e-05 | 5.491e-05 | -4.6303e-06 | -374.591 | -0.000473172 | 0.000468542 | False | True | True | risk_not_breached_proxy | True | False | False | False |
| S05_q50_sp050_liqall | S05 | zero_latency_spread_only_control | 3038 | 2.32978e-05 | 4.1592e-05 | -1.82942e-05 | -5557.78 | -0.000473172 | 0.000454878 | False | True | True | risk_not_breached_proxy | True | False | False | False |
| S05_q50_sp050_liqmed | S05 | zero_latency_spread_only_control | 3038 | 2.32978e-05 | 4.1592e-05 | -1.82942e-05 | -5557.78 | -0.000473172 | 0.000454878 | False | True | True | risk_not_breached_proxy | True | False | False | False |
| S09_q50_sp050_liqall | S09 | zero_latency_spread_only_control | 2554 | 2.75067e-05 | 5.47476e-05 | -2.72409e-05 | -6957.33 | -0.000473172 | 0.000445931 | False | True | True | risk_not_breached_proxy | True | False | False | False |
| S05_q50_sp080_liqmed | S05 | zero_latency_spread_only_control | 3425 | 1.81104e-05 | 4.76701e-05 | -2.95597e-05 | -10124.2 | -0.000473172 | 0.000443612 | False | True | True | risk_not_breached_proxy | True | False | False | False |
| S05_q50_sp100_liqmed | S05 | zero_latency_spread_only_control | 3425 | 1.81104e-05 | 4.76701e-05 | -2.95597e-05 | -10124.2 | -0.000473172 | 0.000443612 | False | True | True | risk_not_breached_proxy | True | False | False | False |
| S09_q70_sp050_liqall | S09 | zero_latency_spread_only_control | 1315 | -2.11905e-05 | 5.47158e-05 | -7.59063e-05 | -9981.68 | -0.000473172 | 0.000397266 | False | True | True | risk_not_breached_proxy | True | False | False | False |

## Rejection Ledger

| variant_id | parent_strategy_id | execution_profile | rejection_reasons | salvage_candidate_proxy | phase26_scope |
| --- | --- | --- | --- | --- | --- |
| S07_q70_sp080_liqmed | S07 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S07_q70_sp100_liqmed | S07 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S07_q70_sp050_liqmed | S07 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S07_q70_sp050_liqall | S07 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S07_q50_sp050_liqall | S07 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S09_q50_sp080_liqmed | S09 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S09_q50_sp100_liqmed | S09 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S09_q50_sp050_liqmed | S09 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S07_q50_sp080_liqall | S07 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S07_q50_sp050_liqmed | S07 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S07_q50_sp080_liqmed | S07 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S07_q50_sp100_liqmed | S07 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S07_q70_sp080_liqall | S07 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S05_q70_sp080_liqall | S05 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S09_q50_sp080_liqall | S09 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S05_q50_sp080_liqall | S05 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S09_q70_sp050_liqmed | S09 | zero_latency_spread_only_control | zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S09_q70_sp080_liqmed | S09 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S09_q70_sp100_liqmed | S09 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S05_q50_sp050_liqall | S05 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S05_q50_sp050_liqmed | S05 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S09_q50_sp050_liqall | S09 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S05_q50_sp080_liqmed | S05 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S05_q50_sp100_liqmed | S05 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S09_q70_sp050_liqall | S09 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S05_q70_sp050_liqall | S05 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S05_q70_sp050_liqmed | S05 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S09_q70_sp080_liqall | S09 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q50_sp080_liqall | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q50_sp050_liqall | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S05_q85_sp080_liqall | S05 | stressed_retail | net_return_not_positive_after_costs;insufficient_trade_count | False | parameter_salvage_scan_not_acceptance |
| S05_q95_sp080_liqall | S05 | stressed_retail | net_return_not_positive_after_costs;insufficient_trade_count | False | parameter_salvage_scan_not_acceptance |
| S09_q85_sp080_liqall | S09 | stressed_retail | net_return_not_positive_after_costs;insufficient_trade_count | False | parameter_salvage_scan_not_acceptance |
| S09_q95_sp080_liqall | S09 | stressed_retail | net_return_not_positive_after_costs;insufficient_trade_count | False | parameter_salvage_scan_not_acceptance |
| S02_q50_sp050_liqmed | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q50_sp080_liqmed | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q50_sp100_liqmed | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S05_q70_sp080_liqmed | S05 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S05_q70_sp100_liqmed | S05 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q70_sp050_liqall | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q70_sp050_liqmed | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q70_sp080_liqmed | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q70_sp100_liqmed | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q70_sp080_liqall | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S01_q70_sp050_liqmed | S01 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q95_sp050_liqall | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q95_sp050_liqmed | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S01_q70_sp050_liqall | S01 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q95_sp080_liqmed | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |
| S02_q95_sp100_liqmed | S02 | zero_latency_spread_only_control | net_return_not_positive_after_costs;zero_latency_control_not_retail_survivor | False | parameter_salvage_scan_not_acceptance |

## Variant Catalog

| variant_id | parent_strategy_id | threshold_quantile | spread_limit_quantile | spread_tick_limit | liquidity_filter | min_liquidity_score | variant_scope |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01_q50_sp050_liqall | S01 | 0.5 | 0.5 | 4 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q50_sp050_liqmed | S01 | 0.5 | 0.5 | 4 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q50_sp080_liqall | S01 | 0.5 | 0.8 | 10 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q50_sp080_liqmed | S01 | 0.5 | 0.8 | 10 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q50_sp100_liqall | S01 | 0.5 | 1 | 35 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q50_sp100_liqmed | S01 | 0.5 | 1 | 35 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q70_sp050_liqall | S01 | 0.7 | 0.5 | 4 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q70_sp050_liqmed | S01 | 0.7 | 0.5 | 4 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q70_sp080_liqall | S01 | 0.7 | 0.8 | 10 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q70_sp080_liqmed | S01 | 0.7 | 0.8 | 10 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q70_sp100_liqall | S01 | 0.7 | 1 | 35 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q70_sp100_liqmed | S01 | 0.7 | 1 | 35 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q85_sp050_liqall | S01 | 0.85 | 0.5 | 4 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q85_sp050_liqmed | S01 | 0.85 | 0.5 | 4 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q85_sp080_liqall | S01 | 0.85 | 0.8 | 10 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q85_sp080_liqmed | S01 | 0.85 | 0.8 | 10 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q85_sp100_liqall | S01 | 0.85 | 1 | 35 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q85_sp100_liqmed | S01 | 0.85 | 1 | 35 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q95_sp050_liqall | S01 | 0.95 | 0.5 | 4 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q95_sp050_liqmed | S01 | 0.95 | 0.5 | 4 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q95_sp080_liqall | S01 | 0.95 | 0.8 | 10 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q95_sp080_liqmed | S01 | 0.95 | 0.8 | 10 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q95_sp100_liqall | S01 | 0.95 | 1 | 35 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S01_q95_sp100_liqmed | S01 | 0.95 | 1 | 35 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q50_sp050_liqall | S02 | 0.5 | 0.5 | 4 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q50_sp050_liqmed | S02 | 0.5 | 0.5 | 4 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q50_sp080_liqall | S02 | 0.5 | 0.8 | 10 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q50_sp080_liqmed | S02 | 0.5 | 0.8 | 10 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q50_sp100_liqall | S02 | 0.5 | 1 | 35 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q50_sp100_liqmed | S02 | 0.5 | 1 | 35 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q70_sp050_liqall | S02 | 0.7 | 0.5 | 4 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q70_sp050_liqmed | S02 | 0.7 | 0.5 | 4 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q70_sp080_liqall | S02 | 0.7 | 0.8 | 10 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q70_sp080_liqmed | S02 | 0.7 | 0.8 | 10 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q70_sp100_liqall | S02 | 0.7 | 1 | 35 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q70_sp100_liqmed | S02 | 0.7 | 1 | 35 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q85_sp050_liqall | S02 | 0.85 | 0.5 | 4 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q85_sp050_liqmed | S02 | 0.85 | 0.5 | 4 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q85_sp080_liqall | S02 | 0.85 | 0.8 | 10 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q85_sp080_liqmed | S02 | 0.85 | 0.8 | 10 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q85_sp100_liqall | S02 | 0.85 | 1 | 35 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q85_sp100_liqmed | S02 | 0.85 | 1 | 35 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q95_sp050_liqall | S02 | 0.95 | 0.5 | 4 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q95_sp050_liqmed | S02 | 0.95 | 0.5 | 4 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q95_sp080_liqall | S02 | 0.95 | 0.8 | 10 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q95_sp080_liqmed | S02 | 0.95 | 0.8 | 10 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q95_sp100_liqall | S02 | 0.95 | 1 | 35 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S02_q95_sp100_liqmed | S02 | 0.95 | 1 | 35 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |
| S05_q50_sp050_liqall | S05 | 0.5 | 0.5 | 4 | none | 0 | phase26_parameter_salvage_scan_not_acceptance |
| S05_q50_sp050_liqmed | S05 | 0.5 | 0.5 | 4 | above_median | 0.259685 | phase26_parameter_salvage_scan_not_acceptance |

## Replay Summary

| model_id | model_type | execution_profile | trades | symbols | scenario_days | mean_gross_return | mean_cost_return | mean_zerodha_charge_return | mean_net_return | win_rate_net | total_net_pnl_inr | market_shock_trade_fraction | disconnect_trade_fraction | acceptance_ready | replay_status | parent_strategy_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S07_q70_sp080_liqmed | strategy_variant | zero_latency_spread_only_control | 498 | 1 | 6 | 0.000201846 | 5.55458e-05 | 0 | 0.0001463 | 0.481928 | 7285.74 | 0.0100402 | 0 | False | event_order_replay_not_acceptance | S07 |
| S07_q70_sp100_liqmed | strategy_variant | zero_latency_spread_only_control | 498 | 1 | 6 | 0.000201846 | 5.55458e-05 | 0 | 0.0001463 | 0.481928 | 7285.74 | 0.0100402 | 0 | False | event_order_replay_not_acceptance | S07 |
| S07_q70_sp050_liqmed | strategy_variant | zero_latency_spread_only_control | 493 | 1 | 5 | 0.000193396 | 5.50042e-05 | 0 | 0.000138392 | 0.484787 | 6822.7 | 0 | 0 | False | event_order_replay_not_acceptance | S07 |
| S07_q70_sp050_liqall | strategy_variant | zero_latency_spread_only_control | 898 | 1 | 5 | 0.000179632 | 5.49864e-05 | 0 | 0.000124645 | 0.510022 | 11193.2 | 0 | 0 | False | event_order_replay_not_acceptance | S07 |
| S07_q50_sp050_liqall | strategy_variant | zero_latency_spread_only_control | 2682 | 2 | 5 | 0.000138431 | 4.99781e-05 | 0 | 8.84533e-05 | 0.517524 | 23723.2 | 0 | 0 | False | event_order_replay_not_acceptance | S07 |
| S09_q50_sp080_liqmed | strategy_variant | zero_latency_spread_only_control | 1810 | 2 | 8 | 0.000138463 | 5.50725e-05 | 0 | 8.33906e-05 | 0.525967 | 15093.7 | 0.00828729 | 0 | False | event_order_replay_not_acceptance | S09 |
| S09_q50_sp100_liqmed | strategy_variant | zero_latency_spread_only_control | 1810 | 2 | 8 | 0.000138463 | 5.50725e-05 | 0 | 8.33906e-05 | 0.525967 | 15093.7 | 0.00828729 | 0 | False | event_order_replay_not_acceptance | S09 |
| S09_q50_sp050_liqmed | strategy_variant | zero_latency_spread_only_control | 1795 | 1 | 7 | 0.000130296 | 5.46658e-05 | 0 | 7.56298e-05 | 0.527019 | 13575.6 | 0 | 0 | False | event_order_replay_not_acceptance | S09 |
| S07_q50_sp080_liqall | strategy_variant | zero_latency_spread_only_control | 3243 | 3 | 6 | 0.000123568 | 5.91079e-05 | 0 | 6.44605e-05 | 0.517422 | 20904.5 | 0.172988 | 0 | False | event_order_replay_not_acceptance | S07 |
| S07_q50_sp050_liqmed | strategy_variant | zero_latency_spread_only_control | 1923 | 2 | 5 | 0.000107979 | 4.80192e-05 | 0 | 5.99603e-05 | 0.50182 | 11530.4 | 0 | 0 | False | event_order_replay_not_acceptance | S07 |
| S07_q50_sp080_liqmed | strategy_variant | zero_latency_spread_only_control | 1943 | 2 | 6 | 0.000102969 | 4.85615e-05 | 0 | 5.44074e-05 | 0.50386 | 10571.4 | 0.0102934 | 0 | False | event_order_replay_not_acceptance | S07 |
| S07_q50_sp100_liqmed | strategy_variant | zero_latency_spread_only_control | 1943 | 2 | 6 | 0.000102969 | 4.85615e-05 | 0 | 5.44074e-05 | 0.50386 | 10571.4 | 0.0102934 | 0 | False | event_order_replay_not_acceptance | S07 |
| S07_q70_sp080_liqall | strategy_variant | zero_latency_spread_only_control | 1057 | 1 | 6 | 0.000101242 | 6.33304e-05 | 0 | 3.79112e-05 | 0.513718 | 4007.21 | 0.150426 | 0 | False | event_order_replay_not_acceptance | S07 |
| S05_q70_sp080_liqall | strategy_variant | zero_latency_spread_only_control | 1464 | 4 | 8 | 0.000113489 | 8.0708e-05 | 0 | 3.27809e-05 | 0.495902 | 4799.13 | 0.922131 | 0 | False | event_order_replay_not_acceptance | S05 |
| S09_q50_sp080_liqall | strategy_variant | zero_latency_spread_only_control | 5546 | 3 | 8 | 6.89742e-05 | 3.98215e-05 | 0 | 2.91527e-05 | 0.493689 | 16168.1 | 0.114136 | 0 | False | event_order_replay_not_acceptance | S09 |
| S05_q50_sp080_liqall | strategy_variant | zero_latency_spread_only_control | 4393 | 4 | 8 | 6.33476e-05 | 5.47632e-05 | 0 | 8.58431e-06 | 0.503528 | 3771.09 | 0.308445 | 0 | False | event_order_replay_not_acceptance | S05 |
| S09_q70_sp050_liqmed | strategy_variant | zero_latency_spread_only_control | 804 | 1 | 7 | 5.70292e-05 | 5.4574e-05 | 0 | 2.45519e-06 | 0.498756 | 197.397 | 0 | 0 | False | event_order_replay_not_acceptance | S09 |
| S09_q70_sp080_liqmed | strategy_variant | zero_latency_spread_only_control | 809 | 1 | 8 | 5.02797e-05 | 5.491e-05 | 0 | -4.6303e-06 | 0.500618 | -374.591 | 0.00618047 | 0 | False | event_order_replay_not_acceptance | S09 |
| S09_q70_sp100_liqmed | strategy_variant | zero_latency_spread_only_control | 809 | 1 | 8 | 5.02797e-05 | 5.491e-05 | 0 | -4.6303e-06 | 0.500618 | -374.591 | 0.00618047 | 0 | False | event_order_replay_not_acceptance | S09 |
| S05_q50_sp050_liqall | strategy_variant | zero_latency_spread_only_control | 3038 | 2 | 7 | 2.32978e-05 | 4.1592e-05 | 0 | -1.82942e-05 | 0.504279 | -5557.78 | 0 | 0 | False | event_order_replay_not_acceptance | S05 |
| S05_q50_sp050_liqmed | strategy_variant | zero_latency_spread_only_control | 3038 | 2 | 7 | 2.32978e-05 | 4.1592e-05 | 0 | -1.82942e-05 | 0.504279 | -5557.78 | 0 | 0 | False | event_order_replay_not_acceptance | S05 |
| S09_q50_sp050_liqall | strategy_variant | zero_latency_spread_only_control | 2554 | 1 | 7 | 2.75067e-05 | 5.47476e-05 | 0 | -2.72409e-05 | 0.490995 | -6957.33 | 0 | 0 | False | event_order_replay_not_acceptance | S09 |
| S05_q50_sp080_liqmed | strategy_variant | zero_latency_spread_only_control | 3425 | 3 | 8 | 1.81104e-05 | 4.76701e-05 | 0 | -2.95597e-05 | 0.500438 | -10124.2 | 0.112993 | 0 | False | event_order_replay_not_acceptance | S05 |
| S05_q50_sp100_liqmed | strategy_variant | zero_latency_spread_only_control | 3425 | 3 | 8 | 1.81104e-05 | 4.76701e-05 | 0 | -2.95597e-05 | 0.500438 | -10124.2 | 0.112993 | 0 | False | event_order_replay_not_acceptance | S05 |
| S09_q70_sp050_liqall | strategy_variant | zero_latency_spread_only_control | 1315 | 1 | 7 | -2.11905e-05 | 5.47158e-05 | 0 | -7.59063e-05 | 0.471483 | -9981.68 | 0 | 0 | False | event_order_replay_not_acceptance | S09 |
| S05_q70_sp050_liqall | strategy_variant | zero_latency_spread_only_control | 114 | 1 | 7 | -7.74596e-05 | 3.94226e-05 | 0 | -0.000116882 | 0.421053 | -1332.46 | 0 | 0 | False | event_order_replay_not_acceptance | S05 |
| S05_q70_sp050_liqmed | strategy_variant | zero_latency_spread_only_control | 114 | 1 | 7 | -7.74596e-05 | 3.94226e-05 | 0 | -0.000116882 | 0.421053 | -1332.46 | 0 | 0 | False | event_order_replay_not_acceptance | S05 |
| S09_q70_sp080_liqall | strategy_variant | zero_latency_spread_only_control | 1509 | 2 | 8 | -6.13277e-05 | 6.13742e-05 | 0 | -0.000122702 | 0.472498 | -18515.7 | 0.128562 | 0 | False | event_order_replay_not_acceptance | S09 |
| S02_q50_sp080_liqall | strategy_variant | zero_latency_spread_only_control | 6978 | 4 | 8 | -7.94085e-05 | 4.74639e-05 | 0 | -0.000126872 | 0.476211 | -88531.5 | 0.141301 | 0 | False | event_order_replay_not_acceptance | S02 |
| S02_q50_sp050_liqall | strategy_variant | zero_latency_spread_only_control | 5635 | 3 | 7 | -9.79744e-05 | 4.26346e-05 | 0 | -0.000140609 | 0.468855 | -79233.2 | 0 | 0 | False | event_order_replay_not_acceptance | S02 |
| S05_q85_sp080_liqall | strategy_variant | stressed_retail | 9 | 1 | 1 | 0.000915095 | 0.00105996 | 0.000826846 | -0.000144866 | 0.555556 | -130.38 | 1 | 0 | False | event_order_replay_not_acceptance | S05 |
| S05_q95_sp080_liqall | strategy_variant | stressed_retail | 9 | 1 | 1 | 0.000915095 | 0.00105996 | 0.000826846 | -0.000144866 | 0.555556 | -130.38 | 1 | 0 | False | event_order_replay_not_acceptance | S05 |
| S09_q85_sp080_liqall | strategy_variant | stressed_retail | 9 | 1 | 1 | 0.000915095 | 0.00105996 | 0.000826846 | -0.000144866 | 0.555556 | -130.38 | 1 | 0 | False | event_order_replay_not_acceptance | S09 |
| S09_q95_sp080_liqall | strategy_variant | stressed_retail | 9 | 1 | 1 | 0.000915095 | 0.00105996 | 0.000826846 | -0.000144866 | 0.555556 | -130.38 | 1 | 0 | False | event_order_replay_not_acceptance | S09 |
| S02_q50_sp050_liqmed | strategy_variant | zero_latency_spread_only_control | 5251 | 3 | 7 | -0.000111299 | 4.17311e-05 | 0 | -0.00015303 | 0.464483 | -80356.2 | 0 | 0 | False | event_order_replay_not_acceptance | S02 |
| S02_q50_sp080_liqmed | strategy_variant | zero_latency_spread_only_control | 5597 | 3 | 8 | -0.000114025 | 4.50516e-05 | 0 | -0.000159077 | 0.46382 | -89035.3 | 0.0618188 | 0 | False | event_order_replay_not_acceptance | S02 |
| S02_q50_sp100_liqmed | strategy_variant | zero_latency_spread_only_control | 5597 | 3 | 8 | -0.000114025 | 4.50516e-05 | 0 | -0.000159077 | 0.46382 | -89035.3 | 0.0618188 | 0 | False | event_order_replay_not_acceptance | S02 |
| S05_q70_sp080_liqmed | strategy_variant | zero_latency_spread_only_control | 496 | 3 | 8 | -0.000101028 | 8.23619e-05 | 0 | -0.00018339 | 0.459677 | -9096.14 | 0.770161 | 0 | False | event_order_replay_not_acceptance | S05 |
| S05_q70_sp100_liqmed | strategy_variant | zero_latency_spread_only_control | 496 | 3 | 8 | -0.000101028 | 8.23619e-05 | 0 | -0.00018339 | 0.459677 | -9096.14 | 0.770161 | 0 | False | event_order_replay_not_acceptance | S05 |
| S02_q70_sp050_liqall | strategy_variant | zero_latency_spread_only_control | 3209 | 3 | 7 | -0.000171475 | 3.9774e-05 | 0 | -0.000211249 | 0.450296 | -67789.9 | 0 | 0 | False | event_order_replay_not_acceptance | S02 |
| S02_q70_sp050_liqmed | strategy_variant | zero_latency_spread_only_control | 3173 | 3 | 7 | -0.000179991 | 3.96007e-05 | 0 | -0.000219591 | 0.449102 | -69676.3 | 0 | 0 | False | event_order_replay_not_acceptance | S02 |
| S02_q70_sp080_liqmed | strategy_variant | zero_latency_spread_only_control | 3447 | 3 | 8 | -0.000191118 | 4.40552e-05 | 0 | -0.000235173 | 0.446475 | -81064.2 | 0.0794894 | 0 | False | event_order_replay_not_acceptance | S02 |
| S02_q70_sp100_liqmed | strategy_variant | zero_latency_spread_only_control | 3447 | 3 | 8 | -0.000191118 | 4.40552e-05 | 0 | -0.000235173 | 0.446475 | -81064.2 | 0.0794894 | 0 | False | event_order_replay_not_acceptance | S02 |
| S02_q70_sp080_liqall | strategy_variant | zero_latency_spread_only_control | 3749 | 3 | 8 | -0.000197336 | 4.7904e-05 | 0 | -0.00024524 | 0.452387 | -91940.3 | 0.144038 | 0 | False | event_order_replay_not_acceptance | S02 |
| S01_q70_sp050_liqmed | strategy_variant | zero_latency_spread_only_control | 778 | 3 | 7 | -0.000217232 | 4.20758e-05 | 0 | -0.000259308 | 0.496144 | -20174.1 | 0 | 0 | False | event_order_replay_not_acceptance | S01 |
| S02_q95_sp050_liqall | strategy_variant | zero_latency_spread_only_control | 373 | 2 | 7 | -0.000225718 | 3.82658e-05 | 0 | -0.000263983 | 0.477212 | -9846.58 | 0 | 0 | False | event_order_replay_not_acceptance | S02 |
| S02_q95_sp050_liqmed | strategy_variant | zero_latency_spread_only_control | 373 | 2 | 7 | -0.000225718 | 3.82658e-05 | 0 | -0.000263983 | 0.477212 | -9846.58 | 0 | 0 | False | event_order_replay_not_acceptance | S02 |
| S01_q70_sp050_liqall | strategy_variant | zero_latency_spread_only_control | 791 | 3 | 7 | -0.000225624 | 4.22828e-05 | 0 | -0.000267907 | 0.495575 | -21191.5 | 0 | 0 | False | event_order_replay_not_acceptance | S01 |
| S02_q95_sp080_liqmed | strategy_variant | zero_latency_spread_only_control | 450 | 3 | 8 | -0.000244369 | 4.81998e-05 | 0 | -0.000292569 | 0.477778 | -13165.6 | 0.171111 | 0 | False | event_order_replay_not_acceptance | S02 |
| S02_q95_sp100_liqmed | strategy_variant | zero_latency_spread_only_control | 450 | 3 | 8 | -0.000244369 | 4.81998e-05 | 0 | -0.000292569 | 0.477778 | -13165.6 | 0.171111 | 0 | False | event_order_replay_not_acceptance | S02 |

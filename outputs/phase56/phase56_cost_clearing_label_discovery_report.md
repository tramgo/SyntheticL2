# Phase56 Cost-Clearing Label Discovery

Generated UTC: 2026-07-19T18:52:10.103932+00:00

Phase56 searches for no-lookahead observable rules that predict Phase55-style cost-clearing forward moves.
Thresholds are derived from the chronological training split and evaluated on a later test split.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase56_dense_shards_scanned | 8 | Dense shards scanned |
| phase56_observation_rows | 1981976 | No-lookahead feature/label observations |
| phase56_train_rows | 1382136 | Chronological training rows |
| phase56_test_rows | 599840 | Chronological test rows |
| phase56_rule_rows_evaluated | 180 | Candidate rules with at least 20 training trades |
| phase56_positive_test_rule_rows | 0 | Rules positive after retail costs on test split |
| phase56_scale_candidate_rows | 0 | Rules passing no-lookahead scale gate |
| phase56_best_traded_test_net_pnl_inr | -4829.7 | Best no-lookahead test net P&L among rules that emitted at least one test trade |
| phase56_best_rule_id | S56_MOMENTUM_SIGN_Q975_SP75_DP75_H20 | Top test rule |
| phase56_elapsed_seconds | 59.7151 | Elapsed seconds |
| phase56_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |
| phase56_recommend_scale_to_wider_dense_replay | 0 | 1 means at least one no-lookahead rule deserves wider replay |

## Oracle Label Summary

| horizon_events | observations | oracle_trades | oracle_trade_fraction | oracle_net_pnl_inr | oracle_mean_net_return |
| --- | --- | --- | --- | --- | --- |
| 20 | 1981976 | 8976 | 0.00452881 | 2.1386e+06 | 0.00238257 |
| 50 | 1981736 | 22416 | 0.0113099 | 5.34514e+06 | 0.00238452 |
| 100 | 1981336 | 44816 | 0.0226118 | 1.06894e+07 | 0.00238517 |

## Top No-Lookahead Rules

| rule_id | feature_family | feature | side_mode | horizon_events | abs_quantile | spread_quantile | depth_quantile | abs_threshold | spread_bps_max | depth_notional_min | train_trades | train_net_pnl_inr | train_precision_cost_clear | train_mean_net_return | test_trades | test_net_pnl_inr | test_gross_pnl_proxy_inr | test_cost_pnl_drag_proxy_inr | test_precision_cost_clear | test_mean_net_return | test_positive_symbol_rows | test_symbols | test_positive_after_costs | test_positive_symbol_fraction | phase56_candidate | has_test_trades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S56_MOMENTUM_SIGN_Q975_SP75_DP75_H20 | momentum | one_tick_return | sign | 20 | 0.975 | 0.75 | 0.75 | 2.57117e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q975_SP75_DP75_H50 | momentum | one_tick_return | sign | 50 | 0.975 | 0.75 | 0.75 | 2.57117e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q975_SP75_DP75_H100 | momentum | one_tick_return | sign | 100 | 0.975 | 0.75 | 0.75 | 2.57117e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q990_SP75_DP75_H20 | momentum | one_tick_return | sign | 20 | 0.99 | 0.75 | 0.75 | 2.74231e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q990_SP75_DP75_H50 | momentum | one_tick_return | sign | 50 | 0.99 | 0.75 | 0.75 | 2.74231e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q990_SP75_DP75_H100 | momentum | one_tick_return | sign | 100 | 0.99 | 0.75 | 0.75 | 2.74231e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q995_SP75_DP75_H20 | momentum | one_tick_return | sign | 20 | 0.995 | 0.75 | 0.75 | 2.83051e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q995_SP75_DP75_H50 | momentum | one_tick_return | sign | 50 | 0.995 | 0.75 | 0.75 | 2.83051e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q995_SP75_DP75_H100 | momentum | one_tick_return | sign | 100 | 0.995 | 0.75 | 0.75 | 2.83051e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_CONTRARIAN_OPPOSITE_Q975_SP75_DP75_H20 | contrarian | one_tick_return | opposite | 20 | 0.975 | 0.75 | 0.75 | 2.57117e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_CONTRARIAN_OPPOSITE_Q975_SP75_DP75_H50 | contrarian | one_tick_return | opposite | 50 | 0.975 | 0.75 | 0.75 | 2.57117e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_CONTRARIAN_OPPOSITE_Q975_SP75_DP75_H100 | contrarian | one_tick_return | opposite | 100 | 0.975 | 0.75 | 0.75 | 2.57117e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_CONTRARIAN_OPPOSITE_Q990_SP75_DP75_H20 | contrarian | one_tick_return | opposite | 20 | 0.99 | 0.75 | 0.75 | 2.74231e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_CONTRARIAN_OPPOSITE_Q990_SP75_DP75_H50 | contrarian | one_tick_return | opposite | 50 | 0.99 | 0.75 | 0.75 | 2.74231e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_CONTRARIAN_OPPOSITE_Q990_SP75_DP75_H100 | contrarian | one_tick_return | opposite | 100 | 0.99 | 0.75 | 0.75 | 2.74231e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_CONTRARIAN_OPPOSITE_Q995_SP75_DP75_H20 | contrarian | one_tick_return | opposite | 20 | 0.995 | 0.75 | 0.75 | 2.83051e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_CONTRARIAN_OPPOSITE_Q995_SP75_DP75_H50 | contrarian | one_tick_return | opposite | 50 | 0.995 | 0.75 | 0.75 | 2.83051e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_CONTRARIAN_OPPOSITE_Q995_SP75_DP75_H100 | contrarian | one_tick_return | opposite | 100 | 0.995 | 0.75 | 0.75 | 2.83051e-05 | 2.92412 | 847033 | 86 | -11226.1 | 0 | -0.00130535 | 37 | -4829.7 | 0 | 4829.7 | 0 | -0.00130533 | 0 | 1 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q900_SP50_DP50_H20 | momentum | one_tick_return | sign | 20 | 0.9 | 0.5 | 0.5 | 2.01252e-05 | 2.20702 | 620124 | 170 | -19638.2 | 0 | -0.00115519 | 72 | -8310.89 | 0 | 8310.89 | 0 | -0.00115429 | 0 | 2 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q900_SP50_DP50_H50 | momentum | one_tick_return | sign | 50 | 0.9 | 0.5 | 0.5 | 2.01252e-05 | 2.20702 | 620124 | 170 | -19638.2 | 0 | -0.00115519 | 72 | -8310.89 | 0 | 8310.89 | 0 | -0.00115429 | 0 | 2 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q900_SP50_DP50_H100 | momentum | one_tick_return | sign | 100 | 0.9 | 0.5 | 0.5 | 2.01252e-05 | 2.20702 | 620124 | 170 | -19638.2 | 0 | -0.00115519 | 72 | -8310.89 | 0 | 8310.89 | 0 | -0.00115429 | 0 | 2 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q950_SP50_DP50_H20 | momentum | one_tick_return | sign | 20 | 0.95 | 0.5 | 0.5 | 2.29378e-05 | 2.20702 | 620124 | 170 | -19638.2 | 0 | -0.00115519 | 72 | -8310.89 | 0 | 8310.89 | 0 | -0.00115429 | 0 | 2 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q950_SP50_DP50_H50 | momentum | one_tick_return | sign | 50 | 0.95 | 0.5 | 0.5 | 2.29378e-05 | 2.20702 | 620124 | 170 | -19638.2 | 0 | -0.00115519 | 72 | -8310.89 | 0 | 8310.89 | 0 | -0.00115429 | 0 | 2 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q950_SP50_DP50_H100 | momentum | one_tick_return | sign | 100 | 0.95 | 0.5 | 0.5 | 2.29378e-05 | 2.20702 | 620124 | 170 | -19638.2 | 0 | -0.00115519 | 72 | -8310.89 | 0 | 8310.89 | 0 | -0.00115429 | 0 | 2 | False | 0 | False | True |
| S56_MOMENTUM_SIGN_Q975_SP50_DP50_H20 | momentum | one_tick_return | sign | 20 | 0.975 | 0.5 | 0.5 | 2.57117e-05 | 2.20702 | 620124 | 170 | -19638.2 | 0 | -0.00115519 | 72 | -8310.89 | 0 | 8310.89 | 0 | -0.00115429 | 0 | 2 | False | 0 | False | True |

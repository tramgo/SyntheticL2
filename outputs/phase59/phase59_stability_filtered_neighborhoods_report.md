# Phase59 Stability-Filtered Neighborhoods

Generated UTC: 2026-07-19T19:08:27.742613+00:00

Phase59 addresses the Phase58 failure mode: a single exact interaction cell was profitable in discovery but absent in disjoint validation.
It requires discovery recurrence across shards/symbols and validates both exact and ±1-bin relaxed neighborhoods on disjoint shards.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase59_discovery_shards | 8 | Dense shards used to discover stable cells |
| phase59_validation_shards | 8 | Disjoint dense shards used for validation |
| phase59_discovery_observation_rows | 785944 | Discovery observation rows |
| phase59_validation_observation_rows | 783961 | Validation observation rows |
| phase59_train_positive_cell_rows | 17 | Discovery train-positive cell rows |
| phase59_discovery_stable_cell_rows | 2 | Cells recurring across multiple discovery shards and symbols |
| phase59_validation_result_rows | 34 | Exact and relaxed validation result rows |
| phase59_positive_validation_rows | 0 | Validation rows positive after retail costs |
| phase59_scale_candidate_rows | 0 | Stable cells passing disjoint validation gate |
| phase59_best_traded_validation_net_pnl_inr | -785962 | Best validation net P&L among rows that emitted at least one trade |
| phase59_elapsed_seconds | 53.8302 | Elapsed seconds |
| phase59_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |
| phase59_recommend_scale_to_month_sweep | 0 | 1 means at least one stable candidate deserves month/symbol sweep |

## Top Validation Results

| template_id | columns | cell_key | side | horizon_events | discovery_trades | discovery_net_pnl_inr | discovery_precision_cost_clear | discovery_symbols | discovery_shards | discovery_positive_symbol_fraction | discovery_positive_shard_fraction | discovery_stable | relaxation_radius | validation_trades | validation_net_pnl_inr | validation_gross_pnl_proxy_inr | validation_cost_pnl_drag_proxy_inr | validation_precision_cost_clear | validation_symbols | validation_shards | validation_positive_symbol_fraction | validation_positive_shard_fraction | validation_positive_after_costs | phase59_scale_candidate | has_validation_trades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| absret_spread_depth | abs_ret_bin;spread_bin;depth_bin | abs_ret_bin=6\|spread_bin=4\|depth_bin=4 | 1 | 100 | 1332 | 236574 | 0.15015 | 2 | 2 | 0.5 | 0.5 | True | 1 | 8483 | -785962 | 193669 | 979631 | 0.0471531 | 1 | 1 | 0 | 0 | False | False | True |
| absret_spread_depth | abs_ret_bin;spread_bin;depth_bin | abs_ret_bin=6\|spread_bin=4\|depth_bin=4 | 1 | 50 | 1332 | 35942.5 | 0.0750751 | 2 | 2 | 0.5 | 0.5 | True | 1 | 8483 | -882796 | 96834.6 | 979631 | 0.0235766 | 1 | 1 | 0 | 0 | False | False | True |
| absret_spread_depth | abs_ret_bin;spread_bin;depth_bin | abs_ret_bin=7\|spread_bin=5\|depth_bin=3 | 1 | 100 | 624 | 32622.3 | 0.320513 | 1 | 1 | 1 | 1 | False | 1 | 15871 | -1.72004e+06 | 244461 | 1.9645e+06 | 0.0756096 | 2 | 2 | 0 | 0 | False | False | True |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=6\|imb_bin=5\|spread_bin=4 | 1 | 100 | 876 | 295446 | 0.228311 | 1 | 1 | 1 | 1 | False | 0 | 25922 | -3.13136e+06 | 72401.5 | 3.20376e+06 | 0.033678 | 1 | 1 | 0 | 0 | False | False | True |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=6\|imb_bin=5\|spread_bin=4 | 1 | 50 | 876 | 94814.9 | 0.114155 | 1 | 1 | 1 | 1 | False | 0 | 25922 | -3.19568e+06 | 8082.83 | 3.20376e+06 | 0.0124605 | 1 | 1 | 0 | 0 | False | False | True |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=7\|imb_bin=7\|spread_bin=5 | 1 | 100 | 942 | 57263.5 | 0.318471 | 1 | 1 | 1 | 1 | False | 1 | 36877 | -4.8412e+06 | 101036 | 4.94224e+06 | 0.0298289 | 1 | 1 | 0 | 0 | False | False | True |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=6\|imb_bin=5\|spread_bin=4 | 1 | 100 | 876 | 295446 | 0.228311 | 1 | 1 | 1 | 1 | False | 1 | 43049 | -5.16675e+06 | 149654 | 5.3164e+06 | 0.0278752 | 2 | 2 | 0 | 0 | False | False | True |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=6\|imb_bin=5\|spread_bin=4 | 1 | 50 | 876 | 94814.9 | 0.114155 | 1 | 1 | 1 | 1 | False | 1 | 43049 | -5.24157e+06 | 74826.8 | 5.3164e+06 | 0.0139376 | 2 | 2 | 0 | 0 | False | False | True |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=6\|imb_bin=6\|spread_bin=3 | -1 | 50 | 416 | 15816.9 | 0.120192 | 1 | 1 | 1 | 1 | False | 1 | 42508 | -5.31812e+06 | -64318.6 | 5.2538e+06 | 0.0117625 | 1 | 1 | 0 | 0 | False | False | True |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=6\|imb_bin=6\|spread_bin=3 | -1 | 100 | 416 | 81699.5 | 0.240385 | 1 | 1 | 1 | 1 | False | 1 | 42508 | -5.38244e+06 | -128637 | 5.2538e+06 | 0.023525 | 1 | 1 | 0 | 0 | False | False | True |
| absret_spread_depth | abs_ret_bin;spread_bin;depth_bin | abs_ret_bin=7\|spread_bin=5\|depth_bin=2 | 1 | 100 | 318 | 24641.2 | 0.314465 | 1 | 1 | 1 | 1 | False | 1 | 55944 | -6.55268e+06 | 370928 | 6.92361e+06 | 0.0500501 | 2 | 2 | 0 | 0 | False | False | True |
| absret_spread_depth | abs_ret_bin;spread_bin;depth_bin | abs_ret_bin=6\|spread_bin=4\|depth_bin=4 | 1 | 100 | 1332 | 236574 | 0.15015 | 2 | 2 | 0.5 | 0.5 | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| absret_spread_depth | abs_ret_bin;spread_bin;depth_bin | abs_ret_bin=6\|spread_bin=4\|depth_bin=4 | 1 | 50 | 1332 | 35942.5 | 0.0750751 | 2 | 2 | 0.5 | 0.5 | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=6\|micro_bin=5\|imb_bin=5\|spread_bin=4\|depth_bin=4 | 1 | 100 | 876 | 295446 | 0.228311 | 1 | 1 | 1 | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=6\|micro_bin=5\|imb_bin=5\|spread_bin=4\|depth_bin=4 | 1 | 100 | 876 | 295446 | 0.228311 | 1 | 1 | 1 | 1 | False | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=6\|micro_bin=5\|imb_bin=5\|spread_bin=4\|depth_bin=4 | 1 | 50 | 876 | 94814.9 | 0.114155 | 1 | 1 | 1 | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=6\|micro_bin=5\|imb_bin=5\|spread_bin=4\|depth_bin=4 | 1 | 50 | 876 | 94814.9 | 0.114155 | 1 | 1 | 1 | 1 | False | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=6\|imb_bin=6\|spread_bin=3 | -1 | 100 | 416 | 81699.5 | 0.240385 | 1 | 1 | 1 | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=6\|micro_bin=6\|imb_bin=6\|spread_bin=3\|depth_bin=5 | -1 | 100 | 416 | 81699.5 | 0.240385 | 1 | 1 | 1 | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=6\|micro_bin=6\|imb_bin=6\|spread_bin=3\|depth_bin=5 | -1 | 100 | 416 | 81699.5 | 0.240385 | 1 | 1 | 1 | 1 | False | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=7\|imb_bin=7\|spread_bin=5 | 1 | 100 | 942 | 57263.5 | 0.318471 | 1 | 1 | 1 | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| absret_spread_depth | abs_ret_bin;spread_bin;depth_bin | abs_ret_bin=7\|spread_bin=5\|depth_bin=3 | 1 | 100 | 624 | 32622.3 | 0.320513 | 1 | 1 | 1 | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=7\|micro_bin=7\|imb_bin=7\|spread_bin=5\|depth_bin=3 | 1 | 100 | 624 | 32622.3 | 0.320513 | 1 | 1 | 1 | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=7\|micro_bin=7\|imb_bin=7\|spread_bin=5\|depth_bin=3 | 1 | 100 | 624 | 32622.3 | 0.320513 | 1 | 1 | 1 | 1 | False | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| absret_spread_depth | abs_ret_bin;spread_bin;depth_bin | abs_ret_bin=7\|spread_bin=5\|depth_bin=2 | 1 | 100 | 318 | 24641.2 | 0.314465 | 1 | 1 | 1 | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=7\|micro_bin=7\|imb_bin=7\|spread_bin=5\|depth_bin=2 | 1 | 100 | 318 | 24641.2 | 0.314465 | 1 | 1 | 1 | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=7\|micro_bin=7\|imb_bin=7\|spread_bin=5\|depth_bin=2 | 1 | 100 | 318 | 24641.2 | 0.314465 | 1 | 1 | 1 | 1 | False | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=6\|imb_bin=6\|spread_bin=3 | -1 | 50 | 416 | 15816.9 | 0.120192 | 1 | 1 | 1 | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=6\|micro_bin=6\|imb_bin=6\|spread_bin=3\|depth_bin=5 | -1 | 50 | 416 | 15816.9 | 0.120192 | 1 | 1 | 1 | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=6\|micro_bin=6\|imb_bin=6\|spread_bin=3\|depth_bin=5 | -1 | 50 | 416 | 15816.9 | 0.120192 | 1 | 1 | 1 | 1 | False | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False | False |

## Discovery Cell Catalog Sample

| template_id | columns | cell_key | side | horizon_events | discovery_trades | discovery_net_pnl_inr | discovery_precision_cost_clear | discovery_symbols | discovery_shards | discovery_positive_symbol_fraction | discovery_positive_shard_fraction | discovery_stable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| absret_spread_depth | abs_ret_bin;spread_bin;depth_bin | abs_ret_bin=6\|spread_bin=4\|depth_bin=4 | 1 | 50 | 1332 | 35942.5 | 0.0750751 | 2 | 2 | 0.5 | 0.5 | True |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=6\|imb_bin=5\|spread_bin=4 | 1 | 50 | 876 | 94814.9 | 0.114155 | 1 | 1 | 1 | 1 | False |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=6\|imb_bin=6\|spread_bin=3 | -1 | 50 | 416 | 15816.9 | 0.120192 | 1 | 1 | 1 | 1 | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=6\|micro_bin=5\|imb_bin=5\|spread_bin=4\|depth_bin=4 | 1 | 50 | 876 | 94814.9 | 0.114155 | 1 | 1 | 1 | 1 | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=6\|micro_bin=6\|imb_bin=6\|spread_bin=3\|depth_bin=5 | -1 | 50 | 416 | 15816.9 | 0.120192 | 1 | 1 | 1 | 1 | False |
| absret_spread_depth | abs_ret_bin;spread_bin;depth_bin | abs_ret_bin=6\|spread_bin=4\|depth_bin=4 | 1 | 100 | 1332 | 236574 | 0.15015 | 2 | 2 | 0.5 | 0.5 | True |
| absret_spread_depth | abs_ret_bin;spread_bin;depth_bin | abs_ret_bin=7\|spread_bin=5\|depth_bin=3 | 1 | 100 | 624 | 32622.3 | 0.320513 | 1 | 1 | 1 | 1 | False |
| absret_spread_depth | abs_ret_bin;spread_bin;depth_bin | abs_ret_bin=7\|spread_bin=5\|depth_bin=2 | 1 | 100 | 318 | 24641.2 | 0.314465 | 1 | 1 | 1 | 1 | False |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=6\|imb_bin=5\|spread_bin=4 | 1 | 100 | 876 | 295446 | 0.228311 | 1 | 1 | 1 | 1 | False |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=6\|imb_bin=6\|spread_bin=3 | -1 | 100 | 416 | 81699.5 | 0.240385 | 1 | 1 | 1 | 1 | False |
| absret_imb_spread | abs_ret_bin;imb_bin;spread_bin | abs_ret_bin=7\|imb_bin=7\|spread_bin=5 | 1 | 100 | 942 | 57263.5 | 0.318471 | 1 | 1 | 1 | 1 | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=6\|micro_bin=5\|imb_bin=5\|spread_bin=4\|depth_bin=4 | 1 | 100 | 876 | 295446 | 0.228311 | 1 | 1 | 1 | 1 | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=6\|micro_bin=6\|imb_bin=6\|spread_bin=3\|depth_bin=5 | -1 | 100 | 416 | 81699.5 | 0.240385 | 1 | 1 | 1 | 1 | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=7\|micro_bin=7\|imb_bin=7\|spread_bin=5\|depth_bin=3 | 1 | 100 | 624 | 32622.3 | 0.320513 | 1 | 1 | 1 | 1 | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=7\|micro_bin=7\|imb_bin=7\|spread_bin=5\|depth_bin=2 | 1 | 100 | 318 | 24641.2 | 0.314465 | 1 | 1 | 1 | 1 | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=5\|micro_bin=1\|imb_bin=2\|spread_bin=0\|depth_bin=2 | -1 | 100 | 138 | 4093.61 | 0.5 | 1 | 1 | 1 | 1 | False |
| all_core_interaction | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | abs_ret_bin=5\|micro_bin=2\|imb_bin=3\|spread_bin=1\|depth_bin=6 | 1 | 100 | 256 | 1175.91 | 0.390625 | 1 | 1 | 1 | 1 | False |

## Bin Edges

| bin_feature | edges |
| --- | --- |
| abs_ret_bin | -inf;2.17661928437e-06;4.40364258755e-06;6.49209042081e-06;8.6932514709e-06;1.08660323673e-05;1.37660444829e-05;1.88126074576e-05;inf |
| micro_bin | -inf;-2.31245541861e-06;1.34942256286e-06;5.95159921455e-06;6.95395515859e-06;1.62760256115e-05;2.59973188966e-05;5.93016702603e-05;inf |
| abs_micro_bin | -inf;1.3519704389e-06;3.62559671277e-06;5.97279878857e-06;6.95395515859e-06;1.62760256115e-05;2.59973188966e-05;5.93016702603e-05;inf |
| imb_bin | -inf;-0.0286975717439;0.0183246073298;0.0355329949239;0.0897755610973;0.112244897959;0.236406619385;0.339759036145;inf |
| spread_bin | -inf;1.51906425642;1.5762925599;1.62813415826;2.19937317864;2.78590332916;2.92411910912;3.62778886269;inf |
| depth_bin | -inf;140543.575;502372.9;554337.4;618419.4;742756.45;829800.1;2304330;inf |

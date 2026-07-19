# Phase57 Supervised Interaction Ranker

Generated UTC: 2026-07-19T18:55:50.925585+00:00

Phase57 moves beyond hand-tuned thresholds by mining train-positive feature-interaction cells and validating them on a later chronological test split.
It remains dependency-light, deterministic, no-lookahead, and after-cost.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase57_dense_shards_scanned | 8 | Dense shards scanned |
| phase57_observation_rows | 1981976 | Feature/label observations |
| phase57_train_rows | 1382136 | Chronological train rows |
| phase57_test_rows | 599840 | Chronological test rows |
| phase57_interaction_candidate_rows | 14 | Train-positive interaction cells evaluated on test |
| phase57_positive_test_rows | 1 | Interaction candidates positive after retail costs on test |
| phase57_scale_candidate_rows | 1 | Interaction candidates passing wider-replay gate |
| phase57_best_traded_test_net_pnl_inr | 4093.61 | Best test net P&L among interaction candidates with test trades |
| phase57_best_rule_key | abs_ret_bin=5\|micro_bin=1\|imb_bin=2\|spread_bin=0\|depth_bin=2 | Best ranked interaction cell key |
| phase57_elapsed_seconds | 37.6043 | Elapsed seconds |
| phase57_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |
| phase57_recommend_scale_to_wider_dense_replay | 1 | 1 means at least one supervised interaction candidate deserves wider replay |

## Top Interaction Candidates

| horizon_events | template_id | side | cell_key | columns | train_trades | train_net_pnl_inr | train_precision_cost_clear | train_mean_net_return | train_rank_within_template | test_trades | test_net_pnl_inr | test_gross_pnl_proxy_inr | test_cost_pnl_drag_proxy_inr | test_precision_cost_clear | test_mean_net_return | test_symbols | test_positive_symbol_fraction | test_positive_after_costs | phase57_scale_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | all_core_interaction | -1 | abs_ret_bin=5\|micro_bin=1\|imb_bin=2\|spread_bin=0\|depth_bin=2 | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | 138 | 4093.61 | 0.5 | 0.000296639 | 6 | 138 | 4093.61 | 19229.9 | 15136.3 | 0.5 | 0.000296639 | 1 | 1 | True | True |
| 100 | absret_imb_spread | 1 | abs_ret_bin=6\|imb_bin=5\|spread_bin=4 | abs_ret_bin;imb_bin;spread_bin | 1712 | 234190 | 0.175234 | 0.00136793 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| 100 | all_core_interaction | 1 | abs_ret_bin=6\|micro_bin=5\|imb_bin=5\|spread_bin=4\|depth_bin=4 | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | 1712 | 234190 | 0.175234 | 0.00136793 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| 100 | absret_spread_depth | 1 | abs_ret_bin=6\|spread_bin=4\|depth_bin=4 | abs_ret_bin;spread_bin;depth_bin | 2168 | 175414 | 0.138376 | 0.000809105 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| 100 | absret_imb_spread | -1 | abs_ret_bin=6\|imb_bin=6\|spread_bin=3 | abs_ret_bin;imb_bin;spread_bin | 828 | 39193.5 | 0.120773 | 0.000473351 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| 100 | all_core_interaction | -1 | abs_ret_bin=6\|micro_bin=6\|imb_bin=6\|spread_bin=3\|depth_bin=5 | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | 828 | 39193.5 | 0.120773 | 0.000473351 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| 100 | absret_imb_spread | 1 | abs_ret_bin=7\|imb_bin=7\|spread_bin=5 | abs_ret_bin;imb_bin;spread_bin | 1271 | 29330.7 | 0.236035 | 0.000230769 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| 100 | absret_spread_depth | 1 | abs_ret_bin=7\|spread_bin=5\|depth_bin=3 | abs_ret_bin;spread_bin;depth_bin | 638 | 18217.6 | 0.15674 | 0.000285543 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| 100 | all_core_interaction | 1 | abs_ret_bin=7\|micro_bin=7\|imb_bin=7\|spread_bin=5\|depth_bin=3 | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | 638 | 18217.6 | 0.15674 | 0.000285543 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| 50 | absret_imb_spread | 1 | abs_ret_bin=6\|imb_bin=5\|spread_bin=4 | abs_ret_bin;imb_bin;spread_bin | 1712 | 13694.9 | 0.0876168 | 7.99937e-05 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| 50 | all_core_interaction | 1 | abs_ret_bin=6\|micro_bin=5\|imb_bin=5\|spread_bin=4\|depth_bin=4 | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | 1712 | 13694.9 | 0.0876168 | 7.99937e-05 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| 100 | absret_spread_depth | 1 | abs_ret_bin=7\|spread_bin=5\|depth_bin=2 | abs_ret_bin;spread_bin;depth_bin | 633 | 11113.1 | 0.315956 | 0.000175562 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| 100 | all_core_interaction | 1 | abs_ret_bin=7\|micro_bin=7\|imb_bin=7\|spread_bin=5\|depth_bin=2 | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | 633 | 11113.1 | 0.315956 | 0.000175562 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| 100 | all_core_interaction | 1 | abs_ret_bin=5\|micro_bin=1\|imb_bin=1\|spread_bin=0\|depth_bin=3 | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | 964 | 15670.8 | 0.262448 | 0.00016256 | 4 | 482 | -27739.5 | 25235.7 | 52975.2 | 0.190871 | -0.000575509 | 1 | 0 | False | False |

## Bin Edges

| bin_feature | edges |
| --- | --- |
| abs_ret_bin | -inf;2.16485535914e-06;4.39678216613e-06;6.50337912941e-06;8.71681212289e-06;1.08851656642e-05;1.38243495933e-05;1.88625886387e-05;inf |
| micro_bin | -inf;-2.31245541861e-06;1.3518286669e-06;5.99664188071e-06;7.03068858565e-06;1.62983923543e-05;2.64817399741e-05;7.61080657135e-05;inf |
| abs_micro_bin | -inf;1.35342198246e-06;3.62559671277e-06;6.02940419851e-06;7.03068858565e-06;1.62983923543e-05;2.64817399741e-05;7.61080657135e-05;inf |
| imb_bin | -inf;-0.0286975717439;0.0183727034121;0.0356234096692;0.0911270983213;0.112244897959;0.243181818182;0.553990610329;inf |
| spread_bin | -inf;1.51906425642;1.57770181436;1.63505559189;2.20701831825;2.80426247897;2.92411910912;3.62811791383;inf |
| depth_bin | -inf;140543.575;502372.9;554337.4;620123.6;742562.1;847033.05;2333648;inf |

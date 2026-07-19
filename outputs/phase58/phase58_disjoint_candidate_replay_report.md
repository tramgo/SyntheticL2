# Phase58 Disjoint Candidate Replay

Generated UTC: 2026-07-19T18:59:35.862254+00:00

Phase58 replays the exact Phase57-discovered interaction rule on dense shards outside the discovery window.
The Phase57 bin edges and cell key are reused without refitting.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase58_disjoint_shards_scanned | 24 | Dense shards scanned outside Phase57 discovery shard window |
| phase58_trade_rows | 0 | Candidate trade rows on disjoint validation shards |
| phase58_net_pnl_inr | 0 | After-cost net P&L on disjoint validation shards |
| phase58_positive_symbol_fraction | 0 | Fraction of shard-symbol rows positive after costs |
| phase58_precision_cost_clear | 0 | Trade-weighted cost-clearing precision |
| phase58_survives_disjoint_validation | 0 | 1 means the Phase57 candidate survived disjoint validation |
| phase58_elapsed_seconds | 14.6191 | Elapsed seconds |
| phase58_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |
| phase58_recommend_scale_to_month_sweep | 0 | 1 means move to broader month/symbol sweep |

## Candidate Summary

| candidate_source | horizon_events | side | cell_key | symbols | trade_dates | trades | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | positive_symbol_fraction | precision_cost_clear | mean_net_return | phase58_survives_disjoint_validation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase57 | 100 | -1 | abs_ret_bin=5\|micro_bin=1\|imb_bin=2\|spread_bin=0\|depth_bin=2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False |

## Daily Symbol Results

_No rows._

## Cell Coverage Diagnostics

| cell_component | component_match_rows | component_match_fraction | cumulative_match_rows | cumulative_match_fraction |
| --- | --- | --- | --- | --- |
| abs_ret_bin=5 | 750805 | 0.127163 | 750805 | 0.127163 |
| micro_bin=1 | 287671 | 0.0487226 | 49768 | 0.00842916 |
| imb_bin=2 | 25792 | 0.00436837 | 0 | 0 |
| spread_bin=0 | 1646687 | 0.278898 | 0 | 0 |
| depth_bin=2 | 424570 | 0.071909 | 0 | 0 |

## Replayed Phase57 Candidate

| horizon_events | template_id | side | cell_key | columns | train_trades | train_net_pnl_inr | train_precision_cost_clear | train_mean_net_return | train_rank_within_template | test_trades | test_net_pnl_inr | test_gross_pnl_proxy_inr | test_cost_pnl_drag_proxy_inr | test_precision_cost_clear | test_mean_net_return | test_symbols | test_positive_symbol_fraction | test_positive_after_costs | phase57_scale_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | all_core_interaction | -1 | abs_ret_bin=5\|micro_bin=1\|imb_bin=2\|spread_bin=0\|depth_bin=2 | abs_ret_bin;micro_bin;imb_bin;spread_bin;depth_bin | 138 | 4093.61 | 0.5 | 0.000296639 | 6 | 138 | 4093.61 | 19229.9 | 15136.3 | 0.5 | 0.000296639 | 1 | 1 | True | True |

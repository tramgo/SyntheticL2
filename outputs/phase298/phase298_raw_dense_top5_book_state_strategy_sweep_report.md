# Phase298 Raw Dense Top-Five Book-State Strategy Sweep

Phase298 runs a bounded full-year HDFCBANK slice over the Phase51 raw dense top-five market-by-price lake.

Unlike Phase296, this milestone uses persisted raw book-state columns for levels 1-5: bid/ask price, quantity and order-count fields.

The sweep is intentionally bounded by symbol and deterministic dense-row stride so the milestone completes interactively without claiming a full 5.97B-row portfolio result.

No replay, promotion, paper/live acceptance, or deployable profitability claim is opened by this search.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase298_raw_dense_sweep_complete | 1 | Phase298 raw dense top-five book-state strategy sweep completed |
| phase298_selected_route | P298_RAW_DENSE_TOP5_BOOK_STATE_STRATEGY_SWEEP | Selected route |
| phase298_dense_root | raw_synthetic_l2_dense_full_year | Raw dense lake root |
| phase298_symbol_rows | 1 | Symbols in bounded sweep |
| phase298_trade_month_rows | 12 | Trade months in bounded sweep |
| phase298_source_file_rows | 12 | Dense shard files scanned |
| phase298_sample_stride | 256 | Deterministic dense-row sample stride |
| phase298_sampled_dense_rows | 729132 | Sampled raw dense rows |
| phase298_shard_trade_date_rows | 252 | Shard-date rows sampled |
| phase298_raw_event_rows | 9596 | Raw dense candidate event rows |
| phase298_variant_rows | 576 | Raw-book-state variants evaluated |
| phase298_scenario_rows | 1152 | Cost200 fixed-capital scenarios evaluated |
| phase298_sparse_above12_scenario_rows | 0 | Above-12 sparse diagnostic rows |
| phase298_robust_portfolio_floor_scenario_rows | 0 | Robust floor rows |
| phase298_robust_portfolio_above12_scenario_rows | 0 | Robust above-12 rows |
| phase298_best_variant_id | P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q99_DL3_H6 | Best variant |
| phase298_best_strategy_family | P298_RAW_MICROPRICE_DEPTH_REVERSAL | Best family |
| phase298_best_cost200_annualized_pct | 382.997 | Best fixed-capital annualized diagnostic |
| phase298_best_realized_net_pnl_inr | 15198.3 | Best net P&L |
| phase298_best_scheduled_event_rows | 3 | Best scheduled events |
| phase298_best_observed_trade_dates | 1 | Best observed dates |
| phase298_best_initial_capital_inr | 1e+06 | Fixed initial capital denominator |
| phase298_raw_book_state_l1_l5_required | 1 | Raw levels 1-5 required |
| phase298_levels_2_to_5_required | 1 | Levels 2-5 materiality required |
| phase298_l1_only_variant_rows | 0 | L1-only variants |
| phase298_net_edge_live_mask_rows | 0 | Net edge live masks |
| phase298_annualized_denominator | fixed_initial_capital | Annualized denominator |
| phase298_strategy_replay_allowed | 0 | No replay |
| phase298_strategy_promotion_allowed | 0 | No promotion |
| phase298_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase298_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase298_hard_gate_pass_rows | 13 | Passed hard gates |
| phase298_hard_gate_rows | 13 | Hard gates |
| phase298_next_best_action | run_phase299_raw_dense_top5_book_state_strategy_sweep_interpretation_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P298_PHASE297_WORK_ORDER_PRESENT | True | run_phase298_raw_dense_top5_book_state_strategy_sweep_no_paper_live | Phase297 routes to Phase298 | hard |
| P298_DENSE_LAKE_MATERIALIZED | True | 1 | Phase51 full 80GB-class dense lake materialized | hard |
| P298_RAW_SCHEMA_PRESENT | True | 12/12 | all sampled shards have raw levels 1-5 price/qty/order columns | hard |
| P298_FULL_YEAR_SLICE_PRESENT | True | months=12;date_rows=252 | 12 monthly shards and >=240 shard-date rows | hard |
| P298_RAW_EVENTS_PRESENT | True | 9596 | >0 raw dense candidate events | hard |
| P298_VARIANTS_PRESENT | True | 576 | >=48 raw-book-state variants | hard |
| P298_SCENARIOS_PRESENT | True | 1152 | >=96 fixed-capital scenarios | hard |
| P298_FIXED_CAPITAL_REQUIRED | True | 1e+06 | fixed initial capital denominator | hard |
| P298_COST200_REQUIRED | True | cost200 | Zerodha cost stress profile | hard |
| P298_RAW_FULL_DEPTH_REQUIRED | True | l1_only=0 | raw levels 1-5 and levels 2-5 materiality | hard |
| P298_NO_LIVE_NET_EDGE_MASKS | True | 0 | no net/gross edge live masks | hard |
| P298_FIXED_CAPITAL_ANNUALIZED_DENOMINATOR | True | fixed_initial_capital | no unlimited-capital annualization | hard |
| P298_BOUNDARIES_CLOSED | True | replay=0;paper=0;claim=0 | no replay/paper/live/claim | hard |

## Shard Summary

| sampled_rows | trade_dates | min_trade_date | max_trade_date | avg_spread_bps | avg_abs_top5_imbalance | avg_abs_beyond_l1_imbalance | avg_abs_microprice_dev_l5 | trade_month | symbol | file_path | sample_stride |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 63686 | 22 | 2026-01-01 | 2026-01-30 | 1.44768 | 0.572532 | 0.572532 | 0.000125657 | 2026-01 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | 256 |
| 57921 | 20 | 2026-02-02 | 2026-02-27 | 1.55661 | 0.572077 | 0.572074 | 0.000128781 | 2026-02 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=HDFCBANK\part-00000.parquet | 256 |
| 63686 | 22 | 2026-03-02 | 2026-03-31 | 1.41677 | 0.572564 | 0.572566 | 0.000124974 | 2026-03 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=HDFCBANK\part-00000.parquet | 256 |
| 63624 | 22 | 2026-04-01 | 2026-04-30 | 1.56933 | 0.571986 | 0.571982 | 0.000128646 | 2026-04 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-04\symbol=HDFCBANK\part-00000.parquet | 256 |
| 60804 | 21 | 2026-05-01 | 2026-05-29 | 1.57224 | 0.572489 | 0.572488 | 0.000129373 | 2026-05 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-05\symbol=HDFCBANK\part-00000.parquet | 256 |
| 63515 | 22 | 2026-06-01 | 2026-06-30 | 1.66955 | 0.57247 | 0.572468 | 0.000132331 | 2026-06 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-06\symbol=HDFCBANK\part-00000.parquet | 256 |
| 66529 | 23 | 2026-07-01 | 2026-07-31 | 1.43905 | 0.572502 | 0.572504 | 0.000125807 | 2026-07 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-07\symbol=HDFCBANK\part-00000.parquet | 256 |
| 60749 | 21 | 2026-08-03 | 2026-08-31 | 1.61926 | 0.57215 | 0.572146 | 0.000130379 | 2026-08 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=HDFCBANK\part-00000.parquet | 256 |
| 63593 | 22 | 2026-09-01 | 2026-09-30 | 1.73911 | 0.572829 | 0.572828 | 0.000134677 | 2026-09 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-09\symbol=HDFCBANK\part-00000.parquet | 256 |
| 63624 | 22 | 2026-10-01 | 2026-10-30 | 1.27203 | 0.572148 | 0.572149 | 0.000120273 | 2026-10 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-10\symbol=HDFCBANK\part-00000.parquet | 256 |
| 60881 | 21 | 2026-11-02 | 2026-11-30 | 1.51101 | 0.572172 | 0.572169 | 0.000127465 | 2026-11 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-11\symbol=HDFCBANK\part-00000.parquet | 256 |
| 40520 | 14 | 2026-12-01 | 2026-12-18 | 1.52826 | 0.572685 | 0.572689 | 0.000128215 | 2026-12 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-12\symbol=HDFCBANK\part-00000.parquet | 256 |

## Family Summary

| strategy_family | scenario_rows | variant_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_variant_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL | 288 | 144 | 6 | 0 | 0 | 0 | 0 | -19.6156 | -4.16713 | 382.997 | 15658 | P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q99_DL3_H6 |
| P298_RAW_ORDERCOUNT_PRESSURE_CONTINUATION | 288 | 144 | 6 | 0 | 0 | 0 | 0 | -39.5878 | -1.04178 | 2.52844 | 802.679 | P298_RAW_ORDERCOUNT_PRESSURE_CONTINUATION_HDFCBANK_2026-01_Q99_DL3_H6 |
| P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION | 288 | 144 | 6 | 0 | 0 | 0 | 0 | -39.5878 | -1.04178 | 1.9451 | 540.304 | P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-11_Q99_DL3_H6 |
| P298_RAW_TOP5_PRESSURE_CONTINUATION | 288 | 144 | 6 | 0 | 0 | 0 | 0 | -39.5878 | -1.19061 | -0.219323 | -47.1922 | P298_RAW_TOP5_PRESSURE_CONTINUATION_HDFCBANK_2026-05_Q95_DL1_H6 |

## Top Variants

| phase298_variant_id | strategy_family | symbol | threshold_quantile | daily_event_limit | exit_horizon_ticks | scenario_rows | selected_event_rows | max_scheduled_event_rows | cost200_above12_sparse_diagnostic_rows | robust_portfolio_floor_above12_rows | sparse_floor_met_rows | robust_portfolio_floor_met_rows | min_annualized_pct | median_annualized_pct | max_annualized_pct | max_net_pnl_inr | best_scenario_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 382.997 | 382.997 | 382.997 | 15198.3 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q99_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-09_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 5.79169 | 101.541 | 197.29 | 15658 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-09_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 2.78547 | 98.5348 | 194.284 | 15419.4 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-01_Q95_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-12_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 3 | 3 | 0 | 0 | 0 | 0 | 31.829 | 31.829 | 31.829 | 1263.06 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-12_Q99_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-03_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 12.9295 | 14.422 | 15.9145 | 1263.06 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-03_Q95_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-03_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 12.9295 | 14.422 | 15.9145 | 1263.06 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-03_Q99_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-12_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 11.2966 | 13.6056 | 15.9145 | 1263.06 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-12_Q95_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-04_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 9 | 6 | 0 | 0 | 0 | 0 | -1.11444 | 6.09483 | 13.3041 | 1583.82 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-04_Q95_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-04_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 9 | 6 | 0 | 0 | 0 | 0 | -1.11444 | 6.09483 | 13.3041 | 1583.82 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-04_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-06_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | 9.89443 | 10.4841 | 11.0737 | 878.866 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-06_Q99_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-09_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 12 | 6 | 0 | 0 | 0 | 0 | -9.61646 | -3.36031 | 2.89584 | 459.658 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-09_Q95_DL3_H6_CAP1000000_NOT100000_CONC1_COST200 |
| P298_RAW_ORDERCOUNT_PRESSURE_CONTINUATION_HDFCBANK_2026-01_Q99_DL3_H6 | P298_RAW_ORDERCOUNT_PRESSURE_CONTINUATION | HDFCBANK | 0.99 | 3 | 6 | 2 | 24 | 6 | 0 | 0 | 0 | 0 | 0.0346291 | 1.28153 | 2.52844 | 802.679 | P271_P298_RAW_ORDERCOUNT_PRESSURE_CONTINUATION_HDFCBANK_2026-01_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-11_Q99_DL3_H6 | P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION | HDFCBANK | 0.99 | 3 | 6 | 2 | 21 | 6 | 0 | 0 | 0 | 0 | -2.30756 | -0.181232 | 1.9451 | 540.304 | P271_P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-11_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-02_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | -11.0859 | -4.97323 | 1.13942 | 90.4304 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-02_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-11_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 6 | 6 | 0 | 0 | 0 | 0 | -11.0859 | -4.97323 | 1.13942 | 90.4304 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-11_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-06_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 12 | 6 | 0 | 0 | 0 | 0 | -5.13221 | -2.36378 | 0.404648 | 64.2298 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-06_Q95_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-05_Q95_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.95 | 3 | 6 | 2 | 9 | 6 | 0 | 0 | 0 | 0 | -0.0723884 | -0.0650069 | -0.0576254 | -6.86017 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-05_Q95_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-05_Q99_DL3_H6 | P298_RAW_MICROPRICE_DEPTH_REVERSAL | HDFCBANK | 0.99 | 3 | 6 | 2 | 9 | 6 | 0 | 0 | 0 | 0 | -0.0723884 | -0.0650069 | -0.0576254 | -6.86017 | P271_P298_RAW_MICROPRICE_DEPTH_REVERSAL_HDFCBANK_2026-05_Q99_DL3_H6_CAP1000000_NOT100000_CONC2_COST200 |
| P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-07_Q95_DL1_H1 | P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION | HDFCBANK | 0.95 | 1 | 1 | 2 | 19 | 2 | 0 | 0 | 0 | 0 | -0.438646 | -0.328984 | -0.219323 | -165.362 | P271_P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-07_Q95_DL1_H1_CAP1000000_NOT100000_CONC1_COST200 |
| P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-07_Q95_DL1_H3 | P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION | HDFCBANK | 0.95 | 1 | 3 | 2 | 19 | 2 | 0 | 0 | 0 | 0 | -0.438646 | -0.328984 | -0.219323 | -165.362 | P271_P298_RAW_BEYOND_L1_ABSORPTION_CONTINUATION_HDFCBANK_2026-07_Q95_DL1_H3_CAP1000000_NOT100000_CONC1_COST200 |

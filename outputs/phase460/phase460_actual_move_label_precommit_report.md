# Phase460 Actual-Move Candidate Label Source Precommit

Phase460 freezes an actual non-flat move-candidate label source after fixed-window routes produced zero gross edge.

Important boundary: actual forward movement is a label source for research, not a tradable signal available at order time.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase460_actual_move_label_precommit_complete | 1 | Phase460 precommit completed |
| phase460_thesis_id | P460_ACTUAL_MOVE_CANDIDATE_LABEL_SOURCE_PRECOMMIT | Actual-move label-source thesis |
| phase460_selected_source_id | actual_move_candidate_labels_for_past_only_l2_feature_learning | Selected label source |
| phase460_execution_results_generated | 0 | Precommit only |
| phase460_strategy_promotion_allowed | 0 | No promotion |
| phase460_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase460_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase460_phase461_allowed_next | 1 | Whether Phase461 may materialize labels |
| phase460_hard_gate_pass_rows | 10 | Passed hard gates |
| phase460_hard_gate_rows | 10 | Hard gates |
| phase460_next_best_action | run_phase461_actual_move_candidate_label_materialization_no_pnl | Recommended next action |

## Prior Boundary

| phase | route | verdict_or_status | boundary |
| --- | --- | --- | --- |
| P459 | delayed_fixed_window_cross_asset | P459_DELAYED_CROSS_ASSET_DISPLACEMENT_REJECTED_ZERO_GROSS_EDGE | closed; next action requires actual move-candidate label source or pausing fixed-window routes |
| P458 | fixed_row_5000_windows | zero_gross_edge | do not tune row offsets after result |
| P455 | first_window_cross_asset | zero_gross_edge | do not tune first-window thresholds or side rules |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| dense_root_exists | 1 | Dense raw L1-L5 root exists. |
| selected_file_rows | 21 | Frozen selected file rows. |
| selected_files_present | 21 | Selected files present. |
| months | 2026-01;2026-02;2026-03 | Frozen months. |
| target_symbols | AXISBANK;HDFCBANK;ICICIBANK;INFY;HCLTECH;TCS;RELIANCE | Frozen target symbols. |
| window_start_rows | 0;5000;10000;20000;50000 | Frozen candidate offsets per symbol/date. |
| feature_lookback_ticks | 20 | Past-only feature lookback. |
| entry_index | 20 | Entry index after feature window. |
| horizon_ticks | 240 | Forward label horizon. |
| min_abs_forward_move_bps | 2 | Actual non-flat move label floor. |

## Selected Files

| trade_month | symbol | path | exists |
| --- | --- | --- | --- |
| 2026-01 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=AXISBANK\part-00000.parquet | 1 |
| 2026-01 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | 1 |
| 2026-01 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ICICIBANK\part-00000.parquet | 1 |
| 2026-01 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=INFY\part-00000.parquet | 1 |
| 2026-01 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=HCLTECH\part-00000.parquet | 1 |
| 2026-01 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=TCS\part-00000.parquet | 1 |
| 2026-01 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=RELIANCE\part-00000.parquet | 1 |
| 2026-02 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=AXISBANK\part-00000.parquet | 1 |
| 2026-02 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=HDFCBANK\part-00000.parquet | 1 |
| 2026-02 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ICICIBANK\part-00000.parquet | 1 |
| 2026-02 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=INFY\part-00000.parquet | 1 |
| 2026-02 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=HCLTECH\part-00000.parquet | 1 |
| 2026-02 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=TCS\part-00000.parquet | 1 |
| 2026-02 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=RELIANCE\part-00000.parquet | 1 |
| 2026-03 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=AXISBANK\part-00000.parquet | 1 |
| 2026-03 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=HDFCBANK\part-00000.parquet | 1 |
| 2026-03 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ICICIBANK\part-00000.parquet | 1 |
| 2026-03 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=INFY\part-00000.parquet | 1 |
| 2026-03 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=HCLTECH\part-00000.parquet | 1 |
| 2026-03 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=TCS\part-00000.parquet | 1 |
| 2026-03 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=RELIANCE\part-00000.parquet | 1 |

## Frozen Phase461 Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P460_ACTUAL_MOVE_CANDIDATE_LABEL_SOURCE_PRECOMMIT | Phase460 actual-move label-source precommit. |
| selected_source | actual_move_candidate_labels_for_past_only_l2_feature_learning | Materially new label source after fixed-window failures. |
| material_difference | candidate_selection_by_actual_forward_move_labels_not_fixed_clock_windows | A label dataset source, not a tradable signal by itself. |
| target_symbols | AXISBANK;HDFCBANK;ICICIBANK;INFY;HCLTECH;TCS;RELIANCE | Frozen target symbols. |
| months | 2026-01;2026-02;2026-03 | Frozen months. |
| window_start_rows | 0;5000;10000;20000;50000 | Frozen candidate offsets to inspect. |
| feature_lookback_ticks | 20 | All features must end before entry tick. |
| entry_index | 20 | Entry tick index inside candidate window. |
| horizon_ticks | 240 | Forward return label horizon. |
| min_abs_forward_move_bps | 2.0 | Minimum non-flat forward move for positive/negative label inclusion. |
| primary_features | past_only_L1_L5_spread_imbalance_depth_shape_churn_and_recent_mid_return | L1-L5 features available for later fit. |
| label_columns | forward_return_bps;label_side;abs_forward_return_bps;move_candidate | Label columns to materialize. |
| allowed_outputs | label_ledger;feature_label_summary;gate_evaluation;manifest;report | No trading P&L output in Phase461. |
| forbidden | strategy_pnl;paper_live;deployable_profitability_claim;future_label_as_signal;threshold_tuning_after_label_result | Closed boundaries. |
| cost_model_reference | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Kept for downstream replay but not charged in label materialization. |
| capital_policy_reference | fixed_initial_capital_1000000_inr_order_notional_100000_inr_cost200 | Downstream replay denominator remains fixed. |
| execution_results_generated_now | 0 | Precommit only. |
| contract_hash | 7b867e82633d116b537ac27a6cf27d8ca4329283dc47db476bd11d79a21b2577 | Hash of frozen contract rows above. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P460_PHASE459_AVAILABLE | True | 1 | 1 | hard |
| P460_NEXT_ACTION_MATCHED | True | precommit_actual_move_candidate_label_source_or_pause_synthetic_fixed_window_routes | actual_move_candidate_label_source | hard |
| P460_DENSE_ROOT_PRESENT | True | 1 | 1 | hard |
| P460_SELECTED_FILES_PRESENT | True | 21 | 21 | hard |
| P460_MULTIPLE_OFFSETS_FROZEN | True | 5 | >=3 | hard |
| P460_LABEL_SOURCE_NOT_TRADABLE_SIGNAL | True | strategy_pnl;paper_live;deployable_profitability_claim;future_label_as_signal;threshold_tuning_after_label_result | future_label_as_signal_forbidden | hard |
| P460_PAST_ONLY_FEATURES_PRECOMMITTED | True | past_only_L1_L5_spread_imbalance_depth_shape_churn_and_recent_mid_return | past_only | hard |
| P460_NO_PNL_OUTPUTS | True | label_ledger;feature_label_summary;gate_evaluation;manifest;report | no_strategy_pnl | hard |
| P460_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P460_BOUNDARIES_CLOSED | True | strategy_pnl;paper_live;deployable_profitability_claim;future_label_as_signal;threshold_tuning_after_label_result | closed | hard |

Boundary: commit this precommit before Phase461 materializes labels. Phase461 must not emit P&L or acceptance as a strategy.

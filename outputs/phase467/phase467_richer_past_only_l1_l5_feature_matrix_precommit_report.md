# Phase467 Richer Past-Only L1-L5 Feature Matrix Precommit

Phase467 freezes a richer past-only L1-L5 feature matrix before any additional model fit or P&L replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase467_richer_past_only_l1_l5_feature_matrix_precommit_complete | 1 | Phase467 precommit completed |
| phase467_thesis_id | P467_RICHER_PAST_ONLY_L1_L5_FEATURE_MATRIX_PRECOMMIT | Precommit thesis |
| phase467_feature_count | 20 | Allowed feature count |
| phase467_l2_l5_feature_count | 9 | Features using levels 2-5 |
| phase467_selected_file_count | 21 | Selected files |
| phase467_selected_files_present | 21 | Present selected files |
| phase467_model_fit_generated | 0 | No model fit |
| phase467_strategy_pnl_generated | 0 | No strategy P&L |
| phase467_strategy_promotion_allowed | 0 | No promotion |
| phase467_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase467_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase467_phase468_allowed_next | 1 | Allows richer matrix materialization only if all gates pass |
| phase467_hard_gate_pass_rows | 10 | Passed hard gates |
| phase467_hard_gate_rows | 10 | Hard gates |
| phase467_next_best_action | run_phase468_materialize_richer_past_only_l1_l5_feature_matrix_no_model_no_pnl | Recommended next action |

## Frozen Phase468 Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| phase467_thesis_id | P467_RICHER_PAST_ONLY_L1_L5_FEATURE_MATRIX_PRECOMMIT | Precommit thesis |
| source_phase | phase462_phase463_distributional_label_source | Use same selected replacement source |
| input_dense_root | raw_synthetic_l2_phase162_distributional_full_year | Dense root |
| input_profile_id | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | Profile id |
| selected_file_count | 21 | Selected files |
| selected_file_hash | 14b16054c17f688680c32b4a378e7f74ee7e7c6b9ccc3cac0f627d9545a19315 | Selected files hash |
| required_schema_column_count | 39 | Required raw columns |
| lookback_ticks | 20 | Past-only lookback |
| entry_index | 20 | Entry row |
| horizon_ticks | 240 | Forward label horizon retained for labels only |
| min_abs_forward_move_bps | 2 | Move label floor |
| allowed_features | recent_mid_return_bps;spread_bps;l1_imbalance;l25_imbalance;volume_delta_lookback;l1_l5_bid_depth_slope;l1_l5_ask_depth_slope;l1_l5_depth_concentration;l25_order_imbalance;ofi_l1_lookback;ofi_l25_lookback;l25_replenishment_events;l25_withdrawal_events;microprice_l1_minus_mid_bps;microprice_l25_minus_mid_bps;spread_change_lookback_bps;spread_mean_lookback_bps;trade_qty_sum_lookback;trade_qty_accel_lookback;minute_of_day | Allowed richer features |
| l2_l5_feature_count | 9 | Features using levels 2-5 |
| forbidden_feature_columns | forward_return_bps;abs_forward_return_bps;label_side;move_candidate;exit_price;exit_row | Future/label columns forbidden as predictors |
| feature_contract_hash | ed5cfad137c17ad74a6c12256000a47fb6cc4c642eeed3d36fc1976a8d151793 | Feature contract hash |
| schema_evidence_hash | 803e8f5e7e476aa7a3c7c1543f6a09ea981425d7dd96fd7a74011104bf4d0f41 | Schema evidence hash |
| phase468_allowed_next | 1 | Allows matrix materialization only |
| model_fit_allowed | 0 | No model fit in Phase467/468 |
| strategy_pnl_allowed | 0 | No strategy P&L |
| strategy_promotion_allowed | 0 | No promotion |
| paper_or_live_acceptance_allowed | 0 | No paper/live |
| deployable_profitability_claim_allowed | 0 | No deployable claim |

## Feature Contract

| feature_name | feature_family | timestamp_rule | description | uses_l2_l5_depth | allowed_as_model_input |
| --- | --- | --- | --- | --- | --- |
| recent_mid_return_bps | base | computed only from rows <= entry row inside each candidate window | mid return from lookback start to entry | 0 | 1 |
| spread_bps | base | computed only from rows <= entry row inside each candidate window | entry best ask minus best bid in bps | 0 | 1 |
| l1_imbalance | base | computed only from rows <= entry row inside each candidate window | entry level-1 quantity imbalance | 0 | 1 |
| l25_imbalance | base | computed only from rows <= entry row inside each candidate window | entry levels 2-5 quantity imbalance | 1 | 1 |
| volume_delta_lookback | base | computed only from rows <= entry row inside each candidate window | entry volume minus lookback-start volume | 0 | 1 |
| l1_l5_bid_depth_slope | depth_curve_shape | computed only from rows <= entry row inside each candidate window | entry bid quantity slope over levels 1-5 | 1 | 1 |
| l1_l5_ask_depth_slope | depth_curve_shape | computed only from rows <= entry row inside each candidate window | entry ask quantity slope over levels 1-5 | 1 | 1 |
| l1_l5_depth_concentration | depth_curve_shape | computed only from rows <= entry row inside each candidate window | entry L1 depth share of total L1-L5 depth | 1 | 1 |
| l25_order_imbalance | depth_curve_shape | computed only from rows <= entry row inside each candidate window | entry levels 2-5 order-count imbalance | 1 | 1 |
| ofi_l1_lookback | ofi_and_depth_churn | computed only from rows <= entry row inside each candidate window | signed L1 quantity change over lookback | 0 | 1 |
| ofi_l25_lookback | ofi_and_depth_churn | computed only from rows <= entry row inside each candidate window | signed levels 2-5 quantity change over lookback | 1 | 1 |
| l25_replenishment_events | ofi_and_depth_churn | computed only from rows <= entry row inside each candidate window | count of positive levels 2-5 depth changes before entry | 1 | 1 |
| l25_withdrawal_events | ofi_and_depth_churn | computed only from rows <= entry row inside each candidate window | count of negative levels 2-5 depth changes before entry | 1 | 1 |
| microprice_l1_minus_mid_bps | microprice_pressure | computed only from rows <= entry row inside each candidate window | L1 microprice displacement from mid at entry | 0 | 1 |
| microprice_l25_minus_mid_bps | microprice_pressure | computed only from rows <= entry row inside each candidate window | levels 2-5 microprice displacement from mid at entry | 1 | 1 |
| spread_change_lookback_bps | spread_regime_context | computed only from rows <= entry row inside each candidate window | entry spread minus lookback-start spread | 0 | 1 |
| spread_mean_lookback_bps | spread_regime_context | computed only from rows <= entry row inside each candidate window | mean spread over past-only lookback | 0 | 1 |
| trade_qty_sum_lookback | volume_acceleration | computed only from rows <= entry row inside each candidate window | sum last_traded_quantity over lookback | 0 | 1 |
| trade_qty_accel_lookback | volume_acceleration | computed only from rows <= entry row inside each candidate window | second-half minus first-half traded quantity over lookback | 0 | 1 |
| minute_of_day | time_of_day_context | computed only from rows <= entry row inside each candidate window | known exchange timestamp minute bucket | 0 | 1 |

## Schema Evidence

| path | exists | schema_columns | missing_required_columns |
| --- | --- | --- | --- |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=AXISBANK\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=ICICIBANK\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=INFY\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=HCLTECH\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=TCS\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=RELIANCE\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=AXISBANK\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=HDFCBANK\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=ICICIBANK\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=INFY\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=HCLTECH\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=TCS\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=RELIANCE\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=AXISBANK\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=HDFCBANK\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=ICICIBANK\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=INFY\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=HCLTECH\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=TCS\part-00000.parquet | 1 | 64 |  |
| raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=RELIANCE\part-00000.parquet | 1 | 64 |  |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P467_PHASE466_RICHER_FEATURE_PRECOMMIT_ALLOWED | True | 1 | 1 | hard |
| P467_SELECTED_FILES_PRESENT | True | 21 | 21 | hard |
| P467_REQUIRED_SCHEMA_PRESENT | True | 21 | 21 | hard |
| P467_FEATURE_COUNT_GE_20 | True | 20 | >=20 | hard |
| P467_L2_L5_FEATURE_COUNT_GE_8 | True | 9 | >=8 | hard |
| P467_BASE_PHASE465_FEATURES_RETAINED | True | l1_imbalance;l1_l5_ask_depth_slope;l1_l5_bid_depth_slope;l1_l5_depth_concentration;l25_imbalance;l25_order_imbalance;l25_replenishment_events;l25_withdrawal_events;microprice_l1_minus_mid_bps;microprice_l25_minus_mid_bps;minute_of_day;ofi_l1_lookback;ofi_l25_lookback;recent_mid_return_bps;spread_bps;spread_change_lookback_bps;spread_mean_lookback_bps;trade_qty_accel_lookback;trade_qty_sum_lookback;volume_delta_lookback | base features included | hard |
| P467_FORBIDDEN_LABELS_NOT_FEATURES | True |  | empty | hard |
| P467_MODEL_FIT_NOT_ALLOWED | True | precommit_only | no_model_fit | hard |
| P467_NO_STRATEGY_PNL | True | precommit_only | no_pnl | hard |
| P467_NO_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: Phase468 may materialize the richer matrix only. Model fitting and strategy P&L remain closed.

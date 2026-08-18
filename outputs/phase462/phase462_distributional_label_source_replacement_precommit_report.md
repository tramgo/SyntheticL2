# Phase462 Distributional Label-Source Replacement Precommit

Phase462 responds to Phase461's flat-label finding by freezing a replacement label source: the Phase162/P159 distributional full-year L1-L5 lake. It does not run strategy P&L.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase462_distributional_label_source_replacement_precommit_complete | 1 | Phase462 precommit completed |
| phase462_thesis_id | P462_DISTRIBUTIONAL_LABEL_SOURCE_REPLACEMENT_PRECOMMIT | Precommit thesis |
| phase462_selected_source_id | phase162_p159_distributional_full_year_l1_l5_replacement_for_flat_phase461_source | Selected replacement source |
| phase462_replacement_profile_id | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | Replacement profile |
| phase462_replacement_selected_files | 21 | Frozen selected files |
| phase462_replacement_files_present | 21 | Present files |
| phase462_execution_results_generated | 0 | Precommit only |
| phase462_strategy_pnl_generated | 0 | No strategy P&L |
| phase462_strategy_promotion_allowed | 0 | No promotion |
| phase462_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase462_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase462_phase463_allowed_next | 1 | Allows Phase463 label materialization only if all gates pass |
| phase462_hard_gate_pass_rows | 12 | Passed hard gates |
| phase462_hard_gate_rows | 12 | Hard gates |
| phase462_next_best_action | run_phase463_actual_move_label_materialization_on_phase162_distributional_l1_l5_no_pnl | Recommended next action |

## Input Evidence

| evidence_id | observed_value | description |
| --- | --- | --- |
| phase461_next_action | pause_or_repair_synthetic_generator_non_flat_move_distribution_before_strategy_replay | Phase461 requested repair/replacement after flat labels |
| phase461_move_candidate_rows | 0.0 | Flat-source move candidates |
| phase461_long_label_rows | 0.0 | Flat-source long labels |
| phase461_short_label_rows | 0.0 | Flat-source short labels |
| phase162_profile_id | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | Distributional profile evidence |
| phase162_months_materialized | 12 | Materialized months |
| phase162_symbols_materialized | 32 | Materialized symbols |
| phase162_partition_files | 384 | Distributional partition files |
| phase162_expected_partition_files | 384 | Expected partition files |
| phase162_missing_partition_files | 0 | Missing partition files |
| phase162_full_year_realism_audit_pass | 1 | Realism audit pass |
| phase162_strategy_replay_allowed | 0 | Replay remained closed in Phase162 |
| replacement_profile_root_exists | 1 | Replacement profile root |
| selected_files_present | 21 | Selected replacement files present |
| selected_files_expected | 21 | Selected replacement files expected |
| selected_files_bytes | 228838666 | Selected replacement bytes |

## Frozen Phase463 Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| phase462_thesis_id | P462_DISTRIBUTIONAL_LABEL_SOURCE_REPLACEMENT_PRECOMMIT | Precommit thesis |
| selected_source_id | phase162_p159_distributional_full_year_l1_l5_replacement_for_flat_phase461_source | Replacement label source |
| prior_flat_source_root | raw_synthetic_l2_dense_full_year | Phase461 source that produced zero non-flat labels |
| replacement_dense_root | raw_synthetic_l2_phase162_distributional_full_year | Distributional full-year dense root |
| replacement_profile_id | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | Distributional profile |
| target_symbols | AXISBANK;HDFCBANK;ICICIBANK;INFY;HCLTECH;TCS;RELIANCE | Target symbols |
| months | 2026-01;2026-02;2026-03 | Target months |
| window_start_rows | 0;5000;10000;20000;50000 | Candidate start rows |
| entry_index | 20 | Entry row inside each candidate window |
| horizon_ticks | 240 | Forward label horizon |
| min_abs_forward_move_bps | 2 | Actual-move floor |
| selected_file_count | 21 | Frozen replacement file count |
| selected_file_hash | 14b16054c17f688680c32b4a378e7f74ee7e7c6b9ccc3cac0f627d9545a19315 | Hash of replacement file registry |
| phase463_allowed_next | 1 | Allows label materialization only |
| strategy_pnl_allowed | 0 | No P&L in Phase462 or Phase463 label materialization |
| strategy_promotion_allowed | 0 | No promotion |
| paper_or_live_acceptance_allowed | 0 | No paper/live |
| deployable_profitability_claim_allowed | 0 | No deployable claim |

## Selected Replacement Files

| trade_month | symbol | profile_id | path | exists | bytes |
| --- | --- | --- | --- | --- | --- |
| 2026-01 | AXISBANK | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=AXISBANK\part-00000.parquet | 1 | 11096622 |
| 2026-01 | HDFCBANK | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | 1 | 11278095 |
| 2026-01 | ICICIBANK | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=ICICIBANK\part-00000.parquet | 1 | 11088317 |
| 2026-01 | INFY | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=INFY\part-00000.parquet | 1 | 11196406 |
| 2026-01 | HCLTECH | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=HCLTECH\part-00000.parquet | 1 | 11229206 |
| 2026-01 | TCS | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=TCS\part-00000.parquet | 1 | 11127884 |
| 2026-01 | RELIANCE | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-01\symbol=RELIANCE\part-00000.parquet | 1 | 11252173 |
| 2026-02 | AXISBANK | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=AXISBANK\part-00000.parquet | 1 | 10301608 |
| 2026-02 | HDFCBANK | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=HDFCBANK\part-00000.parquet | 1 | 10383586 |
| 2026-02 | ICICIBANK | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=ICICIBANK\part-00000.parquet | 1 | 10344892 |
| 2026-02 | INFY | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=INFY\part-00000.parquet | 1 | 10312444 |
| 2026-02 | HCLTECH | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=HCLTECH\part-00000.parquet | 1 | 10357513 |
| 2026-02 | TCS | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=TCS\part-00000.parquet | 1 | 10246711 |
| 2026-02 | RELIANCE | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-02\symbol=RELIANCE\part-00000.parquet | 1 | 10421315 |
| 2026-03 | AXISBANK | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=AXISBANK\part-00000.parquet | 1 | 11166915 |
| 2026-03 | HDFCBANK | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=HDFCBANK\part-00000.parquet | 1 | 11077658 |
| 2026-03 | ICICIBANK | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=ICICIBANK\part-00000.parquet | 1 | 11136064 |
| 2026-03 | INFY | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=INFY\part-00000.parquet | 1 | 11149524 |
| 2026-03 | HCLTECH | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=HCLTECH\part-00000.parquet | 1 | 11213424 |
| 2026-03 | TCS | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=TCS\part-00000.parquet | 1 | 11114037 |
| 2026-03 | RELIANCE | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE\trade_month=2026-03\symbol=RELIANCE\part-00000.parquet | 1 | 11344272 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P462_PHASE461_REPAIR_REQUESTED | True | pause_or_repair_synthetic_generator_non_flat_move_distribution_before_strategy_replay | repair_or_replace_after_flat_labels | hard |
| P462_PHASE461_ZERO_MOVE_CANDIDATES_CONFIRMED | True | 0.0 | 0 | hard |
| P462_PHASE162_DISTRIBUTIONAL_PROFILE_SELECTED | True | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | hard |
| P462_PHASE162_FULL_YEAR_SCOPE_COMPLETE | True | months=12;symbols=32 | months>=12;symbols>=32 | hard |
| P462_PHASE162_NO_MISSING_PARTITIONS | True | 0 | 0 | hard |
| P462_PHASE162_REALISM_AUDIT_PASSED | True | 1 | 1 | hard |
| P462_PHASE162_REPLAY_WAS_CLOSED | True | 0 | 0 | hard |
| P462_REPLACEMENT_PROFILE_ROOT_PRESENT | True | raw_synthetic_l2_phase162_distributional_full_year\profile=P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE | exists | hard |
| P462_SELECTED_FILES_PRESENT | True | 21 | 21 | hard |
| P462_LABEL_ONLY_NEXT | True | run_phase463_actual_move_label_materialization_on_phase162_distributional_l1_l5_no_pnl | label_materialization_only | hard |
| P462_NO_STRATEGY_PNL | True | precommit_only | no_pnl | hard |
| P462_NO_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: Phase463 may materialize actual-move labels from the replacement source only. Strategy replay, promotion, paper/live and deployable profitability claims remain closed.

# Phase463 Distributional Actual-Move Label Materialization

Phase463 materializes actual non-flat forward-move labels on the Phase162/P159 distributional full-year L1-L5 source. It emits no strategy P&L and makes no acceptance claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase463_distributional_actual_move_label_materialization_complete | 1 | Phase463 label materialization completed |
| phase463_thesis_id | P463_DISTRIBUTIONAL_ACTUAL_MOVE_LABEL_MATERIALIZATION | Label materialization thesis |
| phase463_label_rows | 1792 | All materialized label rows |
| phase463_move_candidate_rows | 935 | Rows passing non-flat move floor |
| phase463_trade_dates | 64 | Dates with labels |
| phase463_symbols | 7 | Symbols with labels |
| phase463_long_label_rows | 943 | Long forward labels |
| phase463_short_label_rows | 838 | Short forward labels |
| phase463_strategy_pnl_generated | 0 | No P&L generated |
| phase463_strategy_promotion_allowed | 0 | No promotion |
| phase463_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase463_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase463_phase464_allowed_next | 1 | Allows past-only L2 feature-model precommit only if all gates pass |
| phase463_hard_gate_pass_rows | 11 | Passed hard gates |
| phase463_hard_gate_rows | 11 | Hard gates |
| phase463_next_best_action | precommit_phase464_past_only_l2_feature_model_on_distributional_actual_move_candidates | Recommended next action |

## Label Summary

| metric | value |
| --- | --- |
| selected_files | 21 |
| files_present | 21 |
| label_rows | 1792 |
| move_candidate_rows | 935 |
| trade_dates | 64 |
| symbols | 7 |
| long_label_rows | 943 |
| short_label_rows | 838 |
| flat_label_rows | 11 |
| median_abs_forward_return_bps | 2.09403 |
| max_abs_forward_return_bps | 24.188 |
| median_spread_bps | 1.80884 |
| median_l25_imbalance_abs | 0.294285 |

## Label Side Summary

| label_side | rows | move_candidate_rows | median_forward_return_bps | median_abs_forward_return_bps |
| --- | --- | --- | --- | --- |
| flat | 11 | 0 | 0 | 0 |
| long | 943 | 522 | 2.33663 | 2.33663 |
| short | 838 | 413 | -1.96132 | 1.96132 |

## Symbol Summary

| symbol | trade_dates | label_rows | move_candidate_rows | long_rows | short_rows | max_abs_forward_return_bps |
| --- | --- | --- | --- | --- | --- | --- |
| AXISBANK | 64 | 256 | 126 | 141 | 113 | 17.7845 |
| HCLTECH | 64 | 256 | 140 | 130 | 124 | 24.188 |
| HDFCBANK | 64 | 256 | 145 | 135 | 120 | 18.3857 |
| ICICIBANK | 64 | 256 | 130 | 137 | 118 | 13.6998 |
| INFY | 64 | 256 | 131 | 129 | 125 | 22.2995 |
| RELIANCE | 64 | 256 | 128 | 142 | 111 | 20.2096 |
| TCS | 64 | 256 | 135 | 129 | 127 | 21.6224 |

## Selected Files

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
| P463_PHASE462_PRECOMMIT_USED | True | 1 | 1 | hard |
| P463_SELECTED_FILES_PRESENT | True | 21 | 21 | hard |
| P463_LABEL_ROWS_PRESENT | True | 1792 | >0 | hard |
| P463_MOVE_CANDIDATES_PRESENT | True | 935 | >0 | hard |
| P463_DATE_BREADTH_GE_5 | True | 64 | >=5 | hard |
| P463_SYMBOL_BREADTH_GE_3 | True | 7 | >=3 | hard |
| P463_LONG_LABELS_PRESENT | True | 943 | >0 | hard |
| P463_SHORT_LABELS_PRESENT | True | 838 | >0 | hard |
| P463_FULL_DEPTH_FEATURE_COLUMNS_PRESENT | True | 0.294285 | computed_from_L2_L5 | hard |
| P463_NO_STRATEGY_PNL | True | label_materialization_only | no_pnl | hard |
| P463_NO_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: labels are research labels only. Phase464 must precommit any past-only feature model before strategy P&L exists.

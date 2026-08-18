# Phase461 Actual-Move Candidate Label Materialization

Phase461 materializes actual non-flat forward-move labels from dense raw L1-L5 data. It emits no P&L and makes no strategy acceptance claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase461_actual_move_label_materialization_complete | 1 | Phase461 label materialization completed |
| phase461_thesis_id | P461_ACTUAL_MOVE_CANDIDATE_LABEL_MATERIALIZATION | Label materialization thesis |
| phase461_label_rows | 2240 | All materialized label rows |
| phase461_move_candidate_rows | 0 | Rows passing non-flat move floor |
| phase461_trade_dates | 64 | Dates with labels |
| phase461_symbols | 7 | Symbols with labels |
| phase461_long_label_rows | 0 | Long forward labels |
| phase461_short_label_rows | 0 | Short forward labels |
| phase461_strategy_pnl_generated | 0 | No P&L generated |
| phase461_strategy_promotion_allowed | 0 | No promotion |
| phase461_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase461_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase461_hard_gate_pass_rows | 7 | Passed hard gates |
| phase461_hard_gate_rows | 9 | Hard gates |
| phase461_next_best_action | pause_or_repair_synthetic_generator_non_flat_move_distribution_before_strategy_replay | Recommended next action |

## Label Summary

| metric | value |
| --- | --- |
| selected_files | 21 |
| files_present | 21 |
| label_rows | 2240 |
| move_candidate_rows | 0 |
| trade_dates | 64 |
| symbols | 7 |
| long_label_rows | 0 |
| short_label_rows | 0 |
| flat_label_rows | 2240 |
| median_abs_forward_return_bps | 0 |
| max_abs_forward_return_bps | 0 |

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

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P461_PHASE460_PRECOMMIT_USED | True | 1 | 1 | hard |
| P461_SELECTED_FILES_PRESENT | True | 21 | 21 | hard |
| P461_LABEL_ROWS_PRESENT | True | 2240 | >0 | hard |
| P461_MOVE_CANDIDATES_PRESENT | False | 0 | >0 | hard |
| P461_DATE_BREADTH_GE_5 | True | 64 | >=5 | hard |
| P461_SYMBOL_BREADTH_GE_3 | True | 7 | >=3 | hard |
| P461_LONG_OR_SHORT_LABELS_PRESENT | False | long=0.0;short=0.0 | >0 | hard |
| P461_NO_STRATEGY_PNL | True | label_materialization_only | no_pnl | hard |
| P461_NO_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: actual forward move labels are research labels only. A later phase must precommit past-only modeling/replay before any strategy P&L.

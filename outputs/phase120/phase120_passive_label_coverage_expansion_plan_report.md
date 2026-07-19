# Phase120 Passive Label Coverage Expansion Plan

Generated UTC: 2026-07-19T23:12:54.630330+00:00

Phase120 converts the Phase119 breadth failure into a staged label-only coverage plan.
It does not open replay. It identifies how to expand passive labels from the current one-month run toward four-month, train-half, and full-year label coverage.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase120_dense_shards_available | 384 | Dense full-year symbol/month shards available |
| phase120_current_label_months | 1 | Months currently covered by passive labels |
| phase120_dense_months_available | 12 | Months available in dense lake |
| phase120_phase119_pre_replay_candidate_rows | 0 | Current Phase119 pre-replay candidates passing all gates |
| phase120_stage_plan_rows | 3 | Label-only expansion stages emitted |
| phase120_next_stage_limit_shards | 128 | Recommended next label-only expansion shard limit |
| phase120_label_expansion_allowed | 1 | 1 means label coverage can expand without replay |
| phase120_replay_allowed | 0 | Replay remains closed |
| phase120_next_best_action | run_phase120_stage_01_label_only_expansion_then_rerun_phase119_on_expanded_labels | Recommended next milestone |

## Coverage Summary

| metric | value | description |
| --- | --- | --- |
| phase120_dense_shard_rows | 384 | Dense full-year symbol/month parquet shards available |
| phase120_dense_months | 12 | Distinct dense trade_month partitions available |
| phase120_dense_symbols | 32 | Distinct dense symbols available |
| phase120_current_label_source_rows | 96 | Current passive label inventory rows across Phase66/68/69 |
| phase120_current_label_months | 1 | Distinct trade_month partitions already labeled by passive label stages |
| phase120_current_label_symbols | 32 | Distinct symbols already labeled by passive label stages |
| phase120_phase119_max_joined_symbols | 3 | Max symbols in Phase119 joined candidates |
| phase120_phase119_max_joined_trade_dates | 1 | Max trade dates in Phase119 joined candidates |
| phase120_label_breadth_gap_symbols | 17 | Additional joined-candidate symbol breadth needed for Phase119 gate |
| phase120_label_breadth_gap_trade_dates | 3 | Additional joined-candidate trade-date breadth needed for Phase119 gate |

## Passive Label Expansion Stage Plan

| stage_id | limit_shards | expected_months | purpose | expected_symbols | expected_trade_months_from_manifest | phase66_command | phase68_command | phase69_command | phase119_command_after_labels | run_now_recommended |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P120_LABEL_STAGE_01_MIN_BREADTH | 128 | 2026-01\|2026-02\|2026-03\|2026-04 | Expand passive labels from one month to four months across the 32-symbol universe. | 32 | 4 | python scripts/run_phase66_passive_adverse_selection_labels.py --limit-shards 128 --output-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase66 | python scripts/run_phase68_replenishment_after_touch_labels.py --limit-shards 128 --output-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase68 | python scripts/run_phase69_spread_transition_labels.py --limit-shards 128 --output-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase69 | python scripts/run_phase119_richer_passive_label_builder.py --phase66-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase66 --phase68-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase68 --phase69-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase69 --output-dir outputs/phase120/P120_LABEL_STAGE_01_MIN_BREADTH/phase119 | True |
| P120_LABEL_STAGE_02_TRAIN_HALF | 192 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | Cover the train half of the synthetic year for pre-replay label stability. | 32 | 6 | python scripts/run_phase66_passive_adverse_selection_labels.py --limit-shards 192 --output-dir outputs/phase120/P120_LABEL_STAGE_02_TRAIN_HALF/phase66 | python scripts/run_phase68_replenishment_after_touch_labels.py --limit-shards 192 --output-dir outputs/phase120/P120_LABEL_STAGE_02_TRAIN_HALF/phase68 | python scripts/run_phase69_spread_transition_labels.py --limit-shards 192 --output-dir outputs/phase120/P120_LABEL_STAGE_02_TRAIN_HALF/phase69 | python scripts/run_phase119_richer_passive_label_builder.py --phase66-dir outputs/phase120/P120_LABEL_STAGE_02_TRAIN_HALF/phase66 --phase68-dir outputs/phase120/P120_LABEL_STAGE_02_TRAIN_HALF/phase68 --phase69-dir outputs/phase120/P120_LABEL_STAGE_02_TRAIN_HALF/phase69 --output-dir outputs/phase120/P120_LABEL_STAGE_02_TRAIN_HALF/phase119 | False |
| P120_LABEL_STAGE_03_FULL_YEAR_LABELS | 384 | 2026-01..2026-12 | Full-year label-only coverage if Stage 01/02 improve adverse-selection and breadth gates. | 32 | 12 | python scripts/run_phase66_passive_adverse_selection_labels.py --limit-shards 384 --output-dir outputs/phase120/P120_LABEL_STAGE_03_FULL_YEAR_LABELS/phase66 | python scripts/run_phase68_replenishment_after_touch_labels.py --limit-shards 384 --output-dir outputs/phase120/P120_LABEL_STAGE_03_FULL_YEAR_LABELS/phase68 | python scripts/run_phase69_spread_transition_labels.py --limit-shards 384 --output-dir outputs/phase120/P120_LABEL_STAGE_03_FULL_YEAR_LABELS/phase69 | python scripts/run_phase119_richer_passive_label_builder.py --phase66-dir outputs/phase120/P120_LABEL_STAGE_03_FULL_YEAR_LABELS/phase66 --phase68-dir outputs/phase120/P120_LABEL_STAGE_03_FULL_YEAR_LABELS/phase68 --phase69-dir outputs/phase120/P120_LABEL_STAGE_03_FULL_YEAR_LABELS/phase69 --output-dir outputs/phase120/P120_LABEL_STAGE_03_FULL_YEAR_LABELS/phase119 | False |

## Top Month/Symbol Targets

| sorted_shard_index | trade_month | symbol | shard_path | already_labeled_by_any_passive_stage | target_priority |
| --- | --- | --- | --- | --- | --- |
| 33 | 2026-02 | ADANIPORTS | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ADANIPORTS\part-00000.parquet | False | 1 |
| 34 | 2026-02 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=AXISBANK\part-00000.parquet | False | 1 |
| 35 | 2026-02 | BAJAJ-AUTO | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=BAJAJ-AUTO\part-00000.parquet | False | 1 |
| 36 | 2026-02 | BANKBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=BANKBEES\part-00000.parquet | False | 1 |
| 37 | 2026-02 | BHARTIARTL | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=BHARTIARTL\part-00000.parquet | False | 1 |
| 38 | 2026-02 | BPCL | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=BPCL\part-00000.parquet | False | 1 |
| 39 | 2026-02 | BRITANNIA | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=BRITANNIA\part-00000.parquet | False | 1 |
| 40 | 2026-02 | CIPLA | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=CIPLA\part-00000.parquet | False | 1 |
| 41 | 2026-02 | DRREDDY | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=DRREDDY\part-00000.parquet | False | 1 |
| 42 | 2026-02 | GOLDBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=GOLDBEES\part-00000.parquet | False | 1 |
| 43 | 2026-02 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=HCLTECH\part-00000.parquet | False | 1 |
| 44 | 2026-02 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=HDFCBANK\part-00000.parquet | False | 1 |
| 45 | 2026-02 | HINDUNILVR | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=HINDUNILVR\part-00000.parquet | False | 1 |
| 46 | 2026-02 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ICICIBANK\part-00000.parquet | False | 1 |
| 47 | 2026-02 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=INFY\part-00000.parquet | False | 1 |
| 48 | 2026-02 | ITBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ITBEES\part-00000.parquet | False | 1 |
| 49 | 2026-02 | ITC | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ITC\part-00000.parquet | False | 1 |
| 50 | 2026-02 | JUNIORBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=JUNIORBEES\part-00000.parquet | False | 1 |
| 51 | 2026-02 | KOTAKBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=KOTAKBANK\part-00000.parquet | False | 1 |
| 52 | 2026-02 | LT | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=LT\part-00000.parquet | False | 1 |
| 53 | 2026-02 | M&M | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=M&M\part-00000.parquet | False | 1 |
| 54 | 2026-02 | MARUTI | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=MARUTI\part-00000.parquet | False | 1 |
| 55 | 2026-02 | NESTLEIND | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=NESTLEIND\part-00000.parquet | False | 1 |
| 56 | 2026-02 | NIFTYBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=NIFTYBEES\part-00000.parquet | False | 1 |
| 57 | 2026-02 | ONGC | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ONGC\part-00000.parquet | False | 1 |
| 58 | 2026-02 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=RELIANCE\part-00000.parquet | False | 1 |
| 59 | 2026-02 | SBIN | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=SBIN\part-00000.parquet | False | 1 |
| 60 | 2026-02 | SUNPHARMA | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=SUNPHARMA\part-00000.parquet | False | 1 |
| 61 | 2026-02 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=TCS\part-00000.parquet | False | 1 |
| 62 | 2026-02 | TECHM | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=TECHM\part-00000.parquet | False | 1 |
| 63 | 2026-02 | ULTRACEMCO | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=ULTRACEMCO\part-00000.parquet | False | 1 |
| 64 | 2026-02 | WIPRO | raw_synthetic_l2_dense_full_year\trade_month=2026-02\symbol=WIPRO\part-00000.parquet | False | 1 |
| 65 | 2026-03 | ADANIPORTS | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ADANIPORTS\part-00000.parquet | False | 1 |
| 66 | 2026-03 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=AXISBANK\part-00000.parquet | False | 1 |
| 67 | 2026-03 | BAJAJ-AUTO | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=BAJAJ-AUTO\part-00000.parquet | False | 1 |
| 68 | 2026-03 | BANKBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=BANKBEES\part-00000.parquet | False | 1 |
| 69 | 2026-03 | BHARTIARTL | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=BHARTIARTL\part-00000.parquet | False | 1 |
| 70 | 2026-03 | BPCL | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=BPCL\part-00000.parquet | False | 1 |
| 71 | 2026-03 | BRITANNIA | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=BRITANNIA\part-00000.parquet | False | 1 |
| 72 | 2026-03 | CIPLA | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=CIPLA\part-00000.parquet | False | 1 |
| 73 | 2026-03 | DRREDDY | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=DRREDDY\part-00000.parquet | False | 1 |
| 74 | 2026-03 | GOLDBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=GOLDBEES\part-00000.parquet | False | 1 |
| 75 | 2026-03 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=HCLTECH\part-00000.parquet | False | 1 |
| 76 | 2026-03 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=HDFCBANK\part-00000.parquet | False | 1 |
| 77 | 2026-03 | HINDUNILVR | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=HINDUNILVR\part-00000.parquet | False | 1 |
| 78 | 2026-03 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ICICIBANK\part-00000.parquet | False | 1 |
| 79 | 2026-03 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=INFY\part-00000.parquet | False | 1 |
| 80 | 2026-03 | ITBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ITBEES\part-00000.parquet | False | 1 |
| 81 | 2026-03 | ITC | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ITC\part-00000.parquet | False | 1 |
| 82 | 2026-03 | JUNIORBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=JUNIORBEES\part-00000.parquet | False | 1 |
| 83 | 2026-03 | KOTAKBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=KOTAKBANK\part-00000.parquet | False | 1 |
| 84 | 2026-03 | LT | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=LT\part-00000.parquet | False | 1 |
| 85 | 2026-03 | M&M | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=M&M\part-00000.parquet | False | 1 |
| 86 | 2026-03 | MARUTI | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=MARUTI\part-00000.parquet | False | 1 |
| 87 | 2026-03 | NESTLEIND | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=NESTLEIND\part-00000.parquet | False | 1 |
| 88 | 2026-03 | NIFTYBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=NIFTYBEES\part-00000.parquet | False | 1 |
| 89 | 2026-03 | ONGC | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ONGC\part-00000.parquet | False | 1 |
| 90 | 2026-03 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=RELIANCE\part-00000.parquet | False | 1 |
| 91 | 2026-03 | SBIN | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=SBIN\part-00000.parquet | False | 1 |
| 92 | 2026-03 | SUNPHARMA | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=SUNPHARMA\part-00000.parquet | False | 1 |
| 93 | 2026-03 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=TCS\part-00000.parquet | False | 1 |
| 94 | 2026-03 | TECHM | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=TECHM\part-00000.parquet | False | 1 |
| 95 | 2026-03 | ULTRACEMCO | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=ULTRACEMCO\part-00000.parquet | False | 1 |
| 96 | 2026-03 | WIPRO | raw_synthetic_l2_dense_full_year\trade_month=2026-03\symbol=WIPRO\part-00000.parquet | False | 1 |

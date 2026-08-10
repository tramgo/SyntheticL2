# Phase307 Event-Catalyst Top-Five Depth Join Materialization

Phase307 attempts to materialize the Phase306 event-catalyst to top-five depth join. It records timestamp coverage explicitly and does not run strategy search.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase307_join_materialization_complete | 1 | Phase307 event-catalyst top-five depth join materialization completed |
| phase307_work_order_rows | 32 | Event-symbol work-order rows audited |
| phase307_timestamp_overlap_rows | 0 | Event-symbol rows whose dense file overlaps event window |
| phase307_materialized_join_rows | 0 | Joined top-five depth rows materialized |
| phase307_materialized_symbols | 0 | Symbols with joined rows |
| phase307_full_depth_columns_present | 1 | Depth levels 1-5 price/quantity/order columns retained |
| phase307_strategy_search_allowed_now | 0 | No strategy search in Phase307 |
| phase307_strategy_replay_allowed | 0 | No replay |
| phase307_strategy_promotion_allowed | 0 | No promotion |
| phase307_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase307_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase307_hard_gate_pass_rows | 7 | Passed hard gates |
| phase307_hard_gate_rows | 7 | Hard gates |
| phase307_next_best_action | add_event_catalyst_with_timestamp_overlapping_dense_lake_or_recalendarize_synthetic_event_time_then_rerun_phase307 | Recommended next action |

## Coverage audit

| event_id | symbol | dense_file_path | file_exists | file_min_epoch | file_max_epoch | window_start_epoch | window_end_epoch | timestamp_overlap | materialized_rows | source_rows | row_groups |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P306_EVT_0001 | ADANIPORTS | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ADANIPORTS\part-00000.parquet | 1 | 1787130875 | 1789579457 | 1785903300 | 1785906000 | 0 | 0 | 15549968 | 31 |
| P306_EVT_0001 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=AXISBANK\part-00000.parquet | 1 | 1787130875 | 1789583957 | 1785903300 | 1785906000 | 0 | 0 | 15555918 | 31 |
| P306_EVT_0001 | BAJAJ-AUTO | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BAJAJ-AUTO\part-00000.parquet | 1 | 1787130875 | 1789580957 | 1785903300 | 1785906000 | 0 | 0 | 15542034 | 31 |
| P306_EVT_0001 | BANKBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BANKBEES\part-00000.parquet | 1 | 1787130875 | 1789582957 | 1785903300 | 1785906000 | 0 | 0 | 15557902 | 31 |
| P306_EVT_0001 | BHARTIARTL | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BHARTIARTL\part-00000.parquet | 1 | 1787130875 | 1789581957 | 1785903300 | 1785906000 | 0 | 0 | 15575752 | 31 |
| P306_EVT_0001 | BPCL | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BPCL\part-00000.parquet | 1 | 1787130725 | 1789588457 | 1785903300 | 1785906000 | 0 | 0 | 15512283 | 31 |
| P306_EVT_0001 | BRITANNIA | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BRITANNIA\part-00000.parquet | 1 | 1787130875 | 1789584457 | 1785903300 | 1785906000 | 0 | 0 | 15561869 | 31 |
| P306_EVT_0001 | CIPLA | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=CIPLA\part-00000.parquet | 1 | 1787130875 | 1789593457 | 1785903300 | 1785906000 | 0 | 0 | 15549968 | 31 |
| P306_EVT_0001 | DRREDDY | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=DRREDDY\part-00000.parquet | 1 | 1787130875 | 1789584957 | 1785903300 | 1785906000 | 0 | 0 | 15563852 | 31 |
| P306_EVT_0001 | GOLDBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=GOLDBEES\part-00000.parquet | 1 | 1787130875 | 1789579457 | 1785903300 | 1785906000 | 0 | 0 | 15551951 | 31 |
| P306_EVT_0001 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=HCLTECH\part-00000.parquet | 1 | 1787130875 | 1789585457 | 1785903300 | 1785906000 | 0 | 0 | 15575752 | 31 |
| P306_EVT_0001 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=HDFCBANK\part-00000.parquet | 1 | 1787130875 | 1789586189 | 1785903300 | 1785906000 | 0 | 0 | 15551951 | 31 |
| P306_EVT_0001 | HINDUNILVR | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=HINDUNILVR\part-00000.parquet | 1 | 1787130875 | 1789597457 | 1785903300 | 1785906000 | 0 | 0 | 15542034 | 31 |
| P306_EVT_0001 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ICICIBANK\part-00000.parquet | 1 | 1787130875 | 1789582957 | 1785903300 | 1785906000 | 0 | 0 | 15569802 | 31 |
| P306_EVT_0001 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=INFY\part-00000.parquet | 1 | 1787130875 | 1789581957 | 1785903300 | 1785906000 | 0 | 0 | 15565835 | 31 |
| P306_EVT_0001 | ITBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ITBEES\part-00000.parquet | 1 | 1787130875 | 1789580457 | 1785903300 | 1785906000 | 0 | 0 | 15551951 | 31 |
| P306_EVT_0001 | ITC | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ITC\part-00000.parquet | 1 | 1787130875 | 1789576957 | 1785903300 | 1785906000 | 0 | 0 | 15577736 | 31 |
| P306_EVT_0001 | JUNIORBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=JUNIORBEES\part-00000.parquet | 1 | 1787130875 | 1789581957 | 1785903300 | 1785906000 | 0 | 0 | 15547985 | 31 |
| P306_EVT_0001 | KOTAKBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=KOTAKBANK\part-00000.parquet | 1 | 1787130475 | 1789596457 | 1785903300 | 1785906000 | 0 | 0 | 15557902 | 31 |
| P306_EVT_0001 | LT | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=LT\part-00000.parquet | 1 | 1787130875 | 1789596707 | 1785903300 | 1785906000 | 0 | 0 | 15581703 | 31 |
| P306_EVT_0001 | M&M | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=M&M\part-00000.parquet | 1 | 1787130875 | 1789595957 | 1785903300 | 1785906000 | 0 | 0 | 15565835 | 31 |
| P306_EVT_0001 | MARUTI | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=MARUTI\part-00000.parquet | 1 | 1787130875 | 1789595457 | 1785903300 | 1785906000 | 0 | 0 | 15569802 | 31 |
| P306_EVT_0001 | NESTLEIND | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=NESTLEIND\part-00000.parquet | 1 | 1787130875 | 1789577707 | 1785903300 | 1785906000 | 0 | 0 | 15524184 | 31 |
| P306_EVT_0001 | NIFTYBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=NIFTYBEES\part-00000.parquet | 1 | 1787130875 | 1789585957 | 1785903300 | 1785906000 | 0 | 0 | 15553935 | 31 |
| P306_EVT_0001 | ONGC | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ONGC\part-00000.parquet | 1 | 1787130725 | 1789586457 | 1785903300 | 1785906000 | 0 | 0 | 15561869 | 31 |
| P306_EVT_0001 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=RELIANCE\part-00000.parquet | 1 | 1787130475 | 1789587957 | 1785903300 | 1785906000 | 0 | 0 | 15569802 | 31 |
| P306_EVT_0001 | SBIN | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=SBIN\part-00000.parquet | 1 | 1787130875 | 1789580957 | 1785903300 | 1785906000 | 0 | 0 | 15595587 | 31 |
| P306_EVT_0001 | SUNPHARMA | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=SUNPHARMA\part-00000.parquet | 1 | 1787130475 | 1789586707 | 1785903300 | 1785906000 | 0 | 0 | 15561869 | 31 |
| P306_EVT_0001 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=TCS\part-00000.parquet | 1 | 1787130875 | 1789601457 | 1785903300 | 1785906000 | 0 | 0 | 15546001 | 31 |
| P306_EVT_0001 | TECHM | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=TECHM\part-00000.parquet | 1 | 1787130875 | 1789597457 | 1785903300 | 1785906000 | 0 | 0 | 15569802 | 31 |
| P306_EVT_0001 | ULTRACEMCO | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ULTRACEMCO\part-00000.parquet | 1 | 1787130475 | 1789582957 | 1785903300 | 1785906000 | 0 | 0 | 15534101 | 31 |
| P306_EVT_0001 | WIPRO | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=WIPRO\part-00000.parquet | 1 | 1787130875 | 1789579957 | 1785903300 | 1785906000 | 0 | 0 | 15546001 | 31 |

## Joined row preview

| status | reason |
| --- | --- |
| no_joined_rows | event timestamp window does not overlap dense parquet timestamp bounds |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P307_PHASE306_PRECOMMIT_COMPLETE | True | 1 | 1 | hard |
| P307_WORK_ORDER_COVERAGE_AUDITED | True | 32 | >0 | hard |
| P307_FULL_DEPTH_COLUMNS_RETAINED | True | 1 | 1 | hard |
| P307_TIMESTAMP_OVERLAP_RECORDED | True | 0 | recorded | hard |
| P307_MATERIALIZATION_RESULT_RECORDED | True | 0 | recorded | hard |
| P307_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P307_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

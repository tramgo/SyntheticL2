# Phase307 Event-Catalyst Top-Five Depth Join Materialization

Phase307 attempts to materialize the Phase306 event-catalyst to top-five depth join. It records timestamp coverage explicitly and does not run strategy search.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase307_join_materialization_complete | 1 | Phase307 event-catalyst top-five depth join materialization completed |
| phase307_work_order_rows | 64 | Event-symbol work-order rows audited |
| phase307_timestamp_overlap_rows | 32 | Event-symbol rows whose dense file overlaps event window |
| phase307_materialized_join_rows | 2721782 | Joined top-five depth rows materialized |
| phase307_materialized_symbols | 32 | Symbols with joined rows |
| phase307_full_depth_columns_present | 1 | Depth levels 1-5 price/quantity/order columns retained |
| phase307_strategy_search_allowed_now | 0 | No strategy search in Phase307 |
| phase307_strategy_replay_allowed | 0 | No replay |
| phase307_strategy_promotion_allowed | 0 | No promotion |
| phase307_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase307_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase307_hard_gate_pass_rows | 7 | Passed hard gates |
| phase307_hard_gate_rows | 7 | Hard gates |
| phase307_next_best_action | run_phase308_event_catalyst_join_quality_audit_no_strategy_search | Recommended next action |

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
| P306_EVT_0002 | ADANIPORTS | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ADANIPORTS\part-00000.parquet | 1 | 1787130875 | 1789579457 | 1787219100 | 1787221800 | 1 | 85930 | 15549968 | 31 |
| P306_EVT_0002 | AXISBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=AXISBANK\part-00000.parquet | 1 | 1787130875 | 1789583957 | 1787219100 | 1787221800 | 1 | 86352 | 15555918 | 31 |
| P306_EVT_0002 | BAJAJ-AUTO | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BAJAJ-AUTO\part-00000.parquet | 1 | 1787130875 | 1789580957 | 1787219100 | 1787221800 | 1 | 84440 | 15542034 | 31 |
| P306_EVT_0002 | BANKBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BANKBEES\part-00000.parquet | 1 | 1787130875 | 1789582957 | 1787219100 | 1787221800 | 1 | 89892 | 15557902 | 31 |
| P306_EVT_0002 | BHARTIARTL | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BHARTIARTL\part-00000.parquet | 1 | 1787130875 | 1789581957 | 1787219100 | 1787221800 | 1 | 85327 | 15575752 | 31 |
| P306_EVT_0002 | BPCL | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BPCL\part-00000.parquet | 1 | 1787130725 | 1789588457 | 1787219100 | 1787221800 | 1 | 85675 | 15512283 | 31 |
| P306_EVT_0002 | BRITANNIA | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=BRITANNIA\part-00000.parquet | 1 | 1787130875 | 1789584457 | 1787219100 | 1787221800 | 1 | 84434 | 15561869 | 31 |
| P306_EVT_0002 | CIPLA | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=CIPLA\part-00000.parquet | 1 | 1787130875 | 1789593457 | 1787219100 | 1787221800 | 1 | 87819 | 15549968 | 31 |
| P306_EVT_0002 | DRREDDY | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=DRREDDY\part-00000.parquet | 1 | 1787130875 | 1789584957 | 1787219100 | 1787221800 | 1 | 86138 | 15563852 | 31 |
| P306_EVT_0002 | GOLDBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=GOLDBEES\part-00000.parquet | 1 | 1787130875 | 1789579457 | 1787219100 | 1787221800 | 1 | 86554 | 15551951 | 31 |
| P306_EVT_0002 | HCLTECH | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=HCLTECH\part-00000.parquet | 1 | 1787130875 | 1789585457 | 1787219100 | 1787221800 | 1 | 84900 | 15575752 | 31 |
| P306_EVT_0002 | HDFCBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=HDFCBANK\part-00000.parquet | 1 | 1787130875 | 1789586189 | 1787219100 | 1787221800 | 1 | 81606 | 15551951 | 31 |
| P306_EVT_0002 | HINDUNILVR | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=HINDUNILVR\part-00000.parquet | 1 | 1787130875 | 1789597457 | 1787219100 | 1787221800 | 1 | 79410 | 15542034 | 31 |
| P306_EVT_0002 | ICICIBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ICICIBANK\part-00000.parquet | 1 | 1787130875 | 1789582957 | 1787219100 | 1787221800 | 1 | 78383 | 15569802 | 31 |
| P306_EVT_0002 | INFY | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=INFY\part-00000.parquet | 1 | 1787130875 | 1789581957 | 1787219100 | 1787221800 | 1 | 86901 | 15565835 | 31 |
| P306_EVT_0002 | ITBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ITBEES\part-00000.parquet | 1 | 1787130875 | 1789580457 | 1787219100 | 1787221800 | 1 | 84640 | 15551951 | 31 |
| P306_EVT_0002 | ITC | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ITC\part-00000.parquet | 1 | 1787130875 | 1789576957 | 1787219100 | 1787221800 | 1 | 86816 | 15577736 | 31 |
| P306_EVT_0002 | JUNIORBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=JUNIORBEES\part-00000.parquet | 1 | 1787130875 | 1789581957 | 1787219100 | 1787221800 | 1 | 84742 | 15547985 | 31 |
| P306_EVT_0002 | KOTAKBANK | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=KOTAKBANK\part-00000.parquet | 1 | 1787130475 | 1789596457 | 1787219100 | 1787221800 | 1 | 81137 | 15557902 | 31 |
| P306_EVT_0002 | LT | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=LT\part-00000.parquet | 1 | 1787130875 | 1789596707 | 1787219100 | 1787221800 | 1 | 84090 | 15581703 | 31 |
| P306_EVT_0002 | M&M | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=M&M\part-00000.parquet | 1 | 1787130875 | 1789595957 | 1787219100 | 1787221800 | 1 | 80859 | 15565835 | 31 |
| P306_EVT_0002 | MARUTI | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=MARUTI\part-00000.parquet | 1 | 1787130875 | 1789595457 | 1787219100 | 1787221800 | 1 | 84687 | 15569802 | 31 |
| P306_EVT_0002 | NESTLEIND | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=NESTLEIND\part-00000.parquet | 1 | 1787130875 | 1789577707 | 1787219100 | 1787221800 | 1 | 88082 | 15524184 | 31 |
| P306_EVT_0002 | NIFTYBEES | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=NIFTYBEES\part-00000.parquet | 1 | 1787130875 | 1789585957 | 1787219100 | 1787221800 | 1 | 84352 | 15553935 | 31 |
| P306_EVT_0002 | ONGC | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ONGC\part-00000.parquet | 1 | 1787130725 | 1789586457 | 1787219100 | 1787221800 | 1 | 82748 | 15561869 | 31 |
| P306_EVT_0002 | RELIANCE | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=RELIANCE\part-00000.parquet | 1 | 1787130475 | 1789587957 | 1787219100 | 1787221800 | 1 | 82550 | 15569802 | 31 |
| P306_EVT_0002 | SBIN | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=SBIN\part-00000.parquet | 1 | 1787130875 | 1789580957 | 1787219100 | 1787221800 | 1 | 84692 | 15595587 | 31 |
| P306_EVT_0002 | SUNPHARMA | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=SUNPHARMA\part-00000.parquet | 1 | 1787130475 | 1789586707 | 1787219100 | 1787221800 | 1 | 86902 | 15561869 | 31 |
| P306_EVT_0002 | TCS | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=TCS\part-00000.parquet | 1 | 1787130875 | 1789601457 | 1787219100 | 1787221800 | 1 | 87069 | 15546001 | 31 |
| P306_EVT_0002 | TECHM | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=TECHM\part-00000.parquet | 1 | 1787130875 | 1789597457 | 1787219100 | 1787221800 | 1 | 88790 | 15569802 | 31 |
| P306_EVT_0002 | ULTRACEMCO | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=ULTRACEMCO\part-00000.parquet | 1 | 1787130475 | 1789582957 | 1787219100 | 1787221800 | 1 | 87316 | 15534101 | 31 |
| P306_EVT_0002 | WIPRO | raw_synthetic_l2_dense_full_year\trade_month=2026-08\symbol=WIPRO\part-00000.parquet | 1 | 1787130875 | 1789579957 | 1787219100 | 1787221800 | 1 | 88549 | 15546001 | 31 |

## Joined row preview

| event_id | event_time_ist | event_type | symbol | relative_second | exchange_timestamp_ms | last_price | volume_traded | buy_1_price | buy_1_quantity | buy_1_orders | sell_1_price | sell_1_quantity | sell_1_orders | buy_2_price | buy_2_quantity | buy_2_orders | sell_2_price | sell_2_quantity | sell_2_orders | buy_3_price | buy_3_quantity | buy_3_orders | sell_3_price | sell_3_quantity | sell_3_orders | buy_4_price | buy_4_quantity | buy_4_orders | sell_4_price | sell_4_quantity | sell_4_orders | buy_5_price | buy_5_quantity | buy_5_orders | sell_5_price | sell_5_quantity | sell_5_orders |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -900 | 1787219100 | 1829.1 | 4504 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -899 | 1787219101 | 1829.1 | 4508 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -898 | 1787219102 | 1829.1 | 4512 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -897 | 1787219103 | 1829.11 | 4516 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -896 | 1787219104 | 1829.1 | 4520 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -895 | 1787219105 | 1829.11 | 4524 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -894 | 1787219106 | 1829.09 | 4528 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -893 | 1787219107 | 1829.11 | 4532 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -892 | 1787219108 | 1829.09 | 4536 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -891 | 1787219109 | 1829.11 | 4540 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -890 | 1787219110 | 1829.09 | 4544 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -889 | 1787219111 | 1829.11 | 4548 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -888 | 1787219112 | 1829.09 | 4552 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -887 | 1787219113 | 1829.11 | 4556 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -886 | 1787219114 | 1829.09 | 4560 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -885 | 1787219115 | 1829.11 | 4564 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -884 | 1787219116 | 1829.09 | 4568 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -883 | 1787219117 | 1829.11 | 4572 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -882 | 1787219118 | 1829.09 | 4576 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -881 | 1787219119 | 1829.11 | 4580 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -880 | 1787219120 | 1829.09 | 4584 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -879 | 1787219121 | 1829.11 | 4588 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -878 | 1787219122 | 1829.09 | 4592 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -877 | 1787219123 | 1829.11 | 4596 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |
| P306_EVT_0002 | 2026-08-20 15:30:00+05:30 | rbi_policy | ADANIPORTS | -876 | 1787219124 | 1829.09 | 4600 | 1828.65 | 714 | 4 | 1829.55 | 462 | 3 | 1828.55 | 967 | 5 | 1829.65 | 621 | 4 | 1828.45 | 1222 | 7 | 1829.75 | 777 | 4 | 1828.35 | 1478 | 8 | 1829.85 | 933 | 5 | 1828.25 | 1736 | 9 | 1829.95 | 1086 | 6 |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P307_PHASE306_PRECOMMIT_COMPLETE | True | 1 | 1 | hard |
| P307_WORK_ORDER_COVERAGE_AUDITED | True | 64 | >0 | hard |
| P307_FULL_DEPTH_COLUMNS_RETAINED | True | 1 | 1 | hard |
| P307_TIMESTAMP_OVERLAP_RECORDED | True | 32 | recorded | hard |
| P307_MATERIALIZATION_RESULT_RECORDED | True | 2721782 | recorded | hard |
| P307_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P307_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

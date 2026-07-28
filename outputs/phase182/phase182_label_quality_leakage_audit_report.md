# Phase182 Label Quality and Leakage Audit

Generated UTC: 2026-07-28T16:31:12.854022+00:00

Phase182 audits Phase181 labels for quality, split integrity, leakage boundaries, and forbidden output columns.
It does not run strategies, emit orders, compute fills, calculate P&L, claim profitability, or open paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase182_partition_audit_rows | 640 | Label partitions audited |
| phase182_split_audit_rows | 3 | Split leakage audit rows |
| phase182_failed_partitions | 0 | Failed label partitions |
| phase182_forbidden_column_partitions | 0 | Partitions with forbidden output columns |
| phase182_min_label_available_fraction | 0.993243 | Minimum partition label availability |
| phase182_gate_rows | 7 | Gates evaluated |
| phase182_hard_gate_rows | 7 | Hard gates evaluated |
| phase182_hard_gate_pass_rows | 7 | Hard gates passed |
| phase182_label_quality_leakage_audit_pass | 1 | 1 means label quality/leakage audit passed |
| phase182_strategy_replay_allowed | 0 | No strategy replay opened |
| phase182_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase182_next_best_action | build_phase183_replay_readiness_precommit_no_pnl | Recommended next milestone |

## Split Leakage Audit

| split_role | partitions | rows | test_untouched_rows | failed_partitions | min_label_available_fraction | leakage_policy |
| --- | --- | --- | --- | --- | --- | --- |
| test_untouched | 128 | 567640 | 567640 | 0 | 0.994695 | test_untouched rows may exist as labels but must not be used for selection before replay precommit |
| train | 384 | 1080009 | 0 | 0 | 0.993243 | test_untouched rows may exist as labels but must not be used for selection before replay precommit |
| validation | 128 | 561515 | 0 | 0 | 0.997347 | test_untouched rows may exist as labels but must not be used for selection before replay precommit |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P182_PHASE181_LABELS_MATERIALIZED | 1 | phase181_labels_materialized=1 | hard |
| P182_PHASE180_PRECOMMIT_READY | 1 | phase180_precommit_ready=1 | hard |
| P182_ALL_LABEL_PARTITIONS_PASS | 1 | partitions=640;failed_partitions=0 | hard |
| P182_NO_FORBIDDEN_OUTPUT_COLUMNS | 1 | forbidden_column_partitions=0 | hard |
| P182_SPLIT_ROLES_AND_TEST_UNTOUCHED_PRESENT | 1 | split_roles=test_untouched;train;validation | hard |
| P182_LABEL_AVAILABILITY_THRESHOLD | 1 | min_label_available_fraction=0.993243 | hard |
| P182_NO_REPLAY_OR_PROFITABILITY_OUTPUTS | 1 | label quality/leakage audit only; no replay or PnL artifacts emitted | hard |

## Label Partition Quality Audit

| label_file | read_status | horizon_sec | trade_date | exchange | symbol | split_role | rows | missing_required_columns | forbidden_columns | bucket_monotonic_violations | duplicate_bucket_rows | split_role_mismatch_rows | test_role_rows | label_available_fraction | audit_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | ADANIPORTS | train | 3618 |  |  | 0 | 0 | 0 | 0 | 0.999724 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | AXISBANK | train | 5830 |  |  | 0 | 0 | 0 | 0 | 0.999828 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 3324 |  |  | 0 | 0 | 0 | 0 | 0.999699 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | BANKBEES | train | 5646 |  |  | 0 | 0 | 0 | 0 | 0.999823 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | BHARTIARTL | train | 3953 |  |  | 0 | 0 | 0 | 0 | 0.999747 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | BPCL | train | 2853 |  |  | 0 | 0 | 0 | 0 | 0.999649 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | BRITANNIA | train | 2152 |  |  | 0 | 0 | 0 | 0 | 0.999535 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | CIPLA | train | 2954 |  |  | 0 | 0 | 0 | 0 | 0.999661 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | DRREDDY | train | 2936 |  |  | 0 | 0 | 0 | 0 | 0.999659 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | GOLDBEES | train | 4079 |  |  | 0 | 0 | 0 | 0 | 0.999755 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | HCLTECH | train | 2707 |  |  | 0 | 0 | 0 | 0 | 0.999631 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | HDFCBANK | train | 6817 |  |  | 0 | 0 | 0 | 0 | 0.999853 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | HINDUNILVR | train | 3471 |  |  | 0 | 0 | 0 | 0 | 0.999712 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | ICICIBANK | train | 6211 |  |  | 0 | 0 | 0 | 0 | 0.999839 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=INFY\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | INFY | train | 5153 |  |  | 0 | 0 | 0 | 0 | 0.999806 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | ITBEES | train | 2356 |  |  | 0 | 0 | 0 | 0 | 0.999576 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ITC\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | ITC | train | 4272 |  |  | 0 | 0 | 0 | 0 | 0.999766 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | JUNIORBEES | train | 5242 |  |  | 0 | 0 | 0 | 0 | 0.999809 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | KOTAKBANK | train | 4945 |  |  | 0 | 0 | 0 | 0 | 0.999798 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=LT\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | LT | train | 6329 |  |  | 0 | 0 | 0 | 0 | 0.999842 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=M&M\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | M&M | train | 6038 |  |  | 0 | 0 | 0 | 0 | 0.999834 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | MARUTI | train | 4918 |  |  | 0 | 0 | 0 | 0 | 0.999797 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | NESTLEIND | train | 2944 |  |  | 0 | 0 | 0 | 0 | 0.99966 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | NIFTYBEES | train | 5017 |  |  | 0 | 0 | 0 | 0 | 0.999801 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | ONGC | train | 4122 |  |  | 0 | 0 | 0 | 0 | 0.999757 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | RELIANCE | train | 6548 |  |  | 0 | 0 | 0 | 0 | 0.999847 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | SBIN | train | 5500 |  |  | 0 | 0 | 0 | 0 | 0.999818 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | SUNPHARMA | train | 3353 |  |  | 0 | 0 | 0 | 0 | 0.999702 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=TCS\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | TCS | train | 3905 |  |  | 0 | 0 | 0 | 0 | 0.999744 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | TECHM | train | 2803 |  |  | 0 | 0 | 0 | 0 | 0.999643 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ULTRACEMCO\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | ULTRACEMCO | train | 3044 |  |  | 0 | 0 | 0 | 0 | 0.999671 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=WIPRO\receive_flow_labels.parquet | ok | 1 | 2026-07-08 | NSE | WIPRO | train | 2626 |  |  | 0 | 0 | 0 | 0 | 0.999619 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | ADANIPORTS | train | 5554 |  |  | 0 | 0 | 0 | 0 | 0.99982 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | AXISBANK | train | 7447 |  |  | 0 | 0 | 0 | 0 | 0.999866 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 5050 |  |  | 0 | 0 | 0 | 0 | 0.999802 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | BANKBEES | train | 8886 |  |  | 0 | 0 | 0 | 0 | 0.999887 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | BHARTIARTL | train | 9412 |  |  | 0 | 0 | 0 | 0 | 0.999894 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | BPCL | train | 4697 |  |  | 0 | 0 | 0 | 0 | 0.999787 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | BRITANNIA | train | 4230 |  |  | 0 | 0 | 0 | 0 | 0.999764 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | CIPLA | train | 4887 |  |  | 0 | 0 | 0 | 0 | 0.999795 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=DRREDDY\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | DRREDDY | train | 9054 |  |  | 0 | 0 | 0 | 0 | 0.99989 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=GOLDBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | GOLDBEES | train | 6408 |  |  | 0 | 0 | 0 | 0 | 0.999844 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=HCLTECH\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | HCLTECH | train | 5478 |  |  | 0 | 0 | 0 | 0 | 0.999817 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=HDFCBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | HDFCBANK | train | 9420 |  |  | 0 | 0 | 0 | 0 | 0.999894 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=HINDUNILVR\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | HINDUNILVR | train | 6947 |  |  | 0 | 0 | 0 | 0 | 0.999856 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ICICIBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | ICICIBANK | train | 9153 |  |  | 0 | 0 | 0 | 0 | 0.999891 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=INFY\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | INFY | train | 7567 |  |  | 0 | 0 | 0 | 0 | 0.999868 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ITBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | ITBEES | train | 3873 |  |  | 0 | 0 | 0 | 0 | 0.999742 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ITC\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | ITC | train | 7310 |  |  | 0 | 0 | 0 | 0 | 0.999863 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=JUNIORBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | JUNIORBEES | train | 8590 |  |  | 0 | 0 | 0 | 0 | 0.999884 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=KOTAKBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | KOTAKBANK | train | 8944 |  |  | 0 | 0 | 0 | 0 | 0.999888 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=LT\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | LT | train | 9073 |  |  | 0 | 0 | 0 | 0 | 0.99989 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=M&M\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | M&M | train | 7705 |  |  | 0 | 0 | 0 | 0 | 0.99987 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=MARUTI\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | MARUTI | train | 7380 |  |  | 0 | 0 | 0 | 0 | 0.999864 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=NESTLEIND\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | NESTLEIND | train | 4455 |  |  | 0 | 0 | 0 | 0 | 0.999776 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=NIFTYBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | NIFTYBEES | train | 8020 |  |  | 0 | 0 | 0 | 0 | 0.999875 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ONGC\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | ONGC | train | 5783 |  |  | 0 | 0 | 0 | 0 | 0.999827 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=RELIANCE\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | RELIANCE | train | 9018 |  |  | 0 | 0 | 0 | 0 | 0.999889 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=SBIN\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | SBIN | train | 7834 |  |  | 0 | 0 | 0 | 0 | 0.999872 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=SUNPHARMA\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | SUNPHARMA | train | 7323 |  |  | 0 | 0 | 0 | 0 | 0.999863 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=TCS\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | TCS | train | 7970 |  |  | 0 | 0 | 0 | 0 | 0.999875 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=TECHM\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | TECHM | train | 4930 |  |  | 0 | 0 | 0 | 0 | 0.999797 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ULTRACEMCO\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | ULTRACEMCO | train | 3980 |  |  | 0 | 0 | 0 | 0 | 0.999749 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=WIPRO\receive_flow_labels.parquet | ok | 1 | 2026-07-09 | NSE | WIPRO | train | 5789 |  |  | 0 | 0 | 0 | 0 | 0.999827 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | ADANIPORTS | train | 9547 |  |  | 0 | 0 | 0 | 0 | 0.999895 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | AXISBANK | train | 10802 |  |  | 0 | 0 | 0 | 0 | 0.999907 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 9728 |  |  | 0 | 0 | 0 | 0 | 0.999897 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | BANKBEES | train | 9231 |  |  | 0 | 0 | 0 | 0 | 0.999783 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | BHARTIARTL | train | 11366 |  |  | 0 | 0 | 0 | 0 | 0.999912 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | BPCL | train | 6759 |  |  | 0 | 0 | 0 | 0 | 0.999852 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | BRITANNIA | train | 6030 |  |  | 0 | 0 | 0 | 0 | 0.999834 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | CIPLA | train | 7908 |  |  | 0 | 0 | 0 | 0 | 0.999874 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=DRREDDY\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | DRREDDY | train | 13142 |  |  | 0 | 0 | 0 | 0 | 0.999924 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=GOLDBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | GOLDBEES | train | 9150 |  |  | 0 | 0 | 0 | 0 | 0.999781 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=HCLTECH\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | HCLTECH | train | 14318 |  |  | 0 | 0 | 0 | 0 | 0.99993 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=HDFCBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | HDFCBANK | train | 15044 |  |  | 0 | 0 | 0 | 0 | 0.999934 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=HINDUNILVR\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | HINDUNILVR | train | 8662 |  |  | 0 | 0 | 0 | 0 | 0.999885 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ICICIBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | ICICIBANK | train | 11237 |  |  | 0 | 0 | 0 | 0 | 0.999911 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=INFY\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | INFY | train | 15211 |  |  | 0 | 0 | 0 | 0 | 0.999934 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ITBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | ITBEES | train | 6824 |  |  | 0 | 0 | 0 | 0 | 0.999707 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ITC\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | ITC | train | 11085 |  |  | 0 | 0 | 0 | 0 | 0.99991 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=JUNIORBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | JUNIORBEES | train | 13254 |  |  | 0 | 0 | 0 | 0 | 0.999849 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=KOTAKBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | KOTAKBANK | train | 10165 |  |  | 0 | 0 | 0 | 0 | 0.999902 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=LT\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | LT | train | 10641 |  |  | 0 | 0 | 0 | 0 | 0.999906 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=M&M\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | M&M | train | 9988 |  |  | 0 | 0 | 0 | 0 | 0.9999 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=MARUTI\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | MARUTI | train | 11105 |  |  | 0 | 0 | 0 | 0 | 0.99991 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=NESTLEIND\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | NESTLEIND | train | 7879 |  |  | 0 | 0 | 0 | 0 | 0.999873 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=NIFTYBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | NIFTYBEES | train | 11228 |  |  | 0 | 0 | 0 | 0 | 0.999822 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ONGC\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | ONGC | train | 9396 |  |  | 0 | 0 | 0 | 0 | 0.999894 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=RELIANCE\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | RELIANCE | train | 11460 |  |  | 0 | 0 | 0 | 0 | 0.999913 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=SBIN\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | SBIN | train | 12206 |  |  | 0 | 0 | 0 | 0 | 0.999918 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=SUNPHARMA\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | SUNPHARMA | train | 9909 |  |  | 0 | 0 | 0 | 0 | 0.999899 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=TCS\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | TCS | train | 16260 |  |  | 0 | 0 | 0 | 0 | 0.999938 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=TECHM\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | TECHM | train | 9552 |  |  | 0 | 0 | 0 | 0 | 0.999895 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ULTRACEMCO\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | ULTRACEMCO | train | 6526 |  |  | 0 | 0 | 0 | 0 | 0.999847 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=WIPRO\receive_flow_labels.parquet | ok | 1 | 2026-07-10 | NSE | WIPRO | train | 10158 |  |  | 0 | 0 | 0 | 0 | 0.999902 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | ADANIPORTS | validation | 9454 |  |  | 0 | 0 | 0 | 0 | 0.999894 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | AXISBANK | validation | 10798 |  |  | 0 | 0 | 0 | 0 | 0.999907 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 14299 |  |  | 0 | 0 | 0 | 0 | 0.99993 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | BANKBEES | validation | 13184 |  |  | 0 | 0 | 0 | 0 | 0.999924 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | BHARTIARTL | validation | 11539 |  |  | 0 | 0 | 0 | 0 | 0.999913 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | BPCL | validation | 8035 |  |  | 0 | 0 | 0 | 0 | 0.999876 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | BRITANNIA | validation | 6760 |  |  | 0 | 0 | 0 | 0 | 0.999852 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | CIPLA | validation | 8388 |  |  | 0 | 0 | 0 | 0 | 0.999881 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=DRREDDY\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | DRREDDY | validation | 8736 |  |  | 0 | 0 | 0 | 0 | 0.999886 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=GOLDBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | GOLDBEES | validation | 8948 |  |  | 0 | 0 | 0 | 0 | 0.999888 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=HCLTECH\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | HCLTECH | validation | 14297 |  |  | 0 | 0 | 0 | 0 | 0.99993 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=HDFCBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | HDFCBANK | validation | 16566 |  |  | 0 | 0 | 0 | 0 | 0.99994 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=HINDUNILVR\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | HINDUNILVR | validation | 8592 |  |  | 0 | 0 | 0 | 0 | 0.999884 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ICICIBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | ICICIBANK | validation | 13717 |  |  | 0 | 0 | 0 | 0 | 0.999927 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=INFY\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | INFY | validation | 16207 |  |  | 0 | 0 | 0 | 0 | 0.999938 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ITBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | ITBEES | validation | 8306 |  |  | 0 | 0 | 0 | 0 | 0.999759 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ITC\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | ITC | validation | 8758 |  |  | 0 | 0 | 0 | 0 | 0.999886 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=JUNIORBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | JUNIORBEES | validation | 11802 |  |  | 0 | 0 | 0 | 0 | 0.999915 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=KOTAKBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | KOTAKBANK | validation | 9403 |  |  | 0 | 0 | 0 | 0 | 0.999894 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=LT\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | LT | validation | 11479 |  |  | 0 | 0 | 0 | 0 | 0.999913 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=M&M\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | M&M | validation | 14146 |  |  | 0 | 0 | 0 | 0 | 0.999929 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=MARUTI\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | MARUTI | validation | 15407 |  |  | 0 | 0 | 0 | 0 | 0.999935 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=NESTLEIND\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | NESTLEIND | validation | 9036 |  |  | 0 | 0 | 0 | 0 | 0.999889 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=NIFTYBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | NIFTYBEES | validation | 13040 |  |  | 0 | 0 | 0 | 0 | 0.999923 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ONGC\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | ONGC | validation | 10645 |  |  | 0 | 0 | 0 | 0 | 0.999906 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=RELIANCE\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | RELIANCE | validation | 13220 |  |  | 0 | 0 | 0 | 0 | 0.999924 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=SBIN\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | SBIN | validation | 13085 |  |  | 0 | 0 | 0 | 0 | 0.999924 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=SUNPHARMA\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | SUNPHARMA | validation | 9573 |  |  | 0 | 0 | 0 | 0 | 0.999896 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=TCS\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | TCS | validation | 16807 |  |  | 0 | 0 | 0 | 0 | 0.999941 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=TECHM\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | TECHM | validation | 11317 |  |  | 0 | 0 | 0 | 0 | 0.999912 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ULTRACEMCO\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | ULTRACEMCO | validation | 6784 |  |  | 0 | 0 | 0 | 0 | 0.999853 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=WIPRO\receive_flow_labels.parquet | ok | 1 | 2026-07-13 | NSE | WIPRO | validation | 11491 |  |  | 0 | 0 | 0 | 0 | 0.999913 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | ADANIPORTS | test_untouched | 9871 |  |  | 0 | 0 | 0 | 9871 | 0.999899 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | AXISBANK | test_untouched | 12369 |  |  | 0 | 0 | 0 | 12369 | 0.999838 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | BAJAJ-AUTO | test_untouched | 15119 |  |  | 0 | 0 | 0 | 15119 | 0.999934 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | BANKBEES | test_untouched | 12042 |  |  | 0 | 0 | 0 | 12042 | 0.999751 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | BHARTIARTL | test_untouched | 13068 |  |  | 0 | 0 | 0 | 13068 | 0.999923 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | BPCL | test_untouched | 8730 |  |  | 0 | 0 | 0 | 8730 | 0.999771 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | BRITANNIA | test_untouched | 8238 |  |  | 0 | 0 | 0 | 8238 | 0.999879 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | CIPLA | test_untouched | 8978 |  |  | 0 | 0 | 0 | 8978 | 0.999889 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=DRREDDY\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | DRREDDY | test_untouched | 8456 |  |  | 0 | 0 | 0 | 8456 | 0.999882 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=GOLDBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | GOLDBEES | test_untouched | 9933 |  |  | 0 | 0 | 0 | 9933 | 0.999799 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=HCLTECH\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | HCLTECH | test_untouched | 15678 |  |  | 0 | 0 | 0 | 15678 | 0.999872 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=HDFCBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | HDFCBANK | test_untouched | 15864 |  |  | 0 | 0 | 0 | 15864 | 0.999937 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=HINDUNILVR\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | HINDUNILVR | test_untouched | 10846 |  |  | 0 | 0 | 0 | 10846 | 0.999908 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ICICIBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | ICICIBANK | test_untouched | 13574 |  |  | 0 | 0 | 0 | 13574 | 0.999926 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=INFY\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | INFY | test_untouched | 15629 |  |  | 0 | 0 | 0 | 15629 | 0.999936 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ITBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | ITBEES | test_untouched | 6618 |  |  | 0 | 0 | 0 | 6618 | 0.999547 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ITC\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | ITC | test_untouched | 12350 |  |  | 0 | 0 | 0 | 12350 | 0.999838 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=JUNIORBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | JUNIORBEES | test_untouched | 11963 |  |  | 0 | 0 | 0 | 11963 | 0.999749 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=KOTAKBANK\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | KOTAKBANK | test_untouched | 11204 |  |  | 0 | 0 | 0 | 11204 | 0.999821 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=LT\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | LT | test_untouched | 12561 |  |  | 0 | 0 | 0 | 12561 | 0.99992 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=M&M\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | M&M | test_untouched | 13068 |  |  | 0 | 0 | 0 | 13068 | 0.999923 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=MARUTI\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | MARUTI | test_untouched | 11008 |  |  | 0 | 0 | 0 | 11008 | 0.999909 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=NESTLEIND\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | NESTLEIND | test_untouched | 9368 |  |  | 0 | 0 | 0 | 9368 | 0.999893 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=NIFTYBEES\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | NIFTYBEES | test_untouched | 11590 |  |  | 0 | 0 | 0 | 11590 | 0.999741 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ONGC\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | ONGC | test_untouched | 10278 |  |  | 0 | 0 | 0 | 10278 | 0.999903 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=RELIANCE\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | RELIANCE | test_untouched | 13625 |  |  | 0 | 0 | 0 | 13625 | 0.999853 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=SBIN\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | SBIN | test_untouched | 12764 |  |  | 0 | 0 | 0 | 12764 | 0.999843 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=SUNPHARMA\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | SUNPHARMA | test_untouched | 11509 |  |  | 0 | 0 | 0 | 11509 | 0.999913 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=TCS\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | TCS | test_untouched | 15792 |  |  | 0 | 0 | 0 | 15792 | 0.999937 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=TECHM\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | TECHM | test_untouched | 11095 |  |  | 0 | 0 | 0 | 11095 | 0.99991 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ULTRACEMCO\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | ULTRACEMCO | test_untouched | 7965 |  |  | 0 | 0 | 0 | 7965 | 0.999874 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=WIPRO\receive_flow_labels.parquet | ok | 1 | 2026-07-14 | NSE | WIPRO | test_untouched | 9396 |  |  | 0 | 0 | 0 | 9396 | 0.999787 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | ADANIPORTS | train | 1618 |  |  | 0 | 0 | 0 | 0 | 0.999382 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | AXISBANK | train | 1700 |  |  | 0 | 0 | 0 | 0 | 0.999412 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 1595 |  |  | 0 | 0 | 0 | 0 | 0.999373 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | BANKBEES | train | 1694 |  |  | 0 | 0 | 0 | 0 | 0.99941 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | BHARTIARTL | train | 1617 |  |  | 0 | 0 | 0 | 0 | 0.999382 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | BPCL | train | 1579 |  |  | 0 | 0 | 0 | 0 | 0.999367 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | BRITANNIA | train | 1526 |  |  | 0 | 0 | 0 | 0 | 0.999345 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | CIPLA | train | 1573 |  |  | 0 | 0 | 0 | 0 | 0.999364 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | DRREDDY | train | 1583 |  |  | 0 | 0 | 0 | 0 | 0.999368 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | GOLDBEES | train | 1643 |  |  | 0 | 0 | 0 | 0 | 0.999391 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | HCLTECH | train | 1565 |  |  | 0 | 0 | 0 | 0 | 0.999361 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | HDFCBANK | train | 1746 |  |  | 0 | 0 | 0 | 0 | 0.999427 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | HINDUNILVR | train | 1619 |  |  | 0 | 0 | 0 | 0 | 0.999382 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | ICICIBANK | train | 1723 |  |  | 0 | 0 | 0 | 0 | 0.99942 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=INFY\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | INFY | train | 1683 |  |  | 0 | 0 | 0 | 0 | 0.999406 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | ITBEES | train | 1586 |  |  | 0 | 0 | 0 | 0 | 0.999369 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ITC\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | ITC | train | 1644 |  |  | 0 | 0 | 0 | 0 | 0.999392 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | JUNIORBEES | train | 1686 |  |  | 0 | 0 | 0 | 0 | 0.999407 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | KOTAKBANK | train | 1665 |  |  | 0 | 0 | 0 | 0 | 0.999399 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=LT\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | LT | train | 1734 |  |  | 0 | 0 | 0 | 0 | 0.999423 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=M&M\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | M&M | train | 1715 |  |  | 0 | 0 | 0 | 0 | 0.999417 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | MARUTI | train | 1680 |  |  | 0 | 0 | 0 | 0 | 0.999405 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | NESTLEIND | train | 1581 |  |  | 0 | 0 | 0 | 0 | 0.999367 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | NIFTYBEES | train | 1688 |  |  | 0 | 0 | 0 | 0 | 0.999408 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | ONGC | train | 1629 |  |  | 0 | 0 | 0 | 0 | 0.999386 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | RELIANCE | train | 1732 |  |  | 0 | 0 | 0 | 0 | 0.999423 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | SBIN | train | 1687 |  |  | 0 | 0 | 0 | 0 | 0.999407 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | SUNPHARMA | train | 1601 |  |  | 0 | 0 | 0 | 0 | 0.999375 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=TCS\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | TCS | train | 1652 |  |  | 0 | 0 | 0 | 0 | 0.999395 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | TECHM | train | 1575 |  |  | 0 | 0 | 0 | 0 | 0.999365 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ULTRACEMCO\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | ULTRACEMCO | train | 1578 |  |  | 0 | 0 | 0 | 0 | 0.999366 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=WIPRO\receive_flow_labels.parquet | ok | 5 | 2026-07-08 | NSE | WIPRO | train | 1570 |  |  | 0 | 0 | 0 | 0 | 0.999363 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | ok | 5 | 2026-07-09 | NSE | ADANIPORTS | train | 2449 |  |  | 0 | 0 | 0 | 0 | 0.999592 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | ok | 5 | 2026-07-09 | NSE | AXISBANK | train | 2523 |  |  | 0 | 0 | 0 | 0 | 0.999604 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | ok | 5 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 2391 |  |  | 0 | 0 | 0 | 0 | 0.999582 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | ok | 5 | 2026-07-09 | NSE | BANKBEES | train | 2538 |  |  | 0 | 0 | 0 | 0 | 0.999606 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | ok | 5 | 2026-07-09 | NSE | BHARTIARTL | train | 2559 |  |  | 0 | 0 | 0 | 0 | 0.999609 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | ok | 5 | 2026-07-09 | NSE | BPCL | train | 2422 |  |  | 0 | 0 | 0 | 0 | 0.999587 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | ok | 5 | 2026-07-09 | NSE | BRITANNIA | train | 2365 |  |  | 0 | 0 | 0 | 0 | 0.999577 | 1 |
| derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-09\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | ok | 5 | 2026-07-09 | NSE | CIPLA | train | 2408 |  |  | 0 | 0 | 0 | 0 | 0.999585 | 1 |

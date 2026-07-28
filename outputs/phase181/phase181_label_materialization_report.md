# Phase181 Label Materialization

Generated UTC: 2026-07-28T18:07:08.278152+00:00

Phase181 materializes future receive-flow labels from Phase176 features under the Phase180 precommit.
It does not emit signals, sides, orders, fills, P&L, profitability claims, or paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase181_label_partition_rows | 768 | Label partitions materialized |
| phase181_label_rows | 2772233 | Label rows written |
| phase181_label_available_rows | 2771375 | Rows with primary labels available |
| phase181_quality_rows | 24 | Horizon/date/split quality rows |
| phase181_gate_rows | 5 | Gates evaluated |
| phase181_hard_gate_rows | 5 | Hard gates evaluated |
| phase181_hard_gate_pass_rows | 5 | Hard gates passed |
| phase181_labels_materialized | 1 | 1 means label parquet was materialized |
| phase181_strategy_replay_allowed | 0 | No strategy replay opened |
| phase181_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase181_forbidden_outputs | signal;side;order;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | Outputs forbidden in this phase |
| phase181_next_best_action | build_phase182_label_quality_leakage_audit_no_replay | Recommended next milestone |

## Label Quality by Horizon/date/split

| horizon_sec | trade_date | split_role | partitions | rows | label_available_rows | availability_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-07-08 | train | 32 | 135666 | 135634 | 0.999764 |
| 1 | 2026-07-09 | train | 32 | 222167 | 222135 | 0.999856 |
| 1 | 2026-07-10 | train | 32 | 335771 | 335734 | 0.99989 |
| 1 | 2026-07-13 | validation | 32 | 363819 | 363786 | 0.999909 |
| 1 | 2026-07-14 | test_untouched | 32 | 370549 | 370500 | 0.999868 |
| 1 | 2026-07-15 | unassigned | 32 | 365743 | 365701 | 0.999885 |
| 5 | 2026-07-08 | train | 32 | 52467 | 52435 | 0.99939 |
| 5 | 2026-07-09 | train | 32 | 79436 | 79404 | 0.999597 |
| 5 | 2026-07-10 | train | 32 | 136471 | 136434 | 0.999729 |
| 5 | 2026-07-13 | validation | 32 | 137509 | 137477 | 0.999767 |
| 5 | 2026-07-14 | test_untouched | 32 | 136919 | 136873 | 0.999664 |
| 5 | 2026-07-15 | unassigned | 32 | 137136 | 137094 | 0.999694 |
| 15 | 2026-07-08 | train | 32 | 18688 | 18656 | 0.998288 |
| 15 | 2026-07-09 | train | 32 | 27492 | 27460 | 0.998836 |
| 15 | 2026-07-10 | train | 32 | 48085 | 48053 | 0.999335 |
| 15 | 2026-07-13 | validation | 32 | 48096 | 48064 | 0.999335 |
| 15 | 2026-07-14 | test_untouched | 32 | 48081 | 48036 | 0.999064 |
| 15 | 2026-07-15 | unassigned | 32 | 48095 | 48058 | 0.999231 |
| 60 | 2026-07-08 | train | 32 | 4736 | 4704 | 0.993243 |
| 60 | 2026-07-09 | train | 32 | 6943 | 6911 | 0.995391 |
| 60 | 2026-07-10 | train | 32 | 12087 | 12055 | 0.997353 |
| 60 | 2026-07-13 | validation | 32 | 12091 | 12059 | 0.997353 |
| 60 | 2026-07-14 | test_untouched | 32 | 12091 | 12054 | 0.99694 |
| 60 | 2026-07-15 | unassigned | 32 | 12095 | 12058 | 0.996941 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P181_PHASE180_PRECOMMIT_READY | 1 | phase180_precommit_ready=1 | hard |
| P181_LABEL_PARTITIONS_WRITTEN | 1 | label_partitions=768 | hard |
| P181_SPLIT_ROLES_PRESENT | 1 | split_roles=test_untouched;train;unassigned;validation | hard |
| P181_LABEL_AVAILABILITY_NONZERO | 1 | min_availability_fraction=0.993243 | hard |
| P181_NO_REPLAY_OR_PROFITABILITY_OUTPUTS | 1 | label materialization only; forbidden_outputs=signal;side;order;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | hard |

## Label Partition Inventory

| horizon_sec | trade_date | exchange | symbol | split_role | rows | label_available_rows | label_file | bytes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-07-08 | NSE | ADANIPORTS | train | 3618 | 3617 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | 114148 |
| 1 | 2026-07-08 | NSE | AXISBANK | train | 5830 | 5829 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | 180917 |
| 1 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 3324 | 3323 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | 98981 |
| 1 | 2026-07-08 | NSE | BANKBEES | train | 5646 | 5645 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | 168662 |
| 1 | 2026-07-08 | NSE | BHARTIARTL | train | 3953 | 3952 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | 107549 |
| 1 | 2026-07-08 | NSE | BPCL | train | 2853 | 2852 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | 61776 |
| 1 | 2026-07-08 | NSE | BRITANNIA | train | 2152 | 2151 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | 53845 |
| 1 | 2026-07-08 | NSE | CIPLA | train | 2954 | 2953 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | 84320 |
| 1 | 2026-07-08 | NSE | DRREDDY | train | 2936 | 2935 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=DRREDDY\receive_flow_labels.parquet | 83793 |
| 1 | 2026-07-08 | NSE | GOLDBEES | train | 4079 | 4078 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=GOLDBEES\receive_flow_labels.parquet | 88098 |
| 1 | 2026-07-08 | NSE | HCLTECH | train | 2707 | 2706 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=HCLTECH\receive_flow_labels.parquet | 72366 |
| 1 | 2026-07-08 | NSE | HDFCBANK | train | 6817 | 6816 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=HDFCBANK\receive_flow_labels.parquet | 191627 |
| 1 | 2026-07-08 | NSE | HINDUNILVR | train | 3471 | 3470 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=HINDUNILVR\receive_flow_labels.parquet | 108695 |
| 1 | 2026-07-08 | NSE | ICICIBANK | train | 6211 | 6210 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ICICIBANK\receive_flow_labels.parquet | 155540 |
| 1 | 2026-07-08 | NSE | INFY | train | 5153 | 5152 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=INFY\receive_flow_labels.parquet | 133457 |
| 1 | 2026-07-08 | NSE | ITBEES | train | 2356 | 2355 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ITBEES\receive_flow_labels.parquet | 41651 |
| 1 | 2026-07-08 | NSE | ITC | train | 4272 | 4271 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ITC\receive_flow_labels.parquet | 90191 |
| 1 | 2026-07-08 | NSE | JUNIORBEES | train | 5242 | 5241 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=JUNIORBEES\receive_flow_labels.parquet | 177377 |
| 1 | 2026-07-08 | NSE | KOTAKBANK | train | 4945 | 4944 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=KOTAKBANK\receive_flow_labels.parquet | 120162 |
| 1 | 2026-07-08 | NSE | LT | train | 6329 | 6328 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=LT\receive_flow_labels.parquet | 228992 |
| 1 | 2026-07-08 | NSE | M&M | train | 6038 | 6037 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=M&M\receive_flow_labels.parquet | 208920 |
| 1 | 2026-07-08 | NSE | MARUTI | train | 4918 | 4917 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=MARUTI\receive_flow_labels.parquet | 138491 |
| 1 | 2026-07-08 | NSE | NESTLEIND | train | 2944 | 2943 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=NESTLEIND\receive_flow_labels.parquet | 81578 |
| 1 | 2026-07-08 | NSE | NIFTYBEES | train | 5017 | 5016 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=NIFTYBEES\receive_flow_labels.parquet | 140862 |
| 1 | 2026-07-08 | NSE | ONGC | train | 4122 | 4121 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ONGC\receive_flow_labels.parquet | 123736 |
| 1 | 2026-07-08 | NSE | RELIANCE | train | 6548 | 6547 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=RELIANCE\receive_flow_labels.parquet | 161470 |
| 1 | 2026-07-08 | NSE | SBIN | train | 5500 | 5499 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=SBIN\receive_flow_labels.parquet | 147340 |
| 1 | 2026-07-08 | NSE | SUNPHARMA | train | 3353 | 3352 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=SUNPHARMA\receive_flow_labels.parquet | 98125 |
| 1 | 2026-07-08 | NSE | TCS | train | 3905 | 3904 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=TCS\receive_flow_labels.parquet | 117575 |
| 1 | 2026-07-08 | NSE | TECHM | train | 2803 | 2802 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=TECHM\receive_flow_labels.parquet | 83016 |
| 1 | 2026-07-08 | NSE | ULTRACEMCO | train | 3044 | 3043 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=ULTRACEMCO\receive_flow_labels.parquet | 78472 |
| 1 | 2026-07-08 | NSE | WIPRO | train | 2626 | 2625 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-08\exchange=NSE\symbol=WIPRO\receive_flow_labels.parquet | 78995 |
| 1 | 2026-07-09 | NSE | ADANIPORTS | train | 5554 | 5553 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | 144727 |
| 1 | 2026-07-09 | NSE | AXISBANK | train | 7447 | 7446 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | 170481 |
| 1 | 2026-07-09 | NSE | BAJAJ-AUTO | train | 5050 | 5049 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | 123211 |
| 1 | 2026-07-09 | NSE | BANKBEES | train | 8886 | 8885 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | 264789 |
| 1 | 2026-07-09 | NSE | BHARTIARTL | train | 9412 | 9411 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | 264836 |
| 1 | 2026-07-09 | NSE | BPCL | train | 4697 | 4696 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | 84369 |
| 1 | 2026-07-09 | NSE | BRITANNIA | train | 4230 | 4229 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | 95485 |
| 1 | 2026-07-09 | NSE | CIPLA | train | 4887 | 4886 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | 90286 |
| 1 | 2026-07-09 | NSE | DRREDDY | train | 9054 | 9053 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=DRREDDY\receive_flow_labels.parquet | 215642 |
| 1 | 2026-07-09 | NSE | GOLDBEES | train | 6408 | 6407 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=GOLDBEES\receive_flow_labels.parquet | 102890 |
| 1 | 2026-07-09 | NSE | HCLTECH | train | 5478 | 5477 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=HCLTECH\receive_flow_labels.parquet | 121802 |
| 1 | 2026-07-09 | NSE | HDFCBANK | train | 9420 | 9419 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=HDFCBANK\receive_flow_labels.parquet | 219351 |
| 1 | 2026-07-09 | NSE | HINDUNILVR | train | 6947 | 6946 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=HINDUNILVR\receive_flow_labels.parquet | 196510 |
| 1 | 2026-07-09 | NSE | ICICIBANK | train | 9153 | 9152 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ICICIBANK\receive_flow_labels.parquet | 201109 |
| 1 | 2026-07-09 | NSE | INFY | train | 7567 | 7566 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=INFY\receive_flow_labels.parquet | 173375 |
| 1 | 2026-07-09 | NSE | ITBEES | train | 3873 | 3872 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ITBEES\receive_flow_labels.parquet | 55819 |
| 1 | 2026-07-09 | NSE | ITC | train | 7310 | 7309 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ITC\receive_flow_labels.parquet | 108691 |
| 1 | 2026-07-09 | NSE | JUNIORBEES | train | 8590 | 8589 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=JUNIORBEES\receive_flow_labels.parquet | 260567 |
| 1 | 2026-07-09 | NSE | KOTAKBANK | train | 8944 | 8943 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=KOTAKBANK\receive_flow_labels.parquet | 179175 |
| 1 | 2026-07-09 | NSE | LT | train | 9073 | 9072 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=LT\receive_flow_labels.parquet | 274225 |
| 1 | 2026-07-09 | NSE | M&M | train | 7705 | 7704 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=M&M\receive_flow_labels.parquet | 205854 |
| 1 | 2026-07-09 | NSE | MARUTI | train | 7380 | 7379 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=MARUTI\receive_flow_labels.parquet | 146026 |
| 1 | 2026-07-09 | NSE | NESTLEIND | train | 4455 | 4454 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=NESTLEIND\receive_flow_labels.parquet | 116404 |
| 1 | 2026-07-09 | NSE | NIFTYBEES | train | 8020 | 8019 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=NIFTYBEES\receive_flow_labels.parquet | 153859 |
| 1 | 2026-07-09 | NSE | ONGC | train | 5783 | 5782 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ONGC\receive_flow_labels.parquet | 137201 |
| 1 | 2026-07-09 | NSE | RELIANCE | train | 9018 | 9017 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=RELIANCE\receive_flow_labels.parquet | 208528 |
| 1 | 2026-07-09 | NSE | SBIN | train | 7834 | 7833 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=SBIN\receive_flow_labels.parquet | 167466 |
| 1 | 2026-07-09 | NSE | SUNPHARMA | train | 7323 | 7322 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=SUNPHARMA\receive_flow_labels.parquet | 165670 |
| 1 | 2026-07-09 | NSE | TCS | train | 7970 | 7969 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=TCS\receive_flow_labels.parquet | 228746 |
| 1 | 2026-07-09 | NSE | TECHM | train | 4930 | 4929 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=TECHM\receive_flow_labels.parquet | 114346 |
| 1 | 2026-07-09 | NSE | ULTRACEMCO | train | 3980 | 3979 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=ULTRACEMCO\receive_flow_labels.parquet | 75670 |
| 1 | 2026-07-09 | NSE | WIPRO | train | 5789 | 5788 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-09\exchange=NSE\symbol=WIPRO\receive_flow_labels.parquet | 139274 |
| 1 | 2026-07-10 | NSE | ADANIPORTS | train | 9547 | 9546 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | 215352 |
| 1 | 2026-07-10 | NSE | AXISBANK | train | 10802 | 10801 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | 213792 |
| 1 | 2026-07-10 | NSE | BAJAJ-AUTO | train | 9728 | 9727 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | 227796 |
| 1 | 2026-07-10 | NSE | BANKBEES | train | 9231 | 9229 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | 234744 |
| 1 | 2026-07-10 | NSE | BHARTIARTL | train | 11366 | 11365 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | 248894 |
| 1 | 2026-07-10 | NSE | BPCL | train | 6759 | 6758 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | 106221 |
| 1 | 2026-07-10 | NSE | BRITANNIA | train | 6030 | 6029 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | 110604 |
| 1 | 2026-07-10 | NSE | CIPLA | train | 7908 | 7907 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | 165590 |
| 1 | 2026-07-10 | NSE | DRREDDY | train | 13142 | 13141 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=DRREDDY\receive_flow_labels.parquet | 313984 |
| 1 | 2026-07-10 | NSE | GOLDBEES | train | 9150 | 9148 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=GOLDBEES\receive_flow_labels.parquet | 142900 |
| 1 | 2026-07-10 | NSE | HCLTECH | train | 14318 | 14317 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=HCLTECH\receive_flow_labels.parquet | 296658 |
| 1 | 2026-07-10 | NSE | HDFCBANK | train | 15044 | 15043 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=HDFCBANK\receive_flow_labels.parquet | 255396 |
| 1 | 2026-07-10 | NSE | HINDUNILVR | train | 8662 | 8661 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=HINDUNILVR\receive_flow_labels.parquet | 187656 |
| 1 | 2026-07-10 | NSE | ICICIBANK | train | 11237 | 11236 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ICICIBANK\receive_flow_labels.parquet | 209263 |
| 1 | 2026-07-10 | NSE | INFY | train | 15211 | 15210 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=INFY\receive_flow_labels.parquet | 312721 |
| 1 | 2026-07-10 | NSE | ITBEES | train | 6824 | 6822 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ITBEES\receive_flow_labels.parquet | 82645 |
| 1 | 2026-07-10 | NSE | ITC | train | 11085 | 11084 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ITC\receive_flow_labels.parquet | 153754 |
| 1 | 2026-07-10 | NSE | JUNIORBEES | train | 13254 | 13252 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=JUNIORBEES\receive_flow_labels.parquet | 355610 |
| 1 | 2026-07-10 | NSE | KOTAKBANK | train | 10165 | 10164 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=KOTAKBANK\receive_flow_labels.parquet | 169492 |
| 1 | 2026-07-10 | NSE | LT | train | 10641 | 10640 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=LT\receive_flow_labels.parquet | 236680 |
| 1 | 2026-07-10 | NSE | M&M | train | 9988 | 9987 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=M&M\receive_flow_labels.parquet | 203878 |
| 1 | 2026-07-10 | NSE | MARUTI | train | 11105 | 11104 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=MARUTI\receive_flow_labels.parquet | 220255 |
| 1 | 2026-07-10 | NSE | NESTLEIND | train | 7879 | 7878 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=NESTLEIND\receive_flow_labels.parquet | 180602 |
| 1 | 2026-07-10 | NSE | NIFTYBEES | train | 11228 | 11226 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=NIFTYBEES\receive_flow_labels.parquet | 181808 |
| 1 | 2026-07-10 | NSE | ONGC | train | 9396 | 9395 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ONGC\receive_flow_labels.parquet | 187639 |
| 1 | 2026-07-10 | NSE | RELIANCE | train | 11460 | 11459 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=RELIANCE\receive_flow_labels.parquet | 207744 |
| 1 | 2026-07-10 | NSE | SBIN | train | 12206 | 12205 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=SBIN\receive_flow_labels.parquet | 261284 |
| 1 | 2026-07-10 | NSE | SUNPHARMA | train | 9909 | 9908 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=SUNPHARMA\receive_flow_labels.parquet | 242570 |
| 1 | 2026-07-10 | NSE | TCS | train | 16260 | 16259 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=TCS\receive_flow_labels.parquet | 444590 |
| 1 | 2026-07-10 | NSE | TECHM | train | 9552 | 9551 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=TECHM\receive_flow_labels.parquet | 239136 |
| 1 | 2026-07-10 | NSE | ULTRACEMCO | train | 6526 | 6525 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=ULTRACEMCO\receive_flow_labels.parquet | 116453 |
| 1 | 2026-07-10 | NSE | WIPRO | train | 10158 | 10157 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-10\exchange=NSE\symbol=WIPRO\receive_flow_labels.parquet | 223475 |
| 1 | 2026-07-13 | NSE | ADANIPORTS | validation | 9454 | 9453 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | 236185 |
| 1 | 2026-07-13 | NSE | AXISBANK | validation | 10798 | 10797 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | 226754 |
| 1 | 2026-07-13 | NSE | BAJAJ-AUTO | validation | 14299 | 14298 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | 382914 |
| 1 | 2026-07-13 | NSE | BANKBEES | validation | 13184 | 13183 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | 302063 |
| 1 | 2026-07-13 | NSE | BHARTIARTL | validation | 11539 | 11538 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | 251386 |
| 1 | 2026-07-13 | NSE | BPCL | validation | 8035 | 8034 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | 118625 |
| 1 | 2026-07-13 | NSE | BRITANNIA | validation | 6760 | 6759 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | 107659 |
| 1 | 2026-07-13 | NSE | CIPLA | validation | 8388 | 8387 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | 177305 |
| 1 | 2026-07-13 | NSE | DRREDDY | validation | 8736 | 8735 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=DRREDDY\receive_flow_labels.parquet | 207736 |
| 1 | 2026-07-13 | NSE | GOLDBEES | validation | 8948 | 8947 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=GOLDBEES\receive_flow_labels.parquet | 145886 |
| 1 | 2026-07-13 | NSE | HCLTECH | validation | 14297 | 14296 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=HCLTECH\receive_flow_labels.parquet | 418421 |
| 1 | 2026-07-13 | NSE | HDFCBANK | validation | 16566 | 16565 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=HDFCBANK\receive_flow_labels.parquet | 389414 |
| 1 | 2026-07-13 | NSE | HINDUNILVR | validation | 8592 | 8591 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=HINDUNILVR\receive_flow_labels.parquet | 202918 |
| 1 | 2026-07-13 | NSE | ICICIBANK | validation | 13717 | 13716 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ICICIBANK\receive_flow_labels.parquet | 313181 |
| 1 | 2026-07-13 | NSE | INFY | validation | 16207 | 16206 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=INFY\receive_flow_labels.parquet | 459065 |
| 1 | 2026-07-13 | NSE | ITBEES | validation | 8306 | 8304 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ITBEES\receive_flow_labels.parquet | 126039 |
| 1 | 2026-07-13 | NSE | ITC | validation | 8758 | 8757 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ITC\receive_flow_labels.parquet | 107381 |
| 1 | 2026-07-13 | NSE | JUNIORBEES | validation | 11802 | 11801 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=JUNIORBEES\receive_flow_labels.parquet | 318806 |
| 1 | 2026-07-13 | NSE | KOTAKBANK | validation | 9403 | 9402 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=KOTAKBANK\receive_flow_labels.parquet | 174712 |
| 1 | 2026-07-13 | NSE | LT | validation | 11479 | 11478 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=LT\receive_flow_labels.parquet | 317709 |
| 1 | 2026-07-13 | NSE | M&M | validation | 14146 | 14145 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=M&M\receive_flow_labels.parquet | 415021 |
| 1 | 2026-07-13 | NSE | MARUTI | validation | 15407 | 15406 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=MARUTI\receive_flow_labels.parquet | 324431 |
| 1 | 2026-07-13 | NSE | NESTLEIND | validation | 9036 | 9035 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=NESTLEIND\receive_flow_labels.parquet | 193381 |
| 1 | 2026-07-13 | NSE | NIFTYBEES | validation | 13040 | 13039 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=NIFTYBEES\receive_flow_labels.parquet | 264417 |
| 1 | 2026-07-13 | NSE | ONGC | validation | 10645 | 10644 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ONGC\receive_flow_labels.parquet | 235625 |
| 1 | 2026-07-13 | NSE | RELIANCE | validation | 13220 | 13219 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=RELIANCE\receive_flow_labels.parquet | 252372 |
| 1 | 2026-07-13 | NSE | SBIN | validation | 13085 | 13084 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=SBIN\receive_flow_labels.parquet | 264797 |
| 1 | 2026-07-13 | NSE | SUNPHARMA | validation | 9573 | 9572 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=SUNPHARMA\receive_flow_labels.parquet | 226319 |
| 1 | 2026-07-13 | NSE | TCS | validation | 16807 | 16806 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=TCS\receive_flow_labels.parquet | 555454 |
| 1 | 2026-07-13 | NSE | TECHM | validation | 11317 | 11316 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=TECHM\receive_flow_labels.parquet | 328701 |
| 1 | 2026-07-13 | NSE | ULTRACEMCO | validation | 6784 | 6783 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=ULTRACEMCO\receive_flow_labels.parquet | 124835 |
| 1 | 2026-07-13 | NSE | WIPRO | validation | 11491 | 11490 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-13\exchange=NSE\symbol=WIPRO\receive_flow_labels.parquet | 331185 |
| 1 | 2026-07-14 | NSE | ADANIPORTS | test_untouched | 9871 | 9870 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | 269550 |
| 1 | 2026-07-14 | NSE | AXISBANK | test_untouched | 12369 | 12367 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | 315757 |
| 1 | 2026-07-14 | NSE | BAJAJ-AUTO | test_untouched | 15119 | 15118 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | 390681 |
| 1 | 2026-07-14 | NSE | BANKBEES | test_untouched | 12042 | 12039 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | 303210 |
| 1 | 2026-07-14 | NSE | BHARTIARTL | test_untouched | 13068 | 13067 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | 340080 |
| 1 | 2026-07-14 | NSE | BPCL | test_untouched | 8730 | 8728 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | 140994 |
| 1 | 2026-07-14 | NSE | BRITANNIA | test_untouched | 8238 | 8237 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | 163899 |
| 1 | 2026-07-14 | NSE | CIPLA | test_untouched | 8978 | 8977 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | 230348 |
| 1 | 2026-07-14 | NSE | DRREDDY | test_untouched | 8456 | 8455 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=DRREDDY\receive_flow_labels.parquet | 185237 |
| 1 | 2026-07-14 | NSE | GOLDBEES | test_untouched | 9933 | 9931 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=GOLDBEES\receive_flow_labels.parquet | 154312 |
| 1 | 2026-07-14 | NSE | HCLTECH | test_untouched | 15678 | 15676 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=HCLTECH\receive_flow_labels.parquet | 435824 |
| 1 | 2026-07-14 | NSE | HDFCBANK | test_untouched | 15864 | 15863 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=HDFCBANK\receive_flow_labels.parquet | 367068 |
| 1 | 2026-07-14 | NSE | HINDUNILVR | test_untouched | 10846 | 10845 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=HINDUNILVR\receive_flow_labels.parquet | 316893 |
| 1 | 2026-07-14 | NSE | ICICIBANK | test_untouched | 13574 | 13573 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ICICIBANK\receive_flow_labels.parquet | 316207 |
| 1 | 2026-07-14 | NSE | INFY | test_untouched | 15629 | 15628 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=INFY\receive_flow_labels.parquet | 353322 |
| 1 | 2026-07-14 | NSE | ITBEES | test_untouched | 6618 | 6615 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ITBEES\receive_flow_labels.parquet | 95677 |
| 1 | 2026-07-14 | NSE | ITC | test_untouched | 12350 | 12348 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ITC\receive_flow_labels.parquet | 180888 |
| 1 | 2026-07-14 | NSE | JUNIORBEES | test_untouched | 11963 | 11960 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=JUNIORBEES\receive_flow_labels.parquet | 359781 |
| 1 | 2026-07-14 | NSE | KOTAKBANK | test_untouched | 11204 | 11202 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=KOTAKBANK\receive_flow_labels.parquet | 235799 |
| 1 | 2026-07-14 | NSE | LT | test_untouched | 12561 | 12560 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=LT\receive_flow_labels.parquet | 345974 |
| 1 | 2026-07-14 | NSE | M&M | test_untouched | 13068 | 13067 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=M&M\receive_flow_labels.parquet | 375709 |
| 1 | 2026-07-14 | NSE | MARUTI | test_untouched | 11008 | 11007 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=MARUTI\receive_flow_labels.parquet | 245105 |
| 1 | 2026-07-14 | NSE | NESTLEIND | test_untouched | 9368 | 9367 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=NESTLEIND\receive_flow_labels.parquet | 217824 |
| 1 | 2026-07-14 | NSE | NIFTYBEES | test_untouched | 11590 | 11587 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=NIFTYBEES\receive_flow_labels.parquet | 229724 |
| 1 | 2026-07-14 | NSE | ONGC | test_untouched | 10278 | 10277 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ONGC\receive_flow_labels.parquet | 233579 |
| 1 | 2026-07-14 | NSE | RELIANCE | test_untouched | 13625 | 13623 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=RELIANCE\receive_flow_labels.parquet | 299592 |
| 1 | 2026-07-14 | NSE | SBIN | test_untouched | 12764 | 12762 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=SBIN\receive_flow_labels.parquet | 274681 |
| 1 | 2026-07-14 | NSE | SUNPHARMA | test_untouched | 11509 | 11508 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=SUNPHARMA\receive_flow_labels.parquet | 309368 |
| 1 | 2026-07-14 | NSE | TCS | test_untouched | 15792 | 15791 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=TCS\receive_flow_labels.parquet | 463625 |
| 1 | 2026-07-14 | NSE | TECHM | test_untouched | 11095 | 11094 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=TECHM\receive_flow_labels.parquet | 336805 |
| 1 | 2026-07-14 | NSE | ULTRACEMCO | test_untouched | 7965 | 7964 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=ULTRACEMCO\receive_flow_labels.parquet | 157303 |
| 1 | 2026-07-14 | NSE | WIPRO | test_untouched | 9396 | 9394 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-14\exchange=NSE\symbol=WIPRO\receive_flow_labels.parquet | 242534 |
| 1 | 2026-07-15 | NSE | ADANIPORTS | unassigned | 10123 | 10122 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | 246303 |
| 1 | 2026-07-15 | NSE | AXISBANK | unassigned | 15634 | 15633 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | 417756 |
| 1 | 2026-07-15 | NSE | BAJAJ-AUTO | unassigned | 14797 | 14796 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | 361926 |
| 1 | 2026-07-15 | NSE | BANKBEES | unassigned | 12146 | 12143 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | 308646 |
| 1 | 2026-07-15 | NSE | BHARTIARTL | unassigned | 11420 | 11419 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | 251524 |
| 1 | 2026-07-15 | NSE | BPCL | unassigned | 8175 | 8174 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | 115010 |
| 1 | 2026-07-15 | NSE | BRITANNIA | unassigned | 6463 | 6462 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | 117938 |
| 1 | 2026-07-15 | NSE | CIPLA | unassigned | 8702 | 8701 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | 195999 |
| 1 | 2026-07-15 | NSE | DRREDDY | unassigned | 7818 | 7817 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=DRREDDY\receive_flow_labels.parquet | 150976 |
| 1 | 2026-07-15 | NSE | GOLDBEES | unassigned | 9171 | 9168 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=GOLDBEES\receive_flow_labels.parquet | 144981 |
| 1 | 2026-07-15 | NSE | HCLTECH | unassigned | 10358 | 10357 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=HCLTECH\receive_flow_labels.parquet | 243524 |
| 1 | 2026-07-15 | NSE | HDFCBANK | unassigned | 15203 | 15202 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=HDFCBANK\receive_flow_labels.parquet | 317092 |
| 1 | 2026-07-15 | NSE | HINDUNILVR | unassigned | 9061 | 9060 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=HINDUNILVR\receive_flow_labels.parquet | 215385 |
| 1 | 2026-07-15 | NSE | ICICIBANK | unassigned | 14980 | 14979 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=ICICIBANK\receive_flow_labels.parquet | 323954 |
| 1 | 2026-07-15 | NSE | INFY | unassigned | 15271 | 15270 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=INFY\receive_flow_labels.parquet | 328717 |
| 1 | 2026-07-15 | NSE | ITBEES | unassigned | 6727 | 6724 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=ITBEES\receive_flow_labels.parquet | 89810 |
| 1 | 2026-07-15 | NSE | ITC | unassigned | 9670 | 9669 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=ITC\receive_flow_labels.parquet | 137475 |
| 1 | 2026-07-15 | NSE | JUNIORBEES | unassigned | 14353 | 14350 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=JUNIORBEES\receive_flow_labels.parquet | 401156 |
| 1 | 2026-07-15 | NSE | KOTAKBANK | unassigned | 9572 | 9571 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=KOTAKBANK\receive_flow_labels.parquet | 186922 |
| 1 | 2026-07-15 | NSE | LT | unassigned | 13054 | 13053 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=LT\receive_flow_labels.parquet | 358164 |
| 1 | 2026-07-15 | NSE | M&M | unassigned | 14536 | 14535 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=M&M\receive_flow_labels.parquet | 353591 |
| 1 | 2026-07-15 | NSE | MARUTI | unassigned | 11030 | 11029 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=MARUTI\receive_flow_labels.parquet | 218250 |
| 1 | 2026-07-15 | NSE | NESTLEIND | unassigned | 7020 | 7019 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=NESTLEIND\receive_flow_labels.parquet | 144467 |
| 1 | 2026-07-15 | NSE | NIFTYBEES | unassigned | 13048 | 13045 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=NIFTYBEES\receive_flow_labels.parquet | 248819 |
| 1 | 2026-07-15 | NSE | ONGC | unassigned | 10933 | 10932 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=ONGC\receive_flow_labels.parquet | 228603 |
| 1 | 2026-07-15 | NSE | RELIANCE | unassigned | 13692 | 13691 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=RELIANCE\receive_flow_labels.parquet | 250211 |
| 1 | 2026-07-15 | NSE | SBIN | unassigned | 14130 | 14129 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=SBIN\receive_flow_labels.parquet | 308498 |
| 1 | 2026-07-15 | NSE | SUNPHARMA | unassigned | 11790 | 11789 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=SUNPHARMA\receive_flow_labels.parquet | 283027 |
| 1 | 2026-07-15 | NSE | TCS | unassigned | 15134 | 15133 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=TCS\receive_flow_labels.parquet | 394436 |
| 1 | 2026-07-15 | NSE | TECHM | unassigned | 12409 | 12408 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=TECHM\receive_flow_labels.parquet | 321223 |
| 1 | 2026-07-15 | NSE | ULTRACEMCO | unassigned | 9876 | 9875 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=ULTRACEMCO\receive_flow_labels.parquet | 185980 |
| 1 | 2026-07-15 | NSE | WIPRO | unassigned | 9447 | 9446 | derived_real_l2_receive_flow_labels_phase181\horizon=1s\trade_date=2026-07-15\exchange=NSE\symbol=WIPRO\receive_flow_labels.parquet | 224579 |
| 5 | 2026-07-08 | NSE | ADANIPORTS | train | 1618 | 1617 | derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=ADANIPORTS\receive_flow_labels.parquet | 67719 |
| 5 | 2026-07-08 | NSE | AXISBANK | train | 1700 | 1699 | derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=AXISBANK\receive_flow_labels.parquet | 72802 |
| 5 | 2026-07-08 | NSE | BAJAJ-AUTO | train | 1595 | 1594 | derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BAJAJ-AUTO\receive_flow_labels.parquet | 63720 |
| 5 | 2026-07-08 | NSE | BANKBEES | train | 1694 | 1693 | derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BANKBEES\receive_flow_labels.parquet | 69154 |
| 5 | 2026-07-08 | NSE | BHARTIARTL | train | 1617 | 1616 | derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BHARTIARTL\receive_flow_labels.parquet | 61736 |
| 5 | 2026-07-08 | NSE | BPCL | train | 1579 | 1578 | derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BPCL\receive_flow_labels.parquet | 44613 |
| 5 | 2026-07-08 | NSE | BRITANNIA | train | 1526 | 1525 | derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=BRITANNIA\receive_flow_labels.parquet | 46569 |
| 5 | 2026-07-08 | NSE | CIPLA | train | 1573 | 1572 | derived_real_l2_receive_flow_labels_phase181\horizon=5s\trade_date=2026-07-08\exchange=NSE\symbol=CIPLA\receive_flow_labels.parquet | 61206 |

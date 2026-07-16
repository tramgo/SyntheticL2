# Phase 50 Dense Lake Shard Planner

Generated UTC: 2026-07-16T15:22:11.272141+00:00

This phase converts the Phase49 dense calibration into a full symbol-month shard schedule for the 80GB-class dense target and validates the plan with a bounded multi-symbol materialization.
It is storage/input orchestration evidence, not strategy acceptance evidence.

## Planner Summary

| metric | value | description |
| --- | --- | --- |
| phase50_target_dense_raw_gb | 83.24 | Target compressed dense raw lake size |
| phase50_target_dense_rows | 5.97463e+09 | Dense rows implied by Phase49 measured compression |
| phase50_target_full_universe_multiplier | 1983.41 | Full-universe multiplier implied by target dense rows |
| phase50_schedule_shards | 384 | Symbol-month shards in full dense target schedule |
| phase50_schedule_source_rows | 3012294 | Current compact monthly source rows covered by schedule |
| phase50_schedule_estimated_dense_bytes | 8.93783e+10 | Estimated compressed bytes for target schedule |
| phase50_schedule_estimated_runtime_hours | 4.30225 | Estimated runtime hours at Phase49 measured throughput |
| phase50_selected_symbols | HDFCBANK;INFY;RELIANCE | Symbols selected for bounded materialization |
| phase50_selected_shards | 36 | Selected symbol-month shards for bounded materialization |
| phase50_materialized_dense_rows | 18068416 | Dense rows materialized in bounded multi-symbol run |
| phase50_materialized_dense_bytes | 269683823 | Compressed bytes materialized in bounded multi-symbol run |
| phase50_materialized_partition_files | 36 | Dense parquet files written in bounded run |
| phase50_dense_output_root | raw_synthetic_l2_dense_phase50_multisymbol_x64 | Local bounded dense output root; ignored by Git |
| phase50_full_80gb_dense_lake_materialized | 0 | 80GB-class dense full-universe lake not materialized by Phase50 |
| phase50_synthetic_full_year_acceptance_ready | 0 | Dense shard planning is storage/input evidence, not strategy acceptance |

## Bounded Run Plan

| shard_id | trade_month | symbol | source_rows | target_dense_multiplier | target_dense_rows | estimated_dense_bytes | estimated_runtime_seconds | planned_materialization_multiplier | planned_dense_rows | materialization_scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dense_target_HDFCBANK_2026-01 | 2026-01 | HDFCBANK | 8220 | 1983.41 | 16303665 | 2.43897e+08 | 42.2642 | 64 | 526080 | phase50_bounded_multisymbol_validation_shard |
| dense_target_HDFCBANK_2026-02 | 2026-02 | HDFCBANK | 7476 | 1983.41 | 14828005 | 2.21822e+08 | 38.4388 | 64 | 478464 | phase50_bounded_multisymbol_validation_shard |
| dense_target_HDFCBANK_2026-03 | 2026-03 | HDFCBANK | 8220 | 1983.41 | 16303665 | 2.43897e+08 | 42.2642 | 64 | 526080 | phase50_bounded_multisymbol_validation_shard |
| dense_target_HDFCBANK_2026-04 | 2026-04 | HDFCBANK | 8212 | 1983.41 | 16287798 | 2.4366e+08 | 42.2231 | 64 | 525568 | phase50_bounded_multisymbol_validation_shard |
| dense_target_HDFCBANK_2026-05 | 2026-05 | HDFCBANK | 7848 | 1983.41 | 15565835 | 2.32859e+08 | 40.3515 | 64 | 502272 | phase50_bounded_multisymbol_validation_shard |
| dense_target_HDFCBANK_2026-06 | 2026-06 | HDFCBANK | 8198 | 1983.41 | 16260030 | 2.43244e+08 | 42.1511 | 64 | 524672 | phase50_bounded_multisymbol_validation_shard |
| dense_target_HDFCBANK_2026-07 | 2026-07 | HDFCBANK | 8587 | 1983.41 | 17031579 | 2.54786e+08 | 44.1512 | 64 | 549568 | phase50_bounded_multisymbol_validation_shard |
| dense_target_HDFCBANK_2026-08 | 2026-08 | HDFCBANK | 7841 | 1983.41 | 15551951 | 2.32652e+08 | 40.3155 | 64 | 501824 | phase50_bounded_multisymbol_validation_shard |
| dense_target_HDFCBANK_2026-09 | 2026-09 | HDFCBANK | 8208 | 1983.41 | 16279864 | 2.43541e+08 | 42.2025 | 64 | 525312 | phase50_bounded_multisymbol_validation_shard |
| dense_target_HDFCBANK_2026-10 | 2026-10 | HDFCBANK | 8212 | 1983.41 | 16287798 | 2.4366e+08 | 42.2231 | 64 | 525568 | phase50_bounded_multisymbol_validation_shard |
| dense_target_HDFCBANK_2026-11 | 2026-11 | HDFCBANK | 7858 | 1983.41 | 15585669 | 2.33156e+08 | 40.4029 | 64 | 502912 | phase50_bounded_multisymbol_validation_shard |
| dense_target_HDFCBANK_2026-12 | 2026-12 | HDFCBANK | 5230 | 1983.41 | 10373257 | 1.5518e+08 | 26.8907 | 64 | 334720 | phase50_bounded_multisymbol_validation_shard |
| dense_target_INFY_2026-01 | 2026-01 | INFY | 8225 | 1983.41 | 16313583 | 2.44045e+08 | 42.2899 | 64 | 526400 | phase50_bounded_multisymbol_validation_shard |
| dense_target_INFY_2026-02 | 2026-02 | INFY | 7459 | 1983.41 | 14794287 | 2.21317e+08 | 38.3514 | 64 | 477376 | phase50_bounded_multisymbol_validation_shard |
| dense_target_INFY_2026-03 | 2026-03 | INFY | 8210 | 1983.41 | 16283831 | 2.436e+08 | 42.2128 | 64 | 525440 | phase50_bounded_multisymbol_validation_shard |
| dense_target_INFY_2026-04 | 2026-04 | INFY | 8197 | 1983.41 | 16258047 | 2.43215e+08 | 42.1459 | 64 | 524608 | phase50_bounded_multisymbol_validation_shard |
| dense_target_INFY_2026-05 | 2026-05 | INFY | 7857 | 1983.41 | 15583686 | 2.33126e+08 | 40.3978 | 64 | 502848 | phase50_bounded_multisymbol_validation_shard |
| dense_target_INFY_2026-06 | 2026-06 | INFY | 8222 | 1983.41 | 16307632 | 2.43956e+08 | 42.2745 | 64 | 526208 | phase50_bounded_multisymbol_validation_shard |
| dense_target_INFY_2026-07 | 2026-07 | INFY | 8598 | 1983.41 | 17053396 | 2.55113e+08 | 44.2077 | 64 | 550272 | phase50_bounded_multisymbol_validation_shard |
| dense_target_INFY_2026-08 | 2026-08 | INFY | 7848 | 1983.41 | 15565835 | 2.32859e+08 | 40.3515 | 64 | 502272 | phase50_bounded_multisymbol_validation_shard |
| dense_target_INFY_2026-09 | 2026-09 | INFY | 8223 | 1983.41 | 16309616 | 2.43986e+08 | 42.2796 | 64 | 526272 | phase50_bounded_multisymbol_validation_shard |
| dense_target_INFY_2026-10 | 2026-10 | INFY | 8221 | 1983.41 | 16305649 | 2.43927e+08 | 42.2693 | 64 | 526144 | phase50_bounded_multisymbol_validation_shard |
| dense_target_INFY_2026-11 | 2026-11 | INFY | 7829 | 1983.41 | 15528150 | 2.32296e+08 | 40.2538 | 64 | 501056 | phase50_bounded_multisymbol_validation_shard |
| dense_target_INFY_2026-12 | 2026-12 | INFY | 5222 | 1983.41 | 10357389 | 1.54943e+08 | 26.8496 | 64 | 334208 | phase50_bounded_multisymbol_validation_shard |
| dense_target_RELIANCE_2026-01 | 2026-01 | RELIANCE | 8214 | 1983.41 | 16291765 | 2.43719e+08 | 42.2334 | 64 | 525696 | phase50_bounded_multisymbol_validation_shard |
| dense_target_RELIANCE_2026-02 | 2026-02 | RELIANCE | 7453 | 1983.41 | 14782387 | 2.21139e+08 | 38.3206 | 64 | 476992 | phase50_bounded_multisymbol_validation_shard |
| dense_target_RELIANCE_2026-03 | 2026-03 | RELIANCE | 8223 | 1983.41 | 16309616 | 2.43986e+08 | 42.2796 | 64 | 526272 | phase50_bounded_multisymbol_validation_shard |
| dense_target_RELIANCE_2026-04 | 2026-04 | RELIANCE | 8212 | 1983.41 | 16287798 | 2.4366e+08 | 42.2231 | 64 | 525568 | phase50_bounded_multisymbol_validation_shard |
| dense_target_RELIANCE_2026-05 | 2026-05 | RELIANCE | 7853 | 1983.41 | 15575752 | 2.33008e+08 | 40.3772 | 64 | 502592 | phase50_bounded_multisymbol_validation_shard |
| dense_target_RELIANCE_2026-06 | 2026-06 | RELIANCE | 8210 | 1983.41 | 16283831 | 2.436e+08 | 42.2128 | 64 | 525440 | phase50_bounded_multisymbol_validation_shard |
| dense_target_RELIANCE_2026-07 | 2026-07 | RELIANCE | 8590 | 1983.41 | 17037529 | 2.54875e+08 | 44.1666 | 64 | 549760 | phase50_bounded_multisymbol_validation_shard |
| dense_target_RELIANCE_2026-08 | 2026-08 | RELIANCE | 7850 | 1983.41 | 15569802 | 2.32919e+08 | 40.3618 | 64 | 502400 | phase50_bounded_multisymbol_validation_shard |
| dense_target_RELIANCE_2026-09 | 2026-09 | RELIANCE | 8223 | 1983.41 | 16309616 | 2.43986e+08 | 42.2796 | 64 | 526272 | phase50_bounded_multisymbol_validation_shard |
| dense_target_RELIANCE_2026-10 | 2026-10 | RELIANCE | 8205 | 1983.41 | 16273914 | 2.43452e+08 | 42.1871 | 64 | 525120 | phase50_bounded_multisymbol_validation_shard |
| dense_target_RELIANCE_2026-11 | 2026-11 | RELIANCE | 7838 | 1983.41 | 15546001 | 2.32563e+08 | 40.3001 | 64 | 501632 | phase50_bounded_multisymbol_validation_shard |
| dense_target_RELIANCE_2026-12 | 2026-12 | RELIANCE | 5227 | 1983.41 | 10367306 | 1.55091e+08 | 26.8753 | 64 | 334528 | phase50_bounded_multisymbol_validation_shard |

## Bounded Materialization Inventory

| trade_month | symbol | source_rows | dense_rows | multiplier | file_path | bytes | elapsed_seconds_total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | HDFCBANK | 8220 | 526080 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | 7746199 | 44.4089 |
| 2026-01 | INFY | 8225 | 526400 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-01\symbol=INFY\part-00000.parquet | 7552839 | 44.4089 |
| 2026-01 | RELIANCE | 8214 | 525696 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-01\symbol=RELIANCE\part-00000.parquet | 7756457 | 44.4089 |
| 2026-02 | HDFCBANK | 7476 | 478464 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-02\symbol=HDFCBANK\part-00000.parquet | 7252358 | 44.4089 |
| 2026-02 | INFY | 7459 | 477376 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-02\symbol=INFY\part-00000.parquet | 7202238 | 44.4089 |
| 2026-02 | RELIANCE | 7453 | 476992 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-02\symbol=RELIANCE\part-00000.parquet | 7216376 | 44.4089 |
| 2026-03 | HDFCBANK | 8220 | 526080 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-03\symbol=HDFCBANK\part-00000.parquet | 7781793 | 44.4089 |
| 2026-03 | INFY | 8210 | 525440 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-03\symbol=INFY\part-00000.parquet | 7723522 | 44.4089 |
| 2026-03 | RELIANCE | 8223 | 526272 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-03\symbol=RELIANCE\part-00000.parquet | 7734792 | 44.4089 |
| 2026-04 | HDFCBANK | 8212 | 525568 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-04\symbol=HDFCBANK\part-00000.parquet | 7785363 | 44.4089 |
| 2026-04 | INFY | 8197 | 524608 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-04\symbol=INFY\part-00000.parquet | 7792672 | 44.4089 |
| 2026-04 | RELIANCE | 8212 | 525568 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-04\symbol=RELIANCE\part-00000.parquet | 7794170 | 44.4089 |
| 2026-05 | HDFCBANK | 7848 | 502272 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-05\symbol=HDFCBANK\part-00000.parquet | 7516891 | 44.4089 |
| 2026-05 | INFY | 7857 | 502848 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-05\symbol=INFY\part-00000.parquet | 7541714 | 44.4089 |
| 2026-05 | RELIANCE | 7853 | 502592 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-05\symbol=RELIANCE\part-00000.parquet | 7485134 | 44.4089 |
| 2026-06 | HDFCBANK | 8198 | 524672 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-06\symbol=HDFCBANK\part-00000.parquet | 7724067 | 44.4089 |
| 2026-06 | INFY | 8222 | 526208 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-06\symbol=INFY\part-00000.parquet | 7718394 | 44.4089 |
| 2026-06 | RELIANCE | 8210 | 525440 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-06\symbol=RELIANCE\part-00000.parquet | 7705117 | 44.4089 |
| 2026-07 | HDFCBANK | 8587 | 549568 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-07\symbol=HDFCBANK\part-00000.parquet | 8029165 | 44.4089 |
| 2026-07 | INFY | 8598 | 550272 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-07\symbol=INFY\part-00000.parquet | 8064036 | 44.4089 |
| 2026-07 | RELIANCE | 8590 | 549760 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-07\symbol=RELIANCE\part-00000.parquet | 8065105 | 44.4089 |
| 2026-08 | HDFCBANK | 7841 | 501824 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-08\symbol=HDFCBANK\part-00000.parquet | 7459772 | 44.4089 |
| 2026-08 | INFY | 7848 | 502272 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-08\symbol=INFY\part-00000.parquet | 7482198 | 44.4089 |
| 2026-08 | RELIANCE | 7850 | 502400 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-08\symbol=RELIANCE\part-00000.parquet | 7503701 | 44.4089 |
| 2026-09 | HDFCBANK | 8208 | 525312 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-09\symbol=HDFCBANK\part-00000.parquet | 7872523 | 44.4089 |
| 2026-09 | INFY | 8223 | 526272 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-09\symbol=INFY\part-00000.parquet | 7798069 | 44.4089 |
| 2026-09 | RELIANCE | 8223 | 526272 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-09\symbol=RELIANCE\part-00000.parquet | 7802326 | 44.4089 |
| 2026-10 | HDFCBANK | 8212 | 525568 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-10\symbol=HDFCBANK\part-00000.parquet | 7769526 | 44.4089 |
| 2026-10 | INFY | 8221 | 526144 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-10\symbol=INFY\part-00000.parquet | 7678045 | 44.4089 |
| 2026-10 | RELIANCE | 8205 | 525120 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-10\symbol=RELIANCE\part-00000.parquet | 7736371 | 44.4089 |
| 2026-11 | HDFCBANK | 7858 | 502912 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-11\symbol=HDFCBANK\part-00000.parquet | 7523741 | 44.4089 |
| 2026-11 | INFY | 7829 | 501056 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-11\symbol=INFY\part-00000.parquet | 7432648 | 44.4089 |
| 2026-11 | RELIANCE | 7838 | 501632 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-11\symbol=RELIANCE\part-00000.parquet | 7464539 | 44.4089 |
| 2026-12 | HDFCBANK | 5230 | 334720 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-12\symbol=HDFCBANK\part-00000.parquet | 5641113 | 44.4089 |
| 2026-12 | INFY | 5222 | 334208 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-12\symbol=INFY\part-00000.parquet | 5628116 | 44.4089 |
| 2026-12 | RELIANCE | 5227 | 334528 | 64 | raw_synthetic_l2_dense_phase50_multisymbol_x64\trade_month=2026-12\symbol=RELIANCE\part-00000.parquet | 5702733 | 44.4089 |

## Top Target Schedule Shards

| shard_id | trade_month | symbol | source_rows | target_dense_multiplier | target_dense_rows | estimated_dense_bytes | estimated_runtime_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dense_target_NESTLEIND_2026-07 | 2026-07 | NESTLEIND | 8611 | 1983.41 | 17079180 | 2.55498e+08 | 44.2746 |
| dense_target_JUNIORBEES_2026-07 | 2026-07 | JUNIORBEES | 8608 | 1983.41 | 17073230 | 2.55409e+08 | 44.2592 |
| dense_target_SBIN_2026-07 | 2026-07 | SBIN | 8607 | 1983.41 | 17071247 | 2.5538e+08 | 44.254 |
| dense_target_BANKBEES_2026-07 | 2026-07 | BANKBEES | 8606 | 1983.41 | 17069263 | 2.5535e+08 | 44.2489 |
| dense_target_BPCL_2026-07 | 2026-07 | BPCL | 8602 | 1983.41 | 17061330 | 2.55231e+08 | 44.2283 |
| dense_target_ADANIPORTS_2026-07 | 2026-07 | ADANIPORTS | 8601 | 1983.41 | 17059346 | 2.55202e+08 | 44.2232 |
| dense_target_AXISBANK_2026-07 | 2026-07 | AXISBANK | 8601 | 1983.41 | 17059346 | 2.55202e+08 | 44.2232 |
| dense_target_GOLDBEES_2026-07 | 2026-07 | GOLDBEES | 8601 | 1983.41 | 17059346 | 2.55202e+08 | 44.2232 |
| dense_target_NIFTYBEES_2026-07 | 2026-07 | NIFTYBEES | 8600 | 1983.41 | 17057363 | 2.55172e+08 | 44.218 |
| dense_target_SUNPHARMA_2026-07 | 2026-07 | SUNPHARMA | 8600 | 1983.41 | 17057363 | 2.55172e+08 | 44.218 |
| dense_target_BHARTIARTL_2026-07 | 2026-07 | BHARTIARTL | 8599 | 1983.41 | 17055379 | 2.55142e+08 | 44.2129 |
| dense_target_ITBEES_2026-07 | 2026-07 | ITBEES | 8599 | 1983.41 | 17055379 | 2.55142e+08 | 44.2129 |
| dense_target_INFY_2026-07 | 2026-07 | INFY | 8598 | 1983.41 | 17053396 | 2.55113e+08 | 44.2077 |
| dense_target_MARUTI_2026-07 | 2026-07 | MARUTI | 8598 | 1983.41 | 17053396 | 2.55113e+08 | 44.2077 |
| dense_target_HINDUNILVR_2026-07 | 2026-07 | HINDUNILVR | 8597 | 1983.41 | 17051413 | 2.55083e+08 | 44.2026 |
| dense_target_M&M_2026-07 | 2026-07 | M&M | 8597 | 1983.41 | 17051413 | 2.55083e+08 | 44.2026 |
| dense_target_ULTRACEMCO_2026-07 | 2026-07 | ULTRACEMCO | 8595 | 1983.41 | 17047446 | 2.55024e+08 | 44.1923 |
| dense_target_CIPLA_2026-07 | 2026-07 | CIPLA | 8594 | 1983.41 | 17045462 | 2.54994e+08 | 44.1872 |
| dense_target_WIPRO_2026-07 | 2026-07 | WIPRO | 8593 | 1983.41 | 17043479 | 2.54964e+08 | 44.182 |
| dense_target_BAJAJ-AUTO_2026-07 | 2026-07 | BAJAJ-AUTO | 8592 | 1983.41 | 17041496 | 2.54935e+08 | 44.1769 |
| dense_target_DRREDDY_2026-07 | 2026-07 | DRREDDY | 8592 | 1983.41 | 17041496 | 2.54935e+08 | 44.1769 |
| dense_target_KOTAKBANK_2026-07 | 2026-07 | KOTAKBANK | 8591 | 1983.41 | 17039512 | 2.54905e+08 | 44.1717 |
| dense_target_ONGC_2026-07 | 2026-07 | ONGC | 8591 | 1983.41 | 17039512 | 2.54905e+08 | 44.1717 |
| dense_target_ICICIBANK_2026-07 | 2026-07 | ICICIBANK | 8590 | 1983.41 | 17037529 | 2.54875e+08 | 44.1666 |
| dense_target_RELIANCE_2026-07 | 2026-07 | RELIANCE | 8590 | 1983.41 | 17037529 | 2.54875e+08 | 44.1666 |
| dense_target_TECHM_2026-07 | 2026-07 | TECHM | 8590 | 1983.41 | 17037529 | 2.54875e+08 | 44.1666 |
| dense_target_HCLTECH_2026-07 | 2026-07 | HCLTECH | 8588 | 1983.41 | 17033562 | 2.54816e+08 | 44.1563 |
| dense_target_TCS_2026-07 | 2026-07 | TCS | 8588 | 1983.41 | 17033562 | 2.54816e+08 | 44.1563 |
| dense_target_HDFCBANK_2026-07 | 2026-07 | HDFCBANK | 8587 | 1983.41 | 17031579 | 2.54786e+08 | 44.1512 |
| dense_target_ITC_2026-07 | 2026-07 | ITC | 8587 | 1983.41 | 17031579 | 2.54786e+08 | 44.1512 |
| dense_target_LT_2026-07 | 2026-07 | LT | 8585 | 1983.41 | 17027612 | 2.54727e+08 | 44.1409 |
| dense_target_BRITANNIA_2026-07 | 2026-07 | BRITANNIA | 8584 | 1983.41 | 17025628 | 2.54697e+08 | 44.1358 |
| dense_target_WIPRO_2026-10 | 2026-10 | WIPRO | 8245 | 1983.41 | 16353251 | 2.44639e+08 | 42.3927 |
| dense_target_WIPRO_2026-01 | 2026-01 | WIPRO | 8239 | 1983.41 | 16341350 | 2.44461e+08 | 42.3619 |
| dense_target_ITC_2026-10 | 2026-10 | ITC | 8238 | 1983.41 | 16339367 | 2.44431e+08 | 42.3568 |
| dense_target_ITBEES_2026-10 | 2026-10 | ITBEES | 8237 | 1983.41 | 16337384 | 2.44401e+08 | 42.3516 |
| dense_target_ULTRACEMCO_2026-01 | 2026-01 | ULTRACEMCO | 8237 | 1983.41 | 16337384 | 2.44401e+08 | 42.3516 |
| dense_target_BPCL_2026-09 | 2026-09 | BPCL | 8236 | 1983.41 | 16335400 | 2.44372e+08 | 42.3465 |
| dense_target_BHARTIARTL_2026-10 | 2026-10 | BHARTIARTL | 8234 | 1983.41 | 16331433 | 2.44312e+08 | 42.3362 |
| dense_target_MARUTI_2026-10 | 2026-10 | MARUTI | 8234 | 1983.41 | 16331433 | 2.44312e+08 | 42.3362 |
| dense_target_NESTLEIND_2026-06 | 2026-06 | NESTLEIND | 8234 | 1983.41 | 16331433 | 2.44312e+08 | 42.3362 |
| dense_target_NIFTYBEES_2026-06 | 2026-06 | NIFTYBEES | 8234 | 1983.41 | 16331433 | 2.44312e+08 | 42.3362 |
| dense_target_BRITANNIA_2026-09 | 2026-09 | BRITANNIA | 8233 | 1983.41 | 16329450 | 2.44283e+08 | 42.331 |
| dense_target_NIFTYBEES_2026-09 | 2026-09 | NIFTYBEES | 8233 | 1983.41 | 16329450 | 2.44283e+08 | 42.331 |
| dense_target_BPCL_2026-03 | 2026-03 | BPCL | 8232 | 1983.41 | 16327466 | 2.44253e+08 | 42.3259 |
| dense_target_CIPLA_2026-03 | 2026-03 | CIPLA | 8232 | 1983.41 | 16327466 | 2.44253e+08 | 42.3259 |
| dense_target_TCS_2026-09 | 2026-09 | TCS | 8232 | 1983.41 | 16327466 | 2.44253e+08 | 42.3259 |
| dense_target_GOLDBEES_2026-10 | 2026-10 | GOLDBEES | 8231 | 1983.41 | 16325483 | 2.44223e+08 | 42.3208 |
| dense_target_ICICIBANK_2026-06 | 2026-06 | ICICIBANK | 8231 | 1983.41 | 16325483 | 2.44223e+08 | 42.3208 |
| dense_target_NIFTYBEES_2026-01 | 2026-01 | NIFTYBEES | 8231 | 1983.41 | 16325483 | 2.44223e+08 | 42.3208 |
| dense_target_ULTRACEMCO_2026-10 | 2026-10 | ULTRACEMCO | 8231 | 1983.41 | 16325483 | 2.44223e+08 | 42.3208 |
| dense_target_ITC_2026-06 | 2026-06 | ITC | 8230 | 1983.41 | 16323500 | 2.44194e+08 | 42.3156 |
| dense_target_BHARTIARTL_2026-01 | 2026-01 | BHARTIARTL | 8229 | 1983.41 | 16321516 | 2.44164e+08 | 42.3105 |
| dense_target_ITBEES_2026-04 | 2026-04 | ITBEES | 8229 | 1983.41 | 16321516 | 2.44164e+08 | 42.3105 |
| dense_target_LT_2026-09 | 2026-09 | LT | 8229 | 1983.41 | 16321516 | 2.44164e+08 | 42.3105 |
| dense_target_MARUTI_2026-01 | 2026-01 | MARUTI | 8229 | 1983.41 | 16321516 | 2.44164e+08 | 42.3105 |
| dense_target_ONGC_2026-10 | 2026-10 | ONGC | 8229 | 1983.41 | 16321516 | 2.44164e+08 | 42.3105 |
| dense_target_SBIN_2026-04 | 2026-04 | SBIN | 8229 | 1983.41 | 16321516 | 2.44164e+08 | 42.3105 |
| dense_target_TECHM_2026-04 | 2026-04 | TECHM | 8229 | 1983.41 | 16321516 | 2.44164e+08 | 42.3105 |
| dense_target_ULTRACEMCO_2026-04 | 2026-04 | ULTRACEMCO | 8229 | 1983.41 | 16321516 | 2.44164e+08 | 42.3105 |
| dense_target_BPCL_2026-01 | 2026-01 | BPCL | 8228 | 1983.41 | 16319533 | 2.44134e+08 | 42.3053 |
| dense_target_BRITANNIA_2026-01 | 2026-01 | BRITANNIA | 8228 | 1983.41 | 16319533 | 2.44134e+08 | 42.3053 |
| dense_target_TCS_2026-01 | 2026-01 | TCS | 8228 | 1983.41 | 16319533 | 2.44134e+08 | 42.3053 |
| dense_target_ULTRACEMCO_2026-06 | 2026-06 | ULTRACEMCO | 8228 | 1983.41 | 16319533 | 2.44134e+08 | 42.3053 |
| dense_target_WIPRO_2026-03 | 2026-03 | WIPRO | 8228 | 1983.41 | 16319533 | 2.44134e+08 | 42.3053 |
| dense_target_BHARTIARTL_2026-04 | 2026-04 | BHARTIARTL | 8227 | 1983.41 | 16317549 | 2.44105e+08 | 42.3002 |
| dense_target_ITC_2026-01 | 2026-01 | ITC | 8227 | 1983.41 | 16317549 | 2.44105e+08 | 42.3002 |
| dense_target_KOTAKBANK_2026-06 | 2026-06 | KOTAKBANK | 8227 | 1983.41 | 16317549 | 2.44105e+08 | 42.3002 |
| dense_target_M&M_2026-01 | 2026-01 | M&M | 8227 | 1983.41 | 16317549 | 2.44105e+08 | 42.3002 |
| dense_target_TCS_2026-03 | 2026-03 | TCS | 8227 | 1983.41 | 16317549 | 2.44105e+08 | 42.3002 |
| dense_target_ULTRACEMCO_2026-09 | 2026-09 | ULTRACEMCO | 8227 | 1983.41 | 16317549 | 2.44105e+08 | 42.3002 |
| dense_target_AXISBANK_2026-09 | 2026-09 | AXISBANK | 8226 | 1983.41 | 16315566 | 2.44075e+08 | 42.2951 |
| dense_target_BHARTIARTL_2026-03 | 2026-03 | BHARTIARTL | 8226 | 1983.41 | 16315566 | 2.44075e+08 | 42.2951 |
| dense_target_HINDUNILVR_2026-06 | 2026-06 | HINDUNILVR | 8226 | 1983.41 | 16315566 | 2.44075e+08 | 42.2951 |
| dense_target_AXISBANK_2026-01 | 2026-01 | AXISBANK | 8225 | 1983.41 | 16313583 | 2.44045e+08 | 42.2899 |
| dense_target_BANKBEES_2026-03 | 2026-03 | BANKBEES | 8225 | 1983.41 | 16313583 | 2.44045e+08 | 42.2899 |
| dense_target_INFY_2026-01 | 2026-01 | INFY | 8225 | 1983.41 | 16313583 | 2.44045e+08 | 42.2899 |
| dense_target_ITBEES_2026-01 | 2026-01 | ITBEES | 8225 | 1983.41 | 16313583 | 2.44045e+08 | 42.2899 |
| dense_target_KOTAKBANK_2026-10 | 2026-10 | KOTAKBANK | 8225 | 1983.41 | 16313583 | 2.44045e+08 | 42.2899 |
| dense_target_MARUTI_2026-03 | 2026-03 | MARUTI | 8225 | 1983.41 | 16313583 | 2.44045e+08 | 42.2899 |

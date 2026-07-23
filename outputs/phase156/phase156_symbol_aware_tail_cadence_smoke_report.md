# Phase156 Symbol-aware Tail Cadence Smoke

Generated UTC: 2026-07-23T09:52:53.289655+00:00

Phase156 smoke-tests a generator profile whose symbol tail-gap multipliers come from the Phase155 full-partition cadence contract.
It materializes a bounded local dense shard only. It does not run strategy replay, fills, P&L, or Azure reads.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase156_profile_id | P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE | Generator calibration profile smoke-tested |
| phase156_smoke_symbols | 32 | Representative high-multiplier symbols in bounded smoke |
| phase156_smoke_partition_files | 32 | Dense smoke partition files materialized |
| phase156_smoke_dense_rows | 16838528 | Dense rows materialized |
| phase156_smoke_bytes | 357833393 | Compressed dense smoke bytes |
| phase156_elapsed_seconds | 50.9107 | Smoke materialization/profile elapsed seconds |
| phase156_p95_improved_symbols | 32 | Smoke symbols whose p95 synthetic gap moved above Phase106 synthetic p95 |
| phase156_p95_contract_band_pass_symbols | 32 | Smoke symbols whose p95 synthetic gap is within [0.5,2.0] of Phase155 target |
| phase156_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase156_next_best_action | expand_phase156_profile_to_full_symbol_audit_then_rewire_phase106_cadence_anchors | Recommended next milestone |

## Phase155 Contract Smoke Comparison

| symbol | target_median_p95_gap_ms | phase106_synthetic_p95_gap_ms | p95_gap_ms | phase106_to_target_p95_ratio | phase156_to_target_p95_ratio | p95_gap_improved_vs_phase106 | p95_contract_band_pass | phase106_synthetic_gap_le_1s_fraction | gap_le_1s_fraction | gap_le_1s_fraction_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | 5500 | 792 | 5500 | 0.144 | 1 | 1 | 1 | 0.991883 | 0.922508 | -0.0693747 |
| AXISBANK | 4380.75 | 792 | 4381 | 0.180791 | 1.00006 | 1 | 1 | 0.992144 | 0.92258 | -0.0695636 |
| BAJAJ-AUTO | 5939.25 | 792 | 5939 | 0.13335 | 0.999958 | 1 | 1 | 0.992223 | 0.922307 | -0.0699159 |
| BANKBEES | 4450 | 792 | 4450 | 0.177978 | 1 | 1 | 1 | 0.992127 | 0.922602 | -0.0695249 |
| BHARTIARTL | 4762.4 | 792 | 4762 | 0.166303 | 0.999916 | 1 | 1 | 0.99226 | 0.922572 | -0.0696878 |
| BPCL | 6081.7 | 792 | 6082 | 0.130227 | 1.00005 | 1 | 1 | 0.992045 | 0.922307 | -0.0697385 |
| BRITANNIA | 7000.8 | 792 | 7001 | 0.11313 | 1.00003 | 1 | 1 | 0.991937 | 0.922288 | -0.0696493 |
| CIPLA | 5953.9 | 792 | 5954 | 0.133022 | 1.00002 | 1 | 1 | 0.992041 | 0.922302 | -0.0697399 |
| DRREDDY | 5750 | 792 | 5750 | 0.137739 | 1 | 1 | 1 | 0.992113 | 0.92233 | -0.0697831 |
| GOLDBEES | 5250 | 792 | 5250 | 0.150857 | 1 | 1 | 1 | 0.99214 | 0.922565 | -0.0695749 |
| HCLTECH | 5324.85 | 792 | 5325 | 0.148737 | 1.00003 | 1 | 1 | 0.992078 | 0.922573 | -0.0695046 |
| HDFCBANK | 1250 | 792 | 1250 | 0.6336 | 1 | 1 | 1 | 0.991948 | 0.937459 | -0.0544889 |
| HINDUNILVR | 5859.45 | 792 | 5859 | 0.135166 | 0.999923 | 1 | 1 | 0.992083 | 0.922323 | -0.0697605 |
| ICICIBANK | 3403 | 792 | 3403 | 0.232736 | 1 | 1 | 1 | 0.992151 | 0.922379 | -0.0697716 |
| INFY | 3922.15 | 792 | 3922 | 0.20193 | 0.999962 | 1 | 1 | 0.992097 | 0.922567 | -0.06953 |
| ITBEES | 6911.05 | 792 | 6911 | 0.114599 | 0.999993 | 1 | 1 | 0.992057 | 0.922276 | -0.069781 |
| ITC | 4815.4 | 792 | 4815 | 0.164472 | 0.999917 | 1 | 1 | 0.992047 | 0.922599 | -0.0694474 |
| JUNIORBEES | 4511 | 792 | 4511 | 0.175571 | 1 | 1 | 1 | 0.992121 | 0.922586 | -0.0695356 |
| KOTAKBANK | 4051.3 | 792 | 4051 | 0.195493 | 0.999926 | 1 | 1 | 0.992164 | 0.922598 | -0.0695657 |
| LT | 3367 | 792 | 3367 | 0.235224 | 1 | 1 | 1 | 0.992006 | 0.922391 | -0.0696148 |
| M&M | 4285.45 | 792 | 4285 | 0.184811 | 0.999895 | 1 | 1 | 0.992027 | 0.922578 | -0.069449 |
| MARUTI | 4212 | 792 | 4212 | 0.188034 | 1 | 1 | 1 | 0.992272 | 0.922593 | -0.0696786 |
| NESTLEIND | 6232.4 | 792 | 6232 | 0.127078 | 0.999936 | 1 | 1 | 0.992183 | 0.9223 | -0.069883 |
| NIFTYBEES | 4467.05 | 792 | 4467 | 0.177298 | 0.999989 | 1 | 1 | 0.992136 | 0.922576 | -0.0695601 |
| ONGC | 5002 | 792 | 5002 | 0.158337 | 1 | 1 | 1 | 0.992224 | 0.922579 | -0.0696446 |
| RELIANCE | 2999 | 792 | 2999 | 0.264088 | 1 | 1 | 1 | 0.992321 | 0.922499 | -0.069821 |
| SBIN | 4257.7 | 792 | 4258 | 0.186016 | 1.00007 | 1 | 1 | 0.992078 | 0.922585 | -0.0694925 |
| SUNPHARMA | 5484 | 792 | 5484 | 0.14442 | 1 | 1 | 1 | 0.992104 | 0.922535 | -0.0695688 |
| TCS | 4250.7 | 792 | 4251 | 0.186322 | 1.00007 | 1 | 1 | 0.992238 | 0.922609 | -0.0696297 |
| TECHM | 5806.1 | 792 | 5806 | 0.136408 | 0.999983 | 1 | 1 | 0.992011 | 0.922311 | -0.0697 |
| ULTRACEMCO | 6772.6 | 792 | 6773 | 0.116942 | 1.00006 | 1 | 1 | 0.992217 | 0.922289 | -0.0699277 |
| WIPRO | 5142.2 | 792 | 5142 | 0.15402 | 0.999961 | 1 | 1 | 0.992048 | 0.922573 | -0.0694743 |

## Dense Smoke Inventory

| trade_month | symbol | source_rows | dense_rows | multiplier | file_path | bytes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | ADANIPORTS | 8221 | 526144 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=ADANIPORTS\part-00000.parquet | 11082962 |
| 2026-01 | AXISBANK | 8225 | 526400 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=AXISBANK\part-00000.parquet | 11271542 |
| 2026-01 | BAJAJ-AUTO | 8221 | 526144 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=BAJAJ-AUTO\part-00000.parquet | 11090967 |
| 2026-01 | BANKBEES | 8216 | 525824 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=BANKBEES\part-00000.parquet | 11127130 |
| 2026-01 | BHARTIARTL | 8229 | 526656 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=BHARTIARTL\part-00000.parquet | 11245097 |
| 2026-01 | BPCL | 8228 | 526592 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=BPCL\part-00000.parquet | 11019958 |
| 2026-01 | BRITANNIA | 8228 | 526592 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=BRITANNIA\part-00000.parquet | 11180047 |
| 2026-01 | CIPLA | 8216 | 525824 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=CIPLA\part-00000.parquet | 11086460 |
| 2026-01 | DRREDDY | 8218 | 525952 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=DRREDDY\part-00000.parquet | 11165881 |
| 2026-01 | GOLDBEES | 8222 | 526208 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=GOLDBEES\part-00000.parquet | 11280286 |
| 2026-01 | HCLTECH | 8218 | 525952 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=HCLTECH\part-00000.parquet | 11181813 |
| 2026-01 | HDFCBANK | 8220 | 526080 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=HDFCBANK\part-00000.parquet | 11420745 |
| 2026-01 | HINDUNILVR | 8207 | 525248 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=HINDUNILVR\part-00000.parquet | 11119902 |
| 2026-01 | ICICIBANK | 8219 | 526016 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=ICICIBANK\part-00000.parquet | 11339541 |
| 2026-01 | INFY | 8225 | 526400 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=INFY\part-00000.parquet | 11340196 |
| 2026-01 | ITBEES | 8225 | 526400 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=ITBEES\part-00000.parquet | 11130161 |
| 2026-01 | ITC | 8227 | 526528 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=ITC\part-00000.parquet | 11192716 |
| 2026-01 | JUNIORBEES | 8209 | 525376 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=JUNIORBEES\part-00000.parquet | 11269091 |
| 2026-01 | KOTAKBANK | 8218 | 525952 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=KOTAKBANK\part-00000.parquet | 11201367 |
| 2026-01 | LT | 8218 | 525952 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=LT\part-00000.parquet | 11308563 |
| 2026-01 | M&M | 8227 | 526528 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=M&M\part-00000.parquet | 11250826 |
| 2026-01 | MARUTI | 8229 | 526656 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=MARUTI\part-00000.parquet | 10941224 |
| 2026-01 | NESTLEIND | 8216 | 525824 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=NESTLEIND\part-00000.parquet | 11158797 |
| 2026-01 | NIFTYBEES | 8231 | 526784 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=NIFTYBEES\part-00000.parquet | 11293616 |
| 2026-01 | ONGC | 8219 | 526016 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=ONGC\part-00000.parquet | 11097645 |
| 2026-01 | RELIANCE | 8214 | 525696 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=RELIANCE\part-00000.parquet | 11348324 |
| 2026-01 | SBIN | 8215 | 525760 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=SBIN\part-00000.parquet | 11071614 |
| 2026-01 | SUNPHARMA | 8220 | 526080 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=SUNPHARMA\part-00000.parquet | 10816581 |
| 2026-01 | TCS | 8228 | 526592 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=TCS\part-00000.parquet | 11356346 |
| 2026-01 | TECHM | 8217 | 525888 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=TECHM\part-00000.parquet | 11098862 |
| 2026-01 | ULTRACEMCO | 8237 | 527168 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=ULTRACEMCO\part-00000.parquet | 11118218 |
| 2026-01 | WIPRO | 8239 | 527296 | 64 | raw_synthetic_l2_phase156_symbol_tail_cadence_smoke\profile=P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE\trade_month=2026-01\symbol=WIPRO\part-00000.parquet | 11226915 |

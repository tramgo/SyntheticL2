# Phase157 Full-partition Cadence Rewire Audit

Generated UTC: 2026-07-23T09:56:05.222136+00:00

Phase157 verifies that cadence targets for future Phase106-style audits can be sourced from Phase154 full local partitions.
It audits cadence only. It does not claim spread, depth, imbalance, volatility, execution, fill, P&L, or strategy readiness.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase157_phase154_anchor_available | 1 | Phase154 full-partition anchor exists |
| phase157_phase155_contract_available | 1 | Phase155 full-partition cadence contract exists |
| phase157_phase156_smoke_available | 1 | Phase156 regenerated synthetic cadence profile exists |
| phase157_phase106_legacy_profile_available | 1 | Legacy Phase106 synthetic profile exists for comparison |
| phase157_symbols_audited | 32 | Symbols audited for cadence rewire |
| phase157_p95_contract_pass_symbols | 32 | Symbols whose Phase156 p95 gap is inside the full-partition target band |
| phase157_p95_exact_target_pass_symbols | 32 | Symbols whose Phase156 p95 gap is within 1 ms of the Phase154/155 target |
| phase157_cadence_rewire_pass_symbols | 32 | Symbols passing all cadence-rewire checks |
| phase157_legacy_sampled_anchor_stale_symbols | 32 | Symbols for which legacy sampled cadence anchors must not be used |
| phase157_inherited_phase154_sample_bias_flag_rows | 42 | Inherited Phase154 sample-bias rows |
| phase157_inherited_phase156_dense_rows | 16838528 | Inherited Phase156 dense smoke rows |
| phase157_full_partition_cadence_rewire_ready | 1 | 1 means cadence-slice anchor rewire is ready for Phase106-style audits |
| phase157_strategy_replay_allowed | 0 | Strategy replay remains closed |
| phase157_next_best_action | run_phase106_style_full_realism_audit_with_phase157_cadence_contract_and_non_cadence_gates | Recommended next milestone |

## Phase106 Cadence Metric Source Contract

| metric | anchor_source | synthetic_source | ratio_gate | rewire_status |
| --- | --- | --- | --- | --- |
| median_gap_ms | phase154_symbol_cadence_anchor.target_median_gap_ms | regenerated_synthetic_anchor_profile.median_gap_ms | [0.5,2.0] | ready_for_phase106_style_audit_replacement |
| p90_gap_ms | phase154_partition_cadence_profiles.target_median_p90_gap_ms | regenerated_synthetic_anchor_profile.p90_gap_ms | [0.5,2.0] | ready_for_phase106_style_audit_replacement_after_full_profile |
| p95_gap_ms | phase154_symbol_cadence_anchor.target_median_p95_gap_ms | regenerated_synthetic_anchor_profile.p95_gap_ms | [0.5,2.0] | ready_for_phase106_style_audit_replacement |
| gap_le_1s_fraction | phase154_symbol_cadence_anchor.target_median_gap_le_1s_fraction | regenerated_synthetic_anchor_profile.gap_le_1s_fraction | absolute_delta<=0.20 | diagnostic_only_until_dense_frequency_model_is_distributional |
| spread_depth_imbalance_volatility | existing_realism_audit_non_cadence_sources | existing_synthetic_anchor_profile | unchanged_existing_gates | not_modified_by_phase157 |

## Symbol Cadence Rewire Matrix

| exchange | symbol | phase154_full_partition_rows | phase154_target_median_gap_ms | phase154_target_p95_gap_ms | phase154_target_gap_le_1s_fraction | target_median_gap_ms | target_median_p95_gap_ms | phase106_synthetic_p95_gap_ms | phase106_synthetic_gap_le_1s_fraction | synthetic_to_full_p95_ratio | phase106_cadence_contract_pass | phase156_smoke_rows | phase156_synthetic_median_gap_ms | phase156_synthetic_p90_gap_ms | phase156_synthetic_p95_gap_ms | phase156_synthetic_gap_le_1s_fraction | phase106_profile_p95_gap_ms | phase106_profile_gap_le_1s_fraction | target_consistent_with_phase154 | phase156_to_full_p95_ratio | phase156_p95_contract_pass | phase156_p95_exact_target_pass | phase156_gap_le_1s_delta_vs_phase154 | legacy_phase106_sampled_anchor_stale | future_cadence_anchor_source | cadence_rewire_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NSE | ADANIPORTS | 27481 | 1000 | 5500 | 0.546345 | 1000 | 5500 | 792 | 0.991883 | 0.144 | 0 | 526144 | 500 | 500 | 5500 | 0.922508 | 792 | 0.991883 | 1 | 1 | 1 | 1 | 0.376163 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | AXISBANK | 43257 | 501 | 4380.75 | 0.773267 | 501 | 4380.75 | 792 | 0.992144 | 0.180791 | 0 | 526400 | 500 | 500 | 4381 | 0.92258 | 792 | 0.992144 | 1 | 1.00006 | 1 | 1 | 0.149313 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | BAJAJ-AUTO | 36720 | 1000 | 5939.25 | 0.536706 | 1000 | 5939.25 | 792 | 0.992223 | 0.13335 | 0 | 526144 | 500 | 500 | 5939 | 0.922307 | 792 | 0.992223 | 1 | 0.999958 | 1 | 1 | 0.385601 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | BANKBEES | 41253 | 999 | 4450 | 0.769716 | 999 | 4450 | 792 | 0.992127 | 0.177978 | 0 | 525824 | 500 | 500 | 4450 | 0.922602 | 792 | 0.992127 | 1 | 1 | 1 | 1 | 0.152886 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | BHARTIARTL | 46148 | 749 | 4762.4 | 0.708779 | 749 | 4762.4 | 792 | 0.99226 | 0.166303 | 0 | 526656 | 500 | 500 | 4762 | 0.922572 | 792 | 0.99226 | 1 | 0.999916 | 1 | 1 | 0.213794 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | BPCL | 20739 | 1635.5 | 6081.7 | 0.392118 | 1635.5 | 6081.7 | 792 | 0.992045 | 0.130227 | 0 | 526592 | 500 | 500 | 6082 | 0.922307 | 792 | 0.992045 | 1 | 1.00005 | 1 | 1 | 0.530188 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | BRITANNIA | 16325 | 2000 | 7000.8 | 0.345689 | 2000 | 7000.8 | 792 | 0.991937 | 0.11313 | 0 | 526592 | 500 | 500 | 7001 | 0.922288 | 792 | 0.991937 | 1 | 1.00003 | 1 | 1 | 0.576598 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | CIPLA | 22213 | 1378 | 5953.9 | 0.438237 | 1378 | 5953.9 | 792 | 0.992041 | 0.133022 | 0 | 525824 | 500 | 500 | 5954 | 0.922302 | 792 | 0.992041 | 1 | 1.00002 | 1 | 1 | 0.484065 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | DRREDDY | 34854 | 1250 | 5750 | 0.461243 | 1250 | 5750 | 792 | 0.992113 | 0.137739 | 0 | 525952 | 500 | 500 | 5750 | 0.92233 | 792 | 0.992113 | 1 | 1 | 1 | 1 | 0.461086 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | GOLDBEES | 29870 | 750 | 5250 | 0.667216 | 750 | 5250 | 792 | 0.99214 | 0.150857 | 0 | 526208 | 500 | 500 | 5250 | 0.922565 | 792 | 0.99214 | 1 | 1 | 1 | 1 | 0.255349 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | HCLTECH | 40610 | 1000 | 5324.85 | 0.520642 | 1000 | 5324.85 | 792 | 0.992078 | 0.148737 | 0 | 525952 | 500 | 500 | 5325 | 0.922573 | 792 | 0.992078 | 1 | 1.00003 | 1 | 1 | 0.401932 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | HDFCBANK | 70803 | 500 | 1250 | 0.921965 | 500 | 1250 | 792 | 0.991948 | 0.6336 | 1 | 526080 | 500 | 500 | 1250 | 0.937459 | 792 | 0.991948 | 1 | 1 | 1 | 1 | 0.0154949 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | HINDUNILVR | 29461 | 1000 | 5859.45 | 0.5779 | 1000 | 5859.45 | 792 | 0.992083 | 0.135166 | 0 | 525248 | 500 | 500 | 5859 | 0.922323 | 792 | 0.992083 | 1 | 0.999923 | 1 | 1 | 0.344423 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | ICICIBANK | 58334 | 500 | 3403 | 0.896955 | 500 | 3403 | 792 | 0.992151 | 0.232736 | 0 | 526016 | 500 | 500 | 3403 | 0.922379 | 792 | 0.992151 | 1 | 1 | 1 | 1 | 0.0254241 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | INFY | 58214 | 500 | 3922.15 | 0.829054 | 500 | 3922.15 | 792 | 0.992097 | 0.20193 | 0 | 526400 | 500 | 500 | 3922 | 0.922567 | 792 | 0.992097 | 1 | 0.999962 | 1 | 1 | 0.0935134 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | ITBEES | 18963 | 2001 | 6911.05 | 0.306614 | 2001 | 6911.05 | 792 | 0.992057 | 0.114599 | 0 | 526400 | 500 | 500 | 6911 | 0.922276 | 792 | 0.992057 | 1 | 0.999993 | 1 | 1 | 0.615663 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | ITC | 32733 | 749 | 4815.4 | 0.727574 | 749 | 4815.4 | 792 | 0.992047 | 0.164472 | 0 | 526528 | 500 | 500 | 4815 | 0.922599 | 792 | 0.992047 | 1 | 0.999917 | 1 | 1 | 0.195025 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | JUNIORBEES | 38437 | 999 | 4511 | 0.760716 | 999 | 4511 | 792 | 0.992121 | 0.175571 | 0 | 525376 | 500 | 500 | 4511 | 0.922586 | 792 | 0.992121 | 1 | 1 | 1 | 1 | 0.16187 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | KOTAKBANK | 42075 | 500 | 4051.3 | 0.833298 | 500 | 4051.3 | 792 | 0.992164 | 0.195493 | 0 | 525952 | 500 | 500 | 4051 | 0.922598 | 792 | 0.992164 | 1 | 0.999926 | 1 | 1 | 0.0893005 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | LT | 50307 | 500 | 3367 | 0.885798 | 500 | 3367 | 792 | 0.992006 | 0.235224 | 0 | 525952 | 500 | 500 | 3367 | 0.922391 | 792 | 0.992006 | 1 | 1 | 1 | 1 | 0.0365932 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | M&M | 51233 | 501 | 4285.45 | 0.825434 | 501 | 4285.45 | 792 | 0.992027 | 0.184811 | 0 | 526528 | 500 | 500 | 4285 | 0.922578 | 792 | 0.992027 | 1 | 0.999895 | 1 | 1 | 0.0971444 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | MARUTI | 48890 | 683 | 4212 | 0.774621 | 683 | 4212 | 792 | 0.992272 | 0.188034 | 0 | 526656 | 500 | 500 | 4212 | 0.922593 | 792 | 0.992272 | 1 | 1 | 1 | 1 | 0.147973 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | NESTLEIND | 22657 | 1251 | 6232.4 | 0.437565 | 1251 | 6232.4 | 792 | 0.992183 | 0.127078 | 0 | 525824 | 500 | 500 | 6232 | 0.9223 | 792 | 0.992183 | 1 | 0.999936 | 1 | 1 | 0.484735 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | NIFTYBEES | 44715 | 749 | 4467.05 | 0.790702 | 749 | 4467.05 | 792 | 0.992136 | 0.177298 | 0 | 526784 | 500 | 500 | 4467 | 0.922576 | 792 | 0.992136 | 1 | 0.999989 | 1 | 1 | 0.131874 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | ONGC | 32786 | 750 | 5002 | 0.663951 | 750 | 5002 | 792 | 0.992224 | 0.158337 | 0 | 526016 | 500 | 500 | 5002 | 0.922579 | 792 | 0.992224 | 1 | 1 | 1 | 1 | 0.258628 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | RELIANCE | 58141 | 500 | 2999 | 0.890378 | 500 | 2999 | 792 | 0.992321 | 0.264088 | 0 | 525696 | 500 | 500 | 2999 | 0.922499 | 792 | 0.992321 | 1 | 1 | 1 | 1 | 0.0321213 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | SBIN | 50664 | 500 | 4257.7 | 0.825014 | 500 | 4257.7 | 792 | 0.992078 | 0.186016 | 0 | 525760 | 500 | 500 | 4258 | 0.922585 | 792 | 0.992078 | 1 | 1.00007 | 1 | 1 | 0.0975705 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | SUNPHARMA | 32921 | 982 | 5484 | 0.600041 | 982 | 5484 | 792 | 0.992104 | 0.14442 | 0 | 526080 | 500 | 500 | 5484 | 0.922535 | 792 | 0.992104 | 1 | 1 | 1 | 1 | 0.322494 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | TCS | 57870 | 500 | 4250.7 | 0.819414 | 500 | 4250.7 | 792 | 0.992238 | 0.186322 | 0 | 526592 | 500 | 500 | 4251 | 0.922609 | 792 | 0.992238 | 1 | 1.00007 | 1 | 1 | 0.103194 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | TECHM | 29591 | 1238.5 | 5806.1 | 0.471861 | 1238.5 | 5806.1 | 792 | 0.992011 | 0.136408 | 0 | 525888 | 500 | 500 | 5806 | 0.922311 | 792 | 0.992011 | 1 | 0.999983 | 1 | 1 | 0.45045 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | ULTRACEMCO | 17353 | 2000 | 6772.6 | 0.31124 | 2000 | 6772.6 | 792 | 0.992217 | 0.116942 | 0 | 527168 | 500 | 500 | 6773 | 0.922289 | 792 | 0.992217 | 1 | 1.00006 | 1 | 1 | 0.611049 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |
| NSE | WIPRO | 32657 | 751 | 5142.2 | 0.601747 | 751 | 5142.2 | 792 | 0.992048 | 0.15402 | 0 | 527296 | 500 | 500 | 5142 | 0.922573 | 792 | 0.992048 | 1 | 0.999961 | 1 | 1 | 0.320827 | 1 | phase154_full_partition_symbol_cadence_anchor | 1 |

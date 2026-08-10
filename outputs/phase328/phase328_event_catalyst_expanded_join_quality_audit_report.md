# Phase328 Event-Catalyst Expanded Join Quality Audit

Phase328 audits the Phase327 joined top-five market-by-price depth parquet. It does not run strategy search, replay, promotion, paper/live acceptance, or profitability claims.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase328_expanded_join_quality_audit_complete | 1 | Phase328 expanded join quality audit completed |
| phase328_joined_rows | 141708530 | Joined rows audited |
| phase328_event_rows | 50 | Distinct events audited |
| phase328_symbol_rows | 32 | Distinct symbols audited |
| phase328_min_event_symbol_coverage | 32 | Minimum symbols per event |
| phase328_min_symbol_event_coverage | 50 | Minimum events per symbol |
| phase328_relative_second_min | -900 | Minimum relative second |
| phase328_relative_second_max | 1800 | Maximum relative second |
| phase328_crossed_or_locked_l1_rows | 0 | Crossed or locked top-of-book rows |
| phase328_bid_depth_sort_error_rows | 0 | Bid depth sort error rows |
| phase328_ask_depth_sort_error_rows | 0 | Ask depth sort error rows |
| phase328_depth_beyond_l1_material_rows | 141708530 | Rows with depth levels 2-5 material |
| phase328_strategy_search_allowed_now | 0 | No strategy search in Phase328 |
| phase328_strategy_replay_allowed | 0 | No replay |
| phase328_strategy_promotion_allowed | 0 | No promotion |
| phase328_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase328_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase328_hard_gate_pass_rows | 12 | Passed hard gates |
| phase328_hard_gate_rows | 12 | Hard gates |
| phase328_next_best_action | run_phase329_event_catalyst_expanded_feature_materialization_precommit_no_replay | Recommended next action |

## Quality summary

| joined_rows | event_rows | symbol_rows | min_relative_second | max_relative_second | crossed_or_locked_l1_rows | nonpositive_l1_quantity_rows | nonpositive_depth_beyond_l1_quantity_rows | bid_depth_sort_error_rows | ask_depth_sort_error_rows | depth_beyond_l1_material_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 141708530 | 50 | 32 | -900 | 1800 | 0 | 0 | 0 | 0 | 0 | 1.41709e+08 |

## Event coverage

| event_id | joined_rows | symbols | min_relative_second | max_relative_second |
| --- | --- | --- | --- | --- |
| P325_SYNTH_EVENT_001_20260714 | 2835216 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_002_20260715 | 2800243 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_003_20260716 | 2809966 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_004_20260717 | 2881479 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_005_20260720 | 2855655 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_006_20260721 | 2835659 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_007_20260722 | 2806388 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_008_20260723 | 2851646 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_009_20260724 | 2848047 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_010_20260727 | 2867004 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_011_20260728 | 2854161 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_012_20260729 | 2852436 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_013_20260730 | 2806814 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_014_20260731 | 2837732 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_015_20260803 | 2829576 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_016_20260804 | 2831162 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_017_20260805 | 2858281 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_018_20260806 | 2857004 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_019_20260807 | 2831253 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_020_20260810 | 2831057 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_021_20260811 | 2858739 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_022_20260812 | 2808109 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_023_20260813 | 2819907 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_024_20260814 | 2834548 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_025_20260817 | 2836791 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_026_20260818 | 2845808 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_027_20260819 | 2830131 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_028_20260820 | 2847316 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_029_20260821 | 2844062 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_030_20260824 | 2862372 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_031_20260825 | 2865131 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_032_20260826 | 2804337 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_033_20260827 | 2807267 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_034_20260828 | 2831802 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_035_20260831 | 2831944 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_036_20260901 | 2824486 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_037_20260902 | 2872464 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_038_20260903 | 2804000 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_039_20260904 | 2796932 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_040_20260907 | 2853884 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_041_20260908 | 2845218 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_042_20260909 | 2774228 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_043_20260910 | 2849753 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_044_20260911 | 2811036 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_045_20260914 | 2822509 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_046_20260915 | 2837436 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_047_20260916 | 2829237 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_048_20260917 | 2829545 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_049_20260918 | 2806772 | 32 | -900 | 1800 |
| P325_SYNTH_EVENT_050_20260921 | 2841987 | 32 | -900 | 1800 |

## Symbol coverage

| symbol | joined_rows | events | min_relative_second | max_relative_second |
| --- | --- | --- | --- | --- |
| ADANIPORTS | 4402396 | 50 | -900 | 1800 |
| AXISBANK | 4417911 | 50 | -900 | 1800 |
| BAJAJ-AUTO | 4418527 | 50 | -900 | 1800 |
| BANKBEES | 4409864 | 50 | -900 | 1800 |
| BHARTIARTL | 4435178 | 50 | -900 | 1800 |
| BPCL | 4462547 | 50 | -900 | 1800 |
| BRITANNIA | 4413622 | 50 | -900 | 1800 |
| CIPLA | 4438813 | 50 | -900 | 1800 |
| DRREDDY | 4404587 | 50 | -900 | 1800 |
| GOLDBEES | 4441011 | 50 | -900 | 1800 |
| HCLTECH | 4440820 | 50 | -900 | 1800 |
| HDFCBANK | 4558855 | 50 | -900 | 1800 |
| HINDUNILVR | 4445205 | 50 | -900 | 1800 |
| ICICIBANK | 4381061 | 50 | -900 | 1800 |
| INFY | 4433459 | 50 | -900 | 1800 |
| ITBEES | 4396293 | 50 | -900 | 1800 |
| ITC | 4403189 | 50 | -900 | 1800 |
| JUNIORBEES | 4459285 | 50 | -900 | 1800 |
| KOTAKBANK | 4410249 | 50 | -900 | 1800 |
| LT | 4447765 | 50 | -900 | 1800 |
| M&M | 4443087 | 50 | -900 | 1800 |
| MARUTI | 4420355 | 50 | -900 | 1800 |
| NESTLEIND | 4406913 | 50 | -900 | 1800 |
| NIFTYBEES | 4437891 | 50 | -900 | 1800 |
| ONGC | 4440726 | 50 | -900 | 1800 |
| RELIANCE | 4417384 | 50 | -900 | 1800 |
| SBIN | 4386501 | 50 | -900 | 1800 |
| SUNPHARMA | 4407196 | 50 | -900 | 1800 |
| TCS | 4468746 | 50 | -900 | 1800 |
| TECHM | 4415088 | 50 | -900 | 1800 |
| ULTRACEMCO | 4429222 | 50 | -900 | 1800 |
| WIPRO | 4414784 | 50 | -900 | 1800 |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P328_PHASE327_COMPLETE | True | 1 | 1 | hard |
| P328_JOINED_PARQUET_EXISTS | True | 1 | 1 | hard |
| P328_FULL_DEPTH_SCHEMA_PRESENT | True | 1 | 1 | hard |
| P328_JOINED_ROWS_MATCH_PHASE327 | True | 141708530 | 141708530 | hard |
| P328_EVENT_COVERAGE_COMPLETE | True | events=50;min_symbols=32 | >=50_events_x_32_symbols | hard |
| P328_SYMBOL_COVERAGE_COMPLETE | True | symbols=32;min_events=50 | >=32_symbols_x_50_events | hard |
| P328_RELATIVE_WINDOW_BOUNDED | True | -900.0..1800.0 | -900..1800 | hard |
| P328_NO_CROSSED_OR_LOCKED_L1 | True | 0 | 0 | hard |
| P328_DEPTH_SORT_OK | True | bid=0.0;ask=0.0 | 0 | hard |
| P328_DEPTH_BEYOND_L1_MATERIAL | True | 141708530 | 141708530 | hard |
| P328_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P328_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

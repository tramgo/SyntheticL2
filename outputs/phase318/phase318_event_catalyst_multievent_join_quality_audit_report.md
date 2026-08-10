# Phase318 Event-Catalyst Multi-Event Join Quality Audit

Phase318 audits the Phase317 joined top-five market-by-price depth parquet. It does not run strategy search, replay, promotion, paper/live acceptance, or profitability claims.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase318_multievent_join_quality_audit_complete | 1 | Phase318 multi-event join quality audit completed |
| phase318_joined_rows | 28350310 | Joined rows audited |
| phase318_event_rows | 10 | Distinct events audited |
| phase318_symbol_rows | 32 | Distinct symbols audited |
| phase318_min_event_symbol_coverage | 32 | Minimum symbols per event |
| phase318_min_symbol_event_coverage | 10 | Minimum events per symbol |
| phase318_relative_second_min | -900 | Minimum relative second |
| phase318_relative_second_max | 1800 | Maximum relative second |
| phase318_crossed_or_locked_l1_rows | 0 | Crossed or locked top-of-book rows |
| phase318_bid_depth_sort_error_rows | 0 | Bid depth sort error rows |
| phase318_ask_depth_sort_error_rows | 0 | Ask depth sort error rows |
| phase318_depth_beyond_l1_material_rows | 28350310 | Rows with depth levels 2-5 material |
| phase318_strategy_search_allowed_now | 0 | No strategy search in Phase318 |
| phase318_strategy_replay_allowed | 0 | No replay |
| phase318_strategy_promotion_allowed | 0 | No promotion |
| phase318_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase318_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase318_hard_gate_pass_rows | 12 | Passed hard gates |
| phase318_hard_gate_rows | 12 | Hard gates |
| phase318_next_best_action | run_phase319_event_catalyst_multievent_feature_materialization_precommit_no_replay | Recommended next action |

## Quality summary

| joined_rows | event_rows | symbol_rows | min_relative_second | max_relative_second | crossed_or_locked_l1_rows | nonpositive_l1_quantity_rows | nonpositive_depth_beyond_l1_quantity_rows | bid_depth_sort_error_rows | ask_depth_sort_error_rows | depth_beyond_l1_material_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 28350310 | 10 | 32 | -900 | 1800 | 0 | 0 | 0 | 0 | 0 | 2.83503e+07 |

## Event coverage

| event_id | joined_rows | symbols | min_relative_second | max_relative_second |
| --- | --- | --- | --- | --- |
| P315_SYNTH_EVENT_001_20260714 | 2835216 | 32 | -900 | 1800 |
| P315_SYNTH_EVENT_002_20260716 | 2809966 | 32 | -900 | 1800 |
| P315_SYNTH_EVENT_003_20260727 | 2867004 | 32 | -900 | 1800 |
| P315_SYNTH_EVENT_004_20260729 | 2852436 | 32 | -900 | 1800 |
| P315_SYNTH_EVENT_005_20260730 | 2806814 | 32 | -900 | 1800 |
| P315_SYNTH_EVENT_006_20260804 | 2831162 | 32 | -900 | 1800 |
| P315_SYNTH_EVENT_007_20260806 | 2857004 | 32 | -900 | 1800 |
| P315_SYNTH_EVENT_008_20260812 | 2808109 | 32 | -900 | 1800 |
| P315_SYNTH_EVENT_009_20260817 | 2836791 | 32 | -900 | 1800 |
| P315_SYNTH_EVENT_010_20260818 | 2845808 | 32 | -900 | 1800 |

## Symbol coverage

| symbol | joined_rows | events | min_relative_second | max_relative_second |
| --- | --- | --- | --- | --- |
| ADANIPORTS | 874446 | 10 | -900 | 1800 |
| AXISBANK | 876672 | 10 | -900 | 1800 |
| BAJAJ-AUTO | 887635 | 10 | -900 | 1800 |
| BANKBEES | 888320 | 10 | -900 | 1800 |
| BHARTIARTL | 893489 | 10 | -900 | 1800 |
| BPCL | 889549 | 10 | -900 | 1800 |
| BRITANNIA | 886006 | 10 | -900 | 1800 |
| CIPLA | 895556 | 10 | -900 | 1800 |
| DRREDDY | 875640 | 10 | -900 | 1800 |
| GOLDBEES | 896423 | 10 | -900 | 1800 |
| HCLTECH | 878588 | 10 | -900 | 1800 |
| HDFCBANK | 909059 | 10 | -900 | 1800 |
| HINDUNILVR | 896332 | 10 | -900 | 1800 |
| ICICIBANK | 870173 | 10 | -900 | 1800 |
| INFY | 876408 | 10 | -900 | 1800 |
| ITBEES | 874952 | 10 | -900 | 1800 |
| ITC | 882233 | 10 | -900 | 1800 |
| JUNIORBEES | 887742 | 10 | -900 | 1800 |
| KOTAKBANK | 894526 | 10 | -900 | 1800 |
| LT | 885786 | 10 | -900 | 1800 |
| M&M | 884364 | 10 | -900 | 1800 |
| MARUTI | 886302 | 10 | -900 | 1800 |
| NESTLEIND | 882795 | 10 | -900 | 1800 |
| NIFTYBEES | 883137 | 10 | -900 | 1800 |
| ONGC | 875765 | 10 | -900 | 1800 |
| RELIANCE | 888084 | 10 | -900 | 1800 |
| SBIN | 874698 | 10 | -900 | 1800 |
| SUNPHARMA | 890457 | 10 | -900 | 1800 |
| TCS | 896696 | 10 | -900 | 1800 |
| TECHM | 879231 | 10 | -900 | 1800 |
| ULTRACEMCO | 896642 | 10 | -900 | 1800 |
| WIPRO | 892604 | 10 | -900 | 1800 |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P318_PHASE317_COMPLETE | True | 1 | 1 | hard |
| P318_JOINED_PARQUET_EXISTS | True | 1 | 1 | hard |
| P318_FULL_DEPTH_SCHEMA_PRESENT | True | 1 | 1 | hard |
| P318_JOINED_ROWS_MATCH_PHASE317 | True | 28350310 | 28350310 | hard |
| P318_EVENT_COVERAGE_COMPLETE | True | events=10;min_symbols=32 | >=10_events_x_32_symbols | hard |
| P318_SYMBOL_COVERAGE_COMPLETE | True | symbols=32;min_events=10 | >=32_symbols_x_10_events | hard |
| P318_RELATIVE_WINDOW_BOUNDED | True | -900.0..1800.0 | -900..1800 | hard |
| P318_NO_CROSSED_OR_LOCKED_L1 | True | 0 | 0 | hard |
| P318_DEPTH_SORT_OK | True | bid=0.0;ask=0.0 | 0 | hard |
| P318_DEPTH_BEYOND_L1_MATERIAL | True | 28350310 | 28350310 | hard |
| P318_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P318_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

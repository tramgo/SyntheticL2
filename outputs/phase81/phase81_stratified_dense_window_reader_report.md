# Phase81 Stratified Dense-Window Reader

Generated UTC: 2026-07-19T20:24:59.894600+00:00

Phase81 implements the Phase80 recalibration contract by selecting source-day/regime/feed-profile balanced dense windows.
It emits explicit predicates that future dense audits and replays can use instead of prefix-only `local_sequence_id` windows.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase81_months_planned | 12 | Months with stratified dense-window plans |
| phase81_plan_pass_fraction | 1 | Fraction of month plans passing compact diversity capture gates |
| phase81_dense_control_pass_fraction | 1 | Fraction of month plans verified on dense control symbol |
| phase81_min_selected_days | 7 | Minimum selected source days per month |
| phase81_max_selected_days | 14 | Maximum selected source days per month |
| phase81_stratified_dense_window_reader_pass | 1 | 1 means stratified reader contract is ready for replay use |
| phase81_recommend_next_action | rerun_hdfcbank_disjoint_retest_with_stratified_windows | Recommended next milestone |

## Stratified Window Monthly Plan

| trade_month | compact_days | selected_days | compact_regime_codes | selected_regime_codes | regime_code_capture_fraction | compact_regime_entropy_bits | selected_regime_entropy_bits | regime_entropy_capture_fraction | compact_feed_profiles | selected_feed_profiles | feed_profile_capture_fraction | selected_source_rows | selected_market_shock_rows | selected_symbol_shock_rows | stratified_window_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | 22 | 11 | 11 | 11 | 1 | 3.29951 | 3.45943 | 1.04847 | 5 | 5 | 1 | 131555 | 23869 | 8202 | True |
| 2026-02 | 20 | 12 | 12 | 12 | 1 | 3.42163 | 3.58496 | 1.04774 | 5 | 5 | 1 | 143406 | 35785 | 13801 | True |
| 2026-03 | 22 | 12 | 12 | 12 | 1 | 3.26498 | 3.58496 | 1.098 | 5 | 5 | 1 | 143408 | 23833 | 6702 | True |
| 2026-04 | 22 | 11 | 11 | 11 | 1 | 3.11341 | 3.45943 | 1.11114 | 5 | 5 | 1 | 131434 | 23849 | 8935 | True |
| 2026-05 | 21 | 12 | 12 | 12 | 1 | 3.40439 | 3.58496 | 1.05304 | 5 | 5 | 1 | 143463 | 35821 | 3733 | True |
| 2026-06 | 22 | 13 | 13 | 13 | 1 | 3.51576 | 3.70044 | 1.05253 | 5 | 5 | 1 | 155346 | 59629 | 16386 | True |
| 2026-07 | 23 | 12 | 12 | 12 | 1 | 3.41421 | 3.58496 | 1.05001 | 5 | 5 | 1 | 143532 | 11950 | 6714 | True |
| 2026-08 | 21 | 13 | 13 | 13 | 1 | 3.59444 | 3.70044 | 1.02949 | 5 | 5 | 1 | 155426 | 23900 | 14540 | True |
| 2026-09 | 22 | 11 | 11 | 11 | 1 | 3.39097 | 3.45943 | 1.02019 | 5 | 5 | 1 | 131541 | 35829 | 13046 | True |
| 2026-10 | 22 | 11 | 11 | 11 | 1 | 3.24304 | 3.45943 | 1.06672 | 5 | 5 | 1 | 131565 | 0 | 2611 | True |
| 2026-11 | 21 | 14 | 14 | 14 | 1 | 3.68927 | 3.80735 | 1.03201 | 5 | 5 | 1 | 167311 | 35785 | 14547 | True |
| 2026-12 | 14 | 7 | 7 | 7 | 1 | 2.54869 | 2.80735 | 1.10149 | 5 | 5 | 1 | 83604 | 23833 | 5956 | True |

## Dense Control Verification

| trade_month | control_symbol | dense_path_exists | expected_selected_trade_dates | expected_selected_regime_codes | expected_feed_profiles | selected_dense_rows_found | selected_trade_dates_found | selected_regime_codes_found | selected_feed_profiles_found | min_local_sequence_id | max_local_sequence_id | dense_control_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | HDFCBANK | True | 11 | 11 | 5 | 8146420 | 11 | 11 | 5 | 1 | 16303665 | True |
| 2026-02 | HDFCBANK | True | 12 | 12 | 5 | 8902807 | 12 | 12 | 5 | 1488001 | 14828005 | True |
| 2026-03 | HDFCBANK | True | 12 | 12 | 5 | 8900007 | 12 | 12 | 5 | 1 | 16303665 | True |
| 2026-04 | HDFCBANK | True | 11 | 11 | 5 | 8132581 | 11 | 11 | 5 | 1 | 15548139 | True |
| 2026-05 | HDFCBANK | True | 12 | 12 | 5 | 8886830 | 12 | 12 | 5 | 1482049 | 14830142 | True |
| 2026-06 | HDFCBANK | True | 13 | 13 | 5 | 9623423 | 13 | 13 | 5 | 740033 | 16260030 | True |
| 2026-07 | HDFCBANK | True | 12 | 12 | 5 | 8887892 | 12 | 12 | 5 | 1 | 15542346 | True |
| 2026-08 | HDFCBANK | True | 13 | 13 | 5 | 9628845 | 13 | 13 | 5 | 2218113 | 15551951 | True |
| 2026-09 | HDFCBANK | True | 11 | 11 | 5 | 8153281 | 11 | 11 | 5 | 1 | 16279864 | True |
| 2026-10 | HDFCBANK | True | 11 | 11 | 5 | 8144480 | 11 | 11 | 5 | 1 | 16287798 | True |
| 2026-11 | HDFCBANK | True | 14 | 14 | 5 | 10390692 | 14 | 14 | 5 | 2230017 | 14104368 | True |
| 2026-12 | HDFCBANK | True | 7 | 7 | 5 | 5190634 | 7 | 7 | 5 | 738049 | 10373257 | True |

## Reader Contract Sample

| trade_month | reader_id | dense_where_predicate | feed_profiles | selected_trade_dates | contract |
| --- | --- | --- | --- | --- | --- |
| 2026-01 | P81_STRATIFIED_DENSE_WINDOW_2026-01 | trade_month = '2026-01' and trade_date in ('2026-01-01', '2026-01-02', '2026-01-06', '2026-01-07', '2026-01-09', '2026-01-13', '2026-01-15', '2026-01-19', '2026-01-22', '2026-01-26', '2026-01-30') and feed_profile in ('disconnect_scenario', 'good_retail', 'ideal_research', 'normal_retail', 'stressed_retail') | disconnect_scenario\|good_retail\|ideal_research\|normal_retail\|stressed_retail | 2026-01-01\|2026-01-02\|2026-01-06\|2026-01-07\|2026-01-09\|2026-01-13\|2026-01-15\|2026-01-19\|2026-01-22\|2026-01-26\|2026-01-30 | Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation. |
| 2026-02 | P81_STRATIFIED_DENSE_WINDOW_2026-02 | trade_month = '2026-02' and trade_date in ('2026-02-04', '2026-02-05', '2026-02-10', '2026-02-13', '2026-02-17', '2026-02-18', '2026-02-19', '2026-02-20', '2026-02-23', '2026-02-24', '2026-02-25', '2026-02-27') and feed_profile in ('disconnect_scenario', 'good_retail', 'ideal_research', 'normal_retail', 'stressed_retail') | disconnect_scenario\|good_retail\|ideal_research\|normal_retail\|stressed_retail | 2026-02-04\|2026-02-05\|2026-02-10\|2026-02-13\|2026-02-17\|2026-02-18\|2026-02-19\|2026-02-20\|2026-02-23\|2026-02-24\|2026-02-25\|2026-02-27 | Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation. |
| 2026-03 | P81_STRATIFIED_DENSE_WINDOW_2026-03 | trade_month = '2026-03' and trade_date in ('2026-03-02', '2026-03-03', '2026-03-04', '2026-03-05', '2026-03-06', '2026-03-12', '2026-03-13', '2026-03-16', '2026-03-19', '2026-03-20', '2026-03-30', '2026-03-31') and feed_profile in ('disconnect_scenario', 'good_retail', 'ideal_research', 'normal_retail', 'stressed_retail') | disconnect_scenario\|good_retail\|ideal_research\|normal_retail\|stressed_retail | 2026-03-02\|2026-03-03\|2026-03-04\|2026-03-05\|2026-03-06\|2026-03-12\|2026-03-13\|2026-03-16\|2026-03-19\|2026-03-20\|2026-03-30\|2026-03-31 | Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation. |
| 2026-04 | P81_STRATIFIED_DENSE_WINDOW_2026-04 | trade_month = '2026-04' and trade_date in ('2026-04-01', '2026-04-02', '2026-04-06', '2026-04-07', '2026-04-08', '2026-04-13', '2026-04-14', '2026-04-17', '2026-04-20', '2026-04-28', '2026-04-29') and feed_profile in ('disconnect_scenario', 'good_retail', 'ideal_research', 'normal_retail', 'stressed_retail') | disconnect_scenario\|good_retail\|ideal_research\|normal_retail\|stressed_retail | 2026-04-01\|2026-04-02\|2026-04-06\|2026-04-07\|2026-04-08\|2026-04-13\|2026-04-14\|2026-04-17\|2026-04-20\|2026-04-28\|2026-04-29 | Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation. |
| 2026-05 | P81_STRATIFIED_DENSE_WINDOW_2026-05 | trade_month = '2026-05' and trade_date in ('2026-05-05', '2026-05-08', '2026-05-13', '2026-05-14', '2026-05-18', '2026-05-20', '2026-05-21', '2026-05-22', '2026-05-25', '2026-05-26', '2026-05-27', '2026-05-28') and feed_profile in ('disconnect_scenario', 'good_retail', 'ideal_research', 'normal_retail', 'stressed_retail') | disconnect_scenario\|good_retail\|ideal_research\|normal_retail\|stressed_retail | 2026-05-05\|2026-05-08\|2026-05-13\|2026-05-14\|2026-05-18\|2026-05-20\|2026-05-21\|2026-05-22\|2026-05-25\|2026-05-26\|2026-05-27\|2026-05-28 | Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation. |
| 2026-06 | P81_STRATIFIED_DENSE_WINDOW_2026-06 | trade_month = '2026-06' and trade_date in ('2026-06-02', '2026-06-03', '2026-06-04', '2026-06-10', '2026-06-11', '2026-06-12', '2026-06-16', '2026-06-17', '2026-06-18', '2026-06-19', '2026-06-23', '2026-06-25', '2026-06-30') and feed_profile in ('disconnect_scenario', 'good_retail', 'ideal_research', 'normal_retail', 'stressed_retail') | disconnect_scenario\|good_retail\|ideal_research\|normal_retail\|stressed_retail | 2026-06-02\|2026-06-03\|2026-06-04\|2026-06-10\|2026-06-11\|2026-06-12\|2026-06-16\|2026-06-17\|2026-06-18\|2026-06-19\|2026-06-23\|2026-06-25\|2026-06-30 | Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation. |
| 2026-07 | P81_STRATIFIED_DENSE_WINDOW_2026-07 | trade_month = '2026-07' and trade_date in ('2026-07-01', '2026-07-02', '2026-07-03', '2026-07-07', '2026-07-08', '2026-07-14', '2026-07-15', '2026-07-17', '2026-07-22', '2026-07-27', '2026-07-28', '2026-07-29') and feed_profile in ('disconnect_scenario', 'good_retail', 'ideal_research', 'normal_retail', 'stressed_retail') | disconnect_scenario\|good_retail\|ideal_research\|normal_retail\|stressed_retail | 2026-07-01\|2026-07-02\|2026-07-03\|2026-07-07\|2026-07-08\|2026-07-14\|2026-07-15\|2026-07-17\|2026-07-22\|2026-07-27\|2026-07-28\|2026-07-29 | Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation. |
| 2026-08 | P81_STRATIFIED_DENSE_WINDOW_2026-08 | trade_month = '2026-08' and trade_date in ('2026-08-06', '2026-08-10', '2026-08-12', '2026-08-13', '2026-08-18', '2026-08-19', '2026-08-21', '2026-08-24', '2026-08-25', '2026-08-26', '2026-08-27', '2026-08-28', '2026-08-31') and feed_profile in ('disconnect_scenario', 'good_retail', 'ideal_research', 'normal_retail', 'stressed_retail') | disconnect_scenario\|good_retail\|ideal_research\|normal_retail\|stressed_retail | 2026-08-06\|2026-08-10\|2026-08-12\|2026-08-13\|2026-08-18\|2026-08-19\|2026-08-21\|2026-08-24\|2026-08-25\|2026-08-26\|2026-08-27\|2026-08-28\|2026-08-31 | Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation. |
| 2026-09 | P81_STRATIFIED_DENSE_WINDOW_2026-09 | trade_month = '2026-09' and trade_date in ('2026-09-01', '2026-09-03', '2026-09-04', '2026-09-14', '2026-09-16', '2026-09-17', '2026-09-22', '2026-09-23', '2026-09-24', '2026-09-28', '2026-09-30') and feed_profile in ('disconnect_scenario', 'good_retail', 'ideal_research', 'normal_retail', 'stressed_retail') | disconnect_scenario\|good_retail\|ideal_research\|normal_retail\|stressed_retail | 2026-09-01\|2026-09-03\|2026-09-04\|2026-09-14\|2026-09-16\|2026-09-17\|2026-09-22\|2026-09-23\|2026-09-24\|2026-09-28\|2026-09-30 | Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation. |
| 2026-10 | P81_STRATIFIED_DENSE_WINDOW_2026-10 | trade_month = '2026-10' and trade_date in ('2026-10-01', '2026-10-02', '2026-10-05', '2026-10-06', '2026-10-07', '2026-10-09', '2026-10-14', '2026-10-16', '2026-10-22', '2026-10-27', '2026-10-30') and feed_profile in ('disconnect_scenario', 'good_retail', 'ideal_research', 'normal_retail', 'stressed_retail') | disconnect_scenario\|good_retail\|ideal_research\|normal_retail\|stressed_retail | 2026-10-01\|2026-10-02\|2026-10-05\|2026-10-06\|2026-10-07\|2026-10-09\|2026-10-14\|2026-10-16\|2026-10-22\|2026-10-27\|2026-10-30 | Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation. |
| 2026-11 | P81_STRATIFIED_DENSE_WINDOW_2026-11 | trade_month = '2026-11' and trade_date in ('2026-11-05', '2026-11-09', '2026-11-10', '2026-11-11', '2026-11-12', '2026-11-13', '2026-11-16', '2026-11-17', '2026-11-19', '2026-11-20', '2026-11-23', '2026-11-24', '2026-11-25', '2026-11-26') and feed_profile in ('disconnect_scenario', 'good_retail', 'ideal_research', 'normal_retail', 'stressed_retail') | disconnect_scenario\|good_retail\|ideal_research\|normal_retail\|stressed_retail | 2026-11-05\|2026-11-09\|2026-11-10\|2026-11-11\|2026-11-12\|2026-11-13\|2026-11-16\|2026-11-17\|2026-11-19\|2026-11-20\|2026-11-23\|2026-11-24\|2026-11-25\|2026-11-26 | Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation. |
| 2026-12 | P81_STRATIFIED_DENSE_WINDOW_2026-12 | trade_month = '2026-12' and trade_date in ('2026-12-02', '2026-12-03', '2026-12-04', '2026-12-09', '2026-12-10', '2026-12-15', '2026-12-18') and feed_profile in ('disconnect_scenario', 'good_retail', 'ideal_research', 'normal_retail', 'stressed_retail') | disconnect_scenario\|good_retail\|ideal_research\|normal_retail\|stressed_retail | 2026-12-02\|2026-12-03\|2026-12-04\|2026-12-09\|2026-12-10\|2026-12-15\|2026-12-18 | Use this predicate instead of local_sequence_id prefix sampling for scenario-balanced dense validation. |

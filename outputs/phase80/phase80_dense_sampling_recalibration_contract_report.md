# Phase80 Dense Sampling Recalibration Contract

Generated UTC: 2026-07-19T20:22:10.238110+00:00

Phase80 reconciles the Phase79 dense-prefix diversity failure against the compact monthly source lake.
It distinguishes a genuinely weak generator from a biased dense-prefix replay window.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase80_compact_months_audited | 12 | Compact monthly source months audited |
| phase80_compact_min_regime_codes | 7 | Minimum compact regime codes per month |
| phase80_compact_median_regime_entropy_bits | 3.39768 | Median compact regime entropy |
| phase80_compact_min_feed_profiles | 5 | Minimum compact feed profiles per month |
| phase80_compact_generator_diversity_pass | 1 | 1 means compact source generator diversity is acceptable |
| phase80_dense_prefix_biased_months | 12 | Months where dense-prefix windows under-capture compact diversity |
| phase80_dense_prefix_capture_pass | 0 | 1 means dense-prefix scan windows capture compact diversity |
| phase80_replay_sampling_recalibration_required | 1 | 1 means replay/audit sampling must be recalibrated before new mining |
| phase80_recommend_next_action | implement_stratified_dense_window_reader | Recommended next milestone |

## Dense Prefix vs Compact Diversity

| trade_month | compact_rows | compact_days | compact_regime_codes | compact_regime_entropy_bits | compact_feed_profiles | compact_feed_entropy_bits | compact_market_shock_rows | compact_symbol_shock_rows | dense_prefix_regime_codes | dense_prefix_regime_entropy_bits | dense_prefix_feed_profiles | dense_prefix_feed_entropy_bits | dense_prefix_market_shock_symbols | dense_prefix_symbol_shock_symbols | regime_code_capture_fraction | regime_entropy_capture_fraction | feed_profile_capture_fraction | dense_prefix_sampling_bias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | 263102 | 22 | 11 | 3.29951 | 5 | 2.32191 | 23869 | 8202 | 1 | -0 | 2 | 0.975717 | 0 | 0 | 0.0909091 | -0 | 0.4 | True |
| 2026-02 | 238970 | 20 | 12 | 3.42163 | 5 | 2.32191 | 35785 | 14548 | 1 | -0 | 2 | 0.979281 | 0 | 0 | 0.0833333 | -0 | 0.4 | True |
| 2026-03 | 262973 | 22 | 12 | 3.26498 | 5 | 2.32191 | 23833 | 8572 | 1 | -0 | 2 | 0.975849 | 0 | 0 | 0.0833333 | -0 | 0.4 | True |
| 2026-04 | 262883 | 22 | 11 | 3.11341 | 5 | 2.32191 | 35777 | 10425 | 1 | -0 | 2 | 0.979158 | 32 | 1 | 0.0909091 | -0 | 0.4 | True |
| 2026-05 | 251038 | 21 | 12 | 3.40439 | 5 | 2.32191 | 35821 | 6334 | 1 | -0 | 2 | 0.976374 | 0 | 0 | 0.0833333 | -0 | 0.4 | True |
| 2026-06 | 262929 | 22 | 13 | 3.51576 | 5 | 2.32191 | 59629 | 18253 | 1 | -0 | 2 | 0.976635 | 0 | 0 | 0.0769231 | -0 | 0.4 | True |
| 2026-07 | 275062 | 23 | 12 | 3.41421 | 5 | 2.32191 | 11950 | 9702 | 1 | -0 | 2 | 0.977023 | 0 | 0 | 0.0833333 | -0 | 0.4 | True |
| 2026-08 | 251003 | 21 | 13 | 3.59444 | 5 | 2.32191 | 35835 | 21238 | 1 | -0 | 2 | 0.978041 | 0 | 0 | 0.0769231 | -0 | 0.4 | True |
| 2026-09 | 262989 | 22 | 11 | 3.39097 | 5 | 2.32191 | 59681 | 24988 | 1 | -0 | 2 | 0.977535 | 0 | 0 | 0.0909091 | -0 | 0.4 | True |
| 2026-10 | 263098 | 22 | 11 | 3.24304 | 5 | 2.32191 | 0 | 2611 | 1 | -0 | 2 | 0.978166 | 0 | 0 | 0.0909091 | -0 | 0.4 | True |
| 2026-11 | 250973 | 21 | 14 | 3.68927 | 5 | 2.32191 | 35785 | 14547 | 1 | -0 | 2 | 0.977151 | 0 | 0 | 0.0714286 | -0 | 0.4 | True |
| 2026-12 | 167274 | 14 | 7 | 2.54869 | 5 | 2.3219 | 23833 | 7826 | 1 | -0 | 2 | 0.977915 | 0 | 0 | 0.142857 | -0 | 0.4 | True |

## Dense Sampling Recalibration Contract

| contract_id | patch_target | required_change | evidence | acceptance_gate |
| --- | --- | --- | --- | --- |
| P80_STRATIFIED_DENSE_REPLAY_WINDOW | strategy_replay_and_generator_audit_readers | Replace local_sequence_id prefix sampling with stratified source-day/regime/feed-profile sampling or explicit full-month source-day windows. | 12/12 months show dense-prefix scenario capture bias. | For every replay validation month, sampled windows must capture at least 50% of compact regime codes, 50% of compact regime entropy, and 75% of compact feed profiles unless the test explicitly targets a single regime. |
| P80_SOURCE_DAY_BALANCED_ACCEPTANCE | future_phase79_and_strategy_falsification_runs | Report compact-source diversity and dense-window capture side by side before any profitability result can be interpreted. | Phase79 failed because dense-prefix windows saw one regime per month while compact months contain 7-14 regimes. | Profitability reports must include source-day/regime coverage evidence and mark results invalid if coverage gate fails. |
| P80_NO_MORE_PREFIX_ONLY_FALSIFICATION | phase77_like_disjoint_retests | Retain Phase77 as a falsification of the prefix/common-overlap HDFCBANK pocket, but do not generalize it to full generator diversity without stratified replay. | Phase77 used common-overlap prefix windows inherited from Phase75/76; Phase80 shows those windows are scenario-narrow. | New disjoint retests must be rerun with stratified windows before broad family-level conclusions are finalized. |

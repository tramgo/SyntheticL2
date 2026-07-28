# Phase188 Cost-aware Sparse Candidate Interpretation

Generated UTC: 2026-07-28T17:03:08.217917+00:00

Phase188 interprets the Phase187 validation-positive sparse candidate without opening test replay or promotion.
It audits date/symbol concentration, negative-control margin and profile robustness.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase188_interpretation_rows | 1 | Interpretation rows |
| phase188_gate_rows | 7 | Gates evaluated |
| phase188_hard_gate_rows | 7 | Hard gates evaluated |
| phase188_hard_gate_pass_rows | 7 | Hard gates passed |
| phase188_candidate_id | P187_TOP5_I85_S2p5_Z1_R100 | Interpreted candidate |
| phase188_validation_decision_events | 2646 | Validation dry decision events interpreted |
| phase188_min_profile_net_bps_proxy_mean | 46.3309 | Minimum profile validation net bps |
| phase188_min_profile_edge_over_shuffled_bps | 45.4392 | Minimum profile edge over shuffled-time control |
| phase188_top_symbol_event_share | 0.058579 | Top symbol decision-event share |
| phase188_top3_symbol_event_share | 0.172714 | Top 3 symbol decision-event share |
| phase188_concentration_warning | 0 | 1 means concentration review warning |
| phase188_symbol_positive_fraction | 0.0666667 | Fraction of symbol/profile groups net positive |
| phase188_breadth_warning | 1 | 1 means symbol breadth is weak |
| phase188_date_count_warning | 1 | 1 means validation evidence has fewer than two dates |
| phase188_robustness_interpretation | promising_but_breadth_limited_requires_phase189_precommit_or_redesign_decision | Interpretation verdict |
| phase188_interpretation_complete | 1 | 1 means Phase188 interpretation completed |
| phase188_test_replay_allowed_next | 0 | No test replay opened by Phase188 |
| phase188_promotion_allowed | 0 | No promotion opened |
| phase188_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase188_forbidden_outputs | test_result;test_replay;promotion;paper_live_acceptance;order_arrival;fill_model;pnl_replay;profitability_claim | Outputs forbidden in this phase |
| phase188_next_best_action | build_phase189_untouched_test_replay_precommit_or_redesign_decision | Recommended next milestone |

## Interpretation

| candidate_id | validation_decision_events | validation_symbols_with_events | validation_dates_with_events | overall_net_bps_proxy_mean | overall_gross_bps_proxy_mean | overall_cost_bps_mean | min_profile_net_bps_proxy_mean | min_profile_edge_over_shuffled_bps | date_positive_fraction | symbol_positive_fraction | top_symbol_event_share | top3_symbol_event_share | concentration_warning | breadth_warning | date_count_warning | robustness_interpretation | test_replay_allowed_by_phase188 | promotion_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P187_TOP5_I85_S2p5_Z1_R100 | 2646 | 30 | 1 | 47.3651 | 60.5943 | 13.2292 | 46.3309 | 45.4392 | 1 | 0.0666667 | 0.058579 | 0.172714 | 0 | 1 | 1 | promising_but_breadth_limited_requires_phase189_precommit_or_redesign_decision | 0 | 0 |

## By Date

| candidate_id | latency_profile_id | trade_date | decision_events | symbols | dates | gross_return_bps_proxy_mean | cost_bound_bps_mean | net_return_bps_after_cost_proxy_mean | net_positive_event_fraction | shuffled_time_net_bps_proxy_mean | net_edge_over_shuffled_time_bps_mean | net_positive_group | beats_shuffled_group |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | 2026-07-13 | 1323 | 30 | 1 | 60.5943 | 12.195 | 48.3994 | 0.00604686 | -12.2009 | 60.6002 | 1 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | 2026-07-13 | 1323 | 30 | 1 | 60.5943 | 14.2634 | 46.3309 | 0.00604686 | 0.891773 | 45.4392 | 1 | 1 |

## By Symbol

| candidate_id | latency_profile_id | symbol | decision_events | symbols | dates | gross_return_bps_proxy_mean | cost_bound_bps_mean | net_return_bps_after_cost_proxy_mean | net_positive_event_fraction | shuffled_time_net_bps_proxy_mean | net_edge_over_shuffled_time_bps_mean | net_positive_group | beats_shuffled_group |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | NIFTYBEES | 155 | 1 | 1 | 0.109243 | 14.2987 | -14.1895 | 0 | -143.321 | 129.132 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | NIFTYBEES | 155 | 1 | 1 | 0.109243 | 18.5384 | -18.4291 | 0 | -18.5767 | 0.147541 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | JUNIORBEES | 147 | 1 | 1 | 0.0932475 | 14.5444 | -14.4512 | 0 | -14.6287 | 0.177511 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | JUNIORBEES | 147 | 1 | 1 | 0.0932475 | 12.5179 | -12.4246 | 0 | 55.4006 | -67.8252 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | TCS | 120 | 1 | 1 | 0.10965 | 11.103 | -10.9933 | 0 | -11.1847 | 0.191422 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | TCS | 120 | 1 | 1 | 0.10965 | 12.1571 | -12.0474 | 0 | -11.8569 | -0.190568 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | HDFCBANK | 119 | 1 | 1 | 0.17702 | 13.2111 | -13.0341 | 0 | -13.2475 | 0.213397 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | HDFCBANK | 119 | 1 | 1 | 0.17702 | 11.4899 | -11.3129 | 0 | 72.6499 | -83.9628 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | BANKBEES | 105 | 1 | 1 | 0.00796974 | 12.9864 | -12.9784 | 0 | -108.145 | 95.1666 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | BANKBEES | 105 | 1 | 1 | 0.00796974 | 15.417 | -15.409 | 0 | -15.2602 | -0.148835 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | M&M | 83 | 1 | 1 | -0.112734 | 11.3497 | -11.4624 | 0 | -11.2014 | -0.261001 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | M&M | 83 | 1 | 1 | -0.112734 | 10.5425 | -10.6552 | 0 | -10.4939 | -0.161264 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ULTRACEMCO | 71 | 1 | 1 | 0.158098 | 11.6279 | -11.4698 | 0 | -152.595 | 141.125 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ULTRACEMCO | 71 | 1 | 1 | 0.158098 | 10.9042 | -10.7461 | 0 | -151.737 | 140.991 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ICICIBANK | 65 | 1 | 1 | 0.32918 | 10.9106 | -10.5814 | 0 | -11.2197 | 0.638261 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ICICIBANK | 65 | 1 | 1 | 0.32918 | 12.1057 | -11.7765 | 0 | -11.9693 | 0.192824 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | RELIANCE | 55 | 1 | 1 | 0.26611 | 13.0993 | -12.8332 | 0 | -13.3622 | 0.528933 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | RELIANCE | 55 | 1 | 1 | 0.26611 | 11.671 | -11.4049 | 0 | -11.8977 | 0.492857 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | WIPRO | 52 | 1 | 1 | 0.476201 | 22.6237 | -22.1475 | 0 | -22.4756 | 0.328187 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | WIPRO | 52 | 1 | 1 | 0.476201 | 16.3972 | -15.921 | 0 | -16.1262 | 0.205139 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ONGC | 45 | 1 | 1 | 0.080485 | 14.9945 | -14.9141 | 0 | 206.823 | -221.737 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ONGC | 45 | 1 | 1 | 0.080485 | 19.7032 | -19.6227 | 0 | -19.4015 | -0.22127 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | BHARTIARTL | 42 | 1 | 1 | -0.412703 | 11.2898 | -11.7025 | 0 | 226.999 | -238.701 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | BHARTIARTL | 42 | 1 | 1 | -0.412703 | 10.37 | -10.7827 | 0 | -10.2653 | -0.517432 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | MARUTI | 38 | 1 | 1 | 0.172815 | 11.0678 | -10.8949 | 0 | 252.289 | -263.184 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | MARUTI | 38 | 1 | 1 | 0.172815 | 11.8224 | -11.6496 | 0 | -11.7591 | 0.109563 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | NESTLEIND | 28 | 1 | 1 | -0.0146572 | 11.3185 | -11.3332 | 0 | -11.1072 | -0.226003 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | HCLTECH | 28 | 1 | 1 | 0.332754 | 12.185 | -11.8522 | 0 | -12.4353 | 0.583134 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | NESTLEIND | 28 | 1 | 1 | -0.0146572 | 12.6062 | -12.6209 | 0 | -12.7324 | 0.111487 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | HCLTECH | 28 | 1 | 1 | 0.332754 | 13.7788 | -13.4461 | 0 | 343.405 | -356.851 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | LT | 25 | 1 | 1 | 0.2049 | 10.5088 | -10.3039 | 0 | -10.3486 | 0.0446446 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | LT | 25 | 1 | 1 | 0.2049 | 11.2608 | -11.0559 | 0 | -10.7482 | -0.307649 | 0 | 0 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | ADANIPORTS | 21 | 1 | 1 | 0.58988 | 12.4522 | -11.8623 | 0 | -12.8242 | 0.961927 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | ADANIPORTS | 21 | 1 | 1 | 0.58988 | 11.2848 | -10.695 | 0 | -11.5044 | 0.809395 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | INFY | 20 | 1 | 1 | 0.843937 | 11.5618 | -10.7179 | 0 | -11.3862 | 0.668272 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | INFY | 20 | 1 | 1 | 0.843937 | 13.0713 | -12.2273 | 0 | -12.7979 | 0.570539 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | CIPLA | 19 | 1 | 1 | 0.128781 | 13.0809 | -12.9521 | 0 | -13.6405 | 0.688342 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | CIPLA | 19 | 1 | 1 | 0.128781 | 11.6979 | -11.5691 | 0 | -11.6077 | 0.0385977 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_RETAIL_MARKETABLE_DEFAULT | SUNPHARMA | 18 | 1 | 1 | 0.201352 | 11.3285 | -11.1272 | 0 | -11.4499 | 0.322762 | 0 | 1 |
| P187_TOP5_I85_S2p5_Z1_R100 | P180_STRESSED_RETAIL | SUNPHARMA | 18 | 1 | 1 | 0.201352 | 12.4834 | -12.2821 | 0 | 543.185 | -555.467 | 0 | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P188_PHASE187_CANDIDATE_COMPLETE | 1 | phase187_cost_aware_sparse_candidate_complete=1 | hard |
| P188_VALIDATION_POSITIVE_ALL_PROFILES_ACKNOWLEDGED | 1 | phase187_validation_positive_all_profiles=1 | hard |
| P188_DATE_SYMBOL_CONCENTRATION_AUDIT_PRESENT | 1 | date_rows=2; symbol_rows=60 | hard |
| P188_NEGATIVE_CONTROL_MARGIN_POSITIVE | 1 | min_profile_edge_over_shuffled_bps=45.439161105260446 | hard |
| P188_CONCENTRATION_REVIEW_RECORDED | 1 | concentration_warning=0 | hard |
| P188_BREADTH_REVIEW_RECORDED | 1 | breadth_warning=1; date_count_warning=1 | hard |
| P188_NO_TEST_REPLAY_OR_PROMOTION | 1 | test_replay_allowed_by_phase188=0; promotion_allowed=0 | hard |

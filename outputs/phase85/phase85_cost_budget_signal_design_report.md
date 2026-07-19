# Phase85 Cost-Budget Signal Design Gate

Generated UTC: 2026-07-19T20:56:40.411465+00:00

Phase85 creates a cost-budget gate for future strategy work using the Phase83 cached stratified bars.
It estimates one-way retail execution hurdles from spread, slippage, impact, and Zerodha charges before allowing any new replay branch.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase85_symbol_month_rows | 384 | Symbol-month cost budget rows |
| phase85_tail_edge_available_symbol_month_fraction | 1 | Fraction of symbol-months with tail edge available |
| phase85_feature_filter_rows | 35 | Feature filter budget rows |
| phase85_eligible_filter_seeds | 35 | Feature filters passing cost-budget eligibility |
| phase85_allowed_precommit_contracts | 10 | Allowed precommit filter contracts |
| phase85_cost_budget_signal_design_pass | 1 | 1 means at least one filter seed can move to precommitted signal design |
| phase85_recommend_next_action | precommit_composite_regime_conditioned_signal_family | Recommended next milestone |

## Monthly Cost Budget Summary

| trade_month | symbols | median_symbol_cost_hurdle_bps | median_symbol_p95_abs_next_return_bps | median_fraction_abs_return_ge_1_25x_cost | tail_edge_available_symbols | tail_edge_available_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | 32 | 11.8561 | 180.894 | 0.770196 | 32 | 1 |
| 2026-02 | 32 | 12.4297 | 196.231 | 0.792308 | 32 | 1 |
| 2026-03 | 32 | 12.1728 | 135.73 | 0.769128 | 32 | 1 |
| 2026-04 | 32 | 11.901 | 170.004 | 0.788592 | 32 | 1 |
| 2026-05 | 32 | 12.4225 | 118.767 | 0.762816 | 32 | 1 |
| 2026-06 | 32 | 12.5777 | 205.162 | 0.789098 | 32 | 1 |
| 2026-07 | 32 | 12.1694 | 137.7 | 0.759251 | 32 | 1 |
| 2026-08 | 32 | 12.444 | 183.748 | 0.81132 | 32 | 1 |
| 2026-09 | 32 | 12.0573 | 181.725 | 0.805556 | 32 | 1 |
| 2026-10 | 32 | 11.8325 | 130.01 | 0.772523 | 32 | 1 |
| 2026-11 | 32 | 12.4258 | 176.941 | 0.773872 | 32 | 1 |
| 2026-12 | 32 | 12.3883 | 189.433 | 0.753285 | 32 | 1 |

## Top Feature Filter Cost-Budget Rows

| feature_name | quantile | threshold | selected_bars | selected_fraction | mean_abs_next_return_bps | median_abs_next_return_bps | median_cost_hurdle_bps | fraction_abs_return_ge_1x_cost | fraction_abs_return_ge_1_25x_cost | fraction_abs_return_ge_1_5x_cost | candidate_budget_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| event_intensity | 0.99 | 197.3 | 1463 | 0.0100914 | 172.08 | 162.907 | 15.5857 | 0.958305 | 0.947368 | 0.935748 | eligible_filter_seed |
| event_intensity | 0.975 | 190.1 | 3658 | 0.0252319 | 156.964 | 140.502 | 15.8175 | 0.943685 | 0.934664 | 0.921815 | eligible_filter_seed |
| abs_bar_return | 0.99 | 276.162 | 1451 | 0.0100086 | 137.183 | 126.368 | 15.4852 | 0.935906 | 0.922812 | 0.901447 | eligible_filter_seed |
| event_intensity | 0.95 | 182.6 | 7269 | 0.0501397 | 146.791 | 125.016 | 15.952 | 0.930114 | 0.918283 | 0.902738 | eligible_filter_seed |
| event_intensity | 0.9 | 164.3 | 14530 | 0.100224 | 146.661 | 124.327 | 15.772 | 0.931452 | 0.917343 | 0.901996 | eligible_filter_seed |
| event_intensity | 0.8 | 148.3 | 29168 | 0.201193 | 110.49 | 85.4701 | 14.4684 | 0.904244 | 0.883365 | 0.861938 | eligible_filter_seed |
| abs_bar_return | 0.975 | 213.418 | 3631 | 0.0250457 | 119.969 | 98.6156 | 14.8243 | 0.889838 | 0.868631 | 0.841641 | eligible_filter_seed |
| event_intensity | 0.7 | 139.5 | 43518 | 0.300176 | 94.5346 | 71.2336 | 14.1791 | 0.889816 | 0.865136 | 0.84002 | eligible_filter_seed |
| abs_bar_return | 0.95 | 167.742 | 7250 | 0.0500086 | 109.224 | 86.1735 | 14.5488 | 0.886897 | 0.863448 | 0.833793 | eligible_filter_seed |
| abs_bar_return | 0.9 | 126.999 | 14498 | 0.100003 | 96.4209 | 71.2128 | 14.1749 | 0.876673 | 0.851497 | 0.820803 | eligible_filter_seed |
| event_intensity | 0.5 | 126.3 | 72491 | 0.500024 | 77.9374 | 57.9584 | 13.3977 | 0.869694 | 0.840022 | 0.809687 | eligible_filter_seed |
| abs_bar_return | 0.8 | 86.6025 | 28995 | 0.2 | 84.946 | 60.523 | 13.6557 | 0.867701 | 0.835972 | 0.805863 | eligible_filter_seed |
| abs_bar_return | 0.7 | 65.5272 | 43493 | 0.300003 | 77.1523 | 54.8024 | 13.2225 | 0.858759 | 0.826248 | 0.794082 | eligible_filter_seed |
| abs_bar_return | 0.5 | 38.1008 | 72489 | 0.50001 | 68.736 | 48.9884 | 12.9492 | 0.846653 | 0.810385 | 0.775594 | eligible_filter_seed |
| abs_l1_imbalance | 0.99 | 0.741085 | 1451 | 0.0100086 | 50.4491 | 39.4059 | 13.4352 | 0.822881 | 0.769814 | 0.731909 | eligible_filter_seed |
| abs_microprice_dev_bps | 0.975 | 1.44701 | 3627 | 0.0250181 | 81.7757 | 53.6278 | 18.0704 | 0.81362 | 0.768955 | 0.732837 | eligible_filter_seed |
| abs_microprice_dev_bps | 0.99 | 2.21578 | 1450 | 0.0100017 | 93.1664 | 59.6921 | 18.2318 | 0.826207 | 0.766207 | 0.732414 | eligible_filter_seed |
| abs_microprice_dev_bps | 0.5 | 0.251308 | 72491 | 0.500024 | 58.867 | 39.7573 | 13.3486 | 0.807507 | 0.764136 | 0.723428 | eligible_filter_seed |
| abs_l5_imbalance | 0.99 | 0.741113 | 1450 | 0.0100017 | 51.2056 | 39.9878 | 13.4323 | 0.809655 | 0.762759 | 0.726897 | eligible_filter_seed |
| abs_microprice_dev_bps | 0.95 | 1.25965 | 7249 | 0.0500017 | 73.6382 | 47.3543 | 16.8196 | 0.805766 | 0.759553 | 0.721341 | eligible_filter_seed |
| abs_microprice_dev_bps | 0.8 | 0.580877 | 28996 | 0.200007 | 64.8167 | 42.5671 | 14.2478 | 0.806146 | 0.75876 | 0.717306 | eligible_filter_seed |
| abs_l1_imbalance | 0.7 | 0.368481 | 43495 | 0.300017 | 53.7788 | 37.2328 | 12.9633 | 0.801012 | 0.756547 | 0.715622 | eligible_filter_seed |
| abs_l5_imbalance | 0.7 | 0.368465 | 43500 | 0.300052 | 53.6651 | 37.1134 | 12.9626 | 0.80023 | 0.755655 | 0.714552 | eligible_filter_seed |
| abs_l5_imbalance | 0.5 | 0.198206 | 72488 | 0.500003 | 53.8821 | 37.176 | 12.7414 | 0.799843 | 0.755022 | 0.712132 | eligible_filter_seed |
| abs_l1_imbalance | 0.5 | 0.199749 | 72488 | 0.500003 | 53.8356 | 37.1737 | 12.7573 | 0.799926 | 0.754856 | 0.712159 | eligible_filter_seed |

## Precommit Signal Filter Contract

| contract_id | allowed | feature_name | quantile | threshold | fraction_abs_return_ge_1_25x_cost | rule | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P85_ELIGIBLE_FILTER_SEED_01 | True | event_intensity | 0.99 | 197.3 | 0.947368 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_02 | True | event_intensity | 0.975 | 190.1 | 0.934664 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_03 | True | abs_bar_return | 0.99 | 276.162 | 0.922812 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_04 | True | event_intensity | 0.95 | 182.6 | 0.918283 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_05 | True | event_intensity | 0.9 | 164.3 | 0.917343 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_06 | True | event_intensity | 0.8 | 148.3 | 0.883365 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_07 | True | abs_bar_return | 0.975 | 213.418 | 0.868631 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_08 | True | event_intensity | 0.7 | 139.5 | 0.865136 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_09 | True | abs_bar_return | 0.95 | 167.742 | 0.863448 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_10 | True | abs_bar_return | 0.9 | 126.999 | 0.851497 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |

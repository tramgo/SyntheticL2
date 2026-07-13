# Phase 13 Experiment Run Smoke Report

Generated UTC: 2026-07-13T22:03:11.030776+00:00

## Scope

This is a deterministic engineering smoke ledger over the pre-registered Phase 13 initial experiment rows.
It uses existing Phase 11 signal diagnostics and Phase 12 execution summaries; it is not a full experiment execution, parameter search, walk-forward result or promotion result.

## Manifest Summary

- Registered rows evaluated: 324
- Strategies: 9
- Controls: 4
- Execution profile: retail_marketable_default
- Robustness execution profiles: ['retail_marketable_default', 'stressed_retail', 'zero_latency_spread_only_control']
- Acceptance eligible: False

## Strategy Robustness Smoke Summary

| strategy_id | run_rows | base_rows | negative_control_rows | interpretable_negative_control_rows | passed_negative_control_rows | positive_base_rows | median_base_net_return | worst_control_net_return | robustness_smoke_status | acceptance_eligible | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | 36 | 9 | 27 | 27 | 18 | 9 | 0.006451115540031 | -0.006451115540031 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S02 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0011430818376006 | -0.00040007864316021 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S03 | 36 | 9 | 27 | 27 | 18 | 9 | 0.0050215903769418 | -0.0050215903769418 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S04 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0004006507711948 | -0.00014022776991817998 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S05 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0022514659545176 | -0.0007880130840811601 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S06 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0017628356795214 | -0.0006169924878324899 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S07 | 36 | 9 | 27 | 0 | 0 | 0 | -0.001066182425619 | -0.00037316384896665 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S08 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0010654318680528 | -0.00037290115381847995 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |
| S09 | 36 | 9 | 27 | 0 | 0 | 0 | -0.0010539616922056 | -0.00036888659227196 | executed_proxy_smoke_not_acceptance | False | Proxy smoke ledger only; full multi-seed walk-forward, parameter-smoothness, holdout and real rerun evidence is still missing. |

## Control Summary

| control_id | run_rows | strategies | mean_proxy_net_return | mean_proxy_signal_fraction | interpretable_rows |
| --- | --- | --- | --- | --- | --- |
| BASE | 81 | 9 | 0.00030323285425122224 | 0.17267142188000106 | 0 |
| NC01 | 81 | 9 | 1.5161642712561107e-05 | 0.17267142188000106 | 18 |
| NC02 | 81 | 9 | 0.00010613149898792776 | 0.15540427969200096 | 18 |
| NC03 | 81 | 9 | -0.00030323285425122224 | 0.17267142188000106 | 18 |

## Multi-Profile Robustness Proxy Summary

| strategy_id | execution_profiles_evaluated | base_profile_rows | positive_base_profiles | all_profiles_positive | retail_profile_positive | stressed_profile_positive | worst_profile_base_net_return | best_profile_base_net_return | profile_base_net_return_range | interpretable_negative_control_rows | passed_negative_control_rows | profile_robustness_status | acceptance_eligible | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | 3 | 3 | 1 | False | True | False | -0.0079238299884688 | 0.006451115540031 | 0.0143749455284998 | 27 | 18 | multi_profile_proxy_not_acceptance | False | Multi-profile proxy robustness evidence exists, but full multi-seed, walk-forward, parameter-smoothness, holdout-generator and real-data rerun evidence is still missing. |
| S02 | 3 | 3 | 0 | False | False | False | -0.0014380631843309 | -0.0002990898986589 | 0.001138973285672 | 0 | 0 | multi_profile_proxy_not_acceptance | False | Multi-profile proxy robustness evidence exists, but full multi-seed, walk-forward, parameter-smoothness, holdout-generator and real-data rerun evidence is still missing. |
| S03 | 3 | 3 | 1 | False | True | False | -0.0066621402674241 | 0.0050215903769418 | 0.0116837306443659 | 27 | 18 | multi_profile_proxy_not_acceptance | False | Multi-profile proxy robustness evidence exists, but full multi-seed, walk-forward, parameter-smoothness, holdout-generator and real-data rerun evidence is still missing. |
| S04 | 3 | 3 | 0 | False | False | False | -0.0013854630797482 | -0.0004006507711948 | 0.0009848123085534001 | 0 | 0 | multi_profile_proxy_not_acceptance | False | Multi-profile proxy robustness evidence exists, but full multi-seed, walk-forward, parameter-smoothness, holdout-generator and real-data rerun evidence is still missing. |
| S05 | 3 | 3 | 1 | False | False | False | -0.0022514659545176 | 0.0011650700188144 | 0.003416535973332 | 27 | 18 | multi_profile_proxy_not_acceptance | False | Multi-profile proxy robustness evidence exists, but full multi-seed, walk-forward, parameter-smoothness, holdout-generator and real-data rerun evidence is still missing. |
| S06 | 3 | 3 | 1 | False | False | False | -0.0017628356795214 | 0.0001855334584192 | 0.0019483691379406 | 27 | 18 | multi_profile_proxy_not_acceptance | False | Multi-profile proxy robustness evidence exists, but full multi-seed, walk-forward, parameter-smoothness, holdout-generator and real-data rerun evidence is still missing. |
| S07 | 3 | 3 | 0 | False | False | False | -0.0016241453468308 | -0.0008735786643444 | 0.0007505666824864 | 0 | 0 | multi_profile_proxy_not_acceptance | False | Multi-profile proxy robustness evidence exists, but full multi-seed, walk-forward, parameter-smoothness, holdout-generator and real-data rerun evidence is still missing. |
| S08 | 3 | 3 | 0 | False | False | False | -0.0013552244852151 | -0.000148133053968 | 0.0012070914312471 | 0 | 0 | multi_profile_proxy_not_acceptance | False | Multi-profile proxy robustness evidence exists, but full multi-seed, walk-forward, parameter-smoothness, holdout-generator and real-data rerun evidence is still missing. |
| S09 | 3 | 3 | 0 | False | False | False | -0.0012864231169767 | -0.0002711679119243 | 0.0010152552050524 | 0 | 0 | multi_profile_proxy_not_acceptance | False | Multi-profile proxy robustness evidence exists, but full multi-seed, walk-forward, parameter-smoothness, holdout-generator and real-data rerun evidence is still missing. |

## Robustness Dimension Coverage Summary

| strategy_id | registered_for_phase13_proxy | proxy_run_rows | profile_robustness_rows | initial_engineering_seeds_run | required_full_validation_seeds | seed_scope_status | quarter_profiles_run | execution_profiles_evaluated | all_execution_profiles_positive | stressed_profile_positive | negative_control_rows | interpretable_negative_control_rows | passed_negative_control_rows | parameter_sets_planned | parameter_sets_run | parameter_smoothness_status | walk_forward_windows_planned | walk_forward_windows_run | walk_forward_status | holdout_generator_profiles_available | holdout_generator_profiles_present_in_proxy | holdout_status | real_data_rerun_status | dimension_status | acceptance_eligible | blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | True | 36 | 108 | 9 | 30 | initial_engineering_seed_proxy_only | 3 | 3 | False | False | 27 | 27 | 18 | 18 | 1 | design_available_single_parameter_proxy_run | 48 | 0 | design_available_not_run | 2 | 2 | holdout_profiles_present_as_proxy_not_rerun_acceptance | not_available_one_day_seed_only | robustness_proxy_dimensions_available_not_acceptance | False | Robustness proxy dimensions are now summarized, but acceptance still requires full required-seed execution, walk-forward runs, parameter-neighborhood smoothness, holdout-generator strategy reruns and later multi-day real-data reruns. |
| S02 | True | 36 | 108 | 9 | 30 | initial_engineering_seed_proxy_only | 3 | 3 | False | False | 27 | 0 | 0 | 6 | 1 | design_available_single_parameter_proxy_run | 48 | 0 | design_available_not_run | 2 | 2 | holdout_profiles_present_as_proxy_not_rerun_acceptance | not_available_one_day_seed_only | robustness_proxy_dimensions_available_not_acceptance | False | Robustness proxy dimensions are now summarized, but acceptance still requires full required-seed execution, walk-forward runs, parameter-neighborhood smoothness, holdout-generator strategy reruns and later multi-day real-data reruns. |
| S03 | True | 36 | 108 | 9 | 30 | initial_engineering_seed_proxy_only | 3 | 3 | False | False | 27 | 27 | 18 | 6 | 1 | design_available_single_parameter_proxy_run | 48 | 0 | design_available_not_run | 2 | 2 | holdout_profiles_present_as_proxy_not_rerun_acceptance | not_available_one_day_seed_only | robustness_proxy_dimensions_available_not_acceptance | False | Robustness proxy dimensions are now summarized, but acceptance still requires full required-seed execution, walk-forward runs, parameter-neighborhood smoothness, holdout-generator strategy reruns and later multi-day real-data reruns. |
| S04 | True | 36 | 108 | 9 | 30 | initial_engineering_seed_proxy_only | 3 | 3 | False | False | 27 | 0 | 0 | 4 | 1 | design_available_single_parameter_proxy_run | 48 | 0 | design_available_not_run | 2 | 2 | holdout_profiles_present_as_proxy_not_rerun_acceptance | not_available_one_day_seed_only | robustness_proxy_dimensions_available_not_acceptance | False | Robustness proxy dimensions are now summarized, but acceptance still requires full required-seed execution, walk-forward runs, parameter-neighborhood smoothness, holdout-generator strategy reruns and later multi-day real-data reruns. |
| S05 | True | 36 | 108 | 9 | 30 | initial_engineering_seed_proxy_only | 3 | 3 | False | False | 27 | 0 | 0 | 3 | 1 | design_available_single_parameter_proxy_run | 48 | 0 | design_available_not_run | 2 | 2 | holdout_profiles_present_as_proxy_not_rerun_acceptance | not_available_one_day_seed_only | robustness_proxy_dimensions_available_not_acceptance | False | Robustness proxy dimensions are now summarized, but acceptance still requires full required-seed execution, walk-forward runs, parameter-neighborhood smoothness, holdout-generator strategy reruns and later multi-day real-data reruns. |
| S06 | True | 36 | 108 | 9 | 30 | initial_engineering_seed_proxy_only | 3 | 3 | False | False | 27 | 0 | 0 | 4 | 1 | design_available_single_parameter_proxy_run | 48 | 0 | design_available_not_run | 2 | 2 | holdout_profiles_present_as_proxy_not_rerun_acceptance | not_available_one_day_seed_only | robustness_proxy_dimensions_available_not_acceptance | False | Robustness proxy dimensions are now summarized, but acceptance still requires full required-seed execution, walk-forward runs, parameter-neighborhood smoothness, holdout-generator strategy reruns and later multi-day real-data reruns. |
| S07 | True | 36 | 108 | 9 | 30 | initial_engineering_seed_proxy_only | 3 | 3 | False | False | 27 | 0 | 0 | 4 | 1 | design_available_single_parameter_proxy_run | 48 | 0 | design_available_not_run | 2 | 2 | holdout_profiles_present_as_proxy_not_rerun_acceptance | not_available_one_day_seed_only | robustness_proxy_dimensions_available_not_acceptance | False | Robustness proxy dimensions are now summarized, but acceptance still requires full required-seed execution, walk-forward runs, parameter-neighborhood smoothness, holdout-generator strategy reruns and later multi-day real-data reruns. |
| S08 | True | 36 | 108 | 9 | 30 | initial_engineering_seed_proxy_only | 3 | 3 | False | False | 27 | 0 | 0 | 9 | 1 | design_available_single_parameter_proxy_run | 48 | 0 | design_available_not_run | 2 | 2 | holdout_profiles_present_as_proxy_not_rerun_acceptance | not_available_one_day_seed_only | robustness_proxy_dimensions_available_not_acceptance | False | Robustness proxy dimensions are now summarized, but acceptance still requires full required-seed execution, walk-forward runs, parameter-neighborhood smoothness, holdout-generator strategy reruns and later multi-day real-data reruns. |
| S09 | True | 36 | 108 | 9 | 30 | initial_engineering_seed_proxy_only | 3 | 3 | False | False | 27 | 0 | 0 | 9 | 1 | design_available_single_parameter_proxy_run | 48 | 0 | design_available_not_run | 2 | 2 | holdout_profiles_present_as_proxy_not_rerun_acceptance | not_available_one_day_seed_only | robustness_proxy_dimensions_available_not_acceptance | False | Robustness proxy dimensions are now summarized, but acceptance still requires full required-seed execution, walk-forward runs, parameter-neighborhood smoothness, holdout-generator strategy reruns and later multi-day real-data reruns. |
| S10 | False | 0 | 0 | 0 | 30 | not_run | 0 | 0 | False | False | 0 | 0 | 0 | 0 | 0 | not_registered_or_not_run | 48 | 0 | design_available_not_run | 2 | 0 | holdout_proxy_not_present_for_strategy | not_available_one_day_seed_only | not_registered_for_phase13_proxy_run | False | Strategy is not registered in the current Phase 13 alpha-parameter proxy grid; robustness acceptance evidence is missing. |
| S11 | False | 0 | 0 | 0 | 30 | not_run | 0 | 0 | False | False | 0 | 0 | 0 | 0 | 0 | not_registered_or_not_run | 48 | 0 | design_available_not_run | 2 | 0 | holdout_proxy_not_present_for_strategy | not_available_one_day_seed_only | not_registered_for_phase13_proxy_run | False | Strategy is not registered in the current Phase 13 alpha-parameter proxy grid; robustness acceptance evidence is missing. |

## Caveat

The output closes the bookkeeping gap between a planned registry and auditable proxy run ledgers, including execution-profile sensitivity and dimension coverage, but it does not close the acceptance-grade robustness gate.

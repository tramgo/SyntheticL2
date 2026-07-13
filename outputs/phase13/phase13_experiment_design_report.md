# Phase 13 Experiment Design Report

Generated UTC: 2026-07-13T20:34:56.994112+00:00

## Scope

This phase defines experiment splits, seed plans, walk-forward windows, predeclared parameter grids and negative controls.
It does not run or promote strategy results.

## Segment Summary

| quarter_profile | experiment_segment | days |
| --- | --- | --- |
| Q-A | calibration_development | 30 |
| Q-A | untouched_test | 18 |
| Q-A | validation | 15 |
| Q-B | calibration_development | 30 |
| Q-B | untouched_test | 18 |
| Q-B | validation | 15 |
| Q-C | calibration_development | 30 |
| Q-C | untouched_test | 18 |
| Q-C | validation | 15 |

## Seed Plan

- Quarter profiles: 3
- Full validation seeds: 30
- Initial engineering seeds: 9

## Walk-Forward Windows

- Windows: 48

## Parameter Sets

| strategy_id | parameter_sets |
| --- | --- |
| S01 | 18 |
| S02 | 6 |
| S03 | 6 |
| S04 | 4 |
| S05 | 3 |
| S06 | 4 |
| S07 | 4 |
| S08 | 9 |
| S09 | 9 |

## Negative Controls

| negative_control_id | control_name | mandatory |
| --- | --- | --- |
| NC01 | shuffle_signal_time_bucket | True |
| NC02 | delayed_signal | True |
| NC03 | inverted_signal | True |
| NC04 | random_matched_turnover | True |
| NC05 | no_predictive_coupling_data | True |
| NC06 | zero_cost_vs_realistic_cost | True |
| NC07 | zero_latency_vs_realistic_latency | True |
| NC08 | hide_regime_labels | True |
| NC09 | cross_ticker_timestamp_shift | True |

## Registry Skeleton

- Planned initial experiments: 324

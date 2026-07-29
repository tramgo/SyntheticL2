# Phase232 Phase231 Candidate Validation

Generated UTC: 2026-07-29T06:18:53.528575+00:00

Phase232 validates only the Phase231 train+test synthetic candidates using stricter holdout/concentration checks,
cost stress, side-flip negative controls and deterministic random-side controls.
Passing this phase is still synthetic-only validation; it does not promote a strategy or authorize paper/live use.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase232_validate_phase231_candidates_complete | 1 | Phase232 validation completed |
| phase232_phase231_candidate_rows | 3 | Phase231 train+test candidates validated |
| phase232_negative_control_pass_rows | 3 | Candidates passing negative controls |
| phase232_cost_stress_pass_rows | 3 | Candidates passing cost stress |
| phase232_holdout_stability_pass_rows | 1 | Candidates passing holdout/concentration stability |
| phase232_validated_synthetic_candidate_rows | 1 | Candidates passing all Phase232 gates |
| phase232_best_candidate_id | P231_MICROPRICE_REVERSAL_H3_Q0_9 | Best validated or ranked candidate |
| phase232_best_test_net_pnl_inr | 229963 | Best candidate test net P&L |
| phase232_best_test_random_side_beat_fraction | 1 | Best candidate test random-side beat fraction |
| phase232_best_test_leave_one_month_min_net_pnl_inr | 116948 | Best candidate minimum leave-one-test-month net P&L |
| phase232_strategy_promotion_allowed | 0 | No promotion from synthetic validation alone |
| phase232_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from synthetic validation alone |
| phase232_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from synthetic validation alone |
| phase232_next_best_action | run_phase233_fragility_and_realism_validation_for_phase232_candidates_no_paper_live | Next validation milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | interpretation |
| --- | --- | --- | --- | --- |
| P232_PHASE231_CANDIDATES_AVAILABLE | True | 3 | >0 Phase231 candidates | Phase232 has Phase231 candidates to validate. |
| P232_NEGATIVE_CONTROLS_PASS | True | 3 | >0 candidates pass side-flip and random-side controls | Candidate performance beats deterministic negative controls. |
| P232_COST_STRESS_PASS | True | 3 | >0 candidates pass cost stress | Candidate remains positive under 1.25x train/test and 1.50x test cost stress. |
| P232_HOLDOUT_STABILITY_PASS | True | 1 | >0 candidates pass month/symbol stability | Candidate is not solely one-month or one-symbol dominated under the configured thresholds. |
| P232_VALIDATED_SYNTHETIC_CANDIDATE_FOUND | True | 1 | >0 candidates pass all Phase232 validation gates | Validated synthetic candidates may proceed to stricter fragility/realism validation, not promotion. |

## Candidate Validation Summary

| candidate_id | family_id | horizon_event_bars | threshold_quantile | phase231_train_net_pnl_inr | phase231_test_net_pnl_inr | train_trades | train_net_pnl_inr | train_gross_pnl_inr | train_cost_pnl_drag_inr | train_positive_months | train_months | train_symbols | train_days | train_min_month_net_pnl_inr | train_leave_one_month_min_net_pnl_inr | train_max_month_contribution_abs | train_max_symbol_contribution_abs | test_trades | test_net_pnl_inr | test_gross_pnl_inr | test_cost_pnl_drag_inr | test_positive_months | test_months | test_symbols | test_days | test_min_month_net_pnl_inr | test_leave_one_month_min_net_pnl_inr | test_max_month_contribution_abs | test_max_symbol_contribution_abs | train_random_side_beat_fraction | test_random_side_beat_fraction | test_random_side_p95_net_pnl_inr | test_side_flip_net_pnl_inr | train_cost_125_pass | test_cost_125_pass | test_cost_150_pass | negative_controls_pass | cost_stress_pass | holdout_stability_pass | phase232_validated_synthetic_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL | 3 | 0.9 | 353035 | 229963 | 471 | 353035 | 420199 | 67164.4 | 6 | 6 | 8 | 18 | 331.929 | 184299 | 0.477958 | 0.289776 | 365 | 229963 | 280316 | 50353.1 | 4 | 6 | 8 | 19 | -15418.8 | 116948 | 0.491447 | 0.315216 | 1 | 1 | 14548.1 | -330669 | True | True | True | True | True | True | True |
| P231_L5_IMBALANCE_REVERSAL_H3_Q0_9 | P231_L5_IMBALANCE_REVERSAL | 3 | 0.9 | 63582.2 | 89257.6 | 376 | 63582.2 | 109659 | 46076.5 | 5 | 6 | 5 | 30 | -18008.9 | 39366.8 | 0.380852 | 1.02324 | 364 | 89257.6 | 131819 | 42561.7 | 4 | 6 | 5 | 28 | -18855.1 | 16203 | 0.818469 | 0.564834 | 0.99 | 0.99 | 6075.78 | -174381 | True | True | True | True | True | False | False |
| P231_MICROPRICE_REVERSAL_H3_Q0_95 | P231_MICROPRICE_REVERSAL | 3 | 0.95 | 113918 | 83574.3 | 165 | 113918 | 139137 | 25218.4 | 3 | 5 | 6 | 7 | -10634.6 | 36901.9 | 0.676068 | 0.532067 | 97 | 83574.3 | 97933.8 | 14359.6 | 3 | 5 | 5 | 10 | -10634.6 | 39886.8 | 0.522739 | 0.362964 | 1 | 1 | 30145.6 | -112293 | True | True | True | True | True | False | False |

## Cost Stress Summary

| candidate_id | split | cost_multiplier | gross_pnl_inr | stressed_cost_pnl_drag_inr | stressed_net_pnl_inr | stress_pass |
| --- | --- | --- | --- | --- | --- | --- |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 1.25 | 280316 | 62941.4 | 217375 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 1.5 | 280316 | 75529.6 | 204786 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 1.25 | 420199 | 83955.4 | 336244 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 1.5 | 420199 | 100747 | 319453 | True |
| P231_L5_IMBALANCE_REVERSAL_H3_Q0_9 | test | 1.25 | 131819 | 53202.1 | 78617.1 | True |
| P231_L5_IMBALANCE_REVERSAL_H3_Q0_9 | test | 1.5 | 131819 | 63842.5 | 67976.7 | True |
| P231_L5_IMBALANCE_REVERSAL_H3_Q0_9 | train | 1.25 | 109659 | 57595.6 | 52063 | True |
| P231_L5_IMBALANCE_REVERSAL_H3_Q0_9 | train | 1.5 | 109659 | 69114.7 | 40543.9 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_95 | test | 1.25 | 97933.8 | 17949.4 | 79984.4 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_95 | test | 1.5 | 97933.8 | 21539.3 | 76394.5 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_95 | train | 1.25 | 139137 | 31523.1 | 107614 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_95 | train | 1.5 | 139137 | 37827.7 | 101309 | True |

## Side Flip Controls

| candidate_id | split | side_flip_net_pnl_inr | side_flip_negative_control_pass |
| --- | --- | --- | --- |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | -330669 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | -487363 | True |
| P231_L5_IMBALANCE_REVERSAL_H3_Q0_9 | test | -174381 | True |
| P231_L5_IMBALANCE_REVERSAL_H3_Q0_9 | train | -155735 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_95 | test | -112293 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_95 | train | -164355 | True |

## Random Side Control Sample

| candidate_id | split | control_seed | actual_net_pnl_inr | random_side_net_pnl_inr | actual_beats_random |
| --- | --- | --- | --- | --- | --- |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 1 | 229963 | -28148.4 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 1 | 353035 | -83041 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 2 | 229963 | -119975 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 2 | 353035 | -68452.4 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 3 | 229963 | -34868.9 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 3 | 353035 | -65012.6 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 4 | 229963 | -68928.3 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 4 | 353035 | 44084.2 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 5 | 229963 | -81745.7 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 5 | 353035 | -195413 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 6 | 229963 | 12867.6 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 6 | 353035 | -170998 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 7 | 229963 | -98013.9 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 7 | 353035 | 18948 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 8 | 229963 | -129903 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 8 | 353035 | -18608.7 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 9 | 229963 | -97321.1 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 9 | 353035 | 7924.74 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 10 | 229963 | -38329.7 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 10 | 353035 | -25341.1 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 11 | 229963 | -85725.9 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 11 | 353035 | -40371 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 12 | 229963 | -116788 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 12 | 353035 | -122440 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 13 | 229963 | -47864.4 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 13 | 353035 | -90448.4 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 14 | 229963 | -73610.6 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 14 | 353035 | -46467.9 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | test | 15 | 229963 | -67230.2 | True |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | train | 15 | 353035 | -69403.4 | True |

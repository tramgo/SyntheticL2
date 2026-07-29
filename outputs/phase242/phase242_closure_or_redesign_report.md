# Phase242 Closure / Redesign Decision After One-date Diagnostic

Generated UTC: 2026-07-29T08:09:10.977064+00:00

Phase242 closes the exact Phase237 frozen candidate after the Phase241 one-date unseen diagnostic failed robustness controls.
It opens redesign work that must not tune on the 2026-07-17 holdout and must not consume more disk by downloading dates for the closed candidate.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase242_closure_or_redesign_complete | 1 | Phase242 closure/redesign decision completed |
| phase242_closed_candidate_id | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | Exact candidate closed |
| phase242_one_date_net_pnl_inr | 700.437 | Phase241 net P&L |
| phase242_control_pass_rows | 1 | Phase241 control passes |
| phase242_control_rows | 4 | Phase241 controls |
| phase242_redesign_queue_rows | 3 | Redesign queue rows opened |
| phase242_download_more_dates_for_closed_candidate_allowed | 0 | Do not spend disk on this closed candidate |
| phase242_holdout_parameter_tuning_allowed | 0 | Do not tune on 2026-07-17 |
| phase242_strategy_promotion_allowed | 0 | No strategy promotion from Phase242 |
| phase242_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase242 |
| phase242_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase242 |
| phase242_next_best_action | run_phase243_cost_stress_first_redesign_search_without_2026_07_17_holdout_tuning_no_paper_live | Recommended next milestone |

## Closure Decision

| candidate_id | decision | decision_reason | one_date_net_pnl_inr | control_pass_rows | control_rows | candidate_survived_one_date_diagnostic | download_more_dates_for_this_candidate | reuse_2026_07_17_for_parameter_tuning | paper_or_live_acceptance_allowed | deployable_profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | close_exact_phase237_candidate | positive one-date net P&L did not survive robustness controls | 700.437 | 1 | 4 | 0 | 0 | 0 | 0 | 0 |

## Failure Attribution

| control_id | passed | net_pnl_inr | random_beat_fraction | failure_reason | required_redesign_action |
| --- | --- | --- | --- | --- | --- |
| SIDE_FLIP | 1 | -4406.02 |  | control_passed | retain_as_supporting_evidence_only |
| RANDOM_SIDE_1000_RUNS | 0 | 700.437 | 0.912 | edge_not_strong_enough_against_randomized_direction_control | require stronger directional mechanism before any new holdout use |
| COST_150 | 0 | -225.958 |  | edge_not_robust_to_transaction_cost_stress | redesign for wider expected move or materially lower turnover |
| COST_200 | 0 | -1152.35 |  | edge_not_robust_to_transaction_cost_stress | redesign for wider expected move or materially lower turnover |

## Redesign Queue

| priority | redesign_track | allowed_data | required_change | blocked_action | closed_candidate_id | paper_or_live_acceptance_allowed | deployable_profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | cost_stress_first_signal_search | pre_existing_synthetic_and_discovery_real_anchor_only_not_2026_07_17_tuning | optimize for pass under 1.5x and 2.0x modeled Zerodha cost before any future holdout | do_not_download_more_dates_for_closed_candidate | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | 0 | 0 |
| 2 | random_side_discriminator_strength | training_discovery_sets_only | require random-side beat fraction >=0.95 before reopening a holdout candidate | do_not_adjust_phase237_thresholds_using_2026_07_17 | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | 0 | 0 |
| 3 | lower_turnover_wider_move_hypotheses | synthetic_only_or_existing_discovery_real_anchor | prefer fewer trades with larger expected move and lower cost drag ratio | do_not_claim_profitability_from_positive_one_date_net_pnl | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | 0 | 0 |

## Gate Evaluation

| gate_id | passed | required |
| --- | --- | --- |
| P242_PHASE241_RESULT_PRESENT | 1 | closure decision row exists |
| P242_CANDIDATE_CLOSED | 1 | exact candidate closed |
| P242_HOLDOUT_TUNING_BLOCKED | 1 | 2026-07-17 cannot be used for parameter tuning |
| P242_MORE_DOWNLOADS_FOR_CLOSED_CANDIDATE_BLOCKED | 1 | no additional raw dates for this closed candidate under low disk |
| P242_NO_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | promotion/paper/live/profitability claims closed |

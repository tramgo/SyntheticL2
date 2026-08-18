# Phase473 Interpret Phase472 Costed Failure

Phase473 interprets the Phase472 costed replay failure and precommits the next experiment boundary.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase473_interpret_phase472_costed_failure_complete | 1 | Phase473 interpretation completed |
| phase473_thesis_id | P473_INTERPRET_PHASE472_COSTED_FAILURE | Interpretation thesis |
| phase473_same_phase472_threshold_retune_allowed | 0 | Same-grid threshold rescue is blocked |
| phase473_larger_horizon_experiment_precommitted | 1 | Next experiment must target larger gross move |
| phase473_strategy_promotion_allowed | 0 | No promotion |
| phase473_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase473_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase473_phase474_allowed_next | 1 | Allows Phase474 precommit only if gates pass |
| phase473_hard_gate_pass_rows | 10 | Passed hard gates |
| phase473_hard_gate_rows | 10 | Hard gates |
| phase473_next_best_action | precommit_phase474_larger_horizon_fewer_trade_source_event_l1_l5_experiment | Recommended next action |

## Failure Attribution

| attribution_id | observed_value | comparison_value | verdict | description |
| --- | --- | --- | --- | --- |
| predictive_signal_passed | 0.545578 | 0.53 | passed | Phase471 primary holdout AUC cleared the predictive floor. |
| gross_edge_positive_but_small | 1173.46 | 9322.76 | cost_drag_larger_than_gross_edge | Best primary scenario had positive gross P&L but costs plus slippage were larger. |
| best_primary_net_negative | -8149.31 | 0 | failed | Best primary net P&L was negative after cost200 and Zerodha charges. |
| annualized_profitability_failed | -97.7917 | 12 | failed | Best primary fixed-capital annualized return was below the 12% research profitability bar. |
| same_threshold_grid_not_rescuable | 0 | 1 | closed | No primary threshold in the tested grid produced positive net P&L. |
| phase472_expansion_not_allowed | 0 | 1 | expansion_blocked | Phase472 did not allow direct expansion because profitability gates failed. |

## Next Experiment Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| selected_next_thesis | P474_LARGER_HORIZON_FEWER_TRADE_SOURCE_EVENT_L1_L5 | Seek larger gross moves rather than denser threshold retuning. |
| input_matrix_allowed | outputs/phase470/phase470_source_event_aware_feature_label_matrix.csv | Reuse repaired source-event-aware L1-L5 features. |
| same_phase472_threshold_retune_allowed | 0 | Do not only move thresholds on the same 240-tick horizon replay. |
| required_change_1 | larger_forward_horizon | Increase horizon to target moves large enough to survive costs. |
| required_change_2 | fewer_higher_confidence_events | Reduce turnover by ranking confidence and trading fewer events. |
| required_change_3 | full_depth_l1_l5_required | Keep L1-L5 depth features central to the experiment. |
| required_change_4 | zerodha_cost200_required | Apply Zerodha order-formula charges and cost200 slippage. |
| required_change_5 | fixed_capital_annualization_required | Annualize using fixed reusable capital, not unlimited notional. |
| minimum_profitability_bar_pct | 12 | Research lead profitability floor requested by user. |
| model_retraining_required | 1 | Horizon change requires new labels and a new train/holdout model evaluation. |
| paper_or_live_acceptance_allowed | 0 | No paper/live without expanded synthetic and real-L2 holdout checks. |
| deployable_profitability_claim_allowed | 0 | No deployable claim from this synthetic-only failure interpretation. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P473_PHASE472_REPLAY_COMPLETE | True | 1 | 1 | hard |
| P473_PHASE472_REJECTED_CONFIRMED | True | 0 | 0 | hard |
| P473_COST_DRAG_ATTRIBUTED | True | cost_drag_larger_than_gross_edge | cost_drag_larger_than_gross_edge | hard |
| P473_BEST_PRIMARY_NET_NEGATIVE_CONFIRMED | True | failed | failed | hard |
| P473_12PCT_BAR_FAILED_CONFIRMED | True | failed | failed | hard |
| P473_SAME_THRESHOLD_RETUNE_BLOCKED | True | 0 | 0 | hard |
| P473_LARGER_HORIZON_NEXT_PRECOMMITTED | True | P474_LARGER_HORIZON_FEWER_TRADE_SOURCE_EVENT_L1_L5 | larger_horizon | hard |
| P473_FULL_DEPTH_REQUIRED_NEXT | True | full_depth_l1_l5_required | full_depth_l1_l5_required | hard |
| P473_COST200_REQUIRED_NEXT | True | zerodha_cost200_required | zerodha_cost200_required | hard |
| P473_NO_PAPER_LIVE_OR_CLAIM | True | paper=0;claim=0 | all_zero | hard |

Boundary: this is not a rescue. Same-horizon threshold tuning remains blocked. The next valid path must seek larger gross moves with full-depth L1-L5 and cost200 replay.

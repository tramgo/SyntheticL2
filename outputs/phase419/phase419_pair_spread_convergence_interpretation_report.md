# Phase419 Pair-Spread Convergence Interpretation

Phase419 interprets the positive synthetic Phase418 pair-spread result as a lead, not an accepted strategy.

The result passes breadth and annualized-return gates, but promotion remains blocked because the levels 2-5 removed control outperformed the primary and real-anchor pair evidence is not strong yet.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase419_pair_spread_convergence_interpretation_complete | 1 | Phase419 interpretation completed |
| phase419_selected_verdict | P419_PAIR_SPREAD_CONVERGENCE_POSITIVE_SYNTHETIC_LEAD_NOT_ACCEPTED | Selected verdict |
| phase419_phase418_primary_completed_round_trips | 189 | Primary pair round trips |
| phase419_phase418_primary_positive_date_fraction | 0.8 | Positive date fraction |
| phase419_phase418_primary_net_pnl_inr | 15352.134856071578 | Primary net P&L |
| phase419_phase418_primary_annualized_return_pct | 77.37475967460075 | Primary annualized return |
| phase419_positive_synthetic_lead_preserved | 1 | Keep as lead |
| phase419_strategy_acceptance_allowed | 0 | Blocked by L2-L5 removed control and real-anchor gap |
| phase419_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase419_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase419_hard_gate_pass_rows | 8 | Passed hard gates |
| phase419_hard_gate_rows | 8 | Hard gates |
| phase419_next_best_action | repair_full_depth_contribution_and_real_anchor_pair_evidence_before_any_promotion | Recommended next action |

## Decision Ledger

| decision_id | decision_value | evidence | status |
| --- | --- | --- | --- |
| selected_verdict | P419_PAIR_SPREAD_CONVERGENCE_POSITIVE_SYNTHETIC_LEAD_NOT_ACCEPTED | Positive cost200 synthetic result but failed full-depth contribution gate. | lead_not_acceptance |
| primary_completed_round_trips | 189 | Event floor passed. | positive_lead |
| primary_trade_dates | 5 | Date breadth passed. | positive_lead |
| primary_pairs | 4 | Pair breadth passed. | positive_lead |
| primary_positive_date_fraction | 0.8 | Positive-date gate passed. | positive_lead |
| primary_net_pnl_inr | 15352.134856071578 | Synthetic cost200 net P&L. | positive_lead |
| primary_annualized_return_pct | 77.3748 | Synthetic cost200 annualized return. | positive_lead |
| side_flip_annualized_return_pct | -519.939 | Side-flip control was strongly worse. | supportive_control |
| l2_l5_removed_annualized_return_pct | 98.212 | Levels 2-5 removed control outperformed primary. | blocking_control |
| single_leg_proxy_annualized_return_pct | 38.6874 | Single-leg proxy positive but below primary. | supportive_control |
| phase418_failed_hard_gates | P418_L2_L5_REMOVED_CONTROL | Explicit failed gate basis. | basis |
| full_depth_contribution_proven | 0 | Must be one before acceptance. | blocked |
| real_anchor_pair_evidence_strong | 0 | Real-anchor pair catalog evidence unavailable/zero in bounded run. | blocked |
| strategy_promotion_allowed | 0 | Blocked despite positive synthetic lead. | closed |
| paper_or_live_acceptance_allowed | 0 | No paper/live acceptance. | closed |
| deployable_profitability_claim_allowed | 0 | No deployable claim. | closed |
| next_action | repair_full_depth_contribution_and_real_anchor_pair_evidence_before_any_promotion | Repair contribution/evidence first, not paper/live. | next |

## Required Repairs Before Acceptance

| repair_id | repair_requirement | status |
| --- | --- | --- |
| P420_FULL_DEPTH_CONTRIBUTION_REPAIR | Create a precommitted test where levels 2-5 materially improve or uniquely gate the pair-spread result. | required_before_acceptance |
| P420_REAL_ANCHOR_PAIR_PANEL_REPAIR | Verify whether local/Azure real L2 has matching pair symbols and dates, then run pair replay on real anchors if available. | required_before_acceptance |
| P420_SAME_TIMESTAMP_ALIGNMENT_AUDIT | Audit same-millisecond aligned entry/exit cases and enforce a minimum forward-tick or elapsed-time rule if needed. | required_before_acceptance |
| P420_COST100_COST200_RANK_AUDIT | Record whether the positive lead remains ranked under cost100/cost200 without weakening acceptance. | required_before_acceptance |
| P420_NO_PAPER_LIVE_BOUNDARY | No paper/live until contribution, real-anchor and timing realism repairs pass. | closed_boundary |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P419_PHASE418_COMPLETE | True | 1 | 1 | hard |
| P419_PHASE418_GATES_EVALUATED | True | 21 | 21 | hard |
| P419_POSITIVE_SYNTHETIC_LEAD_CONFIRMED | True | annualized=77.37475967460075;survivors=3 | annualized>=12;survivors>0 | hard |
| P419_FAILED_GATE_BASIS_PRESENT | True | P418_L2_L5_REMOVED_CONTROL | nonempty | hard |
| P419_FULL_DEPTH_CONTRIBUTION_BLOCKER_RECORDED | True | 0 | 0 | hard |
| P419_REAL_ANCHOR_BLOCKER_RECORDED | True | 0 | 0 | hard |
| P419_VERDICT_PRESENT | True | P419_PAIR_SPREAD_CONVERGENCE_POSITIVE_SYNTHETIC_LEAD_NOT_ACCEPTED | P419_PAIR_SPREAD_CONVERGENCE_POSITIVE_SYNTHETIC_LEAD_NOT_ACCEPTED | hard |
| P419_NO_PROMOTION_OR_PAPER_LIVE | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: positive synthetic lead does not mean paper/live acceptance.

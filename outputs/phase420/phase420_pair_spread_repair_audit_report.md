# Phase420 Pair-Spread Repair Audit

Phase420 audits the Phase418/419 positive pair-spread lead before any acceptance or promotion.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase420_pair_spread_repair_audit_complete | 1 | Phase420 audit completed |
| phase420_selected_verdict | P420_PAIR_SPREAD_REPAIR_AUDIT_BLOCKED_ACCEPTANCE_BUT_LEAD_SURVIVES | Selected verdict |
| phase420_phase418_positive_lead_preserved | 1 | Positive lead still preserved |
| phase420_acceptance_allowed | 0 | Blocked |
| phase420_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase420_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase420_hard_gate_pass_rows | 9 | Passed hard gates |
| phase420_hard_gate_rows | 9 | Hard gates |
| phase420_next_best_action | precommit_phase421_pair_spread_realism_retest_with_min_forward_time_and_full_depth_unique_gate | Recommended next action |

## Full-Depth Contribution Audit

| audit_id | value | description |
| --- | --- | --- |
| primary_annualized_return_pct | 77.3748 | Phase418 primary |
| l2_l5_removed_annualized_return_pct | 98.212 | Levels 2-5 removed control |
| single_leg_proxy_annualized_return_pct | 38.6874 | Single-leg proxy control |
| primary_minus_l2_l5_removed_pct | -20.8372 | Must be positive before full-depth contribution is accepted |
| primary_minus_single_leg_proxy_pct | 38.6874 | Pair must beat single-leg proxy |
| full_depth_contribution_pass | 0 | Observed primary greater than L2-L5 removed control |
| pair_structure_beats_proxy | 1 | Observed primary greater than single-leg proxy |

## Timing Realism Audit

| audit_id | value | description |
| --- | --- | --- |
| trade_rows | 189 | Primary trade rows |
| same_timestamp_entry_exit_rows | 80 | entry_ts_ms >= exit_ts_ms due aligned synthetic ticks |
| same_timestamp_share | 0.42328 | same timestamp rows / trades |
| median_hold_ms | 1 | median exit-entry ms |
| p10_hold_ms | 0 | 10th percentile hold ms |
| p90_hold_ms | 2 | 90th percentile hold ms |
| timing_realism_pass | 0 | Requires same timestamp share <= 0.05 |

## Real-Anchor Pair Availability

| pair_id | leg_a | leg_b | leg_a_dates | leg_b_dates | overlap_dates | overlap_date_list | real_anchor_pair_available |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HDFCBANK_ICICIBANK | HDFCBANK | ICICIBANK | 16 | 16 | 16 | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14;2026-07-15;2026-07-16;2026-07-17;2026-07-20;2026-07-21;2026-07-22;2026-07-23;2026-07-24;2026-07-27;2026-08-03;2026-08-04 | 1 |
| HDFCBANK_AXISBANK | HDFCBANK | AXISBANK | 16 | 16 | 16 | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14;2026-07-15;2026-07-16;2026-07-17;2026-07-20;2026-07-21;2026-07-22;2026-07-23;2026-07-24;2026-07-27;2026-08-03;2026-08-04 | 1 |
| INFY_TCS | INFY | TCS | 16 | 16 | 16 | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14;2026-07-15;2026-07-16;2026-07-17;2026-07-20;2026-07-21;2026-07-22;2026-07-23;2026-07-24;2026-07-27;2026-08-03;2026-08-04 | 1 |
| RELIANCE_ONGC | RELIANCE | ONGC | 16 | 16 | 16 | 2026-07-08;2026-07-09;2026-07-10;2026-07-13;2026-07-14;2026-07-15;2026-07-16;2026-07-17;2026-07-20;2026-07-21;2026-07-22;2026-07-23;2026-07-24;2026-07-27;2026-08-03;2026-08-04 | 1 |

## Cost Rank Audit

| scenario_id | net_pnl_cost100_inr | net_pnl_cost200_inr | cost100_rank | cost200_rank |
| --- | --- | --- | --- | --- |
| P418_L2_L5_REMOVED_CONTROL | 44491.4 | 19486.5 | 1 | 1 |
| P418_PRIMARY_PAIR_SPREAD_CONVERGENCE | 35015.7 | 15352.1 | 2 | 2 |
| P418_SINGLE_LEG_PROXY_CONTROL | 17507.8 | 7676.07 | 3 | 3 |
| P418_SIDE_FLIP_CONTROL | -83496.5 | -103163 | 4 | 4 |

## Decision Ledger

| decision_id | decision_value | evidence | status |
| --- | --- | --- | --- |
| selected_verdict | P420_PAIR_SPREAD_REPAIR_AUDIT_BLOCKED_ACCEPTANCE_BUT_LEAD_SURVIVES | Positive lead remains but acceptance blockers persist. | lead_not_acceptance |
| full_depth_contribution_pass | 0 | Primary must beat L2-L5 removed control. | blocker |
| timing_realism_pass | 0 | Same-timestamp entry/exit share must be low. | blocker |
| real_anchor_pair_available_count | 4 | Matching real-anchor pair-date availability. | available |
| primary_cost200_rank | 2 | Rank among Phase418 scenarios at cost200. | diagnostic |
| acceptance_allowed | 0 | Blocked until full-depth/timing/real-anchor repairs pass. | closed |
| paper_or_live_acceptance_allowed | 0 | No paper/live. | closed |
| deployable_profitability_claim_allowed | 0 | No deployable claim. | closed |
| next_action | precommit_phase421_pair_spread_realism_retest_with_min_forward_time_and_full_depth_unique_gate | Retest lead with full-depth unique gate and minimum forward time. | next |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P420_PHASE419_COMPLETE | True | 1 | 1 | hard |
| P420_FULL_DEPTH_AUDIT_WRITTEN | True | 7 | >0 | hard |
| P420_TIMING_AUDIT_WRITTEN | True | 7 | >0 | hard |
| P420_COST_RANK_AUDIT_WRITTEN | True | written | written | hard |
| P420_REAL_ANCHOR_AVAILABILITY_WRITTEN | True | 4 | >0 | hard |
| P420_FULL_DEPTH_BLOCKER_RECORDED | True | 0 | 0 | hard |
| P420_TIMING_BLOCKER_RECORDED | True | 0 | 0 | hard |
| P420_REAL_ANCHOR_STATUS_RECORDED | True | 4 | >=0 | hard |
| P420_NO_ACCEPTANCE_OR_PAPER_LIVE | True | acceptance=0;paper=0;claim=0 | all_zero | hard |

Boundary: positive synthetic lead remains blocked for acceptance.

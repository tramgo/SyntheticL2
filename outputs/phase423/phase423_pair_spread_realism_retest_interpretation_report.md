# Phase423 Pair-Spread Realism Retest Interpretation

Phase423 formally interprets Phase422: the Phase418 positive pair-spread lead is falsified by the precommitted realism retest.

The synthetic lead depended on same-timestamp or too-fast exits. After the 250 ms forward-time filter, synthetic primary trades fell to zero. The real-anchor pair replay was active, but it was negative after Zerodha cost200.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase423_pair_spread_realism_retest_interpretation_complete | 1 | Phase423 interpretation completed |
| phase423_selected_verdict | P423_PAIR_SPREAD_POSITIVE_LEAD_FALSIFIED_BY_REALISM_RETEST | Selected verdict |
| phase423_phase422_primary_completed_round_trips | 0 | Phase422 synthetic primary round trips |
| phase423_phase422_primary_annualized_return_pct | 0.0 | Phase422 synthetic primary annualized return |
| phase423_phase422_hard_gate_pass_rows | 10 | Phase422 hard gates passed |
| phase423_phase422_hard_gate_rows | 17 | Phase422 hard gates |
| phase423_pair_spread_positive_lead_preserved | 0 | Lead is falsified for this route |
| phase423_same_family_tuning_allowed | 0 | No same-family tuning |
| phase423_strategy_promotion_allowed | 0 | No promotion |
| phase423_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase423_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase423_hard_gate_pass_rows | 9 | Passed hard gates |
| phase423_hard_gate_rows | 9 | Hard gates |
| phase423_next_best_action | stop_pair_spread_convergence_route_or_precommit_material_new_full_depth_source | Recommended next action |

## Decision Ledger

| decision_id | decision_value | evidence | status |
| --- | --- | --- | --- |
| selected_verdict | P423_PAIR_SPREAD_POSITIVE_LEAD_FALSIFIED_BY_REALISM_RETEST | Phase418 positive synthetic lead did not survive the precommitted Phase421 realism retest. | terminal_for_this_route |
| phase422_next_action_matched | interpret_phase422_pair_spread_realism_retest_no_paper_live | Phase423 implements the Phase422 next-action string. | basis |
| synthetic_raw_selections_before_forward_filter | 807 | Synthetic signal opportunities existed before realism filtering. | evidence |
| synthetic_selections_after_forward_filter | 0 | No synthetic trades survived the 250 ms forward-time filter. | falsification |
| synthetic_primary_completed_round_trips | 0 | Synthetic primary after realism filter. | falsification |
| synthetic_primary_annualized_return_pct | 0.0 | Annualized return uses fixed INR 1,000,000 capital. | falsification |
| full_depth_unique_gate_passed | 0 | Full-depth L2-L5 edge did not beat the removed-depth control by the required margin. | falsification |
| forward_tick_exact_gate_passed | 0 | Exact post-entry aligned tick indexing was not available, so the tick-count rule remains failed/proxy-only. | caveat |
| real_anchor_raw_selections_before_forward_filter | 606 | Real-anchor pair panel was active. | real_anchor |
| real_anchor_selections_after_forward_filter | 593 | Real-anchor trades survived timing filter. | real_anchor |
| real_anchor_primary_completed_round_trips | 139 | Real-anchor primary completed round trips. | real_anchor_negative |
| real_anchor_primary_trade_dates | 5 | Real-anchor date breadth. | real_anchor_negative |
| real_anchor_primary_pairs | 4 | Real-anchor pair breadth. | real_anchor_negative |
| real_anchor_primary_net_pnl_inr | -31111.8 | Real-anchor cost200 net P&L. | real_anchor_negative |
| real_anchor_primary_annualized_return_pct | -156.803 | Real-anchor fixed-capital annualized return. | real_anchor_negative |
| same_family_tuning_allowed | 0 | Do not tune the same pair-spread convergence route after realism falsification. | closed |
| strategy_promotion_allowed | 0 | No accepted survivor. | closed |
| paper_or_live_acceptance_allowed | 0 | No paper/live acceptance. | closed |
| deployable_profitability_claim_allowed | 0 | No deployable claim. | closed |
| next_action | stop_pair_spread_convergence_route_or_precommit_material_new_full_depth_source | Move to a materially new full-depth source if strategy search continues. | next |

## Durable Byproducts

| artifact_id | description | status |
| --- | --- | --- |
| pair_alignment_panel | Pair tick alignment across synthetic and real-anchor panels remains reusable. | preserve |
| real_anchor_pair_loader | Local real L2 loader normalizes symbol/trade_date metadata and top-five depth fields. | preserve |
| zerodha_cost200_pair_ledger | Both synthetic and real-anchor ledgers retain gross, cost100, cost200 and net P&L. | preserve |
| forward_time_filter | Minimum 250 ms forward-time realism filter is reusable. | preserve |
| forward_tick_index_repair | Exact post-entry aligned tick count was not implemented in Phase422 and should be added before any future tick-count gate is claimed. | required_if_reused |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P423_PHASE422_COMPLETE | True | 1 | 1 | hard |
| P423_PHASE422_GATES_EVALUATED | True | 17 | 17 | hard |
| P423_PHASE422_FAILED_GATES_PRESENT | True | passed=10/17;failed=P422_FORWARD_TICKS_ENFORCED;P422_FULL_DEPTH_UNIQUE_GATE;P422_EVENT_FLOOR;P422_DATE_BREADTH;P422_PAIR_BREADTH;P422_POSITIVE_DATE_FRACTION;P422_ANNUALIZED_FLOOR | failed_gates_nonempty | hard |
| P423_SYNTHETIC_LEAD_ELIMINATED_BY_REALISM | True | trips=0;annualized=0.0 | zero_trades_after_forward_filter | hard |
| P423_REAL_ANCHOR_NEGATIVE_CONFIRMED | True | -156.803 | <0 | hard |
| P423_FULL_DEPTH_UNIQUE_FAILURE_RECORDED | True | P422_FORWARD_TICKS_ENFORCED;P422_FULL_DEPTH_UNIQUE_GATE;P422_EVENT_FLOOR;P422_DATE_BREADTH;P422_PAIR_BREADTH;P422_POSITIVE_DATE_FRACTION;P422_ANNUALIZED_FLOOR | contains_full_depth_gate | hard |
| P423_VERDICT_PRESENT | True | P423_PAIR_SPREAD_POSITIVE_LEAD_FALSIFIED_BY_REALISM_RETEST | P423_PAIR_SPREAD_POSITIVE_LEAD_FALSIFIED_BY_REALISM_RETEST | hard |
| P423_NO_SAME_FAMILY_TUNING | True | 0 | 0 | hard |
| P423_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: the pair-spread convergence route is closed for acceptance. Continue only with a materially new full-depth L2 source or thesis.

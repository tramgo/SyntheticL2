# Phase382 Interpret Phase381 Retest

Generated: 2026-08-11T19:57:11.489475+00:00

Phase382 interprets the expanded real-L2 frozen reversal retest. The primary is profitable and beats the side-flip control, but it is not accepted because the actual capacity-selected event count remains below the 30-trade floor.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase382_interpret_phase381_retest_complete | 1 | Phase382 complete |
| phase382_primary_annualized_return_pct | 25.6896 | Primary annualized return |
| phase382_primary_selected_trade_rows | 19 | Primary capacity-selected trades |
| phase382_event_floor_required | 30 | Required selected trades |
| phase382_event_floor_gap | 11 | Remaining selected-trade gap |
| phase382_profitability_gate_met | 1 | Annualized return > 12% |
| phase382_event_floor_met | 0 | Selected-trade floor met |
| phase382_breadth_met | 1 | Breadth met |
| phase382_side_flip_control_passed | 1 | Primary beats continuation control |
| phase382_acceptance_candidate | 0 | Acceptance candidate |
| phase382_strategy_promotion_allowed | 0 | No promotion |
| phase382_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase382_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase382_hard_gate_pass_rows | 6 | Passed gates |
| phase382_hard_gate_rows | 6 | Gates |
| phase382_next_best_action | precommit_event_density_repair_or_new_material_thesis_no_paper_live | Recommended next action |

## Decision ledger

| decision_id | value | evidence | decision |
| --- | --- | --- | --- |
| P382_PROFITABILITY_DIAGNOSTIC_POSITIVE | 1 | primary_annualized_return_pct=25.68958992557929; threshold=12.0 | The frozen primary remains economically positive after expanding real L2 evidence. |
| P382_EVENT_FLOOR_FAILS | 1 | selected_trades=19; required=30; gap=11 | The retest is still too sparse for acceptance. |
| P382_BREADTH_PASSES | 1 | breadth_met=1 | Breadth is not the blocker in this retest. |
| P382_SIDE_FLIP_CONTROL_PASSES | 1 | primary_ann=25.68958992557929; side_flip_ann=-93.55244161582728 | The reversal direction dominates the same-filter continuation control. |
| P382_NO_ACCEPTANCE_OR_PROMOTION | 1 | acceptance_candidate=0 | Do not promote, paper trade, or claim deployable profitability. |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P382_PHASE381_COMPLETE | 1 | Phase381 complete |
| P382_PROFITABILITY_GATE_CHECKED | 1 | ann=25.690; pass=1 |
| P382_EVENT_FLOOR_GATE_CHECKED | 1 | selected=19; required=30; pass=0 |
| P382_BREADTH_GATE_CHECKED | 1 | breadth=1 |
| P382_CONTROL_GATE_CHECKED | 1 | side_flip_ann=-93.552 |
| P382_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.

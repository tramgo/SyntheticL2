# Phase388 Interpret Phase387 Retest

Generated: 2026-08-11T20:42:44.866568+00:00

| metric | value | description |
| --- | --- | --- |
| phase388_interpret_phase387_retest_complete | 1 | Phase388 complete |
| phase388_primary_annualized_return_pct | 12.566 | Primary annualized return |
| phase388_primary_net_pnl_inr | 1620.62 | Primary net PnL |
| phase388_primary_scheduled_candidates | 32 | Raw scheduled candidates |
| phase388_primary_capacity_selected_trades | 23 | Capacity-selected trades |
| phase388_capacity_selected_gap | 7 | Capacity-selected gap |
| phase388_no_start_tick_rows | 3 | No-start rows |
| phase388_event_floor_met | 0 | Selected-trade floor met |
| phase388_breadth_met | 1 | Breadth met |
| phase388_acceptance_candidate | 0 | Acceptance candidate |
| phase388_side_flip_annualized_return_pct | -82.0301 | Side-flip annualized return |
| phase388_strategy_promotion_allowed | 0 | No promotion |
| phase388_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase388_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase388_next_best_action | precommit_capacity_rule_sensitivity_or_add_more_real_l2_no_paper_live | Recommended next action |

| decision_id | value | evidence | decision |
| --- | --- | --- | --- |
| P388_PROFITABILITY_STILL_POSITIVE | 1 | ann=12.566037902421556; net=1620.6199675742087 | Frozen reversal remains profitable after the Phase384 density repair. |
| P388_RAW_CANDIDATE_FLOOR_REACHED | 1 | scheduled_candidates=32; required=30 | Raw filtered candidates now reach the event floor. |
| P388_CAPACITY_SELECTED_FLOOR_FAILS | 1 | capacity_selected=23; required=30; gap=7 | Capacity selection remains the acceptance blocker. |
| P388_SHORT_DAY_EFFECT_RECORDED | 1 | no_start_tick_rows=3 | The short 2026-07-27 collector window produced some non-ready event rows. |
| P388_NO_ACCEPTANCE_OR_PROMOTION | 1 | acceptance_candidate=0; breadth=1; side_flip_ann=-82.03012519492701 | No promotion, paper/live action, or deployable profitability claim. |

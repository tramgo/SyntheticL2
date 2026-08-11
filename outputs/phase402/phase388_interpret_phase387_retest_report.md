# Phase388 Interpret Phase387 Retest

Generated: 2026-08-11T21:08:17.812058+00:00

| metric | value | description |
| --- | --- | --- |
| phase388_interpret_phase387_retest_complete | 1 | Phase388 complete |
| phase388_primary_annualized_return_pct | 7.14935 | Primary annualized return |
| phase388_primary_net_pnl_inr | 992.965 | Primary net PnL |
| phase388_primary_scheduled_candidates | 34 | Raw scheduled candidates |
| phase388_primary_capacity_selected_trades | 25 | Capacity-selected trades |
| phase388_capacity_selected_gap | 5 | Capacity-selected gap |
| phase388_no_start_tick_rows | 3 | No-start rows |
| phase388_event_floor_met | 0 | Selected-trade floor met |
| phase388_breadth_met | 1 | Breadth met |
| phase388_acceptance_candidate | 0 | Acceptance candidate |
| phase388_side_flip_annualized_return_pct | -77.2339 | Side-flip annualized return |
| phase388_strategy_promotion_allowed | 0 | No promotion |
| phase388_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase388_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase388_next_best_action | precommit_capacity_rule_sensitivity_or_add_more_real_l2_no_paper_live | Recommended next action |

| decision_id | value | evidence | decision |
| --- | --- | --- | --- |
| P388_PROFITABILITY_STILL_POSITIVE | 0 | ann=7.149347884879218; net=992.9649840110026 | Frozen reversal remains profitable after the Phase384 density repair. |
| P388_RAW_CANDIDATE_FLOOR_REACHED | 1 | scheduled_candidates=34; required=30 | Raw filtered candidates now reach the event floor. |
| P388_CAPACITY_SELECTED_FLOOR_FAILS | 1 | capacity_selected=25; required=30; gap=5 | Capacity selection remains the acceptance blocker. |
| P388_SHORT_DAY_EFFECT_RECORDED | 1 | no_start_tick_rows=3 | The short 2026-07-27 collector window produced some non-ready event rows. |
| P388_NO_ACCEPTANCE_OR_PROMOTION | 1 | acceptance_candidate=0; breadth=1; side_flip_ann=-77.233854814144 | No promotion, paper/live action, or deployable profitability claim. |

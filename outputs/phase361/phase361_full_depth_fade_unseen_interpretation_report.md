# Phase361 Full-Depth Fade Unseen Interpretation

Generated: 2026-08-11T15:37:39.030670+00:00

Phase361 interprets the Phase360 unseen real-L2 result for the Phase357/358 full-depth market-neutral fade family. It is a branch decision, not a new search.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase361_full_depth_fade_unseen_interpretation_complete | 1 | Phase361 interpretation completed |
| phase361_phase360_unseen_net_pnl_inr | -939.536 | Phase360 primary unseen net PnL |
| phase361_phase360_unseen_annualized_return_pct | -47.3526 | Phase360 primary unseen annualized return |
| phase361_combined_trade_rows | 17 | Phase356 + Phase360 trades |
| phase361_combined_diagnostic_dates | 9 | Phase356 + Phase360 dates |
| phase361_combined_net_pnl_inr | 882.355 | Combined net PnL |
| phase361_combined_annualized_return_pct | 9.88238 | Combined annualized return |
| phase361_combined_above12 | 0 | Combined above 12% |
| phase361_combined_event_floor_met | 0 | Combined event floor met |
| phase361_acceptance_candidate_rows | 0 | Combined acceptance candidates |
| phase361_branch_closed_for_acceptance | 1 | Full-depth market-neutral fade closed for acceptance under current evidence |
| phase361_parameter_rescue_allowed | 0 | No same-family parameter rescue |
| phase361_additional_real_date_falsification_allowed | 1 | More real dates may be used for falsification evidence |
| phase361_materially_new_thesis_allowed | 1 | A materially different thesis may be precommitted |
| phase361_strategy_promotion_allowed | 0 | No promotion |
| phase361_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase361_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase361_hard_gate_pass_rows | 8 | Passed hard gates |
| phase361_hard_gate_rows | 8 | Hard gates |
| phase361_next_best_action | precommit_materially_new_real_l2_thesis_or_expand_real_dates_for_falsification_no_paper_live | Recommended next milestone |

## Combined read-through

| readthrough_id | phase356_primary_trades | phase356_primary_dates | phase356_primary_net_pnl_inr | phase356_primary_annualized_return_pct | phase360_unseen_trades | phase360_unseen_dates | phase360_unseen_net_pnl_inr | phase360_unseen_annualized_return_pct | combined_trades | combined_dates | combined_net_pnl_inr | combined_annualized_return_pct | combined_above12 | combined_event_floor_met | combined_acceptance_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase356_training_plus_phase360_unseen | 12 | 7 | 1821.89 | 26.2352 | 5 | 2 | -939.536 | -47.3526 | 17 | 9 | 882.355 | 9.88238 | 0 | 0 | 0 |

## Interpretation

| interpretation_id | value | evidence | decision |
| --- | --- | --- | --- |
| unseen_failure | 1 | net=-939.5364392427646; annualized=-47.35263653783534 | Phase358 positive clue did not survive first unseen local real-L2 expansion. |
| combined_below_threshold | 1 | combined_annualized=9.882375164637406; threshold=12.0 | Combined read-through is not profitable by the user's 12% annualized bar. |
| combined_event_floor_failed | 1 | combined_trades=17; required=30 | Even after unseen expansion, event count is below acceptance floor. |
| no_acceptance_survivor | 1 | phase360_acceptance_candidate_rows=0 | No replay, paper/live, promotion or deployable profitability claim is allowed. |

## Branch decision

| decision_id | decision | reason | parameter_rescue_allowed | additional_same_family_filter_rescue_allowed | additional_real_date_falsification_allowed | materially_new_thesis_allowed | paper_live_or_profit_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P361_CLOSE_FULL_DEPTH_MARKET_NEUTRAL_FADE_FOR_ACCEPTANCE | close_for_acceptance_under_current_real_l2_evidence | The sparse Phase358 positive clue failed on unseen real L2 and the combined read-through is below the 12% threshold and below the 30-event floor. | 0 | 0 | 1 | 1 | 0 |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P361_PHASE358_PRESENT | 1 | Phase358 summary present |
| P361_PHASE359_PRESENT | 1 | Phase359 summary present |
| P361_PHASE360_PRESENT | 1 | Phase360 summary present |
| P361_UNSEEN_FAILURE_RECORDED | 1 | phase360_ann=-47.35263653783534 |
| P361_COMBINED_READTHROUGH_BELOW12_RECORDED | 1 | combined_ann=9.882375164637406 |
| P361_EVENT_FLOOR_RECHECKED | 1 | combined_trades=17 |
| P361_PARAMETER_RESCUE_FORBIDDEN | 1 | same-family parameter/filter rescue closed |
| P361_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.

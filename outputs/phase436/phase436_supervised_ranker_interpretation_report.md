# Phase436 Supervised Ranker Interpretation

Phase436 formally interprets Phase435 as a negative execution result.

The supervised full-depth event ranker was materially new and generated enough validation trades to test execution costs, but it did not produce a profitable cost200 strategy and failed important controls.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase436_supervised_ranker_interpretation_complete | 1 | Phase436 interpretation completed |
| phase436_selected_verdict | P436_SUPERVISED_FULL_DEPTH_EVENT_RANKER_REJECTED_COST_DOMINATED | Selected verdict |
| phase436_phase435_best_completed_round_trips | 32 | Phase435 primary round trips |
| phase436_phase435_best_annualized_return_pct | -130.2218249756231 | Phase435 primary annualized return |
| phase436_phase435_acceptance_survivors | 0 | Phase435 cost200 survivors |
| phase436_strategy_promotion_allowed | 0 | No promotion |
| phase436_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase436_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase436_same_source_rescue_allowed | 0 | No same-source rescue |
| phase436_hard_gate_pass_rows | 8 | Passed hard gates |
| phase436_hard_gate_rows | 8 | Hard gates |
| phase436_next_best_action | precommit_material_new_lower_turnover_horizon_or_pause_strategy_search | Recommended next action |

## Decision Ledger

| decision_id | decision_value | evidence | status |
| --- | --- | --- | --- |
| selected_verdict | P436_SUPERVISED_FULL_DEPTH_EVENT_RANKER_REJECTED_COST_DOMINATED | The materially new supervised full-depth event ranker produced enough events to test but failed cost200 profitability and controls. | terminal_for_this_source_form |
| phase435_next_action_matched | interpret_phase435_supervised_full_depth_event_ranker_no_paper_live | Phase436 implements the Phase435 next-action string. | basis |
| synthetic_event_rows | 960 | Synthetic event-label rows used by Phase435. | evidence |
| primary_round_trips | 32 | Primary selected validation trades. | evidence |
| primary_trade_dates | 1 | Validation date breadth. | failure |
| primary_symbols | 4 | Validation symbol breadth. | failure |
| primary_gross_pnl_inr | 76.56 | Gross edge before costs. | evidence |
| primary_cost200_inr | 5244.09 | Zerodha cost200 charges. | failure |
| primary_net_pnl_inr | -5167.53 | Net P&L after cost200. | failure |
| primary_annualized_return_pct | -130.222 | Failed annualized floor. | failure |
| l1_only_annualized_return_pct | -130.82 | L1-only ablation nearly matched primary. | control_failure |
| time_shuffle_annualized_return_pct | -64.478 | Time-shuffle control was less negative than primary. | control_failure |
| real_anchor_annualized_return_pct | -224.917 | Real-anchor cross-check preserved negative sign. | evidence |
| phase435_failed_hard_gates | P435_L2_L5_MATERIALITY_OVER_L1;P435_TIME_SHUFFLE_CONTROL_NOT_DOMINANT;P435_DATE_BREADTH;P435_SYMBOL_BREADTH;P435_POSITIVE_DATE_FRACTION;P435_ANNUALIZED_FLOOR | Explicit failed gate basis. | basis |
| strategy_promotion_allowed | 0 | No accepted survivor. | closed |
| paper_or_live_acceptance_allowed | 0 | No paper/live acceptance. | closed |
| deployable_profitability_claim_allowed | 0 | No deployable claim. | closed |
| same_source_rescue_allowed | 0 | Do not retune this same ranker after seeing validation/control failures. | closed |
| next_action | precommit_material_new_lower_turnover_horizon_or_pause_strategy_search | Move only to a materially lower-turnover/longer-horizon source, or pause strategy search. | next |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P436_PHASE435_COMPLETE | True | 1 | 1 | hard |
| P436_PHASE435_GATES_EVALUATED | True | 14 | 14 | hard |
| P436_PHASE435_FAILED_GATES_PRESENT | True | passed=8/14;failed=P435_L2_L5_MATERIALITY_OVER_L1;P435_TIME_SHUFFLE_CONTROL_NOT_DOMINANT;P435_DATE_BREADTH;P435_SYMBOL_BREADTH;P435_POSITIVE_DATE_FRACTION;P435_ANNUALIZED_FLOOR | failed_gates_nonempty | hard |
| P436_NO_ACCEPTANCE_SURVIVOR_CONFIRMED | True | 0 | 0 | hard |
| P436_NEGATIVE_COST200_CONFIRMED | True | -130.222 | <0 | hard |
| P436_VERDICT_PRESENT | True | P436_SUPERVISED_FULL_DEPTH_EVENT_RANKER_REJECTED_COST_DOMINATED | P436_SUPERVISED_FULL_DEPTH_EVENT_RANKER_REJECTED_COST_DOMINATED | hard |
| P436_NO_SAME_SOURCE_RESCUE | True | 0 | 0 | hard |
| P436_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: do not rescue the same supervised ranker by retuning after seeing the validation result. If strategy search continues, precommit a materially lower-turnover or longer-horizon source before execution.

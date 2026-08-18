# Phase416 Deep-Book Divergence Snapback Interpretation

Phase416 formally interprets the non-sparse but negative Phase415 result.

The route is rejected for acceptance: it generated enough trades and breadth, but every date was non-positive and annualized return was deeply negative after cost200.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase416_deep_book_divergence_snapback_interpretation_complete | 1 | Phase416 interpretation completed |
| phase416_selected_verdict | P416_DEEP_BOOK_DIVERGENCE_SNAPBACK_REJECTED_NON_SPARSE_NEGATIVE | Selected verdict |
| phase416_phase415_primary_completed_round_trips | 238 | Primary round trips |
| phase416_phase415_primary_positive_date_fraction | 0.0 | Primary positive date fraction |
| phase416_phase415_primary_net_pnl_inr | -83261.78122609416 | Primary net P&L |
| phase416_phase415_primary_annualized_return_pct | -419.6393773795146 | Primary annualized return |
| phase416_cost200_acceptance_survivor_rows | 0 | Acceptance survivors |
| phase416_same_family_tuning_allowed | 0 | No same-family tuning |
| phase416_strategy_promotion_allowed | 0 | No promotion |
| phase416_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase416_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase416_hard_gate_pass_rows | 8 | Passed hard gates |
| phase416_hard_gate_rows | 8 | Hard gates |
| phase416_next_best_action | stop_deep_book_divergence_snapback_route_or_precommit_material_new_non_directional_full_depth_source | Recommended next action |

## Decision Ledger

| decision_id | decision_value | evidence | status |
| --- | --- | --- | --- |
| selected_verdict | P416_DEEP_BOOK_DIVERGENCE_SNAPBACK_REJECTED_NON_SPARSE_NEGATIVE | Enough events/breadth, but negative cost200 result. | terminal_for_this_route |
| primary_completed_round_trips | 238 | Event floor passed. | non_sparse |
| primary_trade_dates | 5 | Date breadth passed. | non_sparse |
| primary_symbols | 3 | Symbol breadth passed. | non_sparse |
| primary_positive_date_fraction | 0 | Failed positive-date fraction. | failure |
| primary_net_pnl_inr | -83261.8 | Net P&L after cost200. | failure |
| primary_annualized_return_pct | -419.639 | Failed annualized floor. | failure |
| cost200_acceptance_survivor_rows | 0 | No accepted scenario. | failure |
| phase415_failed_hard_gates | P415_POSITIVE_DATE_FRACTION;P415_ANNUALIZED_FLOOR;P415_SIDE_FLIP_CONTROL | Explicit failed gate basis. | basis |
| same_family_tuning_allowed | 0 | Do not tune this route after broad negative evidence. | closed |
| strategy_promotion_allowed | 0 | No accepted survivor. | closed |
| paper_or_live_acceptance_allowed | 0 | No paper/live acceptance. | closed |
| deployable_profitability_claim_allowed | 0 | No deployable claim. | closed |
| next_action | stop_deep_book_divergence_snapback_route_or_precommit_material_new_non_directional_full_depth_source | Move away from this directional snapback route. | next |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P416_PHASE415_COMPLETE | True | 1 | 1 | hard |
| P416_PHASE415_GATES_EVALUATED | True | 21 | 21 | hard |
| P416_NON_SPARSE_EVENT_EVIDENCE | True | trips=238;dates=5;symbols=3 | event_date_symbol_breadth | hard |
| P416_NEGATIVE_COST200_CONFIRMED | True | -419.639 | <0 | hard |
| P416_NO_COST200_SURVIVORS | True | 0 | 0 | hard |
| P416_VERDICT_PRESENT | True | P416_DEEP_BOOK_DIVERGENCE_SNAPBACK_REJECTED_NON_SPARSE_NEGATIVE | P416_DEEP_BOOK_DIVERGENCE_SNAPBACK_REJECTED_NON_SPARSE_NEGATIVE | hard |
| P416_NO_SAME_FAMILY_TUNING | True | 0 | 0 | hard |
| P416_BOUNDARIES_CLOSED | True | promotion=0;paper=0;claim=0 | all_zero | hard |

Boundary: do not tune the same deep-book divergence snapback route after this negative result.

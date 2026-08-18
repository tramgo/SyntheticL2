# Phase483 Interpret Real-L2 Capacity Candidate

Phase483 interprets the Phase482 max5 concurrent capital-feasible candidate before any acceptance or paper/live claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase483_interpret_real_l2_capacity_candidate_complete | 1 | Phase483 complete if all interpretation-process gates pass |
| phase483_thesis_id | P483_INTERPRET_REAL_L2_CAPACITY_CANDIDATE | Phase483 thesis |
| phase483_selected_policy | P481_BASELINE_MAX2_CONCURRENT | Selected Phase482 policy |
| phase483_selected_verdict | P483_CAPACITY_CANDIDATE_REJECTED_BY_CONCENTRATION_AND_DATE_ROBUSTNESS | Selected verdict |
| phase483_selected_trades | 25 | Selected primary trades |
| phase483_net_pnl_inr | 992.965 | Selected primary net PnL |
| phase483_positive_date_fraction | 0.357143 | Positive-date fraction |
| phase483_top_date_net_share | 3.79503 | Top date net contribution share |
| phase483_top_symbol_net_share | 3.26075 | Top symbol net contribution share |
| phase483_research_candidate_allowed | 0 | Can advance only to independent holdout precommit |
| phase483_strategy_promotion_allowed | 0 | No promotion |
| phase483_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase483_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase483_hard_gate_pass_rows | 10 | Passed hard gates |
| phase483_hard_gate_rows | 10 | Hard gates |
| phase483_next_best_action | stop_acceptance_for_phase482_candidate_or_require_materially_new_real_l2_signal_no_paper_live | Recommended next action |

## Diagnostics

| diagnostic_id | value | description |
| --- | --- | --- |
| selected_policy | P481_BASELINE_MAX2_CONCURRENT | Best capital-feasible Phase482 primary policy. |
| primary_selected_trades | 25 | Capacity-selected primary trades. |
| primary_dates | 14 | Diagnostic dates represented. |
| primary_symbols | 12 | Symbols represented. |
| primary_net_pnl_inr | 992.965 | Selected primary net PnL. |
| primary_positive_date_rows | 5 | Positive dates. |
| primary_positive_date_fraction | 0.357143 | Positive-date fraction. |
| primary_positive_symbol_rows | 3 | Positive symbols. |
| top_date_net_share | 3.79503 | Top profitable date contribution divided by total net PnL. |
| top_symbol_net_share | 3.26075 | Top profitable symbol contribution divided by total net PnL. |
| side_flip_net_pnl_inr | -10726.9 | Same policy side-flip net PnL. |
| capital_notional_cap_inr | 200000 | Max5 concurrent positions times INR 100,000 notional. |
| initial_capital_inr | 250000 | Pinned capital denominator. |
| capital_feasible_ratio | 0.8 | Max simultaneous notional divided by capital. |
| phase482_acceptance_candidate_rows | 0 | Phase482 candidate rows. |

## Contribution by Date

| diagnostic_trade_date | selected_trades | net_pnl_inr | symbols | positive |
| --- | --- | --- | --- | --- |
| 2026-07-08 | 1 | -273.144 | 1 | 0 |
| 2026-07-09 | 1 | 110.347 | 1 | 1 |
| 2026-07-10 | 2 | 3768.33 | 1 | 1 |
| 2026-07-13 | 1 | -183.643 | 1 | 0 |
| 2026-07-14 | 2 | -517.996 | 2 | 0 |
| 2026-07-15 | 1 | -369.168 | 1 | 0 |
| 2026-07-16 | 1 | -658.722 | 1 | 0 |
| 2026-07-20 | 3 | 1230.73 | 2 | 1 |
| 2026-07-21 | 3 | 300.955 | 2 | 1 |
| 2026-07-23 | 2 | 189.239 | 2 | 1 |
| 2026-07-24 | 2 | -793.498 | 1 | 0 |
| 2026-07-27 | 2 | -559.312 | 2 | 0 |
| 2026-08-03 | 2 | -623.496 | 1 | 0 |
| 2026-08-04 | 2 | -627.655 | 2 | 0 |

## Contribution by Symbol

| symbol | selected_trades | net_pnl_inr | dates | positive |
| --- | --- | --- | --- | --- |
| TCS | 4 | 3237.82 | 3 | 1 |
| ULTRACEMCO | 2 | 979.363 | 2 | 1 |
| WIPRO | 2 | 865.146 | 1 | 1 |
| NESTLEIND | 1 | -76.7739 | 1 | 0 |
| SBIN | 1 | -273.144 | 1 | 0 |
| KOTAKBANK | 1 | -337.602 | 1 | 0 |
| ICICIBANK | 3 | -370.39 | 2 | 0 |
| BAJAJ-AUTO | 3 | -434.689 | 2 | 0 |
| BHARTIARTL | 3 | -439.215 | 3 | 0 |
| HINDUNILVR | 1 | -658.722 | 1 | 0 |
| CIPLA | 2 | -705.326 | 2 | 0 |
| ITC | 2 | -793.498 | 1 | 0 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P483_PHASE482_COMPLETE | True | 1 | 1 | hard |
| P483_SELECTED_POLICY_CAPITAL_FEASIBLE | True | capital_feasible=1;ratio=0.8 | true_and_ratio<=1 | hard |
| P483_SELECTED_POLICY_EVENT_FLOOR_EVALUATED | True | 25 | evaluated | hard |
| P483_SELECTED_POLICY_ABOVE12_EVALUATED | True | 7.14935 | evaluated | hard |
| P483_SELECTED_POLICY_BREADTH_EVALUATED | True | symbols=12;dates=14 | evaluated | hard |
| P483_SIDE_FLIP_EVALUATED | True | primary=992.9649840110019;side_flip=-10726.924279742221 | evaluated | hard |
| P483_POSITIVE_DATE_FRACTION_EVALUATED | True | 0.357143 | evaluated | hard |
| P483_CONCENTRATION_EVALUATED | True | top_date=3.7950274600005844;top_symbol=3.260754895398129 | evaluated | hard |
| P483_ALL_READY_NOT_USED_FOR_ACCEPTANCE | True | diagnostic_only | diagnostic_only | hard |
| P483_NO_PROMOTION_PAPER_LIVE_OR_CLAIM | True | promotion=0;paper=0;claim=0 | all_zero | hard |

## Verdict

| verdict_id | verdict_value | evidence | status |
| --- | --- | --- | --- |
| selected_verdict | P483_CAPACITY_CANDIDATE_REJECTED_BY_CONCENTRATION_AND_DATE_ROBUSTNESS | Phase482 max5 result can advance only if profitability is not too date/symbol concentrated. | rejected |
| event_floor_pass | 0 | selected_trades=25 | quality_check |
| above12_pass | 0 | annualized_return_pct=7.149347884879213 | quality_check |
| breadth_pass | 1 | symbols=12;dates=14 | quality_check |
| positive_date_fraction_pass | 0 | positive_date_fraction=0.35714285714285715 | quality_check |
| concentration_pass | 0 | top_date_share=3.7950274600005844;top_symbol_share=3.260754895398129 | quality_check |
| paper_live_allowed | 0 | No paper/live from this interpretation. | closed |
| promotion_allowed | 0 | No strategy promotion from this interpretation. | closed |
| deployable_profitability_claim_allowed | 0 | No deployable profitability claim. | closed |
| next_action | stop_acceptance_for_phase482_candidate_or_require_materially_new_real_l2_signal_no_paper_live | Do not tune Phase482 after seeing this result. | next |

Boundary: the result may advance to independent holdout precommit only; no promotion, paper/live, or deployable profitability claim.

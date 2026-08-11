# Phase352 Full-Depth Selective Strategy Interpretation

Generated: 2026-08-11T15:01:22.528524+00:00

Phase352 interprets Phase351. The key result is that the bounded full-depth selective synthetic branch has no hidden positive symbol/date pockets and no scenario above the 12% fixed-capital diagnostic bar.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase352_full_depth_selective_interpretation_complete | 1 | Phase352 interpretation completed |
| phase352_phase351_complete | 1 | Phase351 evidence present |
| phase352_phase351_scenario_rows | 9 | Phase351 scenario rows interpreted |
| phase352_phase351_event_rows | 162 | Phase351 event rows interpreted |
| phase352_phase351_positive_event_rows | 0 | Positive daily/symbol event rows |
| phase352_phase351_above12_rows | 0 | Above-12 fixed-capital annualized rows |
| phase352_phase351_acceptance_candidate_rows | 0 | Acceptance candidate rows |
| phase352_best_strategy_id | P351_FULL_DEPTH_SHOCK_REVERSAL | Best Phase351 strategy |
| phase352_best_execution_profile | passive_pessimistic_back_of_queue_cost200 | Best Phase351 execution profile |
| phase352_best_annualized_pct | -4.17216 | Best fixed-capital annualized return |
| phase352_best_expected_net_pnl_inr | -41721.6 | Best expected net PnL |
| phase352_worst_annualized_pct | -289.153 | Worst fixed-capital annualized return |
| phase352_close_phase351_for_acceptance | 1 | Close Phase351 branch for acceptance |
| phase352_expand_same_branch_allowed | 0 | No same-branch expansion without material new thesis |
| phase352_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned cost model |
| phase352_strategy_promotion_allowed | 0 | No promotion |
| phase352_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase352_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase352_next_best_action | restore_phase350_real_date_expansion_or_precommit_material_new_thesis_no_paper_live | Recommended next milestone |

## Decision ledger

| decision_id | decision_value | evidence | interpretation |
| --- | --- | --- | --- |
| phase351_evidence_complete | 1 | scenario_rows=9; event_rows=162; gates=7/7 | Phase351 can be interpreted. |
| hidden_positive_pockets_exist | 0 | positive_event_rows=0; positive_strategy_rows=0 | No positive symbol/date or scenario pocket was found in Phase351. |
| phase351_expand_same_branch | 0 | above12=0; acceptance_candidates=0; positive_event_rows=0 | Do not widen the same bounded synthetic branch without a material new thesis. |
| phase351_branch_closed_for_acceptance | 1 | best_ann=-4.1721579450629775; best_net=-41721.57945062977 | Close Phase351 as a negative synthetic full-depth selective-search result. |
| real_date_expansion_route_remains_open_if_access_restored | 1 | Phase348/350 failed only to add a new unseen real L2 date; Phase342/343 real holdout remains completed and negative. | If fresh SAS/local drop exists, rerun Phase350; otherwise precommit a materially new thesis. |

## Failure ledger

| failure_or_limit | observed | interpretation |
| --- | --- | --- |
| no_positive_event_rows | 0 | The branch has no hidden profitable symbol/date pocket in the bounded evidence. |
| no_above12_scenarios | 0 | No scenario reached the user's >12% annualized diagnostic threshold. |
| no_acceptance_candidates | 0 | No scenario passed event floor, breadth and profitability criteria. |
| passive_reduces_loss_but_does_not_rescue | passive_pessimistic_back_of_queue_cost200 | The best result is a passive-aware profile, but it remains negative. |

## Top Phase351 scenarios

| strategy_id | execution_profile | fill_model_id | horizon_ticks | trade_dates | scheduled_events | expected_filled_events | positive_symbols | positive_symbol_dates | expected_net_pnl_inr | annualized_pct_fixed_capital | avg_fill_probability | avg_depth25_materiality | avg_abs_deep_imbalance_2_5 | avg_spread_bps | worst_event_pnl_inr | above12 | event_floor_met | breadth_met | acceptance_candidate | diagnostic_clue_only | expand_same_branch_allowed | acceptance_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P351_FULL_DEPTH_SHOCK_REVERSAL | passive_pessimistic_back_of_queue_cost200 | P351_PASSIVE_PESSIMISTIC_BACK_OF_QUEUE | 6 | 1 | 761 | 204.516 | 0 | 0 | -41721.6 | -4.17216 | 0.271229 | 0.882351 | 0.40636 | 2.14172 | -1189.53 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| P351_FULL_DEPTH_SHOCK_REVERSAL | passive_base_back_of_queue_cost200 | P351_PASSIVE_BASE_BACK_OF_QUEUE | 6 | 1 | 761 | 306.773 | 0 | 0 | -56013.2 | -5.60132 | 0.406844 | 0.882351 | 0.40636 | 2.14172 | -1168.33 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| P351_FULL_DEPTH_SHOCK_REVERSAL | taker_cost200_fixed_capital | P351_TAKER_DETERMINISTIC | 6 | 1 | 761 | 761 | 0 | 0 | -127652 | -12.7652 | 1 | 0.882351 | 0.40636 | 2.14172 | -1152.7 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| P351_VOLUME_ABSORPTION_REVERSAL | passive_pessimistic_back_of_queue_cost200 | P351_PASSIVE_PESSIMISTIC_BACK_OF_QUEUE | 6 | 1 | 2364 | 639.838 | 0 | 0 | -129297 | -12.9297 | 0.270985 | 0.882351 | 0.391075 | 2.16619 | -1189.53 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| P351_VOLUME_ABSORPTION_REVERSAL | passive_base_back_of_queue_cost200 | P351_PASSIVE_BASE_BACK_OF_QUEUE | 6 | 1 | 2364 | 959.758 | 0 | 0 | -173598 | -17.3598 | 0.406477 | 0.882351 | 0.391075 | 2.16619 | -1168.33 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| P351_VOLUME_ABSORPTION_REVERSAL | taker_cost200_fixed_capital | P351_TAKER_DETERMINISTIC | 6 | 1 | 2364 | 2364 | 0 | 0 | -390623 | -39.0623 | 1 | 0.882351 | 0.391075 | 2.16619 | -1152.7 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| P351_DEEP_PRESSURE_CONTINUATION | passive_pessimistic_back_of_queue_cost200 | P351_PASSIVE_PESSIMISTIC_BACK_OF_QUEUE | 6 | 1 | 17615 | 4787.83 | 0 | 0 | -963620 | -96.362 | 0.271894 | 0.882348 | 0.374361 | 2.07519 | -1189.53 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| P351_DEEP_PRESSURE_CONTINUATION | passive_base_back_of_queue_cost200 | P351_PASSIVE_BASE_BACK_OF_QUEUE | 6 | 1 | 17615 | 7181.75 | 0 | 0 | -1.29409e+06 | -129.409 | 0.407841 | 0.882348 | 0.374361 | 2.07519 | -1168.33 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| P351_DEEP_PRESSURE_CONTINUATION | taker_cost200_fixed_capital | P351_TAKER_DETERMINISTIC | 6 | 1 | 17615 | 17615 | 0 | 0 | -2.89153e+06 | -289.153 | 1 | 0.882348 | 0.374361 | 2.07519 | -1152.7 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P352_PHASE351_COMPLETE | 1 | Phase351 evidence files present |
| P352_HIDDEN_POCKET_AUDITED | 1 | positive_event_rows=0 |
| P352_ZERO_ACCEPTANCE_RECOGNIZED | 1 | acceptance_candidates=0 |
| P352_CLOSE_OR_ROUTE_DECIDED | 1 | Close same branch; route to real-date expansion or material-new thesis |
| P352_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.

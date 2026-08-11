# Phase364 Catalyst Impulse Reversal Clue Interpretation

Generated: 2026-08-11T15:56:54.848379+00:00

Phase364 interprets Phase363. It rejects the precommitted impulse-continuation thesis for acceptance and freezes the impulse-reversal-after-replenishment control as a new sparse clue requiring its own precommit.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase364_catalyst_impulse_reversal_clue_interpretation_complete | 1 | Phase364 interpretation completed |
| phase364_phase363_above12_rows | 8 | Phase363 above-12 rows |
| phase364_continuation_above12_rows | 0 | Continuation above-12 rows |
| phase364_reversal_control_above12_rows | 8 | Reversal-control above-12 rows |
| phase364_best_reversal_scenario_id | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | Best reversal clue |
| phase364_best_reversal_trade_rows | 12 | Best reversal selected trades |
| phase364_best_reversal_dates | 8 | Best reversal dates |
| phase364_best_reversal_symbols | 7 | Best reversal symbols |
| phase364_best_reversal_net_pnl_inr | 3106.73 | Best reversal net PnL |
| phase364_best_reversal_annualized_return_pct | 39.1448 | Best reversal annualized return |
| phase364_best_reversal_event_floor_met | 0 | Best reversal event floor |
| phase364_acceptance_candidate_rows | 0 | No acceptance candidates |
| phase364_strategy_promotion_allowed | 0 | No promotion |
| phase364_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase364_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase364_hard_gate_pass_rows | 6 | Passed hard gates |
| phase364_hard_gate_rows | 6 | Hard gates |
| phase364_next_best_action | precommit_phase365_post_catalyst_impulse_reversal_after_replenishment_no_paper_live | Recommended next milestone |

## Interpretation

| interpretation_id | value | evidence | decision |
| --- | --- | --- | --- |
| continuation_failed | 1 | continuation_above12_rows=0; best_continuation_ann=-25.30190130634633 | Do not continue the Phase362 primary continuation thesis for acceptance. |
| reversal_control_positive_sparse | 1 | reversal_above12_rows=8; best_trades=12; required=30 | Treat reversal-after-replenishment as a new sparse clue only. |
| acceptance_still_closed | 1 | phase363_acceptance_candidate_rows=0 | No replay, promotion, paper/live acceptance or deployable profitability claim. |

## Branch decisions

| decision_id | decision | reason | evidence | paper_live_or_profit_claim_allowed |
| --- | --- | --- | --- | --- |
| P364_REJECT_PHASE362_CONTINUATION_PRIMARY | reject_primary_continuation_thesis_for_acceptance | All impulse-continuation variants were below the 12% annualized threshold. | continuation_above12_rows=0; best_continuation_ann=-25.30190130634633 | 0 |
| P364_FREEZE_REVERSAL_AFTER_REPLENISHMENT_CLUE | freeze_as_new_precommit_candidate_not_acceptance | All above-12 rows came from impulse-reversal controls, not the precommitted continuation thesis, and the best clue is below the 30-event floor. | reversal_above12_rows=8; best_reversal=P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL; trades=12; ann=39.144819884564285 | 0 |

## Reversal clue contract

| clue_id | source_phase | source_scenario_id | decision_delay_seconds | min_abs_impulse_bps | min_abs_l2_l5_imbalance | min_replenishment_ratio | side_rule | best_capacity_selected_trade_rows | best_diagnostic_trade_dates | best_symbols | best_net_pnl_inr | best_annualized_return_pct | event_floor_met | acceptance_candidate | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P364_POST_CATALYST_IMPULSE_REVERSAL_AFTER_REPLENISHMENT | Phase363 | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | 120 | 2.5 | 0.25 | 0 | reverse the signed post-catalyst impulse after displayed liquidity replenishment and levels 2-5 support the original impulse | 12 | 8 | 7 | 3106.73 | 39.1448 | 0 | 0 | sparse_clue_requires_precommit |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P364_PHASE363_PRESENT | 1 | Phase363 summary and scenarios present |
| P364_CONTINUATION_FAILURE_RECORDED | 1 | continuation_above12=0 |
| P364_REVERSAL_CLUE_RECORDED | 1 | reversal_above12=8 |
| P364_EVENT_FLOOR_BLOCKER_RECORDED | 1 | best_trades=12 |
| P364_NO_ACCEPTANCE_CANDIDATES | 1 | acceptance_rows=0 |
| P364_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.

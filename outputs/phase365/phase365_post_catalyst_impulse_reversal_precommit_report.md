# Phase365 Post-Catalyst Impulse Reversal Precommit

Generated: 2026-08-11T16:00:19.960522+00:00

Phase365 precommits the Phase364 sparse reversal-after-replenishment clue as its own frozen thesis. It does not run a search and opens no promotion, paper/live acceptance, or deployable profitability claim.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase365_post_catalyst_impulse_reversal_precommit_complete | 1 | Phase365 precommit completed |
| phase365_thesis_id | P365_POST_CATALYST_IMPULSE_REVERSAL_AFTER_REPLENISHMENT | Precommitted thesis |
| phase365_source_clue_id | P364_POST_CATALYST_IMPULSE_REVERSAL_AFTER_REPLENISHMENT | Source clue |
| phase365_decision_delay_seconds | 120 | Frozen delay |
| phase365_min_abs_impulse_bps | 2.5 | Frozen impulse threshold |
| phase365_min_abs_l2_l5_imbalance | 0.25 | Frozen depth threshold |
| phase365_min_replenishment_ratio | 0 | Frozen replenishment threshold |
| phase365_control_rows | 5 | Control rows |
| phase365_strategy_promotion_allowed | 0 | No promotion |
| phase365_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase365_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase365_hard_gate_pass_rows | 7 | Passed hard gates |
| phase365_hard_gate_rows | 7 | Hard gates |
| phase365_next_best_action | run_phase366_post_catalyst_impulse_reversal_frozen_diagnostic_no_paper_live | Recommended next milestone |

## Thesis contract

| thesis_id | source_clue_id | source_scenario_id | status | material_difference_from_phase362_primary | decision_delay_seconds | horizon_seconds | min_abs_impulse_bps | min_abs_l2_l5_imbalance | min_replenishment_ratio | side_rule | full_depth_rule | cost_rule | paper_live_or_profit_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P365_POST_CATALYST_IMPULSE_REVERSAL_AFTER_REPLENISHMENT | P364_POST_CATALYST_IMPULSE_REVERSAL_AFTER_REPLENISHMENT | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | precommit | This is post-catalyst impulse reversal after replenishment, not impulse continuation. | 120 | 900 | 2.5 | 0.25 | 0 | reverse the signed post-catalyst impulse after displayed liquidity replenishment and levels 2-5 support the original impulse | use full top-five L1-L5 book state; levels 2-5 support must be material; no L1-only variant | Zerodha cost200 fixed-capital scoring | 0 |

## Control catalog

| control_id | control_description | purpose |
| --- | --- | --- |
| primary | post_catalyst_impulse_reversal_after_replenishment | Frozen Phase364 side rule |
| side_flip | post_catalyst_impulse_continuation_same_filters | Must be worse than primary or treated as ambiguity |
| stricter_replenishment | same_reversal_rule_min_replenishment_0p10 | Checks dependence on zero replenishment threshold |
| weaker_depth | same_reversal_rule_min_l2_l5_imbalance_0p15 | Checks depth-threshold sensitivity |
| shorter_delay | same_reversal_rule_decision_delay_60s | Checks delay sensitivity |

## Validation contract

| contract_id | contract_value | description |
| --- | --- | --- |
| phase364_complete_required | 1 | Phase364 must freeze the clue before this precommit. |
| exact_primary_parameters_frozen | 1 | 120s delay, 2.5 bps impulse, 0.25 levels-2-5 imbalance, 0.0 replenishment. |
| full_depth_required | 1 | Use L1-L5 price/qty/order-count fields and levels 2-5 materiality. |
| l1_only_allowed | 0 | No L1-only variants. |
| event_floor | 30 | Acceptance requires at least 30 selected trades. |
| annualized_threshold_pct | 12 | User profitability bar. |
| breadth_required | >=2 positive symbols and >=2 positive symbol/date cells | Avoid one-pocket clue. |
| cost200_fixed_capital_required | 1 | Zerodha cost200 fixed capital. |
| same_run_search_allowed | 0 | No parameter search in Phase366; controls only. |
| paper_live_or_profit_claim_allowed | 0 | No promotion or deployable claim. |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P365_PHASE364_COMPLETE | 1 | Phase364 complete |
| P365_REVERSAL_CLUE_PRESENT | 1 | clue_rows=1 |
| P365_EXACT_PARAMETERS_FROZEN | 1 | delay=120; impulse=2.5; depth=0.25; replenishment=0.0 |
| P365_FULL_DEPTH_REQUIRED | 1 | L1-L5 and levels 2-5 materiality |
| P365_CONTROLS_REGISTERED | 1 | control_rows=5 |
| P365_NO_SEARCH_OR_SAME_FAMILY_RESCUE | 1 | frozen primary plus controls only |
| P365_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.

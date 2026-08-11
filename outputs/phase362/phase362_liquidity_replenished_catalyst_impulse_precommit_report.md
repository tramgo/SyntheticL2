# Phase362 Liquidity-Replenished Catalyst Impulse Precommit

Generated: 2026-08-11T15:40:35.606911+00:00

Phase362 precommits a materially new real-L2 thesis after Phase361 closed the full-depth fade branch for acceptance. This route tests post-catalyst impulse continuation only after displayed liquidity replenishes and levels 2-5 support the impulse direction.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase362_liquidity_replenished_catalyst_impulse_precommit_complete | 1 | Phase362 precommit completed |
| phase362_thesis_id | P362_LIQUIDITY_REPLENISHED_CATALYST_IMPULSE_CONTINUATION | Precommitted thesis |
| phase362_scenario_grid_rows | 16 | Scenario grid rows |
| phase362_materially_new_thesis | 1 | Not same-family fade rescue |
| phase362_same_family_parameter_rescue_allowed | 0 | No rescue of closed fade branch |
| phase362_strategy_promotion_allowed | 0 | No promotion |
| phase362_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase362_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase362_hard_gate_pass_rows | 6 | Passed hard gates |
| phase362_hard_gate_rows | 6 | Hard gates |
| phase362_next_best_action | run_phase363_liquidity_replenished_catalyst_impulse_diagnostic_no_paper_live | Recommended next milestone |

## Thesis contract

| thesis_id | status | material_difference_from_closed_fade | signal_timing | side_rule | full_depth_rule | liquidity_replenishment_rule | execution_rule | lookahead_forbidden | paper_live_or_profit_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P362_LIQUIDITY_REPLENISHED_CATALYST_IMPULSE_CONTINUATION | precommit | Uses post-catalyst price impulse continuation after liquidity replenishment; does not fade top-five or levels-2-5 imbalance. | wait 60s/120s after official catalyst diagnostic start before deciding | continue the signed mid-price impulse from start to decision tick | levels 2-5 imbalance must support impulse direction and top-five imbalance must not contradict it | top-five displayed quantity at decision must be at least as large as at start, with stressed variant requiring >=10% replenishment | marketable diagnostic entry/exit with Zerodha cost200 fixed-capital scoring | 1 | 0 |

## Scenario grid

| scenario_grid_id | decision_delay_seconds | horizon_seconds | min_abs_impulse_bps | min_abs_l2_l5_imbalance | min_replenishment_ratio | top5_noncontradiction_required | side_policy | control_side_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P362_D60_I2p5_D0p15_R0p0 | 60 | 900 | 2.5 | 0.15 | 0 | 1 | impulse_continuation | impulse_reversal |
| P362_D60_I2p5_D0p15_R0p1 | 60 | 900 | 2.5 | 0.15 | 0.1 | 1 | impulse_continuation | impulse_reversal |
| P362_D60_I2p5_D0p25_R0p0 | 60 | 900 | 2.5 | 0.25 | 0 | 1 | impulse_continuation | impulse_reversal |
| P362_D60_I2p5_D0p25_R0p1 | 60 | 900 | 2.5 | 0.25 | 0.1 | 1 | impulse_continuation | impulse_reversal |
| P362_D60_I5p0_D0p15_R0p0 | 60 | 900 | 5 | 0.15 | 0 | 1 | impulse_continuation | impulse_reversal |
| P362_D60_I5p0_D0p15_R0p1 | 60 | 900 | 5 | 0.15 | 0.1 | 1 | impulse_continuation | impulse_reversal |
| P362_D60_I5p0_D0p25_R0p0 | 60 | 900 | 5 | 0.25 | 0 | 1 | impulse_continuation | impulse_reversal |
| P362_D60_I5p0_D0p25_R0p1 | 60 | 900 | 5 | 0.25 | 0.1 | 1 | impulse_continuation | impulse_reversal |
| P362_D120_I2p5_D0p15_R0p0 | 120 | 900 | 2.5 | 0.15 | 0 | 1 | impulse_continuation | impulse_reversal |
| P362_D120_I2p5_D0p15_R0p1 | 120 | 900 | 2.5 | 0.15 | 0.1 | 1 | impulse_continuation | impulse_reversal |
| P362_D120_I2p5_D0p25_R0p0 | 120 | 900 | 2.5 | 0.25 | 0 | 1 | impulse_continuation | impulse_reversal |
| P362_D120_I2p5_D0p25_R0p1 | 120 | 900 | 2.5 | 0.25 | 0.1 | 1 | impulse_continuation | impulse_reversal |
| P362_D120_I5p0_D0p15_R0p0 | 120 | 900 | 5 | 0.15 | 0 | 1 | impulse_continuation | impulse_reversal |
| P362_D120_I5p0_D0p15_R0p1 | 120 | 900 | 5 | 0.15 | 0.1 | 1 | impulse_continuation | impulse_reversal |
| P362_D120_I5p0_D0p25_R0p0 | 120 | 900 | 5 | 0.25 | 0 | 1 | impulse_continuation | impulse_reversal |
| P362_D120_I5p0_D0p25_R0p1 | 120 | 900 | 5 | 0.25 | 0.1 | 1 | impulse_continuation | impulse_reversal |

## Validation contract

| contract_id | contract_value | description |
| --- | --- | --- |
| phase361_branch_closed | 1 | The prior full-depth fade branch must be closed for acceptance before this new thesis runs. |
| materially_new_thesis_required | 1 | This is continuation after catalyst absorption, not same-family fade rescue. |
| input_real_l2_roots | real_data_sample/l2_multiday_panel;real_data_sample/l2_unseen_validation | Use the current local official-catalyst real L2 panels. |
| input_work_orders | outputs/phase341/phase341_phase342_execution_work_order.csv;outputs/phase359/phase359_phase360_execution_work_order.csv | Use existing official-catalyst no-lookahead work orders. |
| full_top_five_depth_required | 1 | Use bid/ask price, quantity and order-count levels 1-5. |
| levels_2_to_5_materiality_required | 1 | Levels 2-5 determine the support filter; no L1-only variant is allowed. |
| liquidity_replenishment_required | 1 | Displayed top-five quantity must replenish after catalyst start. |
| cost200_fixed_capital_required | 1 | Zerodha cost200 and fixed INR 250000 capital denominator are required. |
| annualized_threshold_pct | 12 | Keep user profitability threshold. |
| robust_event_floor | 30 | Sparse fewer-than-30 trade outcomes are discovery only. |
| same_family_parameter_rescue_allowed | 0 | Do not reopen Phase357/358 fade via hidden filters. |
| paper_live_or_profit_claim_allowed | 0 | No paper/live acceptance or deployable profitability claim. |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P362_MATERIAL_NEW_THESIS | 1 | continuation_after_liquidity_replenishment_not_fade |
| P362_SCENARIO_GRID_PRESENT | 1 | grid_rows=16 |
| P362_FULL_DEPTH_REQUIRED | 1 | levels 1-5 with levels 2-5 materiality |
| P362_COST200_FIXED_CAPITAL_REQUIRED | 1 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 |
| P362_NO_SAME_FAMILY_RESCUE | 1 | fade branch remains closed |
| P362_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.

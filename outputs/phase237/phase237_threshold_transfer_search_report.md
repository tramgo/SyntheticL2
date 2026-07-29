# Phase237 Threshold-transfer / Expanded Real-anchor Strategy Search Report

Generated UTC: 2026-07-29T07:01:20.606313+00:00

Phase237 widens the real-anchor strategy search after Phase236 found positive but too-sparse microprice-reversal pockets.
The key redesign is real-quantile threshold transfer: event and signal cutoffs are computed on the Phase235 real-anchor event bars, not copied from synthetic score magnitudes.
This is still research evidence only and does not unlock paper/live trading or a deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase237_threshold_transfer_search_complete | 1 | Phase237 expanded real-anchor search completed |
| phase237_expanded_variant_rows | 3584 | Expanded variants evaluated |
| phase237_positive_variant_rows | 5 | Positive real-anchor variants |
| phase237_breadth_positive_candidate_rows | 3 | Positive breadth candidates |
| phase237_best_candidate_id | P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | Best candidate by real-anchor net P&L |
| phase237_best_family_id | bar_return_reversal | Best candidate family |
| phase237_best_real_anchor_net_pnl_inr | 7041.52 | Best real-anchor net P&L after costs |
| phase237_best_real_anchor_trade_rows | 71 | Best selected trades |
| phase237_best_real_anchor_dates | 6 | Best dates represented |
| phase237_best_real_anchor_symbols | 21 | Best symbols represented |
| phase237_best_control_pass_rows | 3 | Best candidate controls passed |
| phase237_best_control_rows | 4 | Best candidate controls evaluated |
| phase237_hard_gate_pass_rows | 6 | Hard Phase237 gates passed |
| phase237_hard_gate_rows | 6 | Hard Phase237 gates evaluated |
| phase237_candidate_opened_for_phase238 | 1 | Whether Phase238 validation precommit is opened |
| phase237_strategy_promotion_allowed | 0 | No strategy promotion from Phase237 |
| phase237_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase237 |
| phase237_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase237 |
| phase237_next_best_action | run_phase238_precommit_unseen_real_anchor_or_walk_forward_validation_for_phase237_candidate_no_paper_live | Recommended next milestone |

## Best Candidate

| candidate_id | family_id | signal_source | direction | horizon_event_bars | event_quantile | signal_quantile | event_window_score_threshold | signal_abs_threshold | real_anchor_trades | real_anchor_net_pnl_inr | real_anchor_gross_pnl_inr | real_anchor_cost_pnl_drag_inr | real_anchor_dates | real_anchor_symbols | real_anchor_positive_dates | real_anchor_min_date_net_pnl_inr | real_anchor_max_date_contribution_abs | real_anchor_max_symbol_contribution_abs | real_anchor_precision_cost_clear | real_anchor_positive | real_anchor_breadth_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | bar_return_reversal | bar_return | reversal | 6 | 0.95 | 0.95 | 8.3341 | 0.00564863 | 71 | 7041.52 | 15596.5 | 8554.99 | 6 | 21 | 4 | -718.495 | 0.688677 | 0.533342 | 0.507042 | True | True |

## Breadth-positive Candidates

| candidate_id | family_id | signal_source | direction | horizon_event_bars | event_quantile | signal_quantile | event_window_score_threshold | signal_abs_threshold | real_anchor_trades | real_anchor_net_pnl_inr | real_anchor_gross_pnl_inr | real_anchor_cost_pnl_drag_inr | real_anchor_dates | real_anchor_symbols | real_anchor_positive_dates | real_anchor_min_date_net_pnl_inr | real_anchor_max_date_contribution_abs | real_anchor_max_symbol_contribution_abs | real_anchor_precision_cost_clear | real_anchor_positive | real_anchor_breadth_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P237_BAR_RETURN_REVERSAL_H6_EQ0_95_SQ0_95 | bar_return_reversal | bar_return | reversal | 6 | 0.95 | 0.95 | 8.3341 | 0.00564863 | 71 | 7041.52 | 15596.5 | 8554.99 | 6 | 21 | 4 | -718.495 | 0.688677 | 0.533342 | 0.507042 | True | True |
| P237_BAR_RETURN_REVERSAL_H8_EQ0_95_SQ0_95 | bar_return_reversal | bar_return | reversal | 8 | 0.95 | 0.95 | 8.3341 | 0.00566026 | 70 | 6899.11 | 15343.4 | 8444.28 | 6 | 21 | 4 | -1967.35 | 0.702375 | 0.578223 | 0.528571 | True | True |
| P237_BAR_RETURN_REVERSAL_H10_EQ0_95_SQ0_95 | bar_return_reversal | bar_return | reversal | 10 | 0.95 | 0.95 | 8.3341 | 0.00567373 | 69 | 4494.88 | 12812.7 | 8317.85 | 6 | 21 | 4 | -3254.15 | 0.723968 | 0.887326 | 0.42029 | True | True |

## Best Candidate Controls

| control_id | net_pnl_inr | passed | random_p95_net_pnl_inr | random_beat_fraction |
| --- | --- | --- | --- | --- |
| SIDE_FLIP | -24151.5 | True |  |  |
| RANDOM_SIDE_1000_RUNS | 7041.52 | True | 1218 | 0.998 |
| COST_150 | 2764.03 | True |  |  |
| COST_200 | -1513.47 | False |  |  |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P237_EXPANDED_VARIANTS_EVALUATED | True | 3584 | >=3000 expanded variants | hard |
| P237_BREADTH_POSITIVE_CANDIDATE_FOUND | True | 3 | >0 positive breadth candidates | hard |
| P237_BEST_CANDIDATE_NET_POSITIVE | True | 7041.52 | >0 best net P&L | hard |
| P237_BEST_CANDIDATE_BREADTH | True | trades=71;dates=6;symbols=21 | >=50 trades, >=5 dates, >=20 symbols, >=4 positive dates | hard |
| P237_BEST_CANDIDATE_CONTROLS | True | 3 | >=3 / 4 controls pass | hard |
| P237_NO_PAPER_LIVE_OR_PROMOTION_UNLOCK | True | 0 | 0 | hard |

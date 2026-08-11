# Phase357 Full-Depth Market-Neutral Fade Precommit

Generated: 2026-08-11T15:18:02.041448+00:00

Phase357 freezes the Phase356 interpretation that depth-levels-2-5 variants outperformed the top-five-only frozen clue. It is a precommit only.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase357_full_depth_market_neutral_fade_precommit_complete | 1 | Phase357 precommit completed |
| phase357_phase356_complete | 1 | Phase356 evidence present |
| phase357_best_full_depth_scenario | P356_CONTROL_DEPTH_2_5_FADE_VARIANT | Best full-depth scenario |
| phase357_best_full_depth_trade_rows | 12 | Best full-depth trade rows |
| phase357_best_full_depth_annualized_pct | 26.2352 | Best full-depth annualized return |
| phase357_best_full_depth_net_pnl_inr | 1821.89 | Best full-depth net PnL |
| phase357_event_floor_required | 30 | Required event floor |
| phase357_execution_allowed_next | 1 | Phase358 execution allowed |
| phase357_strategy_promotion_allowed | 0 | No promotion |
| phase357_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase357_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase357_next_best_action | run_phase358_full_depth_market_neutral_fade_execution_no_paper_live_or_restore_phase350_real_dates | Recommended next milestone |

## Family contract

| field | frozen_value | description |
| --- | --- | --- |
| family_id | P357_FULL_DEPTH_MARKET_NEUTRAL_FADE | Frozen family identifier |
| source_phase | Phase356 | Derived from Phase356 controls that dominated the Phase355 frozen top-five clue |
| primary_proxy | NIFTYBEES | No proxy tuning before validation |
| primary_lookback_seconds | 900 | No lookback tuning before validation |
| market_context | abs(NIFTYBEES 900s pre-entry return) <= 1.0 bps | Market-neutral context |
| primary_side_rule | fade depth-levels-2-5 imbalance | Full-depth primary side rule |
| guard_rule | top-five fade allowed only with non-contradictory depth-levels-2-5 context | Full-depth guard rule |
| scope | capacity-selected official-catalyst real L2 events | Same event scope as Phase354/356 clue |
| cost_profile | zerodha_2x_all_in_cost_proxy | Pinned cost stress |
| initial_capital_inr | 250000 | Fixed-capital annualization denominator |
| current_best_scenario | P356_CONTROL_DEPTH_2_5_FADE_VARIANT | Best full-depth Phase356 row |
| current_best_trade_rows | 12 | Current sparse count |
| current_best_annualized_pct | 26.2352 | Current diagnostic annualized return |
| current_best_net_pnl_inr | 1821.89 | Current diagnostic net PnL |
| top5_reference_annualized_pct | 24.5055 | Reference top-five frozen clue |

## Validation contract

| contract_id | requirement | hard_gate |
| --- | --- | --- |
| P357_NO_POST_HOC_TUNING | No change to proxy, lookback, market-neutral threshold, event scope, costs, or capital denominator. | 1 |
| P357_FULL_DEPTH_PRIMARY | Depth-levels-2-5 fade/guard is primary; top-five-only clue is reference, not primary. | 1 |
| P357_EVENT_FLOOR | At least 30 events/trades required before acceptance. | 1 |
| P357_ABOVE12 | Annualized return must remain > 12.0% at cost200 fixed capital. | 1 |
| P357_BREADTH | At least two positive symbols and two positive symbol/date cells. | 1 |
| P357_CONTROLS | Side flip, deterministic alternate side, proxy swap, lookback swap, top-five-only reference, and depth-guard ablation required. | 1 |
| P357_UNSEEN_REAL_DATES_FIRST | If current panel remains below event floor, restore Phase350 real-date expansion before acceptance. | 1 |
| P357_NO_PROMOTION_PAPER_LIVE | No strategy promotion, paper/live acceptance or deployable profitability claim. | 1 |

## Control catalog

| control_id | description | required_interpretation |
| --- | --- | --- |
| side_flip | Flip the full-depth fade side. | must_be_negative_or_weaker |
| deterministic_alternate_side | Alternate long/short over the same selected events. | must_be_negative_or_weaker |
| proxy_swap_bankbees | Use BANKBEES under same market-neutral logic. | robustness_control |
| lookback_swap_300s | Use 300s NIFTYBEES lookback. | robustness_control |
| top5_only_reference | Original Phase355 top-five fade clue. | reference_not_primary |
| depth_guard_ablation | Remove or invert depth-levels-2-5 guard. | must_not_improve_cleanly |

## Gate evaluation

| gate_id | passed | evidence |
| --- | --- | --- |
| P357_PHASE356_COMPLETE | 1 | Phase356 evidence present |
| P357_FULL_DEPTH_DOMINANCE_RECOGNIZED | 1 | Depth variant beats top-five clue |
| P357_SPARSE_RECOGNIZED | 1 | trade_rows=12 |
| P357_CONTRACT_PRESENT | 1 | contract_rows=8 |
| P357_CONTROLS_PRESENT | 1 | control_rows=6 |
| P357_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | 1 | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened.

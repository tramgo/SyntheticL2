# Phase236 Real-anchor Neighbor Search Report

Generated UTC: 2026-07-29T06:51:51.182740+00:00

Phase236 tests the Phase233 microprice-reversal horizon/threshold neighborhood on the Phase235 real-anchor event bars.
It searches for breadth around the profitable synthetic candidate, but it does not tune on real data for promotion and does not unlock paper/live trading.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase236_real_anchor_neighbor_search_complete | 1 | Phase236 neighbor replay completed |
| phase236_neighbor_variant_rows | 12 | Phase233 neighbor variants replayed |
| phase236_positive_real_anchor_variant_rows | 7 | Positive real-anchor variants after cost floor |
| phase236_breadth_passing_variant_rows | 0 | Positive variants passing date/symbol breadth |
| phase236_best_candidate_id | P233_MICROPRICE_REVERSAL_H5_Q0_9 | Best real-anchor neighbor by net P&L |
| phase236_best_real_anchor_net_pnl_inr | 1447.7 | Best real-anchor net P&L after costs |
| phase236_best_real_anchor_trade_rows | 1 | Best real-anchor selected trades |
| phase236_best_real_anchor_dates | 1 | Best real-anchor dates represented |
| phase236_best_real_anchor_symbols | 1 | Best real-anchor symbols represented |
| phase236_hard_gate_pass_rows | 3 | Hard Phase236 gates passed |
| phase236_hard_gate_rows | 5 | Hard Phase236 gates evaluated |
| phase236_real_anchor_neighbor_search_pass | 0 | Whether any neighbor passed positive breadth gates |
| phase236_strategy_promotion_allowed | 0 | No strategy promotion from Phase236 |
| phase236_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase236 |
| phase236_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase236 |
| phase236_next_best_action | run_phase237_redesign_threshold_transfer_or_expand_real_anchor_strategy_family_no_paper_live | Recommended next milestone |

## Neighbor Summary

| candidate_id | parent_candidate_id | horizon_event_bars | threshold_quantile | event_window_score_threshold | abs_microprice_dev_threshold | real_anchor_trades | real_anchor_net_pnl_inr | real_anchor_gross_pnl_inr | real_anchor_cost_pnl_drag_inr | real_anchor_dates | real_anchor_symbols | real_anchor_positive_dates | real_anchor_min_date_net_pnl_inr | real_anchor_precision_cost_clear | real_anchor_breadth_pass | real_anchor_positive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P233_MICROPRICE_REVERSAL_H5_Q0_9 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | 5 | 0.9 | 54.3162 | 0.00010257 | 1 | 1447.7 | 1610.39 | 162.692 | 1 | 1 | 1 | 1447.7 | 1 | False | True |
| P233_MICROPRICE_REVERSAL_H5_Q0_875 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | 5 | 0.875 | 48.4975 | 8.71008e-05 | 2 | 1292.35 | 1581.15 | 288.808 | 2 | 2 | 1 | -155.351 | 0.5 | False | True |
| P233_MICROPRICE_REVERSAL_H4_Q0_9 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | 4 | 0.9 | 54.3162 | 0.00010257 | 1 | 1223.94 | 1386.63 | 162.692 | 1 | 1 | 1 | 1223.94 | 1 | False | True |
| P233_MICROPRICE_REVERSAL_H4_Q0_875 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | 4 | 0.875 | 48.4975 | 8.71008e-05 | 2 | 947.47 | 1236.28 | 288.808 | 2 | 2 | 1 | -276.467 | 0.5 | False | True |
| P233_MICROPRICE_REVERSAL_H3_Q0_9 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | 3 | 0.9 | 54.3162 | 0.00010257 | 1 | 637.416 | 800.108 | 162.692 | 1 | 1 | 1 | 637.416 | 1 | False | True |
| P233_MICROPRICE_REVERSAL_H3_Q0_875 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | 3 | 0.875 | 48.4975 | 8.71008e-05 | 2 | 540.535 | 829.343 | 288.808 | 2 | 2 | 1 | -96.881 | 0.5 | False | True |
| P233_MICROPRICE_REVERSAL_H2_Q0_9 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | 2 | 0.9 | 54.3162 | 0.00010257 | 1 | 78.0186 | 240.711 | 162.692 | 1 | 1 | 1 | 78.0186 | 1 | False | True |
| P233_MICROPRICE_REVERSAL_H2_Q0_925 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | 2 | 0.925 |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| P233_MICROPRICE_REVERSAL_H3_Q0_925 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | 3 | 0.925 |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| P233_MICROPRICE_REVERSAL_H4_Q0_925 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | 4 | 0.925 |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| P233_MICROPRICE_REVERSAL_H5_Q0_925 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | 5 | 0.925 |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | False | False |
| P233_MICROPRICE_REVERSAL_H2_Q0_875 | P231_MICROPRICE_REVERSAL_H3_Q0_9 | 2 | 0.875 | 48.4975 | 8.71008e-05 | 2 | -327.917 | -39.109 | 288.808 | 2 | 2 | 1 | -405.935 | 0.5 | False | False |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P236_NEIGHBOR_VARIANTS_REPLAYED | True | 12 | >=12 Phase233 neighbor variants | hard |
| P236_POSITIVE_REAL_ANCHOR_VARIANTS_FOUND | True | 7 | >0 positive real-anchor variants | hard |
| P236_BREADTH_PASSING_VARIANTS_FOUND | False | 0 | >0 positive variants with >=3 dates and >=5 symbols | hard |
| P236_BEST_VARIANT_TRADE_BREADTH | False | 1 | best variant has >=25 trades | hard |
| P236_NO_PAPER_LIVE_OR_PROMOTION_UNLOCK | True | 0 | 0 | hard |

# Phase235 Real-anchor Microprice-reversal Replay Report

Generated UTC: 2026-07-29T06:48:50.355252+00:00

Phase235 uses tick-derived Phase176 15-second real receive-flow features, aggregates 10 source buckets per event bar, and replays the frozen Phase234/Phase233 microprice-reversal candidate.
It is a local real-anchor dry run only: no paper/live acceptance, no parameter tuning on real data, and no deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase235_real_anchor_microprice_replay_complete | 1 | Phase235 real-anchor replay completed |
| phase235_parent_candidate_id | P231_MICROPRICE_REVERSAL_H3_Q0_9 | Candidate carried forward from Phase234 |
| phase235_source_horizon_sec | 15 | Phase176 source feature horizon used |
| phase235_source_buckets_per_event_bar | 10 | Source buckets aggregated per real event bar |
| phase235_source_feature_rows | 286633 | Phase176 real source feature rows loaded |
| phase235_real_event_bar_rows | 28793 | Real event bars materialized |
| phase235_real_anchor_trade_rows | 1 | Frozen candidate trades selected on real-anchor bars |
| phase235_real_anchor_net_pnl_inr | 637.416 | Real-anchor net P&L after cost floor |
| phase235_real_anchor_dates | 1 | Real dates represented in selected trades |
| phase235_real_anchor_symbols | 1 | Symbols represented in selected trades |
| phase235_control_pass_rows | 3 | Controls passed |
| phase235_control_rows | 4 | Controls evaluated |
| phase235_hard_gate_pass_rows | 4 | Hard Phase235 gates passed |
| phase235_hard_gate_rows | 6 | Hard Phase235 gates evaluated |
| phase235_real_anchor_replay_pass | 0 | Whether the frozen candidate passed the real-anchor dry run |
| phase235_strategy_promotion_allowed | 0 | No strategy promotion from Phase235 |
| phase235_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase235 |
| phase235_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase235 |
| phase235_next_best_action | run_phase236_close_or_redesign_microprice_reversal_after_real_anchor_failure_no_paper_live | Recommended next milestone |

## Replay Summary

| candidate_id | real_anchor_trades | real_anchor_net_pnl_inr | real_anchor_gross_pnl_inr | real_anchor_cost_pnl_drag_inr | real_anchor_positive_dates | real_anchor_dates | real_anchor_symbols | real_anchor_min_date_net_pnl_inr | real_anchor_leave_one_date_min_net_pnl_inr | real_anchor_max_date_contribution_abs | real_anchor_max_symbol_contribution_abs | real_anchor_precision_cost_clear |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | 1 | 637.416 | 800.108 | 162.692 | 1 | 1 | 1 | 637.416 | 0 | 1 | 1 | 1 |

## Real Event-bar Coverage

| trade_date | symbols | real_event_bars | min_symbol_event_bars | median_symbol_event_bars | max_symbol_event_bars |
| --- | --- | --- | --- | --- | --- |
| 2026-07-08 | 32 | 1888 | 59 | 59 | 59 |
| 2026-07-09 | 32 | 2752 | 86 | 86 | 86 |
| 2026-07-10 | 32 | 4832 | 151 | 151 | 151 |
| 2026-07-13 | 32 | 4832 | 151 | 151 | 151 |
| 2026-07-14 | 32 | 4825 | 150 | 151 | 151 |
| 2026-07-15 | 32 | 4832 | 151 | 151 | 151 |
| 2026-07-16 | 32 | 4832 | 151 | 151 | 151 |

## Controls

| control_id | net_pnl_inr | passed | random_p95_net_pnl_inr | random_beat_fraction |
| --- | --- | --- | --- | --- |
| SIDE_FLIP | -962.801 | True |  |  |
| RANDOM_SIDE_100_RUNS | 637.416 | False | 637.416 | 0.5 |
| COST_150 | 556.07 | True |  |  |
| COST_200 | 474.724 | True |  |  |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P235_REAL_EVENT_BARS_MATERIALIZED | True | 1 | >0 candidate trades after materialization | hard |
| P235_REAL_ANCHOR_NET_POSITIVE | True | 637.416 | >0 real-anchor net P&L after costs | hard |
| P235_REAL_ANCHOR_DATE_BREADTH | False | 1 | >=3 real dates represented in selected trades | hard |
| P235_REAL_ANCHOR_SYMBOL_BREADTH | False | 1 | >=5 symbols represented in selected trades | hard |
| P235_CONTROLS_PASS | True | 3 | >=3 / 4 controls pass | hard |
| P235_NO_PAPER_LIVE_OR_PROMOTION_UNLOCK | True | 0 | 0 | hard |

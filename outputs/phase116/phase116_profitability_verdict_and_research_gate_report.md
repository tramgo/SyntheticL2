# Phase116 Profitability Verdict and Research Gate

Generated UTC: 2026-07-19T22:59:21.972130+00:00

Phase116 updates the stop/continue decision using the latest dense replay, candidate replay and real-anchor gate evidence.
The current verdict is intentionally blunt: no strategy family has an accepted profitable survivor, so more same-family dense shards are blocked.
The next useful work is either importing/collecting enough real L2 days to unlock real-anchor replay or precommitting a genuinely new edge hypothesis before any bounded synthetic replay.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase116_profitability_evidence_rows | 6 | Latest profitability and replay-lock evidence rows reviewed |
| phase116_dense_strategy_profile_rows | 9 | Dense strategy/profile rows reviewed from Phase52 |
| phase116_dense_positive_after_cost_rows | 0 | Dense strategy/profile rows positive after costs |
| phase116_positive_pocket_evidence_rows | 3 | Evidence rows with isolated positive pockets |
| phase116_accepted_strategy_rows | 0 | Accepted profitable strategy rows across reviewed evidence |
| phase116_blocklisted_family_rows | 6 | Strategy families blocked from same-shard continuation |
| phase116_same_family_shard_continuation_allowed | 0 | 1 means more same-family shard replay is allowed |
| phase116_strategy_replay_gate | closed | Profitability gate for current strategy families |
| phase116_next_best_action | collect_or_import_more_real_l2_days_then_run_phase115_with_execute_import | Recommended next milestone |
| phase116_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha equity intraday NSE cost model version |

## Dense Strategy Profile Verdict

| strategy_id | execution_profile | trade_dates | trades | annual_net_pnl_inr | mean_net_return_per_trade | after_cost_profitable | decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DENSE_S01_L1_IMBALANCE | zero_latency_spread_only_control | 84 | 90068501 | -1.54677e+09 | -0.000171732 | False | retired_negative_after_costs |
| DENSE_S03_1T_MOMENTUM | zero_latency_spread_only_control | 86 | 88584746 | -2.07147e+09 | -0.000233841 | False | retired_negative_after_costs |
| DENSE_S02_MICROPRICE | zero_latency_spread_only_control | 33 | 89084762 | -2.20327e+09 | -0.000247323 | False | retired_negative_after_costs |
| DENSE_S01_L1_IMBALANCE | retail_marketable_default | 85 | 89100465 | -1.23948e+10 | -0.0013911 | False | retired_negative_after_costs |
| DENSE_S03_1T_MOMENTUM | retail_marketable_default | 86 | 87500212 | -1.38106e+10 | -0.00157836 | False | retired_negative_after_costs |
| DENSE_S02_MICROPRICE | retail_marketable_default | 43 | 88045262 | -1.42514e+10 | -0.00161864 | False | retired_negative_after_costs |
| DENSE_S01_L1_IMBALANCE | stressed_retail | 85 | 89100367 | -1.67842e+10 | -0.00188374 | False | retired_negative_after_costs |
| DENSE_S03_1T_MOMENTUM | stressed_retail | 86 | 87500146 | -1.92156e+10 | -0.00219606 | False | retired_negative_after_costs |
| DENSE_S02_MICROPRICE | stressed_retail | 43 | 88045104 | -1.99255e+10 | -0.0022631 | False | retired_negative_after_costs |

## Profitability Verdict Ledger

| evidence_id | scope | trades_or_rows | positive_after_cost_rows | accepted_strategy_rows | best_net_pnl_inr | worst_net_pnl_inr | positive_pockets_observed | verdict | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P52_DENSE_TICK_FULL_YEAR_PARTIAL_REPLAY | dense L1/microprice/one-tick-momentum replay across scanned full-year shards | 797029565 | 0 | 0 | -1.54677e+09 | -1.99255e+10 | False | falsified_for_same_family_continuation | do_not_continue_dense_taker_shards_without_new_edge_hypothesis |
| P82_HDFCBANK_STRATIFIED_SMOKE | HDFCBANK lead-lag stratified smoke retest | 0 | 0 | 0 | 0 | 0 | False | falsified | retire_hdfcbank_lead_lag_after_stratified_falsification |
| P84_HDFCBANK_CACHED_STRATIFIED_FULL_YEAR | HDFCBANK cached stratified full-year retest | 58988 | 3 | 0 | -6.97746e+06 | -6.97746e+06 | True | falsified_despite_positive_month_pockets | retire_hdfcbank_lead_lag_after_cached_stratified_falsification |
| P91_CROSS_SYMBOL_REGIME_IMBALANCE | cross-symbol market/sector/symbol-vs-sector imbalance candidates | 8623 | 1 | 0 | 34609 | -245423 | True | no_accepted_survivor | retire_cross_symbol_imbalance_or_move_to_low_turnover_event_window_design |
| P93_LOW_TURNOVER_EVENT_WINDOW | low-turnover shock continuation/reversal event-window candidates | 202 | 4 | 0 | 38990.4 | -46599.9 | True | no_accepted_survivor | stop_strategy_mining_return_to_generator_realism_calibration_audit |
| P115_REAL_PANEL_REFRESH_GATE | real-anchor refresh and replay unlock gate | 6 | 0 | 0 |  |  | False | real_strategy_replay_locked | collect_or_import_more_real_l2_days_then_run_phase115_with_execute_import |

## Strategy Replay Blocklist

| blocked_family_id | blocked_strategy_ids | block_reason | same_shard_continuation_allowed | unlock_condition |
| --- | --- | --- | --- | --- |
| DENSE_L1_IMBALANCE_MARKETABLE | DENSE_S01_L1_IMBALANCE | Phase52 dense replay found negative annual net P&L in every execution profile. | False | new precommitted non-taker or materially different feature class plus train/test/month gates |
| DENSE_MICROPRICE_MARKETABLE | DENSE_S02_MICROPRICE | Phase52 dense replay found negative annual net P&L in every execution profile. | False | new precommitted non-taker or materially different feature class plus train/test/month gates |
| DENSE_ONE_TICK_MOMENTUM_MARKETABLE | DENSE_S03_1T_MOMENTUM | Phase52 dense replay found negative annual net P&L in every execution profile. | False | new precommitted non-taker or materially different feature class plus train/test/month gates |
| HDFCBANK_LEAD_LAG | phase77_phase82_phase84_hdfcbank_rechecks | Disjoint and cached stratified HDFCBANK retests produced zero pass months/zero accepted survivor. | False | only a newly specified cross-symbol feature may include HDFCBANK; do not rerun the retired rule |
| CROSS_SYMBOL_IMBALANCE_CURRENT_RULES | P90_MARKET_IMBALANCE_CONTINUATION;P90_SECTOR_IMBALANCE_CONTINUATION;P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION | Phase91 found positive pockets but zero candidate pass rows. | False | redesign features and precommit new gates before replay |
| LOW_TURNOVER_EVENT_WINDOW_CURRENT_RULES | P92_SHOCK_CONTINUATION;P92_BOOK_DISLOCATION_REVERSAL;P92_SHOCK_EXHAUSTION_REVERSAL | Phase93 found positive pockets but zero candidate pass rows. | False | new event-window hypothesis with stronger gross edge over retail costs |

## Next Best Action Gate

| gate_id | gate_status | evidence | policy |
| --- | --- | --- | --- |
| P116_NO_ACCEPTED_PROFITABILITY | closed | accepted_strategy_rows=0 | synthetic positive pockets are not profitability proof |
| P116_REAL_REPLAY_UNLOCK | closed | ready_real_anchor_days=1; days_needed_for_min=4 | real-anchor replay stays closed until Phase115/Phase110 unlocks it |
| P116_COMPUTE_BUDGET | no_more_large_dense_strategy_shards | Phase52 scanned 797M+ dense simulated trades with zero positive-after-cost rows | large shard continuation requires a materially new precommitted edge hypothesis |
| P116_NEXT_BEST_ACTION | collect_or_import_more_real_l2_days_then_run_phase115_with_execute_import | latest evidence favors real-anchor expansion and hypothesis redesign over brute-force shard replay | spend next milestone on data unlock or new-feature precommit, not repeated failed-family replay |

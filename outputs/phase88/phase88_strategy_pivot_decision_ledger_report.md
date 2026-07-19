# Phase88 Strategy Pivot Decision Ledger

Generated UTC: 2026-07-19T21:05:16.930965+00:00

Phase88 answers the post-Phase87 question: synthetic profitability pockets have appeared, but no dense tick-level retail-cost strategy family has produced an accepted survivor.
The decision is to stop shard-by-shard continuation for the retired families and pivot to a new feature class with predeclared gates.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase88_profitability_evidence_rows | 12 | Profitability evidence rows reviewed |
| phase88_positive_pocket_rows | 8 | Rows where some positive synthetic P&L pocket was observed |
| phase88_accepted_survivor_rows | 0 | Rows accepted as robust retail-cost survivors |
| phase88_retired_family_rows | 4 | Strategy families retired by cumulative evidence |
| phase88_more_same_family_shards_allowed | 0 | 1 means continuing same-family shard replay is allowed |
| phase88_next_best_action | P89_passive_queue_capture_cost_floor | Recommended next milestone |
| phase88_strategy_pivot_required | 1 | 1 means pivot to a new feature class before more replay scale |
| phase88_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model used by cited evidence |

## Profitability Evidence Ledger

| evidence_id | source_phase | strategy_scope | positive_pocket_observed | accepted_survivor | best_net_pnl_inr | realistic_or_retail_positive_rows | total_trades_or_rows | failure_mode | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P41_all_profile_synthetic_positive | 41 | deterministic full-year expansion across all model/profile rows | True | False | 1.18574e+06 | 0 | 2612173 | positive only outside realistic retail/stressed profiles | not_deployable_evidence |
| P42_native_full_year_l2_negative | 42 | native full-year L2 event-state strategy/profile replay | False | False | -4.33712e+06 | 0 | 6846221 | all annual strategy/profile rows negative after costs | retired |
| P43_cost_salvage_oracle_like_positive | 43 | cost-aware salvage variants across profiles | True | False | 85087.1 | 0 | 5027566 | positive variants did not survive realistic retail profiles | retired |
| P52_dense_replay_checkpoint_negative | 52 | dense tick replay checkpoint | False | False |  | 0 | 14530597 | zero positive strategy/profile rows after Zerodha retail costs | do_not_continue_dense_bruteforce |
| P54_selective_control_positive | 54 | bounded selective dense replay | True | False | 7856.21 | 0 | 456 | positive only under nondeployable zero-latency/spread-only control | control_only |
| P55_cost_aware_oracle_positive | 55 | cost-aware edge mining | True | False | 65110.5 | 0 | 490 | oracle ceiling positive but deployable candidate negative | retired |
| P56_no_lookahead_rules_negative | 56 | no-lookahead cost-clearing rule discovery | False | False | -4829.7 | 0 | 180 | zero positive no-lookahead test rules after retail costs | retired |
| P60_to_P61_lower_frequency_failed_wider_sweep | 60,61 | lower-frequency event-bar continuation candidate | True | False | 4939 | 1 | 645 | initial validation candidate failed wider sweep with net_pnl_inr=-88748.03 | retired |
| P63_kotakbank_falsification | 63 | KOTAKBANK-only follow-up from Phase62 clue | False | False | -24100.3 | 0 | 155 | single-symbol clue negative after costs | retire_phase60_candidate_family |
| P77_HDFCBANK_disjoint_month_failed | 77 | HDFCBANK lead-lag disjoint-month retest | True | False | -130842 | 0 | 624 | only 3 of 10 valid months positive and aggregate net P&L negative | retire_or_redesign_hdfcbank_lead_lag_before_more_shards |
| P84_HDFCBANK_cached_stratified_full_year_failed | 84 | cached stratified HDFCBANK full-year retest | True | False | -6.97746e+06 | 0 | 58988 | full-year cached stratified retest lost materially after costs | retire_hdfcbank_lead_lag_after_cached_stratified_falsification |
| P87_precommitted_composite_family_failed | 87 | Phase86-precommitted composite event-intensity/absolute-move families | True | False | 61590.8 | 0 | 18 | best test pocket failed train gates and no precommitted candidate passed both splits | retire_precommitted_composite_family_or_design_new_feature_class |

## Retired Strategy Family Ledger

| family_id | source_evidence | decision | more_shards_allowed | why | resume_condition |
| --- | --- | --- | --- | --- | --- |
| DENSE_MARKETABLE_TAKER_MICRO_MOMENTUM | P42,P52,P54,P55,P56 | retired | False | Dense marketable/taker variants repeatedly fail after spread, slippage, impact and Zerodha retail charges. | Only if a new precommitted signal class has ex-ante expected edge above costs and uses disjoint validation before replay expansion. |
| LOWER_FREQUENCY_EVENT_BAR_CONTINUATION | P60,P61,P63 | retired | False | The Phase60 validation pocket did not survive wider symbol/month sweep or KOTAKBANK follow-up. | Do not resume this rule family; use only as a negative-control benchmark. |
| HDFCBANK_CROSS_SYMBOL_LEAD_LAG | P77,P84 | retired | False | Disjoint-month and cached stratified retests are aggregate negative with zero accepted pass months under the final gate. | Only a genuinely new cross-symbol feature with predeclared train/test/month gates may use HDFCBANK again. |
| COMPOSITE_EVENT_INTENSITY_ABS_MOVE | P85,P86,P87 | retired | False | The cost-budget design stage produced candidates, but locked replay found zero train/test/full survivors. | Do not widen thresholds; design a new feature class instead. |
| SYNTHETIC_PROFITABILITY_CLAIM | P41_all_profile_synthetic_positive,P42_native_full_year_l2_negative,P43_cost_salvage_oracle_like_positive,P52_dense_replay_checkpoint_negative,P54_selective_control_positive,P55_cost_aware_oracle_positive,P56_no_lookahead_rules_negative,P60_to_P61_lower_frequency_failed_wider_sweep,P63_kotakbank_falsification,P77_HDFCBANK_disjoint_month_failed,P84_HDFCBANK_cached_stratified_full_year_failed,P87_precommitted_composite_family_failed | not_established | False | Positive pockets exist, but no dense tick-level retail-cost strategy has passed robustness, breadth and train/test gates. | A future profitability claim requires a precommitted survivor with after-cost P&L, breadth, positive-month persistence and adverse-selection controls. |

## Next Feature Class Gate

| priority | next_action_id | feature_class | why_this_is_different | minimum_implementation | go_no_go_gate |
| --- | --- | --- | --- | --- | --- |
| 1 | P89_passive_queue_capture_cost_floor | passive_limit_queue_capture_with_adverse_selection | It tests a different economic mechanism: earning spread/queue edge rather than paying spread as a taker. | Construct no-lookahead hypothetical passive fills at L1 with pessimistic/base/optimistic queue-position assumptions, adverse-selection markouts and Zerodha charge model. | All fill-assumption tiers must report after-cost P&L, hit rate, adverse markout and positive-month breadth; optimistic-only success is not a survivor. |
| 2 | P90_cross_symbol_regime_imbalance_precommit | sector_or_index_conditioned_cross_symbol_imbalance | It lowers turnover and requires cross-sectional context rather than single-symbol dense twitch signals. | Precommit sector/index imbalance features, symbols, train/test months, max turnover and cost-budget thresholds before replay. | Must beat Zerodha retail costs in train and test with no single symbol/month contributing the majority of P&L. |
| 3 | P91_event_window_low_turnover_shock_response | low_turnover_event_window_reversal_or_continuation | It trades fewer, larger expected moves where retail cost drag is less dominant. | Define shock windows from generator state and received-event features, then precommit entry/exit horizons and cost floors. | Must pass disjoint-month validation and show gross edge comfortably above spread/slippage/impact/charges. |

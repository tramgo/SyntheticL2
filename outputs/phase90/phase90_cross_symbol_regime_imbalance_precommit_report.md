# Phase90 Cross-Symbol Regime-Imbalance Precommit

Generated UTC: 2026-07-19T21:12:46.893586+00:00

Phase90 locks a new cross-symbol feature class before directional replay.
It follows Phase88's pivot contract and Phase89's simple passive falsification by moving to lower-turnover market/sector-context imbalance features.
Feature thresholds are computed from train-month feature distributions only; replay P&L is not inspected here.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase90_feature_rows | 160150 | Cross-symbol feature rows materialized from Phase83 cached bars |
| phase90_train_feature_rows | 81818 | Train rows available for feature-threshold calibration |
| phase90_test_feature_rows | 78332 | Test rows locked for replay evaluation |
| phase90_signal_family_rows | 3 | Cross-symbol/regime signal families precommitted |
| phase90_candidate_spec_rows | 12 | Candidate threshold specs precommitted |
| phase90_validation_gate_rows | 7 | Replay validation gates locked |
| phase90_phase88_same_family_shards_allowed | 0 | Must be 0 before pivoting to a new family |
| phase90_phase89_passive_queue_pass | 0 | Phase89 simple passive result used only as pivot context |
| phase90_ready_for_replay | 1 | 1 means Phase91 cross-symbol replay may run without changing thresholds |
| phase90_recommend_next_action | run_precommitted_cross_symbol_regime_imbalance_replay | Recommended next milestone |

## Feature Diagnostics

| feature | train_rows | train_abs_p75 | train_abs_p90 | train_abs_p95 | train_mean |
| --- | --- | --- | --- | --- | --- |
| x_market_l5_ex_target | 81818 | 0.0497447 | 0.0554489 | 0.0619224 | 0.0426956 |
| x_sector_l5_ex_target | 66476 | 0.306157 | 0.38726 | 0.621527 | -0.00190293 |
| x_symbol_vs_sector_l1 | 66476 | 0.38613 | 0.683171 | 1.31843 | 5.21075e-19 |
| x_market_regime_intensity | 81818 | 6.54439 | 7.80543 | 8.59647 | 5.46721 |
| x_sector_regime_intensity | 66476 | 36.1731 | 54.1318 | 77.6957 | 27.876 |
| taker_round_trip_cost_floor_bps | 81818 | 11.9845 | 13.1523 | 13.863 | 11.2077 |

## Precommitted Signal Families

| family_id | hypothesis | feature_column | direction_rule | target_universe | required_filters | turnover_policy | why_not_posthoc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P90_MARKET_IMBALANCE_CONTINUATION | When broad same-bar ex-target market L5 imbalance is extreme and event intensity is high, target symbols may continue in the same direction over the next event bar. | x_market_l5_ex_target | side = sign(x_market_l5_ex_target) | equities_only | abs(x_market_l5_ex_target) threshold AND x_market_regime_intensity threshold AND taker_round_trip_cost_floor_bps <= train_p60_cost_floor_bps | max 1 signal per symbol per trade_date/feed_profile/source_event_bar_id; candidate replay must cap test trades by predeclared gate | Family is defined after Phase89 failure and before any Phase90 directional P&L replay. |
| P90_SECTOR_IMBALANCE_CONTINUATION | When ex-target sector L5 imbalance is extreme, lower-turnover sector-context signals may transfer to target symbols. | x_sector_l5_ex_target | side = sign(x_sector_l5_ex_target) | equities_only_with_sector_symbol_count_ge_3 | abs(x_sector_l5_ex_target) threshold AND x_sector_regime_intensity threshold AND taker_round_trip_cost_floor_bps <= train_p60_cost_floor_bps | max 1 signal per symbol per trade_date/feed_profile/source_event_bar_id; no symbol may exceed concentration gate | Uses sector map and train feature thresholds only; no next_bar_return inspection. |
| P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION | When a symbol's own L1 pressure diverges from its sector ex-target pressure, the symbol may mean-revert toward sector pressure over the next event bar. | x_symbol_vs_sector_l1 | side = -sign(x_symbol_vs_sector_l1) | equities_only_with_sector_symbol_count_ge_3 | abs(x_symbol_vs_sector_l1) threshold AND sector_event_intensity threshold AND taker_round_trip_cost_floor_bps <= train_p60_cost_floor_bps | max 1 signal per symbol per trade_date/feed_profile/source_event_bar_id; require broad symbol/month survival | Divergence/reversion hypothesis is locked before replay and competes with continuation families. |

## Precommitted Candidate Specs

| candidate_id | family_id | feature_column | direction_rule | target_universe | feature_abs_quantile | feature_abs_threshold | intensity_column | intensity_abs_quantile | intensity_abs_threshold | max_taker_round_trip_cost_floor_bps | train_months | test_months |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P90_MARKET_IMBALANCE_CONTINUATION_F0_9_I0_75 | P90_MARKET_IMBALANCE_CONTINUATION | x_market_l5_ex_target | side = sign(x_market_l5_ex_target) | equities_only | 0.9 | 0.0554489 | x_market_regime_intensity | 0.75 | 6.54439 | 11.3507 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P90_MARKET_IMBALANCE_CONTINUATION_F0_9_I0_9 | P90_MARKET_IMBALANCE_CONTINUATION | x_market_l5_ex_target | side = sign(x_market_l5_ex_target) | equities_only | 0.9 | 0.0554489 | x_market_regime_intensity | 0.9 | 7.80543 | 11.3507 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P90_MARKET_IMBALANCE_CONTINUATION_F0_95_I0_75 | P90_MARKET_IMBALANCE_CONTINUATION | x_market_l5_ex_target | side = sign(x_market_l5_ex_target) | equities_only | 0.95 | 0.0619224 | x_market_regime_intensity | 0.75 | 6.54439 | 11.3507 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P90_MARKET_IMBALANCE_CONTINUATION_F0_95_I0_9 | P90_MARKET_IMBALANCE_CONTINUATION | x_market_l5_ex_target | side = sign(x_market_l5_ex_target) | equities_only | 0.95 | 0.0619224 | x_market_regime_intensity | 0.9 | 7.80543 | 11.3507 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P90_SECTOR_IMBALANCE_CONTINUATION_F0_9_I0_75 | P90_SECTOR_IMBALANCE_CONTINUATION | x_sector_l5_ex_target | side = sign(x_sector_l5_ex_target) | equities_only_with_sector_symbol_count_ge_3 | 0.9 | 0.38726 | x_sector_regime_intensity | 0.75 | 36.1731 | 11.3507 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P90_SECTOR_IMBALANCE_CONTINUATION_F0_9_I0_9 | P90_SECTOR_IMBALANCE_CONTINUATION | x_sector_l5_ex_target | side = sign(x_sector_l5_ex_target) | equities_only_with_sector_symbol_count_ge_3 | 0.9 | 0.38726 | x_sector_regime_intensity | 0.9 | 54.1318 | 11.3507 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P90_SECTOR_IMBALANCE_CONTINUATION_F0_95_I0_75 | P90_SECTOR_IMBALANCE_CONTINUATION | x_sector_l5_ex_target | side = sign(x_sector_l5_ex_target) | equities_only_with_sector_symbol_count_ge_3 | 0.95 | 0.621527 | x_sector_regime_intensity | 0.75 | 36.1731 | 11.3507 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P90_SECTOR_IMBALANCE_CONTINUATION_F0_95_I0_9 | P90_SECTOR_IMBALANCE_CONTINUATION | x_sector_l5_ex_target | side = sign(x_sector_l5_ex_target) | equities_only_with_sector_symbol_count_ge_3 | 0.95 | 0.621527 | x_sector_regime_intensity | 0.9 | 54.1318 | 11.3507 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION_F0_9_I0_75 | P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION | x_symbol_vs_sector_l1 | side = -sign(x_symbol_vs_sector_l1) | equities_only_with_sector_symbol_count_ge_3 | 0.9 | 0.683171 | sector_event_intensity | 0.75 | 144.18 | 11.3507 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION_F0_9_I0_9 | P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION | x_symbol_vs_sector_l1 | side = -sign(x_symbol_vs_sector_l1) | equities_only_with_sector_symbol_count_ge_3 | 0.9 | 0.683171 | sector_event_intensity | 0.9 | 161.6 | 11.3507 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION_F0_95_I0_75 | P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION | x_symbol_vs_sector_l1 | side = -sign(x_symbol_vs_sector_l1) | equities_only_with_sector_symbol_count_ge_3 | 0.95 | 1.31843 | sector_event_intensity | 0.75 | 144.18 | 11.3507 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |
| P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION_F0_95_I0_9 | P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION | x_symbol_vs_sector_l1 | side = -sign(x_symbol_vs_sector_l1) | equities_only_with_sector_symbol_count_ge_3 | 0.95 | 1.31843 | sector_event_intensity | 0.9 | 161.6 | 11.3507 | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 |

## Validation Gates

| gate_id | requirement | pass_threshold |
| --- | --- | --- |
| P90_NO_LABEL_INSPECTION | Phase90 may compute cross-symbol features and train-period feature thresholds only; directional P&L and next_bar_return labels are reserved for replay. | No candidate is selected or edited using replay P&L. |
| P90_SPLIT_LOCK | Train months are 2026-01 through 2026-06; test months are 2026-07 through 2026-12. | Splits appear in every candidate spec and cannot be changed in replay. |
| P90_COST_BUDGET | Replay may only trade rows at or below the train-period p60 taker round-trip cost floor for the relevant cached bars. | taker_round_trip_cost_floor_bps <= max_taker_round_trip_cost_floor_bps |
| P90_TURNOVER_BREADTH | Replay candidate must have 500 to 8000 trades per split and at least 20 target symbols in both train and test. | 500<=train_trades<=8000; 500<=test_trades<=8000; train_symbols>=20; test_symbols>=20 |
| P90_AFTER_COST_SURVIVAL | Replay must produce positive after-cost net P&L in both train and test with precision_cost_clear >= 0.55. | train_net_pnl_inr>0; test_net_pnl_inr>0; train_precision>=0.55; test_precision>=0.55 |
| P90_CONCENTRATION | No single symbol or month may contribute more than 35% of absolute positive test net P&L. | max_symbol_contribution_abs<=0.35; max_month_contribution_abs<=0.35 |
| P90_RETIREMENT | If no precommitted candidate passes, do not widen thresholds in the same family; move to P91 event-window low-turnover design. | No post-hoc threshold widening. |

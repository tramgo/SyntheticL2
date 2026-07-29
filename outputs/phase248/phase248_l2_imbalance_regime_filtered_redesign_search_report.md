# Phase248 L2 Imbalance / Regime-filtered Redesign Search

Generated UTC: 2026-07-29T09:23:31.949364+00:00

Phase248 is a training-only search for the Phase247 redesign families.
It excludes the 2026-07-17 and 2026-07-20 holdout/fresh diagnostic dates from tuning, requires top-five market-by-price imbalance in every variant, and keeps downloads/paper/live/profitability claims closed.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase248_l2_imbalance_regime_filtered_search_complete | 1 | Phase248 training-only redesign search completed |
| phase248_training_event_bar_rows | 28793 | Training event bars used |
| phase248_training_dates | 7 | Training dates used |
| phase248_training_symbols | 32 | Training symbols used |
| phase248_forbidden_tuning_dates | 2026-07-17;2026-07-20 | Dates excluded from tuning |
| phase248_variant_rows | 1728 | Combined-filter variants evaluated |
| phase248_l2_filtered_variant_rows | 1728 | Variants with required top-five imbalance filter active |
| phase248_net_positive_variant_rows | 30 | Net-positive variants at base cost |
| phase248_cost150_positive_variant_rows | 12 | Positive variants at 1.5x cost |
| phase248_cost200_positive_variant_rows | 0 | Positive variants at 2.0x cost |
| phase248_controlled_candidate_rows | 0 | Candidates evaluated with side-flip/random-side controls |
| phase248_survivor_candidate_rows | 0 | Candidates passing controls and breadth gates |
| phase248_best_candidate_id | P248_COMBINED_STRICT_REVERSAL_H8_EQ0_99_BQ0_85_TQ0_8_SP0_75_IQ0_25_RQ0_75 | Best Phase248 survivor/candidate |
| phase248_best_family_id | P247_COMBINED_STRICT_REVERSAL | Best candidate family |
| phase248_best_training_net_pnl_inr | 62.2026 | Best training net P&L |
| phase248_best_cost200_net_pnl_inr | -37.8345 | Best 2x-cost net P&L |
| phase248_best_random_beat_fraction | 0 | Best random-side beat fraction |
| phase248_best_trade_rows | 1 | Best trade rows |
| phase248_best_dates | 1 | Best dates represented |
| phase248_best_symbols | 1 | Best symbols represented |
| phase248_hard_gate_pass_rows | 5 | Hard gates passed |
| phase248_hard_gate_rows | 6 | Hard gates evaluated |
| phase248_future_holdout_precommit_allowed | 0 | Future holdout precommit allowed only if survivors exist |
| phase248_download_more_dates_now_allowed | 0 | No raw-date download in Phase248 |
| phase248_holdout_parameter_tuning_allowed | 0 | No holdout-date tuning |
| phase248_strategy_promotion_allowed | 0 | No strategy promotion from Phase248 |
| phase248_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase248 |
| phase248_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase248 |
| phase248_next_best_action | close_or_broaden_phase248_l2_imbalance_regime_filtered_search_no_downloads_no_paper_live | Recommended next milestone |

## Best Candidate

| candidate_id | family_id | horizon_event_bars | event_quantile | bar_return_quantile | top5_abs_quantile | spread_quantile | intensity_quantile | range_vol_quantile | event_window_score_threshold | bar_abs_threshold | top5_abs_threshold | spread_max | event_intensity_min | range_vol_max | market_abs_max | training_trades | training_net_pnl_inr | training_gross_pnl_inr | training_cost_pnl_drag_inr | cost150_net_pnl_inr | cost200_net_pnl_inr | training_dates | training_symbols | training_positive_dates | training_min_date_net_pnl_inr | training_max_date_contribution_abs | training_max_symbol_contribution_abs | training_precision_cost_clear | cost_stress_pass | top5_filter_active | spread_liquidity_guard_active | range_or_market_veto_active |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P248_COMBINED_STRICT_REVERSAL_H8_EQ0_99_BQ0_85_TQ0_8_SP0_75_IQ0_25_RQ0_75 | P247_COMBINED_STRICT_REVERSAL | 8 | 0.99 | 0.85 | 0.8 | 0.75 | 0.25 | 0.75 | 15.9509 | 0.00104634 | 0.428267 | 0.41 | 71 | 5.34974 | 0.000312989 | 1 | 62.2026 | 162.24 | 100.037 | 12.1841 | -37.8345 | 1 | 1 | 1 | 62.2026 | 1 | 1 | 1 | False | 1 | 1 | 1 |

## Survivor Candidates

_No rows._

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P248_PHASE247_WORK_ORDER_PRESENT | True | run_phase248_training_only_l2_imbalance_regime_filtered_redesign_no_2026_07_17_or_2026_07_20_tuning_no_downloads_no_paper_live | Phase247 next action targets Phase248 | hard |
| P248_FORBIDDEN_HOLDOUT_DATES_EXCLUDED | True | 2026-07-17;2026-07-20 | 2026-07-17 and 2026-07-20 excluded | hard |
| P248_L2_FILTER_ACTIVE_IN_ALL_VARIANTS | True | 1728/1728 | all variants | hard |
| P248_VARIANTS_EVALUATED | True | 1728 | >=800 combined-filter variants | hard |
| P248_COST200_POSITIVE_VARIANTS_FOUND | False | 0 | >0 positive at 2x cost | hard |
| P248_CONTROLLED_SURVIVOR_FOUND | False | 0 | >0 controlled survivors | diagnostic |
| P248_NO_DOWNLOAD_HOLDOUT_TUNING_OR_PAPER_LIVE | True | 0 | 0 | hard |

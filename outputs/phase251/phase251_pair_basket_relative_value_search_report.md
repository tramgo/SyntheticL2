# Phase251 Pair/Basket Relative-value Training Search

Generated UTC: 2026-07-29T10:04:15.198780+00:00

Phase251 executes the Phase250 precommitted training-only search.
It excludes 2026-07-17 and 2026-07-20 from tuning, uses existing Phase235 event bars only, balances long/short notional, applies costs per leg and keeps downloads, holdout execution, paper/live and profitability claims closed.
Every variant requires Zerodha top-five market-by-price depth through `avg_top5_market_by_price_imbalance` and a depth-beyond-L1 contrast, so this is not an L1-only or price-only search.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase251_pair_basket_search_complete | 1 | Phase251 pair/basket training-only search completed |
| phase251_training_event_bar_rows | 26095 | Training event bars after forbidden-date exclusion and universe filter |
| phase251_training_dates | 7 | Training dates used |
| phase251_training_symbols | 29 | Training symbols used |
| phase251_forbidden_tuning_dates | 2026-07-17;2026-07-20 | Dates excluded from tuning |
| phase251_variant_rows | 3840 | Pair/basket variants evaluated |
| phase251_full_top_five_depth_variant_rows | 3840 | Variants using top-five market-by-price depth |
| phase251_depth_beyond_l1_variant_rows | 3840 | Variants using depth-beyond-L1 contrast |
| phase251_net_positive_variant_rows | 0 | Net-positive variants at base cost |
| phase251_cost150_positive_variant_rows | 0 | Positive variants at 1.5x cost |
| phase251_cost200_positive_variant_rows | 0 | Positive variants at 2.0x cost |
| phase251_controlled_candidate_rows | 0 | Candidates evaluated with side-flip/random-side controls |
| phase251_survivor_candidate_rows | 0 | Candidates passing controls and breadth gates |
| phase251_best_candidate_id | P251_SECTOR_PAIR_RESIDUAL_REVERSION_H10_RQ0_95_TQ0_8_DQ0_5_SP0_75_IQ0_5_RB1 | Best Phase251 survivor/candidate |
| phase251_best_family_id | P250_SECTOR_PAIR_RESIDUAL_REVERSION | Best candidate family |
| phase251_best_training_net_pnl_inr | -1681.18 | Best training net P&L |
| phase251_best_cost200_net_pnl_inr | -5120.63 | Best 2x-cost net P&L |
| phase251_best_random_beat_fraction | 0 | Best random-side beat fraction |
| phase251_best_trade_rows | 17 | Best signal trades |
| phase251_best_leg_rows | 34 | Best leg rows |
| phase251_best_dates | 6 | Best dates represented |
| phase251_best_symbols | 11 | Best leg symbols represented |
| phase251_best_peer_groups | 7 | Best peer groups represented |
| phase251_hard_gate_pass_rows | 8 | Hard gates passed |
| phase251_hard_gate_rows | 9 | Hard gates evaluated |
| phase251_future_holdout_precommit_allowed | 0 | Future holdout precommit allowed only if survivors exist |
| phase251_download_more_dates_now_allowed | 0 | No raw-date download in Phase251 |
| phase251_holdout_parameter_tuning_allowed | 0 | No holdout-date tuning |
| phase251_strategy_promotion_allowed | 0 | No strategy promotion from Phase251 |
| phase251_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase251 |
| phase251_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase251 |
| phase251_next_best_action | close_or_broaden_phase251_pair_basket_relative_value_search_no_downloads_no_paper_live | Recommended next milestone |

## Best Candidate

| candidate_id | family_id | horizon_event_bars | residual_quantile | top5_abs_quantile | depth_beyond_l1_quantile | spread_quantile | intensity_quantile | rank_bucket | basket_mode | training_trades | training_leg_rows | training_net_pnl_inr | training_gross_pnl_inr | training_cost_pnl_drag_inr | cost150_net_pnl_inr | cost200_net_pnl_inr | training_dates | training_symbols | training_signal_symbols | training_peer_groups | training_positive_dates | training_min_date_net_pnl_inr | training_max_date_contribution_abs | training_max_symbol_contribution_abs | training_precision_cost_clear | cost_stress_pass | market_neutral_notional | costs_applied_per_leg | top5_feature_active | full_top_five_depth_active | depth_beyond_l1_active |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P251_SECTOR_PAIR_RESIDUAL_REVERSION_H10_RQ0_95_TQ0_8_DQ0_5_SP0_75_IQ0_5_RB1 | P250_SECTOR_PAIR_RESIDUAL_REVERSION | 10 | 0.95 | 0.8 | 0.5 | 0.75 | 0.5 | 1 | residual_reversion_against_peers | 17 | 34 | -1681.18 | 1758.28 | 3439.46 | -3400.91 | -5120.63 | 6 | 11 | 11 | 7 | 2 | -1259.71 | 0.7493 | 0.380224 | 0.352941 | False | 1 | 1 | 1 | 1 | 1 |

## Survivor Candidates

_No rows._

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P251_PHASE250_WORK_ORDER_PRESENT | True | run_phase251_training_only_pair_basket_relative_value_search_no_downloads_no_2026_07_17_or_2026_07_20_tuning_no_paper_live | Phase250 next action targets Phase251 | hard |
| P251_FORBIDDEN_DATES_EXCLUDED | True | 2026-07-17;2026-07-20 | 2026-07-17 and 2026-07-20 excluded | hard |
| P251_VARIANTS_EVALUATED | True | 3840 | >=400 pair/basket variants | hard |
| P251_MARKET_NEUTRAL_ALL_VARIANTS | True | 3840/3840 | all variants | hard |
| P251_COSTS_PER_LEG_ALL_VARIANTS | True | 3840/3840 | all variants | hard |
| P251_FULL_TOP_FIVE_DEPTH_ALL_VARIANTS | True | 3840/3840 | all variants use top-five market-by-price depth | hard |
| P251_DEPTH_BEYOND_L1_ALL_VARIANTS | True | 3840/3840 | all variants use depth beyond L1 | hard |
| P251_COST200_POSITIVE_VARIANTS_FOUND | False | 0 | >0 positive at 2x cost | hard |
| P251_CONTROLLED_SURVIVOR_FOUND | False | 0 | >0 controlled survivors | diagnostic |
| P251_NO_DOWNLOAD_HOLDOUT_TUNING_OR_PAPER_LIVE | True | 0 | 0 | hard |

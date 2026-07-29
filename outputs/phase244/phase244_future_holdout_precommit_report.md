# Phase244 Future Holdout Precommit

Generated UTC: 2026-07-29T08:26:14.342158+00:00

Phase244 freezes the best Phase243 survivor for future holdout testing and defines the storage decision required before any more raw L2 downloads.
It does not download data, tune on 2026-07-17, run a holdout, open paper/live trading, or claim deployable profitability.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase244_future_holdout_precommit_complete | 1 | Phase244 future holdout precommit completed |
| phase244_candidate_id | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | Frozen Phase243 candidate |
| phase244_best_training_net_pnl_inr | 8576.39 | Training/discovery net P&L |
| phase244_best_cost200_net_pnl_inr | 5033.27 | 2x-cost training/discovery net P&L |
| phase244_best_random_beat_fraction | 0.997 | Training random-side beat fraction |
| phase244_min_holdout_dates_required | 2 | Minimum fresh unseen holdout dates |
| phase244_target_holdout_dates | 3 | Target fresh unseen holdout dates |
| phase244_min_holdout_trades_required | 20 | Minimum frozen-candidate holdout trades |
| phase244_min_holdout_symbols_required | 10 | Minimum holdout symbols |
| phase244_storage_decision_required | 1 | Storage decision required before more raw downloads |
| phase244_download_more_dates_now_allowed | 0 | No additional raw-date download in Phase244 |
| phase244_holdout_parameter_tuning_allowed | 0 | No 2026-07-17 or future holdout tuning |
| phase244_future_holdout_execution_allowed_now | 0 | Precommit only; no holdout run in Phase244 |
| phase244_strategy_promotion_allowed | 0 | No strategy promotion from Phase244 |
| phase244_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase244 |
| phase244_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase244 |
| phase244_hard_gate_pass_rows | 7 | Hard gates passed |
| phase244_hard_gate_rows | 7 | Hard gates evaluated |
| phase244_next_best_action | choose_storage_option_then_download_fresh_unseen_dates_for_phase244_frozen_candidate_no_tuning_no_paper_live | Recommended next milestone |

## Frozen Candidate Spec

| candidate_id | family_id | signal_source | direction | horizon_event_bars | event_quantile | signal_quantile | event_window_score_threshold | signal_abs_threshold | training_trades | training_dates | training_symbols | training_net_pnl_inr | cost150_net_pnl_inr_x | cost200_net_pnl_inr_x | random_beat_fraction | control_pass_rows | frozen_for_future_holdout | parameter_tuning_allowed_in_future_holdout | forbidden_tuning_date | paper_or_live_acceptance_allowed | deployable_profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | bar_return_reversal | bar_return | reversal | 8 | 0.99 | 0.9 | 15.5881 | 0.00779013 | 29 | 5 | 13 | 8576.39 | 6804.83 | 5033.27 | 0.997 | 4 | 1 | 0 | 2026-07-17 | 0 | 0 |

## Storage Decision Options

| option_id | description | allowed_now | download_allowed_without_user_storage_decision | expected_effect |
| --- | --- | --- | --- | --- |
| H244_A_STORAGE_FREE_LOCAL | Free or archive local scratch/smoke/raw data before downloading more unseen real dates | 1 | 0 | enables 2-3 date holdout without new disk pressure |
| H244_B_EXTERNAL_OR_SECONDARY_DISK | Attach or choose a larger storage location for unseen raw L2 dates | 1 | 0 | preserves current local artifacts and shifts raw date footprint off C drive |
| H244_C_ONE_DATE_ONLY_DIAGNOSTIC | Use only already downloaded 2026-07-17 as diagnostic if storage is not expanded | 1 | 0 | fastest but cannot satisfy acceptance and must not tune thresholds |

## Future Holdout Contract

| contract_id | requirement | requirement_type | candidate_id |
| --- | --- | --- | --- |
| H244_FREEZE_CANDIDATE | Candidate id, horizon, signal source, direction and thresholds are frozen before holdout | hard | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 |
| H244_NO_2026_07_17_TUNING | The existing 2026-07-17 holdout cannot be used for threshold or parameter selection | hard | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 |
| H244_STORAGE_DECISION_REQUIRED | Choose local cleanup/archive or external storage before downloading more raw dates | hard | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 |
| H244_MIN_DATES | Minimum 2 fresh unseen dates; target 3 dates | acceptance | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 |
| H244_MIN_TRADES | At least 20 frozen-candidate trades after materialization | acceptance | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 |
| H244_MIN_SYMBOLS | At least 10 symbols represented in selected trades | acceptance | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 |
| H244_COST_CONTROLS | Net P&L positive at base, 1.5x and 2.0x modeled Zerodha costs | acceptance | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 |
| H244_RANDOM_SIDE_CONTROL | Random-side beat fraction at least 0.95 on the holdout | acceptance | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 |
| H244_SIDE_FLIP_CONTROL | Side-flipped net P&L must be negative | acceptance | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 |
| H244_NO_PAPER_LIVE | No paper/live/deployable profitability claim from precommit or download phases | hard | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P244_PHASE243_SURVIVOR_SELECTED | True | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | non-empty Phase243 survivor | hard |
| P244_CANDIDATE_FROZEN | True | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | candidate spec frozen for future holdout | hard |
| P244_NO_HOLDOUT_TUNING | True | 2026-07-17 | 2026-07-17 cannot be used for tuning | hard |
| P244_STORAGE_DECISION_OPTIONS_WRITTEN | True | 3 | >=3 storage options | hard |
| P244_HOLDOUT_CONTRACT_WRITTEN | True | 10 | >=10 contract requirements | hard |
| P244_DOWNLOAD_NOT_ALLOWED_NOW | True | 0 | no raw download until storage decision | hard |
| P244_NO_PAPER_LIVE_OR_PROFIT_CLAIM | True | 0 | 0 | hard |

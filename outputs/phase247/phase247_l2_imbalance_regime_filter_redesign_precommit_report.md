# Phase247 L2 Imbalance / Regime-filter Redesign Precommit

Generated UTC: 2026-07-29T09:11:43.472680+00:00

Phase247 converts the Phase246 failure into a bounded redesign contract.
It explicitly rejects bar-return reversal as a standalone strategy and requires top-five market-by-price imbalance, spread/liquidity, volatility/range and market-direction checks before the next training-only search.
No new raw date is downloaded, no holdout data is tuned, and no paper/live or deployable profitability claim is opened.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase247_l2_imbalance_regime_filter_redesign_precommit_complete | 1 | Phase247 redesign precommit completed |
| phase247_parent_candidate_id | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | Failed frozen Phase244 parent candidate |
| phase247_failure_attribution_rows | 6 | Phase246 failure rows attributed |
| phase247_feature_filter_rows | 9 | Required/optional feature filter rows |
| phase247_redesign_candidate_rows | 4 | Redesign candidate families precommitted |
| phase247_acceptance_contract_rows | 8 | Acceptance contract rows |
| phase247_forbidden_tuning_dates | 2026-07-17;2026-07-20 | Dates excluded from tuning |
| phase247_l2_imbalance_filter_required | 1 | Top-five market-by-price imbalance filter required |
| phase247_range_or_market_veto_required | 1 | Range-regime or market-direction veto required |
| phase247_cost_stress_first_objective | 1 | 2x cost stress prioritized in candidate ranking |
| phase247_no_more_downloads_for_failed_parent_allowed | 1 | No more raw-date downloads for failed parent candidate |
| phase247_training_search_allowed_next | 1 | Phase248 training-only redesign search may run next |
| phase247_holdout_execution_allowed_now | 0 | No holdout execution in Phase247 |
| phase247_strategy_promotion_allowed | 0 | No strategy promotion from Phase247 |
| phase247_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase247 |
| phase247_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase247 |
| phase247_hard_gate_pass_rows | 6 | Hard gates passed |
| phase247_hard_gate_rows | 6 | Hard gates evaluated |
| phase247_next_best_action | run_phase248_training_only_l2_imbalance_regime_filtered_redesign_no_2026_07_17_or_2026_07_20_tuning_no_downloads_no_paper_live | Recommended next milestone |

## Failure Attribution

| failure_id | observed_value | required_value | interpretation |
| --- | --- | --- | --- |
| P247_BAR_REVERSAL_ALONE_FAILED_FRESH_DATE | 0 | 1 | Frozen bar-return reversal did not survive one fresh unseen date; redesign required before any more downloads. |
| P247_CONTROL_FAIL_RANDOM_SIDE_1000_RUNS | 645.948 | control_pass=True | Existing candidate is not robust enough under the configured control. |
| P247_CONTROL_FAIL_COST_200 | -481.076 | control_pass=True | Existing candidate is not robust enough under the configured control. |
| P247_GATE_FAIL_P246_DIAGNOSTIC_MIN_TRADES | 9 | >=20 trades | One-date diagnostic gate failed; do not continue this frozen candidate date-by-date. |
| P247_GATE_FAIL_P246_DIAGNOSTIC_MIN_SYMBOLS | 9 | >=10 symbols | One-date diagnostic gate failed; do not continue this frozen candidate date-by-date. |
| P247_GATE_FAIL_P246_DIAGNOSTIC_CONTROLS | 2/4 | 4/4 controls | One-date diagnostic gate failed; do not continue this frozen candidate date-by-date. |

## Required Filter Catalog

| feature_or_filter | status | source | purpose |
| --- | --- | --- | --- |
| bar_return | required | existing Phase235/246 event-bar field | primary reversal trigger retained but no longer sufficient alone |
| avg_top5_market_by_price_imbalance | required | top-five market-by-price depth field | confirm reversal pressure or veto continuation-aligned depth |
| avg_l1_imbalance | optional_confirmation | best bid/ask depth field | secondary order-book pressure check |
| avg_spread | required | event-bar spread field | avoid expensive or unstable spread states |
| taker_round_trip_cost_floor_bps | required | modeled Zerodha cost and spread floor | cost floor remains embedded in every replay |
| avg_event_intensity_proxy | required | tick/update intensity proxy | avoid weak bars with insufficient market activity |
| abs_bar_return_bps | required | bar move size field | compare bar move with recent volatility/range regime |
| market_direction_proxy | required_if_available | NIFTYBEES or index proxy to be materialized in Phase248 if present | veto reversal trades aligned with broad market continuation |
| news_event_calendar | blocked_external_optional | not currently available locally | do not fabricate news labels; leave as explicit external data gap |

## Redesign Candidate Catalog

| redesign_id | parent_candidate_id | entry_logic | required_filters | tuning_scope | holdout_execution_now_allowed |
| --- | --- | --- | --- | --- | --- |
| P247_REVERSAL_L2_CONFIRMATION | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | bar_return reversal only when top-five market-by-price imbalance points against continuation and toward reversal | avg_top5_market_by_price_imbalance directional confirmation; spread guard; event-intensity guard; cost floor | training_only_excludes_2026_07_17_and_2026_07_20 | 0 |
| P247_REVERSAL_L2_DIVERGENCE | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | large bar-return reversal only when price impulse and top-five imbalance diverge | bar_return sign opposite depth-pressure sign; spread guard; recent-volatility normalization | training_only_excludes_2026_07_17_and_2026_07_20 | 0 |
| P247_RANGE_ONLY_REVERSAL | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | bar-return reversal only in range-bound / non-trending volatility states | recent volatility/range filter; market-direction veto if proxy available; spread guard | training_only_excludes_2026_07_17_and_2026_07_20 | 0 |
| P247_COMBINED_STRICT_REVERSAL | P243_BAR_RETURN_REVERSAL_H8_EQ0_99_SQ0_9 | strict conjunction of reversal trigger, top-five imbalance confirmation, range regime, liquidity/spread and market-direction veto | all P247 required filters; smallest turnover first; 2x-cost-positive objective | training_only_excludes_2026_07_17_and_2026_07_20 | 0 |

## Acceptance Contract

| contract_id | requirement | requirement_type |
| --- | --- | --- |
| H247_NO_HOLDOUT_TUNING | Exclude 2026-07-17;2026-07-20 from threshold, filter and parameter selection | hard |
| H247_L2_FILTER_REQUIRED | At least one top-five market-by-price imbalance filter must be active | hard |
| H247_RANGE_OR_MARKET_VETO_REQUIRED | At least one range-regime or market-direction veto must be active if the needed proxy exists | hard |
| H247_LIQUIDITY_SPREAD_GUARD_REQUIRED | Spread/liquidity guard must be active before any replay candidate can be opened | hard |
| H247_COST_STRESS_FIRST_OBJECTIVE | Candidate ranking must prefer positive 2.0x-cost net P&L before base-cost headline P&L | hard |
| H247_RANDOM_SIDE_AND_SIDE_FLIP_CONTROLS | Random-side beat >=0.95 and side-flip net negative remain required | hard |
| H247_NO_MORE_DATE_DOWNLOAD_FOR_FAILED_PARENT | Do not download more fresh dates for the failed Phase244 parent candidate | hard |
| H247_NO_PAPER_LIVE | No paper/live/deployable profitability claim from the redesign precommit | hard |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P247_PHASE246_FAILURE_OBSERVED | True | 6 | >0 failure attribution rows | hard |
| P247_TOP5_IMBALANCE_INCLUDED | True | avg_top5_market_by_price_imbalance | present | hard |
| P247_REDESIGN_CATALOG_WRITTEN | True | 4 | >=3 redesign candidates | hard |
| P247_ACCEPTANCE_CONTRACT_WRITTEN | True | 8 | >=6 contract rows | hard |
| P247_NO_HOLDOUT_TUNING | True | 2026-07-17;2026-07-20 | excluded from tuning | hard |
| P247_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

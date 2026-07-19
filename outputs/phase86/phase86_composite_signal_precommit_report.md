# Phase86 Composite Signal Precommit

Generated UTC: 2026-07-19T20:58:27.605242+00:00

Phase86 locks the next signal-family experiment before directional P&L is inspected.
It uses Phase85 cost-budget seeds but precommits family definitions, train/test split, and retirement gates.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase86_selected_filter_seed_rows | 6 | Phase85 filter seeds selected for precommit |
| phase86_precommitted_family_rows | 3 | Composite signal families precommitted |
| phase86_validation_gate_rows | 6 | Validation gates locked before P&L replay |
| phase86_train_months | 2026-01\|2026-02\|2026-03\|2026-04\|2026-05\|2026-06 | Train months for family selection |
| phase86_test_months | 2026-07\|2026-08\|2026-09\|2026-10\|2026-11\|2026-12 | Untouched test months for final evaluation |
| phase86_ready_for_replay | 1 | 1 means Phase87 replay may run |
| phase86_recommend_next_action | run_precommitted_composite_signal_replay | Recommended next milestone |

## Selected Filter Seeds

| contract_id | allowed | feature_name | quantile | threshold | fraction_abs_return_ge_1_25x_cost | rule | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P85_ELIGIBLE_FILTER_SEED_01 | True | event_intensity | 0.99 | 197.3 | 0.947368 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_02 | True | event_intensity | 0.975 | 190.1 | 0.934664 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_03 | True | abs_bar_return | 0.99 | 276.162 | 0.922812 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_04 | True | event_intensity | 0.95 | 182.6 | 0.918283 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_05 | True | event_intensity | 0.9 | 164.3 | 0.917343 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |
| P85_ELIGIBLE_FILTER_SEED_07 | True | abs_bar_return | 0.975 | 213.418 | 0.868631 | May be used only as a pre-filter seed; direction and execution logic still require disjoint validation. | combine_with_regime_context_and_validate_direction_out_of_sample |

## Precommitted Composite Signal Families

| family_id | hypothesis | direction_rule | required_filters | excluded_conditions | position_model | why_not_posthoc | event_intensity_seed_thresholds | abs_bar_return_seed_thresholds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P86_INTENSITY_MOMENTUM_CONTINUATION | High event-intensity bars with same-sign current bar return may continue for one source-event bar when cost budget is favorable. | side = sign(bar_return) | event_intensity_seed AND abs_bar_return_seed AND one_way_cost_hurdle_bps <= symbol_month_p75_cost_hurdle_bps | ETF targets excluded only if later cross-symbol variant is used; no HDFCBANK leader rule reuse. | single_bar_marketable_entry_exit_proxy | Feature seeds are imported from Phase85 cost-budget ranking before directional P&L is evaluated. | q0.99:197.3\|q0.975:190.1\|q0.95:182.6 | q0.99:276.16159960665465\|q0.975:213.41842443330265 |
| P86_INTENSITY_MEAN_REVERSION | Extreme high event-intensity bars may overreact and reverse for one source-event bar when current bar move is large. | side = -sign(bar_return) | event_intensity_seed AND abs_bar_return_seed AND one_way_cost_hurdle_bps <= symbol_month_p75_cost_hurdle_bps | No HDFCBANK leader rule reuse; no symbol-specific tuning before disjoint validation. | single_bar_marketable_entry_exit_proxy | Continuation and reversion are both precommitted as competing hypotheses before P&L inspection. | q0.99:197.3\|q0.975:190.1\|q0.95:182.6 | q0.99:276.16159960665465\|q0.975:213.41842443330265 |
| P86_SHOCK_INTENSITY_REVERSAL | On market/symbol shock bars, high intensity plus large current move may reverse after liquidity shock exhaustion. | side = -sign(bar_return) | shock_bar AND event_intensity_seed AND abs_bar_return_seed | Must report shock and non-shock separately; no pooling-only acceptance. | single_bar_marketable_entry_exit_proxy | Shock split is motivated by Phase72/79/83 generator shock diagnostics before replay. | q0.99:197.3\|q0.975:190.1\|q0.95:182.6 | q0.99:276.16159960665465\|q0.975:213.41842443330265 |

## Precommitted Validation Gates

| gate_id | requirement | pass_threshold |
| --- | --- | --- |
| P86_SPLIT_LOCK | Use train months 2026-01 through 2026-06 only for selecting among precommitted families; test months 2026-07 through 2026-12 are untouched until final evaluation. | No thresholds may be changed after Phase86. |
| P86_COST_CLEARANCE | A candidate must have positive after-cost net P&L and precision_cost_clear >= 0.55 on both train and test. | train_pass=1 and test_pass=1 |
| P86_BREADTH | A candidate must trade at least 1000 bars in train and 1000 bars in test, with at least 20 symbols represented. | train_trades>=1000; test_trades>=1000; train_symbols>=20; test_symbols>=20 |
| P86_MONTH_STABILITY | At least 4/6 test months must be after-cost positive, and no single month may contribute more than 50% of total test net P&L. | test_positive_months>=4 and max_month_contribution_abs<=0.50 |
| P86_COST_DRAG | Cost drag divided by absolute gross P&L must be <= 0.60 on test. | test_cost_drag_to_abs_gross_ratio<=0.60 |
| P86_RETIREMENT | If no precommitted family passes, retire this composite family class rather than widening thresholds in the same run. | No in-run threshold widening allowed |

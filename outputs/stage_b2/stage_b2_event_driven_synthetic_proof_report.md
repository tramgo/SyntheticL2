# Stage B2 Event-Driven Synthetic Proof

Generated UTC: 2026-07-14T16:58:21.312725+00:00

## Scope

This proof uses the Stage B1 development subset, selects 5 normal days, 2 trend days and 1 shock day, and emits raw/event-driven synthetic proof datasets.
It emits 1-second/event-driven rows only where measured readiness supports that horizon. It does not claim dense 1-second support and must not be used to accept or reject S01-S11 profitability.

## Criteria

| criterion_id | criterion_description | acceptance_threshold | current_status |
| --- | --- | --- | --- |
| development_subset | Use the same five-instrument Stage B1 development subset, including at least one ETF. | 5 symbols and ETF count >= 1 | proof_check_not_strategy_acceptance |
| scenario_selection | Select 5 normal days, 2 explicit trend days and 1 explicit shock day. | normal_days == 5, trend_days == 2, shock_days == 1 | proof_check_not_strategy_acceptance |
| raw_event_dataset | Emit raw synthetic event rows for the selected symbols/days. | raw_event_rows > 0 | proof_check_not_strategy_acceptance |
| event_feature_dataset | Emit event-driven feature rows from received synthetic feed observations. | event_feature_rows > 0 | proof_check_not_strategy_acceptance |
| one_second_scope | Emit 1-second/event-driven feature rows only for symbols/windows supported by measured readiness. | all 1s symbols have event_driven_1s_ready == true | proof_check_not_strategy_acceptance |
| no_dense_1s_overclaim | Do not claim dense 1-second readiness where measured coverage does not support it. | dense_1s_claim_rows == 0 | proof_check_not_strategy_acceptance |
| deterministic_replay_storage | Persist deterministic proof outputs with manifest and stable row counts. | dataset rows stable and manifest records inputs/outputs | proof_check_not_strategy_acceptance |

## Development Readiness

| symbol | instrument_class | window_name | rows | event_rate_per_second | coverage_fraction | forward_fill_fraction | median_gap_ms | p95_gap_ms | dense_1s_ready | event_driven_1s_ready | readiness_status | stage_b2_1s_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BHARTIARTL | equity | open_0915_0920 | 350 | 1.1666666666666667 | 0.6266666666666667 | 0.3733333333333333 | 500.0 | 4175.799999999995 | False | True | event_driven_1s_ready | emit_event_driven_1s_features |
| ADANIPORTS | equity | open_0915_0920 | 211 | 0.7033333333333334 | 0.42 | 0.5800000000000001 | 636.5 | 6214.749999999985 | False | False | not_1s_ready | exclude_from_1s_features_due_to_measured_readiness |
| AXISBANK | equity | open_0915_0920 | 203 | 0.6766666666666666 | 0.4133333333333333 | 0.5866666666666667 | 749.0 | 7664.349999999997 | False | False | not_1s_ready | exclude_from_1s_features_due_to_measured_readiness |
| BAJAJ-AUTO | equity | open_0915_0920 | 191 | 0.6366666666666667 | 0.4066666666666667 | 0.5933333333333333 | 750.0 | 7588.399999999994 | False | False | not_1s_ready | exclude_from_1s_features_due_to_measured_readiness |
| BANKBEES | etf | open_0915_0920 | 56 | 0.1866666666666666 | 0.1833333333333333 | 0.8166666666666667 | 5072.0 | 9931.4 | False | False | not_1s_ready | exclude_from_1s_features_due_to_measured_readiness |

## Scenario Selection

| stage_b2_bucket | scenario_day | trade_date | quarter_profile | regime_code | regime_family | is_market_shock_day | event_rate_multiplier | spread_multiplier | depth_multiplier | evidence_label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| normal | 4 | 2026-07-17 | Q-A | D01 | Normal balanced | False | 1.0 | 1.0 | 1.0 | synthetic_scenario_design |
| normal | 8 | 2026-07-23 | Q-A | D01 | Normal balanced | False | 1.0 | 1.0 | 1.0 | synthetic_scenario_design |
| normal | 19 | 2026-08-07 | Q-A | D01 | Normal balanced | False | 1.0 | 1.0 | 1.0 | synthetic_scenario_design |
| normal | 21 | 2026-08-11 | Q-A | D01 | Normal balanced | False | 1.0 | 1.0 | 1.0 | synthetic_scenario_design |
| normal | 24 | 2026-08-14 | Q-A | D01 | Normal balanced | False | 1.0 | 1.0 | 1.0 | synthetic_scenario_design |
| shock | 2 | 2026-07-15 | Q-A | D12 | Event day | True | 1.35 | 1.25 | 0.85 | synthetic_scenario_design |
| trend | 1 | 2026-07-14 | Q-A | D04 | Gradual bullish trend | False | 1.1 | 1.0 | 1.0 | synthetic_scenario_design |
| trend | 10 | 2026-07-27 | Q-A | D04 | Gradual bullish trend | False | 1.1 | 1.0 | 1.0 | synthetic_scenario_design |

## Dataset Summary

| metric | value | description |
| --- | --- | --- |
| selected_symbols | 5 | same five-symbol development subset |
| selected_scenario_days | 8 | 5 normal + 2 trend + 1 shock |
| normal_days | 5 | normal scenario days |
| trend_days | 2 | explicit trend scenario days |
| shock_days | 1 | explicit shock scenario days |
| raw_event_rows | 15061 | raw synthetic event subset rows |
| event_feature_rows | 14952 | event-driven received-feed feature rows |
| event_driven_1s_ready_symbols | 1 | symbols eligible for event-driven 1s features |
| dense_1s_ready_symbols | 0 | symbols eligible for dense 1s features |
| one_second_event_feature_rows | 2400 | event-driven 1s proof rows |

## Proof Checks

| check_id | observed_value | expected_value | passed | detail | acceptance_scope |
| --- | --- | --- | --- | --- | --- |
| development_subset | 5 | 5 | True | etf_count=1 | stage_b2_event_driven_proof_not_strategy_profitability |
| scenario_selection | 1 | 1 | True | bucket_counts={'normal': 5, 'trend': 2, 'shock': 1} | stage_b2_event_driven_proof_not_strategy_profitability |
| raw_event_dataset | 15061 | 1 | True | raw Phase 9 Tier A events selected for Stage B2 symbols/days | stage_b2_event_driven_proof_not_strategy_profitability |
| event_feature_dataset | 14952 | 1 | True | received-feed event features built from Phase 8 observations | stage_b2_event_driven_proof_not_strategy_profitability |
| one_second_scope | 0 | 0 | True | one_second_symbols=['BHARTIARTL']; ready_symbols=['BHARTIARTL'] | stage_b2_event_driven_proof_not_strategy_profitability |
| no_dense_1s_overclaim | 0 | 0 | True | Stage B2 only emits event-driven 1s rows, not dense 1s claims | stage_b2_event_driven_proof_not_strategy_profitability |
| deterministic_replay_storage | 32413 | 1 | True | parquet datasets plus csv ledgers and manifest | stage_b2_event_driven_proof_not_strategy_profitability |

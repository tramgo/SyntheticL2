# Stage B1 Received-Tick Structural Synthetic Proof

Generated UTC: 2026-07-14T16:46:49.166281+00:00

## Scope

This proof selects a five-instrument development subset, including one ETF, and validates structural L2 book properties on current synthetic five-minute book states.
It is a generator-engineering proof only. It must not be used to accept or reject S01-S11 profitability.

## Criteria

| criterion_id | criterion_description | acceptance_threshold | current_status |
| --- | --- | --- | --- |
| development_subset | Five instruments are included with at least one ETF. | 5 symbols and ETF count >= 1 | proof_check_not_strategy_acceptance |
| scenario_coverage | Five normal/non-shock days plus explicit trend and shock scenarios are present. | normal_days >= 5 and trend_days >= 1 and shock_days >= 1 | proof_check_not_strategy_acceptance |
| five_level_book | Five-level bid/ask prices, quantities and order counts are present. | L1-L5 price/quantity/order columns present | proof_check_not_strategy_acceptance |
| cadence_not_finer_than_evidence | Synthetic proof cadence is no finer than validated real evidence used for this stage. | 5-minute synthetic book cadence is coarser than measured real tick cadence | proof_check_not_strategy_acceptance |
| price_grid | Bid/ask prices align to each symbol tick grid. | off-grid rows == 0 | proof_check_not_strategy_acceptance |
| spread_and_depth_ordering | Books have positive spreads and monotonic depth price ordering. | crossed/negative-spread/order-error rows == 0 | proof_check_not_strategy_acceptance |
| deterministic_replay_storage | Proof is deterministic and storage is compact parquet/csv with manifest. | row counts stable and manifest records inputs/outputs | proof_check_not_strategy_acceptance |

## Development Subset

| symbol | instrument_class | row_count | event_rate_per_second | median_interarrival_ms | p95_interarrival_ms | stale_gap_gt_15s_count | stage_b1_selected | selection_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADANIPORTS | equity | 13886 | 0.6088482941308139 | 1000.0 | 5500.0 | 2 | True | liquid_equity_development_subset |
| AXISBANK | equity | 18309 | 0.803904475652219 | 749.0 | 4913.649999999998 | 2 | True | liquid_equity_development_subset |
| BAJAJ-AUTO | equity | 25141 | 1.1038618480081333 | 741.0 | 4410.049999999999 | 2 | True | liquid_equity_development_subset |
| BHARTIARTL | equity | 19560 | 0.8576316169666368 | 749.0 | 4762.399999999994 | 2 | True | liquid_equity_development_subset |
| BANKBEES | etf | 18916 | 0.8379597726150352 | 1000.0 | 4833.0 | 2 | True | required_etf_in_development_subset |

## Scenario Coverage

| coverage_bucket | scenario_days | l2_rows | passes_stage_b1_requirement |
| --- | --- | --- | --- |
| non_shock_normal_or_reference_days | 164 | 69750 | True |
| explicit_trend_days | 44 | 16500 | True |
| explicit_shock_days | 25 | 9375 | True |

## Structural Checks

| check_id | observed_value | expected_value | passed | detail | acceptance_scope |
| --- | --- | --- | --- | --- | --- |
| development_subset | 5 | 5 | True | symbols=ADANIPORTS,AXISBANK,BAJAJ-AUTO,BANKBEES,BHARTIARTL; etf_count=1 | stage_b1_structural_proof_not_strategy_profitability |
| scenario_coverage | 3 | 3 | True | normal/trend/shock coverage buckets | stage_b1_structural_proof_not_strategy_profitability |
| five_level_book | 0 | 0 | True | missing_columns= | stage_b1_structural_proof_not_strategy_profitability |
| cadence_not_finer_than_evidence | 5 | 5 | True | Phase 6 proof uses 5-minute bars, coarser than measured real tick cadence | stage_b1_structural_proof_not_strategy_profitability |
| price_grid | 0 | 0 | True | all L1-L5 prices checked against symbol tick_size | stage_b1_structural_proof_not_strategy_profitability |
| spread_and_depth_ordering | 0 | 0 | True | crossed=0; nonpositive_spread=0; bid_order_errors=0; ask_order_errors=0; nonpositive_qty=0 | stage_b1_structural_proof_not_strategy_profitability |
| deterministic_replay_storage | 70875 | 1 | True | subset rows written as compact parquet plus csv ledgers and manifest | stage_b1_structural_proof_not_strategy_profitability |

# Phase163 Synthetic-only Replay Preflight

Generated UTC: 2026-07-23T10:43:06.379173+00:00

Phase163 decides whether the Phase162 full-year generated L2 lake can be used for guarded synthetic-only replay diagnostics.
It opens only synthetic-only replay execution for the next phase. It does not run P&L replay itself, does not promote strategies, and keeps broker/paper/live acceptance closed.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase163_required_gate_rows | 8 | Required synthetic-only replay preflight gates |
| phase163_required_gate_pass_rows | 8 | Required preflight gates passed |
| phase163_synthetic_only_replay_preflight_pass | 1 | 1 means guarded synthetic-only replay may be implemented next |
| phase163_synthetic_only_replay_execution_allowed | 1 | 1 means Phase164 synthetic-only replay execution may open |
| phase163_phase162_months | 12 | Phase162 months available |
| phase163_phase162_dense_rows | 192786816 | Phase162 dense rows available |
| phase163_phase162_dense_bytes | 4141341739 | Phase162 dense bytes available |
| phase163_work_queue_rows | 11 | Rows in Phase163 replay work queue |
| phase163_alpha_replay_allowed_rows | 9 | Alpha strategy rows allowed for synthetic-only replay diagnostics |
| phase163_control_replay_allowed_rows | 2 | Control/risk-plumbing rows allowed only as diagnostics |
| phase163_blocklisted_family_rows | 7 | Phase116 blocklisted family rows enforced |
| phase163_strategy_promotion_allowed | 0 | Strategy promotion remains closed |
| phase163_paper_or_live_acceptance_allowed | 0 | Broker/paper/live acceptance remains closed |
| phase163_azure_read_policy | forbidden_for_analysis_download_first_then_local | No direct Python Azure scanning for replay inputs |
| phase163_next_best_action | implement_phase164_synthetic_only_full_year_replay_on_phase162_data | Recommended next milestone |

## Preflight Gate Ledger

| gate_id | gate_group | required_for_replay_execution | observed_value | passed | failure_action |
| --- | --- | --- | --- | --- | --- |
| phase162_full_year_materialization_passed | realism_materialization | True | 1 | True | Rerun/fix Phase162 before any synthetic-only replay execution. |
| phase162_full_year_scope_complete | realism_materialization | True | months=12; symbols=32; missing_shards=0 | True | Complete all month/symbol shards before replay. |
| phase162_dense_parquet_root_present | local_storage | True | root=raw_synthetic_l2_phase162_distributional_full_year; parquet_files=384; expected_files=384 | True | Regenerate or restore the local Phase162 dense parquet lake. |
| phase39_synthetic_only_experiment_policy_open | synthetic_only_policy | True | True | True | Revisit Phase39 synthetic-only acceptance path before replay. |
| broker_paper_live_acceptance_remains_closed | broker_boundary | True | False | True | Do not run this preflight if it would imply broker/paper/live readiness. |
| strategy_promotion_still_not_open | promotion_boundary | True | False | True | Separate replay diagnostics from promotion/acceptance claims. |
| phase116_blocklist_present_and_enforced | blocklist | True | blocked_families=7 | True | Do not open replay until closed strategy families can be excluded. |
| phase136_deep_book_branch_closed | blocklist | True | A_CLEAN_FALSIFICATION | True | Do not reopen the closed top-five-depth passive branch inside this replay. |

## Phase164 Replay Contract

| contract_id | contract_status | input_dense_root | input_inventory | allowed_scope | allowed_strategy_rows | control_rows | excluded_blocklist_rows | required_cost_model | required_execution_profiles | required_outputs | forbidden_outputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P164_SYNTHETIC_ONLY_FULL_YEAR_REPLAY | open_for_implementation | raw_synthetic_l2_phase162_distributional_full_year | outputs\phase162\phase162_dense_full_year_inventory.csv | synthetic_only_replay_diagnostics | 9 | 2 | 7 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14_or_successor_with_documented_components | zero_latency_control;retail_marketable_default;stressed_retail | trade_ledger;daily_symbol_summary;strategy_profile_summary;risk_summary;acceptance_summary;manifest | broker_acceptance;paper_live_readiness;contract_note_reconciliation_claim;promoted_buy_sell_signal;deployable_profitability_claim |

## Replay Work Queue

| priority | strategy_id | strategy_name | experiment_track | phase163_synthetic_only_replay_allowed | phase163_replay_status | must_not_claim | phase162_input_root | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S01 | Momentum/breakout filtered by MLOFI | alpha_redesign_diagnostics | True | allowed_for_synthetic_only_replay_diagnostics | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation; strategy_promotion | raw_synthetic_l2_phase162_distributional_full_year | May run in Phase164 synthetic-only replay diagnostics on Phase162 data; do not reuse retired dense marketable rules and do not claim broker/paper/live readiness. |
| 2 | S02 | Pure multi-level OFI directional model | alpha_redesign_diagnostics | True | allowed_for_synthetic_only_replay_diagnostics | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation; strategy_promotion | raw_synthetic_l2_phase162_distributional_full_year | May run in Phase164 synthetic-only replay diagnostics on Phase162 data; do not reuse retired dense marketable rules and do not claim broker/paper/live readiness. |
| 3 | S03 | Liquidity-vacuum breakout | alpha_redesign_diagnostics | True | allowed_for_synthetic_only_replay_diagnostics | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation; strategy_promotion | raw_synthetic_l2_phase162_distributional_full_year | May run in Phase164 synthetic-only replay diagnostics on Phase162 data; do not reuse retired dense marketable rules and do not claim broker/paper/live readiness. |
| 4 | S04 | Trade-flow plus depth confirmation | alpha_redesign_diagnostics | True | allowed_for_synthetic_only_replay_diagnostics | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation; strategy_promotion | raw_synthetic_l2_phase162_distributional_full_year | May run in Phase164 synthetic-only replay diagnostics on Phase162 data; do not reuse retired dense marketable rules and do not claim broker/paper/live readiness. |
| 5 | S05 | Microprice entry/exit filter | alpha_redesign_diagnostics | True | allowed_for_synthetic_only_replay_diagnostics | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation; strategy_promotion | raw_synthetic_l2_phase162_distributional_full_year | May run in Phase164 synthetic-only replay diagnostics on Phase162 data; do not reuse retired dense marketable rules and do not claim broker/paper/live readiness. |
| 6 | S06 | Absorption and exhaustion reversal | alpha_redesign_diagnostics | True | allowed_for_synthetic_only_replay_diagnostics | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation; strategy_promotion | raw_synthetic_l2_phase162_distributional_full_year | May run in Phase164 synthetic-only replay diagnostics on Phase162 data; do not reuse retired dense marketable rules and do not claim broker/paper/live readiness. |
| 7 | S07 | Mean reversion after imbalance | alpha_redesign_diagnostics | True | allowed_for_synthetic_only_replay_diagnostics | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation; strategy_promotion | raw_synthetic_l2_phase162_distributional_full_year | May run in Phase164 synthetic-only replay diagnostics on Phase162 data; do not reuse retired dense marketable rules and do not claim broker/paper/live readiness. |
| 8 | S08 | Cross-ticker/index lead-lag OFI | alpha_redesign_diagnostics | True | allowed_for_synthetic_only_replay_diagnostics | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation; strategy_promotion | raw_synthetic_l2_phase162_distributional_full_year | May run in Phase164 synthetic-only replay diagnostics on Phase162 data; do not reuse retired dense marketable rules and do not claim broker/paper/live readiness. |
| 9 | S09 | Pure queue-imbalance scalping | alpha_redesign_diagnostics | True | allowed_for_synthetic_only_replay_diagnostics | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation; strategy_promotion | raw_synthetic_l2_phase162_distributional_full_year | May run in Phase164 synthetic-only replay diagnostics on Phase162 data; do not reuse retired dense marketable rules and do not claim broker/paper/live readiness. |
| 10 | S10 | Passive market making | control_risk_plumbing | True | allowed_as_control_or_risk_plumbing_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation; strategy_promotion | raw_synthetic_l2_phase162_distributional_full_year | May run only as a control/risk-plumbing diagnostic; exclude from alpha promotion. |
| 11 | S11 | Spoof-like wall filter | control_risk_plumbing | True | allowed_as_control_or_risk_plumbing_only | paper_or_live_acceptance; broker_fill_quality; contract_note_cost_reconciliation; strategy_promotion | raw_synthetic_l2_phase162_distributional_full_year | May run only as a control/risk-plumbing diagnostic; exclude from alpha promotion. |

## Blocklist Exclusion Ledger

| blocked_family_id | blocked_strategy_ids | same_shard_continuation_allowed | unlock_condition | phase163_replay_status | phase163_reason |
| --- | --- | --- | --- | --- | --- |
| DENSE_L1_IMBALANCE_MARKETABLE | DENSE_S01_L1_IMBALANCE | False | new precommitted non-taker or materially different feature class plus train/test/month gates | excluded_from_phase163_phase164_replay | Phase52 dense replay found negative annual net P&L in every execution profile. |
| DENSE_MICROPRICE_MARKETABLE | DENSE_S02_MICROPRICE | False | new precommitted non-taker or materially different feature class plus train/test/month gates | excluded_from_phase163_phase164_replay | Phase52 dense replay found negative annual net P&L in every execution profile. |
| DENSE_ONE_TICK_MOMENTUM_MARKETABLE | DENSE_S03_1T_MOMENTUM | False | new precommitted non-taker or materially different feature class plus train/test/month gates | excluded_from_phase163_phase164_replay | Phase52 dense replay found negative annual net P&L in every execution profile. |
| HDFCBANK_LEAD_LAG | phase77_phase82_phase84_hdfcbank_rechecks | False | only a newly specified cross-symbol feature may include HDFCBANK; do not rerun the retired rule | excluded_from_phase163_phase164_replay | Disjoint and cached stratified HDFCBANK retests produced zero pass months/zero accepted survivor. |
| CROSS_SYMBOL_IMBALANCE_CURRENT_RULES | P90_MARKET_IMBALANCE_CONTINUATION;P90_SECTOR_IMBALANCE_CONTINUATION;P90_SYMBOL_SECTOR_DIVERGENCE_REVERSION | False | redesign features and precommit new gates before replay | excluded_from_phase163_phase164_replay | Phase91 found positive pockets but zero candidate pass rows. |
| LOW_TURNOVER_EVENT_WINDOW_CURRENT_RULES | P92_SHOCK_CONTINUATION;P92_BOOK_DISLOCATION_REVERSAL;P92_SHOCK_EXHAUSTION_REVERSAL | False | new event-window hypothesis with stronger gross edge over retail costs | excluded_from_phase163_phase164_replay | Phase93 found positive pockets but zero candidate pass rows. |
| DEEP_BOOK_LABEL_LIFT | phase131_phase132_top_five_depth_feature_diagnostics | False | real Zerodha L2 anchor data through Phase113-115, or an externally precommitted research plan outside the synthetic-only top-five-depth passive branch | excluded_from_phase163_phase164_replay | Phase132 top-five-depth feature diagnostics found zero labels where Phase131 features beat the Phase130 top-of-book/context baseline by the precommitted Brier margin. |

## Historical Dense Replay Context

| metric | value | description | phase163_use |
| --- | --- | --- | --- |
| phase52_dense_replay_shards_scanned | 384 | Dense parquet shards scanned | historical_falsification_context_only_not_replay_input |
| phase52_dense_replay_strategy_profile_rows | 9 | Strategy/profile result rows | historical_falsification_context_only_not_replay_input |
| phase52_dense_replay_trade_rows | 797029565 | Aggregated dense tick trade count | historical_falsification_context_only_not_replay_input |
| phase52_positive_after_cost_rows | 0 | Strategy/profile rows positive after costs | historical_falsification_context_only_not_replay_input |
| phase52_dense_replay_candidate_rows | 0 | Rows passing positive and proxy-risk screens | historical_falsification_context_only_not_replay_input |
| phase52_elapsed_seconds | 90525.24089789999 | Replay elapsed seconds | historical_falsification_context_only_not_replay_input |
| phase52_dense_output_root | raw_synthetic_l2_dense_full_year | Dense input lake root | historical_falsification_context_only_not_replay_input |
| phase52_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha cost model used for charge bps | historical_falsification_context_only_not_replay_input |
| phase52_synthetic_full_year_acceptance_ready | 0 | Dense replay is synthetic-only proxy evidence, not broker/real acceptance | historical_falsification_context_only_not_replay_input |

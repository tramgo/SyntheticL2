# Phase74 Generator and Alignment Remediation Plan

Generated UTC: 2026-07-19T19:56:58.766705+00:00

Phase74 turns the Phase73 audit into implementation requirements.
It keeps replay expansion closed until timestamp alignment, shock-panel balance and cost-drag gates are remediated.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase74_source_phase73_allow_replay_expansion | 0 | Phase73 replay-expansion gate |
| phase74_remediation_actions | 4 | Concrete remediation actions declared |
| phase74_retest_queue_items | 2 | Near-miss retests queued behind remediation gates |
| phase74_allow_replay_expansion_now | 0 | 0 means no near-miss replay expansion before remediation gates pass |
| phase74_next_implementation | timestamp_unit_contract_and_synchronous_matrix_validator | Next implementation step |
| phase74_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model retained for future gates |

## Remediation Action Plan

| priority | remediation_id | area | issue | required_change | acceptance_gate | unblocks |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | R74_timestamp_unit_contract | timestamp_alignment | Dense lake column callback_received_utc_ms behaves like seconds in generated data despite the _ms suffix. | Add a timestamp unit contract artifact and validator that reports observed min/max deltas and names the alignment unit used by every cross-symbol study. | Timestamp unit inferred consistently for every symbol partition in the target month; mismatches fail the run. | Reliable cross-symbol alignment and replay comparability. |
| 2 | R74_synchronous_cross_symbol_bars | cross_symbol_alignment | Phase70 used per-symbol event bars; Phase73 timestamp recheck stayed positive but failed precision. | Build a reusable timestamp-aligned matrix with coverage/staleness diagnostics and target-side tradability filters. | At least 95% of selected symbol/bucket cells have fresh observations within the declared staleness limit. | A cleaner HDFCBANK lead-lag refinement without sequence-alignment ambiguity. |
| 3 | R74_shock_panel_balance | shock_scenarios | Phase73 found shock coverage concentrated in one audited month. | Create or select a scenario-balanced shock panel with multiple market-shock and symbol-shock months before replaying shock rules. | At least two market-shock months and at least two symbol-shock months with two or more shocked symbols each. | Retesting Phase71 shock mean-reversion without one-scenario concentration. |
| 4 | R74_cost_drag_filter | execution_costs | Positive near-misses still lose too much gross edge to costs or fail precision gates. | Add pre-trade filters that reject candidate rules where validation cost drag exceeds 50% of absolute gross edge. | Every promoted candidate reports gross edge, cost drag, precision and target/month stability before replay. | Prevents expensive replay of rules that are technically positive but operationally fragile. |

## Near-Miss Retest Queue

| retest_id | source_near_miss | allowed_after | experiment | not_allowed_yet |
| --- | --- | --- | --- | --- |
| RT74_hdfcbank_timestamp_refinement | NM70_HDFCBANK_LEAD_LAG | R74_timestamp_unit_contract,R74_synchronous_cross_symbol_bars,R74_cost_drag_filter | Refine HDFCBANK lead-lag with timestamp bars, staleness filtering, lower-turnover thresholds and disjoint-month validation. | No direct full-year replay from Phase70/73 because precision is below gate. |
| RT74_market_shock_mean_reversion | NM71_MARKET_SHOCK_MEAN_REVERSION | R74_shock_panel_balance,R74_cost_drag_filter | Retest market-shock mean reversion on a balanced shock panel with enough trade count and matched no-shock controls. | No direct replay from Phase71 because trade count was below the predeclared minimum. |

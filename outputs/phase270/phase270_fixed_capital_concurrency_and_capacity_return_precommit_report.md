# Phase270 Fixed-capital Concurrency and Capacity Return Precommit

Generated UTC: 2026-08-02T02:50:30.921987+00:00

Phase270 precommits the capital-aware return model required after Phase269 preserved fixed-notional annualized research leads.
The purpose is to prevent fixed-notional annualized proxies from being mistaken for portfolio annual return.
Full Zerodha top-five market-by-price rows 1-5 and levels 2-5 remain mandatory; L1-only candidates remain forbidden.
This is not replay execution, strategy promotion, paper/live acceptance, or a deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase270_fixed_capital_precommit_complete | 1 | Phase270 fixed-capital/concurrency/capacity precommit completed |
| phase270_selected_route | P270_FIXED_CAPITAL_CONCURRENCY_AND_CAPACITY_RETURN_MODEL | Selected route |
| phase270_phase269_interpretation_complete | 1 | Phase269 interpretation complete |
| phase270_phase269_research_leads_preserved | 1 | Phase269 preserved research leads |
| phase270_phase269_do_not_claim_portfolio_annual_return | 1 | Portfolio annual return claim forbidden |
| phase270_phase269_do_not_promote_or_replay | 1 | Replay/promotion forbidden |
| phase270_capital_model_contract_rows | 8 | Capital model contract rows |
| phase270_concurrency_capacity_contract_rows | 8 | Concurrency/capacity contract rows |
| phase270_candidate_input_contract_rows | 5 | Candidate input contract rows |
| phase270_return_output_contract_rows | 5 | Return output contract rows |
| phase270_control_contract_rows | 8 | Control contract rows |
| phase270_full_top_five_depth_required | 1 | Zerodha rows 1-5 required |
| phase270_levels_2_to_5_materiality_required | 1 | Levels 2-5 materiality required |
| phase270_l1_only_candidate_allowed | 0 | L1-only candidates forbidden |
| phase270_unlimited_capital_assumption_allowed | 0 | Unlimited capital assumption forbidden |
| phase270_portfolio_return_claim_without_scheduler_allowed | 0 | Portfolio return claim without scheduler forbidden |
| phase270_fixed_notional_proxy_as_portfolio_return_allowed | 0 | Fixed-notional proxy cannot be relabeled portfolio return |
| phase270_hard_gate_pass_rows | 13 | Hard gates passed |
| phase270_hard_gate_rows | 13 | Hard gates evaluated |
| phase270_download_more_dates_now_allowed | 0 | No new download in Phase270 |
| phase270_replay_execution_allowed_now | 0 | No replay execution in Phase270 |
| phase270_strategy_promotion_allowed | 0 | No strategy promotion from Phase270 |
| phase270_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase270 |
| phase270_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase270 |
| phase270_next_best_action | run_phase271_fixed_capital_concurrency_and_capacity_return_analysis_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P270_PHASE269_WORK_ORDER_PRESENT | True | run_phase270_fixed_capital_concurrency_and_capacity_return_precommit_no_paper_live | Phase269 next action targets Phase270 | hard |
| P270_PHASE269_ROUTE_SELECTED | True | P269_FIXED_CAPITAL_CONCURRENCY_AND_CAPACITY_RETURN_PRECOMMIT | Phase269 selected fixed-capital route | hard |
| P270_PHASE269_FORBIDS_PORTFOLIO_CLAIM | True | 1 | Phase269 forbids portfolio-return claim | hard |
| P270_PHASE269_FORBIDS_REPLAY | True | 1 | Phase269 forbids replay/promotion | hard |
| P270_PHASE269_FULL_DEPTH_RECOGNIZED | True | full_depth=1200;l2_l5=1200;l1_only=0;variants=1200 | Full-depth Phase268 evidence recognized | hard |
| P270_PHASE269_CAPITAL_CONTRACT_PRESENT | True | 1 | Phase269 next route contains capital accounting | hard |
| P270_PHASE269_CAPACITY_CONTRACT_PRESENT | True | 1 | Phase269 next route contains capacity accounting | hard |
| P270_CAPITAL_MODEL_CONTRACT_WRITTEN | True | 8 | Capital model contract rows written | hard |
| P270_CONCURRENCY_CAPACITY_CONTRACT_WRITTEN | True | 8 | Concurrency/capacity rows written | hard |
| P270_INPUT_CONTRACT_WRITTEN | True | 5 | Input contract rows written | hard |
| P270_OUTPUT_CONTRACT_WRITTEN | True | 5 | Phase271 output contract rows written | hard |
| P270_CONTROLS_WRITTEN | True | 8 | Required and forbidden controls written | hard |
| P270_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

## Capital Model Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| initial_capital_inr | 100000;250000;500000;1000000 | Evaluate fixed starting capital scenarios instead of unlimited capital. |
| per_trade_notional_policy | min(fixed_notional, available_cash / open_slot_count) | Each event consumes capital; no order may exceed available capital. |
| fixed_notional_grid_inr | 25000;50000;100000 | Stress the Phase268 fixed-notional proxy under smaller and equal notionals. |
| max_concurrent_positions | 1;2;4;8 | Cap simultaneous exposure; overlapping events must compete for capital. |
| capital_reuse_rule | capital_released_after_horizon_exit | Capital is not reusable until the event horizon exits. |
| cash_drag_rule | idle_cash_return_zero_intraday | Unused cash earns zero intraday return. |
| portfolio_return_formula | realized_net_pnl_inr / initial_capital_inr | Only this capital-accounted formula may be called portfolio return. |
| annualized_portfolio_return_formula | portfolio_return_over_observed_dates * 252 / observed_trade_dates | Annualize only after fixed-capital event scheduling is materialized. |

## Concurrency and Capacity Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| event_time_key | trade_date;exchange;symbol;richer_event_bar_id;horizon | Event scheduling key for capital locks. |
| position_exit_key | richer_event_bar_id + horizon | Capital is released after the modeled holding horizon. |
| same_symbol_overlap_policy | keep_highest_ranked_event_when_capital_or_overlap_conflict | Avoid stacking contradictory events in the same symbol/window. |
| cross_symbol_concurrency_policy | rank_by_research_lead_score_then_allocate_until_cash_or_slot_limit | Allocate limited capital to ranked research leads. |
| capacity_proxy | event_count;symbol_count;notional_turnover;cost_stress;depth_quantity_context | Small-event leads must pass capacity diagnostics. |
| turnover_limit_diagnostic | daily_notional_turnover / initial_capital | Record turnover pressure before acceptance. |
| slippage_sensitivity | base_cost;1p5x_cost;2x_cost;additional_1bp;additional_2bp | Capacity analysis must include extra slippage stress. |
| minimum_observed_dates_for_claim | >=1_current_data_for_mechanics;>=5_future_for_portfolio_claim | One-date current data can test mechanics, not robust annual portfolio claims. |

## Candidate Input Contract

| input_id | path | description |
| --- | --- | --- |
| ranked_research_leads | outputs/phase269/phase269_ranked_annualized_research_leads.csv | Use the 17 fixed-notional annualized research leads. |
| variant_results | outputs/phase268/phase268_two_lane_variant_results.csv | Use all Phase268 variants for controls and fallback ranking. |
| exploratory_event_ledger | outputs/phase268/phase268_exploratory_event_ledger.csv | Use event-level rows for scheduling and capital locks. |
| acceptance_event_ledger | outputs/phase268/phase268_acceptance_event_ledger.csv | Expected empty until acceptance-grade candidates appear. |
| full_depth_source_surface | outputs/phase254/phase254_richer_raw_top5_depth_event_bars.parquet | Full top-five event-bar source remains the underlying signal surface. |

## Return Output Contract

| output_id | planned_path | description |
| --- | --- | --- |
| capital_scenario_results | phase271_capital_scenario_results.csv | Portfolio return, drawdown, turnover and utilization by capital/concurrency scenario. |
| scheduled_event_ledger | phase271_scheduled_event_ledger.csv | Event-level capital allocation and rejection reasons. |
| candidate_capacity_diagnostics | phase271_candidate_capacity_diagnostics.csv | Capacity, turnover and slippage diagnostics by candidate family. |
| annualized_proxy_reconciliation | phase271_annualized_proxy_reconciliation.csv | Compare fixed-notional proxy vs capital-accounted return. |
| acceptance_summary | phase271_acceptance_summary.csv | No replay/promotion unless capital model passes gates. |

## Control Contract

| control_id | control_status | description |
| --- | --- | --- |
| full_top_five_depth_required | required | Rows 1-5 remain mandatory for every included signal. |
| levels_2_to_5_materiality_required | required | L2-L5 materiality remains mandatory. |
| l1_only_candidate_allowed | forbidden | No L1-only candidate or capital analysis is allowed. |
| unlimited_capital_assumption | forbidden | Capital-aware return cannot assume unlimited simultaneous capital. |
| portfolio_return_claim_without_scheduler | forbidden | No portfolio return claim without event scheduling and capital locks. |
| fixed_notional_proxy_as_portfolio_return | forbidden | Phase268 annualized proxy cannot be relabeled as portfolio return. |
| paper_live_or_deployable_profitability_claim | forbidden | No paper/live or deployable profitability claim in Phase270/271. |
| replay_execution_now | forbidden | Phase270 is a precommit only. |

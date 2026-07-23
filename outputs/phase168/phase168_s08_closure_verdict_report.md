# Phase168 S08 Closure Verdict

Generated UTC: 2026-07-23T15:53:28.403665+00:00

Phase168 converts the Phase167 S08 full-year replay into a closure/blocklist decision.
It does not run a new strategy, does not promote a signal, and does not claim paper/live or deployable readiness.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase168_outcome | A_S08_CURRENT_FORM_FALSIFIED | Selected Phase168 outcome |
| phase168_decision | close_s08_current_cross_symbol_lead_lag_form | S08 current-form decision |
| phase168_closure_gates_passed | 10 | Closure gates passed |
| phase168_closure_gates_total | 10 | Closure gates evaluated |
| phase168_blocklist_rows | 1 | Blocklist-candidate rows emitted |
| phase168_best_annual_net_pnl_inr | -4.1439e+06 | Inherited best Phase167 annual net P&L |
| phase168_strategy_promotion_allowed | 0 | Strategy promotion remains closed |
| phase168_paper_or_live_acceptance_allowed | 0 | Paper/live broker acceptance remains closed |
| phase168_deployable_profitability_claim_allowed | 0 | Deployable claim remains closed |
| phase168_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Inherited Zerodha equity intraday NSE formula |
| phase168_next_best_action | design_new_precommitted_non_blocklisted_hypothesis_or_wait_for_real_l2_anchor | Recommended next milestone |

## Verdict

| verdict_id | outcome | decision | phase167_strategy_id | phase167_trade_rows | phase167_positive_after_cost_profile_rows | phase167_candidate_profile_rows | best_execution_profile | best_annual_net_pnl_inr | strategy_promotion_allowed | paper_or_live_acceptance_allowed | deployable_profitability_claim_allowed | next_best_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| phase168_s08_closure_verdict | A_S08_CURRENT_FORM_FALSIFIED | close_s08_current_cross_symbol_lead_lag_form | P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | 817814 | 0 | 0 | zero_latency_spread_only_control | -4.1439e+06 | 0 | 0 | 0 | design_new_precommitted_non_blocklisted_hypothesis_or_wait_for_real_l2_anchor |

## Closure Gate Evaluation

| gate_id | passed | observed_value | required_value | interpretation |
| --- | --- | --- | --- | --- |
| P168_PHASE166_CACHE_READY | True | 1 | 1 | S08 closure is based on a ready full-year Phase166 cache. |
| P168_FULL_YEAR_SCOPE | True | 12 | >=12 monthly cache files | Phase167 used the full local Phase166 cache scope. |
| P168_TRADE_LEDGER_PRESENT | True | 817814 | >0 trade rows | The S08 closure is based on actual replay trades, not a dry verdict. |
| P168_NO_POSITIVE_PROFILE_ROWS | True | 0 | 0 | No execution profile is positive after costs. |
| P168_NO_CANDIDATE_PROFILE_ROWS | True | 0 | 0 | No profile passes the positive, coverage, stability and precision gates. |
| P168_BEST_PROFILE_NEGATIVE | True | -4.1439e+06 | <0 INR annual net P&L | Even the best observed S08 profile is negative. |
| P168_ALL_PROFILE_GATES_FAIL | True | 1 | 1 | All Phase167 execution-profile gate rows fail. |
| P168_PROMOTION_BOUNDARY_CLOSED | True | 0 | 0 | S08 closure must not promote a strategy. |
| P168_BROKER_BOUNDARY_CLOSED | True | 0 | 0 | S08 closure must not claim broker/paper/live readiness. |
| P168_DEPLOYABLE_CLAIM_CLOSED | True | 0 | 0 | S08 closure must not make a deployable profitability claim. |

## Blocklist Candidate Update

| blocked_family_id | source_strategy_id | phase167_strategy_id | blocked_form | best_execution_profile | best_annual_net_pnl_inr | profile_rows | positive_after_cost_profile_rows | candidate_profile_rows | recommended_status | unlock_condition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PHASE167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | S08 | P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | fixed_score_threshold_0_42_market_sector_etf_lagged_depth_pressure_continuation | zero_latency_spread_only_control | -4.1439e+06 | 3 | 0 | 0 | block_current_phase167_s08_form | new precommitted feature form, different label/execution contract, or real-anchor evidence; do not rerun this same S08 form shard-after-shard hoping for profit |

## Phase167 Profile Summary

| strategy_id | source_strategy_id | feature_family | feature_status | execution_profile | trades | symbols | months | trade_dates | sum_gross_return | sum_cost_return | sum_net_return | mean_gross_return | mean_cost_return | mean_net_return | gross_pnl_inr | cost_pnl_drag_inr | annual_net_pnl_inr | worst_trade_pnl_inr | precision_cost_clear | mean_spread_bps | total_latency_buckets | fixed_slippage_ticks | internal_impact_bps | zerodha_charge_bps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | S08 | cross_symbol_lead_lag | precommitted_phase167_single_s08_branch | zero_latency_spread_only_control | 273062 | 5 | 12 | 252 | -0.00426301 | 41.4347 | -41.439 | -1.56119e-08 | 0.000151741 | -0.000151757 | -426.301 | 4.14347e+06 | -4.1439e+06 | -314.325 | 1.83109e-05 | 3.03482 | 0 | 0 | 0 | 0 |
| P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | S08 | cross_symbol_lead_lag | precommitted_phase167_single_s08_branch | retail_marketable_default | 272592 | 5 | 12 | 252 | 0.000954917 | 282.512 | -282.511 | 3.5031e-09 | 0.00103639 | -0.00103639 | 95.4917 | 2.82512e+07 | -2.82511e+07 | -402.857 | 1.10055e-05 | 3.03451 | 2 | 1 | 0.5 | 8.26812 |
| P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION | S08 | cross_symbol_lead_lag | precommitted_phase167_single_s08_branch | stressed_retail | 272160 | 5 | 12 | 252 | 0.000531413 | 325.026 | -325.025 | 1.95258e-09 | 0.00119425 | -0.00119424 | 53.1413 | 3.25026e+07 | -3.25025e+07 | -418.667 | 7.34862e-06 | 3.03447 | 4 | 2 | 2 | 8.26812 |

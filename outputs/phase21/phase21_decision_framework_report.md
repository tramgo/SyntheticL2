# Phase 21 Decision Framework

Generated UTC: 2026-07-14T17:30:07.691840+00:00

## Scope

This framework evaluates the plan's post-three-month decision table against current Stage D, Stage E, Phase 15 and Phase 16 evidence.
It is a decision ledger, not strategy-promotion evidence.

## Decision Summary

| metric | value | description |
| --- | --- | --- |
| decision_rules | 9 | Phase 21 decision rules evaluated |
| active_current_decisions | 1 | Rules currently determining the decision |
| extension_or_paper_ready | 0 | No current row permits full-year extension or real-data paper testing |
| current_decision | Improve or reject strategies; do not tune generator to create profit | Current Phase 21 decision |

## Decision Rules

| decision_rule_id | outcome_condition | plan_decision | rule_scope |
| --- | --- | --- | --- |
| D21_01_no_strategy_survives_costs_latency | No strategy survives costs and latency | Improve or reject strategies; do not tune generator to create profit | phase21_post_three_month_decision_framework |
| D21_02_only_price_baselines_work | Only price baselines work | L2 adds insufficient value under tested assumptions | phase21_post_three_month_decision_framework |
| D21_03_l2_improves_modestly_robustly | L2 improves baseline modestly and robustly | Continue collecting real data and extend synthetic testing | phase21_post_three_month_decision_framework |
| D21_04_strategy_works_one_regime | Strategy works only in one regime | Build explicit regime gate and test false-classification risk | phase21_post_three_month_decision_framework |
| D21_05_zero_latency_only | Strategy works only with zero latency | Reject for retail deployment | phase21_post_three_month_decision_framework |
| D21_06_optimistic_passive_only | Strategy works only with optimistic passive fills | Reject or redesign execution | phase21_post_three_month_decision_framework |
| D21_07_across_generators_seeds | Strategy works across generators/seeds | Candidate for real-data paper testing | phase21_post_three_month_decision_framework |
| D21_08_synthetic_not_real | Strategy works synthetically but not on accumulating real days | Treat as generator artifact and investigate | phase21_post_three_month_decision_framework |
| D21_09_wild_seed_variation | Results vary wildly by seed | Insufficient robustness or unstable scenario design | phase21_post_three_month_decision_framework |

## Current Decision Ledger

| decision_rule_id | current_condition_met | observed_value | current_decision | evidence_source | next_action | decision_status |
| --- | --- | --- | --- | --- | --- | --- |
| D21_01_no_strategy_survives_costs_latency | True | promoted=0; risk_adjusted_joint_pass_rows=0; retail_stress_positive_strategies=2 | Improve or reject strategies; do not tune generator to create profit | outputs\phase15\strategy_acceptance_summary.csv; outputs\phase16\risk_adjusted_economic_frontier.csv; outputs\phase16\economic_viability_frontier.csv | Clear acceptance blockers or reject/redesign strategies before any full-year extension. | active_current_decision |
| D21_02_only_price_baselines_work | False | Stage C baseline proxies exist, but current evidence does not prove price-only baselines are the only working models. | L2 adds insufficient value under tested assumptions | outputs\stage_c\stage_c_baseline_proxy_run_summary.csv | Compare acceptance-grade L2 and price-only baselines after full execution/holdout evidence exists. | not_proven_currently |
| D21_03_l2_improves_modestly_robustly | False | predictive_candidates=0; holdout_all_cell_pass=0; extension_allowed=False | Continue collecting real data and extend synthetic testing | outputs\phase16\predictive_promotion_falsification.csv; outputs\stage_e\stage_e_prerequisite_ledger.csv | Do not advance; predictive/holdout/full-year readiness criteria are not met. | blocked_not_current_decision |
| D21_04_strategy_works_one_regime | False | No acceptance-grade per-regime winner exists; Stage D is proxy-only. | Build explicit regime gate and test false-classification risk | outputs\stage_d\stage_d_strategy_proxy_summary.csv | Create regime-gated acceptance diagnostics only after candidate strategy exists. | not_proven_currently |
| D21_05_zero_latency_only | False | zero_latency_positive_strategies=2; retail_or_stress_positive_strategies=2 | Reject for retail deployment | outputs\phase12\execution_summary.csv | Keep retail/stressed execution profiles as required; do not promote zero-latency-only behavior. | not_current_primary_decision |
| D21_06_optimistic_passive_only | False | Current acceptance state does not contain an optimistic-passive-only promoted candidate. | Reject or redesign execution | outputs\phase16\risk_adjusted_economic_frontier.csv | Require pessimistic/retail execution controls before promotion. | not_proven_currently |
| D21_07_across_generators_seeds | False | stage_d_positive_noncontrol_strategies=2; predictive_candidates=0; stage_e_blocking_prereqs=4 | Candidate for real-data paper testing | outputs\stage_d\stage_d_strategy_proxy_summary.csv; outputs\phase16\predictive_promotion_falsification.csv; outputs\stage_e\stage_e_prerequisite_ledger.csv | Do not paper-test yet; full readiness blockers remain. | blocked_not_current_decision |
| D21_08_synthetic_not_real | False | Real multi-day strategy comparison does not exist yet. | Treat as generator artifact and investigate | outputs\stage_e\stage_e_prerequisite_ledger.csv | Collect/import multi-day real holdout before classifying synthetic-vs-real divergence. | not_testable_currently |
| D21_09_wild_seed_variation | False | wild_seed_variation_rows=0; note=Stage D current seed summaries are proxy/static by seed | Insufficient robustness or unstable scenario design | outputs\stage_d\stage_d_strategy_proxy_summary.csv | Run true full-seed stochastic execution before using seed variation as an acceptance decision. | not_proven_currently |

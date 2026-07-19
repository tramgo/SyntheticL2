# Phase122 Non-Trading Forecast Filter Precommit

Generated UTC: 2026-07-19T23:26:40.135417+00:00

Phase122 opens a new admissible branch after taker and passive replay paths failed: non-trading forecast filters.
These filters are not buy/sell strategies. They may only predict cost toxicity, realism risk, or abstention regimes until their own calibration gates pass.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase122_prior_evidence_rows | 6 | Prior evidence rows reviewed |
| phase122_prior_surviving_replay_rows | 0 | Prior rows currently allowing replay |
| phase122_feature_source_rows | 3 | Non-trading feature sources precommitted |
| phase122_validation_gate_rows | 5 | Validation gates locked |
| phase122_model_queue_rows | 3 | Future model work items queued |
| phase122_filter_design_allowed | 1 | 1 means filter design may continue |
| phase122_strategy_replay_allowed | 0 | 1 means strategy replay may run |
| phase122_next_best_action | build_phase123_filter_label_matrix_no_replay | Recommended next milestone |
| phase122_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model retained for future cost/toxicity filters |

## Prior Replay Blocker Evidence

| evidence_id | scope | rows_reviewed | candidate_rows | best_net_pnl_inr | survives_gate | decision_use |
| --- | --- | --- | --- | --- | --- | --- |
| P70_CROSS_SYMBOL_LEAD_LAG | cross-symbol lead-lag labels | 48 | 0 | 38915.7 | 0 | feature_context_only_not_replay |
| P71_SHOCK_RESILIENCE | shock/control event-bar labels | 36 | 0 | 13311.4 | 0 | regime_risk_context_only_not_replay |
| P72_RESEARCH_AUDIT | strategy family audit across Phase52-71 | 12 | 0 |  | 0 | blocks_more_strategy_replay |
| P116_PROFITABILITY_VERDICT | latest strategy profitability verdict | 6 | 0 |  | 0 | current_families_not_profitable |
| P121_PASSIVE_RETIREMENT | passive branch train-half retirement gate | 34124776 | 0 |  | 0 | passive_branch_replay_closed |
| P117_REAL_ANCHOR_GATE | real-anchor acquisition status | 1 | 0 |  | 0 | real_replay_locked_until_more_days |

## Non-Trading Filter Feature Contract

| feature_source_id | purpose | not_a_strategy | allowed_inputs | forbidden_inputs | candidate_output | minimum_value_claim |
| --- | --- | --- | --- | --- | --- | --- |
| P122_COST_TOXICITY_FORECAST_FILTER | Predict when spread, costs and adverse-selection risk are too high, so future strategies can abstain rather than trade. | True | spread bucket, depth bucket, event intensity, shock flags, passive toxicity labels, cross-symbol context | future P&L, realized trade outcome, test-period threshold tuning | probability_of_cost_clearing_failure | reduces false-positive strategy candidates and improves abstention calibration |
| P122_REGIME_REALISM_FILTER | Classify synthetic regimes where generator assumptions are unreliable before using them for strategy evidence. | True | shock flags, spread/depth/cadence diagnostics, Phase94/109 realism gaps, cross-symbol synchronization features | strategy net P&L as a regime label | realism_risk_score | separates calibration-quality screening from alpha mining |
| P122_OPPORTUNITY_ABSTENTION_FILTER | Predict low-opportunity periods where any future strategy family should be disabled before execution modeling. | True | event rate, spread, depth, volatility, shock state, cross-symbol dispersion | directional side labels or threshold selection from replay P&L | trade_disable_flag | reduces compute spent on structurally untradeable event windows |

## Validation Gates

| gate_id | stage | requirement | pass_threshold |
| --- | --- | --- | --- |
| P122_NO_DIRECT_TRADING | pre_model | Phase122 feature sources must not emit buy/sell signals or open replay. | strategy_replay_allowed == 0 and outputs are filters/scores only |
| P122_NO_PNL_SELECTION | pre_model | Feature filters cannot be selected or tuned using strategy P&L. | threshold policy uses train-only labels and calibration metrics, not replay P&L |
| P122_CALIBRATION_VALUE | model_gate | A future model must improve calibration of cost/toxicity/realism labels over naive baselines. | holdout Brier/log-loss improvement and monotonic risk buckets |
| P122_BREADTH | model_gate | A future filter must be valid across symbols and months, not a pocket. | >=20 symbols and >=4 train months before pilot integration |
| P122_INTEGRATION_ONLY_AFTER_FILTER_PASS | integration_gate | Only after filter validation may future strategy candidates use it as a risk/abstention layer. | filter_validation_pass == 1; still no profitability claim without downstream gates |

## Filter Model Work Queue

| priority | model_work_item | first_deliverable | model_type_allowed | pilot_replay_allowed | full_year_replay_allowed | why |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | P122_COST_TOXICITY_FORECAST_FILTER | label_matrix_and_baseline_diagnostics | calibrated_logistic_or_tree_model_only_after_label_matrix | False | False | Predict when spread, costs and adverse-selection risk are too high, so future strategies can abstain rather than trade. |
| 2 | P122_REGIME_REALISM_FILTER | label_matrix_and_baseline_diagnostics | calibrated_logistic_or_tree_model_only_after_label_matrix | False | False | Classify synthetic regimes where generator assumptions are unreliable before using them for strategy evidence. |
| 3 | P122_OPPORTUNITY_ABSTENTION_FILTER | label_matrix_and_baseline_diagnostics | calibrated_logistic_or_tree_model_only_after_label_matrix | False | False | Predict low-opportunity periods where any future strategy family should be disabled before execution modeling. |

## Permission Gate

| permission_id | permission | evidence |
| --- | --- | --- |
| P122_FILTER_DESIGN | allowed | Designing non-trading filters is allowed because it does not reopen replay. |
| P122_FILTER_MODEL_FIT | closed_until_label_matrix_exists | No Phase122 label matrix has been built yet. |
| P122_STRATEGY_REPLAY | closed | accepted_strategies=0; passive_replay_allowed=0 |
| P122_REAL_ANCHOR_REPLAY | closed | ready_real_anchor_days=1; additional_days_needed_for_min=4 |

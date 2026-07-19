# Phase64 Strategy-Family Decision Ledger

Generated UTC: 2026-07-19T19:26:14.435433+00:00

Phase64 converts the Phase53-63 evidence into a stop/continue ledger.
The main decision is to stop continuing the failed marketable-taker momentum families shard-by-shard.
The next branch is passive limit-order queue-capture research, handled as an assumption-sensitivity problem because the Zerodha top-five market-by-price feed does not reveal true queue position.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase64_strategy_families_reviewed | 7 | Strategy families in the decision ledger |
| phase64_retired_family_count | 6 | Families explicitly retired by evidence |
| phase64_active_next_branch_count | 1 | New active research branches |
| phase64_marketable_taker_family_retired_count | 6 | Retired marketable/taker-like families |
| phase64_continue_phase60_shard_by_shard | 0 | 0 means do not continue Phase60 shard-by-shard replay |
| phase64_next_priority_research_item | passive_limit_queue_capture_sensitivity | Highest-priority next experiment |
| phase64_next_priority_phase | 65 | Suggested next phase number |
| phase64_requires_passive_assumption_sensitivity | 1 | Passive fills require assumption sensitivity because true queue position is unavailable |
| phase64_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model used by retired taker-family evidence |

## Strategy Family Decision Ledger

| strategy_family_id | phases | decision | deployable | best_evidence | primary_failure_mode | gross_positive_evidence | after_cost_positive_evidence | net_pnl_inr | trade_count | scale_recommendation | required_next_action | can_continue_same_shard_family |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F01_dense_marketable_bruteforce | 52,53 | retired | False | Phase53 found zero profitable aggregate strategy/profile rows after retail costs. | costs_overwhelmed_dense_taker_signals | 3 | 0 |  | 8.26538e+08 | 0 | do_not_continue_bruteforce_shard_replay | False |
| F02_selective_marketable_controls | 54 | retired | False | Phase54 produced one after-cost positive row only in nondeployable controls and zero deployable retail candidates. | positive_only_under_nondeployable_control_assumptions |  | 1 | 7856.21 | 456 | 0 | keep_as_control_not_live_candidate | False |
| F03_cost_aware_taker_edge_mining | 55 | retired | False | Phase55 found no deployable positive after-cost candidates; the positive ceiling was oracle-only. | oracle_positive_but_retail_deployable_negative | 1 | 0 | -13367.6 | 490 | 0 | do_not_scale_oracle_edges | False |
| F04_no_lookahead_dense_rule_labels | 56 | retired | False | Phase56 evaluated 180 no-lookahead rules and found zero positive test rules after retail costs. | no_test_rule_cleared_costs |  | 0 | -4829.7 | 180 | 0 | do_not_widen_dense_no_lookahead_rules | False |
| F05_supervised_interaction_cells | 57,58,59 | retired | False | Phase57 found one candidate, but Phase58 emitted zero disjoint trades and Phase59 found zero positive stable validation rows. | non_repeating_sparse_cell_and_failed_stability_validation | 1 | 0 | -785962 | 0 | 0 | retire_sparse_interaction_cell_family | False |
| F06_lower_frequency_event_bar_momentum | 60,61,62,63 | retired | False | Phase60 passed initial validation, then Phase61 lost -88,748.03 INR, Phase62 found only a tiny KOTAKBANK clue, and Phase63 falsified that clue at -24,100.26 INR. | initial_validation_edge_did_not_survive_wider_symbol_month_falsification | 1 | 0 | -24100.3 | 155 | 0 | retire_phase60_candidate_family | False |
| F07_passive_limit_queue_capture | 64_next | next_active_research_branch | False | Marketable-taker families repeatedly failed after spread, slippage, impact and Zerodha charges; a different mechanism must be tested. | not_yet_tested_and_passive_fills_are_unobserved_assumptions |  |  |  |  | 1 | implement_passive_queue_assumption_sensitivity_before_any_profit_claim | True |

## Next Research Queue

| priority | research_item | phase | why_now | minimum_deliverable | acceptance_gate | risk_note |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | passive_limit_queue_capture_sensitivity | 65 | All dense marketable-taker families are retired; passive queue capture is the nearest genuinely different L2 mechanism. | Replay simulator with explicit queue-position assumptions, fill probability catalog, maker adverse-selection model and Zerodha cost handling. | Positive after-cost P&L must survive pessimistic, base and optimistic fill assumptions separately; no single assumed queue model may be enough. | Zerodha top-five market-by-price data cannot directly observe order identity or true queue position. |
| 2 | passive_adverse_selection_labels | 66 | A passive order can earn spread only if post-fill adverse selection does not dominate. | No-lookahead labels for whether a hypothetical bid/ask queue fill is followed by favorable or adverse mid-price movement. | Labels must be generated without future leakage and reported by symbol, time-of-day, spread bucket and depth bucket. | Fill labels remain hypothetical until real broker fills or richer exchange/order data are available. |
| 3 | strategy_stop_rule_and_experiment_budgeting | 67 | The recent phases show how easy it is to over-iterate a dead family. | Machine-readable stop/continue gates applied before large full-year runs. | A strategy family cannot request more shards unless it passes a predeclared out-of-sample gate. | This protects compute and attention from false-positive chasing. |

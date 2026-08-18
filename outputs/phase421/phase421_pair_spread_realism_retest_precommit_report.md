# Phase421 Pair-Spread Realism Retest Precommit

Phase421 freezes the repair retest required by Phase420 before any new pair-spread execution.

It keeps the positive lead alive while requiring minimum forward time/ticks and a full-depth unique contribution gate.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase421_pair_spread_realism_retest_precommit_complete | 1 | Phase421 precommit completed |
| phase421_thesis_id | P421_PAIR_SPREAD_REALISM_RETEST_FULL_DEPTH_UNIQUE_GATE | Frozen repair retest |
| phase421_contract_rows | 15 | Contract rows |
| phase421_parameter_freeze_rows | 11 | Frozen parameter rows |
| phase421_parameter_freeze_hash | 8930d855e637875b84b73b1412ffa72c3bbb571b712ff17680c92ebb51fe4f57 | Parameter freeze hash |
| phase421_min_forward_hold_ms | 250 | New timing rule |
| phase421_min_forward_ticks_after_entry | 3 | New timing rule |
| phase421_min_l2_l5_edge_delta_vs_removed_pct | 5 | New full-depth unique gate |
| phase421_execution_results_generated | 0 | Precommit only |
| phase421_strategy_promotion_allowed | 0 | No promotion |
| phase421_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase421_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase421_execution_allowed_next | 1 | Whether Phase422 may run |
| phase421_hard_gate_pass_rows | 12 | Passed hard gates |
| phase421_hard_gate_rows | 12 | Hard gates |
| phase421_next_best_action | run_phase422_pair_spread_realism_retest_execution_no_paper_live | Recommended next action |

## Frozen Contract

| contract_id | contract_value | description |
| --- | --- | --- |
| thesis_id | P421_PAIR_SPREAD_REALISM_RETEST_FULL_DEPTH_UNIQUE_GATE | Realism repair precommit for the Phase418 positive pair lead. |
| relationship_to_phase418 | same_pair_family_allowed_only_as_precommitted_repair_not_promotion | This is a repair retest, not a new acceptance claim. |
| phase420_blockers_addressed | full_depth_contribution;timing_realism;real_anchor_pair_panel;cost_rank | All Phase420 required repairs are in scope. |
| pair_catalog | HDFCBANK/ICICIBANK;HDFCBANK/AXISBANK;INFY/TCS;RELIANCE/ONGC | Same frozen Phase417 pairs. |
| entry_signal | same_pair_spread_zscore_form_as_phase417 | Signal form unchanged to isolate repairs. |
| minimum_forward_time | hold_ms>=250.0 | Blocks same-timestamp exits. |
| minimum_forward_ticks | ticks_after_entry>=3 | Requires actual forward ticks after entry. |
| full_depth_unique_gate | primary_annualized_minus_l2_removed>=5.0 | Levels 2-5 must add value versus removal. |
| real_anchor_requirement | real_anchor_pair_dates>=5 | Use existing local real pair coverage. |
| execution_profile | taker_entry_both_legs_taker_exit_both_legs_cost200 | No passive fill, no maker rebate. |
| cost_model | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Pinned Zerodha equity intraday NSE formula. |
| cost_multiplier | 2 | Cost200 acceptance scoring. |
| capital | initial=1000000.0;leg_notional=50000.0 | Fixed capital denominator. |
| acceptance | round_trips>=30;dates>=5;pairs>=2;positive_date_fraction>=0.6;annualized>=12.0 | Same profitability acceptance discipline. |
| forbidden | promotion_before_phase422;paper_live;deployable_claim;dropping_l2_l5_gate;dropping_forward_time_rule | Closed boundaries. |

## Frozen Parameters

| parameter_id | value | status |
| --- | --- | --- |
| P421_LOOKBACK_TICKS | 240 | same_as_phase417 |
| P421_ENTRY_ZSCORE | 1.75 | same_as_phase417 |
| P421_EXIT_ZSCORE | 0.35 | same_as_phase417 |
| P421_STOP_ZSCORE | 3.25 | same_as_phase417 |
| P421_MAX_HOLD_TICKS | 360 | same_as_phase417 |
| P421_MIN_FORWARD_HOLD_MS | 250 | new_repair |
| P421_MIN_FORWARD_TICKS_AFTER_ENTRY | 3 | new_repair |
| P421_MIN_L2_L5_EDGE_DELTA_VS_REMOVED_PCT | 5 | new_repair |
| P421_REQUIRE_REAL_ANCHOR_PAIR_DATES | 5 | new_repair |
| P421_ALIGN_TOLERANCE_MS | 1000 | same_as_phase418 |
| P421_MAX_ROWS_PER_SYMBOL_MONTH | 25000 | bounded_execution |

## Input Registry

| input_id | value | description |
| --- | --- | --- |
| phase420_complete | 1 | Phase420 audit complete. |
| phase420_positive_lead_preserved | 1 | Lead still alive. |
| phase420_acceptance_allowed | 0 | Must be zero before repair. |
| phase420_full_depth_contribution_pass | 0 | Must be zero blocker. |
| phase420_timing_realism_pass | 0 | Must be zero blocker. |
| phase420_same_timestamp_share | 0.42328 | Timing blocker magnitude. |
| phase420_real_anchor_pair_available_count | 4 | Real-anchor pair availability. |
| phase420_min_overlap_dates_per_pair | 16 | Minimum overlap dates across frozen pairs. |
| execution_results_generated_now | 0 | Precommit only. |

## Phase422 Hard-Gate Contract

| gate_id | requirement | severity | phase421_precommitted |
| --- | --- | --- | --- |
| P422_PHASE421_PRECOMMIT_USED | Execution must read Phase421 frozen contract. | hard | 1 |
| P422_FORWARD_TIME_ENFORCED | Exit must be at least 250.0 ms after entry. | hard | 1 |
| P422_FORWARD_TICKS_ENFORCED | Exit must be at least 3 aligned ticks after entry. | hard | 1 |
| P422_FULL_DEPTH_UNIQUE_GATE | Primary must beat L2-L5 removed control by required margin. | hard | 1 |
| P422_REAL_ANCHOR_PAIR_PANEL_USED | Use local real-anchor pair dates if available. | hard | 1 |
| P422_PAIR_MARKET_NEUTRAL | Equal notional long/short pair exposure. | hard | 1 |
| P422_TAKER_ONLY | No passive fill and no maker rebate. | hard | 1 |
| P422_NO_LOOKAHEAD | Rolling features before entry only. | hard | 1 |
| P422_COST200_FIXED_CAPITAL | Zerodha cost200 with fixed capital. | hard | 1 |
| P422_BREADTH_AND_RETURN_GATES | Event/date/pair/positive-date/annualized gates must pass. | hard | 1 |
| P422_COST_RANK_RECORDED | Cost100 and cost200 rank must be recorded. | hard | 1 |
| P422_BOUNDARIES_CLOSED | No promotion, paper/live or deployable claim in execution phase. | hard | 1 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P421_PHASE420_COMPLETE | True | 1 | 1 | hard |
| P421_POSITIVE_LEAD_PRESERVED | True | 1 | 1 | hard |
| P421_ACCEPTANCE_STILL_BLOCKED | True | 0 | 0 | hard |
| P421_FULL_DEPTH_BLOCKER_ACKNOWLEDGED | True | 0 | 0 | hard |
| P421_TIMING_BLOCKER_ACKNOWLEDGED | True | 0 | 0 | hard |
| P421_REAL_ANCHOR_PANEL_AVAILABLE | True | 16 | >=5 | hard |
| P421_FORWARD_TIME_RULE_FROZEN | True | ms=250.0;ticks=3 | positive | hard |
| P421_FULL_DEPTH_UNIQUE_GATE_FROZEN | True | 5 | >0 | hard |
| P421_FIXED_PARAMETERS_FROZEN | True | 11 | >=11 | hard |
| P421_EXECUTION_HARD_GATES_PRECOMMITTED | True | 12 | 12 | hard |
| P421_RESULTS_NOT_GENERATED | True | 0 | 0 | hard |
| P421_FORBIDDEN_BOUNDARIES_CLOSED | True | promotion_before_phase422;paper_live;deployable_claim;dropping_l2_l5_gate;dropping_forward_time_rule | closed_routes_listed | hard |

No Phase421 result, promotion, paper/live acceptance or deployable claim is generated.

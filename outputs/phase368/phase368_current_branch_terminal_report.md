# Phase368 Current Branch Terminal Report

Generated: 2026-08-11T16:13:16.860015+00:00

Phase368 closes the current passive-aware/catalyst-reversal evidence branch for acceptance. This is not a claim that all top-five depth research is useless; it says the current evidence does not justify replay promotion, paper/live acceptance, or deployable profitability claims.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase368_current_branch_terminal_report_complete | 1 | Phase368 complete if all hard gates pass |
| phase368_selected_verdict | P368_CURRENT_PASSIVE_AWARE_AND_CATALYST_REVERSAL_BRANCH_CLOSED_FOR_ACCEPTANCE | Current branch verdict |
| phase368_phase359_no_lookahead_events | 25 | Phase359 eligible catalyst events |
| phase368_phase360_primary_annualized_return_pct | -47.3526 | Phase360 real holdout annualized |
| phase368_phase360_acceptance_candidate_rows | 0 | Phase360 acceptance candidates |
| phase368_phase363_best_scenario_id | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | Phase363 best clue |
| phase368_phase363_best_annualized_return_pct | 39.1448 | Phase363 best annualized |
| phase368_phase366_primary_trade_rows | 12 | Phase366 selected trades |
| phase368_phase366_event_floor_met | 0 | Phase366 event floor |
| phase368_phase367_passive_acceptance_reopened | 0 | Phase367 passive acceptance reopened |
| phase368_strategy_promotion_allowed | 0 | No promotion |
| phase368_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase368_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase368_hard_gate_pass_rows | 7 | Passed hard gates |
| phase368_hard_gate_rows | 7 | Hard gates |
| phase368_next_best_action | add_or_verify_more_official_catalyst_real_l2_events_before_any_retest_no_paper_live | Recommended next action |

## Evidence chain

| phase | evidence_role | key_observation | acceptance_read |
| --- | --- | --- | --- |
| 302 | old_passive_aware_terminal_report | verdict=P302_RETAIL_TOP5_L2_ALPHA_THESIS_CLOSED_FOR_ACCEPTANCE | Old Phase298-301 passive-aware route closed for acceptance. |
| 359 | local_unseen_real_l2_official_catalyst_join | unseen_dates=2026-07-17;2026-07-20; eligible_events=25 | Real L2/catalyst holdout evidence exists, but event count is still small. |
| 360 | full_depth_market_neutral_fade_real_holdout | ann=-47.35263653783534; acceptance=0 | Full-depth fade failed on unseen real L2 catalyst holdout. |
| 363 | liquidity_replenished_catalyst_impulse_diagnostic | best=P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL; ann=39.144819884564285; acceptance=0 | Found a positive reversal-control clue, but no acceptance candidate. |
| 366 | frozen_reversal_clue_audit | trades=12; event_floor_met=0; acceptance=0 | Clue remains sparse and below event-floor acceptance. |
| 367 | passive_aware_charter_reconciliation | passive_acceptance_reopened=0 | Passive-aware route is not reopened by the sparse clue. |

## Closure decisions

| decision_id | decision_value | evidence | decision_status |
| --- | --- | --- | --- |
| selected_current_branch_verdict | P368_CURRENT_PASSIVE_AWARE_AND_CATALYST_REVERSAL_BRANCH_CLOSED_FOR_ACCEPTANCE | Phase302 closure plus Phase367 reconciliation | close_current_branch_for_acceptance |
| do_not_run_passive_acceptance_on_12_trade_clue | 1 | Phase366 selected trades=12; event_floor_met=0 | blocked_until_more_real_events |
| preserve_catalyst_reversal_clue | P362_D120_I2p5_D0p25_R0p0_REVERSAL_CONTROL | ann=39.144819884564285; acceptance=0 | diagnostic_only |
| next_data_action_if_continuing | add_or_verify_more_official_catalyst_real_l2_events | Phase367 next-action contract | data_expansion_before_retest |
| boundaries_closed | promotion=0;paper_live=0;deployable_claim=0 | Phase367 and upstream summaries | closed |

## Durable by-products

| byproduct_id | kept_for | not_kept_for |
| --- | --- | --- |
| P368_OFFICIAL_CATALYST_EVENT_JOIN | future event-count expansion and no-lookahead real L2 diagnostics | acceptance on current sparse event count |
| P368_FULL_DEPTH_REAL_L2_SCHEMA_AUDIT | ensuring levels 1-5 and levels 2-5 materiality in later tests | L1-only strategy variants |
| P368_PASSIVE_AWARE_REALISM_CHARTER | future passive execution tests after event-floor evidence exists | weakening fill, adverse-selection, or forced-flatten penalties |
| P368_CATALYST_REVERSAL_CLUE | falsification on additional official-catalyst real L2 days | paper/live or profitability claims |

## Gates

| gate_id | passed | evidence |
| --- | --- | --- |
| P368_PHASE302_TERMINAL_PRESENT | 1 | P302_RETAIL_TOP5_L2_ALPHA_THESIS_CLOSED_FOR_ACCEPTANCE |
| P368_PHASE359_REAL_HOLDOUT_PRESENT | 1 | eligible_events=25 |
| P368_PHASE360_REAL_HOLDOUT_EXECUTED | 1 | ann=-47.35263653783534; acceptance=0 |
| P368_PHASE366_CLUE_BELOW_ACCEPTANCE | 1 | trades=12; event_floor=0; acceptance=0 |
| P368_PHASE367_RECONCILIATION_COMPLETE | 1 | Phase367 complete |
| P368_EVIDENCE_CHAIN_PRESENT | 1 | rows=6 |
| P368_BOUNDARIES_CLOSED | 1 | promotion=0;paper_live=0;claim=0 |

## Boundary

No replay promotion, paper/live acceptance, or deployable profitability claim is opened. The next productive path is data expansion: add or verify more official-catalyst real L2 events before any retest.

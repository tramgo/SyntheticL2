# Phase344 Official-Catalyst-Native Full-Depth Strategy Search Precommit

Generated: 2026-08-11T08:11:38.241323+00:00

Phase344 precommits a materially new official-catalyst-native full-depth search. The failed Phase338/339 survivor remains closed.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase344_official_catalyst_native_full_depth_strategy_search_precommit_complete | 1 | Phase344 precommit completed |
| phase344_phase343_complete | 1 | Phase343 complete |
| phase344_failed_survivor_closed | 1 | Failed survivor remains closed |
| phase344_family_rows | 4 | Search family rows |
| phase344_grid_rows | 67 | Search grid rows |
| phase344_negative_control_rows | 1 | Negative control family rows |
| phase344_material_new_required | 1 | Material-new route required |
| phase344_full_depth_required | 1 | Full top-five depth required |
| phase344_levels_2_to_5_required | 1 | Levels 2-5 materiality required |
| phase344_l1_only_allowed | 0 | No L1-only variants |
| phase344_no_lookahead_required | 1 | No lookahead |
| phase344_phase345_execution_allowed_next | 1 | Phase345 execution allowed next |
| phase344_strategy_promotion_allowed | 0 | No promotion |
| phase344_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase344_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase344_hard_gate_pass_rows | 8 | Passed hard gates |
| phase344_hard_gate_rows | 8 | Hard gates |
| phase344_next_best_action | run_phase345_official_catalyst_native_full_depth_strategy_search_execution_no_paper_live | Recommended next action |

## Family catalog

| family_id | material_new_reason | allowed_catalyst_categories | side_policy | entry_timing_grid | horizon_grid_seconds | full_depth_features | control_required |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P344_CATALYST_CATEGORY_CONTINUATION | Uses official catalyst category and real post-catalyst L2 response; not the failed synthetic survivor signal. | General Updates;Updates | category_directional_continuation | market_open_or_first_tick_after_announcement;delay_60s;delay_300s | 300;900;1800 | top5_qty_imbalance;l2_l5_qty_imbalance;top5_order_imbalance;spread;quote_churn | category_shuffle;side_flip;random_side |
| P344_FULL_DEPTH_CATALYST_REACTION_FILTER | Conditions official catalyst rows on observed real full-depth pressure after event start. | all_official_categories | depth_pressure_sign | first_valid_tick;delay_60s;delay_300s | 300;900;1800 | l2_l5_qty_imbalance_delta;top5_order_imbalance_delta;spread_compression;depth_replenishment_proxy | depth_feature_shuffle;side_flip;random_side |
| P344_SBIN_AND_BANK_CATALYST_DIAGNOSTIC | Separately tests official SBIN/bank catalysts requested by the user, without treating SBIN clues as accepted. | SBIN;AXISBANK;HDFCBANK;ICICIBANK;KOTAKBANK | bank_catalyst_depth_confirmation | market_open_or_first_tick_after_announcement;delay_300s | 900;1800 | top5_qty_imbalance;l2_l5_qty_imbalance;spread;receive_event_rate | bank_symbol_shuffle;side_flip;random_side |
| P344_NEGATIVE_CONTROL_FAILED_SURVIVOR_REPLAY | Negative control only: confirms failed Phase338/339 survivor is not reopened as a tuned route. | all_official_categories | failed_survivor_frozen_long_only | phase342_exact | 900 | none_new_negative_control | must_remain_closed_for_acceptance |

## Gate evaluation

| gate_id | passed | observed | required |
| --- | --- | --- | --- |
| P344_PHASE343_COMPLETE | True | 1 | 1 |
| P344_FAILED_SURVIVOR_CLOSED | True | 1 | 1 |
| P344_MATERIAL_NEW_FAMILIES_PRESENT | True | 4 | >=3 |
| P344_GRID_PRESENT | True | 67 | >0 |
| P344_NEGATIVE_CONTROL_PRESENT | True | 1 | 1 |
| P344_FULL_DEPTH_NO_L1_ONLY_NO_LOOKAHEAD | True | preserved | preserved |
| P344_CONTRACT_PRESENT | True | 21 | >=18 |
| P344_NO_PROMOTION_PAPER_LIVE_OR_PROFIT_CLAIM | True | closed | closed |

No promotion, paper/live acceptance, or deployable profitability claim is opened by Phase344.
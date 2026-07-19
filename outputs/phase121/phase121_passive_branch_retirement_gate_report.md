# Phase121 Passive Branch Retirement Gate

Generated UTC: 2026-07-19T23:23:52.045813+00:00

Phase121 reviews the Phase120 Stage 01 and Stage 02 label-only expansions before allowing any more passive work.
The verdict is to retire the current passive branch from replay: broader train-half coverage did not produce a single pre-replay candidate and adverse-selection remains toxic.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase121_stage_rows_reviewed | 2 | Phase120 passive label expansion stages reviewed |
| phase121_max_shards_reviewed | 192 | Largest label-only expansion reviewed |
| phase121_train_half_candidate_orders | 34124776 | Train-half hypothetical passive candidate orders reviewed |
| phase121_train_half_inferred_touches | 405440 | Train-half inferred passive touches reviewed |
| phase121_train_half_pre_replay_candidates | 0 | Train-half richer passive pre-replay candidates |
| phase121_hard_failure_rows | 5 | Hard failure bases recorded |
| phase121_retired_family_rows | 4 | Passive families retired or blocked |
| phase121_passive_replay_allowed | 0 | 1 means passive bounded replay may run |
| phase121_stage03_full_year_label_allowed | 0 | 1 means full-year passive label Stage03 should run now |
| phase121_next_best_action | return_to_real_anchor_acquisition_or_precommit_new_non_passive_feature_source | Recommended next milestone |
| phase121_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model used by passive label evidence |

## Passive Stage Evidence Ledger

| stage_id | stage_root | shards_scanned | phase66_candidate_orders | phase66_inferred_touches | phase66_label_candidate_rows | phase66_best_after_cost_bps | phase68_label_candidate_rows | phase68_best_after_cost_bps | phase68_best_adverse_selection_rate | phase69_signal_rows | phase69_label_candidate_rows | phase69_best_after_cost_bps | phase119_joined_label_candidate_rows | phase119_pre_replay_candidate_rows | phase119_max_candidate_symbols | phase119_max_candidate_trade_dates | phase119_bounded_pilot_replay_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stage01_min_breadth | outputs\phase120\P120_LABEL_STAGE_01_MIN_BREADTH | 128 | 22821992 | 274244 | 0 | -22.4421 | 0 | -19.1692 | 0.976202 | 1312100 | 0 | -10.0382 | 696 | 0 | 4 | 4 | 0 |
| stage02_train_half | outputs\phase120\P120_LABEL_STAGE_02_TRAIN_HALF | 192 | 34124776 | 405440 | 0 | -21.2765 | 0 | -18.2877 | 0.970833 | 1816100 | 0 | -10.067 | 696 | 0 | 4 | 6 | 0 |

## Passive Failure Basis

| failure_id | evidence | decision | why_it_matters |
| --- | --- | --- | --- |
| P121_ADVERSE_SELECTION_TOXICITY | best_train_half_replenishment_adverse_selection_rate=0.9708333333333334 | hard_fail | Passive fills are expected to be toxic if nearly all inferred touches are followed by adverse markout. |
| P121_NO_LABEL_CANDIDATES | phase66=0; phase68=0; phase69=0 | hard_fail | The component label gates produced no candidate buckets even before replay. |
| P121_NO_JOINED_PRE_REPLAY_CANDIDATES | phase119_pre_replay_candidate_rows=0 | hard_fail | The richer composite label builder could form candidates but none passed all feasibility gates. |
| P121_SYMBOL_BREADTH_SHORTFALL | max_joined_symbols=4; required_symbols=20 | hard_fail | A passive label pocket across four symbols is not broad enough to justify replay. |
| P121_AFTER_COST_LABEL_NEGATIVE | best_phase66_bps=-21.276485937116394; best_phase68_bps=-18.28774559151268; best_phase69_bps=-10.066955534890022 | hard_fail | The best label buckets remain negative after the Zerodha cost floor. |

## Passive Retirement Ledger

| family_id | decision | replay_allowed | full_year_label_stage03_allowed | resume_condition |
| --- | --- | --- | --- | --- |
| P66_NAIVE_PASSIVE_IMBALANCE | retired | False | False | Only as a negative-control label family. |
| P68_REPLENISHMENT_AFTER_TOUCH | retired_as_standalone_alpha | False | False | Only if a future non-P&L label source reduces adverse-selection rate below 0.45 across at least 20 symbols. |
| P69_SPREAD_TRANSITION | retired_as_standalone_alpha | False | False | Only as context inside a new non-toxic feature class, not as standalone spread-transition replay. |
| P118_RICHER_PASSIVE_LABEL_COMPOSITE | retired_pending_new_feature_source | False | False | Requires a materially new feature source that passes adverse-selection and breadth gates before any bounded replay. |

## Next Research Queue

| priority | next_item | phase_reference | why | allowed_now | forbidden |
| --- | --- | --- | --- | --- | --- |
| 1 | real_anchor_data_acquisition | Phase117 | The current synthetic strategy families are falsified or replay-locked; adding real WebSocket L2 days is the cleanest source of new evidence. | True | Do not claim profitability from synthetic-only pockets. |
| 2 | new_non_passive_non_taker_feature_source_precommit | new_phase | Both taker and passive-simple mechanisms failed; a new branch must use a genuinely different edge source before replay. | True | No threshold widening of P66/P68/P69/P118 candidates. |
| 3 | full_year_passive_label_stage03 | Phase120 Stage03 | Only useful as final confirmation/negative-control, not as a path to replay after Stage02 hard failures. | False | Do not run unless explicitly needed for audit completeness. |

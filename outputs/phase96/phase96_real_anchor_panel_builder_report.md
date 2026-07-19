# Phase96 Real Anchor Panel Builder

Generated UTC: 2026-07-19T21:35:50.897586+00:00

Phase96 validates available real Zerodha WebSocket L2 data against the Phase95 multi-day panel contract.
It uses deterministic per-symbol file sampling so the current 50k tiny-file one-day archive can be checked quickly, while preserving the replay lock until enough real days exist.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase96_symbol_partitions_found | 32 | Symbol partitions discovered under real-data roots |
| phase96_total_real_parquet_files | 50205 | Total real Parquet files inventoried |
| phase96_day_readiness_rows | 1 | Panel/day readiness rows built from deterministic samples |
| phase96_ready_anchor_days | 1 | Days passing schema/L1/timing/symbol-coverage sample gates |
| phase96_max_ready_dates_in_panel | 1 | Maximum ready trade-date count in any panel |
| phase96_panels_ready_for_phase94_rerun | 0 | Panels with enough ready days for Phase94 rerun |
| phase96_strategy_replay_unlocked | 0 | 1 means strategy replay gate is reopened |
| phase96_recommend_next_action | collect_more_real_websocket_l2_days | Recommended next milestone |

## Panel Manifest

| panel_name | distinct_trade_dates | ready_trade_dates | ready_trade_date_list | min_expected_symbol_fraction | all_days_schema_pass | all_days_l1_book_pass | all_days_timing_pass | panel_ready_for_phase94_rerun |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| l2_single_day | 1 | 1 | 2026-07-13 | 1 | True | True | True | False |

## Replay Gate

| gate_id | gate_pass | evidence | next_action_if_fail |
| --- | --- | --- | --- |
| P96_REAL_PANEL_READY_FOR_PHASE94_RERUN | False | At least one panel has >=5 ready trade dates with >=95% symbol coverage, schema pass, L1 book pass, and timing pass. | collect_more_real_websocket_l2_days |
| P96_STRATEGY_REPLAY_LOCK | False | Phase95 real_anchor_panel_ready=0.0; Phase96 panel_ready=0. | keep_strategy_replay_closed_until_phase94_rerun_passes |

## Day Readiness

| panel_name | trade_date | symbols_observed | expected_symbol_fraction | missing_expected_symbols | sampled_rows | schema_pass | l1_book_pass | timing_pass | day_ready_for_anchor_panel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| l2_single_day | 2026-07-13 | 32 | 1 |  | 19237 | True | True | True | True |

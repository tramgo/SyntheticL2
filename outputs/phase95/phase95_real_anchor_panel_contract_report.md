# Phase95 Real Anchor Panel Contract

Generated UTC: 2026-07-19T21:32:56.077723+00:00

Phase95 converts the Phase94 calibration stop into a concrete real-data acquisition contract.
The current workspace is scanned for available real L2 panels, and strategy replay remains closed until a multi-day real anchor panel exists and Phase94 passes on rerun.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase95_real_panel_roots_found | 1 | Real-data panel roots with Parquet files discovered |
| phase95_schema_anchor_panel_roots | 1 | Panel roots usable for schema/single-day anchors |
| phase95_multi_day_calibration_panel_roots | 0 | Panel roots meeting the multi-day calibration gate |
| phase95_max_inferred_real_dates | 1 | Maximum inferred real date count across panel roots |
| phase95_max_expected_symbol_fraction | 1 | Best expected-symbol coverage fraction across panel roots |
| phase95_phase94_generator_calibration_pass | 0 | Phase94 generator calibration pass flag |
| phase95_phase94_strategy_resume_allowed | 0 | Phase94 strategy replay resume flag |
| phase95_real_anchor_panel_ready | 0 | 1 means real anchor panel is ready and strategy replay may reopen |
| phase95_recommend_next_action | collect_5_to_10_real_websocket_l2_days_then_rerun_phase94 | Recommended next milestone |

## Available Real Panel Inventory

| panel_root | panel_name | parquet_files | symbol_partitions | expected_symbol_fraction | missing_expected_symbols | inferred_dates | inferred_date_count | usable_for_schema_anchor | usable_for_multi_day_calibration |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| real_data_sample\l2_single_day | l2_single_day | 50205 | 32 | 1 |  | unknown_single_day | 1 | True | False |

## Required Real Anchor Panel Contract

| requirement_id | requirement | acceptance_gate | why |
| --- | --- | --- | --- |
| P95_MIN_REAL_DAYS | Collect at least 5 complete NSE trading days before generator recalibration is considered stable; 10 days preferred. | real_distinct_trade_dates >= 5 | One real day cannot identify regime frequencies, tails, month effects, or stable calibration distributions. |
| P95_SYMBOL_UNIVERSE | Each accepted day should cover the fixed 32-symbol universe or explicitly document missing symbols. | expected_symbol_fraction >= 0.95 for each accepted day | Cross-sectional spread/depth/cadence calibration needs broad symbol coverage. |
| P95_SCHEMA | Persist the Zerodha WebSocket 54-column schema plus capture diagnostics when available. | L1-L5 price, quantity, order-count fields present for bid and ask | Generator calibration depends on visible top-five book state and received tick timing. |
| P95_TIMING | Preserve callback receive timestamps, exchange timestamps, local monotonic time, and receive ordering. | monotonic/order violation, duplicate timestamp, stale interval, and gap metrics can be computed per symbol/day | Phase94 found tail cadence calibration gaps; timing evidence is mandatory. |
| P95_MARKET_CONTEXT | Include a mix of normal, volatile, and shock-like sessions where practical. | panel labels include at least one high-volatility or news/shock-like day before full-year recalibration claims | Synthetic regime and shock assumptions cannot be validated from a calm single day. |
| P95_REPLAY_LOCK | No new strategy replay branch may be opened until Phase94 calibration gaps are rerun against the multi-day panel. | phase94_strategy_replay_resume_allowed == 1 after rerun | Phase93 stopped strategy mining; Phase94 confirmed calibration gaps. |

## Collection Manifest Template

| field | required | example | description |
| --- | --- | --- | --- |
| trade_date | True | 2026-07-20 | NSE trading date represented by the captured WebSocket ticks. |
| session_label | True | normal\|volatile\|shock_like\|expiry\|event | Human or rule-based context label for calibration stratification. |
| symbols_expected | True | ADANIPORTS\|AXISBANK\|BAJAJ-AUTO\|BANKBEES\|BHARTIARTL\|BPCL\|BRITANNIA\|CIPLA\|DRREDDY\|GOLDBEES\|HCLTECH\|HDFCBANK\|HINDUNILVR\|ICICIBANK\|INFY\|ITBEES\|ITC\|JUNIORBEES\|KOTAKBANK\|LT\|M&M\|MARUTI\|NESTLEIND\|NIFTYBEES\|ONGC\|RELIANCE\|SBIN\|SUNPHARMA\|TCS\|TECHM\|ULTRACEMCO\|WIPRO | Expected fixed universe for the capture day. |
| symbols_observed | True | ADANIPORTS\|AXISBANK\|... | Observed symbols with at least one readable L2 tick. |
| capture_start_ist | True | 09:15:00 | Intended market-open capture start in IST. |
| capture_end_ist | True | 15:30:00 | Intended market-close capture end in IST. |
| collector_version | True | zerodha_websocket_l2_collector_vX | Collector/script version or git commit used for capture. |
| known_incidents | False | disconnect 10:42-10:44; reconnect ok | Disconnects, subscription failures, parser issues, or machine/network incidents. |

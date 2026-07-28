# Phase180 Cost/Latency-bound Label Precommit

Generated UTC: 2026-07-28T16:22:26.384663+00:00

Phase180 pins Zerodha equity cost components, latency/slippage profiles, and future label families before any replay.
It does not emit signals, orders, fills, P&L, profitability claims, or paper/live acceptance.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase180_cost_component_rows | 26 | Zerodha cost component rows pinned |
| phase180_latency_profile_rows | 3 | Latency/slippage profiles declared |
| phase180_label_family_rows | 3 | Label families precommitted |
| phase180_gate_rows | 6 | Gates evaluated |
| phase180_hard_gate_rows | 6 | Hard gates evaluated |
| phase180_hard_gate_pass_rows | 6 | Hard gates passed |
| phase180_precommit_ready | 1 | 1 means label materialization phase may be built |
| phase180_strategy_replay_allowed | 0 | No strategy replay opened |
| phase180_paper_or_live_acceptance_allowed | 0 | Paper/live remains closed |
| phase180_forbidden_outputs | signal;order;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | Outputs forbidden in this phase |
| phase180_next_best_action | build_phase181_label_materialization_no_replay | Recommended next milestone |

## Zerodha Equity Cost Component Catalog

| segment | exchange | component | applicable_side | formula | unit | note | official_source_url | verified_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| equity_delivery | NSE | brokerage | both | 0 | inr_per_executed_order | Zero brokerage for resident retail equity delivery | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | BSE | brokerage | both | 0 | inr_per_executed_order | Zero brokerage for resident retail equity delivery | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_intraday | NSE | brokerage | both | min(0.0003 * turnover, 20) | inr_per_executed_order | 0.03 percent or Rs 20 per executed order, whichever is lower | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_intraday | BSE | brokerage | both | min(0.0003 * turnover, 20) | inr_per_executed_order | 0.03 percent or Rs 20 per executed order, whichever is lower | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | NSE | stt | buy_and_sell | 0.001 * turnover | inr | 0.1 percent on buy and sell | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | BSE | stt | buy_and_sell | 0.001 * turnover | inr | 0.1 percent on buy and sell | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_intraday | NSE | stt | sell | 0.00025 * sell_turnover | inr | 0.025 percent on sell side only | https://support.zerodha.com/category/account-opening/resident-individual/ri-charges/articles/how-is-the-securities-transaction-tax-stt-calculated | 2026-07-28T16:22:26.344990+00:00 |
| equity_intraday | BSE | stt | sell | 0.00025 * sell_turnover | inr | 0.025 percent on sell side only | https://support.zerodha.com/category/account-opening/resident-individual/ri-charges/articles/how-is-the-securities-transaction-tax-stt-calculated | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | NSE | transaction_charges | both | 0.0000307 * turnover | inr | NSE equity transaction charges 0.00307 percent | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_intraday | NSE | transaction_charges | both | 0.0000307 * turnover | inr | NSE equity transaction charges 0.00307 percent | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | BSE | transaction_charges | both | 0.0000375 * turnover | inr | BSE equity transaction charges 0.00375 percent | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_intraday | BSE | transaction_charges | both | 0.0000375 * turnover | inr | BSE equity transaction charges 0.00375 percent | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | NSE | sebi_charges | both | 10 / 10000000 * turnover | inr | SEBI charges Rs 10 per crore | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_intraday | NSE | sebi_charges | both | 10 / 10000000 * turnover | inr | SEBI charges Rs 10 per crore | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | BSE | sebi_charges | both | 10 / 10000000 * turnover | inr | SEBI charges Rs 10 per crore | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_intraday | BSE | sebi_charges | both | 10 / 10000000 * turnover | inr | SEBI charges Rs 10 per crore | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | NSE | stamp_duty | buy | 0.00015 * buy_turnover | inr | 0.015 percent or Rs 1500 per crore on buy side | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | BSE | stamp_duty | buy | 0.00015 * buy_turnover | inr | 0.015 percent or Rs 1500 per crore on buy side | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_intraday | NSE | stamp_duty | buy | 0.00003 * buy_turnover | inr | 0.003 percent or Rs 300 per crore on buy side | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_intraday | BSE | stamp_duty | buy | 0.00003 * buy_turnover | inr | 0.003 percent or Rs 300 per crore on buy side | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | NSE | gst | both | 0.18 * (brokerage + sebi_charges + transaction_charges) | inr | GST on brokerage plus SEBI plus transaction charges | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_intraday | NSE | gst | both | 0.18 * (brokerage + sebi_charges + transaction_charges) | inr | GST on brokerage plus SEBI plus transaction charges | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | BSE | gst | both | 0.18 * (brokerage + sebi_charges + transaction_charges) | inr | GST on brokerage plus SEBI plus transaction charges | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_intraday | BSE | gst | both | 0.18 * (brokerage + sebi_charges + transaction_charges) | inr | GST on brokerage plus SEBI plus transaction charges | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | NSE | dp_charges | sell | 15.34 per scrip debit transaction when delivery holding is sold | inr | DP charges are delivery-sale only and not intraday | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |
| equity_delivery | BSE | dp_charges | sell | 15.34 per scrip debit transaction when delivery holding is sold | inr | DP charges are delivery-sale only and not intraday | https://zerodha.com/charges | 2026-07-28T16:22:26.344990+00:00 |

## Latency/slippage Profile Catalog

| profile_id | decision_latency_ms | broker_network_latency_ms | slippage_ticks | spread_cross_multiplier | allowed_for_promotion | purpose |
| --- | --- | --- | --- | --- | --- | --- |
| P180_ZERO_LATENCY_CONTROL_DIAGNOSTIC_ONLY | 0 | 0 | 0 | 1 | 0 | diagnostic lower-bound only; cannot support profitability acceptance |
| P180_RETAIL_MARKETABLE_DEFAULT | 100 | 250 | 1 | 1 | 1 | base retail stress before any future replay |
| P180_STRESSED_RETAIL | 250 | 750 | 2 | 1.25 | 1 | adverse retail latency/slippage stress before any future replay |

## Label Family Precommit

| strategy_family_id | label_family_id | label_status | train_dates | validation_dates | test_dates | minimum_label_requirements | cost_latency_binding_required | replay_allowed_after_phase180 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P179_SOURCE_QUALITY_REGIME_FILTER | future_mid_or_spread_adjusted_return_label_precommitted_after_phase179 | precommitted_not_materialized | 2026-07-08;2026-07-09;2026-07-10 | 2026-07-13 | 2026-07-14 | event-time causal;feature_timestamp_before_label_horizon;no_test_date_selection;coverage_by_symbol_date | zerodha_equity_cost_catalog_plus_receive_to_order_latency_catalog_before_replay | 0 |
| P179_LIQUIDITY_CHURN_CONTEXT | execution_risk_or_spread_transition_label_precommitted_after_phase179 | precommitted_not_materialized | 2026-07-08;2026-07-09;2026-07-10 | 2026-07-13 | 2026-07-14 | event-time causal;feature_timestamp_before_label_horizon;no_test_date_selection;coverage_by_symbol_date | zerodha_equity_cost_catalog_plus_slippage_latency_stress_before_replay | 0 |
| P179_RECEIVE_CADENCE_SHOCK_CONTEXT | short_horizon_direction_or_volatility_label_precommitted_after_phase179 | precommitted_not_materialized | 2026-07-08;2026-07-09;2026-07-10 | 2026-07-13 | 2026-07-14 | event-time causal;feature_timestamp_before_label_horizon;no_test_date_selection;coverage_by_symbol_date | zerodha_equity_cost_catalog_plus_latency_queue_before_replay | 0 |

## Gate Evaluation

| gate_id | gate_pass | evidence | severity |
| --- | --- | --- | --- |
| P180_PHASE179_PRECOMMIT_READY | 1 | phase179_precommit_ready=1 | hard |
| P180_ZERODHA_COST_COMPONENTS_PINNED | 1 | observed_components=brokerage;dp_charges;gst;sebi_charges;stamp_duty;stt;transaction_charges | hard |
| P180_OFFICIAL_COST_SOURCE_RECORDED | 1 | official Zerodha charge and STT URLs recorded | hard |
| P180_LATENCY_STRESS_PROFILES_DECLARED | 1 | profiles=3;promotion_eligible_profiles=2 | hard |
| P180_LABEL_FAMILIES_PRECOMMITTED | 1 | label_rows=3;replay_allowed_sum=0 | hard |
| P180_NO_REPLAY_OR_PROFITABILITY_OUTPUTS | 1 | cost/latency/label precommit only; forbidden_outputs=signal;order;order_arrival;fill_model;pnl_replay;profitability_claim;paper_live_acceptance | hard |

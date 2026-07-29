# Phase234 Real-anchor or Sealed-holdout Preparation Report

Generated UTC: 2026-07-29T06:38:31.210084+00:00

Phase234 responds to the profitable Phase231/232/233 synthetic microprice-reversal result by selecting the next executable holdout path.
It does not tune the strategy, run paper/live trading, or unlock a deployable profitability claim.

Selected route: `P234_REAL_ANCHOR_EVENT_BAR_ADAPTER_PREP`.
Next action: `run_phase235_build_real_anchor_event_bar_microprice_reversal_adapter_no_paper_live`.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase234_holdout_preparation_complete | 1 | Phase234 route preparation completed |
| phase234_parent_candidate_id | P231_MICROPRICE_REVERSAL_H3_Q0_9 | Candidate carried forward from Phase233 |
| phase234_phase233_fragility_realism_pass | 1 | Phase233 survivor pass flag |
| phase234_required_schema_rows | 11 | Required schema mapping rows evaluated |
| phase234_required_schema_present_rows | 11 | Required schema rows present in local real L2 sample |
| phase234_real_anchor_route_ready | 1 | Whether the next best action can use local real L2 adapter preparation |
| phase234_selected_route_id | P234_REAL_ANCHOR_EVENT_BAR_ADAPTER_PREP | Selected holdout route |
| phase234_phase235_work_order_rows | 4 | Concrete work-order rows for Phase235 |
| phase234_hard_gate_pass_rows | 6 | Hard Phase234 gates passed |
| phase234_hard_gate_rows | 6 | Hard Phase234 gates evaluated |
| phase234_strategy_replay_execution_allowed_now | 0 | Phase234 does not execute strategy replay |
| phase234_strategy_promotion_allowed | 0 | No strategy promotion from Phase234 |
| phase234_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase234 |
| phase234_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase234 |
| phase234_next_best_action | run_phase235_build_real_anchor_event_bar_microprice_reversal_adapter_no_paper_live | Recommended next milestone |

## Candidate Handoff

| candidate_id | phase233_fragility_realism_pass | family_id | signal_rule | signal_source | horizon_event_bars | threshold_quantile | event_window_score_threshold | abs_microprice_dev_threshold | synthetic_train_net_pnl_inr | synthetic_test_net_pnl_inr | synthetic_test_2x_cost_net_pnl_inr | zerodha_cost_model_version | promotion_allowed | paper_or_live_acceptance_allowed | deployable_profitability_claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P231_MICROPRICE_REVERSAL_H3_Q0_9 | 1 | P231_MICROPRICE_REVERSAL | reversal: go opposite the event-bar average microprice deviation | avg_microprice_dev | 3 | 0.9 | 54.3162 | 0.00010257 | 353035 | 229963 | 179610 | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | 0 | 0 | 0 |

## Real-anchor Readiness

| check_id | passed | observed_value | required_value | interpretation |
| --- | --- | --- | --- | --- |
| P234_PHASE233_SYNTHETIC_CANDIDATE_SURVIVED | True | 1 | Phase233 pass=1 | Filled after candidate handoff is built. |
| P234_LOCAL_REAL_PARQUET_CATALOG_EXISTS | True | 99272 | >0 local Parquet files | Download-first real L2 storage is available locally. |
| P234_MIN_REAL_RECEIVE_FLOW_DAYS | True | 7 | >=5 ready receive-flow dates | Enough real days exist for a small real-anchor adapter trial. |
| P234_SCHEMA_SUPPORTS_MICROPRICE_REVERSAL | True | 11 | 11 / 11 required schema rows present | Raw real ticks contain the fields needed to compute event bars and microprice reversal inputs. |
| P234_EVENT_BAR_ADAPTER_ALREADY_EXISTS | False | 0 | Phase235 adapter not yet built | Phase234 does not pretend strategy replay already exists on real L2; it creates the next executable adapter work order. |

## Schema Mapping

| required_feature | source_column_or_family | present_in_real_l2_schema | missing_columns | purpose |
| --- | --- | --- | --- | --- |
| receive_order | collector_received_utc_ms | True |  | Required to replay websocket receive order and event-bar chronology. |
| monotonic_tiebreak | collector_received_monotonic_ns | True |  | Required when multiple ticks share the same receive millisecond. |
| trade_date | trade_date | True |  | Required for day partitioning and holdout split. |
| symbol | tradingsymbol | True |  | Required for symbol-level event bars. |
| last_price | last_price | True |  | Required for event-bar close price and return labels. |
| volume | volume_traded | True |  | Required for volume deltas and event-window intensity. |
| level1_bid_price | buy_1_price | True |  | Required for mid price and microprice. |
| level1_bid_quantity | buy_1_quantity | True |  | Required for microprice. |
| level1_ask_price | sell_1_price | True |  | Required for mid price and microprice. |
| level1_ask_quantity | sell_1_quantity | True |  | Required for microprice. |
| top_five_market_by_price_depth | buy_1_price..buy_5_orders/sell_1_price..sell_5_orders | True |  | Required for top-five market-by-price context and book-valid filtering. |

## Phase235 Work Order

| step_order | phase235_task | candidate_id | implementation_detail | acceptance_evidence |
| --- | --- | --- | --- | --- |
| 1 | materialize_real_event_bars | P231_MICROPRICE_REVERSAL_H3_Q0_9 | Read local real L2 Parquet partitions; sort by collector_received_utc_ms and collector_received_monotonic_ns; build per-symbol/day event bars. | Real event-bar row counts by date/symbol with no paper/live execution. |
| 2 | compute_microprice_reversal_features | P231_MICROPRICE_REVERSAL_H3_Q0_9 | Compute mid price, L1 microprice, avg_microprice_dev, event_window_score, and forward 3-event-bar close-mid return labels. | Feature quality ledger including missingness, stale-book filtering, gap segmentation and top-five market-by-price schema coverage. |
| 3 | dry_run_real_anchor_candidate | P231_MICROPRICE_REVERSAL_H3_Q0_9 | Replay the frozen Phase233 thresholds and Zerodha equity intraday NSE cost model on local real-anchor event bars only. | Train-free real-anchor summary; no parameter tuning on real data and no promotion claim. |
| 4 | controls_and_decision | P231_MICROPRICE_REVERSAL_H3_Q0_9 | Run side-flip, random-side, cost stress, date/symbol concentration and stale-feed exclusion controls before deciding continuation. | Phase235 gates decide whether to continue, redesign, or close the candidate. |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | interpretation | severity |
| --- | --- | --- | --- | --- | --- |
| P234_PHASE233_SYNTHETIC_CANDIDATE_SURVIVED | True | 1 | Phase233 pass=1 | Filled after candidate handoff is built. | hard |
| P234_LOCAL_REAL_PARQUET_CATALOG_EXISTS | True | 99272 | >0 local Parquet files | Download-first real L2 storage is available locally. | hard |
| P234_MIN_REAL_RECEIVE_FLOW_DAYS | True | 7 | >=5 ready receive-flow dates | Enough real days exist for a small real-anchor adapter trial. | hard |
| P234_SCHEMA_SUPPORTS_MICROPRICE_REVERSAL | True | 11 | 11 / 11 required schema rows present | Raw real ticks contain the fields needed to compute event bars and microprice reversal inputs. | hard |
| P234_EVENT_BAR_ADAPTER_ALREADY_EXISTS | False | 0 | Phase235 adapter not yet built | Phase234 does not pretend strategy replay already exists on real L2; it creates the next executable adapter work order. | info |
| P234_REAL_ANCHOR_OR_SEALED_HOLDOUT_ROUTE_SELECTED | True | P234_REAL_ANCHOR_EVENT_BAR_ADAPTER_PREP | explicit route decision | Phase234 always exits with a concrete next experiment. | hard |
| P234_NO_PAPER_LIVE_OR_PROMOTION_UNLOCK | True | 0 | 0 | Phase234 prepares the next experiment without changing paper/live boundaries. | hard |
| P234_REAL_ANCHOR_ADAPTER_ROUTE_READY | True | 1 | 1 | Whether the next best experiment can use local real L2 immediately. | soft |

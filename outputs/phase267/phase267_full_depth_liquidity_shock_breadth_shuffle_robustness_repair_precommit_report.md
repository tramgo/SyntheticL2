# Phase267 Full-depth Liquidity-shock Breadth and Shuffle-robustness Repair Precommit

Generated UTC: 2026-08-02T02:27:58.484154+00:00

Phase267 freezes the repair contract after Phase266 found that the Phase265 lead was 2x-cost positive but too sparse and effectively indistinguishable from the shuffled-label control.
The repair preserves the core project objective: Zerodha top-five market-by-price rows 1-5 are mandatory, levels 2-5 must be material, and L1-only variants are forbidden.
This is a precommit only. It does not download data, execute replay, promote a strategy, open paper/live acceptance, or make a deployable profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase267_breadth_shuffle_repair_precommit_complete | 1 | Phase267 full-depth breadth/shuffle robustness repair precommit completed |
| phase267_selected_route | P267_FULL_DEPTH_LIQUIDITY_SHOCK_BREADTH_SHUFFLE_ROBUSTNESS_REPAIR | Selected route |
| phase267_phase266_interpretation_complete | 1 | Phase266 interpretation complete |
| phase267_phase266_full_depth_preserved | 1 | Phase266 preserved full depth |
| phase267_phase266_close_phase265_for_replay | 1 | Phase266 closed replay |
| phase267_phase266_best_cost200_avg_net_per_event_inr | 4.211649981625751 | Phase266 best 2x average edge |
| phase267_phase266_best_shuffle_label_margin_inr | 1.1368683772161603e-13 | Phase266 best shuffled-label margin |
| phase267_repair_feature_catalog_rows | 17 | Repair feature catalog rows |
| phase267_candidate_family_rows | 5 | Candidate family rows |
| phase267_acceptance_floor_rows | 17 | Acceptance floor rows |
| phase267_search_grid_contract_rows | 10 | Search grid contract rows |
| phase267_control_contract_rows | 14 | Control contract rows |
| phase267_exploratory_lane_enabled | 1 | Keep positive/near-positive small pockets as non-accepted research leads |
| phase267_exploratory_controls_are_filters | 0 | Exploratory controls are metrics, not hard filters |
| phase267_exploratory_min_event_rows | 5 | Minimum event rows for exploratory candidate ledger inclusion |
| phase267_exploratory_min_symbols | 2 | Minimum symbols for exploratory candidate ledger inclusion |
| phase267_acceptance_min_event_rows | 30 | Minimum event rows for acceptance-grade survival |
| phase267_acceptance_min_symbols | 8 | Minimum symbols for acceptance-grade survival |
| phase267_acceptance_min_trade_dates_current_data | 1 | Minimum dates on current one-date training data |
| phase267_acceptance_min_cost200_avg_net_per_event_inr | 25 | Minimum 2x average net/event for acceptance-grade survival |
| phase267_acceptance_min_shuffle_label_margin_inr | 100 | Minimum shuffled-label margin for acceptance-grade survival |
| phase267_full_top_five_depth_required | 1 | Zerodha rows 1-5 required |
| phase267_levels_2_to_5_materiality_required | 1 | Levels 2-5 materiality required |
| phase267_l1_only_candidate_allowed | 0 | L1-only candidates forbidden |
| phase267_threshold_relaxation_only_allowed | 0 | Threshold-relaxation-only continuation forbidden |
| phase267_hard_gate_pass_rows | 12 | Hard gates passed |
| phase267_hard_gate_rows | 12 | Hard gates evaluated |
| phase267_download_more_dates_now_allowed | 0 | No new download in Phase267 |
| phase267_replay_execution_allowed_now | 0 | No replay execution in Phase267 |
| phase267_strategy_promotion_allowed | 0 | No strategy promotion from Phase267 |
| phase267_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase267 |
| phase267_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase267 |
| phase267_next_best_action | run_phase268_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_training_search_no_paper_live | Recommended next milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P267_PHASE266_WORK_ORDER_PRESENT | True | run_phase267_full_depth_liquidity_shock_breadth_shuffle_robustness_repair_precommit_no_paper_live | Phase266 next action targets Phase267 | hard |
| P267_PHASE266_FULL_DEPTH_PRESERVED | True | 1 | Phase266 preserved full top-five depth | hard |
| P267_PHASE266_CLOSED_REPLAY | True | 1 | Phase266 closed Phase265 for replay | hard |
| P267_PHASE266_FORBIDS_THRESHOLD_RELAXATION_ONLY | True | 0 | threshold-relaxation-only continuation forbidden | hard |
| P267_PHASE266_DEPTH_CONTRACT_PRESENT | True | 1 | Phase266 route requires rows 1-5 and L2-L5 | hard |
| P267_PHASE266_REPAIR_CONTRACT_PRESENT | True | 1 | Phase266 route targets breadth and shuffle robustness | hard |
| P267_REPAIR_FEATURE_CATALOG_WRITTEN | True | 17 | feature catalog includes full-depth requirements and forbidden L1-only row | hard |
| P267_CANDIDATE_FAMILIES_WRITTEN | True | 5 | >=5 candidate families, all requiring levels 2-5 | hard |
| P267_TWO_LANE_FLOORS_WRITTEN | True | 17 | exploratory and acceptance lane floors present | hard |
| P267_SEARCH_GRID_WRITTEN | True | 10 | >=8 search-grid contract rows | hard |
| P267_CONTROLS_WRITTEN | True | 14 | full-depth, L2-L5, exploratory lane, acceptance shuffle-margin and threshold-relaxation controls present | hard |
| P267_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

## Repair Feature Catalog

| feature_group | feature | description | status |
| --- | --- | --- | --- |
| full_depth_core | avg_cum_buy_qty_l1_l5 | Full visible bid quantity across Zerodha rows 1-5 | required |
| full_depth_core | avg_cum_sell_qty_l1_l5 | Full visible ask quantity across Zerodha rows 1-5 | required |
| l2_l5_core | avg_cum_buy_qty_l2_l5 | Bid-side depth beyond L1; required levels 2-5 materiality | required |
| l2_l5_core | avg_cum_sell_qty_l2_l5 | Ask-side depth beyond L1; required levels 2-5 materiality | required |
| l2_l5_core | avg_depth_beyond_l1_qty_imbalance | Levels 2-5 quantity imbalance | required |
| l2_l5_core | avg_level_weighted_depth_imbalance | Top-five level-weighted depth imbalance | required |
| l2_l5_core | avg_order_count_imbalance_l1_l5 | Top-five order-count imbalance | required |
| shock | depth_replenishment_pressure | Visible-depth replenishment pressure | required |
| shock | depth_withdrawal_pressure | Visible-depth withdrawal pressure | required |
| shock | top5_qty_churn_sum | Top-five quantity churn / book instability | required |
| shock | top5_order_churn_sum | Top-five order-count churn / cancel pressure | required |
| spread_regime | avg_spread_bps | Spread regime and cost context | required |
| spread_regime | spread_compression_bps | Spread compression confirmation | required |
| market_regime | market_direction_proxy | Optional broad-market direction guard if available in the event surface | optional |
| market_regime | market_volatility_proxy | Optional market volatility guard if available in the event surface | optional |
| cost | zerodha_round_trip_charge_bps | Zerodha modeled round-trip charge floor | required |
| forbidden | l1_only_depth_imbalance | L1-only feature set is forbidden | forbidden |

## Candidate Family Contract

| candidate_family_id | direction_space | description | required_features | requires_levels_2_to_5 |
| --- | --- | --- | --- | --- |
| P268_BID_ABSORPTION_BREADTH_REPAIR | long | Bid-side L2-L5 absorption/continuation, broadened from the Phase265 lead but forced through breadth and shuffled-label margin floors. | avg_cum_buy_qty_l2_l5;avg_depth_beyond_l1_qty_imbalance;avg_level_weighted_depth_imbalance;depth_replenishment_pressure;top5_qty_churn_sum | 1 |
| P268_ASK_ABSORPTION_BREADTH_REPAIR | short | Ask-side L2-L5 absorption/continuation with identical breadth and shuffled-label robustness floors. | avg_cum_sell_qty_l2_l5;avg_depth_beyond_l1_qty_imbalance;avg_level_weighted_depth_imbalance;depth_replenishment_pressure;top5_qty_churn_sum | 1 |
| P268_SPREAD_COMPRESSION_ABSORPTION_REPAIR | long_or_short | Spread-compression confirmation after book shock, requiring top-five and L2-L5 imbalance agreement. | avg_spread_bps;spread_compression_bps;avg_cum_top5_qty_imbalance;avg_depth_beyond_l1_qty_imbalance;top5_qty_churn_sum | 1 |
| P268_WITHDRAWAL_REVERSAL_ROBUSTNESS_REPAIR | long_or_short | Withdrawal/churn reversal only when opposite-side L2-L5 replenishment confirms absorption. | depth_withdrawal_pressure;top5_order_churn_sum;avg_cum_buy_qty_l2_l5;avg_cum_sell_qty_l2_l5;avg_depth_beyond_l1_qty_imbalance | 1 |
| P268_MARKET_REGIME_CONFIRMED_ABSORPTION | long_or_short | Absorption families gated by market-direction or volatility context where available; no trade if market context contradicts the book signal. | avg_depth_beyond_l1_qty_imbalance;avg_level_weighted_depth_imbalance;market_direction_proxy;market_volatility_proxy | 1 |

## Acceptance Floor Contract

| floor_id | required_expression | numeric_floor | description |
| --- | --- | --- | --- |
| exploratory_minimum_event_rows | >=5 | 5 | Profit-hunting lane keeps small but interesting pockets for diagnosis; not acceptance. |
| exploratory_minimum_symbols | >=2 | 2 | Profit-hunting lane keeps sparse cross-symbol clues; not acceptance. |
| exploratory_cost100_net_pnl_inr | >0 | 0 | Exploratory candidates may enter the ledger if base-cost net is positive. |
| exploratory_controls_as_metrics_not_filters | record_only | 0 | Side-flip, random-side and shuffled-label controls are recorded for exploratory ranking but do not suppress discovery rows. |
| acceptance_minimum_event_rows | >=30 | 30 | Acceptance-grade candidate must have enough events before replay or promotion discussion. |
| acceptance_minimum_symbols | >=8 | 8 | Acceptance-grade candidate must not be a one-name or four-name artifact. |
| acceptance_minimum_trade_dates | >=1_current_data;>=2_when_additional_unseen_dates_available | 1 | Current training data has one date; future unseen date expansion must raise this floor. |
| acceptance_cost100_net_pnl_inr | >0 | 0 | Acceptance lane base cost stack must be positive. |
| acceptance_cost150_net_pnl_inr | >0 | 0 | Acceptance lane 1.5x modeled Zerodha cost stress must be positive. |
| acceptance_cost200_net_pnl_inr | >0 | 0 | Acceptance lane 2x modeled Zerodha cost stress must be positive. |
| acceptance_cost200_avg_net_per_event_inr | >=25 | 25 | Acceptance lane rejects tiny residual 2x edges such as Phase265's about 4.21 INR/event. |
| acceptance_shuffle_label_margin_inr | >=100 | 100 | Acceptance lane must beat shuffled-label net P&L by an economically material margin. |
| acceptance_side_flip_degrades | ==1 | 1 | Acceptance lane requires flipped signal side to degrade net P&L. |
| acceptance_random_side_beat | ==1 | 1 | Acceptance lane requires deterministic random-side beat. |
| uses_full_top_five_depth | ==1 | 1 | Both lanes require rows 1-5. |
| uses_depth_beyond_l1 | ==1 | 1 | Both lanes require levels 2-5 materiality. |
| uses_l1_only | ==0 | 0 | L1-only candidate is forbidden in both lanes. |

## Search Grid Contract

| grid_component | contract_value | description |
| --- | --- | --- |
| horizons | 3;6;10 | Reuse available future mid-return horizons. |
| imbalance_quantiles | 0.50;0.60;0.75;0.90 | Include a controlled lower threshold only when breadth and shuffle margin floors remain binding. |
| shock_quantiles | 0.50;0.60;0.75;0.90 | Include a controlled lower shock threshold only under the same floors. |
| spread_regimes | low;mid;high;compression;all_with_spread_cap | Broaden context without dropping spread/cost awareness. |
| families | bid_absorption;ask_absorption;spread_compression;withdrawal_reversal;market_regime_confirmed | Repair must generalize mechanism families. |
| cost_multipliers | 1.0;1.5;2.0 | Use actual modeled Zerodha cost stack under stress. |
| shuffle_margin_modes | absolute_inr>=100;relative_to_cost200_net>=1x | Shuffled-label edge must be economically material. |
| exploratory_lane | keep_positive_or_near_positive_small_pockets_for_diagnosis | Do not over-filter discovery; preserve promising anomalies as non-accepted research leads. |
| acceptance_lane | apply_breadth_cost_shuffle_and_control_floors_before_replay_or_promotion | Controls become hard only for acceptance-grade labels, not for exploration. |
| threshold_relaxation_guard | relaxation_allowed_for_exploration_but_not_as_standalone_acceptance | Threshold widening may discover ideas, but cannot by itself create an accepted survivor. |

## Control Contract

| control_id | control_status | description |
| --- | --- | --- |
| full_depth_control | required | Every candidate must use Zerodha rows 1-5. |
| levels_2_to_5_materiality_control | required | Every candidate must include L2-L5/beyond-L1 evidence. |
| no_l1_only_control | required | Reject L1-only features and candidates. |
| exploratory_lane_control | required | Keep broad positive and near-positive pockets for inspection even when controls fail; label them exploratory only. |
| acceptance_breadth_control | required | Require minimum events, symbols and dates only before acceptance/replay/promotion. |
| acceptance_cost_stress_control | required | Require positive 1x, 1.5x and 2x modeled Zerodha-cost net P&L before acceptance. |
| acceptance_cost200_average_edge_control | required | Require cost200 average net/event >= 25 INR before acceptance. |
| acceptance_shuffle_label_margin_control | required | Require economically material shuffled-label margin >= 100 INR before acceptance. |
| acceptance_side_flip_control | required | Require side flip degradation before acceptance. |
| acceptance_random_side_control | required | Require deterministic random-side beat before acceptance. |
| threshold_relaxation_only_acceptance | forbidden | No accepted survivor may be created solely by loosening thresholds. |
| paper_live_or_deployable_profitability_claim | forbidden | No paper/live acceptance or deployable profitability claim in Phase267/268. |
| download_more_dates_now | forbidden_in_phase267 | Phase267 is a precommit; it does not download data. |
| replay_execution_now | forbidden_in_phase267 | Phase267 is not replay execution. |

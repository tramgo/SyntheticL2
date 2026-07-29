# Phase250 Pair/Basket Relative-value Precommit

Generated UTC: 2026-07-29T09:38:30.775718+00:00

Phase250 opens a materially different route after the single-name bar-return reversal branch failed cost robustness.
It precommits the Phase251 training-only search contract for pair/basket relative-value strategies using existing real event bars only.
No raw data download, replay execution, strategy promotion, paper/live acceptance or deployable profitability claim is allowed in this phase.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase250_pair_basket_precommit_complete | 1 | Phase250 pair/basket precommit completed |
| phase250_selected_route | P249_PAIR_OR_BASKET_RELATIVE_VALUE | Selected materially different route |
| phase250_training_event_bar_rows | 28793 | Existing Phase235 event-bar rows available |
| phase250_training_dates | 7 | Existing Phase235 dates available before forbidden-date exclusion |
| phase250_training_symbols | 32 | Existing Phase235 symbols available |
| phase250_forbidden_tuning_dates | 2026-07-17,2026-07-20 | Dates excluded from Phase251 parameter selection |
| phase250_pair_group_rows | 8 | Peer groups with at least two eligible symbols |
| phase250_grouped_symbols | 29 | Symbols eligible for pair/basket construction |
| phase250_candidate_family_rows | 4 | Candidate families registered |
| phase250_feature_contract_rows | 18 | Feature contract rows |
| phase250_required_input_features_present | 1 | Required Phase235 input columns present |
| phase250_acceptance_contract_rows | 10 | Acceptance contract rows |
| phase250_hard_gate_pass_rows | 10 | Hard gates passed |
| phase250_hard_gate_rows | 10 | Hard gates evaluated |
| phase250_phase251_training_search_allowed_next | 1 | Whether Phase251 training search is allowed next |
| phase250_download_more_dates_now_allowed | 0 | No raw-date download in Phase250 |
| phase250_replay_execution_allowed_now | 0 | No replay execution in Phase250 |
| phase250_strategy_promotion_allowed | 0 | No strategy promotion from Phase250 |
| phase250_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from Phase250 |
| phase250_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from Phase250 |
| phase250_next_best_action | run_phase251_training_only_pair_basket_relative_value_search_no_downloads_no_2026_07_17_or_2026_07_20_tuning_no_paper_live | Recommended next milestone |

## Pair/Basket Universe

| symbol | peer_group_id | group_size_available | role | phase251_allowed | notes |
| --- | --- | --- | --- | --- | --- |
| BAJAJ-AUTO | auto | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| M&M | auto | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| MARUTI | auto | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| AXISBANK | bank_finance | 5 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| HDFCBANK | bank_finance | 5 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| ICICIBANK | bank_finance | 5 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| KOTAKBANK | bank_finance | 5 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| SBIN | bank_finance | 5 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| BRITANNIA | consumer | 4 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| HINDUNILVR | consumer | 4 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| ITC | consumer | 4 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| NESTLEIND | consumer | 4 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| BPCL | energy | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| ONGC | energy | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| RELIANCE | energy | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| BANKBEES | index_etf_basket | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| JUNIORBEES | index_etf_basket | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| NIFTYBEES | index_etf_basket | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| HCLTECH | information_technology | 5 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| INFY | information_technology | 5 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| TCS | information_technology | 5 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| TECHM | information_technology | 5 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| WIPRO | information_technology | 5 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| ADANIPORTS | infra_capital_goods | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| LT | infra_capital_goods | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| ULTRACEMCO | infra_capital_goods | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| CIPLA | pharma | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| DRREDDY | pharma | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| SUNPHARMA | pharma | 3 | pair_and_basket | 1 | eligible for peer residuals and market-neutral baskets |
| BHARTIARTL | benchmark_or_singleton | 1 | benchmark_or_excluded | 0 | single telecom name in current universe; usable only against broad basket unless a telecom peer appears |
| GOLDBEES | benchmark_or_singleton | 1 | benchmark_or_excluded | 0 | commodity ETF; keep out of equity-sector pair residuals |
| ITBEES | benchmark_or_singleton | 1 | benchmark_or_excluded | 0 | sector ETF; usable as IT basket reference, not as a single-name equity peer |

## Feature Contract

| feature_name | source_stage | required_for_phase251 | present_now | purpose |
| --- | --- | --- | --- | --- |
| trade_date | input | 1 | 1 | date partition and train/holdout exclusion key |
| symbol | input | 1 | 1 | cross-sectional and peer grouping key |
| source_event_bar_id | input | 1 | 1 | same event-bar clock used for cross-symbol alignment |
| open_mid_price | input | 1 | 1 | event-bar opening mid |
| close_mid_price | input | 1 | 1 | event-bar closing mid and future-return anchor |
| bar_return | input | 1 | 1 | symbol event-bar return used for residual construction |
| avg_top5_market_by_price_imbalance | input | 1 | 1 | top-five market-by-price depth imbalance, not universal L5 data |
| avg_l1_imbalance | input | 1 | 1 | secondary top-of-book pressure check |
| avg_spread | input | 1 | 1 | liquidity/spread guard |
| avg_event_intensity_proxy | input | 1 | 1 | activity/volume-style guard |
| taker_round_trip_cost_floor_bps | input | 1 | 1 | modeled Zerodha cost and spread floor |
| abs_bar_return_bps | input | 1 | 1 | recent move magnitude / volatility comparison proxy |
| peer_group_id | phase251_derived | 1 | 1 | static group assignment from the Phase250 universe catalog |
| basket_return | phase251_derived | 1 | 1 | leave-one-out peer or benchmark basket return |
| symbol_residual_return | phase251_derived | 1 | 1 | symbol return minus basket return |
| relative_top5_imbalance | phase251_derived | 1 | 1 | symbol top-five imbalance minus peer/basket imbalance |
| cross_sectional_rank | phase251_derived | 1 | 1 | within-event residual rank used for long/short baskets |
| market_beta_proxy | phase251_optional | 0 | 1 | rough broad-basket sensitivity; do not tune on forbidden dates |

## Candidate Family Catalog

| family_id | hypothesis | required_inputs | top_five_depth_use | market_neutrality |
| --- | --- | --- | --- | --- |
| P250_SECTOR_PAIR_RESIDUAL_REVERSION | A stock stretched versus its same-sector peer basket reverts after common market movement is hedged. | bar_return, peer_group_id, basket_return, symbol_residual_return, taker_round_trip_cost_floor_bps | veto residual reversion when top-five imbalance confirms continuation pressure | long/short pair or leave-one-out sector basket |
| P250_INDEX_BASKET_RESIDUAL_REVERSION | A stock residual versus NIFTYBEES/BANKBEES/JUNIORBEES style baskets reverts only when cost floor is small. | bar_return, benchmark basket return, symbol_residual_return, spread and cost floor | require depth pressure to disagree with the stretched price impulse | single stock versus benchmark ETF proxy where available |
| P250_TOP5_IMBALANCE_RELATIVE_DIVERGENCE | Relative top-five depth pressure predicts near-term convergence better than absolute bar reversal. | avg_top5_market_by_price_imbalance, relative_top5_imbalance, future close-mid return | primary signal source rather than a decorative filter | ranked long/short within sector or broad basket |
| P250_MARKET_NEUTRAL_LONG_SHORT_BASKET | Long the strongest residual/depth-confirmed names and short the weakest residual/depth-confirmed names within each event window. | cross_sectional_rank, symbol_residual_return, relative_top5_imbalance, cost floor | must support selected long/short ranks after spread/liquidity filtering | notional-balanced long and short legs; costs applied per leg |

## Acceptance Contract

| contract_id | requirement | severity |
| --- | --- | --- |
| P250_NO_FORBIDDEN_TUNING_DATES | Phase251 search must exclude 2026-07-17 and 2026-07-20 from parameter selection. | hard |
| P250_EXISTING_BARS_ONLY | Phase251 starts from existing Phase235 real event bars; no new raw L2 download until a frozen materially new survivor exists. | hard |
| P250_MIN_GROUPS | At least 5 peer groups with 2 or more available symbols must be present. | hard |
| P250_MIN_GROUPED_SYMBOLS | At least 20 symbols must be eligible for peer/basket construction. | hard |
| P250_MARKET_NEUTRAL_NOTIONALS | Pair/basket variants must balance long and short notional before cost and risk scoring. | hard |
| P250_COST_PER_LEG | Zerodha-modeled costs, spread and slippage must be applied per leg; pair/basket costs are not single-leg costs. | hard |
| P250_2X_COST_FIRST | No survivor may proceed without positive 2.0x modeled-cost net P&L. | hard |
| P250_CONTROLS_REQUIRED | Side-flip, random-side, concentration and cost-stress controls remain mandatory. | hard |
| P250_BREADTH_REQUIRED | Any training survivor must use at least 4 dates, 8 symbols and 20 trades before holdout precommit. | hard |
| P250_NO_PROFIT_CLAIM | Phase250 is a precommit only: no replay execution, paper/live acceptance or deployable profitability claim. | hard |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P250_PHASE249_ROUTE_SELECTED | True | P249_PAIR_OR_BASKET_RELATIVE_VALUE | P249_PAIR_OR_BASKET_RELATIVE_VALUE | hard |
| P250_PHASE249_WORK_ORDER_PRESENT | True | run_phase250_pair_basket_relative_value_precommit_no_downloads_no_2026_07_17_or_2026_07_20_tuning_no_paper_live | Phase249 next action points to Phase250 pair/basket precommit | hard |
| P250_EVENT_BARS_AVAILABLE | True | 28793 | >0 Phase235 real event bars | hard |
| P250_FORBIDDEN_DATES_NOT_USED_FOR_TUNING | True | 2026-07-17,2026-07-20 | Excluded from Phase251 parameter search | hard |
| P250_REQUIRED_INPUT_FEATURES_PRESENT | True | 1 | all required input features present | hard |
| P250_MIN_GROUPS_AVAILABLE | True | 8 | >=5 peer groups | hard |
| P250_MIN_GROUPED_SYMBOLS_AVAILABLE | True | 29 | >=20 eligible grouped symbols | hard |
| P250_CANDIDATE_FAMILIES_REGISTERED | True | 4 | >=4 materially different pair/basket families | hard |
| P250_ACCEPTANCE_CONTRACT_REGISTERED | True | 10 | >=10 acceptance contract rows | hard |
| P250_NO_DOWNLOAD_REPLAY_PROMOTION_OR_PAPER_LIVE | True | 0 | 0 | hard |

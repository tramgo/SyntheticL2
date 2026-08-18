# Phase472 Score-to-Signal Replay Cost200

Phase472 replays Phase471 holdout scores with fixed reusable capital, Zerodha equity intraday NSE charges, and adverse round-trip slippage.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase472_score_to_signal_replay_cost200_complete | 1 | Phase472 replay completed |
| phase472_thesis_id | P472_SCORE_TO_SIGNAL_REPLAY_COST200 | Replay thesis |
| phase472_best_primary_scenario_id | primary_threshold_0.60_cost200 | Best primary scenario |
| phase472_best_primary_trade_count | 91 | Trade count |
| phase472_best_primary_net_pnl_inr | -8149.31 | Best primary net P&L |
| phase472_best_primary_annualized_return_pct | -97.7917 | Fixed-capital annualized return |
| phase472_best_primary_avg_net_per_trade_inr | -89.5528 | Average net per trade |
| phase472_primary_above12_scenario_rows | 0 | Primary scenarios above 12% annualized |
| phase472_fixed_capital_inr | 100000 | Reusable capital denominator |
| phase472_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model version |
| phase472_zerodha_cost_source_url | https://zerodha.com/charges/ | Cost source |
| phase472_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase472_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase472_phase473_allowed_next | 0 | Allows expanded validation if all gates pass |
| phase472_hard_gate_pass_rows | 7 | Passed hard gates |
| phase472_hard_gate_rows | 10 | Hard gates |
| phase472_next_best_action | interpret_phase472_costed_replay_failure_before_tuning | Recommended next action |

## Scenario Summary

| scenario_id | trade_count | unique_trade_dates | gross_pnl_inr | zerodha_total_charges_inr | adverse_slippage_inr | net_pnl_inr | win_rate | avg_net_per_trade_inr | annualized_return_pct | max_daily_drawdown_inr | model_name | threshold | fixed_capital_inr | adverse_slippage_round_trip_bps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| primary_threshold_0.50_cost200 | 309 | 21 | 2400.71 | 25515.1 | 6133.44 | -29247.8 | 0.02589 | -94.6531 | -350.974 | -27203.1 | primary | 0.5 | 100000 | 2 |
| primary_threshold_0.52_cost200 | 251 | 21 | 1702.42 | 20725 | 4981.86 | -24004.4 | 0.0239044 | -95.6352 | -288.053 | -22405.5 | primary | 0.52 | 100000 | 2 |
| primary_threshold_0.54_cost200 | 212 | 21 | 1221.54 | 17506 | 4208.58 | -20493 | 0.0235849 | -96.6651 | -245.916 | -19102.8 | primary | 0.54 | 100000 | 2 |
| primary_threshold_0.56_cost200 | 173 | 21 | 1590.59 | 14285.6 | 3434.72 | -16129.7 | 0.0289017 | -93.2355 | -193.557 | -15113.6 | primary | 0.56 | 100000 | 2 |
| primary_threshold_0.58_cost200 | 132 | 21 | 1643.74 | 10898.7 | 2620.53 | -11875.5 | 0.030303 | -89.9658 | -142.506 | -11135.3 | primary | 0.58 | 100000 | 2 |
| primary_threshold_0.60_cost200 | 91 | 21 | 1173.46 | 7516.02 | 1806.74 | -8149.31 | 0.021978 | -89.5528 | -97.7917 | -7668.37 | primary | 0.6 | 100000 | 2 |
| shuffled_threshold_0.50_cost200 | 309 | 21 | -1537.89 | 25515.1 | 6133.44 | -33186.5 | 0.012945 | -107.4 | -398.238 | -30853.3 | shuffled | 0.5 | 100000 | 2 |
| shuffled_threshold_0.52_cost200 | 213 | 21 | -1494.23 | 17588.4 | 4228.16 | -23310.8 | 0.0187793 | -109.44 | -279.73 | -21744.7 | shuffled | 0.52 | 100000 | 2 |
| shuffled_threshold_0.54_cost200 | 139 | 21 | -1017.37 | 11477.5 | 2758.55 | -15253.4 | 0.00719424 | -109.737 | -183.041 | -14708.2 | shuffled | 0.54 | 100000 | 2 |
| shuffled_threshold_0.56_cost200 | 76 | 21 | -373.845 | 6274.22 | 1507.51 | -8155.57 | 0.0131579 | -107.31 | -97.8668 | -7881.72 | shuffled | 0.56 | 100000 | 2 |
| shuffled_threshold_0.58_cost200 | 46 | 21 | -313.302 | 3797.18 | 912.09 | -5022.57 | 0.0217391 | -109.186 | -60.2709 | -4895.49 | shuffled | 0.58 | 100000 | 2 |
| shuffled_threshold_0.60_cost200 | 25 | 21 | -167.972 | 2063.31 | 494.808 | -2726.09 | 0 | -109.043 | -32.713 | -2599.01 | shuffled | 0.6 | 100000 | 2 |
| l25_threshold_threshold_0.50_cost200 | 309 | 21 | -787.025 | 25515.1 | 6133.44 | -32435.6 | 0.00970874 | -104.97 | -389.227 | -29907.3 | l25_threshold | 0.5 | 100000 | 2 |
| l25_threshold_threshold_0.52_cost200 | 297 | 21 | -834.522 | 24524 | 5895.42 | -31253.9 | 0.010101 | -105.232 | -375.047 | -28880.7 | l25_threshold | 0.52 | 100000 | 2 |
| l25_threshold_threshold_0.54_cost200 | 285 | 21 | -711.507 | 23532.5 | 5656.79 | -29900.8 | 0.0105263 | -104.915 | -358.81 | -27658.3 | l25_threshold | 0.54 | 100000 | 2 |
| l25_threshold_threshold_0.56_cost200 | 271 | 21 | -957.357 | 22375.9 | 5378.56 | -28711.9 | 0.0110701 | -105.948 | -344.542 | -26469.3 | l25_threshold | 0.56 | 100000 | 2 |
| l25_threshold_threshold_0.58_cost200 | 259 | 21 | -907.992 | 21384.6 | 5140.24 | -27432.9 | 0.011583 | -105.918 | -329.195 | -25262.3 | l25_threshold | 0.58 | 100000 | 2 |
| l25_threshold_threshold_0.60_cost200 | 247 | 21 | -1016.13 | 20394.4 | 4901.97 | -26312.5 | 0.0121457 | -106.528 | -315.75 | -24217.3 | l25_threshold | 0.6 | 100000 | 2 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P472_PHASE471_MODEL_USED | True | 1 | 1 | hard |
| P472_SCENARIOS_PRESENT | True | 18 | 18 | hard |
| P472_FIXED_CAPITAL_USED | True | 100000 | 100000 | hard |
| P472_ZERODHA_COSTS_INCLUDED | True | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | zerodha_cost_model | hard |
| P472_COST200_SLIPPAGE_INCLUDED | True | 2 | 2 | hard |
| P472_PRIMARY_POSITIVE_SCENARIO_EXISTS | False | 0 | >0 | hard |
| P472_PRIMARY_ABOVE_12PCT_ANNUALIZED_EXISTS | False | 0 | >0 | hard |
| P472_BEST_PRIMARY_TRADE_COUNT_GE_10 | True | 91 | >=10 | hard |
| P472_BEST_PRIMARY_BEATS_BEST_SHUFFLED | False | primary=-97.79167082366413;shuffled=-32.713032380419534 | primary>shuffled | hard |
| P472_NO_PAPER_LIVE_OR_CLAIM | True | replay_only;paper=0;live=0 | no_paper_live | hard |

Boundary: Phase472 is synthetic holdout replay evidence only. It is not paper/live acceptance and not a deployable profitability claim.

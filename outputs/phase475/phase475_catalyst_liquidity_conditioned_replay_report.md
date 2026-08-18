# Phase475 Catalyst/Liquidity-Conditioned Replay

Phase475 conditions the Phase474 synthetic branch on catalyst/shock flags and entry-time L1-L5 liquidity-vacuum features, then replays top-confidence holdout trades with Zerodha cost200.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase475_catalyst_liquidity_conditioned_replay_complete | 1 | Phase475 conditioned replay completed |
| phase475_thesis_id | P475_CATALYST_LIQUIDITY_CONDITIONED_REPLAY | Conditioned replay thesis |
| phase475_best_scenario_id | horizon_480_shock_only_top_0.05_cost200 | Best scenario |
| phase475_best_trade_count | 10 | Best trade count |
| phase475_best_net_pnl_inr | -232.243 | Best net P&L |
| phase475_best_annualized_return_pct | -2.66024 | Best fixed-capital annualized return |
| phase475_positive_net_scenario_rows | 0 | Positive net scenarios |
| phase475_above12_annualized_scenario_rows | 0 | Scenarios above 12% annualized |
| phase475_fixed_capital_inr | 100000 | Reusable capital denominator |
| phase475_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model version |
| phase475_zerodha_cost_source_url | https://zerodha.com/charges/ | Cost source |
| phase475_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase475_deployable_profitability_claim_allowed | 0 | No deployable claim |
| phase475_phase476_allowed_next | 0 | Allows expansion only if all gates pass |
| phase475_hard_gate_pass_rows | 9 | Passed hard gates |
| phase475_hard_gate_rows | 11 | Hard gates |
| phase475_next_best_action | interpret_phase475_conditioned_replay_failure_or_return_to_real_date_expansion | Recommended next action |

## Train-Only Filter Thresholds

| horizon_ticks | spread_q75 | spread_vol_q75 | l25_abs_imbalance_q75 | l25_ofi_abs_q75 |
| --- | --- | --- | --- | --- |
| 480 | 2.4311 | 0.000434526 | 0.439597 | 122 |
| 960 | 2.4311 | 0.000434526 | 0.439597 | 122 |
| 1800 | 2.4311 | 0.000434526 | 0.439597 | 122 |

## Scenario Summary

| scenario_id | horizon_ticks | filter_id | top_fraction | candidate_rows_after_filter | trade_count | holdout_days | gross_pnl_inr | zerodha_total_charges_inr | adverse_slippage_inr | net_pnl_inr | annualized_return_pct | win_rate | avg_net_per_trade_inr | max_daily_drawdown_inr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| horizon_480_shock_only_top_0.05_cost200 | 480 | shock_only | 0.05 | 56 | 10 | 22 | 792.26 | 826.019 | 198.484 | -232.243 | -2.66024 | 0.3 | -23.2243 | -361.132 |
| horizon_480_shock_only_top_0.10_cost200 | 480 | shock_only | 0.1 | 56 | 10 | 22 | 792.26 | 826.019 | 198.484 | -232.243 | -2.66024 | 0.3 | -23.2243 | -361.132 |
| horizon_480_shock_only_top_0.20_cost200 | 480 | shock_only | 0.2 | 56 | 11 | 22 | 808.004 | 908.7 | 218.482 | -319.178 | -3.65603 | 0.272727 | -29.0161 | -361.132 |
| horizon_480_liquidity_vacuum_top_0.05_cost200 | 480 | liquidity_vacuum | 0.05 | 54 | 10 | 22 | 544.275 | 826.209 | 198.815 | -480.749 | -5.50676 | 0.3 | -48.0749 | -609.638 |
| horizon_480_liquidity_vacuum_top_0.10_cost200 | 480 | liquidity_vacuum | 0.1 | 54 | 10 | 22 | 544.275 | 826.209 | 198.815 | -480.749 | -5.50676 | 0.3 | -48.0749 | -609.638 |
| horizon_480_liquidity_vacuum_top_0.20_cost200 | 480 | liquidity_vacuum | 0.2 | 54 | 11 | 22 | 529.295 | 908.813 | 218.669 | -598.187 | -6.85196 | 0.272727 | -54.3806 | -727.076 |
| horizon_480_shock_and_liquidity_vacuum_top_0.05_cost200 | 480 | shock_and_liquidity_vacuum | 0.05 | 34 | 10 | 22 | 743.66 | 826.019 | 198.478 | -280.837 | -3.21686 | 0.3 | -28.0837 | -409.726 |
| horizon_480_shock_and_liquidity_vacuum_top_0.10_cost200 | 480 | shock_and_liquidity_vacuum | 0.1 | 34 | 10 | 22 | 743.66 | 826.019 | 198.478 | -280.837 | -3.21686 | 0.3 | -28.0837 | -409.726 |
| horizon_480_shock_and_liquidity_vacuum_top_0.20_cost200 | 480 | shock_and_liquidity_vacuum | 0.2 | 34 | 10 | 22 | 743.66 | 826.019 | 198.478 | -280.837 | -3.21686 | 0.3 | -28.0837 | -409.726 |
| horizon_480_shock_and_l25_pressure_top_0.05_cost200 | 480 | shock_and_l25_pressure | 0.05 | 35 | 10 | 22 | 754.387 | 826.201 | 198.827 | -270.641 | -3.10007 | 0.3 | -27.0641 | -399.183 |
| horizon_480_shock_and_l25_pressure_top_0.10_cost200 | 480 | shock_and_l25_pressure | 0.1 | 35 | 10 | 22 | 754.387 | 826.201 | 198.827 | -270.641 | -3.10007 | 0.3 | -27.0641 | -399.183 |
| horizon_480_shock_and_l25_pressure_top_0.20_cost200 | 480 | shock_and_l25_pressure | 0.2 | 35 | 10 | 22 | 754.387 | 826.201 | 198.827 | -270.641 | -3.10007 | 0.3 | -27.0641 | -399.183 |
| horizon_960_shock_only_top_0.05_cost200 | 960 | shock_only | 0.05 | 56 | 10 | 22 | 377.384 | 826.174 | 198.784 | -647.574 | -7.41767 | 0.2 | -64.7574 | -287.361 |
| horizon_960_shock_only_top_0.10_cost200 | 960 | shock_only | 0.1 | 56 | 10 | 22 | 377.384 | 826.174 | 198.784 | -647.574 | -7.41767 | 0.2 | -64.7574 | -287.361 |
| horizon_960_shock_only_top_0.20_cost200 | 960 | shock_only | 0.2 | 56 | 11 | 22 | 454.334 | 908.825 | 218.737 | -673.228 | -7.71152 | 0.181818 | -61.2026 | -313.015 |
| horizon_960_liquidity_vacuum_top_0.05_cost200 | 960 | liquidity_vacuum | 0.05 | 54 | 10 | 22 | 430.725 | 826.126 | 198.671 | -594.072 | -6.80483 | 0.2 | -59.4072 | -523.979 |
| horizon_960_liquidity_vacuum_top_0.10_cost200 | 960 | liquidity_vacuum | 0.1 | 54 | 10 | 22 | 430.725 | 826.126 | 198.671 | -594.072 | -6.80483 | 0.2 | -59.4072 | -523.979 |
| horizon_960_liquidity_vacuum_top_0.20_cost200 | 960 | liquidity_vacuum | 0.2 | 54 | 11 | 22 | 444.09 | 908.701 | 218.472 | -683.083 | -7.8244 | 0.181818 | -62.0984 | -612.989 |
| horizon_960_shock_and_liquidity_vacuum_top_0.05_cost200 | 960 | shock_and_liquidity_vacuum | 0.05 | 34 | 10 | 22 | 488.062 | 826.058 | 198.558 | -536.554 | -6.14598 | 0.3 | -53.6554 | -380.494 |
| horizon_960_shock_and_liquidity_vacuum_top_0.10_cost200 | 960 | shock_and_liquidity_vacuum | 0.1 | 34 | 10 | 22 | 488.062 | 826.058 | 198.558 | -536.554 | -6.14598 | 0.3 | -53.6554 | -380.494 |
| horizon_960_shock_and_liquidity_vacuum_top_0.20_cost200 | 960 | shock_and_liquidity_vacuum | 0.2 | 34 | 10 | 22 | 488.062 | 826.058 | 198.558 | -536.554 | -6.14598 | 0.3 | -53.6554 | -380.494 |
| horizon_960_shock_and_l25_pressure_top_0.05_cost200 | 960 | shock_and_l25_pressure | 0.05 | 35 | 10 | 22 | 332.504 | 826.132 | 198.698 | -692.326 | -7.93028 | 0.3 | -69.2326 | -423.887 |
| horizon_960_shock_and_l25_pressure_top_0.10_cost200 | 960 | shock_and_l25_pressure | 0.1 | 35 | 10 | 22 | 332.504 | 826.132 | 198.698 | -692.326 | -7.93028 | 0.3 | -69.2326 | -423.887 |
| horizon_960_shock_and_l25_pressure_top_0.20_cost200 | 960 | shock_and_l25_pressure | 0.2 | 35 | 10 | 22 | 332.504 | 826.132 | 198.698 | -692.326 | -7.93028 | 0.3 | -69.2326 | -423.887 |
| horizon_1800_shock_only_top_0.05_cost200 | 1800 | shock_only | 0.05 | 56 | 10 | 22 | 597.354 | 826.163 | 198.701 | -427.51 | -4.89693 | 0.4 | -42.751 | -133.312 |
| horizon_1800_shock_only_top_0.10_cost200 | 1800 | shock_only | 0.1 | 56 | 10 | 22 | 597.354 | 826.163 | 198.701 | -427.51 | -4.89693 | 0.4 | -42.751 | -133.312 |
| horizon_1800_shock_only_top_0.20_cost200 | 1800 | shock_only | 0.2 | 56 | 11 | 22 | 524.621 | 908.767 | 218.544 | -602.689 | -6.90353 | 0.363636 | -54.7899 | -133.312 |
| horizon_1800_liquidity_vacuum_top_0.05_cost200 | 1800 | liquidity_vacuum | 0.05 | 54 | 10 | 22 | 756.338 | 826.133 | 198.683 | -268.478 | -3.07529 | 0.4 | -26.8478 | -135.668 |
| horizon_1800_liquidity_vacuum_top_0.10_cost200 | 1800 | liquidity_vacuum | 0.1 | 54 | 10 | 22 | 756.338 | 826.133 | 198.683 | -268.478 | -3.07529 | 0.4 | -26.8478 | -135.668 |
| horizon_1800_liquidity_vacuum_top_0.20_cost200 | 1800 | liquidity_vacuum | 0.2 | 54 | 11 | 22 | 758.16 | 908.7 | 218.465 | -369.006 | -4.22679 | 0.363636 | -33.546 | -236.195 |
| horizon_1800_shock_and_liquidity_vacuum_top_0.05_cost200 | 1800 | shock_and_liquidity_vacuum | 0.05 | 34 | 10 | 22 | 495.235 | 825.992 | 198.388 | -529.144 | -6.06111 | 0.3 | -52.9144 | -221.154 |
| horizon_1800_shock_and_liquidity_vacuum_top_0.10_cost200 | 1800 | shock_and_liquidity_vacuum | 0.1 | 34 | 10 | 22 | 495.235 | 825.992 | 198.388 | -529.144 | -6.06111 | 0.3 | -52.9144 | -221.154 |
| horizon_1800_shock_and_liquidity_vacuum_top_0.20_cost200 | 1800 | shock_and_liquidity_vacuum | 0.2 | 34 | 10 | 22 | 495.235 | 825.992 | 198.388 | -529.144 | -6.06111 | 0.3 | -52.9144 | -221.154 |
| horizon_1800_shock_and_l25_pressure_top_0.05_cost200 | 1800 | shock_and_l25_pressure | 0.05 | 35 | 10 | 22 | 613.399 | 826.085 | 198.555 | -411.241 | -4.71058 | 0.4 | -41.1241 | -133.312 |
| horizon_1800_shock_and_l25_pressure_top_0.10_cost200 | 1800 | shock_and_l25_pressure | 0.1 | 35 | 10 | 22 | 613.399 | 826.085 | 198.555 | -411.241 | -4.71058 | 0.4 | -41.1241 | -133.312 |
| horizon_1800_shock_and_l25_pressure_top_0.20_cost200 | 1800 | shock_and_l25_pressure | 0.2 | 35 | 10 | 22 | 613.399 | 826.085 | 198.555 | -411.241 | -4.71058 | 0.4 | -41.1241 | -133.312 |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P475_PHASE474_COMPLETE_USED | True | 1 | 1 | hard |
| P475_PHASE474_REJECTION_USED | True | 0 | 0 | hard |
| P475_FILTER_GRID_PRESENT | True | 36 | 36 | hard |
| P475_CATALYST_FILTERS_USED | True | liquidity_vacuum;shock_and_l25_pressure;shock_and_liquidity_vacuum;shock_only | shock_filter_present | hard |
| P475_LIQUIDITY_FILTERS_USED | True | liquidity_vacuum;shock_and_l25_pressure;shock_and_liquidity_vacuum;shock_only | liquidity_or_l25_filter_present | hard |
| P475_COST200_INCLUDED | True | 2 | 2 | hard |
| P475_FIXED_CAPITAL_USED | True | 100000 | 100000 | hard |
| P475_POSITIVE_NET_SCENARIO_EXISTS | False | 0 | >0 | hard |
| P475_ABOVE_12PCT_ANNUALIZED_SCENARIO_EXISTS | False | 0 | >0 | hard |
| P475_BEST_TRADE_COUNT_GE_10 | True | 10 | >=10 | hard |
| P475_NO_PAPER_LIVE_OR_CLAIM | True | synthetic_conditioned_replay_only;paper=0;live=0 | no_paper_live | hard |

Boundary: Phase475 is synthetic-conditioned replay evidence only. It is not paper/live acceptance and not a deployable profitability claim.

# Phase55 Cost-Aware Dense Edge Mining

Generated UTC: 2026-07-19T18:46:32.795865+00:00

Phase55 responds to the Phase53/Phase54 finding that dense marketable retail micro-trading is dominated by costs.
It mines bounded dense shards with explicit cost-hurdle metrics before any full-year replay is authorized.
The oracle ceiling row is nondeployable and exists only to show whether the data contains enough forward movement to beat costs in principle.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase55_dense_shards_scanned | 8 | Dense parquet shards scanned |
| phase55_trade_rows | 490 | Aggregated candidate trade rows |
| phase55_candidate_rows | 6 | Candidate result rows |
| phase55_deployable_positive_after_cost_rows | 0 | Deployable candidates positive after retail costs |
| phase55_cost_aware_scale_candidate_rows | 0 | Deployable candidates passing cost-aware scale gate |
| phase55_non_deployable_oracle_positive_rows | 1 | Oracle ceiling rows positive after costs |
| phase55_best_traded_deployable_net_pnl_inr | -13367.6 | Best deployable candidate net P&L among candidates that emitted at least one trade |
| phase55_best_any_net_pnl_inr | 65110.5 | Best candidate net P&L including nondeployable oracle ceilings |
| phase55_elapsed_seconds | 7.11322 | Replay elapsed seconds |
| phase55_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha cost model used |
| phase55_recommend_scale_deployable_to_full_year | 0 | 1 means at least one deployable cost-aware candidate deserves a wider dense replay |

## Candidate Catalog

| candidate_id | feature_family | raw_signal | forward_horizon_events | cooldown_modulus | cost_hurdle_multiplier | requires_signal_transition | candidate_role |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S55_MOM_Q995_H20_COST1P25 | one_tick_momentum | case when abs(one_tick_return) >= momentum_q995 and spread_bps <= spread_bps_q75 then sign(one_tick_return) else 0 end | 20 | 25 | 1.25 | True | deployable_cost_hurdle_test |
| S55_MOM_Q999_H50_COST1P50 | one_tick_momentum | case when abs(one_tick_return) >= momentum_q999 and spread_bps <= spread_bps_q50 then sign(one_tick_return) else 0 end | 50 | 100 | 1.5 | True | deployable_cost_hurdle_test |
| S55_MOM_Q999_H100_COST1P50 | one_tick_momentum | case when abs(one_tick_return) >= momentum_q999 and spread_bps <= spread_bps_q50 then sign(one_tick_return) else 0 end | 100 | 150 | 1.5 | True | deployable_cost_hurdle_test |
| S55_IMB_Q999_H50_COST1P50 | l1_imbalance | case when abs(l1_imbalance) >= l1_q999 and spread_bps <= spread_bps_q50 and l1_depth_notional >= depth_notional_q75 then sign(l1_imbalance) else 0 end | 50 | 100 | 1.5 | True | deployable_cost_hurdle_test |
| S55_MICRO_Q999_H50_COST1P50 | microprice | case when abs(microprice_dev) >= micro_q999 and spread_bps <= spread_bps_q50 then sign(microprice_dev) else 0 end | 50 | 100 | 1.5 | True | deployable_cost_hurdle_test |
| S55_ORACLE_H20_COST_CEILING | oracle_forward_return | case when abs(future_return_h20) >= retail_cost_return * 1.25 then sign(future_return_h20) else 0 end | 20 | 25 | 1.25 | False | nondeployable_cost_ceiling |

## Candidate Summary

| candidate_id | feature_family | candidate_role | symbols | trade_dates | trades | net_pnl_inr | gross_pnl_proxy_inr | cost_pnl_drag_proxy_inr | edge_over_cost_proxy_inr | mean_gross_return_per_trade | mean_cost_return_per_trade | mean_edge_over_cost_return_per_trade | mean_net_return_per_trade | positive_symbol_rows | positive_symbol_fraction | gross_positive_symbol_rows | edge_over_cost_positive_symbol_rows | worst_symbol_net_pnl_inr | best_symbol_net_pnl_inr | max_drawdown_inr | worst_trade_pnl_inr | best_trade_pnl_inr | forward_horizon_events | cooldown_modulus | cost_hurdle_multiplier | deployable_candidate | positive_after_costs | cost_aware_scale_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S55_ORACLE_H20_COST_CEILING | oracle_forward_return | nondeployable_cost_ceiling | 8 | 1 | 376 | 65110.5 | 111094 | 45983.1 | 53614.7 | 0.00295462 | 0.00122296 | 0.00142592 | 0.00173166 | 8 | 1 | 8 | 8 | 2368.25 | 11855.5 | 0 | -143.448 | 2628.3 | 20 | 25 | 1.25 | False | True | False |
| S55_MOM_Q999_H50_COST1P50 | one_tick_momentum | deployable_cost_hurdle_test | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 50 | 100 | 1.5 | True | False | False |
| S55_MOM_Q999_H100_COST1P50 | one_tick_momentum | deployable_cost_hurdle_test | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100 | 150 | 1.5 | True | False | False |
| S55_IMB_Q999_H50_COST1P50 | l1_imbalance | deployable_cost_hurdle_test | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 50 | 100 | 1.5 | True | False | False |
| S55_MICRO_Q999_H50_COST1P50 | microprice | deployable_cost_hurdle_test | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 50 | 100 | 1.5 | True | False | False |
| S55_MOM_Q995_H20_COST1P25 | one_tick_momentum | deployable_cost_hurdle_test | 8 | 1 | 114 | -13367.6 | 1181.5 | 14549.2 | -13355.2 | 0.000103641 | 0.00127624 | -0.00117151 | -0.0011726 | 0 | 0 | 3 | 0 | -3812.47 | -299.928 | -12062.1 | -519.608 | 1334.97 | 20 | 25 | 1.25 | True | False | False |

## Daily Symbol Sample

| shard_index | shard_path | trade_date | symbol | candidate_id | feature_family | candidate_role | execution_profile | trades | sum_gross_return | sum_cost_return | sum_edge_over_cost_return | sum_net_return | mean_gross_return | mean_cost_return | mean_edge_over_cost_return | mean_net_return | net_pnl_inr | worst_trade_pnl_inr | best_trade_pnl_inr | forward_horizon_events | cooldown_modulus | cost_hurdle_multiplier | total_latency_events | fixed_slippage_ticks | internal_impact_bps | zerodha_charge_bps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ADANIPORTS\part-00000.parquet | 2026-01-01 | ADANIPORTS | S55_MOM_Q995_H20_COST1P25 | one_tick_momentum | deployable_cost_hurdle_test | retail_marketable_default | 11 | 0.000162031 | 0.0132176 | -0.0163599 | -0.0130555 | 1.47301e-05 | 0.0012016 | -0.00148727 | -0.00118687 | -1305.55 | -120.803 | -103.884 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 1 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=ADANIPORTS\part-00000.parquet | 2026-01-01 | ADANIPORTS | S55_ORACLE_H20_COST_CEILING | oracle_forward_return | nondeployable_cost_ceiling | retail_marketable_default | 53 | 0.177809 | 0.0636987 | 0.0981855 | 0.11411 | 0.00335489 | 0.00120186 | 0.00185256 | 0.00215302 | 11411 | -120.803 | 2628.3 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 2 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=AXISBANK\part-00000.parquet | 2026-01-01 | AXISBANK | S55_MOM_Q995_H20_COST1P25 | one_tick_momentum | deployable_cost_hurdle_test | retail_marketable_default | 14 | -0.000895832 | 0.0153991 | -0.0147785 | -0.016295 | -6.3988e-05 | 0.00109994 | -0.0010556 | -0.00116393 | -1629.5 | -258.991 | -20.6571 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 2 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=AXISBANK\part-00000.parquet | 2026-01-01 | AXISBANK | S55_ORACLE_H20_COST_CEILING | oracle_forward_return | nondeployable_cost_ceiling | retail_marketable_default | 52 | 0.159185 | 0.0571793 | 0.0877109 | 0.102006 | 0.00306125 | 0.0010996 | 0.00168675 | 0.00196165 | 10200.6 | -110.467 | 856.202 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 3 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-01-01 | BAJAJ-AUTO | S55_MOM_Q995_H20_COST1P25 | one_tick_momentum | deployable_cost_hurdle_test | retail_marketable_default | 14 | 0.00169537 | 0.0183056 | -0.013797 | -0.0166102 | 0.000121098 | 0.00130754 | -0.000985501 | -0.00118645 | -1661.02 | -500.349 | 182.029 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 3 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BAJAJ-AUTO\part-00000.parquet | 2026-01-01 | BAJAJ-AUTO | S55_ORACLE_H20_COST_CEILING | oracle_forward_return | nondeployable_cost_ceiling | retail_marketable_default | 48 | 0.181316 | 0.0627609 | 0.102865 | 0.118555 | 0.00377742 | 0.00130752 | 0.00214302 | 0.0024699 | 11855.5 | -130.942 | 2164.57 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 4 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BANKBEES\part-00000.parquet | 2026-01-01 | BANKBEES | S55_MOM_Q995_H20_COST1P25 | one_tick_momentum | deployable_cost_hurdle_test | retail_marketable_default | 26 | -0.00184151 | 0.0362832 | -0.0410697 | -0.0381247 | -7.08274e-05 | 0.00139551 | -0.0015796 | -0.00146633 | -3812.47 | -322.153 | -63.7621 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 4 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BANKBEES\part-00000.parquet | 2026-01-01 | BANKBEES | S55_ORACLE_H20_COST_CEILING | oracle_forward_return | nondeployable_cost_ceiling | retail_marketable_default | 25 | 0.0585941 | 0.0349116 | 0.0149546 | 0.0236825 | 0.00234376 | 0.00139647 | 0.000598183 | 0.000947299 | 2368.25 | -140.27 | 465.529 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 5 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BHARTIARTL\part-00000.parquet | 2026-01-01 | BHARTIARTL | S55_MOM_Q995_H20_COST1P25 | one_tick_momentum | deployable_cost_hurdle_test | retail_marketable_default | 15 | -0.00191402 | 0.0166413 | -0.0145426 | -0.0185553 | -0.000127601 | 0.00110942 | -0.000969508 | -0.00123702 | -1855.53 | -519.608 | 18.4979 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 5 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BHARTIARTL\part-00000.parquet | 2026-01-01 | BHARTIARTL | S55_ORACLE_H20_COST_CEILING | oracle_forward_return | nondeployable_cost_ceiling | retail_marketable_default | 52 | 0.113522 | 0.0576843 | 0.0414169 | 0.055838 | 0.00218312 | 0.00110931 | 0.00079648 | 0.00107381 | 5583.8 | -111.347 | 493.564 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 6 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BPCL\part-00000.parquet | 2026-01-01 | BPCL | S55_MOM_Q995_H20_COST1P25 | one_tick_momentum | deployable_cost_hurdle_test | retail_marketable_default | 3 | 0 | 0.00334845 | -0.00418556 | -0.00334845 | 0 | 0.00111615 | -0.00139519 | -0.00111615 | -334.845 | -111.651 | -111.582 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 6 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BPCL\part-00000.parquet | 2026-01-01 | BPCL | S55_ORACLE_H20_COST_CEILING | oracle_forward_return | nondeployable_cost_ceiling | retail_marketable_default | 57 | 0.145651 | 0.063716 | 0.0660059 | 0.0819349 | 0.00255528 | 0.00111782 | 0.001158 | 0.00143745 | 8193.49 | -112.231 | 644.183 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 7 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BRITANNIA\part-00000.parquet | 2026-01-01 | BRITANNIA | S55_MOM_Q995_H20_COST1P25 | one_tick_momentum | deployable_cost_hurdle_test | retail_marketable_default | 17 | -0.000449647 | 0.0242384 | -0.0243286 | -0.024688 | -2.64498e-05 | 0.00142579 | -0.00143109 | -0.00145224 | -2468.8 | -463.656 | 133.11 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 7 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=BRITANNIA\part-00000.parquet | 2026-01-01 | BRITANNIA | S55_ORACLE_H20_COST_CEILING | oracle_forward_return | nondeployable_cost_ceiling | retail_marketable_default | 37 | 0.122867 | 0.0527938 | 0.0568747 | 0.0700731 | 0.00332073 | 0.00142686 | 0.00153715 | 0.00189387 | 7007.31 | -143.448 | 1717.67 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 8 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=CIPLA\part-00000.parquet | 2026-01-01 | CIPLA | S55_MOM_Q995_H20_COST1P25 | one_tick_momentum | deployable_cost_hurdle_test | retail_marketable_default | 14 | 0.0150586 | 0.0180579 | -0.00449012 | -0.00299928 | 0.00107562 | 0.00128985 | -0.000320723 | -0.000214234 | -299.928 | -280.095 | 1334.97 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |
| 8 | raw_synthetic_l2_dense_full_year\trade_month=2026-01\symbol=CIPLA\part-00000.parquet | 2026-01-01 | CIPLA | S55_ORACLE_H20_COST_CEILING | oracle_forward_return | nondeployable_cost_ceiling | retail_marketable_default | 52 | 0.151992 | 0.0670866 | 0.0681338 | 0.0849054 | 0.00292292 | 0.00129013 | 0.00131027 | 0.0016328 | 8490.54 | -129.769 | 1334.97 | 20 | 25 | 1.25 | 2 | 1 | 0.5 | 8.26812 |

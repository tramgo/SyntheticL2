# Phase230 Low-turnover High-edge Strategy Search

Generated UTC: 2026-07-29T06:05:17.326072+00:00

Phase230 expands beyond the Phase229 ranking by testing original, inverse/contrarian and oracle-signed variants
of the Phase164 full-year synthetic trade ledger across lower-turnover grouping scopes.
The oracle-signed variant is an infeasible upper bound, not a tradable strategy; it asks whether any available
directional signal magnitude could clear modeled realistic costs if sign selection were perfect at that scope.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase230_low_turnover_high_edge_search_complete | 1 | Phase230 search completed |
| phase230_phase229_positive_realistic_candidate_rows | 0 | Inherited Phase229 positive realistic candidates |
| phase230_phase164_ledger_rows | 37424 | Phase164 ledger rows scanned |
| phase230_realistic_ledger_rows | 25010 | Realistic retail/stressed rows scanned |
| phase230_group_scope_rows | 4 | Expansion scope rows summarized |
| phase230_variant_group_rows | 28162 | Variant groups tested across scopes |
| phase230_positive_expanded_group_rows | 0 | Positive original/inverse/oracle best groups |
| phase230_positive_oracle_signed_group_rows | 0 | Positive oracle-signed upper-bound groups |
| phase230_best_scope | strategy_symbol_date_profile | Best expanded scope |
| phase230_best_strategy_id | P164_S06_ABSORPTION_REVERSAL | Best expanded strategy id where present |
| phase230_best_execution_profile | retail_marketable_default | Best expanded execution profile |
| phase230_best_expanded_variant | original | Best among original/inverse/oracle variants |
| phase230_best_expanded_net_return | -0.0010052 | Best expanded net return |
| phase230_best_expanded_net_pnl_inr | -100.52 | Best expanded net P&L INR |
| phase230_strategy_promotion_allowed | 0 | No promotion from synthetic expansion alone |
| phase230_paper_or_live_acceptance_allowed | 0 | No paper/live acceptance from synthetic expansion alone |
| phase230_deployable_profitability_claim_allowed | 0 | No deployable profitability claim from synthetic expansion alone |
| phase230_next_best_action | run_phase231_material_new_strategy_forms_longer_horizon_or_pessimistic_passive_no_generator_profit_tuning | Next strategy-discovery milestone |

## Gate Evaluation

| gate_id | passed | observed_value | required_value | interpretation |
| --- | --- | --- | --- | --- |
| P230_PHASE164_LEDGER_AVAILABLE | True | 37424 | >0 ledger rows | Full-year synthetic daily/symbol/profile trade ledger is available. |
| P230_REALISTIC_PROFILE_ROWS_AVAILABLE | True | 25010 | >0 realistic rows | Search is evaluated under realistic retail/stressed profiles. |
| P230_MULTIPLE_EXPANSION_SCOPES_TESTED | True | 4 | >=4 grouping scopes | Search tests low-turnover selective scopes instead of only full portfolio rows. |
| P230_EXPANDED_REALISTIC_PROFITABLE_GROUP_FOUND | False | 0 | >0 original/inverse/oracle best groups | If this fails, expanded variants of the current signal set still do not clear modeled costs. |
| P230_ORACLE_SIGNED_UPPER_BOUND_CLEARS_COST | False | 0 | >0 oracle-signed groups | This is an upper-bound feasibility check; failure means even perfect sign choice at tested scopes cannot beat costs. |

## Expansion Catalog

| expansion_id | scope | groups_tested | positive_original_groups | positive_inverse_groups | positive_oracle_signed_groups | best_expanded_variant | best_expanded_net_return | best_expanded_net_pnl_inr | best_trades | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P230_STRATEGY_SYMBOL_DATE_PROFILE_BEST_OF_ORIGINAL_INVERSE_ORACLE | strategy_symbol_date_profile | 25010 | 0 | 0 | 0 | original | -0.0010052 | -100.52 | 1 | no_positive_group_after_costs |
| P230_STRATEGY_DATE_PROFILE_BEST_OF_ORIGINAL_INVERSE_ORACLE | strategy_date_profile | 2714 | 0 | 0 | 0 | original | -0.00108706 | -108.706 | 1 | no_positive_group_after_costs |
| P230_STRATEGY_SYMBOL_PROFILE_BEST_OF_ORIGINAL_INVERSE_ORACLE | strategy_symbol_profile | 422 | 0 | 0 | 0 | original | -0.00703561 | -703.561 | 5 | no_positive_group_after_costs |
| P230_STRATEGY_PROFILE_BEST_OF_ORIGINAL_INVERSE_ORACLE | strategy_profile | 16 | 0 | 0 | 0 | original | -13.8206 | -1.38206e+06 | 9417 | no_positive_group_after_costs |

## Top Variant Groups

| scope | strategy_id | execution_profile | rows | trades | gross_return | cost_return | original_net_return | inverse_net_return | oracle_signed_net_return | original_net_pnl_inr | inverse_net_pnl_inr | oracle_signed_net_pnl_inr | original_positive | inverse_positive | oracle_signed_positive | turnover_bucket | abs_gross_to_cost_ratio | symbol | trade_date | best_expanded_variant | best_expanded_net_return | best_expanded_net_pnl_inr | best_expanded_positive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| strategy_symbol_date_profile | P164_S06_ABSORPTION_REVERSAL | retail_marketable_default | 1 | 1 | 0 | 0.0010052 | -0.0010052 | -0.0010052 | -0.0010052 | -100.52 | -100.52 | -100.52 | False | False | False | single_trade | 0 | GOLDBEES | 2026-07-01 | original | -0.0010052 | -100.52 | False |
| strategy_symbol_date_profile | P164_S06_ABSORPTION_REVERSAL | retail_marketable_default | 1 | 1 | 0 | 0.00100521 | -0.00100521 | -0.00100521 | -0.00100521 | -100.521 | -100.521 | -100.521 | False | False | False | single_trade | 0 | GOLDBEES | 2026-05-29 | original | -0.00100521 | -100.521 | False |
| strategy_symbol_date_profile | P164_S06_ABSORPTION_REVERSAL | retail_marketable_default | 1 | 1 | 0 | 0.00100522 | -0.00100522 | -0.00100522 | -0.00100522 | -100.522 | -100.522 | -100.522 | False | False | False | single_trade | 0 | GOLDBEES | 2026-02-04 | original | -0.00100522 | -100.522 | False |
| strategy_symbol_date_profile | P164_S06_ABSORPTION_REVERSAL | retail_marketable_default | 1 | 1 | 0 | 0.00100522 | -0.00100522 | -0.00100522 | -0.00100522 | -100.522 | -100.522 | -100.522 | False | False | False | single_trade | 0 | GOLDBEES | 2026-10-27 | original | -0.00100522 | -100.522 | False |
| strategy_symbol_date_profile | P164_S06_ABSORPTION_REVERSAL | retail_marketable_default | 1 | 1 | 0 | 0.00100552 | -0.00100552 | -0.00100552 | -0.00100552 | -100.552 | -100.552 | -100.552 | False | False | False | single_trade | 0 | GOLDBEES | 2026-10-28 | original | -0.00100552 | -100.552 | False |
| strategy_symbol_date_profile | P164_S06_ABSORPTION_REVERSAL | retail_marketable_default | 1 | 1 | 0 | 0.00100568 | -0.00100568 | -0.00100568 | -0.00100568 | -100.568 | -100.568 | -100.568 | False | False | False | single_trade | 0 | GOLDBEES | 2026-04-23 | original | -0.00100568 | -100.568 | False |
| strategy_symbol_date_profile | P164_S04_TRADE_FLOW_DEPTH | retail_marketable_default | 1 | 1 | 0 | 0.00100571 | -0.00100571 | -0.00100571 | -0.00100571 | -100.571 | -100.571 | -100.571 | False | False | False | single_trade | 0 | GOLDBEES | 2026-06-22 | original | -0.00100571 | -100.571 | False |
| strategy_symbol_date_profile | P164_S06_ABSORPTION_REVERSAL | retail_marketable_default | 1 | 1 | 0 | 0.00100573 | -0.00100573 | -0.00100573 | -0.00100573 | -100.573 | -100.573 | -100.573 | False | False | False | single_trade | 0 | GOLDBEES | 2026-07-23 | original | -0.00100573 | -100.573 | False |
| strategy_symbol_date_profile | P164_S06_ABSORPTION_REVERSAL | retail_marketable_default | 1 | 1 | 0 | 0.00100599 | -0.00100599 | -0.00100599 | -0.00100599 | -100.599 | -100.599 | -100.599 | False | False | False | single_trade | 0 | GOLDBEES | 2026-05-07 | original | -0.00100599 | -100.599 | False |
| strategy_symbol_date_profile | P164_S03_LIQUIDITY_VACUUM | retail_marketable_default | 1 | 1 | 0 | 0.00100605 | -0.00100605 | -0.00100605 | -0.00100605 | -100.605 | -100.605 | -100.605 | False | False | False | single_trade | 0 | GOLDBEES | 2026-08-06 | original | -0.00100605 | -100.605 | False |
| strategy_symbol_date_profile | P164_S06_ABSORPTION_REVERSAL | retail_marketable_default | 1 | 1 | 0 | 0.00100648 | -0.00100648 | -0.00100648 | -0.00100648 | -100.648 | -100.648 | -100.648 | False | False | False | single_trade | 0 | GOLDBEES | 2026-01-13 | original | -0.00100648 | -100.648 | False |
| strategy_symbol_date_profile | P164_S06_ABSORPTION_REVERSAL | retail_marketable_default | 1 | 1 | 0 | 0.00100777 | -0.00100777 | -0.00100777 | -0.00100777 | -100.777 | -100.777 | -100.777 | False | False | False | single_trade | 0 | GOLDBEES | 2026-03-03 | original | -0.00100777 | -100.777 | False |

## Phase231 Work Order

| work_order_id | action | rationale | candidate_family_1 | candidate_family_2 | candidate_family_3 | forbidden_shortcut |
| --- | --- | --- | --- | --- | --- | --- |
| P231_MATERIAL_NEW_LOW_TURNOVER_HIGH_EDGE_STRATEGY_FORMS | design_materially_new_execution_or_horizon_contract | Original, inverse and oracle-signed variants of the current Phase164 signal set do not clear realistic costs. Next search must reduce cost drag structurally through fewer trades, longer horizons, passive/limit assumptions where modelable, or a genuinely new edge source. | opening_range_or_event_window_continuation_with_minimum_expected_move_filter | longer_horizon_cross_sectional_relative_strength_with_turnover_cap | passive_or_midpoint_control_only_if_fill_model_is_explicitly_pessimistic | do_not_tune_synthetic_generator_to_create_profit |

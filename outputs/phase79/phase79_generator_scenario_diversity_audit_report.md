# Phase79 Generator Scenario Diversity Audit

Generated UTC: 2026-07-19T20:19:03.280707+00:00

Phase79 audits whether the dense synthetic year has enough regime, shock, feed-imperfection, spread and correlation diversity to support strategy falsification.
The audit samples a bounded prefix per symbol partition and is not a profitability claim.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase79_months_audited | 12 | Distinct synthetic months audited |
| phase79_complete_month_fraction | 1 | Fraction of months with all expected symbols |
| phase79_min_regime_codes_per_month | 1 | Minimum distinct regime codes in any month |
| phase79_median_regime_entropy_bits | 0 | Median monthly regime entropy |
| phase79_min_feed_profiles_per_month | 2 | Minimum feed-profile count in any month |
| phase79_market_shock_months | 1 | Months where market shock flag appears broadly across symbols |
| phase79_symbol_shock_months | 1 | Months with at least one symbol shock |
| phase79_median_spread_cross_symbol_cv | 0.349585 | Median monthly cross-symbol coefficient of variation for mean spread bps |
| phase79_corr_months | 12 | Months with cross-symbol correlation diagnostics |
| phase79_median_corr_pair_std | 0.220938 | Median monthly standard deviation of pairwise correlations |
| phase79_negative_corr_months | 2 | Months with more than 5 percent negative pair correlations |
| phase79_generator_scenario_diversity_pass | 0 | 1 means generator diversity gate passes |
| phase79_recommend_next_action | generator_scenario_recalibration_before_new_strategy_mining | Recommended next milestone |
| phase79_elapsed_seconds | 181.649 | Elapsed seconds |

## Monthly Scenario Diversity

| trade_month | symbols | rows_scanned | regime_codes | regime_entropy_bits | feed_profiles | feed_profile_entropy_bits | market_shock_symbols | symbol_shock_symbols | mean_duplicate_rate | mean_disconnect_gap_rate | mean_out_of_order_rate | median_symbol_spread_bps | spread_cross_symbol_cv | median_symbol_l1_depth | median_symbol_one_tick_return_std |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | 32 | 8000000 | 1 | -0 | 2 | 0.975717 | 0 | 0 | 0.000992 | 0.00496 | 0.008184 | 2.00918 | 0.35009 | 792.88 | 7.84789e-05 |
| 2026-02 | 32 | 8000000 | 1 | -0 | 2 | 0.979281 | 0 | 0 | 0.002232 | 0.005208 | 0.00744 | 2.03504 | 0.349483 | 796.974 | 6.29426e-05 |
| 2026-03 | 32 | 8000000 | 1 | -0 | 2 | 0.975849 | 0 | 0 | 0.003472 | 0.002728 | 0.007192 | 2.05451 | 0.354697 | 788.173 | 5.13053e-05 |
| 2026-04 | 32 | 8000000 | 1 | -0 | 2 | 0.979158 | 32 | 1 | 0.00496 | 0.006696 | 0.017856 | 4.21105 | 0.206361 | 975.285 | 0.000150645 |
| 2026-05 | 32 | 8000000 | 1 | -0 | 2 | 0.976374 | 0 | 0 | 0.002728 | 0.004216 | 0.00992 | 2.02737 | 0.349686 | 791.209 | 8.53893e-05 |
| 2026-06 | 32 | 8000000 | 1 | -0 | 2 | 0.976635 | 0 | 0 | 0.001736 | 0.004216 | 0.008432 | 1.73752 | 0.336968 | 611.801 | 2.27987e-05 |
| 2026-07 | 32 | 8000000 | 1 | -0 | 2 | 0.977023 | 0 | 0 | 0.00496 | 0.00496 | 0.010416 | 2.04962 | 0.349444 | 792.169 | 8.3635e-05 |
| 2026-08 | 32 | 8000000 | 1 | -0 | 2 | 0.978041 | 0 | 0 | 0.001984 | 0.00248 | 0.00868 | 2.04234 | 0.355736 | 795.162 | 6.03546e-05 |
| 2026-09 | 32 | 8000000 | 1 | -0 | 2 | 0.977535 | 0 | 0 | 0.003224 | 0.002976 | 0.007688 | 1.72055 | 0.337805 | 611.714 | 3.70366e-05 |
| 2026-10 | 32 | 8000000 | 1 | -0 | 2 | 0.978166 | 0 | 0 | 0.003224 | 0.0062 | 0.006944 | 2.04137 | 0.355457 | 772.413 | 5.39339e-05 |
| 2026-11 | 32 | 8000000 | 1 | -0 | 2 | 0.977151 | 0 | 0 | 0.002976 | 0.003472 | 0.008928 | 2.03217 | 0.356514 | 789.817 | 5.94284e-05 |
| 2026-12 | 32 | 8000000 | 1 | -0 | 2 | 0.977915 | 0 | 0 | 0.001488 | 0.004216 | 0.009176 | 2.04471 | 0.348804 | 725.288 | 4.83586e-05 |

## Monthly Correlation Diversity

| trade_month | symbols_in_corr | bar_rows | corr_pair_count | mean_pair_corr | median_pair_corr | std_pair_corr | min_pair_corr | max_pair_corr | negative_corr_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-01 | 32 | 10 | 1024 | 0.823606 | 0.910683 | 0.208745 | 0.0804301 | 0.993319 | 0 |
| 2026-02 | 32 | 10 | 1024 | 0.791679 | 0.845827 | 0.163066 | -0.0477388 | 0.984276 | 0.00195312 |
| 2026-03 | 32 | 10 | 1024 | 0.703743 | 0.736714 | 0.182535 | 0.0767114 | 0.976232 | 0 |
| 2026-04 | 32 | 10 | 1024 | 0.692708 | 0.806458 | 0.310023 | -0.360869 | 0.989373 | 0.0585938 |
| 2026-05 | 32 | 10 | 1024 | 0.849652 | 0.876763 | 0.103057 | 0.343482 | 0.996137 | 0 |
| 2026-06 | 32 | 10 | 1024 | 0.559158 | 0.606589 | 0.280796 | -0.287806 | 0.990057 | 0.0253906 |
| 2026-07 | 32 | 10 | 1024 | 0.822809 | 0.84444 | 0.112501 | 0.409558 | 0.992167 | 0 |
| 2026-08 | 32 | 10 | 1024 | 0.82177 | 0.866987 | 0.159928 | 0.0240918 | 0.987935 | 0 |
| 2026-09 | 32 | 10 | 1024 | 0.800374 | 0.91036 | 0.233131 | 0.0942506 | 0.996914 | 0 |
| 2026-10 | 32 | 10 | 1024 | 0.722171 | 0.842793 | 0.281972 | -0.403759 | 0.990765 | 0.0214844 |
| 2026-11 | 32 | 10 | 1024 | 0.570688 | 0.637979 | 0.286758 | -0.278327 | 0.981334 | 0.0488281 |
| 2026-12 | 32 | 10 | 1024 | 0.501209 | 0.587377 | 0.365778 | -0.747152 | 0.991374 | 0.101562 |

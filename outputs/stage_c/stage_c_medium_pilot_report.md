# Stage C Medium Pilot

Generated UTC: 2026-07-14T17:06:17.189842+00:00

## Scope

This medium pilot covers all 32 instruments, 20 selected Q-A trading days, 3 initial engineering seeds, S01-S05 proxy strategies and all 7 registered baselines.
It is medium-pilot proxy evidence only. It is not acceptance-grade promotion evidence.

## Selected Days

| quarter_profile | scenario_day | trade_date | regime_code | regime_family | is_market_shock_day | vol_multiplier | event_rate_multiplier | spread_multiplier | depth_multiplier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-A | 1 | 2026-07-14 | D04 | Gradual bullish trend | False | 1.1 | 1.1 | 1.0 | 1.0 |
| Q-A | 2 | 2026-07-15 | D12 | Event day | True | 1.6 | 1.35 | 1.25 | 0.85 |
| Q-A | 3 | 2026-07-16 | D02 | Low-volatility sideways | False | 0.65 | 0.8 | 0.85 | 1.05 |
| Q-A | 4 | 2026-07-17 | D01 | Normal balanced | False | 1.0 | 1.0 | 1.0 | 1.0 |
| Q-A | 5 | 2026-07-20 | D07 | Sell-off/panic | True | 2.2 | 1.55 | 1.75 | 0.65 |
| Q-A | 6 | 2026-07-21 | D10 | Gap-down continuation | False | 1.55 | 1.3 | 1.25 | 0.85 |
| Q-A | 7 | 2026-07-22 | D15 | Rotation day | False | 1.15 | 1.1 | 1.05 | 1.0 |
| Q-A | 8 | 2026-07-23 | D01 | Normal balanced | False | 1.0 | 1.0 | 1.0 | 1.0 |
| Q-A | 9 | 2026-07-24 | D03 | High-volatility sideways | False | 1.45 | 1.15 | 1.2 | 0.95 |
| Q-A | 10 | 2026-07-27 | D04 | Gradual bullish trend | False | 1.1 | 1.1 | 1.0 | 1.0 |
| Q-A | 11 | 2026-07-28 | D08 | Gap-up continuation | False | 1.35 | 1.2 | 1.05 | 0.95 |
| Q-A | 12 | 2026-07-29 | D08 | Gap-up continuation | False | 1.35 | 1.2 | 1.05 | 0.95 |
| Q-A | 13 | 2026-07-30 | D02 | Low-volatility sideways | False | 0.65 | 0.8 | 0.85 | 1.05 |
| Q-A | 14 | 2026-07-31 | D03 | High-volatility sideways | False | 1.45 | 1.15 | 1.2 | 0.95 |
| Q-A | 15 | 2026-08-03 | D15 | Rotation day | False | 1.15 | 1.1 | 1.05 | 1.0 |
| Q-A | 16 | 2026-08-04 | D10 | Gap-down continuation | False | 1.55 | 1.3 | 1.25 | 0.85 |
| Q-A | 17 | 2026-08-05 | D02 | Low-volatility sideways | False | 0.65 | 0.8 | 0.85 | 1.05 |
| Q-A | 18 | 2026-08-06 | D17 | Stock-specific dispersion | False | 1.25 | 1.15 | 1.1 | 0.95 |
| Q-A | 19 | 2026-08-07 | D01 | Normal balanced | False | 1.0 | 1.0 | 1.0 | 1.0 |
| Q-A | 20 | 2026-08-10 | D03 | High-volatility sideways | False | 1.45 | 1.15 | 1.2 | 0.95 |

## Selected Seeds

| quarter_profile | seed_ordinal | simulation_seed | initial_engineering_seed | required_for_full_validation |
| --- | --- | --- | --- | --- |
| Q-A | 1 | 910001 | True | True |
| Q-A | 2 | 910002 | True | True |
| Q-A | 3 | 910003 | True | True |

## Dataset Summary

| metric | value | description |
| --- | --- | --- |
| symbols | 32 | instrument count in pilot feature subset |
| selected_trading_days | 20 | selected Q-A pilot trading days |
| selected_seed_rows | 3 | initial engineering seed rows |
| regime_families | 10 | regime families in selected days |
| shock_days | 2 | selected market shock days |
| feature_rows | 239173 | Phase 9 Tier C rows in pilot feature subset |
| feed_profiles | 5 | feed profiles represented |
| strategy_run_rows | 15 | S01-S05 strategy/seed proxy run summaries |
| baseline_run_rows | 21 | baseline/seed proxy run summaries |
| acceptance_ready_rows | 0 | promotion-ready rows |

## Checks

| check_id | observed_value | expected_value | passed | detail | acceptance_scope |
| --- | --- | --- | --- | --- | --- |
| all_32_instruments | 32 | 32 | True | all current Stage A1 symbols represented | stage_c_medium_pilot_proxy_not_strategy_promotion |
| twenty_trading_days | 20 | 20 | True | Q-A first 20 scenario days selected | stage_c_medium_pilot_proxy_not_strategy_promotion |
| three_initial_seeds | 3 | 3 | True | Q-A initial engineering seeds selected | stage_c_medium_pilot_proxy_not_strategy_promotion |
| multiple_regimes | 10 | 3 | True | shock_days=2 | stage_c_medium_pilot_proxy_not_strategy_promotion |
| strategy_proxy_runs | 15 | 15 | True | S01-S05 x 3 seeds | stage_c_medium_pilot_proxy_not_strategy_promotion |
| baseline_proxy_runs | 21 | 21 | True | B01-B07 x 3 seeds | stage_c_medium_pilot_proxy_not_strategy_promotion |
| non_acceptance_scope | 0 | 0 | True | medium pilot is not strategy promotion evidence | stage_c_medium_pilot_proxy_not_strategy_promotion |

## Strategy Proxy Runs

| model_id | model_name | model_type | simulation_seed | rows_evaluated | trades | signal_fraction | mean_gross_return_proxy | win_rate_proxy | total_gross_pnl_units_proxy | acceptance_ready | pilot_status | caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Momentum/breakout filtered by MLOFI | strategy | 910001 | 239173 | 89313 | 0.3734242577548469 | -0.0003308604083267482 | 0.4425335617435312 | -29.55013564888686 | False | medium_pilot_proxy_not_acceptance | runnable_proxy medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S02 | Pure multi-level OFI directional model | strategy | 910001 | 239173 | 220397 | 0.9214961555025024 | -9.231740015725651e-05 | 0.4770028630153768 | -20.346478042458862 | False | medium_pilot_proxy_not_acceptance | runnable_proxy medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S03 | Liquidity-vacuum breakout | strategy | 910001 | 239173 | 19888 | 0.08315319873062595 | -0.00021400221302325046 | 0.4624396621078037 | -4.256076012606405 | False | medium_pilot_proxy_not_acceptance | partial_missing_required_features medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S04 | Trade-flow plus depth confirmation | strategy | 910001 | 239173 | 89702 | 0.3750506955216517 | -0.00016200514725754527 | 0.4792200842790573 | -14.532185719296326 | False | medium_pilot_proxy_not_acceptance | partial_missing_required_features medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S05 | Microprice entry/exit filter | strategy | 910001 | 239173 | 229247 | 0.9584986599657989 | -1.9614621100767384e-05 | 0.4873738805742278 | -4.4965930434876205 | False | medium_pilot_proxy_not_acceptance | runnable_proxy medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S01 | Momentum/breakout filtered by MLOFI | strategy | 910002 | 239173 | 89313 | 0.3734242577548469 | -0.0003308604083267482 | 0.4425335617435312 | -29.55013564888686 | False | medium_pilot_proxy_not_acceptance | runnable_proxy medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S02 | Pure multi-level OFI directional model | strategy | 910002 | 239173 | 220397 | 0.9214961555025024 | -9.231740015725651e-05 | 0.4770028630153768 | -20.346478042458862 | False | medium_pilot_proxy_not_acceptance | runnable_proxy medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S03 | Liquidity-vacuum breakout | strategy | 910002 | 239173 | 19888 | 0.08315319873062595 | -0.00021400221302325046 | 0.4624396621078037 | -4.256076012606405 | False | medium_pilot_proxy_not_acceptance | partial_missing_required_features medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S04 | Trade-flow plus depth confirmation | strategy | 910002 | 239173 | 89702 | 0.3750506955216517 | -0.00016200514725754527 | 0.4792200842790573 | -14.532185719296326 | False | medium_pilot_proxy_not_acceptance | partial_missing_required_features medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S05 | Microprice entry/exit filter | strategy | 910002 | 239173 | 229247 | 0.9584986599657989 | -1.9614621100767384e-05 | 0.4873738805742278 | -4.4965930434876205 | False | medium_pilot_proxy_not_acceptance | runnable_proxy medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S01 | Momentum/breakout filtered by MLOFI | strategy | 910003 | 239173 | 89313 | 0.3734242577548469 | -0.0003308604083267482 | 0.4425335617435312 | -29.55013564888686 | False | medium_pilot_proxy_not_acceptance | runnable_proxy medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S02 | Pure multi-level OFI directional model | strategy | 910003 | 239173 | 220397 | 0.9214961555025024 | -9.231740015725651e-05 | 0.4770028630153768 | -20.346478042458862 | False | medium_pilot_proxy_not_acceptance | runnable_proxy medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S03 | Liquidity-vacuum breakout | strategy | 910003 | 239173 | 19888 | 0.08315319873062595 | -0.00021400221302325046 | 0.4624396621078037 | -4.256076012606405 | False | medium_pilot_proxy_not_acceptance | partial_missing_required_features medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S04 | Trade-flow plus depth confirmation | strategy | 910003 | 239173 | 89702 | 0.3750506955216517 | -0.00016200514725754527 | 0.4792200842790573 | -14.532185719296326 | False | medium_pilot_proxy_not_acceptance | partial_missing_required_features medium-pilot proxy over 5-minute features; not acceptance-grade. |
| S05 | Microprice entry/exit filter | strategy | 910003 | 239173 | 229247 | 0.9584986599657989 | -1.9614621100767384e-05 | 0.4873738805742278 | -4.4965930434876205 | False | medium_pilot_proxy_not_acceptance | runnable_proxy medium-pilot proxy over 5-minute features; not acceptance-grade. |

## Baseline Proxy Runs

| model_id | model_name | model_type | simulation_seed | rows_evaluated | trades | signal_fraction | mean_gross_return_proxy | win_rate_proxy | total_gross_pnl_units_proxy | acceptance_ready | pilot_status | caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B01 | Random direction with matched trade frequency | baseline | 910001 | 239173 | 235973 | 0.9866205633579042 | -7.1620742416220056e-06 | 0.48942463756446714 | -1.6900561450182696 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B02 | Buy-and-hold intraday control | baseline | 910001 | 239173 | 235973 | 0.9866205633579042 | -2.2705277044505813e-05 | 0.49083581596199566 | -5.35783234002317 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B03 | Simple short-term momentum | baseline | 910001 | 239173 | 223623 | 0.9349843000673153 | -0.00028370455484999306 | 0.45755579703339994 | -63.44286366922 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B04 | Opening-range breakout | baseline | 910001 | 239173 | 231704 | 0.968771558662558 | 4.1547627423229095e-05 | 0.49586109864309635 | 9.626751464471875 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B05 | VWAP continuation | baseline | 910001 | 239173 | 232003 | 0.9700216997738039 | -8.893388318421565e-05 | 0.4677180898522864 | -20.632927700387583 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; B05 uses rolling-mid proxy because trade-volume/VWAP is not yet acceptance-grade. |
| B06 | Short-term mean reversion | baseline | 910001 | 239173 | 223623 | 0.9349843000673153 | 0.00028370455484999306 | 0.520550211740295 | 63.44286366922 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B07 | Volatility breakout | baseline | 910001 | 239173 | 125624 | 0.5252432339770794 | -0.0003758275670622449 | 0.4495239763102592 | -47.21296228462745 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B01 | Random direction with matched trade frequency | baseline | 910002 | 239173 | 235973 | 0.9866205633579042 | -2.317734935785235e-06 | 0.4880304102588008 | -0.5469228660020493 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B02 | Buy-and-hold intraday control | baseline | 910002 | 239173 | 235973 | 0.9866205633579042 | -2.2705277044505813e-05 | 0.49083581596199566 | -5.35783234002317 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B03 | Simple short-term momentum | baseline | 910002 | 239173 | 223623 | 0.9349843000673153 | -0.00028370455484999306 | 0.45755579703339994 | -63.44286366922 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B04 | Opening-range breakout | baseline | 910002 | 239173 | 231704 | 0.968771558662558 | 4.1547627423229095e-05 | 0.49586109864309635 | 9.626751464471875 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B05 | VWAP continuation | baseline | 910002 | 239173 | 232003 | 0.9700216997738039 | -8.893388318421565e-05 | 0.4677180898522864 | -20.632927700387583 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; B05 uses rolling-mid proxy because trade-volume/VWAP is not yet acceptance-grade. |
| B06 | Short-term mean reversion | baseline | 910002 | 239173 | 223623 | 0.9349843000673153 | 0.00028370455484999306 | 0.520550211740295 | 63.44286366922 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B07 | Volatility breakout | baseline | 910002 | 239173 | 125624 | 0.5252432339770794 | -0.0003758275670622449 | 0.4495239763102592 | -47.21296228462745 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B01 | Random direction with matched trade frequency | baseline | 910003 | 239173 | 235973 | 0.9866205633579042 | 9.641695819043596e-06 | 0.48719133121162167 | 2.2751798875071745 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B02 | Buy-and-hold intraday control | baseline | 910003 | 239173 | 235973 | 0.9866205633579042 | -2.2705277044505813e-05 | 0.49083581596199566 | -5.35783234002317 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B03 | Simple short-term momentum | baseline | 910003 | 239173 | 223623 | 0.9349843000673153 | -0.00028370455484999306 | 0.45755579703339994 | -63.44286366922 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B04 | Opening-range breakout | baseline | 910003 | 239173 | 231704 | 0.968771558662558 | 4.1547627423229095e-05 | 0.49586109864309635 | 9.626751464471875 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B05 | VWAP continuation | baseline | 910003 | 239173 | 232003 | 0.9700216997738039 | -8.893388318421565e-05 | 0.4677180898522864 | -20.632927700387583 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; B05 uses rolling-mid proxy because trade-volume/VWAP is not yet acceptance-grade. |
| B06 | Short-term mean reversion | baseline | 910003 | 239173 | 223623 | 0.9349843000673153 | 0.00028370455484999306 | 0.520550211740295 | 63.44286366922 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |
| B07 | Volatility breakout | baseline | 910003 | 239173 | 125624 | 0.5252432339770794 | -0.0003758275670622449 | 0.4495239763102592 | -47.21296228462745 | False | medium_pilot_proxy_not_acceptance | Medium-pilot baseline proxy; not acceptance-grade. |

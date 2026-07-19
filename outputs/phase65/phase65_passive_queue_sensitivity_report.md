# Phase65 Passive Queue-Capture Sensitivity Replay

Generated UTC: 2026-07-19T19:30:23.422139+00:00

Phase65 starts the passive/limit-order branch after Phase64 retired the marketable-taker families.
Fills are hypothetical: Zerodha top-five market-by-price data does not reveal true order identity or queue position.
The replay therefore tests pessimistic, base and optimistic queue-fill assumptions instead of claiming observed passive fills.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase65_shards_scanned | 16 | Dense shards scanned |
| phase65_strategy_profile_rows | 6 | Strategy/queue-profile rows evaluated |
| phase65_unique_candidate_orders | 2558352 | Unique hypothetical passive order placements before queue-profile expansion |
| phase65_unique_inferred_touch_orders | 61696 | Unique orders whose limit price was touched within the horizon |
| phase65_strategy_profile_expected_fills | 61696 | Expected fills summed across strategy/profile rows |
| phase65_best_expected_net_pnl_inr | -1.02067e+06 | Best expected after-cost P&L across strategy/profile rows |
| phase65_surviving_strategy_count | 0 | Strategies positive under pessimistic, base and optimistic queue assumptions |
| phase65_survives_passive_sensitivity | 0 | 1 means at least one passive strategy survived all queue assumptions |
| phase65_elapsed_seconds | 6.01962 | Elapsed seconds |
| phase65_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Zerodha retail intraday cost model |
| phase65_recommend_next_action | build_passive_adverse_selection_labels | Recommended next action |

## Passive Strategy/Profile Summary

| strategy_id | queue_profile | shards_scanned | symbols | trade_dates | candidate_orders | inferred_touch_orders | expected_fills | expected_gross_pnl_inr | expected_cost_pnl_drag_inr | expected_net_pnl_inr | positive_rows | mean_touch_win_rate | mean_spread_bps | positive_row_fraction | expected_net_pnl_per_fill_inr | phase65_survives_passive_sensitivity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P65_FADE_IMBALANCE | pessimistic_back_of_queue | 6 | 6 | 1 | 1279176 | 31448 | 3144.8 | -603412 | 417256 | -1.02067e+06 | 0 | 0 | 2.38305 | 0 | -324.557 | False |
| P65_JOIN_IMBALANCE | pessimistic_back_of_queue | 6 | 6 | 1 | 1279176 | 30248 | 3024.8 | -628042 | 401334 | -1.02938e+06 | 0 | 0.0047619 | 2.38305 | 0 | -340.312 | False |
| P65_FADE_IMBALANCE | base_mid_queue | 6 | 6 | 1 | 1279176 | 31448 | 9434.4 | -1.81024e+06 | 968736 | -2.77897e+06 | 0 | 0 | 2.38305 | 0 | -294.557 | False |
| P65_JOIN_IMBALANCE | base_mid_queue | 6 | 6 | 1 | 1279176 | 30248 | 9074.4 | -1.88413e+06 | 931770 | -2.8159e+06 | 0 | 0.0047619 | 2.38305 | 0 | -310.312 | False |
| P65_FADE_IMBALANCE | optimistic_front_queue | 6 | 6 | 1 | 1279176 | 31448 | 18868.8 | -3.62047e+06 | 1.5601e+06 | -5.18057e+06 | 0 | 0 | 2.38305 | 0 | -274.557 | False |
| P65_JOIN_IMBALANCE | optimistic_front_queue | 6 | 6 | 1 | 1279176 | 30248 | 18148.8 | -3.76825e+06 | 1.50056e+06 | -5.26882e+06 | 0 | 0.0047619 | 2.38305 | 0 | -290.312 | False |

## Queue Profile Catalog

| queue_profile | fill_weight | adverse_selection_bps | description |
| --- | --- | --- | --- |
| pessimistic_back_of_queue | 0.1 | 5 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. |
| base_mid_queue | 0.3 | 2 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. |
| optimistic_front_queue | 0.6 | 0 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. |

## Daily Symbol Results

| shard_index | trade_date | symbol | strategy_id | candidate_orders | inferred_touch_orders | gross_return_on_touches | mean_gross_return_on_touch | mean_spread_bps | mean_abs_l1_imbalance | touch_win_rate | queue_profile | fill_weight | adverse_selection_bps | zerodha_roundtrip_bps | expected_fills | expected_gross_pnl_inr | expected_cost_pnl_drag_inr | expected_net_pnl_inr | queue_profile_description | positive_after_costs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 2026-01-01 | BANKBEES | P65_JOIN_IMBALANCE | 243948 | 4516 | -7.27743 | -0.00161148 | 3.45861 | 0.328295 | 0 | pessimistic_back_of_queue | 0.1 | 5 | 8.26812 | 451.6 | -72774.3 | 59918.8 | -132693 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. | False |
| 4 | 2026-01-01 | BANKBEES | P65_FADE_IMBALANCE | 243948 | 7000 | -8.23962 | -0.00117709 | 3.45861 | 0.328295 | 0 | pessimistic_back_of_queue | 0.1 | 5 | 8.26812 | 700 | -82396.2 | 92876.8 | -175273 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. | False |
| 8 | 2026-01-01 | CIPLA | P65_JOIN_IMBALANCE | 247916 | 5116 | -12.1457 | -0.00237406 | 2.74954 | 0.568911 | 0 | pessimistic_back_of_queue | 0.1 | 5 | 8.26812 | 511.6 | -121457 | 67879.7 | -189337 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. | False |
| 8 | 2026-01-01 | CIPLA | P65_FADE_IMBALANCE | 247916 | 7200 | -14.2001 | -0.00197224 | 2.74954 | 0.568911 | 0 | pessimistic_back_of_queue | 0.1 | 5 | 8.26812 | 720 | -142001 | 95530.5 | -237532 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. | False |
| 11 | 2026-01-01 | HCLTECH | P65_JOIN_IMBALANCE | 55468 | 1500 | -4.27442 | -0.00284962 | 2.41064 | 0.303145 | 0 | pessimistic_back_of_queue | 0.1 | 5 | 8.26812 | 150 | -42744.2 | 19902.2 | -62646.4 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. | False |
| 11 | 2026-01-01 | HCLTECH | P65_FADE_IMBALANCE | 55468 | 1216 | -3.25245 | -0.00267471 | 2.41064 | 0.303145 | 0 | pessimistic_back_of_queue | 0.1 | 5 | 8.26812 | 121.6 | -32524.5 | 16134 | -48658.5 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. | False |
| 12 | 2026-01-01 | HDFCBANK | P65_JOIN_IMBALANCE | 236012 | 7000 | -15.7791 | -0.00225415 | 1.19743 | 0.571184 | 0.0285714 | pessimistic_back_of_queue | 0.1 | 5 | 8.26812 | 700 | -157791 | 92876.8 | -250667 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. | False |
| 12 | 2026-01-01 | HDFCBANK | P65_FADE_IMBALANCE | 236012 | 4816 | -12.9281 | -0.00268441 | 1.19743 | 0.571184 | 0 | pessimistic_back_of_queue | 0.1 | 5 | 8.26812 | 481.6 | -129281 | 63899.3 | -193181 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. | False |
| 14 | 2026-01-01 | ICICIBANK | P65_JOIN_IMBALANCE | 249900 | 7400 | -14.6668 | -0.00198201 | 1.39362 | 0.367678 | 0 | pessimistic_back_of_queue | 0.1 | 5 | 8.26812 | 740 | -146668 | 98184.1 | -244853 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. | False |
| 14 | 2026-01-01 | ICICIBANK | P65_FADE_IMBALANCE | 249900 | 5116 | -12.2628 | -0.00239695 | 1.39362 | 0.367678 | 0 | pessimistic_back_of_queue | 0.1 | 5 | 8.26812 | 511.6 | -122628 | 67879.7 | -190508 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. | False |
| 16 | 2026-01-01 | ITBEES | P65_FADE_IMBALANCE | 245932 | 6100 | -9.45808 | -0.0015505 | 3.08849 | 0.740932 | 0 | pessimistic_back_of_queue | 0.1 | 5 | 8.26812 | 610 | -94580.8 | 80935.5 | -175516 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. | False |
| 16 | 2026-01-01 | ITBEES | P65_JOIN_IMBALANCE | 245932 | 4716 | -8.66074 | -0.00183646 | 3.08849 | 0.740932 | 0 | pessimistic_back_of_queue | 0.1 | 5 | 8.26812 | 471.6 | -86607.4 | 62572.5 | -149180 | Assume only 10% of inferred touches fill and filled orders suffer 5 bps adverse selection. | False |
| 4 | 2026-01-01 | BANKBEES | P65_JOIN_IMBALANCE | 243948 | 4516 | -7.27743 | -0.00161148 | 3.45861 | 0.328295 | 0 | base_mid_queue | 0.3 | 2 | 8.26812 | 1354.8 | -218323 | 139112 | -357435 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. | False |
| 4 | 2026-01-01 | BANKBEES | P65_FADE_IMBALANCE | 243948 | 7000 | -8.23962 | -0.00117709 | 3.45861 | 0.328295 | 0 | base_mid_queue | 0.3 | 2 | 8.26812 | 2100 | -247189 | 215631 | -462819 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. | False |
| 8 | 2026-01-01 | CIPLA | P65_JOIN_IMBALANCE | 247916 | 5116 | -12.1457 | -0.00237406 | 2.74954 | 0.568911 | 0 | base_mid_queue | 0.3 | 2 | 8.26812 | 1534.8 | -364371 | 157595 | -521966 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. | False |
| 8 | 2026-01-01 | CIPLA | P65_FADE_IMBALANCE | 247916 | 7200 | -14.2001 | -0.00197224 | 2.74954 | 0.568911 | 0 | base_mid_queue | 0.3 | 2 | 8.26812 | 2160 | -426004 | 221791 | -647795 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. | False |
| 11 | 2026-01-01 | HCLTECH | P65_JOIN_IMBALANCE | 55468 | 1500 | -4.27442 | -0.00284962 | 2.41064 | 0.303145 | 0 | base_mid_queue | 0.3 | 2 | 8.26812 | 450 | -128233 | 46206.5 | -174439 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. | False |
| 11 | 2026-01-01 | HCLTECH | P65_FADE_IMBALANCE | 55468 | 1216 | -3.25245 | -0.00267471 | 2.41064 | 0.303145 | 0 | base_mid_queue | 0.3 | 2 | 8.26812 | 364.8 | -97573.4 | 37458.1 | -135032 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. | False |
| 12 | 2026-01-01 | HDFCBANK | P65_JOIN_IMBALANCE | 236012 | 7000 | -15.7791 | -0.00225415 | 1.19743 | 0.571184 | 0.0285714 | base_mid_queue | 0.3 | 2 | 8.26812 | 2100 | -473372 | 215631 | -689002 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. | False |
| 12 | 2026-01-01 | HDFCBANK | P65_FADE_IMBALANCE | 236012 | 4816 | -12.9281 | -0.00268441 | 1.19743 | 0.571184 | 0 | base_mid_queue | 0.3 | 2 | 8.26812 | 1444.8 | -387844 | 148354 | -536198 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. | False |
| 14 | 2026-01-01 | ICICIBANK | P65_JOIN_IMBALANCE | 249900 | 7400 | -14.6668 | -0.00198201 | 1.39362 | 0.367678 | 0 | base_mid_queue | 0.3 | 2 | 8.26812 | 2220 | -440005 | 227952 | -667958 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. | False |
| 14 | 2026-01-01 | ICICIBANK | P65_FADE_IMBALANCE | 249900 | 5116 | -12.2628 | -0.00239695 | 1.39362 | 0.367678 | 0 | base_mid_queue | 0.3 | 2 | 8.26812 | 1534.8 | -367884 | 157595 | -525479 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. | False |
| 16 | 2026-01-01 | ITBEES | P65_FADE_IMBALANCE | 245932 | 6100 | -9.45808 | -0.0015505 | 3.08849 | 0.740932 | 0 | base_mid_queue | 0.3 | 2 | 8.26812 | 1830 | -283742 | 187907 | -471649 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. | False |
| 16 | 2026-01-01 | ITBEES | P65_JOIN_IMBALANCE | 245932 | 4716 | -8.66074 | -0.00183646 | 3.08849 | 0.740932 | 0 | base_mid_queue | 0.3 | 2 | 8.26812 | 1414.8 | -259822 | 145273 | -405095 | Assume 30% of inferred touches fill and filled orders suffer 2 bps adverse selection. | False |
| 4 | 2026-01-01 | BANKBEES | P65_JOIN_IMBALANCE | 243948 | 4516 | -7.27743 | -0.00161148 | 3.45861 | 0.328295 | 0 | optimistic_front_queue | 0.6 | 0 | 8.26812 | 2709.6 | -436646 | 224033 | -660679 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. | False |
| 4 | 2026-01-01 | BANKBEES | P65_FADE_IMBALANCE | 243948 | 7000 | -8.23962 | -0.00117709 | 3.45861 | 0.328295 | 0 | optimistic_front_queue | 0.6 | 0 | 8.26812 | 4200 | -494377 | 347261 | -841638 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. | False |
| 8 | 2026-01-01 | CIPLA | P65_JOIN_IMBALANCE | 247916 | 5116 | -12.1457 | -0.00237406 | 2.74954 | 0.568911 | 0 | optimistic_front_queue | 0.6 | 0 | 8.26812 | 3069.6 | -728742 | 253798 | -982540 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. | False |
| 8 | 2026-01-01 | CIPLA | P65_FADE_IMBALANCE | 247916 | 7200 | -14.2001 | -0.00197224 | 2.74954 | 0.568911 | 0 | optimistic_front_queue | 0.6 | 0 | 8.26812 | 4320 | -852008 | 357183 | -1.20919e+06 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. | False |
| 11 | 2026-01-01 | HCLTECH | P65_JOIN_IMBALANCE | 55468 | 1500 | -4.27442 | -0.00284962 | 2.41064 | 0.303145 | 0 | optimistic_front_queue | 0.6 | 0 | 8.26812 | 900 | -256465 | 74413.1 | -330879 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. | False |
| 11 | 2026-01-01 | HCLTECH | P65_FADE_IMBALANCE | 55468 | 1216 | -3.25245 | -0.00267471 | 2.41064 | 0.303145 | 0 | optimistic_front_queue | 0.6 | 0 | 8.26812 | 729.6 | -195147 | 60324.2 | -255471 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. | False |
| 12 | 2026-01-01 | HDFCBANK | P65_JOIN_IMBALANCE | 236012 | 7000 | -15.7791 | -0.00225415 | 1.19743 | 0.571184 | 0.0285714 | optimistic_front_queue | 0.6 | 0 | 8.26812 | 4200 | -946743 | 347261 | -1.294e+06 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. | False |
| 12 | 2026-01-01 | HDFCBANK | P65_FADE_IMBALANCE | 236012 | 4816 | -12.9281 | -0.00268441 | 1.19743 | 0.571184 | 0 | optimistic_front_queue | 0.6 | 0 | 8.26812 | 2889.6 | -775688 | 238916 | -1.0146e+06 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. | False |
| 14 | 2026-01-01 | ICICIBANK | P65_JOIN_IMBALANCE | 249900 | 7400 | -14.6668 | -0.00198201 | 1.39362 | 0.367678 | 0 | optimistic_front_queue | 0.6 | 0 | 8.26812 | 4440 | -880011 | 367105 | -1.24712e+06 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. | False |
| 14 | 2026-01-01 | ICICIBANK | P65_FADE_IMBALANCE | 249900 | 5116 | -12.2628 | -0.00239695 | 1.39362 | 0.367678 | 0 | optimistic_front_queue | 0.6 | 0 | 8.26812 | 3069.6 | -735768 | 253798 | -989566 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. | False |
| 16 | 2026-01-01 | ITBEES | P65_FADE_IMBALANCE | 245932 | 6100 | -9.45808 | -0.0015505 | 3.08849 | 0.740932 | 0 | optimistic_front_queue | 0.6 | 0 | 8.26812 | 3660 | -567485 | 302613 | -870098 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. | False |
| 16 | 2026-01-01 | ITBEES | P65_JOIN_IMBALANCE | 245932 | 4716 | -8.66074 | -0.00183646 | 3.08849 | 0.740932 | 0 | optimistic_front_queue | 0.6 | 0 | 8.26812 | 2829.6 | -519644 | 233955 | -753599 | Assume 60% of inferred touches fill with no extra adverse-selection haircut. | False |

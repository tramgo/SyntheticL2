# Phase308 Event-Catalyst Join Quality Audit

Phase308 audits the Phase307 joined event/top-five-depth artifact before any feature construction or strategy search.

## Acceptance summary

| metric | value | description |
| --- | --- | --- |
| phase308_join_quality_audit_complete | 1 | Phase308 joined event/depth quality audit completed |
| phase308_joined_rows | 2721782 | Joined rows audited |
| phase308_materialized_event_rows | 1 | Distinct materialized events |
| phase308_materialized_symbols | 32 | Distinct materialized symbols |
| phase308_symbol_quality_rows | 32 | Event-symbol quality rows |
| phase308_required_columns_present | 1 | Required joined columns present |
| phase308_full_depth_columns_present | 1 | Depth levels 1-5 columns present |
| phase308_required_null_cells | 0 | Null cells in required columns |
| phase308_hard_issue_rows | 0 | Hard issue rows |
| phase308_strategy_search_allowed_now | 0 | No strategy search in Phase308 |
| phase308_strategy_replay_allowed | 0 | No replay |
| phase308_strategy_promotion_allowed | 0 | No promotion |
| phase308_paper_or_live_acceptance_allowed | 0 | No paper/live |
| phase308_deployable_profitability_claim_allowed | 0 | No deployable profitability claim |
| phase308_hard_gate_pass_rows | 9 | Passed hard gates |
| phase308_hard_gate_rows | 9 | Hard gates |
| phase308_next_best_action | run_phase309_event_catalyst_feature_precommit_no_strategy_search | Recommended next action |

## Symbol quality preview

| event_id | symbol | rows | relative_second_min | relative_second_max | distinct_relative_seconds | duplicate_event_symbol_second_rows | non_crossed_l1_rows | bid_depth_monotonic_rows | ask_depth_monotonic_rows | positive_depth_quantity_rows | positive_depth_order_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P306_EVT_0002 | ADANIPORTS | 85930 | -900 | 1800 | 2701 | 83229 | 85930 | 85930 | 85930 | 85930 | 85930 |
| P306_EVT_0002 | AXISBANK | 86352 | -900 | 1800 | 2701 | 83651 | 86352 | 86352 | 86352 | 86352 | 86352 |
| P306_EVT_0002 | BAJAJ-AUTO | 84440 | -900 | 1800 | 2701 | 81739 | 84440 | 84440 | 84440 | 84440 | 84440 |
| P306_EVT_0002 | BANKBEES | 89892 | -900 | 1800 | 2701 | 87191 | 89892 | 89892 | 89892 | 89892 | 89892 |
| P306_EVT_0002 | BHARTIARTL | 85327 | -900 | 1800 | 2701 | 82626 | 85327 | 85327 | 85327 | 85327 | 85327 |
| P306_EVT_0002 | BPCL | 85675 | -900 | 1800 | 2701 | 82974 | 85675 | 85675 | 85675 | 85675 | 85675 |
| P306_EVT_0002 | BRITANNIA | 84434 | -900 | 1800 | 2701 | 81733 | 84434 | 84434 | 84434 | 84434 | 84434 |
| P306_EVT_0002 | CIPLA | 87819 | -900 | 1800 | 2701 | 85118 | 87819 | 87819 | 87819 | 87819 | 87819 |
| P306_EVT_0002 | DRREDDY | 86138 | -900 | 1800 | 2701 | 83437 | 86138 | 86138 | 86138 | 86138 | 86138 |
| P306_EVT_0002 | GOLDBEES | 86554 | -900 | 1800 | 2701 | 83853 | 86554 | 86554 | 86554 | 86554 | 86554 |
| P306_EVT_0002 | HCLTECH | 84900 | -900 | 1800 | 2701 | 82199 | 84900 | 84900 | 84900 | 84900 | 84900 |
| P306_EVT_0002 | HDFCBANK | 81606 | -900 | 1800 | 2701 | 78905 | 81606 | 81606 | 81606 | 81606 | 81606 |
| P306_EVT_0002 | HINDUNILVR | 79410 | -900 | 1800 | 2701 | 76709 | 79410 | 79410 | 79410 | 79410 | 79410 |
| P306_EVT_0002 | ICICIBANK | 78383 | -900 | 1800 | 2701 | 75682 | 78383 | 78383 | 78383 | 78383 | 78383 |
| P306_EVT_0002 | INFY | 86901 | -900 | 1800 | 2701 | 84200 | 86901 | 86901 | 86901 | 86901 | 86901 |
| P306_EVT_0002 | ITBEES | 84640 | -900 | 1800 | 2701 | 81939 | 84640 | 84640 | 84640 | 84640 | 84640 |
| P306_EVT_0002 | ITC | 86816 | -900 | 1800 | 2701 | 84115 | 86816 | 86816 | 86816 | 86816 | 86816 |
| P306_EVT_0002 | JUNIORBEES | 84742 | -900 | 1800 | 2701 | 82041 | 84742 | 84742 | 84742 | 84742 | 84742 |
| P306_EVT_0002 | KOTAKBANK | 81137 | -900 | 1800 | 2701 | 78436 | 81137 | 81137 | 81137 | 81137 | 81137 |
| P306_EVT_0002 | LT | 84090 | -900 | 1800 | 2701 | 81389 | 84090 | 84090 | 84090 | 84090 | 84090 |
| P306_EVT_0002 | M&M | 80859 | -900 | 1800 | 2701 | 78158 | 80859 | 80859 | 80859 | 80859 | 80859 |
| P306_EVT_0002 | MARUTI | 84687 | -900 | 1800 | 2701 | 81986 | 84687 | 84687 | 84687 | 84687 | 84687 |
| P306_EVT_0002 | NESTLEIND | 88082 | -900 | 1800 | 2701 | 85381 | 88082 | 88082 | 88082 | 88082 | 88082 |
| P306_EVT_0002 | NIFTYBEES | 84352 | -900 | 1800 | 2701 | 81651 | 84352 | 84352 | 84352 | 84352 | 84352 |
| P306_EVT_0002 | ONGC | 82748 | -900 | 1800 | 2701 | 80047 | 82748 | 82748 | 82748 | 82748 | 82748 |
| P306_EVT_0002 | RELIANCE | 82550 | -900 | 1800 | 2701 | 79849 | 82550 | 82550 | 82550 | 82550 | 82550 |
| P306_EVT_0002 | SBIN | 84692 | -900 | 1800 | 2701 | 81991 | 84692 | 84692 | 84692 | 84692 | 84692 |
| P306_EVT_0002 | SUNPHARMA | 86902 | -900 | 1800 | 2701 | 84201 | 86902 | 86902 | 86902 | 86902 | 86902 |
| P306_EVT_0002 | TCS | 87069 | -900 | 1800 | 2701 | 84368 | 87069 | 87069 | 87069 | 87069 | 87069 |
| P306_EVT_0002 | TECHM | 88790 | -900 | 1800 | 2701 | 86089 | 88790 | 88790 | 88790 | 88790 | 88790 |
| P306_EVT_0002 | ULTRACEMCO | 87316 | -900 | 1800 | 2701 | 84615 | 87316 | 87316 | 87316 | 87316 | 87316 |
| P306_EVT_0002 | WIPRO | 88549 | -900 | 1800 | 2701 | 85848 | 88549 | 88549 | 88549 | 88549 | 88549 |

## Issue ledger

| issue_id | severity | observed | required |
| --- | --- | --- | --- |
| none |  |  |  |

## Gates

| gate_id | passed | observed_value | required_value | severity |
| --- | --- | --- | --- | --- |
| P308_PHASE307_MATERIALIZED_ROWS | True | 2721782 | >0 | hard |
| P308_REQUIRED_COLUMNS_PRESENT | True | 1 | 1 | hard |
| P308_FULL_DEPTH_COLUMNS_PRESENT | True | 1 | 1 | hard |
| P308_JOINED_ROWS_NONEMPTY | True | 2721782 | >0 | hard |
| P308_SYMBOL_BREADTH_32 | True | 32 | >=32 | hard |
| P308_EVENT_BREADTH_NONZERO | True | 1 | >=1 | hard |
| P308_NO_HARD_QUALITY_ISSUES | True | 0 | 0 | hard |
| P308_NO_STRATEGY_SEARCH_OPENED | True | strategy_search_allowed_now=0 | 0 | hard |
| P308_BOUNDARIES_CLOSED | True | replay=0;promotion=0;paper=0;claim=0 | all_zero | hard |

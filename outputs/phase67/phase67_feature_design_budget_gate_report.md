# Phase67 Feature Design and Experiment-Budget Gate

Generated UTC: 2026-07-19T19:35:27.896063+00:00

Phase67 responds to the failed Phase66 passive imbalance labels by returning to feature design under strict budget gates.
The purpose is to prevent another expensive full-year replay until a genuinely new feature family passes small, disjoint, cost-aware tests.

## Acceptance Summary

| metric | value | description |
| --- | --- | --- |
| phase67_source_phase66_survives_label_gate | 0 | Phase66 passive imbalance label gate |
| phase67_source_phase66_best_after_cost_bps | -17.0135 | Best Phase66 after-cost touch label |
| phase67_feature_families_queued | 4 | New feature families queued for bounded testing |
| phase67_budget_gates_declared | 5 | Predeclared gates before large replay |
| phase67_allow_full_year_replay_now | 0 | 0 means no new full-year replay until a new family passes the declared gates |
| phase67_next_priority_feature_family | F67_replenishment_after_touch | Highest-priority next feature family |
| phase67_next_priority_experiment | No-lookahead label discovery for post-touch depth replenishment and next-100-tick mid outcome. | Next bounded experiment |
| phase67_zerodha_cost_model_version | zerodha_equity_intraday_nse_order_formula_v2_2026_07_14 | Cost model to preserve in next experiments |

## Feature Design Queue

| priority | feature_family_id | hypothesis | required_inputs | first_experiment | small_sample_budget | scale_gate | reason_for_priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | F67_replenishment_after_touch | After a best-bid/best-ask touch, rapid visible replenishment may identify liquidity support/resistance better than static imbalance. | L1-L5 quantity changes, touch inference, local sequence ordering, spread and mid-price path. | No-lookahead label discovery for post-touch depth replenishment and next-100-tick mid outcome. | 32 shards x 250k rows | At least 2 disjoint symbols and 2 disjoint months positive after costs; adverse-selection rate <= 45%; cost-clearing rate >= 55%. | Phase66 showed static imbalance touches were adverse; replenishment tests whether dynamic book repair carries different information. |
| 2 | F67_spread_compression_expansion | Transitions from wide-to-tight or tight-to-wide spreads may be more informative than the spread level alone. | Spread bps, rolling spread rank, mid-price movement, L1-L5 depth state. | Event-bar label discovery for spread regime transitions with taker and passive variants separated. | 32 shards x 250k rows | Positive no-lookahead validation under retail costs and stable sign across at least 50% of active symbols. | Marketable and passive static imbalance failed; spread transition features may target liquidity regime changes instead of directional imbalance. |
| 3 | F67_cross_symbol_lead_lag | Index/bank/IT ETF and large-cap quote moves may lead slower constituents enough to beat costs at lower frequency. | Synchronized event-time bars by symbol, sector/ETF groups, lagged returns, lagged OFI/MLOFI proxies. | DuckDB event-bar matrix build plus no-lookahead lead-lag label scan. | 1 month all 32 symbols at event-bar frequency | Disjoint-month positive after-cost validation with turnover low enough that cost drag < 50% of gross edge. | Single-symbol tick-local features repeatedly failed; cross-symbol information is a genuinely different axis in the plan. |
| 4 | F67_shock_resilience_mean_reversion | Synthetic shock/reconnect/regime tags may identify overreaction pockets where lower turnover mean reversion survives costs. | Regime code, shock flags, feed profile, event bars, post-shock liquidity normalization. | Regime-conditioned lower-frequency labels for shock recovery windows. | All shock-tagged shards with capped rows | Positive after-cost P&L in at least two shock classes and negative-control non-shock comparison not driving the result. | The generator explicitly contains regimes and shocks; these should be used as falsifiable stress-test features, not ignored. |

## Experiment Budget Gates

| gate_id | rule | required_evidence | failure_action |
| --- | --- | --- | --- |
| G67_01_small_before_large | No feature family may request a full-year replay before passing a bounded small-sample discovery and disjoint validation. | Discovery artifact, disjoint validation artifact, acceptance summary and manifest. | retire_or_redesign_feature_family |
| G67_02_no_oracle_promotion | Oracle, zero-latency, zero-cost or hindsight-positive rows cannot be promoted to deployable candidates. | Candidate catalog must mark deployable=false for oracle/control rows. | keep_as_control_only |
| G67_03_cost_drag_limit | A candidate cannot scale if cost drag consumes more than 50% of gross edge on validation. | gross_pnl_proxy_inr, cost_pnl_drag_proxy_inr and net_pnl_inr reported on validation. | reduce_turnover_or_retire |
| G67_04_stability | A candidate cannot scale if it is positive only in one symbol, one month, or one sparse interaction cell. | Symbol, month and bucket/stability rollups. | falsification_probe_or_retire |
| G67_05_passive_fill_honesty | Passive results must be reported as assumption sensitivity until real fills, contract notes or true queue data are available. | Queue profile catalog and pessimistic/base/optimistic sensitivity outputs. | do_not_claim_live_fill_profitability |

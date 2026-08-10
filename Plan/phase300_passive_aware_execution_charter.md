# Phase300 Precommit Charter: Passive-Aware Execution of Directional L2 Signals

Charter ID: `P300_PASSIVE_AWARE_DIRECTIONAL_L2_EXECUTION`

Status: `PRECOMMIT_NO_RESULTS_GENERATED`

Authored from attached charter: 2026-08-04

This document is committed before generating Phase300 backtest results.

## Thesis

Prior Phase185-Phase298 strategy families showed the same hard arithmetic: thin short-horizon top-five-depth edges can appear before costs, but they generally die against the fixed retail cost toll under Zerodha-style cost200 stress when taker execution crosses the spread on entry and exit.

Phase300 tests the remaining retail-realistic cost-side lever: passive-aware execution of already-discovered directional L2 signals.

This is not two-sided continuous market-making. Retail has no assumed maker rebate, weak queue priority and slow cancel risk. The policy is:

- place a passive limit entry near the bid or ask according to side;
- wait briefly;
- cancel if the market moves away;
- cross aggressively only when expected move comfortably exceeds total cost;
- exit passively when calm;
- exit aggressively when risk rises, the signal expires, or end-of-day/end-of-signal flattening is required;
- never stay exposed merely to save spread.

## Inputs

Phase300 reuses validated components; it is not a new alpha search.

| Component | Source phase | Role |
|---|---:|---|
| Directional entry signals | P235, P268, P280-P282, P298 sparse directional seeds | When to want a position |
| Passive fill / queue-depth features | P260-P269 | Estimate fill probability |
| Adverse-selection / toxicity estimate | P130, P280-P282 | Fill-conditioned penalty |
| Feed-imperfection / regime filter | P130 | Skip toxic or degraded feed windows |
| Calibrated cost model + 2x stress | `zerodha_equity_intraday_nse_order_formula_v2_2026_07_14` | Net scoring |
| Raw dense top-five book state | P51 lake, P298 schema audit | Top-five market-by-price depth levels 1-5 price/qty/order-count |

No L1-only variants are allowed. Levels 2-5 materiality is required. Net-edge live masks are forbidden.

## Mandatory realism penalties

1. Passive fill model: passive entry fills only with probability `P(fill | queue_depth, side, horizon)` estimated from raw depth levels 1-5. Retail starts with a pessimistic back-of-queue prior.
2. Adverse-selection penalty: when a passive order fills, apply fill-conditioned toxicity/adverse-selection penalty.
3. Forced-flatten cost: any inventory unexited by end-of-signal or end-of-day pays taker spread plus full statutory cost to flatten.

Brokerage per executed order, STT sell-side, transaction charges, GST, SEBI charges and stamp duty apply to passive and aggressive fills. No maker rebate is assumed.

## Hard execution gates for the next phase

- Phase299 routes to Phase300.
- All input components are version-pinned.
- Raw top-five market-by-price depth levels 1-5 price/qty/order-count are used.
- `l1_only_variant_rows = 0`.
- Passive fill model is applied; fills are never assumed.
- Adverse-selection penalty is applied to every passive fill.
- Forced-flatten cost is applied to leftover inventory.
- `net_edge_live_mask_rows = 0`.
- Cost200 scoring and fixed initial-capital denominator are used.
- Replay, promotion, paper/live acceptance and deployable profitability claims remain closed.

## Acceptance diagnostics

Acceptance still requires:

- scheduled event rows `>= 30`;
- cost200 annualized return `> 12%`;
- multi-symbol and multi-date breadth;
- no cost-stress ordering reversal;
- rank stability from 1x cost to 2x cost.

A sparse result above 12% on fewer than 30 events is a discovery clue only, never acceptance.

## Kill-switch

Close this route for acceptance and route to the terminal report if any of these holds after the honest run:

- robust portfolio above12 scenario rows are zero at cost200;
- the best clue remains sparse, meaning fewer than 30 events;
- the edge survives only when any mandatory realism penalty is weakened.

Do not relax the 12% bar, drop a realism penalty, assume a rebate, or add more filters to rescue the same stack.

## Boundaries

- `strategy_replay_allowed = 0`
- `strategy_promotion_allowed = 0`
- `paper_or_live_acceptance_allowed = 0`
- `deployable_profitability_claim_allowed = 0`

## Next best action

After Phase299 and this precommit complete:

`run_phase300_passive_aware_execution_hybrid_no_paper_live`

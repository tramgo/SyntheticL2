# Comprehensive Plan: Synthetic Zerodha L2 Data Generation and Strategy Validation

## 1. Objective

Build a controlled synthetic-data research environment for 32 NSE instruments using the supplied Zerodha retail five-level WebSocket tick day as the initial microstructure calibration seed and later real days for stronger multi-day calibration.

The synthetic environment should support:

- initial testing with approximately three months of simulated trading days;
- later extension to a full synthetic year;
- five-level market-by-price bid/ask depth;
- tick-wise quote and trade updates;
- multiple market regimes;
- market-wide and ticker-specific shocks;
- realistic intraday seasonality;
- realistic cross-ticker correlation;
- execution-aware backtesting;
- storage and compute optimization;
- systematic validation of all priority L2 strategies.

The system is intended for **research, falsification, pipeline testing and stress testing**. Synthetic profitability must never be treated as proof that a strategy will earn the same returns in live NSE trading.

### 1.1 Confirmed workspace inputs as of 2026-07-13

The current workspace contains:

- plan: `Plan/zerodha_l2_synthetic_data_strategy_validation_plan.md`;
- sample: `real_data_sample/l2_single_day`;
- source trading date: `2026-07-13`;
- 32 symbol partitions;
- 50,205 Parquet batch files containing 620,853 tick rows;
- approximately 1.764 GB of Parquet data;
- 1–31 rows per Parquet file, with all files readable and using the same 54-column schema;
- 1,569 batch files for most symbols and 1,568 for GOLDBEES, JUNIORBEES and NIFTYBEES;
- WebSocket-based tick-wise Zerodha updates inside the files;
- typical observed per-symbol receive intervals of approximately 0.5–2 seconds, varying with symbol activity;
- an approximately 14-second file-flush cadence, which must not be confused with tick sampling cadence.

The Azure manifest and local file counts agree. The three 1,568-row partitions are therefore treated as source-side capture differences, not incomplete downloads.

### 1.2 Fixed instrument universe

**Equities (27):** ADANIPORTS, AXISBANK, BAJAJ-AUTO, BHARTIARTL, BPCL, BRITANNIA, CIPLA, DRREDDY, HCLTECH, HDFCBANK, HINDUNILVR, ICICIBANK, INFY, ITC, KOTAKBANK, LT, M&M, MARUTI, NESTLEIND, ONGC, RELIANCE, SBIN, SUNPHARMA, TCS, TECHM, ULTRACEMCO, WIPRO.

**ETFs (5):** BANKBEES, GOLDBEES, ITBEES, JUNIORBEES, NIFTYBEES.

Equities and ETFs must be profiled separately before pooled shrinkage because their prices, displayed quantities, activity, and zero-depth behaviour can differ materially.

### 1.3 Current data-readiness decision

The supplied day is a **received WebSocket tick-wise L2 stream stored in small batches**. It is accepted for:

- schema and field audit;
- price, spread and displayed-depth scale checks;
- received-tick event-rate and inter-arrival profiling at Zerodha retail-feed resolution;
- sequential L2 state-change and OFI/MLOFI reconstruction with market-by-price limitations;
- intraday and cross-sectional tick-stream profiles;
- storage compaction and replay-pipeline engineering;
- generator interface and structural-invariant testing.

One day remains insufficient evidence for:

- regime frequencies and transitions;
- annual volatility, tail-event and cross-regime distributions;
- robust out-of-sample strategy profitability;
- stable event-model parameters across days.

The retail top-five market-by-price feed also cannot directly identify individual exchange orders, exact queue position, all exchange-side events, hidden liquidity, or true passive fills. Add/cancel/consume, aggressor side, replenishment and queue behaviour remain **inferences or assumptions**, even when reconstructed from consecutive received ticks.

Feature horizons must be gated by observed per-symbol update density. The data may support 500 ms or 1 second work for active symbols, but 100 ms and 250 ms views will often be sparse or forward-filled and cannot automatically be treated as equally evidenced across the universe.

---

## 2. Important Constraints

### 2.1 What the current one-day WebSocket tick sample can calibrate

A single received-tick day across 32 instruments can provide useful estimates of:

- actual Parquet schema;
- Zerodha timestamp fields and update behaviour;
- field completeness;
- per-ticker received event rates and inter-arrival distributions for that day;
- price and quantity scales;
- tick sizes;
- spreads;
- visible depth shapes;
- intraday activity profiles for that day;
- last-traded-quantity and depth-size distributions at received update times;
- relationships among L1-L5 quantities;
- approximate quote/trade and cumulative-volume relationships between consecutive received updates;
- file-size and compression characteristics;
- receive-time synchronization quality across tickers.

It cannot turn changes suppressed, aggregated or unobserved by the retail feed into exchange-order events. Resampled views must report coverage, staleness and forward-fill rates by symbol and horizon.

### 2.2 What one day cannot identify reliably

One day is insufficient to infer:

- true regime transition probabilities;
- annual volatility distributions;
- tail-event frequency;
- rally/crash duration;
- earnings-event behaviour;
- expiry-day effects;
- budget/RBI/election reactions;
- month-end and quarter-end behaviour;
- long-term changes in liquidity;
- robust cross-regime correlations;
- realistic annual strategy returns.

In addition, received top-five market-by-price updates are insufficient to directly observe:

- individual order identities and exact queue priority;
- every exchange-side add, cancel and trade between retail-feed updates;
- hidden-liquidity or iceberg identity;
- deterministic passive fills;
- exchange-level causality from receive-time ordering alone.

Therefore, the generator must combine:

1. **empirical calibration** from the supplied real day;
2. **controlled regime assumptions**;
3. **stress scenarios**;
4. **stylized market-microstructure constraints**;
5. later recalibration as more real days become available.

---

## 3. Recommended Overall Architecture

Use a hierarchical, regime-conditioned simulator rather than duplicating and perturbing the sample day.

```text
Trading calendar
    ↓
Daily market regime
    ↓
Intraday regime schedule
    ↓
Market/index latent process
    ↓
Sector latent processes
    ↓
Ticker latent efficient prices
    ↓
Liquidity/spread/depth state
    ↓
Order-flow and trade events
    ↓
Top-five L2 snapshots/events
    ↓
Retail receive latency and data imperfections
    ↓
Parquet output
```

### 3.1 Recommended hybrid generation approach

| Layer | Recommended method |
|---|---|
| Annual and daily regime scheduling | Hidden/semi-Markov state model with explicit scenario overrides |
| Efficient market/sector/ticker prices | Correlated stochastic process with jumps and stochastic volatility |
| Intraday seasonality | Empirical time-of-day curves calibrated from the sample day and adjusted by regime |
| Spread and liquidity | Conditional statistical model by ticker, time, volatility and regime |
| L1-L5 depth shape | Conditional distribution or copula model |
| Event timing | Hawkes-like or regime-conditioned point process |
| Queue additions/cancellations/trades | State-dependent probabilistic event engine |
| Top-five book output | Deterministic market-by-price reconstruction from generated events |
| Extreme scenarios | Explicit scenario injection |
| Retail feed behaviour | Latency, batching, missing updates and reconnect simulation |
| Optional advanced generator | Conditional diffusion/GAN/Transformer only after baseline model is validated |

A simpler transparent simulator should be built before attempting deep generative models.

---

## 4. Project Phases

## Phase 0 — Intake Contract for the Real Sample Data

Before generation, establish a strict input contract.

### 4.1 Expected input

Maintain two explicit intake classes.

**Class A — periodic polling snapshot input:**

- one complete NSE trading day where possible;
- clearly identifiable symbol and instrument token;
- exchange, last-trade and local receive timestamps;
- L1-L5 prices, quantities and order counts;
- known polling/sampling cadence;
- no claim that changes between snapshots were observed.

**Class B — received WebSocket tick input (the current sample):**

- subscription-driven output containing every callback/update received by the collector;
- raw receive ordering preserved with a strictly increasing local sequence;
- connection ID and reconnect boundaries where captured;
- dropped-message, parsing-error and subscription diagnostics where captured;
- no resampling before persistence;
- buffered multi-row Parquet files rather than one-row files.

Class A is sufficient for structural calibration only. Class B supports received-event timing, MLOFI, resilience proxies and short-horizon labels at horizons justified by observed density. Neither class proves exchange queue state or passive fills.

### 4.2 Desired fields

| Category | Desired fields |
|---|---|
| Identity | instrument token, trading symbol, exchange, segment |
| Timestamps | exchange timestamp, last-trade timestamp, local receive timestamp |
| Trade | last traded price, last traded quantity, cumulative volume, average traded price |
| Market summary | OHLC, total buy quantity, total sell quantity |
| Depth L1-L5 bid | price, quantity, order count |
| Depth L1-L5 ask | price, quantity, order count |
| Derivatives, if present | open interest, OI day high, OI day low |
| Capture diagnostics | connection ID, reconnect marker, local sequence, parser version |

### 4.3 Mandatory schema audit

For every ticker:

- row count;
- first and last timestamp;
- duplicate timestamp count;
- monotonic ordering violations;
- null rate per field;
- crossed-book frequency;
- locked-book frequency;
- invalid negative quantity;
- off-tick prices;
- stale intervals;
- cumulative-volume reversals;
- depth-level sorting errors;
- file size;
- compressed bytes per row.

Output an automated `data_quality_report.parquet` and human-readable Markdown report.

### 4.4 Intake acceptance gates

| Gate | Current sample | Consequence |
|---|---|---|
| All 32 requested symbols represented | Pass | Cross-sectional snapshot work may proceed |
| Local files match source manifest | Pass | No download repair is currently required |
| Five-level price/quantity/order fields present | Pass on inspected schema | Structural L2 profiling may proceed after full audit |
| One or more rows per source file | Pass: 1–31 rows per file | Compaction is strongly recommended before repeated analysis |
| WebSocket tick-wise capture | Pass | Received-event profiling may proceed |
| Receive ordering | Partial pass: receive UTC milliseconds plus monotonic nanoseconds are present | Verify ties and monotonicity before event reconstruction |
| Connection/reconnect diagnostics in row schema | Not present in inspected 54-column schema | Gap/reconnect attribution remains limited |
| Sub-second observation density | Mixed by symbol | Gate each feature horizon using empirical coverage and staleness |

No downstream work package may silently convert a failed or partial gate into a calibrated parameter. Unsupported parameters must be supplied as documented scenario assumptions with sensitivity ranges.

---

## Phase 1 — Normalize and Reconstruct the Real Day

### 5.1 Canonical normalized schema

Use one canonical table shape, but identify each dataset's observation semantics explicitly as `poll_snapshot`, `received_tick` or `synthetic_event`. The current real day must be labelled `received_tick`; compaction must preserve receive order and batch provenance.

```text
trading_date
event_ts_exchange
event_ts_receive
instrument_token
symbol
sequence_local
ltp
last_trade_qty
cum_volume
avg_trade_price
open
high
low
close
total_buy_qty
total_sell_qty
bid_px_1 ... bid_px_5
bid_qty_1 ... bid_qty_5
bid_orders_1 ... bid_orders_5
ask_px_1 ... ask_px_5
ask_qty_1 ... ask_qty_5
ask_orders_1 ... ask_orders_5
spread_ticks
mid_price
microprice_l1
book_valid
connection_id
is_reconnect_boundary
```

### 5.2 Derive received-tick deltas

For the current Class B sample, create a received-tick delta table containing:

- elapsed time between observations;
- price change;
- spread change;
- per-level bid/ask quantity change;
- per-level price shift;
- cumulative-volume increment;
- inferred depth withdrawal/recovery indicators;
- book slope;
- book convexity;
- coarse local volatility.

Consecutive received-tick differences may be used for OFI/MLOFI and state-change features, while retaining the elapsed receive time and feed limitations.

Add/cancel/consume quantities, aggressor side and replenishment remain inferred because the feed exposes market-by-price state rather than individual order events. Store confidence/ambiguity flags and never relabel these inferences as direct exchange observations.

Do not overwrite the raw normalized data.

### 5.3 Resampled research views

For Class B data and synthetic event streams, create separate views at:

- 100 ms;
- 250 ms;
- 500 ms;
- 1 second;
- 5 seconds;
- 15 seconds;
- 1 minute.

Only create a view when its interval is supported by source observation density for the intended comparison. Report per-symbol update coverage, stale fraction and forward-fill fraction at every interval; exclude or separately label horizons with inadequate coverage.

The raw received-tick stream is the source of truth for the current Class B data.

**Current implementation status as of 2026-07-14:** Phase 1 has an initial runnable implementation in `scripts/run_phase1_received_tick_features.py`, backed by `src/synthetic_l2/phase1_received_tick_features.py`, plus a received-tick event-inference companion in `scripts/run_phase1_event_reconstruction.py`, backed by `src/synthetic_l2/phase1_event_reconstruction.py`.

Generated artifacts are under `outputs/phase1/`:

- `phase1_report.md`;
- `phase1_feature_summary.csv`;
- `event_reconstruction/event_reconstruction_report.md`;
- `event_reconstruction/event_reconstruction_manifest.json`;
- `event_reconstruction/event_reconstruction_summary.csv`;
- `event_reconstruction/event_reconstruction_quality.csv`;
- normalized received-tick Parquet files under `normalized_ticks_by_symbol/symbol=*/normalized_ticks.parquet`;
- received-tick delta Parquet files under `received_tick_deltas_by_symbol/symbol=*/received_tick_deltas.parquet`.

The current completed run processed all 32 symbols and preserved 620,853 rows in both the normalized and delta outputs. The delta output includes elapsed receive time, price/mid/microprice/spread changes, cumulative-volume increments, per-level bid/ask quantity deltas, per-level price shifts, L1 and L5 imbalance, MLOFI quantity, inferred withdrawal/replenishment flags, weak aggressor-side labels, book slope/convexity and rolling local volatility. The event-inference companion evaluated the same 620,853 rows and produced explicit quality summaries for weak trade-side classification, visible-depth replenishment and add/cancel/consume proxies: 144,489 classified trade-side rows, 344,771 replenishment proxy rows and 360,142 queue-event proxy rows. These labels are explicitly marked as non-acceptance-grade market-by-price inferences, not direct exchange event observations.

Important Phase 1 caveat: all 32 symbols have at least two receive gaps greater than 15 seconds in the one-day sample. These rows are explicitly flagged in the delta outputs and must be excluded, segmented or separately modelled before using short-horizon labels.

---

## Phase 2 — Empirical Calibration from the Real Day

For each ticker estimate the following from received ticks, while attaching uncertainty and one-day scope labels to every parameter.

### 6.1 Price and tick characteristics

- reference price;
- minimum tick;
- spread in ticks;
- spread distribution;
- mid-price return distribution;
- realized volatility by time bucket;
- jump frequency within the sample day;
- high-low range;
- gap behaviour between updates.

### 6.2 Activity characteristics

**Current Class B sample:**

- received-event cadence and gaps;
- fraction of successive ticks with a book-state change;
- fraction of successive ticks with a cumulative-volume change;
- time-of-day event intensity for the sample day;
- event inter-arrival distribution and burstiness;
- quote-only versus cumulative-volume-changing update proxies;
- cumulative volume curve.

**Capture diagnostics still required for stronger attribution:**

- explicit reconnect boundaries;
- connection and subscription identifiers;
- dropped-message counters;
- parser-error counters;
- exact distinction between a quiet instrument and a degraded connection.

### 6.3 Depth characteristics

At each level and time bucket:

- quantity distribution;
- order-count distribution;
- quantity per displayed order;
- distance from midpoint;
- depth concentration;
- bid/ask imbalance;
- cross-level correlation;
- depth slope;
- convexity;
- probability of empty/depleted levels;
- inferred recovery across consecutive received ticks.

Replenishment rate, cancellation proxies and resilience may be estimated from received state changes, but must remain inference-labelled and sensitivity-tested because intervening exchange events can be aggregated.

### 6.4 Trade-flow characteristics

The current Class B sample supports received-tick trade-flow proxies from last-traded quantity, cumulative-volume increments and price/book changes. The number and side of exchange trades between received states can still be ambiguous.

Estimate with ambiguity flags:

- observed last-traded-quantity distribution;
- approximate aggressor side;
- buy/sell run lengths and trade imbalance;
- received-tick price response to trade imbalance or OFI;
- trade-to-depth ratio at event time;
- clustered trade intensity.

### 6.5 Cross-sectional characteristics

Across all 32 instruments:

- return correlation;
- received-event intensity correlation;
- volume correlation;
- spread correlation;
- market beta proxy;
- sector cluster proxy;
- simultaneous shock frequency;
- lead-lag exploration using receive timestamps, with timestamp-skew and common-shock controls;
- common intraday seasonality.

With one day, shrink all estimates heavily toward pooled cross-sectional values.

**Current implementation status as of 2026-07-13:** Phase 2 has an initial runnable implementation in `scripts/run_phase2_empirical_calibration.py`, backed by `src/synthetic_l2/phase2_empirical_calibration.py`.

Generated artifacts are under `outputs/phase2/`:

- `phase2_calibration_report.md`;
- `price_tick_calibration.csv`;
- `activity_calibration.csv`;
- `depth_calibration.csv`;
- `trade_flow_calibration.csv`;
- `cross_section_class_summary.csv`;
- `cross_section_correlation_summary.csv`;
- `parameter_evidence_ledger.csv`;
- `calibration_manifest.json`.

The first completed run calibrated all 32 symbols and represented 620,853 rows. It produced one-day measured distributions for reference prices, spreads, event cadence, stale gaps, visible L1-L5 depth, imbalance and depth-shape measures. MLOFI, withdrawal/replenishment and trade-flow pressure remain weakly inferred because the feed is market-by-price state, not individual exchange order events. Five-second cross-symbol correlation is reported as weak one-day evidence only.

Important Phase 2 caveat: regime-transition probabilities, shock frequencies and queue/fill-priority parameters remain blocked from the current one-day sample.

---

## Phase 3 — Regime Taxonomy

Use regimes at three levels:

1. daily market regime;
2. intraday market regime;
3. ticker-specific state.

## 7. Daily market regimes

| Code | Regime | Description |
|---|---|---|
| D01 | Normal balanced | Typical volatility, normal spreads and mixed direction |
| D02 | Low-volatility sideways | Narrow range, low volume, repeated mean reversion |
| D03 | High-volatility sideways | Wide oscillation without sustained direction |
| D04 | Gradual bullish trend | Persistent positive drift and constructive OFI |
| D05 | Strong rally | High participation, expanding volume, repeated upside breakouts |
| D06 | Gradual bearish trend | Persistent negative drift |
| D07 | Sell-off/panic | High volatility, thin bids, spread widening and correlated falls |
| D08 | Gap-up continuation | Positive opening gap followed by continuation |
| D09 | Gap-up fade | Positive gap followed by reversal |
| D10 | Gap-down continuation | Negative opening gap followed by continuation |
| D11 | Gap-down recovery | Negative gap followed by recovery |
| D12 | Event day | Scheduled or unscheduled event with pre/post-event phases |
| D13 | Liquidity-stressed | Low visible depth, higher slippage and unstable spreads |
| D14 | Expiry-like | High derivatives-linked activity, bursts and closing effects |
| D15 | Rotation day | Index muted while sectors diverge |
| D16 | Index-dominated day | Strong common market factor across most tickers |
| D17 | Stock-specific dispersion | Weak index move but large idiosyncratic moves |
| D18 | False-breakout day | Repeated breakouts that reverse quickly |
| D19 | Trend reversal day | Morning direction reverses in the afternoon |
| D20 | Shock-and-normalize | Sudden jump/crash followed by liquidity recovery |

## 8. Intraday state regimes

A daily regime is composed of intraday states:

| Code | Intraday state |
|---|---|
| I01 | Pre-open/opening discovery |
| I02 | Opening momentum |
| I03 | Opening reversal |
| I04 | Normal continuous trading |
| I05 | Midday liquidity lull |
| I06 | Momentum burst |
| I07 | Volatility burst |
| I08 | Liquidity withdrawal |
| I09 | Absorption |
| I10 | Exhaustion |
| I11 | Range compression |
| I12 | Breakout |
| I13 | False breakout |
| I14 | News shock |
| I15 | Post-shock recovery |
| I16 | Closing positioning |
| I17 | Closing imbalance/trend |
| I18 | Feed degradation/reconnect episode |

Use semi-Markov durations so states persist for realistic, variable periods.

## 9. Ticker-specific states

Each ticker can differ from the market state:

- market follower;
- high-beta follower;
- defensive/low-beta;
- sector-led;
- idiosyncratic positive event;
- idiosyncratic negative event;
- illiquid/stale;
- abnormal volume;
- spread stress;
- temporary dislocation;
- leader;
- laggard;
- mean-reverting outlier.

**Current implementation status as of 2026-07-13:** Phase 3 has an initial runnable implementation in `scripts/run_phase3_regime_taxonomy.py`, backed by `src/synthetic_l2/phase3_regime_taxonomy.py`.

Generated artifacts are under `outputs/phase3/`:

- `phase3_regime_taxonomy_report.md`;
- `daily_regime_observation.csv`;
- `intraday_market_states.csv`;
- `ticker_state_profile.csv`;
- `symbol_intraday_features.csv`;
- `regime_manifest.json`.

The first completed run used 5-minute bins across all 32 symbols, producing 2,459 symbol-bin rows and 77 intraday market bins. The daily label is `D04` / gradual bullish trend as a one-day candidate, based on positive median cross-symbol drift. Intraday labels are dominated by `I04` / normal continuous trading, with 2 opening-discovery bins and 2 feed/reconnect-gap bins. Ticker-specific labels are one-day candidates only and currently include illiquid/stale, market follower, high-beta follower, spread stress and laggard states.

Important Phase 3 caveat: these regime labels are engineering inputs for synthetic scenario design and are not promotable regime statistics until Stage A2 multi-day capture and holdout validation exist.

---

## Phase 4 — Three-Month Synthetic Scenario Calendar

Assume approximately 63 trading days.

### 10.1 Suggested initial composition

| Regime family | Days | Approximate share |
|---|---:|---:|
| Normal balanced | 12 | 19% |
| Low-volatility sideways | 7 | 11% |
| High-volatility sideways | 5 | 8% |
| Gradual bullish trend | 6 | 10% |
| Strong rally | 3 | 5% |
| Gradual bearish trend | 5 | 8% |
| Sell-off/panic | 3 | 5% |
| Gap scenarios | 6 | 10% |
| Event days | 5 | 8% |
| Rotation/dispersion | 4 | 6% |
| False-breakout days | 3 | 5% |
| Trend reversal days | 2 | 3% |
| Liquidity-stressed days | 1 | 2% |
| Shock-and-normalize | 1 | 2% |

This is intentionally more stressful and diverse than a typical random quarter.

### 10.2 Seed sets

Generate at least three independent synthetic quarters:

- **Q-A: typical mix**
- **Q-B: bullish/high-momentum**
- **Q-C: stressed/volatile**

A strategy should not be accepted based on one random seed or one quarter.

### 10.3 Full-year extension

The later 252-day synthetic year should include:

- four broad volatility phases;
- bull, bear and range-bound blocks;
- multiple transitions;
- at least 15 market-wide shocks;
- at least 2–4 ticker-specific shocks per ticker;
- several low-liquidity weeks;
- expiry-like sessions;
- event clusters;
- correlation spikes;
- volatility clustering;
- regime persistence;
- structural-break simulations.

**Current implementation status as of 2026-07-13:** Phase 4 has an initial runnable implementation in `scripts/run_phase4_scenario_calendar.py`, backed by `src/synthetic_l2/phase4_scenario_calendar.py`.

Generated artifacts are under `outputs/phase4/`:

- `phase4_scenario_calendar_report.md`;
- `scenario_calendar.csv`;
- `scenario_calendar.jsonl`;
- `regime_mix_summary.csv`;
- `profile_summary.csv`;
- `scenario_manifest.json`.

The first completed run generated three deterministic 63-day synthetic-quarter profiles: `Q-A` typical mix, `Q-B` bullish/high-momentum and `Q-C` stressed/volatile. The combined scenario calendar has 189 rows, 63 days per profile and 18 regime codes per profile. It carries regime codes, intraday-template labels, volatility/event/spread/depth/correlation multipliers, gap-day flags, market-shock flags, event-cluster flags and shock-symbol sets.

Important Phase 4 caveat: this phase designs scenario coverage only. It does not yet generate prices, order-book states, feed effects or strategy results.

---

## Phase 5 — Price Process

### 11.1 Hierarchical return model

For ticker \(i\):

\[
r_{i,t}
=
\beta_{i,t} r_{m,t}
+
\gamma_{i,t} r_{sector(i),t}
+
\epsilon_{i,t}
+
J_{i,t}
\]

Where:

- \(r_{m,t}\): market latent return;
- \(r_{sector,t}\): sector latent return;
- \(\epsilon_{i,t}\): ticker-specific component;
- \(J_{i,t}\): jump/shock component;
- betas vary by regime.

### 11.2 Stochastic volatility

Volatility should:

- vary through the day;
- cluster through time;
- increase after shocks;
- decay gradually;
- correlate across tickers during market stress;
- affect spread, depth and event intensity.

Possible baseline:

- regime-switching GARCH-like variance; or
- log-volatility AR process with jumps.

### 11.3 Price-grid enforcement

Every generated tradable price must:

- respect the instrument tick size;
- preserve positive prices;
- maintain ordered bid/ask levels;
- avoid crossed books except optional transient data-error scenarios;
- use realistic daily price limits where applicable.

---

**Current implementation status as of 2026-07-13:** Phase 5 has an initial runnable implementation in `scripts/run_phase5_price_process.py`, backed by `src/synthetic_l2/phase5_price_process.py`.

Generated artifacts are under `outputs/phase5/`:

- `phase5_price_process_report.md`;
- `price_paths_5m.parquet`;
- `daily_price_summary.csv`;
- `price_process_manifest.json`.

The first completed run generated deterministic 5-minute OHLC synthetic price paths for all Phase 4 profiles. It produced 453,600 bar rows across 189 scenario days, 32 symbols and 75 bars per symbol-day, plus 6,048 daily symbol summaries. The generator uses Phase 2 reference prices, observed tick-size estimates, volatility proxies, sector groupings, Phase 4 regime multipliers, gap flags, market-shock flags and shock-symbol sets. Validation confirmed positive prices, no OHLC high/low violations and tick-grid error only at floating-point tolerance.

Important Phase 5 caveat: this is a price-path layer only. It does not yet generate executable L2 events, five-level market depth, retail feed batching, latency, fills or strategy PnL.

## Phase 6 — Limit Order Book Generator

## 12. Recommended baseline L2 engine

Use an event-driven top-five market-by-price book simulator.

Possible event types:

1. bid limit addition;
2. bid cancellation;
3. sell market/aggressive order consuming bids;
4. ask limit addition;
5. ask cancellation;
6. buy market/aggressive order consuming asks;
7. best-price improvement;
8. level depletion and price shift;
9. multi-level sweep;
10. replenishment;
11. spread widening;
12. spread compression.

Event probabilities depend on:

- current regime;
- ticker;
- time of day;
- spread;
- imbalance;
- recent OFI;
- recent trades;
- local volatility;
- shock state;
- market and sector state.

### 12.1 Event intensity

Use a regime-conditioned point process.

Baseline:

\[
\lambda_{event}(t)
=
\lambda_{ticker}
\times TOD(t)
\times RegimeMultiplier
\times VolatilityMultiplier
\times ShockMultiplier
\]

A self-exciting component can create clustered activity:

\[
\lambda_t = \mu_t + \sum_j \alpha_j e^{-\beta(t-t_j)}
\]

Implement this only after a simpler conditional renewal model works.

### 12.2 Depth quantities

Model depth quantities with:

- positive heavy-tailed distributions;
- ticker-specific scaling;
- level-specific scaling;
- time-of-day scaling;
- volatility/liquidity adjustment;
- cross-level dependence;
- bid/ask dependence;
- occasional large displayed walls;
- realistic order-count relationship.

Avoid independent random quantities at each level.

### 12.3 Book shape

Generate and validate:

- average depth increasing with distance;
- temporary concave or convex shapes;
- side asymmetry;
- thinning ahead of large moves;
- rebuilding after moves;
- shape instability during shocks.

### 12.4 Resilience

After aggressive depth consumption:

- some books replenish quickly;
- some continue moving;
- some spread temporarily;
- recovery speed depends on regime and ticker liquidity.

This is essential for testing liquidity-vacuum, absorption and mean-reversion strategies.

**Current implementation status as of 2026-07-13:** Phase 6 has an initial runnable implementation in `scripts/run_phase6_l2_book_generator.py`, backed by `src/synthetic_l2/phase6_l2_book_generator.py`.

Generated artifacts are under `outputs/phase6/`:

- `phase6_l2_book_report.md`;
- `l2_book_states_5m.parquet`;
- `l2_book_summary.csv`;
- `l2_book_manifest.json`.

The first completed run generated one synthetic top-five market-by-price L2 book state for every Phase 5 price bar: 453,600 rows across 189 scenario days, 32 symbols and 3 profiles. Each row contains L1-L5 bid/ask prices, quantities and order counts, spread ticks, event-intensity proxy and a coarse book-event label. Validation confirmed 0 crossed/locked L1 rows, 0 bid/ask depth-sort errors, 0 nonpositive quantity/order rows and 0 tick-grid error rows.

Important Phase 6 caveat: this is a compact market-by-price state generator, not a full individual-order event simulator. Queue identity, deterministic passive fill priority and true add/cancel/consume causality remain future work.

---

## Phase 7 — Synthetic Event and Shock Library

## 13. Market-wide shocks

| Shock | Required L2 effects |
|---|---|
| Sudden positive macro surprise | correlated price jump, ask depletion, buy trade burst, spread widening then normalization |
| Sudden negative macro surprise | correlated fall, bid withdrawal, sell sweep, high trade intensity |
| RBI-like scheduled decision | low/normal activity before event, abrupt two-sided volatility, then directional or reverting phase |
| Budget-like event | repeated shocks, sector dispersion, prolonged elevated activity |
| Global overnight gap | opening gap, price discovery, elevated spreads and volume |
| Index rebalancing-like flow | concentrated activity near close, selected ticker divergence |
| Broad risk-off episode | correlation spike, declining depth, widening spreads |
| Relief rally | rapid positive reversal following stress |

## 14. Ticker-specific shocks

- earnings beat;
- earnings miss;
- guidance change;
- regulatory action;
- block/bulk-like volume burst;
- promoter/news headline;
- sudden rumor and reversal;
- trading halt-like gap in updates;
- stock-specific liquidity disappearance;
- sharp move followed by absorption;
- false breakout caused by temporary depth withdrawal.

### 14.1 Shock parameterization

Each shock should specify:

```yaml
shock_id:
scope: market | sector | ticker
start_time:
duration:
price_jump_bps:
drift_after_jump:
volatility_multiplier:
event_rate_multiplier:
spread_multiplier:
depth_multiplier_bid:
depth_multiplier_ask:
buy_sell_flow_bias:
correlation_multiplier:
recovery_half_life:
reversal_probability:
```

### 14.2 Counterfactual pairs

Generate paired scenarios using the same random seed:

- no shock;
- positive shock;
- negative shock;
- shock with quick recovery;
- shock with continuation.

This allows causal-style stress comparison of strategy behaviour.

**Current implementation status as of 2026-07-13:** Phase 7 has an initial runnable implementation in `scripts/run_phase7_shock_library.py`, backed by `src/synthetic_l2/phase7_shock_library.py`.

Generated artifacts are under `outputs/phase7/`:

- `phase7_shock_library_report.md`;
- `shock_library.csv`;
- `shock_library.jsonl`;
- `shock_type_summary.csv`;
- `shock_day_summary.csv`;
- `shock_library_manifest.json`.

The first completed run generated 1,504 synthetic shock/event rows: 200 market-scope events and 1,304 ticker-scope events. It covers 56 scenario days, all 32 ticker targets, 366 counterfactual groups and five variants: no shock, positive shock, negative shock, quick recovery and continuation. Each event carries scope, target, start time, duration, price jump, drift-after-jump, volatility/event/spread/depth/correlation multipliers, buy/sell flow bias, recovery half-life, reversal probability and required L2 effects.

Important Phase 7 caveat: this phase defines the shock/event schedule and required effects. It does not yet mutate Phase 6 book states or simulate retail feed delivery.

---

## Phase 8 — Simulate Zerodha Retail Feed Characteristics

The output should resemble what a retail client receives, not an ideal exchange feed.

### 15.1 Feed effects

Support configurable:

- local receive latency;
- latency jitter;
- batched updates;
- missed packets;
- duplicate packets;
- out-of-order receive timestamps;
- brief disconnects;
- reconnect snapshots;
- stale periods;
- timestamp granularity limitations;
- per-ticker asynchronous arrival.

### 15.2 Latency profiles

| Profile | Median | Tail behaviour |
|---|---:|---|
| Ideal research | 0 ms | no jitter |
| Good retail | 50–100 ms | moderate tail |
| Normal retail | 150–300 ms | occasional 500–1000 ms |
| Stressed retail | 300–700 ms | long tail and bursts |
| Disconnect scenario | N/A | 2–30 second gaps |

Do not claim these are measured Zerodha production latencies. They are test profiles and must later be calibrated from order and receive logs.

**Current implementation status as of 2026-07-13:** Phase 8 has an initial runnable implementation in `scripts/run_phase8_retail_feed_emulator.py`, backed by `src/synthetic_l2/phase8_retail_feed_emulator.py`.

Generated artifacts are under `outputs/phase8/`:

- `phase8_retail_feed_report.md`;
- `retail_feed_observations.parquet`;
- `retail_feed_dropped_events.csv`;
- `feed_profile_summary.csv`;
- `retail_feed_manifest.json`.

The first completed run emitted five test feed profiles over the Phase 6 synthetic L2 book-state stream: `ideal_research`, `good_retail`, `normal_retail`, `stressed_retail` and `disconnect_scenario`. Across all profiles it produced 2,259,039 received-feed observation rows, 15,600 dropped source events and 6,639 duplicate observations. The profile summary records drop fractions, duplicate fractions, median/p95/p99 latency, disconnect-gap rows, out-of-order injection rows and symbol coverage.

Important Phase 8 caveat: latency, batching, drop, duplicate, disconnect and out-of-order behaviours are synthetic test profiles. They are not measured Zerodha production latency distributions and must be recalibrated if live receive/order diagnostics become available.

---

## Phase 9 — Data Products

Generate three tiers.

## 16. Tier A: Raw synthetic event stream

Purpose:

- auditability;
- reconstruction;
- event-based research;
- future feature engineering.

Contains every generated event/book update.

## 17. Tier B: Compact L2 state stream

Store only state-changing snapshots:

- timestamp;
- ticker;
- trade fields when changed;
- L1-L5 bid/ask state;
- event type;
- regime IDs.

This will be the main backtest source.

## 18. Tier C: Resampled feature datasets

At 100 ms, 250 ms, 500 ms, 1 s, 5 s, 15 s, only where the symbol/window coverage gate supports that horizon:

- mid-price returns;
- spread;
- static imbalance;
- MLOFI;
- trade imbalance;
- microprice;
- liquidity withdrawal;
- replenishment;
- volatility;
- momentum;
- book shape;
- regime labels;
- future-return labels.

Tier C is for fast model iteration and should be reproducible from Tier A/B.

**Current implementation status as of 2026-07-14:** Phase 9 has an initial runnable implementation in `scripts/run_phase9_data_products.py`, backed by `src/synthetic_l2/phase9_data_products.py`.

Generated artifacts are under `outputs/phase9/`:

- `phase9_data_products_report.md`;
- `data_product_manifest.json`;
- `tier_a/raw_synthetic_events.parquet`;
- `tier_b/compact_l2_state.parquet`;
- `tier_c/features_5m.parquet`;
- `tier_d/resampled_features_15m.parquet`;
- `tier_d/resampled_panel_summary.csv`.

The current completed run produced 2,276,143 Tier A synthetic event rows, 2,259,039 Tier B compact L2 rows, 2,259,039 Tier C 5-minute feature rows and 756,000 Tier D 15-minute resampled feature-panel rows across 5 feed profiles and all 32 symbols. Tier B had 0 crossed L1 rows. Tier D is a deterministic resampled product derived from Tier C, with 21,633 incomplete panels retained and labeled by `panel_complete`; any 1-second product must still be gated by symbol/window coverage and staleness labels rather than assumed as a dense full-session panel.

The horizon-readiness gate in `outputs/horizon_readiness/` converts the Stage A1 coverage measurements into explicit horizon decisions. It confirms that the current one-day Zerodha retail WebSocket sample supports event-driven 1-second work for 12 of 32 active symbols during the 09:15-09:20 IST open window, but supports 0 of 32 symbols as a dense 1-second regular panel in that window. Full-session dense regular-panel support is 0/32 at 1 second, 30/32 at 5 seconds and 32/32 at 15 seconds and 60 seconds. Sub-second 100 ms, 250 ms and 500 ms views remain sparse and must not be used as dense panels.

---

## Phase 10 — Storage and Size Optimization

## 19. Do not store expanded JSON

Avoid JSON for large-scale tick data because repeated field names and nested structures greatly inflate size.

Use Parquet with:

- Zstandard compression;
- dictionary encoding for symbol/exchange/regime/event type;
- delta encoding for timestamps where supported;
- appropriate integer widths;
- fixed-point integer prices;
- partition pruning.

## 20. Recommended physical types

| Logical field | Suggested type |
|---|---|
| Timestamp | int64 epoch microseconds/nanoseconds |
| Instrument token | int32/int64 |
| Symbol | dictionary-encoded string |
| Price | int32/int64 integer ticks or paise |
| Quantity | int32/int64 |
| Order count | int16/int32 |
| Regime/event code | int8/int16 |
| Boolean flags | bool/bit-packed |
| Sequence | int64 |
| Returns/features | float32 for derived data, float64 where precision is essential |

### 20.1 Price representation

Prefer:

```text
price_ticks = round(price / tick_size)
```

or integer paise where valid.

This improves compression and prevents floating-point tick-grid errors.

## 21. Partitioning

Recommended:

```text
dataset/
  layer=raw_events/
    trading_date=YYYY-MM-DD/
      symbol=ABC/
        part-*.parquet

  layer=l2_state/
    trading_date=YYYY-MM-DD/
      symbol=ABC/
        part-*.parquet

  layer=features_1s/
    trading_month=YYYY-MM/
      symbol=ABC/
        part-*.parquet
```

Avoid excessive tiny files. Aim for approximately 128–512 MB Parquet files where practical.

**Current storage/query decision as of 2026-07-13:** keep Parquet/Zstandard as the durable storage format and use DuckDB as the local analytic query layer over Parquet/CSV views. Do not load high-volume tick or depth data into SQLite. SQLite may be introduced later only for a small transactional run registry, manual annotations or experiment metadata.

DuckDB is installed in the current Python environment and an initial workspace builder exists in `scripts/build_duckdb_workspace.py`, backed by `src/synthetic_l2/duckdb_workspace.py`.

Generated artifacts are under `outputs/duckdb/`:

- `synthetic_l2.duckdb`;
- `duckdb_workspace_report.md`;
- `duckdb_workspace_manifest.json`.

The current DuckDB validation registers views over Stage A1 through Phase 20 outputs. SQL validation confirms 620,853 compact tick rows, 620,853 normalized rows, 620,853 received-delta rows, 32 Phase 1 event-reconstruction symbols, 4 Phase 1 event-reconstruction quality rows, 144,489 classified trade-side rows, 344,771 replenishment proxy rows, 360,142 queue-event proxy rows, 32 Stage A1 symbols, 32 Phase 2 symbols, 77 Phase 3 intraday bins, 189 Phase 4 scenario-calendar rows, 453,600 Phase 5 price-bar rows, 6,048 Phase 5 daily symbol rows, 453,600 Phase 6 L2 book rows, 0 Phase 6 crossed L1 rows, 1,504 Phase 7 shock events, 32 Phase 7 ticker targets, 2,259,039 Phase 8 feed observation rows, 15,600 Phase 8 dropped source events, 6,639 Phase 8 duplicate observations, 2,276,143 Phase 9 Tier A events, 2,259,039 Phase 9 Tier B rows, 2,259,039 Phase 9 Tier C rows, 756,000 Phase 9 Tier D 15-minute resampled rows, 8 Phase 10 inventory datasets, 5 Phase 10 generation profiles, 5 Phase 10 feature intervals, 11 Phase 11 strategy rows, 81 Phase 12 full-run lifecycle risk rows, 4,932 Phase 12 full-run lifecycle daily risk rows, 81 Phase 12 full-run lifecycle breach-severity rows, 0 Phase 12 proxy risk-pass candidate rows, 68 Phase 12 high-severity proxy risk rows, 324 Phase 12 risk-limit sensitivity rows, 4 Phase 12 risk-limit sensitivity profiles, 14 Phase 12 proxy pass rows under sensitivity profiles, 267 Phase 12 high-severity risk-limit rows, 88 Phase 12 risk acceptance-readiness rows, 88 open Phase 12 risk acceptance-readiness rows, 54 Phase 12 risk-readiness rows with proxy evidence, 0 met Phase 12 risk acceptance requirements, 11 Phase 13 robustness-dimension rows, 88 Phase 13 robustness acceptance-gap rows, 79 open Phase 13 robustness acceptance-gap rows, 9 met Phase 13 robustness proxy requirements, 88 Phase 14 realism acceptance-gap rows, 88 open Phase 14 realism acceptance-gap rows, 38 Phase 14 realism-gap rows with proxy evidence, 0 met Phase 14 realism acceptance requirements, 407 Phase 16 predictive holdout-stability cell rows, 11 Phase 16 predictive holdout-stability summary rows, 11 Phase 16 predictive promotion-falsification rows, 0 Phase 16 predictive proxy promotion candidates, 11 Phase 16 predictive promotion-falsified rows, 99 Phase 16 predictive acceptance-gap rows, 99 open Phase 16 predictive acceptance-gap rows, 58 Phase 16 predictive acceptance-gap rows with proxy evidence, 0 met Phase 16 predictive acceptance requirements, 27 Phase 16 economic-viability frontier rows, 81 Phase 16 risk-adjusted economic frontier rows, 0 Phase 16 risk-adjusted joint-pass rows, 12 Phase 16 economic-positive but risk-blocked rows, 13 Phase 16 broker-reconciliation readiness rows, 10 Phase 16 proxy/formula-ready reconciliation rows, 0 Phase 16 contract-note-ready reconciliation rows, 11 Phase 16 economic-reconciliation strategy rows, 0 Phase 16 economically reconciliation-ready strategies, 88 Phase 16 economic acceptance-gap rows, 88 open Phase 16 economic acceptance-gap rows, 58 Phase 16 economic acceptance-gap rows with proxy evidence, 0 met Phase 16 economic acceptance requirements, 50 Phase 20 acceptance-hardening queue rows, 5 Phase 20 gate-summary rows, 11 Phase 20 strategy-summary rows, 88 Phase 20 risk-hardening plan rows, 54 Phase 20 risk-hardening rows with proxy evidence, 34 Phase 20 risk-hardening rows missing required evidence, 6 Phase 20 risk-hardening action classes, 88 Phase 20 economic-hardening plan rows, 58 Phase 20 economic-hardening rows with proxy evidence, 30 Phase 20 economic-hardening rows missing required evidence, 8 Phase 20 economic-hardening action/dependency rows and 0 promoted Phase 15 strategies.

**Current implementation status as of 2026-07-13:** Phase 10 has an initial runnable storage optimizer in `scripts/run_phase10_storage_optimizer.py`, backed by `src/synthetic_l2/phase10_storage_optimizer.py`. The older `scripts/run_phase10_storage_size_estimator.py` entrypoint remains as a compatibility wrapper.

Generated artifacts are under `outputs/phase10/`:

- `phase10_storage_report.md`;
- `storage_manifest.json`;
- `storage_inventory.csv`;
- `schema_physical_types.csv`;
- `size_estimates.csv`;
- `partition_recommendations.csv`;
- `phase10_storage_size_report.md`;
- `storage_size_manifest.json`;
- `measured_storage_footprint.csv`;
- `real_sample_symbol_storage.csv`;
- `regime_storage_multipliers.csv`;
- `generation_profile_size_estimates.csv`;
- `feature_interval_size_estimates.csv`.

The consolidated storage run measured current product sizes across Stage A1 and Phase 5-9 artifacts. Current Parquet footprints include 39.71 MB for Stage A1 compact real ticks, 158.26 MB for Phase 9 Tier B compact L2 state, 122.93 MB for Phase 9 Tier C 5-minute features and 55.23 MB for Phase 9 Tier D 15-minute resampled features. Using the current one-day received-tick row rate and current synthetic product bytes-per-row, including the Tier D resampled product, the consolidated optimizer projects approximately 29.73 GB for the Medium profile, 118.93 GB for the Full annual profile, 37.16 GB for the Dense profile and 28.44 GB for Feature-only. The earlier storage-size estimate artifacts are retained for comparison. Three-month fine-horizon feature products remain subject to the symbol/window coverage gates.

Important Phase 10 caveat: these are capacity-planning estimates from a one-day real sample and the current Phase 9 products. They are not guarantees for multi-day production capture, and the raw source-file footprint is inflated by many tiny files. Compact Parquet should remain the planning basis.

## 22. Delta-state option

For maximum compression, store:

- full snapshot at session start;
- then only changed fields;
- periodic full checkpoint every 30–300 seconds;
- full checkpoint after reconnect.

Advantages:

- smaller files;
- preserves event semantics.

Disadvantages:

- more complex replay;
- corruption can affect subsequent reconstruction.

Maintain both delta data and periodic checkpoints.

## 23. Adaptive event-rate generation

Do not generate an arbitrary constant rate.

Use:

- lower rates for quiet tickers and midday;
- higher rates near open/close;
- bursts around shocks;
- event rate proportional to calibrated liquidity/activity;
- configurable maximum rate.

This both improves realism and avoids unnecessary storage.

## 24. Data-size estimation stage

After receiving the sample files, calculate:

```text
bytes_per_real_event
events_per_ticker_day
compressed_bytes_per_ticker_day
expected_multiplier_by_regime
expected_three_month_size
expected_one_year_size
feature_dataset sizes by interval
```

Produce conservative, expected and aggressive estimates.

### 24.1 Generation profiles

| Profile | Purpose | Approximate event retention |
|---|---|---|
| Small | unit/integration tests | 1–5 tickers, 5–10 days |
| Medium | initial strategy screening | 32 instruments, 63 days, controlled event rates |
| Full | annual stress study | 32 instruments, 252 days |
| Dense | microstructure stress | selected 5–10 tickers at high event rate |
| Feature-only | rapid ML experiments | resampled feature tables, no raw replay |

---

## Phase 11 — Strategy Validation Matrix

This phase defines the eventual experiments. The current tick-wise day supports feature engineering, pipeline tests and within-day falsification, but not robust strategy acceptance. S01–S11 promotion decisions require multiple real days plus multi-seed synthetic controls; any result based primarily on this one day must be labelled preliminary and day-specific.

**Current implementation status as of 2026-07-14:** Phase 11 has an initial runnable strategy validation matrix and signal-diagnostics implementation in `scripts/run_phase11_strategy_validation_matrix.py`, backed by `src/synthetic_l2/phase11_strategy_validation_matrix.py`, plus an S01-S11 module registry in `scripts/run_phase11_strategy_modules.py`, backed by `src/synthetic_l2/phase11_strategy_modules.py`.

Generated artifacts are under `outputs/phase11/`:

- `phase11_strategy_validation_report.md`;
- `strategy_validation_manifest.json`;
- `strategy_validation_matrix.csv`;
- `baseline_strategy_matrix.csv`;
- `strategy_feature_availability.csv`;
- `strategy_signal_diagnostics.csv`;
- `strategy_module_registry.csv`;
- `strategy_module_coverage.csv`;
- `strategy_module_registry_report.md`;
- `strategy_module_registry_manifest.json`.

The first completed run emitted 11 strategy rows covering S01â€“S11, 77 baseline-requirement rows, 65 scenario-requirement rows and 59 metric-requirement rows. All strategies are explicitly marked `promotion_allowed_now = false` with the evidence label `engineering_and_within_day_falsification_only`.

Important Phase 11 caveat: this is an experiment-control matrix, not a backtest. It defines what must be tested and which baselines/scenarios/metrics are required before any promotion decision.

Current Phase 11 superseding note: the current runnable output also includes signal diagnostics against the 2,259,039-row Phase 9 Tier C 5-minute feature product. Current support levels are 5 `runnable_proxy` strategies, 4 `partial_missing_required_features` strategies and 2 `not_supported_by_current_product` strategies. The module registry now gives all S01-S11 explicit implementation rows: 11 implemented-proxy modules, 0 acceptance-grade modules, 0 promotion-ready modules and 2 non-alpha/risk modules for S10/S11. S10 is represented as a passive-market-making execution/risk module backed by Phase 12 event-backtest proxy evidence; S11 is represented as a risk-filter specification and must not be interpreted as spoof/manipulation detection. These diagnostics and module rows remain preliminary and are not strategy acceptance.

## 25. Priority strategies

| ID | Strategy | Initial priority |
|---|---|---:|
| S01 | Momentum/breakout filtered by MLOFI | 1 |
| S02 | Pure multi-level OFI directional model | 2 |
| S03 | Liquidity-vacuum breakout | 3 |
| S04 | Trade-flow plus depth confirmation | 4 |
| S05 | Microprice entry/exit filter | 5 |
| S06 | Absorption and exhaustion reversal | 6 |
| S07 | Short-term mean reversion after imbalance | 7 |
| S08 | Cross-ticker/index lead-lag OFI | 8 |
| S09 | Pure queue-imbalance scalping | 9, benchmark only |
| S10 | Passive market making | 10, research only |
| S11 | Suspicious wall/spoof-like pattern filter | 11, risk filter only |

---

## 26. Common baseline strategies

Every L2 strategy must be compared against a price-only baseline.

Baselines:

- random direction with matched trade frequency;
- buy-and-hold intraday control;
- simple short-term momentum;
- opening-range breakout;
- VWAP continuation;
- short-term mean reversion;
- volatility breakout.

The key test is whether L2 improves performance over these baselines.

---

## 27. S01 — Momentum/Breakout + MLOFI

### Hypothesis

Price breakouts confirmed by persistent five-level OFI have:

- higher continuation probability;
- fewer false breakouts;
- better excursion;
- improved net expectancy.

### Variables

- breakout horizon: 1, 3, 5, 10 minutes;
- OFI lookback: 1, 5, 15, 30 seconds;
- percentile threshold;
- trade-flow confirmation;
- spread filter;
- liquidity-withdrawal filter;
- market/sector alignment;
- time-of-day regime.

### Required scenario coverage

- gradual trend;
- strong rally;
- sell-off;
- false-breakout day;
- sideways day;
- shock continuation;
- shock reversal.

### Primary metrics

- false-breakout reduction;
- net expectancy;
- maximum adverse excursion;
- maximum favourable excursion;
- cost sensitivity;
- latency tolerance;
- regime stability.

---

## 28. S02 — Pure Multi-Level OFI

### Hypothesis

MLOFI predicts future mid-price movement beyond static imbalance.

### Compare

1. L1 static imbalance;
2. five-level static imbalance;
3. L1 OFI;
4. five-level OFI;
5. five-level OFI plus trade imbalance;
6. nonlinear model using all levels.

### Forecast horizons

- next quote move;
- 1 second;
- 5 seconds;
- 15 seconds;
- 30 seconds;
- 1 minute;
- 3 minutes;
- 5 minutes.

### Metrics

- information coefficient;
- directional accuracy;
- calibration;
- return by signal decile;
- net edge after crossing spread;
- incremental value of levels 2–5;
- feature stability across regimes.

---

## 29. S03 — Liquidity-Vacuum Breakout

### Hypothesis

Rapid one-sided depth withdrawal plus aggressive flow precedes a tradable short-horizon move.

### Test variants

- withdrawal alone;
- withdrawal plus trade confirmation;
- withdrawal plus price breakout;
- withdrawal plus spread constraint;
- withdrawal plus market alignment.

### Synthetic scenarios required

- genuine continuation;
- fake withdrawal then replenishment;
- spread blowout;
- market-wide shock;
- isolated ticker vacuum;
- rapid recovery;
- multi-level sweep.

### Failure criteria

Reject if profitability depends mainly on:

- zero latency;
- no slippage;
- one shock template;
- one ticker;
- the first few seconds after an artificial event.

---

## 30. S04 — Trade-Flow + Depth Confirmation

### Hypothesis

Trade imbalance and depth flow jointly classify:

- continuation;
- absorption;
- exhaustion;
- false breakout.

### State matrix

| MLOFI | Trade imbalance | Candidate interpretation |
|---|---|---|
| Positive | Positive | bullish continuation |
| Positive | Negative | bid-side absorption |
| Negative | Positive | offer-side absorption/exhaustion |
| Negative | Negative | bearish continuation |

Validate each interpretation separately by regime.

---

## 31. S05 — Microprice Filter

### Hypothesis

Microprice improves entry timing, exit timing and next-tick direction estimates.

Use as:

- entry acceptance filter;
- exit trigger;
- limit-vs-market execution selector;
- adverse-selection filter.

Metrics:

- entry slippage;
- post-entry adverse movement;
- next-price-move Brier score;
- trade reduction;
- net performance uplift over the parent strategy.

Do not prioritize microprice as a standalone annual-return strategy.

---

## 32. S06 — Absorption and Exhaustion

### Hypothesis

Large aggressive flow with limited price progress, followed by flow reversal, predicts a short-term reversal.

Synthetic variants must include:

- true absorption;
- temporary pause before continuation;
- hidden-liquidity-like replenishment;
- multiple independent passive participants;
- post-shock stabilization;
- deceptive replenishment.

Because top-five retail depth cannot identify individual orders, label this as **absorption-like behaviour**, not proof of iceberg activity.

---

## 33. S07 — Mean Reversion after Imbalance

### Hypothesis

Extreme temporary imbalance followed by replenishment and declining trade intensity predicts reversion.

Regime gate:

- allow in sideways, high-volatility sideways and post-shock recovery;
- suppress in sustained trend, panic and rally states.

Compare regime-aware versus regime-unaware performance.

---

## 34. S08 — Cross-Ticker/Market Lead-Lag OFI

### Hypothesis

Market, sector or leader-ticker OFI improves prediction of follower tickers.

Possible hierarchy:

```text
market latent factor
  → sector factor
    → leader ticker
      → follower ticker
```

Synthetic test sets must include:

- true causal lead-lag;
- simultaneous common shock;
- timestamp skew;
- spurious correlation;
- changing leader;
- no lead-lag.

A strategy that profits only when the simulator explicitly embeds lead-lag is not sufficient. It must also avoid false detection in simultaneous-shock controls.

---

## 35. S09 — Queue-Imbalance Scalping

Use as a benchmark.

Test whether:

- next quote direction is predictable;
- prediction survives 50, 100, 250, 500 ms latency;
- expected move exceeds spread and costs.

Do not advance merely because classification accuracy is above 50%.

---

## 36. S10 — Passive Market Making

Synthetic testing can help develop inventory/risk logic but cannot validate real queue fills from shallow market-by-price data.

Required execution assumptions:

- pessimistic queue position;
- probabilistic partial fills;
- cancellation latency;
- adverse selection;
- fill uncertainty;
- inventory limits;
- spread capture;
- market-order liquidation cost.

Report results under:

- optimistic;
- neutral;
- pessimistic fill models.

Treat the pessimistic model as the decision model.

---

## 37. S11 — Spoof-Like Wall Filter

Use only as a risk feature:

- wall appearance;
- wall movement;
- cancellation before touch;
- repeated non-execution;
- temporary imbalance distortion.

Do not classify participants or assert market manipulation.

---

## Phase 12 — Backtest and Execution Simulator

**Current implementation status as of 2026-07-14:** Phase 12 has an initial runnable marketable-order execution simulator in `scripts/run_phase12_execution_simulator.py`, backed by `src/synthetic_l2/phase12_execution_simulator.py`, a sampled order-lifecycle and risk-control proxy in `scripts/run_phase12_order_lifecycle_risk.py`, backed by `src/synthetic_l2/phase12_order_lifecycle_risk.py`, and an event-driven order-lifecycle backtester proxy in `scripts/run_phase12_event_backtester.py`, backed by `src/synthetic_l2/phase12_event_backtester.py`.

Generated artifacts are under `outputs/phase12/`:

- `phase12_execution_simulator_report.md`;
- `execution_manifest.json`;
- `execution_summary.csv`;
- `execution_profiles.csv`;
- `cost_schedule.csv`;
- `charge_component_catalog.csv`;
- `representative_charge_scenarios.csv`;
- `full_run_risk_summary.csv`;
- `trade_ledger_sample.parquet`;
- `event_backtest_report.md`;
- `event_backtest_manifest.json`;
- `event_backtest_order_summary.csv`;
- `event_backtest_pnl_trace.csv`;
- `order_model_catalog.csv`;
- `slippage_model_catalog.csv`;
- local/generated `event_backtest_order_trace.parquet`.

Additional order-lifecycle and risk-control artifacts are under `outputs/phase12_order_lifecycle/`:

- `order_lifecycle_risk_report.md`;
- `order_lifecycle_risk_manifest.json`;
- `partial_fill_summary.csv`;
- `risk_control_summary.csv`;
- `fill_model_catalog.csv`;
- `order_lifecycle_sample.parquet`.

The current completed run processed all 2,259,039 Phase 9 Tier C 5-minute feature rows, applied Phase 11 proxy signals, and simulated 9 supported/proxy strategies across 3 execution profiles: `zero_latency_spread_only_control`, `retail_marketable_default` and `stressed_retail`. It produced 27 strategy/profile summary rows, 27 no-fill full-run risk summary rows, 81 full-run fill-adjusted lifecycle risk summary rows, 4,932 full-run lifecycle daily risk rows, 81 full-run lifecycle breach-severity rows and a 249,993-row deterministic stratified sampled trade ledger covering all 27 strategy/profile combinations. The sampled trade ledger now carries proxy `volatility_bucket` and `liquidity_bucket` fields derived from Phase 9 local volatility, event intensity and spread, plus a deterministic `seed`/`simulation_seed` lineage assigned from the Phase 13 seed plan by quarter profile and scenario day. The current sample exposes all 30 Phase 13 registered seeds, 10 per quarter profile. Across all strategy/profile combinations the run simulated 10,350,654 marketable proxy trades before fill-model expansion; the full-run lifecycle proxy evaluates 31,127,580 strategy/profile/fill-model order rows in aggregate across 3 fill models.

The simulator applies event-latency shifts, stale/disconnect cancellation, half-spread marketable execution cost, fixed slippage ticks, internal impact bps and Zerodha-sourced equity-intraday NSE rupee order-formula charges. Retail and stressed profiles now apply the rupee formula directly to each simulated round trip using `order_notional_inr=100000`, including the Rs. 20/order brokerage cap, sell-side STT with nearest-rupee rounding, NSE transaction charges, SEBI charges, buy-side stamp duty and GST. The current retail/stressed summaries show the `zerodha_equity_intraday_nse_order_formula_per_trade` basis, with average charges of roughly Rs. 82.6 per Rs. 100,000 simulated order and about 8.26 bps on entry notional. The companion `charge_component_catalog.csv` and `representative_charge_scenarios.csv` remain as an auditable charge-component and scenario ledger. This is better than a bps-only placeholder, but it is still not acceptance-grade because actual broker fills, broker contract-note reconciliation, DP/depository charges where applicable, and full tick/order lifecycle are not verified.

The sampled lifecycle/risk-control proxy currently expands the 249,993-row sampled trade ledger into 749,979 lifecycle rows across 3 deterministic fill profiles: `optimistic_marketable`, `neutral_partial` and `pessimistic_partial`. It adds queue-position bucket, partial-fill ratio, unfilled quantity, filled notional, risk-equity, drawdown, tail-loss, position-limit and daily-loss-halt fields, with 81 strategy/profile/fill-model partial-fill summary rows and 81 strategy/profile/fill-model risk-control summary rows. The main Phase 12 simulator now also emits full-run fill-adjusted lifecycle summaries over every simulated trade, not just the sampled ledger, through `outputs/phase12/full_run_lifecycle_risk_summary.csv`, `outputs/phase12/full_run_lifecycle_daily_risk_summary.csv`, `outputs/phase12/full_run_lifecycle_risk_breach_severity.csv`, `outputs/phase12/full_run_lifecycle_risk_limit_sensitivity.csv` and `outputs/phase12/full_run_risk_acceptance_readiness.csv`.

The no-fill full-run risk summary covers all simulated marketable proxy trades before deterministic trade-ledger sampling. It reports per strategy/profile total INR P&L, worst daily net P&L, 1% trade-level tail loss, max intraday drawdown, max absolute signal-position proxy and warning-day counts for daily loss, drawdown and position exposure. The full-run lifecycle risk summary applies the deterministic fill models to all simulated trades and reports fill-adjusted P&L, risk-adjusted P&L, worst daily risk-adjusted P&L, tail loss, drawdown, position exposure, daily halt rows and position-limit breach rows by strategy/profile/fill model. The breach-severity ledger derives daily-loss breach days, position-limit breach days, drawdown breach days, daily-halt days, breach-day fractions, a deterministic risk-severity score and proxy risk-pass candidate flag from those full-run lifecycle daily rows. The current breach-severity result has 81 rows: 68 high-severity proxy rows, 11 medium-severity proxy rows, 2 low-severity proxy rows and 0 proxy risk-pass candidate rows. The risk-limit sensitivity frontier evaluates those same daily lifecycle rows under 4 deterministic guardrail profiles: `tight_capital_preservation`, `current_proxy_limits`, `expanded_research_limits` and `stress_capacity_limits`. It produces 324 strategy/profile/fill/limit rows: 0 pass rows under tight limits, 0 under current proxy limits, 2 under expanded research limits and 12 under very loose stress-capacity limits, with 267 high-severity rows overall. The new risk acceptance-readiness ledger expands the risk gate into 88 strategy/requirement rows covering full-run coverage, daily equity and halt state, drawdown, position-limit, daily-loss, tail-loss, broker/exchange fill provenance and contract-note/cost reconciliation. It records 54 rows with current proxy evidence, 88 open acceptance requirements and 0 acceptance-met risk rows. This materially improves risk visibility over sample-only lifecycle evidence, but it remains a 5-minute marketable-proxy diagnostic without broker/exchange-confirmed fills. The event-driven backtester proxy samples the Phase 12 trade ledger into 6,480 order-lifecycle rows across 9 strategies, 3 execution profiles, 6 order models and 4 slippage models. It exercises market orders, marketable limits, passive-limit proxies, cancel/replace, partial fills and rejection scenarios; the summary shows 6,061 filled orders, 419 rejected/cancelled orders, 738 passive-limit orders, 4,259 market/marketable orders and 1,264 partial-fill orders.

Important Phase 12 caveat: this is an execution-plumbing, cost-sensitivity, full-run marketable-risk, full-run fill-adjusted lifecycle-risk, breach-severity, risk-limit sensitivity, risk acceptance-readiness and sampled lifecycle/fill proxy, not a tick-accurate exchange queue simulator, full-run backtest acceptance result or promotion result. Passive order-book placement, cancel/replace/rejection state machines and Zerodha order-formula charges are now exercised in proxy evidence, but true queue priority, broker/exchange fills and broker contract-note reconciliation remain requirements for acceptance.

## 38. Event-driven backtester

The backtester must process:

1. synthetic feed event;
2. strategy feature update;
3. signal decision;
4. configured decision latency;
5. order submission;
6. broker/network latency;
7. order arrival;
8. fill simulation;
9. partial fills;
10. cancellation/replacement;
11. charges;
12. P&L and risk update.

Avoid candle-only execution.

## 39. Order models

Support:

- market order;
- marketable limit order;
- passive limit order;
- stop-market approximation;
- stop-limit approximation;
- cancel/replace;
- partial fills;
- rejection scenarios;
- stale-signal cancellation.

## 40. Costs

Parameterize:

- brokerage;
- STT;
- exchange transaction charges;
- GST;
- SEBI charges;
- stamp duty;
- spread;
- impact;
- slippage;
- partial-fill opportunity cost.

Maintain cost schedules externally so they can be updated without regenerating data.

## 41. Slippage models

Use at least:

- fixed ticks;
- participation-rate impact;
- depth-consuming book walk;
- volatility/liquidity-conditioned slippage;
- stressed-shock slippage.

---

## Phase 13 — Experiment Design

Superseded Phase 13 note: an older artifact list remains below for continuity, but the authoritative current Phase 13 implementation status is recorded after the negative-control requirements.

Generated artifacts are under `outputs/phase13/`:

- `phase13_experiment_design_report.md`;
- `experiment_design_manifest.json`;
- `experiment_data_split.csv`;
- `experiment_seed_plan.csv`;
- `walk_forward_folds.csv`;
- `parameter_grid_registry.csv`;
- `negative_control_registry.csv`;
- `experiment_registry.csv`.

The first completed run created the planned 30/15/18 day split for each 63-day quarter profile, producing 189 split rows with `no_shuffle = true`. It created 30 seed-plan rows: 10 target seeds per quarter profile, with the first 3 seeds marked as initial engineering seeds. It also generated 48 walk-forward folds, 33 strategy/profile experiment-registry rows, 33 predeclared parameter-grid rows and 99 mandatory negative-control rows across S01â€“S11.

Superseded Phase 13 caveat: see the current Phase 13 implementation block below for the active artifact names and counts.

## 42. Data split

For a 63-day synthetic quarter:

| Segment | Days | Purpose |
|---|---:|---|
| Calibration/development | 30 | feature construction and rough thresholds |
| Validation | 15 | model/threshold selection |
| Untouched test | 18 | final quarter evaluation |

Do not randomly shuffle ticks.

## 43. Multi-seed validation

Minimum:

- 10 seeds per quarter profile;
- 3 quarter profiles;
- 30 independent quarter simulations.

For faster initial engineering:

- start with 3 seeds;
- scale to 10 after code stabilizes.

## 44. Walk-forward

Example:

- train 20 days;
- test next 5 days;
- roll forward 5 days;
- aggregate results.

Also test expanding and fixed rolling windows.

## 45. Parameter control

For each strategy:

- define a small, predeclared parameter grid;
- limit repeated tuning;
- track every experiment;
- retain failed runs;
- separate model selection from final evaluation;
- use nested validation for ML models.

## 46. Negative controls

Mandatory controls:

- shuffled signal within the same time-of-day bucket;
- delayed signal;
- inverted signal;
- random signal with matching turnover;
- synthetic data generated without predictive coupling;
- costs set to zero versus realistic;
- latency set to zero versus realistic;
- regime labels hidden;
- cross-ticker timestamps intentionally shifted.

These detect simulator leakage and backtest bugs.

**Current implementation status as of 2026-07-14:** Phase 13 has an initial runnable experiment-design implementation in `scripts/run_phase13_experiment_design.py`, backed by `src/synthetic_l2/phase13_experiment_design.py`, plus a deterministic experiment smoke-run ledger in `scripts/run_phase13_experiment_runner.py`, backed by `src/synthetic_l2/phase13_experiment_runner.py`.

Generated artifacts are under `outputs/phase13/`:

- `phase13_experiment_design_report.md`;
- `experiment_design_manifest.json`;
- `data_splits.csv`;
- `seed_plan.csv`;
- `walk_forward_windows.csv`;
- `parameter_grid.csv`;
- `negative_controls.csv`;
- `experiment_registry.csv`.

Additional experiment-run smoke artifacts are under `outputs/phase13/`:

- `experiment_run_smoke_report.md`;
- `experiment_run_manifest.json`;
- `experiment_run_ledger.csv`;
- `experiment_run_summary.csv`;
- `negative_control_run_summary.csv`;
- `experiment_profile_robustness_ledger.csv`;
- `experiment_profile_robustness_summary.csv`;
- `robustness_dimension_summary.csv`.

The first completed run used the Phase 4 189-row, 3-profile scenario calendar. It preserved ordered 63-day quarter splits per profile: 30 calibration/development days, 15 validation days and 18 untouched-test days. It produced 30 full-validation seed rows, 9 initial engineering seeds, 48 walk-forward windows, 63 predeclared parameter sets across S01-S09, 9 mandatory negative controls and 324 planned initial experiment-registry rows.

The current smoke run evaluated all 324 pre-registered initial experiment rows using existing Phase 11 signal diagnostics and the Phase 12 `retail_marketable_default` execution profile. It produced 324 run-ledger rows, 9 strategy-level robustness-smoke summary rows and 4 negative-control summary rows covering `BASE`, `NC01`, `NC02` and `NC03`. The current multi-profile robustness proxy additionally evaluates the same registered rows across all 3 Phase 12 execution profiles: `zero_latency_spread_only_control`, `retail_marketable_default` and `stressed_retail`. It produced 972 profile-robustness ledger rows and 9 strategy-level profile-robustness summary rows. No strategy is positive across all execution profiles, and no strategy is positive under the stressed-retail profile. The robustness-dimension summary covers all 11 S01-S11 strategy IDs: 9 strategies are registered in the current Phase 13 alpha-parameter proxy grid, each with 9 initial-engineering seed rows versus 30 required full-validation seeds, 3 execution profiles evaluated, 1 parameter set run versus the predeclared grid, 0 walk-forward windows run, and 2 holdout-generator quarter profiles present as proxy coverage. S10 and S11 are correctly marked not registered for the current alpha-parameter proxy run. The new robustness acceptance-gap ledger expands those dimensions into 88 explicit strategy/requirement rows: 9 rows meet only the proxy-grid registration requirement, while 79 rows remain open across full-validation seed coverage, execution-profile robustness, parameter-neighborhood smoothness, walk-forward coverage, holdout-generator strategy reruns, negative-control rejection and real-data reruns. All robustness rows remain `acceptance_eligible=false`.

Important Phase 13 caveat: the run ledgers close the bookkeeping gap between a planned registry and auditable proxy evidence, including execution-profile sensitivity and dimension coverage, but they are not full required-seed execution, parameter-neighborhood smoothness evidence, walk-forward result, holdout-generator strategy rerun, real-data rerun or promotion result.

---

## Phase 14 — Validation of Synthetic Data Quality

Synthetic data must be validated before strategy results are examined.

**Current implementation status as of 2026-07-14:** Phase 14 has an initial runnable synthetic-data quality validator in `scripts/run_phase14_synthetic_quality_validation.py`, backed by `src/synthetic_l2/phase14_synthetic_quality_validation.py`.

Generated artifacts are under `outputs/phase14/`:

- `phase14_quality_validation_report.md`;
- `quality_validation_manifest.json`;
- `quality_gate_summary.csv`;
- `quality_warning_triage.csv`;
- `holdout_generator_realism_summary.csv`;
- `level1_structural.csv`;
- `level2_marginal.csv`;
- `level3_temporal.csv`;
- `level4_cross_sectional.csv`;
- `level5_conditional.csv`;
- `level6_discriminator_proxy.csv`;
- `level7_counterfactual.csv`.

The current completed run validates the current synthetic products against structural, marginal, temporal, cross-sectional, conditional, strategy-neutral discriminator-proxy and counterfactual checks. It produced 24 quality-gate rows: all 24 pass, with 0 warnings and 0 failures. The earlier `nonzero_price_change_fraction` warning has been replaced by a horizon-matched comparison: Phase 14 now derives 5-minute real bars from `outputs/phase1/received_tick_deltas_by_symbol/` and compares those real-derived bars against the current Phase 9 5-minute synthetic feature product. The horizon-matched median relative/absolute error for nonzero price-change fraction is approximately 0.01095 across all 32 symbols, so the quality warning triage ledger is empty. Structural checks passed for crossed L1, negative spreads, nonpositive mid prices, expected forward-label null fraction and Phase 6 summary availability. The holdout-generator realism summary now records 15 quarter-profile/feed-profile combinations across 3 quarter profiles and 5 feed profiles; all 15 are structurally available as proxy holdout coverage, but none is acceptance-eligible until strategies are rerun on holdout configurations with full event/tick execution and later multi-day real holdout. Phase 14 now also emits `outputs/phase14/realism_acceptance_gap_ledger.csv`, which expands realism blockers into 88 strategy/requirement rows across synthetic quality, holdout-generator coverage, feed-imperfection coverage, strategy-support readiness, holdout strategy reruns, pessimistic execution realism, artifact-exploitation rejection and real multi-day realism validation. The current ledger has 38 proxy-backed rows, all 88 rows remain open and 0 rows meet acceptance-grade realism requirements.

Important Phase 14 caveat: this is a data-quality gate diagnostic, not strategy acceptance. Real evidence is still a one-day sample, and current Phase 6-9 synthetic products are 5-minute state/feature products rather than full tick-event simulation.

## 47. Level 1: Structural validity

- no invalid prices;
- no negative quantities;
- correctly sorted depth;
- spread non-negative;
- consistent cumulative volume;
- realistic timestamps;
- correct session boundaries;
- valid OHLC relationships;
- stable replay determinism.

## 48. Level 2: Marginal distributions

Compare real seed day versus synthetic normal days:

- spreads;
- event rates;
- inter-arrival times;
- trade sizes;
- depth quantities;
- order counts;
- depth by level;
- return distribution;
- volume curve;
- intraday volatility curve.

Use:

- quantile comparisons;
- KS distance;
- Wasserstein distance;
- Jensen-Shannon divergence;
- tail percentiles.

## 49. Level 3: Temporal properties

Validate:

- return autocorrelation;
- absolute-return autocorrelation;
- OFI autocorrelation;
- trade-sign autocorrelation;
- spread persistence;
- depth persistence;
- event clustering;
- volatility clustering;
- replenishment timing;
- price response decay.

## 50. Level 4: Cross-sectional properties

Validate:

- correlation distribution;
- correlation increase in stress;
- market beta distribution;
- dispersion by regime;
- sector grouping;
- simultaneous event bursts;
- cross-ticker activity dependence.

## 51. Level 5: Conditional market response

Test whether synthetic data reproduces plausible conditional relationships:

- price impact versus OFI;
- price impact versus depth;
- spread versus volatility;
- spread versus liquidity;
- event rate versus volatility;
- depth withdrawal before jumps;
- resilience after sweeps;
- continuation versus reversal conditional on flow.

## 52. Level 6: Strategy-neutral realism

Train a discriminator to distinguish real normal-day windows from synthetic normal-day windows.

Use carefully:

- a near-50% discriminator score is not sufficient by itself;
- inspect which features reveal synthetic data;
- avoid deliberately overfitting the generator to fool the discriminator.

## 53. Level 7: Counterfactual validity

When regime controls are changed, verify expected changes:

| Intervention | Expected result |
|---|---|
| Increase volatility | wider return distribution, more activity, wider spreads |
| Reduce liquidity | lower depth, more impact, more slippage |
| Positive trend | positive drift and persistent positive flow |
| Panic state | correlation spike, bid withdrawal and negative flow |
| Sideways state | low drift, repeated reversal and balanced flow |
| Shock recovery | initial jump followed by decaying volatility and restoring depth |

---

## Phase 15 — Strategy Acceptance Gates

A strategy may advance from synthetic screening only if it passes all applicable gates.

## 54. Predictive gate

- stable sign of signal-response relationship;
- improvement over baseline;
- performance across seeds;
- no dependence on one ticker;
- no dependence on one event template.

## 55. Economic gate

- positive after realistic costs;
- survives 25–50% slippage increase;
- survives retail latency;
- sufficient expected move relative to spread;
- acceptable turnover.

## 56. Robustness gate

- works in intended regimes;
- safely deactivates in hostile regimes;
- adjacent parameters behave smoothly;
- no extreme sensitivity to one threshold;
- performance not concentrated in a few days.

## 57. Risk gate

- controlled drawdown;
- bounded position size;
- manageable tail loss;
- shock-day behaviour understood;
- no uncontrolled inventory accumulation;
- daily loss limit effective.

## 58. Realism gate

- strategy does not exploit generator artifacts;
- remains viable on holdout generator configurations;
- remains viable with feed imperfections;
- remains viable under pessimistic execution.

**Current implementation status as of 2026-07-14:** Phase 15 has an initial runnable acceptance-gate evaluator in `scripts/run_phase15_acceptance_gates.py`, backed by `src/synthetic_l2/phase15_acceptance_gates.py`.

Generated artifacts are under `outputs/phase15/`:

- `phase15_acceptance_gates_report.md`;
- `acceptance_gates_manifest.json`;
- `gate_definitions.csv`;
- `strategy_gate_results.csv`;
- `strategy_acceptance_summary.csv`;
- `acceptance_blockers.csv`.

The current completed run evaluated 11 strategies across 5 gates each: predictive, economic, robustness, risk and realism. It produced 55 strategy/gate rows: 5 realism rows pass and 50 rows remain blocked. No strategy is promoted and all 11 strategies remain `blocked_not_promotable`. The blocker ledger now attaches structured blocker categories, missing requirements, next-required-evidence text and evidence-source status to all 50 blocker rows; all 50 blocker evidence sources are present. The 11 predictive blocker rows now cite `outputs/phase16/predictive_baseline_comparison.csv`, `outputs/phase16/predictive_holdout_stability_summary.csv`, `outputs/phase16/predictive_promotion_falsification.csv` and `outputs/phase16/predictive_acceptance_gap_ledger.csv`; the predictive gate remains blocked because 0 strategies beat the required proxy baseline checks, 0 strategies pass all holdout-stability cells, 0 strategies are proxy predictive-promotion candidates, all 11 strategies are falsified for predictive promotion under current proxy evidence, 5 runnable strategies fail at least some quarter/feed/segment stability cells, 6 strategies are partial or unsupported by the current product, and the predictive acceptance-gap ledger has 99 open rows, 58 proxy-backed rows and 0 acceptance-met rows across support, baseline, holdout-cell, untouched-test, feature-stability, multi-seed/walk-forward, calibrated-model, real-holdout and promotion-falsification requirements. The realism gate now passes for the 5 runnable-proxy strategies after the Phase 14 horizon-matched quality fix, but the 6 remaining realism blocker rows are for partial/unsupported strategies and now cite `outputs/phase14/realism_acceptance_gap_ledger.csv` plus `outputs/phase14/holdout_generator_realism_summary.csv` in addition to the Phase 14 quality summary and warning triage. Their blocker text covers partial/unsupported strategy support, holdout-generator rerun gaps, pessimistic-execution evidence gaps, artifact-control gaps and missing real multi-day validation; the realism acceptance-gap ledger has 88 open rows, 38 proxy-backed rows and 0 acceptance-met rows. The 11 economic blocker rows now cite `outputs/phase16/risk_adjusted_economic_frontier.csv`, `outputs/phase16/broker_reconciliation_readiness.csv`, `outputs/phase16/economic_reconciliation_strategy_summary.csv` and `outputs/phase16/economic_acceptance_gap_ledger.csv` in addition to Phase 12 execution/cost artifacts and the Phase 16 economic frontier. The economic gate remains blocked because broker contract-note reconciliation and actual fills remain missing, all stressed-profile mean net returns remain nonpositive, only 2 retail/stress rows are currently net-positive in the standalone proxy frontier, 0 rows jointly clear net-positive proxy economics and lifecycle risk-pass checks, 12 rows are economic-positive but risk-blocked in the risk-adjusted frontier, the broker-reconciliation readiness ledger has 13 rows with 10 proxy/formula-ready rows but 0 broker contract-note-ready rows, 0 of 11 strategies are economically reconciliation-ready, and the economic acceptance-gap ledger has 88 open rows, 58 proxy-backed rows and 0 acceptance-met rows across net-positive, risk-adjusted, broker-fill, contract-note, stress and holdout economic requirements. The 11 risk blocker rows now cite `outputs/phase12/full_run_lifecycle_risk_breach_severity.csv`, `outputs/phase12/full_run_lifecycle_risk_limit_sensitivity.csv` and `outputs/phase12/full_run_risk_acceptance_readiness.csv` in addition to the no-fill full-run risk, fill-adjusted lifecycle/daily risk and sampled lifecycle/risk summaries; the risk gate remains blocked because 0 lifecycle breach-severity rows are proxy risk-pass candidates, the risk-limit sensitivity frontier has 0 pass rows under tight or current proxy limits, 14 pass rows only under looser research/stress-capacity sensitivity profiles, 68 of 81 severity rows are high-severity proxy rows, 267 of 324 risk-limit sensitivity rows are high-severity proxy rows, the risk acceptance-readiness ledger has 88 open rows, 54 proxy-backed rows and 0 acceptance-met rows, and broker/exchange-confirmed fill-adjusted drawdown, position-limit, tail-loss, daily-loss, fill-provenance and contract-note validation still does not exist. All 11 robustness blocker rows now cite `outputs/phase13/robustness_dimension_summary.csv` and `outputs/phase13/robustness_acceptance_gap_ledger.csv` in addition to the registry/smoke/profile robustness evidence. The 9 registered-strategy robustness blockers state that proxy smoke, multi-profile robustness, robustness-dimension coverage and acceptance-gap ledgers exist, while S10/S11 are explicitly marked not registered in the current alpha-parameter proxy grid. The robustness gate remains blocked because the acceptance-gap ledger has 79 open rows and shows that full required-seed execution, walk-forward runs, parameter-neighborhood smoothness, holdout-generator strategy reruns, negative-control acceptance evidence and real-data reruns are still missing. This is the correct current result because Phase 11 diagnostics are proxy-only, Phase 12 remains a 5-minute execution/lifecycle proxy rather than broker/exchange-verified execution, Phase 13 and Phase 14 remain proxy realism/robustness evidence rather than acceptance-grade validation, and holdout-generator strategy reruns plus multi-day real holdout evidence are still missing.

Important Phase 15 caveat: this phase is the promotion gate. A strategy may only advance when every applicable gate is backed by completed, current evidence. The current result is explicitly non-promotion for all S01-S11 strategies.

---

## Phase 16 — Metrics and Reporting

## 59. Predictive metrics

- directional accuracy;
- balanced accuracy;
- precision/recall by direction;
- ROC-AUC, used cautiously;
- Brier score;
- calibration curve;
- information coefficient;
- future return by signal decile;
- incremental \(R^2\);
- feature importance stability.

## 60. Trading metrics

- gross and net P&L;
- return on allocated capital;
- Sharpe and Sortino;
- maximum drawdown;
- Calmar ratio;
- profit factor;
- win rate;
- average win/loss;
- expectancy per trade;
- turnover;
- cost-to-gross-profit ratio;
- fill ratio;
- adverse selection;
- maximum adverse/favourable excursion;
- exposure and holding time.

## 61. Robustness breakdowns

Every report must break results down by:

- ticker;
- day;
- regime;
- time of day;
- volatility bucket;
- spread bucket;
- liquidity bucket;
- long/short;
- latency profile;
- cost profile;
- random seed;
- event versus non-event day.

**Current implementation status as of 2026-07-14:** Phase 16 has a runnable metrics/reporting layer in `scripts/run_phase16_metrics_reporting.py`, backed by `src/synthetic_l2/phase16_metrics_reporting.py`.

Generated artifacts are under `outputs/phase16/`:

- `phase16_metrics_reporting_report.md`;
- `metrics_reporting_manifest.json`;
- `metric_catalog.csv`;
- `predictive_metric_scoreboard.csv`;
- `predictive_proxy_diagnostics.csv`;
- `predictive_signal_bucket_returns.csv`;
- `predictive_brier_score_proxy.csv`;
- `predictive_calibration_curve_proxy.csv`;
- `predictive_baseline_comparison.csv`;
- `predictive_holdout_stability.csv`;
- `predictive_holdout_stability_summary.csv`;
- `feature_importance_stability_proxy.csv`;
- `predictive_promotion_falsification.csv`;
- `trading_metric_scoreboard.csv`;
- `economic_viability_frontier.csv`;
- `risk_adjusted_economic_frontier.csv`;
- `broker_reconciliation_readiness.csv`;
- `economic_reconciliation_strategy_summary.csv`;
- `markout_mae_mfe_summary.csv`;
- `breakdown_coverage.csv`;
- `strategy_metric_requirement_coverage.csv`.

The current completed run builds the reporting catalog and proxy scoreboards from Phase 11 diagnostics, Phase 9 feature/signals, Phase 12 execution summaries, the sampled trade ledger, the Phase 12 lifecycle/risk-control proxy, the Phase 13 seed plan and Phase 15 acceptance status. It produced 30 metric catalog rows, 11 predictive scoreboard rows, 9 predictive confusion/rank/R2 proxy rows, 27 ternary signal-bucket return rows, 9 Brier-score proxy rows, 45 calibration-bucket proxy rows, 11 predictive baseline-comparison rows, 407 predictive holdout-stability cell rows, 11 predictive holdout-stability summary rows, 9 feature-importance stability proxy rows, 11 predictive promotion-falsification rows, 99 predictive acceptance-gap rows, 27 trading scoreboard rows, 27 economic-viability frontier rows, 81 risk-adjusted economic frontier rows, 13 broker-reconciliation readiness rows, 11 economic-reconciliation strategy rows, 88 economic acceptance-gap rows, 27 sampled markout/MAE/MFE summary rows, 12 breakdown-coverage rows and 59 strategy-metric requirement coverage rows. All 30 metric catalog rows now carry explicit evidence paths to existing artifacts plus non-acceptance blockers. All predictive and trading metrics have at least proxy/sample evidence, including Brier score and calibration curve from deterministic ternary-signal pseudo-probabilities, baseline comparison against no-skill, majority-direction and Brier baselines, quarter/feed/segment holdout-stability diagnostics, feature-importance stability from seed-sampled feature/target association stability, predictive promotion falsification that combines baseline, untouched-test, holdout-cell and feature-stability criteria, and an economic frontier that decomposes gross edge, cost drag, Zerodha charge drag, net edge, break-even cost, additional gross edge needed and cost reduction needed by strategy/profile. The predictive promotion-falsification ledger currently has 11 rows: 0 proxy promotion candidates and 11 strategies falsified for predictive promotion under current proxy evidence. The predictive acceptance-gap ledger expands those blockers into 99 strategy/requirement rows: 58 rows have proxy evidence, all 99 rows remain open and 0 rows meet acceptance-grade predictive requirements. The standalone economic frontier currently has 4 net-positive proxy rows overall and 2 net-positive retail/stress rows; it is a diagnostic frontier, not acceptance evidence. The risk-adjusted economic frontier joins those net-edge rows to Phase 12 lifecycle breach severity across fill models, producing 0 joint-pass rows where net-positive proxy economics and proxy lifecycle risk-pass align, 0 retail/stress joint-pass rows and 12 economic-positive but risk-blocked rows. The broker-reconciliation readiness ledger decomposes documented Zerodha formula readiness versus missing broker evidence: 10 of 13 readiness rows have proxy/formula evidence, 0 rows have broker contract-note evidence, and the all-strategy summary marks 0 of 11 strategies economically reconciliation-ready. The economic acceptance-gap ledger expands those blockers into 88 strategy/requirement rows: 58 rows have proxy evidence, all 88 rows remain open and 0 rows meet acceptance-grade economic requirements. The Phase 14 realism acceptance-gap ledger is now also available as a reporting input with 88 open rows, 38 proxy-backed rows and 0 acceptance-met rows across quality, holdout, feed-imperfection, support, execution-realism, artifact-control and real multi-day validation requirements. The current predictive baseline comparison has 0 baseline-beating strategies: 5 runnable strategies do not beat the required proxy baselines and 6 strategies are partial or unsupported. The predictive holdout-stability diagnostic has 0 all-cell-pass strategies: 9 strategies fail at least some local-majority stability cells and S10/S11 are not supported by the current alpha-feature product. Required breakdown coverage now includes proxy volatility and liquidity buckets with three values each, and `random_seed` is now available as proxy seed lineage with 30 distinct values in the Phase 12 trade sample. Strategy metric requirement coverage now maps all 59 of 59 rows to computed/proxy/sample evidence; the previous unmapped regime-stability requirements are now mapped to the `holdout_segment_stability` proxy metric. No metric is acceptance-grade yet: `acceptance_grade_metrics=0`.

Important Phase 16 caveat: these reports are current-evidence scoreboards, not promotion evidence. Predictive metrics are Phase 11 ternary-signal proxy diagnostics, not calibrated probabilistic model outputs; trading metrics are Phase 12 5-minute marketable-order/lifecycle/markout proxies. Metrics remain proxy-only until full experiment execution, acceptance-grade risk/equity-curve simulation, calibrated model outputs, broker-verified fill/cost modeling and holdout-generator evidence exist.

---

## Phase 17 — Implementation Work Packages

## WP1 — Data intake and audit

Deliverables:

- schema detector;
- data-quality checks;
- sample-day profile;
- size report;
- canonical Parquet conversion.

## WP2 — Feature and event reconstruction

Deliverables:

- L1/L5 imbalance;
- MLOFI;
- trade classification;
- microprice;
- liquidity withdrawal;
- replenishment;
- book shape;
- regime-independent baseline features.

## WP3 — Regime/scenario framework

Deliverables:

- regime definitions;
- scenario YAML/JSON;
- daily calendar generator;
- intraday state generator;
- shock injector.

## WP4 — Price and cross-ticker simulator

Deliverables:

- market/sector/ticker factors;
- stochastic volatility;
- jump process;
- correlation controls;
- price-grid enforcement.

## WP5 — L2 event simulator

Deliverables:

- additions/cancellations/trades;
- five-level reconstruction;
- resilience;
- spread/depth dynamics;
- activity seasonality.

## WP6 — Retail feed emulator

Deliverables:

- receive latency;
- batching;
- gaps;
- duplicates;
- reconnects;
- asynchronous ticker stream.

## WP7 — Storage pipeline

Deliverables:

- raw/delta/resampled Parquet;
- partitioning;
- compression benchmark;
- replay tool;
- metadata manifest.

## WP8 — Backtester

Deliverables:

- event-driven engine;
- market and limit orders;
- latency;
- partial fills;
- slippage;
- fees;
- risk controls.

## WP9 — Strategy suite

Deliverables:

- S01-S11 modules;
- shared feature interface;
- baseline strategies;
- parameter registry.

## WP10 — Validation and reporting

Deliverables:

- synthetic realism dashboard;
- strategy performance reports;
- robustness matrix;
- failed-test log;
- promotion/rejection decision.

Current Phase 17 implementation status:

Generated artifacts are under `outputs/phase17/`:

- `phase17_work_packages_report.md`;
- `work_packages_manifest.json`;
- `work_package_registry.csv`;
- `deliverable_traceability.csv`;
- `implementation_gap_backlog.csv`.

The current completed run converts WP1-WP10 into an evidence-backed work-package registry. It tracks 10 work packages and 55 deliverables: 23 implemented deliverables, 32 proxy/partial deliverables and 0 missing deliverables. No work package is currently blocked by missing deliverables, the Phase 17 backlog has 0 P0 gaps, and the current P1 backlog has 0 rows. The deliverable traceability ledger now has 0 `missing_evidence` rows, including the multi-file WP8 fee evidence bundle. WP2 now has explicit inference-quality evidence for weak trade classification and visible-depth replenishment through `outputs/phase1/event_reconstruction/`. WP5 now has explicit add/cancel/consume proxy summaries from received market-by-price deltas through the same event-reconstruction quality artifact. WP7 has explicit raw/compact/features/resampled evidence through Phase 9 Tier A/B/C/D products; the 15-minute resampled panel is registered in DuckDB through `phase9_tier_d_resampled_features_15m`. The WP7 replay tool is implemented through `scripts/run_replay_tool.py`, validated by `outputs/replay/replay_validation_report.md`, and registered in DuckDB through `replay_validation_summary`. WP8 now has proxy evidence for event-driven order lifecycle, market/limit order models, partial fills, full-run no-fill risk, full-run fill-adjusted lifecycle/daily/breach-severity/risk-limit-sensitivity/acceptance-readiness risk controls, sampled lifecycle risk controls, Zerodha-sourced equity-intraday rupee order-formula fees applied to retail/stressed P&L proxy rows, representative order-notional charge formulas and broker-reconciliation readiness through `outputs/phase12/event_backtest_order_summary.csv`, `outputs/phase12/order_model_catalog.csv`, `outputs/phase12/full_run_risk_summary.csv`, `outputs/phase12/full_run_lifecycle_risk_summary.csv`, `outputs/phase12/full_run_lifecycle_daily_risk_summary.csv`, `outputs/phase12/full_run_lifecycle_risk_breach_severity.csv`, `outputs/phase12/full_run_lifecycle_risk_limit_sensitivity.csv`, `outputs/phase12/full_run_risk_acceptance_readiness.csv`, `outputs/phase12_order_lifecycle/partial_fill_summary.csv`, `outputs/phase12_order_lifecycle/risk_control_summary.csv`, `outputs/phase12/cost_schedule.csv`, `outputs/phase12/charge_component_catalog.csv`, `outputs/phase12/representative_charge_scenarios.csv` and `outputs/phase16/broker_reconciliation_readiness.csv`. WP9 now has explicit S01-S11 module registry evidence through `outputs/phase11/strategy_module_registry.csv`, with S10/S11 represented as non-alpha execution/risk-filter modules and no promotion-ready modules. WP10 now has deterministic robustness-smoke, execution-profile robustness, robustness-dimension coverage and robustness acceptance-gap ledgers through `outputs/phase13/experiment_run_summary.csv`, `outputs/phase13/experiment_profile_robustness_summary.csv`, `outputs/phase13/robustness_dimension_summary.csv` and `outputs/phase13/robustness_acceptance_gap_ledger.csv`, Phase 14 holdout-generator realism proxy evidence and realism acceptance-gap tracking through `outputs/phase14/holdout_generator_realism_summary.csv` and `outputs/phase14/realism_acceptance_gap_ledger.csv`, Phase 16 predictive holdout-stability and economic-frontier proxy evidence through `outputs/phase16/predictive_holdout_stability_summary.csv`, `outputs/phase16/predictive_promotion_falsification.csv`, `outputs/phase16/predictive_acceptance_gap_ledger.csv`, `outputs/phase16/economic_viability_frontier.csv`, `outputs/phase16/risk_adjusted_economic_frontier.csv`, `outputs/phase16/broker_reconciliation_readiness.csv`, `outputs/phase16/economic_reconciliation_strategy_summary.csv` and `outputs/phase16/economic_acceptance_gap_ledger.csv`, plus a static validation dashboard through `outputs/dashboard/synthetic_l2_validation_dashboard.html`.

The remaining work is acceptance hardening rather than missing-deliverable closure: promote proxy/partial artifacts to full-run, broker-verified and holdout-tested evidence before any strategy promotion claim.

Important Phase 17 caveat: this is a traceability and implementation-backlog layer, not a promotion result. It intentionally preserves proxy/partial statuses where earlier phases have generated useful artifacts but not acceptance-grade evidence.

---

## Phase 18 — Suggested Technology Stack

| Component | Suggested options |
|---|---|
| Language | Python |
| DataFrame engine | Polars and/or PyArrow; Pandas for smaller summaries |
| Storage | Parquet + Zstandard |
| Query | DuckDB |
| Numerical work | NumPy, SciPy |
| Statistical models | statsmodels, scikit-learn |
| Tree models | LightGBM/XGBoost if permitted |
| Configuration | YAML + Pydantic |
| Experiment tracking | MLflow or structured local metadata |
| Parallel generation | multiprocessing, Ray or Dask only if needed |
| Testing | pytest + property-based tests |
| Visualization | Matplotlib/Plotly |
| Versioning | Git; data manifests and generator-version hashes |

Avoid introducing distributed infrastructure before single-machine limits are measured.

Current Phase 18 implementation status:

Generated artifacts are under `outputs/phase18/`:

- `phase18_technology_stack_report.md`;
- `technology_stack_manifest.json`;
- `stack_decisions.csv`;
- `dependency_availability.csv`.

The current completed run records 21 stack decisions and checks 15 local dependencies. All 5 required-now dependencies are available: Python, Pandas, NumPy, PyArrow and DuckDB. Optional or deferred dependencies such as SciPy, scikit-learn, statsmodels, Polars, Pydantic, Hypothesis and Plotly/Matplotlib-related extensions remain non-blocking until the relevant modeling, testing or dashboard work starts. `pytest` is marked `recommended_next` for formal test coverage.

Important Phase 18 caveat: this phase deliberately keeps the stack single-machine and local-first. Distributed tools such as Ray/Dask and experiment servers such as MLflow remain deferred until measured local bottlenecks or experiment volume justify them.

---

## Phase 19 — Reproducibility

Every generated partition must record:

- generator version;
- configuration hash;
- random seed;
- calibration dataset ID;
- ticker metadata version;
- regime calendar version;
- scenario IDs;
- cost model version;
- latency model version;
- creation timestamp.

A manifest should allow exact regeneration.

Current Phase 19 implementation status:

Generated artifacts are under `outputs/phase19/`:

- `phase19_reproducibility_report.md`;
- `reproducibility_manifest.json`;
- `reproducibility_required_fields.csv`;
- `manifest_field_audit.csv`;
- `artifact_reproducibility_summary.csv`;
- `reproducibility_gap_summary.csv`;
- `manifest_schema_template.json`;
- `reproducibility_remediation_plan.csv`;
- `reproducibility_remediation_summary.csv`;
- `normalized_manifest_overlay_manifest.json`;
- `normalized_manifest_overlay_summary.csv`;
- `normalized_manifest_field_sources.csv`;
- `normalized_manifests/*.normalized_manifest.json`;
- `reproducibility_gate_result.json`;
- `reproducibility_gate_report.md`.

The current completed run audits 10 required reproducibility fields across 27 phase/workspace/dashboard/decision manifests, producing 270 field checks. Current native source-manifest coverage is complete for the audited artifact set: all 27 artifacts are exact-regeneration-ready at the source-manifest level, 0 artifacts have missing fields and 0 artifact groups have a missing/unreadable manifest. The exact-ready source manifests now include `stage_a1`, `phase1`, `phase1_event_reconstruction`, `phase2`, `phase3`, `phase4`, `phase5`, `phase6`, `phase7`, `phase8`, `phase9`, `phase10`, `phase11`, `phase11_strategy_modules`, `phase12`, `phase12_event_backtest`, `phase13`, `phase13_smoke_run`, `phase14`, `phase15`, `phase16`, `phase17`, `phase18`, `phase20`, `horizon_readiness`, `dashboard` and `duckdb`.

The remediation layer now emits a normalized reproducibility manifest template and 270 field-level remediation rows. All 270 rows are `complete_exact`, confirming that the audited source manifests now expose the exact required fields without generator-field, alias-normalization or recover/rerun gaps.

The normalized manifest overlay still creates exact-field manifest overlays for all 27 audited artifacts. The overlay now has 27 exact-field-ready artifacts and 270 normalized field rows, with all 270 values coming from exact/alias fields already present in source manifests and 0 values supplied by normalizer defaults. It is retained as an audit/inspection bridge, not as a substitute for source-manifest metadata.

Important Phase 19 caveat: this phase now proves native reproducibility metadata coverage for the 27 audited manifests, not byte-for-byte deterministic regeneration of every large Parquet/table artifact and not coverage for future artifact classes that are not yet registered in the Phase 19 manifest-candidate list. New phases or dashboards must be added to the audit candidate list and emit the same normalized manifest schema before they can be treated as exact-regeneration-ready.

The regression guardrail is `python scripts/run_reproducibility_gate.py`. It fails if the 27/27 native exact-ready invariant, zero missing/unreadable manifests, 27/27 normalized-overlay readiness, zero normalizer-default fields, or `complete_exact`-only remediation state regresses.

**Current Phase 20 implementation status as of 2026-07-14:** Phase 20 now has a runnable acceptance-hardening queue in `scripts/run_phase20_acceptance_hardening.py`, backed by `src/synthetic_l2/phase20_acceptance_hardening.py`. This is an execution-sequence and blocker-prioritization artifact, not a strategy-promotion result.

Generated Phase 20 artifacts are under `outputs/phase20/`:

- `phase20_acceptance_hardening_report.md`;
- `acceptance_hardening_manifest.json`;
- `acceptance_hardening_queue.csv`;
- `acceptance_hardening_gate_summary.csv`;
- `acceptance_hardening_strategy_summary.csv`;
- `risk_hardening_plan.csv`;
- `risk_hardening_action_summary.csv`;
- `economic_hardening_plan.csv`;
- `economic_hardening_action_summary.csv`.

The current completed Phase 20 run converts the 50 Phase 15 blocker rows and Phase 17 proxy backlog into 50 ranked acceptance-hardening queue rows, 5 gate-summary rows and 11 strategy-summary rows. The highest-priority gate is `G04_risk`, with 11 blocked strategies, followed by `G02_economic`, `G01_predictive`, `G03_robustness` and `G05_realism`. Phase 20 now decomposes the top risk blocker into `outputs/phase20/risk_hardening_plan.csv`: 88 strategy/risk-requirement rows across broker/exchange fill provenance, contract-note/cost reconciliation, full-run coverage, daily equity/halt state, daily-loss validation, drawdown validation, position-limit validation and tail-loss validation. Of those rows, 54 have proxy evidence that must be upgraded into acceptance evidence, 34 still lack required evidence, 0 meet acceptance requirements and 0 are acceptance-ready. The companion `risk_hardening_action_summary.csv` groups the work into 6 action classes: guardrail validation, acceptance-run coverage, broker contract-note reconciliation, broker/exchange reconciliation, risk-state persistence and tail-risk validation. Phase 20 also decomposes the P2 economic blocker into `outputs/phase20/economic_hardening_plan.csv`: 88 strategy/economic-requirement rows across broker/exchange fill provenance, contract-note reconciliation, Zerodha order-formula readiness, latency/slippage stress confirmation, retail-and-stress net profitability, stressed-profile net profitability, risk-adjusted economic joint pass and multi-day real/holdout economic validation. Of those rows, 58 have proxy evidence that must be upgraded into acceptance evidence, 30 still lack required evidence, 0 meet acceptance requirements and 0 are acceptance-ready. The companion `economic_hardening_action_summary.csv` groups the work into 8 action/dependency rows covering broker contract-note reconciliation, broker/exchange fill reconciliation, documented cost-formula validation, holdout/real multi-day economic validation, latency/slippage acceptance replay, net-profitability validation and risk-adjusted economic validation. The queue has 0 acceptance-ready rows by design: it identifies the next evidence-producing work, not completed acceptance evidence. The dashboard and DuckDB workspace now register these Phase 20 outputs, and Phase 19 now audits the Phase 20 manifest as an exact-regeneration-ready source manifest.

Important Phase 20 caveat: the ranking is deterministic blocker triage based on current evidence, not an optimization proof. It should guide the next implementation sequence, but it does not relax any Phase 15 acceptance gate.

---

## Phase 20 — Initial Execution Sequence

### Stage A1 — Current one-day tick-stream audit

1. ingest the supplied Parquet files;
2. infer and document schema;
3. validate timestamps and depth;
4. verify manifest/file/row completeness and identify source-side gaps;
5. measure received-event rates, inter-arrival times, batch-flush cadence and storage separately;
6. compact the 50,205 small batch files into an analysis-efficient tick dataset without changing row order or semantics;
7. produce separate equity and ETF profiles;
8. produce a parameter-evidence ledger marking each parameter as measured, weakly estimated, assumed or blocked.

**Stage A1 exit gate:** structural and receive-order checks pass, horizon coverage is measured per symbol, and every downstream parameter has an evidence label.

**Current implementation status as of 2026-07-13:** Stage A1 has an initial runnable implementation in `scripts/run_stage_a1_audit.py`, backed by `src/synthetic_l2/stage_a1_audit.py`.

Generated artifacts are under `outputs/stage_a1/`:

- `stage_a1_report.md`;
- `data_quality_report.csv` and `data_quality_report.parquet`;
- `horizon_coverage.csv`;
- `file_inventory.csv`;
- `schema_report.csv`;
- `schema_mismatches.csv`;
- `manifest_check.json`;
- `parameter_evidence_ledger.csv`;
- compact received-tick Parquet files under `compact_ticks_by_symbol/symbol=*/ticks.parquet`.

The first completed run produced 32 compact per-symbol files with 620,853 total rows, matching the raw input audit. Manifest/file completeness passed for 50,205 files. Logical schema compatibility passed for all files; exact physical schema differs in many files because `volume_traded` appears as both `double` and `int64`, but it remains a numeric field. Receive monotonic ordering, crossed-book checks and L1-L5 depth price ordering passed.

Important Stage A1 caveat: under the current dense full-session 90% bin-coverage rule, all symbols are below the 1-second regular-panel gate, while 30 of 32 pass the 5-second gate. This does not mean 1-second/sub-second ticks are absent. One-second features are conditionally supported by symbol and time window, especially active/open windows; they must use event-driven ticks or window-specific coverage/staleness labels rather than a blanket full-session dense-panel assumption.

### Stage A2 — Capture-diagnostics and multi-day expansion

In parallel with initial one-day engineering:

1. continue subscription-driven collection under the Class B contract;
2. add or verify local sequences, connection boundaries and dropped-message diagnostics;
3. confirm actual callback cadence and timestamp semantics;
4. compact without resampling or losing event order;
5. capture at least 5–10 complete days for initial normal-day event calibration.

**Stage A2 exit gate:** at least 5–10 complete, diagnostically sound days are available for initial normal-day variability and event-model calibration. One-day feature/pipeline work may proceed before this gate, but strategy robustness or promotion claims may not.

### Stage B1 — Received-tick structural synthetic proof

Using the current Class B evidence, generate a small proof for:

- 5 instruments including at least one ETF;
- 5 normal days plus explicit trend and shock scenarios;
- five-level book states at a cadence no finer than the real evidence used for validation;
- deterministic replay, price-grid, spread, depth-ordering and storage checks.

Do not use Stage B1 to accept or reject S01–S11 profitability. Its purpose is generator engineering, received-tick feature verification and falsification of structural defects.

### Stage B2 — Event-driven synthetic proof

Generate:

- the same 5-instrument development subset;
- 5 normal days;
- 2 trend days;
- 1 shock day;
- raw and 1-second/event-driven feature datasets for symbols and windows whose measured coverage supports that horizon.

This stage may start after Stage A1. Validate event-level and statistical realism against the current Class B day, but keep all strategy results preliminary and day-specific until Stage A2 and later holdout gates pass.

### Stage C — Medium pilot

Generate:

- all 32 instruments;
- 20 trading days;
- 3 random seeds;
- multiple regimes.

Run S01-S05 and baseline strategies.

### Stage D — Three-month study

Generate:

- 32 instruments;
- 63 trading days;
- Q-A, Q-B and Q-C profile families;
- at least 3 seeds initially, later 10;
- raw compact L2 plus feature datasets.

Run all strategies, with S09-S11 treated as experimental controls.

### Stage E — Full-year extension

Only after:

- synthetic-quality gates pass;
- backtest controls pass;
- storage is acceptable;
- strategy code is stable;
- results are not dependent on generator artifacts.

---

## Phase 21 — Decision Framework after Three Months

| Outcome | Decision |
|---|---|
| No strategy survives costs and latency | Improve or reject strategies; do not tune generator to create profit |
| Only price baselines work | L2 adds insufficient value under tested assumptions |
| L2 improves baseline modestly and robustly | Continue collecting real data and extend synthetic testing |
| Strategy works only in one regime | Build explicit regime gate and test false-classification risk |
| Strategy works only with zero latency | Reject for retail deployment |
| Strategy works only with optimistic passive fills | Reject or redesign execution |
| Strategy works across generators/seeds | Candidate for real-data paper testing |
| Strategy works synthetically but not on accumulating real days | Treat as generator artifact and investigate |
| Results vary wildly by seed | Insufficient robustness or unstable scenario design |

---

## Phase 22 — Real Data Integration Roadmap

Synthetic testing should run in parallel with continued real capture.

The milestones below refer to complete **Class B event-grade days** for event-flow recalibration. Additional Class A snapshot days improve coarse distributions but do not satisfy event-level milestones.

### As new real days arrive

Re-estimate:

- intraday curves;
- spread/depth distributions;
- regime frequencies;
- price-impact functions;
- trade/quote interaction;
- cross-ticker correlation;
- shocks and recovery;
- retail feed latency;
- missing-data patterns.

### Recommended milestones

| Real-data availability | Recalibration use |
|---|---|
| 1 day | schema, scale and pipeline |
| 5–10 days | normal intraday variation |
| 20–30 days | basic regime calibration |
| 60 days | preliminary out-of-sample comparison |
| 3–6 months | meaningful strategy screening |
| 12+ months | stronger regime and robustness assessment |

Synthetic data should progressively become less assumption-driven as the real dataset grows.

---

## Phase 23 — Key Risks

### 23.1 Synthetic alpha

The generator may accidentally encode a predictable relationship that strategies exploit.

Mitigations:

- negative-control generators;
- multiple model families;
- hidden holdout generator;
- parameter perturbation;
- real-data paper testing;
- generator-blind strategy development where feasible.

### 23.2 One-day overfitting

The sample day may be unusual.

Mitigations:

- pooled shrinkage;
- broad stress ranges;
- explicit uncertainty bands;
- multiple synthetic normal-day configurations;
- immediate recalibration with new real days.

### 23.3 Unrealistic fills

Mitigations:

- pessimistic execution;
- marketable-order focus initially;
- latency simulation;
- partial fills;
- depth walk;
- adverse-selection modelling.

### 23.4 Excessive data volume

Mitigations:

- event-driven generation;
- integer encoding;
- Parquet/Zstandard;
- delta-state representation;
- separate raw and feature tiers;
- selected dense tickers;
- feature-only datasets for repeated experiments.

### 23.5 False confidence from three months

Three synthetic months are a screening laboratory, not a profitability proof.

Promotion path:

```text
Synthetic engineering test
→ synthetic multi-regime stress test
→ real-data historical test
→ live paper trading
→ shadow execution
→ very small capital
→ gradual scale-up
```

---

## 24. Recommended Initial Scope

### 24.1 Immediate scope with the supplied Class B day

- all 32 supplied instruments;
- one received-tick day for schema, scale, event timing and initial microstructure calibration;
- full five-level depth;
- equity-versus-ETF profiling;
- tick-batch compaction with deterministic receive-order replay;
- per-symbol coverage/staleness analysis for every proposed feature horizon;
- OFI/MLOFI, microprice, book-shape and cumulative-volume-change feature verification;
- structural and received-event generator invariants;
- explicit uncertainty ranges for one-day estimates and unobservable queue parameters;
- a 5-instrument event-driven proof using horizons supported by observed density;
- automated quality reporting and a parameter-evidence ledger.

Do not assume uniform 100 ms, 250 ms, 500 ms or 1 s support across symbols. Measure it. The sample may be used for day-specific S01–S11 falsification and pipeline tests, but not for robust acceptance or profitability claims.

### 24.2 Scope after the Class B multi-day gate passes

- all 32 instruments;
- at least 5–10 event-grade days for initial calibration, with continued collection;
- 63 synthetic trading days;
- three quarter profiles and three seeds per profile initially;
- state-changing event storage;
- 250 ms, 1 s and 5 s feature views only where supported by observed event density;
- S01–S08 as primary research;
- S09 as a latency benchmark;
- S10–S11 as experimental/risk-only modules;
- pessimistic execution assumptions;
- automated quality and strategy reports.

This staged scope preserves useful work from the current day without granting it event-level evidence it does not contain.

---

## 25. Final Principle

The synthetic generator must be designed to **challenge strategies**, not to make them profitable.

A high-quality outcome is not necessarily a winning strategy. A high-quality outcome may be the early rejection of fragile ideas that depend on:

- perfect fills;
- zero latency;
- one market regime;
- one ticker;
- hidden future information;
- unrealistic book behaviour;
- insufficient transaction-cost modelling.

The strongest candidates will be those that survive:

- multiple synthetic generators;
- multiple regime calendars;
- multiple random seeds;
- realistic costs;
- adverse latency;
- data gaps;
- pessimistic execution;
- and later, genuinely unseen real Zerodha data.

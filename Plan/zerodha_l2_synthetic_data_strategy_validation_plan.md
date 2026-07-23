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
- 1ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ31 rows per Parquet file, with all files readable and using the same 54-column schema;
- 1,569 batch files for most symbols and 1,568 for GOLDBEES, JUNIORBEES and NIFTYBEES;
- WebSocket-based tick-wise Zerodha updates inside the files;
- typical observed per-symbol receive intervals of approximately 0.5ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ2 seconds, varying with symbol activity;
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

### 1.4 Terminology: market-data levels versus book-depth levels

This project must use the terms **L1-L5** carefully because they can mean different things in market-data conversations.

General market-data terminology is not universal across exchanges and vendors, but the common distinction is:

| Term | Typical meaning | Typical use |
| --- | --- | --- |
| Level 1 / L1 market data | Last traded price, best bid, best ask, bid/ask quantity, volume and OHLC-style quote fields | Basic quotes, investing, simple order placement and top-of-book logic |
| Level 2 / L2 market data | Aggregated bid/ask market-by-price depth, often top 5 or top 10 visible price levels | Liquidity analysis, spread and slippage estimation |
| Level 3 / L3 market data | Deeper or order-level book detail where available | Scalping, execution planning and order-flow analysis |
| Level 4 / L4 market data | Vendor-specific enriched microstructure data such as full-depth/order-by-order events or participant information | Institutional execution and deeper market-microstructure research |
| Level 5 / L5 market data | Vendor-specific analytics derived from order-book state rather than a universal exchange standard | Advanced imbalance, liquidity and derived-feature modelling |

For this repository:

- **Zerodha L2** means Zerodha's retail WebSocket market-depth feed with **top-five visible market-by-price depth**, not exchange order-by-order L3/L4/L5 data.
- **Depth level 1** means the best bid or best ask row inside that top-five book snapshot.
- **Depth levels 2-5** mean the second through fifth visible bid/ask price levels inside the same Zerodha L2/top-five market-by-price snapshot.
- References to `bid_level_1` through `bid_level_5` and `ask_level_1` through `ask_level_5` are **book-depth rows**, not market-data product tiers.
- The plan should prefer phrases such as **top-five depth**, **depth levels 1-5**, **depth levels 2-5**, and **top-of-book/best-bid-offer** when describing features.
- The plan should avoid using **L2-L5** to describe features, because that can incorrectly imply multiple market-data product tiers. If the phrase appears in older phase history, it should be read as historical shorthand for visible book-depth fields, not as a claim that Zerodha provides L3/L4/L5 market-data tiers.

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
    ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ
Daily market regime
    ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ
Intraday regime schedule
    ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ
Market/index latent process
    ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ
Sector latent processes
    ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ
Ticker latent efficient prices
    ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ
Liquidity/spread/depth state
    ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ
Order-flow and trade events
    ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ
Top-five L2 snapshots/events
    ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ
Retail receive latency and data imperfections
    ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ
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

## Phase 0 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Intake Contract for the Real Sample Data

Before generation, establish a strict input contract.

### 4.1 Expected input

Maintain two explicit intake classes.

**Class A ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â periodic polling snapshot input:**

- one complete NSE trading day where possible;
- clearly identifiable symbol and instrument token;
- exchange, last-trade and local receive timestamps;
- L1-L5 prices, quantities and order counts;
- known polling/sampling cadence;
- no claim that changes between snapshots were observed.

**Class B ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â received WebSocket tick input (the current sample):**

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
| One or more rows per source file | Pass: 1ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ31 rows per file | Compaction is strongly recommended before repeated analysis |
| WebSocket tick-wise capture | Pass | Received-event profiling may proceed |
| Receive ordering | Partial pass: receive UTC milliseconds plus monotonic nanoseconds are present | Verify ties and monotonicity before event reconstruction |
| Connection/reconnect diagnostics in row schema | Not present in inspected 54-column schema | Gap/reconnect attribution remains limited |
| Sub-second observation density | Mixed by symbol | Gate each feature horizon using empirical coverage and staleness |

No downstream work package may silently convert a failed or partial gate into a calibrated parameter. Unsupported parameters must be supplied as documented scenario assumptions with sensitivity ranges.

---

## Phase 1 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Normalize and Reconstruct the Real Day

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

## Phase 2 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Empirical Calibration from the Real Day

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

## Phase 3 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Regime Taxonomy

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

## Phase 4 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Three-Month Synthetic Scenario Calendar

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
- at least 2ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ4 ticker-specific shocks per ticker;
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

## Phase 5 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Price Process

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

## Phase 6 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Limit Order Book Generator

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

## Phase 7 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Synthetic Event and Shock Library

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

## Phase 8 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Simulate Zerodha Retail Feed Characteristics

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
| Good retail | 50ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ100 ms | moderate tail |
| Normal retail | 150ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ300 ms | occasional 500ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ1000 ms |
| Stressed retail | 300ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ700 ms | long tail and bursts |
| Disconnect scenario | N/A | 2ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ30 second gaps |

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

## Phase 9 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Data Products

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

## Phase 10 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Storage and Size Optimization

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

Avoid excessive tiny files. Aim for approximately 128ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ512 MB Parquet files where practical.

**Current storage/query decision as of 2026-07-13:** keep Parquet/Zstandard as the durable storage format and use DuckDB as the local analytic query layer over Parquet/CSV views. Do not load high-volume tick or depth data into SQLite. SQLite may be introduced later only for a small transactional run registry, manual annotations or experiment metadata.

DuckDB is installed in the current Python environment and an initial workspace builder exists in `scripts/build_duckdb_workspace.py`, backed by `src/synthetic_l2/duckdb_workspace.py`.

Generated artifacts are under `outputs/duckdb/`:

- `synthetic_l2.duckdb`;
- `duckdb_workspace_report.md`;
- `duckdb_workspace_manifest.json`.

The current DuckDB validation registers views over Stage A1 through Phase 39 outputs. SQL validation confirms the core row-count invariants across the compact real tick data, normalized/delta feature products, synthetic generation layers, execution/risk/metrics outputs, Phase 15 acceptance gates, Phase 16 metric and acceptance-gap ledgers, Phase 17 traceability, Phase 19 reproducibility artifacts, Phase 20 hardening outputs, the Phase 21 decision framework, the Phase 22 real-data integration roadmap, the Phase 23 key-risk register, the Phase 25 event replay expansion, the Phase 26 strategy-salvage scan, the Phase 27 feature-edge cost-hurdle scan, the Phase 28 richer event-label support layer, the Phase 29 partial-strategy proxy replay, the Phase 30 strategy decision triage, the Phase 31 redesign evidence contract, the Phase 32 contract evidence scanner, the Phase 33 broker evidence intake package, the Phase 34 real-data multi-day readiness inventory, Phase 35 computable diagnostics, Phase 36 collector instrumentation, Phase 37 collector ledger verification, Phase 38 Class B day promotion and Phase 39 synthetic-only acceptance path. Current headline counts include 620,853 compact tick rows, 620,853 normalized rows, 620,853 received-delta rows, 2,276,143 Phase 9 Tier A events, 2,259,039 Phase 9 Tier B/C rows, 756,000 Phase 9 Tier D 15-minute rows, 0 promoted Phase 15 strategies, 50 Phase 20 acceptance-hardening queue rows, 411 Phase 20 acceptance execution-roadmap rows, 7 Phase 20 acceptance execution milestones, 259 Phase 20 execution-roadmap rows with proxy evidence, 152 Phase 20 execution-roadmap rows missing required evidence, 9 met Phase 20 execution-roadmap proxy-registration rows, 88 Phase 20 risk-hardening rows, 88 Phase 20 economic-hardening rows, 99 Phase 20 predictive-hardening rows, 88 Phase 20 robustness-hardening rows, 48 Phase 20 realism-hardening rows, 4 Phase 20 M01 required broker/external evidence files, 0 currently available broker/external files, 40 Phase 20 M01 broker evidence schema rows, 5 Phase 20 M01 broker reconciliation tests, 44 Phase 20 M01 broker/external gap rows, 28 Phase 20 M02 strategy-support closure rows, 12 Phase 20 M02 feature-engineering rows, 6 Phase 20 M02 explicit non-alpha classification rows, 10 Phase 20 M02 proxy-to-acceptance upgrade rows, 66 Phase 20 M03 predictive-validation rows, 11 Phase 20 M03 calibrated-model-required rows, 22 Phase 20 M03 holdout/untouched-test rows, 11 Phase 20 M03 promotion-falsification rows, 0 Phase 20 M03 acceptance-met rows, 66 Phase 20 M04 robustness-execution rows, 22 Phase 20 M04 full-seed-required rows, 22 Phase 20 M04 walk-forward-required rows, 11 Phase 20 M04 parameter-smoothness-required rows, 11 Phase 20 M04 execution-profile-required rows, 11 Phase 20 M04 negative-control-required rows, 0 Phase 20 M04 acceptance-met rows, 121 Phase 20 M05 lifecycle/economic replay rows, 66 Phase 20 M05 risk-replay-required rows, 55 Phase 20 M05 economic-replay-required rows, 11 Phase 20 M05 broker-reconciliation-required rows, 33 Phase 20 M05 guardrail-validation-required rows, 0 Phase 20 M05 acceptance-met rows, 47 Phase 20 M06 holdout/realism rerun rows, 17 Phase 20 M06 holdout-rerun-required rows, 6 Phase 20 M06 quality-gate-required rows, 6 Phase 20 M06 feed-imperfection-required rows, 6 Phase 20 M06 pessimistic-execution-required rows, 6 Phase 20 M06 artifact-control-required rows, 0 Phase 20 M06 acceptance-met rows, 39 Phase 20 M07 real multi-day acceptance rows, 11 Phase 20 M07 economic-real-validation rows, 11 Phase 20 M07 predictive-real-holdout rows, 11 Phase 20 M07 robustness-real-rerun rows, 6 Phase 20 M07 realism-real-validation rows, 0 Phase 20 M07 acceptance-met rows, 192 Stage A2 capture-diagnostics rows, 17 Stage A2 required capture schema rows, 32 Stage A2 symbols evaluated, 1 current sample day available, 192 Stage A2 open contract rows, 0 Stage A2 acceptance-met rows, 5 Stage B1 development symbols, 1 Stage B1 ETF symbol, 70,875 Stage B1 L2 subset rows, 7 Stage B1 structural-check rows, 7 Stage B1 passed structural checks, 0 Stage B1 failed structural checks, 5 Stage B2 development symbols, 1 Stage B2 event-driven 1s-ready symbol, 8 Stage B2 selected scenario days, 15,061 Stage B2 raw-event rows, 14,952 Stage B2 event-feature rows, 2,400 Stage B2 event-driven 1s feature rows, 7 Stage B2 proof-check rows, 7 Stage B2 passed proof checks, 0 Stage B2 failed proof checks, 32 Stage C symbols, 20 Stage C selected trading days, 3 Stage C selected seed rows, 239,173 Stage C feature rows, 15 Stage C strategy proxy run rows, 21 Stage C baseline proxy run rows, 7 Stage C check rows, 7 Stage C passed checks, 0 Stage C failed checks, 32 Stage D symbols, 3 Stage D quarter profiles, 63 Stage D minimum days per profile, 2,259,228 Stage D feature rows, 99 Stage D strategy proxy rows, 27 Stage D control/risk rows, 9 Stage D check rows, 9 Stage D passed checks, 0 Stage D failed checks, 7 Stage E prerequisite rows, 3 Stage E passing prerequisites, 4 Stage E blocking prerequisites, 0 Stage E extension-allowed rows, 9 Phase 21 decision rules, 1 Phase 21 active current decision, 0 Phase 21 extension/paper-ready rows, 6 Phase 22 real-data milestone rows, 0 Phase 22 Class B event-grade days, 54 Phase 22 recalibration task rows, 0 Phase 22 ready recalibration tasks, 0 Phase 22 extension/paper-ready rows, 5 Phase 23 key risks, 5 Phase 23 open acceptance-blocking risks, 31 Phase 23 mitigation rows, 7 Phase 23 promotion-path steps, 0 Phase 23 promotion-ready rows, 113,848 Phase 25 event replay trade rows, 24 Phase 25 model/profile rows, 5 Phase 25 strategy models replayed, 0 Phase 25 positive strategy/profile rows, 3 Phase 25 beats-best-baseline rows, 0 Phase 25 acceptance-ready rows, 542,406 Phase 26 strategy-salvage trade rows, 120 Phase 26 registered variants, 282 Phase 26 variant/profile rows, 0 Phase 26 realistic positive rows after costs, 17 Phase 26 zero-latency positive control rows, 0 Phase 26 salvage candidate rows, 282 Phase 26 rejected variant/profile rows, 0 Phase 26 acceptance-ready rows, 1,213,296 Phase 27 feature-edge trade rows, 112 Phase 27 registered feature candidates, 336 Phase 27 candidate/profile rows, 0 Phase 27 positive rows after costs, 0 Phase 27 realistic cost-clearing rows, 0 Phase 27 zero-latency edge-control rows, 336 Phase 27 rejected candidate/profile rows, 0 Phase 27 acceptance-ready rows, 620,853 Phase 28 richer event-label rows, 133,020 Phase 28 lead-lag bucket rows, 32 Phase 28 symbols evaluated, 4 Phase 28 partial strategy families, 4 Phase 28 proxy-feature engineered families, 290,162 Phase 28 proxy label rows, 0 Phase 28 acceptance-ready rows, 742,623 Phase 29 partial-strategy proxy replay trade rows, 4 Phase 29 partial strategies replayed, 12 Phase 29 strategy/profile rows, 0 Phase 29 positive rows after costs, 0 Phase 29 realistic positive rows, 0 Phase 29 proxy candidate rows, 0 Phase 29 acceptance-ready rows, 11 Phase 30 strategy/control families triaged, 9 Phase 30 alpha families triaged, 9 Phase 30 reject/redesign rows, 2 Phase 30 non-alpha control rows, 0 Phase 30 promotion-ready rows, 0 Phase 30 acceptance-ready rows, 0 Phase 30 realistic positive execution rows, 0 Phase 30 candidate rows, 4 Phase 30 proxy-label-only families, 9 Phase 31 strategy redesign specs, 44 Phase 31 contract requirement rows, 44 Phase 31 open contract requirements, 0 Phase 31 replay-allowed rows, 9 Phase 31 replay-blocked rows, 0 Phase 31 acceptance-ready rows, 7 Phase 31 label-engineering requirements, 3 Phase 31 broker-evidence requirements, 9 Phase 31 execution-economics requirements, 44 Phase 32 contract rows scanned, 35 Phase 32 proxy/partial available rows, 21 Phase 32 external/new-artifact missing rows, 0 Phase 32 acceptance-met rows, 0 Phase 32 replay-allowed rows, 9 Phase 32 strategy rows scanned, 9 Phase 32 evidence acquisition queue rows, 4 Phase 33 broker evidence templates generated, 4 Phase 33 expected external files, 0 Phase 33 external files present, 0 Phase 33 acceptance import-ready files, 4 Phase 33 missing external files, 0 Phase 33 reconciliation tests ready, 0 Phase 33 acceptance-ready rows, 1 Phase 34 raw trade day available, 1 Phase 34 full-universe raw day, 0 Phase 34 Class B event-grade days, 5 Phase 34 required minimum complete days, 5 Phase 34 days needed for minimum, 10 Phase 34 days needed for target, 192 Phase 34 Stage A2 open contract rows and 0 Phase 34 replay-allowed rows. The full current SQL rollup is preserved in `outputs/duckdb/duckdb_workspace_report.md`.

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
- periodic full checkpoint every 30ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ300 seconds;
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
| Small | unit/integration tests | 1ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ5 tickers, 5ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ10 days |
| Medium | initial strategy screening | 32 instruments, 63 days, controlled event rates |
| Full | annual stress study | 32 instruments, 252 days |
| Dense | microstructure stress | selected 5ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ10 tickers at high event rate |
| Feature-only | rapid ML experiments | resampled feature tables, no raw replay |

---

## Phase 11 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Strategy Validation Matrix

This phase defines the eventual experiments. The current tick-wise day supports feature engineering, pipeline tests and within-day falsification, but not robust strategy acceptance. S01ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œS11 promotion decisions require multiple real days plus multi-seed synthetic controls; any result based primarily on this one day must be labelled preliminary and day-specific.

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

The first completed run emitted 11 strategy rows covering S01ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“S11, 77 baseline-requirement rows, 65 scenario-requirement rows and 59 metric-requirement rows. All strategies are explicitly marked `promotion_allowed_now = false` with the evidence label `engineering_and_within_day_falsification_only`.

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

## 27. S01 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Momentum/Breakout + MLOFI

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

## 28. S02 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Pure Multi-Level OFI

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
- incremental value of levels 2ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ5;
- feature stability across regimes.

---

## 29. S03 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Liquidity-Vacuum Breakout

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

## 30. S04 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Trade-Flow + Depth Confirmation

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

## 31. S05 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Microprice Filter

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

## 32. S06 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Absorption and Exhaustion

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

## 33. S07 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Mean Reversion after Imbalance

### Hypothesis

Extreme temporary imbalance followed by replenishment and declining trade intensity predicts reversion.

Regime gate:

- allow in sideways, high-volatility sideways and post-shock recovery;
- suppress in sustained trend, panic and rally states.

Compare regime-aware versus regime-unaware performance.

---

## 34. S08 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Cross-Ticker/Market Lead-Lag OFI

### Hypothesis

Market, sector or leader-ticker OFI improves prediction of follower tickers.

Possible hierarchy:

```text
market latent factor
  ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ sector factor
    ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ leader ticker
      ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ follower ticker
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

## 35. S09 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Queue-Imbalance Scalping

Use as a benchmark.

Test whether:

- next quote direction is predictable;
- prediction survives 50, 100, 250, 500 ms latency;
- expected move exceeds spread and costs.

Do not advance merely because classification accuracy is above 50%.

---

## 36. S10 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Passive Market Making

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

## 37. S11 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Spoof-Like Wall Filter

Use only as a risk feature:

- wall appearance;
- wall movement;
- cancellation before touch;
- repeated non-execution;
- temporary imbalance distortion.

Do not classify participants or assert market manipulation.

---

## Phase 12 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Backtest and Execution Simulator

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

## Phase 13 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Experiment Design

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

The first completed run created the planned 30/15/18 day split for each 63-day quarter profile, producing 189 split rows with `no_shuffle = true`. It created 30 seed-plan rows: 10 target seeds per quarter profile, with the first 3 seeds marked as initial engineering seeds. It also generated 48 walk-forward folds, 33 strategy/profile experiment-registry rows, 33 predeclared parameter-grid rows and 99 mandatory negative-control rows across S01ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“S11.

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

## Phase 14 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Validation of Synthetic Data Quality

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

## Phase 15 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Strategy Acceptance Gates

A strategy may advance from synthetic screening only if it passes all applicable gates.

## 54. Predictive gate

- stable sign of signal-response relationship;
- improvement over baseline;
- performance across seeds;
- no dependence on one ticker;
- no dependence on one event template.

## 55. Economic gate

- positive after realistic costs;
- survives 25ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ50% slippage increase;
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

## Phase 16 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Metrics and Reporting

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

## Phase 17 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Implementation Work Packages

## WP1 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Data intake and audit

Deliverables:

- schema detector;
- data-quality checks;
- sample-day profile;
- size report;
- canonical Parquet conversion.

## WP2 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Feature and event reconstruction

Deliverables:

- L1/L5 imbalance;
- MLOFI;
- trade classification;
- microprice;
- liquidity withdrawal;
- replenishment;
- book shape;
- regime-independent baseline features.

## WP3 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Regime/scenario framework

Deliverables:

- regime definitions;
- scenario YAML/JSON;
- daily calendar generator;
- intraday state generator;
- shock injector.

## WP4 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Price and cross-ticker simulator

Deliverables:

- market/sector/ticker factors;
- stochastic volatility;
- jump process;
- correlation controls;
- price-grid enforcement.

## WP5 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â L2 event simulator

Deliverables:

- additions/cancellations/trades;
- five-level reconstruction;
- resilience;
- spread/depth dynamics;
- activity seasonality.

## WP6 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Retail feed emulator

Deliverables:

- receive latency;
- batching;
- gaps;
- duplicates;
- reconnects;
- asynchronous ticker stream.

## WP7 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Storage pipeline

Deliverables:

- raw/delta/resampled Parquet;
- partitioning;
- compression benchmark;
- replay tool;
- metadata manifest.

## WP8 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Backtester

Deliverables:

- event-driven engine;
- market and limit orders;
- latency;
- partial fills;
- slippage;
- fees;
- risk controls.

## WP9 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Strategy suite

Deliverables:

- S01-S11 modules;
- shared feature interface;
- baseline strategies;
- parameter registry.

## WP10 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Validation and reporting

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

## Phase 18 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Suggested Technology Stack

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

## Phase 19 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Reproducibility

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

The current completed run audits 10 required reproducibility fields across 69 phase/workspace/dashboard/decision manifests, producing 690 field checks. Current native source-manifest coverage is complete for the audited artifact set: all 69 artifacts are exact-regeneration-ready at the source-manifest level, 0 artifacts have missing fields and 0 artifact groups have a missing/unreadable manifest. The exact-ready source manifests now include `stage_a1`, `phase1`, `phase1_event_reconstruction`, `stage_a2`, `stage_b1`, `stage_b2`, `stage_c`, `stage_d`, `stage_e`, `phase21`, `phase22`, `phase23`, `phase25`, `phase26`, `phase27`, `phase28`, `phase29`, `phase30`, `phase31`, `phase32`, `phase33`, `phase34`, `phase35`, `phase36`, `phase37`, `phase38`, `phase39`, `phase41`, `phase42`, `phase43`, `phase44`, `phase45`, `phase46`, `phase47`, `phase48`, `phase49`, `phase50`, `phase51`, `phase2`, `phase3`, `phase4`, `phase5`, `phase6`, `phase7`, `phase8`, `phase9`, `phase10`, `phase11`, `phase11_strategy_modules`, `phase12`, `phase12_event_backtest`, `phase13`, `phase13_smoke_run`, `phase14`, `phase15`, `phase16`, `phase17`, `phase18`, `phase20`, `phase20_m01`, `phase20_m02`, `phase20_m03`, `phase20_m04`, `phase20_m05`, `phase20_m06`, `phase20_m07`, `horizon_readiness`, `dashboard` and `duckdb`.

The remediation layer now emits a normalized reproducibility manifest template and 690 field-level remediation rows. All 690 rows are `complete_exact`, confirming that the audited source manifests now expose the exact required fields without generator-field, alias-normalization or recover/rerun gaps.

The normalized manifest overlay still creates exact-field manifest overlays for all 48 audited artifacts. The overlay now has 48 exact-field-ready artifacts and 480 normalized field rows, with all 480 values coming from exact/alias fields already present in source manifests and 0 values supplied by normalizer defaults. It is retained as an audit/inspection bridge, not as a substitute for source-manifest metadata.

Important Phase 19 caveat: this phase now proves native reproducibility metadata coverage for the 48 audited manifests, not byte-for-byte deterministic regeneration of every large Parquet/table artifact and not coverage for future artifact classes that are not yet registered in the Phase 19 manifest-candidate list. New phases or dashboards must be added to the audit candidate list and emit the same normalized manifest schema before they can be treated as exact-regeneration-ready.

The regression guardrail is `python scripts/run_reproducibility_gate.py`. It fails if the 44/44 native exact-ready invariant, zero missing/unreadable manifests, 44/44 normalized-overlay readiness, zero normalizer-default fields, or `complete_exact`-only remediation state regresses.

**Current Phase 20 implementation status as of 2026-07-14:** Phase 20 now has a runnable acceptance-hardening queue in `scripts/run_phase20_acceptance_hardening.py`, backed by `src/synthetic_l2/phase20_acceptance_hardening.py`. This is an execution-sequence and blocker-prioritization artifact, not a strategy-promotion result.

Generated Phase 20 artifacts are under `outputs/phase20/`:

- `phase20_acceptance_hardening_report.md`;
- `acceptance_hardening_manifest.json`;
- `acceptance_hardening_queue.csv`;
- `acceptance_hardening_gate_summary.csv`;
- `acceptance_hardening_strategy_summary.csv`;
- `acceptance_execution_roadmap.csv`;
- `acceptance_execution_milestones.csv`;
- `risk_hardening_plan.csv`;
- `risk_hardening_action_summary.csv`;
- `economic_hardening_plan.csv`;
- `economic_hardening_action_summary.csv`;
- `predictive_hardening_plan.csv`;
- `predictive_hardening_action_summary.csv`;
- `robustness_hardening_plan.csv`;
- `robustness_hardening_action_summary.csv`;
- `realism_hardening_plan.csv`;
- `realism_hardening_action_summary.csv`.

The current completed Phase 20 run converts the 50 Phase 15 blocker rows and Phase 17 proxy backlog into 50 ranked acceptance-hardening queue rows, 5 gate-summary rows and 11 strategy-summary rows. It also consolidates the five gate-specific hardening ledgers into `outputs/phase20/acceptance_execution_roadmap.csv`, a 411-row cross-gate execution roadmap, and `outputs/phase20/acceptance_execution_milestones.csv`, a 7-row milestone rollup spanning broker/external reconciliation, strategy support and registry closure, predictive model/baseline validation, full-seed/walk-forward robustness execution, full lifecycle risk/economic replay, holdout-generator/realism reruns and real multi-day acceptance validation. The roadmap currently has 259 proxy-backed rows, 152 rows missing required evidence, 9 met proxy-registration rows and 0 acceptance-ready rows. The highest-priority gate is `G04_risk`, with 11 blocked strategies, followed by `G02_economic`, `G01_predictive`, `G03_robustness` and `G05_realism`. Phase 20 now decomposes the top risk blocker into `outputs/phase20/risk_hardening_plan.csv`: 88 strategy/risk-requirement rows across broker/exchange fill provenance, contract-note/cost reconciliation, full-run coverage, daily equity/halt state, daily-loss validation, drawdown validation, position-limit validation and tail-loss validation. Of those rows, 54 have proxy evidence that must be upgraded into acceptance evidence, 34 still lack required evidence, 0 meet acceptance requirements and 0 are acceptance-ready. The companion `risk_hardening_action_summary.csv` groups the work into 6 action classes: guardrail validation, acceptance-run coverage, broker contract-note reconciliation, broker/exchange reconciliation, risk-state persistence and tail-risk validation. Phase 20 also decomposes the P2 economic blocker into `outputs/phase20/economic_hardening_plan.csv`: 88 strategy/economic-requirement rows across broker/exchange fill provenance, contract-note reconciliation, Zerodha order-formula readiness, latency/slippage stress confirmation, retail-and-stress net profitability, stressed-profile net profitability, risk-adjusted economic joint pass and multi-day real/holdout economic validation. Of those rows, 58 have proxy evidence that must be upgraded into acceptance evidence, 30 still lack required evidence, 0 meet acceptance requirements and 0 are acceptance-ready. The companion `economic_hardening_action_summary.csv` groups the work into 8 action/dependency rows covering broker contract-note reconciliation, broker/exchange fill reconciliation, documented cost-formula validation, holdout/real multi-day economic validation, latency/slippage acceptance replay, net-profitability validation and risk-adjusted economic validation. Phase 20 also decomposes the P3 predictive blocker into `outputs/phase20/predictive_hardening_plan.csv`: 99 strategy/predictive-requirement rows across strategy feature support, baseline outperformance, holdout-cell stability, untouched-test stability, feature stability, multi-seed walk-forward validation, calibrated model output, real multi-day holdout and promotion-falsification clearance. Of those rows, 58 have proxy evidence that must be upgraded into acceptance evidence, 41 still lack required evidence, 0 meet acceptance requirements and 0 are acceptance-ready. The companion `predictive_hardening_action_summary.csv` groups the work into 9 action classes covering baseline lift, calibrated model training, holdout cells, model feature stability, multi-seed walk-forward execution, promotion-falsification clearance, real multi-day predictive holdout, strategy feature-support closure and untouched-test validation. Phase 20 also decomposes the P4 robustness blocker into `outputs/phase20/robustness_hardening_plan.csv`: 88 strategy/robustness-requirement rows across strategy registry support, full required-seed execution, execution-profile robustness, negative-control rejection, parameter-neighborhood smoothness, walk-forward coverage, holdout-generator strategy reruns and real-data reruns. Of those rows, 71 have proxy evidence, 17 still lack required evidence, 9 meet the current proxy registration requirement and 0 are acceptance-ready. The companion `robustness_hardening_action_summary.csv` groups the work into 8 action classes covering execution-profile robustness, full-seed execution, holdout-generator reruns, negative controls, parameter smoothness, real-data reruns, walk-forward execution and strategy-registry support. Phase 20 also decomposes the P5 realism blocker into `outputs/phase20/realism_hardening_plan.csv`: 48 strategy/realism-requirement rows for the 6 realism-blocked strategies across synthetic quality gates, strategy support, holdout-generator coverage, feed-imperfection coverage, holdout strategy reruns, pessimistic execution realism, artifact-exploitation rejection and real multi-day realism validation. Of those rows, 18 have proxy evidence that must be upgraded into acceptance evidence, 30 still lack required evidence, 0 meet acceptance requirements and 0 are acceptance-ready. The companion `realism_hardening_action_summary.csv` groups the work into 8 action classes covering synthetic quality validation, strategy support closure, holdout-generator coverage, feed-imperfection coverage, holdout strategy reruns, pessimistic execution reruns, artifact controls and real multi-day realism validation. The queue has 0 acceptance-ready rows by design: it identifies the next evidence-producing work, not completed acceptance evidence. The dashboard and DuckDB workspace now register these Phase 20 outputs, and Phase 19 now audits the Phase 20 manifest as an exact-regeneration-ready source manifest.

Important Phase 20 caveat: the ranking is deterministic blocker triage based on current evidence, not an optimization proof. It should guide the next implementation sequence, but it does not relax any Phase 15 acceptance gate.

### Phase 20 M01 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Broker/external evidence contract

**Current implementation status as of 2026-07-14:** the first Phase 20 execution milestone now has a runnable broker/external evidence intake contract in `scripts/run_phase20_m01_broker_evidence_contract.py`, backed by `src/synthetic_l2/phase20_m01_broker_evidence_contract.py`. This milestone translates the M01 broker/external reconciliation roadmap rows into required files, required fields, reconciliation tests and gap ledgers. It is not acceptance evidence and does not make any strategy promotion-ready.

Generated Phase 20 M01 artifacts are under `outputs/phase20_m01/`:

- `phase20_m01_broker_evidence_contract_report.md`;
- `broker_evidence_contract_manifest.json`;
- `broker_evidence_import_checklist.csv`;
- `broker_evidence_schema.csv`;
- `broker_reconciliation_test_catalog.csv`;
- `broker_external_gap_ledger.csv`;
- `broker_external_gap_summary.csv`.

The current completed run defines 4 required broker/external evidence files: broker order/fill events, broker contract-note charge rows, strategy-order linkage rows and broker reconciliation tolerances. It also defines 40 required evidence-schema rows and 5 reconciliation tests covering order-lineage joins, fill-quantity matching, average-price matching, charge-component matching and net-obligation matching. The import checklist correctly records 0 of 4 broker/external files present in the workspace. The M01 gap ledger contains 44 strategy/gate/requirement rows across the Phase 20 broker/external reconciliation milestone: 22 risk-gate rows still require broker/exchange fill provenance or contract-note/cost reconciliation, 11 economic-gate rows still require broker/exchange fill provenance, and 11 economic-gate rows have current Zerodha formula proxy evidence but still require broker contract-note reconciliation and broker/exchange fill linkage. All 44 rows remain non-acceptance-ready, with 0 acceptance-met rows after the contract layer. This is the desired current result: the contract exists, the evidence is not yet imported, and the blocker remains explicit.

Important Phase 20 M01 caveat: the contract is an intake and validation specification. Broker/exchange records, contract notes and strategy-order linkage must still be captured or imported before the risk and economic gates can use this milestone as acceptance evidence.

### Phase 20 M02 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Strategy support and registry closure contract

**Current implementation status as of 2026-07-14:** the second Phase 20 execution milestone now has a runnable strategy-support and registry closure contract in `scripts/run_phase20_m02_strategy_support_contract.py`, backed by `src/synthetic_l2/phase20_m02_strategy_support_contract.py`. This milestone translates M02 roadmap rows into explicit strategy support decisions, acceptance criteria, support-gap summaries and per-strategy required actions. It is not acceptance evidence and does not make any strategy promotion-ready.

Generated Phase 20 M02 artifacts are under `outputs/phase20_m02/`:

- `phase20_m02_strategy_support_contract_report.md`;
- `strategy_support_contract_manifest.json`;
- `strategy_support_acceptance_criteria.csv`;
- `strategy_support_closure_ledger.csv`;
- `strategy_support_gap_summary.csv`;
- `strategy_support_decision_summary.csv`.

The current completed run defines 4 strategy-support acceptance criteria covering feature-product coverage, module-registry decisions, alpha-registry scope and support-evidence lineage. It produces 28 M02 closure rows across predictive, robustness and realism support blockers. Of those rows, 10 are runnable-proxy rows that require proxy-to-acceptance feature/module upgrades, 12 rows require feature engineering for partial strategies S03/S04/S06/S08, and 6 rows require explicit non-alpha classification or separate control registration for S10/S11. The strategy decision summary keeps S01/S02/S05/S07/S09 as proxy-supported but not acceptance-ready, marks S03/S04/S06/S08 as requiring missing plan features, and marks S10/S11 as requiring explicit research-only or risk-filter-only treatment before alpha-promotion workflows. All 28 rows remain non-acceptance-ready, with 0 acceptance-met rows after the contract layer.

Important Phase 20 M02 caveat: this contract clarifies the support work and classification decisions required before acceptance reruns. It does not implement the missing features, does not register S10/S11 as alpha strategies, and does not relax the Phase 15 promotion gate.

### Phase 20 M03 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Predictive validation contract

**Current implementation status as of 2026-07-14:** the third Phase 20 execution milestone now has a runnable predictive validation contract in `scripts/run_phase20_m03_predictive_validation_contract.py`, backed by `src/synthetic_l2/phase20_m03_predictive_validation_contract.py`. This milestone consolidates current Phase 16 baseline, holdout, feature-stability and promotion-falsification proxy diagnostics into an explicit predictive acceptance contract. It is not acceptance evidence and does not make any strategy promotion-ready.

Generated Phase 20 M03 artifacts are under `outputs/phase20_m03/`:

- `phase20_m03_predictive_validation_contract_report.md`;
- `predictive_validation_contract_manifest.json`;
- `predictive_validation_acceptance_criteria.csv`;
- `predictive_validation_ledger.csv`;
- `predictive_validation_gap_summary.csv`;
- `predictive_validation_strategy_summary.csv`.

The current completed run defines 6 predictive acceptance criteria covering calibrated model output, baseline lift, holdout-cell stability, untouched-test stability, feature stability and promotion-falsification clearance. It produces 66 predictive-validation rows across the 11 strategies and the 6 M03 requirements. All rows remain non-acceptance-ready. The ledger records 24 rows blocked by partial strategy support, 12 rows blocked by unsupported strategy scope, 5 runnable-proxy rows missing calibrated model artifacts, 5 runnable-proxy rows failing proxy baselines, 5 runnable-proxy rows failing holdout-cell checks, 5 runnable-proxy rows with untouched-test failures or missing evidence, 5 runnable-proxy rows with only proxy feature-stability evidence and 5 runnable-proxy rows falsified for predictive promotion. Current counts include 11 calibrated-model-required rows, 11 baseline-lift-required rows, 22 holdout/untouched-test rows, 11 promotion-falsification-required rows and 0 acceptance-met rows after the contract layer.

Important Phase 20 M03 caveat: this contract records predictive validation requirements and current blocker evidence. It does not train calibrated models, does not rerun multi-seed/walk-forward holdouts, does not clear the predictive promotion-falsification checklist and does not relax the Phase 15 promotion gate.

### Phase 20 M04 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Robustness execution contract

**Current implementation status as of 2026-07-14:** the fourth Phase 20 execution milestone now has a runnable robustness execution contract in `scripts/run_phase20_m04_robustness_execution_contract.py`, backed by `src/synthetic_l2/phase20_m04_robustness_execution_contract.py`. This milestone joins the M04 roadmap rows to current Phase 13 seed, walk-forward, parameter, execution-profile and negative-control proxy evidence. It is not acceptance evidence and does not make any strategy promotion-ready.

Generated Phase 20 M04 artifacts are under `outputs/phase20_m04/`:

- `phase20_m04_robustness_execution_contract_report.md`;
- `robustness_execution_contract_manifest.json`;
- `robustness_execution_acceptance_criteria.csv`;
- `robustness_execution_ledger.csv`;
- `robustness_execution_gap_summary.csv`;
- `robustness_execution_strategy_summary.csv`.

The current completed run defines 5 robustness execution acceptance criteria covering full validation seed coverage, walk-forward execution, parameter-neighborhood smoothness, execution-profile robustness and negative-control rejection. It produces 66 robustness-execution rows across the 11 strategies and the M04 requirements. All rows remain non-acceptance-ready. The ledger records 24 rows blocked by partial strategy support, 12 rows blocked by unsupported strategy scope, 5 predictive multi-seed/walk-forward prerequisite rows, 5 runnable-proxy rows with only initial-engineering seed coverage, 5 rows with walk-forward design available but not executed, 5 rows with only single-parameter proxy execution, 5 rows with execution-profile proxy evidence that is not acceptance-grade and 5 rows with incomplete or proxy-only negative-control evidence. Current counts include 22 full-seed-required rows, 22 walk-forward-required rows, 11 parameter-smoothness-required rows, 11 execution-profile-required rows, 11 negative-control-required rows and 0 acceptance-met rows after the contract layer.

Important Phase 20 M04 caveat: this contract records robustness execution requirements and current blocker evidence. It does not execute the full Phase 13 seed plan, does not run the walk-forward windows, does not expand parameter neighborhoods, does not replace proxy fills/costs with acceptance-grade execution evidence and does not relax the Phase 15 promotion gate.

### Phase 20 M05 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Lifecycle risk and economic replay contract

**Current implementation status as of 2026-07-14:** the fifth Phase 20 execution milestone now has a runnable lifecycle risk and economic replay contract in `scripts/run_phase20_m05_lifecycle_economic_replay_contract.py`, backed by `src/synthetic_l2/phase20_m05_lifecycle_economic_replay_contract.py`. This milestone joins the M05 roadmap rows to current Phase 12 lifecycle risk, risk-limit, cost and execution proxy evidence plus Phase 16 economic frontier and reconciliation summaries. It is not acceptance evidence and does not make any strategy promotion-ready.

Generated Phase 20 M05 artifacts are under `outputs/phase20_m05/`:

- `phase20_m05_lifecycle_economic_replay_contract_report.md`;
- `lifecycle_economic_replay_contract_manifest.json`;
- `lifecycle_economic_acceptance_criteria.csv`;
- `lifecycle_economic_replay_ledger.csv`;
- `lifecycle_economic_gap_summary.csv`;
- `lifecycle_economic_strategy_summary.csv`.

The current completed run defines 8 lifecycle/economic acceptance criteria covering full-run lifecycle coverage, daily equity/halt state, guardrail validation, tail-loss validation, documented Zerodha cost-formula validation, latency/slippage replay, net profitability and risk-adjusted economic joint pass. It produces 121 lifecycle/economic replay rows across the 11 strategies and the M05 requirements. All rows remain non-acceptance-ready. The ledger records 44 rows blocked by partial strategy support, 22 rows blocked by unsupported strategy scope, 30 lifecycle-risk proxy rows that are not acceptance-grade, 10 net-profitability proxy rows that are not acceptance-grade, 5 Zerodha-formula rows with broker contract-note reconciliation missing, 5 latency/slippage proxy rows that are not acceptance replay evidence and 5 risk-adjusted joint-pass rows that fail or are missing under current proxy evidence. Current counts include 66 risk-replay-required rows, 55 economic-replay-required rows, 11 broker-reconciliation-required rows, 33 guardrail-validation-required rows and 0 acceptance-met rows after the contract layer.

Important Phase 20 M05 caveat: this contract records lifecycle risk and economic replay requirements and current blocker evidence. It does not run an acceptance-grade event/tick lifecycle engine, does not reconcile broker/exchange fills or contract notes, does not convert proxy risk/economic rows into acceptance evidence and does not relax the Phase 15 promotion gate.

### Phase 20 M06 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Holdout generator and realism rerun contract

**Current implementation status as of 2026-07-14:** the sixth Phase 20 execution milestone now has a runnable holdout-generator and realism rerun contract in `scripts/run_phase20_m06_realism_rerun_contract.py`, backed by `src/synthetic_l2/phase20_m06_realism_rerun_contract.py`. This milestone joins the M06 roadmap rows to current Phase 14 quality/holdout realism diagnostics, Phase 13 robustness proxy evidence and Phase 11 strategy support metadata. It is not acceptance evidence and does not make any strategy promotion-ready.

Generated Phase 20 M06 artifacts are under `outputs/phase20_m06/`:

- `phase20_m06_realism_rerun_contract_report.md`;
- `realism_rerun_contract_manifest.json`;
- `realism_rerun_acceptance_criteria.csv`;
- `realism_rerun_ledger.csv`;
- `realism_rerun_gap_summary.csv`;
- `realism_rerun_strategy_summary.csv`.

The current completed run defines 6 holdout/realism rerun acceptance criteria covering synthetic quality gates, holdout-generator coverage, feed-imperfection coverage, holdout strategy reruns, pessimistic execution realism and artifact-exploitation rejection. It produces 47 holdout/realism rerun rows across the 11 strategies and the M06 requirements. All rows remain non-acceptance-ready. The ledger records 28 rows blocked by partial strategy support, 14 rows blocked by unsupported strategy scope and 5 runnable-proxy rows missing acceptance-grade holdout strategy rerun evidence. Current counts include 17 holdout-rerun-required rows, 6 quality-gate-required rows, 6 feed-imperfection-required rows, 6 pessimistic-execution-required rows, 6 artifact-control-required rows and 0 acceptance-met rows after the contract layer.

Important Phase 20 M06 caveat: this contract records holdout-generator and realism rerun requirements and current blocker evidence. It does not run strategy P&L/signal/risk reruns on holdout generator profiles, does not run pessimistic execution realism, does not run artifact controls and does not relax the Phase 15 promotion gate.

### Phase 20 M07 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Real multi-day acceptance validation contract

**Current implementation status as of 2026-07-14:** the seventh Phase 20 execution milestone now has a runnable real multi-day acceptance validation contract in `scripts/run_phase20_m07_real_multiday_acceptance_contract.py`, backed by `src/synthetic_l2/phase20_m07_real_multiday_acceptance_contract.py`. This milestone joins the M07 roadmap rows to current one-day real sample diagnostics, horizon-readiness evidence, Phase 16 economic/predictive summaries, Phase 13 robustness evidence, Phase 14 holdout realism evidence and Phase 20 M02 strategy-support decisions. It is not acceptance evidence and does not make any strategy promotion-ready.

Generated Phase 20 M07 artifacts are under `outputs/phase20_m07/`:

- `phase20_m07_real_multiday_acceptance_contract_report.md`;
- `real_multiday_acceptance_contract_manifest.json`;
- `real_multiday_acceptance_criteria.csv`;
- `real_multiday_acceptance_ledger.csv`;
- `real_multiday_gap_summary.csv`;
- `real_multiday_strategy_summary.csv`.

The current completed run defines 5 real multi-day acceptance criteria covering multi-day real data coverage, predictive real holdout validation, economic real validation, robustness real reruns and realism validation. It produces 39 real multi-day acceptance rows across the 11 strategies and the M07 requirements. All rows remain non-acceptance-ready. The ledger records 16 rows blocked by partial strategy support, 8 rows blocked by unsupported strategy scope, 5 runnable-proxy rows missing real multi-day economic validation, 5 runnable-proxy rows missing real multi-day predictive holdout validation and 5 runnable-proxy rows missing real multi-day robustness reruns. Current counts include 11 economic-real-validation rows, 11 predictive-real-holdout rows, 11 robustness-real-rerun rows, 6 realism-real-validation rows and 0 acceptance-met rows after the contract layer.

Important Phase 20 M07 caveat: this contract records final real multi-day acceptance requirements and current blocker evidence. It does not collect additional real market days, does not run multi-day real strategy validation, does not reconcile broker/exchange fills or costs and does not relax the Phase 15 promotion gate.

---

## Phase 20 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Initial Execution Sequence

### Stage A1 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Current one-day tick-stream audit

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

### Stage A2 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Capture-diagnostics and multi-day expansion

In parallel with initial one-day engineering:

1. continue subscription-driven collection under the Class B contract;
2. add or verify local sequences, connection boundaries and dropped-message diagnostics;
3. confirm actual callback cadence and timestamp semantics;
4. compact without resampling or losing event order;
5. capture at least 5ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ10 complete days for initial normal-day event calibration.

**Stage A2 exit gate:** at least 5ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ10 complete, diagnostically sound days are available for initial normal-day variability and event-model calibration. One-day feature/pipeline work may proceed before this gate, but strategy robustness or promotion claims may not.

**Current implementation status as of 2026-07-14:** Stage A2 now has a runnable capture-diagnostics and multi-day expansion contract in `scripts/run_stage_a2_capture_diagnostics_contract.py`, backed by `src/synthetic_l2/stage_a2_capture_diagnostics_contract.py`. This is a capture/readiness contract, not evidence that the multi-day gate has passed.

Generated Stage A2 artifacts are under `outputs/stage_a2/`:

- `stage_a2_capture_diagnostics_contract_report.md`;
- `stage_a2_capture_diagnostics_contract_manifest.json`;
- `capture_diagnostics_acceptance_criteria.csv`;
- `required_capture_schema.csv`;
- `capture_diagnostics_gap_ledger.csv`;
- `capture_diagnostics_gap_summary.csv`;
- `stage_a2_readiness_summary.csv`.

The current completed run defines 6 capture-diagnostic criteria covering multi-day Class B coverage, local sequence integrity, connection-boundary logging, dropped-message diagnostics, timestamp semantics and lossless compaction. It also defines 17 required capture-schema fields across capture-day manifests, connection-session ledgers, tick-sequence diagnostics, timestamp semantics and compaction reconciliation. The current one-day sample produces 192 open contract rows across 32 symbols and 6 criteria. All rows remain non-acceptance-ready: 32 rows each require multi-day capture, callback local-sequence evidence, connection-boundary ledgers, dropped-message diagnostics, timestamp-semantics contracts and repeatable multi-day lossless compaction. The readiness summary records 1 current sample day, 32 symbols, 620,853 rows, 32 symbols with at least one stale gap greater than 15 seconds and 0 acceptance-met rows.

Important Stage A2 caveat: this contract does not collect additional days and does not make strategy robustness or promotion claims. It makes the capture-side diagnostics explicit so future Class B days can be accepted or rejected consistently before recalibration and real multi-day validation.

### Stage B1 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Received-tick structural synthetic proof

Using the current Class B evidence, generate a small proof for:

- 5 instruments including at least one ETF;
- 5 normal days plus explicit trend and shock scenarios;
- five-level book states at a cadence no finer than the real evidence used for validation;
- deterministic replay, price-grid, spread, depth-ordering and storage checks.

Do not use Stage B1 to accept or reject S01ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œS11 profitability. Its purpose is generator engineering, received-tick feature verification and falsification of structural defects.

**Current implementation status as of 2026-07-14:** Stage B1 now has a runnable received-tick structural synthetic proof in `scripts/run_stage_b1_structural_synthetic_proof.py`, backed by `src/synthetic_l2/stage_b1_structural_synthetic_proof.py`. This is a generator-engineering structural proof, not profitability, robustness or strategy-promotion evidence.

Generated Stage B1 artifacts are under `outputs/stage_b1/`:

- `stage_b1_structural_synthetic_proof_report.md`;
- `stage_b1_structural_synthetic_proof_manifest.json`;
- `stage_b1_l2_book_subset_5m.parquet`;
- `stage_b1_development_subset.csv`;
- `stage_b1_structural_criteria.csv`;
- `stage_b1_scenario_coverage_summary.csv`;
- `stage_b1_structural_check_ledger.csv`.

The current completed run selects 5 development instruments: `ADANIPORTS`, `AXISBANK`, `BAJAJ-AUTO`, `BHARTIARTL` and `BANKBEES`, including 1 ETF. It preserves 70,875 five-level L2 book-state rows from the current Phase 6 five-minute synthetic book states. Scenario coverage includes 164 non-shock/reference days, 44 explicit trend days and 25 explicit shock days. All 7 structural checks pass: development subset, scenario coverage, five-level book columns, cadence no finer than the real evidence, price grid, spread/depth ordering and deterministic replay/storage. There are 0 failed structural checks.

Important Stage B1 caveat: this proof only verifies structural generator mechanics over a small development subset. It does not use Stage B1 to accept or reject S01-S11 profitability, and it does not replace the Stage A2 multi-day capture gate, Stage B2 event-driven proof, medium pilot, three-month study or real holdout gates.

### Stage B2 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Event-driven synthetic proof

Generate:

- the same 5-instrument development subset;
- 5 normal days;
- 2 trend days;
- 1 shock day;
- raw and 1-second/event-driven feature datasets for symbols and windows whose measured coverage supports that horizon.

**Current implementation status as of 2026-07-14:** Stage B2 now has a runnable event-driven synthetic proof in `scripts/run_stage_b2_event_driven_synthetic_proof.py`, backed by `src/synthetic_l2/stage_b2_event_driven_synthetic_proof.py`. This is a generator-engineering and horizon-scope proof, not strategy profitability, robustness or promotion evidence.

Generated Stage B2 artifacts are under `outputs/stage_b2/`:

- `stage_b2_event_driven_synthetic_proof_report.md`;
- `stage_b2_event_driven_synthetic_proof_manifest.json`;
- `stage_b2_raw_event_subset.parquet`;
- `stage_b2_event_feature_panel.parquet`;
- `stage_b2_event_driven_1s_features.parquet`;
- `stage_b2_event_driven_criteria.csv`;
- `stage_b2_development_readiness.csv`;
- `stage_b2_scenario_selection.csv`;
- `stage_b2_dataset_summary.csv`;
- `stage_b2_proof_check_ledger.csv`.

The current completed run uses the same 5 development instruments as Stage B1: `ADANIPORTS`, `AXISBANK`, `BAJAJ-AUTO`, `BHARTIARTL` and `BANKBEES`. It selects 8 explicit scenario rows: 5 normal days, 2 gradual-bullish-trend days and 1 shock/event day. It emits 15,061 raw synthetic event rows, 14,952 received-feed event-feature rows and 2,400 event-driven 1-second proof rows. The measured one-second readiness ledger allows event-driven 1-second rows only for `BHARTIARTL`; the other four development symbols are explicitly excluded from 1-second feature emission because their measured open-window coverage does not support that horizon. Dense 1-second readiness remains 0 symbols and Stage B2 makes 0 dense 1-second claims.

All 7 Stage B2 proof checks pass: development subset, scenario selection, raw event dataset, event-feature dataset, one-second scope, no dense one-second overclaim and deterministic replay/storage. There are 0 failed proof checks.

Important Stage B2 caveat: this proof validates event-driven artifact mechanics and horizon eligibility only. It does not validate S01-S11 profitability, does not create acceptance-grade one-second dense panels, and does not replace Stage A2 multi-day capture evidence, full event-level realism validation, medium/full pilot runs or real holdout gates.

This stage may start after Stage A1. Validate event-level and statistical realism against the current Class B day, but keep all strategy results preliminary and day-specific until Stage A2 and later holdout gates pass.

### Stage C ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Medium pilot

Generate:

- all 32 instruments;
- 20 trading days;
- 3 random seeds;
- multiple regimes.

Run S01-S05 and baseline strategies.

**Current implementation status as of 2026-07-14:** Stage C now has a runnable medium-pilot proxy in `scripts/run_stage_c_medium_pilot.py`, backed by `src/synthetic_l2/stage_c_medium_pilot.py`. This is medium-pilot engineering evidence over existing Phase 9 features, not strategy-promotion evidence.

Generated Stage C artifacts are under `outputs/stage_c/`:

- `stage_c_medium_pilot_report.md`;
- `stage_c_medium_pilot_manifest.json`;
- `stage_c_medium_pilot_feature_subset.parquet`;
- `stage_c_selected_trading_days.csv`;
- `stage_c_selected_seeds.csv`;
- `stage_c_dataset_summary.csv`;
- `stage_c_check_ledger.csv`;
- `stage_c_strategy_proxy_run_summary.csv`;
- `stage_c_baseline_proxy_run_summary.csv`.

The current completed run uses the Q-A medium-pilot slice with all 32 instruments, 20 selected trading days, 3 initial engineering seeds, 10 regime families, 2 market-shock days, 5 feed profiles and 239,173 Phase 9 Tier C feature rows. It emits 15 S01-S05 strategy/seed proxy summaries and 21 baseline/seed proxy summaries covering all registered baselines B01-B07. All 7 Stage C checks pass: all-32 instrument coverage, 20 trading days, 3 seeds, multiple regimes, S01-S05 strategy proxy runs, baseline proxy runs and non-acceptance scope. There are 0 failed Stage C checks and 0 acceptance-ready rows.

Important Stage C caveat: the current pilot uses 5-minute feature proxies and gross-return summaries. It does not replace full execution/cost/risk replay, multi-profile robustness, walk-forward validation, negative-control acceptance evidence, broker/exchange fill reconciliation or multi-day real holdout evidence.

### Stage D ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Three-month study

Generate:

- 32 instruments;
- 63 trading days;
- Q-A, Q-B and Q-C profile families;
- at least 3 seeds initially, later 10;
- raw compact L2 plus feature datasets.

Run all strategies, with S09-S11 treated as experimental controls.

**Current implementation status as of 2026-07-14:** Stage D now has a runnable three-month study proxy in `scripts/run_stage_d_three_month_study.py`, backed by `src/synthetic_l2/stage_d_three_month_study.py`. This is a three-month proxy/control study over existing Phase 9 products, not acceptance-grade strategy promotion evidence.

Generated Stage D artifacts are under `outputs/stage_d/`:

- `stage_d_three_month_study_report.md`;
- `stage_d_three_month_study_manifest.json`;
- `stage_d_profile_summary.csv`;
- `stage_d_seed_summary.csv`;
- `stage_d_data_product_inventory.csv`;
- `stage_d_dataset_summary.csv`;
- `stage_d_criteria.csv`;
- `stage_d_check_ledger.csv`;
- `stage_d_strategy_proxy_summary.csv`.

The current completed run covers all 32 instruments, all 3 quarter profiles (`Q-A`, `Q-B`, `Q-C`), 63 trading days per profile, 2,259,228 Phase 9 Tier C feature rows, 2,276,282 Phase 9 Tier A raw-event rows and 2,259,228 Phase 9 Tier B compact-L2 rows. It uses the current 9 initial engineering seeds, 3 per quarter profile, and explicitly tracks the later 30-row full-validation seed target as a remaining expansion gap. It emits 99 S01-S11 strategy/control proxy summaries across 11 strategy IDs and 9 initial seeds. S09-S11 are labelled as controls, non-alpha or risk-only rows, producing 27 control/risk rows. S10 and S11 are zero-trade non-alpha/risk-only controls under the current product rather than promotion candidates.

All 9 Stage D checks pass: all-32 instrument coverage, 63 days per profile, 3 quarter profiles, initial 3 seeds per profile, 10-seed expansion tracking, raw/compact/feature inventory, all-strategy proxy summaries, S09-S11 control labelling and non-acceptance scope. There are 0 failed Stage D checks and 0 acceptance-ready rows.

Important Stage D caveat: the current study is still a 5-minute proxy/control study. It does not replace full 10-seed execution, walk-forward result generation, parameter-neighborhood smoothness, full lifecycle execution/cost/risk replay, broker/exchange fill reconciliation, contract-note reconciliation, holdout-generator strategy reruns or multi-day real-data reruns.

### Stage E ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Full-year extension

Only after:

- synthetic-quality gates pass;
- backtest controls pass;
- storage is acceptable;
- strategy code is stable;
- results are not dependent on generator artifacts.

**Current implementation status as of 2026-07-14:** Stage E now has a runnable full-year extension readiness gate in `scripts/run_stage_e_full_year_readiness.py`, backed by `src/synthetic_l2/stage_e_full_year_readiness.py`. This gate does not run the full-year extension. It decides whether the current evidence permits starting one.

Generated Stage E artifacts are under `outputs/stage_e/`:

- `stage_e_full_year_readiness_report.md`;
- `stage_e_full_year_readiness_manifest.json`;
- `stage_e_readiness_criteria.csv`;
- `stage_e_prerequisite_ledger.csv`;
- `stage_e_gap_summary.csv`;
- `stage_e_required_action_plan.csv`.

The current completed readiness run has 7 prerequisite rows: 3 pass and 4 block. Synthetic quality currently passes with 0 fail rows and 0 warn rows. Full-year storage is currently acceptable under the configured conservative threshold, with the Phase 10 full-year conservative estimate at about 83.24 GB. Stage D proxy evidence is available and passing.

The full-year extension is not allowed yet. Blocking prerequisites are: 0 promoted strategies with 50 acceptance blockers still open; 0 promotion-ready or acceptance-grade strategy modules; 0 predictive promotion candidates; 88 open economic acceptance gaps; and 79 open robustness acceptance gaps. The action plan therefore requires clearing predictive, economic, robustness, risk and realism blockers, upgrading strategy modules from proxy to acceptance-grade, and running holdout-generator, walk-forward, full-seed and real-data reruns before treating results as non-generator-artifact evidence.

Important Stage E caveat: this is a readiness and blocker contract. It intentionally prevents full-year materialization until the plan's prerequisite gates pass.

---

## Phase 21 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Decision Framework after Three Months

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

**Current Phase 21 implementation status as of 2026-07-14:** Phase 21 now has a runnable post-three-month decision framework in `scripts/run_phase21_decision_framework.py`, backed by `src/synthetic_l2/phase21_decision_framework.py`.

Generated Phase 21 artifacts are under `outputs/phase21/`:

- `decision_rules.csv`;
- `decision_ledger.csv`;
- `decision_summary.csv`;
- `phase21_decision_framework_report.md`;
- `phase21_decision_framework_manifest.json`.

The current active decision is: **Improve or reject strategies; do not tune generator to create profit**. The framework evaluates all 9 plan decision rules, currently has 1 active current decision and has 0 extension/paper-ready rows. Rule `D21_01_no_strategy_survives_costs_latency` is active because current Phase 15 promoted strategies = 0 and Phase 16 risk-adjusted joint-pass rows = 0.

Important Phase 21 caveat: this is a decision-framework artifact, not strategy-promotion evidence and not permission to start the full-year extension.

---

## Phase 22 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Real Data Integration Roadmap

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
| 5ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ10 days | normal intraday variation |
| 20ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ30 days | basic regime calibration |
| 60 days | preliminary out-of-sample comparison |
| 3ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ6 months | meaningful strategy screening |
| 12+ months | stronger regime and robustness assessment |

Synthetic data should progressively become less assumption-driven as the real dataset grows.

**Current Phase 22 implementation status as of 2026-07-14:** Phase 22 now has a runnable real-data integration roadmap in `scripts/run_phase22_real_data_integration_roadmap.py`, backed by `src/synthetic_l2/phase22_real_data_integration_roadmap.py`.

Generated Phase 22 artifacts are under `outputs/phase22/`:

- `real_data_milestone_catalog.csv`;
- `recalibration_task_ledger.csv`;
- `capture_expansion_plan.csv`;
- `real_data_integration_summary.csv`;
- `phase22_real_data_integration_report.md`;
- `phase22_real_data_integration_manifest.json`.

The current completed run records 1 available real sample day, but 0 complete Class B event-grade days for Phase 22 milestones because Stage A2 still has open capture-contract rows and 0 acceptance-met rows. The current one-day sample therefore supports only schema/scale smoke checks, not event-flow recalibration. The roadmap emits 6 real-data milestone rows and 54 milestone/domain recalibration task rows across intraday curves, spread/depth distributions, regime frequencies, price-impact functions, trade/quote interaction, cross-ticker correlation, shocks/recovery, retail-feed latency and missing-data patterns. Current status: 0 milestones reached, 9 schema-smoke-only task rows, 0 event-flow recalibration-ready rows and 0 extension/paper-ready rows.

Important Phase 22 caveat: Class B event-grade milestones require diagnostically complete multi-day websocket L2 capture. Additional Class A or incomplete snapshot days may improve coarse checks but do not unlock the event-flow recalibration milestones.

---

## Phase 23 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Key Risks

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
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ synthetic multi-regime stress test
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ real-data historical test
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ live paper trading
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ shadow execution
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ very small capital
ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ gradual scale-up
```

**Current Phase 23 implementation status as of 2026-07-14:** Phase 23 now has a runnable key-risk register in `scripts/run_phase23_key_risk_register.py`, backed by `src/synthetic_l2/phase23_key_risk_register.py`.

Generated Phase 23 artifacts are under `outputs/phase23/`:

- `key_risk_register.csv`;
- `risk_mitigation_ledger.csv`;
- `promotion_path_guardrail.csv`;
- `key_risk_summary.csv`;
- `phase23_key_risk_register_report.md`;
- `phase23_key_risk_register_manifest.json`.

The current completed run records 5 key risks, 4 high-severity risks, 5 open acceptance-blocking risks, 31 mitigation rows and 7 governed promotion-path steps. The current promotion-ready count is 0. The register keeps synthetic alpha, one-day overfitting, unrealistic fills and false confidence from three months open as high-severity controls. Excessive data volume is lower-severity and currently mitigated/monitored by the Parquet/Zstandard plus DuckDB storage design, but it remains an acceptance-blocking operational control before larger materializations.

Important Phase 23 caveat: this is a governance/risk-control artifact. It does not close any promotion gate and does not permit skipping the staged path from synthetic engineering tests to real historical testing, paper trading, shadow execution, small capital and gradual scale-up.

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

Do not assume uniform 100 ms, 250 ms, 500 ms or 1 s support across symbols. Measure it. The sample may be used for day-specific S01ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œS11 falsification and pipeline tests, but not for robust acceptance or profitability claims.

### 24.2 Scope after the Class B multi-day gate passes

- all 32 instruments;
- at least 5ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ10 event-grade days for initial calibration, with continued collection;
- 63 synthetic trading days;
- three quarter profiles and three seeds per profile initially;
- state-changing event storage;
- 250 ms, 1 s and 5 s feature views only where supported by observed event density;
- S01ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œS08 as primary research;
- S09 as a latency benchmark;
- S10ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œS11 as experimental/risk-only modules;
- pessimistic execution assumptions;
- automated quality and strategy reports.

This staged scope preserves useful work from the current day without granting it event-level evidence it does not contain.

---

## Phase 25 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Event Replay Expansion

**Current Phase 25 implementation status as of 2026-07-14:** Phase 25 now has a runnable event-order strategy replay expansion in `scripts/run_phase25_event_replay_expansion.py`, backed by `src/synthetic_l2/phase25_event_replay_expansion.py`.

Generated Phase 25 artifacts are under `outputs/phase25/`:

- `event_replay_trade_ledger.parquet`;
- `event_replay_summary.csv`;
- `event_replay_risk_summary.csv`;
- `event_replay_baseline_comparison.csv`;
- `event_replay_overall_summary.csv`;
- `phase25_event_replay_report.md`;
- `phase25_event_replay_manifest.json`.

The current completed run replays S01, S02, S05, S07 and S09 plus baselines B01, B03 and B06 over the Stage B2 event-ordered feature product. It evaluates zero-latency control, retail-marketable-default and stressed-retail profiles with Zerodha equity-intraday order-formula charges applied where relevant. The run emits 113,848 event-order replay trade rows, 24 model/profile summary rows, 12 proxy risk-breach rows, 3 strategy/profile rows beating the best baseline proxy and 0 positive strategy/profile rows after costs. No row is acceptance-ready.

Important Phase 25 caveat: this is materially more execution-heavy than the prior contracts, but it is still an engineering replay over the Stage B2 development subset, not multi-day acceptance evidence and not a promotion result.

---

## Phase 26 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Strategy Salvage Scan

**Current Phase 26 implementation status as of 2026-07-14:** Phase 26 now has a runnable event-order parameter/filter salvage scan in `scripts/run_phase26_strategy_salvage_scan.py`, backed by `src/synthetic_l2/phase26_strategy_salvage_scan.py`.

Generated Phase 26 artifacts are under `outputs/phase26/`:

- `phase26_strategy_salvage_scan_report.md`;
- `phase26_strategy_salvage_scan_manifest.json`;
- `strategy_salvage_variant_catalog.csv`;
- `strategy_salvage_summary.csv`;
- `strategy_salvage_risk_summary.csv`;
- `strategy_salvage_baseline_comparison.csv`;
- `strategy_salvage_candidate_summary.csv`;
- `strategy_salvage_rejection_ledger.csv`;
- `strategy_salvage_overall_summary.csv`;
- local ignored heavy artifact: `strategy_salvage_trade_ledger.parquet`.

The current completed run registers 120 threshold/spread/liquidity variants across S01, S02, S05, S07 and S09, then replays them across the zero-latency, retail-marketable-default and stressed-retail execution profiles. It emits 542,406 local event-order replay trades and 282 variant/profile summary rows. The scan finds 17 positive rows only in the zero-latency control, 0 retail/stressed rows with positive mean net return after Zerodha-style costs, 204 rows that beat the best baseline proxy but still do not survive the realistic cost/risk filter, 0 realistic salvage-candidate rows and 282 rejected variant/profile rows.

Important Phase 26 caveat: this is useful execution-heavy rejection evidence, not acceptance evidence. The immediate implication is that simple threshold, spread and liquidity filtering does not currently rescue the Stage B2 event-order strategies under retail/stressed cost assumptions; deeper work should either redesign the signal family or obtain stronger real multi-day event data before promoting any variant.

---

## Phase 27 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Feature Edge Cost-Hurdle Scan

**Current Phase 27 implementation status as of 2026-07-14:** Phase 27 now has a runnable event-feature edge and cost-hurdle scan in `scripts/run_phase27_feature_edge_scan.py`, backed by `src/synthetic_l2/phase27_feature_edge_scan.py`.

Generated Phase 27 artifacts are under `outputs/phase27/`:

- `phase27_feature_edge_scan_report.md`;
- `phase27_feature_edge_scan_manifest.json`;
- `feature_edge_candidate_catalog.csv`;
- `feature_edge_summary.csv`;
- `feature_edge_risk_summary.csv`;
- `feature_edge_baseline_comparison.csv`;
- `feature_edge_candidate_summary.csv`;
- `feature_edge_family_summary.csv`;
- `feature_edge_rejection_ledger.csv`;
- `feature_edge_overall_summary.csv`;
- local ignored heavy artifact: `feature_edge_trade_ledger.parquet`.

The current completed run registers 112 feature/horizon/threshold candidates across short-horizon momentum, order-flow imbalance, top-of-book imbalance, depth imbalance, microprice pressure and mean-reversion variants. It evaluates 1-, 2-, 3- and 5-event horizons across zero-latency, retail-marketable-default and stressed-retail profiles. The run emits 1,213,296 local feature-edge replay trades and 336 candidate/profile summary rows. The scan finds 0 positive rows after costs, 0 realistic cost-clearing rows, 0 zero-latency edge-control rows, 336 rejected candidate/profile rows and 0 acceptance-ready rows.

Important Phase 27 caveat: this is signal-redesign diagnostic evidence, not acceptance evidence. It shows that the current simple signed event features do not clear even the basic execution-cost hurdle in the Stage B2 event product. The next research move should be feature redesign, richer event labels or stronger real multi-day capture, not further tuning of these raw signed feature signals.

---

## Phase 28 â€” Richer Event Label Support

**Current Phase 28 implementation status as of 2026-07-14:** Phase 28 now has a runnable richer event-label support layer in `scripts/run_phase28_richer_event_label_support.py`, backed by `src/synthetic_l2/phase28_richer_event_label_support.py`.

Generated Phase 28 artifacts are under `outputs/phase28/`:

- `phase28_richer_event_label_support_report.md`;
- `phase28_richer_event_label_support_manifest.json`;
- `feature_label_catalog.csv`;
- `event_label_summary.csv`;
- `lead_lag_proxy_summary.csv`;
- `strategy_support_upgrade_summary.csv`;
- `richer_event_label_overall_summary.csv`;
- local ignored heavy artifacts: `richer_event_label_panel.parquet` and `lead_lag_bucket_panel.parquet`.

The current completed run scans all 620,853 one-day received tick-delta rows across 32 symbols and engineers explicit weak market-by-price proxy labels for the four partial strategy families S03, S04, S06 and S08. It records 47,449 S03 liquidity-vacuum/reversal proxy rows, 38,481 S04 trade-flow plus depth-confirmation proxy rows, 71,244 S06 absorption-like replenishment proxy rows and 132,988 S08 cross-symbol lead-lag bucket rows. All 4 partial strategy families now have proxy feature labels engineered, producing 290,162 total proxy label rows or buckets, but 0 rows are acceptance-ready.

Important Phase 28 caveat: this closes a feature-engineering support gap, not a validation gate. The labels remain weak inferences from a market-by-price retail WebSocket feed; they do not prove true aggressor side, hidden liquidity, exact queue state, causal lead-lag or broker/exchange fills. Multi-day Class B capture, timestamp-skew/common-shock controls and acceptance-grade replay remain required before these partial strategies can be treated as promotable.

---

## Phase 29 — Partial Strategy Proxy Replay

**Current Phase 29 implementation status as of 2026-07-14:** Phase 29 now has a runnable proxy execution replay for the Phase 28 richer-label partial strategy families in `scripts/run_phase29_partial_strategy_proxy_replay.py`, backed by `src/synthetic_l2/phase29_partial_strategy_proxy_replay.py`.

Generated Phase 29 artifacts are under `outputs/phase29/`:

- `phase29_partial_strategy_proxy_replay_report.md`;
- `phase29_partial_strategy_proxy_replay_manifest.json`;
- `partial_strategy_proxy_summary.csv`;
- `partial_strategy_proxy_risk_summary.csv`;
- `partial_strategy_proxy_peer_comparison.csv`;
- `partial_strategy_proxy_candidate_summary.csv`;
- `partial_strategy_proxy_overall_summary.csv`;
- local ignored heavy artifact: `partial_strategy_proxy_trade_ledger.parquet`.

The current completed run converts the Phase 28 weak proxy labels for S03, S04, S06 and S08 into executable replay signals across the zero-latency, retail-marketable-default and stressed-retail profiles. It emits 742,623 local partial-strategy proxy replay trades and 12 strategy/profile rows. The run finds 0 positive rows after costs, 0 retail/stressed positive rows, 0 proxy candidate rows and 0 acceptance-ready rows. Even the zero-latency control rows remain negative after spread/slippage costs, so the richer proxy labels improve feature coverage but do not yet create a cost-surviving strategy signal.

Important Phase 29 caveat: this is execution-heavy rejection evidence for weak proxy labels, not acceptance evidence. The next useful research move is not to promote S03/S04/S06/S08; it is to require multi-day Class B labels, better causal controls, calibrated models, and broker/exchange fill/cost reconciliation before any partial-family strategy can re-enter promotion consideration.

---

## Phase 30 — Strategy Decision Triage

**Current Phase 30 implementation status as of 2026-07-14:** Phase 30 now has a runnable execution-evidence triage layer in `scripts/run_phase30_strategy_decision_triage.py`, backed by `src/synthetic_l2/phase30_strategy_decision_triage.py`.

Generated Phase 30 artifacts are under `outputs/phase30/`:

- `strategy_family_decision_ledger.csv`;
- `strategy_family_execution_evidence_summary.csv`;
- `strategy_redesign_queue.csv`;
- `strategy_rejection_or_redesign_overall_summary.csv`;
- `phase30_strategy_decision_triage_report.md`;
- `phase30_strategy_decision_triage_manifest.json`.

The current completed run aggregates Phase 25, Phase 26, Phase 27, Phase 28 and Phase 29 evidence into a strategy-family verdict table. It triages 11 strategy/control families: 9 alpha families and 2 non-alpha/risk-control families. The execution-led outcome is deliberately conservative and concrete: 9 alpha families are rejected in their current form or marked redesign-only, 2 rows are classified as non-alpha controls, 0 rows are promotion-ready, 0 rows are acceptance-ready, 0 rows have realistic positive execution evidence and 0 rows are current candidates.

The Phase 30 redesign queue prevents more compute from being spent on current-form signals that repeatedly fail costs. S05, S07 and S09 retain a medium-priority redesign path only because Phase 26 found tiny zero-latency positive controls that did not survive realistic costs; S03, S04, S06 and S08 retain a medium-priority label-redesign path because Phase 28 produced proxy labels but Phase 29 showed those proxies do not survive execution. S01 and S02 move to low-priority redesign unless a materially new event-level hypothesis appears. S10 and S11 remain non-alpha/risk plumbing and should not enter the alpha promotion queue.

Important Phase 30 caveat: this is a decision-triage artifact, not a new acceptance run. It answers the current execution question by saying that no existing strategy form should be promoted. The next useful execution work is either to design a materially new cost-aware event signal, or to expand real multi-day Class B/broker evidence before retesting partial-family labels.

---

## Phase 31 — Redesign Evidence Contract

**Current Phase 31 implementation status as of 2026-07-15:** Phase 31 now has a runnable redesign evidence contract in `scripts/run_phase31_redesign_evidence_contract.py`, backed by `src/synthetic_l2/phase31_redesign_evidence_contract.py`.

Generated Phase 31 artifacts are under `outputs/phase31/`:

- `strategy_redesign_spec_catalog.csv`;
- `redesign_evidence_contract_ledger.csv`;
- `replay_expansion_gate.csv`;
- `redesign_evidence_contract_overall_summary.csv`;
- `phase31_redesign_evidence_contract_report.md`;
- `phase31_redesign_evidence_contract_manifest.json`.

The current completed run converts the Phase 30 reject/redesign verdict into a no-replay-until contract for the 9 rejected alpha strategy families. It emits 9 strategy redesign specs and 44 explicit evidence requirements. All 44 requirements are currently open, 0 strategy rows are allowed back into replay expansion, 9 rows remain replay-blocked and 0 rows are acceptance-ready.

The contract is intentionally execution-protective. It prevents more compute from being spent on current-form strategies that have already failed realistic costs. Required evidence includes 7 acceptance-grade label-engineering requirements, 3 broker/fill/cost reconciliation requirements and 9 execution-economics requirements, plus signal-design, feature-engineering, real-data, robustness and timestamp/data-quality requirements where relevant.

Important Phase 31 caveat: this is not a strategy promotion result. It is the opposite: a machine-readable gate saying that further replay expansion is blocked until the relevant redesign evidence exists. The next useful work is to satisfy one or more Phase 31 contract rows with real multi-day labels, broker/fill evidence, or a materially new cost-aware signal thesis.

---

## Phase 32 — Contract Evidence Scanner

**Current Phase 32 implementation status as of 2026-07-15:** Phase 32 now has a runnable contract evidence scanner in `scripts/run_phase32_contract_evidence_scanner.py`, backed by `src/synthetic_l2/phase32_contract_evidence_scanner.py`.

Generated Phase 32 artifacts are under `outputs/phase32/`:

- `contract_evidence_scan_ledger.csv`;
- `evidence_availability_summary.csv`;
- `evidence_acquisition_queue.csv`;
- `strategy_evidence_scan_summary.csv`;
- `contract_evidence_scan_overall_summary.csv`;
- `phase32_contract_evidence_scanner_report.md`;
- `phase32_contract_evidence_scanner_manifest.json`.

The current completed run scans all 44 Phase 31 contract rows against current workspace artifacts. It records 35 rows with some proxy, partial or negative evidence already present, but it marks 0 rows acceptance-met and 0 rows replay-allowed. This is the correct conservative outcome: current evidence can guide redesign work, but it does not satisfy the no-replay-until contract.

The scan separates available-but-not-acceptance evidence from truly missing evidence. Phase 28 weak labels support label/lead-lag feature awareness but not acceptance-grade labels. Phase 1 received-delta summaries support feature-engineering direction but not redesigned strategy features. Phase 16 and Phase 20 M01 show Zerodha formula and broker-evidence schemas exist, but actual broker fills, contract notes, strategy-order linkage and reconciliation tolerances remain missing. Stage A2 confirms only one current sample day is available against the multi-day Class B requirement.

The Phase 32 evidence acquisition queue now gives concrete next actions: import external broker evidence, collect or import multi-day Class B real tick data, upgrade proxy labels/features to acceptance-grade artifacts, write new cost-aware signal theses, and avoid replaying current-form strategies until expected edge clears cost and latency hurdles.

Important Phase 32 caveat: this scanner is an evidence-discovery and acquisition-priority artifact, not an acceptance run. It reduces uncertainty about what already exists, while preserving the Phase 31 replay block.

---

## Phase 33 — Broker Evidence Intake

**Current Phase 33 implementation status as of 2026-07-15:** Phase 33 now has a runnable broker evidence intake package in `scripts/run_phase33_broker_evidence_intake.py`, backed by `src/synthetic_l2/phase33_broker_evidence_intake.py`.

Generated Phase 33 artifacts are under `outputs/phase33/`:

- `broker_evidence_template_inventory.csv`;
- `broker_evidence_file_validation.csv`;
- `broker_reconciliation_test_readiness.csv`;
- `broker_evidence_intake_overall_summary.csv`;
- `phase33_broker_evidence_intake_report.md`;
- `phase33_broker_evidence_intake_manifest.json`;
- template CSVs under `outputs/phase33/broker_evidence_templates/`.

The current completed run generates 4 broker evidence templates for `broker_order_fill_events`, `broker_contract_note_charges`, `strategy_order_linkage` and `broker_reconciliation_tolerances`. It checks the corresponding expected external paths under `external_broker_evidence/` and finds 0 files present, 0 import-ready files and 4 missing files. All 5 broker reconciliation tests remain blocked until the required external files are populated and pass schema validation.

The template files are intentionally generated under `outputs/phase33/`, not under `external_broker_evidence/`, so they cannot be mistaken for real broker evidence. Once actual broker/export files are placed in the expected external paths, rerunning Phase 33 will validate required columns, row counts and reconciliation-test readiness before any broker evidence can be treated as acceptance material.

Important Phase 33 caveat: this closes the import-packaging gap, not the broker-evidence gap. No broker fills, contract notes, strategy-order linkage or reconciliation tolerances are currently imported.

## Phase 34 — Real Data Multi-Day Readiness

**Current Phase 34 implementation status as of 2026-07-15:** Phase 34 now has a runnable real-data multi-day readiness inventory in `scripts/run_phase34_real_data_multiday_readiness.py`, backed by `src/synthetic_l2/phase34_real_data_multiday_readiness.py`.

Generated Phase 34 artifacts are under `outputs/phase34/`:

- `symbol_day_real_data_coverage.csv`
- `real_data_day_inventory.csv`
- `multiday_real_data_readiness_summary.csv`
- `multiday_real_data_acquisition_plan.csv`
- `phase34_real_data_multiday_readiness_report.md`
- `phase34_real_data_multiday_readiness_manifest.json`

The current Phase 34 run detected one local raw full-universe day: `2026-07-13` on `NSE`, with 32 symbols, 50,205 parquet files, 1,764,005,784 bytes and 620,853 Phase 1 delta rows. This proves the local websocket-derived sample is materially richer than minute bars and is suitable for schema, inventory and smoke/regression use.

Acceptance readiness remains blocked: Phase 34 reports 0 Class B event-grade days, a minimum requirement of 5 complete days, a target of 10 complete days, 5 additional Class B days needed for the minimum, 10 additional Class B days needed for the target, 192 open Stage A2 capture-diagnostics contract rows and 0 replay-allowed rows. The current raw full-universe day must not be promoted into strategy acceptance evidence until the Stage A2 connection-boundary, dropped-message, local-sequence, lossless-compaction and timestamp-semantics diagnostics pass for each collected day/symbol.

The Phase 34 acquisition plan is therefore execution-directed rather than theoretical: collect/import the missing Class B days, close the Stage A2 diagnostics for those days, expand toward the 10-day target, and preserve the current raw day as a regression/smoke day without overstating acceptance readiness.

## Phase 35 — Stage A2 Computable Diagnostics

**Current Phase 35 implementation status as of 2026-07-15:** Phase 35 now has a runnable Stage A2 computable diagnostic scanner in `scripts/run_phase35_stage_a2_computable_diagnostics.py`, backed by `src/synthetic_l2/phase35_stage_a2_computable_diagnostics.py`.

Generated Phase 35 artifacts are under `outputs/phase35/`:

- `symbol_day_computable_diagnostics.csv`
- `stage_a2_computable_contract_evidence_ledger.csv`
- `stage_a2_computable_diagnostics_summary.csv`
- `stage_a2_collector_instrumentation_action_plan.csv`
- `phase35_stage_a2_computable_diagnostics_report.md`
- `phase35_stage_a2_computable_diagnostics_manifest.json`

The current Phase 35 run scans the audited Stage A1/Phase 1 evidence for the local raw day and covers 32 symbols, 620,853 raw rows and 50,205 source files. It finds 32/32 symbols with computable timestamp-semantics checks passing, 32/32 symbols with raw-to-Phase1/manifest reconciliation passing and 32/32 symbols where duplicate/stale symptom scanning is computable.

Phase 35 also explains why the data still cannot be promoted to Class B acceptance evidence: 0 symbols have explicit callback-ingress local sequence IDs, 0 symbols have connection-boundary ledger evidence and 0 criterion rows are accepted for Class B promotion. The next implementation work is collector instrumentation: persist a session boundary ledger, persist a monotonic callback local sequence ID before parquet writes, persist broker/session dropped-message counters and rerun the computable diagnostics on every newly collected day.

## Phase 36 — Collector Instrumentation Package

**Current Phase 36 implementation status as of 2026-07-15:** Phase 36 now provides an importable collector instrumentation helper in `src/synthetic_l2/collector_instrumentation.py` and a runnable package generator in `scripts/run_phase36_collector_instrumentation_package.py`, backed by `src/synthetic_l2/phase36_collector_instrumentation_package.py`.

Generated Phase 36 artifacts are under `outputs/phase36/`:

- `collector_instrumentation_required_schema.csv`
- `collector_instrumentation_interface_catalog.csv`
- `collector_instrumentation_integration_checklist.csv`
- `collector_instrumentation_package_summary.csv`
- `dry_run_ledgers/session_ledger.csv`
- `dry_run_ledgers/tick_sequence_diagnostics.csv`
- `dry_run_ledgers/drop_counter_ledger.csv`
- `phase36_collector_instrumentation_package_report.md`
- `phase36_collector_instrumentation_package_manifest.json`

The package directly targets the Phase 35 gaps. The `CollectorInstrumentation` helper exposes `open_session`, `enrich_ticks`, `record_drop_counters`, `close_session` and `flush` so the live Zerodha websocket collector can persist connection/session boundaries, callback-local tick sequence IDs, callback receive timestamps and per-symbol dropped/duplicate/stale/out-of-order counters.

The current Phase 36 dry run produces 21 required schema fields, 1 session-ledger row, 3 local sequence diagnostic rows and 2 drop-counter rows. This is implementation scaffolding and dry-run proof only: `phase36_live_collector_integrated` remains 0 and `phase36_class_b_capture_enabled` remains 0 until the actual live collector imports this helper and emits these ledgers beside new raw parquet captures.

## Phase 37 — Collector Ledger Verifier

**Current Phase 37 implementation status as of 2026-07-16:** Phase 37 now has a runnable collector-ledger verifier in `scripts/run_phase37_collector_ledger_verifier.py`, backed by `src/synthetic_l2/phase37_collector_ledger_verifier.py`.

Generated Phase 37 artifacts are under `outputs/phase37/`:

- `schema_validation.csv`
- `session_validation.csv`
- `sequence_validation.csv`
- `drop_counter_validation.csv`
- `promotion_gate.csv`
- `summary.csv`
- `phase37_collector_ledger_verifier_report.md`
- `phase37_collector_ledger_verifier_manifest.json`

The current Phase 37 run verifies the Phase 36 dry-run ledgers and proves the verifier mechanics: 0 schema columns are missing, the session-boundary gate passes, the local-sequence gate passes and the drop-counter coverage gate passes. The live-evidence gate remains 0 because the input is dry-run scaffolding, not actual Zerodha collector output; therefore `phase37_stage_a2_collector_evidence_ready` remains 0.

This phase gives the future live collector a deterministic acceptance harness: once real collector ledgers are emitted beside new raw parquet captures, rerun Phase 37 with `--collector-source live_collector` and the live ledger paths. Only then can the collector-side Stage A2 evidence become eligible for Class B promotion checks.

## Phase 38 — Class B Day Promotion Gate

**Current Phase 38 implementation status as of 2026-07-16:** Phase 38 now has a runnable Class B day promotion gate in `scripts/run_phase38_class_b_promotion_gate.py`, backed by `src/synthetic_l2/phase38_class_b_promotion_gate.py`.

Generated Phase 38 artifacts are under `outputs/phase38/`:

- `class_b_promotion_summary.csv`
- `class_b_day_decision.csv`
- `class_b_promotion_gate_ledger.csv`
- `class_b_promotion_action_plan.csv`
- `phase38_class_b_promotion_gate_report.md`
- `phase38_class_b_promotion_gate_manifest.json`

The current Phase 38 run evaluates the `2026-07-13` `NSE` raw full-universe day against six promotion gates. Four gates pass: raw full-universe coverage, computable timestamp semantics, computable lossless compaction and computable duplicate/stale symptom scanning. Two gates fail: live collector evidence and collector Stage A2 evidence readiness. Therefore the day remains blocked with `class_b_promotion_allowed=False`, 4 passed gates, 2 failed gates, 0 promoted Class B days, 5 days still needed for the minimum and 10 days still needed for the target.

This is now the executable boundary between real-data capture and strategy replay: strategy replay remains blocked until live collector ledgers pass Phase 37 and this Phase 38 gate promotes enough Class B days.

## Phase 39 — Synthetic-Only Acceptance Path

**Current Phase 39 implementation status as of 2026-07-16:** Phase 39 now has a runnable synthetic-only acceptance path in `scripts/run_phase39_synthetic_only_acceptance_path.py`, backed by `src/synthetic_l2/phase39_synthetic_only_acceptance_path.py`.

Generated Phase 39 artifacts are under `outputs/phase39/`:

- `synthetic_only_acceptance_summary.csv`
- `synthetic_only_acceptance_policy.csv`
- `synthetic_only_gate_ledger.csv`
- `synthetic_only_strategy_decision.csv`
- `synthetic_only_experiment_queue.csv`
- `phase39_synthetic_only_acceptance_path_report.md`
- `phase39_synthetic_only_acceptance_path_manifest.json`

This phase records the explicit path selected for the current experiment program: Zerodha fills and broker contract notes are not available, so they are deferred only for synthetic-only experiments. This unlocks synthetic experiment continuation and redesign diagnostics, but it does not waive broker evidence for paper/live readiness and it does not promote current strategies.

The current Phase 39 run allows 11 strategy/control families to continue under a synthetic-only scope, with 9 alpha families having current synthetic/proxy replay artifacts. It records 3 broker-evidence blockers as deferred only inside the synthetic experiment scope. It keeps `phase39_synthetic_strategy_acceptance_ready=0`, `phase39_paper_or_live_acceptance_ready=0` and `phase39_realistic_positive_strategy_rows=0`, because Phase 25 and Phase 29 still show no realistic positive after-cost strategy rows.

The active acceptance semantics are therefore:

| Path | Current state | Meaning |
| --- | --- | --- |
| Synthetic experiment continuation | Allowed | Run redesign diagnostics, synthetic replay plumbing and cost-aware hypothesis work. |
| Synthetic strategy acceptance | Blocked | No current alpha strategy clears realistic positive after-cost evidence. |
| Paper/live broker acceptance | Blocked | Zerodha fills, contract notes and broker reconciliation remain required. |
| Real Class B multi-day acceptance replay | Blocked | Phase 38 has 0 promoted Class B days. |

This phase is the executable boundary that prevents missing broker evidence from freezing synthetic research while also preventing synthetic fills from being reported as real broker acceptance evidence.

## Phase 41 — Immediate Full-Year Synthetic Tick Experiment

**Current Phase 41 implementation status as of 2026-07-16:** Phase 41 now has a runnable immediate full-year synthetic tick/event trade-ledger experiment in `scripts/run_phase41_full_year_synthetic_tick_experiment.py`, backed by `src/synthetic_l2/phase41_full_year_synthetic_tick_experiment.py`.

Generated Phase 41 artifacts are under `outputs/phase41/`:

- `full_year_synthetic_tick_experiment_summary.csv`
- `full_year_synthetic_tick_experiment_results.csv`
- `full_year_synthetic_tick_experiment_realistic_results.csv`
- `full_year_synthetic_tick_experiment_daily_path_sample.csv`
- `phase41_full_year_synthetic_tick_experiment_report.md`
- `phase41_full_year_synthetic_tick_experiment_manifest.json`

This phase was added to answer the immediate execution question: what do the existing synthetic tick/event replay ledgers imply at a 252-trading-day full-year horizon? It loads the Phase 25, Phase 26, Phase 27 and Phase 29 synthetic trade ledgers, aggregates daily P&L by model/profile, and deterministically cycles the observed daily tick-ledger paths into a 252-day synthetic year. It is therefore a full-year tick-trade-ledger replay result, not a newly generated independent 252-day L2 universe and not acceptance evidence.

The current Phase 41 run loads 2,612,173 synthetic tick/event trade rows across 4 replay sources, builds 4,865 daily source rows and evaluates 654 model/profile full-year experiment rows. It finds 17 annualized positive rows across all profiles, but all profitable rows are zero-latency/control-like profiles. Under realistic retail/stressed profiles, 0 model/profile rows are profitable. The best all-profile annualized net P&L is approximately `1185737.54` INR, while the best realistic retail/stressed annualized net P&L remains negative at approximately `-32855.64` INR. `phase41_synthetic_full_year_acceptance_ready` remains 0.

The immediate interpretation is blunt: synthetic-only full-year replay can now produce annual-scale results, but the current strategy forms still do not clear realistic Zerodha-style cost/latency profiles.

## Phase 42 — Native Full-Year Synthetic L2 Experiment

**Current Phase 42 implementation status as of 2026-07-16:** Phase 42 now has a runnable native 252-trading-day synthetic L2 experiment in `scripts/run_phase42_native_full_year_l2_experiment.py`, backed by `src/synthetic_l2/phase42_native_full_year_l2_experiment.py`.

Generated Phase 42 artifacts are under `outputs/phase42/`:

- `native_full_year_l2_event_state.parquet`
- `native_full_year_l2_experiment_summary.csv`
- `native_full_year_strategy_results.csv`
- `native_full_year_daily_pnl.csv`
- `native_full_year_trade_sample.parquet`
- `phase42_native_full_year_l2_experiment_report.md`
- `phase42_native_full_year_l2_experiment_manifest.json`

This phase is the native full-year run that supersedes the Phase 41 annualized replay for the immediate experiment question. It expands the existing 189-day Phase 9 Tier B compact L2 event-state universe into a deterministic 252-trading-day synthetic year, recomputes event features on the annual event stream and runs S01/S02/S05/S07/S09 directly over the generated tick/event rows using the Phase 12 execution profiles and Zerodha-style cost model.

The current Phase 42 run generates 3,012,294 synthetic L2 event-state rows across 252 synthetic trading days, 32 symbols and 5 feed profiles. It evaluates 15 strategy/profile rows and simulates 6,846,221 strategy trades. No strategy/profile row is annual-P&L positive, including zero-latency controls. Under realistic retail/stressed profiles, 0 rows are profitable. The best all-profile annual net P&L is approximately `-4337116.65` INR, and the best realistic retail/stressed annual net P&L is approximately `-22101469.61` INR. `phase42_synthetic_full_year_acceptance_ready` remains 0.

This result is the strongest current synthetic-only evidence: at native full-year L2 event scale, the current strategy forms are rejected economically under the configured cost/latency model.

## Phase 43 — Native Full-Year Cost-Aware Salvage Scan

**Current Phase 43 implementation status as of 2026-07-16:** Phase 43 now has a runnable native full-year cost-aware salvage scan in `scripts/run_phase43_native_full_year_cost_salvage_scan.py`, backed by `src/synthetic_l2/phase43_native_full_year_cost_salvage_scan.py`.

Generated Phase 43 artifacts are under `outputs/phase43/`:

- `cost_salvage_summary.csv`
- `cost_salvage_variant_catalog.csv`
- `cost_salvage_variant_results.csv`
- `cost_salvage_strategy_rollup.csv`
- `phase43_native_full_year_cost_salvage_scan_report.md`
- `phase43_native_full_year_cost_salvage_scan_manifest.json`

This phase scans sparse/high-confidence variants over the Phase 42 native 252-day synthetic L2 event stream. It varies signal thresholds, spread gates and liquidity floors for S01/S02/S05/S07/S09 and reruns the Phase 12 execution profiles and Zerodha-style costs. The goal is to test whether churn reduction and tighter entry filters can rescue the full-year economics after Phase 42 rejected the base strategy forms.

The current Phase 43 run scans 60 variants and 180 variant/profile rows over 3,012,294 native full-year L2 event rows. It simulates 5,027,566 variant trades. Four annual-positive rows appear, but all four are zero-latency/control rows. Under realistic retail/stressed profiles, 0 rows are annual-positive and 0 rows qualify for deeper synthetic replay. The best all-profile annual net P&L is approximately `85087.07` INR, while the best realistic retail/stressed annual net P&L remains negative at approximately `-184924.47` INR. `phase43_synthetic_full_year_acceptance_ready` remains 0.

The immediate conclusion is that tighter thresholds and cost-aware filters reduce losses materially, but they do not produce a realistic-cost survivor. The next research move should be new signal/label design rather than more promotion work on the current signal families.

## Phase 44 — Native Full-Year Forward Edge Label Mining

**Current Phase 44 implementation status as of 2026-07-16:** Phase 44 now has a runnable native full-year forward-edge label mining pass in `scripts/run_phase44_native_full_year_forward_edge_label_mining.py`, backed by `src/synthetic_l2/phase44_native_full_year_forward_edge_label_mining.py`.

Generated Phase 44 artifacts are under `outputs/phase44/`:

- `forward_edge_label_mining_summary.csv`
- `forward_edge_label_candidate_catalog.csv`
- `forward_edge_label_mining_results.csv`
- `forward_edge_label_thesis_rollup.csv`
- `phase44_native_full_year_forward_edge_label_mining_report.md`
- `phase44_native_full_year_forward_edge_label_mining_manifest.json`

This phase responds to the Phase 43 conclusion that more tuning of the current strategy variants is unlikely to be useful. Instead of promoting another current-form strategy, it mines the Phase 42 native 252-day synthetic L2 event stream for forward labels that can clear a retail Zerodha-style hurdle before execution replay. It tests 10 feature theses across forward event horizons, signal-strength thresholds and spread gates, using current L2 features such as momentum, MLOFI, microprice deviation and level-1/level-5 imbalance.

The current Phase 44 run labels 3,012,294 native full-year L2 event rows and evaluates 240 feature/threshold/spread/horizon candidates with 21,863,842 total feature-threshold signals. It finds 0 replay-candidate rows under the conservative pre-replay rule. The best mean signed forward return after the retail hurdle is approximately `0.003143`, the best directional precision is approximately `0.54123`, and the best precision lift versus the baseline any-edge rate is only approximately `1.02448`, below the configured replay-candidate threshold of `1.25`. `phase44_synthetic_full_year_acceptance_ready` remains 0.

The immediate conclusion is that extreme one-event momentum-fade labels show some raw mean edge in the synthetic stream, but not enough precision lift over the broad baseline edge rate to justify a new full execution replay yet. The next design step should be a more selective label contract: condition the best momentum-fade family by regime, symbol class, event intensity and feed-quality state before replay.

## Phase 45 — Raw Synthetic L2 Tick-Lake Materialization

**Current Phase 45 implementation status as of 2026-07-16:** Phase 45 now has a runnable raw Zerodha-websocket-like L2 materializer in `scripts/run_phase45_raw_tick_lake_materializer.py`, backed by `src/synthetic_l2/phase45_raw_tick_lake_materializer.py`.

Generated Phase 45 metadata artifacts are under `outputs/phase45/`:

- `raw_tick_lake_partition_inventory.csv`
- `raw_tick_lake_schema.csv`
- `raw_tick_lake_size_ledger.csv`
- `phase45_raw_tick_lake_materialization_report.md`
- `phase45_raw_tick_lake_materialization_manifest.json`

The full current-event raw lake itself is intentionally outside Git under `raw_synthetic_l2_full_year/`, partitioned as:

`trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/part-00000.parquet`

Each persisted row is a Zerodha-websocket-like tick update with collector/session/callback sequencing fields, received/exchange timestamps, symbol/instrument metadata, last price/quantity/volume fields and L1-L5 bid/ask price, quantity and order-count state. This makes the raw tick layer explicit instead of treating the compact Phase 42 event-state parquet as if it were the raw archive.

The current Phase 45 full run materialized the complete current synthetic event universe: 3,012,294 raw websocket-like L2 rows across 8,064 date/exchange/symbol parquet partitions. The compressed materialized raw lake is 491,002,806 bytes, or approximately 0.457 GB, with a measured compressed density of approximately 163 bytes per row. This is full-year for the current synthetic tick/event universe, but it is not an 80GB-class dense stress archive. At the measured compression rate, an 83.240 GB dense raw lake would require approximately 548,334,188 rows.

The immediate conclusion is that the requested raw full-year L2 partitioned lake now exists for every current synthetic tick update, and the storage gap is quantified rather than hidden: the next storage milestone, if required, should deliberately densify the synthetic tick process toward the 548M-row/83GB-class stress lake instead of calling the compact 3.0M-row event universe equivalent to that larger target.

## Phase 46 — Raw Tick-Lake Replay Diagnostics

**Current Phase 46 implementation status as of 2026-07-16:** Phase 46 now has a runnable raw-lake replay diagnostic in `scripts/run_phase46_raw_tick_lake_replay_diagnostics.py`, backed by `src/synthetic_l2/phase46_raw_tick_lake_replay_diagnostics.py`.

Generated Phase 46 artifacts are under `outputs/phase46/`:

- `raw_tick_lake_integrity_summary.csv`
- `raw_tick_lake_replay_summary.csv`
- `raw_tick_lake_forward_edge_results.csv`
- `raw_tick_lake_feature_sample.csv`
- `phase46_raw_tick_lake_replay_diagnostics_report.md`
- `phase46_raw_tick_lake_replay_diagnostics_manifest.json`

This phase proves the Phase 45 raw lake is not just storage decoration. It reads the partition inventory, loads the date/exchange/symbol parquet files directly, reconstructs event features from raw L1-L5 depth fields and runs a raw-source forward-edge diagnostic without using the compact Phase 42 event-state parquet as the experiment source.

The current Phase 46 run scans all 8,064 raw partitions and loads all 3,012,294 raw websocket-like L2 rows. It confirms 32 symbols, 252 trade dates, 5 feed profiles, complete nonzero L1-L5 depth fields, exact inventory row-count match and 0 reconstructed mid-price null rows. It evaluates 72 raw-derived forward-edge candidates and 11,333,962 raw-derived feature-threshold signals. No raw replay candidate passes the conservative pre-replay rule. The best raw-derived mean net edge return is approximately `0.002731`, the best raw directional precision is approximately `0.52537`, and the best raw precision lift versus baseline is approximately `0.87609`. `phase46_synthetic_full_year_acceptance_ready` remains 0.

The immediate conclusion is that downstream experiments can now source from the raw partitioned L2 lake itself. The raw-derived economics still do not justify promotion, but Phase 46 closes the infrastructure gap between raw tick storage and executable replay diagnostics.

## Phase 47 — Raw Lake DuckDB Catalog

**Current Phase 47 implementation status as of 2026-07-16:** Phase 47 now has a runnable DuckDB catalog and benchmark layer in `scripts/run_phase47_raw_lake_duckdb_catalog.py`, backed by `src/synthetic_l2/phase47_raw_lake_duckdb_catalog.py`.

Generated Phase 47 artifacts are under `outputs/phase47/`:

- `raw_lake_duckdb_catalog_summary.csv`
- `raw_lake_duckdb_schema.csv`
- `raw_lake_duckdb_benchmark_timings.csv`
- `raw_lake_duckdb_benchmark_results.csv`
- `phase47_raw_lake_duckdb_catalog_report.md`
- `phase47_raw_lake_duckdb_catalog_manifest.json`

The local DuckDB file `outputs/phase47/raw_lake.duckdb` is intentionally ignored by Git. The committed artifacts capture the query evidence and reproducibility manifest.

This phase registers the Phase 45 raw partitioned websocket-like L2 parquet lake as a DuckDB view and runs SQL integrity/benchmark queries. It uses `read_parquet(..., hive_partitioning=false, union_by_name=true)` so the physical `trade_date`, `exchange` and `symbol` columns remain authoritative and do not collide with hive partition inference.

The current Phase 47 run queries 8,064 raw parquet partitions and confirms via DuckDB SQL that the raw lake has 3,012,294 rows, 32 symbols, 252 trade dates, 5 feed profiles and 3,012,294 rows with complete L1/L5 price and quantity state. HDFCBANK has 94,110 raw rows in the lake. The benchmark set executed 7 SQL queries; full-scan timings ranged from approximately 5.9 seconds for total row count to approximately 19.7 seconds for the L1/L5 completeness scan.

The immediate conclusion is that the raw lake is queryable through DuckDB and ready for SQL-driven experiment filters. The benchmark also exposes a concrete optimization target: 8,064 tiny symbol-day parquet files work functionally, but the next storage-performance improvement should compact them into larger monthly or symbol-bucket row groups before scaling toward the 80GB-class dense lake.

## Phase 48 — Raw Lake Compaction Benchmark

**Current Phase 48 implementation status as of 2026-07-16:** Phase 48 now has a runnable raw-lake compaction and benchmark workflow in `scripts/run_phase48_raw_lake_compaction_benchmark.py`, backed by `src/synthetic_l2/phase48_raw_lake_compaction_benchmark.py`.

Generated Phase 48 artifacts are under `outputs/phase48/`:

- `compact_raw_lake_inventory.csv`
- `raw_lake_compaction_summary.csv`
- `raw_lake_compaction_benchmark_timings.csv`
- `raw_lake_compaction_benchmark_results.csv`
- `raw_lake_compaction_speedup_comparison.csv`
- `phase48_raw_lake_compaction_benchmark_report.md`
- `phase48_raw_lake_compaction_benchmark_manifest.json`

The compacted raw lake itself is local and ignored by Git under `raw_synthetic_l2_full_year_compact_monthly/`, partitioned as:

`trade_month=YYYY-MM/part-00000.parquet`

This phase compacts the Phase 45 date/exchange/symbol raw parquet lake into larger monthly parquet files and benchmarks the same DuckDB SQL query set against both layouts. It preserves row-level raw websocket-like L2 records while reducing file-count overhead.

The current Phase 48 run reduces the raw lake from 8,064 symbol-day parquet files to 12 monthly parquet files, a 672x file-count reduction. Row counts match exactly: both layouts contain 3,012,294 rows. Compressed parquet bytes fall from 491,002,806 bytes to 177,847,919 bytes. DuckDB benchmark speedups are material: total row count improves from approximately 14.4 seconds to 25 ms, HDFCBANK row count from approximately 17.0 seconds to 55 ms, and the L1/L5 completeness scan from approximately 90.2 seconds to 1.57 seconds. The best query speedup is approximately 572x and the median query speedup is approximately 185x. `phase48_synthetic_full_year_acceptance_ready` remains 0.

The immediate conclusion is that the compact monthly layout should be the default query source for repeated experiments, while the original date/exchange/symbol raw lake remains the audit/source-of-truth layout. This also sets the storage pattern for any future 80GB-class dense tick expansion: generate raw partitions for auditability, then compact into larger query row groups before running expensive experiments.

## Phase 49 — Dense Tick-Rate Expansion Calibration

**Current Phase 49 implementation status as of 2026-07-16:** Phase 49 now has a runnable dense tick-rate expansion calibration workflow in `scripts/run_phase49_dense_tick_rate_expansion.py`, backed by `src/synthetic_l2/phase49_dense_tick_rate_expansion.py`.

Generated Phase 49 artifacts are under `outputs/phase49/`:

- `dense_tick_shard_inventory.csv`
- `dense_tick_expansion_summary.csv`
- `phase49_dense_tick_rate_expansion_report.md`
- `phase49_dense_tick_rate_expansion_manifest.json`

The dense calibration shard itself is local and ignored by Git under `raw_synthetic_l2_dense_phase49_hdfcbank_x64/`, partitioned as:

`trade_month=YYYY-MM/symbol=HDFCBANK/part-00000.parquet`

This phase deliberately separates raw persistence from tick-rate density. Earlier phases proved the raw websocket-like L2 pipe and query layer; Phase 49 turns up the event-rate faucet for one full-year HDFCBANK shard to measure dense compression, throughput and the real multiplier needed for an 80GB-class compressed raw lake.

The current Phase 49 run densifies all HDFCBANK full-year compact-raw rows with a 64x subtick multiplier. It converts 94,110 source rows into 6,023,040 dense raw rows across 12 monthly parquet files. The dense shard is 90,102,511 compressed bytes, or approximately 14.96 compressed bytes per row, and was generated in approximately 15.6 seconds at roughly 385,756 rows/second. Because dense subticks compress much more strongly than the earlier raw-row estimate, an 83.240 GB compressed dense lake now implies approximately 5.97 billion rows and an estimated full-universe source-row multiplier of approximately 1,983x at this encoding. At the measured shard throughput, that target would take roughly 4.3 hours before accounting for full-universe skew and I/O contention. `phase49_full_80gb_dense_lake_materialized` remains 0.

The immediate conclusion is that the next dense expansion step should be a controlled multi-symbol or full-universe shard plan using the compact monthly layout, not a blind one-shot write. The target is now quantified in compressed-row terms: the 80GB-class lake is closer to a multi-billion-row synthetic tick process than a 500M-row process under the current Zstandard/Parquet encoding.

## Phase 50 — Dense Lake Shard Planner

**Current Phase 50 implementation status as of 2026-07-16:** Phase 50 now has a runnable dense-lake shard planner in `scripts/run_phase50_dense_lake_shard_planner.py`, backed by `src/synthetic_l2/phase50_dense_lake_shard_planner.py`.

Generated Phase 50 artifacts are under `outputs/phase50/`:

- `dense_target_shard_schedule.csv`
- `dense_bounded_run_plan.csv`
- `dense_bounded_materialization_inventory.csv`
- `dense_lake_shard_planner_summary.csv`
- `phase50_dense_lake_shard_planner_report.md`
- `phase50_dense_lake_shard_planner_manifest.json`

The bounded dense validation shard is local and ignored by Git under `raw_synthetic_l2_dense_phase50_multisymbol_x64/`, partitioned by trade month and symbol.

This phase converts the Phase 49 dense compression/throughput calibration into a concrete symbol-month shard schedule for the 80GB-class target. It then materializes a bounded multi-symbol dense shard to prove orchestration beyond one ticker before attempting a full-universe multi-billion-row run.

The current Phase 50 run creates a 384-row target schedule covering 32 symbols x 12 trade months and all 3,012,294 compact monthly source rows. Using the Phase 49 dense compression measurement, the 83.240 GB compressed target implies approximately 5.9746 billion dense rows and a full-universe source-row multiplier of approximately 1,983x. The schedule estimates approximately 89.38 billion compressed bytes and approximately 4.3 hours at the Phase 49 measured throughput. As a bounded validation run, Phase 50 materializes HDFCBANK, INFY and RELIANCE at 64x across the full year: 36 symbol-month dense files, 18,068,416 dense rows and 269,683,823 compressed bytes. `phase50_full_80gb_dense_lake_materialized` remains 0.

The immediate conclusion is that the dense target is now schedulable rather than hand-wavy. The next run can choose between a larger bounded tranche or the full 384-shard schedule, but it should preserve this shard manifest so partial progress and disk usage remain auditable.

## Phase 51 — Full Dense Lake Materializer

**Current Phase 51 implementation status as of 2026-07-16:** Phase 51 now has a runnable full dense lake materializer in `scripts/run_phase51_full_dense_lake_materializer.py`, backed by `src/synthetic_l2/phase51_full_dense_lake_materializer.py`.

Planned/generated Phase 51 artifacts are under `outputs/phase51/`:

- `full_dense_lake_inventory.csv`
- `full_dense_lake_summary.csv`
- `phase51_full_dense_lake_materializer_report.md`
- `phase51_full_dense_lake_materializer_manifest.json`

The full dense lake itself is local and ignored by Git under `raw_synthetic_l2_dense_full_year/`, partitioned as:

`trade_month=YYYY-MM/symbol=SYMBOL/part-00000.parquet`

This phase consumes the Phase 50 384-shard target schedule and materializes every symbol-month shard to its scheduled dense row count. Because the Phase 50 target multiplier is fractional at approximately 1,983.414x, Phase 51 writes 1,983 subticks for every source tick plus one extra subtick for the first required source rows in each shard so the final row count matches the target schedule. It streams each shard through bounded source-row chunks rather than building the full multi-billion-row lake in memory.

The completed Phase 51 run materialized all 384 scheduled symbol-month shards and matched the Phase 50 row schedule exactly: 5,974,626,961 dense rows written versus 5,974,626,961 scheduled rows, with 0 row difference. It consumed all 3,012,294 compact monthly source rows and wrote 384 parquet files under `raw_synthetic_l2_dense_full_year/`. The actual compressed lake size is 70,591,392,905 bytes, or approximately 65.743 GiB, which is below the Phase 50 83.240 GiB target estimate because the full dense lake compressed more strongly than the calibration estimate: actual bytes were approximately 78.98% of the estimated 89,378,269,358 bytes. The observed materialization throughput was approximately 456,065 dense rows/second over 13,100.4 seconds. The completion flag `phase51_full_80gb_dense_lake_materialized` is now `1`; `phase51_synthetic_full_year_acceptance_ready` remains `0` until strategies are actually replayed on the dense lake with the synthetic-only acceptance criteria.

## Phase 52 — Dense Lake Strategy Replay

**Current Phase 52 implementation status as of 2026-07-16:** Phase 52 now has a runnable dense-lake strategy replay workflow in `scripts/run_phase52_dense_lake_strategy_replay.py`, backed by `src/synthetic_l2/phase52_dense_lake_strategy_replay.py`.

Planned/generated Phase 52 artifacts are under `outputs/phase52/`:

- `dense_replay_daily_symbol.csv`
- `dense_replay_strategy_summary.csv`
- `dense_replay_acceptance_summary.csv`
- `phase52_dense_lake_strategy_replay_report.md`
- `phase52_dense_lake_strategy_replay_manifest.json`

This phase scans the Phase 51 dense parquet lake shard-by-shard with DuckDB rather than loading the full 5.97B-row lake into memory. It computes L1 imbalance, microprice deviation and one-tick momentum proxy signals, applies the Phase 12 execution latency profiles, and deducts spread, slippage, impact and Zerodha equity-intraday NSE cost-model charges. Results are aggregated to daily-symbol and strategy-profile ledgers without persisting billions of individual trade rows.

The acceptance boundary remains strict: Phase 52 can produce dense synthetic-only replay evidence and candidate rows, but `phase52_synthetic_full_year_acceptance_ready` remains `0` unless a candidate clears the synthetic-only acceptance gates and subsequent evidence contracts.

---

## Phase 131-136 — Post-Phase130 Top-Five-Depth Passive Continuation

**Continuation source:** `Plan/Plan continuation2.txt`, imported into this main plan on 2026-07-23 with corrected terminology.

This continuation begins from the Phase130 state: no-replay diagnostic baselines over the Phase129 allowed-context matrix. It deliberately does **not** reopen the failed Level-1/top-of-book taker branch. Its only remaining synthetic strategy surface is the Zerodha Level-2 **top-five market-by-price depth** passive surface.

### Standing constraints for Phase131-136

These constraints govern every phase in this continuation and must not be relaxed:

1. **Retail cash equity only.** No futures, options, derivative synthetics or expanded symbol universe. All instruments remain the current 32-symbol NSE cash-equity/ETF panel.
2. **Top-five market-by-price depth only.** Zerodha WebSocket depth is treated as Level-2/top-five visible book depth: best bid/ask plus depth levels 2-5. No phase may use hidden-order models, full order-book reconstruction, participant information, exchange-side queue snapshots or order-by-order L3/L4/L5 data.
3. **Pinned Zerodha cost model.** The base cost model remains `zerodha_equity_intraday_nse_order_formula_v2_2026_07_14`. This continuation may add a precommitted harsh-stress regime, but it may not edit the pinned base formula.
4. **No profitability or replay unlock inside the continuation.** `strategy_replay_allowed = 0` remains the default. No phase may emit promoted buy/sell signals, order-arrival streams, live-tagged fill models, P&L replay or deployable profitability claims.
5. **Positive pockets do not rescue a failed family.** Full-sample verdicts and harsh-regime gates decide outcomes.

### Established state as of Phase130

The repository has already established:

- Level-1/top-of-book taker families do not clear retail costs on synthetic data. Phase52/Phase116 reviewed roughly 800 million dense replay observations across L1 imbalance, microprice and one-tick momentum families under multiple execution profiles, with no accepted profitable survivor.
- Same-family rescues and related strategy branches failed: HDFCBANK lead-lag, cross-symbol regime imbalance, low-turnover event windows, composite signals, passive queue-capture probes and lower-frequency meta replays did not survive precommitted gates.
- Isolated positive pockets were observed in some failed branches, but none became accepted strategies.
- Generator realism has improved through Phases79 and 94-109, but real anchor L2 remains insufficient. Phase117 still records 1 candidate day and 4 additional ready real-anchor days needed for minimum replay unlock.
- Phase130 diagnostic baselines are the current frontier:
  - `feed_imperfection_rate <= 0.015872` for regime stability, holdout AUC approximately 0.9048;
  - `passive_min_adverse_rate >= 0.99099099` for cost-toxicity refinement, holdout AUC approximately 0.85;
  - `median_spread_bps >= 4.0782951` for liquidity opportunity, weak/degenerate holdout AUC 0.5 despite Brier improvement.

### Continuation objective

Exhaust the **top-five-depth passive surface** on synthetic data under realistic Zerodha retail cost stress and end in exactly one of three clean states:

1. **Falsified.** Update the Phase116 blocklist with a deep-book/top-five-depth passive entry and formally close synthetic strategy hunting.
2. **Marginal handoff.** Emit a machine-readable feature and strategy specification that can be re-evaluated when real Zerodha L2 data arrives through the Phase113-115 drop-zone.
3. **Clean synthetic survivor with advisory.** Emit the same handoff artifact plus an explicit advisory that synthetic-only survival is not deployable evidence and must be re-tested on real L2 before any replay unlock.

The continuation is intentionally bounded to six phases. If the Phase132 kill-switch fires, the continuation terminates at Phase132 and skips Phases133-136.

### Phase 131 — Top-Five-Depth Feature and Cost-Stress Precommit

**Runner:** `scripts/run_phase131_deep_book_feature_precommit.py`

**Outputs:** `outputs/phase131/`

**Purpose:** lock the feature catalog, cost regimes and evaluation rules before Phase132 diagnostics touch data.

**Current implementation status as of 2026-07-23:** Phase131 is implemented and committed. The current artifacts are:

- `phase131_feature_catalog.csv`
- `phase131_cost_regimes.csv`
- `phase131_evaluation_rules.md`
- `phase131_phase130_baseline_reference.csv`
- `phase131_guardrails.csv`
- `phase131_gate_evaluation.csv`
- `phase131_deep_book_feature_precommit_acceptance_summary.csv`
- `phase131_deep_book_feature_precommit_report.md`
- `phase131_precommit_manifest.json`

Phase131 precommits 10 top-five depth-level feature definitions. Feature catalog references such as `depth_level_1` through `depth_level_5` are book-depth rows in the Zerodha Level-2/top-five market-by-price feed, not L1-L5 market-data product tiers.

The Phase131 cost regimes are:

- `base`: the pinned Zerodha cost model unchanged;
- `harsh`: the pinned Zerodha cost model plus 25% uplift to spread-cross cost and all per-leg fee components.

The Phase131 acceptance summary currently records:

- feature catalog rows: 10;
- top-of-book-only feature rows: 0;
- cost regime rows: 2;
- Phase130 baseline reference rows: 3;
- allowed Phase129 context rows: 228;
- Phase132 Brier lift margin: 0.005;
- gate rows: 7;
- all gates passed: 1;
- strategy replay allowed: 0;
- pinned cost model: `zerodha_equity_intraday_nse_order_formula_v2_2026_07_14`.

### Phase 132 — Top-Five-Depth Feature Diagnostics

**Runner:** `scripts/run_phase132_deep_book_feature_diagnostics.py`

**Outputs:** `outputs/phase132/`

**Purpose:** evaluate Phase131 top-five-depth features as label predictors only against the three Phase129 diagnostic labels:

- `p129_regime_stability_label`;
- `p129_liquidity_opportunity_label`;
- `p129_cost_toxicity_refinement_label`.

**Method:**

- Reuse the Phase130 chronological split: 172 train rows and 56 holdout rows.
- Fit single-feature threshold baselines and simple two-feature threshold combinations for Phase131 features.
- Report Brier, log-loss, accuracy and AUC.
- Do not fit models more complex than the precommitted threshold families.
- Do not emit strategy code, buy/sell signals, order-arrival streams, live-tagged fill models, P&L replay or profitability claims.

**Kill-switch:** if no Phase131 feature beats the corresponding Phase130 top-of-book/context baseline by more than the precommitted 0.005 Brier margin on any of the three labels, the branch closes at Phase132. Phase133-136 are skipped, and the Phase116 blocklist is updated with `DEEP_BOOK_LABEL_LIFT = falsified`.

If at least one Phase131 feature clears the lift requirement, the surviving features are promoted to Phase133.

**Current implementation status as of 2026-07-23:** Phase132 is implemented and the kill-switch fired. Generated artifacts are under `outputs/phase132/`:

- `top_five_depth_feature_matrix.csv`
- `feature_diagnostic_results.csv`
- `feature_model_selection.csv`
- `surviving_features.csv`
- `kill_switch_summary.csv`
- `phase116_blocklist_update_verification.csv`
- `phase132_guardrails.csv`
- `phase132_gate_evaluation.csv`
- `phase132_deep_book_feature_diagnostics_acceptance_summary.csv`
- `phase132_deep_book_feature_diagnostics_report.md`
- `phase132_deep_book_feature_diagnostics_manifest.json`

The Phase132 run scanned the compact monthly raw top-five-depth lake, aggregated the Phase131 feature catalog by the 228 allowed Phase129 symbol-month contexts, reused the Phase130 172/56 chronological split, and evaluated 711 prior/single-feature/two-feature diagnostic rows. No Phase131 top-five-depth feature beat the corresponding Phase130 top-of-book/context baseline by the precommitted Brier margin of 0.005:

- regime stability: best Phase132 Brier `0.254286` versus Phase130 reference `0.082857`;
- liquidity opportunity: best Phase132 Brier `0.072143` versus Phase130 reference `0.072143`;
- cost-toxicity refinement: best Phase132 Brier `0.147143` versus Phase130 reference `0.104286`.

Therefore:

- `phase132_surviving_feature_rows = 0`;
- `phase132_labels_cleared_brier_lift = 0`;
- `phase132_kill_switch_fired = 1`;
- Phase133-136 are skipped for this branch;
- `outputs/phase116/strategy_replay_blocklist.csv` now includes `DEEP_BOOK_LABEL_LIFT`;
- `strategy_replay_allowed` remains `0`.

The branch conclusion is clean falsification of the synthetic-only top-five-depth label-lift surface. The correct next action is not another synthetic strategy branch; further strategy work waits on real Zerodha L2 anchor acquisition through Phases113-115 or a separately precommitted plan outside this closed branch.

### Phase 137 — Post-Phase132 Real-Anchor Restart

**Runner:** `scripts/run_phase137_post_phase132_real_anchor_restart.py`

**Outputs:** `outputs/phase137/`

**Purpose:** convert the Phase132 clean falsification into the next operational path: real Zerodha L2 anchor acquisition. This phase does not reopen synthetic strategy work, run Phase133-136, emit order simulations or change replay permissions.

**Current implementation status as of 2026-07-23:** Phase137 is implemented and generated:

- `closed_synthetic_branch_ledger.csv`
- `real_anchor_acquisition_requirements.csv`
- `real_anchor_operational_runbook.csv`
- `phase137_gate_evaluation.csv`
- `phase137_post_phase132_real_anchor_restart_acceptance_summary.csv`
- `phase137_post_phase132_real_anchor_restart_report.md`
- `phase137_post_phase132_real_anchor_restart_manifest.json`

The Phase137 acceptance summary records:

- closed branch rows: 1;
- Phase132 kill-switch fired: 1;
- Phase116 `DEEP_BOOK_LABEL_LIFT` blocklist row present: 1;
- current ready real-anchor days: 1;
- additional days needed for minimum replay-unlock review: 4;
- additional days needed for preferred 10-day target: 9;
- real-anchor requirement rows: 9;
- all gates passed: 1;
- strategy replay allowed: 0.

The next concrete milestone is `drop_or_sync_4_more_real_l2_days_then_run_phase115_execute_import`. New real data should be placed under:

`real_data_sample/l2_multiday_panel/trade_date=YYYY-MM-DD/exchange=NSE/symbol=SYMBOL/*.parquet`

Each new real day should cover at least 95% of the 32-symbol universe and include raw Zerodha Level-2/top-five market-by-price WebSocket updates with depth levels 1-5 bid/ask price, quantity and order-count fields. After the data lands, run:

`python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root real_data_sample/l2_multiday_panel --execute-import`

Replay remains closed until Phase115/Phase110 prove enough ready real-anchor days and downstream realism gates are refreshed.

**Current continuation status as of 2026-07-23 after Azure real-data sync:** Azure Files account `stctrade1ramic`, share `ctrade1-l2-data`, path `raw_l2/` was live-checked and showed real L2 date partitions including:

- `trade_date=2026-07-08`;
- `trade_date=2026-07-09`;
- `trade_date=2026-07-10`;
- `trade_date=2026-07-13`;
- `trade_date=2026-07-14`;
- `trade_date=2026-07-15`;
- `trade_date=2026-07-16`;
- `trade_date=2026-07-17`;
- `trade_date=2026-07-20`;
- `trade_date=2026-07-21`;
- `trade_date=2026-07-22`;
- `trade_date=2026-07-23`;
- plus a small anomaly partition `trade_date=1970-01-01`.

AzCopy was installed locally from Microsoft's official Windows v10 package and used as the practical transfer path because direct Python Azure Files inventory/download and Azure CLI `download-batch --pattern` were too slow for the tiny-file archive. The local sync/import result currently is:

- `2026-07-08` downloaded under `scratch_azcopy_selected/raw_l2/trade_date=2026-07-08` and imported into `real_data_sample/l2_multiday_panel`;
- `2026-07-09` downloaded under `scratch_azcopy_selected/raw_l2/trade_date=2026-07-09` and imported into `real_data_sample/l2_multiday_panel`;
- `2026-07-13` already present from `real_data_sample/l2_single_day` and imported into `real_data_sample/l2_multiday_panel`;
- canonical multiday panel size after import: 3 date partitions, 99,272 parquet files, 3,490,276,400 bytes;
- Phase115 copied 49,067 new files from the AzCopy scratch source in the latest import;
- Phase114 executed-import integrity passed;
- Phase96 now reports `phase96_ready_anchor_days = 3` using the maximum distinct ready trade dates in any one panel, so duplicate copies of the same date across `l2_single_day` and `l2_multiday_panel` cannot inflate the gate;
- Phase110 reports `phase110_ready_real_anchor_days = 3`, `phase110_days_needed_for_min = 2`, and `phase110_replay_unlock_allowed = 0`.

The immediate next operational action is to download and import two more Azure real L2 dates, preferably from the already-observed available set such as `2026-07-10` and `2026-07-14`, then rerun:

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_azure_real_l2_dates_azcopy.ps1 -Dates 2026-07-10,2026-07-14 -ShareSasToken "<read_list_share_sas>"`

or, when a storage account key is available but Azure CLI token refresh is blocked locally:

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_azure_real_l2_dates_azcopy.ps1 -Dates 2026-07-10,2026-07-14 -AccountKey "<storage_account_key>"`

Then verify local download/import readiness without contacting Azure:

`python scripts/run_phase142_local_real_l2_download_verifier.py --roots scratch_azcopy_selected/raw_l2 real_data_sample/l2_multiday_panel`

Then run the two-date acquisition preflight:

`python scripts/run_phase143_real_l2_two_date_preflight.py`

Optionally run the post-download refresh orchestrator, which stitches Phase142, Phase143, conditional Phase115 import, Phase117 and Phase137 together:

`python scripts/run_phase145_real_l2_post_download_refresh.py`

Then import/refresh:

`python scripts/run_phase115_real_panel_refresh_orchestrator.py --source-root scratch_azcopy_selected/raw_l2 --target-root real_data_sample/l2_multiday_panel --execute-import`

If Azure CLI token refresh again hits local TLS certificate failures, generate a fresh read/list SAS from an already-authenticated PowerShell session, provide the storage account key directly to the helper, or repair the Azure CLI CA chain before continuing the AzCopy downloads. The helper script accepts the SAS as a parameter or via `AZURE_STORAGE_SAS_TOKEN`; it also accepts the account key as `-AccountKey` or via `AZURE_STORAGE_KEY` and generates a short-lived read/list share SAS locally. It redacts `sig=` in dry-run command output and does not persist credentials. The helper normalizes comma-separated date arguments, so `-Dates 2026-07-10,2026-07-14` emits separate AzCopy transfers for both dates. The helper copies date URLs into the raw root `scratch_azcopy_selected/raw_l2` so future downloads should land as a single `trade_date=YYYY-MM-DD` partition rather than nesting duplicate date folders.

Phase142 local verification is implemented under `outputs/phase142/` and currently records:

- roots checked: 2 (`scratch_azcopy_selected/raw_l2` and `real_data_sample/l2_multiday_panel`);
- symbol partition rows: 160;
- canonical symbol partition rows: 96;
- nested trade-date symbol partition rows: 64, all in the historical AzCopy scratch root from the earlier date-URL-to-date-folder copy style;
- root/date readiness rows: 5;
- ready root/date rows for Phase115 import: 5;
- maximum ready dates in one root: 3;
- total checked parquet files: 148,339;
- total checked bytes: 5,216,547,016;
- strategy replay allowed: 0.

Phase142 is an import/download preflight, not a market-quality gate. It checks coverage, required schema, readable first/last samples, parquet counts and bytes. Its L1 book sample status is diagnostic only; Phase96 remains the authoritative real-anchor market-quality gate.

The canonical imported panel is clean: `real_data_sample/l2_multiday_panel` contains 96 canonical symbol partitions across the three ready dates (`2026-07-08`, `2026-07-09`, `2026-07-13`) and zero nested duplicate `trade_date` symbol partitions. The nested scratch layout is tolerated for import discovery but should not be produced by future downloads now that the AzCopy helper copies date URLs into the raw root.

Phase143 two-date preflight is implemented under `outputs/phase143/`. Its current evidence records:

- current ready real-anchor days: 3;
- days needed for minimum: 2;
- required next-date rows checked: 2 (`2026-07-10`, `2026-07-14`);
- required dates satisfied in scratch or target: 0;
- required dates ready in canonical target: 0;
- required dates ready in scratch for import: 0;
- can run Phase115 import now: 0;
- strategy replay allowed: 0;
- next best action: `download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase142_phase143`.

Phase143 is the guard that prevents a premature Phase115 rerun when an empty or partial date folder exists locally but does not yet contain a complete import-ready 32-symbol real L2 partition.

Phase145 post-download refresh orchestration is implemented under `outputs/phase145/`. It always refreshes Phase142 and Phase143, runs Phase115 only when Phase143 reports `phase143_can_run_phase115_import_now = 1`, and then refreshes Phase117/137 handoff evidence. Its current run records:

- steps attempted: 4;
- failed steps: 0;
- Phase115 import executed: 0, correctly skipped because the required dates are not locally ready;
- Phase143 required dates satisfied: 0 of 2;
- ready real-anchor days: 3;
- days needed for minimum: 2;
- Phase137 refreshed days needed for minimum: 2;
- replay unlock allowed: 0;
- next best action: `download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase145`.

Phase146 real-anchor minimum unlock audit is implemented under `outputs/phase146/`.

**Runner:** `python scripts/run_phase146_real_anchor_minimum_unlock_audit.py`

**Purpose:** provide a read-only, local-only final audit before any strategy replay is allowed to reopen after new real L2 anchor dates are downloaded and imported. Phase146 reconciles Phase96, Phase110, Phase115, Phase143 and Phase145 evidence. It does not contact Azure, does not import data, and does not infer readiness from partial folders.

Current Phase146 evidence records:

- hard unlock-audit gates evaluated: 6;
- hard unlock-audit gates passed: 4;
- minimum ready real-anchor days required: 5;
- Phase115/110 ready real-anchor days: 3;
- days still needed for minimum: 2;
- Phase143 required date rows checked: 2 (`2026-07-10`, `2026-07-14`);
- Phase143 required dates satisfied: 0 of 2;
- Phase145 Phase115 import executed: 0;
- minimum unlock audit pass: 0;
- strategy replay allowed: 0;
- next best action: `download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase145_phase146`.

Phase146 gate evaluation currently confirms:

- Phase96/Phase110/Phase115 ready-day counts are internally consistent (`3 / 3 / 3`);
- Phase115 days-needed arithmetic is consistent (`2`);
- replay unlock flags are internally consistent (`0 / 0 / 0`);
- Phase145 completed cleanly with zero failed steps;
- the minimum-ready-real-anchor-days gate fails because `3 < 5`;
- the configured required-date gate fails because `0 / 2` required dates are locally ready;
- replay remains closed.

Phase147 AzCopy download intake audit is implemented under `outputs/phase147/`.

**Runner:** `python scripts/run_phase147_azcopy_download_intake_audit.py`

**Purpose:** validate the local AzCopy landing zone immediately after a bulk date download and before Phase145 import/refresh is attempted. This keeps Azure I/O in AzCopy and keeps Python on local inspection only. Phase147 checks the configured required dates across scratch and canonical target, verifies 32-symbol coverage, sampled required Zerodha top-five market-by-price schema, file/byte counts, target-vs-scratch state, and duplicate nested `trade_date` layouts.

Current Phase147 evidence records:

- required date rows checked: 2 (`2026-07-10`, `2026-07-14`);
- required dates satisfied in scratch or target: 0;
- required dates ready for import from scratch: 0;
- required dates already complete in target: 0;
- scratch complete dates: 0;
- target complete dates: 0;
- nested duplicate `trade_date` symbol directories across checked required dates: 0;
- can run Phase145 now: 0;
- strategy replay allowed: 0;
- next best action: `download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase147`.

Phase147 specifically confirms that the current empty/partial `scratch_azcopy_selected/raw_l2/trade_date=2026-07-10` folder is not import-ready: it has a date root but `0 / 32` expected symbol partitions with Parquet files. This prevents an empty local date folder from being mistaken for a complete Zerodha WebSocket top-five market-by-price L2 date.

Phase147 symbol-intake output is deterministic: expected symbols are emitted in sorted order so reruns do not churn evidence solely because of Python set ordering.

Phase148 real L2 download refresh workflow is implemented under `outputs/phase148/`.

**Runner:** `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_phase148_real_l2_download_refresh_workflow.ps1`

**Purpose:** make the AzCopy-first real L2 path executable as one workflow. Phase148 optionally runs the AzCopy download helper, always runs Phase147 local intake, conditionally runs Phase145 only when Phase147 reports a required date is ready for import, and always runs Phase146 final unlock audit. Python remains local-only; Azure bulk I/O remains in AzCopy.

Current Phase148 local skip-download validation records:

- workflow steps: 4;
- failed steps: 0;
- AzCopy download ran: 0, because validation used `-SkipDownload`;
- Phase147 says Phase145 can run now: 0;
- Phase145 ran: 0, correctly skipped because no required date is import-ready;
- Phase146 strategy replay allowed: 0;
- Phase146 days still needed for minimum: 2;
- workflow strategy replay allowed: 0;
- next best action: `download_missing_required_dates_with_azcopy_sas_or_account_key_then_rerun_phase148`.

The next operational path remains AzCopy-first, local-analysis-second:

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_phase148_real_l2_download_refresh_workflow.ps1 -Dates 2026-07-10,2026-07-14 -AccountKey "<storage_account_key>"`

For local validation without touching Azure:

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_phase148_real_l2_download_refresh_workflow.ps1 -SkipDownload`

Phase149 research state auditor is implemented under `outputs/phase149/`.

**Runner:** `python scripts/run_phase149_research_state_auditor.py`

**Purpose:** reconcile current phase scripts, output evidence, branch states, and replay gates from files. Phase149 does not run strategies, contact Azure, import data, or unlock replay. It is the authoritative local ledger for answering “what phases exist, what is finished, what is closed, and what is still gated?”.

Current Phase149 evidence records:

- phase rows discovered from scripts and outputs: 142;
- phase rows with at least one runner: 140;
- phase rows with acceptance summaries: 91;
- current research branches summarized: 3;
- hard global-state gates evaluated: 3;
- hard global-state gates passed: 3;
- strategy replay allowed: 0;
- next best action: `download_real_l2_anchor_dates_with_phase148_or_start_new_precommitted_non_blocklisted_branch`.

Current branch summary:

- `real_l2_anchor_gate`: gated; Phase146/148 keep strategy replay closed until at least five ready real-anchor days are proven.
- `top_five_depth_passive`: closed clean falsification; Phase136 Outcome A closes the branch after Phase132 kill-switch and Phase116 blocklist verification.
- `dense_synthetic_replay`: not promoted; partial/smoke dense replay artifacts remain non-promotional and do not override replay gates.

Current global gates:

- real L2 replay gate closed: pass;
- deep-book branch closed: pass;
- no promoted strategy replay: pass.

Phase150 real L2 DuckDB catalog is implemented under `outputs/phase150/`.

**Runner:** `python scripts/run_phase150_real_l2_duckdb_catalog.py`

**Purpose:** build a metadata-first DuckDB catalog for the local real Zerodha WebSocket Level-2/top-five market-by-price Parquet panel. The catalog keeps the canonical data in partitioned Parquet and does not copy all tick rows into DuckDB. DuckDB stores file inventory, date/symbol summaries, sampled schema, query templates, and a sample-file smoke view.

This confirms the storage decision for this project:

- use DuckDB for local multi-GB/multi-day Parquet analytics and ad hoc tick queries;
- avoid SQLite for tick L2 storage because it is row-store oriented and would require inefficient row ingestion/duplication;
- keep raw and canonical tick data in partitioned Parquet by `trade_date/exchange/symbol`;
- let DuckDB query Parquet locally after AzCopy downloads complete.

Current Phase150 evidence records:

- DuckDB available: 1;
- catalog database created: 1;
- Parquet files cataloged: 99,272;
- cataloged bytes: 3,490,276,400;
- trade dates cataloged: 3 (`2026-07-08`, `2026-07-09`, `2026-07-13`);
- date/exchange/symbol partitions cataloged: 96;
- sampled schema columns: 54;
- top-five book depth columns present: 30 (`buy/sell` levels 1-5, price/quantity/orders);
- DuckDB sample-file query rows: 5;
- strategy replay allowed: 0;
- next best action: `use_duckdb_catalog_for_local_real_l2_queries_after_phase148_downloads`.

Current catalog database:

`outputs/phase150/real_l2_catalog.duckdb`

Current catalog tables:

- `real_l2_parquet_files`;
- `real_l2_date_symbol_summary`;
- `real_l2_date_summary`;
- `real_l2_schema_columns`;
- `real_l2_query_templates`.

Current sample view:

- `real_l2_sample_ticks`.

Phase151 real L2 DuckDB query benchmark is implemented under `outputs/phase151/`.

**Runner:** `python scripts/run_phase151_real_l2_duckdb_query_benchmark.py`

**Purpose:** prove that bounded local DuckDB queries over the Phase150 catalog and partitioned Parquet panel work without Azure I/O and without copying all tick rows into DuckDB. Phase151 uses partition-scoped Parquet scans plus catalog metadata queries only.

Current Phase151 evidence records:

- Phase150 catalog DB exists locally: 1;
- benchmark partitions selected: 4;
- DuckDB queries attempted: 9;
- failed queries: 0;
- total query elapsed seconds: 7.223478;
- maximum bounded query elapsed seconds: 1.423375;
- minimum valid L1 book fraction across spread/depth queries: 0.999928;
- minimum visible depth-level-5 presence fraction: 0.999928;
- strategy replay allowed: 0;
- next best action: `use_partition_scoped_duckdb_queries_for_local_real_l2_analysis_after_phase148_downloads`.

Current benchmark partitions were all from `2026-07-13` because it is the largest currently cataloged date:

- ADANIPORTS: 1,569 files, 54,744,007 bytes, 13,886 queried rows;
- HDFCBANK: 1,569 files, 56,719,345 bytes, 35,959 queried rows;
- RELIANCE: 1,569 files, 55,637,533 bytes, 26,056 queried rows;
- TCS: 1,569 files, 56,845,524 bytes, 36,467 queried rows.

Phase151 confirms DuckDB should be used for local real L2 Parquet analytics. It still does not unlock strategy replay.

Phase152 real L2 microstructure profile is implemented under `outputs/phase152/`.

**Runner:** `python scripts/run_phase152_real_l2_microstructure_profile.py`

**Purpose:** profile bounded local real L2 partitions for received update cadence, inter-update gaps, L1 spread sanity, and visible depth-level-5 presence. Phase152 is diagnostics-only: no signals, no order-arrival stream, no fills, no P&L, no Azure I/O, and no replay unlock.

Current Phase152 evidence records:

- Phase150 catalog DB exists locally: 1;
- bounded date/symbol partitions profiled: 6;
- failed partition profiles: 0;
- total profile elapsed seconds: 10.312931;
- maximum bounded profile query elapsed seconds: 2.794497;
- minimum observed tick/update rate across profiled partitions: 0.608848 ticks/sec;
- maximum p95 inter-update gap across profiled partitions: 5,500 ms;
- minimum valid L1 book fraction: 0.999928;
- minimum visible depth-level-5 presence fraction: 0.999928;
- strategy replay allowed: 0;
- next best action: `use_profiles_for_real_anchor_diagnostics_after_phase148_downloads_not_strategy_replay`.

Current profiled partitions are all from `2026-07-13`:

- ADANIPORTS: 13,886 rows, 0.608848 ticks/sec, median gap 1,000 ms, p95 gap 5,500 ms;
- HCLTECH: 29,266 rows, 1.284992 ticks/sec, median gap 500 ms, p95 gap 4,158.8 ms;
- HDFCBANK: 35,959 rows, 1.578874 ticks/sec, median gap 500 ms, p95 gap 1,250 ms;
- INFY: 34,511 rows, 1.515286 ticks/sec, median gap 500 ms, p95 gap 2,627.1 ms;
- RELIANCE: 26,056 rows, 1.144087 ticks/sec, median gap 500 ms, p95 gap 4,324 ms;
- TCS: 36,467 rows, 1.601221 ticks/sec, median gap 500 ms, p95 gap 1,250 ms.

Phase152 confirms that the current real Zerodha WebSocket top-five market-by-price L2 panel is suitable for local microstructure diagnostics, while the strategy replay gate remains closed.

Phase153 real-vs-synthetic microstructure gap audit is implemented under `outputs/phase153/`.

**Runner:** `python scripts/run_phase153_real_synthetic_microstructure_gap_audit.py`

**Purpose:** compare bounded Phase152 full-partition real microstructure profiles against Phase106 calibrated synthetic anchor metrics, and audit whether older sampled real-anchor cadence profiles may be biased. Phase153 is diagnostic-only: no strategy, no replay unlock, no P&L, and no Azure I/O.

Current Phase153 evidence records:

- overlap symbols compared: 6;
- real-vs-synthetic gap rows: 18;
- real-vs-synthetic rows outside the 0.80-1.25 ratio band or missing: 11;
- Phase152 full-partition vs Phase106 sampled-anchor rows: 12;
- sample-bias rows outside the 0.50-2.00 sampled/full ratio band or missing: 3;
- inherited Phase106 severe metric gap count: 1;
- diagnostic recommendation rows: 2;
- strategy replay allowed: 0;
- next best action: `recompute_real_anchor_cadence_profiles_from_full_partitions_after_phase148_downloads`.

Current Phase153 diagnostic recommendations:

- `P153_RECOMPUTE_REAL_CADENCE_ANCHORS_FROM_FULL_PARTITIONS`: high priority. Three profiled symbols show older sampled p95 gap much higher than Phase152 full-partition p95 gap, so future cadence calibration should use Phase152-style full-partition DuckDB profiles before changing generator cadence parameters.
- `P153_KEEP_REPLAY_CLOSED_USE_GAPS_FOR_GENERATOR_DIAGNOSTICS`: high priority. Tail-cadence synthetic-low-vs-real rows and displayed-depth proxy gaps are generator diagnostics only; they must not open strategy replay or tune strategies to selected partitions.

Important interpretation: Phase153 does not say the synthetic generator is ready. It says the next calibration work should first recompute real-anchor cadence profiles from full local partitions, because the older sampled-file Phase106 p95 gap can overstate real tail gaps for some symbols.

Phase154 full-partition real cadence anchor is implemented under `outputs/phase154/`.

**Runner:** `python scripts/run_phase154_full_partition_real_cadence_anchor.py --all-dates`

**Purpose:** recompute Zerodha WebSocket received-cadence anchors from the full downloaded local Parquet partitions using DuckDB. Phase154 intentionally does not connect Python directly to Azure for data scans. The required operational pattern remains: bulk download Azure Files data first, then run local Parquet/DuckDB analytics. Phase154 scans only cadence columns and partition metadata; it does not generate signals, model fills, run P&L, contact Azure, or unlock strategy replay.

Current Phase154 evidence records:

- Phase150 local DuckDB catalog DB exists: 1;
- selected full local date/symbol partitions: 96;
- completed partition cadence profiles: 96;
- failed partition cadence profiles: 0;
- trade dates profiled: 3 (`2026-07-08`, `2026-07-09`, `2026-07-13`);
- symbols profiled: 32;
- total tick/update rows profiled: 1,238,275;
- total partition-profile elapsed seconds: 561.826513;
- slowest partition-profile elapsed seconds: 22.361562;
- median symbol-level tick/update rate: 0.791127 ticks/sec;
- median symbol-level p95 inter-update gap: 4,908.7 ms;
- maximum symbol-level p95 inter-update gap: 7,565.7 ms;
- Phase106 sampled-file cadence rows outside sampled/full comparison bands: 42;
- strategy replay allowed: 0;
- next best action: `use_phase154_full_partition_cadence_anchors_for_generator_calibration_contract`.

Current Phase154 date-level anchors:

- `2026-07-08`: 32 symbols, 226,430 rows, median symbol tick/update rate 0.744352/sec, min 0.270623/sec, max 1.606119/sec;
- `2026-07-09`: 32 symbols, 390,992 rows, median symbol tick/update rate 1.010363/sec, min 0.369570/sec, max 1.603423/sec;
- `2026-07-13`: 32 symbols, 620,853 rows, median symbol tick/update rate 0.820932/sec, min 0.368191/sec, max 1.601221/sec.

Current Phase154 interpretation: the older sampled-file cadence anchors are not safe calibration targets for tail inter-update gaps. All 42 sample-bias flags are `sampled_high_vs_full`, meaning sampled Phase106 p90/p95 gap values can greatly overstate full-partition p90/p95 gaps. Future generator cadence calibration should use the Phase154 full-partition cadence anchors, not the sampled Phase106 cadence rows.

Phase155 full-partition cadence calibration contract is implemented under `outputs/phase155/`.

**Runner:** `python scripts/run_phase155_full_partition_cadence_calibration_contract.py`

**Purpose:** convert Phase154 full-local-partition cadence anchors into an executable generator calibration contract. Phase155 supersedes sampled-file Phase106 cadence targets for cadence calibration only. It is local-only CSV contract work: no Azure read path, no synthetic shard generation, no order stream, no fills, no P&L, and no replay unlock.

Current Phase155 evidence records:

- Phase154 full-partition symbol cadence anchors available: 1;
- Phase106 calibrated synthetic anchor profile available: 1;
- symbols in cadence contract: 32;
- symbols requiring a cadence patch versus current Phase106 synthetic cadence: 31;
- symbols whose existing Phase106 synthetic cadence passes the Phase154 full-partition contract: 1;
- patch contract items emitted: 2;
- median required p95-gap multiplier versus Phase106 synthetic cadence: 6.315657;
- maximum required p95-gap multiplier versus Phase106 synthetic cadence: 8.839394;
- inherited Phase154 sample-bias rows: 42;
- strategy replay allowed: 0;
- next best action: `implement_symbol_aware_idle_tail_gap_model_then_rerun_phase155_contract`.

Current Phase155 patch contract:

- `symbol_aware_idle_tail_gap_model`: priority 1, affects 31 symbols, representative highest-multiplier symbols include `BRITANNIA`, `ITBEES`, `ULTRACEMCO`, `NESTLEIND`, `BPCL`, `CIPLA`, `BAJAJ-AUTO`, and `HINDUNILVR`.
- `phase106_cadence_anchor_source_rewire`: priority 2, affects all 32 symbols. Future Phase106-style cadence audits must use Phase154 full-partition cadence anchors rather than sampled Phase106 `real_anchor_profile` cadence rows.

Current Phase155 interpretation: the existing synthetic cadence is still too uniformly dense. HDFCBANK is the only symbol that passes the current Phase155 cadence contract without a cadence patch. The next generator milestone should implement a symbol-aware idle/tail inter-update gap model and then rerun Phase155 before any dense strategy replay gate is considered.

Phase156 symbol-aware tail cadence smoke is implemented under `outputs/phase156/`.

**Runner:** `python scripts/run_phase156_symbol_aware_tail_cadence_smoke.py --symbols ADANIPORTS AXISBANK BAJAJ-AUTO BANKBEES BHARTIARTL BPCL BRITANNIA CIPLA DRREDDY GOLDBEES HCLTECH HDFCBANK HINDUNILVR ICICIBANK INFY ITBEES ITC JUNIORBEES KOTAKBANK LT "M&M" MARUTI NESTLEIND NIFTYBEES ONGC RELIANCE SBIN SUNPHARMA TCS TECHM ULTRACEMCO WIPRO`

**Purpose:** implement and smoke-test `P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE`, a generator calibration profile that uses Phase155/Phase154 full-partition symbol p95 gap targets. Phase156 patches the dense materializer so symbol-specific p95 targets affect intra-source dense subtick gaps, not only sparse source-boundary gaps. It is a bounded local dense-materialization smoke: no Azure reads, no order stream, no fills, no P&L, and no replay unlock.

Current Phase156 evidence records:

- profile smoke-tested: `P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE`;
- smoke symbols: 32;
- dense smoke partition files materialized: 32;
- dense rows materialized: 16,838,528;
- compressed dense smoke bytes: 357,833,393;
- elapsed seconds: 50.910705;
- symbols whose p95 synthetic gap improved above Phase106 synthetic p95: 32;
- symbols within the Phase155 p95 target band `[0.5, 2.0]`: 32;
- strategy replay allowed: 0;
- next best action: `expand_phase156_profile_to_full_symbol_audit_then_rewire_phase106_cadence_anchors`.

Current Phase156 interpretation: the original source-boundary-only tail-gap hook was insufficient because source-boundary gaps are too rare in a 64x dense expansion to move p95. The Phase156 implementation now injects deterministic intra-source idle gaps at enough dense subtick transitions for p95 to match the full-partition targets. In the one-month, 32-symbol smoke, p95 ratios versus Phase155 targets were approximately 1.0 for every symbol, including HDFCBANK preservation at 1,250 ms. This is generator-calibration evidence only; strategy replay remains closed until Phase156 is expanded into the full-symbol/full-audit cadence-anchor rewire and the broader realism gates pass.

Phase157 full-partition cadence rewire audit is implemented under `outputs/phase157/`.

**Runner:** `python scripts/run_phase157_full_partition_cadence_rewire_audit.py`

**Purpose:** verify the cadence slice of future Phase106-style realism audits can be rewired from stale sampled-file cadence anchors to Phase154 full-local-partition cadence anchors. Phase157 is cadence-only: it does not claim spread, depth, imbalance, volatility, execution, fill, P&L, or strategy readiness.

Current Phase157 evidence records:

- Phase154 full-partition anchor available: 1;
- Phase155 cadence contract available: 1;
- Phase156 regenerated synthetic cadence profile available: 1;
- legacy Phase106 synthetic profile available for comparison: 1;
- symbols audited: 32;
- Phase156 p95 contract-band pass symbols: 32;
- Phase156 p95 exact-target pass symbols within 1 ms: 32;
- cadence-rewire pass symbols: 32;
- legacy sampled cadence-anchor stale symbols: 32;
- inherited Phase154 sample-bias rows: 42;
- inherited Phase156 dense smoke rows: 16,838,528;
- full-partition cadence rewire ready: 1;
- strategy replay allowed: 0;
- next best action: `run_phase106_style_full_realism_audit_with_phase157_cadence_contract_and_non_cadence_gates`.

Current Phase157 cadence metric source contract:

- `median_gap_ms`: anchor source `phase154_symbol_cadence_anchor.target_median_gap_ms`, ratio gate `[0.5,2.0]`;
- `p90_gap_ms`: anchor source `phase154_partition_cadence_profiles.target_median_p90_gap_ms`, ratio gate `[0.5,2.0]`;
- `p95_gap_ms`: anchor source `phase154_symbol_cadence_anchor.target_median_p95_gap_ms`, ratio gate `[0.5,2.0]`;
- `gap_le_1s_fraction`: anchor source `phase154_symbol_cadence_anchor.target_median_gap_le_1s_fraction`, diagnostic gate `absolute_delta <= 0.20`;
- non-cadence spread/depth/imbalance/volatility gates remain unchanged and outside the Phase157 cadence rewire.

Current Phase157 interpretation: the cadence rewire is ready for future Phase106-style audits, but only for cadence metrics. The old sampled Phase106 cadence anchor remains stale and must not be used for future cadence calibration. The next milestone should run a Phase106-style full realism audit using the Phase157 cadence contract while preserving the existing non-cadence gates.

Phase158 Phase106-style full realism audit with rewired cadence is implemented under `outputs/phase158/`.

**Runner:** `python scripts/run_phase158_phase106_style_full_realism_audit.py`

**Purpose:** rerun the Phase106-style realism decision using Phase157 full-partition cadence anchors for cadence metrics and preserving the existing Phase106 non-cadence gates for spread, depth, imbalance, and one-tick volatility. Phase158 is an audit only: no Azure reads, no strategy replay, no fills, and no P&L.

Current Phase158 evidence records:

- inherited Phase157 cadence rewire ready: 1;
- symbols compared: 32;
- symbol/metric anchor rows compared: 320;
- calibration gap rows: 87;
- calibration gap fraction: 0.271875;
- severe metric gap count: 2;
- cadence gap rows: 56;
- preserved non-cadence gap rows: 31;
- full rewired realism pass: 0;
- strategy replay allowed: 0;
- next best action: `fix_phase158_remaining_distributional_cadence_depth_imbalance_gaps_before_strategy_replay`.

Current Phase158 gap summary:

- `p95_gap_ms`: 0 / 32 gaps after Phase156/157, confirming the p95 full-partition cadence target was fixed;
- `p90_gap_ms`: 31 / 32 gaps, meaning Phase156 pins p95 but leaves the p90 cadence distribution too dense;
- `gap_le_1s_fraction`: 17 / 32 gaps, meaning the frequency of sub-1-second updates is still not distributionally realistic;
- `median_gap_ms`: 8 / 32 gaps, mainly slower symbols still pinned too close to the 500 ms dense baseline;
- `median_abs_l1_imbalance`: 15 / 32 gaps;
- `median_l5_depth`: 9 / 32 gaps;
- `median_l1_depth`: 7 / 32 gaps;
- `median_spread_bps`, `p90_spread_bps`, and `one_tick_return_std`: 0 / 32 gaps under preserved gates.

Current Phase158 interpretation: the p95 cadence repair worked, but full realism still fails. The next generator milestone should implement a distributional cadence model that matches p90, p95, median gap, and gap<=1s frequency together, while preserving the p95 repair and then revisiting the remaining depth/imbalance blockers. Strategy replay remains closed.

Phase159 distributional cadence smoke is implemented under `outputs/phase159/`.

**Runner:** `python scripts/run_phase159_distributional_cadence_smoke.py`

**Purpose:** implement and bounded-smoke a distributional cadence model that allocates deterministic dense subtick gaps to Phase155 median, p90, p95, and gap<=1s targets, instead of pinning p95 alone. Phase159 inherits the Phase156 profile as its base, adds `symbol_dense_gap_distribution_overrides`, and keeps the audit local-only: no Azure reads, no strategy replay, no fills, and no P&L.

Current Phase159 evidence records:

- profile smoke-tested: `P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE`;
- base profile: `P156_FULL_PARTITION_SYMBOL_TAIL_CADENCE`;
- smoke symbols: 32;
- dense rows materialized: 16,838,528;
- compressed dense smoke bytes: 357,615,839;
- elapsed seconds: 52.242869;
- inherited Phase157 cadence rewire ready: 1;
- symbol/metric anchor rows compared through the Phase158-style audit: 320;
- calibration gap rows: 39;
- calibration gap fraction: 0.121875;
- severe metric gap count: 0;
- cadence gap rows: 8;
- preserved non-cadence gap rows: 31;
- Phase158-style full rewired realism pass: 1;
- strategy replay allowed: 0.

Current Phase159 gap summary:

- `p90_gap_ms`: 0 / 32 gaps, improved from Phase158's 31 / 32;
- `p95_gap_ms`: 0 / 32 gaps, preserving the Phase156 p95 repair;
- `gap_le_1s_fraction`: 0 / 32 gaps, improved from Phase158's 17 / 32;
- `median_gap_ms`: 8 / 32 gaps remain, with median synthetic/real ratio median 1.0 but slow-symbol overshoots still present;
- preserved non-cadence blockers remain: `median_abs_l1_imbalance` 15 / 32, `median_l5_depth` 9 / 32, and `median_l1_depth` 7 / 32;
- `median_spread_bps`, `p90_spread_bps`, and `one_tick_return_std`: 0 / 32 gaps.

Current Phase159 interpretation: the distributional cadence model substantially repairs the cadence blocker and clears the Phase158-style full rewired realism threshold in a bounded one-month, 32-symbol smoke. This still does not open strategy replay: the next milestone should address remaining depth/imbalance and slow-symbol median-cadence gaps, then rerun a broader full-audit materialization before any synthetic-only strategy experiment is re-enabled.

Phase160 Phase159 generated non-cadence realism audit is implemented under `outputs/phase160/`.

**Runner:** `python scripts/run_phase160_phase159_noncadence_realism_audit.py`

**Purpose:** profile spread, visible depth, L1 imbalance, and one-tick volatility from the actual Phase159 generated dense parquet shards, then compare them to the existing real non-cadence anchors. Phase160 replaces stale non-cadence assumptions from older Phase106 comparison rows with generated-shard evidence. It is local-only and still does not run strategy replay, fills, P&L, or Azure reads.

Current Phase160 evidence records:

- symbols compared: 32;
- non-cadence symbol/metric rows compared: 192;
- calibration gap rows: 0;
- calibration gap fraction: 0.0;
- severe metric gap count: 0;
- Phase159 dense rows profiled: 16,838,528;
- generated non-cadence realism pass: 1;
- strategy replay allowed: 0;
- next best action: `combine_phase159_cadence_and_phase160_noncadence_acceptance_then_plan_broader_materialization`.

Current Phase160 generated non-cadence gap summary:

- `median_spread_bps`: 0 / 32 gaps;
- `p90_spread_bps`: 0 / 32 gaps;
- `median_l1_depth`: 0 / 32 gaps;
- `median_l5_depth`: 0 / 32 gaps;
- `median_abs_l1_imbalance`: 0 / 32 gaps;
- `one_tick_return_std`: 0 / 32 gaps.

Current Phase160 interpretation: the apparent Phase159 depth/imbalance blockers were stale inherited Phase106 comparison rows, not failures in the actual Phase159 generated dense shard. The generated Phase159 non-cadence profile passes all preserved non-cadence gates in the bounded 32-symbol smoke. Strategy replay still remains closed because the combined proof is bounded to one generated month and the Phase159 cadence audit still has 8 / 32 median-gap edge cases. The next milestone should produce a combined Phase159+Phase160 acceptance gate and decide whether to broaden materialization before any synthetic-only strategy replay is reconsidered.

Phase161 combined realism handoff gate is implemented under `outputs/phase161/`.

**Runner:** `python scripts/run_phase161_combined_realism_handoff_gate.py`

**Purpose:** combine Phase159 distributional cadence evidence with Phase160 generated non-cadence evidence and decide whether the bounded generated shard is ready for broader materialization/audit. Phase161 is a handoff gate only: it does not run strategy replay, fills, P&L, or Azure reads.

Current Phase161 evidence records:

- inherited Phase159 Phase158-style full rewired realism pass: 1;
- inherited Phase160 generated non-cadence realism pass: 1;
- combined symbols: 32;
- combined cadence plus generated non-cadence anchor rows: 320;
- combined gap rows: 8;
- combined gap fraction: 0.025;
- combined severe metric gap count: 0;
- cadence gap rows: 8;
- generated non-cadence gap rows: 0;
- bounded realism handoff pass: 1;
- smoke months materialized: 1;
- broader materialization required: 1;
- strategy replay allowed: 0;
- next best action: `materialize_phase159_distributional_profile_all_12_months_then_rerun_combined_audit`.

Current Phase161 broader materialization plan:

- materialize `P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE` for all 12 synthetic months and all 32 symbols;
- current bounded smoke size: 1 month, 32 symbols, 16,838,528 rows, 357,615,839 compressed bytes;
- estimated 12-month generated profile size: 202,062,336 rows and 4,291,390,068 compressed bytes;
- rerun Phase159/Phase160-style audits on the broader materialization;
- consider synthetic-only strategy replay preflight only after the broader materialization and combined audit pass.

Current Phase161 interpretation: the bounded generated shard passes the combined realism handoff gate, but it is not enough to reopen strategy replay. The next milestone is broader 12-month materialization with the Phase159 distributional cadence profile, followed by rerunning the combined audit on that broader generated dataset.

Phase162 Phase159 full-year materialization audit is implemented under `outputs/phase162/`.

**Runner:** `python scripts/run_phase162_phase159_full_year_materialization_audit.py --max-months 0`

**Purpose:** materialize the Phase159 distributional cadence profile across the full local compact synthetic year, then rerun cadence plus generated non-cadence realism checks on the broader generated parquet dataset. Phase162 is explicitly local/download-first: it does not stream Azure files through Python, does not run strategy replay, does not simulate fills or P&L, and does not make profitability claims.

Current Phase162 evidence records:

- profile id: `P159_DISTRIBUTIONAL_FULL_PARTITION_CADENCE`;
- months materialized: 12;
- symbols materialized: 32;
- dense month/symbol partition files: 384;
- expected partition files: 384;
- missing partition files: 0;
- dense rows materialized: 192,786,816;
- compressed dense bytes: 4,141,341,739;
- elapsed seconds: 610.819;
- combined cadence plus generated non-cadence anchor rows: 320;
- combined gap rows: 12;
- combined gap fraction: 0.0375;
- combined severe metric gap count: 0;
- cadence gap rows: 8;
- generated non-cadence gap rows: 4;
- full-year realism audit pass: 1;
- strategy replay allowed: 0;
- Azure read policy: `forbidden_for_analysis_download_first_then_local`;
- next best action: `review_full_year_materialization_then_prepare_synthetic_only_replay_preflight_if_accepted`.

Current Phase162 combined metric gate:

- `median_gap_ms`: 8 / 32 cadence gaps, gap fraction 0.25, metric gate pass 1;
- `one_tick_return_std`: 4 / 32 generated non-cadence gaps, gap fraction 0.125, metric gate pass 1;
- `gap_le_1s_fraction`: 0 / 32 cadence gaps;
- `p90_gap_ms`: 0 / 32 cadence gaps;
- `p95_gap_ms`: 0 / 32 cadence gaps;
- `median_spread_bps`: 0 / 32 generated non-cadence gaps;
- `p90_spread_bps`: 0 / 32 generated non-cadence gaps;
- `median_l1_depth`: 0 / 32 generated non-cadence gaps;
- `median_l5_depth`: 0 / 32 generated non-cadence gaps;
- `median_abs_l1_imbalance`: 0 / 32 generated non-cadence gaps.

Current Phase162 interpretation: the broader 12-month local materialization replaces the Phase161 one-month smoke with full-year generated parquet evidence. The broader realism audit passes with a 3.75% combined gap fraction and zero severe metric gaps. This is a generator/materialization acceptance result only. It keeps `strategy_replay_allowed=0`; the next milestone should be a review/preflight checkpoint that decides whether a synthetic-only strategy replay may be opened under the already-agreed synthetic-only acceptance path.

Phase163 synthetic-only replay preflight is implemented under `outputs/phase163/`.

**Runner:** `python scripts/run_phase163_synthetic_only_replay_preflight.py`

**Purpose:** decide whether the Phase162 full-year generated L2 lake can be used for guarded synthetic-only replay diagnostics. Phase163 does not run P&L replay itself. It opens only synthetic-only replay execution for the next phase, enforces the Phase116 blocklist, excludes the closed Phase136 top-five-depth passive branch, keeps strategy promotion closed, keeps broker/paper/live acceptance closed and preserves the download-first/local-only Azure boundary.

Current Phase163 evidence records:

- required preflight gate rows: 8;
- required preflight gates passed: 8;
- synthetic-only replay preflight pass: 1;
- synthetic-only replay execution allowed: 1;
- Phase162 months available: 12;
- Phase162 dense rows available: 192,786,816;
- Phase162 dense bytes available: 4,141,341,739;
- replay work queue rows: 11;
- alpha replay diagnostic rows allowed: 9;
- control/risk-plumbing rows allowed: 2;
- Phase116 blocklisted family rows enforced: 7;
- strategy promotion allowed: 0;
- paper/live broker acceptance allowed: 0;
- Azure read policy: `forbidden_for_analysis_download_first_then_local`;
- next best action: `implement_phase164_synthetic_only_full_year_replay_on_phase162_data`.

Current Phase163 required gate ledger:

- `phase162_full_year_materialization_passed`: pass;
- `phase162_full_year_scope_complete`: pass;
- `phase162_dense_parquet_root_present`: pass;
- `phase39_synthetic_only_experiment_policy_open`: pass;
- `broker_paper_live_acceptance_remains_closed`: pass;
- `strategy_promotion_still_not_open`: pass;
- `phase116_blocklist_present_and_enforced`: pass;
- `phase136_deep_book_branch_closed`: pass.

Current Phase163 replay contract:

- contract id: `P164_SYNTHETIC_ONLY_FULL_YEAR_REPLAY`;
- contract status: `open_for_implementation`;
- input dense root: `raw_synthetic_l2_phase162_distributional_full_year`;
- input inventory: `outputs/phase162/phase162_dense_full_year_inventory.csv`;
- allowed scope: `synthetic_only_replay_diagnostics`;
- allowed strategy rows: 9;
- control rows: 2;
- excluded blocklist rows: 7;
- required cost model: `zerodha_equity_intraday_nse_order_formula_v2_2026_07_14_or_successor_with_documented_components`;
- required execution profiles: `zero_latency_control;retail_marketable_default;stressed_retail`;
- forbidden outputs: broker acceptance, paper/live readiness, contract-note reconciliation claims, promoted buy/sell signals and deployable profitability claims.

Current Phase163 interpretation: the full-year generated dataset is now accepted for guarded synthetic-only replay diagnostics. This is the first post-Phase162 unlock: it opens implementation of Phase164 synthetic-only full-year replay on Phase162 data, while explicitly excluding the old blocklisted dense-market-form continuation and preserving all no-promotion/no-broker boundaries.

Phase164 synthetic-only full-year replay is started under `outputs/phase164/`.

**Runner:** `python scripts/run_phase164_synthetic_only_full_year_replay.py --output-dir outputs/phase164 --stop-after-new-shards <N>`

**Purpose:** replay guarded S01-S11 diagnostic strategy families over the Phase162 full-year generated dense L2 lake using local DuckDB scans, Phase12 execution profiles and the Zerodha equity intraday NSE charge formula. Phase164 is resumable by shard. It emits an aggregate trade ledger, daily/symbol/profile strategy summaries, risk summary, acceptance summary, strategy catalog, report and manifest. It is synthetic-only diagnostic evidence only: broker acceptance, paper/live readiness, contract-note reconciliation claims, promoted buy/sell signals and deployable profitability claims remain forbidden.

Current Phase164 checkpoint evidence records:

- Phase162 dense shards scanned: 384 / 384;
- full-year replay complete: 1;
- strategy/profile rows: 24;
- aggregate synthetic-only replay trade count: 7,611,950;
- positive-after-cost strategy/profile rows: 0;
- synthetic replay candidate rows: 0;
- cost model version: `zerodha_equity_intraday_nse_order_formula_v2_2026_07_14`;
- strategy promotion allowed: 0;
- paper/live broker acceptance allowed: 0;
- deployable profitability claim allowed: 0;
- next best action: `continue_phase164_until_full_year_complete_then_verdict`.

Current Phase164 strategy catalog:

- `P164_S01_MLOFI_BREAKOUT`: replayable from local L1-L5 book state;
- `P164_S02_MULTI_LEVEL_OFI`: replayable from local L1-L5 book state;
- `P164_S03_LIQUIDITY_VACUUM`: replayable from local L1-L5 book state;
- `P164_S04_TRADE_FLOW_DEPTH`: replayable from local L1-L5 book state;
- `P164_S05_MICROPRICE_FILTER`: replayable from local L1-L5 book state;
- `P164_S06_ABSORPTION_REVERSAL`: replayable from local L1-L5 book state;
- `P164_S07_IMBALANCE_MEAN_REVERSION`: replayable from local L1-L5 book state;
- `P164_S08_CROSS_SYMBOL_LEAD_LAG_PLACEHOLDER`: not replayable in isolated symbol-shard scans; requires a cross-symbol month cache;
- `P164_S09_QUEUE_IMBALANCE_SCALP`: guarded queue-imbalance replay that does not reuse the old Phase52 dense strategy id;
- `P164_S10_PASSIVE_CONTROL_NO_ALPHA`: control-only/no-alpha replay;
- `P164_S11_RISK_FILTER_CONTROL_NO_ALPHA`: control-only/no-alpha replay.

Current Phase164 implementation note: the resumable runner now normalizes shard paths before comparing the existing aggregate ledger to the Phase162 inventory and de-duplicates aggregate ledger keys before summarizing. This fixed the Windows path separator mismatch that initially caused a same-64-shard replay attempt.

Current Phase164 interpretation: the completed 384 / 384 Phase162 shard replay shows no positive-after-cost strategy/profile rows and no synthetic replay candidates. The best observed Phase164 profile is `P164_S06_ABSORPTION_REVERSAL` under `zero_latency_spread_only_control`, with annual net P&L of -189,512.606 INR. This completes the Phase164 full-year replay evidence and requires a verdict phase rather than continued replay of the same forms.

Phase165 Phase164 full-year replay verdict is implemented under `outputs/phase165/`.

**Runner:** `python scripts/run_phase165_phase164_full_year_replay_verdict.py`

**Purpose:** convert completed Phase164 full-year synthetic-only replay evidence into a decision. Phase165 does not promote strategies, does not claim paper/live readiness, and does not claim deployable profitability.

Current Phase165 evidence records:

- outcome: `A_SYNTHETIC_FULL_YEAR_REPLAY_FALSIFIED`;
- decision: `close_phase164_current_guarded_diagnostic_forms`;
- inherited Phase164 full-year complete: 1;
- inherited Phase164 positive-after-cost rows: 0;
- inherited Phase164 synthetic replay candidate rows: 0;
- best strategy/profile: `P164_S06_ABSORPTION_REVERSAL` / `zero_latency_spread_only_control`;
- best annual net P&L: -189,512.606 INR;
- strategy promotion allowed: 0;
- paper/live broker acceptance allowed: 0;
- deployable profitability claim allowed: 0;
- next best action: `stop_current_phase164_strategy_forms_or_design_new_precommitted_non_blocklisted_hypothesis`.

Current Phase165 gate evaluation:

- `P165_FULL_YEAR_REPLAY_COMPLETE`: pass, observed 384 / required 384;
- `P165_POSITIVE_AFTER_COST_ECONOMICS`: fail, observed 0 / required >0 strategy/profile rows;
- `P165_SYNTHETIC_REPLAY_CANDIDATE`: fail, observed 0 / required >0 positive plus risk-proxy-pass rows;
- `P165_BEST_PROFILE_NET_POSITIVE`: fail, observed -189,512.606 INR / required >0 INR annual net P&L;
- `P165_PROMOTION_BOUNDARY_CLOSED`: pass;
- `P165_BROKER_BOUNDARY_CLOSED`: pass;
- `P165_DEPLOYABLE_CLAIM_CLOSED`: pass.

Current Phase165 blocklist-candidate update marks current Phase164 forms for S01, S02, S03, S04, S05, S06, S07 and S09 as `block_current_phase164_form`. S08 was not replayable in the isolated symbol-shard scan and requires a cross-symbol month cache before any valid lead-lag replay. S10 and S11 remain non-alpha control/risk-plumbing rows.

Phase166 cross-symbol lead-lag cache is implemented under `outputs/phase166/`.

**Runner:** `python scripts/run_phase166_cross_symbol_lead_lag_cache.py --output-root raw_synthetic_l2_phase166_cross_symbol_lead_lag_cache --output-dir outputs/phase166`

**Purpose:** materialize the missing local cross-symbol month cache required before any valid S08 lead-lag replay. Phase166 reads the already-materialized Phase162 dense synthetic L2 Parquet locally and writes month-partitioned synchronized feature-cache Parquet. It does not scan Azure directly, does not run a strategy, does not emit P&L, and does not unlock broker/paper/live acceptance.

Current Phase166 evidence records:

- source data policy: `forbidden_for_analysis_download_first_then_local`;
- synchronization bucket: 5,000 ms;
- bucket interpretation: alignment device only, not a claim that native tick data is uniformly sampled;
- months cached: 12;
- cache files: 12;
- symbols cached: 32;
- source dense rows represented: 192,786,816;
- synchronized symbol/bucket rows: 77,944,215;
- compressed cache bytes: 4,635,703,054;
- median lag-1 feature coverage: 0.9929824537245444;
- S08 cache ready: 1;
- strategy replay allowed: 0;
- next best action: `precommit_and_run_s08_cross_symbol_lead_lag_replay_using_phase166_cache`.

Current Phase166 interpretation: the S08 blocker identified by Phase165 is now removed at the data-cache level. The local cache contains market ex-target, sector ex-target, ETF pressure/return, lag-1/lag-2 bucket features and next-bucket target returns across the 32-symbol full-year synthetic L2 lake. This is not a profitability result; it is a prerequisite artifact for a later precommitted S08 replay phase.

### Phase 133 — Retail Passive Execution Model Upgrade

**Runner:** `scripts/run_phase133_passive_execution_model_upgrade.py`

**Outputs:** `outputs/phase133/`

**Purpose:** upgrade the passive fill model before any passive strategy precommit. Deep visible-book information can only matter economically for retail if passive posting is modelled realistically.

**Required deliverables:**

- `phase133_execution_contract.json`, pinned and immutable for later phases in this continuation.
- A fill-probability model of `P(fill | queue_position, depth_level, cancel_intensity, latency_ms)` derived from Phase6 generator add/cancel statistics and Phase131 depth-level features.
- A retail latency jitter distribution with 50-350 ms central mass and a fat right tail, pinned in the contract file.
- Per-depth-level cancel-intensity inputs from Phase131 features.
- A sanity replay of the Phase89 passive queue-capture cost-floor experiment under the new fill model.

**Acceptance:** no new strategies. The phase ships the execution model and validates that its Phase89 sanity replay remains directionally consistent with prior passive-expense evidence. If the sanity replay contradicts Phase89 directionally, Phase134 must not open.

**Current implementation evidence:** Phase133 is implemented and executed under `outputs/phase133/`.

Current outputs include:

- `phase133_execution_contract.json`;
- `phase133_phase6_generator_anchor.csv`;
- `phase133_latency_distribution.csv`;
- `phase133_cancel_intensity_inputs.csv`;
- `phase133_fill_probability_catalog.csv`;
- `phase133_phase89_sanity_replay.csv`;
- `phase133_gate_evaluation.csv`;
- `phase133_passive_execution_model_upgrade_acceptance_summary.csv`;
- `phase133_passive_execution_model_upgrade_report.md`;
- `phase133_passive_execution_model_upgrade_manifest.json`.

Current Phase133 evidence records:

- hard gates evaluated: 5;
- hard gates passed: 5;
- pinned execution contract created: 1;
- inherited Phase132 kill-switch fired: 1;
- inherited Phase132 surviving feature rows: 0;
- Phase89 sanity rows re-evaluated: 54;
- best Phase133 sanity test expected net P&L: `-23,942.0570 INR`;
- worst Phase133 sanity test expected net P&L: `-2,245,206.1422 INR`;
- Phase134 open allowed: 0;
- strategy replay allowed: 0;
- next best action: `stop_update_phase116_blocklist_do_not_open_phase134`.

The contract explicitly uses the correct terminology: Zerodha scope is Level-2/top-five market-by-price data, while `depth_level_1..depth_level_5` are visible aggregated book price levels, not L1-L5 market-data tiers.

The Phase6 generator anchor records:

- source rows: 453,600;
- book-state-update fraction: 0.874063;
- spread-widening fraction: 0.085745;
- best-price-shift fraction: 0.025082;
- median event-intensity proxy: 1.400818;
- median L5 quantity: 398.5;
- capped fill-probability scale: 1.25.

Phase133 therefore improves the simulator execution contract, but it does **not** revive the Phase132-killed deep-book strategy branch.

### Phase 134 — Precommitted Top-Five-Depth Passive Strategy Family

**Runner:** `scripts/run_phase134_deep_book_passive_strategy_precommit.py`

**Outputs:** `outputs/phase134/`

**Purpose:** register 2-3 passive strategy definitions before any bounded replay.

**Rules:**

- 2-3 strategies maximum.
- Each strategy must consume at least one Phase132 surviving top-five-depth feature.
- Entry must be passive/post-only; marketable entry orders are forbidden.
- Gates must be pre-registered per strategy:
  - minimum 5,000 trades across the allowed-context matrix;
  - minimum out-of-sample Sharpe under both `base` and `harsh` cost regimes;
  - failure if either cost regime is negative;
  - no cost-stress ordering reversal;
  - at least 50% of months net positive under `harsh`;
  - no positive-pockets exception;
  - explicit blocklist unlock condition if falsified.

**Acceptance:** manifest locks strategy IDs, gates, allowed datasets and forbidden outputs. No replay is executed in Phase134.

### Phase 135 — Bounded Synthetic Replay

**Runner:** `scripts/run_phase135_deep_book_passive_bounded_replay.py`

**Outputs:** `outputs/phase135/`

**Purpose:** run exactly one bounded synthetic replay of the Phase134 strategies over the recalibrated dense lake, using the Phase133 execution model and both Phase131 cost regimes.

**Rules:**

- Single run only.
- No parameter sweeps.
- No re-fits after seeing results.
- Full trade-level output plus per-symbol and per-month decomposition under `base` and `harsh` regimes side by side.
- `strategy_replay_allowed` remains `0`.
- No promoted profitability claim in any report.

**Acceptance:** every Phase134 gate is evaluated exactly as written, including explicit cost-stress ordering-reversal checks.

### Phase 136 — Verdict, Blocklist Update and Handoff Artifact

**Runner:** `scripts/run_phase136_deep_book_verdict_and_handoff.py`

**Outputs:** `outputs/phase136/`

**Purpose:** close the top-five-depth passive branch cleanly with exactly one outcome.

**Outcome A — Falsified:**

- Triggered by any Phase134 gate failure under `harsh`, any cost-stress ordering reversal, or the Phase132 kill-switch.
- Append/update the Phase116 strategy replay blocklist with the relevant deep-book/top-five-depth passive falsification entry.
- Write a markdown verdict declaring synthetic-only strategy hunting terminated. Further strategy work waits on real anchor L2 through Phases113-115.

**Outcome B — Marginal handoff:**

- Triggered if all gates pass under both regimes but effect size or coverage is thin.
- Emit `phase136_real_l2_precommit_handoff.json` containing:
  - Phase131 surviving feature definitions;
  - Phase133 execution-model parameters;
  - Phase134 strategy definitions and gates unchanged;
  - `base` and `harsh` cost regimes;
  - the ordering-reversal rule.
- Do not change `strategy_replay_allowed`.

**Outcome C — Clean synthetic survivor with advisory:**

- Triggered if all gates pass with margin under `harsh` and no ordering reversal occurs.
- Emit the same handoff artifact as Outcome B.
- Add `phase136_synthetic_survivor_advisory.md` explaining that synthetic-only survival is not deployable evidence and must be re-tested on real Zerodha L2 before any replay unlock.
- Do not change `strategy_replay_allowed`.

**Acceptance:** exactly one outcome document is produced. Outcome A verifies the blocklist update against Phase116. Outcomes B and C validate the handoff JSON against the real-anchor schema so it can be re-evaluated once real L2 lands through the Phase113-115 drop-zone pipeline.

**Current implementation evidence:** Phase136 is implemented and executed under `outputs/phase136/`.

Current outputs include:

- `phase136_deep_book_verdict.json`;
- `phase136_deep_book_clean_falsification_verdict.md`;
- `phase136_blocklist_verification.csv`;
- `phase136_gate_evaluation.csv`;
- `phase136_deep_book_verdict_acceptance_summary.csv`;
- `phase136_deep_book_verdict_manifest.json`.

Current Phase136 evidence records:

- hard closure-verdict gates evaluated: 8;
- hard closure-verdict gates passed: 8;
- selected outcome: `A_CLEAN_FALSIFICATION`;
- clean falsification selected: 1;
- inherited Phase132 kill-switch fired: 1;
- inherited Phase132 surviving feature rows: 0;
- inherited Phase133 Phase134-open flag: 0;
- Phase116 blocklist entry `DEEP_BOOK_LABEL_LIFT` verified with blocked strategy id `phase131_phase132_top_five_depth_feature_diagnostics`;
- strategy replay allowed: 0;
- next best action: `wait_for_real_l2_anchor_unlock_or_start_new_precommitted_non_blocklisted_research_branch`.

Phase136 therefore closes the Phase131-136 top-five-depth passive branch. It emits no Phase134 precommit, no Phase135 replay, no buy/sell signal, no order-arrival stream, no live-tagged fill model, and no deployable profitability claim.

### Forbidden actions inside Phase131-136

The continuation forbids:

- reopening Level-1/top-of-book-only taker families;
- vendor backfill of historical L2 data;
- expanding beyond the current 32-symbol universe;
- changing the pinned Zerodha base cost model or editing the harsh-regime factors after Phase131;
- flipping `strategy_replay_allowed` from any phase in this continuation;
- emitting promoted buy/sell signals, order-arrival streams, live-tagged fill models, P&L replay or deployable profitability claims;
- RL, meta-learning or ensembles on top of Phase134 strategies before Phase136 verdict;
- adding new synthetic scenario diversity beyond the existing realism audit while this continuation is running.

### Success definition for Phase131-136

Success is not a profitable synthetic strategy. Success is one clean conclusion:

1. **Clean falsification:** Phase132 kill-switch or Phase136 Outcome A closes the synthetic top-five-depth passive branch and updates the blocklist.
2. **Marginal handoff:** Outcome B produces a dormant real-L2 precommit artifact.
3. **Synthetic survivor with advisory:** Outcome C produces the same handoff plus an explicit warning that synthetic evidence alone is not deployable.

Prolonging the branch to force a positive result is explicitly not success.

---

## 24A. Synthetic-only Continuation After Phase165

Phase165 closed the Phase164 full-year synthetic-only replay as falsified. The current Phase164 strategy forms produced no positive after-cost rows and no synthetic replay candidates, so those forms must not be kept alive by shard-after-shard reruns.

The next non-blocklisted path is the previously incomplete cross-symbol lead-lag branch. Phase164 could not fairly test S08 in isolated symbol/month shards because S08 needs a synchronized cross-symbol feature view. The continuation therefore proceeds through a cache-preparation milestone first, not through an immediate profitability verdict.

### Data-access rule for Azure and real L2

Heavy L2 analysis must be download-first/local-first:

- Azure storage may be used as a source of raw real L2 files.
- Python strategy/cache/replay code must not stream-scan Azure directly for heavy experiments.
- Downloaded or already materialized local Parquet is the analysis substrate.
- DuckDB is the preferred local scan/cache engine for dense tick/L2 experiments.

This avoids turning every experiment into remote object-store latency and keeps replay evidence reproducible from local paths.

### Phase166 — Cross-symbol Lead-lag Cache for S08

**Runner:** `scripts/run_phase166_cross_symbol_lead_lag_cache.py`

**Implementation:** `src/synthetic_l2/phase166_cross_symbol_lead_lag_cache.py`

**Outputs:** `outputs/phase166/`

**Local cache root:** `raw_synthetic_l2_phase166_cross_symbol_lead_lag_cache/`

**Purpose:** build a synchronized local feature cache from the Phase162 full-year dense L2 lake so S08 cross-symbol lead-lag can be tested without pretending isolated symbol shards contain cross-symbol information.

**Important terminology:** the Phase166 `5000 ms` bucket is a synchronization/alignment device. It is not a claim that the native Zerodha-like websocket feed is uniformly sampled at 5 seconds. Native tick rows remain event/tick updates; Phase166 aggregates them into cross-symbol buckets for lagged feature construction.

**Current implementation evidence:** Phase166 is implemented and executed.

Current outputs include:

- `phase166_cross_symbol_cache_acceptance_summary.csv`;
- `phase166_cross_symbol_cache_inventory.csv`;
- `phase166_cross_symbol_cache_sample.csv`;
- `phase166_cross_symbol_lead_lag_cache_manifest.json`;
- `phase166_cross_symbol_lead_lag_cache_report.md`.

Current Phase166 evidence records:

- bucket size: `5000 ms`;
- months cached: `12`;
- monthly cache files: `12`;
- symbols cached: `32`;
- source dense rows represented: `192,786,816`;
- synchronized symbol/bucket rows: `77,944,215`;
- compressed cache bytes: `4,635,703,054`;
- median lag-1 feature coverage: `0.9929824537245444`;
- S08 cache ready: `1`;
- strategy replay allowed: `0`;
- Azure read policy: `forbidden_for_analysis_download_first_then_local`;
- next best action: `precommit_and_run_s08_cross_symbol_lead_lag_replay_using_phase166_cache`.

Phase166 does not produce a P&L result, promoted signal, order-arrival stream, fill verdict, or deployable profitability claim. It only prepares the synchronized local feature substrate required for a fair S08 replay.

### Phase167 — Precommitted S08 Cross-symbol Replay

**Runner:** `scripts/run_phase167_s08_cross_symbol_lead_lag_replay.py`

**Implementation:** `src/synthetic_l2/phase167_s08_cross_symbol_lead_lag_replay.py`

**Outputs:** `outputs/phase167/`

Phase167 uses the Phase166 local cache to run exactly one precommitted cross-symbol lead-lag replay branch. It must:

- read from `raw_synthetic_l2_phase166_cross_symbol_lead_lag_cache/`, not Azure;
- preserve the Zerodha equity intraday NSE cost model used by Phase164 for execution-cost accounting;
- model feed event, feature update, signal, latency, order arrival, fill, costs, and P&L/risk update before any verdict;
- report base and adverse latency/cost variants side by side;
- emit full trade-level, symbol-level, month-level, and strategy/profile-level evidence;
- keep paper/live acceptance and strategy promotion closed unless the precommitted gates explicitly pass;
- update the blocklist if S08 is falsified.

Success is not a positive synthetic chart. Success is a clean Phase167 verdict: S08 either survives a precommitted full-year synthetic-only replay as a dormant real-L2 handoff candidate, or it is falsified and blocked like the earlier Phase164 forms.

Current Phase167 outputs include:

- `phase167_s08_cross_symbol_trade_ledger.parquet`;
- `phase167_s08_replay_acceptance_summary.csv`;
- `phase167_s08_strategy_profile_summary.csv`;
- `phase167_s08_gate_evaluation.csv`;
- `phase167_s08_split_summary.csv`;
- `phase167_s08_monthly_summary.csv`;
- `phase167_s08_symbol_summary.csv`;
- `phase167_execution_profile_catalog.csv`;
- `phase167_zerodha_charge_component_catalog.csv`;
- `phase167_s08_cross_symbol_replay_report.md`;
- `phase167_s08_cross_symbol_replay_manifest.json`.

Current Phase167 evidence records:

- source cache ready: 1;
- cache files scanned: 12;
- strategy id: `P167_S08_CROSS_SYMBOL_LEAD_LAG_CONTINUATION`;
- score threshold: 0.42 fixed before replay;
- execution profile rows: 3;
- full trade-level rows: 817,814;
- positive-after-cost profile rows: 0;
- candidate profile rows: 0;
- best execution profile: `zero_latency_spread_only_control`;
- best annual net P&L: -4,143,898.966 INR;
- Zerodha-cost retail default annual net P&L: -28,251,117.745 INR;
- stressed retail annual net P&L: -32,502,523.595 INR;
- cost model version: `zerodha_equity_intraday_nse_order_formula_v2_2026_07_14`;
- strategy promotion allowed: 0;
- paper/live broker acceptance allowed: 0;
- deployable profitability claim allowed: 0;
- Azure read policy: `forbidden_for_analysis_download_first_then_local`;
- next best action: `close_s08_current_form_and_update_blocklist_candidate`.

Current Phase167 gate interpretation: S08 fails even under the zero-latency spread-only control and fails all realistic Zerodha-cost execution profiles by a larger margin. The replay has no positive train split, no positive test split, no positive test months, no candidate profile rows and no promotion path. The current S08 form should therefore be closed by a follow-on blocklist/verdict ledger rather than rerun.

### Phase168 — S08 Closure Verdict and Blocklist Candidate

**Runner:** `scripts/run_phase168_s08_closure_verdict.py`

**Implementation:** `src/synthetic_l2/phase168_s08_closure_verdict.py`

**Outputs:** `outputs/phase168/`

Phase168 converts the Phase167 full-year S08 replay evidence into a closure decision. It does not run a new strategy and does not alter the Phase167 replay result.

Current Phase168 outputs include:

- `phase168_s08_closure_acceptance_summary.csv`;
- `phase168_s08_closure_gate_evaluation.csv`;
- `phase168_s08_closure_verdict.csv`;
- `phase168_s08_blocklist_candidate_update.csv`;
- `phase168_s08_closure_verdict_report.md`;
- `phase168_s08_closure_manifest.json`.

Current Phase168 evidence records:

- outcome: `A_S08_CURRENT_FORM_FALSIFIED`;
- decision: `close_s08_current_cross_symbol_lead_lag_form`;
- closure gates passed: 10 / 10;
- blocklist candidate rows: 1;
- inherited Phase167 trade rows: 817,814;
- inherited Phase167 positive-after-cost profile rows: 0;
- inherited Phase167 candidate profile rows: 0;
- best execution profile: `zero_latency_spread_only_control`;
- best annual net P&L: -4,143,898.966 INR;
- recommended status: `block_current_phase167_s08_form`;
- strategy promotion allowed: 0;
- paper/live broker acceptance allowed: 0;
- deployable profitability claim allowed: 0;
- next best action: `design_new_precommitted_non_blocklisted_hypothesis_or_wait_for_real_l2_anchor`.

Current Phase168 interpretation: the current S08 cross-symbol lead-lag form is now closed. It must not be rerun shard-after-shard in the same form hoping for profit. Reopening cross-symbol work requires a new precommitted feature form, a materially different label/execution contract, or real-anchor evidence.

### Phase169 — Post-S08 Research Queue

**Runner:** `scripts/run_phase169_post_s08_research_queue.py`

**Implementation:** `src/synthetic_l2/phase169_post_s08_research_queue.py`

**Outputs:** `outputs/phase169/`

Phase169 consolidates the current closure state and emits the next safe research queue. It is a guardrail/queue phase only: it does not run a strategy, does not open replay, and does not create a profitability claim.

Current Phase169 outputs include:

- `phase169_post_s08_research_queue_acceptance_summary.csv`;
- `phase169_closure_evidence_ledger.csv`;
- `phase169_forbidden_family_ledger.csv`;
- `phase169_candidate_source_evaluation.csv`;
- `phase169_next_research_queue.csv`;
- `phase169_research_queue_gate_evaluation.csv`;
- `phase169_post_s08_research_queue_report.md`;
- `phase169_post_s08_research_queue_manifest.json`.

Current Phase169 evidence records:

- closure rows consolidated: 5;
- forbidden family/form rows: 9;
- candidate source rows evaluated: 3;
- selected synthetic source: `P130_FILTER_CONDITIONED_DIAGNOSTICS`;
- next queue rows: 2;
- gates passed: 5 / 5;
- strategy replay allowed: 0;
- paper/live acceptance allowed: 0;
- Azure read policy: `forbidden_for_analysis_download_first_then_local`;
- next best action: `implement_phase170_filter_conditioned_feasibility_matrix_no_replay`.

Current Phase169 interpretation: the only synthetic-only continuation allowed after Phase168 is a no-replay, filter-conditioned feasibility matrix using the Phase130 diagnostic filter source. The parallel priority remains real-anchor acquisition using download-first/local-first data handling. Reopening Phase164 or Phase167 forms is explicitly blocked.

### Phase170 — Filter-conditioned Feasibility Matrix

**Runner:** `scripts/run_phase170_filter_conditioned_feasibility_matrix.py`

**Implementation:** `src/synthetic_l2/phase170_filter_conditioned_feasibility_matrix.py`

**Outputs:** `outputs/phase170/`

Phase170 converts the Phase129/Phase130 diagnostic-filter artifacts into a no-replay context feasibility matrix. It emits context tiers only. It does not emit buy/sell signals, order-arrival streams, fill models, P&L replay, or profitability claims.

Current Phase170 outputs include:

- `phase170_filter_conditioned_feasibility_acceptance_summary.csv`;
- `phase170_filter_conditioned_context_matrix.csv`;
- `phase170_context_tier_summary.csv`;
- `phase170_diagnostic_model_evidence.csv`;
- `phase170_blocked_family_overlap_audit.csv`;
- `phase170_feasibility_gate_evaluation.csv`;
- `phase170_filter_conditioned_feasibility_matrix_report.md`;
- `phase170_filter_conditioned_feasibility_matrix_manifest.json`.

Current Phase170 evidence records:

- context matrix rows: 228;
- strict stable + liquid + non-toxic context rows: 6;
- strict context symbols: 3;
- strict context months: 5;
- stable + non-toxic rows: 75;
- liquid + non-toxic rows: 29;
- gates passed: 6 / 6;
- replay ready: 0;
- strategy replay allowed: 0;
- paper/live acceptance allowed: 0;
- next best action: `do_not_replay_filter_only_contexts_design_new_external_or_orderflow_feature_source`.

Current Phase170 interpretation: the Phase130 diagnostic filter source is useful as a context-quality filter, but its strict replay-safe subset is too narrow to justify another synthetic-only replay. The plan should not promote filter-only contexts into signals. The next synthetic research step must either introduce a genuinely new external/order-flow feature source under precommit, or remain on real-anchor acquisition.

### Phase171 — External/Order-flow Feature Source Contract

**Runner:** `scripts/run_phase171_external_orderflow_source_contract.py`

**Implementation:** `src/synthetic_l2/phase171_external_orderflow_source_contract.py`

**Outputs:** `outputs/phase171/`

Phase171 implements the Phase170 continuation decision by creating a no-replay source contract for the next genuinely new research axis. It does not emit buy/sell signals, order-arrival streams, fill models, P&L replay, profitability claims, or broker/paper-live acceptance.

The declared candidate source axes are:

1. `P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW` — multiday real Zerodha L2 receive-event cadence, quote churn, depth refresh intensity, stale-quote duration and cross-symbol arrival synchrony;
2. `P171_BROKER_ORDER_TELEMETRY` — own decision/order/ack/fill/reject/cancel timing, if actual broker logs become available;
3. `P171_EXTERNAL_REGIME_CONTEXT` — timestamped external regime/context series with provenance and no future leakage.

The selected next source is `P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW`. This keeps the next milestone aligned with the user's Azure guidance: heavy L2 data should be downloaded or imported into local Parquet first, then scanned locally with DuckDB or equivalent local tooling. Python strategy/cache/replay code must not stream-scan Azure directly for heavy experiments.

Current Phase171 outputs include:

- `phase171_external_orderflow_source_contract.csv`;
- `phase171_selected_source_work_order.csv`;
- `phase171_blocked_family_overlap_audit.csv`;
- `phase171_source_contract_gate_evaluation.csv`;
- `phase171_external_orderflow_source_acceptance_summary.csv`;
- `phase171_external_orderflow_source_contract_report.md`;
- `phase171_external_orderflow_source_contract_manifest.json`.

Current Phase171 evidence records:

- source contract rows: 3;
- selected source id: `P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW`;
- work-order rows: 3;
- blocked-family overlap audit rows: 3;
- gates passed: 6 / 6;
- strategy replay allowed: 0;
- paper/live acceptance allowed: 0;
- Azure read policy: `forbidden_for_analysis_download_first_then_local`;
- cost model version retained for audit continuity: `zerodha_equity_intraday_nse_order_formula_v2_2026_07_14`;
- next best action: `run_download_first_real_l2_receive_flow_availability_audit_or_collect_broker_order_telemetry`.

Current Phase171 interpretation: the plan now has a concrete bridge out of the falsified synthetic-only replay loop. The next action is not another strategy shard. It is a download-first/local-first real L2 receive-flow availability audit, or a broker-order telemetry collection path if actual broker logs become available.

### Phase172 — Real L2 Receive-flow Availability Audit

**Runner:** `scripts/run_phase172_real_l2_receive_flow_availability_audit.py`

**Implementation:** `src/synthetic_l2/phase172_real_l2_receive_flow_availability_audit.py`

**Outputs:** `outputs/phase172/`

Phase172 executes the Phase171 next-best action against the currently downloaded local real L2 panel. It is a local-only audit over `real_data_sample/l2_multiday_panel`; it does not contact Azure, stream-scan remote storage, emit buy/sell signals, create order-arrival streams, run fills, compute strategy P&L or open paper/live acceptance.

The audit uses the selected Phase171 source `P171_REAL_MULTIDAY_RECEIVE_EVENT_FLOW` and measures:

- local date/symbol/file/byte/row availability;
- required Zerodha WebSocket top-five market-by-price receive-flow columns;
- per-symbol receive cadence during the NSE session;
- receive gap quantiles and sub-second update counts;
- L1/top-of-book state-change availability;
- top-five depth quantity-change availability;
- 1-second cross-symbol bucket synchrony as a source-feature availability proxy.

Current Phase172 outputs include:

- `phase172_date_receive_flow_audit.csv`;
- `phase172_symbol_day_receive_flow_audit.csv`;
- `phase172_symbol_1s_bucket_presence.csv`;
- `phase172_receive_flow_gate_evaluation.csv`;
- `phase172_real_l2_receive_flow_availability_acceptance_summary.csv`;
- `phase172_real_l2_receive_flow_availability_audit_report.md`;
- `phase172_real_l2_receive_flow_availability_audit_manifest.json`.

Current Phase172 evidence records:

- local trade dates discovered: 3 (`2026-07-08`, `2026-07-09`, `2026-07-13`);
- ready receive-flow dates: 3;
- minimum ready dates required by the Phase171 source contract: 5;
- additional ready dates needed: 2;
- symbol/day partitions audited: 96;
- total local Parquet files audited: 99,272;
- total local rows scanned: 1,238,275;
- total compressed local bytes audited: 3,490,276,400;
- median symbol session receive tick rate: approximately 0.835 ticks/sec;
- median symbol receive gap: approximately 0.75 sec;
- median L1/top-of-book state-change fraction: approximately 0.541;
- median top-five depth quantity-change fraction: approximately 0.570;
- hard gates passed: 5 / 5;
- unlock gates passed: 0 / 1;
- strategy replay allowed: 0;
- paper/live acceptance allowed: 0;
- Azure read policy: `forbidden_for_analysis_download_first_then_local`;
- next best action: `download_at_least_2_additional_real_l2_dates_then_rerun_phase172`.

Current Phase172 interpretation: the local real L2 receive-flow source is structurally usable and more than minute-level; all currently available local dates have all 32 symbols and required receive/depth fields. However, only 3 ready dates are available versus the 5-date minimum required by the Phase171 source contract, so no strategy replay or paper/live path opens. The next correct action is to download or import at least two additional complete real L2 dates locally, then rerun Phase172 and the downstream real-anchor gates.

### Phase173 — Real L2 Download Credential Preflight

**Runner:** `scripts/run_phase173_real_l2_download_credential_preflight.py`

**Implementation:** `src/synthetic_l2/phase173_real_l2_download_credential_preflight.py`

**Outputs:** `outputs/phase173/`

Phase173 records whether the next two-date real L2 download can be executed immediately. It is a credential/readiness preflight only. It never records SAS signatures, storage account keys, broker credentials or passwords, and it does not contact Azure, run AzCopy, import data, unlock replay or run strategy P&L.

Current Phase173 outputs include:

- `phase173_download_preflight_evidence.csv`;
- `phase173_download_preflight_gate_evaluation.csv`;
- `phase173_real_l2_download_credential_preflight_acceptance_summary.csv`;
- `phase173_real_l2_download_credential_preflight_report.md`;
- `phase173_real_l2_download_credential_preflight_manifest.json`.

Current Phase173 evidence records:

- required next download dates: `2026-07-10`, `2026-07-14`;
- AzCopy available: 1;
- SAS token available in environment: 0;
- storage account key available in environment: 0;
- Azure CLI account login probe: account context is available;
- Azure CLI storage metadata/token-refresh probe: blocked by local TLS certificate verification failure;
- Phase172 ready receive-flow dates: 3;
- additional complete real L2 dates still needed: 2;
- latest Phase148 download ran: 0;
- latest Phase147 required dates satisfied: 0;
- latest Phase146 strategy replay allowed: 0;
- Phase173 download ready now: 0;
- strategy replay allowed: 0;
- paper/live acceptance allowed: 0;
- next best action: `provide_share_sas_or_storage_key_or_repair_azure_cli_tls_then_run_phase148_download`.

Current Phase173 interpretation: the next blocked item is not strategy logic. The plan needs a credential/trust fix for the download leg: provide a read/list share SAS, provide the storage account key through `AZURE_STORAGE_KEY` or `-AccountKey`, or repair Azure CLI certificate trust so a fresh SAS/key path can be generated. Once that is available, rerun Phase148 with download enabled for `2026-07-10` and `2026-07-14`, then rerun Phase172.

### Phase174 — Secure Real L2 Download Orchestrator

**Runner:** `scripts/run_phase174_secure_real_l2_download_orchestrator.ps1`

**Outputs:** `outputs/phase174/`

Phase174 makes the Phase173 next action executable without exposing secrets. It checks `.env` and the current process environment for `AZURE_STORAGE_SAS_TOKEN` or `AZURE_STORAGE_KEY`, records only the credential variable names that were loaded, and never prints or persists the secret values.

If a SAS token or storage account key is present, Phase174 runs Phase148 with download enabled for the configured dates and then reruns Phase172. If neither credential is available, it refreshes Phase173 and writes a skipped-download ledger instead of attempting Azure access.

Current Phase174 outputs include:

- `phase174_secure_download_step_ledger.csv`;
- `phase174_secure_real_l2_download_orchestrator_acceptance_summary.csv`;
- `phase174_secure_real_l2_download_orchestrator_report.md`;
- `phase174_secure_real_l2_download_orchestrator_manifest.json`.

Current Phase174 evidence records:

- required dates: `2026-07-10`, `2026-07-14`;
- `.env` checked: 1;
- Azure credential variable names loaded from `.env`: none;
- SAS available in process environment: 0;
- storage account key available in process environment: 0;
- Phase173 refreshed after `.env` load: 1;
- Phase148 download ran: 0;
- Phase172 reran: 0;
- failed workflow steps: 0;
- Phase173 download ready now: 0;
- Phase172 additional dates still needed: 2;
- strategy replay allowed: 0;
- paper/live acceptance allowed: 0;
- next best action: `add_AZURE_STORAGE_SAS_TOKEN_or_AZURE_STORAGE_KEY_to_env_or_process_then_rerun_phase174`.

Current Phase174 interpretation: the download path is now executable and secret-safe. The user can add a read/list share SAS or storage account key to `.env` or the process environment, then rerun Phase174. Until that happens, the plan remains correctly gated with no replay, no paper/live acceptance and no Azure data movement attempted.

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

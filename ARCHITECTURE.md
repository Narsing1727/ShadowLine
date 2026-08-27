# ShadowLine — Architecture

This document describes the design in full: the layered structure and the
direction dependencies are allowed to flow, why the codebase is split into two
services, what every module is responsible for, the event schema the two
services agree on, the API contract the frontend binds to, the shadow-to-live
lifecycle, and the path from this prototype to a production deployment.

Nothing here is implemented yet — this file is the contract the implementation
sessions build against.

---

## 1. Two services, one boundary

```
┌─────────────────────┐        canonical event stream        ┌──────────────────────────────┐
│      sim_plant        │  ────────────────────────────────▶  │          shadowline             │
│  (Service A — stand-in │        (the only thing shared)       │        (Service B — the product) │
│   for the physical      │                                       │                                    │
│   factory)              │                                       │                                    │
└─────────────────────┘                                       └──────────────────────────────┘
```

`sim_plant` is a SimPy discrete-event simulation of a 42-station mixed-model
assembly line. It plays the role of the physical factory: it moves units
through stations, randomises cycle times per variant, injects faults from
`configs/faults.yaml`, and emits an event stream — while deliberately
withholding data for stations marked `DARK`, so the rest of the system
genuinely has to cope with missing signal rather than being handed a
convenient, fully-observed world.

`shadowline` is the actual product. It consumes that event stream, maintains
its own twin of the line, forks the twin every 60 seconds to forecast the
next four hours, runs three prediction heads, calibrates their output,
decides what's worth alerting on, scores its own track record, and serves an
API and WebSocket feed.

**`shadowline` must never import from `sim_plant`.** These are separate
top-level packages under `src/`, and the only thing that crosses the
boundary between them is the canonical event schema defined in §4. This is
the single most important structural rule in the codebase, and it exists for
a concrete reason: if `shadowline` cannot tell — architecturally, not just in
practice — whether it is being fed simulated or real data, then replacing
`sim_plant` with a real OPC-UA or MQTT feed is a configuration change (point
the ingestion adapter elsewhere) rather than a rewrite. That substitutability
is the prototype's actual proof that the design generalises to a line it has
never seen, which is Constraint 5 (see README).

**SimPy appears in both services, in two different roles, deliberately.** In
`sim_plant`, SimPy *is* the physical world — the ground truth the rest of the
system only ever observes secondhand, through emitted events. In
`shadowline/twin`, SimPy is the *model of that world* — the twin, forked
every cycle and run forward to forecast. The same library plays the simulated
subject and the simulating instrument. That symmetry isn't incidental: the
twin forking itself to simulate forward is the core mechanism of the product,
and using the same discrete-event tool for both roles keeps that mechanism
honest — the twin's forward runs are held to the same modelling assumptions
as the world it's trying to predict.

## 2. Layers inside `shadowline`, and dependency direction

Dependencies point one way — down this list. A layer may depend on anything
above it; nothing above may depend on anything below it. `domain` depends on
nothing else in the codebase; `api` and `orchestration` depend on everything.

```
 1. domain           — entities and enums every other layer speaks in
 2. ingestion         — turns adapter-specific payloads into canonical events
 3. twin               — maintains and forks live state from the event stream
 4. prediction          — three heads consume twin state, produce Predictions
 5. calibration           — maps raw prediction probabilities to honest confidence
 6. decision                — ranks, budgets, and suppresses; Predictions become Alerts
 7. trust                     — logs, scores, and gates predictions and alerts over time
 8. discovery                   — infers topology/coverage for a line, independent of the above
 9. impact                        — translates twin/decision output into monetary terms
10. persistence                    — SQLAlchemy models and repositories, used by layers 3–9
11. orchestration                    — wires 2–10 together on the 60s cycle
12. api                                — exposes 3–10 over REST/WebSocket
```

`config` and `telemetry` are cross-cutting and may be used from any layer.
`discovery` depends only on `domain` and `persistence` (it consumes historical
exit-timestamp data, not live twin state) — it is how a *new* line gets onto
the platform, before a live twin exists for it at all.

## 3. Module responsibilities

### `src/sim_plant/`

| Module | Responsibility |
|---|---|
| `main.py` | Service entry point — wires config, model, faults, and emit, then starts the SimPy environment. |
| `config.py` | Loads `sim_plant`'s own settings plus the line and fault YAML configs. |
| `clock.py` | Maps SimPy virtual time to wall-clock timestamps; applies the configurable speed factor. |
| `model/line.py` | Top-level SimPy model of the full line — owns every station and buffer process and the unit generator. |
| `model/station.py` | SimPy process for one station: takes a unit, holds it for a randomised cycle time, transitions its `StationState`. |
| `model/buffer.py` | SimPy store wrapper representing the buffer between two stations, with capacity and current count. |
| `model/unit.py` | The `Unit` entity moving down the line — VIN, variant, and an accumulating genealogy record. |
| `model/variant_profile.py` | Per-variant cycle-time distributions and defect propensities for `SUV_A`, `SEDAN_B`, `EV_C`. |
| `faults/injector.py` | Schedules and applies fault scenarios from `configs/faults.yaml` onto stations during the run. |
| `faults/gradual_drift.py` | Fault type — a station's cycle time or quality drifts slowly over time. |
| `faults/sudden_failure.py` | Fault type — a station goes `DOWN` abruptly for a random or fixed duration. |
| `faults/intermittent.py` | Fault type — a station flickers between `ACTIVE` and faulted at short, irregular intervals. |
| `emit/event_stream.py` | Converts internal model events into the canonical wire event (§4) and pushes them out. |
| `emit/sensor_gaps.py` | Withholds or degrades emitted data for stations configured `DARK` or `INFERRED`, simulating real sensor coverage. |
| `emit/transport.py` | The outbound transport the event stream is pushed over, read by `shadowline`'s simulated ingestion adapter. |

### `src/shadowline/domain/`

| Module | Responsibility |
|---|---|
| `enums.py` | The shared vocabulary: `StationState`, `ConfidenceTier`, `Zone`, `Mode`, `Variant`. |
| `station.py` | `Station` entity — id, zone, current state, cycle time, confidence tier. |
| `buffer.py` | `Buffer` entity — capacity, current count, upstream/downstream station references. |
| `zone.py` | `Zone` entity grouping stations into `BODY_SHOP` / `PAINT_SHOP` / `FINAL_ASSEMBLY`. |
| `unit.py` | `Unit` entity — VIN, variant, current station, timestamps. |
| `genealogy.py` | The full record of stations, tools, and operators that touched a given `Unit`. |
| `topology.py` | A line's station order, buffer graph, parallel paths, and takt time. |
| `events.py` | The canonical internal event type every ingestion adapter normalizes into (§4). |
| `prediction.py` | `Prediction` entity — subject, probability, horizon, evidence. |
| `alert.py` | `Alert` entity — a `Prediction` that survived ranking and the alarm budget, plus ack/snooze/false-alarm lifecycle state. |
| `evidence.py` | The human-readable facts attached to a `Prediction`/`Alert` explaining why it fired. |

### `src/shadowline/ingestion/`

| Module | Responsibility |
|---|---|
| `port.py` | The abstract ingestion interface every adapter implements — read paths only; no adapter exposes a write method. |
| `normalizer.py` | Converts adapter-specific payloads into the canonical internal event type. |
| `buffering.py` | Short-term buffering and backpressure handling before events reach the twin. |
| `adapters/simulated.py` | Reads the event stream emitted by `sim_plant`. |
| `adapters/csv_replay.py` | Replays a CSV/historian export as an event stream, for offline testing and history seeding. |
| `adapters/opcua_stub.py` | Documents the real OPC-UA integration path (read-only subscriptions) without implementing it. |
| `adapters/mqtt_sparkplug_stub.py` | Documents the real MQTT Sparkplug B integration path (read-only subscriptions) without implementing it. |

### `src/shadowline/twin/`

| Module | Responsibility |
|---|---|
| `state_store.py` | Holds live in-memory state for every station, buffer, and in-flight unit. |
| `line_model.py` | The SimPy model of the twin itself — the "model of the world" counterpart to `sim_plant`'s "the world" (see §1). |
| `fork.py` | Produces an independent copy of current twin state that can be advanced without disturbing the live model. |
| `advance.py` | Advances a forked twin forward in simulated time — the primitive Monte Carlo forecasting is built on. |
| `genealogy_tracker.py` | Maintains genealogy records as units move through the live twin. |
| `snapshot.py` | A serializable snapshot of twin state, used for persistence and as the basis for a fork. |

### `src/shadowline/prediction/`

| Module | Responsibility |
|---|---|
| `base.py` | The shared interface every prediction head implements. |
| `registry.py` | Registers and looks up available prediction heads for the orchestration cycle. |
| `bottleneck/active_period.py` | Implements the Active Period Method — longest uninterrupted `ACTIVE` stretch per station from state/timestamp history alone. |
| `bottleneck/shifting_detector.py` | Detects when the bottleneck station changes over time (a wandering bottleneck). |
| `bottleneck/monte_carlo.py` | Forks the twin and runs N forward simulations (default 200) of the next horizon to sample bottleneck outcomes. |
| `bottleneck/horizon_forecast.py` | Aggregates Monte Carlo run outcomes into a per-station probability-of-bottleneck-by-time forecast. |
| `bottleneck/aggregator.py` | Combines the Active Period signal and the Monte Carlo forecast into the bottleneck head's final output. |
| `defect/lag_estimator.py` | Learns the typical time lag between a causing station's drift and a detecting station's failure. |
| `defect/propagation_graph.py` | The directed graph of station-to-station defect relationships, with lag and observed case-count edge weights. |
| `defect/drift_detector.py` | Detects process drift at a station that historically precedes downstream defects. |
| `defect/backward_trace.py` | Given a confirmed defect, walks the propagation graph backward to candidate causing stations. |
| `defect/containment.py` | Given a defect origin, walks forward to determine which units downstream were potentially affected. |
| `soft_sensor/features.py` | Builds the feature vectors (neighbouring buffer levels, takt deviation) soft-sensor estimation uses. |
| `soft_sensor/estimator.py` | Regression model(s) estimating state for `INFERRED` stations without direct sensor data — the virtual-sensor equivalent of virtual metrology. |
| `soft_sensor/coverage_classifier.py` | Assigns each station's confidence tier from observed signal availability. |
| `soft_sensor/training.py` | Trains and refits soft-sensor estimators against historical data. |

### `src/shadowline/calibration/`

| Module | Responsibility |
|---|---|
| `port.py` | The abstract calibration interface — designed so a conformal implementation can replace isotonic without changing any caller. |
| `isotonic.py` | Isotonic regression calibration mapping raw model probabilities to honest confidence values. |
| `conformal.py` | Conformal prediction calibrator behind the same port — the intended future upgrade path. |
| `reliability.py` | Computes reliability/calibration curves from historical predictions versus outcomes. |

### `src/shadowline/decision/`

| Module | Responsibility |
|---|---|
| `ranker.py` | Ranks predictions by severity, confidence, and time-to-impact. |
| `alarm_budget.py` | Enforces the hard cap on alerts surfaced per operator per hour (Constraint 3). |
| `suppression.py` | Suppresses chattering and duplicate alerts for the same underlying condition. |
| `recommendation.py` | Generates human-readable recommendations, always phrased as suggestions, never commands. |
| `explanation.py` | Builds the evidence/explanation payload attached to a prediction or alert. |

### `src/shadowline/trust/`

| Module | Responsibility |
|---|---|
| `shadow_log.py` | Persists every prediction made, in either mode, with a timestamp, for later scoring. |
| `outcome_matcher.py` | Matches a logged prediction to what actually happened once its horizon passes. |
| `scorecard.py` | Computes precision, recall, false alarm rate, mean lead time, and calibration curves over scored predictions. |
| `promotion_gate.py` | Evaluates whether the scorecard clears the thresholds required to promote a line from `SHADOW` to `LIVE`. |
| `operator_feedback.py` | Records operator feedback (e.g. a false-alarm mark) against an alert, feeding it back into the scorecard. |

### `src/shadowline/discovery/`

| Module | Responsibility |
|---|---|
| `topology_inference.py` | Infers station order and line topology from unit-exit timestamps alone. |
| `buffer_inference.py` | Infers buffer existence and capacity between inferred stations from exit-timestamp patterns. |
| `takt_estimator.py` | Estimates takt time from observed exit-timestamp cadence. |
| `parallel_path_detector.py` | Detects parallel paths (e.g. parallel respot-welding stations) in the inferred topology. |
| `onboarding_session.py` | Orchestrates a discovery run end-to-end as a stateful session with stage progress, for onboarding a new line. |

### `src/shadowline/impact/`

| Module | Responsibility |
|---|---|
| `assumptions.py` | Editable cost assumptions — labor rate, downtime cost, rework cost — used by every calculation below. |
| `downtime_value.py` | Translates predicted or avoided downtime into a monetary figure. |
| `rework_value.py` | Translates predicted or avoided defects into a rework cost figure. |
| `containment_value.py` | Translates defect containment (units caught before shipping) into a value figure. |
| `oee.py` | Computes OEE — availability, performance, quality — from twin and state history. |

### `src/shadowline/persistence/`

| Module | Responsibility |
|---|---|
| `engine.py` | SQLAlchemy engine and session setup against the SQLite database. |
| `models.py` | SQLAlchemy ORM models for events, stations, predictions, alerts, genealogy, and scorecards. |
| `migrations/` | Reserved for schema migration scripts; the prototype uses `create_all` and has none yet. |
| `repositories/events.py` | Persistence access for raw and normalized events. |
| `repositories/stations.py` | Persistence access for station state history. |
| `repositories/predictions.py` | Persistence access for logged predictions. |
| `repositories/alerts.py` | Persistence access for alerts and their lifecycle state. |
| `repositories/genealogy.py` | Persistence access for unit genealogy records. |
| `repositories/scorecard.py` | Persistence access for computed scorecards and promotion-gate history. |

### `src/shadowline/api/`

| Module | Responsibility |
|---|---|
| `app.py` | Constructs the FastAPI application and mounts the routers and WebSocket endpoint. |
| `deps.py` | Shared FastAPI dependencies — DB session, current settings, twin/state access. |
| `errors.py` | Shared exception types and error-response handlers. |
| `schemas/*.py` | Pydantic request/response schemas, one module per resource, at the API boundary (kept separate from `domain` entities). |
| `routers/*.py` | One module per resource area, implementing the routes in §6. |
| `ws/connection_manager.py` | Tracks connected WebSocket clients for the live feed. |
| `ws/live_feed.py` | Pushes station state and alert updates to connected clients. |

### `src/shadowline/orchestration/`

| Module | Responsibility |
|---|---|
| `scheduler.py` | Drives the periodic 60-second fork-and-forecast cycle. |
| `prediction_cycle.py` | Runs one full cycle: fork twin → run prediction heads → calibrate → decide → persist. |
| `lifecycle.py` | Service startup/shutdown wiring — starts ingestion, twin, and scheduler; handles graceful shutdown. |

### `src/shadowline/config/` and `src/shadowline/telemetry/`

| Module | Responsibility |
|---|---|
| `config/settings.py` | Pydantic settings loaded from the environment for the `shadowline` service. |
| `config/line_loader.py` | Loads and validates a line's YAML configuration into domain `Topology`/`Station`/`Buffer` entities. |
| `config/mode.py` | Holds and exposes the current `SHADOW`/`LIVE` mode. |
| `telemetry/logging.py` | Structured logging setup. |
| `telemetry/metrics.py` | Lightweight counters — prediction cycle duration, alert counts — for observability. |

### `configs/`, `scripts/`, `tests/`

| Path | Responsibility |
|---|---|
| `configs/lines/*.yaml` | Full line definitions — stations, zones, buffers, takt, confidence tiers. Nothing about a line is hardcoded (Constraint 5). |
| `configs/variants.yaml` | Variant definitions (`SUV_A`, `SEDAN_B`, `EV_C`) and their profiles. |
| `configs/faults.yaml` | Fault scenarios `sim_plant` can inject. |
| `configs/thresholds.yaml` | Alarm budget, promotion-gate, and other operational thresholds. |
| `scripts/run_sim_plant.py` | Entry point starting the `sim_plant` service. |
| `scripts/run_api.py` | Entry point starting the `shadowline` API/orchestration service. |
| `scripts/seed_history.py` | Seeds the database with historical events/predictions, e.g. from a CSV replay, for cold-start scoring and discovery. |
| `scripts/replay_shift.py` | Replays a recorded shift's worth of events through ingestion, for demos and testing. |
| `scripts/score_predictions.py` | Runs the trust layer's scoring pass against logged predictions on demand. |
| `tests/unit/` | One module per algorithmic unit: Active Period Method, Monte Carlo, alarm budget, soft sensor, lag estimator, topology inference, calibration. |
| `tests/integration/` | Ingestion-to-twin, full prediction cycle, and API contract tests. |
| `tests/fixtures/` | Shared static fixtures — sample configs and canned event sequences. |

## 4. The canonical event schema

Every ingestion adapter (`simulated`, `csv_replay`, and eventually `opcua`,
`mqtt_sparkplug`) normalizes whatever it reads into this one shape before
anything downstream — twin, prediction, decision — ever sees it. This is the
entire contract between `sim_plant` and `shadowline`, and the entire contract
a future real-plant integration has to satisfy.

| Field | Meaning |
|---|---|
| `event_id` | Unique id for this event. |
| `event_type` | One of `STATION_STATE_CHANGED`, `UNIT_EXITED_STATION`, `DEFECT_DETECTED`, `HEARTBEAT`. |
| `occurred_at` | UTC timestamp of when the event happened on the line — not when it was received. |
| `ingested_at` | UTC timestamp set by the normalizer when the event entered `shadowline`. |
| `station_id` | The station this event concerns, e.g. `"S-14"` (absent for line-level events). |
| `zone` | The station's zone — `BODY_SHOP`, `PAINT_SHOP`, or `FINAL_ASSEMBLY`. |
| `confidence_tier` | `MEASURED`, `INFERRED`, or `DARK` — the coverage tier of the *source* this event came from. Set at the point of ingestion and never upgraded downstream. |
| `source` | Which adapter produced this event — `simulated`, `csv_replay`, `opcua`, `mqtt_sparkplug`. |
| `payload` | Event-type-specific data (below). |

Payload shape by `event_type`:

- **`STATION_STATE_CHANGED`** — `state` (`StationState`), `previous_state`,
  `cycle_time_seconds` (if the transition closed a cycle).
- **`UNIT_EXITED_STATION`** — `vin`, `variant`, `dwell_seconds`. This is the
  event type discovery (§ `discovery/`) treats as its sole required input —
  by design, it is the most elementary signal a line produces regardless of
  instrumentation.
- **`DEFECT_DETECTED`** — `vin`, `defect_code`, `detecting_station_id`.
- **`HEARTBEAT`** — no payload; liveness signal from an adapter/source.

An event with `confidence_tier: DARK` still carries `station_id` and
timestamps — a `DARK` station is known to exist and to have produced a unit
at a point in time; what's missing is everything about *how*. This is what
lets soft-sensor estimation and discovery reason about a `DARK` station's
neighbours without ever fabricating a value for the station itself.

## 5. Ingestion is read-only by construction

`ingestion/port.py` defines the interface every adapter implements. It has
methods to connect, to stream/poll events, and to report adapter health —
and nothing else. There is no `write`, `command`, `set_point`, or equivalent
anywhere in that interface, in any adapter, or anywhere else in the
codebase. This is Constraint 1, and it is enforced by what the interface
makes it physically possible to call, not by a comment or a code-review
convention. The OPC-UA and MQTT Sparkplug B stubs document real-world
integration exclusively in terms of read-side subscriptions for the same
reason — see §8.

## 6. API contract

REST plus one WebSocket, serving three role-shaped views (floor supervisor,
plant manager, leadership) over one underlying twin. Implemented under
`api/routers/`, with request/response shapes defined in `api/schemas/`. Every
response that touches station-level data includes each station's
`confidence_tier` — there is no route that can present an inferred value
without labelling it as such.

| Route | Description |
|---|---|
| `GET /health` | Liveness/readiness check. |
| `GET /api/line` | Line metadata — name, takt time, target JPH, shift, current `Mode`. |
| `GET /api/line/state` | Current state of all 42 stations. |
| `GET /api/line/state?horizon=1h\|2h\|4h` | Simulated future state at the given horizon, from the latest twin fork. |
| `GET /api/line/simulation` | Monte Carlo run metadata — runs completed, horizon, timestamp of the last fork. |
| `GET /api/stations` | All stations, each with confidence tier, state, cycle time, and buffer status. |
| `GET /api/stations/{id}` | Full detail for one station. |
| `GET /api/stations/{id}/history` | State and cycle-time history for one station. |
| `GET /api/alerts` | Currently active alerts, ranked, within the alarm budget. |
| `GET /api/alerts/suppressed` | Signals that were detected but held back by ranking/budget/suppression. |
| `GET /api/alerts/{id}` | Alert detail — evidence and recommendations. |
| `POST /api/alerts/{id}/acknowledge` | Operator acknowledges an alert. |
| `POST /api/alerts/{id}/snooze` | Operator snoozes an alert for a period. |
| `POST /api/alerts/{id}/false-alarm` | Operator marks an alert a false alarm — feeds `trust/operator_feedback.py`. |
| `GET /api/predictions/bottleneck` | Current bottleneck forecast with per-station probabilities. |
| `GET /api/predictions/bottleneck/history` | Predicted-versus-actual bottleneck history. |
| `GET /api/defects/propagation` | Defect propagation graph — edges with lag and case counts. |
| `GET /api/defects/containment` | Units affected, given a defect origin. |
| `GET /api/genealogy/{vin}` | Full genealogy trail for one unit. |
| `GET /api/coverage` | Confidence tier per station across the line. |
| `GET /api/trust/scorecard` | Precision, recall, false alarm rate, mean lead time, calibration. |
| `GET /api/trust/promotion-gate` | Promotion-gate thresholds and current standing. |
| `GET /api/impact` | Downtime, rework, OEE, and payback figures. |
| `PUT /api/impact/assumptions` | Update the editable cost assumptions impact figures are computed from. |
| `POST /api/discovery/session` | Start onboarding a new line via discovery. |
| `GET /api/discovery/session/{id}` | Discovery session stage progress and inferred topology so far. |
| `GET /api/settings` | Current settings — mode, alarm budget, thresholds, sim params. |
| `PUT /api/settings` | Update mode, alarm budget, thresholds, sim params. |
| `WS /ws/live` | Push feed of station state changes and new alerts. |

## 7. The shadow-to-live lifecycle

This is a first-class feature, not internal hygiene — Constraint 4 exists
because a plant team has no reason to trust a fresh model's alerts, and a
false alarm early on can poison trust in the whole system permanently.

1. **A line starts in `SHADOW` mode.** `orchestration/prediction_cycle.py`
   runs the full pipeline — fork, predict, calibrate, rank — every cycle, and
   `trust/shadow_log.py` persists every prediction produced. Nothing reaches
   `/api/alerts`; there is nothing for an operator to see.
2. **Predictions get scored as their horizon passes.**
   `trust/outcome_matcher.py` compares each logged prediction to what the
   twin (fed by real ingested events, not the forecast) actually recorded
   happening.
3. **The scorecard accumulates.** `trust/scorecard.py` computes precision,
   recall, false alarm rate, mean lead time, and calibration curves over a
   rolling window.
4. **The promotion gate is evaluated continuously.**
   `trust/promotion_gate.py` checks the scorecard against thresholds defined
   in `configs/thresholds.yaml` — a minimum precision, a maximum false alarm
   rate consistent with the EEMUA 191 budget, and a minimum sample size so
   the gate can't be cleared on a lucky handful of predictions.
5. **`GET /api/trust/promotion-gate` exposes standing at all times** — this
   is visible to the plant team throughout, not revealed only at the moment
   of promotion.
6. **Promotion to `LIVE` is a mode change** (`PUT /api/settings`), not a
   code change. Once `LIVE`, `decision/` output starts reaching
   `/api/alerts` and the WebSocket feed. `SHADOW` logging and scoring
   continue exactly as before — `LIVE` adds alerting, it doesn't replace
   scoring.
7. **A line can be demoted back to `SHADOW`** if its live scorecard
   regresses below the gate — the gate is a standing condition, not a
   one-time checkpoint.

## 8. Production scale path

This prototype's choices are deliberately right-sized for a single simulated
line and a few events per second (see README, "What we deliberately did not
build"). None of them are the right answer at the scale of a real plant
network, and the path from here to there is:

- **OPC-UA.** Real modern equipment exposes state over OPC-UA. The
  production ingestion adapter subscribes read-only to the relevant node IDs
  — station state, cycle completion, fault codes — mirroring exactly the
  interface `ingestion/adapters/opcua_stub.py` documents today. No control
  nodes are ever subscribed to, let alone written.
- **MQTT Sparkplug B.** For newer/edge-instrumented equipment and IIoT
  gateways, Sparkplug B's defined payload structure (NBIRTH/NDATA/NDEATH)
  gives the same read-only subscription model over MQTT, again as documented
  in `ingestion/adapters/mqtt_sparkplug_stub.py`.
- **Kafka fan-out.** At one line, one producer and one consumer at ~20
  events/second, a broker adds pure operational overhead. At plant scale —
  many lines, many consumers (the twin, long-term storage, other analytics)
  — Kafka's fan-out and replay properties become genuinely necessary, and
  the canonical event schema in §4 is already shaped to be a Kafka message
  value with no changes required.
- **TimescaleDB (or equivalent time-series store) in place of SQLite.**
  SQLite is correct for one line, one writer, and a prototype's data volume.
  A multi-line deployment needs a database built for high-cardinality
  time-series retention, continuous aggregation, and concurrent writers —
  Timescale's hypertables are the natural upgrade from
  `persistence/models.py`, and the repository layer (`persistence/repositories/`)
  exists specifically so that swap doesn't touch any caller above it.
- **IEC 62443 network zoning.** A real plant's OT network is zoned and
  conduited per IEC 62443 to keep control-system traffic isolated from IT
  and analytics traffic. A production ShadowLine ingestion service is
  deployed as a read-only conduit *out* of the OT zone into an
  IT/analytics zone — it never sits inside the control zone, and it never
  originates traffic back into it. Constraint 1's architectural read-only
  guarantee (§5) is what makes that placement possible in the first place:
  a service that cannot write is a service a plant's security team can
  approve to sit at that boundary.

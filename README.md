# ShadowLine

A predictive digital twin for a vehicle assembly line — built for the **Accenture
Innovation Challenge 2026**, Round 2, problem statement **DigitalTwin.ai**.

ShadowLine runs ahead of the physical line. Every 60 seconds it takes the live
state of the line, forks it, and runs Monte Carlo simulations of the next four
hours. It answers two questions a plant team actually needs answered before
their shift ends, not after:

1. **Which station is about to become a bottleneck, and when?**
2. **Which upstream station is causing the defects being detected downstream?**

> **Status:** this repository currently contains the project skeleton only —
> directory structure, empty modules, and documentation. Implementation lands
> incrementally, module by module, in subsequent work sessions. See
> [ARCHITECTURE.md](ARCHITECTURE.md) for the full design.

---

## The problem

A modern assembly line generates a constant stream of station states, cycle
times, and buffer levels, but plant teams are almost always reacting to
problems after they've already cost output: a bottleneck is diagnosed once the
buffer in front of it is already full, and a defect's root cause is traced
once dozens of units downstream are already affected.

The Round 2 brief asks for a digital twin prototype that helps plant teams see
bottlenecks forming and predict likely defects before they happen — on
illustrative or simulated data, as a proof of concept, not a production
system.

## The deliberate scope decision

**ShadowLine does not build a photorealistic 3D factory.** The twin is a
lightweight discrete-event model of exactly what determines output: station
cycle times, station states, buffer levels, and part genealogy. Weld physics,
robot kinematics, and CAD geometry are out of scope by choice, not by
limitation — none of them change which station is about to starve or block,
and none of them explain why a defect surfaced three stations downstream of
where it originated. Spending effort there would have produced something that
looks more impressive in a screenshot and answers fewer of the two questions
that matter.

Every other structural decision in this codebase follows from five hard
constraints taken directly from how real plants operate:

| # | Constraint | Structural consequence |
|---|---|---|
| 1 | **Read-only, always.** Software is never allowed to write to a PLC — the risk of stopping production or injuring someone is not one a prototype gets to take. | The ingestion layer exposes read paths only. No adapter interface anywhere in this codebase has a write method. This is architecturally enforced, not a convention. |
| 2 | **Sensor coverage is uneven.** Real lines mix instrumented equipment, legacy machines, and manual stations. | Every station carries a confidence tier — `MEASURED`, `INFERRED`, or `DARK` — that propagates through every layer and appears in every API response. The system degrades gracefully and never presents an inferred value as measured. |
| 3 | **False alarms destroy trust.** EEMUA 191 treats >12 alerts/operator/hour as unmanageable; a system that cries wolf gets ignored within weeks. | Detection and alerting are two distinct stages with a hard boundary. A dedicated decision layer enforces an alarm budget and ranks alerts before anything reaches an operator. |
| 4 | **Predictions must earn trust before they're used.** | Two modes: `SHADOW` (compute and log, never alert) and `LIVE` (alert). Every prediction is persisted and scored against outcome. An explicit promotion gate defines the accuracy and alarm-rate thresholds a model must clear to go live. |
| 5 | **It must generalise to lines we've never seen.** Every plant has a different layout, equipment vintage, and sensor maturity. | Nothing about a specific line is hardcoded — line definitions load from YAML. A discovery module infers topology, buffers, capacities, and takt time from nothing but unit-exit timestamps. |

## Architecture in one paragraph

ShadowLine is two separate services. **`sim_plant`** is a SimPy discrete-event
simulation that stands in for the physical factory — it moves units through
42 stations, randomises cycle times, injects faults, and emits an event
stream, deliberately withholding data for stations marked `DARK`. **`shadowline`**
is the actual product — it consumes that event stream, maintains its own twin
of the line, forks it every 60 seconds to forecast forward, predicts, decides
what's worth an operator's attention, and serves an API. The two share only
the event schema on the wire; `shadowline` never imports from `sim_plant`. If
the product genuinely cannot tell whether it's being fed simulated or real
data, swapping `sim_plant` for a real OPC-UA feed is a configuration change,
not a rewrite — that is the prototype's proof that the design generalises.
Full detail, including the dependency direction between every internal layer,
is in [ARCHITECTURE.md](ARCHITECTURE.md).

## Tech stack

| Concern | Choice |
|---|---|
| Language | Python 3.11+ |
| HTTP / WebSocket API | FastAPI |
| Discrete-event simulation | SimPy — used in both services, in two different roles (see ARCHITECTURE.md) |
| Numerical / Monte Carlo aggregation | NumPy |
| Time-series forecasting | statsmodels |
| Soft-sensor regression | scikit-learn |
| Defect propagation graph | NetworkX |
| Schemas & settings | Pydantic v2 |
| Persistence | SQLite via SQLAlchemy |
| Tests | pytest |
| Lint / types | Ruff, mypy |
| Local orchestration | Docker Compose |
| Dependency management | uv / pip (via `pyproject.toml`) |

## What we deliberately did not build, and why

- **Kafka.** One producer, one consumer, roughly 20 events per second. A
  message broker would add operational burden for zero additional capability
  at this scale. It's the correct answer at production scale — see the
  "Production scale path" section of ARCHITECTURE.md — but not here.
- **Kubernetes / cloud deployment.** Two containers on Docker Compose is the
  entire deployment footprint this prototype needs.
- **Unity, Omniverse, or any 3D engine.** Consistent with the core scope
  decision above — a visual twin doesn't answer either of the two questions
  ShadowLine exists to answer.
- **Any LLM.** Nothing in bottleneck forecasting, defect propagation, or
  soft-sensor estimation benefits from a language model; adding one would
  add latency, cost, and an unpredictable failure mode without adding
  capability.
- **Any deep learning framework.** The Active Period Method, Monte Carlo
  forecasting, isotonic/conformal calibration, and scikit-learn regressors
  are the right-sized tools for tabular, low-volume industrial time series.
  A neural network would need far more data than a 42-station line produces
  and would be harder to calibrate honestly.
- **Postgres / TimescaleDB.** The correct production answer for
  high-cardinality time-series retention, and documented as the scale path
  in ARCHITECTURE.md — but SQLite is the right choice for a single-line
  prototype with one writer.

## Running it

Two services, one command:

```bash
cp .env.example .env
make run          # docker compose up --build: sim_plant + shadowline
```

Or run each service locally without Docker:

```bash
make install       # pip install -e ".[dev]"
make run-sim        # starts sim_plant, begins emitting the event stream
make run-api         # starts the shadowline API, consuming that stream
```

The API serves on `http://localhost:8000` (see ARCHITECTURE.md for the full
route list); the live WebSocket feed is at `ws://localhost:8000/ws/live`.

```bash
make test    # pytest
make lint    # ruff check + mypy
make format  # ruff format + ruff check --fix
```

## Reference line

The bundled configuration (`configs/lines/plant2_line_a.yaml`) models a
42-station, two-shift, mixed-model line producing three variants
(`SUV_A`, `SEDAN_B`, `EV_C`) at a 58-second takt, targeting 62 JPH. Sensor
coverage is intentionally uneven — 27 `MEASURED`, 11 `INFERRED`, 4 `DARK` —
because a twin that assumes uniform instrumentation would fail on the first
real plant it met. Full station list and rationale are in ARCHITECTURE.md.

## Repository layout

```
configs/      line, variant, fault, and threshold definitions (YAML — no line is hardcoded)
docker/       Dockerfiles for both services
scripts/      entry points: run each service, seed history, replay a shift, score predictions
src/sim_plant/    the simulated factory (Service A)
src/shadowline/   the product (Service B)
tests/        unit, integration, and shared fixtures
```

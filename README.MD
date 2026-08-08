# Weather ETL Pipeline

A small, production-style ETL pipeline that extracts current weather data from
the [Open-Meteo](https://open-meteo.com/) API, transforms it, and loads it into
PostgreSQL — built as a portfolio project to practice the engineering practices
expected of a Data Engineering Analyst role: modular design, structured logging,
error handling with retries, automated testing, and containerization.

## What it does

1. **Extract** — requests current weather data for a fixed location (Fortaleza,
   Brazil) from the Open-Meteo API, with a timeout and automatic retry on
   transient failures (timeouts, connection errors, HTTP 5xx)
2. **Transform** — reshapes the API response into the flat structure the
   database expects
3. **Load** — inserts the record into `weather.weather_measurements` in
   PostgreSQL

Every stage logs its own progress and failures, tagged by module
(`extractor`, `transformer`, `loader`), to both the console and
`logs/pipeline.log`.

## Quick start (Docker)

The fastest way to run the full pipeline, database included, with nothing
installed locally except Docker:

```bash
git clone https://github.com/LucasMeneses1/weather-etl-pipeline.git
cd weather-etl-pipeline
cp .env.example .env   # fill in your own values
docker compose up
```

This starts PostgreSQL, waits until it's genuinely ready to accept connections,
seeds the schema and table automatically on first run, then runs the pipeline.
See [ADR-004](docs/decisions/ADR-004-containerization-strategy.md) and
[ADR-005](docs/decisions/ADR-005-compose-orchestration-strategy.md) for the
reasoning behind the container setup.

## Running locally (without Docker)

Useful for development and running the test suite.

**Requirements:** Python 3.11, PostgreSQL 17

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements-dev.txt
```

Create a `.env` file (see `.env.example`) pointing at your local PostgreSQL
instance, then create the schema:

> **Note:** if you've been running the project via Docker, `DB_HOST` in your
> `.env` is set to `db` (the Compose service name), which only resolves inside
> Docker's own network. Switch it back to `localhost` (or your PostgreSQL
> host) before running the pipeline this way — otherwise the connection will
> fail with `Connection refused`.

```bash
psql -U <user> -d <database> -f sql/sql001_create_database.sql
```

Run the pipeline:

```bash
python src/main.py
```

## Running tests

```bash
pytest -v
```

The suite covers the extractor (success, retry-then-recover, non-retryable
errors, and exhausted retries), the transformer, and the loader — each using
mocks, so no real network or database connection is required to run them.

## Project structure

```
weather-etl-pipeline/
├── src/                  # application code
│   ├── main.py           # orchestrates the pipeline
│   ├── extractor.py      # Open-Meteo API client, timeout + retry
│   ├── transformer.py    # reshapes API data for the database
│   ├── loader.py         # persists to PostgreSQL
│   ├── database.py       # SQLAlchemy engine
│   ├── config.py         # environment variable loading
│   └── logger.py         # logging configuration
├── tests/                # pytest suite (mocked, no external dependencies)
├── sql/                  # database schema
├── docs/decisions/       # Architecture Decision Records (ADRs)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt / requirements-dev.txt
```

## Engineering decisions

Architectural decisions are documented as ADRs in
[`docs/decisions/`](docs/decisions/) as they're made, including the reasoning
and trade-offs considered — not just the final choice:

- [ADR-001](docs/decisions/ADR-001-modular-architecture.md) — Modular ETL architecture
- [ADR-002](docs/decisions/ADR-002-centralized-logging-strategy.md) — Per-module logging
- [ADR-003](docs/decisions/ADR-003-extractor-error-handling.md) — Timeout and retry strategy
- [ADR-004](docs/decisions/ADR-004-containerization-strategy.md) — Base image and credential handling
- [ADR-005](docs/decisions/ADR-005-compose-orchestration-strategy.md) — Compose health checks and database seeding

## Tech stack

Python 3.11 · PostgreSQL 17 · SQLAlchemy · pytest · Docker & Docker Compose

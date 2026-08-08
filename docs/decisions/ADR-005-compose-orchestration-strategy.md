# ADR-005 - Compose Orchestration Strategy: Health Checks and Database Seeding

## Status

Accepted

---

## Context

Running the application and PostgreSQL as separate Compose services surfaced two
problems that only became visible at runtime, not while writing the YAML.

First, `depends_on` alone only waits for the `db` container to *start* — not for
PostgreSQL inside it to actually accept connections. In practice, `app` reached the
database before it was ready and failed with `Connection refused`, even though `db`
had technically "started" first.

Second, a freshly created `db` container boots with an empty database. The schema
and table the pipeline depends on (`weather.weather_measurements`) don't exist
until something creates them — nothing about the official Postgres image knows
about this project's specific schema.

---

## Decision

Added a `healthcheck` to the `db` service using `pg_isready`, and changed `app`'s
`depends_on` from the default (container started) to `condition: service_healthy`.
`app` now only starts once Postgres is verified to accept connections, not just
once its container process exists.

Mounted the project's existing `sql/sql001_create_database.sql` into the
container's `/docker-entrypoint-initdb.d/` directory via a volume. The official
PostgreSQL image automatically runs any `.sql` file placed there exactly once —
the first time it starts with an empty data directory — reusing the same script
already written in Sprint 01 instead of duplicating the schema definition
anywhere else.

---

## Consequences

### Advantages

- Eliminates the startup race condition entirely — `app` can no longer reach the
  database before it's genuinely ready
- A completely fresh clone of the repository can run `docker compose up` and get a
  fully working, seeded database with zero manual setup
- Single source of truth for the schema (`sql001_create_database.sql`), reused
  rather than rewritten

### Disadvantages

- The initialization script only runs against an empty data directory; anyone
  changing the schema later must remember this affects fresh databases only, not
  ones that already have data (a migration tool would be needed for that — out of
  scope for now)
- `healthcheck` adds a small delay to every `docker compose up` (the interval
  before the first successful check), even on runs where Postgres would have been
  ready sooner

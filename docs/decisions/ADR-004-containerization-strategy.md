# ADR-004 - Containerization: Base Image and Credential Handling

## Status

Accepted

---

## Context

The project ran only on machines with Python 3.11, PostgreSQL, and the
exact dependency versions installed manually — a real barrier to
reproducing the environment elsewhere. Two decisions needed to be made
while containerizing it: which base image to build on, and how the
container would obtain database credentials without exposing them.

---

## Decision

**Base image:** `python:3.11-slim` instead of the full `python:3.11`
image or the smaller `python:3.11-alpine`. Verified empirically that
all runtime dependencies (including `psycopg2-binary`) install as
pre-built `manylinux` wheels on this image, requiring no C compiler —
removing the main risk `slim` usually carries.

**Credentials:** never copied into the image. `.env` is excluded via
`.dockerignore`, and credentials are injected only at `docker run` time
via `--env-file .env` (or, later, Compose's `env_file`). The image
itself carries no secrets and is identical regardless of which
environment it runs in.

---

## Consequences

### Advantages

- `slim` keeps the image small (~150MB base) without sacrificing
  compatibility, since every dependency resolves to a binary wheel
- The same image can be shared, inspected, or pushed to a registry
  without ever leaking a database password
- Runtime credential injection means one image works across local,
  staging, or production environments — only the `--env-file` changes

### Disadvantages

- `slim` is not guaranteed to work if a future dependency lacks a
  pre-built wheel for it — would require adding build tools
  (`build-essential`) back in, increasing image size
- Forgetting `--env-file` at `docker run` time fails with a confusing
  error (`ValueError: invalid literal for int() with base 10: 'None'`)
  rather than a clear "missing credentials" message
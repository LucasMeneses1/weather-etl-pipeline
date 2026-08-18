# ADR-006 - CI Pipeline: Lazy Engine Initialization and Lint/Formatter Alignment

## Status

Accepted

---

## Context

Adding GitHub Actions CI surfaced two problems that only became visible once the
pipeline ran in a genuinely clean environment — no existing `.venv`, no real
`.env`, no locally-configured tools already agreeing with each other.

First, `database.py` built the SQLAlchemy engine as soon as it was imported,
using environment variables that don't exist on the CI runner (no `.env` is
ever committed). Even test *collection* alone — importing `loader.py`, which
imports `database.py` — crashed before a single test could run, despite every
test properly mocking `get_engine()` and never needing a real connection.

Second, `flake8` and `black` disagreed about line length by default (79 vs. 88
characters), meaning code the formatter considered correctly formatted could
still fail the linter — a confusing, contradictory signal for anyone
maintaining the pipeline.

---

## Decision

Made engine creation lazy: `database.py` now caches a module-level `engine`
variable, initialized to `None`, and `get_engine()` creates it only the first
time it's actually called — never merely by importing the module. This extends
the same principle already applied to `logger.py` since Sprint 05: importing a
module must never have side effects; only calling a function should.

Added a `.flake8` configuration file setting `max-line-length = 88`, matching
`black`'s default instead of `flake8`'s own, so the two tools agree with each
other.

---

## Consequences

### Advantages

- Importing any module in the codebase — including during test collection —
  is now safe regardless of which environment variables exist, matching how
  every other module already behaves
- `flake8` and `black` can no longer contradict each other over line length
- CI runs in a genuinely clean environment and still passes reliably, closing
  the gap between "works on my machine" and "works anywhere"

### Disadvantages

- The lazy-initialization pattern (a module-level cache, checked and
  populated inside a function) has to be remembered and reapplied if a
  similar module-level side effect is introduced later — nothing enforces it
  automatically
- The 88-character limit in `.flake8` is specific to this project's tooling
  choice (`black`); adopting a different formatter later would need this
  reconciled again

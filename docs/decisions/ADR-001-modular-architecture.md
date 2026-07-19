# ADR-001 - Adopt a Modular ETL Architecture

## Status

Accepted

---

## Context

The project requires an ETL pipeline capable of extracting weather data from an external API, transforming it and storing it in a PostgreSQL database.

Keeping all responsibilities inside a single file would make the application harder to understand, maintain and extend.

---

## Decision

The application will follow a modular architecture.

Each module is responsible for a single stage of the ETL pipeline.

- extractor.py
- transformer.py
- loader.py
- database.py
- main.py

---

## Consequences

### Advantages

- Better readability
- Easier maintenance
- Lower coupling
- Better scalability
- Easier testing

### Disadvantages

- More files to manage
- Slightly more complex project structure
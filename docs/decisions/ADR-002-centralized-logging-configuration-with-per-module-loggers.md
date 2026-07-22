# ADR-002 - Centralized Logging Configuration with Per-Module Loggers

## Status

Accepted

---

## Context

The application needs structured logging to trace pipeline execution and diagnose failures. The initial implementation (`logger.py`, Sprint 04) configured logging once and exported a single shared `logger` object for every module to import.

This meant every log entry showed the same generic logger identity, regardless of which module (extractor, transformer, loader) actually produced it — making it hard to tell, from `pipeline.log` alone, where a given message or failure originated.

---

## Decision

`logger.py` is now responsible only for configuring the logging system (`setup_logging()`): log level, format, and handlers. It no longer exports a logger instance.

Each module creates its own logger instead:

    import logging
    logger = logging.getLogger(__name__)

`setup_logging()` is called once, as the first line of `main()`, before any other pipeline function runs. Every logging call lives inside a function — never at module import time — since a message logged at import time would fire before `setup_logging()` configures the handlers and would be silently lost.

---

## Consequences

### Advantages

- Every log line is tagged with the module that actually produced it (`extractor`, `transformer`, `loader`, `__main__`)
- Lower coupling: modules depend only on Python's standard `logging` module, not on a custom shared object
- Matches the logging convention used by most Python libraries and frameworks
- Easier to filter or route logs per component later (e.g. by module name), which will matter when integrating with tools like Azure Log Analytics / Application Insights

### Disadvantages

- One extra line (`logger = logging.getLogger(__name__)`) repeated in every module
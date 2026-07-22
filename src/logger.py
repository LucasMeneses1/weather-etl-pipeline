"""
Logging configuration for the Weather ETL Pipeline.

This module centralizes the application's logging configuration.
It creates the log directory and configures the logging system
(format, level, and handlers).

It does NOT expose a shared logger instance. Each module is
responsible for creating its own logger:

    import logging
    logger = logging.getLogger(__name__)

This keeps every log entry correctly tagged with the name of the
module that produced it (e.g. "extractor", "transformer", "loader"),
instead of every message sharing one generic identity.
"""

import logging
from pathlib import Path

LOG_DIRECTORY = Path("logs")
LOG_FILE = LOG_DIRECTORY / "pipeline.log"


def setup_logging():
    """
    Configures the root logging system for the application.

    Must be called once, as early as possible in the entry point
    (currently the first line of main(), in main.py), before any
    module emits a log message. Messages logged at module import
    time, before this function runs, would not be captured by the
    handlers configured here — they would fall through to Python's
    default "no handlers configured" behavior and effectively be
    lost. For that reason, no module in this project logs at the
    top level; every logging call lives inside a function.
    """
    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
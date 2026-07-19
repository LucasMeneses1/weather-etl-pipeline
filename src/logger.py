"""
Logging configuration for the Weather ETL Pipeline.

This module centralizes the application's logging configuration.
It creates the log directory, configures the logging system, and
exposes a shared logger instance for use across all modules.
"""

import logging
from pathlib import Path

LOG_DIRECTORY = Path("logs")
LOG_FILE = LOG_DIRECTORY / "pipeline.log"

LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
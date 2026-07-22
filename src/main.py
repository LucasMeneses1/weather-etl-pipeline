from sqlalchemy import text
from database import get_engine
from extractor import extract_weather
from transformer import transform_weather
from loader import load_weather
from logger import setup_logging

import logging

CITY_NAME = "Fortaleza"
LATITUDE = -3.7319
LONGITUDE = -38.5267


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Pipeline started")

    engine = get_engine()

    try:
        logger.info("Connecting to database")

        with engine.connect() as connection:
            logger.info("Connection established")

            result = connection.execute(text("SELECT version();"))

            for row in result:
                logger.info(f"PostgreSQL version: {row[0]}")

        extracted_data = extract_weather(LATITUDE, LONGITUDE)

        transformed_data = transform_weather(
            extracted_data, CITY_NAME, LATITUDE, LONGITUDE
        )

        load_weather(transformed_data)

        logger.info("Pipeline finished")

    except Exception as erro:
        logger.error(f"Pipeline failed: {erro}", exc_info=True)


if __name__ == "__main__":
    main()
import logging

from sqlalchemy import text
from database import get_engine

logger = logging.getLogger(__name__)


def load_weather(data: dict):
    """
    Grava uma medicao meteorologica no banco de dados.

    Args:
        data (dict): Dados transformados, incluindo city,
        latitude e longitude (colunas NOT NULL na tabela).
    """

    logger.info("Loading into PostgreSQL")

    engine = get_engine()

    try:
        with engine.begin() as connection:

            sql = text("""
                INSERT INTO weather.weather_measurements (
                    city,
                    latitude,
                    longitude,
                    observation_time,
                    temperature,
                    humidity,
                    wind_speed,
                    pressure
                )
                VALUES (
                    :city,
                    :latitude,
                    :longitude,
                    :observation_time,
                    :temperature,
                    :humidity,
                    :wind_speed,
                    :pressure
                )
            """)

            connection.execute(sql, data)

        logger.info("Insert successful")

    except Exception as erro:
        logger.error(f"Failed to insert data: {erro}")
        raise
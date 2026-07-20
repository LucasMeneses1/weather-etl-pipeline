from sqlalchemy import text
from database import get_engine


def load_weather(data: dict):
    """
    Grava uma medicao meteorologica no banco de dados.

    Args:
        data (dict): Dados transformados, incluindo city,
        latitude e longitude (colunas NOT NULL na tabela).
    """

    engine = get_engine()

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
from sqlalchemy import text
from database import get_engine


def load_weather(data: dict):
    """
    Grava uma medição meteorológica no banco de dados.

    Args:
        data (dict): Dados transformados.
    """

    engine = get_engine()

    with engine.begin() as connection:

        sql = text("""
            INSERT INTO weather.weather_measurements (
                observation_time,
                temperature,
                humidity,
                wind_speed,
                pressure
            )
            VALUES (
                :observation_time,
                :temperature,
                :humidity,
                :wind_speed,
                :pressure
            )
        """)

        # <- aqui falta apenas executar o INSERT
        connection.execute(sql, data)
        
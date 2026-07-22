import logging

logger = logging.getLogger(__name__)


def transform_weather(weather_data: dict, city: str, latitude: float, longitude: float) -> dict:
    """
    Transforma os dados meteorologicos retornados pela API
    para o formato utilizado pela aplicacao.

    Args:
        weather_data (dict): Dicionario retornado pela API.
        city (str): Nome da cidade associada a medicao.
        latitude (float): Latitude usada na consulta.
        longitude (float): Longitude usada na consulta.

    Returns:
        dict: Dicionario contendo os campos de interesse,
        incluindo a localizacao (city/latitude/longitude)
        exigida pelo schema da tabela weather_measurements.
    """

    logger.info("Transforming data")

    try:
        transformed_data = {
            "city": city,
            "latitude": latitude,
            "longitude": longitude,
            "observation_time": weather_data["current"]["time"],
            "temperature": weather_data["current"]["temperature_2m"],
            "humidity": weather_data["current"]["relative_humidity_2m"],
            "wind_speed": weather_data["current"]["wind_speed_10m"],
            "pressure": weather_data["current"]["pressure_msl"]
        }
    except (KeyError, TypeError) as erro:
        logger.error(f"Transformation failed: unexpected data format ({erro})")
        raise

    logger.info("Transformation completed")

    return transformed_data
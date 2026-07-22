import logging

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def extract_weather(latitude: float, longitude: float):

    logger.info("Extracting weather data")

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,pressure_msl"
    }

    response = requests.get(BASE_URL, params=params)

    if response.ok:
        logger.info("Weather data extracted")
        return response.json()
    else:
        logger.error(f"Extraction failed with status code {response.status_code}")
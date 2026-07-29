import logging
import time
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
    for tentativa in range(5):
        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            logger.info("Weather data extracted")
            return response.json()
        
        except requests.exceptions.HTTPError as error:
            if response.status_code <  500:
                logger.error(f"Extraction failed with status code {response.status_code}")
                raise requests.exceptions.RequestException(f"API returned status {response.status_code}")
            else:
                logger.info(f"Trying again...")
                time.sleep(3)

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                logger.info(f"Trying again...")      
                time.sleep(3)
    raise requests.exceptions.RequestException("API did not return data")
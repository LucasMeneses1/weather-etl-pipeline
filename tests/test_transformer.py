from transformer import transform_weather



CITY_NAME = "Fortaleza"
LATITUDE = -3.7319
LONGITUDE = -38.5267

current = {
            "current": {
                "time": "2026-07-23T10:00",
                "temperature_2m": 28.5,
                "relative_humidity_2m": 65,
                "wind_speed_10m": 12.3,
                "pressure_msl": 1013,
            }
        }

expected_response = {
            "city": CITY_NAME,
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "observation_time": "2026-07-23T10:00",
            "temperature": 28.5,
            "humidity": 65,
            "wind_speed": 12.3,
            "pressure": 1013
        }


def test_transform_weather():

    assert transform_weather(current, CITY_NAME, LATITUDE, LONGITUDE) == expected_response


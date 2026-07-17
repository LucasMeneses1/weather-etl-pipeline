import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def extract_weather(latitude: float, longitude: float):

    params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,pressure_msl"
}

    response = requests.get(BASE_URL, params=params)
    if response.ok:
        return response.json()
    else:
        print("Erro na requisição.")
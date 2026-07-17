def transform_weather(weather_data: dict) -> dict:
    """
    Transforma os dados meteorológicos retornados pela API
    para o formato utilizado pela aplicação.

    Args:
        weather_data (dict): Dicionário retornado pela API.

    Returns:
        dict: Dicionário contendo apenas os campos de interesse.
    """    

    transformed_data = {
        "observation_time": weather_data["current"]["time"],
        "temperature": weather_data["current"]["temperature_2m"],
        "humidity": weather_data["current"]["relative_humidity_2m"],
        "wind_speed": weather_data["current"]["wind_speed_10m"],
        "pressure": weather_data["current"]["pressure_msl"]
    }

    return transformed_data
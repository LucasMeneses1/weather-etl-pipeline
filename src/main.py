from sqlalchemy import text
from database import get_engine
from extractor import extract_weather
from transformer import transform_weather
from loader import load_weather
from logger import logger

CITY_NAME = "Fortaleza"
LATITUDE = -3.7319
LONGITUDE = -38.5267


def main():
    engine = get_engine()

    try:
        with engine.connect() as connection:

            result = connection.execute(text("SELECT version();"))

            for row in result:
                print(row[0])

        extracted_data = extract_weather(LATITUDE, LONGITUDE)

        transformed_data = transform_weather(
            extracted_data, CITY_NAME, LATITUDE, LONGITUDE
        )

        load_weather(transformed_data)

        print("\n Pipeline executado e dados gravados com sucesso.")

    except Exception as erro:
        print(f"\n ERRO AO CONECTAR: {erro}")


if __name__ == "__main__":
    main()
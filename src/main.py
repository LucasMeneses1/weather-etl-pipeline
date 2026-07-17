from extractor import extract_weather


def main():
    weather = extract_weather(
        latitude=52.52,
        longitude=13.41
    )

    print(weather["current"])


if __name__ == "__main__":
    main()
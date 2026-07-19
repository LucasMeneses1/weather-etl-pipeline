# Weather ETL Pipeline

A modular ETL pipeline developed in Python that extracts real-time weather data from the Open-Meteo API, transforms it into a structured format and loads it into a PostgreSQL database using SQLAlchemy.

This project was developed as part of a Data Engineering learning journey with a focus on software architecture, clean code, version control and engineering best practices.

## Architecture

The application follows a modular ETL architecture in which each module is responsible for a single stage of the data pipeline.

```text
(Open-Meteo API)
        │
        ▼
 extractor.py
        │
        ▼
transformer.py
        │
        ▼
 loader.py
        │
        ▼
 PostgreSQL
```
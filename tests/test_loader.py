from unittest.mock import Mock, patch, MagicMock
import pytest
from loader import load_weather

fake_engine = MagicMock()
fake_connection = MagicMock()
fake_engine.begin.return_value.__enter__.return_value = fake_connection
sample_data = {
            "city": "Fortaleza",
            "latitude": -3.7319,
            "longitude": -38.5267,
            "observation_time": "2026-07-23T10:00",
            "temperature": 28.5,
            "humidity": 65,
            "wind_speed": 12.3,
            "pressure": 1013
        }

def test_loader_insert():
    with patch("loader.get_engine", return_value = fake_engine):
        load_weather(sample_data)

    fake_connection.execute.assert_called_once()

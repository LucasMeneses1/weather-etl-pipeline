from extractor import extract_weather
from unittest.mock import Mock, patch
import pytest
import requests

LATITUDE = -3.7319
LONGITUDE = -38.5267

fake_response = Mock()
fake_response.raise_for_status.return_value = None
fake_response.json.return_value = {
                                    'latitude': -3.7609842, 
                                    'longitude': -38.529663, 
                                    'generationtime_ms': 0.05841255187988281, 
                                    'utc_offset_seconds': 0, 
                                    'timezone': 'GMT', 
                                    'timezone_abbreviation': 'GMT', 
                                    'elevation': 21.0, 
                                    'current_units': {
                                                        'time': 'iso8601', 
                                                        'interval': 
                                                        'seconds', 
                                                        'temperature_2m': '°C', 
                                                        'relative_humidity_2m': '%', 
                                                        'wind_speed_10m': 'km/h', 
                                                        'pressure_msl': 'hPa'
                                                     }, 
                                                        'current': {
                                                                        'time': '2026-07-26T17:30', 
                                                                        'interval': 900, 
                                                                        'temperature_2m': 29.0, 
                                                                        'relative_humidity_2m': 66, 
                                                                        'wind_speed_10m': 20.0, 
                                                                        'pressure_msl': 1012.0
                                                                   }
                                 }


def test_extract_weather_success():

    with patch("extractor.requests.get", return_value = fake_response), patch("extractor.time.sleep"):
        assert extract_weather(LATITUDE, LONGITUDE) == fake_response.json.return_value


def test_extract_weather_timeout():

    with patch("extractor.requests.get", side_effect = [requests.exceptions.Timeout("Simulating issue..."), fake_response]), patch("extractor.time.sleep"):
        assert extract_weather(LATITUDE, LONGITUDE) == fake_response.json.return_value
    

def test_extract_weather_HTTPError_404():
    fake_response_404 = Mock()
    fake_response_404.status_code = 404
    fake_response_404.raise_for_status.side_effect = requests.exceptions.HTTPError
    with patch("extractor.requests.get", return_value = fake_response_404) as mock_get, patch("extractor.time.sleep"), pytest.raises(requests.exceptions.RequestException):
        
        extract_weather(LATITUDE, LONGITUDE)

    assert mock_get.call_count == 1

def test_extract_weather_HTTPError_500():
    fake_response_500 = Mock()
    fake_response_500.status_code = 500
    fake_response_500.raise_for_status.side_effect = requests.exceptions.HTTPError
    with patch("extractor.requests.get", return_value = fake_response_500) as mock_get, patch("extractor.time.sleep"), pytest.raises(requests.exceptions.RequestException):
        
        extract_weather(LATITUDE, LONGITUDE)

    assert mock_get.call_count == 5
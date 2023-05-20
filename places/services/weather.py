import requests
from django.conf import settings
from dataclasses import dataclass


@dataclass
class WeatherData:
    temp_c: float
    humidity: int
    pressure_mb: float
    wind_direction: str
    wind_kph: float


def _parse_weather_from_response(response: requests.Response) -> WeatherData:
    json = response.json()
    current_data = json['current']
    return WeatherData(
        temp_c=current_data['temp_c'],
        humidity=current_data['humidity'],
        pressure_mb=current_data['pressure_mb'],
        wind_direction=current_data['wind_dir'],
        wind_kph=current_data['wind_kph']
    )


def try_retrieve_weather(latitude: float, longitude: float) -> WeatherData:
    """
    Can raise RequestException
    """

    key = settings.WEATHER_API_KEY
    provider = settings.WEATHER_PROVIDER
    params = {
        'key': key,
        'q': f'{latitude},{longitude}',
        'aqi': 'no'  # Dont call air quality data
    }

    response = requests.get(provider, params=params)
    response.raise_for_status()

    return _parse_weather_from_response(response)

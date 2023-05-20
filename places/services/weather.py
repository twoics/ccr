import requests
import xlsxwriter
from django.conf import settings
from dataclasses import dataclass
from ..models import Weather, Places
from datetime import datetime


@dataclass
class WeatherData:
    temp_c: float
    humidity: int
    pressure_mb: float
    wind_direction: str
    wind_kph: float

    def to_kwargs(self):
        return {
            Weather.temperature_c.field.name: self.temp_c,
            Weather.humidity.field.name: self.humidity,
            Weather.pressure_mb.field.name: self.pressure_mb,
            Weather.wind_direction.field.name: self.wind_direction,
            Weather.wind_kph.field.name: self.wind_kph,
            Weather.measure_date.field.name: datetime.now()
        }


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


def create_weather(weather_data: WeatherData, place: Places) -> Weather:
    kwargs_data = weather_data.to_kwargs()

    place_name = Weather.place.field.name
    kwargs_data[place_name] = place

    return Weather.objects.create(
        **kwargs_data
    )


def export_weather() -> str:
    """
    :return: Path to generated file
    """
    headers = [f.name for f in Weather._meta.get_fields()]

    def create_header(work_sheet):
        for col_num, data in enumerate(headers):
            work_sheet.write(0, col_num, data)

    weather_query = Weather.objects.select_related('place').order_by(
        'place__title', 'measure_date'
    )

    # TODO CHECK QUERY COUNT
    workbook = xlsxwriter.Workbook(settings.PATH_WEATHER_XLSX)
    worksheet = workbook.add_worksheet()
    create_header(worksheet)

    for index, weather in enumerate(weather_query):
        weather_dict = weather.__dict__
        weather_dict['place'] = weather.place.title
        string_time = weather_dict['measure_date'].strftime('%m/%d/%Y/%H:%M:%S')
        weather_dict['measure_date'] = string_time
        for weather_name in headers:
            worksheet.write(index + 1, headers.index(weather_name), weather_dict[weather_name])

    workbook.close()
    return settings.PATH_WEATHER_XLSX

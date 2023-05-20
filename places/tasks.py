from .models import Places
from ccr.celery import app
from .services import create_weather, try_retrieve_weather


@app.task
def retrieve_weather_in_places():
    for place in Places.objects.all():
        place_weather_data = try_retrieve_weather(
            latitude=place.latitude,
            longitude=place.longitude
        )

        create_weather(place_weather_data, place)

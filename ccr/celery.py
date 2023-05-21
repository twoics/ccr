import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from constance import config


def convert_minutes_to_seconds(float_minutes: float) -> int:
    minutes, seconds = divmod(float_minutes * 60, 3600)
    return minutes * 60 + seconds


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ccr.settings')

app = Celery('ccr')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-daily-email': {
        'task': 'news.tasks.send_daily_email',
        'schedule': crontab(
            minute=config.SEND_TIME.minute,
            hour=config.SEND_TIME.hour
        ),
    },

    'retrieve-weather-in-places': {
        'task': 'places.tasks.retrieve_weather_in_places',
        'schedule': timedelta(
            seconds=convert_minutes_to_seconds(60 / config.WEATHER_RECEIVE_FREQUENCY)
        )
    }
}

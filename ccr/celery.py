import os
from celery import Celery
from celery.schedules import crontab
from constance import config

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
        'schedule': crontab(
            minute=f'*/{int(60 / config.WEATHER_RECEIVE_FREQUENCY)}'
        ),
    }
}
# TODO Calculate frequency func

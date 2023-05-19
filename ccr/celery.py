import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ccr.settings')

app = Celery('ccr')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-email-if-available': {
        'task': 'news.tasks.send_email_if_available',
        'schedule': crontab(),  # Check every minute
    },
}

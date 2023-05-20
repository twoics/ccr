from constance.signals import config_updated
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask
from news.models import News


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    print('WEATHER RECEIVE')

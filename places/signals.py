from constance.signals import config_updated
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from places.models import Places
from places.tasks import try_retrieve_weather


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    print('PLACES RECEIVE')

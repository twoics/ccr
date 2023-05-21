from constance.signals import config_updated
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule
from places.tasks import retrieve_weather_in_places
from ccr.celery import convert_minutes_to_seconds


@receiver(config_updated)
def constance_updated(**kwargs):
    key = kwargs['key']
    if key != 'WEATHER_RECEIVE_FREQUENCY':
        return

    amount_in_hour = kwargs['new_value']
    task = PeriodicTask.objects.get(
        task=f'places.tasks.{retrieve_weather_in_places.__name__}'
    )
    task.interval.period = IntervalSchedule.SECONDS
    task.interval.every = convert_minutes_to_seconds(60 / amount_in_hour)
    task.interval.save()
    task.save()
    PeriodicTasks.changed(task)

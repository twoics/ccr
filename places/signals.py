from constance.signals import config_updated
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, PeriodicTasks
from places.tasks import retrieve_weather_in_places


@receiver(config_updated)
def constance_updated(**kwargs):
    key = kwargs['key']
    if key != 'WEATHER_RECEIVE_FREQUENCY':
        return

    amount_in_hour = kwargs['new_value']
    task = PeriodicTask.objects.get(
        task=f'places.tasks.{retrieve_weather_in_places.__name__}'
    )

    task.crontab.minute = f'*/{int(60 / amount_in_hour)}'
    task.crontab.save()
    task.save()
    PeriodicTasks.changed(task)

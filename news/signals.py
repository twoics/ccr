from constance.signals import config_updated
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, PeriodicTasks
from news.tasks import send_daily_email


@receiver(config_updated)
def constance_updated(**kwargs):
    key = kwargs['key']

    if key != 'SEND_TIME':
        return

    send_time = kwargs['new_value']
    task = PeriodicTask.objects.get(
        task=f'news.tasks.{send_daily_email.__name__}'
    )

    task.crontab.minute = send_time.minute
    task.crontab.hour = send_time.hour
    task.crontab.save()

    task.save()
    PeriodicTasks.changed(task)

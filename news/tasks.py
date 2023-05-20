import os
from ccr.celery import app
from constance import config
from django.core.mail import send_mail


# TODO Send email to many receivers
@app.task
def send_daily_email():
    receiver_mail = config.RECEIVERS
    # TODO Replace: get from settings
    from_email = os.environ.get('EMAIL_HOST_USER')
    subject = config.SUBJECT
    message = config.MESSAGE

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[receiver_mail],
        fail_silently=False,
    )

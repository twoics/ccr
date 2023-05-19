import os
from ccr.celery import app
from constance import config
from datetime import datetime
from django.core.mail import send_mail


@app.task
def send_daily_email():
    receiver_mail = config.RECEIVERS
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


@app.task
def send_email_if_available():
    current_time = datetime.now().time()
    if current_time.minute == config.SEND_TIME.minute:
        send_daily_email.delay()

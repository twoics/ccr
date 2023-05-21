from constance import config
from django.conf import settings
from django.core.mail import send_mail
from typing import List
from ccr.celery import app


def _parse_emails(emails: str) -> List[str]:
    # Delete spaces, delete new lines, separate by EMAIL_DIVIDER
    receivers_mail = emails.replace(' ', '').replace('\n', '').split(settings.EMAIL_DIVIDER)
    receivers_mail.remove('')  # Remove empty
    return receivers_mail


@app.task
def send_daily_email():
    receivers_mail = _parse_emails(config.RECEIVERS)
    from_email = settings.EMAIL_HOST_USER
    subject = config.SUBJECT
    message = config.MESSAGE

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=receivers_mail,
        fail_silently=False,
    )

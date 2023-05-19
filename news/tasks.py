from ccr.celery import app
from .services import send_email


@app.task
def send_daily_email(user_email: str):
    send_email(user_email)

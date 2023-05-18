from django.core.mail import send_mail


def send_email(user_email: str):
    send_mail(
        subject='Здарова меченый',
        message='Я с тобой в благородство играть не буду',
        from_email='ccr.smtp@mail.ru',
        recipient_list=[user_email],
        fail_silently=False,
    )

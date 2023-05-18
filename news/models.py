from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class News(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='News title',
        null=False
    )

    main_image = models.ImageField(
        verbose_name='Main image',
        upload_to='news_images/main/%Y/%m/%d',
        null=False,

    )

    preview = models.ImageField(
        verbose_name='Preview',
        upload_to='news_images/preview/%Y/%m/%d',
        null=False,
    )

    text = models.TextField(
        verbose_name='News text'
    )

    publish_day = models.DateTimeField(
        verbose_name='Publish day',
        default=datetime.now
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author'
    )

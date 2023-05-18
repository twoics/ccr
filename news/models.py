from PIL import Image
from typing import Tuple
from django.core.files.images import ImageFile
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

TARGET_MIN_SIDE_SIZE = 200


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

    @staticmethod
    def _get_output_size(image) -> Tuple[int, int]:
        is_width_smaller = image.width < image.height

        if is_width_smaller:
            return TARGET_MIN_SIDE_SIZE, image.height
        return image.width, TARGET_MIN_SIDE_SIZE

    def save(self, *args, **kwargs):
        self.preview = ImageFile(self.main_image.file)
        super().save()

        source_img = Image.open(self.preview.file)
        output_size = self._get_output_size(source_img)
        source_img.thumbnail(output_size)
        source_img.save(self.preview.file.name)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return f'News {self.title} by {self.author.username}'

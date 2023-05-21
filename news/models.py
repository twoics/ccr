from PIL import Image
from typing import Tuple
from django.core.files.images import ImageFile
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class News(models.Model):
    __previous_image = None
    __TARGET_MIN_SIDE_SIZE = 200

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

    author = models.CharField(
        verbose_name='Author',
        max_length=100
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__previous_image = self.main_image

    def _get_output_size(self, image) -> Tuple[int, int]:
        is_width_smaller = image.width < image.height

        if is_width_smaller:
            return self.__TARGET_MIN_SIDE_SIZE, image.height
        return image.width, self.__TARGET_MIN_SIDE_SIZE

    def save(self, *args, **kwargs):
        if not self.preview.name or self.main_image != self.__previous_image:
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
        return f'News {self.title} by {self.author}'

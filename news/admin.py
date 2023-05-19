from django.contrib import admin
from .models import News
from django_summernote.admin import SummernoteModelAdmin


@admin.register(News)
class News(SummernoteModelAdmin):
    summernote_fields = (
        'text',
    )

    list_display = [
        'id',
        'author',
        'title',
        'main_image',
        'preview'
    ]

    exclude = [
        'preview'
    ]

from django.contrib import admin
from .models import News


@admin.register(News)
class News(admin.ModelAdmin):
    list_display = [
        'id',
        'main_image',
        'preview'
    ]

    exclude = [
        'preview'
    ]

from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    preview = serializers.ImageField(
        read_only=True
    )

    class Meta:
        model = News
        fields = (
            'id',
            'title',
            'main_image',
            'preview',
            'text',
            'publish_day',
            'author'
        )

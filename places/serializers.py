from .validators import XlsxValidator
from rest_framework import serializers
from .models import Places


class PlaceSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    title = serializers.CharField(
        read_only=True
    )

    rating = serializers.IntegerField(
        read_only=True
    )

    latitude = serializers.FloatField(
        read_only=True
    )

    longitude = serializers.FloatField(
        read_only=True
    )

    xlsx_file = serializers.FileField(
        write_only=True
    )

    validators = [
        XlsxValidator()
    ]

    class Meta:
        model = Places
        fields = (
            'id',
            'title',
            'rating',
            'latitude',
            'longitude',
            'xlsx_file'
        )

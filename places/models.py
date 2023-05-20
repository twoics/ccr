from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django_admin_geomap import GeoItem


class Places(models.Model, GeoItem):
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Title'
    )

    latitude = models.FloatField(
        verbose_name="Latitude",
        null=False,
        validators=[
            MaxValueValidator(90.0),
            MinValueValidator(-90.0)
        ]
    )

    longitude = models.FloatField(
        verbose_name="Longitude",
        null=False,
        validators=[
            MaxValueValidator(180.0),
            MinValueValidator(-180.0)
        ]
    )

    rating = models.IntegerField(
        null=False,
        verbose_name="Rating",
        validators=[
            MaxValueValidator(25),
            MinValueValidator(0)
        ]
    )

    @property
    def geomap_longitude(self):
        return '' if self.longitude is None else str(round(self.longitude))

    @property
    def geomap_latitude(self):
        return '' if self.latitude is None else str(self.latitude)

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"

    def __str__(self):
        return f'Place {self.title}'


class Weather(models.Model):
    temperature_c = models.FloatField(
        verbose_name='Temperature C',
        null=False
    )

    humidity = models.IntegerField(
        verbose_name='Humidity',
        null=False
    )

    pressure_mb = models.FloatField(
        verbose_name='Pressure millibars',
        null=False
    )

    wind_direction = models.CharField(
        verbose_name='Wind direction',
        max_length=10,
        null=False
    )

    wind_kph = models.FloatField(
        verbose_name='Wind speed (kph)',
        null=False
    )

    measure_date = models.DateTimeField(
        verbose_name='Measure day',
        null=False
    )

    place = models.ForeignKey(
        Places,
        on_delete=models.CASCADE,
        verbose_name='Place of measurement weather'
    )

    class Meta:
        verbose_name = 'Weather'
        verbose_name_plural = 'Weather'

    def __str__(self):
        return f'Weather at {self.place.title}'

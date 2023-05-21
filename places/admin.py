from django.contrib import admin
from django_admin_geomap import ModelAdmin
from .models import Places, Weather

from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
    PeriodicTask,
)

admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)


@admin.register(Places)
class PlacesAdmin(ModelAdmin):
    geomap_field_longitude = "id_longitude"
    geomap_field_latitude = "id_latitude"
    geomap_show_map_on_list = False


@admin.register(Weather)
class News(admin.ModelAdmin):
    list_display = [
        'id',
        'temperature_c',
        'humidity',
        'pressure_mb',
        'wind_direction',
        'wind_kph',
        'measure_date',
        'place'
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# admin.py
from django.contrib import admin
from django_admin_geomap import ModelAdmin
from .models import Places


class Admin(ModelAdmin):
    geomap_field_longitude = "id_longitude"
    geomap_field_latitude = "id_latitude"
    geomap_show_map_on_list = False


admin.site.register(Places, Admin)

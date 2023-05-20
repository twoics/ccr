from django.urls import path
from .views import PlacesApiView, weather_xlsx

urlpatterns = [
    path('places/', PlacesApiView.as_view(), name='import_place'),
    path('weather-xlsx/', weather_xlsx, name='weather-xlsx')
]

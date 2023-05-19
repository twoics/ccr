from django.urls import path
from .views import PlacesApiView

urlpatterns = [
    path('places/', PlacesApiView.as_view(), name='import_place')
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import NewsViewSet

news_router = DefaultRouter()
news_router.register(r'', NewsViewSet, basename='News')

urlpatterns = [
    path('news/', include(news_router.urls))
]

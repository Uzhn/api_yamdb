from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import TitleViewSet, GenreViewSet, CategoryViewSet

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('title', TitleViewSet)
v1_router.register('genre', GenreViewSet)
v1_router.register('category',CategoryViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
]
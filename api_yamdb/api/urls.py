from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import (UserViewSet, user_registration, get_token_for_user,
                       TitleViewSet, GenreViewSet, CategoryViewSet
                       )


app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'title', TitleViewSet)
router.register(r'genre', GenreViewSet)
router.register(r'category', CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', user_registration),
    path('auth/token/', get_token_for_user),
]

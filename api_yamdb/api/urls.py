from django.urls import path, include

from rest_framework import routers

from api.views import UserViewSet, user_registration, get_token_for_user


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', user_registration),
    path('auth/token/', get_token_for_user),
]

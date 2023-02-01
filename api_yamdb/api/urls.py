from rest_framework import routers

from django.urls import path, include

from api.views import ReviewsViewSet

router_api_v01 = routers.DefaultRouter()
router_api_v01.register(r'titles/(?P<title_id>[\d]{1,})/reviews',
                        ReviewsViewSet, basename='reviews')

urlpatterns = [
    path('', include(router_api_v01.urls))
]

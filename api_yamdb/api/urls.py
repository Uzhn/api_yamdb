from rest_framework import routers

from django.urls import path, include

from api.views import ReviewsViewSet, CommentViewSet, TitlesViewSet

router_api_v01 = routers.DefaultRouter()
router_api_v01.register(r'titles/(?P<title_id>[\d]{1,})/reviews',
                        ReviewsViewSet, basename='reviews')
router_api_v01.register(r'titles/(?P<title_id>[\d]{1,})/reviews/(?P<review_id>[\d]{1,})/comments',
                        CommentViewSet, basename='comments')
router_api_v01.register(r'titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('', include(router_api_v01.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
